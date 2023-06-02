---
title: Two Data Centers in One City Deployment
summary: Learn the deployment solution of two data centers in one city.
---

# 1 つの地域に展開された 2 つのデータ センター {#two-data-centers-in-one-city-deployment}

このドキュメントでは、アーキテクチャ、構成、この展開モードを有効にする方法、このモードでのレプリカの使用方法など、1 つの都市にある 2 つのデータ センター (DC) の展開モードを紹介します。

セルフホスト環境では、TiDB は通常、高可用性と災害復旧機能を確保するためにマルチデータセンター展開ソリューションを採用します。マルチデータセンター導入ソリューションには、2 つの都市に 3 つのデータセンター、1 つの都市に 3 つのデータセンターなど、複数の導入モードが含まれています。このドキュメントでは、1 つの都市に 2 つのデータセンターを配置するモードを紹介します。このモードで導入すると、TiDB は低コストで高可用性と災害復旧の要件を満たすこともできます。この展開ソリューションは、データ レプリケーション自動同期モード、つまり DR 自動同期モードを採用しています。

1 つの都市に 2 つのデータ センターがあるモードでは、2 つのデータ センターの距離は 50 キロメートル未満です。通常、これらは同じ都市または隣接する 2 つの都市にあります。 2 つのデータセンター間のネットワークレイテンシーは1.5 ミリ秒未満で、帯域幅は 10 Gbps を超えています。

## 導入アーキテクチャ {#deployment-architecture}

このセクションでは、2 つのデータ センター IDC1 と IDC2 がそれぞれ東と西に位置する都市を例に挙げます。

クラスター展開のアーキテクチャは次のとおりです。

-   TiDB クラスターは、1 つの都市の 2 つの DC (東のプライマリ IDC1 と西のディザスター リカバリー (DR) IDC2) にデプロイされています。
-   クラスターには 4 つのレプリカがあります。IDC1 に 2 つの投票者レプリカ、IDC2 に 1 つの投票者レプリカ、および 1 つのLearnerレプリカです。 TiKVコンポーネントの場合、各ラックには適切なラベルが付いています。
-   Raftプロトコルは、ユーザーにとって透過的なデータの一貫性と高可用性を確保するために採用されています。

![2-DC-in-1-city architecture](/media/two-dc-replication-1.png)

