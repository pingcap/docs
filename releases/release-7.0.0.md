---
title: TiDB 7.0.0 Release Notes
summary: TiDB 7.0.0 の新機能、互換性の変更、改善点、バグ修正について説明します。
---

# TiDB 7.0.0 リリースノート {#tidb-7-0-0-release-notes}

発売日：2023年3月30日

TiDB バージョン: 7.0.0- [DMR](/releases/versioning.md#development-milestone-releases)

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.0/quick-start-with-tidb)

v7.0.0-DMR の主な新機能と改善点は次のとおりです。

<table><thead><tr><th>カテゴリ</th><th>特徴</th><th>説明</th></tr></thead><tbody><tr><td rowspan="2">スケーラビリティとパフォーマンス<br/></td><td>セッション レベルの<a href="https://docs.pingcap.com/tidb/v7.0/sql-non-prepared-plan-cache" target="_blank">非準備 SQL プラン キャッシュ</a>(実験的)</td><td>セッション レベルでプラン キャッシュを自動的に再利用することをサポートし、事前に準備ステートメントを手動で設定することなく、コンパイルを減らし、同じ SQL パターンのクエリ時間を短縮します。</td></tr><tr><td> TiFlash は<a href="https://docs.pingcap.com/tidb/v7.0/tiflash-disaggregated-and-s3" target="_blank">、分散storageとコンピューティングアーキテクチャ、および S3 共有storage</a>(実験的) をサポートします。</td><td> TiFlash は、オプションとしてクラウドネイティブアーキテクチャを導入します。<ul><li> TiFlash のコンピューティングとstorageを分離します。これは、弾力性のある HTAP リソース利用のマイルストーンとなります。</li><li>低コストで共有storageを提供できる S3 ベースのstorageエンジンを導入します。</li></ul></td></tr><tr><td rowspan="2">信頼性と可用性<br/></td><td><a href="https://docs.pingcap.com/tidb/v7.0/tidb-resource-control" target="_blank">リソース制御の強化</a>（実験的）</td><td>リソースグループを使用して、単一クラスタ内の様々なアプリケーションやワークロードにリソースを割り当て、分離できるようになりました。このリリースでは、TiDB は、異なるリソースバインディングモード（ユーザーレベル、セッションレベル、ステートメントレベル）とユーザー定義の優先順位のサポートを追加しました。さらに、コマンドを使用してリソースキャリブレーション（リソース全体の使用量の見積もり）を実行することもできます。</td></tr><tr><td> TiFlashは<a href="https://docs.pingcap.com/tidb/v7.0/tiflash-spill-disk" target="_blank">ディスクへの書き込み</a>をサポート</td><td>TiFlash は、集約、ソート、ハッシュ結合などのデータ集約型操作における OOM を軽減するために、ディスクへの中間結果のスピルをサポートします。</td></tr><tr><td rowspan="2"> SQL</td><td><a href="https://docs.pingcap.com/tidb/v7.0/time-to-live" target="_blank">行レベルの TTL</a> (GA)</td><td>一定の期間が経過したデータを自動的に期限切れにすることで、データベース サイズの管理をサポートし、パフォーマンスを向上します。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v7.0/partitioned-table#reorganize-partitions" target="_blank"><code>LIST</code> / <code>RANGE</code>パーティションの再編成</a></td><td><code>REORGANIZE PARTITION</code>ステートメントは、隣接するパーティションを結合したり、1 つのパーティションを複数のパーティションに分割したりするために使用でき、パーティション化されたテーブルの使いやすさが向上します。</td></tr><tr><td rowspan="2"> DB操作と可観測性<br/></td><td>TiDB は<a href="https://docs.pingcap.com/tidb/v7.0/sql-statement-load-data" target="_blank"><code>LOAD DATA</code>ステートメント</a>の機能を強化します (実験的)</td><td> TiDB は、S3/GCS からのデータインポートのサポートなど、 <code>LOAD DATA</code> SQL ステートメントの機能を強化します。<br/></td></tr><tr><td> TiCDC は<a href="https://docs.pingcap.com/tidb/v7.0/ticdc-sink-to-cloud-storage" target="_blank">オブジェクトstorageシンク</a>(GA) をサポートします</td><td>TiCDC は、Amazon S3、GCS、Azure Blob Storage、NFS などのオブジェクトstorageサービスへの行変更イベントの複製をサポートしています。<br/></td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### スケーラビリティ {#scalability}

