---
title: tiup dm start
---

# tiup dm 開始 {#tiup-dm-start}

`tiup dm start`コマンドは、指定されたクラスターのサービスのすべてまたは一部を開始するために使用されます。

## 構文 {#syntax}

```shell
tiup dm start <cluster-name> [flags]
```

`<cluster-name>` : 操作するクラスターの名前。クラスター名を忘れた場合は、 [クラスタ リスト](/tiup/tiup-component-dm-list.md)コマンドで確認できます。

## オプション {#options}

### -N, --ノード {#n-node}

-   開始するノードを指定します。指定しない場合、すべてのノードが開始されます。このオプションの値は、ノード ID のコンマ区切りリストです。ノード ID は、 [`tiup dm display`](/tiup/tiup-component-dm-display.md)コマンドによって返されるクラスター ステータス テーブルの最初の列から取得できます。
-   データ型: `STRINGS`
-   このオプションがコマンドで指定されていない場合、すべてのノードが開始されます。

> **ノート：**
>
> `-R, --role`オプションを同時に指定した場合、 `-N, --node`と`-R, --role`の両方の指定に一致するサービスノードだけが起動されます。

### -R, --role {#r-role}

-   開始するロールを指定します。指定しない場合、すべてのロールが開始されます。このオプションの値は、ノード ロールのコンマ区切りリストです。 [`tiup dm display`](/tiup/tiup-component-dm-display.md)コマンドで返されるクラスター ステータス テーブルの 2 列目から、ノードの役割を取得できます。
-   データ型: `STRINGS`
-   このオプションがコマンドで指定されていない場合、すべての役割が開始されます。

> **ノート：**
>
> `-N, --node`オプションを同時に指定した場合、 `-N, --node`と`-R, --role`の両方の指定に一致するサービスノードだけが起動されます。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   デフォルト: false

## 出力 {#output}

サービス開始のログ。

[&lt;&lt; 前のページに戻る - TiUP DMコマンド一覧](/tiup/tiup-component-dm.md#command-list)
