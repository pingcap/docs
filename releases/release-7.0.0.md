---
title: TiDB 7.0.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 7.0.0.
---

# TiDB 7.0.0 リリースノート {#tidb-7-0-0-release-notes}

発売日：2023年3月30日

TiDB バージョン: [<a href="/releases/versioning.md#development-milestone-releases">DMR</a>](/releases/versioning.md#development-milestone-releases)

クイックアクセス: [<a href="https://docs.pingcap.com/tidb/v7.0/quick-start-with-tidb">クイックスタート</a>](https://docs.pingcap.com/tidb/v7.0/quick-start-with-tidb) | [<a href="https://www.pingcap.com/download/?version=v7.0.0#version-list">インストールパッケージ</a>](https://www.pingcap.com/download/?version=v7.0.0#version-list)

v7.0.0-DMR の主な新機能と改善点は次のとおりです。

<table><thead><tr><th>カテゴリー</th><th>特徴</th><th>説明</th></tr></thead><tbody><tr><td rowspan="2">スケーラビリティとパフォーマンス<br/></td><td>セッションレベル<a href="https://docs.pingcap.com/tidb/v7.0/sql-non-prepared-plan-cache" target="_blank">の未準備SQLプランキャッシュ</a>(実験的)</td><td>事前に準備ステートメントを手動で設定しなくても、セッション レベルでプラン キャッシュの自動的な再利用をサポートし、コンパイルを削減し、同じ SQL パターンのクエリ時間を短縮します。</td></tr><tr><td> TiFlash は、<a href="https://docs.pingcap.com/tidb/v7.0/tiflash-disaggregated-and-s3" target="_blank">分散storageとコンピューティングアーキテクチャ、および S3 共有storage</a>(実験的) をサポートしています。</td><td> TiFlash は、オプションとしてクラウドネイティブアーキテクチャを導入しています。<ul><li> TiFlash のコンピューティングとstorageを分割します。これは、Elastic HTAP リソース使用率のマイルストーンです。</li><li>低コストで共有storageを提供できる S3 ベースのstorageエンジンを導入します。</li></ul></td></tr><tr><td rowspan="2">信頼性と可用性<br/></td><td><a href="https://docs.pingcap.com/tidb/v7.0/tidb-resource-control" target="_blank">リソース制御の強化</a>(実験的)</td><td>リソース グループを使用して、1 つのクラスター内のさまざまなアプリケーションまたはワークロードにリソースを割り当て、分離することをサポートします。このリリースでは、TiDB にさまざまなリソース バインディング モード (ユーザー、セッション、ステートメント レベル) とユーザー定義の優先順位のサポートが追加されています。また、コマンドを使用してリソースキャリブレーション（リソース全体量の見積り）を行うこともできます。</td></tr><tr><td> TiFlash は<a href="https://docs.pingcap.com/tidb/v7.0/tiflash-spill-disk" target="_blank">ディスクへのスピルを</a>サポートします</td><td>TiFlash は、集計、ソート、ハッシュ結合などのデータ集約型操作における OOM を軽減するために、中間結果のディスクへのスピルをサポートしています。</td></tr><tr><td rowspan="2"> SQL</td><td><a href="https://docs.pingcap.com/tidb/v7.0/time-to-live" target="_blank">行レベル TTL</a> (GA)</td><td>データベース サイズの管理をサポートし、一定の期間を経過したデータを自動的に期限切れにすることでパフォーマンスを向上させます。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v7.0/partitioned-table#reorganize-partitions" target="_blank"><code>LIST</code> / <code>RANGE</code>パーティションを再編成する</a></td><td><code>REORGANIZE PARTITION</code>ステートメントを使用すると、隣接するパーティションを結合したり、1 つのパーティションを複数のパーティションに分割したりすることができ、これによりパーティション テーブルの使いやすさが向上します。</td></tr><tr><td rowspan="2"> DB の操作と可観測性<br/></td><td>TiDB は<a href="https://docs.pingcap.com/tidb/v7.0/sql-statement-load-data" target="_blank"><code>LOAD DATA</code>ステートメント</a>の機能を強化します (実験的)</td><td> TiDB は、S3/GCS からのデータ インポートのサポートなど、 <code>LOAD DATA</code> SQL ステートメントの機能を強化します。<br/></td></tr><tr><td> TiCDC は<a href="https://docs.pingcap.com/tidb/v7.0/ticdc-sink-to-cloud-storage" target="_blank">オブジェクトstorageシンク</a>(GA) をサポートします</td><td>TiCDC は、Amazon S3、GCS、Azure Blob Storage、NFS などのオブジェクトstorageサービスへの行変更イベントのレプリケートをサポートしています。<br/></td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### スケーラビリティ {#scalability}

-   TiFlash は、分散storageとコンピューティングアーキテクチャをサポートし、このアーキテクチャでのオブジェクトstorageをサポートします (実験的) [<a href="https://github.com/pingcap/tiflash/issues/6882">#6882</a>](https://github.com/pingcap/tiflash/issues/6882) @ [<a href="https://github.com/flowbehappy">フロービハッピー</a>](https://github.com/flowbehappy)

    v7.0.0 より前では、 TiFlash は結合されたstorageとコンピューティングアーキテクチャのみをサポートしていました。このアーキテクチャでは、各TiFlashノードはstorageとコンピューティング ノードの両方として機能し、そのコンピューティング機能とstorage機能を個別に拡張することはできません。さらに、 TiFlashノードはローカルstorageのみを使用できます。

    v7.0.0 以降、 TiFlash は、分散storageとコンピューティングアーキテクチャもサポートします。このアーキテクチャでは、 TiFlashノードは 2 つのタイプ (コンピューティング ノードと書き込みノード) に分けられ、S3 API と互換性のあるオブジェクトstorageをサポートします。どちらのタイプのノードも、コンピューティング容量またはstorage容量に合わせて個別にスケーリングできます。**分離されたstorageとコンピューティングアーキテクチャ**と、**結合されたstorageとコンピューティングアーキテクチャを**同じクラスター内で使用したり、相互に変換したりすることはできません。 TiFlash を展開するときに使用するアーキテクチャを構成できます。

    詳細については、 [<a href="/tiflash/tiflash-disaggregated-and-s3.md">ドキュメンテーション</a>](/tiflash/tiflash-disaggregated-and-s3.md)を参照してください。

### パフォーマンス {#performance}

-   Fast Online DDL と PITR [<a href="https://github.com/pingcap/tidb/issues/38045">#38045</a>](https://github.com/pingcap/tidb/issues/38045) @ [<a href="https://github.com/Leavrth">レヴルス</a>](https://github.com/Leavrth)の間の互換性を実現

    TiDB v6.5.0 では、 [<a href="/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630">高速オンライン DDL</a>](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) [<a href="/br/backup-and-restore-overview.md">PITR</a>](/br/backup-and-restore-overview.md)と完全な互換性がありません。完全なデータ バックアップを確実に行うには、まず PITR バックグラウンド バックアップ タスクを停止し、Fast Online DDL を使用してインデックスをすぐに追加してから、PITR バックアップ タスクを再開することをお勧めします。

    TiDB v7.0.0 以降、Fast Online DDL と PITR は完全に互換性があります。 PITR を介してクラスター データを復元する場合、互換性を確保するために、ログ バックアップ中に Fast Online DDL を介して追加されたインデックス操作が自動的に再生されます。

    詳細については、 [<a href="/ddl-introduction.md">ドキュメンテーション</a>](/ddl-introduction.md)を参照してください。

-   TiFlash は、ヌル対応セミ結合演算子およびヌル対応アンチセミ結合演算子[<a href="https://github.com/pingcap/tiflash/issues/6674">#6674</a>](https://github.com/pingcap/tiflash/issues/6674) @ [<a href="https://github.com/gengliqi">ゲンリチ</a>](https://github.com/gengliqi)をサポートします。

    相関サブクエリで`IN` 、 `NOT IN` 、 `= ANY` 、または`!= ALL`演算子を使用する場合、TiDB はそれらをセミ結合またはアンチセミ結合に変換することでコンピューティング パフォーマンスを最適化します。結合キー列が`NULL`である可能性がある場合は、 [<a href="/explain-subqueries.md#null-aware-semi-join-in-and--any-subqueries">Null 認識セミ結合</a>](/explain-subqueries.md#null-aware-semi-join-in-and--any-subqueries)や[<a href="/explain-subqueries.md#null-aware-anti-semi-join-not-in-and--all-subqueries">Null を認識するアンチセミ結合</a>](/explain-subqueries.md#null-aware-anti-semi-join-not-in-and--all-subqueries)などの null 対応結合アルゴリズムが必要です。

    v7.0.0 より前のTiFlash は、null 対応セミ結合演算子および null 対応アンチセミ結合演算子をサポートしていないため、これらのサブクエリがTiFlashに直接プッシュダウンされません。 v7.0.0 以降、 TiFlash はnull 対応セミ結合演算子と null 対応アンチセミ結合演算子をサポートします。 SQL ステートメントにこれらの相関サブクエリが含まれており、クエリ内のテーブルにTiFlashレプリカがあり、 [<a href="/tiflash/use-tiflash-mpp-mode.md">MPPモード</a>](/tiflash/use-tiflash-mpp-mode.md)有効になっている場合、オプティマイザは、全体のパフォーマンスを向上させるために null 対応セミ結合演算子と null 対応アンチ セミ結合演算子をTiFlashにプッシュダウンするかどうかを自動的に決定します。 。

    詳細については、 [<a href="/tiflash/tiflash-supported-pushdown-calculations.md">ドキュメンテーション</a>](/tiflash/tiflash-supported-pushdown-calculations.md)を参照してください。

-   TiFlash はFastScan (GA) [<a href="https://github.com/pingcap/tiflash/issues/5252">#5252</a>](https://github.com/pingcap/tiflash/issues/5252) @ [<a href="https://github.com/hongyunyan">ホンユニャン</a>](https://github.com/hongyunyan)の使用をサポートします

    v6.3.0 以降、 TiFlash は実験的機能として FastScan を導入します。 v7.0.0 では、この機能が一般利用可能になります。システム変数[<a href="/system-variables.md#tiflash_fastscan-new-in-v630">`tiflash_fastscan`</a>](/system-variables.md#tiflash_fastscan-new-in-v630)を使用して FastScan を有効にできます。この機能は、強力な一貫性を犠牲にすることで、テーブル スキャンのパフォーマンスを大幅に向上させます。対応するテーブルに`UPDATE` `DELETE`が含まれず、 `INSERT`操作のみが含まれる場合、FastScan は強い一貫性を維持し、スキャン パフォーマンスを向上させることができます。

    詳細については、 [<a href="/tiflash/use-fastscan.md">ドキュメンテーション</a>](/tiflash/use-fastscan.md)を参照してください。

-   TiFlash は後期実体化 (実験的) [<a href="https://github.com/pingcap/tiflash/issues/5829">#5829</a>](https://github.com/pingcap/tiflash/issues/5829) @ [<a href="https://github.com/Lloyd-Pottiger">ロイド・ポティガー</a>](https://github.com/Lloyd-Pottiger)をサポートします

    フィルタ条件 ( `WHERE`句) を使用して`SELECT`ステートメントを処理する場合、 TiFlash はデフォルトでクエリに必要な列からすべてのデータを読み取り、クエリ条件に基づいてデータをフィルタリングして集計します。遅延具体化は、フィルター条件の一部を TableScan オペレーターにプッシュダウンすることをサポートする最適化方法です。つまり、 TiFlash は、最初に押し下げられたフィルター条件に関連する列データをスキャンし、条件を満たす行をフィルターし、次にこれらの行の他の列データをスキャンしてさらなる計算を行うことで、IO スキャンとデータ処理の計算を削減します。 。

    TiFlash遅延マテリアライゼーション機能は、デフォルトでは有効になっていません。これを有効にするには、システム変数`tidb_opt_enable_late_materialization`を`OFF`に設定します。この機能が有効になると、TiDB オプティマイザーは統計とフィルター条件に基づいてどのフィルター条件をプッシュダウンするかを決定します。

    詳細については、 [<a href="/tiflash/tiflash-late-materialization.md">ドキュメンテーション</a>](/tiflash/tiflash-late-materialization.md)を参照してください。

-   準備されていないステートメントの実行プランのキャッシュをサポート (実験的) [<a href="https://github.com/pingcap/tidb/issues/36598">#36598</a>](https://github.com/pingcap/tidb/issues/36598) @ [<a href="https://github.com/qw4990">qw4990</a>](https://github.com/qw4990)

    実行プラン キャッシュは、同時 OLTP の負荷容量を向上させるために重要であり、TiDB はすでに[<a href="/sql-prepared-plan-cache.md">準備された実行プランのキャッシュ</a>](/sql-prepared-plan-cache.md)をサポートしています。 v7.0.0 では、TiDB は非 Prepare ステートメントの実行プランをキャッシュすることもできるため、実行プラン キャッシュの範囲が拡張され、TiDB の同時処理能力が向上します。

    この機能はデフォルトでは無効になっています。システム変数[<a href="/system-variables.md#tidb_enable_non_prepared_plan_cache">`tidb_enable_non_prepared_plan_cache`</a>](/system-variables.md#tidb_enable_non_prepared_plan_cache) ～ `ON`を設定することで有効にできます。安定性の理由から、TiDB v7.0.0 では、準備されていない実行プランをキャッシュするための新しい領域が割り当てられ、システム変数[<a href="/system-variables.md#tidb_non_prepared_plan_cache_size">`tidb_non_prepared_plan_cache_size`</a>](/system-variables.md#tidb_non_prepared_plan_cache_size)を使用してキャッシュ サイズを設定できます。さらに、この機能には SQL ステートメントに関する特定の制限があります。詳細については、 [<a href="/sql-non-prepared-plan-cache.md#restrictions">制限</a>](/sql-non-prepared-plan-cache.md#restrictions)を参照してください。

    詳細については、 [<a href="/sql-non-prepared-plan-cache.md">ドキュメンテーション</a>](/sql-non-prepared-plan-cache.md)を参照してください。

-   TiDB は、サブクエリ[<a href="https://github.com/pingcap/tidb/issues/40219">#40219</a>](https://github.com/pingcap/tidb/issues/40219) @ [<a href="https://github.com/fzzf678">fzzf678</a>](https://github.com/fzzf678)の実行プラン キャッシュ制約を削除します。

    TiDB v7.0.0 では、サブクエリの実行プラン キャッシュ制約が削除されます。これは、サブクエリを含む SQL ステートメントの実行プラン`SELECT * FROM t WHERE a > (SELECT ...)`など) をキャッシュできるようになったということです。この機能により、実行プラン キャッシュの適用範囲がさらに拡張され、SQL クエリの実行効率が向上します。

    詳細については、 [<a href="/sql-prepared-plan-cache.md">ドキュメンテーション</a>](/sql-prepared-plan-cache.md)を参照してください。

-   TiKV は、ログのリサイクルのための空のログ ファイルの自動生成をサポートしています[<a href="https://github.com/tikv/tikv/issues/14371">#14371</a>](https://github.com/tikv/tikv/issues/14371) @ [<a href="https://github.com/LykxSassinator">リククスサシネーター</a>](https://github.com/LykxSassinator)

    v6.3.0 では、TiKV は書き込み負荷によって引き起こされるロングテールレイテンシーを削減する機能[<a href="/tikv-configuration-file.md#enable-log-recycle-new-in-v630">Raftのリサイクル</a>](/tikv-configuration-file.md#enable-log-recycle-new-in-v630)を導入しました。ただし、ログのリサイクルはRaftログ ファイルの数が特定のしきい値に達した場合にのみ有効になるため、ユーザーがこの機能によってもたらされるスループットの向上を直接体験するのは困難です。

    v7.0.0 では、ユーザー エクスペリエンスを向上させるために、 `raft-engine.prefill-for-recycle`と呼ばれる新しい構成項目が導入されました。この項目は、プロセスの開始時にリサイクルのために空のログ ファイルを生成するかどうかを制御します。この構成を有効にすると、TiKV は初期化中に空のログ ファイルのバッチを自動的に埋め、初期化直後にログのリサイクルが確実に有効になります。

    詳細については、 [<a href="/tikv-configuration-file.md#prefill-for-recycle-new-in-v700">ドキュメンテーション</a>](/tikv-configuration-file.md#prefill-for-recycle-new-in-v700)を参照してください。

-   ウィンドウ関数のパフォーマンスを向上させるために、TopN または Limit 演算子を[<a href="/functions-and-operators/expressions-pushed-down.md">ウィンドウ関数</a>](/functions-and-operators/expressions-pushed-down.md)から導出するサポート[<a href="https://github.com/tikv/tikv/issues/13936">#13936</a>](https://github.com/tikv/tikv/issues/13936) @ [<a href="https://github.com/windtalker">ウィンドトーカー</a>](https://github.com/windtalker)

    この機能はデフォルトでは無効になっています。これを有効にするには、セッション変数[<a href="/system-variables.md#tidb_opt_derive_topn-new-in-v700">tidb_opt_derive_topn</a>](/system-variables.md#tidb_opt_derive_topn-new-in-v700) ～ `ON`を設定します。

    詳細については、 [<a href="/derive-topn-from-window.md">ドキュメンテーション</a>](/derive-topn-from-window.md)を参照してください。

-   Fast Online DDL [<a href="https://github.com/pingcap/tidb/issues/40730">#40730</a>](https://github.com/pingcap/tidb/issues/40730) @ [<a href="https://github.com/tangenta">タンジェンタ</a>](https://github.com/tangenta)による一意のインデックスの作成をサポート

    TiDB v6.5.0 は、Fast Online DDL を介した通常のセカンダリ インデックスの作成をサポートしています。 TiDB v7.0.0 は、Fast Online DDL を介した一意のインデックスの作成をサポートしています。 v6.1.0 と比較して、大きなテーブルへの一意のインデックスの追加は数倍高速になり、パフォーマンスが向上すると予想されます。

    詳細については、 [<a href="/ddl-introduction.md">ドキュメンテーション</a>](/ddl-introduction.md)を参照してください。

### 信頼性 {#reliability}

-   リソース制御機能の強化 (実験的) [<a href="https://github.com/pingcap/tidb/issues/38825">#38825</a>](https://github.com/pingcap/tidb/issues/38825) @ [<a href="https://github.com/nolouch">ノールーシュ</a>](https://github.com/nolouch) @ [<a href="https://github.com/BornChanger">ボーンチェンジャー</a>](https://github.com/BornChanger) @ [<a href="https://github.com/glorv">グロルフ</a>](https://github.com/glorv) @ [<a href="https://github.com/tiancaiamao">ティエンチャイアマオ</a>](https://github.com/tiancaiamao) @ [<a href="https://github.com/Connor1996">コナー1996</a>](https://github.com/Connor1996) @ [<a href="https://github.com/JmPotato">Jmポテト</a>](https://github.com/JmPotato) @ [<a href="https://github.com/hnes">フネス</a>](https://github.com/hnes) @ [<a href="https://github.com/CabinfeverB">キャビンフィーバーB</a>](https://github.com/CabinfeverB) @ [<a href="https://github.com/HuSharp">ヒューシャープ</a>](https://github.com/HuSharp)

    TiDB は、リソース グループに基づいたリソース制御機能を強化します。この機能により、TiDB クラスターのリソース利用効率とパフォーマンスが大幅に向上します。リソース制御機能の導入は、TiDB にとってマイルストーンです。分散データベース クラスターを複数の論理ユニットに分割し、さまざまなデータベース ユーザーを対応するリソース グループにマップし、必要に応じて各リソース グループのクォータを設定できます。クラスターのリソースが制限されている場合、同じリソース グループ内のセッションで使用されるすべてのリソースはクォータ内に制限されます。これにより、リソース グループが過剰に消費されても、他のリソース グループのセッションは影響を受けません。

    この機能を使用すると、異なるシステムからの複数の中小規模のアプリケーションを単一の TiDB クラスターに結合できます。アプリケーションのワークロードが大きくなっても、他のアプリケーションの通常の動作には影響しません。システムのワークロードが低い場合は、設定されたクォータを超えている場合でも、ビジー状態のアプリケーションに必要なシステム リソースを割り当てることができ、リソースを最大限に活用することができます。さらに、リソース制御機能を合理的に使用することで、クラスタ数を削減し、運用保守の困難を軽減し、管理コストを節約できます。

    この機能は、Grafana でのリソースの実際の使用状況を示す組み込みのリソース制御ダッシュボードを提供し、リソースをより合理的に割り当てるのに役立ちます。また、セッション レベルとステートメント レベル (ヒント) の両方に基づいた動的なリソース管理機能もサポートします。この機能の導入により、TiDB クラスターのリソース使用量をより正確に制御し、実際のニーズに基づいてクォータを動的に調整できるようになります。

    TiDB v7.0.0 では、リソース グループに絶対スケジュール優先度 ( `PRIORITY` ) を設定して、重要なサービスがリソースを確実に取得できるようにすることができます。また、リソース グループの設定方法も拡張されます。

    リソース グループは次の方法で使用できます。

    -   ユーザーレベル。 [<a href="/sql-statements/sql-statement-create-user.md">`CREATE USER`</a>](/sql-statements/sql-statement-create-user.md)または[<a href="/sql-statements/sql-statement-alter-user.md">`ALTER USER`</a>](/sql-statements/sql-statement-alter-user.md)ステートメントを使用してユーザーを特定のリソース グループにバインドします。リソース グループをユーザーにバインドすると、ユーザーが新しく作成したセッションは、対応するリソース グループに自動的にバインドされます。
    -   セッションレベル。現在のセッションで使用されるリソース グループを[<a href="/sql-statements/sql-statement-set-resource-group.md">`SET RESOURCE GROUP`</a>](/sql-statements/sql-statement-set-resource-group.md)で設定します。
    -   発言レベル。現在のステートメントで使用されるリソース グループを[<a href="/optimizer-hints.md#resource_groupresource_group_name">`RESOURCE_GROUP()`</a>](/optimizer-hints.md#resource_groupresource_group_name)で設定します。

    詳細については、 [<a href="/tidb-resource-control.md">ドキュメンテーション</a>](/tidb-resource-control.md)を参照してください。

-   Fast Online DDL のチェックポイント メカニズムをサポートし、フォールト トレランスと自動回復機能を向上させます[<a href="https://github.com/pingcap/tidb/issues/42164">#42164</a>](https://github.com/pingcap/tidb/issues/42164) @ [<a href="https://github.com/tangenta">タンジェンタ</a>](https://github.com/tangenta)

    TiDB v7.0.0 では、 [<a href="/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630">高速オンライン DDL</a>](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)のチェックポイント メカニズムが導入されており、フォールト トレランスと自動回復機能が大幅に向上しています。 DDL の進行状況を定期的に記録して同期することにより、TiDB DDL 所有者の障害や切り替えが発生した場合でも、進行中の DDL 操作を高速オンライン DDL モードで実行し続けることができます。これにより、DDL の実行がより安定して効率的になります。

    詳細については、 [<a href="/ddl-introduction.md">ドキュメンテーション</a>](/ddl-introduction.md)を参照してください。

-   TiFlash はディスク[<a href="https://github.com/pingcap/tiflash/issues/6528">#6528</a>](https://github.com/pingcap/tiflash/issues/6528) @ [<a href="https://github.com/windtalker">ウィンドトーカー</a>](https://github.com/windtalker)へのスピルをサポートします

    実行パフォーマンスを向上させるために、 TiFlash は可能な限りデータ全体をメモリ内で実行します。データ量がメモリの合計サイズを超えると、 TiFlash はメモリ不足によるシステム クラッシュを避けるためにクエリを終了します。したがって、 TiFlashが処理できるデータ量は、利用可能なメモリによって制限されます。

    v7.0.0 以降、 TiFlash はディスクへのスピルをサポートします。オペレーター ( [<a href="/system-variables.md#tidb_max_bytes_before_tiflash_external_group_by-new-in-v700">`tidb_max_bytes_before_tiflash_external_group_by`</a>](/system-variables.md#tidb_max_bytes_before_tiflash_external_group_by-new-in-v700) 、 [<a href="/system-variables.md#tidb_max_bytes_before_tiflash_external_sort-new-in-v700">`tidb_max_bytes_before_tiflash_external_sort`</a>](/system-variables.md#tidb_max_bytes_before_tiflash_external_sort-new-in-v700) 、および[<a href="/system-variables.md#tidb_max_bytes_before_tiflash_external_join-new-in-v700">`tidb_max_bytes_before_tiflash_external_join`</a>](/system-variables.md#tidb_max_bytes_before_tiflash_external_join-new-in-v700) ) のメモリ使用量のしきい値を調整することにより、オペレーターが使用できるメモリの最大量を制御できます。オペレータが使用するメモリがしきい値を超えると、データが自動的にディスクに書き込まれます。これにより、パフォーマンスがいくらか犠牲になりますが、より多くのデータを処理できるようになります。

    詳細については、 [<a href="/tiflash/tiflash-spill-disk.md">ドキュメンテーション</a>](/tiflash/tiflash-spill-disk.md)を参照してください。

-   統計収集の効率の向上[<a href="https://github.com/pingcap/tidb/issues/41930">#41930</a>](https://github.com/pingcap/tidb/issues/41930) @ [<a href="https://github.com/xuyifangreeneyes">シュイファングリーンアイズ</a>](https://github.com/xuyifangreeneyes)

    v7.0.0 では、TiDB は統計収集ロジックをさらに最適化し、収集時間を約 25% 短縮します。この最適化により、大規模データベース クラスターの運用効率と安定性が向上し、クラスターのパフォーマンスに対する統計収集の影響が軽減されます。

-   MPP 最適化[<a href="https://github.com/pingcap/tidb/issues/39710">#39710</a>](https://github.com/pingcap/tidb/issues/39710) @ [<a href="https://github.com/Reminiscent">懐かしい</a>](https://github.com/Reminiscent)用の新しいオプティマイザー ヒントを追加

    v7.0.0 では、TiDB に、MPP 実行プランの生成に影響を与える一連のオプティマイザー ヒントが追加されています。

    -   [<a href="/optimizer-hints.md#shuffle_joint1_name--tl_name-">`SHUFFLE_JOIN()`</a>](/optimizer-hints.md#shuffle_joint1_name--tl_name-) : MPP に有効になります。これは、指定されたテーブルに対してシャッフル結合アルゴリズムを使用するようにオプティマイザーに示唆します。
    -   [<a href="/optimizer-hints.md#broadcast_joint1_name--tl_name-">`BROADCAST_JOIN()`</a>](/optimizer-hints.md#broadcast_joint1_name--tl_name-) : MPP に有効になります。これは、指定されたテーブルに対してブロードキャスト結合アルゴリズムを使用するようにオプティマイザーに示唆します。
    -   [<a href="/optimizer-hints.md#mpp_1phase_agg">`MPP_1PHASE_AGG()`</a>](/optimizer-hints.md#mpp_1phase_agg) : MPP に有効になります。これは、指定されたクエリ ブロック内のすべての集計関数に対して 1 フェーズ集計アルゴリズムを使用するようにオプティマイザーに示唆します。
    -   [<a href="/optimizer-hints.md#mpp_2phase_agg">`MPP_2PHASE_AGG()`</a>](/optimizer-hints.md#mpp_2phase_agg) : MPP に有効になります。これは、指定されたクエリ ブロック内のすべての集計関数に対して 2 フェーズ集計アルゴリズムを使用するようにオプティマイザに示唆します。

    MPP オプティマイザーのヒントは、HTAP クエリへの介入に役立ち、HTAP ワークロードのパフォーマンスと安定性を向上させることができます。

    詳細については、 [<a href="/optimizer-hints.md">ドキュメンテーション</a>](/optimizer-hints.md)を参照してください。

-   オプティマイザー ヒントは、結合方法と結合順序[<a href="https://github.com/pingcap/tidb/issues/36600">#36600</a>](https://github.com/pingcap/tidb/issues/36600) @ [<a href="https://github.com/Reminiscent">懐かしい</a>](https://github.com/Reminiscent)の指定をサポートします。

    v7.0.0 では、オプティマイザ ヒント[<a href="/optimizer-hints.md#leadingt1_name--tl_name-">`LEADING()`</a>](/optimizer-hints.md#leadingt1_name--tl_name-)は結合方法に影響を与えるヒントと組み合わせて使用でき、それらの動作には互換性があります。複数テーブル結合の場合、最適な結合方法と結合順序を効果的に指定できるため、実行計画に対するオプティマイザー ヒントの制御が強化されます。

    新しいヒントの動作には小さな変更が加えられています。上位互換性を確保するために、TiDB ではシステム変数[<a href="/system-variables.md#tidb_opt_advanced_join_hint-new-in-v700">`tidb_opt_advanced_join_hint`</a>](/system-variables.md#tidb_opt_advanced_join_hint-new-in-v700)が導入されています。この変数が`OFF`に設定されている場合、オプティマイザー ヒントの動作は以前のバージョンと互換性があります。クラスターを以前のバージョンから v7.0.0 以降のバージョンにアップグレードすると、この変数は`OFF`に設定されます。より柔軟なヒント動作を取得するには、その動作がパフォーマンスの低下を引き起こさないことを確認した後、この変数を`ON`に設定することを強くお勧めします。

    詳細については、 [<a href="/optimizer-hints.md">ドキュメンテーション</a>](/optimizer-hints.md)を参照してください。

### 可用性 {#availability}

-   `prefer-leader`オプションをサポートします。これにより、読み取り操作の可用性が向上し、不安定なネットワーク状態での応答レイテンシーが短縮されます[<a href="https://github.com/pingcap/tidb/issues/40905">#40905</a>](https://github.com/pingcap/tidb/issues/40905) @ [<a href="https://github.com/LykxSassinator">リククスサシネーター</a>](https://github.com/LykxSassinator)

    TiDB のデータ読み取り動作は、システム変数[<a href="/system-variables.md#tidb_replica_read-new-in-v40">`tidb_replica_read`</a>](/system-variables.md#tidb_replica_read-new-in-v40)を通じて制御できます。 v7.0.0 では、この変数に`prefer-leader`オプションが追加されます。変数が`prefer-leader`に設定されている場合、TiDB は読み取り操作を実行するリーダー レプリカの選択を優先します。ディスクやネットワークのパフォーマンスの変動などにより、リーダー レプリカの処理速度が大幅に低下すると、TiDB は他の利用可能なフォロワー レプリカを選択して読み取り操作を実行し、可用性を高め、応答レイテンシーを短縮します。

    詳細については、 [<a href="/develop/dev-guide-use-follower-read.md">ドキュメンテーション</a>](/develop/dev-guide-use-follower-read.md)を参照してください。

### SQL {#sql}

-   生存時間 (TTL) は一般提供されています[<a href="https://github.com/pingcap/tidb/issues/39262">#39262</a>](https://github.com/pingcap/tidb/issues/39262) @ [<a href="https://github.com/lcwangchao">ルクワンチャオ</a>](https://github.com/lcwangchao) @ [<a href="https://github.com/YangKeao">ヤンケオ</a>](https://github.com/YangKeao)

    TTL は行レベルのライフサイクル制御ポリシーを提供します。 TiDB では、TTL 属性が設定されたテーブルは、構成に基づいて期限切れの行データを自動的にチェックして削除します。 TTL の目標は、クラスターのワークロードへの影響を最小限に抑えながら、ユーザーが時間内に不要なデータを定期的にクリーンアップできるようにすることです。

    詳細については、 [<a href="/time-to-live.md">ドキュメンテーション</a>](/time-to-live.md)を参照してください。

-   サポート`ALTER TABLE…REORGANIZE PARTITION` [<a href="https://github.com/pingcap/tidb/issues/15000">#15000</a>](https://github.com/pingcap/tidb/issues/15000) @ [<a href="https://github.com/mjonss">むじょん</a>](https://github.com/mjonss)

    TiDB は`ALTER TABLE...REORGANIZE PARTITION`構文をサポートします。この構文を使用すると、データを失うことなく、テーブルのパーティションの一部またはすべてを、結合、分割、その他の変更を含めて再編成できます。

    詳細については、 [<a href="/partitioned-table.md#reorganize-partitions">ドキュメンテーション</a>](/partitioned-table.md#reorganize-partitions)を参照してください。

-   キー分割[<a href="https://github.com/pingcap/tidb/issues/41364">#41364</a>](https://github.com/pingcap/tidb/issues/41364) @ [<a href="https://github.com/TonsnakeLin">トンスネークリン</a>](https://github.com/TonsnakeLin)をサポート

    TiDB はキー パーティショニングをサポートするようになりました。キー パーティショニングとハッシュ パーティショニングはどちらも、データを一定数のパーティションに均等に分散できます。違いは、ハッシュ パーティショニングでは指定された整数式または整数列に基づくデータの分散のみがサポートされるのに対し、キー パーティショニングでは列リストに基づいたデータの分散がサポートされ、キー パーティショニングのパーティショニング列は整数型に限定されないことです。

    詳細については、 [<a href="/partitioned-table.md#key-partitioning">ドキュメンテーション</a>](/partitioned-table.md#key-partitioning)を参照してください。

### DB操作 {#db-operations}

-   TiCDC は、storageサービス (GA) [<a href="https://github.com/pingcap/tiflow/issues/6797">#6797</a>](https://github.com/pingcap/tiflow/issues/6797) @ [<a href="https://github.com/zhaoxinyu">ジャオシンユ</a>](https://github.com/zhaoxinyu)への変更データのレプリケートをサポートします

    TiCDC は、Amazon S3、GCS、Azure Blob Storage、NFS、およびその他の S3 互換storageサービスへの変更データのレプリケートをサポートしています。ストレージサービスは価格も手頃で使いやすいです。 Kafka を使用していない場合は、storageサービスを使用できます。 TiCDC は、変更されたログをファイルに保存し、代わりにそれをstorageサービスに送信します。独自のコンシューマー プログラムは、storageサービスから、新しく生成された変更されたログ ファイルを定期的に読み取ることができます。現在、TiCDC は、変更されたログを canal-json および CSV 形式でstorageサービスにレプリケートすることをサポートしています。

    詳細については、 [<a href="/ticdc/ticdc-sink-to-cloud-storage.md">ドキュメンテーション</a>](/ticdc/ticdc-sink-to-cloud-storage.md)を参照してください。

-   TiCDC OpenAPI v2 [<a href="https://github.com/pingcap/tiflow/issues/8019">#8019</a>](https://github.com/pingcap/tiflow/issues/8019) @ [<a href="https://github.com/sdojjy">スドジ</a>](https://github.com/sdojjy)

    TiCDC は OpenAPI v2 を提供します。 OpenAPI v1 と比較して、OpenAPI v2 はレプリケーション タスクのより包括的なサポートを提供します。 TiCDC OpenAPI によって提供される機能は、 [<a href="/ticdc/ticdc-manage-changefeed.md">`cdc cli`ツール</a>](/ticdc/ticdc-manage-changefeed.md)のサブセットです。 OpenAPI v2 を介して TiCDC クラスターのクエリと操作を行うことができます。たとえば、TiCDC ノードのステータスの取得、クラスターの健全性ステータスの確認、レプリケーション タスクの管理などが可能です。

    詳細については、 [<a href="/ticdc/ticdc-open-api-v2.md">ドキュメンテーション</a>](/ticdc/ticdc-open-api-v2.md)を参照してください。

-   [<a href="https://dbeaver.io/">Dビーバー</a>](https://dbeaver.io/) v23.0.1 はデフォルトで TiDB をサポートします[<a href="https://github.com/dbeaver/dbeaver/issues/17396">#17396</a>](https://github.com/dbeaver/dbeaver/issues/17396) @ [<a href="https://github.com/Icemap">アイスマップ</a>](https://github.com/Icemap)

    -   独立した TiDB モジュール、アイコン、ロゴを提供します。
    -   デフォルト構成では[<a href="https://docs.pingcap.com/tidbcloud/select-cluster-tier#serverless-tier-beta">TiDB CloudServerless Tier</a>](https://docs.pingcap.com/tidbcloud/select-cluster-tier#serverless-tier-beta)サポートされており、Serverless Tierへの接続が容易になります。
    -   外部キー タブを表示または非表示にするための TiDB バージョンの識別をサポートします。
    -   SQL 実行計画を`EXPLAIN`結果で視覚化することをサポートします。
    -   `PESSIMISTIC` 、 `OPTIMISTIC` 、 `AUTO_RANDOM` 、 `PLACEMENT` 、 `POLICY` 、 `REORGANIZE` 、 `EXCHANGE` 、 `CACHE` 、 `NONCLUSTERED` 、 `CLUSTERED`などの TiDB キーワードの強調表示をサポートします。
    -   `TIDB_BOUNDED_STALENESS` 、 `TIDB_DECODE_KEY` 、 `TIDB_DECODE_PLAN` 、 `TIDB_IS_DDL_OWNER` 、 `TIDB_PARSE_TSO` 、 `TIDB_VERSION` 、 `TIDB_DECODE_SQL_DIGESTS` 、 `TIDB_SHARD`などの TiDB関数の強調表示をサポートします。

    詳細については、 [<a href="https://github.com/dbeaver/dbeaver/wiki">DBeaver のドキュメント</a>](https://github.com/dbeaver/dbeaver/wiki)を参照してください。

### データ移行 {#data-migration}

-   `LOAD DATA`ステートメントの機能を強化し、クラウドstorageからのデータのインポートをサポート (実験的) [<a href="https://github.com/pingcap/tidb/issues/40499">#40499</a>](https://github.com/pingcap/tidb/issues/40499) @ [<a href="https://github.com/lance6716">ランス6716</a>](https://github.com/lance6716)

    TiDB v7.0.0 より前では、 `LOAD DATA`ステートメントはクライアント側からのみデータ ファイルをインポートできました。クラウドstorageからデータをインポートしたい場合は、 TiDB Lightningに依存する必要がありました。ただし、 TiDB Lightningを個別に導入すると、追加の導入コストと管理コストが発生します。 v7.0.0 では、 `LOAD DATA`ステートメントを使用してクラウドstorageからデータを直接インポートできます。機能の例としては、次のようなものがあります。

    -   Amazon S3 および Google Cloud Storage から TiDB へのデータのインポートをサポートします。ワイルドカードを使用して複数のソース ファイルを TiDB に一度にインポートすることをサポートします。
    -   `DEFINED NULL BY`を使用した null の定義をサポートします。
    -   CSV および TSV 形式のソース ファイルをサポートします。

    詳細については、 [<a href="/sql-statements/sql-statement-load-data.md">ドキュメンテーション</a>](/sql-statements/sql-statement-load-data.md)を参照してください。

-   TiDB Lightning は、キーと値のペアを TiKV (GA) [<a href="https://github.com/pingcap/tidb/issues/41163">#41163</a>](https://github.com/pingcap/tidb/issues/41163) @ [<a href="https://github.com/gozssky">ゴズスキー</a>](https://github.com/gozssky)に送信する際の圧縮転送の有効化をサポートします

    v6.6.0 以降、 TiDB Lightning は、TiKV に送信する際のネットワーク転送用にローカルでエンコードおよびソートされたキーと値のペアの圧縮をサポートするため、ネットワーク上で転送されるデータ量が削減され、ネットワーク帯域幅のオーバーヘッドが削減されます。この機能がサポートされる前の以前の TiDB バージョンでは、 TiDB Lightning は比較的広いネットワーク帯域幅を必要とし、データ量が多い場合には高額なトラフィック料金が発生します。

    v7.0.0 では、この機能は GA となり、デフォルトで無効になっています。有効にするには、 TiDB Lightningの`compress-kv-pairs`設定項目を`"gzip"`または`"gz"`に設定します。

    詳細については、 [<a href="/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task">ドキュメンテーション</a>](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)を参照してください。

## 互換性の変更 {#compatibility-changes}

> **ノート：**
>
> このセクションでは、v6.6.0 から現在のバージョン (v7.0.0) にアップグレードするときに知っておく必要がある互換性の変更について説明します。 v6.5.0 以前のバージョンから現在のバージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更も確認する必要がある場合があります。

### MySQLの互換性 {#mysql-compatibility}

-   TiDB は、自動インクリメント列がインデックス[<a href="https://github.com/pingcap/tidb/issues/40580">#40580</a>](https://github.com/pingcap/tidb/issues/40580) @ [<a href="https://github.com/tiancaiamao">ティエンチャイアマオ</a>](https://github.com/tiancaiamao)でなければならないという制約を削除します。

    v7.0.0 より前では、TiDB の動作は MySQL と一致しており、自動インクリメント列がインデックスまたはインデックス プレフィックスである必要があります。 v7.0.0 以降、TiDB では、自動インクリメント列がインデックスまたはインデックス プレフィックスである必要があるという制約が削除されます。テーブルの主キーをより柔軟に定義し、自動インクリメント列を使用して並べ替えとページネーションをより簡単に実装できるようになりました。これにより、自動インクリメント列によって引き起こされる書き込みホットスポットの問題も回避され、クラスター化インデックスを持つテーブルを使用することでクエリのパフォーマンスが向上します。新しいリリースでは、次の構文を使用してテーブルを作成できます。

    ```sql
    CREATE TABLE test1 (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `k` int(11) NOT NULL DEFAULT '0',
        `c` char(120) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
        PRIMARY KEY(`k`, `id`)
    );
    ```

    この機能は TiCDC データ複製には影響しません。

    詳細については、 [<a href="/mysql-compatibility.md#auto-increment-id">ドキュメンテーション</a>](/mysql-compatibility.md#auto-increment-id)を参照してください。

-   TiDB は、次の例に示すように、キー パーティションをサポートします。

    ```sql
    CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
    job_code INT,
    store_id INT) PARTITION BY KEY(store_id) PARTITIONS 4;
    ```

    v7.0.0 以降、TiDB はキー パーティションをサポートし、MySQL `PARTITION BY LINEAR KEY`構文を解析できるようになりました。ただし、TiDB は`LINEAR`キーワードを無視し、代わりに非線形ハッシュ アルゴリズムを使用します。現在、 `KEY`パーティション タイプは、空のパーティション列リストを含むパーティション ステートメントをサポートしていません。

    詳細については、 [<a href="/partitioned-table.md#key-partitioning">ドキュメンテーション</a>](/partitioned-table.md#key-partitioning)を参照してください。

### 行動の変化 {#behavior-changes}

-   TiCDC は、Avro [<a href="https://github.com/pingcap/tiflow/issues/8490">#8490</a>](https://github.com/pingcap/tiflow/issues/8490) @ [<a href="https://github.com/3AceShowHand">3エースショーハンド</a>](https://github.com/3AceShowHand)の`FLOAT`データの誤ったエンコードの問題を修正しました

    TiCDC クラスターを v7.0.0 にアップグレードするときに、Avro を使用してレプリケートされたテーブルに`FLOAT`データ型が含まれている場合、変更フィードがスキーマを正常に更新できるように、アップグレードする前に Confluent Schema Registry の互換性ポリシーを手動で`None`に調整する必要があります。そうしないと、アップグレード後に変更フィードがスキーマを更新できなくなり、エラー状態になります。

-   v7.0.0 以降、 [<a href="/system-variables.md#tidb_dml_batch_size">`tidb_dml_batch_size`</a>](/system-variables.md#tidb_dml_batch_size)システム変数は[<a href="/sql-statements/sql-statement-load-data.md">`LOAD DATA`ステートメント</a>](/sql-statements/sql-statement-load-data.md)に影響しなくなりました。

### システム変数 {#system-variables}

| 変数名                                                                                                                                                                                                                            | 種類の変更    | 説明                                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `tidb_pessimistic_txn_aggressive_locking`                                                                                                                                                                                      | 削除されました  | この変数の名前は[<a href="/system-variables.md#tidb_pessimistic_txn_fair_locking-new-in-v700">`tidb_pessimistic_txn_fair_locking`</a>](/system-variables.md#tidb_pessimistic_txn_fair_locking-new-in-v700)に変更されます。                          |
| [<a href="/system-variables.md#tidb_enable_non_prepared_plan_cache">`tidb_enable_non_prepared_plan_cache`</a>](/system-variables.md#tidb_enable_non_prepared_plan_cache)                                                       | 修正済み     | v7.0.0 から有効になり、 [<a href="/sql-non-prepared-plan-cache.md">準備されていないプラン キャッシュ</a>](/sql-non-prepared-plan-cache.md)機能を有効にするかどうかを制御します。                                                                                               |
| [<a href="/system-variables.md#tidb_enable_null_aware_anti_join-new-in-v630">`tidb_enable_null_aware_anti_join`</a>](/system-variables.md#tidb_enable_null_aware_anti_join-new-in-v630)                                        | 修正済み     | さらなるテストの後、デフォルト値を`OFF`から`ON`に変更します。これは、デフォルトで特別な集合演算子`NOT IN`および`!= ALL`によって導かれるサブクエリによってアンチ結合が生成される場合に、TiDB が Null-Aware Hash Join を適用することを意味します。                                                                                  |
| [<a href="/system-variables.md#tidb_enable_resource_control-new-in-v660">`tidb_enable_resource_control`</a>](/system-variables.md#tidb_enable_resource_control-new-in-v660)                                                    | 修正済み     | デフォルト値を`OFF`から`ON`に変更します。これは、クラスターがデフォルトでリソースをリソース グループごとに分離することを意味します。 v7.0.0 ではリソース制御がデフォルトで有効になっているため、いつでもこの機能を使用できます。                                                                                                           |
| [<a href="/system-variables.md#tidb_non_prepared_plan_cache_size">`tidb_non_prepared_plan_cache_size`</a>](/system-variables.md#tidb_non_prepared_plan_cache_size)                                                             | 修正済み     | v7.0.0 から有効になり、キャッシュできる実行プランの最大数を[<a href="/sql-non-prepared-plan-cache.md">準備されていないプラン キャッシュ</a>](/sql-non-prepared-plan-cache.md)で制御します。                                                                                          |
| [<a href="/system-variables.md#tidb_rc_read_check_ts-new-in-v600">`tidb_rc_read_check_ts`</a>](/system-variables.md#tidb_rc_read_check_ts-new-in-v600)                                                                         | 修正済み     | v7.0.0 以降、この変数はプリペアドステートメントプロトコルでのカーソル フェッチ読み取りには無効になりました。                                                                                                                                                                          |
| [<a href="/system-variables.md#tidb_enable_inl_join_inner_multi_pattern-new-in-v700">`tidb_enable_inl_join_inner_multi_pattern`</a>](/system-variables.md#tidb_enable_inl_join_inner_multi_pattern-new-in-v700)                | 新しく追加された | この変数は、内部テーブルに`Selection`または`Projection`の演算子がある場合にインデックス結合をサポートするかどうかを制御します。                                                                                                                                                         |
| [<a href="/system-variables.md#tidb_enable_plan_cache_for_subquery-new-in-v700">`tidb_enable_plan_cache_for_subquery`</a>](/system-variables.md#tidb_enable_plan_cache_for_subquery-new-in-v700)                               | 新しく追加された | この変数は、 プリペアドプランキャッシュ がサブクエリを含むクエリをキャッシュするかどうかを制御します。                                                                                                                                                                                |
| [<a href="/system-variables.md#tidb_enable_plan_replayer_continuous_capture-new-in-v700">`tidb_enable_plan_replayer_continuous_capture`</a>](/system-variables.md#tidb_enable_plan_replayer_continuous_capture-new-in-v700)    | 新しく追加された | この変数は、 [<a href="/sql-plan-replayer.md#use-plan-replayer-continuous-capture">`PLAN REPLAYER CONTINUOUS CAPTURE`</a>](/sql-plan-replayer.md#use-plan-replayer-continuous-capture)機能を有効にするかどうかを制御します。デフォルト値`OFF` 、この機能を無効にすることを意味します。 |
| [<a href="/system-variables.md#tidb_load_based_replica_read_threshold-new-in-v700">`tidb_load_based_replica_read_threshold`</a>](/system-variables.md#tidb_load_based_replica_read_threshold-new-in-v700)                      | 新しく追加された | この変数は、負荷ベースのレプリカ読み取りをトリガーするためのしきい値を設定します。この変数によって制御される機能は、TiDB v7.0.0 では完全には機能しません。デフォルト値を変更しないでください。                                                                                                                               |
| [<a href="/system-variables.md#tidb_opt_advanced_join_hint-new-in-v700">`tidb_opt_advanced_join_hint`</a>](/system-variables.md#tidb_opt_advanced_join_hint-new-in-v700)                                                       | 新しく追加された | この変数は、結合方法のヒントが結合再順序の最適化に影響を与えるかどうかを制御します。デフォルト値は`ON`で、新しい互換性のある制御モードが使用されることを意味します。値`OFF` 、v7.0.0 が使用される前の動作を意味します。上位互換性を確保するため、クラスターが以前のバージョンから v7.0.0 以降にアップグレードされると、この変数の値は`OFF`に設定されます。                                        |
| [<a href="/system-variables.md#tidb_opt_derive_topn-new-in-v700">`tidb_opt_derive_topn`</a>](/system-variables.md#tidb_opt_derive_topn-new-in-v700)                                                                            | 新しく追加された | この変数は、 [<a href="/derive-topn-from-window.md">ウィンドウ関数から TopN または Limit を導出する</a>](/derive-topn-from-window.md)最適化ルールを有効にするかどうかを制御します。デフォルト値は`OFF`で、最適化ルールが有効になっていないことを意味します。                                                        |
| [<a href="/system-variables.md#tidb_opt_enable_late_materialization-new-in-v700">`tidb_opt_enable_late_materialization`</a>](/system-variables.md#tidb_opt_enable_late_materialization-new-in-v700)                            | 新しく追加された | この変数は、 [<a href="/tiflash/tiflash-late-materialization.md">TiFlash後期マテリアライゼーション</a>](/tiflash/tiflash-late-materialization.md)機能を有効にするかどうかを制御します。デフォルト値は`OFF`で、この機能が有効になっていないことを意味します。                                              |
| [<a href="/system-variables.md#tidb_opt_ordering_index_selectivity_threshold-new-in-v700">`tidb_opt_ordering_index_selectivity_threshold`</a>](/system-variables.md#tidb_opt_ordering_index_selectivity_threshold-new-in-v700) | 新しく追加された | この変数は、SQL ステートメントに`ORDER BY`と`LIMIT`節が含まれ、フィルター条件がある場合に、オプティマイザーがインデックスを選択する方法を制御します。                                                                                                                                               |
| [<a href="/system-variables.md#tidb_pessimistic_txn_fair_locking-new-in-v700">`tidb_pessimistic_txn_fair_locking`</a>](/system-variables.md#tidb_pessimistic_txn_fair_locking-new-in-v700)                                     | 新しく追加された | 拡張された悲観的ロック解除モデルを有効にして、単一行の競合シナリオでトランザクションの末尾レイテンシーを短縮するかどうかを制御します。デフォルト値は`ON`です。クラスターが以前のバージョンから v7.0.0 以降にアップグレードされると、この変数の値は`OFF`に設定されます。                                                                                        |
| [<a href="/system-variables.md#tidb_ttl_running_tasks-new-in-v700">`tidb_ttl_running_tasks`</a>](/system-variables.md#tidb_ttl_running_tasks-new-in-v700)                                                                      | 新しく追加された | この変数は、クラスター全体にわたる TTL タスクの同時実行性を制限するために使用されます。デフォルト値`-1` TTL タスクが TiKV ノードの数と同じであることを意味します。                                                                                                                                         |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                                                                                                                  | 種類の変更    | 説明                                                                                                                                                                                                                                                                  |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiKV           | `server.snap-max-write-bytes-per-sec`                                                                                                                                                            | 削除されました  | このパラメータの名前は[<a href="/tikv-configuration-file.md#snap-io-max-bytes-per-sec">`server.snap-io-max-bytes-per-sec`</a>](/tikv-configuration-file.md#snap-io-max-bytes-per-sec)に変更されます。                                                                                  |
| TiKV           | [<a href="/tikv-configuration-file.md#enable-log-recycle-new-in-v630">`raft-engine.enable-log-recycle`</a>](/tikv-configuration-file.md#enable-log-recycle-new-in-v630)                          | 修正済み     | デフォルト値は`false`から`true`に変更されます。                                                                                                                                                                                                                                      |
| TiKV           | [<a href="/tikv-configuration-file.md#advance-ts-interval">`resolved-ts.advance-ts-interval`</a>](/tikv-configuration-file.md#advance-ts-interval)                                               | 修正済み     | デフォルト値は`"1s"`から`"20s"`に変更されます。この変更により、Resolved TS の定期的な進行の間隔が長くなり、TiKV ノード間のトラフィック消費が削減されます。                                                                                                                                                                        |
| TiKV           | [<a href="/tikv-configuration-file.md#resource-control">`resource-control.enabled`</a>](/tikv-configuration-file.md#resource-control)                                                            | 修正済み     | デフォルト値は`false`から`true`に変更されます。                                                                                                                                                                                                                                      |
| TiKV           | [<a href="/tikv-configuration-file.md#prefill-for-recycle-new-in-v700">`raft-engine.prefill-for-recycle`</a>](/tikv-configuration-file.md#prefill-for-recycle-new-in-v700)                       | 新しく追加された | Raft Engineでログをリサイクルするために空のログ ファイルを生成するかどうかを制御します。デフォルト値は`false`です。                                                                                                                                                                                                 |
| PD             | [<a href="/pd-configuration-file.md#degraded-mode-wait-duration">`degraded-mode-wait-duration`</a>](/pd-configuration-file.md#degraded-mode-wait-duration)                                       | 新しく追加された | [<a href="/tidb-resource-control.md">リソース制御</a>](/tidb-resource-control.md)に関連する設定項目。縮退モードをトリガーするまでの待ち時間を制御します。デフォルト値は`0s`です。                                                                                                                                       |
| PD             | [<a href="/pd-configuration-file.md#read-base-cost">`read-base-cost`</a>](/pd-configuration-file.md#read-base-cost)                                                                              | 新しく追加された | [<a href="/tidb-resource-control.md">リソース制御</a>](/tidb-resource-control.md)に関連する設定項目。読み取りリクエストから RU への変換の基本係数を制御します。デフォルト値は`0.25`です。                                                                                                                                |
| PD             | [<a href="/pd-configuration-file.md#read-cost-per-byte">`read-cost-per-byte`</a>](/pd-configuration-file.md#read-cost-per-byte)                                                                  | 新しく追加された | [<a href="/tidb-resource-control.md">リソース制御</a>](/tidb-resource-control.md)に関連する設定項目。読み取りフローから RU への変換の基本係数を制御します。デフォルト値は`1/ (64 * 1024)`です。                                                                                                                        |
| PD             | [<a href="/pd-configuration-file.md#read-cpu-ms-cost">`read-cpu-ms-cost`</a>](/pd-configuration-file.md#read-cpu-ms-cost)                                                                        | 新しく追加された | [<a href="/tidb-resource-control.md">リソース制御</a>](/tidb-resource-control.md)に関連する設定項目。 CPU から RU への変換の基本係数を制御します。デフォルト値は`1/3`です。                                                                                                                                     |
| PD             | [<a href="/pd-configuration-file.md#write-base-cost">`write-base-cost`</a>](/pd-configuration-file.md#write-base-cost)                                                                           | 新しく追加された | [<a href="/tidb-resource-control.md">リソース制御</a>](/tidb-resource-control.md)に関連する設定項目。書き込みリクエストから RU への変換の基本係数を制御します。デフォルト値は`1`です。                                                                                                                                   |
| PD             | [<a href="/pd-configuration-file.md#write-cost-per-byte">`write-cost-per-byte`</a>](/pd-configuration-file.md#write-cost-per-byte)                                                               | 新しく追加された | [<a href="/tidb-resource-control.md">リソース制御</a>](/tidb-resource-control.md)に関連する設定項目。書き込みフローから RU への変換の基本係数を制御します。デフォルト値は`1/1024`です。                                                                                                                                |
| TiFlash        | [<a href="/tiflash/tiflash-disaggregated-and-s3.md">`flash.disaggregated_mode`</a>](/tiflash/tiflash-disaggregated-and-s3.md)                                                                    | 新しく追加された | TiFlashの分散アーキテクチャでは、このTiFlashノードが書き込みノードであるか計算ノードであるかを示します。値は`tiflash_write`または`tiflash_compute`です。                                                                                                                                                                 |
| TiFlash        | [<a href="/tiflash/tiflash-disaggregated-and-s3.md">`storage.s3.endpoint`</a>](/tiflash/tiflash-disaggregated-and-s3.md)                                                                         | 新しく追加された | S3 に接続するエンドポイント。                                                                                                                                                                                                                                                    |
| TiFlash        | [<a href="/tiflash/tiflash-disaggregated-and-s3.md">`storage.s3.bucket`</a>](/tiflash/tiflash-disaggregated-and-s3.md)                                                                           | 新しく追加された | TiFlashがすべてのデータを保存するバケット。                                                                                                                                                                                                                                           |
| TiFlash        | [<a href="/tiflash/tiflash-disaggregated-and-s3.md">`storage.s3.root`</a>](/tiflash/tiflash-disaggregated-and-s3.md)                                                                             | 新しく追加された | S3 バケット内のデータstorageのルート ディレクトリ。                                                                                                                                                                                                                                     |
| TiFlash        | [<a href="/tiflash/tiflash-disaggregated-and-s3.md">`storage.s3.access_key_id`</a>](/tiflash/tiflash-disaggregated-and-s3.md)                                                                    | 新しく追加された | S3 にアクセスする場合は`ACCESS_KEY_ID` 。                                                                                                                                                                                                                                      |
| TiFlash        | [<a href="/tiflash/tiflash-disaggregated-and-s3.md">`storage.s3.secret_access_key`</a>](/tiflash/tiflash-disaggregated-and-s3.md)                                                                | 新しく追加された | S3 にアクセスする場合は`SECRET_ACCESS_KEY` 。                                                                                                                                                                                                                                  |
| TiFlash        | [<a href="/tiflash/tiflash-disaggregated-and-s3.md">`storage.remote.cache.dir`</a>](/tiflash/tiflash-disaggregated-and-s3.md)                                                                    | 新しく追加された | TiFlash計算ノードのローカル データ キャッシュ ディレクトリ。                                                                                                                                                                                                                                 |
| TiFlash        | [<a href="/tiflash/tiflash-disaggregated-and-s3.md">`storage.remote.cache.capacity`</a>](/tiflash/tiflash-disaggregated-and-s3.md)                                                               | 新しく追加された | TiFlashコンピューティング ノードのローカル データ キャッシュ ディレクトリのサイズ。                                                                                                                                                                                                                     |
| TiDB Lightning | [<a href="/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task">`add-index-by-sql`</a>](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)                      | 新しく追加された | SQL を使用して物理インポート モードでインデックスを追加するかどうかを制御します。デフォルト値は`false`です。これは、 TiDB Lightning が行データとインデックス データの両方を KV ペアにエンコードし、一緒に TiKV にインポートすることを意味します。 SQL を使用してインデックスを追加する利点は、データのインポートとインデックスのインポートを分離し、データを迅速にインポートできることです。データのインポート後にインデックスの作成に失敗した場合でも、データの整合性は影響を受けません。 |
| TiCDC          | [<a href="/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters">`enable-table-across-nodes`</a>](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)         | 新しく追加された | リージョンの数に応じてテーブルを複数の同期範囲に分割するかどうかを決定します。これらの範囲は、複数の TiCDC ノードによって複製できます。                                                                                                                                                                                             |
| TiCDC          | [<a href="/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters">`region-threshold`</a>](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)                  | 新しく追加された | `enable-table-across-nodes`が有効な場合、この機能は`region-threshold`以上のリージョンを持つテーブルでのみ有効になります。                                                                                                                                                                                 |
| DM             | [<a href="/dm/task-configuration-file-full.md#task-configuration-file-template-advanced">`analyze`</a>](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)           | 新しく追加された | CHECKSUM の完了後に各テーブルに対して`ANALYZE TABLE <table>`操作を実行するかどうかを制御します。 `"required"` / `"optional"` / `"off"`として設定できます。デフォルト値は`"optional"`です。                                                                                                                              |
| DM             | [<a href="/dm/task-configuration-file-full.md#task-configuration-file-template-advanced">`range-concurrency`</a>](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced) | 新しく追加された | KV データを TiKV に書き込む dm-worker の同時実行性を制御します。                                                                                                                                                                                                                          |
| DM             | [<a href="/dm/task-configuration-file-full.md#task-configuration-file-template-advanced">`compress-kv-pairs`</a>](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced) | 新しく追加された | dm-worker が KV データを TiKV に送信するときに圧縮を有効にするかどうかを制御します。現在、gzip のみがサポートされています。デフォルト値は空で、圧縮しないことを意味します。                                                                                                                                                                  |
| DM             | [<a href="/dm/task-configuration-file-full.md#task-configuration-file-template-advanced">`pd-addr`</a>](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)           | 新しく追加された | 物理インポート モードでダウンストリーム PDサーバーのアドレスを制御します。 1 つ以上の PD サーバーを入力できます。この構成項目が空の場合、デフォルトで TiDB クエリからの PD アドレス情報が使用されます。                                                                                                                                                      |

## 改善点 {#improvements}

-   TiDB

    -   `EXPAND`演算子を導入して、1 つのステートメントに複数の`DISTINCT`含む SQL クエリのパフォーマンスを最適化します。 `SELECT`ステートメント[<a href="https://github.com/pingcap/tidb/issues/16581">#16581</a>](https://github.com/pingcap/tidb/issues/16581) @ [<a href="https://github.com/AilinKid">アイリンキッド</a>](https://github.com/AilinKid)
    -   インデックス結合[<a href="https://github.com/pingcap/tidb/issues/40505">#40505</a>](https://github.com/pingcap/tidb/issues/40505) @ [<a href="https://github.com/Yisaer">イーサール</a>](https://github.com/Yisaer)でより多くの SQL 形式をサポート
    -   場合によっては、TiDB でパーティションテーブルデータをグローバルにソートしないでください[<a href="https://github.com/pingcap/tidb/issues/26166">#26166</a>](https://github.com/pingcap/tidb/issues/26166) @ [<a href="https://github.com/Defined2014">定義2014</a>](https://github.com/Defined2014)
    -   `fair lock mode`と`lock only if exists`の同時使用をサポート[<a href="https://github.com/pingcap/tidb/issues/42068">#42068</a>](https://github.com/pingcap/tidb/issues/42068) @ [<a href="https://github.com/MyonKeminta">ミョンケミンタ</a>](https://github.com/MyonKeminta)
    -   トランザクション低速ログとトランザクション内部イベント[<a href="https://github.com/pingcap/tidb/issues/41863">#41863</a>](https://github.com/pingcap/tidb/issues/41863) @ [<a href="https://github.com/ekexium">エキシウム</a>](https://github.com/ekexium)の印刷をサポート
    -   `ILIKE`オペレーター[<a href="https://github.com/pingcap/tidb/issues/40943">#40943</a>](https://github.com/pingcap/tidb/issues/40943) @ [<a href="https://github.com/xzhangxian1008">xzhangxian1008</a>](https://github.com/xzhangxian1008)をサポート

-   PD

    -   ストア制限[<a href="https://github.com/tikv/pd/issues/6043">#6043</a>](https://github.com/tikv/pd/issues/6043) @ [<a href="https://github.com/nolouch">ノールーシュ</a>](https://github.com/nolouch)によるスケジュールの失敗に対する新しい監視メトリックを追加します。

-   TiFlash

    -   書き込みパス[<a href="https://github.com/pingcap/tiflash/issues/7144">#7144</a>](https://github.com/pingcap/tiflash/issues/7144) @ [<a href="https://github.com/hongyunyan">ホンユニャン</a>](https://github.com/hongyunyan)での TiFlash のメモリ使用量を削減します。
    -   多くのテーブル[<a href="https://github.com/pingcap/tiflash/issues/7146">#7146</a>](https://github.com/pingcap/tiflash/issues/7146) @ [<a href="https://github.com/hongyunyan">ホンユニャン</a>](https://github.com/hongyunyan)を使用するシナリオで TiFlash の再起動時間を短縮します。
    -   `ILIKE`オペレーター[<a href="https://github.com/pingcap/tiflash/issues/6740">#6740</a>](https://github.com/pingcap/tiflash/issues/6740) @ [<a href="https://github.com/xzhangxian1008">xzhangxian1008</a>](https://github.com/xzhangxian1008)の押し下げをサポート

-   ツール

    -   TiCDC

        -   Kafka がダウンストリームであるシナリオで、単一の大きなテーブルのデータ変更を複数の TiCDC ノードに分散することをサポートします。これにより、大規模な TiDB クラスター[<a href="https://github.com/pingcap/tiflow/issues/8247">#8247</a>](https://github.com/pingcap/tiflow/issues/8247) @ [<a href="https://github.com/overvenus">オーバーヴィーナス</a>](https://github.com/overvenus)のデータ統合シナリオにおける単一テーブルのスケーラビリティの問題が解決されます。

            TiCDC 構成項目`enable_table_across_nodes` ～ `true`を設定することで、この機能を有効にできます。 `region_threshold`を使用すると、テーブルのリージョン数がこのしきい値を超えたときに、TiCDC が対応するテーブルのデータ変更の複数の TiCDC ノードへの分散を開始するように指定できます。

        -   REDO アプライアでのトランザクションの分割をサポートして、スループットを向上させ、災害復旧シナリオでの RTO を削減します[<a href="https://github.com/pingcap/tiflow/issues/8318">#8318</a>](https://github.com/pingcap/tiflow/issues/8318) @ [<a href="https://github.com/CharlesCheung96">CharlesCheung96</a>](https://github.com/CharlesCheung96)

        -   テーブルのスケジューリングを改善して、単一のテーブルをさまざまな TiCDC ノード[<a href="https://github.com/pingcap/tiflow/issues/8247">#8247</a>](https://github.com/pingcap/tiflow/issues/8247) @ [<a href="https://github.com/overvenus">オーバーヴィーナス</a>](https://github.com/overvenus)にさらに均等に分割します。

        -   MQ シンク[<a href="https://github.com/pingcap/tiflow/issues/8286">#8286</a>](https://github.com/pingcap/tiflow/issues/8286) @ [<a href="https://github.com/hi-rustin">こんにちはラスティン</a>](https://github.com/hi-rustin)にラージ行監視メトリクスを追加します。

        -   リージョンに複数のテーブル[<a href="https://github.com/pingcap/tiflow/issues/6346">#6346</a>](https://github.com/pingcap/tiflow/issues/6346) @ [<a href="https://github.com/overvenus">オーバーヴィーナス</a>](https://github.com/overvenus)のデータが含まれるシナリオで、TiKV ノードと TiCDC ノード間のネットワーク トラフィックを削減します。

        -   チェックポイント TS と解決済み TS の P99 メトリクス パネルをラグ分析パネル[<a href="https://github.com/pingcap/tiflow/issues/8524">#8524</a>](https://github.com/pingcap/tiflow/issues/8524) @ [<a href="https://github.com/hi-rustin">こんにちはラスティン</a>](https://github.com/hi-rustin)に移動します。

        -   REDO ログ[<a href="https://github.com/pingcap/tiflow/issues/8361">#8361</a>](https://github.com/pingcap/tiflow/issues/8361) @ [<a href="https://github.com/CharlesCheung96">CharlesCheung96</a>](https://github.com/CharlesCheung96)での DDL イベントの適用のサポート

        -   アップストリーム書き込みスループット[<a href="https://github.com/pingcap/tiflow/issues/7720">#7720</a>](https://github.com/pingcap/tiflow/issues/7720) @ [<a href="https://github.com/overvenus">オーバーヴィーナス</a>](https://github.com/overvenus)に基づいて、TiCDC ノードへのテーブルの分割とスケジューリングをサポートします。

    -   TiDB Lightning

        -   TiDB Lightning物理インポート モードは、データ インポートとインデックス インポートの分離をサポートし、インポートの速度と安定性を向上させます[<a href="https://github.com/pingcap/tidb/issues/42132">#42132</a>](https://github.com/pingcap/tidb/issues/42132) @ [<a href="https://github.com/gozssky">ゴズスキー</a>](https://github.com/gozssky)

            `add-index-by-sql`パラメータを追加します。デフォルト値は`false`です。これは、 TiDB Lightning が行データとインデックス データの両方を KV ペアにエンコードし、それらを一緒に TiKV にインポートすることを意味します。これを`true`に設定すると、 TiDB Lightning が行データのインポート後に`ADD INDEX` SQL ステートメントを介してインデックスを追加し、インポートの速度と安定性が向上することを意味します。

        -   `tikv-importer.keyspace-name`パラメータを追加します。デフォルト値は空の文字列です。これは、 TiDB Lightning が、データをインポートするために対応するテナントのキースペース名を自動的に取得することを意味します。値を指定すると、指定したキースペース名がデータのインポートに使用されます。このパラメータにより、マルチテナント TiDB クラスターにデータをインポートする際のTiDB Lightningの構成に柔軟性が与えられます。 [<a href="https://github.com/pingcap/tidb/issues/41915">#41915</a>](https://github.com/pingcap/tidb/issues/41915) @ [<a href="https://github.com/lichunzhu">リチュンジュ</a>](https://github.com/lichunzhu)

## バグの修正 {#bug-fixes}

-   TiDB

    -   TiDB を v6.5.1 から以降のバージョン[<a href="https://github.com/pingcap/tidb/issues/41502">#41502</a>](https://github.com/pingcap/tidb/issues/41502) @ [<a href="https://github.com/chrysan">クリサン</a>](https://github.com/chrysan)にアップグレードするときに更新が欠落する問題を修正
    -   [<a href="https://github.com/pingcap/tidb/issues/41423">#41423</a>](https://github.com/pingcap/tidb/issues/41423) @ [<a href="https://github.com/crazycs520">クレイジークス520</a>](https://github.com/crazycs520)のアップグレード後に一部のシステム変数のデフォルト値が変更されない問題を修正
    -   インデックスの追加に関連するコプロセッサーのリクエスト タイプが不明[<a href="https://github.com/pingcap/tidb/issues/41400">#41400</a>](https://github.com/pingcap/tidb/issues/41400) @ [<a href="https://github.com/tangenta">タンジェンタ</a>](https://github.com/tangenta)として表示される問題を修正
    -   インデックス[<a href="https://github.com/pingcap/tidb/issues/41515">#41515</a>](https://github.com/pingcap/tidb/issues/41515) @ [<a href="https://github.com/tangenta">タンジェンタ</a>](https://github.com/tangenta)を追加するときに「PessimisticLockNotFound」を返す問題を修正
    -   一意のインデックス[<a href="https://github.com/pingcap/tidb/issues/41630">#41630</a>](https://github.com/pingcap/tidb/issues/41630) @ [<a href="https://github.com/tangenta">タンジェンタ</a>](https://github.com/tangenta)を追加するときに誤って`found duplicate key`を返す問題を修正
    -   インデックス[<a href="https://github.com/pingcap/tidb/issues/41880">#41880</a>](https://github.com/pingcap/tidb/issues/41880) @ [<a href="https://github.com/tangenta">タンジェンタ</a>](https://github.com/tangenta)を追加するときのpanicの問題を修正
    -   TiFlash が実行中に生成された列のエラーを報告する問題を修正[<a href="https://github.com/pingcap/tidb/issues/40663">#40663</a>](https://github.com/pingcap/tidb/issues/40663) @ [<a href="https://github.com/guo-shaoge">グオシャオゲ</a>](https://github.com/guo-shaoge)
    -   時間タイプ[<a href="https://github.com/pingcap/tidb/issues/41938">#41938</a>](https://github.com/pingcap/tidb/issues/41938) @ [<a href="https://github.com/xuyifangreeneyes">シュイファングリーンアイズ</a>](https://github.com/xuyifangreeneyes)がある場合、TiDB が統計を正しく取得できない場合がある問題を修正
    -   準備されたプラン キャッシュが有効になっている場合にフル インデックス スキャンでエラーが発生する可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/42150">#42150</a>](https://github.com/pingcap/tidb/issues/42150) @ [<a href="https://github.com/fzzf678">fzzf678</a>](https://github.com/fzzf678)
    -   `IFNULL(NOT NULL COLUMN, ...)`が間違った結果[<a href="https://github.com/pingcap/tidb/issues/41734">#41734</a>](https://github.com/pingcap/tidb/issues/41734) @ [<a href="https://github.com/LittleFall">リトルフォール</a>](https://github.com/LittleFall)を返す可能性がある問題を修正
    -   パーティションテーブル内のすべてのデータが単一のリージョン[<a href="https://github.com/pingcap/tidb/issues/41801">#41801</a>](https://github.com/pingcap/tidb/issues/41801) @ [<a href="https://github.com/Defined2014">定義2014</a>](https://github.com/Defined2014)にある場合、TiDB が誤った結果を生成する可能性がある問題を修正します。
    -   単一の SQL ステートメント[<a href="https://github.com/pingcap/tidb/issues/42135">#42135</a>](https://github.com/pingcap/tidb/issues/42135) @ [<a href="https://github.com/mjonss">むじょん</a>](https://github.com/mjonss)に異なるパーティション分割テーブルが含まれる場合、TiDB が誤った結果を生成する可能性がある問題を修正します。
    -   パーティションテーブル[<a href="https://github.com/pingcap/tidb/issues/41638">#41638</a>](https://github.com/pingcap/tidb/issues/41638) @ [<a href="https://github.com/xuyifangreeneyes">シュイファングリーンアイズ</a>](https://github.com/xuyifangreeneyes)に新しいインデックスを追加した後、パーティションテーブルテーブルで統計の自動収集が正しくトリガーされないことがある問題を修正します。
    -   統計を 2 回続けて収集した後、TiDB が間違った列統計情報を読み取る可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/42073">#42073</a>](https://github.com/pingcap/tidb/issues/42073) @ [<a href="https://github.com/xuyifangreeneyes">シュイファングリーンアイズ</a>](https://github.com/xuyifangreeneyes)
    -   プラン キャッシュの準備が有効になっている場合に IndexMerge が誤った結果を生成する可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/41828">#41828</a>](https://github.com/pingcap/tidb/issues/41828) @ [<a href="https://github.com/qw4990">qw4990</a>](https://github.com/qw4990)
    -   IndexMerge で goroutine リーク[<a href="https://github.com/pingcap/tidb/issues/41605">#41605</a>](https://github.com/pingcap/tidb/issues/41605) @ [<a href="https://github.com/guo-shaoge">グオシャオゲ</a>](https://github.com/guo-shaoge)が発生する可能性がある問題を修正
    -   非 BIGINT 符号なし整数が文字列/10 進数[<a href="https://github.com/pingcap/tidb/issues/41736">#41736</a>](https://github.com/pingcap/tidb/issues/41736) @ [<a href="https://github.com/LittleFall">リトルフォール</a>](https://github.com/LittleFall)と比較されたときに誤った結果を生成する可能性がある問題を修正
    -   メモリ制限の超過により前の`ANALYZE`ステートメントを強制終了すると、同じセッション内の現在の`ANALYZE`ステートメントが強制終了される可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/41825">#41825</a>](https://github.com/pingcap/tidb/issues/41825) @ [<a href="https://github.com/XuHuaiyu">徐淮嶼</a>](https://github.com/XuHuaiyu)
    -   バッチコプロセッサ[<a href="https://github.com/pingcap/tidb/issues/41412">#41412</a>](https://github.com/pingcap/tidb/issues/41412) @ [<a href="https://github.com/you06">あなた06</a>](https://github.com/you06)の情報収集処理中にデータ競合が発生することがある問題を修正
    -   アサーション エラーにより、パーティション テーブル[<a href="https://github.com/pingcap/tidb/issues/40629">#40629</a>](https://github.com/pingcap/tidb/issues/40629) @ [<a href="https://github.com/ekexium">エキシウム</a>](https://github.com/ekexium)の MVCC 情報が出力されない問題を修正します。
    -   フェア ロック モードにより、存在しないキー[<a href="https://github.com/pingcap/tidb/issues/41527">#41527</a>](https://github.com/pingcap/tidb/issues/41527) @ [<a href="https://github.com/ekexium">エキシウム</a>](https://github.com/ekexium)にロックが追加される問題を修正
    -   `INSERT IGNORE`および`REPLACE`ステートメントが、値[<a href="https://github.com/pingcap/tidb/issues/42121">#42121</a>](https://github.com/pingcap/tidb/issues/42121) @ [<a href="https://github.com/zyguan">ジグアン</a>](https://github.com/zyguan)を変更しないキーをロックしない問題を修正します。

-   PD

    -   リージョン散布操作によりリーダー[<a href="https://github.com/tikv/pd/issues/6017">#6017</a>](https://github.com/tikv/pd/issues/6017) @ [<a href="https://github.com/HunDunDM">フンドゥンDM</a>](https://github.com/HunDunDM)が不均一に分布する可能性がある問題を修正
    -   起動時[<a href="https://github.com/tikv/pd/issues/6069">#6069</a>](https://github.com/tikv/pd/issues/6069) @ [<a href="https://github.com/rleungx">ルルンクス</a>](https://github.com/rleungx)でPDメンバーを取得する際にデータ競合が発生する場合がある問題を修正
    -   ホットスポット統計[<a href="https://github.com/tikv/pd/issues/6069">#6069</a>](https://github.com/tikv/pd/issues/6069) @ [<a href="https://github.com/lhy1024">lhy1024</a>](https://github.com/lhy1024)を収集するときにデータ競合が発生する可能性がある問題を修正
    -   配置ルールを切り替えると、引出線[<a href="https://github.com/tikv/pd/issues/6195">#6195</a>](https://github.com/tikv/pd/issues/6195) @ [<a href="https://github.com/bufferflies">バッファフライ</a>](https://github.com/bufferflies)の分布が不均一になる可能性がある問題を修正

-   TiFlash

    -   特定の場合に 10 進数の除算で最後の桁が切り上げられない問題を修正[<a href="https://github.com/pingcap/tiflash/issues/7022">#7022</a>](https://github.com/pingcap/tiflash/issues/7022) @ [<a href="https://github.com/LittleFall">リトルフォール</a>](https://github.com/LittleFall)
    -   特定の場合に Decimal キャストが誤って切り上げられる問題を修正[<a href="https://github.com/pingcap/tiflash/issues/6994">#6994</a>](https://github.com/pingcap/tiflash/issues/6994) @ [<a href="https://github.com/windtalker">ウィンドトーカー</a>](https://github.com/windtalker)
    -   新しい照合順序[<a href="https://github.com/pingcap/tiflash/issues/6807">#6807</a>](https://github.com/pingcap/tiflash/issues/6807) @ [<a href="https://github.com/xzhangxian1008">xzhangxian1008</a>](https://github.com/xzhangxian1008)を有効にした後、TopN/Sort 演算子が誤った結果を生成する問題を修正します。
    -   単一のTiFlashノード[<a href="https://github.com/pingcap/tiflash/issues/6993">#6993</a>](https://github.com/pingcap/tiflash/issues/6993) @ [<a href="https://github.com/windtalker">ウィンドトーカー</a>](https://github.com/windtalker)で 1,200 万行を超える結果セットを集計するときに、 TiFlash がエラーを報告する問題を修正します。

-   ツール

    -   バックアップと復元 (BR)

        -   PITR リカバリ プロセス[<a href="https://github.com/pingcap/tidb/issues/42001">#42001</a>](https://github.com/pingcap/tidb/issues/42001) @ [<a href="https://github.com/joccau">ジョッカウ</a>](https://github.com/joccau)中にリージョンを分割するための待ち時間が不十分である問題を修正します。
        -   PITR リカバリ プロセス[<a href="https://github.com/pingcap/tidb/issues/41983">#41983</a>](https://github.com/pingcap/tidb/issues/41983) @ [<a href="https://github.com/joccau">ジョッカウ</a>](https://github.com/joccau)中に発生した`memory is limited`エラーによるリカバリの失敗の問題を修正します。
        -   PD ノードがダウンしているときに PITR ログのバックアップの進行状況が進まない問題を修正[<a href="https://github.com/tikv/tikv/issues/14184">#14184</a>](https://github.com/tikv/tikv/issues/14184) @ [<a href="https://github.com/YuJuncen">ユジュンセン</a>](https://github.com/YuJuncen)
        -   リージョンリーダーの移行が発生したときに PITR ログ バックアップの進行状況のレイテンシーが増加する問題を緩和します[<a href="https://github.com/tikv/tikv/issues/13638">#13638</a>](https://github.com/tikv/tikv/issues/13638) @ [<a href="https://github.com/YuJuncen">ユジュンセン</a>](https://github.com/YuJuncen)

    -   TiCDC

        -   変更フィードを再開するとデータが失われる可能性がある、またはチェックポイントが[<a href="https://github.com/pingcap/tiflow/issues/8242">#8242</a>](https://github.com/pingcap/tiflow/issues/8242) @ [<a href="https://github.com/overvenus">オーバーヴィーナス</a>](https://github.com/overvenus)進むことができないという問題を修正します。
        -   DDL シンク[<a href="https://github.com/pingcap/tiflow/issues/8238">#8238</a>](https://github.com/pingcap/tiflow/issues/8238) @ [<a href="https://github.com/3AceShowHand">3エースショーハンド</a>](https://github.com/3AceShowHand)のデータ競合の問題を修正
        -   `stopped`ステータスのチェンジフィードが自動的に[<a href="https://github.com/pingcap/tiflow/issues/8330">#8330</a>](https://github.com/pingcap/tiflow/issues/8330) @ [<a href="https://github.com/sdojjy">スドジ</a>](https://github.com/sdojjy)で再起動する場合がある問題を修正
        -   すべてのダウンストリーム Kafka サーバーが利用できない場合に TiCDCサーバーがパニックになる問題を修正[<a href="https://github.com/pingcap/tiflow/issues/8523">#8523</a>](https://github.com/pingcap/tiflow/issues/8523) @ [<a href="https://github.com/3AceShowHand">3エースショーハンド</a>](https://github.com/3AceShowHand)
        -   ダウンストリームが MySQL で、実行されたステートメントが TiDB [<a href="https://github.com/pingcap/tiflow/issues/8453">#8453</a>](https://github.com/pingcap/tiflow/issues/8453) @ [<a href="https://github.com/asddongmen">東門</a>](https://github.com/asddongmen)と互換性がない場合にデータが失われる可能性がある問題を修正
        -   ローリング アップグレードによって TiCDC OOM が発生する可能性があるか、チェックポイントが[<a href="https://github.com/pingcap/tiflow/issues/8329">#8329</a>](https://github.com/pingcap/tiflow/issues/8329) @ [<a href="https://github.com/overvenus">オーバーヴィーナス</a>](https://github.com/overvenus)でスタックする問題を修正します。
        -   Kubernetes [<a href="https://github.com/pingcap/tiflow/issues/8484">#8484</a>](https://github.com/pingcap/tiflow/issues/8484) @ [<a href="https://github.com/overvenus">オーバーヴィーナス</a>](https://github.com/overvenus)で TiCDC クラスターの正常なアップグレードが失敗する問題を修正

    -   TiDB データ移行 (DM)

        -   DM ワーカー ノードが Google Cloud Storage を使用する場合、ブレークポイントが頻繁すぎるため、Google Cloud Storage のリクエスト頻度制限に達し、DM ワーカーが Google Cloud Storage にデータを書き込むことができず、完全なデータの書き込みが失敗する問題を修正します。 [<a href="https://github.com/pingcap/tiflow/issues/8482">#8482</a>](https://github.com/pingcap/tiflow/issues/8482) @ [<a href="https://github.com/maxshuang">マックスシュアン</a>](https://github.com/maxshuang)をロードするには
        -   複数の DM タスクが同じダウンストリーム データを同時にレプリケートし、すべてがダウンストリーム メタデータ テーブルを使用してブレークポイント情報を記録する場合、すべてのタスクのブレークポイント情報が同じメタデータ テーブルに書き込まれ、同じタスク ID [<a href="https://github.com/pingcap/tiflow/issues/8500">#8500</a>](https://github.com/pingcap/tiflow/issues/8500)が使用される問題を修正します。 @ [<a href="https://github.com/maxshuang">マックスシュアン</a>](https://github.com/maxshuang)

    -   TiDB Lightning

        -   データのインポートに物理インポート モードが使用されている場合、ターゲット テーブルの複合主キーに`auto_random`の列が存在するが、その列の値がソース データで指定されていない場合、 TiDB Lightning がデータを生成しない問題を修正しました。 `auto_random`列の場合は自動的に[<a href="https://github.com/pingcap/tidb/issues/41454">#41454</a>](https://github.com/pingcap/tidb/issues/41454) @ [<a href="https://github.com/D3Hunter">D3ハンター</a>](https://github.com/D3Hunter)
        -   データのインポートに論理インポート モードが使用されている場合、ターゲット クラスター[<a href="https://github.com/pingcap/tidb/issues/41915">#41915</a>](https://github.com/pingcap/tidb/issues/41915) @ [<a href="https://github.com/lichunzhu">リチュンジュ</a>](https://github.com/lichunzhu)の`CONFIG`権限がないためにインポートが失敗する問題を修正します。

## 貢献者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   [<a href="https://github.com/AntiTopQuark">アンチトップクワーク</a>](https://github.com/AntiTopQuark)
-   [<a href="https://github.com/blacktear23">ブラックティア23</a>](https://github.com/blacktear23)
-   [<a href="https://github.com/BornChanger">ボーンチェンジャー</a>](https://github.com/BornChanger)
-   [<a href="https://github.com/Dousir9">ドゥーシール9</a>](https://github.com/Dousir9)
-   [<a href="https://github.com/erwadba">エルワドバ</a>](https://github.com/erwadba)
-   [<a href="https://github.com/HappyUncle">ハッピーアンクル</a>](https://github.com/HappyUncle)
-   [<a href="https://github.com/jiyfhust">ジフフスト</a>](https://github.com/jiyfhust)
-   [<a href="https://github.com/L-maple">L-カエデ</a>](https://github.com/L-maple)
-   [<a href="https://github.com/liumengya94">リウメンギャ94</a>](https://github.com/liumengya94)
-   [<a href="https://github.com/woofyzhao">ウーフィージャオ</a>](https://github.com/woofyzhao)
-   [<a href="https://github.com/xiaguan">夏関</a>](https://github.com/xiaguan)
