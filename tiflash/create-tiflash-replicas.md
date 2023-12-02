---
title: Create TiFlash Replicas
summary: Learn how to create TiFlash replicas.
---

# TiFlashレプリカの作成 {#create-tiflash-replicas}

このドキュメントでは、テーブルとデータベースのTiFlashレプリカを作成し、レプリカのスケジュール設定に使用可能なゾーンを設定する方法を紹介します。

## テーブルのTiFlashレプリカを作成する {#create-tiflash-replicas-for-tables}

TiFlashが TiKV クラスターに接続された後、デフォルトではデータ レプリケーションは開始されません。 MySQL クライアントを通じて DDL ステートメントを TiDB に送信して、特定のテーブルのTiFlashレプリカを作成できます。

```sql
ALTER TABLE table_name SET TIFLASH REPLICA count;
```

上記コマンドのパラメータは次のように記述されます。

-   `count`レプリカの数を示します。値が`0`の場合、レプリカは削除されます。

同じテーブルに対して複数の DDL ステートメントを実行すると、最後のステートメントのみが有効になります。次の例では、テーブル`tpch50`に対して 2 つの DDL ステートメントが実行されますが、有効になるのは 2 番目のステートメント (レプリカを削除する) だけです。

テーブルの 2 つのレプリカを作成します。

```sql
ALTER TABLE `tpch50`.`lineitem` SET TIFLASH REPLICA 2;
```

レプリカを削除します。

```sql
ALTER TABLE `tpch50`.`lineitem` SET TIFLASH REPLICA 0;
```

**ノート：**

-   上記の DDL ステートメントを通じてテーブル`t`がTiFlashにレプリケートされる場合、次のステートメントを使用して作成されたテーブルも自動的にTiFlashにレプリケートされます。

    ```sql
    CREATE TABLE table_name like t;
    ```

-   v4.0.6 より前のバージョンの場合、 TiDB Lightning を使用してデータをインポートする前にTiFlashレプリカを作成すると、データのインポートは失敗します。テーブルのTiFlashレプリカを作成する前に、テーブルにデータをインポートする必要があります。

-   TiDB とTiDB Lightning が両方とも v4.0.6 以降の場合、テーブルにTiFlashレプリカがあるかどうかに関係なく、 TiDB Lightningを使用してそのテーブルにデータをインポートできます。これにより、 TiDB Lightning の手順が遅くなる可能性があることに注意してください。これは、Lightning ホストの NIC 帯域幅、 TiFlashノードの CPU とディスクの負荷、 TiFlashレプリカの数によって異なります。

-   PD スケジュールのパフォーマンスが低下するため、1,000 を超えるテーブルを複製しないことをお勧めします。この制限は、後のバージョンでは削除される予定です。

-   v5.1 以降のバージョンでは、システム テーブルのレプリカの設定はサポートされなくなりました。クラスターをアップグレードする前に、関連するシステム テーブルのレプリカをクリアする必要があります。そうしないと、クラスターを新しいバージョンにアップグレードした後にシステム テーブルのレプリカ設定を変更できません。

### レプリケーションの進行状況を確認する {#check-replication-progress}

