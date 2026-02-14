---
title: TiDB Cloud Partner Web Console
summary: 再販業者およびマネージド サービス プロバイダー (MSP) としてTiDB Cloud Partner Web コンソールを使用する方法を学習します。
aliases: ['/ja/tidbcloud/managed-service-provider']
---

# TiDB Cloudパートナー Web コンソール {#tidb-cloud-partner-web-console}

TiDB Cloudパートナー Web コンソールは、SaaS ソリューションに重点を置くパートナー向けに設計されており、PingCAP とパートナー間の強力なパートナーシップを構築および育成し、顧客により良いサービスを提供することを目的としています。

TiDB Cloudパートナーには 2 つの種類があります。

-   再販業者: AWS Marketplace チャネルパートナープライベートオファー (CPPO) を通じてTiDB Cloud を再販します
-   マネージド サービス プロバイダー (MSP): TiDB Cloudを再販し、付加価値サービスを提供します

## AWS チャネルパートナープライベートオファー (CPPO) を通じた再販業者 {#reseller-through-aws-channel-partner-private-offer-cppo}

[AWS CPPO](https://aws.amazon.com/marketplace/features/cpprivateoffers)を介したリセラーは、お客様がAWS Marketplaceを通じてリセラーから直接TiDB Cloudを購入できるようにします。これにより、お客様はパートナーのビジネス知識、地域に根ざしたサポート、そして専門知識を活用しながら、AWS Marketplaceならではの迅速かつシームレスな購入体験を享受できます。

### PingCAPの再販業者になる {#become-a-reseller-of-pingcap}

リセラー プログラムに興味があり、パートナーとして参加したい場合は、登録して[営業担当者に問い合わせる](https://www.pingcap.com/partners/become-a-partner/) 。

### 再販業者の日常業務を管理する {#manage-daily-tasks-for-a-reseller}

再販業者には、日常の管理タスクを管理する 2 つの方法があります。

-   [TiDB Cloudパートナーコンソール](https://partner-console.tidbcloud.com)
-   パートナー管理 API。オープン API ドキュメントは、 TiDB Cloudパートナー コンソールの**サポート**ページでご覧いただけます。

## マネージドサービスプロバイダー（MSP） {#managed-service-provider-msp}

MSP は、 TiDB Cloudを再販し、 TiDB Cloud組織管理、課金サービス、技術サポートなどを含む付加価値サービスを提供するパートナーです。

マネージド サービス プロバイダーになるメリットは次のとおりです。

-   割引とインセンティブプログラム
-   エンパワーメントトレーニング
-   認証による可視性の向上
-   共同マーケティングの機会

### PingCAPのMSPになる {#become-an-msp-of-pingcap}

MSPプログラムにご興味があり、パートナーとしてご参加をご希望の場合は、登録[営業担当者に問い合わせる](https://www.pingcap.com/partners/become-a-partner/)にご記入ください。以下の情報をご提供ください。

-   会社名
-   会社の連絡先メールアドレス
-   会社公式サイトURL
-   会社のロゴ（ライトモード用に 1 つの SVG ファイル、ダークモード用に 1 つの SVG ファイル。256 x 48 ピクセルの横長のロゴが推奨されます）

上記の情報は、顧客専用のサインアップ URL と会社ロゴ入りのページを生成するために使用されます。

お客様のご要望を慎重に評価し、すぐにご返答させていただきます。

### MSPの日常業務を管理する {#manage-daily-tasks-for-an-msp}

TiDB Cloud MSP パートナーとして、日常の管理タスクを管理するには 2 つの方法があります。

-   [TiDB Cloudパートナーコンソール](https://partner-console.tidbcloud.com)
-   [MSP 管理 API (非推奨)](https://docs.pingcap.com/tidbcloud/api/v1beta1/msp)

TiDB Cloudパートナーとしての登録が完了すると、 TiDB Cloudパートナー コンソールでアカウントをアクティブ化するための電子メール通知が届き、MSP 管理 API の API キーが送信されます。

MSP 管理 API を使用して、次の日常的なタスクを管理できます。

-   特定の月の MSP 月額料金を照会する
-   MSPに適用されるクエリクレジット
-   MSP に適用されるクエリ割引
-   特定の MSP 顧客の月額料金を照会する
-   MSP顧客用の新しいサインアップURLを作成する
-   すべてのMSP顧客を一覧表示する
-   顧客組織IDでMSP顧客情報を取得する
