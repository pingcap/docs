---
title: Two Availability Zones in One Region Deployment
summary: 1 つのリージョンに 2 つの可用性ゾーンを展開するソリューションについて学習します。
---

# 1 つのリージョンに 2 つのアベイラビリティ ゾーンを展開 {#two-availability-zones-in-one-region-deployment}

このドキュメントでは、アーキテクチャ、構成、このデプロイメント モードを有効にする方法、このモードでレプリカを使用する方法など、1 つのリージョンに 2 つのアベイラビリティ ゾーン (AZ) を配置するデプロイメント モードについて説明します。

このドキュメントの「リージョン」という用語は地理的なエリアを指し、大文字の「リージョン」は TiKV のデータstorageの基本単位を指します。「AZ」はリージョン内の隔離された場所を指し、各リージョンには複数の AZ があります。このドキュメントで説明されているソリューションは、1 つの都市に複数のデータ センターがあるシナリオにも適用されます。

## 導入 {#introduction}

TiDB は通常、高可用性と災害復旧機能を確保するために、マルチ AZ デプロイメント ソリューションを採用しています。マルチ AZ デプロイメント ソリューションには、1 つのリージョンに複数の AZ を配置したり、2 つのリージョンに複数の AZ を配置するなど、複数のデプロイメント モードが含まれます。このドキュメントでは、1 つのリージョンに 2 つの AZ を配置するデプロイメント モードを紹介します。このモードでデプロイすると、TiDB は低コストで高可用性と災害復旧の要件も満たすことができます。このデプロイメント ソリューションは、データ レプリケーション自動同期モード、または DR 自動同期モードを採用しています。

1 つのリージョンに 2 つの AZ を配置するモードでは、2 つの AZ の距離は 50 キロメートル未満です。通常、これらは同じリージョンまたは 2 つの隣接するリージョンに配置されます。2 つの AZ 間のネットワークレイテンシーは1.5 ミリ秒未満で、帯域幅は 10 Gbps を超えます。

## デプロイメントアーキテクチャ {#deployment-architecture}

このセクションでは、AZ1 と AZ2 という 2 つのアベイラビリティ ゾーンがそれぞれ東と西に配置されているリージョンの例を取り上げます。AZ1 はプライマリ AZ で、AZ2 はディザスタ リカバリ (DR) AZ です。

クラスター展開のアーキテクチャは次のとおりです。

-   クラスターには 6 つのレプリカがあります。AZ1 には 3 つの Voter レプリカ、AZ2 には 2 つの Voter レプリカと 1 つのLearnerレプリカがあります。TiKVコンポーネントの場合、各ラックには適切なラベルがあります。
-   ユーザーにとって透過的なデータの一貫性と高可用性を確保するために、 Raftプロトコルが採用されています。

![2-AZ-in-1-region architecture](/media/two-dc-replication-1.png)

