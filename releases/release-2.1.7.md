---
title: TiDB 2.1.7 Release Notes
---

# TiDB 2.1.7 リリースノート {#tidb-2-1-7-release-notes}

リリース日：2019年3月28日

TiDB バージョン: 2.1.7

TiDB Ansible バージョン: 2.1.7

## TiDB {#tidb}

-   DDL 操作のキャンセルによりプログラムのアップグレード時に起動時間が長くなる問題を修正[#9768](https://github.com/pingcap/tidb/pull/9768)
-   `check-mb4-value-in-utf8`構成アイテムが`config.example.toml`ファイル[#9852](https://github.com/pingcap/tidb/pull/9852)の間違った位置にある問題を修正します。
-   `str_to_date`組み込み関数と MySQL [#9817](https://github.com/pingcap/tidb/pull/9817)の互換性を向上
-   `last_day`組み込み関数の互換性の問題を修正[#9750](https://github.com/pingcap/tidb/pull/9750)
-   SQL ステートメントを使用して`table_id`を取得しやすくするために`infoschema.tables`に`tidb_table_id`列を追加し、テーブルとインデックス間の関係を管理するために`tidb_indexes`システム テーブルを追加します[#9862](https://github.com/pingcap/tidb/pull/9862)
-   テーブルパーティション[#9663](https://github.com/pingcap/tidb/pull/9663)のnull定義に関するチェックを追加
-   MySQL [#9876](https://github.com/pingcap/tidb/pull/9876)との一貫性を保つために、 `Truncate Table`に必要な権限を`Delete`から`Drop`に変更します。
-   `DO`ステートメントでのサブクエリの使用のサポート[#9877](https://github.com/pingcap/tidb/pull/9877)
-   `default_week_format`変数が`week`関数で有効にならない問題を修正[#9753](https://github.com/pingcap/tidb/pull/9753)
-   プラグイン フレームワーク[#9880](https://github.com/pingcap/tidb/pull/9880) 、 [#9888](https://github.com/pingcap/tidb/pull/9888)をサポートします。
-   `log_bin`システム変数[#9634](https://github.com/pingcap/tidb/pull/9634)を使用したbinlogの有効化状態のチェックのサポート
-   SQL ステートメントを使用したPump/Drainerのステータスのチェックをサポート[#9896](https://github.com/pingcap/tidb/pull/9896)
-   TiDB [#9887](https://github.com/pingcap/tidb/pull/9887)をアップグレードする際の utf8 での mb4 文字のチェックに関する互換性の問題を修正
-   場合によっては集計関数が JSON データを計算するときのpanicの問題を修正します[#9927](https://github.com/pingcap/tidb/pull/9927)

## PD {#pd}

-   レプリカ数が[#1462](https://github.com/pingcap/pd/pull/1462)の場合、バランス領域に転送リーダーステップが作成できない問題を修正

## ツール {#tools}

-   binlogを使用した生成された列のレプリケーションのサポート

## TiDB Ansible {#tidb-ansible}

Prometheus 監視データのデフォルトの保持時間を 30 日に変更します
