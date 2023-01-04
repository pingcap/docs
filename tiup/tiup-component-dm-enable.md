---
title: tiup dm enable
---

# tiup dm を有効にする {#tiup-dm-enable}

`tiup dm enable`コマンドは、マシンの再起動後にクラスター サービスの自動有効化を設定するために使用されます。このコマンドは、指定したノードで`systemctl enable <service>`を実行することにより、サービスの自動有効化を有効にします。

## 構文 {#syntax}

```shell
tiup dm enable <cluster-name> [flags]
```

`<cluster-name>`は、サービスの自動有効化を有効にするクラスターです。

## オプション {#options}

### -N, --ノード {#n-node}

-   サービスの自動有効化を有効にするノードを指定します。このオプションの値は、ノード ID のコンマ区切りリストです。ノード ID は、 [`tiup dm display`](/tiup/tiup-component-dm-display.md)コマンドによって返されるクラスター ステータス テーブルの最初の列から取得できます。
-   データ型: `STRINGS`
-   このオプションがコマンドで指定されていない場合、すべてのノードの自動有効化がデフォルトで有効になります。

> **ノート：**
>
> オプション`-R, --role`を同時に指定すると、オプション`-N, --node`と`-R, --role`の両方の指定に一致するサービスの自動有効化が有効になります。

### -R, --role {#r-role}

-   サービスの自動有効化を有効にするロールを指定します。このオプションの値は、ノード ロールのコンマ区切りリストです。 [`tiup dm display`](/tiup/tiup-component-dm-display.md)コマンドで返されるクラスター ステータス テーブルの 2 列目から、ノードの役割を取得できます。
-   データ型: `STRINGS`
-   このオプションがコマンドで指定されていない場合、すべてのロールの自動有効化がデフォルトで有効になります。

> **ノート：**
>
> オプション`-N, --node`を同時に指定すると、オプション`-N, --node`と`-R, --role`の両方の指定に一致するサービスの自動有効化が有効になります。

### -h, --help {#h-help}

ヘルプ情報を出力します。

## 出力 {#output}

tiup-dm の実行ログ。

[&lt;&lt; 前のページに戻る - TiUP DMコマンド一覧](/tiup/tiup-component-dm.md#command-list)
