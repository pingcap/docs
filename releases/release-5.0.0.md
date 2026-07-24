---
title: What's New in TiDB 5.0
summary: TiDB 5.0では、MPPアーキテクチャ、クラスター化インデックス、非同期コミット、および安定性の向上が導入されています。また、互換性の変更、構成パラメータ、および新機能も強化されています。さらに、パフォーマンス、高可用性、ディザスタリカバリ、データ移行、診断、デプロイ、およびメンテナンスが最適化されています。クラスタの使用状況メトリクス用のテレメトリ機能も追加されています。
---

# TiDB 5.0の新機能 {#what-s-new-in-tidb-5-0}

発売日：2021年4月7日

TiDB バージョン: 5.0.0

バージョン5.0では、PingCAPは企業がTiDBをベースとしたアプリケーションを迅速に構築できるよう支援することに特化しており、データベースのパフォーマンス、パフォーマンスの変動、セキュリティ、高可用性、ディザスタリカバリ、SQLパフォーマンスのトラブルシューティングなどに関する懸念から解放します。

バージョン5.0における主な新機能または改善点は以下のとおりです。

-   TiFlashノードを介して大規模並列処理（MPP）アーキテクチャを導入し、大規模な結合クエリの実行ワークロードをTiFlashノード間で共有します。MPPモードが有効になっている場合、TiDBはコストに基づいて、計算を実行するためにMPPフレームワークを使用するかどうかを決定します。MPPモードでは、結合キーは計算中に`Exchange`操作によって再分配され、計算負荷が各TiFlashノードに分散され、計算が高速化されます。ベンチマークによると、同じクラスタリソースを使用した場合、TiDB 5.0 MPPはGreenplum 6.15.0およびApache Spark 3.1.1と比較して2～3倍高速化され、一部のクエリでは8倍のパフォーマンス向上を実現しています。
-   データベースのパフォーマンスを向上させるために、クラスター化インデックス機能を導入します。例えば、TPC-C tpmCテストでは、クラスター化インデックスを有効にしたTiDBのパフォーマンスは39%向上しました。
-   非同期コミット機能を有効にすると、書き込みレイテンシーを削減できます。例えば、64スレッドのSysbenchテストでは、非同期コミットを有効にした場合、インデックス更新の平均レイテンシーは12.04msから7.01msへと41.7%削減されます。
-   ジッターを低減します。これは、オプティマイザの安定性を向上させ、システムタスクによるI/O、ネットワーク、CPU、メモリリソースの使用を制限することによって実現されます。例えば、8時間のパフォーマンステストでは、TPC-C tpmCの標準偏差は2%を超えません。
-   スケジューリングを改善し、実行計画を可能な限り安定させることで、システムの安定性を向上させる。
-   リージョンメンバーシップの変更時にもシステムの可用性を保証するRaft共同合意アルゴリズムを導入します。
-   `EXPLAIN`機能と不可視インデックスを最適化することで、データベース管理者 (DBA) が SQL ステートメントをより効率的にデバッグできるようになります。
-   企業データの信頼性を保証します。TiDBからAmazon S3ストレージやGoogle Cloud GCSにデータをバックアップしたり、これらのクラウドストレージプラットフォームからデータを復元したりできます。
-   Amazon S3ストレージまたはTiDB/MySQLへのデータインポートおよびデータエクスポートのパフォーマンスが向上し、企業がクラウド上でアプリケーションを迅速に構築できるようになります。例えば、TPC-Cテストでは、1 TiBのデータをインポートする際のパフォーマンスが40%向上し、254 GiB/hから366 GiB/hになりました。

## 互換性の変更 {#compatibility-changes}

### システム変数 {#system-variables}

