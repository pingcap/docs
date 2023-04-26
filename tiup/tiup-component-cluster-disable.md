---
title: tiup cluster disable
---

# tiup cluster disable {#tiup-cluster-disable}

クラスタ サービスが配置されているマシンを再起動すると、クラスタ サービスが自動的に有効になります。クラスター サービスの自動有効化を無効にするには、 `tiup cluster disable`コマンドを使用できます。このコマンドは、指定したノードで`systemctl disable <service>`を実行して、サービスの自動有効化を無効にします。

## 構文 {#syntax}

```shell
tiup cluster disable <cluster-name> [flags]
```

`<cluster-name>` : サービスの自動有効化を無効にするクラスター。

## オプション {#options}

### -N, --ノード {#n-node}

-   サービスの自動有効化を無効にするノードを指定します。このオプションの値は、ノード ID のコンマ区切りリストです。ノード ID は、 [`tiup cluster display`](/tiup/tiup-component-cluster-display.md)コマンドによって返されるクラスター ステータス テーブルの最初の列から取得できます。
-   データ型: `STRINGS`
-   このオプションがコマンドで指定されていない場合、すべてのノードの自動有効化はデフォルトで無効になります。

> **ノート：**
>
> オプション`-R, --role`を同時に指定すると、オプション`-N, --node`と`-R, --role`の両方の指定に一致するサービスの自動有効化が無効になります。

### -R, --role {#r-role}

-   サービスの自動有効化を無効にするロールを指定します。このオプションの値は、ノード ロールのコンマ区切りリストです。 [`tiup cluster display`](/tiup/tiup-component-cluster-display.md)コマンドで返されるクラスター ステータス テーブルの 2 列目から、ノードの役割を取得できます。
-   データ型: `STRINGS`
-   このオプションがコマンドで指定されていない場合、すべてのロールの自動有効化はデフォルトで無効になります。

> **ノート：**
>
> オプション`-N, --node`を同時に指定すると、オプション`-N, --node`と`-R, --role`の両方の指定に一致するサービスの自動有効化が無効になります。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加して、値`true`渡すか、値を何も渡さないようにします。

## 出力 {#output}

tiup-clusterの実行ログ。

[&lt;&lt; 前のページに戻る - TiUP クラスタコマンド一覧](/tiup/tiup-component-cluster.md#command-list)
