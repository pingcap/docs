---
title: TiDB Cloud CLI のリージョン、セキュリティ、および制限事項
summary: サポートされるリージョン、認証の境界、プラットフォーム依存関係、プレビュー時の制約、および Filesystem companion の動作について参照します。
---

# TiDB Cloud CLI のリージョン、セキュリティ、および制限事項

このリファレンスでは、現在の配置、認証、プラットフォーム、およびプレビューに関する境界について説明します。

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

設定したリージョンが TiDB Cloud Starter をサポートしていても TiDB Cloud Filesystem をサポートしていない場合、そのリージョンで Starter インスタンスを管理できます。Filesystem コマンドは `unsupported endpoint` エラーで失敗します。

サポートされる Filesystem リージョンは、各 `ti` リリースに組み込まれています。インストール済みバージョンのリリース後に追加されたリージョンで Filesystem を使用するには、`ti` をアップグレードしてください。サービス URL を指定しても、非サポートのリージョンを有効にすることはできません。

## 認証情報の要件 {#credential-requirements}

| 操作 | 必要な認証情報 |
| --- | --- |
| `ti configure`、すべての `ti db` コントロールプレーン操作 | TiDB Cloud API public/private キー |
| `ti fs create-file-system` | TiDB Cloud API キー |
| `ti fs delete-file-system` | TiDB Cloud API キーと file system ID |
| Filesystem の抽出および埋め込み設定の表示または更新 | TiDB Cloud API キーと明示的な file system ID |
| Filesystem トークンの生成、一覧表示、有効化、無効化、削除 | TiDB Cloud API キーと明示的な file system ID |
| Filesystem トークンの更新 | 現在の FS bearer トークンのみ |
| リモートの file、レイヤー、パック、マウント、Git、ジャーナル、およびオーナー vault 操作 | FS オーナートークンまたは登録済みリソース認証情報 |
| 委任された vault の read、list、run、またはマウント | スコープに適した委任された vault トークン |
| 成功したバックグラウンドマウント後の drain およびアンマウント | 同じ `HOME` 内の機密情報を含まないマウントロケーター |

TiDB Cloud API 呼び出しでは Digest 認証を使用します。SQL HTTPS 実行では、生成された SQL のユーザー名とパスワードによる Basic 認証を TLS 上で使用します。これらの認証情報は相互に置き換えできません。

## セキュリティのベストプラクティス {#security-best-practices}

- TiDB Cloud API キーは、ワークフローに必要なアクセス権のみを持つように作成してください。無人自動化で個人の管理者キーを再利用しないでください。
- 自動化用の認証情報は、CI のシークレットストアまたは実行時シークレットマネージャーから注入してください。認証情報をソース管理、コンテナイメージ、シェルスクリプト、またはプロセス一覧やシェル履歴に表示される可能性のあるコマンドライン引数に置かないでください。
- 完全な `~/.ti/` ディレクトリをエージェントのサンドボックスにコピーしないでください。既存の Filesystem には、`TI_FS_TOKEN` と `TI_REGION_CODE` のみを渡し、`TI_FS_FILE_SYSTEM_ID` は任意のアサーションとしてのみ使用してください。
- FS オーナートークンは、その Filesystem への完全アクセスとして扱ってください。エージェントが一部のシークレットのみを必要とする場合は、最も狭い field scope と実用上最短の TTL を持つ vault grant を作成し、代わりに委任された vault トークンを渡してください。
- マシン、CI ワークフロー、またはサンドボックスのクラスごとに別々の Filesystem トークンを使用してください。これにより、ある環境を無効化または失効しても、他の環境を中断せずに済みます。トークン名は運用上のラベルであり、一意識別子ではありません。トークンの変更は `token_id` でのみ行ってください。
- 生成または更新されたトークンの平文は、1 回しか返されないため、すぐに取得してください。`TI_FS_TOKEN` から更新されたトークンは、外部シークレットマネージャーには書き戻されません。更新は冪等ではないため、ネットワーク障害が曖昧な場合は再試行しないでください。
- 共有トークンのローテーションでは、まず置き換え用トークンを生成して配布し、アクセスを検証してから、古いトークンを無効化して削除してください。状態変更後、認証キャッシュが収束するまで約 10 秒かかります。
- AI プロバイダーキーは `TI_FS_AI_PROVIDER_API_KEY` を通じてのみ渡してください。TiDB Cloud CLI はこの値をローカルに永続化せず、Filesystem サービスはマスクされた形式でのみ返します。有効な設定を describe するまで、曖昧な障害後に AI 設定更新を再試行しないでください。
- 抽出を有効にすると、Filesystem のメディアが設定された抽出プロバイダーと共有されます。アプリケーション管理埋め込みを有効にすると、テキストまたは抽出された説明が設定された埋め込みプロバイダーと共有されます。いずれかの機能を有効にする前に、そのプロバイダーのデータ保持およびセキュリティ条件を確認してください。
- 信頼できないエージェントや探索的なエージェントによる SQL 調査には `--read-only` を使用してください。DDL または権限管理には `--admin` のみを使用し、データ変更を意図する場合にのみ `--read-write` を使用してください。
- 破壊的なコントロールプレーン操作の前に `--dry-run` を使用してください。`~/.ti/credentials`、リソース認証情報、および DB SQL 認証情報は、所有者のみが読み取り可能にしてください。
- `/dev/fuse`、`SYS_ADMIN`、および制限のない AppArmor プロファイルへの Docker アクセスは、Dedicated で信頼できるコンテナにのみ付与してください。これらの設定はコンテナ分離を弱めます。
- 診断情報を共有する前に、ローカルの操作ログを確認してください。ログには SQL テキスト、パス、ペイロード、認証情報の値は含まれませんが、コマンド名、フラグ名、プロファイルおよびリージョンのメタデータ、ステータスコード、操作タイミングは依然として機微情報となる可能性があります。

