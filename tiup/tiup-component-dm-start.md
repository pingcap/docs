---
title: tiup dm start
---

# ティアップDM開始 {#tiup-dm-start}

`tiup dm start`コマンドは、指定したクラスターのサービスのすべてまたは一部を開始するために使用されます。

## 構文 {#syntax}

```shell
tiup dm start <cluster-name> [flags]
```

`<cluster-name>` : 操作するクラスターの名前。クラスター名を忘れた場合は、 [クラスタリスト](/tiup/tiup-component-dm-list.md)コマンドで確認できます。

## オプション {#options}

### -N、--node {#n-node}

-   起動するノードを指定します。指定しない場合は、すべてのノードが開始されます。このオプションの値は、ノード ID のカンマ区切りリストです。ノード ID は、 [`tiup dm display`](/tiup/tiup-component-dm-display.md)コマンドによって返されるクラスター ステータス テーブルの最初の列から取得できます。
-   データ型: `STRINGS`
-   コマンドでこのオプションを指定しない場合は、すべてのノードが起動されます。

> **注記：**
>
> `-R, --role`オプションを同時に指定した場合は、 `-N, --node`と`-R, --role`の両方の指定に一致するサービスノードだけが起動されます。

### -R、--役割 {#r-role}

-   開始するロールを指定します。指定しない場合、すべてのロールが開始されます。このオプションの値は、ノードの役割のカンマ区切りのリストです。ノードの役割は、 [`tiup dm display`](/tiup/tiup-component-dm-display.md)コマンドによって返されるクラスター状態テーブルの 2 番目の列から取得できます。
-   データ型: `STRINGS`
-   このオプションがコマンドで指定されていない場合は、すべてのロールが開始されます。

> **注記：**
>
> `-N, --node`オプションを同時に指定した場合は、 `-N, --node`と`-R, --role`の両方の指定に一致するサービスノードだけが起動されます。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   デフォルト: false

## 出力 {#output}

サービスを開始したときのログです。

[&lt;&lt; 前のページに戻る - TiUP DMコマンド一覧](/tiup/tiup-component-dm.md#command-list)
