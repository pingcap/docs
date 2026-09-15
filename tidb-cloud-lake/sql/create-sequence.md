---
title: CREATE SEQUENCE
summary: 在 {{{ .lake }}} 中创建一个新的序列。
---

# CREATE SEQUENCE

在 {{{ .lake }}} 中创建一个新的序列。

序列是一种能够自动生成唯一数字标识符的对象，通常用于为表中的行分配不同的值（例如用户 ID）。虽然序列能够保证值的唯一性，但**不能**保证连续性（即，可能会出现间隔）。

## 语法 {#syntax}

```sql
CREATE [ OR REPLACE ] SEQUENCE [ IF NOT EXISTS ] <sequence>
    [ START [ = ] <start_value> ]
    [ INCREMENT [ = ] <increment_value> ]
```

| 参数 | 描述 | 默认值 |
|---------------------|-------------------------------------------------------|---------|
| `<sequence>`        | 要创建的序列名称。               | -       |
| `START`             | 序列的初始值。                    | 1       |
| `INCREMENT`         | 每次调用 NEXTVAL 时的增量值。         | 1       |

## 访问控制要求 {#access-control-requirements}

| 权限 | 对象类型 | 描述 |
|:----------------|:------------|:----------------------|
| CREATE SEQUENCE | Global      | 创建序列。 |

要创建序列，执行该操作的用户或 [current_role](/tidb-cloud-lake/guides/roles.md) 必须具有 CREATE SEQUENCE [权限](/tidb-cloud-lake/guides/privileges.md)。

> **注意：**
>
> `enable_experimental_sequence_rbac_check` 设置控制序列级别的访问控制。该设置默认禁用。
> 创建序列时仅要求用户具有 superuser 权限，会跳过详细的 RBAC 检查。
> 启用后，在创建序列期间会强制执行细粒度的权限验证。
>
> 这是一个实验特性，未来可能会默认启用。

## 示例 {#examples}

### 基本序列 {#basic-sequence}

使用默认设置创建一个序列（从 1 开始，每次递增 1）：

```sql
CREATE SEQUENCE staff_id_seq;

CREATE TABLE staff (
    staff_id INT,
    name VARCHAR(50),
    department VARCHAR(50)
);

INSERT INTO staff (staff_id, name, department)
VALUES (NEXTVAL(staff_id_seq), 'John Doe', 'HR');

INSERT INTO staff (staff_id, name, department)
VALUES (NEXTVAL(staff_id_seq), 'Jane Smith', 'Finance');

SELECT * FROM staff;

┌───────────────────────────────────────────────────────┐
│     staff_id    │       name       │    department    │
├─────────────────┼──────────────────┼──────────────────┤
│               2 │ Jane Smith       │ Finance          │
│               1 │ John Doe         │ HR               │
└───────────────────────────────────────────────────────┘
```

### 自定义起始值和增量 {#custom-start-and-increment}

创建一个从 1000 开始、每次递增 10 的序列：

```sql
CREATE SEQUENCE order_id_seq START = 1000 INCREMENT = 10;

CREATE TABLE orders (
    order_id BIGINT,
    order_name VARCHAR(100)
);

INSERT INTO orders (order_id, order_name)
VALUES (NEXTVAL(order_id_seq), 'Order A');

INSERT INTO orders (order_id, order_name)
VALUES (NEXTVAL(order_id_seq), 'Order B');

SELECT * FROM orders;

┌──────────────────────────────────┐
│    order_id    │    order_name   │
├────────────────┼─────────────────┤
│           1000 │ Order A         │
│           1010 │ Order B         │
└──────────────────────────────────┘
```