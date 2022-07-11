---
title: TiDB 4.0.2 Release Notes
---

# TiDB4.0.2リリースノート {#tidb-4-0-2-release-notes}

発売日：2020年7月1日

TiDBバージョン：4.0.2

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   低速クエリログとステートメントサマリーテーブル[＃18130](https://github.com/pingcap/tidb/pull/18130)の機密情報を削除します
    -   シーケンスキャッシュ[＃18103](https://github.com/pingcap/tidb/pull/18103)で負の値を禁止する
    -   `CLUSTER_INFO`のテーブルからトゥームストーンTiKVおよびTiFlashストアを削除します[＃17953](https://github.com/pingcap/tidb/pull/17953)
    -   診断ルールを`current-load`から[＃17660](https://github.com/pingcap/tidb/pull/17660)に変更し`node-check`

-   PD

    -   `store-limit`を永続化し、 [＃2557](https://github.com/pingcap/pd/pull/2557)を削除し`store-balance-rate`

## 新しい変更 {#new-change}

-   デフォルトでは、TiDBおよびTiDBダッシュボードは使用法の詳細をPingCAPと共有して、製品を改善する方法を理解するのに役立ちます[＃18180](https://github.com/pingcap/tidb/pull/18180) 。共有される内容と共有を無効にする方法の詳細については、 [テレメトリー](/telemetry.md)を参照してください。

## 新機能 {#new-features}

-   TiDB

    -   `INSERT`のステートメントで`MEMORY_QUOTA()`のヒントをサポートする[＃18101](https://github.com/pingcap/tidb/pull/18101)
    -   TLS証明書の`SAN`フィールドに基づく認証をサポート[＃17698](https://github.com/pingcap/tidb/pull/17698)
    -   `REGEXP()`関数[＃17581](https://github.com/pingcap/tidb/pull/17581)の照合順序をサポートします
    -   `sql_select_limit`セッションとグローバル変数[＃17604](https://github.com/pingcap/tidb/pull/17604)をサポートします
    -   デフォルトで新しく追加されたパーティションのリージョンの分割をサポート[＃17665](https://github.com/pingcap/tidb/pull/17665)
    -   `BITXOR()`関数の`IF()` `BITNEG()` `JSON_LENGTH()`への[＃17592](https://github.com/pingcap/tidb/pull/17592)をサポート[＃17651](https://github.com/pingcap/tidb/pull/17651)
    -   `COUNT(DISTINCT)` [＃18120](https://github.com/pingcap/tidb/pull/18120)の近似結果を計算するために、新しい集計関数`APPROX_COUNT_DISTINCT()`をサポートします。
    -   TiFlashでの照合順序をサポートし、照合関連関数を[＃17705](https://github.com/pingcap/tidb/pull/17705)にプッシュします。
    -   サーバー[＃17695](https://github.com/pingcap/tidb/pull/17695)のステータスアドレスを示すために、 `INFORMATION_SCHEMA.INSPECTION_RESULT`のテーブルに`STATUS_ADDRESS`の列を追加します。
    -   `MYSQL.BIND_INFO`テーブルに`SOURCE`列を追加して、バインディングがどのように作成されるかを示します[＃17587](https://github.com/pingcap/tidb/pull/17587)
    -   `PERFORMANCE_SCHEMA.EVENTS_STATEMENTS_SUMMARY_BY_DIGEST`テーブルに`PLAN_IN_CACHE`列と`PLAN_CACHE_HITS`列を追加して、SQLステートメントのプランキャッシュ使用量を示します[＃17493](https://github.com/pingcap/tidb/pull/17493)
    -   `enable-collect-execution-info`の構成アイテムと`tidb_enable_collect_execution_info`のセッション変数を追加して、各オペレーターの実行情報を収集し、その情報を低速クエリログに記録するかどうかを制御します[＃18073](https://github.com/pingcap/tidb/pull/18073) [＃18072](https://github.com/pingcap/tidb/pull/18072)
    -   `tidb_slow_log_masking`のグローバル変数を追加して、遅いクエリログ[＃17694](https://github.com/pingcap/tidb/pull/17694)のクエリの感度を下げるかどうかを制御します
    -   3TiKV構成アイテム`storage.block-cache.capacity`の`INFORMATION_SCHEMA.INSPECTION_RESULT`テーブルに診断ルールを追加し[＃17671](https://github.com/pingcap/tidb/pull/17671) 。
    -   `BACKUP`と`RESTORE`のSQLステートメントを追加して、データをバックアップおよび復元します[＃15274](https://github.com/pingcap/tidb/pull/15274)

-   TiKV

    -   TiKV Controlで`encryption-meta`コマンドを[＃8103](https://github.com/tikv/tikv/pull/8103)する
    -   [＃7991](https://github.com/tikv/tikv/pull/7991)のパフォーマンスコンテキストメトリックを追加し`RocksDB::WriteImpl`

-   PD

    -   リーダーピア[＃2551](https://github.com/pingcap/pd/pull/2551)を削除しようとしたときに、オペレーターがすぐに失敗するようにサポートします。
    -   TiFlashストアに適切なデフォルトのストア制限を設定する[＃2559](https://github.com/pingcap/pd/pull/2559)

-   TiFlash

    -   コプロセッサーで新しい集計関数`APPROX_COUNT_DISTINCT`をサポートする
    -   デフォルトで`rough set filter`つの機能を有効にする
    -   TiFlashをARMアーキテクチャで実行できるようにする
    -   コプロセッサーの`JSON_LENGTH`関数のプッシュダウンをサポート

-   ツール

    -   TiCDC

        -   サブタスクの新しい`capture`秒[＃665](https://github.com/pingcap/tiflow/pull/665)への移行をサポート
        -   `cli`コマンドを追加して、TiCDC [＃652](https://github.com/pingcap/tiflow/pull/652)を削除します。
        -   MQシンク[＃649](https://github.com/pingcap/tiflow/pull/649)で運河プロトコルをサポート

## 改善 {#improvements}

-   TiDB

    -   CM-Sketchが大量のメモリを消費する場合にGolangのメモリ割り当てによって引き起こされるクエリの待ち時間を短縮する[＃17545](https://github.com/pingcap/tidb/pull/17545)
    -   TiKVサーバーが障害回復プロセスにある場合、クラスタのQPS回復期間を短縮します[＃17681](https://github.com/pingcap/tidb/pull/17681)
    -   パーティションテーブル[＃17655](https://github.com/pingcap/tidb/pull/17655)のTiKV/TiFlashコプロセッサーへの集約関数のプッシュをサポート
    -   インデックスが等しい条件の行数推定の精度を向上させる[＃17611](https://github.com/pingcap/tidb/pull/17611)

-   TiKV

    -   PDクライアントのpanicログを改善する[＃8093](https://github.com/tikv/tikv/pull/8093)
    -   `process_cpu_seconds_total`と`process_start_time_seconds`の監視メトリックを追加し直します[＃8029](https://github.com/tikv/tikv/pull/8029)

-   TiFlash

    -   古いバージョンからアップグレードする際の下位互換性を改善する[＃786](https://github.com/pingcap/tics/pull/786)
    -   デルタインデックス[＃787](https://github.com/pingcap/tics/pull/787)のメモリ消費を削減します
    -   デルタインデックス[＃794](https://github.com/pingcap/tics/pull/794)にはより効率的な更新アルゴリズムを使用します

-   ツール

    -   バックアップと復元（BR）

        -   復元プロセスをパイプライン化してパフォーマンスを向上させる[＃266](https://github.com/pingcap/br/pull/266)

## バグの修正 {#bug-fixes}

-   TiDB

    -   `tidb_isolation_read_engines`が変更された後にプランキャッシュから取得された誤った実行プランの問題を修正します[＃17570](https://github.com/pingcap/tidb/pull/17570)
    -   `EXPLAIN FOR CONNECTION`ステートメント[＃18124](https://github.com/pingcap/tidb/pull/18124)の実行時に発生するときどき発生するランタイムエラーを修正します。
    -   場合によっては`last_plan_from_cache`セッション変数の誤った結果を修正します[＃18111](https://github.com/pingcap/tidb/pull/18111)
    -   プランキャッシュから`UNIX_TIMESTAMP()`関数を実行するときに発生するランタイムエラーを修正し[＃18002](https://github.com/pingcap/tidb/pull/18002) [＃17673](https://github.com/pingcap/tidb/pull/17673)
    -   `HashJoin`のエグゼキュータの子が`NULL`列[＃17937](https://github.com/pingcap/tidb/pull/17937)を返すときのランタイムエラーを修正します
    -   同じデータベースで`DROP DATABASE`ステートメントと他のDDLステートメントを同時に実行することによって発生するランタイムエラーを修正します[＃17659](https://github.com/pingcap/tidb/pull/17659)
    -   ユーザー変数[＃17890](https://github.com/pingcap/tidb/pull/17890)の`COERCIBILITY()`関数の誤った結果を修正します
    -   `IndexMergeJoin`エグゼキュータがときどきスタックする問題を修正します[＃18091](https://github.com/pingcap/tidb/pull/18091)
    -   メモリクォータが不足し、クエリのキャンセルがトリガーされた場合の`IndexMergeJoin`エグゼキュータのハングの問題を修正します[＃17654](https://github.com/pingcap/tidb/pull/17654)
    -   `Insert`および`Replace`エグゼキュータの過剰なカウントメモリ使用量を修正します[＃18062](https://github.com/pingcap/tidb/pull/18062)
    -   同じデータベースで`DROP DATABASE`と`DROP TABLE`が同時に実行されると、TiFlashストレージへのデータレプリケーションが停止する問題を修正します[＃17901](https://github.com/pingcap/tidb/pull/17901)
    -   TiDBとオブジェクトストレージサービス`RESTORE`の間の`BACKUP`障害を修正し[＃17844](https://github.com/pingcap/tidb/pull/17844)
    -   アクセスが拒否されたときに特権チェックが失敗するという誤ったエラーメッセージを修正します[＃17724](https://github.com/pingcap/tidb/pull/17724)
    -   `DELETE`ステートメントから生成されたクエリフィードバックを破棄し[＃17843](https://github.com/pingcap/tidb/pull/17843) `UPDATE`
    -   `AUTO_RANDOM`のプロパティがないテーブルの`AUTO_RANDOM_BASE`を変更することを禁止します[＃17828](https://github.com/pingcap/tidb/pull/17828)
    -   テーブルがデータベース間で[＃18243](https://github.com/pingcap/tidb/pull/18243)移動すると、 `AUTO_RANDOM`列に誤った結果が割り当てられる問題を修正し`ALTER TABLE ... RENAME` 。
    -   [＃17719](https://github.com/pingcap/tidb/pull/17719)なしで`tidb_isolation_read_engines`の値を設定すると、一部のシステムテーブルにアクセスできない問題を修正し`tidb` 。
    -   大きな整数と浮動小数点値でのJSON比較の不正確な結果を修正します[＃17717](https://github.com/pingcap/tidb/pull/17717)
    -   `COUNT()`関数[＃17704](https://github.com/pingcap/tidb/pull/17704)の結果の誤ったdecimalプロパティを修正します
    -   入力のタイプがバイナリ文字列[＃17620](https://github.com/pingcap/tidb/pull/17620)の場合の`HEX()`関数の誤った結果を修正します
    -   フィルタ条件[＃17697](https://github.com/pingcap/tidb/pull/17697)なしで`INFORMATION_SCHEMA.INSPECTION_SUMMARY`テーブルをクエリすると、空の結果が返される問題を修正します。
    -   `ALTER USER`ステートメントがユーザー情報を更新するために使用するハッシュパスワードが予期しないものであるという問題を修正します[＃17646](https://github.com/pingcap/tidb/pull/17646)
    -   `ENUM`と`SET`の値の照合順序をサポート[＃17701](https://github.com/pingcap/tidb/pull/17701)
    -   テーブル[＃17619](https://github.com/pingcap/tidb/pull/17619)を作成するときに、リージョンを事前分割するためのタイムアウトメカニズムが機能しない問題を修正します。
    -   DDLジョブが再試行されたときにスキーマが予期せず更新され、DDLジョブのアトミック性が損なわれる可能性があるという問題を修正します[＃17608](https://github.com/pingcap/tidb/pull/17608)
    -   引数に列[＃17562](https://github.com/pingcap/tidb/pull/17562)が含まれている場合の`FIELD()`関数の誤った結果を修正します
    -   `max_execution_time`ヒントがときどき機能しない問題を修正します[＃17536](https://github.com/pingcap/tidb/pull/17536)
    -   13の結果で同時実行情報が冗長に`EXPLAIN ANALYZE`される問題を修正し[＃17350](https://github.com/pingcap/tidb/pull/17350)
    -   `STR_TO_DATE`関数[＃17498](https://github.com/pingcap/tidb/pull/17498)の`%h`の互換性のない動作を修正します
    -   `tidb_replica_read`が`follower`に設定されていて、リーダーとフォロワー/学習者の間にネットワークパーティションがある場合に、フォロワー/学習者が再試行し続ける問題を修正します[＃17443](https://github.com/pingcap/tidb/pull/17443)
    -   TiDBがPDフォロワーに送信するpingが多すぎる場合がある問題を修正します[＃17947](https://github.com/pingcap/tidb/pull/17947)
    -   古いバージョンの範囲パーティションテーブルを[＃17983](https://github.com/pingcap/tidb/pull/17983)にロードできない問題を修正します。
    -   リージョン[＃17585](https://github.com/pingcap/tidb/pull/17585)ごとに異なる`Backoffer`を割り当てることにより、複数のリージョンリクエストが同時に失敗した場合のSQLステートメントのタイムアウトの問題を修正します。
    -   `DateTime`の区切り文字を解析するときのMySQLの互換性のない動作を修正します[＃17501](https://github.com/pingcap/tidb/pull/17501)
    -   TiKVリクエストがTiFlashサーバーに送信されることがある問題を修正します[＃18105](https://github.com/pingcap/tidb/pull/18105)
    -   あるトランザクションで書き込まれ、削除された主キーのロックが別のトランザクションによって解決されるために発生したデータの不整合の問題を修正します[＃18250](https://github.com/pingcap/tidb/pull/18250)

-   TiKV

    -   ステータスサーバー[＃8101](https://github.com/tikv/tikv/pull/8101)のメモリ安全性の問題を修正します
    -   JSON数値比較で精度が失われる問題を修正[＃8087](https://github.com/tikv/tikv/pull/8087)
    -   間違ったクエリの遅いログを修正する[＃8050](https://github.com/tikv/tikv/pull/8050)
    -   複数のマージプロセス中にストアが分離されている場合にピアを削除できない問題を修正します[＃8048](https://github.com/tikv/tikv/pull/8048)
    -   `tikv-ctl recover-mvcc`が無効な悲観的ロックを削除しないという問題を修正します[＃8047](https://github.com/tikv/tikv/pull/8047)
    -   一部のTitanヒストグラムメトリックが欠落している問題を修正します[＃7997](https://github.com/tikv/tikv/pull/7997)
    -   TiKVが`duplicated error`をTiCDC3に返す問題を修正し[＃7887](https://github.com/tikv/tikv/pull/7887)

-   PD

    -   `pd-server.dashboard-address`構成項目[＃2517](https://github.com/pingcap/pd/pull/2517)の正しさを確認してください
    -   `store-limit-mode`を[＃2544](https://github.com/pingcap/pd/pull/2544)に設定するときのPDのpanicの問題を修正し`auto`
    -   場合によってはホットスポットを特定できない問題を修正します[＃2463](https://github.com/pingcap/pd/pull/2463)
    -   配置ルールにより、ストアが`tombstone`に変更されない場合があるという問題を修正します[＃2546](https://github.com/pingcap/pd/pull/2546)
    -   場合によっては、以前のバージョンからアップグレードするときのPDのpanicの問題を修正します[＃2564](https://github.com/pingcap/pd/pull/2564)

-   TiFlash

    -   `region not found`エラーが発生したときにプロキシがpanicになる可能性がある問題を修正します
    -   `drop table`でスローされたI/O例外がTiFlashスキーマの同期エラーにつながる可能性がある問題を修正します
