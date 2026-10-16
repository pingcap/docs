---
title: PostgreSQL 高级 SQL
summary: 了解 PostgreSQL 兼容的 TiDB Cloud Starter 中的 PL/pgSQL、触发器、序列、自定义类型和排序规则。
---

# PostgreSQL 高级 SQL

PostgreSQL 兼容的 {{{ .starter }}} 支持常见的 PostgreSQL 高级特性，包括 PL/pgSQL 函数、触发器、序列、枚举和复合类型，以及自定义排序规则。

## PL/pgSQL {#pl-pgsql}

PostgreSQL 兼容的 {{{ .starter }}} 支持 PL/pgSQL 函数和 `DO` 代码块，以及常用的过程式构造。

支持的构造包括：

- 变量声明和赋值
- `IF`、`ELSIF` 和 `ELSE`
- `CASE`
- `FOR` 循环
- `LOOP`
- `EXIT` 和 `CONTINUE`
- `PERFORM`
- `SELECT ... INTO`
- `INSERT ... RETURNING ... INTO`、`UPDATE ... RETURNING ... INTO` 和 `DELETE ... RETURNING ... INTO`
- `RAISE`
- `RETURN`
- 动态 `EXECUTE`，包括 `INTO` 和 `USING`

### 准备示例表 {#prepare-sample-tables}

本文档中的一些示例会使用 `users`、`orders` 和 `audit_log` 表。在运行这些示例之前，请先创建以下示例表：

```sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    active BOOLEAN DEFAULT TRUE
);

CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    item TEXT NOT NULL
);

CREATE TABLE audit_log (
    table_name TEXT,
    action TEXT,
    changed_at TIMESTAMPTZ
);
```

### 创建 PL/pgSQL 函数 {#create-a-pl-pgsql-function}

例如：

```sql
CREATE FUNCTION increment_value(val INTEGER)
RETURNS INTEGER AS $$
BEGIN
    RETURN val + 1;
END;
$$ LANGUAGE plpgsql;
```

调用该函数：

```sql
SELECT increment_value(41);
```

### 声明变量 {#declare-variables}

使用 `DECLARE` 代码块：

```sql
CREATE FUNCTION user_count()
RETURNS INTEGER AS $$
DECLARE
    n INTEGER;
BEGIN
    SELECT count(*) INTO n
    FROM users;

    RETURN n;
END;
$$ LANGUAGE plpgsql;
```

声明可以跨多行书写。

### 条件逻辑 {#conditional-logic}

使用 `IF`、`ELSIF` 和 `ELSE`：

```sql
CREATE FUNCTION size_label(n INTEGER)
RETURNS TEXT AS $$
BEGIN
    IF n > 100 THEN
        RETURN 'large';
    ELSIF n > 10 THEN
        RETURN 'medium';
    ELSE
        RETURN 'small';
    END IF;
END;
$$ LANGUAGE plpgsql;
```

也支持 `CASE` 语句：

```sql
CREATE FUNCTION category_label(n INTEGER)
RETURNS TEXT AS $$
BEGIN
    CASE
        WHEN n > 100 THEN RETURN 'large';
        WHEN n > 10 THEN RETURN 'medium';
        ELSE RETURN 'small';
    END CASE;
END;
$$ LANGUAGE plpgsql;
```

> **Note:**
>
> 在 PL/pgSQL 的 `CASE` 语句中，请始终包含 `ELSE` 分支。如果没有任何分支匹配且省略了 `ELSE`，PostgreSQL 兼容的 {{{ .starter }}} 可能会直接继续执行，而不是像 PostgreSQL 那样抛出 `CASE_NOT_FOUND` 错误。

### `SELECT ... INTO` {#select-into}

将查询结果赋值给变量：

```sql
CREATE FUNCTION active_user_count()
RETURNS INTEGER AS $$
DECLARE
    n INTEGER;
BEGIN
    SELECT count(*) INTO n
    FROM users
    WHERE active = true;

    RETURN n;
END;
$$ LANGUAGE plpgsql;
```

### `RETURNING ... INTO` {#returning-into}

