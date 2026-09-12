---
title: SPLIT_PART
summary: 使用指定的分隔符切分字符串，并返回指定的部分。
---

# SPLIT_PART

使用指定的分隔符切分字符串，并返回指定的部分。

另请参阅：[SPLIT](/tidb-cloud-lake/sql/split.md)

## 语法 {#syntax}

```sql
SPLIT_PART('<input_string>', '<delimiter>', '<position>')
```

*position* 参数用于指定要返回哪一部分。它使用从 1 开始的索引，同时也接受正数、负数或 0：

- 如果 *position* 是正数，则返回从左到右对应位置的部分；如果该部分不存在，则返回 NULL。
- 如果 *position* 是负数，则返回从右到左对应位置的部分；如果该部分不存在，则返回 NULL。
- 如果 *position* 为 0，则按 1 处理，即返回字符串的第一部分。

## 返回类型 {#return-type}

字符串。当输入字符串、分隔符或 position 中任一值为 NULL 时，SPLIT_PART 返回 NULL。

## 示例 {#examples}

```sql
-- 使用空格作为分隔符
-- SPLIT_PART 返回指定的部分。
SELECT SPLIT_PART('Datalake Cloud', ' ', 1);

split_part('datalake cloud', ' ', 1)|
------------------------------------+
Datalake                            |

-- 使用空字符串作为分隔符，或使用输入字符串中不存在的分隔符
-- SPLIT_PART 返回整个输入字符串。
SELECT SPLIT_PART('Datalake Cloud', '', 1);

split_part('datalake cloud', '', 1)|
-----------------------------------+
Datalake Cloud                     |

SELECT SPLIT_PART('Datalake Cloud', ',', 1);

split_part('datalake cloud', ',', 1)|
------------------------------------+
Datalake Cloud                      |

-- 使用 '    '（tab）作为分隔符
-- SPLIT_PART 返回各个字段。
SELECT SPLIT_PART('2023-10-19 15:30:45   INFO   Log message goes here', '   ', 3);

split_part('2023-10-19 15:30:45   info   log message goes here', '   ', 3)|
--------------------------------------------------------------------------+
Log message goes here                                                     |

-- 由于指定的部分完全不存在，SPLIT_PART 返回空字符串。
SELECT SPLIT_PART('2023-10-19 15:30:45   INFO   Log message goes here', '   ', 4);

split_part('2023-10-19 15:30:45   info   log message goes here', '   ', 4)|
--------------------------------------------------------------------------+
                                                                          |
```