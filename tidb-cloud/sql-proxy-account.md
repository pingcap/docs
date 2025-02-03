---
title: SQL Proxy Account
summary: TiDB Cloudの SQL プロキシ アカウントについて学習します。
---

# SQL プロキシ アカウント {#sql-proxy-account}

SQL プロキシ アカウントは、 TiDB Cloudユーザーに代わって[SQL エディター](/tidb-cloud/explore-data-with-chat2query.md)または[データサービス](https://docs.pingcap.com/tidbcloud/api/v1beta1/dataservice)介してデータベースにアクセスするためにTiDB Cloudによって自動的に作成される SQL ユーザー アカウントです。たとえば、 `testuser@pingcap.com` TiDB Cloudユーザー アカウントで、 `3jhEcSimm7keKP8.testuser._41mqK6H4`対応する SQL プロキシ アカウントです。

SQL プロキシ アカウントは、 TiDB Cloudのデータベースにアクセスするための安全なトークンベースの認証メカニズムを提供します。従来のユーザー名とパスワードの資格情報が不要になることで、SQL プロキシ アカウントはセキュリティを強化し、アクセス管理を簡素化します。

SQL プロキシ アカウントの主な利点は次のとおりです。

-   強化されたセキュリティ: JWT トークンを使用することで、静的資格情報に関連するリスクを軽減します。
-   合理化されたアクセス: SQL エディターとデータ サービスへのアクセスを具体的に制限し、正確な制御を保証します。
-   管理の容易さ: TiDB Cloudを使用する開発者と管理者の認証を簡素化します。

## SQLプロキシアカウントを特定する {#identify-the-sql-proxy-account}

特定の SQL アカウントが SQL プロキシ アカウントであるかどうかを識別する場合は、次の手順を実行します。

1.  `mysql.user`表を調べます。

    ```sql
    USE mysql;
    SELECT user FROM user WHERE plugin = 'tidb_auth_token';
    ```

2.  SQL アカウントの権限付与を確認します。 `role_admin` 、 `role_readonly` 、 `role_readwrite`などのロールがリストされている場合は、SQL プロキシ アカウントです。

    ```sql
    SHOW GRANTS for 'username';
    ```

## SQL プロキシ アカウントの作成方法 {#how-the-sql-proxy-account-is-created}

SQL プロキシ アカウントは、クラスター内で権限を持つロールが付与されているTiDB Cloudユーザーに対して、 TiDB Cloudクラスターの初期化中に自動的に作成されます。

## SQL プロキシ アカウントを削除する方法 {#how-the-sql-proxy-account-is-deleted}

ユーザーが[組織](/tidb-cloud/manage-user-access.md#remove-an-organization-member)または[プロジェクト](/tidb-cloud/manage-user-access.md#remove-a-project-member)から削除されるか、そのロールがクラスターにアクセスできないロールに変更されると、SQL プロキシ アカウントは自動的に削除されます。

SQL プロキシ アカウントを手動で削除した場合、ユーザーが次回TiDB Cloudコンソールにログインしたときに自動的に再作成されることに注意してください。

## SQL プロキシ アカウントのユーザー名 {#sql-proxy-account-username}

SQL プロキシ アカウントのユーザー名は、 TiDB Cloud のユーザー名とまったく同じ場合もありますが、まったく同じでない場合もあります。SQL プロキシ アカウントのユーザー名は、 TiDB Cloudユーザーの電子メール アドレスの長さによって決まります。ルールは次のとおりです。

| 環境               | メールの長さ | ユーザー名の形式                                                                             |
| ---------------- | ------ | ------------------------------------------------------------------------------------ |
| TiDB Cloud専用     | 32文字以下 | 完全なメールアドレス                                                                           |
| TiDB Cloud専用     | 32文字   | `prefix($email, 23)_prefix(base58(sha1($email)), 8)`                                 |
| TiDB Cloudサーバーレス | 15文字以下 | `serverless_unique_prefix + "." + email`                                             |
| TiDB Cloudサーバーレス | 15文字   | `serverless_unique_prefix + "." + prefix($email, 6)_prefix(base58(sha1($email)), 8)` |

例:

| 環境               | 電子メールアドレス                             | SQL プロキシ アカウントのユーザー名                 |
| ---------------- | ------------------------------------- | ------------------------------------ |
| TiDB Cloud専用     | `user@pingcap.com`                    | `user@pingcap.com`                   |
| TiDB Cloud専用     | `longemailaddressexample@pingcap.com` | `longemailaddressexample_48k1jwL9`   |
| TiDB Cloudサーバーレス | `u1@pingcap.com`                      | `{user_name_prefix}.u1@pingcap.com`  |
| TiDB Cloudサーバーレス | `longemailaddressexample@pingcap.com` | `{user_name_prefix}.longem_48k1jwL9` |

> **注記：**
>
> 上記の表の`{user_name_prefix}` 、 TiDB Cloud Serverless クラスターを区別するためにTiDB Cloudによって生成された一意のプレフィックスです。詳細については、 TiDB Cloud Serverless クラスターの[ユーザー名プレフィックス](/tidb-cloud/select-cluster-tier.md#user-name-prefix)参照してください。

## SQL プロキシ アカウントのパスワード {#sql-proxy-account-password}

SQL プロキシ アカウントは JWT トークン ベースであるため、これらのアカウントのパスワードを管理する必要はありません。セキュリティ トークンはシステムによって自動的に管理されます。

## SQL プロキシ アカウント ロール {#sql-proxy-account-roles}

SQL プロキシ アカウントのロールは、 TiDB CloudユーザーのIAMロールによって異なります。

-   組織レベル:
    -   組織の所有者: role_admin
    -   組織の請求管理者: 代理アカウントなし
    -   組織閲覧者: プロキシアカウントなし
    -   組織コンソール監査マネージャ: プロキシアカウントなし

-   プロジェクトレベル:
    -   プロジェクトオーナー: role_admin
    -   プロジェクト データ アクセス読み取り/書き込み: role_readwrite
    -   プロジェクト データ アクセス読み取り専用: role_readonly

## SQL プロキシ アカウント アクセス制御 {#sql-proxy-account-access-control}

SQL プロキシ アカウントは JWT トークン ベースであり、データ サービスと SQL エディターからのみアクセスできます。ユーザー名とパスワードを使用して SQL プロキシ アカウントを使用してTiDB Cloudクラスターにアクセスすることはできません。
