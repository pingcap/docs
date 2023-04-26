---
title: Two Availability Zones in One Region Deployment
summary: Learn the deployment solution of two availability zones in one region.
---

# 1 つのリージョンデプロイでの 2 つのアベイラビリティー ゾーン {#two-availability-zones-in-one-region-deployment}

このドキュメントでは、アーキテクチャ、構成、このデプロイ モードを有効にする方法、このモードでレプリカを使用する方法など、1 つのリージョンに 2 つのアベイラビリティ ゾーン (AZ) のデプロイ モードを紹介します。

このドキュメントの「地域」という用語は地理的な領域を指し、大文字の「リージョン」は TiKV のデータstorageの基本単位を指します。 「AZ」はリージョン内の孤立した場所を指し、各リージョンには複数の AZ があります。このドキュメントで説明するソリューションは、1 つの都市に複数のデータ センターが配置されているシナリオにも適用されます。

## 序章 {#introduction}

TiDB は通常、マルチ AZ 配置ソリューションを採用して、高可用性と災害復旧機能を確保します。マルチ AZ 配置ソリューションには、1 つのリージョンに複数の AZ、2 つのリージョンに複数の AZ など、複数の配置モードが含まれています。このドキュメントでは、1 つのリージョンに 2 つの AZ を配置するモードを紹介します。このモードで展開された TiDB は、低コストで高可用性と災害復旧の要件を満たすこともできます。この展開ソリューションは、データ レプリケーション自動同期モードまたは DR 自動同期モードを採用しています。

1 つのリージョンに 2 つの AZ があるモードでは、2 つの AZ の距離は 50 キロメートル未満です。これらは通常、同じリージョンまたは隣接する 2 つのリージョンにあります。 2 つの AZ 間のネットワークレイテンシーは1.5 ミリ秒未満であり、帯域幅は 10 Gbps を超えています。

## 導入アーキテクチャ {#deployment-architecture}

このセクションでは、2 つのアベイラビリティーゾーン AZ1 と AZ2 がそれぞれ東と西にあるリージョンの例を取り上げます。 AZ1 はプライマリ AZ で、AZ2 はディザスター リカバリー (DR) AZ です。

クラスタ展開のアーキテクチャは次のとおりです。

-   クラスターには 4 つのレプリカがあります。AZ1 に 2 つの投票者レプリカ、AZ2 に 1 つの投票者レプリカ、1 つのLearnerレプリカです。 TiKVコンポーネントの場合、各ラックには適切なラベルが付いています。
-   Raftプロトコルは、データの一貫性と高可用性を確保するために採用されており、ユーザーに対して透過的です。

![2-AZ-in-1-region architecture](/media/two-dc-replication-1.png)

