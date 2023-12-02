---
title: TiDB 2.1 GA Release Notes
---

# TiDB 2.1 GA リリース ノート {#tidb-2-1-ga-release-notes}

2018 年 11 月 30 日に、TiDB 2.1 GA がリリースされました。このリリースの次の更新を参照してください。 TiDB 2.0 と比較して、このリリースでは安定性、パフォーマンス、互換性、使いやすさが大幅に向上しています。

## TiDB {#tidb}

-   SQLオプティマイザー

    -   `Index Join`の選択範囲を最適化して実行パフォーマンスを向上させます。

    -   外表の選択を`Index Join`に最適化し、行数の推定値が小さい表を外表として使用します。

    -   適切なインデックスが利用できない場合でもマージ結合を使用できるように結合ヒント`TIDB_SMJ`を最適化します。

    -   結合ヒント`TIDB_INLJ`を最適化して結合する内部テーブルを指定する

    -   相関サブクエリを最適化し、フィルターをプッシュダウンし、インデックス選択範囲を拡張して、一部のクエリの効率を桁違いに向上させます。

    -   `UPDATE`ステートメントと`DELETE`ステートメントでのインデックス ヒントと結合ヒントの使用のサポート

    -   より多くの関数の押し下げをサポート: `ABS` / `CEIL` / `FLOOR` / `IS TRUE` / `IS FALSE`

    -   組み込み関数`IF`および`IFNULL`定数折りたたみアルゴリズムを最適化します。

    -   `EXPLAIN`ステートメントの出力を最適化し、階層構造を使用して演算子間の関係を表示します。

-   SQL実行者

    -   すべての集計関数をリファクタリングし、 `Stream`と`Hash`の集計演算子の実行効率を向上させます。

    -   並列`Hash Aggregate`演算子を実装し、一部のシナリオでコンピューティング パフォーマンスを 350% 向上させます。

    -   並列`Project`演算子を実装すると、一部のシナリオでパフォーマンスが 74% 向上します。

    -   `Hash Join`の内部テーブルと外部テーブルのデータを同時に読み込み、実行パフォーマンスを向上させます。

    -   `REPLACE INTO`ステートメントの実行速度を最適化し、パフォーマンスを 10 倍近く向上させます。

    -   時間データ型のメモリ使用量を最適化し、時間データ型のメモリ使用量を 50% 削減します。

    -   ポイント選択パフォーマンスを最適化し、Sysbench のポイント選択効率の結果を 60% 向上させます。

    -   幅の広いテーブルの挿入または更新における TiDB のパフォーマンスが 20 倍向上します。

    -   構成ファイル内の単一ステートメントのメモリ上限の構成をサポート

    -   ハッシュ結合の実行を最適化します。結合タイプが内部結合またはセミ結合で、内部テーブルが空の場合、外部テーブルからデータを読み取らずに結果を返します。

    -   [`EXPLAIN ANALYZE`文](/sql-statements/sql-statement-explain-analyze.md)を使用して、各演算子の実行時間や返された行数などの実行時統計を確認できるようになりました。

-   統計

    -   一日の特定の時間帯のみ自動分析統計を有効にするサポート

    -   クエリのフィードバックに従ってテーブル統計を自動的に更新するサポート

    -   `ANALYZE TABLE WITH BUCKETS`ステートメントを使用したヒストグラム内のバケット数の構成のサポート

    -   等価クエリと範囲クエリの混合クエリに対してヒストグラムを使用して行数推定アルゴリズムを最適化します。

-   式

    -   次の組み込み関数をサポートします。

        -   `json_contains`

        -   `json_contains_path`

        -   `encode/decode`

