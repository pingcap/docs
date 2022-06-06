---
title: tiup cluster replay
---

# tiupクラスタの再生 {#tiup-cluster-replay}

アップグレードや再起動などのクラスタ操作を実行すると、クラスタ環境の問題により操作が失敗する場合があります。操作を再実行する場合は、最初からすべての手順を実行する必要があります。クラスタが大きい場合、これらの手順の再実行には長い時間がかかります。この場合、 `tiup cluster replay`コマンドを使用して、失敗したコマンドを再試行し、正常に実行された手順をスキップできます。

## 構文 {#syntax}

```shell
tiup cluster replay <audit-id> [flags]
```

-   `<audit-id>` ：再試行するコマンドの`audit-id` 。 [`tiup cluster audit`](/tiup/tiup-component-cluster-audit.md)コマンドを使用して、履歴コマンドとその`audit-id`を表示できます。

## オプション {#option}

### -h、-help {#h-help}

ヘルプ情報を出力します。

## 出力 {#output}

`<audit-id>`に対応するコマンドの出力。

[&lt;&lt;前のページに戻る-TiUPClusterコマンドリスト](/tiup/tiup-component-cluster.md#command-list)