捕获 DML 返回的值：

```sql
CREATE FUNCTION create_order(p_item TEXT)
RETURNS BIGINT AS $$
DECLARE
    new_id BIGINT;
BEGIN
    INSERT INTO orders (item)
    VALUES (p_item)
    RETURNING id INTO new_id;

    RETURN new_id;
END;
$$ LANGUAGE plpgsql;
```

`RETURNING ... INTO` 支持与 `INSERT`、`UPDATE` 和 `DELETE` 一起使用。

### 动态 SQL {#dynamic-sql}

使用 `EXECUTE` 实现动态 SQL：

```sql
CREATE FUNCTION count_rows(table_name TEXT)
RETURNS INTEGER AS $$
DECLARE
    n INTEGER;
BEGIN
    EXECUTE
        'SELECT count(*) FROM ' || quote_ident(table_name)
        INTO n;

    RETURN n;
END;
$$ LANGUAGE plpgsql;
```

使用 `USING` 对动态 SQL 进行参数化：

```sql
CREATE FUNCTION double_it(p INTEGER)
RETURNS INTEGER AS $$
DECLARE
    result INTEGER;
BEGIN
    EXECUTE 'SELECT $1 * 2'
        INTO result
        USING p;

    RETURN result;
END;
$$ LANGUAGE plpgsql;
```

### 异常处理 {#exception-handling}

`DO` 块支持 `BEGIN ... EXCEPTION` 代码块：

```sql
DO $$
BEGIN
    EXECUTE 'CREATE TABLE audit_snapshot(id INTEGER)';
EXCEPTION
    WHEN others THEN
        RAISE NOTICE 'setup skipped';
END;
$$;
```

异常处理程序遵循 PostgreSQL 对受保护代码块的回滚语义。

`CREATE FUNCTION` 函数体内不支持 `BEGIN ... EXCEPTION` 和嵌套的过程式 `BEGIN ... END` 代码块。它们仅在 `DO` 块中受支持。

### PL/pgSQL 限制 {#pl-pgsql-limitations}

以下结构不受支持：

- `WHILE` 循环
- `FOREACH` 循环
- Cursor 操作
- `REFCURSOR`

## 触发器 {#triggers}

支持以下操作的行级 `BEFORE` 和 `AFTER` 触发器：

- `INSERT`
- `UPDATE`
- `DELETE`

### 创建 AFTER 触发器 {#create-an-after-trigger}

创建触发器函数：

```sql
CREATE FUNCTION audit_trigger()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_log (table_name, action, changed_at)
    VALUES (TG_TABLE_NAME, TG_OP, NOW());

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

创建触发器：

```sql
CREATE TRIGGER users_audit
AFTER INSERT OR UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION audit_trigger();
```

### 创建 BEFORE 触发器 {#create-a-before-trigger}

`BEFORE` 触发器可以在 `INSERT` 或 `UPDATE` 事件中修改 `NEW`，通过 `RETURN NULL` 跳过一行，或通过 `RAISE EXCEPTION` 拒绝一行。

例如：

```sql
CREATE FUNCTION normalize_user_name()
RETURNS TRIGGER AS $$
BEGIN
    NEW.name := upper(NEW.name);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

```sql
CREATE TRIGGER normalize_user
BEFORE INSERT OR UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION normalize_user_name();
```

拒绝无效输入：

```sql
CREATE FUNCTION reject_invalid_user()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.name = 'INVALID' THEN
        RAISE EXCEPTION 'invalid user name';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

### BEFORE 触发器限制 {#before-trigger-limitations}

`BEFORE` 触发器函数支持常见的校验和重写逻辑，包括：

- `IF` / `ELSIF` / `ELSE`
- `RAISE`
- `PERFORM`
- 已声明的局部变量
- `SELECT ... INTO`
- 对 `NEW` 的赋值
- 对其他表执行 DML
- `TG_OP` 和 `TG_TABLE_NAME`

`BEFORE` 触发器函数中不支持以下过程式结构：

- `FOR` 循环
- 裸 `LOOP`
- `WHILE` 和 `FOREACH`
- PL/pgSQL `CASE` 语句
- 动态 `EXECUTE`
- 异常处理程序
- 嵌套过程式代码块

不过，`CASE` 表达式（例如 `NEW.status := CASE WHEN ... END`）仍可用于赋值。

### AFTER 触发器格式要求 {#after-trigger-formatting}

在 `AFTER` 触发器函数中，请将单独的 `RETURN NEW;` 或 `RETURN OLD;` 放在独立的一行。

例如：

```sql
BEGIN
    INSERT INTO audit_log (action) VALUES (TG_OP);
    RETURN NEW;
