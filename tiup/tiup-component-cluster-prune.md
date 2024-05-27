---
title: tiup cluster prune
summary: クラスターをスケーリングする場合、 TiUP はすぐにサービスを停止したり、一部のコンポーネントのデータを削除したりしません。データのスケジュールが完了するまで待ってから、手動で「tiup cluster prune」コマンドを実行してクリーンアップする必要があります。構文は「tiup cluster prune <cluster-name> [flags]」です。オプション「-h, --help」はヘルプ情報を出力、出力はクリーンアップ プロセスのログです。
---

# tiup cluster prune {#tiup-cluster-prune}

[クラスターのスケーリング](/tiup/tiup-component-cluster-scale-in.md)場合、一部のコンポーネントでは、 TiUP はすぐにサービスを停止したり、データを削除したりしません。データのスケジュールが完了するまで待ってから、 `tiup cluster prune`コマンドを手動で実行してクリーンアップする必要があります。

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

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
