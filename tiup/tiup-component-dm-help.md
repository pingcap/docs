---
title: tiup dm help
summary: tiup-dm コマンドラインインターフェースは豊富なヘルプ情報を提供しており、help` コマンドまたは `--help` オプションを使用してアクセスできます。ヘルプにアクセスするための構文は `tiup dm help [command] [flags]` です。`[command]` には、ヘルプ情報が必要なコマンドを指定します。`-h` または `--help` オプションはヘルプ情報を出力。出力は、指定されたコマンドまたは `tiup-dm` のヘルプ情報です。
---

# tiup dm help {#tiup-dm-help}

tiup-dm コマンドラインインターフェースは、豊富なヘルプ情報を提供します。ヘルプ情報は、コマンド`help`またはオプション`--help`で表示できます。基本的に、 `tiup dm help <command>` `tiup dm <command> --help`に相当します。

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
