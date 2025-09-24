---
title: Security Overview
summary: ID 管理、ネットワーク分離、データ保護、アクセス制御、監査などを含むTiDB Cloudの包括的なセキュリティ フレームワークについて学習します。
---

# Securityの概要 {#security-overview}

TiDB Cloudは、データライフサイクルのあらゆる段階をカバーする包括的かつ柔軟なセキュリティフレームワークを提供します。このプラットフォームは、IDおよびアクセス管理、ネットワークセキュリティと分離、データアクセス制御、データベースアクセス制御、監査ログなど、包括的な保護を提供します。

## アイデンティティとアクセス管理 {#identity-and-access-management}

TiDB Cloud は、 [メールアドレスとパスワードでログイン](/tidb-cloud/tidb-cloud-password-authentication.md) 、 [標準SSO](/tidb-cloud/tidb-cloud-sso-authentication.md) 、 [組織レベルのSSO](/tidb-cloud/tidb-cloud-org-sso-authentication.md)を含む複数の認証方法をサポートしています。

TiDB Cloudは階層化されたロールと権限管理を提供し、多要素認証（MFA）を有効にしてアカウントのセキュリティを強化できます。Flexible [アイデンティティとアクセス制御](/tidb-cloud/manage-user-access.md)では、きめ細かな権限設定でプロジェクトとリソースへのアクセスを管理できるため、最小権限の原則を維持できます。

## ネットワークセキュリティと分離 {#network-security-and-isolation}

TiDB Cloud は、ネットワークの分離とアクセス制御のために、プライベート エンドポイント、VPC ピアリング、IP アクセス リストを提供します。

TLSを使用してすべての通信を暗号化することで、転送中のデータの機密性と整合性を確保できます。ネットワークアクセス制御により、許可されたソースのみがクラスターリソースにアクセスできるようにすることで、全体的なセキュリティを強化します。

## データアクセス制御 {#data-access-control}

顧客管理暗号化キー (CMEK) をサポートするクラスタ タイプの場合、 TiDB Cloud は保存データとバックアップの両方の暗号化を提供します。

強力なキー管理メカニズムと組み合わせることで、暗号化キーのライフサイクルと使用状況を制御でき、データのセキュリティとコンプライアンスをさらに強化できます。

詳細については、 [AWS での顧客管理の暗号化キーを使用した保存時の暗号化](/tidb-cloud/tidb-cloud-encrypt-cmek-aws.md)および[Azure での顧客管理の暗号化キーを使用した保存時の暗号化](/tidb-cloud/tidb-cloud-encrypt-cmek-azure.md)参照してください。

## データベースアクセス制御 {#database-access-control}

TiDB Cloudは、静的権限と動的権限を組み合わせた、ユーザーベースおよびロールベースのアクセス制御メカニズムを提供します。ユーザーにロールを割り当てることで、よりきめ細かな権限管理と配分が可能になります。

[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの場合、 [ルートアカウントのパスワードを設定および管理する](/tidb-cloud/configure-security-settings.md)から[IPアクセスリスト](/tidb-cloud/configure-ip-access-list.md)までアクセスを制限して、機密性の高いアカウントを保護できます。

## 監査ログ {#audit-logging}

TiDB Cloud は、アクティビティの追跡、コンプライアンスの監視、セキュリティ インシデントの調査をサポートするために、コンソールとデータベース操作の両方の監査ログを提供します。

監査ログには、アクション、操作時間、ソースが記録され、企業のセキュリティ管理に信頼できる証拠が提供されます。
