---
title: TiDB 7.6.0 Release Notes
summary: TiDB 7.6.0 の新機能、互換性の変更点、改善点、およびバグ修正についてご確認ください。
---

# TiDB 7.6.0 リリースノート {#tidb-7-6-0-release-notes}

発売日：2024年1月25日

TiDB バージョン: 7.6.0

クイックアクセス: [クイックスタート](https://docs-archive.pingcap.com/tidb/v7.6/quick-start-with-tidb/)

バージョン7.6.0では、以下の主要な機能と改善点が導入されています。

<table><thead><tr><th>カテゴリ</th><th>機能／改善点</th><th>説明</th></tr></thead><tbody><tr><td rowspan="4">拡張性とパフォーマンス</td><td><a href="https://docs-archive.pingcap.com/tidb/v7.6/sql-plan-management/#cross-database-binding">クロスデータベースSQLバインディング</a></td><td>同じスキーマを持つ数百ものデータベースを管理する場合、これらのデータベース間でSQLバインディングを適用する必要が生じることがよくあります。例えば、SaaSやPaaSのデータプラットフォームでは、通常、各ユーザーが同じスキーマを持つ個別のデータベースを操作し、それらに対して同様のSQLクエリを実行します。このような場合、各データベースごとにSQLを個別にバインドするのは現実的ではありません。TiDB v7.6.0では、スキーマが同等のすべてのデータベース間でバインディングを一致させることができる、データベース間SQLバインディングが導入されました。</td></tr><tr><td> <a href="https://docs-archive.pingcap.com/tidb/v7.6/br-snapshot-guide/#restore-cluster-snapshots">スナップショット復元速度を最大10倍向上（実験的）</a></td><td> BR v7.6.0では、クラスターのスナップショット復元を高速化するための、実験的粗粒度リージョン分散アルゴリズムが導入されました。TiKVノードが多数存在するクラスターでは、このアルゴリズムにより、ノード間で負荷がより均等に分散され、ノードごとのネットワーク帯域幅がより有効に活用されるため、クラスターのリソース効率が大幅に向上します。実際のいくつかの事例では、この改善により復元プロセスが最大約10倍高速化されています。</td></tr><tr><td><a href="https://docs-archive.pingcap.com/tidb/v7.6/ddl-v2/">テーブル作成をバッチ処理で行う際の処理速度を最大10倍向上（実験的）</a></td><td>バージョン7.6.0で新しいDDLアーキテクチャが導入されたことで、バッチテーブル作成のパフォーマンスが最大10倍高速化され、目覚ましい改善が見られました。この大幅な機能強化により、多数のテーブルを作成するのに必要な時間が大幅に短縮されます。この高速化は、数十万から数十万ものテーブルが頻繁に発生するSaaS環境において特に顕著です。</td></tr><tr><td> <a href="https://docs-archive.pingcap.com/tidb/v7.6/tune-region-performance/#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service">アクティブなPDフォロワーを使用してPDのリージョン情報クエリサービスを強化する（実験的）</a></td><td> TiDB v7.6.0では、実験的機能「アクティブPDFollower」が導入されました。これにより、PDフォロワーがリージョン情報クエリサービスを提供できるようになります。この機能は、多数のTiDBノードとリージョンを持つクラスターにおいて、PDクラスターが<code>GetRegion</code>および<code>ScanRegions</code>リクエストを処理する能力を向上させ、PDリーダーのCPU負荷を軽減します。</td></tr><tr><td rowspan="2">信頼性と可用性</td><td><a href="https://docs-archive.pingcap.com/tidb/v7.6/tiproxy-overview/">TiProxyのサポート（実験的）</a></td><td> TiProxyサービスを完全にサポートし、デプロイツールを介して簡単にデプロイできます。これにより、TiDBへの接続を管理および維持し、ローリング再起動、アップグレード、またはスケーリングイベント後も接続が維持されます。</td></tr><tr><td><a href="https://docs-archive.pingcap.com/tidb/v7.6/dm-compatibility-catalog/">データ移行（DM）は、MySQL 8.0（GA）を正式にサポートします。</a></td><td>これまで、DMを使用してMySQL 8.0からデータを移行する機能は実験的機能であり、本番環境では利用できませんでした。TiDB v7.6.0では、この機能の安定性と互換性が向上し、本番環境においてMySQL 8.0からTiDBへのデータ移行をスムーズかつ迅速に行えるようになりました。v7.6.0では、この機能が一般提供（GA）となります。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### 拡張性 {#scalability}

-   Active PD Follower機能を使用して PD のリージョン情報クエリ サービスのスケーラビリティを強化する (実験的) [#7431](https://github.com/tikv/pd/issues/7431) @[CabinfeverB](https://github.com/CabinfeverB)

    リージョン数の多いTiDBクラスタでは、ハートビート処理やタスクスケジューリングに伴うオーバーヘッドが増加するため、PDリーダーのCPU負荷が高くなる可能性があります。クラスタにTiDBインスタンスが多数存在し、リージョン情報へのリクエストが同時に多数発生すると、PDリーダーのCPU負荷はさらに高まり、PDサービスが利用できなくなる恐れがあります。

    高可用性を確保するため、TiDB v7.6.0 では、PD のリージョン情報クエリ サービスの拡張性を向上させる Active PD Follower機能をサポートしています。Active PD Follower機能は、システム変数[`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-new-in-v760) `ON`に設定することで有効にできます。この機能を有効にすると、TiDB はリージョン情報要求をすべての PD サーバーに均等に分散し、PD フォロワーもリージョン要求を処理できるようになるため、PD リーダーの CPU 負荷が軽減されます。

    詳細については、 [ドキュメント](/tune-region-performance.md#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service)を参照してください。

### パフォーマンス {#performance}

-   BRはスナップショットの復元速度を最大 10 倍向上させます (実験的) [#33937](https://github.com/pingcap/tidb/issues/33937) [#49886](https://github.com/pingcap/tidb/issues/49886) @[3pointer](https://github.com/3pointer)

    TiDBクラスタの規模が拡大するにつれて、業務停止時間を最小限に抑えるために、障害発生時にクラスタを迅速に復旧することがますます重要になります。v7.6.0より前は、リージョン分散アルゴリズムがパフォーマンス復旧における主要なボトルネックとなっていました。v7.6.0では、 BRがリージョン分散アルゴリズムを最適化し、復旧タスクを多数の小さなタスクに迅速に分割し、バッチ処理で全てのTiKVノードに分散させます。新しい並列リカバリアルゴリズムは、各TiKVノードのリソースを最大限に活用し、高速な並列リカバリを実現します。実際の運用事例では、大規模なリージョン環境において、クラスタのスナップショット復旧速度が約10倍向上しています。

    新しい粗粒度リージョン散布アルゴリズムは実験的です。これを使用するには、 `--granularity="coarse-grained"`コマンドの`br`パラメータを設定します。例:

    ```bash
    br restore full \
    --pd "${PDIP}:2379" \
    --storage "s3://${Bucket}/${Folder}" \
    --s3.region "${region}" \
    --granularity "coarse-grained" \
    --send-credentials-to-tikv=true \ 
    --log-file restorefull.log
    ```

    詳細については、 [ドキュメント](/br/br-snapshot-guide.md#restore-cluster-snapshots)を参照してください。

-   Titan エンジンはデフォルトで有効になっています [#16245](https://github.com/tikv/tikv/issues/16245) @[Connor1996](https://github.com/Connor1996) @[v01dstar](https://github.com/v01dstar) @[tonyxuqqi](https://github.com/tonyxuqqi)

    TiDB v7.6.0以降では、特にJSONをサポートするTiDBワイドテーブル書き込みシナリオをより適切にサポートするために、Titanエンジンがデフォルトで有効になっています。Titanエンジンは、RocksDBのLSMツリーから32KBを超える大きな値を自動的に分離し、Titanに個別に保存することで、大きな値の処理を最適化します。Titanエンジンは、TiKVで使用されているRocksDBの機能と完全に互換性があります。この戦略的な変更により、書き込み増幅効果が軽減されるだけでなく、大きな値を含む書き込み、更新、およびポイントクエリのシナリオにおけるパフォーマンスも向上します。さらに、レンジスキャンシナリオでは、Titanエンジンの最適化により、デフォルト構成のRocksDBと同等のパフォーマンスを実現しています。

    この構成変更は、以前のバージョンとの互換性を維持しています。既存のTiDBクラスタの場合、TiDB v7.6.0以降のバージョンにアップグレードすると、Titanエンジンはデフォルトで無効になります。お客様の特定の要件に基づいて、Titanエンジンを手動で有効または無効にすることができます。

    詳細については、[ドキュメント](/storage-engine/titan-overview.md)を参照してください。

-   以下の文字列関数をTiKVにプッシュダウンするサポート [#48170](https://github.com/pingcap/tidb/issues/48170) @[gengliqi](https://github.com/gengliqi)

    -   `LOWER()`
    -   `UPPER()`

    詳細については、 [ドキュメント](/functions-and-operators/expressions-pushed-down.md)を参照してください。

-   TiFlashへの以下のJSON関数のプッシュダウンをサポートします[#48350](https://github.com/pingcap/tidb/issues/48350) [#48986](https://github.com/pingcap/tidb/issues/48986) [#48994](https://github.com/pingcap/tidb/issues/48994) [#49345](https://github.com/pingcap/tidb/issues/49345) [#49392](https://github.com/pingcap/tidb/issues/49392) @[SeaRise](https://github.com/SeaRise)@[yibin87](https://github.com/yibin87)

    -   `JSON_UNQUOTE()`
    -   `JSON_ARRAY()`
    -   `JSON_DEPTH()`
    -   `JSON_VALID()`
    -   `JSON_KEYS()`
    -   `JSON_CONTAINS_PATH()`

    詳細については、 [ドキュメント](/tiflash/tiflash-supported-pushdown-calculations.md)を参照してください。

-   テーブル作成のパフォーマンスを10倍向上（実験的） [#49752](https://github.com/pingcap/tidb/issues/49752) @[gmhdbjd](https://github.com/gmhdbjd)

    以前のバージョンでは、数万ものテーブルをアップストリームデータベースからTiDBに移行する際に、TiDBがこれらのテーブルを作成するのに時間がかかり、非効率的でした。v7.6.0以降、TiDBは新しいTiDB DDL V2アーキテクチャを導入しました。システム変数[`tidb_ddl_version`](https://docs-archive.pingcap.com/tidb/v7.6/system-variables/#tidb_ddl_version-new-in-v760)を設定することで有効にできます。以前のバージョンと比較して、新しいバージョンのDDLはバッチテーブルの作成パフォーマンスを10倍向上させ、テーブル作成時間を大幅に短縮します。

    詳細については、 [ドキュメント](https://docs-archive.pingcap.com/tidb/v7.6/ddl-v2/)を参照してください。

-   定期的な完全圧縮をサポート (実験的) [#12729](https://github.com/tikv/tikv/issues/12729) @@ [afeinberg](https://github.com/afeinberg)

    TiDBはv7.6.0以降、TiKVの定期的なフルコンパクションをサポートしています。この機能は、ガベージコレクション（GC）を拡張し、冗長なデータバージョンを排除するものです。アプリケーションのアクティビティに明らかなピークと谷が見られるシナリオでは、この機能を使用してアイドル期間中にデータコンパクションを実行することで、ピーク時のパフォーマンスを向上させることができます。

    TiKV の設定項目[`periodic-full-compact-start-times`](/tikv-configuration-file.md#periodic-full-compact-start-times-new-in-v760)設定することで、TiKV が定期的な完全圧縮を開始する特定の時間を設定できます。また、 [`periodic-full-compact-start-max-cpu`](/tikv-configuration-file.md#periodic-full-compact-start-max-cpu-new-in-v760)を設定することで、TiKV の定期的な完全圧縮の最大 CPU 使用率を制限できます。 `periodic-full-compact-start-max-cpu`のデフォルト値は`0.1`です。これは、TiKV の CPU 使用率が 10% 未満の場合にのみ定期的な完全圧縮がトリガーされることを意味し、アプリケーションのトラフィックへの影響を軽減します。

    詳細については、 [ドキュメント](/tikv-configuration-file.md#periodic-full-compact-start-times-new-in-v760)を参照してください。

### 信頼性 {#reliability}

-   クロスデータベース実行プランのバインディング [#48875](https://github.com/pingcap/tidb/issues/48875) @[qw4990](https://github.com/qw4990)

    TiDB上でSaaSサービスを実行する場合、データの保守管理を容易にするため、テナントごとにデータを個別のデータベースに保存するのが一般的です。その結果、同じテーブルとインデックス定義、そして類似したSQL文を持つデータベースが数百個も存在することになります。このような状況では、SQL文に対して実行プランバインディングを作成すると、通常、そのバインディングは他のデータベースのSQL文にも適用されてしまいます。

    このシナリオでは、TiDB v7.6.0 でクロスデータベースバインディング機能が導入されました。この機能は、異なるデータベースにある場合でも、同じスキーマを持つ SQL ステートメントに同じ実行プランをバインドすることをサポートします。クロスデータベースバインディングを作成する際には、次の例に示すように、データベース名を表すためにワイルドカード`*`を使用する必要があります。バインディングが作成されると、テーブル`t1`と`t2`がどのデータベースにあるかに関係なく、TiDB はこのバインディングを使用して同じスキーマを持つすべての SQL ステートメントの実行プランを生成しようとします。これにより、各データベースごとにバインディングを作成する手間が省けます。

    ```sql
    CREATE GLOBAL BINDING FOR
    USING
        SELECT /*+ merge_join(t1, t2) */ t1.id, t2.amount
        FROM *.t1, *.t2
        WHERE t1.id = t2.id;
    ```

    さらに、クロスデータベースバインディングは、ユーザーデータとワークロードの不均一な分布や急激な変化によって引き起こされるSQLパフォーマンスの問題を効果的に軽減できます。SaaSプロバイダーは、クロスデータベースバインディングを使用して、大量のデータを持つユーザーによって検証された実行プランを修正することで、すべてのユーザーの実行プランを固定できます。SaaSプロバイダーにとって、この機能は利便性とユーザーエクスペリエンスを大幅に向上させます。

    クロスデータベースバインディングによって発生するシステムオーバーヘッド（1%未満）のため、TiDBはこの機能をデフォルトで無効にしています。クロスデータベースバインディングを使用するには、まずシステム変数[`tidb_opt_enable_fuzzy_binding`](/system-variables.md#tidb_opt_enable_fuzzy_binding-new-in-v760)有効にする必要があります。

    詳細については、 [ドキュメント](/sql-plan-management.md#cross-database-binding)を参照してください。

### 可用性 {#availability}

-   プロキシコンポーネントTiProxyのサポート（実験的） [#413](https://github.com/pingcap/tiproxy/issues/413) @[djshow832](https://github.com/djshow832) [xhebox](https://github.com/xhebox)

    TiProxyはTiDBの公式プロキシコンポーネントであり、クライアントとTiDBサーバーの間に配置されます。TiProxyはTiDBの負荷分散と接続維持関数を提供し、TiDBクラスタのワークロードをよりバランス良く分散させ、メンテナンス作業中もデータベースへのユーザーアクセスに影響を与えないようにします。

    -   TiDBクラスタにおけるローリング再起動、ローリングアップグレード、スケールインなどのメンテナンス作業中、TiDBサーバーに変更が発生すると、クライアントとTiDBサーバー間の接続が中断されます。TiProxyを使用することで、これらのメンテナンス作業中に接続を他のTiDBサーバーにスムーズに移行できるため、クライアントへの影響を最小限に抑えることができます。
    -   TiDBサーバーへのクライアント接続を、他のTiDBサーバーに動的に移行することはできません。複数のTiDBサーバーのワークロードが不均衡になると、クラスタ全体のリソースは十分であっても、特定のTiDBサーバーでリソース枯渇が発生し、レイテンシーが大幅に増加する可能性があります。この問題を解決するために、TiProxyは接続の動的移行機能を提供します。これにより、クライアントに影響を与えることなく、接続をあるTiDBサーバーから別のTiDBサーバーに移行できるため、TiDBクラスタの負荷分散が実現されます。

    TiProxyはTiUP、 TiDB Operator、およびTiDB Dashboardに統合されているため、設定、デプロイ、およびメンテナンスが容易です。

    詳細については、[ドキュメント](/tiproxy/tiproxy-overview.md)を参照してください。

### SQL {#sql}

-   `LOAD DATA`は明示的なトランザクションとロールバックをサポートします [#49079](https://github.com/pingcap/tidb/pull/49079) @[ekexium](https://github.com/ekexium)

    MySQLと比較すると、v7.6.0より前のTiDBバージョンでは`LOAD DATA`ステートメントのトランザクション動作が異なるため、このステートメントを使用する際には追加の調整が必要になる場合があります。具体的には、v4.0.0より前では、 `LOAD DATA`は20000行ごとにコミットされます。v4.0.0からv6.6.0までは、TiDBはデフォルトで1つのトランザクションですべての行をコミットし、 [`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size)システム変数を設定することで固定行数ごとにコミットすることもサポートしています。v7.0.0以降では、 `tidb_dml_batch_size` `LOAD DATA`には適用されなくなり、TiDBは1つのトランザクションですべての行をコミットします。

    バージョン7.6.0以降、TiDBはトランザクション内で`LOAD DATA`他のDMLステートメントと同様に、特にMySQLと同様に処理します。トランザクション内の`LOAD DATA`ステートメントは、現在のトランザクションを自動的にコミットしたり、新しいトランザクションを開始したりしなくなりました。さらに、トランザクション内の`LOAD DATA`ステートメントを明示的にコミットまたはロールバックできます。また、 `LOAD DATA`ステートメントは、TiDBトランザクションモード設定（楽観的トランザクションまたは悲観的トランザクション）の影響を受けます。これらの改善により、MySQLからTiDBへの移行プロセスが簡素化され、データインポートにおいてより統一的で制御しやすいエクスペリエンスが提供されます。

    詳細については、 [ドキュメント](/sql-statements/sql-statement-load-data.md)を参照してください。

### データベース操作 {#db-operations}

-   `FLASHBACK CLUSTER`は、正確な TSO [#48372](https://github.com/pingcap/tidb/issues/48372) @ [BornChanger](https://github.com/BornChanger)の指定をサポートしています

    TiDB v7.6.0 では、フラッシュバック機能がより強力かつ正確になりました。クラスタを指定した履歴タイムスタンプにロールバックできるだけでなく、 `FLASHBACK CLUSTER TO TSO`を使用して正確なリカバリ[TSO](/tso.md)指定できるため、データリカバリの柔軟性が向上します。たとえば、この機能を TiCDC と組み合わせて使用​​できます。ダウンストリームの TiDB クラスタでデータレプリケーションを一時停止し、オンライン前の読み書きテストを実行した後、この機能を使用すると、クラスタは一時停止した TSO にスムーズかつ迅速にロールバックし、TiCDC を使用してデータのレプリケーションを再開できます。これにより、オンライン前の検証プロセスが効率化され、データ管理が簡素化されます。

    ```sql
    FLASHBACK CLUSTER TO TSO 445494839813079041;
    ```

    詳細については、 [ドキュメント](/sql-statements/sql-statement-flashback-cluster.md)を参照してください。

-   長時間実行されているアイドル状態のトランザクションを自動的に終了させる機能のサポート [#48714](https://github.com/pingcap/tidb/pull/48714) @[crazycs520](https://github.com/crazycs520)

    ネットワーク切断やアプリケーション障害が発生するシナリオでは、 `COMMIT` / `ROLLBACK`ステートメントがデータベースに送信されない可能性があります。これにより、データベース ロックの解放が遅延し、トランザクション ロック待機が発生し、データベース接続が急増する可能性があります。このような問題はテスト環境ではよく発生しますが、本番環境でも時折発生する可能性があり、迅速な診断が難しい場合があります。これらの問題を回避するために、TiDB v7.6.0 では、長時間実行されているアイドル状態のトランザクションを自動的に終了する[`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760)システム変数が導入されました。トランザクション状態のユーザー セッションがこの変数の値を超える期間アイドル状態になると、TiDB はトランザクションのデータベース接続を終了し、トランザクションをロールバックします。

    詳細については、 [ドキュメント](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760)を参照してください。

-   実行プランバインディングを作成するための構文を簡素化する [#48876](https://github.com/pingcap/tidb/issues/48876) @[qw4990](https://github.com/qw4990)

    TiDB v7.6.0 では、実行プランバインディングを作成するための構文が簡素化されました。実行プランバインディングを作成する際に、元の SQL ステートメントを指定する必要がなくなりました。TiDB は、ヒント付きのステートメントに基づいて元の SQL ステートメントを識別します。この改善により、実行プランバインディングの作成がより便利になります。例:

    ```sql
    CREATE GLOBAL BINDING
    USING
    SELECT /*+ merge_join(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
    ```

    詳細については、 [ドキュメント](/sql-plan-management.md#create-a-binding-according-to-a-sql-statement)を参照してください。

-   TiDB で単一行レコードのサイズ制限を動的に変更する機能をサポート [#49237](https://github.com/pingcap/tidb/pull/49237) @[zyguan](https://github.com/zyguan)

    v7.6.0 より前では、トランザクション内の単一行レコードのサイズは、TiDB 構成項目[`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v4010-and-v500)によって制限されていました。サイズ制限を超えると、TiDB は`entry too large`エラーを返します。この場合、TiDB 構成ファイルを手動で変更し、TiDB を再起動して変更を有効にする必要があります。管理オーバーヘッドを削減するために、TiDB v7.6.0 では`txn-entry-size-limit`構成項目の値を動的に変更できるシステム変数[`tidb_txn_entry_size_limit`](/system-variables.md#tidb_txn_entry_size_limit-new-in-v760)が導入されました。この変数のデフォルト値は`0`であり、これは TiDB がデフォルトで構成項目`txn-entry-size-limit`の値を使用することを意味します。この変数にゼロ以外の値を設定すると、TiDB はトランザクション内の行レコードのサイズをこの変数の値に制限します。この改善により、TiDB を再起動することなくシステム構成を調整できる柔軟性が向上します。

    詳細については、 [ドキュメント](/system-variables.md#tidb_txn_entry_size_limit-new-in-v760)を参照してください。

-   BR はデフォルトでユーザー データなどのシステム テーブルを復元します[#48567](https://github.com/pingcap/tidb/issues/48567) @[BornChanger](https://github.com/BornChanger) [#49627](https://github.com/pingcap/tidb/issues/49627) @[Leavrth](https://github.com/Leavrth)

    バージョン5.1.0以降、スナップショットをバックアップすると、 BRは`mysql`スキーマ内のシステムテーブルを自動的にバックアップしますが、デフォルトではこれらのシステムテーブルを復元しません。バージョン6.2.0では、 BRは`--with-sys-table`パラメータを追加し、一部のシステムテーブルのデータを復元できるようにすることで、操作の柔軟性を向上させています。

    管理の手間をさらに軽減し、より直感的なデフォルト動作を実現するために、バージョン7.6.0以降、 BRはデフォルトで`--with-sys-table`パラメータを有効にします。これにより、 BRは復元時に一部のシステムテーブル、特にユーザーアカウントとテーブル統計データをデフォルトで復元します。この改善により、バックアップと復元操作がより直感的になり、手動設定の負担が軽減され、全体的な操作性が向上します。

    詳細については、[ドキュメント](/br/br-snapshot-guide.md)を参照してください。

### 可観測性 {#observability}

-   リソース制御に関する可観測性の強化 [#49318](https://github.com/pingcap/tidb/issues/49318) @[glorv](https://github.com/glorv)@ [bufferflies](https://github.com/bufferflies)@ [nolouch](https://github.com/nolouch)

    アプリケーションのワークロードを分離するためにリソース グループを使用するユーザーが増えるにつれ、リソース コントロールはリソース グループに基づいた強化されたデータを提供します。これにより、リソース グループのワークロードと設定を監視し、次のような問題を迅速かつ正確に特定して診断できるようになります。

    -   [スロークエリ](/identify-slow-queries.md): リソース グループ名、リソース ユニット (RU) の消費量、およびリソースの待機時間を追加します。
    -   [ステートメントサマリーテーブル](/statement-summary-tables.md): リソース グループ名、RU 消費量、リソースの待機時間を追加します。
    -   システム変数[`tidb_last_query_info`](/system-variables.md#tidb_last_query_info-new-in-v4014)に、SQL ステートメントによって消費された[RU](/tidb-resource-control-ru-groups.md#what-is-request-unit-ru)を示す新しいエントリ`ru_consumption`を追加します。この変数を使用して、セッション内の最後のステートメントのリソース消費量を取得できます。
    -   リソースグループに基づいてデータベースのメトリックを追加します。具体的には、QPS/TPS、実行時間（P999/P99/P95）、障害発生回数、接続数などです。
    -   すべてのリソースグループの1日あたりのRU消費量の履歴レコードを記録するために、システムテーブル[`request_unit_by_group`](/mysql-schema/mysql-schema.md#system-tables-related-to-resource-control)を追加します。

    詳細については、[スロークエリを特定する](/identify-slow-queries.md)、[ステートメントサマリーテーブル](/statement-summary-tables.md)、および[リソース制御の主要監視指標](/grafana-resource-control-dashboard.md)を参照してください。

### データ移行 {#data-migration}

-   MySQL 8.0への移行をサポートするデータ移行（DM）機能が一般提供開始（GA）になりました [#10405](https://github.com/pingcap/tiflow/issues/10405) @[lyzx2001](https://github.com/lyzx2001)

    これまで、DMを使用してMySQL 8.0からデータを移行する機能は実験的機能であり、本番環境では利用できませんでした。TiDB v7.6.0では、この機能の安定性と互換性が向上し、本番環境においてMySQL 8.0からTiDBへのデータ移行をスムーズかつ迅速に行えるようになりました。v7.6.0では、この機能が一般提供（GA）となります。

    詳細については、[ドキュメント](/dm/dm-compatibility-catalog.md)を参照してください。

-   TiCDCは双方向レプリケーション（BDR）モードでのDDLステートメントのレプリケーションをサポートします（実験的） [#10301](https://github.com/pingcap/tiflow/issues/10301) [#48519](https://github.com/pingcap/tidb/issues/48519) @[okJiang](https://github.com/okJiang) @[asddongmen](https://github.com/asddongmen)

    バージョン7.6.0以降、TiCDCは双方向レプリケーションが構成されたDDLステートメントのレプリケーションをサポートします。以前は、TiCDCはDDLステートメントのレプリケーションをサポートしていなかったため、TiCDCの双方向レプリケーションを使用するユーザーは、DDLステートメントを両方のTiDBクラスタに個別に適用する必要がありました。この機能により、TiCDCはクラスタに`PRIMARY` BDRロールを割り当てることができ、そのクラスタからダウンストリームクラスタへのDDLステートメントのレプリケーションが可能になります。

    詳細については、 [ドキュメント](/ticdc/ticdc-bidirectional-replication.md)を参照してください。

-   TiCDCは、チェンジフィードの下流同期ステータスのクエリをサポートします [#10289](https://github.com/pingcap/tiflow/issues/10289) @[hongyunyan](https://github.com/hongyunyan)

    バージョン7.6.0以降、TiCDCは、指定されたレプリケーションタスク（チェンジフィード）のダウンストリーム同期ステータスを照会するための新しいAPI `GET /api/v2/changefeed/{changefeed_id}/synced`を導入しました。このAPIを使用することで、TiCDCが受信したアップストリームデータがダウンストリームシステムに完全に同期されているかどうかを判断できます。

    詳細については、 [ドキュメント](/ticdc/ticdc-open-api-v2.md#query-whether-a-specific-replication-task-is-completed)を参照してください。

-   TiCDCがCSV出力プロトコルで3文字区切り文字のサポートを追加 [#9969](https://github.com/pingcap/tiflow/issues/9969) @[zhangjinpeng87](https://github.com/zhangjinpeng87)

    バージョン7.6.0以降では、CSV出力プロトコルの区切り文字を1～3文字の長さで指定できるようになりました。この変更により、TiCDCは、出力内のフィールドを区切るために、2文字の区切り文字（ `||`や`$^`など）または3文字の区切り文字（ `|@|`など）を使用してファイル出力を生成するように構成できます。

    詳細については、[ドキュメント](/ticdc/ticdc-csv.md)を参照してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、バージョン7.5.0から最新バージョン（7.6.0）にアップグレードする際に知っておくべき互換性の変更点について説明します。バージョン7.4.0以前のバージョンから最新バージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更点も確認する必要があるかもしれません。

### MySQLとの互換性 {#mysql-compatibility}

-   TiDB v7.6.0 より前は、 `LOAD DATA`操作は、単一のトランザクションですべての行をコミットするか、トランザクションをバッチでコミットしていました。これは MySQL の動作とは若干異なります。v7.6.0 以降、TiDB は`LOAD DATA` MySQL と同様にトランザクションで処理します。トランザクション内の`LOAD DATA`ステートメントは、現在のトランザクションを自動的にコミットしたり、新しいトランザクションを開始したりしなくなりました。さらに、トランザクション内の`LOAD DATA`ステートメントを明示的にコミットまたはロールバックできます。また、 `LOAD DATA`ステートメントは、TiDB のトランザクション モード設定 (楽観的トランザクションまたは悲観的トランザクション) の影響を受けます。 [#49079](https://github.com/pingcap/tidb/pull/49079) @[ekexium](https://github.com/ekexium)

### システム変数 {#system-variables}

| 変数名                                                                                                                 | 変更の種類  | 説明                                                                                                                                                                                                                                                                                                                      |
| ------------------------------------------------------------------------------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_auto_analyze_partition_batch_size`](/system-variables.md#tidb_auto_analyze_partition_batch_size-new-in-v640) | 変更     | さらなるテストの結果、デフォルト値を`1`から`128`に変更します。                                                                                                                                                                                                                                                                                     |
| [`tidb_sysproc_scan_concurrency`](/system-variables.md#tidb_sysproc_scan_concurrency-new-in-v650)                   | 変更     | 大規模クラスタでは、 `scan`操作の同時実行数を`ANALYZE`のニーズに合わせて高く調整できます。したがって、最大値を`256`から`4294967295`に変更します。                                                                                                                                                                                                                               |
| [`tidb_analyze_distsql_scan_concurrency`](/system-variables.md#tidb_analyze_distsql_scan_concurrency-new-in-v760)   | 新しく追加された | `scan`操作を実行する際の`ANALYZE`操作の同時実行数を設定します。デフォルト値は`4`です。                                                                                                                                                                                                                                                                    |
| [`tidb_ddl_version`](https://docs-archive.pingcap.com/tidb/v7.6/system-variables/#tidb_ddl_version-new-in-v760)     | 新しく追加された | [TiDB DDL V2](https://docs-archive.pingcap.com/tidb/v7.6/ddl-v2/)を有効にするかどうかを制御します。有効にするには`2`に、無効にするには`1`に値を設定します。デフォルト値は`1`です。TiDB DDL V2 が有効になっている場合、DDL ステートメントは TiDB DDL V2 を使用して実行されます。テーブルを作成する DDL ステートメントの実行速度は、TiDB DDL V1 と比較して 10 倍向上します。                                                                     |
| [`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-new-in-v760)                             | 新しく追加された | パーティションテーブルに対して`Global indexes`を作成するかどうかを制御します。デフォルト値は`OFF`です。 `Global index`は現在開発段階です。**このシステム変数の値を変更することは推奨されません**。                                                                                                                                                                                                   |
| [`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760)                   | 新しく追加された | ユーザーセッションにおけるトランザクションのアイドルタイムアウトを制御します。ユーザーセッションがトランザクション状態にあり、この変数の値を超える時間アイドル状態が続くと、TiDB はセッションを終了します。デフォルト値`0`は無制限を意味します。                                                                                                                                                                                            |
| [`tidb_ignore_inlist_plan_digest`](/system-variables.md#tidb_ignore_inlist_plan_digest-new-in-v760)                 | 新しく追加された | プランダイジェストを生成する際に、TiDB が異なるクエリ間で`IN`リスト内の要素の差異を無視するかどうかを制御します。デフォルト値`OFF`は、差異を無視しないことを意味します。                                                                                                                                                                                                                             |
| [`tidb_opt_enable_fuzzy_binding`](/system-variables.md#tidb_opt_enable_fuzzy_binding-new-in-v760)                   | 新しく追加された | クロスデータベースバインディング機能を有効にするかどうかを制御します。デフォルト値`OFF`は、クロスデータベースバインディングが無効であることを意味します。                                                                                                                                                                                                                                         |
| [`tidb_txn_entry_size_limit`](/system-variables.md#tidb_txn_entry_size_limit-new-in-v760)                           | 新しく追加された | TiDB 構成項目[`performance.txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v4010-and-v500)を動的に変更します。これは、TiDB 内の単一行のデータのサイズを制限します。この変数のデフォルト値は`0`です。これは、TiDB がデフォルトで構成項目`txn-entry-size-limit`の値を使用することを意味します。この変数がゼロ以外の値に設定されている場合、 `txn-entry-size-limit`も同じ値に設定されます。                       |
| [`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-new-in-v760)             | 新しく追加された | 有効にするかどうかを制御します[アクティブなPDFollower](/tune-region-performance.md#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service)機能 (実験的)。値が`OFF`の場合、TiDB は PD リーダーからのみリージョン情報を取得します。値が`ON`の場合、TiDB はリージョン情報の要求をすべての PD サーバーに均等に分散し、PD フォロワーもリージョン要求を処理できるため、PD リーダーの CPU 負荷が軽減されます。 |

### コンフィグレーションファイルパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                                                                        | 変更の種類  | 説明                                                                                                                                                                                                                        |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | [`tls-version`](/tidb-configuration-file.md#tls-version)                                                                                               | 変更     | デフォルト値は &quot;&quot; です。TiDB のデフォルトのサポート TLS バージョンが`TLS1.1`以上から`TLS1.2`以上に変更されました。                                                                                                                                        |
| TiKV           | [`raftstore.report-min-resolved-ts-interval`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file/#report-min-resolved-ts-interval-new-in-v600) | 名称変更     | 名前をより正確にするため、この構成項目は[`raftstore.pd-report-min-resolved-ts-interval`](/tikv-configuration-file.md#pd-report-min-resolved-ts-interval-new-in-v760)に名前が変更されました。 `raftstore.report-min-resolved-ts-interval`は無効になりました。        |
| TiKV           | [`blob-file-compression`](/tikv-configuration-file.md#blob-file-compression)                                                                           | 変更     | Titan で値を圧縮するために使用されるアルゴリズムで、値を単位とします。TiDB v7.6.0 以降、デフォルトの圧縮アルゴリズムは`zstd`です。                                                                                                                                             |
| TiKV           | [`rocksdb.defaultcf.titan.min-blob-size`](/tikv-configuration-file.md#min-blob-size)                                                                   | 変更     | TiDB v7.6.0以降、新規クラスタのデフォルト値は`32KB`となります。v7.6.0にアップグレードする既存クラスタの場合、デフォルト値`1KB`は変更されません。                                                                                                                                    |
| TiKV           | [`rocksdb.titan.enabled`](/tikv-configuration-file.md#enabled)                                                                                         | 変更     | Titan を有効または無効にします。v7.5.0 以前のバージョンでは、デフォルト値は`false`です。v7.6.0 以降では、新規クラスターの場合のみデフォルト値は`true`になります。v7.6.0 以降のバージョンにアップグレードされた既存のクラスターは、元の構成を維持します。                                                                          |
| TiKV           | [`cdc.incremental-scan-concurrency-limit`](/tikv-configuration-file.md#incremental-scan-concurrency-limit-new-in-v760)                                 | 新しく追加された | 履歴データを増分スキャンするタスクの実行待ちキューの最大長を設定します。デフォルト値は`10000`で、これは最大 10000 個のタスクを実行待ちキューに入れることができることを意味します。                                                                                                                          |
| TiKV           | [`gc.num-threads`](/tikv-configuration-file.md#num-threads-new-in-v658-v714-v751-and-v760)                                                             | 新しく追加された | `enable-compaction-filter` `false`に設定すると、このパラメータは GC スレッドの数を制御します。デフォルト値は`1`です。                                                                                                                                           |
| TiKV           | [`raftstore.periodic-full-compact-start-times`](/tikv-configuration-file.md#periodic-full-compact-start-times-new-in-v760)                             | 新しく追加された | TiKVが定期的な完全圧縮を開始する具体的な時間を設定します。デフォルト値`[]`は、定期的な完全圧縮が無効になっていることを意味します。                                                                                                                                                     |
| TiKV           | [`raftstore.periodic-full-compact-start-max-cpu`](/tikv-configuration-file.md#periodic-full-compact-start-max-cpu-new-in-v760)                         | 新しく追加された | TiKVの定期的な完全圧縮における最大CPU使用率を制限します。デフォルト値は`0.1`です。                                                                                                                                                                           |
| TiKV           | [`raftstore.pd-report-min-resolved-ts-interval`](/tikv-configuration-file.md#pd-report-min-resolved-ts-interval-new-in-v760)                           | 新しく追加された | [`raftstore.report-min-resolved-ts-interval`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#report-min-resolved-ts-interval-new-in-v600)から名前が変更されました。TiKV が解決済み TS を PD リーダーに報告する最小間隔を指定します。デフォルト値は`"1s"`です。 |
| TiKV           | [`zstd-dict-size`](/tikv-configuration-file.md#zstd-dict-size)                                                                                         | 新しく追加された | `zstd`辞書の圧縮サイズを指定します。デフォルト値は`"0KB"`で、これは`zstd`辞書の圧縮を無効にすることを意味します。                                                                                                                                                        |
| TiFlash        | [`logger.level`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                                                                     | 変更     | ログ記録のコストを削減するために、デフォルト値を`"debug"`から`"INFO"`に変更します。                                                                                                                                                                        |
| TiDB Lightning | [`tidb.pd-addr`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)                                                                  | 変更     | PDサーバーのアドレスを設定します。バージョン7.6.0以降、TiDBは複数のPDアドレスの設定をサポートしています。                                                                                                                                                               |
| TiDB Lightning | [`block-size`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)                                                                    | 新しく追加された | 物理インポートモード（ `backend='local'` ）でローカルファイルをソートするためのI/Oブロックサイズを制御します。デフォルト値は`16KiB`です。ディスクIOPSがボトルネックになっている場合は、この値を増やすことでパフォーマンスを向上させることができます。                                                                               |
| BR             | [`--granularity`](/br/br-snapshot-guide.md#performance-and-impact-of-snapshot-restore)                                                                 | 新しく追加された | `--granularity="coarse-grained"`を指定することで、粗粒度リージョン散布アルゴリズム（実験的）を使用します。これにより、大規模なリージョンシナリオにおける復元速度が向上します。                                                                                                                   |
| TiCDC          | [`compression`](/ticdc/ticdc-changefeed-config.md)                                                                                                     | 新しく追加された | リドゥログファイルの圧縮動作を制御します。                                                                                                                                                                                                     |
| TiCDC          | [`sink.cloud-storage-config`](/ticdc/ticdc-changefeed-config.md)                                                                                       | 新しく追加された | オブジェクトストレージにデータを複製する際に、履歴データの自動クリーンアップを設定します。                                                                                                                                                                           |

### システムテーブル {#system-tables}

-   TiDBでサポートされているすべてのキーワードの情報を表示するために、新しいシステムテーブル[`INFORMATION_SCHEMA.KEYWORDS`](/information-schema/information-schema-keywords.md)を追加します。
-   システムテーブル[`INFORMATION_SCHEMA.SLOW_QUERY`](/information-schema/information-schema-slow-query.md)に、リソース制御に関連する以下のフィールドを追加します。
    -   `Resource_group` : ステートメントがバインドされているリソース グループ。
    -   `Request_unit_read` : ステートメントによって消費された読み取り RU の合計。
    -   `Request_unit_write` : ステートメントによって消費された書き込み RU の合計。
    -   `Time_queued_by_rc` : ステートメントが利用可能なリソースを待機する合計時間。

## オフラインパッケージの変更 {#offline-package-changes}

v7.6.0 以降、 `TiDB-community-server`[バイナリパッケージ](/binary-package.md)には、プロキシ コンポーネント[TiProxy](/tiproxy/tiproxy-overview.md)のインストール パッケージである`tiproxy-{version}-linux-{arch}.tar.gz`含まれるようになりました。

## 非推奨機能 {#deprecated-features}

-   TiDB v7.6.0ではTLSv1.0およびTLSv1.1プロトコルのサポートは非​​推奨となり、v8.0.0で削除されます。TLSv1.2またはTLSv1.3にアップグレードしてください。
-   実行計画の [ベースラインの進化](/sql-plan-management.md#baseline-evolution)機能は、TiDB v8.0.0 で非推奨になります。同等の機能は後続のバージョンで再設計される予定です。
-   TiDB v8.0.0では、システム変数[`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry)が非推奨となります。それ以降、TiDBは楽観的トランザクションの自動再試行をサポートしなくなります。

## 改善点 {#improvements}

-   TiDB

    -   非バイナリ照合順序が設定され、クエリに`LIKE`が含まれる場合、オプティマイザは実行効率を向上させるために`IndexRangeScan`を生成します[#48181](https://github.com/pingcap/tidb/issues/48181) [#49138](https://github.com/pingcap/tidb/issues/49138) @[time-and-fate](https://github.com/time-and-fate)
    -   特定のシナリオにおいて`OUTER JOIN`を`INNER JOIN`に変換する機能を強化する [#49616](https://github.com/pingcap/tidb/issues/49616) @[qw4990](https://github.com/qw4990)
    -   ノードが再起動されるシナリオにおける分散実行フレームワーク（DXF）タスクのバランスを改善する [#47298](https://github.com/pingcap/tidb/issues/47298) @[ywqzzy](https://github.com/ywqzzy)
    -   複数の高速化された`ADD INDEX` DDL タスクをキューに入れて実行できるようにサポートします。通常の`ADD INDEX`タスクにフォールバックするのではなく、実行します。 [#47758](https://github.com/pingcap/tidb/issues/47758) @[tangenta](https://github.com/tangenta)
    -   `ALTER TABLE ... ROW_FORMAT`の互換性を改善 [#48754](https://github.com/pingcap/tidb/issues/48754) @[hawkingrei](https://github.com/hawkingrei)
    -   `CANCEL IMPORT JOB`ステートメントを同期ステートメントに変更します [#48736](https://github.com/pingcap/tidb/issues/48736) @[D3Hunter](https://github.com/D3Hunter)
    -   空のテーブルへのインデックス追加速度の改善 [#49682](https://github.com/pingcap/tidb/issues/49682) @[zimulala](https://github.com/zimulala)
    -   相関サブクエリの列が上位レベルの演算子によって参照されていない場合、相関サブクエリは直接削除できます [#45822](https://github.com/pingcap/tidb/issues/45822) @[King-Dylan](https://github.com/King-Dylan)
    -   `EXCHANGE PARTITION`操作により、統計情報のメンテナンス更新がトリガーされるようになりました [#47354](https://github.com/pingcap/tidb/issues/47354) @[Rustin170506](https://github.com/Rustin170506)
    -   TiDBは、連邦情報処理標準（FIPS）の要件を満たすバイナリファイルの作成をサポートしています。 [#47948](https://github.com/pingcap/tidb/issues/47948) @[tiancaiamao](https://github.com/tiancaiamao)
    -   一部の型変換を処理する際の TiDB 実装を最適化し、関連する問題を修正します[#47945](https://github.com/pingcap/tidb/issues/47945) [#47864](https://github.com/pingcap/tidb/issues/47864) [#47829](https://github.com/pingcap/tidb/issues/47829) [#47816](https://github.com/pingcap/tidb/issues/47816) @[YangKeao](https://github.com/YangKeao)@[lcwangchao](https://github.com/lcwangchao)
    -   スキーマバージョンを取得する際、TiDBはデフォルトでKVタイムアウト機能を使用して読み取りを行うため、遅いメタリージョンリーダーの読み取りがスキーマバージョン更新に与える影響が軽減されます。 [#48125](https://github.com/pingcap/tidb/pull/48125) @[cfzjywxk](https://github.com/cfzjywxk)

-   TiKV

    -   非同期タスクを照会するためのAPIエンドポイント`/async_tasks`を追加 [#15759](https://github.com/tikv/tikv/issues/15759) @[YuJuncen](https://github.com/YuJuncen)
    -   gRPC モニタリングに優先度ラベルを追加して、異なる優先度のリソース グループ データを表示します [#49318](https://github.com/pingcap/tidb/issues/49318) @[bufferflies](https://github.com/bufferflies)
    -   `readpool.unified.max-tasks-per-worker`の値を動的に調整することで、優先度に基づいて実行中のタスク数を個別に計算できます [#16026](https://github.com/tikv/tikv/issues/16026) @[glorv](https://github.com/glorv)
    -   GCスレッド数を動的に調整する機能をサポート。デフォルト値は`1` [#16101](https://github.com/tikv/tikv/issues/16101) @[tonyxuqqi](https://github.com/tonyxuqqi)

-   PD

    -   ディスクジッター時のPD TSOの可用性を向上させる [#7377](https://github.com/tikv/pd/issues/7377) @[HuSharp](https://github.com/HuSharp)

-   TiFlash

    -   読み取りレイテンシーに対するディスク パフォーマンス ジッターの影響を軽減 [#8583](https://github.com/pingcap/tiflash/issues/8583) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   バックグラウンド GC タスクの読み取りおよび書き込みタスクのレイテンシーへの影響を軽減 [#8650](https://github.com/pingcap/tiflash/issues/8650) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   ストレージとコンピューティングを分離したアーキテクチャで同一のデータ読み取り操作をマージして、高並行処理下でのデータスキャン性能を向上させるサポート [#6834](https://github.com/pingcap/tiflash/issues/6834) @[JinheLin](https://github.com/JinheLin)
    -   `SEMI JOIN`と`LEFT OUTER SEMIJOIN`の実行パフォーマンスを最適化する`JOIN ON`に JOIN KEY 等価条件のみが含まれる場合） [#47424](https://github.com/pingcap/tidb/issues/47424) @[gengliqi](https://github.com/gengliqi)

-   ツール

    -   Backup & Restore (BR)

        -   フルバックアップリカバリフェーズ中に Amazon S3 `session-token`および`assume-role`を使用した認証をサポート [#39832](https://github.com/pingcap/tidb/issues/39832) @[3pointer](https://github.com/3pointer)
        -   `delete range`シナリオにおけるポイントインタイムリカバリ (PITR) の新しい統合テストを導入し、PITR の安定性を向上させます [#47738](https://github.com/pingcap/tidb/issues/47738) @[Leavrth](https://github.com/Leavrth)
        -   大規模データセットのシナリオにおける`RESTORE`ステートメントのテーブル作成パフォーマンスを改善 [#48301](https://github.com/pingcap/tidb/issues/48301) @[Leavrth](https://github.com/Leavrth)
        -   BR例外処理メカニズムをリファクタリングして、不明なエラーに対する耐性を高めます [#47656](https://github.com/pingcap/tidb/issues/47656) @[3pointer](https://github.com/3pointer)

    -   TiCDC

        -   TiCDCによるオブジェクトストレージへのデータ複製パフォーマンスを並列処理の増加によって改善する [#10098](https://github.com/pingcap/tiflow/issues/10098) @[CharlesCheung96](https://github.com/CharlesCheung96)
        -   `content-compatible=true` [公式Canal出力のコンテンツ形式と互換性がある](/ticdc/ticdc-canal-json.md#compatibility-with-the-official-canal)`sink-uri`の@ [3AceShowHand](https://github.com/3AceShowHand) [#10106](https://github.com/pingcap/tiflow/issues/10106)

    -   TiDB Data Migration (DM)

        -   DM OpenAPIへのフルデータ物理インポートの設定を追加 [#10193](https://github.com/pingcap/tiflow/issues/10193) @[GMHDBJD](https://github.com/GMHDBJD)

    -   TiDB Lightning

        -   安定性を高めるために複数の PD アドレスの構成をサポート [#49515](https://github.com/pingcap/tidb/issues/49515) @[mittalrishabh](https://github.com/mittalrishabh)
        -   ローカルファイルのソートにおけるI/Oブロックサイズを制御するための`block-size`パラメータの設定をサポートし、パフォーマンスを向上させます [#45037](https://github.com/pingcap/tidb/issues/45037) @[mittalrishabh](https://github.com/mittalrishabh)

## バグ修正 {#bug-fixes}

-   TiDB

    -   TiDBがパニックを起こしてエラー`invalid memory address or nil pointer dereference`を報告する問題を修正 [#42739](https://github.com/pingcap/tidb/issues/42739) @[CbcWestwolf](https://github.com/CbcWestwolf)
    -   DDL `jobID`が 0 に復元されたときに発生する TiDB ノードpanicの問題を修正 [#46296](https://github.com/pingcap/tidb/issues/46296) @[jiyfhust](https://github.com/jiyfhust)
    -   同じクエリプランでも異なる`PLAN_DIGEST`値が存在する場合がある問題を修正 [#47634](https://github.com/pingcap/tidb/issues/47634) @[King-Dylan](https://github.com/King-Dylan)
    -   DUALテーブルを最初のサブノードとして`UNION ALL`を実行するとエラーが発生する可能性がある問題を修正しました [#48755](https://github.com/pingcap/tidb/issues/48755) @[winoros](https://github.com/winoros)
    -   共通テーブル式（CTE）を含むクエリで、 `runtime error: index out of range [32] with length 32`小さな値に設定されている場合に`tidb_max_chunk_size`が報告される問題を修正 [#48808](https://github.com/pingcap/tidb/issues/48808) @[guo-shaoge](https://github.com/guo-shaoge)
    -   `AUTO_ID_CACHE=1`使用時のゴルーチンリークの問題を修正 [#46324](https://github.com/pingcap/tidb/issues/46324) @[tiancaiamao](https://github.com/tiancaiamao)
    -   MPP によって計算された`COUNT(INT)`の結果が正しくない可能性がある問題を修正 [#48643](https://github.com/pingcap/tidb/issues/48643) @[AilinKid](https://github.com/AilinKid)
    -   パーティション列のタイプが`ALTER TABLE ... LAST PARTITION`の場合に`DATETIME`の実行が失敗する問題を修正します [#48814](https://github.com/pingcap/tidb/issues/48814) @[crazycs520](https://github.com/crazycs520)
    -   `_`で`LIKE`ワイルドカードを使用すると、データに末尾の空白が含まれている場合にクエリ結果が正しくない可能性がある問題を修正します [#48983](https://github.com/pingcap/tidb/issues/48983) @[time-and-fate](https://github.com/time-and-fate)
    -   `tidb_server_memory_limit` による長期メモリ負荷が原因で TiDB の CPU 使用率が高くなる問題を修正しました。 [#48741](https://github.com/pingcap/tidb/issues/48741) @[XuHuaiyu](https://github.com/XuHuaiyu)
    -   `ENUM`型の列を結合キーとして使用した場合にクエリ結果が正しくない問題を修正 [#48991](https://github.com/pingcap/tidb/issues/48991) @[winoros](https://github.com/winoros)
    -   メモリ制限を超えると、CTE を含むクエリが予期せずスタックする問題を修正 [#49096](https://github.com/pingcap/tidb/issues/49096) @[AilinKid](https://github.com/AilinKid)
    -   TiDBサーバーが監査ログ用のEnterpriseプラグイン使用時に大量のリソースを消費する可能性がある問題を修正 [#49273](https://github.com/pingcap/tidb/issues/49273) @[lcwangchao](https://github.com/lcwangchao)
    -   特定のシナリオでオプティマイザーがTiFlash選択パスを DUAL テーブルに誤って変換する問題を修正 [#49285](https://github.com/pingcap/tidb/issues/49285) @[AilinKid](https://github.com/AilinKid)
    -   `UPDATE`または`DELETE`ステートメントに`WITH RECURSIVE` CTE が含まれている場合、誤った結果が生じる可能性がある問題を修正しました [#48969](https://github.com/pingcap/tidb/issues/48969) @[winoros](https://github.com/winoros)
    -   IndexHashJoin演算子を含むクエリがメモリ使用量`tidb_mem_quota_query`超えると停止する問題を修正しました [#49033](https://github.com/pingcap/tidb/issues/49033) @[XuHuaiyu](https://github.com/XuHuaiyu)
    -   非厳格モード ( `sql_mode = ''` ) で`INSERT`実行中に切り捨てが発生し、エラーが報告される問題を修正しました [#49369](https://github.com/pingcap/tidb/issues/49369) @[tiancaiamao](https://github.com/tiancaiamao)
    -   CTEクエリが再試行処理中にエラー`type assertion for CTEStorageMap failed`を報告する可能性がある問題を修正 [#46522](https://github.com/pingcap/tidb/issues/46522) @[tiancaiamao](https://github.com/tiancaiamao)
    -   `LIMIT`と`ORDER BY`がネストされた`UNION`クエリで無効になる可能性がある問題を修正 [#49377](https://github.com/pingcap/tidb/issues/49377) @[AilinKid](https://github.com/AilinKid)
    -   `ENUM`または`SET`型の無効な値を解析すると、SQL ステートメント エラーが直接発​​生する問題を修正しました [#49487](https://github.com/pingcap/tidb/issues/49487) @[winoros](https://github.com/winoros)
    -   Golangの暗黙的な型変換アルゴリズムが原因で統計構築時に発生する過剰な統計誤差の問題を修正 [#49801](https://github.com/pingcap/tidb/issues/49801) @[qw4990](https://github.com/qw4990)
    -   一部のタイムゾーンでサマータイムが正しく表示されない問題を修正 [#49586](https://github.com/pingcap/tidb/issues/49586) @[overvenus](https://github.com/overvenus)
    -   `AUTO_ID_CACHE=1`を含むテーブルが多数存在する場合に gRPC クライアントのリークを引き起こす可能性がある問題を修正しました [#48869](https://github.com/pingcap/tidb/issues/48869) @[tiancaiamao](https://github.com/tiancaiamao)
    -   TiDBサーバーが正常なシャットダウン中にpanic可能性がある問題を修正しました [#36793](https://github.com/pingcap/tidb/issues/36793) @[bb7133](https://github.com/bb7133)
    -   `ADMIN RECOVER INDEX`が`ERROR 1105`を報告する問題を、 `CommonHandle`を含むテーブルを処理する際に修正します。 [#47687](https://github.com/pingcap/tidb/issues/47687) @[Defined2014](https://github.com/Defined2014)
    -   `ALTER TABLE t PARTITION BY`を実行する際に配置ルールを指定すると`ERROR 8239`というエラーが報告される問題を修正しました。 [#48630](https://github.com/pingcap/tidb/issues/48630) @[mjonss](https://github.com/mjonss)
    -   `START_TIME`の`INFORMATION_SCHEMA.CLUSTER_INFO`列タイプが無効であるという問題を修正します [#45221](https://github.com/pingcap/tidb/issues/45221) @[dveeden](https://github.com/dveeden)
    -   `EXTRA`の列タイプが無効であるために`INFORMATION_SCHEMA.COLUMNS`エラー`Data Too Long, field len 30, data len 45`が発生する問題を修正しました。 [#42030](https://github.com/pingcap/tidb/issues/42030) @[tangenta](https://github.com/tangenta)
    -   `IN (...)`で`INFORMATION_SCHEMA.STATEMENTS_SUMMARY`で異なるプラン ダイジェストが発生する問題を修正 [#33559](https://github.com/pingcap/tidb/issues/33559) @[King-Dylan](https://github.com/King-Dylan)
    -   `TIME`型を`YEAR`型に変換する際に、返される結果に`TIME`と年が混在する問題を修正しました。 [#48557](https://github.com/pingcap/tidb/issues/48557) @[YangKeao](https://github.com/YangKeao)
    -   `tidb_enable_collect_execution_info`を無効にするとコプロセッサキャッシュがpanicを起こす問題を修正 [#48212](https://github.com/pingcap/tidb/issues/48212) @[you06](https://github.com/you06)
    -   `shuffleExec`が予期せず終了した際にTiDBがクラッシュする問題を修正 [#48230](https://github.com/pingcap/tidb/issues/48230) @[wshwsh12](https://github.com/wshwsh12)
    -   静的`CALIBRATE RESOURCE`が Prometheus データに依存している問題を修正 [#49174](https://github.com/pingcap/tidb/issues/49174) @[glorv](https://github.com/glorv)
    -   日付に大きな間隔を追加した際に、誤った結果が返される問題を修正しました。修正後、無効なプレフィックスまたは文字列`true`を含む間隔はゼロとして扱われ、MySQL 8.0 と整合性が取れます。 [#49227](https://github.com/pingcap/tidb/issues/49227) @[lcwangchao](https://github.com/lcwangchao)
    -   `ROW`関数が`null`型を誤って推論し、予期しないエラーが発生する問題を修正しました [#49015](https://github.com/pingcap/tidb/issues/49015) @[wshwsh12](https://github.com/wshwsh12)
    -   `ILIKE`関数が一部のシナリオでデータ競合を引き起こす可能性がある問題を修正しました [#49677](https://github.com/pingcap/tidb/issues/49677) @[lcwangchao](https://github.com/lcwangchao)
    -   `STREAM_AGG()` が CI を正しく処理しないためにクエリ結果が正しくない問題を修正します [#49902](https://github.com/pingcap/tidb/issues/49902) @[wshwsh12](https://github.com/wshwsh12)
    -   `TIME`への変換時にエンコードが失敗する問題を修正 [#47346](https://github.com/pingcap/tidb/issues/47346) @[wshwsh12](https://github.com/wshwsh12)
    -   `ENFORCED`制約内の`CHECK`オプションの動作がMySQL 8.0と矛盾する問題を修正しました。 [#47567](https://github.com/pingcap/tidb/issues/47567) [#47631](https://github.com/pingcap/tidb/issues/47631) @[jiyfhust](https://github.com/jiyfhust)
    -   `CHECK`制約を持つDDLステートメントが停止する問題を修正 [#47632](https://github.com/pingcap/tidb/issues/47632) @[jiyfhust](https://github.com/jiyfhust)
    -   メモリ不足が原因でDDLステートメントのインデックス追加が失敗する問題を修正 [#47862](https://github.com/pingcap/tidb/issues/47862) @[GMHDBJD](https://github.com/GMHDBJD)
    -   `ADD INDEX`の実行中にクラスターをアップグレードすると、データがインデックスと不整合になる可能性がある問題を修正しました [#46306](https://github.com/pingcap/tidb/issues/46306) @[zimulala](https://github.com/zimulala)
    -   `ADMIN CHECK`システム変数を更新した後に`tidb_mem_quota_query`を実行すると`ERROR 8175`が返される問題を修正 [#49258](https://github.com/pingcap/tidb/issues/49258) @[tangenta](https://github.com/tangenta)
    -   `ALTER TABLE`外部キーで参照される列の型を変更した際に、 `DECIMAL`の精度変更がエラーとして報告されない問題を修正しました。 [#49836](https://github.com/pingcap/tidb/issues/49836) @[yoshikipom](https://github.com/yoshikipom)
    -   `ALTER TABLE`外部キーで参照される列の型を変更する際に、 `INTEGER`の長さの変更が誤ってエラーとして報告される問題を修正しました。 [#47702](https://github.com/pingcap/tidb/issues/47702) @[yoshikipom](https://github.com/yoshikipom)
    -   一部のシナリオで式のインデックスが除数が0であることを検出しない問題を修正しました [#50053](https://github.com/pingcap/tidb/issues/50053) @[lcwangchao](https://github.com/lcwangchao)
    -   TiDBノードが多数のテーブルを処理する際にOOMエラーが発生する可能性がある問題を軽減する [#50077](https://github.com/pingcap/tidb/issues/50077) @[zimulala](https://github.com/zimulala)
    -   クラスターのローリング再起動中にDDLが実行状態のままになる問題を修正 [#50073](https://github.com/pingcap/tidb/issues/50073) @[tangenta](https://github.com/tangenta)
    -   `PointGet`または`BatchPointGet`を使用してパーティションテーブルのグローバルインデックスにアクセスした際に、結果が正しくない可能性がある問題を修正しました [#47539](https://github.com/pingcap/tidb/issues/47539) @[L-maple](https://github.com/L-maple)
    -   生成された列のインデックスが表示されるように設定されている場合、MPP プランが選択されない可能性がある問題を修正 [#47766](https://github.com/pingcap/tidb/issues/47766) @[AilinKid](https://github.com/AilinKid)
    -   `LIMIT`が`OR`型`Index Merge`にプッシュされない可能性がある [#48588](https://github.com/pingcap/tidb/issues/48588) @[AilinKid](https://github.com/AilinKid)
    -   BRインポート後に`mysql.bind_info`テーブルに重複した組み込み行が存在する可能性がある問題を修正します [#46527](https://github.com/pingcap/tidb/issues/46527) @[qw4990](https://github.com/qw4990)
    -   パーティションが削除された後、パーティションテーブルの統計情報が期待どおりに更新されない問題を修正 [#48182](https://github.com/pingcap/tidb/issues/48182) @[Rustin170506](https://github.com/Rustin170506)
    -   パーティションテーブルのグローバル統計情報の同時マージ中にエラーが返される可能性がある問題を修正 [#48713](https://github.com/pingcap/tidb/issues/48713) @[hawkingrei](https://github.com/hawkingrei)
    -   PADDING SPACE を持つ列のインデックス範囲スキャンに`LIKE`演算子が使用されている場合、クエリ結果が正しくないことがある問題を修正します [#48821](https://github.com/pingcap/tidb/issues/48821) @[time-and-fate](https://github.com/time-and-fate)
    -   生成された列がメモリ上で同時読み取りと書き込みを引き起こし、データ競合が発生する可能性がある問題を修正しました [#44919](https://github.com/pingcap/tidb/issues/44919) @[tangenta](https://github.com/tangenta)
    -   `ANALYZE TABLE` （トップN統計を収集しないことを示す）が指定されている場合でも、 `WITH 0 TOPN`がトップ1統計を収集してしまう問題を修正しました。 [#49080](https://github.com/pingcap/tidb/issues/49080) @[hawkingrei](https://github.com/hawkingrei)
    -   無効なオプティマイザヒントによって有効なヒントが無効になる可能性がある問題を修正 [#49308](https://github.com/pingcap/tidb/issues/49308) @[hawkingrei](https://github.com/hawkingrei)
    -   ハッシュパーティションテーブルの統計情報が、パーティションの追加、削除、再編成、または`TRUNCATE`を行った際に適切に更新されない問題を修正します。 [#48235](https://github.com/pingcap/tidb/issues/48235) [#48233](https://github.com/pingcap/tidb/issues/48233) [#48226](https://github.com/pingcap/tidb/issues/48226) [#48231](https://github.com/pingcap/tidb/issues/48231) @[Rustin170506](https://github.com/Rustin170506)
    -   自動統計更新の時間枠を設定した後でも、その時間枠外で統計が更新される可能性がある問題を修正しました [#49552](https://github.com/pingcap/tidb/issues/49552) @[hawkingrei](https://github.com/hawkingrei)
    -   パーティションテーブルを非パーティションテーブルに変換した際に、古い統計情報が自動的に削除されない問題を修正します [#49547](https://github.com/pingcap/tidb/issues/49547) @[Rustin170506](https://github.com/Rustin170506)
    -   `TRUNCATE TABLE`を使用してパーティションテーブルからデータをクリアしたときに、古い統計情報が自動的に削除されない問題を修正します [#49663](https://github.com/pingcap/tidb/issues/49663) @[Rustin170506](https://github.com/Rustin170506)
    -   クエリが強制ソートを行うオプティマイザヒント（ `STREAM_AGG()`など）を使用し、かつ実行プランに`IndexMerge`が含まれている場合に、強制ソートが無効になる可能性がある問題を修正します。 [#49605](https://github.com/pingcap/tidb/issues/49605) @[AilinKid](https://github.com/AilinKid)
    -   ヒストグラムの境界に`NULL`が含まれる場合、ヒストグラム統計が読み取り可能な文字列に解析されない可能性がある問題を修正 [#49823](https://github.com/pingcap/tidb/issues/49823) @[AilinKid](https://github.com/AilinKid)
    -   `GROUP_CONCAT(ORDER BY)`構文を含むクエリを実行するとエラーが返される可能性がある問題を修正 [#49986](https://github.com/pingcap/tidb/issues/49986) @[AilinKid](https://github.com/AilinKid)
    -   `UPDATE` 、 `DELETE` 、および`INSERT`ステートメントが、 `SQL_MODE`が厳密でない場合に警告ではなくオーバーフローエラーを返す問題を修正します [#49137](https://github.com/pingcap/tidb/issues/49137) @[YangKeao](https://github.com/YangKeao)
    -   テーブルに多値インデックスと非バイナリ型文字列で構成される複合インデックスがある場合にデータを挿入できない問題を修正 [#49680](https://github.com/pingcap/tidb/issues/49680) @[YangKeao](https://github.com/YangKeao)
    -   多階層にネストされた`LIMIT`クエリ内の`UNION`無効になる可能性がある問題を修正 [#49874](https://github.com/pingcap/tidb/issues/49874) @[Defined2014](https://github.com/Defined2014)
    -   `BETWEEN ... AND ...`条件を使用してパーティション テーブルをクエリすると誤った結果が返される問題を修正 [#49842](https://github.com/pingcap/tidb/issues/49842) @[Defined2014](https://github.com/Defined2014)
    -   `REPLACE INTO`ステートメントでヒントが使用できない問題を修正 [#34325](https://github.com/pingcap/tidb/issues/34325) @[YangKeao](https://github.com/YangKeao)
    -   ハッシュ パーティション テーブルのクエリ時に TiDB が間違ったパーティションを選択する可能性がある問題を修正 [#50044](https://github.com/pingcap/tidb/issues/50044) @[Defined2014](https://github.com/Defined2014)
    -   圧縮を有効にして MariaDB Connector/J を使用するときに発生する接続エラーを修正 [#49845](https://github.com/pingcap/tidb/issues/49845) @[onlyacat](https://github.com/onlyacat)

-   TiKV

    -   破損したSSTファイルが他のTiKVノードに拡散し、TiKVがpanic可能性がある問題を修正しました [#15986](https://github.com/tikv/tikv/issues/15986) @[Connor1996](https://github.com/Connor1996)
    -   オンラインの安全でない回復がマージ中止を処理できない問題を修正 [#15580](https://github.com/tikv/tikv/issues/15580) @[v01dstar](https://github.com/v01dstar)
    -   スケールアウト時に DR Auto-Sync のジョイント状態がタイムアウトする可能性がある問題を修正します [#15817](https://github.com/tikv/tikv/issues/15817) @[Connor1996](https://github.com/Connor1996)
    -   Titan の`blob-run-mode`オンラインで更新できない問題を修正 [#15978](https://github.com/tikv/tikv/issues/15978) @[tonyxuqqi](https://github.com/tonyxuqqi)
    -   解決済みTSが2時間ブロックされる可能性がある問題を修正[#11847](https://github.com/tikv/tikv/issues/11847) [#15520](https://github.com/tikv/tikv/issues/15520) [#39130](https://github.com/pingcap/tidb/issues/39130) @[overvenus](https://github.com/overvenus)
    -   `notLeader`または`regionNotFound`に遭遇した際に Flashback が停止する可能性がある問題を修正しました [#15712](https://github.com/tikv/tikv/issues/15712) @[HuSharp](https://github.com/HuSharp)
    -   TiKV の実行が非常に遅い場合、リージョンのマージ後にpanicする可能性がある問題を修正 [#16111](https://github.com/tikv/tikv/issues/16111) @[overvenus](https://github.com/overvenus)
    -   TiKVがGCが期限切れロックをスキャンする際にメモリ内の悲観的ロックを読み取れない問題を修正 [#15066](https://github.com/tikv/tikv/issues/15066) @[cfzjywxk](https://github.com/cfzjywxk)
    -   Titanモニタリングにおけるブロブファイルサイズが正しくない問題を修正 [#15971](https://github.com/tikv/tikv/issues/15971) @[Connor1996](https://github.com/Connor1996)
    -   TiCDC を使用して大きなテーブルをレプリケートすると TiKV が OOM になる可能性がある問題を修正 [#16035](https://github.com/tikv/tikv/issues/16035) @[overvenus](https://github.com/overvenus)
    -   TiDBとTiKVが`DECIMAL`算術乗算の切り捨て処理時に一貫性のない結果を生成する可能性がある問題を修正 [#16268](https://github.com/tikv/tikv/issues/16268) @[solotzg](https://github.com/solotzg)
    -   `cast_duration_as_time`が誤った結果を返す可能性がある問題を修正 [#16211](https://github.com/tikv/tikv/issues/16211) @[gengliqi](https://github.com/gengliqi)
    -   TiKV がブラジルとエジプトのタイムゾーンを誤って変換する問題を修正 [#16220](https://github.com/tikv/tikv/issues/16220) @[overvenus](https://github.com/overvenus)
    -   gRPCスレッドが`is_shutdown`をチェックしているときにTiKVがpanic可能性がある問題を修正 [#16236](https://github.com/tikv/tikv/issues/16236) @[pingyu](https://github.com/pingyu)

-   PD

    -   PD の etcd ヘルスチェックで期限切れのアドレスが削除されない問題を修正 [#7226](https://github.com/tikv/pd/issues/7226) @[iosmanthus](https://github.com/iosmanthus)
    -   PDリーダーが転送され、新しいリーダーとPDクライアントの間にネットワーク分断が発生した場合、PDクライアントがリーダー情報を更新できない問題を修正しました [#7416](https://github.com/tikv/pd/issues/7416) @[CabinfeverB](https://github.com/CabinfeverB)
    -   Gin Web Frameworkのバージョンをv1.8.1からv1.9.1にアップグレードすることで、いくつかのセキュリティ問題を修正しました。 [#7438](https://github.com/tikv/pd/issues/7438) @[niubell](https://github.com/niubell)
    -   レプリカ数が要件を満たさない場合に孤立ピアが削除される問題を修正 [#7584](https://github.com/tikv/pd/issues/7584) @[bufferflies](https://github.com/bufferflies)

-   TiFlash

    -   TiFlashがクエリ中にメモリ制限に遭遇した際のメモリリークの問題を修正 [#8447](https://github.com/pingcap/tiflash/issues/8447) @[JinheLin](https://github.com/JinheLin)
    -   `FLASHBACK DATABASE`を実行後もTiFlashレプリカのデータがガベージコレクションされてしまう問題を修正 [#8450](https://github.com/pingcap/tiflash/issues/8450) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   クエリの遅延によりメモリ使用量が大幅に増加する問題を修正 [#8564](https://github.com/pingcap/tiflash/issues/8564) @[JinheLin](https://github.com/JinheLin)
    -   `RECOVER TABLE`および`FLASHBACK TABLE`TiFlash`CREATE TABLE` `DROP TABLE`を介して一部の TiFlash レプリカデータを復元できない問題 [#1664](https://github.com/pingcap/tiflash/issues/1664) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   `ColumnRef in (Literal, Func...)`のようなフィルタリング条件を指定してクエリを実行すると、クエリ結果が正しくなくなる問題を修正 [#8631](https://github.com/pingcap/tiflash/issues/8631) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   DDL の同時実行中にTiFlash で競合が発生した場合のTiFlash panic問題を修正 [#8578](https://github.com/pingcap/tiflash/issues/8578) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   TiFlash が非集約ストレージおよびコンピューティングアーキテクチャの下でオブジェクトストレージデータの GC 所有者を選択できない場合がある問題を修正 [#8519](https://github.com/pingcap/tiflash/issues/8519) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   `lowerUTF8`および`upperUTF8`関数で、大文字と小文字が異なるバイトを占有することを許可しない問題を修正 [#8484](https://github.com/pingcap/tiflash/issues/8484) @[gengliqi](https://github.com/gengliqi)
    -   TiFlashが`ENUM`の値が0の場合に`ENUM`を正しく処理しない問題を修正 [#8311](https://github.com/pingcap/tiflash/issues/8311) @[solotzg](https://github.com/solotzg)
    -   `INET_NTOA()`式の互換性の問題を修正 [#8211](https://github.com/pingcap/tiflash/issues/8211) @[solotzg](https://github.com/solotzg)
    -   ストリーム読み取り中に複数のパーティションテーブルをスキャンする際に発生する可能性のあるメモリ不足（OOM）問題を修正 [#8505](https://github.com/pingcap/tiflash/issues/8505) @[gengliqi](https://github.com/gengliqi)
    -   短いクエリを実行すると過剰な情報ログが正常に出力される問題を修正 [#8592](https://github.com/pingcap/tiflash/issues/8592) @[windtalker](https://github.com/windtalker)
    -   TiFlashが停止時にクラッシュする可能性がある問題を修正 [#8550](https://github.com/pingcap/tiflash/issues/8550) @[guo-shaoge](https://github.com/guo-shaoge)
    -   定数文字列パラメーターを含む`GREATEST`または`LEAST`関数で発生する可能性のあるランダムな無効なメモリアクセスの問題を修正します [#8604](https://github.com/pingcap/tiflash/issues/8604) @[windtalker](https://github.com/windtalker)

-   ツール

    -   Backup & Restore (BR)

        -   BRが外部ストレージファイルに対して不正なURIを生成する問題を修正 [#48452](https://github.com/pingcap/tidb/issues/48452) @[3AceShowHand](https://github.com/3AceShowHand)
        -   ログバックアップタスクは開始できるものの、タスク初期化中にPDへの接続に失敗すると正しく動作しない問題を修正 [#16056](https://github.com/tikv/tikv/issues/16056) @[YuJuncen](https://github.com/YuJuncen)
        -   ログバックアップタスクが起動後にメモリリークを起こして正常に実行されない可能性がある問題を修正 [#16070](https://github.com/tikv/tikv/issues/16070) @[YuJuncen](https://github.com/YuJuncen)
        -   PITR 処理中にシステムテーブル`mysql.gc_delete_range`にデータを挿入するとエラーが返される問題を修正しました。 [#49346](https://github.com/pingcap/tidb/issues/49346) @[Leavrth](https://github.com/Leavrth)
        -   古いバージョンのバックアップからデータを復元すると、 `Unsupported collation`エラーが報告される問題を修正 [#49466](https://github.com/pingcap/tidb/issues/49466) @[3pointer](https://github.com/3pointer)
        -   特定のシナリオでスナップショットを介してユーザーテーブルが復元された後、権限がタイムリーに更新されない問題を修正 [#49394](https://github.com/pingcap/tidb/issues/49394) @[Leavrth](https://github.com/Leavrth)

    -   TiCDC

        -   `WHERE`句が、特定のシナリオで`DELETE`ステートメントを複製する際に主キーを条件として使用しない問題を修正しました [#9812](https://github.com/pingcap/tiflow/issues/9812) @[asddongmen](https://github.com/asddongmen)
        -   TiCDCサーバーがオブジェクトストレージサービスへのデータ複製時にpanic可能性がある問題を修正しました [#10137](https://github.com/pingcap/tiflow/issues/10137) @[sdojjy](https://github.com/sdojjy)
        -   `kv-client`の初期化中の潜在的なデータ競合の問題を修正 [#10095](https://github.com/pingcap/tiflow/issues/10095) @[3AceShowHand](https://github.com/3AceShowHand)
        -   TiCDCが特定の特殊なシナリオで誤ってTiKVとの接続を閉じる問題を修正 [#10239](https://github.com/pingcap/tiflow/issues/10239) @[hicqu](https://github.com/hicqu)
        -   TiCDCサーバーが損失のあるDDLステートメントを実行する際にpanic可能性がある問題を修正しました（アップストリーム [#9739](https://github.com/pingcap/tiflow/issues/9739) @[hicqu](https://github.com/hicqu)
        -   TiCDCがデータを下流のMySQLに複製する際に`checkpoint-ts`が停止する可能性がある問題を修正しました [#10334](https://github.com/pingcap/tiflow/issues/10334) @[zhangjinpeng87](https://github.com/zhangjinpeng87)

    -   TiDB Data Migration (DM)

        -   DM で「イベント タイプ truncate が無効です」というエラーが発生し、アップグレードが失敗する問題を修正します [#10282](https://github.com/pingcap/tiflow/issues/10282) @[GMHDBJD](https://github.com/GMHDBJD)
        -   GTID モードでデータをレプリケートする際のパフォーマンス低下の問題を修正 [#9676](https://github.com/pingcap/tiflow/issues/9676) @[feran-morgan-pingcap](https://github.com/feran-morgan-pingcap)
        -   下流テーブル構造に`shard_row_id_bits`が含まれている場合にマイグレーションタスクエラーが発生する問題を修正 [#10308](https://github.com/pingcap/tiflow/issues/10308) @[GMHDBJD](https://github.com/GMHDBJD)

## 貢献者 {#contributors}

TiDBコミュニティの以下の貢献者の皆様に感謝申し上げます。

-   [0o001](https://github.com/0o001) (初回貢献者)
-   [bagechengzi](https://github.com/bagechengzi) (初回貢献者)
-   [feran-morgan-pingcap](https://github.com/feran-morgan-pingcap) (初回貢献者)
-   [highpon](https://github.com/highpon)
-   [jiyfhust](https://github.com/jiyfhust)
-   [L-maple](https://github.com/L-maple)
-   [lkshminarayanan](https://github.com/lkshminarayanan) (初回貢献者)
-   [lyang24](https://github.com/lyang24) (初回貢献者)
-   [mittalrishabh](https://github.com/mittalrishabh)
-   [morgo](https://github.com/morgo)
-   [nkg-](https://github.com/nkg-) (初回貢献者)
-   [onlyacat](https://github.com/onlyacat)
-   [shawn0915](https://github.com/shawn0915)
-   [Smityz](https://github.com/Smityz)
-   [szpnygo](https://github.com/szpnygo) (初回貢献者)
-   [ub-3](https://github.com/ub-3) (初回貢献者)
-   [xiaoyawei](https://github.com/xiaoyawei) (初回貢献者)
-   [yorkhellen](https://github.com/yorkhellen)
-   [yoshikipom](https://github.com/yoshikipom) (初回貢献者)
-   [Zheaoli](https://github.com/Zheaoli)
