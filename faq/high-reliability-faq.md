---
title: High Reliability FAQs
summary: TiDB の高信頼性に関連する FAQ について説明します。
---

# 高信頼性に関するFAQ {#high-reliability-faqs}

このドキュメントでは、TiDB の高信頼性に関連する FAQ をまとめています。

## TiDB はデータ暗号化をサポートしていますか? {#does-tidb-support-data-encryption}

はい。ネットワークトラフィック内のデータを暗号化するには、 [TiDBクライアントとサーバー間のTLSを有効にする](/enable-tls-between-clients-and-servers.md)有効にします。storageエンジン内のデータを暗号化するには、 [透過的なデータ暗号化（TDE）](/encryption-at-rest.md)有効にします。

## TiDB は、サーバーの MySQL バージョン文字列を、セキュリティ脆弱性スキャン ツールに必要な特定のバージョンに変更することをサポートしていますか? {#does-tidb-support-modifying-the-mysql-version-string-of-the-server-to-a-specific-one-that-is-required-by-the-security-vulnerability-scanning-tool}

-   v3.0.8 以降、TiDB は構成ファイル内の[`server-version`](/tidb-configuration-file.md#server-version)変更することでサーバーのバージョン文字列を変更することをサポートしています。

-   v4.0 以降、 TiUPを使用して TiDB をデプロイする場合は、 `tiup cluster edit-config <cluster-name>`実行して次のセクションを編集することで、適切なバージョン文字列を指定することもできます。

        server_configs:
          tidb:
            server-version: 'YOUR_VERSION_STRING'

    次に、 `tiup cluster reload <cluster-name> -R tidb`コマンドを使用して前述の変更を有効にし、セキュリティ脆弱性スキャンの失敗を回避します。

## TiDB はどのような認証プロトコルをサポートしていますか? プロセスはどのようなものですか? {#what-authentication-protocols-does-tidb-support-what-s-the-process}

MySQL と同様に、TiDB はユーザー ログイン認証とパスワード処理のための SASL プロトコルをサポートしています。

クライアントがTiDBに接続すると、チャレンジレスポンス認証モードが開始されます。プロセスは以下のとおりです。

1.  クライアントはサーバーに接続します。
2.  サーバーはランダムな文字列チャレンジをクライアントに送信します。
3.  クライアントはユーザー名と応答をサーバーに送信します。
4.  サーバーは応答を検証します。

## ユーザーのパスワードと権限を変更するにはどうすればよいですか? {#how-to-modify-the-user-password-and-privilege}

TiDB でユーザー パスワードを変更する場合は、他のノードのパスワードがタイムリーに更新されない可能性がある`UPDATE mysql.user`ではなく、 `ALTER USER` (たとえば、 `ALTER USER 'test'@'localhost' IDENTIFIED BY 'mypass';` ) を使用することをお勧めします。

ユーザーのパスワードと権限を変更する際は、公式の標準ステートメントを使用することをお勧めします。詳細については、 [TiDB ユーザーアカウント管理](/user-account-management.md)参照してください。
