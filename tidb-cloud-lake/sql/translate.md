---
title: TRANSLATE
summary: 指定されたマッピングに基づいて、特定の文字を対応する置換文字に置き換えることで、指定された文字列を変換します。
---

# TRANSLATE

指定されたマッピングに基づいて、特定の文字を対応する置換文字に置き換えることで、指定された文字列を変換します。

## 構文 {#syntax}

```sql
TRANSLATE('<inputString>', '<charactersToReplace>', '<replacementCharacters>')
```

| パラメータ                | 説明                                                                                           |
|---------------------------|------------------------------------------------------------------------------------------------|
| `<inputString>`           | 変換対象の入力文字列です。                                                                     |
| `<charactersToReplace>`   | 入力文字列内で置換対象となる文字を含む文字列です。                                             |
| `<replacementCharacters>` | `<charactersToReplace>` 内の文字に対応する置換文字を含む文字列です。                           |

## 例 {#examples}

```sql
-- Replace 'd' with '$' in 'datalake'
SELECT TRANSLATE('datalake', 'd', '$');

---
$atalake

-- Replace 'd' with 'D' in 'datalake'
SELECT TRANSLATE('datalake', 'd', 'D');

---
Datalake

-- Replace 'd' with 'D' and 'e' with 'E' in 'datalake'
SELECT TRANSLATE('datalake', 'de', 'DE');

---
DatalakE

-- Remove 'd' from 'datalake'
SELECT TRANSLATE('datalake', 'd', '');

---
atalake
```