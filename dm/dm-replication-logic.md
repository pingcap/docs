---
title: DML Replication Mechanism in Data Migration
summary: Learn how the core processing unit Sync in DM replicates DML statements.
---

# データ移行における DML レプリケーション メカニズム {#dml-replication-mechanism-in-data-migration}

このドキュメントでは、DM のコア処理ユニット Sync が、データ ソースまたはリレー ログから読み取られた DML ステートメントを処理する方法を紹介します。このドキュメントでは、binlogの読み取り、フィルタリング、ルーティング、変換、最適化、実行のロジックを含む、DM における DML イベントの完全な処理フローを紹介します。このドキュメントでは、DML 最適化ロジックと DML 実行ロジックについても詳しく説明します。

## DML処理の流れ {#dml-processing-flow}

同期ユニットは、DML ステートメントを次のように処理します。

1.  MySQL、MariaDB、またはリレー ログからbinlogイベントを読み取ります。

2.  データ ソースから読み取ったbinlogイベントを変換します。

    1.  [Binlogフィルター](/dm/dm-binlog-event-filter.md) : `filters`で構成されたbinlog式に従ってbinlogイベントをフィルタリングします。
    2.  [テーブルルーティング](/dm/dm-table-routing.md) : `routes`で構成された「データベース/テーブル」ルーティング ルールに従って「データベース/テーブル」名を変換します。
    3.  [式フィルター](/filter-dml-event.md) : `expression-filter`で構成された SQL 式に従ってbinlogイベントをフィルタリングします。

