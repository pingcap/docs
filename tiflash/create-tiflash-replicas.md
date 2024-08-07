---
title: Create TiFlash Replicas
summary: TiFlashレプリカを作成する方法を学びます。
---

# TiFlashレプリカを作成する {#create-tiflash-replicas}

このドキュメントでは、テーブルとデータベースのTiFlashレプリカを作成し、レプリカのスケジュールに使用可能なゾーンを設定する方法について説明します。

## テーブルのTiFlashレプリカを作成する {#create-tiflash-replicas-for-tables}

TiFlashが TiKV クラスターに接続された後、デフォルトではデータ レプリケーションは開始されません。MySQL クライアントを介して DDL ステートメントを TiDB に送信し、特定のテーブルのTiFlashレプリカを作成できます。

```sql
ALTER TABLE table_name SET TIFLASH REPLICA count;
```

上記コマンドのパラメータは以下のように記述されます。

-   `count`レプリカの数を示します。値が`0`の場合、レプリカは削除されます。

> **注記：**
>
> [TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターの場合、 TiFlashレプリカの`count` `2`までしか設定できません。 `1`に設定すると、実行時に自動的に`2`に調整されます。 2 より大きい数値に設定すると、レプリカ数に関するエラーが発生します。

同じテーブルに対して複数の DDL ステートメントを実行する場合、最後のステートメントのみが有効になります。次の例では、テーブル`tpch50`に対して 2 つの DDL ステートメントが実行されていますが、2 番目のステートメント (レプリカを削除する) のみが有効になります。

テーブルのレプリカを 2 つ作成します。

```sql
ALTER TABLE `tpch50`.`lineitem` SET TIFLASH REPLICA 2;
```

レプリカを削除します。

```sql
ALTER TABLE `tpch50`.`lineitem` SET TIFLASH REPLICA 0;
```

**ノート：**

-   上記の DDL ステートメントを通じてテーブル`t`がTiFlashに複製されると、次のステートメントを使用して作成されたテーブルも自動的にTiFlashに複製されます。

    ```sql
    CREATE TABLE table_name like t;
    ```

-   v4.0.6 より前のバージョンでは、 TiDB Lightningを使用してデータをインポートする前にTiFlashレプリカを作成すると、データのインポートは失敗します。テーブルのTiFlashレプリカを作成する前に、テーブルにデータをインポートする必要があります。

-   TiDB とTiDB Lightning の両方が v4.0.6 以降の場合、テーブルにTiFlashレプリカがあるかどうかに関係なく、 TiDB Lightningを使用してそのテーブルにデータをインポートできます。ただし、これにより、 TiDB Lightning の手順が遅くなる場合があります。これは、Lightning ホストの NIC 帯域幅、 TiFlashノードの CPU とディスクの負荷、およびTiFlashレプリカの数によって異なります。

-   PD スケジューリングのパフォーマンスが低下するため、1,000 を超えるテーブルをレプリケートしないことをお勧めします。この制限は、今後のバージョンでは削除される予定です。

-   v5.1 以降のバージョンでは、システム テーブルのレプリカの設定はサポートされなくなりました。クラスターをアップグレードする前に、関連するシステム テーブルのレプリカをクリアする必要があります。そうしないと、クラスターを新しいバージョンにアップグレードした後に、システム テーブルのレプリカ設定を変更できなくなります。

### レプリケーションの進行状況を確認する {#check-replication-progress}

次のステートメントを使用して`WHERE`特定のテーブルのTiFlashレプリカのステータスを確認できます。テーブルは`WHERE`句を使用して指定されます。3 句を削除すると、すべてのテーブルのレプリカ ステータスがチェックされます。

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>' and TABLE_NAME = '<table_name>';
```

上記のステートメントの結果:

-   `AVAILABLE` 、このテーブルのTiFlashレプリカが使用可能かどうかを示します。2 `1`使用可能、 `0`使用不可を意味します。レプリカが使用可能になると、このステータスは変更されません。DDL ステートメントを使用してレプリカの数を変更すると、レプリケーション ステータスが再計算されます。
-   `PROGRESS`レプリケーションの進行状況を意味します。値は`0.0`から`1.0`の間です。6 `1`少なくとも 1 つのレプリカがレプリケートされていることを意味します。

## データベースのTiFlashレプリカを作成する {#create-tiflash-replicas-for-databases}

テーブルのTiFlashレプリカを作成する場合と同様に、MySQL クライアントを介して DDL ステートメントを TiDB に送信し、特定のデータベース内のすべてのテーブルのTiFlashレプリカを作成できます。

```sql
ALTER DATABASE db_name SET TIFLASH REPLICA count;
```

このステートメントでは、 `count`レプリカの数を示します。 `0`に設定すると、レプリカが削除されます。

例:

-   データベース`tpch50`内のすべてのテーブルに対して 2 つのレプリカを作成します。

    ```sql
    ALTER DATABASE `tpch50` SET TIFLASH REPLICA 2;
    ```

-   データベース`tpch50`用に作成されたTiFlashレプリカを削除します。

    ```sql
    ALTER DATABASE `tpch50` SET TIFLASH REPLICA 0;
    ```

> **注記：**
>
> -   このステートメントは、実際にはリソースを大量に消費する一連の DDL 操作を実行します。ステートメントの実行中に中断された場合、実行された操作はロールバックされず、実行されていない操作は続行されません。
>
> -   ステートメントを実行した後、**このデータベース内のすべてのテーブルがレプリケートされる**まで、 TiFlashレプリカの数を設定したり、このデータベースで DDL 操作を実行したりしないでください。そうしないと、次のような予期しない結果が発生する可能性があります。
>     -   TiFlashレプリカの数を 2 に設定し、データベース内のすべてのテーブルがレプリケートされる前にその数を 1 に変更した場合、すべてのテーブルのTiFlashレプリカの最終的な数は必ずしも 1 または 2 になるとは限りません。
>     -   ステートメントを実行した後、ステートメントの実行が完了する前にこのデータベースにテーブルを作成すると、これらの新しいテーブルに対してTiFlashレプリカが作成される**場合と作成されない場合があります**。
>     -   ステートメントを実行した後、ステートメントの実行が完了する前にデータベース内のテーブルにインデックスを追加すると、ステートメントがハングし、インデックスが追加された後にのみ再開される可能性があります。
>
> -   ステートメントの実行が完了した**後に**このデータベースにテーブルを作成した場合、これらの新しいテーブルに対してTiFlashレプリカは自動的に作成されません。
>
> -   このステートメントは、システム テーブル、ビュー、一時テーブル、およびTiFlashでサポートされていない文字セットを持つテーブルをスキップします。

### レプリケーションの進行状況を確認する {#check-replication-progress}

テーブルのTiFlashレプリカを作成する場合と同様に、DDL ステートメントの実行が成功してもレプリケーションが完了したことにはなりません。次の SQL ステートメントを実行して、ターゲット テーブルのレプリケーションの進行状況を確認できます。

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>';
```

データベース内にTiFlashレプリカのないテーブルをチェックするには、次の SQL ステートメントを実行します。

```sql
SELECT TABLE_NAME FROM information_schema.tables where TABLE_SCHEMA = "<db_name>" and TABLE_NAME not in (SELECT TABLE_NAME FROM information_schema.tiflash_replica where TABLE_SCHEMA = "<db_name>");
```

## TiFlashレプリケーションの高速化 {#speed-up-tiflash-replication}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> このセクションはTiDB Cloudには適用されません。

</CustomContent>

TiFlashレプリカが追加される前に、各 TiKV インスタンスは完全なテーブル スキャンを実行し、スキャンされたデータを「スナップショット」としてTiFlashに送信してレプリカを作成します。デフォルトでは、オンライン サービスへの影響を最小限に抑えるために、 TiFlashレプリカはリソース使用量を抑えながらゆっくりと追加されます。TiKV ノードとTiFlashノードに余裕のある CPU とディスク IO リソースがある場合は、次の手順を実行してTiFlashレプリケーションを高速化できます。

1.  [動的構成SQLステートメント](https://docs.pingcap.com/tidb/stable/dynamic-config)を使用して、各 TiKV およびTiFlashインスタンスのスナップショット書き込み速度制限を一時的に上げます。

    ```sql
    -- The default value for both configurations are 100MiB, i.e. the maximum disk bandwidth used for writing snapshots is no more than 100MiB/s.
    SET CONFIG tikv `server.snap-io-max-bytes-per-sec` = '300MiB';
    SET CONFIG tiflash `raftstore-proxy.server.snap-max-write-bytes-per-sec` = '300MiB';
    ```

    これらの SQL 文を実行すると、クラスターを再起動せずに構成の変更がすぐに有効になります。ただし、レプリケーション速度は依然として PD 制限によってグローバルに制限されているため、現時点では高速化を確認することはできません。

2.  新しいレプリカの速度制限を徐々に緩和するには、 [PD Control](https://docs.pingcap.com/tidb/stable/pd-control)使用します。

    デフォルトの新しいレプリカの速度制限は 30 です。つまり、約 30 のリージョンが毎分TiFlashレプリカを追加します。次のコマンドを実行すると、すべてのTiFlashインスタンスの制限が 60 に調整され、元の速度が 2 倍になります。

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 60 add-peer
    ```

    > 上記のコマンドでは、 `v<CLUSTER_VERSION>`実際のクラスター バージョンに置き換える必要があります (例: `v7.5.3`と`<PD_ADDRESS>:2379`任意の PD ノードのアドレスに置き換える)。次に例を示します。
    >
    > ```shell
    > tiup ctl:v7.5.3 pd -u http://192.168.1.4:2379 store limit all engine tiflash 60 add-peer
    > ```

    数分以内に、 TiFlashノードの CPU とディスク IO リソースの使用率が大幅に増加し、 TiFlashによるレプリカの作成速度が速くなります。同時に、TiKV ノードの CPU とディスク IO リソースの使用率も増加します。

    この時点で TiKV ノードとTiFlashノードにまだ余分なリソースがあり、オンライン サービスのレイテンシーが大幅に増加しない場合は、制限をさらに緩和して、たとえば元の速度を 3 倍にすることができます。

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 90 add-peer
    ```

3.  TiFlashレプリケーションが完了したら、オンライン サービスへの影響を軽減するために、デフォルト構成に戻します。

    デフォルトの新しいレプリカ速度制限を復元するには、次のPD Controlコマンドを実行します。

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 30 add-peer
    ```

    デフォルトのスナップショット書き込み速度制限を復元するには、次の SQL ステートメントを実行します。

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

レプリカを構成するときに、災害復旧のためにTiFlashレプリカを複数のデータセンターに配布する必要がある場合は、次の手順に従って使用可能なゾーンを構成できます。

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

    以前のバージョンの`flash.proxy.labels`構成では、使用可能なゾーン名内の特殊文字を正しく処理できないことに注意してください。使用可能なゾーンの名前を構成するには、 `learner_config`の`server.labels`を使用することをお勧めします。

2.  クラスターを起動した後、レプリカを作成するときにラベルを指定します。

    ```sql
    ALTER TABLE table_name SET TIFLASH REPLICA count LOCATION LABELS location_labels;
    ```

    例えば：

    ```sql
    ALTER TABLE t SET TIFLASH REPLICA 2 LOCATION LABELS "zone";
    ```

3.  PD はラベルに基づいてレプリカをスケジュールします。この例では、PD はテーブル`t`の 2 つのレプリカをそれぞれ 2 つの利用可能なゾーンにスケジュールします。スケジュールを表示するには、pd-ctl を使用できます。

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

ラベルを使用してレプリカをスケジュールする方法の詳細については、 [トポロジラベルによるレプリカのスケジュール](/schedule-replicas-by-topology-labels.md) 、 [1 つの地域展開における複数のデータセンター](/multi-data-centers-in-one-city-deployment.md) 、および[2 つの地域に配置された 3 つのデータ センター](/three-data-centers-in-two-cities-deployment.md)を参照してください。

TiFlash は、さまざまなゾーンのレプリカ選択戦略の構成をサポートしています。詳細については、 [`tiflash_replica_read`](/system-variables.md#tiflash_replica_read-new-in-v730)を参照してください。

</CustomContent>
