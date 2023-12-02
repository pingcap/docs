---
title: Snapshot Backup and Restore Guide
summary: Learn about how to back up and restore TiDB snapshots using the br command-line tool.
---

# スナップショットのバックアップと復元ガイド {#snapshot-backup-and-restore-guide}

このドキュメントでは、br コマンドライン ツール (以下`br`と呼びます) を使用して TiDB スナップショットをバックアップおよび復元する方法について説明します。データをバックアップおよび復元する前に、まず[br コマンドライン ツールをインストールする](/br/br-use-overview.md#deploy-and-use-br)を行う必要があります。

スナップショット バックアップは、クラスター全体をバックアップする実装です。これは[マルチバージョン同時実行制御 (MVCC)](/tidb-storage.md#mvcc)に基づいており、指定されたスナップショット内のすべてのデータをターゲットstorageにバックアップします。バックアップ データのサイズは、クラスター内の圧縮された単一レプリカのサイズとほぼ同じです。バックアップが完了したら、バックアップ データを空のクラスター、または競合データを含まないクラスター (同じスキーマまたは同じテーブルを持つ) に復元したり、クラスターをスナップショット バックアップの時点に復元したり、複数のクラスターを復元したりできます。クラスターレプリカ設定に従ってレプリカを作成します。

基本的なバックアップと復元に加えて、スナップショット バックアップと復元では次の機能も提供します。

-   [指定した時点のデータをバックアップする](#back-up-cluster-snapshots)
-   [指定したデータベースまたはテーブルのデータを復元します](#restore-a-database-or-a-table)

## クラスターのスナップショットをバックアップする {#back-up-cluster-snapshots}

> **注記：**
>
> -   次の例では、Amazon S3 アクセス キーと秘密キーがアクセス許可の承認に使用されることを前提としています。 IAMロールを使用して権限を承認する場合は、 `--send-credentials-to-tikv` ～ `false`を設定する必要があります。
> -   他のstorageシステムまたは認証方法を使用して権限を認証する場合は、 [バックアップストレージ](/br/backup-and-restore-storages.md)に従ってパラメータ設定を調整します。

`br backup full`コマンドを実行すると、TiDB クラスターのスナップショットをバックアップできます。 `br backup full --help`を実行してヘルプ情報を表示します。

```shell
tiup br backup full --pd "${PD_IP}:2379" \
    --backupts '2022-09-08 13:30:00' \
    --storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --ratelimit 128 \
```

前述のコマンドでは次のようになります。

-   `--backupts` : スナップショットの時点。形式は[TSO](/glossary.md#tso)またはタイムスタンプ ( `400036290571534337`や`2018-05-11 01:42:23`など) です。このスナップショットのデータがガベージ コレクションされた場合、 `br backup`コマンドはエラーを返し、 `br`は終了します。このパラメータを指定しないままにすると、 `br`バックアップ開始時刻に対応するスナップショットを選択します。
-   `--storage` : バックアップデータのstorageアドレス。スナップショット バックアップは、バックアップstorageとして Amazon S3、Google Cloud Storage、および Azure Blob Storage をサポートします。前述のコマンドでは、例として Amazon S3 を使用しています。詳細については、 [外部ストレージ サービスの URI 形式](/external-storage-uri.md)を参照してください。
-   `--ratelimit` : バックアップ タスクを実行する**TiKV ごとの**最大速度。単位は MiB/s です。

バックアップ中、以下に示すように進行状況バーがターミナルに表示されます。進行状況バーが 100% まで進むと、バックアップ タスクが完了し、合計バックアップ時間、平均バックアップ速度、バックアップ データ サイズなどの統計が表示されます。

```shell
Full Backup <-------------------------------------------------------------------------------> 100.00%
Checksum <----------------------------------------------------------------------------------> 100.00%
*** ["Full Backup success summary"] *** [backup-checksum=3.597416ms] [backup-fast-checksum=2.36975ms] *** [total-take=4.715509333s] [BackupTS=435844546560000000] [total-kv=1131] [total-kv-size=250kB] [average-speed=53.02kB/s] [backup-data-size(after-compressed)=71.33kB] [Size=71330]
```

## スナップショットバックアップのバックアップ時点を取得する {#get-the-backup-time-point-of-a-snapshot-backup}

大量のバックアップを管理するために、スナップショット バックアップの物理時間を取得する必要がある場合は、次のコマンドを実行できます。

```shell
tiup br validate decode --field="end-version" \
--storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}" | tail -n1
```

出力は次のとおりであり、物理時間`2022-09-08 13:30:00 +0800 CST`に対応します。

    435844546560000000

## クラスターのスナップショットを復元する {#restore-cluster-snapshots}

`br restore full`コマンドを実行すると、スナップショット バックアップを復元できます。 `br restore full --help`を実行してヘルプ情報を表示します。

次の例では、 [以前のバックアップ スナップショット](#back-up-cluster-snapshots)をターゲット クラスターに復元します。

```shell
tiup br restore full --pd "${PD_IP}:2379" \
--storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

復元中、以下に示すように進行状況バーがターミナルに表示されます。進行状況バーが 100% まで進むと、復元タスクが完了し、合計復元時間、平均復元速度、合計データ サイズなどの統計が表示されます。

```shell
Full Restore <------------------------------------------------------------------------------> 100.00%
*** ["Full Restore success summary"] *** [total-take=4.344617542s] [total-kv=5] [total-kv-size=327B] [average-speed=75.27B/s] [restore-data-size(after-compressed)=4.813kB] [Size=4813] [BackupTS=435844901803917314]
```

### データベースまたはテーブルを復元する {#restore-a-database-or-a-table}

BR は、バックアップ データから指定したデータベースまたはテーブルの部分データを復元することをサポートします。この機能を使用すると、不要なデータをフィルタリングして除外し、特定のデータベースまたはテーブルのみをバックアップできます。

**データベースを復元する**

データベースをクラスターに復元するには、 `br restore db`コマンドを実行します。次の例では、バックアップ データからターゲット クラスターに`test`データベースを復元します。

```shell
tiup br restore db \
--pd "${PD_IP}:2379" \
--db "test" \
--storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

前述のコマンドでは、リストアするデータベースの名前を`--db`に指定します。

**テーブルを復元する**

単一のテーブルをクラスターに復元するには、 `br restore table`コマンドを実行します。次の例では、バックアップ データからターゲット クラスターに`test.usertable`テーブルを復元します。

```shell
tiup br restore table --pd "${PD_IP}:2379" \
--db "test" \
--table "usertable" \
--storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

前述のコマンドでは、 `--db`復元するデータベースの名前を指定し、 `--table`は復元するテーブルの名前を指定します。

**テーブルフィルターを使用して複数のテーブルを復元する**

より複雑なフィルター ルールを使用して複数のテーブルを復元するには、 `br restore full`コマンドを実行し、 [テーブルフィルター](/table-filter.md)に`--filter`または`-f`を指定します。次の例では、 `db*.tbl*`フィルター ルールに一致するテーブルをバックアップ データからターゲット クラスターに復元します。

```shell
tiup br restore full \
--pd "${PD_IP}:2379" \
--filter 'db*.tbl*' \
--storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

### <code>mysql</code>スキーマ内のテーブルを復元する {#restore-tables-in-the-code-mysql-code-schema}

BR v5.1.0 以降、スナップショットをバックアップする場合、 BR は`mysql`スキーマ内の**システム テーブル**をバックアップし、デフォルトでは復元しません。 BR v6.2.0 以降、 `--with-sys-table`を構成すると、 BR は**一部のシステム テーブルのデータ**を復元します。

**BR は、次のシステム テーブルのデータを復元できます。**

    +----------------------------------+
    | mysql.columns_priv               |
    | mysql.db                         |
    | mysql.default_roles              |
    | mysql.global_grants              |
    | mysql.global_priv                |
    | mysql.role_edges                 |
    | mysql.tables_priv                |
    | mysql.user                       |
    | mysql.bind_info                  |
    +----------------------------------+

**BR は次のシステム テーブルを復元しません。**

-   統計表 ( `mysql.stat_*` )。ただし、統計は復元できます。 [統計のバックアップ](/br/br-snapshot-manual.md#back-up-statistics)を参照してください。
-   システム変数テーブル ( `mysql.tidb`および`mysql.global_variables` )
-   [その他のシステムテーブル](https://github.com/pingcap/tidb/blob/release-7.5/br/pkg/restore/systable_restore.go#L31)

<!---->

    +-----------------------------------------------------+
    | capture_plan_baselines_blacklist                    |
    | column_stats_usage                                  |
    | gc_delete_range                                     |
    | gc_delete_range_done                                |
    | global_variables                                    |
    | schema_index_usage                                  |
    | stats_buckets                                       |
    | stats_extended                                      |
    | stats_feedback                                      |
    | stats_fm_sketch                                     |
    | stats_histograms                                    |
    | stats_history                                       |
    | stats_meta                                          |
    | stats_meta_history                                  |
    | stats_table_locked                                  |
    | stats_top_n                                         |
    | tidb                                                |
    +-----------------------------------------------------+

システム権限に関連するデータを復元するときは、次の点に注意してください。

-   BR は、 `user`を`cloud_admin`に、 `host`を`'%'`に持つユーザー データを復元しません。このユーザーはTiDB Cloud用に予約されています。 `cloud_admin`に関連するユーザー権限は正しく復元できないため、クラスター内に`cloud_admin`という名前のユーザーまたはロールを作成しないでください。
-   データを復元する前に、 BR はターゲット クラスタ内のシステム テーブルがバックアップ データ内のシステム テーブルと互換性があるかどうかをチェックします。 「互換性がある」とは、次の条件がすべて満たされていることを意味します。

    -   ターゲット クラスタには、バックアップ データと同じシステム テーブルがあります。
    -   対象クラスタのシステム権限テーブル**の列数は**バックアップデータの列数と同じです。列の順序は重要ではありません。
    -   ターゲット クラスタのシステム権限テーブルの列は、バックアップ データの列と互換性があります。列のデータ型が長さのある型 (整数や文字列など) の場合、ターゲット クラスターの長さはバックアップ データの長さ以上である必要があります。列のデータ型が`ENUM`型の場合、ターゲット クラスター内の`ENUM`の値の数は、バックアップ データ内の値のスーパーセットである必要があります。

## パフォーマンスと影響 {#performance-and-impact}

### スナップショット バックアップのパフォーマンスと影響 {#performance-and-impact-of-snapshot-backup}

バックアップ機能は、クラスターのパフォーマンス (トランザクションレイテンシーと QPS) にある程度の影響を与えます。ただし、バックアップ スレッドの数を[`backup.num-threads`](/tikv-configuration-file.md#num-threads-1)調整するか、クラスターを追加することで影響を軽減できます。

バックアップの影響を説明するために、このドキュメントでは、いくつかのスナップショット バックアップ テストの結果をリストします。

-   (5.3.0 以前) TiKV ノード上のBRのバックアップ スレッドがノードの合計 CPU の 75% を占めると、QPS は元の QPS の 35% 減少します。
-   (5.4.0 以降) TiKV ノード上にBRのスレッドが`8`以下で、クラスターの合計 CPU 使用率が 80% を超えない場合、クラスターに対するBRタスク (書き込みおよび読み取り) の影響は、時点で 20% です。ほとんど。
-   (5.4.0 以降) TiKV ノード上にBRのスレッドが`8`以下で、クラスターの合計 CPU 使用率が 75% を超えない場合、クラスターに対するBRタスク (書き込みおよび読み取り) の影響は、時点で 10% です。ほとんど。
-   (5.4.0 以降) TiKV ノード上にBRのスレッドが`8`以下で、クラスターの合計 CPU 使用率が 60% を超えない場合、 BRタスクはクラスター (書き込みおよび読み取り) にほとんど影響を与えません。

次の方法を使用して、クラスタのパフォーマンスに対するバックアップ タスクの影響を手動で制御できます。ただし、これら 2 つの方法では、クラスターに対するバックアップ タスクの影響を軽減しながら、バックアップ タスクの速度も低下します。

-   `--ratelimit`パラメータを使用して、バックアップ タスクの速度を制限します。このパラメータは、**バックアップ ファイルを外部storageに保存する**速度を制限することに注意してください。バックアップ ファイルの合計サイズを計算するときは、 `backup data size(after compressed)`ベンチマークとして使用してください。
-   TiKV 構成項目[`backup.num-threads`](/tikv-configuration-file.md#num-threads-1)を調整して、バックアップ タスクで使用されるスレッドの数を制限します。内部テストによると、 BR がバックアップ タスクに使用するスレッドが`8`以下で、クラスターの合計 CPU 使用率が 60% を超えない場合、読み取りおよび書き込みのワークロードに関係なく、バックアップ タスクはクラスターにほとんど影響を与えません。

バックアップがクラスターのパフォーマンスに与える影響は、バックアップ スレッドの数を制限することで軽減できますが、これはバックアップのパフォーマンスに影響します。前述のテストは、バックアップ速度がバックアップ スレッドの数に比例することを示しています。スレッド数が少ない場合、バックアップ速度は 20 MiB/スレッド程度になります。たとえば、単一の TiKV ノード上の 5 つのバックアップ スレッドは、100 MiB/秒のバックアップ速度に達します。

### スナップショット復元のパフォーマンスと影響 {#performance-and-impact-of-snapshot-restore}

-   データの復元中、TiDB は TiKV CPU、ディスク IO、およびネットワーク帯域幅のリソースを最大限に活用しようとします。したがって、実行中のアプリケーションへの影響を避けるために、空のクラスターにバックアップ データを復元することをお勧めします。
-   バックアップ データの復元速度は、クラスターの構成、展開、および実行中のアプリケーションに大きく関係します。内部テストでは、単一 TiKV ノードの復元速度は 100 MiB/秒に達する可能性があります。スナップショット復元のパフォーマンスと影響はユーザー シナリオによって異なるため、実際の環境でテストする必要があります。

## こちらも参照 {#see-also}

-   [TiDB のバックアップと復元の使用例](/br/backup-and-restore-use-cases.md)
-   [br コマンドラインマニュアル](/br/use-br-command-line-tool.md)
-   [TiDB スナップショットのバックアップおよび復元のアーキテクチャ](/br/br-snapshot-architecture.md)
