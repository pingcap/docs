---
title: tiup dm enable
summary: tiup dm enable コマンドは、マシンの再起動後にクラスター サービスの自動有効化を有効にするために使用されます。指定されたノードで `systemctl enable <service>` を実行します。オプションには、自動有効化するノードまたはロールの指定が含まれます。出力は tiup-dm の実行ログです。
---

# tiup dm 有効 {#tiup-dm-enable}

`tiup dm enable`コマンドは、マシンの再起動後にクラスター サービスの自動有効化を設定するために使用されます。このコマンドは、指定されたノードで`systemctl enable <service>`を実行することで、サービスの自動有効化を有効にします。

## 構文 {#syntax}

```shell
tiup dm enable <cluster-name> [flags]
```

`<cluster-name>`は、サービスの自動有効化を有効にするクラスターです。

## オプション {#options}

### -N、--ノード {#n-node}

-   サービスの自動有効化を有効にするノードを指定します。このオプションの値は、ノード ID のコンマ区切りリストです。ノード ID は、 [`tiup dm display`](/tiup/tiup-component-dm-display.md)コマンドによって返されるクラスター ステータス テーブルの最初の列から取得できます。
-   データ型: `STRINGS`
-   このオプションがコマンドで指定されていない場合、すべてのノードの自動有効化がデフォルトで有効になります。

> **注記：**
>
> `-R, --role`オプションを同時に指定した場合、 `-N, --node`と`-R, --role`の両方の指定に一致するサービスの自動有効化が有効になります。

### -R, --役割 {#r-role}

-   サービスの自動有効化を有効にするロールを指定します。このオプションの値は、ノード ロールのコンマ区切りリストです。1 コマンドによって返されるクラスター ステータス テーブルの 2 番目の列からノード[`tiup dm display`](/tiup/tiup-component-dm-display.md)ロールを取得できます。
-   データ型: `STRINGS`
-   コマンドでこのオプションが指定されていない場合、すべてのロールの自動有効化がデフォルトで有効になります。

> **注記：**
>
> `-N, --node`オプションを同時に指定した場合、 `-N, --node`と`-R, --role`の両方の指定に一致するサービスの自動有効化が有効になります。

### -h, --help {#h-help}

ヘルプ情報を出力します。

## 出力 {#output}

tiup-dm の実行ログ。

[&lt;&lt; 前のページに戻る - TiUP DMコマンドリスト](/tiup/tiup-component-dm.md#command-list)
