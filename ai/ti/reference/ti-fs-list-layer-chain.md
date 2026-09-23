---
title: ti fs list-layer-chain
summary: ファイルシステム レイヤーの祖先チェーンを一覧表示します。
---

# ti fs list-layer-chain

ルートレイヤーから選択した子レイヤーまでの親子レイヤーチェーンを、各レイヤーのシーケンス境界を含めて一覧表示します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェイスは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs list-layer-chain
  --layer-ref <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## オプション {#options}

- `--layer-ref <string>`: レイヤー ID、一意の名前、または [タグ参照](/ai/ti/reference/ti-filesystem.md#layer-references)。\[required]
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: ファイルシステム トークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、このコマンドは選択したファイルシステム用にローカルに保存されているトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- 子タイムラインを確認します。

    ```bash
    # Render the root-to-tip ancestry as stable text columns.
    ti fs list-layer-chain --file-system-id <file-system-id> --layer-ref experiment-a --output text
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)
- [`ti fs fork-layer`](/ai/ti/reference/ti-fs-fork-layer.md)