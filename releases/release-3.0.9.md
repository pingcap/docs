---
title: TiDB 3.0.9 Release Notes
summary: TiDB 3.0.9は2020年1月14日にリリースされました。既知の問題の修正と新機能が含まれています。Executor、Server、DDL、Planner、TiKV、PD、Tools、TiDB Ansibleにいくつかの改善が加えられました。主な変更点としては、システム変数のサポート、メトリクスの監視、トランザクション実行レイテンシーの最適化などが挙げられます。さらに、ロケーションラベル名でのバックラッシュの使用と、 TiDB Lightningデプロイメント用のディレクトリの自動作成のサポートが追加されました。
---

# TiDB 3.0.9 リリースノート {#tidb-3-0-9-release-notes}

発売日：2020年1月14日

TiDB バージョン: 3.0.9

TiDB Ansible バージョン: 3.0.9

> **警告：**
>
> このバージョンにはいくつかの既知の問題が見つかりましたが、これらの問題は新しいバージョンで修正されています。最新の3.0.xバージョンをご利用いただくことをお勧めします。

## TiDB {#tidb}

-   執行者
    -   集計関数を`ENUM`列目とコレクション列[＃14364](https://github.com/pingcap/tidb/pull/14364)に適用した場合の誤った結果を修正しました
-   サーバ
    -   システム変数`auto_increment_increment`と`auto_increment_offset`サポート[＃14396](https://github.com/pingcap/tidb/pull/14396)
    -   `tidb_tikvclient_ttl_lifetime_reach_total`監視メトリックを追加して、TTL が 10 分の悲観的トランザクションの数を監視します[＃14300](https://github.com/pingcap/tidb/pull/14300)
    -   SQLクエリの実行中にpanicが発生した場合に、SQL情報をログに出力します[＃14322](https://github.com/pingcap/tidb/pull/14322)
    -   ステートメント要約テーブルに`plan`と`plan_digest`フィールドを追加して、実行されている`plan`と`plan`署名[＃14285](https://github.com/pingcap/tidb/pull/14285)記録します。
    -   `stmt-summary.max-stmt-count`構成項目のデフォルト値を`100`から`200`に調整します[＃14285](https://github.com/pingcap/tidb/pull/14285)
    -   スロークエリテーブルに`plan_digest`フィールドを追加して、 `plan`署名[＃14292](https://github.com/pingcap/tidb/pull/14292)記録する
-   DDL
    -   `primary`列目に`alter table ... add index`を使用して作成された匿名インデックスの結果がMySQL [＃14310](https://github.com/pingcap/tidb/pull/14310)と一致しない問題を修正しました
    -   `drop table`構文で`VIEW`が誤って削除される問題を修正[＃14052](https://github.com/pingcap/tidb/pull/14052)
-   プランナー
    -   `select max(a), min(a) from t`のような文のパフォーマンスを最適化します。3 `a`にインデックスが存在する場合、文は`select * from (select a from t order by a desc limit 1) as t1, (select a from t order by a limit 1) as t2`に最適化され、フルテーブルスキャン[＃14410](https://github.com/pingcap/tidb/pull/14410)を回避します。

## TiKV {#tikv}

-   Raftstore
    -   構成変更を高速化して、リージョン分散[＃6421](https://github.com/tikv/tikv/pull/6421)高速化します。
-   トランザクション
    -   `tikv_lock_manager_waiter_lifetime_duration` `tikv_lock_manager_detect_duration`監視メトリックを追加して、 `waiter`の寿命、デッドロックの検出にかかる時間コスト、および`Wait`表[＃6392](https://github.com/tikv/tikv/pull/6392)の状態`tikv_lock_manager_detect_duration`監視します。
    -   極端な状況でリージョンリーダーまたはデッドロック検出器のリーダーを変更することによって発生するトランザクション実行のレイテンシーを削減するために、次の構成項目を最適化します[＃6429](https://github.com/tikv/tikv/pull/6429)
        -   デフォルト値の`wait-for-lock-time`を`3s`から`1s`に変更します
        -   デフォルト値の`wake-up-delay-duration`を`100ms`から`20ms`に変更します
    -   リージョンマージプロセス中にデッドロック検出器のリーダーが正しくない可能性がある問題を修正しました[＃6431](https://github.com/tikv/tikv/pull/6431)

## PD {#pd}

-   位置ラベル名[＃2083](https://github.com/pingcap/pd/pull/2083)でバックラッシュ`/`使用をサポート
-   トゥームストーンストアがラベルカウンタ[＃2067](https://github.com/pingcap/pd/pull/2067)に誤って含まれているために誤った統計を修正しました

## ツール {#tools}

-   TiDBBinlog
    -   Drainer [＃862](https://github.com/pingcap/tidb-binlog/pull/862)によって出力されたbinlogプロトコルに一意のキー情報を追加します。
    -   Drainer [＃868](https://github.com/pingcap/tidb-binlog/pull/868)データベース接続に暗号化されたパスワードの使用をサポート

## TiDB アンシブル {#tidb-ansible}

-   TiDB Lightning [＃1105](https://github.com/pingcap/tidb-ansible/pull/1105)の展開を最適化するためにディレクトリを自動的に作成する機能をサポート
