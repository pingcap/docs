---
title: Optimizer Fix Controls
summary: オプティマイザー修正制御機能について学習し、tidb_opt_fix_control` を使用して TiDB オプティマイザーをより細かく制御する方法について説明します。
---

# オプティマイザー修正コントロール {#optimizer-fix-controls}

製品が繰り返し進化するにつれて、TiDB オプティマイザーの動作が変化し、より合理的な実行プランが生成されます。ただし、特定のシナリオでは、新しい動作によって予期しない結果が生じる可能性があります。例:

-   一部の動作の効果は特定のシナリオに依存します。ほとんどのシナリオに改善をもたらす変更が、他のシナリオに後退を引き起こす可能性があります。
-   場合によっては、動作の詳細の変化とその結果の関係が非常に複雑になることがあります。特定の動作の改善が全体的な退行を引き起こす可能性があります。

そのため、TiDB は、一連の修正の値を設定することで TiDB オプティマイザの動作をきめ細かく制御できるオプティマイザ修正制御機能を提供します。このドキュメントでは、オプティマイザ修正制御機能とその使用方法について説明し、現在 TiDB がオプティマイザ修正制御でサポートしているすべての修正を一覧表示します。

## <code>tidb_opt_fix_control</code>の紹介 {#introduction-to-code-tidb-opt-fix-control-code}

v6.5.3 および v7.1.0 以降、TiDB は、オプティマイザーの動作をより細かく制御するための[`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v653-and-v710)システム変数を提供します。

