---
title: TiDB 4.0.14 Release Notes
---

# TiDB4.0.14リリースノート {#tidb-4-0-14-release-notes}

発売日：2021年7月27日

TiDBバージョン：4.0.14

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   v4.0では、デフォルト値の`tidb_multi_statement_mode`を`WARN`から`OFF`に変更します。代わりに、クライアントライブラリのマルチステートメント機能を使用することをお勧めします。詳細については、 [`tidb_multi_statement_mode`に関するドキュメント](/system-variables.md#tidb_multi_statement_mode-new-in-v4011)を参照してください。 [＃25749](https://github.com/pingcap/tidb/pull/25749)
    -   Grafanaダッシュボードをv6.1.16からv7.5.7にアップグレードして、2つのセキュリティの脆弱性を解決します。詳細については、 [Grafanaブログ投稿](https://grafana.com/blog/2020/06/03/grafana-6.7.4-and-7.0.2-released-with-important-security-fix/)を参照してください。
    -   `tidb_stmt_summary_max_stmt_count`変数のデフォルト値を`200`から[＃25872](https://github.com/pingcap/tidb/pull/25872)に変更し`3000` 。

-   TiKV

    -   リージョンのマージプロセスを高速化するには、デフォルト値の`merge-check-tick-interval`を`10`から`2`に変更します[＃9676](https://github.com/tikv/tikv/pull/9676)

## 機能の強化 {#feature-enhancements}

-   TiKV

    -   メトリック`pending`を追加して、保留中のPDハートビートの数を監視します。これは、遅いPDスレッド[＃10008](https://github.com/tikv/tikv/pull/10008)の問題を特定するのに役立ちます。
    -   仮想ホストアドレッシングモードの使用をサポートして、BRがS3互換ストレージをサポートするようにする[＃10242](https://github.com/tikv/tikv/pull/10242)

-   TiDBダッシュボード

    -   OIDCSSOをサポートします。 OIDC互換のSSOサービス（OktaやAuth0など）を設定することで、ユーザーはSQLパスワードを入力せずにTiDBダッシュボードにログインできます。 [＃960](https://github.com/pingcap/tidb-dashboard/pull/960)
    -   高度なデバッグのためにいくつかの一般的なTiDBおよびPD内部**API**を呼び出すためのコマンドラインの代替メソッドであるDebugAPIUIを追加します[＃927](https://github.com/pingcap/tidb-dashboard/pull/927)

## 改善点 {#improvements}

-   TiDB

    -   `UPDATE`の読み取りに`point get`または`batch point get`を使用して、インデックスキーの`LOCK`レコードを`PUT`レコードに変更します[＃26223](https://github.com/pingcap/tidb/pull/26223)
    -   MySQLシステム変数`init_connect`とそれに関連する機能[＃26031](https://github.com/pingcap/tidb/pull/26031)をサポートする
    -   安定した結果モードをサポートして、クエリ結果をより安定させます[＃26003](https://github.com/pingcap/tidb/pull/26003)
    -   内蔵機能`json_unquote()`から[＃25721](https://github.com/pingcap/tidb/pull/25721)へのプッシュダウンをサポート
    -   SQL計画管理（SPM）を文字セット[＃23295](https://github.com/pingcap/tidb/pull/23295)の影響を受けないようにする

-   TiKV

    -   最初にステータスサーバーをシャットダウンして、クライアントがシャットダウンステータスを正しく確認できることを確認します[＃10504](https://github.com/tikv/tikv/pull/10504)
    -   常に古いピアに応答して、これらのピアがより迅速にクリアされるようにします[＃10400](https://github.com/tikv/tikv/pull/10400)
    -   TiCDCシンクのメモリ消費を制限する[＃10147](https://github.com/tikv/tikv/pull/10147)
    -   リージョンが大きすぎる場合は、偶数分割を使用して分割プロセスを高速化します[＃10275](https://github.com/tikv/tikv/pull/10275)

-   PD

    -   同時に実行される複数のスケジューラー間の競合を減らし[＃3854](https://github.com/tikv/pd/pull/3854) [＃3858](https://github.com/pingcap/pd/pull/3858)

-   TiDBダッシュボード

    -   TiDBダッシュボードをv2021.07.17.1に更新します[＃3882](https://github.com/pingcap/pd/pull/3882)
    -   現在のセッションを読み取り専用セッションとして共有して、それ以上の変更を回避することをサポートします[＃960](https://github.com/pingcap/tidb-dashboard/pull/960)

-   ツール

    -   バックアップと復元（BR）

        -   小さなバックアップファイルをマージして復元を高速化[#655](https://github.com/pingcap/br/pull/655)

    -   Dumpling

        -   アップストリームがTiDBv3.xクラスタの場合は、常に`_tidb_rowid`を使用してテーブルを分割します。これにより、TiDBのメモリ使用量が削減されます[＃306](https://github.com/pingcap/dumpling/pull/306)

    -   TiCDC

        -   PDエンドポイントが証明書を見逃したときに返されるエラーメッセージを改善する[＃1973](https://github.com/pingcap/tiflow/issues/1973)
        -   ソーターI/Oエラーをよりユーザーフレンドリーにする[＃1976](https://github.com/pingcap/tiflow/pull/1976)
        -   KVクライアントのリージョンインクリメンタルスキャンに同時実行制限を追加して、TiKV1のプレッシャーを軽減し[＃1926](https://github.com/pingcap/tiflow/pull/1926)
        -   テーブルのメモリ消費量のメトリックを追加する[＃1884](https://github.com/pingcap/tiflow/pull/1884)
        -   TiCDCサーバー構成に`capture-session-ttl`を追加します[＃2169](https://github.com/pingcap/tiflow/pull/2169)

## バグの修正 {#bug-fixes}

-   TiDB

    -   `false` [＃24865](https://github.com/pingcap/tidb/issues/24865)と評価された`WHERE`句を使用してサブクエリを結合すると、 `SELECT`の結果がMySQLと互換性がないという問題を修正します。
    -   引数が`ENUM`または`SET`タイプ[＃24944](https://github.com/pingcap/tidb/issues/24944)の場合に発生する`ifnull`関数の計算エラーを修正しました
    -   場合によっては、間違った集計プルーニングを修正します[＃25202](https://github.com/pingcap/tidb/issues/25202)
    -   列が`SET`タイプ[＃25669](https://github.com/pingcap/tidb/issues/25669)の場合に発生する可能性があるマージ結合操作の誤った結果を修正します
    -   TiDBがデカルト結合[＃25591](https://github.com/pingcap/tidb/issues/25591)に対して誤った結果を返す問題を修正します
    -   `SELECT ... FOR UPDATE`が結合操作で機能し、結合がパーティションテーブル[＃20028](https://github.com/pingcap/tidb/issues/20028)を使用する場合に発生するpanicの問題を修正します。
    -   キャッシュされた`prepared`プランが[＃24741](https://github.com/pingcap/tidb/issues/24741)に誤って使用される問題を修正し`point get`
    -   `LOAD DATA`ステートメントがutf8以外のデータを異常にインポートする可能性がある問題を修正します[＃25979](https://github.com/pingcap/tidb/issues/25979)
    -   HTTPAPIを介して統計にアクセスするときに発生する可能性のあるメモリリークの問題を修正します[＃24650](https://github.com/pingcap/tidb/pull/24650)
    -   `ALTER USER`ステートメント[＃25225](https://github.com/pingcap/tidb/issues/25225)の実行時に発生するセキュリティの問題を修正します。
    -   `TIKV_REGION_PEERS`テーブルが`DOWN`ステータス[＃24879](https://github.com/pingcap/tidb/issues/24879)を正しく処理できないバグを修正します
    -   `DateTime`を解析するときに無効な文字列が切り捨てられない問題を修正し[＃22231](https://github.com/pingcap/tidb/issues/22231)
    -   列タイプが[＃22159](https://github.com/pingcap/tidb/issues/22159)の場合、 `select into outfile`ステートメントで結果が得られない可能性がある問題を修正し`YEAR` 。
    -   `NULL`が`UNION`サブクエリ[＃26532](https://github.com/pingcap/tidb/issues/26532)にある場合、クエリ結果が間違っている可能性がある問題を修正します。
    -   実行中の射影演算子が場合によってはpanicを引き起こす可能性がある問題を修正します[＃26534](https://github.com/pingcap/tidb/pull/26534)

-   TiKV

    -   特定のプラットフォームで期間の計算がpanicになる可能性がある問題を修正します[＃related-issue](https://github.com/rust-lang/rust/issues/86470#issuecomment-877557654)
    -   `DOUBLE`から[＃25200](https://github.com/pingcap/tidb/issues/25200)をキャストする間違った関数を修正し`DOUBLE`
    -   非同期ロガーを使用するとpanicログが失われる可能性がある問題を修正します[＃8998](https://github.com/tikv/tikv/issues/8998)
    -   暗号化が有効になっている場合にスナップショットを2回作成するときに発生するpanicの問題を修正し[＃10407](https://github.com/tikv/tikv/issues/10407) [＃9786](https://github.com/tikv/tikv/issues/9786)
    -   コプロセッサー[＃10176](https://github.com/tikv/tikv/issues/10176)の`json_unquote()`関数の間違った引数タイプを修正します
    -   シャットダウン中の疑わしい警告と[＃10307](https://github.com/tikv/tikv/issues/10307)からの非決定的な応答の問題を修正します[＃10353](https://github.com/tikv/tikv/issues/10353)
    -   バックアップスレッドリークの問題を修正[＃10287](https://github.com/tikv/tikv/issues/10287)
    -   分割プロセスが遅すぎてリージョンのマージが進行中の場合、リージョンの分割がpanicになり、メタデータが破損する可能性がある問題を修正します[＃8456](https://github.com/tikv/tikv/issues/8456) [＃8783](https://github.com/tikv/tikv/issues/8783)
    -   リージョンのハートビートにより、状況によってはTiKVが大きなリージョンを分割できない問題を修正します[＃10111](https://github.com/tikv/tikv/issues/10111)
    -   TiKVとTiDB1の間のCMスケッチのフォーマットの不一致によって引き起こされる誤った統計を修正し[＃25638](https://github.com/pingcap/tidb/issues/25638)
    -   `apply wait duration`メトリック[＃9893](https://github.com/tikv/tikv/issues/9893)の誤った統計を修正します
    -   Titan [＃10232](https://github.com/tikv/tikv/pull/10232)で`delete_files_in_range`を使用した後、「MissingBlob」エラーを修正しました

-   PD

    -   削除操作の実行後にスケジューラーが再表示される可能性があるバグを修正します[＃2572](https://github.com/tikv/pd/issues/2572)
    -   一時構成がロードされる前にスケジューラーが開始されたときに発生する可能性のあるデータ競合の問題を修正します[＃3771](https://github.com/tikv/pd/issues/3771)
    -   リージョン散乱操作中に発生する可能性のあるPDpanicの問題を修正します[＃3761](https://github.com/pingcap/pd/pull/3761)
    -   一部の演算子の優先度が正しく設定されていない問題を修正します[＃3703](https://github.com/pingcap/pd/pull/3703)
    -   存在しないストアから`evict-leader`スケジューラーを削除するときに発生する可能性があるPDpanicの問題を修正します[＃3660](https://github.com/tikv/pd/issues/3660)
    -   店舗数が多いとPDリーダーの再選が遅くなる問題を修正[＃3697](https://github.com/tikv/pd/issues/3697)

-   TiDBダッシュボード

    -   **プロファイリング**UIがすべてのTiDBインスタンスをプロファイリングできない問題を修正します[＃944](https://github.com/pingcap/tidb-dashboard/pull/944)
    -   **ステートメント**UIに「プランカウント」が表示されない問題を修正します[＃939](https://github.com/pingcap/tidb-dashboard/pull/939)
    -   クラスタのアップグレード後に**SlowQueryUI**に「不明なフィールド」エラーが表示される可能性がある問題を修正します[＃902](https://github.com/pingcap/tidb-dashboard/issues/902)

-   TiFlash

    -   DAGリクエストのコンパイル時に発生する可能性のあるpanicの問題を修正します
    -   読み取り負荷が大きいときに発生するpanicの問題を修正します
    -   列ストレージでの分割の失敗が原因でTiFlashが再起動し続ける問題を修正します
    -   TiFlashがデルタデータを削除できない潜在的なバグを修正します
    -   共有デルタインデックスを同時に複製するときに発生する誤った結果を修正します
    -   データが不完全な場合にTiFlashが再起動しないバグを修正します
    -   古いdmファイルを自動的に削除できない問題を修正します
    -   特定の引数を使用して`SUBSTRING`関数を実行するときに発生するpanicの問題を修正します
    -   `INTEGER`タイプを`TIME`タイプにキャストするときの誤った結果の問題を修正します

-   ツール

    -   バックアップと復元（BR）

        -   `mysql`スキーマからのデータ復元が失敗する可能性がある問題を修正します[＃1142](https://github.com/pingcap/br/pull/1142)

    -   TiDB Lightning

        -   TiDBLightningがTiDB Lightningファイル[＃1276](https://github.com/pingcap/br/pull/1276)の`DECIMAL`型データの解析に失敗する問題を修正します。
        -   TiDB Lightningがインポートされた大きなCSVファイルを分割するときに報告されるEOFエラーを修正します[＃1133](https://github.com/pingcap/br/issues/1133)
        -   TiDB Lightningが`FLOAT`または`DOUBLE`タイプ[＃1185](https://github.com/pingcap/br/pull/1185)の`auto_increment`列のテーブルをインポートすると、非常に大きな基本値が生成されるバグを修正します。
        -   4GBを超えるKVデータを生成するときに発生するTiDB Lightningpanicの問題を修正します[＃1128](https://github.com/pingcap/br/pull/1128)

    -   Dumpling

        -   Dumplingを使用してデータをS3ストレージにエクスポートする場合、バケット全体で`s3:ListBucket`のアクセス許可は不要になりました。この権限は、データソースプレフィックスにのみ必要です。 [＃898](https://github.com/pingcap/br/issues/898)

    -   TiCDC

        -   新しいテーブルパーティションを追加した後の余分なパーティションディスパッチの問題を修正します[＃2205](https://github.com/pingcap/tiflow/pull/2205)
        -   [＃2023](https://github.com/pingcap/tiflow/pull/2023)が13の読み取りに失敗したときに発生するpanicの問題を修正し`/proc/meminfo`
        -   [＃1957](https://github.com/pingcap/tiflow/pull/1957)のランタイムメモリ消費を削減する[＃2011](https://github.com/pingcap/tiflow/pull/2011)
        -   MySQLシンクがエラーに遭遇して一時停止した後に一部のMySQL接続がリークする可能性があるバグを修正します[＃1945](https://github.com/pingcap/tiflow/pull/1945)
        -   開始TSが現在のTSからGCTTL1を引いた値よりも小さい場合、 [＃1839](https://github.com/pingcap/tiflow/issues/1839)チェンジフィードを作成できない問題を修正します。
        -   ソートヒープ内のメモリ`malloc`を減らして、CPUオーバーヘッド[＃1853](https://github.com/pingcap/tiflow/issues/1853)が多すぎないようにします。
        -   テーブルを移動するときにレプリケーションタスクが停止する可能性があるバグを修正します[＃1827](https://github.com/pingcap/tiflow/pull/1827)
