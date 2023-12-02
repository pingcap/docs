---
title: tiup cluster help
---

# tiup cluster help {#tiup-cluster-help}

tiup-cluster は、コマンド ライン インターフェイスでユーザーに豊富なヘルプ情報を提供します。 `help`コマンドまたは`--help`オプションで取得できます。 `tiup cluster help <command>`は基本的に`tiup cluster <command> --help`と同等です。

## 構文 {#syntax}

```shell
tiup cluster help [command] [flags]
```

`[command]`は、ユーザーが表示する必要があるコマンドのヘルプ情報を指定するために使用されます。指定しない場合は、 tiup-clusterのヘルプ情報が表示されます。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   デフォルト: false

## 出力 {#output}

`[command]`またはtiup-clusterのヘルプ情報。

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