END;
```

如果函数体采用紧凑写法，将 `RETURN NEW;` 或 `RETURN OLD;` 与其他语句放在同一行，可能会在运行时失败。

### 语句级触发器 {#statement-level-triggers}

可以接受 `FOR EACH STATEMENT` 语法，但当前它执行的是逐行行为，而不是 PostgreSQL 的语句级行为。

为获得可预测的行为，请显式使用 `FOR EACH ROW`。

### 删除触发器 {#drop-a-trigger}

删除触发器时使用 `IF EXISTS`：

```sql
DROP TRIGGER IF EXISTS users_audit ON users;
```

## 序列 {#sequences}

创建并使用序列：

```sql
CREATE SEQUENCE order_seq
START WITH 1000
INCREMENT BY 1;

SELECT nextval('order_seq');
SELECT currval('order_seq');
SELECT lastval();
SELECT setval('order_seq', 2000);
```

删除序列：

```sql
DROP SEQUENCE order_seq;
```

创建序列时可以指定以下选项：

- `START`
- `INCREMENT`
- `MINVALUE`
- `MAXVALUE`
- `CACHE`
- `CYCLE`

`ALTER SEQUENCE` 支持 `OWNER TO` 和 `OWNED BY` 等所有权操作。不支持在创建后更改序列生成选项。当你需要重新定位序列时，请使用 `setval()`。

## 自定义类型 {#custom-types}

### Enum 类型 {#enum-types}

创建 Enum 类型：

```sql
CREATE TYPE mood AS ENUM (
    'happy',
    'sad',
    'neutral'
);
```

添加一个 Enum 值：

```sql
ALTER TYPE mood
ADD VALUE 'excited';
```

在表中使用该类型：

```sql
CREATE TABLE user_mood (
    id BIGSERIAL PRIMARY KEY,
    mood mood
);
```

> **Note:**
>
> Enum 的比较和排序使用的是 Enum 标签文本，而不是 PostgreSQL 中的声明顺序。相等比较、`IN` 和分组不受影响。如果应用逻辑依赖 Enum 顺序，请使用显式的排名表达式。

例如：

```sql
SELECT mood
FROM user_mood
ORDER BY array_position(
    ARRAY['sad', 'neutral', 'happy', 'excited'],
    mood::text
);
```

### 复合类型 {#composite-types}

创建复合类型：

```sql
CREATE TYPE address AS (
    street TEXT,
    city TEXT,
    zip TEXT
);
```

## 排序规则 {#collations}

创建排序规则：

```sql
CREATE COLLATION my_collation (
    LOCALE = 'en_US.utf8'
);
```

在列上使用它：

```sql
CREATE TABLE names (
    value TEXT COLLATE my_collation
);
```

删除排序规则：

```sql
DROP COLLATION my_collation;
```

自定义排序规则会改变普通文本比较和 `ORDER BY` 的行为。`LOCALE` 值用于选择排序规则。例如，`en_US.utf8` 会将 `å`、`ä` 和 `ö` 排在 `z` 之前，而 `sv_SE.utf8` 会将这些字母排在 `z` 之后。

### 排序规则限制 {#collation-limitations}

请注意以下差异：

- 未显式指定自定义排序规则的文本使用按字节排序。
- 排序规则不会应用于聚合函数内部的 `ORDER BY`。
- 排序规则不会应用于窗口函数的 `ORDER BY`。
- 可以使用自定义排序规则，但不会列在 `pg_collation` 中。