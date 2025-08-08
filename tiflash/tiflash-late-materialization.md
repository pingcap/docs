---
title: TiFlash Late Materialization
summary: TiFlash の遅延マテリアライゼーション機能を使用して、OLAP シナリオでクエリを高速化する方法について説明します。
---

# TiFlash遅延マテリアライゼーション {#tiflash-late-materialization}

> **注記：**
>
> TiFlash の遅延マテリアライゼーションは[高速スキャンモード](/tiflash/use-fastscan.md)では有効になりません。

TiFlash の遅延マテリアライゼーションは、OLAP シナリオにおけるクエリを高速化するための最適化手法です。システム変数[`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-new-in-v700)使用して、 TiFlash の遅延マテリアライゼーションの有効化または無効化を制御できます。

-   無効にすると、フィルタ条件（ `WHERE`句）を含む`SELECT`ステートメントを処理するために、 TiFlash はクエリに必要な列からすべてのデータを読み取り、クエリ条件に基づいてデータをフィルタリングして集計します。
-   有効にすると、 TiFlash はフィルター条件の一部を TableScan オペレーターにプッシュダウンすることをサポートします。つまり、 TiFlash はまず TableScan オペレーターにプッシュダウンされたフィルター条件に関連する列データをスキャンし、条件を満たす行をフィルタリングした後、それらの行の残りの列データをスキャンしてさらに計算を行います。これにより、データ処理における IO スキャンと計算量が削減されます。

OLAPシナリオにおける特定のクエリのパフォーマンスを向上させるため、v7.1.0以降ではTiFlashの遅延マテリアライゼーション機能がデフォルトで有効化されています。TiDBオプティマイザーは、統計情報とフィルタ条件に基づいてプッシュダウンするフィルタ条件を決定し、フィルタリング率の高いフィルタ条件を優先的にプッシュダウンします。詳細なアルゴリズムについては、 [RFC文書](https://github.com/pingcap/tidb/tree/release-8.5/docs/design/2022-12-06-support-late-materialization.md)参照してください。

例えば：

```sql
EXPLAIN SELECT a, b, c FROM t1 WHERE a < 1;
```

    +-------------------------+----------+--------------+---------------+-------------------------------------------------------+
    | id                      | estRows  | task         | access object | operator info                                         |
    +-------------------------+----------+--------------+---------------+-------------------------------------------------------+
    | TableReader_12          | 12288.00 | root         |               | MppVersion: 1, data:ExchangeSender_11                 |
    | └─ExchangeSender_11     | 12288.00 | mpp[tiflash] |               | ExchangeType: PassThrough                             |
    |   └─TableFullScan_9     | 12288.00 | mpp[tiflash] | table:t1      | pushed down filter:lt(test.t1.a, 1), keep order:false |
    +-------------------------+----------+--------------+---------------+-------------------------------------------------------+

この例では、フィルタ条件`a < 1` TableScan演算子にプッシュダウンされます。TiFlashはまず列`a`からすべてのデータを読み取り、次に条件`a < 1`を満たす行をフィルタリングします。次に、 TiFlashはフィルタリングされた行から列`b`と`c`読み取ります。

## TiFlash の遅延マテリアライゼーションを有効または無効にする {#enable-or-disable-tiflash-late-materialization}

デフォルトでは、システム変数`tidb_opt_enable_late_materialization`セッションレベルとグローバルレベルの両方で`ON`設定されており、これはTiFlash の遅延マテリアライゼーション機能が有効になっていることを意味します。対応する変数情報を表示するには、次のステートメントを使用します。

```sql
SHOW VARIABLES LIKE 'tidb_opt_enable_late_materialization';
```

    +--------------------------------------+-------+
    | Variable_name                        | Value |
    +--------------------------------------+-------+
    | tidb_opt_enable_late_materialization | ON    |
    +--------------------------------------+-------+

```sql
SHOW GLOBAL VARIABLES LIKE 'tidb_opt_enable_late_materialization';
```

    +--------------------------------------+-------+
    | Variable_name                        | Value |
    +--------------------------------------+-------+
    | tidb_opt_enable_late_materialization | ON    |
    +--------------------------------------+-------+

`tidb_opt_enable_late_materialization`変数は、セッション レベルまたはグローバル レベルで変更できます。

-   現在のセッションでTiFlash の遅延マテリアライゼーションを無効にするには、次のステートメントを使用します。

    ```sql
    SET SESSION tidb_opt_enable_late_materialization=OFF;
    ```

-   グローバル レベルでTiFlash の遅延マテリアライゼーションを無効にするには、次のステートメントを使用します。

    ```sql
    SET GLOBAL tidb_opt_enable_late_materialization=OFF;
    ```

    この設定後、新しいセッションでは、セッション レベルとグローバル レベルの両方で`tidb_opt_enable_late_materialization`変数がデフォルトで有効になります。

TiFlash の遅延マテリアライゼーションを有効にするには、次のステートメントを使用します。

```sql
SET SESSION tidb_opt_enable_late_materialization=ON;
```

```sql
SET GLOBAL tidb_opt_enable_late_materialization=ON;
```

## 実施メカニズム {#implementation-mechanism}

フィルター条件が TableScan オペレーターにプッシュダウンされると、TableScan オペレーターの実行プロセスには主に次の手順が含まれます。

1.  3 つの列`<handle, del_mark, version>`読み取り、マルチバージョン同時実行制御 (MVCC) フィルタリングを実行し、MVCC ビットマップを生成します。
2.  フィルター条件に関連する列を読み取り、条件を満たす行をフィルターして、フィルター ビットマップを生成します。
3.  MVCC ビットマップとフィルター ビットマップの間で`AND`演算を実行して、最終ビットマップを生成します。
4.  最終ビットマップに従って、残りの列の対応する行を読み取ります。
5.  手順 2 と 4 で読み取ったデータを結合し、結果を返します。
