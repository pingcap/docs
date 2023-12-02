---
title: TiDB 3.0.0-rc.1 Release Notes
---

# TiDB 3.0.0-rc.1 リリースノート {#tidb-3-0-0-rc-1-release-notes}

リリース日：2019年5月10日

TiDB バージョン: 3.0.0-rc.1

TiDB Ansible バージョン: 3.0.0-rc.1

## 概要 {#overview}

2019 年 5 月 10 日に、TiDB 3.0.0-rc.1 がリリースされました。対応する TiDB Ansible バージョンは 3.0.0-rc.1 です。 TiDB 3.0.0-beta.1 と比較して、このリリースでは安定性、使いやすさ、機能、SQL オプティマイザー、統計、実行エンジンが大幅に向上しています。

## TiDB {#tidb}

-   SQLオプティマイザー
    -   列間の順序相関を使用してコスト見積もりの​​精度を向上させます。ヒューリスティック パラメーター`tidb_opt_correlation_exp_factor`を導入して、相関関係を推定に直接使用できない場合のシナリオでインデックス スキャンの優先順位を制御します。 [#9839](https://github.com/pingcap/tidb/pull/9839)
    -   フィルタ[#10053](https://github.com/pingcap/tidb/pull/10053)に該当する列がある場合、複合インデックスのアクセス条件を抽出する際に、より多くのインデックスの接頭列と一致します。
    -   動的プログラミング アルゴリズムを使用して、結合に参加しているテーブルの数が値`tidb_opt_join_reorder_threshold`未満の場合の結合操作の実行順序を指定します。 [#8816](https://github.com/pingcap/tidb/pull/8816)
    -   アクセス条件として複合インデックスを使用する場合、インデックス結合を構築する内部テーブル内のインデックスのより多くのプレフィックス列と一致します[#8471](https://github.com/pingcap/tidb/pull/8471)
    -   NULL 値[#9474](https://github.com/pingcap/tidb/pull/9474)を持つ単一列インデックスの行数推定の精度を向上させます。
    -   論理最適化フェーズ中に集計関数を削除する場合は、誤った実行を防ぐために`GROUP_CONCAT`特別に処理します[#9967](https://github.com/pingcap/tidb/pull/9967)
    -   フィルターが定数[#9848](https://github.com/pingcap/tidb/pull/9848)の場合、フィルターを結合演算子の子ノードに適切にプッシュダウンします。
    -   MySQL [#10064](https://github.com/pingcap/tidb/pull/10064)の非互換性を防ぐために、論理最適化フェーズ中に列をプルーニングするときに`RAND()`などの一部の関数を特別に処理します。
    -   サポート`FAST ANALYZE` 。領域全体をスキャンするのではなく、領域をサンプリングすることで統計収集を高速化します。この機能は変数`tidb_enable_fast_analyze`によって制御されます。 [#10258](https://github.com/pingcap/tidb/pull/10258)
    -   SQL ステートメントの実行計画バインドを実行することで実行の安定性を確保する SQL 計画管理をサポートします。この機能は現在ベータ版であり、SELECT ステートメントのバインドされた実行プランのみをサポートします。本番環境での使用はお勧めしません。 [#10284](https://github.com/pingcap/tidb/pull/10284)

-   実行エンジン
    -   3 つの演算子 ( `TableReader` `IndexReader`および`IndexLookupReader`でのメモリ使用量の追跡と制御をサポートします[#10003](https://github.com/pingcap/tidb/pull/10003)
    -   コプロセッサ内のタスク数、実行時間/待機時間の平均/最長/90%、実行時間または待機時間が最も長い TiKV のアドレスなど、低速ログ内のコプロセッサ タスクに関する詳細情報の表示をサポートします[#10165](https://github.com/pingcap/tidb/pull/10165)
    -   プレースホルダーなしで準備された DDL ステートメントをサポートします[#10144](https://github.com/pingcap/tidb/pull/10144)

-   サーバ
    -   TiDB の開始時にのみ DDL 所有者にブートストラップの実行を許可する[#10029](https://github.com/pingcap/tidb/pull/10029)
    -   変数`tidb_skip_isolation_level_check`を追加して、トランザクション分離レベルをSERIALIZABLE [#10065](https://github.com/pingcap/tidb/pull/10065)に設定するときに TiDB がエラーを報告しないようにします。
    -   暗黙的なコミット時間と SQL 実行時間をスローログ[#10294](https://github.com/pingcap/tidb/pull/10294)にマージします。
        -   SQL ロールのサポート (RBAC権限管理)
        -   サポート`SHOW GRANT` [#10016](https://github.com/pingcap/tidb/pull/10016)
        -   サポート`SET DEFAULT ROLE` [#9949](https://github.com/pingcap/tidb/pull/9949)
    -   サポート`GRANT ROLE` [#9721](https://github.com/pingcap/tidb/pull/9721)
    -   TiDB を終了させる`whitelist`プラグインの`ConnectionEvent`エラーを修正[#9889](https://github.com/pingcap/tidb/pull/9889)
    -   読み取り専用ステートメントをトランザクション履歴に誤って追加する問題を修正[#9723](https://github.com/pingcap/tidb/pull/9723)
    -   `kill`ステートメントを改善して SQL の実行を停止し、リソースをより迅速に解放します[#9844](https://github.com/pingcap/tidb/pull/9844)
    -   起動オプション`config-check`を追加して、設定ファイル[#9855](https://github.com/pingcap/tidb/pull/9855)の有効性を確認します。
    -   厳密な SQL モードが無効になっている場合の NULL フィールド挿入の有効性チェックを修正しました[#10161](https://github.com/pingcap/tidb/pull/10161)

-   DDL
    -   `CREATE TABLE`ステートメントに対して`pre_split_regions`オプションを追加します。このオプションは、テーブル作成後の大量の書き込みによって引き起こされる書き込みホットスポットを回避するために、テーブルを作成する際のテーブルリージョンの事前分割をサポートします[#10138](https://github.com/pingcap/tidb/pull/10138)
    -   一部の DDL ステートメントの実行パフォーマンスを最適化します[#10170](https://github.com/pingcap/tidb/pull/10170)
    -   `FULLTEXT KEY` [#9821](https://github.com/pingcap/tidb/pull/9821)ではフルテキスト インデックスがサポートされていないという警告を追加します。
    -   TiDB [#9820](https://github.com/pingcap/tidb/pull/9820)の古いバージョンにおける UTF8 および UTF8MB4 文字セットの互換性の問題を修正
    -   表[#9868](https://github.com/pingcap/tidb/pull/9868)の`shard_row_id_bits`の潜在的なバグを修正
    -   テーブルの文字セットを変更しても列の文字セットが変更されないバグを修正[#9790](https://github.com/pingcap/tidb/pull/9790)
    -   列のデフォルト値[#9897](https://github.com/pingcap/tidb/pull/9897)として`BINARY` / `BIT`を使用する場合の`SHOW COLUMN`の潜在的なバグを修正しました。
    -   `SHOW FULL COLUMNS`ステートメント[#10007](https://github.com/pingcap/tidb/pull/10007)の`CHARSET` / `COLLATION`の説明を表示する際の互換性の問題を修正
    -   `SHOW COLLATIONS`ステートメントが TiDB [#10186](https://github.com/pingcap/tidb/pull/10186)でサポートされている照合順序のみをリストする問題を修正します。

## PD {#pd}

-   ETCD [#1452](https://github.com/pingcap/pd/pull/1452)のアップグレード
    -   etcdとPDサーバーのログ形式を統一する
    -   PreVoteでLeaderを選出できない問題を修正
    -   後続のリクエストのブロックを回避するために、失敗する「提案」リクエストと「読み取り」リクエストの高速ドロップをサポートします。
    -   リースのデッドロック問題を修正する
-   ホット ストアがキーの不正な統計を作成する問題を修正します[#1487](https://github.com/pingcap/pd/pull/1487)
-   単一 PD ノードからの PD クラスターの強制再構築のサポート[#1485](https://github.com/pingcap/pd/pull/1485)
-   `regionScatterer`が無効な`OperatorStep` [#1482](https://github.com/pingcap/pd/pull/1482)を生成する可能性がある問題を修正
-   `MergeRegion`オペレーター[#1495](https://github.com/pingcap/pd/pull/1495)の短すぎるタイムアウト問題を修正
-   ホット リージョンのスケジューリングを優先するサポート[#1492](https://github.com/pingcap/pd/pull/1492)
-   PDサーバー側での TSO 要求の処理時間を記録するためのメトリックを追加します[#1502](https://github.com/pingcap/pd/pull/1502)
-   対応するストア ID とアドレスをストア[#1506](https://github.com/pingcap/pd/pull/1506)に関連するメトリクスに追加します。
-   `GetOperator`サービスをサポート[#1477](https://github.com/pingcap/pd/pull/1477)
-   ストアが見つからないため、ハートビート ストリームでエラーを送信できない問題を修正します[#1521](https://github.com/pingcap/pd/pull/1521)

## TiKV {#tikv}

-   エンジン
    -   読み取りトラフィック[#4436](https://github.com/tikv/tikv/pull/4436)に関する不正確な統計を引き起こす可能性がある問題を修正しました。
    -   範囲[#4503](https://github.com/tikv/tikv/pull/4503)を削除するときにプレフィックス抽出panicを引き起こす可能性がある問題を修正します。
    -   メモリ管理を最適化して、 `Iterator Key Bound Option` [#4537](https://github.com/tikv/tikv/pull/4537)のメモリ割り当てとコピーを削減します。
    -   学習者のログギャップを考慮しないと、場合によってはpanic[#4559](https://github.com/tikv/tikv/pull/4559)が発生する問題を修正
    -   異なる`column families` [#4612](https://github.com/tikv/tikv/pull/4612)間での`block cache`共有をサポート

-   サーバ
    -   `batch commands` [#4473](https://github.com/tikv/tikv/pull/4473)のコンテキスト スイッチのオーバーヘッドを削減します。
    -   シークイテレータステータス[#4470](https://github.com/tikv/tikv/pull/4470)の有効性をチェックする

-   RaftStore
    -   サポート構成可能`properties index distance` [#4517](https://github.com/tikv/tikv/pull/4517)

-   コプロセッサー
    -   バッチインデックススキャンエグゼキュータの追加[#4419](https://github.com/tikv/tikv/pull/4419)
    -   ベクトル化された評価フレームワークを追加[#4322](https://github.com/tikv/tikv/pull/4322)
    -   バッチ エグゼキュータの実行概要フレームワークを追加[#4433](https://github.com/tikv/tikv/pull/4433)
    -   評価panic[#4481](https://github.com/tikv/tikv/pull/4481)を引き起こす可能性のある無効な列オフセットを避けるために、RPN 式を構築するときに最大列を確認してください。
    -   `BatchLimitExecutor` [#4469](https://github.com/tikv/tikv/pull/4469)を追加
    -   コンテキストスイッチ[#4486](https://github.com/tikv/tikv/pull/4486)を減らすために、ReadPool の元の`futures-cpupool` `tokio-threadpool`に置き換えます。
    -   バッチ集計フレームワークの追加[#4533](https://github.com/tikv/tikv/pull/4533)
    -   `BatchSelectionExecutor` [#4562](https://github.com/tikv/tikv/pull/4562)を追加
    -   バッチアグレッション機能追加`AVG` [#4570](https://github.com/tikv/tikv/pull/4570)
    -   RPN機能追加`LogicalAnd` [#4575](https://github.com/tikv/tikv/pull/4575)

-   その他
    -   メモリアロケータ[#4370](https://github.com/tikv/tikv/pull/4370)として`tcmalloc`をサポート

## ツール {#tools}

-   TiDBBinlog
    -   unsigned int 型の主キー列のbinlogデータが負の[#573](https://github.com/pingcap/tidb-binlog/pull/573)である場合のレプリケーション中止の問題を修正
    -   downstream が`pb`の場合は圧縮オプションを提供しません。ダウンストリーム名を`pb`から`file` [#559](https://github.com/pingcap/tidb-binlog/pull/559)に変更します。
    -   ローカルstorage[#509](https://github.com/pingcap/tidb-binlog/pull/509)での非同期フラッシュを可能にする`storage.sync-log`構成項目をPumpに追加します。
    -   PumpとDrainer [#495](https://github.com/pingcap/tidb-binlog/pull/495)間の通信のトラフィック圧縮をサポート
    -   異なる SQL モード[#511](https://github.com/pingcap/tidb-binlog/pull/511)での DDL クエリの解析をサポートするために、 Drainerに`syncer.sql-mode`構成項目を追加します。
    -   レプリケーションを必要としないテーブルのフィルタリングをサポートするために`syncer.ignore-table`構成アイテムを追加します[#520](https://github.com/pingcap/tidb-binlog/pull/520)

-   稲妻
    -   行 ID またはデフォルトの列値を使用して、ダンプ ファイルに含まれていない列データを入力します[#170](https://github.com/pingcap/tidb-lightning/pull/170)
    -   SST の一部がインポートに失敗した場合でもインポート成功が返されることがあるインポーターのバグを修正しました[#4566](https://github.com/tikv/tikv/pull/4566)
    -   SST を TiKV [#4412](https://github.com/tikv/tikv/pull/4412)にアップロードする際のインポーターでの速度制限のサポート
    -   サイズごとのテーブルのインポートをサポートし、大きなテーブルのチェックサムと分析によるクラスターへの影響を軽減し、チェックサムと分析[#156](https://github.com/pingcap/tidb-lightning/pull/156)の成功率を向上させます。
    -   データソースファイルを TiDB の type.Datum として直接解析し、KV エンコーダからの余分な解析オーバーヘッドを節約することで、Lightning の SQL エンコードパフォーマンスが 50% 向上します[#145](https://github.com/pingcap/tidb-lightning/pull/145)
    -   ログ形式を[統一されたログ形式](https://github.com/tikv/rfcs/blob/master/text/0018-unified-log-format.md) [#162](https://github.com/pingcap/tidb-lightning/pull/162)に変更します
    -   構成ファイルが見つからない場合に使用するコマンド ライン オプションをいくつか追加します[#157](https://github.com/pingcap/tidb-lightning/pull/157)

-   同期差分インスペクター
    -   チェックポイントをサポートして検証ステータスを記録し、再起動後に最後に保存されたポイントから検証を続行します[#224](https://github.com/pingcap/tidb-tools/pull/224)
    -   チェックサムを計算してデータの整合性をチェックするための`only-use-checksum`構成アイテムを追加します[#215](https://github.com/pingcap/tidb-tools/pull/215)

## TiDB Ansible {#tidb-ansible}

-   より多くの TiKV 監視パネルをサポートし、Ansible、Grafana、Prometheus [#727](https://github.com/pingcap/tidb-ansible/pull/727)のバージョンを更新します
    -   クラスターのステータスを表示するための概要ダッシュボード
    -   問題のトラブルシューティングのためのトラブルシューティング ダッシュボード
    -   開発者が問題を分析するための詳細ダッシュボード
-   Kafka バージョン[#730](https://github.com/pingcap/tidb-ansible/pull/730)の TiDB Binlogのダウンロードに失敗するバグを修正
-   サポートされているオペレーティング システムのバージョン制限を CentOS 7.0 以降および Red Hat 7.0 以降として変更します[#733](https://github.com/pingcap/tidb-ansible/pull/733)
-   ローリング アップデート中のバージョン検出モードをマルチ同時[#736](https://github.com/pingcap/tidb-ansible/pull/736)に変更します。
-   README [#740](https://github.com/pingcap/tidb-ansible/pull/740)のドキュメントのリンクを更新する
-   冗長な TiKV モニタリング メトリクスを削除します。トラブルシューティング用の新しいメトリクスを追加[#735](https://github.com/pingcap/tidb-ansible/pull/735)
-   表[#739](https://github.com/pingcap/tidb-ansible/pull/739)によるリーダー分布を表示するために`table-regions.py`スクリプトを最適化します。
-   Drainer [#745](https://github.com/pingcap/tidb-ansible/pull/745)の設定ファイルを更新する
-   SQL カテゴリごとにレイテンシーを表示する新しいパネルで TiDB モニタリングを最適化します[#747](https://github.com/pingcap/tidb-ansible/pull/747)
-   Lightning 設定ファイルを更新し、 `tidb_lightning_ctl`スクリプト[#1e946f8](https://github.com/pingcap/tidb-ansible/commit/1e946f89908e8fd6ef84128c6da3064ddfccf6a8)を追加します。
