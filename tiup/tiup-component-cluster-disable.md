---
title: tiup cluster disable
summary: tiup cluster disable` コマンドは、マシンの再起動後にクラスター サービスの自動有効化を無効にするために使用されます。指定されたノードで `systemctl enable <service>` を実行します。オプションには、ノードを指定するための -N とロールを指定するための -R があります。出力はtiup-clusterの実行ログです。
---

# tiup cluster disable {#tiup-cluster-disable}

クラスター サービスが配置されているマシンを再起動すると、クラスター サービスが自動的に有効になります。クラスター サービスの自動有効化を無効にするには、 `tiup cluster disable`コマンドを使用します。このコマンドは、指定されたノードで`systemctl disable <service>`実行して、サービスの自動有効化を無効にします。

## 構文 {#syntax}

```shell
tiup cluster disable <cluster-name> [flags]
```

`<cluster-name>` : サービスの自動有効化を無効にするクラスター。

## オプション {#options}

### -N、--ノード {#n-node}

-   サービスの自動有効化を無効にするノードを指定します。このオプションの値は、ノード ID のコンマ区切りリストです。ノード ID は、 [`tiup cluster display`](/tiup/tiup-component-cluster-display.md)コマンドによって返されるクラスター ステータス テーブルの最初の列から取得できます。
-   データ型: `STRINGS`
-   このオプションがコマンドで指定されていない場合、すべてのノードの自動有効化はデフォルトで無効になります。

> **注記：**
>
> `-R, --role`オプションを同時に指定した場合、 `-N, --node`と`-R, --role`の両方の指定に一致するサービスの自動有効化は無効になります。

### -R, --役割 {#r-role}

-   サービスの自動有効化を無効にするロールを指定します。このオプションの値は、ノード ロールのコンマ区切りリストです[`tiup cluster display`](/tiup/tiup-component-cluster-display.md)コマンドによって返されるクラスター ステータス テーブルの 2 番目の列から、ノードのロールを取得できます。
-   データ型: `STRINGS`
-   このオプションがコマンドで指定されていない場合、すべてのロールの自動有効化はデフォルトで無効になります。

> **注記：**
>
> `-N, --node`オプションを同時に指定した場合、 `-N, --node`と`-R, --role`の両方の指定に一致するサービスの自動有効化は無効になります。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトでは無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`を渡すか、値を渡さないようにします。

## 出力 {#output}

tiup-clusterの実行ログ。

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
