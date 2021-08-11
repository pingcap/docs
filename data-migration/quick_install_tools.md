---
title: Quick install guide of TiDB data migration tools
summary: Learn how to install TiDB data migration tools.
---

# Migrate from Aurora snapshot to TiDB

This document introduces how to install data migration related tools quickly.

## Complete the following tasks before start

- [Hardware and software requirements](/hardware-and-software-requirements.md)
- [Environment and system configuration check](/check-before-deployment.md)

## Install TiUP

Starting with TiDB 4.0, TiUP, as the package manager, makes it far easier to manage different cluster components in the TiDB ecosystem. Now you can run any component with only a single line of TiUP commands.

{{< copyable "shell-regular" >}}

```shell
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
```

Redeclare the global environment variables:

{{< copyable "shell-regular" >}}

```shell
source ~/.bash_profile
```

## Install Component

{{< copyable "shell-regular" >}}

```shell
tiup install dumpling tidb-lightning dm dmctl
```

> **Note:**
>
> You can install a component of specific version by: `tiup install <component>[:version]`

## Helpful Topics

- [Deploy TiUP offline](/production-deployment-using-tiup#method-2-deploy-tiup-offline)
- [Deploy TiDB Lightning manually](/tidb-lightning/deploy-tidb-lightning.md#deploy-tidb-lightning-manually)
- [Download Dumpling and DM](/download-ecosystem-tools#tidb-dm-data-migration)