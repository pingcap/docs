---
title: Best Practices of Data Migration in the Shard Merge Scenario
summary: Learn the best practices of data migration in the shard merge scenario.
---

# シャードマージシナリオでのデータ移行のベストプラクティス {#best-practices-of-data-migration-in-the-shard-merge-scenario}

このドキュメントでは、シャードマージシナリオにおける[TiDBデータ移行](https://github.com/pingcap/dm) （DM）の機能と制限について説明し、アプリケーションのデータ移行のベストプラクティスガイドを提供します（デフォルトの「悲観的」モードが使用されます）。

## 別のデータ移行タスクを使用する {#use-a-separate-data-migration-task}

[シャーディングされたテーブルからのデータのマージと移行](/dm/feature-shard-merge-pessimistic.md#principles)のドキュメントでは、「シャーディンググループ」の定義が示されています。シャーディンググループは、同じダウンストリームテーブルにマージおよび移行する必要があるすべてのアップストリームテーブルで構成されます。

現在のシャーディングDDLメカニズムには、さまざまなシャードテーブルでのDDL操作によってもたらされるスキーマの変更を調整するための[使用制限](/dm/feature-shard-merge-pessimistic.md#restrictions)があります。予期しない理由でこれらの制限に違反した場合は、データ移行タスク全体を[DMでシャーディングDDLロックを手動で処理する](/dm/manually-handling-sharding-ddl-locks.md) 、またはやり直す必要があります。

例外が発生した場合のデータ移行への影響を軽減するために、各シャーディンググループを個別のデータ移行タスクとしてマージおよび移行することをお勧めします。**これにより、少数のデータ移行タスクのみを手動で処理する必要があり、他のタスクは影響を受けないままになる可能性があります。**

## シャーディングDDLロックを手動で処理する {#handle-sharding-ddl-locks-manually}

DMのシャーディングDDLロックは、複数のアップストリームシャードテーブルからダウンストリームへのDDL操作の実行を調整するためのメカニズムであると[シャーディングされたテーブルからのデータのマージと移行](/dm/feature-shard-merge-pessimistic.md#principles)から簡単に結論付けることができます。

したがって、 `DM-master`コマンドでシャーディングDDLロックを見つけた場合、または`shard-ddl-lock`コマンドで一部のDMワーカーで`unresolvedGroups`または`blockingDDLs`を見つけた場合は、 `query-status`コマンドでシャーディング`shard-ddl-lock unlock`ロックを手動で解放しないでください。

代わりに、次のことができます。

-   シャーディングDDLロックの自動解放の失敗が[リストされた異常なシナリオ](/dm/manually-handling-sharding-ddl-locks.md#supported-scenarios)のいずれかである場合は、対応する手動ソリューションに従ってシナリオを処理します。
-   サポートされていないシナリオの場合は、データ移行タスク全体をやり直します。まず、ダウンストリームデータベースのデータと、移行タスクに関連付けられている`dm_meta`の情報を空にします。次に、完全な増分データレプリケーションを再実行します。

## 複数のシャードテーブル間での主キーまたは一意のインデックス間の競合を処理します {#handle-conflicts-between-primary-keys-or-unique-indexes-across-multiple-sharded-tables}

複数のシャードテーブルからのデータにより、主キーまたは一意のインデックス間で競合が発生する可能性があります。これらのシャーディングされたテーブルのシャーディングロジックに基づいて、各主キーまたは一意のインデックスを確認する必要があります。主キーまたは一意のインデックスに関連する3つのケースは次のとおりです。

-   シャードキー：通常、同じシャードキーは1つのシャードテーブルにのみ存在します。つまり、シャードキーでデータの競合は発生しません。
-   自動インクリメント主キー：各シャーディングされたテーブルの自動インクリメント主キーは別々にカウントされるため、それらの範囲が重複する可能性があります。この場合、次のセクション[自動インクリメント主キーの競合を処理します](/dm/shard-merge-best-practices.md#handle-conflicts-of-auto-increment-primary-key)を参照して解決する必要があります。
-   その他の主キーまたは一意のインデックス：ビジネスロジックに基づいてそれらを分析する必要があります。データが競合する場合は、次のセクション[自動インクリメント主キーの競合を処理します](/dm/shard-merge-best-practices.md#handle-conflicts-of-auto-increment-primary-key)を参照して解決することもできます。

## 自動インクリメント主キーの競合を処理します {#handle-conflicts-of-auto-increment-primary-key}

このセクションでは、自動インクリメントの主キーの競合を処理するための2つの推奨されるソリューションを紹介します。

### 列から<code>PRIMARY KEY</code>属性を削除します {#remove-the-code-primary-key-code-attribute-from-the-column}

アップストリームスキーマが次のとおりであると想定します。

```sql
CREATE TABLE `tbl_no_pk` (
  `auto_pk_c1` bigint(20) NOT NULL,
  `uk_c2` bigint(20) NOT NULL,
  `content_c3` text,
  PRIMARY KEY (`auto_pk_c1`),
  UNIQUE KEY `uk_c2` (`uk_c2`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

次の要件が満たされている場合：

-   `auto_pk_c1`列はアプリケーションに影響を与えず、列の`PRIMARY KEY`属性に依存しません。
-   `uk_c2`列には`UNIQUE KEY`属性があり、すべてのアップストリームシャードテーブルでグローバルに一意です。

次に、次の手順を実行して、シャーディングされたテーブルをマージするときに`auto_pk_c1`列が原因である可能性がある`ERROR 1062 (23000): Duplicate entry '***' for key 'PRIMARY'`エラーを修正できます。

1.  完全なデータ移行の前に、データをマージおよび移行するためのテーブルをダウンストリームデータベースに作成し、 `auto_pk_c1`列の`PRIMARY KEY`属性を通常のインデックスに変更します。

    ```sql
    CREATE TABLE `tbl_no_pk_2` (
      `auto_pk_c1` bigint(20) NOT NULL,
      `uk_c2` bigint(20) NOT NULL,
      `content_c3` text,
      INDEX (`auto_pk_c1`),
      UNIQUE KEY `uk_c2` (`uk_c2`)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1
    ```

2.  次の構成を`task.yaml`に追加して、自動インクリメントの主キーの競合のチェックをスキップします。

    ```yaml
    ignore-checking-items: ["auto_increment_ID"]
    ```

3.  フルおよびインクリメンタルデータレプリケーションタスクを開始します。

4.  `query-status`を実行して、データ移行タスクが正常に処理されたかどうか、およびアップストリームからのデータが既にマージされてダウンストリームデータベースに移行されているかどうかを確認します。

### 複合主キーを使用する {#use-a-composite-primary-key}

アップストリームスキーマが次のとおりであると想定します。

```sql
CREATE TABLE `tbl_multi_pk` (
  `auto_pk_c1` bigint(20) NOT NULL,
  `uuid_c2` bigint(20) NOT NULL,
  `content_c3` text,
  PRIMARY KEY (`auto_pk_c1`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

次の要件が満たされている場合：

-   アプリケーションは、 `auto_pk_c1`列の`PRIMARY KEY`属性に依存しません。
-   `auto_pk_c1`列と`uuid_c2`列で構成される複合主キーは、グローバルに一意です。
-   アプリケーションで複合主キーを使用することは許容されます。

次に、次の手順を実行して、シャーディングされたテーブルをマージするときに`auto_pk_c1`列が原因である可能性がある`ERROR 1062 (23000): Duplicate entry '***' for key 'PRIMARY'`エラーを修正できます。

1.  完全なデータ移行の前に、データをマージおよび移行するためのテーブルをダウンストリームデータベースに作成します。 `auto_pk_c1`列に`PRIMARY KEY`属性を指定せずに、 `auto_pk_c1`列と`uuid_c2`列を使用して複合主キーを構成します。

    ```sql
    CREATE TABLE `tbl_multi_pk_c2` (
      `auto_pk_c1` bigint(20) NOT NULL,
      `uuid_c2` bigint(20) NOT NULL,
      `content_c3` text,
      PRIMARY KEY (`auto_pk_c1`,`uuid_c2`)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1
    ```

2.  完全な増分データ移行タスクを開始します。

3.  `query-status`を実行して、データ移行タスクが正常に処理されたかどうか、およびアップストリームからのデータが既にマージされてダウンストリームデータベースに移行されているかどうかを確認します。

## アップストリームRDSにシャーディングテーブルが含まれている場合の特別な処理 {#special-processing-when-the-upstream-rds-contains-sharded-tables}

アップストリームデータソースがRDSであり、シャーディングテーブルが含まれている場合、SQLクライアントに接続すると、MySQLbinlogのテーブル名が表示されない場合があります。たとえば、アップストリームがUCloud分散データベースである場合、binlogのテーブル名に追加のプレフィックス`_0001`が付いている可能性があります。したがって、SQLクライアントのテーブル名ではなく、binlogのテーブル名に基づいて[テーブルルーティング](/dm/dm-key-features.md#table-routing)を構成する必要があります。

## アップストリームでテーブルを作成/削除します {#create-drop-tables-in-the-upstream}

[シャーディングされたテーブルからのデータのマージと移行](/dm/feature-shard-merge-pessimistic.md#principles)では、シャーディングDDLロックの調整は、ダウンストリームデータベースがすべてのアップストリームシャードテーブルのDDLステートメントを受信するかどうかに依存することは明らかです。さらに、DMは現在、アップストリームでのシャードテーブルの動的な作成または削除を**サポートしていません**。したがって、アップストリームでシャードテーブルを作成または削除するには、次の手順を実行することをお勧めします。

### 上流にシャードテーブルを作成する {#create-sharded-tables-in-the-upstream}

アップストリームに新しいシャードテーブルを作成する必要がある場合は、次の手順を実行します。

1.  アップストリームのシャーディングテーブルで実行されたすべてのシャーディングDDLの調整が完了するのを待ちます。

2.  `stop-task`を実行して、データ移行タスクを停止します。

3.  アップストリームに新しいシャードテーブルを作成します。

4.  `task.yaml`ファイルの構成で、新しく追加されたシャードテーブルを1つのダウンストリームテーブルで他の既存のシャードテーブルとマージできることを確認してください。

5.  `start-task`を実行してタスクを開始します。

6.  `query-status`を実行して、データ移行タスクが正常に処理されたかどうか、およびアップストリームからのデータが既にマージされてダウンストリームデータベースに移行されているかどうかを確認します。

### シャーディングされたテーブルをアップストリームにドロップします {#drop-sharded-tables-in-the-upstream}

シャードテーブルをアップストリームにドロップする必要がある場合は、次の手順を実行します。

1.  シャーディングされたテーブルを削除し、 [`SHOW BINLOG EVENTS`](https://dev.mysql.com/doc/refman/5.7/en/show-binlog-events.html)を実行してbinlogイベントの`DROP TABLE`ステートメントに対応する`End_log_pos`をフェッチし、 *Pos-M*としてマークします。

2.  `query-status`を実行して、DMによって処理されたbinlogイベントに対応する位置（ `syncerBinlog` ）をフェッチし、 *Pos-S*としてマークします。

3.  *Pos-S*が<em>Pos-M</em>より大きい場合は、DMが`DROP TABLE`のステートメントすべてを処理し、ドロップする前のテーブルのデータがダウンストリームに移行されたため、後続の操作を実行できることを意味します。それ以外の場合は、DMがデータの移行を完了するのを待ちます。

4.  `stop-task`を実行してタスクを停止します。

5.  `task.yaml`ファイルの構成が、アップストリームでドロップされたシャードテーブルを無視していることを確認してください。

6.  `start-task`を実行してタスクを開始します。

7.  `query-status`を実行して、データ移行タスクが正常に処理されたかどうかを確認します。

## 制限速度と交通流制御 {#speed-limits-and-traffic-flow-control}

複数のアップストリームMySQLまたはMariaDBインスタンスからのデータがマージされ、ダウンストリームの同じTiDBクラスタに移行されると、各アップストリームインスタンスに対応するすべてのDMワーカーは、完全なデータレプリケーションと増分データレプリケーションを同時に実行します。これは、DMワーカーの数が増えると、デフォルトの同時実行度（完全なデータ移行で`pool-size` 、増分データレプリケーションで`worker-count` ）が累積し、ダウンストリームデータベースが過負荷になる可能性があることを意味します。この場合、TiDBおよびDMの監視メトリックに基づいて予備的なパフォーマンス分析を実行し、各同時実行パラメーターの値を調整する必要があります。将来的には、DMは部分的に自動化された交通流制御をサポートすることが期待されています。
