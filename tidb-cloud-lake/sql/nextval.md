---
title: NEXTVAL
summary: 从序列中获取下一个值。
---

# NEXTVAL

从序列中获取下一个值。

## 语法 {#syntax}

```sql
NEXTVAL(<sequence_name>)
```

## 返回类型 {#return-type}

整数型。

## 访问控制要求 {#access-control-requirements}

| 权限 | 对象类型 | 描述 |
|:----------------|:------------|:-------------------|
| ACCESS SEQUENCE | SEQUENCE    | 访问序列。 |

要访问序列，执行该操作的用户或其角色必须具有 ACCESS SEQUENCE [权限](/tidb-cloud-lake/guides/privileges.md)。

> **注意：**
>
> `enable_experimental_sequence_rbac_check` 设置控制序列级别的访问控制。该设置默认禁用。
> 创建序列时仅要求用户具有 superuser 权限，会绕过详细的 RBAC 检查。
> 启用后，在创建序列期间会强制执行细粒度的权限验证。
>
> 这是一个实验特性，未来可能会默认启用。

## 示例 {#examples}

以下示例演示了 NEXTVAL 函数如何与序列配合使用：

```sql
CREATE SEQUENCE my_seq;

SELECT
  NEXTVAL(my_seq),
  NEXTVAL(my_seq),
  NEXTVAL(my_seq);

┌─────────────────────────────────────────────────────┐
│ nextval(my_seq) │ nextval(my_seq) │ nextval(my_seq) │
├─────────────────┼─────────────────┼─────────────────┤
│               1 │               2 │               3 │
└─────────────────────────────────────────────────────┘
```

以下示例展示了如何使用序列和 NEXTVAL 函数为表中的行自动生成并分配唯一标识符。

```sql
-- Create a new sequence named staff_id_seq
CREATE SEQUENCE staff_id_seq;

-- Create a new table named staff with an auto-generated staff_id
CREATE TABLE staff (
    staff_id INT DEFAULT NEXTVAL(staff_id_seq),
    name VARCHAR(50),
    department VARCHAR(50)
);

--  Insert a new staff member with an auto-generated staff_id into the staff table
INSERT INTO staff (name, department)
VALUES ('John Doe', 'HR');

-- Insert another row
INSERT INTO staff (name, department)
VALUES ('Jane Smith', 'Finance');

SELECT * FROM staff;

┌───────────────────────────────────────────────────────┐
│     staff_id    │       name       │    department    │
├─────────────────┼──────────────────┼──────────────────┤
│               3 │ Jane Smith       │ Finance          │
│               2 │ John Doe         │ HR               │
└───────────────────────────────────────────────────────┘
```