---
title: Security
summary: TiDB Cloudのセキュリティ概念について学びましょう。
---

# Security {#security}

TiDB Cloudは、データの保護、アクセス制御の徹底、最新のコンプライアンス基準への準拠を目的とした、堅牢かつ柔軟なセキュリティフレームワークを提供します。このフレームワークは、高度なセキュリティ機能と運用効率を組み合わせ、大規模な組織のニーズに対応します。

**主要構成要素**

-   **IDおよびアクセス管理（IAM ）** ： TiDB Cloudコンソール環境とデータベース環境の両方において、セキュリティかつ柔軟な認証と権限管理を実現します。

-   **ネットワークアクセス制御**：プライベートエンドポイント、VPCピアリング、TLS暗号化、IPアクセスリストなど、設定可能な接続オプション。

-   **データアクセス制御**：保存されているデータを保護するための、顧客管理暗号化キー（CMEK）などの高度な暗号化機能。

-   **監査ログ**：コンソール操作とデータベース操作の両方について包括的なアクティビティ追跡を行い、説明責任と透明性を確保します。

TiDB Cloudはこれらの機能を統合することで、組織が機密データを保護し、アクセス制御を効率化し、セキュリティ運用を最適化できるよう支援します。

## IDおよびアクセス管理（IAM） {#identity-and-access-management-iam}

TiDB Cloudは、アイデンティティおよびアクセス管理（IAM）を採用し、コンソール環境とデータベース環境の両方でユーザーのIDと権限を安全かつ効率的に管理します。IAMの機能は、認証オプション、ロールベースのアクセス制御、階層的なリソース構造を組み合わせることで、組織のセキュリティとコンプライアンスのニーズを満たすように設計されています。

### TiDB Cloudユーザーアカウント {#tidb-cloud-user-accounts}

TiDB Cloudのユーザーアカウントは、ID管理とリソースへのアクセス管理の基盤となります。各アカウントはプラットフォーム内の個人または組織を表し、組織のニーズに合わせて複数の認証方法をサポートします。

-   **デフォルトのユーザー名とパスワード**

    -   ユーザーはメールアドレスとパスワードを使ってアカウントを作成します。

    -   外部のIDプロバイダーを利用していない小規模チームや個人に適しています。

-   **標準SSO認証**

    -   ユーザーはGitHub、Google、またはMicrosoftのアカウント経由でログインします。

    -   すべての組織でデフォルトで有効になっています。

    -   **推奨される使用方法**：小規模チームや、厳格なコンプライアンス要件がないチームでの使用。

    -   詳細については、 [標準SSO認証](/tidb-cloud/tidb-cloud-sso-authentication.md)を参照してください。

-   **組織のSSO認証**

    -   OIDCまたはSAMLプロトコルを使用して、企業IDプロバイダー（IdP）と連携します。

    -   多要素認証の強制、パスワード有効期限ポリシー、ドメイン制限などの機能を有効にします。

    -   **ベストプラクティス**：高度なセキュリティおよびコンプライアンス要件を持つ大規模組織に最適です。

    -   詳細については、 [組織のSSO認証](/tidb-cloud/tidb-cloud-org-sso-authentication.md)を参照してください。

### データベースアクセス制御 {#database-access-control}

TiDB Cloudは、ユーザーベースおよびロールベースの権限設定により、きめ細かなデータベースアクセス制御を提供します。これらの仕組みにより、管理者は組織のセキュリティポリシーを遵守しながら、データオブジェクトとスキーマへのアクセスを安全に管理できます。

-   **ベストプラクティス：**

    -   最小権限の原則を実践するため、ユーザーにはそれぞれの役割に必要な権限のみを付与してください。

    -   組織の要件の変化に合わせて、ユーザーアクセス権限を定期的に監査および更新する。

### データベースユーザーアカウント {#database-user-accounts}

データベースのユーザーアカウントは`mysql.user`システムテーブルに格納され、ユーザー名とクライアントホストによって一意に識別されます。

データベースの初期化中に、TiDB は自動的にデフォルト アカウント`'root'@'%'`を作成します。

