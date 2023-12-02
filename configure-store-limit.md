---
title: Store Limit
summary: Learn the feature of Store Limit.
---

# 店舗制限 {#store-limit}

ストア制限は、TiDB 3.0 で導入された PD の機能です。さまざまなシナリオでパフォーマンスを向上させるために、スケジューリング速度をより細かく制御するように設計されています。

## 実装原則 {#implementation-principles}

PDはオペレータ単位でスケジューリングを行います。オペレーターには複数のスケジュール操作が含まれる場合があります。例えば：

    "replace-down-replica {mv peer: store [2] to [3]} (kind:region,replica, region:10(4,5), createAt:2020-05-18 06:40:25.775636418 +0000 UTC m=+2168762.679540369, startAt:2020-05-18 06:40:25.775684648 +0000 UTC m=+2168762.679588599, currentStep:0, steps:[add learner peer 20 on store 3, promote learner peer 20 on store 3 to voter, remove peer on store 2])"

上記の例では、 `replace-down-replica`演算子には次の特定の演算が含まれています。

1.  ID `20` ～ `store 3`の学習者ピアを追加します。
2.  ID `20`から`store 3`の学習者ピアを投票者に昇格します。
3.  `store 2`のピアを削除します。

Store Limit は、ストア ID からトークン バケットへのマッピングをメモリ内に維持することで、ストア レベルの速度制限を実現します。ここでのさまざまな操作は、さまざまなトークン バケットに対応します。現在、ストア制限は、学習者/ピアの追加とピアの削除という 2 つの操作の速度制限のみをサポートしています。つまり、各ストアには 2 種類のトークン バケットがあります。

オペレーターが生成されるたびに、その操作に必要なトークンがトークン バケットに存在するかどうかがチェックされます。 「はい」の場合、オペレーターはスケジューリング キューに追加され、対応するトークンがトークン バケットから取得されます。それ以外の場合、オペレーターは放棄されます。トークン バケットは固定レートでトークンを補充するため、速度制限が達成されます。

Store Limit は、主にオペレーターの消費速度を制限するのに対し、他のパラメーターはオペレーターの生成速度を制限するという点で、PD の他の制限関連パラメーター ( `region-schedule-limit`や`leader-schedule-limit`など) とは異なります。ストア制限機能を導入する前は、スケジュールの速度制限はほとんどがグローバルな範囲にありました。したがって、グローバル速度が制限されている場合でも、スケジューリング操作が一部のストアに集中し、クラスターのパフォーマンスに影響を与える可能性があります。より細かいレベルで速度を制限することにより、ストア制限はスケジューリング動作をより適切に制御できます。

## 使用法 {#usage}

Store Limit のパラメータは`pd-ctl`を使用して設定できます。

### 現在のストアの設定をビュー {#view-setting-of-the-current-store}

現在のストアの制限設定を表示するには、次のコマンドを実行します。

```bash
store limit                         // Shows the speed limit of adding and deleting peers in all stores.
store limit add-peer                // Shows the speed limit of adding peers in all stores.
store limit remove-peer             // Shows the speed limit of deleting peers in all stores. 
```

### すべてのストアに制限を設定する {#set-limit-for-all-stores}

すべてのストアの速度制限を設定するには、次のコマンドを実行します。

```bash
store limit all 5                   // All stores can at most add and delete 5 peers per minute.
store limit all 5 add-peer          // All stores can at most add 5 peers per minute.
store limit all 5 remove-peer       // All stores can at most delete 5 peers per minute.
```

### 単一ストアの制限を設定する {#set-limit-for-a-single-store}

単一ストアの速度制限を設定するには、次のコマンドを実行します。

```bash
store limit 1 5                     // store 1 can at most add and delete 5 peers per minute.
store limit 1 5 add-peer            // store 1 can at most add 5 peers per minute.
store limit 1 5 remove-peer         // store 1 can at most delete 5 peers per minute.
```

### ストア制限 v2 の原則 {#principles-of-store-limit-v2}

[`store-limit-version`](/pd-configuration-file.md#store-limit-version-new-in-v710)を`v2`に設定すると、ストア制限 v2 が有効になります。 v2 モードでは、オペレーターの制限は TiKV スナップショットの機能に基づいて動的に調整されます。 TiKV の保留中のタスクが少なくなると、PD はスケジューリング タスクを増やします。それ以外の場合、PD はノードのスケジューリング タスクを削減します。したがって、スケジュール プロセスを高速化するために手動で`store limit`を設定する必要はありません。

v2 モードでは、TiKV の実行速度が移行中の主なボトルネックになります。現在のスケジュール速度が上限に達しているかどうかは、 **[TiKV 詳細]** &gt; **[スナップショット]** &gt; **[スナップショット速度]**パネルで確認できます。ノードのスケジューリング速度を増減するには、TiKV スナップショット制限を調整できます ( [`snap-io-max-bytes-per-sec`](/tikv-configuration-file.md#snap-io-max-bytes-per-sec) )。
