---
title: TiDB Lightning Overview
summary: Lightning とアーキテクチャ全体について学びます。
---

# TiDB Lightning の概要 {#tidb-lightning-overview}

[TiDB Lightning](https://github.com/pingcap/tidb/tree/release-8.1/lightning) 、TB 規模のデータを TiDB クラスターにインポートするために使用されるツールです。TiDB クラスターへの初期データ インポートによく使用されます。

TiDB Lightning は次のファイル形式をサポートしています。

-   [Dumpling](/dumpling-overview.md)によってエクスポートされたファイル
-   CSVファイル
-   [Amazon Auroraによって生成された Apache Parquet ファイル](/migrate-aurora-to-tidb.md)

TiDB Lightning は次のソースからデータを読み取ることができます。

-   地元
-   [アマゾンS3](/external-storage-uri.md#amazon-s3-uri-format)
-   [Google クラウド ストレージ](/external-storage-uri.md#gcs-uri-format)

## TiDB Lightningアーキテクチャ {#tidb-lightning-architecture}

![Architecture of TiDB Lightning tool set](/media/tidb-lightning-architecture.png)

TiDB Lightning は、 `backend`で設定された 2 つのインポート モードをサポートしています。インポート モードによって、データが TiDB にインポートされる方法が決まります。

-   [物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md) : TiDB Lightning は、まずデータをキーと値のペアにエンコードしてローカルの一時ディレクトリに保存し、次にこれらのキーと値のペアを各 TiKV ノードにアップロードし、最後に TiKV 取り込みインターフェイスを呼び出して TiKV の RocksDB にデータを挿入します。初期インポートを実行する必要がある場合は、インポート速度が速い物理インポート モードを検討してください。物理インポート モードのバックエンドは`local`です。

-   [論理インポートモード](/tidb-lightning/tidb-lightning-logical-import-mode.md) : TiDB Lightning は最初にデータを SQL 文にエンコードし、次にこれらの SQL 文を直接実行してデータをインポートします。インポートするクラスターが本番にある場合、またはインポートするターゲット テーブルにすでにデータが含まれている場合は、論理インポート モードを使用します。論理インポート モードのバックエンドは`tidb`です。

| インポートモード                       | 物理インポートモード                                                                   | 論理インポートモード       |
| :----------------------------- | :--------------------------------------------------------------------------- | :--------------- |
| バックエンド                         | `local`                                                                      | `tidb`           |
| スピード                           | 高速 (100~500 GiB/時間)                                                          | 低 (10~50 GiB/時間) |
| 資源消費                           | 高い                                                                           | 低い               |
| ネットワーク帯域幅の消費                   | 高い                                                                           | 低い               |
| インポート時のACID準拠                  | いいえ                                                                          | はい               |
| ターゲットテーブル                      | 空である必要があります                                                                  | データを含むことができる     |
| TiDB クラスタ バージョン                | = 4.0.0                                                                      | 全て               |
| TiDBクラスタがインポート中にサービスを提供できるかどうか | [限定サービス](/tidb-lightning/tidb-lightning-physical-import-mode.md#limitations) | はい               |

<Note>

上記のパフォーマンス データは、2 つのモード間のインポート パフォーマンスの違いを比較するために使用されます。実際のインポート速度は、ハードウェア構成、テーブル スキーマ、インデックスの数など、さまざまな要因によって影響を受けます。

</Note>