詳細については、 [TiDBユーザーアカウント管理](https://docs.pingcap.com/tidb/stable/user-account-management#user-names-and-passwords)参照してください。

### SQLプロキシアカウント {#sql-proxy-accounts}

SQLプロキシアカウントは、 TiDB Cloudによって自動的に生成される特殊用途アカウントです。これらのアカウントの主な特徴は以下のとおりです。

-   **TiDB Cloudユーザーアカウントにリンクされています：**各SQLプロキシアカウントは、特定のTiDB Cloudユーザーに対応しています。

-   **役割にマッピングされています:** SQL プロキシ アカウントには`role_admin`役割が付与されます。

-   **トークンベース：** SQLプロキシアカウントは、パスワードの代わりに安全なJWTトークンを使用するため、 TiDB CloudデータサービスまたはSQLエディターを介したシームレスで制限されたアクセスが保証されます。

### TiDBの権限と役割 {#tidb-privileges-and-roles}

TiDBの権限管理システムはMySQL 5.7をベースとしており、データベースオブジェクトへのきめ細かなアクセス制御を可能にします。同時に、TiDBはMySQL 8.0のRBAC（ロールベースアクセス制御）と動的権限メカニズムも導入しています。これにより、データベース権限をきめ細かく、かつ便利に管理できます。

**静的権限**

-   テーブル、ビュー、インデックス、ユーザー、その他のオブジェクトを含むデータベースオブジェクトに基づいた、きめ細かなアクセス制御をサポートします。

-   *例：特定のテーブルに対するSELECT権限をユーザーに付与する。*

**動的な権限**

-   データベース管理権限の適切な分割をサポートし、システム管理権限のきめ細かな制御を実現します。

-   例: より広範な管理権限を持たないデータベースバックアップを管理するアカウントに`BACKUP_ADMIN`を割り当てます。

**SQLロール（RBAC）**

-   権限を役割ごとにグループ化し、ユーザーに割り当てられるようにすることで、権限管理の効率化と動的な更新が可能になります。

-   例：アナリストに読み書き権限を割り当てることで、ユーザーアクセス制御を簡素化する。

このシステムは、組織の方針に準拠しながら、ユーザーアクセス管理における柔軟性と正確性を確保します。

### 組織とプロジェクト {#organization-and-projects}

TiDB Cloudは、組織、プロジェクト、リソースという階層構造でユーザーとリソースを管理します。

**組織**

-   ユーザー、役割、プロジェクト、リソース、および請求を管理するための最上位エンティティ。

-   組織の所有者は、プロジェクトの作成や役割の割り当てなど、すべての権限を持っています。

**プロジェクト**

-   TiDB Cloudのリソースをグループ化および管理するためのコンテナ。

-   TiDB Cloudには、3種類のプロジェクトがあります。

    -   **TiDB Dedicatedプロジェクト**： TiDB Cloud Dedicatedクラスタ専用のプロジェクトタイプです。Dedicatedプロジェクトは、ネットワーク、メンテナンス、アラート購読、統合、暗号化関連のアクセスなど、プロジェクトスコープの設定を管理します。
    -   **TiDB Xプロジェクト**：TiDB Xインスタンス（ TiDB Cloud Starter、 Essential、Premiumインスタンスを含む）の論理コンテナです。TiDB Xプロジェクトは、リソースのグループ化やプロジェクトレベルのRBACの適用に使用されますが、専用環境専用のインフラストラクチャ設定は保持しません。
    -   **TiDB X仮想プロジェクト**：どのTiDB Xプロジェクトにもグループ化されていないTiDB Xインスタンス用の仮想プロジェクトです。このプロジェクトタイプはAPI互換性のためだけに使用され、管理機能は提供されません。

**リソース**

-   TiDB Cloudリソースは、TiDB X インスタンス ( [TiDB Xアーキテクチャ](/tidb-cloud/tidb-x-architecture.md)上に構築されたサービス指向のTiDB Cloudオファリング) またはTiDB Cloud Dedicatedクラスタのいずれかになります。

### 例となる構造 {#example-structure}

    - Your organization
        - TiDB X instances out of any project
            - TiDB Cloud Starter instance 1
            - TiDB Cloud Essential instance 1
        - TiDB X project 1
            - TiDB Cloud Starter instance 2
            - TiDB Cloud Starter instance 3
            - TiDB Cloud Essential instance 2
        - TiDB Dedicated project 1
            - TiDB Cloud Dedicated cluster 1
            - TiDB Cloud Dedicated cluster 2

### 主な機能 {#key-features}

-   **詳細な権限設定**：
    -   組織、プロジェクト、インスタンスの各レベルで特定の役割を割り当てることで、正確なアクセス制御を実現します。

    -   TiDB Xインスタンスにはプロジェクトロールまたはインスタンスロールのいずれかを通じてアクセスできますが、 TiDB Cloud Dedicatedクラスタはプロジェクトレベルのアクセスによって管理されます。

-   **柔軟なプロジェクトモデル**：
    -   TiDB Xプロジェクトはオプションなので、TiDB Xインスタンスはプロジェクトにグループ化することも、組織レベルで管理することもできます。

    -   TiDB Dedicatedプロジェクトは必須であるため、各DedicatedクラスターはDedicatedプロジェクトに属していなければなりません。

-   **請求管理**：
    -   請求は組織レベルで統合され、各プロジェクトおよびリソースごとに詳細な内訳が提供されます。

### IDおよびアクセス管理（IAM）の役割 {#identity-and-access-management-iam-roles}

TiDB Cloudは、組織、プロジェクト、インスタンス全体にわたる権限管理のためのロールベースのアクセス制御を提供します。

-   **<a href="/tidb-cloud/manage-user-access.md#organization-roles">組織レベルの役割</a>**：請求処理やプロジェクト作成など、組織全体を管理するための権限を付与します。

-   **<a href="/tidb-cloud/manage-user-access.md#project-roles">プロジェクトレベルの役割</a>**：プロジェクトスコープのリソースや構成など、特定のプロジェクトを管理するための権限を割り当てます。

-   **<a href="/tidb-cloud/manage-user-access.md#instance-roles">インスタンスレベルのロール</a>**：特定のTiDB Xインスタンスに対して、きめ細かなアクセス権限を付与します。

## ネットワークアクセス制御 {#network-access-control}

TiDB Cloudは、堅牢なネットワークアクセス制御により、安全な接続とデータ伝送を保証します。主な機能は以下のとおりです。

### プライベートエンドポイント {#private-endpoints}

<CustomContent language="en,zh">

-   仮想プライベートクラウド（VPC）内のSQLクライアントとTiDB Cloud Dedicatedクラスター間の安全な接続を可能にします。

-   [AWSプライベートリンク](/tidb-cloud/set-up-private-endpoint-connections.md)、 [Azure プライベートリンク](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md)リンク、 [Google Cloud Private Service Connect](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md) 、 [Alibaba Cloudプライベートエンドポイント](/tidb-cloud/set-up-private-endpoint-connections-on-alibaba-cloud.md)でサポートされています。

</CustomContent>

<CustomContent language="ja">

-   仮想プライベートクラウド（VPC）内のSQLクライアントとTiDB Cloud Dedicatedクラスター間の安全な接続を可能にします。

-   [AWSプライベートリンク](/tidb-cloud/set-up-private-endpoint-connections.md)、 [Azure プライベートリンク](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md)リンク、 [Google Cloud Private Service Connect](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)でサポートされています。

</CustomContent>

**ベストプラクティス：**本番ではプライベートエンドポイントを使用して外部への露出を最小限に抑え、設定を定期的に見直してください。

### TLS（トランスポート層Security） {#tls-transport-layer-security}

-   クライアントとサーバー間の通信を暗号化し、データ送信の安全性を確保します。

-   セットアップガイド：

    -   [TiDB Cloud StarterまたはEssentialへのTLS接続](/tidb-cloud/secure-connections-to-serverless-clusters.md)
    -   [TiDB Cloud DedicatedへのTLS接続](/tidb-cloud/tidb-cloud-tls-connect-to-dedicated.md)

**ベストプラクティス：** TLS証明書が最新であることを確認し、定期的に更新してください。

### VPCピアリング {#vpc-peering}

-   仮想プライベートクラウド間でプライベート接続を確立し、安全でシームレスな通信を実現します。

-   詳細については、 [VPCピアリング経由でTiDB Cloud Dedicatedに接続します](/tidb-cloud/set-up-vpc-peering-connections.md)参照してください。

**推奨される使用方法：**重要なワークロードには、インターネットへの公開を避け、パフォーマンスを監視するために使用してください。

### IPアクセスリスト {#ip-access-list}

-   ファイアウォールとして機能し、クラスタへのアクセスを信頼できるIPアドレスに制限します。

-   詳細については、 [IPアクセスリストを設定する](/tidb-cloud/configure-ip-access-list.md)参照してください。

**ベストプラクティス：**セキュリティを維持するために、アクセスリストを定期的に監査し、更新してください。

## データアクセス制御 {#data-access-control}

TiDB Cloudは、高度な暗号化機能で静的データを保護し、セキュリティと業界規制への準拠を保証します。

<CustomContent plan="starter,essential,dedicated">

**顧客管理暗号化キー（CMEK）**

-   TiDB Cloud Dedicatedクラスターの暗号化に関して、組織に完全な制御権限を提供します。

-   有効にすると、静的データとバックアップをCMEKキーで暗号化します。

-   CMEKを使用しないTiDB Cloud Dedicatedクラスタの場合、 TiDB Cloudはエスクローキーを使用します。TiDB TiDB Cloud StarterおよびTiDB Cloud Essentialインスタンスは、エスクローキーのみに依存します。

**ベストプラクティス：**

-   セキュリティを強化し、コンプライアンス基準を満たすため、CMEKキーは定期的に交換してください。

-   バックアップはCMEKキーを使用して一貫して暗号化することで、セキュリティをさらに強化できます。

-   HIPAAやGDPRなど、厳格なコンプライアンスが求められる業界では、CMEKを活用してください。

詳細については、 [AWS 上で顧客管理暗号化キーを使用した保存時の暗号化](/tidb-cloud/tidb-cloud-encrypt-cmek-aws.md)および[Azure 上で顧客管理暗号化キーを使用した保存時の暗号化](/tidb-cloud/tidb-cloud-encrypt-cmek-azure.md)参照してください。

</CustomContent>

<CustomContent plan="premium">

**二重層データ暗号化**

-   ストレージ層の暗号化（クラウドプロバイダーによって提供される）とデータベースレイヤーの暗号化を組み合わせることで、AWS上でホストされているTiDB Cloud Premiumインスタンスの保存データに対する保護をさらに強化します。

-   有効にすると、TiKVに保存されているデータ、変更フィードデータ、およびバックアップデータを暗号化します。

-   セキュリティ要件や運用要件に応じて、顧客管理型暗号化キー（CMEK）とサービス管理型暗号化キーのどちらかを選択できます。

詳細については、 [二重層データ暗号化](/tidb-cloud/premium/dual-layer-data-encryption-premium.md)参照してください。

</CustomContent>

## 監査ログ {#audit-logging}

TiDB Cloudは、ユーザーアクティビティとデータベース操作を監視するための包括的な監査ログ機能を提供し、セキュリティ、説明責任、およびコンプライアンスを確保します。

### コンソール監査ログ {#console-audit-logging}

TiDB Cloudコンソール上で行われた主要な操作（ユーザーの招待やデータのインポートなど）を追跡します。

**ベストプラクティス：**

-   ログをSIEMツールと統合することで、リアルタイムの監視とアラートを実現します。

-   法令遵守要件を満たすようにデータ保持ポリシーを設定する。

### 国立データベース監査ログ {#database-audit-logging}

実行されたSQL文やユーザーアクセスなど、データベース操作の詳細を記録します。

**ベストプラクティス：**

-   不審な活動や不正アクセスがないか、定期的にログを確認してください。

-   ログは、コンプライアンス報告およびフォレンジック分析に活用してください。

詳細については、 [コンソール監査ログ](/tidb-cloud/tidb-cloud-console-auditing.md)[データベース監査ログ](/tidb-cloud/tidb-cloud-auditing.md)を参照してください。
