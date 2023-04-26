---
title: TiDB 2.0.6 Release Notes
---

# TiDB 2.0.6 リリースノート {#tidb-2-0-6-release-notes}

2018 年 8 月 6 日に、TiDB 2.0.6 がリリースされました。 TiDB 2.0.5 と比較すると、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   改良点
    -   ディスク容量を節約するために「システム変数の設定」ログを短くする[#7031](https://github.com/pingcap/tidb/pull/7031)
    -   `ADD INDEX`の実行中に遅い操作をログに記録し、トラブルシューティングを容易にします[#7083](https://github.com/pingcap/tidb/pull/7083)
    -   統計更新時のトランザクションの競合を減らす[#7138](https://github.com/pingcap/tidb/pull/7138)
    -   推定保留中の値が統計範囲[#7185](https://github.com/pingcap/tidb/pull/7185)を超える場合の行数推定の精度を向上させます。
    -   `Index Join`の外部表として、推定行数の少ない表を選択し、実行効率を向上させる[#7277](https://github.com/pingcap/tidb/pull/7277)
    -   `ANALYZE TABLE`の実行中に発生したパニックの回復メカニズムを追加して、統計収集プロセスの異常な動作が原因で tidb-server が使用できなくなることを回避します[#7228](https://github.com/pingcap/tidb/pull/7228)
    -   `RPAD` / `LPAD`の結果が`max_allowed_packet`システム変数の値を超えると、 `NULL`と対応する警告が返されます。MySQL [#7244](https://github.com/pingcap/tidb/pull/7244)と互換性があります。
    -   `PREPARE`ステートメントのプレースホルダー数の上限を 65535 に設定し、MySQL [#7250](https://github.com/pingcap/tidb/pull/7250)と互換性があります
-   バグの修正
    -   場合によっては`DROP USER`ステートメントが MySQL の動作と互換性がないという問題を修正します[#7014](https://github.com/pingcap/tidb/pull/7014)
    -   `tidb_batch_insert` [#7092](https://github.com/pingcap/tidb/pull/7092)を開いた後、 `INSERT` / `LOAD DATA`のようなステートメントが OOM を満たす問題を修正します。
    -   テーブルのデータが更新され続けると、統計が自動的に更新されない問題を修正します[#7093](https://github.com/pingcap/tidb/pull/7093)
    -   ファイアウォールが非アクティブな gPRC 接続を切断する問題を修正します[#7099](https://github.com/pingcap/tidb/pull/7099)
    -   一部のシナリオでプレフィックス インデックスが間違った結果を返す問題を修正します[#7126](https://github.com/pingcap/tidb/pull/7126)
    -   一部のシナリオで古い統計が原因で発生するpanicの問題を修正します[#7155](https://github.com/pingcap/tidb/pull/7155)
    -   一部のシナリオで`ADD INDEX`操作後に 1 つのインデックス データが欠落する問題を修正[#7156](https://github.com/pingcap/tidb/pull/7156)
    -   一部のシナリオで一意のインデックスを使用して`NULL`値をクエリするときの間違った結果の問題を修正します[#7172](https://github.com/pingcap/tidb/pull/7172)
    -   一部のシナリオでの`DECIMAL`乗算結果の乱雑なコードの問題を修正します[#7212](https://github.com/pingcap/tidb/pull/7212)
    -   一部のシナリオでの`DECIMAL`モジュロ演算の間違った結果の問題を修正[#7245](https://github.com/pingcap/tidb/pull/7245)
    -   トランザクションの`UPDATE` / `DELETE`ステートメントが、ステートメントの特別なシーケンスの下で間違った結果を返す問題を修正します[#7219](https://github.com/pingcap/tidb/pull/7219)
    -   一部のシナリオで実行計画を作成するプロセス中の`UNION ALL` / `UPDATE`ステートメントのpanicの問題を修正します[#7225](https://github.com/pingcap/tidb/pull/7225)
    -   一部のシナリオでプレフィックス インデックスの範囲が正しく計算されない問題を修正します[#7231](https://github.com/pingcap/tidb/pull/7231)
    -   一部のシナリオで`LOAD DATA`ステートメントがbinlog の書き込みに失敗する問題を修正します[#7242](https://github.com/pingcap/tidb/pull/7242)
    -   一部のシナリオで`ADD INDEX`の実行プロセス中に`SHOW CREATE TABLE`の間違った結果の問題を修正[#7243](https://github.com/pingcap/tidb/pull/7243)
    -   `Index Join`一部のシナリオでタイムスタンプを初期化しないとpanicが発生する問題を修正[#7246](https://github.com/pingcap/tidb/pull/7246)
    -   `ADMIN CHECK TABLE`セッションで誤ってタイムゾーンを使用した場合の誤報の問題を修正[#7258](https://github.com/pingcap/tidb/pull/7258)
    -   一部のシナリオで`ADMIN CLEANUP INDEX`がインデックスをクリーンアップしない問題を修正します[#7265](https://github.com/pingcap/tidb/pull/7265)
    -   Read Committed 分離レベル[#7282](https://github.com/pingcap/tidb/pull/7282)を無効にする

## TiKV {#tikv}

-   改良点
    -   スケジューラのデフォルト スロットを拡大して、誤った競合を減らします
    -   競合が非常に深刻な場合の読み取りパフォーマンスを向上させるために、ロールバック トランザクションの継続的な記録を減らします。
    -   RocksDB ログ ファイルのサイズと数を制限して、長時間実行状態での不要なディスク使用量を減らします
-   バグの修正
    -   データ型を文字列から 10 進数に変換する際のクラッシュの問題を修正
