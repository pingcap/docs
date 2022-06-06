---
title: tiup dm enable
---

# tiup dm enable {#tiup-dm-enable}

`tiup dm enable`コマンドは、マシンの再起動後にクラスタサービスの自動有効化を設定するために使用されます。このコマンドは、指定されたノードで`systemctl enable <service>`を実行することにより、サービスの自動有効化を有効にします。

## 構文 {#syntax}

```shell
tiup dm enable <cluster-name> [flags]
```

`<cluster-name>`は、サービスの自動有効化を有効にするクラスタです。

## オプション {#options}

### -N、-node {#n-node}

-   サービスの自動有効化を有効にするノードを指定します。このオプションの値は、ノードIDのコンマ区切りのリストです。 [`tiup dm display`](/tiup/tiup-component-dm-display.md)コマンドによって返されるクラスタステータステーブルの最初の列からノードIDを取得できます。
-   データ型： `STRINGS`
-   このオプションがコマンドで指定されていない場合、すべてのノードの自動有効化がデフォルトで有効になっています。

> **ノート：**
>
> `-R, --role`オプションを同時に指定すると、 `-N, --node`と`-R, --role`の両方の仕様に一致するサービスの自動有効化が有効になります。

### -R、-role {#r-role}

-   サービスの自動有効化を有効にするロールを指定します。このオプションの値は、ノードの役割のコンマ区切りのリストです。ノードの役割は、 [`tiup dm display`](/tiup/tiup-component-dm-display.md)コマンドによって返されるクラスタステータステーブルの2番目の列から取得できます。
-   データ型： `STRINGS`
-   このオプションがコマンドで指定されていない場合、すべての役割の自動有効化がデフォルトで有効になっています。

> **ノート：**
>
> `-N, --node`オプションを同時に指定すると、 `-N, --node`と`-R, --role`の両方の仕様に一致するサービスの自動有効化が有効になります。

### -h、-help {#h-help}

ヘルプ情報を出力します。

## 出力 {#output}

tiup-dmの実行ログ。

[&lt;&lt;前のページに戻る-TiUPDMコマンドリスト](/tiup/tiup-component-dm.md#command-list)
