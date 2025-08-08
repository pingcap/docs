---
title: TiDB 6.5.0 Release Notes
summary: TiDB 6.5.0 の新機能、互換性の変更、改善点、バグ修正について説明します。
---

# TiDB 6.5.0 リリースノート {#tidb-6-5-0-release-notes}

発売日：2022年12月29日

TiDB バージョン: 6.5.0

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup)

TiDB 6.5.0 は長期サポートリリース (LTS) です。

TiDB [6.4.0-DMR](/releases/release-6.4.0.md)と比較して、TiDB 6.5.0 では次の主な機能と改善が導入されています。

> **ヒント：**
>
> 以前の LTS 6.1.0 と比較して、 TiDB 6.5.0 には、 [6.2.0-DMR](/releases/release-6.2.0.md) 、 [6.3.0-DMR](/releases/release-6.3.0.md) 、 [6.4.0-DMR](/releases/release-6.4.0.md)でリリースされた新機能、改善点、バグ修正も含まれています。
>
> -   6.1.0 LTS バージョンと 6.5.0 LTS バージョン間の変更点の完全なリストを取得するには、このリリース ノートに加えて、 [6.2.0-DMR リリースノート](/releases/release-6.2.0.md) 、 [6.3.0-DMR リリースノート](/releases/release-6.3.0.md) 、および[6.4.0-DMR リリースノート](/releases/release-6.4.0.md)参照してください。
> -   6.1.0 LTS バージョンと 6.5.0 LTS バージョンの主な機能を簡単に比較するには、 [TiDBの機能](/basic-features.md)の`v6.1`列と`v6.5`列を確認してください。

