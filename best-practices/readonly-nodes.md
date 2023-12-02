---
title: Best Practices for Read-Only Storage Nodes
summary: Learn how to configure read-only storage nodes to physically isolate important online services.
---

# 読み取り専用ストレージ ノードのベスト プラクティス {#best-practices-for-read-only-storage-nodes}

このドキュメントでは、読み取り専用storageノードを構成する方法と、バックアップ、分析、テスト、およびその他のトラフィックをこれらのノードに送信する方法を紹介します。このようにして、遅延に対する耐性が高い負荷を重要なオンライン サービスから物理的に分離できます。

## 手順 {#procedures}

### 1. 一部の TiKV ノードを読み取り専用として指定します {#1-specify-some-tikv-nodes-as-read-only}

一部の TiKV ノードを読み取り専用として指定するには、これらのノードを特別なラベルでマークします (ラベル キーのプレフィックスとして`$`を使用します)。配置ルールを使用してデータを保存するようにこれらのノードを明示的に指定しない限り、PD はこれらのノードにデータをスケジュールしません。

`tiup cluster edit-config`コマンドを実行して、読み取り専用ノードを構成できます。

    tikv_servers:
      - host: ...
        ...
        labels:
          $mode: readonly

### 2. 配置ルールを使用して、データを学習者として読み取り専用ノードに保存します {#2-use-placement-rules-to-store-data-on-read-only-nodes-as-learners}

1.  `pd-ctl config placement-rules`コマンドを実行して、デフォルトの配置ルールをエクスポートします。

    ```shell
    pd-ctl config placement-rules rule-bundle load --out="rules.json"
    ```

    これまでに配置ルールを構成したことがない場合、出力は次のようになります。

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

3.  `pd-ctl config placement-rules`コマンドを使用して、前述の設定を PD に書き込みます。

    ```shell
    pd-ctl config placement-rules rule-bundle save --in="rules.json"
    ```

> **注記：**
>
> -   大規模なデータセットを含むクラスターで前述の操作を実行する場合、クラスター全体でデータを読み取り専用ノードに完全にレプリケートするのに時間がかかる場合があります。この期間中、読み取り専用ノードはサービスを提供できない可能性があります。
> -   バックアップの特殊な実装のため、各ラベルの学習者番号は 1 を超えることはできません。1 を超えると、バックアップ中に重複データが生成されます。

### 3. Follower Read を使用して読み取り専用ノードからデータを読み取ります {#3-use-follower-read-to-read-data-from-read-only-nodes}

#### 3.1 TiDB でのFollower Readの使用 {#3-1-use-follower-read-in-tidb}

TiDB の使用時に読み取り専用ノードからデータを読み取るには、システム変数[`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40)から`learner`を設定できます。

```sql
set tidb_replica_read=learner;
```

#### 3.2 TiSpark でFollower Readを使用する {#3-2-use-follower-read-in-tispark}

TiSpark の使用時に読み取り専用ノードからデータを読み取るには、Spark 構成ファイルで構成項目`spark.tispark.replica_read`から`learner`を設定できます。

    spark.tispark.replica_read learner

#### 3.3 クラスターデータのバックアップ時にFollower Readを使用する {#3-3-use-follower-read-when-backing-up-cluster-data}

クラスター データのバックアップ時に読み取り専用ノードからデータを読み取るには、br コマンド ラインで`--replica-read-label`オプションを指定できます。シェルで次のコマンドを実行するときは、 `$`が解析されないように、一重引用符を使用してラベルを囲む必要があることに注意してください。

```shell
br backup full ... --replica-read-label '$mode:readonly'
```
