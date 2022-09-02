---
title: Store Limit
summary: Learn the feature of Store Limit.
---

# 店舗制限 {#store-limit}

Store Limit は、TiDB 3.0 で導入された PD の機能です。さまざまなシナリオでパフォーマンスを向上させるために、スケジューリング速度をより細かく制御するように設計されています。

## 実施原則 {#implementation-principles}

PD は、オペレータ単位でスケジューリングを行います。オペレーターには、複数のスケジューリング操作が含まれる場合があります。例えば：

```
"replace-down-replica {mv peer: store [2] to [3]} (kind:region,replica, region:10(4,5), createAt:2020-05-18 06:40:25.775636418 +0000 UTC m=+2168762.679540369, startAt:2020-05-18 06:40:25.775684648 +0000 UTC m=+2168762.679588599, currentStep:0, steps:[add learner peer 20 on store 3, promote learner peer 20 on store 3 to voter, remove peer on store 2])"
```

上記の例では、 `replace-down-replica`演算子に次の特定の操作が含まれています。

1.  ID `20` ～ `store 3`の学習者ピアを追加します。
2.  ID `20` on `store 3`の学習者ピアを有権者に昇格させます。
3.  `store 2`のピアを削除します。

Store Limit は、ストア ID からメモリ内のトークン バケットへのマッピングを維持することで、ストア レベルの速度制限を実現します。ここでのさまざまな操作は、さまざまなトークン バケットに対応しています。現在、Store Limit は、学習者/ピアの追加とピアの削除の 2 つの操作の速度制限のみをサポートしています。つまり、各ストアには 2 種類のトークン バケットがあります。

オペレーターが生成されるたびに、その操作に十分なトークンがトークン バケットに存在するかどうかがチェックされます。はいの場合、オペレータがスケジューリング キューに追加され、対応するトークンがトークン バケットから取得されます。それ以外の場合、オペレーターは放棄されます。トークン バケットは固定レートでトークンを補充するため、速度制限が達成されます。

Store Limit は、主にオペレーターの消費速度を制限し、他のパラメーターはオペレーターの生成速度を制限するという点で、PD の他の制限関連パラメーター ( `region-schedule-limit`や`leader-schedule-limit`など) とは異なります。ストア制限機能を導入する前は、スケジューリングの速度制限はほとんどがグローバル スコープでした。したがって、グローバル速度が制限されている場合でも、スケジューリング操作が一部のストアに集中し、クラスターのパフォーマンスに影響を与える可能性があります。より細かいレベルで速度を制限することにより、Store Limit はスケジューリング動作をより適切に制御できます。

## 使用法 {#usage}

Store Limit のパラメーターは、 `pd-ctl`を使用して構成できます。

### 現在の店舗のビュー設定 {#view-setting-of-the-current-store}

現在のストアの制限設定を表示するには、次のコマンドを実行します。

{{< copyable "" >}}

```bash
store limit                         // Shows the speed limit of adding and deleting peers in all stores.
store limit add-peer                // Shows the speed limit of adding peers in all stores.
store limit remove-peer             // Shows the speed limit of deleting peers in all stores. 
```

### 全店舗に制限を設ける {#set-limit-for-all-stores}

すべての店舗の速度制限を設定するには、次のコマンドを実行します。

{{< copyable "" >}}

```bash
store limit all 5                   // All stores can at most add and delete 5 peers per minute.
store limit all 5 add-peer          // All stores can at most add 5 peers per minute.
store limit all 5 remove-peer       // All stores can at most delete 5 peers per minute.
```

### 1 店舗の制限を設定する {#set-limit-for-a-single-store}

1 つのストアの速度制限を設定するには、次のコマンドを実行します。

{{< copyable "" >}}

```bash
store limit 1 5                     // store 1 can at most add and delete 5 peers per minute.
store limit 1 5 add-peer            // store 1 can at most add 5 peers per minute.
store limit 1 5 remove-peer         // store 1 can at most delete 5 peers per minute.
```
