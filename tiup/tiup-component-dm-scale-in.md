---
title: tiup dm scale-in
---

# tiup dm scale-in {#tiup-dm-scale-in}

`tiup dm scale-in`コマンドは、クラスタでスケーリングするために使用されます。クラスタでのスケーリングとは、サービスをオフラインにすることを意味し、最終的に指定されたノードをクラスタから削除し、残りの関連ファイルを削除します。

## 構文 {#syntax}

```shell
tiup dm scale-in <cluster-name> [flags]
```

`<cluster-name>` : 操作するクラスタの名前。クラスタ名を忘れた場合は、 [クラスタリスト](/tiup/tiup-component-dm-list.md)コマンドで確認できます。

## オプション {#options}

### -N, --ノード {#n-node}

-   スケールインするノードを指定します。複数のノードをスケールインする必要がある場合は、ノードをコンマで区切ります。
-   データ型: `STRINGS`
-   デフォルト: いいえ。このオプションは必須であり、値は null であってはなりません。

### &#x20;--force {#force}

-   場合によっては、クラスタの一部のスケールイン ノードがダウンしており、SSH 経由でノードに接続して操作することができません。この時点で、 `--force`オプションを使用してこれらのノードをクラスタから削除できます。
-   データ型: `BOOLEAN`
-   デフォルト: false。コマンドで本オプションを指定しない場合、指定したノードは強制的に削除されません。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   デフォルト: false

## 出力 {#output}

スケーリングのログ。

[&lt;&lt; 前のページに戻る - TiUP DMコマンド一覧](/tiup/tiup-component-dm.md#command-list)
