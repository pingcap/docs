---
title: TiDB Lightning Overview
summary: Learn about Lightning and the whole architecture.
---

# TiDB Lightningの概要 {#tidb-lightning-overview}

[<a href="https://github.com/pingcap/tidb/tree/master/br/pkg/lightning">TiDB Lightning</a>](https://github.com/pingcap/tidb/tree/master/br/pkg/lightning) TB スケールのデータを TiDB クラスターにインポートするために使用されるツールです。これは、TiDB クラスターへの初期データのインポートによく使用されます。

TiDB Lightning は次のファイル形式をサポートしています。

-   [<a href="/dumpling-overview.md">Dumpling</a>](/dumpling-overview.md)によってエクスポートされたファイル
-   CSVファイル
-   [<a href="/migrate-aurora-to-tidb.md">Amazon Auroraによって生成された Apache Parquet ファイル</a>](/migrate-aurora-to-tidb.md)

TiDB Lightning は、次のソースからデータを読み取ることができます。

-   地元
-   [<a href="/br/backup-and-restore-storages.md#uri-format">アマゾンS3</a>](/br/backup-and-restore-storages.md#uri-format)
-   [<a href="/br/backup-and-restore-storages.md#uri-format">Googleクラウドストレージ</a>](/br/backup-and-restore-storages.md#uri-format)

## TiDB Lightningアーキテクチャ {#tidb-lightning-architecture}

![Architecture of TiDB Lightning tool set](/media/tidb-lightning-architecture.png)

TiDB Lightning は2 つのインポート モードをサポートしており、 `backend`で構成されます。インポート モードは、データを TiDB にインポートする方法を決定します。

-   [<a href="/tidb-lightning/tidb-lightning-physical-import-mode.md">物理インポートモード</a>](/tidb-lightning/tidb-lightning-physical-import-mode.md) : TiDB Lightning は、まずデータをキーと値のペアにエンコードしてローカルの一時ディレクトリに保存し、次にこれらのキーと値のペアを各 TiKV ノードにアップロードし、最後に TiKV 取り込みインターフェイスを呼び出して TiKV の RocksDB にデータを挿入します。初期インポートを実行する必要がある場合は、インポート速度が高い物理インポート モードを検討してください。物理インポート モードのバックエンドは`local`です。

-   [<a href="/tidb-lightning/tidb-lightning-logical-import-mode.md">論理インポートモード</a>](/tidb-lightning/tidb-lightning-logical-import-mode.md) : TiDB Lightning は、まずデータを SQL ステートメントにエンコードし、次にこれらの SQL ステートメントを直接実行してデータをインポートします。インポートされるクラスターが本番にある場合、またはインポートされるターゲット テーブルに既にデータが含まれている場合は、論理インポート モードを使用します。論理インポート モードのバックエンドは`tidb`です。

| インポートモード                         | 物理インポートモード                                                                                                                                                    | 論理インポートモード         |
| :------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------ | :----------------- |
| バックエンド                           | `local`                                                                                                                                                       | `tidb`             |
| スピード                             | 高速 (100 ～ 500 GiB/時間)                                                                                                                                         | 低 (10 ～ 50 GiB/時間) |
| 資源の消費                            | 高い                                                                                                                                                            | 低い                 |
| ネットワーク帯域幅の消費量                    | 高い                                                                                                                                                            | 低い                 |
| インポート時のACID準拠                    | いいえ                                                                                                                                                           | はい                 |
| ターゲットテーブル                        | 空でなければなりません                                                                                                                                                   | データを含めることができる      |
| TiDB クラスターのバージョン                 | <blockquote>= 4.0.0</blockquote>                                                                                                                              | 全て                 |
| TiDB クラスターがインポート中にサービスを提供できるかどうか | [<a href="/tidb-lightning/tidb-lightning-physical-import-mode.md#limitations">限定サービス</a>](/tidb-lightning/tidb-lightning-physical-import-mode.md#limitations) | はい                 |

<Note>前述のパフォーマンス データは、2 つのモード間のインポート パフォーマンスの違いを比較するために使用されます。実際のインポート速度は、ハードウェア構成、テーブル スキーマ、インデックスの数などのさまざまな要因の影響を受けます。</Note>
