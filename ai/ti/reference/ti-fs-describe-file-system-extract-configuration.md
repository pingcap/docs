---
title: ti fs describe-file-system-extract-configuration
summary: ファイルシステムのメディア抽出設定を表示します。
---

# ti fs describe-file-system-extract-configuration

ファイルシステムの画像、音声、または動画の抽出設定を表示します。この設定は任意であり、カスタマイズしていない場合でも通常のファイルシステム操作には影響しません。このコマンドには TiDB Cloud API 認証情報が必要で、ファイルシステムトークンは使用しません。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs describe-file-system-extract-configuration
  --file-system-id <string>
  --media-type <string>
  [--help]
  [--version]
```

## オプション {#options}

- `--file-system-id <string>`: 変更不可のファイルシステム ID を設定します。\[required]
- `--media-type <string>`: `image`、`audio`、または `video` を選択します。\[required]
- `--help`: ヘルプ情報を表示します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- 画像抽出を確認します。

    ```bash
    # Show whether image extraction uses a custom, default, or absent provider configuration.
    ti fs describe-file-system-extract-configuration \
      --file-system-id <file-system-id> \
      --media-type image
    ```

- 有効なプロバイダーソースのみを出力します。

    ```bash
    # Return custom, default, or none for use in a script.
    ti fs describe-file-system-extract-configuration \
      --file-system-id <file-system-id> \
      --media-type audio \
      --query source \
      --output text
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)