---
title: NEXTVAL
summary: シーケンスから次の値を取得します。
---

# NEXTVAL

シーケンスから次の値を取得します。

## 構文 {#syntax}

```sql
NEXTVAL(<sequence_name>)
```

## 戻り値の型 {#return-type}

整数です。

## アクセス制御の要件 {#access-control-requirements}

| 権限 | オブジェクトタイプ | 説明 |
|:----------------|:------------|:-------------------|
| ACCESS SEQUENCE | SEQUENCE    | シーケンスにアクセスします。 |

シーケンスにアクセスするには、操作を実行するユーザーまたはロールが ACCESS SEQUENCE [権限](/tidb-cloud-lake/guides/privileges.md) を持っている必要があります。

> **Note:**
>
> `enable_experimental_sequence_rbac_check` 設定は、シーケンスレベルのアクセス制御を管理します。デフォルトでは無効です。
> シーケンスの作成では、詳細な RBAC チェックを行わず、ユーザーが superuser 権限を持っていることだけが必要です。
> 有効にすると、シーケンス作成時にきめ細かな権限検証が実施されます。
>
> これは実験的機能であり、将来的にはデフォルトで有効になる可能性があります。

## 例 {#examples}

次の例は、NEXTVAL 関数がシーケンスとどのように動作するかを示しています。

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

次の例は、シーケンスと NEXTVAL 関数を使用して、テーブル内の行に一意の識別子を自動生成して割り当てる方法を示しています。

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