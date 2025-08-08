---
title: TiDB 4.0.14 Release Notes
summary: TiDB 4.0.14は2021年7月27日にリリースされました。このリリースには、互換性の変更、機能強化、改善、バグ修正、および各種ツールのアップデートが含まれています。主な変更点としては、TiDBとTiKVのデフォルト値の更新、TiDBダッシュボードでのOIDC SSOのサポート、TiDB、TiKV、PD、 TiFlash、および各種ツールのバグ修正などがあります。
---

# TiDB 4.0.14 リリースノート {#tidb-4-0-14-release-notes}

発売日：2021年7月27日

TiDB バージョン: 4.0.14

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   バージョン4.0では、デフォルト値の`tidb_multi_statement_mode`を`WARN`から`OFF`に変更しました。代わりに、クライアントライブラリのマルチステートメント機能を使用することをお勧めします。詳細は[`tidb_multi_statement_mode`に関するドキュメント](/system-variables.md#tidb_multi_statement_mode-new-in-v4011)ご覧ください[＃25749](https://github.com/pingcap/tidb/pull/25749)
    -   2つのセキュリティ脆弱性を解決するため、Grafanaダッシュボードをv6.1.16からv7.5.7にアップグレードしました。詳細は[Grafanaのブログ投稿](https://grafana.com/blog/2020/06/03/grafana-6.7.4-and-7.0.2-released-with-important-security-fix/)ご覧ください。
    -   `tidb_stmt_summary_max_stmt_count`変数のデフォルト値を`200`から`3000`に変更します[＃25872](https://github.com/pingcap/tidb/pull/25872)

-   TiKV

    -   リージョンマージプロセスを高速化するために、デフォルト値の`merge-check-tick-interval`を`10`から`2`に変更します[＃9676](https://github.com/tikv/tikv/pull/9676)

## 機能強化 {#feature-enhancements}

-   TiKV

    -   保留中のPDハートビートの数を監視するメトリック`pending`を追加します。これは、遅いPDスレッド[＃10008](https://github.com/tikv/tikv/pull/10008)の問題の特定に役立ちます。
    -   BRがS3互換storage[＃10242](https://github.com/tikv/tikv/pull/10242)サポートするために仮想ホストアドレス指定モードの使用をサポート

-   TiDBダッシュボード

    -   OIDC SSOをサポートします。OIDC対応のSSOサービス（OktaやAuth0など）を設定することで、ユーザーはSQLパスワードを入力せずにTiDBダッシュボードにログインできます[＃960](https://github.com/pingcap/tidb-dashboard/pull/960)
    -   高度なデバッグのために、いくつかの一般的な TiDB および PD 内部 API を呼び出すためのコマンドラインの代替手段である**デバッグ API** UI を追加します[＃927](https://github.com/pingcap/tidb-dashboard/pull/927)

## 改善点 {#improvements}

-   TiDB

    -   `UPDATE`読み取りで`point get`または`batch point get`使用して、インデックスキーの`LOCK`レコードを`PUT`レコードに変更します[＃26223](https://github.com/pingcap/tidb/pull/26223)
    -   MySQLシステム変数`init_connect`とその関連機能[＃26031](https://github.com/pingcap/tidb/pull/26031)サポートする
    -   クエリ結果をより安定させるために、安定した結果モードをサポートします[＃26003](https://github.com/pingcap/tidb/pull/26003)
    -   組み込み関数`json_unquote()`をTiKV [＃25721](https://github.com/pingcap/tidb/pull/25721)にプッシュダウンする機能をサポート
    -   SQLプラン管理（SPM）が文字セット[＃23295](https://github.com/pingcap/tidb/pull/23295)の影響を受けないようにする

-   TiKV

    -   最初にステータスサーバーをシャットダウンして、クライアントがシャットダウンステータス[＃10504](https://github.com/tikv/tikv/pull/10504)正しく確認できることを確認します。
    -   古いピアには常に応答して、これらのピアがより早くクリアされるようにしてください[＃10400](https://github.com/tikv/tikv/pull/10400)
    -   TiCDCシンクのメモリ消費を制限する[＃10147](https://github.com/tikv/tikv/pull/10147)
    -   リージョンが大きすぎる場合は、均等分割を使用して分割プロセスを高速化します[＃10275](https://github.com/tikv/tikv/pull/10275)

-   PD

    -   同時に実行される複数のスケジューラ間の競合を減らす[＃3858](https://github.com/pingcap/pd/pull/3858) [＃3854](https://github.com/tikv/pd/pull/3854)

-   TiDBダッシュボード

    -   TiDBダッシュボードをv2021.07.17.1に更新[＃3882](https://github.com/pingcap/pd/pull/3882)
    -   現在のセッションを読み取り専用セッションとして共有して、それ以上の変更を回避できるようにする[＃960](https://github.com/pingcap/tidb-dashboard/pull/960)

-   ツール

    -   バックアップと復元 (BR)

        -   小さなバックアップファイルを結合して復元を高速化[＃655](https://github.com/pingcap/br/pull/655)

    -   Dumpling

        -   アップストリームが TiDB v3.x クラスタの場合は、常に`_tidb_rowid`を使用してテーブルを分割します。これにより、TiDB のメモリ使用量が削減されます[＃306](https://github.com/pingcap/dumpling/pull/306)

    -   TiCDC

        -   PDエンドポイントに証明書がない場合に返されるエラーメッセージを改善しました[＃1973](https://github.com/pingcap/tiflow/issues/1973)
        -   ソーターのI/Oエラーをよりユーザーフレンドリーにする[＃1976](https://github.com/pingcap/tiflow/pull/1976)
        -   KVクライアントのリージョン増分スキャンに同時実行制限を追加して、TiKV [＃1926](https://github.com/pingcap/tiflow/pull/1926)の負荷を軽減します。
        -   テーブルメモリ消費量のメトリクスを追加する[＃1884](https://github.com/pingcap/tiflow/pull/1884)
        -   TiCDCサーバー構成[＃2169](https://github.com/pingcap/tiflow/pull/2169)に`capture-session-ttl`追加

## バグ修正 {#bug-fixes}

-   TiDB

    -   `false` [＃24865](https://github.com/pingcap/tidb/issues/24865)と評価される`WHERE`節を持つサブクエリを結合すると、 `SELECT`結果が MySQL と互換性がない問題を修正しました。
    -   引数が`ENUM`または`SET`型の場合に発生する`ifnull`関数の計算エラーを修正[＃24944](https://github.com/pingcap/tidb/issues/24944)
    -   いくつかのケースで誤った集計プルーニングを修正[＃25202](https://github.com/pingcap/tidb/issues/25202)
    -   列が`SET`型[＃25669](https://github.com/pingcap/tidb/issues/25669)の場合に発生する可能性のあるマージ結合操作の誤った結果を修正しました
    -   TiDBがカルテシアン結合[＃25591](https://github.com/pingcap/tidb/issues/25591)で間違った結果を返す問題を修正
    -   `SELECT ... FOR UPDATE`結合操作で動作し、結合がパーティションテーブル[＃20028](https://github.com/pingcap/tidb/issues/20028)を使用する場合に発生するpanic問題を修正しました。
    -   キャッシュされた`prepared`プランが`point get` [＃24741](https://github.com/pingcap/tidb/issues/24741)に誤って使用される問題を修正
    -   `LOAD DATA`文が非 UTF8 データを異常にインポートする可能性がある問題を修正[＃25979](https://github.com/pingcap/tidb/issues/25979)
    -   HTTP API [＃24650](https://github.com/pingcap/tidb/pull/24650)経由で統計情報にアクセスする際に発生する可能性のあるメモリリークの問題を修正しました
    -   `ALTER USER`文[＃25225](https://github.com/pingcap/tidb/issues/25225)実行するときに発生するセキュリティ問題を修正しました
    -   `TIKV_REGION_PEERS`テーブルが`DOWN`ステータス[＃24879](https://github.com/pingcap/tidb/issues/24879)正しく処理できないバグを修正
    -   `DateTime` [＃22231](https://github.com/pingcap/tidb/issues/22231)の解析時に無効な文字列が切り捨てられない問題を修正
    -   列タイプが`YEAR` [＃22159](https://github.com/pingcap/tidb/issues/22159)の場合に`select into outfile`文で結果が返されないことがある問題を修正しました
    -   `NULL` `UNION`サブクエリ[＃26532](https://github.com/pingcap/tidb/issues/26532)にある場合にクエリ結果が間違っている可能性がある問題を修正しました
    -   実行中の射影演算子が場合によってはpanicを引き起こす可能性がある問題を修正[＃26534](https://github.com/pingcap/tidb/pull/26534)

-   TiKV

    -   特定のプラットフォームで期間計算がpanicになる可能性がある問題を修正[#関連問題](https://github.com/rust-lang/rust/issues/86470#issuecomment-877557654)
    -   `DOUBLE`を`DOUBLE` [＃25200](https://github.com/pingcap/tidb/issues/25200)に変換する間違った関数を修正
    -   非同期ロガー[＃8998](https://github.com/tikv/tikv/issues/8998)使用時にpanicログが失われる可能性がある問題を修正
    -   暗号化が有効になっている場合にスナップショットを2回構築すると発生するpanic問題を修正[＃9786](https://github.com/tikv/tikv/issues/9786) [＃10407](https://github.com/tikv/tikv/issues/10407)
    -   コプロセッサ[＃10176](https://github.com/tikv/tikv/issues/10176)の関数`json_unquote()`の間違った引数の型を修正
    -   シャットダウン時の疑わしい警告とRaftstore [＃10353](https://github.com/tikv/tikv/issues/10353) [＃10307](https://github.com/tikv/tikv/issues/10307)からの非決定的な応答の問題を修正しました
    -   バックアップスレッドリークの問題を修正[＃10287](https://github.com/tikv/tikv/issues/10287)
    -   分割プロセスが遅すぎてリージョンのマージが進行中の場合、リージョン分割がpanicてメタデータが破損する可能性がある問題を修正しました[＃8456](https://github.com/tikv/tikv/issues/8456) [＃8783](https://github.com/tikv/tikv/issues/8783)
    -   リージョンハートビートにより、TiKV が特定の状況で大規模なリージョンを分割できない問題を修正[＃10111](https://github.com/tikv/tikv/issues/10111)
    -   TiKVとTiDB [＃25638](https://github.com/pingcap/tidb/issues/25638)間のCMスケッチの形式の不一致によって発生した誤った統計を修正しました
    -   `apply wait duration`メトリック[＃9893](https://github.com/tikv/tikv/issues/9893)の誤った統計を修正
    -   Titan [＃10232](https://github.com/tikv/tikv/pull/10232)で`delete_files_in_range`使用した後に発生する「Missing Blob」エラーを修正

-   PD

    -   削除操作を実行した後にスケジューラが再表示されることがあるバグを修正[＃2572](https://github.com/tikv/pd/issues/2572)
    -   一時構成がロードされる前にスケジューラが起動されたときに発生する可能性のあるデータ競合の問題を修正しました[＃3771](https://github.com/tikv/pd/issues/3771)
    -   リージョン分散操作中に発生する可能性のあるPDpanic問題を修正しました[＃3761](https://github.com/pingcap/pd/pull/3761)
    -   一部の演算子の優先順位が正しく設定されていない問題を修正[＃3703](https://github.com/pingcap/pd/pull/3703)
    -   存在しないストア[＃3660](https://github.com/tikv/pd/issues/3660)から`evict-leader`スケジューラを削除するときに発生する可能性のある PDpanicの問題を修正しました。
    -   店舗数が多い場合にPDLeaderの再選出が遅くなる問題を修正[＃3697](https://github.com/tikv/pd/issues/3697)

-   TiDBダッシュボード

    -   **プロファイリング**UIがすべてのTiDBインスタンスをプロファイリングできない問題を修正[＃944](https://github.com/pingcap/tidb-dashboard/pull/944)
    -   **明細書**UIに「プラン数」が表示されない問題を修正しました[＃939](https://github.com/pingcap/tidb-dashboard/pull/939)
    -   クラスタアップグレード[＃902](https://github.com/pingcap/tidb-dashboard/issues/902)後に**スロークエリ**UIに「不明なフィールド」エラーが表示される問題を修正しました

-   TiFlash

    -   DAGリクエストをコンパイルする際に発生する可能性のあるpanic問題を修正しました
    -   読み取り負荷が大きい場合に発生するpanic問題を修正しました
    -   列storageの分割失敗によりTiFlashが再起動し続ける問題を修正しました
    -   TiFlashがデルタデータを削除できない潜在的なバグを修正
    -   共有デルタインデックスを同時に複製するときに発生する誤った結果を修正しました
    -   データが不完全な場合にTiFlashが再起動に失敗するバグを修正
    -   古いdmファイルが自動的に削除されない問題を修正しました
    -   特定の引数で`SUBSTRING`関数を実行したときに発生するpanic問題を修正しました
    -   `INTEGER`型を`TIME`型にキャストしたときに結果が不正確になる問題を修正しました

-   ツール

    -   バックアップと復元 (BR)

        -   `mysql`スキーマからのデータ復元が失敗する可能性がある問題を修正[＃1142](https://github.com/pingcap/br/pull/1142)

    -   TiDB Lightning

        -   TiDB LightningがParquetファイル[＃1276](https://github.com/pingcap/br/pull/1276)の`DECIMAL`型データを解析できない問題を修正
        -   TiDB Lightningがインポートした大きなCSVファイルを分割する際に報告されるEOFエラーを修正しました[＃1133](https://github.com/pingcap/br/issues/1133)
        -   TiDB Lightningが`FLOAT`または`DOUBLE`タイプの`auto_increment`列目を持つテーブルをインポートするときに過度に大きなベース値が生成されるバグを修正しました[＃1185](https://github.com/pingcap/br/pull/1185)
        -   4 GBを超えるKVデータを生成する際に発生するTiDB Lightningpanicの問題を修正[＃1128](https://github.com/pingcap/br/pull/1128)

    -   Dumpling

        -   Dumplingを使用してS3storageにデータをエクスポートする場合、バケット全体に対する`s3:ListBucket`権限は不要になりました。この権限はデータソースプレフィックスに対してのみ必要です[＃898](https://github.com/pingcap/br/issues/898)

    -   TiCDC

        -   新しいテーブルパーティションを追加した後に余分なパーティションがディスパッチされる問題を修正[＃2205](https://github.com/pingcap/tiflow/pull/2205)
        -   TiCDCが`/proc/meminfo` [＃2023](https://github.com/pingcap/tiflow/pull/2023)の読み取りに失敗した場合に発生するpanic問題を修正しました
        -   TiCDC のランタイムメモリ消費を削減する[#2011](https://github.com/pingcap/tiflow/pull/2011) [＃1957](https://github.com/pingcap/tiflow/pull/1957)
        -   MySQLシンクがエラーに遭遇して一時停止した後に、一部のMySQL接続がリークする可能性があるバグを修正しました[＃1945](https://github.com/pingcap/tiflow/pull/1945)
        -   開始 TS が現在の TS から GC TTL [＃1839](https://github.com/pingcap/tiflow/issues/1839)を引いた値より小さい場合、TiCDC チェンジフィードを作成できない問題を修正しました。
        -   過度のCPUオーバーヘッドを避けるためにソートヒープのメモリ`malloc`を減らす[＃1853](https://github.com/pingcap/tiflow/issues/1853)
        -   テーブル[＃1827](https://github.com/pingcap/tiflow/pull/1827)移動する際にレプリケーションタスクが停止する可能性があるバグを修正
