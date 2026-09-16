---
title: ti update
summary: TiDB Cloud CLI リリースの更新を確認またはインストールします。
---

# ti update

TiDB Cloud CLI リリースの更新を確認またはインストールします。このコマンドは、`~/.ti/` 配下の設定、プロファイル、認証情報、操作ログ、その他の状態を読み取ったり変更したりしません。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェイスは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti update
  [--check]
  [--dry-run]
  [--fail-if-update-available]
  [--help]
  [--target-version <string>]
  [--version]
```

## オプション {#options}

- `--check`: 更新を実行せずに、新しい `ti` リリースが利用可能かどうかを確認します。
- `--dry-run`: ローカルバイナリを変更せずに、更新計画を表示します。
- `--fail-if-update-available`: `--check` と併用すると、更新が利用可能な場合に終了コード 1 で終了します。
- `--help`: ヘルプ情報を表示します。
- `--target-version <string>`: 対象の `ti` バージョンです。`latest` または `vX.Y.Z` などを指定します。\[default: latest]
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- 更新が利用可能かどうかを確認する:

    ```bash
    # Compare the installed version with the latest GitHub release without changing files.
    ti update --check
    ```

- 更新が利用可能な場合に CI ジョブを失敗させる:

    ```bash
    # Exit with code 1 when a newer release is available, without changing files.
    ti update --check --fail-if-update-available
    ```

- 更新をプレビューする:

    ```bash
    # Show the files and versions that an update would change.
    ti update --dry-run
    ```

- 特定のリリースをインストールする:

    ```bash
    # Replace an eligible installation with the requested release version.
    ti update --target-version <version>
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud CLI のインストール、設定、および更新](/ai/ti/reference/ti-install-configure-update.md)