---
title: Hash Functions
summary: このページでは、{{{ .lake }}} の Hash 関数について、機能別に整理して包括的に紹介します。
---

# Hash Functions

このページでは、{{{ .lake }}} の Hash 関数について、機能別に整理して包括的に紹介します。

## Cryptographic Hash Functions {#cryptographic-hash-functions}

| 関数 | 説明 | 例 |
|----------|-------------|--------|
| [MD5](/tidb-cloud-lake/sql/md.md) | MD5 128-bit チェックサムを計算します | `MD5('1234567890')` → `'e807f1fcf82d132f9bb018ca6738a19f'` |
| [SHA1](/tidb-cloud-lake/sql/sha.md) / [SHA](/tidb-cloud-lake/sql/sha.md) | SHA-1 160-bit チェックサムを計算します | `SHA1('1234567890')` → `'01b307acba4f54f55aafc33bb06bbbf6ca803e9a'` |
| [SHA2](/tidb-cloud-lake/sql/sha.md) | SHA-2 ファミリーのハッシュ（SHA-224、SHA-256、SHA-384、SHA-512）を計算します | `SHA2('1234567890', 256)` → `'c775e7b757ede630cd0aa1113bd102661ab38829ca52a6422ab782862f268646'` |
| [BLAKE3](/tidb-cloud-lake/sql/blake.md) | BLAKE3 ハッシュを計算します | `BLAKE3('1234567890')` → `'e2cf6ae2a7e65c7b9e089da1ad582100a0d732551a6a07abb07f7a4a119ecc51'` |

## Non-Cryptographic Hash Functions {#non-cryptographic-hash-functions}

| 関数 | 説明 | 例 |
|----------|-------------|--------|
| [XXHASH32](/tidb-cloud-lake/sql/xxhash.md) | xxHash32 32-bit ハッシュ値を計算します | `XXHASH32('1234567890')` → `3768853052` |
| [XXHASH64](/tidb-cloud-lake/sql/xxhash.md) | xxHash64 64-bit ハッシュ値を計算します | `XXHASH64('1234567890')` → `12237639266330420150` |
| [SIPHASH64](/tidb-cloud-lake/sql/siphash.md) / [SIPHASH](/tidb-cloud-lake/sql/siphash.md) | SipHash-2-4 64-bit ハッシュ値を計算します | `SIPHASH64('1234567890')` → `2917646445633666330` |
| [CITY64WITHSEED](/tidb-cloud-lake/sql/city-withseed.md) | シード値付きの CityHash64 ハッシュを計算します | `CITY64WITHSEED('1234567890', 42)` → `5210846883572933352` |

## Usage Examples {#usage-examples}

### Data Integrity Verification {#data-integrity-verification}

```sql
-- Calculate MD5 hash for file content verification
SELECT
  filename,
  MD5(file_content) AS content_hash
FROM files
ORDER BY filename;
```

### Data Anonymization {#data-anonymization}

```sql
-- Hash sensitive data before storing or processing
SELECT
  user_id,
  SHA2(email, 256) AS hashed_email,
  SHA2(phone_number, 256) AS hashed_phone
FROM users;
```

### Hash-Based Partitioning {#hash-based-partitioning}

```sql
-- Use hash functions for data distribution
SELECT
  XXHASH64(customer_id) % 10 AS partition_id,
  COUNT(*) AS records_count
FROM orders
GROUP BY partition_id;
```