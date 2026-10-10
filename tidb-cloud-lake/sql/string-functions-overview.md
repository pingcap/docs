---
title: 文字列関数
summary: このページでは、{{{ .lake }}} の文字列関数について、参照しやすいように機能別に整理して包括的に紹介します。
---

# 文字列関数

このページでは、{{{ .lake }}} の文字列関数について、参照しやすいように機能別に整理して包括的に紹介します。

## 文字列の連結と操作 {#string-concatenation-and-manipulation}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [CONCAT](/tidb-cloud-lake/sql/concat.md) | 文字列を連結します | `CONCAT('data', 'lake')` → `'datalake'` |
| [CONCAT_WS](/tidb-cloud-lake/sql/concat-ws.md) | 区切り文字を使って文字列を連結します | `CONCAT_WS('-', 'data', 'lake')` → `'data-lake'` |
| [INSERT](/tidb-cloud-lake/sql/insert.md) | 指定した位置に文字列を挿入します | `INSERT('datalake', 5, 0, 'cloud')` → `'datacloudlake'` |
| [REPLACE](/tidb-cloud-lake/sql/replace.md) | 部分文字列の出現箇所を置換します | `REPLACE('datalake', 'lake', 'cloud')` → `'datacloud'` |
| [TRANSLATE](/tidb-cloud-lake/sql/translate.md) | 文字を対応する置換文字に置き換えます | `TRANSLATE('datalake', 'de', 'DE')` → `'DatalakE'` |

## 文字列の抽出 {#string-extraction}

| 関数                                        | 説明                                                          | 例                                                                                |
|-------------------------------------------------|----------------------------------------------------------------------|----------------------------------------------------------------------------------------|
| [LEFT](/tidb-cloud-lake/sql/left.md)                                 | 左端から指定した文字数を返します                                     | `LEFT('datalake', 4)` → `'data'`                                                       |
| [RIGHT](/tidb-cloud-lake/sql/right.md)                               | 右端から指定した文字数を返します                                     | `RIGHT('datalake', 4)` → `'lake'`                                                      |
| [SUBSTR](/tidb-cloud-lake/sql/substr.md) / [SUBSTRING](/tidb-cloud-lake/sql/substring.md) | 部分文字列を抽出します                                               | `SUBSTR('datalake', 5, 4)` → `'lake'`                                                  |
| [MID](/tidb-cloud-lake/sql/mid.md)                                   | 部分文字列を抽出します（SUBSTRING のエイリアス）                     | `MID('datalake', 5, 4)` → `'lake'`                                                     |
| [SPLIT](/tidb-cloud-lake/sql/split.md)                               | 文字列を配列に分割します                                             | `SPLIT('data,lake', ',')` → `['data', 'lake']`                                         |
| [SPLIT_PART](/tidb-cloud-lake/sql/split-part.md)                     | 分割後の特定の部分を返します                                         | `SPLIT_PART('data,lake', ',', 2)` → `'lake'`                                           |
| [REGEXP_SPLIT_TO_ARRAY](/tidb-cloud-lake/sql/regexp-split-array.md)  | 指定したパターンを使って文字列をセグメントの配列に分割します         | `regexp_split_to_array('apple,banana,orange', ',');` → `'['apple','banana','orange']'` |
| [REGEXP_SPLIT_TO_TABLE](/tidb-cloud-lake/sql/regexp-split-table.md)  | 指定したパターンを使って文字列をセグメントのテーブルに分割します     | `regexp_split_to_table('data,lake', ',', 2)`                                           |

