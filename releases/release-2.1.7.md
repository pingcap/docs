---
title: TiDB 2.1.7 Release Notes
summary: TiDB 2.1.7 は、2019 年 3 月 28 日にリリースされました。さまざまなバグ修正、互換性の改善、および `DO` ステートメントでのサブクエリのサポート、プラグイン フレームワーク、SQL ステートメントを使用したbinlogおよびPump/ Drainerステータスの確認などの新機能が含まれています。PD では、バランス リージョンでのリーダー ステップの転送に関連する問題も修正されました。さらに、TiDB Ansible の Prometheus 監視データのデフォルトの保持期間が 30 日に変更されました。
---

# TiDB 2.1.7 リリースノート {#tidb-2-1-7-release-notes}

リリース日：2019年3月28日

TiDB バージョン: 2.1.7

TiDB Ansible バージョン: 2.1.7

## ティビ {#tidb}

-   DDL操作のキャンセルによりプログラムのアップグレード時に起動時間が長くなる問題を修正[＃9768](https://github.com/pingcap/tidb/pull/9768)
-   `check-mb4-value-in-utf8`構成項目が`config.example.toml`ファイル[＃9852](https://github.com/pingcap/tidb/pull/9852)内の間違った位置にある問題を修正
-   `str_to_date`の組み込み関数とMySQL [＃9817](https://github.com/pingcap/tidb/pull/9817)の互換性を改善
-   `last_day`組み込み関数[＃9750](https://github.com/pingcap/tidb/pull/9750)の互換性問題を修正
-   SQL文を使用して`table_id`を取得しやすくするために`infoschema.tables`の`tidb_table_id`列を追加し、テーブルとインデックス[＃9862](https://github.com/pingcap/tidb/pull/9862)の関係を管理するために`tidb_indexes`システムテーブルを追加します。
-   テーブルパーティション[＃9663](https://github.com/pingcap/tidb/pull/9663)のNULL定義に関するチェックを追加します
-   MySQL [＃9876](https://github.com/pingcap/tidb/pull/9876)と一致するように、 `Truncate Table`に必要な権限を`Delete`から`Drop`に変更します。
-   `DO`文[＃9877](https://github.com/pingcap/tidb/pull/9877)でのサブクエリの使用をサポート
-   `default_week_format`変数が`week`関数[＃9753](https://github.com/pingcap/tidb/pull/9753)で有効にならない問題を修正
-   プラグインフレームワーク[＃9880](https://github.com/pingcap/tidb/pull/9880) [＃9888](https://github.com/pingcap/tidb/pull/9888)サポート
-   `log_bin`システム変数[＃9634](https://github.com/pingcap/tidb/pull/9634)を使用してbinlogの有効化状態の確認をサポートします
-   SQL文を使用したPump/Drainerの状態確認のサポート[＃9896](https://github.com/pingcap/tidb/pull/9896)
-   TiDB [＃9887](https://github.com/pingcap/tidb/pull/9887)のアップグレード時に utf8 上の mb4 文字をチェックする際の互換性の問題を修正しました
-   集計関数が JSON データを計算するときに発生するpanic問題を修正[＃9927](https://github.com/pingcap/tidb/pull/9927)

## PD {#pd}

-   レプリカ数が[＃1462](https://github.com/pingcap/pd/pull/1462)の場合、バランス領域に転送リーダー ステップを作成できない問題を修正しました。

## ツール {#tools}

-   binlogを使用して生成された列の複製をサポートする

## TiDB アンシブル {#tidb-ansible}

Prometheus モニタリングデータのデフォルトの保存期間を 30 日に変更します。
