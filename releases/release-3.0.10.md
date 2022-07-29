---
title: TiDB 3.0.10 Release Notes
---

# TiDB3.0.10リリースノート {#tidb-3-0-10-release-notes}

発売日：2020年2月20日

TiDBバージョン：3.0.10

TiDB Ansibleバージョン：3.0.10

> **警告：**
>
> このバージョンにはいくつかの既知の問題があり、これらの問題は新しいバージョンで修正されています。最新の3.0.xバージョンを使用することをお勧めします。

## TiDB {#tidb}

-   `IndexLookUpJoin`が`OtherCondition`を使用して`InnerRange`を構築するときに[＃14599](https://github.com/pingcap/tidb/pull/14599)た`Join`の結果を修正する
-   `tidb_pprof_sql_cpu`の構成アイテムを削除し、 `tidb_pprof_sql_cpu`の変数[＃14416](https://github.com/pingcap/tidb/pull/14416)を追加します。
-   ユーザーがグローバル権限を持っている場合にのみすべてのデータベースにクエリを実行できるという問題を修正します[＃14386](https://github.com/pingcap/tidb/pull/14386)
-   `PointGet`の操作を実行するときにトランザクションのタイムアウトが原因でデータの可視性が期待を満たさないという問題を修正します[＃14480](https://github.com/pingcap/tidb/pull/14480)
-   楽観的なトランザクションモード[＃14474](https://github.com/pingcap/tidb/pull/14474)と一致して、悲観的なトランザクションのアクティブ化のタイミングを遅延アクティブ化に変更します。
-   `unixtimestamp`式がテーブルパーティションのタイムゾーンを計算するときの誤ったタイムゾーンの結果を修正します[＃14476](https://github.com/pingcap/tidb/pull/14476)
-   `tidb_session_statement_deadlock_detect_duration_seconds`の監視項目を追加して、デッドロック検出期間[＃14484](https://github.com/pingcap/tidb/pull/14484)を監視します。
-   GCワーカーのいくつかの論理エラーによって引き起こされるシステムpanicの問題を修正します[＃14439](https://github.com/pingcap/tidb/pull/14439)
-   `IsTrue`関数の式名を修正してください[＃14516](https://github.com/pingcap/tidb/pull/14516)
-   一部のメモリ使用量が不正確にカウントされる問題を修正します[＃14533](https://github.com/pingcap/tidb/pull/14533)
-   CM-Sketch統計の初期化中に誤った処理ロジックによって引き起こされるシステムpanicの問題を修正します[＃14470](https://github.com/pingcap/tidb/pull/14470)
-   パーティションテーブルをクエリするときの不正確なパーティションプルーニングの問題を修正します[＃14546](https://github.com/pingcap/tidb/pull/14546)
-   SQLバインディングのSQLステートメントのデフォルトのデータベース名が正しく設定されていない問題を修正します[＃14548](https://github.com/pingcap/tidb/pull/14548)
-   `json_key`がMySQL3と互換性がないという問題を修正し[＃14561](https://github.com/pingcap/tidb/pull/14561)
-   パーティションテーブルの統計を自動的に更新する機能を追加する[＃14566](https://github.com/pingcap/tidb/pull/14566)
-   `PointGet`の操作を実行するとプランIDが変わる問題を修正します（プランIDは常に`1`であると予想されます） [＃14595](https://github.com/pingcap/tidb/pull/14595)
-   SQLバインディングが正確に[＃14263](https://github.com/pingcap/tidb/pull/14263)と一致しない場合に、誤った処理ロジックによって引き起こされるシステムpanicの問題を修正します
-   悲観的トランザクションのロックに失敗した後の再試行回数を監視するには、 `tidb_session_statement_pessimistic_retry_count`の監視項目を追加します[＃14619](https://github.com/pingcap/tidb/pull/14619)
-   `show binding`ステートメントの誤った特権チェックを修正します[＃14618](https://github.com/pingcap/tidb/pull/14618)
-   `backoff`ロジックに`killed`タグ[＃14614](https://github.com/pingcap/tidb/pull/14614)のチェックが含まれていないため、クエリを強制終了できない問題を修正します。
-   内部ロックを保持する時間を短縮することにより、ステートメントの要約のパフォーマンスを向上させます[＃14627](https://github.com/pingcap/tidb/pull/14627)
-   文字列を時間に解析したTiDBの結果がMySQL1と互換性がないという問題を修正し[＃14570](https://github.com/pingcap/tidb/pull/14570)
-   ユーザーのログイン失敗を監査ログに記録する[＃14620](https://github.com/pingcap/tidb/pull/14620)
-   `tidb_session_ statement_lock_keys_count`の監視項目を追加して、悲観的なトランザクションのロックキーの数を監視します[＃14634](https://github.com/pingcap/tidb/pull/14634)
-   `&`などのJSONの文字が誤って[＃14637](https://github.com/pingcap/tidb/pull/14637)される問題を修正し`>` `<`
-   `HashJoin`操作がハッシュテーブルを構築しているときに過剰なメモリ使用量によって引き起こされるシステムpanicの問題を修正します[＃14642](https://github.com/pingcap/tidb/pull/14642)
-   SQLバインディングが不正なレコードを処理するときに誤った処理ロジックによって引き起こされるpanicの問題を修正します[＃14645](https://github.com/pingcap/tidb/pull/14645)
-   ix10進除算の計算に切り捨てられたエラー検出を追加することによるMySQLの非互換性の問題[＃14673](https://github.com/pingcap/tidb/pull/14673)
-   存在しないテーブルに対する特権をユーザーに正常に付与する問題を修正します[＃14611](https://github.com/pingcap/tidb/pull/14611)

## TiKV {#tikv}

-   ラフトストア
    -   リージョンマージの失敗によって引き起こされるシステムpanicの問題＃6460またはデータ損失の問題＃598を修正します[＃6481](https://github.com/tikv/tikv/pull/6481)
    -   スケジューリングの公平性を最適化するために`yield`をサポートし、リーダーのスケジューリングの安定性を向上させるためにリーダーの事前転送をサポートします[＃6563](https://github.com/tikv/tikv/pull/6563)

## PD {#pd}

-   システムトラフィックが変更されたときにリージョンキャッシュ情報を自動的に更新することをサポートすることにより、無効なキャッシュの問題を修正します[＃2103](https://github.com/pingcap/pd/pull/2103)
-   リーダーのリース時間を使用して、TSOサービスの有効性を判断します[＃2117](https://github.com/pingcap/pd/pull/2117)

## ツール {#tools}

-   TiDB Binlog
    -   [＃893](https://github.com/pingcap/tidb-binlog/pull/893)のDrainerをサポートする
-   TiDB Lightning
    -   構成ファイルが欠落している場合に、一部の構成アイテムでデフォルト値を使用するようにする[＃255](https://github.com/pingcap/tidb-lightning/pull/255)
    -   非サーバーモードでWebインターフェイスを開くことができない問題を修正します[＃259](https://github.com/pingcap/tidb-lightning/pull/259)

## TiDB Ansible {#tidb-ansible}

-   一部のシナリオでPDリーダーの取得に失敗したためにコマンドの実行が失敗する問題を修正します[＃1121](https://github.com/pingcap/tidb-ansible/pull/1121)
-   TiDBダッシュボードに`Deadlock Detect Duration`の監視項目を追加します[＃1127](https://github.com/pingcap/tidb-ansible/pull/1127)
-   TiDBダッシュボードに`Statement Lock Keys Count`の監視項目を追加します[＃1132](https://github.com/pingcap/tidb-ansible/pull/1132)
-   TiDBダッシュボードに`Statement Pessimistic Retry Count`の監視項目を追加します[＃1133](https://github.com/pingcap/tidb-ansible/pull/1133)
