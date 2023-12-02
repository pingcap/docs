---
title: TiDB 2.0 RC4 Release Notes
---

# TiDB 2.0 RC4 リリースノート {#tidb-2-0-rc4-release-notes}

2018 年 3 月 30 日に、TiDB 2.0 RC4 がリリースされました。このリリースでは、MySQL の互換性、SQL の最適化、安定性が大幅に向上しています。

## TiDB {#tidb}

-   サポート`SHOW GRANTS FOR CURRENT_USER();`
-   `UnionScan`分の`Expression`が複製されない問題を修正
-   `SET TRANSACTION`構文をサポートする
-   `copIterator`の潜在的な goroutine リークの問題を修正
-   `admin check table` nullを含むユニークインデックスを誤判定する問題を修正
-   科学表記法を使用した浮動小数点数の表示をサポート
-   バイナリリテラル計算中の型推論の問題を修正
-   `CREATE VIEW`ステートメントの解析の問題を修正
-   1 つのステートメントに`ORDER BY`と`LIMIT 0`の両方が含まれる場合のpanicの問題を修正
-   `DecodeBytes`の実行パフォーマンスの向上
-   `LIMIT 0` ～ `TableDual`を最適化して、無駄な実行計画の構築を回避します

## PD {#pd}

-   単一リージョン内のホットスポットを処理するためのリージョンの手動分割をサポートします。
-   `pdctl` `config show all`を実行するとラベルのプロパティが表示されない問題を修正
-   メトリクスとコード構造を最適化する

## TiKV {#tikv}

-   極端な状況での OOM を回避するために、スナップショットの受信中のメモリ使用量を制限します。
-   警告が発生した場合のコプロセッサーの動作の構成をサポートします。
-   TiKV でのデータ パターンのインポートのサポート
-   中央のリージョン分割をサポート
-   CIテストの速度を上げる
-   `crossbeam channel`を使用します
-   TiKV分離時にリーダー欠落によりログが過剰に出力される問題を修正
