---
title: Hash Functions
summary: This page provides a comprehensive overview of Hash functions in Databend, organized by functionality for easy reference.
---

# Hash Functions

This page provides a comprehensive overview of Hash functions in Databend, organized by functionality for easy reference.

## Cryptographic Hash Functions

| Function | Description | Example |
|----------|-------------|--------|
| [MD5](/tidb-cloud-lake/sql/md.md) | Calculates an MD5 128-bit checksum | `MD5('1234567890')` → `'e807f1fcf82d132f9bb018ca6738a19f'` |
| [SHA1](/tidb-cloud-lake/sql/sha.md) / [SHA](/tidb-cloud-lake/sql/sha.md) | Calculates an SHA-1 160-bit checksum | `SHA1('1234567890')` → `'01b307acba4f54f55aafc33bb06bbbf6ca803e9a'` |
| [SHA2](/tidb-cloud-lake/sql/sha.md) | Calculates SHA-2 family hash (SHA-224, SHA-256, SHA-384, SHA-512) | `SHA2('1234567890', 256)` → `'c775e7b757ede630cd0aa1113bd102661ab38829ca52a6422ab782862f268646'` |
| [BLAKE3](/tidb-cloud-lake/sql/blake.md) | Calculates a BLAKE3 hash | `BLAKE3('1234567890')` → `'e2cf6ae2a7e65c7b9e089da1ad582100a0d732551a6a07abb07f7a4a119ecc51'` |

## Non-Cryptographic Hash Functions

| Function | Description | Example |
|----------|-------------|--------|
| [XXHASH32](/tidb-cloud-lake/sql/xxhash.md) | Calculates an xxHash32 32-bit hash value | `XXHASH32('1234567890')` → `3768853052` |
| [XXHASH64](/tidb-cloud-lake/sql/xxhash.md) | Calculates an xxHash64 64-bit hash value | `XXHASH64('1234567890')` → `12237639266330420150` |
| [SIPHASH64](/tidb-cloud-lake/sql/siphash.md) / [SIPHASH](/tidb-cloud-lake/sql/siphash.md) | Calculates a SipHash-2-4 64-bit hash value | `SIPHASH64('1234567890')` → `2917646445633666330` |
| [CITY64WITHSEED](/tidb-cloud-lake/sql/city-withseed.md) | Calculates a CityHash64 hash with a seed value | `CITY64WITHSEED('1234567890', 42)` → `5210846883572933352` |

## Usage Examples

### Data Integrity Verification

```sql
-- Calculate MD5 hash for file content verification
SELECT
  filename,
  MD5(file_content) AS content_hash
FROM files
ORDER BY filename;
```

### Data Anonymization

```sql
-- Hash sensitive data before storing or processing
SELECT
  user_id,
  SHA2(email, 256) AS hashed_email,
  SHA2(phone_number, 256) AS hashed_phone
FROM users;
```

### Hash-Based Partitioning

```sql
-- Use hash functions for data distribution
SELECT
  XXHASH64(customer_id) % 10 AS partition_id,
  COUNT(*) AS records_count
FROM orders
GROUP BY partition_id;
```
