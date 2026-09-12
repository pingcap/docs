---
title: 散列函数
summary: 本页按功能分类，全面概述 {{{ .lake }}} 中的散列函数，便于快速查阅。
---

# 散列函数

本页按功能分类，全面概述 {{{ .lake }}} 中的散列函数，便于快速查阅。

## 加密散列函数 {#cryptographic-hash-functions}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [MD5](/tidb-cloud-lake/sql/md.md) | 计算 MD5 128 位校验和 | `MD5('1234567890')` → `'e807f1fcf82d132f9bb018ca6738a19f'` |
| [SHA1](/tidb-cloud-lake/sql/sha.md) / [SHA](/tidb-cloud-lake/sql/sha.md) | 计算 SHA-1 160 位校验和 | `SHA1('1234567890')` → `'01b307acba4f54f55aafc33bb06bbbf6ca803e9a'` |
| [SHA2](/tidb-cloud-lake/sql/sha.md) | 计算 SHA-2 系列散列值（SHA-224、SHA-256、SHA-384、SHA-512） | `SHA2('1234567890', 256)` → `'c775e7b757ede630cd0aa1113bd102661ab38829ca52a6422ab782862f268646'` |
| [BLAKE3](/tidb-cloud-lake/sql/blake.md) | 计算 BLAKE3 散列值 | `BLAKE3('1234567890')` → `'e2cf6ae2a7e65c7b9e089da1ad582100a0d732551a6a07abb07f7a4a119ecc51'` |

## 非加密散列函数 {#non-cryptographic-hash-functions}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [XXHASH32](/tidb-cloud-lake/sql/xxhash.md) | 计算 xxHash32 32 位散列值 | `XXHASH32('1234567890')` → `3768853052` |
| [XXHASH64](/tidb-cloud-lake/sql/xxhash.md) | 计算 xxHash64 64 位散列值 | `XXHASH64('1234567890')` → `12237639266330420150` |
| [SIPHASH64](/tidb-cloud-lake/sql/siphash.md) / [SIPHASH](/tidb-cloud-lake/sql/siphash.md) | 计算 SipHash-2-4 64 位散列值 | `SIPHASH64('1234567890')` → `2917646445633666330` |
| [CITY64WITHSEED](/tidb-cloud-lake/sql/city-withseed.md) | 使用数据填充值计算 CityHash64 散列值 | `CITY64WITHSEED('1234567890', 42)` → `5210846883572933352` |

## 使用示例 {#usage-examples}

### 数据完整性验证 {#data-integrity-verification}

```sql
-- Calculate MD5 hash for file content verification
SELECT
  filename,
  MD5(file_content) AS content_hash
FROM files
ORDER BY filename;
```

### 数据匿名化 {#data-anonymization}

```sql
-- Hash sensitive data before storing or processing
SELECT
  user_id,
  SHA2(email, 256) AS hashed_email,
  SHA2(phone_number, 256) AS hashed_phone
FROM users;
```

### 基于散列的分区 {#hash-based-partitioning}

```sql
-- Use hash functions for data distribution
SELECT
  XXHASH64(customer_id) % 10 AS partition_id,
  COUNT(*) AS records_count
FROM orders
GROUP BY partition_id;
```