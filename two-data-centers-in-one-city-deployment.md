---
title: Two Availability Zones in One Region Deployment
summary: 1 つのリージョンに 2 つの可用性ゾーンを展開するソリューションについて学習します。
---

# 1つのリージョンに2つのアベイラビリティゾーンを展開 {#two-availability-zones-in-one-region-deployment}

このドキュメントでは、アーキテクチャ、構成、このデプロイメント モードを有効にする方法、このモードでレプリカを使用する方法など、1 つのリージョン内の 2 つのアベイラビリティ ゾーン (AZ) のデプロイメント モードについて説明します。

このドキュメントにおける「リージョン」という用語は地理的な領域を指し、「リージョン」はTiKVにおけるデータstorageの基本単位を指します。「AZ」はリージョン内の独立した場所を指し、各リージョンには複数のAZが存在します。このドキュメントで説明するソリューションは、単一の都市に複数のデータセンターが存在するシナリオにも適用されます。

## 導入 {#introduction}

TiDBは通常、高可用性と災害復旧機能を確保するために、マルチAZ配置ソリューションを採用しています。マルチAZ配置ソリューションには、1つのリージョンに複数のAZを配置する、2つのリージョンに複数のAZを配置するなど、複数の配置モードがあります。このドキュメントでは、1つのリージョンに2つのAZを配置する配置モードを紹介します。このモードで配置することで、TiDBは低コストで高可用性と災害復旧の要件を満たすことができます。この配置ソリューションは、データレプリケーション自動同期モード、またはDR自動同期モードを採用しています。

1つのリージョンに2つのAZを配置するモードでは、2つのAZ間の距離は50キロメートル未満です。通常、これらは同じリージョンまたは隣接する2つのリージョンに配置されます。2つのAZ間のネットワークレイテンシーは1.5ミリ秒未満で、帯域幅は10Gbpsを超えます。

## デプロイメントアーキテクチャ {#deployment-architecture}

このセクションでは、AZ1 と AZ2 という 2 つのアベイラビリティゾーンがそれぞれ東と西に配置されているリージョンを例に説明します。AZ1 はプライマリ AZ で、AZ2 は災害復旧 (DR) AZ です。

クラスター展開のアーキテクチャは次のとおりです。

-   クラスターには6つのレプリカがあります。AZ1には3つのVoterレプリカ、AZ2には2つのVoterレプリカと1つのLearnerレプリカがあります。TiKVコンポーネントでは、各ラックに適切なラベルが付けられています。
-   ユーザーにとって透過的なデータの一貫性と高可用性を確保するために、 Raftプロトコルが採用されています。

![2-AZ-in-1-region architecture](/media/two-dc-replication-1.png)

