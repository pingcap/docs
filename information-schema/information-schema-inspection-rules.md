---
title: INSPECTION_RULES
summary: INSPECTION_RULES` information_schema テーブルについて学習します。
---

# 検査ルール {#inspection-rules}

`INSPECTION_RULES`表は、検査結果で実行される診断テストに関する情報を提供します。使用例については[検査結果](/information-schema/information-schema-inspection-result.md)参照してください。

> **注記：**
>
> このテーブルは TiDB Self-Managed にのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では使用できません。

```sql
USE information_schema;
DESC inspection_rules;
```

    +---------+--------------+------+------+---------+-------+
    | Field   | Type         | Null | Key  | Default | Extra |
    +---------+--------------+------+------+---------+-------+
    | NAME    | varchar(64)  | YES  |      | NULL    |       |
    | TYPE    | varchar(64)  | YES  |      | NULL    |       |
    | COMMENT | varchar(256) | YES  |      | NULL    |       |
    +---------+--------------+------+------+---------+-------+
    3 rows in set (0.00 sec)

```sql
SELECT * FROM inspection_rules;
```

    +-----------------+------------+---------+
    | NAME            | TYPE       | COMMENT |
    +-----------------+------------+---------+
    | config          | inspection |         |
    | version         | inspection |         |
    | node-load       | inspection |         |
    | critical-error  | inspection |         |
    | threshold-check | inspection |         |
    | ddl             | summary    |         |
    | gc              | summary    |         |
    | pd              | summary    |         |
    | query-summary   | summary    |         |
    | raftstore       | summary    |         |
    | read-link       | summary    |         |
    | rocksdb         | summary    |         |
    | stats           | summary    |         |
    | wait-events     | summary    |         |
    | write-link      | summary    |         |
    +-----------------+------------+---------+
    15 rows in set (0.00 sec)