## 文字列のパディングと書式設定 {#string-padding-and-formatting}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [LPAD](/tidb-cloud-lake/sql/lpad.md) | 文字列の左側を埋めて指定した長さにします | `LPAD('lake', 8, 'data')` → `'datalake'` |
| [RPAD](/tidb-cloud-lake/sql/rpad.md) | 文字列の右側を埋めて指定した長さにします | `RPAD('data', 8, 'lake')` → `'datalake'` |
| [REPEAT](/tidb-cloud-lake/sql/repeat.md) | 文字列を n 回繰り返します | `REPEAT('data', 2)` → `'datadata'` |
| [SPACE](/tidb-cloud-lake/sql/space.md) | 空白文字からなる文字列を返します | `SPACE(4)` → `'    '` |
| [REVERSE](/tidb-cloud-lake/sql/reverse.md) | 文字列を逆順にします | `REVERSE('datalake')` → `'ekalatad'` |

## 文字列のトリミング {#string-trimming}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [TRIM](/tidb-cloud-lake/sql/trim.md) | 先頭と末尾の空白を削除します | `TRIM('  datalake  ')` → `'datalake'` |
| [TRIM_BOTH](/tidb-cloud-lake/sql/trim-both.md) | 両端から指定した文字を削除します | `TRIM_BOTH('xxdatalakexx', 'x')` → `'datalake'` |
| [TRIM_LEADING](/tidb-cloud-lake/sql/trim-leading.md) | 先頭から指定した文字を削除します | `TRIM_LEADING('xxdatalake', 'x')` → `'datalake'` |
| [TRIM_TRAILING](/tidb-cloud-lake/sql/trim-trailing.md) | 末尾から指定した文字を削除します | `TRIM_TRAILING('datalakexx', 'x')` → `'datalake'` |
| [LTRIM](/tidb-cloud-lake/sql/ltrim.md) | 先頭の空白を削除します | `LTRIM('  datalake')` → `'datalake'` |
| [RTRIM](/tidb-cloud-lake/sql/rtrim.md) | 末尾の空白を削除します | `RTRIM('datalake  ')` → `'datalake'` |

## 文字列情報 {#string-information}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [LENGTH](/tidb-cloud-lake/sql/length.md) | 文字数で文字列の長さを返します | `LENGTH('datalake')` → `8` |
| [CHAR_LENGTH](/tidb-cloud-lake/sql/char-length.md) / [CHARACTER_LENGTH](/tidb-cloud-lake/sql/character-length.md) | 文字数で文字列の長さを返します | `CHAR_LENGTH('datalake')` → `8` |
| [BIT_LENGTH](/tidb-cloud-lake/sql/bit-length.md) | ビット数で文字列の長さを返します | `BIT_LENGTH('datalake')` → `64` |
| [OCTET_LENGTH](/tidb-cloud-lake/sql/octet-length.md) | バイト数で文字列の長さを返します | `OCTET_LENGTH('datalake')` → `8` |
| [INSTR](/tidb-cloud-lake/sql/instr.md) | 最初に出現する位置を返します | `INSTR('datalake', 'lake')` → `5` |
| [LOCATE](/tidb-cloud-lake/sql/locate.md) | 最初に出現する位置を返します | `LOCATE('lake', 'datalake')` → `5` |
| [POSITION](/tidb-cloud-lake/sql/position.md) | 最初に出現する位置を返します | `POSITION('lake' IN 'datalake')` → `5` |
| [STRCMP](/tidb-cloud-lake/sql/strcmp.md) | 2 つの文字列を比較します | `STRCMP('datalake', 'datalake')` → `0` |
| [JARO_WINKLER](/tidb-cloud-lake/sql/jaro-winkler.md) | 文字列間の類似度を返します | `JARO_WINKLER('datalake', 'datalake')` → `1.0` |

## 大文字・小文字の変換 {#case-conversion}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [LOWER](/tidb-cloud-lake/sql/lower.md) / [LCASE](/tidb-cloud-lake/sql/lcase.md) | 小文字に変換します | `LOWER('DataLake')` → `'datalake'` |
| [UPPER](/tidb-cloud-lake/sql/upper.md) / [UCASE](/tidb-cloud-lake/sql/ucase.md) | 大文字に変換します | `UPPER('datalake')` → `'DATALAKE'` |

