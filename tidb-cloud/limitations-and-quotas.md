---
title: TiDB Dedicated Limitations and Quotas
summary: TiDB Cloudの制限と割り当てについて説明します。
---

# TiDB 専用制限とクォータ {#tidb-dedicated-limitations-and-quotas}

TiDB Cloud、 [TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターで作成できる各種類のコンポーネントの数と、TiDB の一般的な使用上の制限が制限されています。さらに、実際に必要な量を超えるリソースが作成されないように、ユーザーが作成するリソースの量を制限する組織レベルのクォータもいくつかあります。次の表は、制限とクォータの概要を示しています。

> **注記：**
>
> これらの制限または割り当てが組織にとって問題となる場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。

## クラスタの制限 {#cluster-limits}

| 成分                     | 制限 |
| :--------------------- | :- |
| データレプリカの数              | 3  |
| クロスゾーン展開のアベイラビリティゾーンの数 | 3  |

> **注記：**
>
> TiDB の一般的な使用上の制限について詳しく知りたい場合は、 [TiDB の制限](https://docs.pingcap.com/tidb/stable/tidb-limitations)を参照してください。

## クラスタクォータ {#cluster-quotas}

| 成分                            | クォータ（デフォルト） |
| :---------------------------- | :---------- |
| 組織内のすべてのクラスタの合計 TiDB ノードの最大数  | 10          |
| 組織内のすべてのクラスタの合計 TiKV ノードの最大数  | 15          |
| 組織内のすべてのクラスタの合計TiFlashノードの最大数 | 5           |
