---
title: tiup dm help
---

# tiup dm help {#tiup-dm-help}

tiup-dmコマンドラインインターフェイスは、ユーザーに豊富なヘルプ情報を提供します。 `help`コマンドまたは`--help`オプションで表示できます。基本的に、 `tiup dm help <command>`は`tiup dm <command> --help`に相当します。

## 構文 {#syntax}

```shell
tiup dm help [command] [flags]
```

`[command]`は、ユーザーが表示する必要のあるコマンドのヘルプ情報を指定するために使用されます。指定しない場合は、 `tiup-dm`のヘルプ情報が表示されます。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型： `BOOLEAN`
-   デフォルト：false

## 出力 {#output}

`[command]`または`tiup-dm`のヘルプ情報。

[&lt;&lt;前のページに戻るTiUP DMコマンドリスト](/tiup/tiup-component-dm.md#command-list)
