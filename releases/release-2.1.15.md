---
title: TiDB 2.1.15 Release Notes
summary: TiDB 2.1.15 は 2019 年 7 月 16 日にリリースされました。DATE_ADD や INSERT などの関数の問題の修正、SHOW TABLE REGIONS などの新しい SQL ステートメントの追加、Audit プラグインの強化など、さまざまなバグ修正と改善が含まれています。TiKV と PD も更新され、ログ形式が統一され、精度が向上しました。さらに、TiDB BinlogとTiDB Lightningが最適化され、TiDB Ansible に新しい監視項目が追加されました。
---

# TiDB 2.1.15 リリースノート {#tidb-2-1-15-release-notes}

発売日: 2019年7月16日

TiDB バージョン: 2.1.15

TiDB Ansible バージョン: 2.1.15

## ティビ {#tidb}

-   マイクロ秒を扱う際に誤ったアライメントが原因で`DATE_ADD`関数が間違った結果を返す問題を修正[＃11289](https://github.com/pingcap/tidb/pull/11289)
-   文字列列の空の値を`FLOAT`または`INT`と比較するとエラーが報告される問題を修正しました[＃11279](https://github.com/pingcap/tidb/pull/11279)
-   パラメータが`NULL` [＃11249](https://github.com/pingcap/tidb/pull/11249)の場合に`INSERT`関数が`NULL`値を正しく返さない問題を修正しました
-   非文字列型で長さ`0` [＃11215](https://github.com/pingcap/tidb/pull/11215)をインデックスするとエラーが発生する問題を修正
-   SQL文[＃11238](https://github.com/pingcap/tidb/pull/11238)を使用してテーブルのリージョン分布を照会するための`SHOW TABLE REGIONS`文を追加します。
-   `SELECT`のサブクエリ[＃11254](https://github.com/pingcap/tidb/pull/11254)のルールを最適化するために投影除去が使用されるため、 `UPDATE … SELECT`ステートメントを使用するとエラーが報告される問題を修正しました。
-   プラグインを動的に有効または無効にする`ADMIN PLUGINS ENABLE` SQL ステートメントを`ADMIN PLUGINS DISABLE`します[＃11189](https://github.com/pingcap/tidb/pull/11189)
-   監査プラグイン[＃11189](https://github.com/pingcap/tidb/pull/11189)にセッション接続情報を追加する
-   ポイントクエリ[＃11227](https://github.com/pingcap/tidb/pull/11227)中に列が複数回クエリされ、返された結果が`NULL`である場合に発生するpanic問題を修正しました。
-   テーブル[＃11213](https://github.com/pingcap/tidb/pull/11213)を作成するときに、散布テーブルRegionsに`tidb_scatter_region`構成項目を追加します。
-   `RAND`関数[＃11170](https://github.com/pingcap/tidb/pull/11170)使用するときに非スレッドセーフ`rand.Rand`によって発生するデータ競合の問題を修正しました
-   整数と非整数の比較結果が場合によっては正しくない問題を修正[＃11191](https://github.com/pingcap/tidb/pull/11191)
-   データベースまたはテーブルの照合順序の変更をサポートしますが、データベース/テーブルの文字セットは UTF-8 または utf8mb4 である必要があります[＃11085](https://github.com/pingcap/tidb/pull/11085)
-   列のデフォルト値として`CURRENT_TIMESTAMP`が使用され、浮動小数点精度が[＃11087](https://github.com/pingcap/tidb/pull/11087)に指定されている場合、 `SHOW CREATE TABLE`ステートメントで表示される精度が不完全になる問題を修正しました。

## ティクヴ {#tikv}

-   ログフォーマットの統一[＃5083](https://github.com/tikv/tikv/pull/5083)
-   極端なケースでのリージョンのおおよそのサイズやキーの精度を向上させて、スケジュールの精度を向上させます[＃5085](https://github.com/tikv/tikv/pull/5085)

## PD {#pd}

-   ログフォーマットの統一[＃1625](https://github.com/pingcap/pd/pull/1625)

## ツール {#tools}

TiDBBinlog

-   Pump GC戦略を最適化し、未使用のbinlogをクリーンアップできないという制限を削除して、リソースが長時間占有されないようにします[＃663](https://github.com/pingcap/tidb-binlog/pull/663)

TiDB Lightning

-   SQLダンプで指定された列名が小文字でない場合に発生するインポートエラーを修正[＃210](https://github.com/pingcap/tidb-lightning/pull/210)

## TiDB アンシブル {#tidb-ansible}

-   TiDBダッシュボードに監視項目`parse duration`と`compile duration`を追加して、SQL文の解析とコンパイルの実行にかかる時間を監視します[＃815](https://github.com/pingcap/tidb-ansible/pull/815)
