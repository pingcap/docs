---
title: What's New in TiDB 5.0
summary: TiDB 5.0 では、MPPアーキテクチャ、クラスター化インデックス、非同期コミット、安定性の向上が導入されています。また、互換性の変更、構成パラメータ、新機能も強化されています。さらに、パフォーマンス、高可用性、災害復旧、データ移行、診断、展開、メンテナンスが最適化されています。クラスター使用状況メトリック用のテレメトリが追加されています。
---

# TiDB 5.0 の新機能 {#what-s-new-in-tidb-5-0}

発売日: 2021年4月7日

TiDB バージョン: 5.0.0

バージョン 5.0 では、PingCAP は、企業が TiDB に基づいてアプリケーションを迅速に構築できるように支援し、データベースのパフォーマンス、パフォーマンスのジッター、セキュリティ、高可用性、災害復旧、SQL パフォーマンスのトラブルシューティングなどに関する心配から解放することに重点を置いています。

v5.0 の主な新機能または改善点は次のとおりです。

-   TiFlashノードを通じて超並列処理 (MPP)アーキテクチャを導入し、大規模な結合クエリの実行ワークロードをTiFlashノード間で共有します。MPP モードを有効にすると、TiDB はコストに基づいて、MPP フレームワークを使用して計算を実行するかどうかを決定します。MPP モードでは、計算中に結合キーが`Exchange`操作を通じて再分配されるため、計算負荷が各TiFlashノードに分散され、計算が高速化されます。ベンチマークによると、同じクラスター リソースの場合、TiDB 5.0 MPP は Greenplum 6.15.0 および Apache Spark 3.1.1 よりも 2 ～ 3 倍高速化され、一部のクエリでは 8 倍のパフォーマンスが向上しました。
-   クラスター化インデックス機能を導入して、データベースのパフォーマンスを向上させます。たとえば、TPC-C tpmC テストでは、クラスター化インデックスを有効にした TiDB のパフォーマンスが 39% 向上します。
-   非同期コミット機能を有効にすると、書き込みレイテンシーが短縮されます。たとえば、64 スレッドの Sysbench テストでは、非同期コミットを有効にすると、インデックス更新の平均レイテンシーが12.04 ミリ秒から 7.01 ミリ秒に 41.7% 短縮されます。
-   ジッターを削減します。これは、オプティマイザーの安定性を向上させ、システム タスクによる I/O、ネットワーク、CPU、メモリリソースの使用を制限することで実現されます。たとえば、8 時間のパフォーマンス テストでは、TPC-C tpmC の標準偏差は 2% を超えません。
-   スケジュールを改善し、実行計画を可能な限り安定させることで、システムの安定性を高めます。
-   リージョンメンバーシップの変更中にシステムの可用性を確保するRaft Joint Consensus アルゴリズムを導入します。
-   `EXPLAIN`機能と非表示のインデックスを最適化し、データベース管理者 (DBA) が SQL ステートメントをより効率的にデバッグできるようにします。
-   企業データの信頼性を保証します。TiDB から Amazon S3storageや Google Cloud GCS にデータをバックアップしたり、これらのクラウドstorageプラットフォームからデータを復元したりできます。
-   Amazon S3storageまたは TiDB/MySQL からのデータ インポートまたはデータ エクスポートのパフォーマンスが向上し、企業がクラウド上でアプリケーションを迅速に構築できるようになります。たとえば、TPC-C テストでは、1 TiB データのインポートのパフォーマンスが 254 GiB/h から 366 GiB/h に 40% 向上します。

## 互換性の変更 {#compatibility-changes}

### システム変数 {#system-variables}

