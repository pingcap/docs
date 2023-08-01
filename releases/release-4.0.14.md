---
title: TiDB 4.0.14 Release Notes
---

# TiDB 4.0.14 リリースノート {#tidb-4-0-14-release-notes}

発売日：2021年7月27日

TiDB バージョン: 4.0.14

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   v4.0 では、デフォルト値`tidb_multi_statement_mode`を`WARN`から`OFF`に変更します。代わりに、クライアント ライブラリのマルチステートメント機能を使用することをお勧めします。詳細は[`tidb_multi_statement_mode`に関するドキュメント](/system-variables.md#tidb_multi_statement_mode-new-in-v4011)を参照してください。 [#25749](https://github.com/pingcap/tidb/pull/25749)
    -   Grafana ダッシュボードを v6.1.16 から v7.5.7 にアップグレードして、2 つのセキュリティ脆弱性を解決します。詳細は[グラファナのブログ投稿](https://grafana.com/blog/2020/06/03/grafana-6.7.4-and-7.0.2-released-with-important-security-fix/)を参照してください。
    -   `tidb_stmt_summary_max_stmt_count`変数のデフォルト値を`200`から`3000`に変更します[#25872](https://github.com/pingcap/tidb/pull/25872)

-   TiKV

    -   デフォルト値の`merge-check-tick-interval` `10`から`2`に変更して、リージョンのマージ プロセスを高速化します[#9676](https://github.com/tikv/tikv/pull/9676)

## 機能強化 {#feature-enhancements}

-   TiKV

    -   保留中の PD ハートビートの数を監視するメトリック`pending`を追加します。これは、遅い PD スレッド[#10008](https://github.com/tikv/tikv/pull/10008)の問題を特定するのに役立ちます。
    -   BR でS3 互換storageをサポートするための仮想ホスト アドレッシング モードの使用のサポート[#10242](https://github.com/tikv/tikv/pull/10242)

-   TiDB ダッシュボード

    -   OIDC SSO をサポートします。 OIDC 互換の SSO サービス (Okta や Auth0 など) を設定すると、ユーザーは SQL パスワードを入力せずに TiDB ダッシュボードにログインできます。 [#960](https://github.com/pingcap/tidb-dashboard/pull/960)
    -   **デバッグ API** UI を追加します。これは、高度なデバッグのためにいくつかの一般的な TiDB および PD 内部 API を呼び出すコマンド ラインの代替方法です[#927](https://github.com/pingcap/tidb-dashboard/pull/927)

## 改善点 {#improvements}

-   TiDB

    -   `UPDATE`回の読み取りに対して`point get`または`batch point get`を使用して、インデックス キーの`LOCK`レコードを`PUT`レコードに変更します[#26223](https://github.com/pingcap/tidb/pull/26223)
    -   MySQL システム変数`init_connect`とそれに関連する機能[#26031](https://github.com/pingcap/tidb/pull/26031)をサポートします。
    -   安定した結果モードをサポートして、クエリ結果をより安定させます[#26003](https://github.com/pingcap/tidb/pull/26003)
    -   組み込み関数`json_unquote()`の TiKV [#25721](https://github.com/pingcap/tidb/pull/25721)へのプッシュダウンをサポート
    -   SQL プラン管理 (SPM) が文字セット[#23295](https://github.com/pingcap/tidb/pull/23295)の影響を受けないようにする

-   TiKV

    -   まずステータスサーバーをシャットダウンして、クライアントがシャットダウン ステータスを正しく確認できることを確認します[#10504](https://github.com/tikv/tikv/pull/10504)
    -   古いピアに常に応答して、これらのピアがより早くクリアされるようにします[#10400](https://github.com/tikv/tikv/pull/10400)
    -   TiCDC シンクのメモリ消費を制限する[#10147](https://github.com/tikv/tikv/pull/10147)
    -   リージョンが大きすぎる場合は、均等分割を使用して分割プロセスを高速化します[#10275](https://github.com/tikv/tikv/pull/10275)

-   PD

    -   同時に実行される複数のスケジューラ間の競合を軽減します[#3858](https://github.com/pingcap/pd/pull/3858) [#3854](https://github.com/tikv/pd/pull/3854)

-   TiDB ダッシュボード

    -   TiDB ダッシュボードを v2021.07.17.1 に更新します[#3882](https://github.com/pingcap/pd/pull/3882)
    -   現在のセッションを読み取り専用セッションとして共有し、それ以上の変更を避けることをサポートします[#960](https://github.com/pingcap/tidb-dashboard/pull/960)

-   ツール

    -   バックアップと復元 (BR)

        -   小さなバックアップ ファイルを結合することで復元を高速化します[#655](https://github.com/pingcap/br/pull/655)

    -   Dumpling

        -   アップストリームが TiDB v3.x クラスターの場合は、常に`_tidb_rowid`使用してテーブルを分割します。これにより、TiDB のメモリ使用量が削減されます[#306](https://github.com/pingcap/dumpling/pull/306)

    -   TiCDC

        -   PD エンドポイントに証明書がない場合に返されるエラー メッセージを改善します[#1973](https://github.com/pingcap/tiflow/issues/1973)
        -   ソーターの I/O エラーをより使いやすくする[#1976](https://github.com/pingcap/tiflow/pull/1976)
        -   TiKV [#1926](https://github.com/pingcap/tiflow/pull/1926)の負荷を軽減するために、KV クライアントのリージョン増分スキャンに同時実行制限を追加します。
        -   テーブルのメモリ消費量のメトリクスを追加[#1884](https://github.com/pingcap/tiflow/pull/1884)
        -   TiCDCサーバー構成[#2169](https://github.com/pingcap/tiflow/pull/2169)に`capture-session-ttl`を追加します。

## バグの修正 {#bug-fixes}

-   TiDB

    -   `false` [#24865](https://github.com/pingcap/tidb/issues/24865)と評価される`WHERE`句を含むサブクエリを結合すると、 `SELECT`結果が MySQL と互換性がないという問題を修正
    -   引数が`ENUM`または`SET`型[#24944](https://github.com/pingcap/tidb/issues/24944)の場合に発生する`ifnull`関数の計算エラーを修正
    -   場合によっては間違った集約プルーニングを修正[#25202](https://github.com/pingcap/tidb/issues/25202)
    -   列が`SET` type [#25669](https://github.com/pingcap/tidb/issues/25669)の場合に発生する可能性があるマージ結合操作の誤った結果を修正しました。
    -   TiDB がデカルト結合[#25591](https://github.com/pingcap/tidb/issues/25591)に対して間違った結果を返す問題を修正
    -   `SELECT ... FOR UPDATE`結合操作で動作し、その結合でパーティションテーブル[#20028](https://github.com/pingcap/tidb/issues/20028)が使用されている場合に発生するpanicの問題を修正します。
    -   キャッシュされた`prepared`プランが`point get` [#24741](https://github.com/pingcap/tidb/issues/24741)に誤って使用される問題を修正
    -   `LOAD DATA`ステートメントが非 utf8 データを異常にインポートする可能性がある問題を修正します[#25979](https://github.com/pingcap/tidb/issues/25979)
    -   HTTP API [#24650](https://github.com/pingcap/tidb/pull/24650)経由で統計にアクセスするときに発生する潜在的なメモリリークの問題を修正します。
    -   `ALTER USER`ステートメント[#25225](https://github.com/pingcap/tidb/issues/25225)の実行時に発生するセキュリティ問題を修正します。
    -   `TIKV_REGION_PEERS`テーブルが`DOWN`ステータス[#24879](https://github.com/pingcap/tidb/issues/24879)を正しく扱えないバグを修正
    -   `DateTime` [#22231](https://github.com/pingcap/tidb/issues/22231)の解析時に無効な文字列が切り捨てられない問題を修正
    -   列の型が`YEAR` [#22159](https://github.com/pingcap/tidb/issues/22159)の場合、 `select into outfile`ステートメントの結果が得られないことがある問題を修正します。
    -   `UNION`サブクエリ[#26532](https://github.com/pingcap/tidb/issues/26532)に`NULL`が含まれている場合、クエリ結果が間違っていることがある問題を修正
    -   実行中の投影オペレータが場合によってpanicを引き起こす可能性がある問題を修正[#26534](https://github.com/pingcap/tidb/pull/26534)

-   TiKV

    -   特定のプラットフォームで継続時間の計算がpanicになる問題を修正[#関連問題](https://github.com/rust-lang/rust/issues/86470#issuecomment-877557654)
    -   `DOUBLE`を`DOUBLE` [#25200](https://github.com/pingcap/tidb/issues/25200)にキャストする間違った関数を修正
    -   非同期ロガー[#8998](https://github.com/tikv/tikv/issues/8998)を使用するとpanicログが失われる可能性がある問題を修正
    -   暗号化が有効になっている場合にスナップショットを 2 回構築すると発生するpanicの問題を修正します[#9786](https://github.com/tikv/tikv/issues/9786) [#10407](https://github.com/tikv/tikv/issues/10407)
    -   コプロセッサ[#10176](https://github.com/tikv/tikv/issues/10176)の`json_unquote()`関数の間違った引数の型を修正しました。
    -   シャットダウン中の不審な警告とRaftstoreからの非決定的な応答の問題を修正[#10353](https://github.com/tikv/tikv/issues/10353) [#10307](https://github.com/tikv/tikv/issues/10307)
    -   バックアップスレッドのリーク[#10287](https://github.com/tikv/tikv/issues/10287)の問題を修正
    -   分割プロセスが遅すぎてリージョンのリージョンがパニックを起こしてメタデータが破損する可能性がある問題を修正します[#8456](https://github.com/tikv/tikv/issues/8456) [#8783](https://github.com/tikv/tikv/issues/8783)
    -   状況によっては、リージョンのハートビートによって TiKV が大きなリージョンを分割できないという問題を修正します[#10111](https://github.com/tikv/tikv/issues/10111)
    -   TiKV と TiDB [#25638](https://github.com/pingcap/tidb/issues/25638)の間の CM スケッチの形式の不一致によって引き起こされる間違った統計を修正しました。
    -   `apply wait duration`メトリクス[#9893](https://github.com/tikv/tikv/issues/9893)の間違った統計を修正します。
    -   Titan [#10232](https://github.com/tikv/tikv/pull/10232)で`delete_files_in_range`使用した後の「Missing Blob」エラーを修正

-   PD

    -   削除操作[#2572](https://github.com/tikv/pd/issues/2572)を実行するとスケジューラが再表示される場合があるバグを修正
    -   一時構成がロードされる前にスケジューラが起動されたときに発生する可能性があるデータ競合の問題を修正します[#3771](https://github.com/tikv/pd/issues/3771)
    -   リージョン分散操作[#3761](https://github.com/pingcap/pd/pull/3761)中に発生する可能性がある PDpanicの問題を修正します。
    -   一部の演算子の優先度が正しく設定されない問題を修正[#3703](https://github.com/pingcap/pd/pull/3703)
    -   存在しないストア[#3660](https://github.com/tikv/pd/issues/3660)から`evict-leader`スケジューラを削除するときに発生する可能性がある PDpanicの問題を修正します。
    -   店舗数が多い場合、PDLeaderの再選出が遅い問題を修正[#3697](https://github.com/tikv/pd/issues/3697)

-   TiDB ダッシュボード

    -   **プロファイリング**UI がすべての TiDB インスタンスをプロファイリングできない問題を修正します[#944](https://github.com/pingcap/tidb-dashboard/pull/944)
    -   **ステートメント**UI に「プラン数」が表示されない問題を修正します[#939](https://github.com/pingcap/tidb-dashboard/pull/939)
    -   クラスターのアップグレード後に**スロー クエリ**UI に「不明なフィールド」エラーが表示されることがある問題を修正[#902](https://github.com/pingcap/tidb-dashboard/issues/902)

-   TiFlash

    -   DAG リクエストのコンパイル時に発生する潜在的なpanicの問題を修正
    -   読み取り負荷が高いときに発生するpanicの問題を修正
    -   カラムstorageの分割障害によりTiFlash が再起動し続ける問題を修正
    -   TiFlash がデルタ データを削除できない潜在的なバグを修正
    -   共有デルタインデックスを同時にクローン作成するときに発生する誤った結果を修正
    -   データが不完全な場合にTiFlashの再起動に失敗するバグを修正
    -   古いDMファイルが自動的に削除できない問題を修正
    -   特定の引数を指定して`SUBSTRING`関数を実行するときに発生するpanicの問題を修正
    -   `INTEGER`型を`TIME`型にキャストするときに誤った結果が表示される問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   `mysql`スキーマからのデータの復元が失敗する可能性がある問題を修正します[#1142](https://github.com/pingcap/br/pull/1142)

    -   TiDB Lightning

        -   TiDB Lightning がParquet ファイル[#1276](https://github.com/pingcap/br/pull/1276)の`DECIMAL`タイプのデータの解析に失敗する問題を修正
        -   TiDB Lightning がインポートされた大きな CSV ファイルを分割するときに報告される EOF エラーを修正しました[#1133](https://github.com/pingcap/br/issues/1133)
        -   TiDB Lightning が`FLOAT`または`DOUBLE`型[#1185](https://github.com/pingcap/br/pull/1185)の`auto_increment`カラムを持つテーブルをインポートすると、過度に大きなベース値が生成されるバグを修正
        -   4 GB を超える KV データを生成するときに発生するTiDB Lightningpanicの問題を修正します[#1128](https://github.com/pingcap/br/pull/1128)

    -   Dumpling

        -   Dumplingを使用してデータを S3storageにエクスポートする場合、バケット全体に対する`s3:ListBucket`権限は必要なくなりました。権限はデータ ソース プレフィックスに対してのみ必要です。 [#898](https://github.com/pingcap/br/issues/898)

    -   TiCDC

        -   新しいテーブル パーティションを追加した後の余分なパーティションのディスパッチの問題を修正[#2205](https://github.com/pingcap/tiflow/pull/2205)
        -   TiCDC が`/proc/meminfo` [#2023](https://github.com/pingcap/tiflow/pull/2023)の読み取りに失敗したときに発生するpanicの問題を修正
        -   TiCDC のランタイムメモリ消費量を削減[#2011](https://github.com/pingcap/tiflow/pull/2011) [#1957](https://github.com/pingcap/tiflow/pull/1957)
        -   MySQL シンクがエラーに遭遇して一時停止した後、一部の MySQL 接続がリークする可能性があるバグを修正します[#1945](https://github.com/pingcap/tiflow/pull/1945)
        -   開始 TS が現在の TS から GC TTL [#1839](https://github.com/pingcap/tiflow/issues/1839)を引いたものより小さい場合、TiCDC チェンジフィードを作成できない問題を修正
        -   過剰な CPU オーバーヘッドを避けるために、ソート ヒープ内のメモリ`malloc`を削減します[#1853](https://github.com/pingcap/tiflow/issues/1853)
        -   テーブル[#1827](https://github.com/pingcap/tiflow/pull/1827)の移動時にレプリケーションタスクが停止する場合があるバグを修正
