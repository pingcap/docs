---
title: tiup dm scale-in
summary: tiup dm scale-inコマンドは、サービスをオフラインにし、指定されたノードをクラスタから削除することで、クラスタをスケールインします。構文は「tiup dm scale-in <cluster-name> [flags]」です。オプションには、ノードの指定、ダウンしているノードの強制削除、ヘルプ情報の表示などを行う -N、 --force、-h があります。出力はスケールインのログです。
---

# tiup dm scale-in {#tiup-dm-scale-in}

`tiup dm scale-in`コマンドはクラスターをスケールインするために使用されます。クラスターをスケールインすると、サービスがオフラインになり、指定されたノードがクラスターから削除され、残りの関連ファイルも削除されます。

## 構文 {#syntax}

```shell
tiup dm scale-in <cluster-name> [flags]
```

`<cluster-name>` : 操作対象のクラスターの名前。クラスター名を忘れた場合は、 [クラスターリスト](/tiup/tiup-component-dm-list.md)コマンドで確認できます。

## オプション {#options}

### -N, --node {#n-node}

-   スケールインするノードを指定します。複数のノードをスケールインする必要がある場合は、カンマで区切ります。
-   データ型: `STRINGS`
-   デフォルト: no。このオプションは必須であり、値は null であってはなりません。

### &#x20;--force {#force}

-   場合によっては、クラスタ内の一部のスケールインノードがダウンし、SSH経由でノードに接続して操作できなくなることがあります。このような場合は、 `--force`オプションを使用してこれらのノードをクラスタから削除できます。
-   データ型: `BOOLEAN`
-   デフォルト：false。このオプションがコマンドで指定されていない場合、指定されたノードは強制的に削除されません。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   デフォルト: false

## 出力 {#output}

スケールインのログ。

[&lt;&lt; 前のページに戻る - TiUP DMコマンドリスト](/tiup/tiup-component-dm.md#command-list)
