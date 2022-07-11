---
title: Create TiFlash Replicas
summary: Learn how to create TiFlash replicas.
---

# TiFlashレプリカを作成する {#create-tiflash-replicas}

このドキュメントでは、テーブルとデータベースのTiFlashレプリカを作成する方法と、レプリカのスケジューリングに使用できるゾーンを設定する方法を紹介します。

## テーブルのTiFlashレプリカを作成する {#create-tiflash-replicas-for-tables}

TiFlashがTiKVクラスタに接続された後、デフォルトではデータレプリケーションは開始されません。 MySQLクライアントを介してDDLステートメントをTiDBに送信して、特定のテーブルのTiFlashレプリカを作成できます。

{{< copyable "" >}}

```sql
ALTER TABLE table_name SET TIFLASH REPLICA count;
```

上記のコマンドのパラメータは次のとおりです。

-   `count`はレプリカの数を示します。値が`0`の場合、レプリカは削除されます。

同じテーブルで複数のDDLステートメントを実行すると、最後のステートメントのみが有効になります。次の例では、2つのDDLステートメントがテーブル`tpch50`で実行されますが、2番目のステートメント（レプリカを削除するため）のみが有効になります。

テーブルのレプリカを2つ作成します。

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

-   テーブル`t`が上記のDDLステートメントを介してTiFlashに複製される場合、次のステートメントを使用して作成されたテーブルも自動的にTiFlashに複製されます。

    {{< copyable "" >}}

    ```sql
    CREATE TABLE table_name like t;
    ```

-   v4.0.6より前のバージョンでは、 TiDB Lightningを使用してデータをインポートする前にTiFlashレプリカを作成すると、データのインポートが失敗します。テーブルのTiFlashレプリカを作成する前に、データをテーブルにインポートする必要があります。

-   TiDBとTiDB Lightningの両方がv4.0.6以降の場合、テーブルにTiFlashレプリカがあるかどうかに関係なく、 TiDB Lightningを使用してそのテーブルにデータをインポートできます。これにより、 TiDB Lightningの手順が遅くなる可能性があることに注意してください。これは、LightningホストのNIC帯域幅、TiFlashノードのCPUとディスクの負荷、およびTiFlashレプリカの数によって異なります。

-   PDスケジューリングのパフォーマンスが低下するため、1,000を超えるテーブルを複製しないことをお勧めします。この制限は、今後のバージョンで削除される予定です。

-   v5.1以降のバージョンでは、システムテーブルのレプリカの設定はサポートされなくなりました。クラスタをアップグレードする前に、関連するシステムテーブルのレプリカをクリアする必要があります。そうしないと、クラスタを新しいバージョンにアップグレードした後、システムテーブルのレプリカ設定を変更できません。

### レプリケーションの進行状況を確認する {#check-replication-progress}

次のステートメントを使用して、特定のテーブルのTiFlashレプリカのステータスを確認できます。テーブルは`WHERE`句を使用して指定されます。 `WHERE`句を削除すると、すべてのテーブルのレプリカステータスが確認されます。

