---
title: Create TiFlash Replicas
summary: Learn how to create TiFlash replicas.
---

# TiFlashレプリカの作成 {#create-tiflash-replicas}

このドキュメントでは、テーブルとデータベースのTiFlashレプリカを作成し、レプリカのスケジュールに使用できるゾーンを設定する方法を紹介します。

## テーブルのTiFlashレプリカを作成する {#create-tiflash-replicas-for-tables}

TiFlashが TiKV クラスターに接続された後、デフォルトではデータ複製は開始されません。 MySQL クライアント経由で DDL ステートメントを TiDB に送信して、特定のテーブルのTiFlashレプリカを作成できます。

{{< copyable "" >}}

```sql
ALTER TABLE table_name SET TIFLASH REPLICA count;
```

上記のコマンドのパラメーターは、次のように記述されます。

-   `count`レプリカの数を示します。値が`0`の場合、レプリカは削除されます。

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

-   v4.0.6 より前のバージョンでは、 TiDB Lightning を使用してデータをインポートする前にTiFlashレプリカを作成すると、データのインポートは失敗します。テーブルのTiFlashレプリカを作成する前に、テーブルにデータをインポートする必要があります。

-   TiDB とTiDB Lightning が両方とも v4.0.6 以降の場合、テーブルにTiFlashレプリカがあるかどうかに関係なく、 TiDB Lightningを使用してそのテーブルにデータをインポートできます。これにより、 TiDB Lightning手順が遅くなる可能性があることに注意してください。これは、Lightning ホストの NIC 帯域幅、 TiFlashノードの CPU とディスクの負荷、およびTiFlashレプリカの数に依存します。

-   PD スケジューリングのパフォーマンスが低下するため、1,000 を超えるテーブルを複製しないことをお勧めします。この制限は、以降のバージョンで削除されます。

-   v5.1 以降のバージョンでは、システム テーブルのレプリカの設定はサポートされなくなりました。クラスタをアップグレードする前に、関連するシステム テーブルのレプリカをクリアする必要があります。そうしないと、クラスターを新しいバージョンにアップグレードした後で、システム テーブルのレプリカ設定を変更できません。

### レプリケーションの進行状況を確認する {#check-replication-progress}

次のステートメントを使用して、特定のテーブルのTiFlashレプリカのステータスを確認できます。テーブルは`WHERE`句を使用して指定されます。 `WHERE`句を削除すると、すべてのテーブルのレプリカ ステータスがチェックされます。

{{< copyable "" >}}

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>' and TABLE_NAME = '<table_name>';
```

上記のステートメントの結果:

-   `AVAILABLE` 、このテーブルのTiFlashレプリカが使用可能かどうかを示します。 `1`利用可能であることを意味し、 `0`利用できないことを意味します。レプリカが利用可能になると、このステータスは変わりません。 DDL ステートメントを使用してレプリカの数を変更すると、レプリケーション ステータスが再計算されます。
-   `PROGRESS`レプリケーションの進行状況を意味します。値は`0.0` ～ `1.0`です。 `1`少なくとも 1 つのレプリカが複製されていることを意味します。

## データベースのTiFlashレプリカを作成する {#create-tiflash-replicas-for-databases}

テーブルのTiFlashレプリカを作成するのと同様に、MySQL クライアントを介して TiDB に DDL ステートメントを送信し、特定のデータベース内のすべてのテーブルのTiFlashレプリカを作成できます。

{{< copyable "" >}}

```sql
ALTER DATABASE db_name SET TIFLASH REPLICA count;
```

このステートメントでは、 `count`レプリカの数を示します。 `0`に設定すると、レプリカが削除されます。

例:

-   データベース`tpch50`内のすべてのテーブルに対して 2 つのレプリカを作成します。

    {{< copyable "" >}}

    ```sql
    ALTER DATABASE `tpch50` SET TIFLASH REPLICA 2;
    ```

-   データベース`tpch50`用に作成されたTiFlashレプリカを削除します。

    {{< copyable "" >}}

    ```sql
    ALTER DATABASE `tpch50` SET TIFLASH REPLICA 0;
    ```

> **ノート：**
>
> -   このステートメントは、リソースを集中的に使用する一連の DDL 操作を実際に実行します。実行中にステートメントが中断された場合、実行された操作はロールバックされず、実行されていない操作は続行されません。
>
> -   ステートメントを実行した後、**このデータベース内のすべてのテーブルがレプリケートされる**まで、 TiFlashレプリカの数を設定したり、このデータベースで DDL 操作を実行したりしないでください。そうしないと、次のような予期しない結果が発生する可能性があります。
>     -   TiFlashレプリカの数を 2 に設定し、データベース内のすべてのテーブルが複製される前に数を 1 に変更した場合、すべてのテーブルのTiFlashレプリカの最終的な数は必ずしも 1 または 2 とは限りません。
>     -   ステートメントの実行後、ステートメントの実行が完了する前にこのデータベースにテーブルを作成すると、これらの新しいテーブルに対してTiFlashレプリカが作成される**場合と作成されない場合があります**。
>     -   ステートメントの実行後、ステートメントの実行が完了する前にデータベース内のテーブルのインデックスを追加すると、ステートメントがハングし、インデックスが追加された後にのみ再開される場合があります。
>
> -   このステートメントは、システム テーブル、ビュー、一時テーブル、およびTiFlashでサポートされていない文字セットを含むテーブルをスキップします。

### レプリケーションの進行状況を確認する {#check-replication-progress}

テーブルのTiFlashレプリカの作成と同様に、DDL ステートメントの実行が成功しても、レプリケーションが完了するわけではありません。次の SQL ステートメントを実行して、ターゲット テーブルでのレプリケーションの進行状況を確認できます。

{{< copyable "" >}}

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>';
```

