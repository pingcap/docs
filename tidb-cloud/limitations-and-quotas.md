---
title: Limitations and Quotas in TiDB Cloud
summary: Learn the limitations and quotas in TiDB Cloud.
---

# TiDB Cloudの制限と割り当て {#limitations-and-quotas-in-tidb-cloud}

TiDB Cloudは、作成できる各種類のコンポーネントの数と、TiDBの一般的な使用制限を制限します。さらに、実際に必要な数よりも多くのリソースが作成されないように、ユーザーが作成するリソースの量を制限するための組織レベルの割り当てがいくつかあります。これらの表は、制限と割り当ての概要を示しています。

> **ノート：**
>
> これらの制限または割り当てのいずれかが組織に問題をもたらす場合は、 [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)に連絡してください。

## クラスターの制限 {#cluster-limits}

| 成分                      | 制限 |
| :---------------------- | :- |
| データレプリカの数               | 3  |
| クロスゾーン展開のアベイラビリティーゾーンの数 | 3  |

> **ノート：**
>
> TiDBの一般的な使用制限について詳しく知りたい場合は、 [TiDBの制限](https://docs.pingcap.com/tidb/stable/tidb-limitations)を参照してください。

## クラスタークォータ {#cluster-quotas}

| 成分                             | クォータ（デフォルト） |
| :----------------------------- | :---------- |
| 組織内のすべてのクラスターの合計TiDBノードの最大数    | 20          |
| 組織内のすべてのクラスターの合計TiKVノードの最大数    | 30          |
| 組織内のすべてのクラスターの合計TiFlashノードの最大数 | 30          |
