---
title: TiDB Lightning Overview
summary: Lightning とアーキテクチャ全体について学びます。
---

# TiDB Lightning の概要 {#tidb-lightning-overview}

[TiDB Lightning](https://github.com/pingcap/tidb/tree/release-8.5/lightning) 、TB規模のデータをTiDBクラスタにインポートするためのツールです。TiDBクラスタへの初期データインポートによく使用されます。

TiDB Lightning は次のファイル形式をサポートしています。

-   [Dumpling](/dumpling-overview.md)によってエクスポートされたファイル
-   CSVファイル
-   [Amazon Auroraによって生成された Apache Parquet ファイル](/migrate-aurora-to-tidb.md) 、Apache Hive、またはSnowflake

TiDB Lightning は次のソースからデータを読み取ることができます。

-   地元
-   [アマゾンS3](/external-storage-uri.md#amazon-s3-uri-format)
-   [Googleクラウドストレージ](/external-storage-uri.md#gcs-uri-format)

> **注記：**
>
> TiDB Lightningと比較すると、 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)ステートメントは TiDB ノード上で直接実行でき、自動化された分散タスクスケジューリングと[TiDB グローバルソート](/tidb-global-sort.md)サポートし、デプロイメント、リソース利用率、タスク設定の利便性、呼び出しと統合の容易さ、高可用性、スケーラビリティにおいて大幅な改善が見られます。適切なシナリオでは、 TiDB Lightningではなく`IMPORT INTO`使用を検討することをお勧めします。

## TiDB Lightningアーキテクチャ {#tidb-lightning-architecture}

![Architecture of TiDB Lightning tool set](/media/tidb-lightning-architecture.png)

TiDB Lightning は、 `backend`で設定された 2 つのインポート モードをサポートしています。インポート モードによって、TiDB へのデータのインポート方法が決まります。

-   [物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md) : TiDB Lightningは、まずデータをキーと値のペアにエンコードし、ローカルの一時ディレクトリに保存します。次に、これらのキーと値のペアを各TiKVノードにアップロードし、最後にTiKV 取り込みインターフェースを呼び出してTiKVのRocksDBにデータを挿入します。初期インポートを実行する必要がある場合は、インポート速度が速い物理インポートモードを検討してください。物理インポートモードのバックエンドは`local`です。

-   [論理インポートモード](/tidb-lightning/tidb-lightning-logical-import-mode.md) : TiDB Lightning はまずデータをSQL文にエンコードし、その後、これらのSQL文を直接実行してデータをインポートします。インポート対象のクラスターが本番の場合、またはインポート対象のテーブルに既にデータが含まれている場合は、論理インポートモードを使用してください。論理インポートモードのバックエンドは`tidb`です。

| インポートモード                       | 物理インポートモード                                                                   | 論理インポートモード      |
| :----------------------------- | :--------------------------------------------------------------------------- | :-------------- |
| バックエンド                         | `local`                                                                      | `tidb`          |
| スピード                           | 高速（100～500 GiB/時間）                                                           | 低（10～50 GiB/時間） |
| 資源消費                           | 高い                                                                           | 低い              |
| ネットワーク帯域幅の消費                   | 高い                                                                           | 低い              |
| インポート時のACID準拠                  | いいえ                                                                          | はい              |
| ターゲットテーブル                      | 空でなければなりません                                                                  | データを含むことができる    |
| TiDB クラスタ バージョン                | = 4.0.0                                                                      | 全て              |
| TiDBクラスタがインポート中にサービスを提供できるかどうか | [限定サービス](/tidb-lightning/tidb-lightning-physical-import-mode.md#limitations) | はい              |

<Note>

上記のパフォーマンスデータは、2つのモード間のインポートパフォーマンスの違いを比較するために使用されます。実際のインポート速度は、ハードウェア構成、テーブルスキーマ、インデックス数など、さまざまな要因の影響を受けます。

</Note>
