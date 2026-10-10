---
title: CAST
summary: 値をあるデータ型から別のデータ型に変換します。`::` は CAST のエイリアスです。
---

# CAST

値をあるデータ型から別のデータ型に変換します。`::` は CAST のエイリアスです。

関連情報: [TRY_CAST](/tidb-cloud-lake/sql/try-cast.md)

## 構文 {#syntax}

```sql
CAST( <expr> AS <data_type> )

<expr>::<data_type>
```

## 例 {#examples}

```sql
SELECT CAST(1 AS VARCHAR), 1::VARCHAR;

┌───────────────────────────────┐
│ cast(1 as string) │ 1::string │
├───────────────────┼───────────┤
│ 1                 │ 1         │
└───────────────────────────────┘
```

文字列を Variant にキャストし、Variant を `Map<String, Variant>` にキャストします。

```sql
select '{"k1":"v1","k2":"v2"}'::Variant a, a::Map(String, String) b, b::Variant = a;
┌──────────────────────┬──────────────────────┬────────────────┐
│ a                    │ b                    │ b::VARIANT = a │
├──────────────────────┼──────────────────────┼────────────────┤
│ {"k1":"v1","k2":"v2"}│ {'k1':'v1','k2':'v2'}│ 1              │
└──────────────────────┴──────────────────────┴────────────────┘
```