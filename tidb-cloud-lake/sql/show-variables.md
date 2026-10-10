---
title: SHOW VARIABLES
summary: 名前、値、型など、すべてのセッション変数とその詳細を表示します。
---

# SHOW VARIABLES

名前、値、型など、すべてのセッション変数とその詳細を表示します。

関連情報: [SHOW_VARIABLES](/tidb-cloud-lake/sql/show-variables.md)

## 構文 {#syntax}

```sql
SHOW VARIABLES [ LIKE '<pattern>' | WHERE <expr> ]
```

## 例 {#examples}

次の例では、すべてのセッション変数をその値と型とともに一覧表示します。

```sql
SHOW VARIABLES;

┌──────────────────────────┐
│  name  │  value │  type  │
├────────┼────────┼────────┤
│ a      │ 3      │ UInt8  │
│ b      │ 55     │ UInt8  │
│ x      │ 'xx'   │ String │
│ y      │ 'yy'   │ String │
└──────────────────────────┘
```

`a` という名前の変数のみを絞り込んで返すには、次のいずれかのクエリを使用します。

```sql
SHOW VARIABLES LIKE 'a';

SHOW VARIABLES WHERE name = 'a';
```