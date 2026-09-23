---
title: ti fs delete-layer
summary: ファイルシステムのレイヤーを放棄します。
---

# ti fs delete-layer

履歴を消去せずにレイヤーを放棄します。レイヤーに有効な子孫レイヤーがある場合、先にそれらの子孫を放棄する `--cascade` を指定しない限り、このコマンドは失敗します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs delete-layer
  --layer-ref <string>
  [--cascade]
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## オプション {#options}

- `--layer-ref <string>`: レイヤー ID、一意の名前、または[タグ参照](/ai/ti/reference/ti-filesystem.md#layer-references)。\[required]
- `--cascade`: 選択したレイヤーを放棄する前に、有効な子孫レイヤーを放棄します。
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: ファイルシステムトークンを設定します。省略した場合、コマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、コマンドは選択したファイルシステム用にローカルに保存されたトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options)を参照してください.

## 例 {#examples}

- 却下されたリーフタイムラインを放棄する:

    ```bash
    # Deletion fails when the selected layer still has live descendants.
    ti fs delete-layer --file-system-id <file-system-id> --layer-ref experiment-a
    ```

- テスト所有のサブツリーを放棄する:

    ```bash
    # Cascade is explicit and abandons descendants before the selected layer.
    ti fs delete-layer --file-system-id <file-system-id> --layer-ref experiment-root --cascade
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)
- [`ti fs list-layer-chain`](/ai/ti/reference/ti-fs-list-layer-chain.md)