## パターンマッチング {#pattern-matching}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [LIKE](/tidb-cloud-lake/sql/like.md) | ワイルドカードを使ったパターンマッチング | `'datalake' LIKE 'data%'` → `true` |
| [NOT_LIKE](/tidb-cloud-lake/sql/not-like.md) | LIKE の否定 | `'datalake' NOT LIKE 'cloud%'` → `true` |
| [REGEXP](/tidb-cloud-lake/sql/regexp.md) / [RLIKE](/tidb-cloud-lake/sql/rlike.md) | 正規表現を使ったパターンマッチング | `'datalake' REGEXP '^data'` → `true` |
| [NOT_REGEXP](/tidb-cloud-lake/sql/not-regexp.md) / [NOT_RLIKE](/tidb-cloud-lake/sql/not-rlike.md) | 正規表現マッチングの否定 | `'datalake' NOT REGEXP '^cloud'` → `true` |
| [REGEXP_LIKE](/tidb-cloud-lake/sql/regexp-like.md) | 正規表現に一致するかどうかを boolean で返します | `REGEXP_LIKE('datalake', '^data')` → `true` |
| [REGEXP_INSTR](/tidb-cloud-lake/sql/regexp-instr.md) | 正規表現に一致した位置を返します | `REGEXP_INSTR('datalake', 'lake')` → `5` |
| [REGEXP_SUBSTR](/tidb-cloud-lake/sql/regexp-substr.md) | 正規表現に一致する部分文字列を返します | `REGEXP_SUBSTR('datalake', 'lake')` → `'lake'` |
| [REGEXP_REPLACE](/tidb-cloud-lake/sql/regexp-replace.md) | 正規表現に一致した部分を置換します | `REGEXP_REPLACE('datalake', 'lake', 'cloud')` → `'datacloud'` |
| [GLOB](/tidb-cloud-lake/sql/glob.md) | Unix スタイルのパターンマッチング | `'datalake' GLOB 'data*'` → `true` |

## エンコードとデコード {#encoding-and-decoding}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [ASCII](/tidb-cloud-lake/sql/ascii.md) | 先頭文字の ASCII 値を返します | `ASCII('D')` → `68` |
| [ORD](/tidb-cloud-lake/sql/ord.md) | 先頭文字の Unicode コードポイントを返します | `ORD('D')` → `68` |
| [CHAR](/tidb-cloud-lake/sql/char.md) / [CHR](/tidb-cloud-lake/sql/char.md) | 指定した Unicode コードポイントに対応する文字列を返します | `CHAR(68,97,116,97)` → `'Data'` |
| [BIN](/tidb-cloud-lake/sql/bin.md) | 2 進表現を返します | `BIN(5)` → `'101'` |
| [OCT](/tidb-cloud-lake/sql/oct.md) | 8 進表現を返します | `OCT(8)` → `'10'` |
| [HEX](/tidb-cloud-lake/sql/hex.md) | 16 進表現を返します | `HEX('ABC')` → `'414243'` |
| [UNHEX](/tidb-cloud-lake/sql/unhex.md) | 16 進数をバイナリに変換します | `UNHEX('414243')` → `'ABC'` |
| [TO_BASE64](/tidb-cloud-lake/sql/to-base64.md) | base64 にエンコードします | `TO_BASE64('datalake')` → `'ZGF0YWxha2U='` |
| [FROM_BASE64](/tidb-cloud-lake/sql/from-base64.md) | base64 からデコードします | `FROM_BASE64('ZGF0YWxha2U=')` → `'datalake'` |

## その他 {#miscellaneous}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [QUOTE](/tidb-cloud-lake/sql/quote.md) | SQL 用に文字列をエスケープします | `QUOTE('datalake')` → `'"datalake"'` |
| [SOUNDEX](/tidb-cloud-lake/sql/soundex.md) | soundex コードを返します | `SOUNDEX('datalake')` → `'D42'` |
| [SOUNDSLIKE](/tidb-cloud-lake/sql/sounds-like.md) | soundex 値を比較します | `SOUNDSLIKE('datalake', 'datalake')` → `true` |