-   複数の演算子の同時実行を制御するには、 [`tidb_executor_concurrency`](/system-variables.md#tidb_executor_concurrency-new-in-v50)システム変数を追加します。以前の`tidb_*_concurrency`設定 ( `tidb_projection_concurrency`など) は引き続き有効ですが、使用すると警告が表示されます。

-   ASCII 文字セットを書き込むときに ASCII 検証チェックをスキップするかどうかを指定するには、 [`tidb_skip_ascii_check`](/system-variables.md#tidb_skip_ascii_check-new-in-v50)システム変数を追加します。このデフォルト値は`OFF`です。

-   [`tidb_enable_strict_double_type_check`](/system-variables.md#tidb_enable_strict_double_type_check-new-in-v50)システム変数を追加して、 `double(N)`のような構文をテーブル スキーマで定義できるかどうかを決定します。このデフォルト値は`OFF`です。

-   デフォルト値[`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size)を`20000`から`0`に変更します。これは、 `LOAD` / `INSERT INTO SELECT ...`ではバッチ DML ステートメントがデフォルトで使用されなくなることを意味します。代わりに、厳密なACIDセマンティクスに準拠するために大規模なトランザクションが使用されます。

    > **注記：**
    >
    > 変数のスコープはセッションからグローバルに変更され、デフォルト値は`20000`から`0`に変更されます。アプリケーションが元のデフォルト値に依存している場合は、アップグレード後に`set global`ステートメントを使用して変数を元の値に変更する必要があります。

-   [`tidb_enable_noop_functions`](/system-variables.md#tidb_enable_noop_functions-new-in-v40)システム変数を使用して、一時テーブルの構文の互換性を制御します。この変数値が`OFF`場合、 `CREATE TEMPORARY TABLE`構文はエラーを返します。

-   ガベージコレクション関連のパラメータを直接制御するには、次のシステム変数を追加します。
    -   [`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-new-in-v50)
    -   [`tidb_gc_enable`](/system-variables.md#tidb_gc_enable-new-in-v50)
    -   [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)
    -   [`tidb_gc_run_interval`](/system-variables.md#tidb_gc_run_interval-new-in-v50)
    -   [`tidb_gc_scan_lock_mode`](/system-variables.md#tidb_gc_scan_lock_mode-new-in-v50)

-   デフォルト値[`enable-joint-consensus`](/pd-configuration-file.md#enable-joint-consensus-new-in-v50)を`false`から`true`に変更します。これにより、共同コンセンサス機能がデフォルトで有効になります。

-   `tidb_enable_amend_pessimistic_txn`の値を`0`または`1`から`ON`または`OFF`に変更します。

-   デフォルト値[`tidb_enable_clustered_index`](/system-variables.md#tidb_enable_clustered_index-new-in-v50)を`OFF`から`INT_ONLY`に変更し、次の新しい意味を追加します。
    -   `ON` : クラスター化インデックスが有効です。非クラスター化インデックスの追加または削除がサポートされています。

    -   `OFF` : クラスター化インデックスは無効です。非クラスター化インデックスの追加または削除はサポートされています。

    -   `INT_ONLY` : デフォルト値。動作は v5.0 以前と同じです。 `alter-primary-key = false`と組み合わせて INT 型のクラスター化インデックスを有効にするかどうかを制御できます。
    > **注記：**
    >
    > 5.0 GA の`tidb_enable_clustered_index`の`INT_ONLY`値は、 5.0 RC の`OFF`値と同じ意味を持ちます。 `OFF`設定の 5.0 RC クラスターから 5.0 GA にアップグレードすると、 `INT_ONLY`として表示されます。

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

-   TiDB の[`index-limit`](/tidb-configuration-file.md#index-limit-new-in-v50)構成項目を追加します。その値はデフォルトで`64`に設定され、範囲は`[64,512]`です。MySQL テーブルは最大 64 個のインデックスをサポートします。その値がデフォルト設定を超え、テーブルに対して 64 個を超えるインデックスが作成されると、テーブル スキーマが MySQL に再インポートされたときにエラーが報告されます。
-   TiDB が MySQL の ENUM/SET の長さ (ENUM の長さ &lt; 255) と互換性と一貫性を保つために、 [`enable-enum-length-limit`](/tidb-configuration-file.md#enable-enum-length-limit-new-in-v50)構成項目を追加します。デフォルト値は`true`です。
-   `pessimistic-txn.enable`構成項目を[`tidb_txn_mode`](/system-variables.md#tidb_txn_mode)環境変数に置き換えます。
-   `performance.max-memory`構成項目を[`performance.server-memory-quota`](/tidb-configuration-file.md#server-memory-quota-new-in-v409)に置き換える
-   `tikv-client.copr-cache.enable`構成項目を[`tikv-client.copr-cache.capacity-mb`](/tidb-configuration-file.md#capacity-mb)に置き換えます。項目の値が`0.0`の場合、この機能は無効になります。項目の値が`0.0`より大きい場合、この機能は有効になります。デフォルト値は`1000.0`です。
-   `rocksdb.auto-tuned`構成項目を[`rocksdb.rate-limiter-auto-tuned`](/tikv-configuration-file.md#rate-limiter-auto-tuned-new-in-v50)に置き換えます。
-   `raftstore.sync-log`設定項目を削除します。デフォルトでは、書き込まれたデータは強制的にディスクに書き込まれます。v5.0 より前は、 `raftstore.sync-log`明示的に無効にできました。v5.0 以降では、設定値は強制的に`true`に設定されます。
-   `gc.enable-compaction-filter`構成項目のデフォルト値を`false`から`true`に変更します。
-   `enable-cross-table-merge`構成項目のデフォルト値を`false`から`true`に変更します。
-   [`rate-limiter-auto-tuned`](/tikv-configuration-file.md#rate-limiter-auto-tuned-new-in-v50)構成項目のデフォルト値を`false`から`true`に変更します。

### その他 {#others}

-   アップグレード前に、TiDB 構成[`feedback-probability`](https://docs.pingcap.com/tidb/v5.0/tidb-configuration-file#feedback-probability)の値を確認してください。値が 0 でない場合、アップグレード後に「回復可能な goroutine でpanicが発生しました」というエラーが発生しますが、このエラーはアップグレードには影響しません。
-   データの正確性の問題を回避するために、列タイプの変更中に`VARCHAR`タイプと`CHAR`タイプ間の変換を禁止します。

## 新機能 {#new-features}

### 構文 {#sql}

#### List パーティショニング（<strong>Experimental</strong>） {#list-partitioning-strong-experimental-strong}

[ユーザードキュメント](/partitioned-table.md#list-partitioning)

リスト パーティション機能を使用すると、大量のデータを含むテーブルを効率的にクエリおよび管理できます。

この機能を有効にすると、パーティションと、パーティション間でのデータの分散方法が`PARTITION BY LIST(expr) PARTITION part_name VALUES IN (...)`式に従って定義されます。パーティション化されたテーブルのデータ セットは、最大 1024 個の異なる整数値をサポートします。値は`PARTITION ... VALUES IN (...)`句を使用して定義できます。

リストのパーティション分割を有効にするには、セッション変数[`tidb_enable_list_partition`](/system-variables.md#tidb_enable_list_partition-new-in-v50)を`ON`に設定します。

#### List COLUMNS パーティショニング（<strong>Experimental</strong>） {#list-columns-partitioning-strong-experimental-strong}

[ユーザードキュメント](/partitioned-table.md#list-columns-partitioning)

List COLUMNS パーティショニングは`DATETIME` `DATE`型の列もパーティション列として使用できます。

List COLUMNS パーティショニングを有効にするには、セッション変数[`tidb_enable_list_partition`](/system-variables.md#tidb_enable_list_partition-new-in-v50)を`ON`に設定します。

#### 目に見えないインデックス {#invisible-indexes}

[ユーザードキュメント](/sql-statements/sql-statement-alter-index.md) , [＃9246](https://github.com/pingcap/tidb/issues/9246)

パフォーマンスを調整したり、最適なインデックスを選択したりする場合、SQL ステートメントを使用してインデックスを`Visible`または`Invisible`に設定できます。この設定により、 `DROP INDEX`や`ADD INDEX`などのリソースを消費する操作の実行を回避できます。

インデックスの可視性を変更するには、 `ALTER INDEX`ステートメントを使用します。変更後、オプティマイザーはインデックスの可視性に基づいて、このインデックスをインデックス リストに追加するかどうかを決定します。

#### <code>EXCEPT</code>および<code>INTERSECT</code>演算子 {#code-except-code-and-code-intersect-code-operators}

[ユーザードキュメント](/functions-and-operators/set-operators.md) , [＃18031](https://github.com/pingcap/tidb/issues/18031)

`INTERSECT`演算子はセット演算子であり、2 つ以上のクエリの結果セットの積集合を返します。ある程度、これは`Inner Join`演算子の代替となります。

`EXCEPT`演算子はセット演算子であり、2 つのクエリの結果セットを結合し、最初のクエリ結果にはあるが 2 番目のクエリ結果にはない要素を返します。

### トランザクション {#transaction}

[＃18005](https://github.com/pingcap/tidb/issues/18005)

悲観的トランザクション モードでは、トランザクションに関係するテーブルに同時 DDL 操作または`SCHEMA VERSION`変更が含まれている場合、システムはトランザクションの`SCHEMA VERSION`最新のものに自動的に更新して、トランザクションのコミットが成功することを保証し、トランザクションが DDL 操作または`SCHEMA VERSION`変更によって中断されたときにクライアントが`Information schema is changed`エラーを受け取ることを回避します。

この機能はデフォルトで無効になっています。この機能を有効にするには、 `tidb_enable_amend_pessimistic_txn`システム変数の値を変更します。この機能は v4.0.7 で導入され、v5.0 では次の問題が修正されています。

-   TiDB Binlogが`Add Column`操作を実行するときに発生する互換性の問題
-   この機能をユニークインデックスと併用すると発生するデータの不整合の問題
-   追加されたインデックスとこの機能を併用すると発生するデータの不整合の問題

現在、この機能には次のような非互換性の問題が残っています。

-   同時トランザクションがある場合、トランザクションのセマンティクスが変わる可能性があります
-   この機能を TiDB Binlogと併用すると発生する既知の互換性の問題
-   `Change Column`との互換性がない

### 文字セットと照合順序 {#character-set-and-collation}

-   `utf8mb4_unicode_ci`と`utf8_unicode_ci` [ユーザードキュメント](/character-set-and-collation.md#new-framework-for-collations)をサポートします[＃17596](https://github.com/pingcap/tidb/issues/17596)
-   照合順序の大文字と小文字を区別しない比較ソートをサポートする

### Security {#security}

[ユーザードキュメント](/log-redaction.md) , [＃18566](https://github.com/pingcap/tidb/issues/18566)

セキュリティコンプライアンス要件（*一般データ保護規則*（GDPR）など）を満たすために、システムは出力エラーメッセージとログ内の情報（IDやクレジットカード番号など）の機密性を下げることをサポートしており、これにより機密情報の漏洩を防ぐことができます。

TiDB は出力ログ情報の感度低下をサポートしています。この機能を有効にするには、次のスイッチを使用します。

-   グローバル変数[`tidb_redact_log`](/system-variables.md#tidb_redact_log) 。デフォルト値は`0`で、これは感度低下が無効であることを意味します。tidb-server ログの感度低下を有効にするには、変数値を`1`に設定します。
-   設定項目`security.redact-info-log` 。デフォルト値は`false`で、これは感度低下が無効であることを意味します。tikv-server ログの感度低下を有効にするには、変数値を`true`に設定します。
-   構成項目`security.redact-info-log` 。デフォルト値は`false`で、これは感度低下が無効であることを意味します。pd-server ログの感度低下を有効にするには、変数値を`true`に設定します。
-   tiflash-server の場合は設定項目`security.redact_info_log` 、tiflash-learner の場合は設定項目`security.redact-info-log` 。デフォルト値は両方とも`false`で、これは感度低下が無効であることを意味します。tiflash-server および tiflash-learner ログの感度低下を有効にするには、両方の変数の値を`true`に設定します。

この機能はバージョン 5.0 で導入されました。この機能を使用するには、システム変数と上記のすべての構成項目を有効にします。

## パフォーマンスの最適化 {#performance-optimization}

### MPPアーキテクチャ {#mpp-architecture}

[ユーザードキュメント](/tiflash/use-tiflash-mpp-mode.md)

TiDB は、 TiFlashノードを通じて MPPアーキテクチャを導入します。このアーキテクチャにより、複数のTiFlashノードが大規模な結合クエリの実行ワークロードを共有できるようになります。

MPP モードがオンの場合、TiDB は計算コストに基づいて、計算のためにクエリを MPP エンジンに送信するかどうかを決定します。MPP モードでは、TiDB はデータ計算 ( `Exchange`操作) 中に結合キーを再配布することにより、実行中の各TiFlashノードにテーブル結合の計算を分散し、計算を高速化します。さらに、 TiFlashがすでにサポートしている集計コンピューティング機能を使用すると、TiDB はクエリの計算をTiFlash MPP クラスターにプッシュダウンできます。分散環境により、実行プロセス全体が高速化され、分析クエリの速度が大幅に向上します。

TPC-H 100 ベンチマーク テストでは、 TiFlash MPP は従来の分析データベースの分析エンジンや Hadoop 上の SQL よりも大幅に処理速度が速いことが示されています。このアーキテクチャにより、最新のトランザクション データに対して大規模な分析クエリを直接実行でき、従来のオフライン分析ソリューションよりも高いパフォーマンスが得られます。ベンチマークによると、同じクラスター リソースの場合、TiDB 5.0 MPP は Greenplum 6.15.0 や Apache Spark 3.1.1 よりも 2 ～ 3 倍高速化しており、一部のクエリでは 8 倍のパフォーマンス向上が見られます。

現在、MPP モードでサポートされていない主な機能は次のとおりです (詳細については[TiFlashを使用する](/tiflash/use-tiflash-mpp-mode.md)を参照してください)。

-   テーブルパーティション
-   ウィンドウ関数
-   照合
-   いくつかの組み込み関数
-   TiKVからデータを読み取る
-   OOMスピル
-   連合
-   完全外部結合

### クラスター化インデックス {#clustered-index}

[ユーザードキュメント](/clustered-indexes.md) , [＃4841](https://github.com/pingcap/tidb/issues/4841)

テーブル構造を設計したり、データベースの動作を分析したりする際に、主キーを持つ一部の列が頻繁にグループ化され、並べ替えられ、これらの列に対するクエリによって特定の範囲のデータや異なる値を持つ少量のデータが返されることが多く、対応するデータによって読み取りまたは書き込みのホットスポットの問題が発生しない場合は、クラスター化インデックス機能を使用することをお勧めします。

クラスター化インデックスは、テーブルのデータに関連付けられたstorage構造です。一部のデータベース管理システムでは、クラスター化インデックス テーブルを*インデックス構成テーブル*と呼びます。クラスター化インデックスを作成するときに、テーブルの 1 つ以上の列をインデックスのキーとして指定できます。TiDB はこれらのキーを特定の構造に格納します。これにより、TiDB はキーに関連付けられた行を迅速かつ効率的に見つけることができるため、データのクエリと書き込みのパフォーマンスが向上します。

クラスター化インデックス機能を有効にすると、次の場合に TiDB のパフォーマンスが大幅に向上します (たとえば、TPC-C tpmC テストでは、クラスター化インデックスを有効にした TiDB のパフォーマンスが 39% 向上します)。

-   データが挿入されると、クラスター化インデックスにより、ネットワークからのインデックス データの書き込みが 1 回削減されます。
-   同等の条件を持つクエリに主キーのみが関係する場合、クラスター化インデックスにより、ネットワークからのインデックス データの読み取りが 1 回削減されます。
-   範囲条件を持つクエリに主キーのみが関係する場合、クラスター化インデックスにより、ネットワークからのインデックス データの複数回の読み取りが削減されます。
-   同等条件または範囲条件を持つクエリに主キー プレフィックスが含まれる場合、クラスター化インデックスによって、ネットワークからのインデックス データの複数回の読み取りが削減されます。

各テーブルでは、クラスター化インデックスまたは非クラスター化インデックスを使用してデータを並べ替えて保存できます。これら 2 つのstorage構造の違いは次のとおりです。

-   クラスター化インデックスを作成する場合、テーブル内の 1 つ以上の列をインデックスのキー値として指定できます。クラスター化インデックスは、キー値に従ってテーブルのデータを並べ替えて格納します。各テーブルには、クラスター化インデックスを 1 つだけ含めることができます。テーブルにクラスター化インデックスがある場合は、クラスター化インデックス テーブルと呼ばれます。それ以外の場合は、非クラスター化インデックス テーブルと呼ばれます。
-   非クラスター化インデックスを作成すると、テーブル内のデータは順序付けされていない構造で格納されます。TiDB は各データ行に一意の ROWID を自動的に割り当てるため、非クラスター化インデックスのキー値を明示的に指定する必要はありません。クエリの実行中、ROWID は対応する行の検索に使用されます。データのクエリまたは挿入を実行すると、少なくとも 2 つのネットワーク I/O 操作が発生するため、クラスター化インデックスと比較してパフォーマンスが低下します。

テーブル データが変更されると、データベース システムはクラスター化インデックスと非クラスター化インデックスを自動的に維持します。

すべての主キーは、デフォルトで非クラスター化インデックスとして作成されます。次の 2 つの方法のいずれかで、主キーをクラスター化インデックスまたは非クラスター化インデックスとして作成できます。

-   テーブルを作成するときにステートメントにキーワード`CLUSTERED | NONCLUSTERED`を指定すると、システムは指定された方法でテーブルを作成します。構文は次のとおりです。

```sql
CREATE TABLE `t` (`a` VARCHAR(255), `b` INT, PRIMARY KEY (`a`, `b`) CLUSTERED);
```

または

```sql
CREATE TABLE `t` (`a` VARCHAR(255) PRIMARY KEY CLUSTERED, `b` INT);
```

ステートメント`SHOW INDEX FROM tbl-name`を実行すると、テーブルにクラスター化インデックスがあるかどうかを照会できます。

-   クラスター化インデックス機能を制御するには、システム変数`tidb_enable_clustered_index`を構成します。サポートされる値は`ON` 、 `OFF` 、および`INT_ONLY`です。
    -   `ON` : すべての種類の主キーに対してクラスター化インデックス機能が有効になっていることを示します。非クラスター化インデックスの追加と削除がサポートされています。
    -   `OFF` : すべての種類の主キーに対してクラスター化インデックス機能が無効になっていることを示します。非クラスター化インデックスの追加と削除はサポートされています。
    -   `INT_ONLY` : デフォルト値。変数が`INT_ONLY`に設定され、 `alter-primary-key` `false`に設定されている場合、単一の整数列で構成される主キーは、デフォルトでクラスター化インデックスとして作成されます。この動作は、TiDB v5.0 以前のバージョンの動作と一致しています。

`CREATE TABLE`ステートメントにキーワード`CLUSTERED | NONCLUSTERED`含まれている場合、そのステートメントはシステム変数と構成項目の構成をオーバーライドします。

ステートメントでキーワード`CLUSTERED | NONCLUSTERED`を指定して、クラスター化インデックス機能を使用することをお勧めします。これにより、TiDB はシステム内のクラスター化インデックスと非クラスター化インデックスのすべてのデータ型を必要に応じて同時に使用できるようになります。

`INT_ONLY` 、この機能の互換性を保つために一時的に使用されているもので、将来的には廃止される予定であるため、 `tidb_enable_clustered_index = INT_ONLY`使用はお勧めしません。

クラスター化インデックスの制限は次のとおりです。

-   クラスター化インデックスと非クラスター化インデックス間の相互変換はサポートされていません。
-   クラスター化インデックスの削除はサポートされていません。
-   `ALTER TABLE`ステートメントを使用したクラスター化インデックスの追加、削除、および変更はサポートされていません。
-   クラスター化インデックスの再編成と再作成はサポートされていません。
-   インデックスの有効化または無効化はサポートされていないため、非表示のインデックス機能はクラスター化インデックスには効果がありません。
-   クラスター化インデックスとして`UNIQUE KEY`作成することはサポートされていません。
-   クラスター化インデックス機能を TiDB Binlogと併用することはサポートされていません。TiDB Binlogを有効にすると、TiDB はクラスター化インデックスとして単一の整数主キーの作成のみをサポートします。TiDB Binlog は、クラスター化インデックスを持つ既存のテーブルのデータ変更をダウンストリームに複製しません。
-   クラスター化インデックス機能を属性`SHARD_ROW_ID_BITS`および`PRE_SPLIT_REGIONS`と併用することはサポートされていません。
-   クラスターを新しいバージョンにアップグレードしてからロールバックする場合は、ロールバック前にテーブル データをエクスポートし、ロールバック後にデータをインポートして、新しく追加されたテーブルをダウングレードする必要があります。他のテーブルは影響を受けません。

### 非同期コミット {#async-commit}

[ユーザードキュメント](/system-variables.md#tidb_enable_async_commit-new-in-v50) , [＃8316](https://github.com/tikv/tikv/issues/8316)

データベースのクライアントは、データベース システムが 2 フェーズ (2PC) で同期的にトランザクション コミットを完了するまで待機します。トランザクションは、第 1 フェーズのコミットが成功した後に結果をクライアントに返し、システムは第 2 フェーズのコミット操作をバックグラウンドで非同期的に実行して、トランザクション コミットのレイテンシーを短縮します。トランザクションの書き込みに 1 つのリージョンのみが含まれる場合、第 2 フェーズは直接省略され、トランザクションは 1 フェーズ コミットになります。

非同期コミット機能を有効にした後、同じハードウェアと構成で、Sysbench を 64 スレッドで更新インデックスをテストするように設定すると、平均レイテンシーは12.04 ミリ秒から 7.01 ミリ秒に 41.7% 減少します。

非同期コミット機能を有効にすると、ネットワーク インタラクションのレイテンシーを減らし、データ書き込みのパフォーマンスを向上させるために、データベース アプリケーション開発者は、トランザクションの一貫性を線形一貫性から[因果関係の一貫性](/transaction-overview.md#causal-consistency)に減らすことを検討することをお勧めします。因果一貫性を有効にする SQL ステートメントは`START TRANSACTION WITH CAUSAL CONSISTENCY`です。

因果一貫性を有効にした後、同じハードウェアと構成で、Sysbench を 64 スレッドで oltp_write_only をテストするように設定すると、平均レイテンシーは11.86 ミリ秒から 11.19 ミリ秒に 5.6% 減少しました。

トランザクションの一貫性が線形一貫性から因果一貫性に低下した後、アプリケーション内の複数のトランザクション間に相互依存性がない場合、トランザクションはグローバルに一貫した順序を持ちません。

**新しく作成された v5.0 クラスターでは、非同期コミット機能がデフォルトで有効になっています。**

この機能は、以前のバージョンから v5.0 にアップグレードされたクラスターではデフォルトで無効になっています。この機能を有効にするには、 `set global tidb_enable_async_commit = ON;`および`set global tidb_enable_1pc = ON;`ステートメントを実行します。

非同期コミット機能の制限は次のとおりです。

-   直接のダウングレードはサポートされていません。

### コプロセッサーキャッシュ機能をデフォルトで有効にする {#enable-the-coprocessor-cache-feature-by-default}

[ユーザードキュメント](/tidb-configuration-file.md#tikv-clientcopr-cache-new-in-v400) , [＃18028](https://github.com/pingcap/tidb/issues/18028)

5.0 GA では、コプロセッサーキャッシュ機能がデフォルトで有効になっています。この機能を有効にすると、データの読み取りのレイテンシーを減らすために、TiDB は tikv-server にプッシュダウンされた演算子の計算結果を tidb-server にキャッシュします。

コプロセッサーキャッシュ機能を無効にするには、 `tikv-client.copr-cache` ～ `0.0`の`capacity-mb`構成項目を変更します。

### <code>delete from table where id &lt;? Limit ?</code>ステートメントの実行パフォーマンスを向上 {#improve-the-execution-performance-of-code-delete-from-table-where-id-x3c-limit-code-statement}

[＃18028](https://github.com/pingcap/tidb/issues/18028)

`delete from table where id <? limit ?`ステートメントの p99 パフォーマンスが 4 倍向上します。

### ロードベースの分割戦略を最適化して、一部の小さなテーブルのホットスポット読み取りシナリオでデータを分割できないというパフォーマンスの問題を解決します。 {#optimize-load-base-split-strategy-to-solve-the-performance-problem-that-data-cannot-be-split-in-some-small-table-hotspot-read-scenarios}

[＃18005](https://github.com/pingcap/tidb/issues/18005)

## 安定性の向上 {#improve-stability}

### 不完全なスケジューリングによって発生するパフォーマンスジッターの問題を最適化します {#optimize-the-performance-jitter-issue-caused-by-imperfect-scheduling}

[＃18005](https://github.com/pingcap/tidb/issues/18005)

TiDB のスケジューリング プロセスは、I/O、ネットワーク、CPU、メモリなどのリソースを占有します。TiDB がスケジュールされたタスクを制御しない場合、リソースのプリエンプションにより QPS と遅延によってパフォーマンスのジッターが発生する可能性があります。

以下の最適化を行った後、8 時間のパフォーマンス テストでは、TPC-C tpmC の標準偏差は 2% を超えません。

#### 不要なスケジューリングとパフォーマンスのジッターを削減するための新しいスケジューリング計算式を導入 {#introduce-new-scheduling-calculation-formulas-to-reduce-unnecessary-scheduling-and-performance-jitter}

ノード容量が常にシステムで設定されたウォーターラインに近い場合、または`store-limit`が大きすぎる場合、容量負荷のバランスをとるために、システムは頻繁にリージョンを他のノードにスケジュールしたり、リージョンを元のノードに戻してスケジュールしたりします。スケジューリングは I/O、ネットワーク、CPU、メモリなどのリソースを占有し、パフォーマンスのジッターを引き起こすため、このタイプのスケジューリングは必要ありません。

この問題を緩和するために、PD では新しいデフォルトのスケジュール計算式が導入されています。 `region-score-formula-version = v1`設定することで、古い式に戻すことができます。

#### デフォルトでクロステーブルリージョン結合機能を有効にする {#enable-the-cross-table-region-merge-feature-by-default}

[ユーザードキュメント](/pd-configuration-file.md#enable-cross-table-merge)

v5.0 より前の TiDB では、テーブル間のリージョンマージ機能がデフォルトで無効になっています。v5.0 以降では、空のリージョンの数と、ネットワーク、メモリ、CPU のオーバーヘッドを削減するために、この機能がデフォルトで有効になっています。1 `schedule.enable-cross-table-merge`構成項目を変更することで、この機能を無効にすることができます。

#### バックグラウンドタスクとフォアグラウンドの読み取りおよび書き込み間のI/Oリソースの競合のバランスをとるために、デフォルトでシステムが自動的にデータ圧縮速度を調整するようにする {#enable-the-system-to-automatically-adjust-the-data-compaction-speed-by-default-to-balance-the-contention-for-i-o-resources-between-background-tasks-and-foreground-reads-and-writes}

[ユーザードキュメント](/tikv-configuration-file.md#rate-limiter-auto-tuned-new-in-v50)

v5.0 より前では、バックグラウンド タスクとフォアグラウンドの読み取りおよび書き込み間の I/O リソースの競合のバランスをとるために、システムがデータ圧縮速度を自動的に調整する機能はデフォルトで無効になっています。v5.0 以降、TiDB はこの機能をデフォルトで有効にし、アルゴリズムを最適化してレイテンシージッターを大幅に削減します。

`rate-limiter-auto-tuned`構成項目を変更することで、この機能を無効にすることができます。

#### GC 圧縮フィルター機能をデフォルトで有効にして、GC による CPU と I/O リソースの消費を削減します。 {#enable-the-gc-compaction-filter-feature-by-default-to-reduce-gc-s-consumption-of-cpu-and-i-o-resources}

[ユーザードキュメント](/garbage-collection-configuration.md#gc-in-compaction-filter) , [＃18009](https://github.com/pingcap/tidb/issues/18009)

TiDB がガベージコレクション(GC) とデータ圧縮を実行すると、パーティションが CPU と I/O リソースを占有します。これら 2 つのタスクの実行中に重複データが存在します。

GC による CPU と I/O リソースの消費を減らすために、GC 圧縮フィルター機能はこれら 2 つのタスクを 1 つに結合し、同じタスクで実行します。この機能はデフォルトで有効になっています。1 `gc.enable-compaction-filter = false`設定することで無効にできます。

#### TiFlash は、圧縮とデータソートの I/O リソースの使用を制限します (<strong>実験的機能</strong>) {#tiflash-limits-the-compression-and-data-sorting-s-use-of-i-o-resources-strong-experimental-feature-strong}

この機能により、バックグラウンド タスクとフォアグラウンドの読み取りおよび書き込み間の I/O リソースの競合が軽減されます。

この機能はデフォルトでは無効になっています。1 `bg_task_io_rate_limit`構成項目を変更することで、この機能を有効にすることができます。

#### 大規模クラスター内のスケジュール制約のチェックと不健全なリージョンの修正のパフォーマンスを向上 {#improve-the-performance-of-checking-scheduling-constraints-and-the-performance-of-fixing-the-unhealthy-regions-in-a-large-cluster}

### パフォーマンスのジッタを回避するために、実行プランが可能な限り変更されないようにします。 {#ensure-that-the-execution-plans-are-unchanged-as-much-as-possible-to-avoid-performance-jitter}

[ユーザードキュメント](/sql-plan-management.md)

#### SQLバインディングは<code>INSERT</code> 、 <code>REPLACE</code> 、 <code>UPDATE</code> 、 <code>DELETE</code>ステートメントをサポートします。 {#sql-binding-supports-the-code-insert-code-code-replace-code-code-update-code-code-delete-code-statements}

パフォーマンスのチューニングやデータベースのメンテナンスを行う際に、実行プランが不安定なためにシステムのパフォーマンスが不安定になっていることが判明した場合は、ユーザーの判断や`EXPLAIN ANALYZE`でテストした SQL 文を手動で最適化して選択することができます。最適化された SQL 文をアプリケーション コードで実行する SQL 文にバインドすることで、安定したパフォーマンスを確保できます。

SQL BINDING ステートメントを使用して SQL ステートメントを手動でバインドする場合は、最適化された SQL ステートメントの構文が元の SQL ステートメントと同じであることを確認する必要があります。

`SHOW {GLOBAL | SESSION} BINDINGS`コマンドを実行すると、手動または自動でバインドされた実行プラン情報を表示できます。出力は、v5.0 より前のバージョンと同じです。

#### 実行プランを自動的にキャプチャしてバインドする {#automatically-capture-and-bind-execution-plans}

TiDB をアップグレードする場合、パフォーマンスのジッターを回避するために、ベースライン キャプチャ機能を有効にして、システムが最新の実行プランを自動的にキャプチャしてバインドし、システム テーブルに保存できるようにします。TiDB をアップグレードした後、 `SHOW GLOBAL BINDING`コマンドを実行してバインドされた実行プランをエクスポートし、これらのプランを削除するかどうかを決定できます。

この機能はデフォルトでは無効になっています。サーバーを変更するか、 `tidb_capture_plan_baselines`グローバル システム変数を`ON`に設定することで有効にできます。この機能を有効にすると、システムは`bind-info-lease`回 (デフォルト値は`3s` ) ごとにステートメント サマリーから少なくとも 2 回表示される SQL ステートメントを取得し、これらの SQL ステートメントを自動的にキャプチャしてバインドします。

### TiFlashクエリの安定性を向上 {#improve-stability-of-tiflash-queries}

TiFlash が失敗した場合に TiKV にクエリをフォールバックするためのシステム変数[`tidb_allow_fallback_to_tikv`](/system-variables.md#tidb_allow_fallback_to_tikv-new-in-v50)を追加します。デフォルト値は`OFF`です。

### TiCDC の安定性を改善し、増分データの複製が多すぎることによる OOM の問題を軽減します。 {#improve-ticdc-stability-and-alleviate-the-oom-issue-caused-by-replicating-too-much-incremental-data}

[ユーザードキュメント](/ticdc/ticdc-manage-changefeed.md#unified-sorter) , [＃1150](https://github.com/pingcap/tiflow/issues/1150)

TiCDC v4.0.9 以前のバージョンでは、データ変更を過度に複製すると OOM が発生する可能性があります。v5.0 では、次のシナリオによって発生する OOM の問題を軽減するために、Unified Sorter 機能がデフォルトで有効になっています。

-   TiCDC のデータ複製タスクは長時間一時停止され、その間に大量の増分データが蓄積され、複製が必要になります。
-   データ複製タスクは早いタイムスタンプから開始されるため、大量の増分データを複製する必要が生じます。

Unified Sorter は`file`以前のバージョンの`memory`ソート エンジン オプションと統合されています。変更を手動で構成する必要はありません。

制限事項:

-   増分データの量に応じて十分なディスク容量を用意する必要があります。空き容量が 128 GB を超える SSD を使用することをお勧めします。

## 高可用性と災害復旧 {#high-availability-and-disaster-recovery}

### リージョンメンバーシップの変更時のシステム可用性の向上 {#improve-system-availability-during-region-membership-change}

[ユーザードキュメント](/pd-configuration-file.md#enable-joint-consensus-new-in-v50) [＃18079](https://github.com/pingcap/tidb/issues/18079) [＃7587](https://github.com/tikv/tikv/issues/7587) [＃2860](https://github.com/tikv/pd/issues/2860)

リージョンメンバーシップの変更プロセスでは、「メンバーの追加」と「メンバーの削除」という 2 つの操作が 2 つのステップで実行されます。メンバーシップの変更が完了したときに障害が発生すると、リージョンが使用できなくなり、フォアグラウンド アプリケーションのエラーが返されます。

導入されたRaft Joint Consensus アルゴリズムにより、リージョンメンバーシップの変更時のシステムの可用性が向上します。メンバーシップの変更時の「メンバーの追加」と「メンバーの削除」の操作は 1 つの操作に結合され、すべてのメンバーに送信されます。変更プロセス中、リージョンは中間状態にあります。変更されたメンバーのいずれかに障害が発生した場合でも、システムは引き続き利用可能です。

この機能はデフォルトで有効になっています。 `pd-ctl config set enable-joint-consensus`コマンドを実行して`enable-joint-consensus`値を`false`に設定することで無効にできます。

### メモリ管理モジュールを最適化してシステムOOMのリスクを軽減する {#optimize-the-memory-management-module-to-reduce-system-oom-risks}

集計関数のメモリ使用量を追跡します。この機能はデフォルトで有効になっています。集計関数を含む SQL 文が実行されると、現在のクエリの合計メモリ使用量が`mem-quota-query`で設定されたしきい値を超えると、システムは`oom-action`で定義された操作を自動的に実行します。

### ネットワーク分割時のシステム可用性の向上 {#improve-the-system-availability-during-network-partition}

## データ移行 {#data-migration}

### S3/ Auroraから TiDB へのデータの移行 {#migrate-data-from-s3-aurora-to-tidb}

TiDB データ移行ツールは、Amazon S3 (およびその他の S3 互換storageサービス) をデータ移行の中間として使用し、 Auroraスナップショット データを TiDB に直接初期化することをサポートしており、Amazon S3/ Auroraから TiDB にデータを移行するためのオプションがさらに増えています。

この機能を使用するには、次のドキュメントを参照してください。

-   [Amazon S3クラウドstorageにデータをエクスポートする](/dumpling-overview.md#export-data-to-amazon-s3-cloud-storage) , [＃8](https://github.com/pingcap/dumpling/issues/8)
-   [TiDB Lightning を使用して Amazon Aurora MySQL から移行する](/migrate-aurora-to-tidb.md) , [＃266](https://github.com/pingcap/tidb-lightning/issues/266)

### TiDB Cloudのデータインポートパフォーマンスを最適化 {#optimize-the-data-import-performance-of-tidb-cloud}

TiDB Lightning は、特にTiDB Cloudの AWS T1.standard 構成 (または同等) 向けにデータ インポート パフォーマンスを最適化します。テスト結果によると、 TiDB Lightningにより、1 TB の TPC-C データを TiDB にインポートする速度が 254 GiB/h から 366 GiB/h に 40% 向上しました。

## データの共有とサブスクリプション {#data-sharing-and-subscription}

### TiCDC を使用して TiDB を Kafka Connect (Confluent Platform) に統合する (<strong>実験的機能</strong>) {#integrate-tidb-to-kafka-connect-confluent-platform-using-ticdc-strong-experimental-feature-strong}

[ユーザードキュメント](/ticdc/integrate-confluent-using-ticdc.md) , [＃660](https://github.com/pingcap/tiflow/issues/660)

この機能により、TiDB データを他のシステムにストリーミングするというビジネス要件をサポートするために、TiDB データを Kafka、Hadoop、Oracle などのシステムにストリーミングできるようになります。

Confluent プラットフォームが提供する Kafka コネクタ プロトコルはコミュニティで広く使用されており、さまざまなプロトコルでリレーショナル データベースまたは非リレーショナル データベースへのデータ転送をサポートしています。TiCDC を Confluent プラットフォームの Kafka Connect に統合することで、TiDB は TiDB データを他の異種データベースまたはシステムにストリーミングする機能を拡張します。

## 診断 {#diagnostics}

[ユーザードキュメント](/sql-statements/sql-statement-explain.md#explain)

SQL パフォーマンスの問題のトラブルシューティングでは、パフォーマンスの問題の原因を特定するために詳細な診断情報が必要です。TiDB 5.0 より前では、 `EXPLAIN`ステートメントによって収集された情報は十分に詳細ではありませんでした。問題の根本原因は、ログ情報、監視情報、または推測に基づいてのみ特定できるため、非効率的である可能性があります。

TiDB v5.0 では、パフォーマンスの問題をより効率的にトラブルシューティングできるように、次の改善が加えられています。

-   `EXPLAIN ANALYZE`ステートメントを使用してすべての DML ステートメントを分析し、実際のパフォーマンス プランと各演算子の実行情報を表示することをサポートします[＃18056](https://github.com/pingcap/tidb/issues/18056)
-   `EXPLAIN FOR CONNECTION`ステートメントを使用して、実行中のすべての SQL ステートメントのリアルタイムステータスを確認することをサポートします。たとえば、ステートメントを使用して、各演算子の実行時間や処理された行数を確認できます[＃18233](https://github.com/pingcap/tidb/issues/18233)
-   `EXPLAIN ANALYZE`ステートメントの出力で、オペレータによって送信された RPC 要求の数、ロック競合の解決にかかる時間、ネットワークレイテンシー、RocksDB でスキャンされた削除済みデータの量、RocksDB キャッシュのヒット率など、オペレータの実行に関する詳細情報を提供します[＃18663](https://github.com/pingcap/tidb/issues/18663)
-   SQL 文の詳細な実行情報をスロー ログに自動的に記録する機能をサポートします。スロー ログ内の実行情報は、各演算子の消費時間、処理された行数、送信された RPC 要求の数など、 `EXPLAIN ANALYZE`文の出力情報と一致します[＃15009](https://github.com/pingcap/tidb/issues/15009)

## 導入とメンテナンス {#deployment-and-maintenance}

### クラスタ展開操作のロジックを最適化し、DBAが標準のTiDB本番クラスタのセットをより迅速に展開できるようにします。 {#optimize-the-logic-of-cluster-deployment-operations-to-help-dbas-deploy-a-set-of-standard-tidb-production-cluster-faster}

[ユーザードキュメント](/production-deployment-using-tiup.md)

以前のバージョンの TiDB では、 TiUP を使用して TiDB クラスターを展開する DBA は、環境の初期化が複雑で、チェックサム構成が過剰で、クラスター トポロジ ファイルの編集が難しいことに気付きました。これらの問題はすべて、DBA の展開効率の低下につながります。TiDB v5.0 では、次の項目により、 TiUP を使用した TiDB 展開の DBA の効率が向上しています。

-   TiUP クラスタ は、より包括的なワンクリック環境チェックを実行し、修復の推奨事項を提供する`check topo.yaml`コマンドをサポートしています。
-   TiUP クラスタ は、環境チェック中に検出された環境の問題を自動的に修復する`check topo.yaml --apply`コマンドをサポートしています。
-   TiUP クラスタ は、DBA が編集してグローバル ノード パラメータの変更をサポートするためのクラスター トポロジ テンプレート ファイルを取得する`template`コマンドをサポートしています。
-   TiUP は、リモート Prometheus を構成するために`edit-config`コマンドを使用して`remote_config`パラメータを編集することをサポートしています。
-   TiUP は、 `edit-config`コマンドを使用してさまざまな AlertManager を構成するために`external_alertmanagers`パラメータを編集することをサポートしています。
-   tiup-clusterの`edit-config`サブコマンドを使用してトポロジ ファイルを編集するときに、構成項目の値のデータ型を変更できます。

### アップグレードの安定性を向上 {#improve-upgrade-stability}

TiUP v1.4.0 より前では、 tiup-cluster を使用して TiDB クラスターをアップグレードすると、クラスターの SQL 応答が長時間にわたってジッタし、PD オンライン ローリング アップグレード中は、クラスターの QPS が 10 秒から 30 秒の間ジッタします。

TiUP v1.4.0 ではロジックが調整され、次の最適化が行われます。

-   PD ノードのアップグレード中、 TiUP は再起動された PD ノードのステータスを自動的にチェックし、ステータスが準備完了であることを確認した後、次の PD ノードのアップグレードをロールします。
-   TiUP はPD ロールを自動的に識別し、最初にフォロワー ロールの PD ノードをアップグレードし、最後に PDLeaderノードをアップグレードします。

### アップグレード時間を最適化する {#optimize-the-upgrade-time}

TiUP v1.4.0 より前では、DBA がtiup-clusterを使用して TiDB クラスターをアップグレードする場合、多数のノードを持つクラスターでは合計アップグレード時間が長くなり、特定のユーザーのアップグレード時間枠の要件を満たすことができません。

v1.4.0 以降、 TiUP は次の項目を最適化します。

-   `tiup cluster upgrade --offline`サブコマンドを使用した高速オフライン アップグレードをサポートします。
-   デフォルトで、アップグレード中にローリング アップグレードを使用するユーザーのリージョンLeaderの再配置が高速化されるため、ローリング TiKV アップグレードの時間が短縮されます。
-   ローリング アップグレードを実行する前に、 `check`サブコマンドを使用してリージョンモニターのステータスを確認します。アップグレード前にクラスターが正常な状態であることを確認し、アップグレードが失敗する可能性を減らします。

### ブレークポイント機能をサポートする {#support-the-breakpoint-feature}

TiUP v1.4.0 より前では、DBA がtiup-cluster を使用して TiDB クラスターをアップグレードするときに、コマンドの実行が中断されると、すべてのアップグレード操作を最初から再度実行する必要がありました。

TiUP v1.4.0 では、アップグレードの中断後にすべての操作が再実行されるのを回避するために、 tiup-cluster `replay`サブコマンドを使用してブレークポイントから失敗した操作を再試行することがサポートされています。

### 保守・運用機能の強化 {#enhance-the-functionalities-of-maintenance-and-operations}

TiUP v1.4.0 では、TiDB クラスターの操作と保守の機能がさらに強化されています。

-   より多くの使用シナリオに適応するために、ダウンタイム TiDB および DM クラスターでのアップグレードまたはパッチ操作をサポートします。
-   クラスターのバージョンを取得するために、 tiup-clusterの`display`サブコマンドに`--version`パラメータを追加します。
-   スケールアウトするノードに Prometheus のみが含まれている場合、Prometheus ノードの不在によるスケールアウトの失敗を回避するために、監視構成の更新操作は実行されません。
-   入力されたTiUPコマンドの結果が正しくない場合に、エラー メッセージにユーザー入力を追加して、問題の原因をより迅速に特定できるようにします。

## テレメトリー {#telemetry}

TiDB は、データ テーブルの数、クエリの数、新しい機能が有効になっているかどうかなど、テレメトリにクラスター使用状況メトリックを追加します。

この動作の詳細と無効にする方法については、 [テレメトリー](/telemetry.md)を参照してください。
