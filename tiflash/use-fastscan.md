---
title: Use FastScan
summary: FastScan を使用して OLAP シナリオでのクエリを高速化する方法を紹介します。
---

# ファストスキャンを使用する {#use-fastscan}

このドキュメントでは、FastScan を使用してオンライン分析処理 (OLAP) シナリオでのクエリを高速化する方法について説明します。

TiFlash はデフォルトでクエリ結果の精度とデータの一貫性を保証します。FastScan 機能を使用すると、 TiFlash はより効率的なクエリパフォーマンスを提供しますが、クエリ結果の精度とデータの一貫性は保証されません。

一部のOLAPシナリオでは、クエリ結果の精度に多少の許容範囲が認められます。このような場合、より高いクエリパフォーマンスが必要な場合は、セッションレベルまたはグローバルレベルでFastScan機能を有効にできます。FastScan機能を有効にするかどうかは、変数[`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-new-in-v630)設定することで選択できます。

## 制限 {#restrictions}

FastScan機能を有効にすると、クエリ結果にテーブルの古いデータが含まれる場合があります。つまり、同じ主キーを持つ複数の履歴データや、削除されたデータが返される可能性があります。

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

TiFlash は古いデータの圧縮をバックグラウンドで自動的に開始できますが、古いデータは圧縮が完了し、データバージョンが GC セーフポイントより古くなるまで物理的にクリーンアップされません。物理的クリーンアップ後、クリーンアップされた古いデータは FastScan モードでは返されなくなります。データ圧縮のタイミングは、様々な要因によって自動的にトリガーされます。また、 [`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md)ステートメントを使用して手動でデータ圧縮を開始することもできます。

## FastScanを有効または無効にする {#enable-and-disable-fastscan}

デフォルトでは、セッションレベルとグローバルレベルで変数は`tiflash_fastscan=OFF`設定されており、FastScan機能は無効です。変数情報を表示するには、次のステートメントを使用します。

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

変数`tiflash_fastscan`セッションレベルとグローバルレベルで設定できます。現在のセッションでFastScanを有効にするには、次のステートメントを使用します。

    set session tiflash_fastscan=ON;

グローバルレベルで`tiflash_fastscan`設定することもできます。新しい設定は新しいセッションで有効になりますが、現在のセッションと以前のセッションには適用されません。また、新しいセッションでは、セッションレベルとグローバルレベルの両方の`tiflash_fastscan`に新しい値が設定されます。

    set global tiflash_fastscan=ON;

次のステートメントを使用して FastScan を無効にすることができます。

    set session tiflash_fastscan=OFF;
    set global tiflash_fastscan=OFF;

## FastScanの仕組み {#mechanism-of-fastscan}

TiFlashのstorageレイヤーのデータは、デルタレイヤーと安定レイヤーの 2 つの層に保存されます。

デフォルトでは、FastScan は有効になっておらず、TableScan オペレーターは次の手順でデータを処理します。

1.  データの読み取り: Deltaレイヤーと Stableレイヤーに個別のデータ ストリームを作成し、それぞれのデータを読み取ります。
2.  ソートマージ: 手順 1 で作成したデータ ストリームをマージします。次に、(主キー列、タイムスタンプ列) の順序でソートしたデータを返します。
3.  範囲フィルター: データ範囲に従って、手順 2 で生成されたデータをフィルターし、データを返します。
4.  MVCC +カラムフィルター: 手順 3 で生成されたデータを MVCC (つまり、主キー列とタイムスタンプ列に従ってデータ バージョンをフィルター処理) および列 (つまり、不要な列をフィルター処理) を通じてフィルター処理し、データを返します。

FastScanは、データの一貫性をある程度犠牲にすることで、クエリ速度を向上させます。通常のスキャンプロセスにおけるステップ2とステップ4のMVCC部分はFastScanでは省略されるため、クエリパフォーマンスが向上します。
