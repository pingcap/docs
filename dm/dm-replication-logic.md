---
title: DML Replication Mechanism in Data Migration
summary: DM のコア処理ユニット Sync が DML ステートメントを複製する方法について説明します。
---

# データ移行におけるDMLレプリケーションメカニズム {#dml-replication-mechanism-in-data-migration}

このドキュメントでは、DM のコア処理ユニット Sync が、データ ソースまたはリレー ログから読み取られた DML ステートメントを処理する方法を紹介します。このドキュメントでは、binlogの読み取り、フィルタリング、ルーティング、変換、最適化、実行のロジックを含む、DM の DML イベントの完全な処理フローを紹介します。また、このドキュメントでは、DML 最適化ロジックと DML 実行ロジックについても詳しく説明します。

## DML処理フロー {#dml-processing-flow}

Sync ユニットは、DML ステートメントを次のように処理します。

1.  MySQL、MariaDB、またはリレー ログからbinlogイベントを読み取ります。

2.  データ ソースから読み取ったbinlogイベントを変換します。

    1.  [Binlogフィルター](/dm/dm-binlog-event-filter.md) : `filters`で設定されたbinlog式に従ってbinlogイベントをフィルタリングします。
    2.  [テーブルルーティング](/dm/dm-table-routing.md) : `routes`で設定された「データベース/テーブル」ルーティング ルールに従って「データベース/テーブル」名を変換します。
    3.  [表現フィルター](/filter-dml-event.md) : `expression-filter`で設定された SQL 式に従ってbinlogイベントをフィルタリングします。

