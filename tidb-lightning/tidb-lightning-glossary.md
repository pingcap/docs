---
title: TiDB Lightning Glossary
summary: TiDB Lightningで使用される特殊用語のリスト。
---

# TiDB Lightning用語集 {#tidb-lightning-glossary}

このページでは、TiDB Lightning のログ、監視、構成、ドキュメントで使用される特殊な用語について説明します。

TiDB 関連の用語と定義については、 [TiDB用語集](/glossary.md)参照してください。

<!-- A -->

## あ {#a}

### 分析する {#analyze}

[`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)ステートメントを実行している TiDB テーブルの[統計](/statistics.md)情報を再構築する操作。

TiDB LightningはTiDBを経由せずにデータをインポートするため、統計情報は自動的に更新されません。そのため、 TiDB Lightningはインポート後に各テーブルを明示的に分析します。この手順は、 `post-restore.analyze`設定を`false`に設定することで省略できます。

### <code>AUTO_INCREMENT_ID</code> {#code-auto-increment-id-code}

各テーブルには、自動増分列のデフォルト値を提供するためのカウンタ`AUTO_INCREMENT_ID`が関連付けられています。TiDBでは、このカウンタは行IDの割り当てにも使用されます。

TiDB LightningはTiDBを経由せずにデータをインポートするため、 `AUTO_INCREMENT_ID`カウンタは自動的に更新されません。そのため、 TiDB Lightningは`AUTO_INCREMENT_ID`明示的に有効な値に変更します。この手順は、テーブルに`AUTO_INCREMENT`列がない場合でも常に実行されます。

<!-- B -->

## B {#b}

### バックエンド {#back-end}

バックエンドとは、TiDB Lightningが解析結果を送信する宛先です。「backend」とも表記されます。

詳細は[TiDB Lightningアーキテクチャ](/tidb-lightning/tidb-lightning-overview.md)参照。

<!-- C -->

## C {#c}

### チェックポイント {#checkpoint}

TiDB Lightningは、インポート中に進行状況をローカルファイルまたはリモートデータベースに継続的に保存します。これにより、インポート中にクラッシュした場合でも、中間状態から再開できます。詳細はセクション[チェックポイント](/tidb-lightning/tidb-lightning-checkpoints.md)ご覧ください。

### チェックサム {#checksum}

TiDB Lightningでは、テーブルのチェックサムは、そのテーブル内の各KVペアの内容から計算される3つの数値のセットです。これらの数値はそれぞれ以下のとおりです。

-   KVペアの数、
-   すべてのKVペアの合計長さ、および
-   各ペアの[CRC-64-ECMA](https://en.wikipedia.org/wiki/Cyclic_redundancy_check)値のビット単位の XOR です。

TiDB Lightning [インポートされたデータを検証する](/tidb-lightning/tidb-lightning-faq.md#how-to-ensure-the-integrity-of-the-imported-data) 、各テーブルの[地元](/tidb-lightning/tidb-lightning-glossary.md#local-checksum)と[リモートチェックサム](/tidb-lightning/tidb-lightning-glossary.md#remote-checksum)比較することで、このチェックを実行します。いずれのペアも一致しない場合、プログラムは停止します。このチェックは、 `post-restore.checksum`設定を`false`に設定することでスキップできます。

チェックサムの不一致を適切に処理する方法については、 [よくある質問](/tidb-lightning/troubleshoot-tidb-lightning.md#checksum-failed-checksum-mismatched-remote-vs-local)も参照してください。

### Chunk {#chunk}

ソース データの連続した範囲。通常は、データ ソース内の 1 つのファイルに相当します。

ファイルが大きすぎる場合、 TiDB Lightning はファイルを複数のチャンクに分割することがあります。

### 圧縮 {#compaction}

複数の小さなSSTファイルを1つの大きなSSTファイルに結合し、削除されたエントリをクリーンアップする操作です。TiKVは、 TiDB Lightningによるインポート中にバックグラウンドで自動的にデータを圧縮します。

> **注記：**
>
> レガシーシステムへの対応のため、 TiDB Lightning、テーブルのインポートごとに明示的にコンパクションを実行するように設定できます。ただし、これは推奨されず、対応する設定はデフォルトで無効になっています。

技術的な詳細については[RocksDBの圧縮に関するWikiページ](https://github.com/facebook/rocksdb/wiki/Compaction)参照してください。

<!-- D -->

## D {#d}

### データエンジン {#data-engine}

実際の行データをソートする場合は[エンジン](/tidb-lightning/tidb-lightning-glossary.md#engine) 。

テーブルが非常に大きい場合、タスクのパイプライン処理を改善し、TiKVインポーターのメモリを節約するため、そのデータは複数のデータエンジンに分散されます。デフォルトでは、SQLデータ100GBごとに新しいデータエンジンが開かれますが、 `mydumper.batch-size`設定で変更可能です。

TiDB Lightningは複数のデータエンジンを同時に処理します。これは`lightning.table-concurrency`設定で制御されます。

<!-- E -->

## E {#e}

### エンジン {#engine}

TiKV インポーターでは、エンジンは KV ペアをソートするための RocksDB インスタンスです。

TiDB Lightningは、エンジンを介してTiKV Importerにデータを転送します。まずエンジンを開き、KVペアを（順序は問わず）エンジンに送信し、最後にエンジンを閉じます。エンジンは閉じた後、受信したKVペアをソートします。閉じられたエンジンは、TiKVストアにアップロードして取り込みを行うことができます。

エンジンは TiKV インポーター`import-dir`一時storageとして使用します。これは「エンジン ファイル」と呼ばれることもあります。

[データエンジン](/tidb-lightning/tidb-lightning-glossary.md#data-engine)と[インデックスエンジン](/tidb-lightning/tidb-lightning-glossary.md#index-engine)も参照してください。

<!-- F -->

## F {#f}

### フィルター {#filter}

インポートまたは除外するテーブルを指定する構成リスト。

詳細は[テーブルフィルター](/table-filter.md)参照。

<!-- I -->

## 私 {#i}

### インポートモード {#import-mode}

読み取り速度とスペース使用量を犠牲にして、書き込み用に TiKV を最適化する構成。

TiDB Lightningは実行中に自動的にインポートモードを切り替えます。ただし、TiKVがインポートモードで停止した場合は、 `tidb-lightning-ctl` ～ [強制的に元に戻す](/tidb-lightning/troubleshoot-tidb-lightning.md#the-tidb-cluster-uses-lots-of-cpu-resources-and-runs-very-slowly-after-using-tidb-lightning) ～ [通常モード](/tidb-lightning/tidb-lightning-glossary.md#normal-mode)使用してください。

### インデックスエンジン {#index-engine}

インデックスをソートする場合は[エンジン](/tidb-lightning/tidb-lightning-glossary.md#engine) 。

インデックスの数に関係なく、すべてのテーブルは 1 つのインデックス エンジンに関連付けられます。

TiDB Lightningは複数のインデックスエンジンを同時に処理します。これは`lightning.index-concurrency`設定によって制御されます。各テーブルには1つのインデックスエンジンがあるため、同時に処理できるテーブルの最大数も設定されます。

### 取り込み {#ingest}

[SSTファイル](/tidb-lightning/tidb-lightning-glossary.md#sst-file)の内容全体を RocksDB (TiKV) ストアに挿入する操作。

取り込みは、KVペアを1つずつ挿入する操作に比べて非常に高速です。この操作がTiDB Lightningのパフォーマンスを決定づける要因です。

技術的な詳細については[RocksDB の SST ファイルの作成と取り込みに関する wiki ページ](https://github.com/facebook/rocksdb/wiki/Creating-and-Ingesting-SST-files)参照してください。

<!-- K -->

## K {#k}

### KVペア {#kv-pair}

「キーと値のペア」の略語。

### KVエンコーダ {#kv-encoder}

SQLまたはCSV行をKVペアに解析するルーチン。複数のKVエンコーダーを並列実行することで処理を高速化します。

<!-- L -->

## L {#l}

### ローカルチェックサム {#local-checksum}

KV ペアを TiKV Importer に送信する前に、 TiDB Lightning自体によって計算されたテーブルの[チェックサム](/tidb-lightning/tidb-lightning-glossary.md#checksum) 。

<!-- N -->

## 北 {#n}

### 通常モード {#normal-mode}

[インポートモード](/tidb-lightning/tidb-lightning-glossary.md#import-mode)が無効になっているモード。

<!-- P -->

## P {#p}

### 後処理 {#post-processing}

データソース全体が解析され、TiKV Importer に送信された後の期間。TiDB TiDB Lightning はTiKV Importer のアップロードを待機し、 [SST ファイル](/tidb-lightning/tidb-lightning-glossary.md#sst-file)の[摂取する](/tidb-lightning/tidb-lightning-glossary.md#ingest) 。

<!-- R -->

## R {#r}

### リモートチェックサム {#remote-checksum}

インポート後に TiDB によって計算されたテーブルの[チェックサム](/tidb-lightning/tidb-lightning-glossary.md#checksum) 。

<!-- S -->

## S {#s}

### Scattering {#scattering}

[リージョン](/glossary.md#regionpeerraft-group)のリーダーとピアをランダムに再割り当てする操作。Scatteringにより、インポートされたデータが TiKV ストア間で均等に分散されます。これにより、PD への負荷が軽減されます。

### 分割 {#splitting}

通常、エンジンは非常に大きい (約 100 GB) ため、単一の[地域](/glossary.md#regionpeerraft-group)として扱うのは TiKV にとって扱いにくいものです。TiKV インポーターは、アップロードする前にエンジンを複数の小さな[SST ファイル](/tidb-lightning/tidb-lightning-glossary.md#sst-file) (TiKV インポーターの`import.region-split-size`設定で構成可能) に分割します。

### SSTファイル {#sst-file}

SSTは「sorted string table（ソートされた文字列テーブル）」の略です。SSTファイルは、RocksDB（およびTiKV）のKVペアのコレクションのネイティブstorage形式です。

TiKVインポーターは、閉じた[エンジン](/tidb-lightning/tidb-lightning-glossary.md#engine)からSSTファイルを生成します。これらのSSTファイルはアップロードされ、その後TiKVストアに[摂取した](/tidb-lightning/tidb-lightning-glossary.md#ingest)されます。
