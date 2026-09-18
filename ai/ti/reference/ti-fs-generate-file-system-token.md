---
title: ti fs generate-file-system-token
summary: 1 つの TiDB Cloud Filesystem 用の追加のオーナートークンを生成します。
---

# ti fs generate-file-system-token

TiDB Cloud API 認証情報を使用して、Filesystem のオーナートークンを生成します。トークン値はコマンド出力にのみ表示され、後から取得することはできません。トークンをローカルの認証情報ストアに保存するには、`--store-locally` を使用します。既存の Filesystem トークンを使用してオーナートークンを生成することはできません。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。その機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs generate-file-system-token
  --file-system-id <string>
  --token-name <string>
  (--ttl <duration> | --no-expiration)
  [--dry-run]
  [--help]
  [--replace]
  [--store-locally]
  [--version]
```

## オプション {#options}

- `--file-system-id <string>`: トークンを所有する Filesystem を指定します。FS トークンではこのオプションを置き換えることも、オーナートークンの生成を認可することもできません。このオプションは必須です。
- `--token-name <string>`: 最大 64 バイトの運用用トークン名を設定します。名前は一意ではありません。このオプションは必須です。
- `--ttl <duration>`: 正の有効期間を秒単位で設定します。最大 365 日まで指定できます。`--ttl` と `--no-expiration` のいずれか一方を必ず指定してください。
- `--no-expiration`: 有効期限のないトークンを作成します。`--ttl` と `--no-expiration` のいずれか一方を必ず指定してください。
- `--store-locally`: このプロファイルと Filesystem 用に、生成したトークンを保存して選択します。
- `--replace`: 既存の選択済みローカルトークンを置き換えます。`--store-locally` が必要であり、以前のリモートトークンは失効されません。
- `--dry-run`: トークンを生成せずに、認証情報、リージョン、有効期間、およびローカル保存の前提条件を検証します。
- `--help`: ヘルプ情報を表示します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- CI ジョブ用の短期間有効なトークンを生成する場合:

    ```bash
    # Save the one-time plaintext response in an owner-only file.
    umask 077
    ti fs generate-file-system-token \
      --file-system-id "<file-system-id>" \
      --token-name ci-deploy \
      --ttl 24h > ./ci-token.json
    ```

- 別のマシン用に有効期限のないトークンを生成する場合:

    ```bash
    # Generation does not change the current local selection by default.
    ti fs generate-file-system-token \
      --file-system-id "<file-system-id>" \
      --token-name workstation \
      --no-expiration
    ```

- 置き換え用のローカルトークンを生成して選択する場合:

    ```bash
    # The old remote token remains active until you explicitly disable or delete it.
    ti fs generate-file-system-token \
      --file-system-id "<file-system-id>" \
      --token-name local-owner-v2 \
      --ttl 720h \
      --store-locally \
      --replace
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)
- [`ti fs list-file-system-tokens`](/ai/ti/reference/ti-fs-list-file-system-tokens.md)
