---
title: tiup dm scale-in
---

# tiup dm scale-in {#tiup-dm-scale-in}

`tiup dm scale-in`コマンドは、クラスタでスケーリングするために使用されます。クラスタでのスケーリングとは、サービスをオフラインにすることを意味します。これにより、最終的に指定されたノードがクラスタから削除され、残りの関連ファイルが削除されます。

## 構文 {#syntax}

```shell
tiup dm scale-in <cluster-name> [flags]
```

`<cluster-name>` ：操作するクラスタの名前。クラスタ名を忘れた場合は、 [クラスタリスト](/tiup/tiup-component-dm-list.md)コマンドで確認できます。

## オプション {#options}

### -N、-node {#n-node}

-   スケールインするノードを指定します。複数のノードでスケールインする必要がある場合は、それらをコンマで分割します。
-   データ型： `STRINGS`
-   デフォルト：いいえ。このオプションは必須であり、値はnullであってはなりません。

### &#x20;--force {#force}

-   場合によっては、クラスタの一部のスケールインノードがダウンしており、SSHを介してノードに接続して操作することができません。このとき、 `--force`オプションを使用して、これらのノードをクラスタから削除できます。
-   データ型： `BOOLEAN`
-   デフォルト：false。コマンドでこのオプションが指定されていない場合、指定されたノードは強制的に削除されません。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型： `BOOLEAN`
-   デフォルト：false

## 出力 {#output}

のスケーリングのログ。

[&lt;&lt;前のページに戻るTiUP DMコマンドリスト](/tiup/tiup-component-dm.md#command-list)