データベースにTiFlashレプリカがないテーブルをチェックするには、次の SQL ステートメントを実行します。

{{< copyable "" >}}

```sql
SELECT TABLE_NAME FROM information_schema.tables where TABLE_SCHEMA = "<db_name>" and TABLE_NAME not in (SELECT TABLE_NAME FROM information_schema.tiflash_replica where TABLE_SCHEMA = "<db_name>");
```

## TiFlashレプリケーションの高速化 {#speed-up-tiflash-replication}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> このセクションはTiDB Cloudには適用されません。

</CustomContent>

TiFlashレプリカが追加される前に、各 TiKV インスタンスはフル テーブル スキャンを実行し、スキャンされたデータを「スナップショット」としてTiFlashに送信してレプリカを作成します。デフォルトでは、オンライン サービスへの影響を最小限に抑えるために、 TiFlashレプリカはリソースの使用量を抑えてゆっくりと追加されます。 TiKV およびTiFlashノードに予備の CPU およびディスク IO リソースがある場合は、次の手順を実行してTiFlashレプリケーションを高速化できます。

1.  [動的構成 SQL ステートメント](https://docs.pingcap.com/tidb/stable/dynamic-config)を使用して、各 TiKV およびTiFlashインスタンスのスナップショット書き込み速度制限を一時的に上げます。

    ```sql
    -- The default value for both configurations are 100MiB, i.e. the maximum disk bandwidth used for writing snapshots is no more than 100MiB/s.
    SET CONFIG tikv `server.snap-max-write-bytes-per-sec` = '300MiB';
    SET CONFIG tiflash `raftstore-proxy.server.snap-max-write-bytes-per-sec` = '300MiB';
    ```

    これらの SQL ステートメントを実行すると、クラスターを再起動しなくても、構成の変更がすぐに有効になります。ただし、レプリケーション速度は依然としてグローバルに PD 制限によって制限されているため、現時点では加速を観察できません。

2.  [PD Control](https://docs.pingcap.com/tidb/stable/pd-control)使用して、新しいレプリカの速度制限を徐々に緩和します。

    デフォルトの新しいレプリカの速度制限は 30 です。これは、毎分約 30 のリージョンがTiFlashレプリカを追加することを意味します。次のコマンドを実行すると、すべてのTiFlashインスタンスの制限が 60 に調整され、元の速度の 2 倍になります。

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 60 add-peer
    ```

    > 上記のコマンドでは、 `v<CLUSTER_VERSION>`実際のクラスター バージョンに置き換える必要があります。たとえば、 `v6.5.2`や`<PD_ADDRESS>:2379`を任意の PD ノードのアドレスに置き換える必要があります。例えば：
    >
    > ```shell
    > tiup ctl:v6.1.1 pd -u http://192.168.1.4:2379 store limit all engine tiflash 60 add-peer
    > ```

    数分以内に、 TiFlashノードの CPU およびディスク IO リソースの使用率が大幅に増加し、 TiFlash はレプリカをより速く作成するはずです。同時に、TiKV ノードの CPU およびディスク IO リソースの使用率も増加します。

    この時点で TiKV ノードとTiFlashノードにまだ予備のリソースがあり、オンライン サービスのレイテンシーが大幅に増加しない場合は、制限をさらに緩和できます。たとえば、元の速度を 3 倍にします。

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 90 add-peer
    ```

3.  TiFlashの複製が完了したら、既定の構成に戻して、オンライン サービスへの影響を軽減します。

    次のPD Controlコマンドを実行して、デフォルトの新しいレプリカの速度制限を復元します。

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 30 add-peer
    ```

    次の SQL ステートメントを実行して、デフォルトのスナップショットの書き込み速度制限を復元します。

    ```sql
    SET CONFIG tikv `server.snap-max-write-bytes-per-sec` = '100MiB';
    SET CONFIG tiflash `raftstore-proxy.server.snap-max-write-bytes-per-sec` = '100MiB';
    ```

## 利用可能なゾーンを設定する {#set-available-zones}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> このセクションはTiDB Cloudには適用されません。

</CustomContent>

レプリカを構成するときに、災害復旧のためにTiFlashレプリカを複数のデータ センターに配布する必要がある場合は、次の手順に従って使用可能なゾーンを構成できます。

1.  クラスター構成ファイルでTiFlashノードのラベルを指定します。

    ```
    tiflash_servers:
      - host: 172.16.5.81
          logger.level: "info"
        learner_config:
          server.labels:
            zone: "z1"
      - host: 172.16.5.82
        config:
          logger.level: "info"
        learner_config:
          server.labels:
            zone: "z1"
      - host: 172.16.5.85
        config:
          logger.level: "info"
        learner_config:
          server.labels:
            zone: "z2"
    ```

    以前のバージョンの`flash.proxy.labels`構成では、使用可能なゾーン名の特殊文字を正しく処理できないことに注意してください。 `server.labels` in `learner_config`を使用して、使用可能なゾーンの名前を構成することをお勧めします。

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

<CustomContent platform="tidb">

ラベルを使用してレプリカをスケジュールする方法の詳細については、 [トポロジ ラベルごとにレプリカをスケジュールする](/schedule-replicas-by-topology-labels.md) 、 [1 つの地域展開における複数のデータセンター](/multi-data-centers-in-one-city-deployment.md) 、および[2 つの地域に配置された 3 つのデータ センター](/three-data-centers-in-two-cities-deployment.md)を参照してください。

</CustomContent>
