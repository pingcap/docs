---
title: tiup dm scale-in
---

# tiup dm scale-in {#tiup-dm-scale-in}

`tiup dm scale-in`コマンドは、クラスターをスケールインするために使用されます。クラスター内でのスケーリングはサービスをオフラインにすることを意味し、最終的には指定されたノードがクラスターから削除され、残りの関連ファイルが削除されます。

## 構文 {#syntax}

```shell
tiup dm scale-in <cluster-name> [flags]
```

`<cluster-name>` : 操作するクラスターの名前。クラスター名を忘れた場合は、 [クラスタリスト](/tiup/tiup-component-dm-list.md)コマンドで確認できます。

## オプション {#options}

### -N、--node {#n-node}

-   スケールインするノードを指定します。複数のノードをスケールインする必要がある場合は、ノードをカンマで区切ります。
-   データ型: `STRINGS`
-   デフォルト: いいえ。このオプションは必須であり、値は null であってはなりません。

### &#x20;--force {#force}

-   場合によっては、クラスター内の一部のスケールイン ノードがダウンし、SSH 経由でノードに接続して操作できなくなることがあります。現時点では、 `--force`オプションを使用してこれらのノードをクラスターから削除できます。
-   データ型: `BOOLEAN`
-   デフォルト: false。コマンドでこのオプションを指定しない場合、指定したノードは強制的に削除されません。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   デフォルト: false

## 出力 {#output}

スケールインのログ。

[&lt;&lt; 前のページに戻る - TiUP DMコマンド一覧](/tiup/tiup-component-dm.md#command-list)
