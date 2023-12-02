---
title: TiDB Lightning Glossary
summary: List of special terms used in TiDB Lightning.
---

# TiDB Lightning用語集 {#tidb-lightning-glossary}

このページでは、TiDB Lightning のログ、モニタリング、構成、およびドキュメントで使用される特別な用語について説明します。

<!-- A -->

## あ {#a}

### 分析する {#analyze}

[`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)ステートメントを実行している TiDB テーブルの[統計](/statistics.md)情報を再構築する操作。

TiDB Lightning はTiDB を経由せずにデータをインポートするため、統計情報は自動的に更新されません。したがって、 TiDB Lightning はインポート後にすべてのテーブルを明示的に分析します。この手順は、 `post-restore.analyze`構成を`false`に設定することで省略できます。

### <code>AUTO_INCREMENT_ID</code> {#code-auto-increment-id-code}

すべてのテーブルには、自動インクリメント列のデフォルト値を提供する`AUTO_INCREMENT_ID`カウンターが関連付けられています。 TiDB では、このカウンターは行 ID を割り当てるためにさらに使用されます。

TiDB Lightning はTiDB を経由せずにデータをインポートするため、 `AUTO_INCREMENT_ID`カウンターは自動的に更新されません。したがって、 TiDB Lightning は`AUTO_INCREMENT_ID`明示的に有効な値に変更します。このステップは、テーブルに`AUTO_INCREMENT`列がない場合でも常に実行されます。

<!-- B -->

## B {#b}

### バックエンド {#back-end}

バックエンドは、 TiDB Lightning が解析結果を送信する宛先です。 「バックエンド」とも表記されます。

詳細については[TiDB Lightningアーキテクチャ](/tidb-lightning/tidb-lightning-overview.md)を参照してください。

<!-- C -->

## C {#c}

### チェックポイント {#checkpoint}

TiDB Lightning は、インポート中に進行状況をローカル ファイルまたはリモート データベースに継続的に保存します。これにより、プロセス中にクラッシュした場合でも、中間状態から再開できます。詳細については、 [チェックポイント](/tidb-lightning/tidb-lightning-checkpoints.md)セクションを参照してください。

### チェックサム {#checksum}

TiDB Lightningでは、テーブルのチェックサムは、そのテーブル内の各 KV ペアの内容から計算された 3 つの数値のセットです。これらの数値はそれぞれ次のとおりです。

-   KV ペアの数、
-   すべての KV ペアの合計長、および
-   各ペアの[CRC-64-ECMA](https://en.wikipedia.org/wiki/Cyclic_redundancy_check)の値のビットごとの XOR。

TiDB Lightning [インポートされたデータを検証します](/tidb-lightning/tidb-lightning-faq.md#how-to-ensure-the-integrity-of-the-imported-data)各表の[地元](/tidb-lightning/tidb-lightning-glossary.md#local-checksum)と[リモートチェックサム](/tidb-lightning/tidb-lightning-glossary.md#remote-checksum)を比較します。いずれかのペアが一致しない場合、プログラムは停止します。 `post-restore.checksum`構成を`false`に設定すると、このチェックをスキップできます。

チェックサムの不一致を適切に処理する方法については、 [よくある質問](/tidb-lightning/troubleshoot-tidb-lightning.md#checksum-failed-checksum-mismatched-remote-vs-local)も参照してください。

### Chunk {#chunk}

ソース データの連続した範囲。通常はデータ ソース内の 1 つのファイルに相当します。

ファイルが大きすぎる場合、 TiDB Lightning はファイルを複数のチャンクに分割することがあります。

### 圧縮 {#compaction}

複数の小さな SST ファイルを 1 つの大きな SST ファイルにマージし、削除されたエントリをクリーンアップする操作。 TiKV は、 TiDB Lightningのインポート中にバックグラウンドでデータを自動的に圧縮します。

> **注記：**
>
> 従来の理由から、テーブルがインポートされるたびに明示的に圧縮をトリガーするようにTiDB Lightningを設定することもできます。ただし、これはお勧めできません。対応する設定はデフォルトで無効になっています。

技術的な詳細については[RocksDB の圧縮に関する wiki ページ](https://github.com/facebook/rocksdb/wiki/Compaction)参照してください。

<!-- D -->

## D {#d}

### データエンジン {#data-engine}

実際の行データをソートする場合は[エンジン](/tidb-lightning/tidb-lightning-glossary.md#engine) 。

テーブルが非常に大きい場合、そのデータは複数のデータ エンジンに配置され、タスクのパイプライン処理が改善され、TiKV インポーターのスペースが節約されます。デフォルトでは、100 GB の SQL データごとに新しいデータ エンジンが開きます。これは`mydumper.batch-size`設定で構成できます。

TiDB Lightning は複数のデータ エンジンを同時に処理します。これは`lightning.table-concurrency`設定によって制御されます。

<!-- E -->

## E {#e}

### エンジン {#engine}

TiKV Importer では、エンジンは KV ペアをソートするための RocksDB インスタンスです。

TiDB Lightning は、エンジンを通じてデータを TiKV Importer に転送します。まずエンジンを開き、KV ペアをそれに送信し (特に順序はありません)、最後にエンジンを閉じます。エンジンは閉じられた後に、受信した KV ペアを並べ替えます。これらのクローズド エンジンは、さらに TiKV ストアにアップロードして取り込むことができます。

エンジンは TiKV Importer の`import-dir`一時storageとして使用します。これは「エンジン ファイル」と呼ばれることもあります。

[データエンジン](/tidb-lightning/tidb-lightning-glossary.md#data-engine)と[インデックスエンジン](/tidb-lightning/tidb-lightning-glossary.md#index-engine)も参照してください。

<!-- F -->

## F {#f}

### フィルター {#filter}

どのテーブルをインポートまたは除外するかを指定する構成リスト。

詳細については[テーブルフィルター](/table-filter.md)を参照してください。

<!-- I -->

## 私 {#i}

### インポートモード {#import-mode}

読み取り速度とスペース使用量の低下を犠牲にして、書き込み用に TiKV を最適化する構成。

TiDB Lightning は、実行中に自動的にインポート モードに切り替わったり、インポート モードがオフになったりします。ただし、TiKV がインポート モードでスタックした場合は、 `tidb-lightning-ctl` ～ [強制的に元に戻す](/tidb-lightning/troubleshoot-tidb-lightning.md#the-tidb-cluster-uses-lots-of-cpu-resources-and-runs-very-slowly-after-using-tidb-lightning) ～ [ノーマルモード](/tidb-lightning/tidb-lightning-glossary.md#normal-mode)を使用できます。

### インデックスエンジン {#index-engine}

インデックスをソートする場合は[エンジン](/tidb-lightning/tidb-lightning-glossary.md#engine) 。

インデックスの数に関係なく、すべてのテーブルは 1 つのインデックス エンジンにのみ関連付けられます。

TiDB Lightning は複数のインデックス エンジンを同時に処理します。これは`lightning.index-concurrency`設定によって制御されます。すべてのテーブルにはインデックス エンジンが 1 つだけあるため、同時に処理するテーブルの最大数もこれによって構成されます。

### 取り込み {#ingest}

[SSTファイル](/tidb-lightning/tidb-lightning-glossary.md#sst-file)の内容全体を RocksDB (TiKV) ストアに挿入する操作。

取り込みは、KV ペアを 1 つずつ挿入する場合と比べて、非常に高速な操作です。この操作は、 TiDB Lightningのパフォーマンスの決定要因となります。

技術的な詳細については[SST ファイルの作成と取り込みに関する RocksDB の Wiki ページ](https://github.com/facebook/rocksdb/wiki/Creating-and-Ingesting-SST-files)参照してください。

<!-- K -->

## K {#k}

### KVペア {#kv-pair}

「キーと値のペア」の略称。

### KVエンコーダ {#kv-encoder}

SQL または CSV 行を KV ペアに解析するルーチン。複数の KV エンコーダを並列実行して処理を高速化します。

<!-- L -->

## L {#l}

### ローカルチェックサム {#local-checksum}

KV ペアを TiKV Importer に送信する前に、 TiDB Lightning自体によって計算されるテーブルの[チェックサム](/tidb-lightning/tidb-lightning-glossary.md#checksum) 。

<!-- N -->

## N {#n}

### ノーマルモード {#normal-mode}

[インポートモード](/tidb-lightning/tidb-lightning-glossary.md#import-mode)が無効になるモード。

<!-- P -->

## P {#p}

### 後処理 {#post-processing}

データ ソース全体が解析されて TiKV インポーターに送信された後の期間。 TiDB Lightning は、 TiKV インポーターがアップロードするのを待っています[摂取する](/tidb-lightning/tidb-lightning-glossary.md#ingest) [SST ファイル](/tidb-lightning/tidb-lightning-glossary.md#sst-file) 。

<!-- R -->

## R {#r}

### リモートチェックサム {#remote-checksum}

インポート後に TiDB によって計算されたテーブルの[チェックサム](/tidb-lightning/tidb-lightning-glossary.md#checksum) 。

<!-- S -->

## S {#s}

### Scattering {#scattering}

[リージョン](/glossary.md#regionpeerraft-group)のリーダーとピアをランダムに再割り当てする操作。Scattering、インポートされたデータが TiKV ストア間で均等に分散されます。これにより、PD へのストレスが軽減されます。

### 分割 {#splitting}

通常、エンジンは非常に大きく (約 100 GB)、単一の[地域](/glossary.md#regionpeerraft-group)として扱う場合は TiKV にとって好ましくありません。 TiKV Importer は、アップロードする前にエンジンを複数の小さな[SST ファイル](/tidb-lightning/tidb-lightning-glossary.md#sst-file) (TiKV Importer の`import.region-split-size`設定で構成可能) に分割します。

### SSTファイル {#sst-file}

SSTとは「ソート文字列テーブル」の略称です。 SST ファイルは、RocksDB (したがって TiKV) の KV ペアのコレクションのネイティブstorage形式です。

TiKV インポーターは、閉じた[エンジン](/tidb-lightning/tidb-lightning-glossary.md#engine)から SST ファイルを生成します。これらの SST ファイルはアップロードされ、TiKV ストアに[摂取した](/tidb-lightning/tidb-lightning-glossary.md#ingest)されます。