-   [インデックス加速](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)機能が一般提供 (GA) され、v6.1.0 と比較してインデックス追加のパフォーマンスが約 10 倍向上しました。
-   TiDB グローバルメモリ制御が GA になり、 [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)を介してメモリ消費しきい値を制御できるようになりました。
-   高性能かつグローバルに単調な[`AUTO_INCREMENT`](/auto-increment.md#mysql-compatibility-mode)列属性が、MySQLと互換性のあるGAになります。
-   [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-cluster.md)は TiCDC および PITR と互換性があり、GA になります。
-   より正確な[コストモデル バージョン 2](/cost-model.md#cost-model-version-2)一般に公開し、 `AND`で[インデックスマージ](/explain-index-merge.md)に接続された式をサポートすることで、 TiDB オプティマイザーを強化します。
-   `JSON_EXTRACT()`機能をTiFlashにプッシュダウンすることをサポートします。
-   パスワード コンプライアンス監査要件を満たす[パスワード管理](/password-management.md)ポリシーをサポートします。
-   TiDB LightningとDumpling は、 [輸入](/tidb-lightning/tidb-lightning-data-source.md)および[輸出](/dumpling-overview.md#improve-export-efficiency-through-concurrency)圧縮された SQL および CSV ファイルをサポートします。
-   TiDB データ移行 (DM) [継続的なデータ検証](/dm/dm-continuous-data-validation.md) GA になります。
-   TiDB バックアップ &amp; リストアは、スナップショット チェックポイント バックアップをサポートし、 [PITR](/br/br-pitr-guide.md#run-pitr)のリカバリ パフォーマンスを 50% 向上させ、一般的なシナリオでの RPO を最短 5 分に短縮します。
-   [Kafkaへのデータの複製](/replicate-data-to-kafka.md)の TiCDC スループットを 4000 行/秒から 35000 行/秒に向上し、レプリケーションのレイテンシーを2 秒に短縮します。
-   データのライフサイクルを管理するために行レベル[存続時間（TTL）](/time-to-live.md)を提供します (実験的)。
-   TiCDC は、Amazon S3、Azure Blob Storage、NFS (実験的) などの[変更ログをオブジェクトstorageに複製する](/ticdc/ticdc-sink-to-cloud-storage.md)サポートしています。

## 新機能 {#new-features}

### SQL {#sql}

-   TiDBのインデックス追加のパフォーマンスは約10倍向上します（GA） [＃35983](https://github.com/pingcap/tidb/issues/35983) @ [ベンジャミン2037](https://github.com/benjamin2037) @ [接線](https://github.com/tangenta)

    TiDB v6.3.0では、インデックス作成時のバックフィル速度を向上させる実験的機能として[インデックス加速を追加](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)が導入されました。v6.5.0ではこの機能がGAとなり、デフォルトで有効化されます。大規模テーブルのパフォーマンスはv6.1.0と比較して約10倍向上すると予想されます。この高速化機能は、単一のSQL文がインデックスを逐次追加するシナリオに適しています。複数のSQL文が並列でインデックスを追加する場合は、そのうちの1つのSQL文のみが高速化されます。

-   DDL 変更時の DML 成功率を向上させる軽量メタデータ ロックを提供する (GA) [＃37275](https://github.com/pingcap/tidb/issues/37275) @ [wjhuang2016](https://github.com/wjhuang2016)

    TiDB v6.3.0 では、 [メタデータロック](/metadata-lock.md)実験的機能として導入されています。DML 文によって発生する`Information schema is changed`エラーを回避するため、TiDB はテーブルメタデータの変更時に DML と DDL の優先順位を調整し、実行中の DDL を古いメタデータを持つ DML のコミットまで待機させます。v6.5.0 ではこの機能が GA となり、デフォルトで有効化されます。これは、さまざまな種類の DDL 変更シナリオに適しています。既存のクラスターを v6.5.0 より前のバージョンから v6.5.0 以降にアップグレードすると、TiDB は自動的にメタデータロックを有効にします。この機能を無効にするには、システム変数[`tidb_enable_metadata_lock`](/system-variables.md#tidb_enable_metadata_lock-new-in-v630)を`OFF`に設定します。

    詳細については[ドキュメント](/metadata-lock.md)参照してください。

-   `FLASHBACK CLUSTER TO TIMESTAMP` (GA) [＃37197](https://github.com/pingcap/tidb/issues/37197) [＃13303](https://github.com/tikv/tikv/issues/13303) @ [定義2014](https://github.com/Defined2014) @ [bb7133](https://github.com/bb7133) @ [Jmポテト](https://github.com/JmPotato) @ [コナー1996](https://github.com/Connor1996) @ [HuSharp](https://github.com/HuSharp) @ [カルビンネオ](https://github.com/CalvinNeo)を使用して、クラスターを特定の時点に復元する機能をサポートします。

    TiDB v6.4.0以降、 [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-cluster.md)ステートメントが実験的機能として導入されました。このステートメントを使用すると、ガベージコレクション（GC）の有効期間内の特定の時点にクラスターを復元できます。v6.5.0では、この機能がTiCDCおよびPITRと互換性を持つようになり、GAとなります。この機能により、DMLの誤操作を簡単に元に戻したり、数分で元のクラスターを復元したり、異なる時点のデータをロールバックしてデータが変更された正確な時刻を特定したりすることが可能になります。

    詳細については[ドキュメント](/sql-statements/sql-statement-flashback-cluster.md)参照してください。

-   `INSERT` `UPDATE`含む非トランザクション[＃33485](https://github.com/pingcap/tidb/issues/33485)ステートメント`DELETE`完全[エキシウム](https://github.com/ekexium)サポートします`REPLACE`

    大規模データ処理のシナリオでは、大規模なトランザクションを含む単一のSQL文が、クラスタの安定性とパフォーマンスに悪影響を及ぼす可能性があります。非トランザクションDML文とは、内部実行のために複数のSQL文に分割されたDML文です。分割された文はトランザクションの原子性と独立性を損なう一方で、クラスタの安定性を大幅に向上させます。TiDBはバージョン6.1.0以降、非トランザクション`DELETE`文をサポートしており、バージョン6.5.0以降、非トランザクション`INSERT`文`REPLACE`サポートしてい`UPDATE` 。

    詳細については、 [非トランザクションDMLステートメント](/non-transactional-dml.md)および[`BATCH`構文](/sql-statements/sql-statement-batch.md)参照してください。

-   TTL (time to live) のサポート (実験的) [＃39262](https://github.com/pingcap/tidb/issues/39262) @ [lcwangchao](https://github.com/lcwangchao)

    TTLは行レベルのデータ有効期間管理を提供します。TiDBでは、TTL属性を持つテーブルはデータ有効期間を自動的にチェックし、期限切れのデータを行レベルで削除します。TTLは、オンラインの読み取りおよび書き込みワークロードに影響を与えることなく、不要なデータを定期的かつタイムリーにクリーンアップできるように設計されています。

    詳細については[ドキュメント](/time-to-live.md)参照してください。

-   `INSERT INTO SELECT`ステートメントを使用したTiFlashクエリ結果の保存をサポート (実験的) [＃37515](https://github.com/pingcap/tidb/issues/37515) @ [ゲンリチ](https://github.com/gengliqi)

    TiDB v6.5.0以降、 `INSERT INTO SELECT`ステートメントの`SELECT`句（分析クエリ）をTiFlashにプッシュダウンできるようになりました。これにより、 TiFlashクエリの結果を`INSERT INTO`のようになります。

    ```sql
    INSERT INTO t2 SELECT Mod(x,y) FROM t1;
    ```

    実験的段階中は、この機能はデフォルトで無効になっています。有効にするには、システム変数[`tidb_enable_tiflash_read_for_write_stmt`](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-new-in-v630) `ON`に設定します。この機能では、 `INSERT INTO`で指定される結果テーブルに特別な制限はなく、その結果テーブルにTiFlashレプリカを追加するかどうかは自由に選択できます。この機能の典型的な使用シナリオは以下のとおりです。

    -   TiFlashを使用して複雑な分析クエリを実行する
    -   TiFlashクエリ結果を再利用するか、同時実行性の高いオンライン リクエストを処理する
    -   入力データのサイズと比較して比較的小さい結果セットが必要です。100 MiB 未満が望ましいです。

    詳細については[ドキュメント](/tiflash/tiflash-results-materialization.md)参照してください。

-   バインディング履歴実行プランのサポート（実験的） [＃39199](https://github.com/pingcap/tidb/issues/39199) @ [fzzf678](https://github.com/fzzf678)

    SQL文の場合、実行中の様々な要因により、オプティマイザが以前の最適な実行プランではなく新しい実行プランを選択することがあり、SQLパフォーマンスに影響が出ます。この場合、最適な実行プランがまだクリアされていない場合は、SQL実行履歴に残ります。

    TiDB v6.5.0では、 [`CREATE [GLOBAL | SESSION] BINDING`](/sql-statements/sql-statement-create-binding.md)ステートメントのバインディングオブジェクトを拡張することで、履歴実行プランのバインディングをサポートします。SQLステートメントの実行プランが変更された場合、 `CREATE [GLOBAL | SESSION] BINDING`ステートメントで`plan_digest`指定することで元の実行プランをバインドし、SQL実行履歴メモリテーブルに元の実行プランが残っている限り（例えば`statements_summary` ）、SQLパフォーマンスを迅速に回復できます。この機能により、実行プラン変更の問題への対応プロセスが簡素化され、メンテナンス効率が向上します。

    詳細については[ドキュメント](/sql-plan-management.md#create-a-binding-according-to-a-historical-execution-plan)参照してください。

### Security {#security}

-   パスワードの複雑さのポリシー[＃38928](https://github.com/pingcap/tidb/issues/38928) @ [CbcWestwolf](https://github.com/CbcWestwolf)をサポートする

    このポリシーを有効にすると、パスワードを設定する際に、TiDBはパスワードの長さ、大文字と小文字、数字、特殊文字の数が適切かどうか、パスワードが辞書と一致しているかどうか、そしてユーザー名と一致しているかどうかをチェックします。これにより、安全なパスワードを設定できます。

    TiDB は、パスワードの強度を検証するための SQL 関数[`VALIDATE_PASSWORD_STRENGTH()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_validate-password-strength)提供します。

    詳細については[ドキュメント](/password-management.md#password-complexity-policy)参照してください。

-   パスワード有効期限ポリシー[＃38936](https://github.com/pingcap/tidb/issues/38936) @ [CbcWestwolf](https://github.com/CbcWestwolf)サポート

    TiDBは、パスワードの有効期限ポリシー（手動による有効期限、グローバルレベルの自動有効期限、アカウントレベルの自動有効期限など）の設定をサポートしています。このポリシーを有効にすると、パスワードを定期的に変更する必要があります。これにより、長期使用によるパスワード漏洩のリスクが軽減され、パスワードのセキュリティが向上します。

    詳細については[ドキュメント](/password-management.md#password-expiration-policy)参照してください。

-   パスワード再利用ポリシー[＃38937](https://github.com/pingcap/tidb/issues/38937) @ [キープラーニング20221](https://github.com/keeplearning20221)をサポートする

    TiDBは、グローバルレベルのパスワード再利用ポリシーとアカウントレベルのパスワード再利用ポリシーを含む、パスワード再利用ポリシーの設定をサポートしています。このポリシーを有効にすると、指定期間内に使用したパスワード、または直近の数個のパスワードは使用できなくなります。これにより、パスワードの繰り返し使用によるパスワード漏洩のリスクが軽減され、パスワードのセキュリティが向上します。

    詳細については[ドキュメント](/password-management.md#password-reuse-policy)参照してください。

-   ログイン失敗の追跡と一時的なアカウントロックポリシー[＃38938](https://github.com/pingcap/tidb/issues/38938) @ [末切歯](https://github.com/lastincisor)をサポート

    このポリシーを有効にすると、TiDBに連続して間違ったパスワードでログインした場合、アカウントは一時的にロックされます。ロック時間が終了すると、アカウントは自動的にロック解除されます。

    詳細については[ドキュメント](/password-management.md#failed-login-tracking-and-temporary-account-locking-policy)参照してください。

### 可観測性 {#observability}

-   TiDBダッシュボードはKubernetes上に独立したPod [＃1447](https://github.com/pingcap/tidb-dashboard/issues/1447) @ [サバピン](https://github.com/SabaPing)としてデプロイできる

    TiDB v6.5.0以降およびTiDB Operator v1.4.0以降では、Kubernetes上にTiDB Dashboardを独立したPodとしてデプロイできます。TiDB TiDB Operatorを使用すると、このPodのIPアドレスにアクセスしてTiDB Dashboardを起動できます。

    TiDB ダッシュボードを個別に展開すると、次の利点が得られます。

    -   TiDBダッシュボードのコンピューティング作業はPDノードに負担をかけません。これにより、より安定したクラスター運用が実現します。
    -   PD ノードが利用できない場合でも、ユーザーは診断のために TiDB ダッシュボードにアクセスできます。
    -   インターネット経由でTiDBダッシュボードにアクセスする場合、PDの特権インターフェースは使用されません。そのため、クラスターのセキュリティリスクは軽減されます。

    詳細については[ドキュメント](https://docs.pingcap.com/tidb-in-kubernetes/dev/get-started#deploy-tidb-dashboard-independently)参照してください。

-   パフォーマンス概要ダッシュボードにTiFlashと CDC (変更データキャプチャ) パネル[＃39230](https://github.com/pingcap/tidb/issues/39230) @ [dbsid](https://github.com/dbsid)が追加されました

    TiDB v6.1.0以降、Grafanaにパフォーマンス概要ダッシュボードが導入され、TiDB、TiKV、PDの全体的なパフォーマンス診断のためのシステムレベルのエントリが提供されるようになりました。v6.5.0では、パフォーマンス概要ダッシュボードにTiFlashとCDCのパネルが追加されました。これらのパネルを使用することで、v6.5.0以降では、パフォーマンス概要ダッシュボードを使用してTiDBクラスター内のすべてのコンポーネントのパフォーマンスを分析できます。

    TiFlashパネルと CDC パネルは、 TiFlashおよび TiCDC の監視情報を再編成します。これにより、 TiFlashおよび TiCDC のパフォーマンスの問題の分析とトラブルシューティングの効率が大幅に向上します。

    -   [TiFlashパネル](/grafana-performance-overview-dashboard.md#tiflash)では、 TiFlashクラスターのリクエスト タイプ、レイテンシー分析、リソース使用状況の概要を簡単に表示できます。
    -   [CDCパネル](/grafana-performance-overview-dashboard.md#cdc)では、TiCDC クラスターの健全性、レプリケーションのレイテンシー、データ フロー、ダウンストリームの書き込みレイテンシーを簡単に確認できます。

    詳細については[ドキュメント](/performance-tuning-methods.md)参照してください。

### パフォーマンス {#performance}

-   [インデックスマージ](/glossary.md#index-merge) `AND` [＃39333](https://github.com/pingcap/tidb/issues/39333) @ [グオシャオゲ](https://github.com/guo-shaoge) @ [時間と運命](https://github.com/time-and-fate) @ [ハイランフー](https://github.com/hailanwhu)で接続された式をサポートします

    v6.5.0より前のTiDBでは、 `OR`で連結されたフィルタ条件に対してのみインデックスマージの使用をサポートしていました。v6.5.0以降、TiDBは`WHERE`節において`AND`で連結されたフィルタ条件に対してインデックスマージの使用をサポートするようになりました。これにより、TiDBのインデックスマージはより一般的なクエリフィルタ条件の組み合わせをカバーできるようになり、union( `OR` )関係に限定されなくなりました。現在のv6.5.0バージョンでは、オプティマイザによって自動的に選択された`OR`条件でのインデックスマージのみをサポートしています。11 `AND`条件でインデックスマージを有効にするには、 [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)ヒントを使用する必要があります。

    インデックスマージの詳細については、 [v5.4.0 リリースノート](/releases/release-5.4.0.md#performance)と[インデックスのマージについて説明する](/explain-index-merge.md)参照してください。

-   以下のJSON関数をTiFlash [＃39458](https://github.com/pingcap/tidb/issues/39458) @ [イービン87](https://github.com/yibin87)にプッシュダウンすることをサポートします

    -   `->`
    -   `->>`
    -   `JSON_EXTRACT()`

    JSON形式は、アプリケーションのデータモデリングに柔軟な方法を提供します。そのため、ますます多くのアプリケーションがデータ交換とデータstorageにJSON形式を使用しています。JSON関数をTiFlashにプッシュダウンすることで、JSON型のデータ分析の効率を向上させ、TiDBをよりリアルタイムな分析シナリオに活用できるようになります。

-   以下の文字列関数をTiFlash [＃6115](https://github.com/pingcap/tiflash/issues/6115) @ [xzhangxian1008](https://github.com/xzhangxian1008)にプッシュダウンすることをサポートします

    -   `regexp_like`
    -   `regexp_instr`
    -   `regexp_substr`

-   [ビュー](/views.md) [＃37887](https://github.com/pingcap/tidb/issues/37887) @ [思い出させる](https://github.com/Reminiscent)で実行プラン生成に干渉するグローバルオプティマイザヒントをサポートします

    ビューアクセスのシナリオによっては、最適なパフォーマンスを実現するために、ビュー内のクエリの実行プランにオプティマイザヒントを使用して介入する必要があります。TiDB v6.5.0以降、ビュー内のクエリブロックへのグローバルヒントの追加がサポートされ、クエリで定義されたヒントがビュー内で有効になります。この機能により、ネストされたビューを含む複雑なSQL文にヒントを挿入できるようになり、実行プランの制御が強化され、複雑な文のパフォーマンスが安定化します。グローバルヒントを使用するには、 [クエリブロックに名前を付ける](/optimizer-hints.md#step-1-define-the-query-block-name-of-the-view-using-the-qb_name-hint)と[ヒント参照を指定する](/optimizer-hints.md#step-2-add-the-target-hints)必要です。

    詳細については[ドキュメント](/optimizer-hints.md#hints-that-take-effect-globally)参照してください。

-   [パーティションテーブル](/partitioned-table.md)から TiKV [＃26166](https://github.com/pingcap/tidb/issues/26166) @ [ウィノロス](https://github.com/winoros)へのソート操作のプッシュダウンをサポート

    [パーティションテーブル](/partitioned-table.md)機能は v6.1.0 から GA となっていますが、TiDB は継続的にパフォーマンスを改善しています。v6.5.0 では、TiDB は計算とフィルタリングのために`ORDER BY`や`LIMIT`などのソート操作を TiKV にプッシュダウンする機能をサポートしています。これにより、ネットワーク I/O オーバーヘッドが削減され、パーティションテーブル使用時の SQL パフォーマンスが向上します。

-   オプティマイザーはより正確なコストモデルバージョン2（GA） [＃35240](https://github.com/pingcap/tidb/issues/35240) @ [qw4990](https://github.com/qw4990)を導入しました

    TiDB v6.2.0 では、 [コストモデル バージョン 2](/cost-model.md#cost-model-version-2)実験的機能として導入されました。このモデルは、より正確なコスト推定手法を用いて、オプティマイザーが最適な実行プランを選択できるように支援します。特にTiFlashを導入している場合、コストモデル バージョン 2 は適切なstorageエンジンを自動的に選択し、手動による介入を大幅に削減します。一定期間の実環境テストを経て、このモデルは v6.5.0 で一般提供となります。v6.5.0 以降、新規に作成されたクラスターはデフォルトでコストモデル バージョン 2 を使用します。v6.5.0 にアップグレードしたクラスターでは、コストモデル バージョン 2 によってクエリプランが変更される可能性があるため、十分なパフォーマンステストを行った後、 [`tidb_cost_model_version = 2`](/system-variables.md#tidb_cost_model_version-new-in-v620)変数を設定して新しいコストモデルを使用するように設定できます。

    コスト モデル バージョン 2 は、TiDB オプティマイザーの全体的な機能を大幅に向上させ、TiDB をより強力な HTAP データベースへと進化させる機能として一般公開されます。

    詳細については[ドキュメント](/cost-model.md#cost-model-version-2)参照してください。

-   TiFlashはテーブル行数[＃37165](https://github.com/pingcap/tidb/issues/37165) @ [エルサ0520](https://github.com/elsa0520)を取得する操作を最適化します

    データ分析のシナリオでは、フィルター条件を使わずに`COUNT(*)`でテーブルの実際の行数を取得する操作が一般的です。v6.5.0では、 TiFlashは`COUNT(*)`の書き換えを最適化し、列定義が最短の非NULL列を自動的に選択して行数をカウントします。これにより、 TiFlashのI/O操作数を効果的に削減し、行数取得の実行効率を向上させます。

### 安定性 {#stability}

-   グローバルメモリ制御機能はGA [＃37816](https://github.com/pingcap/tidb/issues/37816) @ [wshwsh12](https://github.com/wshwsh12)になりました

    TiDBはv6.4.0以降、実験的機能としてグローバルメモリ制御を導入しました。v6.5.0ではGAとなり、メインメモリの消費量を追跡できるようになりました。グローバルメモリの消費量が[`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)で定義されたしきい値に達すると、TiDBはGCまたはSQL操作のキャンセルによってメモリ使用量を制限し、安定性を確保しようとします。

    セッション中のトランザクションによって消費されるメモリ（最大値は以前は設定項目[`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit)によって設定されていました）が、メモリ管理モジュールによって追跡されるようになりました。単一セッションのメモリ消費量がシステム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)で定義されたしきい値に達すると、システム変数[`tidb_mem_oom_action`](/system-variables.md#tidb_mem_oom_action-new-in-v610)で定義された動作がトリガーされます（デフォルトは`CANCEL` 、つまり操作のキャンセルです）。前方互換性を確保するため、デフォルト以外の値として[`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit)設定されている場合でも、TiDB はトランザクションが`txn-total-size-limit`で設定されたメモリを使用できるようにします。

    TiDB v6.5.0以降をご利用の場合は、 [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit)削除し、トランザクションのメモリ使用量に別途制限を設けないことを推奨します。代わりに、システム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)と[`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)使用してグローバルメモリを管理することで、メモリ使用効率を向上させることができます。

    詳細については[ドキュメント](/configure-memory-usage.md)参照してください。

### 使いやすさ {#ease-of-use}

-   `EXPLAIN ANALYZE`出力[＃5926](https://github.com/pingcap/tiflash/issues/5926) @ [ホンユニャン](https://github.com/hongyunyan)のTiFlash `TableFullScan`演算子の実行情報を精緻化する

    `EXPLAIN ANALYZE`ステートメントは、実行計画と実行時統計を出力するために使用されます。v6.5.0 では、 TiFlash は`TableFullScan`演算子の実行情報を改良し、DMFile 関連の実行情報を追加しました。これにより、 TiFlash のデータスキャンステータス情報がより直感的に表示されるようになり、 TiFlash のパフォーマンス分析が容易になります。

    詳細については[ドキュメント](/sql-statements/sql-statement-explain-analyze.md)参照してください。

-   JSON形式での実行プランの出力をサポート[＃39261](https://github.com/pingcap/tidb/issues/39261) @ [fzzf678](https://github.com/fzzf678)

    TiDB v6.5.0では、実行プランの出力形式が拡張されました。3 `EXPLAIN`に`FORMAT = "tidb_json"`指定することで、SQL実行プランをJSON形式で出力できます。この機能により、SQLデバッグツールや診断ツールは実行プランをより便利かつ正確に読み取ることができるため、SQL診断やチューニングの利便性が向上します。

    詳細については[ドキュメント](/sql-statements/sql-statement-explain.md)参照してください。

### MySQLの互換性 {#mysql-compatibility}

-   高性能かつグローバルに単調な`AUTO_INCREMENT`列属性 (GA) [＃38442](https://github.com/pingcap/tidb/issues/38442) @ [天菜まお](https://github.com/tiancaiamao)をサポート

    TiDBはv6.4.0以降、実験的機能としてMySQL互換モード`AUTO_INCREMENT`導入しました。このモードでは、すべてのTiDBインスタンスでIDが単調に増加するようにする、集中型の自動インクリメントID割り当てサービスが導入されます。この機能により、自動インクリメントIDによるクエリ結果のソートが容易になります。v6.5.0では、この機能がGAになります。この機能を使用したテーブルの挿入TPSは20,000を超えると予想され、この機能は単一のテーブルとクラスタ全体の書き込みスループットを向上させるためのエラスティックスケーリングをサポートしています。MySQL互換モードを使用するには、テーブル作成時に`AUTO_ID_CACHE` `1`設定する必要があります。以下は例です。

    ```sql
    CREATE TABLE t(a int AUTO_INCREMENT key) AUTO_ID_CACHE 1;
    ```

    詳細については[ドキュメント](/auto-increment.md#mysql-compatibility-mode)参照してください。

### データ移行 {#data-migration}

-   gzip、snappy、zstd 圧縮形式での SQL および CSV ファイルのエクスポートとインポートをサポート[＃38514](https://github.com/pingcap/tidb/issues/38514) @ [リチュンジュ](https://github.com/lichunzhu)

    Dumpling は、gzip、snappy、zstd などの圧縮形式で圧縮された SQL ファイルおよび CSV ファイルへのデータのエクスポートをサポートしています。TiDB TiDB Lightning は、これらの形式で圧縮されたファイルのインポートもサポートしています。

    これまで、CSVファイルやSQLファイルの保存には、データのエクスポートやインポートに大量のstorage容量が必要であり、storageコストが高額になっていました。この機能のリリースにより、データファイルを圧縮することでstorageコストを大幅に削減できます。

    詳細については[ドキュメント](/dumpling-overview.md#improve-export-efficiency-through-concurrency)参照してください。

-   binlog解析機能の最適化[＃924](https://github.com/pingcap/dm/issues/924) @ [gmhdbjd](https://github.com/GMHDBJD)

    TiDBは、移行タスクに含まれないスキーマとテーブルのbinlogイベントをフィルタリングすることで、解析効率と安定性を向上させます。このポリシーはv6.5.0でデフォルトで有効になっています。追加の設定は必要ありません。

    以前は、少数のテーブルを移行する場合でも、上流のbinlogファイル全体を解析する必要がありました。binlogファイル内の移行が不要なテーブルのbinlogイベントも解析する必要があり、効率が悪かったです。また、これらのbinlogイベントが解析をサポートしていない場合、タスクは失敗します。移行タスクで必要なテーブルのbinlogイベントのみを解析することで、binlog解析の効率が大幅に向上し、タスクの安定性も向上します。

-   TiDB LightningのディスククォータはGA [＃446](https://github.com/pingcap/tidb-lightning/issues/446) @ [ブチュイトデゴウ](https://github.com/buchuitoudegou)です

    TiDB Lightningのディスククォータを設定できます。ディスククォータが不足している場合、 TiDB Lightning はソースデータの読み取りと一時ファイルへの書き込みを停止します。代わりに、ソートされたキーと値をまず TiKV に書き込み、TiDB Lightningの一時ファイルを削除した後、インポートプロセスを続行します。

    以前は、 TiDB Lightning が物理モードでデータをインポートすると、生データのエンコード、ソート、分割のためにローカルディスク上に多数の一時ファイルが作成されていました。ローカルディスクの空き容量が不足すると、 TiDB Lightning はファイルへの書き込みに失敗したためにエラーで終了していました。この機能により、 TiDB Lightningタスクはローカルディスクの上書きを回避できます。

    詳細については[ドキュメント](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#configure-disk-quota-new-in-v620)参照してください。

-   DMにおける継続的なデータ検証はGA [＃4426](https://github.com/pingcap/tiflow/issues/4426) @ [D3ハンター](https://github.com/D3Hunter)です

    上流データベースから下流データベースへの増分データ移行プロセスでは、データフローによってエラーやデータ損失が発生する可能性がわずかにあります。クレジットや証券業務など、強力なデータ整合性が求められるシナリオでは、移行後にデータに対してフルボリュームチェックサムを実行し、データの整合性を確保できます。ただし、一部の増分レプリケーションシナリオでは、上流と下流のデータが常に変化するため、上流と下流への書き込みが継続的かつ中断されることなく行われるため、すべてのデータに対して整合性チェックを実行することが困難です。

    以前は、データ全体を検証するために業務を中断する必要があり、業務に影響が出ていました。この機能により、業務を中断することなく増分データ検証を実行できるようになりました。

    詳細については[ドキュメント](/dm/dm-continuous-data-validation.md)参照してください。

### TiDBデータ共有サブスクリプション {#tidb-data-share-subscription}

-   TiCDC は、変更されたログをstorageシンクに複製することをサポートしています (実験的) [＃6797](https://github.com/pingcap/tiflow/issues/6797) @ [ジャオシンユ](https://github.com/zhaoxinyu)

    TiCDCは、Amazon S3、Azure Blob Storage、NFS、その他のS3互換storageサービスへの変更ログのレプリケーションをサポートしています。クラウドstorageは手頃な価格で使いやすいです。Kafkaを使用していない場合は、storageシンクを使用できます。TiCDCは変更ログをファイルに保存し、storageシステムに送信します。コンシューマープログラムは、storageシステムから新しく生成された変更ログファイルを定期的に読み取ります。

    storageシンクは、canal-json形式とCSV形式の変更ログをサポートしています。詳細については、 [ドキュメント](/ticdc/ticdc-sink-to-cloud-storage.md)ご覧ください。

-   TiCDCは2つのクラスタ間の双方向レプリケーションをサポートします[＃38587](https://github.com/pingcap/tidb/issues/38587) @ [ションジウェイ](https://github.com/xiongjiwei) @ [アズドンメン](https://github.com/asddongmen)

    TiCDCは、2つのTiDBクラスタ間の双方向レプリケーションをサポートしています。アプリケーションのために地理的に分散された複数のアクティブデータセンターを構築する必要がある場合、この機能をソリューションとして利用できます。あるTiDBクラスタから別のTiDBクラスタへのTiCDC変更フィードに`bdr-mode = true`パラメータを設定することで、2つのTiDBクラスタ間の双方向データレプリケーションを実現できます。

    詳細については[ドキュメント](/ticdc/ticdc-bidirectional-replication.md)参照してください。

-   TiCDCはTLSオンライン[＃7908](https://github.com/pingcap/tiflow/issues/7908) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)更新をサポート

    データベースシステムのセキュリティを維持するには、システムで使用する証明書に有効期限ポリシーを設定する必要があります。有効期限が切れると、システムは新しい証明書を必要とします。TiCDC v6.5.0は、TLS証明書のオンライン更新をサポートしています。レプリケーションタスクを中断することなく、TiCDCは証明書を自動的に検出して更新するため、手動による介入は不要です。

-   TiCDCのパフォーマンスが大幅に向上[＃7540](https://github.com/pingcap/tiflow/issues/7540) [＃7478](https://github.com/pingcap/tiflow/issues/7478) [＃7532](https://github.com/pingcap/tiflow/issues/7532) @ [スドジ](https://github.com/sdojjy) @ [3エースショーハンド](https://github.com/3AceShowHand)

    TiDBクラスタのテストシナリオでは、TiCDCのパフォーマンスが大幅に向上しました。具体的には、シナリオ[Kafkaへのデータの複製](/replicate-data-to-kafka.md)では、単一のTiCDCが処理できる行変更の最大量は3万行/秒に達し、レプリケーションのレイテンシーは10秒に短縮されました。TiKVとTiCDCのローリングアップグレード中でも、レプリケーションのレイテンシーは30秒未満です。

    災害復旧 (DR) シナリオでは、TiCDC の再実行ログと同期ポイントを有効にすると、TiCDC のスループットが 4000 行/秒から 35000 行/秒に向上し、レプリケーションのレイテンシーを2 秒に制限できます。

### バックアップと復元 {#backup-and-restore}

-   TiDB バックアップ &amp; リストアはスナップショット チェックポイント バックアップ[＃38647](https://github.com/pingcap/tidb/issues/38647) @ [リーヴルス](https://github.com/Leavrth)をサポートします

    TiDBスナップショットバックアップは、チェックポイントからのバックアップ再開をサポートしています。バックアップ＆リストア（BR）は、回復可能なエラーが発生するとバックアップを再試行します。ただし、再試行が複数回失敗するとBRは終了します。チェックポイントバックアップ機能により、数十分のネットワーク障害など、回復可能なより長い障害の再試行が可能になります。

    BR終了後1時間以内にシステムを障害から復旧しない場合、バックアップ対象のスナップショットデータがGCメカニズムによって再利用され、バックアップが失敗する可能性があります。詳細については、 [ドキュメント](/br/br-checkpoint-backup.md#backup-retry-must-be-prior-to-gc)参照してください。

-   PITRのパフォーマンスは[ジョッカウ](https://github.com/joccau)で著しく向上しました

    ログリストア段階では、1つのTiKVのリストア速度が9MiB/秒に達し、従来比50%の高速化を実現しました。リストア速度はスケーラブルで、DRシナリオにおけるRTO（目標復旧時間）は大幅に短縮されます。DRシナリオにおけるRPO（目標復旧時点）は最短5分です。通常のクラスタ運用保守（OM）では、例えばローリングアップグレードの実行時や1つのTiKVのみがダウンしている場合でも、RPOは5分です。

-   TiKV- BR GA: RawKV [＃67](https://github.com/tikv/migration/issues/67) @ [ピンギュ](https://github.com/pingyu) @ [ハオジンミン](https://github.com/haojinming)バックアップと復元をサポート

    TiKV- BRは、TiKVクラスターで使用されるバックアップおよびリストアツールです。TiKVとPDは、TiDBを使用せずにRawKVと呼ばれるKVデータベースを構成できます。TiKV- BRは、RawKVを使用する製品のデータバックアップとリストアをサポートします。また、 BRクラスターの[`api-version`](/tikv-configuration-file.md#api-version-new-in-v610) `API V1`から`API V2`にアップグレードすることもできます。

    詳細については[ドキュメント](https://tikv.org/docs/latest/concepts/explore-tikv-features/backup-restore/)参照してください。

## 互換性の変更 {#compatibility-changes}

### システム変数 {#system-variables}

| 変数名                                                                                                                       | タイプを変更   | 説明                                                                                                                                                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `tidb_enable_amend_pessimistic_txn`                                                                                       | 非推奨      | v6.5.0 以降、この変数は非推奨となり、TiDB は`Information schema is changed`エラーを回避するためにデフォルトで[メタデータロック](/metadata-lock.md)機能を使用します。                                                                                                                                                                                                                                  |
| [`tidb_enable_outer_join_reorder`](/system-variables.md#tidb_enable_outer_join_reorder-new-in-v610)                       | 修正済み     | さらにテストを行った後、デフォルト値を`OFF`から`ON`に変更します。つまり、 [結合したテーブルの再配置](/join-reorder.md)アルゴリズムの Outer Join のサポートがデフォルトで有効になります。                                                                                                                                                                                                                                   |
| [`tidb_cost_model_version`](/system-variables.md#tidb_cost_model_version-new-in-v620)                                     | 修正済み     | さらにテストを行った後、デフォルト値を`1`から`2`に変更します。つまり、インデックス選択と演算子選択には、デフォルトでコスト モデル バージョン 2 が使用されることになります。                                                                                                                                                                                                                                                         |
| [`tidb_enable_gc_aware_memory_track`](/system-variables.md#tidb_enable_gc_aware_memory_track)                             | 修正済み     | デフォルト値を`ON`から`OFF`に変更します。GC対応メモリトラックはテストで不正確であることが判明し、追跡されるメモリサイズが過大になるため、メモリトラックは無効化されています。また、 Golang 1.19では、GC対応メモリトラックによって追跡されるメモリは、全体のメモリに大きな影響を与えません。                                                                                                                                                                                          |
| [`tidb_enable_metadata_lock`](/system-variables.md#tidb_enable_metadata_lock-new-in-v630)                                 | 修正済み     | さらにテストを行った後、デフォルト値を`OFF`から`ON`に変更します。これは、メタデータ ロック機能がデフォルトで有効になっていることを意味します。                                                                                                                                                                                                                                                                        |
| [`tidb_enable_tiflash_read_for_write_stmt`](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-new-in-v630)     | 修正済み     | バージョン6.5.0以降で有効になります。1、3、5 `INSERT` `UPDATE` SQL文の読み取り操作`DELETE` TiFlashにプッシュダウンするかどうかを制御します。デフォルト値は`OFF`です。                                                                                                                                                                                                                                        |
| [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)                               | 修正済み     | さらにテストを行った後、デフォルト値を`OFF`から`ON`に変更します。つまり、 `ADD INDEX`と`CREATE INDEX`の加速はデフォルトで有効になります。                                                                                                                                                                                                                                                              |
| [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)                                                       | 修正済み     | TiDB v6.5.0より前のバージョンでは、この変数はクエリのメモリクォータのしきい値を設定するために使用されます。TiDB v6.5.0以降のバージョンでは、DML文のメモリをより正確に制御するために、この変数はセッションのメモリクォータのしきい値を設定するために使用されます。                                                                                                                                                                                                       |
| [`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40)                                                  | 修正済み     | v6.5.0 以降、TiDB ノード間の負荷分散を最適化するために、この変数が`closest-adaptive`に設定され、読み取り要求の推定結果が[`tidb_adaptive_closest_read_threshold`](/system-variables.md#tidb_adaptive_closest_read_threshold-new-in-v630)以上の場合、 `closest-adaptive`構成が有効になる TiDB ノードの数が各アベイラビリティーゾーンで制限されます。これは、TiDB ノードが最も少ないアベイラビリティーゾーンの TiDB ノードの数と常に同じになり、その他の TiDB ノードは自動的にリーダー レプリカから読み取ります。 |
| [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)                                   | 修正済み     | デフォルト値を`0`から`80%`に変更します。TiDB グローバルメモリ制御が GA になったため、このデフォルト値の変更により、メモリ制御がデフォルトで有効になり、TiDB インスタンスのメモリ制限がデフォルトで合計メモリの 80% に設定されます。                                                                                                                                                                                                                     |
| [`default_password_lifetime`](/system-variables.md#default_password_lifetime-new-in-v650)                                 | 新しく追加された | パスワードの自動有効期限に関するグローバルポリシーを設定し、ユーザーに定期的なパスワード変更を義務付けます。デフォルト値`0` 、パスワードが無期限であることを示します。                                                                                                                                                                                                                                                               |
| [`disconnect_on_expired_password`](/system-variables.md#disconnect_on_expired_password-new-in-v650)                       | 新しく追加された | パスワードの有効期限が切れたときにTiDBがクライアント接続を切断するかどうかを示します。この変数は読み取り専用です。                                                                                                                                                                                                                                                                                         |
| [`tidb_store_batch_size`](/system-variables.md#tidb_store_batch_size)                                                     | 新しく追加された | この変数はデフォルトで無効になっており、これによって制御される機能はまだ安定していません。本番環境ではこの変数を変更することは推奨されません。                                                                                                                                                                                                                                                                             |
| [`password_history`](/system-variables.md#password_history-new-in-v650)                                                   | 新しく追加された | この変数は、パスワード変更回数に基づいてTiDBがパスワードの再利用を制限するためのパスワード再利用ポリシーを設定するために使用されます。デフォルト値の`0` 、パスワード変更回数に基づくパスワード再利用ポリシーを無効にすることを意味します。                                                                                                                                                                                                                           |
| [`password_reuse_interval`](/system-variables.md#password_reuse_interval-new-in-v650)                                     | 新しく追加された | この変数は、TiDBが経過時間に基づいてパスワードの再利用を制限するためのパスワード再利用ポリシーを設定するために使用されます。デフォルト値の`0` 、経過時間に基づくパスワード再利用ポリシーを無効にすることを意味します。                                                                                                                                                                                                                                     |
| [`tidb_auto_build_stats_concurrency`](/system-variables.md#tidb_auto_build_stats_concurrency-new-in-v650)                 | 新しく追加された | この変数は、統計の自動更新の同時実行数を設定するために使用されます。デフォルト値は`1`です。                                                                                                                                                                                                                                                                                                     |
| [`tidb_cdc_write_source`](/system-variables.md#tidb_cdc_write_source-new-in-v650)                                         | 新しく追加された | この変数が0以外の値に設定されている場合、このセッションで書き込まれたデータはTiCDCによって書き込まれたものとみなされます。この変数はTiCDCによってのみ変更できます。いかなる場合でも、この変数を手動で変更しないでください。                                                                                                                                                                                                                                 |
| [`tidb_enable_plan_replayer_capture`](/system-variables.md#tidb_enable_plan_replayer_capture)                             | 新しく追加された | この変数で制御される機能は、TiDB v6.5.0では完全には機能しません。デフォルト値を変更しないでください。                                                                                                                                                                                                                                                                                            |
| [`tidb_index_merge_intersection_concurrency`](/system-variables.md#tidb_index_merge_intersection_concurrency-new-in-v650) | 新しく追加された | インデックスマージが実行する交差操作の最大同時実行数を設定します。これは、TiDBが動的プルーニングモードでパーティションテーブルにアクセスする場合にのみ有効です。                                                                                                                                                                                                                                                                  |
| [`tidb_source_id`](/system-variables.md#tidb_source_id-new-in-v650)                                                       | 新しく追加された | この変数は、 [双方向レプリケーション](/ticdc/ticdc-bidirectional-replication.md)クラスター内の異なるクラスター ID を構成するために使用されます。                                                                                                                                                                                                                                                   |
| [`tidb_sysproc_scan_concurrency`](/system-variables.md#tidb_sysproc_scan_concurrency-new-in-v650)                         | 新しく追加された | この変数は、TiDBが内部SQL文（統計情報の自動更新など）を実行する際に実行されるスキャン操作の同時実行性を設定するために使用されます。デフォルト値は`1`です。                                                                                                                                                                                                                                                                  |
| [`tidb_ttl_delete_batch_size`](/system-variables.md#tidb_ttl_delete_batch_size-new-in-v650)                               | 新しく追加された | この変数は、TTL ジョブ内の単一`DELETE`トランザクションで削除できる行の最大数を設定するために使用されます。                                                                                                                                                                                                                                                                                         |
| [`tidb_ttl_delete_rate_limit`](/system-variables.md#tidb_ttl_delete_rate_limit-new-in-v650)                               | 新しく追加された | この変数は、TTLジョブにおいて単一ノードで1秒あたりに許可される`DELETE`ステートメントの最大数を制限するために使用されます。この変数を`0`に設定すると、制限は適用されません。                                                                                                                                                                                                                                                       |
| [`tidb_ttl_delete_worker_count`](/system-variables.md#tidb_ttl_delete_worker_count-new-in-v650)                           | 新しく追加された | この変数は、各 TiDB ノード上の TTL ジョブの最大同時実行数を設定するために使用されます。                                                                                                                                                                                                                                                                                                   |
| [`tidb_ttl_job_enable`](/system-variables.md#tidb_ttl_job_enable-new-in-v650)                                             | 新しく追加された | この変数は、TTLジョブを有効にするかどうかを制御するために使用されます`OFF`に設定すると、TTL属性を持つすべてのテーブルで期限切れデータのクリーンアップが自動的に停止されます。                                                                                                                                                                                                                                                        |
| `tidb_ttl_job_run_interval`                                                                                               | 新しく追加された | この変数は、バックグラウンドでのTTLジョブのスケジュール間隔を制御するために使用されます。例えば、現在の値が`1h0m0s`に設定されている場合、TTL属性を持つ各テーブルは、期限切れのデータを1時間ごとにクリーンアップします。                                                                                                                                                                                                                                 |
| [`tidb_ttl_job_schedule_window_start_time`](/system-variables.md#tidb_ttl_job_schedule_window_start_time-new-in-v650)     | 新しく追加された | この変数は、バックグラウンドで実行されるTTLジョブのスケジュールウィンドウの開始時刻を制御するために使用されます。この変数の値を変更する際は、ウィンドウが小さいと期限切れデータのクリーンアップが失敗する可能性があるので注意してください。                                                                                                                                                                                                                             |
| [`tidb_ttl_job_schedule_window_end_time`](/system-variables.md#tidb_ttl_job_schedule_window_end_time-new-in-v650)         | 新しく追加された | この変数は、バックグラウンドでのTTLジョブのスケジュールウィンドウの終了時刻を制御するために使用されます。この変数の値を変更する際は、ウィンドウが小さいと期限切れデータのクリーンアップが失敗する可能性があるので注意してください。                                                                                                                                                                                                                                 |
| [`tidb_ttl_scan_batch_size`](/system-variables.md#tidb_ttl_scan_batch_size-new-in-v650)                                   | 新しく追加された | この変数は、TTL ジョブで期限切れのデータをスキャンするために使用される`SELECT`ステートメントごとに`LIMIT`値を設定するために使用されます。                                                                                                                                                                                                                                                                      |
| [`tidb_ttl_scan_worker_count`](/system-variables.md#tidb_ttl_scan_worker_count-new-in-v650)                               | 新しく追加された | この変数は、各 TiDB ノード上の TTL スキャン ジョブの最大同時実行数を設定するために使用されます。                                                                                                                                                                                                                                                                                              |
| [`validate_password.check_user_name`](/system-variables.md#validate_passwordcheck_user_name-new-in-v650)                  | 新しく追加された | パスワード複雑度チェックにおけるチェック項目。パスワードがユーザー名と一致するかどうかをチェックします。この変数は、 [`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650)有効になっている場合にのみ有効になります。デフォルト値は`ON`です。                                                                                                                                                                |
| [`validate_password.dictionary`](/system-variables.md#validate_passworddictionary-new-in-v650)                            | 新しく追加された | パスワードの複雑性チェックにおけるチェック項目です。パスワードが辞書内の単語と一致するかどうかをチェックします。この変数は、 [`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650)が有効で、 [`validate_password.policy`](/system-variables.md#validate_passwordpolicy-new-in-v650) `2` （STRONG）に設定されている場合にのみ有効になります。デフォルト値は`""`です。                                                   |
| [`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650)                                    | 新しく追加された | この変数は、パスワードの複雑さのチェックを実行するかどうかを制御します。この変数を`ON`に設定すると、TiDBはパスワード設定時にパスワードの複雑さのチェックを実行します。デフォルト値は`OFF`です。                                                                                                                                                                                                                                              |
| [`validate_password.length`](/system-variables.md#validate_passwordlength-new-in-v650)                                    | 新しく追加された | パスワードの複雑さチェックにおけるチェック項目です。パスワードの長さが十分かどうかをチェックします。デフォルトでは、パスワードの最小長は`8`です。この変数は、 [`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650)有効になっている場合にのみ有効になります。                                                                                                                                                        |
| [`validate_password.mixed_case_count`](/system-variables.md#validate_passwordmixed_case_count-new-in-v650)                | 新しく追加された | パスワードの複雑さチェックにおけるチェック項目です。パスワードに十分な大文字と小文字が含まれているかどうかをチェックします。この変数は、 [`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650)が有効で、 [`validate_password.policy`](/system-variables.md#validate_passwordpolicy-new-in-v650) `1` （中）以上に設定されている場合にのみ有効になります。デフォルト値は`1`です。                                                 |
| [`validate_password.number_count`](/system-variables.md#validate_passwordnumber_count-new-in-v650)                        | 新しく追加された | パスワードの複雑さチェックにおけるチェック項目です。パスワードに十分な数の数字が含まれているかどうかをチェックします。この変数は、 [`validate_password.enable`](/system-variables.md#password_reuse_interval-new-in-v650)が有効で、 [`validate_password.policy`](/system-variables.md#validate_passwordpolicy-new-in-v650) `1` （中）以上に設定されている場合にのみ有効になります。デフォルト値は`1`です。                                                    |
| [`validate_password.policy`](/system-variables.md#validate_passwordpolicy-new-in-v650)                                    | 新しく追加された | この変数は、パスワードの複雑さチェックのポリシーを制御します。値は`0` 、 `1` 、または`2` （それぞれLOW、MEDIUM、STRONGに対応）です。この変数は[`validate_password.enable`](/system-variables.md#password_reuse_interval-new-in-v650)が有効な場合にのみ有効になります。デフォルト値は`1`です。                                                                                                                                           |
| [`validate_password.special_char_count`](/system-variables.md#validate_passwordspecial_char_count-new-in-v650)            | 新しく追加された | パスワード複雑度チェックにおけるチェック項目。パスワードに十分な特殊文字が含まれているかどうかをチェックします。この変数は、 [`validate_password.enable`](/system-variables.md#password_reuse_interval-new-in-v650)が有効で、 [`validate_password.policy`](/system-variables.md#validate_passwordpolicy-new-in-v650) `1` （中）以上に設定されている場合にのみ有効になります。デフォルト値は`1`です。                                                       |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                            | タイプを変更   | 説明                                                                                                                                                      |
| -------------- | ---------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | [`server-memory-quota`](/tidb-configuration-file.md#server-memory-quota-new-in-v409)                       | 非推奨      | バージョン6.5.0以降、この設定項目は非推奨となりました。代わりに、システム変数[`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)使用してメモリをグローバルに管理してください。 |
| TiDB           | [`disconnect-on-expired-password`](/tidb-configuration-file.md#disconnect-on-expired-password-new-in-v650) | 新しく追加された | パスワードの有効期限が切れたときに、TiDBがクライアント接続を切断するかどうかを決定します。デフォルト値は`true`で、パスワードの有効期限が切れるとクライアント接続が切断されます。                                                           |
| TiKV           | `raw-min-ts-outlier-threshold`                                                                             | 削除済み     | この構成項目はバージョン 6.4.0 で非推奨となり、バージョン 6.5.0 で削除されました。                                                                                                        |
| TiKV           | [`raft-engine.bytes-per-sync`](/tikv-configuration-file.md#bytes-per-sync-2)                               | 非推奨      | バージョン6.5.0以降、 Raft Engineはバッファリングなしでログを直接ディスクに書き込むようになりました。そのため、この設定項目は非推奨となり、機能しなくなりました。                                                               |
| TiKV           | [`cdc.min-ts-interval`](/tikv-configuration-file.md#min-ts-interval)                                       | 修正済み     | CDC のレイテンシーを削減するために、デフォルト値は`"1s"`から`"200ms"`に変更されます。                                                                                                    |
| TiKV           | [`memory-use-ratio`](/tikv-configuration-file.md#memory-use-ratio-new-in-v650)                             | 新しく追加された | PITR ログリカバリにおける使用可能なメモリとシステムメモリの合計の比率を示します。                                                                                                             |
| TiCDC          | [`sink.terminator`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)                 | 新しく追加された | 2つのデータ変更イベントを区切るために使用される行ターミネータを示します。デフォルトでは値は空で、 `\r\n`が使用されます。                                                                                        |
| TiCDC          | [`sink.date-separator`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)             | 新しく追加された | ファイルディレクトリの日付区切りの種類を示します。値のオプションは`none` 、 `year` 、 `month` 、 `day`です。デフォルト値は`none`で、日付が区切られないことを意味します。                                                  |
| TiCDC          | [`sink.enable-partition-separator`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters) | 新しく追加された | パーティションを区切り文字列として使用するかどうかを指定します。デフォルト値は`false`で、テーブル内のパーティションが別々のディレクトリに保存されないことを意味します。                                                                 |
| TiCDC          | [`sink.csv.delimiter`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)              | 新しく追加された | フィールド間の区切り文字を示します。値はASCII文字でなければならず、デフォルトは`,`です。                                                                                                        |
| TiCDC          | [`sink.csv.quote`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)                  | 新しく追加された | フィールドを囲む引用符。デフォルト値は`"`です。値が空の場合、引用符は使用されません。                                                                                                            |
| TiCDC          | [`sink.csv.null`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)                   | 新しく追加された | CSV列がnullの場合に表示される文字を指定します。デフォルト値は`\N`です。                                                                                                               |
| TiCDC          | [`sink.csv.include-commit-ts`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)      | 新しく追加された | CSV行にコミット情報を含めるかどうかを指定します。デフォルト値は`false`です。                                                                                                             |

### その他 {#others}

-   v6.5.0 以降、 `mysql.user`テーブルに`Password_reuse_history`と`Password_reuse_time` 2 つの新しい列が追加されます。
-   バージョン6.5.0以降、 [インデックス加速](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)機能がデフォルトで有効になっています。この機能はバージョン[1つの`ALTER TABLE`文で複数の列またはインデックスを変更する](/sql-statements/sql-statement-alter-table.md)と完全に互換性がありません。インデックスアクセラレーションを使用してユニークインデックスを追加する場合、同じステートメント内で他の列やインデックスを変更しないようにする必要があります。この機能はバージョン[PITR（ポイントインタイムリカバリ）](/br/br-pitr-guide.md)とも互換性がありません。インデックスアクセラレーション機能を使用する場合は、バックグラウンドでPITRバックアップタスクが実行されていないことを確認する必要があります。そうしないと、予期しない結果が発生する可能性があります。詳細については、 [ドキュメント](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)参照してください。

## 非推奨の機能 {#deprecated-feature}

v6.5.0 以降、v4.0.7 で導入された`AMEND TRANSACTION`メカニズムは非推奨となり、 [メタデータロック](/metadata-lock.md)に置き換えられます。

## 改善点 {#improvements}

-   TiDB

    -   `BIT`列目と`CHAR`列目については、 `INFORMATION_SCHEMA.COLUMNS`の結果をMySQL [＃25472](https://github.com/pingcap/tidb/issues/25472) @ [ホーキングレイ](https://github.com/hawkingrei)と一致させる
    -   TiFlash MPPモードのTiFlashノードのTiDBプローブメカニズムを最適化し、ノードが異常な場合のパフォーマンスへの影響を軽減します[＃39686](https://github.com/pingcap/tidb/issues/39686) @ [ハッカーシアン](https://github.com/hackersean)

-   TiKV

    -   ディスク容量の枯渇を避けるため、十分なスペースがない場合はRaft Engineへの書き込みを停止します[＃13642](https://github.com/tikv/tikv/issues/13642) @ [嘉陽鄭](https://github.com/jiayang-zheng)
    -   `json_valid`関数を TiKV [＃13571](https://github.com/tikv/tikv/issues/13571) @ [立振環](https://github.com/lizhenhuan)にプッシュダウンすることをサポートします
    -   1回のバックアップ要求で複数の範囲のデータのバックアップをサポート[＃13701](https://github.com/tikv/tikv/issues/13701) @ [リーヴルス](https://github.com/Leavrth)
    -   rusotoライブラリ[＃13751](https://github.com/tikv/tikv/issues/13751) @ [3ポイントシュート](https://github.com/3pointer)を更新してAWSのアジア太平洋地域（ap-southeast-3）へのデータバックアップをサポート
    -   悲観的トランザクション競合を減らす[＃13298](https://github.com/tikv/tikv/issues/13298) @ [ミョンケミンタ](https://github.com/MyonKeminta)
    -   外部storageオブジェクト[＃13798](https://github.com/tikv/tikv/issues/13798) @ [ユジュンセン](https://github.com/YuJuncen)をキャッシュすることでリカバリパフォーマンスを向上
    -   専用スレッドで CheckLeader を実行して、TiCDC レプリケーションのレイテンシー[＃13774](https://github.com/tikv/tikv/issues/13774) @ [金星の上](https://github.com/overvenus)を削減します。
    -   チェックポイント[＃13824](https://github.com/tikv/tikv/issues/13824) @ [ユジュンセン](https://github.com/YuJuncen)のプル モデルをサポート
    -   クロスビームチャネル[＃13815](https://github.com/tikv/tikv/issues/13815)を[スティクナーフ](https://github.com/sticnarf)に更新することで、送信側での回転の問題を回避します。
    -   TiKV [＃13849](https://github.com/tikv/tikv/issues/13849) @ [cfzjywxk](https://github.com/cfzjywxk)でのバッチココプロセッサータスク処理をサポート
    -   TiKVにリージョン[＃13648](https://github.com/tikv/tikv/issues/13648) @ [LykxSassinator](https://github.com/LykxSassinator)を起動するように通知することで、障害回復の待ち時間を短縮します。
    -   コード最適化[＃13827](https://github.com/tikv/tikv/issues/13827) @ [ビジージェイ](https://github.com/BusyJay)によりメモリ使用量の要求サイズを削減
    -   コードの拡張性を向上させるためにRaft拡張機能を導入する[＃13827](https://github.com/tikv/tikv/issues/13827) @ [ビジージェイ](https://github.com/BusyJay)
    -   tikv-ctl を使用して、特定のキー範囲[＃13760](https://github.com/tikv/tikv/issues/13760) @ [HuSharp](https://github.com/HuSharp)に含まれるリージョンを照会することをサポートします。
    -   更新されないが継続的にロックされている行の読み取りおよび書き込みパフォーマンスを向上[＃13694](https://github.com/tikv/tikv/issues/13694) @ [スティクナーフ](https://github.com/sticnarf)

-   PD

    -   ロックの粒度を最適化してロックの競合を減らし、高同時実行時のハートビートの処理能力を向上させる[＃5586](https://github.com/tikv/pd/issues/5586) @ [rleungx](https://github.com/rleungx)
    -   大規模クラスタのスケジューラパフォーマンスを最適化し、スケジューリングポリシー[＃5473](https://github.com/tikv/pd/issues/5473) @ [バッファフライ](https://github.com/bufferflies)の本番を高速化します。
    -   リージョン[＃5606](https://github.com/tikv/pd/issues/5606) @ [rleungx](https://github.com/rleungx)の読み込み速度を向上
    -   リージョンハートビート[＃5648](https://github.com/tikv/pd/issues/5648) @ [rleungx](https://github.com/rleungx)の最適化された処理により不要なオーバーヘッドを削減
    -   墓石ストア[＃5348](https://github.com/tikv/pd/issues/5348) @ [ノルーシュ](https://github.com/nolouch)のガベージコレクションを自動的に行う機能を追加

-   TiFlash

    -   SQL側でバッチ処理が行われないシナリオでの書き込みパフォーマンスの向上[＃6404](https://github.com/pingcap/tiflash/issues/6404) @ [リデジュ](https://github.com/lidezhu)
    -   `explain analyze`出力[＃5926](https://github.com/pingcap/tiflash/issues/5926) @ [ホンユニャン](https://github.com/hongyunyan)に TableFullScan の詳細を追加します

-   ツール

    -   TiDBダッシュボード

        -   低速クエリ ページに 3 つの新しいフィールドを追加します:「準備済みですか?」、「プランはキャッシュから取得されていますか?」、「プランはバインディングから取得されていますか?」 [＃1451](https://github.com/pingcap/tidb-dashboard/issues/1451) @ [シュジット](https://github.com/shhdgit)

    -   バックアップと復元 (BR)

        -   バックアップログデータ[＃38869](https://github.com/pingcap/tidb/issues/38869) @ [リーヴルス](https://github.com/Leavrth)の消去プロセス中のBRメモリ使用量を最適化します
        -   復元プロセス中にPDリーダースイッチによって発生する復元失敗の問題を修正[＃36910](https://github.com/pingcap/tidb/issues/36910) @ [モクイシュル28](https://github.com/MoCuishle28)
        -   ログバックアップ[＃13867](https://github.com/tikv/tikv/issues/13867) @ [ユジュンセン](https://github.com/YuJuncen)で OpenSSL プロトコルを使用することにより、TLS 互換性が向上します。

    -   TiCDC

        -   Kafka プロトコルエンコーダー[＃7540](https://github.com/pingcap/tiflow/issues/7540) [＃7532](https://github.com/pingcap/tiflow/issues/7532) [＃7543](https://github.com/pingcap/tiflow/issues/7543) @ [3エースショーハンド](https://github.com/3AceShowHand) @ [スドジ](https://github.com/sdojjy)のパフォーマンスを向上

    -   TiDB データ移行 (DM)

        -   ブロックリスト[＃7622](https://github.com/pingcap/tiflow/pull/7622) @ [GMHDBJD](https://github.com/GMHDBJD)内のテーブルのデータを解析しないことで、DMのデータ複製パフォーマンスを向上します。
        -   非同期書き込みとバッチ書き込み[＃7580](https://github.com/pingcap/tiflow/pull/7580) @ [GMHDBJD](https://github.com/GMHDBJD)を使用してDMリレーの書き込み効率を向上
        -   DM事前チェック[＃7621](https://github.com/pingcap/tiflow/issues/7621) @ [ブチュイトデゴウ](https://github.com/buchuitoudegou)のエラーメッセージを最適化
        -   古いMySQLバージョン[＃5017](https://github.com/pingcap/tiflow/issues/5017)と`SHOW SLAVE HOSTS` [lyzx2001](https://github.com/lyzx2001)互換性を改善

## バグ修正 {#bug-fixes}

-   TiDB

    -   一部のケースで発生するチャンク再利用機能のメモリチャンクの誤用問題を修正[＃38917](https://github.com/pingcap/tidb/issues/38917) @ [キープラーニング20221](https://github.com/keeplearning20221)
    -   `tidb_constraint_check_in_place_pessimistic`の内部セッションがグローバル設定[＃38766](https://github.com/pingcap/tidb/issues/38766) @ [エキシウム](https://github.com/ekexium)の影響を受ける可能性がある問題を修正しました
    -   `AUTO_INCREMENT`列目が`CHECK`制約[＃38894](https://github.com/pingcap/tidb/issues/38894) @ [ヤンケオ](https://github.com/YangKeao)で動作できない問題を修正
    -   `INSERT IGNORE INTO`使用して`STRING`型のデータを`SMALLINT`型の自動インクリメント列に挿入すると、エラー[＃38483](https://github.com/pingcap/tidb/issues/38483) @ [ホーキングレイ](https://github.com/hawkingrei)が発生する問題を修正しました。
    -   パーティションテーブル[＃38932](https://github.com/pingcap/tidb/issues/38932) @ [ミョンス](https://github.com/mjonss)のパーティション列の名前を変更する操作で NULL ポインタエラーが発生する問題を修正しました。
    -   パーティションテーブルのパーティション列を変更するとDDLが[＃38530](https://github.com/pingcap/tidb/issues/38530) @ [ミョンス](https://github.com/mjonss)でハングする問題を修正しました
    -   v4.0.16からv6.4.0 [＃38980](https://github.com/pingcap/tidb/issues/38980) @ [接線](https://github.com/tangenta)にアップグレードした後に`ADMIN SHOW JOB`操作がパニックになる問題を修正
    -   `tidb_decode_key`関数がパーティションテーブル[＃39304](https://github.com/pingcap/tidb/issues/39304) @ [定義2014](https://github.com/Defined2014)のエンコードを正しく解析できない問題を修正しました
    -   ログローテーション[＃38941](https://github.com/pingcap/tidb/issues/38941) @ [xhebox](https://github.com/xhebox)中に gRPC エラーログが正しいログファイルにリダイレクトされない問題を修正しました
    -   TiKV が読み取りエンジンとして設定されていない場合に、TiDB が`BEGIN; SELECT... FOR UPDATE;`ポイントクエリに対して予期しない実行プランを生成する問題を修正[＃39344](https://github.com/pingcap/tidb/issues/39344) @ [イーサール](https://github.com/Yisaer)
    -   誤って`StreamAgg` TiFlashに押し下げると、間違った結果[＃39266](https://github.com/pingcap/tidb/issues/39266) @ [修正データベース](https://github.com/fixdb)が発生する問題を修正しました。

-   TiKV

    -   Raft Engine ctl [＃11119](https://github.com/tikv/tikv/issues/11119) @ [タボキ](https://github.com/tabokie)のエラーを修正しました
    -   tikv-ctl [＃13515](https://github.com/tikv/tikv/issues/13515) @ [国翔CN](https://github.com/guoxiangCN)で`compact raft`コマンドを実行するときに発生する`Get raft db is not allowed`エラーを修正しました
    -   TLS が有効な場合にログバックアップが機能しない問題を修正[＃13867](https://github.com/tikv/tikv/issues/13867) @ [ユジュンセン](https://github.com/YuJuncen)
    -   ジオメトリフィールドタイプ[＃13651](https://github.com/tikv/tikv/issues/13651) @ [ドヴェーデン](https://github.com/dveeden)のサポート問題を修正しました
    -   新しい照合順序が有効になっていない場合、 `LIKE`演算子の`_`非 ASCII 文字と一致しない問題を修正[＃13769](https://github.com/tikv/tikv/issues/13769) @ [ヤンケオ](https://github.com/YangKeao)
    -   `reset-to-version`コマンド[＃13829](https://github.com/tikv/tikv/issues/13829) @ [タボキ](https://github.com/tabokie)を実行すると tikv-ctl が予期せず終了する問題を修正しました

-   PD

    -   `balance-hot-region-scheduler`構成が変更されていない場合は[＃5701](https://github.com/tikv/pd/issues/5701) @ [ハンドゥンDM](https://github.com/HunDunDM)が保持されない問題を修正しました
    -   `rank-formula-version`アップグレードプロセス中にアップグレード前の構成が保持されない問題を修正[＃5698](https://github.com/tikv/pd/issues/5698) @ [ハンドゥンDM](https://github.com/HunDunDM)

-   TiFlash

    -   TiFlash [＃6159](https://github.com/pingcap/tiflash/issues/6159) @ [リデジュ](https://github.com/lidezhu)を再起動した後、デルタレイヤーの列ファイルを圧縮できない問題を修正しました。
    -   TiFlashファイルオープンOPSが[＃6345](https://github.com/pingcap/tiflash/issues/6345) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)と高すぎる問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   BRがログバックアップデータを削除するときに、削除されるべきでないデータを誤って削除してしまう問題を修正[＃38939](https://github.com/pingcap/tidb/issues/38939) @ [リーヴルス](https://github.com/Leavrth)
        -   データベースまたはテーブル[＃39150](https://github.com/pingcap/tidb/issues/39150) @ [モクイシュル28](https://github.com/MoCuishle28)照合に古いフレームワークを使用すると復元タスクが失敗する問題を修正しました
        -   Alibaba CloudとHuawei CloudがAmazon S3storageと完全に互換性がないためバックアップが失敗する問題を修正[＃39545](https://github.com/pingcap/tidb/issues/39545) @ [3ポイントシュート](https://github.com/3pointer)

    -   TiCDC

        -   PDリーダーが[＃7470](https://github.com/pingcap/tiflow/issues/7470) @ [沢民州](https://github.com/zeminzhou)でクラッシュするとTiCDCが停止する問題を修正
        -   最初にDDLステートメントを実行し、次に変更フィード[＃7682](https://github.com/pingcap/tiflow/issues/7682) @ [アズドンメン](https://github.com/asddongmen)を一時停止して再開するシナリオで発生したデータ損失を修正しました
        -   TiFlash [＃7744](https://github.com/pingcap/tiflow/issues/7744) @ [金星の上](https://github.com/overvenus)以降のバージョンがある場合に TiCDC が誤ってエラーを報告する問題を修正しました
        -   下流ネットワークが利用できない場合にシンクコンポーネントが停止する問題を修正[＃7706](https://github.com/pingcap/tiflow/issues/7706) @ [ヒック](https://github.com/hicqu)
        -   ユーザーがレプリケーションタスクを素早く削除し、同じタスク名で別のタスクを作成するとデータが失われる問題を修正[＃7657](https://github.com/pingcap/tiflow/issues/7657) @ [金星の上](https://github.com/overvenus)

    -   TiDB データ移行 (DM)

        -   上流データベースがGTIDモードを有効にしているが、データ[＃7037](https://github.com/pingcap/tiflow/issues/7037) @ [liumengya94](https://github.com/liumengya94)がない場合に`task-mode:all`タスクを開始できない問題を修正しました。
        -   既存のワーカーが終了する前に新しい DM ワーカーがスケジュールされると、データが複数回複製される問題を修正しました[＃7658](https://github.com/pingcap/tiflow/issues/7658) @ [GMHDBJD](https://github.com/GMHDBJD)
        -   アップストリームデータベースが正規表現を使用して権限[＃7645](https://github.com/pingcap/tiflow/issues/7645) @ [ランス6716](https://github.com/lance6716)を付与するときに DM 事前チェックに合格しない問題を修正しました

    -   TiDB Lightning

        -   TiDB Lightning が巨大なソースデータファイル[＃39331](https://github.com/pingcap/tidb/issues/39331) @ [dsdashun](https://github.com/dsdashun)をインポートする際のメモリリークの問題を修正しました
        -   TiDB Lightningが並列[＃39476](https://github.com/pingcap/tidb/issues/39476) @ [dsdashun](https://github.com/dsdashun)でデータをインポートするときに競合を正しく検出できない問題を修正しました

## 寄稿者 {#contributors}

TiDB コミュニティからの以下の貢献者に感謝いたします。

-   [エリヤ1](https://github.com/e1ijah1)
-   [国翔CN](https://github.com/guoxiangCN) (初回投稿者)
-   [嘉陽鄭](https://github.com/jiayang-zheng)
-   [ジフハウス](https://github.com/jiyfhust)
-   [マイクチェンウェイ](https://github.com/mikechengwei)
-   [ピンアンドビー](https://github.com/pingandb)
-   [サシャシュラ](https://github.com/sashashura)
-   [ソースリウ](https://github.com/sourcelliu)
-   [wxbty](https://github.com/wxbty)
