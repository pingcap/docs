---
title: TiDB 3.0.9 Release Notes
---

# TiDB 3.0.9 リリースノート {#tidb-3-0-9-release-notes}

発売日：2020年1月14日

TiDB バージョン: 3.0.9

TiDB Ansible バージョン: 3.0.9

> **警告：**
>
> このバージョンではいくつかの既知の問題が見つかり、これらの問題は新しいバージョンで修正されています。最新の 3.0.x バージョンを使用することをお勧めします。

## TiDB {#tidb}

-   執行者
    -   集計関数を列`ENUM`とコレクション列[#14364](https://github.com/pingcap/tidb/pull/14364)に適用した場合の誤った結果を修正
-   サーバ
    -   システム変数`auto_increment_increment`および`auto_increment_offset`をサポート[#14396](https://github.com/pingcap/tidb/pull/14396)
    -   `tidb_tikvclient_ttl_lifetime_reach_total`監視メトリックを追加して、10 分の TTL で悲観的トランザクションの数を監視します[#14300](https://github.com/pingcap/tidb/pull/14300)
    -   SQLクエリの実行中にpanicが発生した場合にSQL情報をログに出力します[#14322](https://github.com/pingcap/tidb/pull/14322)
    -   ステートメント概要テーブルに`plan`フィールドと`plan_digest`フィールドを追加して、実行中の`plan`と`plan`署名[#14285](https://github.com/pingcap/tidb/pull/14285)を記録します。
    -   `stmt-summary.max-stmt-count`設定項目のデフォルト値を`100`から`200`に調整します[#14285](https://github.com/pingcap/tidb/pull/14285)
    -   スロー クエリ テーブルに`plan_digest`フィールドを追加して、 `plan`シグネチャ[#14292](https://github.com/pingcap/tidb/pull/14292)を記録します。
-   DDL
    -   `primary`列の`alter table ... add index`を使用して作成された匿名インデックスの結果が MySQL [#14310](https://github.com/pingcap/tidb/pull/14310)と一致しない問題を修正
    -   `drop table`構文で`VIEW`が誤って削除される問題を修正[#14052](https://github.com/pingcap/tidb/pull/14052)
-   プランナー
    -   `select max(a), min(a) from t`などのステートメントのパフォーマンスを最適化します。 `a`列にインデックスが存在する場合、テーブル全体のスキャンを回避するためにステートメントは`select * from (select a from t order by a desc limit 1) as t1, (select a from t order by a limit 1) as t2`に最適化されます[#14410](https://github.com/pingcap/tidb/pull/14410)

## TiKV {#tikv}

-   Raftstore
    -   構成変更を高速化して、リージョン分散[#6421](https://github.com/tikv/tikv/pull/6421)を高速化します。
-   トランザクション
    -   `tikv_lock_manager_waiter_lifetime_duration` 、 `tikv_lock_manager_detect_duration` 、および`tikv_lock_manager_detect_duration`監視メトリクスを追加して、 `waiter`の存続期間、デッドロックの検出にかかる時間コスト、および`Wait`のステータスを監視します。 表[#6392](https://github.com/tikv/tikv/pull/6392)
    -   以下の設定項目を最適化して、極端な状況でリージョンリーダーまたはデッドロック ディテクタのリーダーを変更することによって発生するトランザクション実行レイテンシーを削減します[#6429](https://github.com/tikv/tikv/pull/6429)
        -   デフォルト値の`wait-for-lock-time`を`3s`から`1s`に変更します。
        -   デフォルト値の`wake-up-delay-duration`を`100ms`から`20ms`に変更します。
    -   リージョンマージ プロセス中にデッドロック ディテクタのリーダーが正しくない可能性がある問題を修正します[#6431](https://github.com/tikv/tikv/pull/6431)

## PD {#pd}

-   位置ラベル名[#2083](https://github.com/pingcap/pd/pull/2083)でのバックラッシュ`/`の使用のサポート
-   ラベル カウンター[#2067](https://github.com/pingcap/pd/pull/2067)に誤ってトゥームストーン ストアが含まれているため、誤った統計を修正しました。

## ツール {#tools}

-   TiDBBinlog
    -   Drainer [#862](https://github.com/pingcap/tidb-binlog/pull/862)が出力したbinlogプロトコルに一意のキー情報を追加します。
    -   Drainer [#868](https://github.com/pingcap/tidb-binlog/pull/868)のデータベース接続に暗号化パスワードの使用をサポート

## TiDB Ansible {#tidb-ansible}

-   TiDB Lightning [#1105](https://github.com/pingcap/tidb-ansible/pull/1105)のデプロイメントを最適化するためのディレクトリの自動作成のサポート
