---
title: SET CLUSTER KEY
summary: テーブル作成時にクラスターキーを設定します。
---

# SET CLUSTER KEY

テーブル作成時にクラスターキーを設定します。

クラスターキーは、データを物理的にまとめて配置することで、クエリ性能を向上させることを目的としています。たとえば、テーブルのクラスターキーとしてあるカラムを設定すると、テーブルデータは設定したカラムに基づいて物理的にソートされます。クエリの多くがそのカラムでフィルタされる場合、クエリ性能を最大化できます。

> **Note:**
>
> String カラムの場合、クラスター統計では先頭 8 バイトのみが使用されます。十分なカーディナリティを確保するために、substring を使用できます。

関連情報:

* [ALTER CLUSTER KEY](/tidb-cloud-lake/sql/alter-cluster-key.md)
* [DROP CLUSTER KEY](/tidb-cloud-lake/sql/drop-cluster-key.md)

## 構文 {#syntax}

```sql
CREATE TABLE <name> ... CLUSTER BY ( <expr1> [ , <expr2> ... ] )
```

## 例 {#examples}

このコマンドは、カラムでクラスタリングされたテーブルを作成します。

```sql
CREATE TABLE t1(a int, b int) CLUSTER BY(b,a);

CREATE TABLE t2(a int, b string) CLUSTER BY(SUBSTRING(b, 5, 6));
```