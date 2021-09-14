---
title: Install TiDB data migration tools
summary: Learn how to install TiDB data migration tools.
---

# Install TiDB data migration tools


This document describes how to install data migration tools.

## Prerequisites

- [Hardware and software requirements](/hardware-and-software-requirements.md)
- [Environment and system configuration check](/check-before-deployment.md)

## Install TiUP

Since TiDB 4.0, TiUP serves as the package manager to help you easily manage different cluster components in the TiDB ecosystem. Now you can manage any components with only one single TiUP command line.

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
> To install a component of a specific version, you can use the `tiup install <component>[:version]` command.

## Helpful topics

- [Deploy TiUP offline](/production-deployment-using-tiup.md)
- [Deploy TiDB Lightning manually](/tidb-lightning/deploy-tidb-lightning.md)
- [Download Dumpling and DM](/download-ecosystem-tools.md)