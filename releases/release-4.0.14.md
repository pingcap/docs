---
title: TiDB 4.0.14 Release Notes
---

# TiDB 4.0.14 リリースノート {#tidb-4-0-14-release-notes}

発売日：2021年7月27日

TiDB バージョン: 4.0.14

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   v4.0 では、デフォルト値の`tidb_multi_statement_mode`が`WARN`から`OFF`に変更されました。代わりに、クライアント ライブラリのマルチステートメント機能を使用することをお勧めします。詳細は[`tidb_multi_statement_mode`に関するドキュメント](/system-variables.md#tidb_multi_statement_mode-new-in-v4011)を参照してください。 [#25749](https://github.com/pingcap/tidb/pull/25749)
    -   Grafana ダッシュボードを v6.1.16 から v7.5.7 にアップグレードして、2 つのセキュリティ脆弱性を解決します。詳細は[Grafana ブログ投稿](https://grafana.com/blog/2020/06/03/grafana-6.7.4-and-7.0.2-released-with-important-security-fix/)を参照してください。
    -   `tidb_stmt_summary_max_stmt_count`変数のデフォルト値を`200`から`3000` [#25872](https://github.com/pingcap/tidb/pull/25872)に変更します。

-   TiKV

    -   デフォルト値の`merge-check-tick-interval` `10`から`2`に変更して、リージョンのマージ プロセスを高速化します[#9676](https://github.com/tikv/tikv/pull/9676)

## 機能強化 {#feature-enhancements}

-   TiKV

    -   メトリクス`pending`を追加して、保留中の PD ハートビートの数を監視します。これは、遅い PD スレッドの問題を特定するのに役立ちます[#10008](https://github.com/tikv/tikv/pull/10008)
    -   仮想ホスト アドレッシング モードを使用して、 BR がS3 互換storageをサポートするようにするサポート[#10242](https://github.com/tikv/tikv/pull/10242)

-   TiDB ダッシュボード

    -   OIDC SSO をサポートします。 OIDC 互換の SSO サービス (Okta や Auth0 など) を設定することで、ユーザーは SQL パスワードを入力せずに TiDB ダッシュボードにログインできます。 [#960](https://github.com/pingcap/tidb-dashboard/pull/960)
    -   **デバッグ API** UI を追加します。これは、高度なデバッグのためにいくつかの一般的な TiDB および PD 内部 API を呼び出すためのコマンド ラインの代替方法です[#927](https://github.com/pingcap/tidb-dashboard/pull/927)

## 改良点 {#improvements}

-   TiDB

    -   `UPDATE`回の読み取り[#26223](https://github.com/pingcap/tidb/pull/26223)に対して`point get`または`batch point get`を使用して、インデックス キーの`LOCK`レコードを`PUT`レコードに変更します。
    -   MySQL システム変数`init_connect`とそれに関連する機能[#26031](https://github.com/pingcap/tidb/pull/26031)サポート
    -   安定した結果モードをサポートして、クエリ結果をより安定させます[#26003](https://github.com/pingcap/tidb/pull/26003)
    -   組み込み関数`json_unquote()`を TiKV [#25721](https://github.com/pingcap/tidb/pull/25721)にプッシュ ダウンするサポート
    -   SQL Plan Management (SPM) が文字セットの影響を受けないようにする[#23295](https://github.com/pingcap/tidb/pull/23295)

-   TiKV

    -   最初にステータスサーバーをシャットダウンして、クライアントがシャットダウン ステータスを正しく確認できることを確認します[#10504](https://github.com/tikv/tikv/pull/10504)
    -   古いピアに常に応答して、これらのピアがより迅速にクリアされるようにします[#10400](https://github.com/tikv/tikv/pull/10400)
    -   TiCDC シンクのメモリ消費を制限する[#10147](https://github.com/tikv/tikv/pull/10147)
    -   リージョンが大きすぎる場合は、偶数分割を使用して分割プロセスを高速化します[#10275](https://github.com/tikv/tikv/pull/10275)

-   PD

    -   同時に実行される複数のスケジューラ間の競合を減らす[#3858](https://github.com/pingcap/pd/pull/3858) [#3854](https://github.com/tikv/pd/pull/3854)

-   TiDB ダッシュボード

    -   TiDB ダッシュボードを v2021.07.17.1 に更新する[#3882](https://github.com/pingcap/pd/pull/3882)
    -   それ以上の変更を避けるために、現在のセッションを読み取り専用セッションとして共有することをサポートします[#960](https://github.com/pingcap/tidb-dashboard/pull/960)

-   ツール

    -   バックアップと復元 (BR)

        -   小さなバックアップ ファイルをマージして復元を高速化する[#655](https://github.com/pingcap/br/pull/655)

    -   Dumpling

        -   アップストリームが TiDB v3.x クラスターである場合は、常に`_tidb_rowid`使用してテーブルを分割します。これにより、TiDB のメモリ使用量を削減できます[#306](https://github.com/pingcap/dumpling/pull/306)

    -   TiCDC

        -   PD エンドポイントで証明書が見つからない場合に返されるエラー メッセージを改善します[#1973](https://github.com/pingcap/tiflow/issues/1973)
        -   ソーターの I/O エラーをより使いやすくする[#1976](https://github.com/pingcap/tiflow/pull/1976)
        -   KV クライアントのリージョン増分スキャンに同時実行制限を追加して、TiKV [#1926](https://github.com/pingcap/tiflow/pull/1926)のプレッシャーを軽減します
        -   テーブルメモリ消費量のメトリックを追加します[#1884](https://github.com/pingcap/tiflow/pull/1884)
        -   TiCDCサーバー構成に`capture-session-ttl`を追加します[#2169](https://github.com/pingcap/tiflow/pull/2169)

## バグの修正 {#bug-fixes}

-   TiDB

    -   `false` [#24865](https://github.com/pingcap/tidb/issues/24865)に評価される`WHERE`句でサブクエリを結合すると、 `SELECT`結果が MySQL と互換性がない問題を修正します
    -   引数が`ENUM`または`SET`型[#24944](https://github.com/pingcap/tidb/issues/24944)の場合に発生する`ifnull`関数の計算エラーを修正
    -   場合によっては間違った集計プルーニングを修正する[#25202](https://github.com/pingcap/tidb/issues/25202)
    -   列が`SET`タイプ[#25669](https://github.com/pingcap/tidb/issues/25669)の場合に発生する可能性のあるマージ結合操作の誤った結果を修正します。
    -   TiDB がデカルト結合[#25591](https://github.com/pingcap/tidb/issues/25591)に対して間違った結果を返す問題を修正
    -   結合操作で`SELECT ... FOR UPDATE`機能し、結合でパーティションテーブルが使用されている場合に発生するpanicの問題を修正します[#20028](https://github.com/pingcap/tidb/issues/20028)
    -   キャッシュされた`prepared`プランが`point get` [#24741](https://github.com/pingcap/tidb/issues/24741)に誤って使用される問題を修正
    -   `LOAD DATA`ステートメントが非 utf8 データを異常にインポートできる問題を修正[#25979](https://github.com/pingcap/tidb/issues/25979)
    -   HTTP API [#24650](https://github.com/pingcap/tidb/pull/24650)経由で統計にアクセスするときに発生する潜在的なメモリリークの問題を修正します。
    -   `ALTER USER`ステートメント[#25225](https://github.com/pingcap/tidb/issues/25225)の実行時に発生するセキュリティの問題を修正します。
    -   `TIKV_REGION_PEERS`テーブルが`DOWN`ステータス[#24879](https://github.com/pingcap/tidb/issues/24879)を正しく処理できないバグを修正
    -   `DateTime` [#22231](https://github.com/pingcap/tidb/issues/22231)の解析時に無効な文字列が切り捨てられない問題を修正
    -   列タイプが`YEAR` [#22159](https://github.com/pingcap/tidb/issues/22159)の場合、 `select into outfile`ステートメントが結果を返さない場合がある問題を修正します。
    -   `UNION`サブクエリ[#26532](https://github.com/pingcap/tidb/issues/26532)に`NULL`があるとクエリ結果がおかしくなることがある問題を修正
    -   実行中の射影演算子が場合によってはpanicを引き起こす可能性がある問題を修正します[#26534](https://github.com/pingcap/tidb/pull/26534)

-   TiKV

    -   特定のプラットフォームで継続時間の計算がpanicになる問題を修正[#関連する問題](https://github.com/rust-lang/rust/issues/86470#issuecomment-877557654)
    -   `DOUBLE`を`DOUBLE` [#25200](https://github.com/pingcap/tidb/issues/25200)にキャストする間違った関数を修正
    -   非同期ロガー使用時にpanicログが失われることがある問題を修正[#8998](https://github.com/tikv/tikv/issues/8998)
    -   暗号化が有効になっている場合にスナップショットを 2 回作成すると発生するpanicの問題を修正します[#9786](https://github.com/tikv/tikv/issues/9786) [#10407](https://github.com/tikv/tikv/issues/10407)
    -   コプロセッサ[#10176](https://github.com/tikv/tikv/issues/10176)の`json_unquote()`関数の間違った引数タイプを修正します。
    -   シャットダウン中の疑わしい警告と、 Raftstoreからの非決定論的な応答の問題を修正します[#10353](https://github.com/tikv/tikv/issues/10353) [#10307](https://github.com/tikv/tikv/issues/10307)
    -   バックアップ スレッド リークの問題を修正します[#10287](https://github.com/tikv/tikv/issues/10287)
    -   分割プロセスが遅すぎてリージョンのリージョンがpanicになり、メタデータが破損する可能性がある問題を修正します[#8456](https://github.com/tikv/tikv/issues/8456) [#8783](https://github.com/tikv/tikv/issues/8783)
    -   一部の状況で、リージョンのハートビートによって TiKV が大きなリージョンを分割できないという問題を修正します[#10111](https://github.com/tikv/tikv/issues/10111)
    -   TiKV と TiDB [#25638](https://github.com/pingcap/tidb/issues/25638)の間の CM Sketch のフォーマットの不一致によって引き起こされる誤った統計を修正します。
    -   `apply wait duration`メトリクス[#9893](https://github.com/tikv/tikv/issues/9893)の誤った統計を修正する
    -   Titan [#10232](https://github.com/tikv/tikv/pull/10232)で`delete_files_in_range`使用した後の「Missing Blob」エラーを修正

-   PD

    -   削除操作を実行した後にスケジューラーが再表示される可能性があるバグを修正します[#2572](https://github.com/tikv/pd/issues/2572)
    -   一時構成がロードされる前にスケジューラーが開始されたときに発生する可能性があるデータ競合の問題を修正します[#3771](https://github.com/tikv/pd/issues/3771)
    -   リージョン分散操作中に発生する可能性のある PDpanicの問題を修正します[#3761](https://github.com/pingcap/pd/pull/3761)
    -   一部のオペレーターの優先度が正しく設定されていない問題を修正[#3703](https://github.com/pingcap/pd/pull/3703)
    -   存在しないストアから`evict-leader`スケジューラーを削除するときに発生する可能性のある PDpanicの問題を修正します[#3660](https://github.com/tikv/pd/issues/3660)
    -   店舗数が多い場合、PDLeaderの再選が遅い問題を修正[#3697](https://github.com/tikv/pd/issues/3697)

-   TiDB ダッシュボード

    -   **プロファイリング**UI がすべての TiDB インスタンスをプロファイリングできないという問題を修正します[#944](https://github.com/pingcap/tidb-dashboard/pull/944)
    -   **ステートメント**UI に「計画数」が表示されない問題を修正します[#939](https://github.com/pingcap/tidb-dashboard/pull/939)
    -   クラスターのアップグレード後に**スロー クエリ**UI に「不明なフィールド」エラーが表示されることがある問題を修正します[#902](https://github.com/pingcap/tidb-dashboard/issues/902)

-   TiFlash

    -   DAG リクエストのコンパイル時に発生する潜在的なpanicの問題を修正
    -   読み取り負荷が高い場合に発生するpanicの問題を修正
    -   列storageの分割失敗によりTiFlash が再起動し続ける問題を修正
    -   TiFlash が差分データを削除できない潜在的なバグを修正
    -   共有デルタ インデックスを同時に複製するときに発生する誤った結果を修正します。
    -   データが不完全な場合、 TiFlash が再起動に失敗するバグを修正
    -   古い dm ファイルが自動的に削除されない問題を修正
    -   特定の引数で`SUBSTRING`関数を実行すると発生するpanicの問題を修正します。
    -   `INTEGER`型を`TIME`型にキャストしたときの結果が正しくない問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   `mysql`スキーマからのデータ復元が失敗する可能性がある問題を修正します[#1142](https://github.com/pingcap/br/pull/1142)

    -   TiDB Lightning

        -   TiDB Lightning がParquet ファイルの`DECIMAL`型データの解析に失敗する問題を修正[#1276](https://github.com/pingcap/br/pull/1276)
        -   TiDB Lightning がインポートされた大きな CSV ファイルを分割するときに報告される EOF エラーを修正します[#1133](https://github.com/pingcap/br/issues/1133)
        -   TiDB Lightning が`FLOAT`または`DOUBLE`タイプ[#1185](https://github.com/pingcap/br/pull/1185)の`auto_increment`列を持つテーブルをインポートすると、非常に大きなベース値が生成されるバグを修正します
        -   4 GB を超える KV データを生成するとTiDB Lightningpanicが発生する問題を修正[#1128](https://github.com/pingcap/br/pull/1128)

    -   Dumpling

        -   Dumplingを使用してデータを S3storageにエクスポートする場合、バケット全体に対する`s3:ListBucket`アクセス許可は不要になりました。アクセス許可は、データ ソース プレフィックスに対してのみ必要です。 [#898](https://github.com/pingcap/br/issues/898)

    -   TiCDC

        -   新しいテーブル パーティションを追加した後の余分なパーティション ディスパッチの問題を修正します[#2205](https://github.com/pingcap/tiflow/pull/2205)
        -   TiCDC が`/proc/meminfo` [#2023](https://github.com/pingcap/tiflow/pull/2023)の読み取りに失敗したときに発生するpanicの問題を修正します。
        -   TiCDC の実行時のメモリ消費を削減する[#2011](https://github.com/pingcap/tiflow/pull/2011) [#1957](https://github.com/pingcap/tiflow/pull/1957)
        -   MySQL シンクがエラーに遭遇して一時停止した後、一部の MySQL 接続がリークする可能性があるというバグを修正します[#1945](https://github.com/pingcap/tiflow/pull/1945)
        -   開始 TS が現在の TS から GC TTL [#1839](https://github.com/pingcap/tiflow/issues/1839)を引いた値より小さい場合、TiCDC チェンジフィードを作成できない問題を修正
        -   過度の CPU オーバーヘッドを避けるために、ソート ヒープのメモリ`malloc`を減らします[#1853](https://github.com/pingcap/tiflow/issues/1853)
        -   テーブル移動時にレプリケーションタスクが停止することがある不具合を修正[#1827](https://github.com/pingcap/tiflow/pull/1827)
