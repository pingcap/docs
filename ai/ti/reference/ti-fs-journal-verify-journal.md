---
title: ti fs-journal verify-journal
summary: Filesystem ジャーナルのハッシュチェーンを検証します。
---

# ti fs-journal verify-journal

1 つのジャーナルのハッシュチェーンの整合性を検証します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs-journal verify-journal
  --journal-id <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## オプション {#options}

- `--journal-id <string>`: ジャーナル ID。\[required]
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: Filesystem トークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、このコマンドは選択した Filesystem 用にローカルに保存されているトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- ジャーナルを検証します。

    ```bash
    # Validate the journal's ordered hash chain and integrity metadata.
    ti fs-journal verify-journal --file-system-id <file-system-id> --journal-id jrn-demo
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem Journal CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem-journal.md)