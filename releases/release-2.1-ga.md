---
title: TiDB 2.1 GA Release Notes
---

# TiDB2.1GAリリースノート {#tidb-2-1-ga-release-notes}

2018年11月30日、TiDB2.1GAがリリースされました。このリリースの次の更新を参照してください。このリリースでは、TiDB 2.0と比較して、安定性、パフォーマンス、互換性、および使いやすさが大幅に向上しています。

## TiDB {#tidb}

-   SQLオプティマイザー

    -   `Index Join`の選択範囲を最適化して、実行パフォーマンスを向上させます

    -   `Index Join`の外部テーブルの選択を最適化し、行カウントの推定値が小さいテーブルを外部テーブルとして使用します

    -   結合ヒント`TIDB_SMJ`を最適化して、適切なインデックスが利用できない場合でもマージ結合を使用できるようにします

    -   結合ヒント`TIDB_INLJ`を最適化して、結合する内部テーブルを指定します

    -   相関サブクエリを最適化し、フィルタを押し下げ、インデックスの選択範囲を拡張して、一部のクエリの効率を桁違いに向上させます

    -   `UPDATE`および`DELETE`ステートメントでのインデックスヒントと結合ヒントの使用のサポート

    -   より多くの機能の`CEIL` `IS FALSE`を`IS TRUE` `FLOOR` `ABS`

    -   `IF`および`IFNULL`の組み込み関数の定数畳み込みアルゴリズムを最適化します

    -   `EXPLAIN`ステートメントの出力を最適化し、階層構造を使用して演算子間の関係を示します

-   SQLエグゼキュータ

    -   すべての集計関数をリファクタリングし、 `Stream`および`Hash`の集計演算子の実行効率を向上させます

    -   並列`Hash Aggregate`演算子を実装し、一部のシナリオでコンピューティングパフォーマンスを350％向上させます

    -   並列`Project`演算子を実装し、一部のシナリオでパフォーマンスを74％向上させます

    -   実行性能を向上させるために、 `Hash Join`の内部テーブルと外部テーブルのデータを同時に読み取ります。

    -   `REPLACE INTO`ステートメントの実行速度を最適化し、パフォーマンスをほぼ10倍向上させます

    -   時間データ型のメモリ使用量を最適化し、時間データ型のメモリ使用量を50％削減します

    -   ポイント選択のパフォーマンスを最適化し、Sysbenchのポイント選択効率の結果を60％向上させます

    -   ワイドテーブルの挿入または更新時のTiDBのパフォーマンスを20倍向上させます

    -   構成ファイル内の単一ステートメントのメモリー上限の構成をサポート

    -   ハッシュ結合の実行を最適化します。結合タイプが内部結合または半結合であり、内部テーブルが空の場合、外部テーブルからデータを読み取らずに結果を返します。

    -   [`EXPLAIN ANALYZE`ステートメント](/sql-statements/sql-statement-explain-analyze.md)を使用して、実行時間や各演算子の返された行数などの実行時統計を確認することをサポートします

-   統計

    -   1日の特定の期間にのみ自動ANALYZE統計を有効にすることをサポート

    -   クエリのフィードバックに従ってテーブル統計を自動的に更新することをサポートします

    -   `ANALYZE TABLE WITH BUCKETS`ステートメントを使用したヒストグラム内のバケット数の構成をサポート

    -   等式クエリと範囲クエリの混合クエリのヒストグラムを使用して、行数推定アルゴリズムを最適化します

-   式

    -   次の組み込み関数をサポートします。

        -   `json_contains`

        -   `json_contains_path`

        -   `encode/decode`

