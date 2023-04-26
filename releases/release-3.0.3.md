---
title: TiDB 3.0.3 Release Notes
---

# TiDB 3.0.3 リリースノート {#tidb-3-0-3-release-notes}

発売日：2019年8月29日

TiDB バージョン: 3.0.3

TiDB アンシブル バージョン: 3.0.3

## TiDB {#tidb}

-   SQL オプティマイザー
    -   `opt_rule_blacklist`テーブルを追加して、 `aggregation_eliminate`や`column_prune` [#11658](https://github.com/pingcap/tidb/pull/11658)などのロジック最適化ルールを無効にします。
    -   結合キーがプレフィックス インデックスまたは負の値[#11759](https://github.com/pingcap/tidb/pull/11759)に等しい符号なしインデックス カラムを使用する場合、 `Index Join`に対して誤った結果が返される可能性がある問題を修正します。
    -   `create … binding ...`の`SELECT`のステートメントの`”`または`\`解析エラーになる可能性がある問題を修正します[#11726](https://github.com/pingcap/tidb/pull/11726)
-   SQL 実行エンジン
    -   Quote関数でnull値を扱う際に戻り値に型エラーが発生することがある問題を修正[#11619](https://github.com/pingcap/tidb/pull/11619)
    -   Max/Min を使用して`NotNullFlag`保持[#11641](https://github.com/pingcap/tidb/pull/11641)の型推論を行うと、 `ifnull`に対して誤った結果が返されることがある問題を修正します。
    -   文字列形式[#11660](https://github.com/pingcap/tidb/pull/11660)のビット型データを比較するときに発生する潜在的なエラーを修正します。
    -   OOM [#11679](https://github.com/pingcap/tidb/pull/11679)の可能性を下げるために、シーケンシャル読み取りが必要なデータの同時実行数を減らします
    -   一部の組み込み関数 (たとえば、 `if`および`coalesce` ) で複数のパラメーターが符号なしの場合、誤った型関数が発生する可能性がある問題を修正します[#11621](https://github.com/pingcap/tidb/pull/11621)
    -   `Div`関数が符号なし 10 進数型を処理する場合の MySQL との非互換性を修正します[#11813](https://github.com/pingcap/tidb/pull/11813)
    -   Pump/ Drainer [#11827](https://github.com/pingcap/tidb/pull/11827)のステータスを変更する SQL ステートメントを実行すると、panicが発生することがある問題を修正します。
    -   Autocommit = 1 で`begin`ステートメントがない場合、 `select ... for update`に対してpanicが発生する可能性がある問題を修正[#11736](https://github.com/pingcap/tidb/pull/11736)
    -   `set default role`ステートメントの実行時に発生する可能性があるパーミッション チェック エラーを修正します[#11777](https://github.com/pingcap/tidb/pull/11777)
    -   `create user`または`drop user`を実行した際に発生する可能性があったパーミッションチェックエラーを修正[#11814](https://github.com/pingcap/tidb/pull/11814)
    -   `select ... for update`ステートメントが`PointGetExecutor`関数[#11718](https://github.com/pingcap/tidb/pull/11718)に構築されると、自動的に再試行される可能性がある問題を修正します。
    -   Window 関数がパーティション[#11825](https://github.com/pingcap/tidb/pull/11825)を処理するときに発生する可能性がある境界エラーを修正します。
    -   `time`関数が不適切な形式の引数を処理すると EOF エラーが発生する問題を修正します[#11893](https://github.com/pingcap/tidb/pull/11893)
    -   Window 関数が渡されたパラメーターをチェックしない問題を修正します[#11705](https://github.com/pingcap/tidb/pull/11705)
    -   `Explain`で表示した計画結果と実際に実行した計画が一致しない問題を修正[#11186](https://github.com/pingcap/tidb/pull/11186)
    -   Window 関数によって参照されるメモリが重複すると、クラッシュまたは誤った結果が生じる可能性があるという問題を修正します[#11823](https://github.com/pingcap/tidb/pull/11823)
    -   スローログの`Succ`フィールドの誤った情報を更新します[#11887](https://github.com/pingcap/tidb/pull/11887)
-   サーバ
    -   `tidb_back_off_wexight`変数の名前を`tidb_backoff_weight` [#11665](https://github.com/pingcap/tidb/pull/11665)に変更します
    -   現在の TiDB と互換性のある TiKV の最小バージョンを v3.0.0 に更新します[#11618](https://github.com/pingcap/tidb/pull/11618)
    -   サポート`make testSuite`テストのスイートが正しく使用されていることを確認する[#11685](https://github.com/pingcap/tidb/pull/11685)
-   DDL
    -   複数のパーティションの削除中にパーティション タイプを変更するステートメントを含む、サポートされていないパーティション関連の DDL ステートメントの実行をスキップする[#11373](https://github.com/pingcap/tidb/pull/11373)
    -   依存列の前に生成カラムを配置することを禁止する[#11686](https://github.com/pingcap/tidb/pull/11686)
    -   デフォルト値の`tidb_ddl_reorg_worker_cnt`と`tidb_ddl_reorg_batch_size`を変更します[#11874](https://github.com/pingcap/tidb/pull/11874)
-   モニター
    -   新しいバックオフ監視タイプを追加して、各バックオフ タイプの期間を記録します。コミット バックオフ[#11728](https://github.com/pingcap/tidb/pull/11728)など、以前は数えられなかったタイプをカバーするバックオフ メトリックを追加します。

## TiKV {#tikv}

-   コンテキストが重複しているため、 ReadIndex が要求に応答しない場合がある問題を修正します[#5256](https://github.com/tikv/tikv/pull/5256)
-   時期尚早によって引き起こされる可能性のあるスケジューリング ジッタを修正します`PutStore` [#5277](https://github.com/tikv/tikv/pull/5277)
-   リージョンハートビートから報告された誤ったタイムスタンプを修正します[#5296](https://github.com/tikv/tikv/pull/5296)
-   コア ダンプから共有ブロックキャッシュを除外して、コア ダンプのサイズを縮小します[#5322](https://github.com/tikv/tikv/pull/5322)
-   リージョンのマージ中の潜在的な TiKV パニックを修正[#5291](https://github.com/tikv/tikv/pull/5291)
-   デッドロック検出器[#5317](https://github.com/tikv/tikv/pull/5317)のリーダー変更チェックの高速化
-   `grpc env`を使用したデッドロック クライアントの作成のサポート[#5346](https://github.com/tikv/tikv/pull/5346)
-   `config-check`を追加して、構成が正しいかどうかを確認します[#5349](https://github.com/tikv/tikv/pull/5349)
-   リーダーがない場合、 ReadIndex が何も返さない問題を修正します[#5351](https://github.com/tikv/tikv/pull/5351)

## PD {#pd}

-   `pdctl` [#1685](https://github.com/pingcap/pd/pull/1685)の成功メッセージを返す

## ツール {#tools}

-   TiDBBinlog
    -   Drainerのデフォルト値`defaultBinlogItemCount`を 65536 から 512 に変更して、 Drainer の起動時の OOM の可能性を減らします[#721](https://github.com/pingcap/tidb-binlog/pull/721)
    -   潜在的なオフラインの輻輳を回避するために、ポンプサーバーのオフライン ロジックを最適化します[#701](https://github.com/pingcap/tidb-binlog/pull/701)
-   TiDB Lightning:
    -   [#225](https://github.com/pingcap/tidb-lightning/pull/225)をインポートするときに、デフォルトでシステム データベース`mysql` 、 `information_schema` 、 `performance_schema` 、および`sys`をスキップします。

## TiDB アンシブル {#tidb-ansible}

-   PD 操作をローリング アップデート用に最適化して安定性を向上させる[#894](https://github.com/pingcap/tidb-ansible/pull/894)
-   現在の Grafana バージョン[#892](https://github.com/pingcap/tidb-ansible/pull/892)でサポートされていない Grafana Collector コンポーネントを削除します
-   TiKV アラート ルールの更新[#898](https://github.com/pingcap/tidb-ansible/pull/898)
-   生成された TiKV 構成で`pessimistic-txn`パラメーター[#911](https://github.com/pingcap/tidb-ansible/pull/911)が欠落している問題を修正
-   Spark を V2.4.3 にアップデートし、TiSpark を Spark V2.4.3 と互換性のある V2.1.4 にアップデートします[#913](https://github.com/pingcap/tidb-ansible/pull/913) , [#918](https://github.com/pingcap/tidb-ansible/pull/918)
