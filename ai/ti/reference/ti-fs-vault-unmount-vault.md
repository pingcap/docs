---
title: ti fs-vault unmount-vault
summary: file system Vault ビューをアンマウントします。
---

# ti fs-vault unmount-vault

ファイルシステム用のローカル Vault マウントをアンマウントします。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs-vault unmount-vault
  --mount-path <string>
  [--dry-run]
  [--force]
  [--help]
  [--ignore-absent]
  [--timeout <duration>]
  [--version]
```

## オプション {#options}

- `--mount-path <string>`: ローカルのマウントパス。\[required]
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--force`: 正常なアンマウントがタイムアウトした場合、マウントプロセスを強制終了します。
- `--help`: ヘルプ情報を表示します。
- `--ignore-absent`: パスに対して `ti fs-vault` のマウント状態が存在しない場合でも成功を返します。
- `--timeout <duration>`: マウントプロセスの終了を待機する時間。\[default: `30s`]
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- Vault ビューをアンマウントする場合:

    ```bash
    # Detach the local read-only Vault mount.
    ti fs-vault unmount-vault --mount-path ./vault
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem Vault CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem-vault.md)