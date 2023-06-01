---
title: TiDB 2.0.4 Release Notes
---

# TiDB 2.0.4 リリースノート {#tidb-2-0-4-release-notes}

2018 年 6 月 15 日に、TiDB 2.0.4 がリリースされました。 TiDB 2.0.3 と比較して、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   `ALTER TABLE t DROP COLUMN a CASCADE`構文をサポートする
-   TSO への`tidb_snapshot`の値の構成のサポート
-   監視項目のステートメントの種類の表示を絞り込む
-   クエリコスト推定の精度を最適化する
-   gRPCの`backoff max delay`パラメータを設定する
-   構成ファイル内の単一ステートメントのメモリしきい値の構成をサポート
-   オプティマイザーのエラーをリファクタリングする
-   `Cast Decimal`データの副作用を修正
-   特定のシナリオにおける`Merge Join`オペレーターの間違った結果の問題を修正
-   Null オブジェクトを String に変換する問題を修正
-   JSON タイプのデータを JSON タイプにキャストする問題を修正します。
-   `Union` + `OrderBy`の条件でMySQLと結果の順序が一致しない問題を修正
-   `Union`ステートメントが`Limit/OrderBy`句をチェックするときのコンプライアンス ルールの問題を修正
-   `Union All`結果の互換性の問題を修正
-   述語プッシュダウンのバグを修正
-   `Union`ステートメントと`For Update`句の互換性の問題を修正
-   `concat_ws`関数が誤って結果を切り捨てる問題を修正

## PD {#pd}

-   最大数`PendingPeer`秒の制限なしに変更することで、未設定のスケジュール引数`max-pending-peer-count`の動作を改善しました。

## TiKV {#tikv}

-   デバッグ用に RocksDB `PerfContext`インターフェイスを追加する
-   `import-mode`パラメータを削除します
-   `region-properties`コマンドを`tikv-ctl`に追加します
-   RocksDB のトゥームストーンが多数存在すると`reverse-seek`が遅くなる問題を修正
-   `do_sub`によって引き起こされるクラッシュの問題を修正
-   GC が多くのバージョンのデータに遭遇したときに GC にログを記録させる
