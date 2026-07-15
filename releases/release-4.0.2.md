---
title: TiDB 4.0.2 Release Notes
summary: TiDB 4.0.2は2020年7月1日にリリースされました。この新バージョンには、互換性の変更、新機能、改善、バグ修正、そして新しい変更が含まれています。主な主な変更点としては、新しい集計関数のサポート、レイテンシーの改善、実行プラン、ランタイムエラー、データレプリケーションに関するバグ修正などが挙げられます。さらに、TiKV、PD、 TiFlash、ツールにも新機能と改善が加えられています。
---

# TiDB 4.0.2 リリースノート {#tidb-4-0-2-release-notes}

発売日：2020年7月1日

TiDB バージョン: 4.0.2

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   スロークエリログとステートメントサマリーテーブルから機密情報を削除します [＃18130](https://github.com/pingcap/tidb/pull/18130)
    -   シーケンスキャッシュの負の値を禁止する [＃18103](https://github.com/pingcap/tidb/pull/18103)
    -   `CLUSTER_INFO`テーブルから、Tombstone TiKV およびTiFlashストアを削除します。 [＃17953](https://github.com/pingcap/tidb/pull/17953)
    -   診断ルールを`current-load`から`node-check`に変更する[＃17660](https://github.com/pingcap/tidb/pull/17660)

-   PD

    -   `store-limit`を持続し、 `store-balance-rate` を削除 [＃2557](https://github.com/pingcap/pd/pull/2557)

## 新たな変化 {#new-change}

-   デフォルトでは、TiDBとTiDB Dashboardは、製品の改善方法を把握するために、PingCAPと使用状況の詳細を共有します共有される情報と共有を無効にする方法については、 [テレメトリー](/telemetry.md)ご覧ください。 [＃18180](https://github.com/pingcap/tidb/pull/18180)

## 新機能 {#new-features}

-   TiDB

    -   `INSERT`ステートメントの`MEMORY_QUOTA()`ヒントをサポートする[＃18101](https://github.com/pingcap/tidb/pull/18101)
    -   TLS証明書の`SAN`フィールドに基づく認証をサポート [＃17698](https://github.com/pingcap/tidb/pull/17698)
    -   `REGEXP()`関数照合順序をサポート [＃17581](https://github.com/pingcap/tidb/pull/17581)
    -   `sql_select_limit`セッションとグローバル変数サポート [＃17604](https://github.com/pingcap/tidb/pull/17604)
    -   新しく追加されたパーティションのリージョン分割をデフォルトでサポート[＃17665](https://github.com/pingcap/tidb/pull/17665)
    -   `IF()` / `BITXOR()` / `BITNEG()` / `JSON_LENGTH()`関数をTiFlashコプロセッサー にプッシュすることをサポート [＃17592](https://github.com/pingcap/tidb/pull/17592) [＃17651](https://github.com/pingcap/tidb/pull/17651)
    -   `COUNT(DISTINCT)` のおおよその結果を計算する新しい集計関数`APPROX_COUNT_DISTINCT()`サポートします。 [＃18120](https://github.com/pingcap/tidb/pull/18120)
    -   TiFlashでの照合順序をサポートし、照合関連の関数をTiFlash にプッシュします。 [＃17705](https://github.com/pingcap/tidb/pull/17705)
    -   `INFORMATION_SCHEMA.INSPECTION_RESULT`テーブルに`STATUS_ADDRESS`列を追加して、サーバのステータス アドレスを示します。 [＃17695](https://github.com/pingcap/tidb/pull/17695)
    -   `MYSQL.BIND_INFO`表に`SOURCE`列を追加して、バインディングの作成方法を示します[＃17587](https://github.com/pingcap/tidb/pull/17587)
    -   SQL文のプランキャッシュの使用状況を示すために、 `PERFORMANCE_SCHEMA.EVENTS_STATEMENTS_SUMMARY_BY_DIGEST`表に`PLAN_IN_CACHE`と`PLAN_CACHE_HITS`列を追加します。 [＃17493](https://github.com/pingcap/tidb/pull/17493)
    -   `enable-collect-execution-info`構成項目と`tidb_enable_collect_execution_info`セッション変数を追加して、各演算子の実行情報を収集し、その情報をスロークエリログ に記録するかどうかを制御します。 [＃18072](https://github.com/pingcap/tidb/pull/18072) [＃18073](https://github.com/pingcap/tidb/pull/18073)
    -   スロークエリログでクエリの感度を下げるかどうかを制御するグローバル変数`tidb_slow_log_masking`追加します。 [＃17694](https://github.com/pingcap/tidb/pull/17694)
    -   `storage.block-cache.capacity` TiKV構成項目[＃17671](https://github.com/pingcap/tidb/pull/17671) `INFORMATION_SCHEMA.INSPECTION_RESULT`テーブルに診断ルールを追加します。
    -   データのバックアップと復元を行うSQL文`BACKUP`と`RESTORE`を追加する[＃15274](https://github.com/pingcap/tidb/pull/15274)

-   TiKV

    -   TiKV Control の`encryption-meta`コマンドをサポート [＃8103](https://github.com/tikv/tikv/pull/8103)
    -   `RocksDB::WriteImpl` の perf コンテキスト メトリックを追加します。 [＃7991](https://github.com/tikv/tikv/pull/7991)

-   PD

    -   リーダーピアを削除しようとしたときにオペレータが直ちに失敗するようにサポートします。 [＃2551](https://github.com/pingcap/pd/pull/2551)
    -   TiFlashストアに適切なデフォルトのストア制限を設定する [＃2559](https://github.com/pingcap/pd/pull/2559)

-   TiFlash

    -   コプロセッサーで新しい集計関数`APPROX_COUNT_DISTINCT`サポート
    -   `rough set filter`機能をデフォルトで有効にする
    -   TiFlashをARMアーキテクチャ上で実行できるようにする
    -   コプロセッサーの`JSON_LENGTH`関数のプッシュダウンをサポート

-   ツール

    -   TiCDC

        -   サブタスクを新しい`capture` s に移行できるようにサポート [＃665](https://github.com/pingcap/tiflow/pull/665)
        -   TiCDC GC TTL を削除するコマンド`cli`を追加 [＃652](https://github.com/pingcap/tiflow/pull/652)
        -   MQシンクでチャネルプロトコルをサポート [＃649](https://github.com/pingcap/tiflow/pull/649)

## 改善点 {#improvements}

-   TiDB

    -   CM-Sketch がメモリを大量に消費する場合に、 Golangのメモリ割り当てによって発生するクエリのレイテンシーを削減します[＃17545](https://github.com/pingcap/tidb/pull/17545)
    -   TiKVサーバーが障害回復プロセスにあるときにクラスターのQPS回復時間を短縮する[＃17681](https://github.com/pingcap/tidb/pull/17681)
    -   パーティションテーブルの TiKV/ TiFlashコプロセッサーへの集計関数のプッシュをサポート [＃17655](https://github.com/pingcap/tidb/pull/17655)
    -   インデックスの等価条件の行数推定の精度を向上[＃17611](https://github.com/pingcap/tidb/pull/17611)

-   TiKV

    -   PDクライアントのpanicログ改善 [＃8093](https://github.com/tikv/tikv/pull/8093)
    -   `process_cpu_seconds_total`と`process_start_time_seconds`監視指標再度追加します [＃8029](https://github.com/tikv/tikv/pull/8029)

-   TiFlash

    -   旧バージョンからのアップグレード時の下位互換性の向上 [＃786](https://github.com/pingcap/tics/pull/786)
    -   デルタインデックスのメモリ消費量を削減 [＃787](https://github.com/pingcap/tics/pull/787)
    -   デルタインデックスに対してより効率的な更新アルゴリズムを使用する [＃794](https://github.com/pingcap/tics/pull/794)

-   ツール

    -   Backup & Restore (BR)

        -   復元プロセスをパイプライン化してパフォーマンスを向上させる[＃266](https://github.com/pingcap/br/pull/266)

## バグ修正 {#bug-fixes}

-   TiDB

    -   `tidb_isolation_read_engines`が変更された後にプランキャッシュから取得される実行プランが正しくない問題を修正[＃17570](https://github.com/pingcap/tidb/pull/17570)
    -   `EXPLAIN FOR CONNECTION`文を実行するときに時々発生するランタイムエラーを修正 [＃18124](https://github.com/pingcap/tidb/pull/18124)
    -   いくつかのケースで`last_plan_from_cache`セッション変数の誤った結果を修正[＃18111](https://github.com/pingcap/tidb/pull/18111)
    -   プランキャッシュ から`UNIX_TIMESTAMP()`関数を実行するときに発生するランタイムエラーを修正しました [＃17673](https://github.com/pingcap/tidb/pull/17673) [＃18002](https://github.com/pingcap/tidb/pull/18002)
    -   `HashJoin` Executor の子が`NULL`列返すときのランタイムエラーを修正しました [＃17937](https://github.com/pingcap/tidb/pull/17937)
    -   同じデータベースで`DROP DATABASE`文と他の DDL 文を同時に実行することによって発生する実行時エラーを修正します。 [＃17659](https://github.com/pingcap/tidb/pull/17659)
    -   ユーザー変数の関数`COERCIBILITY()`の誤った結果を修正 [＃17890](https://github.com/pingcap/tidb/pull/17890)
    -   `IndexMergeJoin`実行者が時々スタックする問題を修正[＃18091](https://github.com/pingcap/tidb/pull/18091)
    -   メモリクォータ不足とクエリキャンセルがトリガーされたときに`IndexMergeJoin`のエグゼキュータがハングする問題を修正[＃17654](https://github.com/pingcap/tidb/pull/17654)
    -   `Insert`と`Replace`エグゼキュータの過剰なカウントメモリ使用量を修正 [＃18062](https://github.com/pingcap/tidb/pull/18062)
    -   `DROP DATABASE`と`DROP TABLE`同じデータベースで同時に実行するとTiFlashストレージへのデータレプリケーションが停止する問題を修正 [＃17901](https://github.com/pingcap/tidb/pull/17901)
    -   TiDBとオブジェクトストレージサービスの`BACKUP` `RESTORE`障害を修正 [＃17844](https://github.com/pingcap/tidb/pull/17844)
    -   アクセスが拒否されたときに権限チェックに失敗したという誤ったエラーメッセージを修正しました[＃17724](https://github.com/pingcap/tidb/pull/17724)
    -   `DELETE`文から`UPDATE`されたクエリフィードバックを破棄する[＃17843](https://github.com/pingcap/tidb/pull/17843)
    -   `AUTO_RANDOM`プロパティのないテーブルでは`AUTO_RANDOM_BASE`変更を禁止します [＃17828](https://github.com/pingcap/tidb/pull/17828)
    -   テーブルを`ALTER TABLE ... RENAME` でデータベース間で移動したときに`AUTO_RANDOM`列が間違った結果が割り当てられる問題を修正 [＃18243](https://github.com/pingcap/tidb/pull/18243)
    -   `tidb` なしで`tidb_isolation_read_engines`の値を設定すると、一部のシステムテーブルにアクセスできない問題を修正しました。 [＃17719](https://github.com/pingcap/tidb/pull/17719)
    -   大きな整数と浮動小数点値に対する JSON 比較の不正確な結果を修正[＃17717](https://github.com/pingcap/tidb/pull/17717)
    -   `COUNT()`関数結果の小数点以下のプロパティが正しくない問題を修正しました [＃17704](https://github.com/pingcap/tidb/pull/17704)
    -   入力の型がバイナリ文字列の場合の`HEX()`関数の誤った結果を修正 [＃17620](https://github.com/pingcap/tidb/pull/17620)
    -   フィルタ条件なしで`INFORMATION_SCHEMA.INSPECTION_SUMMARY`テーブルをクエリすると空の結果が返される問題を修正 [＃17697](https://github.com/pingcap/tidb/pull/17697)
    -   `ALTER USER`ステートメントでユーザー情報を更新する際に使用されるハッシュ化されたパスワードが予期しないものである問題を修正[＃17646](https://github.com/pingcap/tidb/pull/17646)
    -   `ENUM`と`SET`値の照合順序をサポート[＃17701](https://github.com/pingcap/tidb/pull/17701)
    -   テーブル作成時にリージョンの事前分割のタイムアウトメカニズムが機能しない問題を修正しました [＃17619](https://github.com/pingcap/tidb/pull/17619)
    -   DDLジョブの再試行時にスキーマが予期せず更新され、DDLジョブのアトミック性が損なわれる可能性がある問題を修正しました[＃17608](https://github.com/pingcap/tidb/pull/17608)
    -   引数に列が含まれている場合の`FIELD()`関数の誤った結果を修正しました [＃17562](https://github.com/pingcap/tidb/pull/17562)
    -   `max_execution_time`ヒントが時々機能しない問題を修正[＃17536](https://github.com/pingcap/tidb/pull/17536)
    -   `EXPLAIN ANALYZE` の結果に同時実行情報が重複して出力される問題を修正しました [＃17350](https://github.com/pingcap/tidb/pull/17350)
    -   `STR_TO_DATE`関数の`%h`の非互換な動作を修正 [＃17498](https://github.com/pingcap/tidb/pull/17498)
    -   `tidb_replica_read` `follower`に設定され、リーダーとフォロワー/ラーナー間にネットワーク パーティションがある場合にフォロワー/ラーナーが再試行を続ける問題を修正しました。 [＃17443](https://github.com/pingcap/tidb/pull/17443)
    -   TiDBがPDフォロワーにpingを送信しすぎる場合がある問題を修正[＃17947](https://github.com/pingcap/tidb/pull/17947)
    -   TiDB v4.0 で古いバージョンの範囲パーティションテーブルをロードできない問題を修正しました [＃17983](https://github.com/pingcap/tidb/pull/17983)
    -   各リージョンに異なる`Backoffer`割り当てることで、複数のリージョン要求が同時に失敗した場合の SQL ステートメントのタイムアウト問題を修正しました[＃17585](https://github.com/pingcap/tidb/pull/17585)
    -   `DateTime`区切り文字を解析する際の MySQL 非互換の動作を修正 [＃17501](https://github.com/pingcap/tidb/pull/17501)
    -   TiKVリクエストがTiFlashサーバーに時々送信される問題を修正 [＃18105](https://github.com/pingcap/tidb/pull/18105)
    -   あるトランザクションで書き込まれ、削除された主キーのロックが別のトランザクションによって解決されたために発生したデータの不整合の問題を修正しました[＃18250](https://github.com/pingcap/tidb/pull/18250)

-   TiKV

    -   ステータスサーバーメモリ安全性の問題を修正 [＃8101](https://github.com/tikv/tikv/pull/8101)
    -   JSON数値比較で精度が失われる問題を修正 [＃8087](https://github.com/tikv/tikv/pull/8087)
    -   間違ったクエリのスローログを修正 [＃8050](https://github.com/tikv/tikv/pull/8050)
    -   複数のマージプロセス中にストアが分離されている場合にピアを削除できない問題を修正[＃8048](https://github.com/tikv/tikv/pull/8048)
    -   `tikv-ctl recover-mvcc`無効な悲観的ロックが削除されない問題を修正[＃8047](https://github.com/tikv/tikv/pull/8047)
    -   Titanヒストグラムのメトリックの一部が欠落している問題を修正[＃7997](https://github.com/tikv/tikv/pull/7997)
    -   TiKVがTiCDC に`duplicated error`返す問題を修正 [＃7887](https://github.com/tikv/tikv/pull/7887)

-   PD

    -   `pd-server.dashboard-address`構成項目の正確性を確認する [＃2517](https://github.com/pingcap/pd/pull/2517)
    -   `store-limit-mode`から`auto` に設定するとPDのpanic問題を修正 [＃2544](https://github.com/pingcap/pd/pull/2544)
    -   ホットスポットを識別できないことがある問題を修正[＃2463](https://github.com/pingcap/pd/pull/2463)
    -   配置ルールにより、ストアが`tombstone`に変更できない場合がある問題を修正しました場合) [＃2546](https://github.com/pingcap/pd/pull/2546)
    -   以前のバージョンからアップグレードする際に発生するPDのpanic問題を修正[＃2564](https://github.com/pingcap/pd/pull/2564)

-   TiFlash

    -   `region not found`エラーが発生したときにプロキシがpanic可能性がある問題を修正しました
    -   `drop table`でスローされた I/O 例外によりTiFlashスキーマの同期が失敗する可能性がある問題を修正しました
