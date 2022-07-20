---
title: TiDB 3.0.3 Release Notes
---

# TiDB3.0.3リリースノート {#tidb-3-0-3-release-notes}

発売日：2019年8月29日

TiDBバージョン：3.0.3

TiDB Ansibleバージョン：3.0.3

## TiDB {#tidb}

-   SQLオプティマイザー
    -   `opt_rule_blacklist`テーブルを追加して、 `aggregation_eliminate`や[＃11658](https://github.com/pingcap/tidb/pull/11658)などのロジック最適化ルールを無効にし`column_prune` 。
    -   結合キーが負の値[＃11759](https://github.com/pingcap/tidb/pull/11759)に等しいプレフィックスインデックスまたは符号なしインデックス列を使用すると、 `Index Join`に対して誤った結果が返される可能性がある問題を修正します。
    -   `create … binding ...`の`SELECT`のステートメントの`”`つまたは`\`が解析エラーになる可能性があるという問題を修正します[＃11726](https://github.com/pingcap/tidb/pull/11726)
-   SQL実行エンジン
    -   Quote関数がnull値を処理するときに戻り値のタイプエラーが発生する可能性がある問題を修正します[＃11619](https://github.com/pingcap/tidb/pull/11619)
    -   `NotNullFlag`が保持されたタイプ推論に最大/最小が使用された場合に`ifnull`の誤った結果が返される可能性がある問題を修正します[＃11641](https://github.com/pingcap/tidb/pull/11641)
    -   文字列形式[＃11660](https://github.com/pingcap/tidb/pull/11660)のビットタイプデータを比較するときに発生する可能性のあるエラーを修正します
    -   シーケンシャル読み取りが必要なデータの同時実行性を減らして、 [＃11679](https://github.com/pingcap/tidb/pull/11679)の可能性を減らします。
    -   一部の組み込み関数（ `if`や`coalesce`など）で複数のパラメーターが署名されていない場合に、誤った型の推測が発生する可能性がある問題を修正します[＃11621](https://github.com/pingcap/tidb/pull/11621)
    -   `Div`関数が符号なし10進型を処理する場合のMySQLとの非互換性を修正します[＃11813](https://github.com/pingcap/tidb/pull/11813)
    -   Pump/ Drainerのステータスを変更するSQLステートメントを実行するときにpanicが発生する可能性がある問題を修正し[＃11827](https://github.com/pingcap/tidb/pull/11827)
    -   Autocommit = 1で、 `begin`のステートメントがない場合に`select ... for update`でpanicが発生する可能性がある問題を修正します[＃11736](https://github.com/pingcap/tidb/pull/11736)
    -   `set default role`ステートメントの実行時に発生する可能性のある権限チェックエラーを修正します[＃11777](https://github.com/pingcap/tidb/pull/11777)
    -   `create user`または`drop user`を実行したときに発生する可能性のある権限チェックエラーを修正します[＃11814](https://github.com/pingcap/tidb/pull/11814)
    -   `select ... for update`ステートメントが`PointGetExecutor`関数[＃11718](https://github.com/pingcap/tidb/pull/11718)に組み込まれると、自動再試行される可能性がある問題を修正します。
    -   Window関数がパーティション[＃11825](https://github.com/pingcap/tidb/pull/11825)を処理するときに発生する可能性のある境界エラーを修正します
    -   誤ってフォーマットされた引数を処理するときに`time`関数がEOFエラーに遭遇する問題を修正します[＃11893](https://github.com/pingcap/tidb/pull/11893)
    -   Window関数が渡されたパラメーターをチェックしない問題を修正します[＃11705](https://github.com/pingcap/tidb/pull/11705)
    -   `Explain`を介して表示された計画結果が、実際に実行された計画[＃11186](https://github.com/pingcap/tidb/pull/11186)と矛盾する問題を修正します。
    -   Window関数によって参照される重複メモリがクラッシュまたは誤った結果をもたらす可能性がある問題を修正します[＃11823](https://github.com/pingcap/tidb/pull/11823)
    -   スローログ[＃11887](https://github.com/pingcap/tidb/pull/11887)の`Succ`フィールドの誤った情報を更新します
-   サーバ
    -   `tidb_back_off_wexight`変数の名前を[＃11665](https://github.com/pingcap/tidb/pull/11665)に変更し`tidb_backoff_weight`
    -   現在のTiDBと互換性のある最小TiKVバージョンを[＃11618](https://github.com/pingcap/tidb/pull/11618)に更新します。
    -   テストの[＃11685](https://github.com/pingcap/tidb/pull/11685)が正しく使用されていることを確認するためのサポート`make testSuite`
-   DDL
    -   複数のパーティションを削除するときにパーティションタイプを変更するステートメントを含む、サポートされていないパーティション関連のDDLステートメントの実行をスキップします[＃11373](https://github.com/pingcap/tidb/pull/11373)
    -   生成されたカラムをその依存列の前に配置することを禁止する[＃11686](https://github.com/pingcap/tidb/pull/11686)
    -   `tidb_ddl_reorg_worker_cnt`と[＃11874](https://github.com/pingcap/tidb/pull/11874)のデフォルト値を変更し`tidb_ddl_reorg_batch_size`
-   モニター
    -   新しいバックオフ監視タイプを追加して、各バックオフタイプの期間を記録します。コミットバックオフ[＃11728](https://github.com/pingcap/tidb/pull/11728)など、以前はカウントされていなかったタイプをカバーするために、バックオフメトリックを追加します。

## TiKV {#tikv}

-   コンテキスト[＃5256](https://github.com/tikv/tikv/pull/5256)が重複しているためにReadIndexがリクエストに応答できない可能性がある問題を修正します
-   時期[＃5277](https://github.com/tikv/tikv/pull/5277)の`PutStore`によって引き起こされる潜在的なスケジューリングジッターを修正する
-   リージョンハートビートから報告された誤ったタイムスタンプを修正[＃5296](https://github.com/tikv/tikv/pull/5296)
-   共有ブロックキャッシュをコアダンプから除外して、コアダンプのサイズを縮小します[＃5322](https://github.com/tikv/tikv/pull/5322)
-   リージョンマージ中の潜在的なTiKVパニックを修正[＃5291](https://github.com/tikv/tikv/pull/5291)
-   デッドロック検出器のリーダー変更チェックを高速化[＃5317](https://github.com/tikv/tikv/pull/5317)
-   `grpc env`を使用したデッドロッククライアントの作成のサポート[＃5346](https://github.com/tikv/tikv/pull/5346)
-   `config-check`を追加して、構成が正しいかどうかを確認します[＃5349](https://github.com/tikv/tikv/pull/5349)
-   リーダーがない場合にReadIndexが何も返さない問題を修正します[＃5351](https://github.com/tikv/tikv/pull/5351)

## PD {#pd}

-   [＃1685](https://github.com/pingcap/pd/pull/1685)の成功メッセージを返し`pdctl`

## ツール {#tools}

-   TiDB Binlog
    -   Drainerのデフォルト値`defaultBinlogItemCount`を65536から512に変更して、 Drainerの起動時にOOMが発生する可能性を減らします[＃721](https://github.com/pingcap/tidb-binlog/pull/721)
    -   潜在的なオフライン輻輳を回避するために、ポンプサーバーのオフラインロジックを最適化する[＃701](https://github.com/pingcap/tidb-binlog/pull/701)
-   TiDB Lightning：
    -   `information_schema`をインポートする場合、デフォルトでシステムデータベース`mysql` 、および`performance_schema`をスキップし`sys` [＃225](https://github.com/pingcap/tidb-lightning/pull/225)

## TiDB Ansible {#tidb-ansible}

-   安定性を向上させるためにローリングアップデートのためにPD操作を最適化する[＃894](https://github.com/pingcap/tidb-ansible/pull/894)
-   現在のGrafanaバージョン[＃892](https://github.com/pingcap/tidb-ansible/pull/892)でサポートされていないGrafanaCollectorコンポーネントを削除します
-   TiKVアラートルールを更新する[＃898](https://github.com/pingcap/tidb-ansible/pull/898)
-   生成されたTiKV構成が`pessimistic-txn`パラメーター[＃911](https://github.com/pingcap/tidb-ansible/pull/911)を見逃す問題を修正します
-   SparkをV2.4.3に更新し、 [＃918](https://github.com/pingcap/tidb-ansible/pull/918)をSpark V2.4.3 [＃913](https://github.com/pingcap/tidb-ansible/pull/913)と互換性のあるV2.1.4に更新します。