この導入ソリューションでは、クラスターのレプリケーション ステータスを制御および識別するための 3 つのステータスを定義し、TiKV のレプリケーション モードを制限します。クラスターのレプリケーション モードは、3 つのステータス間を自動的かつ適応的に切り替えることができます。詳細は[ステータススイッチ](#status-switch)章を参照してください。

-   **sync** : 同期レプリケーション モード。このモードでは、ディザスタ リカバリ (DR) データ センター内の少なくとも 1 つのレプリカがプライマリ データ センターと同期します。 Raftアルゴリズムにより、各ログがラベルに基づいて確実に DR に複製されます。
-   **async** : 非同期レプリケーション モード。このモードでは、DR データセンターはプライマリ データセンターと完全には同期しません。 Raftアルゴリズムは、多数決プロトコルに従ってログを複製します。
-   **sync-recover** : 同期リカバリモード。このモードでは、DR データセンターはプライマリ データセンターと完全には同期しません。 Raft は徐々にラベル複製モードに切り替え、ラベル情報を PD に報告します。

## コンフィグレーション {#configuration}

### 例 {#example}

次の`tiup topology.yaml`サンプル ファイルは、1 つの都市展開モードにおける 2 つのデータ センターの一般的なトポロジ構成です。

```
# # Global variables are applied to all deployments and used as the default value of
# # the deployments if a specific deployment value is missing.
global:
  user: "tidb"
  ssh_port: 22
  deploy_dir: "/data/tidb_cluster/tidb-deploy"
  data_dir: "/data/tidb_cluster/tidb-data"
server_configs:
  pd:
    replication.location-labels:  ["zone","rack","host"]
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
      server.labels: { zone: "east", rack: "east-1", host: "30" }
  - host: 10.63.10.31
    config:
      server.labels: { zone: "east", rack: "east-2", host: "31" }
  - host: 10.63.10.32
    config:
      server.labels: { zone: "west", rack: "west-1", host: "32" }
  - host: 10.63.10.33
    config:
      server.labels: { zone: "west", rack: "west-2", host: "33" }
monitoring_servers:
  - host: 10.63.10.60
grafana_servers:
  - host: 10.63.10.60
alertmanager_servers:
  - host: 10.63.10.60
```

### 配置ルール {#placement-rules}

計画されたトポロジに基づいてクラスターをデプロイするには、 [配置ルール](/configure-placement-rules.md)を使用してクラスターのレプリカの場所を決定する必要があります。例として 4 つのレプリカの展開 (2 つの投票者レプリカがプライマリ センターにあり、1 つの投票者レプリカと 1 つのLearnerレプリカが DR センターにあります) を例にとると、配置ルールを使用してレプリカを次のように構成できます。

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
        "id": "zone-east",
        "start_key": "",
        "end_key": "",
        "role": "voter",
        "count": 2,
        "label_constraints": [
          {
            "key": "zone",
            "op": "in",
            "values": [
              "east"
            ]
          }
        ],
        "location_labels": [
          "zone",
          "rack",
          "host"
        ]
      },
      {
        "group_id": "pd",
        "id": "zone-west",
        "start_key": "",
        "end_key": "",
        "role": "voter",
        "count": 1,
        "label_constraints": [
          {
            "key": "zone",
            "op": "in",
            "values": [
              "west"
            ]
          }
        ],
        "location_labels": [
          "zone",
          "rack",
          "host"
        ]
      },
      {
        "group_id": "pd",
        "id": "zone-west",
        "start_key": "",
        "end_key": "",
        "role": "learner",
        "count": 1,
        "label_constraints": [
          {
            "key": "zone",
            "op": "in",
            "values": [
              "west"
            ]
          }
        ],
        "location_labels": [
          "zone",
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

以前の構成にロールバックする必要がある場合は、バックアップ ファイル`default.json`を復元するか、次の JSON ファイルを手動で書き込み、現在の構成をこの JSON ファイルで上書きします。

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
        "count": 3
      }
    ]
  }
]
```

### DR 自動同期モードを有効にする {#enable-the-dr-auto-sync-mode}

レプリケーション モードは PD によって制御されます。次のいずれかの方法を使用して、PD 構成ファイルでレプリケーション モードを構成できます。

-   方法 1: PD 構成ファイルを構成し、クラスターをデプロイします。

    {{< copyable "" >}}

    ```toml
    [replication-mode]
    replication-mode = "dr-auto-sync"
    [replication-mode.dr-auto-sync]
    label-key = "zone"
    primary = "east"
    dr = "west"
    primary-replicas = 2
    dr-replicas = 1
    wait-store-timeout = "1m"
    wait-sync-timeout = "1m"
    ```

-   方法 2: クラスターを展開している場合は、pd-ctl コマンドを使用して PD の構成を変更します。

    {{< copyable "" >}}

    ```shell
    config set replication-mode dr-auto-sync
    config set replication-mode dr-auto-sync label-key zone
    config set replication-mode dr-auto-sync primary east
    config set replication-mode dr-auto-sync dr west
    config set replication-mode dr-auto-sync primary-replicas 2
    config set replication-mode dr-auto-sync dr-replicas 1
    ```

設定項目の説明:

-   `replication-mode`は、有効にするレプリケーション モードです。上の例では、 `dr-auto-sync`に設定されています。デフォルトでは、多数決プロトコルが使用されます。
-   `label-key`はさまざまなデータセンターを区別するために使用され、配置ルールと一致する必要があります。この例では、プライマリ データ センターは「東」、DR データ センターは「西」です。
-   `primary-replicas`は、プライマリ データ センター内の Voter レプリカの数です。
-   `dr-replicas`は、DR データセンター内の Voter レプリカの数です。
-   `wait-store-timeout` 、ネットワークの分離または障害が発生したときに非同期レプリケーション モードに切り替えるまでの待ち時間です。ネットワーク障害の時間が待機時間を超えると、非同期レプリケーション モードが有効になります。デフォルトの待機時間は 60 秒です。

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
    "label-key": "zone",
    "state": "sync"
  }
}
```

