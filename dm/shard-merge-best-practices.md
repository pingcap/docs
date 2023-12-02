---
title: Best Practices of Data Migration in the Shard Merge Scenario
summary: Learn the best practices of data migration in the shard merge scenario.
---

# シャード結合シナリオにおけるデータ移行のベスト プラクティス {#best-practices-of-data-migration-in-the-shard-merge-scenario}

このドキュメントでは、シャード マージ シナリオにおける[TiDB データ移行](https://github.com/pingcap/dm) (DM) の機能と制限について説明し、アプリケーションのデータ移行のベスト プラクティス ガイドを提供します (デフォルトの「悲観的」モードが使用されます)。

## 別のデータ移行タスクを使用する {#use-a-separate-data-migration-task}

[シャードテーブルからのデータのマージと移行](/dm/feature-shard-merge-pessimistic.md#principles)ドキュメントでは、「シャーディング グループ」の定義が示されています。シャーディング グループは、同じダウンストリーム テーブルにマージおよび移行する必要があるすべての上流テーブルで構成されます。

現在のシャーディング DDL メカニズムには、さまざまなシャーディング テーブルでの DDL 操作によってもたらされるスキーマの変更を調整するために、いくつかの[使用制限](/dm/feature-shard-merge-pessimistic.md#restrictions)があります。予期せぬ理由でこれらの制限に違反した場合は、 [DM でシャーディング DDL ロックを手動で処理する](/dm/manually-handling-sharding-ddl-locks.md) 、あるいはデータ移行タスク全体をやり直す必要があります。

例外が発生した場合のデータ移行への影響を軽減するには、各シャーディング グループを個別のデータ移行タスクとしてマージおよび移行することをお勧めします。**これにより、少数のデータ移行タスクのみを手動で処理する必要があり、他のタスクは影響を受けないままになる可能性があります。**

## シャーディング DDL ロックを手動で処理する {#handle-sharding-ddl-locks-manually}

[シャードテーブルからのデータのマージと移行](/dm/feature-shard-merge-pessimistic.md#principles)から、DM のシャーディング DDL ロックは、複数の上流のシャーディング テーブルから下流への DDL 操作の実行を調整するためのメカニズムであると簡単に結論付けることができます。

したがって、 `DM-master` ～ `shard-ddl-lock`コマンドでシャーディング DDL ロックが見つかった場合、または一部の DM ワーカーで`query-status`コマンドで`unresolvedGroups`または`blockingDDLs`が見つかった場合は、急いで`shard-ddl-lock unlock`コマンドでシャーディング DDL ロックを手動で解放しないでください。

代わりに、次のことができます。

-   シャーディング DDL ロックの自動解放の失敗が[リストされた異常なシナリオ](/dm/manually-handling-sharding-ddl-locks.md#supported-scenarios)のいずれかである場合は、対応する手動の解決策に従ってシナリオを処理します。
-   サポートされていないシナリオの場合は、データ移行タスク全体をやり直します。まず、ダウンストリーム データベース内のデータと移行タスクに関連付けられ`dm_meta`情報を空にします。その後、完全および増分データ レプリケーションを再実行します。

## 複数のシャードテーブルにわたる主キーまたは一意のインデックス間の競合を処理する {#handle-conflicts-between-primary-keys-or-unique-indexes-across-multiple-sharded-tables}

複数のシャードテーブルからのデータにより、主キーまたは一意のインデックス間で競合が発生する可能性があります。これらのシャードテーブルのシャーディングロジックに基づいて、各主キーまたは一意のインデックスをチェックする必要があります。主キーまたは一意のインデックスに関連する 3 つのケースを次に示します。

-   シャード キー: 通常、同じシャード キーは 1 つのシャード テーブルにのみ存在します。これは、シャード キーでデータの競合が発生しないことを意味します。
-   自動インクリメント主キー: 各シャードテーブルの自動インクリメント主キーは個別にカウントされるため、範囲が重複する可能性があります。この場合は、次のセクション[自動インクリメント主キーの競合を処理する](/dm/shard-merge-best-practices.md#handle-conflicts-of-auto-increment-primary-key)を参照して解決する必要があります。
-   その他の主キーまたは一意のインデックス: ビジネス ロジックに基づいて分析する必要があります。データが競合する場合は、次のセクション[自動インクリメント主キーの競合を処理する](/dm/shard-merge-best-practices.md#handle-conflicts-of-auto-increment-primary-key)を参照して解決することもできます。

## 自動インクリメント主キーの競合を処理する {#handle-conflicts-of-auto-increment-primary-key}

このセクションでは、自動インクリメント主キーの競合に対処するための 2 つの推奨ソリューションを紹介します。

### 列から<code>PRIMARY KEY</code>属性を削除します。 {#remove-the-code-primary-key-code-attribute-from-the-column}

上流のスキーマが次のとおりであると仮定します。

```sql
CREATE TABLE `tbl_no_pk` (
  `auto_pk_c1` bigint(20) NOT NULL,
  `uk_c2` bigint(20) NOT NULL,
  `content_c3` text,
  PRIMARY KEY (`auto_pk_c1`),
  UNIQUE KEY `uk_c2` (`uk_c2`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

以下の要件が満たされている場合:

-   `auto_pk_c1`列はアプリケーションに影響を与えず、列の`PRIMARY KEY`属性には依存しません。
-   `uk_c2`列には`UNIQUE KEY`属性があり、上流のすべてのシャードテーブルでグローバルに一意です。

次に、次の手順を実行して、シャードテーブルをマージするときに`auto_pk_c1`列によって発生する可能性がある`ERROR 1062 (23000): Duplicate entry '***' for key 'PRIMARY'`エラーを修正できます。

1.  完全なデータ移行の前に、データをマージおよび移行するためのテーブルをダウンストリーム データベースに作成し、 `auto_pk_c1`列の`PRIMARY KEY`属性を通常のインデックスに変更します。

    ```sql
    CREATE TABLE `tbl_no_pk_2` (
      `auto_pk_c1` bigint(20) NOT NULL,
      `uk_c2` bigint(20) NOT NULL,
      `content_c3` text,
      INDEX (`auto_pk_c1`),
      UNIQUE KEY `uk_c2` (`uk_c2`)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1
    ```

2.  自動インクリメント主キーの競合チェックをスキップするには、 `task.yaml`に次の構成を追加します。

    ```yaml
    ignore-checking-items: ["auto_increment_ID"]
    ```

3.  完全および増分データ レプリケーション タスクを開始します。

4.  `query-status`を実行して、データ移行タスクが正常に処理されたかどうか、およびアップストリームからのデータがすでにマージされ、ダウンストリーム データベースに移行されているかどうかを確認します。

### 複合主キーを使用する {#use-a-composite-primary-key}

上流のスキーマが次のとおりであると仮定します。

```sql
CREATE TABLE `tbl_multi_pk` (
  `auto_pk_c1` bigint(20) NOT NULL,
  `uuid_c2` bigint(20) NOT NULL,
  `content_c3` text,
  PRIMARY KEY (`auto_pk_c1`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

以下の要件が満たされている場合:

-   アプリケーションは`auto_pk_c1`列の`PRIMARY KEY`属性に依存しません。
-   `auto_pk_c1`と`uuid_c2`列で構成される複合主キーはグローバルに一意です。
-   アプリケーションでは複合主キーを使用できます。

次に、次の手順を実行して、シャードテーブルをマージするときに`auto_pk_c1`列によって発生する可能性がある`ERROR 1062 (23000): Duplicate entry '***' for key 'PRIMARY'`エラーを修正できます。

1.  完全なデータ移行の前に、データをマージおよび移行するためのテーブルをダウンストリーム データベースに作成します。 `auto_pk_c1`列には`PRIMARY KEY`属性を指定せず、 `auto_pk_c1`と`uuid_c2`列を使用して複合主キーを作成します。

    ```sql
    CREATE TABLE `tbl_multi_pk_c2` (
      `auto_pk_c1` bigint(20) NOT NULL,
      `uuid_c2` bigint(20) NOT NULL,
      `content_c3` text,
      PRIMARY KEY (`auto_pk_c1`,`uuid_c2`)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1
    ```

2.  完全および増分データ移行タスクを開始します。

3.  `query-status`を実行して、データ移行タスクが正常に処理されたかどうか、およびアップストリームからのデータがすでにマージされ、ダウンストリーム データベースに移行されているかどうかを確認します。

## 上流の RDS にシャードテーブルが含まれる場合の特別な処理 {#special-processing-when-the-upstream-rds-contains-sharded-tables}

アップストリーム データ ソースが RDS であり、それにシャード テーブルが含まれている場合、SQL クライアントに接続するときに MySQLbinlog内のテーブル名が表示されない可能性があります。たとえば、アップストリームが UCloud 分散データベースである場合、binlog内のテーブル名には追加のプレフィックス`_0001`が付く可能性があります。したがって、SQL クライアントのテーブル名ではなく、 binlogのテーブル名に基づいて[テーブルルーティング](/dm/dm-table-routing.md)を構成する必要があります。

## 上流でのテーブルの作成/削除 {#create-drop-tables-in-the-upstream}

[シャードテーブルからのデータのマージと移行](/dm/feature-shard-merge-pessimistic.md#principles)では、シャーディング DDL ロックの調整は、ダウンストリーム データベースがアップストリームのすべてのシャーディング テーブルの DDL ステートメントを受信するかどうかに依存することは明らかです。さらに、DM は現在、アップストリームでのシャード テーブルの動的作成または削除**をサポートしていません**。したがって、アップストリームでシャードテーブルを作成または削除するには、次の手順を実行することをお勧めします。

### アップストリームでシャードテーブルを作成する {#create-sharded-tables-in-the-upstream}

アップストリームに新しいシャードテーブルを作成する必要がある場合は、次の手順を実行します。

1.  上流のシャードテーブルで実行されたすべてのシャーディング DDL の調整が完了するまで待ちます。

2.  `stop-task`を実行してデータ移行タスクを停止します。

3.  上流に新しいシャードテーブルを作成します。

4.  `task.yaml`ファイルの構成により、新しく追加されたシャード テーブルを 1 つのダウンストリーム テーブルに他の既存のシャード テーブルとマージできることを確認してください。

5.  `start-task`を実行してタスクを開始します。

6.  `query-status`を実行して、データ移行タスクが正常に処理されたかどうか、およびアップストリームからのデータがすでにマージされ、ダウンストリーム データベースに移行されているかどうかを確認します。

### 上流でシャード化されたテーブルを削除する {#drop-sharded-tables-in-the-upstream}

アップストリームでシャードテーブルを削除する必要がある場合は、次の手順を実行します。

1.  シャードテーブルを削除し、 [`SHOW BINLOG EVENTS`](https://dev.mysql.com/doc/refman/8.0/en/show-binlog-events.html)を実行してbinlogイベントの`DROP TABLE`ステートメントに対応する`End_log_pos`をフェッチし、それを*Pos-M*としてマークします。

2.  `query-status`を実行して、DM によって処理されたbinlogイベントに対応する位置 ( `syncerBinlog` ) を取得し、それを*Pos-S*としてマークします。

3.  *Pos-S*が*Pos-M*より大きい場合、DM が`DROP TABLE`のステートメントをすべて処理し、削除前のテーブルのデータが下流に移行されているため、以降の操作を実行できることを意味します。それ以外の場合は、DM によるデータの移行が完了するまで待ちます。

4.  タスクを停止するには`stop-task`を実行します。

5.  `task.yaml`ファイルの構成がアップストリームでドロップされたシャードテーブルを無視していることを確認してください。

6.  `start-task`を実行してタスクを開始します。

7.  `query-status`を実行して、データ移行タスクが正常に処理されたかどうかを確認します。

## 速度制限と交通流制御 {#speed-limits-and-traffic-flow-control}

複数のアップストリーム MySQL または MariaDB インスタンスからのデータがマージされ、ダウンストリームの同じ TiDB クラスターに移行される場合、各アップストリーム インスタンスに対応するすべての DM ワーカーは、完全データ レプリケーションと増分データ レプリケーションを同時に実行します。これは、DM ワーカーの数が増加するにつれてデフォルトの同時実行度 (完全なデータ移行では`pool-size` 、増分データ レプリケーションでは`worker-count` ) が累積し、ダウンストリーム データベースに過負荷がかかる可能性があることを意味します。この場合、TiDB および DM 監視メトリックに基づいて予備的なパフォーマンス分析を実行し、各同時実行パラメーターの値を調整する必要があります。将来的には、DM は部分的に自動化されたトラフィック フロー制御をサポートすると予想されます。
