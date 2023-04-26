---
title: Migrate and Merge MySQL Shards of Large Datasets to TiDB
summary: Learn how to migrate and merge large datasets of shards from MySQL into TiDB using Dumpling and TiDB Lightning, as well as how to configure the DM task to replicate incremental data changes from different MySQL shards into TiDB.
---

# 大規模なデータセットの MySQL シャードを TiDB に移行およびマージする {#migrate-and-merge-mysql-shards-of-large-datasets-to-tidb}

大規模な MySQL データセット (たとえば、1 TiB を超える) を異なるパーティションから TiDB に移行する必要があり、移行中にビジネスからすべての TiDB クラスター書き込み操作を一時停止できる場合は、 TiDB Lightningを使用して実行できます。移行を迅速に。移行後、TiDB DM を使用して、ビジネス ニーズに応じて増分レプリケーションを実行することもできます。このドキュメントの「大規模なデータセット」とは、通常、1 TiB 以上のデータを意味します。

このドキュメントでは、例を使用して、この種の移行の手順全体を説明します。

MySQL シャードのデータ サイズが 1 TiB 未満の場合は、 [小さなデータセットの MySQL シャードを TiDB に移行およびマージする](/migrate-small-mysql-shards-to-tidb.md)で説明されている手順に従うことができます。これは、完全移行と増分移行の両方をサポートし、手順がより簡単になります。

このドキュメントの例では、2 つのデータベース`my_db1`と`my_db2`があると想定しています。 Dumplingを使用して、2 つのテーブル`table1`と`table2` `my_db1`から、2 つのテーブル`table3`と`table4`を`my_db2`からそれぞれエクスポートします。その後、 TiDB Lightning を使用して、エクスポートされた 4 つのテーブルをターゲット TiDB の`mydb`から同じ`table5`にインポートしてマージします。

このドキュメントでは、次の手順に従ってデータを移行できます。

1.  Dumpling を使用して完全なデータをエクスポートします。この例では、2 つのアップストリーム データベースからそれぞれ 2 つのテーブルをエクスポートします。

    -   `my_db1`から`table1`と`table2`をエクスポート
    -   `my_db2`から`table3`と`table4`をエクスポート

2.  TiDB Lightning を起動して、TiDB の`mydb.table5`にデータを移行します。

3.  (オプション) TiDB DM を使用して増分レプリケーションを実行します。

## 前提条件 {#prerequisites}

開始する前に、次のドキュメントを参照して、移行タスクの準備をしてください。

