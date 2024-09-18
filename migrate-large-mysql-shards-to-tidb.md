---
title: Migrate and Merge MySQL Shards of Large Datasets to TiDB
summary: DumplingとTiDB Lightning を使用して、MySQL から TiDB にシャードの大規模なデータセットを移行およびマージする方法と、さまざまな MySQL シャードから TiDB に増分データ変更を複製するように DM タスクを構成する方法について学習します。
---

# 大規模データセットの MySQL シャードを TiDB に移行してマージする {#migrate-and-merge-mysql-shards-of-large-datasets-to-tidb}

大規模な MySQL データセット (たとえば、1 TiB 以上) を異なるパーティションから TiDB に移行する場合、移行中に業務からすべての TiDB クラスター書き込み操作を一時停止できるときは、 TiDB Lightning を使用して移行を迅速に行うことができます。移行後は、TiDB DM を使用して業務ニーズに応じて増分レプリケーションを実行することもできます。このドキュメントの「大規模なデータセット」は通常、約 1 TiB 以上のデータを意味します。

このドキュメントでは、例を使用して、このような種類の移行の手順全体を説明します。

MySQL シャードのデータ サイズが 1 TiB 未満の場合は、 [小さなデータセットの MySQL シャードを TiDB に移行してマージする](/migrate-small-mysql-shards-to-tidb.md)で説明した手順に従うことができます。この手順では、完全移行と増分移行の両方がサポートされており、手順が簡単です。

このドキュメントの例では、 `my_db1`と`my_db2` 2 つのデータベースがあることを前提としています。Dumplingを使用して、 `my_db1`から 2 つのテーブル`table1`と`table2` 、 `my_db2`から 2 つのテーブル`table3`と`table4`をそれぞれエクスポートします。その後、 TiDB Lightning を使用して、エクスポートした 4 つのテーブルを、ターゲット TiDB の`mydb`から同じ`table5`にインポートしてマージします。

このドキュメントでは、次の手順に従ってデータを移行できます。

1.  Dumplingを使用して完全なデータをエクスポートします。この例では、2 つのアップストリーム データベースからそれぞれ 2 つのテーブルをエクスポートします。

    -   `my_db1`から`table1`と`table2`エクスポート
    -   `my_db2`から`table3`と`table4`エクスポート

2.  TiDB Lightning を起動して、TiDB の`mydb.table5`にデータを移行します。

3.  (オプション) TiDB DM を使用して増分レプリケーションを実行します。

## 前提条件 {#prerequisites}

開始する前に、次のドキュメントを参照して移行タスクの準備をしてください。

