---
title: CREATE SEQUENCE
summary: {{{ .lake }}} に新しいシーケンスを作成します。
---

# CREATE SEQUENCE

{{{ .lake }}} に新しいシーケンスを作成します。

シーケンスは、一意な数値識別子を自動生成するオブジェクトで、一般的にはテーブル行に異なる値（例: ユーザー ID）を割り当てるために使用されます。シーケンスは値の一意性を保証しますが、**連続性は保証しません**（つまり、欠番が発生する場合があります）。

## 構文 {#syntax}

```sql
CREATE [ OR REPLACE ] SEQUENCE [ IF NOT EXISTS ] <sequence>
    [ START [ = ] <start_value> ]
    [ INCREMENT [ = ] <increment_value> ]
```

| パラメータ           | 説明                                           | デフォルト |
|---------------------|-------------------------------------------------------|---------|
| `<sequence>`        | 作成するシーケンスの名前です。               | -       |
| `START`             | シーケンスの初期値です。                    | 1       |
| `INCREMENT`         | NEXTVAL を呼び出すたびの増分値です。         | 1       |

## アクセス制御の要件 {#access-control-requirements}

| 権限       | オブジェクトタイプ | 説明           |
|:----------------|:------------|:----------------------|
| CREATE SEQUENCE | Global      | シーケンスを作成します。 |

シーケンスを作成するには、操作を実行するユーザーまたは [current_role](/tidb-cloud-lake/guides/roles.md) が CREATE SEQUENCE [privilege](/tidb-cloud-lake/guides/privileges.md) を持っている必要があります。

> **Note:**
>
> enable_experimental_sequence_rbac_check 設定は、シーケンスレベルのアクセス制御を管理します。デフォルトでは無効です。
> シーケンスの作成では、詳細な RBAC チェックを行わず、ユーザーが superuser 権限を持っていることだけが必要です。
> 有効にすると、シーケンス作成時にきめ細かな権限検証が実施されます。
>
> これは実験的機能であり、将来的にはデフォルトで有効になる可能性があります。

## 例 {#examples}

### 基本的なシーケンス {#basic-sequence}

デフォルト設定（1 から開始し、1 ずつ増加）でシーケンスを作成します。

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

### 開始値と増分のカスタマイズ {#custom-start-and-increment}

1000 から開始し、10 ずつ増加するシーケンスを作成します。

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