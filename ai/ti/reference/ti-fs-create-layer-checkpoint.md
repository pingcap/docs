---
title: ti fs create-layer-checkpoint
summary: TiDB Cloud Filesystem のレイヤーにチェックポイントを作成します。
---

# ti fs create-layer-checkpoint

1 つのレイヤーにチェックポイントを作成します。`--checkpoint-id` を省略した場合、サービスが自動的に生成します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs create-layer-checkpoint
  --layer-id <string>
  [--checkpoint-id <string>]
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--label <string>]
  [--version]
```

## オプション {#options}

- `--layer-id <string>`: レイヤーを識別するレイヤー ID です。\[required]
- `--checkpoint-id <string>`: チェックポイント ID です。通常はサービスによって自動生成されます。
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: Filesystem トークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、このコマンドは選択した Filesystem 用にローカルに保存されているトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--label <string>`: チェックポイントのラベルです。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- 名前付きチェックポイントを作成します。

    ```bash
    # Record the current layer state under a stable checkpoint ID.
    ti fs create-layer-checkpoint --file-system-id <file-system-id> --layer-id "<layer-id>" --checkpoint-id before-review
    ```

- 自動的に識別されるチェックポイントを作成します。

    ```bash
    # Let the service assign the checkpoint ID while retaining a human label.
    ti fs create-layer-checkpoint --file-system-id <file-system-id> --layer-id "<layer-id>" --label "before review"
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)