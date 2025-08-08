---
title: Export and Import Data Sources and Task Configuration of Clusters
summary: DM を使用するときに、データ ソースとクラスターのタスク構成をエクスポートおよびインポートする方法を学習します。
---

# データソースのエクスポートとインポート、およびクラスターのタスクコンフィグレーション {#export-and-import-data-sources-and-task-configuration-of-clusters}

`config`コマンドは、クラスターのデータ ソースとタスク構成をエクスポートおよびインポートするために使用されます。

> **注記：**
>
> v2.0.5 より前のクラスターの場合は、dmctl (&gt;= v2.0.5 かつ &lt; v8.0.0) を使用して、データ ソースおよびタスク構成ファイルをエクスポートおよびインポートできます。

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

## クラスターのデータソースとタスク構成をエクスポートする {#export-the-data-source-and-task-configuration-of-clusters}

`export`コマンドを使用して、クラスターのデータ ソースとタスク構成を指定されたファイルにエクスポートできます。

```bash
config export [--dir directory]
```

### パラメータの説明 {#parameter-explanation}

-   `dir` :
    -   オプション
    -   エクスポートするファイルパスを指定します
    -   デフォルト値は`./configs`です

### 返された結果 {#returned-results}

```bash
config export -d /tmp/configs
```

    export configs to directory `/tmp/configs` succeed

## クラスターのデータソースとタスク構成をインポートする {#import-the-data-source-and-task-configuration-of-clusters}

`import`コマンドを使用して、指定されたファイルからクラスターのデータ ソースとタスク構成をインポートできます。

```bash
config import [--dir directory]
```

> **注記：**
>
> v2.0.2以降のクラスターでは、現在、リレーワーカー関連の設定の自動インポートはサポートされていません`start-relay`コマンドを使用して手動で[リレーログを開始](/dm/relay-log.md#enable-and-disable-relay-log)実行できます。

### パラメータの説明 {#parameter-explanation}

-   `dir` :
    -   オプション
    -   インポートするファイルパスを指定します
    -   デフォルト値は`./configs`です

### 返された結果 {#returned-results}

```bash
config import -d /tmp/configs
```

    start creating sources
    start creating tasks
    import configs from directory `/tmp/configs` succeed
