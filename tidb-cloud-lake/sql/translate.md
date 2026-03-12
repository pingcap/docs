---
title: TRANSLATE
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.203"/>

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
-- Replace 'd' with '$' in 'databend'
SELECT TRANSLATE('databend', 'd', '$');

---
$ataben$

-- Replace 'd' with 'D' in 'databend'
SELECT TRANSLATE('databend', 'd', 'D');

---
DatabenD

-- Replace 'd' with 'D' and 'e' with 'E' in 'databend'
SELECT TRANSLATE('databend', 'de', 'DE');

---
DatabEnD

-- Remove 'd' from 'databend'
SELECT TRANSLATE('databend', 'd', '');

---
ataben
```