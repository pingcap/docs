---
title: TiDB 7.6.0 Release Notes
summary: TiDB 7.6.0 の新機能、互換性の変更、改善点、バグ修正について説明します。
---

# TiDB 7.6.0 リリースノート {#tidb-7-6-0-release-notes}

発売日：2024年1月25日

TiDB バージョン: 7.6.0

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.6/quick-start-with-tidb)

7.6.0 では、次の主な機能と改善が導入されています。

<table><thead><tr><th>カテゴリ</th><th>機能/拡張機能</th><th>説明</th></tr></thead><tbody><tr><td rowspan="4">スケーラビリティとパフォーマンス</td><td><a href="https://docs.pingcap.com/tidb/v7.6/sql-plan-management#cross-database-binding">データベース間のSQLバインディング</a></td><td>同じスキーマを持つ数百のデータベースを管理する場合、これらのデータベース全体にSQLバインディングを適用する必要があることがよくあります。例えば、SaaSまたはPaaSデータプラットフォームでは、各ユーザーは通常、同じスキーマを持つ別々のデータベースを操作し、それらに対して類似のSQLクエリを実行します。このような場合、各データベースにSQLを個別にバインドするのは現実的ではありません。TiDB v7.6.0では、スキーマが同等なすべてのデータベース間で一致するバインディングを可能にする、データベース間SQLバインディングが導入されています。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v7.6/br-snapshot-guide#restore-cluster-snapshots">スナップショットの復元を最大10倍高速化（実験的）</a></td><td> BR v7.6.0では、クラスターのスナップショット復元を高速化するための、実験的粗粒度リージョン分散アルゴリズムが導入されました。多数のTiKVノードを持つクラスターでは、このアルゴリズムにより、ノード間の負荷がより均等に分散され、ノードごとのネットワーク帯域幅がより有効に活用されるため、クラスターのリソース効率が大幅に向上します。いくつかの実環境では、この改善により復元プロセスが最大10倍程度高速化されることが示されています。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v7.6/ddl-v2">バッチ処理によるテーブル作成が最大 10 倍高速化 (実験的)</a></td><td> v7.6.0での新しいDDLアーキテクチャの実装により、バッチテーブル作成のパフォーマンスが大幅に向上し、最大10倍高速化しました。この大幅な機能強化により、多数のテーブル作成に必要な時間が大幅に短縮されます。この高速化は、数万から数十万に及ぶ大量のテーブルが頻繁に使用されるSaaSシナリオにおいて特に顕著です。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v7.6/tune-region-performance#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service">アクティブ PD フォロワーを使用して PD のリージョン情報クエリ サービスを強化します (実験的)</a></td><td> TiDB v7.6.0では、PDフォロワーがリージョン情報クエリサービスを提供できる実験的機能「Active PD Follower 」が導入されました。この機能により、多数のTiDBノードとリージョンを持つクラスターにおいて、PDクラスターの<code>GetRegion</code>および<code>ScanRegions</code>リクエスト処理能力が向上し、PDリーダーのCPU負荷が軽減されます。</td></tr><tr><td rowspan="2">信頼性と可用性</td><td><a href="https://docs.pingcap.com/tidb/v7.6/tiproxy-overview">TiProxy をサポート (実験的)</a></td><td>デプロイメント ツールを使用して簡単にデプロイできる TiProxy サービスを完全にサポートし、ローリング リスタート、アップグレード、またはスケーリング イベントを通じて TiDB への接続を管理および維持できるようにします。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v7.6/dm-compatibility-catalog">データ移行（DM）がMySQL 8.0（GA）を正式にサポート</a></td><td>これまで、DMを使用したMySQL 8.0からのデータ移行は実験的機能であり、本番環境ではご利用いただけませんでした。TiDB v7.6.0では、この機能の安定性と互換性が向上し、本番環境においてMySQL 8.0からTiDBへのデータ移行をスムーズかつ迅速に実行できるようになります。v7.6.0では、この機能が一般提供（GA）されます。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### スケーラビリティ {#scalability}

