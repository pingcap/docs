---
title: TiDB 2.1 GA Release Notes
summary: TiDB 2.1 GA は、安定性、パフォーマンス、互換性、および使いやすさが大幅に向上して、2018 年 11 月 30 日にリリースされました。このリリースには、SQL オプティマイザー、SQL エグゼキューター、統計、式、サーバー、DDL、互換性、配置Driver(PD)、TiKV、およびツールの最適化が含まれています。また、高速なフルデータ インポートのためのTiDB Lightningが導入され、新しい TiDB Binlogがサポートされています。ただし、TiDB 2.1 では、新しいstorageエンジンの採用により、v2.0.x 以前へのダウングレードはサポートされていません。さらに、TiDB 2.1 では並列 DDL が有効になっているため、2.0.1 より前のバージョンの TiDB を使用しているクラスターは、ローリング アップデートを使用して 2.1 にアップグレードできません。TiDB 2.0.6 以前から TiDB 2.1 にアップグレードする場合、進行中の DDL 操作によってアップグレード プロセスが遅くなる可能性があります。
---

# TiDB 2.1 GA リリースノート {#tidb-2-1-ga-release-notes}

2018 年 11 月 30 日に、TiDB 2.1 GA がリリースされました。このリリースの次の更新を参照してください。TiDB 2.0 と比較して、このリリースでは安定性、パフォーマンス、互換性、および使いやすさが大幅に向上しています。

## ティビ {#tidb}

-   SQL オプティマイザー

    -   実行パフォーマンスを向上させるために選択範囲`Index Join`を最適化します

    -   `Index Join`の外部テーブルの選択を最適化し、行数の推定値が小さいテーブルを外部テーブルとして使用します。

    -   適切なインデックスがなくてもマージ結合を使用できるように結合ヒント`TIDB_SMJ`最適化します。

    -   結合ヒント`TIDB_INLJ`を最適化して、結合する内部テーブルを指定します。

    -   相関サブクエリを最適化し、フィルタをプッシュダウンし、インデックスの選択範囲を拡張することで、一部のクエリの効率が桁違いに向上します。

    -   `UPDATE`番目と`DELETE`のステートメントでインデックスヒントと結合ヒントの使用をサポートします。

    -   より多くの関数の押し下げをサポート: `ABS` / `CEIL` / `FLOOR` / `IS TRUE` / `IS FALSE`

    -   組み込み関数`IF`と`IFNULL`の定数畳み込みアルゴリズムを最適化する

    -   `EXPLAIN`文の出力を最適化し、階層構造を使用して演算子間の関係を示します。

-   SQLエグゼキュータ

    -   すべての集計関数をリファクタリングし、 `Stream`と`Hash`の集計演算子の実行効率を改善します。

    -   並列`Hash Aggregate`演算子を実装し、いくつかのシナリオで計算パフォーマンスを350%向上

    -   並列`Project`演算子を実装し、いくつかのシナリオでパフォーマンスを74%向上

    -   実行パフォーマンスを向上させるために、 `Hash Join`の内部テーブルと外部テーブルのデータを同時に読み取ります。

    -   `REPLACE INTO`文の実行速度を最適化し、パフォーマンスを約10倍向上

    -   時間データ型のメモリ使用量を最適化し、時間データ型のメモリ使用量を 50% 削減します。

    -   ポイント選択のパフォーマンスを最適化し、Sysbench のポイント選択効率の結果を 60% 向上します。

    -   ワイドテーブルの挿入や更新における TiDB のパフォーマンスを 20 倍向上

    -   設定ファイル内の単一ステートメントのメモリ上限の設定をサポート

    -   ハッシュ結合の実行を最適化します。結合タイプが内部結合またはセミ結合で、内部テーブルが空の場合、外部テーブルからデータを読み取らずに結果を返します。

    -   [`EXPLAIN ANALYZE`ステートメント](/sql-statements/sql-statement-explain-analyze.md)を使用して、各演算子の実行時間と返された行数を含む実行時統計をチェックする機能をサポートします。

-   統計

    -   一日の特定の時間帯のみに自動分析統計を有効にすることをサポート

    -   クエリのフィードバックに応じてテーブル統計を自動的に更新する機能をサポート

    -   `ANALYZE TABLE WITH BUCKETS`ステートメントを使用してヒストグラム内のバケットの数を設定できるようになりました。

    -   等価クエリと範囲クエリの混合クエリのヒストグラムを使用して行数推定アルゴリズムを最適化します。

-   表現

    -   次の組み込み関数をサポートします:

        -   `json_contains`

        -   `json_contains_path`

        -   `encode/decode`

