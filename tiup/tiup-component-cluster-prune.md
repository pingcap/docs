---
title: tiup cluster prune
summary: クラスターをスケールアウトする際、 TiUP は一部のコンポーネントのサービスを即時に停止したり、データを削除したりしません。データのスケジューリングが完了するまで待ってから、「tiup cluster prune」コマンドを手動で実行してクリーンアップする必要があります。構文は「tiup cluster prune <cluster-name> [flags]」です。オプション「-h, --help」を指定するとヘルプ情報が出力、クリーンアッププロセスのログが出力されます。
---

# tiup cluster prune {#tiup-cluster-prune}

[クラスターのスケーリング](/tiup/tiup-component-cluster-scale-in.md)場合、一部のコンポーネントでは、 TiUP はすぐにサービスを停止したり、データを削除したりしません。データのスケジュール設定が完了するまで待ってから、 `tiup cluster prune`コマンドを手動で実行してクリーンアップする必要があります。

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
