---
title: TiDB 2.1.15 Release Notes
---

# TiDB 2.1.15 リリースノート {#tidb-2-1-15-release-notes}

発売日：2019年7月16日

TiDB バージョン: 2.1.15

TiDB Ansible バージョン: 2.1.15

## TiDB {#tidb}

-   マイクロ秒[#11289](https://github.com/pingcap/tidb/pull/11289)を処理するときに、 `DATE_ADD`関数が不正な位置合わせにより間違った結果を返す問題を修正します。
-   文字列列の空の値が`FLOAT`または`INT`と比較されるとエラーが報告される問題を修正します[#11279](https://github.com/pingcap/tidb/pull/11279)
-   パラメータが`NULL` [#11249](https://github.com/pingcap/tidb/pull/11249)の場合、 `INSERT`関数が`NULL`値を正しく返せない問題を修正します。
-   非文字列型かつ長さ`0` [#11215](https://github.com/pingcap/tidb/pull/11215)のインデックス作成時にエラーが発生する問題を修正
-   SQL ステートメント[#11238](https://github.com/pingcap/tidb/pull/11238)を通じてテーブルのリージョン分布をクエリする`SHOW TABLE REGIONS`ステートメントを追加します。
-   [#11254](https://github.com/pingcap/tidb/pull/11254) `SELECT`サブクエリのルールを最適化するために射影除去が使用されるため、 `UPDATE … SELECT`ステートメントを使用するとエラーが報告される問題を修正します。
-   `ADMIN PLUGINS ENABLE` / `ADMIN PLUGINS DISABLE` SQL ステートメントを追加して、プラグインを動的に有効または無効にします[#11189](https://github.com/pingcap/tidb/pull/11189)
-   監査プラグイン[#11189](https://github.com/pingcap/tidb/pull/11189)にセッション接続情報を追加します。
-   列が複数回クエリされ、ポイント クエリ中に返された結果が`NULL`ある場合に発生するpanicの問題を修正します[#11227](https://github.com/pingcap/tidb/pull/11227)
-   テーブル[#11213](https://github.com/pingcap/tidb/pull/11213)を作成するときに、 `tidb_scatter_region`構成アイテムを散布テーブルのリージョンに追加します。
-   `RAND`関数[#11170](https://github.com/pingcap/tidb/pull/11170)の使用時に非スレッド セーフ`rand.Rand`によって引き起こされるデータ競合の問題を修正します。
-   整数と非整数の比較結果が正しくない場合がある問題を修正[#11191](https://github.com/pingcap/tidb/pull/11191)
-   データベースまたはテーブルの照合順序の変更をサポートしますが、データベース/テーブルの文字セットは UTF-8 または utf8mb4 である必要があります[#11085](https://github.com/pingcap/tidb/pull/11085)
-   カラムのデフォルト値として`CURRENT_TIMESTAMP`使用し、float 精度を[#11087](https://github.com/pingcap/tidb/pull/11087)に指定した場合、 `SHOW CREATE TABLE`ステートメントで示される精度が不完全になる問題を修正しました。

## TiKV {#tikv}

-   ログフォーマットの統一[#5083](https://github.com/tikv/tikv/pull/5083)
-   極端な場合のリージョンのおおよそのサイズまたはキーの精度を向上させ、スケジューリング[#5085](https://github.com/tikv/tikv/pull/5085)の精度を向上させます。

## PD {#pd}

-   ログフォーマットの統一[#1625](https://github.com/pingcap/pd/pull/1625)

## ツール {#tools}

TiDBBinlog

-   PumpGC 戦略を最適化し、未消費のbinlogをクリーンアップできないという制限を削除して、リソースが長時間占有されないようにする[#663](https://github.com/pingcap/tidb-binlog/pull/663)

TiDB Lightning

-   SQL ダンプで指定された列名が小文字ではない場合に発生するインポート エラーを修正[#210](https://github.com/pingcap/tidb-lightning/pull/210)

## TiDB Ansible {#tidb-ansible}

-   TiDB ダッシュボードに監視項目`parse duration`と`compile duration`を追加して、SQL ステートメントの解析とコンパイルの実行にかかる時間を監視します[#815](https://github.com/pingcap/tidb-ansible/pull/815)
