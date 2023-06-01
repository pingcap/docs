---
title: TiDB 6.5.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 6.5.0.
---

# TiDB 6.5.0 リリースノート {#tidb-6-5-0-release-notes}

発売日：2022年12月29日

TiDB バージョン: 6.5.0

クイックアクセス: [<a href="https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb">クイックスタート</a>](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [<a href="https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup">本番展開</a>](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup) | [<a href="https://www.pingcap.com/download/?version=v6.5.0#version-list">インストールパッケージ</a>](https://www.pingcap.com/download/?version=v6.5.0#version-list)

TiDB 6.5.0 は長期サポート リリース (LTS) です。

以前の LTS 6.1.0 と比較して、6.5.0 には[<a href="/releases/release-6.2.0.md">6.2.0-DMR</a>](/releases/release-6.2.0.md) 、 [<a href="/releases/release-6.3.0.md">6.3.0-DMR</a>](/releases/release-6.3.0.md) 、 [<a href="/releases/release-6.4.0.md">6.4.0-DMR</a>](/releases/release-6.4.0.md)でリリースされた新機能、改善、バグ修正が含まれているだけでなく、次の主要な機能と改善も導入されています。

-   [<a href="/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630">インデックス加速度</a>](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)機能が一般公開 (GA) され、インデックス追加のパフォーマンスが v6.1.0 と比較して約 10 倍向上しました。
-   TiDB グローバルメモリコントロールが GA になり、 [<a href="/system-variables.md#tidb_server_memory_limit-new-in-v640">`tidb_server_memory_limit`</a>](/system-variables.md#tidb_server_memory_limit-new-in-v640)を介してメモリ消費のしきい値を制御できるようになります。
-   高性能でグローバルに単調な[<a href="/auto-increment.md#mysql-compatibility-mode">`AUTO_INCREMENT`</a>](/auto-increment.md#mysql-compatibility-mode)カラム属性が GA となり、MySQL と互換性があります。
-   [<a href="/sql-statements/sql-statement-flashback-to-timestamp.md">`FLASHBACK CLUSTER TO TIMESTAMP`</a>](/sql-statements/sql-statement-flashback-to-timestamp.md)は TiCDC および PITR と互換性があり、GA になりました。
-   より正確な[<a href="/cost-model.md#cost-model-version-2">コストモデル バージョン 2</a>](/cost-model.md#cost-model-version-2)一般提供し、 `AND` for [<a href="/explain-index-merge.md">インデックスのマージ</a>](/explain-index-merge.md)で接続された式をサポートすることにより、TiDB オプティマイザーを強化します。
-   `JSON_EXTRACT()`機能のTiFlashへのプッシュダウンをサポートします。
-   パスワード コンプライアンスの監査要件を満たす[<a href="/password-management.md">パスワード管理</a>](/password-management.md)ポリシーをサポートします。
-   TiDB LightningおよびDumpling は、 [<a href="/tidb-lightning/tidb-lightning-data-source.md">輸入する</a>](/tidb-lightning/tidb-lightning-data-source.md)および[<a href="/dumpling-overview.md#improve-export-efficiency-through-concurrency">輸出する</a>](/dumpling-overview.md#improve-export-efficiency-through-concurrency)の圧縮 SQL および CSV ファイルをサポートしています。
-   TiDB データ移行 (DM) [<a href="/dm/dm-continuous-data-validation.md">継続的なデータ検証</a>](/dm/dm-continuous-data-validation.md) GA になります。
-   TiDB バックアップ &amp; リストアは、スナップショット チェックポイント バックアップをサポートし、 [<a href="/br/br-pitr-guide.md#run-pitr">PITR</a>](/br/br-pitr-guide.md#run-pitr)リカバリ パフォーマンスを 50% 向上させ、一般的なシナリオでの RPO を最短 5 分に短縮します。
-   TiCDC スループット[<a href="/replicate-data-to-kafka.md">Kafka へのデータの複製</a>](/replicate-data-to-kafka.md)が 4000 行/秒から 35000 行/秒に向上し、レプリケーションのレイテンシーが2 秒に短縮されます。
-   データのライフサイクルを管理するために行レベル[<a href="/time-to-live.md">生存時間 (TTL)</a>](/time-to-live.md)を提供します (実験的)。
-   TiCDC は、Amazon S3、Azure Blob Storage、NFS (実験的) など[<a href="/ticdc/ticdc-sink-to-cloud-storage.md">変更されたログをオブジェクトstorageにレプリケートする</a>](/ticdc/ticdc-sink-to-cloud-storage.md)をサポートします。

## 新機能 {#new-features}

### SQL {#sql}

-   インデックスを追加する TiDB のパフォーマンスが約 10 倍向上しました (GA) [<a href="https://github.com/pingcap/tidb/issues/35983">#35983</a>](https://github.com/pingcap/tidb/issues/35983) @ [<a href="https://github.com/benjamin2037">ベンジャミン2037</a>](https://github.com/benjamin2037) @ [<a href="https://github.com/tangenta">タンジェンタ</a>](https://github.com/tangenta)

    TiDB v6.3.0 では、インデックス作成時のバックフィルの速度を向上させるための実験的機能として[<a href="/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630">インデックスアクセラレーションを追加</a>](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)が導入されています。 v6.5.0 では、この機能が GA となり、デフォルトで有効になり、大規模なテーブルでのパフォーマンスが v6.1.0 よりも約 10 倍高速になることが予想されます。高速化機能は、単一の SQL ステートメントでインデックスを連続的に追加するシナリオに適しています。複数の SQL ステートメントが並行してインデックスを追加する場合、SQL ステートメントのうち 1 つだけが高速化されます。

-   軽量メタデータ ロックを提供して、DDL 変更時の DML 成功率 (GA) [<a href="https://github.com/pingcap/tidb/issues/37275">#37275</a>](https://github.com/pingcap/tidb/issues/37275) @ [<a href="https://github.com/wjhuang2016">wjhuang2016</a>](https://github.com/wjhuang2016)を向上させます。

    TiDB v6.3.0 では、実験的機能として[<a href="/metadata-lock.md">メタデータロック</a>](/metadata-lock.md)が導入されています。 DML ステートメントによって引き起こされる`Information schema is changed`エラーを回避するために、TiDB はテーブル メタデータの変更中に DML と DDL の優先順位を調整し、古いメタデータを持つ DML がコミットされるまで進行中の DDL を待機させます。 v6.5.0 では、この機能は GA となり、デフォルトで有効になります。これは、さまざまなタイプの DDL 変更シナリオに適しています。既存のクラスターを v6.5.0 より前のバージョンから v6.5.0 以降にアップグレードすると、TiDB はメタデータ ロックを自動的に有効にします。この機能を無効にするには、システム変数[<a href="/system-variables.md#tidb_enable_metadata_lock-new-in-v630">`tidb_enable_metadata_lock`</a>](/system-variables.md#tidb_enable_metadata_lock-new-in-v630) `OFF`に設定します。

    詳細については、 [<a href="/metadata-lock.md">ドキュメンテーション</a>](/metadata-lock.md)を参照してください。

-   `FLASHBACK CLUSTER TO TIMESTAMP` (GA) [<a href="https://github.com/pingcap/tidb/issues/37197">#37197</a>](https://github.com/pingcap/tidb/issues/37197) [<a href="https://github.com/tikv/tikv/issues/13303">#13303</a>](https://github.com/tikv/tikv/issues/13303) @ [<a href="https://github.com/Defined2014">定義2014</a>](https://github.com/Defined2014) @ [<a href="https://github.com/bb7133">bb7133</a>](https://github.com/bb7133) @ [<a href="https://github.com/JmPotato">Jmポテト</a>](https://github.com/JmPotato) @ [<a href="https://github.com/Connor1996">コナー1996</a>](https://github.com/Connor1996) @ [<a href="https://github.com/HuSharp">ヒューシャープ</a>](https://github.com/HuSharp) @ [<a href="https://github.com/CalvinNeo">カルビンネオ</a>](https://github.com/CalvinNeo)を使用した、特定の時点へのクラスターの復元のサポート

    v6.4.0 以降、TiDB は実験的機能として[<a href="/sql-statements/sql-statement-flashback-to-timestamp.md">`FLASHBACK CLUSTER TO TIMESTAMP`</a>](/sql-statements/sql-statement-flashback-to-timestamp.md)ステートメントを導入しました。このステートメントを使用すると、ガベージ コレクション (GC) の有効期間内の特定の時点にクラスターを復元できます。 v6.5.0 では、この機能は TiCDC および PITR と互換性があり、GA になりました。この機能は、DML の誤った操作を簡単に元に戻し、数分で元のクラスターを復元し、さまざまな時点でデータをロールバックしてデータが変更された正確な時間を判断するのに役立ちます。

    詳細については、 [<a href="/sql-statements/sql-statement-flashback-to-timestamp.md">ドキュメンテーション</a>](/sql-statements/sql-statement-flashback-to-timestamp.md)を参照してください。

-   `INSERT` 、 `REPLACE` 、 `UPDATE` 、 `DELETE` [<a href="https://github.com/pingcap/tidb/issues/33485">#33485</a>](https://github.com/pingcap/tidb/issues/33485) @ [<a href="https://github.com/ekexium">エキシウム</a>](https://github.com/ekexium)を含む非トランザクション DML ステートメントを完全にサポートします。

    大規模なデータ処理のシナリオでは、大規模なトランザクションを含む 1 つの SQL ステートメントがクラスターの安定性とパフォーマンスに悪影響を与える可能性があります。非トランザクション DML ステートメントは、内部実行のために複数の SQL ステートメントに分割された DML ステートメントです。分割ステートメントはトランザクションの原子性と分離性を損ないますが、クラスターの安定性は大幅に向上します。 TiDB は、v6.1.0 以降、非トランザクション`DELETE`ステートメントをサポートし、v6.5.0 以降、非トランザクション`INSERT` 、 `REPLACE` 、および`UPDATE`ステートメントをサポートしています。

    詳細については、 [<a href="/non-transactional-dml.md">非トランザクション DML ステートメント</a>](/non-transactional-dml.md)および[<a href="/sql-statements/sql-statement-batch.md">`BATCH`構文</a>](/sql-statements/sql-statement-batch.md)を参照してください。

-   生存時間 (TTL) (実験的) [<a href="https://github.com/pingcap/tidb/issues/39262">#39262</a>](https://github.com/pingcap/tidb/issues/39262) @ [<a href="https://github.com/lcwangchao">ルクワンチャオ</a>](https://github.com/lcwangchao)のサポート

    TTL は行レベルのデータ有効期間管理を提供します。 TiDB では、TTL 属性を持つテーブルはデータの有効期間を自動的にチェックし、期限切れのデータを行レベルで削除します。 TTL は、オンラインの読み取りおよび書き込みのワークロードに影響を与えることなく、不要なデータを定期的かつタイムリーにクリーンアップできるように設計されています。

    詳細については、 [<a href="/time-to-live.md">ドキュメンテーション</a>](/time-to-live.md)を参照してください。

-   `INSERT INTO SELECT`ステートメントを使用したTiFlashクエリ結果の保存をサポート (実験的) [<a href="https://github.com/pingcap/tidb/issues/37515">#37515</a>](https://github.com/pingcap/tidb/issues/37515) @ [<a href="https://github.com/gengliqi">ゲンリキ</a>](https://github.com/gengliqi)

    v6.5.0 以降、TiDB は`INSERT INTO SELECT`ステートメントの`SELECT`句 (分析クエリ) をTiFlashにプッシュダウンすることをサポートします。このようにして、さらに分析するために、 TiFlashクエリ結果を`INSERT INTO`で指定された TiDB テーブルに簡単に保存できます。これは、結果のキャッシュ (つまり、結果の具体化) として有効になります。例えば：

    ```sql
    INSERT INTO t2 SELECT Mod(x,y) FROM t1;
    ```

    実験的段階では、この機能はデフォルトで無効になっています。これを有効にするには、 [<a href="/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-new-in-v630">`tidb_enable_tiflash_read_for_write_stmt`</a>](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-new-in-v630)システム変数を`ON`に設定します。この機能の`INSERT INTO`で指定される結果テーブルには特別な制限はなく、その結果テーブルにTiFlashレプリカを追加するかどうかは自由です。この機能の一般的な使用シナリオは次のとおりです。

    -   TiFlashを使用して複雑な分析クエリを実行する
    -   TiFlashクエリ結果を再利用するか、高度な同時オンライン要求に対処します
    -   入力データ サイズと比較して比較的小さい結果セットが必要です。できれば 100 MiB 未満です。

    詳細については、 [<a href="/tiflash/tiflash-results-materialization.md">ドキュメンテーション</a>](/tiflash/tiflash-results-materialization.md)を参照してください。

-   バインディング履歴実行プランのサポート (実験的) [<a href="https://github.com/pingcap/tidb/issues/39199">#39199</a>](https://github.com/pingcap/tidb/issues/39199) @ [<a href="https://github.com/fzzf678">fzzf678</a>](https://github.com/fzzf678)

    SQL ステートメントの場合、実行中のさまざまな要因により、オプティマイザが以前の最適な実行プランではなく新しい実行プランを選択することがあり、SQL パフォーマンスに影響が及びます。この場合、最適な実行計画がクリアされていない場合は、SQL 実行履歴に残ります。

    v6.5.0 では、TiDB は[<a href="/sql-statements/sql-statement-create-binding.md">`CREATE [GLOBAL | SESSION] BINDING`</a>](/sql-statements/sql-statement-create-binding.md)ステートメントのバインディング オブジェクトを拡張することにより、履歴実行プランのバインディングをサポートします。 SQL ステートメントの実行計画が変更された場合、元の実行計画が SQL 実行履歴メモリテーブルに残っている限り、 `CREATE [GLOBAL | SESSION] BINDING`ステートメントに`plan_digest`指定して元の実行計画をバインドし、SQL パフォーマンスを迅速に回復できます (たとえば、 `statements_summary` ）。この機能により、実行計画の変更の問題を処理するプロセスが簡素化され、メンテナンスの効率が向上します。

    詳細については、 [<a href="/sql-plan-management.md#create-a-binding-according-to-a-historical-execution-plan">ドキュメンテーション</a>](/sql-plan-management.md#create-a-binding-according-to-a-historical-execution-plan)を参照してください。

### Security {#security}

-   パスワードの複雑さのポリシー[<a href="https://github.com/pingcap/tidb/issues/38928">#38928</a>](https://github.com/pingcap/tidb/issues/38928) @ [<a href="https://github.com/CbcWestwolf">Cbcウェストウルフ</a>](https://github.com/CbcWestwolf)をサポートします。

    このポリシーを有効にした後、パスワードを設定すると、TiDB はパスワードの長さ、パスワード内の大文字と小文字、数字、特殊文字が十分であるかどうか、パスワードが辞書と一致するかどうか、およびパスワードがユーザー名と一致するかどうかをチェックします。これにより、安全なパスワードを設定できます。

    TiDB は、パスワードの強度を検証する SQL 関数[<a href="https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_validate-password-strength">`VALIDATE_PASSWORD_STRENGTH()`</a>](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_validate-password-strength)を提供します。

    詳細については、 [<a href="/password-management.md#password-complexity-policy">ドキュメンテーション</a>](/password-management.md#password-complexity-policy)を参照してください。

-   パスワード有効期限ポリシー[<a href="https://github.com/pingcap/tidb/issues/38936">#38936</a>](https://github.com/pingcap/tidb/issues/38936) @ [<a href="https://github.com/CbcWestwolf">Cbcウェストウルフ</a>](https://github.com/CbcWestwolf)のサポート

    TiDB は、手動有効期限、グローバルレベルの自動有効期限、アカウントレベルの自動有効期限などのパスワード有効期限ポリシーの構成をサポートしています。このポリシーを有効にした後は、パスワードを定期的に変更する必要があります。これにより、長期使用によるパスワード漏洩のリスクが軽減され、パスワードのセキュリティが向上します。

    詳細については、 [<a href="/password-management.md#password-expiration-policy">ドキュメンテーション</a>](/password-management.md#password-expiration-policy)を参照してください。

-   パスワード再利用ポリシー[<a href="https://github.com/pingcap/tidb/issues/38937">#38937</a>](https://github.com/pingcap/tidb/issues/38937) @ [<a href="https://github.com/keeplearning20221">キープラーニング20221</a>](https://github.com/keeplearning20221)のサポート

    TiDB は、グローバル レベルのパスワード再利用ポリシーやアカウント レベルのパスワード再利用ポリシーなど、パスワード再利用ポリシーの構成をサポートしています。このポリシーを有効にすると、指定した期間内に使用したパスワード、または最近使用したいくつかのパスワードは使用できなくなります。これにより、パスワードの繰り返し使用によるパスワード漏洩のリスクが軽減され、パスワードのセキュリティが向上します。

    詳細については、 [<a href="/password-management.md#password-reuse-policy">ドキュメンテーション</a>](/password-management.md#password-reuse-policy)を参照してください。

-   失敗したログインの追跡と一時的なアカウント ロック ポリシー[<a href="https://github.com/pingcap/tidb/issues/38938">#38938</a>](https://github.com/pingcap/tidb/issues/38938) @ [<a href="https://github.com/lastincisor">最後切歯</a>](https://github.com/lastincisor)をサポート

    このポリシーを有効にした後、間違ったパスワードを連続して複数回使用して TiDB にログインすると、アカウントは一時的にロックされます。ロック時間が終了すると、アカウントのロックは自動的に解除されます。

    詳細については、 [<a href="/password-management.md#failed-login-tracking-and-temporary-account-locking-policy">ドキュメンテーション</a>](/password-management.md#failed-login-tracking-and-temporary-account-locking-policy)を参照してください。

### 可観測性 {#observability}

-   TiDB ダッシュボードは、独立したポッド[<a href="https://github.com/pingcap/tidb-dashboard/issues/1447">#1447</a>](https://github.com/pingcap/tidb-dashboard/issues/1447) @ [<a href="https://github.com/SabaPing">サバピン</a>](https://github.com/SabaPing)として Kubernetes にデプロイできます。

    TiDB v6.5.0 (以降) およびTiDB Operator v1.4.0 (以降) は、Kubernetes 上の独立したポッドとして TiDB ダッシュボードをデプロイすることをサポートしています。 TiDB Operatorを使用すると、このポッドの IP アドレスにアクセスして TiDB ダッシュボードを起動できます。

    TiDB ダッシュボードを独立して展開すると、次の利点があります。

    -   TiDB ダッシュボードのコンピューティング作業は、PD ノードに負担をかけません。これにより、より安定したクラスター動作が保証されます。
    -   PD ノードが利用できない場合でも、ユーザーは診断のために TiDB ダッシュボードにアクセスできます。
    -   インターネット上の TiDB ダッシュボードへのアクセスには、PD の特権インターフェイスは必要ありません。したがって、クラスターのセキュリティ リスクが軽減されます。

    詳細については、 [<a href="https://docs.pingcap.com/tidb-in-kubernetes/dev/get-started#deploy-tidb-dashboard-independently">ドキュメンテーション</a>](https://docs.pingcap.com/tidb-in-kubernetes/dev/get-started#deploy-tidb-dashboard-independently)を参照してください。

-   パフォーマンス概要ダッシュボードにTiFlashおよび CDC (変更データ キャプチャ) パネルが追加されました[<a href="https://github.com/pingcap/tidb/issues/39230">#39230</a>](https://github.com/pingcap/tidb/issues/39230) @ [<a href="https://github.com/dbsid">DBID</a>](https://github.com/dbsid)

    v6.1.0 以降、TiDB は Grafana にパフォーマンス概要ダッシュボードを導入しました。これは、TiDB、TiKV、および PD の全体的なパフォーマンス診断のためのシステム レベルのエントリを提供します。 v6.5.0 では、パフォーマンス概要ダッシュボードにTiFlashと CDC パネルが追加されます。 v6.5.0 以降、これらのパネルでは、パフォーマンス概要ダッシュボードを使用して、TiDB クラスター内のすべてのコンポーネントのパフォーマンスを分析できます。

    TiFlashおよび CDC パネルは、 TiFlashおよび TiCDC の監視情報を再編成するため、 TiFlashおよび TiCDC のパフォーマンス問題の分析およびトラブルシューティングの効率を大幅に向上させることができます。

    -   [<a href="/grafana-performance-overview-dashboard.md#tiflash">TiFlashパネル</a>](/grafana-performance-overview-dashboard.md#tiflash)では、 TiFlashクラスターのリクエスト タイプ、レイテンシー分析、およびリソース使用量の概要を簡単に表示できます。
    -   [<a href="/grafana-performance-overview-dashboard.md#cdc">CDCパネル</a>](/grafana-performance-overview-dashboard.md#cdc)では、TiCDC クラスターの健全性、レプリケーションレイテンシー、データ フロー、ダウンストリーム書き込みレイテンシーを簡単に表示できます。

    詳細については、 [<a href="/performance-tuning-methods.md">ドキュメンテーション</a>](/performance-tuning-methods.md)を参照してください。

### パフォーマンス {#performance}

-   [<a href="/glossary.md#index-merge">インデックスのマージ</a>](/glossary.md#index-merge) `AND` [<a href="https://github.com/pingcap/tidb/issues/39333">#39333</a>](https://github.com/pingcap/tidb/issues/39333) @ [<a href="https://github.com/guo-shaoge">グオシャオゲ</a>](https://github.com/guo-shaoge) @ [<a href="https://github.com/time-and-fate">時間と運命</a>](https://github.com/time-and-fate) @ [<a href="https://github.com/hailanwhu">ハイランフー</a>](https://github.com/hailanwhu)で接続された式をサポートします

    v6.5.0 より前では、TiDB は`OR`で接続されたフィルター条件に対するインデックス マージの使用のみをサポートしていました。 v6.5.0 以降、TiDB は`WHERE`句の`AND`で接続されたフィルタ条件のインデックス マージの使用をサポートしました。このようにして、TiDB のインデックス マージは、クエリ フィルター条件のより一般的な組み合わせをカバーできるようになり、union ( `OR` ) 関係に限定されなくなりました。現在の v6.5.0 バージョンは、オプティマイザによって自動的に選択された`OR`条件でのインデックス マージのみをサポートします。 `AND`条件のインデックス マージを有効にするには、 [<a href="/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-">`USE_INDEX_MERGE`</a>](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)ヒントを使用する必要があります。

    インデックスのマージの詳細については、 [<a href="/releases/release-5.4.0.md#performance">v5.4.0 リリースノート</a>](/releases/release-5.4.0.md#performance)および[<a href="/explain-index-merge.md">インデックスのマージについて説明する</a>](/explain-index-merge.md)を参照してください。

-   次の JSON関数のTiFlash [<a href="https://github.com/pingcap/tidb/issues/39458">#39458</a>](https://github.com/pingcap/tidb/issues/39458) @ [<a href="https://github.com/yibin87">イービン87</a>](https://github.com/yibin87)へのプッシュダウンをサポート

    -   `->`
    -   `->>`
    -   `JSON_EXTRACT()`

    JSON 形式は、アプリケーション データ モデリングのための柔軟な方法を提供します。そのため、データ交換やデータstorageに JSON 形式を使用するアプリケーションが増えています。 JSON関数をTiFlashにプッシュダウンすることで、JSON タイプのデータ分析の効率が向上し、よりリアルタイムな分析シナリオに TiDB を使用できます。

-   次の文字列関数のTiFlash [<a href="https://github.com/pingcap/tiflash/issues/6115">#6115</a>](https://github.com/pingcap/tiflash/issues/6115) @ [<a href="https://github.com/xzhangxian1008">xzhangxian1008</a>](https://github.com/xzhangxian1008)へのプッシュダウンをサポート

    -   `regexp_like`
    -   `regexp_instr`
    -   `regexp_substr`

-   [<a href="/views.md">ビュー</a>](/views.md) [<a href="https://github.com/pingcap/tidb/issues/37887">#37887</a>](https://github.com/pingcap/tidb/issues/37887) @ [<a href="https://github.com/Reminiscent">懐かしい</a>](https://github.com/Reminiscent)での実行計画の生成を妨げるグローバル オプティマイザー ヒントをサポートします。

    一部のビュー アクセス シナリオでは、最適なパフォーマンスを達成するために、オプティマイザー ヒントを使用してビュー内のクエリの実行計画に干渉する必要があります。 v6.5.0 以降、TiDB はビュー内のクエリ ブロックへのグローバル ヒントの追加をサポートし、クエリで定義されたヒントがビュー内で有効になります。この機能は、ネストされたビューを含む複雑な SQL ステートメントにヒントを挿入する方法を提供し、実行計画の制御を強化し、複雑なステートメントのパフォーマンスを安定させます。グローバル ヒントを使用するには、 [<a href="/optimizer-hints.md#step-1-define-the-query-block-name-of-the-view-using-the-qb_name-hint">クエリブロックに名前を付けます</a>](/optimizer-hints.md#step-1-define-the-query-block-name-of-the-view-using-the-qb_name-hint)と[<a href="/optimizer-hints.md#step-2-add-the-target-hints">ヒント参照を指定する</a>](/optimizer-hints.md#step-2-add-the-target-hints)を行う必要があります。

    詳細については、 [<a href="/optimizer-hints.md#hints-that-take-effect-globally">ドキュメンテーション</a>](/optimizer-hints.md#hints-that-take-effect-globally)を参照してください。

-   [<a href="/partitioned-table.md">パーティション化されたテーブル</a>](/partitioned-table.md)から TiKV [<a href="https://github.com/pingcap/tidb/issues/26166">#26166</a>](https://github.com/pingcap/tidb/issues/26166) @ [<a href="https://github.com/winoros">ウィノロス</a>](https://github.com/winoros)までのソート操作のプッシュダウンをサポート

    [<a href="/partitioned-table.md">パーティションテーブル</a>](/partitioned-table.md)機能は v6.1.0 以降 GA になっていますが、TiDB は継続的にパフォーマンスを向上させています。 v6.5.0 では、TiDB は、計算とフィルタリングのために`ORDER BY`や`LIMIT`の並べ替え操作を TiKV にプッシュダウンすることをサポートします。これにより、パーティション分割テーブルを使用する場合、ネットワーク I/O オーバーヘッドが削減され、SQL パフォーマンスが向上します。

-   オプティマイザーは、より正確なコスト モデル バージョン 2 (GA) [<a href="https://github.com/pingcap/tidb/issues/35240">#35240</a>](https://github.com/pingcap/tidb/issues/35240) @ [<a href="https://github.com/qw4990">qw4990</a>](https://github.com/qw4990)を導入します。

    TiDB v6.2.0 では、実験的機能として[<a href="/cost-model.md#cost-model-version-2">コストモデルバージョン2</a>](/cost-model.md#cost-model-version-2)が導入されています。このモデルは、オプティマイザーが最適な実行計画を選択できるように、より正確なコスト推定方法を使用します。特にTiFlashが導入されている場合、コスト モデル バージョン 2 は適切なstorageエンジンの選択を自動的に支援し、多くの手動介入を回避します。一定期間の実際のシーンでのテストの後、このモデルは v6.5.0 で GA になります。 v6.5.0 以降、新しく作成されたクラスターはデフォルトでコスト モデル バージョン 2 を使用します。クラスターを v6.5.0 にアップグレードする場合、コスト モデル バージョン 2 によってクエリ プランが変更される可能性があるため、十分なパフォーマンス テストを行った後、新しいコスト モデルを使用するように[<a href="/system-variables.md#tidb_cost_model_version-new-in-v620">`tidb_cost_model_version = 2`</a>](/system-variables.md#tidb_cost_model_version-new-in-v620)変数を設定できます。

    コスト モデル バージョン 2 は、TiDB オプティマイザーの全体的な機能を大幅に向上させ、TiDB がより強力な HTAP データベースに向けて進化するのに役立つ機能として一般提供されます。

    詳細については、 [<a href="/cost-model.md#cost-model-version-2">ドキュメンテーション</a>](/cost-model.md#cost-model-version-2)を参照してください。

-   TiFlash は、テーブルの行数[<a href="https://github.com/pingcap/tidb/issues/37165">#37165</a>](https://github.com/pingcap/tidb/issues/37165) @ [<a href="https://github.com/elsa0520">エルサ0520</a>](https://github.com/elsa0520)を取得する操作を最適化します。

    データ分析のシナリオでは、フィルター条件なしでテーブルの実際の行数を 1 から`COUNT(*)`まで取得するのが一般的な操作です。 v6.5.0 では、 TiFlash は`COUNT(*)`の書き換えを最適化し、行数をカウントするために最も短い列定義を持つ null 以外の列を自動的に選択します。これにより、 TiFlashの I/O 操作の数が効果的に削減され、TiFlash の実行効率が向上します。行数を取得しています。

### 安定性 {#stability}

-   グローバルメモリ制御機能は GA [<a href="https://github.com/pingcap/tidb/issues/37816">#37816</a>](https://github.com/pingcap/tidb/issues/37816) @ [<a href="https://github.com/wshwsh12">wshwsh12</a>](https://github.com/wshwsh12)になりました

    v6.4.0 以降、TiDB は実験的機能としてグローバルメモリ制御を導入しました。 v6.5.0 では GA となり、メインメモリの消費量を追跡できるようになります。グローバルメモリ消費量が[<a href="/system-variables.md#tidb_server_memory_limit-new-in-v640">`tidb_server_memory_limit`</a>](/system-variables.md#tidb_server_memory_limit-new-in-v640)で定義されたしきい値に達すると、TiDB は安定性を確保するために GC または SQL 操作のキャンセルによってメモリ使用量を制限しようとします。

    セッション内のトランザクションによって消費されるメモリ(最大値は構成項目[<a href="/tidb-configuration-file.md#txn-total-size-limit">`txn-total-size-limit`</a>](/tidb-configuration-file.md#txn-total-size-limit)によって以前に設定されていました) は、単一セッションのメモリ消費量がシステム変数[<a href="/system-variables.md#tidb_mem_quota_query">`tidb_mem_quota_query`</a>](/system-variables.md#tidb_mem_quota_query)によって定義されたしきい値に達したとき、メモリ管理モジュールによって追跡されるようになったことに注意してください。 、システム変数[<a href="/system-variables.md#tidb_mem_oom_action-new-in-v610">`tidb_mem_oom_action`</a>](/system-variables.md#tidb_mem_oom_action-new-in-v610)で定義された動作がトリガーされます (デフォルトは`CANCEL` 、つまり操作をキャンセルします)。上位互換性を確保するために、 [<a href="/tidb-configuration-file.md#txn-total-size-limit">`txn-total-size-limit`</a>](/tidb-configuration-file.md#txn-total-size-limit)がデフォルト以外の値として構成されている場合でも、TiDB はトランザクションが`txn-total-size-limit`で設定されたメモリを使用できることを保証します。

    TiDB v6.5.0 以降を使用している場合は、 [<a href="/tidb-configuration-file.md#txn-total-size-limit">`txn-total-size-limit`</a>](/tidb-configuration-file.md#txn-total-size-limit)削除し、トランザクションのメモリ使用量に別個の制限を設定しないことをお勧めします。代わりに、システム変数[<a href="/system-variables.md#tidb_mem_quota_query">`tidb_mem_quota_query`</a>](/system-variables.md#tidb_mem_quota_query)および[<a href="/system-variables.md#tidb_server_memory_limit-new-in-v640">`tidb_server_memory_limit`</a>](/system-variables.md#tidb_server_memory_limit-new-in-v640)を使用してグローバルメモリを管理し、メモリ使用効率を向上させることができます。

    詳細については、 [<a href="/configure-memory-usage.md">ドキュメンテーション</a>](/configure-memory-usage.md)を参照してください。

### 使いやすさ {#ease-of-use}

-   `EXPLAIN ANALYZE`出力[<a href="https://github.com/pingcap/tiflash/issues/5926">#5926</a>](https://github.com/pingcap/tiflash/issues/5926) @ [<a href="https://github.com/hongyunyan">ホンユニャン</a>](https://github.com/hongyunyan)のTiFlash `TableFullScan`オペレーターの実行情報を調整します。

    `EXPLAIN ANALYZE`ステートメントは、実行計画とランタイム統計を出力するために使用されます。 v6.5.0 では、 TiFlash はDMFile 関連の実行情報を追加することにより、 `TableFullScan`オペレーターの実行情報を改良しました。 TiFlashデータ スキャン ステータス情報がより直観的に表示されるようになり、 TiFlash のパフォーマンスをより簡単に分析できるようになりました。

    詳細については、 [<a href="/sql-statements/sql-statement-explain-analyze.md">ドキュメンテーション</a>](/sql-statements/sql-statement-explain-analyze.md)を参照してください。

-   JSON 形式[<a href="https://github.com/pingcap/tidb/issues/39261">#39261</a>](https://github.com/pingcap/tidb/issues/39261) @ [<a href="https://github.com/fzzf678">fzzf678</a>](https://github.com/fzzf678)での実行プランの出力をサポートします。

    v6.5.0 では、TiDB は実行プランの出力形式を拡張します。 `EXPLAIN`ステートメントに`FORMAT = "tidb_json"`を指定すると、SQLの実行計画をJSON形式で出力できます。この機能により、SQL デバッグ ツールと診断ツールは実行計画をより便利かつ正確に読み取ることができるため、SQL の診断とチューニングの使いやすさが向上します。

    詳細については、 [<a href="/sql-statements/sql-statement-explain.md">ドキュメンテーション</a>](/sql-statements/sql-statement-explain.md)を参照してください。

### MySQLの互換性 {#mysql-compatibility}

-   高性能でグローバルに単調な`AUTO_INCREMENT`列属性 (GA) [<a href="https://github.com/pingcap/tidb/issues/38442">#38442</a>](https://github.com/pingcap/tidb/issues/38442) @ [<a href="https://github.com/tiancaiamao">ティエンチャイアマオ</a>](https://github.com/tiancaiamao)をサポート

    v6.4.0 以降、TiDB は実験的機能として`AUTO_INCREMENT` MySQL 互換モードを導入しました。このモードでは、すべての TiDB インスタンスで ID が単調増加することを保証する、集中型の自動インクリメント ID 割り当てサービスが導入されています。この機能により、クエリ結果を自動インクリメント ID で簡単に並べ替えることができます。 v6.5.0 では、この機能は GA になります。この機能を使用したテーブルの挿入 TPS は 20,000 を超えることが予想され、この機能は単一テーブルとクラスター全体の書き込みスループットを向上させるエラスティック スケーリングをサポートしています。 MySQL 互換モードを使用するには、テーブル作成時に`AUTO_ID_CACHE` ～ `1`を設定する必要があります。以下は例です。

    ```sql
    CREATE TABLE t(a int AUTO_INCREMENT key) AUTO_ID_CACHE 1;
    ```

    詳細については、 [<a href="/auto-increment.md#mysql-compatibility-mode">ドキュメンテーション</a>](/auto-increment.md#mysql-compatibility-mode)を参照してください。

### データ移行 {#data-migration}

-   gzip、snappy、zstd 圧縮形式での SQL および CSV ファイルのエクスポートとインポートをサポート[<a href="https://github.com/pingcap/tidb/issues/38514">#38514</a>](https://github.com/pingcap/tidb/issues/38514) @ [<a href="https://github.com/lichunzhu">リチュンジュ</a>](https://github.com/lichunzhu)

    Dumpling は、 gzip、snappy、zstd の圧縮形式での圧縮 SQL および CSV ファイルへのデータのエクスポートをサポートしています。 TiDB Lightning は、これらの形式の圧縮ファイルのインポートもサポートしています。

    以前は、CSV ファイルや SQL ファイルを保存するためにデータをエクスポートまたはインポートするために大規模なstorageスペースを提供する必要があり、storageコストが高くなっていました。この機能のリリースにより、データ ファイルを圧縮することでstorageコストを大幅に削減できます。

    詳細については、 [<a href="/dumpling-overview.md#improve-export-efficiency-through-concurrency">ドキュメンテーション</a>](/dumpling-overview.md#improve-export-efficiency-through-concurrency)を参照してください。

-   binlog解析機能を最適化[<a href="https://github.com/pingcap/dm/issues/924">#924</a>](https://github.com/pingcap/dm/issues/924) @ [<a href="https://github.com/GMHDBJD">gmhdbjd</a>](https://github.com/GMHDBJD)

    TiDB は、移行タスクに含まれていないスキーマとテーブルのbinlogイベントをフィルターで除外できるため、解析の効率と安定性が向上します。このポリシーは、v6.5.0 ではデフォルトで有効になります。追加の構成は必要ありません。

    以前は、少数のテーブルのみを移行する場合でも、アップストリームのbinlogファイル全体を解析する必要がありました。移行する必要のないbinlogファイル内のテーブルのbinlogイベントも解析する必要があり、効率的ではありませんでした。一方、これらのbinlogイベントが解析をサポートしていない場合、タスクは失敗します。移行タスク内のテーブルのbinlogイベントのみを解析することにより、binlogの解析効率が大幅に向上し、タスクの安定性が向上します。

-   TiDB Lightningのディスク クォータは GA [<a href="https://github.com/pingcap/tidb-lightning/issues/446">#446</a>](https://github.com/pingcap/tidb-lightning/issues/446) @ [<a href="https://github.com/buchuitoudegou">ブチュイトデゴウ</a>](https://github.com/buchuitoudegou)です

    TiDB Lightningのディスク クォータを構成できます。十分なディスク クォータがない場合、 TiDB Lightning はソース データの読み取りと一時ファイルの書き込みを停止します。代わりに、ソートされたキーと値を最初に TiKV に書き込み、 TiDB Lightning がローカル一時ファイルを削除した後、インポート プロセスを続行します。

    以前は、 TiDB Lightning が物理モードを使用してデータをインポートすると、生データのエンコード、並べ替え、分割のためにローカル ディスクに大量の一時ファイルが作成されていました。ローカル ディスクのスペースがなくなると、ファイルへの書き込みに失敗し、 TiDB Lightning がエラーで終了します。この機能を使用すると、 TiDB Lightningタスクでローカル ディスクの上書きを回避できます。

    詳細については、 [<a href="/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#configure-disk-quota-new-in-v620">ドキュメンテーション</a>](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#configure-disk-quota-new-in-v620)を参照してください。

-   DM での継続的なデータ検証は GA [<a href="https://github.com/pingcap/tiflow/issues/4426">#4426</a>](https://github.com/pingcap/tiflow/issues/4426) @ [<a href="https://github.com/D3Hunter">D3ハンター</a>](https://github.com/D3Hunter)です

    増分データを上流データベースから下流データベースに移行するプロセスでは、データ フローによってエラーやデータ損失が発生する可能性がわずかにあります。クレジットや証券ビジネスなど、強力なデータ一貫性が必要なシナリオでは、移行後にデータに対してフルボリュームのチェックサムを実行して、データの一貫性を確保できます。ただし、一部の増分レプリケーション シナリオでは、アップストリームとダウンストリームのデータが常に変化するため、アップストリームとダウンストリームの書き込みは継続的かつ中断されず、すべてのデータの整合性チェックを実行することが困難になります。

    以前は、完全なデータを検証するにはビジネスを中断する必要があり、ビジネスに影響を与える可能性がありました。この機能を使用すると、ビジネスを中断することなく増分データ検証を実行できるようになります。

    詳細については、 [<a href="/dm/dm-continuous-data-validation.md">ドキュメンテーション</a>](/dm/dm-continuous-data-validation.md)を参照してください。

### TiDB データ共有サブスクリプション {#tidb-data-share-subscription}

-   TiCDC は、変更されたログのstorageシンクへのレプリケーションをサポートします (実験的) [<a href="https://github.com/pingcap/tiflow/issues/6797">#6797</a>](https://github.com/pingcap/tiflow/issues/6797) @ [<a href="https://github.com/zhaoxinyu">ジャオシンユ</a>](https://github.com/zhaoxinyu)

    TiCDC は、変更されたログの Amazon S3、Azure Blob Storage、NFS、およびその他の S3 互換storageサービスへのレプリケートをサポートしています。クラウドstorageは価格も手頃で使いやすいです。 Kafka を使用していない場合は、storageシンクを使用できます。 TiCDC は、変更されたログをファイルに保存し、それをstorageシステムに送信します。コンシューマ プログラムは、storageシステムから、新しく生成された変更されたログ ファイルを定期的に読み取ります。

    storageシンクは、canal-json および CSV 形式の変更されたログをサポートします。詳細については、 [<a href="/ticdc/ticdc-sink-to-cloud-storage.md">ドキュメンテーション</a>](/ticdc/ticdc-sink-to-cloud-storage.md)を参照してください。

-   TiCDC は、2 つのクラスター[<a href="https://github.com/pingcap/tidb/issues/38587">#38587</a>](https://github.com/pingcap/tidb/issues/38587) @ [<a href="https://github.com/xiongjiwei">ションジウェイ</a>](https://github.com/xiongjiwei) @ [<a href="https://github.com/asddongmen">東門</a>](https://github.com/asddongmen)間の双方向レプリケーションをサポートします。

    TiCDC は、2 つの TiDB クラスター間の双方向レプリケーションをサポートします。アプリケーション用に地理的に分散された複数のアクティブなデータ センターを構築する必要がある場合は、この機能をソリューションとして使用できます。 1 つの TiDB クラスターから別の TiDB クラスターへの TiCDC 変更フィードの`bdr-mode = true`パラメーターを構成することにより、2 つの TiDB クラスター間で双方向のデータ レプリケーションを実現できます。

    詳細については、 [<a href="/ticdc/ticdc-bidirectional-replication.md">ドキュメンテーション</a>](/ticdc/ticdc-bidirectional-replication.md)を参照してください。

-   TiCDC は TLS オンライン[<a href="https://github.com/pingcap/tiflow/issues/7908">#7908</a>](https://github.com/pingcap/tiflow/issues/7908) @ [<a href="https://github.com/CharlesCheung96">CharlesCheung96</a>](https://github.com/CharlesCheung96)の更新をサポートします

    データベース システムのセキュリティを維持するには、システムで使用される証明書の有効期限ポリシーを設定する必要があります。有効期限が過ぎると、システムには新しい証明書が必要になります。 TiCDC v6.5.0 は、TLS 証明書のオンライン更新をサポートしています。 TiCDC は、レプリケーション タスクを中断することなく、手動介入を必要とせずに証明書を自動的に検出して更新できます。

-   TiCDC のパフォーマンスが大幅に向上[<a href="https://github.com/pingcap/tiflow/issues/7540">#7540</a>](https://github.com/pingcap/tiflow/issues/7540) [<a href="https://github.com/pingcap/tiflow/issues/7478">#7478</a>](https://github.com/pingcap/tiflow/issues/7478) [<a href="https://github.com/pingcap/tiflow/issues/7532">#7532</a>](https://github.com/pingcap/tiflow/issues/7532) @ [<a href="https://github.com/sdojjy">スドジ</a>](https://github.com/sdojjy) [<a href="https://github.com/3AceShowHand">@3AceShowHand</a>](https://github.com/3AceShowHand)

    TiDB クラスターのテスト シナリオでは、TiCDC のパフォーマンスが大幅に向上しました。具体的には、Kafka にデータをレプリケートするシナリオでは、単一の TiCDC が処理できる最大行変更は 30K 行/秒に達し、レプリケーションのレイテンシーは10 秒に短縮されます。 TiKV および TiCDC のローリング アップグレード中であっても、レプリケーションのレイテンシーは 30 秒未満です。

    災害復旧 (DR) シナリオでは、TiCDC REDO ログと同期ポイントが有効になっている場合、TiCDC スループット[<a href="/replicate-data-to-kafka.md">Kafka へのデータの複製</a>](/replicate-data-to-kafka.md)を 4000 行/秒から 35000 行/秒に改善でき、レプリケーションのレイテンシーを2 秒に制限できます。

### バックアップと復元 {#backup-and-restore}

-   TiDB バックアップ &amp; リストアはスナップショット チェックポイント バックアップ[<a href="https://github.com/pingcap/tidb/issues/38647">#38647</a>](https://github.com/pingcap/tidb/issues/38647) @ [<a href="https://github.com/Leavrth">レヴルス</a>](https://github.com/Leavrth)をサポートします

    TiDB スナップショット バックアップは、チェックポイントからのバックアップの再開をサポートしています。バックアップと復元 (BR) で回復可能なエラーが発生すると、バックアップが再試行されます。ただし、再試行が数回失敗すると、 BR は終了します。チェックポイント バックアップ機能を使用すると、数十分にわたるネットワーク障害など、より長時間の回復可能な障害の再試行が可能になります。

    BR終了後 1 時間以内にシステムを障害から回復しないと、バックアップされるスナップショット データが GC メカニズムによって再利用され、バックアップが失敗する可能性があることに注意してください。詳細については、 [<a href="/br/br-checkpoint-backup.md#backup-retry-must-be-prior-to-gc">ドキュメンテーション</a>](/br/br-checkpoint-backup.md#backup-retry-must-be-prior-to-gc)を参照してください。

-   PITR性能が大幅に向上[<a href="https://github.com/joccau">@ジョッカウ</a>](https://github.com/joccau)

    ログ復元段階では、1 つの TiKV の復元速度が 9 MiB/s に達し、これは以前より 50% 速くなります。復元速度はスケーラブルであり、DR シナリオの RTO が大幅に短縮されます。 DR シナリオの RPO は最短 5 分です。通常のクラスターの運用および保守 (OM) では、たとえば、ローリング アップグレードが実行されるか、1 つの TiKV のみが停止している場合、RPO は 5 分になることがあります。

-   TiKV- BR GA: RawKV [<a href="https://github.com/tikv/migration/issues/67">#67</a>](https://github.com/tikv/migration/issues/67) @ [<a href="https://github.com/pingyu">ピンギュ</a>](https://github.com/pingyu) @ [<a href="https://github.com/haojinming">ハオジンミン</a>](https://github.com/haojinming)のバックアップと復元をサポート

    TiKV- BR は、TiKV クラスターで使用されるバックアップおよび復元ツールです。 TiKV と PD は、TiDB なしで使用される場合、RawKV と呼ばれる KV データベースを構成できます。 TiKV- BR は、 RawKV を使用する製品のデータのバックアップと復元をサポートしています。 TiKV- BR は、 TiKV クラスターの[<a href="/tikv-configuration-file.md#api-version-new-in-v610">`api-version`</a>](/tikv-configuration-file.md#api-version-new-in-v610) `API V1`から`API V2`にアップグレードすることもできます。

    詳細については、 [<a href="https://tikv.org/docs/latest/concepts/explore-tikv-features/backup-restore/">ドキュメンテーション</a>](https://tikv.org/docs/latest/concepts/explore-tikv-features/backup-restore/)を参照してください。

## 互換性の変更 {#compatibility-changes}

### システム変数 {#system-variables}

| 変数名                                                                                                                                                                                                                | 種類の変更    | 説明                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `tidb_enable_amend_pessimistic_txn`                                                                                                                                                                                | 廃止されました  | v6.5.0 以降、この変数は非推奨となり、TiDB は`Information schema is changed`エラーを回避するためにデフォルトで[<a href="/metadata-lock.md">メタデータロック</a>](/metadata-lock.md)機能を使用します。                                                                                                                                                                                                                                                                                               |
| [<a href="/system-variables.md#tidb_enable_outer_join_reorder-new-in-v610">`tidb_enable_outer_join_reorder`</a>](/system-variables.md#tidb_enable_outer_join_reorder-new-in-v610)                                  | 修正済み     | さらにテストを行った後、デフォルト値を`OFF`から`ON`変更します。これは、 [<a href="/join-reorder.md">結合したテーブルの再配置</a>](/join-reorder.md)アルゴリズムのアウター結合のサポートがデフォルトで有効になることを意味します。                                                                                                                                                                                                                                                                                                  |
| [<a href="/system-variables.md#tidb_cost_model_version-new-in-v620">`tidb_cost_model_version`</a>](/system-variables.md#tidb_cost_model_version-new-in-v620)                                                       | 修正済み     | さらにテストを行った後、デフォルト値を`1`から`2`に変更します。これは、デフォルトでインデックス選択と演算子の選択にコスト モデル バージョン 2 が使用されることを意味します。                                                                                                                                                                                                                                                                                                                                                      |
| [<a href="/system-variables.md#tidb_enable_gc_aware_memory_track">`tidb_enable_gc_aware_memory_track`</a>](/system-variables.md#tidb_enable_gc_aware_memory_track)                                                 | 修正済み     | デフォルト値を`ON`から`OFF`に変更します。 GC 対応メモリトラックがテストで不正確であることが判明し、追跡される分析メモリサイズが大きすぎるため、メモリトラックは無効になっています。さらに、 Golang 1.19 では、GC 対応メモリトラックによって追跡されるメモリはメモリ全体に大きな影響を与えません。                                                                                                                                                                                                                                                                                  |
| [<a href="/system-variables.md#tidb_enable_metadata_lock-new-in-v630">`tidb_enable_metadata_lock`</a>](/system-variables.md#tidb_enable_metadata_lock-new-in-v630)                                                 | 修正済み     | さらにテストを行った後、デフォルト値を`OFF`から`ON`に変更します。これは、メタデータ ロック機能がデフォルトで有効になることを意味します。                                                                                                                                                                                                                                                                                                                                                                        |
| [<a href="/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-new-in-v630">`tidb_enable_tiflash_read_for_write_stmt`</a>](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-new-in-v630)       | 修正済み     | v6.5.0 から有効になります。 `INSERT` 、および`UPDATE` `DELETE`含む SQL ステートメントの読み取り操作をTiFlashにプッシュダウンできるかどうかを制御します。デフォルト値は`OFF`です。                                                                                                                                                                                                                                                                                                                               |
| [<a href="/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630">`tidb_ddl_enable_fast_reorg`</a>](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)                                              | 修正済み     | さらにテストを行った後、デフォルト値を`OFF`から`ON`に変更します。これは、 `ADD INDEX`と`CREATE INDEX`のアクセラレーションがデフォルトで有効になることを意味します。                                                                                                                                                                                                                                                                                                                                              |
| [<a href="/system-variables.md#tidb_mem_quota_query">`tidb_mem_quota_query`</a>](/system-variables.md#tidb_mem_quota_query)                                                                                        | 修正済み     | TiDB v6.5.0 より前のバージョンの場合、この変数はクエリのメモリクォータのしきい値を設定するために使用されます。 TiDB v6.5.0 以降のバージョンでは、DML ステートメントのメモリをより正確に制御するために、この変数を使用してセッションのメモリクォータのしきい値を設定します。                                                                                                                                                                                                                                                                                             |
| [<a href="/system-variables.md#tidb_replica_read-new-in-v40">`tidb_replica_read`</a>](/system-variables.md#tidb_replica_read-new-in-v40)                                                                           | 修正済み     | v6.5.0 以降、TiDB ノード間のロード バランシングを最適化するために、この変数が`closest-adaptive`に設定され、読み取りリクエストの推定結果が[<a href="/system-variables.md#tidb_adaptive_closest_read_threshold-new-in-v630">`tidb_adaptive_closest_read_threshold`</a>](/system-variables.md#tidb_adaptive_closest_read_threshold-new-in-v630)以上の場合、 `closest-adaptive`構成が有効になる TiDB ノードの数は制限されます。各アベイラビリティ ゾーンは、TiDB ノードが最も少ないアベイラビリティ ゾーン内の TiDB ノードの数と常に同じであり、他の TiDB ノードはリーダー レプリカから自動的に読み取られます。    |
| [<a href="/system-variables.md#tidb_server_memory_limit-new-in-v640">`tidb_server_memory_limit`</a>](/system-variables.md#tidb_server_memory_limit-new-in-v640)                                                    | 修正済み     | デフォルト値を`0`から`80%`に変更します。 TiDB グローバルメモリコントロールが GA になると、このデフォルト値の変更により、デフォルトでメモリコントロールが有効になり、TiDB インスタンスのメモリ制限がデフォルトで総メモリの 80% に設定されます。                                                                                                                                                                                                                                                                                                            |
| [<a href="/system-variables.md#default_password_lifetime-new-in-v650">`default_password_lifetime`</a>](/system-variables.md#default_password_lifetime-new-in-v650)                                                 | 新しく追加された | パスワードの自動有効期限のグローバル ポリシーを設定して、ユーザーに定期的なパスワードの変更を要求します。デフォルト値`0`は、パスワードに期限がないことを示します。                                                                                                                                                                                                                                                                                                                                                              |
| [<a href="/system-variables.md#disconnect_on_expired_password-new-in-v650">`disconnect_on_expired_password`</a>](/system-variables.md#disconnect_on_expired_password-new-in-v650)                                  | 新しく追加された | パスワードの有効期限が切れたときに TiDB がクライアント接続を切断するかどうかを示します。この変数は読み取り専用です。                                                                                                                                                                                                                                                                                                                                                                                    |
| [<a href="/system-variables.md#password_history-new-in-v650">`password_history`</a>](/system-variables.md#password_history-new-in-v650)                                                                            | 新しく追加された | この変数は、パスワードの変更回数に基づいて TiDB がパスワードの再利用を制限できるようにするパスワード再利用ポリシーを確立するために使用されます。デフォルト値`0`は、パスワード変更の回数に基づいてパスワード再利用ポリシーを無効にすることを意味します。                                                                                                                                                                                                                                                                                                                 |
| [<a href="/system-variables.md#password_reuse_interval-new-in-v650">`password_reuse_interval`</a>](/system-variables.md#password_reuse_interval-new-in-v650)                                                       | 新しく追加された | この変数は、TiDB が経過時間に基づいてパスワードの再利用を制限できるようにするパスワード再利用ポリシーを確立するために使用されます。デフォルト値`0`は、経過時間に基づいてパスワード再利用ポリシーを無効にすることを意味します。                                                                                                                                                                                                                                                                                                                              |
| [<a href="/system-variables.md#tidb_auto_build_stats_concurrency-new-in-v650">`tidb_auto_build_stats_concurrency`</a>](/system-variables.md#tidb_auto_build_stats_concurrency-new-in-v650)                         | 新しく追加された | この変数は、統計の自動更新を実行する同時実行数を設定するために使用されます。デフォルト値は`1`です。                                                                                                                                                                                                                                                                                                                                                                                              |
| [<a href="/system-variables.md#tidb_cdc_write_source-new-in-v650">`tidb_cdc_write_source`</a>](/system-variables.md#tidb_cdc_write_source-new-in-v650)                                                             | 新しく追加された | この変数が 0 以外の値に設定されている場合、このセッションで書き込まれたデータは TiCDC によって書き込まれたものとみなされます。この変数は TiCDC によってのみ変更できます。いかなる場合でも、この変数を手動で変更しないでください。                                                                                                                                                                                                                                                                                                                        |
| [<a href="/system-variables.md#tidb_index_merge_intersection_concurrency-new-in-v650">`tidb_index_merge_intersection_concurrency`</a>](/system-variables.md#tidb_index_merge_intersection_concurrency-new-in-v650) | 新しく追加された | インデックスのマージが実行する交差操作の最大同時実行数を設定します。これは、TiDB が動的プルーニング モードでパーティション化されたテーブルにアクセスする場合にのみ有効です。                                                                                                                                                                                                                                                                                                                                                        |
| [<a href="/system-variables.md#tidb_source_id-new-in-v650">`tidb_source_id`</a>](/system-variables.md#tidb_source_id-new-in-v650)                                                                                  | 新しく追加された | この変数は、 [<a href="/ticdc/ticdc-bidirectional-replication.md">双方向レプリケーション</a>](/ticdc/ticdc-bidirectional-replication.md)クラスター内でさまざまなクラスター ID を構成するために使用されます。                                                                                                                                                                                                                                                                                      |
| [<a href="/system-variables.md#tidb_sysproc_scan_concurrency-new-in-v650">`tidb_sysproc_scan_concurrency`</a>](/system-variables.md#tidb_sysproc_scan_concurrency-new-in-v650)                                     | 新しく追加された | この変数は、TiDB が内部 SQL ステートメント (統計の自動更新など) を実行するときに実行されるスキャン操作の同時実行性を設定するために使用されます。デフォルト値は`1`です。                                                                                                                                                                                                                                                                                                                                                     |
| [<a href="/system-variables.md#tidb_ttl_delete_batch_size-new-in-v650">`tidb_ttl_delete_batch_size`</a>](/system-variables.md#tidb_ttl_delete_batch_size-new-in-v650)                                              | 新しく追加された | この変数は、TTL ジョブの`DELETE`つのトランザクションで削除できる最大行数を設定するために使用されます。                                                                                                                                                                                                                                                                                                                                                                                        |
| [<a href="/system-variables.md#tidb_ttl_delete_rate_limit-new-in-v650">`tidb_ttl_delete_rate_limit`</a>](/system-variables.md#tidb_ttl_delete_rate_limit-new-in-v650)                                              | 新しく追加された | この変数は、TTL ジョブの単一ノードで 1 秒あたりに許可される`DELETE`ステートメントの最大数を制限するために使用されます。この変数が`0`に設定されている場合、制限は適用されません。                                                                                                                                                                                                                                                                                                                                                |
| [<a href="/system-variables.md#tidb_ttl_delete_worker_count-new-in-v650">`tidb_ttl_delete_worker_count`</a>](/system-variables.md#tidb_ttl_delete_worker_count-new-in-v650)                                        | 新しく追加された | この変数は、各 TiDB ノードでの TTL ジョブの最大同時実行数を設定するために使用されます。                                                                                                                                                                                                                                                                                                                                                                                                |
| [<a href="/system-variables.md#tidb_ttl_job_enable-new-in-v650">`tidb_ttl_job_enable`</a>](/system-variables.md#tidb_ttl_job_enable-new-in-v650)                                                                   | 新しく追加された | この変数は、TTL ジョブを有効にするかどうかを制御するために使用されます。これを`OFF`に設定すると、TTL 属性を持つすべてのテーブルが期限切れデータのクリーンアップを自動的に停止します。                                                                                                                                                                                                                                                                                                                                                |
| `tidb_ttl_job_run_interval`                                                                                                                                                                                        | 新しく追加された | この変数は、バックグラウンドでの TTL ジョブのスケジュール間隔を制御するために使用されます。たとえば、現在の値が`1h0m0s`に設定されている場合、TTL 属性を持つ各テーブルは、1 時間ごとに期限切れのデータをクリーンアップします。                                                                                                                                                                                                                                                                                                                         |
| [<a href="/system-variables.md#tidb_ttl_job_schedule_window_start_time-new-in-v650">`tidb_ttl_job_schedule_window_start_time`</a>](/system-variables.md#tidb_ttl_job_schedule_window_start_time-new-in-v650)       | 新しく追加された | この変数は、バックグラウンドでの TTL ジョブのスケジュール ウィンドウの開始時間を制御するために使用されます。この変数の値を変更する場合は、ウィンドウが小さいと期限切れデータのクリーンアップが失敗する可能性があることに注意してください。                                                                                                                                                                                                                                                                                                                         |
| [<a href="/system-variables.md#tidb_ttl_job_schedule_window_end_time-new-in-v650">`tidb_ttl_job_schedule_window_end_time`</a>](/system-variables.md#tidb_ttl_job_schedule_window_end_time-new-in-v650)             | 新しく追加された | この変数は、バックグラウンドでの TTL ジョブのスケジュール ウィンドウの終了時刻を制御するために使用されます。この変数の値を変更する場合は、ウィンドウが小さいと期限切れデータのクリーンアップが失敗する可能性があることに注意してください。                                                                                                                                                                                                                                                                                                                         |
| [<a href="/system-variables.md#tidb_ttl_scan_batch_size-new-in-v650">`tidb_ttl_scan_batch_size`</a>](/system-variables.md#tidb_ttl_scan_batch_size-new-in-v650)                                                    | 新しく追加された | この変数は、TTL ジョブの期限切れデータのスキャンに使用される各`SELECT`ステートメントの`LIMIT`値を設定するために使用されます。                                                                                                                                                                                                                                                                                                                                                                         |
| [<a href="/system-variables.md#tidb_ttl_scan_worker_count-new-in-v650">`tidb_ttl_scan_worker_count`</a>](/system-variables.md#tidb_ttl_scan_worker_count-new-in-v650)                                              | 新しく追加された | この変数は、各 TiDB ノードでの TTL スキャン ジョブの最大同時実行数を設定するために使用されます。                                                                                                                                                                                                                                                                                                                                                                                           |
| [<a href="/system-variables.md#validate_passwordcheck_user_name-new-in-v650">`validate_password.check_user_name`</a>](/system-variables.md#validate_passwordcheck_user_name-new-in-v650)                           | 新しく追加された | パスワード複雑度チェックのチェック項目です。パスワードがユーザー名と一致するかどうかをチェックします。この変数は、 [<a href="/system-variables.md#validate_passwordenable-new-in-v650">`validate_password.enable`</a>](/system-variables.md#validate_passwordenable-new-in-v650)が有効な場合にのみ有効になります。デフォルト値は`ON`です。                                                                                                                                                                                           |
| [<a href="/system-variables.md#validate_passworddictionary-new-in-v650">`validate_password.dictionary`</a>](/system-variables.md#validate_passworddictionary-new-in-v650)                                          | 新しく追加された | パスワード複雑度チェックのチェック項目です。パスワードが辞書内の単語と一致するかどうかをチェックします。この変数は、 [<a href="/system-variables.md#validate_passwordenable-new-in-v650">`validate_password.enable`</a>](/system-variables.md#validate_passwordenable-new-in-v650)が有効で、 [<a href="/system-variables.md#validate_passwordpolicy-new-in-v650">`validate_password.policy`</a>](/system-variables.md#validate_passwordpolicy-new-in-v650)が`2` (STRONG) に設定されている場合にのみ有効です。デフォルト値は`""`です。        |
| [<a href="/system-variables.md#validate_passwordenable-new-in-v650">`validate_password.enable`</a>](/system-variables.md#validate_passwordenable-new-in-v650)                                                      | 新しく追加された | この変数は、パスワードの複雑さのチェックを実行するかどうかを制御します。この変数が`ON`に設定されている場合、TiDB はパスワードの設定時にパスワードの複雑さのチェックを実行します。デフォルト値は`OFF`です。                                                                                                                                                                                                                                                                                                                                     |
| [<a href="/system-variables.md#validate_passwordlength-new-in-v650">`validate_password.length`</a>](/system-variables.md#validate_passwordlength-new-in-v650)                                                      | 新しく追加された | パスワード複雑度チェックのチェック項目です。パスワードの長さが十分であるかどうかをチェックします。デフォルトでは、パスワードの最小長は`8`です。この変数は、 [<a href="/system-variables.md#validate_passwordenable-new-in-v650">`validate_password.enable`</a>](/system-variables.md#validate_passwordenable-new-in-v650)が有効な場合にのみ有効になります。                                                                                                                                                                                   |
| [<a href="/system-variables.md#validate_passwordmixed_case_count-new-in-v650">`validate_password.mixed_case_count`</a>](/system-variables.md#validate_passwordmixed_case_count-new-in-v650)                        | 新しく追加された | パスワード複雑度チェックのチェック項目です。パスワードに十分な大文字と小文字が含まれているかどうかをチェックします。この変数は、 [<a href="/system-variables.md#validate_passwordenable-new-in-v650">`validate_password.enable`</a>](/system-variables.md#validate_passwordenable-new-in-v650)が有効で、 [<a href="/system-variables.md#validate_passwordpolicy-new-in-v650">`validate_password.policy`</a>](/system-variables.md#validate_passwordpolicy-new-in-v650)が`1` (MEDIUM) 以上に設定されている場合にのみ有効です。デフォルト値は`1`です。 |
| [<a href="/system-variables.md#validate_passwordnumber_count-new-in-v650">`validate_password.number_count`</a>](/system-variables.md#validate_passwordnumber_count-new-in-v650)                                    | 新しく追加された | パスワード複雑度チェックのチェック項目です。パスワードに十分な数字が含まれているかどうかをチェックします。この変数は、 [<a href="/system-variables.md#password_reuse_interval-new-in-v650">`validate_password.enable`</a>](/system-variables.md#password_reuse_interval-new-in-v650)が有効で、 [<a href="/system-variables.md#validate_passwordpolicy-new-in-v650">`validate_password.policy`</a>](/system-variables.md#validate_passwordpolicy-new-in-v650)が`1` (MEDIUM) 以上に設定されている場合にのみ有効です。デフォルト値は`1`です。      |
| [<a href="/system-variables.md#validate_passwordpolicy-new-in-v650">`validate_password.policy`</a>](/system-variables.md#validate_passwordpolicy-new-in-v650)                                                      | 新しく追加された | この変数は、パスワードの複雑さチェックのポリシーを制御します。値は`0` 、 `1` 、または`2` (LOW、MEDIUM、または STRONG に対応) です。この変数は、 [<a href="/system-variables.md#password_reuse_interval-new-in-v650">`validate_password.enable`</a>](/system-variables.md#password_reuse_interval-new-in-v650)が有効な場合にのみ有効になります。デフォルト値は`1`です。                                                                                                                                                             |
| [<a href="/system-variables.md#validate_passwordspecial_char_count-new-in-v650">`validate_password.special_char_count`</a>](/system-variables.md#validate_passwordspecial_char_count-new-in-v650)                  | 新しく追加された | パスワード複雑度チェックのチェック項目です。パスワードに十分な特殊文字が含まれているかどうかをチェックします。この変数は、 [<a href="/system-variables.md#password_reuse_interval-new-in-v650">`validate_password.enable`</a>](/system-variables.md#password_reuse_interval-new-in-v650)が有効で、 [<a href="/system-variables.md#validate_passwordpolicy-new-in-v650">`validate_password.policy`</a>](/system-variables.md#validate_passwordpolicy-new-in-v650)が`1` (MEDIUM) 以上に設定されている場合にのみ有効です。デフォルト値は`1`です。    |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                                                                                                                 | 種類の変更    | 説明                                                                                                                                                                                                                         |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | [<a href="/tidb-configuration-file.md#server-memory-quota-new-in-v409">`server-memory-quota`</a>](/tidb-configuration-file.md#server-memory-quota-new-in-v409)                                  | 廃止されました  | v6.5.0 以降、この構成項目は非推奨になりました。代わりに、システム変数[<a href="/system-variables.md#tidb_server_memory_limit-new-in-v640">`tidb_server_memory_limit`</a>](/system-variables.md#tidb_server_memory_limit-new-in-v640)を使用してメモリをグローバルに管理します。 |
| TiDB           | [<a href="/tidb-configuration-file.md#disconnect-on-expired-password-new-in-v650">`disconnect-on-expired-password`</a>](/tidb-configuration-file.md#disconnect-on-expired-password-new-in-v650) | 新しく追加された | パスワードの有効期限が切れたときに、TiDB がクライアント接続を切断するかどうかを決定します。デフォルト値は`true`で、パスワードの有効期限が切れるとクライアント接続が切断されることを意味します。                                                                                                                      |
| TiKV           | `raw-min-ts-outlier-threshold`                                                                                                                                                                  | 削除されました  | この構成項目は v6.4.0 で非推奨となり、v6.5.0 で削除されました。                                                                                                                                                                                    |
| TiKV           | [<a href="/tikv-configuration-file.md#min-ts-interval">`cdc.min-ts-interval`</a>](/tikv-configuration-file.md#min-ts-interval)                                                                  | 修正済み     | CDCレイテンシーを短縮するために、デフォルト値が`1s`から`200ms`に変更されました。                                                                                                                                                                            |
| TiKV           | [<a href="/tikv-configuration-file.md#memory-use-ratio-new-in-v650">`memory-use-ratio`</a>](/tikv-configuration-file.md#memory-use-ratio-new-in-v650)                                           | 新しく追加された | PITR ログ リカバリでの合計システムメモリに対する利用可能なメモリの比率を示します。                                                                                                                                                                               |
| TiCDC          | [<a href="/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters">`sink.terminator`</a>](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)                  | 新しく追加された | 2 つのデータ変更イベントを区切るために使用される行ターミネータを示します。デフォルトでは値は空であり、 `\r\n`が使用されることを意味します。                                                                                                                                                 |
| TiCDC          | [<a href="/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters">`sink.date-separator`</a>](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)              | 新しく追加された | ファイルディレクトリの日付区切り文字のタイプを示します。値のオプションは`none` 、 `year` 、 `month` 、および`day`です。 `none`はデフォルト値で、日付が区切られていないことを意味します。                                                                                                             |
| TiCDC          | [<a href="/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters">`sink.enable-partition-separator`</a>](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)  | 新しく追加された | パーティションを区切り文字列として使用するかどうかを指定します。デフォルト値は`false`で、テーブル内のパーティションが別のディレクトリに格納されないことを意味します。                                                                                                                                     |
| TiCDC          | [<a href="/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters">`sink.csv.delimiter`</a>](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)               | 新しく追加された | フィールド間の区切り文字を示します。値は ASCII 文字である必要があり、デフォルトは`,`です。                                                                                                                                                                         |
| TiCDC          | [<a href="/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters">`sink.csv.quote`</a>](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)                   | 新しく追加された | フィールドを囲む引用符。デフォルト値は`"`です。値が空の場合、引用符は使用されません。                                                                                                                                                                               |
| TiCDC          | [<a href="/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters">`sink.csv.null`</a>](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)                    | 新しく追加された | CSV列がnullの場合に表示される文字を指定します。デフォルト値は`\N`です。                                                                                                                                                                                  |
| TiCDC          | [<a href="/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters">`sink.csv.include-commit-ts`</a>](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)       | 新しく追加された | CSV 行に commit-ts を含めるかどうかを指定します。デフォルト値は`false`です。                                                                                                                                                                          |

### その他 {#others}

-   v6.5.0 以降、 `mysql.user`テーブルには`Password_reuse_history`と`Password_reuse_time`という 2 つの新しい列が追加されます。
-   v6.5.0 以降、 [<a href="/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630">インデックス加速度</a>](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)機能はデフォルトで有効になります。この機能は[<a href="/sql-statements/sql-statement-alter-table.md">単一の`ALTER TABLE`ステートメントで複数の列またはインデックスを変更する</a>](/sql-statements/sql-statement-alter-table.md)と完全な互換性はありません。インデックス アクセラレーションを使用して一意のインデックスを追加する場合は、同じステートメント内の他の列やインデックスを変更しないようにする必要があります。この機能は[<a href="/br/br-pitr-guide.md">PITR (ポイントインタイムリカバリ)</a>](/br/br-pitr-guide.md)とも互換性がありません。インデックス アクセラレーション機能を使用する場合は、PITR バックアップ タスクがバックグラウンドで実行されていないことを確認する必要があります。そうしないと、予期しない結果が発生する可能性があります。詳細については、 [<a href="/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630">ドキュメンテーション</a>](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)を参照してください。

## 廃止された機能 {#deprecated-feature}

v6.5.0 以降、v4.0.7 で導入された`AMEND TRANSACTION`メカニズムは非推奨となり、 [<a href="/metadata-lock.md">メタデータロック</a>](/metadata-lock.md)に置き換えられます。

## 改善点 {#improvements}

-   TiDB

    -   `BIT`と`CHAR`列については、 `INFORMATION_SCHEMA.COLUMNS`の結果を MySQL [<a href="https://github.com/pingcap/tidb/issues/25472">#25472</a>](https://github.com/pingcap/tidb/issues/25472) @ [<a href="https://github.com/hawkingrei">ホーキングレイ</a>](https://github.com/hawkingrei)と一致させます。
    -   TiFlash MPP モードのTiFlashノードの TiDB プローブ メカニズムを最適化し、ノードが異常な場合のパフォーマンスへの影響を軽減します[<a href="https://github.com/pingcap/tidb/issues/39686">#39686</a>](https://github.com/pingcap/tidb/issues/39686) @ [<a href="https://github.com/hackersean">ハッカー派</a>](https://github.com/hackersean)

-   TiKV

    -   ディスクスペースの枯渇を避けるために、スペースが不十分な場合はRaft Engineへの書き込みを停止します[<a href="https://github.com/tikv/tikv/issues/13642">#13642</a>](https://github.com/tikv/tikv/issues/13642) @ [<a href="https://github.com/jiayang-zheng">嘉陽鄭</a>](https://github.com/jiayang-zheng)
    -   `json_valid`関数の TiKV [<a href="https://github.com/tikv/tikv/issues/13571">#13571</a>](https://github.com/tikv/tikv/issues/13571) @ [<a href="https://github.com/lizhenhuan">立振環</a>](https://github.com/lizhenhuan)へのプッシュダウンをサポート
    -   1 回のバックアップ リクエストで複数範囲のデータのバックアップをサポート[<a href="https://github.com/tikv/tikv/issues/13701">#13701</a>](https://github.com/tikv/tikv/issues/13701) @ [<a href="https://github.com/Leavrth">レヴルス</a>](https://github.com/Leavrth)
    -   rusoto ライブラリ[<a href="https://github.com/tikv/tikv/issues/13751">#13751</a>](https://github.com/tikv/tikv/issues/13751) @ [<a href="https://github.com/3pointer">3ポインター</a>](https://github.com/3pointer)を更新することで、AWS のアジアパシフィック リージョン (ap-southeast-3) へのデータのバックアップをサポートします。
    -   悲観的トランザクション競合を削減[<a href="https://github.com/tikv/tikv/issues/13298">#13298</a>](https://github.com/tikv/tikv/issues/13298) @ [<a href="https://github.com/MyonKeminta">ミョンケミンタ</a>](https://github.com/MyonKeminta)
    -   外部storageオブジェクト[<a href="https://github.com/tikv/tikv/issues/13798">#13798</a>](https://github.com/tikv/tikv/issues/13798) @ [<a href="https://github.com/YuJuncen">ユジュンセン</a>](https://github.com/YuJuncen)をキャッシュすることで、リカバリ パフォーマンスを向上させます。
    -   専用スレッドで CheckLeader を実行して、TiCDC レプリケーションのレイテンシー[<a href="https://github.com/tikv/tikv/issues/13774">#13774</a>](https://github.com/tikv/tikv/issues/13774) @ [<a href="https://github.com/overvenus">オーバーヴィーナス</a>](https://github.com/overvenus)を削減します。
    -   チェックポイント[<a href="https://github.com/tikv/tikv/issues/13824">#13824</a>](https://github.com/tikv/tikv/issues/13824) @ [<a href="https://github.com/YuJuncen">ユジュンセン</a>](https://github.com/YuJuncen)のプル モデルをサポート
    -   送信側でのスピンの問題を回避するには、クロスビームチャネル[<a href="https://github.com/tikv/tikv/issues/13815">#13815</a>](https://github.com/tikv/tikv/issues/13815) @ [<a href="https://github.com/sticnarf">スティックナーフ</a>](https://github.com/sticnarf)を更新します。
    -   TiKV [<a href="https://github.com/tikv/tikv/issues/13849">#13849</a>](https://github.com/tikv/tikv/issues/13849) @ [<a href="https://github.com/cfzjywxk">cfzjywxk</a>](https://github.com/cfzjywxk)でのコプロセッサータスク処理をサポート
    -   TiKV にリージョン[<a href="https://github.com/tikv/tikv/issues/13648">#13648</a>](https://github.com/tikv/tikv/issues/13648) @ [<a href="https://github.com/LykxSassinator">リククスサシネーター</a>](https://github.com/LykxSassinator)をウェイクアップするように通知することで、障害回復時の待ち時間を短縮します。
    -   コード最適化[<a href="https://github.com/tikv/tikv/issues/13827">#13827</a>](https://github.com/tikv/tikv/issues/13827) @ [<a href="https://github.com/BusyJay">ビジージェイ</a>](https://github.com/BusyJay)により、要求されたメモリ使用量のサイズを削減します。
    -   Raft拡張機能を導入してコードの拡張性を向上させます[<a href="https://github.com/tikv/tikv/issues/13827">#13827</a>](https://github.com/tikv/tikv/issues/13827) @ [<a href="https://github.com/BusyJay">ビジージェイ</a>](https://github.com/BusyJay)
    -   tikv-ctl を使用した特定のキー範囲に含まれるリージョンのクエリをサポート[<a href="https://github.com/tikv/tikv/issues/13760">#13760</a>](https://github.com/tikv/tikv/issues/13760) [<a href="https://github.com/HuSharp">@husharp</a>](https://github.com/HuSharp)
    -   更新されていないが継続的にロックされている行の読み取りおよび書き込みパフォーマンスを向上させます[<a href="https://github.com/tikv/tikv/issues/13694">#13694</a>](https://github.com/tikv/tikv/issues/13694) [<a href="https://github.com/sticnarf">@sicnarf</a>](https://github.com/sticnarf)

-   PD

    -   ロックの粒度を最適化してロックの競合を軽減し、高い同時実行性[<a href="https://github.com/tikv/pd/issues/5586">#5586</a>](https://github.com/tikv/pd/issues/5586) @ [<a href="https://github.com/rleungx">ルルンクス</a>](https://github.com/rleungx)でのハートビートの処理能力を向上させます。
    -   大規模クラスターのスケジューラーのパフォーマンスを最適化し、スケジューリング ポリシー[<a href="https://github.com/tikv/pd/issues/5473">#5473</a>](https://github.com/tikv/pd/issues/5473) @ [<a href="https://github.com/bufferflies">バッファフライ</a>](https://github.com/bufferflies)の本番を加速します。
    -   リージョン[<a href="https://github.com/tikv/pd/issues/5606">#5606</a>](https://github.com/tikv/pd/issues/5606) @ [<a href="https://github.com/rleungx">ルルンクス</a>](https://github.com/rleungx)のロード速度を向上させます。
    -   リージョンハートビート[<a href="https://github.com/tikv/pd/issues/5648">#5648</a>](https://github.com/tikv/pd/issues/5648) @ [<a href="https://github.com/rleungx">ルルンクス</a>](https://github.com/rleungx)の処理を最適化することで、不必要なオーバーヘッドを削減します。
    -   墓石ストア[<a href="https://github.com/tikv/pd/issues/5348">#5348</a>](https://github.com/tikv/pd/issues/5348) @ [<a href="https://github.com/nolouch">ノールーシュ</a>](https://github.com/nolouch)を自動的にガベージコレクションする機能を追加

-   TiFlash

    -   SQL 側でバッチ処理がないシナリオでの書き込みパフォーマンスが向上します[<a href="https://github.com/pingcap/tiflash/issues/6404">#6404</a>](https://github.com/pingcap/tiflash/issues/6404) @ [<a href="https://github.com/lidezhu">リデズ</a>](https://github.com/lidezhu)
    -   `explain analyze`出力[<a href="https://github.com/pingcap/tiflash/issues/5926">#5926</a>](https://github.com/pingcap/tiflash/issues/5926) @ [<a href="https://github.com/hongyunyan">ホンユニャン</a>](https://github.com/hongyunyan)に TableFullScan の詳細を追加します。

-   ツール

    -   TiDB ダッシュボード

        -   スロー クエリ ページに 3 つの新しいフィールドを追加します:「Is Prepared?」、「Is Plan from Cache?」、「Is Plan from Binding?」 [<a href="https://github.com/pingcap/tidb-dashboard/issues/1451">#1451</a>](https://github.com/pingcap/tidb-dashboard/issues/1451) @ [<a href="https://github.com/shhdgit">シュギット</a>](https://github.com/shhdgit)

    -   バックアップと復元 (BR)

        -   バックアップ ログ データ[<a href="https://github.com/pingcap/tidb/issues/38869">#38869</a>](https://github.com/pingcap/tidb/issues/38869) @ [<a href="https://github.com/Leavrth">レヴルス</a>](https://github.com/Leavrth)のクリーニング プロセス中のBRメモリ使用量を最適化します。
        -   復元プロセス[<a href="https://github.com/pingcap/tidb/issues/36910">#36910</a>](https://github.com/pingcap/tidb/issues/36910) @ [<a href="https://github.com/MoCuishle28">モクイシュル28</a>](https://github.com/MoCuishle28)中に PD リーダー スイッチによって引き起こされる復元失敗の問題を修正します。
        -   ログ バックアップ[<a href="https://github.com/tikv/tikv/issues/13867">#13867</a>](https://github.com/tikv/tikv/issues/13867) @ [<a href="https://github.com/YuJuncen">ユジュンセン</a>](https://github.com/YuJuncen)で OpenSSL プロトコルを使用することで、TLS 互換性を向上させます。

    -   TiCDC

        -   Kafka プロトコル エンコーダのパフォーマンスを向上させる[<a href="https://github.com/pingcap/tiflow/issues/7540">#7540</a>](https://github.com/pingcap/tiflow/issues/7540) [<a href="https://github.com/pingcap/tiflow/issues/7532">#7532</a>](https://github.com/pingcap/tiflow/issues/7532) [<a href="https://github.com/pingcap/tiflow/issues/7543">#7543</a>](https://github.com/pingcap/tiflow/issues/7543) @ [<a href="https://github.com/3AceShowHand">3エースショーハンド</a>](https://github.com/3AceShowHand) @ [<a href="https://github.com/sdojjy">スドジ</a>](https://github.com/sdojjy)

    -   TiDB データ移行 (DM)

        -   ブロック リスト[<a href="https://github.com/pingcap/tiflow/pull/7622">#7622</a>](https://github.com/pingcap/tiflow/pull/7622) @ [<a href="https://github.com/GMHDBJD">GMHDBJD</a>](https://github.com/GMHDBJD)内のテーブルのデータを解析しないことにより、DM のデータ レプリケーション パフォーマンスが向上します。
        -   非同期書き込みと一括書き込み[<a href="https://github.com/pingcap/tiflow/pull/7580">#7580</a>](https://github.com/pingcap/tiflow/pull/7580) @ [<a href="https://github.com/GMHDBJD">GMHDBJD</a>](https://github.com/GMHDBJD)を使用して、DM リレーの書き込み効率を向上させます
        -   DM 事前チェック[<a href="https://github.com/pingcap/tiflow/issues/7621">#7621</a>](https://github.com/pingcap/tiflow/issues/7621) @ [<a href="https://github.com/buchuitoudegou">ブチュイトデゴウ</a>](https://github.com/buchuitoudegou)のエラー メッセージを最適化します。
        -   古い MySQL バージョン[<a href="https://github.com/pingcap/tiflow/issues/5017">#5017</a>](https://github.com/pingcap/tiflow/issues/5017) @ [<a href="https://github.com/lyzx2001">lyzx2001</a>](https://github.com/lyzx2001)に対する`SHOW SLAVE HOSTS`の互換性を向上

## バグの修正 {#bug-fixes}

-   TiDB

    -   場合によって発生するチャンク再利用機能のメモリチャンクの誤用の問題を修正[<a href="https://github.com/pingcap/tidb/issues/38917">#38917</a>](https://github.com/pingcap/tidb/issues/38917) @ [<a href="https://github.com/keeplearning20221">キープラーニング20221</a>](https://github.com/keeplearning20221)
    -   `tidb_constraint_check_in_place_pessimistic`の内部セッションがグローバル設定[<a href="https://github.com/pingcap/tidb/issues/38766">#38766</a>](https://github.com/pingcap/tidb/issues/38766) @ [<a href="https://github.com/ekexium">エキシウム</a>](https://github.com/ekexium)の影響を受ける可能性がある問題を修正
    -   `AUTO_INCREMENT`列が`CHECK`制約[<a href="https://github.com/pingcap/tidb/issues/38894">#38894</a>](https://github.com/pingcap/tidb/issues/38894) @ [<a href="https://github.com/YangKeao">ヤンケオ</a>](https://github.com/YangKeao)で機能しない問題を修正
    -   `INSERT IGNORE INTO`を使用して`STRING`タイプのデータを`SMALLINT`タイプの自動インクリメント列に挿入すると、エラー[<a href="https://github.com/pingcap/tidb/issues/38483">#38483</a>](https://github.com/pingcap/tidb/issues/38483) @ [<a href="https://github.com/hawkingrei">ホーキングレイ</a>](https://github.com/hawkingrei)が発生する問題を修正します。
    -   パーティションテーブル[<a href="https://github.com/pingcap/tidb/issues/38932">#38932</a>](https://github.com/pingcap/tidb/issues/38932) @ [<a href="https://github.com/mjonss">むじょん</a>](https://github.com/mjonss)のパーティション列の名前変更操作でNULLポインタエラーが発生する問題を修正
    -   パーティションテーブルのパーティション列を変更すると DDL がハングする[<a href="https://github.com/pingcap/tidb/issues/38530">#38530</a>](https://github.com/pingcap/tidb/issues/38530) @ [<a href="https://github.com/mjonss">むじょん</a>](https://github.com/mjonss)という問題を修正します。
    -   v4.0.16 から v6.4.0 [<a href="https://github.com/pingcap/tidb/issues/38980">#38980</a>](https://github.com/pingcap/tidb/issues/38980) @ [<a href="https://github.com/tangenta">タンジェンタ</a>](https://github.com/tangenta)にアップグレードした後に`ADMIN SHOW JOB`操作がパニックになる問題を修正
    -   `tidb_decode_key`関数がパーティション テーブル[<a href="https://github.com/pingcap/tidb/issues/39304">#39304</a>](https://github.com/pingcap/tidb/issues/39304) @ [<a href="https://github.com/Defined2014">定義2014</a>](https://github.com/Defined2014)のエンコーディングを正しく解析できない問題を修正します。
    -   ログ ローテーション中に gRPC エラー ログが正しいログ ファイルにリダイレクトされない問題を修正します[<a href="https://github.com/pingcap/tidb/issues/38941">#38941</a>](https://github.com/pingcap/tidb/issues/38941) @ [<a href="https://github.com/xhebox">ゼボックス</a>](https://github.com/xhebox)
    -   TiKV が読み取りエンジン[<a href="https://github.com/pingcap/tidb/issues/39344">#39344</a>](https://github.com/pingcap/tidb/issues/39344) @ [<a href="https://github.com/Yisaer">イーサール</a>](https://github.com/Yisaer)として構成されていない場合、TiDB が`BEGIN; SELECT... FOR UPDATE;`ポイント クエリに対して予期しない実行プランを生成する問題を修正します。
    -   誤って`StreamAgg` TiFlashに押し込むと、間違った結果[<a href="https://github.com/pingcap/tidb/issues/39266">#39266</a>](https://github.com/pingcap/tidb/issues/39266) @ [<a href="https://github.com/fixdb">修正データベース</a>](https://github.com/fixdb)が発生する問題を修正

-   TiKV

    -   Raft Engine ctl [<a href="https://github.com/tikv/tikv/issues/11119">#11119</a>](https://github.com/tikv/tikv/issues/11119) @ [<a href="https://github.com/tabokie">タボキー</a>](https://github.com/tabokie)のエラーを修正
    -   tikv-ctl [<a href="https://github.com/tikv/tikv/issues/13515">#13515</a>](https://github.com/tikv/tikv/issues/13515) @ [<a href="https://github.com/guoxiangCN">国祥CN</a>](https://github.com/guoxiangCN)で`compact raft`コマンドを実行するときの`Get raft db is not allowed`エラーを修正
    -   TLS が有効になっている場合にログ バックアップが機能しない問題を修正[<a href="https://github.com/tikv/tikv/issues/13867">#13867</a>](https://github.com/tikv/tikv/issues/13867) @ [<a href="https://github.com/YuJuncen">ユジュンセン</a>](https://github.com/YuJuncen)
    -   ジオメトリ フィールド タイプ[<a href="https://github.com/tikv/tikv/issues/13651">#13651</a>](https://github.com/tikv/tikv/issues/13651) @ [<a href="https://github.com/dveeden">ドヴィーデン</a>](https://github.com/dveeden)のサポートの問題を修正
    -   新しい照合順序が有効になっていない場合、 `LIKE`演算子の`_`非 ASCII 文字と一致できない問題を修正[<a href="https://github.com/tikv/tikv/issues/13769">#13769</a>](https://github.com/tikv/tikv/issues/13769) @ [<a href="https://github.com/YangKeao">ヤンケオ</a>](https://github.com/YangKeao)
    -   `reset-to-version`コマンド[<a href="https://github.com/tikv/tikv/issues/13829">#13829</a>](https://github.com/tikv/tikv/issues/13829) @ [<a href="https://github.com/tabokie">タボキー</a>](https://github.com/tabokie)を実行すると tikv-ctl が予期せず終了する問題を修正

-   PD

    -   [<a href="https://github.com/tikv/pd/issues/5701">#5701</a>](https://github.com/tikv/pd/issues/5701) @ [<a href="https://github.com/HunDunDM">フンドゥンDM</a>](https://github.com/HunDunDM)を変更しないと`balance-hot-region-scheduler`設定が保持されない問題を修正
    -   アップグレード プロセス中に`rank-formula-version`がアップグレード前の構成を保持しない問題を修正します[<a href="https://github.com/tikv/pd/issues/5698">#5698</a>](https://github.com/tikv/pd/issues/5698) @ [<a href="https://github.com/HunDunDM">フンドゥンDM</a>](https://github.com/HunDunDM)

-   TiFlash

    -   TiFlash [<a href="https://github.com/pingcap/tiflash/issues/6159">#6159</a>](https://github.com/pingcap/tiflash/issues/6159) @ [<a href="https://github.com/lidezhu">リデズ</a>](https://github.com/lidezhu)の再起動後にデルタレイヤーのカラムファイルが圧縮できない問題を修正
    -   TiFlashファイルオープン OPS が高すぎる問題を修正[<a href="https://github.com/pingcap/tiflash/issues/6345">#6345</a>](https://github.com/pingcap/tiflash/issues/6345) @ [<a href="https://github.com/JaySon-Huang">ジェイ・ソン・ファン</a>](https://github.com/JaySon-Huang)

-   ツール

    -   バックアップと復元 (BR)

        -   BRがログバックアップデータを削除すると、削除すべきでないデータを誤って削除してしまう問題を修正[<a href="https://github.com/pingcap/tidb/issues/38939">#38939</a>](https://github.com/pingcap/tidb/issues/38939) @ [<a href="https://github.com/Leavrth">レヴルス</a>](https://github.com/Leavrth)
        -   データベースまたはテーブル[<a href="https://github.com/pingcap/tidb/issues/39150">#39150</a>](https://github.com/pingcap/tidb/issues/39150) @ [<a href="https://github.com/MoCuishle28">モクイシュル28</a>](https://github.com/MoCuishle28)の照合順序に古いフレームワークを使用すると、復元タスクが失敗する問題を修正します。
        -   Alibaba Cloud および Huawei Cloud が Amazon S3storage[<a href="https://github.com/pingcap/tidb/issues/39545">#39545</a>](https://github.com/pingcap/tidb/issues/39545) @ [<a href="https://github.com/3pointer">3ポインター</a>](https://github.com/3pointer)と完全な互換性がないためにバックアップが失敗する問題を修正

    -   TiCDC

        -   PD リーダーが[<a href="https://github.com/pingcap/tiflow/issues/7470">#7470</a>](https://github.com/pingcap/tiflow/issues/7470) @ [<a href="https://github.com/zeminzhou">沢民州</a>](https://github.com/zeminzhou)でクラッシュすると TiCDC がスタックする問題を修正
        -   最初に DDL ステートメントを実行し、次に変更フィード[<a href="https://github.com/pingcap/tiflow/issues/7682">#7682</a>](https://github.com/pingcap/tiflow/issues/7682) @ [<a href="https://github.com/asddongmen">東門</a>](https://github.com/asddongmen)を一時停止して再開するシナリオで発生したデータ損失を修正しました。
        -   TiFlash [<a href="https://github.com/pingcap/tiflow/issues/7744">#7744</a>](https://github.com/pingcap/tiflow/issues/7744) @ [<a href="https://github.com/overvenus">オーバーヴィーナス</a>](https://github.com/overvenus)の新しいバージョンがある場合に TiCDC が誤ってエラーを報告する問題を修正
        -   ダウンストリーム ネットワークが利用できない場合にシンクコンポーネントがスタックする問題を修正[<a href="https://github.com/pingcap/tiflow/issues/7706">#7706</a>](https://github.com/pingcap/tiflow/issues/7706) @ [<a href="https://github.com/hicqu">ひっくり返る</a>](https://github.com/hicqu)
        -   ユーザーがレプリケーション タスクをすぐに削除し、同じタスク名[<a href="https://github.com/pingcap/tiflow/issues/7657">#7657</a>](https://github.com/pingcap/tiflow/issues/7657) @ [<a href="https://github.com/overvenus">オーバーヴィーナス</a>](https://github.com/overvenus)で別のタスクを作成するとデータが失われる問題を修正します。

    -   TiDB データ移行 (DM)

        -   アップストリーム データベースで GTID モードが有効になっているがデータがない場合、 `task-mode:all`タスクを開始できない問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/7037">#7037</a>](https://github.com/pingcap/tiflow/issues/7037) @ [<a href="https://github.com/liumengya94">リウメンギャ94</a>](https://github.com/liumengya94)
        -   既存のワーカーが終了する前に新しい DM ワーカーがスケジュールされている場合、データが複数回レプリケートされる問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/7658">#7658</a>](https://github.com/pingcap/tiflow/issues/7658) @ [<a href="https://github.com/GMHDBJD">GMHDBJD</a>](https://github.com/GMHDBJD)
        -   アップストリーム データベースが正規表現を使用して権限[<a href="https://github.com/pingcap/tiflow/issues/7645">#7645</a>](https://github.com/pingcap/tiflow/issues/7645) @ [<a href="https://github.com/lance6716">ランス6716</a>](https://github.com/lance6716)を付与する場合、DM 事前チェックが通過しない問題を修正します。

    -   TiDB Lightning

        -   TiDB Lightning が巨大なソース データ ファイル[<a href="https://github.com/pingcap/tidb/issues/39331">#39331</a>](https://github.com/pingcap/tidb/issues/39331) @ [<a href="https://github.com/dsdashun">dsダシュン</a>](https://github.com/dsdashun)をインポートするときのメモリリークの問題を修正
        -   データを並行してインポートするときにTiDB Lightning が競合を正しく検出できない問題を修正[<a href="https://github.com/pingcap/tidb/issues/39476">#39476</a>](https://github.com/pingcap/tidb/issues/39476) @ [<a href="https://github.com/dsdashun">dsダシュン</a>](https://github.com/dsdashun)

## 貢献者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   [<a href="https://github.com/e1ijah1">e1ijah1</a>](https://github.com/e1ijah1)
-   [<a href="https://github.com/guoxiangCN">国祥CN</a>](https://github.com/guoxiangCN) (初投稿者)
-   [<a href="https://github.com/jiayang-zheng">嘉陽鄭</a>](https://github.com/jiayang-zheng)
-   [<a href="https://github.com/jiyfhust">ジフフスト</a>](https://github.com/jiyfhust)
-   [<a href="https://github.com/mikechengwei">マイクチェンウェイ</a>](https://github.com/mikechengwei)
-   [<a href="https://github.com/pingandb">ピンアンドブ</a>](https://github.com/pingandb)
-   [<a href="https://github.com/sashashura">サシャシュラ</a>](https://github.com/sashashura)
-   [<a href="https://github.com/sourcelliu">ソーセリュー</a>](https://github.com/sourcelliu)
-   [<a href="https://github.com/wxbty">wxbty</a>](https://github.com/wxbty)
