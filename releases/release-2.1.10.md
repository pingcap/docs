---
title: TiDB 2.1.10 Release Notes
---

# TiDB 2.1.10 リリースノート {#tidb-2-1-10-release-notes}

発売日：2019年5月22日

TiDB バージョン: 2.1.10

TiDB Ansible バージョン: 2.1.10

## TiDB {#tidb}

-   `tidb_snapshot`を使用して履歴データ[#10359](https://github.com/pingcap/tidb/pull/10359)を読み込むときに、一部の異常によりテーブル スキーマが正しくなくなる問題を修正
-   `NOT`関数により誤った読み取り結果が発生する場合がある問題を修正[#10363](https://github.com/pingcap/tidb/pull/10363)
-   `Replace`または`Insert on duplicate update`ステートメントの`Generated Column`の誤った動作を修正します[#10385](https://github.com/pingcap/tidb/pull/10385)
-   `DATE`比較`DATETIME`の`BETWEEN`関数のバグ[#10407](https://github.com/pingcap/tidb/pull/10407)修正
-   `SLOW_QUERY`テーブルを使用してスロー ログ[#10412](https://github.com/pingcap/tidb/pull/10412)をクエリするときに、長すぎるスロー ログの 1 行によってエラー レポートが発生する問題を修正します。
-   `DATETIME`に`INTERVAL`を加えた結果が MySQL の結果と異なる場合がある問題を修正[#10416](https://github.com/pingcap/tidb/pull/10416) 、 [#10418](https://github.com/pingcap/tidb/pull/10418)
-   閏年の 2 月が無効になる場合のチェックを追加[#10417](https://github.com/pingcap/tidb/pull/10417)
-   クラスター[#10426](https://github.com/pingcap/tidb/pull/10426)の初期化時に大量の競合エラー レポートが発生するのを避けるために、内部初期化操作の制限を DDL 所有者のみで実行します。
-   出力タイムスタンプ列のデフォルト値が`default current_timestamp on update current_timestamp` [#10337](https://github.com/pingcap/tidb/issues/10337)の場合、 `DESC`は MySQL と互換性がないという問題を修正
-   `Update`ステートメント[#10439](https://github.com/pingcap/tidb/pull/10439)の権限チェックでエラーが発生する問題を修正
-   `RANGE`の計算を間違えると`CHAR`列の結果が正しくない場合がある問題を修正[#10455](https://github.com/pingcap/tidb/pull/10455)
-   `SHARD_ROW_ID_BITS` [#9868](https://github.com/pingcap/tidb/pull/9868)を減らすとデータが上書きされる場合がある問題を修正
-   `ORDER BY RAND()`が乱数を返さない問題を修正[#10064](https://github.com/pingcap/tidb/pull/10064)
-   `ALTER`小数の精度を変更するステートメントを禁止します[#10458](https://github.com/pingcap/tidb/pull/10458)
-   `TIME_FORMAT`関数と MySQL [#10474](https://github.com/pingcap/tidb/pull/10474)の互換性の問題を修正
-   `PERIOD_ADD` [#10430](https://github.com/pingcap/tidb/pull/10430)のパラメータの有効性を確認します
-   TiDB の無効な`YEAR`文字列の動作が MySQL [#10493](https://github.com/pingcap/tidb/pull/10493)の動作と互換性がない問題を修正
-   `ALTER DATABASE`構文[#10503](https://github.com/pingcap/tidb/pull/10503)をサポートします。
-   遅いクエリ ステートメント[#10536](https://github.com/pingcap/tidb/pull/10536)に`;`が存在しない場合、 `SLOW_QUERY`メモリエンジンがエラーを報告する問題を修正します。
-   `Add index`パーティションテーブルの操作がキャンセルできない場合がある問題を修正[#10533](https://github.com/pingcap/tidb/pull/10533)
-   OOMpanicが回復できない場合がある問題を修正[#10545](https://github.com/pingcap/tidb/pull/10545)
-   テーブルメタデータを書き換える DDL 操作のセキュリティを向上[#10547](https://github.com/pingcap/tidb/pull/10547)

## PD {#pd}

-   リーダーの優先度が反映されない問題を修正[#1533](https://github.com/pingcap/pd/pull/1533)

## TiKV {#tikv}

-   転送の失敗を避けるために、最近設定が変更されたリージョンでのリーダーの転送を拒否します[#4684](https://github.com/tikv/tikv/pull/4684)
-   コプロセッサーメトリック[#4643](https://github.com/tikv/tikv/pull/4643)の優先順位ラベルを追加します。
-   リーダー[#4724](https://github.com/tikv/tikv/pull/4724)の転送中に発生する可能性のあるダーティ リードの問題を修正
-   `CommitMerge`場合によっては TiKV の再起動に失敗する問題を修正[#4615](https://github.com/tikv/tikv/pull/4615)
-   不明なログを修正[#4730](https://github.com/tikv/tikv/pull/4730)

## ツール {#tools}

-   TiDB Lightning
    -   TiDB Lightning が`importer` [#176](https://github.com/pingcap/tidb-lightning/pull/176)へのデータ送信に失敗した場合の再試行機能を追加
-   TiDBBinlog
    -   トラブルシューティングを容易にするためにPumpのstorageログを最適化します[#607](https://github.com/pingcap/tidb-binlog/pull/607)

## TiDB Ansible {#tidb-ansible}

-   TiDB Lightningの設定ファイルを更新し、 `tidb_lightning_ctl`スクリプト[#d3a4a368](https://github.com/pingcap/tidb-ansible/commit/d3a4a368810a421c49980899a286cf010569b4c7)を追加します。