次のステートメントを使用して、特定のテーブルのTiFlashレプリカのステータスを確認できます。テーブルは`WHERE`句を使用して指定されます。 `WHERE`句を削除すると、すべてのテーブルのレプリカのステータスがチェックされます。

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>' and TABLE_NAME = '<table_name>';
```

上記のステートメントの結果は次のようになります。

-   `AVAILABLE` 、このテーブルのTiFlashレプリカが使用可能かどうかを示します。 `1`使用可能を意味し、 `0`使用不可を意味します。レプリカが使用可能になると、このステータスは変わりません。 DDL ステートメントを使用してレプリカの数を変更すると、レプリケーションのステータスが再計算されます。
-   `PROGRESS`レプリケーションの進行状況を意味します。値は`0.0` ～ `1.0`です。 `1`少なくとも 1 つのレプリカが複製されていることを意味します。

## データベースのTiFlashレプリカを作成する {#create-tiflash-replicas-for-databases}

テーブルのTiFlashレプリカを作成するのと同様に、MySQL クライアントを通じて DDL ステートメントを TiDB に送信して、特定のデータベース内のすべてのテーブルのTiFlashレプリカを作成できます。

```sql
ALTER DATABASE db_name SET TIFLASH REPLICA count;
```

このステートメントでは、 `count`レプリカの数を示します。 `0`に設定すると、レプリカが削除されます。

例:

-   データベース内のすべてのテーブルに対して 2 つのレプリカを作成します`tpch50` :

    ```sql
    ALTER DATABASE `tpch50` SET TIFLASH REPLICA 2;
    ```

-   データベース`tpch50`用に作成されたTiFlashレプリカを削除します。

    ```sql
    ALTER DATABASE `tpch50` SET TIFLASH REPLICA 0;
    ```

> **注記：**
>
> -   このステートメントは実際に、リソースを大量に消費する一連の DDL 操作を実行します。実行中にステートメントが中断された場合、実行された操作はロールバックされず、未実行の操作は続行されません。
>
> -   ステートメントの実行後は、**このデータベース内のすべてのテーブルが複製される**まで、 TiFlashレプリカの数を設定したり、このデータベースに対して DDL 操作を実行したりしないでください。そうしないと、次のような予期しない結果が発生する可能性があります。
>     -   TiFlashレプリカの数を 2 に設定し、データベース内のすべてのテーブルがレプリケートされる前にその数を 1 に変更した場合、すべてのテーブルのTiFlashレプリカの最終的な数は必ずしも 1 または 2 になるとは限りません。
>     -   ステートメントの実行後、ステートメントの実行が完了する前にこのデータベースにテーブルを作成すると、これらの新しいテーブルに対してTiFlashレプリカが作成される**場合と作成されない場合があります**。
>     -   ステートメントの実行後、ステートメントの実行が完了する前にデータベース内のテーブルのインデックスを追加すると、ステートメントがハングし、インデックスの追加後にのみ再開される可能性があります。
>
> -   ステートメントの実行完了**後に**このデータベースにテーブルを作成した場合、これらの新しいテーブルに対してTiFlashレプリカは自動的に作成されません。
>
> -   このステートメントは、システム テーブル、ビュー、一時テーブル、およびTiFlashでサポートされていない文字セットを含むテーブルをスキップします。

### レプリケーションの進行状況を確認する {#check-replication-progress}

テーブルのTiFlashレプリカの作成と同様、DDL ステートメントの実行が成功しても、レプリケーションが完了するわけではありません。次の SQL ステートメントを実行して、ターゲット テーブルでのレプリケーションの進行状況を確認できます。

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>';
```

データベース内にTiFlashレプリカがないテーブルをチェックするには、次の SQL ステートメントを実行できます。

```sql
SELECT TABLE_NAME FROM information_schema.tables where TABLE_SCHEMA = "<db_name>" and TABLE_NAME not in (SELECT TABLE_NAME FROM information_schema.tiflash_replica where TABLE_SCHEMA = "<db_name>");
```

## TiFlashレプリケーションを高速化する {#speed-up-tiflash-replication}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> このセクションはTiDB Cloudには適用されません。

</CustomContent>

TiFlashレプリカが追加される前に、各 TiKV インスタンスはフル テーブル スキャンを実行し、スキャンされたデータを「スナップショット」としてTiFlashに送信してレプリカを作成します。デフォルトでは、オンライン サービスへの影響を最小限に抑えるために、 TiFlashレプリカはリソース使用量を減らしてゆっくり追加されます。 TiKV ノードとTiFlashノードに予備の CPU とディスク IO リソースがある場合は、次の手順を実行してTiFlashレプリケーションを高速化できます。

