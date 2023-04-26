---
title: Best Practices of Data Migration in the Shard Merge Scenario
summary: Learn the best practices of data migration in the shard merge scenario.
---

# シャード マージ シナリオでのデータ移行のベスト プラクティス {#best-practices-of-data-migration-in-the-shard-merge-scenario}

このドキュメントでは、シャード マージ シナリオにおける[TiDB データ移行](https://github.com/pingcap/dm) (DM) の機能と制限について説明し、アプリケーションのデータ移行のベスト プラクティス ガイドを提供します (デフォルトの &quot;悲観的&quot; モードが使用されます)。

## 別のデータ移行タスクを使用する {#use-a-separate-data-migration-task}

[シャード テーブルからのデータのマージと移行](/dm/feature-shard-merge-pessimistic.md#principles)のドキュメントでは、「シャーディング グループ」の定義が示されています。シャーディング グループは、マージして同じダウンストリーム テーブルに移行する必要があるすべてのアップストリーム テーブルで構成されます。

現在のシャーディング DDL メカニズムには、さまざまなシャード テーブルでの DDL 操作によってもたらされるスキーマの変更を調整するための機能が[利用制限](/dm/feature-shard-merge-pessimistic.md#restrictions)かあります。予期しない理由でこれらの制限に違反した場合は、データ移行タスク全体を[DM でシャーディング DDL ロックを手動で処理する](/dm/manually-handling-sharding-ddl-locks.md)実行するか、やり直す必要があります。

例外が発生した場合のデータ移行への影響を軽減するには、各シャーディング グループを個別のデータ移行タスクとしてマージおよび移行することをお勧めします。**これにより、少数のデータ移行タスクのみを手動で処理する必要があり、他のタスクは影響を受けないままにすることができます。**

## シャーディング DDL ロックを手動で処理する {#handle-sharding-ddl-locks-manually}

DM のシャーディング DDL ロックは、アップストリームの複数のシャード テーブルからダウンストリームへの DDL 操作の実行を調整するためのメカニズムであることは、 [シャード テーブルからのデータのマージと移行](/dm/feature-shard-merge-pessimistic.md#principles)から簡単に結論付けることができます。

したがって、コマンド`DM-master` ～ `shard-ddl-lock`でシャーディング DDL ロックが検出された場合、または一部の DM-worker でコマンド`query-status`から`unresolvedGroups`または`blockingDDLs`検出された場合は、急いで`shard-ddl-lock unlock`コマンドを使用してシャーディング DDL ロックを手動で解放しないでください。

代わりに、次のことができます。

-   シャーディング DDL ロックの自動解放の失敗が[列挙された異常なシナリオ](/dm/manually-handling-sharding-ddl-locks.md#supported-scenarios)つである場合は、対応する手動の解決策に従ってシナリオを処理します。
-   サポートされていないシナリオの場合は、データ移行タスク全体をやり直します。まず、ダウンストリーム データベースのデータと、移行タスクに関連付けられた`dm_meta`情報を空にします。次に、完全および増分データ複製を再実行します。

## 複数のシャード テーブル間で主キーまたは一意のインデックス間の競合を処理する {#handle-conflicts-between-primary-keys-or-unique-indexes-across-multiple-sharded-tables}

複数のシャード テーブルからのデータは、主キーまたは一意のインデックス間で競合を引き起こす可能性があります。これらのシャード テーブルのシャーディング ロジックに基づいて、各主キーまたは一意のインデックスを確認する必要があります。主キーまたは一意のインデックスに関連する 3 つのケースを次に示します。

-   シャード キー: 通常、同じシャード キーは 1 つのシャード テーブルにのみ存在します。つまり、シャード キーでデータの競合は発生しません。
-   自動インクリメント主キー: 各シャード テーブルの自動インクリメント主キーは個別にカウントされるため、それらの範囲が重複する可能性があります。この場合、次のセクション[自動インクリメント主キーの競合を処理する](/dm/shard-merge-best-practices.md#handle-conflicts-of-auto-increment-primary-key)を参照して解決する必要があります。
-   その他の主キーまたは一意のインデックス: ビジネス ロジックに基づいて分析する必要があります。データが競合する場合は、次のセクション[自動インクリメント主キーの競合を処理する](/dm/shard-merge-best-practices.md#handle-conflicts-of-auto-increment-primary-key)を参照して解決することもできます。

## 自動インクリメント主キーの競合を処理する {#handle-conflicts-of-auto-increment-primary-key}

このセクションでは、自動インクリメント主キーの競合を処理するための 2 つの推奨ソリューションを紹介します。

### 列から<code>PRIMARY KEY</code>属性を削除します {#remove-the-code-primary-key-code-attribute-from-the-column}

上流のスキーマが次のとおりであるとします。

```sql
CREATE TABLE `tbl_no_pk` (
  `auto_pk_c1` bigint(20) NOT NULL,
  `uk_c2` bigint(20) NOT NULL,
  `content_c3` text,
  PRIMARY KEY (`auto_pk_c1`),
  UNIQUE KEY `uk_c2` (`uk_c2`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

次の要件が満たされている場合:

-   `auto_pk_c1`列はアプリケーションに影響を与えず、列の`PRIMARY KEY`属性に依存しません。
-   `uk_c2`列には`UNIQUE KEY`属性があり、上流のすべてのシャード テーブルでグローバルに一意です。

次に、次の手順を実行して、シャード テーブルをマージするときに`auto_pk_c1`列が原因である可能性がある`ERROR 1062 (23000): Duplicate entry '***' for key 'PRIMARY'`エラーを修正できます。

1.  完全なデータ移行の前に、ダウンストリーム データベースにデータのマージと移行用のテーブルを作成し、 `auto_pk_c1`列の`PRIMARY KEY`属性を通常のインデックスに変更します。

    ```sql
    CREATE TABLE `tbl_no_pk_2` (
      `auto_pk_c1` bigint(20) NOT NULL,
      `uk_c2` bigint(20) NOT NULL,
      `content_c3` text,
      INDEX (`auto_pk_c1`),
      UNIQUE KEY `uk_c2` (`uk_c2`)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1
    ```

2.  次の構成を`task.yaml`に追加して、自動インクリメント主キーの競合のチェックをスキップします。

    ```yaml
    ignore-checking-items: ["auto_increment_ID"]
    ```

3.  完全および増分データ複製タスクを開始します。

4.  `query-status`を実行して、データ移行タスクが正常に処理されたかどうか、および上流のデータが既にマージされて下流のデータベースに移行されているかどうかを確認します。

### 複合主キーを使用する {#use-a-composite-primary-key}

上流のスキーマが次のとおりであるとします。

```sql
CREATE TABLE `tbl_multi_pk` (
  `auto_pk_c1` bigint(20) NOT NULL,
  `uuid_c2` bigint(20) NOT NULL,
  `content_c3` text,
  PRIMARY KEY (`auto_pk_c1`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

次の要件が満たされている場合:

-   アプリケーションは、 `auto_pk_c1`列の`PRIMARY KEY`属性に依存しません。
-   `auto_pk_c1`と`uuid_c2`列で構成される複合主キーは、グローバルに一意です。
-   アプリケーションで複合主キーを使用することは許容されます。

次に、次の手順を実行して、シャード テーブルをマージするときに`auto_pk_c1`列が原因である可能性がある`ERROR 1062 (23000): Duplicate entry '***' for key 'PRIMARY'`エラーを修正できます。

1.  完全なデータ移行の前に、データのマージと移行のためにダウンストリーム データベースにテーブルを作成します。 `auto_pk_c1`列には`PRIMARY KEY`属性を指定せず、 `auto_pk_c1`と`uuid_c2`列を使用して複合主キーを構成します。

    ```sql
    CREATE TABLE `tbl_multi_pk_c2` (
      `auto_pk_c1` bigint(20) NOT NULL,
      `uuid_c2` bigint(20) NOT NULL,
      `content_c3` text,
      PRIMARY KEY (`auto_pk_c1`,`uuid_c2`)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1
    ```

2.  完全および増分データ移行タスクを開始します。

3.  `query-status`を実行して、データ移行タスクが正常に処理されたかどうか、およびアップストリームからのデータが既にマージされてダウンストリーム データベースに移行されているかどうかを確認します。

## アップストリーム RDS にシャード テーブルが含まれている場合の特別な処理 {#special-processing-when-the-upstream-rds-contains-sharded-tables}

アップストリーム データ ソースが RDS であり、シャード テーブルが含まれている場合、SQL クライアントに接続するときに、MySQL binlogのテーブル名が表示されないことがあります。たとえば、アップストリームが UCloud 分散データベースである場合、 binlogのテーブル名には追加のプレフィックス`_0001`が含まれる場合があります。したがって、SQL クライアントのテーブル名ではなく、 binlogのテーブル名に基づいて[テーブル ルーティング](/dm/dm-table-routing.md)を構成する必要があります。

## アップストリームでのテーブルの作成/削除 {#create-drop-tables-in-the-upstream}

[シャード テーブルからのデータのマージと移行](/dm/feature-shard-merge-pessimistic.md#principles)では、シャーディング DDL ロックの調整が、ダウンストリーム データベースがすべてのアップストリーム シャード テーブルの DDL ステートメントを受信するかどうかに依存することは明らかです。さらに、DM は現在、アップストリームでシャード テーブルを動的に作成または削除すること**をサポートしていません**。したがって、アップストリームでシャード テーブルを作成または削除するには、次の手順を実行することをお勧めします。

### アップストリームでシャード テーブルを作成する {#create-sharded-tables-in-the-upstream}

アップストリームで新しいシャード テーブルを作成する必要がある場合は、次の手順を実行します。

1.  アップストリームのシャード テーブルで実行されたすべてのシャーディング DDL の調整が完了するまで待ちます。

2.  `stop-task`を実行して、データ移行タスクを停止します。

3.  アップストリームに新しいシャード テーブルを作成します。

4.  `task.yaml`ファイルの構成により、新しく追加されたシャード テーブルを 1 つのダウンストリーム テーブルで他の既存のシャード テーブルとマージできることを確認します。

5.  `start-task`を実行してタスクを開始します。

6.  `query-status`を実行して、データ移行タスクが正常に処理されたかどうか、およびアップストリームからのデータが既にマージされてダウンストリーム データベースに移行されているかどうかを確認します。

### アップストリームに分割されたテーブルをドロップする {#drop-sharded-tables-in-the-upstream}

アップストリームでシャード テーブルを削除する必要がある場合は、次の手順を実行します。

1.  分割されたテーブルを削除し、 [`SHOW BINLOG EVENTS`](https://dev.mysql.com/doc/refman/5.7/en/show-binlog-events.html)を実行してbinlogイベントの`DROP TABLE`ステートメントに対応する`End_log_pos`をフェッチし、それを*Pos-M*としてマークします。

2.  `query-status`を実行して、DM によって処理されたbinlogイベントに対応する位置 ( `syncerBinlog` ) をフェッチし、それを*Pos-S*としてマークします。

3.  *Pos-S*が<em>Pos-M</em>より大きい場合は、DM が`DROP TABLE`のステートメントをすべて処理したことを意味し、ドロップ前のテーブルのデータはダウンストリームに移行されているため、後続の操作を実行できます。それ以外の場合は、DM がデータの移行を完了するまで待ちます。

4.  `stop-task`を実行してタスクを停止します。

5.  `task.yaml`ファイルの構成が、アップストリームで削除されたシャード テーブルを無視していることを確認してください。

6.  `start-task`を実行してタスクを開始します。

7.  `query-status`を実行して、データ移行タスクが正常に処理されたかどうかを確認します。

## 速度制限と交通流制御 {#speed-limits-and-traffic-flow-control}

複数のアップストリーム MySQL または MariaDB インスタンスからのデータがマージされ、ダウンストリームの同じ TiDB クラスターに移行されると、各アップストリーム インスタンスに対応するすべての DM-worker が完全な増分データ レプリケーションを同時に実行します。これは、DM ワーカーの数が増えるとデフォルトの同時実行度 (完全データ移行では`pool-size` 、増分データ レプリケーションでは`worker-count` ) が累積され、ダウンストリーム データベースが過負荷になる可能性があることを意味します。この場合、TiDB と DM の監視メトリックに基づいて予備的なパフォーマンス分析を行い、各同時実行パラメーターの値を調整する必要があります。将来、DM は部分的に自動化されたトラフィック フロー制御をサポートする予定です。
