---
title: ti fs drain-file-system
summary: マウントされた TiDB Cloud Filesystem をドレインします。
---

# ti fs drain-file-system

マウントをオンラインのまま維持しつつ、FUSE マウントからリモート file system へ保留中の書き込みをフラッシュします。このコマンドのエイリアスは `ti fs drain` です。WebDAV マウントの場合は、書き込み元を停止して `ti fs unmount-file-system` を使用してください。これに対して `drain-file-system` を実行するとエラーが返されます。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs drain-file-system
  --mount-path <string>
  [--dry-run]
  [--help]
  [--timeout <duration>]
  [--version]
```

## オプション {#options}

- `--mount-path <string>`: ローカル FUSE マウントパス。\[required]
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--help`: ヘルプ情報を表示します。
- `--timeout <duration>`: ダーティハンドルと保留中の書き込みがドレインされるまで待機する時間。\[デフォルト: `30s`]
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- 保留中の書き込みをドレインする:

    ```bash
    # Flush queued FUSE writes while leaving the file system mounted.
    ti fs drain-file-system --mount-path /path/to/workspace --timeout 30s
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)