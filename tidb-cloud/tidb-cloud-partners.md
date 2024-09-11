---
title: TiDB Cloud Partner Web Console
summary: 再販業者およびマネージド サービス プロバイダー (MSP) としてTiDB Cloud Partner Web コンソールを使用する方法を学習します。
aliases: ['/tidbcloud/managed-service-provider']
---

# TiDB Cloudパートナー Web コンソール {#tidb-cloud-partner-web-console}

TiDB Cloudパートナー Web コンソールは、SaaS ソリューションに重点を置くパートナー向けに設計されており、PingCAP とパートナー間の強力なパートナーシップを構築および育成し、顧客により良いサービスを提供することを目的としています。

TiDB Cloudパートナーには 2 つの種類があります。

-   再販業者: AWS Marketplace チャネルパートナープライベートオファー (CPPO) を通じてTiDB Cloudを再販します。
-   マネージドサービスプロバイダー（MSP）： TiDB Cloudを再販し、付加価値サービスを提供する

## AWS チャネルパートナープライベートオファー (CPPO) を通じた再販業者 {#reseller-through-aws-channel-partner-private-offer-cppo}

[AWS CPPO](https://aws.amazon.com/marketplace/features/cpprivateoffers)を介したリセラーにより、お客様は AWS Marketplace を通じてリセラーから直接TiDB Cloudを購入できます。これにより、お客様はパートナーのビジネス知識、ローカライズされたサポート、専門知識の恩恵を受けながら、AWS Marketplace に期待される迅速かつシームレスな購入エクスペリエンスを享受できます。

### PingCAPの再販業者になる {#become-a-reseller-of-pingcap}

リセラー プログラムに興味があり、パートナーとして参加したい場合は、登録して[営業担当に問い合わせる](https://www.pingcap.com/partners/become-a-partner/) 。

### 再販業者の日常業務を管理する {#manage-daily-tasks-for-a-reseller}

再販業者には、日常の管理タスクを管理する方法が 2 つあります。

-   [TiDB Cloudパートナー コンソール](https://partner-console.tidbcloud.com)
-   パートナー管理 API。オープン API ドキュメントは、TiDB Cloudパートナー コンソールの**サポート**ページで参照できます。

## マネージド サービス プロバイダー (MSP) {#managed-service-provider-msp}

MSP は、 TiDB Cloudを再販し、 TiDB Cloud組織管理、課金サービス、技術サポートなどを含む付加価値サービスを提供するパートナーです。

マネージド サービス プロバイダーになるメリットは次のとおりです。

-   割引およびインセンティブプログラム
-   エンパワーメントトレーニング
-   認証による認知度の向上
-   共同マーケティングの機会

### PingCAPのMSPになる {#become-an-msp-of-pingcap}

MSP プログラムにご興味があり、パートナーとして参加したい場合は、登録するには、 [営業担当に問い合わせる](https://www.pingcap.com/partners/become-a-partner/)の情報を提供してください。

-   会社名
-   会社の連絡先メールアドレス
-   会社公式サイトURL
-   会社のロゴ (ライト モード用に 1 つの SVG ファイル、ダーク モード用に 1 つの SVG ファイル。256 x 48 ピクセルの横長のロゴが推奨されます)

上記の情報は、顧客専用のサインアップ URL と会社のロゴが入ったページを生成するために使用されます。

ご要望を慎重に検討し、すぐにご連絡させていただきます。

### MSPの日常業務を管理する {#manage-daily-tasks-for-an-msp}

TiDB Cloud MSP パートナーとして、日常の管理タスクを管理するには 2 つの方法があります。

-   [TiDB Cloudパートナー コンソール](https://partner-console.tidbcloud.com)
-   [MSP 管理 API](https://docs.pingcap.com/tidbcloud/api/v1beta1/msp)

TiDB Cloudパートナーとしての登録が完了すると、 TiDB Cloudパートナー コンソールでアカウントをアクティブ化するための電子メール通知が届き、MSP 管理 API の API キーが送信されます。

MSP 管理 API を使用して、次の日常的なタスクを管理できます。

-   特定の月の MSP 月額料金を照会する
-   MSP に適用されるクエリ クレジット
-   MSP に適用される割引を照会する
-   特定の MSP 顧客の月額料金を照会する
-   MSP顧客用の新しいサインアップURLを作成する
-   すべてのMSP顧客を一覧表示する
-   顧客組織IDでMSP顧客情報を取得する