3.  DML 実行プランを最適化します。

    1.  [圧縮機](#compactor) : 同じレコード (同じ主キーを持つ) に対する複数の操作を 1 つの操作にマージします。この機能は`syncer.compact`によって有効になります。
    2.  [因果関係](#causality) : レプリケーションの同時実行性を向上させるために、異なるレコード (異なる主キーを持つ) に対して競合検出を実行します。
    3.  [合併](#merger) : 複数のbinlogイベントを 1 つの DML ステートメントにマージします`syncer.multiple-rows`によって有効になります。

4.  DML をダウンストリームに実行します。

5.  定期的に、binlogの位置または GTID をチェックポイントに保存します。

![DML processing logic](/media/dm/dm-dml-replication-logic.png)

## DML最適化ロジック {#dml-optimization-logic}

同期ユニットは、Compactor、Causality、Merger の 3 つのステップを通じて DML 最適化ロジックを実装します。

### 圧縮機 {#compactor}

アップストリームのbinlogレコードに従って、DM はレコードの変更をキャプチャし、ダウンストリームに複製します。アップストリームが短期間に同じレコードに複数の変更 ( `INSERT` / `UPDATE` / `DELETE` ) を加えた場合、DM は Compactor を通じて複数の変更を 1 つの変更に圧縮し、ダウンストリームへの負荷を軽減してスループットを向上させることができます。例:

    INSERT + UPDATE => INSERT
    INSERT + DELETE => DELETE
    UPDATE + UPDATE => UPDATE
    UPDATE + DELETE => DELETE
    DELETE + INSERT => UPDATE

デフォルトでは、Compactor 機能は無効になっています。有効にするには、以下に示すように、レプリケーション タスクの`sync`構成モジュールで`syncer.compact`から`true`を設定します。

```yaml
syncers:                            # The configuration parameters of the sync processing unit
  global:                           # Configuration name
    ...                              # Other configurations are omitted
    compact: true
```

### 因果関係 {#causality}

MySQL binlogのシーケンシャル レプリケーション モデルでは、 binlogイベントをbinlogの順序でレプリケートする必要があります。このレプリケーション モデルでは、高い QPS と低いレプリケーションレイテンシーの要件を満たすことができません。また、 binlogに関係するすべての操作に競合が発生するわけではないため、そのような場合にはシーケンシャル レプリケーションは必要ありません。

DM は、競合検出を通じて順次実行する必要があるbinlogを認識し、他のbinlogの同時実行性を最大限に高めながら、これらのbinlogが順次実行されるようにします。これにより、binlogログのレプリケーションのパフォーマンスが向上します。

Causality は、union-find アルゴリズムに似たアルゴリズムを採用して、各 DML を分類し、相互に関連する DML をグループ化します。

### 合併 {#merger}

MySQL のbinlogプロトコルによれば、各binlogは1 行のデータの変更操作に対応します。Merger を使用すると、DM は複数のバイナリログを 1 つの DML にマージして下流に実行し、ネットワークの相互作用を減らすことができます。例:

      INSERT tb(a,b) VALUES(1,1);
    + INSERT tb(a,b) VALUES(2,2);
    = INSERT tb(a,b) VALUES(1,1),(2,2);
      UPDATE tb SET a=1, b=1 WHERE a=1;
    + UPDATE tb SET a=2, b=2 WHERE a=2;
    = INSERT tb(a,b) VALUES(1,1),(2,2) ON DUPLICATE UPDATE a=VALUES(a), b=VALUES(b)
      DELETE tb WHERE a=1
    + DELETE tb WHERE a=2
    = DELETE tb WHERE (a) IN (1),(2);

マージャー機能はデフォルトで無効になっています。有効にするには、以下に示すように、レプリケーション タスクの`sync`構成モジュールで`syncer.multiple-rows`から`true`を設定します。

```yaml
syncers:                            # The configuration parameters of the sync processing unit
  global:                           # Configuration name
    ...                              # Other configurations are omitted
    multiple-rows: true
```

## DML実行ロジック {#dml-execution-logic}

同期ユニットは DML を最適化した後、実行ロジックを実行します。

### DML生成 {#dml-generation}

DM には、上流と下流のスキーマ情報を記録するスキーマ トラッカーが組み込まれています。

-   DM は DDL ステートメントを受信すると、内部スキーマ トラッカーのテーブル スキーマを更新します。
-   DM は DML ステートメントを受信すると、スキーマ トラッカーのテーブル スキーマに従って対応する DML を生成します。

DML を生成するロジックは次のとおりです。

1.  Sync ユニットは、アップストリームの初期テーブル構造を記録します。
    -   完全タスクと増分タスクを開始すると、Sync は**アップストリームの完全データ移行中にエクスポートされたテーブル構造を**アップストリームの初期テーブル構造として使用します。
    -   増分タスクを開始すると、MySQL binlog にテーブル構造情報が記録されないため、Sync は**下流の対応するテーブルのテーブル構造を**上流の初期テーブル構造として使用します。
2.  ユーザーの上流と下流のテーブル構造が不一致である可能性があります。たとえば、下流に上流よりも多くの列がある場合や、上流と下流の主キーが不一致である場合があります。そのため、データ複製の正確性を確保するために、DM は**下流の対応するテーブルの主キーと一意のキー情報を**記録します。
3.  DM は DML を生成します:
    -   **スキーマ トラッカーに記録されたアップストリーム テーブル構造を**使用して、DML ステートメントの列名を生成します。
    -   **binlogに記録された列の値を**使用して、DML ステートメントの列の値を生成します。
    -   **スキーマ トラッカーに記録されたダウンストリーム プライマリ キーまたは一意のキー**を使用して、DML ステートメントの`WHERE`の条件を生成します。テーブル構造に一意のキーがない場合、DM はbinlogに記録されたすべての列値を`WHERE`の条件として使用します。

### 労働者数 {#worker-count}

Causality は、競合検出を通じてbinlogを複数のグループに分割し、下流に同時に実行することができます。DM は`worker-count`設定することで同時実行を制御します。下流 TiDB の CPU 使用率が高くない場合は、同時実行を増やすことでデータ複製のスループットを効果的に向上させることができます。

[`syncer.worker-count`設定項目](/dm/dm-tune-configuration.md#worker-count)を変更することで、DML を同時に移行するスレッドの数を変更できます。

### バッチ {#batch}

DM は、複数の DML を 1 つのトランザクションにまとめて、ダウンストリームに実行します。DML ワーカーが DML を受信すると、DML をキャッシュに追加します。キャッシュ内の DML の数が事前に設定されたしきい値に達するか、DML ワーカーが長時間 DML を受信しない場合、DML ワーカーはキャッシュ内の DML をダウンストリームに実行します。

[`syncer.batch`設定項目](/dm/dm-tune-configuration.md#batch)変更することで、トランザクションに含まれる DML の数を変更できます。

### チェックポイント {#checkpoint}

DML を実行してチェックポイントを更新する操作はアトミックではありません。

DM では、チェックポイントはデフォルトで 30 秒ごとに更新されます。複数の DML ワーカー プロセスがあるため、チェックポイント プロセスはすべての DML ワーカーの最も早いレプリケーション進行のbinlog位置を計算し、この位置を現在のレプリケーション チェックポイントとして使用します。この位置より前のすべてのバイナリ ログは、ダウンストリームに正常に実行されることが保証されます。

<!-- For details on checkpoint mechanism, refer to Checkpoint /dm/dm-checkpoint.md -->

## ノート {#notes}

### トランザクションの一貫性 {#transaction-consistency}

DM は行レベルでデータを複製し、トランザクションの一貫性を保証しません。DM では、上流トランザクションは複数の行に分割され、同時実行のために異なる DML ワーカーに分散されます。そのため、DM レプリケーション タスクがエラーを報告して一時停止した場合、またはユーザーが手動でタスクを一時停止した場合、下流は中間状態になる可能性があります。つまり、上流トランザクションの DML ステートメントが下流に部分的に複製され、下流が不整合な状態になる可能性があります。

タスクが一時停止されているときにダウンストリームが可能な限り一貫した状態になるように、DM v5.3.0 以降では、DM はタスクを一時停止する前に 10 秒間待機し、アップストリームからのすべてのトランザクションがダウンストリームに複製されるようにします。ただし、トランザクションが 10 秒以内にダウンストリームに複製されない場合、ダウンストリームは依然として不整合な状態のままになる可能性があります。

### セーフモード {#safe-mode}

DML 実行とチェックポイント更新の操作はアトミックではなく、チェックポイント更新と下流へのデータ書き込みの操作もアトミックではありません。DM が異常終了すると、チェックポイントは終了時刻前の回復ポイントのみを記録する可能性があります。そのため、タスクが再開されると、DM は同じデータを複数回書き込む可能性があります。これは、DM が実際には「少なくとも 1 回の処理」ロジックを提供し、同じデータが複数回処理される可能性があることを意味します。

データが再入可能であることを確認するために、DM は異常終了から再起動するときにセーフ モードに入ります。<!--For the specific logic, refer to [DM Safe Mode](/dm/dm-safe-mode.md).-->

セーフ モードが有効になっている場合、データが複数回処理されるように、DM は次の変換を実行します。

-   アップストリームの`INSERT`番目のステートメントを`REPLACE`ステートメントに書き換えます。
-   アップストリームの`UPDATE`ステートメントを`DELETE` + `REPLACE`ステートメントに書き換えます。

### 正確に1回だけ処理 {#exactly-once-processing}

現在、DM は最終的な一貫性のみを保証しており、「正確に 1 回の処理」や「トランザクションの元の順序の維持」はサポートしていません。
