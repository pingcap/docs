---
title: Binary
summary: 原始字节的变长序列。
---

# Binary

## 概述 {#overview}

`BINARY`（别名 `VARBINARY`）用于存储变长字节序列。与 `STRING` 不同，其值不会被解释为 UTF-8 文本，因此适合存储摘要、压缩数据或序列化对象等负载。在读写数据时，可以使用 [UNHEX](/tidb-cloud-lake/sql/unhex.md)、[FROM_BASE64](/tidb-cloud-lake/sql/from-base64.md) 和 [TO_HEX](/tidb-cloud-lake/sql/to-hex.md) 等转换函数对值进行编码或解码。

## 示例 {#examples}

### 插入原始字节 {#insert-raw-bytes}

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

结果：

```
┌────┬──────────────┬──────────┐
│ id │ hex_value    │ byte_len │
├────┼──────────────┼──────────┤
│  1 │ 68656c6c6f   │        5 │
│  2 │ 646174616c616b65 │     8 │
└────┴──────────────┴──────────┘
```

### 转换回文本 {#convert-back-to-text}

在需要时，可以将二进制值转换为字符串：

```sql
SELECT
  id,
  TO_VARCHAR(raw) AS text_value
FROM binary_samples
ORDER BY id;
```

结果：

```
┌────┬─────────────┐
│ id │ text_value  │
├────┼─────────────┤
│  1 │ hello       │
│  2 │ datalake    │
└────┴─────────────┘
```

二进制列可以接受 NULL 值；当你需要将字节负载与其他数据一起存储时，也可以将其嵌套在 ARRAY、MAP 或 TUPLE 结构中。