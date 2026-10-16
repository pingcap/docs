---
title: TiDB Cloud BYOC オンボーディング概要
summary: TiDB Cloud BYOC のオンボーディングプロセスの概要。顧客と TiDB Cloud チームそれぞれの責任と手順について説明します。
---

# TiDB Cloud BYOC オンボーディング概要

TiDB Cloud BYOC (Bring Your Own Cloud) は、TiDB Cloud のフルマネージドな運用体験を維持しながら、データプレーンをお客様自身のクラウド環境で実行できるエンタープライズ向けソリューションです。

TiDB Cloud BYOC のデプロイプロセスは、お客様の組織と TiDB Cloud チームが共同で進める取り組みです。このプロセスには、安全なインフラストラクチャの準備、自動プロビジョニング、および包括的な検証が含まれます。BYOC のオンボーディングを開始するには、[営業担当にお問い合わせください](https://www.pingcap.com/contact-us/)。

<!--TO confirm: might need to state that currently only AWS is supported and the word AWS is not used in title for future content scale.-->

## デプロイフェーズ {#deployment-phases}

| フェーズ | 担当 | 説明 |
| :---- | :---- | :---- |
| [Phase 1: Environment preparation](/tidb-cloud/byoc/byoc-prepare-environment-aws.md) | Customer | デプロイに必要な AWS の基盤を準備します。これには、専用の AWS アカウントの作成、TiDB 用のパブリックまたはプライベート Route 53 ホストゾーンの設定、およびプライベート認証局 (PCA) のセットアップが含まれます。 |
| [Phase 2: IAM bootstrapping](/tidb-cloud/byoc/byoc-configure-iam-permissions.md) | Customer | 提供されたブートストラップスクリプトを実行して、必要な IAM ロールとポリシーをインストールします。これにより、TiDB Cloud コントロールプレーンが AWS アカウント内のリソースを安全に管理できるようになります。 |
| [Phase 3: Automated region deployment](/tidb-cloud/byoc/byoc-automated-deployment.md) | TiDB Cloud | IAM 権限の検証後、TiDB Cloud が VPC、EKS クラスター、およびコントロールプレーンリソースを自動的にプロビジョニングします。Note: このプロセスは **完全に自動化** されており、お客様による操作は不要です。 |
| [Phase 4: Service initialization](/tidb-cloud/byoc/byoc-initialize-service.md) | Customer | まずリソースプールを作成し、その後コンソールからリソースプール内に TiDB インスタンスを作成します。その後、[踏み台ホストを設定](/tidb-cloud/byoc/byoc-configure-bastion-host.md) し、認証スクリプトを構成して、安全なメンテナンスチャネル (Tailscale) と可観測性パイプラインを確立します。Note: 独自のカスタム方式を使用してメンテナンスチャネルを確立することもできます。 |
| [Phase 5: Validation](/tidb-cloud/byoc/joint-validation.md) | Joint | 両チームが連携して接続性を検証し、メトリクス収集を確認し、システムの健全性を確認することで、BYOC 環境が利用可能な状態であることを保証します。 |

> **Note:**
>
> 各フェーズでは、チーム間のタイムリーな連携が必要です。すべての段階を円滑に進めるために、両組織から専任の担当者を割り当てることを推奨します。

## アーキテクチャ概要 {#architecture-overview}

TiDB Cloud BYOC は、分離プレーンアーキテクチャを採用しています。TiDB Cloud のコントロールプレーンは PingCAP によって管理され、TiDB のデータプレーンはお客様自身のクラウドアカウント内で実行されます。

オンボーディングプロセスを開始する前に、[TiDB Cloud BYOC アーキテクチャ](/tidb-cloud/architecture-concepts.md#tidb-cloud-byoc) を確認し、BYOC のコントロールプレーン、データプレーン、ネットワーク接続モデル、および高可用性オプションについて理解してください。