-   アクティブPDFollower機能を使用して、PDのリージョン情報クエリサービスのスケーラビリティを強化します（実験的） [＃7431](https://github.com/tikv/pd/issues/7431) @ [キャビンフィーバーB](https://github.com/CabinfeverB)

    多数のリージョンを持つTiDBクラスターでは、ハートビート処理とタスクのスケジューリングによるオーバーヘッドの増加により、PDリーダーのCPU負荷が高くなる可能性があります。クラスターに多数のTiDBインスタンスがあり、リージョン情報へのリクエストが同時に発生すると、PDリーダーのCPU負荷がさらに高まり、PDサービスが利用できなくなる可能性があります。

    高可用性を確保するため、TiDB v7.6.0では、PDのリージョン情報クエリサービスのスケーラビリティを向上させるActive PD Follower機能をサポートしています。Active PD Follower機能を有効にするには、システム変数[`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-new-in-v760)を`ON`に設定します。この機能を有効にすると、TiDBはリージョン情報リクエストをすべてのPDサーバーに均等に分散し、PDフォロワーもリージョンリクエストを処理できるようになるため、PDリーダーのCPU負荷が軽減されます。

    詳細については[ドキュメント](/tune-region-performance.md#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service)参照してください。

### パフォーマンス {#performance}

-   BRはスナップショットの復元速度を最大10倍向上させます（実験的） [＃33937](https://github.com/pingcap/tidb/issues/33937) [＃49886](https://github.com/pingcap/tidb/issues/49886) @ [3ポイントシュート](https://github.com/3pointer)

    TiDBクラスターのスケールアップに伴い、業務停止時間を最小限に抑えるために、障害発生時にクラスターを迅速に復旧することがますます重要になっています。バージョン7.6.0より前のバージョンでは、リージョン分散アルゴリズムがパフォーマンス復旧における主要なボトルネックとなっていました。バージョン7.6.0では、 BRはリージョン分散アルゴリズムを最適化し、復旧タスクを多数の小さなタスクに迅速に分割し、それらをすべてのTiKVノードに一括で分散します。新しい並列復旧アルゴリズムは、各TiKVノードのリソースを最大限に活用することで、迅速な並列復旧を実現します。いくつかの実環境において、大規模なリージョンシナリオにおいて、クラスターのスナップショット復旧速度が約10倍向上しました。

    新しい粗粒度リージョン散布アルゴリズムは実験的です。使用するには、 `br`コマンドの`--granularity="coarse-grained"`パラメータを設定します。例:

    ```bash
    br restore full \
    --pd "${PDIP}:2379" \
    --storage "s3://${Bucket}/${Folder}" \
    --s3.region "${region}" \
    --granularity "coarse-grained" \
    --send-credentials-to-tikv=true \ 
    --log-file restorefull.log
    ```

    詳細については[ドキュメント](/br/br-snapshot-guide.md#restore-cluster-snapshots)参照してください。

-   Titanエンジンはデフォルトで有効になっています[＃16245](https://github.com/tikv/tikv/issues/16245) @ [コナー1996](https://github.com/Connor1996) @ [v01dスター](https://github.com/v01dstar) @ [トニー・シュッキ](https://github.com/tonyxuqqi)

    TiDB v7.6.0以降では、特にJSONをサポートするTiDB全体のテーブル書き込みシナリオをより適切にサポートするために、Titanエンジンがデフォルトで有効化されています。Titanエンジンは、32KBを超える大きな値をRocksDBのLSMツリーから自動的に分離し、Titanに個別に保存することで、大きな値の処理を最適化します。Titanエンジンは、TiKVで使用されるRocksDB機能と完全に互換性があります。この戦略的な変更は、書き込み増幅効果を軽減するだけでなく、大きな値を含む書き込み、更新、およびポイントクエリのシナリオにおけるパフォーマンスを向上させます。さらに、Range Scanシナリオでは、Titanエンジンの最適化により、デフォルト構成のRocksDBに匹敵するパフォーマンスを実現しています。

    この設定変更は、以前のバージョンとの互換性を維持しています。既存のTiDBクラスタをTiDB v7.6.0以降にアップグレードする場合、Titanエンジンはデフォルトで無効化されます。お客様の特定の要件に応じて、Titanエンジンを手動で有効化または無効化することができます。

    詳細については[ドキュメント](/storage-engine/titan-overview.md)参照してください。

-   以下の文字列関数を TiKV [＃48170](https://github.com/pingcap/tidb/issues/48170) @ [ゲンリキ](https://github.com/gengliqi)にプッシュダウンすることをサポートします

    -   `LOWER()`
    -   `UPPER()`

    詳細については[ドキュメント](/functions-and-operators/expressions-pushed-down.md)参照してください。

-   次の JSON関数をTiFlashにプッシュダウンすることをサポートします[＃48350](https://github.com/pingcap/tidb/issues/48350) [＃48986](https://github.com/pingcap/tidb/issues/48986) [＃48994](https://github.com/pingcap/tidb/issues/48994) [＃49345](https://github.com/pingcap/tidb/issues/49345) [＃49392](https://github.com/pingcap/tidb/issues/49392) @ [シーライズ](https://github.com/SeaRise) @ [イービン87](https://github.com/yibin87)

    -   `JSON_UNQUOTE()`
    -   `JSON_ARRAY()`
    -   `JSON_DEPTH()`
    -   `JSON_VALID()`
    -   `JSON_KEYS()`
    -   `JSON_CONTAINS_PATH()`

    詳細については[ドキュメント](/tiflash/tiflash-supported-pushdown-calculations.md)参照してください。

-   テーブル作成のパフォーマンスを10倍向上（実験的） [＃49752](https://github.com/pingcap/tidb/issues/49752) @ [gmhdbjd](https://github.com/gmhdbjd)

    以前のバージョンでは、上流データベースから数万のテーブルをTiDBに移行する場合、TiDBによるテーブル作成には時間がかかり、非効率的でした。v7.6.0以降、TiDBは新しいTiDB DDL V2アーキテクチャを導入しました。これは、システム変数[`tidb_ddl_version`](https://docs.pingcap.com/tidb/v7.6/system-variables#tidb_ddl_version-new-in-v760)設定することで有効にできます。以前のバージョンと比較して、新しいバージョンのDDLはバッチテーブル作成のパフォーマンスを10倍向上させ、テーブル作成時間を大幅に短縮します。

    詳細については[ドキュメント](https://docs.pingcap.com/tidb/v7.6/ddl-v2)参照してください。

-   定期的な完全圧縮をサポート（実験的） [＃12729](https://github.com/tikv/tikv/issues/12729) [アファインバーグ](https://github.com/afeinberg)

    TiDBはv7.6.0以降、TiKVの定期的なフルコンパクションをサポートしています。この機能は、ガベージコレクション（GC）の拡張機能として機能し、冗長なデータバージョンを排除します。アプリケーションのアクティビティに明らかなピークと谷が見られるようなシナリオでは、この機能を使用してアイドル期間中にデータコンパクションを実行し、ピーク時のパフォーマンスを向上させることができます。

    TiKV設定項目[`periodic-full-compact-start-times`](/tikv-configuration-file.md#periodic-full-compact-start-times-new-in-v760)設定することで、TiKVが定期的なフルコンパクションを開始する特定の時間を設定できます。また、 [`periodic-full-compact-start-max-cpu`](/tikv-configuration-file.md#periodic-full-compact-start-max-cpu-new-in-v760)設定することで、TiKVの定期的なフルコンパクションの最大CPU使用率を制限できます。デフォルト値は`periodic-full-compact-start-max-cpu`で、 `0.1`です。これは、TiKVのCPU使用率が10%未満の場合にのみ定期的なフルコンパクションがトリガーされることを意味します。これにより、アプリケーショントラフィックへの影響が軽減されます。

    詳細については[ドキュメント](/tikv-configuration-file.md#periodic-full-compact-start-times-new-in-v760)参照してください。

### 信頼性 {#reliability}

-   クロスデータベース実行プランバインディング[＃48875](https://github.com/pingcap/tidb/issues/48875) @ [qw4990](https://github.com/qw4990)

    TiDB上でSaaSサービスを実行する場合、データの保守と管理を容易にするために、テナントごとにデータを別々のデータベースに保存するのが一般的です。その結果、同じテーブルとインデックス定義、そして類似したSQL文を持つデータベースが数百個も存在することになります。このようなシナリオでは、あるSQL文の実行プランバインディングを作成すると、通常、このバインディングは他のデータベースのSQL文にも適用されます。

    このシナリオでは、TiDB v7.6.0 でクロスデータベース バインディング機能が導入され、異なるデータベースであっても、同じスキーマを持つ SQL 文に同じ実行プランをバインドできるようになりました。クロスデータベース バインディングを作成する際は、次の例に示すように、ワイルドカード`*`使用してデータベース名を表す必要があります。バインディングが作成されると、テーブル`t1`と`t2`どのデータベースにあるかに関係なく、TiDB はこのバインディングを使用して、同じスキーマを持つすべての SQL 文の実行プランを生成しようとします。これにより、データベースごとにバインディングを作成する手間が省けます。

    ```sql
    CREATE GLOBAL BINDING FOR
    USING
        SELECT /*+ merge_join(t1, t2) */ t1.id, t2.amount
        FROM *.t1, *.t2
        WHERE t1.id = t2.id;
    ```

    さらに、クロスデータベースバインディングは、ユーザーデータとワークロードの不均一な分散や急激な変化によって引き起こされるSQLパフォーマンスの問題を効果的に軽減します。SaaSプロバイダーは、クロスデータベースバインディングを使用することで、大量のデータを扱うユーザーによって検証された実行プランを修正し、すべてのユーザーの実行プランを修正できます。SaaSプロバイダーにとって、この機能は利便性とユーザーエクスペリエンスを大幅に向上させます。

    データベース間バインディングによって発生するシステムオーバーヘッド（1%未満）のため、TiDBはデフォルトでこの機能を無効にしています。データベース間バインディングを使用するには、まずシステム変数[`tidb_opt_enable_fuzzy_binding`](/system-variables.md#tidb_opt_enable_fuzzy_binding-new-in-v760)有効にする必要があります。

    詳細については[ドキュメント](/sql-plan-management.md#cross-database-binding)参照してください。

### 可用性 {#availability}

-   プロキシコンポーネントTiProxy (実験的) [＃413](https://github.com/pingcap/tiproxy/issues/413) @ [djshow832](https://github.com/djshow832) @ [xhebox](https://github.com/xhebox)サポート

    TiProxyは、TiDBの公式プロキシコンポーネントであり、クライアントとTiDBサーバーの間に配置されます。TiDBの負荷分散機能と接続の永続化関数を提供し、TiDBクラスタのワークロードのバランスを向上させ、メンテナンス作業中のデータベースへのユーザーアクセスに影響を与えません。

    -   TiDBクラスタのローリング再起動、ローリングアップグレード、スケールインなどのメンテナンス作業中は、TiDBサーバに変更が発生し、クライアントとTiDBサーバ間の接続が中断される可能性があります。TiProxyを使用することで、これらのメンテナンス作業中にクライアントへの影響を最小限に抑え、接続を他のTiDBサーバにスムーズに移行できます。
    -   TiDBサーバーへのクライアント接続は、他のTiDBサーバに動的に移行できません。複数のTiDBサーバのワークロードが不均衡な場合、クラスタ全体のリソースは十分であるにもかかわらず、特定のTiDBサーバでリソース枯渇が発生し、レイテンシーが大幅に増加するという状況が発生する可能性があります。この問題に対処するため、TiProxyは接続の動的移行機能を提供します。これにより、クライアントに影響を与えることなく、接続をあるTiDBサーバーから別のTiDBサーバに移行できるため、TiDBクラスタの負荷分散が実現します。

    TiProxy はTiUP、 TiDB Operator、および TiDB Dashboard に統合されており、構成、展開、保守が容易になります。

    詳細については[ドキュメント](/tiproxy/tiproxy-overview.md)参照してください。

### SQL {#sql}

-   `LOAD DATA`明示的なトランザクションとロールバックをサポート[＃49079](https://github.com/pingcap/tidb/pull/49079) @ [エキシウム](https://github.com/ekexium)

    MySQLと比較すると、TiDBのバージョン7.6.0より前のバージョンでは、 `LOAD DATA`文のトランザクション動作が異なるため、この文を使用する際には追加の調整が必要になる場合があります。具体的には、v4.0.0より前のバージョンでは、 `LOAD DATA`文は20000行ごとにコミットします。v4.0.0からv6.6.0までは、TiDBはデフォルトですべての行を1つのトランザクションでコミットし、システム変数[`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size)設定することで、一定数の行ごとにコミットすることもできます。v7.0.0以降では、 `tidb_dml_batch_size` `LOAD DATA`には適用されなくなり、TiDBはすべての行を1つのトランザクションでコミットします。

    v7.6.0以降、TiDBはトランザクション内の`LOAD DATA`他のDML文と同様に、特にMySQLと同様に処理します。トランザクション内の`LOAD DATA`文は、現在のトランザクションを自動的にコミットしたり、新しいトランザクションを開始したりしなくなりました。さらに、トランザクション内の`LOAD DATA`文は明示的にコミットまたはロールバックできます。さらに、 `LOAD DATA`文はTiDBのトランザクションモード設定（楽観的トランザクションまたは悲観的トランザクション）の影響を受けます。これらの改善により、MySQLからTiDBへの移行プロセスが簡素化され、より統一された制御可能なデータインポートエクスペリエンスが提供されます。

    詳細については[ドキュメント](/sql-statements/sql-statement-load-data.md)参照してください。

### DB操作 {#db-operations}

-   `FLASHBACK CLUSTER`正確なTSO [＃48372](https://github.com/pingcap/tidb/issues/48372) @ [生まれ変わった人](https://github.com/BornChanger/BornChanger)指定をサポートします

    TiDB v7.6.0では、フラッシュバック機能がより強力かつ正確になりました。指定した履歴タイムスタンプへのクラスターのロールバックをサポートするだけでなく、 `FLASHBACK CLUSTER TO TSO`使用して正確なリカバリ[TSO](/tso.md)を指定できるため、データリカバリの柔軟性が向上します。例えば、この機能はTiCDCと併用できます。データレプリケーションを一時停止し、下流のTiDBクラスターでオンライン前の読み取り/書き込みテストを実施した後、この機能により、クラスターは一時停止中のTSOに迅速かつ確実にロールバックし、TiCDCを使用してデータのレプリケーションを継続できます。これにより、オンライン前の検証プロセスが合理化され、データ管理が簡素化されます。

    ```sql
    FLASHBACK CLUSTER TO TSO 445494839813079041;
    ```

    詳細については[ドキュメント](/sql-statements/sql-statement-flashback-cluster.md)参照してください。

-   長時間アイドル状態のトランザクションの自動終了をサポート[＃48714](https://github.com/pingcap/tidb/pull/48714) @ [crazycs520](https://github.com/crazycs520)

    ネットワークの切断やアプリケーション障害が発生すると、 `COMMIT` / `ROLLBACK`ステートメントがデータベースへの転送に失敗する可能性があります。これにより、データベースロックの解放が遅れ、トランザクションロックの待機が発生し、データベース接続が急増する可能性があります。このような問題はテスト環境では一般的ですが、本番環境でも時折発生する可能性があり、迅速な診断が困難な場合があります。これらの問題を回避するために、TiDB v7.6.0 では、長時間アイドル状態のトランザクションを自動的に終了する[`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760)システム変数が導入されました。トランザクション状態のユーザーセッションがアイドル状態のままで、この変数の値を超える期間が経過すると、TiDB はトランザクションのデータベース接続を終了し、ロールバックします。

    詳細については[ドキュメント](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760)参照してください。

-   実行プランバインディングを作成するための構文を簡素化する[＃48876](https://github.com/pingcap/tidb/issues/48876) @ [qw4990](https://github.com/qw4990)

    TiDB v7.6.0では、実行プランバインディングを作成するための構文が簡素化されました。実行プランバインディングを作成する際に、元のSQL文を指定する必要がなくなりました。TiDBはヒント付きのSQL文に基づいて元のSQL文を識別します。この改善により、実行プランバインディングの作成の利便性が向上します。例えば、次のようになります。

    ```sql
    CREATE GLOBAL BINDING
    USING
    SELECT /*+ merge_join(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
    ```

    詳細については[ドキュメント](/sql-plan-management.md#create-a-binding-according-to-a-sql-statement)参照してください。

-   TiDB [＃49237](https://github.com/pingcap/tidb/pull/49237) @ [ジグアン](https://github.com/zyguan)の単一行レコードのサイズ制限を動的に変更する機能をサポート

    v7.6.0 より前では、トランザクション内の単一行レコードのサイズは、 TiDB 構成項目[`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v4010-and-v500)によって制限されていました。サイズ制限を超えると、 TiDB は`entry too large`エラーを返します。この場合、 TiDB 構成ファイルを手動で変更し、 TiDB を再起動して変更を有効にする必要があります。 管理オーバーヘッドを削減するために、 TiDB v7.6.0 では、 `txn-entry-size-limit`構成項目の値を動的に変更することをサポートするシステム変数[`tidb_txn_entry_size_limit`](/system-variables.md#tidb_txn_entry_size_limit-new-in-v760)が導入されました。 この変数のデフォルト値は`0`です。つまり、 TiDB はデフォルトで構成項目`txn-entry-size-limit`の値を使用します。 この変数がゼロ以外の値に設定されている場合、 TiDB はトランザクション内の行レコードのサイズをこの変数の値に制限します。 この改善により、 TiDB を再起動せずにシステム構成を調整する柔軟性が向上しました。

    詳細については[ドキュメント](/system-variables.md#tidb_txn_entry_size_limit-new-in-v760)参照してください。

-   BRはデフォルトで、ユーザーデータ[＃48567](https://github.com/pingcap/tidb/issues/48567) @ [生まれ変わった人](https://github.com/BornChanger) [＃49627](https://github.com/pingcap/tidb/issues/49627) @ [リーヴルス](https://github.com/Leavrth)などのシステムテーブルを復元します。

    v5.1.0以降、スナップショットをバックアップすると、 BRは`mysql`スキーマ内のシステムテーブルを自動的にバックアップしますが、デフォルトではこれらのシステムテーブルをリストアしません。v6.2.0では、 BRにパラメータ`--with-sys-table`が追加され、一部のシステムテーブルのデータのリストアがサポートされるようになりました。これにより、操作の柔軟性が向上します。

    管理オーバーヘッドをさらに削減し、より直感的なデフォルト動作を提供するため、v7.6.0以降、 BRはパラメータ`--with-sys-table`デフォルトで有効化します。つまり、 BRは復元時に一部のシステムテーブル、特にユーザーアカウントとテーブル統計データをデフォルトで復元します。この改善により、バックアップと復元の操作がより直感的になり、手動設定の負担が軽減され、全体的な操作性が向上します。

    詳細については[ドキュメント](/br/br-snapshot-guide.md)参照してください。

### 可観測性 {#observability}

-   リソース制御に関する可観測性を強化する[＃49318](https://github.com/pingcap/tidb/issues/49318) @ [栄光](https://github.com/glorv) @ [バッファフライ](https://github.com/bufferflies) @ [ノルーシュ](https://github.com/nolouch)

    リソースグループを使用してアプリケーションのワークロードを分離するユーザーが増えるにつれ、リソースコントロールはリソースグループに基づいた拡張データを提供します。これにより、リソースグループのワークロードと設定を監視し、次のような問題を迅速に特定し、正確に診断できるようになります。

    -   [遅いクエリ](/identify-slow-queries.md) : リソース グループ名、リソース ユニット (RU) の消費量、およびリソースの待機時間を追加します。
    -   [明細書概要表](/statement-summary-tables.md) : リソース グループ名、RU 消費量、リソースの待機時間を追加します。
    -   システム変数[`tidb_last_query_info`](/system-variables.md#tidb_last_query_info-new-in-v4014)に、SQL文によって消費されたリソース量[ロシア](/tidb-resource-control-ru-groups.md#what-is-request-unit-ru)示す新しいエントリ`ru_consumption`を追加します。この変数を使用して、セッション内の最後の文のリソース消費量を取得できます。
    -   リソース グループに基づいてデータベース メトリックを追加します: QPS/TPS、実行時間 (P999/P99/P95)、障害数、接続数。
    -   すべてのリソース グループの毎日消費された RU の履歴レコードを記録するために、システム テーブル[`request_unit_by_group`](/mysql-schema/mysql-schema.md#system-tables-related-to-resource-control)を追加します。

    詳細については、 [遅いクエリを特定する](/identify-slow-queries.md) 、 [明細書概要表](/statement-summary-tables.md) 、 [リソース管理の主要な監視指標](/grafana-resource-control-dashboard.md)参照してください。

### データ移行 {#data-migration}

-   MySQL 8.0 の移行のためのデータ移行 (DM) サポートが一般提供 (GA) [＃10405](https://github.com/pingcap/tiflow/issues/10405) @ [lyzx2001](https://github.com/lyzx2001)に開始されます

    これまで、DMを使用したMySQL 8.0からのデータ移行は実験的機能であり、本番環境ではご利用いただけませんでした。TiDB v7.6.0では、この機能の安定性と互換性が向上し、本番環境においてMySQL 8.0からTiDBへのデータ移行をスムーズかつ迅速に実行できるようになります。v7.6.0では、この機能が一般提供（GA）されます。

    詳細については[ドキュメント](/dm/dm-compatibility-catalog.md)参照してください。

-   TiCDC は、双方向レプリケーション (BDR) モードでの DDL ステートメントのレプリケーションをサポートしています (実験的) [＃10301](https://github.com/pingcap/tiflow/issues/10301) [＃48519](https://github.com/pingcap/tidb/issues/48519) @ [okJiang](https://github.com/okJiang) @ [アズドンメン](https://github.com/asddongmen)

    バージョン7.6.0以降、TiCDCは双方向レプリケーションが設定されたDDL文のレプリケーションをサポートします。以前は、TiCDCはDDL文のレプリケーションをサポートしていなかったため、TiCDCの双方向レプリケーションを利用するユーザーは、両方のTiDBクラスターに個別にDDL文を適用する必要がありました。この機能により、TiCDCはクラスターに`PRIMARY` BDRロールを割り当て、そのクラスターから下流のクラスターへのDDL文のレプリケーションを可能にします。

    詳細については[ドキュメント](/ticdc/ticdc-bidirectional-replication.md)参照してください。

-   TiCDCは、チェンジフィード[＃10289](https://github.com/pingcap/tiflow/issues/10289) @ [ホンユニャン](https://github.com/hongyunyan)の下流同期ステータスの照会をサポートしています。

    TiCDC v7.6.0以降、指定されたレプリケーションタスク（changefeed）の下流同期ステータスを照会するための新しいAPI `GET /api/v2/changefeed/{changefeed_id}/synced`が導入されました。このAPIを使用することで、TiCDCが受信した上流データが下流システムに完全に同期されているかどうかを確認できます。

    詳細については[ドキュメント](/ticdc/ticdc-open-api-v2.md#query-whether-a-specific-replication-task-is-completed)参照してください。

-   TiCDC は、CSV 出力プロトコル[＃9969](https://github.com/pingcap/tiflow/issues/9969) @ [張金鵬87](https://github.com/zhangjinpeng87)で 3 文字の区切り文字のサポートを追加しました。

    バージョン7.6.0以降、CSV出力プロトコルの区切り文字を1～3文字に指定できるようになりました。この変更により、TiCDCは2文字の区切り文字（ `||`や`$^`など）または3文字の区切り文字（ `|@|`など）を使用してファイル出力を生成するように設定できます。

    詳細については[ドキュメント](/ticdc/ticdc-csv.md)参照してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、v7.5.0から最新バージョン（v7.6.0）にアップグレードする際に知っておくべき互換性の変更点について説明します。v7.4.0以前のバージョンから最新バージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更点も確認する必要があるかもしれません。

### MySQLの互換性 {#mysql-compatibility}

-   TiDB v7.6.0より前のバージョンでは、 `LOAD DATA`操作はすべての行を単一のトランザクションでコミットするか、トランザクションをバッチでコミットしていました。これはMySQLの動作とは若干異なります。v7.6.0以降、TiDBはMySQLと同様にトランザクション内の`LOAD DATA`の操作を処理します。トランザクション内の`LOAD DATA`の文は、現在のトランザクションを自動的にコミットしたり、新しいトランザクションを開始したりしなくなりました。また、トランザクション内の`LOAD DATA`文は明示的にコミットまたはロールバックできます。さらに、 `LOAD DATA`文はTiDBのトランザクションモード設定（楽観的トランザクションまたは悲観的トランザクション）の影響を受けます[＃49079](https://github.com/pingcap/tidb/pull/49079) @ [エキシウム](https://github.com/ekexium)

### システム変数 {#system-variables}

| 変数名                                                                                                                 | タイプを変更   | 説明                                                                                                                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_auto_analyze_partition_batch_size`](/system-variables.md#tidb_auto_analyze_partition_batch_size-new-in-v640) | 修正済み     | さらにテストを行った後、デフォルト値を`1`から`128`に変更します。                                                                                                                                                                                                                                                                                |
| [`tidb_sysproc_scan_concurrency`](/system-variables.md#tidb_sysproc_scan_concurrency-new-in-v650)                   | 修正済み     | 大規模クラスターでは、 `scan`操作の同時実行性を`ANALYZE`ニーズに合わせて高めに調整できます。したがって、最大値を`256`から`4294967295`に変更します。                                                                                                                                                                                                                          |
| [`tidb_analyze_distsql_scan_concurrency`](/system-variables.md#tidb_analyze_distsql_scan_concurrency-new-in-v760)   | 新しく追加された | `ANALYZE`操作を実行する際の`scan`操作の同時実行性を設定します。デフォルト値は`4`です。                                                                                                                                                                                                                                                                |
| [`tidb_ddl_version`](https://docs.pingcap.com/tidb/v7.6/system-variables#tidb_ddl_version-new-in-v760)              | 新しく追加された | [TiDB DDL V2](https://docs.pingcap.com/tidb/v7.6/ddl-v2)有効にするかどうかを制御します。有効にするには値を`2`に、無効にするには値を`1`設定します。デフォルト値は`1`です。TiDB DDL V2 を有効にすると、DDL 文は TiDB DDL V2 を使用して実行されます。テーブル作成用の DDL 文の実行速度は、TiDB DDL V1 と比較して 10 倍向上します。                                                                                           |
| [`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-new-in-v760)                             | 新しく追加された | パーティションテーブル`Global indexes`作成をサポートするかどうかを制御します。デフォルト値は`OFF`です。5 `Global index`現在開発段階です。**このシステム変数の値を変更することは推奨されません**。                                                                                                                                                                                               |
| [`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760)                   | 新しく追加された | ユーザーセッションにおけるトランザクションのアイドルタイムアウトを制御します。ユーザーセッションがトランザクション状態にあり、この変数の値を超える期間アイドル状態が続くと、TiDBはセッションを終了します。デフォルト値の`0`無制限を意味します。                                                                                                                                                                                         |
| [`tidb_ignore_inlist_plan_digest`](/system-variables.md#tidb_ignore_inlist_plan_digest-new-in-v760)                 | 新しく追加された | TiDBがプランダイジェストを生成する際に、異なるクエリ間のリスト`IN`内の要素の差異を無視するかどうかを制御します。デフォルト値`OFF` 、差異を無視しないことを意味します。                                                                                                                                                                                                                          |
| [`tidb_opt_enable_fuzzy_binding`](/system-variables.md#tidb_opt_enable_fuzzy_binding-new-in-v760)                   | 新しく追加された | データベース間バインディング機能を有効にするかどうかを制御します。デフォルト値`OFF` 、データベース間バインディングが無効であることを意味します。                                                                                                                                                                                                                                         |
| [`tidb_txn_entry_size_limit`](/system-variables.md#tidb_txn_entry_size_limit-new-in-v760)                           | 新しく追加された | TiDB設定項目[`performance.txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v4010-and-v500)動的に変更します。これにより、TiDB内の単一行のデータサイズが制限されます。この変数のデフォルト値は`0`で、TiDBはデフォルトで設定項目`txn-entry-size-limit`の値を使用します。この変数が0以外の値に設定された場合、 `txn-entry-size-limit`も同じ値に設定されます。                                    |
| [`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-new-in-v760)             | 新しく追加された | [アクティブPDFollower](/tune-region-performance.md#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service)機能（実験的）を有効にするかどうかを制御します。値が`OFF`場合、TiDB は PD リーダーからのみリージョン情報を取得します。値が`ON`場合、TiDB はリージョン情報要求をすべての PD サーバーに均等に分散し、PD フォロワーもリージョン要求を処理できるため、PD リーダーの CPU 負荷が軽減されます。 |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                                                                        | タイプを変更   | 説明                                                                                                                                                                                                                     |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | [`tls-version`](/tidb-configuration-file.md#tls-version)                                                                                               | 修正済み     | デフォルト値は &quot;&quot; です。TiDB のデフォルトでサポートされる TLS バージョンが`TLS1.1`以上から`TLS1.2`以上に変更されました。                                                                                                                                  |
| TiKV           | [`raftstore.report-min-resolved-ts-interval`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file/#report-min-resolved-ts-interval-new-in-v600) | 名前変更     | 名前をより正確にするために、この構成項目の名前は[`raftstore.pd-report-min-resolved-ts-interval`](/tikv-configuration-file.md#pd-report-min-resolved-ts-interval-new-in-v760)に変更されました。 `raftstore.report-min-resolved-ts-interval`無効になりました。     |
| TiKV           | [`blob-file-compression`](/tikv-configuration-file.md#blob-file-compression)                                                                           | 修正済み     | Titanで値を圧縮するために使用されるアルゴリズム。単位はvalueです。TiDB v7.6.0以降、デフォルトの圧縮アルゴリズムは`zstd`です。                                                                                                                                           |
| TiKV           | [`rocksdb.defaultcf.titan.min-blob-size`](/tikv-configuration-file.md#min-blob-size)                                                                   | 修正済み     | TiDB v7.6.0以降、新規クラスターのデフォルト値は`32KB`です。v7.6.0にアップグレードする既存のクラスターの場合、デフォルト値は`1KB`ままです。                                                                                                                                    |
| TiKV           | [`rocksdb.titan.enabled`](/tikv-configuration-file.md#enabled)                                                                                         | 修正済み     | Titanを有効または無効にします。v7.5.0以前のバージョンでは、デフォルト値は`false`です。v7.6.0以降では、新規クラスタのみデフォルト値は`true`です。v7.6.0以降のバージョンにアップグレードされた既存のクラスタでは、元の設定が保持されます。                                                                                 |
| TiKV           | [`cdc.incremental-scan-concurrency-limit`](/tikv-configuration-file.md#incremental-scan-concurrency-limit-new-in-v760)                                 | 新しく追加された | 実行待ちの履歴データの増分スキャンタスクの最大キュー長を設定します。デフォルト値は`10000`で、最大10000個のタスクをキューに入れて実行できます。                                                                                                                                          |
| TiKV           | [`gc.num-threads`](/tikv-configuration-file.md#num-threads-new-in-v658-v714-v751-and-v760)                                                             | 新しく追加された | `enable-compaction-filter` `false`に設定すると、このパラメータはGCスレッドの数を制御します。デフォルト値は`1`です。                                                                                                                                          |
| TiKV           | [`raftstore.periodic-full-compact-start-times`](/tikv-configuration-file.md#periodic-full-compact-start-times-new-in-v760)                             | 新しく追加された | TiKVが定期的なフルコンパクションを開始する特定のタイミングを設定します。デフォルト値の`[]` 、定期的なフルコンパクションが無効であることを意味します。                                                                                                                                        |
| TiKV           | [`raftstore.periodic-full-compact-start-max-cpu`](/tikv-configuration-file.md#periodic-full-compact-start-max-cpu-new-in-v760)                         | 新しく追加された | TiKV定期フルコンパクションの最大CPU使用率を制限します。デフォルト値は`0.1`です。                                                                                                                                                                         |
| TiKV           | [`raftstore.pd-report-min-resolved-ts-interval`](/tikv-configuration-file.md#pd-report-min-resolved-ts-interval-new-in-v760)                           | 新しく追加された | [`raftstore.report-min-resolved-ts-interval`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#report-min-resolved-ts-interval-new-in-v600)から改名されました。TiKVがPDリーダーにResolved TSを報告する最小間隔を指定します。デフォルト値は`"1s"`です。 |
| TiKV           | [`zstd-dict-size`](/tikv-configuration-file.md#zstd-dict-size)                                                                                         | 新しく追加された | `zstd`辞書の圧縮サイズを指定します。デフォルト値は`"0KB"`で、 `zstd`辞書の圧縮を無効にすることを意味します。                                                                                                                                                       |
| TiFlash        | [`logger.level`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                                                                     | 修正済み     | ログ記録のコストを削減するために、デフォルト値を`"debug"`から`"INFO"`に変更します。                                                                                                                                                                     |
| TiDB Lightning | [`tidb.pd-addr`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)                                                                  | 修正済み     | PDサーバーのアドレスを設定します。v7.6.0以降、TiDBは複数のPDアドレスの設定をサポートします。                                                                                                                                                                  |
| TiDB Lightning | [`block-size`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)                                                                    | 新しく追加された | 物理インポートモード（ `backend='local'` ）でローカルファイルをソートするためのI/Oブロックサイズを制御します。デフォルト値は`16KiB`です。ディスクIOPSがボトルネックになっている場合は、この値を増やすことでパフォーマンスを向上させることができます。                                                                            |
| BR             | [`--granularity`](/br/br-snapshot-guide.md#performance-and-impact-of-snapshot-restore)                                                                 | 新しく追加された | `--granularity="coarse-grained"`指定すると、粗粒度のリージョン散布アルゴリズム（実験的）が使用されます。これにより、大規模なリージョンシナリオにおける復元速度が向上します。                                                                                                                 |
| TiCDC          | [`compression`](/ticdc/ticdc-changefeed-config.md)                                                                                                     | 新しく追加された | REDO ログ ファイルを圧縮する動作を制御します。                                                                                                                                                                                             |
| TiCDC          | [`sink.cloud-storage-config`](/ticdc/ticdc-changefeed-config.md)                                                                                       | 新しく追加された | オブジェクトstorageにデータを複製するときに、履歴データの自動クリーンアップを設定します。                                                                                                                                                                       |

### システムテーブル {#system-tables}

-   TiDB でサポートされているすべてのキーワードの情報を表示するための新しいシステム テーブル[`INFORMATION_SCHEMA.KEYWORDS`](/information-schema/information-schema-keywords.md)を追加します。
-   システム テーブル[`INFORMATION_SCHEMA.SLOW_QUERY`](/information-schema/information-schema-slow-query.md)に、リソース制御に関連する次のフィールドを追加します。
    -   `Resource_group` : ステートメントがバインドされているリソース グループ。
    -   `Request_unit_read` : ステートメントによって消費された読み取り RU の合計。
    -   `Request_unit_write` : ステートメントによって消費された書き込み RU の合計。
    -   `Time_queued_by_rc` : ステートメントが利用可能なリソースを待機する合計時間。

## オフラインパッケージの変更 {#offline-package-changes}

v7.6.0 以降、 `TiDB-community-server` [バイナリパッケージ](/binary-package.md)には、プロキシコンポーネント[TiProxy](/tiproxy/tiproxy-overview.md)のインストール パッケージである`tiproxy-{version}-linux-{arch}.tar.gz`が含まれるようになりました。

## 非推奨の機能 {#deprecated-features}

-   TLSv1.0およびTLSv1.1プロトコルのサポートはTiDB v7.6.0で非推奨となり、v8.0.0で削除される予定です。TLSv1.2またはTLSv1.3にアップグレードしてください。
-   実行計画の[ベースライン進化](/sql-plan-management.md#baseline-evolution)機能は、TiDB v8.0.0で廃止されます。同等の機能は、以降のバージョンで再設計される予定です。
-   [`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry)システム変数は TiDB v8.0.0 で非推奨となります。それ以降、TiDB は楽観的トランザクションの自動再試行をサポートしなくなります。

## 改善点 {#improvements}

-   TiDB

    -   非バイナリ照合順序が設定され、クエリに`LIKE`含まれている場合、オプティマイザは実行効率を向上させるために`IndexRangeScan`生成します[＃48181](https://github.com/pingcap/tidb/issues/48181) [＃49138](https://github.com/pingcap/tidb/issues/49138) @ [時間と運命](https://github.com/time-and-fate)
    -   特定のシナリオで`OUTER JOIN`を`INNER JOIN`に変換する能力を強化する[＃49616](https://github.com/pingcap/tidb/issues/49616) @ [qw4990](https://github.com/qw4990)
    -   ノードが[＃47298](https://github.com/pingcap/tidb/issues/47298) @ [ywqzzy](https://github.com/ywqzzy)で再起動されるシナリオでの分散実行フレームワーク (DXF) タスクのバランスを改善します。
    -   通常の`ADD INDEX`タスク[＃47758](https://github.com/pingcap/tidb/issues/47758) @ [接線](https://github.com/tangenta)にフォールバックする代わりに、複数の加速された`ADD INDEX` DDL タスクをキューに入れて実行できるようにサポートします。
    -   `ALTER TABLE ... ROW_FORMAT` [＃48754](https://github.com/pingcap/tidb/issues/48754) @ [ホーキングレイ](https://github.com/hawkingrei)の互換性を向上させる
    -   `CANCEL IMPORT JOB`文を同期文[＃48736](https://github.com/pingcap/tidb/issues/48736) @ [D3ハンター](https://github.com/D3Hunter)に変更します。
    -   空のテーブルにインデックスを追加する速度を向上[＃49682](https://github.com/pingcap/tidb/issues/49682) @ [ジムララ](https://github.com/zimulala)
    -   相関サブクエリの列が上位レベルの演算子によって参照されていない場合、相関サブクエリは直接削除できます[＃45822](https://github.com/pingcap/tidb/issues/45822) @ [キング・ディラン](https://github.com/King-Dylan)
    -   `EXCHANGE PARTITION`操作により、統計[＃47354](https://github.com/pingcap/tidb/issues/47354) @ [ハイラスティン](https://github.com/Rustin170506)のメンテナンス更新がトリガーされます
    -   TiDBは、連邦情報処理標準（FIPS） [＃47948](https://github.com/pingcap/tidb/issues/47948) @ [天菜まお](https://github.com/tiancaiamao)の要件を満たすバイナリファイルの構築をサポートしています。
    -   いくつかの型変換を処理する際のTiDB実装を最適化し、関連する問題を修正しました[＃47945](https://github.com/pingcap/tidb/issues/47945) [＃47864](https://github.com/pingcap/tidb/issues/47864) [＃47829](https://github.com/pingcap/tidb/issues/47829) [＃47816](https://github.com/pingcap/tidb/issues/47816) @ [ヤンケオ](https://github.com/YangKeao) @ [lcwangchao](https://github.com/lcwangchao)
    -   スキーマバージョンを取得する際、TiDBはデフォルトでKVタイムアウト機能を使用して読み取り、低速なメタリージョンリーダーの読み取りがスキーマバージョンの更新に与える影響を軽減します[＃48125](https://github.com/pingcap/tidb/pull/48125) @ [cfzjywxk](https://github.com/cfzjywxk)

-   TiKV

    -   非同期タスク[＃15759](https://github.com/tikv/tikv/issues/15759) @ [ユジュンセン](https://github.com/YuJuncen)をクエリするための API エンドポイント`/async_tasks`を追加します
    -   gRPC モニタリングに優先度ラベルを追加して、異なる優先度[＃49318](https://github.com/pingcap/tidb/issues/49318) @ [バッファフライ](https://github.com/bufferflies)のリソース グループ データを表示します。
    -   `readpool.unified.max-tasks-per-worker`の値を動的に調整することをサポートし、優先度[＃16026](https://github.com/tikv/tikv/issues/16026) @ [栄光](https://github.com/glorv)に基づいて実行中のタスクの数を個別に計算できます。
    -   GCスレッドの数を動的に調整する機能をサポート。デフォルト値は`1` [＃16101](https://github.com/tikv/tikv/issues/16101) @ [トニー・シュッキ](https://github.com/tonyxuqqi)

-   PD

    -   ディスクジッタ[＃7377](https://github.com/tikv/pd/issues/7377) @ [HuSharp](https://github.com/HuSharp)のPD TSOの可用性を向上

-   TiFlash

    -   ディスクパフォーマンスジッタによる読み取りレイテンシーへの影響を軽減[＃8583](https://github.com/pingcap/tiflash/issues/8583) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   バックグラウンド GC タスクによる読み取りおよび書き込みタスクのレイテンシーへの影響を軽減[＃8650](https://github.com/pingcap/tiflash/issues/8650) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   ストレージとコンピューティングの分離アーキテクチャで同一のデータ読み取り操作をマージして、高同時実行時のデータスキャンパフォーマンスを向上させる[＃6834](https://github.com/pingcap/tiflash/issues/6834) @ [ジンヘリン](https://github.com/JinheLin)
    -   `JOIN ON` [＃47424](https://github.com/pingcap/tidb/issues/47424) @ [ゲンリチ](https://github.com/gengliqi)にJOIN KEYの等価条件のみが含まれる場合の`SEMI JOIN`と`LEFT OUTER SEMIJOIN`の実行パフォーマンスを最適化します

-   ツール

    -   バックアップと復元 (BR)

        -   フルバックアップリカバリフェーズ[＃39832](https://github.com/pingcap/tidb/issues/39832) @ [3ポイントシュート](https://github.com/3pointer)でAmazon S3 `session-token`および`assume-role`使用した認証をサポート
        -   `delete range`シナリオで Point-In-Time Recovery (PITR) の新しい統合テストを導入し、PITR の安定性を[＃47738](https://github.com/pingcap/tidb/issues/47738) @ [リーヴルス](https://github.com/Leavrth)強化します。
        -   大規模なデータセット[＃48301](https://github.com/pingcap/tidb/issues/48301) @ [リーヴルス](https://github.com/Leavrth)シナリオで`RESTORE`ステートメントのテーブル作成パフォーマンスを向上
        -   BR例外処理メカニズムをリファクタリングして、未知のエラーに対する許容度を高めます[＃47656](https://github.com/pingcap/tidb/issues/47656) @ [3ポイントシュート](https://github.com/3pointer)

    -   TiCDC

        -   並列度[＃10098](https://github.com/pingcap/tiflow/issues/10098) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)を増やすことで、TiCDC がオブジェクトstorageにデータを複製する際のパフォーマンスが向上します。
        -   `sink-uri`構成[＃10106](https://github.com/pingcap/tiflow/issues/10106) @ [3エースショーハンド](https://github.com/3AceShowHand)で`content-compatible=true`設定することにより、 TiCDC Canal-JSON コンテンツ フォーマット[公式Canal出力のコンテンツ形式と互換性がある](/ticdc/ticdc-canal-json.md#compatibility-with-the-official-canal)作成をサポートします。

    -   TiDB データ移行 (DM)

        -   DM OpenAPI [＃10193](https://github.com/pingcap/tiflow/issues/10193) @ [GMHDBJD](https://github.com/GMHDBJD)にフルデータ物理インポートの構成を追加します

    -   TiDB Lightning

        -   安定性を高めるために複数のPDアドレスの設定をサポート[＃49515](https://github.com/pingcap/tidb/issues/49515) @ [ミッタルリシャブ](https://github.com/mittalrishabh)
        -   パフォーマンスを向上させるために、ローカルファイルのソートのI/Oブロックサイズを制御する`block-size`パラメータの設定をサポート[＃45037](https://github.com/pingcap/tidb/issues/45037) @ [ミッタルリシャブ](https://github.com/mittalrishabh)

## バグ修正 {#bug-fixes}

-   TiDB

    -   TiDBがパニックを起こしてエラーを報告する問題を修正`invalid memory address or nil pointer dereference` [＃42739](https://github.com/pingcap/tidb/issues/42739) @ [CbcWestwolf](https://github.com/CbcWestwolf)
    -   DDL `jobID` 0 [＃46296](https://github.com/pingcap/tidb/issues/46296) @ [ジフハウス](https://github.com/jiyfhust)に復元されたときに発生する TiDB ノードpanicの問題を修正しました
    -   同じクエリプランで、場合によっては[＃47634](https://github.com/pingcap/tidb/issues/47634) @ [キング・ディラン](https://github.com/King-Dylan)の異なる`PLAN_DIGEST`値が発生する問題を修正しました
    -   DUALテーブルを最初のサブノードとして`UNION ALL`実行するとエラー[＃48755](https://github.com/pingcap/tidb/issues/48755) @ [ウィノロス](https://github.com/winoros)が発生する可能性がある問題を修正しました。
    -   共通テーブル式 (CTE) を含むクエリで、 `tidb_max_chunk_size`小さい値[＃48808](https://github.com/pingcap/tidb/issues/48808) @ [グオシャオゲ](https://github.com/guo-shaoge)に設定されている場合に`runtime error: index out of range [32] with length 32`報告される問題を修正しました。
    -   `AUTO_ID_CACHE=1` [＃46324](https://github.com/pingcap/tidb/issues/46324) @ [天菜まお](https://github.com/tiancaiamao)使用時の Goroutine リークの問題を修正
    -   MPPで計算された`COUNT(INT)`の結果が正しくない可能性がある問題を修正[＃48643](https://github.com/pingcap/tidb/issues/48643) @ [アイリンキッド](https://github.com/AilinKid)
    -   パーティション列タイプが`DATETIME` [＃48814](https://github.com/pingcap/tidb/issues/48814) @ [crazycs520](https://github.com/crazycs520)の場合に`ALTER TABLE ... LAST PARTITION`実行が失敗する問題を修正しました
    -   データの末尾にスペースが含まれている場合に`LIKE`で`_`ワイルドカードを使用すると、クエリ結果が不正確になる可能性がある問題を修正しました[＃48983](https://github.com/pingcap/tidb/issues/48983) @ [時間と運命](https://github.com/time-and-fate)
    -   `tidb_server_memory_limit` [＃48741](https://github.com/pingcap/tidb/issues/48741) @ [徐淮嶼](https://github.com/XuHuaiyu)による長期メモリ圧迫により TiDB の CPU 使用率が上昇する問題を修正
    -   `ENUM`型の列を結合キー[＃48991](https://github.com/pingcap/tidb/issues/48991) @ [ウィノロス](https://github.com/winoros)として使用した場合にクエリ結果が正しくない問題を修正しました
    -   メモリ制限を超えたときに CTE を含むクエリが予期せず停止する問題を修正[＃49096](https://github.com/pingcap/tidb/issues/49096) @ [アイリンキッド](https://github.com/AilinKid)
    -   監査ログ用のエンタープライズプラグインを使用すると、TiDBサーバーが大量のリソースを消費する可能性がある問題を修正[＃49273](https://github.com/pingcap/tidb/issues/49273) @ [lcwangchao](https://github.com/lcwangchao)
    -   特定のシナリオでオプティマイザがTiFlash選択パスを DUAL テーブルに誤って変換する問題を修正[＃49285](https://github.com/pingcap/tidb/issues/49285) @ [アイリンキッド](https://github.com/AilinKid)
    -   `WITH RECURSIVE` CTE を含む`UPDATE`または`DELETE`ステートメントで誤った結果が生成される可能性がある問題を修正しました[＃48969](https://github.com/pingcap/tidb/issues/48969) @ [ウィノロス](https://github.com/winoros)
    -   IndexHashJoin 演算子を含むクエリがメモリが`tidb_mem_quota_query` [＃49033](https://github.com/pingcap/tidb/issues/49033) @ [徐淮嶼](https://github.com/XuHuaiyu)を超えると停止する問題を修正しました
    -   非厳密モード（ `sql_mode = ''` ）で、 `INSERT`実行中に切り捨てが行われても、 [天菜まお](https://github.com/tiancaiamao)でエラー[＃49369](https://github.com/pingcap/tidb/issues/49369)が報告される問題を修正しました。
    -   CTEクエリが再試行プロセス[＃46522](https://github.com/pingcap/tidb/issues/46522) @ [天菜まお](https://github.com/tiancaiamao)中にエラー`type assertion for CTEStorageMap failed`を報告する可能性がある問題を修正しました
    -   ネストされた`UNION`クエリ[＃49377](https://github.com/pingcap/tidb/issues/49377) @ [アイリンキッド](https://github.com/AilinKid)で`LIMIT`と`ORDER BY`無効になる可能性がある問題を修正しました
    -   `ENUM`または`SET`種類の無効な値を解析すると、SQL ステートメント エラー[＃49487](https://github.com/pingcap/tidb/issues/49487) @ [ウィノロス](https://github.com/winoros)が直接発生する問題を修正しました。
    -   Golang の暗黙的な変換アルゴリズム[＃49801](https://github.com/pingcap/tidb/issues/49801) @ [qw4990](https://github.com/qw4990)によって発生する統計情報の構築における過剰な統計エラーの問題を修正しました
    -   一部のタイムゾーン[＃49586](https://github.com/pingcap/tidb/issues/49586) @ [金星の上](https://github.com/overvenus)で夏時間が正しく表示されない問題を修正
    -   テーブルが[＃48869](https://github.com/pingcap/tidb/issues/48869) @ [天菜まお](https://github.com/tiancaiamao)と多数ある場合に、テーブルが`AUTO_ID_CACHE=1`の場合に gRPC クライアント リークが発生する可能性がある問題を修正しました。
    -   正常なシャットダウン中に TiDBサーバーがpanic可能性がある問題を修正[＃36793](https://github.com/pingcap/tidb/issues/36793) @ [bb7133](https://github.com/bb7133)
    -   `CommonHandle` [＃47687](https://github.com/pingcap/tidb/issues/47687) @ [定義2014](https://github.com/Defined2014)を含むテーブルを処理するときに`ADMIN RECOVER INDEX` `ERROR 1105`報告する問題を修正しました
    -   `ALTER TABLE t PARTITION BY`実行時に配置ルールを指定するとエラー`ERROR 8239` [＃48630](https://github.com/pingcap/tidb/issues/48630) @ [ミョンス](https://github.com/mjonss)が報告される問題を修正しました
    -   `INFORMATION_SCHEMA.CLUSTER_INFO`の`START_TIME`列目タイプが[＃45221](https://github.com/pingcap/tidb/issues/45221) @ [ドヴェーデン](https://github.com/dveeden)で有効ではない問題を修正
    -   `INFORMATION_SCHEMA.COLUMNS`の無効な`EXTRA`列目タイプがエラー`Data Too Long, field len 30, data len 45` [＃42030](https://github.com/pingcap/tidb/issues/42030) @ [接線](https://github.com/tangenta)を引き起こす問題を修正しました
    -   `IN (...)` `INFORMATION_SCHEMA.STATEMENTS_SUMMARY` [＃33559](https://github.com/pingcap/tidb/issues/33559) @ [キング・ディラン](https://github.com/King-Dylan)で異なるプランダイジェストを引き起こす問題を修正
    -   `TIME`型を`YEAR`型に変換すると、返される結果に`TIME`と[＃48557](https://github.com/pingcap/tidb/issues/48557)年が[ヤンケオ](https://github.com/YangKeao)で混在する問題を修正しました。
    -   `tidb_enable_collect_execution_info`無効にするとコプロセッサキャッシュがpanicになる問題を修正[＃48212](https://github.com/pingcap/tidb/issues/48212) @ [あなた06](https://github.com/you06)
    -   `shuffleExec`予期せず終了すると TiDB がクラッシュする問題を修正[＃48230](https://github.com/pingcap/tidb/issues/48230) @ [wshwsh12](https://github.com/wshwsh12)
    -   静的`CALIBRATE RESOURCE` Prometheusデータ[＃49174](https://github.com/pingcap/tidb/issues/49174) @ [栄光](https://github.com/glorv)に依存している問題を修正
    -   日付に大きな間隔を加算すると誤った結果が返される問題を修正しました。修正後は、無効な接頭辞または文字列`true`を含む間隔は0として扱われるようになり、MySQL 8.0 [＃49227](https://github.com/pingcap/tidb/issues/49227) @ [lcwangchao](https://github.com/lcwangchao)と整合性が取れます。
    -   `ROW`関数が`null`型を誤って推論し、予期しないエラー[＃49015](https://github.com/pingcap/tidb/issues/49015) @ [wshwsh12](https://github.com/wshwsh12)が発生する問題を修正しました。
    -   `ILIKE`関数が一部のシナリオでデータ競合を引き起こす可能性がある問題を修正[＃49677](https://github.com/pingcap/tidb/issues/49677) @ [lcwangchao](https://github.com/lcwangchao)
    -   `STREAM_AGG()` CI [＃49902](https://github.com/pingcap/tidb/issues/49902) @ [wshwsh12](https://github.com/wshwsh12)を誤って処理したためにクエリ結果が正しくない問題を修正しました
    -   バイトを`TIME` [＃47346](https://github.com/pingcap/tidb/issues/47346) @ [wshwsh12](https://github.com/wshwsh12)に変換するときにエンコードが失敗する問題を修正しました
    -   `CHECK`制約の`ENFORCED`オプションの動作がMySQL 8.0 [＃47567](https://github.com/pingcap/tidb/issues/47567) [＃47631](https://github.com/pingcap/tidb/issues/47631) @ [ジフハウス](https://github.com/jiyfhust)と一致しない問題を修正
    -   `CHECK`制約の DDL 文が[＃47632](https://github.com/pingcap/tidb/issues/47632) @ [ジフハウス](https://github.com/jiyfhust)でスタックする問題を修正しました
    -   メモリ不足[＃47862](https://github.com/pingcap/tidb/issues/47862) @ [GMHDBJD](https://github.com/GMHDBJD)により DDL ステートメントのインデックス追加が失敗する問題を修正しました
    -   `ADD INDEX`実行中にクラスタをアップグレードすると、データがインデックス[＃46306](https://github.com/pingcap/tidb/issues/46306) @ [ジムララ](https://github.com/zimulala)と矛盾する可能性がある問題を修正しました。
    -   `tidb_mem_quota_query`システム変数を更新した後に`ADMIN CHECK`実行すると`ERROR 8175` [＃49258](https://github.com/pingcap/tidb/issues/49258) @ [接線](https://github.com/tangenta)が返される問題を修正しました
    -   `ALTER TABLE`外部キーによって参照される列の型を変更すると、 `DECIMAL`精度の変更がエラーとして報告されない問題を修正[＃49836](https://github.com/pingcap/tidb/issues/49836) @ [ヨシキポム](https://github.com/yoshikipom)
    -   `ALTER TABLE`外部キーによって参照される列の型を変更すると、 `INTEGER`長さの変更が誤ってエラーとして報告される問題を修正[＃47702](https://github.com/pingcap/tidb/issues/47702) @ [ヨシキポム](https://github.com/yoshikipom)
    -   いくつかのシナリオで式インデックスが除数が 0 [＃50053](https://github.com/pingcap/tidb/issues/50053) @ [lcwangchao](https://github.com/lcwangchao)であることを検出しない問題を修正しました
    -   多数のテーブル[＃50077](https://github.com/pingcap/tidb/issues/50077) @ [ジムララ](https://github.com/zimulala)を処理するときに TiDB ノードが OOM エラーに遭遇する可能性がある問題を軽減します。
    -   クラスタのローリング再起動[＃50073](https://github.com/pingcap/tidb/issues/50073) @ [接線](https://github.com/tangenta)中に DDL が実行状態のままになる問題を修正しました
    -   `PointGet`または`BatchPointGet`演算子を使用してパーティションテーブルのグローバルインデックスにアクセスすると結果が正しくなくなる可能性がある問題を修正しました[＃47539](https://github.com/pingcap/tidb/issues/47539) @ [L-メープル](https://github.com/L-maple)
    -   生成された列のインデックスが表示[＃47766](https://github.com/pingcap/tidb/issues/47766) @ [アイリンキッド](https://github.com/AilinKid)に設定されている場合、MPP プランが選択されない可能性がある問題を修正しました。
    -   `LIMIT` `OR`型`Index Merge` [＃48588](https://github.com/pingcap/tidb/issues/48588) @ [アイリンキッド](https://github.com/AilinKid)に押し下げられない可能性がある問題を修正しました
    -   BRインポート[＃46527](https://github.com/pingcap/tidb/issues/46527) @ [qw4990](https://github.com/qw4990)後に`mysql.bind_info`テーブルに重複した組み込み行が存在する可能性がある問題を修正しました
    -   パーティションが[＃48182](https://github.com/pingcap/tidb/issues/48182) @ [ハイラスティン](https://github.com/Rustin170506)に削除された後、パーティション化されたテーブルの統計が期待どおりに更新されない問題を修正しました
    -   パーティションテーブル[＃48713](https://github.com/pingcap/tidb/issues/48713) @ [ホーキングレイ](https://github.com/hawkingrei)のグローバル統計の同時マージ中にエラーが返される可能性がある問題を修正しました。
    -   PADDING SPACE [＃48821](https://github.com/pingcap/tidb/issues/48821) @ [時間と運命](https://github.com/time-and-fate)列のインデックス範囲スキャンに`LIKE`演算子を使用するとクエリ結果が正しくなくなる可能性がある問題を修正しました。
    -   生成された列がメモリ上で同時読み取りと書き込みを引き起こし、データ競合[＃44919](https://github.com/pingcap/tidb/issues/44919) @ [接線](https://github.com/tangenta)が発生する可能性がある問題を修正しました。
    -   `WITH 0 TOPN` (トップN統計を収集しないことを示す) が指定されている場合でも、 `ANALYZE TABLE`トップ1統計を収集する可能性がある問題を修正[＃49080](https://github.com/pingcap/tidb/issues/49080) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   不正なオプティマイザヒントによって有効なヒントが無効になる可能性がある問題を修正[＃49308](https://github.com/pingcap/tidb/issues/49308) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   ハッシュパーティションテーブルの統計情報が、パーティションの追加、削除、再編成、または`TRUNCATE`パーティション[＃48235](https://github.com/pingcap/tidb/issues/48235) [＃48233](https://github.com/pingcap/tidb/issues/48233) [＃48226](https://github.com/pingcap/tidb/issues/48226) [＃48231](https://github.com/pingcap/tidb/issues/48231) @ [ハイラスティン](https://github.com/Rustin170506)を行ったときに、それに応じて更新されない問題を修正しました。
    -   自動統計更新の時間枠を設定した後、その時間枠外でも統計が更新される可能性がある問題を修正[＃49552](https://github.com/pingcap/tidb/issues/49552) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   パーティションテーブルを非パーティションテーブルに変換したときに古い統計情報が自動的に削除されない問題を修正[＃49547](https://github.com/pingcap/tidb/issues/49547) @ [ハイラスティン](https://github.com/Rustin170506)
    -   `TRUNCATE TABLE` [＃49663](https://github.com/pingcap/tidb/issues/49663) @ [ハイラスティン](https://github.com/Rustin170506)を使用して非パーティションテーブルからデータをクリアしたときに古い統計が自動的に削除されない問題を修正しました
    -   クエリがソートを強制するオプティマイザヒント（ `STREAM_AGG()`など）を使用し、その実行プランに`IndexMerge` [＃49605](https://github.com/pingcap/tidb/issues/49605) @ [アイリンキッド](https://github.com/AilinKid)が含まれている場合、強制ソートが無効になる可能性がある問題を修正しました。
    -   ヒストグラムの境界に`NULL` [＃49823](https://github.com/pingcap/tidb/issues/49823) @ [アイリンキッド](https://github.com/AilinKid)が含まれている場合、ヒストグラム統計が読み取り可能な文字列に解析されない可能性がある問題を修正しました。
    -   `GROUP_CONCAT(ORDER BY)`構文を含むクエリを実行するとエラー[＃49986](https://github.com/pingcap/tidb/issues/49986) @ [アイリンキッド](https://github.com/AilinKid)が返される可能性がある問題を修正しました
    -   `SQL_MODE`が厳密でない場合に、 `UPDATE` 、 `DELETE` 、 `INSERT`ステートメントが警告ではなくオーバーフローエラーを返す問題を修正しました[＃49137](https://github.com/pingcap/tidb/issues/49137) @ [ヤンケオ](https://github.com/YangKeao)
    -   テーブルに複数値インデックスと非バイナリ型文字列[＃49680](https://github.com/pingcap/tidb/issues/49680) @ [ヤンケオ](https://github.com/YangKeao)で構成される複合インデックスがある場合にデータを挿入できない問題を修正しました
    -   複数レベルのネストされた`UNION`クエリの`LIMIT`無効になる可能性がある問題を修正しました[＃49874](https://github.com/pingcap/tidb/issues/49874) @ [定義2014](https://github.com/Defined2014)
    -   パーティションテーブルを`BETWEEN ... AND ...`条件でクエリすると誤った結果が返される問題を修正[＃49842](https://github.com/pingcap/tidb/issues/49842) @ [定義2014](https://github.com/Defined2014)
    -   `REPLACE INTO`文[＃34325](https://github.com/pingcap/tidb/issues/34325) @ [ヤンケオ](https://github.com/YangKeao)でヒントが使用できない問題を修正
    -   ハッシュパーティションテーブル[＃50044](https://github.com/pingcap/tidb/issues/50044) @ [定義2014](https://github.com/Defined2014)をクエリするときに TiDB が間違ったパーティションを選択する可能性がある問題を修正しました
    -   圧縮を有効にした状態でMariaDB Connector/Jを使用する際に発生する接続エラーを修正[＃49845](https://github.com/pingcap/tidb/issues/49845) @ [猫のみ](https://github.com/onlyacat)

-   TiKV

    -   破損した SST ファイルが他の TiKV ノードに広がり、TiKV がpanic[＃15986](https://github.com/tikv/tikv/issues/15986) @ [コナー1996](https://github.com/Connor1996)になる可能性がある問題を修正しました。
    -   オンラインアンセーフリカバリがマージ中止[＃15580](https://github.com/tikv/tikv/issues/15580) @ [v01dstar](https://github.com/v01dstar)を処理できない問題を修正
    -   [＃15817](https://github.com/tikv/tikv/issues/15817) @ [コナー1996](https://github.com/Connor1996)にスケールアウトするときに DR 自動同期のジョイント状態がタイムアウトする可能性がある問題を修正しました
    -   Titanの`blob-run-mode`がオンライン[＃15978](https://github.com/tikv/tikv/issues/15978) @ [トニー・シュッキ](https://github.com/tonyxuqqi)に更新できない問題を修正
    -   解決済みのTSが2時間ブロックされる可能性がある問題を修正[＃11847](https://github.com/tikv/tikv/issues/11847) [＃15520](https://github.com/tikv/tikv/issues/15520) [＃39130](https://github.com/pingcap/tidb/issues/39130) @ [金星の上](https://github.com/overvenus)
    -   `notLeader`または`regionNotFound` [＃15712](https://github.com/tikv/tikv/issues/15712) @ [HuSharp](https://github.com/HuSharp)に遭遇するとフラッシュバックが停止する可能性がある問題を修正しました
    -   TiKV の実行速度が非常に遅い場合、リージョン[＃16111](https://github.com/tikv/tikv/issues/16111)と[金星の上](https://github.com/overvenus)マージ後にpanicする可能性がある問題を修正しました。
    -   GC が期限切れのロック[＃15066](https://github.com/tikv/tikv/issues/15066) @ [cfzjywxk](https://github.com/cfzjywxk)をスキャンするときに、TiKV がメモリ内の悲観的ロックを読み取ることができない問題を修正しました
    -   Titan モニタリングの BLOB ファイルサイズが正しくない問題を修正[＃15971](https://github.com/tikv/tikv/issues/15971) @ [コナー1996](https://github.com/Connor1996)
    -   TiCDC を使用して大きなテーブルを複製すると、TiKV が OOM [＃16035](https://github.com/tikv/tikv/issues/16035) @ [金星の上](https://github.com/overvenus)になる可能性がある問題を修正しました。
    -   `DECIMAL`算術乗算切り捨て[＃16268](https://github.com/tikv/tikv/issues/16268) @ [ソロツグ](https://github.com/solotzg)を処理するときに TiDB と TiKV が矛盾した結果を生成する可能性がある問題を修正しました
    -   `cast_duration_as_time`誤った結果を返す可能性がある問題を修正[＃16211](https://github.com/tikv/tikv/issues/16211) @ [ゲンリチ](https://github.com/gengliqi)
    -   TiKVがブラジルとエジプトのタイムゾーンを誤って変換する問題を修正[＃16220](https://github.com/tikv/tikv/issues/16220) @ [金星の上](https://github.com/overvenus)
    -   gRPC スレッドが`is_shutdown` [＃16236](https://github.com/tikv/tikv/issues/16236) @ [ピンギュ](https://github.com/pingyu)をチェックしているときに TiKV がpanic可能性がある問題を修正しました

-   PD

    -   PD の etcd ヘルスチェックで期限切れのアドレス[＃7226](https://github.com/tikv/pd/issues/7226) @ [イモムクゲ](https://github.com/iosmanthus)が削除されない問題を修正しました
    -   PDリーダーが転送され、新しいリーダーとPDクライアントの間にネットワークパーティションがある場合、PDクライアントがリーダー[＃7416](https://github.com/tikv/pd/issues/7416) @ [キャビンフィーバーB](https://github.com/CabinfeverB)の情報を更新できない問題を修正しました。
    -   Gin Web Framework のバージョンを v1.8.1 から v1.9.1 にアップグレードして、いくつかのセキュリティ問題を修正しました[＃7438](https://github.com/tikv/pd/issues/7438) @ [ニューベル](https://github.com/niubell)
    -   レプリカ数が[＃7584](https://github.com/tikv/pd/issues/7584) @ [バッファフライ](https://github.com/bufferflies)要件を満たしていない場合に孤立ピアが削除される問題を修正しました

-   TiFlash

    -   クエリ[＃8447](https://github.com/pingcap/tiflash/issues/8447) @ [ジンヘリン](https://github.com/JinheLin)中にTiFlash がメモリ制限に遭遇するとメモリリークが発生する問題を修正しました。
    -   `FLASHBACK DATABASE` [＃8450](https://github.com/pingcap/tiflash/issues/8450) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を実行した後もTiFlashレプリカのデータがガベージコレクションされる問題を修正しました
    -   クエリ[＃8564](https://github.com/pingcap/tiflash/issues/8564) @ [ジンヘリン](https://github.com/JinheLin)の低速化によりメモリ使用量が大幅に増加する問題を修正
    -   `CREATE TABLE`と`DROP TABLE` [＃1664](https://github.com/pingcap/tiflash/issues/1664) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を頻繁に実行するシナリオで、一部のTiFlashレプリカデータが`RECOVER TABLE`または`FLASHBACK TABLE`で回復できない問題を修正しました。
    -   `ColumnRef in (Literal, Func...)` [＃8631](https://github.com/pingcap/tiflash/issues/8631) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)のようなフィルタリング条件でクエリを実行したときにクエリ結果が正しくない問題を修正しました
    -   TiFlash が同時 DDL 実行中に競合に遭遇した場合のTiFlashpanic問題を修正[＃8578](https://github.com/pingcap/tiflash/issues/8578) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   分散storageおよびコンピューティングアーキテクチャ[＃8519](https://github.com/pingcap/tiflash/issues/8519) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)で、 TiFlash がオブジェクトstorageデータの GC 所有者を選択できない可能性がある問題を修正しました。
    -   `lowerUTF8`と`upperUTF8`関数で、大文字と小文字が異なるバイト[＃8484](https://github.com/pingcap/tiflash/issues/8484) @ [ゲンリキ](https://github.com/gengliqi)を占めることができない問題を修正しました。
    -   `ENUM`値が0 [＃8311](https://github.com/pingcap/tiflash/issues/8311) @ [ソロツグ](https://github.com/solotzg)ときにTiFlashが`ENUM`誤って処理する問題を修正しました
    -   `INET_NTOA()`式[＃8211](https://github.com/pingcap/tiflash/issues/8211) @ [ソロツグ](https://github.com/solotzg)の非互換性の問題を修正
    -   ストリーム読み取り[＃8505](https://github.com/pingcap/tiflash/issues/8505) @ [ゲンリキ](https://github.com/gengliqi)中に複数のパーティション テーブルをスキャンするときに発生する可能性のある OOM 問題を修正しました。
    -   短いクエリが正常に実行され、過剰な情報ログ[＃8592](https://github.com/pingcap/tiflash/issues/8592) @ [ウィンドトーカー](https://github.com/windtalker)が出力される問題を修正しました。
    -   TiFlashが停止時にクラッシュする可能性がある問題を修正[＃8550](https://github.com/pingcap/tiflash/issues/8550) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   定数文字列パラメータ[＃8604](https://github.com/pingcap/tiflash/issues/8604) @ [ウィンドトーカー](https://github.com/windtalker)を含む`GREATEST`または`LEAST`関数で発生する可能性のある、ランダムに無効なメモリアクセスの問題を修正しました。

-   ツール

    -   バックアップと復元 (BR)

        -   BRが外部storageファイル[＃48452](https://github.com/pingcap/tidb/issues/48452) @ [3エースショーハンド](https://github.com/3AceShowHand)に対して誤ったURIを生成する問題を修正
        -   タスク初期化中にPDへの接続に失敗すると、ログバックアップタスクは開始できるが正常に動作しない問題を修正[＃16056](https://github.com/tikv/tikv/issues/16056) @ [ユジュンセン](https://github.com/YuJuncen)
        -   ログバックアップタスクがメモリリークに遭遇し、起動後に正常に実行されない可能性がある問題を修正[＃16070](https://github.com/tikv/tikv/issues/16070) @ [ユジュンセン](https://github.com/YuJuncen)
        -   PITRプロセス中にシステムテーブル`mysql.gc_delete_range`にデータを挿入するとエラー[＃49346](https://github.com/pingcap/tidb/issues/49346) @ [リーヴルス](https://github.com/Leavrth)が返される問題を修正しました。
        -   古いバージョン[＃49466](https://github.com/pingcap/tidb/issues/49466) @ [3ポイントシュート](https://github.com/3pointer)のバックアップからデータを復元するときに`Unsupported collation`エラーが報告される問題を修正しました
        -   特定のシナリオでスナップショットを介してユーザーテーブルを回復した後に権限がタイムリーに更新されない問題を修正[＃49394](https://github.com/pingcap/tidb/issues/49394) @ [リーヴルス](https://github.com/Leavrth)

    -   TiCDC

        -   特定のシナリオで`DELETE`ステートメントを複製するときに、 `WHERE`句が主キーを条件として使用しない問題を修正しました[＃9812](https://github.com/pingcap/tiflow/issues/9812) @ [アズドンメン](https://github.com/asddongmen)
        -   オブジェクトstorageサービス[＃10137](https://github.com/pingcap/tiflow/issues/10137) @ [スドジ](https://github.com/sdojjy)にデータを複製するときに TiCDCサーバーがpanic可能性がある問題を修正しました
        -   `kv-client`初期化[＃10095](https://github.com/pingcap/tiflow/issues/10095) @ [3エースショーハンド](https://github.com/3AceShowHand)中に発生する可能性のあるデータ競合問題を修正
        -   特定の特殊なシナリオで TiCDC が TiKV との接続を誤って閉じる問題を修正[＃10239](https://github.com/pingcap/tiflow/issues/10239) @ [ヒック](https://github.com/hicqu)
        -   アップストリーム[＃9739](https://github.com/pingcap/tiflow/issues/9739) @ [ヒック](https://github.com/hicqu)で損失のある DDL 文を実行すると TiCDCサーバーがpanic可能性がある問題を修正しました。
        -   TiCDC が下流の MySQL [＃10334](https://github.com/pingcap/tiflow/issues/10334) @ [張金鵬87](https://github.com/zhangjinpeng87)にデータを複製するときに`checkpoint-ts`スタックする可能性がある問題を修正しました

    -   TiDB データ移行 (DM)

        -   DM が「イベント タイプ切り捨てが無効です」というエラーに遭遇し、アップグレードが失敗する問題を修正しました[＃10282](https://github.com/pingcap/tiflow/issues/10282) @ [GMHDBJD](https://github.com/GMHDBJD)
        -   GTIDモード[＃9676](https://github.com/pingcap/tiflow/issues/9676) @ [フェラン・モーガン・ピングキャップ](https://github.com/feran-morgan-pingcap)でデータを複製する際のパフォーマンス低下の問題を修正
        -   下流テーブル構造に`shard_row_id_bits` [＃10308](https://github.com/pingcap/tiflow/issues/10308) @ [GMHDBJD](https://github.com/GMHDBJD)が含まれている場合に移行タスクエラーが発生する問題を修正しました

## 寄稿者 {#contributors}

TiDB コミュニティからの以下の貢献者に感謝いたします。

-   [0o001](https://github.com/0o001) (初回投稿者)
-   [バゲチェンジ](https://github.com/bagechengzi) (初回投稿者)
-   [フェラン・モーガン・ピングキャップ](https://github.com/feran-morgan-pingcap) (初回投稿者)
-   [ハイポン](https://github.com/highpon)
-   [ジフハウス](https://github.com/jiyfhust)
-   [L-メープル](https://github.com/L-maple)
-   [ルクシュミナラヤナン](https://github.com/lkshminarayanan) (初回投稿者)
-   [lyang24](https://github.com/lyang24) (初回投稿者)
-   [ミッタルリシャブ](https://github.com/mittalrishabh)
-   [モルゴ](https://github.com/morgo)
-   [nkg-](https://github.com/nkg-) (初回投稿者)
-   [猫のみ](https://github.com/onlyacat)
-   [ショーン0915](https://github.com/shawn0915)
-   [スミティズ](https://github.com/Smityz)
-   [シュプニゴ](https://github.com/szpnygo) (初回投稿者)
-   [ub-3](https://github.com/ub-3) (初回投稿者)
-   [シャオヤウェイ](https://github.com/xiaoyawei) (初回投稿者)
-   [ヨークヘレン](https://github.com/yorkhellen)
-   [ヨシキポム](https://github.com/yoshikipom) (初回投稿者)
-   [ジャオリ](https://github.com/Zheaoli)