このデプロイメントソリューションでは、クラスタのレプリケーション状態を制御および識別するために3つのステータスを定義しており、これによりTiKVのレプリケーションモードが制限されます。クラスタのレプリケーションモードは、3つのステータス間を自動的かつ適応的に切り替えることができます。詳細については、セクション[ステータススイッチ](#status-switch)ご覧ください。

-   **sync** : 同期レプリケーションモード。このモードでは、災害復旧AZ内の少なくとも1つのレプリカがプライマリAZと同期します。RaftRaftにより、各ログはラベルに基づいてDRに複製されます。
-   **async** : 非同期レプリケーションモード。このモードでは、ディザスタリカバリAZはプライマリAZと完全に同期されません。RaftアルゴリズムはRaftプロトコルに従ってログを複製します。
-   **sync-recover** : 同期リカバリモード。このモードでは、ディザスタリカバリAZはプライマリAZと完全に同期されていません。Raftは徐々にラベルレプリケーションモードに切り替え、ラベル情報をPDに報告します。

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

計画されたトポロジに基づいてクラスターをデプロイするには、 [配置ルール](/configure-placement-rules.md)使用してクラスターレプリカの配置場所を決定する必要があります。4 つのレプリカ（Voter レプリカ 2 つをプライマリ AZ、Voter レプリカ 1 つをディザスタリカバリ AZ に、 Learnerレプリカ 1 つをディザスタリカバリ AZ に配置）のデプロイを例に挙げると、配置ルールを使用してレプリカを次のように設定できます。

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

レプリケーションモードはPDによって制御されます。PD設定ファイルでレプリケーションモードを設定するには、以下のいずれかの方法を使用します。

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

-   `replication-mode`は有効にするレプリケーションモードです。上記の例では`dr-auto-sync`に設定されています。デフォルトでは、多数決プロトコルが使用されます。
-   `label-key`は異なる AZ を区別するために使用され、配置ルールに一致する必要があります。この例では、プライマリ AZ は「east」、災害復旧 AZ は「west」です。
-   `primary-replicas`はプライマリ AZ 内の Voter レプリカの数です。
-   `dr-replicas`は、災害復旧 (DR) AZ 内の投票者レプリカの数です。
-   `wait-store-timeout` 、ネットワークの分離または障害発生時に非同期レプリケーションモードに切り替えるまでの待機時間です。ネットワーク障害の時間が待機時間を超えると、非同期レプリケーションモードが有効になります。デフォルトの待機時間は60秒です。
-   `wait-recover-timeout` 、ネットワークが回復した後に状態`sync-recover`に戻るまでの待機時間です。デフォルト値は0秒です。
-   `pause-region-split` 、ステータス`async_wait`および`async`においてリージョン分割操作を一時停止するかどうかを制御します。リージョン分割を一時停止すると、ステータス`sync-recover`でデータを同期する際に DR AZ で一時的な部分的なデータ損失が発生するのを防ぐことができます。デフォルト値は`false`です。

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

-   クラスターが正常な場合、同期レプリケーション モードが有効になり、災害復旧 AZ のデータ整合性が最大限に高まります。
-   2 つの AZ 間のネットワーク接続に障害が発生した場合、または災害復旧 AZ が故障した場合、事前に設定された保護間隔の後に、クラスターは非同期レプリケーション モードを有効にして、アプリケーションの可用性を確保します。
-   ネットワークが再接続するか、災害復旧AZが復旧すると、TiKVノードはクラスターに再び参加し、データを段階的にレプリケーションします。最終的に、クラスターは同期レプリケーションモードに切り替わります。

ステータススイッチの詳細は次のとおりです。

1.  **初期化**：初期化段階では、クラスターは同期レプリケーションモードになります。PDはステータス情報をTiKVに送信し、すべてのTiKVノードは同期レプリケーションモードに厳密に従って動作します。

2.  **同期から非同期への切り替え**：PDは定期的にTiKVのハートビート情報をチェックし、TiKVノードに障害が発生したか、切断されているかを判断します。障害が発生したノードの数がプライマリAZ（ `primary-replicas` ）と災害復旧AZ（ `dr-replicas` ）のレプリカ数を超えると、同期レプリケーションモードではデータレプリケーションを提供できなくなり、ステータスを切り替える必要があります。障害または切断の時間が`wait-store-timeout`で設定された時間を超えると、PDはクラスターのステータスを非同期モードに切り替えます。次に、PDはすべてのTiKVノードに非同期のステータスを送信し、TiKVのレプリケーションモードは2つのアベイラビリティゾーンのレプリケーションからネイティブのRaftマジョリティに切り替わります。

3.  **非同期から同期への切り替え**: PD は TiKV のハートビート情報を定期的にチェックし、TiKV ノードが再接続されたかどうかを判断します。障害が発生したノードの数がプライマリ AZ ( `primary-replicas` ) と災害復旧 AZ ( `dr-replicas` ) のレプリカ数より少ない場合、同期レプリケーション モードを再度有効にできます。PD は最初にクラスターのステータスを sync-recover に切り替え、そのステータス情報をすべての TiKV ノードに送信します。TiKV のすべてのリージョンは、2 つのアベイラビリティ ゾーンの同期レプリケーション モードに徐々に切り替わり、ハートビート情報を PD に報告します。PD は TiKV リージョンのステータスを記録し、リカバリの進行状況を計算します。すべての TiKV リージョンで切り替えが完了すると、PD はレプリケーション モードを同期に切り替えます。

### 災害復旧 {#disaster-recovery}

このセクションでは、1 つのリージョン展開における 2 つの AZ の災害復旧ソリューションを紹介します。

同期レプリケーションモードのクラスタに災害が発生した場合、 `RPO = 0`でデータリカバリを実行できます。

-   プライマリ AZ に障害が発生し、Voter レプリカの大部分が失われたものの、災害復旧 AZ に完全なデータが存在する場合、失われたデータは災害復旧 AZ から復旧できます。この場合、専門ツールを用いた手動介入が必要です。復旧ソリューションについては、PingCAP またはコミュニティから[サポートを受ける](/support.md)参照してください。

-   災害復旧 AZ に障害が発生し、いくつかの Voter レプリカが失われた場合、クラスターは自動的に非同期レプリケーション モードに切り替わります。

同期レプリケーションモードになっていないクラスタに災害が発生し、 `RPO = 0`でデータリカバリを実行できない場合:

-   Voterレプリカの大部分が失われた場合は、専門ツールを用いた手動介入が必要です。PingCAPまたはコミュニティから復旧ソリューションを[サポートを受ける](/support.md)することもできます。
