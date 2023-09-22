---
title: Two Availability Zones in One Region Deployment
summary: Learn the deployment solution of two availability zones in one region.
---

# 1 つのリージョンでの 2 つのアベイラビリティーゾーンの展開 {#two-availability-zones-in-one-region-deployment}

このドキュメントでは、アーキテクチャ、構成、このデプロイメント モードを有効にする方法、このモードでのレプリカの使用方法など、1 つのリージョン内の 2 つのアベイラビリティ ゾーン (AZ) のデプロイメント モードを紹介します。

このドキュメントの「リージョン」という用語は地理的エリアを指しますが、大文字の「リージョン」は TiKV のデータstorageの基本単位を指します。 「AZ」はリージョン内の孤立した場所を指し、各リージョンには複数の AZ があります。このドキュメントで説明されているソリューションは、複数のデータ センターが 1 つの都市にあるシナリオにも当てはまります。

## 導入 {#introduction}

TiDB は通常、高可用性と災害復旧機能を確保するためにマルチ AZ 展開ソリューションを採用しています。マルチ AZ デプロイメント ソリューションには、1 つのリージョンに複数の AZ、2 つのリージョンに複数の AZ など、複数のデプロイメント モードが含まれています。このドキュメントでは、1 つのリージョンに 2 つの AZ のデプロイメント モードを紹介します。このモードで導入すると、TiDB は低コストで高可用性と災害復旧の要件を満たすこともできます。この展開ソリューションは、データ レプリケーション自動同期モード、つまり DR 自動同期モードを採用しています。

1 つのリージョンに 2 つの AZ があるモードでは、2 つの AZ の距離は 50 キロメートル未満です。これらは通常、同じリージョンまたは 2 つの隣接するリージョンにあります。 2 つの AZ 間のネットワークレイテンシーは1.5 ミリ秒未満で、帯域幅は 10 Gbps を超えています。

## 導入アーキテクチャ {#deployment-architecture}

このセクションでは、2 つのアベイラビリティ ゾーン AZ1 と AZ2 がそれぞれ東と西に配置されているリージョンを例に挙げます。 AZ1 はプライマリ AZ、AZ2 はディザスター リカバリー (DR) AZ です。

クラスター展開のアーキテクチャは次のとおりです。

-   クラスターには 4 つのレプリカがあります。AZ1 に 2 つの投票者レプリカ、AZ2 に 1 つの投票者レプリカ、および 1 つのLearnerレプリカです。 TiKVコンポーネントの場合、各ラックには適切なラベルが付いています。
-   Raftプロトコルは、ユーザーにとって透過的なデータの一貫性と高可用性を確保するために採用されています。

![2-AZ-in-1-region architecture](/media/two-dc-replication-1.png)

