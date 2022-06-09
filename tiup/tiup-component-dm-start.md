---
title: tiup dm start
---

# tiup dm start {#tiup-dm-start}

`tiup dm start`コマンドは、指定されたクラスタのサービスのすべてまたは一部を開始するために使用されます。

## 構文 {#syntax}

```shell
tiup dm start <cluster-name> [flags]
```

`<cluster-name>` ：操作するクラスタの名前。クラスタ名を忘れた場合は、 [クラスタリスト](/tiup/tiup-component-dm-list.md)コマンドで確認できます。

## オプション {#options}

### -N、-node {#n-node}

-   開始するノードを指定します。指定しない場合、すべてのノードが開始されます。このオプションの値は、ノードIDのコンマ区切りのリストです。ノードIDは、 [`tiup dm display`](/tiup/tiup-component-dm-display.md)コマンドによって返されるクラスタステータステーブルの最初の列から取得できます。
-   データ型： `STRINGS`
-   コマンドでこのオプションが指定されていない場合、すべてのノードが開始されます。

> **ノート：**
>
> `-R, --role`オプションを同時に指定すると、 `-N, --node`と`-R, --role`の両方の仕様に一致するサービスノードのみが開始されます。

### -R、-role {#r-role}

-   開始する役割を指定します。指定しない場合、すべての役割が開始されます。このオプションの値は、ノードの役割のコンマ区切りのリストです。ノードの役割は、 [`tiup dm display`](/tiup/tiup-component-dm-display.md)コマンドによって返されるクラスタステータステーブルの2番目の列から取得できます。
-   データ型： `STRINGS`
-   コマンドでこのオプションが指定されていない場合、すべての役割が開始されます。

> **ノート：**
>
> `-N, --node`オプションを同時に指定すると、 `-N, --node`と`-R, --role`の両方の仕様に一致するサービスノードのみが開始されます。

### -h、-help {#h-help}

-   ヘルプ情報を出力します。
-   データ型： `BOOLEAN`
-   デフォルト：false

## 出力 {#output}

サービス開始のログ。

[&lt;&lt;前のページに戻る-TiUPDMコマンドリスト](/tiup/tiup-component-dm.md#command-list)
