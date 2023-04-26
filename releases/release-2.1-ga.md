---
title: TiDB 2.1 GA Release Notes
---

# TiDB 2.1 GA リリースノート {#tidb-2-1-ga-release-notes}

2018 年 11 月 30 日に、TiDB 2.1 GA がリリースされました。このリリースの次の更新を参照してください。 TiDB 2.0 と比較すると、このリリースでは、安定性、パフォーマンス、互換性、および使いやすさが大幅に向上しています。

## TiDB {#tidb}

-   SQL オプティマイザー

    -   `Index Join`の選択範囲を最適化して実行性能を向上

    -   外部表の選択を`Index Join`に最適化し、Row Count の推定値が小さい方の表を外部表として使用する

    -   Join Hint `TIDB_SMJ`最適化して、適切なインデックスがなくても Merge Join を使用できるようにする

    -   結合する内部テーブルを指定する最適化結合ヒント`TIDB_INLJ`

    -   相関サブクエリを最適化し、フィルターを押し下げ、インデックス選択範囲を拡張して、一部のクエリの効率を桁違いに改善します

    -   `UPDATE`ステートメントと`DELETE`ステートメントでの Index Hint と Join Hint の使用のサポート

    -   より多くの関数を押し下げるサポート： `ABS` / `CEIL` / `FLOOR` / `IS TRUE` / `IS FALSE`

    -   組み込み関数`IF`および`IFNULL`定数畳み込みアルゴリズムを最適化する

    -   `EXPLAIN`ステートメントの出力を最適化し、階層構造を使用して演算子間の関係を示す

-   SQL エグゼキュータ

    -   すべての集計関数をリファクタリングし、 `Stream`と`Hash`の集計演算子の実行効率を改善します

    -   並列`Hash Aggregate`演算子を実装し、いくつかのシナリオで計算パフォーマンスを 350% 向上させます

    -   並列`Project`演算子を実装すると、一部のシナリオでパフォーマンスが 74% 向上します

    -   `Hash Join`の内表と外表のデータを同時に読み込んで実行性能を向上させる

    -   `REPLACE INTO`ステートメントの実行速度を最適化し、パフォーマンスを10倍近く向上させます

    -   時間データ型のメモリ使用量を最適化し、時間データ型のメモリ使用量を 50% 削減します。

    -   ポイント選択のパフォーマンスを最適化し、Sysbench のポイント選択効率の結果を 60% 向上させます

    -   幅の広いテーブルを挿入または更新する際の TiDB のパフォーマンスを 20 倍改善

    -   構成ファイル内の単一ステートメントのメモリ上限の構成をサポート

    -   ハッシュ結合の実行を最適化します。結合タイプが内部結合または半結合で、内部テーブルが空の場合、外部テーブルからデータを読み取らずに結果を返します

    -   [`EXPLAIN ANALYZE`ステートメント](/sql-statements/sql-statement-explain-analyze.md)を使用して実行時間と各演算子の返された行数を含むランタイム統計をチェックするサポート

-   統計

    -   1 日の特定の期間のみ自動 ANALYZE 統計を有効にするサポート

    -   クエリのフィードバックに従ってテーブル統計を自動的に更新するサポート

    -   `ANALYZE TABLE WITH BUCKETS`ステートメントを使用したヒストグラム内のバケット数の構成をサポート

    -   等値クエリと範囲クエリの混合クエリのヒストグラムを使用して行数推定アルゴリズムを最適化する

-   式

    -   次の組み込み関数をサポートします。

        -   `json_contains`

        -   `json_contains_path`

        -   `encode/decode`

