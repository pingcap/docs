---
title: SET SECONDARY ROLES
summary: 为当前会话激活所有次要角色。这意味着授予用户的所有次要角色都将处于激活状态，从而扩展用户的权限。有关活动角色和次要角色的更多信息，请参阅 Active Role & Secondary Roles。
---

# SET SECONDARY ROLES

为当前会话激活所有次要角色。这意味着授予用户的所有次要角色都将处于激活状态，从而扩展用户的权限。有关活动角色和次要角色的更多信息，请参阅 [活动角色和次要角色](/tidb-cloud-lake/guides/roles.md#active-role--secondary-roles)。

另请参阅：[SET ROLE](/tidb-cloud-lake/sql/set-role.md)

## 语法 {#syntax}

```sql
SET SECONDARY ROLES { ALL | NONE }
```

| 参数 | 默认值 | 描述 |
|-----------|---------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ALL       | 是     | 为当前会话激活授予用户的所有次要角色，以及活动角色。这使用户能够使用与所有次要角色关联的权限。 |
| NONE      | 否      | 为当前会话停用所有次要角色，这意味着只有活动角色的权限处于激活状态。这会将用户的权限限制为仅由活动角色授予的权限。  |

## 示例 {#examples}

本示例展示了次要角色如何工作，以及如何激活/停用它们。

1. 以用户 root 创建角色。

    首先，创建两个角色：`admin` 和 `analyst`：

    ```sql
    CREATE ROLE admin;
    
    CREATE ROLE analyst;
    ```

2. 授予权限。

    接下来，为每个角色授予一些权限。例如，为 `admin` 角色授予创建数据库的能力，为 `analyst` 角色授予从表中查询数据的能力：

    ```sql
    GRANT CREATE DATABASE ON *.* TO ROLE admin;
    
    GRANT SELECT ON *.* TO ROLE analyst;
    ```

3. 创建用户。

    现在，创建一个用户：

    ```sql
    CREATE USER 'user1' IDENTIFIED BY 'password';
    ```

4. 分配角色。

    将这两个角色都分配给该用户：

    ```sql
    GRANT ROLE admin TO 'user1';
    
    GRANT ROLE analyst TO 'user1';
    ```

5. 设置活动角色。

    现在，以 `user1` 身份登录到 {{{ .lake }}}，然后将活动角色设置为 `analyst`。

    ```sql
    SET ROLE analyst;
    ```

    默认情况下，所有次要角色都会被激活，因此我们可以创建一个新数据库：

    ```sql
    CREATE DATABASE my_db;
    ```

6. 停用次要角色。

活动角色 `analyst` 不具有 CREATE DATABASE 权限。当所有次要角色都被停用时，创建新数据库将失败。

```sql
SET SECONDARY ROLES NONE;

CREATE DATABASE my_db2;
error: APIError: ResponseError with 1063: Permission denied: privilege [CreateDatabase] is required on *.* for user 'user1'@'%' with roles [analyst,public]
```