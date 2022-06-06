---
title: TiDB 2.1.10 Release Notes
---

# TiDB2.1.10リリースノート {#tidb-2-1-10-release-notes}

発売日：2019年5月22日

TiDBバージョン：2.1.10

TiDB Ansibleバージョン：2.1.10

## TiDB {#tidb}

-   `tidb_snapshot`を使用して履歴データを読み取るときに一部の異常が原因で誤ったテーブルスキーマが発生する問題を修正します[＃10359](https://github.com/pingcap/tidb/pull/10359)
-   `NOT`関数が誤った読み取り結果を引き起こす場合があるという問題を修正します[＃10363](https://github.com/pingcap/tidb/pull/10363)
-   `Replace`または`Insert on duplicate update`ステートメント[＃10385](https://github.com/pingcap/tidb/pull/10385)の`Generated Column`の誤った動作を修正します。
-   `DATE`比較`DATETIME`の`BETWEEN`関数のバグを[＃10407](https://github.com/pingcap/tidb/pull/10407)
-   遅いログの1行が長すぎると、 `SLOW_QUERY`のテーブルを使用して遅いログをクエリするときにエラーレポートが発生する問題を修正します[＃10412](https://github.com/pingcap/tidb/pull/10412)
-   `DATETIME` + `INTERVAL`の結果がMySQLの結果と同じでない場合があるという問題を修正し[＃10418](https://github.com/pingcap/tidb/pull/10418) [＃10416](https://github.com/pingcap/tidb/pull/10416)
-   うるう年の2月の無効な時間のチェックを追加します[＃10417](https://github.com/pingcap/tidb/pull/10417)
-   DDL所有者でのみ内部初期化操作制限を実行して、クラスタ[＃10426](https://github.com/pingcap/tidb/pull/10426)を初期化するときに多数の競合エラーレポートを回避します。
-   出力タイムスタンプ列のデフォルト値が[＃10337](https://github.com/pingcap/tidb/issues/10337)の場合、 `DESC`がMySQLと互換性がないという問題を修正し`default current_timestamp on update current_timestamp` 。
-   `Update`ステートメント[＃10439](https://github.com/pingcap/tidb/pull/10439)の特権チェック中にエラーが発生する問題を修正します。
-   `RANGE`の計算が間違っていると、場合によっては`CHAR`列に間違った結果が生じるという問題を修正します[＃10455](https://github.com/pingcap/tidb/pull/10455)
-   `SHARD_ROW_ID_BITS`を減らした後にデータが上書きされる可能性がある問題を修正し[＃9868](https://github.com/pingcap/tidb/pull/9868)
-   `ORDER BY RAND()`がランダムな数値[＃10064](https://github.com/pingcap/tidb/pull/10064)を返さない問題を修正します
-   小数の精度を変更する`ALTER`ステートメントを禁止する[＃10458](https://github.com/pingcap/tidb/pull/10458)
-   MySQL3との`TIME_FORMAT`関数の互換性の問題を修正し[＃10474](https://github.com/pingcap/tidb/pull/10474)
-   `PERIOD_ADD`のパラメータの有効性を確認して[＃10430](https://github.com/pingcap/tidb/pull/10430)
-   TiDBの無効な`YEAR`文字列の動作がMySQL3の動作と互換性がないという問題を修正し[＃10493](https://github.com/pingcap/tidb/pull/10493)
-   `ALTER DATABASE`構文[＃10503](https://github.com/pingcap/tidb/pull/10503)をサポートします
-   低速クエリステートメント[＃10536](https://github.com/pingcap/tidb/pull/10536)に`;`が存在しない場合に、 `SLOW_QUERY`メモリエンジンがエラーを報告する問題を修正します。
-   パーティションテーブルの`Add index`操作をキャンセルできない場合があるという問題を修正します[＃10533](https://github.com/pingcap/tidb/pull/10533)
-   OOMパニックが回復できない場合がある問題を修正します[＃10545](https://github.com/pingcap/tidb/pull/10545)
-   テーブルメタデータを書き換えるDDL操作のセキュリティを向上させる[＃10547](https://github.com/pingcap/tidb/pull/10547)

## PD {#pd}

-   リーダーの優先順位が有効にならない問題を修正します[＃1533](https://github.com/pingcap/pd/pull/1533)

## TiKV {#tikv}

-   転送の失敗を回避するために、最近構成が変更されたリージョンでリーダーの転送を拒否する[＃4684](https://github.com/tikv/tikv/pull/4684)
-   コプロセッサーメトリックス[＃4643](https://github.com/tikv/tikv/pull/4643)の優先順位ラベルを追加します。
-   リーダー[＃4724](https://github.com/tikv/tikv/pull/4724)の転送中に発生する可能性があったダーティリードの問題を修正します
-   `CommitMerge`が場合によってはTiKVの再起動エラーを引き起こすという問題を修正します[＃4615](https://github.com/tikv/tikv/pull/4615)
-   不明なログを修正する[＃4730](https://github.com/tikv/tikv/pull/4730)

## ツール {#tools}

-   TiDB Lightning
    -   [＃176](https://github.com/pingcap/tidb-lightning/pull/176)が13へのデータ送信に失敗した場合の再試行機能を追加し`importer`
-   TiDB Binlog
    -   トラブルシューティングを容易にするためにポンプ貯蔵ログを最適化する[＃607](https://github.com/pingcap/tidb-binlog/pull/607)

## TiDB Ansible {#tidb-ansible}

-   TiDB Lightningの構成ファイルを更新し、 `tidb_lightning_ctl`のスクリプトを追加します[＃d3a4a368](https://github.com/pingcap/tidb-ansible/commit/d3a4a368810a421c49980899a286cf010569b4c7)
