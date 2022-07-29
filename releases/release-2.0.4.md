---
title: TiDB 2.0.4 Release Notes
---

# TiDB2.0.4リリースノート {#tidb-2-0-4-release-notes}

2018年6月15日、TiDB2.0.4がリリースされました。 TiDB 2.0.3と比較して、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   `ALTER TABLE t DROP COLUMN a CASCADE`構文をサポートする
-   TSOへの`tidb_snapshot`の値の構成をサポート
-   監視項目のステートメントタイプの表示を調整する
-   クエリコスト見積もりの精度を最適化する
-   gRPCの`backoff max delay`つのパラメーターを構成します
-   構成ファイル内の単一ステートメントのメモリーしきい値の構成をサポート
-   オプティマイザーのエラーをリファクタリングする
-   `Cast Decimal`のデータの副作用を修正します
-   特定のシナリオでの`Merge Join`演算子の誤った結果の問題を修正します
-   Nullオブジェクトを文字列に変換する問題を修正します
-   JSONタイプのデータをJSONタイプにキャストする問題を修正します
-   結果の順序が`Union` + `OrderBy`の状態でMySQLと一致しない問題を修正します
-   `Union`ステートメントが`Limit/OrderBy`句をチェックするときのコンプライアンスルールの問題を修正します
-   `Union All`の結果の互換性の問題を修正します
-   述語プッシュダウンのバグを修正
-   `Union`ステートメントと`For Update`句の互換性の問題を修正します
-   `concat_ws`関数が誤って結果を切り捨てる問題を修正します

## PD {#pd}

-   最大数`PendingPeer`の制限なしに変更することにより、未設定のスケジューリング引数`max-pending-peer-count`の動作を改善します。

## TiKV {#tikv}

-   デバッグ用の`PerfContext`インターフェースを追加します
-   `import-mode`つのパラメータを削除します
-   `tikv-ctl`に`region-properties`コマンドを追加します
-   多くのRocksDBトゥームストーンが存在する場合に`reverse-seek`が遅いという問題を修正します
-   `do_sub`によって引き起こされるクラッシュの問題を修正します
-   GCが多くのバージョンのデータに遭遇したときに、GCにログを記録させる
