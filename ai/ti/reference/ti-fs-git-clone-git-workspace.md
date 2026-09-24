---
title: ti fs-git clone-git-workspace
summary: Git リポジトリをマウントされた TiDB Cloud Filesystem にクローンします。
---

# ti fs-git clone-git-workspace

リポジトリをマウントされた file system パスにクローンします。Hydration は同期的に実行することも、バックグラウンドで実行することもできます。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs-git clone-git-workspace
  --repo-url <string>
  --target-path <string>
  [--blobless]
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--hydrate <string>]
  [--version]
```

## オプション {#options}

- `--repo-url <string>`: Git リポジトリの URL。\[required]
- `--target-path <string>`: クローン先のマウントされたファイルシステムパス。\[required]
- `--blobless`: blobless の部分的なローカル `.git` を作成し、クリーンな blob を別途 hydrate します。
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: file system トークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、このコマンドは選択した file system 用にローカルに保存されているトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--hydrate <string>`: クリーンデータの hydration モード: `auto`、`background`、`sync`、または `off`。`auto` では、blobless クローンはバックグラウンドで hydrate され、blobless でないクローンでは別個の hydration ステップは実行されません。`background` と `sync` には `--blobless` が必要です。`off` は hydration をスキップします。\[default: auto]
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- 通常どおりにリポジトリをクローンする場合:

    ```bash
    # Create a complete Git checkout in the mounted file system path.
    ti fs-git clone-git-workspace --file-system-id <file-system-id> --repo-url https://github.com/pingcap/tidb.git --target-path /path/to/workspace/tidb
    ```

- blobless ワークスペースをすぐに開始する場合:

    ```bash
    # Expose the repository tree while clean Git objects hydrate in the background.
    ti fs-git clone-git-workspace --file-system-id <file-system-id> --repo-url https://github.com/pingcap/tidb.git --target-path /path/to/workspace/tidb --blobless --hydrate background
    ```

- blobless hydration の完了を待機する場合:

    ```bash
    # Keep the clone command running until clean Git objects finish hydrating.
    ti fs-git clone-git-workspace --file-system-id <file-system-id> --repo-url https://github.com/pingcap/tidb.git --target-path /path/to/workspace/tidb --blobless --hydrate sync
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem Git CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem-git.md)