---
title: What's New in TiDB 5.0
---

# TiDB5.0の新機能 {#what-s-new-in-tidb-5-0}

発売日：2021年4月7日

TiDBバージョン：5.0.0

v5.0では、PingCAPは、企業がTiDBに基づいてアプリケーションを迅速に構築し、データベースパフォーマンス、パフォーマンスジッター、セキュリティ、高可用性、ディザスタリカバリ、SQLパフォーマンスのトラブルシューティングなどの心配から解放するのを支援することに専念しています。

v5.0では、主な新機能または改善点は次のとおりです。

-   TiFlashノードを介して超並列処理（MPP）アーキテクチャを導入します。これは、TiFlashノード間で大規模な結合クエリの実行ワークロードを共有します。 MPPモードが有効になっている場合、TiDBはコストに基づいて、MPPフレームワークを使用して計算を実行するかどうかを決定します。 MPPモードでは、結合キーは計算中に`Exchange`の操作で再分配されます。これにより、計算圧力が各TiFlashノードに分配され、計算が高速化されます。ベンチマークによると、同じクラスタリソースを使用すると、TiDB5.0MPPはGreenplum6.15.0およびApacheSpark3.1.1よりも2〜3倍高速化され、一部のクエリのパフォーマンスは8倍向上します。
-   データベースのパフォーマンスを向上させるために、クラスター化インデックス機能を導入します。たとえば、TPC-C tpmCテストでは、クラスター化インデックスを有効にしたTiDBのパフォーマンスが39％向上します。
-   非同期コミット機能を有効にして、書き込みレイテンシを減らします。たとえば、64スレッドのSysbenchテストでは、非同期コミットを有効にした場合のインデックス更新の平均遅延は、12.04ミリ秒から7.01ミリ秒に41.7％減少します。
-   ジッタを減らします。これは、オプティマイザの安定性を改善し、システムタスクによるI / O、ネットワーク、CPU、およびメモリリソースの使用を制限することによって実現されます。たとえば、8時間のパフォーマンステストでは、TPC-C tpmCの標準偏差は2％を超えません。
-   スケジューリングを改善し、実行計画を可能な限り安定させることにより、システムの安定性を強化します。
-   Raft Joint Consensusアルゴリズムを導入し、リージョンメンバーシップの変更中にシステムの可用性を確保します。
-   `EXPLAIN`の機能と非表示のインデックスを最適化します。これにより、データベース管理者（DBA）がSQLステートメントをより効率的にデバッグできます。
-   エンタープライズデータの信頼性を保証します。 TiDBからAmazonS3ストレージとGoogleCloudGCSにデータをバックアップしたり、これらのクラウドストレージプラットフォームからデータを復元したりできます。
-   AmazonS3ストレージまたはTiDB/MySQLからのデータインポートまたはデータエクスポートのパフォーマンスを向上させます。これにより、企業はクラウド上でアプリケーションを迅速に構築できます。たとえば、TPC-Cテストでは、1TiBデータのインポートのパフォーマンスが254GiB/hから366GiB/ hに40％向上します。

## 互換性の変更 {#compatibility-changes}

### システム変数 {#system-variables}

