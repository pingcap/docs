---
title: ti fs pack-file-system
summary: ローカル Filesystem オーバーレイ状態をパックします。
---

# ti fs pack-file-system

選択した[ローカルオーバーレイ状態](/ai/ti/reference/ti-filesystem.md#mount-profiles-and-local-overlays)をリモートアーカイブにパックします。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs pack-file-system
  [--archive-path <string>]
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--local-root <string>]
  [--mount-path <string>]
  [--mount-profile <string>]
  [--path <string>]
  [--remote-root <string>]
  [--version]
```

## オプション {#options}

- `--archive-path <string>`: パックされたアーカイブのパスです。
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: Filesystem トークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、このコマンドは選択した Filesystem 用にローカルに保存されているトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--local-root <string>`: オーバーレイディレクトリを含むローカルオーバーレイのルートです。
- `--mount-path <string>`: ローカルのマウント済みパスです。
- `--mount-profile <string>`: [マウントプロファイル](/ai/ti/reference/ti-filesystem.md#mount-profiles-and-local-overlays) を選択します: `coding-agent`、`portable`、または `none`。省略した場合は `none` を使用します。
- `--path <string>`: パック対象のローカルオーバーレイパスです。繰り返し指定できます。
- `--remote-root <string>`: ローカルオーバーレイで表される TiDB Cloud ファイルシステムのルートです。\[default: /]
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options)を参照してください。

## 例 {#examples}

- マウントされたワークスペースをパックする:

    ```bash
    # Persist the local overlay associated with an existing mount.
    ti fs pack-file-system --file-system-id <file-system-id> --mount-path /path/to/workspace
    ```

- 明示的なルートをパックする:

    ```bash
    # Create a portable archive from selected local and remote roots.
    ti fs pack-file-system --file-system-id <file-system-id> --local-root /path/to/local-root --remote-root /workspace --mount-profile portable
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)
