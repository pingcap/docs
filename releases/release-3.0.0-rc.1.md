---
title: TiDB 3.0.0-rc.1 Release Notes
summary: TiDB 3.0.0-rc.1は2019年5月10日にリリースされ、安定性、使いやすさ、機能、SQLオプティマイザ、統計、実行エンジンが改善されました。このリリースには、SQLオプティマイザ、実行エンジン、サーバー、DDL、PD、TiKV、TiDB Binlog、Lightning、sync-diff-inspector、TiDB Ansibleの機能強化が含まれています。主な改善点としては、SQLプラン管理、メモリ使用量の追跡、実行エンジンの制御のサポート、DDLのCREATE TABLE`ステートメントへの`pre_split_regions`オプションの追加などが挙げられます。また、このリリースには、さまざまなバグ修正とパフォーマンスの最適化も含まれています。
---

# TiDB 3.0.0-rc.1 リリースノート {#tidb-3-0-0-rc-1-release-notes}

リリース日：2019年5月10日

TiDB バージョン: 3.0.0-rc.1

TiDB Ansible バージョン: 3.0.0-rc.1

## 概要 {#overview}

2019年5月10日にTiDB 3.0.0-rc.1がリリースされました。対応するTiDB Ansibleバージョンは3.0.0-rc.1です。このリリースでは、TiDB 3.0.0-beta.1と比較して、安定性、使いやすさ、機能、SQLオプティマイザー、統計、実行エンジンが大幅に改善されています。

## TiDB {#tidb}

-   SQLオプティマイザー
    -   列間の順序相関を使用してコスト見積りの精度を向上させます。相関を見積りに直接使用できない場合に、インデックススキャンの優先順位を制御するヒューリスティックパラメータ`tidb_opt_correlation_exp_factor`を導入します[＃9839](https://github.com/pingcap/tidb/pull/9839)
    -   フィルタ[＃10053](https://github.com/pingcap/tidb/pull/10053)に関連する列がある場合、複合インデックスのアクセス条件を抽出するときに、インデックスのプレフィックス列をさらに一致させます。
    -   結合に参加するテーブルの数が`tidb_opt_join_reorder_threshold`未満の場合に、結合操作の実行順序を指定するには、動的プログラミング アルゴリズムを使用します[＃8816](https://github.com/pingcap/tidb/pull/8816)
    -   アクセス条件として複合インデックスを使用する場合、インデックス結合を構築する内部テーブル内のインデックスのプレフィックス列をさらに一致させる[＃8471](https://github.com/pingcap/tidb/pull/8471)
    -   NULL値を持つ単一列インデックスの行数推定の精度を向上[＃9474](https://github.com/pingcap/tidb/pull/9474)
    -   論理最適化フェーズで集計関数を削除するときに、誤った実行を防ぐために`GROUP_CONCAT`特別に処理します[＃9967](https://github.com/pingcap/tidb/pull/9967)
    -   フィルタが定数[＃9848](https://github.com/pingcap/tidb/pull/9848)場合、結合演算子の子ノードにフィルタを適切にプッシュダウンします。
    -   MySQL [＃10064](https://github.com/pingcap/tidb/pull/10064)との非互換性を防ぐために、論理最適化フェーズで列をプルーニングするときに`RAND()`などのいくつかの関数を特別に処理します。
    -   `FAST ANALYZE`サポートします。これは、領域全体をスキャンするのではなく、領域をサンプリングすることで統計収集を高速化します。この機能は変数`tidb_enable_fast_analyze`によって制御されます[＃10258](https://github.com/pingcap/tidb/pull/10258)
    -   SQL文の実行計画のバインドを実行することで実行の安定性を確保するSQL計画管理をサポートします。この機能は現在ベータ版であり、SELECT文のバインド実行計画のみをサポートします。本番環境での使用は推奨されません[＃10284](https://github.com/pingcap/tidb/pull/10284)

-   実行エンジン
    -   3つの演算子`TableReader` `IndexLookupReader` [＃10003](https://github.com/pingcap/tidb/pull/10003)メモリ使用量の追跡と制御をサポートします`IndexReader`
    -   コプロセッサのタスク数、実行時間/待機時間の平均/最長/90%、実行時間または待機時間が最も長い TiKV のアドレスなど、スロー ログ内のコプロセッサ タスクに関する詳細情報の表示をサポートします[＃10165](https://github.com/pingcap/tidb/pull/10165)
    -   プレースホルダなしの準備済みDDL文をサポートする[＃10144](https://github.com/pingcap/tidb/pull/10144)

-   サーバ
    -   TiDB の起動時にのみ DDL 所有者にブートストラップの実行を許可する[＃10029](https://github.com/pingcap/tidb/pull/10029)
    -   トランザクション分離レベルをSERIALIZABLE [＃10065](https://github.com/pingcap/tidb/pull/10065)に設定するときにTiDBがエラーを報告しないようにするために、変数`tidb_skip_isolation_level_check`追加します。
    -   暗黙的なコミット時間とSQL実行時間をスローログ[＃10294](https://github.com/pingcap/tidb/pull/10294)にマージする
        -   SQL ロールのサポート (RBAC権限管理)
        -   サポート`SHOW GRANT` [＃10016](https://github.com/pingcap/tidb/pull/10016)
        -   サポート`SET DEFAULT ROLE` [＃9949](https://github.com/pingcap/tidb/pull/9949)
    -   サポート`GRANT ROLE` [＃9721](https://github.com/pingcap/tidb/pull/9721)
    -   TiDB を終了させる`whitelist`プラグインの`ConnectionEvent`エラーを修正します[＃9889](https://github.com/pingcap/tidb/pull/9889)
    -   トランザクション履歴に読み取り専用ステートメントを誤って追加する問題を修正[＃9723](https://github.com/pingcap/tidb/pull/9723)
    -   `kill`文を改善して SQL 実行を停止し、リソースをより早く解放する[＃9844](https://github.com/pingcap/tidb/pull/9844)
    -   設定ファイル[＃9855](https://github.com/pingcap/tidb/pull/9855)の有効性をチェックするための起動オプション`config-check`を追加する
    -   厳密なSQLモードが無効になっている場合にNULLフィールドを挿入する際の妥当性チェックを修正[＃10161](https://github.com/pingcap/tidb/pull/10161)

-   DDL
    -   `CREATE TABLE`ステートメントに`pre_split_regions`オプションを追加します。このオプションは、テーブルの作成時にテーブルリージョンを事前に分割して、テーブルの作成後に大量の書き込みによって発生する書き込みホットスポットを回避することをサポートします[＃10138](https://github.com/pingcap/tidb/pull/10138)
    -   一部のDDL文の実行パフォーマンスを最適化する[＃10170](https://github.com/pingcap/tidb/pull/10170)
    -   `FULLTEXT KEY` [＃9821](https://github.com/pingcap/tidb/pull/9821)ではフルテキストインデックスがサポートされていないという警告を追加します
    -   TiDB [＃9820](https://github.com/pingcap/tidb/pull/9820)の古いバージョンにおける UTF8 および UTF8MB4 文字セットの互換性の問題を修正しました
    -   表[＃9868](https://github.com/pingcap/tidb/pull/9868)の`shard_row_id_bits`の潜在的なバグを修正
    -   テーブルの文字セットを変更しても列の文字セットが変更されないバグを修正[＃9790](https://github.com/pingcap/tidb/pull/9790)
    -   列のデフォルト値として`BINARY` / `BIT`使用する場合の`SHOW COLUMN`の潜在的なバグを修正[＃9897](https://github.com/pingcap/tidb/pull/9897)
    -   `SHOW FULL COLUMNS`文[＃10007](https://github.com/pingcap/tidb/pull/10007)で`CHARSET` `COLLATION`説明を表示する際の互換性の問題を修正
    -   `SHOW COLLATIONS`文が TiDB [＃10186](https://github.com/pingcap/tidb/pull/10186)でサポートされている照合順序のみをリストする問題を修正しました

## PD {#pd}

-   ETCD [＃1452](https://github.com/pingcap/pd/pull/1452)アップグレード
    -   etcdとPDサーバーのログ形式を統一する
    -   事前投票でLeaderを選出できない問題を修正
    -   後続のリクエストをブロックしないように、失敗する可能性のある「提案」および「読み取り」リクエストを迅速にドロップすることをサポートします。
    -   リースのデッドロック問題を修正
-   ホットストアがキー[＃1487](https://github.com/pingcap/pd/pull/1487)の統計情報を正しく生成しない問題を修正
-   単一のPDノード[＃1485](https://github.com/pingcap/pd/pull/1485)からPDクラスターを強制的に再構築するサポート
-   `regionScatterer`無効な`OperatorStep` [＃1482](https://github.com/pingcap/pd/pull/1482)を生成する可能性がある問題を修正
-   `MergeRegion`オペレータ[＃1495](https://github.com/pingcap/pd/pull/1495)の短すぎるタイムアウト問題を修正
-   ホットリージョンのスケジュールに高い優先度を与えるサポート[＃1492](https://github.com/pingcap/pd/pull/1492)
-   PDサーバー側[＃1502](https://github.com/pingcap/pd/pull/1502)でTSOリクエストの処理時間を記録するためのメトリックを追加します
-   対応する店舗IDと住所を店舗[＃1506](https://github.com/pingcap/pd/pull/1506)に関連する指標に追加します。
-   `GetOperator`サービス[＃1477](https://github.com/pingcap/pd/pull/1477)サポートする
-   ストアが見つからないため、ハートビートストリームでエラーを送信できない問題を修正しました[＃1521](https://github.com/pingcap/pd/pull/1521)

## TiKV {#tikv}

-   エンジン
    -   読み取りトラフィックの統計情報が不正確になる可能性がある問題を修正[＃4436](https://github.com/tikv/tikv/pull/4436)
    -   範囲[＃4503](https://github.com/tikv/tikv/pull/4503)削除するときにプレフィックス抽出プログラムがpanicを起こす可能性がある問題を修正しました
    -   メモリ管理を最適化してメモリ割り当てとコピーを削減`Iterator Key Bound Option` [＃4537](https://github.com/tikv/tikv/pull/4537)
    -   学習者のログギャップを考慮しないと、場合によってはpanicが発生する可能性がある問題を修正しました[＃4559](https://github.com/tikv/tikv/pull/4559)
    -   異なる`column families` [＃4612](https://github.com/tikv/tikv/pull/4612)間での`block cache`共有をサポート

-   サーバ
    -   コンテキストスイッチのオーバーヘッドを`batch commands` [＃4473](https://github.com/tikv/tikv/pull/4473)削減
    -   シークイテレータステータス[＃4470](https://github.com/tikv/tikv/pull/4470)の有効性をチェックする

-   ラフトストア
    -   構成可能な`properties index distance` [＃4517](https://github.com/tikv/tikv/pull/4517)をサポート

-   コプロセッサー
    -   バッチインデックススキャンエグゼキュータ[＃4419](https://github.com/tikv/tikv/pull/4419)を追加
    -   ベクトル化評価フレームワーク[＃4322](https://github.com/tikv/tikv/pull/4322)を追加
    -   バッチエグゼキュータ[＃4433](https://github.com/tikv/tikv/pull/4433)実行サマリーフレームワークの追加
    -   RPN式を構築するときに最大列をチェックして、評価panic[＃4481](https://github.com/tikv/tikv/pull/4481)を引き起こす可能性のある無効な列オフセットを回避します。
    -   `BatchLimitExecutor` [＃4469](https://github.com/tikv/tikv/pull/4469)を加える
    -   ReadPoolの元の`futures-cpupool`を`tokio-threadpool`に置き換えてコンテキストスイッチ[＃4486](https://github.com/tikv/tikv/pull/4486)を減らす
    -   バッチ集計フレームワーク[＃4533](https://github.com/tikv/tikv/pull/4533)を追加
    -   `BatchSelectionExecutor` [＃4562](https://github.com/tikv/tikv/pull/4562)を加える
    -   バッチ攻撃機能の追加`AVG` [＃4570](https://github.com/tikv/tikv/pull/4570)
    -   RPN関数`LogicalAnd` [＃4575](https://github.com/tikv/tikv/pull/4575)を追加

-   その他
    -   メモリアロケータ[＃4370](https://github.com/tikv/tikv/pull/4370)としてのサポート`tcmalloc`

## ツール {#tools}

-   TiDBBinlog
    -   unsigned int 型の主キー列のbinlogデータが負の[＃573](https://github.com/pingcap/tidb-binlog/pull/573)場合にレプリケーションが中止される問題を修正しました。
    -   ダウンストリームが`pb`場合は圧縮オプションを提供しません。ダウンストリーム名を`pb`から`file`に変更します[＃559](https://github.com/pingcap/tidb-binlog/pull/559)
    -   Pumpにローカルstorage[＃509](https://github.com/pingcap/tidb-binlog/pull/509)への非同期フラッシュを許可する`storage.sync-log`設定項目を追加する
    -   PumpとDrainer[＃495](https://github.com/pingcap/tidb-binlog/pull/495)間の通信のトラフィック圧縮をサポート
    -   異なるSQLモード[＃511](https://github.com/pingcap/tidb-binlog/pull/511)でのDDLクエリの解析をサポートするために、 Drainerに`syncer.sql-mode`構成項目を追加します。
    -   レプリケーションを必要としないテーブルを除外するための構成項目を`syncer.ignore-table`追加します[＃520](https://github.com/pingcap/tidb-binlog/pull/520)

-   稲妻
    -   行IDまたはデフォルトの列値を使用して、ダンプファイル[＃170](https://github.com/pingcap/tidb-lightning/pull/170)で欠落した列データを入力します。
    -   SST の一部がインポートに失敗した場合でも、インポート成功が返される可能性があるインポーターのバグを修正しました[＃4566](https://github.com/tikv/tikv/pull/4566)
    -   SST を TiKV [＃4412](https://github.com/tikv/tikv/pull/4412)にアップロードする際のインポーターの速度制限をサポート
    -   大きなテーブルに対するチェックサムと分析によるクラスターへの影響を軽減し、チェックサムと分析[＃156](https://github.com/pingcap/tidb-lightning/pull/156)成功率を向上させるために、サイズによるテーブルインポートをサポートします。
    -   データソースファイルをTiDBのtypes.Datumとして直接解析し、KVエンコーダ[＃145](https://github.com/pingcap/tidb-lightning/pull/145)からの余分な解析オーバーヘッドを削減することで、LightningのSQLエンコードパフォーマンスを50％向上しました。
    -   ログ形式を[統合ログ形式](https://github.com/tikv/rfcs/blob/master/text/0018-unified-log-format.md) [＃162](https://github.com/pingcap/tidb-lightning/pull/162)に変更
    -   設定ファイルが見つからない場合に使用するコマンドラインオプションをいくつか追加します[＃157](https://github.com/pingcap/tidb-lightning/pull/157)

-   同期差分インスペクター
    -   チェックポイントをサポートし、検証ステータスを記録し、再起動後に最後に保存したポイントから検証を続行します[＃224](https://github.com/pingcap/tidb-tools/pull/224)
    -   チェックサム[＃215](https://github.com/pingcap/tidb-tools/pull/215)計算してデータの整合性をチェックするための構成項目`only-use-checksum`追加します

## TiDB アンシブル {#tidb-ansible}

-   より多くの TiKV 監視パネルをサポートし、Ansible、Grafana、Prometheus [＃727](https://github.com/pingcap/tidb-ansible/pull/727)のバージョンを更新しました。
    -   クラスターのステータスを表示するサマリーダッシュボード
    -   問題のトラブルシューティングのためのトラブルシューティングダッシュボード
    -   開発者が問題を分析するための詳細ダッシュボード
-   Kafka バージョン[＃730](https://github.com/pingcap/tidb-ansible/pull/730)の TiDB Binlogのダウンロードに失敗するバグを修正しました
-   CentOS 7.0以降、Red Hat 7.0以降などのサポート対象オペレーティングシステムのバージョン制限を変更します[＃733](https://github.com/pingcap/tidb-ansible/pull/733)
-   ローリングアップデート中のバージョン検出モードをマルチ同時実行[＃736](https://github.com/pingcap/tidb-ansible/pull/736)に変更
-   README [＃740](https://github.com/pingcap/tidb-ansible/pull/740)のドキュメントリンクを更新
-   冗長な TiKV 監視メトリックを削除し、トラブルシューティング用の新しいメトリックを追加します[＃735](https://github.com/pingcap/tidb-ansible/pull/735)
-   `table-regions.py`スクリプトを最適化して、表[＃739](https://github.com/pingcap/tidb-ansible/pull/739)のリーダー分布を表示する
-   Drainer [＃745](https://github.com/pingcap/tidb-ansible/pull/745)の設定ファイルを更新します
-   SQL カテゴリ別にレイテンシを表示する新しいパネルで TiDB モニタリングを最適化[＃747](https://github.com/pingcap/tidb-ansible/pull/747)
-   Lightning設定ファイルを更新し、 `tidb_lightning_ctl`スクリプト[#1e946f8](https://github.com/pingcap/tidb-ansible/commit/1e946f89908e8fd6ef84128c6da3064ddfccf6a8)追加します。
