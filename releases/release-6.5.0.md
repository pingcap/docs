---
title: TiDB 6.5.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 6.5.0.
---

# TiDB 6.5.0 リリースノート {#tidb-6-5-0-release-notes}

発売日：2022年12月29日

TiDB バージョン: 6.5.0

クイック アクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [本番展開](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup) | [インストール パッケージ](https://www.pingcap.com/download/?version=v6.5.0#version-list)

TiDB 6.5.0 は長期サポート リリース (LTS) です。

以前の LTS 6.1.0 と比較して、6.5.0 には、 [6.2.0-DMR](/releases/release-6.2.0.md) 、 [6.3.0-DMR](/releases/release-6.3.0.md) 、 [6.4.0-DMR](/releases/release-6.4.0.md)でリリースされた新機能、改善、およびバグ修正が含まれているだけでなく、次の主要な機能と改善も導入されています。

-   [指数加速度](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)機能が一般提供 (GA) になり、v6.1.0 と比較して、インデックスを追加するパフォーマンスが約 10 倍向上します。
-   TiDB グローバルメモリコントロールが GA になり、 [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)を介してメモリ消費のしきい値を制御できます。
-   高性能でグローバルに単調な[`AUTO_INCREMENT`](/auto-increment.md#mysql-compatibility-mode)列属性は、MySQL と互換性のある GA になります。
-   [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md)は TiCDC および PITR と互換性があり、GA になります。
-   より正確な[コスト モデル バージョン 2](/cost-model.md#cost-model-version-2)一般に利用可能にし、 `AND` for [インデックスマージ](/explain-index-merge.md)で接続された式をサポートすることで、TiDB オプティマイザーを強化します。
-   `JSON_EXTRACT()`関数をTiFlashにプッシュ ダウンすることをサポートします。
-   パスワード コンプライアンスの監査要件を満たす[パスワード管理](/password-management.md)ポリシーをサポートします。
-   TiDB LightningおよびDumpling は、 [インポート](/tidb-lightning/tidb-lightning-data-source.md)および[エクスポート](/dumpling-overview.md#improve-export-efficiency-through-concurrency)の圧縮された SQL および CSV ファイルをサポートします。
-   TiDB データ移行 (DM) [継続的なデータ検証](/dm/dm-continuous-data-validation.md) GA になります。
-   TiDB Backup &amp; Restore は、スナップショット チェックポイント バックアップをサポートし、 [PITR](/br/br-pitr-guide.md#run-pitr)復元パフォーマンスを 50% 向上させ、一般的なシナリオで RPO を 5 分まで短縮します。
-   [データを Kafka に複製する](/replicate-data-to-kafka.md)の TiCDC スループットを 4000 行/秒から 35000 行/秒に改善し、レプリケーションレイテンシーを2 秒に短縮します。
-   データのライフサイクルを管理する行レベル[生存時間 (TTL)](/time-to-live.md)を提供します (実験的)。
-   TiCDC は、Amazon S3、Azure Blob Storage、NFS (実験的) などの[変更されたログをオブジェクトstorageに複製する](/ticdc/ticdc-sink-to-cloud-storage.md)をサポートします。

## 新機能 {#new-features}

### SQL {#sql}

-   インデックスを追加するTiDBのパフォーマンスは約10倍向上します（GA） [#35983](https://github.com/pingcap/tidb/issues/35983) @ [ベンジャミン2037](https://github.com/benjamin2037) @ [接線](https://github.com/tangenta)

    TiDB v6.3.0 では、インデックス作成時のバックフィル速度を向上させるための実験的機能として[インデックス アクセラレーションを追加する](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)が導入されています。 v6.5.0 では、この機能が GA になり、デフォルトで有効になり、大きなテーブルでのパフォーマンスは v6.1.0 の約 10 倍になると予想されます。アクセラレーション機能は、単一の SQL ステートメントがインデックスを連続して追加するシナリオに適しています。複数の SQL ステートメントが並行してインデックスを追加する場合、SQL ステートメントの 1 つだけが高速化されます。

-   DDL 変更中の DML 成功率を向上させるために、軽量のメタデータ ロックを提供します (GA) [#37275](https://github.com/pingcap/tidb/issues/37275) @ [wjhuang2016](https://github.com/wjhuang2016)

    TiDB v6.3.0 では、実験的機能として[メタデータ ロック](/metadata-lock.md)が導入されています。 DML ステートメントによって引き起こされる`Information schema is changed`エラーを回避するために、TiDB はテーブル メタデータの変更中に DML と DDL の優先度を調整し、進行中の DDL が古いメタデータを持つ DML がコミットされるのを待機させます。 v6.5.0 では、この機能は GA になり、デフォルトで有効になっています。さまざまなタイプの DDL 変更シナリオに適しています。既存のクラスターを v6.5.0 より前のバージョンから v6.5.0 以降にアップグレードすると、TiDB は自動的にメタデータ ロックを有効にします。この機能を無効にするには、システム変数[`tidb_enable_metadata_lock`](/system-variables.md#tidb_enable_metadata_lock-new-in-v630) `OFF`に設定します。

    詳細については、 [ドキュメンテーション](/metadata-lock.md)を参照してください。

-   `FLASHBACK CLUSTER TO TIMESTAMP` (GA) [#37197](https://github.com/pingcap/tidb/issues/37197) [#13303](https://github.com/tikv/tikv/issues/13303) @ [定義済み2014](https://github.com/Defined2014) @ [bb7133](https://github.com/bb7133) @ [Jmポテト](https://github.com/JmPotato) @ [コナー1996](https://github.com/Connor1996) @ [ヒューシャープ](https://github.com/HuSharp) @ [カルバンネオ](https://github.com/CalvinNeo)を使用した特定の時点へのクラスターの復元をサポート

    v6.4.0 以降、TiDB は[`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md)ステートメントを実験的機能として導入しました。このステートメントを使用して、ガベージ コレクション (GC) の有効期間内の特定の時点にクラスターを復元できます。 v6.5.0 では、この機能は TiCDC および PITR と互換性があり、GA になりました。この機能は、DML の誤操作を簡単に元に戻し、元のクラスターを数分で復元し、さまざまな時点でデータをロールバックして、データが変更された正確な時刻を特定するのに役立ちます。

    詳細については、 [ドキュメンテーション](/sql-statements/sql-statement-flashback-to-timestamp.md)を参照してください。

-   `INSERT` 、 `REPLACE` 、 `UPDATE` 、および`DELETE` [#33485](https://github.com/pingcap/tidb/issues/33485) @ [エキキシウム](https://github.com/ekexium)を含む非トランザクション DML ステートメントを完全にサポート

    大規模なデータ処理のシナリオでは、大規模なトランザクションを含む単一の SQL ステートメントがクラスターの安定性とパフォーマンスに悪影響を及ぼす可能性があります。非トランザクション DML ステートメントは、内部実行用に複数の SQL ステートメントに分割された DML ステートメントです。 split ステートメントは、トランザクションの原子性と分離性を損ないますが、クラスターの安定性を大幅に向上させます。 TiDB は、v6.1.0 以降、非トランザクション`DELETE`ステートメントをサポートしており、v6.5.0 以降、非トランザクション`INSERT` 、 `REPLACE` 、および`UPDATE`ステートメントをサポートしています。

    詳細については、 [非トランザクション DML ステートメント](/non-transactional-dml.md)および[`BATCH`構文](/sql-statements/sql-statement-batch.md)を参照してください。

-   サポート時間 (TTL) (実験的) [#39262](https://github.com/pingcap/tidb/issues/39262) @ [ルクァンチャオ](https://github.com/lcwangchao)

    TTL は、行レベルのデータ ライフタイム管理を提供します。 TiDB では、TTL 属性を持つテーブルがデータの有効期間を自動的にチェックし、期限切れのデータを行レベルで削除します。 TTL は、オンラインの読み取りおよび書き込みワークロードに影響を与えることなく、不要なデータを定期的かつタイムリーにクリーンアップできるように設計されています。

    詳細については、 [ドキュメンテーション](/time-to-live.md)を参照してください。

-   `INSERT INTO SELECT`ステートメントを使用したTiFlashクエリ結果の保存をサポート (実験的) [#37515](https://github.com/pingcap/tidb/issues/37515) @ [ゲンリキ](https://github.com/gengliqi)

    v6.5.0 から、TiDB は`INSERT INTO SELECT`ステートメントの`SELECT`句 (分析クエリ) をTiFlashにプッシュ ダウンすることをサポートします。このようにして、 TiFlashクエリの結果を`INSERT INTO`で指定された TiDB テーブルに簡単に保存して、さらに分析することができます。これは、結果のキャッシュ (つまり、結果の具体化) として有効になります。例えば：

    ```sql
    INSERT INTO t2 SELECT Mod(x,y) FROM t1;
    ```

    実験的段階では、この機能はデフォルトで無効になっています。有効にするには、システム変数[`tidb_enable_tiflash_read_for_write_stmt`](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-new-in-v630)を`ON`に設定します。この機能の`INSERT INTO`で指定された結果テーブルには特別な制限はなく、その結果テーブルにTiFlashレプリカを追加するかどうかは自由です。この機能の一般的な使用シナリオは次のとおりです。

    -   TiFlashを使用して複雑な分析クエリを実行する
    -   TiFlashクエリの結果を再利用するか、高度な同時オンライン リクエストを処理する
    -   入力データ サイズと比較して比較的小さい結果セットが必要です。できれば 100 MiB 未満である必要があります。

    詳細については、 [ドキュメンテーション](/tiflash/tiflash-results-materialization.md)を参照してください。

-   バインド履歴の実行計画をサポート (実験的) [#39199](https://github.com/pingcap/tidb/issues/39199) @ [fzzf678](https://github.com/fzzf678)

    SQL ステートメントの場合、実行中のさまざまな要因により、オプティマイザが以前の最適な実行計画ではなく新しい実行計画を選択する場合があり、SQL のパフォーマンスが影響を受けます。この場合、最適な実行計画がまだクリアされていなければ、SQL 実行履歴に残ります。

    v6.5.0 では、TiDB は[`CREATE [GLOBAL | SESSION] BINDING`](/sql-statements/sql-statement-create-binding.md)ステートメントでバインド オブジェクトを拡張することにより、過去の実行計画のバインドをサポートします。 SQL 文`CREATE [GLOBAL | SESSION] BINDING`実行計画が変更された場合、 `plan_digest`の実行計画が SQL 実行履歴メモリテーブル (たとえば、 `statements_summary` ）。この機能により、実行計画の変更の問題を処理するプロセスが簡素化され、メンテナンス効率が向上します。

    詳細については、 [ドキュメンテーション](/sql-plan-management.md#create-a-binding-according-to-a-historical-execution-plan)を参照してください。

### Security {#security}

-   パスワード複雑度ポリシー[#38928](https://github.com/pingcap/tidb/issues/38928) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)をサポート

    このポリシーを有効にした後、パスワードを設定すると、TiDB はパスワードの長さ、パスワードの大文字と小文字、数字、および特殊文字が十分かどうか、パスワードが辞書と一致するかどうか、およびパスワードがユーザー名と一致するかどうかをチェックします。これにより、安全なパスワードを設定できます。

    TiDB は、パスワードの強度を検証する SQL 関数[`VALIDATE_PASSWORD_STRENGTH()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_validate-password-strength)を提供します。

    詳細については、 [ドキュメンテーション](/password-management.md#password-complexity-policy)を参照してください。

-   パスワード有効期限ポリシー[#38936](https://github.com/pingcap/tidb/issues/38936) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)をサポート

    TiDB は、手動の有効期限、グローバル レベルの自動有効期限、およびアカウント レベルの自動有効期限を含む、パスワードの有効期限ポリシーの構成をサポートしています。このポリシーを有効にした後は、パスワードを定期的に変更する必要があります。これにより、長期間の使用によるパスワード漏洩のリスクが軽減され、パスワードのセキュリティが向上します。

    詳細については、 [ドキュメンテーション](/password-management.md#password-expiration-policy)を参照してください。

-   パスワード再利用ポリシー[#38937](https://github.com/pingcap/tidb/issues/38937) @ [キープラーニング20221](https://github.com/keeplearning20221)をサポート

    TiDB は、グローバル レベルのパスワード再利用ポリシーやアカウント レベルのパスワード再利用ポリシーなど、パスワード再利用ポリシーの構成をサポートしています。このポリシーを有効にすると、指定した期間内に使用したパスワード、または最近使用したいくつかのパスワードを使用できなくなります。これにより、パスワードの繰り返し使用によるパスワード漏洩のリスクが軽減され、パスワードのセキュリティが向上します。

    詳細については、 [ドキュメンテーション](/password-management.md#password-reuse-policy)を参照してください。

-   失敗したログインの追跡と一時的なアカウント ロック ポリシー[#38938](https://github.com/pingcap/tidb/issues/38938) @ [最後の切歯](https://github.com/lastincisor)をサポート

    このポリシーを有効にした後、間違ったパスワードで連続して複数回 TiDB にログインすると、アカウントが一時的にロックされます。ロック時間が終了すると、アカウントは自動的にロック解除されます。

    詳細については、 [ドキュメンテーション](/password-management.md#failed-login-tracking-and-temporary-account-locking-policy)を参照してください。

### 可観測性 {#observability}

-   TiDB ダッシュボードは、独立した Pod [#1447](https://github.com/pingcap/tidb-dashboard/issues/1447) @ [サバピン](https://github.com/SabaPing)として Kubernetes にデプロイできます

    TiDB v6.5.0 (およびそれ以降) およびTiDB Operator v1.4.0 (およびそれ以降) は、TiDB ダッシュボードを Kubernetes 上の独立した Pod としてデプロイすることをサポートします。 TiDB Operatorを使用して、この Pod の IP アドレスにアクセスし、TiDB ダッシュボードを起動できます。

    TiDB ダッシュボードを個別に展開すると、次の利点があります。

    -   TiDB ダッシュボードの計算作業は、PD ノードに負担をかけません。これにより、より安定したクラスター操作が保証されます。
    -   PD ノードが利用できない場合でも、ユーザーは診断のために TiDB ダッシュボードにアクセスできます。
    -   インターネット上の TiDB ダッシュボードへのアクセスには、PD の特権インターフェイスは必要ありません。したがって、クラスターのセキュリティ リスクが軽減されます。

    詳細については、 [ドキュメンテーション](https://docs.pingcap.com/tidb-in-kubernetes/dev/get-started#deploy-tidb-dashboard-independently)を参照してください。

-   パフォーマンス概要ダッシュボードにTiFlashおよび CDC (Change Data Capture) パネルが追加されました[#39230](https://github.com/pingcap/tidb/issues/39230) @ [データベース ID](https://github.com/dbsid)

    v6.1.0 以降、TiDB は Grafana に Performance Overview ダッシュボードを導入しました。これは、TiDB、TiKV、および PD の全体的なパフォーマンス診断のためのシステムレベルのエントリを提供します。 v6.5.0 では、パフォーマンス概要ダッシュボードにTiFlashおよび CDC パネルが追加されています。これらのパネルでは、v6.5.0 以降、パフォーマンス概要ダッシュボードを使用して、TiDB クラスター内のすべてのコンポーネントのパフォーマンスを分析できます。

    TiFlashおよび CDC パネルは、 TiFlashおよび TiCDC の監視情報を再編成します。これにより、 TiFlashおよび TiCDC のパフォーマンスの問題を分析およびトラブルシューティングする効率が大幅に向上します。

    -   [TiFlashパネル](/grafana-performance-overview-dashboard.md#tiflash)では、 TiFlashクラスターのリクエスト タイプ、レイテンシー分析、リソース使用状況の概要を簡単に表示できます。
    -   [CDC パネル](/grafana-performance-overview-dashboard.md#cdc)では、TiCDC クラスターの正常性、レプリケーションレイテンシー、データ フロー、およびダウンストリーム書き込みレイテンシーを簡単に表示できます。

    詳細については、 [ドキュメンテーション](/performance-tuning-methods.md)を参照してください。

### パフォーマンス {#performance}

-   [インデックスマージ](/glossary.md#index-merge) `AND` [#39333](https://github.com/pingcap/tidb/issues/39333) @ [グオシャオゲ](https://github.com/guo-shaoge) @ [時間と運命](https://github.com/time-and-fate) @ [ハイランフー](https://github.com/hailanwhu)で接続された式をサポートします

    v6.5.0 より前の TiDB は、 `OR`で接続されたフィルター条件に対してインデックス マージの使用のみをサポートしていました。 v6.5.0 から、TiDB は`WHERE`句の`AND`で接続されたフィルター条件に対してインデックス マージの使用をサポートしています。このように、TiDB のインデックス マージは、クエリ フィルター条件のより一般的な組み合わせをカバーできるようになり、ユニオン ( `OR` ) 関係に限定されなくなりました。現在の v6.5.0 バージョンは、オプティマイザーによって自動的に選択される`OR`の条件でのインデックス マージのみをサポートします。 `AND`条件のインデックス マージを有効にするには、 [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)ヒントを使用する必要があります。

    インデックス マージの詳細については、 [v5.4.0 リリースノート](/releases/release-5.4.0.md#performance)および[インデックス マージについて説明する](/explain-index-merge.md)を参照してください。

-   次の JSON関数のTiFlash [#39458](https://github.com/pingcap/tidb/issues/39458) @ [イビン87](https://github.com/yibin87)へのプッシュ ダウンをサポート

    -   `->`
    -   `->>`
    -   `JSON_EXTRACT()`

    JSON 形式は、アプリケーション データのモデリングに柔軟な方法を提供します。したがって、ますます多くのアプリケーションがデータ交換とデータstorageに JSON 形式を使用しています。 JSON関数をTiFlashにプッシュ ダウンすることで、JSON 型のデータ分析の効率を向上させ、TiDB をよりリアルタイムの分析シナリオに使用できます。

-   次の文字列関数のTiFlash [#6115](https://github.com/pingcap/tiflash/issues/6115) @ [xzhangxian1008](https://github.com/xzhangxian1008)へのプッシュ ダウンをサポート

    -   `regexp_like`
    -   `regexp_instr`
    -   `regexp_substr`

-   [ビュー](/views.md) [#37887](https://github.com/pingcap/tidb/issues/37887) @ [思い出す](https://github.com/Reminiscent)で実行計画の生成を妨害するグローバル オプティマイザ ヒントをサポートします。

    一部のビュー アクセス シナリオでは、オプティマイザー ヒントを使用して、ビュー内のクエリの実行プランに干渉し、最適なパフォーマンスを実現する必要があります。 v6.5.0 以降、TiDB はビュー内のクエリ ブロックへのグローバル ヒントの追加をサポートし、クエリで定義されたヒントをビューで有効にします。この機能は、ネストされたビューを含む複雑な SQL ステートメントにヒントを挿入する方法を提供し、実行計画の制御を強化し、複雑なステートメントのパフォーマンスを安定させます。グローバル ヒントを使用するには、 [クエリ ブロックに名前を付ける](/optimizer-hints.md#step-1-define-the-query-block-name-of-the-view-using-the-qb_name-hint)と[ヒント参照を指定する](/optimizer-hints.md#step-2-add-the-target-hints)が必要です。

    詳細については、 [ドキュメンテーション](/optimizer-hints.md#hints-that-take-effect-globally)を参照してください。

-   [分割されたテーブル](/partitioned-table.md)から TiKV [#26166](https://github.com/pingcap/tidb/issues/26166) @ [ウィノロス](https://github.com/winoros)へのソート操作の押し下げをサポート

    [パーティションテーブル](/partitioned-table.md)機能は v6.1.0 から GA になっていますが、TiDB はそのパフォーマンスを継続的に改善しています。 v6.5.0 では、TiDB は`ORDER BY`や`LIMIT`の並べ替え操作を計算とフィルタリングのために TiKV にプッシュ ダウンすることをサポートしています。

-   オプティマイザーは、より正確なコスト モデル バージョン 2 (GA) [#35240](https://github.com/pingcap/tidb/issues/35240) @ [qw4990](https://github.com/qw4990)を導入します

    TiDB v6.2.0 では、実験的機能として[コスト モデル バージョン 2](/cost-model.md#cost-model-version-2)が導入されています。このモデルは、より正確なコスト見積もり方法を使用して、オプティマイザが最適な実行計画を選択できるようにします。特にTiFlashが展開されている場合、Cost Model バージョン 2 は適切なstorageエンジンの選択を自動的に支援し、多くの手動介入を回避します。一定期間の実際のシーンでのテストの後、このモデルは v6.5.0 で GA になります。 v6.5.0 以降、新しく作成されたクラスターはデフォルトでコスト モデル バージョン 2 を使用します。クラスターを v6.5.0 にアップグレードする場合、コスト モデル バージョン 2 によってクエリ プランが変更される可能性があるため、十分なパフォーマンス テストを行った後、新しいコスト モデルを使用するように[`tidb_cost_model_version = 2`](/system-variables.md#tidb_cost_model_version-new-in-v620)変数を設定できます。

    コスト モデル バージョン 2 は、TiDB オプティマイザの全体的な機能を大幅に改善し、TiDB がより強力な HTAP データベースに向けて進化するのを支援する、一般に利用可能な機能になります。

    詳細については、 [ドキュメンテーション](/cost-model.md#cost-model-version-2)を参照してください。

-   TiFlash は、テーブル行[#37165](https://github.com/pingcap/tidb/issues/37165) @ [エルザ0520](https://github.com/elsa0520)の数を取得する操作を最適化します。

    データ分析のシナリオでは、フィルター条件なしでテーブルの実際の行数を`COUNT(*)`で取得するのが一般的な操作です。 v6.5.0 では、 TiFlash は`COUNT(*)`の書き換えを最適化し、列定義が最も短い非 null 列を自動的に選択して行数をカウントします。これにより、 TiFlashでの I/O 操作の数を効果的に削減し、行数の取得。

### 安定性 {#stability}

-   グローバルメモリコントロール機能は GA [#37816](https://github.com/pingcap/tidb/issues/37816) @ [wshwsh12](https://github.com/wshwsh12)になりました

    v6.4.0 以降、TiDB はグローバルメモリコントロールを実験的機能として導入しました。 v6.5.0 では GA になり、メインメモリの消費量を追跡できます。グローバルメモリ消費量が[`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)で定義されたしきい値に達すると、TiDB は安定性を確保するために、GC または SQL 操作のキャンセルによってメモリ使用量を制限しようとします。

    セッション内のトランザクションによって消費されるメモリ(最大値は以前は構成項目によって設定されていました[`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit) ) がメモリ管理モジュールによって追跡されるようにメモリたことに注意してください[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 、システム変数[`tidb_mem_oom_action`](/system-variables.md#tidb_mem_oom_action-new-in-v610)によって定義された動作がトリガーされます (デフォルトは`CANCEL` 、つまり操作のキャンセルです)。前方互換性を確保するために、 [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit)がデフォルト以外の値として設定されている場合でも、TiDB はトランザクションが`txn-total-size-limit`によって設定されたメモリを使用できることを保証します。

    TiDB v6.5.0 以降を使用している場合は、 [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit)削除し、トランザクションのメモリ使用量に別の制限を設定しないことをお勧めします。代わりに、システム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)および[`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)を使用してグローバルメモリを管理します。これにより、メモリの使用効率が向上します。

    詳細については、 [ドキュメンテーション](/configure-memory-usage.md)を参照してください。

### 使いやすさ {#ease-of-use}

-   `EXPLAIN ANALYZE`出力[#5926](https://github.com/pingcap/tiflash/issues/5926) @ [ホンユニャン](https://github.com/hongyunyan)のTiFlash `TableFullScan`オペレーターの実行情報を絞り込みます

    `EXPLAIN ANALYZE`ステートメントは、実行計画とランタイム統計を出力するために使用されます。 v6.5.0 では、 TiFlash はDMFile 関連の実行情報を追加することにより、 `TableFullScan`オペレーターの実行情報を改良しました。 TiFlashデータ スキャン ステータス情報がより直感的に表示されるようになり、 TiFlash のパフォーマンスをより簡単に分析できるようになりました。

    詳細については、 [ドキュメンテーション](/sql-statements/sql-statement-explain-analyze.md)を参照してください。

-   JSON 形式での実行計画の出力をサポート[#39261](https://github.com/pingcap/tidb/issues/39261) @ [fzzf678](https://github.com/fzzf678)

    v6.5.0 では、TiDB は実行計画の出力形式を拡張します。 `EXPLAIN`文に`FORMAT = "tidb_json"`を指定することで、SQL実行計画をJSON形式で出力できます。この機能により、SQL デバッグ ツールと診断ツールは実行計画をより便利かつ正確に読み取ることができるため、SQL の診断とチューニングの使いやすさが向上します。

    詳細については、 [ドキュメンテーション](/sql-statements/sql-statement-explain.md)を参照してください。

### MySQL の互換性 {#mysql-compatibility}

-   高パフォーマンスでグローバルに単調な`AUTO_INCREMENT`列属性 (GA) [#38442](https://github.com/pingcap/tidb/issues/38442) @ [ティアンカイマオ](https://github.com/tiancaiamao)をサポート

    v6.4.0 以降、TiDB は実験的機能として`AUTO_INCREMENT` MySQL 互換モードを導入しました。このモードでは、すべての TiDB インスタンスで ID が単調に増加することを保証する集中自動インクリメント ID 割り当てサービスが導入されます。この機能により、クエリ結果を自動インクリメント ID で簡単に並べ替えることができます。 v6.5.0 では、この機能は GA になります。この機能を使用したテーブルの挿入 TPS は 20,000 を超えると予想され、この機能は柔軟なスケーリングをサポートして、単一のテーブルとクラスター全体の書き込みスループットを向上させます。 MySQL 互換モードを使用するには、テーブル作成時に`AUTO_ID_CACHE` ～ `1`を設定する必要があります。次に例を示します。

    ```sql
    CREATE TABLE t(a int AUTO_INCREMENT key) AUTO_ID_CACHE 1;
    ```

    詳細については、 [ドキュメンテーション](/auto-increment.md#mysql-compatibility-mode)を参照してください。

### データ移行 {#data-migration}

-   gzip、snappy、および zstd 圧縮形式での SQL および CSV ファイルのエクスポートとインポートをサポート[#38514](https://github.com/pingcap/tidb/issues/38514) @ [リチュンジュ](https://github.com/lichunzhu)

    Dumpling は、 gzip、snappy、および zstd の圧縮形式で、圧縮された SQL および CSV ファイルへのデータのエクスポートをサポートしています。 TiDB Lightning は、これらの形式の圧縮ファイルのインポートもサポートしています。

    以前は、データをエクスポートまたはインポートして CSV および SQL ファイルを保存するために大きなstorageスペースを用意する必要があり、その結果、storageコストが高くなりました。この機能のリリースにより、データ ファイルを圧縮することでstorageコストを大幅に削減できます。

    詳細については、 [ドキュメンテーション](/dumpling-overview.md#improve-export-efficiency-through-concurrency)を参照してください。

-   binlog解析機能の最適化[#924](https://github.com/pingcap/dm/issues/924) @ [gmhdbjd](https://github.com/GMHDBJD)

    TiDB は、移行タスクに含まれていないスキーマとテーブルのbinlogイベントを除外できるため、解析の効率と安定性が向上します。このポリシーは、v6.5.0 でデフォルトで有効になります。追加の構成は必要ありません。

    以前は、少数のテーブルのみが移行された場合でも、上流のbinlogファイル全体を解析する必要がありました。移行する必要のないbinlogファイル内のテーブルのbinlogイベントも解析する必要があり、効率的ではありませんでした。一方、これらのbinlogイベントが解析をサポートしていない場合、タスクは失敗します。移行タスクでテーブルのbinlogイベントのみを解析することで、binlogの解析効率が大幅に向上し、タスクの安定性が向上します。

-   TiDB Lightningのディスク クォータは GA [#446](https://github.com/pingcap/tidb-lightning/issues/446) @ [ぶちゅとでごう](https://github.com/buchuitoudegou)です

    TiDB Lightningのディスク クォータを構成できます。ディスク クォータが不足すると、 TiDB Lightning はソース データの読み取りと一時ファイルの書き込みを停止します。代わりに、まず並べ替えられたキー値を TiKV に書き込み、 TiDB Lightning がローカルの一時ファイルを削除した後、インポート プロセスを続行します。

    以前は、 TiDB Lightning が物理モードを使用してデータをインポートすると、生データのエンコード、並べ替え、および分割のために、ローカル ディスク上に多数の一時ファイルが作成されていました。ローカル ディスクの容量が不足すると、ファイルへの書き込みに失敗するため、 TiDB Lightning はエラーで終了します。この機能により、 TiDB Lightningタスクはローカル ディスクの上書きを回避できます。

    詳細については、 [ドキュメンテーション](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#configure-disk-quota-new-in-v620)を参照してください。

-   DM での継続的なデータ検証は GA [#4426](https://github.com/pingcap/tiflow/issues/4426) @ [D3ハンター](https://github.com/D3Hunter)です

    アップストリーム データベースからダウンストリーム データベースに増分データを移行するプロセスでは、データ フローによってエラーやデータ損失が発生する可能性がわずかにあります。信用取引や証券取引など、強力なデータ整合性が必要なシナリオでは、移行後にデータの完全なボリューム チェックサムを実行して、データの整合性を確保できます。ただし、一部の増分レプリケーション シナリオでは、アップストリームとダウンストリームのデータが絶えず変化しているため、アップストリームとダウンストリームの書き込みが継続的で中断されず、すべてのデータの整合性チェックを実行することが困難になります。

    以前は、ビジネスに影響を与える完全なデータを検証するためにビジネスを中断する必要がありました。現在、この機能を使用すると、ビジネスを中断することなく増分データ検証を実行できます。

    詳細については、 [ドキュメンテーション](/dm/dm-continuous-data-validation.md)を参照してください。

### TiDB データ共有サブスクリプション {#tidb-data-share-subscription}

-   TiCDC は変更されたログのstorageシンクへのレプリケートをサポートします (実験的) [#6797](https://github.com/pingcap/tiflow/issues/6797) @ [照信雨](https://github.com/zhaoxinyu)

    TiCDC は、変更されたログを Amazon S3、Azure Blob Storage、NFS、およびその他の S3 互換storageサービスにレプリケートすることをサポートしています。クラウドstorageは手頃な価格で使いやすいです。 Kafka を使用していない場合は、storageシンクを使用できます。 TiCDC は、変更されたログをファイルに保存してから、storageシステムに送信します。コンシューマー プログラムは、storageシステムから、新しく生成された変更済みログ ファイルを定期的に読み取ります。

    storageシンクは、canal-json および CSV 形式の変更ログをサポートしています。詳細については、 [ドキュメンテーション](/ticdc/ticdc-sink-to-cloud-storage.md)を参照してください。

-   TiCDC は、2 つのクラスター間の双方向レプリケーションをサポートします[#38587](https://github.com/pingcap/tidb/issues/38587) @ [ションジウェイ](https://github.com/xiongjiwei) @ [アスドンメン](https://github.com/asddongmen)

    TiCDC は、2 つの TiDB クラスター間の双方向レプリケーションをサポートしています。アプリケーション用に地理的に分散した複数のアクティブなデータ センターを構築する必要がある場合は、この機能をソリューションとして使用できます。 1 つの TiDB クラスターから別の TiDB クラスターへの TiCDC changefeeds の`bdr-mode = true`パラメーターを構成することにより、2 つの TiDB クラスター間で双方向のデータ レプリケーションを実現できます。

    詳細については、 [ドキュメンテーション](/ticdc/ticdc-bidirectional-replication.md)を参照してください。

-   TiCDC は TLS オンライン[#7908](https://github.com/pingcap/tiflow/issues/7908) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)の更新をサポートします

    データベース システムのセキュリティを維持するには、システムで使用される証明書の有効期限ポリシーを設定する必要があります。有効期限が過ぎると、システムは新しい証明書を必要とします。 TiCDC v6.5.0 は、TLS 証明書のオンライン更新をサポートしています。レプリケーション タスクを中断することなく、TiCDC は手動で介入する必要なく、証明書を自動的に検出して更新できます。

-   TiCDC の性能が大幅に向上[#7540](https://github.com/pingcap/tiflow/issues/7540) [#7478](https://github.com/pingcap/tiflow/issues/7478) [#7532](https://github.com/pingcap/tiflow/issues/7532) @ [スドジ](https://github.com/sdojjy) [@3AceShowHand](https://github.com/3AceShowHand)

    TiDB クラスターのテスト シナリオでは、TiCDC のパフォーマンスが大幅に向上しました。具体的には、データを Kafka にレプリケートするシナリオでは、1 つの TiCDC が処理できる最大行変更は 30K 行/秒に達し、レプリケーションレイテンシーは10 秒に短縮されます。 TiKV および TiCDC のローリング アップグレード中でも、レプリケーションのレイテンシーは 30 秒未満です。

    ディザスター リカバリー (DR) シナリオでは、TiCDC REDO ログと同期ポイントが有効になっている場合、 [データを Kafka に複製する](/replicate-data-to-kafka.md)の TiCDC スループットを 4000 行/秒から 35000 行/秒に向上させることができ、レプリケーションレイテンシーを2 秒に制限することができます。

### バックアップと復元 {#backup-and-restore}

-   TiDB Backup &amp; Restore は、スナップショット チェックポイント バックアップ[#38647](https://github.com/pingcap/tidb/issues/38647) @ [レヴルス](https://github.com/Leavrth)をサポートします。

    TiDB スナップショット バックアップは、チェックポイントからのバックアップの再開をサポートしています。バックアップと復元 (BR) で回復可能なエラーが発生すると、バックアップが再試行されます。ただし、リトライが数回失敗すると、 BR は終了します。チェックポイント バックアップ機能を使用すると、数十分のネットワーク障害など、より長い回復可能な障害を再試行できます。

    BRの終了後 1 時間以内にシステムを障害から回復しないと、バックアップ対象のスナップショット データが GC メカニズムによって再利用され、バックアップが失敗する可能性があることに注意してください。詳細については、 [ドキュメンテーション](/br/br-checkpoint.md)を参照してください。

-   PITRのパフォーマンスが著しく向上しました[@ジョッカウ](https://github.com/joccau)

    ログ復元段階では、1 つの TiKV の復元速度は 9 MiB/秒に達し、これは以前よりも 50% 高速です。復元速度はスケーラブルで、DR シナリオの RTO は大幅に短縮されます。 DR シナリオでの RPO は 5 分程度に短縮できます。通常のクラスターの運用と保守 (OM) では、たとえば、ローリング アップグレードが実行されるか、1 つの TiKV のみがダウンしている場合、RPO は 5 分になる可能性があります。

-   TiKV- BR GA: RawKV [#67](https://github.com/tikv/migration/issues/67) @ [ピンギュ](https://github.com/pingyu) @ [ハジンミン](https://github.com/haojinming)のバックアップと復元をサポート

    TiKV- BR は、TiKV クラスターで使用されるバックアップおよび復元ツールです。 TiKV と PD は、RawKV と呼ばれる TiDB なしで使用する場合、KV データベースを構成できます。 TiKV- BR は、 RawKV を使用する製品のデータのバックアップと復元をサポートします。 TiKV- BR は、 TiKV クラスターの[`api-version`](/tikv-configuration-file.md#api-version-new-in-v610) `API V1`から`API V2`にアップグレードすることもできます。

    詳細については、 [ドキュメンテーション](https://tikv.org/docs/latest/concepts/explore-tikv-features/backup-restore/)を参照してください。

## 互換性の変更 {#compatibility-changes}

### システム変数 {#system-variables}

| 変数名                                                                                                                       | タイプを変更 | 説明                                                                                                                                                                                                                                                                                                                                   |
| ------------------------------------------------------------------------------------------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`tidb_enable_amend_pessimistic_txn`](/system-variables.md#tidb_enable_amend_pessimistic_txn-new-in-v407)                 | 非推奨    | v6.5.0 以降、この変数は廃止され、TiDB はデフォルトで[メタデータ ロック](/metadata-lock.md)機能を使用して`Information schema is changed`エラーを回避します。                                                                                                                                                                                                                       |
| [`tidb_enable_outer_join_reorder`](/system-variables.md#tidb_enable_outer_join_reorder-new-in-v610)                       | 修正済み   | さらにテストした後、デフォルト値を`OFF`から`ON`に変更します。これは、 [結合したテーブルの再配置](/join-reorder.md)アルゴリズムの外部結合のサポートがデフォルトで有効になっていることを意味します。                                                                                                                                                                                                                     |
| [`tidb_cost_model_version`](/system-variables.md#tidb_cost_model_version-new-in-v620)                                     | 修正済み   | さらにテストを行った後、デフォルト値を`1`から`2`に変更します。これは、コスト モデル バージョン 2 がデフォルトでインデックスの選択と演算子の選択に使用されることを意味します。                                                                                                                                                                                                                                         |
| [`tidb_enable_gc_aware_memory_track`](/system-variables.md#tidb_enable_gc_aware_memory_track)                             | 修正済み   | デフォルト値を`ON`から`OFF`に変更します。 GC 対応メモリトラックはテストで不正確であることが判明し、追跡されるメモリサイズの分析結果が大きすぎるため、メモリトラックは無効になります。さらに、 Golang 1.19 では、GC 対応のメモリトラックによって追跡されるメモリは、メモリ全体にあまり影響を与えません。                                                                                                                                                                   |
| [`tidb_enable_metadata_lock`](/system-variables.md#tidb_enable_metadata_lock-new-in-v630)                                 | 修正済み   | さらにテストした後、デフォルト値を`OFF`から`ON`に変更します。これは、メタデータ ロック機能がデフォルトで有効になっていることを意味します。                                                                                                                                                                                                                                                           |
| [`tidb_enable_tiflash_read_for_write_stmt`](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-new-in-v630)     | 修正済み   | v6.5.0 から適用されます。 `INSERT` 、および`UPDATE` `DELETE`含む SQL ステートメントの読み取り操作をTiFlashにプッシュできるかどうかを制御します。デフォルト値は`OFF`です。                                                                                                                                                                                                                       |
| [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)                               | 修正済み   | さらにテストした後、デフォルト値を`OFF`から`ON`に変更します。つまり、 `ADD INDEX`と`CREATE INDEX`のアクセラレーションがデフォルトで有効になります。                                                                                                                                                                                                                                          |
| [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)                                                       | 修正済み   | TiDB v6.5.0 より前のバージョンでは、この変数を使用して、クエリのメモリクォータのしきい値を設定します。 TiDB v6.5.0 以降のバージョンでは、DML ステートメントのメモリをより正確に制御するために、この変数を使用してセッションのメモリクォータのしきい値を設定します。                                                                                                                                                                                     |
| [`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40)                                                  | 修正済み   | v6.5.0 以降、TiDB ノード間の負荷分散を最適化するために、この変数が`closest-adaptive`に設定され、読み取り要求の推定結果が[`tidb_adaptive_closest_read_threshold`](/system-variables.md#tidb_adaptive_closest_read_threshold-new-in-v630)以上の場合、 `closest-adaptive`構成が有効になる TiDB ノードの数が制限されます。これは、TiDB ノードが最も少ないアベイラビリティ ゾーン内の TiDB ノードの数と常に同じであり、他の TiDB ノードはリーダー レプリカから自動的に読み取ります。 |
| [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)                                   | 修正済み   | デフォルト値を`0`から`80%`に変更します。 TiDB グローバルメモリコントロールが GA になると、このデフォルト値の変更により、デフォルトでメモリコントロールが有効になり、TiDB インスタンスのメモリ制限がデフォルトで合計メモリの 80% に設定されます。                                                                                                                                                                                               |
| [`default_password_lifetime`](/system-variables.md#default_password_lifetime-new-in-v650)                                 | 新規追加   | パスワードの自動有効期限切れのグローバル ポリシーを設定して、ユーザーが定期的にパスワードを変更することを要求します。デフォルト値`0`は、パスワードが期限切れにならないことを示します。                                                                                                                                                                                                                                        |
| [`disconnect_on_expired_password`](/system-variables.md#disconnect_on_expired_password-new-in-v650)                       | 新規追加   | パスワードの有効期限が切れたときに TiDB がクライアント接続を切断するかどうかを示します。この変数は読み取り専用です。                                                                                                                                                                                                                                                                        |
| [`password_history`](/system-variables.md#password_history-new-in-v650)                                                   | 新規追加   | この変数は、TiDB がパスワードの変更回数に基づいてパスワードの再利用を制限できるパスワード再利用ポリシーを確立するために使用されます。デフォルト値`0`は、パスワードの変更回数に基づいてパスワード再利用ポリシーを無効にすることを意味します。                                                                                                                                                                                                           |
| [`password_reuse_interval`](/system-variables.md#password_reuse_interval-new-in-v650)                                     | 新規追加   | この変数は、経過時間に基づいて TiDB がパスワードの再利用を制限できるパスワード再利用ポリシーを確立するために使用されます。デフォルト値`0`は、経過時間に基づくパスワード再利用ポリシーを無効にすることを意味します。                                                                                                                                                                                                                       |
| [`tidb_auto_build_stats_concurrency`](/system-variables.md#tidb_auto_build_stats_concurrency-new-in-v650)                 | 新規追加   | この変数は、統計の自動更新の同時実行を設定するために使用されます。デフォルト値は`1`です。                                                                                                                                                                                                                                                                                       |
| [`tidb_cdc_write_source`](/system-variables.md#tidb_cdc_write_source-new-in-v650)                                         | 新規追加   | この変数が 0 以外の値に設定されている場合、このセッションで書き込まれたデータは TiCDC によって書き込まれたと見なされます。この変数は、TiCDC によってのみ変更できます。どのような場合でも、この変数を手動で変更しないでください。                                                                                                                                                                                                             |
| [`tidb_index_merge_intersection_concurrency`](/system-variables.md#tidb_index_merge_intersection_concurrency-new-in-v650) | 新規追加   | インデックス マージが実行する交差操作の最大同時実行数を設定します。これは、TiDB が動的プルーニング モードで分割されたテーブルにアクセスする場合にのみ有効です。                                                                                                                                                                                                                                                  |
| [`tidb_source_id`](/system-variables.md#tidb_source_id-new-in-v650)                                                       | 新規追加   | この変数は、 [双方向レプリケーション](/ticdc/ticdc-bidirectional-replication.md)クラスターで異なるクラスター ID を構成するために使用されます。                                                                                                                                                                                                                                     |
| [`tidb_sysproc_scan_concurrency`](/system-variables.md#tidb_sysproc_scan_concurrency-new-in-v650)                         | 新規追加   | この変数は、TiDB が内部 SQL ステートメント (統計の自動更新など) を実行するときに実行されるスキャン操作の並行性を設定するために使用されます。デフォルト値は`1`です。                                                                                                                                                                                                                                           |
| [`tidb_ttl_delete_batch_size`](/system-variables.md#tidb_ttl_delete_batch_size-new-in-v650)                               | 新規追加   | この変数は、TTL ジョブの`DELETE`つのトランザクションで削除できる行の最大数を設定するために使用されます。                                                                                                                                                                                                                                                                           |
| [`tidb_ttl_delete_rate_limit`](/system-variables.md#tidb_ttl_delete_rate_limit-new-in-v650)                               | 新規追加   | この変数は、TTL ジョブの単一ノードで 1 秒あたりに許可される`DELETE`ステートメントの最大数を制限するために使用されます。この変数が`0`に設定されている場合、制限は適用されません。                                                                                                                                                                                                                                    |
| [`tidb_ttl_delete_worker_count`](/system-variables.md#tidb_ttl_delete_worker_count-new-in-v650)                           | 新規追加   | この変数は、各 TiDB ノードでの TTL ジョブの最大同時実行数を設定するために使用されます。                                                                                                                                                                                                                                                                                    |
| [`tidb_ttl_job_enable`](/system-variables.md#tidb_ttl_job_enable-new-in-v650)                                             | 新規追加   | この変数は、TTL ジョブを有効にするかどうかを制御するために使用されます。 `OFF`に設定されている場合、TTL 属性を持つすべてのテーブルは、期限切れデータのクリーンアップを自動的に停止します。                                                                                                                                                                                                                                 |
| [`tidb_ttl_job_run_interval`](/system-variables.md#tidb_ttl_job_run_interval-new-in-v650)                                 | 新規追加   | この変数は、バックグラウンドでの TTL ジョブのスケジューリング間隔を制御するために使用されます。たとえば、現在の値が`1h0m0s`に設定されている場合、TTL 属性を持つ各テーブルは、1 時間ごとに期限切れのデータをクリーンアップします。                                                                                                                                                                                                           |
| [`tidb_ttl_job_schedule_window_start_time`](/system-variables.md#tidb_ttl_job_schedule_window_start_time-new-in-v650)     | 新規追加   | この変数は、バックグラウンドでの TTL ジョブのスケジューリング ウィンドウの開始時刻を制御するために使用されます。この変数の値を変更するときは、ウィンドウが小さいと期限切れデータのクリーンアップが失敗する可能性があることに注意してください。                                                                                                                                                                                                           |
| [`tidb_ttl_job_schedule_window_end_time`](/system-variables.md#tidb_ttl_job_schedule_window_end_time-new-in-v650)         | 新規追加   | この変数は、バックグラウンドでの TTL ジョブのスケジューリング ウィンドウの終了時間を制御するために使用されます。この変数の値を変更するときは、ウィンドウが小さいと期限切れデータのクリーンアップが失敗する可能性があることに注意してください。                                                                                                                                                                                                           |
| [`tidb_ttl_scan_batch_size`](/system-variables.md#tidb_ttl_scan_batch_size-new-in-v650)                                   | 新規追加   | この変数は、TTL ジョブで期限切れデータをスキャンするために使用される各`SELECT`ステートメントの`LIMIT`値を設定するために使用されます。                                                                                                                                                                                                                                                         |
| [`tidb_ttl_scan_worker_count`](/system-variables.md#tidb_ttl_scan_worker_count-new-in-v650)                               | 新規追加   | この変数は、各 TiDB ノードでの TTL スキャン ジョブの最大同時実行数を設定するために使用されます。                                                                                                                                                                                                                                                                               |
| [`validate_password.check_user_name`](/system-variables.md#validate_passwordcheck_user_name-new-in-v650)                  | 新規追加   | パスワード複雑度チェックのチェック項目。パスワードがユーザー名と一致するかどうかをチェックします。この変数は、 [`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650)が有効になっている場合にのみ有効です。デフォルト値は`ON`です。                                                                                                                                                      |
| [`validate_password.dictionary`](/system-variables.md#validate_passworddictionary-new-in-v650)                            | 新規追加   | パスワード複雑度チェックのチェック項目。パスワードが辞書の単語と一致するかどうかをチェックします。この変数は、 [`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650)が有効で、 [`validate_password.policy`](/system-variables.md#validate_passwordpolicy-new-in-v650)が`2` (STRONG) に設定されている場合にのみ有効です。デフォルト値は`""`です。                                             |
| [`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650)                                    | 新規追加   | この変数は、パスワードの複雑さのチェックを実行するかどうかを制御します。この変数が`ON`に設定されている場合、TiDB はパスワードの設定時にパスワードの複雑さのチェックを実行します。デフォルト値は`OFF`です。                                                                                                                                                                                                                         |
| [`validate_password.length`](/system-variables.md#validate_passwordlength-new-in-v650)                                    | 新規追加   | パスワード複雑度チェックのチェック項目。パスワードの長さが十分かどうかをチェックします。デフォルトでは、最小パスワード長は`8`です。この変数は、 [`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650)が有効になっている場合にのみ有効です。                                                                                                                                                  |
| [`validate_password.mixed_case_count`](/system-variables.md#validate_passwordmixed_case_count-new-in-v650)                | 新規追加   | パスワード複雑度チェックのチェック項目。パスワードに十分な大文字と小文字が含まれているかどうかをチェックします。この変数は、 [`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650)が有効で、 [`validate_password.policy`](/system-variables.md#validate_passwordpolicy-new-in-v650)が`1` (MEDIUM) 以上に設定されている場合にのみ有効です。デフォルト値は`1`です。                                     |
| [`validate_password.number_count`](/system-variables.md#validate_passwordnumber_count-new-in-v650)                        | 新規追加   | パスワード複雑度チェックのチェック項目。パスワードに十分な数字が含まれているかどうかをチェックします。この変数は、 [`validate_password.enable`](/system-variables.md#password_reuse_interval-new-in-v650)が有効で、 [`validate_password.policy`](/system-variables.md#validate_passwordpolicy-new-in-v650)が`1` (MEDIUM) 以上に設定されている場合にのみ有効です。デフォルト値は`1`です。                                          |
| [`validate_password.policy`](/system-variables.md#validate_passwordpolicy-new-in-v650)                                    | 新規追加   | この変数は、パスワードの複雑さチェックのポリシーを制御します。値は`0` 、 `1` 、または`2`です (LOW、MEDIUM、または STRONG に対応)。この変数は、 [`validate_password.enable`](/system-variables.md#password_reuse_interval-new-in-v650)が有効になっている場合にのみ有効です。デフォルト値は`1`です。                                                                                                                       |
| [`validate_password.special_char_count`](/system-variables.md#validate_passwordspecial_char_count-new-in-v650)            | 新規追加   | パスワード複雑度チェックのチェック項目。パスワードに十分な特殊文字が含まれているかどうかをチェックします。この変数は、 [`validate_password.enable`](/system-variables.md#password_reuse_interval-new-in-v650)が有効で、 [`validate_password.policy`](/system-variables.md#validate_passwordpolicy-new-in-v650)が`1` (MEDIUM) 以上に設定されている場合にのみ有効です。デフォルト値は`1`です。                                        |

### コンフィグレーションファイルのパラメーター {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメーター                                                                                           | タイプを変更 | 説明                                                                                                                                                   |
| -------------- | ---------------------------------------------------------------------------------------------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | [`server-memory-quota`](/tidb-configuration-file.md#server-memory-quota-new-in-v409)                       | 非推奨    | v6.5.0 以降、この構成アイテムは非推奨になりました。代わりに、システム変数[`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)を使用してメモリをグローバルに管理します。 |
| TiDB           | [`disconnect-on-expired-password`](/tidb-configuration-file.md#disconnect-on-expired-password-new-in-v650) | 新規追加   | パスワードの有効期限が切れたときに TiDB がクライアント接続を切断するかどうかを決定します。デフォルト値は`true`です。これは、パスワードの有効期限が切れるとクライアント接続が切断されることを意味します。                                           |
| TiKV           | `raw-min-ts-outlier-threshold`                                                                             | 削除しました | この構成アイテムは v6.4.0 で廃止され、v6.5.0 で削除されました。                                                                                                              |
| TiKV           | [`cdc.min-ts-interval`](/tikv-configuration-file.md#min-ts-interval)                                       | 修正済み   | CDCレイテンシーを短縮するために、デフォルト値が`1s`から`200ms`に変更されました。                                                                                                      |
| TiKV           | [`memory-use-ratio`](/tikv-configuration-file.md#memory-use-ratio-new-in-v650)                             | 新規追加   | PITR ログ リカバリで使用可能なメモリと合計システムメモリの比率を示します。                                                                                                             |
| TiCDC          | [`sink.terminator`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)                 | 新規追加   | 2 つのデータ変更イベントを区切るために使用される行ターミネータを示します。デフォルトでは値は空です。つまり、 `\r\n`が使用されます。                                                                               |
| TiCDC          | [`sink.date-separator`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)             | 新規追加   | ファイル ディレクトリの日付区切りの種類を示します。値のオプションは`none` 、 `year` 、 `month` 、および`day`です。 `none`はデフォルト値で、日付が区切られていないことを意味します。                                         |
| TiCDC          | [`sink.enable-partition-separator`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters) | 新規追加   | 区切り文字列としてパーティションを使用するかどうかを指定します。デフォルト値は`false`です。これは、テーブル内のパーティションが別々のディレクトリに格納されないことを意味します。                                                         |
| TiCDC          | [`sink.csv.delimiter`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)              | 新規追加   | フィールド間の区切り文字を示します。値は ASCII 文字でなければならず、デフォルトは`,`です。                                                                                                   |
| TiCDC          | [`sink.csv.quote`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)                  | 新規追加   | フィールドを囲む引用.デフォルト値は`"`です。値が空の場合、引用符は使用されません。                                                                                                          |
| TiCDC          | [`sink.csv.null`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)                   | 新規追加   | CSV 列が null の場合に表示される文字を指定します。デフォルト値は`\N`です。                                                                                                         |
| TiCDC          | [`sink.csv.include-commit-ts`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)      | 新規追加   | commit-ts を CSV 行に含めるかどうかを指定します。デフォルト値は`false`です。                                                                                                    |

### その他 {#others}

-   v6.5.0 以降、 `mysql.user`テーブルに`Password_reuse_history`と`Password_reuse_time`の 2 つの新しい列が追加されました。
-   v6.5.0 以降、デフォルトで[指数加速度](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)機能が有効になっています。この機能は[単一の`ALTER TABLE`ステートメントで複数の列またはインデックスを変更する](/sql-statements/sql-statement-alter-table.md)と完全には互換性がありません。インデックス アクセラレーションを使用して一意のインデックスを追加する場合は、同じステートメントで他の列またはインデックスを変更しないようにする必要があります。この機能は[PITR (ポイントインタイム リカバリ)](/br/br-pitr-guide.md)とも互換性がありません。インデックス アクセラレーション機能を使用する場合、PITR バックアップ タスクがバックグラウンドで実行されていないことを確認する必要があります。そうしないと、予期しない結果が生じる可能性があります。詳細については、 [ドキュメンテーション](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)を参照してください。

## 非推奨の機能 {#deprecated-feature}

v6.5.0 以降、v4.0.7 で導入された[`AMEND TRANSACTION`](/system-variables.md#tidb_enable_amend_pessimistic_txn-new-in-v407)メカニズムは廃止され、 [メタデータ ロック](/metadata-lock.md)に置き換えられました。

## 改良点 {#improvements}

-   TiDB

    -   `BIT`と`CHAR`列の場合、 `INFORMATION_SCHEMA.COLUMNS`の結果を MySQL [#25472](https://github.com/pingcap/tidb/issues/25472) @ [ホーキングレイ](https://github.com/hawkingrei)と一致させる
    -   ノードが異常な場合のパフォーマンスへの影響を軽減するために、 TiFlash MPP モードでTiFlashノードの TiDB プローブ メカニズムを最適化します[#39686](https://github.com/pingcap/tidb/issues/39686) @ [ハッカーショーン](https://github.com/hackersean)

-   TiKV

    -   ディスクスペースを使い果たすのを避けるために十分なスペースがない場合、 Raft Engineへの書き込みを停止します[#13642](https://github.com/tikv/tikv/issues/13642) @ [嘉陽正](https://github.com/jiayang-zheng)
    -   `json_valid`機能をTiKV [#13571](https://github.com/tikv/tikv/issues/13571) @ [立振歓](https://github.com/lizhenhuan)に押し下げることをサポート
    -   1 回のバックアップ要求で複数範囲のデータのバックアップをサポート[#13701](https://github.com/tikv/tikv/issues/13701) @ [レヴルス](https://github.com/Leavrth)
    -   rusoto ライブラリ[#13751](https://github.com/tikv/tikv/issues/13751) @ [3ポインター](https://github.com/3pointer)を更新して、AWS のアジア パシフィック リージョン (ap-southeast-3) へのデータのバックアップをサポートします。
    -   悲観的トランザクション競合を減らす[#13298](https://github.com/tikv/tikv/issues/13298) @ [みょんけみんた](https://github.com/MyonKeminta)
    -   外部storageオブジェクト[#13798](https://github.com/tikv/tikv/issues/13798) @ [ユジュンセン](https://github.com/YuJuncen)をキャッシュすることにより、回復のパフォーマンスを向上させます
    -   専用スレッドで CheckLeader を実行して、TiCDC レプリケーションのレイテンシーを短縮します[#13774](https://github.com/tikv/tikv/issues/13774) @ [大静脈](https://github.com/overvenus)
    -   チェックポイント[#13824](https://github.com/tikv/tikv/issues/13824) @ [ユジュンセン](https://github.com/YuJuncen)のプル モデルをサポート
    -   crossbeam-channel [#13815](https://github.com/tikv/tikv/issues/13815) @ [スティックナーフ](https://github.com/sticnarf)を更新することにより、送信側でのスピンの問題を回避します
    -   TiKV [#13849](https://github.com/tikv/tikv/issues/13849) @ [cfzjywxk](https://github.com/cfzjywxk)でコプロセッサータスク処理をサポート
    -   TiKV にリージョン[#13648](https://github.com/tikv/tikv/issues/13648) @ [Lykxサシネーター](https://github.com/LykxSassinator)をウェイクアップするように通知することで、障害回復の待ち時間を短縮します
    -   コードの最適化[#13827](https://github.com/tikv/tikv/issues/13827) @ [ビジージェイ](https://github.com/BusyJay)により、要求されたメモリ使用量のサイズを減らします
    -   Raft拡張機能を導入してコードの拡張性を向上させる[#13827](https://github.com/tikv/tikv/issues/13827) @ [ビジージェイ](https://github.com/BusyJay)
    -   tikv-ctl を使用して、特定のキー範囲に含まれるリージョンを照会するサポート[#13760](https://github.com/tikv/tikv/issues/13760) [@HuSharp](https://github.com/HuSharp)
    -   更新されていないが継続的にロックされている行の読み取りおよび書き込みパフォーマンスを改善する[#13694](https://github.com/tikv/tikv/issues/13694) [@sticnarf](https://github.com/sticnarf)

-   PD

    -   ロックの粒度を最適化して、ロックの競合を減らし、高い並行性の下でのハートビートの処理能力を向上させます[#5586](https://github.com/tikv/pd/issues/5586) @ [ルルング](https://github.com/rleungx)
    -   大規模クラスタ向けにスケジューラのパフォーマンスを最適化し、スケジューリング ポリシーの本番を高速化[#5473](https://github.com/tikv/pd/issues/5473) @ [バタフライ](https://github.com/bufferflies)
    -   Regions [#5606](https://github.com/tikv/pd/issues/5606) @ [ルルング](https://github.com/rleungx)のロード速度を改善
    -   リージョンハートビート[#5648](https://github.com/tikv/pd/issues/5648) @ [ルルング](https://github.com/rleungx)の最適化された処理により、不要なオーバーヘッドを削減
    -   自動ガベージコレクションの機能を追加する墓石ストア[#5348](https://github.com/tikv/pd/issues/5348) @ [ノルーチ](https://github.com/nolouch)

-   TiFlash

    -   SQL 側にバッチ処理がないシナリオでの書き込みパフォーマンスの向上[#6404](https://github.com/pingcap/tiflash/issues/6404) @ [リデジュ](https://github.com/lidezhu)
    -   `explain analyze`出力[#5926](https://github.com/pingcap/tiflash/issues/5926) @ [ホンユニャン](https://github.com/hongyunyan)に TableFullScan の詳細を追加します。

-   ツール

    -   TiDB ダッシュボード

        -   スロー クエリ ページに次の 3 つの新しいフィールドを追加します。 [#1451](https://github.com/pingcap/tidb-dashboard/issues/1451) @ [shhdgit](https://github.com/shhdgit)

    -   バックアップと復元 (BR)

        -   バックアップ ログ データの消去プロセス中のBRメモリ使用量を最適化する[#38869](https://github.com/pingcap/tidb/issues/38869) @ [レヴルス](https://github.com/Leavrth)
        -   復元プロセス中の PD リーダー スイッチによって引き起こされる復元失敗の問題を修正します[#36910](https://github.com/pingcap/tidb/issues/36910) @ [MoCuishle28](https://github.com/MoCuishle28)
        -   ログ バックアップ[#13867](https://github.com/tikv/tikv/issues/13867) @ [ユジュンセン](https://github.com/YuJuncen)で OpenSSL プロトコルを使用して TLS の互換性を向上させる

    -   TiCDC

        -   Kafka プロトコル エンコーダーのパフォーマンスを向上させる[#7540](https://github.com/pingcap/tiflow/issues/7540) [#7532](https://github.com/pingcap/tiflow/issues/7532) [#7543](https://github.com/pingcap/tiflow/issues/7543) @ [3AceShowHand](https://github.com/3AceShowHand) @ [スドジ](https://github.com/sdojjy)

    -   TiDB データ移行 (DM)

        -   ブロック リスト[#7622](https://github.com/pingcap/tiflow/pull/7622) @ [GMHDBJD](https://github.com/GMHDBJD)内のテーブルのデータを解析しないことで、DM のデータ レプリケーション パフォーマンスを向上させます。
        -   非同期書き込みと一括書き込み[#7580](https://github.com/pingcap/tiflow/pull/7580) @ [GMHDBJD](https://github.com/GMHDBJD)でDM中継の書き込み効率アップ
        -   DM precheck [#7621](https://github.com/pingcap/tiflow/issues/7621) @ [ぶちゅとでごう](https://github.com/buchuitoudegou)のエラー メッセージを最適化する
        -   古い MySQL バージョン[#5017](https://github.com/pingcap/tiflow/issues/5017) @ [lyzx2001](https://github.com/lyzx2001)に対する`SHOW SLAVE HOSTS`の互換性を改善します。

## バグの修正 {#bug-fixes}

-   TiDB

    -   場合によっては、チャンク再利用機能でメモリチャンクが誤用される問題を修正します。 [#38917](https://github.com/pingcap/tidb/issues/38917) @ [キープラーニング20221](https://github.com/keeplearning20221)
    -   `tidb_constraint_check_in_place_pessimistic`の内部セッションがグローバル設定[#38766](https://github.com/pingcap/tidb/issues/38766) @ [エキキシウム](https://github.com/ekexium)の影響を受ける可能性がある問題を修正します
    -   `AUTO_INCREMENT`列が`CHECK`制約[#38894](https://github.com/pingcap/tidb/issues/38894) @ [ヤンケアオ](https://github.com/YangKeao)で機能しない問題を修正
    -   `INSERT IGNORE INTO`を使用して`STRING`型のデータを`SMALLINT`型の自動インクリメント列に挿入すると、エラー[#38483](https://github.com/pingcap/tidb/issues/38483) @ [ホーキングレイ](https://github.com/hawkingrei)が発生する問題を修正します。
    -   パーティションテーブル[#38932](https://github.com/pingcap/tidb/issues/38932) @ [ミヨンス](https://github.com/mjonss)の分割列のリネーム操作でヌルポインタエラーが発生する問題を修正
    -   パーティションテーブルのパーティション列を変更すると、DDL が[#38530](https://github.com/pingcap/tidb/issues/38530) @ [ミヨンス](https://github.com/mjonss)でハングする問題を修正します
    -   v4.0.16 から v6.4.0 [#38980](https://github.com/pingcap/tidb/issues/38980) @ [接線](https://github.com/tangenta)にアップグレードした後、 `ADMIN SHOW JOB`操作がパニックになる問題を修正します。
    -   `tidb_decode_key`関数が分割されたテーブル[#39304](https://github.com/pingcap/tidb/issues/39304) @ [定義済み2014](https://github.com/Defined2014)のエンコーディングを正しく解析できない問題を修正します。
    -   ログ ローテーション[#38941](https://github.com/pingcap/tidb/issues/38941) @ [xhebox](https://github.com/xhebox)中に gRPC エラー ログが正しいログ ファイルにリダイレクトされない問題を修正します。
    -   TiKV が読み取りエンジン[#39344](https://github.com/pingcap/tidb/issues/39344) @ [イサール](https://github.com/Yisaer)として構成されていない場合、TiDB が`BEGIN; SELECT... FOR UPDATE;`ポイント クエリに対して予期しない実行プランを生成する問題を修正します。
    -   誤って`StreamAgg` TiFlashに押し下げると、間違った結果[#39266](https://github.com/pingcap/tidb/issues/39266) @ [fixdb](https://github.com/fixdb)になる問題を修正します。

-   TiKV

    -   Raft Engine ctl [#11119](https://github.com/tikv/tikv/issues/11119) @ [タボキー](https://github.com/tabokie)のエラーを修正
    -   tikv-ctl [#13515](https://github.com/tikv/tikv/issues/13515) @ [国翔CN](https://github.com/guoxiangCN)で`compact raft`コマンド実行時の`Get raft db is not allowed`エラーを修正
    -   TLS が有効な場合にログ バックアップが機能しない問題を修正します[#13867](https://github.com/tikv/tikv/issues/13867) @ [ユジュンセン](https://github.com/YuJuncen)
    -   Geometry フィールド タイプ[#13651](https://github.com/tikv/tikv/issues/13651) @ [ドヴィーデン](https://github.com/dveeden)のサポートの問題を修正します。
    -   新しい照合順序が有効になっていない場合、 `LIKE`演算子の`_`非 ASCII 文字と一致しないという問題を修正します[#13769](https://github.com/tikv/tikv/issues/13769) @ [ヤンケアオ](https://github.com/YangKeao)
    -   `reset-to-version`コマンド[#13829](https://github.com/tikv/tikv/issues/13829) @ [タボキー](https://github.com/tabokie)を実行すると tikv-ctl が予期せず終了する問題を修正

-   PD

    -   [#5701](https://github.com/tikv/pd/issues/5701) @ [フンドゥンDM](https://github.com/HunDunDM)を変更しないと`balance-hot-region-scheduler`構成が保持されない問題を修正
    -   `rank-formula-version`アップグレード プロセス中にアップグレード前の構成を保持しないという問題を修正します[#5698](https://github.com/tikv/pd/issues/5698) @ [フンドゥンDM](https://github.com/HunDunDM)

-   TiFlash

    -   TiFlash [#6159](https://github.com/pingcap/tiflash/issues/6159) @ [リデジュ](https://github.com/lidezhu)の再起動後、デルタレイヤーの列ファイルを圧縮できない問題を修正
    -   TiFlash File Open OPS が高すぎる問題を修正[#6345](https://github.com/pingcap/tiflash/issues/6345) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)

-   ツール

    -   バックアップと復元 (BR)

        -   BRがログバックアップデータを削除すると、削除してはいけないデータを誤って削除してしまう問題を修正[#38939](https://github.com/pingcap/tidb/issues/38939) @ [レヴルス](https://github.com/Leavrth)
        -   データベースまたはテーブル[#39150](https://github.com/pingcap/tidb/issues/39150) @ [MoCuishle28](https://github.com/MoCuishle28)の照合に古いフレームワークを使用すると、復元タスクが失敗する問題を修正します
        -   Alibaba Cloud と Huawei Cloud が Amazon S3storageと完全に互換性がないためにバックアップが失敗する問題を修正します[#39545](https://github.com/pingcap/tidb/issues/39545) @ [3ポインター](https://github.com/3pointer)

    -   TiCDC

        -   PD リーダーが[#7470](https://github.com/pingcap/tiflow/issues/7470) @ [ゼミン州](https://github.com/zeminzhou)でクラッシュすると TiCDC がスタックする問題を修正
        -   最初に DDL ステートメントを実行し、次に changefeed [#7682](https://github.com/pingcap/tiflow/issues/7682) @ [アスドンメン](https://github.com/asddongmen)を一時停止して再開するシナリオで発生したデータ損失を修正
        -   TiFlash [#7744](https://github.com/pingcap/tiflow/issues/7744) @ [大静脈](https://github.com/overvenus)の新しいバージョンがある場合、TiCDC が誤ってエラーを報告する問題を修正します。
        -   ダウンストリーム ネットワークが使用できない場合にシンクコンポーネントがスタックする問題を修正します[#7706](https://github.com/pingcap/tiflow/issues/7706) @ [ヒック](https://github.com/hicqu)
        -   ユーザーがレプリケーション タスクをすばやく削除してから、同じタスク名で別のタスクを作成すると、データが失われる問題を修正します[#7657](https://github.com/pingcap/tiflow/issues/7657) @ [大静脈](https://github.com/overvenus)

    -   TiDB データ移行 (DM)

        -   アップストリーム データベースで GTID モードが有効になっているが、データ[#7037](https://github.com/pingcap/tiflow/issues/7037) @ [リウメンギャ94](https://github.com/liumengya94)がない場合に`task-mode:all`タスクを開始できない問題を修正します。
        -   既存のワーカーが[#7658](https://github.com/pingcap/tiflow/issues/7658) @ [GMHDBJD](https://github.com/GMHDBJD)を終了する前に新しい DM ワーカーがスケジュールされると、データが複数回レプリケートされる問題を修正します
        -   アップストリーム データベースが正規表現を使用して権限を付与する場合、DM 事前チェックが渡されない問題を修正します[#7645](https://github.com/pingcap/tiflow/issues/7645) @ [ランス6716](https://github.com/lance6716)

    -   TiDB Lightning

        -   TiDB Lightning が巨大なソース データ ファイルをインポートするときのメモリリークの問題を修正します[#39331](https://github.com/pingcap/tidb/issues/39331) @ [dsdashun](https://github.com/dsdashun)
        -   TiDB Lightning がデータの並列インポート時に競合を正しく検出できない問題を修正[#39476](https://github.com/pingcap/tidb/issues/39476) @ [dsdashun](https://github.com/dsdashun)

## 寄稿者 {#contributors}

TiDB コミュニティの次の貢献者に感謝します。

-   [e1ijah1](https://github.com/e1ijah1)
-   [国翔CN](https://github.com/guoxiangCN) (初めての投稿者)
-   [嘉陽正](https://github.com/jiayang-zheng)
-   [ジーフフスト](https://github.com/jiyfhust)
-   [ミケチェンウェイ](https://github.com/mikechengwei)
-   [ピンアンドブ](https://github.com/pingandb)
-   [サシャシュラ](https://github.com/sashashura)
-   [ソースリウ](https://github.com/sourcelliu)
-   [wxbty](https://github.com/wxbty)