-   TiFlashは、分散storageとコンピューティングアーキテクチャをサポートし、このアーキテクチャでオブジェクトstorageをサポートします（実験的） [＃6882](https://github.com/pingcap/tiflash/issues/6882) @ [フロービーハッピー](https://github.com/flowbehappy)

    v7.0.0より前のTiFlashは、storageとコンピューティングを組み合わせたアーキテクチャのみをサポートしています。このアーキテクチャでは、各TiFlashノードはstorageとコンピューティングノードの両方として機能し、コンピューティング機能とstorage機能を個別に拡張することはできません。また、 TiFlashノードはローカルstorageのみを使用できます。

    v7.0.0以降、 TiFlashは分散storageおよびコンピューティングアーキテクチャもサポートします。このアーキテクチャでは、 TiFlashノードは2種類（コンピューティングノードと書き込みノード）に分かれており、S3 APIと互換性のあるオブジェクトstorageをサポートします。どちらの種類のノードも、コンピューティング容量またはstorage容量に合わせて個別に拡張できます。**分散storageおよびコンピューティングアーキテクチャと**、**結合storageおよびコンピューティングアーキテクチャは**、同じクラスター内で使用したり、相互に変換したりすることはできません。TiFlashをデプロイする際に、使用するアーキテクチャを設定できます。

    詳細については[ドキュメント](/tiflash/tiflash-disaggregated-and-s3.md)参照してください。

### パフォーマンス {#performance}

-   高速オンラインDDLとPITR [＃38045](https://github.com/pingcap/tidb/issues/38045) @ [リーヴルス](https://github.com/Leavrth)間の互換性を実現

    TiDB v6.5.0では、 [高速オンラインDDL](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) [PITR](/br/backup-and-restore-overview.md)と完全に互換性がありません。完全なデータバックアップを確実に行うには、まずPITRバックグラウンドバックアップタスクを停止し、Fast Online DDLを使用してインデックスを素早く追加してから、PITRバックアップタスクを再開することをお勧めします。

    TiDB v7.0.0以降、Fast Online DDLとPITRは完全に互換性があります。PITRを介してクラスターデータをリストアする場合、ログバックアップ中にFast Online DDLによって追加されたインデックス操作は、互換性を確保するために自動的に再生されます。

    詳細については[ドキュメント](/ddl-introduction.md)参照してください。

-   TiFlashは、null認識のセミ結合演算子とnull認識のアンチセミ結合演算子[＃6674](https://github.com/pingcap/tiflash/issues/6674) @ [ゲンリキ](https://github.com/gengliqi)をサポートしています。

    相関サブクエリで`IN` 、 `NOT IN` 、 `= ANY` 、または`!= ALL`演算子を使用する場合、TiDB はそれらをセミ結合またはアンチセミ結合に変換することで計算パフォーマンスを最適化します。結合キー列が`NULL`なる可能性がある場合は、 [Null認識セミ結合](/explain-subqueries.md#null-aware-semi-join-in-and--any-subqueries)や[null 認識アンチセミ結合](/explain-subqueries.md#null-aware-anti-semi-join-not-in-and--all-subqueries)などの null を認識する結合アルゴリズムが必要です。

    バージョン7.0.0より前のTiFlash、null対応セミ結合演算子とnull対応アンチセミ結合演算子をサポートしていないため、これらのサブクエリをTiFlashに直接プッシュダウンすることはできませんでした。バージョン7.0.0以降、 TiFlashはnull対応セミ結合演算子とnull対応アンチセミ結合演算子をサポートします。SQL文にこれらの相関サブクエリが含まれており、クエリ内のテーブルにTiFlashレプリカがあり、 [MPPモード](/tiflash/use-tiflash-mpp-mode.md)有効になっている場合、オプティマイザーはnull対応セミ結合演算子とnull対応アンチセミ結合演算子をTiFlashにプッシュダウンするかどうかを自動的に判断し、全体的なパフォーマンスを向上させます。

    詳細については[ドキュメント](/tiflash/tiflash-supported-pushdown-calculations.md)参照してください。

-   TiFlashはFastScan（GA） [＃5252](https://github.com/pingcap/tiflash/issues/5252) @ [ホンユニャン](https://github.com/hongyunyan)の使用をサポートします

    TiFlash v6.3.0 以降、FastScan は実験的機能として導入されました。v7.0.0 では、この機能が一般公開されます。FastScan はシステム変数[`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-new-in-v630)使って有効化できます。この機能は、強力な一貫性を犠牲にすることで、テーブルスキャンのパフォーマンスを大幅に向上させます。対象となるテーブルで`UPDATE` `DELETE`のオペレーションが含まれず、 `INSERT`回のオペレーションのみが含まれる場合、FastScan は強力な一貫性を維持し、スキャンパフォーマンスを向上させることができます。

    詳細については[ドキュメント](/tiflash/use-fastscan.md)参照してください。

-   TiFlash は遅延マテリアライゼーションをサポートします (実験的) [＃5829](https://github.com/pingcap/tiflash/issues/5829) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)

    フィルタ条件（ `WHERE`節）を含む`SELECT`文を処理する際、 TiFlashはデフォルトでクエリに必要な列からすべてのデータを読み取り、クエリ条件に基づいてデータをフィルタリングおよび集計します。遅延マテリアライゼーションは、フィルタ条件の一部をTableScan演算子にプッシュダウンすることをサポートする最適化手法です。つまり、 TiFlashはまずプッシュダウンされたフィルタ条件に関連する列データをスキャンし、条件を満たす行をフィルタリングした後、これらの行の他の列データをスキャンしてさらなる計算を行うことで、データ処理のIOスキャンと計算を削減します。

    TiFlash の遅延マテリアライゼーション機能はデフォルトでは有効になっていません。システム変数`tidb_opt_enable_late_materialization` `OFF`に設定することで有効にできます。この機能を有効にすると、TiDB オプティマイザーは統計情報とフィルター条件に基づいて、プッシュダウンするフィルター条件を決定します。

    詳細については[ドキュメント](/tiflash/tiflash-late-materialization.md)参照してください。

-   非準備済みステートメントの実行プランのキャッシュをサポート（実験的） [＃36598](https://github.com/pingcap/tidb/issues/36598) @ [qw4990](https://github.com/qw4990)

    実行プランキャッシュは、同時実行OLTPの負荷容量を向上させる上で重要であり、TiDBはすでに[準備された実行プランのキャッシュ](/sql-prepared-plan-cache.md)サポートしています。v7.0.0では、TiDBは非Prepareステートメントの実行プランもキャッシュできるようになり、実行プランキャッシュの範囲が拡大され、TiDBの同時処理容量が向上しました。

    この機能はデフォルトで無効になっています。システム変数[`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache)を`ON`に設定することで有効にできます。安定性を確保するため、TiDB v7.0.0 では、準備されていない実行計画をキャッシュするための新しい領域が割り当てられており、キャッシュサイズはシステム変数[`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size)を使用して設定できます。また、この機能にはSQL文に対する一定の制限があります。詳細については、 [制限](/sql-non-prepared-plan-cache.md#restrictions)参照してください。

    詳細については[ドキュメント](/sql-non-prepared-plan-cache.md)参照してください。

-   TiDBはサブクエリ[＃40219](https://github.com/pingcap/tidb/issues/40219) @ [fzzf678](https://github.com/fzzf678)の実行プランのキャッシュ制約を削除します。

    TiDB v7.0.0では、サブクエリの実行計画キャッシュ制約が削除されました。これにより、 `SELECT * FROM t WHERE a > (SELECT ...)`ようにサブクエリを含むSQL文の実行計画をキャッシュできるようになりました。この機能により、実行計画キャッシュの適用範囲がさらに拡大し、SQLクエリの実行効率が向上します。

    詳細については[ドキュメント](/sql-prepared-plan-cache.md)参照してください。

-   TiKVは、ログリサイクル[＃14371](https://github.com/tikv/tikv/issues/14371) @ [LykxSassinator](https://github.com/LykxSassinator)の空のログファイルの自動生成をサポートします。

    TiKV v6.3.0では、書き込み負荷によるロングテールレイテンシーを削減する機能[Raft丸太のリサイクル](/tikv-configuration-file.md#enable-log-recycle-new-in-v630)導入されました。しかし、ログリサイクルはRaftログファイルの数が一定の閾値に達した場合にのみ有効になるため、ユーザーがこの機能によるスループットの向上を直接体験することは困難です。

    バージョン7.0.0では、ユーザーエクスペリエンスを向上させるために、新しい設定項目「 `raft-engine.prefill-for-recycle`が導入されました。この設定項目は、プロセス開始時にリサイクル用の空のログファイルを生成するかどうかを制御します。この設定を有効にすると、TiKVは初期化中に空のログファイルを自動的にバッチ処理し、初期化直後にログのリサイクルが有効になります。

    詳細については[ドキュメント](/tikv-configuration-file.md#prefill-for-recycle-new-in-v700)参照してください。

-   ウィンドウ関数のパフォーマンスを向上させるために、TopN または Limit 演算子を[ウィンドウ関数](/functions-and-operators/expressions-pushed-down.md)から導出するサポート[＃13936](https://github.com/tikv/tikv/issues/13936) @ [ウィンドトーカー](https://github.com/windtalker)

    この機能はデフォルトで無効になっています。有効にするには、セッション変数[tidb_opt_derive_topn](/system-variables.md#tidb_opt_derive_topn-new-in-v700)を`ON`に設定します。

    詳細については[ドキュメント](/derive-topn-from-window.md)参照してください。

-   高速オンライン DDL [＃40730](https://github.com/pingcap/tidb/issues/40730) @ [接線](https://github.com/tangenta)による一意のインデックスの作成をサポート

    TiDB v6.5.0は、Fast Online DDLによる通常のセカンダリインデックスの作成をサポートします。TiDB v7.0.0は、Fast Online DDLによるユニークインデックスの作成をサポートします。v6.1.0と比較すると、大規模テーブルへのユニークインデックスの追加は、パフォーマンスの向上により数倍高速化されると予想されます。

    詳細については[ドキュメント](/ddl-introduction.md)参照してください。

### 信頼性 {#reliability}

-   リソース制御機能の強化（実験的） [＃38825](https://github.com/pingcap/tidb/issues/38825) @ [ノルーシュ](https://github.com/nolouch) @ [生まれ変わった人](https://github.com/BornChanger) @ [栄光](https://github.com/glorv) @ [天菜まお](https://github.com/tiancaiamao) @ [コナー1996](https://github.com/Connor1996) @ [Jmポテト](https://github.com/JmPotato) @ [ネス](https://github.com/hnes) @ [キャビンフィーバーB](https://github.com/CabinfeverB) @ [HuSharp](https://github.com/HuSharp)

    TiDBは、リソースグループに基づくリソース制御機能を強化しました。この機能により、TiDBクラスタのリソース利用効率とパフォーマンスが大幅に向上します。リソース制御機能の導入は、TiDBにとって画期的な出来事です。分散データベースクラスタを複数の論理ユニットに分割し、異なるデータベースユーザーを対応するリソースグループにマッピングし、必要に応じて各リソースグループのクォータを設定できます。クラスタリソースが制限されている場合、同じリソースグループ内のセッションで使用されるすべてのリソースはクォータに制限されます。これにより、あるリソースグループが過剰に消費されても、他のリソースグループのセッションには影響しません。

    この機能により、異なるシステムの複数の中小規模アプリケーションを単一のTiDBクラスタに統合できます。あるアプリケーションのワークロードが大きくなっても、他のアプリケーションの正常な動作に影響を与えることはありません。システムのワークロードが低い場合は、設定されたクォータを超えても、高負荷のアプリケーションに必要なシステムリソースを割り当てることができるため、リソースを最大限に活用できます。さらに、リソース制御機能を合理的に活用することで、クラスタ数を削減し、運用・保守の難易度を軽減し、管理コストを削減できます。

    この機能は、Grafanaのリソースの実際の使用状況を把握できる組み込みのリソース管理ダッシュボードを提供し、より合理的なリソース割り当てを支援します。また、セッションレベルとステートメントレベル（ヒント）の両方に基づいた動的なリソース管理機能もサポートしています。この機能の導入により、TiDBクラスターのリソース使用状況をより正確に制御し、実際のニーズに基づいてクォータを動的に調整できるようになります。

    TiDB v7.0.0では、リソースグループに絶対的なスケジューリング優先度（ `PRIORITY` ）を設定できるようになりました。これにより、重要なサービスが確実にリソースを確保できるようになります。また、リソースグループの設定方法も拡張されます。

    リソース グループは次の方法で使用できます。

    -   ユーザーレベル。1 または[`CREATE USER`](/sql-statements/sql-statement-create-user.md) [`ALTER USER`](/sql-statements/sql-statement-alter-user.md)ステートメントを使用して、ユーザーを特定のリソースグループにバインドします。リソースグループをユーザーにバインドすると、そのユーザーが新たに作成したセッションは、対応するリソースグループに自動的にバインドされます。
    -   セッションレベル。1 を介して現在の[`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md)で使用されるリソースグループを設定します。
    -   ステートメントレベル[`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name)を介して現在のステートメントで使用されるリソースグループを設定します。

    詳細については[ドキュメント](/tidb-resource-control.md)参照してください。

-   高速オンラインDDLのチェックポイントメカニズムをサポートし、フォールトトレランスと自動リカバリ機能を向上させます[＃42164](https://github.com/pingcap/tidb/issues/42164) @ [接線](https://github.com/tangenta)

    TiDB v7.0.0では、 [高速オンラインDDL](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)にチェックポイント機構が導入され、フォールトトレランスと自動リカバリ機能が大幅に向上しました。DDLの進行状況を定期的に記録・同期することで、TiDB DDLオーナーの障害発生時や切り替え時でも、実行中のDDL操作を高速オンラインDDLモードで継続実行できます。これにより、DDL実行の安定性と効率性が向上します。

    詳細については[ドキュメント](/ddl-introduction.md)参照してください。

-   TiFlashはディスク[＃6528](https://github.com/pingcap/tiflash/issues/6528) @ [ウィンドトーカー](https://github.com/windtalker)への書き込みをサポート

    実行パフォーマンスを向上させるため、 TiFlashは可能な限りデータをメモリ内で実行します。データ量がメモリの総量を超えると、メモリ不足によるシステムクラッシュを回避するため、 TiFlashはクエリを終了します。そのため、 TiFlashが処理できるデータ量は、利用可能なメモリによって制限されます。

    TiFlash v7.0.0以降、ディスクへの書き込みがサポートされます。演算子（ [`tidb_max_bytes_before_tiflash_external_group_by`](/system-variables.md#tidb_max_bytes_before_tiflash_external_group_by-new-in-v700) ）のメモリ使用量のしきい値を調整することで、演算子が使用できるメモリの最大量を制御できます。演算子が使用するメモリがしきい値を超えると、自動的にデータがディスクに書き込まれます。これによりパフォーマンスは多少犠牲[`tidb_max_bytes_before_tiflash_external_join`](/system-variables.md#tidb_max_bytes_before_tiflash_external_join-new-in-v700) [`tidb_max_bytes_before_tiflash_external_sort`](/system-variables.md#tidb_max_bytes_before_tiflash_external_sort-new-in-v700)ますが、より多くのデータを処理できるようになります。

    詳細については[ドキュメント](/tiflash/tiflash-spill-disk.md)参照してください。

-   統計収集の効率を向上[＃41930](https://github.com/pingcap/tidb/issues/41930) @ [xuyifangreeneyes](https://github.com/xuyifangreeneyes)

    TiDB v7.0.0では、統計収集ロジックがさらに最適化され、収集時間が約25%短縮されました。この最適化により、大規模データベースクラスターの運用効率と安定性が向上し、統計収集がクラスターのパフォーマンスに与える影響が軽減されます。

-   MPP 最適化[＃39710](https://github.com/pingcap/tidb/issues/39710) @ [思い出させる](https://github.com/Reminiscent)の新しいオプティマイザーヒントを追加します

    v7.0.0 では、TiDB は MPP 実行プランの生成に影響を与える一連のオプティマイザー ヒントを追加します。

    -   [`SHUFFLE_JOIN()`](/optimizer-hints.md#shuffle_joint1_name--tl_name-) : MPP に有効です。指定されたテーブルに対してシャッフル結合アルゴリズムを使用するようオプティマイザに指示します。
    -   [`BROADCAST_JOIN()`](/optimizer-hints.md#broadcast_joint1_name--tl_name-) : MPP で有効になります。指定されたテーブルに対してブロードキャスト結合アルゴリズムを使用するようオプティマイザに指示します。
    -   [`MPP_1PHASE_AGG()`](/optimizer-hints.md#mpp_1phase_agg) : MPP で有効になります。指定されたクエリブロック内のすべての集計関数に対して、1 フェーズ集計アルゴリズムを使用するようにオプティマイザに指示します。
    -   [`MPP_2PHASE_AGG()`](/optimizer-hints.md#mpp_2phase_agg) : MPP で有効になります。指定されたクエリブロック内のすべての集計関数に対して、2 フェーズ集計アルゴリズムを使用するようにオプティマイザに指示します。

    MPP オプティマイザーヒントは、HTAP クエリに介入して、HTAP ワークロードのパフォーマンスと安定性を向上させるのに役立ちます。

    詳細については[ドキュメント](/optimizer-hints.md)参照してください。

-   オプティマイザヒントは結合方法と結合順序の指定をサポートします[＃36600](https://github.com/pingcap/tidb/issues/36600) @ [思い出させる](https://github.com/Reminiscent)

    バージョン7.0.0では、オプティマイザヒント[`LEADING()`](/optimizer-hints.md#leadingt1_name--tl_name-)結合方法に影響を与えるヒントと組み合わせて使用でき、それらの動作は互換性があります。複数テーブルの結合の場合、最適な結合方法と結合順序を効果的に指定できるため、実行プランに対するオプティマイザヒントの制御が強化されます。

    新しいヒントの動作には若干の変更があります。前方互換性を確保するため、TiDB ではシステム変数[`tidb_opt_advanced_join_hint`](/system-variables.md#tidb_opt_advanced_join_hint-new-in-v700)が導入されています。この変数を`OFF`に設定すると、オプティマイザーヒントの動作は以前のバージョンと互換性があります。クラスターを以前のバージョンから v7.0.0 以降にアップグレードすると、この変数は`OFF`に設定されます。より柔軟なヒント動作を得るには、動作によってパフォーマンスの低下が発生しないことを確認した上で、この変数を`ON`に設定することを強くお勧めします。

    詳細については[ドキュメント](/optimizer-hints.md)参照してください。

### 可用性 {#availability}

-   `prefer-leader`オプションをサポートすることで、読み取り操作の可用性が向上し、不安定なネットワーク状況での応答レイテンシーが短縮されます[＃40905](https://github.com/pingcap/tidb/issues/40905) @ [LykxSassinator](https://github.com/LykxSassinator)

    TiDBのデータ読み取り動作は、システム変数[`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40)介して制御できます。バージョン7.0.0では、この変数に`prefer-leader`オプションが追加されました。変数を`prefer-leader`に設定すると、TiDBはリーダーレプリカを優先的に選択して読み取り操作を実行します。ディスクやネットワークのパフォーマンス変動などにより、リーダーレプリカの処理速度が大幅に低下した場合、TiDBは利用可能な他のフォロワーレプリカを選択して読み取り操作を実行するため、可用性が向上し、応答レイテンシーが短縮されます。

    詳細については[ドキュメント](/develop/dev-guide-use-follower-read.md)参照してください。

### SQL {#sql}

-   有効期限（TTL）は、通常[＃39262](https://github.com/pingcap/tidb/issues/39262) @ [lcwangchao](https://github.com/lcwangchao) @ [ヤンケオ](https://github.com/YangKeao)で利用可能です。

    TTLは行レベルのライフサイクル制御ポリシーを提供します。TiDBでは、TTL属性が設定されたテーブルは、設定に基づいて期限切れの行データを自動的にチェックし、削除します。TTLの目的は、ユーザーが不要なデータを定期的に適切なタイミングでクリーンアップし、クラスタワークロードへの影響を最小限に抑えることです。

    詳細については[ドキュメント](/time-to-live.md)参照してください。

-   サポート`ALTER TABLE…REORGANIZE PARTITION` [＃15000](https://github.com/pingcap/tidb/issues/15000) @ [ミョンス](https://github.com/mjonss)

    TiDBは`ALTER TABLE...REORGANIZE PARTITION`構文をサポートしています。この構文を使用すると、データを失うことなく、テーブルのパーティションの一部またはすべてを再編成（マージ、分割、その他の変更を含む）できます。

    詳細については[ドキュメント](/partitioned-table.md#reorganize-partitions)参照してください。

-   キー分割[＃41364](https://github.com/pingcap/tidb/issues/41364) @ [トンスネークリン](https://github.com/TonsnakeLin)をサポート

    TiDBはキーパーティショニングをサポートするようになりました。キーパーティショニングとハッシュパーティショニングはどちらも、データを一定数のパーティションに均等に分散できます。ただし、ハッシュパーティショニングは指定された整数式または整数列に基づくデータの分散のみをサポートするのに対し、キーパーティショニングは列リストに基づくデータの分散をサポートし、キーパーティショニングの列のパーティションは整数型に限定されません。

    詳細については[ドキュメント](/partitioned-table.md#key-partitioning)参照してください。

### DB操作 {#db-operations}

-   TiCDC は、変更データをstorageサービスに複製することをサポートします (GA) [＃6797](https://github.com/pingcap/tiflow/issues/6797) @ [ジャオシンユ](https://github.com/zhaoxinyu)

    TiCDCは、Amazon S3、GCS、Azure Blob Storage、NFS、その他のS3互換storageサービスへの変更データのレプリケーションをサポートしています。ストレージサービスは価格が手頃で使いやすいです。Kafkaを使用していない場合は、storageサービスをご利用いただけます。TiCDCは変更ログをファイルに保存し、代わりにstorageサービスに送信します。storageサービスから、独自のコンシューマープログラムは新しく生成された変更ログファイルを定期的に読み取ることができます。現在、TiCDCはcanal-json形式とCSV形式での変更ログをstorageサービスにレプリケーションすることをサポートしています。

    詳細については[ドキュメント](/ticdc/ticdc-sink-to-cloud-storage.md)参照してください。

-   TiCDC オープン API v2 [＃8019](https://github.com/pingcap/tiflow/issues/8019) @ [スドジ](https://github.com/sdojjy)

    TiCDCはOpenAPI v2を提供します。OpenAPI v1と比較して、OpenAPI v2はレプリケーションタスクに対するより包括的なサポートを提供します。TiCDC OpenAPIが提供する機能は、 [`cdc cli`ツール](/ticdc/ticdc-manage-changefeed.md)のサブセットです。OpenAPI v2を介して、TiCDCノードのステータスの取得、クラスターのヘルスステータスの確認、レプリケーションタスクの管理など、TiCDCクラスターのクエリと操作を行うことができます。

    詳細については[ドキュメント](/ticdc/ticdc-open-api-v2.md)参照してください。

-   [DBeaver](https://dbeaver.io/) v23.0.1 はデフォルトで TiDB をサポートします[＃17396](https://github.com/dbeaver/dbeaver/issues/17396) @ [アイスマップ](https://github.com/Icemap)

    -   独立した TiDB モジュール、アイコン、ロゴを提供します。
    -   デフォルト構成では[{{{ .スターター }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)サポートされているため、{{{ .starter }}} への接続が容易になります。
    -   外部キー タブを表示または非表示にするために TiDB のバージョンを識別することをサポートします。
    -   `EXPLAIN`結果で SQL 実行プランの視覚化をサポートします。
    -   `PESSIMISTIC` `REORGANIZE`の TiDB `AUTO_RANDOM` `PLACEMENT` `CLUSTERED`表示`OPTIMISTIC` `CACHE` `EXCHANGE` `NONCLUSTERED` `POLICY`
    -   `TIDB_BOUNDED_STALENESS` `TIDB_IS_DDL_OWNER`の`TIDB_VERSION`関数の`TIDB_DECODE_KEY`表示`TIDB_DECODE_PLAN`サポート`TIDB_DECODE_SQL_DIGESTS` `TIDB_SHARD` `TIDB_PARSE_TSO`

    詳細については[DBeaver ドキュメント](https://github.com/dbeaver/dbeaver/wiki)参照してください。

### データ移行 {#data-migration}

-   `LOAD DATA`ステートメントの機能を強化し、クラウドstorageからのデータのインポートをサポートします (実験的) [＃40499](https://github.com/pingcap/tidb/issues/40499) @ [ランス6716](https://github.com/lance6716)

    TiDB v7.0.0より前のバージョンでは、 `LOAD DATA`ステートメントはクライアント側からのデータファイルのインポートのみが可能でした。クラウドstorageからデータをインポートするには、 TiDB Lightningを使用する必要がありました。しかし、 TiDB Lightningを別途導入すると、導入コストと管理コストが増加します。v7.0.0では、 `LOAD DATA`ステートメントを使用してクラウドstorageから直接データをインポートできます。この機能の具体的な例を以下に示します。

    -   Amazon S3およびGoogle Cloud StorageからTiDBへのデータのインポートをサポートします。ワイルドカードを使用して、複数のソースファイルを一度にTiDBにインポートできます。
    -   `DEFINED NULL BY`を使用して null を定義することをサポートします。
    -   CSV および TSV 形式のソース ファイルをサポートします。

    詳細については[ドキュメント](/sql-statements/sql-statement-load-data.md)参照してください。

-   TiDB Lightningは、 TiKV（GA） [＃41163](https://github.com/pingcap/tidb/issues/41163) @ [眠そうなモグラ](https://github.com/sleepymole)にキーと値のペアを送信するときに圧縮転送を有効にすることをサポートします。

    v6.6.0以降、 TiDB Lightningは、ローカルでエンコードおよびソートされたキーと値のペアをTiKVに送信する際に、ネットワーク転送用に圧縮することをサポートします。これにより、ネットワーク経由で転送されるデータ量が削減され、ネットワーク帯域幅のオーバーヘッドが低減されます。この機能がサポートされる以前のTiDBバージョンでは、 TiDB Lightningは比較的高いネットワーク帯域幅を必要とし、大量のデータを扱う場合には高額なトラフィック料金が発生していました。

    この機能はv7.0.0でGAとなり、デフォルトでは無効になっています。有効にするには、 TiDB Lightningの設定項目`compress-kv-pairs` `"gzip"`または`"gz"`に設定してください。

    詳細については[ドキュメント](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)参照してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、v6.6.0から最新バージョン（v7.0.0）にアップグレードする際に知っておくべき互換性の変更点について説明します。v6.5.0以前のバージョンから最新バージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更点も確認する必要があるかもしれません。

### MySQLの互換性 {#mysql-compatibility}

-   TiDBは、自動インクリメント列のインデックスが[＃40580](https://github.com/pingcap/tidb/issues/40580) @ [天菜まお](https://github.com/tiancaiamao)でなければならないという制約を削除します。

    バージョン7.0.0より前のTiDBの動作はMySQLと一貫性があり、自動インクリメント列はインデックスまたはインデックスプレフィックスである必要があります。バージョン7.0.0以降、TiDBは自動インクリメント列がインデックスまたはインデックスプレフィックスである必要があるという制約を削除します。これにより、テーブルの主キーをより柔軟に定義し、自動インクリメント列を使用してソートやページネーションをより便利に実装できるようになります。また、自動インクリメント列によって引き起こされる書き込みホットスポットの問題を回避し、クラスター化インデックスを持つテーブルを使用することでクエリパフォーマンスを向上させます。新しいリリースでは、次の構文を使用してテーブルを作成できます。

    ```sql
    CREATE TABLE test1 (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `k` int(11) NOT NULL DEFAULT '0',
        `c` char(120) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
        PRIMARY KEY(`k`, `id`)
    );
    ```

    この機能は TiCDC データレプリケーションには影響しません。

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

    TiDBはv7.0.0以降、キーパーティションをサポートし、MySQL `PARTITION BY LINEAR KEY`構文を解析できます。ただし、TiDBは`LINEAR`キーワードを無視し、代わりに非線形ハッシュアルゴリズムを使用します。現在、 `KEY`パーティションタイプでは、パーティション列リストが空のパーティションステートメントはサポートされていません。

    詳細については[ドキュメント](/partitioned-table.md#key-partitioning)参照してください。

### 行動の変化 {#behavior-changes}

-   TiCDCは、Avro [＃8490](https://github.com/pingcap/tiflow/issues/8490) @ [3エースショーハンド](https://github.com/3AceShowHand)で`FLOAT`データのエンコードが正しくない問題を修正しました。

    TiCDC クラスターを v7.0.0 にアップグレードする際、Avro を使用して複製されたテーブルに`FLOAT`データ型が含まれている場合は、アップグレード前に Confluent Schema Registry の互換性ポリシーを手動で`None`に調整し、changefeed がスキーマを正常に更新できるようにする必要があります。そうしないと、アップグレード後に changefeed がスキーマを更新できなくなり、エラー状態になります。

-   v7.0.0 以降、 [`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size)システム変数は[`LOAD DATA`文](/sql-statements/sql-statement-load-data.md)では有効になりません。

### システム変数 {#system-variables}

| 変数名                                                                                                                               | タイプを変更   | 説明                                                                                                                                                                                            |
| --------------------------------------------------------------------------------------------------------------------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `tidb_pessimistic_txn_aggressive_locking`                                                                                         | 削除済み     | この変数の名前は[`tidb_pessimistic_txn_fair_locking`](/system-variables.md#tidb_pessimistic_txn_fair_locking-new-in-v700)に変更されます。                                                                     |
| [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache)                                 | 修正済み     | v7.0.0 から有効になり、 [準備されていないプランキャッシュ](/sql-non-prepared-plan-cache.md)機能を有効にするかどうかを制御します。                                                                                                        |
| [`tidb_enable_null_aware_anti_join`](/system-variables.md#tidb_enable_null_aware_anti_join-new-in-v630)                           | 修正済み     | さらにテストを行った後、デフォルト値を`OFF`から`ON`に変更します。つまり、デフォルトで特殊セット演算子`NOT IN`および`!= ALL`始まるサブクエリによってアンチ結合が生成される場合、TiDB は Null 対応ハッシュ結合を適用します。                                                               |
| [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660)                                   | 修正済み     | デフォルト値を`OFF`から`ON`に変更します。これにより、クラスターはデフォルトでリソースをリソースグループごとに分離します。リソース制御はバージョン7.0.0ではデフォルトで有効になっているため、いつでもこの機能を使用できます。                                                                         |
| [`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size)                                     | 修正済み     | v7.0.0 から有効になり、キャッシュできる実行プランの最大数を[準備されていないプランキャッシュ](/sql-non-prepared-plan-cache.md)で制御します。                                                                                                   |
| [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-new-in-v600)                                                 | 修正済み     | バージョン 7.0.0 以降、この変数はプリペアドステートメントプロトコルのカーソル フェッチ読み取りには効果がありません。                                                                                                                                |
| [`tidb_enable_inl_join_inner_multi_pattern`](/system-variables.md#tidb_enable_inl_join_inner_multi_pattern-new-in-v700)           | 新しく追加された | この変数は、内部テーブルに`Selection`または`Projection`演算子がある場合にインデックス結合がサポートされるかどうかを制御します。                                                                                                                   |
| [`tidb_enable_plan_cache_for_subquery`](/system-variables.md#tidb_enable_plan_cache_for_subquery-new-in-v700)                     | 新しく追加された | この変数は、プリペアドプランキャッシュがサブクエリを含むクエリをキャッシュするかどうかを制御します。                                                                                                                                            |
| [`tidb_enable_plan_replayer_continuous_capture`](/system-variables.md#tidb_enable_plan_replayer_continuous_capture-new-in-v700)   | 新しく追加された | この変数は、 [`PLAN REPLAYER CONTINUOUS CAPTURE`](/sql-plan-replayer.md#use-plan-replayer-continuous-capture)機能を有効にするかどうかを制御します。デフォルト値`OFF` 、この機能を無効にすることを意味します。                                    |
| [`tidb_load_based_replica_read_threshold`](/system-variables.md#tidb_load_based_replica_read_threshold-new-in-v700)               | 新しく追加された | この変数は、負荷ベースのレプリカ読み取りをトリガーするためのしきい値を設定します。この変数によって制御される機能は、TiDB v7.0.0では完全には機能しません。デフォルト値を変更しないでください。                                                                                          |
| [`tidb_opt_advanced_join_hint`](/system-variables.md#tidb_opt_advanced_join_hint-new-in-v700)                                     | 新しく追加された | この変数は、結合方法のヒントが結合順序の最適化に影響を与えるかどうかを制御します。デフォルト値は`ON`で、新しい互換制御モードが使用されることを意味します。値`OFF` 、バージョン7.0.0より前の動作が使用されることを意味します。前方互換性のため、クラスターが以前のバージョンからバージョン7.0.0以降にアップグレードされた場合、この変数の値は`OFF`に設定されます。 |
| [`tidb_opt_derive_topn`](/system-variables.md#tidb_opt_derive_topn-new-in-v700)                                                   | 新しく追加された | この変数は、最適化ルール[ウィンドウ関数からTopNまたはLimitを導出する](/derive-topn-from-window.md)有効にするかどうかを制御します。デフォルト値は`OFF`で、最適化ルールは無効です。                                                                               |
| [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-new-in-v700)                   | 新しく追加された | この変数は、 [TiFlash遅延マテリアライゼーション](/tiflash/tiflash-late-materialization.md)機能を有効にするかどうかを制御します。デフォルト値は`OFF`で、この機能は無効です。                                                                            |
| [`tidb_opt_ordering_index_selectivity_threshold`](/system-variables.md#tidb_opt_ordering_index_selectivity_threshold-new-in-v700) | 新しく追加された | この変数は、SQL ステートメントに`ORDER BY`および`LIMIT`句が含まれ、フィルタリング条件がある場合に、オプティマイザーがインデックスを選択する方法を制御します。                                                                                                     |
| [`tidb_pessimistic_txn_fair_locking`](/system-variables.md#tidb_pessimistic_txn_fair_locking-new-in-v700)                         | 新しく追加された | 単一行競合シナリオにおけるトランザクションのテールレイテンシーを削減するために、拡張悲観的ロックウェイキングモデルを有効にするかどうかを制御します。デフォルト値は`ON`です。クラスターを以前のバージョンからv7.0.0以降にアップグレードすると、この変数の値は`OFF`に設定されます。                                              |
| [`tidb_slow_txn_log_threshold`](/system-variables.md#tidb_slow_txn_log_threshold-new-in-v700)                                     | 新しく追加された | 低速トランザクションログのしきい値を設定します。トランザクションの実行時間がこのしきい値を超えると、TiDBはトランザクションの詳細情報を記録します。デフォルト値の`0` 、この機能が無効であることを意味します。                                                                                    |
| [`tidb_ttl_running_tasks`](/system-variables.md#tidb_ttl_running_tasks-new-in-v700)                                               | 新しく追加された | この変数は、クラスター全体のTTLタスクの同時実行数を制限するために使用されます。デフォルト値の`-1` 、TTLタスクがTiKVノードの数と同じであることを意味します。                                                                                                         |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                      | タイプを変更   | 説明                                                                                                                                                                                                                                                |
| -------------- | ---------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiKV           | `server.snap-max-write-bytes-per-sec`                                                                | 削除済み     | このパラメータの名前は[`server.snap-io-max-bytes-per-sec`](/tikv-configuration-file.md#snap-io-max-bytes-per-sec)に変更されます。                                                                                                                                    |
| TiKV           | [`raft-engine.enable-log-recycle`](/tikv-configuration-file.md#enable-log-recycle-new-in-v630)       | 修正済み     | デフォルト値は`false`から`true`に変更されます。                                                                                                                                                                                                                    |
| TiKV           | [`resolved-ts.advance-ts-interval`](/tikv-configuration-file.md#advance-ts-interval)                 | 修正済み     | デフォルト値は`"1s"`から`"20s"`に変更されます。この変更により、Resolved TS の定期的な進行間隔が長くなり、TiKV ノード間のトラフィック消費量が削減されます。                                                                                                                                                      |
| TiKV           | [`resource-control.enabled`](/tikv-configuration-file.md#resource-control)                           | 修正済み     | デフォルト値は`false`から`true`に変更されます。                                                                                                                                                                                                                    |
| TiKV           | [`raft-engine.prefill-for-recycle`](/tikv-configuration-file.md#prefill-for-recycle-new-in-v700)     | 新しく追加された | Raft Engineのログリサイクル用に空のログファイルを生成するかどうかを制御します。デフォルト値は`false`です。                                                                                                                                                                                    |
| PD             | [`degraded-mode-wait-duration`](/pd-configuration-file.md#degraded-mode-wait-duration)               | 新しく追加された | [リソース管理](/tidb-resource-control.md)関連の設定項目です。縮退モードをトリガーするまでの待機時間を制御します。デフォルト値は`0s`です。                                                                                                                                                             |
| PD             | [`read-base-cost`](/pd-configuration-file.md#read-base-cost)                                         | 新しく追加された | [リソース管理](/tidb-resource-control.md)関連の設定項目です。読み取り要求から RU への変換における基準係数を制御します。デフォルト値は`0.25`です。                                                                                                                                                      |
| PD             | [`read-cost-per-byte`](/pd-configuration-file.md#read-cost-per-byte)                                 | 新しく追加された | [リソース管理](/tidb-resource-control.md)関連の設定項目です。読み取りフローから RU への変換の基準係数を制御します。デフォルト値は`1/ (64 * 1024)`です。                                                                                                                                              |
| PD             | [`read-cpu-ms-cost`](/pd-configuration-file.md#read-cpu-ms-cost)                                     | 新しく追加された | [リソース管理](/tidb-resource-control.md)関連の設定項目です。CPU から RU への変換における基準係数を制御します。デフォルト値は`1/3`です。                                                                                                                                                         |
| PD             | [`write-base-cost`](/pd-configuration-file.md#write-base-cost)                                       | 新しく追加された | [リソース管理](/tidb-resource-control.md)関連の設定項目です。書き込み要求から RU への変換の基準係数を制御します。デフォルト値は`1`です。                                                                                                                                                            |
| PD             | [`write-cost-per-byte`](/pd-configuration-file.md#write-cost-per-byte)                               | 新しく追加された | [リソース管理](/tidb-resource-control.md)関連の設定項目です。書き込みフローから RU への変換の基準係数を制御します。デフォルト値は`1/1024`です。                                                                                                                                                      |
| TiFlash        | [`mark_cache_size`](/tiflash/tiflash-configuration.md)                                               | 修正済み     | 不要なメモリ使用量を削減するために、 TiFlashのデータ ブロックのメタデータのデフォルトのキャッシュ制限を`5368709120`から`1073741824`に変更します。                                                                                                                                                         |
| TiFlash        | [`minmax_index_cache_size`](/tiflash/tiflash-configuration.md)                                       | 修正済み     | 不要なメモリ使用量を削減するために、 TiFlashのデータ ブロックの最小最大インデックスのデフォルトのキャッシュ制限を`5368709120`から`1073741824`に変更します。                                                                                                                                                    |
| TiFlash        | [`flash.disaggregated_mode`](/tiflash/tiflash-disaggregated-and-s3.md)                               | 新しく追加された | TiFlashの分散アーキテクチャにおいて、このTiFlashノードが書き込みノードか計算ノードかを示します。値は`tiflash_write`または`tiflash_compute`です。                                                                                                                                                   |
| TiFlash        | [`storage.s3.endpoint`](/tiflash/tiflash-disaggregated-and-s3.md)                                    | 新しく追加された | S3 に接続するためのエンドポイント。                                                                                                                                                                                                                               |
| TiFlash        | [`storage.s3.bucket`](/tiflash/tiflash-disaggregated-and-s3.md)                                      | 新しく追加された | TiFlash がすべてのデータを保存するバケット。                                                                                                                                                                                                                        |
| TiFlash        | [`storage.s3.root`](/tiflash/tiflash-disaggregated-and-s3.md)                                        | 新しく追加された | S3 バケット内のデータstorageのルート ディレクトリ。                                                                                                                                                                                                                   |
| TiFlash        | [`storage.s3.access_key_id`](/tiflash/tiflash-disaggregated-and-s3.md)                               | 新しく追加された | S3 にアクセスする場合は`ACCESS_KEY_ID` 。                                                                                                                                                                                                                    |
| TiFlash        | [`storage.s3.secret_access_key`](/tiflash/tiflash-disaggregated-and-s3.md)                           | 新しく追加された | S3 にアクセスする場合は`SECRET_ACCESS_KEY` 。                                                                                                                                                                                                                |
| TiFlash        | [`storage.remote.cache.dir`](/tiflash/tiflash-disaggregated-and-s3.md)                               | 新しく追加された | TiFlashコンピューティング ノードのローカル データ キャッシュ ディレクトリ。                                                                                                                                                                                                       |
| TiFlash        | [`storage.remote.cache.capacity`](/tiflash/tiflash-disaggregated-and-s3.md)                          | 新しく追加された | TiFlashコンピューティング ノードのローカル データ キャッシュ ディレクトリのサイズ。                                                                                                                                                                                                   |
| TiDB Lightning | [`add-index-by-sql`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)            | 新しく追加された | 物理インポートモードでSQLを使用してインデックスを追加するかどうかを制御します。デフォルト値は`false`で、 TiDB Lightningデータとインデックスデータの両方をKVペアにエンコードし、それらをまとめてTiKVにインポートします。SQLを使用してインデックスを追加する利点は、データのインポートとインデックスのインポートを分離することで、データを迅速にインポートできることです。データのインポート後にインデックスの作成に失敗しても、データの整合性は影響を受けません。 |
| TiCDC          | [`enable-table-across-nodes`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters) | 新しく追加された | リージョン数に応じて、テーブルを複数の同期範囲に分割するかどうかを決定します。これらの範囲は複数のTiCDCノードによって複製できます。                                                                                                                                                                              |
| TiCDC          | [`region-threshold`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)          | 新しく追加された | `enable-table-across-nodes`有効になっている場合、この機能は`region-threshold`以上のリージョンを持つテーブルにのみ適用されます。                                                                                                                                                            |
| DM             | [`analyze`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)           | 新しく追加された | CHECKSUMが完了した後`"optional"`各テーブルで`ANALYZE TABLE <table>`操作を実行するかどうかを制御します。3 / `"required"` / `"off"`に設定できます。デフォルト値は`"optional"`です。                                                                                                                 |
| DM             | [`range-concurrency`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced) | 新しく追加された | dm-worker が KV データを TiKV に書き込む同時実行を制御します。                                                                                                                                                                                                         |
| DM             | [`compress-kv-pairs`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced) | 新しく追加された | dm-workerがTiKVにKVデータを送信する際、圧縮を有効にするかどうかを制御します。現在、gzipのみがサポートされています。デフォルト値は空で、圧縮なしを意味します。                                                                                                                                                          |
| DM             | [`pd-addr`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)           | 新しく追加された | 物理インポートモードにおける下流PDサーバーのアドレスを制御します。1つまたは複数のPDサーバーを指定できます。この設定項目が空の場合、デフォルトでTiDBクエリから取得したPDアドレス情報が使用されます。                                                                                                                                           |

## 改善点 {#improvements}

-   TiDB

    -   `EXPAND`演算子を導入して、1 つの`SELECT`ステートメントに複数の`DISTINCT`含まれる SQL クエリのパフォーマンスを最適化します[＃16581](https://github.com/pingcap/tidb/issues/16581) @ [アイリンキッド](https://github.com/AilinKid)
    -   インデックス結合[＃40505](https://github.com/pingcap/tidb/issues/40505) @ [イーサール](https://github.com/Yisaer)より多くの SQL 形式をサポート
    -   TiDB でパーティションテーブルデータをグローバルにソートすることを避ける必要がある場合[＃26166](https://github.com/pingcap/tidb/issues/26166) @ [定義2014](https://github.com/Defined2014)
    -   `fair lock mode`と`lock only if exists`同時に使用してサポート[＃42068](https://github.com/pingcap/tidb/issues/42068) @ [ミョンケミンタ](https://github.com/MyonKeminta)
    -   トランザクションのスローログとトランザクション内部イベントの印刷をサポート[＃41863](https://github.com/pingcap/tidb/issues/41863) @ [エキシウム](https://github.com/ekexium)
    -   `ILIKE`オペレーター[＃40943](https://github.com/pingcap/tidb/issues/40943) @ [xzhangxian1008](https://github.com/xzhangxian1008)をサポート

-   PD

    -   店舗制限[＃6043](https://github.com/tikv/pd/issues/6043) @ [ノルーシュ](https://github.com/nolouch)によるスケジュール失敗の新しい監視メトリックを追加します

-   TiFlash

    -   書き込みパス[＃7144](https://github.com/pingcap/tiflash/issues/7144) @ [ホンユニャン](https://github.com/hongyunyan)でのTiFlashのメモリ使用量を削減
    -   多数のテーブル[＃7146](https://github.com/pingcap/tiflash/issues/7146) @ [ホンユニャン](https://github.com/hongyunyan)があるシナリオで TiFlash の再起動時間を短縮します
    -   `ILIKE`演算子[＃6740](https://github.com/pingcap/tiflash/issues/6740) @ [xzhangxian1008](https://github.com/xzhangxian1008)を押し下げるサポート

-   ツール

    -   TiCDC

        -   Kafka がダウンストリームであるシナリオで、単一の大きなテーブルのデータ変更を複数の TiCDC ノードに分散することをサポートし、大規模な TiDB クラスター[＃8247](https://github.com/pingcap/tiflow/issues/8247) @ [金星の上](https://github.com/overvenus)のデータ統合シナリオにおける単一テーブルのスケーラビリティの問題を解決します。

            この機能を有効にするには、TiCDC 設定項目`enable_table_across_nodes`を`true`に設定します。5 `region_threshold`指定すると、テーブルのリージョン数がこのしきい値を超えると、TiCDC は対応するテーブルのデータ変更を複数の TiCDC ノードに分散し始めます。

        -   災害復旧シナリオにおけるスループットの向上とRTOの短縮のために、REDOアプライヤでのトランザクション分割をサポートする[＃8318](https://github.com/pingcap/tiflow/issues/8318) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)

        -   テーブルスケジュールを改善し、単一のテーブルをさまざまな TiCDC ノード[＃8247](https://github.com/pingcap/tiflow/issues/8247) @ [金星の上](https://github.com/overvenus)に均等に分割します。

        -   MQシンク[＃8286](https://github.com/pingcap/tiflow/issues/8286) @ [ハイラスティン](https://github.com/Rustin170506)にLarge Rowモニタリングメトリクスを追加します。

        -   リージョンに複数のテーブル[＃6346](https://github.com/pingcap/tiflow/issues/6346) @ [金星の上](https://github.com/overvenus)のデータが含まれているシナリオで、TiKV ノードと TiCDC ノード間のネットワーク トラフィックを削減します。

        -   チェックポイントTSと解決TSのP99メトリックパネルをラグ分析パネル[＃8524](https://github.com/pingcap/tiflow/issues/8524) @ [ハイラスティン](https://github.com/Rustin170506)に移動する

        -   REDOログ[＃8361](https://github.com/pingcap/tiflow/issues/8361) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)へのDDLイベントの適用をサポート

        -   アップストリーム書き込みスループット[＃7720](https://github.com/pingcap/tiflow/issues/7720) @ [金星の上](https://github.com/overvenus)に基づいて、TiCDC ノードへのテーブルの分割とスケジュールをサポートします。

    -   TiDB Lightning

        -   TiDB Lightning物理インポートモードは、データのインポートとインデックスのインポートを分離して、インポート速度と安定性を向上させます[＃42132](https://github.com/pingcap/tidb/issues/42132) @ [眠そうなモグラ](https://github.com/sleepymole)

            パラメータ`add-index-by-sql`を追加します。デフォルト値は`false`で、これはTiDB Lightningが行データとインデックスデータの両方をKVペアにエンコードし、TiKVに一緒にインポートすることを意味します。 `true`に設定すると、 TiDB Lightningデータをインポートした後、SQL文`ADD INDEX`を介してインデックスを追加し、インポート速度と安定性を向上させます。

        -   `tikv-importer.keyspace-name`パラメータを追加します。デフォルト値は空文字列で、 TiDB Lightning はデータのインポート時に、対応するテナントのキースペース名を自動的に取得します。値を指定した場合、指定されたキースペース名がデータのインポートに使用されます。このパラメータは、マルチテナント TiDB クラスタにデータをインポートする際のTiDB Lightningの設定を柔軟にします[＃41915](https://github.com/pingcap/tidb/issues/41915) @ [リチュンジュ](https://github.com/lichunzhu)

## バグ修正 {#bug-fixes}

-   TiDB

    -   TiDBをv6.5.1からそれ以降のバージョン[＃41502](https://github.com/pingcap/tidb/issues/41502) @ [クリサン](https://github.com/chrysan)にアップグレードする際に更新が失われる問題を修正しました
    -   [＃41423](https://github.com/pingcap/tidb/issues/41423) @ [crazycs520](https://github.com/crazycs520)にアップグレードした後、一部のシステム変数のデフォルト値が変更されない問題を修正しました
    -   インデックスの追加に関連するコプロセッサー要求タイプが不明[＃41400](https://github.com/pingcap/tidb/issues/41400) @ [接線](https://github.com/tangenta)として表示される問題を修正しました
    -   インデックス[＃41515](https://github.com/pingcap/tidb/issues/41515) @ [接線](https://github.com/tangenta)を追加するときに「PessimisticLockNotFound」が返される問題を修正しました
    -   ユニークインデックス[＃41630](https://github.com/pingcap/tidb/issues/41630) @ [接線](https://github.com/tangenta)を追加したときに誤って`found duplicate key`返す問題を修正しました
    -   インデックス[＃41880](https://github.com/pingcap/tidb/issues/41880) @ [接線](https://github.com/tangenta)を追加するときに発生するpanic問題を修正しました
    -   実行中にTiFlash が生成された列に対してエラーを報告する問題を修正[＃40663](https://github.com/pingcap/tidb/issues/40663) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   時間タイプ[＃41938](https://github.com/pingcap/tidb/issues/41938) @ [xuyifangreeneyes](https://github.com/xuyifangreeneyes)がある場合に TiDB が統計を正しく取得できない可能性がある問題を修正しました
    -   準備済みプランキャッシュが有効な場合にフルインデックススキャンでエラーが発生する可能性がある問題を修正[＃42150](https://github.com/pingcap/tidb/issues/42150) @ [fzzf678](https://github.com/fzzf678)
    -   `IFNULL(NOT NULL COLUMN, ...)`誤った結果を返す可能性がある問題を修正[＃41734](https://github.com/pingcap/tidb/issues/41734) @ [リトルフォール](https://github.com/LittleFall)
    -   パーティションテーブル内のすべてのデータが単一のリージョン[＃41801](https://github.com/pingcap/tidb/issues/41801) @ [定義2014](https://github.com/Defined2014)にある場合に TiDB が誤った結果を生成する可能性がある問題を修正しました。
    -   単一のSQL文に異なるパーティションテーブルが出現した場合にTiDBが誤った結果を生成する可能性がある問題を修正[＃42135](https://github.com/pingcap/tidb/issues/42135) @ [ミョンス](https://github.com/mjonss)
    -   パーティションテーブル[＃41638](https://github.com/pingcap/tidb/issues/41638) @ [xuyifangreeneyes](https://github.com/xuyifangreeneyes)に新しいインデックスを追加した後、パーティションパーティションテーブルで統計の自動収集が正しくトリガーされない可能性がある問題を修正しました。
    -   統計を2回連続で収集した後にTiDBが誤った列統計情報を読み取る可能性がある問題を修正[＃42073](https://github.com/pingcap/tidb/issues/42073) @ [xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    -   準備プランキャッシュが有効な場合に IndexMerge が誤った結果を生成する可能性がある問題を修正[＃41828](https://github.com/pingcap/tidb/issues/41828) @ [qw4990](https://github.com/qw4990)
    -   IndexMerge で goroutine リーク[＃41605](https://github.com/pingcap/tidb/issues/41605) @ [グオシャオゲ](https://github.com/guo-shaoge)が発生する可能性がある問題を修正しました
    -   BIGINT 以外の符号なし整数が文字列/小数点[＃41736](https://github.com/pingcap/tidb/issues/41736) @ [リトルフォール](https://github.com/LittleFall)と比較されたときに誤った結果を生成する可能性がある問題を修正しました
    -   メモリ制限超過により前の`ANALYZE`ステートメントを強制終了すると、同じセッション内の現在の`ANALYZE`ステートメントが[＃41825](https://github.com/pingcap/tidb/issues/41825) @ [徐淮嶼](https://github.com/XuHuaiyu)で強制終了される可能性がある問題を修正しました。
    -   バッチコプロセッサ[＃41412](https://github.com/pingcap/tidb/issues/41412) @ [あなた06](https://github.com/you06)の情報収集プロセス中にデータ競合が発生する可能性がある問題を修正しました
    -   アサーションエラーによりパーティションテーブル[＃40629](https://github.com/pingcap/tidb/issues/40629) @ [エキシウム](https://github.com/ekexium) MVCC 情報が印刷されない問題を修正しました
    -   フェアロックモードで存在しないキー[＃41527](https://github.com/pingcap/tidb/issues/41527) @ [エキシウム](https://github.com/ekexium)にロックが追加される問題を修正
    -   `INSERT IGNORE`と`REPLACE`ステートメントが値[＃42121](https://github.com/pingcap/tidb/issues/42121) @ [ジグアン](https://github.com/zyguan)を変更しないキーをロックしない問題を修正しました

-   PD

    -   リージョン散布操作でリーダー[＃6017](https://github.com/tikv/pd/issues/6017) @ [ハンドゥンDM](https://github.com/HunDunDM)の分布が不均一になる可能性がある問題を修正しました。
    -   起動時にPDメンバーを取得する際にデータ競合が発生する可能性がある問題を修正[＃6069](https://github.com/tikv/pd/issues/6069) @ [rleungx](https://github.com/rleungx)
    -   ホットスポット統計[＃6069](https://github.com/tikv/pd/issues/6069) @ [lhy1024](https://github.com/lhy1024)を収集する際にデータ競合が発生する可能性がある問題を修正
    -   配置ルールの切り替えにより、リーダー[＃6195](https://github.com/tikv/pd/issues/6195) @ [バッファフライ](https://github.com/bufferflies)の分布が不均等になる可能性がある問題を修正しました。

-   TiFlash

    -   特定のケースで小数点以下の桁が切り上げられない問題を修正[＃7022](https://github.com/pingcap/tiflash/issues/7022) @ [リトルフォール](https://github.com/LittleFall)
    -   特定のケースで[＃6994](https://github.com/pingcap/tiflash/issues/6994) @ [ウィンドトーカー](https://github.com/windtalker) 10 進キャストが誤って切り上げられる問題を修正しました
    -   新しい照合順序[＃6807](https://github.com/pingcap/tiflash/issues/6807) @ [xzhangxian1008](https://github.com/xzhangxian1008)を有効にした後に TopN/Sort 演算子が誤った結果を生成する問題を修正しました
    -   1200万行を超える結果セットを単一のTiFlashノード[＃6993](https://github.com/pingcap/tiflash/issues/6993) @ [ウィンドトーカー](https://github.com/windtalker)で集計するとTiFlashがエラーを報告する問題を修正しました。

-   ツール

    -   バックアップと復元 (BR)

        -   PITRリカバリプロセス[＃42001](https://github.com/pingcap/tidb/issues/42001) @ [ジョッカウ](https://github.com/joccau)中に分割リージョンの再試行の待機時間が不十分になる問題を修正
        -   PITRリカバリプロセス中に発生した`memory is limited`エラーによるリカバリ失敗の問題を修正[＃41983](https://github.com/pingcap/tidb/issues/41983) @ [ジョッカウ](https://github.com/joccau)
        -   PDノードが[＃14184](https://github.com/tikv/tikv/issues/14184) @ [ユジュンセン](https://github.com/YuJuncen)でダウンしているときにPITRログバックアップの進行が進まない問題を修正しました
        -   リージョンリーダーシップの移行が発生すると、PITR ログバックアップの進行のレイテンシーが長くなるという問題を軽減します[＃13638](https://github.com/tikv/tikv/issues/13638) @ [ユジュンセン](https://github.com/YuJuncen)

    -   TiCDC

        -   変更フィードを再開するとデータが失われる可能性がある、またはチェックポイントが[＃8242](https://github.com/pingcap/tiflow/issues/8242) @ [金星の上](https://github.com/overvenus)に進めない問題を修正しました。
        -   DDLシンク[＃8238](https://github.com/pingcap/tiflow/issues/8238) @ [3エースショーハンド](https://github.com/3AceShowHand)のデータ競合問題を修正
        -   `stopped`ステータスの変更フィードが自動的に再起動する可能性がある問題を修正[＃8330](https://github.com/pingcap/tiflow/issues/8330) @ [スドジ](https://github.com/sdojjy)
        -   すべての下流 Kafka サーバーが利用できない場合に TiCDCサーバーがパニックになる問題を修正[＃8523](https://github.com/pingcap/tiflow/issues/8523) @ [3エースショーハンド](https://github.com/3AceShowHand)
        -   ダウンストリームがMySQLで実行されたステートメントがTiDB [＃8453](https://github.com/pingcap/tiflow/issues/8453) @ [アズドンメン](https://github.com/asddongmen)と互換性がない場合にデータが失われる可能性がある問題を修正しました
        -   ローリングアップグレードによって TiCDC OOM が発生したり、チェックポイントが[＃8329](https://github.com/pingcap/tiflow/issues/8329) @ [金星の上](https://github.com/overvenus)で停止したりする可能性がある問題を修正しました。
        -   Kubernetes [＃8484](https://github.com/pingcap/tiflow/issues/8484) @ [金星の上](https://github.com/overvenus)で TiCDC クラスターの正常なアップグレードが失敗する問題を修正しました

    -   TiDB データ移行 (DM)

        -   DM ワーカーノードが Google Cloud Storage を使用する場合、ブレークポイントが頻繁すぎると、Google Cloud Storage のリクエスト頻度の制限に達し、DM ワーカーが Google Cloud Storage にデータを書き込むことができず、完全なデータの読み込みに失敗する問題を修正しました[＃8482](https://github.com/pingcap/tiflow/issues/8482) @ [マックスシュアン](https://github.com/maxshuang)
        -   複数の DM タスクが同じダウンストリーム データを同時に複製し、すべてがダウンストリーム メタデータ テーブルを使用してブレークポイント情報を記録すると、すべてのタスクのブレークポイント情報が同じメタデータ テーブルに書き込まれ、同じタスク ID [＃8500](https://github.com/pingcap/tiflow/issues/8500) @ [マックスシュアン](https://github.com/maxshuang)が使用される問題を修正しました。

    -   TiDB Lightning

        -   物理インポートモードを使用してデータをインポートする場合、ターゲットテーブルの複合主キーに`auto_random`列目があるが、その列の値がソースデータに指定されていない場合、 TiDB Lightningは`auto_random`列目のデータを自動的に生成しないという問題を修正しました[＃41454](https://github.com/pingcap/tidb/issues/41454) @ [D3ハンター](https://github.com/D3Hunter)
        -   論理インポートモードを使用してデータをインポートすると、ターゲットクラスタ[＃41915](https://github.com/pingcap/tidb/issues/41915) @ [リチュンジュ](https://github.com/lichunzhu)の`CONFIG`権限が不足しているためにインポートが失敗する問題を修正しました。

## 寄稿者 {#contributors}

TiDB コミュニティからの以下の貢献者に感謝いたします。

-   [アンチトップクォーク](https://github.com/AntiTopQuark)
-   [ブラックティア23](https://github.com/blacktear23)
-   [生まれ変わった人](https://github.com/BornChanger)
-   [ドゥーシル9](https://github.com/Dousir9)
-   [エルワドバ](https://github.com/erwadba)
-   [ハッピーv587](https://github.com/happy-v587)
-   [ジフハウス](https://github.com/jiyfhust)
-   [L-メープル](https://github.com/L-maple)
-   [liumengya94](https://github.com/liumengya94)
-   [ウーフィジャオ](https://github.com/woofyzhao)
-   [夏関](https://github.com/xiaguan)
