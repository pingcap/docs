---
title: What's New in TiDB 5.0
---

# TiDB 5.0 の新機能 {#what-s-new-in-tidb-5-0}

発売日：2021年4月7日

TiDB バージョン: 5.0.0

v5.0 では、PingCAP は、企業が TiDB に基づいてアプリケーションを迅速に構築できるよう支援することに専念しており、データベースのパフォーマンス、パフォーマンスのジッター、セキュリティ、高可用性、災害復旧、SQL パフォーマンスのトラブルシューティングなどに関する心配から解放されます。

v5.0 の主な新機能または改善点は次のとおりです。

-   TiFlashノードを介して超並列処理 (MPP)アーキテクチャを導入します。これにより、 TiFlashノード間で大規模な結合クエリの実行ワークロードが共有されます。 MPP モードが有効になっている場合、TiDB は、コストに基づいて、MPP フレームワークを使用して計算を実行するかどうかを決定します。 MPP モードでは、計算中に結合キーが`Exchange`の操作で再配布されるため、各TiFlashノードに計算負荷が分散され、計算が高速化されます。ベンチマークによると、同じクラスター リソースで、TiDB 5.0 MPP は Greenplum 6.15.0 および Apache Spark 3.1.1 よりも 2 倍から 3 倍の速度向上を示し、一部のクエリは 8 倍のパフォーマンスを示します。
-   クラスター化インデックス機能を導入して、データベースのパフォーマンスを向上させます。たとえば、TPC-C tpmC テストでは、クラスター化インデックスが有効になっている TiDB のパフォーマンスが 39% 向上しています。
-   非同期コミット機能を有効にして、書き込みレイテンシーを短縮します。たとえば、64 スレッドの Sysbench テストでは、非同期コミットを有効にしたインデックス更新の平均レイテンシーは、12.04 ミリ秒から 7.01 ミリ秒に 41.7% 短縮されました。
-   ジッターを減らします。これは、オプティマイザの安定性を向上させ、システム タスクによる I/O、ネットワーク、CPU、およびメモリリソースの使用を制限することによって実現されます。たとえば、8 時間のパフォーマンス テストでは、TPC-C tpmC の標準偏差は 2% を超えません。
-   スケジューリングを改善し、実行計画を可能な限り安定させて、システムの安定性を高めます。
-   Raft Joint Consensus アルゴリズムを導入し、リージョンメンバーシップの変更中にシステムの可用性を確保します。
-   データベース管理者 (DBA) が SQL ステートメントをより効率的にデバッグするのに役立つ最適化`EXPLAIN`機能と非表示のインデックス。
-   企業データの信頼性を保証します。 TiDB から Amazon S3storageおよび Google Cloud GCS にデータをバックアップしたり、これらのクラウドstorageプラットフォームからデータを復元したりできます。
-   Amazon S3storageまたは TiDB/MySQL からのデータ インポートまたはデータ エクスポートのパフォーマンスを向上させ、企業がクラウド上でアプリケーションを迅速に構築するのに役立ちます。たとえば、TPC-C テストでは、1 TiB のデータをインポートするパフォーマンスが 254 GiB/h から 366 GiB/h に 40% 向上します。

## 互換性の変更 {#compatibility-changes}

### システム変数 {#system-variables}

