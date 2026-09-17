---
title: ti fs disable-file-system-token
summary: TiDB Cloud Filesystem トークンを一時的に無効化します。
---

# ti fs disable-file-system-token

Filesystem トークンを取り消すことなく一時的に無効化します。トークンは後で [`ti fs enable-file-system-token`](/ai/ti/reference/ti-fs-enable-file-system-token.md) を使って再度有効化できます。既知のローカルマウントで使用されているトークンは、先に drain とアンマウントを実行する必要があります。オーナートークン認証では、無効化できるのはスコープ付きトークンのみです。TiDB Cloud API キーでは、どちらの種類のトークンも無効化できます。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs disable-file-system-token
  --token-id <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--dry-run]
  [--help]
  [--version]
```

## オプション {#options}

- `--file-system-id <string>`: トークンを所有する Filesystem を指定します。TiDB Cloud API 認証情報を使用する場合は必須です。オーナートークンが ID を提供する場合は省略できます。
- `--token-id <string>`: list コマンドが返す変更不可のトークン ID を指定します。このオプションは必須です。
- `--fs-token <string>`: オーナー Filesystem トークンを使用してリクエストを認証します。省略した場合、コマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、コマンドは選択した Filesystem 用にローカルに保存されているトークンを使用します。利用可能な Filesystem トークンがない場合、コマンドは設定済みの TiDB Cloud API キーを使用します。
- `--dry-run`: トークンを無効化せずに、認証情報、識別子、および既知のローカルマウント競合を検証します。
- `--help`: ヘルプ情報を表示します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- ローカルマウントを停止した後にトークンを無効化する:

    ```bash
    # Drain and unmount first when this token backs a mount on the current machine.
    ti fs drain-file-system --mount-path /path/to/workspace
    ti fs unmount-file-system --mount-path /path/to/workspace
    ti fs disable-file-system-token \
      --file-system-id "<file-system-id>" \
      --token-id "<token-id>"
    ```

- オーナートークンを使用してスコープ付きトークンを無効化する:

    ```bash
    # Inject TI_FS_TOKEN from a secret manager. The owner token identifies the Filesystem.
    # Drain any local mount that uses the target token first.
    ti fs disable-file-system-token \
      --token-id "<scoped-token-id>"
    ```

## 関連ドキュメント {#related-documentation}

- [トークン管理の認可](/ai/ti/reference/ti-filesystem.md#token-management-authorization)
- [`ti fs enable-file-system-token`](/ai/ti/reference/ti-fs-enable-file-system-token.md)
- [`ti fs delete-file-system-token`](/ai/ti/reference/ti-fs-delete-file-system-token.md)
