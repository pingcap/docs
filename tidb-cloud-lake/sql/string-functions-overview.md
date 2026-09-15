---
title: 字符串函数
summary: 本页按功能对 {{{ .lake }}} 中的字符串函数进行了全面概览，便于快速查阅。
---

# 字符串函数

本页按功能对 {{{ .lake }}} 中的字符串函数进行了全面概览，便于快速查阅。

## 字符串拼接与操作 {#string-concatenation-and-manipulation}

| Function | 描述 | 示例 |
|----------|-------------|---------|
| [CONCAT](/tidb-cloud-lake/sql/concat.md) | 拼接字符串 | `CONCAT('data', 'lake')` → `'datalake'` |
| [CONCAT_WS](/tidb-cloud-lake/sql/concat-ws.md) | 使用分隔符拼接字符串 | `CONCAT_WS('-', 'data', 'lake')` → `'data-lake'` |
| [INSERT](/tidb-cloud-lake/sql/insert.md) | 在指定位置插入字符串 | `INSERT('datalake', 5, 0, 'cloud')` → `'datacloudlake'` |
| [REPLACE](/tidb-cloud-lake/sql/replace.md) | 替换子字符串的出现位置 | `REPLACE('datalake', 'lake', 'cloud')` → `'datacloud'` |
| [TRANSLATE](/tidb-cloud-lake/sql/translate.md) | 将字符替换为对应的替换字符 | `TRANSLATE('datalake', 'de', 'DE')` → `'DatalakE'` |

## 字符串提取 {#string-extraction}

| Function                                        | 描述                                                                 | 示例                                                                                   |
|-------------------------------------------------|----------------------------------------------------------------------|----------------------------------------------------------------------------------------|
| [LEFT](/tidb-cloud-lake/sql/left.md)                                 | 返回最左侧的字符                                                     | `LEFT('datalake', 4)` → `'data'`                                                       |
| [RIGHT](/tidb-cloud-lake/sql/right.md)                               | 返回最右侧的字符                                                     | `RIGHT('datalake', 4)` → `'lake'`                                                      |
| [SUBSTR](/tidb-cloud-lake/sql/substr.md) / [SUBSTRING](/tidb-cloud-lake/sql/substring.md) | 提取子字符串                                                         | `SUBSTR('datalake', 5, 4)` → `'lake'`                                                  |
| [MID](/tidb-cloud-lake/sql/mid.md)                                   | 提取子字符串（SUBSTRING 的别名）                                     | `MID('datalake', 5, 4)` → `'lake'`                                                     |
| [SPLIT](/tidb-cloud-lake/sql/split.md)                               | 将字符串切分为数组                                                   | `SPLIT('data,lake', ',')` → `['data', 'lake']`                                         |
| [SPLIT_PART](/tidb-cloud-lake/sql/split-part.md)                     | 切分后返回指定部分                                                   | `SPLIT_PART('data,lake', ',', 2)` → `'lake'`                                           |
| [REGEXP_SPLIT_TO_ARRAY](/tidb-cloud-lake/sql/regexp-split-array.md)  | 使用指定模式将字符串切分为片段数组                                   | `regexp_split_to_array('apple,banana,orange', ',');` → `'['apple','banana','orange']'` |
| [REGEXP_SPLIT_TO_TABLE](/tidb-cloud-lake/sql/regexp-split-table.md)  | 使用指定模式将字符串切分为片段表                                     | `regexp_split_to_table('data,lake', ',', 2)`                                           |

## 字符串填充与格式化 {#string-padding-and-formatting}

| Function | 描述 | 示例 |
|----------|-------------|---------|
| [LPAD](/tidb-cloud-lake/sql/lpad.md) | 在左侧填充字符串至指定长度 | `LPAD('lake', 8, 'data')` → `'datalake'` |
| [RPAD](/tidb-cloud-lake/sql/rpad.md) | 在右侧填充字符串至指定长度 | `RPAD('data', 8, 'lake')` → `'datalake'` |
| [REPEAT](/tidb-cloud-lake/sql/repeat.md) | 将字符串重复 n 次 | `REPEAT('data', 2)` → `'datadata'` |
| [SPACE](/tidb-cloud-lake/sql/space.md) | 返回由空格组成的字符串 | `SPACE(4)` → `'    '` |
| [REVERSE](/tidb-cloud-lake/sql/reverse.md) | 反转字符串 | `REVERSE('datalake')` → `'ekalatad'` |

