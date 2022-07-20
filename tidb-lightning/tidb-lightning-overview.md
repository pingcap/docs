---
title: TiDB Lightning Overview
summary: Learn about Lightning and the whole architecture.
---

# TiDB Lightningの概要 {#tidb-lightning-overview}

[TiDB Lightning](https://github.com/pingcap/tidb-lightning)は、大量のデータをTiDBクラスタに高速に完全にインポートするために使用されるツールです。 TiDB Lightningは[ここ](/download-ecosystem-tools.md)からダウンロードできます。

現在、 TiDB Lightningは、主に次の2つのシナリオで使用できます。

-   **大量**の<strong>新しい</strong>データ<strong>をすばやく</strong>インポートする
-   すべてのバックアップデータを復元する

現在、 TiDB Lightningは以下をサポートしています。

-   [Dumpling](/dumpling-overview.md) 、CSVファイル、および[AmazonAuroraによって生成されたAuroraファイル](/migrate-aurora-to-tidb.md)でエクスポートされたファイルをインポートします。
-   ローカルディスクまたはAmazonS3ストレージからのデータの読み取り。詳細については、 [外部ストレージ](/br/backup-and-restore-storages.md)を参照してください。

## TiDB Lightningアーキテクチャ {#tidb-lightning-architecture}

![Architecture of TiDB Lightning tool set](/media/tidb-lightning-architecture.png)

完全なインポートプロセスは次のとおりです。

1.  インポートする前に、 `tidb-lightning`はTiKVクラスタを「インポートモード」に切り替えます。これにより、クラスタの書き込みが最適化され、自動圧縮が無効になります。

2.  `tidb-lightning`は、データソースからすべてのテーブルのスケルトンを作成します。

3.  各テーブルは複数の連続し*たバッチ*に分割されるため、巨大なテーブル（200 GB以上）のデータを段階的かつ同時にインポートできます。

4.  バッチごとに、 `tidb-lightning`はKVペアを格納するための*エンジンファイル*を作成します。次に、 `tidb-lightning`はデータソースを並列に読み取り、TiDBルールに従って各行をKVペアに変換し、これらのKVペアを一時ストレージ用のローカルファイルに書き込みます。

5.  完全なエンジンファイルが書き込まれると、 `tidb-lightning`はこれらのデータを分割してスケジュールし、ターゲットTiKVクラスタにインポートします。

    エンジンファイルには、*データエンジン*と<em>インデックスエンジン</em>の2種類があり、それぞれが行データとセカンダリインデックスの2種類のKVペアに対応しています。通常、行データはデータソースで完全に並べ替えられますが、セカンダリインデックスは順序が狂っています。このため、データエンジンはバッチが完了するとすぐにアップロードされますが、インデックスエンジンは、テーブル全体のすべてのバッチがエンコードされた後にのみインポートされます。

6.  テーブルに関連付けられているすべてのエンジンがインポートされた後、 `tidb-lightning`は、ローカルデータソースとクラスタから計算されたエンジンとの間でチェックサム比較を実行し、プロセスでデータの破損がないことを確認します。最適なクエリプランニングの準備をするために、インポートされたすべてのテーブルをTiDBに`ANALYZE`指示します。将来の挿入で競合が発生しないように、 `AUTO_INCREMENT`の値を調整します。

    テーブルの自動インクリメントIDは、行数の推定*上限*によって計算されます。これは、テーブルのデータファイルの合計ファイルサイズに比例します。したがって、最終的な自動インクリメントIDは、実際の行数よりもはるかに大きいことがよくあります。 TiDBでは自動インクリメントが[必ずしも順番に割り当てられるとは限りません](/mysql-compatibility.md#auto-increment-id)であるため、これは予想されます。

7.  最後に、 `tidb-lightning`はTiKVクラスタを「通常モード」に戻すため、クラスタは通常のサービスを再開します。

データインポートのターゲットクラスタがv3.x以前のバージョンの場合は、インポーターバックエンドを使用してデータをインポートする必要があります。このモードでは、 `tidb-lightning`は解析されたKVペアをgRPC経由で`tikv-importer`に送信し、 `tikv-importer`はデータをインポートします。

TiDB Lightningは、データのインポートにTiDBバックエンドを使用することもサポートしています。このモードでは、 `tidb-lightning`はデータを`INSERT`のSQLステートメントに変換し、それらをターゲットクラスタで直接実行します。詳細については、 [TiDB Lightningエンド](/tidb-lightning/tidb-lightning-backends.md)を参照してください。

## 制限 {#restrictions}

-   TiDB LightningをTiFlashと一緒に使用する場合：

    テーブルにTiFlashレプリカがあるかどうかに関係なく、 TiDB Lightningを使用してそのテーブルにデータをインポートできます。これにより、 TiDB Lightningの手順が遅くなる可能性があることに注意してください。これは、LightningホストのNIC帯域幅、TiFlashノードのCPUとディスクの負荷、およびTiFlashレプリカの数によって異なります。

-   TiDB LightningをTiDBと一緒に使用する場合：

    TiDB Lightningは、v5.4.0より前のTiDBクラスターへの`charset=GBK`のテーブルのインポートをサポートしていません。

-   Apache Parquetファイルの場合、 TiDB Lightningは現在Auroraファイルのみを受け入れます。
