---
title: TiDB 2.1.10 Release Notes
---

# TiDB 2.1.10 リリースノート {#tidb-2-1-10-release-notes}

発売日：2019年5月22日

TiDB バージョン: 2.1.10

TiDB アンシブル バージョン: 2.1.10

## TiDB {#tidb}

-   `tidb_snapshot`を使用して履歴データを読み取ると、一部の異常によりテーブル スキーマが正しくなくなる問題を修正します[#10359](https://github.com/pingcap/tidb/pull/10359)
-   `NOT`関数で読み取り結果がおかしくなることがある問題を修正[#10363](https://github.com/pingcap/tidb/pull/10363)
-   `Replace`または`Insert on duplicate update`ステートメントの`Generated Column`の間違った動作を修正します[#10385](https://github.com/pingcap/tidb/pull/10385)
-   `DATE`比較[#10407](https://github.com/pingcap/tidb/pull/10407)で`BETWEEN`機能の不具合`DATETIME`修正
-   `SLOW_QUERY`テーブルを使用してスロー ログ[#10412](https://github.com/pingcap/tidb/pull/10412)をクエリすると、スロー ログの 1 行が長すぎるとエラー レポートが表示される問題を修正します。
-   `DATETIME`たす`INTERVAL`の結果が MySQL の結果と一致しない場合がある問題を修正[#10416](https://github.com/pingcap/tidb/pull/10416) 、 [#10418](https://github.com/pingcap/tidb/pull/10418)
-   うるう年の 2 月の無効時間のチェックを追加します[#10417](https://github.com/pingcap/tidb/pull/10417)
-   内部初期化操作の制限を DDL 所有者でのみ実行して、クラスターの初期化時に大量の競合エラー レポートが発生しないようにする[#10426](https://github.com/pingcap/tidb/pull/10426)
-   出力タイムスタンプ列のデフォルト値が`default current_timestamp on update current_timestamp` [#10337](https://github.com/pingcap/tidb/issues/10337)の場合、 `DESC`が MySQL と互換性がない問題を修正
-   `Update`文[#10439](https://github.com/pingcap/tidb/pull/10439)で権限チェック時にエラーが発生する問題を修正
-   `RANGE`の計算を間違えると`CHAR`列目で間違った結果になる場合がある問題を修正[#10455](https://github.com/pingcap/tidb/pull/10455)
-   `SHARD_ROW_ID_BITS` [#9868](https://github.com/pingcap/tidb/pull/9868)減らすとデータが上書きされることがある問題を修正
-   `ORDER BY RAND()`が乱数を返さない問題を修正[#10064](https://github.com/pingcap/tidb/pull/10064)
-   10 進数の精度を変更する`ALTER`ステートメントを禁止する[#10458](https://github.com/pingcap/tidb/pull/10458)
-   `TIME_FORMAT`関数の MySQL [#10474](https://github.com/pingcap/tidb/pull/10474)との互換性の問題を修正
-   `PERIOD_ADD` [#10430](https://github.com/pingcap/tidb/pull/10430)のパラメーターの妥当性をチェックする
-   TiDB の無効な`YEAR`文字列の動作が MySQL [#10493](https://github.com/pingcap/tidb/pull/10493)と互換性がない問題を修正
-   `ALTER DATABASE`構文[#10503](https://github.com/pingcap/tidb/pull/10503)をサポート
-   スロー クエリ ステートメント[#10536](https://github.com/pingcap/tidb/pull/10536)に`;`が存在しない場合、 `SLOW_QUERY`メモリエンジンがエラーを報告する問題を修正します。
-   分割されたテーブルで`Add index`操作をキャンセルできない場合がある問題を修正[#10533](https://github.com/pingcap/tidb/pull/10533)
-   場合によっては OOMpanicが回復できない問題を修正[#10545](https://github.com/pingcap/tidb/pull/10545)
-   テーブル メタデータを書き換える DDL 操作のセキュリティを向上させる[#10547](https://github.com/pingcap/tidb/pull/10547)

## PD {#pd}

-   リーダーの優先度が反映されない問題を修正[#1533](https://github.com/pingcap/pd/pull/1533)

## TiKV {#tikv}

-   転送の失敗を避けるために、最近構成が変更されたリージョンでリーダーの転送を拒否する[#4684](https://github.com/tikv/tikv/pull/4684)
-   コプロセッサーメトリック[#4643](https://github.com/tikv/tikv/pull/4643)の優先順位ラベルを追加します。
-   リーダー[#4724](https://github.com/tikv/tikv/pull/4724)の転送中に発生する可能性のあるダーティ リードの問題を修正します。
-   1.TiKVの再起動に失敗する場合が`CommitMerge`問題を修正[#4615](https://github.com/tikv/tikv/pull/4615)
-   不明なログの修正[#4730](https://github.com/tikv/tikv/pull/4730)

## ツール {#tools}

-   TiDB Lightning
    -   TiDB Lightning が`importer` [#176](https://github.com/pingcap/tidb-lightning/pull/176)へのデータ送信に失敗した場合のリトライ機能を追加
-   TiDBBinlog
    -   トラブルシューティングを容易にするためにPumpstorageログを最適化する[#607](https://github.com/pingcap/tidb-binlog/pull/607)

## TiDB アンシブル {#tidb-ansible}

-   TiDB Lightningの構成ファイルを更新し、 `tidb_lightning_ctl`スクリプト[#d3a4a368](https://github.com/pingcap/tidb-ansible/commit/d3a4a368810a421c49980899a286cf010569b4c7)を追加します。
