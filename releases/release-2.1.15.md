---
title: TiDB 2.1.15 Release Notes
---

# TiDB2.1.15リリースノート {#tidb-2-1-15-release-notes}

発売日：2019年7月16日

TiDBバージョン：2.1.15

TiDB Ansibleバージョン：2.1.15

## TiDB {#tidb}

-   マイクロ秒[＃11289](https://github.com/pingcap/tidb/pull/11289)を処理するときに、 `DATE_ADD`関数が誤った配置のために、誤った結果を返す問題を修正します。
-   文字列列の空の値を`FLOAT`または[＃11279](https://github.com/pingcap/tidb/pull/11279)と比較すると、エラーが報告される問題を修正し`INT` 。
-   パラメータが[＃11249](https://github.com/pingcap/tidb/pull/11249)の場合、 `INSERT`関数が`NULL`値を正しく返さない問題を修正し`NULL` 。
-   非文字列型で長さ`0`の列にインデックスを付けるときにエラーが発生する問題を修正します[＃11215](https://github.com/pingcap/tidb/pull/11215)
-   `SHOW TABLE REGIONS`ステートメントを追加して、SQLステートメント[＃11238](https://github.com/pingcap/tidb/pull/11238)を介してテーブルのリージョン分布をクエリします。
-   `SELECT`のサブクエリのルールを最適化するために射影除去が使用されるため、 `UPDATE … SELECT`ステートメントを使用するとエラーが報告される問題を修正します[＃11254](https://github.com/pingcap/tidb/pull/11254)
-   プラグインを動的に有効または無効にする`ADMIN PLUGINS ENABLE` / `ADMIN PLUGINS DISABLE`ステートメントを追加します[＃11189](https://github.com/pingcap/tidb/pull/11189)
-   監査プラグイン[＃11189](https://github.com/pingcap/tidb/pull/11189)にセッション接続情報を追加します
-   列が複数回クエリされ、ポイントクエリ中に返される結果が`NULL`である場合に発生するpanicの問題を修正します[＃11227](https://github.com/pingcap/tidb/pull/11227)
-   テーブルを作成するときに、 `tidb_scatter_region`の構成アイテムを分散テーブル領域に追加します[＃11213](https://github.com/pingcap/tidb/pull/11213)
-   `RAND`関数[＃11170](https://github.com/pingcap/tidb/pull/11170)を使用するときに非スレッドセーフ`rand.Rand`によって引き起こされるデータ競合の問題を修正します
-   整数と非整数の比較結果が正しくない場合がある問題を修正します[＃11191](https://github.com/pingcap/tidb/pull/11191)
-   データベースまたはテーブルの照合順序の変更をサポートしますが、データベース/テーブルの文字セットはUTF-8または[＃11085](https://github.com/pingcap/tidb/pull/11085)である必要があります。
-   列のデフォルト値として`CURRENT_TIMESTAMP`が使用され、浮動小数点精度が指定されている場合、 `SHOW CREATE TABLE`ステートメントによって示される精度が不完全であるという問題を修正します[＃11087](https://github.com/pingcap/tidb/pull/11087)

## TiKV {#tikv}

-   ログ形式を統一する[＃5083](https://github.com/tikv/tikv/pull/5083)
-   極端な場合にリージョンのおおよそのサイズまたはキーの精度を向上させて、スケジューリングの精度を向上させます[＃5085](https://github.com/tikv/tikv/pull/5085)

## PD {#pd}

-   ログ形式を統一する[＃1625](https://github.com/pingcap/pd/pull/1625)

## ツール {#tools}

TiDB Binlog

-   Pump GC戦略を最適化し、消費されていないbinlogをクリーンアップできないという制限を取り除き、リソースが長期間使用されないようにします[＃663](https://github.com/pingcap/tidb-binlog/pull/663)

TiDB Lightning

-   SQLダンプで指定された列名が小文字[＃210](https://github.com/pingcap/tidb-lightning/pull/210)でない場合に発生するインポートエラーを修正します

## TiDB Ansible {#tidb-ansible}

-   TiDBダッシュボードに`parse duration`と`compile duration`の監視項目を追加して、SQLステートメントの解析とコンパイルの実行にかかる時間を監視します[＃815](https://github.com/pingcap/tidb-ansible/pull/815)
