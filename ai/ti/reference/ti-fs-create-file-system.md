---
title: ti fs create-file-system
summary: ファイルシステムを作成します。
---

# ti fs create-file-system

ファイルシステム を作成し、その ID とオーナートークンを返します。CLI は現在のプロファイルにトークンを保存して選択します。ファイルシステム が使用可能になるまで待機するには、`--wait` を使用します。

必要に応じて、表示名とラベルを設定できます。これらの値は `list-file-systems` および `describe-file-system` の出力に表示されますが、後続のコマンドで ファイルシステム を選択するためには使用されません。

> **Important:**
>
> サービスは初期オーナートークンを再表示しません。CLI がトークンを保存できなかったと警告した場合は、ターミナルを閉じる前に返された値を保存してください。後でローカル認証情報が失われた場合は、[`ti fs generate-file-system-token`](/ai/ti/reference/ti-fs-generate-file-system-token.md) と TiDB Cloud API 認証情報を使用して、置き換え用のオーナートークンを作成してください。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。その機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs create-file-system
  [--display-name <string>]
  [--dry-run]
  [--help]
  [--label <string>]
  [--version]
  [--wait]
```

## オプション {#options}

- `--display-name <string>`: file system の一覧コマンドで表示される、4～64 文字の表示名を設定します。この値は、後続のコマンドで file system を選択するためには使用されません。
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--help`: ヘルプ情報を表示します。
- `--label <string>`: 組織内で表示可能な `key=value` ラベルを追加します。このオプションを繰り返すことで、最大 30 個のラベルを追加できます。ラベルには秘密情報や個人データを含めないでください。
- `--version`: バージョン情報を表示します。
- `--wait`: 作成した file system がアクティブになるまで待機します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- file system を作成し、使用可能になるまで待機します。

    ```bash
    # Wait until the new file system root is readable before returning.
    ti fs create-file-system \
      --display-name agent-workspace \
      --label environment=development \
      --label team=ai \
      --wait
    ```

- file system を非同期で作成します。

    ```bash
    # Return after provisioning is accepted so work can continue in parallel.
    ti fs create-file-system
    ```

- file system の作成をプレビューします。

    ```bash
    # Validate credentials, placement, and the request without provisioning storage.
    ti fs create-file-system --dry-run
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)
