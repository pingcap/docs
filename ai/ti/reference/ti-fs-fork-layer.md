---
title: ti fs fork-layer
summary: ファイルシステムで copy-on-write の子レイヤーをフォークします。
---

# ti fs fork-layer

親レイヤーの現在の状態、またはそのチェックポイントの 1 つから、書き込み可能な子レイヤーを作成します。子レイヤーへの変更は親レイヤーを変更しません。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs fork-layer
  --parent-layer-ref <string>
  [--actor-id <string>]
  [--checkpoint-id <string>]
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--layer-id <string>]
  [--layer-name <string>]
  [--version]
```

## オプション {#options}

- `--parent-layer-ref <string>`: 親レイヤー ID、一意の名前、または [タグ参照](/ai/ti/reference/ti-filesystem.md#layer-references)。\[required]
- `--actor-id <string>`: 子の所有者を識別するアクター ID。
- `--checkpoint-id <string>`: 子を親のこのチェックポイントに固定します。省略した場合は、シリアライズされた親の tip に固定されます。
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: ファイルシステム トークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、このコマンドは選択したファイルシステム用にローカルに保存されたトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--layer-id <string>`: 安定した子レイヤー ID。省略した場合、サービスが生成します。
- `--layer-name <string>`: 人が判読しやすい子レイヤー名。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- 親の tip からフォークする場合:

    ```bash
    # Start an independent writable timeline at the parent's current serialized tip.
    ti fs fork-layer --file-system-id <file-system-id> --parent-layer-ref research-base --layer-name experiment-a --actor-id agent-a
    ```

- 安定したチェックポイントからフォークする場合:

    ```bash
    # Continue from an earlier review boundary without changing the original timeline.
    ti fs fork-layer --file-system-id <file-system-id> --parent-layer-ref research-base --checkpoint-id seed --layer-name experiment-b --actor-id agent-b
    ```

> **Note:**
>
> レイヤー名は論理削除後も表示されたままとなり、曖昧になる可能性があります。自動化では、返されたレイヤー ID を取得して使用する必要があります。

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)
- [`ti fs mount-file-system`](/ai/ti/reference/ti-fs-mount-file-system.md)
