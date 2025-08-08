---
title: What's New in TiDB 5.0
summary: TiDB 5.0では、MPPアーキテクチャ、クラスター化インデックス、非同期コミット、安定性の向上が導入されています。また、互換性の変更、構成パラメータ、新機能も強化されています。さらに、パフォーマンス、高可用性、ディザスタリカバリ、データ移行、診断、デプロイメント、メンテナンスが最適化されています。クラスターの使用状況メトリクス用のテレメトリが追加されました。
---

# TiDB 5.0 の新機能 {#what-s-new-in-tidb-5-0}

発売日：2021年4月7日

TiDB バージョン: 5.0.0

バージョン 5.0 では、PingCAP は、企業が TiDB に基づくアプリケーションを迅速に構築できるようにし、データベースのパフォーマンス、パフォーマンスのジッター、セキュリティ、高可用性、障害復旧、SQL パフォーマンスのトラブルシューティングなどに関する懸念から解放することに重点を置いています。

v5.0 の主な新機能または改善点は次のとおりです。

-   TiFlashノードを通じて大規模並列処理（MPP）アーキテクチャを導入し、大規模な結合クエリの実行負荷をTiFlashノード間で分散させます。MPPモードを有効にすると、TiDBはコストに基づいてMPPフレームワークを使用して計算を実行するかどうかを判断します。MPPモードでは、計算中に結合キーが`Exchange`操作を通じて再分配されるため、各TiFlashノードへの計算負荷が分散され、計算速度が向上します。ベンチマークによると、同じクラスターリソースの場合、TiDB 5.0 MPPはGreenplum 6.15.0やApache Spark 3.1.1と比較して2～3倍の高速化を示し、一部のクエリでは8倍のパフォーマンス向上が見られました。
-   クラスター化インデックス機能を導入すると、データベースのパフォーマンスが向上します。例えば、TPC-C tpmCテストでは、クラスター化インデックスを有効にしたTiDBのパフォーマンスが39%向上しました。
-   非同期コミット機能を有効にすると、書き込みレイテンシーが短縮されます。例えば、64スレッドのSysbenchテストでは、非同期コミットを有効にすると、インデックス更新の平均レイテンシーが12.04ミリ秒から7.01ミリ秒へと41.7%短縮されます。
-   ジッターを低減します。これは、オプティマイザーの安定性を向上させ、システムタスクによるI/O、ネットワーク、CPU、メモリリソースの使用を制限することで実現されます。例えば、8時間のパフォーマンステストでは、TPC-C tpmCの標準偏差は2%を超えません。
-   スケジュールを改善し、実行プランを可能な限り安定させることで、システムの安定性を高めます。
-   リージョンメンバーシップの変更中にシステムの可用性を確保するRaftジョイント コンセンサス アルゴリズムを導入します。
-   `EXPLAIN`機能と非表示のインデックスを最適化し、データベース管理者 (DBA) が SQL ステートメントをより効率的にデバッグできるようにします。
-   エンタープライズデータの信頼性を保証します。TiDBからAmazon S3storageやGoogle Cloud GCSにデータをバックアップしたり、これらのクラウドstorageプラットフォームからデータを復元したりできます。
-   Amazon S3storageまたはTiDB/MySQLとの間でのデータインポート/エクスポートのパフォーマンスが向上し、企業がクラウド上でアプリケーションを迅速に構築できるようになります。例えば、TPC-Cテストでは、1TiBのデータのインポートパフォーマンスが254GiB/時間から366GiB/時間へと40%向上しました。

## 互換性の変更 {#compatibility-changes}

### システム変数 {#system-variables}

