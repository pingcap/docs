---
title: Migrate and Merge MySQL Shards of Large Datasets to TiDB
summary: DumplingとTiDB Lightningを使用して、MySQLからTiDBへ大規模なシャードデータセットを移行およびマージする方法、そして異なるMySQLシャードからの増分データ変更をTiDBにレプリケートするようにDMタスクを構成する方法を学びます。
---

# 大規模データセットのMySQLシャードをTiDBに移行およびマージする {#migrate-and-merge-mysql-shards-of-large-datasets-to-tidb}

異なるパーティションに分散した大規模な MySQL データセット (例えば 1 TiB 以上) を TiDB に移行する場合、移行中に業務上の TiDB クラスタ書き込み操作をすべて停止できるのであれば、 TiDB Lightning を使用して迅速に移行を実行できます。移行後、業務ニーズに応じて TiDB DM を使用して増分レプリケーションを実行することもできます。このドキュメントにおける「大規模データセット」とは、通常 1 TiB 以上程度のデータを指します。

この文書では、例を用いて、このような移行の全手順を説明します。

MySQL シャードのデータサイズが 1 TiB 未満の場合は、[小規模データセットのMySQLシャードをTiDBに移行およびマージする](/migrate-small-mysql-shards-to-tidb.md)で説明されている手順に従うことができます。この手順では、完全移行と増分移行の両方がサポートされており、手順がより簡単です。

このドキュメントの例では、 `my_db1`と`my_db2`の 2つのデータベースがあることを前提としています。Dumplingを使用して`my_db1`から 2つのテーブル`table1`と`table2`を、 `my_db2`から 2つのテーブル`table3`と`table4`をそれぞれエクスポートします。その後、 TiDB Lightning を使用して、エクスポートされた 4つのテーブルをターゲット TiDB の`mydb`にある同じ`table5`にインポートしてマージします。

このドキュメントでは、以下の手順に従ってデータを移行する方法を説明します。

1. Dumplingを使用して完全なデータをエクスポートします。この例では、2つの上流データベースからそれぞれ2つのテーブルをエクスポートします。

    - `table1`から`table2`と`my_db1`をエクスポートします。
    - `table3`から`table4`と`my_db2`をエクスポートします。

2. TiDB Lightning を起動して、データを TiDB の`mydb.table5`に移行します。

3. （オプション）TiDB DMを使用して増分レプリケーションを実行します。

## 前提条件 {#prerequisites}

作業を開始する前に、移行作業の準備として以下のドキュメントを参照してください。

