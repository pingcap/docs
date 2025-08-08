---
title: tiup dm enable
summary: tiup dm enable`コマンドは、マシンの再起動後にクラスタサービスの自動有効化を有効にするために使用されます。このコマンドは、指定されたノードで`systemctl enable <service>`を実行します。オプションには、自動有効化するノードまたはロールの指定が含まれます。出力はtiup-dmの実行ログです。
---

# tiup dm 有効 {#tiup-dm-enable}

`tiup dm enable`コマンドは、マシンの再起動後にクラスタサービスを自動的に有効化するように設定するために使用されます。このコマンドは、指定されたノードで`systemctl enable <service>`実行することで、サービスの自動有効化を有効にします。

## 構文 {#syntax}

```shell
tiup dm enable <cluster-name> [flags]
```

`<cluster-name>`は、サービスの自動有効化を有効にするクラスターです。

## オプション {#options}

### -N, --node {#n-node}

-   サービスの自動有効化を有効にするノードを指定します。このオプションの値は、ノードIDのカンマ区切りのリストです。ノードIDは、 [`tiup dm display`](/tiup/tiup-component-dm-display.md)コマンドで返されるクラスターステータステーブルの最初の列から取得できます。
-   データ型: `STRINGS`
-   コマンドでこのオプションを指定しない場合は、すべてのノードの自動有効化がデフォルトで有効になります。

> **注記：**
>
> `-R, --role`オプションを同時に指定した場合、 `-N, --node`と`-R, --role`両方の指定に一致するサービスの自動有効化が有効になります。

### -R, --role {#r-role}

-   サービスの自動有効化を有効にするロールを指定します。このオプションの値は、ノードロールのコンマ区切りのリストです。ノードのロールは、 [`tiup dm display`](/tiup/tiup-component-dm-display.md)コマンドで返されるクラスターステータステーブルの2列目から取得できます。
-   データ型: `STRINGS`
-   コマンドでこのオプションを指定しない場合は、すべてのロールの自動有効化がデフォルトで有効になります。

> **注記：**
>
> `-N, --node`オプションを同時に指定した場合、 `-N, --node`と`-R, --role`両方の指定に一致するサービスの自動有効化が有効になります。

### -h, --help {#h-help}

ヘルプ情報を出力します。

## 出力 {#output}

tiup-dm の実行ログ。

[&lt;&lt; 前のページに戻る - TiUP DMコマンドリスト](/tiup/tiup-component-dm.md#command-list)
