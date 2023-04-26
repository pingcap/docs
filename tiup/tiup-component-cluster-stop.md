---
title: tiup cluster stop
---

# tiup cluster stop {#tiup-cluster-stop}

`tiup cluster stop`コマンドは、指定されたクラスターのすべてのサービスまたは一部のサービスを停止するために使用されます。

> **ノート：**
>
> クラスターのコア サービスが停止すると、クラスターはサービスを提供できなくなります。

## 構文 {#syntax}

```shell
tiup cluster stop <cluster-name> [flags]
```

`<cluster-name>`は、操作するクラスターの名前です。クラスター名を忘れた場合は、 [`tiup cluster list`](/tiup/tiup-component-cluster-list.md)コマンドを使用して確認できます。

## オプション {#options}

### -N, --ノード {#n-node}

-   停止するノードを指定します。このオプションの値は、ノード ID のコンマ区切りリストです。 `tiup cluster display`コマンドで返される[クラスタ ステータス テーブル](/tiup/tiup-component-cluster-display.md)の最初の列からノード ID を取得できます。
-   データ型: `STRINGS`
-   このオプションがコマンドで指定されていない場合、コマンドはデフォルトですべてのノードを停止します。

> **ノート：**
>
> `-R, --role`オプションを同時に指定した場合、 `-N, --node`と`-R, --role`の両方の指定に一致するサービスノードだけが停止されます。

### -R, --role {#r-role}

-   停止するノードの役割を指定します。このオプションの値は、ノードの役割のコンマ区切りリストです。 `tiup cluster display`コマンドによって返される[クラスタ ステータス テーブル](/tiup/tiup-component-cluster-display.md)の 2 列目から、ノードの役割を取得できます。
-   データ型: `STRINGS`
-   このオプションがコマンドで指定されていない場合、コマンドはデフォルトですべての役割を停止します。

> **ノート：**
>
> `-N, --node`オプションを同時に指定した場合、 `-N, --node`と`-R, --role`の両方の指定に一致するサービスノードだけが停止されます。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで無効になっており、値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`渡すか、値を何も渡さないでください。

## 出力 {#output}

サービス停止のログ。

[&lt;&lt; 前のページに戻る - TiUP クラスタコマンド一覧](/tiup/tiup-component-cluster.md#command-list)
