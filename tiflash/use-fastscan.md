---
title: Use FastScan
summary: Introduces a way to speed up querying in OLAP scenarios by using FastScan.
---

# FastScan を使用する {#use-fastscan}

このドキュメントでは、FastScan を使用してオンライン分析処理 (OLAP) シナリオでクエリを高速化する方法について説明します。

デフォルトでは、 TiFlash はクエリ結果の精度とデータの一貫性を保証します。 FastScan 機能を使用すると、 TiFlash はより効率的なクエリ パフォーマンスを提供しますが、クエリ結果の精度とデータの一貫性は保証されません。

一部の OLAP シナリオでは、クエリ結果の精度に対してある程度の許容範囲が許容されます。このような場合、より高いクエリ パフォーマンスが必要な場合は、セッション レベルまたはグローバル レベルで FastScan 機能を有効にすることができます。変数`tiflash_fastscan`を構成することで、FastScan 機能を有効にするかどうかを選択できます。

## FastScan を有効または無効にする {#enable-and-disable-fastscan}

デフォルトでは、変数はセッション レベルおよびグローバル レベルで`tiflash_fastscan=OFF`です。つまり、FastScan 機能は有効になっていません。次のステートメントを使用して変数情報を表示できます。

```
show variables like 'tiflash_fastscan';

+------------------+-------+
| Variable_name    | Value |
+------------------+-------+
| tiflash_fastscan | OFF   |
+------------------+-------+
```

```
show global variables like 'tiflash_fastscan';

+------------------+-------+
| Variable_name    | Value |
+------------------+-------+
| tiflash_fastscan | OFF   |
+------------------+-------+
```

変数`tiflash_fastscan`はセッション レベルおよびグローバル レベルで設定できます。現在のセッションで FastScan を有効にする必要がある場合は、次のステートメントを使用して有効にすることができます。

```
set session tiflash_fastscan=ON;
```

グローバル レベルで`tiflash_fastscan`を設定することもできます。新しい設定は新しいセッションで有効になりますが、現在および以前のセッションでは有効になりません。また、新しいセッションでは、セッション レベルとグローバル レベルの`tiflash_fastscan`が両方とも新しい値になります。

```
set global tiflash_fastscan=ON;
```

次のステートメントを使用して FastScan を無効にできます。

```
set session tiflash_fastscan=OFF;
set global tiflash_fastscan=OFF;
```

## FastScanの仕組み {#mechanism-of-fastscan}

TiFlashのstorageレイヤーのデータは、デルタレイヤーと安定レイヤーの 2 つの層に保存されます。

デフォルトでは、FastScan は有効になっておらず、TableScan オペレーターは次の手順でデータを処理します。

1.  データの読み取り: デルタレイヤーと安定レイヤーに個別のデータ ストリームを作成して、それぞれのデータを読み取ります。
2.  並べ替えマージ: 手順 1 で作成したデータ ストリームをマージします。その後、(ハンドル、バージョン) 順に並べ替えた後にデータを返します。
3.  範囲フィルター: データ範囲に従って、手順 2 で生成されたデータをフィルターし、データを返します。
4.  MVCC +カラムフィルター: 手順 3 で生成されたデータを MVCC でフィルターし、不要な列を除外して、データを返します。

FastScan は、データの一貫性をある程度犠牲にすることで、クエリ速度を向上させます。 FastScan では、通常のスキャン プロセスのステップ 2 とステップ 4 の MVCC 部分が省略されるため、クエリのパフォーマンスが向上します。
