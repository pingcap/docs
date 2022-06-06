---
title: TiDB Lightning Glossary
summary: List of special terms used in TiDB Lightning.
---

# TiDBLightning用語集 {#tidb-lightning-glossary}

このページでは、TiDB Lightningのログ、監視、構成、およびドキュメントで使用される特別な用語について説明します。

<!-- A -->

## A {#a}

### 分析する {#analyze}

[`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)ステートメントを実行しているTiDBテーブルの[統計学](/statistics.md)情報を再構築する操作。

TiDB LightningはTiDBを経由せずにデータをインポートするため、統計情報は自動的に更新されません。したがって、TiDB Lightningは、インポート後にすべてのテーブルを明示的に分析します。この手順は、 `post-restore.analyze`構成を`false`に設定することで省略できます。

### <code>AUTO_INCREMENT_ID</code> {#code-auto-increment-id-code}

すべてのテーブルには、自動インクリメント列のデフォルト値を提供する`AUTO_INCREMENT_ID`のカウンターが関連付けられています。 TiDBでは、このカウンターは行IDを割り当てるために追加で使用されます。

TiDB LightningはTiDBを経由せずにデータをインポートするため、 `AUTO_INCREMENT_ID`カウンターは自動的に更新されません。したがって、TiDBLightningは`AUTO_INCREMENT_ID`を有効な値に明示的に変更します。テーブルに`AUTO_INCREMENT`の列がない場合でも、このステップは常に実行されます。

<!-- B -->

## B {#b}

### バックエンド {#back-end}

バックエンドは、TiDBLightningが解析結果を送信する宛先です。 「バックエンド」とも呼ばれます。

詳細については、 [TiDBLightningバックエンド](/tidb-lightning/tidb-lightning-backends.md)を参照してください。

<!-- C -->

## C {#c}

### チェックポイント {#checkpoint}

TiDB Lightningは、インポート中に進行状況をローカルファイルまたはリモートデータベースに継続的に保存します。これにより、プロセス中にクラッシュした場合に、中間状態から再開できます。詳細については、 [チェックポイント](/tidb-lightning/tidb-lightning-checkpoints.md)セクションを参照してください。

### チェックサム {#checksum}

TiDB Lightningでは、テーブルのチェックサムは、そのテーブルの各KVペアの内容から計算された3つの数値のセットです。これらの番号はそれぞれ次のとおりです。

-   KVペアの数、
-   すべてのKVペアの全長、および
-   各ペアに[CRC-64-ECMA](https://en.wikipedia.org/wiki/Cyclic_redundancy_check)の値のビット単位のXOR。

すべてのテーブルの[ローカル](/tidb-lightning/tidb-lightning-glossary.md#local-checksum)と[リモートチェックサム](/tidb-lightning/tidb-lightning-glossary.md#remote-checksum)を比較することによる[インポートされたデータを検証します](/tidb-lightning/tidb-lightning-faq.md#how-to-ensure-the-integrity-of-the-imported-data) 。いずれかのペアが一致しない場合、プログラムは停止します。 `post-restore.checksum`構成を`false`に設定すると、このチェックをスキップできます。

チェックサムの不一致を適切に処理する方法については、 [よくある質問](/tidb-lightning/tidb-lightning-faq.md#checksum-failed-checksum-mismatched-remote-vs-local)も参照してください。

### かたまり {#chunk}

ソースデータの連続範囲。通常、データソース内の単一のファイルに相当します。

ファイルが大きすぎる場合、TiDBLightningはファイルを複数のチャンクに分割する場合があります。

### 圧縮 {#compaction}

複数の小さなSSTファイルを1つの大きなSSTファイルにマージし、削除されたエントリをクリーンアップする操作。 TiKVは、TiDB Lightningのインポート中に、バックグラウンドでデータを自動的に圧縮します。

> **ノート：**
>
> 従来の理由から、テーブルがインポートされるたびに圧縮を明示的にトリガーするようにTiDBLightningを構成することもできます。ただし、これは推奨されておらず、対応する設定はデフォルトで無効になっています。

技術的な詳細については、 [圧縮に関するRocksDBのwikiページ](https://github.com/facebook/rocksdb/wiki/Compaction)を参照してください。

<!-- D -->

## D {#d}

### データエンジン {#data-engine}

実際の行データを並べ替えるための[エンジン](/tidb-lightning/tidb-lightning-glossary.md#engine) 。

テーブルが非常に大きい場合、そのデータは複数のデータエンジンに配置され、タスクのパイプライン化を改善し、TiKVImporterのスペースを節約します。デフォルトでは、100 GBのSQLデータごとに新しいデータエンジンが開かれます。これは、 `mydumper.batch-size`の設定で構成できます。

TiDB Lightningは、複数のデータエンジンを同時に処理します。これは`lightning.table-concurrency`の設定で制御されます。

<!-- E -->

## E {#e}

### エンジン {#engine}

TiKV Importerでは、エンジンはKVペアを並べ替えるためのRocksDBインスタンスです。

TiDB Lightningは、エンジンを介してデータをTiKVImporterに転送します。最初にエンジンを開き、KVペアを（順不同で）送信し、最後にエンジンを閉じます。エンジンは、受信したKVペアを閉じた後にソートします。これらのクローズドエンジンは、取り込みのためにTiKVストアにさらにアップロードできます。

エンジンは、TiKV Importerの`import-dir`を一時ストレージとして使用します。これは、「エンジンファイル」と呼ばれることもあります。

[データエンジン](/tidb-lightning/tidb-lightning-glossary.md#data-engine)および[インデックスエンジン](/tidb-lightning/tidb-lightning-glossary.md#index-engine)も参照してください。

<!-- F -->

## F {#f}

### フィルター {#filter}

インポートまたは除外するテーブルを指定する構成リスト。

詳細については、 [テーブルフィルター](/table-filter.md)を参照してください。

<!-- I -->

## 私 {#i}

### インポートモード {#import-mode}

読み取り速度とスペース使用量が低下する代わりに、書き込み用にTiKVを最適化する構成。

TiDB Lightningは、実行中にインポートモードのオンとオフを自動的に切り替えます。ただし、 [ノーマルモード](/tidb-lightning/tidb-lightning-glossary.md#normal-mode)がインポートモードでスタックした場合は、 `tidb-lightning-ctl`を使用でき[強制的に元に戻す](/tidb-lightning/tidb-lightning-faq.md#why-my-tidb-cluster-is-using-lots-of-cpu-resources-and-running-very-slowly-after-using-tidb-lightning) 。

### インデックスエンジン {#index-engine}

インデックスをソートするための[エンジン](/tidb-lightning/tidb-lightning-glossary.md#engine) 。

インデックスの数に関係なく、すべてのテーブルは1つのインデックスエンジンに関連付けられています。

TiDB Lightningは、複数のインデックスエンジンを同時に処理します。これは`lightning.index-concurrency`の設定で制御されます。すべてのテーブルには1つのインデックスエンジンがあるため、これにより、同時に処理するテーブルの最大数も構成されます。

### 摂取する {#ingest}

[SSTファイル](/tidb-lightning/tidb-lightning-glossary.md#sst-file)のコンテンツ全体をRocksDB（TiKV）ストアに挿入する操作。

取り込みは、KVペアを1つずつ挿入する場合に比べて非常に高速な操作です。この操作は、TiDBLightningのパフォーマンスを決定する要因です。

技術的な詳細については、 [SSTファイルの作成と取り込みに関するRocksDBのwikiページ](https://github.com/facebook/rocksdb/wiki/Creating-and-Ingesting-SST-files)を参照してください。

<!-- K -->

## K {#k}

### KVペア {#kv-pair}

「キーと値のペア」の略語。

### KVエンコーダ {#kv-encoder}

SQLまたはCSV行をKVペアに解析するルーチン。複数のKVエンコーダーが並行して実行され、処理が高速化されます。

<!-- L -->

## L {#l}

### ローカルチェックサム {#local-checksum}

KVペアをTiKVImporterに送信する前にTiDBLightning自体によって計算されたテーブルの[チェックサム](/tidb-lightning/tidb-lightning-glossary.md#checksum) 。

<!-- N -->

## N {#n}

### ノーマルモード {#normal-mode}

[インポートモード](/tidb-lightning/tidb-lightning-glossary.md#import-mode)が無効になっているモード。

<!-- P -->

## P {#p}

### 後処理 {#post-processing}

データソース全体が解析されてTiKVインポーターに送信されてからの期間。 TiDB Lightningは、TiKVImporterがアップロードして[摂取する](/tidb-lightning/tidb-lightning-glossary.md#ingest)を待機してい[SSTファイル](/tidb-lightning/tidb-lightning-glossary.md#sst-file) 。

<!-- R -->

## R {#r}

### リモートチェックサム {#remote-checksum}

インポート後にTiDBによって計算されたテーブルの[チェックサム](/tidb-lightning/tidb-lightning-glossary.md#checksum) 。

<!-- S -->

## S {#s}

### 散乱 {#scattering}

[領域](/glossary.md#regionpeerraft-group)のリーダーとピアをランダムに再割り当てする操作。スキャッタリングにより、インポートされたデータがTiKVストア間で均等に分散されます。これにより、PDへのストレスが軽減されます。

### 分割 {#splitting}

エンジンは通常非常に大きく（約100 GB）、単一の[領域](/glossary.md#regionpeerraft-group)として扱われる場合はTiKVに適していません。 TiKV Importerは、アップロードする前に、エンジンを複数の小さな[SSTファイル](/tidb-lightning/tidb-lightning-glossary.md#sst-file) （TiKV Importerの`import.region-split-size`設定で構成可能）に分割します。

### SSTファイル {#sst-file}

SSTは、「sortedstringtable」の略語です。 SSTファイルは、KVペアのコレクションのRocksDB（したがってTiKV）のネイティブストレージ形式です。

TiKV Importerは、閉じた[エンジン](/tidb-lightning/tidb-lightning-glossary.md#engine)からSSTファイルを生成します。これらのSSTファイルはアップロードされてからTiKVストアに[摂取した](/tidb-lightning/tidb-lightning-glossary.md#ingest)アップロードされます。
