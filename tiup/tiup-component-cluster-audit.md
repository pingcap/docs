---
title: tiup cluster audit
summary: tiup cluster auditコマンドは、すべてのクラスターで実行されたコマンドを履歴と各コマンドの実行ログで表示するために使用されます。[audit-id] が指定されている場合は、対応する実行ログが出力されます。指定されていない場合は、ID、時間、コマンドのフィールドを含むテーブルが逆時系列で出力されます。 -h, --helpオプションはヘルプ情報を出力が、デフォルトでは無効になっています。
---

# tiup cluster audit {#tiup-cluster-audit}

`tiup cluster audit`コマンドは、すべてのクラスターで実行されたコマンドを、各コマンドの履歴と実行ログで表示するために使用されます。

## 構文 {#syntax}

```shell
tiup cluster audit [audit-id] [flags]
```

-   `[audit-id]`記入しない場合は、操作記録表は逆時系列で出力されます。最初の列は`audit-id`です。
-   `[audit-id]`記入した場合は、指定した`audit-id`の実行ログを確認することを意味します。

## オプション {#option}

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `Boolean`
-   このオプションはデフォルトでは無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`を渡すか、値を渡さないようにします。

## 出力 {#outputs}

-   `[audit-id]`指定すると、対応する実行ログが出力されます。
-   `[audit-id]`が指定されていない場合は、次のフィールドを含むテーブルが出力されます。
    -   ID: レコードに対応する`audit-id`
    -   時間: レコードに対応するコマンドの実行時間
    -   コマンド: レコードに対応するコマンド

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
