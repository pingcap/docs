---
title: tiup dm enable
---

# ティアップDMを有効にする {#tiup-dm-enable}

`tiup dm enable`コマンドは、マシンの再起動後のクラスター サービスの自動有効化を設定するために使用されます。このコマンドは、指定したノードで`systemctl enable <service>`を実行することでサービスの自動有効化を有効にします。

## 構文 {#syntax}

```shell
tiup dm enable <cluster-name> [flags]
```

`<cluster-name>`は、サービスの自動有効化が有効になるクラスターです。

## オプション {#options}

### -N、--node {#n-node}

-   サービスの自動有効化を有効にするノードを指定します。このオプションの値は、ノード ID のカンマ区切りリストです。ノード ID は、 [`tiup dm display`](/tiup/tiup-component-dm-display.md)コマンドによって返されるクラスター ステータス テーブルの最初の列から取得できます。
-   データ型: `STRINGS`
-   このオプションがコマンドで指定されていない場合、すべてのノードの自動有効化がデフォルトで有効になります。

> **注記：**
>
> `-R, --role`オプションを同時に指定した場合、 `-N, --node`と`-R, --role`の両方の指定に一致するサービスの自動有効化が有効になります。

### -R、--役割 {#r-role}

-   サービスの自動有効化を有効にするロールを指定します。このオプションの値は、ノードの役割のカンマ区切りのリストです。ノードの役割は、 [`tiup dm display`](/tiup/tiup-component-dm-display.md)コマンドによって返されるクラスター状態テーブルの 2 番目の列から取得できます。
-   データ型: `STRINGS`
-   このオプションがコマンドで指定されていない場合、すべての役割の自動有効化がデフォルトで有効になります。

> **注記：**
>
> `-N, --node`オプションを同時に指定した場合、 `-N, --node`と`-R, --role`の両方の指定に一致するサービスの自動有効化が有効になります。

### -h, --help {#h-help}

ヘルプ情報を出力します。

## 出力 {#output}

tiup-dmの実行ログ。

[&lt;&lt; 前のページに戻る - TiUP DMコマンド一覧](/tiup/tiup-component-dm.md#command-list)