-   [TiUPを使用して DMクラスタをデプロイ](/dm/deploy-a-dm-cluster-using-tiup.md)
-   [TiUPを使用してDumplingとLightningをデプロイ](/migration-tools.md)
-   [Dumplingのダウンストリーム権限要件](/dumpling-overview.md#export-data-from-tidb-or-mysql)
-   [TiDB Lightningのダウンストリーム権限要件](/tidb-lightning/tidb-lightning-requirements.md)
-   [TiDB Lightningのダウンストリームstorageスペース](/tidb-lightning/tidb-lightning-requirements.md)
-   [DMワーカーに必要な権限](/dm/dm-worker-intro.md)

### シャードテーブルの競合をチェックする {#check-conflicts-for-sharded-tables}

移行に異なるシャード テーブルからのデータのマージが含まれる場合、マージ中に主キーまたは一意のインデックスの競合が発生する可能性があります。したがって、移行前に、ビジネスの観点から現在のシャーディング スキームを詳しく検討し、競合を回避する方法を見つける必要があります。詳細については、 [複数のシャードテーブル間の主キーまたは一意のインデックス間の競合を処理する](/dm/shard-merge-best-practices.md#handle-conflicts-between-primary-keys-or-unique-indexes-across-multiple-sharded-tables)参照してください。以下に簡単に説明します。

表1～4が次のように同じ表構造を持っていると仮定します。

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

これら 4 つのテーブルでは、 `id`列目が主キーです。これは自動増分であるため、異なるシャード テーブルで重複した`id`の範囲が生成され、移行中にターゲット テーブルで主キーの競合が発生します。一方、 `sid`列目はシャーディング キーであり、インデックスがグローバルに一意であることを保証します。そのため、ターゲット`table5`の`id`列目の一意制約を削除して、データ マージの競合を回避できます。

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

## ステップ1. Dumplingを使用して完全なデータをエクスポートする {#step1-use-dumpling-to-export-full-data}

エクスポートする複数のシャード テーブルが同じアップストリーム MySQL インスタンス内にある場合は、 Dumplingの`-f`パラメータを直接使用して、1 回の操作でエクスポートできます。

シャードされたテーブルが異なる MySQL インスタンスに保存されている場合は、 Dumpling を使用してそれらをそれぞれエクスポートし、エクスポートされた結果を同じ親ディレクトリに配置できます。

次の例では、両方の方法が使用され、エクスポートされたデータは同じ親ディレクトリに保存されます。

まず、次のコマンドを実行して、 Dumpling を使用して`my_db1`から`table1`と`table2`エクスポートします。

```shell
tiup dumpling -h ${ip} -P 3306 -u root -t 16 -r 200000 -F 256MB -B my_db1 -f 'my_db1.table[12]' -o ${data-path}/my_db1
```

次の表は、上記のコマンドのパラメータについて説明しています。Dumpling パラメータの詳細については、 [Dumplingの概要](/dumpling-overview.md)参照Dumplingてください。

| パラメータ               | 説明                                                                                                                     |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `-u`または`--user`     | 使用するユーザー名を指定します。                                                                                                       |
| `-p`または`--password` | 使用するパスワードを指定します。                                                                                                       |
| `-p`または`--port`     | 使用するポートを指定します。                                                                                                         |
| `-h`または`--host`     | データ ソースの IP アドレスを指定します。                                                                                                |
| `-t`または`--thread`   | エクスポートのスレッド数を指定します。スレッド数を増やすと、 Dumplingの同時実行性とエクスポート速度が向上し、データベースのメモリ消費量が増加します。したがって、数値を大きくしすぎることはお勧めしません。通常は 64 未満です。 |
| `-o`または`--output`   | storageのエクスポート ディレクトリを指定します。ローカル ファイル パスまたは[外部storageURI](/external-storage-uri.md)をサポートします。                           |
| `-r`または`--row`      | 1 つのファイル内の最大行数を指定します。このパラメータを使用すると、 Dumpling はテーブル内の同時実行を有効にしてエクスポートを高速化し、メモリ使用量を削減します。                                |
| `-F`                | 1 つのファイルの最大サイズを指定します。単位は`MiB`です。値は 256 MiB に抑えることをお勧めします。                                                              |
| `-B`または`--database` | エクスポートするデータベースを指定します。                                                                                                  |
| `-f`または`--filter`   | フィルタ パターンに一致するテーブルをエクスポートします。フィルタ構文については、 [テーブルフィルター](/table-filter.md)参照してください。                                       |

`${data-path}`に十分な空き領域があることを確認してください。単一テーブルのサイズが大きすぎるためにバックアップ プロセスが中断されるのを避けるため、 `-F`オプションを使用することを強くお勧めします。

次に、次のコマンドを実行して、 Dumpling を使用して`my_db2`から`table3`と`table4`エクスポートします。パスは`${data-path}/my_db1`ではなく`${data-path}/my_db2`であることに注意してください。

```shell
tiup dumpling -h ${ip} -P 3306 -u root -t 16 -r 200000 -F 256MB -B my_db2 -f 'my_db2.table[34]' -o ${data-path}/my_db2
```

以上の手順で、すべてのソース データ テーブルが`${data-path}`ディレクトリにエクスポートされました。エクスポートしたデータをすべて同じディレクトリに置くと、その後のTiDB Lightningによるインポートが便利になります。

増分レプリケーションに必要な開始位置情報は、それぞれ`${data-path}`ディレクトリの`my_db1`および`my_db2`サブディレクトリの`metadata`ファイルにあります。これらは、 Dumplingによって自動的に生成されるメタ情報ファイルです。増分レプリケーションを実行するには、これらのファイルにbinlog の場所情報を記録する必要があります。

## ステップ2. TiDB Lightningを起動してエクスポートしたデータ全体をインポートする {#step-2-start-tidb-lightning-to-import-full-exported-data}

移行のためにTiDB Lightning を開始する前に、チェックポイントの処理方法を理解し、ニーズに応じて適切な方法を選択することをお勧めします。

### チェックポイント {#checkpoints}

大量のデータの移行には通常、数時間から数日かかります。長時間実行されるプロセスが予期せず中断される可能性はあります。データの一部がすでにインポートされている場合でも、すべてを最初からやり直すのは非常に面倒です。

幸いなことに、 TiDB Lightning には`checkpoints`という機能があり、これにより、 TiDB Lightning はインポートの進行状況`checkpoints`として随時保存し、中断されたインポート タスクを再起動時に最新のチェックポイントから再開できるようになります。

回復不可能なエラー (データ破損など) が原因でTiDB Lightningタスクがクラッシュした場合、チェックポイントから再開されず、エラーが報告されてタスクが終了します。インポートされたデータの安全性を確保するには、他の手順に進む前に、 `tidb-lightning-ctl`コマンドを使用してこれらのエラーを解決する必要があります。オプションは次のとおりです。

-   --checkpoint-error-destroy: このオプションを使用すると、まずテーブル内の既存のデータをすべて破棄して、失敗したターゲット テーブルへのデータのインポートを最初から再開できます。
-   --checkpoint-error-ignore: 移行が失敗した場合、このオプションはエラーが発生しなかったかのようにエラー状態をクリアします。
-   --checkpoint-remove: このオプションは、エラーに関係なく、すべてのチェックポイントをクリアします。

詳細については[TiDB Lightningチェックポイント](/tidb-lightning/tidb-lightning-checkpoints.md)参照してください。

### ターゲットスキーマを作成する {#create-a-target-schema}

下流に`mydb.table5`作成します。

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

`tidb-lightning`開始するには、次の手順に従ってください。

1.  toml ファイルを編集します。次の例では`tidb-lightning.toml`が使用されています。

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

2.  `tidb-lightning`実行します。シェルでプログラム名を直接呼び出してプログラムを実行すると、SIGHUP シグナルを受け取った後にプロセスが予期せず終了することがあります。 `nohup`や`screen`や`tiup`などのツールを使用してプログラムを実行し、プロセスをシェルのバックグラウンドに置くことをお勧めします。 S3 から移行する場合は、Amazon S3 バックエンドストアにアクセスできるアカウントの SecretKey と AccessKey を環境変数として Lightning ノードに渡す必要があります。 `~/.aws/credentials`からの認証情報ファイルの読み取りもサポートされています。例:

    ```shell
    export AWS_ACCESS_KEY_ID=${access_key}
    export AWS_SECRET_ACCESS_KEY=${secret_key}
    nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out 2>&1 &
    ```

3.  移行タスクを開始した後、次のいずれかの方法を使用して進行状況を確認できます。

    -   `grep`ツールを使用して、ログ内のキーワード`progress`検索します。デフォルトでは、進行状況を報告するメッセージが 5 分ごとにログ ファイルにフラッシュされます。
    -   監視ダッシュボードで進行状況をビュー。詳細については、 [TiDB Lightning監視](/tidb-lightning/monitor-tidb-lightning.md)参照してください。
    -   進捗状況はWebページからビュー[ウェブインターフェース](/tidb-lightning/tidb-lightning-web-interface.md)参照してください。

TiDB Lightning はインポートを完了すると、自動的に終了します。最後の行の`tidb-lightning.log`に`the whole procedure completed`含まれているかどうかを確認します。含まれている場合は、インポートは成功です。含まれていない場合は、インポートでエラーが発生します。エラー メッセージの指示に従ってエラーに対処してください。

> **注記：**
>
> 移行が成功したかどうかに関係なく、ログの最後の行は常に`tidb lightning exit`になります。これは、 TiDB Lightning が正常に終了したことを意味するだけで、インポート タスクが正常に完了したことを保証するものではありません。

移行中に問題が発生した場合は、 [TiDB Lightningよくある質問](/tidb-lightning/tidb-lightning-faq.md)参照してください。

## ステップ3. (オプション) DMを使用して増分レプリケーションを実行する {#step-3-optional-use-dm-to-perform-incremental-replication}

ソース データベース内の指定された位置からbinlogに基づいてデータの変更を TiDB に複製するには、TiDB DM を使用して増分レプリケーションを実行します。

### データソースを追加する {#add-the-data-source}

`source1.yaml`という新しいデータ ソース ファイルを作成し、DM にアップストリーム データ ソースを構成して、次のコンテンツを追加します。

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

ターミナルで次のコマンドを実行します`tiup dmctl`使用して、データ ソース構成を DM クラスターにロードします。

```shell
tiup dmctl --master-addr ${advertise-addr} operate-source create source1.yaml
```

パラメータの説明は以下のとおりです。

| パラメータ                   | 説明                                                                       |
| ----------------------- | ------------------------------------------------------------------------ |
| `--master-addr`         | dmctl が接続するクラスター内の任意の DM マスター ノードの {advertise-addr}。例: 172.16.10.71:8261 |
| `operate-source create` | データ ソースを DM クラスターにロードします。                                                |

すべての MySQL アップストリーム インスタンスがデータ ソースとして DM に追加されるまで、上記の手順を繰り返します。

### レプリケーションタスクを作成する {#create-a-replication-task}

`task.yaml`というタスク構成ファイルを編集して、各データ ソースの増分レプリケーション モードとレプリケーション開始点を構成します。

```yaml
name: task-test               # The name of the task. Should be globally unique.
task-mode: incremental        # The mode of the task. "incremental" means full data migration is skipped and only incremental replication is performed.
# Required for incremental replication from sharded tables. By default, the "pessimistic" mode is used.
# If you have a deep understanding of the principles and usage limitations of the optimistic mode, you can also use the "optimistic" mode.
# For more information, see [Merge and Migrate Data from Sharded Tables](https://docs.pingcap.com/tidb/dev/feature-shard-merge/).

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

その他の構成については、 [DM 高度なタスクコンフィグレーションファイル](/dm/task-configuration-file-full.md)参照してください。

データ移行タスクを開始する前に、 `tiup dmctl`の`check-task`サブコマンドを使用して、構成が DM 構成要件を満たしているかどうかを確認することをお勧めします。

```shell
tiup dmctl --master-addr ${advertise-addr} check-task task.yaml
```

`tiup dmctl`使用して次のコマンドを実行し、データ移行タスクを開始します。

```shell
tiup dmctl --master-addr ${advertise-addr} start-task task.yaml
```

このコマンドのパラメータは次のように記述されます。

| パラメータ      | 説明                                                                       |
| ---------- | ------------------------------------------------------------------------ |
| --マスターアドレス | dmctl が接続するクラスター内の任意の DM マスター ノードの {advertise-addr}。例: 172.16.10.71:8261 |
| タスク開始      | データ移行タスクを開始します。                                                          |

タスクの開始に失敗した場合は、返された結果のプロンプト メッセージに従って構成を変更し、 `tiup dmctl`の`start-task task.yaml`サブコマンドを実行してタスクを再起動します。問題が発生した場合は、 [エラーの処理](/dm/dm-error-handling.md)と[TiDB データ移行に関するFAQ](/dm/dm-faq.md)参照してください。

### 移行ステータスを確認する {#check-the-migration-status}

`tiup dmctl`の`query-status`コマンドを実行すると、DM クラスターで実行中の移行タスクがあるかどうか、およびそのステータスを確認できます。

```shell
tiup dmctl --master-addr ${advertise-addr} query-status ${task-name}
```

詳細については[クエリステータス](/dm/dm-query-status.md)参照してください。

### タスクを監視し、ログを表示する {#monitor-tasks-and-view-logs}

Grafana またはログを通じて、移行タスクの履歴と内部運用メトリックを表示できます。

-   Grafana経由

    TiUPを使用して DM クラスターをデプロイする際に、Prometheus、Alertmanager、Grafana が正しくデプロイされていれば、Grafana で DM 監視メトリックを表示できます。具体的には、デプロイ時に指定した IP アドレスとポートを Grafana に入力し、DM ダッシュボードを選択します。

-   ログ経由

    DM が実行中の場合、DM-master、DM-worker、dmctl は移行タスクに関する情報を含むログを出力します。各コンポーネントのログ ディレクトリは次のとおりです。

    -   DM マスター ログ ディレクトリ: DM マスター コマンド ライン パラメータ`--log-file`で指定されます。DM がTiUP を使用して展開されている場合、ログ ディレクトリは`/dm-deploy/dm-master-8261/log/`です。
    -   DM-worker ログ ディレクトリ: DM-worker コマンドライン パラメータ`--log-file`で指定されます。DM がTiUP を使用してデプロイされている場合、ログ ディレクトリは`/dm-deploy/dm-worker-8262/log/`です。

## 参照 {#see-also}

-   [Dumpling](/dumpling-overview.md)
-   [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)
-   [悲観モードと楽観的モード](/dm/feature-shard-merge.md)
-   [データ移行タスクを一時停止する](/dm/dm-pause-task.md)
-   [データ移行タスクを再開する](/dm/dm-resume-task.md)
-   [データ移行タスクを停止する](/dm/dm-stop-task.md)
-   [データソースのエクスポートとインポート、およびクラスターのタスクコンフィグレーション](/dm/dm-export-import-config.md)
-   [失敗したDDLステートメントの処理](/dm/handle-failed-ddl-statements.md)
-   [エラーの処理](/dm/dm-error-handling.md)
