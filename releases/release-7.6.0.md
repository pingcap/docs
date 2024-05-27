---
title: TiDB 7.6.0 Release Notes
summary: TiDB 7.6.0 の新機能、互換性の変更、改善、バグ修正について説明します。
---

# TiDB 7.6.0 リリースノート {#tidb-7-6-0-release-notes}

発売日: 2024年1月25日

TiDB バージョン: 7.6.0

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.6/quick-start-with-tidb)

7.6.0 では、次の主要な機能と改善が導入されています。

<table><thead><tr><th>カテゴリー</th><th>機能/拡張機能</th><th>説明</th></tr></thead><tbody><tr><td rowspan="4">スケーラビリティとパフォーマンス</td><td><a href="https://docs.pingcap.com/tidb/v7.6/sql-plan-management#cross-database-binding">データベース間のSQLバインディング</a></td><td>同じスキーマを持つ数百のデータベースを管理する場合、これらのデータベース全体に SQL バインディングを適用する必要があることがよくあります。たとえば、SaaS または PaaS データ プラットフォームでは、各ユーザーは通常、同じスキーマを持つ個別のデータベースを操作し、それらに対して同様の SQL クエリを実行します。この場合、各データベースに SQL を 1 つずつバインドするのは現実的ではありません。TiDB v7.6.0 では、すべてのスキーマが同等のデータベース間でバインディングを一致させることができるデータベース間 SQL バインディングが導入されています。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v7.6/br-snapshot-guide#restore-cluster-snapshots">スナップショットの復元を最大 10 倍高速化 (実験的)</a></td><td> BR v7.6.0 では、クラスターのスナップショット復元を高速化するための実験的粗粒度のリージョン分散アルゴリズムが導入されています。多数の TiKV ノードを持つクラスターでは、このアルゴリズムにより、ノード間で負荷がより均等に分散され、ノードごとのネットワーク帯域幅がより有効に活用されるため、クラスターのリソース効率が大幅に向上します。実際のいくつかのケースでは、この改善により復元プロセスが最大約 10 倍高速化されます。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v7.6/ddl-v2">バッチでテーブルを作成する場合、最大 10 倍の速度を実現 (実験的)</a></td><td> v7.6.0 で新しい DDLアーキテクチャが実装されたことで、バッチ テーブル作成のパフォーマンスが著しく向上し、最大 10 倍高速化しました。この大幅な機能強化により、多数のテーブルの作成に必要な時間が大幅に短縮されます。この高速化は、数万から数十万に及ぶ大量のテーブルが一般的に存在する SaaS シナリオで特に顕著です。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v7.6/tune-region-performance#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service">アクティブ PD フォロワーを使用して PD のリージョン情報クエリ サービスを強化する (実験的)</a></td><td> TiDB v7.6.0 では、PD フォロワーがリージョン情報クエリ サービスを提供できるようにする実験的機能「Active PD Follower 」が導入されています。この機能により、多数の TiDB ノードとリージョンを持つクラスターで<code>GetRegion</code>および<code>ScanRegions</code>要求を処理する PD クラスターの機能が向上し、PD リーダーの CPU 負荷が軽減されます。</td></tr><tr><td rowspan="2">信頼性と可用性</td><td><a href="https://docs.pingcap.com/tidb/v7.6/tiproxy-overview">TiProxy をサポート (実験的)</a></td><td>デプロイメント ツールを使用して簡単にデプロイできる TiProxy サービスを完全にサポートし、ローリング再起動、アップグレード、またはスケーリング イベントを通じて TiDB への接続を管理および維持します。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v7.6/dm-compatibility-catalog">データ移行 (DM) が MySQL 8.0 (GA) を正式にサポート</a></td><td>これまで、DM を使用して MySQL 8.0 からデータを移行することは実験的機能であり、本番環境では使用できませんでした。TiDB v7.6.0 では、この機能の安定性と互換性が強化され、本番環境で MySQL 8.0 から TiDB にデータをスムーズかつ迅速に移行できるようになります。v7.6.0 では、この機能が一般提供 (GA) されます。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### スケーラビリティ {#scalability}

