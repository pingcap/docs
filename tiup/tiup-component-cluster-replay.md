---
title: tiup cluster replay
summary: tiup cluster replayコマンドを使用すると、クラスター操作の失敗したコマンドを再試行し、正常に実行された手順をスキップできます。再試行するコマンドのaudit-idはtiup cluster auditコマンドで確認できます。操作が失敗した場合、再実行する手順を最初から行う必要がありますが、tiup cluster replayコマンドを使用すると時間を節約できます。
---

# tiup cluster replay {#tiup-cluster-replay}

アップグレードや再起動などのクラスター操作を実行すると、クラスター環境の問題により操作が失敗する可能性があります。再度操作を行う場合は、すべての手順を最初から行う必要があります。クラスターが大きい場合、これらの手順を再実行すると時間がかかります。この場合、 `tiup cluster replay`コマンドを使用して失敗したコマンドを再試行し、正常に実行された手順をスキップできます。

## 構文 {#syntax}

```shell
tiup cluster replay <audit-id> [flags]
```

-   `<audit-id>` : 再試行するコマンドの`audit-id` 。 [`tiup cluster audit`](/tiup/tiup-component-cluster-audit.md)コマンドを使用すると、履歴コマンドとその`audit-id`を表示できます。

## オプション {#option}

### -h, --help {#h-help}

ヘルプ情報を出力します。

## 出力 {#output}

`<audit-id>`に対応するコマンドの出力。

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