1.  [動的構成 SQL ステートメント](https://docs.pingcap.com/tidb/stable/dynamic-config)を使用して、各 TiKV およびTiFlashインスタンスのスナップショット書き込み速度制限を一時的に増加します。

    ```sql
    -- The default value for both configurations are 100MiB, i.e. the maximum disk bandwidth used for writing snapshots is no more than 100MiB/s.
    SET CONFIG tikv `server.snap-io-max-bytes-per-sec` = '300MiB';
    SET CONFIG tiflash `raftstore-proxy.server.snap-max-write-bytes-per-sec` = '300MiB';
    ```

    これらの SQL ステートメントを実行すると、クラスターを再起動しなくても、構成の変更がすぐに有効になります。ただし、レプリケーション速度は依然として PD 制限によってグローバルに制限されているため、現時点では加速を観察することはできません。

2.  新しいレプリカの速度制限を段階的に緩和するには、 [PD Control](https://docs.pingcap.com/tidb/stable/pd-control)使用します。

    デフォルトの新しいレプリカの速度制限は 30 です。これは、毎分約 30 のリージョンがTiFlashレプリカを追加することを意味します。次のコマンドを実行すると、すべてのTiFlashインスタンスの制限が 60 に調整され、元の速度が 2 倍になります。

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 60 add-peer
    ```

    > 前述のコマンドでは、 `v<CLUSTER_VERSION>`実際のクラスターのバージョンに置き換える必要があります。たとえば、 `v7.5.0`と`<PD_ADDRESS>:2379`任意の PD ノードのアドレスに置き換えます。例えば：
    >
    > ```shell
    > tiup ctl:v7.5.0 pd -u http://192.168.1.4:2379 store limit all engine tiflash 60 add-peer
    > ```

    数分以内に、 TiFlashノードの CPU およびディスク IO リソースの使用量が大幅に増加することがわかり、 TiFlash はレプリカをより速く作成するはずです。同時に、TiKV ノードの CPU およびディスク IO リソースの使用量も増加します。

    この時点で TiKV ノードとTiFlashノードにまだ予備のリソースがあり、オンライン サービスのレイテンシーが大幅に増加しない場合は、制限をさらに緩和することができます (たとえば、元の速度を 3 倍にする)。

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 90 add-peer
    ```

3.  TiFlashレプリケーションが完了したら、デフォルト構成に戻して、オンライン サービスへの影響を軽減します。

    次のPD Controlコマンドを実行して、デフォルトの新しいレプリカの速度制限を復元します。

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 30 add-peer
    ```

    次の SQL ステートメントを実行して、デフォルトのスナップショット書き込み速度制限を復元します。

    ```sql
    SET CONFIG tikv `server.snap-io-max-bytes-per-sec` = '100MiB';
    SET CONFIG tiflash `raftstore-proxy.server.snap-max-write-bytes-per-sec` = '100MiB';
    ```

## 利用可能なゾーンを設定する {#set-available-zones}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> このセクションはTiDB Cloudには適用されません。

</CustomContent>

レプリカの構成時に、災害復旧のためにTiFlashレプリカを複数のデータセンターに分散する必要がある場合は、次の手順に従って利用可能なゾーンを構成できます。

1.  クラスター構成ファイルでTiFlashノードのラベルを指定します。

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

    以前のバージョンの`flash.proxy.labels`構成では、使用可能なゾーン名の特殊文字を正しく処理できないことに注意してください。使用可能なゾーンの名前を構成するには、 `server.labels` in `learner_config`を使用することをお勧めします。

2.  クラスターを起動した後、レプリカを作成するときにラベルを指定します。

    ```sql
    ALTER TABLE table_name SET TIFLASH REPLICA count LOCATION LABELS location_labels;
    ```

    例えば：

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

<CustomContent platform="tidb">

ラベルを使用したレプリカのスケジュール設定の詳細については、 [トポロジ ラベルごとにレプリカをスケジュールする](/schedule-replicas-by-topology-labels.md) 、 [1 つの地域展開における複数のデータセンター](/multi-data-centers-in-one-city-deployment.md) 、および[2 つの地域に配置された 3 つのデータ センター](/three-data-centers-in-two-cities-deployment.md)を参照してください。

TiFlash は、さまざまなゾーンのレプリカ選択戦略の構成をサポートしています。詳細については、 [`tiflash_replica_read`](/system-variables.md#tiflash_replica_read-new-in-v730)を参照してください。

</CustomContent>