## 字符串裁剪 {#string-trimming}

| Function | 描述 | 示例 |
|----------|-------------|---------|
| [TRIM](/tidb-cloud-lake/sql/trim.md) | 移除首尾空格 | `TRIM('  datalake  ')` → `'datalake'` |
| [TRIM_BOTH](/tidb-cloud-lake/sql/trim-both.md) | 移除两端指定字符 | `TRIM_BOTH('xxdatalakexx', 'x')` → `'datalake'` |
| [TRIM_LEADING](/tidb-cloud-lake/sql/trim-leading.md) | 移除开头的指定字符 | `TRIM_LEADING('xxdatalake', 'x')` → `'datalake'` |
| [TRIM_TRAILING](/tidb-cloud-lake/sql/trim-trailing.md) | 移除末尾的指定字符 | `TRIM_TRAILING('datalakexx', 'x')` → `'datalake'` |
| [LTRIM](/tidb-cloud-lake/sql/ltrim.md) | 移除前导空格 | `LTRIM('  datalake')` → `'datalake'` |
| [RTRIM](/tidb-cloud-lake/sql/rtrim.md) | 移除尾随空格 | `RTRIM('datalake  ')` → `'datalake'` |

## 字符串信息 {#string-information}

| Function | 描述 | 示例 |
|----------|-------------|---------|
| [LENGTH](/tidb-cloud-lake/sql/length.md) | 返回字符串的字符长度 | `LENGTH('datalake')` → `8` |
| [CHAR_LENGTH](/tidb-cloud-lake/sql/char-length.md) / [CHARACTER_LENGTH](/tidb-cloud-lake/sql/character-length.md) | 返回字符串的字符长度 | `CHAR_LENGTH('datalake')` → `8` |
| [BIT_LENGTH](/tidb-cloud-lake/sql/bit-length.md) | 返回字符串的位长度 | `BIT_LENGTH('datalake')` → `64` |
| [OCTET_LENGTH](/tidb-cloud-lake/sql/octet-length.md) | 返回字符串的字节长度 | `OCTET_LENGTH('datalake')` → `8` |
| [INSTR](/tidb-cloud-lake/sql/instr.md) | 返回首次出现的位置 | `INSTR('datalake', 'lake')` → `5` |
| [LOCATE](/tidb-cloud-lake/sql/locate.md) | 返回首次出现的位置 | `LOCATE('lake', 'datalake')` → `5` |
| [POSITION](/tidb-cloud-lake/sql/position.md) | 返回首次出现的位置 | `POSITION('lake' IN 'datalake')` → `5` |
| [STRCMP](/tidb-cloud-lake/sql/strcmp.md) | 比较两个字符串 | `STRCMP('datalake', 'datalake')` → `0` |
| [JARO_WINKLER](/tidb-cloud-lake/sql/jaro-winkler.md) | 返回字符串之间的相似度 | `JARO_WINKLER('datalake', 'datalake')` → `1.0` |

## 大小写转换 {#case-conversion}

| Function | 描述 | 示例 |
|----------|-------------|---------|
| [LOWER](/tidb-cloud-lake/sql/lower.md) / [LCASE](/tidb-cloud-lake/sql/lcase.md) | 转换为小写 | `LOWER('DataLake')` → `'datalake'` |
| [UPPER](/tidb-cloud-lake/sql/upper.md) / [UCASE](/tidb-cloud-lake/sql/ucase.md) | 转换为大写 | `UPPER('datalake')` → `'DATALAKE'` |

## 模式匹配 {#pattern-matching}

