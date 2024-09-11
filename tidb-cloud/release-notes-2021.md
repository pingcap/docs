---
title: TiDB Cloud Release Notes in 2021
summary: 2021 年のTiDB Cloudのリリース ノートについて説明します。
---

# 2021 年のTiDB Cloudリリース ノート {#tidb-cloud-release-notes-in-2021}

このページには、2021 年の[TiDB Cloud](https://www.pingcap.com/tidb-cloud/)のリリース ノートが記載されています。

## 2021年12月28日 {#december-28-2021}

新機能:

-   サポート[Amazon S3 または GCS から Apache Parquet ファイルをTiDB Cloudにインポートする](/tidb-cloud/import-parquet-files.md)

バグ修正:

-   TiDB Cloudに 1000 を超えるファイルをインポートするときに発生するインポート エラーを修正しました
-   TiDB Cloud が、すでにデータが存在する既存のテーブルにデータをインポートできる問題を修正しました。

## 2021年11月30日 {#november-30-2021}

一般的な変更:

-   TiDB Cloud をDeveloper Tier[TiDB v5.3.0](https://docs.pingcap.com/tidb/stable/release-5.3.0)にアップグレード

新機能:

-   サポート[TiDB クラウド プロジェクトに VPC CIDR を追加する](/tidb-cloud/set-up-vpc-peering-connections.md)

改善点:

-   Developer Tierの監視機能の向上
-   自動バックアップ時間をDeveloper Tierクラスタの作成時間と同じに設定できるようになりました

バグ修正:

-   Developer Tierでディスクがいっぱいになったために発生する TiKV クラッシュの問題を修正
-   HTMLインジェクションの脆弱性を修正

## 2021年11月8日 {#november-8-2021}

-   Launch [Developer Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)では、 TiDB Cloudの1年間の無料トライアルが提供されます。

    各Developer Tierクラスターはフル機能の TiDB クラスターであり、次のものが付属しています。

    -   1つのTiDB共有ノード
    -   1 つの TiKV 共有ノード (500 MiB の OLTPstorage付き)
    -   1 つのTiFlash共有ノード (500 MiB の OLAPstorage付き)

    始めましょう[ここ](/tidb-cloud/tidb-cloud-quickstart.md) .

## 2021年10月21日 {#october-21-2021}

-   個人のメールアカウントへのユーザー登録を開放
-   サポート[Amazon S3 または GCS からTiDB Cloudへのインポートまたは移行](/tidb-cloud/import-csv-files.md)

## 2021年10月11日 {#october-11-2021}

-   サポート[TiDB Cloudの請求詳細の表示とエクスポート](/tidb-cloud/tidb-cloud-billing.md#billing-details) （各サービスおよび各プロジェクトの費用を含む）
-   TiDB Cloudの内部機能に関するいくつかの問題を修正

## 2021年9月16日 {#september-16-2021}

-   新しくデプロイされたクラスターのデフォルトの TiDB バージョンを 5.2.0 から 5.2.1 にアップグレードします。5.2.1 の詳細な変更については、リリース ノート[5.2.1](https://docs.pingcap.com/tidb/stable/release-5.2.1)を参照してください。

## 2021年9月2日 {#september-2-2021}

-   新しくデプロイされたクラスターのデフォルトの TiDB バージョンを 5.0.2 から 5.2.0 にアップグレードします。TiDB 5.1.0 および 5.2.0 の機能の詳細については、リリース ノート[5.2.0](https://docs.pingcap.com/tidb/stable/release-5.2.0)および[5.1.0](https://docs.pingcap.com/tidb/stable/release-5.1.0)を参照してください。
-   TiDB Cloud の内部機能に関するいくつかの問題を修正しました。

## 2021年8月19日 {#august-19-2021}

-   TiDB Cloud の内部機能に関するいくつかの問題を修正しました。このリリースでは、ユーザーの動作に変更はありません。

## 2021年8月5日 {#august-5-2021}

-   組織の役割管理をサポートします。組織の所有者は、必要に応じて組織のメンバーの権限を構成できます。
-   組織内の複数のプロジェクトの分離をサポートします。組織の所有者は必要に応じてプロジェクトを作成および管理でき、プロジェクト間のメンバーとインスタンスはネットワークと権限の分離をサポートします。
-   請求書を最適化して、今月と前月の各項目の請求額を表示します。

## 2021年7月22日 {#july-22-2021}

-   クレジットカード追加のユーザーエクスペリエンスを最適化
-   クレジットカードのセキュリティ管理強化
-   バックアップから回復したクラスターが正常に充電できない問題を修正

## 2021年7月6日 {#july-6-2021}

-   新しくデプロイされたクラスターのデフォルトの TiDB バージョンを 4.0.11 から 5.0.2 にアップグレードします。アップグレードにより、パフォーマンスと機能が大幅に向上します。詳細については[ここ](https://docs.pingcap.com/tidb/stable/release-5.0.0)を参照してください。

## 2021年6月25日 {#june-25-2021}

-   [TiDB Cloudの価格](https://www.pingcap.com/pricing/)ページで**リージョン選択が**機能しない問題を修正

## 2021年6月24日 {#june-24-2021}

-   Auroraスナップショットを TiDB インスタンスにインポートする際の parquet ファイルの解析エラーを修正しました。
-   PoCユーザーがクラスターを作成し、クラスター構成を変更したときに推定時間が更新されない問題を修正しました。

## 2021年6月16日 {#june-16-2021}

-   アカウント登録時に**国/リージョンの**ドロップダウンリストに**中国**が追加されます

## 2021年6月14日 {#june-14-2021}

-   Auroraスナップショットを TiDB インスタンスにインポートする際の EBS マウント エラーを修正

## 2021年5月10日 {#may-10-2021}

一般的な

-   TiDB Cloud は現在パブリック プレビュー中です。1 [サインアップ](https://tidbcloud.com/signup)して、試用オプションの 1 つを選択できます。

    -   48時間無料トライアル
    -   2週間のPoC無料トライアル
    -   オンデマンドプレビュー

管理コンソール

-   サインアッププロセスにメール認証とロボット対策のreCAPTCHAが追加されました
-   [TiDB Cloudサービス契約](https://pingcap.com/legal/tidb-cloud-services-agreement)と[PingCAP プライバシーポリシー](https://pingcap.com/legal/privacy-policy/)更新されました
-   コンソールの申請フォームに記入して[概念実証](/tidb-cloud/tidb-cloud-poc.md)を申請することができます。
-   UIを介してサンプルデータをTiDB Cloudクラスタにインポートできます
-   混乱を避けるため、同じ名前のクラスターは許可されません。
-   **サポートメニュー**の**「フィードバックを送信」**をクリックするとフィードバックを送信できます。
-   データのバックアップと復元機能は、PoCおよびオンデマンドトライアルオプションで利用できます。
-   無料トライアルとPoCにポイント計算機とポイント使用ダッシュボードが追加されました。すべてのトライアルオプションでデータstorageと転送のコストが免除されます。
