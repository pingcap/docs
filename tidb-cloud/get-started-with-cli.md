---
title: TiDB Cloud CLI Quick Start
summary: Learn how to manage TiDB Cloud resources through the TiDB Cloud CLI.
---

# TiDB Cloud CLI Quick Start

TiDB Cloud provides a command-line interface (CLI) [`ticloud`](https://github.com/tidbcloud/tidbcloud-cli) for you to interact with TiDB Cloud from your terminal with a few lines of commands. For example, you can easily perform the following operations using `ticloud`:

- Create, delete, and list your clusters.
- Import data to your clusters.
- Export data from your clusters.

> **Note:**
>
> TiDB Cloud CLI is in beta.

## Before you begin

- Have a TiDB Cloud account. If you do not have one, [sign up for a free trial](https://tidbcloud.com/free-trial).

## Installation

<SimpleTab>
<div label="macOS/Linux">

For macOS or Linux, you can install `ticloud` using any of the following methods:

- Install via script (recommended)

    ```shell
    curl https://raw.githubusercontent.com/tidbcloud/tidbcloud-cli/main/install.sh | sh
    ```

- Install via [TiUP](https://tiup.io/)

    ```shell
    tiup install cloud
    ```

- Install manually

    Download the pre-compiled binaries from the [releases](https://github.com/tidbcloud/tidbcloud-cli/releases/latest) page and copy them to your desired location for installation.

- Install in GitHub Actions

    To set up `ticloud` in GitHub Action, use [`setup-tidbcloud-cli`](https://github.com/tidbcloud/setup-tidbcloud-cli).

Install the MySQL command-line client if you do not have it. You can install it via your package manager:

- Debian-based distributions:

    ```shell
    sudo apt-get install mysql-client
    ```

- RPM-based distributions:

    ```shell
    sudo yum install mysql
    ```

- macOS:

  ```shell
  brew install mysql-client
  ```

</div>

<div label="Windows">

For Windows, you can install `ticloud` using either of the following methods:

- Install manually

    Download the pre-compiled binaries from the [releases](https://github.com/tidbcloud/tidbcloud-cli/releases/latest) page and copy them to the desired location for installation.

- Install in GitHub Actions

    To set up `ticloud` in GitHub Actions, use [`setup-tidbcloud-cli`](https://github.com/tidbcloud/setup-tidbcloud-cli).

Install the MySQL command-line client if you do not have it. You can refer to the instructions in [MySQL Installer for Windows](https://dev.mysql.com/doc/refman/8.0/en/mysql-installer.html) for the installation. To launch `ticloud connect` on Windows, you need to have the directory containing `mysql.exe` in the PATH environment variable.

</div>
</SimpleTab>

## Quick start

[TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) is the best way to get started with TiDB Cloud. In this section, you will learn how to create a TiDB Serverless cluster with TiDB Cloud CLI.

### Create a user profile or log into TiDB Cloud

Before creating a cluster with TiDB Cloud CLI, you need to either create a user profile or log into TiDB Cloud.

- Create a user profile with your [TiDB Cloud API key](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management):

    ```shell
    ticloud config create
    ```

    > **Warning:**
    >
    > The profile name **MUST NOT** contain `.`.

- Log into TiDB Cloud with authentication:

    ```shell
    ticloud auth login
    ```

    After successful login, an OAuth token will be assigned to the current profile. If no profiles exist, the token will be assigned to a profile named `default`.

> **Note:**
>
> In the preceding two methods, the TiDB Cloud API key takes precedence over the OAuth token. If both are available, the API key will be used.

### Create a TiDB Serverless cluster

To create a TiDB Serverless cluster, enter the following command, and then follow the CLI prompts to provide the required information:

```shell
ticloud serverless create
```

## Use the TiDB Cloud CLI

View all commands available:

```shell
ticloud --help
```

Verify that you are using the latest version:

```shell
ticloud version
```

If not, update to the latest version:

```shell
ticloud update
```

### Use the TiDB Cloud CLI through TiUP

The TiDB Cloud CLI is also available through [TiUP](https://tiup.io/), with the component name as `cloud`.

View all commands available:

```shell
tiup cloud --help
```

Run commands with `tiup cloud <command>`. For example:

```shell
tiup cloud serverless create
```

Update to the latest version by TiUP:

```shell
tiup update cloud
```

## What's next

Check out [CLI reference](/tidb-cloud/cli-reference.md) to explore more features of TiDB Cloud CLI.

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.
