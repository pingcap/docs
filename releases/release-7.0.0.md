---
title: TiDB 7.0.0 Release Notes
summary: TiDB 7.0.0 の新機能、互換性の変更、改善、バグ修正について説明します。
---

# TiDB 7.0.0 リリースノート {#tidb-7-0-0-release-notes}

発売日: 2023年3月30日

TiDB バージョン: 7.0.0- [DMMR の](/releases/versioning.md#development-milestone-releases)

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.0/quick-start-with-tidb)

v7.0.0-DMR の主な新機能と改善点は次のとおりです。

<table><thead><tr><th>カテゴリ</th><th>特徴</th><th>説明</th></tr></thead><tbody><tr><td rowspan="2">スケーラビリティとパフォーマンス<br/></td><td>セッション レベルの<a href="https://docs.pingcap.com/tidb/v7.0/sql-non-prepared-plan-cache" target="_blank">非準備 SQL プラン キャッシュ</a>(実験的)</td><td>セッション レベルでプラン キャッシュを自動的に再利用することをサポートします。これにより、事前に準備ステートメントを手動で設定しなくても、コンパイルが削減され、同じ SQL パターンのクエリ時間が短縮されます。</td></tr><tr><td> TiFlash は<a href="https://docs.pingcap.com/tidb/v7.0/tiflash-disaggregated-and-s3" target="_blank">、分散storageとコンピューティングアーキテクチャ、および S3 共有storage</a>(実験的) をサポートします。</td><td> TiFlash は、オプションとしてクラウドネイティブアーキテクチャを導入します。<ul><li> TiFlash のコンピューティングとstorageを分離します。これは、弾力的な HTAP リソース利用のマイルストーンです。</li><li>低コストで共有storageを提供できる S3 ベースのstorageエンジンを導入します。</li></ul></td></tr><tr><td rowspan="2">信頼性と可用性<br/></td><td><a href="https://docs.pingcap.com/tidb/v7.0/tidb-resource-control" target="_blank">リソース制御の強化</a>（実験的）</td><td>リソース グループを使用して、1 つのクラスター内のさまざまなアプリケーションまたはワークロードのリソースを割り当て、分離することをサポートします。このリリースでは、TiDB はさまざまなリソース バインディング モード (ユーザー、セッション、ステートメント レベル) とユーザー定義の優先順位のサポートを追加します。さらに、コマンドを使用してリソース調整 (全体のリソース量の推定) を実行することもできます。</td></tr><tr><td> TiFlashは<a href="https://docs.pingcap.com/tidb/v7.0/tiflash-spill-disk" target="_blank">ディスクへの書き込み</a>をサポート</td><td>TiFlash は、集約、ソート、ハッシュ結合などのデータ集約型操作における OOM を軽減するために、ディスクへの中間結果のスピルをサポートします。</td></tr><tr><td rowspan="2">構文</td><td><a href="https://docs.pingcap.com/tidb/v7.0/time-to-live" target="_blank">行レベルの TTL</a> (GA)</td><td>一定の期間が経過したデータを自動的に期限切れにすることで、データベース サイズの管理をサポートし、パフォーマンスを向上します。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v7.0/partitioned-table#reorganize-partitions" target="_blank"><code>LIST</code> / <code>RANGE</code>パーティションの再編成</a></td><td><code>REORGANIZE PARTITION</code>ステートメントは、隣接するパーティションをマージしたり、1 つのパーティションを複数のパーティションに分割したりするために使用でき、パーティション化されたテーブルの使いやすさが向上します。</td></tr><tr><td rowspan="2"> DB 操作と可観測性<br/></td><td>TiDB は<a href="https://docs.pingcap.com/tidb/v7.0/sql-statement-load-data" target="_blank"><code>LOAD DATA</code>ステートメント</a>の機能を強化します (実験的)</td><td> TiDB は、S3/GCS からのデータ インポートのサポートなど、 <code>LOAD DATA</code> SQL ステートメントの機能を強化します。<br/></td></tr><tr><td> TiCDC は<a href="https://docs.pingcap.com/tidb/v7.0/ticdc-sink-to-cloud-storage" target="_blank">オブジェクトstorageシンク</a>(GA) をサポートします</td><td>TiCDC は、Amazon S3、GCS、Azure Blob Storage、NFS などのオブジェクトstorageサービスへの行変更イベントの複製をサポートしています。<br/></td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### スケーラビリティ {#scalability}

