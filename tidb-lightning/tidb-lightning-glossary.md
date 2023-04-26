---
title: TiDB Lightning Glossary
summary: List of special terms used in TiDB Lightning.
---

# TiDB Lightning用語集 {#tidb-lightning-glossary}

このページでは、TiDB Lightning のログ、監視、構成、およびドキュメントで使用される特別な用語について説明します。

<!-- A -->

## あ {#a}

### 分析する {#analyze}

[`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)ステートメントを実行している TiDB テーブルの[統計](/statistics.md)情報を再構築する操作。

TiDB Lightning はTiDB を介さずにデータをインポートするため、統計情報は自動的に更新されません。したがって、 TiDB Lightning はインポート後にすべてのテーブルを明示的に分析します。 `post-restore.analyze`構成を`false`に設定すると、このステップを省略できます。

### <code>AUTO_INCREMENT_ID</code> {#code-auto-increment-id-code}

すべてのテーブルには、自動インクリメント列のデフォルト値を提供する`AUTO_INCREMENT_ID`カウンターが関連付けられています。 TiDB では、このカウンターは行 ID を割り当てるために追加で使用されます。

TiDB Lightning はTiDB を介さずにデータをインポートするため、 `AUTO_INCREMENT_ID`カウンターは自動的に更新されません。したがって、 TiDB Lightning は明示的に`AUTO_INCREMENT_ID`を有効な値に変更します。テーブルに`AUTO_INCREMENT`列がない場合でも、この手順は常に実行されます。

<!-- B -->

## B {#b}

### バックエンド {#back-end}

バックエンドは、 TiDB Lightning が解析結果を送信する宛先です。 「バックエンド」とも表記されます。

詳細は[TiDB Lightningアーキテクチャ](/tidb-lightning/tidb-lightning-overview.md)を参照してください。

<!-- C -->

## ハ {#c}

### チェックポイント {#checkpoint}

TiDB Lightning は、インポート中に進行状況をローカル ファイルまたはリモート データベースに継続的に保存します。これにより、プロセスでクラッシュした場合に中間状態から再開できます。詳細については、セクション[チェックポイント](/tidb-lightning/tidb-lightning-checkpoints.md)を参照してください。

### チェックサム {#checksum}

TiDB Lightningでは、テーブルのチェックサムは、そのテーブル内の各 KV ペアの内容から計算された 3 つの数値のセットです。これらの数値はそれぞれ次のとおりです。

-   KVペアの数、
-   すべての KV ペアの全長、および
-   各ペアの[CRC-64-ECMA](https://en.wikipedia.org/wiki/Cyclic_redundancy_check)の値のビットごとの XOR。

すべてのテーブルの[地元](/tidb-lightning/tidb-lightning-glossary.md#local-checksum)と[リモート チェックサム](/tidb-lightning/tidb-lightning-glossary.md#remote-checksum)比較することによるTiDB Lightning [インポートされたデータを検証します](/tidb-lightning/tidb-lightning-faq.md#how-to-ensure-the-integrity-of-the-imported-data) 。いずれかのペアが一致しない場合、プログラムは停止します。 `post-restore.checksum`構成を`false`に設定することで、このチェックをスキップできます。

チェックサムの不一致を適切に処理する方法については、 [よくある質問](/tidb-lightning/troubleshoot-tidb-lightning.md#checksum-failed-checksum-mismatched-remote-vs-local)も参照してください。

### Chunk {#chunk}

ソース データの連続した範囲。通常は、データ ソース内の 1 つのファイルに相当します。

ファイルが大きすぎる場合、 TiDB Lightning はファイルを複数のチャンクに分割することがあります。

### 締固め {#compaction}

複数の小さな SST ファイルを 1 つの大きな SST ファイルにマージし、削除されたエントリをクリーンアップする操作。 TiDB Lightningのインポート中に、TiKV はバックグラウンドで自動的にデータを圧縮します。

> **ノート：**
>
> 従来の理由から、テーブルがインポートされるたびに明示的に圧縮をトリガーするようにTiDB Lightningを引き続き構成できます。ただし、これはお勧めできません。対応する設定はデフォルトで無効になっています。

技術的な詳細については[圧縮に関する RocksDB の wiki ページ](https://github.com/facebook/rocksdb/wiki/Compaction)参照してください。

<!-- D -->

## D {#d}

### データエンジン {#data-engine}

実際の行データを並べ替える場合は[エンジン](/tidb-lightning/tidb-lightning-glossary.md#engine) 。

テーブルが非常に大きい場合、そのデータは複数のデータ エンジンに配置され、タスクのパイプライン処理が改善され、TiKV Importer のスペースが節約されます。デフォルトでは、100 GB の SQL データごとに新しいデータ エンジンが開かれます。これは`mydumper.batch-size`設定で構成できます。

TiDB Lightning は複数のデータ エンジンを同時に処理します。これは`lightning.table-concurrency`設定によって制御されます。

<!-- E -->

## え {#e}

### エンジン {#engine}

TiKV Importer では、エンジンは KV ペアをソートするための RocksDB インスタンスです。

TiDB Lightning は、エンジンを介してデータを TiKV Importer に転送します。最初にエンジンを開き、KV ペアを (特定の順序で) 送信し、最後にエンジンを閉じます。エンジンは、閉じた後、受信した KV ペアを並べ替えます。これらのクローズド エンジンは、取り込みのために TiKV ストアにさらにアップロードできます。

エンジンは TiKV Importer の`import-dir`一時storageとして使用し、「エンジン ファイル」と呼ばれることもあります。

[データエンジン](/tidb-lightning/tidb-lightning-glossary.md#data-engine)と[索引エンジン](/tidb-lightning/tidb-lightning-glossary.md#index-engine)も参照してください。

<!-- F -->

## ふ {#f}

### フィルター {#filter}

インポートまたは除外するテーブルを指定する構成リスト。

詳細は[テーブル フィルター](/table-filter.md)を参照してください。

<!-- I -->

## 私 {#i}

### インポート モード {#import-mode}

読み取り速度とスペース使用量の低下を犠牲にして、書き込み用に TiKV を最適化する構成。

TiDB Lightning は、実行中にインポート モードを自動的に切り替えます。ただし、TiKV がインポート モードで動かなくなった場合は、 `tidb-lightning-ctl` ～ [強制復帰](/tidb-lightning/troubleshoot-tidb-lightning.md#the-tidb-cluster-uses-lots-of-cpu-resources-and-runs-very-slowly-after-using-tidb-lightning) ～ [ノーマルモード](/tidb-lightning/tidb-lightning-glossary.md#normal-mode)を使用できます。

### 索引エンジン {#index-engine}

インデックスを並べ替える場合は[エンジン](/tidb-lightning/tidb-lightning-glossary.md#engine) 。

インデックスの数に関係なく、すべてのテーブルは 1 つのインデックス エンジンに関連付けられています。

TiDB Lightning は、複数のインデックス エンジンを同時に処理します。これは`lightning.index-concurrency`設定によって制御されます。すべてのテーブルには 1 つのインデックス エンジンしかないため、同時に処理するテーブルの最大数も構成されます。

### 取り込み {#ingest}

[SSTファイル](/tidb-lightning/tidb-lightning-glossary.md#sst-file)のコンテンツ全体を RocksDB (TiKV) ストアに挿入する操作。

取り込みは、KV ペアを 1 つずつ挿入するのに比べて非常に高速な操作です。この操作は、 TiDB Lightningのパフォーマンスの決定要因です。

技術的な詳細については[SST ファイルの作成と取り込みに関する RocksDB の wiki ページ](https://github.com/facebook/rocksdb/wiki/Creating-and-Ingesting-SST-files)参照してください。

<!-- K -->

## K {#k}

### KVペア {#kv-pair}

「キーバリューペア」の略。

### KV エンコーダ {#kv-encoder}

SQL または CSV 行を解析して KV ペアにするルーチン。複数の KV エンコーダーが並行して実行され、処理が高速化されます。

<!-- L -->

## L {#l}

### ローカル チェックサム {#local-checksum}

KV ペアを TiKV Importer に送信する前に、 TiDB Lightning自体によって計算されたテーブルの[チェックサム](/tidb-lightning/tidb-lightning-glossary.md#checksum) 。

<!-- N -->

## N {#n}

### ノーマルモード {#normal-mode}

[インポート モード](/tidb-lightning/tidb-lightning-glossary.md#import-mode)が無効なモード。

<!-- P -->

## P {#p}

### 後処理 {#post-processing}

データ ソース全体が解析され、TiKV Importer に送信された後の期間。 TiDB Lightning はTiKV Importer がアップロードするのを待っており、 [摂取する](/tidb-lightning/tidb-lightning-glossary.md#ingest) the [SST ファイル](/tidb-lightning/tidb-lightning-glossary.md#sst-file) .

<!-- R -->

## R {#r}

### リモート チェックサム {#remote-checksum}

インポート後に TiDB によって計算されたテーブルの[チェックサム](/tidb-lightning/tidb-lightning-glossary.md#checksum) 。

<!-- S -->

## S {#s}

### Scattering {#scattering}

[リージョン](/glossary.md#regionpeerraft-group)のリーダーとピアをランダムに再割り当てする操作。Scattering、インポートされたデータが TiKV ストア間で均等に分散されます。これにより、PD のストレスが軽減されます。

### 分割 {#splitting}

通常、エンジンは非常に大きく (約 100 GB)、単一の[領域](/glossary.md#regionpeerraft-group)として扱われると TiKV には適していません。 TiKV Importer は、アップロードする前にエンジンを複数の小さな[SST ファイル](/tidb-lightning/tidb-lightning-glossary.md#sst-file) (TiKV Importer の`import.region-split-size`設定で構成可能) に分割します。

### SSTファイル {#sst-file}

SST は「ソートされた文字列テーブル」の略です。 SST ファイルは、KV ペアのコレクションの RocksDB (したがって TiKV) のネイティブstorage形式です。

TiKV Importer は、閉じた[エンジン](/tidb-lightning/tidb-lightning-glossary.md#engine)から SST ファイルを生成します。これらの SST ファイルはアップロードされ、TiKV ストアに[摂取した](/tidb-lightning/tidb-lightning-glossary.md#ingest)されます。
