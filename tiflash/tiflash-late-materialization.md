---
title: TiFlash Late Materialization
summary: TiFlash の遅延マテリアライゼーション機能を使用して OLAP シナリオでクエリを高速化する方法について説明します。
---

# TiFlash後期実体化 {#tiflash-late-materialization}

> **注記：**
>
> TiFlash の遅延マテリアライゼーションは[高速スキャンモード](/tiflash/use-fastscan.md)では有効になりません。

TiFlash遅延マテリアライゼーションは、OLAP シナリオでクエリを高速化するための最適化方法です。1 システム[`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-new-in-v700)を使用して、 TiFlash遅延マテリアライゼーションを有効にするか無効にするかを制御できます。

-   無効にすると、フィルタ条件（ `WHERE`句）を含む`SELECT`ステートメントを処理するために、 TiFlash はクエリに必要な列からすべてのデータを読み取り、クエリ条件に基づいてデータをフィルタ処理して集計します。
-   有効にすると、 TiFlash はフィルター条件の一部を TableScan 演算子にプッシュダウンすることをサポートします。つまり、 TiFlash はまず、TableScan 演算子にプッシュダウンされたフィルター条件に関連する列データをスキャンし、条件を満たす行をフィルター処理してから、これらの行の他の列データをスキャンしてさらに計算することで、IO スキャンとデータ処理の計算を削減します。

OLAP シナリオにおける特定のクエリのパフォーマンスを向上させるため、v7.1.0 以降では、 TiFlash の遅延マテリアライゼーション機能がデフォルトで有効になっています。TiDB オプティマイザーは、統計とフィルター条件に基づいてプッシュダウンするフィルター条件を決定し、フィルタリング率の高いフィルター条件を優先してプッシュダウンします。詳細なアルゴリズムについては、 [RFC ドキュメント](https://github.com/pingcap/tidb/tree/release-8.5/docs/design/2022-12-06-support-late-materialization.md)を参照してください。

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

この例では、フィルター条件`a < 1`が TableScan 演算子にプッシュダウンされます。TiFlashは最初に列`a`からすべてのデータを読み取り、次に`a < 1`条件を満たす行をフィルターします。次に、 TiFlash はこれらのフィルターされた行から列`b`と`c`読み取ります。

## TiFlash の遅延マテリアライゼーションを有効または無効にする {#enable-or-disable-tiflash-late-materialization}

デフォルトでは、 `tidb_opt_enable_late_materialization`システム変数はセッション レベルとグローバル レベルの両方で`ON`です。これは、 TiFlash の遅延マテリアライゼーション機能が有効になっていることを意味します。次のステートメントを使用して、対応する変数情報を表示できます。

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

`tidb_opt_enable_late_materialization`変数はセッション レベルまたはグローバル レベルで変更できます。

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

1.  3 つの列`<handle, del_mark, version>`読み取り、マルチバージョン同時実行制御 (MVCC) フィルタリングを実行して、MVCC ビットマップを生成します。
2.  フィルター条件に関連する列を読み取り、条件を満たす行をフィルターして、フィルター ビットマップを生成します。
3.  MVCC ビットマップとフィルター ビットマップの間で`AND`操作を実行して、最終ビットマップを生成します。
4.  最終ビットマップに従って、残りの列の対応する行を読み取ります。
5.  手順 2 と 4 で読み取ったデータを結合し、結果を返します。
