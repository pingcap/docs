---
title: Create TiFlash Replicas
summary: Learn how to create TiFlash replicas.
---

# TiFlash レプリカの作成 {#create-tiflash-replicas}

このドキュメントでは、テーブルとデータベースの TiFlash レプリカを作成し、レプリカのスケジュールに使用できるゾーンを設定する方法を紹介します。

## テーブルの TiFlash レプリカを作成する {#create-tiflash-replicas-for-tables}

TiFlash が TiKVクラスタに接続された後、デフォルトではデータ複製は開始されません。 MySQL クライアント経由で DDL ステートメントを TiDB に送信して、特定のテーブルの TiFlash レプリカを作成できます。

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

-   テーブル`t`が上記の DDL ステートメントによって TiFlash に複製される場合、次のステートメントを使用して作成されたテーブルも自動的に TiFlash に複製されます。

    {{< copyable "" >}}

    ```sql
    CREATE TABLE table_name like t;
    ```

-   v4.0.6 より前のバージョンでは、 TiDB Lightningを使用してデータをインポートする前に TiFlash レプリカを作成すると、データのインポートは失敗します。テーブルの TiFlash レプリカを作成する前に、テーブルにデータをインポートする必要があります。

-   TiDB とTiDB Lightningが両方とも v4.0.6 以降の場合、テーブルに TiFlash レプリカがあるかどうかに関係なく、 TiDB Lightningを使用してそのテーブルにデータをインポートできます。これにより、 TiDB Lightning手順が遅くなる可能性があることに注意してください。これは、Lightning ホストの NIC 帯域幅、TiFlash ノードの CPU とディスクの負荷、および TiFlash レプリカの数に依存します。

-   PD スケジューリングのパフォーマンスが低下するため、1,000 を超えるテーブルを複製しないことをお勧めします。この制限は、以降のバージョンで削除されます。

-   v5.1 以降のバージョンでは、システム テーブルのレプリカの設定はサポートされなくなりました。クラスタをアップグレードする前に、関連するシステム テーブルのレプリカをクリアする必要があります。そうしないと、クラスタを新しいバージョンにアップグレードした後で、システム テーブルのレプリカ設定を変更できません。

### レプリケーションの進行状況を確認する {#check-replication-progress}

次のステートメントを使用して、特定のテーブルの TiFlash レプリカのステータスを確認できます。テーブルは`WHERE`句を使用して指定されます。 `WHERE`句を削除すると、すべてのテーブルのレプリカ ステータスがチェックされます。

{{< copyable "" >}}

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>' and TABLE_NAME = '<table_name>';
```

上記のステートメントの結果:

-   `AVAILABLE`は、このテーブルの TiFlash レプリカが使用可能かどうかを示します。 `1`は利用可能であることを意味し、 `0`は利用できないことを意味します。レプリカが利用可能になると、このステータスは変わりません。 DDL ステートメントを使用してレプリカの数を変更すると、レプリケーション ステータスが再計算されます。
-   `PROGRESS`は、レプリケーションの進行状況を意味します。値は`0.0` ～ `1.0`です。 `1`は、少なくとも 1 つのレプリカが複製されていることを意味します。

## データベースの TiFlash レプリカを作成する {#create-tiflash-replicas-for-databases}

テーブルの TiFlash レプリカを作成するのと同様に、MySQL クライアントを介して TiDB に DDL ステートメントを送信し、特定のデータベース内のすべてのテーブルの TiFlash レプリカを作成できます。

{{< copyable "" >}}

```sql
ALTER DATABASE db_name SET TIFLASH REPLICA count;
```

このステートメントでは、 `count`はレプリカの数を示します。 `0`に設定すると、レプリカが削除されます。

例:

-   データベース`tpch50`内のすべてのテーブルに対して 2 つのレプリカを作成します。

    {{< copyable "" >}}

    ```sql
    ALTER DATABASE `tpch50` SET TIFLASH REPLICA 2;
    ```

-   データベース`tpch50`用に作成された TiFlash レプリカを削除します。

    {{< copyable "" >}}

    ```sql
    ALTER DATABASE `tpch50` SET TIFLASH REPLICA 0;
    ```

> **ノート：**
>
> -   このステートメントは、リソースを集中的に使用する一連の DDL 操作を実際に実行します。実行中にステートメントが中断された場合、実行された操作はロールバックされず、実行されていない操作は続行されません。
>
> -   ステートメントを実行した後、このデータベース**内のすべてのテーブルがレプリケートされる**まで、TiFlash レプリカの数を設定したり、このデータベースで DDL 操作を実行したりしないでください。そうしないと、次のような予期しない結果が発生する可能性があります。
>     -   TiFlash レプリカの数を 2 に設定し、データベース内のすべてのテーブルが複製される前に数を 1 に変更した場合、すべてのテーブルの TiFlash レプリカの最終的な数は必ずしも 1 または 2 とは限りません。
>     -   ステートメントの実行後、ステートメントの実行が完了する前にこのデータベースにテーブルを作成すると、これらの新しいテーブルに対して TiFlash レプリカ**が作成される場合と作成されない場合があり**ます。
>     -   ステートメントの実行後、ステートメントの実行が完了する前にデータベース内のテーブルのインデックスを追加すると、ステートメントがハングし、インデックスが追加された後にのみ再開される場合があります。
>
> -   このステートメントは、システム テーブル、ビュー、一時テーブル、および TiFlash でサポートされていない文字セットを含むテーブルをスキップします。

### レプリケーションの進行状況を確認する {#check-replication-progress}

テーブルの TiFlash レプリカの作成と同様に、DDL ステートメントの実行が成功しても、レプリケーションが完了するわけではありません。次の SQL ステートメントを実行して、ターゲット テーブルでのレプリケーションの進行状況を確認できます。

{{< copyable "" >}}

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>';
```

データベースに TiFlash レプリカがないテーブルをチェックするには、次の SQL ステートメントを実行します。

{{< copyable "" >}}

```sql
SELECT TABLE_NAME FROM information_schema.tables where TABLE_SCHEMA = "<db_name>" and TABLE_NAME not in (SELECT TABLE_NAME FROM information_schema.tiflash_replica where TABLE_SCHEMA = "<db_name>");
```

## 利用可能なゾーンを設定する {#set-available-zones}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> このセクションはTiDB Cloudには適用されません。

</CustomContent>

レプリカを構成するときに、災害復旧のために TiFlash レプリカを複数のデータ センターに配布する必要がある場合は、次の手順に従って使用可能なゾーンを構成できます。

1.  クラスタ構成ファイルで TiFlash ノードのラベルを指定します。

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

2.  クラスタを開始した後、レプリカを作成するときにラベルを指定します。

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
    > tiup ctl:<version> pd -u<pd-host>:<pd-port> store

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

ラベルを使用してレプリカをスケジュールする方法の詳細については、 [トポロジ ラベルごとにレプリカをスケジュールする](/schedule-replicas-by-topology-labels.md) 、 [1 つの地域展開における複数のデータセンター](/multi-data-centers-in-one-city-deployment.md) 、および[2 つの都市に配置された 3 つのデータ センター](/three-data-centers-in-two-cities-deployment.md)を参照してください。

</CustomContent>
