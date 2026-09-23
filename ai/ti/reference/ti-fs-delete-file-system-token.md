---
title: ti fs delete-file-system-token
summary: ファイルシステムトークンを完全に取り消し、認証に使用できないようにします。
---

# ti fs delete-file-system-token

ファイルシステムトークンを完全に取り消します。変更が反映されると、そのトークンは認証に使用できなくなり、一覧結果にも表示されなくなります。オーナートークンは同じ file system 内のいずれの種類のトークンも取り消せますが、スコープ付きトークンではこのコマンドを使用できません。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs delete-file-system-token
  --token-id <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--dry-run]
  [--help]
  [--version]
```

## オプション {#options}

- `--file-system-id <string>`: トークンを所有するファイルシステムを指定します。TiDB Cloud API 認証情報を使用する場合は必須です。オーナートークンが ID を提供する場合は省略可能です。
- `--token-id <string>`: list コマンドが返す不変のトークン ID を指定します。このオプションは必須です。
- `--fs-token <string>`: ファイルシステムのオーナートークンを使用してリクエストを認可します。省略した場合、コマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、コマンドは選択したファイルシステム用にローカルに保存されたトークンを使用します。利用可能なファイルシステムトークンがない場合、コマンドは設定済みの TiDB Cloud API キーを使用します。
- `--dry-run`: トークンを取り消さずに、認証情報、識別子、および既知のローカルマウント競合を検証します。
- `--help`: ヘルプ情報を表示します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- 置き換え用トークンを検証した後で古いトークンを取り消します。

    ```bash
    # Revocation is permanent; use disable first when you need a reversible rollout.
    ti fs delete-file-system-token \
      --file-system-id "<file-system-id>" \
      --token-id "<old-token-id>"
    ```

- オーナートークンを使用してトークンを取り消します。

    ```bash
    # The owner token identifies the file system; use the immutable ID of the token being revoked.
    TI_FS_TOKEN="<owner-fs-token>" ti fs delete-file-system-token \
      --token-id "<old-token-id>"
    ```

## 関連ドキュメント {#related-documentation}

- [トークン管理の認可](/ai/ti/reference/ti-filesystem.md#token-management-authorization)
- [`ti fs generate-file-system-token`](/ai/ti/reference/ti-fs-generate-file-system-token.md)
- [`ti fs disable-file-system-token`](/ai/ti/reference/ti-fs-disable-file-system-token.md)
