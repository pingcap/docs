---
title: tiup dm audit
---

# tiupdm監査 {#tiup-dm-audit}

`tiup dm audit`コマンドは、すべてのクラスターで実行された履歴コマンドと各コマンドの実行ログを表示するために使用されます。

## 構文 {#syntax}

```shell
tiup dm audit [audit-id] [flags]
```

-   `[audit-id]`を入力しないと、操作レコードの表が新しい順に出力されます。最初の列は`audit-id`です。
-   `[audit-id]`を入力すると、指定した`audit-id`の実行ログがチェックされます。

## オプション {#option}

### -h、-help {#h-help}

-   ヘルプ情報を出力します。
-   データ型： `BOOLEAN`
-   デフォルト：false

## 出力 {#output}

-   `[audit-id]`を指定すると、対応する実行ログが出力されます。
-   `[audit-id]`が指定されていない場合、次のフィールドを持つテーブルが出力されます。
    -   ID：このレコードに対応する`audit-id`
    -   時間：レコードに対応するコマンドの実行時間
    -   コマンド：レコードに対応するコマンド

[&lt;&lt;前のページに戻る-TiUPDMコマンドリスト](/tiup/tiup-component-dm.md#command-list)
