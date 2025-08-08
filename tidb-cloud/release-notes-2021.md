---
title: TiDB Cloud Release Notes in 2021
summary: 2021 年のTiDB Cloudのリリース ノートについて説明します。
---

# 2021年のTiDB Cloudリリースノート {#tidb-cloud-release-notes-in-2021}

このページには、2021 年の[TiDB Cloud](https://www.pingcap.com/tidb-cloud/)のリリース ノートが記載されています。

## 2021年12月28日 {#december-28-2021}

新機能:

-   サポート[Amazon S3 または GCS からTiDB Cloudに Apache Parquet ファイルをインポートする](/tidb-cloud/import-parquet-files.md)

バグ修正:

-   TiDB Cloudに 1000 個を超えるファイルをインポートするときに発生するインポート エラーを修正しました
-   TiDB Cloud が、既にデータが存在する既存のテーブルにデータをインポートできる問題を修正しました。

## 2021年11月30日 {#november-30-2021}

一般的な変更:

-   TiDB Cloud をDeveloper Tier [TiDB v5.3.0](https://docs.pingcap.com/tidb/stable/release-5.3.0)にアップグレード

新機能:

-   サポート[TiDB クラウド プロジェクトに VPC CIDR を追加する](/tidb-cloud/set-up-vpc-peering-connections.md)

改善点:

-   Developer Tierの監視能力の向上
-   自動バックアップ時間をDeveloper Tierクラスタの作成時間と同じに設定することをサポート

バグ修正:

-   Developer Tierでディスクがいっぱいになると TiKV がクラッシュする問題を修正しました
-   HTMLインジェクションの脆弱性を修正

## 2021年11月8日 {#november-8-2021}

-   Launch [Developer Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 、 TiDB Cloudの 1 年間の無料トライアルが提供されます。

    各Developer Tierクラスターはフル機能の TiDB クラスターであり、次のものが含まれます。

    -   1つのTiDB共有ノード
    -   1 つの TiKV 共有ノード (500 MiB の OLTPstorage付き)
    -   1 つのTiFlash共有ノード (500 MiB の OLAPstorage付き)

    始めましょ[ここ](/tidb-cloud/tidb-cloud-quickstart.md) .

## 2021年10月21日 {#october-21-2021}

-   個人のメールアカウントへのユーザー登録を開放
-   サポート[Amazon S3 または GCS からTiDB Cloudへのインポートまたは移行](/tidb-cloud/import-csv-files.md)

## 2021年10月11日 {#october-11-2021}

-   サポート[TiDB Cloudの請求詳細の表示とエクスポート](/tidb-cloud/tidb-cloud-billing.md#billing-details) （各サービスおよび各プロジェクトの費用を含む）
-   TiDB Cloudの内部機能に関するいくつかの問題を修正

## 2021年9月16日 {#september-16-2021}

-   新規にデプロイされたクラスタのデフォルトのTiDBバージョンを5.2.0から5.2.1にアップグレードしてください。5.2.1の詳細な変更点については、リリースノート[5.2.1](https://docs.pingcap.com/tidb/stable/release-5.2.1)ご覧ください。

## 2021年9月2日 {#september-2-2021}

-   新規にデプロイされたクラスタのデフォルトのTiDBバージョンを5.0.2から5.2.0にアップグレードしてください。TiDB 5.1.0および5.2.0の機能の詳細については、リリースノート[5.2.0](https://docs.pingcap.com/tidb/stable/release-5.2.0)および[5.1.0](https://docs.pingcap.com/tidb/stable/release-5.1.0)ご覧ください。
-   TiDB Cloud内部機能のいくつかの問題を修正しました。

## 2021年8月19日 {#august-19-2021}

-   TiDB Cloud内部機能に関するいくつかの問題を修正しました。このリリースではユーザーの動作に変更はありません。

## 2021年8月5日 {#august-5-2021}

-   組織の役割管理をサポートします。組織の所有者は、必要に応じて組織メンバーの権限を設定できます。
-   組織内の複数プロジェクトの分離をサポートします。組織のオーナーは必要に応じてプロジェクトを作成・管理でき、プロジェクト間のメンバーとインスタンスはネットワークと権限の分離をサポートします。
-   請求書を最適化して、当月と前月の各項目の請求額を表示します。

## 2021年7月22日 {#july-22-2021}

-   クレジットカード追加のユーザーエクスペリエンスを最適化
-   クレジットカードのセキュリティ管理強化
-   バックアップから回復したクラスターが正常に充電できない問題を修正しました

## 2021年7月6日 {#july-6-2021}

-   新規にデプロイされたクラスタのデフォルトのTiDBバージョンを4.0.11から5.0.2にアップグレードしてください。このアップグレードにより、パフォーマンスと機能が大幅に向上します。詳細は[ここ](https://docs.pingcap.com/tidb/stable/release-5.0.0)ご覧ください。

## 2021年6月25日 {#june-25-2021}

-   [TiDB Cloudの価格](https://www.pingcap.com/pricing/)ページ目の**リージョン選択**が機能しない問題を修正

## 2021年6月24日 {#june-24-2021}

-   Auroraスナップショットを TiDB インスタンスにインポートする際の parquet ファイルの解析エラーを修正しました
-   PoCユーザーがクラスタを作成し、クラスタ構成を変更したときに推定時間が更新されない問題を修正しました。

## 2021年6月16日 {#june-16-2021}

-   アカウント登録時に**国/リージョンの**ドロップダウンリストに**中国**が追加されます

## 2021年6月14日 {#june-14-2021}

-   Auroraスナップショットを TiDB インスタンスにインポートする際の EBS マウントエラーを修正しました

## 2021年5月10日 {#may-10-2021}

一般的な

-   TiDB Cloudは現在パブリックプレビュー中です。1 [サインアップ](https://tidbcloud.com/signup)クリックして、以下のいずれかのトライアルオプションを選択してください。

    -   48時間無料トライアル
    -   2週間のPoC無料トライアル
    -   オンデマンドプレビュー

管理コンソール

-   サインアッププロセスにメール認証とロボット対策のreCAPTCHAが追加されました
-   [TiDB Cloudサービス契約](https://pingcap.com/legal/tidb-cloud-services-agreement)と[PingCAPプライバシーポリシー](https://pingcap.com/legal/privacy-policy/)が更新されました
-   コンソールの申請フォームに記入して[概念実証](/tidb-cloud/tidb-cloud-poc.md)申請することができます。
-   UIを介してサンプルデータをTiDB Cloudクラスタにインポートできます
-   混乱を避けるため、同じ名前のクラスターは許可されません。
-   **サポートメニュー**の**「フィードバックを送信」**をクリックするとフィードバックを送信できます。
-   データのバックアップと復元機能は、PoCおよびオンデマンドのトライアルオプションでご利用いただけます。
-   無料トライアルとPoCにポイント計算ツールとポイント利用ダッシュボードが追加されました。すべてのトライアルオプションでデータstorageと転送の費用は無料です。
