---
title: Encryption and Compression Functions
summary: Learn about the encryption and compression functions.
---

# 暗号化および圧縮機能 {#encryption-and-compression-functions}

TiDB は、 MySQL 5.7で利用可能なほとんどの[<a href="https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html">暗号化および圧縮関数</a>](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html)をサポートします。

## サポートされている関数 {#supported-functions}

| 名前                                                                                                                                                                                                                                                          | 説明                                            |
| :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------- |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_md5">`MD5()`</a>](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_md5)                                                                      | MD5チェックサムを計算する                                |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_password">`PASSWORD()`</a>](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_password)                                                       | パスワード文字列を計算して返します                             |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_random-bytes">`RANDOM_BYTES()`</a>](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_random-bytes)                                           | ランダムなバイトベクトルを返す                               |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_sha1">`SHA1(), SHA()`</a>](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_sha1)                                                            | SHA-1 160 ビット チェックサムを計算する                     |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_sha2">`SHA2()`</a>](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_sha2)                                                                   | SHA-2 チェックサムを計算する                             |
| [<a href="https://en.wikipedia.org/wiki/SM3_(hash_function)">`SM3()`</a>](https://en.wikipedia.org/wiki/SM3_(hash_function))                                                                                                                                | SM3 チェックサムを計算します (現在、MySQL はこの機能をサポートしていません)。 |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_aes-decrypt">`AES_DECRYPT()`</a>](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_aes-decrypt)                                              | AES を使用して復号化する                                |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_aes-encrypt">`AES_ENCRYPT()`</a>](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_aes-encrypt)                                              | AES を使用して暗号化する                                |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_compress">`COMPRESS()`</a>](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_compress)                                                       | 結果をバイナリ文字列として返す                               |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_uncompress">`UNCOMPRESS()`</a>](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_uncompress)                                                 | 圧縮された文字列を解凍する                                 |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_uncompressed-length">`UNCOMPRESSED_LENGTH()`</a>](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_uncompressed-length)                      | 圧縮前の文字列の長さを返します。                              |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_validate-password-strength">`VALIDATE_PASSWORD_STRENGTH()`</a>](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_validate-password-strength) | パスワードの強度を検証する                                 |

## 関連するシステム変数 {#related-system-variables}

`block_encryption_mode`変数は、 `AES_ENCRYPT()`と`AES_DECRYPT()`に使用される暗号化モードを設定します。

## サポートされていない関数 {#unsupported-functions}

-   `DES_DECRYPT()` 、 `DES_ENCRYPT()` 、 `OLD_PASSWORD()` 、 `ENCRYPT()` : これらの関数はMySQL 5.7で非推奨となり、8.0 で削除されました。
-   MySQL Enterprise でのみ使用できる機能[<a href="https://github.com/pingcap/tidb/issues/2632">問題 #2632</a>](https://github.com/pingcap/tidb/issues/2632) 。
