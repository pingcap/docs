---
title: tiup cluster enable
---

# tiup cluster enable {#tiup-cluster-enable}

`tiup cluster enable`コマンドは、マシンの再起動後のクラスター サービスの自動有効化を設定するために使用されます。このコマンドは、指定したノードで`systemctl enable <service>`を実行することでサービスの自動有効化を有効にします。

> **ノート：**
>
> すべてのクラスターがシャットダウンして再起動されると、サービスの起動順序はノードのオペレーティング システムの起動順序によって決まります。再起動の順序が正しくないと、場合によっては、再起動されたクラスターが依然としてサービスを提供できないことがあります。たとえば、TiKV が最初に開始されても PD が開始されていない場合、PD が見つからない間に TiKV が複数回再起動されると、systemd はあきらめます)。

## 構文 {#syntax}

```shell
tiup cluster enable <cluster-name> [flags]
```

`<cluster-name>` : サービスの自動有効化が有効になるクラスター。

## オプション {#options}

### -N、--node {#n-node}

-   サービスの自動有効化を有効にするノードを指定します。このオプションの値は、ノード ID のカンマ区切りリストです。ノード ID は、 [<a href="/tiup/tiup-component-cluster-display.md">`tiup cluster display`</a>](/tiup/tiup-component-cluster-display.md)コマンドによって返されるクラスター ステータス テーブルの最初の列から取得できます。
-   データ型: `STRINGS`
-   このオプションがコマンドで指定されていない場合、すべてのノードの自動有効化がデフォルトで有効になります。

> **ノート：**
>
> `-R, --role`オプションを同時に指定した場合、 `-N, --node`と`-R, --role`の両方の指定に一致するサービスの自動有効化が有効になります。

### -R、--役割 {#r-role}

-   サービスの自動有効化を有効にするロールを指定します。このオプションの値は、ノードの役割のカンマ区切りのリストです。ノードの役割は、 [<a href="/tiup/tiup-component-cluster-display.md">`tiup cluster display`</a>](/tiup/tiup-component-cluster-display.md)コマンドによって返されるクラスター状態テーブルの 2 番目の列から取得できます。
-   データ型: `STRINGS`
-   このオプションがコマンドで指定されていない場合、すべての役割の自動有効化がデフォルトで有効になります。

> **ノート：**
>
> `-N, --node`オプションを同時に指定した場合、 `-N, --node`と`-R, --role`の両方の指定に一致するサービスの自動有効化が有効になります。

### -h, --help {#h-help}

-   ヘルプ情報を印刷します。
-   データ型: `BOOLEAN`
-   このオプションは、値`false`を指定するとデフォルトで無効になります。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`渡すか、値を渡しません。

## 出力 {#output}

tiup-clusterの実行ログ。

[<a href="/tiup/tiup-component-cluster.md#command-list">&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト</a>](/tiup/tiup-component-cluster.md#command-list)