-   [`tidb_executor_concurrency`](/system-variables.md#tidb_executor_concurrency-new-in-v50)システム変数を追加して、複数のオペレーターの同時実行を制御します。前の`tidb_*_concurrency`設定 ( `tidb_projection_concurrency`など) は引き続き有効ですが、使用すると警告が表示されます。

-   [`tidb_skip_ascii_check`](/system-variables.md#tidb_skip_ascii_check-new-in-v50)システム変数を追加して、ASCII 文字セットが書き込まれるときに ASCII 検証チェックをスキップするかどうかを指定します。このデフォルト値は`OFF`です。

-   [`tidb_enable_strict_double_type_check`](/system-variables.md#tidb_enable_strict_double_type_check-new-in-v50)システム変数を追加して、 `double(N)`のような構文をテーブル スキーマで定義できるかどうかを判断します。このデフォルト値は`OFF`です。

-   デフォルト値の[`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size)を`20000`から`0`に変更します。これは、バッチ DML ステートメントが`LOAD`ではデフォルトで使用されなくなったことを意味し`INSERT INTO SELECT ...` 。代わりに、厳密なACIDセマンティクスに準拠するために大規模なトランザクションが使用されます。

    > **ノート：**
    >
    > 変数のスコープがセッションからグローバルに変更され、デフォルト値が`20000`から`0`に変更されました。アプリケーションが元のデフォルト値に依存している場合は、 `set global`ステートメントを使用して、アップグレード後に変数を元の値に変更する必要があります。

-   [`tidb_enable_noop_functions`](/system-variables.md#tidb_enable_noop_functions-new-in-v40)システム変数を使用して、一時テーブルの構文の互換性を制御します。この変数値が`OFF`の場合、 `CREATE TEMPORARY TABLE`構文はエラーを返します。

-   次のシステム変数を追加して、ガベージコレクション関連のパラメーターを直接制御します。
    -   [`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-new-in-v50)
    -   [`tidb_gc_enable`](/system-variables.md#tidb_gc_enable-new-in-v50)
    -   [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)
    -   [`tidb_gc_run_interval`](/system-variables.md#tidb_gc_run_interval-new-in-v50)
    -   [`tidb_gc_scan_lock_mode`](/system-variables.md#tidb_gc_scan_lock_mode-new-in-v50)

-   デフォルト値の[`enable-joint-consensus`](/pd-configuration-file.md#enable-joint-consensus-new-in-v50) `false`から`true`に変更します。これにより、ジョイント コンセンサス機能がデフォルトで有効になります。

-   [`tidb_enable_amend_pessimistic_txn`](/system-variables.md#tidb_enable_amend_pessimistic_txn-new-in-v407)の値を`0`または`1`から`ON`または`OFF`に変更します。

-   次の新しい意味で、デフォルト値の[`tidb_enable_clustered_index`](/system-variables.md#tidb_enable_clustered_index-new-in-v50)を`OFF`から`INT_ONLY`に変更します。
    -   `ON` : クラスター化インデックスが有効です。非クラスター化インデックスの追加または削除がサポートされています。

    -   `OFF` : クラスター化インデックスは無効です。非クラスター化インデックスの追加または削除がサポートされています。

    -   `INT_ONLY` : デフォルト値。この動作は、v5.0 より前の動作と一致しています。 `alter-primary-key = false`と共に INT 型のクラスター化インデックスを有効にするかどうかを制御できます。
    > **ノート：**
    >
    > 5.0 GA の`INT_ONLY`値`tidb_enable_clustered_index` 5.0 RC の`OFF`値と同じ意味を持ちます。 `OFF`設定の 5.0 RC クラスターから 5.0 GA にアップグレードすると、 `INT_ONLY`と表示されます。

### コンフィグレーションファイルのパラメーター {#configuration-file-parameters}

-   TiDB の構成項目を[`index-limit`](/tidb-configuration-file.md#index-limit-new-in-v50)追加します。その値のデフォルトは`64`で、範囲は`[64,512]`です。 MySQL テーブルは最大 64 個のインデックスをサポートします。その値がデフォルト設定を超え、テーブルに対して 64 を超えるインデックスが作成された場合、テーブル スキーマが MySQL に再インポートされると、エラーが報告されます。
-   TiDB の構成項目を[`enable-enum-length-limit`](/tidb-configuration-file.md#enable-enum-length-limit-new-in-v50)追加して、MySQL の ENUM/SET の長さと互換性を保ち、一貫性を持たせます (ENUM の長さ &lt; 255)。デフォルト値は`true`です。
-   `pessimistic-txn.enable`構成項目を[`tidb_txn_mode`](/system-variables.md#tidb_txn_mode)環境変数に置き換えます。
-   `performance.max-memory`構成アイテムを[`performance.server-memory-quota`](/tidb-configuration-file.md#server-memory-quota-new-in-v409)に置き換えます
-   `tikv-client.copr-cache.enable`構成アイテムを[`tikv-client.copr-cache.capacity-mb`](/tidb-configuration-file.md#capacity-mb)に置き換えます。項目の値が`0.0`の場合、この機能は無効になっています。アイテムの値が`0.0`より大きい場合、この機能は有効になります。デフォルト値は`1000.0`です。
-   `rocksdb.auto-tuned`構成アイテムを[`rocksdb.rate-limiter-auto-tuned`](/tikv-configuration-file.md#rate-limiter-auto-tuned-new-in-v50)に置き換えます。
-   `raftstore.sync-log`構成アイテムを削除します。デフォルトでは、書き込まれたデータは強制的にディスクにスピルされます。 v5.0 より前では、明示的に`raftstore.sync-log`を無効にすることができます。 v5.0 以降、構成値は強制的に`true`に設定されます。
-   `gc.enable-compaction-filter`構成アイテムのデフォルト値を`false`から`true`に変更します。
-   `enable-cross-table-merge`構成アイテムのデフォルト値を`false`から`true`に変更します。
-   [`rate-limiter-auto-tuned`](/tikv-configuration-file.md#rate-limiter-auto-tuned-new-in-v50)構成アイテムのデフォルト値を`false`から`true`に変更します。

### その他 {#others}

-   アップグレードの前に、TiDB 構成の値を確認してください[`feedback-probability`](https://docs.pingcap.com/tidb/v5.0/tidb-configuration-file#feedback-probability) 。値が 0 でない場合、アップグレード後に「回復可能なゴルーチンでpanic」エラーが発生しますが、このエラーはアップグレードには影響しません。
-   データの正確性の問題を回避するために、列の型の変更中に`VARCHAR`型と`CHAR`型の間の変換を禁止します。

## 新機能 {#new-features}

### SQL {#sql}

#### List パーティショニング(<strong>Experimental</strong>) {#list-partitioning-strong-experimental-strong}

[ユーザー文書](/partitioned-table.md#list-partitioning)

リスト パーティショニング機能を使用すると、大量のデータを含むテーブルを効果的にクエリおよび維持できます。

この機能を有効にすると、パーティションとパーティション間でのデータの分散方法が`PARTITION BY LIST(expr) PARTITION part_name VALUES IN (...)`式に従って定義されます。分割されたテーブルのデータ セットは、最大 1024 の個別の整数値をサポートします。 `PARTITION ... VALUES IN (...)`句を使用して値を定義できます。

リスト パーティショニングを有効にするには、セッション変数[`tidb_enable_list_partition`](/system-variables.md#tidb_enable_list_partition-new-in-v50)を`ON`に設定します。

#### List COLUMNS パーティショニング(<strong>Experimental</strong>) {#list-columns-partitioning-strong-experimental-strong}

[ユーザー文書](/partitioned-table.md#list-columns-partitioning)

List COLUMNS パーティショニングは、リスト パーティショニングの一種です。複数の列をパーティション キーとして使用できます。整数データ型のほかに、string、 `DATE` 、および`DATETIME`データ型の列をパーティション列として使用することもできます。

List COLUMNS パーティショニングを有効にするには、セッション変数を[`tidb_enable_list_partition`](/system-variables.md#tidb_enable_list_partition-new-in-v50)から`ON`に設定します。

#### 見えないインデックス {#invisible-indexes}

[ユーザー文書](/sql-statements/sql-statement-alter-index.md) 、 [#9246](https://github.com/pingcap/tidb/issues/9246)

パフォーマンスを調整するとき、または最適なインデックスを選択するときに、SQL ステートメントを使用してインデックスを`Visible`または`Invisible`に設定できます。この設定により、リソースを消費する操作 ( `DROP INDEX`や`ADD INDEX`など) の実行を回避できます。

インデックスの可視性を変更するには、 `ALTER INDEX`ステートメントを使用します。変更後、オプティマイザーは、インデックスの可視性に基づいて、このインデックスをインデックス リストに追加するかどうかを決定します。

#### <code>EXCEPT</code>および<code>INTERSECT</code>演算子 {#code-except-code-and-code-intersect-code-operators}

[ユーザー文書](/functions-and-operators/set-operators.md) 、 [#18031](https://github.com/pingcap/tidb/issues/18031)

`INTERSECT`演算子は集合演算子であり、2 つ以上のクエリの結果セットの共通部分を返します。ある程度、これは`Inner Join`演算子の代わりになります。

`EXCEPT`演算子はセット演算子で、2 つのクエリの結果セットを結合し、最初のクエリ結果には含まれるが 2 番目のクエリ結果には含まれない要素を返します。

### トランザクション {#transaction}

[ユーザー文書](/system-variables.md#tidb_enable_amend_pessimistic_txn-new-in-v407) 、 [#18005](https://github.com/pingcap/tidb/issues/18005)

悲観的トランザクション モードでは、トランザクションに関連するテーブルに同時 DDL 操作または`SCHEMA VERSION`変更が含まれている場合、システムはトランザクションの`SCHEMA VERSION`を最新のものに自動的に更新して、トランザクションのコミットが成功するようにし、クライアントが`Information schema is changed`エラーを受け取るのを回避します。トランザクションは、DDL 操作または`SCHEMA VERSION`の変更によって中断されます。

この機能はデフォルトで無効になっています。この機能を有効にするには、 [`tidb_enable_amend_pessimistic_txn`](/system-variables.md#tidb_enable_amend_pessimistic_txn-new-in-v407)のシステム変数の値を変更します。この機能は v4.0.7 で導入され、v5.0 で次の問題が修正されています。

-   TiDB Binlog が`Add Column`操作を実行するときに発生する互換性の問題
-   この機能を一意のインデックスと一緒に使用するときに発生するデータの不整合の問題
-   追加されたインデックスと一緒に機能を使用するときに発生するデータの不整合の問題

現在、この機能にはまだ次の非互換性の問題があります。

-   同時トランザクションがある場合、トランザクションのセマンティクスが変わる可能性があります
-   この機能を TiDB Binlogと一緒に使用する場合に発生する既知の互換性の問題
-   `Change Column`との非互換性

### 文字セットと照合順序 {#character-set-and-collation}

-   `utf8mb4_unicode_ci`および`utf8_unicode_ci`照合をサポートします。 [ユーザー文書](/character-set-and-collation.md#new-framework-for-collations) , [#17596](https://github.com/pingcap/tidb/issues/17596)
-   照合順序で大文字と小文字を区別しない比較並べ替えをサポートする

### Security {#security}

[ユーザー文書](/log-redaction.md) 、 [#18566](https://github.com/pingcap/tidb/issues/18566)

セキュリティ コンプライアンス要件 (*一般データ保護規則*(GDPR) など) を満たすために、システムは、出力エラー メッセージとログで情報 (ID やクレジット カード番号など) の感度を下げることをサポートしています。これにより、機密情報の漏洩を防ぐことができます。

TiDB は、出力ログ情報の感度を下げることをサポートしています。この機能を有効にするには、次のスイッチを使用します。

-   グローバル変数[`tidb_redact_log`](/system-variables.md#tidb_redact_log) .デフォルト値は`0`で、感度低下が無効になっていることを意味します。 tidb-server ログの感度低下を有効にするには、変数の値を`1`に設定します。
-   設定項目`security.redact-info-log` ．デフォルト値は`false`で、感度低下が無効になっていることを意味します。 tikv-server ログの感度低下を有効にするには、変数の値を`true`に設定します。
-   設定項目`security.redact-info-log` ．デフォルト値は`false`で、感度低下が無効になっていることを意味します。 pd-server ログの感度低下を有効にするには、変数の値を`true`に設定します。
-   tiflash-server の設定項目`security.redact_info_log`と tiflash-learner の設定項目`security.redact-info-log` 。デフォルト値はどちらも`false`で、感度低下が無効になっていることを意味します。 tiflash-server および tiflash-learner ログの感度低下を有効にするには、両方の変数の値を`true`に設定します。

この機能は v5.0 で導入されました。この機能を使用するには、システム変数と上記のすべての構成項目を有効にします。

## パフォーマンスの最適化 {#performance-optimization}

### MPPアーキテクチャ {#mpp-architecture}

[ユーザー文書](/tiflash/use-tiflash-mpp-mode.md)

TiDB は、 TiFlashノードを通じて MPPアーキテクチャを導入します。このアーキテクチャ、複数のTiFlashノードが大規模な結合クエリの実行ワークロードを共有できます。

MPP モードがオンの場合、TiDB は、計算コストに基づいて、計算のためにクエリを MPP エンジンに送信するかどうかを決定します。 MPP モードでは、TiDB はデータ計算 ( `Exchange`操作) 中に結合キーを再配布することにより、実行中の各TiFlashノードにテーブル結合の計算を分散し、計算を高速化します。さらに、 TiFlashがすでにサポートしているアグリゲーション コンピューティング機能を使用して、TiDB はクエリの計算をTiFlash MPP クラスターにプッシュダウンできます。次に、分散環境は、実行プロセス全体を高速化し、分析クエリの速度を劇的に向上させるのに役立ちます。

TPC-H 100 ベンチマーク テストでは、 TiFlash MPP は、従来の分析データベースの分析エンジンや Hadoop 上の SQL よりも大幅な処理速度を実現しています。このアーキテクチャにより、大規模な分析クエリを最新のトランザクション データに対して直接実行でき、従来のオフライン分析ソリューションよりも高いパフォーマンスを実現できます。ベンチマークによると、同じクラスター リソースで、TiDB 5.0 MPP は Greenplum 6.15.0 および Apache Spark 3.1.1 よりも 2 倍から 3 倍の速度向上を示し、一部のクエリは 8 倍のパフォーマンスを示します。

現在、MPP モードがサポートしていない主な機能は次のとおりです (詳細については、 [TiFlashを使用する](/tiflash/use-tiflash-mpp-mode.md)を参照してください)。

-   テーブルの分割
-   ウィンドウ関数
-   照合
-   一部の組み込み関数
-   TiKV からのデータの読み取り
-   OOM流出
-   連合
-   完全外部結合

### クラスタ化されたインデックス {#clustered-index}

[ユーザー文書](/clustered-indexes.md) 、 [#4841](https://github.com/pingcap/tidb/issues/4841)

テーブル構造を設計したり、データベースの動作を分析したりするときに、主キーを持つ一部の列がグループ化およびソートされることが多く、これらの列に対するクエリが特定の範囲のデータまたは少量のデータを返すことが多い場合は、クラスター化インデックス機能を使用することをお勧めします。値が異なるデータの場合、対応するデータによって読み取りまたは書き込みのホットスポットの問題が発生することはありません。

一部のデータベース管理システムでは*インデックス構成テーブル*とも呼ばれるクラスター化インデックスは、テーブルのデータに関連付けられたstorage構造です。クラスター化インデックスを作成するときは、テーブルから 1 つ以上の列をインデックスのキーとして指定できます。 TiDB はこれらのキーを特定の構造に格納します。これにより、TiDB はキーに関連付けられた行を迅速かつ効率的に見つけることができるため、データのクエリと書き込みのパフォーマンスが向上します。

クラスター化インデックス機能を有効にすると、次の場合に TiDB のパフォーマンスが大幅に向上します (たとえば、TPC-C tpmC テストでは、クラスター化インデックスを有効にした TiDB のパフォーマンスが 39% 向上します)。

-   データが挿入されると、クラスター化インデックスは、ネットワークからのインデックス データの 1 回の書き込みを減らします。
-   同等の条件を持つクエリに主キーのみが含まれる場合、クラスター化インデックスは、ネットワークからのインデックス データの 1 回の読み取りを減らします。
-   範囲条件を含むクエリに主キーのみが含まれる場合、クラスター化インデックスにより、ネットワークからのインデックス データの複数回の読み取りが削減されます。
-   同等または範囲条件を含むクエリに主キー プレフィックスが含まれる場合、クラスター化インデックスは、ネットワークからのインデックス データの複数回の読み取りを減らします。

各テーブルは、クラスター化インデックスまたは非クラスター化インデックスのいずれかを使用して、データを並べ替えて格納できます。これら 2 つのstorage構造の違いは次のとおりです。

-   クラスター化インデックスを作成する場合、テーブル内の 1 つ以上の列をインデックスのキー値として指定できます。クラスター化インデックスは、キー値に従ってテーブルのデータを並べ替えて格納します。各テーブルは、クラスター化インデックスを 1 つだけ持つことができます。テーブルにクラスター化インデックスがある場合、それはクラスター化インデックス テーブルと呼ばれます。それ以外の場合は、非クラスター化インデックス テーブルと呼ばれます。
-   非クラスター化インデックスを作成すると、テーブル内のデータは順不同の構造で格納されます。 TiDB は一意の ROWID をデータの各行に自動的に割り当てるため、非クラスター化インデックスのキー値を明示的に指定する必要はありません。クエリ中、ROWID は対応する行を見つけるために使用されます。データのクエリまたは挿入時に少なくとも 2 つのネットワーク I/O 操作があるため、クラスター化インデックスと比較してパフォーマンスが低下します。

テーブル データが変更されると、データベース システムはクラスター化インデックスと非クラスター化インデックスを自動的に維持します。

デフォルトでは、すべての主キーは非クラスター化インデックスとして作成されます。次の 2 つの方法のいずれかで、主キーをクラスター化インデックスまたは非クラスター化インデックスとして作成できます。

-   テーブルを作成するときにステートメントにキーワード`CLUSTERED | NONCLUSTERED`を指定すると、システムは指定された方法でテーブルを作成します。構文は次のとおりです。

```sql
CREATE TABLE `t` (`a` VARCHAR(255), `b` INT, PRIMARY KEY (`a`, `b`) CLUSTERED);
```

また

```sql
CREATE TABLE `t` (`a` VARCHAR(255) PRIMARY KEY CLUSTERED, `b` INT);
```

ステートメント`SHOW INDEX FROM tbl-name`を実行して、テーブルにクラスター化インデックスがあるかどうかを照会できます。

-   クラスター化インデックス機能を制御するには、システム変数`tidb_enable_clustered_index`を構成します。サポートされている値は`ON` 、 `OFF` 、および`INT_ONLY`です。
    -   `ON` : すべての種類の主キーに対してクラスター化インデックス機能が有効になっていることを示します。非クラスター化インデックスの追加と削除がサポートされています。
    -   `OFF` : すべての種類の主キーに対してクラスター化インデックス機能が無効になっていることを示します。非クラスター化インデックスの追加と削除がサポートされています。
    -   `INT_ONLY` : デフォルト値。変数が`INT_ONLY`に設定され、 `alter-primary-key` `false`に設定されている場合、デフォルトでは、単一の整数列で構成される主キーがクラスター化インデックスとして作成されます。この動作は、TiDB v5.0 以前のバージョンの動作と一致しています。

`CREATE TABLE`ステートメントにキーワード`CLUSTERED | NONCLUSTERED`含まれている場合、ステートメントはシステム変数と構成アイテムの構成をオーバーライドします。

ステートメントでキーワード`CLUSTERED | NONCLUSTERED`を指定して、クラスター化インデックス機能を使用することをお勧めします。このようにして、TiDB が必要に応じて同時にシステム内のクラスター化および非クラスター化インデックスのすべてのデータ型を使用することがより柔軟になります。

`tidb_enable_clustered_index = INT_ONLY`使用はお勧めしません。3 はこの機能の互換性を保つために一時的に使用されており、将来的に`INT_ONLY`非推奨になるためです。

クラスター化インデックスの制限は次のとおりです。

-   クラスター化インデックスと非クラスター化インデックス間の相互変換はサポートされていません。
-   クラスター化インデックスの削除はサポートされていません。
-   `ALTER TABLE`ステートメントを使用したクラスター化インデックスの追加、削除、および変更はサポートされていません。
-   クラスター化インデックスの再編成と再作成はサポートされていません。
-   インデックスの有効化または無効化はサポートされていません。つまり、インデックスの非表示機能は、クラスター化されたインデックスに対して有効ではありません。
-   クラスター化インデックスとして`UNIQUE KEY`を作成することはサポートされていません。
-   クラスター化インデックス機能を TiDB Binlogと一緒に使用することはサポートされていません。 TiDB Binlogを有効にすると、TiDB はクラスター化インデックスとして単一の整数主キーの作成のみをサポートします。 TiDB Binlog は、クラスター化されたインデックスを持つ既存のテーブルのデータ変更をダウンストリームに複製しません。
-   クラスター化インデックス機能を属性`SHARD_ROW_ID_BITS`および`PRE_SPLIT_REGIONS`と共に使用することはサポートされていません。
-   クラスターを新しいバージョンにアップグレードしてからロールバックする場合は、ロールバックの前にテーブル データをエクスポートし、ロールバック後にデータをインポートして、新しく追加されたテーブルをダウングレードする必要があります。他のテーブルは影響を受けません。

### 非同期コミット {#async-commit}

[ユーザー文書](/system-variables.md#tidb_enable_async_commit-new-in-v50) 、 [#8316](https://github.com/tikv/tikv/issues/8316)

データベースのクライアントは、データベース システムがトランザクション コミットを 2 フェーズ (2PC) で同期的に完了するまで待機します。トランザクションは、第 1 フェーズのコミットが成功した後にクライアントに結果を返し、システムは第 2 フェーズのコミット操作をバックグラウンドで非同期的に実行して、トランザクション コミットのレイテンシーを短縮します。トランザクション書き込みに含まれるリージョン が1 つだけの場合、2 番目のフェーズは直接省略され、トランザクションは 1 フェーズ コミットになります。

Async Commit 機能を有効にした後、同じハードウェアと構成で、Sysbench が 64 スレッドで更新インデックスをテストするように設定されている場合、平均レイテンシーは12.04 ミリ秒から 7.01 ミリ秒に 41.7% 減少します。

Async Commit 機能が有効になっている場合、1 つのネットワーク対話のレイテンシーを短縮し、データ書き込みのパフォーマンスを向上させるために、データベース アプリケーションの開発者は、トランザクションの一貫性を線形の一貫性から[因果の一貫性](/transaction-overview.md#causal-consistency)に減らすことを検討することをお勧めします。因果整合性を有効にする SQL ステートメントは`START TRANSACTION WITH CAUSAL CONSISTENCY`です。

原因の一貫性が有効になった後、同じハードウェアと構成で、Sysbench が oltp_write_only を 64 スレッドでテストするように設定されている場合、平均レイテンシーは11.86ms から 11.19ms に 5.6% 減少しました。

トランザクションの一貫性が線形一貫性から因果的一貫性に低下した後、アプリケーション内の複数のトランザクション間に相互依存関係がない場合、トランザクションはグローバルに一貫した順序を持ちません。

**非同期コミット機能は、新しく作成された v5.0 クラスターに対してデフォルトで有効になっています。**

以前のバージョンから v5.0 にアップグレードされたクラスターでは、この機能はデフォルトで無効になっています。この機能を有効にするには、 `set global tidb_enable_async_commit = ON;`ステートメントと`set global tidb_enable_1pc = ON;`ステートメントを実行します。

非同期コミット機能の制限は次のとおりです。

-   直接のダウングレードはサポートされていません。

### デフォルトでコプロセッサーのキャッシュ機能を有効にする {#enable-the-coprocessor-cache-feature-by-default}

[ユーザー文書](/tidb-configuration-file.md#tikv-clientcopr-cache-new-in-v400) 、 [#18028](https://github.com/pingcap/tidb/issues/18028)

5.0 GA では、コプロセッサーのキャッシュ機能がデフォルトで有効になっています。この機能を有効にすると、データ読み取りのレイテンシーを短縮するために、TiDB は tikv-server にプッシュされたオペレーターの計算結果を tidb-server にキャッシュします。

コプロセッサーのキャッシュ機能を無効にするには、 `tikv-client.copr-cache`から`0.0`の`capacity-mb`構成項目を変更します。

### <code>delete from table where id &lt;? Limit ?</code>実行パフォーマンスを改善<code>delete from table where id &lt;? Limit ?</code>声明 {#improve-the-execution-performance-of-code-delete-from-table-where-id-x3c-limit-code-statement}

[#18028](https://github.com/pingcap/tidb/issues/18028)

`delete from table where id <? limit ?`ステートメントの p99 パフォーマンスは 4 倍向上します。

### 負荷ベースの分割戦略を最適化して、一部の小さなテーブルのホットスポット読み取りシナリオでデータを分割できないというパフォーマンスの問題を解決します {#optimize-load-base-split-strategy-to-solve-the-performance-problem-that-data-cannot-be-split-in-some-small-table-hotspot-read-scenarios}

[#18005](https://github.com/pingcap/tidb/issues/18005)

## 安定性の向上 {#improve-stability}

### 不完全なスケジューリングによって引き起こされるパフォーマンス ジッターの問題を最適化する {#optimize-the-performance-jitter-issue-caused-by-imperfect-scheduling}

[#18005](https://github.com/pingcap/tidb/issues/18005)

TiDB スケジューリング プロセスは、I/O、ネットワーク、CPU、メモリなどのリソースを占有します。 TiDB がスケジュールされたタスクを制御しない場合、QPS と遅延により、リソースのプリエンプションが原因でパフォーマンスのジッターが発生する可能性があります。

次の最適化の後、8 時間のパフォーマンス テストで、TPC-C tpmC の標準偏差は 2% を超えません。

#### 不要なスケジューリングとパフォーマンス ジッタを削減するための新しいスケジューリング計算式の導入 {#introduce-new-scheduling-calculation-formulas-to-reduce-unnecessary-scheduling-and-performance-jitter}

ノード容量がシステムで設定されたウォーターラインに常に近い場合、または`store-limit`が大きすぎて容量負荷のバランスを取る場合、システムは頻繁にリージョンを他のノードにスケジュールしたり、リージョンを元のノードに戻したりします。スケジューリングは I/O、ネットワーク、CPU、メモリなどのリソースを占有し、パフォーマンスのジッターを引き起こすため、このタイプのスケジューリングは必要ありません。

この問題を軽減するために、PD は新しい一連の既定のスケジュール計算式を導入しています。 `region-score-formula-version = v1`を構成することで、古い式に戻すことができます。

#### デフォルトでクロステーブルのリージョン結合機能を有効にする {#enable-the-cross-table-region-merge-feature-by-default}

[ユーザー文書](/pd-configuration-file.md#enable-cross-table-merge)

v5.0 より前では、TiDB はクロステーブルのリージョンマージ機能をデフォルトで無効にしています。 v5.0 以降、この機能はデフォルトで有効になっており、空のリージョンの数と、ネットワーク、メモリ、および CPU のオーバーヘッドを削減します。この機能を無効にするには、 `schedule.enable-cross-table-merge`構成アイテムを変更します。

#### システムがデフォルトでデータ圧縮速度を自動的に調整できるようにして、バックグラウンド タスクとフォアグラウンドの読み取りおよび書き込みの間の I/O リソースの競合のバランスをとります。 {#enable-the-system-to-automatically-adjust-the-data-compaction-speed-by-default-to-balance-the-contention-for-i-o-resources-between-background-tasks-and-foreground-reads-and-writes}

[ユーザー文書](/tikv-configuration-file.md#rate-limiter-auto-tuned-new-in-v50)

v5.0 より前では、バックグラウンド タスクとフォアグラウンドの読み取りおよび書き込みの間の I/O リソースの競合のバランスをとるために、システムがデータ圧縮速度を自動的に調整する機能がデフォルトで無効になっています。 v5.0 から、TiDB はデフォルトでこの機能を有効にし、アルゴリズムを最適化して、レイテンシーのジッターを大幅に削減します。

この機能を無効にするには、 `rate-limiter-auto-tuned`構成アイテムを変更します。

#### デフォルトで GC 圧縮フィルター機能を有効にして、GC の CPU および I/O リソースの消費を削減します。 {#enable-the-gc-compaction-filter-feature-by-default-to-reduce-gc-s-consumption-of-cpu-and-i-o-resources}

[ユーザー文書](/garbage-collection-configuration.md#gc-in-compaction-filter) 、 [#18009](https://github.com/pingcap/tidb/issues/18009)

TiDB がガベージコレクション(GC) とデータ圧縮を実行するとき、パーティションは CPU と I/O リソースを占有します。これら 2 つのタスクの実行中に重複データが存在します。

GC の CPU および I/O リソースの消費を削減するために、GC 圧縮フィルター機能はこれら 2 つのタスクを 1 つに結合し、同じタスクで実行します。この機能はデフォルトで有効になっています。 `gc.enable-compaction-filter = false`を設定することで無効にできます。

#### TiFlash は、圧縮とデータの並べ替えによる I/O リソースの使用を制限します (<strong>実験的機能</strong>)。 {#tiflash-limits-the-compression-and-data-sorting-s-use-of-i-o-resources-strong-experimental-feature-strong}

この機能により、バックグラウンド タスクとフォアグラウンドの読み取りおよび書き込みの間の I/O リソースの競合が軽減されます。

この機能はデフォルトで無効になっています。この機能を有効にするには、 `bg_task_io_rate_limit`構成アイテムを変更します。

#### スケジューリングの制約をチェックするパフォーマンスと、大規模なクラスター内の異常なリージョンを修正するパフォーマンスを向上させます {#improve-the-performance-of-checking-scheduling-constraints-and-the-performance-of-fixing-the-unhealthy-regions-in-a-large-cluster}

### パフォーマンスのジッターを回避するために、実行計画を可能な限り変更しないようにします。 {#ensure-that-the-execution-plans-are-unchanged-as-much-as-possible-to-avoid-performance-jitter}

[ユーザー文書](/sql-plan-management.md)

#### SQL バインディングは<code>INSERT</code> 、 <code>REPLACE</code> 、 <code>UPDATE</code> 、 <code>DELETE</code>ステートメントをサポートします {#sql-binding-supports-the-code-insert-code-code-replace-code-code-update-code-code-delete-code-statements}

パフォーマンスのチューニングまたはデータベースの保守時に、不安定な実行計画のためにシステムのパフォーマンスが不安定であることが判明した場合は、判断に従って手動で最適化された SQL ステートメントを選択するか、または`EXPLAIN ANALYZE`でテストすることができます。最適化された SQL ステートメントを、アプリケーション コードで実行される SQL ステートメントにバインドして、安定したパフォーマンスを確保できます。

SQL BINDING ステートメントを使用して手動で SQL ステートメントをバインドする場合は、最適化された SQL ステートメントが元の SQL ステートメントと同じ構文であることを確認する必要があります。

`SHOW {GLOBAL | SESSION} BINDINGS`コマンドを実行すると、手動または自動でバインドされた実行計画の情報を表示できます。出力は v5.0 より前のバージョンと同じです。

#### 実行計画を自動的に取得してバインドする {#automatically-capture-and-bind-execution-plans}

TiDB をアップグレードする場合、パフォーマンスのジッタを回避するために、ベースライン キャプチャ機能を有効にして、システムが最新の実行計画を自動的にキャプチャしてバインドし、システム テーブルに保存できるようにすることができます。 TiDB がアップグレードされた後、 `SHOW GLOBAL BINDING`コマンドを実行してバインドされた実行計画をエクスポートし、これらの計画を削除するかどうかを決定できます。

この機能はデフォルトで無効になっています。サーバーを変更するか、グローバルシステム変数`tidb_capture_plan_baselines`を`ON`に設定することで有効にできます。この機能を有効にすると、システムはステートメントの概要から少なくとも 2 回出現する SQL ステートメントを`bind-info-lease` (デフォルト値は`3s` ) ごとにフェッチし、これらの SQL ステートメントを自動的にキャプチャしてバインドします。

### TiFlashクエリの安定性を向上 {#improve-stability-of-tiflash-queries}

システム変数[`tidb_allow_fallback_to_tikv`](/system-variables.md#tidb_allow_fallback_to_tikv-new-in-v50)追加して、 TiFlash が失敗したときにクエリを TiKV にフォールバックします。デフォルト値は`OFF`です。

### TiCDC の安定性を向上させ、過剰な増分データの複製によって引き起こされる OOM の問題を軽減します {#improve-ticdc-stability-and-alleviate-the-oom-issue-caused-by-replicating-too-much-incremental-data}

[ユーザー文書](/ticdc/ticdc-manage-changefeed.md#unified-sorter) 、 [#1150](https://github.com/pingcap/tiflow/issues/1150)

TiCDC v4.0.9 以前のバージョンでは、あまりにも多くのデータ変更をレプリケートすると、OOM が発生する可能性があります。 v5.0 では、Unified Sorter 機能がデフォルトで有効になっており、次のシナリオによって発生する OOM の問題を軽減しています。

-   TiCDC のデータ レプリケーション タスクは長時間一時停止されます。その間、大量の増分データが蓄積され、レプリケートする必要があります。
-   データ複製タスクは早いタイムスタンプから開始されるため、大量の増分データを複製する必要があります。

Unified Sorter は、以前のバージョンの`memory` / `file`ソート エンジン オプションと統合されています。変更を手動で構成する必要はありません。

制限:

-   増分データの量に応じて、十分なディスク容量を用意する必要があります。空き容量が 128 GB を超える SSD を使用することをお勧めします。

## 高可用性と災害復旧 {#high-availability-and-disaster-recovery}

### リージョンメンバーシップの変更中のシステムの可用性を向上させる {#improve-system-availability-during-region-membership-change}

[ユーザー文書](/pd-configuration-file.md#enable-joint-consensus-new-in-v50) 、 [#18079](https://github.com/pingcap/tidb/issues/18079) 、 [#7587](https://github.com/tikv/tikv/issues/7587) 、 [#2860](https://github.com/tikv/pd/issues/2860)

リージョンメンバーシップの変更プロセスでは、「メンバーの追加」と「メンバーの削除」の 2 つの操作が 2 つのステップで実行されます。メンバーシップの変更が完了するときに障害が発生した場合、リージョンは使用できなくなり、フォアグラウンド アプリケーションのエラーが返されます。

導入されたRaft Joint Consensus アルゴリズムは、リージョンメンバーシップの変更中のシステムの可用性を向上させることができます。会員変更時の「会員追加」「会員削除」の操作をまとめて全会員に送信します。変更プロセス中、リージョンは中間状態にあります。変更されたメンバーに障害が発生した場合でも、システムは引き続き使用できます。

この機能はデフォルトで有効になっています。 `pd-ctl config set enable-joint-consensus`コマンドを実行して`enable-joint-consensus`値を`false`に設定することで無効にできます。

### メモリ管理モジュールを最適化して、システム OOM のリスクを軽減します {#optimize-the-memory-management-module-to-reduce-system-oom-risks}

集計関数のメモリ使用量を追跡します。この機能はデフォルトで有効になっています。集計関数を含む SQL ステートメントが実行されるときに、現在のクエリの合計メモリ使用量が`mem-quota-query`で設定されたしきい値を超えると、システムは`oom-action`で定義された操作を自動的に実行します。

### ネットワーク パーティション中のシステムの可用性を向上させる {#improve-the-system-availability-during-network-partition}

## データ移行 {#data-migration}

### S3/ Auroraから TiDB にデータを移行する {#migrate-data-from-s3-aurora-to-tidb}

TiDB データ移行ツールは、Amazon S3 (およびその他の S3 互換storageサービス) をデータ移行の中間として使用し、 Auroraスナップショット データを直接 TiDB に初期化することをサポートし、Amazon S3/ Auroraから TiDB にデータを移行するためのより多くのオプションを提供します。

この機能を使用するには、次のドキュメントを参照してください。

-   [データを Amazon S3 クラウドstorageにエクスポートする](/dumpling-overview.md#export-data-to-amazon-s3-cloud-storage) 、 [#8](https://github.com/pingcap/dumpling/issues/8)
-   [TiDB Lightningを使用して Amazon Aurora MySQL から移行する](/migrate-aurora-to-tidb.md) 、 [#266](https://github.com/pingcap/tidb-lightning/issues/266)

### TiDB Cloudのデータ インポート パフォーマンスを最適化する {#optimize-the-data-import-performance-of-tidb-cloud}

TiDB Lightning は、 TiDB Cloudの AWS T1.standard 構成 (または同等の構成) に特化してデータ インポート パフォーマンスを最適化します。テスト結果は、 TiDB Lightning が1 TB の TPC-C データを TiDB にインポートする速度を 254 GiB/h から 366 GiB/h に 40% 向上させることを示しています。

## データの共有と購読 {#data-sharing-and-subscription}

### TiCDC を使用して TiDB を Kafka Connect (Confluent Platform) に統合 (<strong>実験的機能</strong>) {#integrate-tidb-to-kafka-connect-confluent-platform-using-ticdc-strong-experimental-feature-strong}

[ユーザー文書](/ticdc/integrate-confluent-using-ticdc.md) 、 [#660](https://github.com/pingcap/tiflow/issues/660)

TiDB データを他のシステムにストリーミングするビジネス要件をサポートするために、この機能を使用すると、TiDB データを Kafka、Hadoop、Oracle などのシステムにストリーミングできます。

Confluent プラットフォームによって提供される Kafka コネクタ プロトコルは、コミュニティで広く使用されており、さまざまなプロトコルでのリレーショナル データベースまたは非リレーショナル データベースへのデータ転送をサポートしています。 TiCDC を Confluent プラットフォームの Kafka Connect に統合することで、TiDB は TiDB データを他の異種データベースまたはシステムにストリーミングする機能を拡張します。

## 診断 {#diagnostics}

[ユーザー文書](/sql-statements/sql-statement-explain.md#explain)

SQL パフォーマンスの問題のトラブルシューティングでは、パフォーマンスの問題の原因を特定するために詳細な診断情報が必要です。 TiDB 5.0 より前では、 `EXPLAIN`ステートメントによって収集された情報は十分に詳細ではありませんでした。問題の根本原因は、ログ情報、監視情報、さらには推測に基づいてしか判断できないため、非効率的である可能性があります。

TiDB v5.0 では、パフォーマンスの問題をより効率的にトラブルシューティングできるように、次の改善が行われています。

-   `EXPLAIN ANALYZE`ステートメントを使用してすべての DML ステートメントを分析し、実際のパフォーマンス プランと各オペレーターの実行情報を表示することをサポートします。 [#18056](https://github.com/pingcap/tidb/issues/18056)
-   `EXPLAIN FOR CONNECTION`ステートメントを使用して、実行中のすべての SQL ステートメントのリアルタイム ステータスをチェックすることをサポートします。たとえば、ステートメントを使用して、各演算子の実行時間と処理された行数を確認できます。 [#18233](https://github.com/pingcap/tidb/issues/18233)
-   オペレーターによって送信された RPC リクエストの数、ロックの競合を解決する期間、ネットワークレイテンシー、RocksDB 内の削除されたデータのスキャンされた量、RocksDB のヒット率など、 `EXPLAIN ANALYZE`ステートメントの出力でオペレーターの実行に関する詳細を提供します。キャッシュします。 [#18663](https://github.com/pingcap/tidb/issues/18663)
-   スローログに SQL ステートメントの詳細な実行情報を自動的に記録するサポート。スローログの実行情報は、 `EXPLAIN ANALYZE`ステートメントの出力情報と一致しています。これには、各オペレーターが消費した時間、処理された行数、および送信された RPC 要求の数が含まれます。 [#15009](https://github.com/pingcap/tidb/issues/15009)

## 展開とメンテナンス {#deployment-and-maintenance}

### クラスター展開操作のロジックを最適化して、DBA が一連の標準的な TiDB本番クラスターをより迅速に展開できるようにします。 {#optimize-the-logic-of-cluster-deployment-operations-to-help-dbas-deploy-a-set-of-standard-tidb-production-cluster-faster}

[ユーザードキュメント](/production-deployment-using-tiup.md)

TiDB の以前のバージョンでは、 TiUPを使用して TiDB クラスターを展開する DBA は、環境の初期化が複雑で、チェックサム構成が過剰で、クラスター トポロジ ファイルの編集が難しいことに気付きました。これらの問題はすべて、DBA の導入効率の低下につながります。 TiDB v5.0 では、 TiUPを使用した TiDB の展開効率が、以下の項目によって DBA 向けに改善されています。

-   TiUP クラスタ は、より包括的なワンクリック環境チェックを実行し、修復の推奨事項を提供する`check topo.yaml`コマンドをサポートしています。
-   TiUP クラスタ は、環境チェック中に検出された環境問題を自動的に修復する`check topo.yaml --apply`コマンドをサポートしています。
-   TiUP クラスタ は、 DBA がグローバル ノード パラメータの編集と変更をサポートするためのクラスタ トポロジ テンプレート ファイルを取得する`template`コマンドをサポートしています。
-   TiUP は、 `edit-config`コマンドを使用して`remote_config`パラメータを編集し、リモート Prometheus を構成することをサポートしています。
-   TiUP は、 `external_alertmanagers`パラメータを編集して、 `edit-config`コマンドを使用して異なる AlertManager を設定することをサポートしています。
-   tiup-clusterの`edit-config`サブコマンドを使用してトポロジ ファイルを編集する場合、構成アイテムの値のデータ型を変更できます。

### アップグレードの安定性を向上 {#improve-upgrade-stability}

TiUP v1.4.0 より前では、 tiup-clusterを使用した TiDB クラスターのアップグレード中に、クラスターの SQL 応答が長時間ジッターし、PD オンライン ローリング アップグレード中に、クラスターの QPS が 10 秒から 30 秒の間でジッターしました。

TiUP v1.4.0 はロジックを調整し、次の最適化を行います。

-   PD ノードのアップグレード中、 TiUP は再起動された PD ノードのステータスを自動的にチェックし、ステータスが準備完了であることを確認した後、次の PD ノードのアップグレードにロールバックします。
-   TiUP はPD ロールを自動的に識別し、最初にフォロワー ロールの PD ノードをアップグレードし、最後に PDLeaderノードをアップグレードします。

### アップグレード時間を最適化する {#optimize-the-upgrade-time}

TiUP v1.4.0 より前では、DBA がtiup-clusterを使用して TiDB クラスターをアップグレードする場合、多数のノードを持つクラスターの場合、アップグレードの合計時間が長くなり、特定のユーザーのアップグレード時間枠の要件を満たすことができません。

v1.4.0 から、 TiUP は次の項目を最適化します。

-   `tiup cluster upgrade --offline`サブコマンドを使用した高速オフライン アップグレードをサポートします。
-   デフォルトでアップグレード中にローリング アップグレードを使用して、ユーザーのリージョンLeaderの再配置を高速化します。これにより、TiKV のローリング アップグレードの時間が短縮されます。
-   ローリング アップグレードを実行する前に、 `check`サブコマンドを使用してリージョンモニターのステータスを確認します。アップグレードの前にクラスターが正常な状態であることを確認して、アップグレードの失敗の可能性を減らします。

### ブレークポイント機能をサポート {#support-the-breakpoint-feature}

TiUP v1.4.0 より前では、DBA がtiup-cluster を使用して TiDB クラスターをアップグレードするときに、コマンドの実行が中断された場合、すべてのアップグレード操作を最初からやり直す必要がありました。

TiUP v1.4.0 は、 tiup-cluster `replay`サブコマンドを使用してブレークポイントから失敗した操作を再試行することをサポートし、アップグレードの中断後にすべての操作を再実行することを回避します。

### 保守・運用の機能強化 {#enhance-the-functionalities-of-maintenance-and-operations}

TiUP v1.4.0 では、TiDB クラスターを運用および保守するための機能がさらに強化されています。

-   ダウンタイム TiDB および DM クラスターでのアップグレードまたはパッチ操作をサポートして、より多くの使用シナリオに適応します。
-   クラスターのバージョンを取得するために、tiup-clusterの`display`サブコマンドに`--version`パラメーターを追加します。
-   スケールアウトするノードに Prometheus のみが含まれる場合、Prometheus ノードが存在しないことによるスケールアウトの失敗を回避するために、監視構成の更新操作は実行されません。
-   入力TiUPコマンドの結果が正しくない場合にエラー メッセージにユーザー入力を追加して、問題の原因をより迅速に突き止めることができるようにします。

## テレメトリー {#telemetry}

TiDB は、データ テーブルの数、クエリの数、新しい機能が有効になっているかどうかなど、テレメトリにクラスターの使用状況の指標を追加します。

詳細およびこの動作を無効にする方法については、 [テレメトリー](/telemetry.md)を参照してください。
