---
title: Store Limit
summary: ストア制限の機能について学びます。
---

# 店舗制限 {#store-limit}

ストア制限は、TiDB 3.0 で導入された PD の機能です。さまざまなシナリオでパフォーマンスを向上させるために、スケジュール速度をより細かく制御するように設計されています。

## 実施原則 {#implementation-principles}

PD はオペレータ単位でスケジューリングを実行します。オペレータには複数のスケジューリング操作が含まれる場合があります。例:

    "replace-down-replica {mv peer: store [2] to [3]} (kind:region,replica, region:10(4,5), createAt:2020-05-18 06:40:25.775636418 +0000 UTC m=+2168762.679540369, startAt:2020-05-18 06:40:25.775684648 +0000 UTC m=+2168762.679588599, currentStep:0, steps:[add learner peer 20 on store 3, promote learner peer 20 on store 3 to voter, remove peer on store 2])"

上記の例では、 `replace-down-replica`演算子には次の特定の演算が含まれています。

1.  ID `20` ～ `store 3`の学習者ピアを追加します。
2.  ID `20` on `store 3`の学習者ピアを投票者に昇格します。
3.  `store 2`のピアを削除します。

ストア制限は、ストア ID からメモリ内のトークン バケットへのマッピングを維持することで、ストア レベルの速度制限を実現します。ここでのさまざまな操作は、さまざまなトークン バケットに対応します。現在、ストア制限は、学習者/ピアの追加とピアの削除という 2 つの操作の速度制限のみをサポートしています。つまり、各ストアには 2 種類のトークン バケットがあります。

オペレータが生成されるたびに、そのオペレータは、その操作に十分なトークンがトークン バケット内に存在するかどうかを確認します。存在する場合、オペレータはスケジュール キューに追加され、対応するトークンがトークン バケットから取得されます。そうでない場合、オペレータは放棄されます。トークン バケットは固定レートでトークンを補充するため、速度制限が達成されます。

Store Limit は、PD の他の制限関連パラメータ ( `region-schedule-limit`や`leader-schedule-limit`など) とは異なり、主にオペレータの消費速度を制限し、他のパラメータはオペレータの生成速度を制限します。Store Limit 機能を導入する前は、スケジューリングの速度制限は主にグローバル スコープでした。そのため、グローバル速度が制限されていても、スケジューリング操作が一部のストアに集中し、クラスターのパフォーマンスに影響を与える可能性があります。より細かいレベルで速度を制限することで、Store Limit はスケジューリング動作をより適切に制御できます。

## 使用法 {#usage}

Store Limit のパラメータは`pd-ctl`使用して設定できます。

### 現在のストアの設定をビュー {#view-setting-of-the-current-store}

現在のストアの制限設定を表示するには、次のコマンドを実行します。

```bash
store limit                         // Shows the speed limit of adding and deleting peers in all stores.
store limit add-peer                // Shows the speed limit of adding peers in all stores.
store limit remove-peer             // Shows the speed limit of deleting peers in all stores. 
```

### 全店舗の制限を設定する {#set-limit-for-all-stores}

すべてのストアの速度制限を設定するには、次のコマンドを実行します。

```bash
store limit all 5                   // All stores can at most add and delete 5 peers per minute.
store limit all 5 add-peer          // All stores can at most add 5 peers per minute.
store limit all 5 remove-peer       // All stores can at most delete 5 peers per minute.
```

### 単一店舗の制限を設定する {#set-limit-for-a-single-store}

単一のストアに対して速度制限を設定するには、次のコマンドを実行します。

```bash
store limit 1 5                     // store 1 can at most add and delete 5 peers per minute.
store limit 1 5 add-peer            // store 1 can at most add 5 peers per minute.
store limit 1 5 remove-peer         // store 1 can at most delete 5 peers per minute.
```

### ストア制限の原則 v2 {#principles-of-store-limit-v2}

> **警告：**
>
> Store limit v2 は実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告できます。

[`store-limit-version`](/pd-configuration-file.md#store-limit-version-new-in-v710) `v2`に設定すると、ストア制限 v2 が有効になります。v2 モードでは、演算子の制限は TiKV スナップショットの機能に基づいて動的に調整されます。TiKV の保留中のタスクが少なくなると、PD はスケジュール タスクを増やします。それ以外の場合は、PD はノードのスケジュール タスクを減らします。したがって、スケジュール プロセスを高速化するために手動で`store limit`を設定する必要はありません。

v2モードでは、移行中の主なボトルネックはTiKVの実行速度になります。現在のスケジュール速度が上限に達しているかどうかは、 **TiKVの詳細**&gt;**スナップショット**&gt;**スナップショット速度**パネルで確認できます。ノードのスケジュール速度を増減するには、TiKVスナップショット制限（ [`snap-io-max-bytes-per-sec`](/tikv-configuration-file.md#snap-io-max-bytes-per-sec) ）を調整します。
