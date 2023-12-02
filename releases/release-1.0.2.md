---
title: TiDB 1.0.2 Release Notes
---

# TiDB 1.0.2 リリースノート {#tidb-1-0-2-release-notes}

2017 年 11 月 13 日に、次の更新を含む TiDB 1.0.2 がリリースされました。

## TiDB {#tidb}

-   インデックスポイントクエリのコスト見積もりを最適化する
-   `Alter Table Add Column (ColumnDef ColumnPosition)`構文をサポートする
-   `where`条件が矛盾するクエリを最適化する
-   `Add Index`操作を最適化して進捗を修正し、繰り返しの操作を削減します。
-   `Index Look Join`演算子を最適化して、小さいデータ サイズのクエリ速度を高速化します。
-   プレフィックスインデックス判定の問題を修正

## 配置Driver(PD) {#placement-driver-pd}

-   例外的な状況下でのスケジュールの安定性を向上させる

## TiKV {#tikv}

-   1 つの領域に複数のテーブルのデータが含まれないようにテーブルの分割をサポートします。
-   キーの長さを 4 KB 以下に制限する
-   より正確な読み取りトラフィック統計
-   コプロセッサスタックに高度な保護を実装する
-   `LIKE`動作と`do_div_mod`バグを修正