-   サーバ

    -   競合するトランザクションのパフォーマンスを最適化するために、tidb-server インスタンス内でローカルに競合するトランザクションのキューイングをサポート

    -   サーバー側カーソルのサポート

    <!---->

    -   [HTTP API](https://github.com/pingcap/tidb/blob/master/docs/tidb_http_api.md)を追加

        -   TiKV クラスター内のテーブル リージョンの分布を分散させる

        -   `general log`を開くかどうかを制御します

        -   ログレベルのオンライン変更をサポート

        -   TiDB クラスター情報を確認する

    <!---->

    -   [`auto_analyze_ratio`システム変数を追加して、分析の比率を制御します](/faq/sql-faq.md#whats-the-trigger-strategy-for-auto-analyze-in-tidb)

    -   [`tidb_retry_limit`システム変数を追加して、トランザクションの自動再試行回数を制御します](/system-variables.md#tidb_retry_limit)

    -   [`tidb_disable_txn_auto_retry`システム変数を追加して、トランザクションを自動的に再試行するかどうかを制御します](/system-variables.md#tidb_disable_txn_auto_retry)

    -   [`admin show slow`ステートメントを使用したスロー クエリの取得のサポート](/identify-slow-queries.md#admin-show-slow-command)

    -   [`tidb_slow_log_threshold`環境変数を追加して、スローログのしきい値を自動的に設定します](/system-variables.md#tidb_slow_log_threshold)

    -   [`tidb_query_log_max_len`環境変数を追加して、ログで動的に切り捨てられる SQL ステートメントの長さを設定します](/system-variables.md#tidb_query_log_max_len)

-   DDL

    -   Add index ステートメントと他のステートメントの並列実行をサポートして、時間のかかる Add index 操作が他の操作をブロックするのを回避します。

    -   `ADD INDEX`の実行速度を最適化し、一部のシナリオで大幅に改善

    -   TiDB が`DDL Owner`かどうかの判断を容易にする`select tidb_is_ddl_owner()`ステートメントをサポートする

    -   `ALTER TABLE FORCE`構文をサポート

    -   `ALTER TABLE RENAME KEY TO`構文をサポート

    -   `admin show ddl jobs`の出力情報にテーブル名とデータベース名を追記

    -   [`ddl/owner/resign` HTTP インターフェースを使用して DDL 所有者を解放し、新しい DDL 所有者の選択を開始するサポート](https://github.com/pingcap/tidb/blob/master/docs/tidb_http_api.md)

-   互換性

    -   より多くの MySQL 構文をサポート

    -   `BIT`集計関数が`ALL`パラメータをサポートするようにする

    -   `SHOW PRIVILEGES`ステートメントをサポート

    -   `LOAD DATA`ステートメントで`CHARACTER SET`構文をサポートする

    -   `CREATE USER`ステートメントで`IDENTIFIED WITH`構文をサポートする

    -   `LOAD DATA IGNORE LINES`ステートメントをサポート

    -   `Show ProcessList`ステートメントはより正確な情報を返します

## プレースメントDriver(PD) {#placement-driver-pd}

-   可用性を最適化する

    -   バージョン管理メカニズムを導入し、互換性のあるクラスターのローリング アップデートをサポートします。

    -   ネットワーク分離後にネットワークが回復したときにリーダーの再選択を避けるため、PD ノード間で[`Raft PreVote`を有効にする](https://github.com/pingcap/pd/blob/5c7b18cf3af91098f07cf46df0b59fbf8c7c5462/conf/config.toml#L22)

    -   デフォルトで`raft learner`を有効にして、スケジューリング中のマシン障害によってデータが使用できなくなるリスクを軽減します

    -   TSO 割り当ては、システム クロックが逆行しても影響を受けなくなりました。

    -   メタデータによってもたらされるオーバーヘッドを削減する`Region merge`機能をサポート

-   スケジューラを最適化する

    -   ダウンストアの処理を最適化してレプリカの作成を高速化

    -   ホットスポット スケジューラを最適化して、トラフィック統計情報が不安定になったときの適応性を向上させます

    -   Coordinator の起動を最適化して、PD の再起動によって発生する不要なスケジューリングを減らします

    -   Balance Scheduler が小さなリージョンを頻繁にスケジュールする問題を最適化します

    -   リージョンマージを最適化して、 リージョン内の行数を考慮する

    -   [スケジューリング ポリシーを制御するコマンドをさらに追加する](/pd-control.md#config-show--set-option-value--placement-rules)

    -   スケジューリング シナリオをシミュレートするための改善[PDシミュレーター](https://github.com/pingcap/pd/tree/release-2.1/tools/pd-simulator)

-   API・運用ツール

    -   [`GetPrevRegion`インターフェイス](https://github.com/pingcap/kvproto/blob/8e3f33ac49297d7c93b61a955531191084a2f685/proto/pdpb.proto#L40)を追加して`TiDB reverse scan`機能をサポートする

    -   [`BatchSplitRegion`インターフェイス](https://github.com/pingcap/kvproto/blob/8e3f33ac49297d7c93b61a955531191084a2f685/proto/pdpb.proto#L54)を追加して、TiKVリージョン分割を高速化します

    -   TiDB で分散 GC をサポートするには[`GCSafePoint`インターフェイス](https://github.com/pingcap/kvproto/blob/8e3f33ac49297d7c93b61a955531191084a2f685/proto/pdpb.proto#L64-L66)を追加します

    -   [`GetAllStores`インターフェイス](https://github.com/pingcap/kvproto/blob/8e3f33ac49297d7c93b61a955531191084a2f685/proto/pdpb.proto#L32)を追加して、TiDB で分散 GC をサポートします

    <!---->

    -   pd-ctl は以下をサポートしています:
        -   [リージョン分割の統計の使用](/pd-control.md#operator-check--show--add--remove)

        -   [`jq`を呼び出して JSON 出力をフォーマットする](/pd-control.md#jq-formatted-json-output-usage)

        -   [指定店舗のリージョン情報の確認](/pd-control.md#region-store-store_id)

        -   [バージョン別にソートされた topNリージョンリストの確認](/pd-control.md#region-topconfver-limit)

        -   [サイズでソートされたtopNリージョンリストを確認する](/pd-control.md#region-topsize-limit)

        -   [より正確な TSO エンコーディング](/pd-control.md#tso)

    <!---->

    -   [pd-回復](/pd-recover.md) `max-replica`パラメーターを提供する必要はありません

-   指標

    -   `Filter`の関連指標を追加

    -   etcd Raftステート マシンに関するメトリクスを追加する

-   パフォーマンス

    -   リージョンハートビートのパフォーマンスを最適化して、ハートビートによってもたらされるメモリオーバーヘッドを削減します

    -   リージョンツリーのパフォーマンスを最適化する

    -   ホットスポット統計の計算パフォーマンスを最適化する

## TiKV {#tikv}

-   コプロセッサー

    -   組み込み関数をさらに追加する

    -   [コプロセッサー`ReadPool`を追加して、リクエストを処理する際の同時実行性を向上させます](https://github.com/tikv/rfcs/blob/master/text/0010-read-pool.md)

    -   時間関数の解析の問題とタイム ゾーン関連の問題を修正します。

    -   プッシュダウン集計計算のメモリ使用量を最適化する

-   トランザクション

    -   スキャン操作のパフォーマンスを向上させるために MVCC の読み取りロジックとメモリ使用量を最適化し、フル テーブル スキャンのパフォーマンスは TiDB 2.0 よりも 1 倍優れています。

    -   読み取りパフォーマンスを確保するために、連続ロールバック レコードを折りたたむ

    -   [`UnsafeDestroyRange` API を追加して、削除するテーブル/インデックス用のスペースの収集をサポートします](https://github.com/tikv/rfcs/blob/master/text/0002-unsafe-destroy-range.md)

    -   GCモジュールを分離して書き込みへの影響を軽減

    -   `kv_scan`コマンドに`upper bound`サポートを追加

-   Raftstore

    -   スナップショットの書き込みプロセスを改善して、RocksDB のストールを回避します

    -   [`LocalReader`スレッドを追加して読み取り要求を処理し、読み取り要求の遅延を減らします](https://github.com/tikv/rfcs/pull/17)

    -   [`BatchSplit`をサポートして、大量の書き込みによってもたらされる大きなリージョンを回避します](https://github.com/tikv/rfcs/pull/6)

    -   統計によると、I/O オーバーヘッドを削減するために`Region Split`サポート

    -   キーの数に応じて`Region Split`サポートし、インデックス スキャンの同時実行性を向上させます

    -   `Region Split`によってもたらされる不必要な遅延を回避するために、 Raftメッセージ プロセスを改善します。

    -   `PreVote`機能をデフォルトで有効にして、サービスに対するネットワーク分離の影響を軽減します

-   ストレージ エンジン

    -   RocksDB の`CompactFiles`バグを修正し、Lightning を使用したデータのインポートへの影響を軽減します

    -   RocksDB を v5.15 にアップグレードして、スナップショット ファイルが破損する可能性がある問題を修正します。

    -   フラッシュが書き込みをブロックする可能性がある問題を回避するために`IngestExternalFile`を改善します。

-   tikv-ctl

    -   [`ldb`コマンドを追加して、RocksDB 関連の問題を診断します](https://tikv.org/docs/3.0/reference/tools/tikv-ctl/#ldb-command)

    -   `compact`コマンドは、最下位レベルのデータを圧縮するかどうかの指定をサポートします

## ツール {#tools}

-   大量データの高速完全インポート: [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)

-   新しい[TiDBBinlog](/tidb-binlog/tidb-binlog-overview.md)をサポート

## アップグレードの注意事項 {#upgrade-caveat}

-   新しいstorageエンジンが採用されているため、TiDB 2.1 は v2.0.x 以前へのダウングレードをサポートしていません。

<!---->

-   並列 DDL は TiDB 2.1 で有効になっているため、TiDB バージョンが 2.0.1 より前のクラスターは、ローリング アップデートを使用して 2.1 にアップグレードできません。次の 2 つのオプションのいずれかを選択できます。

    -   クラスターを停止し、2.1 に直接アップグレードする
    -   2.0.1 以降の 2.0.x バージョンにロール アップデートしてから、2.1 バージョンにロール アップデートします。

<!---->

-   TiDB 2.0.6 以前から TiDB 2.1 にアップグレードする場合、進行中の DDL 操作、特に時間のかかる`Add Index`操作があるかどうかを確認してください。これは、DDL 操作によってアップグレード プロセスが遅くなるためです。進行中の DDL 操作がある場合は、DDL 操作が完了するまで待ってから、更新をロールします。
