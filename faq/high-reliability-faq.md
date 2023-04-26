---
title: High Reliability FAQs
summary: Learn about the FAQs related to high reliability of TiDB.
---

# 高信頼性に関するよくある質問 {#high-reliability-faqs}

このドキュメントは、TiDB の高信頼性に関する FAQ をまとめたものです。

## TiDB はデータ暗号化をサポートしていますか? {#does-tidb-support-data-encryption}

はい。ネットワーク トラフィック内のデータを暗号化するには、 [TiDB クライアントとサーバー間の TLS を有効にする](/enable-tls-between-clients-and-servers.md)ことができます。storageエンジンでデータを暗号化するには、 [透過的なデータ暗号化 (TDE)](/encryption-at-rest.md)有効にします。

## TiDB は、サーバーの MySQL バージョン文字列を、セキュリティ脆弱性スキャン ツールで必要とされる特定のものに変更することをサポートしていますか? {#does-tidb-support-modifying-the-mysql-version-string-of-the-server-to-a-specific-one-that-is-required-by-the-security-vulnerability-scanning-tool}

-   v3.0.8 以降、TiDB は構成ファイルの[`server-version`](/tidb-configuration-file.md#server-version)を変更することでサーバーのバージョン文字列を変更することをサポートしています。

-   v4.0 以降、 TiUPを使用して TiDB をデプロイする場合、 `tiup cluster edit-config <cluster-name>`を実行して次のセクションを編集することにより、適切なバージョン文字列を指定することもできます。

    ```
    server_configs:
      tidb:
        server-version: 'YOUR_VERSION_STRING'
    ```

    次に、 `tiup cluster reload <cluster-name> -R tidb`コマンドを使用して前の変更を有効にし、セキュリティ脆弱性スキャンの失敗を回避します。

## TiDB はどの認証プロトコルをサポートしていますか?プロセスは何ですか？ {#what-authentication-protocols-does-tidb-support-what-s-the-process}

MySQL と同様に、TiDB はユーザー ログイン認証とパスワード処理のために SASL プロトコルをサポートします。

クライアントが TiDB に接続すると、チャレンジ/レスポンス認証モードが開始されます。プロセスは次のとおりです。

1.  クライアントがサーバーに接続します。
2.  サーバーはランダムな文字列チャレンジをクライアントに送信します。
3.  クライアントは、ユーザー名と応答をサーバーに送信します。
4.  サーバーは応答を検証します。

## ユーザーのパスワードと権限を変更するには? {#how-to-modify-the-user-password-and-privilege}

TiDB でユーザー パスワードを変更するには、他のノードのパスワードがタイムリーに更新されないという状態につながる可能性がある`UPDATE mysql.user`ではなく、 `ALTER USER` (たとえば`ALTER USER 'test'@'localhost' IDENTIFIED BY 'mypass';` ) を使用することをお勧めします。

ユーザーのパスワードと権限を変更する場合は、公式の標準ステートメントを使用することをお勧めします。詳細については、 [TiDB ユーザー アカウント管理](/user-account-management.md)を参照してください。