-   TiFlash は分散storageとコンピューティングアーキテクチャをサポートし、このアーキテクチャでオブジェクトstorageをサポートします (実験的) [＃6882](https://github.com/pingcap/tiflash/issues/6882) @ [フロービーハッピー](https://github.com/flowbehappy)

    v7.0.0 より前のTiFlashでは、結合storageおよびコンピューティングアーキテクチャのみがサポートされていました。このアーキテクチャでは、各TiFlashノードはstorageとコンピューティング ノードの両方として機能し、コンピューティング機能とstorage機能を個別に拡張することはできません。また、 TiFlashノードはローカルstorageのみを使用できます。

    v7.0.0 以降、 TiFlash は分散storageおよびコンピューティングアーキテクチャもサポートします。このアーキテクチャでは、 TiFlashノードは 2 つのタイプ (コンピューティング ノードと書き込みノード) に分かれており、S3 API と互換性のあるオブジェクトstorageをサポートします。両方のタイプのノードは、コンピューティングまたはstorage容量に合わせて個別にスケーリングできます。**分散storageおよびコンピューティングアーキテクチャ**と**結合storageおよびコンピューティングアーキテクチャは、**同じクラスター内で使用したり、相互に変換したりすることはできません。TiFlashをデプロイするときに、使用するアーキテクチャを構成できます。

    詳細については[ドキュメント](/tiflash/tiflash-disaggregated-and-s3.md)参照してください。

### パフォーマンス {#performance}

-   高速オンラインDDLとPITR [＃38045](https://github.com/pingcap/tidb/issues/38045) @ [リーヴルス](https://github.com/Leavrth)間の互換性を実現

    TiDB v6.5.0 では、 [高速オンラインDDL](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) [ピトル](/br/backup-and-restore-overview.md)と完全に互換性がありません。完全なデータ バックアップを確実に行うには、まず PITR バックグラウンド バックアップ タスクを停止し、Fast Online DDL を使用してインデックスをすばやく追加してから、PITR バックアップ タスクを再開することをお勧めします。

    TiDB v7.0.0 以降、Fast Online DDL と PITR は完全に互換性があります。PITR を介してクラスター データを復元する場合、ログ バックアップ中に Fast Online DDL によって追加されたインデックス操作は、互換性を実現するために自動的に再生されます。

    詳細については[ドキュメント](/ddl-introduction.md)参照してください。

-   TiFlash は、null 認識のセミ結合演算子と null 認識のアンチセミ結合演算子[＃6674](https://github.com/pingcap/tiflash/issues/6674) @ [ゲンリキ](https://github.com/gengliqi)をサポートしています。

    相関サブクエリで`IN` 、 `NOT IN` 、 `= ANY` 、または`!= ALL`演算子を使用する場合、TiDB はそれらをセミ結合またはアンチセミ結合に変換して計算パフォーマンスを最適化します。結合キー列が`NULL`になる可能性がある場合は、 [Null 認識セミ結合](/explain-subqueries.md#null-aware-semi-join-in-and--any-subqueries)や[Null 認識アンチセミ結合](/explain-subqueries.md#null-aware-anti-semi-join-not-in-and--all-subqueries)などの null 認識結合アルゴリズムが必要です。

    v7.0.0 より前のTiFlash、null 対応のセミ結合演算子と null 対応のアンチ セミ結合演算子がサポートされていないため、これらのサブクエリがTiFlashに直接プッシュダウンされませんでした。v7.0.0 以降、 TiFlashnull 対応のセミ結合演算子と null 対応のアンチ セミ結合演算子がサポートされます。SQL ステートメントにこれらの相関サブクエリが含まれ、クエリ内のテーブルにTiFlashレプリカがあり、 [MPPモード](/tiflash/use-tiflash-mpp-mode.md)が有効になっている場合、オプティマイザーは、全体的なパフォーマンスを向上させるために、null 対応のセミ結合演算子と null 対応のアンチ セミ結合演算子をTiFlashにプッシュダウンするかどうかを自動的に決定します。

    詳細については[ドキュメント](/tiflash/tiflash-supported-pushdown-calculations.md)参照してください。

-   TiFlashはFastScan (GA) [＃5252](https://github.com/pingcap/tiflash/issues/5252) @ [ホンユンヤン](https://github.com/hongyunyan)の使用をサポートします

    v6.3.0 以降、 TiFlash はFastScan を実験的機能として導入しました。v7.0.0 では、この機能が一般公開されます。システム変数[`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-new-in-v630)使用して FastScan を有効にすることができます。この機能は、強力な一貫性を犠牲にすることで、テーブル`DELETE` `UPDATE`がなく`INSERT`操作のみが含まれる場合、FastScan は強力な一貫性を維持し、スキャン パフォーマンスを向上させることができます。

    詳細については[ドキュメント](/tiflash/use-fastscan.md)参照してください。

-   TiFlash は遅延マテリアライゼーションをサポートします (実験的) [＃5829](https://github.com/pingcap/tiflash/issues/5829) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)

    フィルター条件 ( `WHERE`句 ) を含む`SELECT`ステートメントを処理する場合、 TiFlash はデフォルトでクエリに必要な列からすべてのデータを読み取り、クエリ条件に基づいてデータをフィルターして集計します。遅延マテリアライゼーションは、フィルター条件の一部を TableScan 演算子にプッシュダウンすることをサポートする最適化方法です。つまり、 TiFlash は最初にプッシュダウンされたフィルター条件に関連する列データをスキャンし、条件を満たす行をフィルターしてから、これらの行の他の列データをスキャンしてさらに計算することで、データ処理の IO スキャンと計算を削減します。

    TiFlash の遅延マテリアライゼーション機能は、デフォルトでは有効になっていません。 `tidb_opt_enable_late_materialization`システム変数を`OFF`に設定することで、この機能を有効にすることができます。この機能を有効にすると、TiDB オプティマイザーは統計とフィルター条件に基づいて、プッシュダウンするフィルター条件を決定します。

    詳細については[ドキュメント](/tiflash/tiflash-late-materialization.md)参照してください。

-   非準備済みステートメントの実行プランのキャッシュをサポート (実験的) [＃36598](https://github.com/pingcap/tidb/issues/36598) @ [qw4990](https://github.com/qw4990)

    実行プラン キャッシュは、同時実行 OLTP の負荷容量を向上させるために重要であり、TiDB はすでに[準備された実行計画キャッシュ](/sql-prepared-plan-cache.md)サポートしています。v7.0.0 では、TiDB は非 Prepare ステートメントの実行プランもキャッシュできるようになり、実行プラン キャッシュの範囲が拡大され、TiDB の同時処理容量が向上しました。

    この機能はデフォルトでは無効になっています。システム変数[`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache)を`ON`に設定することで有効にできます。安定性の理由から、TiDB v7.0.0 では準備されていない実行プランをキャッシュするための新しい領域が割り当てられており、システム変数[`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size)使用してキャッシュ サイズを設定できます。また、この機能には SQL ステートメントに対する特定の制限があります。詳細については、 [制限](/sql-non-prepared-plan-cache.md#restrictions)参照してください。

    詳細については[ドキュメント](/sql-non-prepared-plan-cache.md)参照してください。

-   TiDBはサブクエリ[#40219](https://github.com/pingcap/tidb/issues/40219) @ [ふーふー](https://github.com/fzzf678)の実行プランキャッシュ制約を削除します。

    TiDB v7.0.0 では、サブクエリの実行プラン キャッシュ制約が削除されました。つまり、 `SELECT * FROM t WHERE a > (SELECT ...)`のように、サブクエリを含む SQL ステートメントの実行プランをキャッシュできるようになりました。この機能により、実行プラン キャッシュの適用範囲がさらに広がり、SQL クエリの実行効率が向上します。

    詳細については[ドキュメント](/sql-prepared-plan-cache.md)参照してください。

-   TiKV は、ログリサイクル[＃14371](https://github.com/tikv/tikv/issues/14371) @ [リクササシネーター](https://github.com/LykxSassinator)用の空のログファイルの自動生成をサポートします。

    v6.3.0 では、TiKV は書き込み負荷によって発生するロングテールレイテンシーを削減する[Raft丸太リサイクル](/tikv-configuration-file.md#enable-log-recycle-new-in-v630)機能を導入しました。ただし、ログのリサイクルはRaftログ ファイルの数が一定のしきい値に達した場合にのみ有効になるため、ユーザーがこの機能によってもたらされるスループットの向上を直接体験することは困難です。

    v7.0.0 では、ユーザー エクスペリエンスを向上させるために、 `raft-engine.prefill-for-recycle`という新しい構成項目が導入されました。この項目は、プロセスの開始時にリサイクル用に空のログ ファイルを生成するかどうかを制御します。この構成を有効にすると、TiKV は初期化中に空のログ ファイルのバッチを自動的に埋め、初期化後すぐにログのリサイクルが有効になるようにします。

    詳細については[ドキュメント](/tikv-configuration-file.md#prefill-for-recycle-new-in-v700)参照してください。

-   ウィンドウ関数のパフォーマンスを向上させるために、TopN または Limit 演算子を[ウィンドウ関数](/functions-and-operators/expressions-pushed-down.md)から導出するサポート[＃13936](https://github.com/tikv/tikv/issues/13936) @ [風の話し手](https://github.com/windtalker)

    この機能はデフォルトでは無効になっています。有効にするには、セッション変数[tidb_opt_derive_topn](/system-variables.md#tidb_opt_derive_topn-new-in-v700)を`ON`に設定します。

    詳細については[ドキュメント](/derive-topn-from-window.md)参照してください。

-   高速オンライン DDL [＃40730](https://github.com/pingcap/tidb/issues/40730) @ [タンジェンタ](https://github.com/tangenta)による一意のインデックスの作成をサポート

    TiDB v6.5.0 は、Fast Online DDL による通常のセカンダリ インデックスの作成をサポートしています。TiDB v7.0.0 は、Fast Online DDL による一意のインデックスの作成をサポートしています。v6.1.0 と比較すると、大規模なテーブルに一意のインデックスを追加すると、パフォーマンスが向上し、数倍高速化されることが期待されます。

    詳細については[ドキュメント](/ddl-introduction.md)参照してください。

### 信頼性 {#reliability}

-   リソース制御機能の強化 (実験的) [＃38825](https://github.com/pingcap/tidb/issues/38825) @ [ノルーシュ](https://github.com/nolouch) @ [ボーンチェンジャー](https://github.com/BornChanger) @ [栄光](https://github.com/glorv) @ [天菜まお](https://github.com/tiancaiamao) @ [コナー1996](https://github.com/Connor1996) @ [じゃがいも](https://github.com/JmPotato) @ [ネス](https://github.com/hnes) @ [キャビンフィーバーB](https://github.com/CabinfeverB) @ [ヒューシャープ](https://github.com/HuSharp)

    TiDB は、リソース グループに基づくリソース制御機能を強化しました。この機能により、TiDB クラスターのリソース利用効率とパフォーマンスが大幅に向上します。リソース制御機能の導入は、TiDB にとって画期的な出来事です。分散データベース クラスターを複数の論理ユニットに分割し、異なるデータベース ユーザーを対応するリソース グループにマップし、必要に応じて各リソース グループのクォータを設定できます。クラスター リソースが制限されている場合、同じリソース グループ内のセッションで使用されるすべてのリソースはクォータに制限されます。このようにして、リソース グループが過剰に消費されても、他のリソース グループのセッションには影響しません。

    この機能により、異なるシステムの複数の中小規模のアプリケーションを 1 つの TiDB クラスターに統合できます。アプリケーションのワークロードが大きくなっても、他のアプリケーションの正常な動作には影響しません。システムのワークロードが低い場合は、設定されたクォータを超えても、ビジー状態のアプリケーションに必要なシステム リソースを割り当てることができるため、リソースを最大限に活用できます。さらに、リソース制御機能を合理的に使用すると、クラスターの数を減らし、運用と保守の難しさを軽減し、管理コストを節約できます。

    この機能は、Grafana のリソースの実際の使用状況を表示する組み込みのリソース コントロール ダッシュボードを提供し、リソースをより合理的に割り当てるのに役立ちます。また、セッション レベルとステートメント レベルの両方に基づく動的なリソース管理機能もサポートしています (ヒント)。この機能の導入により、TiDB クラスターのリソース使用状況をより正確に制御し、実際のニーズに基づいてクォータを動的に調整できるようになります。

    TiDB v7.0.0 では、リソース グループに絶対的なスケジュール優先度 ( `PRIORITY` ) を設定して、重要なサービスがリソースを取得できることを保証できます。また、リソース グループの設定方法も拡張されます。

    リソース グループは次の方法で使用できます。

    -   ユーザー レベル[`CREATE USER`](/sql-statements/sql-statement-create-user.md)または[`ALTER USER`](/sql-statements/sql-statement-alter-user.md)ステートメントを使用して、ユーザーを特定のリソース グループにバインドします。リソース グループをユーザーにバインドすると、ユーザーによって新しく作成されたセッションは、対応するリソース グループに自動的にバインドされます。
    -   セッション レベル。 [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md)を介して現在のセッションで使用されるリソース グループを設定します。
    -   ステートメント レベル。 [`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name)を介して現在のステートメントで使用されるリソース グループを設定します。

    詳細については[ドキュメント](/tidb-resource-control.md)参照してください。

-   高速オンラインDDLのチェックポイントメカニズムをサポートし、フォールトトレランスと自動リカバリ機能を向上させます[＃42164](https://github.com/pingcap/tidb/issues/42164) @ [タンジェンタ](https://github.com/tangenta)

    TiDB v7.0.0 では、 [高速オンラインDDL](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)のチェックポイント メカニズムが導入され、フォールト トレランスと自動リカバリ機能が大幅に向上しました。DDL の進行状況を定期的に記録して同期することで、TiDB DDL 所有者に障害が発生したり、切り替えがあったりしても、進行中の DDL 操作を高速オンライン DDL モードで引き続き実行できます。これにより、DDL の実行がより安定して効率的になります。

    詳細については[ドキュメント](/ddl-introduction.md)参照してください。

-   TiFlashはディスク[＃6528](https://github.com/pingcap/tiflash/issues/6528) @ [風の話し手](https://github.com/windtalker)へのスピルをサポート

    実行パフォーマンスを向上させるために、 TiFlash は可能な限りデータ全体をメモリ内で実行します。データ量がメモリの合計サイズを超えると、メモリ不足によるシステムクラッシュを回避するために、 TiFlash はクエリを終了します。したがって、 TiFlash が処理できるデータ量は、使用可能なメモリによって制限されます。

    v7.0.0 以降、 TiFlash はディスクへの書き込みをサポートします。演算子のメモリ使用量のしきい値 ( [`tidb_max_bytes_before_tiflash_external_group_by`](/system-variables.md#tidb_max_bytes_before_tiflash_external_group_by-new-in-v700) 、 [`tidb_max_bytes_before_tiflash_external_sort`](/system-variables.md#tidb_max_bytes_before_tiflash_external_sort-new-in-v700) 、および[`tidb_max_bytes_before_tiflash_external_join`](/system-variables.md#tidb_max_bytes_before_tiflash_external_join-new-in-v700) ) を調整することで、演算子が使用できるメモリの最大量を制御できます。演算子によって使用されるメモリがしきい値を超えると、自動的にデータがディスクに書き込まれます。これにより、パフォーマンスが多少犠牲になりますが、より多くのデータを処理できるようになります。

    詳細については[ドキュメント](/tiflash/tiflash-spill-disk.md)参照してください。

-   統計収集の効率を向上[＃41930](https://github.com/pingcap/tidb/issues/41930) @ [翻訳者](https://github.com/xuyifangreeneyes)

    v7.0.0 では、TiDB は統計収集のロジックをさらに最適化し、収集時間を約 25% 短縮しました。この最適化により、大規模なデータベース クラスターの運用効率と安定性が向上し、統計収集がクラスターのパフォーマンスに与える影響が軽減されます。

-   MPP 最適化[＃39710](https://github.com/pingcap/tidb/issues/39710) @ [思い出させる](https://github.com/Reminiscent)の新しいオプティマイザーヒントを追加します

    v7.0.0 では、TiDB は MPP 実行プランの生成に影響を与える一連のオプティマイザーヒントを追加します。

    -   [`SHUFFLE_JOIN()`](/optimizer-hints.md#shuffle_joint1_name--tl_name-) : MPP に有効になります。指定されたテーブルに対して Shuffle Join アルゴリズムを使用するようにオプティマイザに指示します。
    -   [`BROADCAST_JOIN()`](/optimizer-hints.md#broadcast_joint1_name--tl_name-) : MPP に有効です。指定されたテーブルに対してブロードキャスト結合アルゴリズムを使用するようにオプティマイザに指示します。
    -   [`MPP_1PHASE_AGG()`](/optimizer-hints.md#mpp_1phase_agg) : MPP に有効です。指定されたクエリ ブロック内のすべての集計関数に対して 1 フェーズ集計アルゴリズムを使用するようにオプティマイザに指示します。
    -   [`MPP_2PHASE_AGG()`](/optimizer-hints.md#mpp_2phase_agg) : MPP に有効です。指定されたクエリ ブロック内のすべての集計関数に対して 2 フェーズ集計アルゴリズムを使用するようにオプティマイザに指示します。

    MPP オプティマイザーヒントは、HTAP クエリに介入して、HTAP ワークロードのパフォーマンスと安定性を向上させるのに役立ちます。

    詳細については[ドキュメント](/optimizer-hints.md)参照してください。

-   オプティマイザヒントは結合方法と結合順序の指定をサポートします[＃36600](https://github.com/pingcap/tidb/issues/36600) @ [思い出させる](https://github.com/Reminiscent)

    v7.0.0 では、オプティマイザ ヒント[`LEADING()`](/optimizer-hints.md#leadingt1_name--tl_name-)は結合方法に影響を与えるヒントと組み合わせて使用でき、それらの動作は互換性があります。複数テーブルの結合の場合、最適な結合方法と結合順序を効果的に指定できるため、実行プランに対するオプティマイザ ヒントの制御が強化されます。

    新しいヒントの動作には、若干の変更があります。前方互換性を確保するために、TiDB ではシステム変数[`tidb_opt_advanced_join_hint`](/system-variables.md#tidb_opt_advanced_join_hint-new-in-v700)が導入されています。この変数を`OFF`に設定すると、オプティマイザーのヒント動作は以前のバージョンと互換性があります。クラスターを以前のバージョンから v7.0.0 以降のバージョンにアップグレードすると、この変数は`OFF`に設定されます。より柔軟なヒント動作を得るには、動作によってパフォーマンスの低下が発生しないことを確認した後、この変数を`ON`に設定することを強くお勧めします。

    詳細については[ドキュメント](/optimizer-hints.md)参照してください。

### 可用性 {#availability}

-   `prefer-leader`オプションをサポートすることで、読み取り操作の可用性が向上し、不安定なネットワーク状況での応答レイテンシーが短縮されます[＃40905](https://github.com/pingcap/tidb/issues/40905) @ [リクササシネーター](https://github.com/LykxSassinator)

    システム変数[`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40)を通じて、TiDB のデータ読み取り動作を制御できます。v7.0.0 では、この変数に`prefer-leader`オプションが追加されました。変数が`prefer-leader`に設定されている場合、TiDB はリーダー レプリカを選択して読み取り操作を実行することを優先します。ディスクまたはネットワーク パフォーマンスの変動などにより、リーダー レプリカの処理速度が大幅に低下した場合、TiDB は他の利用可能なフォロワー レプリカを選択して読み取り操作を実行し、可用性を高め、応答のレイテンシーを短縮します。

    詳細については[ドキュメント](/develop/dev-guide-use-follower-read.md)参照してください。

### 構文 {#sql}

-   有効期間（TTL）は一般に[＃39262](https://github.com/pingcap/tidb/issues/39262) @ [lcwangchao](https://github.com/lcwangchao) @ [ヤンケオ](https://github.com/YangKeao)で利用可能

    TTL は行レベルのライフサイクル制御ポリシーを提供します。TiDB では、TTL 属性が設定されたテーブルは、構成に基づいて期限切れの行データを自動的にチェックして削除します。TTL の目的は、クラスターのワークロードへの影響を最小限に抑えながら、ユーザーが不要なデータを定期的にクリーンアップできるようにすることです。

    詳細については[ドキュメント](/time-to-live.md)参照してください。

-   サポート`ALTER TABLE…REORGANIZE PARTITION` [＃15000](https://github.com/pingcap/tidb/issues/15000) @ [ミョンス](https://github.com/mjonss)

    TiDB は`ALTER TABLE...REORGANIZE PARTITION`構文をサポートしています。この構文を使用すると、データを失うことなく、テーブルのパーティションの一部またはすべてを再編成し、マージ、分割、その他の変更を行うことができます。

    詳細については[ドキュメント](/partitioned-table.md#reorganize-partitions)参照してください。

-   キー分割[＃41364](https://github.com/pingcap/tidb/issues/41364) @ [トンスネークリン](https://github.com/TonsnakeLin)をサポート

    現在、TiDB はキー パーティション分割をサポートしています。キー パーティション分割とハッシュ パーティション分割はどちらも、データを一定数のパーティションに均等に分散できます。違いは、ハッシュ パーティション分割では指定された整数式または整数列に基づくデータの分散のみがサポートされるのに対し、キー パーティション分割では列リストに基づくデータの分散がサポートされ、キー パーティション分割の列のパーティション分割は整数型に制限されないことです。

    詳細については[ドキュメント](/partitioned-table.md#key-partitioning)参照してください。

### DB操作 {#db-operations}

-   TiCDC は変更データをstorageサービスに複製することをサポートします (GA) [＃6797](https://github.com/pingcap/tiflow/issues/6797) @ [趙新宇](https://github.com/zhaoxinyu)

    TiCDC は、Amazon S3、GCS、Azure Blob Storage、NFS、およびその他の S3 互換storageサービスへの変更データのレプリケーションをサポートしています。ストレージ サービスは価格が手頃で使いやすいです。Kafka を使用していない場合は、storageサービスを使用できます。TiCDC は変更されたログをファイルに保存し、代わりにstorageサービスに送信します。storageサービスから、独自のコンシューマー プログラムは、新しく生成された変更されたログ ファイルを定期的に読み取ることができます。現在、TiCDC は、canal-json および CSV 形式で変更されたログをstorageサービスにレプリケーションすることをサポートしています。

    詳細については[ドキュメント](/ticdc/ticdc-sink-to-cloud-storage.md)参照してください。

-   TiCDC オープン API v2 [＃8019](https://github.com/pingcap/tiflow/issues/8019) @ [スドジ](https://github.com/sdojjy)

    TiCDC は OpenAPI v2 を提供します。OpenAPI v1 と比較して、OpenAPI v2 はレプリケーション タスクに対するより包括的なサポートを提供します。TiCDC OpenAPI によって提供される機能は、 [`cdc cli`ツール](/ticdc/ticdc-manage-changefeed.md)のサブセットです。TiCDC ノードのステータスの取得、クラスターのヘルス ステータスの確認、レプリケーション タスクの管理など、OpenAPI v2 を介して TiCDC クラスターを照会および操作できます。

    詳細については[ドキュメント](/ticdc/ticdc-open-api-v2.md)参照してください。

-   [DBeaver](https://dbeaver.io/) v23.0.1 はデフォルトで TiDB をサポートします[＃17396](https://github.com/dbeaver/dbeaver/issues/17396) @ [アイスマップ](https://github.com/Icemap)

    -   独立した TiDB モジュール、アイコン、ロゴを提供します。
    -   デフォルト構成では[TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)サポートされているため、 TiDB Cloud Serverless への接続が容易になります。
    -   外部キー タブを表示または非表示にするために TiDB のバージョンを識別することをサポートします。
    -   `EXPLAIN`結果で SQL 実行プランの視覚化をサポートします。
    -   `PESSIMISTIC` `EXCHANGE` `CACHE` TiDB `CLUSTERED` `OPTIMISTIC`強調`AUTO_RANDOM`を`PLACEMENT` `REORGANIZE` `POLICY` `NONCLUSTERED`
    -   `TIDB_BOUNDED_STALENESS`など`TIDB_DECODE_SQL_DIGESTS` TiDB関数の`TIDB_SHARD` `TIDB_DECODE_PLAN` `TIDB_DECODE_KEY` `TIDB_IS_DDL_OWNER` `TIDB_VERSION` `TIDB_PARSE_TSO` 。

    詳細については[DBeaver ドキュメント](https://github.com/dbeaver/dbeaver/wiki)参照してください。

### データ移行 {#data-migration}

-   `LOAD DATA`ステートメントの機能を強化し、クラウドstorageからのデータのインポートをサポートします (実験的) [＃40499](https://github.com/pingcap/tidb/issues/40499) @ [ランス6716](https://github.com/lance6716)

    TiDB v7.0.0 より前では、 `LOAD DATA`ステートメントはクライアント側からデータ ファイルをインポートすることしかできませんでした。クラウドstorageからデータをインポートしたい場合は、 TiDB Lightningに頼る必要がありました。ただし、 TiDB Lightning を個別に導入すると、導入コストと管理コストが追加されます。v7.0.0 では、 `LOAD DATA`ステートメントを使用してクラウドstorageからデータを直接インポートできます。機能の例をいくつか示します。

    -   Amazon S3 および Google Cloud Storage から TiDB へのデータのインポートをサポートします。ワイルドカードを使用して、複数のソース ファイルを一度に TiDB にインポートすることをサポートします。
    -   `DEFINED NULL BY`使用して null を定義することをサポートします。
    -   CSV および TSV 形式のソース ファイルをサポートします。

    詳細については[ドキュメント](/sql-statements/sql-statement-load-data.md)参照してください。

-   TiDB Lightning は、TiKV (GA) [＃41163](https://github.com/pingcap/tidb/issues/41163) @ [眠いモグラ](https://github.com/sleepymole)にキーと値のペアを送信するときに圧縮転送を有効にすることをサポートします。

    v6.6.0 以降、 TiDB Lightning は、ローカルでエンコードされ、ソートされたキーと値のペアを TiKV に送信する際にネットワーク転送用に圧縮することをサポートしています。これにより、ネットワーク経由で転送されるデータの量が削減され、ネットワーク帯域幅のオーバーヘッドが低減されます。この機能がサポートされる前の TiDB バージョンでは、 TiDB Lightning は比較的高いネットワーク帯域幅を必要とし、大量のデータを扱う場合には高いトラフィック料金が発生します。

    v7.0.0 ではこの機能は GA となり、デフォルトでは無効になっています。有効にするには、 TiDB Lightningの`compress-kv-pairs`構成項目を`"gzip"`または`"gz"`に設定します。

    詳細については[ドキュメント](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)参照してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、v6.6.0 から現在のバージョン (v7.0.0) にアップグレードするときに知っておく必要のある互換性の変更について説明します。v6.5.0 以前のバージョンから現在のバージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更も確認する必要がある可能性があります。

### MySQL 互換性 {#mysql-compatibility}

-   TiDBは、自動インクリメント列がインデックス[＃40580](https://github.com/pingcap/tidb/issues/40580) @ [天菜まお](https://github.com/tiancaiamao)でなければならないという制約を削除します。

    v7.0.0 より前の TiDB の動作は MySQL と一致しており、自動インクリメント列はインデックスまたはインデックス プレフィックスである必要があります。v7.0.0 以降、TiDB は自動インクリメント列がインデックスまたはインデックス プレフィックスでなければならないという制約を削除します。これで、テーブルの主キーをより柔軟に定義し、自動インクリメント列を使用して並べ替えとページネーションをより便利に実装できます。これにより、自動インクリメント列によって発生する書き込みホットスポットの問題も回避され、クラスター化インデックスを持つテーブルを使用することでクエリ パフォーマンスが向上します。新しいリリースでは、次の構文を使用してテーブルを作成できます。

    ```sql
    CREATE TABLE test1 (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `k` int(11) NOT NULL DEFAULT '0',
        `c` char(120) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
        PRIMARY KEY(`k`, `id`)
    );
    ```

    この機能は TiCDC データ レプリケーションには影響しません。

    詳細については[ドキュメント](/mysql-compatibility.md#auto-increment-id)参照してください。

-   TiDB は、次の例に示すように、キー パーティションをサポートしています。

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

    v7.0.0 以降、TiDB はキー パーティションをサポートし、MySQL `PARTITION BY LINEAR KEY`構文を解析できます。ただし、TiDB は`LINEAR`キーワードを無視し、代わりに非線形ハッシュ アルゴリズムを使用します。現在、 `KEY`パーティション タイプは、パーティション列リストが空のパーティション ステートメントをサポートしていません。

    詳細については[ドキュメント](/partitioned-table.md#key-partitioning)参照してください。

### 行動の変化 {#behavior-changes}

-   TiCDC は、Avro [＃8490](https://github.com/pingcap/tiflow/issues/8490) @ [3エースショーハンド](https://github.com/3AceShowHand)の`FLOAT`データのエンコードが正しくない問題を修正しました。

    TiCDC クラスターを v7.0.0 にアップグレードするときに、Avro を使用してレプリケートされたテーブルに`FLOAT`データ型が含まれている場合は、アップグレードする前に、Confluent Schema Registry の互換性ポリシーを手動で`None`に調整して、changefeed がスキーマを正常に更新できるようにする必要があります。そうしないと、アップグレード後に changefeed がスキーマを更新できず、エラー状態になります。

-   v7.0.0 以降、 [`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size)システム変数は[`LOAD DATA`ステートメント](/sql-statements/sql-statement-load-data.md)では有効になりません。

### システム変数 {#system-variables}

| 変数名                                                                                                                               | タイプを変更   | 説明                                                                                                                                                                                           |
| --------------------------------------------------------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `tidb_pessimistic_txn_aggressive_locking`                                                                                         | 削除されました  | この変数の名前は[`tidb_pessimistic_txn_fair_locking`](/system-variables.md#tidb_pessimistic_txn_fair_locking-new-in-v700)に変更されます。                                                                    |
| [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache)                                 | 修正済み     | v7.0.0 以降で有効になり、 [準備されていないプラン キャッシュ](/sql-non-prepared-plan-cache.md)機能を有効にするかどうかを制御します。                                                                                                     |
| [`tidb_enable_null_aware_anti_join`](/system-variables.md#tidb_enable_null_aware_anti_join-new-in-v630)                           | 修正済み     | さらにテストを行った後、デフォルト値を`OFF`から`ON`に変更します。つまり、デフォルトで特殊なセット演算子`NOT IN`および`!= ALL`によって導かれるサブクエリによって Anti Join が生成される場合、TiDB は Null 対応ハッシュ結合を適用します。                                                  |
| [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660)                                   | 修正済み     | デフォルト値を`OFF`から`ON`に変更します。これは、クラスターがデフォルトでリソース グループごとにリソースを分離することを意味します。リソース制御はバージョン 7.0.0 ではデフォルトで有効になっているため、いつでもこの機能を使用できます。                                                                |
| [`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size)                                     | 修正済み     | v7.0.0 から有効になり、キャッシュできる実行プランの最大数を[準備されていないプラン キャッシュ](/sql-non-prepared-plan-cache.md)で制御します。                                                                                                 |
| [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-new-in-v600)                                                 | 修正済み     | v7.0.0 以降、この変数はプリペアドステートメントプロトコルのカーソル フェッチ読み取りには効果がありません。                                                                                                                                    |
| [`tidb_enable_inl_join_inner_multi_pattern`](/system-variables.md#tidb_enable_inl_join_inner_multi_pattern-new-in-v700)           | 新しく追加された | この変数は、内部テーブルに`Selection`または`Projection`演算子がある場合にインデックス結合がサポートされるかどうかを制御します。                                                                                                                  |
| [`tidb_enable_plan_cache_for_subquery`](/system-variables.md#tidb_enable_plan_cache_for_subquery-new-in-v700)                     | 新しく追加された | この変数は、プリペアドプランキャッシュがサブクエリを含むクエリをキャッシュするかどうかを制御します。                                                                                                                                           |
| [`tidb_enable_plan_replayer_continuous_capture`](/system-variables.md#tidb_enable_plan_replayer_continuous_capture-new-in-v700)   | 新しく追加された | この変数は、 [`PLAN REPLAYER CONTINUOUS CAPTURE`](/sql-plan-replayer.md#use-plan-replayer-continuous-capture)機能を有効にするかどうかを制御します。デフォルト値`OFF` 、機能を無効にすることを意味します。                                     |
| [`tidb_load_based_replica_read_threshold`](/system-variables.md#tidb_load_based_replica_read_threshold-new-in-v700)               | 新しく追加された | この変数は、負荷ベースのレプリカ読み取りをトリガーするためのしきい値を設定します。この変数によって制御される機能は、TiDB v7.0.0 では完全には機能しません。デフォルト値を変更しないでください。                                                                                        |
| [`tidb_opt_advanced_join_hint`](/system-variables.md#tidb_opt_advanced_join_hint-new-in-v700)                                     | 新しく追加された | この変数は、結合方法のヒントが結合順序の最適化に影響を与えるかどうかを制御します。デフォルト値は`ON`で、新しい互換性のある制御モードが使用されることを意味します。値`OFF`は、v7.0.0 より前の動作が使用されることを意味します。前方互換性のために、クラスターが以前のバージョンから v7.0.0 以降にアップグレードされると、この変数の値は`OFF`に設定されます。 |
| [`tidb_opt_derive_topn`](/system-variables.md#tidb_opt_derive_topn-new-in-v700)                                                   | 新しく追加された | この変数は、 [ウィンドウ関数から TopN または Limit を導出する](/derive-topn-from-window.md)最適化ルールを有効にするかどうかを制御します。デフォルト値は`OFF`で、最適化ルールが有効になっていないことを意味します。                                                           |
| [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-new-in-v700)                   | 新しく追加された | この変数は、 [TiFlash後期実体化](/tiflash/tiflash-late-materialization.md)機能を有効にするかどうかを制御します。デフォルト値は`OFF`で、これは機能が無効であることを意味します。                                                                         |
| [`tidb_opt_ordering_index_selectivity_threshold`](/system-variables.md#tidb_opt_ordering_index_selectivity_threshold-new-in-v700) | 新しく追加された | この変数は、SQL ステートメントに`ORDER BY`および`LIMIT`句が含まれ、フィルタリング条件がある場合に、オプティマイザーがインデックスを選択する方法を制御します。                                                                                                    |
| [`tidb_pessimistic_txn_fair_locking`](/system-variables.md#tidb_pessimistic_txn_fair_locking-new-in-v700)                         | 新しく追加された | 単一行の競合シナリオでトランザクションの末尾のレイテンシーを削減するために、拡張された悲観的ロック ウェイク モデルを有効にするかどうかを制御します。デフォルト値は`ON`です。クラスターが以前のバージョンから v7.0.0 以降にアップグレードされると、この変数の値は`OFF`に設定されます。                                         |
| [`tidb_slow_txn_log_threshold`](/system-variables.md#tidb_slow_txn_log_threshold-new-in-v700)                                     | 新しく追加された | 低速トランザクション ログのしきい値を設定します。トランザクションの実行時間がこのしきい値を超えると、TiDB はトランザクションに関する詳細情報をログに記録します。デフォルト値`0`は、この機能が無効であることを意味します。                                                                            |
| [`tidb_ttl_running_tasks`](/system-variables.md#tidb_ttl_running_tasks-new-in-v700)                                               | 新しく追加された | この変数は、クラスター全体の TTL タスクの同時実行を制限するために使用されます。デフォルト値`-1`は、TTL タスクが TiKV ノードの数と同じであることを意味します。                                                                                                     |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                      | タイプを変更   | 説明                                                                                                                                                                                                                                                                |
| -------------- | ---------------------------------------------------------------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ティクヴ           | `server.snap-max-write-bytes-per-sec`                                                                | 削除されました  | このパラメータの名前は[`server.snap-io-max-bytes-per-sec`](/tikv-configuration-file.md#snap-io-max-bytes-per-sec)に変更されました。                                                                                                                                                   |
| ティクヴ           | [`raft-engine.enable-log-recycle`](/tikv-configuration-file.md#enable-log-recycle-new-in-v630)       | 修正済み     | デフォルト値は`false`から`true`に変更されます。                                                                                                                                                                                                                                    |
| ティクヴ           | [`resolved-ts.advance-ts-interval`](/tikv-configuration-file.md#advance-ts-interval)                 | 修正済み     | デフォルト値は`"1s"`から`"20s"`に変更されます。この変更により、解決済み TS の定期的な進行間隔が長くなり、TiKV ノード間のトラフィック消費が削減されます。                                                                                                                                                                           |
| ティクヴ           | [`resource-control.enabled`](/tikv-configuration-file.md#resource-control)                           | 修正済み     | デフォルト値は`false`から`true`に変更されます。                                                                                                                                                                                                                                    |
| ティクヴ           | [`raft-engine.prefill-for-recycle`](/tikv-configuration-file.md#prefill-for-recycle-new-in-v700)     | 新しく追加された | Raft Engineでログをリサイクルするために空のログ ファイルを生成するかどうかを制御します。デフォルト値は`false`です。                                                                                                                                                                                               |
| PD             | [`degraded-mode-wait-duration`](/pd-configuration-file.md#degraded-mode-wait-duration)               | 新しく追加された | [リソース管理](/tidb-resource-control.md)関連の設定項目。縮退モードをトリガーするまでの待機時間を制御します。デフォルト値は`0s`です。                                                                                                                                                                               |
| PD             | [`read-base-cost`](/pd-configuration-file.md#read-base-cost)                                         | 新しく追加された | [リソース管理](/tidb-resource-control.md)関連の構成項目。読み取り要求から RU への変換の基礎係数を制御します。デフォルト値は`0.25`です。                                                                                                                                                                           |
| PD             | [`read-cost-per-byte`](/pd-configuration-file.md#read-cost-per-byte)                                 | 新しく追加された | [リソース管理](/tidb-resource-control.md)関連の構成項目。読み取りフローから RU への変換の基礎係数を制御します。デフォルト値は`1/ (64 * 1024)`です。                                                                                                                                                                |
| PD             | [`read-cpu-ms-cost`](/pd-configuration-file.md#read-cpu-ms-cost)                                     | 新しく追加された | [リソース管理](/tidb-resource-control.md)関連の構成項目。CPU から RU への変換の基礎係数を制御します。デフォルト値は`1/3`です。                                                                                                                                                                              |
| PD             | [`write-base-cost`](/pd-configuration-file.md#write-base-cost)                                       | 新しく追加された | [リソース管理](/tidb-resource-control.md)関連の構成項目。書き込み要求から RU への変換の基礎係数を制御します。デフォルト値は`1`です。                                                                                                                                                                              |
| PD             | [`write-cost-per-byte`](/pd-configuration-file.md#write-cost-per-byte)                               | 新しく追加された | [リソース管理](/tidb-resource-control.md)関連の構成項目。書き込みフローから RU への変換の基礎係数を制御します。デフォルト値は`1/1024`です。                                                                                                                                                                        |
| TiFlash        | [`mark_cache_size`](/tiflash/tiflash-configuration.md)                                               | 修正済み     | 不要なメモリ使用量を削減するために、 TiFlashのデータ ブロックのメタデータのデフォルトのキャッシュ制限を`5368709120`から`1073741824`に変更します。                                                                                                                                                                         |
| TiFlash        | [`minmax_index_cache_size`](/tiflash/tiflash-configuration.md)                                       | 修正済み     | 不要なメモリ使用量を削減するために、 TiFlashのデータ ブロックの最小最大インデックスのデフォルトのキャッシュ制限を`5368709120`から`1073741824`に変更します。                                                                                                                                                                    |
| TiFlash        | [`flash.disaggregated_mode`](/tiflash/tiflash-disaggregated-and-s3.md)                               | 新しく追加された | TiFlashの分散アーキテクチャでは、このTiFlashノードが書き込みノードであるかコンピューティング ノードであるかを示します。値は`tiflash_write`または`tiflash_compute`になります。                                                                                                                                                    |
| TiFlash        | [`storage.s3.endpoint`](/tiflash/tiflash-disaggregated-and-s3.md)                                    | 新しく追加された | S3 に接続するエンドポイント。                                                                                                                                                                                                                                                  |
| TiFlash        | [`storage.s3.bucket`](/tiflash/tiflash-disaggregated-and-s3.md)                                      | 新しく追加された | TiFlash がすべてのデータを保存するバケット。                                                                                                                                                                                                                                        |
| TiFlash        | [`storage.s3.root`](/tiflash/tiflash-disaggregated-and-s3.md)                                        | 新しく追加された | S3 バケット内のデータstorageのルート ディレクトリ。                                                                                                                                                                                                                                   |
| TiFlash        | [`storage.s3.access_key_id`](/tiflash/tiflash-disaggregated-and-s3.md)                               | 新しく追加された | S3 にアクセスする場合は`ACCESS_KEY_ID` 。                                                                                                                                                                                                                                    |
| TiFlash        | [`storage.s3.secret_access_key`](/tiflash/tiflash-disaggregated-and-s3.md)                           | 新しく追加された | S3 にアクセスする場合は`SECRET_ACCESS_KEY` 。                                                                                                                                                                                                                                |
| TiFlash        | [`storage.remote.cache.dir`](/tiflash/tiflash-disaggregated-and-s3.md)                               | 新しく追加された | TiFlashコンピューティング ノードのローカル データ キャッシュ ディレクトリ。                                                                                                                                                                                                                       |
| TiFlash        | [`storage.remote.cache.capacity`](/tiflash/tiflash-disaggregated-and-s3.md)                          | 新しく追加された | TiFlashコンピューティング ノードのローカル データ キャッシュ ディレクトリのサイズ。                                                                                                                                                                                                                   |
| TiDB Lightning | [`add-index-by-sql`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)            | 新しく追加された | 物理インポート モードで SQL を使用してインデックスを追加するかどうかを制御します。デフォルト値は`false`です。これは、 TiDB Lightning が行データとインデックス データの両方を KV ペアにエンコードし、一緒に TiKV にインポートすることを意味します。SQL を使用してインデックスを追加する利点は、データのインポートとインデックスのインポートを分離し、データをすばやくインポートできることです。データのインポート後にインデックスの作成が失敗しても、データの一貫性は影響を受けません。 |
| ティCDC          | [`enable-table-across-nodes`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters) | 新しく追加された | リージョンの数に応じて、テーブルを複数の同期範囲に分割するかどうかを決定します。これらの範囲は、複数の TiCDC ノードによって複製できます。                                                                                                                                                                                          |
| ティCDC          | [`region-threshold`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)          | 新しく追加された | `enable-table-across-nodes`が有効になっている場合、この機能は`region-threshold`以上のリージョンを持つテーブルにのみ適用されます。                                                                                                                                                                           |
| DM             | [`analyze`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)           | 新しく追加された | CHECKSUM が完了した後、各テーブルで`ANALYZE TABLE <table>`操作を実行するかどうかを制御します。 `"required"` / `"optional"` / `"off"`に設定できます。デフォルト値は`"optional"`です。                                                                                                                               |
| DM             | [`range-concurrency`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced) | 新しく追加された | dm-worker が KV データを TiKV に書き込む同時実行を制御します。                                                                                                                                                                                                                         |
| DM             | [`compress-kv-pairs`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced) | 新しく追加された | dm-worker が KV データを TiKV に送信するときに圧縮を有効にするかどうかを制御します。現在、gzip のみがサポートされています。デフォルト値は空で、圧縮がないことを意味します。                                                                                                                                                                |
| DM             | [`pd-addr`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)           | 新しく追加された | 物理インポート モードでのダウンストリーム PDサーバーのアドレスを制御します。1 つまたは複数の PD サーバーを入力できます。この構成項目が空の場合、デフォルトで TiDB クエリからの PD アドレス情報が使用されます。                                                                                                                                                 |

## 改善点 {#improvements}

-   ティビ

    -   `SELECT`つのステートメントに複数の`DISTINCT`が含まれる SQL クエリのパフォーマンスを最適化するために`EXPAND`演算子を導入します[＃16581](https://github.com/pingcap/tidb/issues/16581) @ [アイリンキッド](https://github.com/AilinKid)
    -   インデックス結合[#40505](https://github.com/pingcap/tidb/issues/40505) @ [イサール](https://github.com/Yisaer) SQL 形式をさらにサポート
    -   場合によっては TiDB でパーティションテーブルデータをグローバルにソートしないようにする[＃26166](https://github.com/pingcap/tidb/issues/26166) @ [定義2014](https://github.com/Defined2014)
    -   `fair lock mode`と`lock only if exists`同時に使用してサポート[＃42068](https://github.com/pingcap/tidb/issues/42068) @ [ミョンケミンタ](https://github.com/MyonKeminta)
    -   トランザクションスローログとトランザクション内部イベントの印刷をサポート[＃41863](https://github.com/pingcap/tidb/issues/41863) @ [エキシウム](https://github.com/ekexium)
    -   `ILIKE`オペレータ[＃40943](https://github.com/pingcap/tidb/issues/40943) @ [翻訳者](https://github.com/xzhangxian1008)をサポート

-   PD

    -   ストア制限[＃6043](https://github.com/tikv/pd/issues/6043) @ [ノルーシュ](https://github.com/nolouch)によるスケジュール失敗の新しい監視メトリックを追加します

-   TiFlash

    -   書き込みパス[＃7144](https://github.com/pingcap/tiflash/issues/7144) @ [ホンユンヤン](https://github.com/hongyunyan)での TiFlash のメモリ使用量を削減
    -   多数のテーブルがあるシナリオで TiFlash の再起動時間を短縮[＃7146](https://github.com/pingcap/tiflash/issues/7146) @ [ホンユンヤン](https://github.com/hongyunyan)
    -   `ILIKE`演算子[＃6740](https://github.com/pingcap/tiflash/issues/6740) @ [翻訳者](https://github.com/xzhangxian1008)を押し下げるサポート

-   ツール

    -   ティCDC

        -   Kafka がダウンストリームであるシナリオで、単一の大きなテーブルのデータ変更を複数の TiCDC ノードに分散することをサポートし、大規模な TiDB クラスターのデータ統合シナリオにおける単一テーブルのスケーラビリティの問題を解決します[＃8247](https://github.com/pingcap/tiflow/issues/8247) @ [金星の上](https://github.com/overvenus)

            この機能を有効にするには、TiCDC 構成項目`enable_table_across_nodes`を`true`に設定します`region_threshold`使用すると、テーブルのリージョン数がこのしきい値を超えると、TiCDC が対応するテーブルのデータ変更を複数の TiCDC ノードに配布し始めるように指定できます。

        -   災害復旧シナリオでのスループットの向上とRTOの短縮のために、REDOアプライヤでのトランザクション分割をサポートする[＃8318](https://github.com/pingcap/tiflow/issues/8318) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)

        -   テーブル スケジューリングを改善して、1 つのテーブルをさまざまな TiCDC ノード[＃8247](https://github.com/pingcap/tiflow/issues/8247) @ [金星の上](https://github.com/overvenus)に均等に分割します。

        -   MQシンク[＃8286](https://github.com/pingcap/tiflow/issues/8286) @ [ハイラスティン](https://github.com/Rustin170506)にLarge Rowモニタリングメトリックを追加します。

        -   リージョンに複数のテーブル[＃6346](https://github.com/pingcap/tiflow/issues/6346) @ [金星の上](https://github.com/overvenus)のデータが含まれているシナリオで、TiKV ノードと TiCDC ノード間のネットワーク トラフィックを削減します。

        -   チェックポイントTSと解決済みTSのP99メトリックパネルをラグ分析パネル[＃8524](https://github.com/pingcap/tiflow/issues/8524) @ [ハイラスティン](https://github.com/Rustin170506)に移動します。

        -   REDOログ[＃8361](https://github.com/pingcap/tiflow/issues/8361) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)へのDDLイベントの適用をサポート

        -   アップストリーム書き込みスループット[＃7720](https://github.com/pingcap/tiflow/issues/7720) @ [金星の上](https://github.com/overvenus)に基づいて TiCDC ノードへのテーブルの分割とスケジュールをサポートします。

    -   TiDB Lightning

        -   TiDB Lightning物理インポート モードは、データのインポートとインデックスのインポートを分離して、インポートの速度と安定性を向上させます[＃42132](https://github.com/pingcap/tidb/issues/42132) @ [眠いモグラ](https://github.com/sleepymole)

            `add-index-by-sql`パラメータを追加します。デフォルト値は`false`で、これはTiDB Lightning が行データとインデックス データの両方を KV ペアにエンコードし、一緒に TiKV にインポートすることを意味します。 `true`に設定すると、 TiDB Lightningデータをインポートした後、 `ADD INDEX` SQL ステートメントを介してインデックスを追加し、インポート速度と安定性を向上させます。

        -   `tikv-importer.keyspace-name`パラメータを追加します。デフォルト値は空の文字列です。つまり、 TiDB Lightning は、データをインポートするために、対応するテナントのキー スペース名を自動的に取得します。値を指定すると、指定されたキー スペース名がデータのインポートに使用されます。このパラメータにより、マルチテナント TiDB クラスターにデータをインポートするときに、 TiDB Lightningの構成に柔軟性がもたらされます[＃41915](https://github.com/pingcap/tidb/issues/41915) @ [リチュンジュ](https://github.com/lichunzhu)

## バグ修正 {#bug-fixes}

-   ティビ

    -   TiDB を v6.5.1 からそれ以降のバージョン[＃41502](https://github.com/pingcap/tidb/issues/41502) @ [クリサン](https://github.com/chrysan)にアップグレードするときに更新が失われる問題を修正しました
    -   [＃41423](https://github.com/pingcap/tidb/issues/41423) @ [クレイジーcs520](https://github.com/crazycs520)にアップグレードした後、一部のシステム変数のデフォルト値が変更されない問題を修正しました
    -   インデックスの追加に関連するコプロセッサー要求タイプが不明[＃41400](https://github.com/pingcap/tidb/issues/41400) @ [タンジェンタ](https://github.com/tangenta)として表示される問題を修正
    -   インデックス[＃41515](https://github.com/pingcap/tidb/issues/41515) @ [タンジェンタ](https://github.com/tangenta)を追加するときに「PessimisticLockNotFound」が返される問題を修正しました
    -   一意のインデックス[＃41630](https://github.com/pingcap/tidb/issues/41630) @ [タンジェンタ](https://github.com/tangenta)を追加するときに誤って`found duplicate key`を返す問題を修正しました
    -   インデックス[＃41880](https://github.com/pingcap/tidb/issues/41880) @ [タンジェンタ](https://github.com/tangenta)を追加するときに発生するpanic問題を修正
    -   実行中にTiFlash が生成された列のエラーを報告する問題を修正[＃40663](https://github.com/pingcap/tidb/issues/40663) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   時間タイプ[＃41938](https://github.com/pingcap/tidb/issues/41938) @ [翻訳者](https://github.com/xuyifangreeneyes)がある場合に TiDB が統計を正しく取得できない可能性がある問題を修正しました。
    -   準備済みプランキャッシュが有効になっている場合にフルインデックススキャンでエラーが発生する可能性がある問題を修正[＃42150](https://github.com/pingcap/tidb/issues/42150) @ [ふーふー](https://github.com/fzzf678)
    -   `IFNULL(NOT NULL COLUMN, ...)`誤った結果を返す可能性がある問題を修正[＃41734](https://github.com/pingcap/tidb/issues/41734) @ [リトルフォール](https://github.com/LittleFall)
    -   パーティションテーブル内のすべてのデータが単一のリージョン[＃41801](https://github.com/pingcap/tidb/issues/41801) @ [定義2014](https://github.com/Defined2014)にある場合に TiDB が誤った結果を生成する可能性がある問題を修正しました。
    -   単一の SQL ステートメントに異なるパーティション テーブルが出現すると、TiDB が誤った結果を生成する可能性がある問題を修正しました[＃42135](https://github.com/pingcap/tidb/issues/42135) @ [ミョンス](https://github.com/mjonss)
    -   パーティションテーブルに新しいインデックスを追加した後、パーティションテーブルで統計の自動収集が正しくトリガーされない可能性がある問題を修正しました[＃41638](https://github.com/pingcap/tidb/issues/41638) @ [翻訳者](https://github.com/xuyifangreeneyes)
    -   統計を2回連続で収集した後にTiDBが誤った列統計情報を読み取る可能性がある問題を修正[＃42073](https://github.com/pingcap/tidb/issues/42073) @ [翻訳者](https://github.com/xuyifangreeneyes)
    -   準備プランキャッシュが有効になっている場合に IndexMerge が誤った結果を生成する可能性がある問題を修正[＃41828](https://github.com/pingcap/tidb/issues/41828) @ [qw4990](https://github.com/qw4990)
    -   IndexMerge で goroutine リークが発生する可能性がある問題を修正[＃41605](https://github.com/pingcap/tidb/issues/41605) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   BIGINT 以外の符号なし整数を文字列/小数と比較すると誤った結果が生成される可能性がある問題を修正[＃41736](https://github.com/pingcap/tidb/issues/41736) @ [リトルフォール](https://github.com/LittleFall)
    -   メモリ制限超過により前の`ANALYZE`ステートメントを強制終了すると、同じセッション内の現在の`ANALYZE`ステートメントが[＃41825](https://github.com/pingcap/tidb/issues/41825) @ [徐懐玉](https://github.com/XuHuaiyu)で強制終了される可能性がある問題を修正しました。
    -   バッチコプロセッサ[＃41412](https://github.com/pingcap/tidb/issues/41412) @ [あなた06](https://github.com/you06)の情報収集処理中にデータ競合が発生する可能性がある問題を修正
    -   アサーションエラーによりパーティションテーブル[＃40629](https://github.com/pingcap/tidb/issues/40629) @ [エキシウム](https://github.com/ekexium)の MVCC 情報が印刷されない問題を修正しました。
    -   フェアロックモードで存在しないキー[＃41527](https://github.com/pingcap/tidb/issues/41527) @ [エキシウム](https://github.com/ekexium)にロックが追加される問題を修正
    -   `INSERT IGNORE`と`REPLACE`ステートメントが値[＃42121](https://github.com/pingcap/tidb/issues/42121) @ [ジグアン](https://github.com/zyguan)を変更しないキーをロックしない問題を修正しました

-   PD

    -   リージョン散布操作によってリーダー[＃6017](https://github.com/tikv/pd/issues/6017) @ [ハンダンDM](https://github.com/HunDunDM)の分布が不均一になる可能性がある問題を修正しました。
    -   起動時にPDメンバーを取得する際にデータ競合が発生する可能性がある問題を修正[＃6069](https://github.com/tikv/pd/issues/6069) @ [rleungx](https://github.com/rleungx)
    -   ホットスポット統計[＃6069](https://github.com/tikv/pd/issues/6069) @ [翻訳者](https://github.com/lhy1024)を収集するときにデータ競合が発生する可能性がある問題を修正
    -   配置ルールを切り替えるとリーダー[＃6195](https://github.com/tikv/pd/issues/6195) @ [バッファフライ](https://github.com/bufferflies)の分布が不均等になる可能性がある問題を修正しました。

-   TiFlash

    -   特定のケースで小数点以下の桁が切り上げられない問題を修正[＃7022](https://github.com/pingcap/tiflash/issues/7022) @ [リトルフォール](https://github.com/LittleFall)
    -   特定のケースで[＃6994](https://github.com/pingcap/tiflash/issues/6994) @ [風の話し手](https://github.com/windtalker) Decimal キャストが誤って切り上げられる問題を修正しました
    -   新しい照合順序[＃6807](https://github.com/pingcap/tiflash/issues/6807) @ [翻訳者](https://github.com/xzhangxian1008)を有効にした後に TopN/Sort 演算子が誤った結果を生成する問題を修正しました。
    -   単一のTiFlashノード[＃6993](https://github.com/pingcap/tiflash/issues/6993) @ [風の話し手](https://github.com/windtalker)で 1200 万行を超える結果セットを集計するときにTiFlash がエラーを報告する問題を修正しました。

-   ツール

    -   バックアップと復元 (BR)

        -   PITR リカバリ プロセス[＃42001](https://github.com/pingcap/tidb/issues/42001) @ [ジョッカウ](https://github.com/joccau)中に分割リージョンの再試行の待機時間が不十分になる問題を修正
        -   PITR リカバリ プロセス中に発生した`memory is limited`エラーが原因でリカバリが失敗する問題を修正[＃41983](https://github.com/pingcap/tidb/issues/41983) @ [ジョッカウ](https://github.com/joccau)
        -   PDノードがダウンしているときにPITRログバックアップの進行が進まない問題を修正[＃14184](https://github.com/tikv/tikv/issues/14184) @ [ユジュンセン](https://github.com/YuJuncen)
        -   リージョンリーダーシップの移行が発生すると、PITR ログバックアップの進行のレイテンシーが長くなるという問題を緩和します[＃13638](https://github.com/tikv/tikv/issues/13638) @ [ユジュンセン](https://github.com/YuJuncen)

    -   ティCDC

        -   変更フィードを再開するとデータが失われる可能性がある、またはチェックポイントが[＃8242](https://github.com/pingcap/tiflow/issues/8242) @ [金星の上](https://github.com/overvenus)に進めない問題を修正しました。
        -   DDLシンク[＃8238](https://github.com/pingcap/tiflow/issues/8238) @ [3エースショーハンド](https://github.com/3AceShowHand)のデータ競合問題を修正
        -   `stopped`ステータスの変更フィードが自動的に再起動する可能性がある問題を修正[＃8330](https://github.com/pingcap/tiflow/issues/8330) @ [スドジ](https://github.com/sdojjy)
        -   すべての下流 Kafka サーバーが利用できない場合に TiCDCサーバーがパニックになる問題を修正[＃8523](https://github.com/pingcap/tiflow/issues/8523) @ [3エースショーハンド](https://github.com/3AceShowHand)
        -   ダウンストリームがMySQLで、実行されたステートメントがTiDB [＃8453](https://github.com/pingcap/tiflow/issues/8453) @ [アズドンメン](https://github.com/asddongmen)と互換性がない場合にデータが失われる可能性がある問題を修正しました。
        -   ローリングアップグレードによって TiCDC OOM が発生したり、チェックポイントが[＃8329](https://github.com/pingcap/tiflow/issues/8329) @ [金星の上](https://github.com/overvenus)で停止したりする問題を修正しました。
        -   Kubernetes [＃8484](https://github.com/pingcap/tiflow/issues/8484) @ [金星の上](https://github.com/overvenus)で TiCDC クラスターの正常なアップグレードが失敗する問題を修正

    -   TiDB データ移行 (DM)

        -   DM ワーカー ノードが Google Cloud Storage を使用する場合、ブレークポイントが頻繁すぎるために Google Cloud Storage のリクエスト頻度の制限に達し、DM ワーカーがデータを Google Cloud Storage に書き込むことができず、完全なデータの読み込みに失敗する問題を修正しました[＃8482](https://github.com/pingcap/tiflow/issues/8482) @ [マックスシュアン](https://github.com/maxshuang)
        -   複数の DM タスクが同じダウンストリーム データを同時に複製し、すべてがダウンストリーム メタデータ テーブルを使用してブレークポイント情報を記録すると、すべてのタスクのブレークポイント情報が同じメタデータ テーブルに書き込まれ、同じタスク ID [＃8500](https://github.com/pingcap/tiflow/issues/8500) @ [マックスシュアン](https://github.com/maxshuang)が使用される問題を修正しました。

    -   TiDB Lightning

        -   物理インポートモードを使用してデータをインポートする場合、ターゲットテーブルの複合主キーに`auto_random`列目があるが、ソースデータに列の値が指定されていない場合、 TiDB Lightning は`auto_random`列目のデータを自動的に生成しないという問題を修正しました[＃41454](https://github.com/pingcap/tidb/issues/41454) @ [D3ハンター](https://github.com/D3Hunter)
        -   論理インポートモードを使用してデータをインポートすると、ターゲットクラスタ[＃41915](https://github.com/pingcap/tidb/issues/41915) @ [リチュンジュ](https://github.com/lichunzhu)の`CONFIG`権限が不足しているためにインポートが失敗する問題を修正しました。

## 寄稿者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   [アンチトップクォーク](https://github.com/AntiTopQuark)
-   [えり](https://github.com/blacktear23)
-   [ボーンチェンジャー](https://github.com/BornChanger)
-   [ドゥージール9](https://github.com/Dousir9)
-   [エルワドバ](https://github.com/erwadba)
-   [ハッピーv587](https://github.com/happy-v587)
-   [ジフハウス](https://github.com/jiyfhust)
-   [L-メープル](https://github.com/L-maple)
-   [りゅうめんぎゃ](https://github.com/liumengya94)
-   [ウーフィジャオ](https://github.com/woofyzhao)
-   [下関](https://github.com/xiaguan)
