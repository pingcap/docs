---
title: SPLIT
summary: 使用指定的分隔符切分字符串，并将结果部分作为数组返回。
---

# SPLIT

使用指定的分隔符切分字符串，并将结果部分作为数组返回。

另请参阅：[SPLIT_PART](/tidb-cloud-lake/sql/split-part.md)

## 语法 {#syntax}

```sql
SPLIT('<input_string>', '<delimiter>')
```

## 返回类型 {#return-type}

字符串数组。当输入字符串或分隔符任一为 NULL 时，SPLIT 返回 NULL。

## 示例 {#examples}

```sql
-- 使用空格作为分隔符
-- SPLIT 返回一个包含两个部分的数组。
SELECT SPLIT('Datalake Cloud', ' ');

split('datalake cloud', ' ')|
----------------------------+
['Datalake','Cloud']        |

-- 使用空字符串作为分隔符，或使用输入字符串中不存在的分隔符
-- SPLIT 返回一个仅包含整个输入字符串作为单个部分的数组。
SELECT SPLIT('Datalake Cloud', '');

split('datalake cloud', '')|
---------------------------+
['Datalake Cloud']         |

SELECT SPLIT('Datalake Cloud', ',');

split('datalake cloud', ',')|
----------------------------+
['Datalake Cloud']          |

-- 使用 ' '（tab）作为分隔符
-- SPLIT 返回一个包含时间戳、日志等级和消息的数组。

SELECT SPLIT('2023-10-19 15:30:45 INFO Log message goes here', ' ');

split('2023-10-19 15:30:45\tinfo\tlog message goes here', '\t')|
---------------------------------------------------------------+
['2023-10-19 15:30:45','INFO','Log message goes here']         |
```