-   サーバ

    -   競合トランザクションのパフォーマンスを最適化するために、tidb-server インスタンス内でローカルに競合するトランザクションをキューイングすることをサポートします。

    -   サーバーサイドカーソルをサポート

    <!---->

    -   [HTTP API](https://github.com/pingcap/tidb/blob/release-2.1/docs/tidb_http_api.md)加える

        -   TiKVクラスター内のテーブル領域の分布を分散する

        -   `general log`開くかどうかを制御します

        -   オンラインでのログレベルの変更をサポート

        -   TiDBクラスタ情報を確認する

    <!---->

    -   [分析の比率を制御するための`auto_analyze_ratio`システム変数を追加します。](/faq/sql-faq.md#whats-the-trigger-strategy-for-auto-analyze-in-tidb)

    -   [トランザクションの自動再試行回数を制御するために`tidb_retry_limit`システム変数を追加します。](/system-variables.md#tidb_retry_limit)

    -   [トランザクションが自動的に再試行されるかどうかを制御するには、 `tidb_disable_txn_auto_retry`システム変数を追加します。](/system-variables.md#tidb_disable_txn_auto_retry)

    -   [遅いクエリを取得するために`admin show slow`ステートメントの使用をサポートします](/identify-slow-queries.md#admin-show-slow-command)

    -   [`tidb_slow_log_threshold`環境変数を追加して、スローログのしきい値を自動的に設定します。](/system-variables.md#tidb_slow_log_threshold)

    -   [`tidb_query_log_max_len`環境変数を追加して、ログ内で切り捨てられるSQL文の長さを動的に設定します。](/system-variables.md#tidb_query_log_max_len)

-   DDL

    -   時間のかかるインデックス追加操作が他の操作をブロックするのを避けるために、インデックス追加ステートメントと他のステートメントの並列実行をサポートします。

    -   `ADD INDEX`の実行速度を最適化し、いくつかのシナリオで大幅に改善しました

    -   TiDBが`DDL Owner`であるかどうかの判断を容易にするために`select tidb_is_ddl_owner()`ステートメントをサポートする

    -   `ALTER TABLE FORCE`構文をサポートする

    -   `ALTER TABLE RENAME KEY TO`構文をサポートする

    -   `admin show ddl jobs`の出力情報にテーブル名とデータベース名を追加します

    -   [`ddl/owner/resign` HTTP インターフェースを使用して DDL 所有者を解放し、新しい DDL 所有者の選出を開始することをサポートします。](https://github.com/pingcap/tidb/blob/release-2.1/docs/tidb_http_api.md)

-   互換性

    -   より多くのMySQL構文をサポート

    -   `BIT`集計関数が`ALL`パラメータをサポートするようにする

    -   `SHOW PRIVILEGES`声明を支持する

    -   `LOAD DATA`ステートメントの`CHARACTER SET`構文をサポートする

    -   `CREATE USER`ステートメントの`IDENTIFIED WITH`構文をサポートする

    -   `LOAD DATA IGNORE LINES`声明を支持する

    -   `Show ProcessList`文はより正確な情報を返します

## 配置Driver（PD） {#placement-driver-pd}

-   可用性を最適化する

    -   バージョン管理メカニズムを導入し、クラスタのローリングアップデートを互換性を持ってサポートする

    -   ネットワーク分離後にネットワークが回復したときにリーダーの再選出を回避するためにPDノード間で[`Raft PreVote`有効にする](https://github.com/pingcap/pd/blob/5c7b18cf3af91098f07cf46df0b59fbf8c7c5462/conf/config.toml#L22)

    -   スケジュール中にマシン障害によってデータが利用できなくなるリスクを軽減するために、デフォルトで`raft learner`有効にします。

    -   TSO割り当てはシステムクロックの逆戻りの影響を受けなくなりました

    -   メタデータによってもたらされるオーバーヘッドを削減する`Region merge`機能をサポートする

-   スケジューラを最適化する

    -   ダウンストアの処理を最適化してレプリカの作成を高速化

    -   ホットスポットスケジューラを最適化し、トラフィック統計情報の変動に対する適応性を向上させる

    -   PDの再起動による不要なスケジュールを削減するためにコーディネーターの起動を最適化します。

    -   バランススケジューラが小さな領域を頻繁にスケジュールする問題を最適化します。

    -   リージョン内の行数を考慮してリージョンのマージを最適化します

    -   [スケジュールポリシーを制御するためのコマンドを追加する](/pd-control.md#config-show--set-option-value--placement-rules)

    -   スケジューリングシナリオをシミュレートするために[PDシミュレータ](https://github.com/pingcap/pd/tree/release-2.1/tools/pd-simulator)改善

-   APIと操作ツール

    -   `TiDB reverse scan`機能をサポートするために[`GetPrevRegion`インターフェース](https://github.com/pingcap/kvproto/blob/8e3f33ac49297d7c93b61a955531191084a2f685/proto/pdpb.proto#L40)追加します

    -   [`BatchSplitRegion`インターフェース](https://github.com/pingcap/kvproto/blob/8e3f33ac49297d7c93b61a955531191084a2f685/proto/pdpb.proto#L54)追加すると、TiKVリージョン分割が高速化されます。

    -   TiDBで分散GCをサポートするには[`GCSafePoint`インターフェース](https://github.com/pingcap/kvproto/blob/8e3f33ac49297d7c93b61a955531191084a2f685/proto/pdpb.proto#L64-L66)追加します

    -   TiDBで分散GCをサポートするために[`GetAllStores`インターフェース](https://github.com/pingcap/kvproto/blob/8e3f33ac49297d7c93b61a955531191084a2f685/proto/pdpb.proto#L32)追加します。

    <!---->

    -   pd-ctl は以下をサポートします:
        -   [リージョン分割の統計情報を使用する](/pd-control.md#operator-check--show--add--remove)

        -   [`jq`呼び出してJSON出力をフォーマットする](/pd-control.md#jq-formatted-json-output-usage)

        -   [指定された店舗のリージョン情報を確認する](/pd-control.md#region-store-store_id)

        -   [バージョン別にソートされた上位Nリージョンリストを確認する](/pd-control.md#region-topconfver-limit)

        -   [規模順に並べられた上位Nリージョンリストを確認する](/pd-control.md#region-topsize-limit)

        -   [より正確なTSOエンコーディング](/pd-control.md#tso)

    <!---->

    -   [pd-回復](/pd-recover.md) `max-replica`パラメータを提供する必要がない

-   メトリクス

    -   `Filter`の関連指標を追加

    -   etcd Raftステートマシンに関するメトリクスを追加する

-   パフォーマンス

    -   リージョンハートビートのパフォーマンスを最適化し、ハートビートによって生じるメモリオーバーヘッドを削減します。

    -   リージョンツリーのパフォーマンスを最適化する

    -   ホットスポット統計の計算パフォーマンスを最適化する

## ティクヴ {#tikv}

-   コプロセッサー

    -   組み込み関数を追加する

    -   [リクエスト処理の同時実行性を向上させるためにコプロセッサー`ReadPool`を追加します](https://github.com/tikv/rfcs/blob/master/text/0010-read-pool.md)

    -   時間関数の解析問題とタイムゾーン関連の問題を修正

    -   プッシュダウン集計計算のメモリ使用量を最適化する

-   トランザクション

    -   MVCC の読み取りロジックとメモリ使用量を最適化してスキャン操作のパフォーマンスを向上させ、フルテーブルスキャンのパフォーマンスは TiDB 2.0 よりも 1 倍向上しました。

    -   連続ロールバックレコードを折り畳んで読み取りパフォーマンスを確保します

    -   [`UnsafeDestroyRange` API を追加して、テーブル/インデックスの削除のためのスペースの収集をサポートします。](https://github.com/tikv/rfcs/blob/master/text/0002-unsafe-destroy-range.md)

    -   GCモジュールを分離して書き込みへの影響を軽減する

    -   `kv_scan`コマンドに`upper bound`サポートを追加します

-   Raftstore

    -   RocksDB の停止を回避するためにスナップショット書き込みプロセスを改善する

    -   [読み取り要求を処理するための`LocalReader`スレッドを追加し、読み取り要求の遅延を減らします。](https://github.com/tikv/rfcs/pull/17)

    -   [大量の書き込みによる大きなリージョンを回避するために、 `BatchSplit`サポートします。](https://github.com/tikv/rfcs/pull/6)

    -   統計に従って`Region Split`サポートし、I/Oオーバーヘッドを削減します

    -   インデックススキャンの同時実行性を向上させるためにキーの数に応じて`Region Split`サポートします

    -   `Region Split`によってもたらされる不要な遅延を回避するためにRaftメッセージプロセスを改善します

    -   ネットワーク分離によるサービスへの影響を軽減するために、 `PreVote`機能をデフォルトで有効にします。

-   ストレージエンジン

    -   RocksDBの`CompactFiles`バグを修正し、Lightningを使用したデータのインポートへの影響を軽減します

    -   スナップショットファイルの破損の可能性のある問題を修正するために、RocksDB を v5.15 にアップグレードしてください。

    -   フラッシュが書き込みをブロックする問題を回避するために`IngestExternalFile`改善しました

-   tikv-ctl

    -   [RocksDB関連の問題を診断するための`ldb`コマンドを追加します](https://tikv.org/docs/3.0/reference/tools/tikv-ctl/#ldb-command)

    -   `compact`コマンドは、最下層のデータを圧縮するかどうかの指定をサポートします。

## ツール {#tools}

-   大量のデータの高速フルインポート: [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)

-   新規サポート[TiDBBinlog](/tidb-binlog/tidb-binlog-overview.md)

## アップグレードの注意事項 {#upgrade-caveat}

-   TiDB 2.1は、新しいstorageエンジンの採用により、v2.0.x以前へのダウングレードをサポートしていません。

<!---->

-   TiDB 2.1 では並列 DDL が有効になっているため、TiDB バージョン 2.0.1 より前のクラスターはローリング アップデートを使用して 2.1 にアップグレードできません。次の 2 つのオプションのいずれかを選択できます。

    -   クラスターを停止し、直接2.1にアップグレードします
    -   2.0.1 以降の 2.0.x バージョンにロール アップデートし、その後 2.1 バージョンにロール アップデートします。

<!---->

-   TiDB 2.0.6 以前から TiDB 2.1 にアップグレードする場合は、進行中の DDL 操作、特に時間のかかる`Add Index`操作があるかどうかを確認してください。DDL 操作によってアップグレード プロセスが遅くなるためです。進行中の DDL 操作がある場合は、DDL 操作が完了するまで待ってからロール更新を行ってください。
