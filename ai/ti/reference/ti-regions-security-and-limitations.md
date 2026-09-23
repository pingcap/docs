---
title: TiDB Cloud CLI のリージョン、セキュリティ、および制限事項
summary: サポートされるリージョン、認証の境界、セキュリティのベストプラクティス、および現在の TiDB Cloud CLI の制限事項について参照します。
---

# TiDB Cloud CLI のリージョン、セキュリティ、および制限事項

このリファレンスでは、TiDB Cloud CLI の現在のリージョン、認証、プラットフォーム、およびプレビューに関する境界について説明します。ファイルシステムのリージョンと制限事項については、[TiDB Cloud Filesystem Regions and Limitations](/tidb-cloud-filesystem/filesystem-regions-and-limitations.md) を参照してください。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## サポートされるリージョン {#supported-regions}

TiDB Cloud CLI を使用する場合、CLI 操作のデフォルトリージョンを設定する必要があります。

次の表は、TiDB Cloud CLI でサポートされるリージョンと、各リージョンで利用可能な TiDB Cloud CLI サービスを示しています。

| プロバイダー | 場所 | 正規リージョンコード | TiDB Cloud Starter | TiDB Cloud Filesystem |
| --- | --- | --- | --- | --- |
| AWS | 北バージニア | `aws-us-east-1` | サポート対象 | サポート対象 |
| AWS | オレゴン | `aws-us-west-2` | サポート対象 | サポート対象 |
| AWS | シンガポール | `aws-ap-southeast-1` | サポート対象 | サポート対象 |
| AWS | フランクフルト | `aws-eu-central-1` | サポート対象 | 非サポート |
| AWS | 東京 | `aws-ap-northeast-1` | サポート対象 | 非サポート |
| Alibaba Cloud | シンガポール | `alicloud-ap-southeast-1` | サポート対象 | サポート対象 |

設定したリージョンが TiDB Cloud Starter をサポートしていても TiDB Cloud Filesystem をサポートしていない場合、そのリージョンで Starter インスタンスを管理できます。File system コマンドは `unsupported endpoint` エラーで失敗します。

サポートされる file system リージョンは、各 `ti` リリースに組み込まれています。インストール済みバージョンのリリース後に追加されたリージョンで file system を使用するには、`ti` をアップグレードしてください。サービス URL を指定しても、非サポートのリージョンを有効にすることはできません。

## 認証情報の要件 {#credential-requirements}

| 操作 | 必要な認証情報 |
| --- | --- |
| `ti configure`、すべての `ti db` コントロールプレーン操作 | TiDB Cloud API public/private キー |
| `ti fs create-file-system` | TiDB Cloud API キー |
| `ti fs delete-file-system` | TiDB Cloud API キーと file system ID |
| file system の抽出および埋め込み設定の表示または更新 | TiDB Cloud API キーと明示的な file system ID |
| file system トークンの生成、一覧表示、有効化、無効化、削除 | TiDB Cloud API キーと明示的な file system ID |
| file system トークンの更新 | 現在の FS bearer トークンのみ |
| リモートの file、レイヤー、パック、マウント、Git、ジャーナル、およびオーナー vault 操作 | FS オーナートークンまたは登録済みリソース認証情報 |
| 委任された vault の read、list、run、またはマウント | スコープに適した委任された vault トークン |
| 成功したバックグラウンドマウント後の drain およびアンマウント | 同じ `HOME` 内の機密情報を含まないマウントロケーター |

TiDB Cloud API 呼び出しでは Digest 認証を使用します。SQL HTTPS 実行では、生成された SQL のユーザー名とパスワードによる Basic 認証を TLS 上で使用します。これらの認証情報は相互に置き換えできません。

## セキュリティのベストプラクティス {#security-best-practices}

- TiDB Cloud API キーは、ワークフローに必要なアクセス権のみを持つように作成してください。無人自動化で個人の管理者キーを再利用しないでください。
- 自動化用の認証情報は、CI のシークレットストアまたは実行時シークレットマネージャーから注入してください。認証情報をソース管理、コンテナイメージ、シェルスクリプト、またはプロセス一覧やシェル履歴に表示される可能性のあるコマンドライン引数に置かないでください。
- 完全な `~/.ti/` ディレクトリをエージェントのサンドボックスにコピーしないでください。既存の file system には、`TI_FS_TOKEN` と `TI_REGION_CODE` のみを渡し、`TI_FS_FILE_SYSTEM_ID` は任意のアサーションとしてのみ使用してください。
- 信頼できないエージェントや探索的なエージェントによる SQL 調査には `--read-only` を使用してください。DDL または権限管理には `--admin` のみを使用し、データ変更を意図する場合にのみ `--read-write` を使用してください。
- 破壊的なコントロールプレーン操作の前に `--dry-run` を使用してください。`~/.ti/credentials`、リソース認証情報、および DB SQL 認証情報は、所有者のみが読み取り可能にしてください。
- 診断情報を共有する前に、ローカルの操作ログを確認してください。ログには SQL テキスト、パス、ペイロード、認証情報の値は含まれませんが、コマンド名、フラグ名、プロファイルおよびリージョンのメタデータ、ステータスコード、操作タイミングは依然として機微情報となる可能性があります。

file system トークン、マウント、Vault、および AI プロバイダーのセキュリティについては、[Authorization](/tidb-cloud-filesystem/filesystem-authorization.md)、[Manage File System Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md)、および [Configure AI Providers for a File System](/tidb-cloud-filesystem/configure-filesystem-ai-providers.md) を参照してください。

## 製品の制限事項 {#product-limitations}

- TiDB Cloud CLI はプレビュー段階であり、コマンドの仕様は変更される可能性があります。
- データベース管理の対象は TiDB Cloud Starter インスタンスであり、他の TiDB Cloud データベースプランではありません。
- SQL 実行では、1 回の呼び出しにつき 1 つのステートメントのみ受け付けます。
- read-write はデフォルトの SQL ロールです。セキュリティに敏感な自動化では、明示的なロールフラグを使用してください。
- テレメトリー管理コマンドは意図的に実装されていません。テレメトリーは `~/.ti/.preferences` または `TI_TELEMETRY` で制御してください。サーバーレス関数のデプロイ、Homebrew、および Scoop 配布は実装されていません。

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem Regions and Limitations](/tidb-cloud-filesystem/filesystem-regions-and-limitations.md)
- [TiDB Cloud CLI の設定と認証情報](/ai/ti/reference/ti-configuration-and-credentials.md)
- [TiDB Cloud CLI のトラブルシューティング](/ai/ti/reference/ti-troubleshooting.md)
