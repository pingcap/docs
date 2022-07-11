---
title: tiup cluster start
---

# tiup cluster start {#tiup-cluster-start}

`tiup cluster start`コマンドは、指定されたクラスタのすべてのサービスまたは一部のサービスを開始するために使用されます。

## 構文 {#syntax}

```shell
tiup cluster start <cluster-name> [flags]
```

`<cluster-name>`は、操作するクラスタの名前です。クラスタ名を忘れた場合は、 [`tiup cluster list`](/tiup/tiup-component-cluster-list.md)コマンドで確認できます。

## オプション {#options}

### -N、-node {#n-node}

-   開始するノードを指定します。このオプションの値は、ノードIDのコンマ区切りのリストです。 `tiup cluster display`コマンドによって返された[クラスタステータステーブル](/tiup/tiup-component-cluster-display.md)の最初の列からノードIDを取得できます。
-   データ型： `STRINGS`
-   このオプションがコマンドで指定されていない場合、すべてのノードがデフォルトで開始されます。

> **ノート：**
>
> `-R, --role`オプションを同時に指定すると、 `-N, --node`と`-R, --role`の両方の仕様に一致するサービスノードのみが開始されます。

### -R、-role {#r-role}

-   開始するノードの役割を指定します。このオプションの値は、ノードの役割のコンマ区切りのリストです。 `tiup cluster display`コマンドによって返される[クラスタステータステーブル](/tiup/tiup-component-cluster-display.md)の2番目の列からノードの役割を取得できます。
-   データ型： `STRINGS`
-   このオプションがコマンドで指定されていない場合、すべての役割がデフォルトで開始されます。

> **ノート：**
>
> `-N, --node`オプションを同時に指定すると、 `-N, --node`と`-R, --role`の両方の仕様に一致するサービスノードのみが開始されます。

### -h、-help {#h-help}

-   ヘルプ情報を出力します。
-   データ型： `BOOLEAN`
-   このオプションは、デフォルトで`false`の値で無効になっています。このオプションを有効にするには、このオプションをコマンドに追加し、 `true`の値を渡すか、値を渡さないようにします。

## 出力 {#output}

サービス開始のログ。

[&lt;&lt;前のページに戻る-TiUPクラスターコマンドリスト](/tiup/tiup-component-cluster.md#command-list)
