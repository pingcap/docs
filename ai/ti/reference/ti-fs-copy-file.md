---
title: ti fs copy-file
summary: ファイルシステムとの間、またはその内部でファイルをコピーします。
---

# ti fs copy-file

ローカルパス、リモートパス、標準入力、標準出力の間でファイルをコピーします。このコマンドのエイリアスは `ti fs cp` です。

以下のソースと宛先の組み合わせのうち、いずれか 1 つだけを指定してください。

| ソース | 宛先 |
| --- | --- |
| `--from-local` | `--to-remote` |
| `--from-stdin` | `--to-remote` |
| `--from-remote` | `--to-local` |
| `--from-remote` | `--to-stdout` |
| `--from-remote` | `--to-remote` |

`--append` は `--from-local` と `--to-remote` の組み合わせでのみサポートされます。標準入力またはリモートソースはサポートされません。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs copy-file
  [--append]
  [--create-parents]
  [--description <string>]
  [--dry-run]
  [--file-system-id <string>]
  [--from-local <string>]
  [--from-remote <string>]
  [--from-stdin]
  [--fs-token <string>]
  [--help]
  [--layer-id <string>]
  [--overwrite]
  [--recursive]
  [--resume]
  [--tag <string>]
  [--to-local <string>]
  [--to-remote <string>]
  [--to-stdout]
  [--version]
```

## オプション {#options}

- `--append`: ローカルファイルの内容を TiDB Cloud file system 内のファイルに追記します。
- `--create-parents`: TiDB Cloud file system からコピーする際に、不足しているローカルの親ディレクトリを作成します。
- `--description <string>`: `--to-remote` 操作のファイル説明です。
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--from-local <string>`: ローカルのソースパスです。
- `--from-remote <string>`: TiDB Cloud file system 内のソースパスです。
- `--from-stdin`: 標準入力から読み取り、`--to-remote` に書き込みます。
- `--fs-token <string>`: file system トークンを設定します。省略した場合、コマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、選択した file system 用にローカルに保存されているトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--layer-id <string>`: コピーした 1 つのファイルを、ベースファイルシステムではなくファイルシステムレイヤーに書き込みます。`--recursive` とは併用できません。
- `--overwrite`: 既存の宛先ファイルを置き換えます。
- `--recursive`: ディレクトリ構造を再帰的にコピーします。`--layer-id` とは併用できません。代わりに、書き込み可能な FUSE マウントを介してレイヤーディレクトリをシードしてください。
- `--resume`: 実行中のコピー操作を再開します。
- `--tag <string>`: `--to-remote` 操作用に `key=value` 形式のタグを作成します。複数回指定できます。
- `--to-local <string>`: ローカルの宛先パスです。
- `--to-remote <string>`: TiDB Cloud file system 内の宛先パスです。
- `--to-stdout`: `--from-remote` を標準出力に書き込みます。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- ローカルファイルをアップロードする:

    ```bash
    # Copy a local report into the selected remote file system.
    ti fs copy-file --file-system-id <file-system-id> --from-local ./report.md --to-remote /reports/report.md
    ```

- リモートファイルをダウンロードする:

    ```bash
    # Create missing local parent directories while downloading the file.
    ti fs copy-file --file-system-id <file-system-id> --from-remote /reports/report.md --to-local ./downloads/report.md --create-parents
    ```

- リモートディレクトリをコピーする:

    ```bash
    # Duplicate a complete directory tree without downloading it locally.
    ti fs copy-file --file-system-id <file-system-id> --from-remote /reports --to-remote /archive/reports --recursive
    ```

- 大きなアップロードを再開する:

    ```bash
    # Continue an interrupted local-to-remote transfer instead of restarting it.
    ti fs copy-file --file-system-id <file-system-id> --from-local ./large.bin --to-remote /artifacts/large.bin --resume
    ```

- リモートログに追記する:

    ```bash
    # Add local log data to the existing remote object efficiently.
    ti fs copy-file --file-system-id <file-system-id> --from-local ./tail.log --to-remote /logs/app.log --append
    ```

- 標準入力を file system にストリーミングする:

    ```bash
    # Upload generated content without creating an intermediate local file.
    printf 'ready\n' | ti fs copy-file --file-system-id <file-system-id> --from-stdin --to-remote /status.txt --tag source=stdin --description "generated status"
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)
