---
title: TRANSLATE
summary: 根据提供的映射关系，将给定字符串中的特定字符替换为对应的替换字符，从而对其进行转换。
---

# TRANSLATE

根据提供的映射关系，将给定字符串中的特定字符替换为对应的替换字符，从而对其进行转换。

## 语法 {#syntax}

```sql
TRANSLATE('<inputString>', '<charactersToReplace>', '<replacementCharacters>')
```

| 参数                      | 描述                                                                                            |
|---------------------------|-------------------------------------------------------------------------------------------------|
| `<inputString>`           | 要转换的输入字符串。                                                                            |
| `<charactersToReplace>`   | 包含输入字符串中需要被替换字符的字符串。                                                        |
| `<replacementCharacters>` | 包含替换字符的字符串，这些字符与 `<charactersToReplace>` 中的字符一一对应。                     |

## 示例 {#examples}

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