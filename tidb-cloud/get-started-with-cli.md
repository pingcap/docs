---
title: TiDB Cloud CLI Quick Start
Summary: Learn how to manage TiDB Cloud resources through the TiDB Cloud CLI.
---

# TiDB Cloud CLI Quick Start

TiDB Cloud provides a command-line interface (CLI) [`ticloud`](https://github.com/tidbcloud/tidbcloud-cli) for you to interact with TiDB Cloud from your terminal with a few lines of commands. For example, you can easily perform the following operations using `ticloud`:

- Create, delete and list your clusters.
- Import data from S3 or local files to your clusters.

## Prerequisites

- Have a TiDB Cloud account. If you don't have one, [sign up for a free trial](https://tidbcloud.com/free-trial).
- [Create a TiDB API Key](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management).

## Installation

<SimpleTab>
<div label="macOS/linux">

- Install via script (recommended)

    ```shell
    curl https://raw.githubusercontent.com/tidbcloud/tidbcloud-cli/main/install.sh | sh
    ```

- Install via [TiUP](https://tiup.io/)

    ```shell
    tiup install cloud
    ```

- Install Manually
    - Download the pre-compiled binaries from the [releases](https://github.com/tidbcloud/tidbcloud-cli/releases/latest) page and copy to the desired location.

- Install in GitHub action
    - To set up `ticloud` in GitHub Action, use [`setup-tidbcloud-cli`](https://github.com/tidbcloud/setup-tidbcloud-cli).

</div>

<div label="Windows">

- Install Manually
    - Download the pre-compiled binaries from the [releases](https://github.com/tidbcloud/tidbcloud-cli/releases/latest) page and copy to the desired location.

- Install in GitHub action
    - To set up `ticloud` in GitHub Action, use [`setup-tidbcloud-cli`](https://github.com/tidbcloud/setup-tidbcloud-cli).

</div>
</SimpleTab>

## Using the TiDB Cloud CLI

See all available commands by running:

```shell
ticloud --help
```

Verify that you're using the latest version:

```shell
ticloud version
```

If not, update to the latest version:

```shell
ticloud update
```

### Using the TiDB Cloud CLI through TiUP

The TiDB Cloud CLI is also available through [TiUP](https://tiup.io/). It's called `cloud` as a component in TiUP.

See all available commands by running:

```shell
tiup cloud --help
```

Run commands with the `tiup cloud <command>`, for example:

```shell
tiup cloud cluster create
```

Update to the latest version by TiUP:

```shell
tiup update cloud
```

## Quick Start

Here give a quick example on how we create a cluster with TiDB Cloud CLI.

### Configure a user profile

Configure a user profile with your TiDB Cloud API Key.

```shell
ticloud config create
```

<Warning> The config name **MUST NOT** contain '.'</Warning>

### Create a serverless cluster

```shell
ticloud cluster create
```

Now you are done. Check out our [CLI reference](/tidb-cloud/cli-reference.md) to explore all that's possible with TiDB Cloud CLI.

## Feedback

If you have any questions or suggestions, please [file an issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.
