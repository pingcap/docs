---
title: TiDB Cloud Release Notes in 2021
summary: Learn about the release notes of TiDB Cloud in 2021.
---

# 2021 年のTiDB Cloudリリース ノート {#tidb-cloud-release-notes-in-2021}

このページには2021年[TiDB Cloud](https://www.pingcap.com/tidb-cloud/)のリリースノートを記載しています。

## 2021年12月28日 {#december-28-2021}

新機能：

-   サポート[Amazon S3 または GCS からTiDB Cloudへの Apache Parquet ファイルのインポート](/tidb-cloud/import-parquet-files.md)

バグの修正：

-   1000 を超えるファイルをTiDB Cloudにインポートするときに発生するインポート エラーを修正
-   TiDB Cloud で、既にデータがある既存のテーブルにデータをインポートできる問題を修正

## 2021年11月30日 {#november-30-2021}

全体的な変更:

-   Developer TierのTiDB Cloudを[TiDB v5.3.0](https://docs.pingcap.com/tidb/stable/release-5.3.0)にアップグレードする

新機能：

-   サポート[TiDB クラウド プロジェクトに VPC CIDR を追加する](/tidb-cloud/set-up-vpc-peering-connections.md)

改善点:

-   Developer Tierの監視能力を向上させる
-   Developer Tierクラスターの作成時間と同じ自動バックアップ時間の設定のサポート

バグの修正：

-   Developer Tierのディスクフルによる TiKV クラッシュの問題を修正
-   HTMLインジェクションの脆弱性を修正

## 2021年11月8日 {#november-8-2021}

-   Launch [Developer Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless) : TiDB Cloudの 1 年間の無料トライアルを提供します

    各Developer Tierクラスターはフル機能の TiDB クラスターであり、以下が付属しています。

    -   1 つの TiDB 共有ノード
    -   1 つの TiKV 共有ノード (500 MiB の OLTPstorageを搭載)
    -   1 つのTiFlash共有ノード (500 MiB の OLAPstorageを搭載)

    始めましょう[ここ](/tidb-cloud/tidb-cloud-quickstart.md) .

## 2021年10月21日 {#october-21-2021}

-   個人メールアカウントへのユーザー登録を開く
-   サポート[Amazon S3 または GCS からTiDB Cloudへのインポートまたは移行](/tidb-cloud/import-csv-files.md)

## 2021年10月11日 {#october-11-2021}

-   サポート[TiDB Cloudの請求詳細の表示とエクスポート](/tidb-cloud/tidb-cloud-billing.md#billing-details) 、各サービスおよび各プロジェクトの費用を含む
-   TiDB Cloud の内部機能のいくつかの問題を修正

## 2021年9月16日 {#september-16-2021}

-   新しくデプロイされたクラスターのデフォルトの TiDB バージョンを 5.2.0 から 5.2.1 にアップグレードします。 5.2.1 の詳細な変更点については、リリース ノート[5.2.1](https://docs.pingcap.com/tidb/stable/release-5.2.1)を参照してください。

## 2021年9月2日 {#september-2-2021}

-   新しくデプロイされたクラスターのデフォルトの TiDB バージョンを 5.0.2 から 5.2.0 にアップグレードします。 TiDB 5.1.0 および 5.2.0 の機能の詳細については、リリース ノート[5.2.0](https://docs.pingcap.com/tidb/stable/release-5.2.0)および[5.1.0](https://docs.pingcap.com/tidb/stable/release-5.1.0)参照してください。
-   TiDB Cloud の内部機能のいくつかの問題を修正しました。

## 2021年8月19日 {#august-19-2021}

-   TiDB Cloud の内部機能のいくつかの問題を修正しました。このリリースでは、ユーザーの動作に変化はありません。

## 2021年8月5日 {#august-5-2021}

-   組織の役割管理をサポートします。組織の所有者は、必要に応じて組織メンバーの権限を構成できます。
-   組織内の複数のプロジェクトの分離をサポートします。組織の所有者は必要に応じてプロジェクトを作成および管理でき、プロジェクト間のメンバーとインスタンスはネットワークと権限の分離をサポートします。
-   当月と前月の各項目の請求を表示するように請求書を最適化します。

## 2021年7月22日 {#july-22-2021}

-   クレジット カードを追加する際のユーザー エクスペリエンスを最適化する
-   クレジットカードのセキュリティ管理の強化
-   バックアップから復元したクラスターが正常に充電できない問題を修正

## 2021年7月6日 {#july-6-2021}

-   新しくデプロイされたクラスターのデフォルトの TiDB バージョンを 4.0.11 から 5.0.2 にアップグレードします。このアップグレードにより、パフォーマンスと機能が大幅に向上します。詳細については[ここ](https://docs.pingcap.com/tidb/stable/release-5.0.0)を参照してください。

## 2021年6月25日 {#june-25-2021}

-   [TiDB Cloudの料金](https://en.pingcap.com/products/tidbcloud/pricing/)ページで**リージョンの選択が**機能しない問題を修正

## 2021年6月24日 {#june-24-2021}

-   Auroraスナップショットを TiDB インスタンスにインポートする際の寄木細工ファイルの解析エラーを修正しました。
-   PoC ユーザーがクラスターを作成してクラスター構成を変更するときに、推定時間が更新されない問題を修正

## 2021年6月16日 {#june-16-2021}

-   アカウントにサインアップすると、**国/リージョンの**ドロップダウン リストに**中国**が追加されます。

## 2021年6月14日 {#june-14-2021}

-   Auroraスナップショットを TiDB インスタンスにインポートする際の EBS マウント エラーを修正しました

## 2021年5月10日 {#may-10-2021}

一般的な

-   TiDB Cloud は現在パブリック プレビュー段階にあります。 [サインアップ](https://tidbcloud.com/signup)試用オプションのいずれかを選択できます。

    -   48時間の無料トライアル
    -   2 週間の PoC 無料トライアル
    -   オンデマンドでプレビュー

管理コンソール

-   電子メール検証とロボット対策 reCAPTCHA がサインアップ プロセスに追加されました
-   [TiDB Cloudサービス契約](https://pingcap.com/legal/tidb-cloud-services-agreement)と[PingCAP プライバシー ポリシー](https://pingcap.com/legal/privacy-policy/)が更新されました
-   [実証実験](/tidb-cloud/tidb-cloud-poc.md)は、コンソールの申請フォームに記入して申請できます。
-   UI を通じてサンプル データをTiDB Cloudクラスターにインポートできます
-   混乱を避けるため、同じ名前のクラスターは許可されません
-   **[サポート]**メニューの**[フィードバックを送信]**をクリックしてフィードバックを送信できます。
-   データのバックアップおよび復元機能は、PoC およびオンデマンド試用オプションで利用可能です
-   無料トライアルおよび PoC 用に、ポイント計算ツールとポイント使用状況ダッシュボードが追加されました。データのstorageと転送のコストは、すべての試用オプションで免除されます
