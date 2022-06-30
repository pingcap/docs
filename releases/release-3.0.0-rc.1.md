---
title: TiDB 3.0.0-rc.1 Release Notes
---

# TiDB3.0.0-rc.1リリースノート {#tidb-3-0-0-rc-1-release-notes}

発売日：2019年5月10日

TiDBバージョン：3.0.0-rc.1

TiDB Ansibleバージョン：3.0.0-rc.1

## 概要 {#overview}

2019年5月10日、TiDB3.0.0-rc.1がリリースされました。対応するTiDBAnsibleのバージョンは3.0.0-rc.1です。このリリースでは、TiDB 3.0.0-beta.1と比較して、安定性、使いやすさ、機能、SQLオプティマイザー、統計、および実行エンジンが大幅に改善されています。

## TiDB {#tidb}

-   SQLオプティマイザー
    -   列間の順序相関を使用して、コスト見積もりの精度を向上させます。ヒューリスティックパラメーター`tidb_opt_correlation_exp_factor`を導入して、相関を直接推定に使用できないシナリオのインデックススキャンの優先度を制御します。 [＃9839](https://github.com/pingcap/tidb/pull/9839)
    -   フィルタ[＃10053](https://github.com/pingcap/tidb/pull/10053)に関連する列がある場合、複合インデックスのアクセス条件を抽出するときに、インデックスのより多くのプレフィックス列に一致します。
    -   動的計画法アルゴリズムを使用して、結合に参加しているテーブルの数が`tidb_opt_join_reorder_threshold`の値より少ない場合の結合操作の実行順序を指定します。 [＃8816](https://github.com/pingcap/tidb/pull/8816)
    -   アクセス条件として複合インデックスを使用する場合に、インデックス結合を構築する内部テーブルのインデックスのより多くのプレフィックス列に一致します[＃8471](https://github.com/pingcap/tidb/pull/8471)
    -   NULL値を持つ単一列インデックスの行数推定の精度を向上させます[＃9474](https://github.com/pingcap/tidb/pull/9474)
    -   誤った実行を防ぐために、論理最適化フェーズで集計関数を削除する場合は、特に`GROUP_CONCAT`を処理します[＃9967](https://github.com/pingcap/tidb/pull/9967)
    -   フィルタが定数[＃9848](https://github.com/pingcap/tidb/pull/9848)の場合は、フィルタを結合演算子の子ノードに適切にプッシュダウンします。
    -   MySQL [＃10064](https://github.com/pingcap/tidb/pull/10064)との非互換性を防ぐために、論理最適化フェーズで列をプルーニングするときに`RAND()`などの一部の関数を特別に処理します。
    -   サポート`FAST ANALYZE`は、領域全体をスキャンするのではなく、領域をサンプリングすることで統計収集を高速化します。この機能は、変数`tidb_enable_fast_analyze`によって制御されます。 [＃10258](https://github.com/pingcap/tidb/pull/10258)
    -   SQLステートメントの実行プランバインディングを実行することで実行の安定性を確保するSQLプラン管理をサポートします。この機能は現在ベータ版であり、SELECTステートメントのバインドされた実行プランのみをサポートします。実稼働環境での使用はお勧めしません。 [＃10284](https://github.com/pingcap/tidb/pull/10284)

-   実行エンジン
    -   `IndexReader` `TableReader`および`IndexLookupReader` [＃10003](https://github.com/pingcap/tidb/pull/10003) ）でのメモリー使用量の追跡と制御をサポートします。
    -   コプロセッサー内のタスクの数、実行/待機時間の平均/最長/ 90％、実行時間または待機時間が最も長いTiKVのアドレスなど、コプロセッサータスクに関する詳細情報を低速ログに表示することをサポートします[＃10165](https://github.com/pingcap/tidb/pull/10165)
    -   プレースホルダーなしで準備されたDDLステートメントをサポートする[＃10144](https://github.com/pingcap/tidb/pull/10144)

-   サーバ
    -   TiDBの起動時にのみDDL所有者にブートストラップの実行を許可する[＃10029](https://github.com/pingcap/tidb/pull/10029)
    -   変数`tidb_skip_isolation_level_check`を追加して、トランザクション分離レベルをSERIALIZABLE3に設定するときに[＃10065](https://github.com/pingcap/tidb/pull/10065)がエラーを報告しないようにします。
    -   スローログ[＃10294](https://github.com/pingcap/tidb/pull/10294)の暗黙的なコミット時間とSQL実行時間をマージします
        -   SQLロールのサポート（RBAC権限管理）
        -   [＃10016](https://github.com/pingcap/tidb/pull/10016) `SHOW GRANT`
        -   [＃9949](https://github.com/pingcap/tidb/pull/9949) `SET DEFAULT ROLE`
    -   [＃9721](https://github.com/pingcap/tidb/pull/9721) `GRANT ROLE`
    -   TiDBを[＃9889](https://github.com/pingcap/tidb/pull/9889)で終了させる`whitelist`プラグインからの`ConnectionEvent`のエラーを修正します
    -   トランザクション履歴に読み取り専用ステートメントを誤って追加する問題を修正します[＃9723](https://github.com/pingcap/tidb/pull/9723)
    -   `kill`ステートメントを改善して、SQLの実行を停止し、リソースをより迅速に解放します[＃9844](https://github.com/pingcap/tidb/pull/9844)
    -   スタートアップオプション`config-check`を追加して、構成ファイル[＃9855](https://github.com/pingcap/tidb/pull/9855)の有効性を確認します。
    -   厳密なSQLモードが無効になっている場合にNULLフィールドを挿入する有効性チェックを修正しました[＃10161](https://github.com/pingcap/tidb/pull/10161)

-   DDL
    -   `CREATE TABLE`のステートメントに`pre_split_regions`のオプションを追加します。このオプションは、テーブル作成時にテーブル領域を事前に分割して、テーブル作成後の大量の書き込みによって引き起こされる書き込みホットスポットを回避することをサポートします[＃10138](https://github.com/pingcap/tidb/pull/10138)
    -   一部のDDLステートメントの実行パフォーマンスを最適化する[＃10170](https://github.com/pingcap/tidb/pull/10170)
    -   フルテキストインデックスは13 [＃9821](https://github.com/pingcap/tidb/pull/9821)サポートされていないという警告を追加し`FULLTEXT KEY`
    -   古いバージョンのTiDB1のUTF8およびUTF8MB4文字セットの互換性の問題を修正し[＃9820](https://github.com/pingcap/tidb/pull/9820)
    -   表[＃9868](https://github.com/pingcap/tidb/pull/9868)の`shard_row_id_bits`の潜在的なバグを修正します
    -   テーブルの文字セットが変更された後、列の文字セットが変更されないというバグを修正します[＃9790](https://github.com/pingcap/tidb/pull/9790)
    -   列のデフォルト値として`BINARY`を使用する場合の`SHOW COLUMN`の潜在的なバグを修正し`BIT` [＃9897](https://github.com/pingcap/tidb/pull/9897)
    -   `COLLATION`ステートメント`SHOW FULL COLUMNS`に`CHARSET`の説明を表示する際の互換性の問題を修正し[＃10007](https://github.com/pingcap/tidb/pull/10007) 。
    -   `SHOW COLLATIONS`ステートメントがTiDB3でサポートされている照合のみをリストするという問題を修正し[＃10186](https://github.com/pingcap/tidb/pull/10186)

## PD {#pd}

-   [＃1452](https://github.com/pingcap/pd/pull/1452)をアップグレードする
    -   etcdとPDサーバーのログ形式を統合する
    -   PreVoteによるリーダーの選出に失敗する問題を修正
    -   後続のリクエストのブロックを回避できない「提案」および「読み取り」リクエストの高速ドロップをサポート
    -   リースのデッドロックの問題を修正
-   ホットストアがキーの誤った統計を作成する問題を修正します[＃1487](https://github.com/pingcap/pd/pull/1487)
-   単一のPDノードからのPDクラスタの強制的な再構築をサポート[＃1485](https://github.com/pingcap/pd/pull/1485)
-   `regionScatterer`が無効な[＃1482](https://github.com/pingcap/pd/pull/1482)を生成する可能性がある問題を修正し`OperatorStep`
-   `MergeRegion`演算子[＃1495](https://github.com/pingcap/pd/pull/1495)の短すぎるタイムアウトの問題を修正します
-   ホットリージョンスケジューリングを優先するサポート[＃1492](https://github.com/pingcap/pd/pull/1492)
-   PDサーバー側でTSO要求を処理する時間を記録するためのメトリックを追加します[＃1502](https://github.com/pingcap/pd/pull/1502)
-   対応するストアIDとアドレスをストア[＃1506](https://github.com/pingcap/pd/pull/1506)に関連するメトリックに追加します
-   `GetOperator`サービスをサポート[＃1477](https://github.com/pingcap/pd/pull/1477)
-   ストアが見つからないためにハートビートストリームでエラーを送信できない問題を修正します[＃1521](https://github.com/pingcap/pd/pull/1521)

## TiKV {#tikv}

-   エンジン
    -   読み取りトラフィックの誤った統計を引き起こす可能性のある問題を修正します[＃4436](https://github.com/tikv/tikv/pull/4436)
    -   範囲[＃4503](https://github.com/tikv/tikv/pull/4503)を削除するときにプレフィックスエクストラクタパニックを引き起こす可能性がある問題を修正します
    -   メモリ管理を最適化して、 [＃4537](https://github.com/tikv/tikv/pull/4537)のメモリ割り当てとコピーを削減し`Iterator Key Bound Option`
    -   学習者のログギャップを考慮しないと、場合によってはパニックが発生する可能性があるという問題を修正します[＃4559](https://github.com/tikv/tikv/pull/4559)
    -   異なる[＃4612](https://github.com/tikv/tikv/pull/4612)間での`block cache` `column families`共有をサポート

-   サーバ
    -   [＃4473](https://github.com/tikv/tikv/pull/4473)のコンテキストスイッチのオーバーヘッドを削減し`batch commands`
    -   シークイテレータステータスの有効性を確認する[＃4470](https://github.com/tikv/tikv/pull/4470)

-   RaftStore
    -   構成可能な[＃4517](https://github.com/tikv/tikv/pull/4517) `properties index distance`

-   コプロセッサー
    -   バッチインデックススキャンエグゼキュータ[＃4419](https://github.com/tikv/tikv/pull/4419)を追加します
    -   ベクトル化された評価フレームワークを追加する[＃4322](https://github.com/tikv/tikv/pull/4322)
    -   バッチエグゼキュータの実行サマリーフレームワークを追加する[＃4433](https://github.com/tikv/tikv/pull/4433)
    -   評価パニックを引き起こす可能性のある無効な列オフセットを回避するために、RPN式を作成するときに最大列を確認してください[＃4481](https://github.com/tikv/tikv/pull/4481)
    -   `BatchLimitExecutor`を[＃4469](https://github.com/tikv/tikv/pull/4469)
    -   ReadPoolで元の`futures-cpupool`を`tokio-threadpool`に置き換えて、コンテキストスイッチ[＃4486](https://github.com/tikv/tikv/pull/4486)を減らします
    -   バッチ集約フレームワークの追加[＃4533](https://github.com/tikv/tikv/pull/4533)
    -   `BatchSelectionExecutor`を[＃4562](https://github.com/tikv/tikv/pull/4562)
    -   [＃4570](https://github.com/tikv/tikv/pull/4570)攻撃関数を追加する`AVG`
    -   [＃4575](https://github.com/tikv/tikv/pull/4575)機能を追加`LogicalAnd`

-   その他
    -   メモリアロケータ[＃4370](https://github.com/tikv/tikv/pull/4370)としてサポート`tcmalloc`

## ツール {#tools}

-   TiDB Binlog
    -   unsignedint型の主キー列のbinlogデータが負の場合のレプリケーション中止の問題を修正します[＃573](https://github.com/pingcap/tidb-binlog/pull/573)
    -   ダウンストリームが`pb`の場合、圧縮オプションを提供しません。ダウンストリーム名を`pb`から[＃559](https://github.com/pingcap/tidb-binlog/pull/559)に変更し`file`
    -   ローカルストレージでの非同期フラッシュを可能にする`storage.sync-log`の構成アイテムをPumpに追加します[＃509](https://github.com/pingcap/tidb-binlog/pull/509)
    -   ポンプとドレイナー[＃495](https://github.com/pingcap/tidb-binlog/pull/495)間の通信のトラフィック圧縮をサポートします
    -   Drainerに`syncer.sql-mode`の構成アイテムを追加して、さまざまなsql- [＃511](https://github.com/pingcap/tidb-binlog/pull/511)でのDDLクエリの解析をサポートします。
    -   レプリケーションを必要としないテーブルの除外をサポートするために`syncer.ignore-table`の構成アイテムを追加します[＃520](https://github.com/pingcap/tidb-binlog/pull/520)

-   雷
    -   行IDまたはデフォルトの列値を使用して、ダンプファイルで欠落している列データを入力します[＃170](https://github.com/pingcap/tidb-lightning/pull/170)
    -   SSTの一部がインポートに失敗した場合でも、インポートの成功が返される可能性があるというImporterのバグを修正します[＃4566](https://github.com/tikv/tikv/pull/4566)
    -   SSTを[＃4412](https://github.com/tikv/tikv/pull/4412)にアップロードする際のインポーターの速度制限をサポート
    -   サイズごとのテーブルのインポートをサポートして、大きなテーブルのChecksumとAnalyzeによるクラスタへの影響を減らし、Checksumと[＃156](https://github.com/pingcap/tidb-lightning/pull/156)の成功率を向上させます。
    -   データソースファイルをtypes.Datumとして直接解析し、KVエンコーダーからの余分な解析オーバーヘッドを節約することで、LightningのSQLエンコーディングパフォーマンスを50％向上させます[＃145](https://github.com/pingcap/tidb-lightning/pull/145)
    -   ログ形式を[統合ログ形式](https://github.com/tikv/rfcs/blob/master/text/0018-unified-log-format.md)に変更し[＃162](https://github.com/pingcap/tidb-lightning/pull/162)
    -   構成ファイルが欠落している場合に使用するコマンドラインオプションをいくつか追加します[＃157](https://github.com/pingcap/tidb-lightning/pull/157)

-   sync-diff-inspector
    -   チェックポイントをサポートして検証ステータスを記録し、再起動後に最後に保存したポイントから検証を続行します[＃224](https://github.com/pingcap/tidb-tools/pull/224)
    -   チェックサム[＃215](https://github.com/pingcap/tidb-tools/pull/215)を計算してデータの整合性をチェックするには、 `only-use-checksum`の構成アイテムを追加します

## TiDB Ansible {#tidb-ansible}

-   より多くのTiKVモニタリングパネルをサポートし、Ansible、Grafana、およびPrometheus1のバージョンを更新し[＃727](https://github.com/pingcap/tidb-ansible/pull/727)
    -   クラスタステータスを表示するためのサマリーダッシュボード
    -   問題のトラブルシューティングのためのtrouble_shootingダッシュボード
    -   開発者が問題を分析するための詳細ダッシュボード
-   Kafkaバージョン[＃730](https://github.com/pingcap/tidb-ansible/pull/730)のTiDBBinlogのダウンロードエラーの原因となるバグを修正します
-   CentOS 7.0以降、およびRedHat7.0以降としてサポートされているオペレーティングシステムのバージョン制限を変更する[＃733](https://github.com/pingcap/tidb-ansible/pull/733)
-   ローリングアップデート中のバージョン検出モードをマルチコンカレント[＃736](https://github.com/pingcap/tidb-ansible/pull/736)に変更します
-   [＃740](https://github.com/pingcap/tidb-ansible/pull/740)のドキュメントリンクを更新する
-   冗長なTiKV監視メトリックを削除します。トラブルシューティング用の新しいメトリックを追加する[＃735](https://github.com/pingcap/tidb-ansible/pull/735)
-   `table-regions.py`のスクリプトを最適化して、表[＃739](https://github.com/pingcap/tidb-ansible/pull/739)ごとにリーダーの分布を表示します
-   Drainer1の構成ファイルを更新し[＃745](https://github.com/pingcap/tidb-ansible/pull/745)
-   SQLカテゴリごとにレイテンシを表示する新しいパネルでTiDBモニタリングを最適化する[＃747](https://github.com/pingcap/tidb-ansible/pull/747)
-   Lightning構成ファイルを更新し、 `tidb_lightning_ctl`のスクリプトを追加します[＃1e946f8](https://github.com/pingcap/tidb-ansible/commit/1e946f89908e8fd6ef84128c6da3064ddfccf6a8)
