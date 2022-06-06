---
title: tiup cluster disable
---

# tiupクラスタの無効化 {#tiup-cluster-disable}

クラスタサービスが配置されているマシンを再起動すると、クラスタサービスが自動的に有効になります。クラスタサービスの自動有効化を無効にするには、 `tiup cluster disable`コマンドを使用できます。このコマンドは、指定されたノードで`systemctl disable <service>`を実行して、サービスの自動有効化を無効にします。

## 構文 {#syntax}

```shell
tiup cluster disable <cluster-name> [flags]
```

`<cluster-name>` ：サービスの自動有効化を無効にするクラスタ。

## オプション {#options}

### -N、-node {#n-node}

-   サービスの自動有効化を無効にするノードを指定します。このオプションの値は、ノードIDのコンマ区切りのリストです。 [`tiup cluster display`](/tiup/tiup-component-cluster-display.md)コマンドによって返されるクラスタステータステーブルの最初の列からノードIDを取得できます。
-   データ型： `STRINGS`
-   このオプションがコマンドで指定されていない場合、すべてのノードの自動有効化はデフォルトで無効になっています。

> **ノート：**
>
> `-R, --role`オプションを同時に指定すると、 `-N, --node`と`-R, --role`の両方の仕様に一致するサービスの自動有効化が無効になります。

### -R、-role {#r-role}

-   サービスの自動有効化を無効にするロールを指定します。このオプションの値は、ノードの役割のコンマ区切りのリストです。ノードの役割は、 [`tiup cluster display`](/tiup/tiup-component-cluster-display.md)コマンドによって返されるクラスタステータステーブルの2番目の列から取得できます。
-   データ型： `STRINGS`
-   このオプションがコマンドで指定されていない場合、すべての役割の自動有効化はデフォルトで無効になっています。

> **ノート：**
>
> `-N, --node`オプションを同時に指定すると、 `-N, --node`と`-R, --role`の両方の仕様に一致するサービスの自動有効化が無効になります。

### -h、-help {#h-help}

-   ヘルプ情報を出力します。
-   データ型： `BOOLEAN`
-   このオプションはデフォルトで無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加して、 `true`の値を渡すか、値を渡さないようにします。

## 出力 {#output}

tiup-clusterの実行ログ。

[&lt;&lt;前のページに戻る-TiUPClusterコマンドリスト](/tiup/tiup-component-cluster.md#command-list)
