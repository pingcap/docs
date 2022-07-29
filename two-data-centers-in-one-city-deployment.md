---
title: Two Data Centers in One City Deployment
summary: Learn the deployment solution of two data centers in one city.
---

# 1つの都市展開における2つのデータセンター {#two-data-centers-in-one-city-deployment}

このドキュメントでは、アーキテクチャ、構成、この展開モードを有効にする方法、このモードでレプリカを使用する方法など、1つの都市にある2つのデータセンター（DC）の展開モードを紹介します。

オンプレミス環境では、TiDBは通常、高可用性とディザスタリカバリ機能を確保するためにマルチデータセンター展開ソリューションを採用しています。マルチデータセンター展開ソリューションには、2つの都市に3つのデータセンター、1つの都市に3つのデータセンターなど、複数の展開モードが含まれています。このドキュメントでは、1つの都市にある2つのデータセンターの展開モードを紹介します。このモードで展開されたTiDBは、低コストで高可用性とディザスタリカバリの要件を満たすこともできます。この展開ソリューションは、データレプリケーション自動同期モードまたはDR自動同期モードを採用しています。

1つの都市に2つのデータセンターがあるモードでは、2つのデータセンターの距離は50km未満です。それらは通常、同じ都市または2つの隣接する都市にあります。 2つのデータセンター間のネットワーク遅延は1.5ミリ秒未満であり、帯域幅は10Gbpsを超えています。

## デプロイメントアーキテクチャ {#deployment-architecture}

このセクションでは、2つのデータセンターIDC1とIDC2がそれぞれ東と西に配置されている都市の例を取り上げます。

クラスタデプロイメントのアーキテクチャは次のとおりです。

-   TiDBクラスタは、1つの都市の2つのDCに展開されます。東のプライマリIDC1と、西のディザスタリカバリ（DR）IDC2です。
-   クラスタには4つのレプリカがあります。IDC1に2つの投票者レプリカ、IDC2に1つの投票者レプリカと1つの学習者レプリカです。 TiKVコンポーネントの場合、各ラックには適切なラベルが付いています。
-   Raftプロトコルは、データの一貫性と高可用性を確保するために採用されており、ユーザーに対して透過的です。

![2-DC-in-1-city architecture](/media/two-dc-replication-1.png)