この展開ソリューションは、TiKV のレプリケーション モードを制限するクラスターのレプリケーション ステータスを制御および識別するために 3 つのステータスを定義します。クラスタのレプリケーション モードは、3 つのステータス間で自動的かつ適応的に切り替えることができます。詳細は、 [ステータススイッチ](#status-switch)節を参照してください。

-   **sync** : 同期レプリケーション モード。このモードでは、ディザスタ リカバリ AZ 内の少なくとも 1 つのレプリカがプライマリ AZ と同期します。 Raftアルゴリズムは、各ログがラベルに基づいて DR に複製されることを保証します。
-   **async** : 非同期レプリケーション モード。このモードでは、災害復旧 AZ はプライマリ AZ と完全には同期されません。 Raftアルゴリズムは多数決プロトコルに従ってログを複製します。
-   **sync-recover** : 同期回復モード。このモードでは、災害復旧 AZ はプライマリ AZ と完全には同期されません。 Raft は徐々にラベル複製モードに切り替え、ラベル情報を PD に報告します。

## コンフィグレーション {#configuration}

### 例 {#example}

次の`tiup topology.yaml`サンプル ファイルは、1 つのリージョン デプロイ モードでの 2 つのアベイラビリティ ゾーンの一般的なトポロジ構成です。

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

計画されたトポロジーに基づいてクラスターをデプロイするには、 [配置ルール](/configure-placement-rules.md)を使用してクラスターのレプリカの場所を決定する必要があります。例として、4 つのレプリカ (2 つの投票者レプリカがプライマリ AZ にあり、1 つの投票者レプリカと 1 つのLearnerレプリカが災害復旧 AZ にあります) の展開を取り上げると、次のように配置ルールを使用してレプリカを構成できます。

```
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
        "id": "az-west",
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
        "id": "az-west",
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
```

`rule.json`の構成を使用するには、次のコマンドを実行して既存の構成を`default.json`ファイルにバックアップし、既存の構成を`rule.json`で上書きします。

{{< copyable "" >}}

```bash
pd-ctl config placement-rules rule-bundle load --out="default.json"
pd-ctl config placement-rules rule-bundle save --in="rule.json"
```

以前の構成にロールバックする必要がある場合は、バックアップ ファイル`default.json`を復元するか、次の JSON ファイルを手動で書き込んで、現在の構成をこの JSON ファイルで上書きすることができます。

```
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
```

### DR 自動同期モードを有効にする {#enable-the-dr-auto-sync-mode}

複製モードは PD によって制御されます。次のいずれかの方法を使用して、PD 構成ファイルでレプリケーション モードを構成できます。

-   方法 1: PD 構成ファイルを構成してから、クラスターをデプロイします。

    {{< copyable "" >}}

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

-   方法 2: クラスターをデプロイした場合は、pd-ctl コマンドを使用して PD の構成を変更します。

    {{< copyable "" >}}

    ```shell
    config set replication-mode dr-auto-sync
    config set replication-mode dr-auto-sync label-key az
    config set replication-mode dr-auto-sync primary east
    config set replication-mode dr-auto-sync dr west
    config set replication-mode dr-auto-sync primary-replicas 3
    config set replication-mode dr-auto-sync dr-replicas 2
    ```

構成項目の説明:

-   `replication-mode`は有効にする複製モードです。前の例では、 `dr-auto-sync`に設定されています。デフォルトでは、マジョリティ プロトコルが使用されます。
-   `label-key`は異なる AZ を区別するために使用され、配置ルールに一致する必要があります。この例では、プライマリ AZ は「東」であり、災害復旧 AZ は「西」です。
-   `primary-replicas`は、プライマリ AZ 内の Voter レプリカの数です。
-   `dr-replicas`は、災害復旧 AZ 内の Voter レプリカの数です。
-   `wait-store-timeout` 、ネットワークの分離または障害が発生したときに、非同期レプリケーション モードに切り替えるための待機時間です。ネットワーク障害の時間が待機時間を超えると、非同期レプリケーション モードが有効になります。デフォルトの待機時間は 60 秒です。

クラスターの現在のレプリケーション ステータスを確認するには、次の API を使用します。

{{< copyable "" >}}

```bash
curl http://pd_ip:pd_port/pd/api/v1/replication_mode/status
```

{{< copyable "" >}}

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

クラスタのレプリケーション モードは、次の 3 つのステータス間で自動的かつ適応的に切り替えることができます。

-   クラスターが正常な場合、同期レプリケーション モードが有効になり、災害復旧 AZ のデータ整合性が最大化されます。
-   2 つの AZ 間のネットワーク接続に障害が発生した場合、または災害復旧 AZ が故障した場合、事前に設定された保護間隔の後、クラスターは非同期レプリケーション モードを有効にして、アプリケーションの可用性を確保します。
-   ネットワークが再接続されるか、災害復旧 AZ が回復すると、TiKV ノードは再びクラスターに参加し、徐々にデータを複製します。最後に、クラスターは同期レプリケーション モードに切り替わります。

ステータススイッチの詳細は次のとおりです。

1.  **初期化**: 初期化段階では、クラスターは同期レプリケーション モードになっています。 PD はステータス情報を TiKV に送信し、すべての TiKV ノードは同期レプリケーション モードに厳密に従って動作します。

2.  **同期から非同期への切り替え**: PD は TiKV のハートビート情報を定期的にチェックして、TiKV ノードが故障しているか、切断されているかを判断します。障害が発生したノードの数が、プライマリ AZ ( `primary-replicas` ) およびディザスター リカバリー AZ ( `dr-replicas` ) のレプリカの数を超える場合、同期レプリケーション モードはデータ レプリケーションを提供できなくなり、状態を切り替える必要があります。障害または切断時間が`wait-store-timeout`で設定された時間を超えると、PD はクラスターのステータスを非同期モードに切り替えます。その後、PD は非同期のステータスをすべての TiKV ノードに送信し、TiKV のレプリケーション モードは、2 つのアベイラビリティ ゾーンのレプリケーションからネイティブRaftマジョリティに切り替わります。

3.  **async から sync への切り替え**: PD は TiKV のハートビート情報を定期的にチェックして、TiKV ノードが再接続されているかどうかを判断します。障害が発生したノードの数が、プライマリ AZ ( `primary-replicas` ) およびディザスター リカバリー AZ ( `dr-replicas` ) のレプリカの数よりも少ない場合は、同期レプリケーション モードを再び有効にすることができます。 PD は、最初にクラスターのステータスを同期回復に切り替え、ステータス情報をすべての TiKV ノードに送信します。 TiKV のすべてのリージョンは、2 つの可用性ゾーンの同期レプリケーション モードに徐々に切り替わり、ハートビート情報を PD に報告します。 PD は TiKV リージョンのステータスを記録し、復旧の進行状況を計算します。すべての TiKV リージョンが切り替えを完了すると、PD はレプリケーション モードを同期に切り替えます。

### 災害からの回復 {#disaster-recovery}

このセクションでは、1 つのリージョンに配置された 2 つの AZ のディザスター リカバリー ソリューションを紹介します。

同期レプリケーション モードのクラスタに障害が発生した場合、次の`RPO = 0`を使用してデータ リカバリを実行できます。

-   プライマリ AZ に障害が発生し、Voter レプリカのほとんどが失われたが、災害復旧 AZ に完全なデータが存在する場合、失われたデータは災害復旧 AZ から復旧できます。現時点では、プロのツールを使用して手動で介入する必要があります。リカバリ ソリューションについては、PingCAP またはコミュニティから[支持を得ます](/support.md)できます。

-   災害復旧 AZ が失敗し、いくつかの Voter レプリカが失われた場合、クラスターは自動的に非同期レプリケーション モードに切り替わります。

同期レプリケーションモードではないクラスタに障害が発生し、 `RPO = 0`でデータリカバリを実行できない場合:

-   投票者のレプリカのほとんどが失われた場合は、専門的なツールを使用して手動で介入する必要があります。リカバリ ソリューションについては、PingCAP またはコミュニティから[支持を得ます](/support.md)できます。
