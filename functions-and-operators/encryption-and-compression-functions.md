---
title: Encryption and Compression Functions
summary: Learn about the encryption and compression functions.
---

# Encryption and Compression Functions

TiDB supports most of the [encryption and compression functions](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html) available in MySQL 8.0.

## Supported functions

| Name                                                          | Description                                       |
|:--------------------------------------------------------------|:--------------------------------------------------|
| [`AES_DECRYPT()`](#aes_decrypt)                               | Decrypt using AES                                 |
| [`AES_ENCRYPT()`](#aes_encrypt)                               | Encrypt using AES                                 |
| [`COMPRESS()`](#compress)                                     | Compress and return result as a binary string     |
| [`MD5()`](#md5)                                               | Calculate MD5 checksum                            |
| [`PASSWORD()`](#password)                                     | Calculate and return a password string            |
| [`RANDOM_BYTES()`](#random_bytes)                             | Return a random byte vector                       |
| [`SHA()`](#sha)                                               | Calculate an SHA-1 160-bit checksum               |
| [`SHA1()`](#sha1)                                             | Calculate an SHA-1 160-bit checksum               |
| [`SHA2()`](#sha2)                                             | Calculate an SHA-2 checksum                       |
| [`SM3()`](#sm3)                                               | Calculate an SM3 checksum                         |
| [`UNCOMPRESS()`](#uncompress)                                 | Uncompress a compressed string                    |
| [`UNCOMPRESSED_LENGTH()`](#uncompressed_length)               | Return the length of a string before compression  |
| [`VALIDATE_PASSWORD_STRENGTH()`](#validate_password_strength) | Validate the password strength                    |

### [`AES_DECRYPT()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_aes-decrypt)

The `AES_DECRYPT(data, key [,iv])` function decrypts `data` that was previously encrypted using the [`AES_ENCRYPT()`](#aes_encrypt) function with the same `key`.

You can use the [`block_encryption_mode`](/system-variables.md#block_encryption_mode) system variable to select the [Advanced Encryption Standard (AES)](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) encryption mode.

For encryption modes that require an initialization vector, set it with the `iv` argument. The default value is `NULL`.

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

The `AES_ENCRYPT(data, key [,iv])` function encrypts `data` with `key` using the [Advanced Encryption Standard (AES)](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) algorithm.

You can use the [`block_encryption_mode`](/system-variables.md#block_encryption_mode) system variable to select the AES encryption mode.

For encryption modes that require an initialization vector, set it with the `iv` argument. The default value is `NULL`.

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

The `COMPRESS(expr)` function returns a compressed version of the input data `expr`.

- If the argument is `NULL`, the function returns `NULL`.
- If the argument is an empty string, the function returns a zero-length value.

For non-zero length argument, the function returns a binary string with the following structure:

- Bytes 0 to 3: the uncompressed length
- Bytes 4 to the end: the zlib compressed data

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

In this output, `0x03000000` represents the uncompressed length (3) and `0x789C72747206040000FFFF018D00C7` is the zlib compressed data.

An example of using Python to decode this outside of TiDB:

```python
import codecs
import zlib

data = codecs.decode('03000000789C72747206040000FFFF018D00C7','hex')
print(int.from_bytes(data[:4], byteorder='little'))  # 3
print(zlib.decompress(data[4:]))  # b'ABC'
```

For short strings, `COMPRESS()` might return more bytes than the input. The following example shows that a string of 100 `a` characters compresses to 19 bytes.

```sql
WITH x AS (SELECT REPEAT('a',100) 'a')
SELECT LENGTH(a),LENGTH(COMPRESS(a)) FROM x;
```

```
+-----------+---------------------+
| LENGTH(a) | LENGTH(COMPRESS(a)) |
+-----------+---------------------+
|       100 |                  19 |
+-----------+---------------------+
1 row in set (0.00 sec)
```

### [`MD5()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_md5)

The `MD5(expr)` function calculates a 128-bit [MD5](https://en.wikipedia.org/wiki/MD5) hash for the given argument `expr`.

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

> **Warning:**
>
> This function is deprecated in MySQL 5.7 and removed in MySQL 8.0. It is deprecated in TiDB. It is not recommended to use this function.

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

The `SHA()` function is an alias for [`SHA1`](#sha1).

### [`SHA1()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_sha1)

The `SHA1(expr)` function calculates a 160-bit [SHA-1](https://en.wikipedia.org/wiki/SHA-1) hash for the given argument `expr`.

```sql
SELECT SHA1('abc');
```

```
+------------------------------------------+
| SHA1('abc')                              |
+------------------------------------------+
| a9993e364706816aba3e25717850c26c9cd0d89d |
+------------------------------------------+
1 row in set (0.00 sec)
```

### [`SHA2()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_sha2)

The `SHA2(str, n)` function calculates a hash using an algorithm from the [SHA-2](https://en.wikipedia.org/wiki/SHA-2) family. The `n` argument is used to select the algorithm. `SHA2()` returns `NULL` if any of the arguments are `NULL` or if the algorithm selected by `n` is unknown or unsupported.

The following lists supported algorithms:

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
> The `SM3()` function is a TiDB extension and is not implemented in MySQL.

The `SM3(str)` function calculates a 256-bit [ShangMi 3 (SM3)](https://en.wikipedia.org/wiki/SM3_(hash_function)) hash for the given argument `str`.

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

### [`UNCOMPRESS()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_uncompress)

The `UNCOMPRESS(data)` function decompresses the data that was compressed with the [`COMPRESS()`](#compress) function.

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

The `UNCOMPRESSED_LENGTH(data)` function returns the first 4 bytes of the compressed data, which store the length that the compressed string had before being compressed with the [`COMPRESS()`](#compress) function.

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

<CustomContent platform="tidb">

The `VALIDATE_PASSWORD_STRENGTH(str)` function is used as part of [password management](/password-management.md). It calculates the strength of a password and returns a value between 0 and 100.

</CustomContent>

<CustomContent platform="tidb-cloud">

The `VALIDATE_PASSWORD_STRENGTH(str)` function is used as part of password management. It calculates the strength of a password and returns a value between 0 and 100.

</CustomContent>

The [`validate_password.*`](/system-variables.md) system variables affect the behavior of the `VALIDATE_PASSWORD_STRENGTH()` function.

Examples:

- To enable the password complexity check, set the [`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650) system variable to `ON`:

    ```sql
    SET GLOBAL validate_password.enable=ON;
    ```

- View password validation-related system variables:

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

- Check the password strength of an empty string, which returns `0`:

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

- Check the password strength of a short string `abcdef`, which returns `25`:

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

- Check the password strength of a longer string `abcdefghi`, which returns `50`. This string is longer than the default value of [`validate_password.length`](/system-variables.md#validate_passwordlength-new-in-v650):

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

- Adding an upper-case character to the string does not improve the password strength:

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

- Adding numbers to the string also does not improve the password strength:

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

- Finally, adding special characters to the string brings the password strength to `100`, indicating a strong password:

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
* TiDB does not support the `kdf_name`, `salt`, and `iterations` arguments for [`AES_ENCRYPT()`](#aes_encrypt) and [`AES_DECRYPT`](#aes_decrypt) that MySQL added in MySQL 8.0.30.
* MySQL does not implement the [`SM3()`](#sm3) function.