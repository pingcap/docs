---
title: TiDB 2.1.7 Release Notes
---

# TiDB 2.1.7 リリースノート {#tidb-2-1-7-release-notes}

リリース日：2019年3月28日

TiDB バージョン: 2.1.7

TiDB アンシブル バージョン: 2.1.7

## TiDB {#tidb}

-   DDL 操作をキャンセルすることにより、プログラムをアップグレードするときに起動時間が長くなる問題を修正します[#9768](https://github.com/pingcap/tidb/pull/9768)
-   `config.example.toml`ファイルで`check-mb4-value-in-utf8`構成アイテムが間違った位置にある問題を修正します[#9852](https://github.com/pingcap/tidb/pull/9852)
-   `str_to_date`組み込み関数の MySQL [#9817](https://github.com/pingcap/tidb/pull/9817)との互換性を向上させる
-   `last_day`組み込み関数の互換性の問題を修正[#9750](https://github.com/pingcap/tidb/pull/9750)
-   `infoschema.tables`の`tidb_table_id`列を追加して、SQL ステートメントを使用して`table_id`を取得しやすくし、 `tidb_indexes`システム テーブルを追加して、テーブルとインデックスの関係を管理します[#9862](https://github.com/pingcap/tidb/pull/9862)
-   テーブル パーティション[#9663](https://github.com/pingcap/tidb/pull/9663)の null 定義に関するチェックを追加します。
-   `Truncate Table`に必要な権限を`Delete`から`Drop`に変更して、MySQL [#9876](https://github.com/pingcap/tidb/pull/9876)と一貫性を持たせます。
-   `DO`ステートメントでのサブクエリの使用のサポート[#9877](https://github.com/pingcap/tidb/pull/9877)
-   `week`関数[#9753](https://github.com/pingcap/tidb/pull/9753)で`default_week_format`変数が有効にならない問題を修正
-   プラグイン フレームワークのサポート[#9880](https://github.com/pingcap/tidb/pull/9880) 、 [#9888](https://github.com/pingcap/tidb/pull/9888)
-   `log_bin`システム変数[#9634](https://github.com/pingcap/tidb/pull/9634)を使用したbinlogの有効化状態のチェックをサポート
-   SQL ステートメントを使用したPump/Drainerステータスの確認のサポート[#9896](https://github.com/pingcap/tidb/pull/9896)
-   TiDB [#9887](https://github.com/pingcap/tidb/pull/9887)をアップグレードする際の utf8 での mb4 文字のチェックに関する互換性の問題を修正
-   場合によっては集計関数が JSON データを計算するときのpanicの問題を修正します[#9927](https://github.com/pingcap/tidb/pull/9927)

## PD {#pd}

-   レプリカの数が[#1462](https://github.com/pingcap/pd/pull/1462)の場合、転送するリーダー ステップがバランス リージョンに作成できない問題を修正します。

## ツール {#tools}

-   binlogを使用して生成された列の複製をサポートする

## TiDB アンシブル {#tidb-ansible}

Prometheus モニタリング データのデフォルトの保持期間を 30 日に変更します