-   サーバ

    -   競合するトランザクションのパフォーマンスを最適化するために、tidb-server インスタンス内でローカルに競合するトランザクションをキューに入れることをサポートします。

    -   サーバー側カーソルのサポート

    <!---->

    -   [HTTP API](https://github.com/pingcap/tidb/blob/master/docs/tidb_http_api.md)を追加します

        -   TiKV クラスター内のテーブル リージョンの分散

        -   `general log`を開くかどうかを制御します。

        -   オンラインでのログレベルの変更のサポート

        -   TiDB クラスター情報を確認する

    <!---->

    -   [`auto_analyze_ratio`システム変数を追加して、Analyze の比率を制御します。](/faq/sql-faq.md#whats-the-trigger-strategy-for-auto-analyze-in-tidb)

    -   [トランザクションの自動再試行時間を制御するために`tidb_retry_limit`システム変数を追加します。](/system-variables.md#tidb_retry_limit)

    -   [`tidb_disable_txn_auto_retry`システム変数を追加して、トランザクションを自動的に再試行するかどうかを制御します](/system-variables.md#tidb_disable_txn_auto_retry)

    -   [`admin show slow`ステートメントを使用したスロー クエリの取得のサポート](/identify-slow-queries.md#admin-show-slow-command)

    -   [`tidb_slow_log_threshold`環境変数を追加して、遅いログのしきい値を自動的に設定します。](/system-variables.md#tidb_slow_log_threshold)

    -   [`tidb_query_log_max_len`環境変数を追加して、ログ内で動的に切り詰められる SQL ステートメントの長さを設定します。](/system-variables.md#tidb_query_log_max_len)

-   DDL

    -   時間のかかるインデックスの追加操作が他の操作をブロックすることを回避するために、インデックスの追加ステートメントと他のステートメントの並列実行をサポートします。

    -   `ADD INDEX`の実行速度を最適化し、一部のシナリオで大幅に改善します。

    -   TiDB が`DDL Owner`であるかどうかの判断を容易にするために`select tidb_is_ddl_owner()`ステートメントをサポートします。

    -   `ALTER TABLE FORCE`構文をサポートする

    -   `ALTER TABLE RENAME KEY TO`構文をサポートする

    -   `admin show ddl jobs`の出力情報にテーブル名とデータベース名を追加します。

    -   [DDL 所有者を解放し、新しい DDL 所有者の選択を開始するための`ddl/owner/resign` HTTP インターフェイスの使用のサポート](https://github.com/pingcap/tidb/blob/master/docs/tidb_http_api.md)

-   互換性

    -   より多くの MySQL 構文をサポートする

    -   `BIT`集計関数が`ALL`パラメータをサポートするようにします。

    -   `SHOW PRIVILEGES`ステートメントをサポートします

    -   `LOAD DATA`ステートメントで`CHARACTER SET`構文をサポートします

    -   `CREATE USER`ステートメントで`IDENTIFIED WITH`構文をサポートします

    -   `LOAD DATA IGNORE LINES`ステートメントをサポートします

    -   `Show ProcessList`ステートメントはより正確な情報を返します

## 配置Driver(PD) {#placement-driver-pd}

-   可用性の最適化

    -   バージョン管理メカニズムを導入し、クラスターのローリング アップデートを互換的にサポートします。

    -   ネットワーク分離後にネットワークが回復したときにリーダーの再選を回避するため、PD ノード間で[`Raft PreVote`を有効にする](https://github.com/pingcap/pd/blob/5c7b18cf3af91098f07cf46df0b59fbf8c7c5462/conf/config.toml#L22)

    -   デフォルトで`raft learner`有効にすると、スケジュール中のマシンの障害によってデータが利用できなくなるリスクが軽減されます。

    -   TSO 割り当ては、システム クロックの逆行による影響を受けなくなりました。

    -   メタデータによってもたらされるオーバーヘッドを削減する`Region merge`機能をサポートします。

-   スケジューラーを最適化する

    -   ダウンストアの処理を最適化し、レプリカの作成を高速化します。

    -   ホットスポット スケジューラを最適化して、トラフィック統計情報が不安定な場合の適応性を向上させます。

    -   コーディネーターの起動を最適化して、PD の再起動によって生じる不必要なスケジューリングを削減します。

    -   Balance Scheduler が小さなリージョンを頻繁にスケジュールする問題を最適化します。

    -   リージョン内の行数を考慮してリージョンのマージを最適化します。

    -   [スケジュール ポリシーを制御するコマンドをさらに追加します。](/pd-control.md#config-show--set-option-value--placement-rules)

    -   スケジューリング シナリオをシミュレートするために[PDシミュレータ](https://github.com/pingcap/pd/tree/release-2.1/tools/pd-simulator)を改善します。

-   APIと運用ツール

    -   `TiDB reverse scan`機能をサポートするには[`GetPrevRegion`インターフェース](https://github.com/pingcap/kvproto/blob/8e3f33ac49297d7c93b61a955531191084a2f685/proto/pdpb.proto#L40)を追加します

    -   [`BatchSplitRegion`インターフェース](https://github.com/pingcap/kvproto/blob/8e3f33ac49297d7c93b61a955531191084a2f685/proto/pdpb.proto#L54)を追加すると、TiKVリージョンの分割が高速化されます。

    -   TiDB で分散 GC をサポートするには[`GCSafePoint`インターフェース](https://github.com/pingcap/kvproto/blob/8e3f33ac49297d7c93b61a955531191084a2f685/proto/pdpb.proto#L64-L66)を追加します。

    -   TiDB で分散 GC をサポートするには、 [`GetAllStores`インターフェース](https://github.com/pingcap/kvproto/blob/8e3f33ac49297d7c93b61a955531191084a2f685/proto/pdpb.proto#L32)を追加します。

    <!---->

    -   pd-ctl は以下をサポートします。
        -   [リージョン分割の統計の使用](/pd-control.md#operator-check--show--add--remove)

        -   [`jq`を呼び出して JSON 出力をフォーマットする](/pd-control.md#jq-formatted-json-output-usage)

        -   [指定した店舗のリージョン情報を確認する](/pd-control.md#region-store-store_id)

        -   [バージョン別にソートされた上位 Nリージョンリストを確認する](/pd-control.md#region-topconfver-limit)

        -   [サイズ順に並べ替えられた上位 Nリージョンリストを確認する](/pd-control.md#region-topsize-limit)

        -   [より正確な TSO エンコーディング](/pd-control.md#tso)

    <!---->

    -   [PD回復](/pd-recover.md)は`max-replica`パラメータを指定する必要はありません

-   メトリクス

    -   `Filter`の関連指標を追加

    -   etcd Raftステートマシンに関するメトリクスを追加

-   パフォーマンス

    -   リージョンハートビートのパフォーマンスを最適化し、ハートビートによってもたらされるメモリオーバーヘッドを削減します。

    -   リージョンツリーのパフォーマンスを最適化する

    -   ホットスポット統計の計算パフォーマンスを最適化する

## TiKV {#tikv}

-   コプロセッサー

    -   組み込み関数をさらに追加する

    -   [コプロセッサー`ReadPool`を追加して、リクエスト処理の同時実行性を向上させます。](https://github.com/tikv/rfcs/blob/master/text/0010-read-pool.md)

    -   時間関数の解析問題とタイムゾーン関連の問題を修正

    -   プッシュダウン集計コンピューティングのメモリ使用量を最適化する

-   トランザクション

    -   MVCC の読み取りロジックとメモリ使用量を最適化してスキャン操作のパフォーマンスを向上させ、フル テーブル スキャンのパフォーマンスが TiDB 2.0 よりも 1 倍向上しました。

    -   連続したロールバック レコードをフォールドして読み取りパフォーマンスを確保します

    -   [`UnsafeDestroyRange` API を追加して、テーブル/インデックスを削除するためのスペースの収集をサポートします。](https://github.com/tikv/rfcs/blob/master/text/0002-unsafe-destroy-range.md)

    -   書き込みへの影響を軽減するために GC モジュールを分離する

    -   `kv_scan`コマンドに`upper bound`サポートを追加します。

-   Raftstore

    -   RocksDB の停止を回避するためにスナップショット書き込みプロセスを改善します。

    -   [`LocalReader`スレッドを追加して読み取りリクエストを処理し、読み取りリクエストの遅延を短縮します。](https://github.com/tikv/rfcs/pull/17)

    -   [大量の書き込みによってもたらされる大きなリージョンを回避するために`BatchSplit`をサポートします](https://github.com/tikv/rfcs/pull/6)

    -   I/O オーバーヘッドを削減するために、統計に従って`Region Split`サポートします。

    -   キーの数に応じて`Region Split`サポートし、インデックス スキャンの同時実行性を向上させます。

    -   Raftメッセージ プロセスを改善して、 `Region Split`によってもたらされる不必要な遅延を回避します。

    -   サービスに対するネットワーク分離の影響を軽減するには、デフォルトで`PreVote`機能を有効にします。

-   ストレージエンジン

    -   RocksDB の`CompactFiles`バグを修正し、Lightning を使用したデータのインポートへの影響を軽減します。

    -   RocksDB を v5.15 にアップグレードして、スナップショット ファイルの破損の可能性がある問題を修正します

    -   フラッシュが書き込みをブロックする可能性がある問題を回避するために`IngestExternalFile`を改善しました。

-   tikv-ctl

    -   [RocksDB 関連の問題を診断するための`ldb`コマンドを追加します。](https://tikv.org/docs/3.0/reference/tools/tikv-ctl/#ldb-command)

    -   `compact`コマンドは、最下位レベルでデータを圧縮するかどうかの指定をサポートします。

## ツール {#tools}

-   大量のデータの高速完全インポート: [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)

-   新しい[TiDBBinlog](/tidb-binlog/tidb-binlog-overview.md)をサポート

## アップグレードに関する注意事項 {#upgrade-caveat}

-   TiDB 2.1 は、新しいstorageエンジンを採用しているため、v2.0.x 以前へのダウングレードをサポートしていません。

<!---->

-   TiDB 2.1 では並列 DDL が有効になっているため、TiDB バージョン 2.0.1 より前のクラスターは、ローリング アップデートを使用して 2.1 にアップグレードできません。次の 2 つのオプションのいずれかを選択できます。

    -   クラスターを停止し、2.1 に直接アップグレードします。
    -   2.0.1 以降の 2.0.x バージョンにロール アップデートしてから、2.1 バージョンにロール アップデートします。

<!---->

-   TiDB 2.0.6 以前から TiDB 2.1 にアップグレードする場合は、進行中の DDL 操作、特に時間のかかる`Add Index`操作があるかどうかを確認してください。これは、DDL 操作によりアップグレード プロセスが遅くなるためです。進行中の DDL 操作がある場合は、DDL 操作が終了するまで待ってから、ロール更新を実行します。
