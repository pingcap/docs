---
title: ti fs-git hydrate-git-workspace
summary: Filesystem Git ワークスペース内のクリーンな Git オブジェクトを hydrate します。
---

# ti fs-git hydrate-git-workspace

既存の `ti` Git ワークスペースに対して、クリーンな Git オブジェクトを hydrate します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs-git hydrate-git-workspace
  --target-path <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--timeout <duration>]
  [--version]
```

## オプション {#options}

- `--target-path <string>`: マウントされた `ti fs` ワークスペースのパスです。\[required]
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: Filesystem トークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、選択した Filesystem 用にローカルに保存されているトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--timeout <duration>`: hydrate の最大実行時間です。\[default: `30m0s`]
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- Git ワークスペースの hydrate を完了する:

    ```bash
    # Download missing clean Git objects for an existing blobless workspace.
    ti fs-git hydrate-git-workspace --file-system-id <file-system-id> --target-path /path/to/workspace/tidb --timeout 30m
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem Git CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem-git.md)