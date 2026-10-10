---
title: EXPLAIN AST
summary: SQL 文の抽象構文木（AST）を返します。このコマンドは SQL 文を構文要素に分解し、階層構造で表現します。
---

# EXPLAIN AST

SQL 文の抽象構文木（AST）を返します。このコマンドは SQL 文を構文要素に分解し、階層構造で表現します。

## 構文 {#syntax}

```sql
EXPLAIN AST <statement>
```

## 例 {#examples}

```sql
EXPLAIN AST create user 'test'@'localhost' identified with sha256_password by 'new_password';

 ----
 CreateUser (children 3)
 ├── User 'test'@'localhost'
 ├── AuthType sha256_password
 └── Password "new_password"
 ```

 ```sql
EXPLAIN AST insert into t1 (a, b) values (1, 2),(3, 4);

 ----
 Insert (children 3)
 ├── TableIdentifier t1
 ├── Columns (children 2)
 │   ├── Identifier a
 │   └── Identifier b
 └── Source (children 1)
     └── ValueSource
```

```sql
EXPLAIN AST select * from t1 inner join t2 on t1.a = t2.a and t1.b = t2.b and t1.a > 2;

 ----
 Query (children 1)
 └── QueryBody (children 1)
     └── SelectQuery (children 2)
         ├── SelectList (children 1)
         │   └── Target *
         └── TableList (children 1)
             └── TableJoin (children 1)
                 └── Join (children 3)
                     ├── TableIdentifier t1
                     ├── TableIdentifier t2
                     └── ConditionOn (children 1)
                         └── Function AND (children 2)
                             ├── Function AND (children 2)
                             │   ├── Function = (children 2)
                             │   │   ├── ColumnIdentifier t1.a
                             │   │   └── ColumnIdentifier t2.a
                             │   └── Function = (children 2)
                             │       ├── ColumnIdentifier t1.b
                             │       └── ColumnIdentifier t2.b
                             └── Function > (children 2)
                                 ├── ColumnIdentifier t1.a
                                 └── Literal Integer(2)
```