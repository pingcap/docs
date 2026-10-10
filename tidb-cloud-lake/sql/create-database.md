---
title: CREATE DATABASE
summary: データベースを作成します。
---

# CREATE DATABASE

データベースを作成します。

## 構文 {#syntax}

```sql
CREATE [ OR REPLACE ] DATABASE [ IF NOT EXISTS ] <database_name>
    [ OPTIONS (
        DEFAULT_STORAGE_CONNECTION = '<connection_name>',
        DEFAULT_STORAGE_PATH = '<path>'
    ) ]
```

## パラメータ {#parameters}

| パラメータ                    | 説明                                                                                                                                      |
|:-----------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------|
| `DEFAULT_STORAGE_CONNECTION` | このデータベース内のテーブルのデフォルトストレージ接続として使用する、既存の接続（`CREATE CONNECTION` で作成）の名前です。        |
| `DEFAULT_STORAGE_PATH`       | このデータベース内のテーブルのデフォルトストレージパス URI（例: `s3://bucket/path/`）です。末尾は `/` で終わる必要があり、接続のストレージタイプと一致している必要があります。 |

> **Note:**
>
> - `DEFAULT_STORAGE_CONNECTION` と `DEFAULT_STORAGE_PATH` は必ず一緒に指定する必要があります。どちらか一方だけを指定するとエラーになります。
> - 両方のオプションが設定されている場合、{{{ .lake }}} は接続が存在すること、パス URI の形式が正しいこと、およびストレージロケーションにアクセス可能であることを検証します。

## アクセス制御要件 {#access-control-requirements}

| 権限       | オブジェクトタイプ | 説明         |
|:----------------|:------------|:--------------------|
| CREATE DATABASE | Global      | データベースを作成します。 |

データベースを作成するには、操作を実行するユーザーまたは [current_role](/tidb-cloud-lake/guides/roles.md) が CREATE DATABASE [権限](/tidb-cloud-lake/guides/privileges.md) を持っている必要があります。

## 例 {#examples}

### 基本的なデータベースの作成 {#creating-a-basic-database}

次の例では、`test` という名前のデータベースを作成します。

```sql
CREATE DATABASE test;
```

### デフォルトストレージ接続を使用したデータベースの作成 {#creating-a-database-with-a-default-storage-connection}

次の例では、AWS IAM ロールを使用して接続を作成し、その後、この接続をデフォルトストレージとして使用するデータベースを作成します。IAM ロールを使用する方法は、{{{ .lake }}} に認証情報を保存する必要がないため、access keys よりも安全です。

```sql
CREATE CONNECTION my_s3
    STORAGE_TYPE = 's3'
    ROLE_ARN = 'arn:aws:iam::987654321987:role/lake-test';

CREATE DATABASE analytics OPTIONS (
    DEFAULT_STORAGE_CONNECTION = 'my_s3',
    DEFAULT_STORAGE_PATH = 's3://mybucket/analytics/'
);
```

> **Note:**
>
> {{{ .lake }}} で IAM ロールを使用するには、AWS アカウントと {{{ .lake }}} の間に信頼関係を設定する必要があります。詳細な手順については、[AWS IAM Role による認証](/tidb-cloud-lake/guides/authenticate-with-aws-iam-role.md) を参照してください。