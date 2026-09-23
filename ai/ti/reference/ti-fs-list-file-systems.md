---
title: ti fs list-file-systems
summary: リージョン内のリモートファイルシステムを一覧表示します。
---

# ti fs list-file-systems

選択したリージョンで、選択した TiDB Cloud 認証情報を使用してアクセス可能なすべてのファイルシステムを一覧表示します。結果には、表示名、ラベル、ステータス、クォータと使用量、および `has_local_token` が含まれます。`has_local_token` は、このマシンに一致するローカルトークンがあるかどうかを示します。トークンの値が含まれることはありません。

利用可能な場合、クォータデータにはメディアおよび動画抽出の上限と使用量が含まれます。

CLI はすべてのサービスページを自動的に取得し、完全でソート済みの 1 つの結果を返すため、このコマンドにはページネーションオプションはありません。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェイスは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs list-file-systems
  [--display-name <string>]
  [--help]
  [--label <string>]
  [--version]
```

## オプション {#options}

- `--display-name <string>`: 大文字と小文字を区別する display-name の部分文字列でフィルタリングします。これは正確なリソース検索ではありません。
- `--help`: ヘルプ情報を表示します。
- `--label <string>`: 1 つの完全一致する `key=value` ラベルでフィルタリングします。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- リモート管理されるファイルシステムを一覧表示します。

    ```bash
    # Return the remote inventory for the profile's region without exposing tokens.
    ti fs list-file-systems
    ```

- 表示メタデータでファイルシステムをフィルタリングします。

    ```bash
    # Match a display-name substring and one exact organization-visible label.
    ti fs list-file-systems \
      --display-name workspace \
      --label environment=production
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)