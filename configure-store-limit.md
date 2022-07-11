---
title: Store Limit
summary: Learn the feature of Store Limit.
---

# ストア制限 {#store-limit}

ストア制限はPDの機能であり、TiDB3.0で導入されました。さまざまなシナリオでパフォーマンスを向上させるために、スケジューリング速度をより細かく制御するように設計されています。

## 実装の原則 {#implementation-principles}

PDはオペレーターの単位でスケジューリングを実行します。オペレーターには、複数のスケジューリング操作が含まれる場合があります。例えば：

```
"replace-down-replica {mv peer: store [2] to [3]} (kind:region,replica, region:10(4,5), createAt:2020-05-18 06:40:25.775636418 +0000 UTC m=+2168762.679540369, startAt:2020-05-18 06:40:25.775684648 +0000 UTC m=+2168762.679588599, currentStep:0, steps:[add learner peer 20 on store 3, promote learner peer 20 on store 3 to voter, remove peer on store 2])"
```

上記の例では、 `replace-down-replica`演算子には次の特定の操作が含まれています。

1.  IDが`20`から`store 3`の学習者ピアを追加します。
2.  ID `20`の学習者ピアを有権者に昇格させ`store 3` 。
3.  `store 2`のピアを削除します。

ストア制限は、ストアIDからメモリ内のトークンバケットへのマッピングを維持することにより、ストアレベルの速度制限を実現します。ここでのさまざまな操作は、さまざまなトークンバケットに対応しています。現在、Store Limitは、学習者/ピアの追加とピアの削除という2つの操作の速度の制限のみをサポートしています。つまり、各ストアには2種類のトークンバケットがあります。

演算子が生成されるたびに、その操作のために十分なトークンがトークンバケットに存在するかどうかをチェックします。はいの場合、オペレーターはスケジューリングキューに追加され、対応するトークンがトークンバケットから取得されます。それ以外の場合、オペレーターは放棄されます。トークンバケットは固定レートでトークンを補充するため、速度制限が達成されます。

Store Limitは、PDの他の制限関連パラメーター（ `region-schedule-limit`や`leader-schedule-limit`など）とは異なり、主にオペレーターの消費速度を制限しますが、他のパラメーターはオペレーターの生成速度を制限します。ストア制限機能を導入する前は、スケジューリングの速度制限はほとんどグローバルスコープにあります。したがって、グローバル速度が制限されている場合でも、スケジューリング操作が一部のストアに集中し、クラスタのパフォーマンスに影響を与える可能性があります。より細かいレベルで速度を制限することにより、StoreLimitはスケジューリング動作をより適切に制御できます。

## 使用法 {#usage}

Store Limitのパラメーターは、 `pd-ctl`を使用して構成できます。

### 現在の店舗の設定をビュー {#view-setting-of-the-current-store}

現在のストアの制限設定を表示するには、次のコマンドを実行します。

{{< copyable "" >}}

```bash
store limit                         // Shows the speed limit of adding and deleting peers in all stores.
store limit add-peer                // Shows the speed limit of adding peers in all stores.
store limit remove-peer             // Shows the speed limit of deleting peers in all stores.
```

### すべての店舗に制限を設定する {#set-limit-for-all-stores}

すべてのストアの制限速度を設定するには、次のコマンドを実行します。

{{< copyable "" >}}

```bash
store limit all 5                   // All stores can at most add and delete 5 peers per minute.
store limit all 5 add-peer          // All stores can at most add 5 peers per minute.
store limit all 5 remove-peer       // All stores can at most delete 5 peers per minute.
```

### 1店舗の制限を設定する {#set-limit-for-a-single-store}

単一ストアの制限速度を設定するには、次のコマンドを実行します。

{{< copyable "" >}}

```bash
store limit 1 5                     // store 1 can at most add and delete 5 peers per minute.
store limit 1 5 add-peer            // store 1 can at most add 5 peers per minute.
store limit 1 5 remove-peer         // store 1 can at most delete 5 peers per minute.
```
