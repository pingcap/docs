---
title: tiup cluster stop
summary: 「tiup cluster stop」コマンドは、指定されたクラスターのすべてのサービスまたは一部のサービスを停止するために使用されます。コア サービスが停止すると、クラスターはサービスを提供できなくなります。コマンド構文は、「tiup cluster stop <cluster-name> [flags] 」です。オプションには、停止するノードを指定する -N/--node、停止するノードのロールを指定する -R/--role、ヘルプ情報を出力する -h/--help があります。出力は、サービスの停止のログです。
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

`<cluster-name>`操作対象となるクラスターの名前です。クラスター名を忘れた場合は、 [`tiup cluster list`](/tiup/tiup-component-cluster-list.md)コマンドで確認できます。

## オプション {#options}

### -N、--ノード {#n-node}

-   停止するノードを指定します。このオプションの値は、ノード ID のコンマ区切りリストです。ノード ID は、 `tiup cluster display`コマンドによって返される[クラスターステータステーブル](/tiup/tiup-component-cluster-display.md)の最初の列から取得できます。
-   データ型: `STRINGS`
-   コマンドでこのオプションが指定されていない場合、コマンドはデフォルトですべてのノードを停止します。

> **注記：**
>
> `-R, --role`オプションを同時に指定した場合は、 `-N, --node`と`-R, --role`の両方の指定に一致するサービス ノードのみが停止されます。

### -R, --役割 {#r-role}

-   停止するノードのロールを指定します。このオプションの値は、ノードのロールのコンマ区切りリストです。ノードのロールは、 `tiup cluster display`コマンドによって返される[クラスターステータステーブル](/tiup/tiup-component-cluster-display.md)の 2 番目の列から取得できます。
-   データ型: `STRINGS`
-   コマンドでこのオプションが指定されていない場合、コマンドはデフォルトですべてのロールを停止します。

> **注記：**
>
> `-N, --node`オプションを同時に指定した場合は、 `-N, --node`と`-R, --role`の両方の指定に一致するサービス ノードのみが停止されます。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションは、デフォルトで値`false`で無効になっています。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`を渡すか、値を渡さないようにする必要があります。

## 出力 {#output}

サービスの停止のログ。

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
