---
title: TiDB Cloud Lake の概要
summary: TiDB Cloud Lake は、分析ワークロード向けのクラウドネイティブなデータウェアハウスサービスです。コンピュートとストレージを分離し、ANSI SQL、半構造化データ処理、AI 指向のワークフローをサポートします。
---

# TiDB Cloud Lake の概要

TiDB Cloud Lake は、分析ワークロード向けのクラウドネイティブなデータウェアハウスサービスです。コンピュートとストレージを分離しているため、Warehouse を個別にプロビジョニングし、ワークロードの変化に応じてスケールさせ、オブジェクトストレージにデータをコスト効率よく保存できます。

TiDB Cloud Lake は、ANSI SQL、半構造化データ処理、ベクトル検索、AI 指向のワークフローを 1 つのプラットフォームでサポートします。基盤となるインフラストラクチャを自ら運用することなく、マネージドな分析体験を求めるチーム向けに設計されています。

> **Warning:**
>
> TiDB Cloud Lake は現在 **public preview** 段階です。製品の改善に伴い、利用可能な機能やサービス制限が変更される場合があります。

## {{{ .lake }}} を選ぶ理由 {#why-lake}

{{{ .lake }}} は、分析、ベクトル、検索、地理空間ワークロードを 1 つのクラウドネイティブプラットフォームに統合します。ストレージとコンピュートの分離、ANSI SQL のサポート、マネージドインフラストラクチャにより、チームはマルチモーダルデータをより高い柔軟性、パフォーマンス、コスト効率で扱えます。

| 機能 | 説明 | 詳細 |
|---|---|---|
| **Unified Engine** | 分析、ベクトル、検索、地理空間は、1 つのオプティマイザとランタイムを共有します。 | [TiDB Cloud Lake アーキテクチャ](/tidb-cloud-lake/guides/tidb-cloud-lake-architecture.md) |
| **Unified Data** | 構造化データ、半構造化データ、非構造化データ、ベクトルデータは、同じオブジェクトストレージを共有します。 | [TiDB Cloud Lake アーキテクチャ](/tidb-cloud-lake/guides/tidb-cloud-lake-architecture.md) |
| **Analytics Native** | ANSI SQL、ウィンドウ処理、増分集計、ストリーミング BI を同じプラットフォーム上で実行できます。 | [Worksheets](/tidb-cloud-lake/guides/worksheet.md) |
| **Vector Native** | 埋め込み、ベクトルインデックス、セマンティック検索はすべて SQL で実行できます。 | [ベクトル検索](/tidb-cloud-lake/guides/vector-search-guide.md) |
| **Search Native** | 全文検索と転置インデックスにより、ハイブリッド検索を実現します。 | [Full-Text Index](/tidb-cloud-lake/guides/full-text-index.md) |
| **Geo Native** | 地理空間インデックスと関数により、地図サービスや位置情報サービスを実現します。 | [Geo Analytics](/tidb-cloud-lake/guides/geo-analytics.md) |

## はじめに {#get-started}

1. [**Quick Start**](/tidb-cloud-lake/lake-quick-start.md): アカウントを作成し、最初のワークフローを実行します。
2. [**TiDB Cloud Lake への接続**](/tidb-cloud-lake/guides/connection-overview.md): ワークフローに適したクライアントまたはドライバを選択します。
3. [**アーキテクチャを学ぶ**](/tidb-cloud-lake/guides/tidb-cloud-lake-architecture.md): メタデータ、コンピュート、ストレージの各レイヤーを理解します。
4. [**製品機能を確認する**](/tidb-cloud-lake/guides/vector-search-guide.md): 分析、ベクトル、検索、地理空間の機能から使い始めます。