この導入ソリューションでは、クラスターのレプリケーション ステータスを制御および識別するための 3 つのステータスを定義し、TiKV のレプリケーション モードを制限します。クラスターのレプリケーション モードは、3 つのステータス間を自動的かつ適応的に切り替えることができます。詳細は[ステータススイッチ](#status-switch)章を参照してください。

-   **sync** : 同期レプリケーション モード。このモードでは、ディザスター リカバリー AZ 内の少なくとも 1 つのレプリカがプライマリ AZ と同期します。 Raftアルゴリズムにより、各ログがラベルに基づいて確実に DR に複製されます。
-   **async** : 非同期レプリケーション モード。このモードでは、ディザスター リカバリー AZ はプライマリ AZ と完全には同期しません。 Raftアルゴリズムは、多数決プロトコルに従ってログを複製します。
-   **sync-recover** : 同期リカバリモード。このモードでは、ディザスター リカバリー AZ はプライマリ AZ と完全には同期しません。 Raft は徐々にラベル複製モードに切り替え、ラベル情報を PD に報告します。

## コンフィグレーション {#configuration}

### 例 {#example}

次の`tiup topology.yaml`ファイル例は、1 つのリージョン展開モードにおける 2 つのアベイラビリティ ゾーンの一般的なトポロジ構成です。

```yaml
# # Global variables are applied to all deployments and used as the default value of
# # the deployments if a specific deployment value is missing.
global:
  user: "tidb"
  ssh_port: 22
  deploy_dir: "/data/tidb_cluster/tidb-deploy"
  data_dir: "/data/tidb_cluster/tidb-data"
server_configs:
  pd:
    replication.location-labels: ["az","rack","host"]
pd_servers:
  - host: 10.63.10.10
    name: "pd-10"
  - host: 10.63.10.11
    name: "pd-11"
  - host: 10.63.10.12
    name: "pd-12"
tidb_servers:
  - host: 10.63.10.10
  - host: 10.63.10.11
  - host: 10.63.10.12
tikv_servers:
  - host: 10.63.10.30
    config:
      server.labels: { az: "east", rack: "east-1", host: "30" }
  - host: 10.63.10.31
    config:
      server.labels: { az: "east", rack: "east-2", host: "31" }
  - host: 10.63.10.32
    config:
      server.labels: { az: "east", rack: "east-3", host: "32" }
  - host: 10.63.10.33
    config:
      server.labels: { az: "west", rack: "west-1", host: "33" }
  - host: 10.63.10.34
    config:
      server.labels: { az: "west", rack: "west-2", host: "34" }
  - host: 10.63.10.35
    config:
      server.labels: { az: "west", rack: "west-3", host: "35" }
monitoring_servers:
  - host: 10.63.10.60
grafana_servers:
  - host: 10.63.10.60
alertmanager_servers:
  - host: 10.63.10.60
```

### 配置ルール {#placement-rules}

計画されたトポロジに基づいてクラスターをデプロイするには、 [配置ルール](/configure-placement-rules.md)を使用してクラスターのレプリカの場所を決定する必要があります。例として 4 つのレプリカの展開 (2 つの投票者レプリカがプライマリ AZ にあり、1 つの投票者レプリカと 1 つのLearnerレプリカがディザスター リカバリー AZ にあります) を例にとると、配置ルールを使用してレプリカを次のように構成できます。

    cat rule.json
    [
      {
        "group_id": "pd",
        "group_index": 0,
        "group_override": false,
        "rules": [
          {
            "group_id": "pd",
            "id": "az-east",
            "start_key": "",
            "end_key": "",
            "role": "voter",
            "count": 3,
            "label_constraints": [
              {
                "key": "az",
                "op": "in",
                "values": [
                  "east"
                ]
              }
            ],
            "location_labels": [
              "az",
              "rack",
              "host"
            ]
          },
          {
            "group_id": "pd",
            "id": "az-west-1",
            "start_key": "",
            "end_key": "",
            "role": "follower",
            "count": 2,
            "label_constraints": [
              {
                "key": "az",
                "op": "in",
                "values": [
                  "west"
                ]
              }
            ],
            "location_labels": [
              "az",
              "rack",
              "host"
            ]
          },
          {
            "group_id": "pd",
            "id": "az-west-2",
            "start_key": "",
            "end_key": "",
            "role": "learner",
            "count": 1,
            "label_constraints": [
              {
                "key": "az",
                "op": "in",
                "values": [
                  "west"
                ]
              }
            ],
            "location_labels": [
              "az",
              "rack",
              "host"
            ]
          }
        ]
      }
    ]

`rule.json`の構成を使用するには、次のコマンドを実行して既存の構成を`default.json`ファイルにバックアップし、既存の構成を`rule.json`で上書きします。

```bash
pd-ctl config placement-rules rule-bundle load --out="default.json"
pd-ctl config placement-rules rule-bundle save --in="rule.json"
```

以前の構成にロールバックする必要がある場合は、バックアップ ファイル`default.json`を復元するか、次の JSON ファイルを手動で書き込み、現在の構成をこの JSON ファイルで上書きします。

    cat default.json
    [
      {
        "group_id": "pd",
        "group_index": 0,
        "group_override": false,
        "rules": [
          {
            "group_id": "pd",
            "id": "default",
            "start_key": "",
            "end_key": "",
            "role": "voter",
            "count": 5
          }
        ]
      }
    ]

### DR 自動同期モードを有効にする {#enable-the-dr-auto-sync-mode}

レプリケーション モードは PD によって制御されます。次のいずれかの方法を使用して、PD 構成ファイルでレプリケーション モードを構成できます。

-   方法 1: PD 構成ファイルを構成し、クラスターをデプロイします。

    ```toml
    [replication-mode]
    replication-mode = "dr-auto-sync"
    [replication-mode.dr-auto-sync]
    label-key = "az"
    primary = "east"
    dr = "west"
    primary-replicas = 3
    dr-replicas = 2
    wait-store-timeout = "1m"
    ```

-   方法 2: クラスターを展開している場合は、pd-ctl コマンドを使用して PD の構成を変更します。

    ```shell
    config set replication-mode dr-auto-sync
    config set replication-mode dr-auto-sync label-key az
    config set replication-mode dr-auto-sync primary east
    config set replication-mode dr-auto-sync dr west
    config set replication-mode dr-auto-sync primary-replicas 3
    config set replication-mode dr-auto-sync dr-replicas 2
    ```

設定項目の説明:

-   `replication-mode`は、有効にするレプリケーション モードです。前の例では、 `dr-auto-sync`に設定されています。デフォルトでは、多数決プロトコルが使用されます。
-   `label-key`は異なる AZ を区別するために使用され、配置ルールと一致する必要があります。この例では、プライマリ AZ は「east」、ディザスタ リカバリ AZ は「west」です。
-   `primary-replicas`は、プライマリ AZ 内の Voter レプリカの数です。
-   `dr-replicas`は、ディザスタ リカバリ AZ 内の Voter レプリカの数です。
-   `wait-store-timeout` 、ネットワークの分離または障害が発生したときに非同期レプリケーション モードに切り替えるまでの待ち時間です。ネットワーク障害の時間が待機時間を超えると、非同期レプリケーション モードが有効になります。デフォルトの待機時間は 60 秒です。

クラスターの現在のレプリケーション ステータスを確認するには、次の API を使用します。

```bash
curl http://pd_ip:pd_port/pd/api/v1/replication_mode/status
```

```bash
{
  "mode": "dr-auto-sync",
  "dr-auto-sync": {
    "label-key": "az",
    "state": "sync"
  }
}
```

#### ステータススイッチ {#status-switch}

クラスターのレプリケーション モードは、次の 3 つのステータスを自動的かつ適応的に切り替えることができます。

-   クラスターが正常な場合、同期レプリケーション モードが有効になり、ディザスター リカバリー AZ のデータ整合性が最大化されます。
-   2 つの AZ 間のネットワーク接続に障害が発生するか、ディザスタ リカバリ AZ が故障すると、事前に設定された保護期間の後、クラスターは非同期レプリケーション モードを有効にしてアプリケーションの可用性を確保します。
-   ネットワークが再接続されるか、ディザスタ リカバリ AZ が回復すると、TiKV ノードは再びクラスターに参加し、データを段階的にレプリケートします。最後に、クラスターは同期レプリケーション モードに切り替わります。

ステータススイッチの詳細は次のとおりです。

1.  **初期化**: 初期化段階では、クラスターは同期レプリケーション モードになっています。 PD はステータス情報を TiKV に送信し、すべての TiKV ノードは同期レプリケーション モードに従って動作します。

2.  **同期から非同期に切り替える**: PD は TiKV のハートビート情報を定期的にチェックして、TiKV ノードに障害が発生したか、切断されているかを判断します。障害ノードの数がプライマリ AZ ( `primary-replicas` ) とディザスター リカバリー AZ ( `dr-replicas` ) のレプリカ数を超えると、同期レプリケーション モードではデータ レプリケーションを実行できなくなり、ステータスを切り替える必要があります。障害または切断時間が`wait-store-timeout`で設定された時間を超えると、PD はクラスターのステータスを非同期モードに切り替えます。次に、PD は非同期のステータスをすべての TiKV ノードに送信し、TiKV のレプリケーション モードが 2 つのアベイラビリティ ゾーン レプリケーションからネイティブRaftマジョリティに切り替わります。

3.  **非同期から同期への切り替え**: PD は定期的に TiKV のハートビート情報をチェックし、TiKV ノードが再接続されているかどうかを判断します。障害が発生したノードの数がプライマリ AZ ( `primary-replicas` ) およびディザスター リカバリー AZ ( `dr-replicas` ) のレプリカ数よりも少ない場合は、同期レプリケーション モードを再度有効にすることができます。 PD はまずクラスターのステータスを同期回復に切り替え、ステータス情報をすべての TiKV ノードに送信します。 TiKV のすべてのリージョンは、2 つのアベイラビリティ ゾーンの同期レプリケーション モードに徐々に切り替わり、ハートビート情報を PD に報告します。 PD は TiKV リージョンのステータスを記録し、復旧の進行状況を計算します。すべての TiKV リージョンの切り替えが完了すると、PD はレプリケーション モードを同期に切り替えます。

### 災害からの回復 {#disaster-recovery}

このセクションでは、1 つのリージョンに 2 つの AZ を展開する災害復旧ソリューションを紹介します。

同期レプリケーション モードでクラスターに障害が発生した場合、 `RPO = 0`でデータ復旧を実行できます。

-   プライマリ AZ に障害が発生し、Voter レプリカの大部分が失われた場合でも、完全なデータがディザスター リカバリー AZ に存在する場合、失われたデータはディザスター リカバリー AZ から復元できます。現時点では、専門ツールを使用した手動介入が必要です。 [支持を得ます](/support.md)回復ソリューションについては、PingCAP またはコミュニティから入手できます。

-   ディザスター リカバリー AZ が失敗し、いくつかの Voter レプリカが失われた場合、クラスターは自動的に非同期レプリケーション モードに切り替わります。

同期レプリケーション モードではないクラスターに障害が発生し、 `RPO = 0`でデータ復旧を実行できない場合:

-   Voter レプリカの大部分が失われた場合は、専門ツールを使用して手動で介入する必要があります。 [支持を得ます](/support.md)回復ソリューションについては、PingCAP またはコミュニティから入手できます。
