---
title: ti fs generate-file-system-scoped-token
summary: 1 つの TiDB Cloud Filesystem に対して、パスと操作が制限されたトークンを生成します。
---

# ti fs generate-file-system-scoped-token

オーナートークンから、パスと操作アクセスが制限されたスコープ付きトークンを生成します。トークン値はコマンド出力にのみ表示され、後から取得することはできません。スコープ付きトークンは、許可されたパスプレフィックスと操作にのみアクセスできます。

スコープ付きトークンは、要求されたパスと操作が許可範囲に含まれている場合に限り、通常のファイル、アップロード、レイヤー、およびマウント操作をサポートします。`chmod`、Git ワークスペース API、ジャーナル、Vault、SQL、フォーク、イベント、およびトークン管理操作は、スコープ付きトークンでは利用できません。スコープ付きトークンは、スコープを変更せずに自身を更新できます。

各操作の意味は次のとおりです。コマンドによっては、コピー元に対する `read` とコピー先に対する `write` のように、複数の操作が必要になる場合があります。

| 操作 | 許可される内容 |
| --- | --- |
| `read` | ファイル内容とメタデータの読み取り。 |
| `list` | ディレクトリ配下のエントリ一覧表示。 |
| `search` | プレフィックス配下のファイルの検索または検出。`read` が必要です。 |
| `write` | ファイル、ディレクトリ、リンク、およびコピー先の作成または変更。 |
| `delete` | パスの削除、または move 中のソースパスの削除。 |

> **Important:**
>
> 検索を許可する場合は、同じ `--allow` 値に `search` と `read` の両方を含めてください。CLI は、`read` を含まない `search` を含むスコープを拒否します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。その機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs generate-file-system-scoped-token
  --ttl <duration>
  --allow <prefix:ops>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--subject <string>]
  [--store-locally]
  [--replace]
  [--dry-run]
  [--help]
  [--version]
```

## オプション {#options}

- `--ttl <duration>`: 秒単位に解決される有限の正のトークン有効期間を設定します。このオプションは必須です。
- `--allow <prefix:ops>`: 1 つのリモートパスプレフィックス配下で許可する操作を指定します。複数のプレフィックスを指定するには、このオプションを繰り返します。操作には `read`、`list`、`search`、`write`、`delete` があり、`search` には `read` が必要です。このオプションは必須です。
- `--file-system-id <string>`: オーナートークンに埋め込まれた file system ID を検証します。このオプションは、ローカルに保存されたオーナートークンを読み込む場合にのみ必須です。
- `--fs-token <string>`: file system オーナートークンを指定します。省略した場合、コマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、コマンドは選択された file system 用にローカル保存されたトークンを使用します。
- `--subject <string>`: 最大 64 バイトの任意のサーバー側監査ラベルを設定します。これは一意のセレクターではありません。
- `--store-locally`: このプロファイルと file system 用に、生成されたスコープ付きトークンを保存して選択します。
- `--replace`: 既存の選択済みローカルトークンを置き換えます。`--store-locally` が必要であり、以前のリモートトークンは失効されません。
- `--dry-run`: トークンを生成せずに、オーナー認証情報、リージョン、有効期間、スコープ、およびローカル保存の前提条件を検証します。
- `--help`: ヘルプ情報を表示します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- 1 つのワークスペースに対してサンドボックスに読み取りおよび書き込みアクセスを付与します。

    ```bash
    # Inject the owner TI_FS_TOKEN from a secret manager, then create a token limited to /workspace.
    ti fs generate-file-system-scoped-token \
      --subject sandbox-agent \
      --ttl 24h \
      --allow /workspace:read,list,write
    ```

- 書き込み可能なワークスペースデータと読み取り専用のアーティファクトを分離します。

    ```bash
    # Inject the owner TI_FS_TOKEN from a secret manager. Repeat --allow to assign different operations to independent prefixes.
    ti fs generate-file-system-scoped-token \
      --ttl 8h \
      --allow /workspace:read,list,write,delete \
      --allow /artifacts:read,list
    ```

- 後続のローカルコマンド用に、生成されたスコープ付きトークンを選択します。

    ```bash
    # Replacing the local selection does not revoke the previous remote owner token.
    ti fs generate-file-system-scoped-token \
      --file-system-id "<file-system-id>" \
      --ttl 1h \
      --allow /task:read,list,write \
      --store-locally \
      --replace
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)
- [`ti fs generate-file-system-token`](/ai/ti/reference/ti-fs-generate-file-system-token.md)
- [`ti fs refresh-file-system-token`](/ai/ti/reference/ti-fs-refresh-file-system-token.md)
