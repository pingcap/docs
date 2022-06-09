---
title: TiDB Cloud Release Notes in 2021
summary: Learn about the release notes of TiDB Cloud in 2021.
---

# 2021年のTiDB Cloudリリースノート {#tidb-cloud-release-notes-in-2021}

このページには、2021年の[TiDB Cloud](https://en.pingcap.com/tidb-cloud/)のリリースノートがリストされています。

## 2021年12月28日 {#december-28-2021}

新機能：

-   サポート[AmazonS3またはGCSからTiDB CloudへのApacheParquetファイルのインポート](/tidb-cloud/import-parquet-files.md)

バグの修正：

-   1000を超えるファイルをTiDB Cloudにインポートするときに発生するインポートエラーを修正します
-   TiDB Cloudがすでにデータを持っている既存のテーブルにデータをインポートすることを許可する問題を修正します

## 2021年11月30日 {#november-30-2021}

一般的な変更：

-   開発者層向けにTiDB Cloudを[TiDB v5.3.0](https://docs.pingcap.com/tidb/stable/release-5.3.0)にアップグレード

新機能：

-   サポート[TiDBクラウドプロジェクトにVPCCIDRを追加する](/tidb-cloud/set-up-vpc-peering-connections.md)

改善点：

-   開発者層の監視機能を向上させる
-   開発者層クラスタの作成時間と同じ自動バックアップ時間の設定をサポート

バグの修正：

-   開発者層のディスクがいっぱいになることによるTiKVクラッシュの問題を修正します
-   HTMLインジェクションの脆弱性を修正

## 2021年11月8日 {#november-8-2021}

-   Launch [開発者層](/tidb-cloud/select-cluster-tier.md#developer-tier)は、 TiDB Cloudの1年間の無料トライアルを提供します

    各開発者層クラスタはフル機能のTiDBクラスタであり、次のものが付属しています。

    -   1つのTiDB共有ノード
    -   1つのTiKV共有ノード（500 MiBのOLTPストレージを使用）
    -   1つのTiFlash<sup>ベータ</sup>共有ノード（500 MiBのOLAPストレージを使用）

    はじめに[ここ](/tidb-cloud/tidb-cloud-quickstart.md) 。

## 2021年10月21日 {#october-21-2021}

-   個人の電子メールアカウントへのユーザー登録を開く
-   サポート[AmazonS3またはGCSからTiDB Cloudへのインポートまたは移行](/tidb-cloud/migrate-from-amazon-s3-or-gcs.md)

## 2021年10月11日 {#october-11-2021}

-   各サービスおよび各プロジェクトのコストを含むサポート[TiDB Cloudの請求詳細の表示とエクスポート](/tidb-cloud/tidb-cloud-billing.md#billing-details)
-   TiDB Cloudの内部機能のいくつかの問題を修正します

## 2021年9月16日 {#september-16-2021}

-   新しくデプロイされたクラスターのデフォルトのTiDBバージョンを5.2.0から5.2.1にアップグレードします。 5.2.1での詳細な変更については、 [5.2.1](https://docs.pingcap.com/tidb/stable/release-5.2.1)リリースノートを参照してください。

## 2021年9月2日 {#september-2-2021}

-   新しくデプロイされたクラスターのデフォルトのTiDBバージョンを5.0.2から5.2.0にアップグレードします。 TiDB 5.1.0および5.2.0の機能の詳細については、 [5.2.0](https://docs.pingcap.com/tidb/stable/release-5.2.0)および[5.1.0](https://docs.pingcap.com/tidb/stable/release-5.1.0)のリリースノートを参照してください。
-   TiDB Cloudの内部機能のいくつかの問題を修正します。

## 2021年8月19日 {#august-19-2021}

-   TiDB Cloudの内部機能のいくつかの問題を修正します。このリリースでは、ユーザーの動作に変更はありません。

## 2021年8月5日 {#august-5-2021}

-   組織の役割管理をサポートします。組織の所有者は、必要に応じて組織のメンバーの権限を構成できます。
-   組織内の複数のプロジェクトの分離をサポートします。組織の所有者は必要に応じてプロジェクトを作成および管理でき、プロジェクト間のメンバーとインスタンスはネットワークと権限の分離をサポートします。
-   請求書を最適化して、当月と前月の各アイテムの請求額を表示します。

## 2021年7月22日 {#july-22-2021}

-   クレジットカードを追加するユーザーエクスペリエンスを最適化する
-   クレジットカードのセキュリティ管理を強化する
-   バックアップから回復したクラスタが正常に充電できない問題を修正します

## 2021年7月6日 {#july-6-2021}

-   新しくデプロイされたクラスターのデフォルトのTiDBバージョンを4.0.11から5.0.2にアップグレードします。アップグレードにより、パフォーマンスと機能が大幅に向上します。詳細については、 [ここ](https://docs.pingcap.com/tidb/stable/release-5.0.0)を参照してください。

## 2021年6月25日 {#june-25-2021}

-   [TiDB Cloudの価格](https://en.pingcap.com/products/tidbcloud/pricing/)ページで**地域の選択**が機能しない問題を修正

## 2021年6月24日 {#june-24-2021}

-   AuroraスナップショットをTiDBインスタンスにインポートするときの寄木細工のファイルの解析エラーを修正します
-   PoCユーザーがクラスタクラスタを変更したときに推定時間が更新されない問題を修正

## 2021年6月16日 {#june-16-2021}

-   アカウントにサインアップすると、**中国**が[<strong>国/地域</strong>]ドロップダウンリストに追加されます

## 2021年6月14日 {#june-14-2021}

-   AuroraスナップショットをTiDBインスタンスにインポートする際のEBSのマウントエラーを修正しました

## 2021年5月10日 {#may-10-2021}

全般的

-   TiDB Cloudは現在パブリックプレビューになっています。 1して、試用オプションの[サインアップ](https://tidbcloud.com/signup)つを選択できます。

    -   48時間無料トライアル
    -   2週間のPoC無料トライアル
    -   オンデマンドプレビュー

管理コンソール

-   電子メールの確認とロボット対策のreCAPTCHAがサインアッププロセスに追加されました
-   [TiDB Cloudサービス契約](https://pingcap.com/legal/tidb-cloud-services-agreement)と[PingCAPプライバシーポリシー](https://pingcap.com/legal/privacy-policy/)が更新されました
-   コンソールで申し込みフォームに記入することで、 [PoC](/tidb-cloud/tidb-cloud-poc.md)を申し込むことができます
-   UIを介してサンプルデータをTiDB Cloudクラスタにインポートできます
-   同じ名前のクラスターは、混乱を避けるために許可されていません
-   [**サポート**]メニューの[<strong>フィードバック</strong>を送信]をクリックすると、フィードバックを送信できます
-   データのバックアップおよび復元機能は、PoCおよびオンデマンドの試用オプションで利用できます
-   無料トライアルとPoCにポイント計算機とポイント使用ダッシュボードが追加されました。すべてのトライアルオプションで、データの保存と転送のコストが免除されます
