---
title: SQL Proxy Account
summary: TiDB Cloudの SQL プロキシ アカウントについて説明します。
---

# SQL プロキシアカウント {#sql-proxy-account}

SQLプロキシアカウントは、 TiDB Cloudによって自動的に作成されるSQLユーザーアカウントで、 TiDB Cloudユーザーに代わって[SQLエディター](/tidb-cloud/explore-data-with-chat2query.md)または[データサービス](https://docs.pingcap.com/tidbcloud/api/v1beta1/dataservice)介してデータベースにアクセスするために作成されます。たとえば、 `testuser@pingcap.com` TiDB Cloudユーザーアカウントで、 `3jhEcSimm7keKP8.testuser._41mqK6H4`それに対応するSQLプロキシアカウントです。

SQLプロキシアカウントは、 TiDB Cloud内のデータベースにアクセスするための安全なトークンベースの認証メカニズムを提供します。従来のユーザー名とパスワードによる認証が不要になるため、SQLプロキシアカウントはセキュリティを強化し、アクセス管理を簡素化します。

SQL プロキシ アカウントの主な利点は次のとおりです。

-   強化されたセキュリティ: JWT トークンを使用することで、静的資格情報に関連するリスクを軽減します。
-   合理化されたアクセス: SQL エディターとデータ サービスへのアクセスを具体的に制限し、正確な制御を保証します。
-   管理の容易さ: TiDB Cloudを使用する開発者と管理者の認証を簡素化します。

## SQLプロキシアカウントを特定する {#identify-the-sql-proxy-account}

特定の SQL アカウントが SQL プロキシ アカウントであるかどうかを識別する場合は、次の手順を実行します。

1.  `mysql.user`テーブルを調べます。

    ```sql
    USE mysql;
    SELECT user FROM user WHERE plugin = 'tidb_auth_token';
    ```

2.  SQLアカウントの権限を確認してください。1、3、5 `role_admin`のロール`role_readonly`リストさ`role_readwrite`ている場合は、SQLプロキシアカウントです。

    ```sql
    SHOW GRANTS for 'username';
    ```

## SQLプロキシアカウントの作成方法 {#how-the-sql-proxy-account-is-created}

SQL プロキシ アカウントは、クラスター内で権限を持つロールが付与されたTiDB Cloud TiDB Cloud Cloud クラスターの初期化中に自動的に作成されます。

## SQLプロキシアカウントを削除する方法 {#how-the-sql-proxy-account-is-deleted}

ユーザーが[組織](/tidb-cloud/manage-user-access.md#remove-an-organization-member)または[プロジェクト](/tidb-cloud/manage-user-access.md#remove-a-project-member)から削除されるか、そのロールがクラスターにアクセスできないロールに変更されると、SQL プロキシ アカウントは自動的に削除されます。

SQL プロキシ アカウントを手動で削除した場合、ユーザーが次回TiDB Cloudコンソールにログインしたときに自動的に再作成されることに注意してください。

## SQLプロキシアカウントのユーザー名 {#sql-proxy-account-username}

SQLプロキシアカウントのユーザー名は、 TiDB Cloudのユーザー名と完全に一致する場合もありますが、完全に一致しない場合もあります。SQLプロキシアカウントのユーザー名は、 TiDB Cloudユーザーのメールアドレスの長さによって決まります。ルールは以下のとおりです。

| 環境               | メールの長さ | ユーザー名の形式                                                                             |
| ---------------- | ------ | ------------------------------------------------------------------------------------ |
| TiDB Cloud専用     | 32文字以下 | 完全なメールアドレス                                                                           |
| TiDB Cloud専用     | 32文字   | `prefix($email, 23)_prefix(base58(sha1($email)), 8)`                                 |
| TiDB Cloudサーバーレス | 15文字以下 | `serverless_unique_prefix + "." + email`                                             |
| TiDB Cloudサーバーレス | 15文字   | `serverless_unique_prefix + "." + prefix($email, 6)_prefix(base58(sha1($email)), 8)` |

例:

| 環境               | 電子メールアドレス                             | SQLプロキシアカウントのユーザー名                   |
| ---------------- | ------------------------------------- | ------------------------------------ |
| TiDB Cloud専用     | `user@pingcap.com`                    | `user@pingcap.com`                   |
| TiDB Cloud専用     | `longemailaddressexample@pingcap.com` | `longemailaddressexample_48k1jwL9`   |
| TiDB Cloudサーバーレス | `u1@pingcap.com`                      | `{user_name_prefix}.u1@pingcap.com`  |
| TiDB Cloudサーバーレス | `longemailaddressexample@pingcap.com` | `{user_name_prefix}.longem_48k1jwL9` |

> **注記：**
>
> 上記の表の`{user_name_prefix}`は、 TiDB Cloud Serverless クラスターを区別するためにTiDB Cloudによって生成される一意のプレフィックスです。詳細については、 TiDB Cloud Serverless クラスターの「 [ユーザー名のプレフィックス](/tidb-cloud/select-cluster-tier.md#user-name-prefix)参照してください。

## SQLプロキシアカウントのパスワード {#sql-proxy-account-password}

SQL プロキシアカウントは JWT トークンベースであるため、これらのアカウントのパスワードを管理する必要はありません。セキュリティトークンはシステムによって自動的に管理されます。

## SQL プロキシ アカウント ロール {#sql-proxy-account-roles}

SQL プロキシ アカウントのロールは、 TiDB CloudユーザーのIAMロールによって異なります。

-   組織レベル:
    -   組織の所有者: role_admin
    -   組織の請求管理者: 代理アカウントなし
    -   組織閲覧者: プロキシアカウントなし
    -   組織コンソール監査マネージャ: プロキシアカウントなし

-   プロジェクトレベル:
    -   プロジェクトオーナー: role_admin
    -   プロジェクトデータアクセスの読み取り/書き込み: role_readwrite
    -   プロジェクトデータアクセス読み取り専用: role_readonly

## SQL プロキシ アカウント アクセス制御 {#sql-proxy-account-access-control}

SQLプロキシアカウントはJWTトークンベースであり、データサービスとSQLエディタからのみアクセスできます。ユーザー名とパスワードを使用してSQLプロキシアカウントを使用してTiDB Cloudクラスターにアクセスすることはできません。
