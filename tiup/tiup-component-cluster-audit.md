---
title: tiup cluster audit
---

# tiup cluster audit {#tiup-cluster-audit}

`tiup cluster audit`コマンドは、すべてのクラスターで実行されたコマンドの履歴と各コマンドの実行ログを表示するために使用されます。

## 構文 {#syntax}

```shell
tiup cluster audit [audit-id] [flags]
```

-   `[audit-id]`を入力しない場合、稼働記録一覧表は新しい順に出力されます。最初の列は`audit-id`です。
-   `[audit-id]`を記入すると、指定した`audit-id`の実行ログを確認することになります。

## オプション {#option}

### -h, --help {#h-help}

-   ヘルプ情報を印刷します。
-   データ型: `Boolean`
-   このオプションはデフォルトでは無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加して、値`true`渡すか、値を渡さないことができます。

## 出力 {#outputs}

-   `[audit-id]`を指定した場合、該当する実行ログが出力されます。
-   `[audit-id]`が指定されていない場合は、次のフィールドを含むテーブルが出力されます。
    -   ID: レコードに対応する`audit-id`
    -   時間: レコードに対応するコマンドの実行時間
    -   コマンド: レコードに対応するコマンド

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
