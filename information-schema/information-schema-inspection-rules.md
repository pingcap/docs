---
title: INSPECTION_RULES
summary: Learn the `INSPECTION_RULES` information_schema table.
---

# 検査ルール {#inspection-rules}

表`INSPECTION_RULES`は、検査結果でどの診断テストが実行されるかに関する情報を示します。使用例については[検査結果](/information-schema/information-schema-inspection-result.md)参照してください。

> **注記：**
>
> このテーブルは TiDB セルフホスト型にのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では利用できません。

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
