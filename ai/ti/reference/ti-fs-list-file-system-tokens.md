---
title: ti fs list-file-system-tokens
summary: 1 つの TiDB Cloud Filesystem のトークンメタデータを一覧表示します。
---

# ti fs list-file-system-tokens

file system のトークンを一覧表示します。トークン値自体は出力に含まれません。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs list-file-system-tokens
  [--file-system-id <string>]
  [--fs-token <string>]
  [--include-expired]
  [--help]
  [--limit <int32>]
  [--offset <int32>]
  [--version]
```

## オプション {#options}

- `--file-system-id <string>`: トークンを一覧表示する file system を指定します。TiDB Cloud API 認証情報を使用する場合は必須です。`--fs-token` または `TI_FS_TOKEN` で所有者トークンが指定されている場合は、`ti` がそのトークンから ID を導出するため、省略可能です。
- `--fs-token <string>`: file system 所有者トークンを使用してリクエストを認可します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、このコマンドは選択した file system 用にローカルに保存されているトークンを使用します。利用可能な file system トークンがない場合、このコマンドは設定済みの TiDB Cloud API キーを使用します。スコープ付きトークンではトークンメタデータを一覧表示できません。
- `--include-expired`: 期限切れのトークンメタデータを含めます。失効済みトークンはサービスから返されません。
- `--help`: ヘルプ情報を表示します。
- `--offset <int32>`: 0 ベースのトークンオフセットを設定します [default: 0]。
- `--limit <int32>`: 返すトークンの最大数を 1 から 200 の範囲で設定します [default: 50]。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- 現在のトークンメタデータをテキストとして一覧表示します。

    ```bash
    # Use token_id, not the non-unique token name, for later mutations.
    ti fs list-file-system-tokens \
      --file-system-id "<file-system-id>" \
      --output text
    ```

- ページネーションを使用して期限切れのトークンメタデータを確認します。

    ```bash
    # Request up to 100 rows starting at offset 0.
    ti fs list-file-system-tokens \
      --file-system-id "<file-system-id>" \
      --include-expired \
      --offset 0 \
      --limit 100
    ```

- 所有者トークンを使用してトークンメタデータを一覧表示します。

    ```bash
    # The owner token identifies the file system, so --file-system-id is not needed.
    TI_FS_TOKEN="<owner-fs-token>" ti fs list-file-system-tokens --output text
    ```

## 関連ドキュメント {#related-documentation}

- [`ti fs generate-file-system-token`](/ai/ti/reference/ti-fs-generate-file-system-token.md)
- [`ti fs generate-file-system-scoped-token`](/ai/ti/reference/ti-fs-generate-file-system-scoped-token.md)
- [TiDB Cloud CLI のリージョン、セキュリティ、および制限事項](/ai/ti/reference/ti-regions-security-and-limitations.md)