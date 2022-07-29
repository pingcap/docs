---
title: TiDB 2.1.7 Release Notes
---

# TiDB2.1.7リリースノート {#tidb-2-1-7-release-notes}

リリース日：2019年3月28日

TiDBバージョン：2.1.7

TiDB Ansibleバージョン：2.1.7

## TiDB {#tidb}

-   DDL操作のキャンセルによってプログラムをアップグレードするときに起動時間が長くなる問題を修正します[＃9768](https://github.com/pingcap/tidb/pull/9768)
-   `check-mb4-value-in-utf8`の構成アイテムが`config.example.toml`のファイル[＃9852](https://github.com/pingcap/tidb/pull/9852)の間違った位置にある問題を修正します
-   `str_to_date`組み込み関数とMySQL3の互換性を改善し[＃9817](https://github.com/pingcap/tidb/pull/9817)
-   `last_day`組み込み関数[＃9750](https://github.com/pingcap/tidb/pull/9750)の互換性の問題を修正します
-   SQLステートメントを使用して`table_id`を取得しやすくするために、 `infoschema.tables`に`tidb_table_id`列を追加し、テーブルとインデックス[＃9862](https://github.com/pingcap/tidb/pull/9862)の間の関係を管理するために`tidb_indexes`システムテーブルを追加します。
-   テーブルパーティション[＃9663](https://github.com/pingcap/tidb/pull/9663)のnull定義に関するチェックを追加します
-   MySQL [＃9876](https://github.com/pingcap/tidb/pull/9876)との整合性を保つために、 `Truncate Table`に必要な特権を`Delete`から`Drop`に変更します。
-   `DO`ステートメント[＃9877](https://github.com/pingcap/tidb/pull/9877)でのサブクエリの使用のサポート
-   `default_week_format`変数が`week`関数[＃9753](https://github.com/pingcap/tidb/pull/9753)で有効にならない問題を修正します
-   プラグインフレームワークをサポートする[＃9880](https://github.com/pingcap/tidb/pull/9880) 、 [＃9888](https://github.com/pingcap/tidb/pull/9888)
-   `log_bin`システム変数[＃9634](https://github.com/pingcap/tidb/pull/9634)を使用して、binlogの有効化状態のチェックをサポートします。
-   SQLステートメントを使用したPump/Drainerステータスのチェックのサポート[＃9896](https://github.com/pingcap/tidb/pull/9896)
-   TiDB1をアップグレードするときにutf8でmb4文字をチェックすることに関する互換性の問題を修正し[＃9887](https://github.com/pingcap/tidb/pull/9887)
-   集計関数がJSONデータを計算する場合のpanicの問題を修正します[＃9927](https://github.com/pingcap/tidb/pull/9927)

## PD {#pd}

-   レプリカの数が1の場合、バランス領域に転送リーダーステップを作成できない問題を修正します[＃1462](https://github.com/pingcap/pd/pull/1462)

## ツール {#tools}

-   binlogを使用して生成された列の複製をサポートする

## TiDB Ansible {#tidb-ansible}

Prometheusモニタリングデータのデフォルトの保持時間を30dに変更します
