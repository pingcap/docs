---
title: Use FastScan
summary: FastScan を使用して OLAP シナリオでのクエリを高速化する方法を紹介します。
---

# FastScanを使用する {#use-fastscan}

このドキュメントでは、FastScan を使用してオンライン分析処理 (OLAP) シナリオでクエリを高速化する方法について説明します。

デフォルトでは、 TiFlash はクエリ結果の精度とデータの一貫性を保証します。FastScan 機能を使用すると、 TiFlash はより効率的なクエリ パフォーマンスを提供しますが、クエリ結果の精度とデータの一貫性は保証されません。

一部の OLAP シナリオでは、クエリ結果の精度に多少の許容範囲が認められます。このような場合、より高いクエリ パフォーマンスが必要な場合は、セッション レベルまたはグローバル レベルで FastScan 機能を有効にできます。変数`tiflash_fastscan`構成することで、FastScan 機能を有効にするかどうかを選択できます。

## 制限 {#restrictions}

FastScan 機能を有効にすると、クエリ結果にテーブルの古いデータが含まれる場合があります。つまり、同じ主キーを持つデータの履歴バージョンが複数取得されるか、データが削除される可能性があります。

例えば：

```sql
CREATE TABLE t1 (a INT PRIMARY KEY, b INT);
ALTER TABLE t1 SET TIFLASH REPLICA 1;
INSERT INTO t1 VALUES(1,2);
INSERT INTO t1 VALUES(10,20);
UPDATE t1 SET b = 4 WHERE a = 1;
DELETE FROM t1 WHERE a = 10;
SET SESSION tidb_isolation_read_engines='tiflash';

SELECT * FROM t1;
+------+------+
| a    | b    |
+------+------+
|    1 |    4 |
+------+------+

SET SESSION tiflash_fastscan=ON;
SELECT * FROM t1;
+------+------+
| a    | b    |
+------+------+
|    1 |    2 |
|    1 |    4 |
|   10 |   20 |
+------+------+
```

TiFlash は、古いデータの圧縮をバックグラウンドで自動的に開始できますが、古いデータは、圧縮されてデータ バージョンが GC セーフ ポイントより古くなるまで物理的にクリーンアップされません。物理的にクリーンアップされた後、クリーンアップされた古いデータは FastScan モードで返さ[`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md)なくなります。データ圧縮のタイミングは、さまざまな要因によって自動的にトリガーされます。1 ステートメントを使用して、データ圧縮を手動でトリガーすることもできます。

## FastScanを有効または無効にする {#enable-and-disable-fastscan}

デフォルトでは、セッション レベルとグローバル レベルで変数は`tiflash_fastscan=OFF`です。つまり、FastScan 機能は有効になっていません。次のステートメントを使用して変数情報を表示できます。

    show variables like 'tiflash_fastscan';

    +------------------+-------+
    | Variable_name    | Value |
    +------------------+-------+
    | tiflash_fastscan | OFF   |
    +------------------+-------+

<!---->

    show global variables like 'tiflash_fastscan';

    +------------------+-------+
    | Variable_name    | Value |
    +------------------+-------+
    | tiflash_fastscan | OFF   |
    +------------------+-------+

変数`tiflash_fastscan`は、セッション レベルとグローバル レベルで設定できます。現在のセッションで FastScan を有効にする必要がある場合は、次のステートメントを使用して有効にできます。

    set session tiflash_fastscan=ON;

グローバル レベルで`tiflash_fastscan`設定することもできます。新しい設定は新しいセッションでは有効になりますが、現在のセッションと以前のセッションでは有効になりません。また、新しいセッションでは、セッション レベルとグローバル レベルの`tiflash_fastscan`両方に新しい値が設定されます。

    set global tiflash_fastscan=ON;

次のステートメントを使用して FastScan を無効にすることができます。

    set session tiflash_fastscan=OFF;
    set global tiflash_fastscan=OFF;

## FastScanの仕組み {#mechanism-of-fastscan}

TiFlashのstorageレイヤーのデータは、デルタレイヤーと安定レイヤーの2 つの層に保存されます。

デフォルトでは、FastScan は有効になっておらず、TableScan オペレーターは次の手順でデータを処理します。

1.  データの読み取り: デルタレイヤーと安定レイヤーに個別のデータ ストリームを作成し、それぞれのデータを読み取ります。
2.  ソートマージ: 手順 1 で作成したデータ ストリームをマージします。次に、(主キー列、タイムスタンプ列) の順序でソートした後、データを返します。
3.  範囲フィルター: データ範囲に従って、手順 2 で生成されたデータをフィルターし、データを返します。
4.  MVCC +カラムフィルター: 手順 3 で生成されたデータを MVCC (つまり、主キー列とタイムスタンプ列に従ってデータ バージョンをフィルター処理) および列 (つまり、不要な列をフィルター処理) でフィルター処理し、データを返します。

FastScan は、データの一貫性をある程度犠牲にすることで、クエリ速度を高速化します。通常のスキャン プロセスのステップ 2 とステップ 4 の MVCC 部分は FastScan では省略されるため、クエリ パフォーマンスが向上します。
