---
title: tiup cluster prune
---

# tiup cluster prune {#tiup-cluster-prune}

[クラスタでのスケーリング](/tiup/tiup-component-cluster-scale-in.md)の場合、一部のコンポーネントでは、TiUPはサービスをすぐに停止したり、データを削除したりしません。データのスケジューリングが完了するのを待ってから、 `tiup cluster prune`コマンドを手動で実行してクリーンアップする必要があります。

## 構文 {#syntax}

```shell
tiup cluster prune <cluster-name> [flags]
```

## オプション {#option}

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型： `BOOLEAN`
-   デフォルト：false

## 出力 {#output}

クリーンアッププロセスのログ。

[&lt;&lt;前のページに戻る-TiUPクラスターコマンドリスト](/tiup/tiup-component-cluster.md#command-list)
