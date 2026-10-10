---
title: SPLIT_PART
summary: 指定した区切り文字で文字列を分割し、指定した部分を返します。
---

# SPLIT_PART

指定した区切り文字で文字列を分割し、指定した部分を返します。

関連情報: [SPLIT](/tidb-cloud-lake/sql/split.md)

## 構文 {#syntax}

```sql
SPLIT_PART('<input_string>', '<delimiter>', '<position>')
```

*position* 引数は、返す部分を指定します。1 始まりのインデックスを使用しますが、正の値、負の値、0 も指定できます。

- *position* が正の数の場合、左から右へ数えたその位置の部分を返します。存在しない場合は NULL を返します。
- *position* が負の数の場合、右から左へ数えたその位置の部分を返します。存在しない場合は NULL を返します。
- *position* が 0 の場合は 1 として扱われ、実質的に文字列の最初の部分を返します。

## 戻り値の型 {#return-type}

文字列。入力文字列、区切り文字、または position のいずれかが NULL の場合、SPLIT_PART は NULL を返します。

## 例 {#examples}

```sql
-- 区切り文字としてスペースを使用
-- SPLIT_PART は指定した部分を返します。
SELECT SPLIT_PART('Datalake Cloud', ' ', 1);

split_part('datalake cloud', ' ', 1)|
------------------------------------+
Datalake                            |

-- 空文字列を区切り文字として使用する場合、または入力文字列内に存在しない区切り文字を使用する場合
-- SPLIT_PART は入力文字列全体を返します。
SELECT SPLIT_PART('Datalake Cloud', '', 1);

split_part('datalake cloud', '', 1)|
-----------------------------------+
Datalake Cloud                     |

SELECT SPLIT_PART('Datalake Cloud', ',', 1);

split_part('datalake cloud', ',', 1)|
------------------------------------+
Datalake Cloud                      |

-- 区切り文字として '   ' (tab) を使用
-- SPLIT_PART は個々のフィールドを返します。
SELECT SPLIT_PART('2023-10-19 15:30:45   INFO   Log message goes here', '   ', 3);

split_part('2023-10-19 15:30:45   info   log message goes here', '   ', 3)|
--------------------------------------------------------------------------+
Log message goes here                                                     |

-- 指定した部分がまったく存在しないため、SPLIT_PART は空文字列を返します。
SELECT SPLIT_PART('2023-10-19 15:30:45   INFO   Log message goes here', '   ', 4);

split_part('2023-10-19 15:30:45   info   log message goes here', '   ', 4)|
--------------------------------------------------------------------------+
                                                                          |
```