このデプロイメント ソリューションでは、クラスターのレプリケーション ステータスを制御および識別するための 3 つのステータスを定義し、TiKV のレプリケーション モードを制限します。クラスターのレプリケーション モードは、3 つのステータス間で自動的かつ適応的に切り替えることができます。詳細については、セクション[ステータススイッチ](#status-switch)を参照してください。

-   **sync** : 同期レプリケーション モード。このモードでは、災害復旧 AZ 内の少なくとも 1 つのレプリカがプライマリ AZ と同期します。Raft アルゴリズムにより、各ログがラベルに基づいて DR にレプリケートされます。
-   **async** : 非同期レプリケーション モード。このモードでは、災害復旧 AZ はプライマリ AZ と完全に同期されません。Raft アルゴリズムは、Raftプロトコルに従ってログをレプリケートします。
-   **sync-recover** : 同期リカバリモード。このモードでは、災害復旧 AZ はプライマリ AZ と完全に同期されていません。Raftは徐々にラベル レプリケーション モードに切り替わり、ラベル情報を PD に報告します。

## コンフィグレーション {#configuration}

### 例 {#example}

次の`tiup topology.yaml`サンプル ファイルは、1 つのリージョン展開モードにおける 2 つの可用性ゾーンの一般的なトポロジ構成です。

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

計画されたトポロジに基づいてクラスターをデプロイするには、 [配置ルール](/configure-placement-rules.md)を使用してクラスター レプリカの場所を決定する必要があります。4 つのレプリカのデプロイ (2 つの Voter レプリカはプライマリ AZ に、1 つの Voter レプリカと 1 つのLearnerレプリカは災害復旧 AZ に) を例にとると、配置ルールを使用してレプリカを次のように構成できます。

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

`rule.json`の設定を使用するには、次のコマンドを実行して既存の設定を`default.json`ファイルにバックアップし、既存の設定を`rule.json`で上書きします。

```bash
pd-ctl config placement-rules rule-bundle load --out="default.json"
pd-ctl config placement-rules rule-bundle save --in="rule.json"
```

以前の構成にロールバックする必要がある場合は、バックアップ ファイル`default.json`を復元するか、次の JSON ファイルを手動で作成し、この JSON ファイルで現在の構成を上書きします。

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

### DR自動同期モードを有効にする {#enable-the-dr-auto-sync-mode}

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
    wait-recover-timeout = "0s"
    pause-region-split = false  
    ```

-   方法 2: クラスターをデプロイしている場合は、pd-ctl コマンドを使用して PD の構成を変更します。

    ```shell
    config set replication-mode dr-auto-sync
    config set replication-mode dr-auto-sync label-key az
    config set replication-mode dr-auto-sync primary east
    config set replication-mode dr-auto-sync dr west
    config set replication-mode dr-auto-sync primary-replicas 3
    config set replication-mode dr-auto-sync dr-replicas 2
    ```

構成項目の説明:

-   `replication-mode`は有効にするレプリケーション モードです。前の例では、 `dr-auto-sync`に設定されています。デフォルトでは、多数決プロトコルが使用されます。
-   `label-key`は異なる AZ を区別するために使用され、配置ルールと一致する必要があります。この例では、プライマリ AZ は「east」で、災害復旧 AZ は「west」です。
-   `primary-replicas`はプライマリ AZ 内の Voter レプリカの数です。
-   `dr-replicas`は、災害復旧 (DR) AZ 内の投票者レプリカの数です。
-   `wait-store-timeout` 、ネットワークの分離または障害が発生したときに、非同期レプリケーション モードに切り替えるための待機時間です。ネットワーク障害の時間が待機時間を超えると、非同期レプリケーション モードが有効になります。デフォルトの待機時間は 60 秒です。
-   `wait-recover-timeout` 、ネットワークが回復した後に`sync-recover`状態に戻るまでの待機時間です。デフォルト値は 0 秒です。
-   `pause-region-split` 、ステータス`async_wait`および`async`でリージョン分割操作を一時停止するかどうかを制御します。リージョン分割を一時停止すると、ステータス`sync-recover`でデータを同期するときに DR AZ で一時的な部分的なデータ損失を防ぐことができます。デフォルト値は`false`です。

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

クラスターのレプリケーション モードは、次の 3 つのステータス間を自動的かつ適応的に切り替えることができます。

-   クラスターが正常な場合、同期レプリケーション モードが有効になり、災害復旧 AZ のデータ整合性が最大化されます。
-   2 つの AZ 間のネットワーク接続に障害が発生したり、災害復旧 AZ が故障したりすると、事前に設定された保護間隔の後に、クラスターは非同期レプリケーション モードを有効にして、アプリケーションの可用性を確保します。
-   ネットワークが再接続するか、災害復旧 AZ が復旧すると、TiKV ノードは再びクラスターに参加し、データを徐々に複製します。最後に、クラスターは同期レプリケーション モードに切り替わります。

ステータススイッチの詳細は次のとおりです。

1.  **初期化**: 初期化段階では、クラスターは同期レプリケーション モードになります。PD はステータス情報を TiKV に送信し、すべての TiKV ノードは同期レプリケーション モードに厳密に従って動作します。

2.  **同期から非同期への切り替え**：PD は TiKV のハートビート情報を定期的にチェックし、TiKV ノードに障害が発生したか、切断されたかを判断します。障害が発生したノードの数がプライマリ AZ ( `primary-replicas` ) と災害復旧 AZ ( `dr-replicas` ) のレプリカ数を超えると、同期レプリケーション モードではデータ レプリケーションを提供できなくなり、ステータスを切り替える必要があります。障害または切断の時間が`wait-store-timeout`で設定された時間を超えると、PD はクラスターのステータスを非同期モードに切り替えます。次に、PD はすべての TiKV ノードに非同期のステータスを送信し、TiKV のレプリケーション モードが 2 つのアベイラビリティ ゾーンのレプリケーションからネイティブのRaftマジョリティに切り替わります。

3.  **非同期から同期への切り替え**：PD は TiKV のハートビート情報を定期的にチェックし、TiKV ノードが再接続されているかどうかを判断します。障害が発生したノードの数がプライマリ AZ ( `primary-replicas` ) と災害復旧 AZ ( `dr-replicas` ) のレプリカ数より少ない場合、同期レプリケーション モードを再度有効にできます。PD は最初にクラスターのステータスを同期回復に切り替え、ステータス情報をすべての TiKV ノードに送信します。TiKV のすべてのリージョンは、2 つのアベイラビリティ ゾーンの同期レプリケーション モードに徐々に切り替わり、ハートビート情報を PD に報告します。PD は TiKV リージョンのステータスを記録し、回復の進行状況を計算します。すべての TiKV リージョンの切り替えが完了すると、PD はレプリケーション モードを同期に切り替えます。

### 災害からの回復 {#disaster-recovery}

このセクションでは、1 つのリージョン展開における 2 つの AZ の災害復旧ソリューションを紹介します。

同期レプリケーションモードのクラスタに災害が発生した場合、 `RPO = 0`でデータ復旧を実行できます。

-   プライマリ AZ に障害が発生し、Voter レプリカのほとんどが失われたが、災害復旧 AZ に完全なデータが存在する場合、失われたデータは災害復旧 AZ から回復できます。このとき、専門ツールを使用した手動介入が必要です。回復ソリューションについては、PingCAP またはコミュニティから[支持を得ます](/support.md)入手できます。

-   災害復旧 AZ に障害が発生し、いくつかの Voter レプリカが失われた場合、クラスターは自動的に非同期レプリケーション モードに切り替わります。

同期レプリケーション モードではないクラスタに災害が発生し、 `RPO = 0`でデータ復旧を実行できない場合:

-   Voter レプリカのほとんどが失われた場合は、専門ツールを使用した手動介入が必要です。回復ソリューションについては、PingCAP またはコミュニティから[支持を得ます](/support.md)入手できます。
