---
title: Masking Policy
summary: This page provides a comprehensive overview of Masking Policy operations in Databend, organized by functionality for easy reference.
---
import EEFeature from '@site/src/components/EEFeature';

<EEFeature featureName='MASKING POLICY'/>

This page provides a comprehensive overview of Masking Policy operations in Databend, organized by functionality for easy reference.

## Masking Policy Management

| Command | Description |
|---------|-------------|
| [CREATE MASKING POLICY](/tidb-cloud-lake/sql/create-masking-policy.md) | Creates a new masking policy for data obfuscation |
| [DESCRIBE MASKING POLICY](/tidb-cloud-lake/sql/desc-masking-policy.md) | Shows details of a specific masking policy |
| [DROP MASKING POLICY](/tidb-cloud-lake/sql/drop-masking-policy.md) | Removes a masking policy |

## Related Topics

- [Masking Policy](/tidb-cloud-lake/guides/masking-policy.md)

> **Note:**
>
> Masking policies in Databend allow you to protect sensitive data by dynamically transforming or obfuscating it when queried by users without proper privileges.
