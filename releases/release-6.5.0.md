---
title: TiDB 6.5.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 6.5.0.
---

# TiDB 6.5.0 リリースノート {#tidb-6-5-0-release-notes}

発売日：2022年12月29日

TiDB バージョン: 6.5.0

クイックアクセス: [インストールパッケージ](https://www.pingcap.com/download/?version=v6.5.0#version-list)

TiDB 6.5.0 は長期サポート リリース (LTS) です。

以前の LTS 6.1.0 と比較して、6.5.0 には[6.4.0-DMR](/releases/release-6.4.0.md)でリリースされた新機能、改善、バグ修正が含まれているだけでなく、次の主要な機能と改善も導入されています。

-   [インデックス加速度](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)機能が一般公開 (GA) され、インデックス追加のパフォーマンスが v6.1.0 と比較して約 10 倍向上しました。
-   TiDB グローバルメモリコントロールが GA になり、 [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)を介してメモリ消費のしきい値を制御できるようになります。
-   高性能でグローバルに単調な[`AUTO_INCREMENT`](/auto-increment.md#mysql-compatibility-mode)カラム属性が GA となり、MySQL と互換性があります。
-   [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md)は TiCDC および PITR と互換性があり、GA になりました。
-   より正確な[インデックスのマージ](/explain-index-merge.md)で接続された式をサポートすることにより、TiDB オプティマイザーを強化します。
-   `JSON_EXTRACT()`機能のTiFlashへのプッシュダウンをサポートします。
-   パスワード コンプライアンスの監査要件を満たす[パスワード管理](/password-management.md)ポリシーをサポートします。
-   TiDB LightningおよびDumpling は、 [輸出する](/dumpling-overview.md#improve-export-efficiency-through-concurrency)の圧縮 SQL および CSV ファイルをサポートしています。
-   TiDB データ移行 (DM) [継続的なデータ検証](/dm/dm-continuous-data-validation.md) GA になります。
-   TiDB バックアップ &amp; リストアは、スナップショット チェックポイント バックアップをサポートし、 [PITR](/br/br-pitr-guide.md#run-pitr)リカバリ パフォーマンスを 50% 向上させ、一般的なシナリオでの RPO を最短 5 分に短縮します。
-   TiCDC スループット[Kafka へのデータの複製](/replicate-data-to-kafka.md)が 4000 行/秒から 35000 行/秒に向上し、レプリケーションのレイテンシーが2 秒に短縮されます。
-   データのライフサイクルを管理するために行レベル[生存時間 (TTL)](/time-to-live.md)を提供します (実験的)。
-   TiCDC は、Amazon S3、Azure Blob Storage、NFS (実験的) など[変更されたログをオブジェクトstorageにレプリケートする](/ticdc/ticdc-sink-to-cloud-storage.md)をサポートします。

## 新機能 {#new-features}

### SQL {#sql}

-   インデックスを追加する TiDB のパフォーマンスが約 10 倍向上しました (GA) [タンジェンタ](https://github.com/tangenta)

    TiDB v6.3.0 では、インデックス作成時のバックフィルの速度を向上させるための実験的機能として[インデックスアクセラレーションを追加](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)が導入されています。 v6.5.0 では、この機能が GA となり、デフォルトで有効になり、大規模なテーブルでのパフォーマンスが v6.1.0 よりも約 10 倍高速になることが予想されます。高速化機能は、単一の SQL ステートメントでインデックスを連続的に追加するシナリオに適しています。複数の SQL ステートメントが並行してインデックスを追加する場合、SQL ステートメントのうち 1 つだけが高速化されます。

-   軽量メタデータ ロックを提供して、DDL 変更時の DML 成功率 (GA) [wjhuang2016](https://github.com/wjhuang2016)を向上させます。

    TiDB v6.3.0 では、実験的機能として[`tidb_enable_metadata_lock`](/system-variables.md#tidb_enable_metadata_lock-new-in-v630) `OFF`に設定します。

    詳細については、 [ドキュメンテーション](/metadata-lock.md)を参照してください。

-   `FLASHBACK CLUSTER TO TIMESTAMP` (GA) [カルビンネオ](https://github.com/CalvinNeo)を使用した、特定の時点へのクラスターの復元のサポート

    v6.4.0 以降、TiDB は実験的機能として[`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md)ステートメントを導入しました。このステートメントを使用すると、ガベージ コレクション (GC) の有効期間内の特定の時点にクラスターを復元できます。 v6.5.0 では、この機能は TiCDC および PITR と互換性があり、GA になりました。この機能は、DML の誤った操作を簡単に元に戻し、数分で元のクラスターを復元し、さまざまな時点でデータをロールバックしてデータが変更された正確な時間を判断するのに役立ちます。

    詳細については、 [ドキュメンテーション](/sql-statements/sql-statement-flashback-to-timestamp.md)を参照してください。

-   `INSERT` 、 `REPLACE` 、 `UPDATE` 、 `DELETE` [エキシウム](https://github.com/ekexium)を含む非トランザクション DML ステートメントを完全にサポートします。

    大規模なデータ処理のシナリオでは、大規模なトランザクションを含む 1 つの SQL ステートメントがクラスターの安定性とパフォーマンスに悪影響を与える可能性があります。非トランザクション DML ステートメントは、内部実行のために複数の SQL ステートメントに分割された DML ステートメントです。分割ステートメントはトランザクションの原子性と分離性を損ないますが、クラスターの安定性は大幅に向上します。 TiDB は、v6.1.0 以降、非トランザクション`DELETE`ステートメントをサポートし、v6.5.0 以降、非トランザクション`INSERT` 、 `REPLACE` 、および`UPDATE`ステートメントをサポートしています。

    詳細については、 [`BATCH`構文](/sql-statements/sql-statement-batch.md)を参照してください。

-   生存時間 (TTL) (実験的) [ルクワンチャオ](https://github.com/lcwangchao)のサポート

    TTL は行レベルのデータ有効期間管理を提供します。 TiDB では、TTL 属性を持つテーブルはデータの有効期間を自動的にチェックし、期限切れのデータを行レベルで削除します。 TTL は、オンラインの読み取りおよび書き込みのワークロードに影響を与えることなく、不要なデータを定期的かつタイムリーにクリーンアップできるように設計されています。

    詳細については、 [ドキュメンテーション](/time-to-live.md)を参照してください。

-   `INSERT INTO SELECT`ステートメントを使用したTiFlashクエリ結果の保存をサポート (実験的) [ゲンリキ](https://github.com/gengliqi)

    v6.5.0 以降、TiDB は`INSERT INTO SELECT`ステートメントの`SELECT`句 (分析クエリ) をTiFlashにプッシュダウンすることをサポートします。このようにして、さらに分析するために、 TiFlashクエリ結果を`INSERT INTO`で指定された TiDB テーブルに簡単に保存できます。これは、結果のキャッシュ (つまり、結果の具体化) として有効になります。例えば：

    ```sql
    INSERT INTO t2 SELECT Mod(x,y) FROM t1;
    ```

    実験的段階では、この機能はデフォルトで無効になっています。これを有効にするには、 [`tidb_enable_tiflash_read_for_write_stmt`](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-new-in-v630)システム変数を`ON`に設定します。この機能の`INSERT INTO`で指定される結果テーブルには特別な制限はなく、その結果テーブルにTiFlashレプリカを追加するかどうかは自由です。この機能の一般的な使用シナリオは次のとおりです。

    -   TiFlashを使用して複雑な分析クエリを実行する
    -   TiFlashクエリ結果を再利用するか、高度な同時オンライン要求に対処します
    -   入力データ サイズと比較して比較的小さい結果セットが必要です。できれば 100 MiB 未満です。

    詳細については、 [ドキュメンテーション](/tiflash/tiflash-results-materialization.md)を参照してください。

-   バインディング履歴実行プランのサポート (実験的) [fzzf678](https://github.com/fzzf678)

    SQL ステートメントの場合、実行中のさまざまな要因により、オプティマイザが以前の最適な実行プランではなく新しい実行プランを選択することがあり、SQL パフォーマンスに影響が及びます。この場合、最適な実行計画がクリアされていない場合は、SQL 実行履歴に残ります。

    v6.5.0 では、TiDB は[`CREATE [GLOBAL | SESSION] BINDING`](/sql-statements/sql-statement-create-binding.md)ステートメントのバインディング オブジェクトを拡張することにより、履歴実行プランのバインディングをサポートします。 SQL ステートメントの実行計画が変更された場合、元の実行計画が SQL 実行履歴メモリテーブルに残っている限り、 `CREATE [GLOBAL | SESSION] BINDING`ステートメントに`plan_digest`指定して元の実行計画をバインドし、SQL パフォーマンスを迅速に回復できます (たとえば、 `statements_summary` ）。この機能により、実行計画の変更の問題を処理するプロセスが簡素化され、メンテナンスの効率が向上します。

    詳細については、 [ドキュメンテーション](/sql-plan-management.md#create-a-binding-according-to-a-historical-execution-plan)を参照してください。

### Security {#security}

-   パスワードの複雑さのポリシー[Cbcウェストウルフ](https://github.com/CbcWestwolf)をサポートします。

    このポリシーを有効にした後、パスワードを設定すると、TiDB はパスワードの長さ、パスワード内の大文字と小文字、数字、特殊文字が十分であるかどうか、パスワードが辞書と一致するかどうか、およびパスワードがユーザー名と一致するかどうかをチェックします。これにより、安全なパスワードを設定できます。

    TiDB は、パスワードの強度を検証する SQL 関数[`VALIDATE_PASSWORD_STRENGTH()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_validate-password-strength)を提供します。

    詳細については、 [ドキュメンテーション](/password-management.md#password-complexity-policy)を参照してください。

-   パスワード有効期限ポリシー[Cbcウェストウルフ](https://github.com/CbcWestwolf)のサポート

    TiDB は、手動有効期限、グローバルレベルの自動有効期限、アカウントレベルの自動有効期限などのパスワード有効期限ポリシーの構成をサポートしています。このポリシーを有効にした後は、パスワードを定期的に変更する必要があります。これにより、長期使用によるパスワード漏洩のリスクが軽減され、パスワードのセキュリティが向上します。

    詳細については、 [ドキュメンテーション](/password-management.md#password-expiration-policy)を参照してください。

-   パスワード再利用ポリシー[キープラーニング20221](https://github.com/keeplearning20221)のサポート

    TiDB は、グローバル レベルのパスワード再利用ポリシーやアカウント レベルのパスワード再利用ポリシーなど、パスワード再利用ポリシーの構成をサポートしています。このポリシーを有効にすると、指定した期間内に使用したパスワード、または最近使用したいくつかのパスワードは使用できなくなります。これにより、パスワードの繰り返し使用によるパスワード漏洩のリスクが軽減され、パスワードのセキュリティが向上します。

    詳細については、 [ドキュメンテーション](/password-management.md#password-reuse-policy)を参照してください。

-   失敗したログインの追跡と一時的なアカウント ロック ポリシー[最後切歯](https://github.com/lastincisor)をサポート

    このポリシーを有効にした後、間違ったパスワードを連続して複数回使用して TiDB にログインすると、アカウントは一時的にロックされます。ロック時間が終了すると、アカウントのロックは自動的に解除されます。

    詳細については、 [ドキュメンテーション](/password-management.md#failed-login-tracking-and-temporary-account-locking-policy)を参照してください。

### 可観測性 {#observability}

-   TiDB ダッシュボードは、独立したポッド[サバピン](https://github.com/SabaPing)として Kubernetes にデプロイできます。

    TiDB v6.5.0 (以降) およびTiDB Operator v1.4.0 (以降) は、Kubernetes 上の独立したポッドとして TiDB ダッシュボードをデプロイすることをサポートしています。 TiDB Operatorを使用すると、このポッドの IP アドレスにアクセスして TiDB ダッシュボードを起動できます。

    TiDB ダッシュボードを独立して展開すると、次の利点があります。

    -   TiDB ダッシュボードのコンピューティング作業は、PD ノードに負担をかけません。これにより、より安定したクラスター動作が保証されます。
    -   PD ノードが利用できない場合でも、ユーザーは診断のために TiDB ダッシュボードにアクセスできます。
    -   インターネット上の TiDB ダッシュボードへのアクセスには、PD の特権インターフェイスは必要ありません。したがって、クラスターのセキュリティ リスクが軽減されます。

    詳細については、 [ドキュメンテーション](https://docs.pingcap.com/tidb-in-kubernetes/dev/get-started#deploy-tidb-dashboard-independently)を参照してください。

-   パフォーマンス概要ダッシュボードにTiFlashおよび CDC (変更データ キャプチャ) パネルが追加されました[DBID](https://github.com/dbsid)

    v6.1.0 以降、TiDB は Grafana にパフォーマンス概要ダッシュボードを導入しました。これは、TiDB、TiKV、および PD の全体的なパフォーマンス診断のためのシステム レベルのエントリを提供します。 v6.5.0 では、パフォーマンス概要ダッシュボードにTiFlashと CDC パネルが追加されます。 v6.5.0 以降、これらのパネルでは、パフォーマンス概要ダッシュボードを使用して、TiDB クラスター内のすべてのコンポーネントのパフォーマンスを分析できます。

    TiFlashおよび CDC パネルは、 TiFlashおよび TiCDC の監視情報を再編成するため、 TiFlashおよび TiCDC のパフォーマンス問題の分析およびトラブルシューティングの効率を大幅に向上させることができます。

    -   [TiFlashパネル](/grafana-performance-overview-dashboard.md#tiflash)では、 TiFlashクラスターのリクエスト タイプ、レイテンシー分析、およびリソース使用量の概要を簡単に表示できます。
    -   [CDCパネル](/grafana-performance-overview-dashboard.md#cdc)では、TiCDC クラスターの健全性、レプリケーションレイテンシー、データ フロー、ダウンストリーム書き込みレイテンシーを簡単に表示できます。

    詳細については、 [ドキュメンテーション](/performance-tuning-methods.md)を参照してください。

### パフォーマンス {#performance}

-   [ハイランフー](https://github.com/hailanwhu)で接続された式をサポートします

    v6.5.0 より前では、TiDB は`OR`で接続されたフィルター条件に対するインデックス マージの使用のみをサポートしていました。 v6.5.0 以降、TiDB は`WHERE`句の`AND`で接続されたフィルタ条件のインデックス マージの使用をサポートしました。このようにして、TiDB のインデックス マージは、クエリ フィルター条件のより一般的な組み合わせをカバーできるようになり、union ( `OR` ) 関係に限定されなくなりました。現在の v6.5.0 バージョンは、オプティマイザによって自動的に選択された`OR`条件でのインデックス マージのみをサポートします。 `AND`条件のインデックス マージを有効にするには、 [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)ヒントを使用する必要があります。

    インデックスのマージの詳細については、 [インデックスのマージについて説明する](/explain-index-merge.md)を参照してください。

-   次の JSON関数のTiFlash [イービン87](https://github.com/yibin87)へのプッシュダウンをサポート

    -   `->`
    -   `->>`
    -   `JSON_EXTRACT()`

    JSON 形式は、アプリケーション データ モデリングのための柔軟な方法を提供します。そのため、データ交換やデータstorageに JSON 形式を使用するアプリケーションが増えています。 JSON関数をTiFlashにプッシュダウンすることで、JSON タイプのデータ分析の効率が向上し、よりリアルタイムな分析シナリオに TiDB を使用できます。

-   次の文字列関数のTiFlash [xzhangxian1008](https://github.com/xzhangxian1008)へのプッシュダウンをサポート

    -   `regexp_like`
    -   `regexp_instr`
    -   `regexp_substr`

-   [懐かしい](https://github.com/Reminiscent)での実行計画の生成を妨げるグローバル オプティマイザー ヒントをサポートします。

    一部のビュー アクセス シナリオでは、最適なパフォーマンスを達成するために、オプティマイザー ヒントを使用してビュー内のクエリの実行計画に干渉する必要があります。 v6.5.0 以降、TiDB はビュー内のクエリ ブロックへのグローバル ヒントの追加をサポートし、クエリで定義されたヒントがビュー内で有効になります。この機能は、ネストされたビューを含む複雑な SQL ステートメントにヒントを挿入する方法を提供し、実行計画の制御を強化し、複雑なステートメントのパフォーマンスを安定させます。グローバル ヒントを使用するには、 [ヒント参照を指定する](/optimizer-hints.md#step-2-add-the-target-hints)を行う必要があります。

    詳細については、 [ドキュメンテーション](/optimizer-hints.md#hints-that-take-effect-globally)を参照してください。

-   [ウィノロス](https://github.com/winoros)までのソート操作のプッシュダウンをサポート

    [パーティションテーブル](/partitioned-table.md)機能は v6.1.0 以降 GA になっていますが、TiDB は継続的にパフォーマンスを向上させています。 v6.5.0 では、TiDB は、計算とフィルタリングのために`ORDER BY`や`LIMIT`の並べ替え操作を TiKV にプッシュダウンすることをサポートします。これにより、パーティション分割テーブルを使用する場合、ネットワーク I/O オーバーヘッドが削減され、SQL パフォーマンスが向上します。

-   オプティマイザーは、より正確なコスト モデル バージョン 2 (GA) [qw4990](https://github.com/qw4990)を導入します。

    TiDB v6.2.0 では、実験的機能として[`tidb_cost_model_version = 2`](/system-variables.md#tidb_cost_model_version-new-in-v620)変数を設定できます。

    コスト モデル バージョン 2 は、TiDB オプティマイザーの全体的な機能を大幅に向上させ、TiDB がより強力な HTAP データベースに向けて進化するのに役立つ機能として一般提供されます。

    詳細については、 [ドキュメンテーション](/cost-model.md#cost-model-version-2)を参照してください。

-   TiFlash は、テーブルの行数[エルサ0520](https://github.com/elsa0520)を取得する操作を最適化します。

    データ分析のシナリオでは、フィルター条件なしでテーブルの実際の行数を 1 から`COUNT(*)`まで取得するのが一般的な操作です。 v6.5.0 では、 TiFlash は`COUNT(*)`の書き換えを最適化し、行数をカウントするために最も短い列定義を持つ null 以外の列を自動的に選択します。これにより、 TiFlashの I/O 操作の数が効果的に削減され、TiFlash の実行効率が向上します。行数を取得しています。

### 安定性 {#stability}

-   グローバルメモリ制御機能は GA [wshwsh12](https://github.com/wshwsh12)になりました

    v6.4.0 以降、TiDB は実験的機能としてグローバルメモリ制御を導入しました。 v6.5.0 では GA となり、メインメモリの消費量を追跡できるようになります。グローバルメモリ消費量が[`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)で定義されたしきい値に達すると、TiDB は安定性を確保するために GC または SQL 操作のキャンセルによってメモリ使用量を制限しようとします。

    セッション内のトランザクションによって消費されるメモリ(最大値は構成項目[`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit)がデフォルト以外の値として構成されている場合でも、TiDB はトランザクションが`txn-total-size-limit`で設定されたメモリを使用できることを保証します。

    TiDB v6.5.0 以降を使用している場合は、 [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)を使用してグローバルメモリを管理し、メモリ使用効率を向上させることができます。

    詳細については、 [ドキュメンテーション](/configure-memory-usage.md)を参照してください。

### 使いやすさ {#ease-of-use}

-   `EXPLAIN ANALYZE`出力[ホンユニャン](https://github.com/hongyunyan)のTiFlash `TableFullScan`オペレーターの実行情報を調整します。

    `EXPLAIN ANALYZE`ステートメントは、実行計画とランタイム統計を出力するために使用されます。 v6.5.0 では、 TiFlash はDMFile 関連の実行情報を追加することにより、 `TableFullScan`オペレーターの実行情報を改良しました。 TiFlashデータ スキャン ステータス情報がより直観的に表示されるようになり、 TiFlash のパフォーマンスをより簡単に分析できるようになりました。

    詳細については、 [ドキュメンテーション](/sql-statements/sql-statement-explain-analyze.md)を参照してください。

-   JSON 形式[fzzf678](https://github.com/fzzf678)での実行プランの出力をサポートします。

    v6.5.0 では、TiDB は実行プランの出力形式を拡張します。 `EXPLAIN`ステートメントに`FORMAT = "tidb_json"`を指定すると、SQLの実行計画をJSON形式で出力できます。この機能により、SQL デバッグ ツールと診断ツールは実行計画をより便利かつ正確に読み取ることができるため、SQL の診断とチューニングの使いやすさが向上します。

    詳細については、 [ドキュメンテーション](/sql-statements/sql-statement-explain.md)を参照してください。

### MySQLの互換性 {#mysql-compatibility}

-   高性能でグローバルに単調な`AUTO_INCREMENT`列属性 (GA) [ティエンチャイアマオ](https://github.com/tiancaiamao)をサポート

    v6.4.0 以降、TiDB は実験的機能として`AUTO_INCREMENT` MySQL 互換モードを導入しました。このモードでは、すべての TiDB インスタンスで ID が単調増加することを保証する、集中型の自動インクリメント ID 割り当てサービスが導入されています。この機能により、クエリ結果を自動インクリメント ID で簡単に並べ替えることができます。 v6.5.0 では、この機能は GA になります。この機能を使用したテーブルの挿入 TPS は 20,000 を超えることが予想され、この機能は単一テーブルとクラスター全体の書き込みスループットを向上させるエラスティック スケーリングをサポートしています。 MySQL 互換モードを使用するには、テーブル作成時に`AUTO_ID_CACHE` ～ `1`を設定する必要があります。以下は例です。

    ```sql
    CREATE TABLE t(a int AUTO_INCREMENT key) AUTO_ID_CACHE 1;
    ```

    詳細については、 [ドキュメンテーション](/auto-increment.md#mysql-compatibility-mode)を参照してください。

### データ移行 {#data-migration}

-   gzip、snappy、zstd 圧縮形式での SQL および CSV ファイルのエクスポートとインポートをサポート[リチュンジュ](https://github.com/lichunzhu)

    Dumpling は、 gzip、snappy、zstd の圧縮形式での圧縮 SQL および CSV ファイルへのデータのエクスポートをサポートしています。 TiDB Lightning は、これらの形式の圧縮ファイルのインポートもサポートしています。

    以前は、CSV ファイルや SQL ファイルを保存するためにデータをエクスポートまたはインポートするために大規模なstorageスペースを提供する必要があり、storageコストが高くなっていました。この機能のリリースにより、データ ファイルを圧縮することでstorageコストを大幅に削減できます。

    詳細については、 [ドキュメンテーション](/dumpling-overview.md#improve-export-efficiency-through-concurrency)を参照してください。

-   binlog解析機能を最適化[gmhdbjd](https://github.com/GMHDBJD)

    TiDB は、移行タスクに含まれていないスキーマとテーブルのbinlogイベントをフィルターで除外できるため、解析の効率と安定性が向上します。このポリシーは、v6.5.0 ではデフォルトで有効になります。追加の構成は必要ありません。

    以前は、少数のテーブルのみを移行する場合でも、アップストリームのbinlogファイル全体を解析する必要がありました。移行する必要のないbinlogファイル内のテーブルのbinlogイベントも解析する必要があり、効率的ではありませんでした。一方、これらのbinlogイベントが解析をサポートしていない場合、タスクは失敗します。移行タスク内のテーブルのbinlogイベントのみを解析することにより、binlogの解析効率が大幅に向上し、タスクの安定性が向上します。

-   TiDB Lightningのディスク クォータは GA [ブチュイトデゴウ](https://github.com/buchuitoudegou)です

    TiDB Lightningのディスク クォータを構成できます。十分なディスク クォータがない場合、 TiDB Lightning はソース データの読み取りと一時ファイルの書き込みを停止します。代わりに、ソートされたキーと値を最初に TiKV に書き込み、 TiDB Lightning がローカル一時ファイルを削除した後、インポート プロセスを続行します。

    以前は、 TiDB Lightning が物理モードを使用してデータをインポートすると、生データのエンコード、並べ替え、分割のためにローカル ディスクに大量の一時ファイルが作成されていました。ローカル ディスクのスペースがなくなると、ファイルへの書き込みに失敗し、 TiDB Lightning がエラーで終了します。この機能を使用すると、 TiDB Lightningタスクでローカル ディスクの上書きを回避できます。

    詳細については、 [ドキュメンテーション](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#configure-disk-quota-new-in-v620)を参照してください。

-   DM での継続的なデータ検証は GA [D3ハンター](https://github.com/D3Hunter)です

    増分データを上流データベースから下流データベースに移行するプロセスでは、データ フローによってエラーやデータ損失が発生する可能性がわずかにあります。クレジットや証券ビジネスなど、強力なデータ一貫性が必要なシナリオでは、移行後にデータに対してフルボリュームのチェックサムを実行して、データの一貫性を確保できます。ただし、一部の増分レプリケーション シナリオでは、アップストリームとダウンストリームのデータが常に変化するため、アップストリームとダウンストリームの書き込みは継続的かつ中断されず、すべてのデータの整合性チェックを実行することが困難になります。

    以前は、完全なデータを検証するにはビジネスを中断する必要があり、ビジネスに影響を与える可能性がありました。この機能を使用すると、ビジネスを中断することなく増分データ検証を実行できるようになります。

    詳細については、 [ドキュメンテーション](/dm/dm-continuous-data-validation.md)を参照してください。

### TiDB データ共有サブスクリプション {#tidb-data-share-subscription}

-   TiCDC は、変更されたログのstorageシンクへのレプリケーションをサポートします (実験的) [ジャオシンユ](https://github.com/zhaoxinyu)

    TiCDC は、変更されたログの Amazon S3、Azure Blob Storage、NFS、およびその他の S3 互換storageサービスへのレプリケートをサポートしています。クラウドstorageは価格も手頃で使いやすいです。 Kafka を使用していない場合は、storageシンクを使用できます。 TiCDC は、変更されたログをファイルに保存し、それをstorageシステムに送信します。コンシューマ プログラムは、storageシステムから、新しく生成された変更されたログ ファイルを定期的に読み取ります。

    storageシンクは、canal-json および CSV 形式の変更されたログをサポートします。詳細については、 [ドキュメンテーション](/ticdc/ticdc-sink-to-cloud-storage.md)を参照してください。

-   TiCDC は、2 つのクラスター[東門](https://github.com/asddongmen)間の双方向レプリケーションをサポートします。

    TiCDC は、2 つの TiDB クラスター間の双方向レプリケーションをサポートします。アプリケーション用に地理的に分散された複数のアクティブなデータ センターを構築する必要がある場合は、この機能をソリューションとして使用できます。 1 つの TiDB クラスターから別の TiDB クラスターへの TiCDC 変更フィードの`bdr-mode = true`パラメーターを構成することにより、2 つの TiDB クラスター間で双方向のデータ レプリケーションを実現できます。

    詳細については、 [ドキュメンテーション](/ticdc/ticdc-bidirectional-replication.md)を参照してください。

-   TiCDC は TLS オンライン[CharlesCheung96](https://github.com/CharlesCheung96)の更新をサポートします

    データベース システムのセキュリティを維持するには、システムで使用される証明書の有効期限ポリシーを設定する必要があります。有効期限が過ぎると、システムには新しい証明書が必要になります。 TiCDC v6.5.0 は、TLS 証明書のオンライン更新をサポートしています。 TiCDC は、レプリケーション タスクを中断することなく、手動介入を必要とせずに証明書を自動的に検出して更新できます。

-   TiCDC のパフォーマンスが大幅に向上[@3AceShowHand](https://github.com/3AceShowHand)

    TiDB クラスターのテスト シナリオでは、TiCDC のパフォーマンスが大幅に向上しました。具体的には、Kafka にデータをレプリケートするシナリオでは、単一の TiCDC が処理できる最大行変更は 30K 行/秒に達し、レプリケーションのレイテンシーは10 秒に短縮されます。 TiKV および TiCDC のローリング アップグレード中であっても、レプリケーションのレイテンシーは 30 秒未満です。

    災害復旧 (DR) シナリオでは、TiCDC REDO ログと同期ポイントが有効になっている場合、TiCDC スループット[Kafka へのデータの複製](/replicate-data-to-kafka.md)を 4000 行/秒から 35000 行/秒に改善でき、レプリケーションのレイテンシーを2 秒に制限できます。

### バックアップと復元 {#backup-and-restore}

-   TiDB バックアップ &amp; リストアはスナップショット チェックポイント バックアップ[レヴルス](https://github.com/Leavrth)をサポートします

    TiDB スナップショット バックアップは、チェックポイントからのバックアップの再開をサポートしています。バックアップと復元 (BR) で回復可能なエラーが発生すると、バックアップが再試行されます。ただし、再試行が数回失敗すると、 BR は終了します。チェックポイント バックアップ機能を使用すると、数十分にわたるネットワーク障害など、より長時間の回復可能な障害の再試行が可能になります。

    BR終了後 1 時間以内にシステムを障害から回復しないと、バックアップされるスナップショット データが GC メカニズムによって再利用され、バックアップが失敗する可能性があることに注意してください。詳細については、 [ドキュメンテーション](/br/br-checkpoint-backup.md#backup-retry-must-be-prior-to-gc)を参照してください。

-   PITR性能が大幅に向上[@ジョッカウ](https://github.com/joccau)

    ログ復元段階では、1 つの TiKV の復元速度が 9 MiB/s に達し、これは以前より 50% 速くなります。復元速度はスケーラブルであり、DR シナリオの RTO が大幅に短縮されます。 DR シナリオの RPO は最短 5 分です。通常のクラスターの運用および保守 (OM) では、たとえば、ローリング アップグレードが実行されるか、1 つの TiKV のみが停止している場合、RPO は 5 分になることがあります。

-   TiKV- BR GA: RawKV [ハオジンミン](https://github.com/haojinming)のバックアップと復元をサポート

    TiKV- BR は、TiKV クラスターで使用されるバックアップおよび復元ツールです。 TiKV と PD は、TiDB なしで使用される場合、RawKV と呼ばれる KV データベースを構成できます。 TiKV- BR は、 RawKV を使用する製品のデータのバックアップと復元をサポートしています。 TiKV- BR は、 TiKV クラスターの[`api-version`](/tikv-configuration-file.md#api-version-new-in-v610) `API V1`から`API V2`にアップグレードすることもできます。

    詳細については、 [ドキュメンテーション](https://tikv.org/docs/latest/concepts/explore-tikv-features/backup-restore/)を参照してください。

## 互換性の変更 {#compatibility-changes}

### システム変数 {#system-variables}

| 変数名                                                                                                                                                                                                                | 種類の変更    | 説明                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `tidb_enable_amend_pessimistic_txn`                                                                                                                                                                                | 廃止されました  | v6.5.0 以降、この変数は非推奨となり、TiDB は`Information schema is changed`エラーを回避するためにデフォルトで[メタデータロック](/metadata-lock.md)機能を使用します。                                                                                                                                                                                                                                                                                               |
| [結合したテーブルの再配置](/join-reorder.md)アルゴリズムのアウター結合のサポートがデフォルトで有効になることを意味します。                                                                                                                                                                                                                                                                                                  |
| [`tidb_cost_model_version`](/system-variables.md#tidb_cost_model_version-new-in-v620)                                                       | 修正済み     | さらにテストを行った後、デフォルト値を`1`から`2`に変更します。これは、デフォルトでインデックス選択と演算子の選択にコスト モデル バージョン 2 が使用されることを意味します。                                                                                                                                                                                                                                                                                                                                                      |
| [`tidb_enable_gc_aware_memory_track`](/system-variables.md#tidb_enable_gc_aware_memory_track)                                                 | 修正済み     | デフォルト値を`ON`から`OFF`に変更します。 GC 対応メモリトラックがテストで不正確であることが判明し、追跡される分析メモリサイズが大きすぎるため、メモリトラックは無効になっています。さらに、 Golang 1.19 では、GC 対応メモリトラックによって追跡されるメモリはメモリ全体に大きな影響を与えません。                                                                                                                                                                                                                                                                                  |
| [`tidb_enable_metadata_lock`](/system-variables.md#tidb_enable_metadata_lock-new-in-v630)                                                 | 修正済み     | さらにテストを行った後、デフォルト値を`OFF`から`ON`に変更します。これは、メタデータ ロック機能がデフォルトで有効になることを意味します。                                                                                                                                                                                                                                                                                                                                                                        |
| [`tidb_enable_tiflash_read_for_write_stmt`](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-new-in-v630)       | 修正済み     | v6.5.0 から有効になります。 `INSERT` 、および`UPDATE` `DELETE`含む SQL ステートメントの読み取り操作をTiFlashにプッシュダウンできるかどうかを制御します。デフォルト値は`OFF`です。                                                                                                                                                                                                                                                                                                                               |
| [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)                                              | 修正済み     | さらにテストを行った後、デフォルト値を`OFF`から`ON`に変更します。これは、 `ADD INDEX`と`CREATE INDEX`のアクセラレーションがデフォルトで有効になることを意味します。                                                                                                                                                                                                                                                                                                                                              |
| [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)                                                                                        | 修正済み     | TiDB v6.5.0 より前のバージョンの場合、この変数はクエリのメモリクォータのしきい値を設定するために使用されます。 TiDB v6.5.0 以降のバージョンでは、DML ステートメントのメモリをより正確に制御するために、この変数を使用してセッションのメモリクォータのしきい値を設定します。                                                                                                                                                                                                                                                                                             |
| [`tidb_adaptive_closest_read_threshold`](/system-variables.md#tidb_adaptive_closest_read_threshold-new-in-v630)以上の場合、 `closest-adaptive`構成が有効になる TiDB ノードの数は制限されます。各アベイラビリティ ゾーンは、TiDB ノードが最も少ないアベイラビリティ ゾーン内の TiDB ノードの数と常に同じであり、他の TiDB ノードはリーダー レプリカから自動的に読み取られます。    |
| [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)                                                    | 修正済み     | デフォルト値を`0`から`80%`に変更します。 TiDB グローバルメモリコントロールが GA になると、このデフォルト値の変更により、デフォルトでメモリコントロールが有効になり、TiDB インスタンスのメモリ制限がデフォルトで総メモリの 80% に設定されます。                                                                                                                                                                                                                                                                                                            |
| [`default_password_lifetime`](/system-variables.md#default_password_lifetime-new-in-v650)                                                 | 新しく追加された | パスワードの自動有効期限のグローバル ポリシーを設定して、ユーザーに定期的なパスワードの変更を要求します。デフォルト値`0`は、パスワードに期限がないことを示します。                                                                                                                                                                                                                                                                                                                                                              |
| [`disconnect_on_expired_password`](/system-variables.md#disconnect_on_expired_password-new-in-v650)                                  | 新しく追加された | パスワードの有効期限が切れたときに TiDB がクライアント接続を切断するかどうかを示します。この変数は読み取り専用です。                                                                                                                                                                                                                                                                                                                                                                                    |
| [`password_history`](/system-variables.md#password_history-new-in-v650)                                                                            | 新しく追加された | この変数は、パスワードの変更回数に基づいて TiDB がパスワードの再利用を制限できるようにするパスワード再利用ポリシーを確立するために使用されます。デフォルト値`0`は、パスワード変更の回数に基づいてパスワード再利用ポリシーを無効にすることを意味します。                                                                                                                                                                                                                                                                                                                 |
| [`password_reuse_interval`](/system-variables.md#password_reuse_interval-new-in-v650)                                                       | 新しく追加された | この変数は、TiDB が経過時間に基づいてパスワードの再利用を制限できるようにするパスワード再利用ポリシーを確立するために使用されます。デフォルト値`0`は、経過時間に基づいてパスワード再利用ポリシーを無効にすることを意味します。                                                                                                                                                                                                                                                                                                                              |
| [`tidb_auto_build_stats_concurrency`](/system-variables.md#tidb_auto_build_stats_concurrency-new-in-v650)                         | 新しく追加された | この変数は、統計の自動更新を実行する同時実行数を設定するために使用されます。デフォルト値は`1`です。                                                                                                                                                                                                                                                                                                                                                                                              |
| [`tidb_cdc_write_source`](/system-variables.md#tidb_cdc_write_source-new-in-v650)                                                             | 新しく追加された | この変数が 0 以外の値に設定されている場合、このセッションで書き込まれたデータは TiCDC によって書き込まれたものとみなされます。この変数は TiCDC によってのみ変更できます。いかなる場合でも、この変数を手動で変更しないでください。                                                                                                                                                                                                                                                                                                                        |
| [`tidb_index_merge_intersection_concurrency`](/system-variables.md#tidb_index_merge_intersection_concurrency-new-in-v650) | 新しく追加された | インデックスのマージが実行する交差操作の最大同時実行数を設定します。これは、TiDB が動的プルーニング モードでパーティション化されたテーブルにアクセスする場合にのみ有効です。                                                                                                                                                                                                                                                                                                                                                        |
| [双方向レプリケーション](/ticdc/ticdc-bidirectional-replication.md)クラスター内でさまざまなクラスター ID を構成するために使用されます。                                                                                                                                                                                                                                                                                      |
| [`tidb_sysproc_scan_concurrency`](/system-variables.md#tidb_sysproc_scan_concurrency-new-in-v650)                                     | 新しく追加された | この変数は、TiDB が内部 SQL ステートメント (統計の自動更新など) を実行するときに実行されるスキャン操作の同時実行性を設定するために使用されます。デフォルト値は`1`です。                                                                                                                                                                                                                                                                                                                                                     |
| [`tidb_ttl_delete_batch_size`](/system-variables.md#tidb_ttl_delete_batch_size-new-in-v650)                                              | 新しく追加された | この変数は、TTL ジョブの`DELETE`つのトランザクションで削除できる最大行数を設定するために使用されます。                                                                                                                                                                                                                                                                                                                                                                                        |
| [`tidb_ttl_delete_rate_limit`](/system-variables.md#tidb_ttl_delete_rate_limit-new-in-v650)                                              | 新しく追加された | この変数は、TTL ジョブの単一ノードで 1 秒あたりに許可される`DELETE`ステートメントの最大数を制限するために使用されます。この変数が`0`に設定されている場合、制限は適用されません。                                                                                                                                                                                                                                                                                                                                                |
| [`tidb_ttl_delete_worker_count`](/system-variables.md#tidb_ttl_delete_worker_count-new-in-v650)                                        | 新しく追加された | この変数は、各 TiDB ノードでの TTL ジョブの最大同時実行数を設定するために使用されます。                                                                                                                                                                                                                                                                                                                                                                                                |
| [`tidb_ttl_job_enable`](/system-variables.md#tidb_ttl_job_enable-new-in-v650)                                                                   | 新しく追加された | この変数は、TTL ジョブを有効にするかどうかを制御するために使用されます。これを`OFF`に設定すると、TTL 属性を持つすべてのテーブルが期限切れデータのクリーンアップを自動的に停止します。                                                                                                                                                                                                                                                                                                                                                |
| `tidb_ttl_job_run_interval`                                                                                                                                                                                        | 新しく追加された | この変数は、バックグラウンドでの TTL ジョブのスケジュール間隔を制御するために使用されます。たとえば、現在の値が`1h0m0s`に設定されている場合、TTL 属性を持つ各テーブルは、1 時間ごとに期限切れのデータをクリーンアップします。                                                                                                                                                                                                                                                                                                                         |
| [`tidb_ttl_job_schedule_window_start_time`](/system-variables.md#tidb_ttl_job_schedule_window_start_time-new-in-v650)       | 新しく追加された | この変数は、バックグラウンドでの TTL ジョブのスケジュール ウィンドウの開始時間を制御するために使用されます。この変数の値を変更する場合は、ウィンドウが小さいと期限切れデータのクリーンアップが失敗する可能性があることに注意してください。                                                                                                                                                                                                                                                                                                                         |
| [`tidb_ttl_job_schedule_window_end_time`](/system-variables.md#tidb_ttl_job_schedule_window_end_time-new-in-v650)             | 新しく追加された | この変数は、バックグラウンドでの TTL ジョブのスケジュール ウィンドウの終了時刻を制御するために使用されます。この変数の値を変更する場合は、ウィンドウが小さいと期限切れデータのクリーンアップが失敗する可能性があることに注意してください。                                                                                                                                                                                                                                                                                                                         |
| [`tidb_ttl_scan_batch_size`](/system-variables.md#tidb_ttl_scan_batch_size-new-in-v650)                                                    | 新しく追加された | この変数は、TTL ジョブの期限切れデータのスキャンに使用される各`SELECT`ステートメントの`LIMIT`値を設定するために使用されます。                                                                                                                                                                                                                                                                                                                                                                         |
| [`tidb_ttl_scan_worker_count`](/system-variables.md#tidb_ttl_scan_worker_count-new-in-v650)                                              | 新しく追加された | この変数は、各 TiDB ノードでの TTL スキャン ジョブの最大同時実行数を設定するために使用されます。                                                                                                                                                                                                                                                                                                                                                                                           |
| [`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650)が有効な場合にのみ有効になります。デフォルト値は`ON`です。                                                                                                                                                                                           |
| [`validate_password.policy`](/system-variables.md#validate_passwordpolicy-new-in-v650)が`2` (STRONG) に設定されている場合にのみ有効です。デフォルト値は`""`です。        |
| [`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650)                                                      | 新しく追加された | この変数は、パスワードの複雑さのチェックを実行するかどうかを制御します。この変数が`ON`に設定されている場合、TiDB はパスワードの設定時にパスワードの複雑さのチェックを実行します。デフォルト値は`OFF`です。                                                                                                                                                                                                                                                                                                                                     |
| [`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650)が有効な場合にのみ有効になります。                                                                                                                                                                                   |
| [`validate_password.policy`](/system-variables.md#validate_passwordpolicy-new-in-v650)が`1` (MEDIUM) 以上に設定されている場合にのみ有効です。デフォルト値は`1`です。 |
| [`validate_password.policy`](/system-variables.md#validate_passwordpolicy-new-in-v650)が`1` (MEDIUM) 以上に設定されている場合にのみ有効です。デフォルト値は`1`です。      |
| [`validate_password.enable`](/system-variables.md#password_reuse_interval-new-in-v650)が有効な場合にのみ有効になります。デフォルト値は`1`です。                                                                                                                                                             |
| [`validate_password.policy`](/system-variables.md#validate_passwordpolicy-new-in-v650)が`1` (MEDIUM) 以上に設定されている場合にのみ有効です。デフォルト値は`1`です。    |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                                                                                                                 | 種類の変更    | 説明                                                                                                                                                                                                                         |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)を使用してメモリをグローバルに管理します。 |
| TiDB           | [`disconnect-on-expired-password`](/tidb-configuration-file.md#disconnect-on-expired-password-new-in-v650) | 新しく追加された | パスワードの有効期限が切れたときに、TiDB がクライアント接続を切断するかどうかを決定します。デフォルト値は`true`で、パスワードの有効期限が切れるとクライアント接続が切断されることを意味します。                                                                                                                      |
| TiKV           | `raw-min-ts-outlier-threshold`                                                                                                                                                                  | 削除されました  | この構成項目は v6.4.0 で非推奨となり、v6.5.0 で削除されました。                                                                                                                                                                                    |
| TiKV           | [`cdc.min-ts-interval`](/tikv-configuration-file.md#min-ts-interval)                                                                  | 修正済み     | CDCレイテンシーを短縮するために、デフォルト値が`1s`から`200ms`に変更されました。                                                                                                                                                                            |
| TiKV           | [`memory-use-ratio`](/tikv-configuration-file.md#memory-use-ratio-new-in-v650)                                           | 新しく追加された | PITR ログ リカバリでの合計システムメモリに対する利用可能なメモリの比率を示します。                                                                                                                                                                               |
| TiCDC          | [`sink.terminator`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)                  | 新しく追加された | 2 つのデータ変更イベントを区切るために使用される行ターミネータを示します。デフォルトでは値は空であり、 `\r\n`が使用されることを意味します。                                                                                                                                                 |
| TiCDC          | [`sink.date-separator`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)              | 新しく追加された | ファイルディレクトリの日付区切り文字のタイプを示します。値のオプションは`none` 、 `year` 、 `month` 、および`day`です。 `none`はデフォルト値で、日付が区切られていないことを意味します。                                                                                                             |
| TiCDC          | [`sink.enable-partition-separator`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)  | 新しく追加された | パーティションを区切り文字列として使用するかどうかを指定します。デフォルト値は`false`で、テーブル内のパーティションが別のディレクトリに格納されないことを意味します。                                                                                                                                     |
| TiCDC          | [`sink.csv.delimiter`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)               | 新しく追加された | フィールド間の区切り文字を示します。値は ASCII 文字である必要があり、デフォルトは`,`です。                                                                                                                                                                         |
| TiCDC          | [`sink.csv.quote`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)                   | 新しく追加された | フィールドを囲む引用符。デフォルト値は`"`です。値が空の場合、引用符は使用されません。                                                                                                                                                                               |
| TiCDC          | [`sink.csv.null`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)                    | 新しく追加された | CSV列がnullの場合に表示される文字を指定します。デフォルト値は`\N`です。                                                                                                                                                                                  |
| TiCDC          | [`sink.csv.include-commit-ts`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)       | 新しく追加された | CSV 行に commit-ts を含めるかどうかを指定します。デフォルト値は`false`です。                                                                                                                                                                          |

### その他 {#others}

-   v6.5.0 以降、 `mysql.user`テーブルには`Password_reuse_history`と`Password_reuse_time`という 2 つの新しい列が追加されます。
-   v6.5.0 以降、 [ドキュメンテーション](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)を参照してください。

## 廃止された機能 {#deprecated-feature}

v6.5.0 以降、v4.0.7 で導入された`AMEND TRANSACTION`メカニズムは非推奨となり、 [メタデータロック](/metadata-lock.md)に置き換えられます。

## 改善点 {#improvements}

-   TiDB

    -   `BIT`と`CHAR`列については、 `INFORMATION_SCHEMA.COLUMNS`の結果を MySQL [ホーキングレイ](https://github.com/hawkingrei)と一致させます。
    -   TiFlash MPP モードのTiFlashノードの TiDB プローブ メカニズムを最適化し、ノードが異常な場合のパフォーマンスへの影響を軽減します[ハッカー派](https://github.com/hackersean)

-   TiKV

    -   ディスクスペースの枯渇を避けるために、スペースが不十分な場合はRaft Engineへの書き込みを停止します[嘉陽鄭](https://github.com/jiayang-zheng)
    -   `json_valid`関数の TiKV [立振環](https://github.com/lizhenhuan)へのプッシュダウンをサポート
    -   1 回のバックアップ リクエストで複数範囲のデータのバックアップをサポート[レヴルス](https://github.com/Leavrth)
    -   rusoto ライブラリ[3ポインター](https://github.com/3pointer)を更新することで、AWS のアジアパシフィック リージョン (ap-southeast-3) へのデータのバックアップをサポートします。
    -   悲観的トランザクション競合を削減[ミョンケミンタ](https://github.com/MyonKeminta)
    -   外部storageオブジェクト[ユジュンセン](https://github.com/YuJuncen)をキャッシュすることで、リカバリ パフォーマンスを向上させます。
    -   専用スレッドで CheckLeader を実行して、TiCDC レプリケーションのレイテンシー[オーバーヴィーナス](https://github.com/overvenus)を削減します。
    -   チェックポイント[ユジュンセン](https://github.com/YuJuncen)のプル モデルをサポート
    -   送信側でのスピンの問題を回避するには、クロスビームチャネル[スティックナーフ](https://github.com/sticnarf)を更新します。
    -   TiKV [cfzjywxk](https://github.com/cfzjywxk)でのコプロセッサータスク処理をサポート
    -   TiKV にリージョン[リククスサシネーター](https://github.com/LykxSassinator)をウェイクアップするように通知することで、障害回復時の待ち時間を短縮します。
    -   コード最適化[ビジージェイ](https://github.com/BusyJay)により、要求されたメモリ使用量のサイズを削減します。
    -   Raft拡張機能を導入してコードの拡張性を向上させます[ビジージェイ](https://github.com/BusyJay)
    -   tikv-ctl を使用した特定のキー範囲に含まれるリージョンのクエリをサポート[@husharp](https://github.com/HuSharp)
    -   更新されていないが継続的にロックされている行の読み取りおよび書き込みパフォーマンスを向上させます[@sicnarf](https://github.com/sticnarf)

-   PD

    -   ロックの粒度を最適化してロックの競合を軽減し、高い同時実行性[ルルンクス](https://github.com/rleungx)でのハートビートの処理能力を向上させます。
    -   大規模クラスターのスケジューラーのパフォーマンスを最適化し、スケジューリング ポリシー[バッファフライ](https://github.com/bufferflies)の本番を加速します。
    -   リージョン[ルルンクス](https://github.com/rleungx)のロード速度を向上させます。
    -   リージョンハートビート[ルルンクス](https://github.com/rleungx)の処理を最適化することで、不必要なオーバーヘッドを削減します。
    -   墓石ストア[ノールーシュ](https://github.com/nolouch)を自動的にガベージコレクションする機能を追加

-   TiFlash

    -   SQL 側でバッチ処理がないシナリオでの書き込みパフォーマンスが向上します[リデズ](https://github.com/lidezhu)
    -   `explain analyze`出力[ホンユニャン](https://github.com/hongyunyan)に TableFullScan の詳細を追加します。

-   ツール

    -   TiDB ダッシュボード

        -   スロー クエリ ページに 3 つの新しいフィールドを追加します:「Is Prepared?」、「Is Plan from Cache?」、「Is Plan from Binding?」 [シュギット](https://github.com/shhdgit)

    -   バックアップと復元 (BR)

        -   バックアップ ログ データ[レヴルス](https://github.com/Leavrth)のクリーニング プロセス中のBRメモリ使用量を最適化します。
        -   復元プロセス[モクイシュル28](https://github.com/MoCuishle28)中に PD リーダー スイッチによって引き起こされる復元失敗の問題を修正します。
        -   ログ バックアップ[ユジュンセン](https://github.com/YuJuncen)で OpenSSL プロトコルを使用することで、TLS 互換性を向上させます。

    -   TiCDC

        -   Kafka プロトコル エンコーダのパフォーマンスを向上させる[スドジ](https://github.com/sdojjy)

    -   TiDB データ移行 (DM)

        -   ブロック リスト[GMHDBJD](https://github.com/GMHDBJD)内のテーブルのデータを解析しないことにより、DM のデータ レプリケーション パフォーマンスが向上します。
        -   非同期書き込みと一括書き込み[GMHDBJD](https://github.com/GMHDBJD)を使用して、DM リレーの書き込み効率を向上させます
        -   DM 事前チェック[ブチュイトデゴウ](https://github.com/buchuitoudegou)のエラー メッセージを最適化します。
        -   古い MySQL バージョン[lyzx2001](https://github.com/lyzx2001)に対する`SHOW SLAVE HOSTS`の互換性を向上

## バグの修正 {#bug-fixes}

-   TiDB

    -   場合によって発生するチャンク再利用機能のメモリチャンクの誤用の問題を修正[キープラーニング20221](https://github.com/keeplearning20221)
    -   `tidb_constraint_check_in_place_pessimistic`の内部セッションがグローバル設定[エキシウム](https://github.com/ekexium)の影響を受ける可能性がある問題を修正
    -   `AUTO_INCREMENT`列が`CHECK`制約[ヤンケオ](https://github.com/YangKeao)で機能しない問題を修正
    -   `INSERT IGNORE INTO`を使用して`STRING`タイプのデータを`SMALLINT`タイプの自動インクリメント列に挿入すると、エラー[ホーキングレイ](https://github.com/hawkingrei)が発生する問題を修正します。
    -   パーティションテーブル[むじょん](https://github.com/mjonss)のパーティション列の名前変更操作でNULLポインタエラーが発生する問題を修正
    -   パーティションテーブルのパーティション列を変更すると DDL がハングする[むじょん](https://github.com/mjonss)という問題を修正します。
    -   v4.0.16 から v6.4.0 [タンジェンタ](https://github.com/tangenta)にアップグレードした後に`ADMIN SHOW JOB`操作がパニックになる問題を修正
    -   `tidb_decode_key`関数がパーティション テーブル[定義2014](https://github.com/Defined2014)のエンコーディングを正しく解析できない問題を修正します。
    -   ログ ローテーション中に gRPC エラー ログが正しいログ ファイルにリダイレクトされない問題を修正します[ゼボックス](https://github.com/xhebox)
    -   TiKV が読み取りエンジン[イーサール](https://github.com/Yisaer)として構成されていない場合、TiDB が`BEGIN; SELECT... FOR UPDATE;`ポイント クエリに対して予期しない実行プランを生成する問題を修正します。
    -   誤って`StreamAgg` TiFlashに押し込むと、間違った結果[修正データベース](https://github.com/fixdb)が発生する問題を修正

-   TiKV

    -   Raft Engine ctl [タボキー](https://github.com/tabokie)のエラーを修正
    -   tikv-ctl [国祥CN](https://github.com/guoxiangCN)で`compact raft`コマンドを実行するときの`Get raft db is not allowed`エラーを修正
    -   TLS が有効になっている場合にログ バックアップが機能しない問題を修正[ユジュンセン](https://github.com/YuJuncen)
    -   ジオメトリ フィールド タイプ[ドヴィーデン](https://github.com/dveeden)のサポートの問題を修正
    -   新しい照合順序が有効になっていない場合、 `LIKE`演算子の`_`非 ASCII 文字と一致できない問題を修正[ヤンケオ](https://github.com/YangKeao)
    -   `reset-to-version`コマンド[タボキー](https://github.com/tabokie)を実行すると tikv-ctl が予期せず終了する問題を修正

-   PD

    -   [フンドゥンDM](https://github.com/HunDunDM)を変更しないと`balance-hot-region-scheduler`設定が保持されない問題を修正
    -   アップグレード プロセス中に`rank-formula-version`がアップグレード前の構成を保持しない問題を修正します[フンドゥンDM](https://github.com/HunDunDM)

-   TiFlash

    -   TiFlash [リデズ](https://github.com/lidezhu)の再起動後にデルタレイヤーのカラムファイルが圧縮できない問題を修正
    -   TiFlashファイルオープン OPS が高すぎる問題を修正[ジェイ・ソン・ファン](https://github.com/JaySon-Huang)

-   ツール

    -   バックアップと復元 (BR)

        -   BRがログバックアップデータを削除すると、削除すべきでないデータを誤って削除してしまう問題を修正[レヴルス](https://github.com/Leavrth)
        -   データベースまたはテーブル[モクイシュル28](https://github.com/MoCuishle28)の照合順序に古いフレームワークを使用すると、復元タスクが失敗する問題を修正します。
        -   Alibaba Cloud および Huawei Cloud が Amazon S3storage[3ポインター](https://github.com/3pointer)と完全な互換性がないためにバックアップが失敗する問題を修正

    -   TiCDC

        -   PD リーダーが[沢民州](https://github.com/zeminzhou)でクラッシュすると TiCDC がスタックする問題を修正
        -   最初に DDL ステートメントを実行し、次に変更フィード[東門](https://github.com/asddongmen)を一時停止して再開するシナリオで発生したデータ損失を修正しました。
        -   TiFlash [オーバーヴィーナス](https://github.com/overvenus)の新しいバージョンがある場合に TiCDC が誤ってエラーを報告する問題を修正
        -   ダウンストリーム ネットワークが利用できない場合にシンクコンポーネントがスタックする問題を修正[ひっくり返る](https://github.com/hicqu)
        -   ユーザーがレプリケーション タスクをすぐに削除し、同じタスク名[オーバーヴィーナス](https://github.com/overvenus)で別のタスクを作成するとデータが失われる問題を修正します。

    -   TiDB データ移行 (DM)

        -   アップストリーム データベースで GTID モードが有効になっているがデータがない場合、 `task-mode:all`タスクを開始できない問題を修正します[リウメンギャ94](https://github.com/liumengya94)
        -   既存のワーカーが終了する前に新しい DM ワーカーがスケジュールされている場合、データが複数回レプリケートされる問題を修正します[GMHDBJD](https://github.com/GMHDBJD)
        -   アップストリーム データベースが正規表現を使用して権限[ランス6716](https://github.com/lance6716)を付与する場合、DM 事前チェックが通過しない問題を修正します。

    -   TiDB Lightning

        -   TiDB Lightning が巨大なソース データ ファイル[dsダシュン](https://github.com/dsdashun)をインポートするときのメモリリークの問題を修正
        -   データを並行してインポートするときにTiDB Lightning が競合を正しく検出できない問題を修正[dsダシュン](https://github.com/dsdashun)

## 貢献者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   [e1ijah1](https://github.com/e1ijah1)
-   [国祥CN](https://github.com/guoxiangCN) (初投稿者)
-   [嘉陽鄭](https://github.com/jiayang-zheng)
-   [ジフフスト](https://github.com/jiyfhust)
-   [マイクチェンウェイ](https://github.com/mikechengwei)
-   [ピンアンドブ](https://github.com/pingandb)
-   [サシャシュラ](https://github.com/sashashura)
-   [ソーセリュー](https://github.com/sourcelliu)
-   [wxbty](https://github.com/wxbty)
