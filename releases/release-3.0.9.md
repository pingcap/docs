---
title: TiDB 3.0.9 Release Notes
---

# TiDB 3.0.9 リリースノート {#tidb-3-0-9-release-notes}

発売日：2020年1月14日

TiDB バージョン: 3.0.9

TiDB アンシブル バージョン: 3.0.9

> **警告：**
>
> このバージョンにはいくつかの既知の問題があり、これらの問題は新しいバージョンで修正されています。最新の 3.0.x バージョンを使用することをお勧めします。

## TiDB {#tidb}

-   実行者
    -   集計関数を`ENUM`列とコレクション列[#14364](https://github.com/pingcap/tidb/pull/14364)に適用したときの誤った結果を修正します。
-   サーバ
    -   `auto_increment_increment`および`auto_increment_offset`システム変数[#14396](https://github.com/pingcap/tidb/pull/14396)をサポート
    -   `tidb_tikvclient_ttl_lifetime_reach_total`モニタリング メトリックを追加して、10 分の TTL で悲観的トランザクションの数をモニタリングします[#14300](https://github.com/pingcap/tidb/pull/14300)
    -   SQLクエリの実行中にpanicが発生した場合、ログにSQL情報を出力します[#14322](https://github.com/pingcap/tidb/pull/14322)
    -   ステートメント要約表に`plan`および`plan_digest`フィールドを追加して、実行中の`plan`と署名`plan`を記録します[#14285](https://github.com/pingcap/tidb/pull/14285)
    -   `stmt-summary.max-stmt-count`構成項目のデフォルト値を`100`から`200`に調整します[#14285](https://github.com/pingcap/tidb/pull/14285)
    -   スロー クエリ テーブルに`plan_digest`フィールドを追加して、 `plan`シグネチャ[#14292](https://github.com/pingcap/tidb/pull/14292)を記録します。
-   DDL
    -   `primary`列に`alter table ... add index`を使用して作成された匿名インデックスの結果が MySQL [#14310](https://github.com/pingcap/tidb/pull/14310)と一致しない問題を修正します。
    -   `drop table`構文[#14052](https://github.com/pingcap/tidb/pull/14052)で`VIEW`が誤ってドロップされる問題を修正
-   プランナー
    -   `select max(a), min(a) from t`などのステートメントのパフォーマンスを最適化します。インデックスが`a`列に存在する場合、ステートメントは`select * from (select a from t order by a desc limit 1) as t1, (select a from t order by a limit 1) as t2`に最適化され、フル テーブル スキャンを回避します[#14410](https://github.com/pingcap/tidb/pull/14410)

## TiKV {#tikv}

-   Raftstore
    -   構成変更を高速化して、リージョン分散を高速化します[#6421](https://github.com/tikv/tikv/pull/6421)
-   トランザクション
    -   `tikv_lock_manager_waiter_lifetime_duration` 、 `tikv_lock_manager_detect_duration` 、および`tikv_lock_manager_detect_duration`モニタリング メトリックを追加して、 `waiter`の有効期間、デッドロックを検出するための時間コスト、および`Wait`表[#6392](https://github.com/tikv/tikv/pull/6392)のステータスをモニタリングします。
    -   次の構成項目を最適化して、極端な状況でリージョンリーダーまたはデッドロック ディテクターのリーダーを変更することによって引き起こされるトランザクション実行レイテンシーを削減します[#6429](https://github.com/tikv/tikv/pull/6429)
        -   デフォルト値の`wait-for-lock-time`を`3s`から`1s`に変更します
        -   デフォルト値の`wake-up-delay-duration`を`100ms`から`20ms`に変更します
    -   リージョン Merge プロセス中にデッドロック検出器のリーダーが正しくない可能性がある問題を修正します[#6431](https://github.com/tikv/tikv/pull/6431)

## PD {#pd}

-   ロケーション ラベル名でのバックラッシュ`/`の使用のサポート[#2083](https://github.com/pingcap/pd/pull/2083)
-   トゥームストーン ストアが誤ってラベル カウンター[#2067](https://github.com/pingcap/pd/pull/2067)に含まれているため、誤った統計を修正します。

## ツール {#tools}

-   TiDBBinlog
    -   Drainer [#862](https://github.com/pingcap/tidb-binlog/pull/862)が出力するbinlogプロトコルに一意のキー情報を追加します
    -   Drainer [#868](https://github.com/pingcap/tidb-binlog/pull/868)のデータベース接続に暗号化パスワードを使用するサポート

## TiDB アンシブル {#tidb-ansible}

-   ディレクトリの自動作成をサポートして、 TiDB Lightning [#1105](https://github.com/pingcap/tidb-ansible/pull/1105)の展開を最適化します
