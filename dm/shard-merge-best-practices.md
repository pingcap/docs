---
title: Best Practices of Data Migration in the Shard Merge Scenario
summary: シャードマージのシナリオにおけるデータ移行のベスト プラクティスを学習します。
---

# シャードマージシナリオにおけるデータ移行のベストプラクティス {#best-practices-of-data-migration-in-the-shard-merge-scenario}

このドキュメントでは、シャード マージ シナリオにおける[TiDB データ移行 (DM)](/dm/dm-overview.md)の機能と制限について説明し、アプリケーションのデータ移行のベスト プラクティス ガイドを提供します (デフォルトの「悲観的」モードが使用されます)。

## 別のデータ移行タスクを使用する {#use-a-separate-data-migration-task}

[シャードテーブルからのデータのマージと移行](/dm/feature-shard-merge-pessimistic.md#principles)ドキュメントでは、「シャーディング グループ」の定義が次のように示されています。シャーディング グループは、同じダウンストリーム テーブルにマージおよび移行する必要があるすべてのアップストリーム テーブルで構成されます。

現在のシャーディング DDL メカニズムには、異なるシャーディングされたテーブルでの DDL 操作によってもたらされるスキーマ変更を調整するための[使用制限](/dm/feature-shard-merge-pessimistic.md#restrictions)あります。予期しない理由によりこれらの制限に違反した場合は、 [DMでシャーディングDDLロックを手動で処理する](/dm/manually-handling-sharding-ddl-locks.md)実行するか、データ移行タスク全体をやり直す必要があります。

例外が発生した場合**にデータ移行への影響を軽減するには、各シャーディング グループを個別のデータ移行タスクとしてマージして移行することをお勧めします。これにより、少数のデータ移行タスクのみを手動で処理し、他のタスクには影響を与えないようにすることができます。**

## シャーディングDDLロックを手動で処理する {#handle-sharding-ddl-locks-manually}

[シャードテーブルからのデータのマージと移行](/dm/feature-shard-merge-pessimistic.md#principles)から、DM のシャーディング DDL ロックは、複数の上流シャーディングされたテーブルから下流への DDL 操作の実行を調整するためのメカニズムであることが簡単にわかります。

したがって、 `DM-master` ～ `shard-ddl-lock`のコマンドでシャーディング DDL ロックが見つかった場合、または`query-status`コマンドで一部の DM ワーカーに`unresolvedGroups`または`blockingDDLs`ロックが見つかった場合は、 `shard-ddl-lock unlock`コマンドでシャーディング DDL ロックを手動で解除しようと急いではいけません。

代わりに、次のことができます。

-   シャーディング DDL ロックの自動解放の失敗が[異常なシナリオを列挙](/dm/manually-handling-sharding-ddl-locks.md#supported-scenarios)の 1 つである場合は、対応する手動ソリューションに従ってシナリオを処理します。
-   サポートされていないシナリオの場合は、データ移行タスク全体をやり直します。まず、ダウンストリーム データベースのデータと移行タスクに関連付けられている`dm_meta`情報を空にし、次に、完全および増分データ レプリケーションを再実行します。

## 複数のシャードテーブル間の主キーまたは一意のインデックス間の競合を処理する {#handle-conflicts-between-primary-keys-or-unique-indexes-across-multiple-sharded-tables}

複数のシャード テーブルのデータにより、主キーまたは一意のインデックス間で競合が発生する可能性があります。これらのシャード テーブルのシャーディング ロジックに基づいて、各主キーまたは一意のインデックスを確認する必要があります。主キーまたは一意のインデックスに関連する 3 つのケースを次に示します。

-   シャード キー: 通常、同じシャード キーは 1 つのシャード テーブルにのみ存在するため、シャード キーでデータの競合は発生しません。
-   自動増分主キー: 各シャードテーブルの自動増分主キーは個別にカウントされるため、範囲が重複する可能性があります。この場合、次のセクション[自動増分主キーの競合を処理する](/dm/shard-merge-best-practices.md#handle-conflicts-of-auto-increment-primary-key)を参照して解決する必要があります。
-   その他の主キーまたは一意のインデックス: ビジネス ロジックに基づいて分析する必要があります。データが競合する場合は、次のセクション[自動増分主キーの競合を処理する](/dm/shard-merge-best-practices.md#handle-conflicts-of-auto-increment-primary-key)を参照して解決することもできます。

## 自動増分主キーの競合を処理する {#handle-conflicts-of-auto-increment-primary-key}

このセクションでは、自動インクリメント主キーの競合を処理するための 2 つの推奨ソリューションを紹介します。

### 列から<code>PRIMARY KEY</code>属性を削除します {#remove-the-code-primary-key-code-attribute-from-the-column}

アップストリーム スキーマが次のとおりであると仮定します。

```sql
CREATE TABLE `tbl_no_pk` (
  `auto_pk_c1` bigint NOT NULL,
  `uk_c2` bigint NOT NULL,
  `content_c3` text,
  PRIMARY KEY (`auto_pk_c1`),
  UNIQUE KEY `uk_c2` (`uk_c2`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

以下の要件を満たしている場合:

-   `auto_pk_c1`列目はアプリケーションに影響を与えず、列目の`PRIMARY KEY`属性に依存しません。
-   `uk_c2`列には`UNIQUE KEY`属性があり、すべての上流のシャード テーブル内でグローバルに一意です。

次に、次の手順を実行して、シャードされたテーブルをマージするときに`auto_pk_c1`の列によって発生する可能性のある`ERROR 1062 (23000): Duplicate entry '***' for key 'PRIMARY'`エラーを修正できます。

1.  完全なデータ移行の前に、ダウンストリーム データベースにデータをマージおよび移行するためのテーブルを作成し、 `auto_pk_c1`列目の`PRIMARY KEY`属性を通常のインデックスに変更します。

    ```sql
    CREATE TABLE `tbl_no_pk_2` (
      `auto_pk_c1` bigint NOT NULL,
      `uk_c2` bigint NOT NULL,
      `content_c3` text,
      INDEX (`auto_pk_c1`),
      UNIQUE KEY `uk_c2` (`uk_c2`)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1
    ```

2.  自動インクリメント主キーの競合のチェックをスキップするには、 `task.yaml`に次の構成を追加します。

    ```yaml
    ignore-checking-items: ["auto_increment_ID"]
    ```

3.  完全および増分データ レプリケーション タスクを開始します。

4.  実行`query-status`は、データ移行タスクが正常に処理されたかどうか、および上流のデータがすでにマージされて下流のデータベースに移行されているかどうかを確認します。

### 複合主キーを使用する {#use-a-composite-primary-key}

アップストリーム スキーマが次のとおりであると仮定します。

```sql
CREATE TABLE `tbl_multi_pk` (
  `auto_pk_c1` bigint NOT NULL,
  `uuid_c2` bigint NOT NULL,
  `content_c3` text,
  PRIMARY KEY (`auto_pk_c1`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

以下の要件を満たしている場合:

-   アプリケーションは、 `auto_pk_c1`列目の`PRIMARY KEY`属性に依存しません。
-   `auto_pk_c1`列目と`uuid_c2`列目で構成される複合主キーはグローバルに一意です。
-   アプリケーションでは複合主キーを使用することが可能です。

次に、次の手順を実行して、シャードされたテーブルをマージするときに`auto_pk_c1`の列によって発生する可能性のある`ERROR 1062 (23000): Duplicate entry '***' for key 'PRIMARY'`エラーを修正できます。

1.  完全なデータ移行の前に、ダウンストリーム データベースに、データのマージと移行のためのテーブルを作成します。3 `auto_pk_c1`目に`PRIMARY KEY`属性を指定せず、 `auto_pk_c1`列目と`uuid_c2`列目を使用して複合主キーを構成します。

    ```sql
    CREATE TABLE `tbl_multi_pk_c2` (
      `auto_pk_c1` bigint NOT NULL,
      `uuid_c2` bigint NOT NULL,
      `content_c3` text,
      PRIMARY KEY (`auto_pk_c1`,`uuid_c2`)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1
    ```

2.  完全および増分データ移行タスクを開始します。

3.  実行`query-status`は、データ移行タスクが正常に処理されたかどうか、および上流のデータがすでにマージされて下流のデータベースに移行されているかどうかを確認します。

## アップストリーム RDS にシャードテーブルが含まれている場合の特別な処理 {#special-processing-when-the-upstream-rds-contains-sharded-tables}

アップストリーム データ ソースが RDS であり、シャード テーブルが含まれている場合、SQL クライアントに接続するときに MySQL binlog内のテーブル名が表示されないことがあります。たとえば、アップストリームが UCloud 分散データベースの場合、 binlog内のテーブル名に追加のプレフィックス`_0001`が付くことがあります。したがって、SQL クライアント内のテーブル名ではなく、 binlog内のテーブル名に基づいて[テーブルルーティング](/dm/dm-table-routing.md)構成する必要があります。

## アップストリームでテーブルを作成/削除する {#create-drop-tables-in-the-upstream}

[シャードテーブルからのデータのマージと移行](/dm/feature-shard-merge-pessimistic.md#principles)では、シャーディング DDL ロックの調整は、下流データベースがすべての上流シャード テーブルの DDL ステートメントを受信するかどうかに依存することは明らかです。また、DM は現在、上流でのシャード テーブルの動的な作成または削除**をサポートしていません**。したがって、上流でシャード テーブルを作成または削除するには、次の手順を実行することをお勧めします。

### アップストリームにシャードテーブルを作成する {#create-sharded-tables-in-the-upstream}

アップストリームに新しいシャード テーブルを作成する必要がある場合は、次の手順を実行します。

1.  アップストリームのシャード テーブルで実行されたすべてのシャーディング DDL の調整が完了するまで待機します。

2.  データ移行タスクを停止するには、 `stop-task`実行します。

3.  アップストリームに新しいシャード テーブルを作成します。

4.  `task.yaml`ファイルの構成で、新しく追加されたシャード テーブルを他の既存のシャード テーブルと 1 つのダウンストリーム テーブルにマージできることを確認します。

5.  タスクを開始するには`start-task`実行します。

6.  実行`query-status`は、データ移行タスクが正常に処理されたかどうか、および上流のデータがすでにマージされて下流のデータベースに移行されているかどうかを確認します。

### アップストリームのシャードテーブルを削除する {#drop-sharded-tables-in-the-upstream}

アップストリームでシャードされたテーブルを削除する必要がある場合は、次の手順を実行します。

1.  シャード化されたテーブルを削除し、 [`SHOW BINLOG EVENTS`](https://dev.mysql.com/doc/refman/8.0/en/show-binlog-events.html)実行して、 binlogイベント内の`DROP TABLE`のステートメントに対応する`End_log_pos`取得し、それを*Pos-M*としてマークします。

2.  `query-status`実行して、DMによって処理されたbinlogイベントに対応する位置（ `syncerBinlog` ）を取得し、それを*Pos-S*としてマークします。

3.  *Pos-S*が*Pos-M*より大きい場合、DM が`DROP TABLE`のステートメントをすべて処理し、ドロップ前のテーブルのデータがダウンストリームに移行されているため、後続の操作を実行できることを意味します。それ以外の場合は、DM がデータの移行を完了するまで待機します。

4.  タスクを停止するには`stop-task`実行します。

5.  `task.yaml`ファイル内の構成で、アップストリーム内の削除されたシャード テーブルが無視されることを確認します。

6.  タスクを開始するには`start-task`実行します。

7.  `query-status`実行して、データ移行タスクが正常に処理されたかどうかを確認します。

## 速度制限と交通流制御 {#speed-limits-and-traffic-flow-control}

複数の上流 MySQL または MariaDB インスタンスからのデータが下流の同じ TiDB クラスターにマージされて移行されると、各上流インスタンスに対応するすべての DM ワーカーが、フルデータレプリケーションと増分データレプリケーションを同時に実行します。つまり、DM ワーカーの数が増えるにつれて、デフォルトの同時実行度 (フルデータ移行では`pool-size` 、増分データレプリケーションでは`worker-count` ) が蓄積され、下流データベースに過負荷がかかる可能性があります。この場合、TiDB と DM の監視メトリックに基づいて予備的なパフォーマンス分析を実施し、各同時実行パラメータの値を調整する必要があります。将来的には、DM は部分的に自動化されたトラフィックフロー制御をサポートする予定です。