-   複数のオペレーターの同時実行を制御するには、 [`tidb_executor_concurrency`](/system-variables.md#tidb_executor_concurrency-new-in-v50)システム変数を追加します。以前の`tidb_*_concurrency`設定 ( `tidb_projection_concurrency`など) は引き続き有効ですが、使用時に警告が表示されます。

-   ASCII文字セットを書き込む際にASCII検証チェックをスキップするかどうかを指定するには、 [`tidb_skip_ascii_check`](/system-variables.md#tidb_skip_ascii_check-new-in-v50)システム変数を追加します。デフォルト値は`OFF`です。

-   テーブルスキーマで`double(N)`のような構文を定義できるかどうかを判断するには、 [`tidb_enable_strict_double_type_check`](/system-variables.md#tidb_enable_strict_double_type_check-new-in-v50)システム変数を追加します。デフォルト値は`OFF`です。

-   [`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size)のデフォルト値を`20000`から`0`に変更します。これは、 `LOAD` / `INSERT INTO SELECT ...`ではバッチ DML ステートメントがデフォルトで使用されなくなることを意味します。代わりに、厳密なACIDセマンティクスに準拠するために、大規模なトランザクションが使用されます。

    > **Note:**
    >
    > 変数のスコープがセッションからグローバルに変更され、デフォルト値が`20000`から`0`に変更されました。アプリケーションが元のデフォルト値に依存している場合は、アップグレード後に`set global`ステートメントを使用して変数を元の値に変更する必要があります。

-   一時テーブルの構文互換性は、システム変数[`tidb_enable_noop_functions`](/system-variables.md#tidb_enable_noop_functions-new-in-v40)を使用して制御します。この変数の値が`OFF`の場合、 `CREATE TEMPORARY TABLE`構文はエラーを返します。

-   ガベージコレクション関連のパラメータを直接制御するには、以下のシステム変数を追加してください。
    -   [`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-new-in-v50)
    -   [`tidb_gc_enable`](/system-variables.md#tidb_gc_enable-new-in-v50)
    -   [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)
    -   [`tidb_gc_run_interval`](/system-variables.md#tidb_gc_run_interval-new-in-v50)
    -   [`tidb_gc_scan_lock_mode`](/system-variables.md#tidb_gc_scan_lock_mode-new-in-v50)

-   [`enable-joint-consensus`](/pd-configuration-file.md#enable-joint-consensus-new-in-v50)のデフォルト値を`false`から`true`に変更すると、ジョイントコンセンサス機能がデフォルトで有効になります。

-   `tidb_enable_amend_pessimistic_txn`の値を`0`または`1`から`ON`または`OFF`に変更します。

-   [`tidb_enable_clustered_index`](/system-variables.md#tidb_enable_clustered_index-new-in-v50)のデフォルト値を`OFF`から`INT_ONLY`に変更し、以下の新しい意味を設定します。
    -   `ON` : クラスター化インデックスが有効になっています。非クラスター化インデックスの追加または削除がサポートされています。

    -   `OFF` : クラスター化インデックスは無効になっています。非クラスター化インデックスの追加または削除はサポートされています。

    -   `INT_ONLY` : デフォルト値。動作はv5.0以前と同じです。 `alter-primary-key = false`と併せて、INT型のクラスター化インデックスを有効にするかどうかを制御できます。
    > **Note:**
    >
    > 5.0 GA の`tidb_enable_clustered_index`の`INT_ONLY`値は、5.0 RC の`OFF`値と同じ意味です。 `OFF`設定の 5.0 RC クラスターから 5.0 GA にアップグレードすると、 `INT_ONLY`と表示されます。

### コンフィグレーションファイルパラメータ {#configuration-file-parameters}

-   TiDB の[`index-limit`](/tidb-configuration-file.md#index-limit-new-in-v50)設定項目を追加します。デフォルト値は`64`で、範囲は`[64,512]`です。MySQL テーブルは最大 64 個のインデックスをサポートします。この値がデフォルト設定を超え、テーブルに 64 個を超えるインデックスが作成された場合、テーブル スキーマが MySQL に再インポートされるとエラーが報告されます。
-   TiDB が MySQL の ENUM/SET の長さ (ENUM の長さ &lt; 255) と互換性があり、一貫性を保つように、 [`enable-enum-length-limit`](/tidb-configuration-file.md#enable-enum-length-limit-new-in-v50)設定項目を追加します。デフォルト値は`true`です。
-   `pessimistic-txn.enable`設定項目を[`tidb_txn_mode`](/system-variables.md#tidb_txn_mode)環境変数に置き換えてください。
-   `performance.max-memory`設定項目を[`performance.server-memory-quota`](/tidb-configuration-file.md#server-memory-quota-new-in-v409)に置き換えます。
-   `tikv-client.copr-cache.enable`設定項目を[`tikv-client.copr-cache.capacity-mb`](/tidb-configuration-file.md#capacity-mb)に置き換えます。項目の値が`0.0`の場合、この機能は無効になります。項目の値が`0.0`より大きい場合、この機能は有効になります。デフォルト値は`1000.0`です。
-   `rocksdb.auto-tuned`設定項目を[`rocksdb.rate-limiter-auto-tuned`](/tikv-configuration-file.md#rate-limiter-auto-tuned-new-in-v50)に置き換えます。
-   `raftstore.sync-log`設定項目を削除します。デフォルトでは、書き込まれたデータは強制的にディスクに書き込まれます。v5.0 より前は、 `raftstore.sync-log`明示的に無効にできます。v5.0 以降では、設定値は`true`に強制的に設定されます。
-   `gc.enable-compaction-filter`設定項目のデフォルト値を`false`から`true`に変更します。
-   `enable-cross-table-merge`設定項目のデフォルト値を`false`から`true`に変更します。
-   [`rate-limiter-auto-tuned`](/tikv-configuration-file.md#rate-limiter-auto-tuned-new-in-v50)設定項目のデフォルト値を`false`から`true`に変更します。

### その他 {#others}

-   アップグレード前に、TiDB構成の[`feedback-probability`](https://docs-archive.pingcap.com/tidb/v5.0/tidb-configuration-file#feedback-probability)の値を確認してください。値が0でない場合、アップグレード後に「回復可能なゴルーチンでpanicが発生しました」というエラーが発生しますが、このエラーはアップグレード自体には影響しません。
-   列の型変更時に、 `VARCHAR`型と`CHAR`型の間の変換を禁止し、データの正確性に関する問題を回避する。

## 新機能 {#new-features}

### SQL {#sql}

#### List パーティショニング（<strong>Experimental</strong>） {#list-partitioning-strong-experimental-strong}

[ユーザー向けドキュメント](/partitioned-table.md#list-partitioning)

リストパーティショニング機能を使用すると、大量のデータを含むテーブルを効率的にクエリおよび管理できます。

この機能を有効にすると、 `PARTITION BY LIST(expr) PARTITION part_name VALUES IN (...)`式に従ってパーティションとパーティション間のデータの分散方法が定義されます。パーティション化されたテーブルのデータセットは、最大 1024 個の異なる整数値をサポートします。これらの値は`PARTITION ... VALUES IN (...)`句を使用して定義できます。

リストパーティショニングを有効にするには、セッション変数[`tidb_enable_list_partition`](/system-variables.md#tidb_enable_list_partition-new-in-v50) `ON`に設定します。

#### List COLUMNS パーティショニング（<strong>Experimental</strong>） {#list-columns-partitioning-strong-experimental-strong}

[ユーザー向けドキュメント](/partitioned-table.md#list-columns-partitioning)

List COLUMNS パーティショニングは、リストパーティショニングの一種です。複数の列をパーティションキーとして使用できます。整数データ型の他に、文字列、 `DATE` 、および`DATETIME`データ型の列もパーティション列として使用できます。

List COLUMNS パーティショニングを有効にするには、セッション変数[`tidb_enable_list_partition`](/system-variables.md#tidb_enable_list_partition-new-in-v50) `ON`に設定します。

#### 不可視インデックス {#invisible-indexes}

[ユーザー向けドキュメント](/sql-statements/sql-statement-alter-index.md)、 [#9246](https://github.com/pingcap/tidb/issues/9246)

パフォーマンスを調整したり、最適なインデックスを選択したりする場合、SQL ステートメントを使用してインデックスを`Visible`または`Invisible`に設定できます。この設定により、 `DROP INDEX`や`ADD INDEX`などのリソースを消費する操作の実行を回避できます。

インデックスの表示設定を変更するには、 `ALTER INDEX`ステートメントを使用します。変更後、オプティマイザはインデックスの表示設定に基づいて、このインデックスをインデックスリストに追加するかどうかを決定します。

#### <code>EXCEPT</code>演算子と<code>INTERSECT</code>演算子 {#code-except-code-and-code-intersect-code-operators}

[ユーザー向けドキュメント](/functions-and-operators/set-operators.md)、 [#18031](https://github.com/pingcap/tidb/issues/18031)

`INTERSECT`演算子は集合演算子であり、2つ以上のクエリの結果セットの共通部分を返します。これは、 `Inner Join`演算子の代替手段と言えます。

`EXCEPT`演算子は集合演算子であり、2つのクエリの結果セットを結合し、最初のクエリ結果には含まれるが2番目のクエリ結果には含まれない要素を返します。

### トランザクション {#transaction}

[#18005](https://github.com/pingcap/tidb/issues/18005)

悲観的トランザクション モードでは、トランザクションに関係するテーブルに同時 DDL 操作または`SCHEMA VERSION`変更が含まれている場合、トランザクションのコミットが成功するように、またトランザクションが DDL 操作または`SCHEMA VERSION`変更によって中断されたときにクライアントが`Information schema is changed`エラーを受け取るのを避けるために、システムはトランザクションの`SCHEMA VERSION`最新の状態に自動的に更新します。

この機能はデフォルトでは無効になっています。機能を有効にするには、システム変数`tidb_enable_amend_pessimistic_txn`の値を変更してください。この機能はバージョン 4.0.7 で導入され、バージョン 5.0 で以下の問題が修正されています。

-   TiDB Binlog が`Add Column`操作を実行する際に発生する互換性の問題
-   一意インデックスとこの機能を併用した場合に発生するデータ不整合の問題
-   追加されたインデックスとこの機能を併用した場合に発生するデータ不整合の問題

現在、この機能には以下の互換性の問題が残っています。

-   同時トランザクションが発生すると、トランザクションの意味が変わる可能性があります。
-   TiDB Binlogと併用した場合に発生する既知の互換性の問題
-   `Change Column`との非互換性

### 文字セットと照合順序 {#character-set-and-collation}

-   `utf8mb4_unicode_ci`および`utf8_unicode_ci`照合順序をサポートします。 [ユーザー向けドキュメント](/character-set-and-collation.md#new-framework-for-collations)、 [#17596](https://github.com/pingcap/tidb/issues/17596)
-   照合順序における大文字小文字を区別しない比較ソートをサポートする

### セキュリティ {#security}

[ユーザー向けドキュメント](/log-redaction.md)、 [#18566](https://github.com/pingcap/tidb/issues/18566)

セキュリティコンプライアンス要件（*一般データ保護規則*、GDPRなど）を満たすため、システムは出力されるエラーメッセージやログから情報（IDやクレジットカード番号など）を匿名化する機能をサポートしており、機密情報の漏洩を防ぐことができます。

TiDBは出力ログ情報の非機密化をサポートしています。この機能を有効にするには、以下のスイッチを使用してください。

-   グローバル変数[`tidb_redact_log`](/system-variables.md#tidb_redact_log) 。デフォルト値は`0`で、これは非機密化が無効になっていることを意味します。tidb-server ログの非機密化を有効にするには、変数の値を`1`に設定します。
-   設定項目`security.redact-info-log` 。デフォルト値は`false`で、これは非感度化が無効になっていることを意味します。tikv-server ログの非感度化を有効にするには、変数の値を`true`に設定します。
-   設定項目`security.redact-info-log` 。デフォルト値は`false`で、これは非機密化が無効になっていることを意味します。pd-server ログの非機密化を有効にするには、変数の値を`true`に設定します。
-   tiflash-server の構成項目`security.redact_info_log`と tiflash-learner の構成項目`security.redact-info-log`です。デフォルト値はどちらも`false`で、これは感度低減が無効になっていることを意味します。tiflash-server と tiflash-learner のログの感度低減を有効にするには、両方の変数の値を`true`に設定します。

この機能はバージョン5.0で導入されました。この機能を使用するには、上記のシステム変数とすべての設定項目を有効にしてください。

## パフォーマンス最適化 {#performance-optimization}

### MPPアーキテクチャ {#mpp-architecture}

[ユーザー向けドキュメント](/tiflash/use-tiflash-mpp-mode.md)

TiDBは、 TiFlashノードを通じてMPPアーキテクチャを導入しています。このアーキテクチャにより、複数のTiFlashノードが大規模な結合クエリの実行ワークロードを共有することが可能になります。

MPPモードが有効な場合、TiDBは計算コストに基づいて、クエリをMPPエンジンに送信して計算を行うかどうかを判断します。MPPモードでは、TiDBはデータ計算中に結合キーを再分配することで（ `Exchange`操作）、テーブル結合の計算を各実行中のTiFlashノードに分散し、計算を高速化します。さらに、 TiFlashが既にサポートしている集計計算機能により、TiDBはクエリの計算をTiFlash MPPクラスタにプッシュダウンできます。これにより、分散環境が実行プロセス全体を高速化し、分析クエリの速度を大幅に向上させることができます。

TPC-H 100ベンチマークテストにおいて、 TiFlash MPPは従来の分析データベースやHadoop上のSQLの分析エンジンに比べて大幅な処理速度向上を実現しています。このアーキテクチャにより、最新のトランザクションデータに対して大規模な分析クエリを直接実行でき、従来のオフライン分析ソリューションよりも高いパフォーマンスを発揮します。ベンチマークによると、同じクラスタリソースを使用した場合、TiDB 5.0 MPPはGreenplum 6.15.0およびApache Spark 3.1.1に比べて2～3倍の高速化を実現し、一部のクエリでは8倍のパフォーマンス向上を達成しています。

現在、MPP モードがサポートしていない主な機能は次のとおりです (詳細については、 [TiFlashを使用する](/tiflash/use-tiflash-mpp-mode.md)を参照してください)。

-   テーブルパーティショニング
-   ウィンドウ機能
-   照合
-   組み込み関数
-   TiKVからデータを読み取る
-   OOM流出
-   連合
-   フルアウタージョイント

### クラスター化インデックス {#clustered-index}

[ユーザー向けドキュメント](/clustered-indexes.md)、 [#4841](https://github.com/pingcap/tidb/issues/4841)

テーブル構造を設計したり、データベースの動作を分析したりする際に、主キーを持つ一部の列が頻繁にグループ化およびソートされ、これらの列に対するクエリが特定の範囲のデータまたは異なる値を持つ少量のデータを頻繁に返し、対応するデータが読み取りまたは書き込みのホットスポット問題を引き起こさないことがわかった場合は、クラスター化インデックス機能を使用することをお勧めします。

クラスター化インデックスは、テーブルのデータに関連付けられたストレージ構造です。一部のデータベース管理システムでは、クラスター化インデックステーブルを*インデックス構成テーブル*と呼びます。クラスター化インデックスを作成する際には、テーブルの1つ以上の列をインデックスのキーとして指定できます。TiDBはこれらのキーを特定の構造に格納するため、キーに関連付けられた行を迅速かつ効率的に検索でき、クエリとデータ書き込みのパフォーマンスが向上します。

クラスター化インデックス機能を有効にすると、TiDB のパフォーマンスは大幅に向上します (例えば、TPC-C tpmC テストでは、クラスター化インデックスを有効にした TiDB のパフォーマンスは、以下のケースで 39% 向上します)。

-   データが挿入される際、クラスター化インデックスによって、ネットワークからのインデックスデータの書き込み回数が1回削減されます。
-   同等の条件を持つクエリが主キーのみに関係する場合、クラスター化インデックスによってネットワークからのインデックスデータの読み取り回数が1回削減されます。
-   範囲条件を含むクエリが主キーのみに関係する場合、クラスター化インデックスはネットワークからのインデックスデータの読み取り回数を削減します。
-   同等条件または範囲条件を含むクエリに主キーのプレフィックスが含まれる場合、クラスター化インデックスによってネットワークからのインデックスデータの読み取り回数が削減されます。

各テーブルは、クラスター化インデックスまたは非クラスター化インデックスのいずれかを使用してデータをソートおよび格納できます。これら2つのストレージ構造の違いは次のとおりです。

-   クラスター化インデックスを作成する際、テーブル内の1つまたは複数の列をインデックスのキー値として指定できます。クラスター化インデックスは、キー値に基づいてテーブルのデータをソートして格納します。各テーブルには、クラスター化インデックスを1つだけ設定できます。テーブルにクラスター化インデックスがある場合、そのテーブルはクラスター化インデックステーブルと呼ばれます。そうでない場合は、非クラスター化インデックステーブルと呼ばれます。
-   非クラスター化インデックスを作成すると、テーブル内のデータは順不同構造で格納されます。TiDBは各データ行に一意のROWIDを自動的に割り当てるため、非クラスター化インデックスのキー値を明示的に指定する必要はありません。クエリ実行時には、ROWIDを使用して対応する行が特定されます。データのクエリまたは挿入時には少なくとも2回のネットワークI/O操作が発生するため、クラスター化インデックスと比較してパフォーマンスが低下します。

テーブルデータが変更されると、データベースシステムはクラスター化インデックスと非クラスター化インデックスを自動的に維持します。

デフォルトでは、すべての主キーは非クラスター化インデックスとして作成されます。主キーをクラスター化インデックスまたは非クラスター化インデックスとして作成するには、次の 2 つの方法のいずれかを使用できます。

-   テーブルを作成する際に、ステートメント内でキーワード`CLUSTERED | NONCLUSTERED`を指定すると、システムは指定された方法でテーブルを作成します。構文は以下のとおりです。

```sql
CREATE TABLE `t` (`a` VARCHAR(255), `b` INT, PRIMARY KEY (`a`, `b`) CLUSTERED);
```

または

```sql
CREATE TABLE `t` (`a` VARCHAR(255) PRIMARY KEY CLUSTERED, `b` INT);
```

テーブルにクラスター化インデックスがあるかどうかを照会するには`SHOW INDEX FROM tbl-name`というステートメントを実行します。

-   クラスター化インデックス機能を制御するには、システム変数`tidb_enable_clustered_index`を設定します。サポートされている値は、 `ON` 、 `OFF` 、および`INT_ONLY` 。
    -   `ON` : すべてのタイプの主キーに対してクラスター化インデックス機能が有効になっていることを示します。非クラスター化インデックスの追加と削除がサポートされています。
    -   `OFF` : すべてのタイプの主キーに対して、クラスター化インデックス機能が無効になっていることを示します。非クラスター化インデックスの追加と削除はサポートされています。
    -   `INT_ONLY` : デフォルト値。変数が`INT_ONLY`に設定され、 `alter-primary-key`が`false`に設定されている場合、単一の整数列で構成される主キーは、デフォルトでクラスター化インデックスとして作成されます。この動作は、TiDB v5.0 およびそれ以前のバージョンと同様です。

`CREATE TABLE`ステートメントにキーワード`CLUSTERED | NONCLUSTERED`が含まれている場合、そのステートメントはシステム変数と構成項目の設定を上書きします。

ステートメントでキーワード`CLUSTERED | NONCLUSTERED`指定して、クラスター化インデックス機能を使用することをお勧めします。この方法により、TiDB は必要に応じてシステム内のクラスター化インデックスと非クラスター化インデックスのすべてのデータ型を同時に使用できるようになり、より柔軟に対応できます。

`tidb_enable_clustered_index = INT_ONLY`の使用は推奨されません。 `INT_ONLY`は、この機能の互換性を確保するために一時的に使用されており、将来的に廃止される予定です。

クラスター化インデックスの制限事項は以下のとおりです。

-   クラスター化インデックスと非クラスター化インデックス間の相互変換はサポートされていません。
-   クラスター化インデックスの削除はサポートされていません。
-   `ALTER TABLE`ステートメントを使用したクラスター化インデックスの追加、削除、および変更はサポートされていません。
-   クラスター化インデックスの再編成および再作成はサポートされていません。
-   インデックスの有効化または無効化はサポートされていないため、不可視インデックス機能はクラスター化インデックスには適用されません。
-   `UNIQUE KEY`をクラスター化インデックスとして作成することはサポートされていません。
-   TiDB Binlogとクラスター化インデックス機能を併用することはサポートされていません。TiDB Binlog を有効にすると、TiDB は単一の整数主キーのみをクラスター化インデックスとして作成することをサポートします。TiDB Binlog は、クラスター化インデックスを持つ既存のテーブルのデータ変更をダウンストリームにレプリケートしません。
-   クラスター化インデックス機能を属性`SHARD_ROW_ID_BITS`および`PRE_SPLIT_REGIONS`と併用することはサポートされていません。
-   クラスターを新しいバージョンにアップグレードした後、ロールバックした場合、ロールバック前にテーブルデータをエクスポートし、ロールバック後にデータをインポートすることで、新しく追加されたテーブルをダウングレードする必要があります。その他のテーブルは影響を受けません。

### 非同期コミット {#async-commit}

[ユーザー向けドキュメント](/system-variables.md#tidb_enable_async_commit-new-in-v50)、 [#8316](https://github.com/tikv/tikv/issues/8316)

データベースのクライアントは、データベースシステムがトランザクションのコミットを2段階（2PC）で同期的に完了するまで待機します。トランザクションは、第1段階のコミットが成功した後に結果をクライアントに返し、システムは第2段階のコミット操作をバックグラウンドで非同期的に実行して、トランザクションのコミットレイテンシーを短縮します。トランザクションの書き込みが1つのリージョンのみに関係する場合は、第2段階は省略され、トランザクションは1段階のコミットとなります。

非同期コミット機能を有効にした後、同じハードウェアと構成で、Sysbenchを64スレッドで更新インデックスをテストするように設定すると、平均レイテンシーが12.04msから7.01msに41.7%減少します。

非同期コミット機能が有効になっている場合、ネットワークインタラクションのレイテンシーを1回減らし、データ書き込みのパフォーマンスを向上させるために、データベースアプリケーション開発者は、トランザクションの一貫性を線形一貫性から[因果関係の一貫性](/transaction-overview.md#causal-consistency)の に下げることを検討することをお勧めします。因果一貫性を有効にするSQLステートメントは`START TRANSACTION WITH CAUSAL CONSISTENCY`です。

因果的一貫性を有効にした後、同じハードウェアと構成で、Sysbenchをoltp_write_onlyを64スレッドでテストするように設定すると、平均レイテンシーが11.86msから11.19msに5.6%減少しました。

トランザクションの一貫性が線形一貫性から因果一貫性に低下した後、アプリケーション内の複数のトランザクション間に相互依存性がない場合、トランザクションはグローバルに一貫した順序を持ちません。

**非同期コミット機能は、新しく作成されたv5.0クラスターではデフォルトで有効になっています。**

この機能は、以前のバージョンから v5.0 にアップグレードされたクラスターではデフォルトで無効になっています。 `set global tidb_enable_async_commit = ON;`および`set global tidb_enable_1pc = ON;`ステートメントを実行することで、この機能を有効にできます。

非同期コミット機能の制限事項は以下のとおりです。

-   直接的なダウングレードはサポートされていません。

### コプロセッサーキャッシュ機能をデフォルトで有効にする {#enable-the-coprocessor-cache-feature-by-default}

[ユーザー向けドキュメント](/tidb-configuration-file.md#tikv-clientcopr-cache-new-in-v400)、 [#18028](https://github.com/pingcap/tidb/issues/18028)

5.0 GAでは、コプロセッサーキャッシュ機能がデフォルトで有効になっています。この機能が有効になると、データ読み取りのレイテンシーを削減するために、TiDBはtikv-serverにプッシュダウンされた演算子の計算結果をtidb-serverにキャッシュします。

コプロセッサーキャッシュ機能を無効にするには、 `capacity-mb`の構成項目`tikv-client.copr-cache`を`0.0`に変更します。

### <code>delete from table where id &lt;? Limit ?</code>ステートメントの実行パフォーマンスを改善します。 {#improve-the-execution-performance-of-code-delete-from-table-where-id-x3c-limit-code-statement}

[#18028](https://github.com/pingcap/tidb/issues/18028)

`delete from table where id <? limit ?`ステートメントの p99 パフォーマンスは 4 倍向上しました。

### ロードベース分割戦略を最適化し、一部の小規模テーブルホットスポット読み取りシナリオでデータが分割できないというパフォーマンス問題を解決します。 {#optimize-load-base-split-strategy-to-solve-the-performance-problem-that-data-cannot-be-split-in-some-small-table-hotspot-read-scenarios}

[#18005](https://github.com/pingcap/tidb/issues/18005)

## 安定性を向上させる {#improve-stability}

### 不完全なスケジューリングによって引き起こされるパフォーマンスのジッター問題を最適化します。 {#optimize-the-performance-jitter-issue-caused-by-imperfect-scheduling}

[#18005](https://github.com/pingcap/tidb/issues/18005)

TiDBのスケジューリングプロセスは、I/O、ネットワーク、CPU、メモリなどのリソースを消費します。TiDBがスケジュールされたタスクを制御しない場合、リソースの優先実行により、QPS（1秒あたりの処理数）や遅延が発生し、パフォーマンスの変動が生じる可能性があります。

以下の最適化後、8時間の性能試験において、TPC-C tpmCの標準偏差は2%を超えない。

#### 不要なスケジューリングとパフォーマンスのジッターを軽減するために、新しいスケジューリング計算式を導入する。 {#introduce-new-scheduling-calculation-formulas-to-reduce-unnecessary-scheduling-and-performance-jitter}

ノード容量がシステムで設定された上限値に常に近い場合、または`store-limit`が大きすぎる場合、容量負荷のバランスを取るために、システムはリージョンを他のノードに頻繁に割り当てたり、リージョンを元のノードに戻したりします。スケジューリングはI/O、ネットワーク、CPU、メモリなどのリソースを消費し、パフォーマンスの変動を引き起こすため、このタイプのスケジューリングは不要です。

この問題を軽減するために、PD は新しいデフォルトのスケジュール計算式を導入しました。 `region-score-formula-version = v1`を設定することで、以前の計算式に戻すことができます。

#### デフォルトでクロステーブルリージョンマージ機能を有効にする {#enable-the-cross-table-region-merge-feature-by-default}

[ユーザー向けドキュメント](/pd-configuration-file.md#enable-cross-table-merge)

バージョン5.0より前は、TiDBはデフォルトでクロステーブルリージョンマージ機能を無効にしていました。バージョン5.0以降では、空のリージョンの数を減らし、ネットワーク、メモリ、CPUのオーバーヘッドを削減するために、この機能がデフォルトで有効になっています。この機能は`schedule.enable-cross-table-merge`構成項目を変更することで無効にできます。

#### バックグラウンドタスクとフォアグラウンドの読み書き間のI/Oリソースの競合のバランスを取るために、システムがデフォルトでデータ圧縮速度を自動的に調整できるようにします。 {#enable-the-system-to-automatically-adjust-the-data-compaction-speed-by-default-to-balance-the-contention-for-i-o-resources-between-background-tasks-and-foreground-reads-and-writes}

[ユーザー向けドキュメント](/tikv-configuration-file.md#rate-limiter-auto-tuned-new-in-v50)

バージョン5.0より前は、バックグラウンドタスクとフォアグラウンドの読み書きにおけるI/Oリソースの競合を緩和するため、データ圧縮速度をシステムが自動的に調整する機能はデフォルトで無効になっていました。バージョン5.0以降、TiDBはこの機能をデフォルトで有効にし、アルゴリズムを最適化することで、レイテンシーのジッターを大幅に低減します。

`rate-limiter-auto-tuned`設定項目を変更することで、この機能を無効にすることができます。

#### GCのCPUおよびI/Oリソース消費を削減するために、GCコンパクションフィルタ機能をデフォルトで有効にします。 {#enable-the-gc-compaction-filter-feature-by-default-to-reduce-gc-s-consumption-of-cpu-and-i-o-resources}

[ユーザー向けドキュメント](/garbage-collection-configuration.md#gc-in-compaction-filter)、 [#18009](https://github.com/pingcap/tidb/issues/18009)

TiDBがガベージコレクション（GC）とデータ圧縮を実行する際、パーティションはCPUとI/Oリソースを消費します。これらの2つのタスクの実行中は、データが重複している状態が発生します。

GC の CPU および I/O リソースの消費を削減するために、GC コンパクション フィルタ機能は、これら 2 つのタスクを 1 つに結合し、同じタスクで実行します。この機能はデフォルトで有効になっています。 `gc.enable-compaction-filter = false`を設定することで無効にできます。

#### TiFlashは、圧縮とデータソートにおけるI/Oリソースの使用を制限します（<strong>実験的機能</strong>）。 {#tiflash-limits-the-compression-and-data-sorting-s-use-of-i-o-resources-strong-experimental-feature-strong}

この機能は、バックグラウンドタスクとフォアグラウンドの読み書き処理の間で発生するI/Oリソースの競合を軽減します。

この機能はデフォルトでは無効になっています。 `bg_task_io_rate_limit`設定項目を変更することで、この機能を有効にできます。

#### 大規模クラスタにおけるスケジューリング制約のチェック性能と、異常リージョンの修復性能を向上させる。 {#improve-the-performance-of-checking-scheduling-constraints-and-the-performance-of-fixing-the-unhealthy-regions-in-a-large-cluster}

### パフォーマンスの変動を避けるため、実行計画はできる限り変更しないようにしてください。 {#ensure-that-the-execution-plans-are-unchanged-as-much-as-possible-to-avoid-performance-jitter}

[ユーザー向けドキュメント](/sql-plan-management.md)

#### SQLバインディングは、 <code>INSERT</code> 、 <code>REPLACE</code> 、 <code>UPDATE</code> 、 <code>DELETE</code>ステートメントをサポートします。 {#sql-binding-supports-the-code-insert-code-code-replace-code-code-update-code-code-delete-code-statements}

パフォーマンスの調整やデータベースの保守を行う際に、実行プランの不安定さが原因でシステムパフォーマンスが不安定になっていることが判明した場合、ご自身の判断または`EXPLAIN ANALYZE`によるテストに基づいて、手動で最適化されたSQL文を選択できます。最適化されたSQL文をアプリケーションコードで実行されるSQL文にバインドすることで、安定したパフォーマンスを確保できます。

SQL BINDING ステートメントを使用して SQL ステートメントを手動でバインドする場合、最適化された SQL ステートメントが元の SQL ステートメントと同じ構文であることを確認する必要があります。

`SHOW {GLOBAL | SESSION} BINDINGS`コマンドを実行すると、手動または自動でバインドされた実行プラン情報を表示できます。出力はバージョン 5.0 より前のバージョンと同じです。

#### 実行プランを自動的にキャプチャしてバインドします {#automatically-capture-and-bind-execution-plans}

TiDBをアップグレードする際、パフォーマンスの不安定性を回避するために、ベースラインキャプチャ機能を有効にして、システムが最新の実行プランを自動的にキャプチャしてバインドし、システムテーブルに保存するように設定できます。TiDBのアップグレード後、 `SHOW GLOBAL BINDING`コマンドを実行してバインドされた実行プランをエクスポートし、これらのプランを削除するかどうかを決定できます。

この機能はデフォルトでは無効になっています。サーバーを変更するか、グローバルシステム変数`tidb_capture_plan_baselines` `ON`に設定することで有効にできます。この機能が有効になると、システムは`bind-info-lease`ごと (デフォルト値は`3s` )、ステートメントサマリーから少なくとも 2 回出現する SQL ステートメントを取得し、これらの SQL ステートメントを自動的にキャプチャしてバインドします。

### TiFlashクエリの安定性を向上させる {#improve-stability-of-tiflash-queries}

TiFlash が失敗した場合にクエリを TiKV にフォールバックするように、システム変数[`tidb_allow_fallback_to_tikv`](/system-variables.md#tidb_allow_fallback_to_tikv-new-in-v50)を追加します。デフォルト値は`OFF`です。

### TiCDCの安定性を向上させ、過剰な増分データの複製によって引き起こされるメモリ不足の問題を軽減する。 {#improve-ticdc-stability-and-alleviate-the-oom-issue-caused-by-replicating-too-much-incremental-data}

[ユーザー向けドキュメント](/ticdc/ticdc-manage-changefeed.md#unified-sorter)、 [#1150](https://github.com/pingcap/tiflow/issues/1150)

TiCDC v4.0.9以前のバージョンでは、データ変更を過剰に複製するとメモリ不足（OOM）が発生する可能性があります。v5.0では、以下のシナリオで発生するOOMの問題を軽減するために、統合ソーター機能がデフォルトで有効になっています。

-   TiCDCにおけるデータ複製タスクが長時間一時停止され、その間に大量の増分データが蓄積され、複製する必要が生じる。
-   データ複製タスクは初期のタイムスタンプから開始されるため、大量の増分データを複製する必要が生じる。

Unified Sorterは、以前のバージョンの`memory` / `file`ソートエンジンオプションと統合されています。変更を手動で設定する必要はありません。

制限事項：

-   追加データ量に応じて、十分なディスク容量を確保する必要があります。128GB以上の空き容量を持つSSDの使用をお勧めします。

## 高可用性とディザスタリカバリ {#high-availability-and-disaster-recovery}

### リージョンメンバーシップ変更時のシステム可用性を向上させる {#improve-system-availability-during-region-membership-change}

[ユーザー向けドキュメント](/pd-configuration-file.md#enable-joint-consensus-new-in-v50)、 [#18079](https://github.com/pingcap/tidb/issues/18079) 、 [#7587](https://github.com/tikv/tikv/issues/7587) 、 [#2860](https://github.com/tikv/pd/issues/2860)

リージョンメンバーシップの変更処理では、「メンバーの追加」と「メンバーの削除」という2つの操作が2つのステップで実行されます。メンバーシップ変更処理の完了時にエラーが発生した場合、リージョンは利用できなくなり、フォアグラウンドアプリケーションのエラーが返されます。

導入されたRaft共同合意アルゴリズムは、リージョンメンバーシップ変更時のシステム可用性を向上させることができます。メンバーシップ変更時の「メンバーの追加」と「メンバーの削除」操作は1つの操作に統合され、すべてのメンバーに送信されます。変更処理中、リージョンは中間状態になります。変更されたメンバーのいずれかが故障した場合でも、システムは引き続き利用可能です。

この機能はデフォルトで有効になっています。 `pd-ctl config set enable-joint-consensus`コマンドを実行して`enable-joint-consensus`の値を`false`に設定することで無効にできます。

### メモリ管理モジュールを最適化して、システムOOMリスクを低減する {#optimize-the-memory-management-module-to-reduce-system-oom-risks}

集計関数のメモリ使用量を追跡します。この機能はデフォルトで有効になっています。集計関数を含む SQL ステートメントが実行されると、現在のクエリの合計メモリ使用量`mem-quota-query`で設定されたしきい値を超えた場合、システムは`oom-action`で定義された操作を自動的に実行します。

### ネットワーク分断時のシステム可用性を向上させる {#improve-the-system-availability-during-network-partition}

## データ移行 {#data-migration}

### S3/ AuroraからTiDBへデータを移行する {#migrate-data-from-s3-aurora-to-tidb}

TiDBのデータ移行ツールは、データ移行の中間段階としてAmazon S3（およびその他のS3互換ストレージサービス）を使用し、 AuroraスナップショットデータをTiDBに直接初期化することをサポートしており、Amazon S3/ AuroraからTiDBへのデータ移行に関するより多くの選択肢を提供します。

この機能を使用するには、以下のドキュメントを参照してください。

-   [データをAmazon S3クラウドストレージにエクスポートする](/dumpling-overview.md#export-data-to-amazon-s3-cloud-storage)、 [#8](https://github.com/pingcap/dumpling/issues/8)
-   [TiDB Lightningを使用してAmazon Aurora MySQLから移行する](/migrate-aurora-to-tidb.md)、 [#266](https://github.com/pingcap/tidb-lightning/issues/266)

### TiDB Cloudのデータインポートパフォーマンスを最適化する {#optimize-the-data-import-performance-of-tidb-cloud}

TiDB Lightningは、特にAWS T1.standard構成（または同等の構成）のTiDB Cloud向けにデータインポートのパフォーマンスを最適化します。テスト結果によると、 TiDB Lightningは1TBのTPC-CデータをTiDBにインポートする速度を40%向上させ、254 GiB/hから366 GiB/hに向上させます。

## データ共有と購読 {#data-sharing-and-subscription}

### TiCDCを使用してTiDBをKafka Connect（Confluent Platform）に統合する（<strong>実験的機能</strong>） {#integrate-tidb-to-kafka-connect-confluent-platform-using-ticdc-strong-experimental-feature-strong}

[ユーザー向けドキュメント](/ticdc/integrate-confluent-using-ticdc.md) [#660](https://github.com/pingcap/tiflow/issues/660)

TiDBデータを他のシステムにストリーミングするというビジネス要件をサポートするため、この機能を使用すると、TiDBデータをKafka、Hadoop、Oracleなどのシステムにストリーミングできます。

Confluentプラットフォームが提供するKafkaコネクタプロトコルは、コミュニティで広く利用されており、さまざまなプロトコルでリレーショナルデータベースと非リレーショナルデータベースの両方へのデータ転送をサポートしています。TiDBは、TiCDCをConfluentプラットフォームのKafka Connectに統合することで、TiDBデータを他の異種データベースやシステムにストリーミングする機能を拡張します。

## 診断 {#diagnostics}

[ユーザー向けドキュメント](/sql-statements/sql-statement-explain.md#explain)

SQLのパフォーマンス問題のトラブルシューティングでは、パフォーマンス問題の原因を特定するために詳細な診断情報が必要です。TiDB 5.0より前は、 `EXPLAIN`ステートメントで収集される情報は十分詳細ではありませんでした。問題の根本原因は、ログ情報、監視情報、あるいは推測に基づいてしか特定できず、非効率的でした。

TiDB v5.0では、パフォーマンスの問題をより効率的にトラブルシューティングできるよう、以下の改善が行われました。

-   `EXPLAIN ANALYZE`ステートメントを使用してすべての DML ステートメントを分析し、各演算子の実際のパフォーマンス プランと実行情報を表示する機能をサポートします。 [#18056](https://github.com/pingcap/tidb/issues/18056)
-   `EXPLAIN FOR CONNECTION`ステートメントを使用して、実行中のすべての SQL ステートメントのリアルタイム ステータスを確認できるようにしました。たとえば、このステートメントを使用して、各演算子の実行時間と処理された行数を確認できます。 [#18233](https://github.com/pingcap/tidb/issues/18233)
-   `EXPLAIN ANALYZE`ステートメントの出力に、オペレーターの実行に関する詳細情報（オペレーターが送信した RPC リクエストの数、ロック競合の解決にかかった時間、ネットワークレイテンシー、RocksDB でスキャンされた削除済みデータのボリューム、RocksDB キャッシュのヒット率など）を記載してください。 [#18663](https://github.com/pingcap/tidb/issues/18663)
-   SQL文の詳細な実行情報をスローログに自動的に記録する機能をサポートします。スローログの実行情報は、 `EXPLAIN ANALYZE`文の出力情報と一致しており、各演算子の消費時間、処理された行数、送信されたRPCリクエスト数などが含まれます。 [#15009](https://github.com/pingcap/tidb/issues/15009)

## 導入と保守 {#deployment-and-maintenance}

### クラスタ展開操作のロジックを最適化し、DBAが標準的なTiDB本番クラスタをより迅速に展開できるようにします。 {#optimize-the-logic-of-cluster-deployment-operations-to-help-dbas-deploy-a-set-of-standard-tidb-production-cluster-faster}

[ユーザー向けドキュメント](/production-deployment-using-tiup.md)

以前のTiDBバージョンでは、 TiUPを使用してTiDBクラスタをデプロイするDBAは、環境初期化が複雑で、チェックサム構成が過剰であり、クラスタトポロジーファイルの編集が困難であるという問題に直面していました。これらの問題はすべて、DBAのデプロイ効率の低下につながっていました。TiDB v5.0では、以下の項目により、 TiUPを使用したTiDBデプロイの効率がDBA向けに改善されています。

-   TiUP クラスタは、より包括的なワンクリック環境チェックを実行し、修復に関する推奨事項を提供する`check topo.yaml`コマンドをサポートしています。
-   TiUP クラスタは、環境チェック中に検出された環境問題を自動的に修復する`check topo.yaml --apply`コマンドをサポートしています。
-   TiUP クラスタ は、DBA が編集するためのクラスタ トポロジ テンプレート ファイルを取得し、グローバル ノード パラメータの変更をサポートする`template`コマンドをサポートしています。
-   TiUPは`remote_config`コマンドを使用して`edit-config`パラメータを編集し、リモートPrometheusを設定することをサポートしています。
-   TiUPは`external_alertmanagers`コマンドを使用して異なるAlertManagerを設定するために、 `edit-config`パラメーターの編集をサポートしています。
-   tiup-clusterの`edit-config`サブコマンドを使用してトポロジ ファイルを編集する場合、構成項目の値のデータ型を変更できます。

### アップグレードの安定性を向上させる {#improve-upgrade-stability}

TiUP v1.4.0より前は、 tiup-clusterを使用してTiDBクラスタをアップグレードする際に、クラスタのSQL応答が長時間ジッターし、PDオンラインローリングアップグレード中にクラスタのQPSが10秒から30秒の間でジッターしていました。

TiUP v1.4.0では、ロジックを調整し、以下の最適化を行いました。

-   PDノードのアップグレード中、 TiUPは再起動されたPDノードの状態を自動的にチェックし、状態が準備完了であることを確認した後、次のPDノードのアップグレードに進みます。
-   TiUPはPDの役割を自動的に識別し、まずフォロワーの役割を持つPDノードをアップグレードし、最後にPD Leaderノードをアップグレードします。

### アップグレード時間を最適化する {#optimize-the-upgrade-time}

TiUP v1.4.0より前は、DBAがtiup-clusterを使用してTiDBクラスタをアップグレードする場合、ノード数が多いクラスタでは、アップグレードにかかる合計時間が長く、一部のユーザーのアップグレード時間枠の要件を満たせないことがありました。

バージョン1.4.0以降、 TiUPは以下の項目を最適化します。

-   `tiup cluster upgrade --offline`サブコマンドを使用した高速オフラインアップグレードをサポートします。
-   デフォルトで、アップグレード中にローリングアップグレードを使用するユーザーのリージョンLeaderの再配置を高速化することで、TiKVのローリングアップグレードにかかる時間を短縮します。
-   ローリングアップグレードを実行する前に、 `check`サブコマンドを使用してリージョンモニターの状態を確認します。アップグレード前にクラスターが正常な状態であることを確認することで、アップグレードの失敗の可能性を低減します。

### ブレークポイント機能をサポートする {#support-the-breakpoint-feature}

TiUP v1.4.0より前のバージョンでは、DBAがtiup-clusterを使用してTiDBクラスタをアップグレードする際に、コマンドの実行が中断された場合、すべてのアップグレード操作を最初からやり直す必要がありました。

TiUP v1.4.0 では、 tiup-cluster `replay`サブコマンドを使用して、ブレークポイントから失敗した操作を再試行することがサポートされており、アップグレードの中断後にすべての操作を再実行する必要がなくなります。

### 保守および運用機能を強化する {#enhance-the-functionalities-of-maintenance-and-operations}

TiUP v1.4.0では、TiDBクラスタの運用と保守に関する機能がさらに強化されています。

-   TiDBおよびDMクラスタのダウンタイム中のアップグレードまたはパッチ適用操作をサポートし、より多くの利用シナリオに対応できるようにします。
-   tiup-clusterの`--version`サブコマンドに`display`パラメータを追加して、クラスタバージョンを取得します。
-   スケールアウト対象のノードにPrometheusのみが含まれている場合、Prometheusノードの不在によるスケールアウトの失敗を回避するため、監視設定の更新操作は実行されません。
-   TiUPコマンドの入力結果が正しくない場合に、エラーメッセージにユーザー入力を追加することで、問題の原因をより迅速に特定できるようにします。

## テレメトリー {#telemetry}

TiDBは、データテーブルの数、クエリの数、新機能が有効になっているかどうかなど、クラスタの使用状況に関するメトリクスをテレメトリに追加します。

詳細およびこの動作を無効にする方法については、[テレメトリー](/telemetry.md)を参照してください。
