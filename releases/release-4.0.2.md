---
title: TiDB 4.0.2 Release Notes
---

# TiDB 4.0.2 リリースノート {#tidb-4-0-2-release-notes}

発売日：2020年7月1日

TiDB バージョン: 4.0.2

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   スロークエリログとステートメント概要テーブル[#18130](https://github.com/pingcap/tidb/pull/18130)の機密情報を削除します。
    -   シーケンス キャッシュ[#18103](https://github.com/pingcap/tidb/pull/18103)での負の値の禁止
    -   トゥームストーン TiKV およびTiFlashストアを`CLUSTER_INFO`テーブル[#17953](https://github.com/pingcap/tidb/pull/17953)から削除します。
    -   診断ルールを`current-load`から`node-check`に変更します[#17660](https://github.com/pingcap/tidb/pull/17660)

-   PD

    -   `store-limit`を保持し、 `store-balance-rate`を削除します[#2557](https://github.com/pingcap/pd/pull/2557)

## 新しい変化 {#new-change}

-   デフォルトでは、TiDB と TiDB ダッシュボードは使用状況の詳細を PingCAP と共有し、製品の改善方法を理解するのに役立ちます[#18180](https://github.com/pingcap/tidb/pull/18180) 。共有内容と共有を無効にする方法については、 [テレメトリー](/telemetry.md)を参照してください。

## 新機能 {#new-features}

-   TiDB

    -   `INSERT`ステートメントで`MEMORY_QUOTA()`ヒントをサポート[#18101](https://github.com/pingcap/tidb/pull/18101)
    -   TLS 証明書の`SAN`フィールドに基づく認証をサポート[#17698](https://github.com/pingcap/tidb/pull/17698)
    -   `REGEXP()`関数[#17581](https://github.com/pingcap/tidb/pull/17581)の照合順序のサポート
    -   `sql_select_limit`セッションとグローバル変数[#17604](https://github.com/pingcap/tidb/pull/17604)をサポート
    -   新しく追加されたパーティションのリージョン分割をデフォルトでサポートします[#17665](https://github.com/pingcap/tidb/pull/17665)
    -   `IF()` / `BITXOR()` / `BITNEG()` / `JSON_LENGTH()`関数のTiFlashコプロセッサーへのプッシュをサポート[#17651](https://github.com/pingcap/tidb/pull/17651) [#17592](https://github.com/pingcap/tidb/pull/17592)
    -   `COUNT(DISTINCT)` [#18120](https://github.com/pingcap/tidb/pull/18120)の近似結果を計算するための新しい集計関数`APPROX_COUNT_DISTINCT()`サポートします。
    -   TiFlashでの照合順序をサポートし、照合関連の関数をTiFlash [#17705](https://github.com/pingcap/tidb/pull/17705)にプッシュ
    -   サーバー[#17695](https://github.com/pingcap/tidb/pull/17695)のステータス アドレスを示すために、テーブル`INFORMATION_SCHEMA.INSPECTION_RESULT`に`STATUS_ADDRESS`列を追加します。
    -   `MYSQL.BIND_INFO`テーブルに`SOURCE`列を追加して、バインディングの作成方法を示します[#17587](https://github.com/pingcap/tidb/pull/17587)
    -   `PERFORMANCE_SCHEMA.EVENTS_STATEMENTS_SUMMARY_BY_DIGEST`テーブルに`PLAN_IN_CACHE`と`PLAN_CACHE_HITS`列を追加して、SQL ステートメントのプラン キャッシュの使用量を示します[#17493](https://github.com/pingcap/tidb/pull/17493)
    -   各オペレーターの実行情報を収集し、スロークエリログに情報を記録するかどうかを制御するための`enable-collect-execution-info`構成アイテムと`tidb_enable_collect_execution_info`セッション変数を追加します[#18073](https://github.com/pingcap/tidb/pull/18073) [#18072](https://github.com/pingcap/tidb/pull/18072)
    -   `tidb_slow_log_masking`グローバル変数を追加して、低速クエリ ログ[#17694](https://github.com/pingcap/tidb/pull/17694)のクエリを鈍感にするかどうかを制御します。
    -   `INFORMATION_SCHEMA.INSPECTION_RESULT`テーブルに`storage.block-cache.capacity` TiKV 構成項目[#17671](https://github.com/pingcap/tidb/pull/17671)の診断ルールを追加します。
    -   データをバックアップおよび復元するために`BACKUP`および`RESTORE` SQL ステートメントを追加します[#15274](https://github.com/pingcap/tidb/pull/15274)

-   TiKV

    -   TiKV Control [#8103](https://github.com/tikv/tikv/pull/8103)の`encryption-meta`コマンドをサポート
    -   `RocksDB::WriteImpl` [#7991](https://github.com/tikv/tikv/pull/7991)のパフォーマンス コンテキスト メトリックを追加します

-   PD

    -   オペレーターがリーダー ピア[#2551](https://github.com/pingcap/pd/pull/2551)を削除しようとするときにすぐに失敗するようにサポートします。
    -   TiFlashストアに適切なデフォルトのストア制限を設定します[#2559](https://github.com/pingcap/pd/pull/2559)

-   TiFlash

    -   コプロセッサーで新しい集計関数`APPROX_COUNT_DISTINCT`をサポート
    -   `rough set filter`機能をデフォルトで有効にする
    -   TiFlash をARMアーキテクチャ上で実行できるようにする
    -   コプロセッサーの`JSON_LENGTH`関数のプッシュダウンをサポート

-   ツール

    -   TiCDC

        -   新しい`capture` s [#665](https://github.com/pingcap/tiflow/pull/665)へのサブタスクの移行をサポート
        -   TiCDC GC TTL [#652](https://github.com/pingcap/tiflow/pull/652)を削除する`cli`コマンドを追加します。
        -   MQ シンク[#649](https://github.com/pingcap/tiflow/pull/649)でカナルプロトコルをサポート

## 改善点 {#improvements}

-   TiDB

    -   CM-Sketch が大量のメモリを消費する場合に、 Golang のメモリ割り当てによって引き起こされるクエリのレイテンシーを削減します[#17545](https://github.com/pingcap/tidb/pull/17545)
    -   TiKVサーバーが障害回復プロセス中の場合、クラスターの QPS 回復時間を短縮します[#17681](https://github.com/pingcap/tidb/pull/17681)
    -   パーティション テーブル[#17655](https://github.com/pingcap/tidb/pull/17655)上の TiKV/ TiFlashコプロセッサーへの集計関数のプッシュのサポート
    -   インデックス等しい条件[#17611](https://github.com/pingcap/tidb/pull/17611)の行数推定の精度を向上させます。

-   TiKV

    -   PDクライアントpanicログ[#8093](https://github.com/tikv/tikv/pull/8093)の改善
    -   `process_cpu_seconds_total`と`process_start_time_seconds`監視メトリクスを再度追加します[#8029](https://github.com/tikv/tikv/pull/8029)

-   TiFlash

    -   古いバージョンからアップグレードする場合の下位互換性を向上[#786](https://github.com/pingcap/tics/pull/786)
    -   デルタインデックス[#787](https://github.com/pingcap/tics/pull/787)のメモリ消費量を削減します。
    -   デルタ インデックス[#794](https://github.com/pingcap/tics/pull/794)には、より効率的な更新アルゴリズムを使用します。

-   ツール

    -   バックアップと復元 (BR)

        -   復元プロセスをパイプライン化してパフォーマンスを向上させる[#266](https://github.com/pingcap/br/pull/266)

## バグの修正 {#bug-fixes}

-   TiDB

    -   `tidb_isolation_read_engines`を変更した後、プラン キャッシュから取得された実行プランが正しくなくなる問題を修正[#17570](https://github.com/pingcap/tidb/pull/17570)
    -   `EXPLAIN FOR CONNECTION`ステートメント[#18124](https://github.com/pingcap/tidb/pull/18124)の実行時に時折発生するランタイム エラーを修正しました。
    -   場合によっては`last_plan_from_cache`セッション変数の誤った結果が修正される[#18111](https://github.com/pingcap/tidb/pull/18111)
    -   プラン キャッシュ[#18002](https://github.com/pingcap/tidb/pull/18002) [#17673](https://github.com/pingcap/tidb/pull/17673)から`UNIX_TIMESTAMP()`関数を実行するときに発生するランタイム エラーを修正します。
    -   `HashJoin`エグゼキューターの子が`NULL`列[#17937](https://github.com/pingcap/tidb/pull/17937)を返すときのランタイム エラーを修正しました。
    -   同じデータベース[#17659](https://github.com/pingcap/tidb/pull/17659)内で`DROP DATABASE`ステートメントと他の DDL ステートメントを同時に実行することによって発生するランタイム エラーを修正します。
    -   ユーザー変数[#17890](https://github.com/pingcap/tidb/pull/17890)に対する関数`COERCIBILITY()`の誤った結果を修正しました。
    -   `IndexMergeJoin` executor が時々スタックする問題を修正[#18091](https://github.com/pingcap/tidb/pull/18091)
    -   メモリクォータが不足し、クエリのキャンセルがトリガーされたときの`IndexMergeJoin`エグゼキュータのハングの問題を修正します[#17654](https://github.com/pingcap/tidb/pull/17654)
    -   `Insert`および`Replace`エグゼキュータの過剰なカウントメモリ使用量を修正する[#18062](https://github.com/pingcap/tidb/pull/18062)
    -   `DROP DATABASE`と`DROP TABLE`を同じデータベースで同時に実行すると、 TiFlashstorageへのデータレプリケーションが停止する問題を修正[#17901](https://github.com/pingcap/tidb/pull/17901)
    -   TiDB `RESTORE`オブジェクトstorageサービス間の`BACKUP`障害を修正[#17844](https://github.com/pingcap/tidb/pull/17844)
    -   アクセスが拒否された場合の権限チェック失敗の誤ったエラー メッセージを修正[#17724](https://github.com/pingcap/tidb/pull/17724)
    -   `DELETE` / `UPDATE`ステートメントから生成されたクエリ フィードバックを破棄します[#17843](https://github.com/pingcap/tidb/pull/17843)
    -   `AUTO_RANDOM`プロパティ[#17828](https://github.com/pingcap/tidb/pull/17828)のないテーブルの`AUTO_RANDOM_BASE`の変更を禁止する
    -   テーブルをデータベース間で`ALTER TABLE ... RENAME` [#18243](https://github.com/pingcap/tidb/pull/18243)移動すると、 `AUTO_RANDOM`列が誤った結果として割り当てられる問題を修正
    -   `tidb` [#17719](https://github.com/pingcap/tidb/pull/17719)を指定せずに`tidb_isolation_read_engines`の値を設定すると、一部のシステム テーブルにアクセスできない問題を修正
    -   大きな整数と浮動小数点値に対する JSON 比較の不正確な結果を修正しました[#17717](https://github.com/pingcap/tidb/pull/17717)
    -   `COUNT()`関数[#17704](https://github.com/pingcap/tidb/pull/17704)の結果の誤った 10 進数プロパティを修正しました。
    -   入力の型がバイナリ文字列[#17620](https://github.com/pingcap/tidb/pull/17620)の場合、 `HEX()`関数の誤った結果を修正しました。
    -   フィルター条件[#17697](https://github.com/pingcap/tidb/pull/17697)なしで`INFORMATION_SCHEMA.INSPECTION_SUMMARY`テーブルをクエリすると空の結果が返される問題を修正
    -   ユーザー情報を更新するための`ALTER USER`ステートメントで使用されるハッシュ化されたパスワードが予期しないものである問題を修正します[#17646](https://github.com/pingcap/tidb/pull/17646)
    -   `ENUM`および`SET`値の照合順序をサポート[#17701](https://github.com/pingcap/tidb/pull/17701)
    -   テーブル[#17619](https://github.com/pingcap/tidb/pull/17619)の作成時にリージョンの事前分割のタイムアウト メカニズムが機能しない問題を修正します。
    -   DDL ジョブの再試行時にスキーマが予期せず更新され、DDL ジョブのアトミック性が損なわれる可能性がある問題を修正します[#17608](https://github.com/pingcap/tidb/pull/17608)
    -   引数に列[#17562](https://github.com/pingcap/tidb/pull/17562)含まれる場合の`FIELD()`関数の誤った結果を修正しました。
    -   `max_execution_time`ヒントが時々機能しない問題を修正[#17536](https://github.com/pingcap/tidb/pull/17536)
    -   `EXPLAIN ANALYZE` [#17350](https://github.com/pingcap/tidb/pull/17350)の結果に同時実行情報が重複して出力される問題を修正
    -   `STR_TO_DATE`関数[#17498](https://github.com/pingcap/tidb/pull/17498)の`%h`の互換性のない動作を修正しました。
    -   `tidb_replica_read`を`follower`に設定し、リーダーとフォロワー/ラーナーの間にネットワーク パーティションがある場合、フォロワー/ラーナーがリトライを繰り返す問題を修正[#17443](https://github.com/pingcap/tidb/pull/17443)
    -   場合によっては TiDB が PD フォロワーに多すぎる ping を送信する問題を修正します[#17947](https://github.com/pingcap/tidb/pull/17947)
    -   TiDB v4.0 [#17983](https://github.com/pingcap/tidb/pull/17983)で古いバージョンのレンジ パーティション テーブルをロードできない問題を修正
    -   リージョン[#17585](https://github.com/pingcap/tidb/pull/17585)ごとに異なる`Backoffer`を割り当てることで、複数のリージョンリクエストが同時に失敗した場合の SQL ステートメントのタイムアウトの問題を修正します。
    -   `DateTime`区切り文字[#17501](https://github.com/pingcap/tidb/pull/17501)を解析するときの MySQL の互換性のない動作を修正しました。
    -   TiKV リクエストが時々 TiFlashサーバーに送信される問題を修正します[#18105](https://github.com/pingcap/tidb/pull/18105)
    -   あるトランザクションで書き込まれ削除された主キーのロックが別のトランザクションによって解決されるために発生するデータの不整合の問題を修正します[#18250](https://github.com/pingcap/tidb/pull/18250)

-   TiKV

    -   ステータスサーバー[#8101](https://github.com/tikv/tikv/pull/8101)のメモリの安全性の問題を修正します。
    -   JSON 数値比較[#8087](https://github.com/tikv/tikv/pull/8087)で精度が失われる問題を修正
    -   間違ったクエリの遅いログ[#8050](https://github.com/tikv/tikv/pull/8050)を修正する
    -   複数のマージ プロセス中にピアのストアが分離されている場合、ピアを削除できない問題を修正します[#8048](https://github.com/tikv/tikv/pull/8048)
    -   `tikv-ctl recover-mvcc`が無効な悲観的ロックを削除しない問題を修正します[#8047](https://github.com/tikv/tikv/pull/8047)
    -   一部の Titan ヒストグラム メトリクスが欠落している問題を修正[#7997](https://github.com/tikv/tikv/pull/7997)
    -   TiKV が TiCDC [#7887](https://github.com/tikv/tikv/pull/7887)に`duplicated error`を返す問題を修正

-   PD

    -   `pd-server.dashboard-address`設定項目が正しいか確認します[#2517](https://github.com/pingcap/pd/pull/2517)
    -   `store-limit-mode` ～ `auto` [#2544](https://github.com/pingcap/pd/pull/2544)設定時のPDのpanic問題を修正
    -   ホットスポットが特定できない場合がある問題を修正[#2463](https://github.com/pingcap/pd/pull/2463)
    -   場合によっては配置ルールによりストアが`tombstone`に変更されない問題を修正します[#2546](https://github.com/pingcap/pd/pull/2546)
    -   以前のバージョンからアップグレードする場合に発生する PD のpanic問題を修正[#2564](https://github.com/pingcap/pd/pull/2564)

-   TiFlash

    -   `region not found`エラーが発生したときにプロキシがpanicになる可能性がある問題を修正
    -   `drop table`でスローされた I/O 例外によりTiFlashスキーマの同期失敗が発生する可能性がある問題を修正
