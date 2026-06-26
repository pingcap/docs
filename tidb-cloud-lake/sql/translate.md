---
title: TRANSLATE
summary: Transforms a given string by replacing specific characters with corresponding replacements, as defined by the provided mapping.
---

# TRANSLATE

Transforms a given string by replacing specific characters with corresponding replacements, as defined by the provided mapping.

## Syntax

```sql
TRANSLATE('<inputString>', '<charactersToReplace>', '<replacementCharacters>')
```

| Parameter                 | Description                                                                                     |
|---------------------------|-------------------------------------------------------------------------------------------------|
| `<inputString>`           | The input string to be transformed.                                                             |
| `<charactersToReplace>`   | The string containing characters to be replaced in the input string.                            |
| `<replacementCharacters>` | The string containing replacement characters corresponding to those in `<charactersToReplace>`. |

## Examples

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
