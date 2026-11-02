---
title: TiDB Cloud Dedicated Limitations and Quotas
summary: TiDB Cloudの制限とクォータについて説明します。
---

# TiDB Cloud Dedicated制限とクォータ {#tidb-cloud-dedicated-limitations-and-quotas}

TiDB Cloudでは、 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスター内で作成できる各コンポーネントの数と、TiDBの一般的な使用が制限されています。さらに、組織レベルのクォータによってユーザーが作成できるリソースの量を制限し、実際に必要な量を超えるリソースの作成を防げます。以下の表は、制限とクォータの概要を示しています。

> **Note:**
>
> これらの制限またはクォータが組織にとって問題となる場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

## クラスターの制限 {#cluster-limits}

| コンポーネント                                                          | 制限 |
| :---------------------------------------------------------- | :- |
| [データリージョン](/tidb-cloud/tidb-cloud-glossary.md#region)あたりのコピー数 | 3  |
| クロスゾーンデプロイのアベイラビリティゾーンの数                                      | 3  |

> **Note:**
>
> TiDB の一般的な使用上の制限について詳しくは、 [TiDB の制限](https://docs.pingcap.com/tidb/stable/tidb-limitations)を参照してください。

## クラスタークォータ {#cluster-quotas}

| コンポーネント                            | クォータ（デフォルト） |
| :---------------------------- | :---------- |
| 組織内のすべてのクラスターの合計 TiDB ノードの最大数  | 10          |
| 組織内のすべてのクラスターの合計 TiKV ノードの最大数  | 15          |
| 組織内のすべてのクラスターのTiFlashノードの最大数   | 5           |
| 組織内のすべてのクラスターの TiProxy ノードの最大数 | 10          |

> **Note:**
>
> これらの制限またはクォータが組織にとって問題となる場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。