| Function | 描述 | 示例 |
|----------|-------------|---------|
| [LIKE](/tidb-cloud-lake/sql/like.md) | 使用通配符进行模式匹配 | `'datalake' LIKE 'data%'` → `true` |
| [NOT_LIKE](/tidb-cloud-lake/sql/not-like.md) | LIKE 的否定形式 | `'datalake' NOT LIKE 'cloud%'` → `true` |
| [REGEXP](/tidb-cloud-lake/sql/regexp.md) / [RLIKE](/tidb-cloud-lake/sql/rlike.md) | 使用正则表达式进行模式匹配 | `'datalake' REGEXP '^data'` → `true` |
| [NOT_REGEXP](/tidb-cloud-lake/sql/not-regexp.md) / [NOT_RLIKE](/tidb-cloud-lake/sql/not-rlike.md) | 正则匹配的否定形式 | `'datalake' NOT REGEXP '^cloud'` → `true` |
| [REGEXP_LIKE](/tidb-cloud-lake/sql/regexp-like.md) | 返回正则匹配的布尔值 | `REGEXP_LIKE('datalake', '^data')` → `true` |
| [REGEXP_INSTR](/tidb-cloud-lake/sql/regexp-instr.md) | 返回正则匹配的位置 | `REGEXP_INSTR('datalake', 'lake')` → `5` |
| [REGEXP_SUBSTR](/tidb-cloud-lake/sql/regexp-substr.md) | 返回匹配正则的子字符串 | `REGEXP_SUBSTR('datalake', 'lake')` → `'lake'` |
| [REGEXP_REPLACE](/tidb-cloud-lake/sql/regexp-replace.md) | 替换正则匹配的内容 | `REGEXP_REPLACE('datalake', 'lake', 'cloud')` → `'datacloud'` |
| [GLOB](/tidb-cloud-lake/sql/glob.md) | Unix 风格的模式匹配 | `'datalake' GLOB 'data*'` → `true` |

## 编码与解码 {#encoding-and-decoding}

| Function | 描述 | 示例 |
|----------|-------------|---------|
| [ASCII](/tidb-cloud-lake/sql/ascii.md) | 返回第一个字符的 ASCII 值 | `ASCII('D')` → `68` |
| [ORD](/tidb-cloud-lake/sql/ord.md) | 返回第一个字符的 Unicode 码点 | `ORD('D')` → `68` |
| [CHAR](/tidb-cloud-lake/sql/char.md) / [CHR](/tidb-cloud-lake/sql/char.md) | 根据给定的 Unicode 码点返回字符组成的字符串 | `CHAR(68,97,116,97)` → `'Data'` |
| [BIN](/tidb-cloud-lake/sql/bin.md) | 返回二进制表示 | `BIN(5)` → `'101'` |
| [OCT](/tidb-cloud-lake/sql/oct.md) | 返回八进制表示 | `OCT(8)` → `'10'` |
| [HEX](/tidb-cloud-lake/sql/hex.md) | 返回十六进制表示 | `HEX('ABC')` → `'414243'` |
| [UNHEX](/tidb-cloud-lake/sql/unhex.md) | 将十六进制转换为二进制 | `UNHEX('414243')` → `'ABC'` |
| [TO_BASE64](/tidb-cloud-lake/sql/to-base64.md) | 编码为 base64 | `TO_BASE64('datalake')` → `'ZGF0YWxha2U='` |
| [FROM_BASE64](/tidb-cloud-lake/sql/from-base64.md) | 从 base64 解码 | `FROM_BASE64('ZGF0YWxha2U=')` → `'datalake'` |

## 其他 {#miscellaneous}

| Function | 描述 | 示例 |
|----------|-------------|---------|
| [QUOTE](/tidb-cloud-lake/sql/quote.md) | 为 SQL 转义字符串 | `QUOTE('datalake')` → `'"datalake"'` |
| [SOUNDEX](/tidb-cloud-lake/sql/soundex.md) | 返回 soundex 编码 | `SOUNDEX('datalake')` → `'D42'` |
| [SOUNDSLIKE](/tidb-cloud-lake/sql/sounds-like.md) | 比较 soundex 值 | `SOUNDSLIKE('datalake', 'datalake')` → `true` |