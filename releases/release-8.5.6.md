---
title: TiDB 8.5.6 Release Notes
summary: TiDB 8.5.6 の機能、互換性の変更点、改善点、およびバグ修正について学びましょう。
---

# TiDB 8.5.6 リリースノート {#tidb-8-5-6-release-notes}

発売日：2026年4月14日

TiDBバージョン：8.5.6

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb)| [本番環境への展開](https://docs.pingcap.com/tidb/v8.5/production-deployment-using-tiup)

## 特徴 {#features}

### パフォーマンス {#performance}

-   外部キー チェックで共有ロックがサポートされるようになりました [#66154](https://github.com/pingcap/tidb/issues/66154) @[you06](https://github.com/you06)

    悲観的トランザクションでは、外部キー制約を持つ子テーブルで`INSERT`または`UPDATE`を実行すると、外部キーチェックによって、デフォルトで対応する親テーブルの行が排他ロックでロックされます。子テーブルへの書き込みが高頻度で行われるシナリオでは、多数のトランザクションが同じ親テーブルの行にアクセスすると、深刻なロック競合が発生する可能性があります。

    バージョン8.5.6以降では、 [`tidb_foreign_key_check_in_shared_lock`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_foreign_key_check_in_shared_lock-new-in-v856)システム変数を`ON`に設定することで、外部キーチェックで親テーブルの共有ロックを使用するように設定でき、ロック競合を減らし、子テーブルの同時書き込みパフォーマンスを向上させることができます。

    詳細については、 [ドキュメント](https://docs.pingcap.com/tidb/v8.5/foreign-key#locking)を参照してください。

### 安定性 {#stability}

-   リソース制御のバックグラウンドタスクにおけるリソース使用量の上限を設定する機能が一般提供開始（GA）になりました [#56019](https://github.com/pingcap/tidb/issues/56019) @[glorv](https://github.com/glorv)

    TiDBのリソース制御機能を使用すると、バックグラウンドタスクを識別して優先度を下げることができます。特定のシナリオでは、リソースが利用可能な場合でも、バックグラウンドタスクのリソース消費を制限したい場合があります。v8.4.0以降では、 `UTILIZATION_LIMIT`パラメータを使用して、バックグラウンドタスクが消費できるリソースの最大割合を設定できます。各ノードは、すべてのバックグラウンドタスクのリソース使用量をこの割合以下に抑えます。この機能により、バックグラウンドタスクのリソース消費を正確に制御できるため、クラスタの安定性がさらに向上します。

    バージョン8.5.6では、この機能は一般提供（GA）されています。

    詳細については、 [ドキュメント](https://docs.pingcap.com/tidb/v8.5/tidb-resource-control-background-tasks)を参照してください。

### 可観測性 {#observability}

-   低速クエリログに対する多次元で詳細なトリガールールの定義をサポートする[#62959](https://github.com/pingcap/tidb/issues/62959) 、 [#64010](https://github.com/pingcap/tidb/issues/64010) @[zimulala](https://github.com/zimulala)

    バージョン 8.5.6 より前では、TiDB でスロークエリを識別する主な方法は、 [`tidb_slow_log_threshold`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_slow_log_threshold)システム変数を設定することでした。このメカニズムはインスタンスレベルでグローバルに適用されるため、スロークエリログのトリガーを大まかにしか制御できず、セッションレベルや SQL レベルでのきめ細かい制御はサポートされていません。さらに、トリガー条件として実行時間 ( `Query_time` ) しかサポートしていないため、複雑なシナリオでスロークエリログをより正確にキャプチャするニーズを満たすことができません。

    バージョン 8.5.6 以降、TiDB [`tidb_slow_log_rules`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_slow_log_rules-new-in-v856)スロークエリログの制御を強化しました。tidb_slow_log_rules システム変数を使用して、 `Query_time` 、 `Digest`などの条件に基づいて、 `Mem_max` `KV_total`および SQL レベルで多次元のスロークエリログ出力ルールを定義できます。tidb_slow_log_max_per_sec [`tidb_slow_log_max_per_sec`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_slow_log_max_per_sec-new-in-v856)使用して、1 秒あたりに書き込まれるログエントリの数を制限したり、 [`WRITE_SLOW_LOG`](https://docs.pingcap.com/tidb/v8.5/optimizer-hints)ヒントを使用して、特定の SQL ステートメントに対してスロークエリログを強制的に記録したりできます。これにより、スロークエリログをより柔軟かつきめ細かく制御できます。

    詳細については、 [ドキュメント](https://docs.pingcap.com/tidb/v8.5/identify-slow-queries)を参照してください。

-   TiDBダッシュボードのTop SQLページで、TiKVネットワークトラフィックと論理I/Oメトリックの収集と表示がサポートされるようになりました [#62916](https://github.com/pingcap/tidb/issues/62916) @[yibin87](https://github.com/yibin87)

    以前のバージョンでは、TiDB DashboardはCPU関連のメトリックのみに基づいてTop SQLクエリを特定していたため、複雑なシナリオにおいてネットワークやstorageへのアクセスに関連するパフォーマンスのボトルネックを特定することが困難でした。

    バージョン8.5.6以降では、Top SQL設定で**TiKVネットワークIO収集（多次元）**を有効にして、TiKVノードの`Network Bytes`や`Logical IO Bytes`などのメトリックを表示できます。また、 `By Query` 、 `By Table` 、 `By DB` `By Region` 、複数の次元にわたってこれらのメトリックを分析することで、リソースのホットスポットをより包括的に特定できます。

    詳細については、 [ドキュメント](https://docs.pingcap.com/tidb/v8.5/top-sql)を参照してください。

### SQL {#sql}

-   列レベルの権限管理をサポート [#61706](https://github.com/pingcap/tidb/issues/61706) @[CbcWestwolf](https://github.com/CbcWestwolf) @[fzzf678](https://github.com/fzzf678)

    バージョン8.5.6より前のTiDBでは、権限制御はデータベースレベルとテーブルレベルの両方を対象としており、MySQLとは異なり、特定の列に対する権限の付与や取り消しはサポートされていませんでした。そのため、ユーザーがテーブル内の機密性の高い列の一部のみにアクセスできるように制限することはできませんでした。

    バージョン8.5.6以降、TiDBは列レベルの権限管理をサポートしています。 `GRANT`および`REVOKE`ステートメントを使用して、特定の列の権限を管理できます。TiDBは、クエリ処理および実行プラン構築時に列レベルの権限に基づいて権限チェックを実行するため、よりきめ細かなアクセス制御が可能になり、機密データの分離と最小権限の原則をより適切にサポートします。

    詳細については、 [ドキュメント](https://docs.pingcap.com/tidb/v8.5/column-privilege-management)を参照してください。

-   `FOR UPDATE OF`句でのテーブル エイリアスの使用をサポート [#63035](https://github.com/pingcap/tidb/issues/63035) @[cryo-zd](https://github.com/cryo-zd)

    v8.5.6 より前のバージョンでは、 `SELECT ... FOR UPDATE OF <table>`ステートメントがロック句でテーブルエイリアスを参照する場合、エイリアスが有効であっても、TiDB がエイリアスを正しく解決できず、 `table not exists`エラーを返すことがありました。

    バージョン8.5.6以降、TiDBは`FOR UPDATE OF`句でのテーブルエイリアスの使用をサポートするようになりました。TiDBは`FROM`句からのロック対象（エイリアス付きテーブルを含む）を正しく解決できるようになり、行ロックが期待どおりに有効になります。これにより、MySQLとの互換性が向上し、テーブルエイリアスを使用するクエリにおける`SELECT ... FOR UPDATE OF`ステートメントの安定性と信頼性が向上します。

    詳細については、 [ドキュメント](https://docs.pingcap.com/tidb/v8.5/sql-statement-select)を参照してください。

### データベース操作 {#db-operations}

-   Distributed eXecution Framework (DXF) タスクの最大ノード数の指定をサポート [#58944](https://github.com/pingcap/tidb/issues/58944) @[tangenta](https://github.com/tangenta)@[D3Hunter](https://github.com/D3Hunter)

    バージョン8.5.6より前のTiDBでは、分散実行タスクで使用されるノード数を制限する機能がありません。DXFのリソース使用量を制御したい場合、TiDBには最大ノード数を制限するための専用オプションが用意されていません。

    バージョン8.5.6以降、TiDBはDXFタスクで使用されるTiDBノードの最大数を指定するためのシステム変数`tidb_max_dist_task_nodes`を導入し、より優れたリソース制御とワークロードベースのチューニングを可能にしました。

    詳細については、 [ドキュメント](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_max_dist_task_nodes-new-in-v856)を参照してください。

### データ移行 {#data-migration}

-   `pingcap/tidb-tools`リポジトリから`pingcap/tiflow`リポジトリへ sync-diff-inspector を移行する [#11672](https://github.com/pingcap/tiflow/issues/11672) @[joechenrh](https://github.com/joechenrh)

## 互換性の変更 {#compatibility-changes}

TiDBクラスタをv8.5.5で新規にデプロイした場合（つまり、v8.5.4より前のバージョンからアップグレードしていない場合）、v8.5.6へスムーズにアップグレードできます。v8.5.6の変更点のほとんどは通常のアップグレードでは問題ありませんが、このリリースにはMySQLとの互換性に関する変更、システム変数の更新、構成パラメータの更新、および非推奨機能も含まれています。アップグレードする前に、このセクションをよくお読みください。

### MySQLとの互換性 {#mysql-compatibility}

-   バージョン8.5.6以降、TiDBはMySQL互換の列レベルの権限管理メカニズムをサポートしています。テーブルレベルで特定の列に対して、 `SELECT` 、 `INSERT` 、 `UPDATE` 、および`REFERENCES`の権限または取り消すことができます。詳細については、 [列レベルの権限管理](https://docs.pingcap.com/tidb/v8.5/column-privilege-management)参照してください。
-   バージョン 8.5.6 以降、TiDB は`FOR UPDATE OF`句でテーブル エイリアスの使用をサポートしています。下位互換性を維持するために、エイリアスが定義されている場合でもベース テーブル名を参照できますが、明示的なエイリアスの使用を推奨する警告が表示されます。詳細については、 [`SELECT`](https://docs.pingcap.com/tidb/v8.5/sql-statement-select)参照してください。
-   バージョン8.5.6以降、 Dumplingは更新されたMySQLバイナリログの用語を採用することで、MySQL 8.4からのデータエクスポートをサポートしています。 [#53082](https://github.com/pingcap/tidb/issues/53082) @[dveeden](https://github.com/dveeden)
-   バージョン8.5.6以降、TiDB Data Migration (DM) は、このバージョンで導入された新しい用語とバージョン検出ロジックに対応することで、アップストリームデータソースとしてMySQL 8.4をサポートします。 [#11020](https://github.com/pingcap/tiflow/issues/11020) @[dveeden](https://github.com/dveeden)

### システム変数 {#system-variables}

| 変数名                                                                                                                                                  | 種類を変更する  | 説明                                                                                                                                                                                                                                |
| ---------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_analyze_version`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_analyze_version-new-in-v510)                                       | 修正済み     | バージョン8.5.6以降、統計情報バージョン1（ `tidb_analyze_version = 1` ）は非推奨となり、今後のリリースで削除されます。統計情報バージョン2（ `tidb_analyze_version = 2` ）の使用をお勧めします。                                                                                                   |
| [`tidb_ignore_inlist_plan_digest`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_ignore_inlist_plan_digest-new-in-v760)                   | 修正済み     | デフォルト値を`OFF`から`ON`に変更します。デフォルト値`ON`は、TiDB が`IN` } リスト内の要素の差異 (要素数の差異を含む) を無視し、プランダイジェストを生成する際に`...`を使用して`IN`リスト内の要素を置き換えることを意味します。                                                                                                |
| [`tidb_service_scope`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_service_scope-new-in-v740)                                           | 修正済み     | バージョン8.5.6以降、この変数の値は大文字と小文字を区別しません。TiDBは、storageおよび比較のために、入力値を小文字に変換します。                                                                                                                                                          |
| [`InPacketBytes`](https://docs.pingcap.com/tidb/v8.5/system-variables#inpacketbytes-new-in-v856)                                                     | 新しく追加された | この変数は内部統計のみに使用され、ユーザーには表示されません。                                                                                                                                                                                                   |
| [`OutPacketBytes`](https://docs.pingcap.com/tidb/v8.5/system-variables#outpacketbytes-new-in-v856)                                                   | 新しく追加された | この変数は内部統計のみに使用され、ユーザーには表示されません。                                                                                                                                                                                                   |
| [`tidb_foreign_key_check_in_shared_lock`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_foreign_key_check_in_shared_lock-new-in-v856)     | 新しく追加された | 悲観的トランザクションにおける外部キーチェックで、親テーブルの行に対して排他ロックではなく共有ロックを使用するかどうかを制御します。デフォルト値は`OFF`で、これは TiDB がデフォルトで排他ロックを使用することを意味します。                                                                                                               |
| [`tidb_max_dist_task_nodes`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_max_dist_task_nodes-new-in-v856)                               | 新しく追加された | 分散実行フレームワーク (DXF) タスクが使用できる TiDB ノードの最大数を定義します。デフォルト値は`-1`で、これは自動モードが有効になっていることを示します。自動モードでは、TiDB は`min(3, tikv_nodes / 3)`という値を動的に計算します。ここで、 `tikv_nodes`クラスタ内の TiKV ノードの数を表します。                                                 |
| [`tidb_opt_join_reorder_through_sel`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_opt_join_reorder_through_sel-new-in-v856)             | 新しく追加された | 特定の複数テーブル結合クエリの結合順序最適化を改善します。これを`ON`に設定し、安全条件が満たされている場合、オプティマイザは、連続する結合演算子間の`Selection`条件と結合順序候補を評価します。結合ツリーの再構築中、オプティマイザは可能な限りこれらの条件をより適切な位置に押し下げ、より多くのテーブルが結合順序最適化に参加できるようにします。                                                 |
| [`tidb_opt_partial_ordered_index_for_topn`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_opt_partial_ordered_index_for_topn-new-in-v856) | 新しく追加された | クエリに`ORDER BY ... LIMIT`が含まれている場合に、オプティマイザがインデックスの部分順序を利用して TopN 計算を最適化できるかどうかを制御します。デフォルト値は`DISABLE`で、これは最適化が無効になっていることを意味します。                                                                                                   |
| [`tidb_slow_log_max_per_sec`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_slow_log_max_per_sec-new-in-v856)                             | 新しく追加された | TiDBノードごとに1秒あたりに書き込める、低速クエリログエントリの最大数を制御します。<ul><li> `0` （デフォルト値）という値は、1秒あたりに書き込まれるスロークエリログエントリの数に制限がないことを意味します。</li><li> `0`より大きい値を指定すると、TiDBは1秒あたりに指定された数のスロークエリログエントリを書き込みます。超過分のログエントリは破棄され、スロークエリログファイルには書き込まれません。</li></ul> |
| [`tidb_slow_log_rules`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_slow_log_rules-new-in-v856)                                         | 新しく追加された | スロークエリログのトリガールールを定義します。多次元メトリクスを組み合わせることで、より柔軟で詳細なログ記録を実現します。                                                                                                                                                                     |

### コンフィグレーションパラメータ {#configuration-parameters}

| コンフィグレーションファイルまたはコンポーネント | コンフィグレーションパラメータ                                                                                                                                         | 種類を変更する  | 説明                                                                               |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------- |
| ティクヴ                     | [`gc.auto-compaction.mvcc-read-aware-enabled`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#mvcc-read-aware-enabled-new-in-v856)          | 新しく追加された | MVCC読み取り対応の圧縮を有効にするかどうかを制御します。デフォルト値は`false`です。                                  |
| ティクヴ                     | [`gc.auto-compaction.mvcc-read-weight`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#mvcc-read-weight-new-in-v856)                        | 新しく追加された | リージョンの圧縮優先度スコアを計算する際に、MVCC 読み取りアクティビティに適用される重み乗数。デフォルト値は`3.0`です。                 |
| ティクヴ                     | [`gc.auto-compaction.mvcc-scan-threshold`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#mvcc-scan-threshold-new-in-v856)                  | 新しく追加された | リージョンを圧縮候補としてマークするために、読み取り要求ごとにスキャンされる MVCC バージョンの最小数。デフォルト値は`1000`です。           |
| ティクヴ                     | [`resource-metering.enable-network-io-collection`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#enable-network-io-collection-new-in-v856) | 新しく追加された | TiKV ネットワーク トラフィックと論理 I/O メトリックをTop SQLに追加で収集するかどうかを制御します。デフォルト値は`false`です。      |
| TiCDC                    | [`sink.csv.output-field-header`](https://docs.pingcap.com/tidb/v8.5/ticdc-csv#use-csv)                                                                  | 新しく追加された | CSVファイルにヘッダー行を出力するかどうかを制御します。デフォルト値は`false`です。このパラメータはTiCDCの新しいアーキテクチャにのみ適用されます。 |

## 非推奨機能 {#deprecated-features}

-   v8.5.6 以降、統計バージョン 1 ( `tidb_analyze_version = 1` ) は非推奨となり、将来のリリースでは削除される予定です。より正確な統計を得るには、統計バージョン 2 ( `tidb_analyze_version = 2` ) および[統計情報を使用する既存のオブジェクトをバージョン1からバージョン2に移行する](https://docs.pingcap.com/tidb/v8.5/statistics#switch-between-statistics-versions)お勧めします。
-   バージョン8.5.6以降、 TiDB Lightning Webインターフェースは非推奨となり、バージョン8.5.7で削除されます。Web UIビルドはバージョン8.4.0以降、不具合が発生しています。代わりに[CLI](/tidb-lightning/tidb-lightning-overview.md)または[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)ステートメントを使用してください。この変更がワークフローに影響する場合は、 [#67697](https://github.com/pingcap/tidb/issues/67697)にコメントしてください。

## 改善点 {#improvements}

-   TiDB

    -   インデックスプレフィックス列に対する`IN`述語を含むクエリのプラン選択を改善します。TiDB は`ORDER BY ... LIMIT`クエリの順序を保持するためにマージソートを使用できるようになり、不要なスキャンを削減してパフォーマンスを向上させます。 [#63449](https://github.com/pingcap/tidb/issues/63449) [#34882](https://github.com/pingcap/tidb/issues/34882) @[time-and-fate](https://github.com/time-and-fate)
    -   印刷不可能なプリペアドステートメント引数を16進数として出力することで、スロークエリログの可読性を向上させる [#65383](https://github.com/pingcap/tidb/issues/65383) @[dveeden](https://github.com/dveeden)
    -   `cluster_id`を`mysql.tidb`に追加し、外部ツールが 2 つの TiDB インスタンスが同じクラスターに属しているかどうかを判断できるようにします [#59476](https://github.com/pingcap/tidb/issues/59476) @[YangKeao](https://github.com/YangKeao)

-   ティクヴ

    -   MVCCの読み取りオーバーヘッドを検出し、読み取りコストの高いリージョンの圧縮を優先することでクエリパフォーマンスを向上させる、負荷ベースの圧縮メカニズムを導入します [#19133](https://github.com/tikv/tikv/issues/19133) @[mittalrishabh](https://github.com/mittalrishabh)
    -   クラスタのスケールアウトおよびスケールイン操作中に、古いキーをSSTファイル取り込みでクリーンアップするのではなく直接削除することで、古いキーの範囲のクリーンアップロジックを最適化し、オンラインリクエストのレイテンシーへの影響を軽減します。 [#18042](https://github.com/tikv/tikv/issues/18042) @[LykxSassinator](https://github.com/LykxSassinator)
    -   Top SQLの TiKV ネットワークトラフィックと論理 I/O メトリックの収集をサポートし、SQL パフォーマンスの問題をより正確に診断できるようにします [#18815](https://github.com/tikv/tikv/issues/18815) @[yibin87](https://github.com/yibin87)

-   PD

    -   存在しないラベルを削除する際に、 `404` `200` } を返す [#10089](https://github.com/tikv/pd/issues/10089) @[lhy1024](https://github.com/lhy1024)
    -   不要なエラーログを削減 [#9370](https://github.com/tikv/pd/issues/9370) @[bufferflies](https://github.com/bufferflies)

-   ツール

    -   TiDBデータ移行（DM）

        -   DMシンカーに外部キーの因果関係サポートを追加し、マルチワーカーシナリオにおける行変更の親から子への実行順序を保証する [#12350](https://github.com/pingcap/tiflow/issues/12350) @[OliverS929](https://github.com/OliverS929)

## バグ修正 {#bug-fixes}

-   TiDB

    -   `release-8.5-20250606-v8.5.2`からアップストリームの`release-8.5`にアップグレードすると、PITR メタデータのアップグレードがスキップされ、PITR 操作が失敗する可能性がある問題を修正します [#66994](https://github.com/pingcap/tidb/issues/66994) @[fzzf678](https://github.com/fzzf678)
    -   `EXCHANGE PARTITION`を実行した後、非クラスター化パーティションテーブルの非一意グローバルインデックスまたは null 許容一意グローバルインデックスが不整合になり、不完全な結果を返す可能性がある問題を修正しました [#65289](https://github.com/pingcap/tidb/issues/65289) @[mjonss](https://github.com/mjonss)
    -   `KILL QUERY`がアイドル状態の接続を誤って終了する可能性がある問題を修正 [#65447](https://github.com/pingcap/tidb/issues/65447) @[gengliqi](https://github.com/gengliqi)
    -   `tidb_service_scope`の値が小文字に変換されない問題を修正 [#66749](https://github.com/pingcap/tidb/issues/66749) @[D3Hunter](https://github.com/D3Hunter)
    -   TiDBの再起動後にアフィニティテーブルが表示されない問題を修正 [#66284](https://github.com/pingcap/tidb/issues/66284) [lcwangchao](https://github.com/lcwangchao)
    -   システムテーブルが統計キャッシュから除外されていないため、Stats Healthyメトリックが不正確に表示される問題を修正しました [#64080](https://github.com/pingcap/tidb/issues/64080) @[0xPoe](https://github.com/0xPoe)
    -   `modify_count`の異常な更新により統計情報が更新されない可能性がある問題を修正しました [#65426](https://github.com/pingcap/tidb/issues/65426) @[0xPoe](https://github.com/0xPoe)
    -   フェアロックモードで最初のステートメントがロックを取得する際に、キープアライブメカニズムの失敗により悲観的トランザクションが予期せずロールバックされる可能性がある問題を修正 [#66571](https://github.com/pingcap/tidb/issues/66571) @[MyonKeminta](https://github.com/MyonKeminta)

-   ティクヴ

    -   クロスビームスキップリストのメモリリーク問題を修正 [#19285](https://github.com/tikv/tikv/issues/19285) @[ekexium](https://github.com/ekexium)
    -   パーティションテーブルの一意でない列のグローバルインデックスが、場合によっては不整合になり、誤った結果を返す可能性がある問題を修正しました [#19262](https://github.com/tikv/tikv/issues/19262) @[mjonss](https://github.com/mjonss)
    -   コプロセッサのスナップショット取得が停止すると、リクエストの期限が切れるまで統合リードプールワーカーが占有され、他のリードリクエストが遅延する問題を修正しました [#18491](https://github.com/tikv/tikv/issues/18491) @[AndreMouche](https://github.com/AndreMouche)
    -   ディスクがいっぱいの TiKV ノードでフォロワーの読み取りがブロックされたままになる可能性がある問題を修正するため、ディスクがいっぱいのフォロワーで読み取りインデックス要求を拒否します [#19201](https://github.com/tikv/tikv/issues/19201) @[glorv](https://github.com/glorv)
    -   resolved-tsワーカーがビジー状態のときに、 resolved-tsタスクのバックログによって OOM が発生する可能性がある問題を修正 [#18359](https://github.com/tikv/tikv/issues/18359) @[overvenus](https://github.com/overvenus)
    -   リーダー転送中にロングテールフォロワーの読み取りレイテンシーが発生する可能性がある問題を修正するため、読み取りインデックス要求をより早く再試行し、専用の再試行間隔設定を追加しました [#18417](https://github.com/tikv/tikv/issues/18417) @[gengliqi](https://github.com/gengliqi)
    -   悲観的トランザクションでプリライト要求を再試行する際に発生するまれなデータ不整合の問題を修正 [#11187](https://github.com/tikv/tikv/issues/11187) @[wk989898](https://github.com/wk989898)

-   PD

    -   マージリージョン演算子が多数存在するシナリオで`DISTRIBUTE TABLE`を実行する際に発生する可能性のあるpanic問題を修正 [#10293](https://github.com/tikv/pd/issues/10293) @[bufferflies](https://github.com/bufferflies)
    -   ストア制限の設定がすぐに反映されない場合がある問題を修正しました [#10108](https://github.com/tikv/pd/issues/10108) [okJiang](https://github.com/okJiang)

-   TiFlash

    -   DDL ステートメントを実行して列 [#10680](https://github.com/pingcap/tiflash/issues/10680) @[JaySon-Huang](https://github.com/JaySon-Huang)の`NOT NULL`制約を削除した後、 TiFlashと TiKV の間で潜在的なデータの不整合の問題を修正しました。
    -   Grafana ダッシュボードのRaftスループット メトリックに異常に大きな値が表示される問題を修正 [#10701](https://github.com/pingcap/tiflash/issues/10701) @[CalvinNeo](https://github.com/CalvinNeo)
    -   ランタイムフィルターが有効で結合キーのデータ型が一致しない場合に結合結果が正しくなくなることがある問題を修正 [#10699](https://github.com/pingcap/tiflash/issues/10699) @[ChangRui-Ryan](https://github.com/ChangRui-Ryan)

-   ツール

    -   バックアップと復元 (BR)

        -   ログバックアップで`flush_ts`が`0`になる可能性がある問題を修正 [#19406](https://github.com/tikv/tikv/issues/19406) @[YuJuncen](https://github.com/YuJuncen)
        -   Amazon S3互換APIを介してS3スタイルの認証情報を使用してGoogle Cloud Storageにアクセスする際、Content-Lengthヘッダーが欠落しているため、マルチパートアップロード中にBRが失敗する可能性がある問題を修正しました。 [#19352](https://github.com/tikv/tikv/issues/19352) @[Leavrth](https://github.com/Leavrth)
        -   BR `restore point` `waiting for schema info finishes reloading`の状態に長時間留まり、15 分後にタイムアウトで失敗する問題を修正しました [#66110](https://github.com/pingcap/tidb/issues/66110) @[kennytm](https://github.com/kennytm)
        -   `SHARD_ROW_ID_BITS` 、 `PRE_SPLIT_REGIONS`BRを持つテーブルを復元する際に、 `merge_option`問題を修正します。 [#65060](https://github.com/pingcap/tidb/issues/65060) @[JoyC-dev](https://github.com/JoyC-dev)

    -   TiCDC

        -   サーバーの再起動後にchangefeedsが繰り返し無効なディスパッチャーを作成する可能性がある問題を修正 [#4452](https://github.com/pingcap/ticdc/issues/4452) @[wlwilliamx](https://github.com/wlwilliamx)
        -   TiCDCが、上流のTiDBバージョンがv8.1.x以前の場合にテーブル名変更操作を正しく複製できない問題を修正します [#4392](https://github.com/pingcap/ticdc/issues/4392) @[lidezhu](https://github.com/lidezhu)
        -   TiCDCが有効になっている場合に、データスキャン中にTiKVがクラッシュする可能性がある問題を修正しました [#19404](https://github.com/tikv/tikv/issues/19404) @[wk989898](https://github.com/wk989898)
        -   Azure Blob Storage の Azure Managed Identity 認証をサポートし、クラウドstorageへのアップロードが停止する可能性がある問題を修正します [#3093](https://github.com/pingcap/ticdc/issues/3093) @[wlwilliamx](https://github.com/wlwilliamx)

    -   TiDBデータ移行（DM）

        -   アップストリームのbinlogファイルのローテーション後にDMがグローバルチェックポイントの位置を進めない問題を修正 [#12339](https://github.com/pingcap/tiflow/issues/12339) @[OliverS929](https://github.com/OliverS929)
        -   セーフモードで外部キー制約のあるテーブルの更新を処理する際に、主キーまたは一意キーが変更されていない場合でも、DM が誤って外部キーのカスケードをトリガーし、意図しないデータ削除を引き起こす可能性がある問題を修正します。 [#12350](https://github.com/pingcap/tiflow/issues/12350) @[OliverS929](https://github.com/OliverS929)
        -   DMバリデーターが`UNSIGNED`列を処理する際に誤って検証エラーを返す問題を修正しました [#12178](https://github.com/pingcap/tiflow/issues/12178) @[OliverS929](https://github.com/OliverS929)
