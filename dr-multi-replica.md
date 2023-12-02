---
title: DR Solution Based on Multiple Replicas in a Single Cluster
summary: Learn about the multi-replica disaster recovery solution for a single cluster.
---

# 単一クラスタ内の複数のレプリカに基づく DR ソリューション {#dr-solution-based-on-multiple-replicas-in-a-single-cluster}

このドキュメントでは、単一クラスター内の複数のレプリカに基づく災害復旧 (DR) ソリューションについて説明します。この文書は次のように構成されています。

-   ソリューションの紹介
-   クラスターをセットアップしてレプリカを構成する方法
-   クラスターを監視する方法
-   DR スイッチオーバーを実行する方法

## 導入 {#introduction}

重要な本番システムには通常、ゼロ RPO と分単位の RTO を備えた地域的な DR が必要です。 Raft ベースの分散データベースである TiDB は複数のレプリカを提供するため、データの一貫性と高可用性が保証された地域 DR をサポートできます。同じリージョン内のアベイラブル ゾーン (AZ) 間のネットワークレイテンシーが小さいことを考慮すると、ビジネス トラフィックを同じリージョン上の 2 つの AZ に同時にディスパッチし、リージョンリーダーと PD リーダーを適切に配置することで、同じリージョン上の AZ 間の負荷分散を実現できます。 。

> **注記：**
>
> [TiKVの「リージョン」](/glossary.md#regionpeerraft-group)データの範囲を意味し、「領域」という用語は物理的な位置を意味します。この 2 つの用語は互換性がありません。

## クラスターをセットアップし、レプリカを構成する {#set-up-a-cluster-and-configure-replicas}

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

          raftstore.raft-min-election-timeout-ticks: 1000
          raftstore.raft-max-election-timeout-ticks: 1200

    monitoring_servers:
      - host: tidb-dr-test2

    grafana_servers:
      - host: tidb-dr-test2

    alertmanager_servers:
      - host: tidb-dr-test2
    ```

    前述の構成では、クロスリージョン DR に向けて最適化するために次のオプションを使用します。

    -   `server.grpc-compression-type: gzip`を指定すると、TiKV での gRPC メッセージ圧縮が有効になり、ネットワーク トラフィックが削減されます。
    -   `raftstore.raft-min-election-timeout-ticks`と`raftstore.raft-max-election-timeout-ticks`使用して、リージョン 3 が選挙に参加するまでの時間を延長します。これにより、このリージョン内のレプリカがリーダーとして投票されなくなります。

2.  前述の構成ファイルを使用してクラスターを作成します。

    ```shell
    tiup cluster deploy drtest v6.4.0 ./topo.yaml
    tiup cluster start drtest --init
    tiup cluster display drtest
    ```

    クラスターのレプリカの数とリーダー制限を構成します。

    ```shell
    tiup ctl:v6.4.0 pd config set max-replicas 5
    tiup ctl:v6.4.0 pd config set label-property reject-leader Region Region3

    # The following step adds some test data to the cluster, which is optional.
    tiup bench tpcc  prepare -H 127.0.0.1 -P 4000 -D tpcc --warehouses 1
    ```

    PD リーダーの優先順位を指定します。

    ```shell
    tiup ctl:v6.4.0 pd member leader_priority  pd-1 4
    tiup ctl:v6.4.0 pd member leader_priority  pd-2 3
    tiup ctl:v6.4.0 pd member leader_priority  pd-3 2
    tiup ctl:v6.4.0 pd member leader_priority  pd-4 1
    tiup ctl:v6.4.0 pd member leader_priority  pd-5 0
    ```

    > **注記：**
    >
    > 優先順位の数値が大きいほど、このノードがリーダーになる確率が高くなります。

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

    次の SQL ステートメントは、すべての非システム スキーマ テーブルのリーダーを特定のリージョンに構成する SQL スクリプトを生成できます。

    ```sql
    SET @region_name=primary_rule_for_region1;
    SELECT CONCAT('ALTER TABLE ', table_schema, '.', table_name, ' PLACEMENT POLICY=', @region_name, ';') FROM information_schema.tables WHERE table_schema NOT IN ('METRICS_SCHEMA', 'PERFORMANCE_SCHEMA', 'INFORMATION_SCHEMA','mysql');
    ```

## クラスターを監視する {#monitor-the-cluster}

Grafana または TiDB ダッシュボードにアクセスして、クラスター内の TiKV、TiDB、PD、およびその他のコンポーネントのパフォーマンス メトリックを監視できます。コンポーネントのステータスに基づいて、DR スイッチオーバーを実行するかどうかを決定できます。詳細については、次のドキュメントを参照してください。

-   [TiDB の主要なモニタリング指標](/grafana-tidb-dashboard.md)
-   [TiKV の主要なモニタリング指標](/grafana-tikv-dashboard.md)
-   [PD の主要なモニタリング指標](/grafana-pd-dashboard.md)
-   [TiDB ダッシュボード監視ページ](/dashboard/dashboard-monitoring.md)

## DR スイッチオーバーを実行する {#perform-a-dr-switchover}

このセクションでは、計画的スイッチオーバーと計画外のスイッチオーバーを含む DR スイッチオーバーを実行する方法について説明します。

### 計画的な切り替え {#planned-switchover}

計画的スイッチオーバーは、メンテナンスのニーズに基づいてプライマリ リージョンとセカンダリ リージョンの間でスケジュールされたスイッチオーバーです。 DR システムが適切に動作しているかどうかを検証するために使用できます。このセクションでは、計画的なスイッチオーバーを実行する方法について説明します。

1.  次のコマンドを実行して、すべてのユーザー テーブルと PD リーダーをリージョン 2 に切り替えます。

    ```sql
    -- Apply the rule secondary_rule_for_region2 to the corresponding user tables.
    ALTER TABLE tpcc.warehouse PLACEMENT POLICY=secondary_rule_for_region2;
    ALTER TABLE tpcc.district PLACEMENT POLICY=secondary_rule_for_region2;
    ```

    注: 必要に応じて、データベース名、テーブル名、配置ルール名を変更できます。

    次のコマンドを実行して、リージョン 1 の PD ノードの優先順位を下げ、リージョン 2 の PD ノードの優先順位を上げます。

    ```shell
    tiup ctl:v6.4.0 pd member leader_priority pd-1 2
    tiup ctl:v6.4.0 pd member leader_priority pd-2 1
    tiup ctl:v6.4.0 pd member leader_priority pd-3 4
    tiup ctl:v6.4.0 pd member leader_priority pd-4 3
    ```

2.  Grafana の PD ノードと TiKV ノードを観察し、PD とユーザー テーブルのリーダーがターゲット リージョンに転送されていることを確認します。元のリージョンに戻す手順は前述の手順と同じであるため、このドキュメントでは説明しません。

### 計画外のスイッチオーバー {#unplanned-switchover}

計画外のスイッチオーバーとは、災害発生時のプライマリ リージョンとセカンダリ リージョン間のスイッチオーバーを意味します。また、災害シナリオをシミュレートして DR システムの有効性を検証するために開始されるプライマリ - セカンダリ リージョンの切り替えであることもできます。

1.  次のコマンドを実行して、リージョン 1 のすべての TiKV、TiDB、および PD ノードを停止します。

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
