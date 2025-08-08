---
title: Store Limit
summary: ストア制限の機能について学びます。
---

# 店舗制限 {#store-limit}

ストア制限はPDの機能です。様々なシナリオでパフォーマンスを向上させるために、スケジューリング速度をより細かく制御できるように設計されています。

## 実施原則 {#implementation-principles}

PDはオペレータ単位でスケジューリングを実行します。オペレータには複数のスケジューリング操作が含まれる場合があります。例：

    "replace-down-replica {mv peer: store [2] to [3]} (kind:region,replica, region:10(4,5), createAt:2020-05-18 06:40:25.775636418 +0000 UTC m=+2168762.679540369, startAt:2020-05-18 06:40:25.775684648 +0000 UTC m=+2168762.679588599, currentStep:0, steps:[add learner peer 20 on store 3, promote learner peer 20 on store 3 to voter, remove peer on store 2])"

上記の例では、 `replace-down-replica`演算子には次の特定の演算が含まれています。

1.  ID `20` ～ `store 3`の学習者ピアを追加します。
2.  ID `20` on `store 3`の学習者ピアを投票者に昇格します。
3.  `store 2`のピアを削除します。

ストア制限は、ストアIDとトークンバケットのマッピングをメモリ内に保持することで、ストアレベルの速度制限を実現します。ここでの異なる操作は、それぞれ異なるトークンバケットに対応しています。現在、ストア制限は、学習者/ピアの追加とピアの削除という2つの操作の速度制限のみをサポートしています。つまり、各ストアには2種類のトークンバケットがあります。

オペレータが生成されるたびに、そのオペレータはトークンバケットにその操作に必要なトークンが十分にあるかどうかを確認します。十分なトークンがある場合、オペレータはスケジューリングキューに追加され、対応するトークンがトークンバケットから取得されます。十分なトークンがない場合、オペレータは破棄されます。トークンバケットは一定の速度でトークンを補充するため、速度制限はこのように達成されます。

ストア制限は、PDの他の制限関連パラメータ（ `region-schedule-limit`や`leader-schedule-limit`など）とは異なり、主にオペレータの消費速度を制限するのに対し、他のパラメータはオペレータの生成速度を制限します。ストア制限機能を導入する前は、スケジューリングの速度制限は主にグローバルスコープでした。そのため、グローバル速度が制限されたとしても、スケジューリング操作が一部のストアに集中し、クラスターのパフォーマンスに影響を与える可能性があります。より細かいレベルで速度を制限することで、ストア制限はスケジューリング動作をより適切に制御できます。

ストア制限は、1分あたりの最大操作数を定義します。ストア制限が1分あたり5操作の場合、クラスターに新しいノードを追加すると、1分あたり5リージョン（ `add-peer`操作）が処理されます。15のリージョンで`add-peer`操作が必要な場合、操作には3分（15 / 5 = 3）かかり、各リージョンが96MiBであると仮定すると、最大8MiB/秒（(5 × 96) / 60 = 8）の帯域幅を消費します。

## 使用法 {#usage}

Store Limit のパラメータは[`PD Control`](/pd-control.md)使用して設定できます。

### 現在のストアのビュー設定 {#view-setting-of-the-current-store}

現在のストアの制限設定を表示するには、次のコマンドを実行します。

```bash
tiup ctl:v<CLUSTER_VERSION> pd store limit                         // Shows the speed limit of adding and deleting peers in all stores.
tiup ctl:v<CLUSTER_VERSION> pd store limit add-peer                // Shows the speed limit of adding peers in all stores.
tiup ctl:v<CLUSTER_VERSION> pd store limit remove-peer             // Shows the speed limit of deleting peers in all stores.
```

### 全店舗の制限を設定する {#set-limit-for-all-stores}

すべてのストアの速度制限を設定するには、次のコマンドを実行します。

```bash
tiup ctl:v<CLUSTER_VERSION> pd store limit all 5                   // All stores can at most add and delete 5 peers per minute.
tiup ctl:v<CLUSTER_VERSION> pd store limit all 5 add-peer          // All stores can at most add 5 peers per minute.
tiup ctl:v<CLUSTER_VERSION> pd store limit all 5 remove-peer       // All stores can at most delete 5 peers per minute.
```

### 単一店舗の制限を設定する {#set-limit-for-a-single-store}

単一のストアに対して速度制限を設定するには、次のコマンドを実行します。

```bash
tiup ctl:v<CLUSTER_VERSION> pd store limit 1 5                     // store 1 can at most add and delete 5 peers per minute.
tiup ctl:v<CLUSTER_VERSION> pd store limit 1 5 add-peer            // store 1 can at most add 5 peers per minute.
tiup ctl:v<CLUSTER_VERSION> pd store limit 1 5 remove-peer         // store 1 can at most delete 5 peers per minute.
```

### 店舗制限の原則 v2 {#principles-of-store-limit-v2}

[`store-limit-version`](/pd-configuration-file.md#store-limit-version-new-in-v710) `v2`に設定すると、ストア制限 v2 が有効になります。v2 モードでは、オペレーターの制限は TiKV スナップショットの性能に基づいて動的に調整されます。TiKV の保留中のタスクが少なくなると、PD はスケジュールするタスクを増やします。そうでない場合は、PD はノードのスケジュールするタスクを減らします。したがって、スケジュール処理を高速化するために手動で`store limit`設定する必要はありません。

v2モードでは、TiKVの実行速度が移行時の主なボトルネックとなります。現在のスケジュール速度が上限に達しているかどうかは、 **「TiKV詳細」** &gt; **「スナップショット」** &gt; **「スナップショット速度」**パネルで確認できます。ノードのスケジュール速度を増減するには、TiKVスナップショット制限（ [`snap-io-max-bytes-per-sec`](/tikv-configuration-file.md#snap-io-max-bytes-per-sec) ）を調整します。
