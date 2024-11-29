---
title: TiDB 2.0.4 Release Notes
summary: TiDB 2.0.4 は、システムの互換性と安定性の向上を伴い、2018 年 6 月 15 日にリリースされました。これには、TiDB、PD、および TiKV のさまざまな機能強化と修正が含まれています。TiDB のハイライトとしては、ALTER TABLE t DROP COLUMN a CASCADE` 構文のサポート、ステートメント タイプ表示の改善、およびデータ変換と結果の順序に関連する問題の修正があります。PD では、`max-pending-peer-count` 引数の動作が改善され、TiKV では、RocksDB `PerfContext` インターフェイスが追加され、`reverse-seek` の速度低下とクラッシュの問題が修正されています。
---

# TiDB 2.0.4 リリースノート {#tidb-2-0-4-release-notes}

2018 年 6 月 15 日に、TiDB 2.0.4 がリリースされました。TiDB 2.0.3 と比較して、このリリースではシステムの互換性と安定性が大幅に向上しています。

## ティビ {#tidb}

-   `ALTER TABLE t DROP COLUMN a CASCADE`構文をサポートする
-   TSOに`tidb_snapshot`の値を設定することをサポート
-   監視項目のステートメントタイプの表示を改良
-   クエリコストの見積り精度を最適化する
-   gRPCの`backoff max delay`のパラメータを設定する
-   設定ファイル内の単一ステートメントのメモリしきい値の設定をサポート
-   オプティマイザのエラーをリファクタリングする
-   `Cast Decimal`データの副作用を修正
-   特定のシナリオで`Merge Join`演算子の結果が間違っている問題を修正
-   NullオブジェクトをStringに変換する問題を修正
-   JSON型のデータをJSON型にキャストする問題を修正
-   `Union` + `OrderBy`の条件で結果の順序がMySQLと一致しない問題を修正
-   `Union`番目のステートメントが`Limit/OrderBy`の句をチェックするときのコンプライアンス ルールの問題を修正します。
-   `Union All`の結果の互換性の問題を修正
-   述語プッシュダウンのバグを修正
-   `Union`番目のステートメントと`For Update`番目の句の互換性の問題を修正します
-   `concat_ws`関数が誤って結果を切り捨てる問題を修正

## PD {#pd}

-   未設定のスケジュール引数`max-pending-peer-count`の動作を、最大`PendingPeer`秒の制限なしに変更して改善しました。

## ティクヴ {#tikv}

-   デバッグ用のRocksDB `PerfContext`インターフェースを追加する
-   `import-mode`パラメータを削除します
-   `tikv-ctl`に`region-properties`コマンドを追加
-   RocksDB の墓石が多数存在する場合に`reverse-seek`が遅くなる問題を修正
-   `do_sub`によって引き起こされたクラッシュの問題を修正
-   GC がデータの複数のバージョンに遭遇したときにログを記録するようにする
