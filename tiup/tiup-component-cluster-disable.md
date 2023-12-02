---
title: tiup cluster disable
---

# tiup cluster disable {#tiup-cluster-disable}

クラスター サービスが配置されているマシンを再起動すると、クラスター サービスは自動的に有効になります。クラスター サービスの自動有効化を無効にするには、 `tiup cluster disable`コマンドを使用します。このコマンドは、指定されたノード上で`systemctl disable <service>`を実行して、サービスの自動有効化を無効にします。

## 構文 {#syntax}

```shell
tiup cluster disable <cluster-name> [flags]
```

`<cluster-name>` : サービスの自動有効化を無効にするクラスター。

## オプション {#options}

### -N、--node {#n-node}

-   サービスの自動有効化を無効にするノードを指定します。このオプションの値は、ノード ID のカンマ区切りリストです。ノード ID は、 [`tiup cluster display`](/tiup/tiup-component-cluster-display.md)コマンドによって返されるクラスター ステータス テーブルの最初の列から取得できます。
-   データ型: `STRINGS`
-   このオプションがコマンドで指定されていない場合、すべてのノードの自動有効化はデフォルトで無効になります。

> **注記：**
>
> `-R, --role`オプションを同時に指定した場合、 `-N, --node`と`-R, --role`の両方の指定に一致するサービスの自動有効化は無効になります。

### -R、--役割 {#r-role}

-   サービスの自動有効化を無効にするロールを指定します。このオプションの値は、ノードの役割のカンマ区切りのリストです。ノードの役割は、 [`tiup cluster display`](/tiup/tiup-component-cluster-display.md)コマンドによって返されるクラスター状態テーブルの 2 番目の列から取得できます。
-   データ型: `STRINGS`
-   このオプションがコマンドで指定されていない場合、すべてのロールの自動有効化はデフォルトで無効になります。

> **注記：**
>
> `-N, --node`オプションを同時に指定した場合、 `-N, --node`と`-R, --role`の両方の指定に一致するサービスの自動有効化は無効になります。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトでは無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加して、値`true`渡すか、値を渡さないことができます。

## 出力 {#output}

tiup-clusterの実行ログ。

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
