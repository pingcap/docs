---
title: Security Overview
summary: TiDB Cloudの包括的なセキュリティフレームワークについて学びましょう。これには、ID管理、ネットワーク分離、データ保護、アクセス制御、監査などが含まれます。
---

# Security概要 {#security-overview}

TiDB Cloudは、データライフサイクルのあらゆる段階を網羅する、包括的かつ柔軟なセキュリティフレームワークを提供します。このプラットフォームは、IDおよびアクセス管理、ネットワークセキュリティと分離、データアクセス制御、データベースアクセス制御、監査ログなど、あらゆる面で完全な保護を実現します。

## IDおよびアクセス管理 {#identity-and-access-management}

TiDB Cloud は[メールアドレスとパスワードでログイン](/tidb-cloud/tidb-cloud-password-authentication.md)、 [標準SSO](/tidb-cloud/tidb-cloud-sso-authentication.md) 、 [組織レベルのSSO](/tidb-cloud/tidb-cloud-org-sso-authentication.md)の複数の認証方法をサポートしています。

TiDB Cloudは階層化された役割と権限管理を提供し、多要素認証（MFA）を有効にすることでアカウントのセキュリティを強化できます。柔軟な[IDとアクセス制御](/tidb-cloud/manage-user-access.md)プロジェクトとリソースへのアクセスをきめ細かな権限で管理でき、最小権限の原則を維持できます。

## ネットワークのセキュリティと分離 {#network-security-and-isolation}

TiDB Cloudは、ネットワークの分離とアクセス制御のために、プライベートエンドポイント、VPCピアリング、およびIPアクセスリストを提供します。

TLSを使用してすべての通信を暗号化することで、転送中のデータの機密性と完全性を確保できます。ネットワークアクセス制御により、承認されたソースのみがクラスターまたはインスタンスのリソースにアクセスできるため、全体的なセキュリティが強化されます。

## データアクセス制御 {#data-access-control}

<CustomContent plan="starter,essential,dedicated">

顧客管理暗号化キー（CMEK）が有効になっているTiDB Cloud Dedicatedクラスタの場合、 TiDB Cloudは保存データとバックアップの両方に対して暗号化を提供します。

堅牢な鍵管理メカニズムと組み合わせることで、暗号化鍵のライフサイクルと使用状況を制御でき、データセキュリティとコンプライアンスをさらに強化できます。

詳細については、 [AWS 上で顧客管理暗号化キーを使用した保存時の暗号化](/tidb-cloud/tidb-cloud-encrypt-cmek-aws.md)および[Azure 上で顧客管理暗号化キーを使用した保存時の暗号化](/tidb-cloud/tidb-cloud-encrypt-cmek-azure.md)参照してください。

</CustomContent>

<CustomContent plan="premium">

AWS 上でホストされているTiDB Cloud Premium インスタンスでは、デュアルレイヤーデータ暗号化を有効にすることで、デフォルトのストレージレイヤー暗号化に加えてデータベースレイヤー暗号化を追加できます。デュアルレイヤーデータ暗号化を有効にすると、 TiDB Cloud はTiKV に保存されたデータ、変更フィードデータ、およびバックアップデータを暗号化し、顧客管理暗号化キー (CMEK) またはサービス管理暗号化キーのいずれかを選択できます。

詳細については、 [二重層データ暗号化](/tidb-cloud/premium/dual-layer-data-encryption-premium.md)参照してください。

</CustomContent>

## データベースアクセス制御 {#database-access-control}

TiDB Cloudは、静的権限と動的権限を組み合わせた、ユーザーおよびロールベースのアクセス制御メカニズムを提供します。ユーザーにロールを割り当てることで、権限をよりきめ細かく管理および配布できます。

[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの場合、 [ルートアカウントのパスワードを設定および管理する](/tidb-cloud/configure-security-settings.md)、 [IPアクセスリスト](/tidb-cloud/configure-ip-access-list.md)を通じてアクセスを制限して、機密性の高いアカウントを保護できます。

## 監査ログ {#audit-logging}

TiDB Cloudは、コンソール操作とデータベース操作の両方について監査ログを提供し、アクティビティ追跡、コンプライアンス監視、およびセキュリティインシデント調査をサポートします。

監査ログには、操作内容、操作時間、および情報源が記録され、企業セキュリティ管理のための信頼できる証拠となります。
