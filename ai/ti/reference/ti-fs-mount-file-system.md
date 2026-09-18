---
title: ti fs mount-file-system
summary: TiDB Cloud Filesystem をマウントします。
---

# ti fs mount-file-system

自動、FUSE、または WebDAV モードで Filesystem をマウントします。このコマンドのエイリアスは `ti fs mount` です。

このコマンドはバックグラウンドでマウント処理を開始し、マウントの準備が完了するまで待機してから、結果を出力します。起動に失敗した場合、エラーには診断用のログパスが含まれます。マウントを終了するには `ti fs unmount-file-system` を使用します。

> **Important:**
>
> レイヤーおよびチェックポイントのマウントには FUSE が必要です。通常自動選択で WebDAV が使用される macOS では、macFUSE をインストールし、`--driver fuse` を指定してください。チェックポイントのマウントは常に読み取り専用です。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。その機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs mount-file-system
  --mount-path <string>
  [--cache-dir <string>]
  [--checkpoint-id <string>]
  [--driver <string>]
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--layer-ref <string>]
  [--local-root <string>]
  [--mount-profile <string>]
  [--no-auto-unpack]
  [--pack-path <string>]
  [--read-cache-max-file-mb <int64>]
  [--read-cache-size-mb <int64>]
  [--read-cache-ttl <duration>]
  [--read-only]
  [--ready-timeout <duration>]
  [--remote-path <string>]
  [--unpack-archive-path <string>]
  [--version]
  [--write-back-cache]
```

## オプション {#options}

- `--mount-path <string>`: ローカルのマウントパス。\[required]
- `--cache-dir <string>`: ローカルの FUSE キャッシュディレクトリ。省略した場合は `~/.ti/cache/mounts/<mount-hash>` を使用します。
- `--checkpoint-id <string>`: `--layer-ref` のこのチェックポイントを読み取り専用でマウントします。FUSE が必要です。
- `--driver <string>`: マウントドライバー: `auto`、`fuse`、または `webdav`。\[default: auto]
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: Filesystem トークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、このコマンドは選択した Filesystem 用にローカルに保存されているトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--layer-ref <string>`: 書き込み可能なレイヤー ID、一意の名前、または [tag reference](/ai/ti/reference/ti-filesystem.md#layer-references) を介してマウントします。FUSE が必要です。
- `--local-root <string>`: ローカルオーバーレイルート。省略した場合は `~/.ti/local/fs/<mount-hash>` を使用します。
- `--mount-profile <string>`: [マウントプロファイル](/ai/ti/reference/ti-filesystem.md#mount-profiles-and-local-overlays) を選択します: `coding-agent`、`portable`、または `none`。省略した場合は `none` を使用します。
- `--no-auto-unpack`: マウント前に `portable` マウントプロファイルのデフォルトの自動 unpack をスキップします。
- `--pack-path <string>`: 自動または手動のパックに含めるローカルオーバーレイパス。繰り返し指定できます。
- `--read-cache-max-file-mb <int64>`: FUSE 読み取りキャッシュに格納できる最大ファイルサイズ（MiB）。0 を指定するとデフォルト値を使用します。\[default: 4]
- `--read-cache-size-mb <int64>`: FUSE 読み取りキャッシュサイズ（MiB）。0 を指定するとデフォルト値を使用します。\[default: 128]
- `--read-cache-ttl <duration>`: FUSE 読み取りキャッシュの有効期間。\[default: `30s`]
- `--read-only`: 読み取り専用マウントモード。
- `--ready-timeout <duration>`: バックグラウンドマウントの準備完了を待機する時間。\[default: `30s`]
- `--remote-path <string>`: マウントする TiDB Cloud file system のルートパス。\[default: /]
- `--unpack-archive-path <string>`: マウント前にパックされたアーカイブを復元します。
- `--version`: バージョン情報を表示します。
- `--write-back-cache`: フラッシュ時にファイルシステムへ書き込む前に、FUSE の書き込みをローカルに永続化します。この動作はデフォルトで有効です。無効にするには `--write-back-cache=false` を指定します。常に読み取り専用であるチェックポイントマウントでは使用できません。\[default: true]

すべてのコマンドで共有されるオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- デフォルトドライバーで Filesystem をマウントします:

    ```bash
    # Let the CLI select the default driver for the current platform.
    ti fs mount-file-system --file-system-id <file-system-id> --mount-path /path/to/workspace
    ```

- 読み取り専用の FUSE マウントを作成します:

    ```bash
    # Expose the remote namespace through FUSE without permitting writes.
    ti fs mount-file-system --file-system-id <file-system-id> --mount-path /path/to/workspace --driver fuse --read-only
    ```

- macFUSE を使わずに macOS で WebDAV を使用します:

    ```bash
    # Select WebDAV explicitly when a FUSE runtime is unavailable.
    ti fs mount-file-system --file-system-id <file-system-id> --mount-path /path/to/workspace --driver webdav
    ```

- FUSE 読み取りキャッシュを調整します:

    ```bash
    # Increase cache capacity for repeated reads of medium-sized files.
    ti fs mount-file-system --file-system-id <file-system-id> --mount-path /path/to/workspace --driver fuse --read-cache-size-mb 256 --read-cache-max-file-mb 16
    ```

- 書き込み可能な子レイヤーをマウントします:

    ```bash
    # Expose only the selected copy-on-write timeline at the local path.
    ti fs mount-file-system --file-system-id <file-system-id> --mount-path /path/to/experiment --remote-path /workspace --driver fuse --layer-ref experiment
    ```

- 変更不可の過去のチェックポイントを比較します:

    ```bash
    # A checkpoint mount is always read-only.
    ti fs mount-file-system --file-system-id <file-system-id> --mount-path /path/to/checkpoint --remote-path /workspace --driver fuse --layer-ref experiment --checkpoint-id v5
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)
