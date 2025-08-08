---
title: DML Replication Mechanism in Data Migration
summary: DM のコア処理ユニット Sync が DML ステートメントを複製する方法について説明します。
---

# データ移行におけるDMLレプリケーションメカニズム {#dml-replication-mechanism-in-data-migration}

このドキュメントでは、DMの中核処理ユニットSyncが、データソースまたはリレーログから読み取ったDML文をどのように処理するかについて説明します。DMにおけるDMLイベントの完全な処理フロー、具体的には、binlogの読み取り、フィルタリング、ルーティング、変換、最適化、実行のロジックについて説明します。また、DMLの最適化ロジックとDML実行ロジックについても詳しく説明します。

## DML処理フロー {#dml-processing-flow}

同期ユニットは、DML ステートメントを次のように処理します。

1.  MySQL、MariaDB、またはリレー ログからbinlogイベントを読み取ります。

2.  データ ソースから読み取ったbinlogイベントを変換します。

    1.  [Binlogフィルター](/dm/dm-binlog-event-filter.md) : `filters`で設定されたbinlog式に従ってbinlogイベントをフィルタリングします。
    2.  [テーブルルーティング](/dm/dm-table-routing.md) : `routes`で設定された「データベース/テーブル」ルーティング ルールに従って「データベース/テーブル」名を変換します。
    3.  [表現フィルター](/filter-dml-event.md) : `expression-filter`で設定された SQL 式に従ってbinlogイベントをフィルタリングします。

