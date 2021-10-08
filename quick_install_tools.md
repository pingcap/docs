---
title: Install TiDB data migration tools
summary: Learn how to install TiDB data migration tools.
---

# Install TiDB data migration tools

This document describes how to install data migration tools. Since TiDB 4.0, TiUP serves as the package manager to help you easily manage different cluster components in the TiDB ecosystem. Now you can manage any components with only one single TiUP command line.

## Prerequisites

- [Hardware and software requirements](/hardware-and-software-requirements.md)
- [Environment and system configuration check](/check-before-deployment.md)

## Step 1. Install TiUP

{{< copyable "shell-regular" >}}

```shell
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
```

Redeclare the global environment variables:

{{< copyable "shell-regular" >}}

```shell
source ~/.bash_profile
```

## Step 2. Install Components

You can start by listing all the installable components

{{< copyable "shell-regular" >}}

```shell
tiup list
```

The following output can be seen

```bash
Available components:
Name            Owner    Description
----            -----    -----------
bench           pingcap  Benchmark database with different workloads
br              pingcap  TiDB/TiKV cluster backup restore tool
cdc             pingcap  CDC is a change data capture tool for TiDB
client          pingcap  Client to connect playground
cluster         pingcap  Deploy a TiDB cluster for production
ctl             pingcap  TiDB controller suite
dm              pingcap  Data Migration Platform manager
dmctl           pingcap  dmctl component of Data Migration Platform
errdoc          pingcap  Document about TiDB errors
pd-recover      pingcap  PD Recover is a disaster recovery tool of PD, used to recover the PD cluster which cannot start or provide services normally
playground      pingcap  Bootstrap a local TiDB cluster for fun
tidb            pingcap  TiDB is an open source distributed HTAP database compatible with the MySQL protocol
tidb-lightning  pingcap  TiDB Lightning is a tool used for fast full import of large amounts of data into a TiDB cluster
tiup            pingcap  TiUP is a command-line component management tool that can help to download and install TiDB platform components to the local system
```

At this point, you can select one or more components to install

{{< copyable "shell-regular" >}}

```shell
tiup install dumpling tidb-lightning
```

> **Note:**
>
> To install a component of a specific version, you can use the `tiup install <component>[:version]` command.

## Step 3. Update TiUP and components (Optional)

It is recommended that you check the release notes and pay attention to compatibility changes.

{{< copyable "shell-regular" >}}

```shell
tiup update --self && tiup update dm
```

## Helpful topics

- [Deploy TiUP offline](/production-deployment-using-tiup.md)
- [Deploy TiDB Lightning manually](/tidb-lightning/deploy-tidb-lightning.md)
- [Download Dumpling and DM](/download-ecosystem-tools.md)
