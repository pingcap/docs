---
title: Snapshot Backup and Restore Guide
summary: このドキュメントでは、br コマンドライン ツールを使用して TiDB スナップショットをバックアップおよび復元する方法について説明します。スナップショットのバックアップ、指定した時点のデータの復元、データベースまたはテーブルの復元の手順が含まれています。また、スナップショットのバックアップと復元のパフォーマンスと影響についても説明します。
---

# スナップショットのバックアップと復元ガイド {#snapshot-backup-and-restore-guide}

このドキュメントでは、br コマンドライン ツール (以下、 `br`と呼びます) を使用して TiDB スナップショットをバックアップおよび復元する方法について説明します。 データのバックアップと復元を行う前に、まず[brコマンドラインツールをインストールする](/br/br-use-overview.md#deploy-and-use-br)を行う必要があります。

スナップショットバックアップは、クラスター全体をバックアップする実装です。 [マルチバージョン同時実行制御 (MVCC)](/tidb-storage.md#mvcc)に基づいて、指定されたスナップショット内のすべてのデータをターゲットstorageにバックアップします。 バックアップデータのサイズは、クラスター内の圧縮された単一のレプリカのサイズとほぼ同じです。 バックアップが完了したら、バックアップデータを空のクラスターまたは競合データを含まないクラスター（同じスキーマまたは同じテーブルを持つ）に復元したり、クラスターをスナップショットバックアップの時点に復元したり、クラスターレプリカ設定に従って複数のレプリカを復元したりできます。

基本的なバックアップと復元に加えて、スナップショット バックアップと復元では次の機能も提供されます。

-   [指定した時点のデータのバックアップ](#back-up-cluster-snapshots)
-   [指定されたデータベースまたはテーブルのデータを復元する](#restore-a-database-or-a-table)

## クラスタースナップショットをバックアップする {#back-up-cluster-snapshots}

> **注記：**
>
> -   次の例では、 Amazon S3 アクセスキーとシークレットキーを使用して権限を承認することを前提としています。IAM ロールを使用して権限を承認する場合は、 `--send-credentials-to-tikv`から`false`に設定する必要があります。
> -   他のstorageシステムまたは認証方法を使用して権限を認証する場合は、 [バックアップストレージ](/br/backup-and-restore-storages.md)に従ってパラメータ設定を調整します。

`br backup full`コマンドを実行すると、TiDB クラスターのスナップショットをバックアップできます。ヘルプ情報を表示するには、 `br backup full --help`実行します。

```shell
tiup br backup full --pd "${PD_IP}:2379" \
    --backupts '2022-09-08 13:30:00 +08:00' \
    --storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --ratelimit 128 \
```

上記のコマンドでは、

-   `--backupts` : スナップショットの時点。形式は[TSO](/glossary.md#tso)またはタイムスタンプ ( `400036290571534337`や`2018-05-11 01:42:23 +08:00`など) です。このスナップショットのデータがガベージ コレクションされた場合、 `br backup`コマンドはエラーを返し、 `br`は終了します。タイムスタンプを使用してバックアップする場合は、タイム ゾーンも指定することをお勧めします。そうしないと、 `br`デフォルトでローカル タイム ゾーンを使用してタイムスタンプを作成するため、バックアップの時点が不正確になる可能性があります。このパラメーターを指定しない場合、 `br`バックアップ開始時刻に対応するスナップショットを選択します。
-   `--storage` : バックアップ データのstorageアドレス。スナップショット バックアップでは、バックアップstorageとして Amazon S3、Google Cloud Storage、Azure Blob Storage がサポートされています。上記のコマンドでは、例として Amazon S3 を使用しています。詳細については、 [外部ストレージサービスの URI 形式](/external-storage-uri.md)を参照してください。
-   `--ratelimit` : バックアップ タスクを実行する**TiKV あたりの**最大速度。単位は MiB/s です。

バックアップ中は、以下のようにターミナルに進行状況バーが表示されます。進行状況バーが 100% に進むと、バックアップ タスクが完了し、合計バックアップ時間、平均バックアップ速度、バックアップ データ サイズなどの統計情報が表示されます。

```shell
Full Backup <-------------------------------------------------------------------------------> 100.00%
Checksum <----------------------------------------------------------------------------------> 100.00%
*** ["Full Backup success summary"] *** [backup-checksum=3.597416ms] [backup-fast-checksum=2.36975ms] *** [total-take=4.715509333s] [BackupTS=435844546560000000] [total-kv=1131] [total-kv-size=250kB] [average-speed=53.02kB/s] [backup-data-size(after-compressed)=71.33kB] [Size=71330]
```

## スナップショットバックアップのバックアップ時点を取得する {#get-the-backup-time-point-of-a-snapshot-backup}

多数のバックアップを管理するために、スナップショット バックアップの物理的な時間を取得する必要がある場合は、次のコマンドを実行できます。

```shell
tiup br validate decode --field="end-version" \
--storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}" | tail -n1
```

出力は物理時間`2022-09-08 13:30:00 +0800 CST`に対応して次のようになります。

    435844546560000000

## クラスタースナップショットを復元する {#restore-cluster-snapshots}

`br restore full`コマンドを実行するとスナップショット バックアップを復元できます。ヘルプ情報を表示するには`br restore full --help`実行します。

次の例では、 [前のバックアップスナップショット](#back-up-cluster-snapshots)ターゲット クラスターに復元します。

```shell
tiup br restore full --pd "${PD_IP}:2379" \
--storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

復元中は、以下のようにターミナルに進行状況バーが表示されます。進行状況バーが 100% に進むと、復元タスクが完了し、合計復元時間、平均復元速度、合計データ サイズなどの統計情報が表示されます。

```shell
Full Restore <------------------------------------------------------------------------------> 100.00%
*** ["Full Restore success summary"] *** [total-take=4.344617542s] [total-kv=5] [total-kv-size=327B] [average-speed=75.27B/s] [restore-data-size(after-compressed)=4.813kB] [Size=4813] [BackupTS=435844901803917314]
```

### データベースまたはテーブルを復元する {#restore-a-database-or-a-table}

BR は、バックアップ データから指定されたデータベースまたはテーブルの部分的なデータの復元をサポートしています。この機能を使用すると、不要なデータを除外し、特定のデータベースまたはテーブルのみをバックアップできます。

**データベースを復元する**

データベースをクラスターに復元するには、 `br restore db`コマンドを実行します。次の例では、 `test`データベースをバックアップ データからターゲット クラスターに復元します。

```shell
tiup br restore db \
--pd "${PD_IP}:2379" \
--db "test" \
--storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

上記のコマンドでは、 `--db`復元するデータベースの名前を指定します。

**テーブルを復元する**

単一のテーブルをクラスターに復元するには、 `br restore table`コマンドを実行します。次の例では、バックアップ データから`test.usertable`テーブルをターゲット クラスターに復元します。

```shell
tiup br restore table --pd "${PD_IP}:2379" \
--db "test" \
--table "usertable" \
--storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

上記のコマンドでは、 `--db`復元するデータベースの名前を指定し、 `--table`復元するテーブルの名前を指定します。

**テーブルフィルターを使用して複数のテーブルを復元する**

より複雑なフィルター ルールを使用して複数のテーブルを復元するには、 `br restore full`コマンドを実行し、 [テーブルフィルター](/table-filter.md) `--filter`または`-f`で指定します。次の例では、 `db*.tbl*`フィルター ルールに一致するテーブルをバックアップ データからターゲット クラスターに復元します。

```shell
tiup br restore full \
--pd "${PD_IP}:2379" \
--filter 'db*.tbl*' \
--storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

### <code>mysql</code>スキーマ内のテーブルを復元する {#restore-tables-in-the-code-mysql-code-schema}

BR v5.1.0 以降では、スナップショットをバックアップすると、 BR は`mysql`スキーマの**システム テーブル**をバックアップし、デフォルトでは復元しません。BR BR以降では、 `--with-sys-table`構成すると、 BR は**一部のシステム テーブルのデータ**を復元します。

**BR は次のシステム テーブルのデータを復元できます。**

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

-   統計表（ `mysql.stat_*` ）。ただし、統計は復元可能です。3 [統計のバックアップ](/br/br-snapshot-manual.md#back-up-statistics)参照してください。
-   システム変数テーブル（ `mysql.tidb`と`mysql.global_variables` ）
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

システム権限に関連するデータを復元する場合、データを復元する前に、 BR はターゲット クラスター内のシステム テーブルがバックアップ データ内のシステム テーブルと互換性があるかどうかをチェックすることに注意してください。「互換性がある」とは、次の条件がすべて満たされていることを意味します。

-   ターゲット クラスターには、バックアップ データと同じシステム テーブルがあります。
-   ターゲット クラスターのシステム権限テーブルの**列数は、**バックアップ データ内の列数と同じです。列の順序は重要ではありません。
-   ターゲット クラスターのシステム権限テーブル内の列は、バックアップ データ内の列と互換性があります。列のデータ型が長さのある型 (整数や文字列など) の場合、ターゲット クラスター内の長さはバックアップ データ内の長さ以上である必要があります。列のデータ型が`ENUM`型の場合、ターゲット クラスター内の`ENUM`の値の数は、バックアップ データ内の値のスーパーセットである必要があります。

## パフォーマンスと影響 {#performance-and-impact}

### スナップショットバックアップのパフォーマンスと影響 {#performance-and-impact-of-snapshot-backup}

バックアップ機能は、クラスターの[`backup.num-threads`](/tikv-configuration-file.md#num-threads-1) (トランザクションのレイテンシーと QPS) に多少影響を及ぼします。ただし、バックアップ スレッドの数を調整するか、クラスターを追加することで、影響を軽減できます。

バックアップの影響を説明するために、このドキュメントでは、いくつかのスナップショット バックアップ テストのテスト結果をリストします。

-   (5.3.0 以前) TiKV ノード上のBRのバックアップ スレッドがノードの合計 CPU の 75% を占めると、QPS は元の QPS の 35% 減少します。
-   (5.4.0 以降) TiKV ノード上のBRスレッドが`8`以下で、クラスターの合計 CPU 使用率が 80% を超えない場合、 BRタスク (書き込みと読み取り) がクラスターに与える影響は最大 20% になります。
-   (5.4.0 以降) TiKV ノード上のBRスレッドが`8`以下で、クラスターの合計 CPU 使用率が 75% を超えない場合、 BRタスク (書き込みと読み取り) がクラスターに与える影響は最大 10% になります。
-   (5.4.0 以降) TiKV ノード上のBRスレッドが`8`以下で、クラスターの合計 CPU 使用率が 60% を超えない場合、 BRタスクはクラスターにほとんど影響を与えません (書き込みと読み取り)。

次の方法を使用して、バックアップ タスクがクラスターのパフォーマンスに与える影響を手動で制御できます。ただし、これら 2 つの方法では、バックアップ タスクの速度が低下すると同時に、バックアップ タスクがクラスターに与える影響も軽減されます。

-   バックアップ タスクの速度を制限するには、 `--ratelimit`パラメータを使用します。このパラメータは**、バックアップ ファイルを外部storageに保存する**速度を制限することに注意してください。バックアップ ファイルの合計サイズを計算するときは、 `backup data size(after compressed)`をベンチマークとして使用します。 `--ratelimit`を設定すると、タスクが多すぎて速度制限に失敗するのを避けるために、 br の`concurrency`パラメータは自動的に`1`に調整されます。
-   TiKV 構成項目[`backup.num-threads`](/tikv-configuration-file.md#num-threads-1)を調整して、バックアップ タスクで使用されるスレッドの数を制限します。内部テストによると、 BR がバックアップ タスクに使用するスレッドが`8`以下で、クラスターの合計 CPU 使用率が 60% を超えない場合、読み取りおよび書き込みのワークロードに関係なく、バックアップ タスクはクラスターにほとんど影響を与えません。

バックアップ スレッド数を制限することで、バックアップがクラスター パフォーマンスに与える影響を軽減できますが、これはバックアップ パフォーマンスに影響します。前述のテストでは、バックアップ速度はバックアップ スレッド数に比例することが示されています。スレッド数が少ない場合、バックアップ速度は約 20 MiB/スレッドです。たとえば、単一の TiKV ノード上の 5 つのバックアップ スレッドは、100 MiB/秒のバックアップ速度に達することができます。

### スナップショット復元のパフォーマンスと影響 {#performance-and-impact-of-snapshot-restore}

-   データの復元中、TiDB は TiKV CPU、ディスク IO、およびネットワーク帯域幅のリソースを最大限に活用しようとします。そのため、実行中のアプリケーションに影響を与えないように、空のクラスターでバックアップ データを復元することをお勧めします。
-   バックアップ データの復元速度は、クラスターの構成、展開、実行中のアプリケーションに大きく関係します。社内テストでは、単一の TiKV ノードの復元速度は 100 MiB/秒に達することがあります。スナップショット復元のパフォーマンスと影響はユーザー シナリオによって異なるため、実際の環境でテストする必要があります。

## 参照 {#see-also}

-   [TiDB バックアップと復元のユースケース](/br/backup-and-restore-use-cases.md)
-   [br コマンドラインマニュアル](/br/use-br-command-line-tool.md)
-   [TiDB スナップショットのバックアップと復元のアーキテクチャ](/br/br-snapshot-architecture.md)
