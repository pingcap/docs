---
title: tiup dm replay
summary: tiup dm replay` コマンドを使用すると、失敗したクラスター操作を再試行し、正常に実行された手順をスキップできます。再試行するコマンドの `audit-id` を使用します。これは、`tiup dm audit` コマンドを使用して見つけることができます。これにより、大規模なクラスターで操作を再実行するときに時間を節約できます。
---

# tiup dm replay {#tiup-dm-replay}

アップグレードや再起動などのクラスター操作を実行すると、クラスター環境の問題により操作が失敗する場合があります。操作を再実行する場合は、すべての手順を最初から実行する必要があります。クラスターが大きい場合、これらの手順を再実行すると時間がかかります。この場合、 `tiup dm replay`コマンドを使用して失敗したコマンドを再試行し、正常に実行された手順をスキップできます。

## 構文 {#syntax}

```shell
tiup dm replay <audit-id> [flags]
```

-   `<audit-id>` : 再試行するコマンドの`audit-id` [`tiup dm audit`](/tiup/tiup-component-dm-audit.md)コマンドを使用して、履歴コマンドとその`audit-id`を表示できます。

## オプション {#option}

### -h, --help {#h-help}

ヘルプ情報を出力します。

## 出力 {#output}

`<audit-id>`に対応するコマンドの出力。

[&lt;&lt; 前のページに戻る - TiUP DMコマンドリスト](/tiup/tiup-component-dm.md#command-list)