- [TiUPを使用してDMクラスタをデプロイ](/dm/deploy-a-dm-cluster-using-tiup.md)
- [TiUPを使用してDumplingとライトニングをデプロイ](/migration-tools.md)
- [Dumplingに必要なターゲットデータベース権限](/dumpling-overview.md#export-data-from-tidb-or-mysql)
- [TiDB Lightningに必要なターゲットデータベース権限](/tidb-lightning/tidb-lightning-requirements.md)
- [TiDB Lightningのダウンストリームストレージスペース](/tidb-lightning/tidb-lightning-requirements.md)
- [DMワーカーに必要な権限](/dm/dm-worker-intro.md)

### シャーディングされたテーブルの競合をチェックする {#check-conflicts-for-sharded-tables}

移行に異なるシャードテーブルのデータのマージが含まれる場合、マージ中に主キーまたは一意インデックスの競合が発生する可能性があります。したがって、移行前に、ビジネスの観点から現在のシャーディング スキームを詳しく調べ、競合を回避する方法を見つける必要があります。詳細については、 [複数のシャーディングされたテーブル間で主キーまたは一意インデックス間の競合を処理する](/dm/shard-merge-best-practices.md#handle-conflicts-between-primary-keys-or-unique-indexes-across-multiple-sharded-tables)を参照してください。以下に簡単に説明します。

表1～4は以下の表構造と同じであると仮定します。

```sql
CREATE TABLE `table1` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `sid` bigint NOT NULL,
  `pid` bigint NOT NULL,
  `comment` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sid` (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

これら4つのテーブルでは、 `id`列が主キーです。この列はAUTO_INCREMENTであるため、異なるシャーディングテーブルで重複する`id`範囲が生成され、移行中にターゲットテーブルで主キーの競合が発生します。一方、 `sid`列はシャーディング キーであり、インデックスがグローバルに一意であることを保証します。したがって、ターゲットの`table5`における`id`列の一意制約を削除することで、データ マージの競合を回避できます。

```sql
CREATE TABLE `table5` (
  `id` bigint NOT NULL,
  `sid` bigint NOT NULL,
  `pid` bigint NOT NULL,
  `comment` varchar(255) DEFAULT NULL,
  INDEX (`id`),
  UNIQUE KEY `sid` (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

## ステップ1. Dumplingを使用して全データをエクスポートします。 {#step1-use-dumpling-to-export-full-data}

エクスポートする複数のシャーディングされたテーブルが同じ上流のMySQLインスタンスにある場合は、 Dumplingの`-f`パラメータを直接使用して、単一の操作でエクスポートできます。

シャーディングされたテーブルが異なるMySQLインスタンスに保存されている場合は、 Dumplingを使用してそれぞれをエクスポートし、エクスポートされた結果を同じ親ディレクトリに配置することができます。

次の例では、両方の方法が使用され、エクスポートされたデータは同じ親ディレクトリに保存されます。

まず、次のコマンドを実行して、 Dumplingを使用して`table1`から`table2`と`my_db1`ます。

```shell
tiup dumpling -h ${ip} -P 3306 -u root -t 16 -r 200000 -F 256MB -B my_db1 -f 'my_db1.table[12]' -o ${data-path}/my_db1
```

以下の表は、上記のコマンドで使用されるパラメータについて説明しています。Dumplingのパラメータの詳細については、 [Dumplingの概要](/dumpling-overview.md)を参照してください。

| パラメータ               | 説明                                                                                                                                      |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `-u`または`--user`     | 使用するユーザー名を指定します。                                                                                                                        |
| `-p`または`--password` | 使用するパスワードを指定します。                                                                                                                        |
| `-p`または`--port`     | 使用するポートを指定します。                                                                                                                          |
| `-h`または`--host`     | データソースのIPアドレスを指定します。                                                                                                                    |
| `-t`または`--thread`   | エクスポートに使用するスレッド数を指定します。スレッド数を増やすと、Dumplingの並列処理能力とエクスポート速度が向上しますが、データベースのメモリ使用量も増加します。そのため、スレッド数をあまり大きく設定することは推奨されません。通常は64未満に設定してください。 |
| `-o`または`--output`   | ストレージのエクスポートディレクトリを指定します。ローカルファイルパスまたは[外部ストレージURI](/external-storage-uri.md)がサポートされます。                                              |
| `-r`または`--row`      | 単一ファイル内の最大行数を指定します。このパラメータを使用すると、Dumplingはテーブル内同時実行を有効にして、エクスポートを高速化し、メモリ使用量を削減します。                                                     |
| `-F`                | 単一ファイルの最大サイズを指定します。単位は`MiB`です。値は 256 MiB に設定することをお勧めします。                                                                                |
| `-B`または`--database` | エクスポートするデータベースを指定します。                                                                                                                   |
| `-f`または`--filter`   | フィルターパターンに一致するテーブルをエクスポートします。フィルターの構文については、[テーブルフィルター](/table-filter.md)を参照してください。                                                      |

`${data-path}`に十分な空き容量があることを確認してください。単一テーブルのサイズが大きすぎるためにバックアップ処理が中断されるのを避けるため`-F`オプションを使用することを強くお勧めします。

次に、以下のコマンドを実行して、 Dumplingを使用して`table3`から`table4`と`my_db2`をエクスポートします。パスは`${data-path}/my_db2`ではなく`${data-path}/my_db1`であることに注意してください。

```shell
tiup dumpling -h ${ip} -P 3306 -u root -t 16 -r 200000 -F 256MB -B my_db2 -f 'my_db2.table[34]' -o ${data-path}/my_db2
```

上記の手順の後、すべてのソースデータテーブルが`${data-path}`ディレクトリにエクスポートされます。エクスポートされたすべてのデータを同じディレクトリに配置することで、 TiDB Lightningによるその後のインポートが容易になります。

増分レプリケーションに必要な開始位置情報は、 `metadata`ディレクトリの`my_db1`サブディレクトリと`my_db2`サブディレクトリにある`${data-path}`ファイルに格納されています。これらはDumplingによって自動的に生成されるメタ情報ファイルです。増分レプリケーションを実行するには、これらのファイルにbinlogの場所情報を記録する必要があります。

## ステップ2. TiDB Lightningを起動して、エクスポートされたデータをすべてインポートします。 {#step-2-start-tidb-lightning-to-import-full-exported-data}

TiDB Lightningによる移行を開始する前に、チェックポイントの処理方法を理解し、ニーズに応じて適切な手順を選択することをお勧めします。

### チェックポイント {#checkpoints}

大量のデータを移行するには、通常数時間、場合によっては数日かかります。長時間かかる処理が予期せず中断される可能性も少なからずあります。たとえデータの一部が既にインポートされていたとしても、すべてを最初からやり直すのは非常に面倒な作業です。

幸いなことに、 TiDB Lightning には`checkpoints`という機能があり、 TiDB Lightning はインポートの進行状況を`checkpoints`として定期的に保存するため、中断されたインポートタスクを再起動時に最新のチェックポイントから再開できます。

TiDB Lightningタスクが回復不能なエラー（データ破損など）によりクラッシュした場合、チェックポイントから再開せず、エラーを報告してタスクを終了します。インポートされたデータの安全性を確保するため、他の手順に進む前に`tidb-lightning-ctl`コマンドを使用してこれらのエラーを解決する必要があります。オプションは次のとおりです。

- --checkpoint-error-destroy: このオプションを使用すると、失敗したターゲットテーブルへのデータインポートを最初からやり直すことができます。そのためには、まずそれらのテーブル内の既存のデータをすべて削除する必要があります。
- --checkpoint-error-ignore: マイグレーションが失敗した場合、このオプションはエラーが発生しなかったかのようにエラー状態をクリアします。
- --checkpoint-remove: このオプションは、エラーの有無に関わらず、すべてのチェックポイントを削除します。

詳細については、 [TiDB Lightningチェックポイント](/tidb-lightning/tidb-lightning-checkpoints.md)を参照してください。

### ターゲットスキーマを作成する {#create-a-target-schema}

ターゲットで`mydb.table5`を作成します。

```sql
CREATE TABLE `table5` (
  `id` bigint NOT NULL,
  `sid` bigint NOT NULL,
  `pid` bigint NOT NULL,
  `comment` varchar(255) DEFAULT NULL,
  INDEX (`id`),
  UNIQUE KEY `sid` (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

### 移行タスクを開始します {#start-the-migration-task}

`tidb-lightning`を開始するには、以下の手順に従ってください。

1. toml ファイルを編集します。次の例では`tidb-lightning.toml`が使用されています。

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
    host = "${host}"           # For example: "172.16.31.1"
    port = "${port}"           # For example: 4000
    user = "${user_name}"    # For example: "root"
    password = "${password}" # For example: "rootroot"
    status-port = "${status-port}" # The table information is read from the status port. For example: 10080
    # the IP address of the PD cluster. TiDB Lightning gets some information through the PD cluster.
    # For example: "172.16.31.3:2379".
    # When backend = "local", make sure that the values of status-port and pd-addr are correct. Otherwise an error will occur.
    pd-addr = "${ip}:${port}"
    ```

2. `tidb-lightning`を実行します。シェルでプログラム名を直接呼び出してプログラムを実行すると、SIGHUP シグナルを受信した後にプロセスが予期せず終了する可能性があります。 `nohup` 、 `screen` 、 `tiup`などのツールを使用してプログラムを実行し、プロセスをシェルのバックグラウンドで実行することをお勧めします。S3 から移行する場合は、Amazon S3 バックエンド ストアにアクセスできるアカウントの SecretKey と AccessKey を環境変数として Lightning ノードに渡す必要があります。 `~/.aws/credentials`からの認証情報ファイルの読み取りもサポートされています。例:

    ```shell
    export AWS_ACCESS_KEY_ID=${access_key}
    export AWS_SECRET_ACCESS_KEY=${secret_key}
    nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out 2>&1 &
    ```

3. 移行タスクを開始した後、以下のいずれかの方法で進捗状況を確認できます。

    - `grep`ツールを使用して、ログファイル内でキーワード`progress`を検索してください。デフォルトでは、進行状況を報告するメッセージが5分ごとにログファイルに書き込まれます。
    - 監視ダッシュボードから進捗状況を確認します。詳細については、 [TiDB Lightningモニタリング](/tidb-lightning/monitor-tidb-lightning.md)を参照してください。

TiDB Lightning はインポートが完了すると自動的に終了します。`tidb-lightning.log`の最後の行に`the whole procedure completed`が含まれているかどうかを確認してください。含まれている場合はインポートが成功しています。含まれていない場合は、インポート中にエラーが発生しました。エラーメッセージの指示に従ってエラーに対処してください。

> **Note:**
>
> 移行が成功したかどうかに関わらず、ログの最後の行は必ず`tidb lightning exit`となります。これは単にTiDB Lightning が正常に終了したことを意味するだけで、インポートタスクが正常に完了したことを保証するものではありません。

移行中に問題が発生した場合は、 [TiDB Lightningよくある質問](/tidb-lightning/tidb-lightning-faq.md)を参照してください。

## ステップ3.（オプション）DMを使用して増分レプリケーションを実行します。 {#step-3-optional-use-dm-to-perform-incremental-replication}

ソースデータベース内の指定された位置のbinlogに基づいてデータ変更をTiDBにレプリケートするには、TiDB DMを使用して増分レプリケーションを実行できます。

### データソースを追加する {#add-the-data-source}

`source1.yaml`という名前の新しいデータソースファイルを作成し、DMに上流データソースを設定します。そして、以下の内容を追加します。

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

ターミナルで次のコマンドを実行します。 `tiup dmctl`を使用して、データソース構成をDMクラスタにロードします。

```shell
tiup dmctl --master-addr ${advertise-addr} operate-source create source1.yaml
```

パラメータは以下のように説明されます。

| パラメータ                   | 説明                                                                |
| ----------------------- | ----------------------------------------------------------------- |
| `--master-addr`         | dmctlが接続するクラスタ内の任意のDMマスターノードの{advertise-addr}。例：172.16.10.71:8261 |
| `operate-source create` | データソースをDMクラスターにロードします。                                            |

上記の手順を繰り返して、すべてのMySQL上流インスタンスをデータソースとしてDMに追加します。

### レプリケーションタスクを作成する {#create-a-replication-task}

`task.yaml`という名前のタスク構成ファイルを編集して、各データソースの増分レプリケーションモードとレプリケーション開始点を設定します。

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

その他の構成については、 [DM 高度タスクコンフィグレーションファイル](/dm/task-configuration-file-full.md)を参照してください。

データ移行タスクを開始する前に、 `check-task`の`tiup dmctl`サブコマンドを使用して、構成が DM 構成要件を満たしているかどうかを確認することをお勧めします。

```shell
tiup dmctl --master-addr ${advertise-addr} check-task task.yaml
```

`tiup dmctl`を使用して、次のコマンドを実行し、データ移行タスクを開始します。

```shell
tiup dmctl --master-addr ${advertise-addr} start-task task.yaml
```

このコマンドのパラメータは、以下のように説明されます。

| パラメータ      | 説明                                                                |
| ---------- | ----------------------------------------------------------------- |
| --master-addr | dmctlが接続するクラスタ内の任意のDMマスターノードの{advertise-addr}。例：172.16.10.71:8261 |
| タスクの開始     | データ移行タスクを開始します。                                                   |

タスクの開始に失敗した場合は、返された結果のプロンプト メッセージに従って構成を変更し、次に`start-task task.yaml`の`tiup dmctl`サブコマンドを実行してタスクを再開します。問題が発生した場合は、[エラーを処理する](/dm/dm-error-handling.md)および[TiDB Data Migrationに関するFAQ](/dm/dm-faq.md)を参照してください。

### 移行状況を確認する {#check-the-migration-status}

`tiup dmctl`で`query-status`コマンドを実行すると、DM クラスターで実行中の移行タスクとそのステータスを確認できます。

```shell
tiup dmctl --master-addr ${advertise-addr} query-status ${task-name}
```

詳細については、[クエリステータス](/dm/dm-query-status.md)を参照してください。

### タスクを監視し、ログを表示する {#monitor-tasks-and-view-logs}

移行タスクの履歴や内部運用指標は、Grafanaまたはログを通じて確認できます。

- Grafana経由

    TiUPを使用してDMクラスタをデプロイする際に、Prometheus、Alertmanager、およびGrafanaが正しくデプロイされていれば、GrafanaでDMの監視メトリクスを表示できます。具体的には、デプロイ時に指定したIPアドレスとポートをGrafanaに入力し、DMダッシュボードを選択してください。

- ログ経由

    DMが実行されている場合、DM-master、DM-worker、およびdmctlは、移行タスクに関する情報を含むログを出力します。各コンポーネントのログディレクトリは以下のとおりです。

    - DM-master ログディレクトリ: これは、DM-master コマンドラインパラメータ`--log-file`で指定されます。DM がTiUPを使用してデプロイされている場合、ログディレクトリは`/dm-deploy/dm-master-8261/log/`です。
    - DM-worker のログディレクトリ: これは、DM-worker コマンドラインパラメータ`--log-file`で指定されます。DM がTiUPを使用してデプロイされている場合、ログディレクトリは`/dm-deploy/dm-worker-8262/log/`です。

## 関連項目 {#see-also}

- [Dumpling](/dumpling-overview.md)
- [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)
- [悲観的モードと楽観的モード](/dm/feature-shard-merge.md)
- [データ移行タスクを一時停止する](/dm/dm-pause-task.md)
- [データ移行タスクを再開する](/dm/dm-resume-task.md)
- [データ移行タスクを停止する](/dm/dm-stop-task.md)
- [クラスターのデータソースのエクスポートとインポート、およびタスクコンフィグレーション](/dm/dm-export-import-config.md)
- [失敗したDDL文を処理する](/dm/handle-failed-ddl-statements.md)
- [エラーを処理する](/dm/dm-error-handling.md)
