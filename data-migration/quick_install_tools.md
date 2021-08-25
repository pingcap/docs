---
title: Quick install guide of TiDB data migration tools
summary: Learn how to install TiDB data migration tools.
---

# Migrate from Aurora snapshots to TiDB

This document introduces how to install data migration tools quickly.

## Complete the following tasks before start

- [Hardware and software requirements](/hardware-and-software-requirements.md)
- [Environment and system configuration check](/check-before-deployment.md)

## Install TiUP

Starting with TiDB 4.0, TiUP, as the package manager, helps you easily manage different cluster components in the TiDB ecosystem. Now you can run any component with only a single TiUP command line.

{{< copyable "shell-regular" >}}

```shell
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
```

Redeclare the global environment variables:

{{< copyable "shell-regular" >}}

```shell
source ~/.bash_profile
```

## Install Components

{{< copyable "shell-regular" >}}

```shell
tiup install dumpling tidb-lightning dm dmctl
```

> **Note:**
>
> You can install a component of a specific version by: `tiup install <component>[:version]`

## Helpful Topics

- [Deploy TiUP offline](/production-deployment-using-tiup.md)
- [Deploy TiDB Lightning manually](/tidb-lightning/deploy-tidb-lightning.md)
- [Download Dumpling and DM](/download-ecosystem-tools.md)