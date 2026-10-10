---
title: SET SECONDARY ROLES
summary: 現在のセッションですべてのセカンダリロールを有効化します。これにより、ユーザーに付与されたすべてのセカンダリロールが有効になり、ユーザーの権限が拡張されます。アクティブロールとセカンダリロールの詳細については、Active Role & Secondary Roles を参照してください。
---

# SET SECONDARY ROLES

現在のセッションですべてのセカンダリロールを有効化します。これにより、ユーザーに付与されたすべてのセカンダリロールが有効になり、ユーザーの権限が拡張されます。アクティブロールとセカンダリロールの詳細については、[Active Role & Secondary Roles](/tidb-cloud-lake/guides/roles.md#active-role--secondary-roles)を参照してください。

関連情報: [SET ROLE](/tidb-cloud-lake/sql/set-role.md)

## 構文 {#syntax}

```sql
SET SECONDARY ROLES { ALL | NONE }
```

| パラメータ | デフォルト | 説明 |
|-----------|---------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ALL       | Yes     | 現在のセッションで、アクティブロールに加えて、ユーザーに付与されているすべてのセカンダリロールを有効化します。これにより、ユーザーはすべてのセカンダリロールに関連付けられた権限を利用できます。 |
| NONE      | No      | 現在のセッションですべてのセカンダリロールを無効化します。つまり、アクティブロールの権限のみが有効になります。これにより、ユーザーの権限はアクティブロール単独で付与されたものに制限されます。 |

## 例 {#examples}

この例では、セカンダリロールの動作と、それらを有効化/無効化する方法を示します。

1. user root としてロールを作成します。

    まず、`admin` と `analyst` の 2 つのロールを作成します。

    ```sql
    CREATE ROLE admin;
    
    CREATE ROLE analyst;
    ```

2. 権限を付与します。

    次に、各ロールにいくつかの権限を付与します。たとえば、`admin` ロールにはデータベースを作成する権限を、`analyst` ロールにはテーブルに対して select する権限を付与します。

    ```sql
    GRANT CREATE DATABASE ON *.* TO ROLE admin;
    
    GRANT SELECT ON *.* TO ROLE analyst;
    ```

3. ユーザーを作成します。

    次に、ユーザーを作成します。

    ```sql
    CREATE USER 'user1' IDENTIFIED BY 'password';
    ```

4. ロールを割り当てます。

    両方のロールをユーザーに割り当てます。

    ```sql
    GRANT ROLE admin TO 'user1';
    
    GRANT ROLE analyst TO 'user1';
    ```

5. アクティブロールを設定します。

    ここで、`user1` として {{{ .lake }}} にログインし、アクティブロールを `analyst` に設定します。

    ```sql
    SET ROLE analyst;
    ```

    デフォルトではすべてのセカンダリロールが有効化されているため、新しいデータベースを作成できます。

    ```sql
    CREATE DATABASE my_db;
    ```

6. セカンダリロールを無効化します。

アクティブロール `analyst` には CREATE DATABASE 権限がありません。すべてのセカンダリロールを無効化すると、新しいデータベースの作成は失敗します。

```sql
SET SECONDARY ROLES NONE;

CREATE DATABASE my_db2;
error: APIError: ResponseError with 1063: Permission denied: privilege [CreateDatabase] is required on *.* for user 'user1'@'%' with roles [analyst,public]
```