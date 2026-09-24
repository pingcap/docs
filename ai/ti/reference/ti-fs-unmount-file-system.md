---
title: ti fs unmount-file-system
summary: ファイルシステムをアンマウントします。
---

# ti fs unmount-file-system

バックグラウンドでマウントされたファイルシステムを、保留中のデータを適切にフラッシュしてからアンマウントします。このコマンドのエイリアスは `ti fs umount` です。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs unmount-file-system
  --mount-path <string>
  [--dry-run]
  [--force]
  [--help]
  [--ignore-absent]
  [--no-auto-pack]
  [--pack-archive-path <string>]
  [--timeout <duration>]
  [--version]
```

## オプション {#options}

- `--mount-path <string>`: ローカルのマウントパスです。\[required]
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--force`: 適切なアンマウントがタイムアウトした場合に、マウントプロセスを強制終了します。これにより、コミットされていないメモリ内データまたは write-back 状態が失われる可能性があります。
- `--help`: ヘルプ情報を表示します。
- `--ignore-absent`: 指定したパスにファイルシステムのマウント状態が存在しない場合でも、成功として返します。
- `--no-auto-pack`: マウントに設定されたデフォルトの自動パックアクションをスキップします。組み込みの `portable` プロファイルでは、パックパスとして `/` を選択することでこのアクションが有効になります。
- `--pack-archive-path <string>`: アンマウント後に、マウントのローカルオーバーレイをこのリモートアーカイブパスにパックします。このオプションを指定すると、マウントプロファイルにデフォルトのパックパスがない場合でもパックが要求されます。
- `--timeout <duration>`: マウントプロセスの終了を待機する時間です。\[default: `30s`]
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- ファイルシステムをアンマウントします。

    ```bash
    # Gracefully flush pending writes and detach the file system mount.
    ti fs unmount-file-system --mount-path /path/to/workspace
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)