この展開ソリューションは、クラスタのレプリケーションステータスを制御および識別するための3つのステータスを定義します。これにより、TiKVのレプリケーションモードが制限されます。クラスタのレプリケーションモードは、3つのステータスを自動的かつ適応的に切り替えることができます。詳細については、 [ステータススイッチ](#status-switch)セクションを参照してください。

-   **sync** ：同期レプリケーションモード。このモードでは、ディザスタリカバリ（DR）データセンターの少なくとも1つのレプリカがプライマリデータセンターと同期します。 Raftアルゴリズムは、各ログがラベルに基づいてDRに複製されることを保証します。
-   **async** ：非同期レプリケーションモード。このモードでは、DRデータセンターはプライマリデータセンターと完全に同期されていません。 Raftアルゴリズムは、多数決プロトコルに従ってログを複製します。
-   **sync-recover** ：同期リカバリモード。このモードでは、DRデータセンターはプライマリデータセンターと完全に同期されていません。 Raftは徐々にラベル複製モードに切り替わり、ラベル情報をPDに報告します。

## Configuration / コンフィグレーション {#configuration}

### 例 {#example}

次の`tiup topology.yaml`のサンプルファイルは、1つの都市展開モードでの2つのデータセンターの一般的なトポロジ構成です。

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

計画されたトポロジに基づいてクラスタをデプロイするには、 [配置ルール](/configure-placement-rules.md)を使用してクラスタレプリカの場所を決定する必要があります。例として、4つのレプリカ（2つの投票者レプリカがプライマリセンターにあり、1つの投票者レプリカと1つの学習者レプリカがDRセンターにあります）の展開を例にとると、配置ルールを使用してレプリカを次のように構成できます。

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

以前の構成にロールバックする必要がある場合は、バックアップファイル`default.json`を復元するか、次のJSONファイルを手動で書き込んで、現在の構成をこのJSONファイルで上書きできます。

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

### DR自動同期モードを有効にします {#enable-the-dr-auto-sync-mode}

レプリケーションモードはPDによって制御されます。次のいずれかの方法を使用して、PD構成ファイルで複製モードを構成できます。

-   方法1：PD構成ファイルを構成してから、クラスタをデプロイします。

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

-   方法2：クラスタをデプロイした場合は、pd-ctlコマンドを使用してPDの構成を変更します。

    {{< copyable "" >}}

    ```shell
    config set replication-mode dr-auto-sync
    config set replication-mode dr-auto-sync label-key zone
    config set replication-mode dr-auto-sync primary east
    config set replication-mode dr-auto-sync dr west
    config set replication-mode dr-auto-sync primary-replicas 2
    config set replication-mode dr-auto-sync dr-replicas 1
    ```

構成アイテムの説明：

-   `replication-mode`は、有効にするレプリケーションモードです。上記の例では、 `dr-auto-sync`に設定されています。デフォルトでは、多数決プロトコルが使用されます。
-   `label-key`は、さまざまなデータセンターを区別するために使用され、配置ルールに一致する必要があります。この例では、プライマリデータセンターは「東」であり、DRデータセンターは「西」です。
-   `primary-replicas`は、プライマリデータセンター内の投票者レプリカの数です。
-   `dr-replicas`は、DRデータセンター内の投票者レプリカの数です。
-   `wait-store-timeout`は、ネットワークの分離または障害が発生したときに非同期レプリケーションモードに切り替わるまでの待機時間です。ネットワーク障害の時間が待機時間を超えると、非同期レプリケーションモードが有効になります。デフォルトの待機時間は60秒です。

クラスタの現在のレプリケーションステータスを確認するには、次のAPIを使用します。

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

クラスタのレプリケーションモードでは、次の3つのステータスを自動的かつ適応的に切り替えることができます。

-   クラスタが正常な場合、同期レプリケーションモードが有効になり、ディザスタリカバリデータセンターのデータ整合性が最大化されます。
-   2つのデータセンター間のネットワーク接続に障害が発生した場合、またはDRデータセンターが故障した場合、事前設定された保護間隔の後、クラスタは非同期レプリケーションモードを有効にして、アプリケーションの可用性を確保します。
-   ネットワークが再接続するか、DRデータセンターが回復すると、TiKVノードは再びクラスタに参加し、データを徐々に複製します。最後に、クラスタは同期レプリケーションモードに切り替わります。

ステータススイッチの詳細は次のとおりです。

1.  **初期化**：初期化段階では、クラスタは同期レプリケーションモードになっています。 PDはステータス情報をTiKVに送信し、すべてのTiKVノードは厳密に同期レプリケーションモードに従って動作します。

2.  **同期から非同期へ**の切り替え：PDは、TiKVのハートビート情報を定期的にチェックして、TiKVノードに障害が発生したか切断されたかを判断します。障害が発生したノードの数がプライマリデータセンター（ `primary-replicas` ）とDRデータセンター（ `dr-replicas` ）のレプリカの数を超えると、同期レプリケーションモードでデータレプリケーションを処理できなくなり、ステータスを切り替える必要があります。障害または切断時間が`wait-store-timeout`で設定された時間を超えると、PDはクラスタのステータスを非同期モードに切り替えます。次に、PDは非同期のステータスをすべてのTiKVノードに送信し、TiKVのレプリケーションモードは2センターレプリケーションからネイティブRaftマジョリティに切り替わります。

3.  **非同期から同期へ**の切り替え：PDは、TiKVのハートビート情報を定期的にチェックして、TiKVノードが再接続されているかどうかを判断します。障害が発生したノードの数がプライマリデータセンター（ `primary-replicas` ）およびDRデータセンター（ `dr-replicas` ）のレプリカの数より少ない場合は、同期レプリケーションモードを再度有効にできます。 PDは、最初にクラスタのステータスを同期回復に切り替え、ステータス情報をすべてのTiKVノードに送信します。 TiKVのすべてのリージョンは、徐々に2データセンターの同期レプリケーションモードに切り替わり、ハートビート情報をPDに報告します。 PDは、TiKVリージョンのステータスを記録し、リカバリの進行状況を計算します。すべてのTiKVリージョンが切り替えを完了すると、PDはレプリケーションモードを同期に切り替えます。

### 災害からの回復 {#disaster-recovery}

このセクションでは、1つの都市展開における2つのデータセンターのディザスタリカバリソリューションを紹介します。

同期レプリケーションモードでクラスタに災害が発生した場合、 `RPO = 0` ：でデータ回復を実行できます。

-   プライマリデータセンターに障害が発生し、投票者のレプリカのほとんどが失われたが、DRデータセンターに完全なデータが存在する場合、失われたデータをDRデータセンターから回復できます。現時点では、専門的なツールを使用して手動で介入する必要があります。リカバリソリューションについては、TiDBチームにお問い合わせください。

-   DRセンターに障害が発生し、いくつかの投票レプリカが失われた場合、クラスタは自動的に非同期レプリケーションモードに切り替わります。

同期レプリケーションモードではないクラスタに災害が発生し、 `RPO = 0`でデータ回復を実行できない場合：

-   投票者のレプリカのほとんどが失われた場合は、専門のツールを使用して手動で介入する必要があります。リカバリソリューションについては、TiDBチームにお問い合わせください。
