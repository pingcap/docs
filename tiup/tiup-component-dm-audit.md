---
title: tiup dm audit
summary: tiup dm audit` コマンドは、すべてのクラスターで実行されたコマンドの履歴と各コマンドの実行ログを表示するために使用されます。 `[audit-id]` が入力されていない場合は、`audit-id`、実行時間、コマンドを示す操作記録のテーブルが逆時系列で出力されます。 `[audit-id]` が入力されている場合は、指定された `audit-id` の実行ログがチェックされます。 `-h, --help` オプションはヘルプ情報を出力。 `[audit-id]` が指定されている場合は、対応する実行ログが出力されます。 指定されていない場合は、ID、時間、コマンドのフィールドを持つテーブルが出力されます。
---

# tiup dm audit {#tiup-dm-audit}

`tiup dm audit`コマンドは、すべてのクラスターで実行された履歴コマンドと各コマンドの実行ログを表示するために使用されます。

## 構文 {#syntax}

```shell
tiup dm audit [audit-id] [flags]
```

-   `[audit-id]`記入しない場合は、操作記録表は逆時系列で出力されます。最初の列は`audit-id`です。
-   `[audit-id]`記入すると、指定した`audit-id`の実行ログがチェックされます。

## オプション {#option}

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   デフォルト: false

## 出力 {#output}

-   `[audit-id]`指定すると、対応する実行ログが出力されます。
-   `[audit-id]`が指定されていない場合は、次のフィールドを含むテーブルが出力されます。
    -   ID: このレコードに対応する`audit-id`
    -   時間: レコードに対応するコマンドの実行時間
    -   コマンド: レコードに対応するコマンド

[&lt;&lt; 前のページに戻る - TiUP DMコマンドリスト](/tiup/tiup-component-dm.md#command-list)
