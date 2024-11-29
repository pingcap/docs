---
title: tiup dm start
summary: tiup dm start コマンドは、指定されたクラスターのサービスを開始するために使用されます。構文は「tiup dm start <cluster-name> [flags]」です。オプションには、ノードを指定する -N/--node、ロールを指定する -R/--role、ヘルプ情報を出力する -h/--help があります。出力は、サービスの開始ログです。
---

# tiup dm スタート {#tiup-dm-start}

`tiup dm start`コマンドは、指定されたクラスターのサービスのすべてまたは一部を開始するために使用されます。

## 構文 {#syntax}

```shell
tiup dm start <cluster-name> [flags]
```

`<cluster-name>` : 操作するクラスターの名前。クラスター名を忘れた場合は、 [クラスターリスト](/tiup/tiup-component-dm-list.md)コマンドで確認できます。

## オプション {#options}

### -N、--ノード {#n-node}

-   起動するノードを指定します。指定しない場合は、すべてのノードが起動されます。このオプションの値は、ノード ID のコンマ区切りリストです。1 [`tiup dm display`](/tiup/tiup-component-dm-display.md)によって返されるクラスター ステータス テーブルの最初の列からノード ID を取得できます。
-   データ型: `STRINGS`
-   コマンドでこのオプションを指定しない場合は、すべてのノードが起動されます。

> **注記：**
>
> `-R, --role`オプションを同時に指定した場合は、 `-N, --node`と`-R, --role`の両方の指定に一致するサービス ノードのみが起動されます。

### -R, --役割 {#r-role}

-   開始するロールを指定します。指定しない場合は、すべてのロールが開始されます。このオプションの値は、ノード ロールのコンマ区切りリストです。1 [`tiup dm display`](/tiup/tiup-component-dm-display.md)によって返されるクラスター ステータス テーブルの 2 番目の列から、ノードのロールを取得できます。
-   データ型: `STRINGS`
-   コマンドでこのオプションを指定しない場合は、すべてのロールが開始されます。

> **注記：**
>
> `-N, --node`オプションを同時に指定した場合は、 `-N, --node`と`-R, --role`の両方の指定に一致するサービス ノードのみが起動されます。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   デフォルト: false

## 出力 {#output}

サービスを開始したログ。

[&lt;&lt; 前のページに戻る - TiUP DMコマンドリスト](/tiup/tiup-component-dm.md#command-list)
