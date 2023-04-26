---
title: TiDB Cloud Release Notes in 2021
summary: Learn about the release notes of TiDB Cloud in 2021.
---

# 2021 年のTiDB Cloudリリース ノート {#tidb-cloud-release-notes-in-2021}

このページでは、2021 年の[TiDB Cloud](https://www.pingcap.com/tidb-cloud/)のリリース ノートを一覧表示します。

## 2021 年 12 月 28 日 {#december-28-2021}

新機能：

-   サポート[Amazon S3 または GCS からTiDB Cloudへの Apache Parquet ファイルのインポート](/tidb-cloud/import-parquet-files.md)

バグの修正：

-   1000 を超えるファイルをTiDB Cloudにインポートするときに発生するインポート エラーを修正します。
-   TiDB Cloud がデータを既に持っている既存のテーブルにデータをインポートできるようにする問題を修正します。

## 2021 年 11 月 30 日 {#november-30-2021}

一般的な変更:

-   TiDB Cloud をDeveloper Tier用に[TiDB v5.3.0](https://docs.pingcap.com/tidb/stable/release-5.3.0)にアップグレードする

新機能：

-   サポート[TiDB クラウド プロジェクトに VPC CIDR を追加する](/tidb-cloud/set-up-vpc-peering-connections.md)

改良点:

-   Developer Tierの監視能力を向上させる
-   Developer Tierクラスターの作成時間と同じ自動バックアップ時間の設定をサポート

バグの修正：

-   Developer Tierでディスクがいっぱいになることによる TiKV クラッシュの問題を修正
-   HTML インジェクションの脆弱性を修正

## 2021 年 11 月 8 日 {#november-8-2021}

-   Launch [Developer Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta) 。TiDB TiDB Cloudの 1 年間の無料トライアルを提供します。

    各Developer Tierクラスターはフル機能の TiDB クラスターであり、以下が付属しています。

    -   1 つの TiDB 共有ノード
    -   1 つの TiKV 共有ノード (500 MiB の OLTPstorageを使用)
    -   1 つのTiFlash共有ノード (500 MiB の OLAPstorageを使用)

    始めましょう[ここ](/tidb-cloud/tidb-cloud-quickstart.md) .

## 2021 年 10 月 21 日 {#october-21-2021}

-   個人の電子メール アカウントへのユーザー登録を開く
-   サポート[Amazon S3 または GCS からTiDB Cloudへのインポートまたは移行](/tidb-cloud/migrate-from-amazon-s3-or-gcs.md)

## 2021 年 10 月 11 日 {#october-11-2021}

-   サポート[TiDB Cloudの請求詳細の表示とエクスポート](/tidb-cloud/tidb-cloud-billing.md#billing-details) 、各サービスおよび各プロジェクトの費用を含む
-   TiDB Cloud内部機能のいくつかの問題を修正

## 2021 年 9 月 16 日 {#september-16-2021}

-   新しくデプロイされたクラスターのデフォルトの TiDB バージョンを 5.2.0 から 5.2.1 にアップグレードします。 5.2.1 での詳細な変更については、 [5.2.1](https://docs.pingcap.com/tidb/stable/release-5.2.1)リリース ノートを参照してください。

## 2021 年 9 月 2 日 {#september-2-2021}

-   新しくデプロイされたクラスターのデフォルトの TiDB バージョンを 5.0.2 から 5.2.0 にアップグレードします。 TiDB 5.1.0 および 5.2.0 の機能の詳細については、 [5.2.0](https://docs.pingcap.com/tidb/stable/release-5.2.0)および[5.1.0](https://docs.pingcap.com/tidb/stable/release-5.1.0)リリース ノートを参照してください。
-   TiDB Cloud内部機能のいくつかの問題を修正します。

## 2021 年 8 月 19 日 {#august-19-2021}

-   TiDB Cloud内部機能のいくつかの問題を修正します。このリリースでは、ユーザーの動作に変更はありません。

## 2021 年 8 月 5 日 {#august-5-2021}

-   組織の役割管理をサポートします。組織の所有者は、必要に応じて組織のメンバーの権限を構成できます。
-   組織内の複数のプロジェクトの分離をサポートします。組織の所有者は必要に応じてプロジェクトを作成および管理でき、プロジェクト間のメンバーとインスタンスはネットワークと権限の分離をサポートします。
-   請求書を最適化して、当月と前月の各アイテムの請求書を表示します。

## 2021年7月22日 {#july-22-2021}

-   クレジット カードを追加する際のユーザー エクスペリエンスを最適化する
-   クレジットカードのセキュリティ管理強化
-   バックアップから復旧したクラスタが正常に課金できない問題を修正

## 2021 年 7 月 6 日 {#july-6-2021}

-   新しくデプロイされたクラスターのデフォルトの TiDB バージョンを 4.0.11 から 5.0.2 にアップグレードします。このアップグレードにより、パフォーマンスと機能が大幅に向上します。詳細は[ここ](https://docs.pingcap.com/tidb/stable/release-5.0.0)を参照してください。

## 2021 年 6 月 25 日 {#june-25-2021}

-   [TiDB Cloudの価格](https://en.pingcap.com/products/tidbcloud/pricing/)ページで**リージョンの選択が**機能しない問題を修正

## 2021 年 6 月 24 日 {#june-24-2021}

-   Auroraスナップショットを TiDB インスタンスにインポートするときの寄木細工のファイルの解析エラーを修正します。
-   PoC ユーザーがクラスターを作成し、クラスター構成を変更するときに、推定時間が更新されない問題を修正します。

## 2021 年 6 月 16 日 {#june-16-2021}

-   アカウントにサインアップすると、**国/リージョンの**ドロップダウン リストに<strong>中国</strong>が追加されます

## 2021 年 6 月 14 日 {#june-14-2021}

-   Auroraスナップショットを TiDB インスタンスにインポートする際のマウント EBS エラーを修正

## 2021 年 5 月 10 日 {#may-10-2021}

全般的

-   TiDB Cloud は現在、パブリック プレビュー段階にあります。 [サインアップ](https://tidbcloud.com/signup)試用オプションのいずれかを選択できます。

    -   48時間無料トライアル
    -   2 週間の PoC 無料トライアル
    -   オンデマンドでプレビュー

管理コンソール

-   メール認証とアンチロボット reCAPTCHA がサインアップ プロセスに追加されました
-   [TiDB Cloudサービス契約](https://pingcap.com/legal/tidb-cloud-services-agreement)と[PingCAP プライバシー ポリシー](https://pingcap.com/legal/privacy-policy/)が更新されました
-   コンソールで申請フォームに記入して[PoC](/tidb-cloud/tidb-cloud-poc.md)に申請できます
-   UI を介してサンプル データをTiDB Cloudクラスターにインポートできます
-   混乱を避けるため、同じ名前のクラスターは使用できません
-   **[サポート]**メニューの<strong>[フィードバックを送信]</strong>をクリックすると、フィードバックを送信できます。
-   データのバックアップと復元機能は、PoC とオンデマンドの試用オプションで利用できます
-   無料トライアルと PoC のポイント計算機とポイント使用ダッシュボードが追加されました。すべての試用オプションで、データのstorageと転送の費用が免除されます
