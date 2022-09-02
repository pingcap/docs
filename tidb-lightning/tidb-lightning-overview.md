---
title: TiDB Lightning Overview
summary: Learn about Lightning and the whole architecture.
---

# TiDB Lightningの概要 {#tidb-lightning-overview}

[TiDB Lightning](https://github.com/pingcap/tidb-lightning)は、大量のデータを TiDB クラスターに高速で完全にインポートするために使用されるツールです。 TiDB Lightningは[ここ](/download-ecosystem-tools.md)からダウンロードできます。

現在、 TiDB Lightningは主に次の 2 つのシナリオで使用できます。

-   **大量**の<strong>新しい</strong>データ<strong>をすばやく</strong>インポートする
-   すべてのバックアップ データを復元する

現在、 TiDB Lightningは以下をサポートしています。

-   [Dumpling](/dumpling-overview.md) 、CSV ファイル、および[Amazon Auroraによって生成された Apache Parquet ファイル](/migrate-aurora-to-tidb.md)によってエクスポートされたファイルのインポート。
-   ローカル ディスクまたは Amazon S3 ストレージからのデータの読み取り。詳細については、 [外部ストレージ](/br/backup-and-restore-storages.md)を参照してください。

## TiDB Lightningアーキテクチャ {#tidb-lightning-architecture}

![Architecture of TiDB Lightning tool set](/media/tidb-lightning-architecture.png)

完全なインポート プロセスは次のとおりです。

1.  インポートする前に、 `tidb-lightning`は TiKV クラスターを「インポート モード」に切り替えます。これにより、書き込み用にクラスターが最適化され、自動圧縮が無効になります。

2.  `tidb-lightning`は、データ ソースからすべてのテーブルのスケルトンを作成します。

3.  各テーブルは複数の連続*バッチ*に分割されるため、巨大なテーブル (200 GB 以上) からのデータを段階的かつ同時にインポートできます。

4.  バッチごとに、 `tidb-lightning`は*エンジン ファイル*を作成して KV ペアを保存します。次に、データ ソースを並列に読み取り、 `tidb-lightning`ルールに従って各行を KV ペアに変換し、これらの KV ペアをローカル ファイルに書き込み、一時的に保存します。

5.  完全なエンジン ファイルが書き込まれると、これらのデータを分割してスケジュールし、ターゲットの`tidb-lightning`クラスターにインポートします。

    エンジン ファイルには、*データ エンジン*と<em>インデックス エンジン</em>の 2 種類があり、それぞれが行データとセカンダリ インデックスの 2 種類の KV ペアに対応しています。通常、行データはデータ ソース内で完全に並べ替えられますが、セカンダリ インデックスは順不同です。このため、データ エンジンはバッチが完了するとすぐにアップロードされますが、インデックス エンジンはテーブル全体のすべてのバッチがエンコードされた後にのみインポートされます。

6.  テーブルに関連付けられたすべてのエンジンがインポートされた後、 `tidb-lightning`はローカル データ ソースとクラスターから計算されたものとの間でチェックサムの比較を実行し、プロセス中にデータの破損がないことを確認します。最適なクエリ計画を準備するために、TiDB にインポートされたすべてのテーブルを`ANALYZE`に指示します。 `AUTO_INCREMENT`の値を調整して、将来の挿入で競合が発生しないようにします。

    テーブルの自動インクリメント ID は、行数の推定*上限*によって計算されます。これは、テーブルのデータ ファイルの合計ファイル サイズに比例します。したがって、最終的な自動インクリメント ID は、多くの場合、実際の行数よりもはるかに大きくなります。 TiDB では auto-increment が[必ずしも順番に割り当てられるわけではありません](/mysql-compatibility.md#auto-increment-id)であるため、これは予期されることです。

7.  最後に、 `tidb-lightning`は TiKV クラスターを「通常モード」に戻すため、クラスターは通常のサービスを再開します。

データ インポートのターゲット クラスターが v3.x 以前のバージョンの場合、データをインポートするには Importer バックエンドを使用する必要があります。このモードでは、 `tidb-lightning`は解析された KV ペアを gRPC 経由で`tikv-importer`に送信し、 `tikv-importer`はデータをインポートします。

TiDB Lightningは、データのインポートに TiDB バックエンドの使用もサポートしています。このモードでは、 `tidb-lightning`はデータを`INSERT`の SQL ステートメントに変換し、それらをターゲット クラスターで直接実行します。詳細は[TiDB Lightningバックエンド](/tidb-lightning/tidb-lightning-backends.md)を参照してください。

## 制限 {#restrictions}

-   TiDB Lightningを TiFlash と一緒に使用する場合:

    テーブルに TiFlash レプリカがあるかどうかに関係なく、 TiDB Lightningを使用してそのテーブルにデータをインポートできます。これにより、 TiDB Lightning手順が遅くなる可能性があることに注意してください。これは、Lightning ホストの NIC 帯域幅、TiFlash ノードの CPU とディスクの負荷、および TiFlash レプリカの数に依存します。

-   TiDB Lightningを TiDB と一緒に使用する場合:

    TiDB Lightningは、v5.4.0 より前の TiDB クラスターへの`charset=GBK`テーブルのインポートをサポートしていません。

-   Apache Parquet ファイルの場合、 TiDB Lightningは現在 Amazon Aurora Parquet ファイルのみを受け入れます。
