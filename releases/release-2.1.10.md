---
title: TiDB 2.1.10 Release Notes
summary: TiDB 2.1.10は、2019年5月22日にリリースされ、様々なバグ修正と改善が行われました。このリリースには、テーブルスキーマ、読み取り結果、生成列、日時関数、スローログなどに関する問題の修正が含まれています。さらに、TiKV、 TiDB Lightning 、TiDB Binlogなどのツールにも改善が加えられました。TiDB Ansibleバージョン2.1.10もアップデートされました。
---

# TiDB 2.1.10 リリースノート {#tidb-2-1-10-release-notes}

発売日：2019年5月22日

TiDB バージョン: 2.1.10

TiDB Ansible バージョン: 2.1.10

## TiDB {#tidb}

-   `tidb_snapshot`使用して履歴データ[＃10359](https://github.com/pingcap/tidb/pull/10359)読み取るときに、一部の異常によりテーブル スキーマが正しくなくなる問題を修正しました。
-   `NOT`関数が場合によっては誤った読み取り結果を引き起こす問題を修正[＃10363](https://github.com/pingcap/tidb/pull/10363)
-   `Replace`または`Insert on duplicate update`ステートメント[＃10385](https://github.com/pingcap/tidb/pull/10385)の`Generated Column`の誤った動作を修正します
-   `DATE` `DATETIME` [＃10407](https://github.com/pingcap/tidb/pull/10407)の`BETWEEN`機能のバグを修正
-   `SLOW_QUERY`テーブルを使用してスローログ[＃10412](https://github.com/pingcap/tidb/pull/10412)をクエリするときに、スローログの 1 行が長すぎるとエラー レポートが発生する問題を修正しました。
-   `DATETIME` + `INTERVAL`の結果が MySQL の結果と一致しないケースがある問題を修正[＃10416](https://github.com/pingcap/tidb/pull/10416) , [＃10418](https://github.com/pingcap/tidb/pull/10418)
-   うるう年の2月の無効な時刻のチェックを追加[＃10417](https://github.com/pingcap/tidb/pull/10417)
-   クラスタ[＃10426](https://github.com/pingcap/tidb/pull/10426)初期化時に多数の競合エラーレポートを回避するために、DDL所有者でのみ内部初期化操作の制限を実行します。
-   出力タイムスタンプ列のデフォルト値が`default current_timestamp on update current_timestamp` [＃10337](https://github.com/pingcap/tidb/issues/10337)の場合、 `DESC` MySQLと互換性がない問題を修正しました。
-   `Update`文[＃10439](https://github.com/pingcap/tidb/pull/10439)の権限チェック中にエラーが発生する問題を修正
-   `RANGE`の計算を間違えると、場合によっては`CHAR`列に間違った結果が出る問題を修正しました[＃10455](https://github.com/pingcap/tidb/pull/10455)
-   `SHARD_ROW_ID_BITS` [＃9868](https://github.com/pingcap/tidb/pull/9868)減らした後にデータが上書きされる可能性がある問題を修正
-   `ORDER BY RAND()`ランダムな数字を返さない問題を修正[＃10064](https://github.com/pingcap/tidb/pull/10064)
-   小数点以下の精度を変更する`ALTER`文を禁止する[＃10458](https://github.com/pingcap/tidb/pull/10458)
-   MySQL [＃10474](https://github.com/pingcap/tidb/pull/10474)との`TIME_FORMAT`関数の互換性の問題を修正
-   `PERIOD_ADD` [＃10430](https://github.com/pingcap/tidb/pull/10430)のパラメータの有効性を確認する
-   TiDBの無効な`YEAR`文字列の動作がMySQL [＃10493](https://github.com/pingcap/tidb/pull/10493)と互換性がない問題を修正しました。
-   `ALTER DATABASE`構文[＃10503](https://github.com/pingcap/tidb/pull/10503)サポートする
-   低速クエリステートメント[＃10536](https://github.com/pingcap/tidb/pull/10536)に`;`存在しない場合に`SLOW_QUERY`メモリエンジンがエラーを報告する問題を修正しました
-   パーティションテーブルでの`Add index`がキャンセルできないことがある問題を修正[＃10533](https://github.com/pingcap/tidb/pull/10533)
-   OOMpanic回復できないケースがある問題を修正[＃10545](https://github.com/pingcap/tidb/pull/10545)
-   テーブルメタデータを書き換えるDDL操作のセキュリティを強化する[＃10547](https://github.com/pingcap/tidb/pull/10547)

## PD {#pd}

-   リーダーの優先順位が有効にならない問題を修正[＃1533](https://github.com/pingcap/pd/pull/1533)

## TiKV {#tikv}

-   転送の失敗を回避するために、最近構成が変更されたリージョンのリーダーの転送を拒否します[＃4684](https://github.com/tikv/tikv/pull/4684)
-   コプロセッサーメトリック[＃4643](https://github.com/tikv/tikv/pull/4643)の優先ラベルを追加します
-   リーダー[＃4724](https://github.com/tikv/tikv/pull/4724)転送中に発生する可能性のあるダーティ リード問題を修正しました
-   `CommitMerge`一部のケースでTiKVの再起動が失敗する問題を修正[＃4615](https://github.com/tikv/tikv/pull/4615)
-   不明なログ[＃4730](https://github.com/tikv/tikv/pull/4730)を修正

## ツール {#tools}

-   TiDB Lightning
    -   TiDB Lightningが`importer` [＃176](https://github.com/pingcap/tidb-lightning/pull/176)へのデータ送信に失敗した場合の再試行機能を追加
-   TiDBBinlog
    -   トラブルシューティングを容易にするためにPumpstorageログを最適化します[＃607](https://github.com/pingcap/tidb-binlog/pull/607)

## TiDB アンシブル {#tidb-ansible}

-   TiDB Lightningの設定ファイルを更新し、 `tidb_lightning_ctl`スクリプト[#d3a4a368](https://github.com/pingcap/tidb-ansible/commit/d3a4a368810a421c49980899a286cf010569b4c7)を追加します。
