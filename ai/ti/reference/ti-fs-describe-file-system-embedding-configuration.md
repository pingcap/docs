---
title: ti fs describe-file-system-embedding-configuration
summary: TiDB Cloud Filesystem の埋め込み設定を表示します。
---

# ti fs describe-file-system-embedding-configuration

Filesystem の埋め込み設定を表示します。この設定は任意であり、カスタマイズしていない場合でも通常の Filesystem 操作には影響しません。このコマンドには TiDB Cloud API 認証情報が必要で、Filesystem トークンは使用しません。

`source` フィールドは、設定が `custom`、`default`、`none`、または `database_auto` のいずれであるかを示します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs describe-file-system-embedding-configuration
  --file-system-id <string>
  [--help]
  [--version]
```

## オプション {#options}

- `--file-system-id <string>`: 変更不可の Filesystem ID を設定します。\[required]
- `--help`: ヘルプ情報を表示します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- 有効な埋め込み設定を確認します。

    ```bash
    # Show provider metadata, masked credentials, source, and generation.
    ti fs describe-file-system-embedding-configuration \
      --file-system-id <file-system-id>
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)