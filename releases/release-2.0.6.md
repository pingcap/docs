---
title: TiDB 2.0.6 Release Notes
summary: TiDB 2.0.6は、システムの互換性と安定性の向上を伴い、2018年8月6日にリリースされました。このリリースには、TiDBとTiKVの様々な改善とバグ修正が含まれています。主な改善点としては、トランザクションの競合の削減、行数推定精度の向上、ANALYZE TABLE実行中のパニックに対するリカバリメカニズムの追加などが挙げられます。バグ修正では、互換性のないDROP USER文の動作、INSERT/LOAD DATA文のOOMエラー、プレフィックスインデックスとDECIMAL操作の誤った結果などの問題が修正されています。TiKVでは、スケジューラスロット、ロールバックトランザクションレコード、RocksDBログファイル管理の改善に加え、データ型変換中のクラッシュ問題も修正されています。
---

# TiDB 2.0.6 リリースノート {#tidb-2-0-6-release-notes}

2018年8月6日にTiDB 2.0.6がリリースされました。TiDB 2.0.5と比較して、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   改善点
    -   ディスク容量を節約するために「システム変数の設定」ログを短くする[＃7031](https://github.com/pingcap/tidb/pull/7031)
    -   `ADD INDEX`の実行中に遅い操作をログに記録して、トラブルシューティングを容易にします[＃7083](https://github.com/pingcap/tidb/pull/7083)
    -   統計情報の更新時にトランザクションの競合を減らす[＃7138](https://github.com/pingcap/tidb/pull/7138)
    -   推定待ちの値が統計範囲[＃7185](https://github.com/pingcap/tidb/pull/7185)を超える場合の行数推定の精度を向上
    -   実行効率を向上させるために、 `Index Join`の外部テーブルとして推定行数が少ないテーブルを選択します[＃7277](https://github.com/pingcap/tidb/pull/7277)
    -   `ANALYZE TABLE`の実行中に発生したパニックに対する回復メカニズムを追加し、統計[＃7228](https://github.com/pingcap/tidb/pull/7228)収集するプロセスでの異常な動作によって tidb サーバーが利用できなくなることを回避します。
    -   `RPAD`の結果が`max_allowed_packet`システム変数の値を超えた場合、 `NULL`と対応する警告を返し、MySQL [＃7244](https://github.com/pingcap/tidb/pull/7244)と互換性があります`LPAD`
    -   `PREPARE`文のプレースホルダ数の上限を 65535 に設定し、MySQL [＃7250](https://github.com/pingcap/tidb/pull/7250)と互換性を持たせます。
-   バグ修正
    -   `DROP USER`文が場合によっては MySQL の動作と互換性がない問題を修正[＃7014](https://github.com/pingcap/tidb/pull/7014)
    -   `INSERT` / `LOAD DATA`のような文が`tidb_batch_insert` [＃7092](https://github.com/pingcap/tidb/pull/7092)を開いた後にOOMに遭遇する問題を修正しました
    -   テーブルのデータが更新され続けると統計が自動的に更新されない問題を修正しました[＃7093](https://github.com/pingcap/tidb/pull/7093)
    -   ファイアウォールが非アクティブな gPRC 接続を切断する問題を修正[＃7099](https://github.com/pingcap/tidb/pull/7099)
    -   一部のシナリオでプレフィックスインデックスが間違った結果を返す問題を修正[＃7126](https://github.com/pingcap/tidb/pull/7126)
    -   一部のシナリオで古い統計情報によって引き起こされるpanicの問題を修正[＃7155](https://github.com/pingcap/tidb/pull/7155)
    -   いくつかのシナリオで`ADD INDEX`操作後にインデックスデータの1つが失われる問題を修正しました[＃7156](https://github.com/pingcap/tidb/pull/7156)
    -   一部のシナリオでユニークインデックスを使用して`NULL`値をクエリしたときに間違った結果が返される問題を修正しました[＃7172](https://github.com/pingcap/tidb/pull/7172)
    -   いくつかのシナリオにおける`DECIMAL`乗算結果のコードの乱雑な問題を修正[＃7212](https://github.com/pingcap/tidb/pull/7212)
    -   いくつかのシナリオで`DECIMAL`剰余演算の誤った結果の問題を修正[＃7245](https://github.com/pingcap/tidb/pull/7245)
    -   トランザクション内の`UPDATE`ステートメントが`DELETE`いくつかの特殊なステートメントシーケンスで間違った結果を返す問題を修正しました[＃7219](https://github.com/pingcap/tidb/pull/7219)
    -   いくつかのシナリオで実行プランを構築するプロセス中に`UNION ALL` `UPDATE`のpanic問題を修正しました[＃7225](https://github.com/pingcap/tidb/pull/7225)
    -   一部のシナリオでプレフィックスインデックスの範囲が正しく計算されない問題を修正[＃7231](https://github.com/pingcap/tidb/pull/7231)
    -   `LOAD DATA`文が一部のシナリオでbinlogの書き込みに失敗する問題を修正[＃7242](https://github.com/pingcap/tidb/pull/7242)
    -   いくつかのシナリオ[＃7243](https://github.com/pingcap/tidb/pull/7243)で`ADD INDEX`実行プロセス中に`SHOW CREATE TABLE`の間違った結果の問題を修正しました
    -   `Index Join`一部のシナリオでタイムスタンプを初期化しないとpanicが発生する問題を修正[＃7246](https://github.com/pingcap/tidb/pull/7246)
    -   セッション[＃7258](https://github.com/pingcap/tidb/pull/7258)でタイムゾーンを誤って使用した`ADMIN CHECK TABLE`の誤報問題を修正
    -   `ADMIN CLEANUP INDEX`一部のシナリオでインデックスがクリーンアップされない問題を修正[＃7265](https://github.com/pingcap/tidb/pull/7265)
    -   読み取りコミット分離レベル[＃7282](https://github.com/pingcap/tidb/pull/7282)を無効にする

## TiKV {#tikv}

-   改善点
    -   スケジューラのデフォルトスロットを拡大して誤った競合を減らす
    -   ロールバックトランザクションの連続記録を減らし、競合が極めて深刻な場合の読み取りパフォーマンスを改善します。
    -   RocksDB ログファイルのサイズと数を制限し、長時間実行時の不要なディスク使用量を削減します。
-   バグ修正
    -   データ型を文字列から小数点に変換するときに発生するクラッシュの問題を修正しました
