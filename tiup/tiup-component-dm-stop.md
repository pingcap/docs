---
title: tiup dm stop
---

# tiup dm stop {#tiup-dm-stop}

`tiup dm stop`コマンドは、指定されたクラスタのサービスのすべてまたは一部を停止するために使用されます。

> **ノート：**
>
> コアサービスが停止した後、クラスタはサービスを提供できません。

## 構文 {#syntax}

```shell
tiup dm stop <cluster-name> [flags]
```

`<cluster-name>` ：操作するクラスタの名前。クラスタ名を忘れた場合は、 [クラスタリスト](/tiup/tiup-component-dm-list.md)コマンドで確認できます。

## オプション {#options}

### -N、-node {#n-node}

-   停止するノードを指定します。指定しない場合、すべてのノードが停止します。このオプションの値は、ノードIDのコンマ区切りのリストです。 [`tiup dm display`](/tiup/tiup-component-dm-display.md)コマンドによって返されるクラスタステータステーブルの最初の列からノードIDを取得できます。
-   データ型： `STRINGS`
-   コマンドでこのオプションが指定されていない場合、デフォルトですべてのノードが選択されます。

> **ノート：**
>
> `-R, --role`オプションを同時に指定すると、 `-N, --node`と`-R, --role`の両方の仕様に一致するサービスノードのみが停止します。

### -R、-role {#r-role}

-   停止する役割を指定します。指定しない場合、すべての役割が停止します。このオプションの値は、ノードの役割のコンマ区切りのリストです。ノードの役割は、 [`tiup dm display`](/tiup/tiup-component-dm-display.md)コマンドによって返されるクラスタステータステーブルの2番目の列から取得できます。
-   データ型： `STRINGS`
-   このオプションがコマンドで指定されていない場合、デフォルトですべての役割が選択されます。

> **ノート：**
>
> `-N, --node`オプションを同時に指定すると、 `-N, --node`と`-R, --role`の両方の仕様に一致するサービスノードのみが停止します。

### -h、-help {#h-help}

-   ヘルプ情報を出力します。
-   データ型： `BOOLEAN`
-   デフォルト：false

## 出力 {#output}

サービス停止のログ。

[&lt;&lt;前のページに戻る-TiUPDMコマンドリスト](/tiup/tiup-component-dm.md#command-list)
