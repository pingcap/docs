---
title: tiup cluster stop
summary: 「tiup cluster stop」コマンドは、指定されたクラスターのすべてまたは一部のサービスを停止するために使用されます。コアサービスが停止すると、クラスターはサービスを提供できなくなります。コマンド構文は「tiup cluster stop <cluster-name> [flags] 」です。オプションには、停止するノードを指定する -N/--node、停止するノードの役割を指定する -R/--role、ヘルプ情報を表示する -h/--help があります。出力は、サービスの停止に関するログです。
---

# tiup cluster stop {#tiup-cluster-stop}

`tiup cluster stop`コマンドは、指定されたクラスターのすべてのサービスまたは一部のサービスを停止するために使用されます。

> **注記：**
>
> クラスターのコア サービスが停止すると、クラスターはサービスを提供できなくなります。

## 構文 {#syntax}

```shell
tiup cluster stop <cluster-name> [flags]
```

`<cluster-name>`は操作対象のクラスターの名前です。クラスター名を忘れた場合は、 [`tiup cluster list`](/tiup/tiup-component-cluster-list.md)コマンドで確認できます。

## オプション {#options}

### -N, --node {#n-node}

-   停止するノードを指定します。このオプションの値は、ノードIDのカンマ区切りのリストです。ノードIDは、コマンド`tiup cluster display`で返される[クラスターステータステーブル](/tiup/tiup-component-cluster-display.md)の1列目から取得できます。
-   データ型: `STRINGS`
-   このオプションがコマンドで指定されていない場合、コマンドはデフォルトですべてのノードを停止します。

> **注記：**
>
> `-R, --role`オプションを同時に指定した場合は、 `-N, --node`と`-R, --role`両方の指定に一致するサービス ノードのみが停止されます。

### -R, --role {#r-role}

-   停止するノードのロールを指定します。このオプションの値は、ノードのロールをカンマで区切ったリストです。ノードのロールは、 `tiup cluster display`コマンドで返される[クラスターステータステーブル](/tiup/tiup-component-cluster-display.md)の2列目から取得できます。
-   データ型: `STRINGS`
-   コマンドでこのオプションを指定しない場合、コマンドはデフォルトですべてのロールを停止します。

> **注記：**
>
> `-N, --node`オプションを同時に指定した場合は、 `-N, --node`と`-R, --role`両方の指定に一致するサービス ノードのみが停止されます。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで値`false`で無効になっています。このオプションを有効にするには、コマンドにこのオプションを追加し、値`true`を渡すか、値を渡さないでください。

## 出力 {#output}

サービスを停止したログ。

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
