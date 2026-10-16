---
title: PostgreSQL Advanced SQL
summary: PostgreSQL互換のTiDB Cloud StarterにおけるPL/pgSQL、トリガー、シーケンス、カスタム型、照合順序について学びます。
---

# PostgreSQL Advanced SQL

PostgreSQL互換の{{{ .starter }}}は、PL/pgSQL 関数、トリガー、シーケンス、enum 型および複合型、カスタム照合順序など、一般的な高度な PostgreSQL 機能をサポートしています。

## PL/pgSQL {#pl-pgsql}

PostgreSQL互換の{{{ .starter }}}は、一般的によく使われる手続き構文を備えた PL/pgSQL 関数と `DO` ブロックをサポートしています。

サポートされる構文は次のとおりです。

- 変数宣言と代入
- `IF`、`ELSIF`、`ELSE`
- `CASE`
- `FOR` ループ
- `LOOP`
- `EXIT` と `CONTINUE`
- `PERFORM`
- `SELECT ... INTO`
- `INSERT ... RETURNING ... INTO`、`UPDATE ... RETURNING ... INTO`、`DELETE ... RETURNING ... INTO`
- `RAISE`
- `RETURN`
- `INTO` と `USING` を含む動的 `EXECUTE`

### サンプルテーブルを準備する {#prepare-sample-tables}

このドキュメント内の一部の例では、`users`、`orders`、`audit_log` テーブルを使用します。これらの例を実行する前に、次のサンプルテーブルを作成してください。

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

### PL/pgSQL 関数を作成する {#create-a-pl-pgsql-function}

例:

```sql
CREATE FUNCTION increment_value(val INTEGER)
RETURNS INTEGER AS $$
BEGIN
    RETURN val + 1;
END;
$$ LANGUAGE plpgsql;
```

関数を呼び出します。

```sql
SELECT increment_value(41);
```

### 変数を宣言する {#declare-variables}

`DECLARE` ブロックを使用します。

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

宣言は複数行にまたがることができます。

### 条件分岐 {#conditional-logic}

`IF`、`ELSIF`、`ELSE` を使用します。

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

`CASE` 文もサポートされています。

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
> PL/pgSQL の `CASE` 文では、必ず `ELSE` 分岐を含めてください。一致する分岐がなく、`ELSE` を省略した場合、PostgreSQL互換の{{{ .starter }}}では PostgreSQL の `CASE_NOT_FOUND` エラーを返さずに、そのまま処理が継続されることがあります。

### `SELECT ... INTO` {#select-into}

クエリ結果を変数に代入します。

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

DML によって返された値を取得します。

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

`RETURNING ... INTO` は `INSERT`、`UPDATE`、`DELETE` でサポートされています。

### Dynamic SQL {#dynamic-sql}

動的 SQL には `EXECUTE` を使用します。

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

`USING` を使って動的 SQL をパラメータ化します。

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

### Exception handling {#exception-handling}

`DO` ブロックでは `BEGIN ... EXCEPTION` ブロックがサポートされています。

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

例外ハンドラは、保護対象ブロックに対して PostgreSQL のロールバックセマンティクスに従います。

`BEGIN ... EXCEPTION` とネストされた手続き型の `BEGIN ... END` ブロックは、`CREATE FUNCTION` 本文内ではサポートされていません。これらは `DO` ブロックでのみサポートされます。

### PL/pgSQL limitations {#pl-pgsql-limitations}

以下の構文はサポートされていません。

- `WHILE` ループ
- `FOREACH` ループ
- カーソル操作
- `REFCURSOR`

## Triggers {#triggers}

行レベルの `BEFORE` トリガーと `AFTER` トリガーは、以下に対してサポートされています。

- `INSERT`
- `UPDATE`
- `DELETE`

### Create an AFTER trigger {#create-an-after-trigger}

トリガー関数を作成します。

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

トリガーを作成します。

```sql
CREATE TRIGGER users_audit
AFTER INSERT OR UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION audit_trigger();
```

### Create a BEFORE trigger {#create-a-before-trigger}

`BEFORE` トリガーは、`INSERT` または `UPDATE` イベントに対して `NEW` を変更したり、`RETURN NULL` で行をスキップしたり、`RAISE EXCEPTION` で行を拒否したりできます。

例:

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

無効な入力を拒否します。

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

### BEFORE trigger limitations {#before-trigger-limitations}

`BEFORE` トリガー関数では、以下を含む一般的な検証および書き換えロジックがサポートされています。

