---
title: TiDB 1.0.2 Release Notes
---

# TiDB 1.0.2 リリースノート {#tidb-1-0-2-release-notes}

2017 年 11 月 13 日に、TiDB 1.0.2 がリリースされ、次の更新が行われました。

## TiDB {#tidb}

-   インデックス ポイント クエリのコスト見積もりを最適化する
-   `Alter Table Add Column (ColumnDef ColumnPosition)`構文をサポート
-   `where`の条件が矛盾するクエリを最適化する
-   `Add Index`操作を最適化して進捗を修正し、繰り返し操作を減らす
-   `Index Look Join`演算子を最適化して、小さなデータ サイズのクエリ速度を加速する
-   プレフィックスインデックス判定の問題を修正

## プレースメントDriver(PD) {#placement-driver-pd}

-   例外的な状況下でのスケジューリングの安定性を向上させる

## TiKV {#tikv}

-   分割テーブルをサポートして、1 つのリージョンに複数のテーブルのデータが含まれないようにします
-   キーの長さを 4 KB 以下に制限する
-   より正確な読み取りトラフィック統計
-   コプロセッサー・スタックに強力な保護を実装する
-   `LIKE`動作と`do_div_mod`バグを修正
