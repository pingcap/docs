---
title: Encryption and Compression Functions
summary: Learn about the encryption and compression functions.
---

# 暗号化・圧縮機能 {#encryption-and-compression-functions}

TiDB は、 MySQL 5.7で利用可能な[暗号化および圧縮関数](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html)のほとんどをサポートします。

## 対応関数 {#supported-functions}

| 名前                                                                                                                        | 説明                        |
| :------------------------------------------------------------------------------------------------------------------------ | :------------------------ |
| [`MD5()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_md5)                                 | MD5 チェックサムを計算する           |
| [`PASSWORD()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_password)                       | パスワード文字列を計算して返す           |
| [`RANDOM_BYTES()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_random-bytes)               | ランダムなバイト ベクトルを返す          |
| [`SHA1(), SHA()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_sha1)                        | SHA-1 160 ビット チェックサムを計算する |
| [`SHA2()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_sha2)                               | SHA-2 チェックサムを計算する         |
| [`AES_DECRYPT()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_aes-decrypt)                 | AES を使用して復号化する            |
| [`AES_ENCRYPT()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_aes-encrypt)                 | AES を使用して暗号化する            |
| [`COMPRESS()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_compress)                       | 結果をバイナリ文字列として返す           |
| [`UNCOMPRESS()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_uncompress)                   | 圧縮された文字列を解凍する             |
| [`UNCOMPRESSED_LENGTH()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_uncompressed-length) | 圧縮前の文字列の長さを返す             |

## 関連するシステム変数 {#related-system-variables}

`block_encryption_mode`変数は、 `AES_ENCRYPT()`および`AES_DECRYPT()`に使用される暗号化モードを設定します。

## サポートされていない関数 {#unsupported-functions}

-   `DES_DECRYPT()` 、 `DES_ENCRYPT()` 、 `OLD_PASSWORD()` 、 `ENCRYPT()` : これらの関数はMySQL 5.7で廃止され、8.0 で削除されました。
-   `VALIDATE_PASSWORD_STRENGTH()` .
-   MySQL Enterprise [問題＃2632](https://github.com/pingcap/tidb/issues/2632)でのみ使用できる関数。
