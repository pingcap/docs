---
title: SPLIT
summary: 指定した区切り文字を使用して文字列を分割し、結果の各部分を配列として返します。
---

# SPLIT

指定した区切り文字を使用して文字列を分割し、結果の各部分を配列として返します。

関連情報: [SPLIT_PART](/tidb-cloud-lake/sql/split-part.md)

## 構文 {#syntax}

```sql
SPLIT('<input_string>', '<delimiter>')
```

## 戻り値の型 {#return-type}

文字列の配列。入力文字列または区切り文字のいずれかが NULL の場合、SPLIT は NULL を返します。

## 例 {#examples}

```sql
-- 区切り文字としてスペースを使用します
-- SPLIT は 2 つの部分を含む配列を返します。
SELECT SPLIT('Datalake Cloud', ' ');

split('datalake cloud', ' ')|
----------------------------+
['Datalake','Cloud']        |

-- 空文字列を区切り文字として使用する場合、または入力文字列内に存在しない区切り文字を使用する場合
-- SPLIT は、入力文字列全体を 1 つの要素として含む配列を返します。
SELECT SPLIT('Datalake Cloud', '');

split('datalake cloud', '')|
---------------------------+
['Datalake Cloud']         |

SELECT SPLIT('Datalake Cloud', ',');

split('datalake cloud', ',')|
----------------------------+
['Datalake Cloud']          |

-- 区切り文字として ' '（タブ）を使用します
-- SPLIT は、タイムスタンプ、ログレベル、およびメッセージを含む配列を返します。

SELECT SPLIT('2023-10-19 15:30:45 INFO Log message goes here', ' ');

split('2023-10-19 15:30:45\tinfo\tlog message goes here', '\t')|
---------------------------------------------------------------+
['2023-10-19 15:30:45','INFO','Log message goes here']         |
```