---
title: TiDB 3.0.3 Release Notes
---

# TiDB 3.0.3 リリースノート {#tidb-3-0-3-release-notes}

発売日：2019年8月29日

TiDB バージョン: 3.0.3

TiDB Ansible バージョン: 3.0.3

## TiDB {#tidb}

-   SQLオプティマイザー
    -   `opt_rule_blacklist`テーブルを追加して、 `aggregation_eliminate`や`column_prune`などのロジック最適化ルールを無効にします[#11658](https://github.com/pingcap/tidb/pull/11658)
    -   結合キーでプレフィックス インデックスまたは負の値[#11759](https://github.com/pingcap/tidb/pull/11759)に等しい符号なしインデックス列が使用されている場合、 `Index Join`に対して誤った結果が返される可能性がある問題を修正します。
    -   `create … binding ...`の`SELECT`ステートメントの`”`または`\`で解析エラーが発生する可能性がある問題を修正[#11726](https://github.com/pingcap/tidb/pull/11726)
-   SQL実行エンジン
    -   Quote関数がnull値を扱う場合に戻り値の型エラーが発生することがある問題を修正[#11619](https://github.com/pingcap/tidb/pull/11619)
    -   `NotNullFlag` [#11641](https://github.com/pingcap/tidb/pull/11641)保持した状態で型推論に Max/Min を使用すると、 `ifnull`に対して誤った結果が返される可能性がある問題を修正
    -   文字列形式[#11660](https://github.com/pingcap/tidb/pull/11660)のビット型データを比較するときに発生する潜在的なエラーを修正しました。
    -   OOM [#11679](https://github.com/pingcap/tidb/pull/11679)の可能性を下げるために、シーケンシャル読み取りを必要とするデータの同時実行性を減らします。
    -   一部の組み込み関数( `if`と`coalesce`など) で複数のパラメーターが署名されていない場合に、誤った型推論が発生する可能性がある問題を修正します[#11621](https://github.com/pingcap/tidb/pull/11621)
    -   `Div`関数が符号なし 10 進数型を処理する場合の MySQL との非互換性を修正します[#11813](https://github.com/pingcap/tidb/pull/11813)
    -   Pump/Drainer[#11827](https://github.com/pingcap/tidb/pull/11827)の状態を変更するSQL実行時にpanicが発生する場合がある問題を修正
    -   Autocommit = 1 で`begin`ステートメントが存在しない場合、 `select ... for update`でpanicが発生することがある問題を修正[#11736](https://github.com/pingcap/tidb/pull/11736)
    -   `set default role`ステートメントの実行時に発生する可能性がある権限チェック エラーを修正[#11777](https://github.com/pingcap/tidb/pull/11777)
    -   `create user`または`drop user`を実行した際にパーミッションチェックエラーが発生することがある問題を修正[#11814](https://github.com/pingcap/tidb/pull/11814)
    -   `select ... for update`ステートメントが`PointGetExecutor`関数に構築されるときに自動再試行される可能性がある問題を修正します。 [#11718](https://github.com/pingcap/tidb/pull/11718)
    -   Window 関数がパーティション[#11825](https://github.com/pingcap/tidb/pull/11825)を処理するときに発生する可能性がある境界エラーを修正しました。
    -   不正な形式の引数[#11893](https://github.com/pingcap/tidb/pull/11893)を処理するときに`time`関数で EOF エラーが発生する問題を修正します。
    -   Window 関数が渡されたパラメータをチェックしない問題を修正します[#11705](https://github.com/pingcap/tidb/pull/11705)
    -   `Explain`で表示される計画結果と実際に実行された計画[#11186](https://github.com/pingcap/tidb/pull/11186)が一致しない問題を修正
    -   Window 関数によって参照されるメモリが重複すると、クラッシュまたは不正な結果が発生する可能性がある問題を修正します[#11823](https://github.com/pingcap/tidb/pull/11823)
    -   遅いログ[#11887](https://github.com/pingcap/tidb/pull/11887)の`Succ`フィールドの誤った情報を更新します。
-   サーバ
    -   `tidb_back_off_wexight`変数の名前を`tidb_backoff_weight` [#11665](https://github.com/pingcap/tidb/pull/11665)に変更します。
    -   現在の TiDB と互換性のある TiKV の最小バージョンを v3.0.0 に更新します[#11618](https://github.com/pingcap/tidb/pull/11618)
    -   テスト内のスイートが正しく使用されていることを確認するためのサポート`make testSuite` [#11685](https://github.com/pingcap/tidb/pull/11685)
-   DDL
    -   複数のパーティションの削除中にパーティション タイプを変更するステートメントなど、サポートされていないパーティション関連の DDL ステートメントの実行をスキップします[#11373](https://github.com/pingcap/tidb/pull/11373)
    -   生成されたカラムをその依存列の前に配置することを禁止します[#11686](https://github.com/pingcap/tidb/pull/11686)
    -   デフォルト値の`tidb_ddl_reorg_worker_cnt`と`tidb_ddl_reorg_batch_size`を変更します[#11874](https://github.com/pingcap/tidb/pull/11874)
-   モニター
    -   新しいバックオフ監視タイプを追加して、各バックオフ タイプの継続時間を記録します。コミット バックオフ[#11728](https://github.com/pingcap/tidb/pull/11728)など、以前はカウントされていなかったタイプをカバーするバックオフ メトリックをさらに追加します。

## TiKV {#tikv}

-   コンテキスト[#5256](https://github.com/tikv/tikv/pull/5256)の重複によりReadIndex がリクエストに応答できない可能性がある問題を修正します。
-   時期尚早な`PutStore` [#5277](https://github.com/tikv/tikv/pull/5277)によって引き起こされる潜在的なスケジューリングのジッターを修正
-   リージョンハートビート[#5296](https://github.com/tikv/tikv/pull/5296)から報告される誤ったタイムスタンプを修正
-   コア ダンプから共有ブロックキャッシュを除外して、コア ダンプのサイズを削減します[#5322](https://github.com/tikv/tikv/pull/5322)
-   リージョンのマージ[#5291](https://github.com/tikv/tikv/pull/5291)中に発生する可能性のある TiKV パニックを修正
-   デッドロック検出器[#5317](https://github.com/tikv/tikv/pull/5317)のリーダー変更チェックを高速化
-   `grpc env`を使用したデッドロック クライアントの作成のサポート[#5346](https://github.com/tikv/tikv/pull/5346)
-   設定が正しいかどうかを確認するには`config-check`を追加します[#5349](https://github.com/tikv/tikv/pull/5349)
-   リーダー[#5351](https://github.com/tikv/tikv/pull/5351)がない場合にReadIndexが何も返さない問題を修正

## PD {#pd}

-   `pdctl` [#1685](https://github.com/pingcap/pd/pull/1685)の成功メッセージを返す

## ツール {#tools}

-   TiDBBinlog
    -   Drainerのデフォルト値`defaultBinlogItemCount`を 65536 から 512 に変更して、 Drainer起動時の OOM の可能性を減らします[#721](https://github.com/pingcap/tidb-binlog/pull/721)
    -   ポンプサーバーのオフライン ロジックを最適化して、潜在的なオフラインの輻輳を回避します[#701](https://github.com/pingcap/tidb-binlog/pull/701)
-   TiDB Lightning:
    -   [#225](https://github.com/pingcap/tidb-lightning/pull/225)をインポートするときに、デフォルトでシステム データベース`mysql` 、 `information_schema` 、 `performance_schema` 、および`sys`をスキップします。

## TiDB Ansible {#tidb-ansible}

-   ローリング アップデートの PD 操作を最適化して安定性を向上[#894](https://github.com/pingcap/tidb-ansible/pull/894)
-   現在の Grafana バージョン[#892](https://github.com/pingcap/tidb-ansible/pull/892)でサポートされていない Grafana Collector コンポーネントを削除します。
-   TiKV アラート ルールの更新[#898](https://github.com/pingcap/tidb-ansible/pull/898)
-   生成された TiKV 構成に`pessimistic-txn`パラメータ[#911](https://github.com/pingcap/tidb-ansible/pull/911)が欠落している問題を修正
-   Spark を V2.4.3 に更新し、TiSpark を Spark V2.4.3 と互換性[#918](https://github.com/pingcap/tidb-ansible/pull/918)ある V2.1.4 に更新します[#913](https://github.com/pingcap/tidb-ansible/pull/913)
