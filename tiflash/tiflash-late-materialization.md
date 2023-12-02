---
title: TiFlash Late Materialization
summary: Describe how to use the TiFlash late materialization feature to accelerate queries in OLAP scenarios.
---

# TiFlash後期マテリアライゼーション {#tiflash-late-materialization}

> **注記：**
>
> TiFlash後期実体化は[高速スキャンモード](/tiflash/use-fastscan.md)では有効になりません。

TiFlash遅延マテリアライゼーションは、OLAP シナリオでクエリを高速化する最適化方法です。 [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-new-in-v700)システム変数を使用して、 TiFlash遅延実体化を有効にするか無効にするかを制御できます。

-   無効にすると、フィルター条件 ( `WHERE`句) を使用して`SELECT`ステートメントを処理するために、 TiFlash はクエリに必要な列からすべてのデータを読み取り、クエリ条件に基づいてデータをフィルターして集計します。
-   これを有効にすると、 TiFlash はフィルター条件の一部を TableScan オペレーターにプッシュダウンすることをサポートします。つまり、 TiFlash は、 TableScan オペレーターにプッシュダウンされたフィルター条件に関連する列データを最初にスキャンし、条件を満たす行をフィルター処理してから、これらの行の他の列データをスキャンしてさらなる計算を行うことで、IO スキャンとデータ処理の計算。

OLAP シナリオでの特定のクエリのパフォーマンスを向上させるために、v7.1.0 以降、 TiFlash遅延マテリアライゼーション機能がデフォルトで有効になっています。 TiDB オプティマイザーは、統計とフィルター条件に基づいてどのフィルター条件を下げるかを決定し、高い濾過率を持つフィルター条件を優先的に下げることができます。詳細なアルゴリズムについては、 [RFC文書](https://github.com/pingcap/tidb/tree/release-7.5/docs/design/2022-12-06-support-late-materialization.md)を参照してください。

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

この例では、フィルター条件`a < 1`が TableScan オペレーターにプッシュダウンされます。 TiFlash は、まず列`a`からすべてのデータを読み取り、次に`a < 1`条件を満たす行をフィルターします。次に、 TiFlash はこれらのフィルタリングされた行から列`b`と列`c`を読み取ります。

## TiFlash遅延マテリアライゼーションを有効または無効にする {#enable-or-disable-tiflash-late-materialization}

デフォルトでは、 `tidb_opt_enable_late_materialization`システム変数はセッション レベルとグローバル レベルの両方で`ON`です。これは、 TiFlash遅延実体化機能が有効であることを意味します。次のステートメントを使用すると、対応する変数情報を表示できます。

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

-   現在のセッションでTiFlash の遅延実体化を無効にするには、次のステートメントを使用します。

    ```sql
    SET SESSION tidb_opt_enable_late_materialization=OFF;
    ```

-   TiFlash の遅延実体化をグローバル レベルで無効にするには、次のステートメントを使用します。

    ```sql
    SET GLOBAL tidb_opt_enable_late_materialization=OFF;
    ```

    この設定後、新しいセッションのセッション レベルとグローバル レベルの両方で`tidb_opt_enable_late_materialization`変数がデフォルトで有効になります。

TiFlash の遅延実体化を有効にするには、次のステートメントを使用します。

```sql
SET SESSION tidb_opt_enable_late_materialization=ON;
```

```sql
SET GLOBAL tidb_opt_enable_late_materialization=ON;
```

## 実装メカニズム {#implementation-mechanism}

フィルター条件が TableScan オペレーターにプッシュダウンされる場合、TableScan オペレーターの実行プロセスには主に次のステップが含まれます。

1.  3 つの列を読み取り`<handle, del_mark, version>` 、マルチバージョン同時実行制御 (MVCC) フィルター処理を実行して、MVCC ビットマップを生成します。
2.  フィルタ条件に関連する列を読み込み、条件を満たす行をフィルタリングして、フィルタビットマップを生成します。
3.  MVCC ビットマップとフィルター ビットマップの間で`AND`操作を実行して、最終ビットマップを生成します。
4.  最終ビットマップに従って、残りの列の対応する行を読み取ります。
5.  手順2と手順4で読み取ったデータを結合し、結果を返します。
