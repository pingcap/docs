---
title: Create TiFlash Replicas
summary: TiFlashレプリカを作成する方法を学びます。
---

# TiFlashレプリカを作成する {#create-tiflash-replicas}

このドキュメントでは、テーブルおよびデータベースのTiFlashレプリカを作成し、レプリカのスケジュールに使用可能なゾーンを設定する方法について説明します。

## テーブルのTiFlashレプリカを作成する {#create-tiflash-replicas-for-tables}

TiFlashがTiKVクラスターに接続されても、デフォルトではデータレプリケーションは開始されません。MySQLクライアント経由でTiDBにDDL文を送信することで、特定のテーブルのTiFlashレプリカを作成できます。

```sql
ALTER TABLE table_name SET TIFLASH REPLICA count;
```

上記コマンドのパラメータは以下のとおりです。

-   `count`レプリカの数を示します。値が`0`の場合、レプリカは削除されます。

> **注記：**
>
> [TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)クラスターの場合、 TiFlashレプリカの`count` `2`しか設定できません。7 `1`設定した場合、実行時に自動的に`2`に調整されます。2 より大きい数に設定した場合、レプリカ数に関するエラーが発生します。

同じテーブルに対して複数のDDL文を実行した場合、最後に実行された文のみが確実に有効になります。次の例では、テーブル`tpch50`に対して2つのDDL文が実行されていますが、2番目の文（レプリカを削除する文）のみが確実に有効になります。

テーブルのレプリカを 2 つ作成します。

```sql
ALTER TABLE `tpch50`.`lineitem` SET TIFLASH REPLICA 2;
```

レプリカを削除します。

```sql
ALTER TABLE `tpch50`.`lineitem` SET TIFLASH REPLICA 0;
```

**注:**

-   上記の DDL ステートメントを使用してテーブル`t` TiFlashに複製されると、次のステートメントを使用して作成されたテーブルも自動的にTiFlashに複製されます。

    ```sql
    CREATE TABLE table_name like t;
    ```

-   v4.0.6より前のバージョンでは、 TiDB Lightningを使用してデータをインポートする前にTiFlashレプリカを作成すると、データのインポートに失敗します。テーブルのTiFlashレプリカを作成する前に、テーブルにデータをインポートする必要があります。

-   TiDB とTiDB Lightning の両方が v4.0.6 以降の場合、テーブルにTiFlashレプリカがあるかどうかに関係なく、 TiDB Lightningを使用してそのテーブルにデータをインポートできます。ただし、 TiDB Lightning のプロセスは、Lightning ホストの NIC 帯域幅、 TiFlashノードの CPU とディスク負荷、およびTiFlashレプリカの数に応じて遅くなる可能性があります。

-   PDスケジューリングのパフォーマンスが低下するため、1,000を超えるテーブルを複製することは推奨されません。この制限は、今後のバージョンで削除される予定です。

-   v5.1以降のバージョンでは、システムテーブルのレプリカ設定はサポートされなくなりました。クラスターをアップグレードする前に、関連するシステムテーブルのレプリカをクリアする必要があります。そうしないと、クラスターを新しいバージョンにアップグレードした後に、システムテーブルのレプリカ設定を変更できなくなります。

-   現在、TiCDC を使用してテーブルをダウンストリーム TiDB クラスターにレプリケートする場合、テーブルのTiFlashレプリカの作成はサポートされていません。つまり、TiCDC は次のようなTiFlash関連の DDL ステートメントのレプリケートをサポートしていません。

    -   `ALTER TABLE table_name SET TIFLASH REPLICA count;`
    -   `ALTER DATABASE db_name SET TIFLASH REPLICA count;`

### レプリケーションの進行状況を確認する {#check-replication-progress}

