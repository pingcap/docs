---
title: tiup cluster help
summary: tiup-cluster は、コマンドライン インターフェイスでユーザーにヘルプ情報を提供します。ヘルプ情報にアクセスするには、`help` コマンドまたは `--help` オプションを使用します。特定のコマンドのヘルプ情報を表示するには、`[command]` を指定します。出力は、指定されたコマンドまたはtiup-clusterのヘルプ情報です。
---

# tiup cluster help {#tiup-cluster-help}

tiup-cluster は、コマンドライン インターフェイスでユーザー向けの豊富なヘルプ情報を提供します。 `help`コマンドまたは`--help`オプションで取得できます。 `tiup cluster help <command>`は基本的に`tiup cluster <command> --help`と同じです。

## 構文 {#syntax}

```shell
tiup cluster help [command] [flags]
```

`[command]`は、ユーザーが表示する必要があるコマンドのヘルプ情報を指定するために使用されます。指定されていない場合は、 tiup-clusterのヘルプ情報が表示されます。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   デフォルト: false

## 出力 {#output}

`[command]`またはtiup-clusterのヘルプ情報。

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