-   [`tidb_executor_concurrency`](/system-variables.md#tidb_executor_concurrency-new-in-v50)のシステム変数を追加して、複数の演算子の並行性を制御します。以前の`tidb_*_concurrency`の設定（ `tidb_projection_concurrency`など）は引き続き有効ですが、使用すると警告が表示されます。

-   [`tidb_skip_ascii_check`](/system-variables.md#tidb_skip_ascii_check-new-in-v50)のシステム変数を追加して、ASCII文字セットが書き込まれるときにASCII検証チェックをスキップするかどうかを指定します。このデフォルト値は`OFF`です。

-   [`tidb_enable_strict_double_type_check`](/system-variables.md#tidb_enable_strict_double_type_check-new-in-v50)のシステム変数を追加して、 `double(N)`のような構文をテーブルスキーマで定義できるかどうかを判断します。このデフォルト値は`OFF`です。

-   デフォルト値の[`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size)を`20000`から`0`に変更します。これは、バッチDMLステートメントが`INSERT INTO SELECT ...`でデフォルトで使用されなくなったことを意味し`LOAD` 。代わりに、大規模なトランザクションは、厳密なACIDセマンティクスに準拠するために使用されます。

    > **ノート：**
    >
    > 変数のスコープがセッションからグローバルに変更され、デフォルト値が`20000`から`0`に変更されます。アプリケーションが元のデフォルト値に依存している場合は、 `set global`ステートメントを使用して、アップグレード後に変数を元の値に変更する必要があります。

-   [`tidb_enable_noop_functions`](/system-variables.md#tidb_enable_noop_functions-new-in-v40)のシステム変数を使用して、一時テーブルの構文の互換性を制御します。この変数値が`OFF`の場合、 `CREATE TEMPORARY TABLE`構文はエラーを返します。

-   次のシステム変数を追加して、ガベージコレクション関連のパラメータを直接制御します。
    -   [`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-new-in-v50)
    -   [`tidb_gc_enable`](/system-variables.md#tidb_gc_enable-new-in-v50)
    -   [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)
    -   [`tidb_gc_run_interval`](/system-variables.md#tidb_gc_run_interval-new-in-v50)
    -   [`tidb_gc_scan_lock_mode`](/system-variables.md#tidb_gc_scan_lock_mode-new-in-v50)

-   デフォルト値の[`enable-joint-consensus`](/pd-configuration-file.md#enable-joint-consensus-new-in-v50)を`false`から`true`に変更します。これにより、デフォルトで共同コンセンサス機能が有効になります。

-   [`tidb_enable_amend_pessimistic_txn`](/system-variables.md#tidb_enable_amend_pessimistic_txn-new-in-v407)の値を`0`または`1`から`ON`または`OFF`に変更します。

-   次の新しい意味で、デフォルト値の[`tidb_enable_clustered_index`](/system-variables.md#tidb_enable_clustered_index-new-in-v50)を`OFF`から`INT_ONLY`に変更します。
    -   `ON` ：クラスター化インデックスが有効になります。非クラスター化インデックスの追加または削除がサポートされています。

    -   `OFF` ：クラスター化インデックスは無効です。非クラスター化インデックスの追加または削除がサポートされています。

    -   `INT_ONLY` ：デフォルト値。動作はv5.0以前の動作と一致しています。 INTタイプのクラスター化インデックスを`alter-primary-key = false`と一緒に有効にするかどうかを制御できます。
    > **ノート：**
    >
    > 5.0 GAの`tidb_enable_clustered_index`の`INT_ONLY`の値は、5.0RCの`OFF`の値と同じ意味です。 `OFF`設定の5.0RCクラスタから5.0GAにアップグレードすると、 `INT_ONLY`と表示されます。

### Configuration / コンフィグレーションファイルのパラメーター {#configuration-file-parameters}

-   TiDBの[`index-limit`](/tidb-configuration-file.md#index-limit-new-in-v50)の構成アイテムを追加します。その値のデフォルトは`64`で、範囲は`[64,512]`です。 MySQLテーブルは最大64個のインデックスをサポートします。その値がデフォルト設定を超え、テーブルに対して64を超えるインデックスが作成された場合、テーブルスキーマがMySQLに再インポートされると、エラーが報告されます。
-   MySQLのENUM/SETの長さ（ENUMの長さ&lt;255）と互換性があり、一貫性があるように、TiDBの[`enable-enum-length-limit`](/tidb-configuration-file.md#enable-enum-length-limit-new-in-v50)の構成項目を追加します。デフォルト値は`true`です。
-   `pessimistic-txn.enable`の構成アイテムを[`tidb_txn_mode`](/system-variables.md#tidb_txn_mode)の環境変数に置き換えます。
-   `performance.max-memory`の構成アイテムを[`performance.server-memory-quota`](/tidb-configuration-file.md#server-memory-quota-new-in-v409)に置き換えます
-   `tikv-client.copr-cache.enable`の構成アイテムを[`tikv-client.copr-cache.capacity-mb`](/tidb-configuration-file.md#capacity-mb)に置き換えます。アイテムの値が`0.0`の場合、この機能は無効になります。アイテムの値が`0.0`より大きい場合、この機能は有効になります。デフォルト値は`1000.0`です。
-   `rocksdb.auto-tuned`の構成アイテムを[`rocksdb.rate-limiter-auto-tuned`](/tikv-configuration-file.md#rate-limiter-auto-tuned-new-in-v50)に置き換えます。
-   `raftstore.sync-log`の構成アイテムを削除します。デフォルトでは、書き込まれたデータは強制的にディスクに流出します。 v5.0より前では、 `raftstore.sync-log`を明示的に無効にすることができます。 v5.0以降、構成値は強制的に`true`に設定されます。
-   `gc.enable-compaction-filter`構成項目のデフォルト値を`false`から`true`に変更します。
-   `enable-cross-table-merge`構成項目のデフォルト値を`false`から`true`に変更します。
-   [`rate-limiter-auto-tuned`](/tikv-configuration-file.md#rate-limiter-auto-tuned-new-in-v50)構成項目のデフォルト値を`false`から`true`に変更します。

### その他 {#others}

-   アップグレードする前に、TiDB構成[`feedback-probability`](/tidb-configuration-file.md#feedback-probability)の値を確認してください。値が0でない場合、アップグレード後に「回復可能なゴルーチンのパニック」エラーが発生しますが、このエラーはアップグレードには影響しません。
-   データの正確性の問題を回避するために、列タイプの変更中に`VARCHAR`タイプと`CHAR`タイプの間の変換を禁止します。

## 新機能 {#new-features}

### SQL {#sql}

#### リストの分割（<strong>実験的</strong>） {#list-partitioning-strong-experimental-strong}

[ユーザードキュメント](/partitioned-table.md#list-partitioning)

リスト分割機能を使用すると、大量のデータを含むテーブルを効果的に照会および保守できます。

この機能を有効にすると、パーティションとパーティション間でのデータの分散方法が`PARTITION BY LIST(expr) PARTITION part_name VALUES IN (...)`式に従って定義されます。パーティションテーブルのデータセットは、最大1024個の個別の整数値をサポートします。 `PARTITION ... VALUES IN (...)`句を使用して値を定義できます。

リストの分割を有効にするには、セッション変数[`tidb_enable_list_partition`](/system-variables.md#tidb_enable_list_partition-new-in-v50)を`ON`に設定します。

#### COLUMNSパーティショニングのリスト（<strong>実験的</strong>） {#list-columns-partitioning-strong-experimental-strong}

[ユーザードキュメント](/partitioned-table.md#list-columns-partitioning)

リスト列のパーティショニングは、リストパーティショニングの変形です。複数の列をパーティションキーとして使用できます。整数データ型に加えて、文字列、 `DATE` 、および`DATETIME`データ型の列をパーティション列として使用することもできます。

List COLUMNSパーティショニングを有効にするには、セッション変数[`tidb_enable_list_partition`](/system-variables.md#tidb_enable_list_partition-new-in-v50)を`ON`に設定します。

#### 見えないインデックス {#invisible-indexes}

[ユーザードキュメント](/sql-statements/sql-statement-alter-index.md) [＃9246](https://github.com/pingcap/tidb/issues/9246)

パフォーマンスを調整したり、最適なインデックスを選択したりする場合は、SQLステートメントを使用してインデックスを`Visible`または`Invisible`に設定できます。この設定により、 `DROP INDEX`や`ADD INDEX`などのリソースを消費する操作の実行を回避できます。

インデックスの可視性を変更するには、 `ALTER INDEX`ステートメントを使用します。変更後、オプティマイザーは、インデックスの可視性に基づいて、このインデックスをインデックスリストに追加するかどうかを決定します。

#### <code>EXCEPT</code>および<code>INTERSECT</code>演算子 {#code-except-code-and-code-intersect-code-operators}

[ユーザードキュメント](/functions-and-operators/set-operators.md) [＃18031](https://github.com/pingcap/tidb/issues/18031)

`INTERSECT`演算子は集合演算子であり、2つ以上のクエリの結果セットの共通部分を返します。ある程度、それは`Inner Join`演算子の代替です。

`EXCEPT`演算子は集合演算子であり、2つのクエリの結果セットを組み合わせて、最初のクエリ結果には含まれているが2番目のクエリ結果には含まれていない要素を返します。

### 取引 {#transaction}

[ユーザードキュメント](/system-variables.md#tidb_enable_amend_pessimistic_txn-new-in-v407) [＃18005](https://github.com/pingcap/tidb/issues/18005)

悲観的トランザクションモードでは、トランザクションに関連するテーブルに同時DDL操作または`SCHEMA VERSION`変更が含まれている場合、システムはトランザクションの`SCHEMA VERSION`を最新に自動的に更新して、トランザクションコミットが成功するようにし、クライアントが`Information schema is changed`エラーを受信しないようにします。トランザクションは、DDL操作または`SCHEMA VERSION`の変更によって中断されます。

この機能はデフォルトで無効になっています。この機能を有効にするには、 [`tidb_enable_amend_pessimistic_txn`](/system-variables.md#tidb_enable_amend_pessimistic_txn-new-in-v407)のシステム変数の値を変更します。この機能はv4.0.7で導入され、v5.0で修正された次の問題があります。

-   TiDBBinlogが`Add Column`の操作を実行するときに発生する互換性の問題
-   この機能を一意のインデックスと一緒に使用すると発生するデータの不整合の問題
-   追加されたインデックスと一緒に機能を使用するときに発生するデータの不整合の問題

現在、この機能にはまだ次の非互換性の問題があります。

-   同時トランザクションがある場合、トランザクションのセマンティクスが変わる可能性があります
-   この機能をTiDBBinlogと一緒に使用すると発生する既知の互換性の問題
-   `Change Column`との非互換性

### 文字セットと照合順序 {#character-set-and-collation}

-   `utf8mb4_unicode_ci`と`utf8_unicode_ci`の照合をサポートします。 [ユーザードキュメント](/character-set-and-collation.md#new-framework-for-collations) [＃17596](https://github.com/pingcap/tidb/issues/17596)
-   照合の大文字と小文字を区別しない比較ソートをサポートする

### 安全 {#security}

[ユーザードキュメント](/log-redaction.md) [＃18566](https://github.com/pingcap/tidb/issues/18566)

セキュリティコンプライアンス要件（*一般データ保護規則*、GDPRなど）を満たすために、システムは出力エラーメッセージとログで機密性の低い情報（IDやクレジットカード番号など）をサポートし、機密情報の漏洩を回避できます。

TiDBは、出力ログ情報の感度低下をサポートしています。この機能を有効にするには、次のスイッチを使用します。

-   グローバル変数[`tidb_redact_log`](/system-variables.md#tidb_redact_log) 。デフォルト値は`0`です。これは、感度低下が無効になっていることを意味します。 tidb-serverログの感度低下を有効にするには、変数値を`1`に設定します。
-   構成項目`security.redact-info-log` 。デフォルト値は`false`です。これは、感度低下が無効になっていることを意味します。 tikv-serverログの感度低下を有効にするには、変数値を`true`に設定します。
-   構成項目`security.redact-info-log` 。デフォルト値は`false`です。これは、感度低下が無効になっていることを意味します。 pd-serverログの感度低下を有効にするには、変数値を`true`に設定します。
-   tiflash-serverの構成項目`security.redact_info_log`とtiflash-learnerの構成項目`security.redact-info-log` 。デフォルト値は両方とも`false`です。これは、感度低下が無効になっていることを意味します。 tiflash-serverおよびtiflash-learnerログの感度低下を有効にするには、両方の変数の値を`true`に設定します。

この機能はv5.0で導入されました。この機能を使用するには、システム変数と上記のすべての構成項目を有効にします。

## パフォーマンスの最適化 {#performance-optimization}

### MPPアーキテクチャ {#mpp-architecture}

[ユーザードキュメント](/tiflash/use-tiflash.md)

TiDBは、TiFlashノードを介してMPPアーキテクチャを導入します。このアーキテクチャにより、複数のTiFlashノードが大規模な結合クエリの実行ワークロードを共有できます。

MPPモードがオンの場合、TiDBは、計算コストに基づいて、計算のためにMPPエンジンにクエリを送信するかどうかを決定します。 MPPモードでは、TiDBは、データ計算（ `Exchange`の操作）中に結合キーを再配布することにより、実行中の各TiFlashノードにテーブル結合の計算を分散し、計算を高速化します。さらに、TiFlashがすでにサポートしている集約コンピューティング機能により、TiDBはクエリの計算をTiFlashMPPクラスタにプッシュダウンできます。次に、分散環境は、実行プロセス全体を加速し、分析クエリの速度を劇的に向上させるのに役立ちます。

TPC-H 100ベンチマークテストでは、TiFlash MPPは、従来の分析データベースの分析エンジンおよびHadoop上のSQLよりも大幅な処理速度を実現します。このアーキテクチャを使用すると、従来のオフライン分析ソリューションよりも高いパフォーマンスで、最新のトランザクションデータに対して直接大規模な分析クエリを実行できます。ベンチマークによると、同じクラスタリソースを使用すると、TiDB5.0MPPはGreenplum6.15.0およびApacheSpark3.1.1よりも2〜3倍高速化され、一部のクエリのパフォーマンスは8倍向上します。

現在、MPPモードでサポートされていない主な機能は次のとおりです（詳細については、 [TiFlashを使用する](/tiflash/use-tiflash.md)を参照してください）。

-   テーブルのパーティション化
-   ウィンドウ関数
-   照合
-   いくつかの組み込み関数
-   TiKVからのデータの読み取り
-   OOM流出
-   連合
-   フルアウタージョイン

### クラスター化されたインデックス {#clustered-index}

[ユーザードキュメント](/clustered-indexes.md) [＃4841](https://github.com/pingcap/tidb/issues/4841)

テーブル構造を設計したり、データベースの動作を分析したりするときに、主キーを持つ一部の列がグループ化およびソートされることが多く、これらの列に対するクエリが特定の範囲のデータまたは少量を返すことが多い場合は、クラスター化インデックス機能を使用することをお勧めします値が異なるデータの場合、対応するデータによって読み取りまたは書き込みのホットスポットの問題が発生することはありません。

一部のデータベース管理システムでは*インデックス編成テーブル*とも呼ばれるクラスター化インデックスは、テーブルのデータに関連付けられたストレージ構造です。クラスタ化インデックスを作成するときに、インデックスのキーとしてテーブルから1つ以上の列を指定できます。 TiDBはこれらのキーを特定の構造に格納します。これにより、TiDBはキーに関連付けられた行をすばやく効率的に検索できるため、データのクエリと書き込みのパフォーマンスが向上します。

クラスタ化インデックス機能を有効にすると、次の場合にTiDBのパフォーマンスが大幅に向上します（たとえば、TPC-C tpmCテストでは、クラスタ化インデックスを有効にした場合のTiDBのパフォーマンスが39％向上します）。

-   データが挿入されると、クラスター化されたインデックスにより、ネットワークからのインデックスデータの書き込みが1回減ります。
-   同等の条件を持つクエリに主キーのみが含まれる場合、クラスター化インデックスは、ネットワークからのインデックスデータの読み取りを1回減らします。
-   範囲条件を含むクエリに主キーのみが含まれる場合、クラスター化インデックスは、ネットワークからのインデックスデータの複数の読み取りを減らします。
-   同等または範囲の条件を持つクエリに主キープレフィックスが含まれる場合、クラスター化インデックスは、ネットワークからのインデックスデータの複数の読み取りを減らします。

各テーブルは、クラスター化インデックスまたは非クラスター化インデックスのいずれかを使用して、データを並べ替えて格納できます。これら2つのストレージ構造の違いは次のとおりです。

-   クラスタ化インデックスを作成するときに、インデックスのキー値としてテーブル内の1つ以上の列を指定できます。クラスタ化されたインデックスは、キー値に従ってテーブルのデータを並べ替えて保存します。各テーブルには、クラスター化インデックスを1つだけ含めることができます。テーブルにクラスター化インデックスがある場合、それはクラスター化インデックステーブルと呼ばれます。それ以外の場合は、非クラスター化インデックステーブルと呼ばれます。
-   非クラスター化インデックスを作成すると、テーブル内のデータは順序付けられていない構造で格納されます。 TiDBはデータの各行に一意のROWIDを自動的に割り当てるため、非クラスター化インデックスのキー値を明示的に指定する必要はありません。クエリ中に、ROWIDを使用して対応する行を検索します。データのクエリまたは挿入時に少なくとも2つのネットワークI/O操作があるため、クラスター化インデックスと比較してパフォーマンスが低下します。

テーブルデータが変更されると、データベースシステムはクラスター化インデックスと非クラスター化インデックスを自動的に維持します。

デフォルトでは、すべての主キーは非クラスター化インデックスとして作成されます。次の2つの方法のいずれかで、主キーをクラスター化インデックスまたは非クラスター化インデックスとして作成できます。

-   テーブルを作成するときにステートメントでキーワード`CLUSTERED | NONCLUSTERED`を指定すると、システムは指定された方法でテーブルを作成します。構文は次のとおりです。

```sql
CREATE TABLE `t` (`a` VARCHAR(255), `b` INT, PRIMARY KEY (`a`, `b`) CLUSTERED);
```

または

```sql
CREATE TABLE `t` (`a` VARCHAR(255) PRIMARY KEY CLUSTERED, `b` INT);
```

ステートメント`SHOW INDEX FROM tbl-name`を実行して、テーブルにクラスター化インデックスがあるかどうかを照会できます。

-   クラスター化インデックス機能を制御するようにシステム変数`tidb_enable_clustered_index`を構成します。サポートされている値は`ON` 、および`OFF` `INT_ONLY` 。
    -   `ON` ：クラスター化インデックス機能がすべてのタイプの主キーに対して有効になっていることを示します。非クラスター化インデックスの追加と削除がサポートされています。
    -   `OFF` ：すべてのタイプの主キーに対してクラスター化インデックス機能が無効になっていることを示します。非クラスター化インデックスの追加と削除がサポートされています。
    -   `INT_ONLY` ：デフォルト値。変数が`INT_ONLY`に設定され、 `alter-primary-key`が`false`に設定されている場合、単一の整数列で構成される主キーは、デフォルトでクラスター化インデックスとして作成されます。動作は、TiDBv5.0以前のバージョンの動作と一致しています。

`CREATE TABLE`ステートメントにキーワード`CLUSTERED | NONCLUSTERED`が含まれている場合、そのステートメントはシステム変数の構成と構成項目をオーバーライドします。

ステートメントでキーワード`CLUSTERED | NONCLUSTERED`を指定して、クラスター化インデックス機能を使用することをお勧めします。このように、TiDBは、必要に応じて、システム内のクラスター化インデックスと非クラスター化インデックスのすべてのデータ型を同時に使用する方が柔軟です。

`tidb_enable_clustered_index = INT_ONLY`を使用することはお勧めしません。これは、この機能を互換性のあるものにするために`INT_ONLY`が一時的に使用され、将来的に非推奨になるためです。

クラスタ化インデックスの制限は次のとおりです。

-   クラスタ化インデックスと非クラスタ化インデックス間の相互変換はサポートされていません。
-   クラスタ化インデックスの削除はサポートされていません。
-   `ALTER TABLE`ステートメントを使用したクラスター化インデックスの追加、削除、および変更はサポートされていません。
-   クラスタ化されたインデックスの再編成と再作成はサポートされていません。
-   インデックスの有効化または無効化はサポートされていません。つまり、非表示インデックス機能はクラスター化インデックスには効果的ではありません。
-   クラスタ化されたインデックスとして`UNIQUE KEY`を作成することはサポートされていません。
-   クラスター化インデックス機能をTiDBBinlogと一緒に使用することはサポートされていません。 TiDB Binlogを有効にすると、TiDBはクラスター化インデックスとして単一の整数主キーの作成のみをサポートします。 TiDB Binlogは、クラスター化インデックスを持つ既存のテーブルのデータ変更をダウンストリームに複製しません。
-   クラスタ化インデックス機能を属性`SHARD_ROW_ID_BITS`および`PRE_SPLIT_REGIONS`と一緒に使用することはサポートされていません。
-   クラスタが新しいバージョンにアップグレードされてからロールバックされる場合は、ロールバック前にテーブルデータをエクスポートし、ロールバック後にデータをインポートして、新しく追加されたテーブルをダウングレードする必要があります。他のテーブルは影響を受けません。

### 非同期コミット {#async-commit}

[ユーザードキュメント](/system-variables.md#tidb_enable_async_commit-new-in-v50) [＃8316](https://github.com/tikv/tikv/issues/8316)

データベースのクライアントは、データベースシステムが2フェーズ（2PC）で同期的にトランザクションコミットを完了するのを待ちます。トランザクションは、第1フェーズのコミットが成功した後、結果をクライアントに返します。システムは、トランザクションのコミット待ち時間を短縮するために、バックグラウンドで第2フェーズのコミット操作を非同期的に実行します。トランザクション書き込みに1つのリージョンのみが含まれる場合、2番目のフェーズは直接省略され、トランザクションは1フェーズコミットになります。

同じハードウェアと構成で非同期コミット機能を有効にした後、Sysbenchが64スレッドで更新インデックスをテストするように設定されている場合、平均遅延は12.04msから7.01msに41.7％減少します。

非同期コミット機能が有効になっている場合、1つのネットワーク相互作用の待ち時間を短縮し、データ書き込みのパフォーマンスを向上させるために、データベースアプリケーション開発者は、トランザクションの整合性を線形整合性から[因果整合性](/transaction-overview.md#causal-consistency)に下げることを検討することをお勧めします。因果整合性を有効にするSQLステートメントは`START TRANSACTION WITH CAUSAL CONSISTENCY`です。

同じハードウェアと構成で因果整合性を有効にした後、Sysbenchが64スレッドでoltp_write_onlyをテストするように設定されている場合、平均遅延は11.86msから11.19msに5.6％減少しました。

トランザクションの整合性が線形整合性から因果整合性に低下した後、アプリケーション内の複数のトランザクション間に相互依存性がない場合、トランザクションはグローバルに一貫した順序になりません。

**非同期コミット機能は、新しく作成されたv5.0クラスターに対してデフォルトで有効になっています。**

この機能は、以前のバージョンからv5.0にアップグレードされたクラスターではデフォルトで無効になっています。この機能を有効にするには、 `set global tidb_enable_async_commit = ON;`ステートメントと`set global tidb_enable_1pc = ON;`ステートメントを実行します。

非同期コミット機能の制限は次のとおりです。

-   直接ダウングレードはサポートされていません。

### コプロセッサーのキャッシュ機能をデフォルトで有効にする {#enable-the-coprocessor-cache-feature-by-default}

[ユーザードキュメント](/tidb-configuration-file.md#tikv-clientcopr-cache-new-in-v400) [＃18028](https://github.com/pingcap/tidb/issues/18028)

5.0 GAでは、コプロセッサーのキャッシュ機能がデフォルトで有効になっています。この機能を有効にすると、データの読み取りの待ち時間を短縮するために、TiDBはtidb-serverのtikv-serverにプッシュダウンされた演算子の計算結果をキャッシュします。

コプロセッサーのキャッシュ機能を無効にするには、 `tikv-client.copr-cache`から`0.0`の`capacity-mb`の構成項目を変更します。

### <code>delete from table where id &lt;? Limit ?</code>の実行パフォーマンスを改善します。 <code>delete from table where id &lt;? Limit ?</code>声明 {#improve-the-execution-performance-of-code-delete-from-table-where-id-x3c-limit-code-statement}

[＃18028](https://github.com/pingcap/tidb/issues/18028)

`delete from table where id <? limit ?`ステートメントのp99パフォーマンスは4倍向上しています。

### ロードベースの分割戦略を最適化して、一部の小さなテーブルのホットスポット読み取りシナリオではデータを分割できないというパフォーマンスの問題を解決します {#optimize-load-base-split-strategy-to-solve-the-performance-problem-that-data-cannot-be-split-in-some-small-table-hotspot-read-scenarios}

[＃18005](https://github.com/pingcap/tidb/issues/18005)

## 安定性を向上させる {#improve-stability}

### 不完全なスケジューリングによって引き起こされるパフォーマンスジッターの問題を最適化する {#optimize-the-performance-jitter-issue-caused-by-imperfect-scheduling}

[＃18005](https://github.com/pingcap/tidb/issues/18005)

TiDBスケジューリングプロセスは、I / O、ネットワーク、CPU、メモリなどのリソースを占有します。 TiDBがスケジュールされたタスクを制御しない場合、QPSと遅延により、リソースのプリエンプションが原因でパフォーマンスジッターが発生する可能性があります。

以下の最適化の後、8時間のパフォーマンステストで、TPC-C tpmCの標準偏差は2％を超えません。

#### 新しいスケジューリング計算式を導入して、不要なスケジューリングとパフォーマンスジッターを削減します {#introduce-new-scheduling-calculation-formulas-to-reduce-unnecessary-scheduling-and-performance-jitter}

ノード容量が常にシステムで設定された喫水線の近くにある場合、または`store-limit`が大きすぎる場合、容量負荷のバランスをとるために、システムはリージョンを他のノードにスケジュールしたり、リージョンを元のノードにスケジュールし直したりします。スケジューリングはI/O、ネットワーク、CPU、メモリなどのリソースを占有し、パフォーマンスのジッターを引き起こすため、このタイプのスケジューリングは必要ありません。

この問題を軽減するために、PDはデフォルトのスケジューリング計算式の新しいセットを導入します。 `region-score-formula-version = v1`を設定することにより、古い式に戻すことができます。

#### クロステーブルリージョンマージ機能をデフォルトで有効にする {#enable-the-cross-table-region-merge-feature-by-default}

[ユーザードキュメント](/pd-configuration-file.md#enable-cross-table-merge)

v5.0より前では、TiDBはデフォルトでクロステーブルリージョンマージ機能を無効にします。 v5.0以降、この機能はデフォルトで有効になり、空のリージョンの数とネットワーク、メモリ、およびCPUのオーバーヘッドを削減します。 `schedule.enable-cross-table-merge`の構成アイテムを変更することにより、この機能を無効にできます。

#### システムがデフォルトでデータ圧縮速度を自動的に調整できるようにして、バックグラウンドタスクとフォアグラウンド読み取りおよび書き込みの間のI/Oリソースの競合のバランスを取ります {#enable-the-system-to-automatically-adjust-the-data-compaction-speed-by-default-to-balance-the-contention-for-i-o-resources-between-background-tasks-and-foreground-reads-and-writes}

[ユーザードキュメント](/tikv-configuration-file.md#rate-limiter-auto-tuned-new-in-v50)

v5.0より前では、バックグラウンドタスクとフォアグラウンド読み取りおよび書き込みの間のI / Oリソースの競合のバランスをとるために、システムがデータ圧縮速度を自動的に調整する機能はデフォルトで無効になっています。 v5.0以降、TiDBはこの機能をデフォルトで有効にし、アルゴリズムを最適化して、遅延ジッターを大幅に削減します。

`rate-limiter-auto-tuned`の構成アイテムを変更することにより、この機能を無効にできます。

#### GCのCPUおよびI/Oリソースの消費を減らすために、デフォルトでGC圧縮フィルター機能を有効にします {#enable-the-gc-compaction-filter-feature-by-default-to-reduce-gc-s-consumption-of-cpu-and-i-o-resources}

[ユーザードキュメント](/garbage-collection-configuration.md#gc-in-compaction-filter) [＃18009](https://github.com/pingcap/tidb/issues/18009)

TiDBがガベージコレクション（GC）とデータ圧縮を実行する場合、パーティションはCPUとI/Oリソースを占有します。これら2つのタスクの実行中に、重複するデータが存在します。

GCのCPUおよびI/Oリソースの消費を削減するために、GC圧縮フィルター機能はこれら2つのタスクを1つに結合し、同じタスクで実行します。この機能はデフォルトで有効になっています。 `gc.enable-compaction-filter = false`を設定することで無効にできます。

#### TiFlashは、圧縮とデータの並べ替えによるI / Oリソースの使用を制限します（<strong>実験的機能</strong>） {#tiflash-limits-the-compression-and-data-sorting-s-use-of-i-o-resources-strong-experimental-feature-strong}

この機能は、バックグラウンドタスクとフォアグラウンドの読み取りおよび書き込みの間のI/Oリソースの競合を軽減します。

この機能はデフォルトで無効になっています。この機能を有効にするには、 `bg_task_io_rate_limit`の構成アイテムを変更します。

#### スケジューリングの制約をチェックするパフォーマンスと、大規模なクラスタの異常なリージョンを修正するパフォーマンスを向上させます {#improve-the-performance-of-checking-scheduling-constraints-and-the-performance-of-fixing-the-unhealthy-regions-in-a-large-cluster}

### パフォーマンスのジッターを回避するために、実行プランが可能な限り変更されていないことを確認してください {#ensure-that-the-execution-plans-are-unchanged-as-much-as-possible-to-avoid-performance-jitter}

[ユーザードキュメント](/sql-plan-management.md)

#### SQLバインディングは、 <code>INSERT</code> 、 <code>REPLACE</code> 、 <code>UPDATE</code> 、 <code>DELETE</code>ステートメントをサポートします {#sql-binding-supports-the-code-insert-code-code-replace-code-code-update-code-code-delete-code-statements}

パフォーマンスの調整またはデータベースの保守時に、実行プランが不安定なためにシステムパフォーマンスが不安定であることがわかった場合は、判断に応じて手動で最適化されたSQLステートメントを選択するか、 `EXPLAIN ANALYZE`でテストできます。最適化されたSQLステートメントをアプリケーションコードで実行されるSQLステートメントにバインドして、安定したパフォーマンスを確保できます。

SQL BINDINGステートメントを使用してSQLステートメントを手動でバインドする場合は、最適化されたSQLステートメントの構文が元のSQLステートメントと同じであることを確認する必要があります。

`SHOW {GLOBAL | SESSION} BINDINGS`コマンドを実行すると、手動または自動でバインドされた実行プラン情報を表示できます。出力は、v5.0より前のバージョンの出力と同じです。

#### 実行プランを自動的にキャプチャしてバインドします {#automatically-capture-and-bind-execution-plans}

TiDBをアップグレードする場合、パフォーマンスジッターを回避するために、ベースラインキャプチャ機能を有効にして、システムが最新の実行プランを自動的にキャプチャしてバインドし、システムテーブルに格納できるようにすることができます。 TiDBがアップグレードされた後、 `SHOW GLOBAL BINDING`コマンドを実行してバインドされた実行プランをエクスポートし、これらのプランを削除するかどうかを決定できます。

この機能はデフォルトで無効になっています。サーバーを変更するか、 `tidb_capture_plan_baselines`グローバルシステム変数を`ON`に設定することで、これを有効にできます。この機能を有効にすると、システムは`bind-info-lease`回ごとにステートメントの概要から少なくとも2回表示されるSQLステートメントをフェッチし（デフォルト値は`3s` ）、これらのSQLステートメントを自動的にキャプチャしてバインドします。

### TiFlashクエリの安定性を向上させる {#improve-stability-of-tiflash-queries}

システム変数[`tidb_allow_fallback_to_tikv`](/system-variables.md#tidb_allow_fallback_to_tikv-new-in-v50)を追加して、TiFlashが失敗したときにクエリをTiKVにフォールバックします。デフォルト値は`OFF`です。

### TiCDCの安定性を改善し、過剰な増分データの複製によって引き起こされるOOMの問題を軽減します {#improve-ticdc-stability-and-alleviate-the-oom-issue-caused-by-replicating-too-much-incremental-data}

[ユーザードキュメント](/ticdc/manage-ticdc.md#unified-sorter) [＃1150](https://github.com/pingcap/tiflow/issues/1150)

TiCDC v4.0.9以前のバージョンでは、あまりにも多くのデータ変更を複製すると、OOMが発生する可能性があります。 v5.0では、次のシナリオによって引き起こされるOOMの問題を軽減するために、統合ソーター機能がデフォルトで有効になっています。

-   TiCDCのデータ複製タスクは長時間一時停止されます。その間、大量の増分データが蓄積され、複製する必要があります。
-   データ複製タスクは早いタイムスタンプから開始されるため、大量の増分データを複製する必要があります。

ユニファイドソーターは、以前のバージョンの`memory`ソートエンジンオプションと統合されてい`file` 。変更を手動で構成する必要はありません。

制限：

-   増分データの量に応じて、十分なディスク容量を提供する必要があります。 128GBを超える空き容量のSSDを使用することをお勧めします。

## 高可用性とディザスタリカバリ {#high-availability-and-disaster-recovery}

### リージョンメンバーシップの変更中のシステムの可用性を向上させる {#improve-system-availability-during-region-membership-change}

[ユーザードキュメント](/pd-configuration-file.md#enable-joint-consensus-new-in-v50) [＃18079](https://github.com/pingcap/tidb/issues/18079) [＃7587](https://github.com/tikv/tikv/issues/7587) [＃2860](https://github.com/tikv/pd/issues/2860)

リージョンメンバーシップの変更の過程で、「メンバーの追加」と「メンバーの削除」は、2つのステップで実行される2つの操作です。メンバーシップの変更が終了したときに障害が発生した場合、リージョンは使用できなくなり、フォアグラウンドアプリケーションのエラーが返されます。

導入されたRaftJointConsensusアルゴリズムは、リージョンメンバーシップの変更中のシステムの可用性を向上させることができます。メンバーシップ変更時の「メンバーの追加」と「メンバーの削除」の操作を1つの操作にまとめて、すべてのメンバーに送信します。変更プロセス中、リージョンは中間状態になります。変更されたメンバーに障害が発生した場合でも、システムは引き続き使用できます。

この機能はデフォルトで有効になっています。 `pd-ctl config set enable-joint-consensus`コマンドを実行して`enable-joint-consensus`の値を`false`に設定すると、無効にできます。

### メモリ管理モジュールを最適化して、システムOOMのリスクを軽減します {#optimize-the-memory-management-module-to-reduce-system-oom-risks}

集計関数のメモリ使用量を追跡します。この機能はデフォルトで有効になっています。集計関数を含むSQLステートメントが実行されるときに、現在のクエリの合計メモリ使用量が`mem-quota-query`で設定されたしきい値を超えると、システムは`oom-action`で定義された操作を自動的に実行します。

### ネットワークパーティション中のシステムの可用性を向上させる {#improve-the-system-availability-during-network-partition}

## データ移行 {#data-migration}

### S3/ AuroraからTiDBにデータを移行する {#migrate-data-from-s3-aurora-to-tidb}

TiDBデータ移行ツールは、データ移行の中間としてAmazon S3（およびその他のS3互換ストレージサービス）を使用し、 AuroraスナップショットデータをTiDBに直接初期化することをサポートし、Amazon S3/ AuroraからTiDBにデータを移行するためのより多くのオプションを提供します。

この機能を使用するには、次のドキュメントを参照してください。

-   [AmazonS3クラウドストレージにデータをエクスポートする](/dumpling-overview.md#export-data-to-amazon-s3-cloud-storage) [＃8](https://github.com/pingcap/dumpling/issues/8)
-   [Auroraを使用してAmazonAuroraMySQLから移行する](/migrate-aurora-to-tidb.md) [＃266](https://github.com/pingcap/tidb-lightning/issues/266)

### TiDB Cloudのデータインポートパフォーマンスを最適化する {#optimize-the-data-import-performance-of-tidb-cloud}

TiDB Lightningは、 TiDB CloudのAWS T1。標準構成（または同等の構成）向けに、データインポートのパフォーマンスを最適化します。テスト結果は、TiDBLightningが1TBのTPC-CデータをTiDBにインポートする速度を254GiB/hから366GiB/ hに40％向上させることを示しています。

## データ共有とサブスクリプション {#data-sharing-and-subscription}

### TiCDC（<strong>実験的機能</strong>）を使用してTiDBをKafka Connect（コンフルエントプラットフォーム）に統合する {#integrate-tidb-to-kafka-connect-confluent-platform-using-ticdc-strong-experimental-feature-strong}

[ユーザードキュメント](/ticdc/integrate-confluent-using-ticdc.md) [＃660](https://github.com/pingcap/tiflow/issues/660)

TiDBデータを他のシステムにストリーミングするというビジネス要件をサポートするために、この機能を使用すると、TiDBデータをKafka、Hadoop、Oracleなどのシステムにストリーミングできます。

Confluentプラットフォームによって提供されるKafkaコネクタプロトコルは、コミュニティで広く使用されており、さまざまなプロトコルでリレーショナルデータベースまたは非リレーショナルデータベースにデータを転送することをサポートしています。 TiCDCをConfluentプラットフォームのKafkaConnectに統合することにより、TiDBは、TiDBデータを他の異種データベースまたはシステムにストリーミングする機能を拡張します。

## 診断 {#diagnostics}

[ユーザードキュメント](/sql-statements/sql-statement-explain.md#explain)

SQLパフォーマンスの問題のトラブルシューティング中に、パフォーマンスの問題の原因を判別するために詳細な診断情報が必要です。 TiDB 5.0より前は、 `EXPLAIN`のステートメントによって収集された情報は十分に詳細ではありませんでした。問題の根本的な原因は、ログ情報、監視情報、または推測に基づいてのみ判断できますが、これは非効率的である可能性があります。

TiDB v5.0では、パフォーマンスの問題をより効率的にトラブルシューティングできるように、次の改善が行われました。

-   `EXPLAIN ANALYZE`ステートメントを使用してすべてのDMLステートメントを分析し、各オペレーターの実際のパフォーマンス計画と実行情報を表示することをサポートします。 [＃18056](https://github.com/pingcap/tidb/issues/18056)
-   `EXPLAIN FOR CONNECTION`ステートメントを使用して、実行中のすべてのSQLステートメントのリアルタイムステータスを確認することをサポートします。たとえば、ステートメントを使用して、各演算子の実行期間と処理された行の数を確認できます。 [＃18233](https://github.com/pingcap/tidb/issues/18233)
-   `EXPLAIN ANALYZE`ステートメントの出力で、オペレーターによって送信されたRPC要求の数、ロックの競合を解決する期間、ネットワークレイテンシー、RocksDBでスキャンされた削除データの量、RocksDBのヒット率など、オペレーターの実行に関する詳細を提供します。キャッシュ。 [＃18663](https://github.com/pingcap/tidb/issues/18663)
-   SQLステートメントの詳細な実行情報を低速ログに自動的に記録することをサポートします。スローログの実行情報は、各オペレーターが消費した時間、処理された行の数、送信されたRPC要求の数など、 `EXPLAIN ANALYZE`ステートメントの出力情報と一致しています。 [＃15009](https://github.com/pingcap/tidb/issues/15009)

## 展開とメンテナンス {#deployment-and-maintenance}

### クラスタ展開操作のロジックを最適化して、DBAが一連の標準TiDB本番クラスタをより高速に展開できるようにします {#optimize-the-logic-of-cluster-deployment-operations-to-help-dbas-deploy-a-set-of-standard-tidb-production-cluster-faster}

[ユーザードキュメント](/production-deployment-using-tiup.md)

以前のTiDBバージョンでは、TiUPを使用してTiDBクラスターを展開するDBAは、環境の初期化が複雑で、チェックサム構成が過剰であり、クラスタトポロジファイルを編集するのが難しいことに気付きました。これらの問題はすべて、DBAの展開効率を低下させます。 TiDB v5.0では、TiUPを使用したTiDBの展開効率が、次の項目を通じてDBAに対して改善されています。

-   TiUP Clusterは、より包括的なワンクリック環境チェックを実行し、修復の推奨事項を提供する`check topo.yaml`コマンドをサポートしています。
-   TiUP Clusterは、環境チェック中に見つかった環境問題を自動的に修復する`check topo.yaml --apply`コマンドをサポートしています。
-   TiUP Clusterは、DBAがグローバルノードパラメーターの変更を編集およびサポートするためのクラスタトポロジテンプレートファイルを取得するための`template`コマンドをサポートしています。
-   TiUPは、 `edit-config`コマンドを使用して`remote_config`パラメータを編集し、リモートPrometheusを設定することをサポートしています。
-   TiUPは、 `external_alertmanagers`パラメータの編集をサポートし、 `edit-config`コマンドを使用してさまざまなAlertManagerを設定します。
-   tiup-clusterの`edit-config`サブコマンドを使用してトポロジファイルを編集する場合、構成アイテム値のデータ型を変更できます。

### アップグレードの安定性を向上させる {#improve-upgrade-stability}

TiUP v1.4.0より前では、tiup-clusterを使用したTiDBクラスタのアップグレード中は、クラスタのSQL応答が長期間にわたってジッターし、PDオンラインローリングアップグレード中は、クラスタのQPSが10秒から30秒の間でジッターします。

TiUP v1.4.0はロジックを調整し、次の最適化を行います。

-   PDノードのアップグレード中に、TiUPは再起動されたPDノードのステータスを自動的にチェックし、ステータスの準備ができたことを確認した後、ロールして次のPDノードをアップグレードします。
-   TiUPはPDの役割を自動的に識別し、最初にフォロワーの役割のPDノードをアップグレードし、最後にPDリーダーノードをアップグレードします。

### アップグレード時間を最適化する {#optimize-the-upgrade-time}

TiUP v1.4.0より前では、DBAがtiup-clusterを使用してTiDBクラスターをアップグレードすると、ノード数が多いクラスターの場合、合計アップグレード時間が長くなり、特定のユーザーのアップグレード時間ウィンドウ要件を満たすことができません。

v1.4.0以降、TiUPは次の項目を最適化します。

-   `tiup cluster upgrade --offline`サブコマンドを使用した高速オフラインアップグレードをサポートします。
-   デフォルトでは、アップグレード中にローリングアップグレードを使用するユーザーのリージョンリーダーの再配置が高速化されるため、TiKVアップグレードのローリング時間が短縮されます。
-   ローリングアップグレードを実行する前に、 `check`サブコマンドを使用してリージョンモニターのステータスを確認します。アップグレードの前にクラスタが正常な状態にあることを確認して、アップグレードが失敗する可能性を減らします。

### ブレークポイント機能をサポートする {#support-the-breakpoint-feature}

TiUP v1.4.0より前では、DBAがtiup-clusterを使用してTiDBクラスターをアップグレードするときに、コマンドの実行が中断された場合、すべてのアップグレード操作を最初からやり直す必要があります。

TiUP v1.4.0は、アップグレードの中断後にすべての操作が再実行されないように、tiup `replay` cluster1サブコマンドを使用してブレークポイントから失敗した操作を再試行することをサポートしています。

### メンテナンスと運用の機能を強化する {#enhance-the-functionalities-of-maintenance-and-operations}

TiUP v1.4.0は、TiDBクラスターを操作および保守するための機能をさらに強化します。

-   より多くの使用シナリオに適応するために、ダウンタイムTiDBおよびDMクラスターでのアップグレードまたはパッチ操作をサポートします。
-   tiup-clusterの`display`サブコマンドに`--version`パラメーターを追加して、クラスタのバージョンを取得します。
-   スケールアウトされるノードにPrometheusのみが含まれている場合、Prometheusノードがないことによるスケールアウトの失敗を回避するために、監視構成を更新する操作は実行されません。
-   入力TiUPコマンドの結果が正しくない場合に、エラーメッセージにユーザー入力を追加して、問題の原因をより迅速に特定できるようにします。

## テレメトリー {#telemetry}

TiDBは、データテーブルの数、クエリの数、新機能が有効になっているかどうかなど、テレメトリにクラスタ使用状況メトリックを追加します。

詳細とこの動作を無効にする方法の詳細については、 [テレメトリー](/telemetry.md)を参照してください。
