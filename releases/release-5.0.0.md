---
title: What's New in TiDB 5.0
---

# TiDB 5.0 の新機能 {#what-s-new-in-tidb-5-0}

発売日：2021年4月7日

TiDB バージョン: 5.0.0

v5.0 では、PingCAP は、企業が TiDB に基づいてアプリケーションを迅速に構築できるように支援し、データベースのパフォーマンス、パフォーマンスのジッター、セキュリティ、高可用性、災害復旧、SQL パフォーマンスのトラブルシューティングなどに関する心配から企業を解放することに専念しています。

v5.0 の主な新機能または改善点は次のとおりです。

-   TiFlashノードを介して超並列処理 (MPP)アーキテクチャを導入し、大規模な結合クエリの実行ワークロードをTiFlashノード間で共有します。 MPP モードが有効な場合、TiDB はコストに基づいて、MPP フレームワークを使用して計算を実行するかどうかを決定します。 MPP モードでは、計算中に結合キーが`Exchange`の操作で再配布されるため、各TiFlashノードへの計算圧力が分散され、計算が高速化されます。ベンチマークによると、同じクラスター リソースを使用した場合、TiDB 5.0 MPP は Greenplum 6.15.0 および Apache Spark 3.1.1 と比較して 2 ～ 3 倍の高速化を示し、一部のクエリのパフォーマンスは 8 倍向上しています。
-   データベースのパフォーマンスを向上させるためにクラスター化インデックス機能を導入します。たとえば、TPC-C tpmC テストでは、クラスター化インデックスを有効にした TiDB のパフォーマンスが 39% 向上しました。
-   書き込みレイテンシーを短縮するには、非同期コミット機能を有効にします。たとえば、64 スレッドの Sysbench テストでは、非同期コミットを有効にした場合のインデックス更新の平均レイテンシーは、12.04 ミリ秒から 7.01 ミリ秒に 41.7% 減少しました。
-   ジッターを軽減します。これは、オプティマイザの安定性を向上させ、システム タスクによる I/O、ネットワーク、CPU、メモリリソースの使用量を制限することによって実現されます。たとえば、8 時間のパフォーマンス テストでは、TPC-C tpmC の標準偏差は 2% を超えません。
-   スケジューリングを改善し、実行計画を可能な限り安定に保つことで、システムの安定性を高めます。
-   Raft Joint Consensus アルゴリズムを導入し、リージョンのメンバーシップ変更中にシステムの可用性を確保します。
-   Optimize `EXPLAIN`機能と非表示のインデックスにより、データベース管理者 (DBA) が SQL ステートメントをより効率的にデバッグできるようになります。
-   企業データの信頼性を保証します。 TiDB から Amazon S3storageおよび Google Cloud GCS にデータをバックアップしたり、これらのクラウドstorageプラットフォームからデータを復元したりできます。
-   Amazon S3storageまたは TiDB/MySQL との間のデータのインポートまたはエクスポートのパフォーマンスが向上し、企業がクラウド上でアプリケーションを迅速に構築できるようになります。たとえば、TPC-C テストでは、1 TiB データをインポートするパフォーマンスが 254 GiB/h から 366 GiB/h に 40% 向上しました。

## 互換性の変更 {#compatibility-changes}

### システム変数 {#system-variables}

