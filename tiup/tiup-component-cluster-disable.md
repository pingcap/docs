---
title: tiup cluster disable
summary: tiup cluster disable`コマンドは、マシンの再起動後にクラスタサービスの自動有効化を無効にするために使用されます。指定されたノードで`systemctl disable <service>`を実行します。オプションには、ノードを指定するための-Nとロールを指定するための-Rがあります。出力はtiup-clusterの実行ログです。
---

# tiup cluster disable {#tiup-cluster-disable}

クラスタサービスが配置されているマシンを再起動すると、クラスタサービスは自動的に有効化されます。クラスタサービスの自動有効化を無効にするには、コマンド`tiup cluster disable`使用します。このコマンドは、指定されたノードでコマンド`systemctl disable <service>`を実行し、サービスの自動有効化を無効にします。

## 構文 {#syntax}

```shell
tiup cluster disable <cluster-name> [flags]
```

`<cluster-name>` : サービスの自動有効化を無効にするクラスター。

## オプション {#options}

### -N, --node {#n-node}

-   サービスの自動有効化を無効にするノードを指定します。このオプションの値は、ノードIDのカンマ区切りのリストです。ノードIDは、 [`tiup cluster display`](/tiup/tiup-component-cluster-display.md)コマンドで返されるクラスタステータステーブルの最初の列から取得できます。
-   データ型: `STRINGS`
-   このオプションがコマンドで指定されていない場合、すべてのノードの自動有効化はデフォルトで無効になります。

> **注記：**
>
> `-R, --role`オプションを同時に指定した場合、 `-N, --node`と`-R, --role`両方の指定に一致するサービスの自動有効化は無効になります。

### -R, --role {#r-role}

-   サービスの自動有効化を無効にするロールを指定します。このオプションの値は、ノードロールのコンマ区切りのリストです。ノードのロールは、 [`tiup cluster display`](/tiup/tiup-component-cluster-display.md)コマンドで返されるクラスターステータステーブルの2列目から取得できます。
-   データ型: `STRINGS`
-   コマンドでこのオプションを指定しない場合、すべてのロールの自動有効化はデフォルトで無効になります。

> **注記：**
>
> `-N, --node`オプションを同時に指定した場合、 `-N, --node`と`-R, --role`両方の指定に一致するサービスの自動有効化は無効になります。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで無効になっており、デフォルト値は`false`です。このオプションを有効にするには、コマンドにこのオプションを追加し、値`true`を渡すか、値を渡さないかのいずれかを選択します。

## 出力 {#output}

tiup-clusterの実行ログ。

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
