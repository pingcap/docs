---
title: FastScan
summary: Introduces a way to speed up querying in OLAP scenarios by using FastScan.
---

# ファストスキャン {#fastscan}

> **警告：**
>
> この機能は実験的であり、その形式と使用法は後続のバージョンで変更される可能性があります。

このドキュメントでは、オンライン分析処理 (OLAP) シナリオで FastScan を使用してクエリを高速化する方法について説明します。

デフォルトでは、TiFlash はクエリ結果の精度とデータの一貫性を保証します。 FastScan 機能を使用すると、TiFlash はより効率的なクエリ パフォーマンスを提供しますが、クエリ結果の精度とデータの一貫性を保証するものではありません。

一部の OLAP シナリオでは、クエリ結果の精度に対してある程度の許容範囲が許容されます。このような場合、より高いクエリ パフォーマンスが必要な場合は、対応するテーブルの FastScan を有効にしてクエリを実行できます。

FastScan は、 [ALTER TABLE SET TIFLASH モード](/sql-statements/sql-statement-set-tiflash-mode.md)を実行して FastScan を有効にしたテーブルでグローバルに有効になります。 TiFlash 関連の操作は、一時テーブル、メモリ内テーブル、システム テーブル、および列名に UTF-8 以外の文字を含むテーブルではサポートされていません。

詳細については、 [ALTER TABLE SET TIFLASH モード](/sql-statements/sql-statement-set-tiflash-mode.md)を参照してください。

## FastScan を有効にする {#enable-fastscan}

デフォルトでは、FastScan はすべてのテーブルで無効になっています。次のステートメントを使用して、FastScan のステータスを表示できます。

```sql
SELECT table_mode FROM information_schema.tiflash_replica WHERE table_name = 'table_name' AND table_schema = 'database_name'
```

次のステートメントを使用して、対応するテーブルの FastScan を有効にします。

```sql
ALTER TABLE table_name SET TIFLASH MODE FAST
```

有効にすると、TiFlash のこのテーブルの後続のクエリで FastScan の機能が使用されます。

次のステートメントを使用して、FastScan を無効にすることができます。

```sql
ALTER TABLE table_name SET TIFLASH MODE NORMAL
```

## FastScanの仕組み {#mechanism-of-fastscan}

TiFlash のストレージレイヤーのデータは、Deltaレイヤーと Stableレイヤーの 2 つの層に格納されます。

通常モードでは、TableScan オペレーターは次の手順でデータを処理します。

1.  データの読み取り: Deltaレイヤーと Stableレイヤーに個別のデータ ストリームを作成して、それぞれのデータを読み取ります。
2.  Sort Merge: 手順 1 で作成したデータ ストリームをマージします。次に、(ハンドル、バージョン) 順に並べ替えた後にデータを返します。
3.  範囲フィルター: データ範囲に従って、手順 2 で生成されたデータをフィルター処理し、データを返します。
4.  MVCC +カラムフィルター: 手順 3 で生成されたデータを MVCC でフィルター処理し、不要な列をフィルターで除外してから、データを返します。

FastScan は、データの一貫性をいくらか犠牲にすることで、クエリ速度を向上させます。 FastScan では、通常のスキャン プロセスのステップ 2 とステップ 4 の MVCC 部分が省略されるため、クエリのパフォーマンスが向上します。
