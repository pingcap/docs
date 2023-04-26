---
title: Export and Import Data Sources and Task Configuration of Clusters
summary: Learn how to export and import data sources and task configuration of clusters when you use DM.
---

# データ ソースのエクスポートとインポート、およびクラスターのタスクコンフィグレーション {#export-and-import-data-sources-and-task-configuration-of-clusters}

`config`コマンドは、データ ソースとクラスターのタスク構成をエクスポートおよびインポートするために使用されます。

> **ノート：**
>
> v2.0.5 より前のクラスターの場合、dmctl v2.0.5 以降を使用して、データ ソースとタスク構成ファイルをエクスポートおよびインポートできます。

{{< copyable "" >}}

```bash
» help config
Commands to import/export config
Usage:
  dmctl config [command]
Available Commands:
  export      Export the configurations of sources and tasks.
  import      Import the configurations of sources and tasks.
Flags:
  -h, --help   help for config
Global Flags:
  -s, --source strings   MySQL Source ID.
Use "dmctl config [command] --help" for more information about a command.
```

## クラスターのデータ ソースとタスク構成をエクスポートする {#export-the-data-source-and-task-configuration-of-clusters}

`export`コマンドを使用して、クラスターのデータ ソースとタスク構成を指定したファイルにエクスポートできます。

{{< copyable "" >}}

```bash
config export [--dir directory]
```

### パラメータの説明 {#parameter-explanation}

-   `dir` :
    -   オプション
    -   エクスポートするファイル パスを指定します
    -   デフォルト値は`./configs`です

### 返された結果 {#returned-results}

{{< copyable "" >}}

```bash
config export -d /tmp/configs
```

```
export configs to directory `/tmp/configs` succeed
```

## クラスターのデータ ソースとタスク構成をインポートする {#import-the-data-source-and-task-configuration-of-clusters}

`import`コマンドを使用して、指定したファイルからクラスターのデータ ソースとタスク構成をインポートできます。

{{< copyable "" >}}

```bash
config import [--dir directory]
```

> **ノート：**
>
> v2.0.2以降のクラスタでは、現在、Relay Workerに関連する設定の自動インポートはサポートされていません。 `start-relay`コマンドを使用して、手動で[リレーログを開始](/dm/relay-log.md#start-and-stop-the-relay-log-feature)実行できます。

### パラメータの説明 {#parameter-explanation}

-   `dir` :
    -   オプション
    -   インポートするファイル パスを指定します
    -   デフォルト値は`./configs`です

### 返された結果 {#returned-results}

{{< copyable "" >}}

```bash
config import -d /tmp/configs
```

```
start creating sources
start creating tasks
import configs from directory `/tmp/configs` succeed
```
