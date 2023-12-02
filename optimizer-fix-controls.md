---
title: Optimizer Fix Controls
summary: Learn about the Optimizer Fix Controls feature and how to use `tidb_opt_fix_control` to control the TiDB optimizer in a more fine-grained way.
---

# オプティマイザー修正コントロール {#optimizer-fix-controls}

製品が反復的に進化するにつれて、TiDB オプティマイザーの動作が変化し、より合理的な実行計画が生成されます。ただし、特定のシナリオでは、新しい動作により予期しない結果が生じる可能性があります。例えば：

-   一部の動作の影響は、特定のシナリオに依存します。ほとんどのシナリオに改善をもたらす変更は、他のシナリオに後退を引き起こす可能性があります。
-   場合によっては、動作の詳細の変化とその結果との関係が非常に複雑になることがあります。特定の動作を改善すると、全体的な退行が発生する可能性があります。

したがって、TiDB は、修正グループの値を設定することによって、TiDB オプティマイザーの動作をきめ細かく制御できるオプティマイザー修正コントロール機能を提供します。このドキュメントでは、Optimizer Fix Controls 機能とその使用方法について説明し、TiDB が現在 Optimizer Fix Controls に対してサポートしているすべての修正をリストします。

## <code>tidb_opt_fix_control</code>の概要 {#introduction-to-code-tidb-opt-fix-control-code}

v7.1.0 以降、TiDB はオプティマイザーの動作をよりきめ細かい方法で制御するための[`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v710)システム変数を提供します。

各修正は、特定の目的のために TiDB オプティマイザーの動作を調整するために使用される制御項目です。これは、動作変更の技術的な詳細を含む GitHub の問題に対応する番号で示されます。たとえば、修正`44262`の場合、修正[問題 44262](https://github.com/pingcap/tidb/issues/44262)で制御される内容を確認できます。

[`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v710)システム変数は、複数の修正をカンマ ( `,` ) で区切って 1 つの値として受け入れます。形式は`"<#issue1>:<value1>,<#issue2>:<value2>,...,<#issueN>:<valueN>"`で、 `<#issueN>`は修正番号です。例えば：

```sql
SET SESSION tidb_opt_fix_control = '44262:ON,44389:ON';
```

## オプティマイザー修正コントロールのリファレンス {#optimizer-fix-controls-reference}

### <a href="https://github.com/pingcap/tidb/issues/44262"><code>44262</code></a> <span class="version-mark">v7.2.0 の新機能</span> {#a-href-https-github-com-pingcap-tidb-issues-44262-code-44262-code-a-span-class-version-mark-new-in-v7-2-0-span}

-   デフォルト値: `OFF`
-   可能な値: `ON` 、 `OFF`
-   この変数は、 [グローバル統計](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode)が欠落している場合に、パーティションテーブルにアクセスするために[動的プルーニングモード](/partitioned-table.md#dynamic-pruning-mode)の使用を許可するかどうかを制御します。

### <a href="https://github.com/pingcap/tidb/issues/44389"><code>44389</code></a> <span class="version-mark">v7.2.0 の新機能</span> {#a-href-https-github-com-pingcap-tidb-issues-44389-code-44389-code-a-span-class-version-mark-new-in-v7-2-0-span}

-   デフォルト値: `OFF`
-   可能な値: `ON` 、 `OFF`
-   `c = 10 and (a = 'xx' or (a = 'kk' and b = 1))`などのフィルタの場合、この変数は`IndexRangeScan`に対してより包括的なスキャン範囲を構築するかどうかを制御します。

### <a href="https://github.com/pingcap/tidb/issues/44823"><code>44823</code></a> <span class="version-mark">v7.3.0 の新機能</span> {#a-href-https-github-com-pingcap-tidb-issues-44823-code-44823-code-a-span-class-version-mark-new-in-v7-3-0-span}

-   デフォルト値: `200`
-   可能な値: `[0, 2147483647]`
-   メモリを節約するために、プラン キャッシュは、この変数で指定された数を超えるパラメーターを持つクエリをキャッシュしません。 `0`制限なしを意味します。

### <a href="https://github.com/pingcap/tidb/issues/44830"><code>44830</code></a> <span class="version-mark">v7.3.0 の新機能</span> {#a-href-https-github-com-pingcap-tidb-issues-44830-code-44830-code-a-span-class-version-mark-new-in-v7-3-0-span}

-   デフォルト値: `OFF`
-   可能な値: `ON` 、 `OFF`
-   この変数は、プラン キャッシュが物理的な最適化中に生成された`PointGet`演算子を使用して実行プランをキャッシュできるかどうかを制御します。

### <a href="https://github.com/pingcap/tidb/issues/44855"><code>44855</code></a> <span class="version-mark">v7.3.0 の新機能</span> {#a-href-https-github-com-pingcap-tidb-issues-44855-code-44855-code-a-span-class-version-mark-new-in-v7-3-0-span}

-   デフォルト値: `OFF`
-   可能な値: `ON` 、 `OFF`
-   一部のシナリオでは、 `IndexJoin`演算子の`Probe`側に`Selection`演算子が含まれる場合、TiDB は行数`IndexScan`を大幅に過大評価します。これにより、 `IndexJoin`ではなく次善のクエリ プランが選択される可能性があります。
-   この問題を軽減するために、TiDB は改善を導入しました。ただし、潜在的なクエリ プランのフォールバック リスクのため、この改善はデフォルトで無効になっています。
-   この変数は、前述の改善を有効にするかどうかを制御します。

### <a href="https://github.com/pingcap/tidb/issues/45132"><code>45132</code></a> <span class="version-mark">v7.4.0 の新機能</span> {#a-href-https-github-com-pingcap-tidb-issues-45132-code-45132-code-a-span-class-version-mark-new-in-v7-4-0-span}

-   デフォルト値: `1000`
-   可能な値: `[0, 2147483647]`
-   この変数は、アクセス パスを選択するためのオプティマイザーのヒューリスティック戦略のしきい値を設定します。アクセス パスの推定行数 ( `Index_A`など) が他のアクセス パスの推定行数 (デフォルトは`1000`倍) よりもはるかに小さい場合、オプティマイザはコスト比較をスキップし、 `Index_A`を直接選択します。
-   `0`このヒューリスティック戦略を無効にすることを意味します。
