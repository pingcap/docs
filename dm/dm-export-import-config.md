---
title: Export and Import Data Sources and Task Configuration of Clusters
summary: Learn how to export and import data sources and task configuration of clusters when you use DM.
---

# データソースのエクスポートとインポート、およびクラスターのタスクConfiguration / コンフィグレーション {#export-and-import-data-sources-and-task-configuration-of-clusters}

`config`コマンドは、クラスターのデータソースとタスク構成をエクスポートおよびインポートするために使用されます。

> **ノート：**
>
> v2.0.5より前のクラスターの場合、dmctl v2.0.5以降を使用して、データソースおよびタスク構成ファイルをエクスポートおよびインポートできます。

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

## クラスターのデータソースとタスク構成をエクスポートします {#export-the-data-source-and-task-configuration-of-clusters}

`export`のコマンドを使用して、クラスターのデータソースとタスク構成を指定したファイルにエクスポートできます。

{{< copyable "" >}}

```bash
config export [--dir directory]
```

### パラメータの説明 {#parameter-explanation}

-   `dir` ：
    -   オプション
    -   エクスポートするファイルパスを指定します
    -   デフォルト値は`./configs`です

### 返された結果 {#returned-results}

{{< copyable "" >}}

```bash
config export -d /tmp/configs
```

```
export configs to directory `/tmp/configs` succeed
```

## クラスターのデータソースとタスク構成をインポートします {#import-the-data-source-and-task-configuration-of-clusters}

`import`のコマンドを使用して、指定したファイルからクラスターのデータソースとタスク構成をインポートできます。

{{< copyable "" >}}

```bash
config import [--dir directory]
```

> **ノート：**
>
> v2.0.2以降のクラスターの場合、現在、リレーワーカーに関連する構成を自動的にインポートすることはサポートされていません。 `start-relay`のコマンドを使用して手動で[リレーログを開始](/dm/relay-log.md#start-and-stop-the-relay-log-feature)を実行できます。

### パラメータの説明 {#parameter-explanation}

-   `dir` ：
    -   オプション
    -   インポートするファイルパスを指定します
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
