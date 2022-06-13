---
title: TiDB 2.0.6 Release Notes
---

# TiDB2.0.6リリースノート {#tidb-2-0-6-release-notes}

2018年8月6日、TiDB2.0.6がリリースされました。 TiDB 2.0.5と比較して、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   改善
    -   ディスク容量を節約するために、「システム変数の設定」ログを短くします[＃7031](https://github.com/pingcap/tidb/pull/7031)
    -   トラブルシューティングを容易にするために、 `ADD INDEX`の実行中に遅い操作をログに記録します[＃7083](https://github.com/pingcap/tidb/pull/7083)
    -   統計を更新する際のトランザクションの競合を減らす[＃7138](https://github.com/pingcap/tidb/pull/7138)
    -   推定される保留中の値が統計範囲[＃7185](https://github.com/pingcap/tidb/pull/7185)を超える場合の行数推定の精度を向上させます
    -   実行効率を向上させるために、 `Index Join`の外部テーブルとして、推定行数が少ないテーブルを選択します[＃7277](https://github.com/pingcap/tidb/pull/7277)
    -   `ANALYZE TABLE`の実行中に発生したパニックの回復メカニズムを追加して、統計の収集プロセスでの異常な動作によってtidb-serverが使用できなくなるのを回避します[＃7228](https://github.com/pingcap/tidb/pull/7228)
    -   `LPAD`の結果が`RPAD`と互換性のある`max_allowed_packet`システム変数の値を超えると、 `NULL`と対応する警告を返し[＃7244](https://github.com/pingcap/tidb/pull/7244) 。
    -   MySQL [＃7250](https://github.com/pingcap/tidb/pull/7250)と互換性のある、 `PREPARE`ステートメントのプレースホルダー数の上限を65535に設定します
-   バグの修正
    -   `DROP USER`ステートメントがMySQLの動作と互換性がない場合があるという問題を修正します[＃7014](https://github.com/pingcap/tidb/pull/7014)
    -   `INSERT`のようなステートメントが`tidb_batch_insert`を開いた後に[＃7092](https://github.com/pingcap/tidb/pull/7092)を満たすという問題を修正し`LOAD DATA`
    -   テーブルのデータが更新され続けると、統計が自動的に更新されない問題を修正します[＃7093](https://github.com/pingcap/tidb/pull/7093)
    -   ファイアウォールが非アクティブなgPRC接続を切断する問題を修正します[＃7099](https://github.com/pingcap/tidb/pull/7099)
    -   一部のシナリオでプレフィックスインデックスが間違った結果を返す問題を修正します[＃7126](https://github.com/pingcap/tidb/pull/7126)
    -   一部のシナリオで古い統計によって引き起こされるパニックの問題を修正する[＃7155](https://github.com/pingcap/tidb/pull/7155)
    -   一部のシナリオで1回の操作後に`ADD INDEX`つのインデックスデータが失われる問題を修正します[＃7156](https://github.com/pingcap/tidb/pull/7156)
    -   一部のシナリオで一意のインデックスを使用して`NULL`の値をクエリするときの誤った結果の問題を修正します[＃7172](https://github.com/pingcap/tidb/pull/7172)
    -   一部のシナリオでの`DECIMAL`乗算結果の厄介なコードの問題を修正します[＃7212](https://github.com/pingcap/tidb/pull/7212)
    -   一部のシナリオでの`DECIMAL`のモジュロ演算の誤った結果の問題を修正します[＃7245](https://github.com/pingcap/tidb/pull/7245)
    -   トランザクションの`UPDATE`ステートメントが、ステートメントの特別なシーケンスの下で間違った結果を返す問題を修正し[＃7219](https://github.com/pingcap/tidb/pull/7219) `DELETE`
    -   一部のシナリオで実行プランを作成するプロセス中の`UNION ALL`ステートメントのパニックの問題を修正し[＃7225](https://github.com/pingcap/tidb/pull/7225) `UPDATE`
    -   一部のシナリオでプレフィックスインデックスの範囲が正しく計算されない問題を修正します[＃7231](https://github.com/pingcap/tidb/pull/7231)
    -   一部のシナリオで`LOAD DATA`ステートメントがbinlogの書き込みに失敗する問題を修正します[＃7242](https://github.com/pingcap/tidb/pull/7242)
    -   一部のシナリオでの`ADD INDEX`の実行プロセス中の`SHOW CREATE TABLE`の誤った結果の問題を修正します[＃7243](https://github.com/pingcap/tidb/pull/7243)
    -   一部のシナリオで`Index Join`がタイムスタンプを初期化しない場合にパニックが発生する問題を修正します[＃7246](https://github.com/pingcap/tidb/pull/7246)
    -   `ADMIN CHECK TABLE`がセッション[＃7258](https://github.com/pingcap/tidb/pull/7258)でタイムゾーンを誤って使用した場合の誤警報の問題を修正します。
    -   一部のシナリオで`ADMIN CLEANUP INDEX`がインデックスをクリーンアップしないという問題を修正します[＃7265](https://github.com/pingcap/tidb/pull/7265)
    -   読み取りコミット分離レベル[＃7282](https://github.com/pingcap/tidb/pull/7282)を無効にする

## TiKV {#tikv}

-   改善
    -   スケジューラのデフォルトスロットを拡大して、誤った競合を減らします
    -   競合が非常に深刻な場合の読み取りパフォーマンスを向上させるために、ロールバックトランザクションの継続的な記録を減らします
    -   RocksDBログファイルのサイズと数を制限して、長時間実行状態での不要なディスク使用量を減らします
-   バグの修正
    -   データ型を文字列から10進数に変換するときのクラッシュの問題を修正しました
