---
title: Utility Functions
summary: このドキュメントでは、TiDB でサポートされているユーティリティ関数について説明します。
---

# ユーティリティ関数 {#utility-functions}

このドキュメントでは、一般的なデータ変換を簡素化して読みやすさを向上させるように設計された、TiDB でサポートされているユーティリティ関数を紹介します。

## <code>FORMAT_BYTES()</code> {#code-format-bytes-code}

`FORMAT_BYTES()`関数は、バイト数を人間が読める形式に変換します。

```sql
SELECT FORMAT_BYTES(10*1024*1024);
```

    +----------------------------+
    | FORMAT_BYTES(10*1024*1024) |
    +----------------------------+
    | 10.00 MiB                  |
    +----------------------------+
    1 row in set (0.001 sec)

## <code>FORMAT_NANO_TIME()</code> {#code-format-nano-time-code}

`FORMAT_NANO_TIME()`関数は、ナノ秒数を人間が読める時間形式に変換します。

```sql
SELECT FORMAT_NANO_TIME(1000000);
```

    +---------------------------+
    | FORMAT_NANO_TIME(1000000) |
    +---------------------------+
    | 1.00 ms                   |
    +---------------------------+
    1 row in set (0.001 sec)
