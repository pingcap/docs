---
title: TiDB 2.0.4 Release Notes
---

# TiDB 2.0.4 リリースノート {#tidb-2-0-4-release-notes}

2018 年 6 月 15 日に、TiDB 2.0.4 がリリースされました。 TiDB 2.0.3 と比較すると、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   `ALTER TABLE t DROP COLUMN a CASCADE`構文をサポート
-   `tidb_snapshot`の値を TSO に構成するサポート
-   監視項目の明細書種別の表示を絞り込む
-   クエリのコスト見積もりの精度を最適化する
-   gRPC の`backoff max delay`パラメータを設定する
-   構成ファイル内の単一ステートメントのメモリしきい値の構成をサポート
-   Optimizer のエラーをリファクタリングする
-   `Cast Decimal`データの副作用を修正
-   特定のシナリオでの`Merge Join`演算子の間違った結果の問題を修正
-   Null オブジェクトを String に変換する問題を修正
-   JSON 型のデータを JSON 型にキャストする問題を修正します。
-   `Union` + `OrderBy`の条件で結果の順序が MySQL と一致しない問題を修正
-   `Union`ステートメントが`Limit/OrderBy`句をチェックするときのコンプライアンス ルールの問題を修正します。
-   `Union All`件の結果の互換性の問題を修正
-   述語プッシュダウンのバグを修正
-   `Union`文と`For Update`句の互換性の問題を修正
-   `concat_ws`関数が誤って結果を切り捨てる問題を修正

## PD {#pd}

-   設定されていないスケジューリング引数`max-pending-peer-count`の動作を、最大数`PendingPeer`の制限なしに変更して改善します。

## TiKV {#tikv}

-   デバッグ用に RocksDB `PerfContext`インターフェイスを追加する
-   `import-mode`パラメータを削除します
-   `tikv-ctl`の`region-properties`コマンドを追加します。
-   RocksDB tombstone が多数存在する場合に`reverse-seek`が遅くなる問題を修正
-   `do_sub`によって引き起こされたクラッシュの問題を修正
-   GC が多くのバージョンのデータに遭遇したときに GC がログを記録するようにする
