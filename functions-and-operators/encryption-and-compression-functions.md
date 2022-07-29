---
title: Encryption and Compression Functions
summary: Learn about the encryption and compression functions.
---

# 暗号化および圧縮機能 {#encryption-and-compression-functions}

TiDBは、MySQL5.7で利用可能な[暗号化および圧縮関数](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html)のほとんどをサポートしMySQL 5.7。

## サポートされている関数 {#supported-functions}

| 名前                                                                                                                                                 | 説明                          |
| :------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------- |
| [`MD5()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_md5)                                                          | MD5チェックサムを計算する              |
| [`PASSWORD()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_password)                                                | パスワード文字列を計算して返す             |
| [`RANDOM_BYTES()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_random-bytes)                                        | ランダムなバイトベクトルを返す             |
| [`SHA1(), SHA()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_sha1)                                                 | SHA-1160ビットチェックサムを計算します     |
| [`SHA2()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_sha2)                                                        | SHA-2チェックサムを計算する            |
| [`AES_DECRYPT()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_aes-decrypt)                                          | AESを使用して復号化                 |
| [`AES_ENCRYPT()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_aes-encrypt)                                          | AESを使用して暗号化する               |
| [`COMPRESS()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_compress)                                                | 結果をバイナリ文字列として返します           |
| [`UNCOMPRESS()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_uncompress)                                            | 圧縮された文字列を解凍します              |
| [`UNCOMPRESSED_LENGTH()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_uncompressed-length)                          | 圧縮前の文字列の長さを返す               |
| [`CREATE_ASYMMETRIC_PRIV_KEY()`](https://dev.mysql.com/doc/refman/5.7/en/enterprise-encryption-functions.html#function_create-asymmetric-priv-key) | 秘密鍵を作成する                    |
| [`CREATE_ASYMMETRIC_PUB_KEY()`](https://dev.mysql.com/doc/refman/5.7/en/enterprise-encryption-functions.html#function_create-asymmetric-pub-key)   | 公開鍵を作成する                    |
| [`CREATE_DH_PARAMETERS()`](https://dev.mysql.com/doc/refman/5.7/en/enterprise-encryption-functions.html#function_create-dh-parameters)             | 共有DHシークレットを生成する             |
| [`CREATE_DIGEST()`](https://dev.mysql.com/doc/refman/5.7/en/enterprise-encryption-functions.html#function_create-digest)                           | 文字列からダイジェストを生成する            |
| [`ASYMMETRIC_DECRYPT()`](https://dev.mysql.com/doc/refman/5.7/en/enterprise-encryption-functions.html#function_asymmetric-decrypt)                 | 秘密鍵または公開鍵を使用して暗号文を復号化する     |
| [`ASYMMETRIC_DERIVE()`](https://dev.mysql.com/doc/refman/5.7/en/enterprise-encryption-functions.html#function_asymmetric-derive)                   | 非対称鍵から対称鍵を導出する              |
| [`ASYMMETRIC_ENCRYPT()`](https://dev.mysql.com/doc/refman/5.7/en/enterprise-encryption-functions.html#function_asymmetric-encrypt)                 | 秘密鍵または公開鍵を使用してクリアテキストを暗号化する |
| [`ASYMMETRIC_SIGN()`](https://dev.mysql.com/doc/refman/5.7/en/enterprise-encryption-functions.html#function_asymmetric-sign)                       | ダイジェストから署名を生成する             |
| [`ASYMMETRIC_VERIFY()`](https://dev.mysql.com/doc/refman/5.7/en/enterprise-encryption-functions.html#function_asymmetric-verify)                   | 署名がダイジェストと一致することを確認します      |

## 関連するシステム変数 {#related-system-variables}

`block_encryption_mode`変数は、 `AES_ENCRYPT()`と`AES_DECRYPT()`に使用される暗号化モードを設定します。

## サポートされていない関数 {#unsupported-functions}

-   `DES_DECRYPT()` ：これらの関数は`ENCRYPT()` `DES_ENCRYPT()`で非推奨にMySQL 5.7、 `OLD_PASSWORD()`で削除されました。
-   `VALIDATE_PASSWORD_STRENGTH()`
-   [問題＃2632](https://github.com/pingcap/tidb/issues/2632)でのみ使用可能な機能
