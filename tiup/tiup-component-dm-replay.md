---
title: tiup dm replay
summary: tiup dm replay` コマンドを使用すると、失敗したクラスタ操作を再試行し、正常に実行された手順をスキップできます。再試行するコマンドの `audit-id` を使用してください。このIDは `tiup dm audit` コマンドで確認できます。これにより、大規模クラスタで操作を再実行する際の時間節約に役立ちます。
---

# tiup dm replay {#tiup-dm-replay}

アップグレードや再起動などのクラスター操作を実行すると、クラスター環境の問題により操作が失敗する場合があります。操作を再実行するには、最初からすべての手順を実行する必要があります。クラスターが大きい場合、これらの手順の再実行には長い時間がかかります。このような場合は、 `tiup dm replay`コマンドを使用して失敗したコマンドを再試行し、正常に実行された手順をスキップすることができます。

## 構文 {#syntax}

```shell
tiup dm replay <audit-id> [flags]
```

-   `<audit-id>` : 再試行するコマンドの`audit-id` 。6 [`tiup dm audit`](/tiup/tiup-component-dm-audit.md)を使用すると、履歴コマンドとその`audit-id`番目を表示できます。

## オプション {#option}

### -h, --help {#h-help}

ヘルプ情報を出力します。

## 出力 {#output}

`<audit-id>`に対応するコマンドの出力。

[&lt;&lt; 前のページに戻る - TiUP DMコマンドリスト](/tiup/tiup-component-dm.md#command-list)
