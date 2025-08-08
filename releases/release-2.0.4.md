---
title: TiDB 2.0.4 Release Notes
summary: TiDB 2.0.4は2018年6月15日にリリースされ、システムの互換性と安定性が向上しました。TiDB、PD、TiKVのさまざまな機能強化と修正が含まれています。TiDBの主な変更点としては、ALTER TABLE t DROP COLUMN a CASCADE`構文のサポート、ステートメントタイプの表示の改善、データ変換と結果順序に関する問題の修正などが挙げられます。PDでは`max-pending-peer-count`引数の動作が改善され、TiKVではRocksDB `PerfContext`インターフェースが追加され、`reverse-seek`の遅延やクラッシュの問題が修正されました。
---

# TiDB 2.0.4 リリースノート {#tidb-2-0-4-release-notes}

2018年6月15日にTiDB 2.0.4がリリースされました。TiDB 2.0.3と比較して、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   `ALTER TABLE t DROP COLUMN a CASCADE`構文をサポートする
-   TSOに`tidb_snapshot`の値を設定することをサポート
-   監視項目のステートメントタイプの表示を改良
-   クエリコストの見積り精度を最適化する
-   gRPCの`backoff max delay`のパラメータを設定する
-   構成ファイル内の単一のステートメントのメモリしきい値の構成をサポート
-   オプティマイザーのエラーをリファクタリングする
-   `Cast Decimal`データの副作用を修正
-   特定のシナリオで`Merge Join`演算子の誤った結果の問題を修正しました
-   Nullオブジェクトを文字列に変換する問題を修正
-   JSON型のデータをJSON型にキャストする問題を修正
-   `Union` + `OrderBy`の条件で結果の順序がMySQLと一致しない問題を修正しました
-   `Union`の文が`Limit/OrderBy`句をチェックするときのコンプライアンス ルールの問題を修正します
-   `Union All`結果の互換性の問題を修正
-   述語プッシュダウンのバグを修正
-   `Union`の文と`For Update`番目の句の互換性の問題を修正
-   `concat_ws`関数が誤って結果を切り捨てる問題を修正

## PD {#pd}

-   未設定のスケジュール引数`max-pending-peer-count`の動作を、最大`PendingPeer`秒の制限なしに変更して改善しました。

## TiKV {#tikv}

-   デバッグ用のRocksDB `PerfContext`インターフェースを追加する
-   `import-mode`パラメータを削除します
-   `tikv-ctl`に`region-properties`コマンドを追加
-   RocksDBの墓石が多数存在する場合に`reverse-seek`遅くなる問題を修正
-   `do_sub`によって引き起こされたクラッシュの問題を修正
-   GC がデータの複数のバージョンに遭遇したときにログを記録するようにする
