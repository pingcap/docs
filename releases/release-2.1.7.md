---
title: TiDB 2.1.7 Release Notes
summary: TiDB 2.1.7は2019年3月28日にリリースされました。様々なバグ修正、互換性向上に加え、DO`文でのサブクエリのサポート、プラグインフレームワーク、SQL文によるbinlogおよびPump/Drainerの状態確認といった新機能が追加されています。PDでは、balance-regionにおけるリーダーステップの転送に関する問題も修正されました。さらに、TiDB AnsibleにおけるPrometheus監視データのデフォルトの保持期間が30日に変更されました。
---

# TiDB 2.1.7 リリースノート {#tidb-2-1-7-release-notes}

リリース日：2019年3月28日

TiDB バージョン: 2.1.7

TiDB Ansible バージョン: 2.1.7

## TiDB {#tidb}

-   DDL操作のキャンセルによりプログラムのアップグレード時に起動時間が長くなる問題を修正[＃9768](https://github.com/pingcap/tidb/pull/9768)
-   `check-mb4-value-in-utf8`構成項目が`config.example.toml`ファイル[＃9852](https://github.com/pingcap/tidb/pull/9852)内の間違った位置にある問題を修正しました
-   `str_to_date`組み込み関数とMySQL [＃9817](https://github.com/pingcap/tidb/pull/9817)の互換性を改善
-   `last_day`組み込み関数[＃9750](https://github.com/pingcap/tidb/pull/9750)の互換性の問題を修正
-   SQL文を使用して`table_id`を取得するために`infoschema.tables`の`tidb_table_id`列を追加し、テーブルとインデックス[＃9862](https://github.com/pingcap/tidb/pull/9862)の関係を管理するために`tidb_indexes`システムテーブルを追加します。
-   テーブルパーティション[＃9663](https://github.com/pingcap/tidb/pull/9663)のNULL定義に関するチェックを追加します
-   MySQL [＃9876](https://github.com/pingcap/tidb/pull/9876)と一致するように、 `Truncate Table`に必要な権限を`Delete`から`Drop`に変更します。
-   `DO`文[＃9877](https://github.com/pingcap/tidb/pull/9877)でのサブクエリの使用をサポート
-   `default_week_format`変数が`week`関数[＃9753](https://github.com/pingcap/tidb/pull/9753)で効果を発揮しない問題を修正
-   プラグインフレームワーク[＃9880](https://github.com/pingcap/tidb/pull/9880) [＃9888](https://github.com/pingcap/tidb/pull/9888)サポート
-   `log_bin`システム変数[＃9634](https://github.com/pingcap/tidb/pull/9634)を使用してbinlogの有効状態の確認をサポート
-   SQL文を使用したPump/Drainerの状態確認をサポート[＃9896](https://github.com/pingcap/tidb/pull/9896)
-   TiDB [＃9887](https://github.com/pingcap/tidb/pull/9887)アップグレードする際の mb4 文字の UTF8 チェックに関する互換性の問題を修正しました
-   集計関数がJSONデータを計算するときに発生するpanic問題を修正[＃9927](https://github.com/pingcap/tidb/pull/9927)

## PD {#pd}

-   レプリカ数が[＃1462](https://github.com/pingcap/pd/pull/1462)場合、バランスリージョンに転送リーダーステップを作成できない問題を修正しました。

## ツール {#tools}

-   binlogを使用して生成された列の複製をサポートする

## TiDB アンシブル {#tidb-ansible}

Prometheus 監視データのデフォルトの保持期間を 30 日に変更します
