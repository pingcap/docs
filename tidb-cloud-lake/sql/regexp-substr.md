---
title: REGEXP_SUBSTR
summary: パターン `pat` で指定された正規表現に一致する文字列 `expr` の部分文字列を返します。一致がない場合は NULL を返します。`expr` または `pat` が NULL の場合、戻り値は NULL です。
---

# REGEXP_SUBSTR

パターン `pat` で指定された正規表現に一致する文字列 `expr` の部分文字列を返します。一致がない場合は NULL を返します。expr または pat が NULL の場合、戻り値は NULL です。

- REGEXP_SUBSTR はキャプチャグループ（丸括弧 `()` で定義されるサブパターン）の抽出をサポートしていません。特定のキャプチャグループではなく、一致した部分文字列全体を返します。

```sql
SELECT REGEXP_SUBSTR('abc123', '(\w+)(\d+)');
-- Returns 'abc123' (the entire match), not 'abc' or '123'.

-- Alternative Solution: Use string functions like SUBSTRING and REGEXP_INSTR to manually extract the desired portion of the string:
SELECT SUBSTRING('abc123', 1, REGEXP_INSTR('abc123', '\d+') - 1);
-- Returns 'abc' (extracts the part before the digits).
SELECT SUBSTRING('abc123', REGEXP_INSTR('abc123', '\d+'));
-- Returns '123' (extracts the digits).
```

- REGEXP_SUBSTR は、`e` パラメータ（Snowflake でキャプチャグループを抽出するために使用）や、返すキャプチャグループを指定する `group_num` パラメータをサポートしていません。

```sql
SELECT REGEXP_SUBSTR('abc123', '(\w+)(\d+)', 1, 1, 'e', 1);
-- Error: {{{ .lake }}} does not support the 'e' parameter or capture group extraction.

-- Alternative Solution: Use string functions like SUBSTRING and LOCATE to manually extract the desired substring, or preprocess the data with external tools (e.g., Python) to extract capture groups before querying.
SELECT SUBSTRING(
    REGEXP_SUBSTR('letters:abc,numbers:123', 'letters:[a-z]+,numbers:[0-9]+'),
    LOCATE('letters:', 'letters:abc,numbers:123') + 8,
    LOCATE(',', 'letters:abc,numbers:123') - (LOCATE('letters:', 'letters:abc,numbers:123') + 8)
);
-- Returns 'abc'
```

## 構文 {#syntax}

```sql
REGEXP_SUBSTR(<expr>, <pat[, pos[, occurrence[, match_type]]]>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|------------|-----------------------------------------------------------------------------------------------------------|
| expr       | 一致対象となる文字列 expr |
| pat        | 正規表現 |
| pos        | 任意。検索を開始する expr 内の位置です。省略した場合のデフォルトは 1 です。 |
| occurrence | 任意。検索する一致の出現回数です。省略した場合のデフォルトは 1 です。 |
| match_type | 任意。一致方法を指定する文字列です。意味は REGEXP_LIKE() で説明されているものと同じです。 |

## 戻り値の型 {#return-type}

`VARCHAR`

## 例 {#examples}

```sql
SELECT REGEXP_SUBSTR('abc def ghi', '[a-z]+');
+----------------------------------------+
| REGEXP_SUBSTR('abc def ghi', '[a-z]+') |
+----------------------------------------+
| abc                                    |
+----------------------------------------+

SELECT REGEXP_SUBSTR('abc def ghi', '[a-z]+', 1, 3);
+----------------------------------------------+
| REGEXP_SUBSTR('abc def ghi', '[a-z]+', 1, 3) |
+----------------------------------------------+
| ghi                                          |
+----------------------------------------------+

SELECT REGEXP_SUBSTR('周 周周 周周周 周周周周', '周+', 2, 3);
+------------------------------------------------------------------+
| REGEXP_SUBSTR('周 周周 周周周 周周周周', '周+', 2, 3)            |
+------------------------------------------------------------------+
| 周周周周                                                         |
+------------------------------------------------------------------+

```