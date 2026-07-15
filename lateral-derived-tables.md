---
title: LATERAL Derived Tables
summary: TiDB における LATERAL 派生テーブルの構文と現在の制限事項について説明します。
---

# LATERAL Derived Tables

**lateral derived table** とは、`FROM` 句内のサブクエリであり、同じ `FROM` 句内でそれより前に現れるテーブルのカラムを参照できるものです。標準的な派生テーブルでは、そのサブクエリは同じ `FROM` 句内の他のテーブルのカラムを参照できませんが、lateral derived table はより柔軟です。

v8.5.7 以降、TiDB は派生テーブルに対する `LATERAL` 構文のパースをサポートしています。これは MySQL 8.0 の構文（[WL#8652](https://dev.mysql.com/worklog/task/?id=8652)）と互換性があります。

> **Note:**
>
> 現在、TiDB は `LATERAL` 派生テーブル構文のパースのみをサポートしており、この構文を使用するクエリの実行はサポートしていません。このようなクエリを実行しようとすると、TiDB はエラーを返します。この機能の完全な実行サポートの進捗は、issue [#40328](https://github.com/pingcap/tidb/issues/40328) で確認できます。

## 構文 {#syntax}

```sql
SELECT ... FROM table_ref, LATERAL (subquery) [AS] alias [(col_list)] ...
SELECT ... FROM table_ref [INNER | CROSS | LEFT [OUTER] | RIGHT [OUTER]] JOIN LATERAL (subquery) [AS] alias [(col_list)] ON ...
```

- `LATERAL` キーワードは、派生テーブルのサブクエリの前に置く必要があります。
- テーブルエイリアスは、サブクエリの閉じ括弧の後に必ず指定する必要があります。
- エイリアスの前の `AS` キーワードは省略可能です。
- オプションの派生カラムリストをエイリアスの後に続けることができます。たとえば、`LATERAL (...) AS dt(col1, col2)` のように指定します。

## 例 {#examples}

### `LATERAL` 派生テーブルでカンマ結合を使用する {#use-a-comma-join-with-a-lateral-derived-table}

```sql
SELECT * FROM t1, LATERAL (SELECT * FROM t2 WHERE t2.id = t1.id) AS dt;
```

この例では、`t1` と `LATERAL` 派生テーブルは、同じ `FROM` 句内でカンマによって結合されています。`LATERAL` 派生テーブル内のサブクエリは、先行するテーブル `t1` のカラム `t1.id` を参照しています。`LATERAL` を付けない通常の派生テーブルでは、このような参照はサポートされません。

### `LEFT JOIN` で `LATERAL` 派生テーブル（派生カラムリスト付き）を使用する {#use-a-lateral-derived-table-with-a-derived-column-list-in-left-join}

```sql
SELECT t1.id, dt.val
FROM t1
LEFT JOIN LATERAL (SELECT t2.val FROM t2 WHERE t2.id = t1.id LIMIT 1) AS dt(val)
ON TRUE;
```

この例では、`LATERAL` 派生テーブルは `LEFT JOIN` の右側のテーブルとして使用され、左側のテーブル `t1` のカラム `t1.id` を参照できます。派生カラムリスト `(val)` は、サブクエリが返すカラムに `val` という名前を付けています。

## 標準的な派生テーブルとの比較 {#comparison-with-standard-derived-tables}

| Feature | Standard derived table | LATERAL derived table |
|---|---|---|
| 同じ `FROM` 句内で先行するテーブルのカラムを参照できるか | No | Yes |
| エイリアスが必須か | Yes | Yes |
| 派生カラムリスト | Supported | Supported |

## MySQL 互換性 {#mysql-compatibility}

TiDB の `LATERAL` 派生テーブル構文は、構文レベルで MySQL 8.0 と互換性があります。

## 関連情報 {#see-also}

- [Subquery Related Optimizations](/subquery-optimization.md)
- [Decorrelation of Correlated Subquery](/correlated-subquery-optimization.md)
- [Explain Statements That Use Subqueries](/explain-subqueries.md)
- [MySQL Compatibility](/mysql-compatibility.md)