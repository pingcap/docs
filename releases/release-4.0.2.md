---
title: TiDB 4.0.2 Release Notes
---

# TiDB 4.0.2 リリースノート {#tidb-4-0-2-release-notes}

発売日：2020年7月1日

TiDB バージョン: 4.0.2

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   スロー クエリ ログとステートメント サマリー テーブルの機密情報を削除します[#18130](https://github.com/pingcap/tidb/pull/18130)
    -   シーケンス キャッシュ[#18103](https://github.com/pingcap/tidb/pull/18103)で負の値を禁止する
    -   トゥームストーン TiKV およびTiFlashストアをテーブル`CLUSTER_INFO`から削除します[#17953](https://github.com/pingcap/tidb/pull/17953)
    -   診断ルールを`current-load`から`node-check` [#17660](https://github.com/pingcap/tidb/pull/17660)に変更します

-   PD

    -   `store-limit`永続化して`store-balance-rate` [#2557](https://github.com/pingcap/pd/pull/2557)を削除

## 新しい変更 {#new-change}

-   デフォルトでは、TiDB と TiDB ダッシュボードは使用状況の詳細を PingCAP と共有して、製品を改善する方法を理解するのに役立ちます[#18180](https://github.com/pingcap/tidb/pull/18180) 。共有される内容と共有を無効にする方法の詳細については、 [テレメトリー](/telemetry.md)参照してください。

## 新機能 {#new-features}

-   TiDB

    -   `INSERT`ステートメントで`MEMORY_QUOTA()`ヒントをサポートする[#18101](https://github.com/pingcap/tidb/pull/18101)
    -   TLS 証明書[#17698](https://github.com/pingcap/tidb/pull/17698)の`SAN`フィールドに基づく認証をサポート
    -   `REGEXP()`関数[#17581](https://github.com/pingcap/tidb/pull/17581)の照合順序をサポート
    -   `sql_select_limit`セッションとグローバル変数[#17604](https://github.com/pingcap/tidb/pull/17604)をサポート
    -   デフォルトで新しく追加されたパーティションのリージョン分割をサポート[#17665](https://github.com/pingcap/tidb/pull/17665)
    -   `IF()` / `BITXOR()` / `BITNEG()` / `JSON_LENGTH()`関数のTiFlashコプロセッサーへのプッシュをサポート[#17651](https://github.com/pingcap/tidb/pull/17651) [#17592](https://github.com/pingcap/tidb/pull/17592)
    -   `COUNT(DISTINCT)` [#18120](https://github.com/pingcap/tidb/pull/18120)のおおよその結果を計算する新しい集約関数`APPROX_COUNT_DISTINCT()`サポートします
    -   TiFlashでの照合順序をサポートし、照合関連の関数をTiFlash [#17705](https://github.com/pingcap/tidb/pull/17705)にプッシュ
    -   `INFORMATION_SCHEMA.INSPECTION_RESULT`テーブルに`STATUS_ADDRESS`列を追加して、サーバー[#17695](https://github.com/pingcap/tidb/pull/17695)のステータス アドレスを示します。
    -   `MYSQL.BIND_INFO`表に`SOURCE`列を追加して、バインディングの作成方法を示します[#17587](https://github.com/pingcap/tidb/pull/17587)
    -   `PERFORMANCE_SCHEMA.EVENTS_STATEMENTS_SUMMARY_BY_DIGEST`テーブルに`PLAN_IN_CACHE`と`PLAN_CACHE_HITS`列を追加して、SQL ステートメントのプラン キャッシュの使用状況を示します[#17493](https://github.com/pingcap/tidb/pull/17493)
    -   各オペレーターの実行情報を収集し、スロークエリログに情報を記録するかどうかを制御する`enable-collect-execution-info`構成項目と`tidb_enable_collect_execution_info`セッション変数を追加します[#18073](https://github.com/pingcap/tidb/pull/18073) [#18072](https://github.com/pingcap/tidb/pull/18072)
    -   `tidb_slow_log_masking`グローバル変数を追加して、スロー クエリ ログ[#17694](https://github.com/pingcap/tidb/pull/17694)でクエリの感度を下げるかどうかを制御します
    -   `storage.block-cache.capacity` TiKV 構成アイテム[#17671](https://github.com/pingcap/tidb/pull/17671)の`INFORMATION_SCHEMA.INSPECTION_RESULT`テーブルに診断ルールを追加します。
    -   `BACKUP`と`RESTORE` SQL ステートメントを追加して、データをバックアップおよび復元します[#15274](https://github.com/pingcap/tidb/pull/15274)

-   TiKV

    -   TiKV Control [#8103](https://github.com/tikv/tikv/pull/8103)の`encryption-meta`コマンドをサポート
    -   `RocksDB::WriteImpl` [#7991](https://github.com/tikv/tikv/pull/7991)のパフォーマンス コンテキスト メトリックを追加する

-   PD

    -   オペレーターがリーダー ピアを削除しようとするとすぐに失敗するようにサポートする[#2551](https://github.com/pingcap/pd/pull/2551)
    -   TiFlashストアに適切なデフォルト ストア制限を設定する[#2559](https://github.com/pingcap/pd/pull/2559)

-   TiFlash

    -   コプロセッサーでの新しい集計機能`APPROX_COUNT_DISTINCT`サポート
    -   デフォルトで`rough set filter`機能を有効にする
    -   TiFlash をARMアーキテクチャで実行できるようにする
    -   コプロセッサーでの`JSON_LENGTH`関数のプッシュダウンをサポート

-   ツール

    -   TiCDC

        -   サブタスクの新しい`capture`秒[#665](https://github.com/pingcap/tiflow/pull/665)への移行をサポート
        -   TiCDC GC TTL [#652](https://github.com/pingcap/tiflow/pull/652)を削除する`cli`コマンドを追加します。
        -   MQ シンク[#649](https://github.com/pingcap/tiflow/pull/649)で canal プロトコルをサポート

## 改良点 {#improvements}

-   TiDB

    -   CM-Sketch が大量のメモリを消費する場合に、 Golang のメモリ割り当てによって引き起こされるクエリのレイテンシーを削減します[#17545](https://github.com/pingcap/tidb/pull/17545)
    -   TiKVサーバーが障害回復プロセスにある場合、クラスターの QPS 回復期間を短縮します[#17681](https://github.com/pingcap/tidb/pull/17681)
    -   パーティション テーブル上の TiKV/ TiFlashコプロセッサーへの集約関数のプッシュをサポート[#17655](https://github.com/pingcap/tidb/pull/17655)
    -   インデックスが等しい条件の行数推定の精度を向上させる[#17611](https://github.com/pingcap/tidb/pull/17611)

-   TiKV

    -   PD クライアントのpanicログ[#8093](https://github.com/tikv/tikv/pull/8093)を改善します。
    -   `process_cpu_seconds_total`と`process_start_time_seconds`モニタリング メトリックを追加し直します[#8029](https://github.com/tikv/tikv/pull/8029)

-   TiFlash

    -   旧バージョンからのアップグレード時の後方互換性を向上[#786](https://github.com/pingcap/tics/pull/786)
    -   デルタ インデックス[#787](https://github.com/pingcap/tics/pull/787)のメモリ消費量を減らす
    -   デルタ インデックス[#794](https://github.com/pingcap/tics/pull/794)に対してより効率的な更新アルゴリズムを使用する

-   ツール

    -   バックアップと復元 (BR)

        -   復元プロセスをパイプライン化してパフォーマンスを向上させる[#266](https://github.com/pingcap/br/pull/266)

## バグの修正 {#bug-fixes}

-   TiDB

    -   `tidb_isolation_read_engines`を変更した後、プラン キャッシュから誤った実行プランを取得する問題を修正します[#17570](https://github.com/pingcap/tidb/pull/17570)
    -   `EXPLAIN FOR CONNECTION`ステートメント[#18124](https://github.com/pingcap/tidb/pull/18124)の実行時に時折発生するランタイム エラーを修正します。
    -   場合によっては`last_plan_from_cache`セッション変数の誤った結果を修正します[#18111](https://github.com/pingcap/tidb/pull/18111)
    -   プラン キャッシュから`UNIX_TIMESTAMP()`関数を実行するときに発生するランタイム エラーを修正します。 [#18002](https://github.com/pingcap/tidb/pull/18002) [#17673](https://github.com/pingcap/tidb/pull/17673)
    -   `HashJoin` executor の子が`NULL`列[#17937](https://github.com/pingcap/tidb/pull/17937)を返すときのランタイム エラーを修正します。
    -   同じデータベースで`DROP DATABASE`ステートメントと他の DDL ステートメントを同時に実行することによって発生するランタイム エラーを修正します[#17659](https://github.com/pingcap/tidb/pull/17659)
    -   ユーザー変数[#17890](https://github.com/pingcap/tidb/pull/17890)に対する`COERCIBILITY()`関数の誤った結果を修正します。
    -   `IndexMergeJoin`エグゼキュータが時々スタックする問題を修正[#18091](https://github.com/pingcap/tidb/pull/18091)
    -   メモリクォータが不足し、クエリのキャンセルがトリガーされた場合の`IndexMergeJoin` executor のハングの問題を修正します[#17654](https://github.com/pingcap/tidb/pull/17654)
    -   `Insert`および`Replace` executor の過剰なカウントメモリ使用量を修正します[#18062](https://github.com/pingcap/tidb/pull/18062)
    -   `DROP DATABASE`と`DROP TABLE`を同一データベースで同時に実行すると、 TiFlashstorageへのデータ複製が停止する問題を修正[#17901](https://github.com/pingcap/tidb/pull/17901)
    -   TiDB とオブジェクトstorageサービス間の`BACKUP` `RESTORE`障害を修正[#17844](https://github.com/pingcap/tidb/pull/17844)
    -   アクセスが拒否された場合の権限チェック失敗の誤ったエラー メッセージを修正します[#17724](https://github.com/pingcap/tidb/pull/17724)
    -   `DELETE` / `UPDATE`ステートメントから生成されたクエリ フィードバックを破棄します[#17843](https://github.com/pingcap/tidb/pull/17843)
    -   `AUTO_RANDOM`プロパティ[#17828](https://github.com/pingcap/tidb/pull/17828)のないテーブルの変更を禁止します`AUTO_RANDOM_BASE`
    -   テーブルがデータベース間で`ALTER TABLE ... RENAME` [#18243](https://github.com/pingcap/tidb/pull/18243)移動されると、 `AUTO_RANDOM`列が間違った結果に割り当てられる問題を修正します。
    -   `tidb` [#17719](https://github.com/pingcap/tidb/pull/17719)なしで`tidb_isolation_read_engines`の値を設定すると、一部のシステム テーブルにアクセスできない問題を修正します。
    -   大きな整数と浮動小数点値の JSON 比較の不正確な結果を修正します[#17717](https://github.com/pingcap/tidb/pull/17717)
    -   `COUNT()`関数[#17704](https://github.com/pingcap/tidb/pull/17704)の結果の誤った小数プロパティを修正します
    -   入力のタイプがバイナリ文字列の場合の`HEX()`関数の誤った結果を修正します[#17620](https://github.com/pingcap/tidb/pull/17620)
    -   フィルター条件[#17697](https://github.com/pingcap/tidb/pull/17697)なしで`INFORMATION_SCHEMA.INSPECTION_SUMMARY`テーブルをクエリすると、空の結果が返される問題を修正します。
    -   ユーザー情報を更新する`ALTER USER`ステートメントで使用されるハッシュ化されたパスワードが予期しないものであるという問題を修正します[#17646](https://github.com/pingcap/tidb/pull/17646)
    -   `ENUM`と`SET`値の照合順序をサポート[#17701](https://github.com/pingcap/tidb/pull/17701)
    -   テーブル[#17619](https://github.com/pingcap/tidb/pull/17619)の作成時に事前分割リージョンのタイムアウト メカニズムが機能しない問題を修正します。
    -   DDL ジョブの再試行時にスキーマが予期せず更新され、DDL ジョブの原子性が失われる可能性がある問題を修正します[#17608](https://github.com/pingcap/tidb/pull/17608)
    -   引数に列[#17562](https://github.com/pingcap/tidb/pull/17562)含まれている場合の`FIELD()`関数の誤った結果を修正します。
    -   `max_execution_time`ヒントがたまに効かない不具合を修正[#17536](https://github.com/pingcap/tidb/pull/17536)
    -   `EXPLAIN ANALYZE` [#17350](https://github.com/pingcap/tidb/pull/17350)の結果に同時実行情報が重複して出力される問題を修正
    -   `STR_TO_DATE`関数[#17498](https://github.com/pingcap/tidb/pull/17498)での`%h`の非互換動作を修正
    -   `tidb_replica_read`が`follower`に設定され、リーダーとフォロワー/学習者[#17443](https://github.com/pingcap/tidb/pull/17443)の間にネットワーク パーティションがある場合、フォロワー/学習者がリトライし続ける問題を修正します。
    -   場合によっては、TiDB が PD フォロワーに送信する ping が多すぎる問題を修正します[#17947](https://github.com/pingcap/tidb/pull/17947)
    -   古いバージョンのレンジパーティションテーブルが TiDB v4.0 で読み込めない問題を修正[#17983](https://github.com/pingcap/tidb/pull/17983)
    -   リージョン[#17585](https://github.com/pingcap/tidb/pull/17585)ごとに異なる`Backoffer`を割り当てることで、複数のリージョンリクエストが同時に失敗した場合の SQL ステートメントのタイムアウトの問題を修正します。
    -   `DateTime`区切り文字[#17501](https://github.com/pingcap/tidb/pull/17501)を解析するときの MySQL の互換性のない動作を修正します。
    -   TiKV リクエストが時々 TiFlashサーバーに送信される問題を修正します[#18105](https://github.com/pingcap/tidb/pull/18105)
    -   [#18250](https://github.com/pingcap/tidb/pull/18250)つのトランザクションで書き込まれ、削除された主キーのロックが別のトランザクションによって解決されるために発生したデータの不整合の問題を修正します。

-   TiKV

    -   ステータスサーバー[#8101](https://github.com/tikv/tikv/pull/8101)のメモリの安全性の問題を修正します。
    -   JSON 数値比較[#8087](https://github.com/tikv/tikv/pull/8087)で精度が失われる問題を修正
    -   間違ったクエリの遅いログを修正する[#8050](https://github.com/tikv/tikv/pull/8050)
    -   複数のマージ プロセス中にピアのストアが分離されている場合、ピアを削除できない問題を修正します[#8048](https://github.com/tikv/tikv/pull/8048)
    -   `tikv-ctl recover-mvcc`無効な悲観的ロックが削除されない問題を修正します[#8047](https://github.com/tikv/tikv/pull/8047)
    -   一部の Titan ヒストグラム メトリックが欠落している問題を修正します[#7997](https://github.com/tikv/tikv/pull/7997)
    -   TiKV が TiCDC [#7887](https://github.com/tikv/tikv/pull/7887)に`duplicated error`を返す問題を修正

-   PD

    -   `pd-server.dashboard-address`構成アイテム[#2517](https://github.com/pingcap/pd/pull/2517)の正確性を確認します
    -   `store-limit-mode`から`auto` [#2544](https://github.com/pingcap/pd/pull/2544)を設定するときの PD のpanic問題を修正します。
    -   ホットスポットが特定できない場合がある問題を修正[#2463](https://github.com/pingcap/pd/pull/2463)
    -   配置ルールにより、ストアが`tombstone`に変更されない場合がある問題を修正します[#2546](https://github.com/pingcap/pd/pull/2546)
    -   場合によっては、以前のバージョンからアップグレードする際の PD のpanic問題を修正します[#2564](https://github.com/pingcap/pd/pull/2564)

-   TiFlash

    -   `region not found`エラー発生時にプロキシがpanicすることがある問題を修正
    -   `drop table`でスローされた I/O 例外により、 TiFlashスキーマの同期エラーが発生する可能性がある問題を修正
