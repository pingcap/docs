---
title: TiDB Cloud CLI (`ti`) の概要
summary: TiDB Cloud Starter インスタンスと TiDB Cloud Filesystem 内の file system を管理するために、TiDB Cloud CLI (`ti`) をいつ使用するかを学びます。
---

# TiDB Cloud CLI (`ti`) の概要

[TiDB Cloud CLI (`ti`)](https://github.com/tidbcloud/ti-cli) は、[TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier/?plan=starter#starter) インスタンスと [TiDB Cloud Filesystem 内の file system](#tidb-cloud-filesystem) を管理するための CLI です。対話的な利用と自動化の両方を想定して設計されており、デフォルトで構造化された JSON 出力を提供します。

> **Note:**
>
> - TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、事前の通知なく変更される場合があります。
> - TiDB Cloud は現在、対象範囲の異なる 2 つの CLI を提供しています: [`ti`](https://github.com/tidbcloud/ti-cli) と [`ticloud`](https://github.com/tidbcloud/tidbcloud-cli)。`ti` と `ticloud` をいつ使い分けるかについては、[`ti` と `ticloud` の違い](#differences-between-ti-and-ticloud) および [TiDB Cloud CLI (`ti`) を使用するタイミング](#when-to-use-tidb-cloud-cli-ti) を参照してください。

## TiDB Cloud Filesystem {#tidb-cloud-filesystem}

TiDB Cloud Filesystem は、AI エージェントおよび自動化ワークロード向けに設計されたサーバーレス分散ファイルシステムです。ローカルマシン、サンドボックス、または CI ランナーとは独立して利用可能な、永続的で共有可能なファイル名前空間を提供します。そのため、永続ストレージ、共有ワークスペース、AI エージェントのワークフローに役立ちます。

## TiDB Cloud CLI (`ti`) を使用するタイミング {#when-to-use-tidb-cloud-cli-ti}

ターミナル、スクリプト、CI ジョブ、または AI エージェント環境から TiDB Cloud を管理したい場合は、TiDB Cloud CLI (`ti`) を使用します。

| 一般的なユースケース | できること |
| --- | --- |
| TiDB Cloud Starter のライフサイクル操作を自動化する | TiDB Cloud Starter インスタンスとブランチを作成および管理し、準備完了まで待機し、結果を JSON として確認し、SQL ステートメントを実行し、ID によってリソースを削除できます。 |
| タスクごとに SQL 権限を分離する | 各コマンドでデータベースパスワードを扱うことなく、タスクごとに CLI 管理の read-only、read-write、または admin ID を使用できます。 |
| 環境をまたいでファイルを永続化して共有する | ローカルマシン、CI ジョブ、サンドボックス、その他の一時的な環境をまたいでファイルを利用可能な状態に保ち、直接のファイルコマンドまたはサポートされている FUSE および WebDAV マウントを通じて同じリモート名前空間にアクセスできます。 |
| 一時的な環境で file system を使用する | 信頼できるマシン上で file system をプロビジョニングし、その後 CLI プロファイルをコピーしたり TiDB Cloud API キーを提供したりすることなく、サンドボックスに file system トークンとリージョンコードを渡せます。 |
| 大規模な Git ワークスペースをより早く開始する | クリーンな Git データの hydration がバックグラウンドで継続している間に、リポジトリのファイルツリーを公開できます。 |
| エージェントの作業を記録して委任する | ジャーナルに追記専用かつハッシュチェーン化されたワークフローイベントを保存し、選択した vault フィールドへの一時的かつスコープ限定のアクセスを付与できます。 |

視覚的でガイド付きのワークフローには、[TiDB Cloud コンソール](https://tidbcloud.com/) を使用してください。TiDB Cloud Essential または `ti` がサポートしていない操作には、[`ticloud`](#differences-between-ti-and-ticloud) を使用してください。

## TiDB Cloud CLI が管理するもの {#what-tidb-cloud-cli-manages}

TiDB Cloud CLI は、次の機能領域をカバーします。

- **TiDB Cloud Starter**
    - インスタンスおよびブランチのライフサイクル操作
    - SQL ユーザーと接続情報
    - SQL ステートメントの実行
- **TiDB Cloud Filesystem**
    - file system のライフサイクルとファイル操作
    - FUSE および WebDAV マウント
    - レイヤー、パック、および Git ワークスペース
    - ジャーナルと vault
- **CLI 設定**
    - プロファイル、リージョン、およびローカル認証情報
    - CLI の更新
    - 出力フォーマットと JMESPath クエリ

ほとんどのリソースコマンドは、2 レベルのコマンドモデルに従います。

```text
ti <command-group> <operation>
```

たとえば、`ti db list-db-clusters --db-cluster-type starter`、`ti fs copy-file`、`ti fs-journal verify-journal` です。

また、トップレベルの `ti configure` および `ti update` コマンドを使用して、CLI を設定および管理することもできます。

## `ti` と `ticloud` の違い {#differences-between-ti-and-ticloud}

TiDB Cloud は現在、対象範囲の異なる 2 つの CLI を提供しています: `ti` と [`ticloud`](/tidb-cloud/cli-reference.md)。

`ti` は TiDB Cloud Starter を使った自動化と TiDB Cloud Filesystem の管理向けに設計されており、一方 `ticloud` は引き続き TiDB Cloud Essential と、`ti` では利用できない追加の TiDB Cloud 操作をサポートします。

| CLI | 最適な用途 | 主な特徴 |
| --- | --- | --- |
| `ti` | サポートされている TiDB Cloud Starter の自動化ワークフローと TiDB Cloud Filesystem | 自動化向けに設計されている。デフォルトで JSON を出力する。コマンドは非対話型ワークフローをサポートし、`ti configure` は対話的なプロンプトも可能。 |
| `ticloud` | TiDB Cloud Essential、既存の TiDB Cloud Starter ワークフロー、および `ti` では利用できない操作（データインポート、データエクスポート、監査ログ操作など） | `ti` では利用できない追加の TiDB Cloud 操作をサポートし、対話型モードと非対話型モードの両方に対応。 |

`ti` は `ticloud` を置き換えるものではありません。必要なリソースと操作に応じて CLI を選択してください。

- TiDB Cloud Starter を使った新しい自動化ワークフローでは、必要な操作を `ti` がサポートしている場合は `ti` を使用します。
- TiDB Cloud Filesystem を管理するには、`ti` を使用します。
- TiDB Cloud Starter または TiDB Cloud Essential 向けに既存の `ticloud` ワークフローがある場合は、それらを引き続き使用できます。
- TiDB Cloud Essential または `ti` では利用できない操作（データインポート、データエクスポート、監査ログ操作など）には、[`ticloud`](/tidb-cloud/cli-reference.md) を使用します。

## 次のステップ {#next-steps}

TiDB Cloud CLI を初めて使用する場合は、[TiDB Cloud CLI を使い始める](/ai/ti/ti-quick-start.md) から始めて、`ti` をインストールし、プロファイルを設定し、基本的な TiDB Cloud Starter または file system のワークフローを完了してください。

その後は、実施したい内容に応じて次に進んでください。

- [TiDB Cloud Starter インスタンスを管理する](/ai/ti/guides/manage-starter-instances.md)
- [TiDB Cloud CLI で TiDB Cloud Filesystem を使用する](/ai/ti/guides/manage-filesystems-via-cli.md)
- **エンドツーエンドのワークフローに従う**: [日次の TiDB Cloud CLI ワークフローを実行する](/ai/ti/guides/ti-daily-workflow-example.md) または [エージェントサンドボックスで TiDB Cloud Filesystem を使用する](/ai/ti/guides/ti-agent-sandbox-example.md) から始めてください
- **特定のコマンドを調べる**: [TiDB Cloud CLI コマンドリファレンス](/ai/ti/reference/ti-cli-reference.md) を確認してください
- **TiDB Cloud CLI の新機能を確認する**: [TiDB Cloud CLI (`ti`) Release Notes](https://github.com/tidbcloud/ti-cli/releases) を確認してください
- **問題を報告する**: [TiDB Cloud CLI GitHub repository](https://github.com/tidbcloud/ti-cli/issues) で issue を作成してください。
