---
title: DR Solution Based on Multiple Replicas in a Single Cluster
summary: 単一クラスターのマルチレプリカ災害復旧ソリューションについて学習します。
---

# 単一クラスタ内の複数のレプリカに基づく DR ソリューション {#dr-solution-based-on-multiple-replicas-in-a-single-cluster}

このドキュメントでは、単一クラスタ内の複数のレプリカに基づく災害復旧 (DR) ソリューションについて説明します。ドキュメントは次のように構成されています。

-   ソリューション紹介
-   クラスターをセットアップしてレプリカを構成する方法
-   クラスターを監視する方法
-   DRスイッチオーバーを実行する方法

## 導入 {#introduction}

重要な本番システムでは通常、RPO がゼロで RTO が分単位の地域 DR が必要です。Raft ベースの分散データベースである TiDB は複数のレプリカを提供するため、データの一貫性と高可用性が保証された地域 DR をサポートできます。同じ地域内の利用可能なゾーン (AZ) 間のネットワークレイテンシーが小さいことを考慮すると、同じ地域にある 2 つの AZ に同時にビジネス トラフィックをディスパッチし、リージョンリーダーと PD リーダーを適切に配置することで、同じ地域にある AZ 間の負荷分散を実現できます。

> **注記：**
>
> [TiKV の「リージョン」](/glossary.md#regionpeerraft-group)データの範囲を意味し、「リージョン」という用語は物理的な場所を意味します。この 2 つの用語は互換性がありません。

## クラスターをセットアップしてレプリカを構成する {#set-up-a-cluster-and-configure-replicas}

このセクションでは、 TiUPを使用して 5 つのレプリカを持つ 3 つのリージョンにまたがる TiDB クラスターを作成する方法と、データと PD ノードを適切に分散して DR を実現する方法を説明します。

この例では、TiDB には 5 つのレプリカと 3 つのリージョンが含まれています。リージョン1 はプライマリ リージョン、リージョン 2 はセカンダリ リージョン、リージョン 3 は投票に使用されます。同様に、PD クラスターにも 5 つのレプリカが含まれており、基本的に TiDB クラスターと同じように機能します。

1.  次のようなトポロジ ファイルを作成します。

    ```toml
    global:
      user: "root"
      ssh_port: 22
      deploy_dir: "/data/tidb_cluster/tidb-deploy"
      data_dir: "/data/tidb_cluster/tidb-data"

    server_configs:
      tikv:
        server.grpc-compression-type: gzip
      pd:
        replication.location-labels:  ["Region","AZ"] # PD schedules replicas according to the Region and AZ configuration of TiKV nodes.

    pd_servers:
      - host: tidb-dr-test1
        name: "pd-1"
      - host: tidb-dr-test2
        name: "pd-2"
      - host: tidb-dr-test3
        name: "pd-3"
      - host: tidb-dr-test4
        name: "pd-4"
      - host: tidb-dr-test5
        name: "pd-5"

    tidb_servers:
      - host: tidb-dr-test1
      - host: tidb-dr-test3

    tikv_servers:  # Label the Regions and AZs of each TiKV node through the labels option.
      - host: tidb-dr-test1
        config:
          server.labels: { Region: "Region1", AZ: "AZ1" }
      - host: tidb-dr-test2
        config:
          server.labels: { Region: "Region1", AZ: "AZ2" }
      - host: tidb-dr-test3
        config:
          server.labels: { Region: "Region2", AZ: "AZ3" }
      - host: tidb-dr-test4
        config:
          server.labels: { Region: "Region2", AZ: "AZ4" }
      - host: tidb-dr-test5
        config:
          server.labels: { Region: "Region3", AZ: "AZ5" }

          raftstore.raft-min-election-timeout-ticks: 50
          raftstore.raft-max-election-timeout-ticks: 60

    monitoring_servers:
      - host: tidb-dr-test2

    grafana_servers:
      - host: tidb-dr-test2

    alertmanager_servers:
      - host: tidb-dr-test2
    ```

    上記の構成では、次のオプションを使用して、リージョン間 DR を最適化します。

    -   `server.grpc-compression-type: gzip`設定すると、TiKV での gRPC メッセージ圧縮が有効になり、ネットワーク トラフィックが削減されます。
    -   `raftstore.raft-min-election-timeout-ticks`と`raftstore.raft-max-election-timeout-ticks`設定すると、領域 3 が選挙に参加するまでの時間が延長され、この領域内のレプリカがリーダーとして投票されるのを防ぐことができます。

2.  上記の構成ファイルを使用してクラスターを作成します。

    ```shell
    tiup cluster deploy drtest v6.4.0 ./topo.yaml
    tiup cluster start drtest --init
    tiup cluster display drtest
    ```

    クラスターのレプリカ数とリーダー制限を設定します。

    ```shell
    tiup ctl:v6.4.0 pd config set max-replicas 5
    tiup ctl:v6.4.0 pd config set label-property reject-leader Region Region3

    # The following step adds some test data to the cluster, which is optional.
    tiup bench tpcc  prepare -H 127.0.0.1 -P 4000 -D tpcc --warehouses 1
    ```

    PD リーダーの優先度を指定します:

    ```shell
    tiup ctl:v6.4.0 pd member leader_priority  pd-1 4
    tiup ctl:v6.4.0 pd member leader_priority  pd-2 3
    tiup ctl:v6.4.0 pd member leader_priority  pd-3 2
    tiup ctl:v6.4.0 pd member leader_priority  pd-4 1
    tiup ctl:v6.4.0 pd member leader_priority  pd-5 0
    ```

    > **注記：**
    >
    > 優先度の数値が大きいほど、このノードがリーダーになる可能性が高くなります。

3.  配置ルールを作成し、テスト テーブルのプライマリ レプリカをリージョン 1 に固定します。

    ```sql
    -- Create two placement rules: the first rule specifies that region 1 works as the primary region, and region 2 as the secondary region.
    -- The second placement rule specifies that when region 1 is down, region 2 will become the primary region.
    MySQL [(none)]> CREATE PLACEMENT POLICY primary_rule_for_region1 PRIMARY_REGION="Region1" REGIONS="Region1, Region2,Region3";
    MySQL [(none)]> CREATE PLACEMENT POLICY secondary_rule_for_region2 PRIMARY_REGION="Region2" REGIONS="Region1,Region2,Region3";

    -- Apply the rule primary_rule_for_region1 to the corresponding user tables.
    ALTER TABLE tpcc.warehouse PLACEMENT POLICY=primary_rule_for_region1;
    ALTER TABLE tpcc.district PLACEMENT POLICY=primary_rule_for_region1;

    -- Note: You can modify the database name, table name, and placement rule name as needed.

    -- Confirm whether the leaders have been transferred by executing the following query to check the number of leaders in each region.
    SELECT STORE_ID, address, leader_count, label FROM TIKV_STORE_STATUS ORDER BY store_id;
    ```

    次の SQL ステートメントは、すべての非システム スキーマ テーブルのリーダーを特定の領域に構成する SQL スクリプトを生成できます。

    ```sql
    SET @region_name=primary_rule_for_region1;
    SELECT CONCAT('ALTER TABLE ', table_schema, '.', table_name, ' PLACEMENT POLICY=', @region_name, ';') FROM information_schema.tables WHERE table_schema NOT IN ('METRICS_SCHEMA', 'PERFORMANCE_SCHEMA', 'INFORMATION_SCHEMA','mysql');
    ```

## クラスターを監視する {#monitor-the-cluster}

Grafana または TiDB ダッシュボードにアクセスすることで、クラスター内の TiKV、TiDB、PD などのコンポーネントのパフォーマンス メトリックを監視できます。コンポーネントのステータスに基づいて、DR スイッチオーバーを実行するかどうかを判断できます。詳細については、次のドキュメントを参照してください。

-   [TiDB の主要な監視指標](/grafana-tidb-dashboard.md)
-   [TiKVの主要な監視指標](/grafana-tikv-dashboard.md)
-   [PDの主要な監視指標](/grafana-pd-dashboard.md)
-   [TiDBダッシュボード監視ページ](/dashboard/dashboard-monitoring.md)

## DRスイッチオーバーを実行する {#perform-a-dr-switchover}

このセクションでは、計画されたスイッチオーバーと計画外のスイッチオーバーを含む DR スイッチオーバーを実行する方法について説明します。

### 計画的な切り替え {#planned-switchover}

計画的スイッチオーバーは、メンテナンスのニーズに基づいてプライマリ リージョンとセカンダリ リージョン間でスケジュールされたスイッチオーバーです。これは、DR システムが正常に動作しているかどうかを確認するために使用できます。このセクションでは、計画的スイッチオーバーを実行する方法について説明します。

1.  次のコマンドを実行して、すべてのユーザー テーブルと PD リーダーをリージョン 2 に切り替えます。

    ```sql
    -- Apply the rule secondary_rule_for_region2 to the corresponding user tables.
    ALTER TABLE tpcc.warehouse PLACEMENT POLICY=secondary_rule_for_region2;
    ALTER TABLE tpcc.district PLACEMENT POLICY=secondary_rule_for_region2;
    ```

    注: 必要に応じて、データベース名、テーブル名、配置ルール名を変更できます。

    次のコマンドを実行して、リージョン 1 の PD ノードの優先度を下げ、リージョン 2 の PD ノードの優先度を上げます。

    ```shell
    tiup ctl:v6.4.0 pd member leader_priority pd-1 2
    tiup ctl:v6.4.0 pd member leader_priority pd-2 1
    tiup ctl:v6.4.0 pd member leader_priority pd-3 4
    tiup ctl:v6.4.0 pd member leader_priority pd-4 3
    ```

2.  Grafana で PD ノードと TiKV ノードを観察し、PD およびユーザー テーブルのリーダーがターゲット リージョンに転送されていることを確認します。元のリージョンに戻す手順は前の手順と同じであるため、このドキュメントでは説明しません。

### 計画外の切り替え {#unplanned-switchover}

計画外の切り替えとは、災害が発生したときにプライマリ リージョンとセカンダリ リージョン間で切り替えが行われることを意味します。また、DR システムの有効性を検証するために災害シナリオをシミュレートするために開始されるプライマリ リージョンとセカンダリ リージョン間の切り替えである場合もあります。

1.  次のコマンドを実行して、リージョン 1 内のすべての TiKV、TiDB、および PD ノードを停止します。

    ```shell
    tiup cluster stop drtest -N tidb-dr-test1:20160,tidb-dr-test2:20160,tidb-dr-test1:2379,tidb-dr-test2:2379
    ```

2.  次のコマンドを実行して、すべてのユーザー テーブルのリーダーをリージョン 2 に切り替えます。

    ```sql
    -- Apply the rule secondary_rule_for_region2 to the corresponding user tables.
    ALTER TABLE tpcc.warehouse PLACEMENT POLICY=secondary_rule_for_region2;
    ALTER TABLE tpcc.district PLACEMENT POLICY=secondary_rule_for_region2;

    --- Confirm whether the leaders have been transferred by executing the following query to check the number of leaders in each region.
    SELECT STORE_ID, address, leader_count, label FROM TIKV_STORE_STATUS ORDER BY store_id;
    ```

    リージョン 1 が回復したら、前述のコマンドと同様のコマンドを使用して、ユーザー テーブルのリーダーをリージョン 1 に戻すことができます。
