---
title: Encryption and Compression Functions
summary: Learn about the encryption and compression functions.
aliases: ['/docs/dev/functions-and-operators/encryption-and-compression-functions/','/docs/dev/reference/sql/functions-and-operators/encryption-and-compression-functions/']
---

# Encryption and Compression Functions

TiDB supports most of the [encryption and compression functions](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html) available in MySQL 8.0.

## Supported functions

| Name                                                                                                                                               | Description                                       |
|:------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------|
| [`MD5()`](#md5)                                               | Calculate MD5 checksum                            |
| [`PASSWORD()`](#password)                                     | Calculate and return a password string            |
| [`RANDOM_BYTES()`](#random_bytes)                             | Return a random byte vector                       |
| [`SHA()`](#sha)                                               | Calculate an SHA-1 160-bit checksum               |
| [`SHA1()`](#sha1)                                             | Calculate an SHA-1 160-bit checksum               |
| [`SHA2()`](#sha2)                                             | Calculate an SHA-2 checksum                       |
| [`SM3()`](#sm3)                                               | Calculate an SM3 checksum                         |
| [`AES_DECRYPT()`](#aes_decrypt)                               | Decrypt using AES                                 |
| [`AES_ENCRYPT()`](#aes_encrypt)                               | Encrypt using AES                                 |
| [`COMPRESS()`](#compress)                                     | Return result as a binary string                  |
| [`UNCOMPRESS()`](#uncompress)                                 | Uncompress a string compressed                    |
| [`UNCOMPRESSED_LENGTH()`](#uncompressed_length)               | Return the length of a string before compression  |
| [`VALIDATE_PASSWORD_STRENGTH()`](#validate_password_strength) | Validate the password strength |

### [`MD5()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_md5)

The `MD5(expr)` function can be used to calculate a 128-bit [MD5](https://en.wikipedia.org/wiki/MD5) hash.

```sql
SELECT MD5('abc');
```

```
+----------------------------------+
| MD5('abc')                       |
+----------------------------------+
| 900150983cd24fb0d6963f7d28e17f72 |
+----------------------------------+
1 row in set (0.00 sec)
```

### [`PASSWORD()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_password)

> **Note:**
>
> This functions was deprecated in MySQL 5.7 and removed in MySQL 8.0. This function is deprecated in TiDB. Using this function is not recommended.

The `PASSWORD(str)` function calculates a password hash that can be used with the `mysql_native_password` authentication method.

```sql
SELECT PASSWORD('secret');
```

```
+-------------------------------------------+
| PASSWORD('secret')                        |
+-------------------------------------------+
| *14E65567ABDB5135D0CFD9A70B3032C179A49EE7 |
+-------------------------------------------+
1 row in set, 1 warning (0.00 sec)

Warning (Code 1681): PASSWORD is deprecated and will be removed in a future release.
```

### [`RANDOM_BYTES()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_random-bytes)

The `RANDOM_BYTES(n)` function returns `n` random bytes.

```sql
SELECT RANDOM_BYTES(3);
```

```
+----------------------------------+
| RANDOM_BYTES(3)                  |
+----------------------------------+
| 0x1DBC0D                         |
+----------------------------------+
1 row in set (0.00 sec)
```

### [`SHA()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_sha1)

The `SHA()` function is an alias for [`SHA1`](#sha1)

### [`SHA1()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_sha1)

The `SHA1(expr)` function calculates a 160 bit [SHA-1](https://en.wikipedia.org/wiki/SHA-1) hash.

```sql
SELECT SHA1('abc');
```

```
+------------------------------------------+
| SHA1('abc')                               |
+------------------------------------------+
| a9993e364706816aba3e25717850c26c9cd0d89d |
+------------------------------------------+
1 row in set (0.00 sec)
```

### [`SHA2()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_sha2)

The `SHA2(str, n)` function calculates a hash from the [SHA-2] family. The `n` argument is used to select the algorithm. `SHA2()` returns `NULL` if any of the arguments are `NULL` or if the algorithm selected by `n` isn't known or supported.

| n   | Algorithm |
|-----|-----------|
| 0   | SHA-256   |
| 224 | SHA-224   |
| 256 | SHA-256   |
| 384 | SHA-384   |
| 512 | SHA-512   |

```sql
SELECT SHA2('abc',224);
```

```
+----------------------------------------------------------+
| SHA2('abc',224)                                          |
+----------------------------------------------------------+
| 23097d223405d8228642a477bda255b32aadbce4bda0b3f7e36c9da7 |
+----------------------------------------------------------+
1 row in set (0.00 sec)
```

### `SM3()`

> **Note:**
>
> MySQL doesn't implement the `SM3()` function, this is a TiDB extension.

The `SM3(str)` function calculates a 256-bit ShangMi 3 ([SM3](https://en.wikipedia.org/wiki/SM3_(hash_function))) hash.

```sql
SELECT SM3('abc');
```

```
+------------------------------------------------------------------+
| SM3('abc')                                                       |
+------------------------------------------------------------------+
| 66c7f0f462eeedd9d1f2d46bdc10e4e24167c4875cf2f7a2297da02b8f4ba8e0 |
+------------------------------------------------------------------+
1 row in set (0.00 sec)
```

### [`AES_DECRYPT()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_aes-decrypt)

The `AES_DECRYPT(data, key [,iv])` function decrypts `data` that has previously been encrypted by the [`AES_ENCRYPT()`](#aes_encrypt) function with the same `key`.

The [`block_encryption_mode`](/system-variables.md#block_encryption_mode) can be used to select the AES encryption mode.

The initialization vector can be set with the `iv` argument for encryption modes that require it. The default is `NULL`.

```sql
SELECT AES_DECRYPT(0x28409970815CD536428876175F1A4923, 'secret');
```

```
+----------------------------------------------------------------------------------------------------------------------+
| AES_DECRYPT(0x28409970815CD536428876175F1A4923, 'secret')                                                            |
+----------------------------------------------------------------------------------------------------------------------+
| 0x616263                                                                                                             |
+----------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

### [`AES_ENCRYPT()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_aes-encrypt)

The `AES_ENCRYPT(data, key [,iv])` function encrypts `data` with the `key` using the Advanced Encryption Standard ([AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)).

The [`block_encryption_mode`](/system-variables.md#block_encryption_mode) can be used to select the AES encryption mode.

The initialization vector can be set with the `iv` argument for encryption modes that require it. The default is `NULL`.

```sql
SELECT AES_ENCRYPT(0x616263,'secret');
```

```
+----------------------------------------------------------------+
| AES_ENCRYPT(0x616263,'secret')                                 |
+----------------------------------------------------------------+
| 0x28409970815CD536428876175F1A4923                             |
+----------------------------------------------------------------+
1 row in set (0.00 sec)
```

### [`COMPRESS()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_compress)

The `COMPRESS(expr)` returns a compressed version of the data supplied in the argument.

If the argument is set to `NULL` then `COMPRESS()` returns `NULL`.

If the argument has a length of 0 then `COMPRESS()` returns a length of 0.

The returned value of any argument of a non-zero length argument consists of:
- bytes 0 to 4: the uncompressed length
- bytes 4 to end: the zlib compressed data

```sql
SELECT COMPRESS(0x414243);
```

```
+------------------------------------------+
| COMPRESS(0x414243)                       |
+------------------------------------------+
| 0x03000000789C72747206040000FFFF018D00C7 |
+------------------------------------------+
1 row in set (0.00 sec)
```

Here the `0x03000000` is the length (3) of the uncompressed version and `0x789C72747206040000FFFF018D00C7` is the zlib compressed data.

An example to decode this outside of TiDB:

```python
>>> import codecs
>>> import zlib
>>> data = codecs.decode('03000000789C72747206040000FFFF018D00C7','hex')
>>> print(int.from_bytes(data[:4], byteorder='little'))
3
>>> print(zlib.decompress(data[4:]))
b'ABC'
```

```sql
WITH x AS (SELECT REPEAT('a',100) 'a')
SELECT LENGTH(a),LENGTH(COMPRESS(a)) FROM x;
```

The example below shows that a string of 100 `a`s compresses to 19 bytes. For short strings the `COMPRESS()` will return more bytes than the input.

```
+-----------+---------------------+
| LENGTH(a) | LENGTH(COMPRESS(a)) |
+-----------+---------------------+
|       100 |                  19 |
+-----------+---------------------+
1 row in set (0.00 sec)
```

### [`UNCOMPRESS()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_uncompress)

The `UNCOMPRESS(data)` function uncompressed data that was compressed with the [`COMPRESS()`](#compress) function.

```sql
SELECT UNCOMPRESS(0x03000000789C72747206040000FFFF018D00C7);
```

```
+------------------------------------------------------------------------------------------------------------+
| UNCOMPRESS(0x03000000789C72747206040000FFFF018D00C7)                                                       |
+------------------------------------------------------------------------------------------------------------+
| 0x414243                                                                                                   |
+------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

### [`UNCOMPRESSED_LENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_uncompressed-length)

The `UNCOMPRESSED_LENGTH(data)` returns the length that is stored in the first 4 bytes of a value that was compressed with the [`COMPRESS()`](#compress) function. 

```sql
SELECT UNCOMPRESSED_LENGTH(0x03000000789C72747206040000FFFF018D00C7);
```

```
+---------------------------------------------------------------+
| UNCOMPRESSED_LENGTH(0x03000000789C72747206040000FFFF018D00C7) |
+---------------------------------------------------------------+
|                                                             3 |
+---------------------------------------------------------------+
1 row in set (0.00 sec)
```

### [`VALIDATE_PASSWORD_STRENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_validate-password-strength)

The ``VALIDATE_PASSWORD_STRENGTH(str)` function is used as part of [password management](/password-management.md) to calculate the strength of a password. The strength that is returned is a number between 0 and 100.

The [`validate_password.*`](/system-variables.md) variables affect the [`VALIDATE_PASSWORD_STRENGTH()`](#validate_password_strength) function

Examples:

We first set the [`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650) variable to `ON`.

```sql
SET GLOBAL validate_password.enable=ON;
```

```
Query OK, 0 rows affected (0.01 sec)
```

Then we inspect the other system variables that are related to password validation.

```sql
SHOW VARIABLES LIKE 'validate_password.%';
```

```
+--------------------------------------+--------+
| Variable_name                        | Value  |
+--------------------------------------+--------+
| validate_password.check_user_name    | ON     |
| validate_password.dictionary         |        |
| validate_password.enable             | ON     |
| validate_password.length             | 8      |
| validate_password.mixed_case_count   | 1      |
| validate_password.number_count       | 1      |
| validate_password.policy             | MEDIUM |
| validate_password.special_char_count | 1      |
+--------------------------------------+--------+
8 rows in set (0.01 sec)
```

We first check the password strength of an empty string, which returns 0.

```sql
SELECT VALIDATE_PASSWORD_STRENGTH('');
```

```
+--------------------------------+
| VALIDATE_PASSWORD_STRENGTH('') |
+--------------------------------+
|                              0 |
+--------------------------------+
1 row in set (0.00 sec)
```

Then we check the password strength of an short string, which returns 25.

```sql
SELECT VALIDATE_PASSWORD_STRENGTH('abcdef');
```

```
+--------------------------------------+
| VALIDATE_PASSWORD_STRENGTH('abcdef') |
+--------------------------------------+
|                                   25 |
+--------------------------------------+
1 row in set (0.00 sec)
```

Then we check the password strength of an longer string, which returns 50. This is now more characters than we have configured with [`validate_password.length`](/system-variables.md#validate_passwordlength-new-in-v650).

```sql
SELECT VALIDATE_PASSWORD_STRENGTH('abcdefghi');
```

```
+-----------------------------------------+
| VALIDATE_PASSWORD_STRENGTH('abcdefghi') |
+-----------------------------------------+
|                                      50 |
+-----------------------------------------+
1 row in set (0.00 sec)
```

Now we add an upper-case character. This still returns 50.

```sql
SELECT VALIDATE_PASSWORD_STRENGTH('Abcdefghi');
```

```
+-----------------------------------------+
| VALIDATE_PASSWORD_STRENGTH('Abcdefghi') |
+-----------------------------------------+
|                                      50 |
+-----------------------------------------+
1 row in set (0.01 sec)
```

Now we add numbers. This still returns 50.

```sql
SELECT VALIDATE_PASSWORD_STRENGTH('Abcdefghi123');
```

```
+--------------------------------------------+
| VALIDATE_PASSWORD_STRENGTH('Abcdefghi123') |
+--------------------------------------------+
|                                         50 |
+--------------------------------------------+
1 row in set (0.00 sec)
```

Now we add special characters and we finally get to 100, which means this is a strong password.

```sql
SELECT VALIDATE_PASSWORD_STRENGTH('Abcdefghi123%$#');
```

```
+-----------------------------------------------+
| VALIDATE_PASSWORD_STRENGTH('Abcdefghi123%$#') |
+-----------------------------------------------+
|                                           100 |
+-----------------------------------------------+
1 row in set (0.00 sec)
```

## Unsupported functions

* TiDB does not support the functions only available in MySQL Enterprise [Issue #2632](https://github.com/pingcap/tidb/issues/2632).

## MySQL compatibility

* TiDB does not support the `STATEMENT_DIGEST()` and `STATEMENT_DIGEST_TEXT()` functions.
* TiDB does not support the KDF, salt and iterations arguments for [`AES_ENCRYPT()`](#aes_encrypt) and [`AES_DECRYPT`](#aes_decrypt) that MySQL added in MySQL 8.0.30.
* MySQL does not implement the [`SM3()`](#sm3) function.