3.  DML 実行プランを最適化します。

    1.  [圧縮機](#compactor) : 同じレコード（同じ主キーを持つ）に対する複数の操作を1つの操作に統合します。この機能は`syncer.compact`で有効になります。
    2.  [因果関係](#causality) : レプリケーションの同時実行性を向上させるために、異なるレコード (異なる主キーを持つ) に対して競合検出を実行します。
    3.  [合併](#merger) : 複数のbinlogイベントを 1 つの DML ステートメントにマージします`syncer.multiple-rows`によって有効になります。

4.  DML をダウンストリームに実行します。

5.  定期的に、binlogの位置または GTID をチェックポイントに保存します。

![DML processing logic](/media/dm/dm-dml-replication-logic.png)

## DML最適化ロジック {#dml-optimization-logic}

同期ユニットは、Compactor、Causality、Merger の 3 つのステップを通じて DML 最適化ロジックを実装します。

### 圧縮機 {#compactor}

DMは上流のbinlogレコードに基づいてレコードの変更をキャプチャし、下流に複製します。上流が短期間に同じレコードに複数の変更（ `INSERT` / `UPDATE` / `DELETE` ）を加えた場合、DMはCompactorを使用して複数の変更を1つの変更に圧縮することで、下流への負荷を軽減し、スループットを向上させます。例：

    INSERT + UPDATE => INSERT
    INSERT + DELETE => DELETE
    UPDATE + UPDATE => UPDATE
    UPDATE + DELETE => DELETE
    DELETE + INSERT => UPDATE

Compactor機能はデフォルトで無効になっています。有効にするには、レプリケーションタスクの`sync`の設定モジュールで`syncer.compact` ～ `true`設定します（以下を参照）。

```yaml
syncers:                            # The configuration parameters of the sync processing unit
  global:                           # Configuration name
    ...                              # Other configurations are omitted
    compact: true
```

### 因果関係 {#causality}

MySQL binlogのシーケンシャルレプリケーションモデルでは、 binlogイベントはbinlogの順序に従って複製される必要があります。このレプリケーションモデルは、高い QPS と低いレプリケーションレイテンシーという要件を満たすことができません。また、 binlogに関連するすべての操作で競合が発生するわけではないため、競合が発生する場合はシーケンシャルレプリケーションは不要です。

DMは、競合検出を通じて順次実行が必要なbinlogを認識し、他のbinlogの同時実行性を最大限に高めながら、これらのbinlogが順次実行されるようにします。これにより、binlogレプリケーションのパフォーマンスが向上します。

Causality は、union-find アルゴリズムに似たアルゴリズムを採用して、各 DML を分類し、相互に関連する DML をグループ化します。

### 合併 {#merger}

MySQLのbinlogプロトコルでは、各binlogは1行のデータの変更操作に対応します。Mergerを使用することで、DMは複数のbinlogを1つのDMLにマージし、下流に実行することでネットワークの干渉を削減できます。例えば、

      INSERT tb(a,b) VALUES(1,1);
    + INSERT tb(a,b) VALUES(2,2);
    = INSERT tb(a,b) VALUES(1,1),(2,2);
      UPDATE tb SET a=1, b=1 WHERE a=1;
    + UPDATE tb SET a=2, b=2 WHERE a=2;
    = INSERT tb(a,b) VALUES(1,1),(2,2) ON DUPLICATE UPDATE a=VALUES(a), b=VALUES(b)
      DELETE tb WHERE a=1
    + DELETE tb WHERE a=2
    = DELETE tb WHERE (a) IN (1),(2);

マージャー機能はデフォルトで無効になっています。有効にするには、レプリケーションタスクの`sync`の設定モジュールで`syncer.multiple-rows` ～ `true`設定します（以下を参照）。

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

DML 生成のロジックは次のとおりです。

1.  Sync ユニットは、アップストリームの初期テーブル構造を記録します。
    -   完全タスクと増分タスクを開始すると、Sync は**アップストリームの完全データ移行中にエクスポートされたテーブル構造を**アップストリームの初期テーブル構造として使用します。
    -   増分タスクを開始する場合、MySQL binlog にはテーブル構造情報が記録されないため、Sync は**下流の対応するテーブルのテーブル構造を**上流の初期テーブル構造として使用します。
2.  ユーザーの上流テーブルと下流テーブルの構造に不整合がある可能性があります。例えば、下流テーブルに上流テーブルよりも多くの列がある場合や、上流テーブルと下流テーブルの主キーが不整合な場合などです。そのため、データ複製の正確性を確保するために、DMは**対応するテーブルの主キーと一意キーの情報を下流テーブルに**記録します。
3.  DM は DML を生成します。
    -   **スキーマ トラッカーに記録されたアップストリーム テーブル構造**を使用して、DML ステートメントの列名を生成します。
    -   **binlogに記録された列の値**を使用して、DML ステートメントの列の値を生成します。
    -   **スキーマトラッカーに記録されたダウンストリーム主キーまたは一意キー**を使用して、DML文の`WHERE`条件を生成します。テーブル構造に一意キーがない場合、DMはbinlogに記録されたすべての列値を`WHERE`条件として使用します。

### 労働者数 {#worker-count}

Causalityは、競合検出機能によりbinlogを複数のグループに分割し、下流へ同時に実行することができます。DMは同時実行数を`worker-count`設定することで制御します。下流TiDBのCPU使用率が高くない場合、同時実行数を増やすことでデータレプリケーションのスループットを効果的に向上させることができます。

[`syncer.worker-count`設定項目](/dm/dm-tune-configuration.md#worker-count)変更することで、DML を同時に移行するスレッドの数を変更できます。

### バッチ {#batch}

DMは複数のDMLを単一のトランザクションにまとめ、下流に実行します。DMLワーカーはDMLを受け取ると、そのDMLをキャッシュに追加します。キャッシュ内のDML数が設定されたしきい値に達した場合、またはDMLワーカーが長時間DMLを受け取っていない場合、DMLワーカーはキャッシュ内のDMLを下流に実行します。

[`syncer.batch`設定項目](/dm/dm-tune-configuration.md#batch)変更することで、トランザクションに含まれる DML の数を変更できます。

### チェックポイント {#checkpoint}

DML を実行してチェックポイントを更新する操作はアトミックではありません。

DMでは、チェックポイントはデフォルトで30秒ごとに更新されます。複数のDMLワーカープロセスが存在するため、チェックポイントプロセスはすべてのDMLワーカーの中で最も早いレプリケーション進行のbinlog位置を計算し、この位置を現在のレプリケーションチェックポイントとして使用します。この位置より前のすべてのバイナリログは、下流に正常に実行されることが保証されます。

<!-- For details on checkpoint mechanism, refer to Checkpoint /dm/dm-checkpoint.md -->

## 注記 {#notes}

### トランザクションの一貫性 {#transaction-consistency}

DMは行レベルでデータを複製するため、トランザクションの一貫性は保証されません。DMでは、上流トランザクションは複数の行に分割され、複数のDMLワーカーに分散されて同時実行されます。そのため、DMレプリケーションタスクがエラーを報告して一時停止した場合、またはユーザーが手動でタスクを一時停止した場合、下流トランザクションは中間状態になる可能性があります。つまり、上流トランザクションのDML文が下流トランザクションに部分的に複製され、その結果、下流トランザクションが不整合な状態になる可能性があります。

タスクが一時停止されている間、ダウンストリームの一貫性を可能な限り確保するため、DM v5.3.0以降では、アップストリームからのすべてのトランザクションがダウンストリームに複製されることを確認するために、タスクを一時停止する前に10秒間待機するようになりました。ただし、10秒以内にトランザクションがダウンストリームに複製されない場合、ダウンストリームは依然として不整合な状態のままになる可能性があります。

### セーフモード {#safe-mode}

DML実行とチェックポイント更新の操作はアトミックではなく、チェックポイント更新と下流へのデータ書き込みの操作もアトミックではありません。DMが異常終了した場合、チェックポイントは終了時刻より前のリカバリポイントのみを記録する可能性があります。そのため、タスクが再開されると、DMは同じデータを複数回書き込む可能性があります。これは、DMが実際には「少なくとも1回の処理」ロジックを提供していることを意味し、同じデータが複数回処理される可能性があります。

データが再入可能であることを確認するために、DM は異常終了から再起動するときにセーフ モードに入ります。<!--For the specific logic, refer to [DM Safe Mode](/dm/dm-safe-mode.md).-->

セーフ モードが有効になっている場合、データが複数回処理されることを確認するために、DM は次の変換を実行します。

-   アップストリームの`INSERT`のステートメントを`REPLACE`ステートメントに書き換えます。
-   アップストリームの`UPDATE`ステートメントを`DELETE` + `REPLACE`ステートメントに書き換えます。

### 正確に1回だけ処理 {#exactly-once-processing}

現在、DM は結果整合性のみを保証しており、「正確に 1 回の処理」や「トランザクションの元の順序の維持」はサポートしていません。
