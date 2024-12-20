---
title: TiDB 6.5.0 Release Notes
summary: TiDB 6.5.0 の新機能、互換性の変更、改善、バグ修正について説明します。
---

# TiDB 6.5.0 リリースノート {#tidb-6-5-0-release-notes}

発売日: 2022年12月29日

TiDB バージョン: 6.5.0

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [実稼働環境への導入](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup)

TiDB 6.5.0 は長期サポートリリース (LTS) です。

TiDB [6.4.0-DMR](/releases/release-6.4.0.md)と比較して、TiDB 6.5.0 では次の主要な機能と改善が導入されています。

> **ヒント：**
>
> 以前の LTS 6.1.0 と比較して、 TiDB 6.5.0 には、 [6.2.0-DMR](/releases/release-6.2.0.md) 、 [6.3.0-DMR](/releases/release-6.3.0.md) 、 [6.4.0-DMR](/releases/release-6.4.0.md)でリリースされた新機能、改善、バグ修正も含まれています。
>
> -   6.1.0 LTS バージョンと 6.5.0 LTS バージョン間の変更点の完全なリストを取得するには、このリリース ノートに加えて、 [6.2.0-DMR リリースノート](/releases/release-6.2.0.md) 、 [6.3.0-DMR リリースノート](/releases/release-6.3.0.md) 、および[6.4.0-DMR リリースノート](/releases/release-6.4.0.md)も参照してください。
> -   6.1.0 LTS バージョンと 6.5.0 LTS バージョンの主な機能を簡単に比較するには、 [TiDBの機能](/basic-features.md)の`v6.1`と`v6.5`列目を確認してください。

