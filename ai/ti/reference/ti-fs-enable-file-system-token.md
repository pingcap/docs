---
title: ti fs enable-file-system-token
summary: 無効化された file system トークンを再度認証できるように有効化します。
---

# ti fs enable-file-system-token

無効化された file system トークンを再度有効にします。トークンが使用可能になるまで約 10 秒かかる場合があります。オーナートークン認証では、有効化できるのはスコープ付きトークンのみです。TiDB Cloud API キーでは、どちらの種類のトークンも有効化できます。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs enable-file-system-token
  --token-id <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--dry-run]
  [--help]
  [--version]
```

## オプション {#options}

- `--file-system-id <string>`: トークンを所有する file system を指定します。TiDB Cloud API 認証情報を使用する場合は必須です。オーナートークンが ID を提供する場合は省略可能です。
- `--token-id <string>`: list コマンドで返される変更不可のトークン ID を指定します。このオプションは必須です。
- `--fs-token <string>`: file system オーナートークンを使用してリクエストを認可します。省略した場合、コマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、コマンドは選択した file system 用にローカルに保存されたトークンを使用します。利用可能な file system トークンがない場合、コマンドは設定済みの TiDB Cloud API キーを使用します。
- `--dry-run`: リモートのトークン状態を変更せずにリクエストを検証します。
- `--help`: ヘルプ情報を表示します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- 既知のトークンを有効化する:

    ```bash
    # Allow about 10 seconds for all authentication caches to observe the change.
    ti fs enable-file-system-token \
      --file-system-id "<file-system-id>" \
      --token-id "<token-id>"
    ```

- オーナートークンを使用してスコープ付きトークンを有効化する:

    ```bash
    # The owner token identifies and authorizes token management for its file system.
    TI_FS_TOKEN="<owner-fs-token>" ti fs enable-file-system-token \
      --token-id "<scoped-token-id>"
    ```

## 関連ドキュメント {#related-documentation}

- [トークン管理の認可](/ai/ti/reference/ti-filesystem.md#token-management-authorization)
- [`ti fs list-file-system-tokens`](/ai/ti/reference/ti-fs-list-file-system-tokens.md)
- [`ti fs disable-file-system-token`](/ai/ti/reference/ti-fs-disable-file-system-token.md)