特定のテーブルのTiFlashレプリカのステータスを確認するには、次のステートメントを使用します。テーブルは`WHERE`句で指定します。3 `WHERE`の句を削除すると、すべてのテーブルのレプリカステータスを確認できます。

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>' and TABLE_NAME = '<table_name>';
```

上記のステートメントの結果は次のようになります。

-   `AVAILABLE` 、このテーブルのTiFlashレプリカが使用可能かどうかを示します。2 `1`使用可能、 `0`使用不可を意味します。レプリカが使用可能になると、このステータスは変更されません。DDL ステートメントを使用してレプリカの数を変更すると、レプリケーション ステータスは再計算されます。
-   `PROGRESS`レプリケーションの進行状況を表します。値は`0.0`から`1.0`までです。6 `1`少なくとも 1 つのレプリカがレプリケートされていることを意味します。

## データベースのTiFlashレプリカを作成する {#create-tiflash-replicas-for-databases}

テーブルのTiFlashレプリカを作成するのと同様に、MySQL クライアントを介して DDL ステートメントを TiDB に送信し、特定のデータベース内のすべてのテーブルのTiFlashレプリカを作成できます。

```sql
ALTER DATABASE db_name SET TIFLASH REPLICA count;
```

このステートメントでは、 `count`レプリカの数を示しています。 `0`に設定すると、レプリカが削除されます。

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
> -   この文は実際には一連のDDL操作を実行しますが、これらの操作はリソースを大量に消費します。文の実行中に中断された場合、実行済みの操作はロールバックされず、未実行の操作は続行されません。
>
> -   ステートメント実行後、**このデータベース内のすべてのテーブルがレプリケートされる**まで、 TiFlashレプリカの数を設定したり、このデータベースに対してDDL操作を実行したりしないでください。そうしないと、次のような予期しない結果が発生する可能性があります。
>     -   TiFlashレプリカの数を 2 に設定し、データベース内のすべてのテーブルがレプリケートされる前にその数を 1 に変更した場合、すべてのテーブルのTiFlashレプリカの最終的な数は必ずしも 1 または 2 になるとは限りません。
>     -   ステートメントを実行した後、ステートメントの実行が完了する前にこのデータベースにテーブルを作成すると、これらの新しいテーブルに対してTiFlashレプリカが作成される**場合と作成されない場合があります**。
>     -   ステートメントを実行した後、ステートメントの実行が完了する前にデータベース内のテーブルのインデックスを追加すると、ステートメントがハングし、インデックスが追加された後にのみ再開される可能性があります。
>
> -   ステートメントの実行が完了した**後に**このデータベースにテーブルを作成した場合、これらの新しいテーブルに対してTiFlashレプリカは自動的に作成されません。
>
> -   このステートメントは、システム テーブル、ビュー、一時テーブル、およびTiFlashでサポートされていない文字セットを持つテーブルをスキップします。

> -   システム変数[`tidb_batch_pending_tiflash_count`](/system-variables.md#tidb_batch_pending_tiflash_count-new-in-v60)設定することで、実行中に利用不可のままにできるテーブルの数を制御できます。この値を下げると、レプリケーション中のクラスターへの負荷を軽減できます。ただし、この制限はリアルタイムではないため、設定適用後も利用不可のテーブルの数が制限を超える可能性があります。

### レプリケーションの進行状況を確認する {#check-replication-progress}

テーブルのTiFlashレプリカの作成と同様に、DDL文の実行が成功してもレプリケーションの完了を意味するわけではありません。次のSQL文を実行することで、ターゲットテーブルのレプリケーションの進行状況を確認できます。

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

TiDB クラスターは、次のいずれかの操作を実行すると、 TiFlashレプリカのレプリケーション プロセスをトリガーします。

-   テーブルにTiFlashレプリカを追加します。
-   新しいTiFlashインスタンスを追加すると、PD は元のインスタンスのTiFlashレプリカを新しいTiFlashインスタンスにスケジュールします。

このプロセス中、各TiKVインスタンスはテーブル全体をスキャンし、スキャンしたデータのスナップショットをTiFlashに送信してレプリカを作成します。デフォルトでは、TiKVおよびTiFlashの本番ワークロードへの影響を最小限に抑えるため、 TiFlashはレプリカの追加速度を遅くし、使用するリソースを少なくしています。TiKVノードとTiFlashノードに十分なCPUとディスクI/Oリソースがある場合は、以下の手順を実行することでTiFlashレプリケーションを高速化できます。

1.  [動的設定SQL文](https://docs.pingcap.com/tidb/stable/dynamic-config)使用して、各 TiKV およびTiFlashインスタンスのスナップショット書き込み速度制限を一時的に上げます。

    ```sql
    -- The default value for both configurations are 100MiB, i.e. the maximum disk bandwidth used for writing snapshots is no more than 100MiB/s.
    SET CONFIG tikv `server.snap-io-max-bytes-per-sec` = '300MiB';
    SET CONFIG tiflash `raftstore-proxy.server.snap-io-max-bytes-per-sec` = '300MiB';
    ```

    これらのSQL文を実行すると、クラスターを再起動することなく設定変更が即座に有効になります。ただし、レプリケーション速度はPD制限によってグローバルに制限されているため、現時点では高速化の効果を確認することはできません。

2.  レプリカのスケジュール速度制限を段階的に緩和するには、 [PD Control](https://docs.pingcap.com/tidb/stable/pd-control)使用します。

    デフォルトの新規レプリカ速度制限は30です。これは、1分間に約30のリージョンが1つのTiFlashインスタンス上でTiFlashレプリカを追加または削除することを意味します。以下のコマンドを実行すると、すべてのTiFlashインスタンスの制限が60に調整され、速度は元の2倍になります。

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 60 add-peer
    ```

    > 上記のコマンドでは、 `v<CLUSTER_VERSION>`実際のクラスターバージョン（ `v8.5.3`など）に置き換え、 `<PD_ADDRESS>:2379`任意の PD ノードのアドレスに置き換える必要があります。例:
    >
    > ```shell
    > tiup ctl:v8.5.3 pd -u http://192.168.1.4:2379 store limit all engine tiflash 60 add-peer
    > ```

    クラスターに古いTiFlashノード上のリージョンが多数含まれている場合、PDはそれらを新しいTiFlashノードに再バランスする必要があります。それに応じて`remove-peer`制限を調整する必要があります。

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 60 remove-peer
    ```

    数分以内に、 TiFlashノードのCPUとディスクIOリソース使用量が大幅に増加し、 TiFlashによるレプリカ作成速度が速くなります。同時に、TiKVノードのCPUとディスクIOリソース使用量も増加します。

    この時点で TiKV ノードとTiFlashノードにまだ余分なリソースがあり、オンライン サービスのレイテンシーが大幅に増加しない場合は、制限をさらに緩和して、たとえば元の速度を 3 倍にすることができます。

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 90 add-peer
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 90 remove-peer
    ```