-   [TiUPを使用して DMクラスタをデプロイ](/dm/deploy-a-dm-cluster-using-tiup.md)
-   [TiUP を使用してDumplingと Lightningをデプロイ](/migration-tools.md)
-   [Dumplingのダウンストリーム権限要件](/dumpling-overview.md#export-data-from-tidb-or-mysql)
-   [TiDB Lightningのダウンストリーム権限要件](/tidb-lightning/tidb-lightning-requirements.md)
-   [TiDB Lightningのダウンストリームstorageスペース](/tidb-lightning/tidb-lightning-requirements.md)
-   [DM-worker に必要な権限](/dm/dm-worker-intro.md)

### シャード テーブルの競合をチェックする {#check-conflicts-for-sharded-tables}

移行に異なるシャード テーブルからのデータのマージが含まれる場合、マージ中に主キーまたは一意のインデックスの競合が発生する可能性があります。したがって、移行の前に、ビジネスの観点から現在のシャーディング スキームを詳しく調べ、競合を回避する方法を見つける必要があります。詳細については、 [複数のシャード テーブル間で主キーまたは一意のインデックス間の競合を処理する](/dm/shard-merge-best-practices.md#handle-conflicts-between-primary-keys-or-unique-indexes-across-multiple-sharded-tables)を参照してください。以下は簡単な説明です。

テーブル 1 ～ 4 は、次のように同じテーブル構造を持っているとします。

{{< copyable "" >}}

```sql
CREATE TABLE `table1` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `sid` bigint(20) NOT NULL,
  `pid` bigint(20) NOT NULL,
  `comment` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sid` (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

これら 4 つのテーブルでは、 `id`列が主キーです。これは自動増分であり、異なるシャード テーブルが重複した`id`の範囲を生成し、移行中にターゲット テーブルで主キーの競合が発生します。一方、 `sid`列はシャーディング キーであり、インデックスがグローバルに一意であることを保証します。したがって、ターゲット`table5`の`id`列の一意の制約を削除して、データ マージの競合を回避できます。

{{< copyable "" >}}

```sql
CREATE TABLE `table5` (
  `id` bigint(20) NOT NULL,
  `sid` bigint(20) NOT NULL,
  `pid` bigint(20) NOT NULL,
  `comment` varchar(255) DEFAULT NULL,
  INDEX (`id`),
  UNIQUE KEY `sid` (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

## ステップ1。 Dumpling を使用して完全なデータをエクスポートする {#step1-use-dumpling-to-export-full-data}

エクスポートする複数のシャード テーブルが同じアップストリーム MySQL インスタンスにある場合は、 Dumplingの`-f`パラメータを直接使用して、1 回の操作でそれらをエクスポートできます。

分割されたテーブルが異なる MySQL インスタンスに格納されている場合は、 Dumpling を使用してそれぞれをエクスポートし、エクスポートした結果を同じ親ディレクトリに配置できます。

次の例では、両方の方法が使用され、エクスポートされたデータは同じ親ディレクトリに格納されます。

まず、次のコマンドを実行してDumpling を使用して`my_db1`から`table1`と`table2`をエクスポートします。

{{< copyable "" >}}

```shell
tiup dumpling -h ${ip} -P 3306 -u root -t 16 -r 200000 -F 256MB -B my_db1 -f 'my_db1.table[12]' -o ${data-path}/my_db1
```

次の表では、上記のコマンドのパラメーターについて説明します。 Dumplingパラメータの詳細については、 [Dumplingの概要](/dumpling-overview.md)を参照してください。

| パラメータ               | 説明                                                                                                                       |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `-u`または`--user`     | 使用するユーザー名を指定します。                                                                                                         |
| `-p`または`--password` | 使用するパスワードを指定します。                                                                                                         |
| `-p`または`--port`     | 使用するポートを指定します。                                                                                                           |
| `-h`または`--host`     | データ ソースの IP アドレスを指定します。                                                                                                  |
| `-t`または`--thread`   | エクスポートのスレッド数を指定します。スレッド数を増やすと、 Dumplingの同時実行性とエクスポート速度が向上し、データベースのメモリ消費量が増加します。そのため、あまり大きな数値を設定することはお勧めしません。通常は 64 未満です。 |
| `-o`または`--output`   | ローカル ファイル パスまたは[外部storageURL](/br/backup-and-restore-storages.md#url-format)をサポートするstorageのエクスポート ディレクトリを指定します。          |
| `-r`または`--row`      | 1 つのファイル内の最大行数を指定します。このパラメータを使用すると、 Dumpling はテーブル内の同時実行性を有効にして、エクスポートを高速化し、メモリ使用量を削減します。                                |
| `-F`                | 1 つのファイルの最大サイズを指定します。単位は`MiB`です。値を 256 MiB に維持することをお勧めします。                                                               |
| `-B`または`--database` | エクスポートするデータベースを指定します。                                                                                                    |
| `-f`または`--filter`   | フィルター パターンに一致するテーブルをエクスポートします。フィルター構文については、 [テーブルフィルター](/table-filter.md)を参照してください。                                      |

`${data-path}`に十分な空き容量があることを確認してください。 1 つのテーブルが大きすぎるためにバックアップ プロセスが中断されるのを避けるために、 `-F`オプションを使用することを強くお勧めします。

次に、次のコマンドを実行してDumplingを使用して`table3`と`table4` `my_db2`からエクスポートします。パスは`${data-path}/my_db1`ではなく`${data-path}/my_db2`であることに注意してください。

{{< copyable "" >}}

```shell
tiup dumpling -h ${ip} -P 3306 -u root -t 16 -r 200000 -F 256MB -B my_db2 -f 'my_db2.table[34]' -o ${data-path}/my_db2
```

前述の手順の後、すべてのソース データ テーブルが`${data-path}`ディレクトリにエクスポートされます。エクスポートされたすべてのデータを同じディレクトリに配置すると、 TiDB Lightningによる後続のインポートが便利になります。

増分複製に必要な開始位置情報は、それぞれ`${data-path}`ディレクトリーの`my_db1`および`my_db2`サブディレクトリー内の`metadata`ファイルにあります。 Dumplingが自動生成するメタ情報ファイルです。増分レプリケーションを実行するには、これらのファイルにbinlogの場所情報を記録する必要があります。

## ステップ 2. TiDB Lightning を起動して、エクスポートされた完全なデータをインポートします {#step-2-start-tidb-lightning-to-import-full-exported-data}

移行のためにTiDB Lightningを開始する前に、チェックポイントの処理方法を理解し、必要に応じて適切な方法を選択することをお勧めします。

### チェックポイント {#checkpoints}

大量のデータを移行するには、通常、数時間から数日かかります。長期実行プロセスが予期せず中断される可能性があります。データの一部が既にインポートされている場合でも、すべてを最初からやり直すのは非常にイライラすることがあります。

幸いなことに、 TiDB Lightning は`checkpoints`と呼ばれる機能を提供します。これにより、 TiDB Lightning はインポートの進行状況を時々 `checkpoints`として保存し、中断されたインポート タスクを再起動時に最新のチェックポイントから再開できるようにします。

回復不能なエラー (データの破損など) が原因でTiDB Lightningタスクがクラッシュした場合、チェックポイントから取得されず、エラーが報告されてタスクが終了します。インポートされたデータの安全性を確保するには、他の手順に進む前に、 `tidb-lightning-ctl`コマンドを使用してこれらのエラーを解決する必要があります。オプションは次のとおりです。

-   --checkpoint-error-destroy: このオプションを使用すると、最初に失敗したターゲット テーブル内の既存のデータをすべて破棄することにより、データのインポートを失敗したターゲット テーブルに最初からやり直すことができます。
-   --checkpoint-error-ignore: 移行が失敗した場合、このオプションは、エラーが発生していないかのようにエラー ステータスをクリアします。
-   --checkpoint-remove: このオプションは、エラーに関係なく、すべてのチェックポイントを単純にクリアします。

詳細については、 [TiDB Lightningチェックポイント](/tidb-lightning/tidb-lightning-checkpoints.md)を参照してください。

### ターゲット スキーマを作成する {#create-a-target-schema}

下流に`mydb.table5`を作成します。

{{< copyable "" >}}

```sql
CREATE TABLE `table5` (
  `id` bigint(20) NOT NULL,
  `sid` bigint(20) NOT NULL,
  `pid` bigint(20) NOT NULL,
  `comment` varchar(255) DEFAULT NULL,
  INDEX (`id`),
  UNIQUE KEY `sid` (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

### 移行タスクを開始する {#start-the-migration-task}

次の手順に従って、 `tidb-lightning`を開始します。

1.  toml ファイルを編集します。 `tidb-lightning.toml`は、次の例で使用されています。

    ```toml
    [lightning]
    # Logs
    level = "info"
    file = "tidb-lightning.log"

    [mydumper]
    data-source-dir = ${data-path}

    [tikv-importer]
    # Choose a local backend.
    # "local": The default mode. It is used for large data volumes greater than 1 TiB. During migration, downstream TiDB cannot provide services.
    # "tidb": Used for data volumes less than 1 TiB. During migration, downstream TiDB can provide services normally.
    # For more information, see [TiDB Lightning Backends](https://docs.pingcap.com/tidb/stable/tidb-lightning-backends)
    backend = "local"
    # Set the temporary directory for the sorted key value pairs. It must be empty.
    # The free space must be greater than the size of the dataset to be imported.
    # It is recommended that you use a directory different from `data-source-dir` to get better migration performance by consuming I/O resources exclusively.
    sorted-kv-dir = "${sorted-kv-dir}"

    # Set the renaming rules ('routes') from source to target tables, in order to support merging different table shards into a single target table. Here you migrate `table1` and `table2` in `my_db1`, and `table3` and `table4` in `my_db2`, to the target `table5` in downstream `my_db`.
    [[mydumper.files]]
    pattern = '(^|/)my_db1\.table[1-2]\..*\.sql$'
    schema = "my_db"
    table = "table5"
    type = "sql"

    [[mydumper.files]]
    pattern = '(^|/)my_db2\.table[3-4]\..*\.sql$'
    schema = "my_db"
    table = "table5"
    type = "sql"

    # Information of the target TiDB cluster. For example purposes only. Replace the IP address with your IP address.
    [tidb]
    # Information of the target TiDB cluster.
    # Values here are only for illustration purpose. Replace them with your own values.
    host = ${host}           # For example: "172.16.31.1"
    port = ${port}           # For example: 4000
    user = "${user_name}"    # For example: "root"
    password = "${password}" # For example: "rootroot"
    status-port = ${status-port} # The table information is read from the status port. For example: 10080
    # the IP address of the PD cluster. TiDB Lightning gets some information through the PD cluster.
    # For example: "172.16.31.3:2379".
    # When backend = "local", make sure that the values of status-port and pd-addr are correct. Otherwise an error will occur.
    pd-addr = "${ip}:${port}"
    ```

2.  `tidb-lightning`を実行します。シェルでプログラム名を直接呼び出してプログラムを実行すると、プロセスが SIGHUP シグナルを受信した後に予期せず終了することがあります。 `nohup`または`screen`または`tiup`などのツールを使用してプログラムを実行し、プロセスをシェルのバックグラウンドに置くことをお勧めします。 S3 から移行する場合、Amazon S3 バックエンド ストアにアクセスできるアカウントの SecretKey と AccessKey を環境変数として Lightning ノードに渡す必要があります。 `~/.aws/credentials`からの資格情報ファイルの読み取りもサポートされています。例えば：

    {{< copyable "" >}}

    ```shell
    export AWS_ACCESS_KEY_ID=${access_key}
    export AWS_SECRET_ACCESS_KEY=${secret_key}
    nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out 2>&1 &
    ```

3.  移行タスクの開始後、次のいずれかの方法を使用して進行状況を確認できます。

    -   `grep`ツールを使用して、ログ内のキーワード`progress`を検索します。デフォルトでは、進行状況を報告するメッセージが 5 分ごとにログ ファイルにフラッシュされます。
    -   監視ダッシュボードを介して進行状況をビュー。詳細については、 [TiDB Lightningモニタリング](/tidb-lightning/monitor-tidb-lightning.md)を参照してください。
    -   Web ページを介して進行状況をビュー。 [ウェブインターフェース](/tidb-lightning/tidb-lightning-web-interface.md)を参照してください。

TiDB Lightning がインポートを完了すると、自動的に終了します。 `tidb-lightning.log`最後の行に`the whole procedure completed`含まれているかどうかを確認します。はいの場合、インポートは成功です。 「いいえ」の場合、インポートでエラーが発生します。エラー メッセージの指示に従って、エラーに対処します。

> **ノート：**
>
> 移行が成功したかどうかにかかわらず、ログの最後の行は常に`tidb lightning exit`になります。これは、 TiDB Lightning が正常に終了したことを意味するだけであり、インポート タスクが正常に完了することを保証するものではありません。

移行中に問題が発生した場合は、 [TiDB LightningFAQ](/tidb-lightning/tidb-lightning-faq.md)を参照してください。

## ステップ 3. (オプション) DM を使用して増分レプリケーションを実行する {#step-3-optional-use-dm-to-perform-incremental-replication}

ソース データベースの指定された位置からのbinlogに基づくデータ変更を TiDB にレプリケートするには、TiDB DM を使用して増分レプリケーションを実行します。

### データ ソースを追加する {#add-the-data-source}

アップストリーム データ ソースを DM に構成する`source1.yaml`という名前の新しいデータ ソース ファイルを作成し、次の内容を追加します。

{{< copyable "" >}}

```yaml
# Configuration.
source-id: "mysql-01" # Must be unique.

# Specifies whether DM-worker pulls binlogs with GTID (Global Transaction Identifier).
# The prerequisite is that you have already enabled GTID in the upstream MySQL.
# If you have configured the upstream database service to switch master between different nodes automatically, you must enable GTID.
enable-gtid: true

from:
  host: "${host}"           # For example: 172.16.10.81
  user: "root"
  password: "${password}"   # Plaintext passwords are supported but not recommended. It is recommended that you use dmctl encrypt to encrypt plaintext passwords.
  port: ${port}             # For example: 3306
```

ターミナルで次のコマンドを実行します。 `tiup dmctl`を使用して、データ ソース構成を DM クラスターに読み込みます。

{{< copyable "" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} operate-source create source1.yaml
```

パラメータは次のとおりです。

| パラメータ                   | 説明                                                                       |
| ----------------------- | ------------------------------------------------------------------------ |
| `--master-addr`         | dmctl が接続するクラスター内の任意の DM マスター ノードの {advertise-addr}。例: 172.16.10.71:8261 |
| `operate-source create` | データ ソースを DM クラスターに読み込みます。                                                |

すべての MySQL アップストリーム インスタンスがデータ ソースとして DM に追加されるまで、上記の手順を繰り返します。

### レプリケーション タスクを作成する {#create-a-replication-task}

`task.yaml`というタスク構成ファイルを編集して、各データ ソースの増分レプリケーション モードとレプリケーションの開始点を構成します。

{{< copyable "" >}}

```yaml
name: task-test               # The name of the task. Should be globally unique.
task-mode: incremental        # The mode of the task. "incremental" means full data migration is skipped and only incremental replication is performed.
# Required for incremental replication from sharded tables. By default, the "pessimistic" mode is used.
# If you have a deep understanding of the principles and usage limitations of the optimistic mode, you can also use the "optimistic" mode.
# For more information, see [Merge and Migrate Data from Sharded Tables](https://docs.pingcap.com/zh/tidb/dev/feature-shard-merge/).

shard-mode: "pessimistic"

# Configure the access information of the target TiDB database instance:
target-database:              # The target database instance
  host: "${host}"             # For example: 127.0.0.1
  port: 4000
  user: "root"
  password: "${password}"     # It is recommended to use a dmctl encrypted password.

# Use block-allow-list to configure tables that require sync:
block-allow-list:             # The set of filter rules on matching tables in the data sources, to decide which tables need to migrate and which not. Use the black-white-list if the DM version is earlier than or equal to v2.0.0-beta.2.
  bw-rule-1:                  # The ID of the block and allow list rule.
    do-dbs: ["my_db1"]        # The databases to be migrated. Here, my_db1 of instance 1 and my_db2 of instance 2 are configured as two separate rules to demonstrate how to prevent my_db2 of instance 1 from being replicated.
  bw-rule-2:
    do-dbs: ["my_db2"]
routes:                               # Table renaming rules ('routes') from upstream to downstream tables, in order to support merging different sharded table into a single target table.
  route-rule-1:                       # Rule name. Migrate and merge table1 and table2 from my_db1 to the downstream my_db.table5.
    schema-pattern: "my_db1"          # Rule for matching upstream schema names. It supports the wildcards "*" and "?".
    table-pattern: "table[1-2]"       # Rule for matching upstream table names. It supports the wildcards "*" and "?".
    target-schema: "my_db"            # Name of the target schema.
    target-table: "table5"            # Name of the target table.
  route-rule-2:                       # Rule name. Migrate and merge table3 and table4 from my_db2 to the downstream my_db.table5.
    schema-pattern: "my_db2"
    table-pattern: "table[3-4]"
    target-schema: "my_db"
    target-table: "table5"

# Configure data sources. The following uses two data sources as an example.
mysql-instances:
  - source-id: "mysql-01"             # Data source ID. It is the source-id in source1.yaml.
    block-allow-list: "bw-rule-1"     # Use the block and allow list configuration above. Replicate `my_db1` in instance 1.
    route-rules: ["route-rule-1"]     # Use the configured routing rule above to merge upstream tables.
#       syncer-config-name: "global"  # Use the syncers configuration below.
    meta:                             # The position where the binlog replication starts when `task-mode` is `incremental` and the downstream database checkpoint does not exist. If the checkpoint exists, the checkpoint is used. If neither the `meta` configuration item nor the downstream database checkpoint exists, the migration starts from the latest binlog position of the upstream.
      binlog-name: "${binlog-name}"   # The log location recorded in ${data-path}/my_db1/metadata in Step 1. You can either specify binlog-name + binlog-pos or binlog-gtid. When the upstream database service is configured to switch master between different nodes automatically, use binlog GTID here.
      binlog-pos: ${binlog-position}
      # binlog-gtid:                  " For example: 09bec856-ba95-11ea-850a-58f2b4af5188:1-9"
  - source-id: "mysql-02"             # Data source ID. It is the source-id in source1.yaml.
    block-allow-list: "bw-rule-2"     # Use the block and allow list configuration above. Replicate `my_db2` in instance2.
    route-rules: ["route-rule-2"]     # Use the routing rule configured above.

#       syncer-config-name: "global"  # Use the syncers configuration below.
    meta:                             # The migration starting point of binlog when task-mode is incremental and there is no checkpoint in the downstream database. If there is a checkpoint, the checkpoint will be used.
      # binlog-name: "${binlog-name}"   # The log location recorded in ${data-path}/my_db2/metadata in Step 1. You can either specify binlog-name + binlog-pos or binlog-gtid. When the upstream database service is configured to switch master between different nodes automatically, use binlog GTID here.
      # binlog-pos: ${binlog-position}
      binlog-gtid: "09bec856-ba95-11ea-850a-58f2b4af5188:1-9"
# (Optional) If you need to incrementally replicate some data changes that have been covered in the full migration, you need to enable the safe mode to avoid data migration errors during incremental replication.
# This scenario is common when the fully migrated data is not part of a consistent snapshot of the data source, and the incremental data is replicated from a location earlier than the fully migrated data.
# syncers:           # The running parameters of the sync processing unit.
#  global:           # Configuration name.
# If set to true, DM changes INSERT to REPLACE, and changes UPDATE to a pair of DELETE and REPLACE for data source replication operations.
# Thus, it can apply DML repeatedly during replication when primary keys or unique indexes exist in the table structure.
# TiDB DM automatically starts safe mode within 1 minute before starting or resuming an incremental replication task.
#    safe-mode: true
```

その他の構成については、 [DM 拡張タスクコンフィグレーションファイル](/dm/task-configuration-file-full.md)を参照してください。

データ移行タスクを開始する前に、 `check-task`サブコマンド in `tiup dmctl`を使用して、構成が DM 構成要件を満たしているかどうかを確認することをお勧めします。

{{< copyable "" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} check-task task.yaml
```

`tiup dmctl`を使用して次のコマンドを実行し、データ移行タスクを開始します。

{{< copyable "" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} start-task task.yaml
```

このコマンドのパラメータは次のとおりです。

| パラメータ         | 説明                                                                       |
| ------------- | ------------------------------------------------------------------------ |
| --master-addr | dmctl が接続するクラスター内の任意の DM マスター ノードの {advertise-addr}。例: 172.16.10.71:8261 |
| 開始タスク         | データ移行タスクを開始します。                                                          |

タスクの起動に失敗した場合は、返された結果のプロンプト メッセージに従って構成を変更し、 `start-task task.yaml`サブコマンド in `tiup dmctl`を実行してタスクを再起動します。問題が発生した場合は、 [エラー処理](/dm/dm-error-handling.md)および[TiDB データ移行に関するFAQ](/dm/dm-faq.md)を参照してください。

### 移行状況を確認する {#check-the-migration-status}

`tiup dmctl`の`query-status`コマンドを実行することで、DM クラスターで実行中の移行タスクとそのステータスがあるかどうかを確認できます。

{{< copyable "" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} query-status ${task-name}
```

詳細については、 [クエリのステータス](/dm/dm-query-status.md)を参照してください。

### タスクの監視とログの表示 {#monitor-tasks-and-view-logs}

Grafana またはログを使用して、移行タスクの履歴と内部運用メトリックを表示できます。

-   グラファナ経由

    TiUPを使用して DM クラスターをデプロイするときに、Prometheus、Alertmanager、および Grafana が正しくデプロイされている場合は、Grafana で DM 監視メトリックを表示できます。具体的には、Grafana でのデプロイ時に指定した IP アドレスとポートを入力し、DM ダッシュボードを選択します。

-   ログ経由

    DM が実行されている場合、DM-master、DM-worker、および dmctl は移行タスクに関する情報を含むログを出力します。各コンポーネントのログディレクトリは以下の通りです。

    -   DM-master ログ ディレクトリ: DM-master コマンド ライン パラメータ`--log-file`で指定します。 DM がTiUPを使用して展開されている場合、ログ ディレクトリは`/dm-deploy/dm-master-8261/log/`です。
    -   DM-worker ログ ディレクトリ: DM-worker コマンド ライン パラメータ`--log-file`で指定します。 DM がTiUPを使用して展開されている場合、ログ ディレクトリは`/dm-deploy/dm-worker-8262/log/`です。

## こちらもご覧ください {#see-also}

-   [Dumpling](/dumpling-overview.md)
-   [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)
-   [悲観モードと楽観的モード](/dm/feature-shard-merge.md)
-   [データ移行タスクの一時停止](/dm/dm-pause-task.md)
-   [データ移行タスクの再開](/dm/dm-resume-task.md)
-   [データ移行タスクを停止する](/dm/dm-stop-task.md)
-   [データ ソースのエクスポートとインポート、およびクラスターのタスクコンフィグレーション](/dm/dm-export-import-config.md)
-   [失敗した DDL ステートメントの処理](/dm/handle-failed-ddl-statements.md)
-   [エラー処理](/dm/dm-error-handling.md)
