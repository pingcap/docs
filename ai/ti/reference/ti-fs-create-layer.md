---
title: ti fs create-layer
summary: file system にレイヤーを作成します。
---

# ti fs create-layer

file system のベースパス上に、分離された変更を記録するためのレイヤーを作成します。`--layer-id` を省略した場合、サービスが自動的に生成します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs create-layer
  --base-root-path <string>
  [--actor-id <string>]
  [--dry-run]
  [--durability-mode <string>]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--layer-id <string>]
  [--layer-name <string>]
  [--tag <string>]
  [--version]
```

## オプション {#options}

- `--base-root-path <string>`: TiDB Cloud file system 内のベースルートパスです。\[required]
- `--actor-id <string>`: レイヤーの所有者を識別するアクター ID です（例: エージェント名）。
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--durability-mode <string>`: レイヤーの耐久性モードを設定します。明示的にサポートされている値は `restore-safe` のみで、これを指定するとリモートレイヤー内の変更が保持され、ローカル環境の終了後もレイヤーを復元できます。省略した場合、サービスは `restore-safe` を使用します。
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: file system トークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、このコマンドは選択した file system 用にローカルに保存されているトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--layer-id <string>`: レイヤー ID です。通常はサービスによって自動生成されます。
- `--layer-name <string>`: レイヤーの名前です。
- `--tag <string>`: レイヤーのタグです。形式は `key=value` で、繰り返し指定できます。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- レイヤーを作成する:

    ```bash
    # Start an isolated writable view over the selected base root.
    ti fs create-layer --file-system-id <file-system-id> --base-root-path /workspace --layer-name agent-task
    ```

- restore-safe タグ付きレイヤーを作成する:

    ```bash
    # Request durable layer behavior and attach task metadata.
    ti fs create-layer --file-system-id <file-system-id> --base-root-path /workspace --durability-mode restore-safe --tag task=review
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)