#### ステータススイッチ {#status-switch}

クラスターのレプリケーション モードは、次の 3 つのステータスを自動的かつ適応的に切り替えることができます。

-   クラスターが正常な場合、同期レプリケーション モードが有効になり、災害復旧データ センターのデータ整合性が最大化されます。
-   2 つのデータセンター間のネットワーク接続に障害が発生するか、DR データセンターが故障した場合、事前に設定された保護期間の後、クラスターは非同期レプリケーション モードを有効にしてアプリケーションの可用性を確保します。
-   ネットワークが再接続されるか、DR データセンターが回復すると、TiKV ノードは再びクラスターに参加し、データを徐々に複製します。最後に、クラスターは同期レプリケーション モードに切り替わります。

ステータススイッチの詳細は次のとおりです。

1.  **初期化**: 初期化段階では、クラスターは同期レプリケーション モードになっています。 PD はステータス情報を TiKV に送信し、すべての TiKV ノードは同期レプリケーション モードに従って動作します。

2.  **同期から非同期に切り替える**: PD は TiKV のハートビート情報を定期的にチェックして、TiKV ノードに障害が発生したか、切断されているかを判断します。障害が発生したノードの数がプライマリ データ センター ( `primary-replicas` ) および DR データ センター ( `dr-replicas` ) のレプリカ数を超える場合、同期レプリケーション モードではデータ レプリケーションを実行できなくなり、ステータスを切り替える必要があります。障害または切断時間が`wait-store-timeout`で設定された時間を超えると、PD はクラスターのステータスを非同期モードに切り替えます。次に、PD は非同期のステータスをすべての TiKV ノードに送信し、TiKV のレプリケーション モードが 2 センター レプリケーションからネイティブRaftマジョリティに切り替わります。

3.  **非同期から同期への切り替え**: PD は定期的に TiKV のハートビート情報をチェックし、TiKV ノードが再接続されているかどうかを判断します。障害が発生したノードの数がプライマリ データ センター ( `primary-replicas` ) および DR データ センター ( `dr-replicas` ) のレプリカの数より少ない場合は、同期レプリケーション モードを再度有効にすることができます。 PD はまずクラスターのステータスを同期回復に切り替え、ステータス情報をすべての TiKV ノードに送信します。 TiKV のすべてのリージョンは、段階的に 2 データセンター同期レプリケーション モードに切り替わり、ハートビート情報を PD に報告します。 PD は TiKV リージョンのステータスを記録し、復旧の進行状況を計算します。すべての TiKV リージョンの切り替えが完了すると、PD はレプリケーション モードを同期に切り替えます。

### 災害からの回復 {#disaster-recovery}

このセクションでは、1 つの都市に展開された 2 つのデータセンターの災害復旧ソリューションを紹介します。

同期レプリケーション モードでクラスターに障害が発生した場合、 `RPO = 0`でデータ復旧を実行できます。

-   プライマリ データ センターに障害が発生し、Voter レプリカの大部分が失われた場合でも、DR データ センターに完全なデータが存在する場合、失われたデータは DR データ センターから復元できます。現時点では、専門ツールを使用した手動介入が必要です。回復ソリューションについては、TiDB チームにお問い合わせください。

-   DR センターに障害が発生し、いくつかの Voter レプリカが失われた場合、クラスターは自動的に非同期レプリケーション モードに切り替わります。

同期レプリケーション モードではないクラスターに障害が発生し、 `RPO = 0`でデータ復旧を実行できない場合:

-   Voter レプリカの大部分が失われた場合は、専門ツールを使用して手動で介入する必要があります。回復ソリューションについては、TiDB チームにお問い合わせください。