- `IF` / `ELSIF` / `ELSE`
- `RAISE`
- `PERFORM`
- 宣言されたローカル変数
- `SELECT ... INTO`
- `NEW` への代入
- 他のテーブルに対する DML
- `TG_OP` と `TG_TABLE_NAME`

`BEFORE` トリガー関数では、以下の手続き型構文はサポートされていません。

- `FOR` ループ
- 単独の `LOOP`
- `WHILE` と `FOREACH`
- PL/pgSQL の `CASE` 文
- 動的 `EXECUTE`
- 例外ハンドラ
- ネストされた手続き型ブロック

`NEW.status := CASE WHEN ... END` のような `CASE` 式は、代入の中で引き続き使用できます。

### AFTER trigger formatting {#after-trigger-formatting}

`AFTER` トリガー関数では、単独の `RETURN NEW;` または `RETURN OLD;` をそれぞれ1行に単独で記述してください。

例:

```sql
BEGIN
    INSERT INTO audit_log (action) VALUES (TG_OP);
    RETURN NEW;
END;
```

`RETURN NEW;` または `RETURN OLD;` を別の文と同じ行に配置するコンパクトな関数本文は、実行時に失敗する可能性があります。

### Statement-level triggers {#statement-level-triggers}

`FOR EACH STATEMENT` 構文は受け付けられますが、現在は PostgreSQL の statement-level の動作ではなく、行ごとの動作として実行されます。

予測可能な動作のために、`FOR EACH ROW` を明示的に使用してください。

### Drop a trigger {#drop-a-trigger}

トリガーを削除する際は `IF EXISTS` を使用します。

```sql
DROP TRIGGER IF EXISTS users_audit ON users;
```

## シーケンス {#sequences}

シーケンスを作成して使用します。

```sql
CREATE SEQUENCE order_seq
START WITH 1000
INCREMENT BY 1;

SELECT nextval('order_seq');
SELECT currval('order_seq');
SELECT lastval();
SELECT setval('order_seq', 2000);
```

シーケンスを削除します。

```sql
DROP SEQUENCE order_seq;
```

シーケンスの作成時には、次のオプションを指定できます。

- `START`
- `INCREMENT`
- `MINVALUE`
- `MAXVALUE`
- `CACHE`
- `CYCLE`

`ALTER SEQUENCE` は、`OWNER TO` や `OWNED BY` などの所有権操作をサポートしています。作成後にシーケンス生成オプションを変更することはサポートしていません。シーケンスの位置を変更する必要がある場合は、`setval()` を使用してください。

## カスタム型 {#custom-types}

### Enum 型 {#enum-types}

Enum 型を作成します。

```sql
CREATE TYPE mood AS ENUM (
    'happy',
    'sad',
    'neutral'
);
```

Enum 値を追加します。

```sql
ALTER TYPE mood
ADD VALUE 'excited';
```

テーブルでこの型を使用します。

```sql
CREATE TABLE user_mood (
    id BIGSERIAL PRIMARY KEY,
    mood mood
);
```

> **Note:**
>
> Enum の比較と並び順には、PostgreSQL の宣言順ではなく Enum ラベルのテキストが使用されます。等価比較、`IN`、およびグループ化には影響しません。アプリケーションロジックが Enum の順序に依存する場合は、明示的なランキング式を使用してください。

たとえば、次のようになります。

```sql
SELECT mood
FROM user_mood
ORDER BY array_position(
    ARRAY['sad', 'neutral', 'happy', 'excited'],
    mood::text
);
```

### 複合型 {#composite-types}

複合型を作成します。

```sql
CREATE TYPE address AS (
    street TEXT,
    city TEXT,
    zip TEXT
);
```

## 照合順序 {#collations}

照合順序を作成します。

```sql
CREATE COLLATION my_collation (
    LOCALE = 'en_US.utf8'
);
```

カラムで使用します。

```sql
CREATE TABLE names (
    value TEXT COLLATE my_collation
);
```

照合順序を削除します。

```sql
DROP COLLATION my_collation;
```

カスタム照合順序は、通常のテキスト比較と `ORDER BY` の動作を変更します。`LOCALE` の値によってソート規則が選択されます。たとえば、`en_US.utf8` では `å`、`ä`、`ö` は `z` の前に並びますが、`sv_SE.utf8` ではこれらの文字は `z` の後に並びます。

### 照合順序の制限事項 {#collation-limitations}

次の違いに注意してください。

- 明示的なカスタム照合順序を指定していないテキストでは、バイト単位の順序が使用されます。
- 集約関数内の `ORDER BY` には照合順序は適用されません。
- ウィンドウ関数の `ORDER BY` には照合順序は適用されません。
- カスタム照合順序は使用できますが、`pg_collation` には一覧表示されません。