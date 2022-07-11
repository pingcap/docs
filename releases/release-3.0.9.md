---
title: TiDB 3.0.9 Release Notes
---

# TiDB3.0.9リリースノート {#tidb-3-0-9-release-notes}

発売日：2020年1月14日

TiDBバージョン：3.0.9

TiDB Ansibleバージョン：3.0.9

> **警告：**
>
> このバージョンにはいくつかの既知の問題があり、これらの問題は新しいバージョンで修正されています。最新の3.0.xバージョンを使用することをお勧めします。

## TiDB {#tidb}

-   エグゼキュータ
    -   集計関数が`ENUM`列とコレクション列[＃14364](https://github.com/pingcap/tidb/pull/14364)に適用されたときの誤った結果を修正します
-   サーバ
    -   `auto_increment_increment`および`auto_increment_offset`のシステム変数をサポートする[＃14396](https://github.com/pingcap/tidb/pull/14396)
    -   `tidb_tikvclient_ttl_lifetime_reach_total`の監視メトリックを追加して、TTLが10分の悲観的なトランザクションの数を監視します[＃14300](https://github.com/pingcap/tidb/pull/14300)
    -   SQLクエリの実行中にpanicが発生した場合にSQL情報をログに出力する[＃14322](https://github.com/pingcap/tidb/pull/14322)
    -   ステートメントサマリーテーブルに`plan`フィールドと`plan_digest`フィールドを追加して、実行中の`plan`フィールドと`plan`シグニチャ[＃14285](https://github.com/pingcap/tidb/pull/14285)を記録します。
    -   `stmt-summary.max-stmt-count`構成項目のデフォルト値を`100`から[＃14285](https://github.com/pingcap/tidb/pull/14285)に調整し`200` 。
    -   低速クエリテーブルに`plan_digest`フィールドを追加して、 `plan`シグニチャを記録します[＃14292](https://github.com/pingcap/tidb/pull/14292)
-   DDL
    -   `primary`列に`alter table ... add index`を使用して作成された匿名インデックスの結果が[＃14310](https://github.com/pingcap/tidb/pull/14310)と矛盾する問題を修正します
    -   `drop table`構文[＃14052](https://github.com/pingcap/tidb/pull/14052)によって`VIEW`が誤ってドロップされる問題を修正します。
-   プランナー
    -   `select max(a), min(a) from t`などのステートメントのパフォーマンスを最適化します。インデックスが`a`列に存在する場合、ステートメントは`select * from (select a from t order by a desc limit 1) as t1, (select a from t order by a limit 1) as t2`に最適化され、全表スキャンを回避します[＃14410](https://github.com/pingcap/tidb/pull/14410)

## TiKV {#tikv}

-   ラフトストア
    -   構成変更を高速化して、領域散乱を高速化します[＃6421](https://github.com/tikv/tikv/pull/6421)
-   取引
    -   `tikv_lock_manager_waiter_lifetime_duration` 、および`tikv_lock_manager_detect_duration`の監視メトリックを追加して、 `tikv_lock_manager_detect_duration`の存続期間、デッドロックの検出にかかる時間コスト、および`Wait` `waiter`テーブル[＃6392](https://github.com/tikv/tikv/pull/6392)のステータスを監視します。
    -   次の構成項目を最適化して、極端な状況でリージョンリーダーまたはデッドロック検出器のリーダーを変更することによって発生するトランザクション実行の待機時間を短縮します[＃6429](https://github.com/tikv/tikv/pull/6429)
        -   デフォルト値の`wait-for-lock-time`を`3s`から`1s`に変更します
        -   デフォルト値の`wake-up-delay-duration`を`100ms`から`20ms`に変更します
    -   リージョンマージプロセス中にデッドロック検出器のリーダーが正しくない可能性がある問題を修正します[＃6431](https://github.com/tikv/tikv/pull/6431)

## PD {#pd}

-   ロケーションラベル名[＃2083](https://github.com/pingcap/pd/pull/2083)でのバックラッシュ`/`の使用をサポート
-   トゥームストーンストアがラベルカウンター[＃2067](https://github.com/pingcap/pd/pull/2067)に誤って含まれているため、誤った統計を修正します

## ツール {#tools}

-   TiDB Binlog
    -   Drainer1によって出力されたDrainerプロトコルに一意のキー情報を追加し[＃862](https://github.com/pingcap/tidb-binlog/pull/862)
    -   Drainerのデータベース接続に暗号化されたパスワードを使用することを[＃868](https://github.com/pingcap/tidb-binlog/pull/868)

## TiDB Ansible {#tidb-ansible}

-   TiDB Lightningの展開を最適化するためのディレクトリの自動作成を[＃1105](https://github.com/pingcap/tidb-ansible/pull/1105)