{{< copyable "" >}}

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>' and TABLE_NAME = '<table_name>';
```

上記のステートメントの結果：

-   `AVAILABLE`は、このテーブルのTiFlashレプリカが使用可能かどうかを示します。 `1`は利用可能、 `0`は利用不可を意味します。レプリカが使用可能になると、このステータスは変更されません。 DDLステートメントを使用してレプリカの数を変更すると、レプリケーションステータスが再計算されます。
-   `PROGRESS`は、レプリケーションの進行状況を意味します。値は`0.0` `1.0` 。 `1`は、少なくとも1つのレプリカが複製されることを意味します。

## データベース用のTiFlashレプリカを作成する {#create-tiflash-replicas-for-databases}

テーブルのTiFlashレプリカを作成するのと同様に、MySQLクライアントを介してDDLステートメントをTiDBに送信して、特定のデータベース内のすべてのテーブルのTiFlashレプリカを作成できます。

{{< copyable "" >}}

```sql
ALTER DATABASE db_name SET TIFLASH REPLICA count;
```

このステートメントで、 `count`はレプリカの数を示します。 `0`に設定すると、レプリカが削除されます。

例：

-   データベース内のすべてのテーブルに対して2つのレプリカを作成します`tpch50` ：

    {{< copyable "" >}}

    ```sql
    ALTER DATABASE `tpch50` SET TIFLASH REPLICA 2;
    ```

-   データベース用に作成されたTiFlashレプリカを削除します`tpch50` ：

    {{< copyable "" >}}

    ```sql
    ALTER DATABASE `tpch50` SET TIFLASH REPLICA 0;
    ```

> **ノート：**
>
> -   このステートメントは、実際には、リソースを大量に消費する一連のDDL操作を実行します。実行中にステートメントが中断された場合、実行された操作はロールバックされず、実行されていない操作は続行されません。
>
> -   ステートメントの実行後、このデータベース**内のすべてのテーブルが複製される**まで、TiFlashレプリカの数を設定したり、このデータベースでDDL操作を実行したりしないでください。そうしないと、次のような予期しない結果が発生する可能性があります。
>     -   データベース内のすべてのテーブルが複製される前に、TiFlashレプリカの数を2に設定し、その数を1に変更した場合、すべてのテーブルのTiFlashレプリカの最終的な数は必ずしも1または2ではありません。
>     -   ステートメントの実行後、ステートメントの実行が完了する前にこのデータベースにテーブルを作成すると、これらの新しいテーブルに対してTiFlashレプリカ**が作成される場合と作成されない場合があり**ます。
>     -   ステートメントの実行後、ステートメントの実行が完了する前にデータベース内のテーブルのインデックスを追加すると、インデックスが追加された後にのみステートメントがハングして再開する場合があります。
>
> -   このステートメントは、システムテーブル、ビュー、一時テーブル、およびTiFlashでサポートされていない文字セットを持つテーブルをスキップします。

### レプリケーションの進行状況を確認する {#check-replication-progress}

テーブルのTiFlashレプリカの作成と同様に、DDLステートメントの正常な実行は、レプリケーションの完了を意味するものではありません。次のSQLステートメントを実行して、ターゲットテーブルでのレプリケーションの進行状況を確認できます。

{{< copyable "" >}}

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>';
```

データベースにTiFlashレプリカがないテーブルをチェックするには、次のSQLステートメントを実行できます。

{{< copyable "" >}}

```sql
SELECT TABLE_NAME FROM information_schema.tables where TABLE_SCHEMA = "<db_name>" and TABLE_NAME not in (SELECT TABLE_NAME FROM information_schema.tiflash_replica where TABLE_SCHEMA = "<db_name>");
```

## 利用可能なゾーンを設定する {#set-available-zones}

レプリカを構成するときに、ディザスタリカバリのためにTiFlashレプリカを複数のデータセンターに配布する必要がある場合は、以下の手順に従って使用可能なゾーンを構成できます。

1.  クラスタ構成ファイルでTiFlashノードのラベルを指定します。

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

2.  クラスタを起動した後、レプリカを作成するときにラベルを指定します。

    {{< copyable "" >}}

    ```sql
    ALTER TABLE table_name SET TIFLASH REPLICA count LOCATION LABELS location_labels;
    ```

    例えば：

    {{< copyable "" >}}

    ```sql
    ALTER TABLE t SET TIFLASH REPLICA 2 LOCATION LABELS "zone";
    ```

3.  PDは、ラベルに基づいてレプリカをスケジュールします。この例では、PDはそれぞれテーブル`t`の2つのレプリカを2つの使用可能なゾーンにスケジュールします。 pd-ctlを使用してスケジュールを表示できます。

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

ラベルを使用したレプリカのスケジューリングの詳細については、 [トポロジラベルによるレプリカのスケジュール](/schedule-replicas-by-topology-labels.md) 、および[1 つの地域展開における複数のデータセンター](/multi-data-centers-in-one-city-deployment.md)を参照して[2つの都市に配置された3つのデータセンター](/three-data-centers-in-two-cities-deployment.md) 。