## マウントのプラットフォーム制限 {#mount-platform-limitations}

| プラットフォーム | Filesystem マウント | Vault マウント | 要件と代替手段 |
| --- | --- | --- | --- |
| macOS | デフォルトでは WebDAV、明示的な `--driver fuse` では FUSE | FUSE | 組み込みの WebDAV helper は Filesystem マウントをサポートします。FUSE または Vault マウントには macFUSE をインストールし、その system extension を承認してください。 |
| Linux | FUSE | FUSE | FUSE3 をインストールし、`/dev/fuse` へのアクセスを提供してください。WebDAV マウントはサポートされていません。 |
| Windows | 非サポート | 非サポート | 代わりに `ti fs` のデータプレーンコマンドと、マウントを使用しない Vault コマンドを使用してください。 |

FUSE と WebDAV は、同梱された [Drive9](https://github.com/mem9-ai/drive9) companion によって実装されています。TiDB Cloud CLI は、別個のネイティブマウント実装にはフォールバックしません。

Ubuntu 26.04 では、さらに AppArmor により `fusermount3` が制限されます。マウントパスには `$HOME` または `/mnt` 配下を使用してください。`/workspace` では、`ti` を root として実行している場合でも、明示的なローカル AppArmor ルールが必要です。

## 耐久性の制限事項 {#durability-limitations}

- デフォルトの FUSE 動作では、companion によって許可される場合、ローカルバッファリングと非同期のリモート処理を使用します。
- `unmount-file-system` が成功すると、FUSE の処理は正常に flush および drain されるため、事前に別途 drain は不要です。
- `drain-file-system` は、マウントをアクティブなままにする、FUSE 専用のオンライン耐久性バリアです。
- マウントプロセスを強制終了したり、マシンを削除したりすると、未コミットのメモリ/write-back 状態が失われる可能性があります。
- デフォルトの coding-agent マウントプロファイルは、依存関係ツリー、生成出力、キャッシュ、および Git 内部データをローカルに保存します。ローカル専用データは、パックされるか別の方法で保持されない限り、そのディスクが失われると消失します。
- 実行中のマウントは、マウント時に読み込まれた companion バージョンのまま動作し続けます。TiDB Cloud CLI を更新した後は、アンマウントして再度マウントしてください。
- リモートにコミット済みの Filesystem データは、クライアントまたはサンドボックスが削除されても保持されます。マシンを削除しても、リモートリソースは削除されません。

## 製品の制限事項 {#product-limitations}

- TiDB Cloud CLI はプレビュー段階であり、コマンドの仕様は変更される可能性があります。
- データベース管理の対象は TiDB Cloud Starter であり、すべての TiDB Cloud クラスタープランではありません。
- SQL 実行では、1 回の呼び出しにつき 1 つのステートメントのみ受け付けます。
- read-write はデフォルトの SQL ロールです。セキュリティに敏感な自動化では、明示的なロールフラグを使用してください。
- ジャーナルは追記専用であり、現在の公開コマンド体系にはジャーナルを削除するコマンドはありません。
- Filesystem の list および describe コマンドは、TiDB Cloud 認証情報を使用してリージョンスコープのリモートインベントリを照会します。リージョンをまたいで集約はしません。
- ローカル認証情報ストアは、プロファイルおよび Filesystem ごとに 1 つの選択済みトークンを保持します。すべてのリモートトークンをミラーリングするわけではありません。既知のトークン ID を持たない古い create/import 認証情報も引き続き使用できますが、リモートトークンメタデータと関連付けることはできません。
- Filesystem の抽出および埋め込みプロバイダー設定は任意です。未設定でも、リソース管理、ファイルアクセス、検索、レイヤー、Git、ジャーナル、vault、またはマウントワークフローは妨げられません。
- OpenAI プロバイダーインターフェースは、埋め込みと画像、音声、動画の抽出でサポートされます。Alibaba Cloud Model Studio Qwen ASR は音声抽出でのみサポートされます。その他のベンダーは、正確な OpenAI 互換コントラクトを通じた場合にのみ条件付きで互換性があります。ネイティブの Anthropic、Gemini、Vertex AI、Bedrock、および Azure OpenAI インターフェースはサポートされません。
- アプリケーション管理埋め込みには、正確に 1024 次元を返すプロバイダーモデルが必要です。`source=database_auto` を報告する Filesystem はデータベース管理埋め込みを使用しており、アプリケーション管理設定を拒否します。
- テレメトリー管理コマンドは意図的に実装されていません。テレメトリーは `~/.ti/.preferences` または `TI_TELEMETRY` で制御してください。サーバーレス関数のデプロイ、Homebrew、および Scoop 配布は実装されていません。
- TiDB Cloud CLI は、直接のファイル操作、レイヤー、マウント、Git ワークスペース、ジャーナル、および Vault 操作を含む、公開されているすべての Filesystem ランタイム動作について、インストール済みの `ti-drive9` companion に依存します。

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)
- [TiDB Cloud CLI の設定と認証情報](/ai/ti/reference/ti-configuration-and-credentials.md)
- [TiDB Cloud CLI のトラブルシューティング](/ai/ti/reference/ti-troubleshooting.md)