各修正は、特定の目的のために TiDB オプティマイザーの動作を調整するために使用される制御項目です。動作変更の技術的な詳細を含む GitHub の問題に対応する番号で示されます。たとえば、修正`44262`の場合、 [問題 44262](https://github.com/pingcap/tidb/issues/44262)でそれが制御するものを確認できます。

[`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v653-and-v710)システム変数は、複数の修正をカンマで区切られた 1 つの値 ( `,` ) として受け入れます。形式は`"<#issue1>:<value1>,<#issue2>:<value2>,...,<#issueN>:<valueN>"`で、 `<#issueN>`修正番号です。例:

```sql
SET SESSION tidb_opt_fix_control = '44262:ON,44389:ON';
```

## オプティマイザー修正コントロールリファレンス {#optimizer-fix-controls-reference}

### <a href="https://github.com/pingcap/tidb/issues/33031"><code>33031</code></a> <span class="version-mark">v8.0.0 の新機能</span> {#a-href-https-github-com-pingcap-tidb-issues-33031-code-33031-code-a-span-class-version-mark-new-in-v8-0-0-span}

-   デフォルト値: `OFF`
-   可能な値: `ON` 、 `OFF`
-   この変数は、パーティション化されたテーブルに対してプラン キャッシュを許可するかどうかを制御します。 `ON`に設定されている場合、 [パーティションテーブル](/partitioned-table.md)に対して[準備されたステートメントプランキャッシュ](/sql-prepared-plan-cache.md)も[非プリペアドステートメントプランキャッシュ](/sql-non-prepared-plan-cache.md)有効になりません。

### <a href="https://github.com/pingcap/tidb/issues/44262"><code>44262</code></a> <span class="version-mark">v6.5.3 および v7.2.0 の新機能</span> {#a-href-https-github-com-pingcap-tidb-issues-44262-code-44262-code-a-span-class-version-mark-new-in-v6-5-3-and-v7-2-0-span}

-   デフォルト値: `OFF`
-   可能な値: `ON` 、 `OFF`
-   この変数は、 [グローバル統計](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode)が欠落している場合に、パーティションテーブルにアクセスするために[動的プルーニングモード](/partitioned-table.md#dynamic-pruning-mode)の使用を許可するかどうかを制御します。

### <a href="https://github.com/pingcap/tidb/issues/44389"><code>44389</code></a> <span class="version-mark">v6.5.3 および v7.2.0 の新機能</span> {#a-href-https-github-com-pingcap-tidb-issues-44389-code-44389-code-a-span-class-version-mark-new-in-v6-5-3-and-v7-2-0-span}

-   デフォルト値: `OFF`
-   可能な値: `ON` 、 `OFF`
-   `c = 10 and (a = 'xx' or (a = 'kk' and b = 1))`などのフィルターの場合、この変数は`IndexRangeScan`のより包括的なスキャン範囲を構築するかどうかを制御します。

### <a href="https://github.com/pingcap/tidb/issues/44823"><code>44823</code></a> <span class="version-mark">v7.3.0 の新機能</span> {#a-href-https-github-com-pingcap-tidb-issues-44823-code-44823-code-a-span-class-version-mark-new-in-v7-3-0-span}

-   デフォルト値: `200`
-   可能な値: `[0, 2147483647]`
-   メモリを節約するために、プラン キャッシュはこの変数で指定された数を超えるパラメータを持つクエリをキャッシュしません。1 `0`制限がないことを意味します。

### <a href="https://github.com/pingcap/tidb/issues/44830"><code>44830</code></a> <span class="version-mark">v6.5.7 および v7.3.0 の新機能</span> {#a-href-https-github-com-pingcap-tidb-issues-44830-code-44830-code-a-span-class-version-mark-new-in-v6-5-7-and-v7-3-0-span}

-   デフォルト値: `OFF`
-   可能な値: `ON` 、 `OFF`
-   この変数は、物理的な最適化中に生成された`PointGet`演算子を使用してプラン キャッシュが実行プランをキャッシュできるかどうかを制御します。

### <a href="https://github.com/pingcap/tidb/issues/44855"><code>44855</code></a> <span class="version-mark">v6.5.4 および v7.3.0 の新機能</span> {#a-href-https-github-com-pingcap-tidb-issues-44855-code-44855-code-a-span-class-version-mark-new-in-v6-5-4-and-v7-3-0-span}

-   デフォルト値: `OFF`
-   可能な値: `ON` 、 `OFF`
-   シナリオによっては、 `IndexJoin`演算子の`Probe`側に`Selection`演算子が含まれている場合、TiDB は行数`IndexScan`を大幅に過大評価します。これにより、 `IndexJoin`ではなく、最適ではないクエリ プランが選択される場合があります。
-   この問題を軽減するために、TiDB では改善が導入されました。ただし、クエリ プランのフォールバックのリスクが発生する可能性があるため、この改善はデフォルトで無効になっています。
-   この変数は、前述の改善を有効にするかどうかを制御します。

### <a href="https://github.com/pingcap/tidb/issues/45132"><code>45132</code></a> <span class="version-mark">v7.4.0 の新機能</span> {#a-href-https-github-com-pingcap-tidb-issues-45132-code-45132-code-a-span-class-version-mark-new-in-v7-4-0-span}

-   デフォルト値: `1000`
-   可能な値: `[0, 2147483647]`
-   この変数は、アクセス パスを選択するためのオプティマイザのヒューリスティック戦略のしきい値を設定します。アクセス パスの推定行数 ( `Index_A`など) が他のアクセス パスの推定行数 (デフォルトは`1000`倍) よりもはるかに小さい場合、オプティマイザはコストの比較をスキップし、直接`Index_A`選択します。
-   `0`このヒューリスティック戦略を無効にすることを意味します。

### <a href="https://github.com/pingcap/tidb/issues/45798"><code>45798</code></a> <span class="version-mark">v7.5.0 の新機能</span> {#a-href-https-github-com-pingcap-tidb-issues-45798-code-45798-code-a-span-class-version-mark-new-in-v7-5-0-span}

-   デフォルト値: `ON`
-   可能な値: `ON` 、 `OFF`
-   この変数は、 Plan Cache が[生成された列](/generated-columns.md)アクセスする実行プランをキャッシュできるかどうかを制御します。

### <a href="https://github.com/pingcap/tidb/issues/46177"><code>46177</code></a> <span class="version-mark">v6.5.6、v7.1.3、v7.5.0 の新機能</span> {#a-href-https-github-com-pingcap-tidb-issues-46177-code-46177-code-a-span-class-version-mark-new-in-v6-5-6-v7-1-3-and-v7-5-0-span}

-   デフォルト値: `OFF`
-   可能な値: `ON` 、 `OFF`
-   この変数は、強制されていないプランを見つけた後、クエリの最適化中にオプティマイザーが強制されたプランを探索するかどうかを制御します。

### <a href="https://github.com/pingcap/tidb/issues/52869"><code>52869</code></a> <span class="version-mark">v8.1.0 の新機能</span> {#a-href-https-github-com-pingcap-tidb-issues-52869-code-52869-code-a-span-class-version-mark-new-in-v8-1-0-span}

-   デフォルト値: `OFF`
-   可能な値: `ON` 、 `OFF`
-   [インデックスマージを使用したステートメントの説明](/explain-index-merge.md#examples)の**注記**に記載されているように、オプティマイザがクエリ プランに対して単一インデックス スキャン メソッド (フル テーブル スキャン以外) を選択できる場合、オプティマイザはインデックス マージを自動的に使用しません。
-   この制限は、この修正コントロールを有効にすることで解除できます。この制限を解除すると、オプティマイザーはより多くのクエリでインデックス マージを自動的に選択できるようになりますが、オプティマイザーが最適な実行プランを無視する可能性があります。したがって、この制限を解除する前に、実際の使用例で十分なテストを実施して、パフォーマンスの低下が発生しないことを確認することをお勧めします。

### <a href="https://github.com/pingcap/tidb/issues/56318"><code>56318</code></a> {#a-href-https-github-com-pingcap-tidb-issues-56318-code-56318-code-a}

> **注記：**
>
> これは[TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)のみ利用可能です。

-   デフォルト値: `ON`
-   可能な値: `ON` 、 `OFF`
-   この変数は、 `ORDER BY`のステートメントで使用される重い式を 2 回計算しないようにするかどうかを制御します。
