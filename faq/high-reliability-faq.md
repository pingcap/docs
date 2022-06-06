---
title: High Reliability FAQs
summary: Learn about the FAQs related to high reliability of TiDB.
---

# 信頼性の高いFAQ {#high-reliability-faqs}

このドキュメントは、TiDBの高信頼性に関連するFAQをまとめたものです。

## TiDBは、サーバーのMySQLバージョン文字列をセキュリティ脆弱性スキャンツールで必要とされる特定のバージョン文字列に変更することをサポートしていますか？ {#does-tidb-support-modifying-the-mysql-version-string-of-the-server-to-a-specific-one-that-is-required-by-the-security-vulnerability-scanning-tool}

v3.0.8以降、TiDBは、構成ファイルの[`server-version`](/tidb-configuration-file.md#server-version)を変更することにより、サーバーのバージョン文字列を変更することをサポートしています。 TiUPを使用してTiDBをデプロイする場合、 `tiup cluster edit-config <cluster-name>`を実行して適切なバージョン文字列を指定することもできます。

```
server_configs:
  tidb:
    server-version: 'YOUR_VERSION_STRING'
```

`tiup cluster reload <cluster-name> -R tidb`コマンドを使用して上記の変更を有効にし、セキュリティ脆弱性スキャンの失敗を回避します。

## TiDBはどの認証プロトコルをサポートしていますか？プロセスは何ですか？ {#what-authentication-protocols-does-tidb-support-what-s-the-process}

MySQLと同様に、TiDBはユーザーログイン認証とパスワード処理のためのSASLプロトコルをサポートしています。

クライアントがTiDBに接続すると、チャレンジ/レスポンス認証モードが開始されます。プロセスは次のとおりです。

1.  クライアントはサーバーに接続します。
2.  サーバーはランダムな文字列チャレンジをクライアントに送信します。
3.  クライアントはユーザー名と応答をサーバーに送信します。
4.  サーバーは応答を検証します。

## ユーザーのパスワードと特権を変更するにはどうすればよいですか？ {#how-to-modify-the-user-password-and-privilege}

TiDBでユーザーパスワードを変更するには、 `update mysql.user`ではなく`set password for 'root'@'%' = '0101001';`または`alter`を使用することをお勧めします。これにより、他のノードのパスワードがタイムリーに更新されない可能性があります。

ユーザーのパスワードと特権を変更するときは、公式の標準ステートメントを使用することをお勧めします。詳細については、 [TiDBユーザーアカウント管理](/user-account-management.md)を参照してください。
