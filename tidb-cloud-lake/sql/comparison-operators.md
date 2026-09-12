---
title: 比较运算符
summary: 本页介绍 TiDB Cloud Lake 中的比较运算符。
---

# 比较运算符

| 运算符      | 描述                                      | 示例                      | 结果   |
| ------------- | ------------------------------------------- | ------------------------- | ------ |
| `=`           | a 等于 b                                   | `2 = 2`                   | TRUE   |
| `!=`          | a 不等于 b                                 | `2 != 3`                  | TRUE   |
| `<>`         | a 不等于 b                                 | `2 <> 2`                 | FALSE  |
| `>`           | a 大于 b                                   | `2 > 3`                   | FALSE  |
| `>=`          | a 大于或等于 b                             | `4 >= NULL`               | NULL   |
| `<`           | a 小于 b                                   | `2 < 3`                   | TRUE   |
| `<=`          | a 小于或等于 b                             | `2 <= 3`                  | TRUE   |
| `IS NULL`     | 如果表达式为 NULL，则为 TRUE；否则为 FALSE | `(4 >= NULL) IS NULL`     | TRUE   |
| `IS NOT NULL` | 如果表达式为 NULL，则为 FALSE；否则为 TRUE | `(4 >= NULL) IS NOT NULL` | FALSE  |