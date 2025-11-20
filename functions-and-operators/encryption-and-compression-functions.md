---
title: Encryption and Compression Functions
summary: 暗号化と圧縮の関数について学びます。
---

# 暗号化と圧縮機能 {#encryption-and-compression-functions}

TiDB は、MySQL 8.0 で利用可能な[暗号化および圧縮関数](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html)のほとんどをサポートしています。

## サポートされている関数 {#supported-functions}

| 名前                                                            | 説明                      |
| :------------------------------------------------------------ | :---------------------- |
| [`AES_DECRYPT()`](#aes_decrypt)                               | AESを使用して復号する            |
| [`AES_ENCRYPT()`](#aes_encrypt)                               | AESを使用して暗号化する           |
| [`COMPRESS()`](#compress)                                     | 結果を圧縮してバイナリ文字列として返す     |
| [`MD5()`](#md5)                                               | MD5チェックサムを計算する          |
| [`PASSWORD()`](#password)                                     | パスワード文字列を計算して返す         |
| [`RANDOM_BYTES()`](#random_bytes)                             | ランダムなバイトベクトルを返す         |
| [`SHA()`](#sha)                                               | SHA-1 160ビットチェックサムを計算する |
| [`SHA1()`](#sha1)                                             | SHA-1 160ビットチェックサムを計算する |
| [`SHA2()`](#sha2)                                             | SHA-2チェックサムを計算する        |
| [`SM3()`](#sm3)                                               | SM3チェックサムを計算する          |
| [`UNCOMPRESS()`](#uncompress)                                 | 圧縮された文字列を解凍する           |
| [`UNCOMPRESSED_LENGTH()`](#uncompressed_length)               | 圧縮前の文字列の長さを返す           |
| [`VALIDATE_PASSWORD_STRENGTH()`](#validate_password_strength) | パスワードの強度を検証する           |

### <code>AES_DECRYPT()</code> {#code-aes-decrypt-code}

`AES_DECRYPT(data, key [,iv])`関数は、同じ`key`を使用して[`AES_ENCRYPT()`](#aes_encrypt)関数を使用して以前に暗号化された`data`復号化します。

[`block_encryption_mode`](/system-variables.md#block_encryption_mode)システム変数を使用して[高度暗号化規格（AES）](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)暗号化モードを選択できます。

初期化ベクトルを必要とする暗号化モードの場合は、 `iv`引数で設定します。デフォルト値は`NULL`です。

```sql
SELECT AES_DECRYPT(0x28409970815CD536428876175F1A4923, 'secret');
```

    +----------------------------------------------------------------------------------------------------------------------+
    | AES_DECRYPT(0x28409970815CD536428876175F1A4923, 'secret')                                                            |
    +----------------------------------------------------------------------------------------------------------------------+
    | 0x616263                                                                                                             |
    +----------------------------------------------------------------------------------------------------------------------+
    1 row in set (0.00 sec)

### <code>AES_ENCRYPT()</code> {#code-aes-encrypt-code}

`AES_ENCRYPT(data, key [,iv])`関数は、 [高度暗号化規格（AES）](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)アルゴリズムを使用して`data` `key`で暗号化します。

[`block_encryption_mode`](/system-variables.md#block_encryption_mode)システム変数を使用して、AES 暗号化モードを選択できます。

初期化ベクトルを必要とする暗号化モードの場合は、 `iv`引数で設定します。デフォルト値は`NULL`です。

```sql
SELECT AES_ENCRYPT(0x616263,'secret');
```

    +----------------------------------------------------------------+
    | AES_ENCRYPT(0x616263,'secret')                                 |
    +----------------------------------------------------------------+
    | 0x28409970815CD536428876175F1A4923                             |
    +----------------------------------------------------------------+
    1 row in set (0.00 sec)

### <code>COMPRESS()</code> {#code-compress-code}

`COMPRESS(expr)`関数は入力データ`expr`の圧縮バージョンを返します。

-   引数が`NULL`の場合、関数は`NULL`返します。
-   引数が空の文字列の場合、関数は長さ 0 の値を返します。

長さがゼロ以外の引数の場合、関数は次の構造を持つバイナリ文字列を返します。

-   バイト0～3: 非圧縮時の長さ
-   バイト4から最後まで: zlib圧縮データ

```sql
SELECT COMPRESS(0x414243);
```

    +------------------------------------------+
    | COMPRESS(0x414243)                       |
    +------------------------------------------+
    | 0x03000000789C72747206040000FFFF018D00C7 |
    +------------------------------------------+
    1 row in set (0.00 sec)

この出力では、 `0x03000000`圧縮されていない長さ (3) を表し、 `0x789C72747206040000FFFF018D00C7` zlib で圧縮されたデータを表します。

Python を使用して TiDB の外部でこれをデコードする例:

```python
import codecs
import zlib

data = codecs.decode('03000000789C72747206040000FFFF018D00C7','hex')
print(int.from_bytes(data[:4], byteorder='little'))  # 3
print(zlib.decompress(data[4:]))  # b'ABC'
```

短い文字列の場合、 `COMPRESS()`入力よりも多くのバイト数を返す可能性があります。次の例では、 `a`文字の文字列が19バイトに圧縮されることを示しています。

```sql
WITH x AS (SELECT REPEAT('a',100) 'a')
SELECT LENGTH(a),LENGTH(COMPRESS(a)) FROM x;
```

    +-----------+---------------------+
    | LENGTH(a) | LENGTH(COMPRESS(a)) |
    +-----------+---------------------+
    |       100 |                  19 |
    +-----------+---------------------+
    1 row in set (0.00 sec)

### <code>MD5()</code> {#code-md5-code}

`MD5(expr)`関数は、指定された引数`expr`に対して 128 ビットの[MD5](https://en.wikipedia.org/wiki/MD5)ハッシュを計算します。

```sql
SELECT MD5('abc');
```

    +----------------------------------+
    | MD5('abc')                       |
    +----------------------------------+
    | 900150983cd24fb0d6963f7d28e17f72 |
    +----------------------------------+
    1 row in set (0.00 sec)

### <code>PASSWORD()</code> {#code-password-code}

> **警告：**
>
> この関数はMySQL 5.7で非推奨となり、MySQL 8.0で削除されました。TiDBでも非推奨です。この関数の使用は推奨されません。

`PASSWORD(str)`関数は、 `mysql_native_password`認証方法で使用できるパスワード ハッシュを計算します。

```sql
SELECT PASSWORD('secret');
```

    +-------------------------------------------+
    | PASSWORD('secret')                        |
    +-------------------------------------------+
    | *14E65567ABDB5135D0CFD9A70B3032C179A49EE7 |
    +-------------------------------------------+
    1 row in set, 1 warning (0.00 sec)

    Warning (Code 1681): PASSWORD is deprecated and will be removed in a future release.

### <code>RANDOM_BYTES()</code> {#code-random-bytes-code}

`RANDOM_BYTES(n)`関数は`n`ランダム バイトを返します。

```sql
SELECT RANDOM_BYTES(3);
```

    +----------------------------------+
    | RANDOM_BYTES(3)                  |
    +----------------------------------+
    | 0x1DBC0D                         |
    +----------------------------------+
    1 row in set (0.00 sec)

### <code>SHA()</code> {#code-sha-code}

`SHA()`関数は[`SHA1`](#sha1)エイリアスです。

### <code>SHA1()</code> {#code-sha1-code}

`SHA1(expr)`関数は、指定された引数`expr`に対して 160 ビット[SHA-1](https://en.wikipedia.org/wiki/SHA-1)ハッシュを計算します。

```sql
SELECT SHA1('abc');
```

    +------------------------------------------+
    | SHA1('abc')                              |
    +------------------------------------------+
    | a9993e364706816aba3e25717850c26c9cd0d89d |
    +------------------------------------------+
    1 row in set (0.00 sec)

### <code>SHA2()</code> {#code-sha2-code}

`SHA2(str, n)`関数は`n` [SHA-2](https://en.wikipedia.org/wiki/SHA-2)ファミリーのアルゴリズムを使用してハッシュを計算します。5 引数はアルゴリズムを選択するために使用されます。7 `SHA2()` 、引数のいずれかが`NULL`の場合、または`n`で選択されたアルゴリズムが不明またはサポートされていない場合、 `NULL`返します。

サポートされているアルゴリズムは次のとおりです。

| n   | アルゴリズム  |
| --- | ------- |
| 0   | SHA-256 |
| 224 | SHA-224 |
| 256 | SHA-256 |
| 384 | SHA-384 |
| 512 | SHA-512 |

```sql
SELECT SHA2('abc',224);
```

    +----------------------------------------------------------+
    | SHA2('abc',224)                                          |
    +----------------------------------------------------------+
    | 23097d223405d8228642a477bda255b32aadbce4bda0b3f7e36c9da7 |
    +----------------------------------------------------------+
    1 row in set (0.00 sec)

### <code>SM3()</code> {#code-sm3-code}

> **注記：**
>
> `SM3()`関数は TiDB 拡張機能であり、MySQL では実装されていません。

`SM3(str)`関数は、指定された引数`str`に対して 256 ビットの[シャンミ 3 (SM3)](https://en.wikipedia.org/wiki/SM3_(hash_function))ハッシュを計算します。

```sql
SELECT SM3('abc');
```

    +------------------------------------------------------------------+
    | SM3('abc')                                                       |
    +------------------------------------------------------------------+
    | 66c7f0f462eeedd9d1f2d46bdc10e4e24167c4875cf2f7a2297da02b8f4ba8e0 |
    +------------------------------------------------------------------+
    1 row in set (0.00 sec)

### <code>UNCOMPRESS()</code> {#code-uncompress-code}

`UNCOMPRESS(data)`関数は[`COMPRESS()`](#compress)関数で圧縮されたデータを解凍します。

```sql
SELECT UNCOMPRESS(0x03000000789C72747206040000FFFF018D00C7);
```

    +------------------------------------------------------------------------------------------------------------+
    | UNCOMPRESS(0x03000000789C72747206040000FFFF018D00C7)                                                       |
    +------------------------------------------------------------------------------------------------------------+
    | 0x414243                                                                                                   |
    +------------------------------------------------------------------------------------------------------------+
    1 row in set (0.00 sec)

### <code>UNCOMPRESSED_LENGTH()</code> {#code-uncompressed-length-code}

`UNCOMPRESSED_LENGTH(data)`関数は、圧縮データの最初の 4 バイトを返します。これには、 [`COMPRESS()`](#compress)関数で圧縮される前の圧縮文字列の長さが格納されます。

```sql
SELECT UNCOMPRESSED_LENGTH(0x03000000789C72747206040000FFFF018D00C7);
```

    +---------------------------------------------------------------+
    | UNCOMPRESSED_LENGTH(0x03000000789C72747206040000FFFF018D00C7) |
    +---------------------------------------------------------------+
    |                                                             3 |
    +---------------------------------------------------------------+
    1 row in set (0.00 sec)

### <code>VALIDATE_PASSWORD_STRENGTH()</code> {#code-validate-password-strength-code}

<CustomContent platform="tidb">

`VALIDATE_PASSWORD_STRENGTH(str)`関数は[パスワード管理](/password-management.md)の一部として使用されます。パスワードの強度を計算し、0 から 100 までの値を返します。

</CustomContent>

<CustomContent platform="tidb-cloud">

`VALIDATE_PASSWORD_STRENGTH(str)`関数はパスワード管理の一部として使用されます。パスワードの強度を計算し、0から100までの値を返します。

</CustomContent>

[`validate_password.*`](/system-variables.md)システム変数は、 `VALIDATE_PASSWORD_STRENGTH()`関数の動作に影響します。

例:

-   パスワードの複雑さのチェックを有効にするには、 [`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650)システム変数を`ON`に設定します。

    ```sql
    SET GLOBAL validate_password.enable=ON;
    ```

-   パスワード検証関連のシステム変数をビュー。

    ```sql
    SHOW VARIABLES LIKE 'validate_password.%';
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

-   空の文字列のパスワード強度をチェックします`0`が返されます。

    ```sql
    SELECT VALIDATE_PASSWORD_STRENGTH('');
    ```

        +--------------------------------+
        | VALIDATE_PASSWORD_STRENGTH('') |
        +--------------------------------+
        |                              0 |
        +--------------------------------+
        1 row in set (0.00 sec)

-   短い文字列`abcdef`のパスワード強度をチェックすると、 `25`が返されます。

    ```sql
    SELECT VALIDATE_PASSWORD_STRENGTH('abcdef');
    ```

        +--------------------------------------+
        | VALIDATE_PASSWORD_STRENGTH('abcdef') |
        +--------------------------------------+
        |                                   25 |
        +--------------------------------------+
        1 row in set (0.00 sec)

-   長い文字列`abcdefghi`のパスワード強度をチェックすると、 `50`返されます。この文字列はデフォルト値の[`validate_password.length`](/system-variables.md#validate_passwordlength-new-in-v650)よりも長いです。

    ```sql
    SELECT VALIDATE_PASSWORD_STRENGTH('abcdefghi');
    ```

        +-----------------------------------------+
        | VALIDATE_PASSWORD_STRENGTH('abcdefghi') |
        +-----------------------------------------+
        |                                      50 |
        +-----------------------------------------+
        1 row in set (0.00 sec)

-   文字列に大文字を追加しても、パスワードの強度は向上しません。

    ```sql
    SELECT VALIDATE_PASSWORD_STRENGTH('Abcdefghi');
    ```

        +-----------------------------------------+
        | VALIDATE_PASSWORD_STRENGTH('Abcdefghi') |
        +-----------------------------------------+
        |                                      50 |
        +-----------------------------------------+
        1 row in set (0.01 sec)

-   文字列に数字を追加しても、パスワードの強度は向上しません。

    ```sql
    SELECT VALIDATE_PASSWORD_STRENGTH('Abcdefghi123');
    ```

        +--------------------------------------------+
        | VALIDATE_PASSWORD_STRENGTH('Abcdefghi123') |
        +--------------------------------------------+
        |                                         50 |
        +--------------------------------------------+
        1 row in set (0.00 sec)

-   最後に、文字列に特殊文字を追加すると、パスワードの強度が`100`になり、強力なパスワードであることを示します。

    ```sql
    SELECT VALIDATE_PASSWORD_STRENGTH('Abcdefghi123%$#');
    ```

        +-----------------------------------------------+
        | VALIDATE_PASSWORD_STRENGTH('Abcdefghi123%$#') |
        +-----------------------------------------------+
        |                                           100 |
        +-----------------------------------------------+
        1 row in set (0.00 sec)

## サポートされていない関数 {#unsupported-functions}

-   TiDB は、MySQL Enterprise [問題 #2632](https://github.com/pingcap/tidb/issues/2632)でのみ利用可能な関数をサポートしていません。

## MySQLの互換性 {#mysql-compatibility}

-   TiDB は`STATEMENT_DIGEST()`および`STATEMENT_DIGEST_TEXT()`関数をサポートしていません。
-   TiDB は、MySQL 8.0.30 で追加された[`AES_ENCRYPT()`](#aes_encrypt)と[`AES_DECRYPT`](#aes_decrypt)の`kdf_name` 、 `salt` 、 `iterations`引数をサポートしていません。
-   MySQL は[`SM3()`](#sm3)関数を実装していません。
