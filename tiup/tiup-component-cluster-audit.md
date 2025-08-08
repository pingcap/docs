---
title: tiup cluster audit
summary: tiup cluster auditコマンドは、すべてのクラスタで実行されたコマンドの履歴と各コマンドの実行ログを表示します。[audit-id] を指定した場合、対応する実行ログが出力されます。指定しない場合は、ID、時間、コマンドのフィールドを含む表が時系列の逆順に出力されます。 -h, --helpオプションはヘルプ情報を出力、デフォルトでは無効になっています。
---

# tiup cluster audit {#tiup-cluster-audit}

`tiup cluster audit`コマンドは、すべてのクラスターで実行されたコマンドを各コマンドの履歴と実行ログで表示するために使用されます。

## 構文 {#syntax}

```shell
tiup cluster audit [audit-id] [flags]
```

-   `[audit-id]`記入しない場合、操作記録表は逆時系列で出力されます。最初の列は`audit-id`です。
-   `[audit-id]`記入した場合は、指定した`audit-id`の実行ログを確認することを意味します。

## オプション {#option}

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `Boolean`
-   このオプションはデフォルトで無効になっており、デフォルト値は`false`です。このオプションを有効にするには、コマンドにこのオプションを追加し、値`true`を渡すか、値を渡さないかのいずれかを選択します。

## 出力 {#outputs}

-   `[audit-id]`指定した場合、対応する実行ログが出力されます。
-   `[audit-id]`指定しない場合は、次のフィールドを含むテーブルが出力されます。
    -   ID: レコードに対応する`audit-id`
    -   時間: レコードに対応するコマンドの実行時間
    -   コマンド: レコードに対応するコマンド

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
