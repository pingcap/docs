---
title: TiDB Lightning Glossary
summary: TiDB Lightningで使用される特殊用語のリスト。
---

# TiDB Lightning用語集 {#tidb-lightning-glossary}

このページでは、TiDB Lightning のログ、監視、構成、ドキュメントで使用される特殊な用語について説明します。

TiDB関連の用語と定義については、 [TiDB 用語集](/glossary.md)参照してください。

<!-- A -->

## あ {#a}

### 分析する {#analyze}

[`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)ステートメントを実行している TiDB テーブルの[統計](/statistics.md)情報を再構築する操作。

TiDB Lightning はTiDB を経由せずにデータをインポートするため、統計情報は自動的に更新されません。そのため、 TiDB Lightning はインポート後にすべてのテーブルを明示的に分析します。この手順は、 `post-restore.analyze`構成を`false`に設定することで省略できます。

### <code>AUTO_INCREMENT_ID</code> {#code-auto-increment-id-code}

各テーブルには、自動増分列のデフォルト値を提供する`AUTO_INCREMENT_ID`カウンターが関連付けられています。TiDB では、このカウンターは行 ID の割り当てにも使用されます。

TiDB Lightning はTiDB を経由せずにデータをインポートするため、 `AUTO_INCREMENT_ID`カウンターは自動的に更新されません。したがって、 TiDB Lightning は`AUTO_INCREMENT_ID`明示的に有効な値に変更します。テーブルに`AUTO_INCREMENT`列がない場合でも、この手順は常に実行されます。

<!-- B -->

## B {#b}

### バックエンド {#back-end}

バックエンドは、 TiDB Lightning が解析結果を送信する宛先です。「backend」とも表記されます。

詳細は[TiDB Lightningアーキテクチャ](/tidb-lightning/tidb-lightning-overview.md)参照。

<!-- C -->

## Ｃ {#c}

### チェックポイント {#checkpoint}

TiDB Lightning は、インポート中に進行状況をローカル ファイルまたはリモート データベースに継続的に保存します。これにより、プロセス中にクラッシュした場合でも、中間状態から再開できます。詳細については、セクション[チェックポイント](/tidb-lightning/tidb-lightning-checkpoints.md)を参照してください。

### チェックサム {#checksum}

TiDB Lightningでは、テーブルのチェックサムは、そのテーブル内の各 KV ペアの内容から計算された 3 つの数値のセットです。これらの数値はそれぞれ次のようになります。

-   KVペアの数、
-   すべてのKVペアの合計長さ、および
-   各ペアの[CRC-64-ECMA](https://en.wikipedia.org/wiki/Cyclic_redundancy_check)の値のビット単位の XOR。

TiDB Lightning [インポートされたデータを検証する](/tidb-lightning/tidb-lightning-faq.md#how-to-ensure-the-integrity-of-the-imported-data) 、各テーブルの[地元](/tidb-lightning/tidb-lightning-glossary.md#local-checksum)と[リモートチェックサム](/tidb-lightning/tidb-lightning-glossary.md#remote-checksum)比較します。いずれかのペアが一致しない場合は、プログラムは停止します。 `post-restore.checksum`構成を`false`に設定することで、このチェックをスキップできます。

チェックサムの不一致を適切に処理する方法については、 [よくある質問](/tidb-lightning/troubleshoot-tidb-lightning.md#checksum-failed-checksum-mismatched-remote-vs-local)も参照してください。

### Chunk {#chunk}

ソース データの連続した範囲。通常は、データ ソース内の 1 つのファイルに相当します。

ファイルが大きすぎる場合、 TiDB Lightning はファイルを複数のチャンクに分割することがあります。

### 圧縮 {#compaction}

複数の小さな SST ファイルを 1 つの大きな SST ファイルに結合し、削除されたエントリをクリーンアップする操作。TiDB TiDB Lightningがインポートしている間、TiKV はバックグラウンドでデータを自動的に圧縮します。

> **注記：**
>
> レガシーな理由から、テーブルがインポートされるたびに明示的に圧縮をトリガーするようにTiDB Lightningを構成することもできます。ただし、これは推奨されておらず、対応する設定はデフォルトで無効になっています。

技術的な詳細については[RocksDB の圧縮に関する wiki ページ](https://github.com/facebook/rocksdb/wiki/Compaction)参照してください。

<!-- D -->

## だ {#d}

### データエンジン {#data-engine}

実際の行データをソートする場合は[エンジン](/tidb-lightning/tidb-lightning-glossary.md#engine)です。

テーブルが非常に大きい場合、タスクのパイプライン処理を改善し、TiKV インポーターのスペースを節約するために、そのデータは複数のデータ エンジンに配置されます。デフォルトでは、SQL データ 100 GB ごとに新しいデータ エンジンが開かれますが、これは`mydumper.batch-size`設定で構成できます。

TiDB Lightning は複数のデータ エンジンを同時に処理します。これは`lightning.table-concurrency`設定によって制御されます。

<!-- E -->

## え {#e}

### エンジン {#engine}

TiKV インポーターでは、エンジンは KV ペアをソートするための RocksDB インスタンスです。

TiDB Lightning は、エンジンを通じてデータを TiKV Importer に転送します。最初にエンジンを開き、KV ペアを (特定の順序なしで) エンジンに送信し、最後にエンジンを閉じます。エンジンは、閉じた後に受信した KV ペアを並べ替えます。閉じたエンジンは、TiKV ストアにアップロードして取り込むことができます。

エンジンは、TiKV インポーター`import-dir`一時storageとして使用します。これは、「エンジン ファイル」と呼ばれることもあります。

[データエンジン](/tidb-lightning/tidb-lightning-glossary.md#data-engine)と[インデックスエンジン](/tidb-lightning/tidb-lightning-glossary.md#index-engine)も参照してください。

<!-- F -->

## ふ {#f}

### フィルター {#filter}

インポートまたは除外するテーブルを指定する構成リスト。

詳細は[テーブルフィルター](/table-filter.md)参照。

<!-- I -->

## 私 {#i}

### インポートモード {#import-mode}

読み取り速度とスペース使用量の低下を犠牲にして、書き込み用に TiKV を最適化する構成。

TiDB Lightning は実行中にインポート モードを自動的にオン/オフにします。ただし、TiKV がインポート モードで停止した場合は、 `tidb-lightning-ctl` ～ [強制的に元に戻す](/tidb-lightning/troubleshoot-tidb-lightning.md#the-tidb-cluster-uses-lots-of-cpu-resources-and-runs-very-slowly-after-using-tidb-lightning) ～ [通常モード](/tidb-lightning/tidb-lightning-glossary.md#normal-mode)使用できます。

### インデックスエンジン {#index-engine}

インデックスをソートする場合は[エンジン](/tidb-lightning/tidb-lightning-glossary.md#engine)です。

インデックスの数に関係なく、すべてのテーブルは 1 つのインデックス エンジンに関連付けられます。

TiDB Lightning は複数のインデックス エンジンを同時に処理します。これは`lightning.index-concurrency`設定によって制御されます。各テーブルには 1 つのインデックス エンジンがあるため、同時に処理するテーブルの最大数も設定されます。

### 取り込み {#ingest}

[SST ファイル](/tidb-lightning/tidb-lightning-glossary.md#sst-file)のコンテンツ全体を RocksDB (TiKV) ストアに挿入する操作。

取り込みは、KV ペアを 1 つずつ挿入する場合に比べて非常に高速な操作です。この操作がTiDB Lightningのパフォーマンスを決定する要因です。

技術的な詳細については[RocksDB の SST ファイルの作成と取り込みに関する wiki ページ](https://github.com/facebook/rocksdb/wiki/Creating-and-Ingesting-SST-files)参照してください。

<!-- K -->

## け {#k}

### KVペア {#kv-pair}

「キーと値のペア」の略語。

### KVエンコーダ {#kv-encoder}

SQL または CSV 行を KV ペアに解析するルーチン。複数の KV エンコーダーが並列に実行され、処理が高速化されます。

<!-- L -->

## ら {#l}

### ローカルチェックサム {#local-checksum}

KV ペアを TiKV Importer に送信する前に、 TiDB Lightning自体によって計算されたテーブルの[チェックサム](/tidb-lightning/tidb-lightning-glossary.md#checksum) 。

<!-- N -->

## いいえ {#n}

### 通常モード {#normal-mode}

[インポートモード](/tidb-lightning/tidb-lightning-glossary.md#import-mode)が無効になっているモード。

<!-- P -->

## ポ {#p}

### 後処理 {#post-processing}

データ ソース全体が解析され、TiKV Importer に送信された後の期間。TiDB TiDB Lightning はTiKV Importer がアップロードして[摂取する](/tidb-lightning/tidb-lightning-glossary.md#ingest)から[SST ファイル](/tidb-lightning/tidb-lightning-glossary.md#sst-file)まで待機します。

<!-- R -->

## R {#r}

### リモートチェックサム {#remote-checksum}

インポート後に TiDB によって計算されたテーブルの[チェックサム](/tidb-lightning/tidb-lightning-glossary.md#checksum) 。

<!-- S -->

## S {#s}

### Scattering {#scattering}

[リージョン](/glossary.md#regionpeerraft-group)のリーダーとピアをランダムに再割り当てする操作。Scatteringにより、インポートされたデータが TiKV ストア間で均等に分散されます。これにより、PD のストレスが軽減されます。

### 分割 {#splitting}

エンジンは通常非常に大きい (約 100 GB) ため、単一の[地域](/glossary.md#regionpeerraft-group)として扱うのは TiKV にとって扱いにくいものです。TiKV インポーターは、アップロードする前にエンジンを複数の小さな[SST ファイル](/tidb-lightning/tidb-lightning-glossary.md#sst-file) (TiKV インポーターの`import.region-split-size`設定で構成可能) に分割します。

### SST ファイル {#sst-file}

SST は「ソートされた文字列テーブル」の略語です。SST ファイルは、RocksDB (および TiKV) の KV ペアのコレクションのネイティブstorage形式です。

TiKV インポーターは、閉じた[エンジン](/tidb-lightning/tidb-lightning-glossary.md#engine)から SST ファイルを生成します。これらの SST ファイルはアップロードされ、その後 TiKV ストアに[摂取した](/tidb-lightning/tidb-lightning-glossary.md#ingest)れます。