-   [`tidb_executor_concurrency`](/system-variables.md#tidb_executor_concurrency-new-in-v50)システム変数を追加して、複数のオペレータの同時実行性を制御します。以前の`tidb_*_concurrency`設定 ( `tidb_projection_concurrency`など) は引き続き有効ですが、使用すると警告が表示されます。

-   [`tidb_skip_ascii_check`](/system-variables.md#tidb_skip_ascii_check-new-in-v50)システム変数を追加して、ASCII 文字セットを書き込むときに ASCII 検証チェックをスキップするかどうかを指定します。このデフォルト値は`OFF`です。

-   [`tidb_enable_strict_double_type_check`](/system-variables.md#tidb_enable_strict_double_type_check-new-in-v50)システム変数を追加して、 `double(N)`のような構文をテーブル スキーマで定義できるかどうかを判断します。このデフォルト値は`OFF`です。

-   デフォルト値の[`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size)を`20000`から`0`に変更します。これは、バッチ DML ステートメントが`LOAD`ではデフォルトで使用されなくなったことを意味`INSERT INTO SELECT ...`ます。代わりに、厳密なACIDセマンティクスに準拠するために大規模なトランザクションが使用されます。

    > **注記：**
    >
    > 変数のスコープがセッションからグローバルに変更され、デフォルト値が`20000`から`0`に変更されます。アプリケーションが元のデフォルト値に依存している場合は、アップグレード後に`set global`ステートメントを使用して変数を元の値に変更する必要があります。

-   [`tidb_enable_noop_functions`](/system-variables.md#tidb_enable_noop_functions-new-in-v40)システム変数を使用して、一時テーブルの構文の互換性を制御します。この変数値が`OFF`の場合、 `CREATE TEMPORARY TABLE`構文はエラーを返します。

-   次のシステム変数を追加して、ガベージコレクション関連のパラメーターを直接制御します。
    -   [`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-new-in-v50)
    -   [`tidb_gc_enable`](/system-variables.md#tidb_gc_enable-new-in-v50)
    -   [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)
    -   [`tidb_gc_run_interval`](/system-variables.md#tidb_gc_run_interval-new-in-v50)
    -   [`tidb_gc_scan_lock_mode`](/system-variables.md#tidb_gc_scan_lock_mode-new-in-v50)

-   デフォルト値[`enable-joint-consensus`](/pd-configuration-file.md#enable-joint-consensus-new-in-v50)を`false`から`true`に変更します。これにより、ジョイント コンセンサス機能がデフォルトで有効になります。

-   `tidb_enable_amend_pessimistic_txn`の値を`0`または`1`から`ON`または`OFF`に変更します。

-   デフォルト値の[`tidb_enable_clustered_index`](/system-variables.md#tidb_enable_clustered_index-new-in-v50)次の新しい意味を持つ`OFF`から`INT_ONLY`に変更します。
    -   `ON` : クラスター化インデックスが有効になります。非クラスター化インデックスの追加または削除がサポートされています。

    -   `OFF` : クラスター化インデックスは無効です。非クラスター化インデックスの追加または削除がサポートされています。

    -   `INT_ONLY` : デフォルト値。この動作は v5.0 より前の動作と一致しています。 `alter-primary-key = false`と合わせて、INT タイプのクラスター化インデックスを有効にするかどうかを制御できます。
    > **注記：**
    >
    > 5.0 GA の`INT_ONLY`値`tidb_enable_clustered_index` 5.0 RC の`OFF`値と同じ意味を持ちます。 `OFF`設定の 5.0 RC クラスターから 5.0 GA にアップグレードすると、 `INT_ONLY`と表示されます。

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

-   TiDB の設定項目を[`index-limit`](/tidb-configuration-file.md#index-limit-new-in-v50)追加します。その値のデフォルトは`64`で、範囲は`[64,512]`です。 MySQL テーブルは最大 64 個のインデックスをサポートします。その値がデフォルト設定を超え、テーブルに 64 を超えるインデックスが作成された場合、テーブル スキーマが MySQL に再インポートされるときにエラーが報告されます。
-   MySQL の ENUM/SET 長 (ENUM 長 &lt; 255) と互換性および一貫性を持たせるために、TiDB の[`enable-enum-length-limit`](/tidb-configuration-file.md#enable-enum-length-limit-new-in-v50)構成項目を追加します。デフォルト値は`true`です。
-   `pessimistic-txn.enable`構成項目を[`tidb_txn_mode`](/system-variables.md#tidb_txn_mode)環境変数に置き換えます。
-   `performance.max-memory`構成項目を[`performance.server-memory-quota`](/tidb-configuration-file.md#server-memory-quota-new-in-v409)に置き換えます。
-   `tikv-client.copr-cache.enable`構成項目を[`tikv-client.copr-cache.capacity-mb`](/tidb-configuration-file.md#capacity-mb)に置き換えます。項目の値が`0.0`の場合、この機能は無効になります。項目の値が`0.0`より大きい場合、この機能は有効になります。デフォルト値は`1000.0`です。
-   `rocksdb.auto-tuned`構成項目を[`rocksdb.rate-limiter-auto-tuned`](/tikv-configuration-file.md#rate-limiter-auto-tuned-new-in-v50)に置き換えます。
-   `raftstore.sync-log`設定項目を削除します。デフォルトでは、書き込まれたデータは強制的にディスクに書き込まれます。 v5.0 より前では、 `raftstore.sync-log`明示的に無効にすることができます。 v5.0 以降、構成値は強制的に`true`に設定されます。
-   `gc.enable-compaction-filter`設定項目のデフォルト値を`false`から`true`に変更します。
-   `enable-cross-table-merge`設定項目のデフォルト値を`false`から`true`に変更します。
-   [`rate-limiter-auto-tuned`](/tikv-configuration-file.md#rate-limiter-auto-tuned-new-in-v50)設定項目のデフォルト値を`false`から`true`に変更します。

### その他 {#others}

-   アップグレードの前に、TiDB 構成の値を確認してください[`feedback-probability`](https://docs.pingcap.com/tidb/v5.0/tidb-configuration-file#feedback-probability) 。値が 0 でない場合、アップグレード後に「回復可能な goroutine のpanic」エラーが発生しますが、このエラーはアップグレードには影響しません。
-   データの正確性の問題を回避するために、列の型変更中に`VARCHAR`型と`CHAR`型の間の変換を禁止します。

## 新機能 {#new-features}

### SQL {#sql}

#### List パーティショニング(<strong>Experimental</strong>) {#list-partitioning-strong-experimental-strong}

[ユーザードキュメント](/partitioned-table.md#list-partitioning)

リスト パーティショニング機能を使用すると、大量のデータを含むテーブルのクエリと管理を効果的に行うことができます。

この機能を有効にすると、パーティションとパーティション間でのデータの分散方法が`PARTITION BY LIST(expr) PARTITION part_name VALUES IN (...)`式に従って定義されます。パーティション テーブルのデータ セットは、最大 1024 個の個別の整数値をサポートします。 `PARTITION ... VALUES IN (...)`句を使用して値を定義できます。

リストのパーティショニングを有効にするには、セッション変数を[`tidb_enable_list_partition`](/system-variables.md#tidb_enable_list_partition-new-in-v50)から`ON`に設定します。

#### List COLUMNS パーティショニング(<strong>Experimental</strong>) {#list-columns-partitioning-strong-experimental-strong}

[ユーザードキュメント](/partitioned-table.md#list-columns-partitioning)

List COLUMNS パーティショニングは、リスト パーティショニングの変形です。複数の列をパーティション キーとして使用できます。整数データ型のほかに、文字列、 `DATE` 、および`DATETIME`データ型の列をパーティション列として使用することもできます。

List COLUMNS パーティショニングを有効にするには、セッション変数を[`tidb_enable_list_partition`](/system-variables.md#tidb_enable_list_partition-new-in-v50)から`ON`に設定します。

#### 非表示のインデックス {#invisible-indexes}

[ユーザードキュメント](/sql-statements/sql-statement-alter-index.md) [#9246](https://github.com/pingcap/tidb/issues/9246)

パフォーマンスを調整したり、最適なインデックスを選択したりする場合、SQL ステートメントを使用してインデックスを`Visible`または`Invisible`に設定できます。この設定により、 `DROP INDEX`や`ADD INDEX`などのリソースを消費する操作の実行を回避できます。

インデックスの可視性を変更するには、 `ALTER INDEX`ステートメントを使用します。変更後、オプティマイザはインデックスの可視性に基づいて、このインデックスをインデックス リストに追加するかどうかを決定します。

#### <code>EXCEPT</code>演算子と<code>INTERSECT</code>演算子 {#code-except-code-and-code-intersect-code-operators}

[ユーザードキュメント](/functions-and-operators/set-operators.md) [#18031](https://github.com/pingcap/tidb/issues/18031)

`INTERSECT`演算子は集合演算子で、2 つ以上のクエリの結果セットの共通部分を返します。ある程度、これは`Inner Join`演算子の代替となります。

`EXCEPT`演算子は集合演算子で、2 つのクエリの結果セットを結合し、最初のクエリ結果には含まれるが 2 番目のクエリ結果には含まれない要素を返します。

### トランザクション {#transaction}

[#18005](https://github.com/pingcap/tidb/issues/18005)

悲観的トランザクション モードでは、トランザクションに関係するテーブルに同時 DDL 操作または`SCHEMA VERSION`の変更が含まれている場合、システムはトランザクションの`SCHEMA VERSION`最新のものに自動的に更新して、トランザクションのコミットが成功することを保証し、クライアントがエラー`Information schema is changed`を受け取るのを回避します。 DDL 操作または`SCHEMA VERSION`によってトランザクションが中断されました。

この機能はデフォルトでは無効になっています。この機能を有効にするには、 `tidb_enable_amend_pessimistic_txn`のシステム変数の値を変更します。この機能は v4.0.7 で導入され、v5.0 では次の問題が修正されています。

-   TiDB Binlog が`Add Column`オペレーションを実行するときに発生する互換性の問題
-   この機能を一意のインデックスと併用すると発生するデータの不整合の問題
-   追加されたインデックスとこの機能を併用するとデータの不整合の問題が発生する

現在、この機能には次の非互換性の問題がまだあります。

-   同時トランザクションがある場合、トランザクションのセマンティクスが変更される可能性があります
-   この機能を TiDB Binlogと併用すると発生する既知の互換性の問題
-   `Change Column`との互換性はありません

### 文字セットと照合順序 {#character-set-and-collation}

-   `utf8mb4_unicode_ci`および`utf8_unicode_ci`照合順序をサポートします。 [ユーザードキュメント](/character-set-and-collation.md#new-framework-for-collations) [#17596](https://github.com/pingcap/tidb/issues/17596)
-   照合順序で大文字と小文字を区別しない比較ソートをサポートする

### Security {#security}

[ユーザードキュメント](/log-redaction.md) [#18566](https://github.com/pingcap/tidb/issues/18566)

セキュリティ コンプライアンス要件 (*一般データ保護規則*(GDPR) など) を満たすために、システムは、出力エラー メッセージおよびログ内の情報 (ID やクレジット カード番号など) の機密性を解除することをサポートしており、機密情報の漏洩を回避できます。

TiDB は、出力ログ情報の感度を下げることをサポートしています。この機能を有効にするには、次のスイッチを使用します。

-   グローバル変数[`tidb_redact_log`](/system-variables.md#tidb_redact_log) 。デフォルト値は`0`で、感度解除が無効であることを意味します。 tidb-server ログの感度解除を有効にするには、変数値を`1`に設定します。
-   構成項目`security.redact-info-log` ．デフォルト値は`false`で、感度解除が無効であることを意味します。 tikv-server ログの感度解除を有効にするには、変数値を`true`に設定します。
-   構成項目`security.redact-info-log` ．デフォルト値は`false`で、感度解除が無効であることを意味します。 pd-server ログの感度解除を有効にするには、変数値を`true`に設定します。
-   設定項目`security.redact_info_log`は tflash-server 、 `security.redact-info-log`は tflash-learner です。デフォルト値はどちらも`false`で、感度解除が無効であることを意味します。 tiflash-server ログと tflash-learner ログの感度解除を有効にするには、両方の変数の値を`true`に設定します。

この機能は v5.0 で導入されました。この機能を使用するには、システム変数と上記のすべての設定項目を有効にします。

## パフォーマンスの最適化 {#performance-optimization}

### MPPアーキテクチャ {#mpp-architecture}

[ユーザードキュメント](/tiflash/use-tiflash-mpp-mode.md)

TiDB は、 TiFlashノードを通じて MPPアーキテクチャを導入します。このアーキテクチャ、複数のTiFlashノードが大規模な結合クエリの実行ワークロードを共有できます。

MPP モードがオンの場合、TiDB は計算コストに基づいて、計算のために MPP エンジンにクエリを送信するかどうかを決定します。 MPP モードでは、TiDB はデータ計算 ( `Exchange`操作) 中に結合キーを再配布することにより、テーブル結合の計算を実行中の各TiFlashノードに分散し、計算を高速化します。さらに、 TiFlashがすでにサポートしている集約コンピューティング機能を使用すると、TiDB はクエリの計算をTiFlash MPP クラスターにプッシュダウンできます。そうすれば、分散環境は実行プロセス全体を加速し、分析クエリの速度を大幅に向上させることができます。

TPC-H 100 ベンチマーク テストでは、 TiFlash MPP は、従来の分析データベースの分析エンジンや Hadoop 上の SQL を上回る大幅な処理速度を実現しました。このアーキテクチャを使用すると、最新のトランザクション データに対して大規模な分析クエリを直接実行でき、従来のオフライン分析ソリューションよりも高いパフォーマンスが得られます。ベンチマークによると、同じクラスター リソースを使用した場合、TiDB 5.0 MPP は Greenplum 6.15.0 および Apache Spark 3.1.1 と比較して 2 ～ 3 倍の高速化を示し、一部のクエリのパフォーマンスは 8 倍向上しています。

現在、MPP モードがサポートしていない主な機能は次のとおりです (詳細については、 [TiFlashを使用する](/tiflash/use-tiflash-mpp-mode.md)を参照してください)。

-   テーブルのパーティショニング
-   窓関数
-   照合
-   いくつかの組み込み関数
-   TiKV からのデータの読み取り
-   OOM 流出
-   連合
-   完全外部結合

### クラスター化インデックス {#clustered-index}

[ユーザードキュメント](/clustered-indexes.md) [#4841](https://github.com/pingcap/tidb/issues/4841)

テーブル構造を設計したり、データベースの動作を分析したりするときに、主キーを持つ一部の列がグループ化および並べ替えられることが多く、これらの列に対するクエリで特定の範囲のデータまたは少量のデータが返されることが多いことが判明した場合は、クラスタード インデックス機能を使用することをお勧めします。異なる値を持つデータが含まれており、対応するデータによって読み取りまたは書き込みのホットスポットの問題が発生することはありません。

クラスター化インデックス (一部のデータベース管理システムでは*インデックス構成テーブル*とも呼ばれます) は、テーブルのデータに関連付けられたstorage構造です。クラスター化インデックスを作成する場合、テーブルの 1 つ以上の列をインデックスのキーとして指定できます。 TiDB はこれらのキーを特定の構造に格納します。これにより、TiDB はキーに関連付けられた行を迅速かつ効率的に見つけることができるため、データのクエリと書き込みのパフォーマンスが向上します。

クラスター化インデックス機能を有効にすると、次の場合に TiDB のパフォーマンスが大幅に向上します (たとえば、TPC-C tpmC テストでは、クラスター化インデックスが有効になっている TiDB のパフォーマンスが 39% 向上しました)。

-   データが挿入されると、クラスター化インデックスにより、ネットワークからのインデックス データの書き込みが 1 回削減されます。
-   同等の条件を持つクエリに主キーのみが含まれる場合、クラスター化インデックスにより、ネットワークからのインデックス データの読み取りが 1 回削減されます。
-   範囲条件を含むクエリに主キーのみが含まれる場合、クラスター化インデックスにより、ネットワークからのインデックス データの複数回の読み取りが削減されます。
-   同等条件または範囲条件を含むクエリに主キー プレフィックスが含まれる場合、クラスター化インデックスにより、ネットワークからのインデックス データの複数回の読み取りが削減されます。

各テーブルは、クラスター化インデックスまたは非クラスター化インデックスのいずれかを使用して、データを並べ替えて保存できます。これら 2 つのstorage構造の違いは次のとおりです。

-   クラスター化インデックスを作成する場合、テーブル内の 1 つ以上の列をインデックスのキー値として指定できます。クラスター化インデックスは、キー値に従ってテーブルのデータを並べ替えて格納します。各テーブルにはクラスター化インデックスを 1 つだけ含めることができます。テーブルにクラスター化インデックスがある場合、そのテーブルはクラスター化インデックス テーブルと呼ばれます。それ以外の場合は、非クラスター化インデックス テーブルと呼ばれます。
-   非クラスター化インデックスを作成すると、テーブル内のデータは順序付けされていない構造で格納されます。 TiDB はデータの各行に一意の ROWID を自動的に割り当てるため、非クラスター化インデックスのキー値を明示的に指定する必要はありません。クエリ中に、ROWID は対応する行を見つけるために使用されます。データのクエリまたは挿入時には少なくとも 2 つのネットワーク I/O 操作が発生するため、クラスター化インデックスと比較してパフォーマンスが低下します。

テーブル データが変更されると、データベース システムはクラスター化インデックスと非クラスター化インデックスを自動的に維持します。

すべての主キーはデフォルトで非クラスター化インデックスとして作成されます。次の 2 つの方法のいずれかで、主キーをクラスター化インデックスまたは非クラスター化インデックスとして作成できます。

-   テーブル作成時にステートメントにキーワード`CLUSTERED | NONCLUSTERED`を指定すると、指定された方法でテーブルが作成されます。構文は次のとおりです。

```sql
CREATE TABLE `t` (`a` VARCHAR(255), `b` INT, PRIMARY KEY (`a`, `b`) CLUSTERED);
```

または

```sql
CREATE TABLE `t` (`a` VARCHAR(255) PRIMARY KEY CLUSTERED, `b` INT);
```

ステートメント`SHOW INDEX FROM tbl-name`を実行すると、テーブルにクラスター化インデックスがあるかどうかをクエリできます。

-   クラスター化インデックス機能を制御するには、システム変数`tidb_enable_clustered_index`を構成します。サポートされている値は`ON` 、 `OFF` 、および`INT_ONLY`です。
    -   `ON` : クラスタード・インデックス機能がすべてのタイプの主キーに対して有効であることを示します。非クラスター化インデックスの追加と削除がサポートされています。
    -   `OFF` : クラスタード・インデックス機能がすべてのタイプの主キーに対して無効になっていることを示します。非クラスター化インデックスの追加と削除がサポートされています。
    -   `INT_ONLY` : デフォルト値。変数が`INT_ONLY`に設定され、 `alter-primary-key` `false`に設定されている場合、単一の整数列で構成される主キーはデフォルトでクラスター化インデックスとして作成されます。この動作は、TiDB v5.0 以前のバージョンの動作と一致しています。

`CREATE TABLE`ステートメントにキーワード`CLUSTERED | NONCLUSTERED`含まれている場合、ステートメントはシステム変数と構成項目の構成をオーバーライドします。

ステートメントでキーワード`CLUSTERED | NONCLUSTERED`を指定してクラスター化インデックス機能を使用することをお勧めします。このようにして、TiDB は必要に応じてシステム内のクラスター化インデックスと非クラスター化インデックスのすべてのデータ型を同時に使用できるため、より柔軟になります。

`INT_ONLY`はこの機能に互換性を持たせるために一時的に使用され、将来非推奨になるため、 `tidb_enable_clustered_index = INT_ONLY`の使用は推奨されません。

クラスター化インデックスの制限は次のとおりです。

-   クラスター化インデックスと非クラスター化インデックス間の相互変換はサポートされていません。
-   クラスター化インデックスの削除はサポートされていません。
-   `ALTER TABLE`ステートメントを使用したクラスター化インデックスの追加、削除、および変更はサポートされていません。
-   クラスター化インデックスの再編成と再作成はサポートされていません。
-   インデックスの有効化または無効化はサポートされていません。つまり、非表示のインデックス機能はクラスター化インデックスに対しては効果的ではありません。
-   クラスター化インデックスとして`UNIQUE KEY`を作成することはサポートされていません。
-   クラスター化インデックス機能と TiDB Binlogの併用はサポートされていません。 TiDB Binlogが有効になった後、TiDB はクラスター化インデックスとして単一の整数主キーの作成のみをサポートします。 TiDB Binlog は、クラスター化インデックスを持つ既存のテーブルのデータ変更をダウンストリームに複製しません。
-   クラスター化インデックス機能と属性`SHARD_ROW_ID_BITS`および`PRE_SPLIT_REGIONS`の併用はサポートされていません。
-   クラスターが新しいバージョンにアップグレードされてからロールバックされる場合は、ロールバック前にテーブル データをエクスポートし、ロールバック後にデータをインポートすることにより、新しく追加されたテーブルをダウングレードする必要があります。他のテーブルには影響しません。

### 非同期コミット {#async-commit}

[ユーザードキュメント](/system-variables.md#tidb_enable_async_commit-new-in-v50) [#8316](https://github.com/tikv/tikv/issues/8316)

データベースのクライアントは、データベース システムがトランザクションのコミットを 2 フェーズ (2PC) で同期的に完了するのを待ちます。第 1 フェーズのコミットが成功した後、トランザクションは結果をクライアントに返し、システムは第 2 フェーズのコミット操作をバックグラウンドで非同期に実行して、トランザクションのコミットレイテンシーを短縮します。トランザクション書き込みに関与するリージョンが1 つだけの場合、2 番目のフェーズは直接省略され、トランザクションは 1 フェーズ コミットになります。

非同期コミット機能を有効にした後、同じハードウェアと構成で、Sysbench が 64 スレッドで更新インデックスをテストするように設定されている場合、平均レイテンシーは12.04 ミリ秒から 7.01 ミリ秒に 41.7% 減少します。

非同期コミット機能が有効になっている場合、ネットワーク インタラクションのレイテンシーを1 つ削減し、データ書き込みのパフォーマンスを向上させるために、データベース アプリケーション開発者は、トランザクションの整合性を線形整合性から[因果関係の一貫性](/transaction-overview.md#causal-consistency)に下げることを検討することをお勧めします。因果関係の一貫性を有効にする SQL ステートメントは`START TRANSACTION WITH CAUSAL CONSISTENCY`です。

因果的整合性を有効にした後、同じハードウェアと構成で、Sysbench が 64 スレッドで oltp_write_only をテストするように設定されている場合、平均レイテンシーは11.86 ミリ秒から 11.19 ミリ秒に 5.6% 減少しました。

トランザクションの一貫性が線形一貫性から因果的一貫性まで低下した後、アプリケーション内の複数のトランザクション間に相互依存性がない場合、トランザクションにはグローバルに一貫した順序がありません。

**非同期コミット機能は、新しく作成された v5.0 クラスターではデフォルトで有効になっています。**

この機能は、以前のバージョンから v5.0 にアップグレードされたクラスターではデフォルトで無効になっています。この機能は、 `set global tidb_enable_async_commit = ON;`および`set global tidb_enable_1pc = ON;`ステートメントを実行することで有効にできます。

非同期コミット機能の制限は次のとおりです。

-   直接のダウングレードはサポートされていません。

### コプロセッサーキャッシュ機能をデフォルトで有効にする {#enable-the-coprocessor-cache-feature-by-default}

[ユーザードキュメント](/tidb-configuration-file.md#tikv-clientcopr-cache-new-in-v400) [#18028](https://github.com/pingcap/tidb/issues/18028)

5.0 GA では、コプロセッサーキャッシュ機能がデフォルトで有効になっています。この機能が有効になった後、データ読み取りのレイテンシーを短縮するために、TiDB は tikv-server にプッシュダウンされた演算子の計算結果を tidb-server にキャッシュします。

コプロセッサーキャッシュ機能を無効にするには、 `tikv-client.copr-cache` `capacity-mb`設定項目を`0.0`に変更します。

### <code>delete from table where id &lt;? Limit ?</code>の実行パフォーマンスを向上させます。 <code>delete from table where id &lt;? Limit ?</code>声明 {#improve-the-execution-performance-of-code-delete-from-table-where-id-x3c-limit-code-statement}

[#18028](https://github.com/pingcap/tidb/issues/18028)

`delete from table where id <? limit ?`ステートメントの p99 パフォーマンスは 4 倍向上しました。

### ロードベース分割戦略を最適化して、一部の小さなテーブルのホットスポット読み取りシナリオでデータを分割できないというパフォーマンスの問題を解決します。 {#optimize-load-base-split-strategy-to-solve-the-performance-problem-that-data-cannot-be-split-in-some-small-table-hotspot-read-scenarios}

[#18005](https://github.com/pingcap/tidb/issues/18005)

## 安定性の向上 {#improve-stability}

### 不完全なスケジューリングによって引き起こされるパフォーマンスのジッター問題を最適化します。 {#optimize-the-performance-jitter-issue-caused-by-imperfect-scheduling}

[#18005](https://github.com/pingcap/tidb/issues/18005)

TiDB スケジューリング プロセスは、I/O、ネットワーク、CPU、メモリなどのリソースを占有します。 TiDB がスケジュールされたタスクを制御しない場合、QPS と遅延により、リソースのプリエンプションによるパフォーマンスのジッターが発生する可能性があります。

次の最適化後、8 時間のパフォーマンス テストで、TPC-C tpmC の標準偏差は 2% を超えません。

#### 新しいスケジューリング計算式を導入して、不必要なスケジューリングとパフォーマンスのジッターを削減します。 {#introduce-new-scheduling-calculation-formulas-to-reduce-unnecessary-scheduling-and-performance-jitter}

ノード容量が常にシステムに設定されているウォーターラインに近い場合、または`store-limit`の設定が大きすぎる場合、容量負荷のバランスをとるために、システムは頻繁にリージョンを他のノードにスケジュールしたり、リージョンを元のノードに戻すようにスケジュールしたりすることがあります。スケジューリングは I/O、ネットワーク、CPU、メモリなどのリソースを占有し、パフォーマンスのジッターを引き起こすため、このタイプのスケジューリングは必要ありません。

この問題を軽減するために、PD はデフォルトのスケジューリング計算式の新しいセットを導入しました。 `region-score-formula-version = v1`を設定すると、古い式に戻すことができます。

#### デフォルトでクロステーブルリージョンマージ機能を有効にする {#enable-the-cross-table-region-merge-feature-by-default}

[ユーザードキュメント](/pd-configuration-file.md#enable-cross-table-merge)

v5.0 より前では、TiDB はデフォルトでクロステーブルリージョンマージ機能を無効にしています。 v5.0 以降、空のリージョンの数とネットワーク、メモリ、CPU のオーバーヘッドを削減するために、この機能はデフォルトで有効になっています。 `schedule.enable-cross-table-merge`構成項目を変更することで、この機能を無効にできます。

#### システムがデフォルトでデータ圧縮速度を自動的に調整し、バックグラウンド タスクとフォアグラウンドの読み取りおよび書き込みの間の I/O リソースの競合のバランスを取ることができるようにします。 {#enable-the-system-to-automatically-adjust-the-data-compaction-speed-by-default-to-balance-the-contention-for-i-o-resources-between-background-tasks-and-foreground-reads-and-writes}

[ユーザードキュメント](/tikv-configuration-file.md#rate-limiter-auto-tuned-new-in-v50)

v5.0 より前では、バックグラウンド タスクとフォアグラウンドの読み取りおよび書き込みの間の I/O リソースの競合のバランスを取るために、システムがデータ圧縮速度を自動的に調整する機能はデフォルトで無効になっていました。 v5.0 以降、TiDB はデフォルトでこの機能を有効にし、アルゴリズムを最適化してレイテンシーのジッターが大幅に減少します。

`rate-limiter-auto-tuned`構成項目を変更することで、この機能を無効にできます。

#### デフォルトで GC 圧縮フィルター機能を有効にして、GC による CPU および I/O リソースの消費を削減します。 {#enable-the-gc-compaction-filter-feature-by-default-to-reduce-gc-s-consumption-of-cpu-and-i-o-resources}

[ユーザードキュメント](/garbage-collection-configuration.md#gc-in-compaction-filter) [#18009](https://github.com/pingcap/tidb/issues/18009)

TiDB がガベージコレクション(GC) とデータ圧縮を実行すると、パーティションが CPU と I/O リソースを占有します。これら 2 つのタスクの実行中に、重複するデータが存在します。

GC による CPU および I/O リソースの消費を削減するために、GC 圧縮フィルター機能はこれら 2 つのタスクを 1 つに結合し、同じタスク内で実行します。この機能はデフォルトで有効になっています。 `gc.enable-compaction-filter = false`を設定することで無効にできます。

#### TiFlash は、圧縮とデータの並べ替えによる I/O リソースの使用を制限します (<strong>実験的機能</strong>) {#tiflash-limits-the-compression-and-data-sorting-s-use-of-i-o-resources-strong-experimental-feature-strong}

この機能は、バックグラウンド タスクとフォアグラウンドの読み取りおよび書き込みの間の I/O リソースの競合を軽減します。

この機能はデフォルトでは無効になっています。この機能は、 `bg_task_io_rate_limit`構成項目を変更することで有効にできます。

#### スケジューリング制約をチェックするパフォーマンスと、大規模なクラスター内の異常なリージョンを修正するパフォーマンスを向上させます。 {#improve-the-performance-of-checking-scheduling-constraints-and-the-performance-of-fixing-the-unhealthy-regions-in-a-large-cluster}

### パフォーマンスのジッターを避けるために、実行計画が可能な限り変更されていないことを確認します。 {#ensure-that-the-execution-plans-are-unchanged-as-much-as-possible-to-avoid-performance-jitter}

[ユーザードキュメント](/sql-plan-management.md)

#### SQL バインディングは、 <code>INSERT</code> 、 <code>REPLACE</code> 、 <code>UPDATE</code> 、 <code>DELETE</code>ステートメントをサポートします {#sql-binding-supports-the-code-insert-code-code-replace-code-code-update-code-code-delete-code-statements}

パフォーマンスのチューニングまたはデータベースの保守時に、実行計画が不安定なためにシステムのパフォーマンスが不安定であることが判明した場合は、判断に従って手動で最適化された SQL ステートメントを選択するか、 `EXPLAIN ANALYZE`によってテストすることができます。最適化された SQL ステートメントをアプリケーション コードで実行される SQL ステートメントにバインドして、安定したパフォーマンスを確保できます。

SQL BINDING ステートメントを使用して SQL ステートメントを手動でバインドする場合は、最適化された SQL ステートメントが元の SQL ステートメントと同じ構文を持つことを確認する必要があります。

`SHOW {GLOBAL | SESSION} BINDINGS`コマンドを実行すると、手動または自動でバインドされた実行計画情報を表示できます。出力は v5.0 より前のバージョンと同じです。

#### 実行計画を自動的にキャプチャしてバインドする {#automatically-capture-and-bind-execution-plans}

TiDB をアップグレードする場合、パフォーマンスのジッターを回避するために、ベースライン キャプチャ機能を有効にして、システムが最新の実行プランを自動的にキャプチャしてバインドし、システム テーブルに保存できるようにすることができます。 TiDB がアップグレードされた後、 `SHOW GLOBAL BINDING`コマンドを実行してバインドされた実行プランをエクスポートし、これらのプランを削除するかどうかを決定できます。

この機能はデフォルトでは無効になっています。これを有効にするには、サーバーを変更するか、グローバル システム変数`tidb_capture_plan_baselines`を`ON`に設定します。この機能が有効な場合、システムはステートメントの概要から少なくとも 2 回出現する SQL ステートメントを`bind-info-lease`ごとにフェッチし (デフォルト値は`3s` )、これらの SQL ステートメントを自動的にキャプチャしてバインドします。

### TiFlashクエリの安定性の向上 {#improve-stability-of-tiflash-queries}

TiFlash が失敗した場合に TiKV にクエリをフォールバックするためのシステム変数[`tidb_allow_fallback_to_tikv`](/system-variables.md#tidb_allow_fallback_to_tikv-new-in-v50)を追加します。デフォルト値は`OFF`です。

### TiCDC の安定性を向上させ、増分データの複製が多すぎることによって引き起こされる OOM 問題を軽減します。 {#improve-ticdc-stability-and-alleviate-the-oom-issue-caused-by-replicating-too-much-incremental-data}

[ユーザードキュメント](/ticdc/ticdc-manage-changefeed.md#unified-sorter) [#1150](https://github.com/pingcap/tiflow/issues/1150)

TiCDC v4.0.9 以前のバージョンでは、あまりにも多くのデータ変更をレプリケートすると OOM が発生する可能性があります。 v5.0 では、次のシナリオによって発生する OOM 問題を軽減するために、統合ソーター機能がデフォルトで有効になっています。

-   TiCDC のデータ複製タスクは長時間停止され、その間に大量の増分データが蓄積され、複製する必要があります。
-   データ複製タスクは早いタイムスタンプから開始されるため、大量の増分データを複製する必要があります。

統合ソーターは、以前のバージョンの`memory` / `file`ソート エンジン オプションと統合されています。変更を手動で構成する必要はありません。

制限事項:

-   増分データの量に応じて十分なディスク容量を用意する必要があります。空き容量が 128 GB を超える SSD を使用することをお勧めします。

## 高可用性と災害復旧 {#high-availability-and-disaster-recovery}

### リージョンのメンバーシップ変更時のシステム可用性の向上 {#improve-system-availability-during-region-membership-change}

[ユーザードキュメント](/pd-configuration-file.md#enable-joint-consensus-new-in-v50) [#18079](https://github.com/pingcap/tidb/issues/18079) [#7587](https://github.com/tikv/tikv/issues/7587) [#2860](https://github.com/tikv/pd/issues/2860)

リージョンのメンバーシップ変更のプロセスでは、「メンバーの追加」と「メンバーの削除」の 2 つの操作が 2 つのステップで実行されます。メンバーシップの変更が完了するときに障害が発生すると、リージョンは使用できなくなり、フォアグラウンド アプリケーションのエラーが返されます。

導入されたRaft Joint Consensus アルゴリズムにより、リージョンのメンバーシップ変更時のシステムの可用性が向上します。会員変更時の「会員追加」と「会員削除」の操作を一つにまとめて全会員に送信します。変更プロセス中、リージョンは中間状態になります。変更されたメンバーのいずれかが失敗した場合でも、システムは引き続き使用できます。

この機能はデフォルトで有効になっています。これを無効にするには、 `pd-ctl config set enable-joint-consensus`コマンドを実行して`enable-joint-consensus`値を`false`に設定します。

### メモリ管理モジュールを最適化してシステム OOM リスクを軽減する {#optimize-the-memory-management-module-to-reduce-system-oom-risks}

集計関数のメモリ使用量を追跡します。この機能はデフォルトで有効になっています。集計関数を含む SQL ステートメントが実行されるとき、現在のクエリの合計メモリ使用量が`mem-quota-query`で設定されたしきい値を超えると、システムは`oom-action`で定義された操作を自動的に実行します。

### ネットワーク分割中のシステムの可用性を向上させる {#improve-the-system-availability-during-network-partition}

## データ移行 {#data-migration}

### S3/ Auroraから TiDB にデータを移行する {#migrate-data-from-s3-aurora-to-tidb}

TiDB データ移行ツールは、データ移行の中間として Amazon S3 (およびその他の S3 互換storageサービス) の使用と、 Auroraスナップショット データを TiDB に直接初期化することをサポートし、Amazon S3/ Auroraから TiDB へのデータ移行のためのより多くのオプションを提供します。

この機能を使用するには、次のドキュメントを参照してください。

-   [データを Amazon S3 クラウドstorageにエクスポートする](/dumpling-overview.md#export-data-to-amazon-s3-cloud-storage) [#8](https://github.com/pingcap/dumpling/issues/8)
-   [TiDB Lightningを使用した Amazon Aurora MySQL からの移行](/migrate-aurora-to-tidb.md) [#266](https://github.com/pingcap/tidb-lightning/issues/266)

### TiDB Cloudのデータインポートパフォーマンスを最適化する {#optimize-the-data-import-performance-of-tidb-cloud}

TiDB Lightning は、特にTiDB Cloudの AWS T1.standard 構成 (または同等のもの) 向けにデータ インポート パフォーマンスを最適化します。テスト結果では、 TiDB Lightning、1 TB の TPC-C データを TiDB にインポートする速度が 254 GiB/h から 366 GiB/h に 40% 向上したことがわかりました。

## データの共有とサブスクリプション {#data-sharing-and-subscription}

### TiCDC を使用して TiDB を Kafka Connect (Confluent Platform) に統合する (<strong>実験的機能</strong>) {#integrate-tidb-to-kafka-connect-confluent-platform-using-ticdc-strong-experimental-feature-strong}

[ユーザードキュメント](/ticdc/integrate-confluent-using-ticdc.md) [#660](https://github.com/pingcap/tiflow/issues/660)

TiDB データを他のシステムにストリーミングするというビジネス要件をサポートするために、この機能を使用すると、TiDB データを Kafka、Hadoop、Oracle などのシステムにストリーミングできるようになります。

Confluent プラットフォームによって提供される Kafka コネクタ プロトコルはコミュニティで広く使用されており、さまざまなプロトコルでのリレーショナル データベースまたは非リレーショナル データベースへのデータ転送をサポートしています。 TiCDC を Confluent プラットフォームの Kafka Connect に統合することにより、TiDB は TiDB データを他の異種データベースやシステムにストリーミングする機能を拡張します。

## 診断 {#diagnostics}

[ユーザードキュメント](/sql-statements/sql-statement-explain.md#explain)

SQL パフォーマンス問題のトラブルシューティングでは、パフォーマンス問題の原因を特定するために詳細な診断情報が必要です。 TiDB 5.0 より前は、 `EXPLAIN`ステートメントによって収集される情報の詳細が十分ではありませんでした。問題の根本原因は、ログ情報、監視情報、または推測に基づいてのみ判断でき、非効率である可能性があります。

TiDB v5.0 では、パフォーマンスの問題をより効率的にトラブルシューティングできるように、次の改良が加えられています。

-   `EXPLAIN ANALYZE`ステートメントを使用したすべての DML ステートメントの分析をサポートし、実際のパフォーマンス プランと各オペレーターの実行情報を表示します。 [#18056](https://github.com/pingcap/tidb/issues/18056)
-   `EXPLAIN FOR CONNECTION`ステートメントを使用して、実行されているすべての SQL ステートメントのリアルタイム ステータスを確認できるようになりました。たとえば、このステートメントを使用して、各演算子の実行時間と処理された行数を確認できます。 [#18233](https://github.com/pingcap/tidb/issues/18233)
-   `EXPLAIN ANALYZE`ステートメントの出力で、オペレーターによって送信された RPC リクエストの数、ロック競合の解決にかかる時間、ネットワークレイテンシー時間、RocksDB 内の削除されたデータのスキャン量、RocksDB のヒット率など、オペレーターの実行に関する詳細を提供します。キャッシュ。 [#18663](https://github.com/pingcap/tidb/issues/18663)
-   SQL ステートメントの詳細な実行情報をスロー ログに自動的に記録する機能をサポートします。低速ログの実行情報は、各オペレーターが費やした時間、処理された行数、送信された RPC リクエストの数を含む、 `EXPLAIN ANALYZE`ステートメントの出力情報と一致しています。 [#15009](https://github.com/pingcap/tidb/issues/15009)

## 導入とメンテナンス {#deployment-and-maintenance}

### クラスター展開操作のロジックを最適化し、DBA が一連の標準 TiDB本番クラスターをより迅速に展開できるようにします。 {#optimize-the-logic-of-cluster-deployment-operations-to-help-dbas-deploy-a-set-of-standard-tidb-production-cluster-faster}

[ユーザードキュメント](/production-deployment-using-tiup.md)

以前の TiDB バージョンでは、 TiUPを使用して TiDB クラスターを展開する DBA は、環境の初期化が複雑で、チェックサム構成が過剰で、クラスター トポロジー ファイルの編集が難しいことに気づきました。これらの問題はすべて、DBA の導入効率の低下につながります。 TiDB v5.0 では、 TiUPを使用した TiDB デプロイメント効率が、次の項目によって DBA 向けに向上しました。

-   TiUP クラスタ は、より包括的なワンクリック環境チェックを実行し、修復の推奨事項を提供する`check topo.yaml`コマンドをサポートしています。
-   TiUP クラスタ は、環境チェック中に検出された環境問題を自動的に修復する`check topo.yaml --apply`コマンドをサポートしています。
-   TiUP クラスタ は、 DBA が編集するためのクラスタ トポロジ テンプレート ファイルを取得する`template`コマンドをサポートし、グローバル ノード パラメータの変更をサポートします。
-   TiUP は、リモート Prometheus を構成するための`edit-config`コマンドを使用した`remote_config`パラメータの編集をサポートしています。
-   TiUP は、 `edit-config`コマンドを使用して異なる AlertManager を設定するための`external_alertmanagers`パラメータの編集をサポートしています。
-   tiup-clusterの`edit-config`サブコマンドを使用してトポロジ ファイルを編集するときに、構成項目の値のデータ型を変更できます。

### アップグレードの安定性の向上 {#improve-upgrade-stability}

TiUP v1.4.0 より前では、 tiup-clusterを使用した TiDB クラスターのアップグレード中に、クラスターの SQL 応答が長期間にわたってジッターし、PD オンライン ローリング アップグレード中に、クラスターの QPS が 10 秒から 30 秒の間でジッターを発生しました。

TiUP v1.4.0 はロジックを調整し、次の最適化を行います。

-   PD ノードのアップグレード中に、 TiUP は再起動された PD ノードのステータスを自動的にチェックし、ステータスが準備完了であることを確認した後、次の PD ノードのアップグレードを開始します。
-   TiUP はPD ロールを自動的に識別し、最初にフォロワー ロールの PD ノードをアップグレードし、最後に PDLeaderノードをアップグレードします。

### アップグレード時間を最適化する {#optimize-the-upgrade-time}

TiUP v1.4.0 より前では、DBA がtiup-clusterを使用して TiDB クラスターをアップグレードする場合、ノード数が多いクラスターの場合、アップグレードの合計時間が長くなり、特定のユーザーのアップグレード時間枠の要件を満たすことができませんでした。

v1.4.0 以降、 TiUP は次の項目を最適化します。

-   `tiup cluster upgrade --offline`サブコマンドを使用した高速オフライン アップグレードをサポートします。
-   デフォルトでアップグレード中にローリング アップグレードを使用するユーザーのリージョンLeaderの再配置が高速化されるため、TiKV のローリング アップグレードの時間が短縮されます。
-   ローリング アップグレードを実行する前に、 `check`サブコマンドを使用してリージョンモニターのステータスを確認します。アップグレード前にクラスターが通常の状態であることを確認して、アップグレードが失敗する可能性を減らします。

### ブレークポイント機能をサポートする {#support-the-breakpoint-feature}

TiUP v1.4.0 より前では、DBA がtiup-cluster を使用して TiDB クラスターをアップグレードする場合、コマンドの実行が中断されると、すべてのアップグレード操作を最初から再実行する必要がありました。

TiUP v1.4.0 は、アップグレードの中断後にすべての操作が再実行されることを避けるために、 tiup-cluster `replay`サブコマンドを使用したブレークポイントからの失敗した操作の再試行をサポートしています。

### 保守・運用機能の強化 {#enhance-the-functionalities-of-maintenance-and-operations}

TiUP v1.4.0 では、TiDB クラスターの運用および保守のための機能がさらに強化されています。

-   より多くの使用シナリオに適応するために、ダウンタイム TiDB および DM クラスターでのアップグレードまたはパッチ操作をサポートします。
-   tiup-clusterの`display`サブコマンドに`--version`パラメータを追加して、クラスターのバージョンを取得します。
-   スケールアウト対象ノードにPrometheusのみが含まれている場合、Prometheusノードの不在によるスケールアウト失敗を回避するため、監視構成の更新操作は行われません。
-   入力したTiUPコマンドの結果が正しくない場合に、エラー メッセージにユーザー入力を追加して、問題の原因をより迅速に特定できるようにします。

## テレメトリー {#telemetry}

TiDB は、データ テーブルの数、クエリの数、新機能が有効になっているかどうかなど、クラスターの使用状況メトリクスをテレメトリに追加します。

詳細とこの動作を無効にする方法については、 [テレメトリー](/telemetry.md)を参照してください。
