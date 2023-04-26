---
title: Snapshot Backup and Restore Guide
summary: Learn about how to back up and restore TiDB snapshots using the br command-line tool.
aliases: ['/tidb/stable/br-usage-backup/','/tidb/stable/br-usage-restore/','/tidb/stable/br-usage-restore-for-maintain/', '/tidb/stable/br-usage-backup-for-maintain/']
---

# スナップショットのバックアップと復元ガイド {#snapshot-backup-and-restore-guide}

このドキュメントでは、br コマンドライン ツール (以下`br`と呼びます) を使用して TiDB スナップショットをバックアップおよび復元する方法について説明します。データのバックアップと復元を行う前に、まず[br コマンドライン ツールをインストールする](/br/br-use-overview.md#deploy-and-use-br)実行する必要があります。

スナップショット バックアップは、クラスター全体をバックアップするための実装です。 [マルチバージョン同時実行制御 (MVCC)](/tidb-storage.md#mvcc)に基づいて、指定されたスナップショット内のすべてのデータをターゲットstorageにバックアップします。バックアップ データのサイズは、クラスター内の圧縮された単一のレプリカのサイズとほぼ同じです。バックアップが完了したら、バックアップ データを空のクラスターまたは競合データを含まない (同じスキーマまたは同じテーブルを持つ) クラスターに復元し、クラスターをスナップショット バックアップの時点に復元し、複数のクラスターを復元することができます。クラスタのレプリカ設定に従ってレプリカを作成します。

基本的なバックアップと復元に加えて、スナップショットのバックアップと復元は次の機能も提供します。

-   [指定した時点のバックアップデータ](#back-up-cluster-snapshots)
-   [指定したデータベースまたはテーブルのデータを復元する](#restore-a-database-or-a-table)

## クラスターのスナップショットをバックアップする {#back-up-cluster-snapshots}

> **ノート：**
>
> -   次の例では、Amazon S3 アクセス キーとシークレット キーを使用してアクセス許可を承認することを前提としています。 IAMロールを使用してパーミッションを承認する場合は、 `--send-credentials-to-tikv`から`false`を設定する必要があります。
> -   他のstorageシステムまたは認証方法を使用してパーミッションを認証する場合は、 [バックアップ ストレージ](/br/backup-and-restore-storages.md)に従ってパラメーター設定を調整します。

`br backup full`コマンドを実行して、TiDB クラスターのスナップショットをバックアップできます。 `br backup full --help`を実行して、ヘルプ情報を表示します。

```shell
tiup br backup full --pd "${PD_IP}:2379" \
    --backupts '2022-09-08 13:30:00' \
    --storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --ratelimit 128 \
```

前述のコマンドでは:

-   `--backupts` : スナップショットの時点。形式は[TSO](/glossary.md#tso)またはタイムスタンプ ( `400036290571534337`や`2018-05-11 01:42:23`など) にすることができます。このスナップショットのデータがガベージ コレクションされている場合、 `br backup`コマンドはエラーを返し、 `br`は終了します。このパラメーターを指定しない場合、 `br`バックアップの開始時刻に対応するスナップショットを選択します。
-   `--storage` : バックアップ データのstorageアドレス。スナップショット バックアップは、バックアップstorageとして Amazon S3、Google Cloud Storage、および Azure Blob Storage をサポートしています。上記のコマンドでは、Amazon S3 を例として使用しています。詳細については、 [バックアップ ストレージの URL 形式](/br/backup-and-restore-storages.md#url-format)を参照してください。
-   `--ratelimit` : バックアップ タスクを実行する**TiKV ごとの**最大速度。単位は MiB/s です。

バックアップ中は、以下のように進行状況バーがターミナルに表示されます。プログレス バーが 100% に進むと、バックアップ タスクが完了し、合計バックアップ時間、平均バックアップ速度、バックアップ データ サイズなどの統計が表示されます。

```shell
Full Backup <-------------------------------------------------------------------------------> 100.00%
Checksum <----------------------------------------------------------------------------------> 100.00%
*** ["Full Backup success summary"] *** [backup-checksum=3.597416ms] [backup-fast-checksum=2.36975ms] *** [total-take=4.715509333s] [BackupTS=435844546560000000] [total-kv=1131] [total-kv-size=250kB] [average-speed=53.02kB/s] [backup-data-size(after-compressed)=71.33kB] [Size=71330]
```

## スナップショット バックアップのバックアップ時点を取得する {#get-the-backup-time-point-of-a-snapshot-backup}

多くのバックアップを管理するために、スナップショット バックアップの物理時間を取得する必要がある場合は、次のコマンドを実行できます。

```shell
tiup br validate decode --field="end-version" \
--storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}" | tail -n1
```

物理時間`2022-09-08 13:30:00 +0800 CST`に対応する出力は次のとおりです。

```
435844546560000000
```

## クラスターのスナップショットを復元する {#restore-cluster-snapshots}

`br restore full`コマンドを実行して、スナップショット バックアップを復元できます。 `br restore full --help`を実行して、ヘルプ情報を表示します。

次の例では、 [前のバックアップ スナップショット](#back-up-cluster-snapshots)をターゲット クラスタに復元します。

```shell
tiup br restore full --pd "${PD_IP}:2379" \
--storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

復元中は、以下に示すように進行状況バーがターミナルに表示されます。プログレス バーが 100% まで進むと、復元タスクが完了し、合計復元時間、平均復元速度、合計データ サイズなどの統計が表示されます。

```shell
Full Restore <------------------------------------------------------------------------------> 100.00%
*** ["Full Restore success summary"] *** [total-take=4.344617542s] [total-kv=5] [total-kv-size=327B] [average-speed=75.27B/s] [restore-data-size(after-compressed)=4.813kB] [Size=4813] [BackupTS=435844901803917314]
```

### データベースまたはテーブルを復元する {#restore-a-database-or-a-table}

BR は、指定されたデータベースまたはテーブルの部分データをバックアップ データから復元することをサポートします。この機能を使用すると、不要なデータを除外して、特定のデータベースまたはテーブルのみをバックアップできます。

**データベースを復元する**

データベースをクラスターに復元するには、 `br restore db`コマンドを実行します。次の例では、バックアップ データから`test`データベースをターゲット クラスターに復元します。

```shell
tiup br restore db \
--pd "${PD_IP}:2379" \
--db "test" \
--storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

上記のコマンドで、 `--db`復元するデータベースの名前を指定します。

**テーブルを復元する**

1 つのテーブルをクラスターに復元するには、 `br restore table`コマンドを実行します。次の例では、バックアップ データから`test.usertable`テーブルをターゲット クラスターに復元します。

```shell
tiup br restore table --pd "${PD_IP}:2379" \
--db "test" \
--table "usertable" \
--storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

上記のコマンドで、 `--db`復元するデータベースの名前を指定し、 `--table`復元するテーブルの名前を指定します。

**テーブル フィルターを使用して複数のテーブルを復元する**

より複雑なフィルタ ルールを使用して複数のテーブルを復元するには、 `br restore full`コマンドを実行し、 `--filter`または`-f`で[テーブル フィルター](/table-filter.md)指定します。次の例では、 `db*.tbl*`フィルター規則に一致するテーブルをバックアップ データからターゲット クラスターに復元します。

```shell
tiup br restore full \
--pd "${PD_IP}:2379" \
--filter 'db*.tbl*' \
--storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

### <code>mysql</code>スキーマのテーブルを復元する {#restore-tables-in-the-code-mysql-code-schema}

BR v5.1.0 以降、スナップショットをバックアップすると、 BR は`mysql`スキーマの**システム テーブル**をバックアップし、デフォルトでは復元しません。 BR v6.2.0 以降、 `--with-sys-table`を構成すると、 BR は<strong>一部のシステム テーブルのデータ</strong>を復元します。

**BR は、次のシステム テーブルのデータを復元できます。**

```
+----------------------------------+
| mysql.columns_priv               |
| mysql.db                         |
| mysql.default_roles              |
| mysql.global_grants              |
| mysql.global_priv                |
| mysql.role_edges                 |
| mysql.tables_priv                |
| mysql.user                       |
+----------------------------------+
```

**BR は、次のシステム テーブルを復元しません。**

-   統計表 ( `mysql.stats_*` )
-   システム変数テーブル ( `mysql.tidb`および`mysql.global_variables` )
-   [その他のシステム テーブル](https://github.com/pingcap/tidb/blob/master/br/pkg/restore/systable_restore.go#L31)

システム権限に関連するデータを復元する場合は、次の点に注意してください。

-   BR は、 `user`を`cloud_admin`として、 `host` `'%'`としてユーザー データを復元しません。このユーザーはTiDB Cloud用に予約されています。 `cloud_admin`に関連するユーザー権限を正しく復元できないため、クラスター内に`cloud_admin`という名前のユーザーまたはロールを作成しないでください。
-   データを復元する前に、 BR はターゲット クラスタ内のシステム テーブルがバックアップ データ内のシステム テーブルと互換性があるかどうかを確認します。 「互換性がある」とは、次のすべての条件が満たされていることを意味します。

    -   ターゲット クラスタには、バックアップ データと同じシステム テーブルがあります。
    -   対象クラスタのシステム権限テーブル**の列数は、**バックアップデータの列数と同じです。列の順序は重要ではありません。
    -   ターゲット クラスタのシステム権限テーブルの列は、バックアップ データの列と互換性があります。列のデータ型が長さのある型 (整数や文字列など) の場合、ターゲット クラスターの長さは、バックアップ データの長さ以上である必要があります。列のデータ型が`ENUM`型の場合、ターゲット クラスター内の`ENUM`の値の数は、バックアップ データ内の値のスーパーセットである必要があります。

## パフォーマンスと影響 {#performance-and-impact}

### スナップショット バックアップのパフォーマンスと影響 {#performance-and-impact-of-snapshot-backup}

バックアップ機能は、クラスターのパフォーマンス (トランザクションのレイテンシーと QPS) に影響を与えます。ただし、バックアップ スレッド[`backup.num-threads`](/tikv-configuration-file.md#num-threads-1)の数を調整するか、クラスターを追加することで、影響を軽減できます。

バックアップの影響を説明するために、このドキュメントではいくつかのスナップショット バックアップ テストの結果を示します。

-   (5.3.0 以前) TiKV ノード上のBRのバックアップ スレッドがノードの合計 CPU の 75% を占める場合、QPS は元の QPS の 35% 減少します。
-   (5.4.0 以降) TiKV ノードにBRのスレッドが`8`しかなく、クラスターの合計 CPU 使用率が 80% を超えない場合、クラスターに対するBRタスク (書き込みおよび読み取り) の影響は 20% です。多くの。
-   (5.4.0 以降) TiKV ノードにBRのスレッドが`8`しかなく、クラスターの合計 CPU 使用率が 75% を超えない場合、クラスターに対するBRタスク (書き込みおよび読み取り) の影響は 10% です。多くの。
-   (5.4.0 以降) TiKV ノードにBRのスレッドが`8`しかなく、クラスターの合計 CPU 使用率が 60% を超えない場合、 BRタスクはクラスター (書き込みと読み取り) にほとんど影響を与えません。

次の方法を使用して、クラスターのパフォーマンスに対するバックアップ タスクの影響を手動で制御できます。ただし、これらの 2 つの方法では、バックアップ タスクの速度が低下すると同時に、クラスターに対するバックアップ タスクの影響が軽減されます。

-   `--ratelimit`パラメータを使用して、バックアップ タスクの速度を制限します。このパラメータは、**バックアップ ファイルを外部storageに保存する**速度を制限することに注意してください。バックアップ ファイルの合計サイズを計算するときは、 `backup data size(after compressed)`ベンチマークとして使用します。
-   TiKV 構成項目[`backup.num-threads`](/tikv-configuration-file.md#num-threads-1)を調整して、バックアップ タスクで使用されるスレッドの数を制限します。内部テストによると、 BR がバックアップ タスクに`8`以下のスレッドを使用し、クラスターの合計 CPU 使用率が 60% を超えない場合、読み取りおよび書き込みワークロードに関係なく、バックアップ タスクはクラスターにほとんど影響を与えません。

バックアップがクラスタ パフォーマンスに与える影響は、バックアップ スレッド数を制限することで軽減できますが、これはバックアップ パフォーマンスに影響します。前述のテストは、バックアップ速度がバックアップ スレッドの数に比例することを示しています。スレッド数が少ない場合、バックアップ速度は約 20 MiB/スレッドです。たとえば、1 つの TiKV ノード上の 5 つのバックアップ スレッドは、100 MiB/秒のバックアップ速度に達する可能性があります。

### スナップショット リストアのパフォーマンスと影響 {#performance-and-impact-of-snapshot-restore}

-   データの復元中、TiDB は TiKV CPU、ディスク IO、およびネットワーク帯域幅のリソースを最大限に活用しようとします。したがって、実行中のアプリケーションへの影響を避けるために、空のクラスターにバックアップ データを復元することをお勧めします。
-   バックアップ データの復元速度は、クラスター構成、展開、および実行中のアプリケーションに大きく関係しています。内部テストでは、単一の TiKV ノードの復元速度は 100 MiB/秒に達することがあります。スナップショット リストアのパフォーマンスと影響は、ユーザー シナリオによって異なるため、実際の環境でテストする必要があります。

## こちらもご覧ください {#see-also}

-   [TiDB のバックアップと復元の使用例](/br/backup-and-restore-use-cases.md)
-   [br コマンドラインマニュアル](/br/use-br-command-line-tool.md)
-   [TiDB スナップショットのバックアップと復元のアーキテクチャ](/br/br-snapshot-architecture.md)
