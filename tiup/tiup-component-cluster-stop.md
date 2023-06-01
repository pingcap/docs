---
title: tiup cluster stop
---

# tiup cluster stop {#tiup-cluster-stop}

`tiup cluster stop`コマンドは、指定したクラスターのすべてのサービスまたは一部のサービスを停止するために使用されます。

> **ノート：**
>
> クラスターのコア サービスが停止すると、クラスターはサービスを提供できなくなります。

## 構文 {#syntax}

```shell
tiup cluster stop <cluster-name> [flags]
```

`<cluster-name>`は、操作するクラスターの名前です。クラスター名を忘れた場合は、 [<a href="/tiup/tiup-component-cluster-list.md">`tiup cluster list`</a>](/tiup/tiup-component-cluster-list.md)コマンドを使用して確認できます。

## オプション {#options}

### -N、--node {#n-node}

-   停止するノードを指定します。このオプションの値は、ノード ID のカンマ区切りリストです。ノード ID は、 `tiup cluster display`コマンドによって返される[<a href="/tiup/tiup-component-cluster-display.md">クラスタステータステーブル</a>](/tiup/tiup-component-cluster-display.md)の最初の列から取得できます。
-   データ型: `STRINGS`
-   このオプションがコマンドで指定されていない場合、コマンドはデフォルトですべてのノードを停止します。

> **ノート：**
>
> `-R, --role`オプションを同時に指定した場合、 `-N, --node`と`-R, --role`の両方の指定に一致するサービスノードだけが停止されます。

### -R、--役割 {#r-role}

-   停止するノードの役割を指定します。このオプションの値は、ノードの役割のカンマ区切りリストです。 `tiup cluster display`コマンドによって返される[<a href="/tiup/tiup-component-cluster-display.md">クラスタステータステーブル</a>](/tiup/tiup-component-cluster-display.md)の 2 番目の列からノードの役割を取得できます。
-   データ型: `STRINGS`
-   このオプションがコマンドで指定されていない場合、コマンドはデフォルトですべてのロールを停止します。

> **ノート：**
>
> `-N, --node`オプションを同時に指定した場合、 `-N, --node`と`-R, --role`の両方の指定に一致するサービスノードだけが停止されます。

### -h, --help {#h-help}

-   ヘルプ情報を印刷します。
-   データ型: `BOOLEAN`
-   このオプションは、値`false`を指定するとデフォルトで無効になります。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`渡すか、値を渡しません。

## 出力 {#output}

サービスを停止したときのログです。

[<a href="/tiup/tiup-component-cluster.md#command-list">&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト</a>](/tiup/tiup-component-cluster.md#command-list)
