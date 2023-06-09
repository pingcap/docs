---
title: Use TiFlash
---

データのインポートから TPC-H データセットでのクエリまでのプロセス全体を体験するには、 [<a href="/quick-start-with-htap.md">TiDB HTAPのクイック スタート ガイド</a>](/quick-start-with-htap.md)を参照してください。

# TiFlashを使用する {#use-tiflash}

TiFlashの展開後、データ レプリケーションは自動的に開始されません。レプリケートするテーブルを手動で指定する必要があります。

TiDB を使用して中規模の分析処理用にTiFlashレプリカを読み取ることも、TiSpark を使用して大規模な分析処理用にTiFlashレプリカを読み取ることもできますが、これは独自のニーズに基づいています。詳細については、次のセクションを参照してください。

-   [<a href="#use-tidb-to-read-tiflash-replicas">TiDB を使用してTiFlashレプリカを読み取る</a>](#use-tidb-to-read-tiflash-replicas)
-   [<a href="#use-tispark-to-read-tiflash-replicas">TiSpark を使用してTiFlashレプリカを読み取る</a>](#use-tispark-to-read-tiflash-replicas)

## テーブルのTiFlashレプリカを作成する {#create-tiflash-replicas-for-tables}

TiFlashが TiKV クラスターに接続された後、デフォルトではデータ レプリケーションは開始されません。 MySQL クライアントを通じて DDL ステートメントを TiDB に送信して、特定のテーブルのTiFlashレプリカを作成できます。

{{< copyable "" >}}

```sql
ALTER TABLE table_name SET TIFLASH REPLICA count;
```

上記コマンドのパラメータは次のように記述されます。

-   `count`レプリカの数を示します。値が`0`の場合、レプリカは削除されます。

同じテーブルに対して複数の DDL ステートメントを実行すると、最後のステートメントのみが有効になります。次の例では、テーブル`tpch50`に対して 2 つの DDL ステートメントが実行されますが、有効になるのは 2 番目のステートメント (レプリカを削除する) のみです。

テーブルの 2 つのレプリカを作成します。

{{< copyable "" >}}

```sql
ALTER TABLE `tpch50`.`lineitem` SET TIFLASH REPLICA 2;
```

レプリカを削除します。

{{< copyable "" >}}

```sql
ALTER TABLE `tpch50`.`lineitem` SET TIFLASH REPLICA 0;
```

**ノート：**

-   上記の DDL ステートメントを通じてテーブル`t`がTiFlashにレプリケートされる場合、次のステートメントを使用して作成されたテーブルも自動的にTiFlashにレプリケートされます。

    {{< copyable "" >}}

    ```sql
    CREATE TABLE table_name like t;
    ```

-   v4.0.6 より前のバージョンの場合、 TiDB Lightning を使用してデータをインポートする前にTiFlashレプリカを作成すると、データのインポートは失敗します。テーブルのTiFlashレプリカを作成する前に、テーブルにデータをインポートする必要があります。

-   TiDB とTiDB Lightning が両方とも v4.0.6 以降の場合、テーブルにTiFlashレプリカがあるかどうかに関係なく、 TiDB Lightningを使用してそのテーブルにデータをインポートできます。これにより、 TiDB Lightningの手順が遅くなる可能性があることに注意してください。これは、Lightning ホストの NIC 帯域幅、 TiFlashノードの CPU とディスクの負荷、 TiFlashレプリカの数によって異なります。

-   PD スケジュールのパフォーマンスが低下するため、1,000 を超えるテーブルを複製しないことをお勧めします。この制限は、後のバージョンでは削除される予定です。

-   v5.1 以降のバージョンでは、システム テーブルのレプリカの設定はサポートされなくなりました。クラスターをアップグレードする前に、関連するシステム テーブルのレプリカをクリアする必要があります。そうしないと、クラスターを新しいバージョンにアップグレードした後にシステム テーブルのレプリカ設定を変更できません。

### レプリケーションの進行状況を確認する {#check-replication-progress}

次のステートメントを使用して、特定のテーブルのTiFlashレプリカのステータスを確認できます。テーブルは`WHERE`句を使用して指定されます。 `WHERE`句を削除すると、すべてのテーブルのレプリカのステータスがチェックされます。

{{< copyable "" >}}

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>' and TABLE_NAME = '<table_name>';
```

上記のステートメントの結果は次のようになります。

-   `AVAILABLE` 、このテーブルのTiFlashレプリカが使用可能かどうかを示します。 `1`使用可能を意味し、 `0`使用不可を意味します。レプリカが使用可能になると、このステータスは変わりません。 DDL ステートメントを使用してレプリカの数を変更すると、レプリケーションのステータスが再計算されます。
-   `PROGRESS`レプリケーションの進行状況を意味します。値は`0.0` ～ `1.0`です。 `1`少なくとも 1 つのレプリカが複製されていることを意味します。

### TiFlashレプリケーションを高速化する {#speed-up-tiflash-replication}

TiFlashレプリカが追加される前に、各 TiKV インスタンスはフル テーブル スキャンを実行し、スキャンされたデータを「スナップショット」としてTiFlashに送信してレプリカを作成します。デフォルトでは、オンライン サービスへの影響を最小限に抑えるために、 TiFlashレプリカはリソース使用量を減らしてゆっくり追加されます。 TiKV ノードとTiFlashノードに予備の CPU とディスク IO リソースがある場合は、次の手順を実行してTiFlashレプリケーションを高速化できます。

1.  TiFlashプロキシおよび TiKV 構成を調整して、各 TiKV およびTiFlashインスタンスのスナップショット書き込み速度制限を一時的に増加します。たとえば、 TiUPを使用して構成を管理する場合、構成は次のようになります。

    ```yaml
    tikv:
      server.snap-max-write-bytes-per-sec: 300MiB  # Default to 100MiB.
    tiflash-learner:
      raftstore.snap-handle-pool-size: 10          # Default to 2. Can be adjusted to >= node's CPU num * 0.6.
      raftstore.apply-low-priority-pool-size: 10   # Default to 1. Can be adjusted to >= node's CPU num * 0.6.
      server.snap-max-write-bytes-per-sec: 300MiB  # Default to 100MiB.
    ```

    構成の変更は、 TiFlashインスタンスと TiKV インスタンスを再起動した後に有効になります。 TiKV 構成は、 [<a href="https://docs.pingcap.com/tidb/stable/dynamic-config">動的構成 SQL ステートメント</a>](https://docs.pingcap.com/tidb/stable/dynamic-config)使用してオンラインで変更することもできます。これは、TiKV インスタンスを再起動せずにすぐに有効になります。

    ```sql
    SET CONFIG tikv `server.snap-max-write-bytes-per-sec` = '300MiB';
    ```

    前述の構成を調整した後、レプリケーション速度は依然として PD 制限によってグローバルに制限されているため、現時点では加速を観察することはできません。

2.  新しいレプリカの速度制限を段階的に緩和するには、 [<a href="https://docs.pingcap.com/tidb/stable/pd-control">PD Control</a>](https://docs.pingcap.com/tidb/stable/pd-control)を使用します。

    デフォルトの新しいレプリカの速度制限は 30 です。これは、毎分約 30 のリージョンがTiFlashレプリカを追加することを意味します。次のコマンドを実行すると、すべてのTiFlashインスタンスの制限が 60 に調整され、元の速度が 2 倍になります。

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 60 add-peer
    ```

    > 前述のコマンドでは、 `<CLUSTER_VERSION>`実際のクラスターのバージョンに置き換え、 `<PD_ADDRESS>:2379`任意の PD ノードのアドレスに置き換える必要があります。例えば：
    >
    > ```shell
    > tiup ctl:v6.1.1 pd -u http://192.168.1.4:2379 store limit all engine tiflash 60 add-peer
    > ```

    数分以内に、 TiFlashノードの CPU およびディスク IO リソースの使用量が大幅に増加することがわかり、 TiFlashはレプリカをより速く作成するはずです。同時に、TiKV ノードの CPU およびディスク IO リソースの使用量も増加します。

    この時点で TiKV ノードとTiFlashノードにまだ予備のリソースがあり、オンライン サービスのレイテンシーが大幅に増加しない場合は、制限をさらに緩和することができます (たとえば、元の速度を 3 倍にする)。

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 90 add-peer
    ```

3.  TiFlashレプリケーションが完了したら、デフォルト構成に戻して、オンライン サービスへの影響を軽減します。

    次のPD Controlコマンドを実行して、デフォルトの新しいレプリカの速度制限を復元します。

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 30 add-peer
    ```

    TiUPで変更された構成をコメントアウトして、デフォルトのスナップショット書き込み速度制限を復元します。

    ```yaml
    # tikv:
    #   server.snap-max-write-bytes-per-sec: 300MiB
    # tiflash-learner:
    #   raftstore.snap-handle-pool-size: 10
    #   raftstore.apply-low-priority-pool-size: 10
    #   server.snap-max-write-bytes-per-sec: 300MiB
    ```

### 利用可能なゾーンを設定する {#set-available-zones}

レプリカの構成時に、災害復旧のためにTiFlashレプリカを複数のデータセンターに分散する必要がある場合は、次の手順に従って利用可能なゾーンを構成できます。

1.  クラスター構成ファイルでTiFlashノードのラベルを指定します。

    ```
    tiflash_servers:
      - host: 172.16.5.81
        config:
          flash.proxy.labels: zone=z1
      - host: 172.16.5.82
        config:
          flash.proxy.labels: zone=z1
      - host: 172.16.5.85
        config:
          flash.proxy.labels: zone=z2
    ```

2.  クラスターを起動した後、レプリカを作成するときにラベルを指定します。

    {{< copyable "" >}}

    ```sql
    ALTER TABLE table_name SET TIFLASH REPLICA count LOCATION LABELS location_labels;
    ```

    例えば：

    {{< copyable "" >}}

    ```sql
    ALTER TABLE t SET TIFLASH REPLICA 2 LOCATION LABELS "zone";
    ```

3.  PD はラベルに基づいてレプリカをスケジュールします。この例では、PD はテーブル`t`の 2 つのレプリカを 2 つの利用可能なゾーンにそれぞれスケジュールします。 pd-ctl を使用してスケジュールを表示できます。

    ```shell
    > tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store

        ...
        "address": "172.16.5.82:23913",
        "labels": [
          { "key": "engine", "value": "tiflash"},
          { "key": "zone", "value": "z1" }
        ],
        "region_count": 4,

        ...
        "address": "172.16.5.81:23913",
        "labels": [
          { "key": "engine", "value": "tiflash"},
          { "key": "zone", "value": "z1" }
        ],
        "region_count": 5,
        ...

        "address": "172.16.5.85:23913",
        "labels": [
          { "key": "engine", "value": "tiflash"},
          { "key": "zone", "value": "z2" }
        ],
        "region_count": 9,
        ...
    ```

ラベルを使用したレプリカのスケジュール設定の詳細については、 [<a href="/schedule-replicas-by-topology-labels.md">トポロジ ラベルごとにレプリカをスケジュールする</a>](/schedule-replicas-by-topology-labels.md) 、 [<a href="/multi-data-centers-in-one-city-deployment.md">1 つの地域展開における複数のデータセンター</a>](/multi-data-centers-in-one-city-deployment.md) 、および[<a href="/three-data-centers-in-two-cities-deployment.md">2 つの地域に配置された 3 つのデータ センター</a>](/three-data-centers-in-two-cities-deployment.md)を参照してください。

## TiDB を使用してTiFlashレプリカを読み取る {#use-tidb-to-read-tiflash-replicas}

TiDB には、 TiFlashレプリカを読み取る 3 つの方法が用意されています。エンジン設定を行わずにTiFlashレプリカを追加した場合、デフォルトで CBO (コストベースの最適化) モードが使用されます。

### 賢い選択 {#smart-selection}

TiFlashレプリカを含むテーブルの場合、TiDB オプティマイザーはコスト見積もりに基づいてTiFlashレプリカを使用するかどうかを自動的に決定します。 `desc`または`explain analyze`ステートメントを使用して、 TiFlashレプリカが選択されているかどうかを確認できます。例えば：

{{< copyable "" >}}

```sql
desc select count(*) from test.t;
```

```
+--------------------------+---------+--------------+---------------+--------------------------------+
| id                       | estRows | task         | access object | operator info                  |
+--------------------------+---------+--------------+---------------+--------------------------------+
| StreamAgg_9              | 1.00    | root         |               | funcs:count(1)->Column#4       |
| └─TableReader_17         | 1.00    | root         |               | data:TableFullScan_16          |
|   └─TableFullScan_16     | 1.00    | cop[tiflash] | table:t       | keep order:false, stats:pseudo |
+--------------------------+---------+--------------+---------------+--------------------------------+
3 rows in set (0.00 sec)
```

{{< copyable "" >}}

```sql
explain analyze select count(*) from test.t;
```

```
+--------------------------+---------+---------+--------------+---------------+----------------------------------------------------------------------+--------------------------------+-----------+------+
| id                       | estRows | actRows | task         | access object | execution info                                                       | operator info                  | memory    | disk |
+--------------------------+---------+---------+--------------+---------------+----------------------------------------------------------------------+--------------------------------+-----------+------+
| StreamAgg_9              | 1.00    | 1       | root         |               | time:83.8372ms, loops:2                                              | funcs:count(1)->Column#4       | 372 Bytes | N/A  |
| └─TableReader_17         | 1.00    | 1       | root         |               | time:83.7776ms, loops:2, rpc num: 1, rpc time:83.5701ms, proc keys:0 | data:TableFullScan_16          | 152 Bytes | N/A  |
|   └─TableFullScan_16     | 1.00    | 1       | cop[tiflash] | table:t       | time:43ms, loops:1                                                   | keep order:false, stats:pseudo | N/A       | N/A  |
+--------------------------+---------+---------+--------------+---------------+----------------------------------------------------------------------+--------------------------------+-----------+------+
```

`cop[tiflash]` 、タスクが処理のためにTiFlashに送信されることを意味します。 TiFlashレプリカを選択していない場合は、 `analyze table`ステートメントを使用して統計の更新を試み、 `explain analyze`ステートメントを使用して結果を確認します。

テーブルにTiFlashレプリカが 1 つしかなく、関連ノードがサービスを提供できない場合、CBO モードでのクエリは繰り返し再試行されることに注意してください。この状況では、エンジンを指定するか、手動ヒントを使用して TiKV レプリカからデータを読み取る必要があります。

### エンジンの隔離 {#engine-isolation}

エンジンの分離では、対応する変数を構成することで、すべてのクエリが指定されたエンジンのレプリカを使用するように指定します。オプションのエンジンは、「tikv」、「tidb」（一部の TiDB システム テーブルを保存し、ユーザーが積極的に使用できない TiDB の内部メモリテーブル領域を示します）、および「tiflash」であり、次の 2 つの構成レベルがあります。

-   TiDB インスタンス レベル、つまり INSTANCE レベル。 TiDB 構成ファイルに次の構成項目を追加します。

    ```
    [isolation-read]
    engines = ["tikv", "tidb", "tiflash"]
    ```

    **INSTANCE レベルのデフォルト構成は`[&quot;tikv&quot;, &quot;tidb&quot;, &quot;tiflash&quot;]`です。**

-   セッションレベル。次のステートメントを使用して構成します。

    {{< copyable "" >}}

    ```sql
    set @@session.tidb_isolation_read_engines = "engine list separated by commas";
    ```

    また

    {{< copyable "" >}}

    ```sql
    set SESSION tidb_isolation_read_engines = "engine list separated by commas";
    ```

    SESSION レベルのデフォルト構成は、TiDB INSTANCE レベルの構成を継承します。

最終的なエンジン設定はセッション レベルの設定です。つまり、セッション レベルの設定はインスタンス レベルの設定をオーバーライドします。たとえば、INSTANCE レベルで「tikv」を設定し、SESSION レベルで「tiflash」を設定した場合、 TiFlashレプリカが読み取られます。最終的なエンジン構成が「tikv」と「tiflash」の場合、TiKV とTiFlash のレプリカが両方とも読み取られ、オプティマイザーは実行するより適切なエンジンを自動的に選択します。

> **ノート：**
>
> [<a href="/dashboard/dashboard-intro.md">TiDB ダッシュボード</a>](/dashboard/dashboard-intro.md)およびその他のコンポーネントは、TiDBメモリテーブル領域に格納されているいくつかのシステム テーブルを読み取る必要があるため、常に「tidb」エンジンをインスタンス レベルのエンジン構成に追加することをお勧めします。

クエリされたテーブルに指定されたエンジンのレプリカがない場合 (たとえば、エンジンが「tiflash」として構成されているが、テーブルにTiFlashレプリカがない場合)、クエリはエラーを返します。

### 手動ヒント {#manual-hint}

手動ヒントでは、エンジン分離を満たすことを前提として、TiDB が特定のテーブルに指定されたレプリカを使用するように強制できます。手動ヒントの使用例を次に示します。

{{< copyable "" >}}

```sql
select /*+ read_from_storage(tiflash[table_name]) */ ... from table_name;
```

クエリ ステートメントでテーブルに別名を設定する場合、ヒントを有効にするために、ヒントを含むステートメントで別名を使用する必要があります。例えば：

{{< copyable "" >}}

```sql
select /*+ read_from_storage(tiflash[alias_a,alias_b]) */ ... from table_name_1 as alias_a, table_name_2 as alias_b where alias_a.column_1 = alias_b.column_2;
```

上記のステートメントで、 `tiflash[]`オプティマイザにTiFlashレプリカを読み取るように指示します。 `tikv[]`使用して、必要に応じてオプティマイザーに TiKV レプリカを読み取るように指示することもできます。ヒント構文の詳細については、 [<a href="/optimizer-hints.md#read_from_storagetiflasht1_name--tl_name--tikvt2_name--tl_name-">READ_FROM_STORAGE</a>](/optimizer-hints.md#read_from_storagetiflasht1_name--tl_name--tikvt2_name--tl_name-)を参照してください。

ヒントで指定されたテーブルに指定されたエンジンのレプリカがない場合、ヒントは無視され、警告が報告されます。また、ヒントはエンジン隔離を前提としてのみ有効となります。ヒントで指定されたエンジンがエンジン分離リストにない場合も、ヒントは無視され、警告が報告されます。

> **ノート：**
>
> 5.7.7 以前のバージョンの MySQL クライアントは、デフォルトでオプティマイザー ヒントをクリアします。これらの初期バージョンでヒント構文を使用するには、 `--comments`オプション (たとえば`mysql -h 127.0.0.1 -P 4000 -uroot --comments`を指定してクライアントを起動します。

### スマート選択、エンジン分離、および手動ヒントの関係 {#the-relationship-of-smart-selection-engine-isolation-and-manual-hint}

TiFlashレプリカを読み取る上記の 3 つの方法では、エンジンの分離により、利用可能なエンジンのレプリカの全体範囲が指定されます。この範囲内では、手動ヒントにより、より詳細なステートメント レベルおよびテーブル レベルのエンジン選択が提供されます。最後に、CBO が決定を下し、指定されたエンジン リスト内のコスト見積もりに基づいてエンジンのレプリカを選択します。

> **ノート：**
>
> v4.0.3 より前では、読み取り専用以外の SQL ステートメント ( `INSERT INTO ... SELECT` 、 `SELECT ... FOR UPDATE` 、 `UPDATE ...` 、 `DELETE ...`など) でTiFlashレプリカから読み取る動作は未定義です。 v4.0.3 以降のバージョンでは、データの正確性を保証するために、TiDB は内部的に読み取り専用以外の SQL ステートメントのTiFlashレプリカを無視します。つまり、 [<a href="#smart-selection">賢い選択</a>](#smart-selection)場合、TiDB は非TiFlashレプリカを自動的に選択します。 TiFlashレプリカ**のみ**を指定する[<a href="#engine-isolation">エンジンの隔離</a>](#engine-isolation)の場合、TiDB はエラーを報告します。 [<a href="#manual-hint">手動ヒント</a>](#manual-hint)の場合、TiDB はヒントを無視します。

## TiSpark を使用してTiFlashレプリカを読み取る {#use-tispark-to-read-tiflash-replicas}

現在、TiSpark を使用して、TiDB のエンジン分離と同様の方法でTiFlashレプリカを読み取ることができます。この方法は`spark.tispark.isolation_read_engines`パラメータを設定する方法です。パラメータ値のデフォルトは`tikv,tiflash`です。これは、TiDB が CBO の選択に従ってTiFlashまたは TiKV からデータを読み取ることを意味します。パラメータ値を`tiflash`に設定すると、TiDB がTiFlashからデータを強制的に読み取ります。

> **ノート：**
>
> このパラメータが`tiflash`に設定されている場合、クエリに含まれるすべてのテーブルのTiFlashレプリカのみが読み取られ、これらのテーブルにはTiFlashレプリカが必要です。 TiFlashレプリカがないテーブルの場合、エラーが報告されます。このパラメータを`tikv`に設定すると、TiKV レプリカのみが読み取られます。

このパラメータは、次のいずれかの方法で構成できます。

-   `spark-defaults.conf`ファイルに次の項目を追加します。

    ```
    spark.tispark.isolation_read_engines tiflash
    ```

-   Spark シェルまたは Thriftサーバーを初期化する場合は、初期化コマンドに`--conf spark.tispark.isolation_read_engines=tiflash`を追加します。

-   Spark シェルにリアルタイムで`spark.conf.set("spark.tispark.isolation_read_engines", "tiflash")`を設定します。

-   サーバーがbeeline経由で接続された後、Thriftサーバーに`set spark.tispark.isolation_read_engines=tiflash`を設定します。

## サポートされているプッシュダウン計算 {#supported-push-down-calculations}

TiFlash は、次の演算子のプッシュダウンをサポートしています。

-   TableScan: テーブルからデータを読み取ります。
-   選択: データをフィルタリングします。
-   HashAgg: [<a href="/explain-aggregation.md#hash-aggregation">ハッシュ集計</a>](/explain-aggregation.md#hash-aggregation)アルゴリズムに基づいてデータの集計を実行します。
-   StreamAgg: [<a href="/explain-aggregation.md#stream-aggregation">ストリーム集計</a>](/explain-aggregation.md#stream-aggregation)アルゴリズムに基づいてデータの集計を実行します。 SteamAgg は`GROUP BY`条件なしの集計のみをサポートします。
-   TopN: TopN 計算を実行します。
-   リミット: リミット計算を実行します。
-   プロジェクト: 投影計算を実行します。
-   HashJoin (等価結合): [<a href="/explain-joins.md#hash-join">ハッシュ結合</a>](/explain-joins.md#hash-join)アルゴリズムに基づいて結合計算を実行しますが、次の条件があります。
    -   オペレータは[<a href="#use-the-mpp-mode">MPPモード</a>](#use-the-mpp-mode)の場合のみ押下可能です。
    -   `Full Outer Join`のプッシュダウンはサポートされていません。
-   HashJoin (非等価結合): デカルト結合アルゴリズムを実行しますが、次の条件があります。
    -   オペレータは[<a href="#use-the-mpp-mode">MPPモード</a>](#use-the-mpp-mode)の場合のみ押下可能です。
    -   デカルト結合はブロードキャスト結合でのみサポートされます。

TiDB では、オペレーターはツリー構造で編成されます。オペレーターをTiFlashにプッシュダウンするには、次の前提条件をすべて満たす必要があります。

-   その子オペレータはすべてTiFlashにプッシュダウンできます。
-   演算子に式が含まれている場合 (ほとんどの演算子には式が含まれています)、演算子のすべての式をTiFlashにプッシュダウンできます。

現在、 TiFlash は次のプッシュダウン式をサポートしています。

-   数学関数: `+, -, /, *, %, >=, <=, =, !=, <, >, round, abs, floor(int), ceil(int), ceiling(int), sqrt, log, log2, log10, ln, exp, pow, sign, radians, degrees, conv, crc32`
-   論理関数: `and, or, not, case when, if, ifnull, isnull, in, like, coalesce`
-   ビット演算: `bitand, bitor, bigneg, bitxor`
-   文字列関数: `substr, char_length, replace, concat, concat_ws, left, right, ascii, length, trim, ltrim, rtrim, position, format, lower, ucase, upper, substring_index, lpad, rpad, strcmp`
-   日付関数: `date_format, timestampdiff, from_unixtime, unix_timestamp(int), unix_timestamp(decimal), str_to_date(date), str_to_date(datetime), datediff, year, month, day, extract(datetime), date, hour, microsecond, minute, second, sysdate, date_add/adddate(datetime, int), date_add/adddate(string, int), date_add/adddate(string, real), date_sub/subdate(datetime, int), date_sub/subdate(string, int), date_sub/subdate(string, real), quarter`
-   JSON関数: `json_length`
-   変換関数： `cast(int as double), cast(int as decimal), cast(int as string), cast(int as time), cast(double as int), cast(double as decimal), cast(double as string), cast(double as time), cast(string as int), cast(string as double), cast(string as decimal), cast(string as time), cast(decimal as int), cast(decimal as string), cast(decimal as time), cast(time as int), cast(time as decimal), cast(time as string), cast(time as real)`
-   集計関数: `min, max, sum, count, avg, approx_count_distinct, group_concat`
-   その他の関数: `inetntoa, inetaton, inet6ntoa, inet6aton`

### その他の制限事項 {#other-restrictions}

-   Bit、Set、および Geometry タイプを含む式をTiFlashにプッシュダウンすることはできません。

-   `date_add` 、 `date_sub` 、 `adddate` 、および`subdate`関数は、次の間隔タイプのみをサポートします。他の間隔タイプが使用されている場合、 TiFlash はエラーを報告します。

    -   日
    -   週
    -   月
    -   年
    -   時間
    -   分
    -   2番

クエリでサポートされていないプッシュダウン計算が発生した場合、TiDB は残りの計算を完了する必要があり、これはTiFlashアクセラレーション効果に大きな影響を与える可能性があります。現在サポートされていない演算子と式は、将来のバージョンでサポートされる可能性があります。

## MPPモードを使用する {#use-the-mpp-mode}

TiFlash は、計算にクロスノード データ交換 (データ シャッフル プロセス) を導入するクエリの実行に MPP モードの使用をサポートします。 TiDB は、オプティマイザーのコスト推定を使用して、MPP モードを選択するかどうかを自動的に決定します。 [<a href="/system-variables.md#tidb_allow_mpp-new-in-v50">`tidb_allow_mpp`</a>](/system-variables.md#tidb_allow_mpp-new-in-v50)と[<a href="/system-variables.md#tidb_enforce_mpp-new-in-v51">`tidb_enforce_mpp`</a>](/system-variables.md#tidb_enforce_mpp-new-in-v51)の値を変更することで、選択戦略を変更できます。

### MPP モードを選択するかどうかを制御します {#control-whether-to-select-the-mpp-mode}

`tidb_allow_mpp`変数は、TiDB がクエリを実行するために MPP モードを選択できるかどうかを制御します。 `tidb_enforce_mpp`変数は、オプティマイザのコスト推定を無視し、クエリの実行にTiFlashの MPP モードを強制的に使用するかどうかを制御します。

これら 2 つの変数のすべての値に対応する結果は次のとおりです。

|                              | tidb_allow_mpp=off | tidb_allow_mpp=on (デフォルト)                 |
| ---------------------------- | ------------------ | ----------------------------------------- |
| tidb_enforce_mpp=off (デフォルト) | MPPモードは使用しません。     | オプティマイザはコスト推定に基づいて MPP モードを選択します。 (デフォルト) |
| tidb_enforce_mpp=on          | MPPモードは使用しません。     | TiDB はコスト見積もりを無視し、MPP モードを選択します。          |

たとえば、MPP モードを使用したくない場合は、次のステートメントを実行できます。

{{< copyable "" >}}

```sql
set @@session.tidb_allow_mpp=1;
set @@session.tidb_enforce_mpp=0;
```

TiDB のコストベースのオプティマイザーに MPP モード (デフォルト) を使用するかどうかを自動的に決定させたい場合は、次のステートメントを実行できます。

{{< copyable "" >}}

```sql
set @@session.tidb_allow_mpp=1;
set @@session.tidb_enforce_mpp=0;
```

TiDB にオプティマイザーのコスト推定を無視させ、強制的に MPP モードを選択させるには、次のステートメントを実行できます。

{{< copyable "" >}}

```sql
set @@session.tidb_allow_mpp=1;
set @@session.tidb_enforce_mpp=1;
```

`tidb_enforce_mpp`セッション変数の初期値は、この tidb-server インスタンスの[<a href="/tidb-configuration-file.md#enforce-mpp">`enforce-mpp`</a>](/tidb-configuration-file.md#enforce-mpp)構成値 (デフォルトでは`false` ) と同じです。 TiDB クラスター内の複数の tidb-server インスタンスが分析クエリのみを実行し、これらのインスタンスで MPP モードが使用されていることを確認したい場合は、それらの[<a href="/tidb-configuration-file.md#enforce-mpp">`enforce-mpp`</a>](/tidb-configuration-file.md#enforce-mpp)構成値を`true`に変更できます。

> **ノート：**
>
> `tidb_enforce_mpp=1`が有効になると、TiDB オプティマイザーはコスト推定を無視して MPP モードを選択します。ただし、他の要因が MPP モードをブロックする場合、TiDB は MPP モードを選択しません。これらの要因には、 TiFlashレプリカの欠如、 TiFlashレプリカの未完了のレプリケーション、MPP モードでサポートされていない演算子または関数を含むステートメントが含まれます。
>
> TiDB オプティマイザーがコスト見積もり以外の理由で MPP モードを選択できない場合、 `EXPLAIN`ステートメントを使用して実行プランをチェックアウトすると、理由を説明する警告が返されます。例えば：
>
> {{< copyable "" >}}
>
> ```sql
> set @@session.tidb_enforce_mpp=1;
> create table t(a int);
> explain select count(*) from t;
> show warnings;
> ```
>
> ```
> +---------+------+-----------------------------------------------------------------------------+
> | Level   | Code | Message                                                                     |
> +---------+------+-----------------------------------------------------------------------------+
> | Warning | 1105 | MPP mode may be blocked because there aren't tiflash replicas of table `t`. |
> +---------+------+-----------------------------------------------------------------------------+
> ```

### MPP モードのアルゴリズムのサポート {#algorithm-support-for-the-mpp-mode}

MPP モードは、ブロードキャスト ハッシュ結合、シャッフル ハッシュ結合、シャッフル ハッシュ集計、Union All、TopN、および Limit の物理アルゴリズムをサポートします。オプティマイザは、クエリでどのアルゴリズムを使用するかを自動的に決定します。特定のクエリ実行プランを確認するには、 `EXPLAIN`ステートメントを実行します。 `EXPLAIN`ステートメントの結果に ExchangeSender 演算子と ExchangeReceiver 演算子が表示される場合は、MPP モードが有効になっていることを示します。

次のステートメントでは、例として TPC-H テスト セットのテーブル構造を取り上げます。

```sql
explain select count(*) from customer c join nation n on c.c_nationkey=n.n_nationkey;
+------------------------------------------+------------+-------------------+---------------+----------------------------------------------------------------------------+
| id                                       | estRows    | task              | access object | operator info                                                              |
+------------------------------------------+------------+-------------------+---------------+----------------------------------------------------------------------------+
| HashAgg_23                               | 1.00       | root              |               | funcs:count(Column#16)->Column#15                                          |
| └─TableReader_25                         | 1.00       | root              |               | data:ExchangeSender_24                                                     |
|   └─ExchangeSender_24                    | 1.00       | batchCop[tiflash] |               | ExchangeType: PassThrough                                                  |
|     └─HashAgg_12                         | 1.00       | batchCop[tiflash] |               | funcs:count(1)->Column#16                                                  |
|       └─HashJoin_17                      | 3000000.00 | batchCop[tiflash] |               | inner join, equal:[eq(tpch.nation.n_nationkey, tpch.customer.c_nationkey)] |
|         ├─ExchangeReceiver_21(Build)     | 25.00      | batchCop[tiflash] |               |                                                                            |
|         │ └─ExchangeSender_20            | 25.00      | batchCop[tiflash] |               | ExchangeType: Broadcast                                                    |
|         │   └─TableFullScan_18           | 25.00      | batchCop[tiflash] | table:n       | keep order:false                                                           |
|         └─TableFullScan_22(Probe)        | 3000000.00 | batchCop[tiflash] | table:c       | keep order:false                                                           |
+------------------------------------------+------------+-------------------+---------------+----------------------------------------------------------------------------+
9 rows in set (0.00 sec)
```

実行プランの例には、 `ExchangeReceiver`と`ExchangeSender`演算子が含まれています。実行計画は、 `nation`テーブルが読み取られた後、 `ExchangeSender`オペレーターがテーブルを各ノードにブロードキャストし、 `HashJoin`と`HashAgg`操作が`nation`テーブルと`customer`テーブルに対して実行され、結果が TiDB に返されることを示しています。

TiFlash は、ブロードキャスト ハッシュ結合を使用するかどうかを制御するために、次の 2 つのグローバル/セッション変数を提供します。

-   [<a href="/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50">`tidb_broadcast_join_threshold_size`</a>](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50) : 値の単位はバイトです。テーブル サイズ (バイト単位) が変数の値より小さい場合は、ブロードキャスト ハッシュ結合アルゴリズムが使用されます。それ以外の場合は、シャッフル ハッシュ結合アルゴリズムが使用されます。
-   [<a href="/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50">`tidb_broadcast_join_threshold_count`</a>](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50) : 値の単位は行です。結合操作のオブジェクトがサブクエリに属している場合、オプティマイザはサブクエリの結果セットのサイズを推定できないため、サイズは結果セット内の行数によって決まります。サブクエリ内の推定行数がこの変数の値より小さい場合は、ブロードキャスト ハッシュ結合アルゴリズムが使用されます。それ以外の場合は、シャッフル ハッシュ結合アルゴリズムが使用されます。

### MPP の既知の問題 {#known-issues-of-mpp}

現在のバージョンでは、 TiFlash はクエリの一意のキーとしてクエリの`start_ts`使用します。ほとんどの場合、各クエリの`start_ts`でクエリを一意に識別できますが、次の場合、異なるクエリに同じ`start_ts`が含まれます。

-   同じトランザクション内のすべてのクエリは同じ`start_ts`を持ちます。
-   [<a href="/system-variables.md#tidb_snapshot">`tidb_snapshot`</a>](/system-variables.md#tidb_snapshot)を使用して特定の履歴時点のデータを読み取る場合、同じ時点が手動で指定されます。
-   [<a href="/stale-read.md">ステイル読み取り</a>](/stale-read.md)を有効にすると、同じ時点を手動で指定します。

`start_ts`が MPP クエリを一意に表すことができない場合、特定の時点で異なるクエリが同じ`start_ts`を持つことをTiFlashが検出すると、 TiFlash はエラーを報告する可能性があります。典型的なエラーのケースは次のとおりです。

-   同じ`start_ts`を持つ複数のクエリが同時にTiFlashに送信されると、 `task has been registered`エラーが発生する可能性があります。
-   同じトランザクション内で`LIMIT`単純なクエリが複数連続して実行される場合、 `LIMIT`条件が満たされると、TiDB はTiFlashにキャンセル リクエストを送信してクエリをキャンセルします。このリクエストでは、キャンセルするクエリを識別するために`start_ts`も使用します。 TiFlashに同じ`start_ts`を持つ他のクエリがある場合、これらのクエリは誤ってキャンセルされる可能性があります。この問題の例は[<a href="https://github.com/pingcap/tidb/issues/43426">#43426</a>](https://github.com/pingcap/tidb/issues/43426)にあります。

この問題は TiDB v6.6.0 で修正されています。 [<a href="https://docs.pingcap.com/tidb/stable">最新のLTSバージョン</a>](https://docs.pingcap.com/tidb/stable)を使用することをお勧めします。

## データ検証 {#data-validation}

### ユーザーシナリオ {#user-scenarios}

データ破損は通常、重大なハードウェア障害によって引き起こされます。このような場合、手動でデータを回復しようとしても、データの信頼性が低くなります。

データの整合性を確保するために、 TiFlash はデフォルトで`City128`アルゴリズムを使用してデータ ファイルの基本的なデータ検証を実行します。データ検証に失敗した場合、 TiFlash はただちにエラーを報告して終了し、データの不整合によって引き起こされる二次災害を回避します。現時点では、 TiFlashノードを復元する前に、手動で介入してデータを再度複製する必要があります。

v5.4.0 以降、 TiFlash には、より高度なデータ検証機能が導入されています。 TiFlash はデフォルトで`XXH3`アルゴリズムを使用し、検証フレームとアルゴリズムをカスタマイズできます。

### 検証メカニズム {#validation-mechanism}

検証メカニズムは、DeltaTree ファイル (DTFile) に基づいて構築されています。 DTFile は、 TiFlashデータを保存するstorageファイルです。 DTFile には 3 つの形式があります。

| バージョン | 州        | 検証メカニズム                                                     | ノート                             |
| :---- | :------- | :---------------------------------------------------------- | :------------------------------ |
| V1    | 廃止されました  | ハッシュはデータ ファイルに埋め込まれます。                                      |                                 |
| V2    | デフォルト    | ハッシュはデータ ファイルに埋め込まれます。                                      | V1 と比較して、V2 では列データの統計が追加されています。 |
| V3    | 手動で有効にする | V3 にはメタデータとトークン データのチェックサムが含まれており、複数のハッシュ アルゴリズムをサポートしています。 | v5.4.0 の新機能。                    |

DTFile はデータファイルディレクトリ内の`stable`フォルダに保存されます。現在有効な形式はすべてフォルダー形式です。つまり、データは`dmf_<file id>`のような名前のフォルダーの下に複数のファイルに保存されます。

#### データ検証を使用する {#use-data-validation}

TiFlash は、自動データ検証と手動データ検証の両方をサポートしています。

-   自動データ検証:
    -   TiFlash は、デフォルトで V2 検証メカニズムを有効にします。
    -   V3 検証メカニズムを有効にするには、 [<a href="/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file">TiFlash設定ファイル</a>](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)を参照してください。
-   手動データ検証。 [<a href="/tiflash/tiflash-command-line-flags.md#dttool-inspect">`DTTool inspect`</a>](/tiflash/tiflash-command-line-flags.md#dttool-inspect)を参照してください。

> **警告：**
>
> V3 検証メカニズムを有効にすると、新しく生成された DTFile は、v5.4.0 より前のTiFlashで直接読み取ることができなくなります。 v5.4.0 以降、 TiFlash はV2 と V3 の両方をサポートし、バージョンを積極的にアップグレードまたはダウングレードしません。既存のファイルのバージョンをアップグレードまたはダウングレードする必要がある場合は、手動で行う必要があります[<a href="/tiflash/tiflash-command-line-flags.md#dttool-migrate">バージョンを切り替える</a>](/tiflash/tiflash-command-line-flags.md#dttool-migrate) 。

#### 検証ツール {#validation-tool}

TiFlash がデータを読み取るときに実行される自動データ検証に加えて、データの整合性を手動でチェックするツールが v5.4.0 で導入されました。詳細は[<a href="/tiflash/tiflash-command-line-flags.md#dttool-inspect">DTツール</a>](/tiflash/tiflash-command-line-flags.md#dttool-inspect)を参照してください。

## ノート {#notes}

TiFlash は、次の状況では TiDB と互換性がありません。

-   TiFlash計算レイヤー内:
    -   オーバーフローした数値のチェックはサポートされていません。たとえば、 `BIGINT`の 2 つの最大値を加算すると、 `9223372036854775807 + 9223372036854775807` 。 TiDB でのこの計算の予期される動作は、 `ERROR 1690 (22003): BIGINT value is out of range`エラーを返すことです。ただし、この計算がTiFlashで実行される場合、エラーなしでオーバーフロー値`-2`が返されます。
    -   ウィンドウ機能はサポートされていません。
    -   TiKV からのデータの読み取りはサポートされていません。
    -   現在、 TiFlashの`sum`関数は文字列型の引数をサポートしていません。ただし、TiDB はコンパイル中に文字列型の引数が`sum`関数に渡されたかどうかを識別できません。したがって、 `select sum(string_col) from t`のようなステートメントを実行すると、 TiFlash は`[FLASH:Coprocessor:Unimplemented] CastStringAsReal is not supported.`エラーを返します。この場合にこのようなエラーを回避するには、この SQL ステートメントを`select sum(cast(string_col as double)) from t`に変更する必要があります。
    -   現在、TiFlash の小数除算計算は TiDB のものと互換性がありません。たとえば、10 進数を除算する場合、 TiFlash は常にコンパイルから推測される型を使用して計算を実行します。ただし、TiDB は、コンパイルから推測される型よりも正確な型を使用してこの計算を実行します。したがって、小数除算を含む一部の SQL ステートメントは、 TiDB + TiKV と TiDB + TiFlashで実行すると異なる実行結果を返します。例えば：

        ```sql
        mysql> create table t (a decimal(3,0), b decimal(10, 0));
        Query OK, 0 rows affected (0.07 sec)
        mysql> insert into t values (43, 1044774912);
        Query OK, 1 row affected (0.03 sec)
        mysql> alter table t set tiflash replica 1;
        Query OK, 0 rows affected (0.07 sec)
        mysql> set session tidb_isolation_read_engines='tikv';
        Query OK, 0 rows affected (0.00 sec)
        mysql> select a/b, a/b + 0.0000000000001 from t where a/b;
        +--------+-----------------------+
        | a/b    | a/b + 0.0000000000001 |
        +--------+-----------------------+
        | 0.0000 |       0.0000000410001 |
        +--------+-----------------------+
        1 row in set (0.00 sec)
        mysql> set session tidb_isolation_read_engines='tiflash';
        Query OK, 0 rows affected (0.00 sec)
        mysql> select a/b, a/b + 0.0000000000001 from t where a/b;
        Empty set (0.01 sec)
        ```

        上の例では、コンパイルから推測される`a/b`の型は、 TiDB とTiFlashの両方で`Decimal(7,4)`です。 `Decimal(7,4)`による制約により、 `a/b`の戻り値の型は`0.0000`になる必要があります。 TiDB では、 `a/b`の実行時精度は`Decimal(7,4)`よりも高いため、元のテーブル データは`where a/b`条件によってフィルターされません。ただし、 TiFlashでは、 `a/b`の計算では結果のタイプとして`Decimal(7,4)`が使用されるため、元のテーブル データは`where a/b`条件によってフィルターされます。