-   [インデックス加速](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)機能が一般提供 (GA) され、v6.1.0 と比較してインデックス追加のパフォーマンスが約 10 倍向上します。
-   TiDB グローバルメモリ制御が GA になり、 [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)を介してメモリ消費しきい値を制御できるようになりました。
-   高性能かつグローバルに単調な[`AUTO_INCREMENT`](/auto-increment.md#mysql-compatibility-mode)列属性が、MySQL と互換性のある GA になります。
-   [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-cluster.md) TiCDC および PITR と互換性があり、GA になります。
-   より正確な[コストモデル バージョン 2](/cost-model.md#cost-model-version-2)一般に公開し、 `AND`で接続された[インデックスマージ](/explain-index-merge.md)式をサポートすることで、 TiDB オプティマイザーを強化します。
-   `JSON_EXTRACT()`機能をTiFlashにプッシュダウンすることをサポートします。
-   パスワード コンプライアンス監査要件を満たす[パスワード管理](/password-management.md)ポリシーをサポートします。
-   TiDB LightningとDumpling は、 [インポート](/tidb-lightning/tidb-lightning-data-source.md)および[輸出](/dumpling-overview.md#improve-export-efficiency-through-concurrency)圧縮された SQL ファイルと CSV ファイルをサポートします。
-   TiDB データ移行 (DM) [継続的なデータ検証](/dm/dm-continuous-data-validation.md) GA になります。
-   TiDB バックアップ &amp; リストアは、スナップショット チェックポイント バックアップをサポートし、 [ピトル](/br/br-pitr-guide.md#run-pitr)のリカバリ パフォーマンスを 50% 向上させ、一般的なシナリオでの RPO を 5 分まで短縮します。
-   [Kafka へのデータの複製](/replicate-data-to-kafka.md)の TiCDC スループットを 4000 行/秒から 35000 行/秒に向上し、レプリケーションのレイテンシーを2 秒に短縮します。
-   データのライフサイクルを管理するために行レベル[存続時間 (TTL)](/time-to-live.md)を提供します (実験的)。
-   TiCDC は、Amazon S3、Azure Blob Storage、NFS (実験的) など[変更されたログをオブジェクトstorageに複製する](/ticdc/ticdc-sink-to-cloud-storage.md)をサポートしています。

## 新機能 {#new-features}

### 構文 {#sql}

-   TiDBのインデックス追加のパフォーマンスは約10倍向上します（GA） [＃35983](https://github.com/pingcap/tidb/issues/35983) @ [ベンジャミン2037](https://github.com/benjamin2037) @ [タンジェンタ](https://github.com/tangenta)

    TiDB v6.3.0 では、インデックス作成時のバックフィル速度を向上させるための実験的機能として[インデックス加速を追加](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)導入されています。v6.5.0 ではこの機能が GA となり、デフォルトで有効になり、大規模なテーブルでのパフォーマンスは v6.1.0 よりも約 10 倍高速になると予想されます。この高速化機能は、単一の SQL ステートメントがインデックスをシリアルに追加するシナリオに適しています。複数の SQL ステートメントが並列でインデックスを追加する場合、SQL ステートメントの 1 つだけが高速化されます。

-   DDL 変更時の DML 成功率を向上させるために軽量メタデータ ロックを提供する (GA) [＃37275](https://github.com/pingcap/tidb/issues/37275) @ [翻訳:](https://github.com/wjhuang2016)

    TiDB v6.3.0 では、 [メタデータロック](/metadata-lock.md)実験的機能として導入されています。DML ステートメントによって発生する`Information schema is changed`エラーを回避するために、TiDB はテーブル メタデータの変更中に DML と DDL の優先順位を調整し、進行中の DDL が古いメタデータを持つ DML がコミットされるまで待機するようにします。v6.5.0 では、この機能が GA になり、デフォルトで有効になります。これは、さまざまな種類の DDL 変更シナリオに適しています。既存のクラスターを v6.5.0 より前のバージョンから v6.5.0 以降にアップグレードすると、TiDB はメタデータ ロックを自動的に有効にします。この機能を無効にするには、システム変数[`tidb_enable_metadata_lock`](/system-variables.md#tidb_enable_metadata_lock-new-in-v630)を`OFF`に設定します。

    詳細については[ドキュメント](/metadata-lock.md)参照してください。

-   `FLASHBACK CLUSTER TO TIMESTAMP` (GA) [＃37197](https://github.com/pingcap/tidb/issues/37197) [＃13303](https://github.com/tikv/tikv/issues/13303) @ [定義2014](https://github.com/Defined2014) @ [bb7133](https://github.com/bb7133) @ [じゃがいも](https://github.com/JmPotato) @ [コナー1996](https://github.com/Connor1996) @ [ヒューシャープ](https://github.com/HuSharp) @ [カルビンネオ](https://github.com/CalvinNeo)を使用して、クラスターを特定の時点に復元する機能をサポートします。

    v6.4.0 以降、TiDB は[`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-cluster.md)ステートメントを実験的機能として導入しました。このステートメントを使用すると、ガベージ コレクション (GC) の有効期間内の特定の時点にクラスターを復元できます。v6.5.0 では、この機能は TiCDC および PITR と互換性があり、GA になりました。この機能を使用すると、DML の誤った操作を簡単に元に戻し、数分で元のクラスターを復元し、さまざまな時点でデータをロールバックして、データが変更された正確な時刻を特定できます。

    詳細については[ドキュメント](/sql-statements/sql-statement-flashback-cluster.md)参照してください。

-   `INSERT` `UPDATE` [＃33485](https://github.com/pingcap/tidb/issues/33485)非トランザクションDMLステートメント[エキシウム](https://github.com/ekexium)完全に`DELETE`します`REPLACE`

    大規模データ処理のシナリオでは、大規模なトランザクションを含む単一の SQL ステートメントが、クラスターの安定性とパフォーマンスに悪影響を及ぼす可能性があります。非トランザクション DML ステートメントは、内部実行のために複数の SQL ステートメントに分割された DML ステートメントです。分割されたステートメントはトランザクションの原子性と分離性を損ないますが、クラスターの安定性を大幅に向上させます。TiDB は、v6.1.0 以降で非トランザクション`DELETE`ステートメントをサポートし、v6.5.0 以降で非トランザクション`INSERT` 、 `REPLACE` 、および`UPDATE`ステートメントをサポートしています。

    詳細については[非トランザクションDMLステートメント](/non-transactional-dml.md)および[`BATCH`構文](/sql-statements/sql-statement-batch.md)参照してください。

-   存続時間 (TTL) のサポート (実験的) [＃39262](https://github.com/pingcap/tidb/issues/39262) @ [lcwangchao](https://github.com/lcwangchao)

    TTL は、行レベルのデータ有効期間管理を提供します。TiDB では、TTL 属性を持つテーブルは、データ有効期間を自動的にチェックし、行レベルで期限切れのデータを削除します。TTL は、オンラインの読み取りおよび書き込みワークロードに影響を与えることなく、不要なデータを定期的かつタイムリーにクリーンアップできるように設計されています。

    詳細については[ドキュメント](/time-to-live.md)参照してください。

-   `INSERT INTO SELECT`ステートメントを使用したTiFlashクエリ結果の保存をサポート (実験的) [＃37515](https://github.com/pingcap/tidb/issues/37515) @ [ゲンリキ](https://github.com/gengliqi)

    v6.5.0 以降、TiDB は`INSERT INTO SELECT`ステートメントの`SELECT`句 (分析クエリ) をTiFlashにプッシュダウンすることをサポートしています。この方法では、 `INSERT INTO`で指定された TiDB テーブルにTiFlashクエリ結果を簡単に保存してさらに分析することができ、結果のキャッシュ (つまり、結果のマテリアライゼーション) として機能します。例:

    ```sql
    INSERT INTO t2 SELECT Mod(x,y) FROM t1;
    ```

    実験的段階では、この機能はデフォルトで無効になっています。有効にするには、 [`tidb_enable_tiflash_read_for_write_stmt`](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-new-in-v630)システム変数を`ON`に設定します。この機能では、 `INSERT INTO`で指定される結果テーブルに特別な制限はなく、その結果テーブルにTiFlashレプリカを追加するかどうかは自由です。この機能の一般的な使用シナリオは次のとおりです。

    -   TiFlashを使用して複雑な分析クエリを実行する
    -   TiFlashクエリ結果を再利用するか、同時実行性の高いオンラインリクエストを処理する
    -   入力データのサイズと比較して比較的小さい結果セットが必要であり、100 MiB 未満が望ましいです。

    詳細については[ドキュメント](/tiflash/tiflash-results-materialization.md)参照してください。

-   バインディング履歴実行プランのサポート (実験的) [＃39199](https://github.com/pingcap/tidb/issues/39199) @ [ふーふー](https://github.com/fzzf678)

    SQL ステートメントの場合、実行中のさまざまな要因により、オプティマイザが以前の最適な実行プランではなく新しい実行プランを選択することがあり、SQL パフォーマンスに影響します。この場合、最適な実行プランがまだクリアされていない場合は、SQL 実行履歴にまだ存在します。

    v6.5.0 では、TiDB は[`CREATE [GLOBAL | SESSION] BINDING`](/sql-statements/sql-statement-create-binding.md)ステートメントのバインディング オブジェクトを拡張することで、履歴実行プランのバインディングをサポートします。SQL ステートメントの実行プランが変更された場合、元の実行プランが SQL 実行履歴メモリテーブルに残っている限り (たとえば、 `statements_summary` )、 `CREATE [GLOBAL | SESSION] BINDING`ステートメントで`plan_digest`指定して元の実行プランをバインドし、SQL パフォーマンスを迅速に回復できます。この機能により、実行プランの変更の問題を処理するプロセスが簡素化され、メンテナンスの効率が向上します。

    詳細については[ドキュメント](/sql-plan-management.md#create-a-binding-according-to-a-historical-execution-plan)参照してください。

### Security {#security}

-   パスワードの複雑さのポリシー[＃38928](https://github.com/pingcap/tidb/issues/38928) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)をサポートする

    このポリシーを有効にすると、パスワードを設定するときに、TiDB はパスワードの長さ、パスワード内の大文字と小文字、数字、特殊文字が十分かどうか、パスワードが辞書と一致しているかどうか、パスワードがユーザー名と一致しているかどうかをチェックします。これにより、安全なパスワードが設定されていることが保証されます。

    TiDB は、パスワードの強度を検証するための SQL 関数[`VALIDATE_PASSWORD_STRENGTH()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_validate-password-strength)を提供します。

    詳細については[ドキュメント](/password-management.md#password-complexity-policy)参照してください。

-   パスワード有効期限ポリシー[＃38936](https://github.com/pingcap/tidb/issues/38936) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)をサポート

    TiDB は、手動による有効期限、グローバル レベルの自動有効期限、アカウント レベルの自動有効期限など、パスワード有効期限ポリシーの構成をサポートしています。このポリシーを有効にすると、パスワードを定期的に変更する必要があります。これにより、長期使用によるパスワード漏洩のリスクが軽減され、パスワードのセキュリティが向上します。

    詳細については[ドキュメント](/password-management.md#password-expiration-policy)参照してください。

-   パスワード再利用ポリシー[＃38937](https://github.com/pingcap/tidb/issues/38937) @ [学習を続ける20221](https://github.com/keeplearning20221)をサポートする

    TiDB は、グローバル レベルのパスワード再利用ポリシーやアカウント レベルのパスワード再利用ポリシーなど、パスワード再利用ポリシーの構成をサポートしています。このポリシーを有効にすると、指定された期間内に使用したパスワードや、最近使用したいくつかのパスワードは使用できません。これにより、パスワードの繰り返し使用によるパスワード漏洩のリスクが軽減され、パスワードのセキュリティが向上します。

    詳細については[ドキュメント](/password-management.md#password-reuse-policy)参照してください。

-   ログイン失敗の追跡と一時的なアカウントロックポリシー[＃38938](https://github.com/pingcap/tidb/issues/38938) @ [最後の切歯](https://github.com/lastincisor)をサポート

    このポリシーを有効にすると、TiDB に連続して間違ったパスワードでログインすると、アカウントが一時的にロックされます。ロック時間が終了すると、アカウントは自動的にロック解除されます。

    詳細については[ドキュメント](/password-management.md#failed-login-tracking-and-temporary-account-locking-policy)参照してください。

### 可観測性 {#observability}

-   TiDBダッシュボードはKubernetes上に独立したPod [＃1447](https://github.com/pingcap/tidb-dashboard/issues/1447) @ [サバピン](https://github.com/SabaPing)としてデプロイできます。

    TiDB v6.5.0 (以降) およびTiDB Operator v1.4.0 (以降) では、Kubernetes 上の独立した Pod として TiDB Dashboard をデプロイできます。TiDB TiDB Operator を使用すると、この Pod の IP アドレスにアクセスして TiDB Dashboard を起動できます。

    TiDB ダッシュボードを個別に展開すると、次の利点が得られます。

    -   TiDB ダッシュボードの計算作業は PD ノードに負担をかけません。これにより、より安定したクラスター操作が保証されます。
    -   PD ノードが利用できない場合でも、ユーザーは診断のために TiDB ダッシュボードにアクセスできます。
    -   インターネット上の TiDB ダッシュボードへのアクセスには、PD の特権インターフェイスは関係しません。そのため、クラスターのセキュリティ リスクが軽減されます。

    詳細については[ドキュメント](https://docs.pingcap.com/tidb-in-kubernetes/dev/get-started#deploy-tidb-dashboard-independently)参照してください。

-   パフォーマンス概要ダッシュボードにTiFlashおよび CDC (変更データ キャプチャ) パネル[＃39230](https://github.com/pingcap/tidb/issues/39230) @ [dbsid](https://github.com/dbsid)が追加されました

    v6.1.0 以降、TiDB は Grafana にパフォーマンス概要ダッシュボードを導入しました。このダッシュボードは、TiDB、TiKV、PD の全体的なパフォーマンス診断のためのシステムレベルのエントリを提供します。v6.5.0 では、パフォーマンス概要ダッシュボードにTiFlashと CDC パネルが追加されました。v6.5.0 以降では、これらのパネルを使用して、パフォーマンス概要ダッシュボードを使用して TiDB クラスター内のすべてのコンポーネントのパフォーマンスを分析できます。

    TiFlashパネルと CDC パネルは、 TiFlashおよび TiCDC の監視情報を再編成します。これにより、 TiFlashおよび TiCDC のパフォーマンスの問題の分析とトラブルシューティングの効率が大幅に向上します。

    -   [TiFlashパネル](/grafana-performance-overview-dashboard.md#tiflash)では、 TiFlashクラスターのリクエスト タイプ、レイテンシー分析、リソース使用状況の概要を簡単に表示できます。
    -   [CDCパネル](/grafana-performance-overview-dashboard.md#cdc)では、TiCDC クラスターの健全性、レプリケーションのレイテンシー、データ フロー、ダウンストリームの書き込みレイテンシーを簡単に確認できます。

    詳細については[ドキュメント](/performance-tuning-methods.md)参照してください。

### パフォーマンス {#performance}

-   [インデックスマージ](/glossary.md#index-merge) `AND` [＃39333](https://github.com/pingcap/tidb/issues/39333) @ [グオシャオゲ](https://github.com/guo-shaoge) @ [時間と運命](https://github.com/time-and-fate) @ [海蘭湖](https://github.com/hailanwhu)で接続された式をサポートします

    v6.5.0 より前の TiDB では、 `OR`で接続されたフィルタ条件に対してのみインデックス マージの使用がサポートされていました。v6.5.0 以降、TiDB では`WHERE`句で`AND`で接続されたフィルタ条件に対してインデックス マージの使用がサポートされるようになりました。このようにして、TiDB のインデックス マージは、クエリ フィルタ条件のより一般的な組み合わせをカバーできるようになり、union ( `OR` ) 関係に限定されなくなりました。現在の v6.5.0 バージョンでは、オプティマイザによって自動的に選択される`OR`条件でのインデックス マージのみがサポートされています。11 条件のインデックス マージを有効にするには、 `AND`ヒント[`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)使用する必要があります。

    インデックスマージの詳細については、 [v5.4.0 リリースノート](/releases/release-5.4.0.md#performance)と[インデックスのマージの説明](/explain-index-merge.md)参照してください。

-   以下のJSON関数をTiFlash [＃39458](https://github.com/pingcap/tidb/issues/39458) @ [いびん87](https://github.com/yibin87)にプッシュダウンするサポート

    -   `->`
    -   `->>`
    -   `JSON_EXTRACT()`

    JSON 形式は、アプリケーション データ モデリングに柔軟な方法を提供します。そのため、データ交換やデータstorageに JSON 形式を使用するアプリケーションが増えています。JSON関数をTiFlashにプッシュダウンすることで、JSON タイプのデータ分析の効率を向上させ、よりリアルタイムな分析シナリオに TiDB を使用できるようになります。

-   以下の文字列関数をTiFlash [＃6115](https://github.com/pingcap/tiflash/issues/6115) @ [翻訳者](https://github.com/xzhangxian1008)にプッシュダウンする機能をサポートします。

    -   `regexp_like`
    -   `regexp_instr`
    -   `regexp_substr`

-   [ビュー](/views.md) [＃37887](https://github.com/pingcap/tidb/issues/37887) @ [思い出させる](https://github.com/Reminiscent)で実行プラン生成に干渉するグローバル オプティマイザ ヒントをサポートします。

    一部のビュー アクセス シナリオでは、最適なパフォーマンスを実現するために、オプティマイザ ヒントを使用してビュー内のクエリの実行プランに干渉する必要があります。v6.5.0 以降、TiDB はビュー内のクエリ ブロックにグローバル ヒントを追加し、クエリで定義されたヒントをビューで有効にできるようになりました。この機能により、ネストされたビューを含む複雑な SQL ステートメントにヒントを挿入できるようになり、実行プランの制御が強化され、複雑なステートメントのパフォーマンスが安定します。グローバル ヒントを使用するには、 [クエリブロックに名前を付ける](/optimizer-hints.md#step-1-define-the-query-block-name-of-the-view-using-the-qb_name-hint)と[ヒント参照を指定する](/optimizer-hints.md#step-2-add-the-target-hints)実行する必要があります。

    詳細については[ドキュメント](/optimizer-hints.md#hints-that-take-effect-globally)参照してください。

-   [パーティションテーブル](/partitioned-table.md)から TiKV [＃26166](https://github.com/pingcap/tidb/issues/26166) @ [ウィノロス](https://github.com/winoros)へのソート操作のプッシュダウンをサポート

    [パーティションテーブル](/partitioned-table.md)機能は v6.1.0 から GA になっていますが、TiDB は継続的にパフォーマンスを改善しています。v6.5.0 では、TiDB は計算とフィルタリングのために`ORDER BY`や`LIMIT`などのソート操作を TiKV にプッシュダウンすることをサポートしています。これにより、ネットワーク I/O オーバーヘッドが削減され、パーティション テーブルを使用する場合の SQL パフォーマンスが向上します。

-   オプティマイザーはより正確なコストモデルバージョン2（GA） [＃35240](https://github.com/pingcap/tidb/issues/35240) @ [qw4990](https://github.com/qw4990)を導入しました

    TiDB v6.2.0 では、 [コストモデル バージョン 2](/cost-model.md#cost-model-version-2)実験的機能として導入されています。このモデルは、より正確なコスト推定方法を使用して、オプティマイザーが最適な実行プランを選択できるようにします。特にTiFlashが展開されている場合、コスト モデル バージョン 2 は適切なstorageエンジンを自動的に選択し、手動による介入を大幅に回避します。一定期間の実際のシーンでのテストの後、このモデルは v6.5.0 で GA になります。v6.5.0 以降、新しく作成されたクラスターはデフォルトでコスト モデル バージョン 2 を使用します。クラスターを v6.5.0 にアップグレードする場合、コスト モデル バージョン 2 によってクエリ プランが変更される可能性があるため、十分なパフォーマンス テストを行った後、 [`tidb_cost_model_version = 2`](/system-variables.md#tidb_cost_model_version-new-in-v620)変数を設定して新しいコスト モデルを使用できます。

    コスト モデル バージョン 2 は、TiDB オプティマイザーの全体的な機能を大幅に向上させ、TiDB をより強力な HTAP データベースへと進化させる、一般利用可能な機能になります。

    詳細については[ドキュメント](/cost-model.md#cost-model-version-2)参照してください。

-   TiFlashはテーブル行数[＃37165](https://github.com/pingcap/tidb/issues/37165) @ [エルサ0520](https://github.com/elsa0520)を取得する操作を最適化します

    データ分析のシナリオでは、フィルター条件なしで`COUNT(*)`介してテーブルの実際の行数を取得することは一般的な操作です。v6.5.0 では、 TiFlash は`COUNT(*)`の書き換えを最適化し、最短の列定義を持つ非 NULL 列を自動的に選択して行数をカウントします。これにより、TiFlashの I/O 操作の数を効果的に削減し、行数取得の実行効率を向上させることができます。

### 安定性 {#stability}

-   グローバルメモリ制御機能はGA [＃37816](https://github.com/pingcap/tidb/issues/37816) @ [うわー](https://github.com/wshwsh12)になりました

    v6.4.0 以降、TiDB は実験的機能としてグローバルメモリ制御を導入しました。v6.5.0 では GA となり、メインメモリの消費量を追跡できるようになりました。グローバルメモリの消費量が[`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)で定義されたしきい値に達すると、TiDB は GC または SQL 操作のキャンセルによってメモリ使用量を制限し、安定性を確保しようとします。

    セッション内のトランザクションによって消費されるメモリ(最大値は以前は構成項目[`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit)によって設定されていました) は、メモリ管理モジュールによって追跡されるようになりました。単一セッションのメモリ消費量がシステム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)によって定義されたしきい値に達すると、システム変数[`tidb_mem_oom_action`](/system-variables.md#tidb_mem_oom_action-new-in-v610)によって定義された動作がトリガーされます (デフォルトは`CANCEL` 、つまり操作のキャンセルです)。前方互換性を確保するために、 [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit)がデフォルト以外の値として構成されている場合でも、TiDB はトランザクションが`txn-total-size-limit`によって設定されたメモリを使用できるようにします。

    TiDB v6.5.0 以降を使用している場合は、 [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit)削除し、トランザクションのメモリ使用量に個別の制限を設定しないことを推奨します。代わりに、システム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)と[`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)使用してグローバルメモリを管理し、メモリ使用の効率を向上させることができます。

    詳細については[ドキュメント](/configure-memory-usage.md)参照してください。

### 使いやすさ {#ease-of-use}

-   `EXPLAIN ANALYZE`出力[＃5926](https://github.com/pingcap/tiflash/issues/5926) @ [ホンユンヤン](https://github.com/hongyunyan)のTiFlash `TableFullScan`演算子の実行情報を精緻化する

    `EXPLAIN ANALYZE`ステートメントは、実行プランと実行時統計を出力するために使用されます。v6.5.0 では、 TiFlash はDMFile 関連の実行情報を追加することで、 `TableFullScan`演算子の実行情報を改良しました。TiFlash データ スキャン ステータス情報がより直感的に表示されるようになり、 TiFlash のTiFlashをより簡単に分析できるようになりました。

    詳細については[ドキュメント](/sql-statements/sql-statement-explain-analyze.md)参照してください。

-   実行プランのJSON形式[＃39261](https://github.com/pingcap/tidb/issues/39261) @ [ふーふー](https://github.com/fzzf678)での出力をサポート

    v6.5.0 では、TiDB は実行プランの出力形式を拡張しました。3 `EXPLAIN`で`FORMAT = "tidb_json"`指定することで、SQL 実行プランを JSON 形式で出力できます。この機能により、SQL デバッグ ツールや診断ツールは実行プランをより便利かつ正確に読み取ることができるため、SQL 診断やチューニングの使いやすさが向上します。

    詳細については[ドキュメント](/sql-statements/sql-statement-explain.md)参照してください。

### MySQL 互換性 {#mysql-compatibility}

-   高性能かつグローバルに単調な`AUTO_INCREMENT`列属性 (GA) [＃38442](https://github.com/pingcap/tidb/issues/38442) @ [天菜まお](https://github.com/tiancaiamao)をサポート

    v6.4.0 以降、TiDB は`AUTO_INCREMENT` MySQL 互換モードを実験的機能として導入しました。このモードでは、すべての TiDB インスタンスで ID が単調に増加するようにする集中型の自動増分 ID 割り当てサービスが導入されます。この機能により、自動増分 ID によるクエリ結果の並べ替えが容易になります。v6.5.0 では、この機能が GA になります。この機能を使用するテーブルの挿入 TPS は 20,000 を超えると予想され、この機能は単一のテーブルとクラスター全体の書き込みスループットを向上させるためのエラスティック スケーリングをサポートします。MySQL 互換モードを使用するには、テーブルの作成時に`AUTO_ID_CACHE`から`1`に設定する必要があります。次に例を示します。

    ```sql
    CREATE TABLE t(a int AUTO_INCREMENT key) AUTO_ID_CACHE 1;
    ```

    詳細については[ドキュメント](/auto-increment.md#mysql-compatibility-mode)参照してください。

### データ移行 {#data-migration}

-   gzip、snappy、zstd 圧縮形式での SQL および CSV ファイルのエクスポートとインポートをサポート[＃38514](https://github.com/pingcap/tidb/issues/38514) @ [リチュンジュ](https://github.com/lichunzhu)

    Dumpling は、gzip、snappy、zstd の圧縮形式で圧縮された SQL および CSV ファイルへのデータのエクスポートをサポートしています。TiDB TiDB Lightning は、これらの形式で圧縮されたファイルのインポートもサポートしています。

    これまでは、CSV ファイルや SQL ファイルを保存するために、データのエクスポートやインポートに大量のstorageスペースを用意する必要があり、storageコストが高くなっていました。この機能のリリースにより、データ ファイルを圧縮することで、storageコストを大幅に削減できます。

    詳細については[ドキュメント](/dumpling-overview.md#improve-export-efficiency-through-concurrency)参照してください。

-   binlog解析機能の最適化[＃924](https://github.com/pingcap/dm/issues/924) @ [翻訳者](https://github.com/GMHDBJD)

    TiDB は、移行タスクに含まれないスキーマとテーブルのbinlogイベントをフィルター処理できるため、解析の効率と安定性が向上します。このポリシーは、v6.5.0 ではデフォルトで有効になります。追加の構成は必要ありません。

    以前は、少数のテーブルのみが移行された場合でも、上流のbinlogファイル全体を解析する必要がありました。移行する必要のないbinlogファイル内のテーブルのbinlogイベントも解析する必要があり、効率的ではありませんでした。一方、これらのbinlogイベントが解析をサポートしていない場合、タスクは失敗します。移行タスク内のテーブルのbinlogイベントのみを解析することで、 binlog解析の効率が大幅に向上し、タスクの安定性が向上します。

-   TiDB Lightningのディスク クォータは GA [＃446](https://github.com/pingcap/tidb-lightning/issues/446) @ [ブチュイトウデゴウ](https://github.com/buchuitoudegou)です

    TiDB Lightningのディスク クォータを設定できます。ディスク クォータが十分でない場合、 TiDB Lightning はソース データの読み取りと一時ファイルの書き込みを停止します。代わりに、まずソートされたキーと値を TiKV に書き込み、その後TiDB Lightning がローカルの一時ファイルを削除した後にインポート プロセスを続行します。

    以前は、 TiDB Lightning が物理モードを使用してデータをインポートすると、生データのエンコード、並べ替え、分割のためにローカル ディスクに大量の一時ファイルが作成されていました。ローカル ディスクの容量が不足すると、 TiDB Lightning はファイルへの書き込みに失敗したためにエラーで終了していました。この機能により、 TiDB Lightningタスクはローカル ディスクの上書きを回避できます。

    詳細については[ドキュメント](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#configure-disk-quota-new-in-v620)参照してください。

-   DM における継続的なデータ検証は GA [＃4426](https://github.com/pingcap/tiflow/issues/4426) @ [D3ハンター](https://github.com/D3Hunter)です

    アップストリーム データベースからダウンストリーム データベースに増分データを移行するプロセスでは、データ フローによってエラーやデータ損失が発生する可能性がわずかにあります。クレジットや証券ビジネスなど、強力なデータ整合性が求められるシナリオでは、移行後にデータに対してフル ボリューム チェックサムを実行して、データの整合性を確保できます。ただし、一部の増分レプリケーション シナリオでは、アップストリームとダウンストリームのデータが絶えず変化しているため、アップストリームとダウンストリームの書き込みは継続的かつ中断されず、すべてのデータに対して整合性チェックを実行することが困難です。

    以前は、完全なデータを検証するために業務を中断する必要があり、業務に影響が出ていました。この機能により、業務を中断することなく増分データ検証を実行できるようになりました。

    詳細については[ドキュメント](/dm/dm-continuous-data-validation.md)参照してください。

### TiDBデータ共有サブスクリプション {#tidb-data-share-subscription}

-   TiCDC は変更されたログをstorageシンクに複製することをサポートしています (実験的) [＃6797](https://github.com/pingcap/tiflow/issues/6797) @ [趙新宇](https://github.com/zhaoxinyu)

    TiCDC は、Amazon S3、Azure Blob Storage、NFS、およびその他の S3 互換storageサービスへの変更ログの複製をサポートしています。クラウドstorageは価格が手頃で使いやすいです。Kafka を使用していない場合は、storageシンクを使用できます。TiCDC は変更されたログをファイルに保存し、それをstorageシステムに送信します。storageシステムから、コンシューマー プログラムは新しく生成された変更ログ ファイルを定期的に読み取ります。

    storageシンクは、canal-json 形式と CSV 形式の変更ログをサポートします。詳細については、 [ドキュメント](/ticdc/ticdc-sink-to-cloud-storage.md)参照してください。

-   TiCDCは2つのクラスター間の双方向レプリケーションをサポートします[＃38587](https://github.com/pingcap/tidb/issues/38587) @ [雄吉偉](https://github.com/xiongjiwei) @ [アズドンメン](https://github.com/asddongmen)

    TiCDC は、2 つの TiDB クラスター間の双方向レプリケーションをサポートします。アプリケーション用に地理的に分散された複数のアクティブなデータ センターを構築する必要がある場合は、この機能をソリューションとして使用できます。1 つの TiDB クラスターから別の TiDB クラスターへの TiCDC 変更フィードに`bdr-mode = true`パラメータを構成すると、2 つの TiDB クラスター間の双方向データ レプリケーションを実現できます。

    詳細については[ドキュメント](/ticdc/ticdc-bidirectional-replication.md)参照してください。

-   TiCDC は TLS のオンライン[＃7908](https://github.com/pingcap/tiflow/issues/7908) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)更新をサポートします

    データベース システムのセキュリティを維持するには、システムで使用される証明書の有効期限ポリシーを設定する必要があります。有効期限が切れると、システムは新しい証明書を必要とします。TiCDC v6.5.0 は、TLS 証明書のオンライン更新をサポートしています。レプリケーション タスクを中断することなく、TiCDC は手動で介入することなく、証明書を自動的に検出して更新できます。

-   TiCDCのパフォーマンスが大幅に向上[＃7540](https://github.com/pingcap/tiflow/issues/7540) [＃7478](https://github.com/pingcap/tiflow/issues/7478) [＃7532](https://github.com/pingcap/tiflow/issues/7532) @ [スドジ](https://github.com/sdojjy) @ [3エースショーハンド](https://github.com/3AceShowHand)

    TiDB クラスターのテスト シナリオでは、TiCDC のパフォーマンスが大幅に向上しました。具体的には、シナリオ[Kafka へのデータの複製](/replicate-data-to-kafka.md)では、単一の TiCDC が処理できる行変更の最大数は 30K 行/秒に達し、レプリケーションのレイテンシーは 10 秒に短縮されました。TiKV および TiCDC のローリング アップグレード中でも、レプリケーションのレイテンシーは30 秒未満です。

    災害復旧 (DR) シナリオでは、TiCDC の再実行ログと同期ポイントを有効にすると、TiCDC スループットを 4000 行/秒から 35000 行/秒に向上でき、レプリケーションのレイテンシーを2 秒に制限できます。

### バックアップと復元 {#backup-and-restore}

-   TiDB バックアップ &amp; リストアはスナップショット チェックポイント バックアップ[＃38647](https://github.com/pingcap/tidb/issues/38647) @ [リーヴルス](https://github.com/Leavrth)をサポートします

    TiDB スナップショット バックアップは、チェックポイントからのバックアップの再開をサポートします。バックアップと復元 (BR) で回復可能なエラーが発生すると、バックアップが再試行されます。ただし、再試行が複数回失敗すると、 BR は終了します。チェックポイント バックアップ機能を使用すると、数十分のネットワーク障害など、回復可能な障害の再試行が長くなります。

    BR終了後 1 時間以内にシステムを障害から回復しない場合、バックアップ対象のスナップショット データが GC メカニズムによってリサイクルされ、バックアップが失敗する可能性があることに注意してください。詳細については、 [ドキュメント](/br/br-checkpoint-backup.md#backup-retry-must-be-prior-to-gc)参照してください。

-   PITRのパフォーマンスが[ジョッカウ](https://github.com/joccau)で著しく向上

    ログ復元ステージでは、1 つの TiKV の復元速度は 9 MiB/s に達し、これは以前より 50% 高速です。復元速度はスケーラブルで、DR シナリオの RTO は大幅に短縮されます。DR シナリオの RPO は 5 分と短くなります。通常のクラスター運用および保守 (OM) では、たとえばローリング アップグレードが実行されるか、1 つの TiKV のみがダウンすると、RPO は 5 分になります。

-   TiKV- BR GA: RawKV [＃67](https://github.com/tikv/migration/issues/67) @ [ピンギュ](https://github.com/pingyu) @ [ハオジンミン](https://github.com/haojinming)のバックアップと復元をサポート

    TiKV- BR は、TiKV クラスターで使用されるバックアップおよび復元ツールです。TiKV と PD は、TiDB なしで使用すると KV データベースを構成でき、これを RawKV と呼びます。TiKV- BR は、 RawKV を使用する製品のデータ バックアップと復元をサポートします。TiKV- BR は、 TiKV クラスターの[`api-version`](/tikv-configuration-file.md#api-version-new-in-v610) `API V1`から`API V2`にアップグレードすることもできます。

    詳細については[ドキュメント](https://tikv.org/docs/latest/concepts/explore-tikv-features/backup-restore/)参照してください。

## 互換性の変更 {#compatibility-changes}

### システム変数 {#system-variables}

| 変数名                                                                                                                       | タイプを変更   | 説明                                                                                                                                                                                                                                                                                                                                                   |
| ------------------------------------------------------------------------------------------------------------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `tidb_enable_amend_pessimistic_txn`                                                                                       | 非推奨      | v6.5.0 以降では、この変数は非推奨となり、TiDB は`Information schema is changed`エラーを回避するためにデフォルトで[メタデータロック](/metadata-lock.md)機能を使用します。                                                                                                                                                                                                                                 |
| [`tidb_enable_outer_join_reorder`](/system-variables.md#tidb_enable_outer_join_reorder-new-in-v610)                       | 修正済み     | さらにテストを行った後、デフォルト値を`OFF`から`ON`に変更します。つまり、 [結合したテーブルの再配置](/join-reorder.md)アルゴリズムの Outer Join のサポートがデフォルトで有効になります。                                                                                                                                                                                                                                    |
| [`tidb_cost_model_version`](/system-variables.md#tidb_cost_model_version-new-in-v620)                                     | 修正済み     | さらにテストを行った後、デフォルト値を`1`から`2`に変更します。つまり、デフォルトでは、インデックス選択と演算子選択にコスト モデル バージョン 2 が使用されることになります。                                                                                                                                                                                                                                                          |
| [`tidb_enable_gc_aware_memory_track`](/system-variables.md#tidb_enable_gc_aware_memory_track)                             | 修正済み     | デフォルト値を`ON`から`OFF`に変更します。GC 対応メモリトラックはテストで不正確であることが判明し、追跡されるメモリサイズが大きくなりすぎるため、メモリトラックは無効になっています。また、 Golang 1.19 では、GC 対応メモリトラックによって追跡されるメモリは、全体のメモリに大きな影響を与えません。                                                                                                                                                                                     |
| [`tidb_enable_metadata_lock`](/system-variables.md#tidb_enable_metadata_lock-new-in-v630)                                 | 修正済み     | さらにテストを行った後、デフォルト値を`OFF`から`ON`に変更します。つまり、メタデータ ロック機能はデフォルトで有効になります。                                                                                                                                                                                                                                                                                  |
| [`tidb_enable_tiflash_read_for_write_stmt`](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-new-in-v630)     | 修正済み     | v6.5.0 から有効になります。 `INSERT` 、 `DELETE` 、および`UPDATE`を含む SQL ステートメントの読み取り操作をTiFlashにプッシュダウンできるかどうかを制御します。デフォルト値は`OFF`です。                                                                                                                                                                                                                                |
| [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)                               | 修正済み     | さらにテストを行った後、デフォルト値を`OFF`から`ON`に変更します。つまり、 `ADD INDEX`と`CREATE INDEX`の加速がデフォルトで有効になります。                                                                                                                                                                                                                                                               |
| [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)                                                       | 修正済み     | TiDB v6.5.0 より前のバージョンでは、この変数はクエリのメモリクォータのしきい値を設定するために使用されます。TiDB v6.5.0 以降のバージョンでは、DML ステートメントのメモリをより正確に制御するために、この変数はセッションのメモリクォータのしきい値を設定するために使用されます。                                                                                                                                                                                               |
| [`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40)                                                  | 修正済み     | v6.5.0 以降では、TiDB ノード間の負荷分散を最適化するために、この変数が`closest-adaptive`に設定され、読み取り要求の推定結果が[`tidb_adaptive_closest_read_threshold`](/system-variables.md#tidb_adaptive_closest_read_threshold-new-in-v630)以上の場合、 `closest-adaptive`構成が有効になる TiDB ノードの数が各アベイラビリティーゾーンで制限されます。この数は、TiDB ノードが最も少ないアベイラビリティーゾーンの TiDB ノードの数と常に同じになり、他の TiDB ノードは自動的にリーダー レプリカから読み取ります。 |
| [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)                                   | 修正済み     | デフォルト値を`0`から`80%`に変更します。TiDB グローバルメモリ制御が GA になると、このデフォルト値の変更により、メモリ制御がデフォルトで有効になり、TiDB インスタンスのメモリ制限がデフォルトで合計メモリの 80% に設定されます。                                                                                                                                                                                                                        |
| [`default_password_lifetime`](/system-variables.md#default_password_lifetime-new-in-v650)                                 | 新しく追加された | パスワードの自動有効期限のグローバル ポリシーを設定し、ユーザーにパスワードを定期的に変更するよう要求します。デフォルト値`0`は、パスワードが期限切れにならないことを示します。                                                                                                                                                                                                                                                            |
| [`disconnect_on_expired_password`](/system-variables.md#disconnect_on_expired_password-new-in-v650)                       | 新しく追加された | パスワードの有効期限が切れたときに TiDB がクライアント接続を切断するかどうかを示します。この変数は読み取り専用です。                                                                                                                                                                                                                                                                                        |
| [`password_history`](/system-variables.md#password_history-new-in-v650)                                                   | 新しく追加された | この変数は、パスワード変更回数に基づいて TiDB がパスワードの再利用を制限できるようにするパスワード再利用ポリシーを確立するために使用されます。デフォルト値`0`は、パスワード変更回数に基づくパスワード再利用ポリシーを無効にすることを意味します。                                                                                                                                                                                                                        |
| [`password_reuse_interval`](/system-variables.md#password_reuse_interval-new-in-v650)                                     | 新しく追加された | この変数は、経過時間に基づいて TiDB がパスワードの再利用を制限できるようにするパスワード再利用ポリシーを確立するために使用されます。デフォルト値`0`は、経過時間に基づくパスワード再利用ポリシーを無効にすることを意味します。                                                                                                                                                                                                                                  |
| [`tidb_auto_build_stats_concurrency`](/system-variables.md#tidb_auto_build_stats_concurrency-new-in-v650)                 | 新しく追加された | この変数は、統計の自動更新を実行する同時実行性を設定するために使用されます。デフォルト値は`1`です。                                                                                                                                                                                                                                                                                                  |
| [`tidb_cdc_write_source`](/system-variables.md#tidb_cdc_write_source-new-in-v650)                                         | 新しく追加された | この変数が 0 以外の値に設定されている場合、このセッションで書き込まれたデータは TiCDC によって書き込まれたものと見なされます。この変数は TiCDC によってのみ変更できます。いかなる場合でも、この変数を手動で変更しないでください。                                                                                                                                                                                                                            |
| [`tidb_index_merge_intersection_concurrency`](/system-variables.md#tidb_index_merge_intersection_concurrency-new-in-v650) | 新しく追加された | インデックス マージが実行する交差操作の最大同時実行性を設定します。これは、TiDB が動的プルーニング モードでパーティション テーブルにアクセスする場合にのみ有効です。                                                                                                                                                                                                                                                               |
| [`tidb_source_id`](/system-variables.md#tidb_source_id-new-in-v650)                                                       | 新しく追加された | この変数は、 [双方向レプリケーション](/ticdc/ticdc-bidirectional-replication.md)クラスター内の異なるクラスター ID を構成するために使用されます。                                                                                                                                                                                                                                                    |
| [`tidb_sysproc_scan_concurrency`](/system-variables.md#tidb_sysproc_scan_concurrency-new-in-v650)                         | 新しく追加された | この変数は、TiDB が内部 SQL ステートメント (統計の自動更新など) を実行するときに実行されるスキャン操作の同時実行性を設定するために使用されます。デフォルト値は`1`です。                                                                                                                                                                                                                                                         |
| [`tidb_ttl_delete_batch_size`](/system-variables.md#tidb_ttl_delete_batch_size-new-in-v650)                               | 新しく追加された | この変数は、TTL ジョブ内の`DELETE`のトランザクションで削除できる行の最大数を設定するために使用されます。                                                                                                                                                                                                                                                                                           |
| [`tidb_ttl_delete_rate_limit`](/system-variables.md#tidb_ttl_delete_rate_limit-new-in-v650)                               | 新しく追加された | この変数は、TTL ジョブの単一ノードで 1 秒あたりに許可される`DELETE`ステートメントの最大数を制限するために使用されます。この変数が`0`に設定されている場合、制限は適用されません。                                                                                                                                                                                                                                                    |
| [`tidb_ttl_delete_worker_count`](/system-variables.md#tidb_ttl_delete_worker_count-new-in-v650)                           | 新しく追加された | この変数は、各 TiDB ノード上の TTL ジョブの最大同時実行数を設定するために使用されます。                                                                                                                                                                                                                                                                                                    |
| [`tidb_ttl_job_enable`](/system-variables.md#tidb_ttl_job_enable-new-in-v650)                                             | 新しく追加された | この変数は、TTL ジョブを有効にするかどうかを制御するために使用されます。 `OFF`に設定すると、TTL 属性を持つすべてのテーブルで期限切れのデータのクリーンアップが自動的に停止されます。                                                                                                                                                                                                                                                    |
| `tidb_ttl_job_run_interval`                                                                                               | 新しく追加された | この変数は、バックグラウンドでの TTL ジョブのスケジュール間隔を制御するために使用されます。たとえば、現在の値が`1h0m0s`に設定されている場合、TTL 属性を持つ各テーブルは、期限切れのデータを 1 時間ごとにクリーンアップします。                                                                                                                                                                                                                            |
| [`tidb_ttl_job_schedule_window_start_time`](/system-variables.md#tidb_ttl_job_schedule_window_start_time-new-in-v650)     | 新しく追加された | この変数は、バックグラウンドでの TTL ジョブのスケジュール ウィンドウの開始時間を制御するために使用されます。この変数の値を変更する場合、ウィンドウが小さいと期限切れのデータのクリーンアップが失敗する可能性があるので注意してください。                                                                                                                                                                                                                              |
| [`tidb_ttl_job_schedule_window_end_time`](/system-variables.md#tidb_ttl_job_schedule_window_end_time-new-in-v650)         | 新しく追加された | この変数は、バックグラウンドでの TTL ジョブのスケジュール ウィンドウの終了時間を制御するために使用されます。この変数の値を変更する場合、ウィンドウが小さいと期限切れのデータのクリーンアップが失敗する可能性があるので注意してください。                                                                                                                                                                                                                              |
| [`tidb_ttl_scan_batch_size`](/system-variables.md#tidb_ttl_scan_batch_size-new-in-v650)                                   | 新しく追加された | この変数は、TTL ジョブで期限切れのデータをスキャンするために使用される`SELECT`ステートメントのそれぞれ`LIMIT`の値を設定するために使用されます。                                                                                                                                                                                                                                                                    |
| [`tidb_ttl_scan_worker_count`](/system-variables.md#tidb_ttl_scan_worker_count-new-in-v650)                               | 新しく追加された | この変数は、各 TiDB ノード上の TTL スキャン ジョブの最大同時実行数を設定するために使用されます。                                                                                                                                                                                                                                                                                               |
| [`validate_password.check_user_name`](/system-variables.md#validate_passwordcheck_user_name-new-in-v650)                  | 新しく追加された | パスワードの複雑さのチェックにおけるチェック項目。パスワードがユーザー名と一致するかどうかをチェックします。この変数は[`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650)が有効になっている場合にのみ有効になります。デフォルト値は`ON`です。                                                                                                                                                                |
| [`validate_password.dictionary`](/system-variables.md#validate_passworddictionary-new-in-v650)                            | 新しく追加された | パスワードの複雑さチェックのチェック項目。パスワードが辞書内のいずれかの単語と一致するかどうかをチェックします。この変数は、 [`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650)が有効で、 [`validate_password.policy`](/system-variables.md#validate_passwordpolicy-new-in-v650) `2` (STRONG) に設定されている場合にのみ有効になります。デフォルト値は`""`です。                                                   |
| [`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650)                                    | 新しく追加された | この変数は、パスワードの複雑さのチェックを実行するかどうかを制御します。この変数を`ON`に設定すると、パスワードを設定するときに TiDB はパスワードの複雑さのチェックを実行します。デフォルト値は`OFF`です。                                                                                                                                                                                                                                         |
| [`validate_password.length`](/system-variables.md#validate_passwordlength-new-in-v650)                                    | 新しく追加された | パスワードの複雑さのチェック項目。パスワードの長さが十分かどうかをチェックします。デフォルトでは、パスワードの最小長は`8`です。この変数は、 [`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650)が有効な場合にのみ有効になります。                                                                                                                                                                      |
| [`validate_password.mixed_case_count`](/system-variables.md#validate_passwordmixed_case_count-new-in-v650)                | 新しく追加された | パスワードの複雑さチェックのチェック項目。パスワードに十分な大文字と小文字が含まれているかどうかをチェックします。この変数は、 [`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650)が有効で、 [`validate_password.policy`](/system-variables.md#validate_passwordpolicy-new-in-v650) `1` (MEDIUM) 以上に設定されている場合にのみ有効になります。デフォルト値は`1`です。                                                 |
| [`validate_password.number_count`](/system-variables.md#validate_passwordnumber_count-new-in-v650)                        | 新しく追加された | パスワードの複雑さチェックのチェック項目。パスワードに十分な数字が含まれているかどうかをチェックします。この変数は、 [`validate_password.enable`](/system-variables.md#password_reuse_interval-new-in-v650)が有効で、 [`validate_password.policy`](/system-variables.md#validate_passwordpolicy-new-in-v650) `1` (MEDIUM) 以上に設定されている場合にのみ有効になります。デフォルト値は`1`です。                                                      |
| [`validate_password.policy`](/system-variables.md#validate_passwordpolicy-new-in-v650)                                    | 新しく追加された | この変数は、パスワードの複雑さのチェックのポリシーを制御します。値は`0` 、 `1` 、または`2` (LOW、MEDIUM、または STRONG に対応) です。この変数は、 [`validate_password.enable`](/system-variables.md#password_reuse_interval-new-in-v650)が有効な場合にのみ有効になります。デフォルト値は`1`です。                                                                                                                                       |
| [`validate_password.special_char_count`](/system-variables.md#validate_passwordspecial_char_count-new-in-v650)            | 新しく追加された | パスワードの複雑さチェックのチェック項目。パスワードに十分な特殊文字が含まれているかどうかをチェックします。この変数は、 [`validate_password.enable`](/system-variables.md#password_reuse_interval-new-in-v650)が有効で、 [`validate_password.policy`](/system-variables.md#validate_passwordpolicy-new-in-v650) `1` (MEDIUM) 以上に設定されている場合にのみ有効になります。デフォルト値は`1`です。                                                    |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                            | タイプを変更   | 説明                                                                                                                                              |
| -------------- | ---------------------------------------------------------------------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| ティビ            | [`server-memory-quota`](/tidb-configuration-file.md#server-memory-quota-new-in-v409)                       | 非推奨      | v6.5.0 以降では、この構成項目は非推奨です。代わりに、システム変数[`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)使用してメモリをグローバルに管理します。 |
| ティビ            | [`disconnect-on-expired-password`](/tidb-configuration-file.md#disconnect-on-expired-password-new-in-v650) | 新しく追加された | パスワードの有効期限が切れたときに TiDB がクライアント接続を切断するかどうかを決定します。デフォルト値は`true`で、パスワードの有効期限が切れるとクライアント接続が切断されることを意味します。                                           |
| ティクヴ           | `raw-min-ts-outlier-threshold`                                                                             | 削除されました  | この構成項目はバージョン 6.4.0 で非推奨となり、バージョン 6.5.0 で削除されました。                                                                                                |
| ティクヴ           | [`raft-engine.bytes-per-sync`](/tikv-configuration-file.md#bytes-per-sync-2)                               | 非推奨      | v6.5.0 以降、 Raft Engineはバッファリングせずにログを直接ディスクに書き込みます。そのため、この構成項目は非推奨となり、機能しなくなりました。                                                                |
| ティクヴ           | [`cdc.min-ts-interval`](/tikv-configuration-file.md#min-ts-interval)                                       | 修正済み     | CDCレイテンシーを削減するために、デフォルト値が`"1s"`から`"200ms"`に変更されます。                                                                                              |
| ティクヴ           | [`memory-use-ratio`](/tikv-configuration-file.md#memory-use-ratio-new-in-v650)                             | 新しく追加された | PITR ログリカバリにおける使用可能なメモリとシステムメモリの合計の比率を示します。                                                                                                     |
| ティCDC          | [`sink.terminator`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)                 | 新しく追加された | 2 つのデータ変更イベントを区切るために使用される行ターミネータを示します。デフォルトでは値は空で、 `\r\n`使用されることを意味します。                                                                         |
| ティCDC          | [`sink.date-separator`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)             | 新しく追加された | ファイル ディレクトリの日付区切り文字の種類を示します。値のオプションは`none` 、 `year` 、 `month` 、および`day`です。 `none`デフォルト値であり、日付が区切られないことを意味します。                                   |
| ティCDC          | [`sink.enable-partition-separator`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters) | 新しく追加された | パーティションを分離文字列として使用するかどうかを指定します。デフォルト値は`false`で、テーブル内のパーティションが個別のディレクトリに保存されないことを意味します。                                                          |
| ティCDC          | [`sink.csv.delimiter`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)              | 新しく追加された | フィールド間の区切り文字を示します。値は ASCII 文字である必要があり、デフォルトは`,`です。                                                                                              |
| ティCDC          | [`sink.csv.quote`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)                  | 新しく追加された | フィールドを囲む引用符。デフォルト値は`"`です。値が空の場合、引用符は使用されません。                                                                                                    |
| ティCDC          | [`sink.csv.null`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)                   | 新しく追加された | CSV 列が null の場合に表示される文字を指定します。デフォルト値は`\N`です。                                                                                                    |
| ティCDC          | [`sink.csv.include-commit-ts`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)      | 新しく追加された | CSV 行に commit-ts を含めるかどうかを指定します。デフォルト値は`false`です。                                                                                               |

### その他 {#others}

-   v6.5.0 以降、 `mysql.user`テーブルに`Password_reuse_history`と`Password_reuse_time` 2 つの新しい列が追加されます。
-   v6.5.0 以降では、 [インデックス加速](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)機能がデフォルトで有効になっています。この機能は[1 つの`ALTER TABLE`ステートメントで複数の列またはインデックスを変更する](/sql-statements/sql-statement-alter-table.md)と完全に互換性がありません。インデックス アクセラレーションを使用して一意のインデックスを追加する場合は、同じステートメント内の他の列またはインデックスを変更しないようにする必要があります。この機能は[PITR (ポイントインタイムリカバリ)](/br/br-pitr-guide.md)とも互換性がありません。インデックス アクセラレーション機能を使用する場合は、バックグラウンドで PITR バックアップ タスクが実行されていないことを確認する必要があります。そうしないと、予期しない結果が発生する可能性があります。詳細については、 [ドキュメント](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)参照してください。

## 非推奨の機能 {#deprecated-feature}

v6.5.0 以降では、v4.0.7 で導入された`AMEND TRANSACTION`メカニズムは非推奨となり、 [メタデータロック](/metadata-lock.md)に置き換えられます。

## 改善点 {#improvements}

-   ティビ

    -   `BIT`目と`CHAR`列目については、 `INFORMATION_SCHEMA.COLUMNS`の結果をMySQL [＃25472](https://github.com/pingcap/tidb/issues/25472) @ [ホーキングレイ](https://github.com/hawkingrei)と一致させる
    -   TiFlash MPPモードのTiFlashノードのTiDBプローブメカニズムを最適化し、ノードが異常な場合のパフォーマンスへの影響を軽減します[＃39686](https://github.com/pingcap/tidb/issues/39686) @ [ハッカー](https://github.com/hackersean)

-   ティクヴ

    -   ディスク容量の枯渇を避けるため、十分な容量がない場合はRaft Engineへの書き込みを停止します[＃13642](https://github.com/tikv/tikv/issues/13642) @ [嘉陽鄭](https://github.com/jiayang-zheng)
    -   `json_valid`関数を TiKV [＃13571](https://github.com/tikv/tikv/issues/13571) @ [李鎮歓](https://github.com/lizhenhuan)にプッシュダウンするサポート
    -   1 回のバックアップ要求で複数の範囲のデータをバックアップする機能をサポート[＃13701](https://github.com/tikv/tikv/issues/13701) @ [リーヴルス](https://github.com/Leavrth)
    -   rusoto ライブラリ[＃13751](https://github.com/tikv/tikv/issues/13751) @ [3ポインター](https://github.com/3pointer)を更新して、AWS のアジア太平洋地域 (ap-southeast-3) へのデータのバックアップをサポート
    -   悲観的トランザクション競合を減らす[＃13298](https://github.com/tikv/tikv/issues/13298) @ [ミョンケミンタ](https://github.com/MyonKeminta)
    -   外部storageオブジェクトをキャッシュすることでリカバリパフォーマンスを向上[＃13798](https://github.com/tikv/tikv/issues/13798) @ [ユジュンセン](https://github.com/YuJuncen)
    -   専用スレッドで CheckLeader を実行して、TiCDC レプリケーションのレイテンシー[＃13774](https://github.com/tikv/tikv/issues/13774) @ [金星の上](https://github.com/overvenus)を削減します。
    -   チェックポイント[＃13824](https://github.com/tikv/tikv/issues/13824) @ [ユジュンセン](https://github.com/YuJuncen)のプル モデルをサポート
    -   クロスビームチャネル[＃13815](https://github.com/tikv/tikv/issues/13815) @ [スティクナーフ](https://github.com/sticnarf)を更新することで、送信側での回転の問題を回避します。
    -   TiKV [＃13849](https://github.com/tikv/tikv/issues/13849) @ [翻訳](https://github.com/cfzjywxk)でのバッチコプロセッサータスク処理をサポート
    -   TiKVにリージョン[＃13648](https://github.com/tikv/tikv/issues/13648) @ [リクササシネーター](https://github.com/LykxSassinator)を起動するように通知することで、障害回復の待ち時間を短縮します。
    -   コード最適化[＃13827](https://github.com/tikv/tikv/issues/13827) @ [ビジージェイ](https://github.com/BusyJay)によりメモリ使用量の要求サイズを削減
    -   コードの拡張性を向上させるためにRaft拡張機能を導入する[＃13827](https://github.com/tikv/tikv/issues/13827) @ [ビジージェイ](https://github.com/BusyJay)
    -   tikv-ctl を使用して、特定のキー範囲[＃13760](https://github.com/tikv/tikv/issues/13760) @ [ヒューシャープ](https://github.com/HuSharp)に含まれるリージョンを照会する機能をサポートします。
    -   更新されないが継続的にロックされている行の読み取りおよび書き込みパフォーマンスを向上[＃13694](https://github.com/tikv/tikv/issues/13694) @ [スティクナーフ](https://github.com/sticnarf)

-   PD

    -   ロックの粒度を最適化してロックの競合を減らし、高同時実行性におけるハートビートの処理能力を向上させる[＃5586](https://github.com/tikv/pd/issues/5586) @ [rleungx](https://github.com/rleungx)
    -   大規模クラスタのスケジューラパフォーマンスを最適化し、スケジューリングポリシーの本番を高速化します[＃5473](https://github.com/tikv/pd/issues/5473) @ [バッファフライ](https://github.com/bufferflies)
    -   リージョン[＃5606](https://github.com/tikv/pd/issues/5606) @ [rleungx](https://github.com/rleungx)の読み込み速度を向上
    -   リージョンハートビート[＃5648](https://github.com/tikv/pd/issues/5648) @ [rleungx](https://github.com/rleungx)の最適化された処理により不要なオーバーヘッドを削減
    -   墓石ストア[＃5348](https://github.com/tikv/pd/issues/5348) @ [ノルーシュ](https://github.com/nolouch)を自動的にガベージコレクションする機能を追加します

-   TiFlash

    -   SQL側でバッチ処理が行われないシナリオでの書き込みパフォーマンスの向上[＃6404](https://github.com/pingcap/tiflash/issues/6404) @ [リデズ](https://github.com/lidezhu)
    -   `explain analyze`出力[＃5926](https://github.com/pingcap/tiflash/issues/5926) @ [ホンユンヤン](https://github.com/hongyunyan)に TableFullScan の詳細を追加します

-   ツール

    -   TiDBダッシュボード

        -   低速クエリ ページに 3 つの新しいフィールドを追加します: 「準備済みですか?」、「プランはキャッシュからですか?」、「プランはバインディングからですか?」 [＃1451](https://github.com/pingcap/tidb-dashboard/issues/1451) @ [シュギット](https://github.com/shhdgit)

    -   バックアップと復元 (BR)

        -   バックアップログデータの消去プロセス中のBRメモリ使用量を最適化[＃38869](https://github.com/pingcap/tidb/issues/38869) @ [リーヴルス](https://github.com/Leavrth)
        -   復元プロセス中の PD リーダー切り替えによって発生する復元失敗の問題を修正[＃36910](https://github.com/pingcap/tidb/issues/36910) @ [モクイシュル28](https://github.com/MoCuishle28)
        -   ログバックアップ[＃13867](https://github.com/tikv/tikv/issues/13867) @ [ユジュンセン](https://github.com/YuJuncen)で OpenSSL プロトコルを使用することにより TLS 互換性を向上

    -   ティCDC

        -   Kafka プロトコルエンコーダーのパフォーマンスを向上[＃7540](https://github.com/pingcap/tiflow/issues/7540) [＃7532](https://github.com/pingcap/tiflow/issues/7532) [＃7543](https://github.com/pingcap/tiflow/issues/7543) @ [3エースショーハンド](https://github.com/3AceShowHand) @ [スドジ](https://github.com/sdojjy)

    -   TiDB データ移行 (DM)

        -   ブロックリスト[＃7622](https://github.com/pingcap/tiflow/pull/7622) @ [GMHDBJD](https://github.com/GMHDBJD)内のテーブルのデータを解析しないことで、DM のデータ複製パフォーマンスが向上します。
        -   非同期書き込みとバッチ書き込み[＃7580](https://github.com/pingcap/tiflow/pull/7580) @ [GMHDBJD](https://github.com/GMHDBJD)使用してDMリレーの書き込み効率を向上
        -   DM事前チェック[＃7621](https://github.com/pingcap/tiflow/issues/7621) @ [ブチュイトウデゴウ](https://github.com/buchuitoudegou)のエラーメッセージを最適化
        -   古いMySQLバージョン[＃5017](https://github.com/pingcap/tiflow/issues/5017) @ [翻訳者](https://github.com/lyzx2001)の`SHOW SLAVE HOSTS`の互換性を改善

## バグ修正 {#bug-fixes}

-   ティビ

    -   場合によっては発生するチャンク再利用機能のメモリチャンクの誤用問題を修正[＃38917](https://github.com/pingcap/tidb/issues/38917) @ [学習を続ける20221](https://github.com/keeplearning20221)
    -   `tidb_constraint_check_in_place_pessimistic`の内部セッションがグローバル設定[＃38766](https://github.com/pingcap/tidb/issues/38766) @ [エキシウム](https://github.com/ekexium)の影響を受ける可能性がある問題を修正
    -   `AUTO_INCREMENT`列が`CHECK`制約[＃38894](https://github.com/pingcap/tidb/issues/38894) @ [ヤンケオ](https://github.com/YangKeao)で動作しない問題を修正
    -   `INSERT IGNORE INTO`使用して`STRING`型のデータを`SMALLINT`型の自動増分列に挿入すると、エラー[＃38483](https://github.com/pingcap/tidb/issues/38483) @ [ホーキングレイ](https://github.com/hawkingrei)発生する問題を修正しました。
    -   パーティションテーブル[＃38932](https://github.com/pingcap/tidb/issues/38932) @ [ミョンス](https://github.com/mjonss)のパーティション列の名前を変更する操作で NULL ポインター エラーが発生する問題を修正しました。
    -   パーティションテーブルのパーティション列を変更すると DDL がハングする問題を修正[＃38530](https://github.com/pingcap/tidb/issues/38530) @ [ミョンス](https://github.com/mjonss)
    -   v4.0.16からv6.4.0 [＃38980](https://github.com/pingcap/tidb/issues/38980) @ [タンジェンタ](https://github.com/tangenta)にアップグレードした後に`ADMIN SHOW JOB`操作がパニックになる問題を修正
    -   `tidb_decode_key`関数がパーティションテーブル[＃39304](https://github.com/pingcap/tidb/issues/39304) @ [定義2014](https://github.com/Defined2014)のエンコーディングを正しく解析できない問題を修正
    -   ログローテーション中に gRPC エラーログが正しいログファイルにリダイレクトされない問題を修正[＃38941](https://github.com/pingcap/tidb/issues/38941) @ [xhebox](https://github.com/xhebox)
    -   TiKV が読み取りエンジンとして構成されていない場合に、TiDB が`BEGIN; SELECT... FOR UPDATE;`ポイント クエリに対して予期しない実行プランを生成する問題を修正[＃39344](https://github.com/pingcap/tidb/issues/39344) @ [イサール](https://github.com/Yisaer)
    -   誤って`StreamAgg` TiFlashに押し下げると、間違った結果[＃39266](https://github.com/pingcap/tidb/issues/39266) @ [修正DB](https://github.com/fixdb)発生する問題を修正しました。

-   ティクヴ

    -   Raft Enginectl [＃11119](https://github.com/tikv/tikv/issues/11119) @ [タボキ](https://github.com/tabokie)のエラーを修正
    -   tikv-ctl [＃13515](https://github.com/tikv/tikv/issues/13515) @ [グオシアンCN](https://github.com/guoxiangCN)で`compact raft`コマンドを実行するときに発生する`Get raft db is not allowed`エラーを修正
    -   TLS が有効な場合にログバックアップが機能しない問題を修正[＃13867](https://github.com/tikv/tikv/issues/13867) @ [ユジュンセン](https://github.com/YuJuncen)
    -   ジオメトリフィールドタイプ[＃13651](https://github.com/tikv/tikv/issues/13651) @ [ドヴェーデン](https://github.com/dveeden)のサポート問題を修正
    -   新しい照合順序が有効になっていない場合、 `LIKE`演算子の`_`非 ASCII 文字と一致しない問題を修正[＃13769](https://github.com/tikv/tikv/issues/13769) @ [ヤンケオ](https://github.com/YangKeao)
    -   `reset-to-version`コマンド[＃13829](https://github.com/tikv/tikv/issues/13829) @ [タボキ](https://github.com/tabokie)を実行すると tikv-ctl が予期せず終了する問題を修正

-   PD

    -   `balance-hot-region-scheduler`構成が変更されていない場合は[＃5701](https://github.com/tikv/pd/issues/5701) @ [ハンダンDM](https://github.com/HunDunDM)が保持されない問題を修正
    -   アップグレードプロセス中に`rank-formula-version`前の構成が保持されない問題を修正[＃5698](https://github.com/tikv/pd/issues/5698) @ [ハンダンDM](https://github.com/HunDunDM)

-   TiFlash

    -   TiFlash [＃6159](https://github.com/pingcap/tiflash/issues/6159) @ [リデズ](https://github.com/lidezhu)を再起動した後、デルタレイヤーの列ファイルを圧縮できない問題を修正しました。
    -   TiFlashファイルオープン OPS が[＃6345](https://github.com/pingcap/tiflash/issues/6345) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)で高すぎる問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   BR がログバックアップデータを削除するときに、削除すべきでないデータを誤って削除してしまう問題を修正[＃38939](https://github.com/pingcap/tidb/issues/38939) @ [リーヴルス](https://github.com/Leavrth)
        -   データベースまたはテーブル[＃39150](https://github.com/pingcap/tidb/issues/39150) @ [モクイシュル28](https://github.com/MoCuishle28)の照合に古いフレームワークを使用すると復元タスクが失敗する問題を修正しました
        -   Alibaba Cloud と Huawei Cloud が Amazon S3storageと完全に互換性がないためバックアップが失敗する問題を修正[＃39545](https://github.com/pingcap/tidb/issues/39545) @ [3ポインター](https://github.com/3pointer)

    -   ティCDC

        -   PDリーダーが[＃7470](https://github.com/pingcap/tiflow/issues/7470) @ [沢民州](https://github.com/zeminzhou)でクラッシュするとTiCDCが停止する問題を修正
        -   最初に DDL ステートメントを実行し、次に変更フィード[＃7682](https://github.com/pingcap/tiflow/issues/7682) @ [アズドンメン](https://github.com/asddongmen)を一時停止して再開するシナリオで発生したデータ損失を修正しました。
        -   TiFlash [＃7744](https://github.com/pingcap/tiflow/issues/7744) @ [金星の上](https://github.com/overvenus)以降のバージョンがある場合に TiCDC が誤ってエラーを報告する問題を修正しました
        -   ダウンストリームネットワークが利用できない場合にシンクコンポーネントが停止する問題を修正[＃7706](https://github.com/pingcap/tiflow/issues/7706) @ [ヒック](https://github.com/hicqu)
        -   ユーザーがレプリケーションタスクをすばやく削除し、同じタスク名で別のタスクを作成するとデータが失われる問題を修正[＃7657](https://github.com/pingcap/tiflow/issues/7657) @ [金星の上](https://github.com/overvenus)

    -   TiDB データ移行 (DM)

        -   アップストリームデータベースがGTIDモードを有効にしているが、データ[＃7037](https://github.com/pingcap/tiflow/issues/7037) @ [りゅうめんぎゃ](https://github.com/liumengya94)がない場合に`task-mode:all`タスクを開始できない問題を修正しました。
        -   既存のワーカーが終了する前に新しい DM ワーカーがスケジュールされると、データが複数回複製される問題を修正[＃7658](https://github.com/pingcap/tiflow/issues/7658) @ [GMHDBJD](https://github.com/GMHDBJD)
        -   アップストリームデータベースが正規表現を使用して権限[＃7645](https://github.com/pingcap/tiflow/issues/7645) @ [ランス6716](https://github.com/lance6716)を付与する場合に DM 事前チェックに合格しない問題を修正しました

    -   TiDB Lightning

        -   TiDB Lightning が巨大なソース データ ファイル[＃39331](https://github.com/pingcap/tidb/issues/39331) @ [ダシュン](https://github.com/dsdashun)をインポートするときに発生するメモリリークの問題を修正しました
        -   TiDB Lightning が並列[＃39476](https://github.com/pingcap/tidb/issues/39476) @ [ダシュン](https://github.com/dsdashun)でデータをインポートするときに競合を正しく検出できない問題を修正

## 寄稿者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   [エ1イヤ1](https://github.com/e1ijah1)
-   [グオシアンCN](https://github.com/guoxiangCN) (初めての投稿者)
-   [嘉陽鄭](https://github.com/jiayang-zheng)
-   [ジフハウス](https://github.com/jiyfhust)
-   [マイクチェンウェイ](https://github.com/mikechengwei)
-   [ピンとb](https://github.com/pingandb)
-   [サシャシュラ](https://github.com/sashashura)
-   [ソースリウ](https://github.com/sourcelliu)
-   [ウィックスブティ](https://github.com/wxbty)
