---
title: TiDB 2.0.6 Release Notes
summary: TiDB 2.0.6 は、システムの互換性と安定性の向上を伴い、2018 年 8 月 6 日にリリースされました。このリリースには、TiDB と TiKV のさまざまな改善とバグ修正が含まれています。注目すべき改善点としては、トランザクションの競合の削減、行数の推定精度の向上、`ANALYZE TABLE` 実行中のパニックに対する回復メカニズムの追加などがあります。バグ修正では、互換性のない `DROP USER` ステートメントの動作、`INSERT`/`LOAD DATA` ステートメントの OOM エラー、プレフィックス インデックスと `DECIMAL` 操作の誤った結果などの問題に対処しています。TiKV では、スケジューラ スロット、ロールバック トランザクション レコード、RocksDB ログ ファイル管理の改善、およびデータ型変換中のクラッシュ問題の修正も行われています。
---

# TiDB 2.0.6 リリースノート {#tidb-2-0-6-release-notes}

2018 年 8 月 6 日に、TiDB 2.0.6 がリリースされました。TiDB 2.0.5 と比較して、このリリースではシステムの互換性と安定性が大幅に向上しています。

## ティビ {#tidb}

-   改善点
    -   ディスク容量を節約するために「システム変数の設定」ログを短くする[＃7031](https://github.com/pingcap/tidb/pull/7031)
    -   `ADD INDEX`の実行中に遅い操作をログに記録して、トラブルシューティングを容易にする[＃7083](https://github.com/pingcap/tidb/pull/7083)
    -   統計情報の更新時にトランザクションの競合を減らす[＃7138](https://github.com/pingcap/tidb/pull/7138)
    -   推定待ちの値が統計範囲[＃7185](https://github.com/pingcap/tidb/pull/7185)を超える場合の行数推定の精度を向上
    -   実行効率を向上させるために、 `Index Join`の外部テーブルとして推定行数が少ないテーブルを選択します[＃7277](https://github.com/pingcap/tidb/pull/7277)
    -   `ANALYZE TABLE`の実行中に発生したパニックに対する回復メカニズムを追加し、統計[＃7228](https://github.com/pingcap/tidb/pull/7228)を収集するプロセスでの異常な動作によって tidb サーバーが利用できなくなるのを回避します。
    -   `RPAD`の結果が`max_allowed_packet`システム変数の値を超えた場合に`NULL`と対応する警告を返し、MySQL [＃7244](https://github.com/pingcap/tidb/pull/7244)と互換性があります`LPAD`
    -   `PREPARE`ステートメントのプレースホルダ数の上限を 65535 に設定し、MySQL [＃7250](https://github.com/pingcap/tidb/pull/7250)と互換性を持たせます。
-   バグの修正
    -   `DROP USER`文が場合によっては MySQL の動作と互換性がない問題を修正[＃7014](https://github.com/pingcap/tidb/pull/7014)
    -   `INSERT` / `LOAD DATA`のような文が`tidb_batch_insert` [＃7092](https://github.com/pingcap/tidb/pull/7092)を開いた後にOOMに遭遇する問題を修正
    -   テーブルのデータが更新され続けると統計が自動的に更新されない問題を修正[＃7093](https://github.com/pingcap/tidb/pull/7093)
    -   ファイアウォールが非アクティブな gPRC 接続を切断する問題を修正[＃7099](https://github.com/pingcap/tidb/pull/7099)
    -   一部のシナリオでプレフィックスインデックスが間違った結果を返す問題を修正[＃7126](https://github.com/pingcap/tidb/pull/7126)
    -   いくつかのシナリオで古い統計情報によって引き起こされるpanicの問題を修正[＃7155](https://github.com/pingcap/tidb/pull/7155)
    -   いくつかのシナリオで`ADD INDEX`操作後にインデックス データが 1 つ失われる問題を修正[＃7156](https://github.com/pingcap/tidb/pull/7156)
    -   いくつかのシナリオで一意のインデックスを使用して`NULL`値をクエリしたときに間違った結果が返される問題を修正しました[＃7172](https://github.com/pingcap/tidb/pull/7172)
    -   いくつかのシナリオにおける`DECIMAL`乗算結果の乱雑なコード問題を修正[＃7212](https://github.com/pingcap/tidb/pull/7212)
    -   いくつかのシナリオで`DECIMAL`剰余演算の誤った結果の問題を修正[＃7245](https://github.com/pingcap/tidb/pull/7245)
    -   トランザクション内の`UPDATE`ステートメント`DELETE` 、一部の特殊なステートメントシーケンスで誤った結果を返す問題を修正しました[＃7219](https://github.com/pingcap/tidb/pull/7219)
    -   いくつかのシナリオで実行プランを`UPDATE`するプロセス中に`UNION ALL`ステートメントのpanic問題を修正しました[＃7225](https://github.com/pingcap/tidb/pull/7225)
    -   一部のシナリオでプレフィックスインデックスの範囲が正しく計算されない問題を修正[＃7231](https://github.com/pingcap/tidb/pull/7231)
    -   `LOAD DATA`ステートメントが一部のシナリオでbinlogの書き込みに失敗する問題を修正[＃7242](https://github.com/pingcap/tidb/pull/7242)
    -   いくつかのシナリオ[＃7243](https://github.com/pingcap/tidb/pull/7243)で`ADD INDEX`の実行プロセス中に`SHOW CREATE TABLE`の誤った結果の問題を修正しました
    -   `Index Join`一部のシナリオでタイムスタンプを初期化しないとpanicが発生する問題を修正[＃7246](https://github.com/pingcap/tidb/pull/7246)
    -   セッション[＃7258](https://github.com/pingcap/tidb/pull/7258)でタイムゾーンを`ADMIN CHECK TABLE`て使用した場合の誤報問題を修正
    -   `ADMIN CLEANUP INDEX`一部のシナリオでインデックスがクリーンアップされない問題を修正[＃7265](https://github.com/pingcap/tidb/pull/7265)
    -   読み取りコミット分離レベル[＃7282](https://github.com/pingcap/tidb/pull/7282)を無効にする

## ティクヴ {#tikv}

-   改善点
    -   スケジューラのデフォルトスロットを拡大して誤った競合を減らす
    -   ロールバックトランザクションの連続記録を減らし、競合が極めて深刻な場合の読み取りパフォーマンスを改善します。
    -   RocksDB ログファイルのサイズと数を制限し、長時間実行時の不要なディスク使用量を削減します。
-   バグの修正
    -   データ型を文字列から小数点に変換するときに発生するクラッシュの問題を修正
