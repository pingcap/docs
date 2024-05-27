---
title: Encryption and Compression Functions
summary: 暗号化と圧縮の関数について学びます。
---

# 暗号化と圧縮機能 {#encryption-and-compression-functions}

TiDB は、MySQL 8.0 で利用可能な[暗号化および圧縮関数](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html)のほとんどをサポートしています。

## サポートされている関数 {#supported-functions}

| 名前                                                                                                                                      | 説明                                           |
| :-------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------- |
| [`MD5()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_md5)                                               | MD5チェックサムを計算する                               |
| [`PASSWORD()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_password)                                     | パスワード文字列を計算して返す                              |
| [`RANDOM_BYTES()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_random-bytes)                             | ランダムなバイトベクトルを返す                              |
| [`SHA1(), SHA()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_sha1)                                      | SHA-1 160ビットチェックサムを計算する                      |
| [`SHA2()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_sha2)                                             | SHA-2チェックサムを計算する                             |
| [`SM3()`](https://en.wikipedia.org/wiki/SM3_(hash_function))                                                                            | SM3 チェックサムを計算します (現在、MySQL はこの関数をサポートしていません) |
| [`AES_DECRYPT()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_aes-decrypt)                               | AESを使用して復号化する                                |
| [`AES_ENCRYPT()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_aes-encrypt)                               | AESを使用して暗号化する                                |
| [`COMPRESS()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_compress)                                     | 結果をバイナリ文字列として返す                              |
| [`UNCOMPRESS()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_uncompress)                                 | 圧縮された文字列を解凍する                                |
| [`UNCOMPRESSED_LENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_uncompressed-length)               | 圧縮前の文字列の長さを返す                                |
| [`VALIDATE_PASSWORD_STRENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_validate-password-strength) | パスワードの強度を検証する                                |

## 関連するシステム変数 {#related-system-variables}

[`block_encryption_mode`](/system-variables.md#block_encryption_mode)変数は、 `AES_ENCRYPT()`および`AES_DECRYPT()`に使用される暗号化モードを設定します。

[`validate_password.*`](/system-variables.md)変数は`VALIDATE_PASSWORD_STRENGTH()`機能に影響します。

## サポートされていない関数 {#unsupported-functions}

-   `DES_DECRYPT()` `ENCRYPT()`これらの関数は`DES_ENCRYPT()` `OLD_PASSWORD()`で非推奨となり、8.0 で削除されました。
-   MySQL Enterprise [問題 #2632](https://github.com/pingcap/tidb/issues/2632)でのみ使用可能な関数。

## MySQL 互換性 {#mysql-compatibility}

-   TiDB は`STATEMENT_DIGEST()`および`STATEMENT_DIGEST_TEXT()`関数をサポートしていません。