-   アクティブ PDFollower機能を使用して、PD のリージョン情報クエリ サービスのスケーラビリティを強化します (実験的) [＃7431](https://github.com/tikv/pd/issues/7431) @ [キャビンフィーバーB](https://github.com/CabinfeverB)

    多数のリージョンを持つ TiDB クラスターでは、ハートビートの処理とタスクのスケジュール設定のオーバーヘッドが増加するため、PD リーダーの CPU 負荷が高くなる可能性があります。クラスターに多数の TiDB インスタンスがあり、リージョン情報に対する要求の同時実行性が高い場合、PD リーダーの CPU 負荷がさらに増加し​​、PD サービスが利用できなくなる可能性があります。

    高可用性を確保するために、TiDB v7.6.0 では、PD のリージョン情報クエリ サービスのスケーラビリティを強化する Active PD Follower機能の使用をサポートしています。システム変数[`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-new-in-v760)を`ON`に設定することで、Active PD Follower機能を有効にすることができます。この機能を有効にすると、TiDB はリージョン情報要求をすべての PD サーバーに均等に分散し、PD フォロワーもリージョン要求を処理できるため、PD リーダーの CPU 負荷が軽減されます。

    詳細については[ドキュメンテーション](/tune-region-performance.md#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service)参照してください。

### パフォーマンス {#performance}

-   BR はスナップショットの復元速度を最大 10 倍向上させます (実験的) [＃33937](https://github.com/pingcap/tidb/issues/33937) [＃49886](https://github.com/pingcap/tidb/issues/49886) @ [3ポインター](https://github.com/3pointer)

    TiDB クラスターのスケールアップに伴い、ビジネスのダウンタイムを最小限に抑えるために、クラスターを障害から迅速に復元することがますます重要になります。v7.6.0 より前では、リージョン分散アルゴリズムがパフォーマンス復元における主なボトルネックでした。v7.6.0 では、 BR はリージョン分散アルゴリズムを最適化し、復元タスクを多数の小さなタスクにすばやく分割し、それらをすべての TiKV ノードに一括で分散します。新しい並列復元アルゴリズムは、各 TiKV ノードのリソースを最大限に活用し、迅速な並列復元を実現します。実際のいくつかのケースでは、大規模なリージョンシナリオでクラスターのスナップショット復元速度が約 10 倍向上しています。

    新しい粗粒度リージョン散布アルゴリズムは実験的です。これを使用するには、 `br`コマンドの`--granularity="coarse-grained"`パラメータを設定します。例:

    ```bash
    br restore full \
    --pd "${PDIP}:2379" \
    --storage "s3://${Bucket}/${Folder}" \
    --s3.region "${region}" \
    --granularity "coarse-grained" \
    --send-credentials-to-tikv=true \ 
    --log-file restorefull.log
    ```

    詳細については[ドキュメンテーション](/br/br-snapshot-guide.md#restore-cluster-snapshots)参照してください。

-   Titanエンジンはデフォルトで有効になっています[＃16245](https://github.com/tikv/tikv/issues/16245) @ [コナー1996](https://github.com/Connor1996) @ [v01dスター](https://github.com/v01dstar) @ [トニー](https://github.com/tonyxuqqi)

    TiDB 全体のテーブル書き込みシナリオをより適切にサポートするため、特に JSON をサポートするために、TiDB v7.6.0 以降では Titan エンジンがデフォルトで有効になっています。Titan エンジンは、32 KB を超える大きな値を RocksDB の LSM ツリーから自動的に分離し、Titan に別々に保存して、大きな値の処理を最適化します。Titan エンジンは、TiKV が使用する RocksDB 機能と完全に互換性があります。この戦略的なシフトにより、書き込み増幅効果が軽減されるだけでなく、大きな値を含む書き込み、更新、およびポイント クエリ シナリオのパフォーマンスが向上します。さらに、範囲スキャン シナリオでは、Titan エンジンの最適化により、デフォルト構成の RocksDB に匹敵するパフォーマンスが実現されています。

    この構成変更は、以前のバージョンとの互換性が維持されます。既存の TiDB クラスターの場合、TiDB v7.6.0 以降のバージョンにアップグレードすると、Titan エンジンはデフォルトで無効になります。特定の要件に基づいて、Titan エンジンを手動で有効または無効にすることができます。

    詳細については[ドキュメンテーション](/storage-engine/titan-overview.md)参照してください。

-   次の文字列関数を TiKV [＃48170](https://github.com/pingcap/tidb/issues/48170) @ [ゲンリキ](https://github.com/gengliqi)にプッシュダウンすることをサポートします

    -   `LOWER()`
    -   `UPPER()`

    詳細については[ドキュメンテーション](/functions-and-operators/expressions-pushed-down.md)参照してください。

-   次のJSON関数をTiFlashにプッシュダウンすることをサポートします[＃48350](https://github.com/pingcap/tidb/issues/48350) [＃48986](https://github.com/pingcap/tidb/issues/48986) [＃48994](https://github.com/pingcap/tidb/issues/48994) [＃49345](https://github.com/pingcap/tidb/issues/49345) [＃49392](https://github.com/pingcap/tidb/issues/49392) @ [シーライズ](https://github.com/SeaRise) @ [いいえ](https://github.com/yibin87)

    -   `JSON_UNQUOTE()`
    -   `JSON_ARRAY()`
    -   `JSON_DEPTH()`
    -   `JSON_VALID()`
    -   `JSON_KEYS()`
    -   `JSON_CONTAINS_PATH()`

    詳細については[ドキュメンテーション](/tiflash/tiflash-supported-pushdown-calculations.md)参照してください。

-   テーブル作成のパフォーマンスを10倍向上（実験的） [＃49752](https://github.com/pingcap/tidb/issues/49752) @ [翻訳者](https://github.com/gmhdbjd)

    以前のバージョンでは、上流データベースから TiDB に数万のテーブルを移行する場合、TiDB がこれらのテーブルを作成するのは時間がかかり、非効率的でした。v7.6.0 以降、TiDB は新しい TiDB DDL V2アーキテクチャを導入します。システム変数[`tidb_ddl_version`](https://docs.pingcap.com/tidb/v7.6/system-variables#tidb_ddl_version-new-in-v760)を構成することでこれを有効にできます。以前のバージョンと比較して、新しいバージョンの DDL ではバッチ テーブルの作成パフォーマンスが 10 倍向上し、テーブルの作成時間が大幅に短縮されます。

    詳細については[ドキュメンテーション](https://docs.pingcap.com/tidb/v7.6/ddl-v2)参照してください。

-   定期的な完全圧縮をサポート（実験的） [＃12729](https://github.com/tikv/tikv/issues/12729) [アファインベルグ](https://github.com/afeinberg)

    v7.6.0 以降、TiDB は TiKV の定期的な完全圧縮をサポートしています。この機能は、冗長なデータ バージョンを排除するためのガベージ コレクション (GC) の拡張機能として機能します。アプリケーション アクティビティに明らかなピークと谷が見られるようなシナリオでは、この機能を使用してアイドル期間中にデータ圧縮を実行し、ピーク期間中のパフォーマンスを向上させることができます。

    TiKV 構成項目[`periodic-full-compact-start-times`](/tikv-configuration-file.md#periodic-full-compact-start-times-new-in-v760)を構成することで、TiKV が定期的な完全圧縮を開始する特定の時間を設定し、 [`periodic-full-compact-start-max-cpu`](/tikv-configuration-file.md#periodic-full-compact-start-max-cpu-new-in-v760)を構成することで TiKV の定期的な完全圧縮の最大 CPU 使用率を制限できます。デフォルト値`periodic-full-compact-start-max-cpu`は 10% です。つまり、定期的な完全圧縮は TiKV の CPU 使用率が 10% 未満の場合にのみトリガーされ、アプリケーション トラフィックへの影響が軽減されます。

    詳細については[ドキュメンテーション](/tikv-configuration-file.md#periodic-full-compact-start-times-new-in-v760)参照してください。

### 信頼性 {#reliability}

-   クロスデータベース実行プランバインディング[＃48875](https://github.com/pingcap/tidb/issues/48875) @ [qw4990](https://github.com/qw4990)

    TiDB で SaaS サービスを実行する場合、データの保守と管理を容易にするために、各テナントのデータを別々のデータベースに保存するのが一般的です。その結果、同じテーブルとインデックスの定義、および類似の SQL ステートメントを持つデータベースが何百も作成されます。このようなシナリオでは、SQL ステートメントの実行プラン バインディングを作成すると、通常、このバインディングは他のデータベースの SQL ステートメントにも適用されます。

    このシナリオでは、TiDB v7.6.0 でクロスデータベース バインディング機能が導入され、異なるデータベースにある場合でも、同じスキーマを持つ SQL ステートメントに同じ実行プランをバインドできるようになりました。クロスデータベース バインディングを作成するときは、次の例に示すように、ワイルドカード`*`を使用してデータベース名を表す必要があります。バインディングが作成されると、テーブル`t1`と`t2`がどのデータベースにあるかに関係なく、TiDB はこのバインディングを使用して同じスキーマを持つすべての SQL ステートメントの実行プランを生成しようとします。これにより、データベースごとにバインディングを作成する手間が省けます。

    ```sql
    CREATE GLOBAL BINDING FOR
    USING
        SELECT /*+ merge_join(t1, t2) */ t1.id, t2.amount
        FROM *.t1, *.t2
        WHERE t1.id = t2.id;
    ```

    さらに、クロスデータベース バインディングは、ユーザー データとワークロードの不均一な分散と急速な変化によって引き起こされる SQL パフォーマンスの問題を効果的に軽減できます。SaaS プロバイダーはクロスデータベース バインディングを使用して、大量のデータを持つユーザーによって検証された実行プランを修正し、すべてのユーザーの実行プランを修正できます。SaaS プロバイダーにとって、この機能は利便性とエクスペリエンスの大幅な向上をもたらします。

    クロスデータベース バインディングによって発生するシステム オーバーヘッド (1% 未満) のため、TiDB はデフォルトでこの機能を無効にします。クロスデータベース バインディングを使用するには、まず[`tidb_opt_enable_fuzzy_binding`](/system-variables.md#tidb_opt_enable_fuzzy_binding-new-in-v760)システム変数を有効にする必要があります。

    詳細については[ドキュメンテーション](/sql-plan-management.md#cross-database-binding)参照してください。

### 可用性 {#availability}

-   プロキシコンポーネントTiProxy をサポート (実験的) [＃413](https://github.com/pingcap/tiproxy/issues/413) @ [翻訳者](https://github.com/djshow832) @ [xhebox](https://github.com/xhebox)

    TiProxy は、クライアントと TiDBサーバーの間にある TiDB の公式プロキシコンポーネントです。TiDB の負荷分散機能と接続永続化関数を提供し、TiDB クラスターのワークロードのバランスをより良くし、メンテナンス操作中にデータベースへのユーザー アクセスに影響を与えないようにします。

    -   TiDB クラスターのローリング再起動、ローリングアップグレード、スケールインなどのメンテナンス操作中は、TiDB サーバーに変更が発生し、クライアントと TiDB サーバー間の接続が中断されます。TiProxy を使用すると、これらのメンテナンス操作中に接続を他の TiDB サーバーにスムーズに移行できるため、クライアントに影響が及ぶことはありません。
    -   TiDBサーバーへのクライアント接続は、他の TiDB サーバーに動的に移行できません。複数の TiDB サーバーのワークロードが不均衡な場合、クラスター全体のリソースは十分であるにもかかわらず、特定の TiDB サーバーでリソースが枯渇し、レイテンシーが大幅に増加する状況が発生する可能性があります。この問題に対処するために、TiProxy は接続の動的移行を提供します。これにより、クライアントに影響を与えることなく、接続を 1 つの TiDBサーバーから別の TiDB サーバーに移行できるため、TiDB クラスターの負荷分散が実現します。

    TiProxy はTiUP、 TiDB Operator、および TiDB Dashboard に統合されており、構成、展開、保守が容易になります。

    詳細については[ドキュメンテーション](/tiproxy/tiproxy-overview.md)参照してください。

### 構文 {#sql}

-   `LOAD DATA`明示的なトランザクションとロールバックをサポート[＃49079](https://github.com/pingcap/tidb/pull/49079) @ [エキシウム](https://github.com/ekexium)

    MySQL と比較すると、 `LOAD DATA`ステートメントのトランザクション動作は、v7.6.0 より前の TiDB バージョンによって異なるため、このステートメントを使用する際には追加の調整が必要になる場合があります。具体的には、v4.0.0 より前では、 `LOAD DATA` 20000 行ごとにコミットします。v4.0.0 から v6.6.0 まで、TiDB はデフォルトで 1 つのトランザクションですべての行をコミットし、 [`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size)システム変数を設定することで固定行数ごとにコミットすることもサポートします。v7.0.0 以降では、 `tidb_dml_batch_size` `LOAD DATA`には影響しなくなり、TiDB は 1 つのトランザクションですべての行をコミットします。

    v7.6.0 以降、TiDB はトランザクション内の`LOAD DATA`他の DML ステートメントと同じ方法、特に MySQL と同じ方法で処理します。トランザクション内の`LOAD DATA`ステートメントは、現在のトランザクションを自動的にコミットしたり、新しいトランザクションを開始したりしなくなりました。さらに、トランザクション内の`LOAD DATA`ステートメントを明示的にコミットまたはロールバックできます。さらに、 `LOAD DATA`ステートメントは、TiDB トランザクション モード設定 (楽観的トランザクションまたは悲観的トランザクション) の影響を受けます。これらの改善により、MySQL から TiDB への移行プロセスが簡素化され、より統一された制御可能なデータ インポート エクスペリエンスが提供されます。

    詳細については[ドキュメンテーション](/sql-statements/sql-statement-load-data.md)参照してください。

### DB操作 {#db-operations}

-   `FLASHBACK CLUSTER`正確なTSO [＃48372](https://github.com/pingcap/tidb/issues/48372) @ [ボーンチェンジャー](https://github.com/BornChanger/BornChanger)の指定をサポートします

    TiDB v7.6.0 では、フラッシュバック機能がさらに強力かつ正確になりました。指定された履歴タイムスタンプへのクラスターのロールバックをサポートするだけでなく、 `FLASHBACK CLUSTER TO TSO`を使用して正確なリカバリ[TSO](/tso.md)を指定できるため、データリカバリの柔軟性が向上します。たとえば、この機能は TiCDC で使用できます。データレプリケーションを一時停止し、ダウンストリーム TiDB クラスターでオンライン前の読み取り/書き込みテストを実行した後、この機能により、クラスターは一時停止した TSO に迅速かつ適切にロールバックし、TiCDC を使用してデータのレプリケーションを続行できます。これにより、オンライン前の検証プロセスが合理化され、データ管理が簡素化されます。

    ```sql
    FLASHBACK CLUSTER TO TSO 445494839813079041;
    ```

    詳細については[ドキュメンテーション](/sql-statements/sql-statement-flashback-cluster.md)参照してください。

-   長時間実行中のアイドルトランザクションの自動終了をサポート[＃48714](https://github.com/pingcap/tidb/pull/48714) @ [クレイジーcs520](https://github.com/crazycs520)

    ネットワークの切断やアプリケーション障害が発生するシナリオでは、 `COMMIT` / `ROLLBACK`ステートメントがデータベースに送信されない可能性があります。これにより、データベース ロックの解放が遅れ、トランザクション ロック待機が発生し、データベース接続が急増する可能性があります。このような問題はテスト環境では一般的ですが、本番環境でも時々発生する可能性があり、迅速に診断することが難しい場合があります。これらの問題を回避するために、TiDB v7.6.0 では、長時間実行されているアイドル トランザクションを自動的に終了する[`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760)システム変数が導入されています。トランザクション状態のユーザー セッションが、この変数の値を超える期間アイドル状態のままになると、TiDB はトランザクションのデータベース接続を終了し、ロールバックします。

    詳細については[ドキュメンテーション](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760)参照してください。

-   実行プランバインディングを作成するための構文を簡素化する[＃48876](https://github.com/pingcap/tidb/issues/48876) @ [qw4990](https://github.com/qw4990)

    TiDB v7.6.0 では、実行プラン バインディングを作成するための構文が簡素化されています。実行プラン バインディングを作成するときに、元の SQL ステートメントを指定する必要がなくなりました。TiDB は、ヒント付きのステートメントに基づいて元の SQL ステートメントを識別します。この改善により、実行プラン バインディングを作成する際の利便性が向上します。例:

    ```sql
    CREATE GLOBAL BINDING
    USING
    SELECT /*+ merge_join(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
    ```

    詳細については[ドキュメンテーション](/sql-plan-management.md#create-a-binding-according-to-a-sql-statement)参照してください。

-   TiDB [＃49237](https://github.com/pingcap/tidb/pull/49237) @ [ジグアン](https://github.com/zyguan)の単一行レコードのサイズ制限を動的に変更する機能をサポート

    v7.6.0 より前では、トランザクション内の単一行レコードのサイズは、TiDB 構成項目[`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50)によって制限されていました。サイズ制限を超えると、TiDB は`entry too large`エラーを返します。この場合、TiDB 構成ファイルを手動で変更し、変更を有効にするために TiDB を再起動する必要があります。管理オーバーヘッドを削減するために、TiDB v7.6.0 では、 `txn-entry-size-limit`構成項目の値を動的に変更することをサポートするシステム変数[`tidb_txn_entry_size_limit`](/system-variables.md#tidb_txn_entry_size_limit-new-in-v760)が導入されました。この変数のデフォルト値は`0`です。つまり、TiDB はデフォルトで構成項目`txn-entry-size-limit`の値を使用します。この変数がゼロ以外の値に設定されている場合、TiDB はトランザクション内の行レコードのサイズをこの変数の値に制限します。この改善により、TiDB を再起動せずにシステム構成を調整する柔軟性が向上しました。

    詳細については[ドキュメンテーション](/system-variables.md#tidb_txn_entry_size_limit-new-in-v760)参照してください。

-   BRはデフォルトで、ユーザーデータ[＃48567](https://github.com/pingcap/tidb/issues/48567) @ [ボーンチェンジャー](https://github.com/BornChanger) [＃49627](https://github.com/pingcap/tidb/issues/49627) @ [リーヴルス](https://github.com/Leavrth)などのシステムテーブルを復元します。

    v5.1.0 以降では、スナップショットをバックアップすると、 BR は`mysql`スキーマ内のシステム テーブルを自動的にバックアップしますが、デフォルトではこれらのシステム テーブルを復元しません。v6.2.0 では、 BR は一部のシステム テーブル内のデータの復元をサポートするためにパラメータ`--with-sys-table`を追加し、操作の柔軟性を高めています。

    管理オーバーヘッドをさらに削減し、より直感的なデフォルト動作を提供するために、バージョン 7.6.0 以降、 BR はパラメータ`--with-sys-table`デフォルトで有効にし、 `cloud_admin`ユーザーのユーザー データの復元をサポートします。つまり、 BR は復元中に一部のシステム テーブル (特にユーザー アカウントとテーブル統計データ) をデフォルトで復元します。この改善により、バックアップと復元の操作がより直感的になり、手動構成の負担が軽減され、全体的な操作エクスペリエンスが向上します。

    詳細については[ドキュメンテーション](/br/br-snapshot-guide.md)参照してください。

### 可観測性 {#observability}

-   リソース制御に関する可観測性を強化する[＃49318](https://github.com/pingcap/tidb/issues/49318) @ [栄光](https://github.com/glorv) @ [バッファフライ](https://github.com/bufferflies) @ [ノルーシュ](https://github.com/nolouch)

    リソース グループを使用してアプリケーションのワークロードを分離するユーザーが増えるにつれて、リソース コントロールはリソース グループに基づいて拡張データを提供します。これにより、リソース グループのワークロードと設定を監視し、次のような問題を迅速に特定して正確に診断できるようになります。

    -   [遅いクエリ](/identify-slow-queries.md) : リソース グループ名、リソース ユニット (RU) の消費量、およびリソースの待機時間を追加します。
    -   [ステートメント要約表](/statement-summary-tables.md) : リソース グループ名、RU 消費量、リソースの待機時間を追加します。
    -   システム変数[`tidb_last_query_info`](/system-variables.md#tidb_last_query_info-new-in-v4014)に、SQL ステートメントによって消費された[ロシア](/tidb-resource-control.md#what-is-request-unit-ru)を示す新しいエントリ`ru_consumption`を追加します。この変数を使用して、セッション内の最後のステートメントのリソース消費量を取得できます。
    -   リソース グループに基づいてデータベース メトリックを追加します: QPS/TPS、実行時間 (P999/P99/P95)、障害数、接続数。
    -   すべてのリソース グループの毎日消費された RU の履歴レコードを記録するために、システム テーブル[`request_unit_by_group`](/mysql-schema.md#system-tables-related-to-resource-control)を追加します。

    詳細については、 [遅いクエリを特定する](/identify-slow-queries.md) 、 [ステートメント要約表](/statement-summary-tables.md) 、 [リソース管理の主要な監視指標](/grafana-resource-control-dashboard.md)を参照してください。

### データ移行 {#data-migration}

-   MySQL 8.0 の移行のためのデータ移行 (DM) サポートが一般提供 (GA) される[＃10405](https://github.com/pingcap/tiflow/issues/10405) @ [翻訳者](https://github.com/lyzx2001)

    これまで、DM を使用して MySQL 8.0 からデータを移行することは実験的機能であり、本番環境では使用できませんでした。TiDB v7.6.0 では、この機能の安定性と互換性が強化され、本番環境で MySQL 8.0 から TiDB にデータをスムーズかつ迅速に移行できるようになります。v7.6.0 では、この機能が一般提供 (GA) されます。

    詳細については[ドキュメンテーション](/dm/dm-compatibility-catalog.md)参照してください。

-   TiCDC は双方向レプリケーション (BDR) モードでの DDL ステートメントのレプリケーションをサポートしています (実験的) [＃10301](https://github.com/pingcap/tiflow/issues/10301) [＃48519](https://github.com/pingcap/tidb/issues/48519) @ [ok江](https://github.com/okJiang) @ [アズドンメン](https://github.com/asddongmen)

    v7.6.0 以降、TiCDC は双方向レプリケーションが構成された DDL ステートメントのレプリケーションをサポートします。以前は、DDL ステートメントのレプリケーションは TiCDC でサポートされていなかったため、TiCDC の双方向レプリケーションのユーザーは、両方の TiDB クラスターに DDL ステートメントを個別に適用する必要がありました。この機能により、TiCDC ではクラスターに`PRIMARY` BDR ロールを割り当てることができ、そのクラスターから下流のクラスターへの DDL ステートメントのレプリケーションが可能になります。

    詳細については[ドキュメンテーション](/ticdc/ticdc-bidirectional-replication.md)参照してください。

-   TiCDC は、チェンジフィード[＃10289](https://github.com/pingcap/tiflow/issues/10289) @ [ホンユンヤン](https://github.com/hongyunyan)のダウンストリーム同期ステータスのクエリをサポートしています。

    v7.6.0 以降、TiCDC では、指定されたレプリケーション タスク (changefeed) のダウンストリーム同期ステータスを照会するための新しい API `GET /api/v2/changefeed/{changefeed_id}/synced`が導入されています。この API を使用すると、TiCDC が受信したアップストリーム データがダウンストリーム システムに完全に同期されているかどうかを判断できます。

    詳細については[ドキュメンテーション](/ticdc/ticdc-open-api-v2.md#query-whether-a-specific-replication-task-is-completed)参照してください。

-   TiCDC は CSV 出力プロトコル[＃9969](https://github.com/pingcap/tiflow/issues/9969) @ [張金鵬87](https://github.com/zhangjinpeng87)で 3 文字の区切り文字のサポートを追加します

    v7.6.0 以降では、CSV 出力プロトコルの区切り文字を 1 ～ 3 文字の長さに指定できます。この変更により、出力内のフィールドを区切るために 2 文字の区切り文字 ( `||`や`$^`など) または 3 文字の区切り文字 ( `|@|`など) を使用してファイル出力を生成するように TiCDC を構成できます。

    詳細については[ドキュメンテーション](/ticdc/ticdc-csv.md)参照してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、v7.5.0 から現在のバージョン (v7.6.0) にアップグレードするときに知っておく必要のある互換性の変更について説明します。v7.4.0 以前のバージョンから現在のバージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更も確認する必要がある可能性があります。

### MySQL 互換性 {#mysql-compatibility}

-   TiDB v7.6.0 より前では、 `LOAD DATA`操作はすべての行を単一のトランザクションでコミットするか、トランザクションをバッチでコミットしていましたが、これは MySQL の動作とは少し異なります。v7.6.0 以降、TiDB は MySQL と同じようにトランザクション内の`LOAD DATA`を処理します。トランザクション内の`LOAD DATA`ステートメントは、現在のトランザクションを自動的にコミットしたり、新しいトランザクションを開始したりし[＃49079](https://github.com/pingcap/tidb/pull/49079)なりました。さらに、トランザクション内の`LOAD DATA`ステートメントを明示的にコミットまたはロールバックできます。さらに、 `LOAD DATA`ステートメントは TiDB トランザクション モード設定 (楽観的トランザクションまたは悲観的トランザクション) の影響を受けます。11 @ [エキシウム](https://github.com/ekexium)

### システム変数 {#system-variables}

| 変数名                                                                                                                 | タイプを変更   | 説明                                                                                                                                                                                                                                                                                                                       |
| ------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`tidb_auto_analyze_partition_batch_size`](/system-variables.md#tidb_auto_analyze_partition_batch_size-new-in-v640) | 修正済み     | さらにテストを行った後、デフォルト値を`1`から`128`に変更します。                                                                                                                                                                                                                                                                                     |
| [`tidb_sysproc_scan_concurrency`](/system-variables.md#tidb_sysproc_scan_concurrency-new-in-v650)                   | 修正済み     | 大規模クラスターでは、 `scan`操作の同時実行性を`ANALYZE`のニーズに合わせて高く調整できるため、最大値を`256`から`4294967295`に変更します。                                                                                                                                                                                                                                    |
| [`tidb_analyze_distsql_scan_concurrency`](/system-variables.md#tidb_analyze_distsql_scan_concurrency-new-in-v760)   | 新しく追加された | `ANALYZE`操作を実行するときの`scan`操作の同時実行性を設定します。デフォルト値は`4`です。                                                                                                                                                                                                                                                                    |
| [`tidb_ddl_version`](https://docs.pingcap.com/tidb/v7.6/system-variables#tidb_ddl_version-new-in-v760)              | 新しく追加された | [TiDB DDL V2](https://docs.pingcap.com/tidb/v7.6/ddl-v2)有効にするかどうかを制御します。有効にするには値を`2`に設定し、無効にするには`1`設定します。デフォルト値は`1`です。TiDB DDL V2 を有効にすると、DDL ステートメントは TiDB DDL V2 を使用して実行されます。テーブルを作成するための DDL ステートメントの実行速度は、TiDB DDL V1 と比較して 10 倍向上します。                                                                               |
| [`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-new-in-v760)                             | 新しく追加された | パーティション化された`Global indexes`の作成をサポートするかどうかを制御します。デフォルト値は`OFF`です。5 `Global index`現在開発段階にあります。**このシステム変数の値を変更することはお勧めしません**。                                                                                                                                                                                                |
| [`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760)                   | 新しく追加された | ユーザー セッション内のトランザクションのアイドル タイムアウトを制御します。ユーザー セッションがトランザクション状態にあり、この変数の値を超える期間アイドル状態のままになると、TiDB はセッションを終了します。デフォルト値`0`無制限を意味します。                                                                                                                                                                                          |
| [`tidb_opt_enable_fuzzy_binding`](/system-variables.md#tidb_opt_enable_fuzzy_binding-new-in-v760)                   | 新しく追加された | クロスデータベース バインディング機能を有効にするかどうかを制御します。デフォルト値`OFF` 、クロスデータベース バインディングが無効であることを意味します。                                                                                                                                                                                                                                        |
| [`tidb_txn_entry_size_limit`](/system-variables.md#tidb_txn_entry_size_limit-new-in-v760)                           | 新しく追加された | TiDB 構成項目[`performance.txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50)を動的に変更します。これにより、TiDB 内の 1 行のデータのサイズが制限されます。この変数のデフォルト値は`0`です。つまり、TiDB はデフォルトで構成項目`txn-entry-size-limit`の値を使用します。この変数がゼロ以外の値に設定されている場合、 `txn-entry-size-limit`も同じ値に設定されます。                                      |
| [`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-new-in-v760)             | 新しく追加された | [アクティブPDFollower](/tune-region-performance.md#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service)機能 (実験的) を有効にするかどうかを制御します。値が`OFF`の場合、TiDB は PD リーダーからのみリージョン情報を取得します。値が`ON`の場合、TiDB はリージョン情報の要求をすべての PD サーバーに均等に分散し、PD フォロワーもリージョン要求を処理できるため、PD リーダーの CPU 負荷が軽減されます。 |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                                                | タイプを変更   | 説明                                                                                                                                            |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------ | -------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| ティビ            | [`tls-version`](/tidb-configuration-file.md#tls-version)                                                                       | 修正済み     | デフォルト値は &quot;&quot; です。TiDB のデフォルトでサポートされる TLS バージョンが`TLS1.1`以上から`TLS1.2`以上に変更されました。                                                         |
| ティクヴ           | [`blob-file-compression`](/tikv-configuration-file.md#blob-file-compression)                                                   | 修正済み     | Titan で値を圧縮するために使用されるアルゴリズム。値を単位とします。TiDB v7.6.0 以降、デフォルトの圧縮アルゴリズムは`zstd`です。                                                                  |
| ティクヴ           | [`rocksdb.defaultcf.titan.min-blob-size`](/tikv-configuration-file.md#min-blob-size)                                           | 修正済み     | TiDB v7.6.0 以降、新しいクラスターのデフォルト値は`32KB`です。既存のクラスターを v7.6.0 にアップグレードする場合、デフォルト値は`1KB`のまま変更されません。                                                 |
| ティクヴ           | [`rocksdb.titan.enabled`](/tikv-configuration-file.md#enabled)                                                                 | 修正済み     | Titan を有効または無効にします。v7.5.0 以前のバージョンの場合、デフォルト値は`false`です。v7.6.0 以降では、新しいクラスターのみのデフォルト値は`true`です。v7.6.0 以降のバージョンにアップグレードされた既存のクラスターは、元の構成を保持します。 |
| ティクヴ           | [`gc.num-threads`](/tikv-configuration-file.md#num-threads-new-in-v658-v714-v751-and-v760)                                     | 新しく追加された | `enable-compaction-filter` `false`に設定すると、このパラメータは GC スレッドの数を制御します。デフォルト値は`1`です。                                                               |
| ティクヴ           | [`raftstore.periodic-full-compact-start-times`](/tikv-configuration-file.md#periodic-full-compact-start-times-new-in-v760)     | 新しく追加された | TiKV が定期的な完全圧縮を開始する特定の時間を設定します。デフォルト値`[]` 、定期的な完全圧縮が無効であることを意味します。                                                                            |
| ティクヴ           | [`raftstore.periodic-full-compact-start-max-cpu`](/tikv-configuration-file.md#periodic-full-compact-start-max-cpu-new-in-v760) | 新しく追加された | TiKV 定期完全圧縮の最大 CPU 使用率を制限します。デフォルト値は`0.1`です。                                                                                                  |
| ティクヴ           | [`zstd-dict-size`](/tikv-configuration-file.md#zstd-dict-size)                                                                 | 新しく追加された | `zstd`辞書圧縮サイズを指定します。デフォルト値は`"0KB"`で、 `zstd`辞書圧縮を無効にすることを意味します。                                                                                |
| TiFlash        | [`logger.level`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                                             | 修正済み     | ログ記録のコストを削減するために、デフォルト値を`"debug"`から`"INFO"`に変更します。                                                                                            |
| TiDB Lightning | [`tidb.pd-addr`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)                                          | 修正済み     | PD サーバーのアドレスを設定します。v7.6.0 以降、TiDB は複数の PD アドレスの設定をサポートします。                                                                                    |
| TiDB Lightning | [`block-size`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)                                            | 新しく追加された | 物理インポート モード ( `backend='local'` ) でローカル ファイルをソートするための I/O ブロック サイズを制御します。デフォルト値は`16KiB`です。ディスク IOPS がボトルネックになっている場合は、この値を増やすとパフォーマンスが向上します。   |
| BR             | [`--granularity`](/br/br-snapshot-guide.md#performance-and-impact-of-snapshot-restore)                                         | 新しく追加された | `--granularity="coarse-grained"`を指定して、粗粒度のリージョン散布アルゴリズム (実験的) を使用します。これにより、大規模なリージョンシナリオでの復元速度が向上します。                                         |
| ティCDC          | [`compression`](/ticdc/ticdc-changefeed-config.md)                                                                             | 新しく追加された | REDO ログ ファイルを圧縮する動作を制御します。                                                                                                                    |
| ティCDC          | [`sink.cloud-storage-config`](/ticdc/ticdc-changefeed-config.md)                                                               | 新しく追加された | データをオブジェクトstorageに複製するときに、履歴データの自動クリーンアップを設定します。                                                                                              |

### システムテーブル {#system-tables}

-   TiDB でサポートされているすべてのキーワードの情報を表示するための新しいシステム テーブル[`INFORMATION_SCHEMA.KEYWORDS`](/information-schema/information-schema-keywords.md)を追加します。
-   システム テーブル[`INFORMATION_SCHEMA.SLOW_QUERY`](/information-schema/information-schema-slow-query.md)に、リソース制御に関連する次のフィールドを追加します。
    -   `Resource_group` : ステートメントがバインドされているリソース グループ。
    -   `Request_unit_read` : ステートメントによって消費された読み取り RU の合計。
    -   `Request_unit_write` : ステートメントによって消費された書き込み RU の合計。
    -   `Time_queued_by_rc` : ステートメントが利用可能なリソースを待機する合計時間。

## オフラインパッケージの変更 {#offline-package-changes}

v7.6.0 以降、 `TiDB-community-server` [バイナリパッケージ](/binary-package.md)には、プロキシコンポーネント[Tiプロキシ](/tiproxy/tiproxy-overview.md)のインストール パッケージである`tiproxy-{version}-linux-{arch}.tar.gz`含まれるようになりました。

## 廃止された機能 {#deprecated-features}

-   TLSv1.0 および TLSv1.1 プロトコルのサポートは TiDB v7.6.0 では非推奨となり、v8.0.0 では削除されます。TLSv1.2 または TLSv1.3 にアップグレードしてください。
-   実行プランの[ベースライン進化](/sql-plan-management.md#baseline-evolution)機能は、TiDB v8.0.0 で廃止されます。同等の機能は、以降のバージョンで再設計されます。
-   [`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry)システム変数は TiDB v8.0.0 で廃止されます。それ以降、TiDB は楽観的トランザクションの自動再試行をサポートしなくなります。

## 改善点 {#improvements}

-   ティビ

    -   非バイナリ照合順序が設定され、クエリに`LIKE`含まれる場合、オプティマイザは実行効率を向上させるために`IndexRangeScan`を生成します[＃48181](https://github.com/pingcap/tidb/issues/48181) [＃49138](https://github.com/pingcap/tidb/issues/49138) @ [時間と運命](https://github.com/time-and-fate)
    -   特定のシナリオで`OUTER JOIN` `INNER JOIN`に変換する能力を強化する[＃49616](https://github.com/pingcap/tidb/issues/49616) @ [qw4990](https://github.com/qw4990)
    -   ノードが再起動されるシナリオで、Distributed eXecution Framework (DXF) タスクのバランスを改善します[＃47298](https://github.com/pingcap/tidb/issues/47298) @ [うわー](https://github.com/ywqzzy)
    -   通常の`ADD INDEX`タスク[＃47758](https://github.com/pingcap/tidb/issues/47758) @ [タンジェンタ](https://github.com/tangenta)にフォールバックする代わりに、複数の高速化された`ADD INDEX` DDL タスクをキューに入れて実行できるようにします。
    -   `ALTER TABLE ... ROW_FORMAT` [＃48754](https://github.com/pingcap/tidb/issues/48754) @ [ホーキングレイ](https://github.com/hawkingrei)の互換性を向上させる
    -   `CANCEL IMPORT JOB`文を同期文[＃48736](https://github.com/pingcap/tidb/issues/48736) @ [D3ハンター](https://github.com/D3Hunter)に変更します。
    -   空のテーブルにインデックスを追加する速度を向上[＃49682](https://github.com/pingcap/tidb/issues/49682) @ [ジムララ](https://github.com/zimulala)
    -   相関サブクエリの列が上位レベルの演算子によって参照されていない場合、相関サブクエリは直接削除できます[＃45822](https://github.com/pingcap/tidb/issues/45822) @ [キング・ディラン](https://github.com/King-Dylan)
    -   `EXCHANGE PARTITION`操作により、統計[＃47354](https://github.com/pingcap/tidb/issues/47354) @ [ハイラスティン](https://github.com/hi-rustin)のメンテナンス更新がトリガーされます
    -   TiDBは、連邦情報処理標準（FIPS） [＃47948](https://github.com/pingcap/tidb/issues/47948) @ [天菜まお](https://github.com/tiancaiamao)の要件を満たすバイナリファイルの構築をサポートしています。
    -   いくつかの型変換を処理する際の TiDB 実装を最適化し、関連する問題を修正[＃47945](https://github.com/pingcap/tidb/issues/47945) [＃47864](https://github.com/pingcap/tidb/issues/47864) [＃47829](https://github.com/pingcap/tidb/issues/47829) [＃47816](https://github.com/pingcap/tidb/issues/47816) @ [ヤンケオ](https://github.com/YangKeao) @ [lcwangchao](https://github.com/lcwangchao)
    -   スキーマバージョンを取得する際、TiDBはデフォルトでKVタイムアウト機能を使用して読み取り、遅いメタリージョンリーダーの読み取りがスキーマバージョンの更新に与える影響を軽減します[＃48125](https://github.com/pingcap/tidb/pull/48125) @ [翻訳](https://github.com/cfzjywxk)

-   ティクヴ

    -   非同期タスク[＃15759](https://github.com/tikv/tikv/issues/15759) @ [ユジュンセン](https://github.com/YuJuncen)をクエリするための API エンドポイント`/async_tasks`を追加します
    -   gRPC モニタリングに優先度ラベルを追加して、異なる優先度[＃49318](https://github.com/pingcap/tidb/issues/49318) @ [バッファフライ](https://github.com/bufferflies)のリソース グループ データを表示します。
    -   `readpool.unified.max-tasks-per-worker`の値を動的に調整する機能をサポートし、優先度[＃16026](https://github.com/tikv/tikv/issues/16026) @ [栄光](https://github.com/glorv)に基づいて実行中のタスクの数を個別に計算できます。
    -   GCスレッドの数を動的に調整する機能をサポート。デフォルト値は`1` [＃16101](https://github.com/tikv/tikv/issues/16101) @ [トニー](https://github.com/tonyxuqqi)

-   PD

    -   ディスクジッタ[＃7377](https://github.com/tikv/pd/issues/7377) @ [ヒューシャープ](https://github.com/HuSharp)中のPD TSOの可用性を向上

-   TiFlash

    -   ディスクパフォ​​ーマンスジッターによる読み取りレイテンシーへの影響を軽減[＃8583](https://github.com/pingcap/tiflash/issues/8583) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   バックグラウンドGCタスクが読み取りおよび書き込みタスクのレイテンシーに与える影響を軽減する[＃8650](https://github.com/pingcap/tiflash/issues/8650) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   ストレージとコンピューティングの分離アーキテクチャで同一のデータ読み取り操作をマージして、高同時実行性[＃6834](https://github.com/pingcap/tiflash/issues/6834) @ [ジンヘリン](https://github.com/JinheLin)でのデータスキャンパフォーマンスを向上させることをサポートします。
    -   `JOIN ON` [＃47424](https://github.com/pingcap/tidb/issues/47424) @ [ゲンリキ](https://github.com/gengliqi)にJOIN KEY等価条件のみが含まれる場合の`SEMI JOIN`と`LEFT OUTER SEMIJOIN`の実行パフォーマンスを最適化します

-   ツール

    -   バックアップと復元 (BR)

        -   フルバックアップリカバリフェーズ[＃39832](https://github.com/pingcap/tidb/issues/39832) @ [3ポインター](https://github.com/3pointer)中にAmazon S3 `session-token`および`assume-role`を使用した認証をサポート
        -   `delete range`シナリオでポイントインタイムリカバリ (PITR) の新しい統合テストを導入し、PITR の安定性を向上[＃47738](https://github.com/pingcap/tidb/issues/47738) @ [リーヴルス](https://github.com/Leavrth)
        -   大規模なデータセットのシナリオで`RESTORE`ステートメントのテーブル作成パフォーマンスを向上[＃48301](https://github.com/pingcap/tidb/issues/48301) @ [リーヴルス](https://github.com/Leavrth)
        -   BR例外処理メカニズムをリファクタリングして、未知のエラーに対する許容度を高める[＃47656](https://github.com/pingcap/tidb/issues/47656) @ [3ポインター](https://github.com/3pointer)

    -   ティCDC

        -   並列処理[＃10098](https://github.com/pingcap/tiflow/issues/10098) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)を増やすことで、TiCDC がオブジェクトstorageにデータを複製する際のパフォーマンスが向上します。
        -   `sink-uri`構成[＃10106](https://github.com/pingcap/tiflow/issues/10106) @ [3エースショーハンド](https://github.com/3AceShowHand)で`content-compatible=true`を設定することにより、 TiCDC Canal-JSON コンテンツ フォーマット[公式Canal出力のコンテンツフォーマットと互換性がある](/ticdc/ticdc-canal-json.md#compatibility-with-the-official-canal)の作成をサポートします。

    -   TiDB データ移行 (DM)

        -   DM OpenAPI [＃10193](https://github.com/pingcap/tiflow/issues/10193) @ [GMHDBJD](https://github.com/GMHDBJD)にフルデータ物理インポートの構成を追加します

    -   TiDB Lightning

        -   安定性を高めるために複数のPDアドレスの設定をサポート[＃49515](https://github.com/pingcap/tidb/issues/49515) @ [ミッタルリシャブ](https://github.com/mittalrishabh)
        -   パフォーマンスを向上させるために、ローカル ファイルのソート用の I/O ブロック サイズを制御する`block-size`パラメータの構成をサポートします[＃45037](https://github.com/pingcap/tidb/issues/45037) @ [ミッタルリシャブ](https://github.com/mittalrishabh)

## バグの修正 {#bug-fixes}

-   ティビ

    -   TiDBがパニックを起こしてエラーを報告する問題を修正`invalid memory address or nil pointer dereference` [＃42739](https://github.com/pingcap/tidb/issues/42739) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)
    -   DDL `jobID`が 0 [＃46296](https://github.com/pingcap/tidb/issues/46296) @ [ジフハウス](https://github.com/jiyfhust)に復元されたときに発生する TiDB ノードpanicの問題を修正しました。
    -   同じクエリプランで`PLAN_DIGEST`値が[＃47634](https://github.com/pingcap/tidb/issues/47634) @ [キング・ディラン](https://github.com/King-Dylan)場合に異なる問題を修正
    -   最初のサブノードとしてDUALテーブルを使用して`UNION ALL`実行するとエラー[＃48755](https://github.com/pingcap/tidb/issues/48755) @ [ウィノロス](https://github.com/winoros)が発生する可能性がある問題を修正しました
    -   共通テーブル式 (CTE) を含むクエリで、 `tidb_max_chunk_size`が小さい値[＃48808](https://github.com/pingcap/tidb/issues/48808) @ [グオシャオゲ](https://github.com/guo-shaoge)に設定されている場合に`runtime error: index out of range [32] with length 32`報告される問題を修正しました。
    -   `AUTO_ID_CACHE=1` [＃46324](https://github.com/pingcap/tidb/issues/46324) @ [天菜まお](https://github.com/tiancaiamao)使用時の Goroutine リークの問題を修正
    -   MPP によって計算された`COUNT(INT)`の結果が正しくない可能性がある問題を修正[＃48643](https://github.com/pingcap/tidb/issues/48643) @ [アイリンキッド](https://github.com/AilinKid)
    -   パーティション列タイプが`DATETIME` [＃48814](https://github.com/pingcap/tidb/issues/48814) @ [クレイジーcs520](https://github.com/crazycs520)の場合に`ALTER TABLE ... LAST PARTITION`実行が失敗する問題を修正
    -   データの末尾にスペースが含まれている場合に`LIKE`で`_`ワイルドカードを使用すると、クエリ結果が不正確になる可能性がある問題を修正しました[＃48983](https://github.com/pingcap/tidb/issues/48983) @ [時間と運命](https://github.com/time-and-fate)
    -   `tidb_server_memory_limit` [＃48741](https://github.com/pingcap/tidb/issues/48741) @ [徐淮宇](https://github.com/XuHuaiyu)による長期メモリ圧迫により TiDB の CPU 使用率が高くなる問題を修正
    -   `ENUM`型の列を結合キー[＃48991](https://github.com/pingcap/tidb/issues/48991) @ [ウィノロス](https://github.com/winoros)として使用するとクエリ結果が正しくなくなる問題を修正
    -   メモリ制限を超えたときに CTE を含むクエリが予期せず停止する問題を修正[＃49096](https://github.com/pingcap/tidb/issues/49096) @ [アイリンキッド](https://github.com/AilinKid)
    -   監査ログ用のエンタープライズプラグインが使用されている場合に TiDBサーバーが大量のリソースを消費する可能性がある問題を修正[＃49273](https://github.com/pingcap/tidb/issues/49273) @ [lcwangchao](https://github.com/lcwangchao)
    -   特定のシナリオでオプティマイザがTiFlash選択パスを DUAL テーブルに誤って変換する問題を修正[＃49285](https://github.com/pingcap/tidb/issues/49285) @ [アイリンキッド](https://github.com/AilinKid)
    -   `WITH RECURSIVE` CTE を含む`UPDATE`または`DELETE`ステートメントで誤った結果が生成される可能性がある問題を修正しました[＃48969](https://github.com/pingcap/tidb/issues/48969) @ [ウィノロス](https://github.com/winoros)
    -   IndexHashJoin 演算子を含むクエリがメモリが`tidb_mem_quota_query` [＃49033](https://github.com/pingcap/tidb/issues/49033) @ [徐淮宇](https://github.com/XuHuaiyu)を超えると停止する問題を修正しました。
    -   非厳密モード（ `sql_mode = ''` ）で、 `INSERT`実行中に切り捨てが行われても、 [＃49369](https://github.com/pingcap/tidb/issues/49369) @ [天菜まお](https://github.com/tiancaiamao)のエラーが報告される問題を修正しました。
    -   CTEクエリが再試行プロセス[＃46522](https://github.com/pingcap/tidb/issues/46522) @ [天菜まお](https://github.com/tiancaiamao)中にエラー`type assertion for CTEStorageMap failed`を報告する可能性がある問題を修正
    -   ネストされた`UNION`のクエリ[＃49377](https://github.com/pingcap/tidb/issues/49377) @ [アイリンキッド](https://github.com/AilinKid)で`LIMIT`と`ORDER BY`無効になる可能性がある問題を修正しました
    -   `ENUM`または`SET`型の無効な値を解析すると、SQL ステートメント エラー[＃49487](https://github.com/pingcap/tidb/issues/49487) @ [ウィノロス](https://github.com/winoros)が直接発生する問題を修正しました。
    -   Golang の暗黙的な変換アルゴリズム[＃49801](https://github.com/pingcap/tidb/issues/49801) @ [qw4990](https://github.com/qw4990)によって発生する統計構築時の過度の統計エラーの問題を修正
    -   一部のタイムゾーンで夏時間が正しく表示されない問題を修正[＃49586](https://github.com/pingcap/tidb/issues/49586) @ [金星の上](https://github.com/overvenus)
    -   テーブルが[＃48869](https://github.com/pingcap/tidb/issues/48869) @ [天菜まお](https://github.com/tiancaiamao)と多数ある場合に、テーブルが`AUTO_ID_CACHE=1`の場合に gRPC クライアント リークが発生する可能性がある問題を修正しました。
    -   正常なシャットダウン中に TiDBサーバーがpanicになる可能性がある問題を修正[＃36793](https://github.com/pingcap/tidb/issues/36793) @ [bb7133](https://github.com/bb7133)
    -   `CommonHandle` [＃47687](https://github.com/pingcap/tidb/issues/47687) @ [定義2014](https://github.com/Defined2014)を含むテーブルを処理するときに`ADMIN RECOVER INDEX` `ERROR 1105`を報告する問題を修正しました
    -   `ALTER TABLE t PARTITION BY`実行時に配置ルールを指定するとエラー`ERROR 8239` [＃48630](https://github.com/pingcap/tidb/issues/48630) @ [ミョンス](https://github.com/mjonss)が報告される問題を修正
    -   `INFORMATION_SCHEMA.CLUSTER_INFO`の`START_TIME`列目タイプが[＃45221](https://github.com/pingcap/tidb/issues/45221) @ [ドヴェーデン](https://github.com/dveeden)では有効ではない問題を修正
    -   `INFORMATION_SCHEMA.COLUMNS`の無効な`EXTRA`列タイプがエラー`Data Too Long, field len 30, data len 45` [＃42030](https://github.com/pingcap/tidb/issues/42030) @ [タンジェンタ](https://github.com/tangenta)を引き起こす問題を修正しました
    -   `IN (...)` `INFORMATION_SCHEMA.STATEMENTS_SUMMARY` [＃33559](https://github.com/pingcap/tidb/issues/33559) @ [キング・ディラン](https://github.com/King-Dylan)で異なるプランダイジェストを引き起こす問題を修正
    -   `TIME`型を`YEAR`型に変換すると、返される結果に`TIME`と年[＃48557](https://github.com/pingcap/tidb/issues/48557) @ [ヤンケオ](https://github.com/YangKeao)が混在する問題を修正しました。
    -   `tidb_enable_collect_execution_info`無効にするとコプロセッサキャッシュがpanicになる問題を修正[＃48212](https://github.com/pingcap/tidb/issues/48212) @ [あなた06](https://github.com/you06)
    -   `shuffleExec`予期せず終了すると TiDB がクラッシュする問題を修正[＃48230](https://github.com/pingcap/tidb/issues/48230) @ [うわー](https://github.com/wshwsh12)
    -   静的`CALIBRATE RESOURCE` Prometheusデータ[＃49174](https://github.com/pingcap/tidb/issues/49174) @ [栄光](https://github.com/glorv)に依存している問題を修正
    -   日付に大きな間隔を追加すると、誤った結果が返される問題を修正しました。修正後は、無効なプレフィックスまたは文字列`true`を持つ間隔はゼロとして扱われ、MySQL 8.0 [＃49227](https://github.com/pingcap/tidb/issues/49227) @ [lcwangchao](https://github.com/lcwangchao)と一致します。
    -   `ROW`関数が`null`型を誤って推論し、予期しないエラー[＃49015](https://github.com/pingcap/tidb/issues/49015) @ [うわー](https://github.com/wshwsh12)が発生する問題を修正しました。
    -   `ILIKE`関数がいくつかのシナリオでデータ競合を引き起こす可能性がある問題を修正[＃49677](https://github.com/pingcap/tidb/issues/49677) @ [lcwangchao](https://github.com/lcwangchao)
    -   `STREAM_AGG()` CI [＃49902](https://github.com/pingcap/tidb/issues/49902) @ [うわー](https://github.com/wshwsh12)を誤って処理したためにクエリ結果が正しくない問題を修正しました
    -   バイトを`TIME` [＃47346](https://github.com/pingcap/tidb/issues/47346) @ [うわー](https://github.com/wshwsh12)に変換するときにエンコードが失敗する問題を修正
    -   `CHECK`制約の`ENFORCED`オプションの動作がMySQL 8.0 [＃47567](https://github.com/pingcap/tidb/issues/47567) [＃47631](https://github.com/pingcap/tidb/issues/47631) @ [ジフハウス](https://github.com/jiyfhust)と一致しない問題を修正
    -   `CHECK`制約を持つ DDL ステートメントが[＃47632](https://github.com/pingcap/tidb/issues/47632) @ [ジフハウス](https://github.com/jiyfhust)でスタックする問題を修正しました
    -   メモリ不足のため DDL ステートメントのインデックス追加が失敗する問題を修正[＃47862](https://github.com/pingcap/tidb/issues/47862) @ [GMHDBJD](https://github.com/GMHDBJD)
    -   `ADD INDEX`実行中にクラスターをアップグレードすると、データがインデックス[＃46306](https://github.com/pingcap/tidb/issues/46306) @ [ジムララ](https://github.com/zimulala)と矛盾する可能性がある問題を修正しました。
    -   `tidb_mem_quota_query`システム変数を更新した後に`ADMIN CHECK`実行すると`ERROR 8175` [＃49258](https://github.com/pingcap/tidb/issues/49258) @ [タンジェンタ](https://github.com/tangenta)が返される問題を修正しました
    -   `ALTER TABLE`外部キーによって参照される列の型を変更すると、 `DECIMAL`精度の変更がエラーとして報告されない問題を修正[＃49836](https://github.com/pingcap/tidb/issues/49836) @ [ヨシキポム](https://github.com/yoshikipom)
    -   `ALTER TABLE`外部キーによって参照される列の型を変更すると、 `INTEGER`長さの変更が誤ってエラーとして報告される問題を修正[＃47702](https://github.com/pingcap/tidb/issues/47702) @ [ヨシキポム](https://github.com/yoshikipom)
    -   いくつかのシナリオで式インデックスが除数が 0 [＃50053](https://github.com/pingcap/tidb/issues/50053) @ [lcwangchao](https://github.com/lcwangchao)であることを検出しない問題を修正しました
    -   多数のテーブル[＃50077](https://github.com/pingcap/tidb/issues/50077) @ [ジムララ](https://github.com/zimulala)を処理するときに TiDB ノードが OOM エラーに遭遇する可能性がある問題を軽減します。
    -   クラスターのローリング再起動中に DDL が実行状態のままになる問題を修正[＃50073](https://github.com/pingcap/tidb/issues/50073) @ [タンジェンタ](https://github.com/tangenta)
    -   `PointGet`または`BatchPointGet`演算子を使用してパーティション テーブルのグローバル インデックスにアクセスすると結果が不正確になる可能性がある問題を修正しました[＃47539](https://github.com/pingcap/tidb/issues/47539) @ [L-メープル](https://github.com/L-maple)
    -   生成された列のインデックスが表示可能[＃47766](https://github.com/pingcap/tidb/issues/47766) @ [アイリンキッド](https://github.com/AilinKid)に設定されている場合、MPP プランが選択されない可能性がある問題を修正しました。
    -   `LIMIT` `OR`に押し下げられない問題を修正しました`Index Merge` [＃48588](https://github.com/pingcap/tidb/issues/48588) @ [アイリンキッド](https://github.com/AilinKid)と入力します。
    -   BRインポート[＃46527](https://github.com/pingcap/tidb/issues/46527) @ [qw4990](https://github.com/qw4990)後に`mysql.bind_info`テーブルに重複した組み込み行が存在する可能性がある問題を修正
    -   パーティションが削除された後にパーティションテーブルの統計が期待どおりに更新されない問題を修正[＃48182](https://github.com/pingcap/tidb/issues/48182) @ [ハイラスティン](https://github.com/hi-rustin)
    -   パーティションテーブル[＃48713](https://github.com/pingcap/tidb/issues/48713) @ [ホーキングレイ](https://github.com/hawkingrei)のグローバル統計の同時マージ中にエラーが返される可能性がある問題を修正しました。
    -   PADDING SPACE [＃48821](https://github.com/pingcap/tidb/issues/48821) @ [時間と運命](https://github.com/time-and-fate)の列のインデックス範囲スキャンに`LIKE`演算子を使用すると、クエリ結果が正しくなくなる可能性がある問題を修正しました。
    -   生成された列がメモリ上で同時読み取りと書き込みをトリガーし、データ競合[＃44919](https://github.com/pingcap/tidb/issues/44919) @ [タンジェンタ](https://github.com/tangenta)が発生する可能性がある問題を修正しました。
    -   `WITH 0 TOPN` (トップN統計を収集しないことを示す) が指定されている場合でも、 `ANALYZE TABLE`トップ1統計を収集する可能性がある問題を修正[＃49080](https://github.com/pingcap/tidb/issues/49080) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   不正なオプティマイザヒントによって有効なヒントが無効になる可能性がある問題を修正[＃49308](https://github.com/pingcap/tidb/issues/49308) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   ハッシュパーティションテーブルの統計が、パーティションの追加、削除、再編成、または`TRUNCATE`パーティション[＃48235](https://github.com/pingcap/tidb/issues/48235) [＃48233](https://github.com/pingcap/tidb/issues/48233) [＃48226](https://github.com/pingcap/tidb/issues/48226) [＃48231](https://github.com/pingcap/tidb/issues/48231) @ [ハイラスティン](https://github.com/hi-rustin)を行ったときに、それに応じて更新されない問題を修正しました。
    -   自動統計更新の時間枠を設定した後、その時間枠外でも統計が更新される可能性がある問題を修正[＃49552](https://github.com/pingcap/tidb/issues/49552) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   パーティションテーブルを非パーティションテーブルに変換したときに古い統計情報が自動的に削除されない問題を修正[＃49547](https://github.com/pingcap/tidb/issues/49547) @ [ハイラスティン](https://github.com/hi-rustin)
    -   `TRUNCATE TABLE` [＃49663](https://github.com/pingcap/tidb/issues/49663) @ [ハイラスティン](https://github.com/hi-rustin)を使用してパーティションテーブルからデータをクリアしたときに古い統計が自動的に削除されない問題を修正しました。
    -   クエリがソートを強制するオプティマイザヒント（ `STREAM_AGG()`など）を使用し、実行プランに`IndexMerge` [＃49605](https://github.com/pingcap/tidb/issues/49605) @ [アイリンキッド](https://github.com/AilinKid)が含まれている場合に、強制ソートが無効になる可能性がある問題を修正しました。
    -   ヒストグラムの境界に`NULL` [＃49823](https://github.com/pingcap/tidb/issues/49823) @ [アイリンキッド](https://github.com/AilinKid)が含まれている場合、ヒストグラム統計が読み取り可能な文字列に解析されない可能性がある問題を修正しました。
    -   `GROUP_CONCAT(ORDER BY)`構文を含むクエリを実行するとエラー[＃49986](https://github.com/pingcap/tidb/issues/49986) @ [アイリンキッド](https://github.com/AilinKid)が返される可能性がある問題を修正しました
    -   `SQL_MODE`が厳密でない場合に、 `UPDATE` 、 `DELETE` 、 `INSERT`ステートメントが警告ではなくオーバーフロー エラーを返す問題を修正しました[＃49137](https://github.com/pingcap/tidb/issues/49137) @ [ヤンケオ](https://github.com/YangKeao)
    -   テーブルに複数値インデックスと非バイナリ型文字列[＃49680](https://github.com/pingcap/tidb/issues/49680) @ [ヤンケオ](https://github.com/YangKeao)で構成される複合インデックスがある場合にデータを挿入できない問題を修正
    -   複数レベルのネストされた`UNION`クエリの`LIMIT`無効になる可能性がある問題を修正[＃49874](https://github.com/pingcap/tidb/issues/49874) @ [定義2014](https://github.com/Defined2014)
    -   `BETWEEN ... AND ...`条件でパーティション テーブルをクエリすると誤った結果が返される問題を修正[＃49842](https://github.com/pingcap/tidb/issues/49842) @ [定義2014](https://github.com/Defined2014)
    -   `REPLACE INTO`文[＃34325](https://github.com/pingcap/tidb/issues/34325) @ [ヤンケオ](https://github.com/YangKeao)でヒントが使用できない問題を修正
    -   ハッシュパーティションテーブル[＃50044](https://github.com/pingcap/tidb/issues/50044) @ [定義2014](https://github.com/Defined2014)をクエリするときに TiDB が間違ったパーティションを選択する可能性がある問題を修正しました。
    -   圧縮を有効にした状態でMariaDB Connector/Jを使用する際に発生する接続エラーを修正[＃49845](https://github.com/pingcap/tidb/issues/49845) @ [猫のみ](https://github.com/onlyacat)

-   ティクヴ

    -   破損した SST ファイルが他の TiKV ノードに広がり、TiKV がpanicを起こす可能性がある問題を修正しました[＃15986](https://github.com/tikv/tikv/issues/15986) @ [コナー1996](https://github.com/Connor1996)
    -   オンラインの安全でないリカバリがマージ中止[＃15580](https://github.com/tikv/tikv/issues/15580) @ [v01dスター](https://github.com/v01dstar)を処理できない問題を修正
    -   [＃15817](https://github.com/tikv/tikv/issues/15817) @ [コナー1996](https://github.com/Connor1996)にスケールアウトするときに DR 自動同期のジョイント状態がタイムアウトする可能性がある問題を修正しました。
    -   Titanの`blob-run-mode`オンライン[＃15978](https://github.com/tikv/tikv/issues/15978) @ [トニー](https://github.com/tonyxuqqi)に更新できない問題を修正
    -   解決済みのTSが2時間ブロックされる可能性がある問題を修正[＃11847](https://github.com/tikv/tikv/issues/11847) [＃15520](https://github.com/tikv/tikv/issues/15520) [＃39130](https://github.com/pingcap/tidb/issues/39130) @ [金星の上](https://github.com/overvenus)
    -   `notLeader`または`regionNotFound` [＃15712](https://github.com/tikv/tikv/issues/15712) @ [ヒューシャープ](https://github.com/HuSharp)に遭遇するとフラッシュバックが停止する可能性がある問題を修正しました
    -   TiKV の実行速度が非常に遅い場合、リージョン[＃16111](https://github.com/tikv/tikv/issues/16111)と[金星の上](https://github.com/overvenus)のマージ後にpanicする可能性がある問題を修正しました。
    -   GC が期限切れのロック[＃15066](https://github.com/tikv/tikv/issues/15066) @ [翻訳](https://github.com/cfzjywxk)をスキャンするときに TiKV がメモリ内の悲観的ロックを読み取れない問題を修正
    -   Titan モニタリングの BLOB ファイル サイズが正しくない問題を修正[＃15971](https://github.com/tikv/tikv/issues/15971) @ [コナー1996](https://github.com/Connor1996)
    -   TiCDC を使用して大きなテーブルを複製すると、TiKV が OOM [＃16035](https://github.com/tikv/tikv/issues/16035) @ [金星の上](https://github.com/overvenus)になる可能性がある問題を修正しました。
    -   `DECIMAL`算術乗算切り捨て[＃16268](https://github.com/tikv/tikv/issues/16268) @ [ソロッツ](https://github.com/solotzg)を処理するときに TiDB と TiKV が矛盾した結果を生成する可能性がある問題を修正しました。
    -   `cast_duration_as_time`誤った結果を返す可能性がある問題を修正[＃16211](https://github.com/tikv/tikv/issues/16211) @ [ゲンリキ](https://github.com/gengliqi)
    -   TiKV がブラジルとエジプトのタイムゾーンを誤って変換する問題を修正[＃16220](https://github.com/tikv/tikv/issues/16220) @ [金星の上](https://github.com/overvenus)
    -   gRPC スレッドが`is_shutdown` [＃16236](https://github.com/tikv/tikv/issues/16236) @ [ピンギュ](https://github.com/pingyu)をチェックしているときに TiKV がpanic可能性がある問題を修正しました

-   PD

    -   PD の etcd ヘルスチェックで期限切れのアドレス[＃7226](https://github.com/tikv/pd/issues/7226) @ [イオマンサス](https://github.com/iosmanthus)が削除されない問題を修正
    -   PDリーダーが転送され、新しいリーダーとPDクライアントの間にネットワークパーティションがある場合、PDクライアントがリーダー[＃7416](https://github.com/tikv/pd/issues/7416) @ [キャビンフィーバーB](https://github.com/CabinfeverB)の情報を更新できない問題を修正しました。
    -   Gin Web Framework のバージョンを v1.8.1 から v1.9.1 にアップグレードして、いくつかのセキュリティ問題を修正しました[＃7438](https://github.com/tikv/pd/issues/7438) @ [ニューベル](https://github.com/niubell)
    -   レプリカ数が要件[＃7584](https://github.com/tikv/pd/issues/7584) @ [バッファフライ](https://github.com/bufferflies)を満たしていない場合に孤立ピアが削除される問題を修正

-   TiFlash

    -   クエリ[＃8447](https://github.com/pingcap/tiflash/issues/8447) @ [ジンヘリン](https://github.com/JinheLin)中にTiFlash がメモリ制限に遭遇した場合のメモリリークの問題を修正しました。
    -   `FLASHBACK DATABASE` [＃8450](https://github.com/pingcap/tiflash/issues/8450) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を実行した後もTiFlashレプリカのデータがガベージ コレクションされる問題を修正しました。
    -   クエリが遅いためにメモリ使用量が大幅に増加する問題を修正[＃8564](https://github.com/pingcap/tiflash/issues/8564) @ [ジンヘリン](https://github.com/JinheLin)
    -   `CREATE TABLE`と`DROP TABLE` [＃1664](https://github.com/pingcap/tiflash/issues/1664) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を頻繁に実行するシナリオで、一部のTiFlashレプリカデータが`RECOVER TABLE`または`FLASHBACK TABLE`で回復できない問題を修正
    -   `ColumnRef in (Literal, Func...)` [＃8631](https://github.com/pingcap/tiflash/issues/8631) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)のようなフィルタリング条件でクエリを実行したときにクエリ結果が正しくない問題を修正しました
    -   TiFlash が同時 DDL 実行中に競合に遭遇した場合のTiFlashpanic問題を修正[＃8578](https://github.com/pingcap/tiflash/issues/8578) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   分散storageおよびコンピューティングアーキテクチャ[＃8519](https://github.com/pingcap/tiflash/issues/8519) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)でTiFlash がオブジェクトstorageデータの GC 所有者を選択できない可能性がある問題を修正しました
    -   `lowerUTF8`と`upperUTF8`関数で、大文字と小文字が異なるバイト[＃8484](https://github.com/pingcap/tiflash/issues/8484) @ [ゲンリキ](https://github.com/gengliqi)を占めることができない問題を修正しました。
    -   `ENUM`値が 0 [＃8311](https://github.com/pingcap/tiflash/issues/8311) @ [ソロッツ](https://github.com/solotzg)の場合にTiFlash が`ENUM`誤って処理する問題を修正しました
    -   `INET_NTOA()`式[＃8211](https://github.com/pingcap/tiflash/issues/8211) @ [ソロッツ](https://github.com/solotzg)の非互換性の問題を修正
    -   ストリーム読み取り[＃8505](https://github.com/pingcap/tiflash/issues/8505) @ [ゲンリキ](https://github.com/gengliqi)中に複数のパーティション テーブルをスキャンするときに発生する可能性のある OOM 問題を修正しました。
    -   短いクエリが正常に実行されると過剰な情報ログ[＃8592](https://github.com/pingcap/tiflash/issues/8592) @ [風の話し手](https://github.com/windtalker)が出力される問題を修正しました
    -   TiFlashが停止時にクラッシュする可能性がある問題を修正[＃8550](https://github.com/pingcap/tiflash/issues/8550) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   定数文字列パラメータ[＃8604](https://github.com/pingcap/tiflash/issues/8604) @ [風の話し手](https://github.com/windtalker)を含む`GREATEST`または`LEAST`関数で発生する可能性のあるランダムな無効なメモリアクセスの問題を修正しました。

-   ツール

    -   バックアップと復元 (BR)

        -   BR が外部storageファイル[＃48452](https://github.com/pingcap/tidb/issues/48452) @ [3エースショーハンド](https://github.com/3AceShowHand)に対して誤った URI を生成する問題を修正
        -   タスク初期化中にPDへの接続に失敗すると、ログバックアップタスクは開始できるが正常に動作しない問題を修正[＃16056](https://github.com/tikv/tikv/issues/16056) @ [ユジュンセン](https://github.com/YuJuncen)
        -   ログバックアップタスクがメモリリークに遭遇し、起動後に正常に実行されない可能性がある問題を修正[＃16070](https://github.com/tikv/tikv/issues/16070) @ [ユジュンセン](https://github.com/YuJuncen)
        -   PITRプロセス中にシステムテーブル`mysql.gc_delete_range`にデータを挿入するとエラー[＃49346](https://github.com/pingcap/tidb/issues/49346) @ [リーヴルス](https://github.com/Leavrth)が返される問題を修正しました。
        -   古いバージョン[＃49466](https://github.com/pingcap/tidb/issues/49466) @ [3ポインター](https://github.com/3pointer)のバックアップからデータを復元するときに`Unsupported collation`エラーが報告される問題を修正しました
        -   特定のシナリオでスナップショットを介してユーザー テーブルが回復された後に権限がタイムリーに更新されない問題を修正[＃49394](https://github.com/pingcap/tidb/issues/49394) @ [リーヴルス](https://github.com/Leavrth)

    -   ティCDC

        -   特定のシナリオで`DELETE`ステートメントを複製するときに、 `WHERE`句が主キーを条件として使用しない問題を修正しました[＃9812](https://github.com/pingcap/tiflow/issues/9812) @ [アズドンメン](https://github.com/asddongmen)
        -   オブジェクトstorageサービス[＃10137](https://github.com/pingcap/tiflow/issues/10137) @ [スドジ](https://github.com/sdojjy)にデータを複製するときに TiCDCサーバーがpanicになる可能性がある問題を修正しました
        -   `kv-client`初期化[＃10095](https://github.com/pingcap/tiflow/issues/10095) @ [3エースショーハンド](https://github.com/3AceShowHand)中に発生する可能性のあるデータ競合問題を修正
        -   特定の特殊なシナリオで TiCDC が TiKV との接続を誤って閉じる問題を修正[＃10239](https://github.com/pingcap/tiflow/issues/10239) @ [ヒック](https://github.com/hicqu)
        -   アップストリーム[＃9739](https://github.com/pingcap/tiflow/issues/9739) @ [ヒック](https://github.com/hicqu)で損失のある DDL ステートメントを実行するときに TiCDCサーバーがpanicになる可能性がある問題を修正しました。
        -   TiCDC がデータを下流の MySQL [＃10334](https://github.com/pingcap/tiflow/issues/10334) @ [張金鵬87](https://github.com/zhangjinpeng87)に複製するときに`checkpoint-ts`スタックする可能性がある問題を修正しました。

    -   TiDB データ移行 (DM)

        -   DM が「イベント タイプ切り捨てが無効です」というエラーに遭遇し、アップグレードが失敗する問題を修正しました[＃10282](https://github.com/pingcap/tiflow/issues/10282) @ [GMHDBJD](https://github.com/GMHDBJD)
        -   GTID モード[＃9676](https://github.com/pingcap/tiflow/issues/9676) @ [フェラン・モーガン・ピングキャップ](https://github.com/feran-morgan-pingcap)でデータを複製する際のパフォーマンス低下の問題を修正
        -   下流のテーブル構造に`shard_row_id_bits` [＃10308](https://github.com/pingcap/tiflow/issues/10308) @ [GMHDBJD](https://github.com/GMHDBJD)が含まれている場合に移行タスクエラーが発生する問題を修正しました。

## 寄稿者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   [0o001](https://github.com/0o001) (初めての投稿者)
-   [バゲチェンジ](https://github.com/bagechengzi) (初めての投稿者)
-   [フェラン・モーガン・ピングキャップ](https://github.com/feran-morgan-pingcap) (初めての投稿者)
-   [ハイポン](https://github.com/highpon)
-   [ジフハウス](https://github.com/jiyfhust)
-   [L-メープル](https://github.com/L-maple)
-   [ルクシュミナラヤナン](https://github.com/lkshminarayanan) (初めての投稿者)
-   [りゃん24](https://github.com/lyang24) (初めての投稿者)
-   [ミッタルリシャブ](https://github.com/mittalrishabh)
-   [モルゴ](https://github.com/morgo)
-   [nkg-](https://github.com/nkg-) (初めての投稿者)
-   [猫のみ](https://github.com/onlyacat)
-   [ショーン0915](https://github.com/shawn0915)
-   [スミティズ](https://github.com/Smityz)
-   [szpnygo](https://github.com/szpnygo) (初めての投稿者)
-   [ub-3](https://github.com/ub-3) (初めての投稿者)
-   [シャオヤウェイ](https://github.com/xiaoyawei) (初めての投稿者)
-   [ヨークヘレン](https://github.com/yorkhellen)
-   [ヨシキポム](https://github.com/yoshikipom) (初めての投稿者)
-   [ジェオリ](https://github.com/Zheaoli)
