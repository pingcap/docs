---
title: TiDB 3.0.3 Release Notes
summary: TiDB 3.0.3 は、2019 年 8 月 29 日にリリースされました。SQL オプティマイザー、SQL 実行エンジン、サーバー、DDL、モニター、TiKV、PD、TiDB Binlog、 TiDB Lightning、および TiDB Ansible のさまざまな修正と更新が含まれています。注目すべき修正には、誤った結果、型エラー、panic発生、および権限チェック エラーに関する問題が含まれます。また、このリリースでは、PD 操作の最適化、サポートされていない Grafana Collector コンポーネントの削除、および TiKV アラート ルールの更新も行われています。さらに、TiDB Ansible は Spark V2.4.3 および TiSpark V2.1.4 をサポートするようになりました。
---

# TiDB 3.0.3 リリースノート {#tidb-3-0-3-release-notes}

発売日: 2019年8月29日

TiDB バージョン: 3.0.3

TiDB Ansible バージョン: 3.0.3

## ティビ {#tidb}

-   SQL オプティマイザー
    -   `aggregation_eliminate`や`column_prune`などのロジック最適化ルールを無効にするには、 `opt_rule_blacklist`テーブルを追加します[＃11658](https://github.com/pingcap/tidb/pull/11658)
    -   結合キーがプレフィックスインデックスまたは負の値に等しい符号なしインデックス列を使用する場合、 `Index Join`に対して誤った結果が返される可能性がある問題を修正しました[＃11759](https://github.com/pingcap/tidb/pull/11759)
    -   `create … binding ...`の`SELECT`のステートメントのうち`”`または`\`解析エラーになる可能性がある問題を修正しました[＃11726](https://github.com/pingcap/tidb/pull/11726)
-   SQL実行エンジン
    -   Quote関数がnull値を処理するときに戻り値の型エラーが発生する可能性がある問題を修正しました[＃11619](https://github.com/pingcap/tidb/pull/11619)
    -   `NotNullFlag`保持した状態で Max/Min を型推論に使用すると、 `ifnull`の誤った結果が返される可能性がある問題を修正しました[＃11641](https://github.com/pingcap/tidb/pull/11641)
    -   文字列形式[＃11660](https://github.com/pingcap/tidb/pull/11660)でビット型データを比較するときに発生する可能性のあるエラーを修正
    -   シーケンシャル読み取りを必要とするデータの同時実行性を減らして、OOM [＃11679](https://github.com/pingcap/tidb/pull/11679)の可能性を下げます。
    -   一部の組み込み関数で複数のパラメータが符号なしの場合（たとえば、 `if`と`coalesce` ）に誤った型推論が発生する可能性がある問題を修正しました[＃11621](https://github.com/pingcap/tidb/pull/11621)
    -   `Div`関数が符号なし 10 進数型を処理する場合の MySQL との非互換性を修正[＃11813](https://github.com/pingcap/tidb/pull/11813)
    -   Pump/Drainer[＃11827](https://github.com/pingcap/tidb/pull/11827)の状態を変更するSQL文を実行するとpanicが発生する可能性がある問題を修正
    -   Autocommit = 1 で`begin`文[＃11736](https://github.com/pingcap/tidb/pull/11736)がない場合に`select ... for update`でpanicが発生する可能性がある問題を修正しました。
    -   `set default role`文の実行時に発生する可能性のある権限チェックエラーを修正[＃11777](https://github.com/pingcap/tidb/pull/11777)
    -   `create user`または`drop user`を実行したときに発生する可能性のある権限チェックエラーを修正[＃11814](https://github.com/pingcap/tidb/pull/11814)
    -   `select ... for update`ステートメントが`PointGetExecutor`関数[＃11718](https://github.com/pingcap/tidb/pull/11718)に組み込まれると自動的に再試行される可能性がある問題を修正しました。
    -   ウィンドウ関数がパーティション[＃11825](https://github.com/pingcap/tidb/pull/11825)処理するときに発生する可能性のある境界エラーを修正しました
    -   `time`関数が誤った形式の引数[＃11893](https://github.com/pingcap/tidb/pull/11893)を処理するときに EOF エラーに遭遇する問題を修正しました
    -   ウィンドウ関数が渡されたパラメータをチェックしない問題を修正[＃11705](https://github.com/pingcap/tidb/pull/11705)
    -   `Explain`で表示される計画結果が実際に実行された計画[＃11186](https://github.com/pingcap/tidb/pull/11186)と一致しない問題を修正
    -   ウィンドウ関数によって参照される重複メモリがクラッシュや誤った結果を引き起こす可能性がある問題を修正[＃11823](https://github.com/pingcap/tidb/pull/11823)
    -   スローログ[＃11887](https://github.com/pingcap/tidb/pull/11887)の`Succ`フィールドの誤った情報を更新します
-   サーバ
    -   `tidb_back_off_wexight`変数の名前を`tidb_backoff_weight` [＃11665](https://github.com/pingcap/tidb/pull/11665)に変更します
    -   現在のTiDBと互換性のある最小TiKVバージョンをv3.0.0 [＃11618](https://github.com/pingcap/tidb/pull/11618)に更新します
    -   テストのスイートが正しく使用されていることを確認するためのサポート`make testSuite` [＃11685](https://github.com/pingcap/tidb/pull/11685)
-   DDL
    -   複数のパーティションを削除する際にパーティション タイプを変更するステートメントを含む、サポートされていないパーティション関連の DDL ステートメントの実行をスキップします[＃11373](https://github.com/pingcap/tidb/pull/11373)
    -   生成カラムを従属列の前に配置することを禁止する[＃11686](https://github.com/pingcap/tidb/pull/11686)
    -   `tidb_ddl_reorg_worker_cnt`と`tidb_ddl_reorg_batch_size`のデフォルト値を変更する[＃11874](https://github.com/pingcap/tidb/pull/11874)
-   モニター
    -   各バックオフタイプの期間を記録するための新しいバックオフ監視タイプを追加し、コミットバックオフ[＃11728](https://github.com/pingcap/tidb/pull/11728)など、これまでカウントされていなかったタイプをカバーするためにバックオフメトリックを追加します。

## ティクヴ {#tikv}

-   重複したコンテキスト[＃5256](https://github.com/tikv/tikv/pull/5256)が原因でReadIndex がリクエストに応答できない問題を修正しました。
-   早すぎる`PutStore` [＃5277](https://github.com/tikv/tikv/pull/5277)による潜在的なスケジュールのジッターを修正
-   リージョンハートビート[＃5296](https://github.com/tikv/tikv/pull/5296)から報告された誤ったタイムスタンプを修正
-   共有ブロックキャッシュを除外することでコアダンプのサイズを縮小する[＃5322](https://github.com/tikv/tikv/pull/5322)
-   リージョンマージ中に発生する可能性のある TiKV パニックを修正[＃5291](https://github.com/tikv/tikv/pull/5291)
-   デッドロック検出器[＃5317](https://github.com/tikv/tikv/pull/5317)のリーダー変更チェックを高速化
-   `grpc env`使用してデッドロック クライアント[＃5346](https://github.com/tikv/tikv/pull/5346)を作成するサポート
-   設定が正しいかどうかを確認するには`config-check`追加します[＃5349](https://github.com/tikv/tikv/pull/5349)
-   リーダー[＃5351](https://github.com/tikv/tikv/pull/5351)がない場合にReadIndex が何も返さない問題を修正しました

## PD {#pd}

-   `pdctl` [＃1685](https://github.com/pingcap/pd/pull/1685)の成功メッセージを返す

## ツール {#tools}

-   TiDBBinlog
    -   Drainerのデフォルト値`defaultBinlogItemCount` 65536 から 512 に変更して、 Drainer の起動時に OOM が発生する可能性を減らします[＃721](https://github.com/pingcap/tidb-binlog/pull/721)
    -   潜在的なオフライン輻輳を回避するためにポンプサーバーのオフラインロジックを最適化します[＃701](https://github.com/pingcap/tidb-binlog/pull/701)
-   TiDB Lightning:
    -   [＃225](https://github.com/pingcap/tidb-lightning/pull/225) `sys`インポートするときに、デフォルトでシステムデータベース`mysql` `performance_schema`スキップします`information_schema`

## TiDB アンシブル {#tidb-ansible}

-   ローリングアップデートのPD操作を最適化して安定性を向上[＃894](https://github.com/pingcap/tidb-ansible/pull/894)
-   現在のGrafanaバージョン[＃892](https://github.com/pingcap/tidb-ansible/pull/892)でサポートされていないGrafana Collectorコンポーネントを削除します。
-   TiKVアラートルール[＃898](https://github.com/pingcap/tidb-ansible/pull/898)更新
-   生成されたTiKV構成で`pessimistic-txn`パラメータ[＃911](https://github.com/pingcap/tidb-ansible/pull/911)が欠落する問題を修正
-   SparkをV2.4.3にアップデートし、TiSparkをSpark V2.4.3 [＃913](https://github.com/pingcap/tidb-ansible/pull/913) 、 [＃918](https://github.com/pingcap/tidb-ansible/pull/918)と互換性のあるV2.1.4にアップデートします。
