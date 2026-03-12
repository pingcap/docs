---
title: Masking Policy
---
import EEFeature from '@site/src/components/EEFeature';

<EEFeature featureName='MASKING POLICY'/>

This page provides a comprehensive overview of Masking Policy operations in Databend, organized by functionality for easy reference.

## Masking Policy Management

| Command | Description |
|---------|-------------|
| [CREATE MASKING POLICY](create-mask-policy.md) | Creates a new masking policy for data obfuscation |
| [DESCRIBE MASKING POLICY](desc-mask-policy.md) | Shows details of a specific masking policy |
| [DROP MASKING POLICY](drop-mask-policy.md) | Removes a masking policy |

## Related Topics

- [Masking Policy](/guides/security/masking-policy)

:::note
Masking policies in Databend allow you to protect sensitive data by dynamically transforming or obfuscating it when queried by users without proper privileges.
:::