3.  DML 実行計画を最適化します。

    1.  [コンパクター](#compactor) : 同じレコード (同じ主キーを持つ) に対する複数の操作を 1 つの操作にマージします。この機能は`syncer.compact`によって有効になります。
    2.  [因果関係](#causality) : レプリケーションの同時実行性を向上させるために、異なるレコード (異なる主キーを持つ) で競合検出を実行します。
    3.  [合併](#merger) : 複数のbinlogイベントを 1 つの DML ステートメントにマージします。 `syncer.multiple-rows`で有効になります。

4.  DMLをダウンストリームに実行します。

5.  定期的にbinlogの位置または GTID をチェックポイントに保存します。

![DML processing logic](/media/dm/dm-dml-replication-logic.png)

## DML最適化ロジック {#dml-optimization-logic}

同期ユニットは、コンパクター、因果関係、マージャーの 3 つのステップを通じて DML 最適化ロジックを実装します。

### コンパクター {#compactor}

アップストリームのbinlogレコードに従って、DM はレコードの変更をキャプチャし、それらをダウンストリームに複製します。アップストリームが短期間に同じレコード ( `INSERT` / `UPDATE` / `DELETE` ) に複数の変更を加えた場合、DM は Compactor を通じて複数の変更を 1 つの変更に圧縮して、ダウンストリームへの負担を軽減し、スループットを向上させることができます。例えば：

    INSERT + UPDATE => INSERT
    INSERT + DELETE => DELETE
    UPDATE + UPDATE => UPDATE
    UPDATE + DELETE => DELETE
    DELETE + INSERT => UPDATE

コンパクタ機能はデフォルトでは無効になっています。これを有効にするには、以下に示すように、レプリケーション タスクの`sync`構成モジュールで`syncer.compact` ～ `true`を設定します。

```yaml
syncers:                            # The configuration parameters of the sync processing unit
  global:                           # Configuration name
    ...                              # Other configurations are omitted
    compact: true
```

### 因果関係 {#causality}

MySQL binlogのシーケンシャル レプリケーション モデルでは、 binlogイベントがbinlogの順序でレプリケートされる必要があります。このレプリケーション モデルは、高い QPS と低いレプリケーションレイテンシーの要件を満たすことができません。さらに、 binlogに関係するすべての操作に競合があるわけではないため、そのような場合には順次レプリケーションは必要ありません。

DM は、競合検出によって順次実行する必要があるbinlog を認識し、他のbinlogの同時実行性を最大化しながら、これらのbinlog が順次実行されるようにします。これは、binlogレプリケーションのパフォーマンスの向上に役立ちます。

Causality では、union-find アルゴリズムと同様のアルゴリズムを採用して、各 DML を分類し、相互に関連する DML をグループ化します。

### 合併 {#merger}

MySQL binlogプロトコルによれば、各binlog は1 行のデータの変更操作に対応します。 Merger を通じて、DM は複数のバイナリログを 1 つの DML にマージし、それをダウンストリームに実行することで、ネットワークのやり取りを軽減できます。例えば：

      INSERT tb(a,b) VALUES(1,1);
    + INSERT tb(a,b) VALUES(2,2);
    = INSERT tb(a,b) VALUES(1,1),(2,2);
      UPDATE tb SET a=1, b=1 WHERE a=1;
    + UPDATE tb SET a=2, b=2 WHERE a=2;
    = INSERT tb(a,b) VALUES(1,1),(2,2) ON DUPLICATE UPDATE a=VALUES(a), b=VALUES(b)
      DELETE tb WHERE a=1
    + DELETE tb WHERE a=2
    = DELETE tb WHERE (a) IN (1),(2);

マージ機能はデフォルトでは無効になっています。これを有効にするには、以下に示すように、レプリケーション タスクの`sync`構成モジュールで`syncer.multiple-rows` ～ `true`を設定します。

```yaml
syncers:                            # The configuration parameters of the sync processing unit
  global:                           # Configuration name
    ...                              # Other configurations are omitted
    multiple-rows: true
```

## DML実行ロジック {#dml-execution-logic}

同期ユニットは DML を最適化した後、実行ロジックを実行します。

### DMLの生成 {#dml-generation}

DM には、アップストリームとダウンストリームのスキーマ情報を記録するスキーマ トラッカーが組み込まれています。

-   DM が DDL ステートメントを受信すると、DM は内部スキーマ トラッカーのテーブル スキーマを更新します。
-   DM が DML ステートメントを受信すると、DM はスキーマ トラッカーのテーブル スキーマに従って対応する DML を生成します。

DML 生成のロジックは次のとおりです。

1.  同期ユニットは、アップストリームの初期テーブル構造を記録します。
    -   完全タスクおよび増分タスクを開始する場合、同期**はアップストリームの完全データ移行中にエクスポートされたテーブル構造を**アップストリームの初期テーブル構造として使用します。
    -   インクリメンタルタスクを開始するとき、MySQL binlog はテーブル構造情報を記録しないため、Sync は**ダウンストリームの対応するテーブルのテーブル構造をアップ**ストリームの初期テーブル構造として使用します。
2.  ユーザーの上流と下流のテーブル構造が矛盾している可能性があります。たとえば、下流に上流よりも追加の列があるか、上流と下流の主キーが一致していない可能性があります。したがって、データ レプリケーションの正確性を保証するために、DM は**対応するテーブルの主キーと一意のキー情報をダウンストリームに**記録します。
3.  DM は DML を生成します。
    -   **スキーマ トラッカーに記録されたアップストリーム テーブル構造を**使用して、DML ステートメントの列名を生成します。
    -   **binlogに記録された列値を**使用して、DML ステートメントの列値を生成します。
    -   **スキーマ トラッカーに記録されたダウンストリーム主キーまたは一意キーを**使用して、DML ステートメントの`WHERE`の条件を生成します。テーブル構造に一意のキーがない場合、DM はbinlogに記録されたすべての列値を条件`WHERE`として使用します。

### 従業員数 {#worker-count}

Causality は、競合検出を通じてbinlog を複数のグループに分割し、ダウンストリームに対して同時に実行できます。 DM は`worker-count`を設定することで同時実行性を制御します。ダウンストリーム TiDB の CPU 使用率が高くない場合、同時実行性を高めることで、データ レプリケーションのスループットを効果的に向上させることができます。

[`syncer.worker-count`構成アイテム](/dm/dm-tune-configuration.md#worker-count)を変更することで、DML を同時に移行するスレッドの数を変更できます。

### バッチ {#batch}

DM は複数の DML を 1 つのトランザクションにまとめて、ダウンストリームに実行します。 DML ワーカーは DML を受信すると、その DML をキャッシュに追加します。キャッシュ内の DML の数が事前に設定されたしきい値に達するか、DML ワーカーが長時間 DML を受信しない場合、DML ワーカーはキャッシュ内の DML をダウンストリームに実行します。

[`syncer.batch`構成アイテム](/dm/dm-tune-configuration.md#batch)を変更することで、トランザクションに含まれる DML の数を変更できます。

### チェックポイント {#checkpoint}

DML の実行とチェックポイントの更新の操作はアトミックではありません。

DM では、チェックポイントはデフォルトで 30 秒ごとに更新されます。複数の DML ワーカー プロセスがあるため、チェックポイント プロセスは、すべての DML ワーカーの最も早いレプリケーション進行状況のbinlog位置を計算し、この位置を現在のレプリケーション チェックポイントとして使用します。この位置より前のすべてのバイナリログは、ダウンストリームに対して正常に実行されることが保証されます。

<!-- For details on checkpoint mechanism, refer to Checkpoint /dm/dm-checkpoint.md -->

## ノート {#notes}

### トランザクションの一貫性 {#transaction-consistency}

DM は行レベルでデータを複製しますが、トランザクションの一貫性は保証されません。 DM では、アップストリーム トランザクションは複数の行に分割され、同時実行のために異なる DML ワーカーに分散されます。したがって、DM レプリケーション タスクがエラーを報告して一時停止した場合、またはユーザーがタスクを手動で一時停止した場合、ダウンストリームは中間状態になる可能性があります。つまり、アップストリーム トランザクションの DML ステートメントが部分的にダウンストリームにレプリケートされる可能性があり、これによりダウンストリームが不整合な状態になる可能性があります。

タスクが一時停止されているときにダウンストリームが可能な限り一貫した状態になるようにするため、DM v5.3.0 以降、DM はタスクを一時停止する前に 10 秒待機して、アップストリームからのすべてのトランザクションがダウンストリームにレプリケートされるようにします。ただし、トランザクションが 10 秒以内にダウンストリームにレプリケートされない場合、ダウンストリームは依然として不整合な状態にある可能性があります。

### セーフモード {#safe-mode}

DML の実行とチェックポイント更新の操作はアトミックではなく、チェックポイントの更新とダウンストリームへのデータの書き込みもアトミックではありません。 DM が異常終了した場合、チェックポイントは終了時間前の回復ポイントのみを記録する可能性があります。したがって、タスクが再開されると、DM は同じデータを複数回書き込む可能性があります。これは、DM が実際に「少なくとも 1 回の処理」ロジックを提供し、同じデータが複数回処理される可能性があることを意味します。

データが再入可能であることを確認するために、DM は異常終了から再起動するときにセーフ モードに入ります。<!--For the specific logic, refer to [DM Safe Mode](/dm/dm-safe-mode.md).-->

セーフ モードが有効になっている場合、データを複数回処理できるようにするために、DM は次の変換を実行します。

-   上流の`INSERT`ステートメントを`REPLACE`ステートメントに書き換えます。
-   上流の`UPDATE`ステートメントを`DELETE` + `REPLACE`ステートメントに書き換えます。

### 1 回限りの処理 {#exactly-once-processing}

現在、DM は結果整合性のみを保証し、「1 回限りの処理」や「トランザクションの元の順序の維持」はサポートしていません。