3.  TiFlashレプリケーションが完了したら、オンライン サービスへの影響を軽減するために、デフォルト構成に戻します。

    デフォルトのレプリカ スケジューリング速度制限を復元するには、次のPD Controlコマンドを実行します。

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 30 add-peer
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 30 remove-peer
    ```

    デフォルトのスナップショット書き込み速度制限を復元するには、次の SQL ステートメントを実行します。

    ```sql
    SET CONFIG tikv `server.snap-io-max-bytes-per-sec` = '100MiB';
    SET CONFIG tiflash `raftstore-proxy.server.snap-io-max-bytes-per-sec` = '100MiB';
    ```

## 利用可能なゾーンを設定する {#set-available-zones}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> このセクションはTiDB Cloudには適用されません。

</CustomContent>

レプリカを構成する際に、災害復旧のためにTiFlashレプリカを複数のデータセンターに分散する必要がある場合は、次の手順に従って使用可能なゾーンを構成できます。

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

    以前のバージョンでは、 `flash.proxy.labels`設定では、利用可能なゾーン名に含まれる特殊文字を正しく処理できないことに注意してください。利用可能なゾーン名を設定するには、 `learner_config`の`server.labels`を使用することをお勧めします。

2.  クラスターを起動した後、高可用性を実現するためにTiFlashレプリカの数を指定します。構文は次のとおりです。

    ```sql
    ALTER TABLE table_name SET TIFLASH REPLICA count;
    ```

    例えば：

    ```sql
    ALTER TABLE t SET TIFLASH REPLICA 2;
    ```

3.  PDは、 TiFlashノードの`learner_config` `server.labels`テーブルのレプリカ数（ `count` ）に基づいて、テーブル`t`のレプリカを異なるアベイラビリティゾーンにスケジュールし、可用性を確保します。詳細については、 [トポロジラベルによるレプリカのスケジュール](https://docs.pingcap.com/tidb/stable/schedule-replicas-by-topology-labels/)参照してください。次のSQL文を使用して、 TiFlashノード間のテーブルのリージョンの分散を確認できます。

    ```sql
    -- Non-partitioned table
    SELECT table_id, p.store_id, address, COUNT(p.region_id) 
    FROM
      information_schema.tikv_region_status r,
      information_schema.tikv_region_peers p,
      information_schema.tikv_store_status s
    WHERE
      r.db_name = 'test' 
      AND r.table_name = 'table_to_check'
      AND r.region_id = p.region_id 
      AND p.store_id = s.store_id
      AND JSON_EXTRACT(s.label, '$[0].value') = 'tiflash'
    GROUP BY table_id, p.store_id, address;

    -- Partitioned table
    SELECT table_id, r.partition_name, p.store_id, address, COUNT(p.region_id)
    FROM
      information_schema.tikv_region_status r,
      information_schema.tikv_region_peers p,
      information_schema.tikv_store_status s
    WHERE 
      r.db_name = 'test' 
      AND r.table_name = 'table_to_check' 
      AND r.partition_name LIKE 'p202312%'
      AND r.region_id = p.region_id 
      AND p.store_id = s.store_id
      AND JSON_EXTRACT(s.label, '$[0].value') = 'tiflash'
    GROUP BY table_id, r.partition_name, p.store_id, address
    ORDER BY table_id, r.partition_name, p.store_id;
    ```

<CustomContent platform="tidb">

ラベルを使用してレプリカをスケジュールする方法の詳細については、 [トポロジラベルによるレプリカのスケジュール](/schedule-replicas-by-topology-labels.md) 、 [1 つの地域展開における複数のデータセンター](/multi-data-centers-in-one-city-deployment.md) 、および[2 つの地域に配置された 3 つのデータ センター](/three-data-centers-in-two-cities-deployment.md)参照してください。

TiFlashは、異なるゾーンに対するレプリカ選択戦略の設定をサポートしています。詳細については、 [`tiflash_replica_read`](/system-variables.md#tiflash_replica_read-new-in-v730)参照してください。

</CustomContent>

> **注記：**
>
> 構文`ALTER TABLE table_name SET TIFLASH REPLICA count LOCATION LABELS location_labels;`において、 `location_labels`に複数のラベルを指定すると、TiDBはそれらを正しく解析して配置ルールを設定できません。したがって、 TiFlashレプリカの設定には`LOCATION LABELS`使用しないでください。
