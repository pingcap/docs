---
title: Use BR to Back Up Cluster Data
summary: Learn how to back up data using BR commands
---

# BR を使用してクラスタデータをバックアップする {#use-br-to-back-up-cluster-data}

このドキュメントでは、次のシナリオで TiDB クラスター データをバックアップする方法について説明します。

-   [TiDB クラスターのスナップショットをバックアップする](#back-up-tidb-cluster-snapshots)
-   [データベースのバックアップ](#back-up-a-database)
-   [テーブルをバックアップする](#back-up-a-table)
-   [テーブル フィルターを使用して複数のテーブルをバックアップする](#back-up-multiple-tables-with-table-filter)
-   [データを外部ストレージにバックアップする](#back-up-data-to-external-storage)
-   [増分データのバックアップ](#back-up-incremental-data)
-   [バックアップ データの暗号化](#encrypt-backup-data)

バックアップ ツールと復元ツールに慣れていない場合は、次のドキュメントを読んで、これらのツールの使用原理と方法を完全に理解することをお勧めします。

-   [BRの概要](/br/backup-and-restore-overview.md)
-   [バックアップと復元に BR コマンドラインを使用する](/br/use-br-command-line-tool.md)

少量のデータ (たとえば、50 GB 未満) をバックアップする必要があり、高速なバックアップ速度を必要としない場合は、Dumplingを使用してデータをエクスポートし、バックアップを実装できます。詳細なバックアップ操作については、 [Dumplingを使用して完全なデータをバックアップする](/backup-and-restore-using-dumpling-lightning.md#use-dumpling-to-back-up-full-data)を参照してください。

## TiDB クラスターのスナップショットをバックアップする {#back-up-tidb-cluster-snapshots}

TiDB クラスターのスナップショットには、特定の時点における最新でトランザクション的に一貫性のあるデータのみが含まれます。 `br backup full`コマンドを実行して、TiDB クラスターの最新または指定したスナップショット データをバックアップできます。このコマンドのヘルプを表示するには、 `br backup full --help`コマンドを実行します。

例: `2022-01-30 07:42:23`で生成されたスナップショットを Amazon S3 の`backup-data`バケットの`2022-01-30/`ディレクトリにバックアップします。

{{< copyable "" >}}

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --backupts '2022-01-30 07:42:23' \
    --storage "s3://backup-data/2022-01-30/" \
    --ratelimit 128 \
    --log-file backupfull.log
```

前述のコマンドでは:

-   `--backupts` : スナップショットの物理時間。このスナップショットのデータがガベージ コレクション (GC) によって処理される場合、 `br backup`コマンドはエラーで終了します。このパラメーターを指定しない場合、BR はバックアップの開始時刻に対応するスナップショットを選択します。
-   `--ratelimit` : バックアップ タスクを実行する**TiKV ごと**の最大速度 (MiB/秒)。
-   `--log-file` : BR ロギングの対象ファイル。

バックアップ中は、以下に示すように、進行状況バーがターミナルに表示されます。プログレス バーが 100% まで進むと、バックアップは完了です。

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --storage "s3://backup-data/2022-01-30/" \
    --ratelimit 128 \
    --log-file backupfull.log
Full Backup <---------/................................................> 17.12%.
```

バックアップが完了すると、BR はバックアップ データのチェックサムとクラスタのチェックサムを比較して、データの正確性とセキュリティを確保し[管理者チェックサム テーブル](/sql-statements/sql-statement-admin-checksum-table.md) 。

## データベースまたはテーブルのバックアップ {#back-up-a-database-or-a-table}

BR は、クラスター スナップショットまたは増分データ バックアップから、指定されたデータベースまたはテーブルの部分的なデータのバックアップをサポートします。この機能を使用すると、スナップショット バックアップと増分データ バックアップから不要なデータを除外し、ビジネス クリティカルなデータのみをバックアップできます。

### データベースのバックアップ {#back-up-a-database}

クラスター内のデータベースをバックアップするには、 `br backup db`コマンドを実行します。このコマンドのヘルプを表示するには、 `br backup db --help`コマンドを実行します。

例: `test`データベースを Amazon S3 の`backup-data`バケットの`db-test/2022-01-30/`ディレクトリにバックアップします。

{{< copyable "" >}}

```shell
br backup db \
    --pd "${PDIP}:2379" \
    --db test \
    --storage "s3://backup-data/db-test/2022-01-30/" \
    --ratelimit 128 \
    --log-file backuptable.log
```

上記のコマンドで、 `--db`はデータベース名を指定し、他のパラメーターは[TiDB クラスターのスナップショットをバックアップする](#back-up-tidb-cluster-snapshots)と同じです。

### テーブルをバックアップする {#back-up-a-table}

クラスター内のテーブルをバックアップするには、 `br backup table`コマンドを実行します。このコマンドのヘルプを表示するには、 `br backup table --help`コマンドを実行します。

例: Amazon S3 の`backup-data`バケットの`table-db-usertable/2022-01-30/`ディレクトリに`test.usertable`をバックアップします。

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

上記のコマンドで、 `--db`と`--table`はそれぞれデータベース名とテーブル名を指定し、その他のパラメーターは[TiDB クラスターのスナップショットをバックアップする](#back-up-tidb-cluster-snapshots)と同じです。

### テーブル フィルターを使用して複数のテーブルをバックアップする {#back-up-multiple-tables-with-table-filter}

複数の基準で複数のテーブルをバックアップするには、 `br backup full`コマンドを実行し、 `--filter`または`-f`で[テーブル フィルター](/table-filter.md)を指定します。

例: テーブルの`db*.tbl*`データを Amazon S3 の`backup-data`バケットの`table-filter/2022-01-30/`ディレクトリにバックアップします。

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

BR は、Amazon S3、Google Cloud Storage (GCS)、Azure Blob Storage、NFS、またはその他の S3 互換ファイル ストレージ サービスへのデータのバックアップをサポートしています。詳細については、次のドキュメントを参照してください。

-   [BR を使用して Amazon S3 のデータをバックアップする](/br/backup-storage-S3.md)
-   [BR を使用して Google Cloud Storage にデータをバックアップする](/br/backup-storage-gcs.md)
-   [BR を使用して Azure Blob Storage 上のデータをバックアップする](/br/backup-storage-azblob.md)

## 増分データのバックアップ {#back-up-incremental-data}

> **警告：**
>
> これはまだ実験的機能です。本番環境で使用することはお勧めし**ません**。

TiDB クラスターの増分データは、開始点のスナップショットと終了点のスナップショットの差分データです。増分データは、スナップショット データと比較してサイズが小さいため、スナップショット バックアップを補完するものであり、バックアップ データの量を削減します。

増分データをバックアップするに**は、最後のバックアップ タイムスタンプ**`--lastbackupts`を指定して`br backup`コマンドを実行します。 `--lastbackupts`を取得するには、 `validate`コマンドを実行します。次に例を示します。

{{< copyable "" >}}

```shell
LAST_BACKUP_TS=`br validate decode --field="end-version" -s s3://backup-data/2022-01-30/ | tail -n1`
```

> **ノート：**
>
> -   増分バックアップ データは、以前のスナップショット バックアップとは別のパスに保存する必要があります。
> -   GC セーフポイントは`lastbackupts`より前でなければなりません。デフォルトの GC ライフタイムは TiDB で 10 分です。つまり、TiDB は過去 10 分間に生成された増分データのみをバックアップします。以前の増分データをバックアップするには、 [TiDB GC ライフタイム設定を調整する](/system-variables.md#tidb_gc_life_time-new-in-v50)を行う必要があります。

{{< copyable "" >}}

```shell
br backup full\
    --pd ${PDIP}:2379 \
    --ratelimit 128 \
    --storage "s3://backup-data/2022-01-30/incr" \
    --lastbackupts ${LAST_BACKUP_TS}
```

上記のコマンドは、 `(LAST_BACKUP_TS, current PD timestamp]`からこの期間中に生成された DDL までの増分データをバックアップします。増分データを復元する場合、BR は最初にすべての DDL を復元し、次にデータを復元します。

## バックアップ データの暗号化 {#encrypt-backup-data}

> **警告：**
>
> これはまだ実験的機能です。本番環境で使用することはお勧めし**ません**。

BR は、Amazon S3 へのバックアップ時に、バックアップ側とストレージ側でバックアップ データの暗号化をサポートします。必要に応じて、いずれかの暗号化方法を選択できます。

### バックアップ終了時にバックアップ データを暗号化する {#encrypt-backup-data-at-the-backup-end}

TiDB v5.3.0 以降、次のパラメータを設定することでバックアップ データを暗号化できます。

-   `--crypter.method` : 暗号化アルゴリズム。 `aes128-ctr` 、 `aes192-ctr` 、または`aes256-ctr`のいずれかです。デフォルト値は`plaintext`で、データが暗号化されていないことを示します。
-   `--crypter.key` : 16 進文字列形式の暗号化キー。これは、アルゴリズム 2 では 128 ビット (16 バイト) の鍵、アルゴリズム`aes128-ctr`では 24 バイトの鍵、アルゴリズム`aes192-ctr`では`aes256-ctr`バイトの鍵です。
-   `--crypter.key-file` : 鍵ファイル。 「crypter.key」を渡さずに、キーが格納されているファイル パスをパラメータとして直接渡すことができます。

例: バックアップの最後にバックアップ データを暗号化します。

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
> -   キーを紛失すると、バックアップ データをクラスタに復元できなくなります。
> -   暗号化機能は、BR ツールおよび TiDB クラスター v5.3.0 以降のバージョンで使用する必要があります。暗号化されたバックアップ データは、v5.3.0 より前のクラスターでは復元できません。

### Amazon S3 へのバックアップ時にバックアップ データを暗号化する {#encrypt-backup-data-when-backing-up-to-amazon-s3}

BR は、データを S3 にバックアップするときにサーバー側の暗号化 (SSE) をサポートします。このシナリオでは、作成した AWS KMS キーを使用してデータを暗号化できます。詳細については、 [BR S3 サーバー側の暗号化](/encryption-at-rest.md#br-s3-server-side-encryption)を参照してください。

## バックアップのパフォーマンスと影響 {#backup-performance-and-impact}

バックアップ機能は、クラスターのパフォーマンス (トランザクションのレイテンシーと QPS) に影響を与えます。ただし、バックアップ スレッド[`backup.num-threads`](/tikv-configuration-file.md#num-threads-1)の数を調整するか、クラスターを追加することで、影響を軽減できます。

バックアップの影響を説明するために、このドキュメントではいくつかのスナップショット バックアップ テストの結果を示します。

-   (5.3.0 以前) TiKV ノード上の BR のバックアップ スレッドがノードの合計 CPU の 75% を占める場合、QPS は元の QPS の 30% 減少します。
-   (5.4.0 以降) TiKV ノードに BR のスレッドが`8`しかなく、クラスターの合計 CPU 使用率が 80% を超えない場合、クラスターに対する BR タスク (書き込みおよび読み取り) の影響は 20% です。多くの。
-   (5.4.0 以降) TiKV ノードに BR のスレッドが`8`しかなく、クラスターの合計 CPU 使用率が 75% を超えない場合、クラスターに対する BR タスク (書き込みおよび読み取り) の影響は 10% です。多くの。
-   (5.4.0 以降) TiKV ノードに BR のスレッドが`8`しかなく、クラスターの合計 CPU 使用率が 60% を超えない場合、BR タスクはクラスター (書き込みと読み取り) にほとんど影響を与えません。

バックアップ スレッドの数を減らすことで、クラスターのパフォーマンスへの影響を軽減できます。ただし、これによりバックアップのパフォーマンスが低下する可能性があります。前述のテスト結果に基づくと、(単一の TiKV ノードで) バックアップ速度はバックアップ スレッドの数に比例します。スレッド数が少ない場合、バックアップ速度は約 20MB/スレッドです。たとえば、5 つのバックアップ スレッドを持つ単一ノードは、100 MB/秒のバックアップ速度を実現できます。

> **ノート：**
>
> バックアップの影響と速度は、クラスタ構成、展開、および実行中のサービスに大きく依存します。多くのシナリオでのシミュレーション テストに基づき、一部の顧客サイトで検証された前述のテストの結論は、参照に値します。ただし、正確な影響とパフォーマンスの上限は、シナリオによって異なる場合があります。したがって、常にテストを実行し、テスト結果を確認する必要があります。

v5.3.0 以降、BR は自動チューニング機能 (デフォルトで有効) を導入して、バックアップ スレッドの数を調整します。バックアップ タスク中にクラスターの CPU 使用率を 80% 未満に維持できます。詳細については、 [BR オートチューン](/br/br-auto-tune.md)を参照してください。
