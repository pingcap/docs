---
title: TiDB Cloud CLI (`ti`) コマンドリファレンス
summary: TiDB Cloud CLI のコマンドグループ、構文、グローバルオプション、出力、dry-run の動作、ヘルプ形式、エラーを参照します。
---

# TiDB Cloud CLI (`ti`) コマンドリファレンス

このページでは、[TiDB Cloud CLI (`ti`)](/ai/ti/ti-overview.md) コマンドに共通するコマンド構造と動作について説明します。個々のコマンドの構文とオプションについては、そのコマンドグループを選択するか、ドキュメントのナビゲーションを使用してください。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti <command> [options] [global options]
ti <command-group> <command> [options] [global options]
```

例:

```bash
ti configure --profile staging
ti db list-db-clusters --db-cluster-type starter
```

`ti` 実行ファイルはロングオプションのみを受け付けます。`-p` のような 1 文字のオプションは拒否されます。

生成される usage では、必須オプションを任意オプションより前に指定し、任意オプションは角括弧で囲みます。

```text
ti db describe-db-cluster
  --db-cluster-id <string>
  [--output <string>]
  [--view <string>]
```

値の型は山括弧で囲まれます。コマンドヘルプでは、各必須オプションの名前と型の後に `(required)` が付きます。

```text
--db-cluster-name <string> (required)   Starter DB cluster display name
--wait                                  Wait until the created cluster is active
```

## コマンドとコマンドグループ {#commands-and-command-groups}

次の表を使用して、トップレベルのコマンドまたはコマンドグループのリファレンスを見つけてください。各コマンドページには、構文、オプション、例が含まれています。

| コマンドまたはコマンドグループ | 目的 | リファレンス |
| --- | --- | --- |
| `configure` | ローカルプロファイル、API キー、デフォルトのリージョンを設定します。 | [`ti configure`](/ai/ti/reference/ti-configure.md) |
| `update` | TiDB Cloud CLI の更新を確認してインストールします。 | [`ti update`](/ai/ti/reference/ti-update.md) |
| `db` | TiDB Cloud Starter インスタンス、ブランチ、SQL ユーザー、接続、SQL ステートメントを管理します。 | [`ti db` コマンド](/ai/ti/reference/ti-starter-database.md) |
| `fs` | Filesystem リソース、AI プロバイダー、トークン、データ、レイヤー、マウントを管理します。 | [`ti fs` コマンド](/ai/ti/reference/ti-filesystem.md) |
| `fs-git` | マウントされた Filesystem 上の Git ワークスペースを管理します。 | [`ti fs-git` コマンド](/ai/ti/reference/ti-filesystem-git.md) |
| `fs-journal` | 検証可能な Filesystem ジャーナルを管理します。 | [`ti fs-journal` コマンド](/ai/ti/reference/ti-filesystem-journal.md) |
| `fs-vault` | Filesystem Vault シークレットと委任アクセスを管理します。 | [`ti fs-vault` コマンド](/ai/ti/reference/ti-filesystem-vault.md) |

ターミナルで使用可能なコマンドを一覧表示するには、`ti help` または `ti <command-group> help` を実行します。

## グローバルオプション {#global-options}

- `--debug`: 秘匿情報をマスクしたデバッグ出力を有効にします。
- `--output <string>`: 出力形式を `json` または `text` に設定します。\[default: json]
- `--profile <string>`: ローカルプロファイルを選択します。\[default: default]
- `--query <string>`: 出力をレンダリングする前に JMESPath 式を適用します。
- `--region <string>`: 現在のコマンドに対して、プロファイルのデフォルトリージョンコードを上書きします。例: `aws-us-east-1`

コマンドページでは、`--help`、`--version`、およびすべてのコマンド固有オプションを個別に説明しています。

## 出力 {#output}

構造化データを返すコマンドは、デフォルトで JSON を使用します。

```bash
ti db list-db-clusters --db-cluster-type starter
```

人が読みやすい形式で表示するには、text 出力を使用します。

```bash
ti db list-db-clusters --db-cluster-type starter --output text
```

`ti fs read-file` や `ti fs copy-file --to-stdout` のような生バイト指向のコマンドは、ファイル内容を直接書き出します。

## JMESPath クエリ {#jmespath-queries}

`--query` は、コマンドが正常に実行された後、出力がレンダリングされる前に実行されます。

```bash
ti db list-db-clusters \
  --db-cluster-type starter \
  --query 'clusters[].{id:id,name:display_name,state:state}'
