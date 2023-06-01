---
title: TiDB 3.0.3 Release Notes
---

# TiDB 3.0.3 リリースノート {#tidb-3-0-3-release-notes}

発売日：2019年8月29日

TiDB バージョン: 3.0.3

TiDB Ansible バージョン: 3.0.3

## TiDB {#tidb}

-   SQLオプティマイザー
    -   `opt_rule_blacklist`テーブルを追加して、 `aggregation_eliminate`や`column_prune`などのロジック最適化ルールを無効にします[<a href="https://github.com/pingcap/tidb/pull/11658">#11658</a>](https://github.com/pingcap/tidb/pull/11658)
    -   結合キーでプレフィックス インデックスまたは負の値[<a href="https://github.com/pingcap/tidb/pull/11759">#11759</a>](https://github.com/pingcap/tidb/pull/11759)に等しい符号なしインデックス列が使用されている場合、 `Index Join`に対して誤った結果が返されることがある問題を修正します。
    -   `create … binding ...`の`SELECT`ステートメントの`”`または`\`で解析エラーが発生する可能性がある問題を修正[<a href="https://github.com/pingcap/tidb/pull/11726">#11726</a>](https://github.com/pingcap/tidb/pull/11726)
-   SQL実行エンジン
    -   Quote関数がnull値を扱う場合に戻り値の型エラーが発生することがある問題を修正[<a href="https://github.com/pingcap/tidb/pull/11619">#11619</a>](https://github.com/pingcap/tidb/pull/11619)
    -   `NotNullFlag` [<a href="https://github.com/pingcap/tidb/pull/11641">#11641</a>](https://github.com/pingcap/tidb/pull/11641)保持した状態で型推論に Max/Min を使用すると、 `ifnull`に対して誤った結果が返される可能性がある問題を修正
    -   文字列形式[<a href="https://github.com/pingcap/tidb/pull/11660">#11660</a>](https://github.com/pingcap/tidb/pull/11660)のビット型データを比較するときに発生する潜在的なエラーを修正しました。
    -   OOM [<a href="https://github.com/pingcap/tidb/pull/11679">#11679</a>](https://github.com/pingcap/tidb/pull/11679)の可能性を下げるために、シーケンシャル読み取りを必要とするデータの同時実行性を減らします。
    -   一部の組み込み関数( `if`と`coalesce`など) で複数のパラメーターが署名されていない場合に、誤った型推論が発生する可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/pull/11621">#11621</a>](https://github.com/pingcap/tidb/pull/11621)
    -   `Div`関数が符号なし 10 進数型を処理する場合の MySQL との非互換性を修正します[<a href="https://github.com/pingcap/tidb/pull/11813">#11813</a>](https://github.com/pingcap/tidb/pull/11813)
    -   Pump/Drainer[<a href="https://github.com/pingcap/tidb/pull/11827">#11827</a>](https://github.com/pingcap/tidb/pull/11827)の状態を変更するSQL実行時にpanicが発生する場合がある問題を修正
    -   Autocommit = 1 で`begin`ステートメントが存在しない場合、 `select ... for update`でpanicが発生することがある問題を修正[<a href="https://github.com/pingcap/tidb/pull/11736">#11736</a>](https://github.com/pingcap/tidb/pull/11736)
    -   `set default role`ステートメントの実行時に発生する可能性がある権限チェック エラーを修正[<a href="https://github.com/pingcap/tidb/pull/11777">#11777</a>](https://github.com/pingcap/tidb/pull/11777)
    -   `create user`または`drop user`を実行した際にパーミッションチェックエラーが発生することがある問題を修正[<a href="https://github.com/pingcap/tidb/pull/11814">#11814</a>](https://github.com/pingcap/tidb/pull/11814)
    -   `select ... for update`ステートメントが`PointGetExecutor`関数に構築されるときに自動再試行される可能性がある問題を修正します。 [<a href="https://github.com/pingcap/tidb/pull/11718">#11718</a>](https://github.com/pingcap/tidb/pull/11718)
    -   Window 関数がパーティション[<a href="https://github.com/pingcap/tidb/pull/11825">#11825</a>](https://github.com/pingcap/tidb/pull/11825)を処理するときに発生する可能性がある境界エラーを修正しました。
    -   不正な形式の引数[<a href="https://github.com/pingcap/tidb/pull/11893">#11893</a>](https://github.com/pingcap/tidb/pull/11893)を処理するときに`time`関数で EOF エラーが発生する問題を修正します。
    -   Window 関数が渡されたパラメータをチェックしない問題を修正します[<a href="https://github.com/pingcap/tidb/pull/11705">#11705</a>](https://github.com/pingcap/tidb/pull/11705)
    -   `Explain`で表示される計画結果と実際に実行された計画[<a href="https://github.com/pingcap/tidb/pull/11186">#11186</a>](https://github.com/pingcap/tidb/pull/11186)が一致しない問題を修正
    -   Window 関数によって参照されるメモリが重複すると、クラッシュまたは不正な結果が発生する可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/pull/11823">#11823</a>](https://github.com/pingcap/tidb/pull/11823)
    -   遅いログ[<a href="https://github.com/pingcap/tidb/pull/11887">#11887</a>](https://github.com/pingcap/tidb/pull/11887)の`Succ`フィールドの誤った情報を更新します。
-   サーバ
    -   `tidb_back_off_wexight`変数の名前を`tidb_backoff_weight` [<a href="https://github.com/pingcap/tidb/pull/11665">#11665</a>](https://github.com/pingcap/tidb/pull/11665)に変更します。
    -   現在の TiDB と互換性のある TiKV の最小バージョンを v3.0.0 に更新します[<a href="https://github.com/pingcap/tidb/pull/11618">#11618</a>](https://github.com/pingcap/tidb/pull/11618)
    -   テスト内のスイートが正しく使用されていることを確認するためのサポート`make testSuite` [<a href="https://github.com/pingcap/tidb/pull/11685">#11685</a>](https://github.com/pingcap/tidb/pull/11685)
-   DDL
    -   複数のパーティションの削除中にパーティション タイプを変更するステートメントなど、サポートされていないパーティション関連の DDL ステートメントの実行をスキップします[<a href="https://github.com/pingcap/tidb/pull/11373">#11373</a>](https://github.com/pingcap/tidb/pull/11373)
    -   生成されたカラムをその依存列の前に配置することを禁止します[<a href="https://github.com/pingcap/tidb/pull/11686">#11686</a>](https://github.com/pingcap/tidb/pull/11686)
    -   デフォルト値の`tidb_ddl_reorg_worker_cnt`と`tidb_ddl_reorg_batch_size`を変更します[<a href="https://github.com/pingcap/tidb/pull/11874">#11874</a>](https://github.com/pingcap/tidb/pull/11874)
-   モニター
    -   新しいバックオフ監視タイプを追加して、各バックオフ タイプの継続時間を記録します。コミット バックオフ[<a href="https://github.com/pingcap/tidb/pull/11728">#11728</a>](https://github.com/pingcap/tidb/pull/11728)など、以前はカウントされていなかったタイプをカバーするバックオフ メトリックをさらに追加します。

## TiKV {#tikv}

-   コンテキスト[<a href="https://github.com/tikv/tikv/pull/5256">#5256</a>](https://github.com/tikv/tikv/pull/5256)の重複によりReadIndex がリクエストに応答できない可能性がある問題を修正します。
-   時期尚早な`PutStore` [<a href="https://github.com/tikv/tikv/pull/5277">#5277</a>](https://github.com/tikv/tikv/pull/5277)によって引き起こされる潜在的なスケジューリングのジッターを修正
-   リージョンハートビート[<a href="https://github.com/tikv/tikv/pull/5296">#5296</a>](https://github.com/tikv/tikv/pull/5296)から報告される誤ったタイムスタンプを修正
-   コア ダンプから共有ブロックキャッシュを除外して、コア ダンプのサイズを削減します[<a href="https://github.com/tikv/tikv/pull/5322">#5322</a>](https://github.com/tikv/tikv/pull/5322)
-   リージョンのマージ[<a href="https://github.com/tikv/tikv/pull/5291">#5291</a>](https://github.com/tikv/tikv/pull/5291)中に発生する可能性のある TiKV パニックを修正
-   デッドロック検出器[<a href="https://github.com/tikv/tikv/pull/5317">#5317</a>](https://github.com/tikv/tikv/pull/5317)のリーダー変更チェックを高速化
-   `grpc env`を使用したデッドロック クライアントの作成のサポート[<a href="https://github.com/tikv/tikv/pull/5346">#5346</a>](https://github.com/tikv/tikv/pull/5346)
-   設定が正しいかどうかを確認するには`config-check`を追加します[<a href="https://github.com/tikv/tikv/pull/5349">#5349</a>](https://github.com/tikv/tikv/pull/5349)
-   リーダー[<a href="https://github.com/tikv/tikv/pull/5351">#5351</a>](https://github.com/tikv/tikv/pull/5351)がない場合にReadIndexが何も返さない問題を修正

## PD {#pd}

-   `pdctl` [<a href="https://github.com/pingcap/pd/pull/1685">#1685</a>](https://github.com/pingcap/pd/pull/1685)の成功メッセージを返す

## ツール {#tools}

-   TiDBBinlog
    -   Drainerのデフォルト値`defaultBinlogItemCount`を 65536 から 512 に変更して、 Drainer起動時の OOM の可能性を減らします[<a href="https://github.com/pingcap/tidb-binlog/pull/721">#721</a>](https://github.com/pingcap/tidb-binlog/pull/721)
    -   ポンプサーバーのオフライン ロジックを最適化して、潜在的なオフラインの輻輳を回避します[<a href="https://github.com/pingcap/tidb-binlog/pull/701">#701</a>](https://github.com/pingcap/tidb-binlog/pull/701)
-   TiDB Lightning:
    -   [<a href="https://github.com/pingcap/tidb-lightning/pull/225">#225</a>](https://github.com/pingcap/tidb-lightning/pull/225)をインポートするときに、デフォルトでシステム データベース`mysql` 、 `information_schema` 、 `performance_schema` 、および`sys`をスキップします。

## TiDB Ansible {#tidb-ansible}

-   ローリング アップデートの PD 操作を最適化して安定性を向上[<a href="https://github.com/pingcap/tidb-ansible/pull/894">#894</a>](https://github.com/pingcap/tidb-ansible/pull/894)
-   現在の Grafana バージョン[<a href="https://github.com/pingcap/tidb-ansible/pull/892">#892</a>](https://github.com/pingcap/tidb-ansible/pull/892)でサポートされていない Grafana Collector コンポーネントを削除します。
-   TiKV アラート ルールの更新[<a href="https://github.com/pingcap/tidb-ansible/pull/898">#898</a>](https://github.com/pingcap/tidb-ansible/pull/898)
-   生成された TiKV 構成に`pessimistic-txn`パラメータ[<a href="https://github.com/pingcap/tidb-ansible/pull/911">#911</a>](https://github.com/pingcap/tidb-ansible/pull/911)が欠落している問題を修正
-   Spark を V2.4.3 に更新し、TiSpark [<a href="https://github.com/pingcap/tidb-ansible/pull/918">#918</a>](https://github.com/pingcap/tidb-ansible/pull/918) Spark V2.4.3 と互換性のある V2.1.4 に更新します[<a href="https://github.com/pingcap/tidb-ansible/pull/913">#913</a>](https://github.com/pingcap/tidb-ansible/pull/913)
