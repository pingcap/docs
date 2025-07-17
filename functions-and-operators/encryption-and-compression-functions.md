---
title: 加密与压缩函数
summary: 了解关于加密和压缩函数的内容。
---

# 加密与压缩函数

TiDB 支持大部分在 MySQL 8.0 中可用的 [加密和压缩函数](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html)。

## 支持的函数

| 名称                                                          | 描述                                       |
|:--------------------------------------------------------------|:--------------------------------------------|
| [`AES_DECRYPT()`](#aes_decrypt)                               | 使用 AES 解密                              |
| [`AES_ENCRYPT()`](#aes_encrypt)                               | 使用 AES 加密                              |
| [`COMPRESS()`](#compress)                                     | 压缩并返回二进制字符串                     |
| [`MD5()`](#md5)                                               | 计算 MD5 校验和                            |
| [`PASSWORD()`](#password)                                     | 计算并返回密码字符串                       |
| [`RANDOM_BYTES()`](#random_bytes)                             | 返回随机字节向量                           |
| [`SHA()`](#sha)                                               | 计算 SHA-1 160 位校验和                     |
| [`SHA1()`](#sha1)                                             | 计算 SHA-1 160 位校验和                     |
| [`SHA2()`](#sha2)                                             | 计算 SHA-2 校验和                          |
| [`SM3()`](#sm3)                                               | 计算 SM3 校验和                            |
| [`UNCOMPRESS()`](#uncompress)                                 | 解压缩已压缩的字符串                        |
| [`UNCOMPRESSED_LENGTH()`](#uncompressed_length)               | 返回压缩前字符串的长度                     |
| [`VALIDATE_PASSWORD_STRENGTH()`](#validate_password_strength) | 验证密码强度                              |

### [`AES_DECRYPT()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_aes-decrypt)

`AES_DECRYPT(data, key [,iv])` 函数使用与 [`AES_ENCRYPT()`](#aes_encrypt) 相同的 `key` 解密之前加密的 `data`。

你可以使用 [`block_encryption_mode`](/system-variables.md#block_encryption_mode) 系统变量选择 [Advanced Encryption Standard (AES)](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) 加密模式。

对于需要初始化向量的加密模式，可以通过 `iv` 参数设置。默认值为 `NULL`。

```sql
SELECT AES_DECRYPT(0x28409970815CD536428876175F1A4923, 'secret');
```

```
+----------------------------------------------------------------------------------------------------------------------+
| AES_DECRYPT(0x28409970815CD536428876175F1A4923, 'secret')                                                            |
+----------------------------------------------------------------------------------------------------------------------+
| 0x616263                                                                                                             |
+----------------------------------------------------------------------------------------------------------------------+
1 行结果，耗时 0.00 秒
```

### [`AES_ENCRYPT()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_aes-encrypt)

`AES_ENCRYPT(data, key [,iv])` 函数使用 [Advanced Encryption Standard (AES)](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) 算法，用 `key` 对 `data` 进行加密。

你可以使用 [`block_encryption_mode`](/system-variables.md#block_encryption_mode) 系统变量选择 AES 加密模式。

对于需要初始化向量的加密模式，可以通过 `iv` 参数设置。默认值为 `NULL`。

```sql
SELECT AES_ENCRYPT(0x616263,'secret');
```

```
+----------------------------------------------------------------+
| AES_ENCRYPT(0x616263,'secret')                                 |
+----------------------------------------------------------------+
| 0x28409970815CD536428876175F1A4923                             |
+----------------------------------------------------------------+
1 行结果，耗时 0.00 秒
```

### [`COMPRESS()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_compress)

`COMPRESS(expr)` 函数返回输入数据 `expr` 的压缩版本。

- 如果参数为 `NULL`，函数返回 `NULL`。
- 如果参数为空字符串，函数返回零长度值。

对于非零长度参数，函数返回一个二进制字符串，其结构如下：

- 字节 0 到 3：未压缩长度
- 字节 4 到末尾： zlib 压缩数据

```sql
SELECT COMPRESS(0x414243);
```

```
+------------------------------------------+
| COMPRESS(0x414243)                       |
+------------------------------------------+
| 0x03000000789C72747206040000FFFF018D00C7 |
+------------------------------------------+
1 行结果，耗时 0.00 秒
```

在此输出中，`0x03000000` 表示未压缩长度（3），`0x789C72747206040000FFFF018D00C7` 为 zlib 压缩数据。

使用 Python 在 TiDB 之外解码的示例：

```python
import codecs
import zlib

data = codecs.decode('03000000789C72747206040000FFFF018D00C7','hex')
print(int.from_bytes(data[:4], byteorder='little'))  # 3
print(zlib.decompress(data[4:]))  # b'ABC'
```

对于短字符串，`COMPRESS()` 可能会返回比输入更多的字节。以下示例显示，100 个 `a` 字符的字符串压缩后为 19 字节。

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
1 行结果，耗时 0.00 秒
```

### [`MD5()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_md5)

`MD5(expr)` 函数计算给定参数 `expr` 的 128 位 [MD5](https://en.wikipedia.org/wiki/MD5) 哈希值。

```sql
SELECT MD5('abc');
```

```
+----------------------------------+
| MD5('abc')                       |
+----------------------------------+
| 900150983cd24fb0d6963f7d28e17f72 |
+----------------------------------+
1 行结果，耗时 0.00 秒
```

### [`PASSWORD()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_password)

> **Warning:**
>
> 这个函数在 MySQL 5.7 中已被弃用，并在 MySQL 8.0 中移除。在 TiDB 中也已弃用。不建议使用此函数。

`PASSWORD(str)` 函数计算可用于 `mysql_native_password` 认证方法的密码哈希。

```sql
SELECT PASSWORD('secret');
```

```
+-------------------------------------------+
| PASSWORD('secret')                        |
+-------------------------------------------+
| *14E65567ABDB5135D0CFD9A70B3032C179A49EE7 |
+-------------------------------------------+
1 行结果，含警告 1 条，耗时 0.00 秒
```

### [`RANDOM_BYTES()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_random-bytes)

`RANDOM_BYTES(n)` 函数返回 `n` 个随机字节。

```sql
SELECT RANDOM_BYTES(3);
```

```
+----------------------------------+
| RANDOM_BYTES(3)                  |
+----------------------------------+
| 0x1DBC0D                         |
+----------------------------------+
1 行结果，耗时 0.00 秒
```

### [`SHA()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_sha1)

`SHA()` 函数是 [`SHA1`](#sha1) 的别名。

### [`SHA1()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_sha1)

`SHA1(expr)` 函数计算给定参数 `expr` 的 160 位 [SHA-1](https://en.wikipedia.org/wiki/SHA-1) 哈希值。

```sql
SELECT SHA1('abc');
```

```
+------------------------------------------+
| SHA1('abc')                              |
+------------------------------------------+
| a9993e364706816aba3e25717850c26c9cd0d89d |
+------------------------------------------+
1 行结果，耗时 0.00 秒
```

### [`SHA2()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_sha2)

`SHA2(str, n)` 函数使用 [SHA-2](https://en.wikipedia.org/wiki/SHA-2) 家族中的算法计算哈希值。`n` 参数用于选择算法。如果任何参数为 `NULL` 或所选算法未知或不支持，`SHA2()` 返回 `NULL`。

支持的算法如下：

| n   | 算法       |
|-----|------------|
| 0   | SHA-256    |
| 224 | SHA-224    |
| 256 | SHA-256    |
| 384 | SHA-384    |
| 512 | SHA-512    |

```sql
SELECT SHA2('abc',224);
```

```
+----------------------------------------------------------+
| SHA2('abc',224)                                          |
+----------------------------------------------------------+
| 23097d223405d8228642a477bda255b32aadbce4bda0b3f7e36c9da7 |
+----------------------------------------------------------+
1 行结果，耗时 0.00 秒
```

### `SM3()`

> **Note:**
>
> `SM3()` 函数是 TiDB 的扩展，不在 MySQL 中实现。

`SM3(str)` 函数计算给定参数 `str` 的 256 位 [ShangMi 3 (SM3)](https://en.wikipedia.org/wiki/SM3_(hash_function)) 哈希值。

```sql
SELECT SM3('abc');
```

```
+------------------------------------------------------------------+
| SM3('abc')                                                       |
+------------------------------------------------------------------+
| 66c7f0f462eeedd9d1f2d46bdc10e4e24167c4875cf2f7a2297da02b8f4ba8e0 |
+------------------------------------------------------------------+
1 行结果，耗时 0.00 秒
```

### [`UNCOMPRESS()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_uncompress)

`UNCOMPRESS(data)` 函数解压由 [`COMPRESS()`](#compress) 函数压缩的数据。

```sql
SELECT UNCOMPRESS(0x03000000789C72747206040000FFFF018D00C7);
```

```
+------------------------------------------------------------------------------------------------------------+
| UNCOMPRESS(0x03000000789C72747206040000FFFF018D00C7)                                                       |
+------------------------------------------------------------------------------------------------------------+
| 0x414243                                                                                                   |
+------------------------------------------------------------------------------------------------------------+
1 行结果，耗时 0.00 秒
```

### [`UNCOMPRESSED_LENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_uncompressed-length)

`UNCOMPRESSED_LENGTH(data)` 函数返回压缩数据的前 4 个字节，即存储压缩前字符串长度的部分。

```sql
SELECT UNCOMPRESSED_LENGTH(0x03000000789C72747206040000FFFF018D00C7);
```

```
+---------------------------------------------------------------+
| UNCOMPRESSED_LENGTH(0x03000000789C72747206040000FFFF018D00C7) |
+---------------------------------------------------------------+
| 3                                                             |
+---------------------------------------------------------------+
1 行结果，耗时 0.00 秒
```

### [`VALIDATE_PASSWORD_STRENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_validate-password-strength)

<CustomContent platform="tidb">

`VALIDATE_PASSWORD_STRENGTH(str)` 函数作为 [密码管理](/password-management.md) 的一部分使用。它计算密码的强度，并返回一个介于 0 和 100 之间的值。

</CustomContent>

<CustomContent platform="tidb-cloud">

`VALIDATE_PASSWORD_STRENGTH(str)` 函数作为密码管理的一部分使用。它计算密码的强度，并返回一个介于 0 和 100 之间的值。

</CustomContent>

`validate_password.*` 系统变量影响 `VALIDATE_PASSWORD_STRENGTH()` 函数的行为。

示例：

- 若要启用密码复杂度检查，将 [`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650) 系统变量设置为 `ON`：

    ```sql
    SET GLOBAL validate_password.enable=ON;
    ```

- 查看与密码验证相关的系统变量：

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
    8 行结果，耗时 0.01 秒
    ```

- 检查空字符串的密码强度，返回 `0`：

    ```sql
    SELECT VALIDATE_PASSWORD_STRENGTH('');
    ```

    ```
    +--------------------------------+
    | VALIDATE_PASSWORD_STRENGTH('') |
    +--------------------------------+
    |                              0 |
    +--------------------------------+
    1 行结果，耗时 0.00 秒
    ```

- 检查短字符串 `abcdef` 的密码强度，返回 `25`：

    ```sql
    SELECT VALIDATE_PASSWORD_STRENGTH('abcdef');
    ```

    ```
    +--------------------------------------+
    | VALIDATE_PASSWORD_STRENGTH('abcdef') |
    +--------------------------------------+
    |                                   25 |
    +--------------------------------------+
    1 行结果，耗时 0.00 秒
    ```

- 检查较长字符串 `abcdefghi` 的密码强度，返回 `50`。此字符串长度超过 [`validate_password.length`](/system-variables.md#validate_passwordlength-new-in-v650) 的默认值：

    ```sql
    SELECT VALIDATE_PASSWORD_STRENGTH('abcdefghi');
    ```

    ```
    +-----------------------------------------+
    | VALIDATE_PASSWORD_STRENGTH('abcdefghi') |
    +-----------------------------------------+
    |                                      50 |
    +-----------------------------------------+
    1 行结果，耗时 0.00 秒
    ```

- 在字符串中加入大写字符不会提升密码强度：

    ```sql
    SELECT VALIDATE_PASSWORD_STRENGTH('Abcdefghi');
    ```

    ```
    +-----------------------------------------+
    | VALIDATE_PASSWORD_STRENGTH('Abcdefghi') |
    +-----------------------------------------+
    |                                      50 |
    +-----------------------------------------+
    1 行结果，耗时 0.01 秒
    ```

- 在字符串中加入数字也不会提升密码强度：

    ```sql
    SELECT VALIDATE_PASSWORD_STRENGTH('Abcdefghi123');
    ```

    ```
    +--------------------------------------------+
    | VALIDATE_PASSWORD_STRENGTH('Abcdefghi123') |
    +--------------------------------------------+
    |                                         50 |
    +--------------------------------------------+
    1 行结果，耗时 0.00 秒
    ```

- 最后，在字符串中加入特殊字符会将密码强度提升到 `100`，表示密码非常强：

    ```sql
    SELECT VALIDATE_PASSWORD_STRENGTH('Abcdefghi123%$#');
    ```

    ```
    +-----------------------------------------------+
    | VALIDATE_PASSWORD_STRENGTH('Abcdefghi123%$#') |
    +-----------------------------------------------+
    |                                           100 |
    +-----------------------------------------------+
    1 行结果，耗时 0.00 秒
    ```

## 不支持的函数

* TiDB 不支持只在 MySQL 企业版中提供的函数 [Issue #2632](https://github.com/pingcap/tidb/issues/2632)。

## MySQL 兼容性

* TiDB 不支持 `STATEMENT_DIGEST()` 和 `STATEMENT_DIGEST_TEXT()` 函数。
* TiDB 不支持在 [`AES_ENCRYPT()`](#aes_encrypt) 和 [`AES_DECRYPT`](#aes_decrypt) 中添加的 `kdf_name`、`salt` 和 `iterations` 参数（MySQL 在 MySQL 8.0.30 中新增）。
* MySQL 不实现 [`SM3()`](#sm3) 函数。