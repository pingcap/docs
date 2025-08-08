---
title: tiup cluster replay
summary: tiup cluster replay` コマンドを使用すると、失敗したクラスター操作を再試行し、正常に実行された手順をスキップできます。指定した監査IDでコマンドを再試行するには、`tiup cluster replay <audit-id>` を使用します。監査IDは ` tiup cluster audit ` コマンドでビュー。出力は、指定した監査IDの結果です。
---

# tiup cluster replay {#tiup-cluster-replay}

アップグレードや再起動などのクラスター操作を実行すると、クラスター環境の問題により操作が失敗する場合があります。操作を再実行するには、最初からすべての手順を実行する必要があります。クラスターが大きい場合、これらの手順の再実行には長い時間がかかります。このような場合は、 `tiup cluster replay`コマンドを使用して失敗したコマンドを再試行し、正常に実行された手順をスキップすることができます。

## 構文 {#syntax}

```shell
tiup cluster replay <audit-id> [flags]
```

-   `<audit-id>` : 再試行するコマンドの`audit-id` 。6 [`tiup cluster audit`](/tiup/tiup-component-cluster-audit.md)を使用すると、履歴コマンドとその`audit-id`番目を表示できます。

## オプション {#option}

### -h, --help {#h-help}

ヘルプ情報を出力します。

## 出力 {#output}

`<audit-id>`に対応するコマンドの出力。

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
