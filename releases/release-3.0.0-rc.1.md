---
title: TiDB 3.0.0-rc.1 Release Notes
---

# TiDB 3.0.0-rc.1 リリースノート {#tidb-3-0-0-rc-1-release-notes}

リリース日：2019年5月10日

TiDB バージョン: 3.0.0-rc.1

TiDB アンシブル バージョン: 3.0.0-rc.1

## 概要 {#overview}

2019 年 5 月 10 日に、TiDB 3.0.0-rc.1 がリリースされました。対応する TiDB Ansible のバージョンは 3.0.0-rc.1 です。 TiDB 3.0.0-beta.1 と比較して、このリリースでは、安定性、使いやすさ、機能、SQL オプティマイザー、統計、および実行エンジンが大幅に改善されています。

## TiDB {#tidb}

-   SQL オプティマイザー
    -   列間の順序相関を使用してコスト見積もりの精度を向上させます。ヒューリスティック パラメータ`tidb_opt_correlation_exp_factor`を導入して、推定に相関を直接使用できないシナリオのインデックス スキャンの設定を制御します。 [#9839](https://github.com/pingcap/tidb/pull/9839)
    -   複合インデックスのアクセス条件を抽出する際に、フィルター[#10053](https://github.com/pingcap/tidb/pull/10053)に該当する列がある場合は、より多くのインデックスのプレフィックス列に一致します
    -   動的計画法アルゴリズムを使用して、結合に参加するテーブルの数が値`tidb_opt_join_reorder_threshold`未満の場合の結合操作の実行順序を指定します。 [#8816](https://github.com/pingcap/tidb/pull/8816)
    -   アクセス条件[#8471](https://github.com/pingcap/tidb/pull/8471)として複合インデックスを使用する場合、インデクス結合を構築する内部表のインデクスのプレフィクス列をより多く一致させます。
    -   NULL 値を持つ単一列インデックスの行数推定の精度を向上させます[#9474](https://github.com/pingcap/tidb/pull/9474)
    -   論理最適化フェーズで集計関数を削除する場合は、特別に`GROUP_CONCAT`処理して、誤った実行を防止します[#9967](https://github.com/pingcap/tidb/pull/9967)
    -   フィルターが定数[#9848](https://github.com/pingcap/tidb/pull/9848)の場合、フィルターを結合演算子の子ノードに適切にプッシュします。
    -   MySQL [#10064](https://github.com/pingcap/tidb/pull/10064)の非互換性を防ぐために、論理最適化フェーズで列をプルーニングするときに`RAND()`などの一部の関数を特別に処理します。
    -   サポート`FAST ANALYZE` 。領域全体をスキャンするのではなく、領域をサンプリングすることで統計収集を高速化します。この機能は、変数`tidb_enable_fast_analyze`によって制御されます。 [#10258](https://github.com/pingcap/tidb/pull/10258)
    -   SQL文の実行計画のバインドを行うことで実行の安定性を確保するSQL計画管理をサポートします。この機能は現在ベータ版であり、SELECT ステートメントのバインドされた実行プランのみをサポートしています。本番環境で使用することはお勧めしません。 [#10284](https://github.com/pingcap/tidb/pull/10284)

-   実行エンジン
    -   `TableReader` 、 `IndexReader`および`IndexLookupReader` [#10003](https://github.com/pingcap/tidb/pull/10003)の 3 つの演算子でのメモリ使用量の追跡と制御をサポートします。
    -   コプロセッサー内のタスクの数、平均/最長/90% の実行/待機時間、および最長の実行時間または待機時間を要した TiKV のアドレスなど、スローログ内のコプロセッサータスクに関する詳細情報の表示をサポート[#10165](https://github.com/pingcap/tidb/pull/10165)
    -   プレースホルダーのない準備済み DDL ステートメントのサポート[#10144](https://github.com/pingcap/tidb/pull/10144)

-   サーバ
    -   TiDB の起動時に DDL 所有者のみがブートストラップを実行できるようにする[#10029](https://github.com/pingcap/tidb/pull/10029)
    -   変数`tidb_skip_isolation_level_check`を追加して、トランザクション分離レベルをSERIALIZABLE [#10065](https://github.com/pingcap/tidb/pull/10065)に設定するときに TiDB がエラーを報告しないようにします。
    -   暗黙的なコミット時間とスロー ログ[#10294](https://github.com/pingcap/tidb/pull/10294)の SQL 実行時間をマージします。
        -   SQL ロールのサポート (RBAC権限管理)
        -   サポート`SHOW GRANT` [#10016](https://github.com/pingcap/tidb/pull/10016)
        -   サポート`SET DEFAULT ROLE` [#9949](https://github.com/pingcap/tidb/pull/9949)
    -   サポート`GRANT ROLE` [#9721](https://github.com/pingcap/tidb/pull/9721)
    -   TiDB を終了させる`whitelist`プラグインからの`ConnectionEvent`エラーを修正します[#9889](https://github.com/pingcap/tidb/pull/9889)
    -   読み取り専用ステートメントをトランザクション履歴に誤って追加する問題を修正します[#9723](https://github.com/pingcap/tidb/pull/9723)
    -   `kill`ステートメントを改善して、SQL の実行を停止し、リソースをより迅速に解放します[#9844](https://github.com/pingcap/tidb/pull/9844)
    -   起動オプションを追加する`config-check`設定ファイルの有効性をチェックする[#9855](https://github.com/pingcap/tidb/pull/9855)
    -   厳密な SQL モードが無効になっている場合の NULL フィールドの挿入の有効性チェックを修正します[#10161](https://github.com/pingcap/tidb/pull/10161)

-   DDL
    -   `CREATE TABLE`ステートメントに`pre_split_regions`オプションを追加します。このオプションは、テーブル作成後の大量の書き込みによって発生する書き込みホット スポットを回避するために、テーブル作成時にテーブル リージョンの事前リージョンをサポートします[#10138](https://github.com/pingcap/tidb/pull/10138)
    -   一部の DDL ステートメントの実行パフォーマンスを最適化する[#10170](https://github.com/pingcap/tidb/pull/10170)
    -   `FULLTEXT KEY` [#9821](https://github.com/pingcap/tidb/pull/9821)ではフルテキスト インデックスがサポートされていないという警告を追加します。
    -   古いバージョンの TiDB [#9820](https://github.com/pingcap/tidb/pull/9820)での UTF8 および UTF8MB4 文字セットの互換性の問題を修正します。
    -   表[#9868](https://github.com/pingcap/tidb/pull/9868)の`shard_row_id_bits`の潜在的なバグを修正
    -   テーブルの文字セットを変更した後、列の文字セットが変更されないバグを修正[#9790](https://github.com/pingcap/tidb/pull/9790)
    -   列のデフォルト値[#9897](https://github.com/pingcap/tidb/pull/9897)として`BINARY` / `BIT`を使用する場合の`SHOW COLUMN`の潜在的なバグを修正します
    -   `SHOW FULL COLUMNS`ステートメント[#10007](https://github.com/pingcap/tidb/pull/10007)で`CHARSET` / `COLLATION`の説明を表示する際の互換性の問題を修正します。
    -   `SHOW COLLATIONS`ステートメントが TiDB [#10186](https://github.com/pingcap/tidb/pull/10186)でサポートされている照合のみをリストする問題を修正します。

## PD {#pd}

-   ETCD [#1452](https://github.com/pingcap/pd/pull/1452)のアップグレード
    -   etcdとPDサーバーのログフォーマットを統一
    -   PreVote によるLeaderの選出に失敗する問題を修正
    -   後続のリクエストのブロックを回避するために、失敗する「提案」および「読み取り」リクエストの迅速なドロップをサポートします
    -   Lease のデッドロックの問題を修正
-   ホット ストアでキーの統計が正しくない問題を修正します[#1487](https://github.com/pingcap/pd/pull/1487)
-   単一の PD ノードから PD クラスターを強制的に再構築するサポート[#1485](https://github.com/pingcap/pd/pull/1485)
-   `regionScatterer`が無効な`OperatorStep` [#1482](https://github.com/pingcap/pd/pull/1482)を生成する可能性がある問題を修正
-   `MergeRegion`オペレーター[#1495](https://github.com/pingcap/pd/pull/1495)のタイムアウトが短すぎる問題を修正
-   ホット リージョン スケジューリングを優先するサポート[#1492](https://github.com/pingcap/pd/pull/1492)
-   PDサーバー側での TSO 要求の処理時間を記録するためのメトリックを追加します[#1502](https://github.com/pingcap/pd/pull/1502)
-   対応する店舗 ID と住所を、店舗に関連するメトリクスに追加します[#1506](https://github.com/pingcap/pd/pull/1506)
-   `GetOperator`サービス[#1477](https://github.com/pingcap/pd/pull/1477)をサポート
-   ストアが見つからないため、Heartbeat ストリームでエラーを送信できない問題を修正します[#1521](https://github.com/pingcap/pd/pull/1521)

## TiKV {#tikv}

-   エンジン
    -   読み取りトラフィックの統計が正しくない可能性がある問題を修正します[#4436](https://github.com/tikv/tikv/pull/4436)
    -   範囲[#4503](https://github.com/tikv/tikv/pull/4503)を削除するときにプレフィックス エクストラクターpanicを引き起こす可能性がある問題を修正します。
    -   メモリ管理を最適化して、 `Iterator Key Bound Option` [#4537](https://github.com/tikv/tikv/pull/4537)のメモリ割り当てとコピーを減らす
    -   学習者のログ ギャップを考慮しないと、場合によってはpanic[#4559](https://github.com/tikv/tikv/pull/4559)が発生する可能性がある問題を修正します。
    -   異なる`column families` [#4612](https://github.com/tikv/tikv/pull/4612)の間で`block cache`共有をサポート

-   サーバ
    -   コンテキスト スイッチのオーバーヘッドを`batch commands` [#4473](https://github.com/tikv/tikv/pull/4473)削減
    -   シーク イテレータ ステータス[#4470](https://github.com/tikv/tikv/pull/4470)の有効性を確認する

-   ラフトストア
    -   設定可能なサポート`properties index distance` [#4517](https://github.com/tikv/tikv/pull/4517)

-   コプロセッサー
    -   バッチ インデックス スキャン エグゼキューター[#4419](https://github.com/tikv/tikv/pull/4419)の追加
    -   ベクトル化された評価フレームワーク[#4322](https://github.com/tikv/tikv/pull/4322)を追加
    -   バッチ executor [#4433](https://github.com/tikv/tikv/pull/4433)の実行概要フレームワークを追加します。
    -   評価panicを引き起こす可能性のある無効な列オフセットを回避するために、RPN 式を作成するときに最大列を確認してください[#4481](https://github.com/tikv/tikv/pull/4481)
    -   `BatchLimitExecutor` [#4469](https://github.com/tikv/tikv/pull/4469)を追加
    -   ReadPool の元の`futures-cpupool` `tokio-threadpool`に置き換えて、コンテキスト スイッチ[#4486](https://github.com/tikv/tikv/pull/4486)を減らします。
    -   バッチ集計フレームワーク[#4533](https://github.com/tikv/tikv/pull/4533)を追加する
    -   `BatchSelectionExecutor` [#4562](https://github.com/tikv/tikv/pull/4562)を追加
    -   一括攻撃機能追加`AVG` [#4570](https://github.com/tikv/tikv/pull/4570)
    -   RPN機能追加`LogicalAnd` [#4575](https://github.com/tikv/tikv/pull/4575)

-   その他
    -   メモリアロケータとして`tcmalloc`サポート[#4370](https://github.com/tikv/tikv/pull/4370)

## ツール {#tools}

-   TiDBBinlog
    -   unsigned int 型の主キー列のbinlogデータが負の[#573](https://github.com/pingcap/tidb-binlog/pull/573)の場合、レプリケーションが中止される問題を修正します。
    -   ダウンストリームが`pb`の場合、圧縮オプションを提供しません。下流の名前を`pb`から`file` [#559](https://github.com/pingcap/tidb-binlog/pull/559)に変更します
    -   ローカルstorage[#509](https://github.com/pingcap/tidb-binlog/pull/509)での非同期フラッシュを可能にする`storage.sync-log`構成項目をPumpに追加します。
    -   PumpとDrainer [#495](https://github.com/pingcap/tidb-binlog/pull/495)間の通信のトラフィック圧縮をサポート
    -   異なる sql-mode [#511](https://github.com/pingcap/tidb-binlog/pull/511)での DDL クエリの解析をサポートするために、 Drainerに`syncer.sql-mode`構成項目を追加します。
    -   `syncer.ignore-table`構成項目を追加して、レプリケーションを必要としないテーブルの除外をサポートします[#520](https://github.com/pingcap/tidb-binlog/pull/520)

-   雷
    -   行 ID またはデフォルトの列値を使用して、ダンプ ファイルに含まれていない列データを入力します[#170](https://github.com/pingcap/tidb-lightning/pull/170)
    -   SST の一部のインポートに失敗した場合でも、インポートの成功が返される可能性があるというインポーターのバグを修正します[#4566](https://github.com/tikv/tikv/pull/4566)
    -   SST を TiKV [#4412](https://github.com/tikv/tikv/pull/4412)にアップロードする際の Importer での速度制限のサポート
    -   サイズごとのテーブルのインポートをサポートして、大きなテーブルのチェックサムと分析によってもたらされるクラスターへの影響を軽減し、チェックサムと分析[#156](https://github.com/pingcap/tidb-lightning/pull/156)の成功率を向上させます
    -   データ ソース ファイルをタイプとして直接解析することで、Lightning の SQL エンコーディングのパフォーマンスを 50% 向上させます[#145](https://github.com/pingcap/tidb-lightning/pull/145)
    -   ログ形式を[統合ログ形式](https://github.com/tikv/rfcs/blob/master/text/0018-unified-log-format.md) [#162](https://github.com/pingcap/tidb-lightning/pull/162)に変更
    -   構成ファイルが見つからない場合に使用するコマンド ライン オプションをいくつか追加します[#157](https://github.com/pingcap/tidb-lightning/pull/157)

-   同期差分インスペクター
    -   チェックポイントをサポートして検証ステータスを記録し、再起動後に最後に保存されたポイントから検証を続行します[#224](https://github.com/pingcap/tidb-tools/pull/224)
    -   チェックサム[#215](https://github.com/pingcap/tidb-tools/pull/215)を計算してデータの整合性をチェックするための`only-use-checksum`構成アイテムを追加します。

## TiDB アンシブル {#tidb-ansible}

-   より多くの TiKV 監視パネルをサポートし、Ansible、Grafana、Prometheus [#727](https://github.com/pingcap/tidb-ansible/pull/727)のバージョンを更新
    -   クラスターのステータスを表示するための概要ダッシュボード
    -   問題をトラブルシューティングするための trouble_shooting ダッシュボード
    -   開発者が問題を分析するための詳細ダッシュボード
-   Kafka バージョン[#730](https://github.com/pingcap/tidb-ansible/pull/730)の TiDB Binlogのダウンロードに失敗するバグを修正
-   CentOS 7.0 以降、および Red Hat 7.0 以降[#733](https://github.com/pingcap/tidb-ansible/pull/733)としてサポートされているオペレーティング システムのバージョン制限を変更します。
-   ローリング更新中のバージョン検出モードをマルチコンカレント[#736](https://github.com/pingcap/tidb-ansible/pull/736)に変更する
-   README [#740](https://github.com/pingcap/tidb-ansible/pull/740)のドキュメント リンクを更新
-   冗長な TiKV モニタリング メトリックを削除します。トラブルシューティング用の新しいメトリックを追加します[#735](https://github.com/pingcap/tidb-ansible/pull/735)
-   `table-regions.py`スクリプトを最適化して、表[#739](https://github.com/pingcap/tidb-ansible/pull/739)ごとにリーダーの分布を表示します
-   Drainer [#745](https://github.com/pingcap/tidb-ansible/pull/745)の構成ファイルを更新する
-   SQL カテゴリ別にレイテンシを表示する新しいパネルで TiDB 監視を最適化します[#747](https://github.com/pingcap/tidb-ansible/pull/747)
-   Lightning 構成ファイルを更新し、 `tidb_lightning_ctl`スクリプト[#1e946f8](https://github.com/pingcap/tidb-ansible/commit/1e946f89908e8fd6ef84128c6da3064ddfccf6a8)を追加します。