-   サーバ

    -   競合するトランザクションのパフォーマンスを最適化するために、tidb-serverインスタンス内でローカルに競合するトランザクションのキューイングをサポートする

    -   サーバー側カーソルのサポート

    <!---->

    -   [HTTP API](https://github.com/pingcap/tidb/blob/master/docs/tidb_http_api.md)を追加します

        -   TiKVクラスタのテーブル領域の分布を分散させる

        -   `general log`を開くかどうかを制御します

        -   オンラインでのログレベルの変更をサポート

        -   TiDBクラスタ情報を確認してください

    <!---->

    -   [`auto_analyze_ratio`システム変数を追加して、Analyzeの比率を制御します](/faq/sql-faq.md#whats-the-trigger-strategy-for-auto-analyze-in-tidb)

    -   [`tidb_retry_limit`システム変数を追加して、トランザクションの自動再試行時間を制御します](/system-variables.md#tidb_retry_limit)

    -   [`tidb_disable_txn_auto_retry`システム変数を追加して、トランザクションが自動的に再試行するかどうかを制御します](/system-variables.md#tidb_disable_txn_auto_retry)

    -   [遅いクエリを取得するための`admin show slow`ステートメントの使用をサポート](/identify-slow-queries.md#admin-show-slow-command)

    -   [`tidb_slow_log_threshold`環境変数を追加して、低速ログのしきい値を自動的に設定します](/system-variables.md#tidb_slow_log_threshold)

    -   [`tidb_query_log_max_len`環境変数を追加して、ログで動的に切り捨てられるSQLステートメントの長さを設定します](/system-variables.md#tidb_query_log_max_len)

-   DDL

    -   Add indexステートメントと他のステートメントの並列実行をサポートして、時間のかかるAddindex操作が他の操作をブロックしないようにします。

    -   `ADD INDEX`の実行速度を最適化し、一部のシナリオでは大幅に改善します

    -   TiDBが`DDL Owner`であるかどうかの決定を容易にするために、 `select tidb_is_ddl_owner()`ステートメントをサポートします

    -   `ALTER TABLE FORCE`構文をサポートする

    -   `ALTER TABLE RENAME KEY TO`構文をサポートする

    -   `admin show ddl jobs`の出力情報にテーブル名とデータベース名を追加します。

    -   [`ddl/owner/resign` HTTPインターフェースを使用してDDL所有者を解放し、新しいDDL所有者の選出を開始することをサポートします](https://github.com/pingcap/tidb/blob/master/docs/tidb_http_api.md)

-   互換性

    -   より多くのMySQL構文をサポートする

    -   `BIT`集計関数が`ALL`パラメーターをサポートするようにします

    -   `SHOW PRIVILEGES`のステートメントをサポートする

    -   `LOAD DATA`ステートメントで`CHARACTER SET`構文をサポートする

    -   `CREATE USER`ステートメントで`IDENTIFIED WITH`構文をサポートする

    -   `LOAD DATA IGNORE LINES`のステートメントをサポートする

    -   `Show ProcessList`ステートメントは、より正確な情報を返します

## 配置ドライバー（PD） {#placement-driver-pd}

-   可用性を最適化する

    -   バージョン管理メカニズムを導入し、互換性のあるクラスタのローリング更新をサポートします

    -   ネットワーク分離後にネットワークが回復したときにリーダーが再選されるのを防ぐために、PDノード間で[`Raft PreVote`有効にする](https://github.com/pingcap/pd/blob/5c7b18cf3af91098f07cf46df0b59fbf8c7c5462/conf/config.toml#L22)

    -   デフォルトで`raft learner`を有効にすると、スケジューリング中のマシン障害によってデータが利用できなくなるリスクが低くなります。

    -   TSOの割り当ては、システムクロックが逆方向になることによる影響を受けなくなりました。

    -   `Region merge`つの機能をサポートして、メタデータによってもたらされるオーバーヘッドを削減します

-   スケジューラーを最適化する

    -   ダウンストアの処理を最適化して、レプリカの作成を高速化します

    -   ホットスポットスケジューラを最適化して、トラフィック統計情報がジッターするときの適応性を向上させます

    -   コーディネーターの開始を最適化して、PDの再起動によって引き起こされる不要なスケジューリングを減らします

    -   BalanceSchedulerが小さなリージョンを頻繁にスケジュールする問題を最適化します

    -   リージョンマージを最適化して、リージョン内の行数を検討します

    -   [スケジューリングポリシーを制御するコマンドを追加します](/pd-control.md#config-show--set-option-value--placement-rules)

    -   [PDシミュレーター](https://github.com/pingcap/pd/tree/release-2.1/tools/pd-simulator)を改善して、スケジューリングシナリオをシミュレートします

-   APIおよび操作ツール

    -   `TiDB reverse scan`機能をサポートするために[`GetPrevRegion`インターフェース](https://github.com/pingcap/kvproto/blob/8e3f33ac49297d7c93b61a955531191084a2f685/proto/pdpb.proto#L40)を追加します

    -   [`BatchSplitRegion`インターフェース](https://github.com/pingcap/kvproto/blob/8e3f33ac49297d7c93b61a955531191084a2f685/proto/pdpb.proto#L54)を追加すると、TiKVリージョンの分割が高速化されます

    -   TiDBで分散GCをサポートするために[`GCSafePoint`インターフェース](https://github.com/pingcap/kvproto/blob/8e3f33ac49297d7c93b61a955531191084a2f685/proto/pdpb.proto#L64-L66)を追加します

    -   TiDBで分散GCをサポートするには、 [`GetAllStores`インターフェース](https://github.com/pingcap/kvproto/blob/8e3f33ac49297d7c93b61a955531191084a2f685/proto/pdpb.proto#L32)を追加します

    <!---->

    -   pd-ctlは以下をサポートします：
        -   [リージョン分割の統計を使用する](/pd-control.md#operator-check--show--add--remove)

        -   [`jq`を呼び出してJSON出力をフォーマットする](/pd-control.md#jq-formatted-json-output-usage)

        -   [指定店舗の地域情報を確認する](/pd-control.md#region-store-store_id)

        -   [バージョン別にソートされたtopNリージョンリストをチェックする](/pd-control.md#region-topconfver-limit)

        -   [サイズでソートされたtopNリージョンリストをチェック](/pd-control.md#region-topsize-limit)

        -   [より正確なTSOエンコーディング](/pd-control.md#tso)

    <!---->

    -   [pd-recover](/pd-recover.md)は`max-replica`パラメータを提供する必要はありません

-   指標

    -   `Filter`の関連メトリックを追加します

    -   etcdRaftステートマシンに関するメトリックを追加します

-   パフォーマンス

    -   リージョンハートビートのパフォーマンスを最適化して、ハートビートによってもたらされるメモリオーバーヘッドを削減します

    -   リージョンツリーのパフォーマンスを最適化する

    -   ホットスポット統計の計算のパフォーマンスを最適化する

## TiKV {#tikv}

-   コプロセッサー

    -   組み込み関数を追加する

    -   [コプロセッサー`ReadPool`を追加して、要求の処理における同時実行性を向上させます](https://github.com/tikv/rfcs/blob/master/text/2017-12-22-read-pool.md)

    -   時間関数の解析の問題とタイムゾーンに関連する問題を修正します

    -   プッシュダウンアグリゲーションコンピューティングのメモリ使用量を最適化する

-   取引

    -   MVCCの読み取りロジックとメモリ使用量を最適化して、スキャン操作のパフォーマンスを向上させます。全表スキャンのパフォーマンスは、TiDB2.0のパフォーマンスの1倍です。

    -   連続ロールバックレコードを折りたたんで、読み取りパフォーマンスを確保します

    -   [`UnsafeDestroyRange` APIを追加して、ドロップするテーブル/インデックスのスペースの収集をサポートします](https://github.com/tikv/rfcs/blob/master/text/2018-08-29-unsafe-destroy-range.md)

    -   書き込みへの影響を減らすためにGCモジュールを分離します

    -   `kv_scan`コマンドに`upper bound`サポートを追加します

-   ラフトストア

    -   RocksDBのストールを回避するために、スナップショットの書き込みプロセスを改善します

    -   [`LocalReader`スレッドを追加して、読み取り要求を処理し、読み取り要求の遅延を減らします](https://github.com/tikv/rfcs/pull/17)

    -   [大量の書き込みによってもたらされる大きな領域を回避するために`BatchSplit`をサポートする](https://github.com/tikv/rfcs/pull/6)

    -   I / Oオーバーヘッドを削減するために、統計に従って`Region Split`をサポートします

    -   キーの数に応じて`Region Split`をサポートし、インデックススキャンの同時実行性を向上させます

    -   ラフトメッセージプロセスを改善して、 `Region Split`による不要な遅延を回避します

    -   ネットワーク分離がサービスに与える影響を減らすために、デフォルトで`PreVote`機能を有効にします

-   ストレージエンジン

    -   RocksDBの`CompactFiles`のバグを修正し、Lightningを使用してデータをインポートする際の影響を軽減します

    -   RocksDBをv5.15にアップグレードして、スナップショットファイルの破損の問題を修正します

    -   フラッシュが書き込みをブロックする可能性がある問題を回避するために`IngestExternalFile`を改善します

-   tikv-ctl

    -   [RocksDB関連の問題を診断するための`ldb`コマンドを追加します](https://tikv.org/docs/3.0/reference/tools/tikv-ctl/#ldb-command)

    -   `compact`コマンドは、最下位レベルでデータを圧縮するかどうかの指定をサポートします

## ツール {#tools}

-   大量のデータの高速フルインポート： [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)

-   新しい[TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md)をサポートする

## アップグレードの警告 {#upgrade-caveat}

-   TiDB 2.1は、新しいストレージエンジンの採用により、v2.0.x以前へのダウングレードをサポートしていません。

<!---->

-   並列DDLはTiDB2.1で有効になっているため、2.0.1より前のバージョンのTiDBを持つクラスターは、ローリングアップデートを使用して2.1にアップグレードできません。次の2つのオプションのいずれかを選択できます。

    -   クラスタを停止し、2.1に直接アップグレードします
    -   2.0.1以降の2.0.xバージョンにロールアップデートしてから、2.1バージョンにロールアップデートします。

<!---->

-   TiDB2.0.6以前からTiDB2.1にアップグレードする場合、DDL操作はアップグレードプロセスを遅くするため、進行中のDDL操作、特に時間のかかる`Add Index`操作があるかどうかを確認します。進行中のDDL操作がある場合は、DDL操作が終了するのを待ってから、更新をロールします。
