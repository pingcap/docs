---
title: tiup dm start
summary: tiup dm start コマンドは、指定されたクラスタのサービスを起動するために使用されます。構文は「tiup dm start <cluster-name> [flags]」です。オプションには、ノードを指定する -N/--node、ロールを指定する -R/--role、ヘルプ情報を表示する -h/--help があります。出力はサービス起動のログです。
---

# tiup dm スタート {#tiup-dm-start}

`tiup dm start`コマンドは、指定されたクラスターのサービスのすべてまたは一部を開始するために使用されます。

## 構文 {#syntax}

```shell
tiup dm start <cluster-name> [flags]
```

`<cluster-name>` : 操作対象のクラスターの名前。クラスター名を忘れた場合は、 [クラスターリスト](/tiup/tiup-component-dm-list.md)コマンドで確認できます。

## オプション {#options}

### -N, --node {#n-node}

-   起動するノードを指定します。指定しない場合は、すべてのノードが起動されます。このオプションの値は、ノードIDのカンマ区切りのリストです。ノードIDは、 [`tiup dm display`](/tiup/tiup-component-dm-display.md)コマンドで返されるクラスターステータステーブルの最初の列から取得できます。
-   データ型: `STRINGS`
-   コマンドでこのオプションを指定しない場合は、すべてのノードが起動されます。

> **注記：**
>
> `-R, --role`オプションを同時に指定した場合は、 `-N, --node`と`-R, --role`両方の指定に一致するサービス ノードのみが起動されます。

### -R, --role {#r-role}

-   起動するロールを指定します。指定しない場合は、すべてのロールが起動されます。このオプションの値は、ノードロールのコンマ区切りのリストです。ノードのロールは、 [`tiup dm display`](/tiup/tiup-component-dm-display.md)コマンドで返されるクラスターステータステーブルの2列目から取得できます。
-   データ型: `STRINGS`
-   コマンドでこのオプションを指定しない場合は、すべてのロールが開始されます。

> **注記：**
>
> `-N, --node`オプションを同時に指定した場合は、 `-N, --node`と`-R, --role`両方の指定に一致するサービス ノードのみが起動されます。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   デフォルト: false

## 出力 {#output}

サービスを開始したログ。

[&lt;&lt; 前のページに戻る - TiUP DMコマンドリスト](/tiup/tiup-component-dm.md#command-list)
