---
title: tiup dm help
summary: tiup dmコマンドラインインターフェイスは、豊富なヘルプ情報を提供します。`help`コマンドまたは`--help`オプションを使用して表示できます。基本的に、`tiup dm help <command>`は`tiup dm <command> --help`と同等です。構文は`tiup dm help [command] [flags]`で、`[command]`は必要に応じて指定します。`-h, --help`オプションはヘルプ情報を出力し、デフォルトはfalseです。出力は`[command]`または`tiup-dm`のヘルプ情報です。
---

# tiup dm help {#tiup-dm-help}

tiup-dm コマンドライン インターフェイスは、ユーザーに豊富なヘルプ情報を提供します。 `help`コマンドまたは`--help`オプションを使用して表示できます。基本的に、 `tiup dm help <command>`は`tiup dm <command> --help`と同等です。

## 構文 {#syntax}

```shell
tiup dm help [command] [flags]
```

`[command]`は、ユーザーが表示する必要があるコマンドのヘルプ情報を指定するために使用されます。指定がない場合は、 `tiup-dm`のヘルプ情報が参照されます。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   デフォルト: false

## 出力 {#output}

`[command]`または`tiup-dm`のヘルプ情報。

[&lt;&lt; 前のページに戻る - TiUP DMコマンド一覧](/tiup/tiup-component-dm.md#command-list)
