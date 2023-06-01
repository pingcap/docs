---
title: TiDB 5.1.1 Release Notes
---

# TiDB 5.1.1 リリースノート {#tidb-5-1-1-release-notes}

リリース日：2021年7月30日

TiDB バージョン: 5.1.1

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   TiDB クラスターを v4.0 から v5.1 にアップグレードする場合、デフォルト値`tidb_multi_statement_mode`は`OFF`です。代わりに、クライアント ライブラリのマルチステートメント機能を使用することをお勧めします。詳細は[<a href="/system-variables.md#tidb_multi_statement_mode-new-in-v4011">`tidb_multi_statement_mode`に関するドキュメント</a>](/system-variables.md#tidb_multi_statement_mode-new-in-v4011)を参照してください。 [<a href="https://github.com/pingcap/tidb/pull/25751">#25751</a>](https://github.com/pingcap/tidb/pull/25751)
    -   `tidb_stmt_summary_max_stmt_count`変数のデフォルト値を`200`から`3000`に変更します[<a href="https://github.com/pingcap/tidb/pull/25874">#25874</a>](https://github.com/pingcap/tidb/pull/25874)
    -   `table_storage_stats`テーブル[<a href="https://github.com/pingcap/tidb/pull/26352">#26352</a>](https://github.com/pingcap/tidb/pull/26352)にアクセスするには`SUPER`権限が必要です
    -   他のユーザーの権限を表示するには`information_schema.user_privileges`テーブルにアクセスするには`mysql.user`の`SELECT`権限が必要です[<a href="https://github.com/pingcap/tidb/pull/26311">#26311</a>](https://github.com/pingcap/tidb/pull/26311)
    -   `information_schema.cluster_hardware`テーブル[<a href="https://github.com/pingcap/tidb/pull/26297">#26297</a>](https://github.com/pingcap/tidb/pull/26297)にアクセスするには`CONFIG`権限が必要です
    -   `information_schema.cluster_info`テーブル[<a href="https://github.com/pingcap/tidb/pull/26297">#26297</a>](https://github.com/pingcap/tidb/pull/26297)にアクセスするには`PROCESS`権限が必要です
    -   `information_schema.cluster_load`テーブル[<a href="https://github.com/pingcap/tidb/pull/26297">#26297</a>](https://github.com/pingcap/tidb/pull/26297)にアクセスするには`PROCESS`権限が必要です
    -   `information_schema.cluster_systeminfo`テーブル[<a href="https://github.com/pingcap/tidb/pull/26297">#26297</a>](https://github.com/pingcap/tidb/pull/26297)にアクセスするには`PROCESS`権限が必要です
    -   `information_schema.cluster_log`テーブル[<a href="https://github.com/pingcap/tidb/pull/26297">#26297</a>](https://github.com/pingcap/tidb/pull/26297)にアクセスするには`PROCESS`権限が必要です
    -   `information_schema.cluster_config`テーブル[<a href="https://github.com/pingcap/tidb/pull/26150">#26150</a>](https://github.com/pingcap/tidb/pull/26150)にアクセスするには`CONFIG`権限が必要です

## 機能強化 {#feature-enhancements}

-   TiDB ダッシュボード

    -   OIDC SSO をサポートします。 OIDC 互換の SSO サービス (Okta や Auth0 など) を設定すると、ユーザーは SQL パスワードを入力せずに TiDB ダッシュボードにログインできます。 [<a href="https://github.com/tikv/pd/pull/3883">#3883</a>](https://github.com/tikv/pd/pull/3883)

-   TiFlash

    -   DAG リクエストで`HAVING()`関数をサポートする

## 改善点 {#improvements}

-   TiDB

    -   ステイル読み取り機能の一般提供 (GA) を発表します。
    -   データ挿入を高速化するために`paramMarker`割り当てを避ける[<a href="https://github.com/pingcap/tidb/pull/26076">#26076</a>](https://github.com/pingcap/tidb/pull/26076)
    -   安定した結果モードをサポートして、クエリ結果をより安定させます[<a href="https://github.com/pingcap/tidb/pull/25995">#25995</a>](https://github.com/pingcap/tidb/pull/25995)
    -   組み込み関数`json_unquote()`の TiKV [<a href="https://github.com/pingcap/tidb/pull/26265">#26265</a>](https://github.com/pingcap/tidb/pull/26265)へのプッシュダウンをサポート
    -   MPP クエリの再試行をサポート[<a href="https://github.com/pingcap/tidb/pull/26480">#26480</a>](https://github.com/pingcap/tidb/pull/26480)
    -   `UPDATE`回の読み取りに対して`point get`または`batch point get`を使用して、インデックス キーの`LOCK`レコードを`PUT`レコードに変更します[<a href="https://github.com/pingcap/tidb/pull/26225">#26225</a>](https://github.com/pingcap/tidb/pull/26225)
    -   古いクエリからのビューの作成を禁止する[<a href="https://github.com/pingcap/tidb/pull/26200">#26200</a>](https://github.com/pingcap/tidb/pull/26200)
    -   `COUNT(DISTINCT)` MPPモードのアグリゲーション機能を徹底的に突き詰める[<a href="https://github.com/pingcap/tidb/pull/26194">#26194</a>](https://github.com/pingcap/tidb/pull/26194)
    -   MPP クエリを起動する前にTiFlashが利用可能かどうかを確認する[<a href="https://github.com/pingcap/tidb/pull/26192">#26192</a>](https://github.com/pingcap/tidb/pull/26192)
    -   読み取りタイムスタンプを将来の時刻に設定することを許可しない[<a href="https://github.com/pingcap/tidb/pull/25763">#25763</a>](https://github.com/pingcap/tidb/pull/25763)
    -   集計関数を`EXPLAIN`ステートメントでプッシュダウンできない場合のログ警告の出力[<a href="https://github.com/pingcap/tidb/pull/25737">#25737</a>](https://github.com/pingcap/tidb/pull/25737)
    -   クラスター[<a href="https://github.com/pingcap/tidb/pull/25587">#25587</a>](https://github.com/pingcap/tidb/pull/25587)のエビクト数情報を記録するテーブル`statements_summary_evicted`を追加します。
    -   書式指定子`%b/%M/%r/%T` [<a href="https://github.com/pingcap/tidb/pull/25768">#25768</a>](https://github.com/pingcap/tidb/pull/25768)の組み込み関数`str_to_date`の MySQL 互換性を向上します。

-   TiKV

    -   未確定エラーの可能性を減らすために、事前書き込みリクエストを可能な限り冪等にしてください[<a href="https://github.com/tikv/tikv/pull/10586">#10586</a>](https://github.com/tikv/tikv/pull/10586)
    -   期限切れのコマンドを多数処理する際のスタック オーバーフローのリスクを防止します[<a href="https://github.com/tikv/tikv/pull/10502">#10502</a>](https://github.com/tikv/tikv/pull/10502)
    -   ステイル読み取りリクエストの`start_ts`から update `max_ts` [<a href="https://github.com/tikv/tikv/pull/10451">#10451</a>](https://github.com/tikv/tikv/pull/10451)を使用しないことで、過剰なコミット リクエストの再試行を回避します。
    -   読み取りレイテンシー[<a href="https://github.com/tikv/tikv/pull/10592">#10592</a>](https://github.com/tikv/tikv/pull/10592)を短縮するために、読み取り準備完了と書き込み準備完了を個別に処理します。
    -   I/O レート制限が有効になっている場合のデータ インポート速度への影響を軽減します[<a href="https://github.com/tikv/tikv/pull/10390">#10390</a>](https://github.com/tikv/tikv/pull/10390)
    -   Raft gRPC 接続間のロード バランスを改善する[<a href="https://github.com/tikv/tikv/pull/10495">#10495</a>](https://github.com/tikv/tikv/pull/10495)

-   ツール

    -   TiCDC

        -   `file sorter` [<a href="https://github.com/pingcap/tiflow/pull/2327">#2327</a>](https://github.com/pingcap/tiflow/pull/2327)を削除
        -   PD エンドポイントに証明書がない場合に返されるエラー メッセージを改善します[<a href="https://github.com/pingcap/tiflow/issues/1973">#1973</a>](https://github.com/pingcap/tiflow/issues/1973)

    -   TiDB Lightning

        -   スキーマを復元するための再試行メカニズムを追加します[<a href="https://github.com/pingcap/br/pull/1294">#1294</a>](https://github.com/pingcap/br/pull/1294)

    -   Dumpling

        -   アップストリームが TiDB v3.x クラスターの場合は、常に`_tidb_rowid`使用してテーブルを分割します。これにより、TiDB のメモリ使用量が削減されます[<a href="https://github.com/pingcap/dumpling/issues/295">#295</a>](https://github.com/pingcap/dumpling/issues/295)
        -   データベースのメタデータにアクセスする頻度を減らして、Dumpling のパフォーマンスと安定性を向上させます[<a href="https://github.com/pingcap/dumpling/pull/315">#315</a>](https://github.com/pingcap/dumpling/pull/315)

## バグの修正 {#bug-fixes}

-   TiDB

    -   `tidb_enable_amend_pessimistic_txn=on` [<a href="https://github.com/pingcap/tidb/issues/26203">#26203</a>](https://github.com/pingcap/tidb/issues/26203)で列タイプを変更するときに発生する可能性があるデータ損失の問題を修正します。
    -   SQLモード[<a href="https://github.com/pingcap/tidb/pull/26001">#26001</a>](https://github.com/pingcap/tidb/pull/26001)において`last_day`関数の動作が互換性がない問題を修正
    -   `LIMIT`ウィンドウ関数[<a href="https://github.com/pingcap/tidb/issues/25344">#25344</a>](https://github.com/pingcap/tidb/issues/25344)の上にある場合に発生する可能性があるpanicの問題を修正
    -   悲観的トランザクションをコミットすると書き込み競合が発生する可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/25964">#25964</a>](https://github.com/pingcap/tidb/issues/25964)
    -   相関サブクエリのインデクス結合結果が正しくない問題を修正[<a href="https://github.com/pingcap/tidb/issues/25799">#25799</a>](https://github.com/pingcap/tidb/issues/25799)
    -   正常にコミットされた楽観的トランザクションがコミット エラーを報告する可能性があるバグを修正[<a href="https://github.com/tikv/tikv/issues/10468">#10468</a>](https://github.com/tikv/tikv/issues/10468)
    -   `SET`型列[<a href="https://github.com/pingcap/tidb/issues/25669">#25669</a>](https://github.com/pingcap/tidb/issues/25669)でマージ結合を使用すると不正な結果が返される問題を修正
    -   悲観的トランザクションのインデックスキーが繰り返しコミットされる可能性があるバグを修正[<a href="https://github.com/pingcap/tidb/issues/26359">#26359</a>](https://github.com/pingcap/tidb/issues/26359)
    -   オプティマイザーがパーティション[<a href="https://github.com/pingcap/tidb/issues/26227">#26227</a>](https://github.com/pingcap/tidb/issues/26227)を検索する際の整数オーバーフローのリスクを修正します。
    -   `DATE`をタイムスタンプ[<a href="https://github.com/pingcap/tidb/issues/26292">#26292</a>](https://github.com/pingcap/tidb/issues/26292)にキャストするときに無効な値が書き込まれる可能性がある問題を修正
    -   Grafana [<a href="https://github.com/pingcap/tidb/issues/26338">#26338</a>](https://github.com/pingcap/tidb/issues/26338)でコプロセッサーキャッシュ メトリクスが表示されない問題を修正
    -   テレメトリによって発生する煩わしいログの問題を修正[<a href="https://github.com/pingcap/tidb/issues/25760">#25760</a>](https://github.com/pingcap/tidb/issues/25760) [<a href="https://github.com/pingcap/tidb/issues/25785">#25785</a>](https://github.com/pingcap/tidb/issues/25785)
    -   プレフィックスインデックス[<a href="https://github.com/pingcap/tidb/issues/26029">#26029</a>](https://github.com/pingcap/tidb/issues/26029)のクエリ範囲のバグを修正
    -   同じパーティションを同時に切り詰めると DDL 実行がハングする問題を修正します[<a href="https://github.com/pingcap/tidb/issues/26229">#26229</a>](https://github.com/pingcap/tidb/issues/26229)
    -   `ENUM`アイテム[<a href="https://github.com/pingcap/tidb/issues/25955">#25955</a>](https://github.com/pingcap/tidb/issues/25955)が重複する問題を修正
    -   CTEイテレータが正しく閉じられないバグを修正[<a href="https://github.com/pingcap/tidb/issues/26112">#26112</a>](https://github.com/pingcap/tidb/issues/26112)
    -   `LOAD DATA`ステートメントが非 utf8 データを異常にインポートする可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/25979">#25979</a>](https://github.com/pingcap/tidb/issues/25979)
    -   符号なし整数列でウィンドウ関数を使用するときに発生する可能性があるpanicの問題を修正します[<a href="https://github.com/pingcap/tidb/issues/25956">#25956</a>](https://github.com/pingcap/tidb/issues/25956)
    -   非同期コミット ロックを解決するときに TiDB がpanicになる可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/25778">#25778</a>](https://github.com/pingcap/tidb/issues/25778)
    -   ステイル読み取り が`PREPARE`ステートメント[<a href="https://github.com/pingcap/tidb/pull/25800">#25800</a>](https://github.com/pingcap/tidb/pull/25800)と完全な互換性がない問題を修正します。
    -   ODBC スタイルの定数 (たとえば、 `{d '2020-01-01'}` ) を式[<a href="https://github.com/pingcap/tidb/issues/25531">#25531</a>](https://github.com/pingcap/tidb/issues/25531)として使用できない問題を修正します。
    -   TiDB を単独で実行するときに発生するエラーを修正[<a href="https://github.com/pingcap/tidb/pull/25555">#25555</a>](https://github.com/pingcap/tidb/pull/25555)

-   TiKV

    -   特定のプラットフォームで継続時間の計算がpanicになる問題を修正[<a href="https://github.com/tikv/tikv/pull/10569">#10569</a>](https://github.com/tikv/tikv/pull/10569)
    -   Load Base Split で`batch_get_command` [<a href="https://github.com/tikv/tikv/issues/10542">#10542</a>](https://github.com/tikv/tikv/issues/10542)のエンコードされていないキーが誤って使用される問題を修正
    -   `resolved-ts.advance-ts-interval`構成を動的に変更してもすぐに有効にならない問題を修正します[<a href="https://github.com/tikv/tikv/issues/10426">#10426</a>](https://github.com/tikv/tikv/issues/10426)
    -   4 つを超えるレプリカでまれにフォロワーのメタデータが破損する問題を修正[<a href="https://github.com/tikv/tikv/issues/10225">#10225</a>](https://github.com/tikv/tikv/issues/10225)
    -   暗号化が有効になっている場合にスナップショットを 2 回構築すると発生するpanicの問題を修正します[<a href="https://github.com/tikv/tikv/issues/9786">#9786</a>](https://github.com/tikv/tikv/issues/9786) [<a href="https://github.com/tikv/tikv/issues/10407">#10407</a>](https://github.com/tikv/tikv/issues/10407)
    -   間違った`tikv_raftstore_hibernated_peer_state`メトリック[<a href="https://github.com/tikv/tikv/issues/10330">#10330</a>](https://github.com/tikv/tikv/issues/10330)を修正します
    -   コプロセッサ[<a href="https://github.com/tikv/tikv/issues/10176">#10176</a>](https://github.com/tikv/tikv/issues/10176)の`json_unquote()`関数の間違った引数の型を修正しました。
    -   悲観的トランザクションのインデックスキーが繰り返しコミットされる可能性があるバグを修正[<a href="https://github.com/tikv/tikv/issues/10468#issuecomment-869491061">#10468</a>](https://github.com/tikv/tikv/issues/10468#issuecomment-869491061)
    -   リーダーが転送された直後に`ReadIndex`リクエストが古い結果を返す問題を修正[<a href="https://github.com/tikv/tikv/issues/9351">#9351</a>](https://github.com/tikv/tikv/issues/9351)

-   PD

    -   複数のスケジューラが同時に実行されているために競合が発生した場合、期待したスケジューリングが生成できない問題を修正します[<a href="https://github.com/tikv/pd/issues/3807">#3807</a>](https://github.com/tikv/pd/issues/3807) [<a href="https://github.com/tikv/pd/issues/3778">#3778</a>](https://github.com/tikv/pd/issues/3778)
    -   スケジューラーを削除してもスケジューラーが再度表示される場合がある問題を修正[<a href="https://github.com/tikv/pd/issues/2572">#2572</a>](https://github.com/tikv/pd/issues/2572)

-   TiFlash

    -   テーブルスキャンタスクの実行時に発生する潜在的なpanicの問題を修正
    -   DAQ リクエストを処理するときにTiFlashが`duplicated region`に関するエラーを発生させるバグを修正
    -   読み取り負荷が高いときに発生するpanicの問題を修正
    -   `DateFormat`関数の実行時に発生する潜在的なpanicの問題を修正
    -   MPP タスクの実行時に発生する潜在的なメモリリークの問題を修正
    -   集計関数`COUNT`または`COUNT DISTINCT`を実行すると予期しない結果が発生する問題を修正
    -   複数のディスクに展開されている場合にTiFlash がデータを復元できないという潜在的なバグを修正
    -   TiDB ダッシュボードがTiFlashのディスク情報を正しく表示できない問題を修正
    -   `SharedQueryBlockInputStream`を分解するときに発生する潜在的なpanicの問題を修正
    -   `MPPTask`を分解するときに発生する潜在的なpanicの問題を修正
    -   スナップショット経由でデータを同期した後のデータの不整合の潜在的な問題を修正

-   ツール

    -   TiCDC

        -   新しい照合順序機能[<a href="https://github.com/pingcap/tiflow/issues/2301">#2301</a>](https://github.com/pingcap/tiflow/issues/2301)のサポートを修正しました。
        -   実行時に共有マップへの非同期アクセスがpanic[<a href="https://github.com/pingcap/tiflow/pull/2300">#2300</a>](https://github.com/pingcap/tiflow/pull/2300)を引き起こす可能性がある問題を修正します。
        -   DDL ステートメント[<a href="https://github.com/pingcap/tiflow/pull/2290">#2290</a>](https://github.com/pingcap/tiflow/pull/2290)の実行中に所有者がクラッシュしたときに発生する潜在的な DDL 損失の問題を修正します。
        -   TiDB のロックを途中で解決しようとする問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/2188">#2188</a>](https://github.com/pingcap/tiflow/issues/2188)
        -   テーブル移行の直後に TiCDC ノードが強制終了された場合にデータ損失を引き起こす可能性があるバグを修正[<a href="https://github.com/pingcap/tiflow/pull/2033">#2033</a>](https://github.com/pingcap/tiflow/pull/2033)
        -   `changefeed update` on `--sort-dir`と`--start-ts` [<a href="https://github.com/pingcap/tiflow/pull/1921">#1921</a>](https://github.com/pingcap/tiflow/pull/1921)の処理ロジックを修正

    -   バックアップと復元 (BR)

        -   復元するデータのサイズが正しく計算されない問題を修正します[<a href="https://github.com/pingcap/br/issues/1270">#1270</a>](https://github.com/pingcap/br/issues/1270)
        -   cdclog [<a href="https://github.com/pingcap/br/issues/870">#870</a>](https://github.com/pingcap/br/issues/870)から復元するときに発生する欠落した DDL イベントの問題を修正します。

    -   TiDB Lightning

        -   TiDB が Parquet ファイル[<a href="https://github.com/pingcap/br/pull/1275">#1275</a>](https://github.com/pingcap/br/pull/1275)の`DECIMAL`タイプのデータの解析に失敗する問題を修正します。
        -   キー間隔[<a href="https://github.com/pingcap/br/issues/1291">#1291</a>](https://github.com/pingcap/br/issues/1291) [<a href="https://github.com/pingcap/br/issues/1290">#1290</a>](https://github.com/pingcap/br/issues/1290)を計算する際の整数オーバーフローの問題を修正
