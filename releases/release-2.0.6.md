---
title: TiDB 2.0.6 Release Notes
---

# TiDB 2.0.6 リリースノート {#tidb-2-0-6-release-notes}

2018 年 8 月 6 日に、TiDB 2.0.6 がリリースされました。 TiDB 2.0.5 と比較して、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   改善点
    -   ディスク容量を節約するために「システム変数の設定」ログを短くする[#7031](https://github.com/pingcap/tidb/pull/7031)
    -   トラブルシューティングを容易にするために、 `ADD INDEX`の実行中に遅い操作をログに記録します[#7083](https://github.com/pingcap/tidb/pull/7083)
    -   統計情報を更新する際のトランザクションの競合を軽減する[#7138](https://github.com/pingcap/tidb/pull/7138)
    -   推定保留中の値が統計範囲[#7185](https://github.com/pingcap/tidb/pull/7185)を超える場合の行数推定の精度を向上させます。
    -   実行効率を向上させるために、 `Index Join`外部テーブルとして推定行数が小さいテーブルを選択します[#7277](https://github.com/pingcap/tidb/pull/7277)
    -   統計[#7228](https://github.com/pingcap/tidb/pull/7228)収集プロセスにおける異常な動作によって tidb サーバーが使用できなくなることを避けるために、 `ANALYZE TABLE`の実行中に発生したパニックに対する回復メカニズムを追加します。
    -   `RPAD` / `LPAD`の結果が`max_allowed_packet`システム変数の値を超えた場合、 `NULL`と対応する警告を返します。MySQL [#7244](https://github.com/pingcap/tidb/pull/7244)と互換性があります。
    -   `PREPARE`ステートメントのプレースホルダー数の上限を 65535 に設定します (MySQL [#7250](https://github.com/pingcap/tidb/pull/7250)と互換性があります)。
-   バグの修正
    -   `DROP USER`ステートメントが場合によっては MySQL の動作と互換性がない問題を修正[#7014](https://github.com/pingcap/tidb/pull/7014)
    -   `tidb_batch_insert` [#7092](https://github.com/pingcap/tidb/pull/7092)を開いた後に`INSERT` / `LOAD DATA`のようなステートメントが OOM を満たす問題を修正
    -   テーブルのデータが更新され続けると統計が自動的に更新されない問題を修正します[#7093](https://github.com/pingcap/tidb/pull/7093)
    -   ファイアウォールが非アクティブな gPRC 接続を切断する問題を修正します[#7099](https://github.com/pingcap/tidb/pull/7099)
    -   一部のシナリオでプレフィックス インデックスが間違った結果を返す問題を修正[#7126](https://github.com/pingcap/tidb/pull/7126)
    -   一部のシナリオで古い統計が原因で発生するpanicの問題を修正します[#7155](https://github.com/pingcap/tidb/pull/7155)
    -   一部のシナリオ[#7156](https://github.com/pingcap/tidb/pull/7156)で`ADD INDEX`操作後にインデックス データが 1 つ欠落する問題を修正します。
    -   一部のシナリオで一意のインデックスを使用して`NULL`値をクエリするときの間違った結果の問題を修正します[#7172](https://github.com/pingcap/tidb/pull/7172)
    -   一部のシナリオでの`DECIMAL`乗算結果の乱雑なコードの問題を修正[#7212](https://github.com/pingcap/tidb/pull/7212)
    -   一部のシナリオでの`DECIMAL`モジュロ演算の間違った結果の問題を修正[#7245](https://github.com/pingcap/tidb/pull/7245)
    -   トランザクション内の`UPDATE` / `DELETE`ステートメントが、ステートメントの特別なシーケンスの下で間違った結果を返す問題を修正します[#7219](https://github.com/pingcap/tidb/pull/7219)
    -   一部のシナリオで実行計画を構築するプロセス中の`UNION ALL` / `UPDATE`ステートメントのpanicの問題を修正します[#7225](https://github.com/pingcap/tidb/pull/7225)
    -   一部のシナリオでプレフィックス インデックスの範囲が正しく計算されない問題を修正します[#7231](https://github.com/pingcap/tidb/pull/7231)
    -   一部のシナリオで`LOAD DATA`ステートメントがbinlogの書き込みに失敗する問題を修正します[#7242](https://github.com/pingcap/tidb/pull/7242)
    -   一部のシナリオで`ADD INDEX`実行プロセス中に`SHOW CREATE TABLE`の間違った結果が発生する問題を修正[#7243](https://github.com/pingcap/tidb/pull/7243)
    -   一部のシナリオで`Index Join`タイムスタンプを初期化しない場合にpanicが発生する問題を修正[#7246](https://github.com/pingcap/tidb/pull/7246)
    -   `ADMIN CHECK TABLE`セッション[#7258](https://github.com/pingcap/tidb/pull/7258)で誤ってタイムゾーンを使用した場合の誤ったアラームの問題を修正します。
    -   一部のシナリオで`ADMIN CLEANUP INDEX`がインデックスをクリーンアップしない問題を修正[#7265](https://github.com/pingcap/tidb/pull/7265)
    -   Read Committed 分離レベル[#7282](https://github.com/pingcap/tidb/pull/7282)を無効にします。

## TiKV {#tikv}

-   改善点
    -   誤った競合を減らすためにスケジューラのデフォルトのスロットを拡大します。
    -   競合が非常に深刻な場合の読み取りパフォーマンスを向上させるために、ロールバック トランザクションの継続的な記録を削減します。
    -   RocksDB ログ ファイルのサイズと数を制限し、長時間実行状態での不必要なディスク使用量を削減します。
-   バグの修正
    -   データ型を文字列から 10 進数に変換する際のクラッシュ問題を修正
