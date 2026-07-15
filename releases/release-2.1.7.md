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
-   `check-mb4-value-in-utf8`構成項目が`config.example.toml`ファイル内の間違った位置にある問題を修正しました [＃9852](https://github.com/pingcap/tidb/pull/9852)
-   `str_to_date`組み込み関数とMySQL の互換性を改善 [＃9817](https://github.com/pingcap/tidb/pull/9817)
-   `last_day`組み込み関数の互換性の問題を修正 [＃9750](https://github.com/pingcap/tidb/pull/9750)
-   SQL文を使用して`table_id`を取得するために`infoschema.tables`の`tidb_table_id`列を追加し、テーブルとインデックスの関係を管理するために`tidb_indexes`システムテーブルを追加します。 [＃9862](https://github.com/pingcap/tidb/pull/9862)
-   テーブルパーティションのNULL定義に関するチェックを追加します [＃9663](https://github.com/pingcap/tidb/pull/9663)
-   MySQL と一致するように、 `Truncate Table`に必要な権限を`Delete`から`Drop`に変更します。 [＃9876](https://github.com/pingcap/tidb/pull/9876)
-   `DO`文でのサブクエリの使用をサポート [＃9877](https://github.com/pingcap/tidb/pull/9877)
-   `default_week_format`変数が`week`関数で効果を発揮しない問題を修正 [＃9753](https://github.com/pingcap/tidb/pull/9753)
-   プラグインフレームワーク サポート [＃9888](https://github.com/pingcap/tidb/pull/9888) [＃9880](https://github.com/pingcap/tidb/pull/9880)
-   `log_bin`システム変数を使用してbinlogの有効状態の確認をサポート [＃9634](https://github.com/pingcap/tidb/pull/9634)
-   SQL文を使用したPump/Drainerの状態確認をサポート[＃9896](https://github.com/pingcap/tidb/pull/9896)
-   TiDB アップグレードする際の mb4 文字の UTF8 チェックに関する互換性の問題を修正しました [＃9887](https://github.com/pingcap/tidb/pull/9887)
-   集計関数がJSONデータを計算するときに発生するpanic問題を修正[＃9927](https://github.com/pingcap/tidb/pull/9927)

## PD {#pd}

-   レプリカ数が1の場合、バランスリージョンに転送リーダーステップを作成できない問題を修正しました。 [＃1462](https://github.com/pingcap/pd/pull/1462)

## ツール {#tools}

-   binlogを使用して生成された列の複製をサポートする

## TiDB Ansible {#tidb-ansible}

Prometheus 監視データのデフォルトの保持期間を 30 日に変更します
