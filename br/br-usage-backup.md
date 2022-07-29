---
title: Use BR to Back Up Cluster Data
summary: Learn how to back up data using BR commands
---

# BRを使用してクラスターデータをバックアップする {#use-br-to-back-up-cluster-data}

このドキュメントでは、次のシナリオでBRを使用してクラスタデータをバックアップする方法について説明します。

-   [TiDBクラスタスナップショットをバックアップします](#back-up-tidb-cluster-snapshots)
-   [データベースをバックアップする](#back-up-a-database)
-   [テーブルをバックアップする](#back-up-a-table)
-   [テーブルフィルターを使用して複数のテーブルをバックアップする](#back-up-multiple-tables-with-table-filter)
-   [データを外部ストレージにバックアップする](#back-up-data-to-external-storage)
-   [インクリメンタルデータをバックアップする](#back-up-incremental-data)
-   [バックアップデータを暗号化する](#encrypt-backup-data)

バックアップと復元（BR）に慣れていない場合は、次のドキュメントを読んで、BRの使用原則と方法を完全に理解することをお勧めします。

-   [BRの概要](/br/backup-and-restore-overview.md)
-   [バックアップと復元にBRコマンドラインを使用する](/br/use-br-command-line-tool.md)

## TiDBクラスタスナップショットをバックアップします {#back-up-tidb-cluster-snapshots}

TiDBクラスタのスナップショットには、特定の時点での最新のトランザクション整合性のあるデータのみが含まれます。 `br backup full`コマンドを実行すると、TiDBクラスタの最新または指定されたスナップショットデータをバックアップできます。このコマンドのヘルプを表示するには、 `br backup full --help`コマンドを実行します。

例： `2022-01-30 07:42:23`で生成されたスナップショットをAmazonS3の`backup-data`バケットの`2022-01-30/`ディレクトリにバックアップします。

{{< copyable "" >}}

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --backupts '2022-01-30 07:42:23' \
    --storage "s3://backup-data/2022-01-30/" \
    --ratelimit 128 \
    --log-file backupfull.log
```

前のコマンドの場合：

-   `--backupts` ：スナップショットの物理時間。このスナップショットのデータがガベージコレクション（GC）によって処理される場合、 `br backup`コマンドはエラーで終了します。このパラメーターを指定しないままにすると、BRはバックアップの開始時刻に対応するスナップショットを選択します。
-   `--ratelimit` ：バックアップタスクを実行する**TiKVあたり**の最大速度（MiB /秒）。
-   `--log-file` ：BRロギングのターゲットファイル。

バックアップ中は、以下のように端末にプログレスバーが表示されます。プログレスバーが100％に進むと、バックアップが完了します。

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --storage "s3://backup-data/2022-01-30/" \
    --ratelimit 128 \
    --log-file backupfull.log
Full Backup <---------/................................................> 17.12%.
```

バックアップが完了すると、BRはバックアップデータのチェックサムをクラスタの[管理チェックサムテーブル](/sql-statements/sql-statement-admin-checksum-table.md)と比較して、データの正確性とセキュリティを確保します。

## データベースまたはテーブルをバックアップします {#back-up-a-database-or-a-table}

BRは、クラスタスナップショットまたは増分データバックアップからの指定されたデータベースまたはテーブルの部分データのバックアップをサポートします。この機能を使用すると、スナップショットバックアップと増分データバックアップから不要なデータを除外し、ビジネスクリティカルなデータのみをバックアップできます。

### データベースをバックアップする {#back-up-a-database}

クラスタのデータベースをバックアップするには、 `br backup db`コマンドを実行します。このコマンドのヘルプを表示するには、 `br backup db --help`コマンドを実行します。

例： `test`のデータベースをAmazonS3の`backup-data`バケットの`db-test/2022-01-30/`ディレクトリにバックアップします。

{{< copyable "" >}}

```shell
br backup db \
    --pd "${PDIP}:2379" \
    --db test \
    --storage "s3://backup-data/db-test/2022-01-30/" \
    --ratelimit 128 \
    --log-file backuptable.log
```

上記のコマンドで、 `--db`はデータベース名を指定し、その他のパラメーターは[TiDBクラスタスナップショットをバックアップします](#back-up-tidb-cluster-snapshots)と同じです。

### テーブルをバックアップする {#back-up-a-table}

クラスタのテーブルをバックアップするには、 `br backup table`コマンドを実行します。このコマンドのヘルプを表示するには、 `br backup table --help`コマンドを実行します。

例：AmazonS3の`backup-data`バケットの`table-db-usertable/2022-01-30/`ディレクトリに`test.usertable`をバックアップします。

{{< copyable "" >}}

```shell
br backup table \
    --pd "${PDIP}:2379" \
    --db test \
    --table usertable \
    --storage "s3://backup-data/table-db-usertable/2022-01-30/" \
    --ratelimit 128 \
    --log-file backuptable.log
```

上記のコマンドで、 `--db`と`--table`はそれぞれデータベース名とテーブル名を指定し、その他のパラメーターは[TiDBクラスタスナップショットをバックアップします](#back-up-tidb-cluster-snapshots)と同じです。

### テーブルフィルターを使用して複数のテーブルをバックアップする {#back-up-multiple-tables-with-table-filter}

より多くの基準で複数のテーブルをバックアップするには、 `br backup full`コマンドを実行し、 `--filter`または`-f`で[テーブルフィルター](/table-filter.md)を指定します。

例：テーブルの`db*.tbl*`のデータをAmazonS3の`backup-data`バケットの`table-filter/2022-01-30/`ディレクトリにバックアップします。

{{< copyable "" >}}

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --filter 'db*.tbl*' \
    --storage "s3://backup-data/table-filter/2022-01-30/" \
    --ratelimit 128 \
    --log-file backupfull.log
```

## データを外部ストレージにバックアップする {#back-up-data-to-external-storage}

BRは、Amazon S3、Google Cloud Storage（GCS）、Azure Blob Storage、NFS、またはその他のS3互換のファイルストレージサービスへのデータのバックアップをサポートしています。詳細については、次のドキュメントを参照してください。

-   [BRを使用してAmazonS3のデータをバックアップする](/br/backup-storage-S3.md)
-   [BRを使用してGoogleCloudStorageにデータをバックアップする](/br/backup-storage-gcs.md)
-   [BRを使用してAzureBlobStorageのデータをバックアップする](/br/backup-storage-azblob.md)

## インクリメンタルデータをバックアップする {#back-up-incremental-data}

> **警告：**
>
> これはまだ実験的機能です。実稼働環境で使用することはお勧めし**ません**。

TiDBクラスタの増分データは、開始点のスナップショットと終了点のスナップショットの間で区別されるデータです。スナップショットデータと比較して、増分データは小さいため、スナップショットバックアップを補足し、バックアップデータの量を減らします。

インクリメンタルデータをバックアップするに**は、最後のバックアップタイムスタンプ**`--lastbackupts`を指定して`br backup`コマンドを実行します。 `--lastbackupts`を取得するには、 `validate`コマンドを実行します。次に例を示します。

{{< copyable "" >}}

```shell
LAST_BACKUP_TS=`br validate decode --field="end-version" -s s3://backup-data/2022-01-30/ | tail -n1`
```

> **ノート：**
>
> -   以前のスナップショットバックアップとは異なるパスで増分バックアップデータを保存する必要があります。
> -   GCセーフポイントは`lastbackupts`より前である必要があります。 TiDBではデフォルトのGCライフタイムは10分です。つまり、TiDBは過去10分間に生成された増分データのみをバックアップします。以前の増分データをバックアップするには、 [TiDBGCライフタイム設定を調整します](/system-variables.md#tidb_gc_life_time-new-in-v50)にする必要があります。

{{< copyable "" >}}

```shell
br backup full\
    --pd ${PDIP}:2379 \
    --ratelimit 128 \
    --storage "s3://backup-data/2022-01-30/incr" \
    --lastbackupts ${LAST_BACKUP_TS}
```

上記のコマンドは、 `(LAST_BACKUP_TS, current PD timestamp]`とこの期間中に生成されたDDLの間の増分データをバックアップします。インクリメンタルデータを復元する場合、BRは最初にすべてのDDLを復元し、次にデータを復元します。

## バックアップデータを暗号化する {#encrypt-backup-data}

> **警告：**
>
> これはまだ実験的機能です。実稼働環境で使用することはお勧めし**ません**。

BRは、Amazon S3にバックアップするときに、バックアップ側とストレージ側でバックアップデータの暗号化をサポートします。必要に応じて、どちらの暗号化方法も選択できます。

### バックアップ側でバックアップデータを暗号化する {#encrypt-backup-data-at-the-backup-end}

TiDB v5.3.0以降、次のパラメーターを構成することにより、バックアップデータを暗号化できます。

-   `--crypter.method` ：暗号化アルゴリズム`aes128-ctr` 、または`aes192-ctr`のいずれか`aes256-ctr` 。デフォルト値は`plaintext`で、データが暗号化されていないことを示します。
-   `--crypter.key`進文字列形式の暗号化キー。これは、アルゴリズム`aes128-ctr`の場合は128ビット（16バイト）のキー、アルゴリズム`aes192-ctr`の場合は24バイトのキー、アルゴリズム`aes256-ctr`の場合は32バイトのキーです。
-   `--crypter.key-file` ：キーファイル。 「crypter.key」を渡さなくても、キーがパラメータとして保存されているファイルパスを直接渡すことができます。

例：バックアップ側でバックアップデータを暗号化します。

{{< copyable "" >}}

```shell
br backup full\
    --pd ${PDIP}:2379 \
    --storage "s3://backup-data/2022-01-30/"  \
    --crypter.method aes128-ctr \
    --crypter.key 0123456789abcdef0123456789abcdef
```

> **ノート：**
>
> -   キーを紛失した場合、バックアップデータをクラスタに復元することはできません。
> -   暗号化機能は、BRツールおよびTiDBクラスターv5.3.0以降のバージョンで使用する必要があります。暗号化されたバックアップデータは、v5.3.0より前のクラスターでは復元できません。

### AmazonS3にバックアップするときにバックアップデータを暗号化する {#encrypt-backup-data-when-backing-up-to-amazon-s3}

BRは、データをS3にバックアップするときに、サーバー側の暗号化（SSE）をサポートします。このシナリオでは、作成したAWSKMSキーを使用してデータを暗号化できます。詳細については、 [BRS3サーバー側の暗号化](/encryption-at-rest.md#br-s3-server-side-encryption)を参照してください。

## バックアップのパフォーマンスと影響 {#backup-performance-and-impact}

バックアップ機能は、クラスタのパフォーマンス（トランザクションの待ち時間とQPS）にいくらかの影響を及ぼします。ただし、バックアップスレッド[`backup.num-threads`](/tikv-configuration-file.md#num-threads-1)の数を調整するか、クラスターを追加することで、影響を軽減できます。

バックアップの影響を説明するために、このドキュメントでは、いくつかのスナップショットバックアップテストのテスト結果を示します。

-   （5.3.0以前）TiKVノード上のBRのバックアップスレッドがノードの合計CPUの75％を占める場合、QPSは元のQPSの30％減少します。
-   （5.4.0以降）TiKVノードにBRのスレッドが`8`つ以下で、クラスターの合計CPU使用率が80％を超えない場合、クラスタ（書き込みおよび読み取り）に対するBRタスクの影響は次の場合に20％です。多くの。
-   （5.4.0以降）TiKVノードにBRのスレッドが`8`つ以下で、クラスターの合計CPU使用率が75％を超えない場合、クラスタ（書き込みおよび読み取り）に対するBRタスクの影響は10％です。多くの。
-   （5.4.0以降）TiKVノードにBRのスレッドが`8`つ以下で、クラスターの合計CPU使用率が60％を超えない場合、BRタスクはクラスタ（書き込みと読み取り）にほとんど影響を与えません。

バックアップスレッドの数を減らすことで、クラスタのパフォーマンスへの影響を軽減できます。ただし、これによりバックアップのパフォーマンスが低下する可能性があります。前述のテスト結果に基づく:(単一のTiKVノードの場合）バックアップ速度はバックアップスレッドの数に比例します。スレッド数が少ない場合、バックアップ速度は約20MB/スレッドです。たとえば、5つのバックアップスレッドを持つ単一ノードは、100MB/秒のバックアップ速度を提供できます。

> **ノート：**
>
> バックアップの影響と速度は、cluserの構成、展開、および実行中のサービスに大きく依存します。多くのシナリオでのシミュレーションテストに基づいており、一部の顧客サイトで検証された前述のテストの結論は、参照する価値があります。ただし、正確な影響とパフォーマンスの上限は、シナリオによって異なる場合があります。したがって、常にテストを実行し、テスト結果を確認する必要があります。

v5.3.0以降、BRは、バックアップスレッドの数を調整するための自動調整機能（デフォルトで有効）を導入しています。バックアップタスク中にクラスタのCPU使用率を80％未満に維持できます。詳細については、 [BRオートチューン](/br/br-auto-tune.md)を参照してください。
