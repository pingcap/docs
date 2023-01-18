---
title: Use TiFlash
---

データのインポートから TPC-H データセットでのクエリまでのプロセス全体を体験するには、 [TiDB HTAPのクイック スタート ガイド](/quick-start-with-htap.md)を参照してください。

# TiFlashを使用する {#use-tiflash}

TiFlashが展開された後、データの複製は自動的に開始されません。レプリケートするテーブルを手動で指定する必要があります。

TiDB を使用して中規模の分析処理用のTiFlashレプリカを読み取るか、TiSpark を使用して大規模な分析処理用のTiFlashレプリカを読み取ることができます。これは、独自のニーズに基づいています。詳細については、次のセクションを参照してください。

-   [TiDB を使用してTiFlashレプリカを読み取る](#use-tidb-to-read-tiflash-replicas)
-   [TiSpark を使用してTiFlashレプリカを読み取る](#use-tispark-to-read-tiflash-replicas)

## テーブルのTiFlashレプリカを作成する {#create-tiflash-replicas-for-tables}

TiFlashが TiKV クラスターに接続された後、デフォルトではデータ複製は開始されません。 MySQL クライアント経由で DDL ステートメントを TiDB に送信して、特定のテーブルのTiFlashレプリカを作成できます。

{{< copyable "" >}}

```sql
ALTER TABLE table_name SET TIFLASH REPLICA count;
```

上記のコマンドのパラメーターは、次のように記述されます。

-   `count`はレプリカの数を示します。値が`0`の場合、レプリカは削除されます。

同じテーブルで複数の DDL ステートメントを実行する場合、最後のステートメントのみが確実に有効になります。次の例では、テーブル`tpch50`に対して 2 つの DDL ステートメントが実行されますが、2 番目のステートメント (レプリカを削除するため) のみが有効になります。

テーブルのレプリカを 2 つ作成します。

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

-   テーブル`t`が上記の DDL ステートメントによってTiFlashに複製される場合、次のステートメントを使用して作成されたテーブルも自動的にTiFlashに複製されます。

    {{< copyable "" >}}

    ```sql
    CREATE TABLE table_name like t;
    ```

-   v4.0.6 より前のバージョンでは、 TiDB Lightningを使用してデータをインポートする前にTiFlashレプリカを作成すると、データのインポートは失敗します。テーブルのTiFlashレプリカを作成する前に、テーブルにデータをインポートする必要があります。

-   TiDB とTiDB Lightningが両方とも v4.0.6 以降の場合、テーブルにTiFlashレプリカがあるかどうかに関係なく、 TiDB Lightningを使用してそのテーブルにデータをインポートできます。これにより、 TiDB Lightning手順が遅くなる可能性があることに注意してください。これは、Lightning ホストの NIC 帯域幅、 TiFlashノードの CPU とディスクの負荷、およびTiFlashレプリカの数に依存します。

-   PD スケジューリングのパフォーマンスが低下するため、1,000 を超えるテーブルを複製しないことをお勧めします。この制限は、以降のバージョンで削除されます。

-   v5.1 以降のバージョンでは、システム テーブルのレプリカの設定はサポートされなくなりました。クラスタをアップグレードする前に、関連するシステム テーブルのレプリカをクリアする必要があります。そうしないと、クラスターを新しいバージョンにアップグレードした後で、システム テーブルのレプリカ設定を変更できません。

### レプリケーションの進行状況を確認する {#check-replication-progress}

次のステートメントを使用して、特定のテーブルのTiFlashレプリカのステータスを確認できます。テーブルは`WHERE`句を使用して指定されます。 `WHERE`句を削除すると、すべてのテーブルのレプリカ ステータスがチェックされます。

{{< copyable "" >}}

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>' and TABLE_NAME = '<table_name>';
```

上記のステートメントの結果:

-   `AVAILABLE`は、このテーブルのTiFlashレプリカが使用可能かどうかを示します。 `1`は利用可能であることを意味し、 `0`は利用できないことを意味します。レプリカが利用可能になると、このステータスは変わりません。 DDL ステートメントを使用してレプリカの数を変更すると、レプリケーション ステータスが再計算されます。
-   `PROGRESS`は、レプリケーションの進行状況を意味します。値は`0.0` ～ `1.0`です。 `1`は、少なくとも 1 つのレプリカが複製されていることを意味します。

### TiFlashレプリケーションの高速化 {#speed-up-tiflash-replication}

TiFlashレプリカが追加される前に、各 TiKV インスタンスはフル テーブル スキャンを実行し、スキャンされたデータを「スナップショット」としてTiFlashに送信してレプリカを作成します。デフォルトでは、オンライン サービスへの影響を最小限に抑えるために、 TiFlashレプリカはリソースの使用量を抑えてゆっくりと追加されます。 TiKV およびTiFlashノードに予備の CPU およびディスク IO リソースがある場合は、次の手順を実行してTiFlashレプリケーションを高速化できます。

1.  TiFlash Proxy と TiKV の設定を調整して、各 TiKV とTiFlashインスタンスのスナップショット書き込み速度制限を一時的に上げます。たとえば、 TiUPを使用して構成を管理する場合、構成は次のようになります。

    ```yaml
    tikv:
      server.snap-max-write-bytes-per-sec: 300MiB  # Default to 100MiB.
    tiflash-learner:
      raftstore.snap-handle-pool-size: 10          # Default to 2. Can be adjusted to >= node's CPU num * 0.6.
      raftstore.apply-low-priority-pool-size: 10   # Default to 1. Can be adjusted to >= node's CPU num * 0.6.
      server.snap-max-write-bytes-per-sec: 300MiB  # Default to 100MiB.
    ```

    構成の変更は、 TiFlashおよび TiKV インスタンスを再起動した後に有効になります。 TiKV 構成は、 [動的構成 SQL ステートメント](https://docs.pingcap.com/tidb/stable/dynamic-config)を使用してオンラインで変更することもできます。これは、TiKV インスタンスを再起動せずにすぐに有効になります。

    ```sql
    SET CONFIG tikv `server.snap-max-write-bytes-per-sec` = '300MiB';
    ```

    前述の構成を調整した後、レプリケーション速度はグローバルに PD 制限によってまだ制限されているため、現時点では加速を観察できません。

2.  [PD Control](https://docs.pingcap.com/tidb/stable/pd-control)を使用して、新しいレプリカの速度制限を徐々に緩和します。

    デフォルトの新しいレプリカの速度制限は 30 です。これは、毎分約 30 のリージョンがTiFlashレプリカを追加することを意味します。次のコマンドを実行すると、すべてのTiFlashインスタンスの制限が 60 に調整され、元の速度の 2 倍になります。

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 60 add-peer
    ```

    > 上記のコマンドでは、 `<CLUSTER_VERSION>`を実際のクラスター バージョンに置き換え、 `<PD_ADDRESS>:2379`を任意の PD ノードのアドレスに置き換える必要があります。例えば：
    >
    > ```shell
    > tiup ctl:v6.1.1 pd -u http://192.168.1.4:2379 store limit all engine tiflash 60 add-peer
    > ```

    数分以内に、 TiFlashノードの CPU およびディスク IO リソースの使用率が大幅に増加し、 TiFlashはレプリカをより速く作成するはずです。同時に、TiKV ノードの CPU およびディスク IO リソースの使用率も増加します。

    この時点で TiKV ノードとTiFlashノードにまだ予備のリソースがあり、オンライン サービスのレイテンシーが大幅に増加しない場合は、制限をさらに緩和できます。たとえば、元の速度を 3 倍にします。

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 90 add-peer
    ```

3.  TiFlashの複製が完了したら、既定の構成に戻して、オンライン サービスへの影響を軽減します。

    次のPD Controlコマンドを実行して、デフォルトの新しいレプリカの速度制限を復元します。

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 30 add-peer
    ```

    TiUPで変更された構成をコメントアウトして、デフォルトのスナップショットの書き込み速度制限を復元します。

    ```yaml
    # tikv:
    #   server.snap-max-write-bytes-per-sec: 300MiB
    # tiflash-learner:
    #   raftstore.snap-handle-pool-size: 10
    #   raftstore.apply-low-priority-pool-size: 10
    #   server.snap-max-write-bytes-per-sec: 300MiB
    ```

### 利用可能なゾーンを設定する {#set-available-zones}

レプリカを構成するときに、災害復旧のためにTiFlashレプリカを複数のデータ センターに配布する必要がある場合は、次の手順に従って使用可能なゾーンを構成できます。

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

2.  クラスターを開始した後、レプリカを作成するときにラベルを指定します。

    {{< copyable "" >}}

    ```sql
    ALTER TABLE table_name SET TIFLASH REPLICA count LOCATION LABELS location_labels;
    ```

    例えば：

    {{< copyable "" >}}

    ```sql
    ALTER TABLE t SET TIFLASH REPLICA 2 LOCATION LABELS "zone";
    ```

3.  PD は、ラベルに基づいてレプリカをスケジュールします。この例では、PD はそれぞれテーブル`t`の 2 つのレプリカを 2 つの使用可能なゾーンにスケジュールします。 pd-ctl を使用してスケジュールを表示できます。

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

ラベルを使用してレプリカをスケジュールする方法の詳細については、 [トポロジ ラベルごとにレプリカをスケジュールする](/schedule-replicas-by-topology-labels.md) 、 [1 つの都市に展開された複数のデータ センター](/multi-data-centers-in-one-city-deployment.md) 、および[2 つの都市に配置された 3 つのデータ センター](/three-data-centers-in-two-cities-deployment.md)を参照してください。

## TiDB を使用してTiFlashレプリカを読み取る {#use-tidb-to-read-tiflash-replicas}

TiDB は、 TiFlashレプリカを読み取る 3 つの方法を提供します。エンジン構成なしでTiFlashレプリカを追加した場合、CBO (コストベースの最適化) モードがデフォルトで使用されます。

### スマートセレクション {#smart-selection}

TiFlashレプリカを含むテーブルの場合、TiDB オプティマイザは、コストの見積もりに基づいてTiFlashレプリカを使用するかどうかを自動的に決定します。 `desc`または`explain analyze`ステートメントを使用して、 TiFlashレプリカが選択されているかどうかを確認できます。例えば：

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

`cop[tiflash]`は、タスクが処理のためにTiFlashに送信されることを意味します。 TiFlashレプリカを選択していない場合は、 `analyze table`ステートメントを使用して統計を更新してから、 `explain analyze`ステートメントを使用して結果を確認できます。

テーブルにTiFlashレプリカが 1 つしかなく、関連するノードがサービスを提供できない場合、CBO モードのクエリは繰り返し再試行されることに注意してください。この状況では、エンジンを指定するか、手動ヒントを使用して TiKV レプリカからデータを読み取る必要があります。

### エンジンの分離 {#engine-isolation}

エンジンの分離とは、対応する変数を構成することにより、すべてのクエリが指定されたエンジンのレプリカを使用することを指定することです。オプションのエンジンは、「tikv」、「tidb」(一部の TiDB システム テーブルを格納し、ユーザーが積極的に使用できない TiDB の内部メモリ テーブル領域を示す)、および「tiflash」であり、次の 2 つの構成レベルがあります。

-   TiDB インスタンス レベル、つまり INSTANCE レベル。 TiDB 構成ファイルに次の構成項目を追加します。

    ```
    [isolation-read]
    engines = ["tikv", "tidb", "tiflash"]
    ```

    **INSTANCE レベルのデフォルト設定は`[&quot;tikv&quot;, &quot;tidb&quot;, &quot;tiflash&quot;]`です。**

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

    SESSION レベルのデフォルト構成は、TiDB INSTANCE レベルの構成を継承しています。

最終的なエンジン構成はセッション レベルの構成です。つまり、セッション レベルの構成がインスタンス レベルの構成をオーバーライドします。たとえば、INSTANCE レベルで「tikv」を構成し、SESSION レベルで「tiflash」を構成した場合、 TiFlashレプリカが読み取られます。最終的なエンジン構成が「tikv」および「tiflash」である場合、TiKV およびTiFlashレプリカの両方が読み取られ、オプティマイザーは実行するより適切なエンジンを自動的に選択します。

> **ノート：**
>
> [TiDB ダッシュボード](/dashboard/dashboard-intro.md)およびその他のコンポーネントは、TiDB メモリ テーブル領域に格納されているシステム テーブルを読み取る必要があるため、インスタンス レベルのエンジン構成に常に「tidb」エンジンを追加することをお勧めします。

照会されたテーブルに指定されたエンジンのレプリカがない場合 (たとえば、エンジンが「tiflash」として構成されているが、テーブルにTiFlashレプリカがない場合)、クエリはエラーを返します。

### 手動ヒント {#manual-hint}

手動ヒントは、TiDB が特定のテーブルに対して指定されたレプリカを使用するように強制することができます。手動ヒントの使用例を次に示します。

{{< copyable "" >}}

```sql
select /*+ read_from_storage(tiflash[table_name]) */ ... from table_name;
```

クエリ ステートメントでテーブルにエイリアスを設定する場合、ヒントを有効にするには、ヒントを含むステートメントでエイリアスを使用する必要があります。例えば：

{{< copyable "" >}}

```sql
select /*+ read_from_storage(tiflash[alias_a,alias_b]) */ ... from table_name_1 as alias_a, table_name_2 as alias_b where alias_a.column_1 = alias_b.column_2;
```

上記のステートメントで、 `tiflash[]`はオプティマイザーにTiFlashレプリカを読み取るように促します。 `tikv[]`を使用して、オプティマイザーに必要に応じて TiKV レプリカを読み取るように指示することもできます。ヒント構文の詳細については、 [READ_FROM_STORAGE](/optimizer-hints.md#read_from_storagetiflasht1_name--tl_name--tikvt2_name--tl_name-)を参照してください。

ヒントで指定されたテーブルに指定されたエンジンのレプリカがない場合、ヒントは無視され、警告が報告されます。また、ヒントはエンジン分離前提でのみ有効です。ヒントで指定されたエンジンがエンジン分離リストにない場合、ヒントも無視され、警告が報告されます。

> **ノート：**
>
> 5.7.7 以前のバージョンの MySQL クライアントは、デフォルトでオプティマイザ ヒントをクリアします。これらの初期バージョンでヒント構文を使用するには、クライアントを`--comments`オプション (例: `mysql -h 127.0.0.1 -P 4000 -uroot --comments` ) で起動します。

### スマートセレクション、エンジンアイソレーション、マニュアルヒントの関係 {#the-relationship-of-smart-selection-engine-isolation-and-manual-hint}

上記の 3 つのTiFlashレプリカの読み取り方法では、エンジンの分離により、エンジンの使用可能なレプリカの全体的な範囲が指定されます。この範囲内では、手動ヒントにより、よりきめ細かいステートメント レベルおよびテーブル レベルのエンジン選択が提供されます。最後に、CBO が決定を下し、指定されたエンジン リスト内のコスト見積もりに基づいてエンジンのレプリカを選択します。

> **ノート：**
>
> v4.0.3 より前では、読み取り専用ではない SQL ステートメント (たとえば、 `INSERT INTO ... SELECT` 、 `SELECT ... FOR UPDATE` 、 `UPDATE ...` 、 `DELETE ...` ) でのTiFlashレプリカからの読み取りの動作は定義されていません。 v4.0.3 以降のバージョンでは、データの正確性を保証するために、TiDB は非読み取り専用 SQL ステートメントのTiFlashレプリカを内部的に無視します。つまり、 [スマートセレクション](#smart-selection)の場合、TiDB は非TiFlashレプリカを自動的に選択します。 TiFlashレプリカ**のみ**を指定する[エンジン分離](#engine-isolation)の場合、TiDB はエラーを報告します。 [手動ヒント](#manual-hint)の場合、TiDB はヒントを無視します。

## TiSpark を使用してTiFlashレプリカを読み取る {#use-tispark-to-read-tiflash-replicas}

現在、TiSpark を使用して、TiDB のエンジン分離と同様の方法でTiFlashレプリカを読み取ることができます。このメソッドは、 `spark.tispark.isolation_read_engines`つのパラメーターを構成することです。パラメータ値のデフォルトは`tikv,tiflash`です。これは、CBO の選択に従って、TiDB がTiFlashまたは TiKV からデータを読み取ることを意味します。パラメータ値を`tiflash`に設定すると、TiDB がTiFlashから強制的にデータを読み取ることを意味します。

> **ノート：**
>
> このパラメーターが`tiflash`に設定されている場合、クエリに含まれるすべてのテーブルのTiFlashレプリカのみが読み取られ、これらのテーブルにはTiFlashレプリカが必要です。 TiFlashレプリカを持たないテーブルの場合、エラーが報告されます。このパラメーターを`tikv`に設定すると、TiKV レプリカのみが読み取られます。

このパラメーターは、次のいずれかの方法で構成できます。

-   `spark-defaults.conf`ファイルに次の項目を追加します。

    ```
    spark.tispark.isolation_read_engines tiflash
    ```

-   Spark シェルまたは Thriftサーバーを初期化するときに、初期化コマンドに`--conf spark.tispark.isolation_read_engines=tiflash`を追加します。

-   リアルタイムで Spark シェルに`spark.conf.set("spark.tispark.isolation_read_engines", "tiflash")`を設定します。

-   サーバーがビーライン経由で接続された後、Thriftサーバーに`set spark.tispark.isolation_read_engines=tiflash`を設定します。

## サポートされているプッシュダウン計算 {#supported-push-down-calculations}

TiFlashは、次の演算子のプッシュダウンをサポートしています。

-   TableScan: テーブルからデータを読み取ります。
-   選択: データをフィルタリングします。
-   HashAgg: [ハッシュ集計](/explain-aggregation.md#hash-aggregation)アルゴリズムに基づいてデータ集計を実行します。
-   StreamAgg: [ストリーム集計](/explain-aggregation.md#stream-aggregation)アルゴリズムに基づいてデータ集計を実行します。 SteamAgg は`GROUP BY`条件なしの集計のみをサポートします。
-   TopN: TopN 計算を実行します。
-   Limit: リミット計算を実行します。
-   Project: 投影計算を実行します。
-   HashJoin (Equi Join): [ハッシュ結合](/explain-joins.md#hash-join)アルゴリズムに基づいて結合計算を実行しますが、次の条件があります。
    -   オペレーターは[MPP モード](#use-the-mpp-mode)でのみ押し下げることができます。
    -   `Full Outer Join`のプッシュダウンはサポートされていません。
-   HashJoin (Non-Equi Join): 直交結合アルゴリズムを実行しますが、次の条件があります。
    -   オペレーターは[MPP モード](#use-the-mpp-mode)でのみ押し下げることができます。
    -   直交結合は、ブロードキャスト結合でのみサポートされています。

TiDB では、オペレーターはツリー構造で編成されています。オペレータがTiFlashにプッシュされるには、次のすべての前提条件を満たす必要があります。

-   その子演算子はすべてTiFlashにプッシュできます。
-   演算子に式が含まれる場合 (ほとんどの演算子には式が含まれます)、演算子のすべての式をTiFlashにプッシュできます。

現在、 TiFlashは次のプッシュダウン式をサポートしています。

-   数学関数: `+, -, /, *, %, >=, <=, =, !=, <, >, round, abs, floor(int), ceil(int), ceiling(int), sqrt, log, log2, log10, ln, exp, pow, sign, radians, degrees, conv, crc32`
-   論理関数: `and, or, not, case when, if, ifnull, isnull, in, like, coalesce`
-   ビット演算: `bitand, bitor, bigneg, bitxor`
-   文字列関数: `substr, char_length, replace, concat, concat_ws, left, right, ascii, length, trim, ltrim, rtrim, position, format, lower, ucase, upper, substring_index, lpad, rpad, strcmp`
-   日付関数： `date_format, timestampdiff, from_unixtime, unix_timestamp(int), unix_timestamp(decimal), str_to_date(date), str_to_date(datetime), datediff, year, month, day, extract(datetime), date, hour, microsecond, minute, second, sysdate, date_add/adddate(datetime, int), date_add/adddate(string, int), date_add/adddate(string, real), date_sub/subdate(datetime, int), date_sub/subdate(string, int), date_sub/subdate(string, real), quarter`
-   JSON 関数: `json_length`
-   変換関数： `cast(int as double), cast(int as decimal), cast(int as string), cast(int as time), cast(double as int), cast(double as decimal), cast(double as string), cast(double as time), cast(string as int), cast(string as double), cast(string as decimal), cast(string as time), cast(decimal as int), cast(decimal as string), cast(decimal as time), cast(time as int), cast(time as decimal), cast(time as string), cast(time as real)`
-   集計関数: `min, max, sum, count, avg, approx_count_distinct, group_concat`
-   その他の関数: `inetntoa, inetaton, inet6ntoa, inet6aton`

### その他の制限 {#other-restrictions}

-   Bit、Set、および Geometry タイプを含む式は、 TiFlashにプッシュダウンできません。

-   `date_add` 、 `date_sub` 、 `adddate` 、および`subdate`関数は、次の間隔タイプのみをサポートします。他の間隔タイプが使用されている場合、 TiFlashはエラーを報告します。

    -   日
    -   週
    -   月
    -   年
    -   時間
    -   分
    -   2番目

サポートされていないプッシュダウン計算がクエリで発生した場合、TiDB は残りの計算を完了する必要があり、 TiFlashアクセラレーション効果に大きな影響を与える可能性があります。現在サポートされていない演算子と式は、将来のバージョンでサポートされる可能性があります。

## MPP モードを使用する {#use-the-mpp-mode}

TiFlashは、MPP モードを使用してクエリを実行することをサポートしています。これにより、クロスノード データ交換 (データ シャッフル プロセス) が計算に導入されます。 TiDB は、オプティマイザのコスト見積もりを使用して、MPP モードを選択するかどうかを自動的に決定します。 [`tidb_allow_mpp`](/system-variables.md#tidb_allow_mpp-new-in-v50)と[`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-new-in-v51)の値を変更することで、選択戦略を変更できます。

### MPP モードを選択するかどうかを制御します {#control-whether-to-select-the-mpp-mode}

`tidb_allow_mpp`変数は、TiDB が MPP モードを選択してクエリを実行できるかどうかを制御します。 `tidb_enforce_mpp`変数は、オプティマイザーのコスト見積もりを無視し、 TiFlashの MPP モードを強制的に使用してクエリを実行するかどうかを制御します。

これら 2 つの変数のすべての値に対応する結果は次のとおりです。

|                              | tidb_allow_mpp=オフ | tidb_allow_mpp=on (デフォルト)                     |
| ---------------------------- | ----------------- | --------------------------------------------- |
| tidb_enforce_mpp=off (デフォルト) | MPP モードは使用されません。  | オプティマイザは、コストの見積もりに基づいて MPP モードを選択します。 (デフォルト) |
| tidb_enforce_mpp=オン          | MPP モードは使用されません。  | TiDB はコスト見積もりを無視し、MPP モードを選択します。              |

たとえば、MPP モードを使用したくない場合は、次のステートメントを実行できます。

{{< copyable "" >}}

```sql
set @@session.tidb_allow_mpp=1;
set @@session.tidb_enforce_mpp=0;
```

TiDB のコストベースのオプティマイザに、MPP モードを使用するかどうか (デフォルトで) を自動的に決定させたい場合は、次のステートメントを実行できます。

{{< copyable "" >}}

```sql
set @@session.tidb_allow_mpp=1;
set @@session.tidb_enforce_mpp=0;
```

TiDB にオプティマイザーのコスト見積もりを無視させ、MPP モードを強制的に選択させたい場合は、次のステートメントを実行できます。

{{< copyable "" >}}

```sql
set @@session.tidb_allow_mpp=1;
set @@session.tidb_enforce_mpp=1;
```

`tidb_enforce_mpp`セッション変数の初期値は、この tidb-server インスタンスの[`enforce-mpp`](/tidb-configuration-file.md#enforce-mpp)構成値 (デフォルトでは`false` ) と同じです。 TiDB クラスター内の複数の tidb-server インスタンスが分析クエリのみを実行し、これらのインスタンスで MPP モードが使用されていることを確認したい場合は、それらの[`enforce-mpp`](/tidb-configuration-file.md#enforce-mpp)の構成値を`true`に変更できます。

> **ノート：**
>
> `tidb_enforce_mpp=1`が有効になると、TiDB オプティマイザーはコスト見積もりを無視して MPP モードを選択します。ただし、他の要因が MPP モードをブロックする場合、TiDB は MPP モードを選択しません。これらの要因には、 TiFlashレプリカの不在、 TiFlashレプリカの未完成の複製、および MPP モードでサポートされていない演算子または関数を含むステートメントが含まれます。
>
> コスト見積もり以外の理由で TiDB オプティマイザーが MPP モードを選択できない場合、 `EXPLAIN`ステートメントを使用して実行計画をチェックアウトすると、その理由を説明する警告が返されます。例えば：
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

### MPP モードのアルゴリズム サポート {#algorithm-support-for-the-mpp-mode}

MPP モードは、ブロードキャスト ハッシュ結合、シャッフル ハッシュ結合、シャッフル ハッシュ集計、Union All、TopN、および Limit の物理アルゴリズムをサポートします。オプティマイザは、クエリで使用するアルゴリズムを自動的に決定します。特定のクエリ実行プランを確認するには、 `EXPLAIN`ステートメントを実行します。 `EXPLAIN`ステートメントの結果が ExchangeSender および ExchangeReceiver オペレーターを示している場合、MPP モードが有効になっていることを示します。

次のステートメントは、例として TPC-H テスト セットのテーブル構造を取ります。

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

実行計画の例では、 `ExchangeReceiver`と`ExchangeSender`の演算子が含まれています。実行計画は、 `nation`テーブルが読み取られた後、 `ExchangeSender`オペレーターがテーブルを各ノードにブロードキャストし、 `nation`テーブルと`customer`テーブルに対して`HashJoin`と`HashAgg`の操作が実行され、結果が TiDB に返されることを示しています。

TiFlashは、ブロードキャスト ハッシュ結合を使用するかどうかを制御するために、次の 2 つのグローバル/セッション変数を提供します。

-   [`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50) : 値の単位はバイトです。テーブル サイズ (バイト単位) が変数の値より小さい場合は、ブロードキャスト ハッシュ結合アルゴリズムが使用されます。それ以外の場合は、Shuffled Hash Join アルゴリズムが使用されます。
-   [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50) : 値の単位は行です。結合操作のオブジェクトがサブクエリに属している場合、オプティマイザはサブクエリの結果セットのサイズを見積もることができないため、サイズは結果セットの行数によって決定されます。サブクエリの推定行数がこの変数の値より少ない場合、ブロードキャスト ハッシュ結合アルゴリズムが使用されます。それ以外の場合は、Shuffled Hash Join アルゴリズムが使用されます。

## データ検証 {#data-validation}

### ユーザー シナリオ {#user-scenarios}

通常、データの破損は深刻なハードウェア障害によって引き起こされます。このような場合、手動でデータを回復しようとしても、データの信頼性が低下します。

データの整合性を確保するために、デフォルトでは、 TiFlashは`City128`アルゴリズムを使用して、データ ファイルに対して基本的なデータ検証を実行します。データの検証に失敗した場合、 TiFlashはすぐにエラーを報告して終了し、データの不一致による二次災害を回避します。この時点で、 TiFlashノードを復元する前に、手動で介入してデータを再度複製する必要があります。

v5.4.0 から、 TiFlashはより高度なデータ検証機能を導入しています。 TiFlashはデフォルトで`XXH3`アルゴリズムを使用し、検証フレームとアルゴリズムをカスタマイズできます。

### 検証メカニズム {#validation-mechanism}

検証メカニズムは、DeltaTree ファイル (DTFile) に基づいています。 DTFile は、 TiFlashデータを保持するストレージ ファイルです。 DTFile には次の 3 つの形式があります。

| バージョン | 州        | 検証メカニズム                                                      | ノート                         |
| :---- | :------- | :----------------------------------------------------------- | :-------------------------- |
| V1    | 非推奨      | ハッシュはデータ ファイルに埋め込まれます。                                       |                             |
| V2    | デフォルト    | ハッシュはデータ ファイルに埋め込まれます。                                       | V1 と比較して、V2 は列データの統計を追加します。 |
| V3    | 手動で有効にする | V3 には、メタデータとトークン データのチェックサムが含まれており、複数のハッシュ アルゴリズムをサポートしています。 | v5.4.0 の新機能。                |

DTFile はデータファイルディレクトリの`stable`フォルダに格納されています。現在有効になっている形式はすべてフォルダー形式です。つまり、データは`dmf_<file id>`のような名前のフォルダーの下にある複数のファイルに保存されます。

#### データ検証を使用する {#use-data-validation}

TiFlashは、自動データ検証と手動データ検証の両方をサポートしています。

-   自動データ検証:
    -   TiFlashは、デフォルトで V2 検証メカニズムを有効にします。
    -   V3 検証メカニズムを有効にするには、 [TiFlash構成ファイル](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)を参照してください。
-   手動データ検証。 [`DTTool inspect`](/tiflash/tiflash-command-line-flags.md#dttool-inspect)を参照してください。

> **警告：**
>
> V3 検証メカニズムを有効にすると、新しく生成された DTFile をTiFlashで直接読み取ることができなくなります。 v5.4.0 以降、 TiFlashは V2 と V3 の両方をサポートし、積極的にバージョンをアップグレードまたはダウングレードしません。既存のファイルのバージョンをアップグレードまたはダウングレードする必要がある場合は、手動で行う必要があります[バージョンを切り替える](/tiflash/tiflash-command-line-flags.md#dttool-migrate) 。

#### 検証ツール {#validation-tool}

TiFlashがデータを読み取るときに実行される自動データ検証に加えて、データの整合性を手動でチェックするツールが v5.4.0 で導入されました。詳細については、 [DTツール](/tiflash/tiflash-command-line-flags.md#dttool-inspect)を参照してください。

## ノート {#notes}

次の状況では、 TiFlashと互換性がありません。

-   TiFlash計算レイヤーでは:
    -   オーバーフローした数値のチェックはサポートされていません。たとえば、 `BIGINT`タイプ`9223372036854775807 + 9223372036854775807`の 2 つの最大値を加算します。 TiDB でのこの計算の予想される動作は、 `ERROR 1690 (22003): BIGINT value is out of range`エラーを返すことです。ただし、この計算をTiFlashで実行すると、オーバーフロー値`-2`がエラーなしで返されます。
    -   ウィンドウ関数はサポートされていません。
    -   TiKV からのデータの読み取りはサポートされていません。
    -   現在、 TiFlashの`sum`関数は文字列型の引数をサポートしていません。しかし、TiDB は、コンパイル中に文字列型の引数が`sum`関数に渡されたかどうかを識別できません。したがって、 `select sum(string_col) from t`のようなステートメントを実行すると、 TiFlashは`[FLASH:Coprocessor:Unimplemented] CastStringAsReal is not supported.`エラーを返します。このようなエラーを回避するには、この SQL ステートメントを`select sum(cast(string_col as double)) from t`に変更する必要があります。
    -   現在、TiFlash の 10 進数除算の計算は TiDB のそれと互換性がありません。たとえば、10 進数を除算する場合、 TiFlashは常にコンパイルから推測された型を使用して計算を実行します。ただし、TiDB は、コンパイルから推測される型よりも正確な型を使用して、この計算を実行します。そのため、10 進数除算を含む一部の SQL ステートメントは、TiDB + TiKV と TiDB + TiFlashで実行した場合に異なる実行結果を返します。例えば：

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

        上記の例では、コンパイルから推測される`a/b`の型は、TiDB とTiFlashの両方で`Decimal(7,4)`です。 `Decimal(7,4)`によって制約され、 `a/b`の返される型は`0.0000`である必要があります。 TiDB では、 `a/b`の実行時の精度が`Decimal(7,4)`よりも高いため、元のテーブル データは`where a/b`の条件によってフィルター処理されません。ただし、 TiFlashでは、 `a/b`の計算は`Decimal(7,4)`を結果の型として使用するため、元のテーブル データは`where a/b`の条件でフィルター処理されます。
