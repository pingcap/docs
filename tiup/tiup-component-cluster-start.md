---
title: tiup cluster start
---

# tiup cluster start {#tiup-cluster-start}

`tiup cluster start`コマンドは、指定されたクラスターのすべてのサービスまたは一部のサービスを開始するために使用されます。

## 構文 {#syntax}

```shell
tiup cluster start <cluster-name> [flags]
```

`<cluster-name>`は、操作するクラスターの名前です。クラスター名を忘れた場合は、 [`tiup cluster list`](/tiup/tiup-component-cluster-list.md)コマンドを使用して確認できます。

## オプション {#options}

### -N, --ノード {#n-node}

-   開始するノードを指定します。このオプションの値は、ノード ID のコンマ区切りリストです。 `tiup cluster display`コマンドで返される[クラスタ ステータス テーブル](/tiup/tiup-component-cluster-display.md)の最初の列からノード ID を取得できます。
-   データ型: `STRINGS`
-   このオプションがコマンドで指定されていない場合、デフォルトですべてのノードが開始されます。

> **ノート：**
>
> `-R, --role`のオプションを同時に指定した場合、 `-N, --node`と`-R, --role`の両方の指定に一致するサービスノードだけが起動されます。

### -R, --role {#r-role}

-   起動するノードの役割を指定します。このオプションの値は、ノードの役割のコンマ区切りリストです。 `tiup cluster display`コマンドによって返される[クラスタ ステータス テーブル](/tiup/tiup-component-cluster-display.md)の 2 列目から、ノードの役割を取得できます。
-   データ型: `STRINGS`
-   このオプションがコマンドで指定されていない場合、すべての役割がデフォルトで開始されます。

> **ノート：**
>
> `-N, --node`のオプションを同時に指定した場合、 `-N, --node`と`-R, --role`の両方の指定に一致するサービスノードだけが起動されます。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで無効になっており、値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`を渡すか、値を何も渡さないでください。

## 出力 {#output}

サービス開始のログ。

[&lt;&lt; 前のページに戻る - TiUP クラスタコマンド一覧](/tiup/tiup-component-cluster.md#command-list)
