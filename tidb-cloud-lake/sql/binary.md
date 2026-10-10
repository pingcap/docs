---
title: Binary
summary: 生のバイト列を格納する可変長シーケンス。
---

# Binary

## 概要 {#overview}

`BINARY`（別名 `VARBINARY`）は、可変長のバイト列を格納します。`STRING` とは異なり、この値は UTF-8 テキストとして解釈されないため、ダイジェスト、圧縮データ、シリアライズされたオブジェクトなどのペイロードの格納に適しています。データの読み取りや書き込み時に値をエンコードまたはデコードするには、[UNHEX](/tidb-cloud-lake/sql/unhex.md)、[FROM_BASE64](/tidb-cloud-lake/sql/from-base64.md)、および [TO_HEX](/tidb-cloud-lake/sql/to-hex.md) などの変換関数を使用します。

## 例 {#examples}

### 生のバイトを挿入する {#insert-raw-bytes}

```sql
CREATE TABLE binary_samples (
  id INT,
  raw BINARY
);

INSERT INTO binary_samples VALUES
  (1, UNHEX('68656c6c6f')),             -- "hello"
  (2, FROM_BASE64('ZGF0YWxha2U='));     -- "datalake"
```

```sql
SELECT
  id,
  HEX(raw)     AS hex_value,
  LENGTH(raw)  AS byte_len
FROM binary_samples
ORDER BY id;
```

結果:

```
┌────┬──────────────┬──────────┐
│ id │ hex_value    │ byte_len │
├────┼──────────────┼──────────┤
│  1 │ 68656c6c6f   │        5 │
│  2 │ 646174616c616b65 │     8 │
└────┴──────────────┴──────────┘
```

### テキストに戻して変換する {#convert-back-to-text}

必要に応じて、バイナリ値を文字列に変換できます。

```sql
SELECT
  id,
  TO_VARCHAR(raw) AS text_value
FROM binary_samples
ORDER BY id;
```

結果:

```
┌────┬─────────────┐
│ id │ text_value  │
├────┼─────────────┤
│  1 │ hello       │
│  2 │ datalake    │
└────┴─────────────┘
```

バイナリカラムは NULL 値を受け入れることができ、他のデータと一緒にバイトペイロードを格納する必要がある場合は、ARRAY、MAP、または TUPLE 構造の中にネストすることもできます。