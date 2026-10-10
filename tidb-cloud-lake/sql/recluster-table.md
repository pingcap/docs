---
title: RECLUSTER TABLE
summary: テーブルを再クラスタリングします。テーブルを再クラスタリングする理由とタイミングについては、Re-clustering Table を参照してください。
---

# RECLUSTER TABLE

> **Note:**
>
> v1.2.25 で導入されました。

テーブルを再クラスタリングします。テーブルを再クラスタリングする理由とタイミングについては、[Re-clustering Table](/tidb-cloud-lake/sql/cluster-key.md#cluster-key-management) を参照してください。

## 構文 {#syntax}

```sql
ALTER TABLE [ IF EXISTS ] <table_name> RECLUSTER [ FINAL ] [ WHERE condition ] [ LIMIT <segment_count> ]
```

このコマンドには、処理できるセグメント数に制限があり、デフォルト値は "max_thread * 4" です。**LIMIT** オプションを使用してこの制限を変更できます。あるいは、テーブル内のデータをさらにクラスタリングする方法として、次の 2 つの選択肢があります。

- テーブルに対してこのコマンドを複数回実行する。
- **FINAL** オプションを使用して、完全にクラスタリングされるまでテーブルの最適化を継続する。

> **Note:**
>
> テーブルの再クラスタリングには時間がかかり（**FINAL** オプションを含めるとさらに長くなります）、クレジットも消費します（{{{ .lake }}} の場合）。最適化処理の実行中は、テーブルに対して DML 操作を行わないでください。

このコマンドは、テーブルを最初からクラスタリングするわけではありません。代わりに、最新の **LIMIT** セグメントから最も無秩序な既存のストレージブロックを選択し、クラスタリングアルゴリズムを使用して再編成します。

### 例 {#examples}

```sql
-- create table
create table t(a int, b int) cluster by(a+1);

-- insert some data to t
insert into t values(1,1),(3,3);
insert into t values(2,2),(5,5);
insert into t values(4,4);

select * from clustering_information('default','t')\G
*************************** 1. row ***************************
            cluster_key: ((a + 1))
      total_block_count: 3
   constant_block_count: 1
unclustered_block_count: 0
       average_overlaps: 1.3333
          average_depth: 2.0
  block_depth_histogram: {"00002":3}

-- alter table recluster
ALTER TABLE t RECLUSTER FINAL WHERE a != 4;

select * from clustering_information('default','t')\G
*************************** 1. row ***************************
            cluster_key: ((a + 1))
      total_block_count: 2
   constant_block_count: 1
unclustered_block_count: 0
       average_overlaps: 1.0
          average_depth: 2.0
  block_depth_histogram: {"00002":2}
```