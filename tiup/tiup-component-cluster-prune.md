---
title: tiup cluster prune
---

# tiup cluster prune {#tiup-cluster-prune}

[クラスターでのスケーリング](/tiup/tiup-component-cluster-scale-in.md)の場合、一部のコンポーネントでは、 TiUP はすぐにサービスを停止したり、データを削除したりしません。データのスケジューリングが完了するまで待ってから、 `tiup cluster prune`コマンドを手動で実行してクリーンアップする必要があります。

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

クリーンアップ プロセスのログ。

[&lt;&lt; 前のページに戻る - TiUP クラスタコマンド一覧](/tiup/tiup-component-cluster.md#command-list)
