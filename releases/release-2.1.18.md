---
title: TiDB 2.1.18 Release Notes
---

# TiDB 2.1.18 リリースノート {#tidb-2-1-18-release-notes}

発売日：2019年11月4日

TiDB バージョン: 2.1.18

TiDB アンシブル バージョン: 2.1.18

## TiDB {#tidb}

-   SQL オプティマイザー
    -   フィードバック[#12172](https://github.com/pingcap/tidb/pull/12172)で分割すると、無効なクエリ範囲が表示される可能性がある問題を修正します
    -   ポイントゲットプラン[#12341](https://github.com/pingcap/tidb/pull/12341)で権限チェックが正しくない問題を修正
    -   Limit 演算子を`IndexLookUpReader`実行ロジック[#12380](https://github.com/pingcap/tidb/pull/12380)まで押し下げて、 `select ... limit ... offset …`ステートメントの実行パフォーマンスを最適化します。
    -   `ORDER BY` 、 `GROUP BY`および`LIMIT OFFSET`のパラメーターを使用したサポート[#12514](https://github.com/pingcap/tidb/pull/12514)
    -   パーティション テーブルの`IndexJoin`が間違った結果を返す問題を修正[#12713](https://github.com/pingcap/tidb/pull/12713)
    -   日付文字列とフォーマット文字列が一致しない場合、TiDB の`str_to_date`関数が MySQL とは異なる結果を返す問題を修正します[#12757](https://github.com/pingcap/tidb/pull/12757)
    -   クエリ条件に`cast`関数が含まれている場合、外部結合が内部結合に誤って変換される問題を修正[#12791](https://github.com/pingcap/tidb/pull/12791)
    -   `AntiSemiJoin` [#12800](https://github.com/pingcap/tidb/pull/12800)の結合条件で誤った式を渡す問題を修正
-   SQL エンジン
    -   時間の誤った丸めを修正します (たとえば、 `2019-09-11 11:17:47.999999666` `2019-09-11 11:17:48`に丸める必要があります) [#12259](https://github.com/pingcap/tidb/pull/12259)
    -   `PREPARE`ステートメントの期間が`sql_type`監視レコードに表示されない問題を修正します[#12329](https://github.com/pingcap/tidb/pull/12329)
    -   `from_unixtime`関数が null [#12572](https://github.com/pingcap/tidb/pull/12572)を処理するときのpanicの問題を修正
    -   無効な値が`YEAR`型として挿入されると、結果が`0000` [#12744](https://github.com/pingcap/tidb/pull/12744)ではなく`NULL`なるという互換性の問題を修正します。
    -   `AutoIncrement`列が暗黙的に割り当てられた場合の動作を改善し、MySQL 自動インクリメント ロックのデフォルト モードとの一貫性を保ちます ( [「連続」ロックモード](https://dev.mysql.com/doc/refman/5.7/en/innodb-auto-increment-handling.html) ): 1 行の`Insert`ステートメントで複数の`AutoIncrement` ID を暗黙的に割り当てる場合、TiDB は割り当てられた値の連続性。この改善により、JDBC `getGeneratedKeys()`メソッドがあらゆるシナリオで正しい結果を得ることが保証されます[#12619](https://github.com/pingcap/tidb/pull/12619)
    -   `HashAgg` `Apply` [#12769](https://github.com/pingcap/tidb/pull/12769)の子ノードになるとクエリがハングアップする問題を修正
    -   型変換時に`AND`と`OR`論理式が間違った結果を返す問題を修正[#12813](https://github.com/pingcap/tidb/pull/12813)
-   サーバ
    -   `SLEEP()`関数が`KILL TIDB QUERY`ステートメントに対して無効である問題を修正します[#12159](https://github.com/pingcap/tidb/pull/12159)
    -   `AUTO_INCREMENT` `MAX int64`と`MAX uint64` [#12210](https://github.com/pingcap/tidb/pull/12210)を誤って割り当てた場合にエラーが報告されない問題を修正
    -   ログ レベルが`ERROR` [#12373](https://github.com/pingcap/tidb/pull/12373)の場合、スロー クエリ ログが記録されない問題を修正します。
    -   TiDB がスキーマの変更とそれに対応する変更されたテーブル情報をキャッシュする回数を 100 から 1024 に調整し、 `tidb_max_delta_schema_count`システム変数[#12515](https://github.com/pingcap/tidb/pull/12515)を使用して変更をサポートします
    -   SQL統計をより正確にするために、クエリの開始時間を「実行開始」から「コンパイル開始」に変更します[#12638](https://github.com/pingcap/tidb/pull/12638)
    -   TiDB ログに`set session autocommit`のレコードを追加[#12568](https://github.com/pingcap/tidb/pull/12568)
    -   SQL クエリの開始時刻を`SessionVars`に記録して、プランの実行中にリセットされないようにする[#12676](https://github.com/pingcap/tidb/pull/12676)
    -   `ORDER BY` 、 `GROUP BY`および`LIMIT OFFSET` [#12514](https://github.com/pingcap/tidb/pull/12514)で`?`プレースホルダーをサポート
    -   スロー クエリ ログに`Prev_stmt`フィールドを追加して、最後のステートメントが`COMMIT` [#12724](https://github.com/pingcap/tidb/pull/12724)のときに前のステートメントを出力します。
    -   明示的にコミットされたトランザクションで`COMMIT`失敗した場合、 `COMMIT`より前の最後のステートメントをログに記録します[#12747](https://github.com/pingcap/tidb/pull/12747)
    -   TiDBサーバーがSQL ステートメントを実行するときの前のステートメントの保存方法を最適化して、パフォーマンスを向上させます[#12751](https://github.com/pingcap/tidb/pull/12751)
    -   `skip-grant-table=true`構成[#12816](https://github.com/pingcap/tidb/pull/12816)の下の`FLUSH PRIVILEGES`ステートメントによって引き起こされるpanic問題を修正します。
    -   AutoID を適用するデフォルトの最小ステップを`1000`から`30000`に増やして、短時間に多くの書き込み要求がある場合のパフォーマンスのボトルネックを回避します[#12891](https://github.com/pingcap/tidb/pull/12891)
    -   TiDB がパニック[#12954](https://github.com/pingcap/tidb/pull/12954)のときに、失敗した`Prepared`ステートメントがエラー ログに出力されない問題を修正します。
    -   スロー クエリ ログの`COM_STMT_FETCH`回のレコードが MySQL [#12953](https://github.com/pingcap/tidb/pull/12953)のレコードと一致しない問題を修正します。
    -   書き込み競合のエラー メッセージにエラー コードを追加して、原因をすばやく特定します[#12878](https://github.com/pingcap/tidb/pull/12878)
-   DDL
    -   デフォルトでは、列の`AUTO INCREMENT`属性のドロップを禁止します。この属性を削除する必要がある場合は、変数`tidb_allow_remove_auto_inc`値を変更してください。詳細については、 [システム変数](/system-variables.md#tidb_allow_remove_auto_inc-new-in-v2118-and-v304)参照してください。 [#12146](https://github.com/pingcap/tidb/pull/12146)
    -   `Create Table`ステートメントで一意のインデックスを作成するときに複数の`unique`をサポートします[#12469](https://github.com/pingcap/tidb/pull/12469)
    -   `CREATE TABLE`ステートメントの外部キー制約にスキーマがない場合、 `No Database selected`エラー[#12678](https://github.com/pingcap/tidb/pull/12678)を返す代わりに、作成されたテーブルのスキーマを使用する必要があるという互換性の問題を修正します。
    -   `ADMIN CANCEL DDL JOBS` [#12681](https://github.com/pingcap/tidb/pull/12681)を実行すると`invalid list index`エラーが報告される問題を修正
-   モニター
    -   バックオフ監視用のタイプを追加し、コミット時のバックオフ時間など、以前に記録されていないバックオフ時間を補足します[#12326](https://github.com/pingcap/tidb/pull/12326)
    -   `Add Index`操作の進行状況を監視するための新しいメトリックを追加する[#12389](https://github.com/pingcap/tidb/pull/12389)

## PD {#pd}

-   pd-ctl [#1772](https://github.com/pingcap/pd/pull/1772)の`--help`コマンド出力を改善

## ツール {#tools}

-   TiDBBinlog
    -   `ALTER DATABASE`関連する DDL 操作によってDrainerが異常終了する問題を修正[#770](https://github.com/pingcap/tidb-binlog/pull/770)
    -   コミットbinlogのトランザクション ステータス情報のクエリをサポートして、レプリケーションの効率を向上させます[#761](https://github.com/pingcap/tidb-binlog/pull/761)
    -   Drainer の`start_ts` Pump の最大の`commit_ts` [#759](https://github.com/pingcap/tidb-binlog/pull/759)より大きい場合、 Pumppanicが発生する可能性がある問題を修正します。

## TiDB アンシブル {#tidb-ansible}

-   TiDB Binlog [#952](https://github.com/pingcap/tidb-ansible/pull/952)に「キューサイズ」と「クエリヒストグラム」の2つの監視項目を追加
-   TiDB アラート ルールを更新する[#961](https://github.com/pingcap/tidb-ansible/pull/961)
-   展開とアップグレードの前に構成ファイルを確認する[#973](https://github.com/pingcap/tidb-ansible/pull/973)
-   TiDB [#987](https://github.com/pingcap/tidb-ansible/pull/987)でインデックス速度を監視するための新しいメトリックを追加します
-   TiDB Binlog監視ダッシュボードを更新して、Grafana v4.6.3 と互換性を持たせます[#993](https://github.com/pingcap/tidb-ansible/pull/993)