-   複数の演算子の同時実行を制御するには、システム変数[`tidb_executor_concurrency`](/system-variables.md#tidb_executor_concurrency-new-in-v50)追加します。以前の`tidb_*_concurrency`設定（例: `tidb_projection_concurrency` ）は引き続き有効ですが、使用時に警告が表示されます。

-   ASCII文字セットの書き込み時にASCII検証チェックをスキップするかどうかを指定するには、システム変数[`tidb_skip_ascii_check`](/system-variables.md#tidb_skip_ascii_check-new-in-v50)追加します。デフォルト値は`OFF`です。

-   システム変数[`tidb_enable_strict_double_type_check`](/system-variables.md#tidb_enable_strict_double_type_check-new-in-v50)追加して、テーブルスキーマで`double(N)`ような構文を定義できるかどうかを決定します。デフォルト値は`OFF`です。

-   デフォルト値の[`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size)を`20000`から`0`に変更します。これにより、バージョン`LOAD` / `INSERT INTO SELECT ...`ではバッチDML文がデフォルトで使用されなくなります。代わりに、厳密なACIDセマンティクスに準拠するために、大規模なトランザクションが使用されます。

    > **注記：**
    >
    > 変数のスコープはセッションからグローバルに変更され、デフォルト値は`20000`から`0`に変更されます。アプリケーションが元のデフォルト値に依存している場合は、アップグレード後に`set global`ステートメントを使用して変数を元の値に変更する必要があります。

-   一時テーブルの構文の互換性は、システム変数[`tidb_enable_noop_functions`](/system-variables.md#tidb_enable_noop_functions-new-in-v40)使用して制御します。この変数の値が`OFF`場合、構文`CREATE TEMPORARY TABLE`エラーを返します。

-   ガベージコレクション関連のパラメータを直接制御するには、次のシステム変数を追加します。
    -   [`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-new-in-v50)
    -   [`tidb_gc_enable`](/system-variables.md#tidb_gc_enable-new-in-v50)
    -   [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)
    -   [`tidb_gc_run_interval`](/system-variables.md#tidb_gc_run_interval-new-in-v50)
    -   [`tidb_gc_scan_lock_mode`](/system-variables.md#tidb_gc_scan_lock_mode-new-in-v50)

-   デフォルト値の[`enable-joint-consensus`](/pd-configuration-file.md#enable-joint-consensus-new-in-v50)を`false`から`true`に変更します。これにより、共同コンセンサス機能がデフォルトで有効になります。

-   `tidb_enable_amend_pessimistic_txn`の値を`0`または`1`から`ON`または`OFF`に変更します。

-   デフォルト値[`tidb_enable_clustered_index`](/system-variables.md#tidb_enable_clustered_index-new-in-v50)を`OFF`から`INT_ONLY`に変更し、次の新しい意味を追加します。
    -   `ON` : クラスター化インデックスが有効です。非クラスター化インデックスの追加または削除がサポートされています。

    -   `OFF` : クラスター化インデックスは無効です。非クラスター化インデックスの追加または削除はサポートされています。

    -   `INT_ONLY` : デフォルト値。動作はv5.0以前と同じです`alter-primary-key = false`と併用することで、INT型に対してクラスター化インデックスを有効にするかどうかを制御できます。
    > **注記：**
    >
    > 5.0 GA の`INT_ONLY`の値は`tidb_enable_clustered_index`で、5.0 RC の`OFF`値と同じ意味になります。7 に設定されている`OFF` RC クラスターから 5.0 GA にアップグレードすると、 `INT_ONLY`と表示されます。

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

-   TiDB の設定項目[`index-limit`](/tidb-configuration-file.md#index-limit-new-in-v50)追加します。デフォルト値は`64`で、範囲は`[64,512]`です。MySQL テーブルは最大 64 個のインデックスをサポートします。この値がデフォルト設定を超え、テーブルに 64 個を超えるインデックスが作成された場合、テーブルスキーマを MySQL に再インポートするとエラーが報告されます。
-   TiDBにMySQLのENUM/SETの長さ（ENUMの長さ &lt; 255）との互換性と一貫性を持たせるために、設定項目を[`enable-enum-length-limit`](/tidb-configuration-file.md#enable-enum-length-limit-new-in-v50)追加します。デフォルト値は`true`です。
-   `pessimistic-txn.enable`構成項目を[`tidb_txn_mode`](/system-variables.md#tidb_txn_mode)環境変数に置き換えます。
-   `performance.max-memory`構成項目を[`performance.server-memory-quota`](/tidb-configuration-file.md#server-memory-quota-new-in-v409)に置き換える
-   設定項目`tikv-client.copr-cache.enable` [`tikv-client.copr-cache.capacity-mb`](/tidb-configuration-file.md#capacity-mb)に置き換えます。項目の値が`0.0`の場合、この機能は無効になります。項目の値が`0.0`より大きい場合、この機能は有効になります。デフォルト値は`1000.0`です。
-   `rocksdb.auto-tuned`構成項目を[`rocksdb.rate-limiter-auto-tuned`](/tikv-configuration-file.md#rate-limiter-auto-tuned-new-in-v50)に置き換えます。
-   設定項目`raftstore.sync-log`削除します。デフォルトでは、書き込まれたデータは強制的にディスクに書き込まれます。v5.0より前は、 `raftstore.sync-log`明示的に無効にできました。v5.0以降では、設定値は強制的に`true`に設定されます。
-   `gc.enable-compaction-filter`構成項目のデフォルト値を`false`から`true`に変更します。
-   `enable-cross-table-merge`構成項目のデフォルト値を`false`から`true`に変更します。
-   [`rate-limiter-auto-tuned`](/tikv-configuration-file.md#rate-limiter-auto-tuned-new-in-v50)構成項目のデフォルト値を`false`から`true`に変更します。

### その他 {#others}

-   アップグレード前に、TiDB設定[`feedback-probability`](https://docs.pingcap.com/tidb/v5.0/tidb-configuration-file#feedback-probability)の値を確認してください。値が0でない場合、アップグレード後に「回復可能なゴルーチンでpanic」エラーが発生しますが、このエラーはアップグレードには影響しません。
-   データの正確性の問題を回避するために、列タイプの変更中に`VARCHAR`タイプと`CHAR`タイプ間の変換を禁止します。

## 新機能 {#new-features}

### SQL {#sql}

#### List パーティショニング（<strong>Experimental</strong>） {#list-partitioning-strong-experimental-strong}

[ユーザードキュメント](/partitioned-table.md#list-partitioning)

リスト パーティション機能を使用すると、大量のデータを含むテーブルを効率的にクエリおよび管理できます。

この機能を有効にすると、パーティションとパーティション間のデータの分散方法が`PARTITION BY LIST(expr) PARTITION part_name VALUES IN (...)`の式に従って定義されます。パーティションテーブルのデータセットは、最大1024個の異なる整数値をサポートします。値は`PARTITION ... VALUES IN (...)`の句を使用して定義できます。

リストのパーティション分割を有効にするには、セッション変数[`tidb_enable_list_partition`](/system-variables.md#tidb_enable_list_partition-new-in-v50)を`ON`に設定します。

#### List COLUMNS パーティショニング（<strong>Experimental</strong>） {#list-columns-partitioning-strong-experimental-strong}

[ユーザードキュメント](/partitioned-table.md#list-columns-partitioning)

List COLUMNS パーティショニングは、 `DATETIME` `DATE`型の列もパーティション列として使用できます。

List COLUMNS パーティショニングを有効にするには、セッション変数[`tidb_enable_list_partition`](/system-variables.md#tidb_enable_list_partition-new-in-v50)を`ON`に設定します。

#### 目に見えないインデックス {#invisible-indexes}

[ユーザードキュメント](/sql-statements/sql-statement-alter-index.md) [＃9246](https://github.com/pingcap/tidb/issues/9246)

パフォーマンスをチューニングしたり、最適なインデックスを選択したりする際に、SQL文を使用してインデックスを`Visible`または`Invisible`に設定できます。この設定により、 `DROP INDEX`や`ADD INDEX`といったリソースを消費する操作の実行を回避できます。

インデックスの可視性を変更するには、 `ALTER INDEX`文を使用します。変更後、オプティマイザはインデックスの可視性に基づいて、このインデックスをインデックスリストに追加するかどうかを決定します。

#### <code>EXCEPT</code>演算子と<code>INTERSECT</code>演算子 {#code-except-code-and-code-intersect-code-operators}

[ユーザードキュメント](/functions-and-operators/set-operators.md) [＃18031](https://github.com/pingcap/tidb/issues/18031)

`INTERSECT`演算子は集合演算子であり、2つ以上のクエリの結果セットの積集合を返します。ある意味では、 `Inner Join`演算子の代替として機能します。

`EXCEPT`演算子はセット演算子であり、2 つのクエリの結果セットを結合し、最初のクエリ結果にはあるが 2 番目のクエリ結果にはない要素を返します。

### トランザクション {#transaction}

[＃18005](https://github.com/pingcap/tidb/issues/18005)

悲観的トランザクション モードでは、トランザクションに関係するテーブルに同時 DDL 操作または`SCHEMA VERSION`変更が含まれている場合、システムはトランザクションの`SCHEMA VERSION`最新のものに自動的に更新して、トランザクションのコミットが確実に成功するようにし、トランザクションが DDL 操作または`SCHEMA VERSION`変更によって中断されたときにクライアントが`Information schema is changed`エラーを受け取ることを回避します。

この機能はデフォルトで無効になっています。この機能を有効にするには、 `tidb_enable_amend_pessimistic_txn`システム変数の値を変更してください。この機能はv4.0.7で導入され、v5.0で以下の問題が修正されています。

-   TiDB Binlogが`Add Column`操作を実行するときに発生する互換性の問題
-   この機能をユニークインデックスと併用した場合に発生するデータの不整合の問題
-   追加されたインデックスとこの機能を併用すると発生するデータの不整合の問題

現在、この機能には次のような非互換性の問題が残っています。

-   同時トランザクションがある場合、トランザクションのセマンティクスが変わる可能性があります
-   この機能を TiDB Binlogと併用した場合に発生する既知の互換性の問題
-   `Change Column`との互換性がない

### 文字セットと照合順序 {#character-set-and-collation}

-   `utf8mb4_unicode_ci`と`utf8_unicode_ci` [＃17596](https://github.com/pingcap/tidb/issues/17596)をサポートします[ユーザードキュメント](/character-set-and-collation.md#new-framework-for-collations)
-   照合順序の大文字と小文字を区別しない比較ソートをサポートする

### Security {#security}

[ユーザードキュメント](/log-redaction.md) [＃18566](https://github.com/pingcap/tidb/issues/18566)

セキュリティコンプライアンス要件（*一般データ保護規則*（GDPR）など）を満たすために、システムは出力エラーメッセージとログ内の機密情報（IDやクレジットカード番号など）の機密性を低減することをサポートしており、機密情報の漏洩を回避できます。

TiDBは出力ログ情報の感度を下げる機能をサポートしています。この機能を有効にするには、以下のスイッチを使用します。

-   グローバル変数[`tidb_redact_log`](/system-variables.md#tidb_redact_log) 。デフォルト値は`0`で、これは感度低下が無効であることを意味します。tidb-server ログの感度低下を有効にするには、変数値を`1`に設定してください。
-   設定項目`security.redact-info-log` 。デフォルト値は`false`で、これは感度低下が無効であることを意味します。tikv-server ログの感度低下を有効にするには、変数値を`true`に設定してください。
-   設定項目`security.redact-info-log` 。デフォルト値は`false`で、これは感度低下が無効であることを意味します。pd-server ログの感度低下を有効にするには、変数値を`true`に設定してください。
-   tiflash-server の設定項目`security.redact_info_log`と tiflash-learner の設定項目`security.redact-info-log` 。これらのデフォルト値はどちらも`false` 、これは感度低下が無効であることを意味します。tiflash-server と tiflash-learner のログの感度低下を有効にするには、両方の変数の値を`true`に設定してください。

この機能はバージョン5.0で導入されました。この機能を使用するには、システム変数と上記のすべての設定項目を有効にしてください。

## パフォーマンスの最適化 {#performance-optimization}

### MPPアーキテクチャ {#mpp-architecture}

[ユーザードキュメント](/tiflash/use-tiflash-mpp-mode.md)

TiDBはTiFlashノードを通じてMPPアーキテクチャを導入します。このアーキテクチャにより、複数のTiFlashノードが大規模な結合クエリの実行ワークロードを共有できるようになります。

MPPモードがオンの場合、TiDBは計算コストに基づいて、クエリをMPPエンジンに送信して計算を行うかどうかを判断します。MPPモードでは、TiDBはデータ計算中に結合キーを再分配することで、実行中の各TiFlashノードにテーブル結合の計算を分散し（ `Exchange`演算）、計算を高速化します。さらに、 TiFlashが既にサポートしている集計計算機能と組み合わせることで、TiDBはクエリの計算をTiFlash MPPクラスターにプッシュダウンできます。この分散環境により、実行プロセス全体が高速化され、分析クエリの速度が大幅に向上します。

TPC-H 100ベンチマークテストにおいて、 TiFlash MPPは従来の分析データベースの分析エンジンやHadoop上のSQLと比べて、大幅な処理速度を実現しました。このアーキテクチャにより、最新のトランザクションデータに対して大規模な分析クエリを直接実行でき、従来のオフライン分析ソリューションよりも高いパフォーマンスを実現します。ベンチマークによると、同じクラスターリソースの場合、TiDB 5.0 MPPはGreenplum 6.15.0やApache Spark 3.1.1と比較して2～3倍の高速化を示し、一部のクエリでは8倍のパフォーマンス向上が見られました。

現在、MPP モードでサポートされていない主な機能は次のとおりです (詳細は[TiFlashを使用する](/tiflash/use-tiflash-mpp-mode.md)を参照)。

-   テーブルパーティション
-   ウィンドウ関数
-   照合
-   いくつかの組み込み関数
-   TiKVからデータを読み取る
-   OOMスピル
-   連合
-   完全外部結合

### クラスター化インデックス {#clustered-index}

[ユーザードキュメント](/clustered-indexes.md) [＃4841](https://github.com/pingcap/tidb/issues/4841)

テーブル構造を設計したり、データベースの動作を分析したりする際に、主キーを持つ一部の列が頻繁にグループ化され、並べ替えられ、これらの列に対するクエリによって特定の範囲のデータや異なる値を持つ少量のデータが返されることが多く、対応するデータによって読み取りまたは書き込みのホットスポットの問題が発生しない場合は、クラスター化インデックス機能を使用することをお勧めします。

クラスター化インデックスは、テーブルのデータに関連付けられたstorage構造です。一部のデータベース管理システムでは、クラスター化インデックステーブルを*インデックス構成テーブル（Index Organized Table）*と呼びます。クラスター化インデックスを作成する際、テーブルの1つ以上の列をインデックスのキーとして指定できます。TiDBはこれらのキーを特定の構造に格納することで、キーに関連付けられた行を迅速かつ効率的に見つけることができ、データのクエリと書き込みのパフォーマンスが向上します。

クラスター化インデックス機能を有効にすると、次の場合に TiDB のパフォーマンスが大幅に向上します (たとえば、TPC-C tpmC テストでは、クラスター化インデックスを有効にした TiDB のパフォーマンスが 39% 向上します)。

-   データが挿入されると、クラスター化インデックスにより、ネットワークからのインデックス データの書き込みが 1 回削減されます。
-   同等の条件を持つクエリに主キーのみが関係する場合、クラスター化インデックスにより、ネットワークからのインデックス データの読み取りが 1 回削減されます。
-   範囲条件を持つクエリに主キーのみが関係する場合、クラスター化インデックスにより、ネットワークからのインデックス データの複数回の読み取りが削減されます。
-   同等条件または範囲条件を持つクエリに主キー プレフィックスが含まれる場合、クラスター化インデックスによって、ネットワークからのインデックス データの複数回の読み取りが削減されます。

各テーブルでは、データの並べ替えと保存にクラスター化インデックスまたは非クラスター化インデックスを使用できます。これら2つのstorage構造の違いは次のとおりです。

-   クラスター化インデックスを作成する際、テーブル内の1つ以上の列をインデックスのキー値として指定できます。クラスター化インデックスは、キー値に基づいてテーブルのデータを並べ替えて格納します。各テーブルには、クラスター化インデックスを1つだけ設定できます。テーブルにクラスター化インデックスが含まれている場合、そのテーブルはクラスター化インデックステーブルと呼ばれます。クラスター化インデックスが含まれていない場合は、非クラスター化インデックステーブルと呼ばれます。
-   非クラスター化インデックスを作成すると、テーブル内のデータは順序付けされていない構造で格納されます。TiDBは各データ行に一意のROWIDを自動的に割り当てるため、非クラスター化インデックスのキー値を明示的に指定する必要はありません。クエリ実行時には、ROWIDを使用して対応する行が検索されます。データのクエリまたは挿入時には少なくとも2回のネットワークI/O操作が発生するため、クラスター化インデックスと比較してパフォーマンスが低下します。

テーブル データが変更されると、データベース システムはクラスター化インデックスと非クラスター化インデックスを自動的に維持します。

すべての主キーは、デフォルトで非クラスター化インデックスとして作成されます。主キーをクラスター化インデックスまたは非クラスター化インデックスとして作成するには、次の2つの方法があります。

-   テーブルを作成する際に、ステートメントにキーワード`CLUSTERED | NONCLUSTERED`指定すると、システムは指定された方法でテーブルを作成します。構文は次のとおりです。

```sql
CREATE TABLE `t` (`a` VARCHAR(255), `b` INT, PRIMARY KEY (`a`, `b`) CLUSTERED);
```

または

```sql
CREATE TABLE `t` (`a` VARCHAR(255) PRIMARY KEY CLUSTERED, `b` INT);
```

ステートメント`SHOW INDEX FROM tbl-name`を実行すると、テーブルにクラスター化インデックスがあるかどうかを照会できます。

-   クラスター化インデックス機能を制御するには、システム変数`tidb_enable_clustered_index`を設定します。サポートされる値は`ON` 、 `OFF` 、 `INT_ONLY`です。
    -   `ON` : すべての種類の主キーに対してクラスター化インデックス機能が有効になっていることを示します。非クラスター化インデックスの追加と削除はサポートされています。
    -   `OFF` : すべての種類の主キーに対してクラスター化インデックス機能が無効であることを示します。非クラスター化インデックスの追加と削除はサポートされています。
    -   `INT_ONLY` : デフォルト値。変数を`INT_ONLY`に設定し、 `alter-primary-key` `false`に設定すると、単一の整数列で構成される主キーはデフォルトでクラスター化インデックスとして作成されます。この動作は、TiDB v5.0以前のバージョンと同じです。

`CREATE TABLE`ステートメントにキーワード`CLUSTERED | NONCLUSTERED`含まれている場合、そのステートメントはシステム変数と構成項目の構成をオーバーライドします。

ステートメントでキーワード`CLUSTERED | NONCLUSTERED`指定して、クラスター化インデックス機能を使用することをお勧めします。これにより、TiDB はシステム内のクラスター化インデックスと非クラスター化インデックスのすべてのデータ型を必要に応じて同時に使用できるため、より柔軟になります。

`INT_ONLY` 、この機能の互換性を保つために一時的に使用されているものであり、将来的には廃止される予定であるため、 `tidb_enable_clustered_index = INT_ONLY`使用はお勧めしません。

クラスター化インデックスの制限は次のとおりです。

-   クラスター化インデックスと非クラスター化インデックス間の相互変換はサポートされていません。
-   クラスター化インデックスの削除はサポートされていません。
-   `ALTER TABLE`ステートメントを使用したクラスター化インデックスの追加、削除、および変更はサポートされていません。
-   クラスター化インデックスの再構成と再作成はサポートされていません。
-   インデックスの有効化または無効化はサポートされていません。つまり、非表示のインデックス機能はクラスター化インデックスでは有効ではありません。
-   クラスター化インデックスとして`UNIQUE KEY`作成することはサポートされていません。
-   クラスター化インデックス機能とTiDB Binlogの併用はサポートされていません。TiDB Binlogを有効にすると、TiDBはクラスター化インデックスとして単一の整数主キーの作成のみをサポートします。TiDB Binlogは、クラスター化インデックスを持つ既存のテーブルのデータ変更を下流に複製しません。
-   クラスター化インデックス機能を属性`SHARD_ROW_ID_BITS`および`PRE_SPLIT_REGIONS`と一緒に使用することはサポートされていません。
-   クラスターを新しいバージョンにアップグレードしてからロールバックする場合は、ロールバック前にテーブルデータをエクスポートし、ロールバック後にデータをインポートすることで、新しく追加されたテーブルをダウングレードする必要があります。他のテーブルには影響しません。

### 非同期コミット {#async-commit}

[ユーザードキュメント](/system-variables.md#tidb_enable_async_commit-new-in-v50) [＃8316](https://github.com/tikv/tikv/issues/8316)

データベースクライアントは、データベースシステムが2フェーズ（2PC）で同期的にトランザクションコミットを完了するまで待機します。トランザクションは、第1フェーズのコミットが成功すると結果をクライアントに返し、システムは第2フェーズのコミット操作をバックグラウンドで非同期的に実行することで、トランザクションコミットのレイテンシーを短縮します。トランザクション書き込みが1つのリージョンのみに関係する場合、第2フェーズは直接省略され、トランザクションは1フェーズコミットになります。

非同期コミット機能を有効にした後、同じハードウェアと構成で、Sysbench を 64 スレッドで更新インデックスをテストするように設定すると、平均レイテンシーは12.04 ミリ秒から 7.01 ミリ秒に 41.7% 減少します。

非同期コミット機能を有効にすると、ネットワークインタラクションのレイテンシーを削減し、データ書き込みのパフォーマンスを向上させるために、データベースアプリケーション開発者は、トランザクションの一貫性を線形一貫性から[因果一貫性](/transaction-overview.md#causal-consistency)に下げることを検討することをお勧めします。因果的一貫性を有効にするSQL文は`START TRANSACTION WITH CAUSAL CONSISTENCY`です。

因果一貫性を有効にした後、同じハードウェアと構成で、Sysbench を 64 スレッドで oltp_write_only をテストするように設定すると、平均レイテンシーは11.86 ミリ秒から 11.19 ミリ秒に 5.6% 減少しました。

トランザクションの一貫性が線形一貫性から因果一貫性に低下した後、アプリケーション内の複数のトランザクション間に相互依存性がない場合、トランザクションはグローバルに一貫した順序を持ちません。

**新しく作成された v5.0 クラスターでは、非同期コミット機能がデフォルトで有効になっています。**

この機能は、以前のバージョンからv5.0にアップグレードされたクラスターではデフォルトで無効になっています。この機能を有効にするには、 `set global tidb_enable_async_commit = ON;`と`set global tidb_enable_1pc = ON;`ステートメントを実行します。

非同期コミット機能の制限は次のとおりです。

-   直接のダウングレードはサポートされていません。

### コプロセッサーキャッシュ機能をデフォルトで有効にする {#enable-the-coprocessor-cache-feature-by-default}

[ユーザードキュメント](/tidb-configuration-file.md#tikv-clientcopr-cache-new-in-v400) [＃18028](https://github.com/pingcap/tidb/issues/18028)

5.0 GAでは、コプロセッサーキャッシュ機能がデフォルトで有効になっています。この機能を有効にすると、データ読み取りのレイテンシーを削減するために、TiDBはtikv-serverにプッシュダウンされた演算子の計算結果をtidb-serverにキャッシュします。

コプロセッサーキャッシュ機能を無効にするには、 `tikv-client.copr-cache` ～ `0.0`の`capacity-mb`構成項目を変更します。

### <code>delete from table where id &lt;? Limit ?</code>ステートメントの実行パフォーマンスを向上 {#improve-the-execution-performance-of-code-delete-from-table-where-id-x3c-limit-code-statement}

[＃18028](https://github.com/pingcap/tidb/issues/18028)

`delete from table where id <? limit ?`文目のp99パフォーマンスが4倍向上します。

### ロードベースの分割戦略を最適化して、一部の小さなテーブルのホットスポット読み取りシナリオでデータを分割できないというパフォーマンスの問題を解決します。 {#optimize-load-base-split-strategy-to-solve-the-performance-problem-that-data-cannot-be-split-in-some-small-table-hotspot-read-scenarios}

[＃18005](https://github.com/pingcap/tidb/issues/18005)

## 安定性を向上 {#improve-stability}

### 不完全なスケジューリングによって発生するパフォーマンスジッターの問題を最適化します {#optimize-the-performance-jitter-issue-caused-by-imperfect-scheduling}

[＃18005](https://github.com/pingcap/tidb/issues/18005)

TiDBのスケジューリングプロセスは、I/O、ネットワーク、CPU、メモリなどのリソースを占有します。TiDBがスケジュールされたタスクを制御しない場合、リソースのプリエンプションによりQPSと遅延が発生し、パフォーマンスのジッタが発生する可能性があります。

以下の最適化を行った後、8 時間のパフォーマンス テストでは、TPC-C tpmC の標準偏差は 2% を超えません。

#### 不要なスケジューリングとパフォーマンスのジッターを削減するための新しいスケジューリング計算式を導入します。 {#introduce-new-scheduling-calculation-formulas-to-reduce-unnecessary-scheduling-and-performance-jitter}

ノードの容量が常にシステムで設定されたウォーターラインに近い場合、または`store-limit`が大きすぎる場合、容量負荷のバランスをとるために、システムは頻繁にリージョンを他のノードにスケジュールしたり、リージョンを元のノードに戻したりします。スケジューリングはI/O、ネットワーク、CPU、メモリなどのリソースを消費し、パフォーマンスのジッタを引き起こすため、このようなスケジューリングは必要ありません。

この問題を軽減するために、PD では新しいデフォルトのスケジュール計算式を導入しました。1 `region-score-formula-version = v1`設定することで、古い計算式に戻すことができます。

#### デフォルトでクロステーブルリージョン結合機能を有効にする {#enable-the-cross-table-region-merge-feature-by-default}

[ユーザードキュメント](/pd-configuration-file.md#enable-cross-table-merge)

v5.0より前のTiDBでは、テーブルリージョンのリージョンマージ機能はデフォルトで無効になっていました。v5.0以降では、空のリージョン数を削減し、ネットワーク、メモリ、CPUのオーバーヘッドを削減するため、この機能はデフォルトで有効になっています。この機能を無効にするには、 `schedule.enable-cross-table-merge`設定項目を変更します。

#### バックグラウンドタスクとフォアグラウンドの読み取りおよび書き込み間のI/Oリソースの競合のバランスをとるために、システムがデフォルトでデータ圧縮速度を自動的に調整できるようにします。 {#enable-the-system-to-automatically-adjust-the-data-compaction-speed-by-default-to-balance-the-contention-for-i-o-resources-between-background-tasks-and-foreground-reads-and-writes}

[ユーザードキュメント](/tikv-configuration-file.md#rate-limiter-auto-tuned-new-in-v50)

v5.0より前のバージョンでは、バックグラウンドタスクとフォアグラウンドの読み取り・書き込み間のI/Oリソースの競合をバランスさせるため、システムがデータ圧縮速度を自動調整する機能はデフォルトで無効になっていました。v5.0以降、TiDBはこの機能をデフォルトで有効にし、アルゴリズムを最適化することでレイテンシージッターを大幅に削減します。

`rate-limiter-auto-tuned`構成項目を変更することで、この機能を無効にすることができます。

#### GC 圧縮フィルター機能をデフォルトで有効にして、GC による CPU と I/O リソースの消費を削減します。 {#enable-the-gc-compaction-filter-feature-by-default-to-reduce-gc-s-consumption-of-cpu-and-i-o-resources}

[ユーザードキュメント](/garbage-collection-configuration.md#gc-in-compaction-filter) [＃18009](https://github.com/pingcap/tidb/issues/18009)

TiDBがガベージコレクション（GC）とデータ圧縮を実行する際、パーティションはCPUとI/Oリソースを占有します。これらの2つのタスクの実行中は、データが重複することがあります。

GCによるCPUおよびI/Oリソースの消費量を削減するため、GCコンパクションフィルタ機能はこれら2つのタスクを1つに統合し、同じタスク内で実行します。この機能はデフォルトで有効になっています。1 `gc.enable-compaction-filter = false`設定することで無効にできます。

#### TiFlash は、圧縮とデータソートの I/O リソースの使用を制限します (<strong>実験的機能</strong>) {#tiflash-limits-the-compression-and-data-sorting-s-use-of-i-o-resources-strong-experimental-feature-strong}

この機能により、バックグラウンド タスクとフォアグラウンドの読み取りおよび書き込み間の I/O リソースの競合が軽減されます。

この機能はデフォルトで無効になっています。1 `bg_task_io_rate_limit`設定項目を変更することで、この機能を有効にすることができます。

#### 大規模クラスター内のスケジュール制約のチェックと不健全なリージョンの修正のパフォーマンスを向上 {#improve-the-performance-of-checking-scheduling-constraints-and-the-performance-of-fixing-the-unhealthy-regions-in-a-large-cluster}

### パフォーマンスのジッタを回避するために、実行プランが可能な限り変更されないようにします。 {#ensure-that-the-execution-plans-are-unchanged-as-much-as-possible-to-avoid-performance-jitter}

[ユーザードキュメント](/sql-plan-management.md)

#### SQLバインディングは、 <code>INSERT</code> 、 <code>REPLACE</code> 、 <code>UPDATE</code> 、 <code>DELETE</code>ステートメントをサポートします。 {#sql-binding-supports-the-code-insert-code-code-replace-code-code-update-code-code-delete-code-statements}

パフォーマンスチューニングやデータベースのメンテナンスを行う際に、実行プランが不安定なためにシステムパフォーマンスが不安定になっていることが判明した場合、ユーザーの判断または`EXPLAIN ANALYZE`でテストしたSQL文を手動で最適化することができます。最適化されたSQL文をアプリケーションコードで実行するSQL文にバインドすることで、安定したパフォーマンスを確保できます。

SQL BINDING ステートメントを使用して SQL ステートメントを手動でバインドする場合は、最適化された SQL ステートメントの構文が元の SQL ステートメントと同じであることを確認する必要があります。

`SHOW {GLOBAL | SESSION} BINDINGS`コマンドを実行すると、手動または自動でバインドされた実行プラン情報を表示できます。出力はv5.0より前のバージョンと同じです。

#### 実行プランを自動的にキャプチャしてバインドする {#automatically-capture-and-bind-execution-plans}

TiDBをアップグレードする際には、パフォーマンスのジッターを回避するために、ベースラインキャプチャ機能を有効にすることができます。これにより、システムは最新の実行プランを自動的にキャプチャしてバインドし、システムテーブルに保存します。TiDBのアップグレード後、 `SHOW GLOBAL BINDING`コマンドを実行してバインドされた実行プランをエクスポートし、これらのプランを削除するかどうかを決定できます。

この機能はデフォルトで無効になっています。サーバーを変更するか、グローバルシステム変数`tidb_capture_plan_baselines` `ON`に設定することで有効にできます。この機能を有効にすると、システムはステートメントサマリーから少なくとも2回出現するSQL文を`bind-info-lease` （デフォルト値は`3s` ）ごとに取得し、自動的にキャプチャしてバインドします。

### TiFlashクエリの安定性を向上 {#improve-stability-of-tiflash-queries}

TiFlashが失敗した場合にTiKVにクエリをフォールバックするためのシステム変数[`tidb_allow_fallback_to_tikv`](/system-variables.md#tidb_allow_fallback_to_tikv-new-in-v50)追加します。デフォルト値は`OFF`です。

### TiCDC の安定性を改善し、過度の増分データの複製によって引き起こされる OOM の問題を軽減します。 {#improve-ticdc-stability-and-alleviate-the-oom-issue-caused-by-replicating-too-much-incremental-data}

[ユーザードキュメント](/ticdc/ticdc-manage-changefeed.md#unified-sorter) [＃1150](https://github.com/pingcap/tiflow/issues/1150)

TiCDC v4.0.9以前のバージョンでは、データ変更のレプリケーションが多すぎるとOOMが発生する可能性がありました。v5.0では、Unified Sorter機能がデフォルトで有効になり、以下のシナリオで発生するOOMの問題を軽減します。

-   TiCDC のデータ複製タスクは長時間一時停止され、その間に大量の増分データが蓄積され、複製が必要になります。
-   データ複製タスクは早いタイムスタンプから開始されるため、大量の増分データを複製する必要が生じます。

Unified Sorterは、以前のバージョンの`memory` `file`エンジンオプションと統合されています。手動で変更する必要はありません。

制限事項:

-   増分データの量に応じて十分なディスク容量を確保する必要があります。128GB以上の空き容量を持つSSDの使用をお勧めします。

## 高可用性と災害復旧 {#high-availability-and-disaster-recovery}

### リージョンメンバーシップの変更時のシステム可用性の向上 {#improve-system-availability-during-region-membership-change}

[ユーザードキュメント](/pd-configuration-file.md#enable-joint-consensus-new-in-v50) [＃18079](https://github.com/pingcap/tidb/issues/18079) [＃7587](https://github.com/tikv/tikv/issues/7587) [＃2860](https://github.com/tikv/pd/issues/2860)

リージョンメンバーシップの変更プロセスでは、「メンバーの追加」と「メンバーの削除」という2つの操作が2つのステップで実行されます。メンバーシップの変更完了時に障害が発生した場合、リージョンは利用できなくなり、フォアグラウンドアプリケーションのエラーが返されます。

導入されたRaft Joint Consensusアルゴリズムは、リージョンメンバーシップの変更時のシステム可用性を向上させます。メンバーシップ変更時の「メンバーの追加」と「メンバーの削除」操作は1つの操作に統合され、すべてのメンバーに送信されます。変更プロセス中、リージョンは中間状態にあります。変更されたメンバーのいずれかに障害が発生しても、システムは引き続き利用可能です。

この機能はデフォルトで有効になっています。1 コマンドを実行して`pd-ctl config set enable-joint-consensus` `enable-joint-consensus`値を`false`に設定することで無効にできます。

### メモリ管理モジュールを最適化してシステムのOOMリスクを軽減します {#optimize-the-memory-management-module-to-reduce-system-oom-risks}

集計関数のメモリ使用量を追跡します。この機能はデフォルトで有効になっています。集計関数を含むSQL文を実行する際、現在のクエリの合計メモリ使用量が`mem-quota-query`で設定されたしきい値を超えると、システムは`oom-action`で定義された操作を自動的に実行します。

### ネットワーク分割時のシステム可用性を向上 {#improve-the-system-availability-during-network-partition}

## データ移行 {#data-migration}

### S3/ Auroraから TiDB へのデータ移行 {#migrate-data-from-s3-aurora-to-tidb}

TiDB データ移行ツールは、Amazon S3 (およびその他の S3 互換storageサービス) をデータ移行の中間として使用し、 Auroraスナップショット データを TiDB に直接初期化することをサポートしており、Amazon S3/ Auroraから TiDB にデータを移行するためのオプションがさらに増えます。

この機能を使用するには、次のドキュメントを参照してください。

-   [Amazon S3クラウドstorageにデータをエクスポートする](/dumpling-overview.md#export-data-to-amazon-s3-cloud-storage) [＃8](https://github.com/pingcap/dumpling/issues/8)
-   [TiDB Lightningを使用して Amazon Aurora MySQL から移行する](/migrate-aurora-to-tidb.md) [＃266](https://github.com/pingcap/tidb-lightning/issues/266)

### TiDB Cloudのデータインポートパフォーマンスを最適化 {#optimize-the-data-import-performance-of-tidb-cloud}

TiDB Lightningは、 TiDB CloudのAWS T1.standard構成（または同等の構成）向けにデータインポートパフォーマンスを最適化します。テスト結果によると、 TiDB Lightningは1TBのTPC-CデータをTiDBにインポートする速度を254GiB/時間から366GiB/時間へと40%向上させました。

## データの共有とサブスクリプション {#data-sharing-and-subscription}

### TiCDC を使用して TiDB を Kafka Connect (Confluent Platform) に統合する (<strong>実験的機能</strong>) {#integrate-tidb-to-kafka-connect-confluent-platform-using-ticdc-strong-experimental-feature-strong}

[ユーザードキュメント](/ticdc/integrate-confluent-using-ticdc.md) [＃660](https://github.com/pingcap/tiflow/issues/660)

この機能により、TiDB データを他のシステムにストリーミングするというビジネス要件をサポートするために、TiDB データを Kafka、Hadoop、Oracle などのシステムにストリーミングできるようになります。

Confluent プラットフォームが提供する Kafka コネクタプロトコルはコミュニティで広く利用されており、様々なプロトコルでリレーショナルデータベースと非リレーショナルデータベースの両方へのデータ転送をサポートしています。TiCDC を Confluent プラットフォームの Kafka Connect に統合することで、TiDB は TiDB データを他の異種データベースやシステムにストリーミングする機能を拡張します。

## 診断 {#diagnostics}

[ユーザードキュメント](/sql-statements/sql-statement-explain.md#explain)

SQLパフォーマンスの問題のトラブルシューティングでは、パフォーマンス問題の原因を特定するために詳細な診断情報が必要です。TiDB 5.0より前のバージョンでは、 `EXPLAIN`ステートメントで収集される情報は十分に詳細ではありませんでした。問題の根本原因は、ログ情報、監視情報、あるいは推測に基づいてしか特定できず、非効率的である可能性があります。

TiDB v5.0 では、パフォーマンスの問題をより効率的にトラブルシューティングできるように、次の改善が加えられています。

-   `EXPLAIN ANALYZE`ステートメントを使用してすべての DML ステートメントを分析し、実際のパフォーマンス プランと各演算子の実行情報を表示することをサポートします[＃18056](https://github.com/pingcap/tidb/issues/18056)
-   `EXPLAIN FOR CONNECTION`ステートメントを使用して、実行中のすべてのSQL文のリアルタイムステータスを確認できます。例えば、各演算子の実行時間や処理された行数を確認できます[＃18233](https://github.com/pingcap/tidb/issues/18233)
-   `EXPLAIN ANALYZE`ステートメントの出力で、オペレータによって送信された RPC 要求の数、ロック競合の解決にかかる時間、ネットワークレイテンシー、RocksDB でスキャンされた削除済みデータの量、RocksDB キャッシュのヒット率など、オペレータ実行に関する詳細情報を提供します[＃18663](https://github.com/pingcap/tidb/issues/18663)
-   SQL文の詳細な実行情報をスローログに自動的に記録する機能をサポートします。スローログに記録される実行情報は、 `EXPLAIN ANALYZE`文の出力情報と一致しており、各演算子の実行時間、処理行数、送信されたRPCリクエスト数などが含まれ[＃15009](https://github.com/pingcap/tidb/issues/15009) 。

## 展開と保守 {#deployment-and-maintenance}

### クラスタ導入操作のロジックを最適化し、DBAが標準のTiDB本番クラスタのセットをより迅速に導入できるようにします。 {#optimize-the-logic-of-cluster-deployment-operations-to-help-dbas-deploy-a-set-of-standard-tidb-production-cluster-faster}

[ユーザードキュメント](/production-deployment-using-tiup.md)

以前のTiDBバージョンでは、 TiUPを使用してTiDBクラスタを展開するDBAは、環境の初期化が複雑で、チェックサム設定が過剰で、クラスタトポロジファイルの編集が困難であることに気づきました。これらの問題はすべて、DBAの展開効率の低下につながっていました。TiDB v5.0では、以下の点が改善され、 TiUPを使用したTiDBの展開効率がDBAにとって向上しました。

-   TiUP クラスタ は、より包括的なワンクリック環境チェックを実行し、修復の推奨事項を提供する`check topo.yaml`コマンドをサポートしています。
-   TiUP クラスタ は、環境チェック中に検出された環境の問題を自動的に修復する`check topo.yaml --apply`コマンドをサポートしています。
-   TiUP クラスタ は、DBA がグローバル ノード パラメータを編集および変更できるように、クラスター トポロジ テンプレート ファイルを取得するための`template`コマンドをサポートしています。
-   TiUP は、リモート Prometheus を構成するために`edit-config`コマンドを使用して`remote_config`パラメータを編集することをサポートしています。
-   TiUP は、 `edit-config`コマンドを使用してさまざまな AlertManagers を構成するために`external_alertmanagers`パラメータを編集することをサポートしています。
-   tiup-clusterの`edit-config`サブコマンドを使用してトポロジファイルを編集するときに、構成項目の値のデータ型を変更できます。

### アップグレードの安定性を向上 {#improve-upgrade-stability}

TiUP v1.4.0 より前では、 tiup-clusterを使用して TiDB クラスターをアップグレードすると、クラスターの SQL 応答が長時間にわたって不安定になり、PD オンライン ローリング アップグレードを実行すると、クラスターの QPS が 10 秒から 30 秒の間不安定になりました。

TiUP v1.4.0 ではロジックが調整され、次の最適化が行われます。

-   PD ノードのアップグレード中、 TiUP は再起動された PD ノードのステータスを自動的にチェックし、ステータスが準備完了であることを確認した後、次の PD ノードのアップグレードをロールします。
-   TiUP はPD ロールを自動的に識別し、最初にフォロワー ロールの PD ノードをアップグレードし、最後に PDLeaderノードをアップグレードします。

### アップグレード時間を最適化する {#optimize-the-upgrade-time}

TiUP v1.4.0 より前のバージョンでは、DBA がtiup-clusterを使用して TiDB クラスターをアップグレードする場合、多数のノードを持つクラスターでは合計アップグレード時間が長くなり、特定のユーザーのアップグレード時間枠の要件を満たすことができません。

v1.4.0 以降、 TiUP は次の項目を最適化します。

-   `tiup cluster upgrade --offline`サブコマンドを使用した高速オフライン アップグレードをサポートします。
-   アップグレード中にローリング アップグレードを使用するユーザーのリージョンLeaderの再配置をデフォルトで高速化し、ローリング TiKV アップグレードの時間を短縮します。
-   ローリングアップグレードを実行する前に、サブコマンド`check`を使用してリージョンモニターのステータスを確認します。アップグレード前にクラスターが正常な状態であることを確認することで、アップグレードが失敗する可能性を低減します。

### ブレークポイント機能をサポートする {#support-the-breakpoint-feature}

TiUP v1.4.0 より前のバージョンでは、DBA がtiup-clusterを使用して TiDB クラスターをアップグレードする場合、コマンドの実行が中断されると、すべてのアップグレード操作を最初から再度実行する必要がありました。

TiUP v1.4.0 は、アップグレードの中断後にすべての操作が再実行されるのを回避するために、 tiup-cluster `replay`サブコマンドを使用してブレークポイントから失敗した操作を再試行することをサポートしています。

### 保守と運用の機能を強化する {#enhance-the-functionalities-of-maintenance-and-operations}

TiUP v1.4.0 では、TiDB クラスターの操作と保守の機能がさらに強化されています。

-   より多くの使用シナリオに適応するために、ダウンタイム TiDB および DM クラスターでのアップグレードまたはパッチ操作をサポートします。
-   クラスターのバージョンを取得するために、 tiup-clusterの`display`サブコマンドに`--version`パラメータを追加します。
-   スケールアウトするノードに Prometheus のみが含まれている場合、Prometheus ノードの不在によるスケールアウトの失敗を回避するために、監視構成の更新操作は実行されません。
-   入力されたTiUPコマンドの結果が正しくない場合に、エラー メッセージにユーザー入力を追加して、問題の原因をより迅速に特定できるようにします。

## テレメトリー {#telemetry}

TiDB は、データ テーブルの数、クエリの数、新しい機能が有効になっているかどうかなど、テレメトリにクラスター使用状況メトリックを追加します。

この動作の詳細と無効にする方法については、 [テレメトリー](/telemetry.md)を参照してください。
