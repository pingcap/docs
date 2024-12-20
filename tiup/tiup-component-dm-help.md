---
title: tiup dm help
summary: tiup-dm コマンドライン インターフェイスは、help` コマンドまたは `--help` オプションを使用してアクセスできる豊富なヘルプ情報を提供します。ヘルプにアクセスするための構文は `tiup dm help [command] [flags]` です。ここで、`[command]` はヘルプ情報が必要なコマンドを指定します。`-h` または `--help` オプションはヘルプ情報を出力。出力は、指定されたコマンドまたは `tiup-dm` のヘルプ情報です。
---

# tiup dm help {#tiup-dm-help}

tiup-dm コマンドライン インターフェイスは、ユーザーに豊富なヘルプ情報を提供します。 `help`コマンドまたは`--help`オプションで表示できます。基本的に、 `tiup dm help <command>` `tiup dm <command> --help`に相当します。

## 構文 {#syntax}

```shell
tiup dm help [command] [flags]
```

`[command]` 、ユーザーが表示する必要があるコマンドのヘルプ情報を指定するために使用されます。指定されていない場合は、 `tiup-dm`のヘルプ情報が表示されます。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   デフォルト: false

## 出力 {#output}

`[command]`または`tiup-dm`のヘルプ情報。

[&lt;&lt; 前のページに戻る - TiUP DMコマンドリスト](/tiup/tiup-component-dm.md#command-list)
