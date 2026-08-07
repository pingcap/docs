---
title: TiDB Cloud CLI (ticloud) Quick Start
summary: Learn how to manage {{{ .starter }}} and Essential instances through the ticloud CLI.
---

# TiDB Cloud CLI (ticloud) Quick Start

> **Note:**
>
> `ticloud` is the TiDB Cloud CLI for Essential. tdc does not replace `ticloud` for Essential. For new TiDB Cloud Starter automation and TiDB Cloud Filesystem workflows, use the [`tdc` CLI](/ai/tdc/tdc-overview.md). Continue to use `ticloud` for Essential and for operations that tdc does not provide, such as import, export, and audit-log commands.

TiDB Cloud provides the command-line interface (CLI) [`ticloud`](https://github.com/tidbcloud/tidbcloud-cli) for you to interact with TiDB Cloud Starter and Essential from your terminal with a few lines of commands. For example, you can perform the following operations using `ticloud`:

- Create, delete, and list your {{{ .starter }}} or Essential instances.
- Import data to your {{{ .starter }}} or Essential instances.
- Export data from your {{{ .starter }}} or Essential instances.

> **Note:**
>
> TiDB Cloud CLI is in public preview.

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

> **Note:**
>
> If you use TiUP, you can use `tiup cloud` instead of `ticloud`.

[{{{ .starter }}}](/tidb-cloud/select-cluster-tier.md#starter) is the best way to get started with TiDB Cloud. In this section, you will learn how to create a {{{ .starter }}} instance with TiDB Cloud CLI.

### Create a user profile or log into TiDB Cloud

Before creating a {{{ .starter }}} instance with TiDB Cloud CLI, you need to either create a user profile or log into TiDB Cloud.

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

### Create a {{{ .starter }}} instance

To create a {{{ .starter }}} instance, enter the following command, and then follow the CLI prompts to provide the required information:

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
