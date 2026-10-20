---
title: TiDB Cloud Filesystem SDKs
summary: TiDB Cloud Filesystem と Drive9 ワークスペースエンジンの関係を理解し、6 つのプログラミング言語向けクライアント SDK ドキュメントを確認します。
---

# TiDB Cloud Filesystem SDKs

TiDB Cloud Filesystem は、ファイルシステム操作を実行するために Drive9 ワークスペースエンジンを使用します。TiDB Cloud Filesystem は、TiDB Cloud 上で提供される PingCAP 公式のホスト型 Drive9 サービスです。Drive9 は PingCAP が所有するオープンソースのコミュニティベースプロジェクトであり、TiDB Cloud Filesystem はそのマネージドクラウドサービスです。API レイヤーおよび SDK レイヤーでは、TiDB Cloud Filesystem サービスによって公開される drive9 エンドポイントを直接呼び出します。

Drive9 は、[mem9-ai/drive9 リポジトリ](https://github.com/mem9-ai/drive9) で管理されているオープンソースプロジェクト（Apache 2.0）です。ワークスペースエンジンに加えて、このリポジトリでは複数のプログラミング言語向けクライアント SDK も公開しています。SDK とそのドキュメントもこのリポジトリで管理されているため、このページに記載されているガイドが、SDK のインストール、設定、および API の詳細に関する信頼できる情報源です。

SDK ガイドでは、サーバー URL と API キーの指定方法を含め、クライアントが Drive9 サーバーに接続する方法を説明しています。

次の表は、使用する TiDB Cloud Filesystem 認証情報を示しています。SDK ガイドで API キーの入力を求められた場合は、ファイルシステムトークンを使用してください。

|TiDB Cloud Filesystem のオブジェクト|Drive9 SDK/API での用途|
|:--|:--|
|TiDB Cloud API キー|ファイルシステムのコントロールプレーン操作|
|ファイルシステムトークン|ファイルシステムのデータプレーン操作|

各 TiDB Cloud Filesystem リージョンでは、次のサーバー URL を使用します。

| TiDB Cloud Filesystem のリージョン| Drive9 SDK/API のサーバー URL | API キー|
|:--|:--|:--|
|`aws-us-east-1`|`https://aws-us-east-1.drive9.ai`| FS トークン|
|`aws-us-west-2`|`https://aws-us-west-2.drive9.ai`| FS トークン|
|`aws-ap-southeast-1`|`https://aws-ap-southeast-1.drive9.ai`| FS トークン|
|`gcp-us-east1`|`https://gcp-us-east1.drive9.ai`| FS トークン|
|`azure-centralus`|`https://azure-centralus.drive9.ai`|FS トークン|
|`alicloud-ap-southeast-1`|`https://alicloud-ap-southeast-1.drive9.ai`|FS トークン|

SDK のサーバー URL は、必ずファイルシステムが配置されているリージョンのエンドポイントに設定してください。サーバー URL を設定しない場合、多くの SDK は `https://api.drive9.ai` にフォールバックしますが、これは TiDB Cloud Filesystem のエンドポイントではなく、TiDB Cloud Filesystem トークンを受け付けません。ファイルシステムトークンは、自身のリージョンのエンドポイントでのみ使用できます。

## 利用可能な SDK {#available-sdks}

| 言語 | リポジトリの場所 | ドキュメント |
| --- | --- | --- |
| TypeScript | `clients/drive9-js` | [TypeScript SDK 統合ガイド](https://github.com/mem9-ai/drive9/blob/main/docs/guides/typescript-sdk-integration.md) |
| Go | `pkg/client` | [Go SDK 統合ガイド](https://github.com/mem9-ai/drive9/blob/main/docs/guides/go-sdk-integration.md) |
| Python | `clients/drive9-py` | [drive9-py README](https://github.com/mem9-ai/drive9/blob/main/clients/drive9-py/README.md) |
| Rust | `clients/drive9-rs` | [drive9-rs README](https://github.com/mem9-ai/drive9/blob/main/clients/drive9-rs/README.md) |
| Kotlin | `clients/drive9-kotlin` | [drive9-kotlin README](https://github.com/mem9-ai/drive9/blob/main/clients/drive9-kotlin/README.md) |
| Swift | `clients/drive9-swift` | [drive9-swift README](https://github.com/mem9-ai/drive9/blob/main/clients/drive9-swift/README.md) |

SDK は Drive9 プロジェクトとともに開発およびリリースされるため、TiDB Cloud Filesystem サービスより先行する場合があります。TiDB Cloud Filesystem のワークロードで SDK を採用する前に、現在のサーバーエンドポイント、認証情報、およびサポートされている操作について、そのドキュメントを確認してください。

## 次のステップ {#what-s-next}

- CLI のインストール、設定、更新については、[TiDB Cloud CLI (`ti`)](/ai/ti/ti-quick-start.md) を参照してください。
- コマンドラインからファイルシステムデータを管理するには、[ファイルとディレクトリの操作](/tidb-cloud-filesystem/work-with-filesystem-data.md) を参照してください。
- 自動化ワークフローでファイルシステムを使用するには、[自動化と AI エージェントのワークフロー](/tidb-cloud-filesystem/use-filesystem-for-automation-and-ai-agents.md) を参照してください。