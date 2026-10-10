---
title: Vector Index
summary: {{{ .lake }}} のベクトルインデックスは、HNSW (Hierarchical Navigable Small World) アルゴリズムを使用して、高次元ベクトルデータに対する効率的な類似検索を可能にします。セマンティック検索、レコメンデーションシステム、AI アプリケーションなどのユースケースをサポートします。
---

# Vector Index

{{{ .lake }}} のベクトルインデックスは、HNSW (Hierarchical Navigable Small World) アルゴリズムを使用して、高次元ベクトルデータに対する効率的な類似検索を可能にします。セマンティック検索、レコメンデーションシステム、AI アプリケーションなどのユースケースをサポートします。

> **Tip:**
>
> ベクトルインデックスは、**データの書き込み時に自動的に構築されます**。Vector index を持つテーブルにデータを挿入またはロード (load) すると、手動操作なしでインデックスが自動的に生成されます。`REFRESH VECTOR INDEX` を実行する必要があるのは、すでにデータが存在するテーブルに対してインデックスを作成した場合のみです。

## ベクトルインデックスの管理 {#vector-index-management}

| コマンド                                         | 説明                                               |
|-------------------------------------------------|-----------------------------------------------------------|
| [CREATE VECTOR INDEX](/tidb-cloud-lake/sql/create-vector-index.md)   | 効率的な類似検索のための新しいベクトルインデックスを作成します |
| [REFRESH VECTOR INDEX](/tidb-cloud-lake/sql/refresh-vector-index.md) | インデックス作成前から存在していたデータのインデックスを構築します  |
| [DROP VECTOR INDEX](/tidb-cloud-lake/sql/drop-vector-index.md)       | ベクトルインデックスを削除します                                    |