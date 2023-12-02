---
title: TiDB Dedicated Limitations and Quotas
summary: Learn the limitations and quotas in TiDB Cloud.
---

# TiDB 専用の制限と割り当て {#tidb-dedicated-limitations-and-quotas}

TiDB Cloud、 [TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスター内に作成できる各種類のコンポーネントの数と、TiDB の一般的な使用制限が制限されています。さらに、実際に必要以上のリソースが作成されないように、ユーザーが作成するリソースの量を制限する組織レベルのクォータがいくつかあります。これらの表は、制限とクォータの概要を示しています。

> **注記：**
>
> これらの制限またはクォータのいずれかが組織に問題を引き起こす場合は、 [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

## クラスタの制限 {#cluster-limits}

| 成分                      | 限界 |
| :---------------------- | :- |
| データレプリカの数               | 3  |
| クロスゾーン展開のアベイラビリティーゾーンの数 | 3  |

> **注記：**
>
> TiDB の一般的な使用上の制限について詳しく知りたい場合は、 [TiDB の制限事項](https://docs.pingcap.com/tidb/stable/tidb-limitations)を参照してください。

## クラスタのクォータ {#cluster-quotas}

| 成分                             | クォータ (デフォルト) |
| :----------------------------- | :----------- |
| 組織内のすべてのクラスターの合計 TiDB ノードの最大数  | 10           |
| 組織内のすべてのクラスターの合計 TiKV ノードの最大数  | 15           |
| 組織内のすべてのクラスターの合計TiFlashノードの最大数 | 5            |
