---
title: AWS で BYOC 環境を準備する
summary: TiDB Cloud BYOC のデプロイに必要なインフラストラクチャ コンポーネントを準備するための手順。
---

# AWS で BYOC 環境を準備する

BYOC のデプロイを開始する前に、AWS 環境で必要なインフラストラクチャ コンポーネントを準備します。以下の手順を順番に完了してください。

## Step 1. TiDB Cloud Organization ID を取得する {#step-1-retrieve-tidb-cloud-organization-id}

TiDB Cloud 内で組織を一意に識別する ID です。

1. [TiDB Cloud console](https://tidbcloud.com/) にログインします。

    TiDB Cloud アカウントをお持ちでない場合は、[こちら](https://tidbcloud.com/free-trial) をクリックしてサインアップしてください。メールアドレスとパスワードを使用して TiDB Cloud の認証情報を管理することも、Google、GitHub、または Microsoft アカウント経由のシングルサインオン (SSO) を使用することもできます。

2. 左側のナビゲーションペインで、プロフィールアイコン > **Organization Settings** をクリックします。

3. **Organization Information** の下で、**Organization ID** をコピーし、後で使用できるよう保存します。

## Step 2. AWS アカウントを準備する {#step-2-prepare-an-aws-account}

分離の確保、コンプライアンス対応の簡素化、正確なコスト管理のために、BYOC 環境専用の **dedicated AWS account** を使用することを強く推奨します。

- **Account ID:** 12 桁の AWS Account ID を用意してください。
- **Permissions:** IAM ロールと Route 53 を設定するために、AdministratorAccess または同等の権限があることを確認してください。

## Step 3. リージョンとアベイラビリティゾーン (AZ) を選択する {#step-3-select-region-and-availability-zones-azs}

TiDB は分散データベースであり、高可用性を実現するために特定のインフラストラクチャが必要です。

1. **Region:** データベースをデプロイする AWS リージョンを選択します。
2. **Availability zones (AZs):** デプロイの目的に応じて、次のいずれかの構成を選択します。

    - **Option A: 本番環境 (Multi-AZ).** 選択したリージョンで少なくとも **3 つの AZ** を特定する必要があります。たとえば、`us-west-2a`、`us-west-2b`、`us-west-2c` です。

    - **Option B: POC / コスト最適化 (Single-AZ).** **1 つの AZ** を正確に選択します。たとえば、`us-west-2a` です。

BYOC リージョン用に準備したアベイラビリティゾーンによって、TiDB Cloud がリソースプールを配置する場所が決まります。リソースプールの作成時には、**Zonal** または **Regional** の高可用性を選択します。Zonal リソースプールは 1 つのアベイラビリティゾーンに配置されます。Regional リソースプールには、そのリージョン内で少なくとも 3 つの適格なアベイラビリティゾーンが必要です。

BYOC リージョンが最初に単一のアベイラビリティゾーンで準備された場合、TiDB Cloud はそのアベイラビリティゾーンを Zonal リソースプールに使用します。Regional リソースプールは、追加で 2 つの適格なアベイラビリティゾーンが利用可能になった場合にのみ作成できます。Regional リソースプールの使用を予定している場合は、環境準備の段階で、そのリージョンに少なくとも 3 つの適格なアベイラビリティゾーンがあることを確認してください。

## Step 4. TiDB 用の hosted zone を作成する {#step-4-create-a-hosted-zone-for-tidb}

TiDB サービス DNS 用に Amazon Route 53 hosted zone を 1 つ作成します。observability (O11Y) 用の hosted zone を用意する必要はありません。

次の hosted zone タイプのいずれかを選択してください。

- **Public hosted zone:** TiDB へのパブリック接続とプライベート接続の両方をサポートします。[Creating a public hosted zone in AWS documentation](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/CreatingHostedZone.html) に従ってください。
- **Private hosted zone:** プライベート接続のみをサポートします。private hosted zone を選択した場合、BYOC 環境ではパブリック接続を利用できません。[Working with private hosted zones](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zones-private.html) に従ってください。

TiDB hosted zone には、38 文字以下の名前を使用してください。たとえば、`byoc.cluster.example.com` です。

public hosted zone の場合は、Route 53 のネームサーバー (NS) レコードを親 DNS 設定に追加して、親ドメインからその zone を委任してください。private hosted zone の場合は、DNS 名前解決が必要な VPC にその hosted zone を関連付けてください。

> **Note:**
>
> 複数の AWS リージョンに TiDB Cloud BYOC をデプロイする予定がある場合は、すべてのリージョンで同じ TiDB hosted zone を共有することも、リージョンごとに専用の hosted zone を使用することもできます。詳細は [Multi-Region Deployment](/tidb-cloud/byoc/multi-region-deployment.md) を参照してください。

## Step 5. private certificate authority (PCA) を設定する {#step-5-set-up-private-certificate-authority-pca}

TiDB Cloud は、証明書の発行に AWS private certificate authority (PCA) サービスを使用し、デジタル証明書の管理に AWS Certificate Manager (ACM) サービスを使用することで、mTLS を介した内部データベース クラスター コンポーネント間の安全な通信を確保します。

コンプライアンス要件を満たすために、TiDB Cloud BYOC は、お客様が提供する PCA と統合し、企業独自のドメインを使用してデータノード用の ID 証明書を発行します。これにより、すべての暗号化通信の信頼のルートが、お客様の組織の管理下に厳密に維持されます。

そのため、デプロイ先リージョンに有効な subordinate CA を準備する必要があります。TiDB Cloud に提供する CA ARN は、subordinate CA の ARN である必要があります。subordinate CA を作成して有効化するには、その証明書に署名するための有効な root CA が必要です。

subordinate CA 証明書の有効期間は少なくとも **20 年** である必要があります。subordinate CA 証明書への署名に使用する root CA が、この有効期間をサポートしていることを確認してください。

次の手順を実行してください。

1. **subordinate CA を作成する。** [Create a private CA in AWS Private CA](https://docs.aws.amazon.com/privateca/latest/userguide/create-CA.html) に従ってください。

    設定: CA タイプとして **Subordinate CA** を選択します。root CA ARN は TiDB Cloud に提供しないでください。

2. **subordinate CA 証明書をインストールする。** [Installing the CA certificate](https://docs.aws.amazon.com/privateca/latest/userguide/PCACertInstall.html) に従ってください。

3. **ARN を記録する。** **Subordinate CA ARN** をコピーします。

    例: `arn:aws:acm-pca:us-west-2:123456789012:ca/abcd-1234...`

4. AWS コンソールで **PCA 情報を確認** します。

<!--To confirm: image screenshot-->

> **Note:**
>
> - **POC またはコスト最適化の場合**: Proof of Concept (POC) フェーズでは、コストを削減するために AWS Private CA の代わりに Self-Signed Certificates を使用することもできます。このオプションに関する具体的な設定手順については、TiDB Cloud Support Representative に直接お問い合わせください。
> - **マルチリージョン デプロイの場合**: hosted zone と同様に、同じ private certificate authority (PCA) をマルチリージョン デプロイのすべてのリージョンで共有できます。あるいは、新しいリージョンごとに専用の PCA を作成することもできます。詳細は [Multi-Region Deployment](/tidb-cloud/byoc/multi-region-deployment.md) を参照してください。

## Step 6. ネットワーク CIDR 範囲を計画する {#step-6-plan-network-cidr-ranges}

BYOC のデプロイを開始する前に、observability (O11Y) インフラストラクチャとリソースプール用の専用プライベート CIDR 範囲を計画してください。プレフィックス長は `/16` から `/22` の間を使用します。

各 BYOC デプロイリージョンには 1 つの O11Y CIDR があります。リソースプール CIDR は、各リソースプールの作成時にそのリソースプールごとに設定されます。BYOC 環境と将来のリソースプールをネットワーク競合なしでプロビジョニングできるように、デプロイ前にこれらの CIDR 範囲を計画してください。

次の情報を準備してください。

| 項目 | 説明 | 例 |
| ----- | ----- | ----- |
| O11Y CIDR | デプロイリージョン内の observability インフラストラクチャおよび関連サービス用に予約される CIDR 範囲。 | `10.1.0.0/22` |
| Resource pool CIDR | リソースプール用に予約される CIDR 範囲。各リソースプールは独自の CIDR を持ち、リソースプール作成後は変更できません。 | `10.10.0.0/16` |

**CIDR 計画のルールと制約**

CIDR 範囲を計画する際は、次の接続ルールに従ってください。

- **内部分離:** 同じリージョン内では、リソースプール CIDR は O11Y CIDR とも、相互にも重複してはいけません。

- **VPC peering ルール:**

    * **重複不可:** O11Y CIDR および任意のリソースプール CIDR は、既存のアプリケーション VPC、オンプレミス ネットワーク、または VPN ネットワークと重複してはいけません。
    * **お客様の責任:** TiDB Cloud は、お客様が管理するネットワークとの競合を検出できません。これらの CIDR 範囲の計画と検証は、デプロイ前またはリソースプール作成前にお客様の責任で行ってください。

- **クロスリージョン CIDR 計画:** 異なるリージョンのリソースプール CIDR は重複していてもかまいません。ただし、クロスリージョン接続またはレプリケーションが必要なリソースプールには、重複しない CIDR を使用してください。

- **リソースプール間レプリケーション (重要):** 複数のリソースプールをデプロイし、**異なるリソースプール内のインスタンス間でデータをレプリケートする必要が生じる可能性がある** 場合 (たとえば、ディザスタリカバリやデータ統合のために TiCDC を使用する場合)、それぞれのリソースプール CIDR 範囲は **重複してはいけません**。

自動リージョン デプロイが開始される前に、計画した CIDR 範囲を TiDB Cloud 担当者に提供してください。

## Summary: 必要な情報 {#summary-required-information}

以下の表に、上記の手順で収集した情報を記入し、デプロイを開始するために TiDB Cloud 担当者と共有してください。

**必要な情報:**

| Category | 提供する詳細 | 例 | コメント |
| :---- | :---- | :---- | :---- |
| **TiDB Cloud Organization ID** | TiDB Cloud 組織の一意識別子 | `1372813089209270552` | Step 1 |
| **AWS Account ID** | 12 桁の AWS アカウント番号 | `123456789012` | Step 2 |
| **AWS Region** | デプロイ用に選択したリージョン | `us-west-2`, `us-east-1`, `us-east-2` | Step 3. マルチリージョン デプロイの場合は、すべてのリージョンを列挙してください。 |
| **Availability Zones** | リージョンごとに 3 つの AZ または単一 AZ (名前と ID を指定) | **Us-east-1:** `us-east-1a`, `use1-az1`, `us-east-1b`, `use1-az2`, `us-east-1c`, `use1-az4`; **Us-east-2:** `us-east-2a`, `use2-az1`, `us-east-2b`, `use2-az2`, `us-east-2c`, `use2-az3`; **Us-west-2:** `us-west-2a`, `usw2-az1` | Step 3. 選択した**各**リージョンで AZ 数の要件を満たすよう注意してください。 |
| **Subordinate CA ARN** | AWS ACM Private CA ARN | `arn:aws:acm-pca:us-west-2:123456789012:ca/abcd-1234` | Step 5. この ARN は複数リージョンで共有できます。 |
| **Hosted Zone Name & Hosted Zone ID** | TiDB hosted zone。public hosted zone または private hosted zone のいずれかを指定できます。 | **Hosted TiDB zone name:** `clusters.byoc-0929.pingcap.net`; **Hosted TiDB zone ID:** `Z1039122VAY4T8UNWR8E`. | Step 4. hosted zone は複数リージョンで共有できます。 |
| **CIDR** | O11Y インフラストラクチャおよびリソースプール用にお客様が計画した CIDR 範囲 | **O11Y CIDR:** `10.1.0.0/22`; **Resource pool CIDR:** `10.10.0.0/16` | Step 6 |
| **Image Sync Region** | イメージ同期用に選択したリージョン ID | `us-west-2` | 詳細は [image synchronization](/tidb-cloud/byoc/byoc-automated-deployment.md#step-1-image-synchronization) を参照してください。 |

## AWS service quotas を確認して引き上げる {#review-and-increase-aws-service-quotas}

AWS service quota の要件は、お客様の環境によって異なります。必要な quota 値は、ワークロードの規模、目標容量、選択した AWS リージョン、可用性モード、想定されるスケーリング範囲などの要因によって決まります。

環境準備の際は、TiDB Cloud Support または TiDB Cloud 担当者と連携して、デプロイに必要な quota 値を算出してください。現在の AWS service quota が算出された要件を下回る場合は、自動リージョン デプロイが始まる前に quota の引き上げを申請してください。

### 確認する quota カテゴリ {#quota-categories-to-review}

対象の各 AWS リージョンで、次の quota カテゴリを確認してください。

- **Amazon EC2 quotas**: デプロイに必要な vCPU ベースのインスタンス使用量およびインスタンスファミリーに関連する quota 値。
- **Amazon EBS quotas**: デプロイに必要なストレージタイプおよびボリューム容量に関連する quota 値。
- **Amazon EKS and scaling-related quotas**: EC2 容量、Auto Scaling Group の上限、EKS managed node group の上限など、EKS クラスターおよびノードのスケーリング容量に影響する quota 値。

### quota 引き上げを申請する方法 {#how-to-request-a-quota-increase}

1. AWS Management Console にログインします。
2. Service Quotas に移動します。
3. 関連するサービスを検索します: Amazon EC2、Amazon EBS、Amazon EKS。
4. 必要な quota を選択します。
5. **Request quota increase** をクリックします。
6. 目標値を入力して申請を送信します。

## What's next {#what-s-next}

AWS 環境の準備を完了し、必要な情報を TiDB Cloud 担当者と共有したら、[TiDB Cloud BYOC IAM Configuration](/tidb-cloud/byoc/byoc-configure-iam-permissions.md) に進み、自動リージョン デプロイに必要な IAM 権限を設定してください。