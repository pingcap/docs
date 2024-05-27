---
title: Best Practices for Read-Only Storage Nodes
summary: このドキュメントでは、オンライン サービスから高許容遅延負荷を分離するための読み取り専用storageノードの構成について説明します。手順には、TiKV ノードを読み取り専用としてマークし、配置ルールを使用して読み取り専用ノードに学習者としてデータを保存し、Follower Readを使用して読み取り専用ノードからデータを読み取ることが含まれます。
---

# 読み取り専用ストレージノードのベストプラクティス {#best-practices-for-read-only-storage-nodes}

このドキュメントでは、読み取り専用storageノードを構成する方法と、バックアップ、分析、テスト、およびその他のトラフィックをこれらのノードに送信する方法について説明します。これにより、遅延に対する許容度の高い負荷を重要なオンライン サービスから物理的に分離できます。

## 手順 {#procedures}

### 1. 一部のTiKVノードを読み取り専用として指定する {#1-specify-some-tikv-nodes-as-read-only}

一部の TiKV ノードを読み取り専用として指定するには、これらのノードに特別なラベルを付けます (ラベル キーのプレフィックスとして`$`を使用します)。配置ルールを使用してこれらのノードにデータを保存するように明示的に指定しない限り、PD はこれらのノードにデータをスケジュールしません。

`tiup cluster edit-config`コマンドを実行して読み取り専用ノードを構成できます。

    tikv_servers:
      - host: ...
        ...
        labels:
          $mode: readonly

### 2. 配置ルールを使用して、学習者として読み取り専用ノードにデータを保存する {#2-use-placement-rules-to-store-data-on-read-only-nodes-as-learners}

1.  `pd-ctl config placement-rules`コマンドを実行して、デフォルトの配置ルールをエクスポートします。

    ```shell
    pd-ctl config placement-rules rule-bundle load --out="rules.json"
    ```

    以前に配置ルールを構成していない場合、出力は次のようになります。

    ```json
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

2.  すべてのデータを学習者として読み取り専用ノードに保存します。次の例は、デフォルトの構成に基づいています。

    ```json
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
          },
          {
            "group_id": "pd",
            "id": "readonly",
            "start_key": "",
            "end_key": "",
            "role": "learner",
            "count": 1,
            "label_constraints": [
              {
                "key": "$mode",
                "op": "in",
                "values": [
                  "readonly"
                ]
              }
            ],
            "version": 1
          }
        ]
      }
    ]
    ```

3.  `pd-ctl config placement-rules`コマンドを使用して、上記の構成を PD に書き込みます。

    ```shell
    pd-ctl config placement-rules rule-bundle save --in="rules.json"
    ```

> **注記：**
>
> -   大規模なデータセットを持つクラスターで前述の操作を実行すると、クラスター全体で読み取り専用ノードにデータを完全に複製するのに時間がかかる場合があります。この期間中、読み取り専用ノードはサービスを提供できない可能性があります。
> -   バックアップの特別な実装のため、各ラベルの学習者数は 1 を超えることはできません。そうしないと、バックアップ中に重複データが生成されます。

### 3. Follower Readを使用して読み取り専用ノードからデータを読み取る {#3-use-follower-read-to-read-data-from-read-only-nodes}

#### 3.1 TiDBでFollower Readを使用する {#3-1-use-follower-read-in-tidb}

TiDB を使用するときに読み取り専用ノードからデータを読み取るには、システム変数[`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40)を`learner`に設定します。

```sql
set tidb_replica_read=learner;
```

#### 3.2 TiSparkでFollower Readを使用する {#3-2-use-follower-read-in-tispark}

TiSpark を使用するときに読み取り専用ノードからデータを読み取るには、Spark 構成ファイルで構成項目`spark.tispark.replica_read` ～ `learner`を設定します。

    spark.tispark.replica_read learner

#### 3.3 クラスターデータのバックアップ時にFollower Readを使用する {#3-3-use-follower-read-when-backing-up-cluster-data}

クラスター データをバックアップするときに読み取り専用ノードからデータを読み取るには、br コマンド ラインで`--replica-read-label`オプションを指定できます。シェルで次のコマンドを実行するときは、 `$`解析されないようにラベルを一重引用符で囲む必要があることに注意してください。

```shell
tiup br backup full ... --replica-read-label '$mode:readonly'
```