```

式が無効な場合は失敗し、コマンド結果が部分的な出力に置き換えられることはありません。

## Dry-run {#dry-run}

`--dry-run` をサポートする変更系のコントロールプレーンコマンドは、ローカルオプション、プロファイル、認証情報、リージョン、およびリクエスト形状を検証したうえで、リモート変更を行わずに実行計画を報告します。

```bash
ti db delete-db-cluster \
  --db-cluster-id "<cluster-id>" \
  --dry-run
```

読み取り専用コマンドは `--dry-run` を拒否します。このオプションはグローバルなシミュレーションオプションではなく、コマンドヘルプに表示されている場合にのみ使用できます。

## ヘルプ形式とバージョン形式 {#help-and-version-forms}

コマンドを指定せずに `ti` を実行すると、終了コード `2` を返し、コンパクトなコマンドツリーの概要を標準エラー出力に出力します。

```text
ti [ERROR]: the following arguments are required: command

The TiDB Cloud Command Line Interface is a unified tool to manage your TiDB Cloud Filesystem (FS) and Starter services.

usage: ti <command> [<subcommand>] [parameters]
To see help information, you can run:

  ti help
  ti <command> help
  ti <command> <subcommand> help
```

コマンドとオプションを表示するには、明示的なヘルプ形式を使用します。

```bash
ti help
ti db help
ti db create-db-cluster help
ti --help
ti --version
```

`help` はコマンド階層をたどるためのコマンドです。`--help` は各コマンドで使用でき、両方の形式が意図的に共存しています。`--version` オプションも各コマンドレベルで使用でき、同じ `ti` 実行ファイルのバージョンを報告します。

## エラーと終了動作 {#errors-and-exit-behavior}

人が読めるエラーは空行で始まり、安定したプレフィックスを使用します。

```text
ti [ERROR]: <message>
```

エラーは標準エラー出力に書き込まれ、正常なコマンド出力は標準出力に書き込まれます。usage および設定の失敗は、リモート変更の前に非ゼロの終了コードを返します。実行時エラーおよびリモート API の失敗も非ゼロを返します。対話型設定が中断された場合は、終了コード `130` を返します。

`--debug` では、秘匿情報をマスクしたリクエストおよび解決コンテキストを表示できます。API キー、FS トークン、DB パスワード、SQL テキスト、ファイル内容、接続文字列を表示してはなりません。

## 関連ドキュメント {#related-documentation}

設定、セキュリティ、互換性、トラブルシューティングの詳細については、次のドキュメントを参照してください。

| ドキュメント | 目的 |
| --- | --- |
| [TiDB Cloud CLI のインストール、設定、更新](/ai/ti/reference/ti-install-configure-update.md) | リリースのインストール、プロファイルの設定、`ti` の更新とアンインストール |
| [TiDB Cloud CLI の設定と認証情報](/ai/ti/reference/ti-configuration-and-credentials.md) | プロファイル、優先順位ルール、認証情報、ローカル状態を理解する |
| [TiDB Cloud CLI のリージョン、セキュリティ、制限事項](/ai/ti/reference/ti-regions-security-and-limitations.md) | サポートされるリージョン、認証情報の境界、プラットフォームサポート、制限事項を確認する |
| [`tdc` から TiDB Cloud CLI への移行](/ai/ti/reference/ti-migrate-from-tdc.md) | `tdc` v0.1.x からローカル状態と環境変数を移行する |
| [TiDB Cloud CLI のトラブルシューティング](/ai/ti/reference/ti-troubleshooting.md) | 設定、認証、ルーティング、コマンド失敗を診断する |

## リリースノート {#release-notes}

TiDB Cloud CLI (`ti`) の最新の変更については、[TiDB Cloud CLI (`ti`) Release Notes](https://github.com/tidbcloud/ti-cli/releases) を参照してください。