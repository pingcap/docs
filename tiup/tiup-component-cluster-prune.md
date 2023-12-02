---
title: tiup cluster prune
---

# tiup cluster prune {#tiup-cluster-prune}

[クラスター内のスケーリング](/tiup/tiup-component-cluster-scale-in.md)の場合、一部のコンポーネントでは、 TiUP はサービスをすぐに停止したり、データを削除したりしません。データのスケジュール設定が完了するまで待ってから、手動で`tiup cluster prune`コマンドを実行してクリーンアップする必要があります。

## 構文 {#syntax}

```shell
tiup cluster prune <cluster-name> [flags]
```

## オプション {#option}

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   デフォルト: false

## 出力 {#output}

クリーンアッププロセスのログ。

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
