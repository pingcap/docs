---
title: tiup dm replay
summary: クラスター操作の失敗を回避するために、tiup dm replayコマンドを使用して失敗したコマンドを再試行し、正常に実行された手順をスキップできます。tiup dm replay <audit-id>コマンドを使用し、<audit-id>に対応するコマンドの出力を表示します。操作の再実行による時間の節約が可能です。
---

# tiup dm replay {#tiup-dm-replay}

アップグレードや再起動などのクラスター操作を実行すると、クラスター環境の問題により操作が失敗する可能性があります。再度操作を行う場合は、すべての手順を最初から行う必要があります。クラスターが大きい場合、これらの手順を再実行すると時間がかかります。この場合、 `tiup dm replay`コマンドを使用して失敗したコマンドを再試行し、正常に実行された手順をスキップできます。

## 構文 {#syntax}

```shell
tiup dm replay <audit-id> [flags]
```

-   `<audit-id>` : 再試行するコマンドの`audit-id` 。 [`tiup dm audit`](/tiup/tiup-component-dm-audit.md)コマンドを使用すると、履歴コマンドとその`audit-id`を表示できます。

## オプション {#option}

### -h, --help {#h-help}

ヘルプ情報を出力します。

## 出力 {#output}

`<audit-id>`に対応するコマンドの出力。

[&lt;&lt; 前のページに戻る - TiUP DMコマンド一覧](/tiup/tiup-component-dm.md#command-list)
