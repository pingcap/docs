---
title: TiDB 7.0.0 Release Notes
summary: TiDB 7.0.0 の新機能、互換性の変更点、改善点、およびバグ修正についてご確認ください。
---

# TiDB 7.0.0 リリースノート {#tidb-7-0-0-release-notes}

発売日：2023年3月30日

TiDB バージョン: 7.0.0- [DMR](/releases/versioning.md#development-milestone-releases)

クイックアクセス: [クイックスタート](https://docs-archive.pingcap.com/tidb/v7.0/quick-start-with-tidb)

バージョン7.0.0-DMRの主な新機能と改善点は以下のとおりです。

<table><thead><tr><th>カテゴリ</th><th>特徴</th><th>説明</th></tr></thead><tbody><tr><td rowspan="2">拡張性とパフォーマンス<br/></td><td>セッションレベルの<a href="https://docs-archive.pingcap.com/tidb/v7.0/sql-non-prepared-plan-cache" target="_blank">非プリペアドSQLプランキャッシュ</a>（実験的）</td><td>セッションレベルでプランキャッシュを自動的に再利用することで、コンパイルを削減し、同じSQLパターンに対して事前に手動でプリペアドステートメントを設定することなくクエリ時間を短縮します。</td></tr><tr><td> TiFlashは <a href="https://docs-archive.pingcap.com/tidb/v7.0/tiflash-disaggregated-and-s3" target="_blank">、分散型ストレージおよびコンピューティングアーキテクチャとS3共有ストレージ</a>（実験的）をサポートしています。</td><td> TiFlashは、オプションとしてクラウドネイティブアーキテクチャを導入します。<ul><li> TiFlashのコンピューティング機能とストレージを分離することで、柔軟なHTAPリソース利用における画期的な進歩を実現しました。</li><li> S3ベースのストレージエンジンを導入し、より低コストで共有ストレージを提供可能にしました。</li></ul></td></tr><tr><td rowspan="2">信頼性と可用性<br/></td><td><a href="https://docs-archive.pingcap.com/tidb/v7.0/tidb-resource-control" target="_blank">リソース制御機能強化</a>（実験的）</td><td>リソースグループを使用して、1 つのクラスタ内のさまざまなアプリケーションやワークロードにリソースを割り当て、分離することをサポートします。今回のリリースでは、TiDB はさまざまなリソースバインディングモード (ユーザー、セッション、ステートメントレベル) とユーザー定義の優先度をサポートします。さらに、コマンドを使用してリソースのキャリブレーション (リソース全体の量の見積もり) を実行することもできます。</td></tr><tr><td> TiFlashは<a href="https://docs-archive.pingcap.com/tidb/v7.0/tiflash-spill-disk" target="_blank">ディスクへのスピル</a>をサポートしています</td><td>TiFlashは、集計、ソート、ハッシュ結合などのデータ集約型操作におけるメモリ不足（OOM）を軽減するために、中間結果をディスクに書き出す機能をサポートしています。</td></tr><tr><td rowspan="2"> SQL</td><td><a href="https://docs-archive.pingcap.com/tidb/v7.0/time-to-live" target="_blank">行レベルTTL</a> （GA）</td><td>一定期間経過したデータを自動的に削除することで、データベースサイズの管理をサポートし、パフォーマンスを向上させます。</td></tr><tr><td> <a href="https://docs-archive.pingcap.com/tidb/v7.0/partitioned-table#reorganize-partitions" target="_blank"><code>LIST</code> / <code>RANGE</code>パーティションを再編成する</a></td><td><code>REORGANIZE PARTITION</code>ステートメントは、隣接するパーティションをマージしたり、1 つのパーティションを複数のパーティションに分割したりするために使用でき、パーティション化されたテーブルの使いやすさを向上させます。</td></tr><tr><td rowspan="2">データベースの運用と可観測性<br/></td><td>TiDBは<a href="https://docs-archive.pingcap.com/tidb/v7.0/sql-statement-load-data" target="_blank"><code>LOAD DATA</code>ステートメント</a>の機能を拡張します（実験的）。</td><td> TiDBは、S3/GCSからのデータインポートをサポートするなど、 <code>LOAD DATA</code> SQLステートメントの機能を拡張します。<br/></td></tr><tr><td> TiCDCは<a href="https://docs-archive.pingcap.com/tidb/v7.0/ticdc-sink-to-cloud-storage" target="_blank">オブジェクトストレージシンク</a>（GA）をサポートしています</td><td>TiCDCは、Amazon S3、GCS、Azure Blob Storage、NFSなどのオブジェクトストレージサービスへの行変更イベントの複製をサポートしています。<br/></td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### 拡張性 {#scalability}

-   TiFlashは、分散ストレージとコンピューティングアーキテクチャをサポートし、このアーキテクチャにおけるオブジェクトストレージをサポートします（実験的） [#6882](https://github.com/pingcap/tiflash/issues/6882) @[flowbehappy](https://github.com/flowbehappy)

    バージョン7.0.0より前のTiFlashは、ストレージとコンピューティングが結合されたアーキテクチャのみをサポートしていました。このアーキテクチャでは、各TiFlashノードがストレージとコンピューティングノードの両方の役割を担い、コンピューティング機能とstorage機能を個別に拡張することはできませんでした。また、 TiFlashノードはローカルストレージしか使用できませんでした。

    バージョン7.0.0以降、 TiFlashは分離型ストレージおよびコンピューティングアーキテクチャもサポートしています。このアーキテクチャでは、 TiFlashノードは2種類（コンピューティングノードと書き込みノード）に分かれており、S3 APIと互換性のあるオブジェクトストレージをサポートしています。どちらのタイプのノードも、コンピューティング容量またはストレージ容量に合わせて個別にスケーリングできます。**分離型ストレージおよびコンピューティングアーキテクチャ**と**結合型ストレージおよびコンピューティングアーキテクチャは、**同じクラスタ内で使用したり、相互に変換したりすることはできません。TiFlashをデプロイする際に、使用するアーキテクチャを設定できます。

    詳細については、[ドキュメント](/tiflash/tiflash-disaggregated-and-s3.md)を参照してください。

### パフォーマンス {#performance}

-   Fast Online DDL と PITR 間の互換性を達成 [#38045](https://github.com/pingcap/tidb/issues/38045) @[Leavrth](https://github.com/Leavrth)

    TiDB v6.5.0では、 [高速オンラインDDL](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) [PITR](/br/backup-and-restore-overview.md)と完全には互換性がありません。完全なデータバックアップを確実に行うには、まずPITRのバックグラウンドバックアップタスクを停止し、高速オンラインDDLを使用してインデックスをすばやく追加してから、PITRのバックアップタスクを再開することをお勧めします。

    TiDB v7.0.0以降、Fast Online DDLとPITRは完全に互換性があります。PITRを使用してクラスタデータを復元する場合、ログバックアップ中にFast Online DDLで追加されたインデックス操作が自動的に再生され、互換性が確保されます。

    詳細については、[ドキュメント](/best-practices/ddl-introduction.md)を参照してください。

-   TiFlashは、null対応セミジョイン演算子とnull対応アンチセミジョイン演算子をサポートしています [#6674](https://github.com/pingcap/tiflash/issues/6674) @[gengliqi](https://github.com/gengliqi)

    相関サブクエリで`IN` 、 `NOT IN` 、 `= ANY` 、または`!= ALL`演算子を使用する場合、TiDB はそれらを準演算子に変換することでコンピューティング パフォーマンスを最適化します。ジョインまたはアンチセミジョイン。結合キー列が`NULL`の場合は、 [NULL値対応セミジョイン](/explain-subqueries.md#null-aware-semi-join-in-and--any-subqueries)や[ヌル値対応アンチセミジョイン](/explain-subqueries.md#null-aware-anti-semi-join-not-in-and--all-subqueries)などの、null 対応結合アルゴリズムが必要です。

    バージョン 7.0.0 より前のTiFlashでは、NULL 対応セミ結合演算子と NULL 対応アンチセミ結合演算子がサポートされていなかったため、これらのサブクエリをTiFlashに直接プッシュダウンすることができませんでした。バージョン 7.0.0 以降では、 TiFlash はNULL 対応セミ結合演算子と NULL 対応アンチセミ結合演算子をサポートしています。SQL ステートメントにこれらの相関サブクエリが含まれており、クエリ内のテーブルにTiFlashレプリカがあり、かつ[MPPモード](/tiflash/use-tiflash-mpp-mode.md)が有効になっている場合、オプティマイザは全体的なパフォーマンスを向上させるために、NULL 対応セミ結合演算子と NULL 対応アンチセミ結合演算子をTiFlashにプッシュダウンするかどうかを自動的に判断します。

    詳細については、 [ドキュメント](/tiflash/tiflash-supported-pushdown-calculations.md)を参照してください。

-   TiFlash は FastScan (GA) の使用をサポートしています [#5252](https://github.com/pingcap/tiflash/issues/5252) @[hongyunyan](https://github.com/hongyunyan)

    TiFlash はv6.3.0 から FastScan を実験的機能として導入しました。v7.0.0 では、この機能が一般利用可能になります。FastScan はシステム変数[`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-new-in-v630)を使用して有効にできます。この機能は、強力な一貫性を犠牲にすることで、テーブルスキャンのパフォーマンスを大幅に向上させます。対応するテーブルが`INSERT` / { `UPDATE`操作を含まず、 `DELETE`操作のみを含む場合、FastScan は強力な一貫性を維持し、スキャンのパフォーマンスを向上させることができます。

    詳細については、[ドキュメント](/tiflash/use-fastscan.md)を参照してください。

-   TiFlashは後期実体化をサポート (実験的) [#5829](https://github.com/pingcap/tiflash/issues/5829) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)

    フィルタ条件 ( `SELECT` `WHERE`ステートメントを処理する場合、 TiFlash はデフォルトでクエリに必要な列からすべてのデータを読み取り、クエリ条件に基づいてデータをフィルタリングおよび集計します。遅延マテリアライゼーションは、フィルタ条件の一部を TableScan オペレータにプッシュダウンすることをサポートする最適化手法です。つまり、 TiFlash はまずプッシュダウンされたフィルタ条件に関連する列データをスキャンし、条件を満たす行をフィルタリングしてから、これらの行の他の列データをスキャンしてさらに計算を行うことで、データ処理の IO スキャンと計算を削減します。

    TiFlashの遅延マテリアライゼーション機能は、デフォルトでは有効になっていません。 `tidb_opt_enable_late_materialization`システム変数を`OFF`に設定することで有効にできます。この機能が有効になると、TiDBオプティマイザは統計情報とフィルタ条件に基づいて、どのフィルタ条件をプッシュダウンするかを決定します。

    詳細については、[ドキュメント](/tiflash/tiflash-late-materialization.md)を参照してください。

-   非プリペアドステートメントの実行プランのキャッシュをサポートする（実験的） [#36598](https://github.com/pingcap/tidb/issues/36598) @[qw4990](https://github.com/qw4990)

    実行プランキャッシュは同時実行 OLTP の処理能力を向上させるために重要であり、TiDB はすでに[プリペアドプランキャッシュ](/sql-prepared-plan-cache.md)をサポートしています。 v7.0.0 では、TiDB は非 Prepare ステートメントの実行プランをキャッシュすることもできるため、実行プラン キャッシュの範囲が拡張され、TiDB の同時処理能力が向上します。

    この機能はデフォルトでは無効になっています。システム変数[`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) `ON`に設定することで有効にできます。安定性のため、TiDB v7.0.0 では非プリペアド実行プランをキャッシュするための新しい領域が割り当てられ、システム変数[`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size)を使用してキャッシュサイズを設定できます。さらに、この機能には SQL ステートメントに関する特定の制限があります。詳細については、 [制限](/sql-non-prepared-plan-cache.md#restrictions)参照してください。

    詳細については、[ドキュメント](/sql-non-prepared-plan-cache.md)を参照してください。

-   TiDB がサブクエリの実行プラン キャッシュ制約を削除 [#40219](https://github.com/pingcap/tidb/issues/40219) @[fzzf678](https://github.com/fzzf678)

    TiDB v7.0.0 では、サブクエリに対する実行プランキャッシュの制約が解除されました。これにより、 `SELECT * FROM t WHERE a > (SELECT ...)`のようにサブクエリを含む SQL ステートメントの実行プランをキャッシュできるようになりました。この機能により、実行プランキャッシュの適用範囲がさらに拡大し、SQL クエリの実行効率が向上します。

    詳細については、[ドキュメント](/sql-prepared-plan-cache.md)を参照してください。

-   TiKVはログリサイクル用の空のログファイルの自動生成をサポートしています [#14371](https://github.com/tikv/tikv/issues/14371) @[LykxSassinator](https://github.com/LykxSassinator)

    バージョン6.3.0では、書き込み負荷によって発生するロングテールレイテンシーを低減するために、TiKVは[Raftのリサイクル](/tikv-configuration-file.md#enable-log-recycle-new-in-v630)機能を導入しました。しかし、ログのリサイクルはRaftログファイルの数が一定のしきい値に達した場合にのみ有効になるため、ユーザーがこの機能によるスループットの向上を直接体感することは困難です。

    バージョン7.0.0では、ユーザーエクスペリエンスを向上させるために`raft-engine.prefill-for-recycle`という新しい設定項目が導入されました。この項目は、プロセスの開始時に空のログファイルが生成されて再利用されるかどうかを制御します。この設定を有効にすると、TiKVは初期化中に空のログファイルのバッチを自動的に作成し、初期化直後にログの再利用が確実に実行されるようにします。

    詳細については、 [ドキュメント](/tikv-configuration-file.md#prefill-for-recycle-new-in-v700)を参照してください。

-   ウィンドウ[ウィンドウ関数](/functions-and-operators/expressions-pushed-down.md)からの TopN または Limit 演算子の導出をサポート [#13936](https://github.com/tikv/tikv/issues/13936) @[windtalker](https://github.com/windtalker)

    この機能はデフォルトでは無効になっています。有効にするには、セッション変数[tidb_opt_derive_topn](/system-variables.md#tidb_opt_derive_topn-new-in-v700) `ON`に設定してください。

    詳細については、[ドキュメント](/derive-topn-from-window.md)を参照してください。

-   Fast Online DDL による一意インデックス作成のサポート [#40730](https://github.com/pingcap/tidb/issues/40730) @[tangenta](https://github.com/tangenta)

    TiDB v6.5.0 では、Fast Online DDL による通常のセカンダリ インデックスの作成がサポートされています。TiDB v7.0.0 では、Fast Online DDL によるユニーク インデックスの作成がサポートされています。v6.1.0 と比較して、大規模テーブルへのユニーク インデックスの追加は、パフォーマンスの向上により数倍高速化されることが期待されます。

    詳細については、[ドキュメント](/best-practices/ddl-introduction.md)を参照してください。

### 信頼性 {#reliability}

-   リソース制御機能の強化 (実験的) [#38825](https://github.com/pingcap/tidb/issues/38825) @[nolouch](https://github.com/nolouch)@[BornChanger](https://github.com/BornChanger)@[glorv](https://github.com/glorv)@[tiancaiamao](https://github.com/tiancaiamao)@[Connor1996](https://github.com/Connor1996) @[JmPotato](https://github.com/JmPotato) @[hnes](https://github.com/hnes) @[CabinfeverB](https://github.com/CabinfeverB) @[HuSharp](https://github.com/HuSharp)

    TiDBは、リソースグループに基づくリソース制御機能を強化しました。この機能により、TiDBクラスタのリソース利用効率とパフォーマンスが大幅に向上します。リソース制御機能の導入は、TiDBにとって画期的な出来事です。分散データベースクラスタを複数の論理ユニットに分割し、異なるデータベースユーザーを対応するリソースグループにマッピングし、必要に応じて各リソースグループのクォータを設定できます。クラスタのリソースが制限されている場合、同じリソースグループ内のセッションが使用するすべてのリソースはクォータに制限されます。このようにして、リソースグループが過剰に消費された場合でも、他のリソースグループのセッションには影響しません。

    この機能により、異なるシステム上の複数の中小規模アプリケーションを単一のTiDBクラスタに統合できます。アプリケーションのワークロードが増加しても、他のアプリケーションの正常な動作には影響しません。システムワークロードが低い場合は、負荷の高いアプリケーションが設定されたクォータを超えても、必要なシステムリソースを割り当てられるため、リソースを最大限に活用できます。さらに、リソース制御機能を合理的に活用することで、クラスタ数を削減し、運用保守の負担を軽減し、管理コストを削減できます。

    この機能は、Grafanaにおけるリソースの実際の使用状況を表示する組み込みのリソース制御ダッシュボードを提供し、リソースをより合理的に割り当てるのに役立ちます。また、セッションレベルとステートメントレベルの両方に基づいた動的なリソース管理機能もサポートしています（ヒント）。この機能の導入により、TiDBクラスタのリソース使用状況をより正確に制御し、実際のニーズに基づいてクォータを動的に調整できるようになります。

    TiDB v7.0.0では、リソースグループの絶対スケジューリング優先度（ `PRIORITY` ）を設定することで、重要なサービスが確実にリソースを取得できるようになります。また、リソースグループの設定方法も拡張されています。

    リソースグループは、以下の方法で使用できます。

    -   ユーザーレベル。[`CREATE USER`](/sql-statements/sql-statement-create-user.md)または[`ALTER USER`](/sql-statements/sql-statement-alter-user.md)ステートメントを使用して、ユーザーを特定のリソースグループにバインドします。リソースグループをユーザーにバインドすると、そのユーザーが新しく作成したセッションは、対応するリソースグループに自動的にバインドされます。
    -   セッションレベル。[`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md)を使用して、現在のセッションで使用されるリソースグループを設定します。
    -   ステートメントレベル。[`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name)を使用して、現在のステートメントで使用されるリソースグループを設定します。

    詳細については、[ドキュメント](/tidb-resource-control-ru-groups.md)を参照してください。

-   高速オンラインDDLのチェックポイントメカニズムをサポートし、耐障害性と自動リカバリ機能を向上させる [#42164](https://github.com/pingcap/tidb/issues/42164) @[tangenta](https://github.com/tangenta)

    TiDB v7.0.0では、 [高速オンラインDDL](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)にチェックポイント機構が導入され、耐障害性と自動リカバリ機能が大幅に向上しました。DDLの進行状況を定期的に記録・同期することで、TiDB DDLオーナーの障害や切り替えが発生した場合でも、進行中のDDL操作を高速オンラインDDLモードで継続実行できます。これにより、DDLの実行がより安定し、効率的になります。

    詳細については、[ドキュメント](/best-practices/ddl-introduction.md)を参照してください。

-   TiFlashはディスクへのスピルをサポート [#6528](https://github.com/pingcap/tiflash/issues/6528) @[windtalker](https://github.com/windtalker)

    実行パフォーマンスを向上させるため、 TiFlashは可能な限りデータをメモリ内で処理します。データ量がメモリの総容量を超えると、メモリ不足によるシステムクラッシュを回避するため、 TiFlashはクエリを終了します。したがって、 TiFlashが処理できるデータ量は、利用可能なメモリ容量によって制限されます。

    バージョン7.0.0以降、 TiFlashはディスクへのスピルをサポートしています。オペレータのメモリ使用量のしきい値（ [`tidb_max_bytes_before_tiflash_external_group_by`](/system-variables.md#tidb_max_bytes_before_tiflash_external_group_by-new-in-v700) 、 [`tidb_max_bytes_before_tiflash_external_sort`](/system-variables.md#tidb_max_bytes_before_tiflash_external_sort-new-in-v700) 、 [`tidb_max_bytes_before_tiflash_external_join`](/system-variables.md#tidb_max_bytes_before_tiflash_external_join-new-in-v700) ）を調整することで、オペレータが使用できる最大メモリ量を制御できます。オペレータが使用するメモリがしきい値を超えると、データは自動的にディスクに書き込まれます。これによりパフォーマンスは多少低下しますが、より多くのデータを処理できるようになります。

    詳細については、[ドキュメント](/tiflash/tiflash-spill-disk.md)を参照してください。

-   統計情報の収集効率を向上させる [#41930](https://github.com/pingcap/tidb/issues/41930) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)

    バージョン7.0.0では、TiDBは統計情報の収集ロジックをさらに最適化し、収集時間を約25%短縮しました。この最適化により、大規模データベースクラスタの運用効率と安定性が向上し、統計情報の収集がクラスタのパフォーマンスに与える影響が軽減されます。

-   MPP 最適化のための新しいオプティマイザー ヒントを追加 [#39710](https://github.com/pingcap/tidb/issues/39710) @[Reminiscent](https://github.com/Reminiscent)

    バージョン7.0.0では、TiDBはMPP実行プランの生成に影響を与える一連のオプティマイザヒントを追加しました。

    -   [`SHUFFLE_JOIN()`](/optimizer-hints.md#shuffle_joint1_name--tl_name-) : MPP で有効になります。指定されたテーブルに対してシャッフル結合アルゴリズムを使用するようにオプティマイザに指示します。
    -   [`BROADCAST_JOIN()`](/optimizer-hints.md#broadcast_joint1_name--tl_name-) : MPP で有効になります。指定されたテーブルに対してブロードキャスト結合アルゴリズムを使用するようにオプティマイザに指示します。
    -   [`MPP_1PHASE_AGG()`](/optimizer-hints.md#mpp_1phase_agg) ：MPP（最大パフォーマンス）に有効です。指定されたクエリブロック内のすべての集計関数に対して、オプティマイザに1フェーズ集計アルゴリズムを使用するように指示します。
    -   [`MPP_2PHASE_AGG()`](/optimizer-hints.md#mpp_2phase_agg) : MPP で有効になります。指定されたクエリ ブロック内のすべての集計関数に対して、2 段階集計アルゴリズムを使用するようにオプティマイザに指示します。

    MPPオプティマイザのヒントを使用すると、HTAPクエリに介入して、HTAPワークロードのパフォーマンスと安定性を向上させることができます。

    詳細については、[ドキュメント](/optimizer-hints.md)を参照してください。

-   オプティマイザーのヒントは、結合メソッドと結合順序の指定をサポートします [#36600](https://github.com/pingcap/tidb/issues/36600) @[Reminiscent](https://github.com/Reminiscent)

    バージョン7.0.0では、オプティマイザヒント[`LEADING()`](/optimizer-hints.md#leadingt1_name--tl_name-)結合方法に影響を与えるヒントと併用できるようになり、両者の動作は互換性があります。複数テーブル結合の場合、最適な結合方法と結合順序を効果的に指定できるため、実行プランに対するオプティマイザヒントの制御が強化されます。

    新しいヒント動作には、若干の変更があります。前方互換性を確保するため、TiDB はシステム変数[`tidb_opt_advanced_join_hint`](/system-variables.md#tidb_opt_advanced_join_hint-new-in-v700)を導入します。この変数が`OFF`に設定されている場合、オプティマイザのヒント動作は以前のバージョンと互換性があります。クラスタを以前のバージョンから v7.0.0 以降のバージョンにアップグレードすると、この変数は`OFF`に設定されます。より柔軟なヒント動作を実現するには、動作によってパフォーマンスが低下しないことを確認した後、この変数を`ON`に設定することを強くお勧めします。

    詳細については、[ドキュメント](/optimizer-hints.md)を参照してください。

### 可用性 {#availability}

-   `prefer-leader`オプションをサポートします。このオプションは、読み取り操作の可用性を高め、不安定なネットワーク状況での応答レイテンシーを低減します。 [#40905](https://github.com/pingcap/tidb/issues/40905) @[LykxSassinator](https://github.com/LykxSassinator)

    TiDB のデータ読み取り動作は、システム変数[`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40)で制御できます。v7.0.0 では、この変数に`prefer-leader`オプションが追加されました。この変数を`prefer-leader`に設定すると、TiDB はリーダー レプリカを選択して読み取り操作を実行することを優先します。ディスクやネットワークのパフォーマンス変動などによりリーダー レプリカの処理速度が著しく低下した場合、TiDB は利用可能な他のフォロワー レプリカを選択して読み取り操作を実行し、可用性を高め、応答レイテンシーを削減します。

    詳細については、[ドキュメント](/develop/dev-guide-use-follower-read.md)を参照してください。

### SQL {#sql}

-   Time to Live (TTL) は一般に利用可能です [#39262](https://github.com/pingcap/tidb/issues/39262) @[lcwangchao](https://github.com/lcwangchao) @[YangKeao](https://github.com/YangKeao)

    TTLは行レベルのライフサイクル制御ポリシーを提供します。TiDBでは、TTL属性が設定されたテーブルは、設定に基づいて期限切れの行データを自動的にチェックして削除します。TTLの目的は、クラスタのワークロードへの影響を最小限に抑えながら、ユーザーが不要なデータを定期的に適切なタイミングでクリーンアップできるようにすることです。

    詳細については、[ドキュメント](/time-to-live.md)を参照してください。

-   サポート`ALTER TABLE…REORGANIZE PARTITION` [#15000](https://github.com/pingcap/tidb/issues/15000) @[mjonss](https://github.com/mjonss)

    TiDBは`ALTER TABLE...REORGANIZE PARTITION`構文をサポートしています。この構文を使用すると、データの損失なしに、テーブルのパーティションの一部または全部を再編成（マージ、分割、その他の変更を含む）できます。

    詳細については、[ドキュメント](/partitioned-table.md#reorganize-partitions)を参照してください。

-   キー分割をサポート [#41364](https://github.com/pingcap/tidb/issues/41364) @[TonsnakeLin](https://github.com/TonsnakeLin)

    TiDBはキーパーティショニングをサポートするようになりました。キーパーティショニングとハッシュパーティショニングはどちらも、データを一定数のパーティションに均等に分散できます。違いは、ハッシュパーティショニングは指定された整数式または整数列に基づいてのみデータを分散できるのに対し、キーパーティショニングは列リストに基づいてデータを分散できる点です。また、キーパーティショニングのパーティション列は整数型に限定されません。

    詳細については、[ドキュメント](/partitioned-table.md#key-partitioning)を参照してください。

### データベース操作 {#db-operations}

-   TiCDC はストレージサービスへの変更データのレプリケーションをサポート (GA) [#6797](https://github.com/pingcap/tiflow/issues/6797) @[zhaoxinyu](https://github.com/zhaoxinyu)

    TiCDCは、変更されたデータをAmazon S3、GCS、Azure Blob Storage、NFS、およびその他のS3互換ストレージサービスに複製することをサポートしています。ストレージサービスは手頃な価格で使いやすく、Kafkaを使用していない場合は、ストレージサービスを利用できます。TiCDCは変更ログをファイルに保存し、それをストレージサービスに送信します。ストレージサービスから、独自のコンシューマープログラムが新しく生成された変更ログファイルを定期的に読み取ることができます。現在、TiCDCはcanal-jsonおよびCSV形式の変更ログをストレージサービスに複製することをサポートしています。

    詳細については、[ドキュメント](/ticdc/ticdc-sink-to-cloud-storage.md)を参照してください。

-   TiCDC OpenAPI v2 [#8019](https://github.com/pingcap/tiflow/issues/8019) @[sdojjy](https://github.com/sdojjy)

    TiCDCはOpenAPI v2を提供します。OpenAPI v1と比較して、OpenAPI v2はレプリケーションタスクをより包括的にサポートします。TiCDC OpenAPIが提供する機能は、 [`cdc cli`ツール](/ticdc/ticdc-manage-changefeed.md)の機能の一部です。OpenAPI v2を介してTiCDCクラスタを照会および操作できます。例えば、TiCDCノードの状態取得、クラスタの健全性状態の確認、レプリケーションタスクの管理などが可能です。

    詳細については、[ドキュメント](/ticdc/ticdc-open-api-v2.md)を参照してください。

-   [DBeaver](https://dbeaver.io/) v23.0.1 はデフォルトで TiDB をサポートします [#17396](https://github.com/dbeaver/dbeaver/issues/17396) @[Icemap](https://github.com/Icemap)

    -   独立したTiDBモジュール、アイコン、およびロゴを提供します。
    -   デフォルト設定では[TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)がサポートされているため、 TiDB Cloud Starterへの接続が容易になります。
    -   TiDBのバージョンを識別して、外部キーのタブを表示または非表示にする機能をサポートしています。
    -   `EXPLAIN`結果に SQL 実行プランを視覚化することをサポートします。
    -   `PESSIMISTIC` 、 `OPTIMISTIC` 、 `AUTO_RANDOM` 、 `PLACEMENT` 、 `POLICY` 、 `REORGANIZE` 、 `EXCHANGE` 、 `CACHE` 、 `NONCLUSTERED` 、 `CLUSTERED`などの TiDB キーワードの強調表示をサポートします。
    -   `TIDB_BOUNDED_STALENESS` 、 `TIDB_DECODE_KEY` 、 `TIDB_DECODE_PLAN` 、 `TIDB_IS_DDL_OWNER` 、 `TIDB_PARSE_TSO` 、 `TIDB_VERSION` 、 `TIDB_DECODE_SQL_DIGESTS` 、 `TIDB_SHARD`などのTiDB関数の強調表示をサポートします。

    詳細については、 [DBeaverのドキュメント](https://github.com/dbeaver/dbeaver/wiki)を参照してください。

### データ移行 {#data-migration}

-   `LOAD DATA`ステートメントの機能を強化し、クラウドストレージからのデータインポートをサポートする (実験的) [#40499](https://github.com/pingcap/tidb/issues/40499) @[lance6716](https://github.com/lance6716)

    TiDB v7.0.0 より前は、 `LOAD DATA`ステートメントではクライアント側からのデータ ファイルのインポートしかできませんでした。クラウドストレージからデータをインポートするには、 TiDB Lightningを使用する必要がありました。しかし、 TiDB Lightning を別途デプロイすると、追加のデプロイおよび管理コストが発生します。v7.0.0 では、 `LOAD DATA`ステートメントを使用してクラウドストレージから直接データをインポートできます。この機能の例を以下に示します。

    -   Amazon S3およびGoogle Cloud StorageからTiDBへのデータインポートをサポートします。ワイルドカードを使用して、複数のソースファイルを一度にTiDBにインポートすることをサポートします。
    -   `DEFINED NULL BY`を使用して null を定義することをサポートします。
    -   CSVおよびTSV形式のソースファイルをサポートします。

    詳細については、 [ドキュメント](/sql-statements/sql-statement-load-data.md)を参照してください。

-   TiDB Lightning は、キーと値のペアを TiKV (GA) に送信する際の圧縮転送の有効化をサポートします [#41163](https://github.com/pingcap/tidb/issues/41163) @[sleepymole](https://github.com/sleepymole)

    バージョン6.6.0以降、 TiDB Lightningは、ローカルでエンコードおよびソートされたキーと値のペアをTiKVに送信する際に圧縮してネットワーク転送する機能をサポートしており、ネットワーク経由で転送されるデータ量を削減し、ネットワーク帯域幅のオーバーヘッドを低減します。この機能がサポートされる以前のTiDBバージョンでは、 TiDB Lightningは比較的高いネットワーク帯域幅を必要とし、データ量が多い場合には高額なトラフィック料金が発生していました。

    バージョン7.0.0では、この機能は一般提供（GA）となり、デフォルトでは無効になっています。有効にするには、 TiDB Lightningの設定項目`compress-kv-pairs`を`"gzip"`または`"gz"` 。

    詳細については、 [ドキュメント](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)を参照してください。

## 互換性の変更 {#compatibility-changes}

> **Note:**
>
> このセクションでは、バージョン6.6.0から最新バージョン（バージョン7.0.0）にアップグレードする際に知っておくべき互換性の変更点について説明します。バージョン6.5.0以前のバージョンから最新バージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更点も確認する必要があるかもしれません。

### MySQLとの互換性 {#mysql-compatibility}

-   TiDBは、AUTO_INCREMENT列がインデックスでなければならないという制約を削除します [#40580](https://github.com/pingcap/tidb/issues/40580) @[tiancaiamao](https://github.com/tiancaiamao)

    バージョン 7.0.0 より前は、TiDB の動作は MySQL と一貫しており、AUTO_INCREMENT列はインデックスまたはインデックスプレフィックスである必要がありました。バージョン 7.0.0 以降、TiDB はAUTO_INCREMENT列がインデックスまたはインデックスプレフィックスである必要があるという制約を撤廃しました。これにより、テーブルの主キーをより柔軟に定義し、AUTO_INCREMENT列を使用してソートやページネーションをより簡単に実装できるようになりました。また、AUTO_INCREMENT列によって引き起こされる書き込みホットスポットの問題も回避され、クラスター化インデックスを持つテーブルを使用することでクエリのパフォーマンスが向上します。新しいリリースでは、次の構文を使用してテーブルを作成できます。

    ```sql
    CREATE TABLE test1 (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `k` int(11) NOT NULL DEFAULT '0',
        `c` char(120) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
        PRIMARY KEY(`k`, `id`)
    );
    ```

    この機能はTiCDCのデータレプリケーションには影響しません。

    詳細については、 [ドキュメント](/mysql-compatibility.md#auto-increment-id)を参照してください。

-   TiDBは、次の例に示すように、キーパーティションをサポートしています。

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

    バージョン7.0.0以降、TiDBはキーパーティションをサポートし、MySQLの`PARTITION BY LINEAR KEY`構文を解析できます。ただし、TiDBは`LINEAR`キーワードを無視し、代わりに非線形ハッシュアルゴリズムを使用します。現在、 `KEY`パーティションタイプは、空のパーティション列リストを持つパーティションステートメントをサポートしていません。

    詳細については、[ドキュメント](/partitioned-table.md#key-partitioning)を参照してください。

### 動作の変更 {#behavior-changes}

-   TiCDC は、Avro の `FLOAT` データの不正なエンコードの問題を修正しました [#8490](https://github.com/pingcap/tiflow/issues/8490) @[3AceShowHand](https://github.com/3AceShowHand)

    TiCDC クラスターを v7.0.0 にアップグレードする際、Avro を使用してレプリケートされたテーブルに`FLOAT`データ型が含まれている場合は、アップグレード前に Confluent Schema Registry の互換性ポリシーを`None`に手動で調整する必要があります。そうしないと、changefeed がスキーマを正常に更新できなくなります。そうしないと、アップグレード後に changefeed がスキーマを更新できず、エラー状態になります。

-   v7.0.0 以降、 [`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size)システム変数は[`LOAD DATA`ステートメント](/sql-statements/sql-statement-load-data.md)に影響しなくなりました。

### システム変数 {#system-variables}

| 変数名                                                                                                                               | 変更の種類  | 説明                                                                                                                                                                                         |
| --------------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `tidb_pessimistic_txn_aggressive_locking`                                                                                         | 削除済み     | この変数は[`tidb_pessimistic_txn_fair_locking`](/system-variables.md#tidb_pessimistic_txn_fair_locking-new-in-v700)に名前が変更されました。                                                                 |
| [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache)                                 | 変更     | v7.0.0 から有効になり、[非プリペアドプランキャッシュ](/sql-non-prepared-plan-cache.md)機能を有効にするかどうかを制御します。                                                                                                      |
| [`tidb_enable_null_aware_anti_join`](/system-variables.md#tidb_enable_null_aware_anti_join-new-in-v630)                           | 変更     | さらなるテストの後、デフォルト値を`OFF`から`ON`に変更します。これは、特別なセット演算子`NOT IN`および`!= ALL`によってリードされるサブクエリによって Anti Join が生成される場合に、TiDB がデフォルトで Null-Aware Hash Join を適用することを意味します。                                |
| [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660)                                   | 変更     | デフォルト値を`OFF`から`ON`に変更します。これは、クラスターがデフォルトでリソースグループごとにリソースを分離することを意味します。リソース制御は v7.0.0 でデフォルトで有効になっているため、いつでもこの機能を使用できます。                                                                    |
| [`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size)                                     | 変更     | v7.0.0 から有効になり、[非プリペアドプランキャッシュ](/sql-non-prepared-plan-cache.md)によってキャッシュできる実行プランの最大数を制御します。                                                                                             |
| [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-new-in-v600)                                                 | 変更     | バージョン7.0.0以降、この変数はプリペアドステートメントプロトコルにおけるカーソルフェッチ読み取りには有効ではなくなりました。                                                                                                                          |
| [`tidb_enable_inl_join_inner_multi_pattern`](/system-variables.md#tidb_enable_inl_join_inner_multi_pattern-new-in-v700)           | 新しく追加された | この変数は、内部テーブルに`Selection`または`Projection`演算子がある場合に、インデックス結合がサポートされるかどうかを制御します。                                                                                                               |
| [`tidb_enable_plan_cache_for_subquery`](/system-variables.md#tidb_enable_plan_cache_for_subquery-new-in-v700)                     | 新しく追加された | この変数は、プリペアドプランキャッシュがサブクエリを含むクエリをキャッシュするかどうかを制御します。                                                                                                                                         |
| [`tidb_enable_plan_replayer_continuous_capture`](/system-variables.md#tidb_enable_plan_replayer_continuous_capture-new-in-v700)   | 新しく追加された | この変数は、 [`PLAN REPLAYER CONTINUOUS CAPTURE`](/sql-plan-replayer.md#use-plan-replayer-continuous-capture)機能を有効にするかどうかを制御します。デフォルト値の`OFF`は、この機能を無効にすることを意味します。                                |
| [`tidb_load_based_replica_read_threshold`](/system-variables.md#tidb_load_based_replica_read_threshold-new-in-v700)               | 新しく追加された | この変数は、負荷ベースのレプリカ読み取りをトリガーするしきい値を設定します。この変数で制御される機能は、TiDB v7.0.0 では完全には動作しません。デフォルト値は変更しないでください。                                                                                            |
| [`tidb_opt_advanced_join_hint`](/system-variables.md#tidb_opt_advanced_join_hint-new-in-v700)                                     | 新しく追加された | この変数は、結合メソッドヒントが結合順序の最適化に影響するかどうかを制御します。デフォルト値は`ON`で、これは新しい互換制御モードが使用されることを意味します。値`OFF`は、v7.0.0 より前の動作が使用されることを意味します。前方互換性のために、クラスターが以前のバージョンから v7.0.0 以降にアップグレードされると、この変数の値は`OFF`に設定されます。 |
| [`tidb_opt_derive_topn`](/system-variables.md#tidb_opt_derive_topn-new-in-v700)                                                   | 新しく追加された | この変数は[ウィンドウ関数からTopNまたはLimitを導出する](/derive-topn-from-window.md)最適化ルールを有効にするかどうかを制御します。デフォルト値は`OFF`で、最適化ルールが有効になっていないことを意味します。                                                               |
| [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-new-in-v700)                   | 新しく追加された | この変数は[TiFlashの遅延発生](/tiflash/tiflash-late-materialization.md)機能を有効にするかどうかを制御します。デフォルト値は`OFF`で、これは機能が有効になっていないことを意味します。                                                                     |
| [`tidb_opt_ordering_index_selectivity_threshold`](/system-variables.md#tidb_opt_ordering_index_selectivity_threshold-new-in-v700) | 新しく追加された | この変数は、SQL ステートメントに`ORDER BY`および`LIMIT`句が含まれ、フィルタリング条件がある場合に、オプティマイザがインデックスを選択する方法を制御します。                                                                                                   |
| [`tidb_pessimistic_txn_fair_locking`](/system-variables.md#tidb_pessimistic_txn_fair_locking-new-in-v700)                         | 新しく追加された | 単一行競合シナリオにおけるトランザクションのテールレイテンシーを削減するために、拡張悲観的ロックウェイクモデルを有効にするかどうかを制御します。デフォルト値は`ON`です。クラスタが以前のバージョンから v7.0.0 以降にアップグレードされると、この変数の値は`OFF`に設定されます。                                           |
| [`tidb_slow_txn_log_threshold`](/system-variables.md#tidb_slow_txn_log_threshold-new-in-v700)                                     | 新しく追加された | トランザクションのログ記録のしきい値を設定します。トランザクションの実行時間がこのしきい値を超えると、TiDB はトランザクションに関する詳細情報をログに記録します。デフォルト値`0`は、この機能が無効になっていることを意味します。                                                                       |
| [`tidb_ttl_running_tasks`](/system-variables.md#tidb_ttl_running_tasks-new-in-v700)                                               | 新しく追加された | この変数は、クラスタ全体におけるTTLタスクの同時実行数を制限するために使用されます。デフォルト値`-1`は、TTLタスクの数がTiKVノードの数と同じであることを意味します。                                                                                                   |

### コンフィグレーションファイルパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                      | 変更の種類  | 説明                                                                                                                                                                                                                                                                        |
| -------------- | ---------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiKV           | `server.snap-max-write-bytes-per-sec`                                                                | 削除済み     | このパラメータは[`server.snap-io-max-bytes-per-sec`](/tikv-configuration-file.md#snap-io-max-bytes-per-sec)に名前が変更されました。                                                                                                                                                           |
| TiKV           | [`raft-engine.enable-log-recycle`](/tikv-configuration-file.md#enable-log-recycle-new-in-v630)       | 変更     | デフォルト値が`false`から`true`に変更されます。                                                                                                                                                                                                                                            |
| TiKV           | [`resolved-ts.advance-ts-interval`](/tikv-configuration-file.md#advance-ts-interval)                 | 変更     | デフォルト値が`"1s"`から`"20s"`に変更されます。この変更により、Resolved TSの定期的な更新間隔が長くなり、TiKVノード間のトラフィック消費量が削減されます。                                                                                                                                                                                |
| TiKV           | [`resource-control.enabled`](/tikv-configuration-file.md#resource-control)                           | 変更     | デフォルト値が`false`から`true`に変更されます。                                                                                                                                                                                                                                            |
| TiKV           | [`raft-engine.prefill-for-recycle`](/tikv-configuration-file.md#prefill-for-recycle-new-in-v700)     | 新しく追加された | Raft Engineのログリサイクル用に空のログファイルを生成するかどうかを制御します。デフォルト値は`false`です。                                                                                                                                                                                                            |
| PD             | [`degraded-mode-wait-duration`](/pd-configuration-file.md#degraded-mode-wait-duration)               | 新しく追加された | [リソース制御](/tidb-resource-control-ru-groups.md)関連する設定項目です。劣化モードをトリガーするまでの待機時間を制御します。デフォルト値は`0s`です。                                                                                                                                                                          |
| PD             | [`read-base-cost`](/pd-configuration-file.md#read-base-cost)                                         | 新しく追加された | A[リソース制御](/tidb-resource-control-ru-groups.md)関連する設定項目です。読み取り要求から RU への変換の基準係数を制御します。デフォルト値は`0.25`です。                                                                                                                                                                     |
| PD             | [`read-cost-per-byte`](/pd-configuration-file.md#read-cost-per-byte)                                 | 新しく追加された | A[リソース制御](/tidb-resource-control-ru-groups.md)関連する設定項目です。読み取りフローからRUへの変換の基準係数を制御します。デフォルト値は`1/ (64 * 1024)`です。                                                                                                                                                            |
| PD             | [`read-cpu-ms-cost`](/pd-configuration-file.md#read-cpu-ms-cost)                                     | 新しく追加された | [リソース制御](/tidb-resource-control-ru-groups.md)関連する設定項目です。CPUからRUへの変換の基準係数を制御します。デフォルト値は`1/3`です。                                                                                                                                                                            |
| PD             | [`write-base-cost`](/pd-configuration-file.md#write-base-cost)                                       | 新しく追加された | [リソース制御](/tidb-resource-control-ru-groups.md)関連の設定項目です。書き込み要求からRUへの変換の基準係数を制御します。デフォルト値は`1`です。                                                                                                                                                                            |
| PD             | [`write-cost-per-byte`](/pd-configuration-file.md#write-cost-per-byte)                               | 新しく追加された | [リソース制御](/tidb-resource-control-ru-groups.md)関連の設定項目です。書き込みフローからRUへの変換の基準係数を制御します。デフォルト値は`1/1024`です。                                                                                                                                                                      |
| TiFlash        | [`mark_cache_size`](/tiflash/tiflash-configuration.md)                                               | 変更     | TiFlashのデータブロックのメタデータのデフォルトのキャッシュ制限を`5368709120`から`1073741824`に変更して、不要なメモリ使用量を削減します。                                                                                                                                                                                      |
| TiFlash        | [`minmax_index_cache_size`](/tiflash/tiflash-configuration.md)                                       | 変更     | TiFlashのデータブロックの最小-最大インデックスのデフォルトのキャッシュ制限を`5368709120`から`1073741824`に変更して、不要なメモリ使用量を削減します。                                                                                                                                                                                |
| TiFlash        | [`flash.disaggregated_mode`](/tiflash/tiflash-disaggregated-and-s3.md)                               | 新しく追加された | TiFlashの分散アーキテクチャでは、このTiFlashノードが書き込みノードか計算ノードかを示します。値は`tiflash_write`または`tiflash_compute`になります。                                                                                                                                                                          |
| TiFlash        | [`storage.s3.endpoint`](/tiflash/tiflash-disaggregated-and-s3.md)                                    | 新しく追加された | S3に接続するためのエンドポイント。                                                                                                                                                                                                                                                        |
| TiFlash        | [`storage.s3.bucket`](/tiflash/tiflash-disaggregated-and-s3.md)                                      | 新しく追加された | TiFlashがすべてのデータを保存するバケット。                                                                                                                                                                                                                                                 |
| TiFlash        | [`storage.s3.root`](/tiflash/tiflash-disaggregated-and-s3.md)                                        | 新しく追加された | S3バケット内のデータストレージのルートディレクトリ。                                                                                                                                                                                                                                             |
| TiFlash        | [`storage.s3.access_key_id`](/tiflash/tiflash-disaggregated-and-s3.md)                               | 新しく追加された | `ACCESS_KEY_ID` S3 にアクセスするためのものです。                                                                                                                                                                                                                                        |
| TiFlash        | [`storage.s3.secret_access_key`](/tiflash/tiflash-disaggregated-and-s3.md)                           | 新しく追加された | `SECRET_ACCESS_KEY` S3 にアクセスするためのものです。                                                                                                                                                                                                                                    |
| TiFlash        | [`storage.remote.cache.dir`](/tiflash/tiflash-disaggregated-and-s3.md)                               | 新しく追加された | TiFlashコンピューティングノードのローカルデータキャッシュディレクトリ。                                                                                                                                                                                                                                   |
| TiFlash        | [`storage.remote.cache.capacity`](/tiflash/tiflash-disaggregated-and-s3.md)                          | 新しく追加された | TiFlashコンピューティングノードのローカルデータキャッシュディレクトリのサイズ。                                                                                                                                                                                                                               |
| TiDB Lightning | [`add-index-by-sql`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)            | 新しく追加された | 物理インポートモードでインデックスを追加する際に SQL を使用するかどうかを制御します。デフォルト値は`false`で、これはTiDB Lightning が行データとインデックスデータの両方を KV ペアにエンコードし、それらをまとめて TiKV にインポートすることを意味します。SQL を使用してインデックスを追加する利点は、データのインポートとインデックスのインポートを分離できるため、データを迅速にインポートできることです。データのインポート後にインデックスの作成が失敗した場合でも、データの一貫性は影響を受けません。 |
| TiCDC          | [`enable-table-across-nodes`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters) | 新しく追加された | リージョン数に応じて、テーブルを複数の同期範囲に分割するかどうかを決定します。これらの範囲は、複数のTiCDCノードによって複製できます。                                                                                                                                                                                                     |
| TiCDC          | [`region-threshold`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)          | 新しく追加された | `enable-table-across-nodes`が有効になっている場合、この機能は`region-threshold`を超えるリージョンを持つテーブルでのみ有効になります。                                                                                                                                                                                 |
| DM             | [`analyze`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)           | 新しく追加された | チェックサムの完了後に各テーブルで`ANALYZE TABLE <table>`操作を実行するかどうかを制御します。 `"required"` / `"optional"` / `"off"` 。デフォルト値は`"optional"`です。                                                                                                                                                  |
| DM             | [`range-concurrency`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced) | 新しく追加された | dm-workerがKVデータをTiKVに書き込む際の同時実行数を制御します。                                                                                                                                                                                                                                   |
| DM             | [`compress-kv-pairs`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced) | 新しく追加された | dm-workerがKVデータをTiKVに送信する際に圧縮を有効にするかどうかを制御します。現在サポートされているのはgzipのみです。デフォルト値は空欄で、これは圧縮しないことを意味します。                                                                                                                                                                          |
| DM             | [`pd-addr`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)           | 新しく追加された | 物理インポートモードにおけるダウンストリームPDサーバーのアドレスを制御します。1つまたは複数のPDサーバーを指定できます。この設定項目が空欄の場合、デフォルトではTiDBクエリから取得したPDアドレス情報が使用されます。                                                                                                                                                           |

## 改善点 {#improvements}

-   TiDB

    -   `EXPAND`演算子を導入し、単一の`DISTINCT`ステートメントに複数の`SELECT`を含むSQLクエリのパフォーマンスを最適化します [#16581](https://github.com/pingcap/tidb/issues/16581) @[AilinKid](https://github.com/AilinKid)
    -   インデックス結合でより多くのSQL形式をサポートする [#40505](https://github.com/pingcap/tidb/issues/40505) @[Yisaer](https://github.com/Yisaer)
    -   場合によっては、TiDB でパーティションテーブルデータをグローバルに並べ替えないようにする [#26166](https://github.com/pingcap/tidb/issues/26166) @[Defined2014](https://github.com/Defined2014)
    -   `fair lock mode`と`lock only if exists`の同時使用をサポート [#42068](https://github.com/pingcap/tidb/issues/42068) @[MyonKeminta](https://github.com/MyonKeminta)
    -   トランザクションのスローログとトランザクション内部イベントの印刷をサポートする [#41863](https://github.com/pingcap/tidb/issues/41863) @[ekexium](https://github.com/ekexium)
    -   `ILIKE` オペレーターをサポートします [#40943](https://github.com/pingcap/tidb/issues/40943) @[xzhangxian1008](https://github.com/xzhangxian1008)

-   PD

    -   ストア制限によるスケジューリング失敗に関する新しい監視メトリックを追加 [#6043](https://github.com/tikv/pd/issues/6043) @[nolouch](https://github.com/nolouch)

-   TiFlash

    -   書き込みパスでの TiFlash のメモリ使用量を削減 [#7144](https://github.com/pingcap/tiflash/issues/7144) @[hongyunyan](https://github.com/hongyunyan)
    -   テーブルが多いシナリオでの TiFlash の再起動時間を短縮する [#7146](https://github.com/pingcap/tiflash/issues/7146) @[hongyunyan](https://github.com/hongyunyan)
    -   `ILIKE`オペレーターのプッシュダウンをサポートします [#6740](https://github.com/pingcap/tiflash/issues/6740) @[xzhangxian1008](https://github.com/xzhangxian1008)

-   ツール

    -   TiCDC

        -   Kafkaがダウンストリームとなるシナリオにおいて、単一の大規模テーブルのデータ変更を複数のTiCDCノードに分散することをサポートし、大規模TiDBクラスタのデータ統合シナリオにおける単一テーブルのスケーラビリティ問題を解決します [#8247](https://github.com/pingcap/tiflow/issues/8247) @[overvenus](https://github.com/overvenus)

            TiCDC 構成項目`enable_table_across_nodes`を`true`に設定することで、この機能を有効にできます。 `region_threshold`を使用すると、テーブルのリージョン数がこのしきい値を超えた場合に、TiCDC が対応するテーブルのデータ変更を複数の TiCDC ノードに分散するように指定できます。

        -   リドゥアプライヤーにおけるトランザクション分割をサポートし、スループットを向上させ、ディザスタリカバリシナリオにおけるRTOを短縮する [#8318](https://github.com/pingcap/tiflow/issues/8318) @[CharlesCheung96](https://github.com/CharlesCheung96)

        -   テーブルのスケジューリングを改善して、単一のテーブルをさまざまな TiCDC ノード間でより均等に分割します [#8247](https://github.com/pingcap/tiflow/issues/8247) @[overvenus](https://github.com/overvenus)

        -   MQ シンクに Large Row モニタリング メトリクスを追加します [#8286](https://github.com/pingcap/tiflow/issues/8286) @[Rustin170506](https://github.com/Rustin170506)

        -   リージョンに複数のテーブルのデータが含まれるシナリオで、TiKV ノードと TiCDC ノード間のネットワーク トラフィックを削減します [#6346](https://github.com/pingcap/tiflow/issues/6346) @[overvenus](https://github.com/overvenus)

        -   Checkpoint TSとResolved TSのP99メトリクスパネルをラグ分析パネルに移動します [#8524](https://github.com/pingcap/tiflow/issues/8524) @[Rustin170506](https://github.com/Rustin170506)

        -   リドゥログへのDDLイベントの適用をサポートする [#8361](https://github.com/pingcap/tiflow/issues/8361) @[CharlesCheung96](https://github.com/CharlesCheung96)

        -   アップストリーム書き込みスループットに基づいて TiCDC ノードへのテーブルの分割とスケジュールをサポート [#7720](https://github.com/pingcap/tiflow/issues/7720) @[overvenus](https://github.com/overvenus)

    -   TiDB Lightning

        -   TiDB Lightning物理インポート モードは、データ インポートとインデックス インポートの分離をサポートし、インポート速度と安定性を向上させます [#42132](https://github.com/pingcap/tidb/issues/42132) @[sleepymole](https://github.com/sleepymole)

            `add-index-by-sql`パラメータを追加します。デフォルト値は`false`で、これはTiDB Lightning が行データとインデックスデータの両方を KV ペアにエンコードし、それらをまとめて TiKV にインポートすることを意味します。これを`true`に設定すると、 TiDB Lightningデータのインポート後に`ADD INDEX` SQL ステートメントを使用してインデックスを追加し、インポートの速度と安定性を向上させます。

        -   `tikv-importer.keyspace-name`パラメータを追加します。デフォルト値は空の文字列で、 TiDB Lightning は対応するテナントのキースペース名を自動的に取得してデータをインポートします。値を指定すると、指定されたキースペース名を使用してデータがインポートされます。このパラメータにより、マルチテナント TiDB クラスタにデータをインポートする際のTiDB Lightningの設定に柔軟性が生まれます。 [#41915](https://github.com/pingcap/tidb/issues/41915) @[lichunzhu](https://github.com/lichunzhu)

## バグ修正 {#bug-fixes}

-   TiDB

    -   TiDBをv6.5.1からそれ以降のバージョンにアップグレードする際にアップデートが欠落する問題を修正 [#41502](https://github.com/pingcap/tidb/issues/41502) @[chrysan](https://github.com/chrysan)
    -   アップグレード後に一部のシステム変数のデフォルト値が変更されない問題を修正 [#41423](https://github.com/pingcap/tidb/issues/41423) @[crazycs520](https://github.com/crazycs520)
    -   インデックス追加に関連するコプロセッサー要求タイプが不明として表示される問題を修正 [#41400](https://github.com/pingcap/tidb/issues/41400) @[tangenta](https://github.com/tangenta)
    -   インデックスを追加する際に「PessimisticLockNotFound」が返される問題を修正 [#41515](https://github.com/pingcap/tidb/issues/41515) @[tangenta](https://github.com/tangenta)
    -   一意インデックスを追加する際に誤って`found duplicate key`を返す問題を修正 [#41630](https://github.com/pingcap/tidb/issues/41630) @[tangenta](https://github.com/tangenta)
    -   インデックス追加時のpanic問題を修正 [#41880](https://github.com/pingcap/tidb/issues/41880) @[tangenta](https://github.com/tangenta)
    -   TiFlashが実行中に生成された列に対してエラーを報告する問題を修正 [#40663](https://github.com/pingcap/tidb/issues/40663) @[guo-shaoge](https://github.com/guo-shaoge)
    -   TiDBが時間型の場合に統計情報を正しく取得できない可能性がある問題を修正しました [#41938](https://github.com/pingcap/tidb/issues/41938) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    -   プリペアドプランキャッシュが有効になっている場合に、フルインデックススキャンでエラーが発生する可能性がある問題を修正しました [#42150](https://github.com/pingcap/tidb/issues/42150) @[fzzf678](https://github.com/fzzf678)
    -   `IFNULL(NOT NULL COLUMN, ...)`が間違った結果を返す可能性がある問題を修正 [#41734](https://github.com/pingcap/tidb/issues/41734) @[LittleFall](https://github.com/LittleFall)
    -   パーティションテーブル内のすべてのデータが単一のリージョンにある場合に、TiDBが誤った結果を生成する可能性がある問題を修正します [#41801](https://github.com/pingcap/tidb/issues/41801) @[Defined2014](https://github.com/Defined2014)
    -   TiDB で、異なるパーティション テーブルが単一の SQL ステートメントに現れる場合に誤った結果が生成される可能性がある問題を修正しました [#42135](https://github.com/pingcap/tidb/issues/42135) @[mjonss](https://github.com/mjonss)
    -   パーティションテーブルに新しいインデックスを追加した後、パーティションパーティションテーブルで統計情報の自動収集が正しくトリガーされない可能性がある問題を修正しました [#41638](https://github.com/pingcap/tidb/issues/41638) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    -   TiDBが統計情報を2回連続で収集した後に誤った列統計情報を読み取る可能性がある問題を修正 [#42073](https://github.com/pingcap/tidb/issues/42073) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    -   プリペアドプランキャッシュが有効になっている場合に IndexMerge が誤った結果を生成する可能性がある問題を修正しました [#41828](https://github.com/pingcap/tidb/issues/41828) @[qw4990](https://github.com/qw4990)
    -   IndexMerge に goroutine リークがある可能性がある問題を修正 [#41605](https://github.com/pingcap/tidb/issues/41605) @[guo-shaoge](https://github.com/guo-shaoge)
    -   非 BIGINT 符号なし整数が文字列/10 進数と比較したときに誤った結果を生成する可能性がある問題を修正 [#41736](https://github.com/pingcap/tidb/issues/41736) @[LittleFall](https://github.com/LittleFall)
    -   メモリ制限超過により以前の`ANALYZE`ステートメントが強制終了されると、同じセッション内の現在の`ANALYZE`ステートメントも強制終了される可能性がある問題を修正しました [#41825](https://github.com/pingcap/tidb/issues/41825) @[XuHuaiyu](https://github.com/XuHuaiyu)
    -   バッチコプロセッサの情報収集プロセス中にデータ競合が発生する可能性がある問題を修正しました [#41412](https://github.com/pingcap/tidb/issues/41412) @[you06](https://github.com/you06)
    -   アサーション エラーによりパーティション テーブルの MVCC 情報が印刷できない問題を修正 [#40629](https://github.com/pingcap/tidb/issues/40629) @[ekexium](https://github.com/ekexium)
    -   フェアロックモードで存在しないキーにロックが追加される問題を修正 [#41527](https://github.com/pingcap/tidb/issues/41527) @[ekexium](https://github.com/ekexium)
    -   `INSERT IGNORE`および`REPLACE`ステートメントが値を変更しないキーをロックしない問題を修正 [#42121](https://github.com/pingcap/tidb/issues/42121) @[zyguan](https://github.com/zyguan)

-   PD

    -   リージョンスキャッター操作でリーダーの分布が不均一になる可能性がある問題を修正 [#6017](https://github.com/tikv/pd/issues/6017) @[HunDunDM](https://github.com/HunDunDM)
    -   起動時にPDメンバーを取得する際にデータ競合が発生する可能性がある問題を修正 [#6069](https://github.com/tikv/pd/issues/6069) @[rleungx](https://github.com/rleungx)
    -   ホットスポット統計情報の収集時にデータ競合が発生する可能性がある問題を修正 [#6069](https://github.com/tikv/pd/issues/6069) @[lhy1024](https://github.com/lhy1024)
    -   配置ルールの切り替えによりリーダーの分布が不均一になる可能性がある問題を修正 [#6195](https://github.com/tikv/pd/issues/6195) @[bufferflies](https://github.com/bufferflies)

-   TiFlash

    -   特定の場合に小数の除算で最後の桁が切り上げられない問題を修正 [#7022](https://github.com/pingcap/tiflash/issues/7022) @[LittleFall](https://github.com/LittleFall)
    -   特定のケースで Decimal キャストが誤って切り上げられる問題を修正 [#6994](https://github.com/pingcap/tiflash/issues/6994) @[windtalker](https://github.com/windtalker)
    -   新しい照合順序を有効にした後、TopN/Sort演算子が誤った結果を生成する問題を修正します [#6807](https://github.com/pingcap/tiflash/issues/6807) @[xzhangxian1008](https://github.com/xzhangxian1008)
    -   単一のTiFlashノード上で 1,200 万行を超える結果セットを集計するときにTiFlash がエラーを報告する問題を修正 [#6993](https://github.com/pingcap/tiflash/issues/6993) @[windtalker](https://github.com/windtalker)

-   ツール

    -   Backup & Restore (BR)

        -   PITRリカバリプロセス中のリージョン分割再試行の待機時間が不十分な問題を修正 [#42001](https://github.com/pingcap/tidb/issues/42001) @[joccau](https://github.com/joccau)
        -   PITRリカバリプロセス中に発生した`memory is limited`エラーによるリカバリ失敗の問題を修正 [#41983](https://github.com/pingcap/tidb/issues/41983) @[joccau](https://github.com/joccau)
        -   PD ノードがダウンしているときに PITR ログのバックアップの進行状況が進まない問題を修正 [#14184](https://github.com/tikv/tikv/issues/14184) @[YuJuncen](https://github.com/YuJuncen)
        -   リージョンリーダーシップの移行時にPITRログバックアップのレイテンシーが増加する問題を軽減する [#13638](https://github.com/tikv/tikv/issues/13638) @[YuJuncen](https://github.com/YuJuncen)

    -   TiCDC

        -   チェンジフィードを再開するとデータが失われる可能性がある、またはチェックポイントが先に進めないという問題を修正 [#8242](https://github.com/pingcap/tiflow/issues/8242) @[overvenus](https://github.com/overvenus)
        -   DDL シンクのデータ競合問題を修正 [#8238](https://github.com/pingcap/tiflow/issues/8238) @[3AceShowHand](https://github.com/3AceShowHand)
        -   `stopped`ステータスの変更フィードが自動的に再起動する可能性がある問題を修正 [#8330](https://github.com/pingcap/tiflow/issues/8330) @[sdojjy](https://github.com/sdojjy)
        -   すべてのダウンストリーム Kafka サーバーが利用できないときに TiCDCサーバーがパニックになる問題を修正 [#8523](https://github.com/pingcap/tiflow/issues/8523) @[3AceShowHand](https://github.com/3AceShowHand)
        -   ダウンストリームがMySQLで、実行されたステートメントがTiDBと互換性がない場合にデータが失われる可能性がある問題を修正します [#8453](https://github.com/pingcap/tiflow/issues/8453) @[asddongmen](https://github.com/asddongmen)
        -   ローリング アップグレードが TiCDC OOM を引き起こす可能性がある問題、またはチェックポイントがスタックする問題を修正 [#8329](https://github.com/pingcap/tiflow/issues/8329) @[overvenus](https://github.com/overvenus)
        -   Kubernetes で TiCDC クラスターの正常なアップグレードが失敗する問題を修正 [#8484](https://github.com/pingcap/tiflow/issues/8484) @[overvenus](https://github.com/overvenus)

    -   TiDB Data Migration (DM)

        -   DMワーカーノードがGoogle Cloud Storageを使用する際に、ブレークポイントが多すぎるためにGoogle Cloud Storageのリクエスト頻度制限に達し、DMワーカーがGoogle Cloud Storageにデータを書き込めなくなり、結果としてデータ全体の読み込みに失敗する問題を修正しました。 [#8482](https://github.com/pingcap/tiflow/issues/8482) @[maxshuang](https://github.com/maxshuang)
        -   複数のDMタスクが同時に同じダウンストリームデータを複製し、すべてがダウンストリームメタデータテーブルを使用してブレークポイント情報を記録する場合、すべてのタスクのブレークポイント情報が同じメタデータテーブルに書き込まれ、同じタスクIDが使用される問題を修正しました。 [#8500](https://github.com/pingcap/tiflow/issues/8500) @[maxshuang](https://github.com/maxshuang)

    -   TiDB Lightning

        -   物理インポートモードを使用してデータをインポートする場合、対象テーブルの複合主キーに`auto_random`列が存在するが、ソースデータでその列の値が指定されていない場合、 TiDB Lightning が`auto_random`列のデータを自動的に生成しない問題を修正しました。 [#41454](https://github.com/pingcap/tidb/issues/41454) @[D3Hunter](https://github.com/D3Hunter)
        -   論理インポートモードを使用してデータをインポートする際に、ターゲットクラスターに対する`CONFIG`権限がないためにインポートが失敗する問題を修正しました [#41915](https://github.com/pingcap/tidb/issues/41915) @[lichunzhu](https://github.com/lichunzhu)

## 貢献者 {#contributors}

TiDBコミュニティの以下の貢献者の皆様に感謝申し上げます。

-   [AntiTopQuark](https://github.com/AntiTopQuark)
-   [blacktear23](https://github.com/blacktear23)
-   [BornChanger](https://github.com/BornChanger)
-   [Dousir9](https://github.com/Dousir9)
-   [erwadba](https://github.com/erwadba)
-   [happy-v587](https://github.com/happy-v587)
-   [jiyfhust](https://github.com/jiyfhust)
-   [L-maple](https://github.com/L-maple)
-   [liumengya94](https://github.com/liumengya94)
-   [woofyzhao](https://github.com/woofyzhao)
-   [xiaguan](https://github.com/xiaguan)
