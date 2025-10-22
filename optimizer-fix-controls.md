---
title: Optimizer Fix Controls
summary: オプティマイザー修正制御機能について学習し、tidb_opt_fix_control` を使用して TiDB オプティマイザーをより細かく制御する方法について説明します。
---

# オプティマイザー修正コントロール {#optimizer-fix-controls}

製品が継続的に進化するにつれて、TiDBオプティマイザの動作が変化し、より合理的な実行プランが生成されます。しかし、特定のシナリオでは、新しい動作が予期しない結果につながる可能性があります。例えば、

-   一部の動作の効果は特定のシナリオに依存します。ほとんどのシナリオで改善をもたらす変更が、他のシナリオでは後退を引き起こす可能性があります。
-   場合によっては、行動の詳細の変化とその結果の関係が非常に複雑になることがあります。特定の行動の改善が、全体的な退行を引き起こす可能性があります。

そのため、TiDBは、複数の修正項目に値を設定することで、TiDBオプティマイザの動作をきめ細かく制御できるオプティマイザ修正制御機能を提供しています。このドキュメントでは、オプティマイザ修正制御機能とその使用方法について説明し、TiDBが現在オプティマイザ修正制御でサポートしているすべての修正項目を一覧表示します。

## <code>tidb_opt_fix_control</code>の紹介 {#introduction-to-code-tidb-opt-fix-control-code}

v6.5.3 および v7.1.0 以降、TiDB は、オプティマイザーの動作をより細かく制御するための[`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v653-and-v710)システム変数を提供します。

各修正は、特定の目的のためにTiDBオプティマイザーの動作を調整するために用いられる制御項目です。修正には、動作変更の技術的な詳細が記載されたGitHub Issueに対応する番号が付けられています。例えば、修正`44262`場合、修正[問題44262](https://github.com/pingcap/tidb/issues/44262)でその制御内容を確認できます。

システム変数[`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v653-and-v710) 、複数の修正をカンマ区切りで 1 つの値として受け入れます ( `,` )。形式は`"<#issue1>:<value1>,<#issue2>:<value2>,...,<#issueN>:<valueN>"`で、 `<#issueN>`修正番号です。例:

```sql
SET SESSION tidb_opt_fix_control = '44262:ON,44389:ON';
```

## オプティマイザー修正コントロールリファレンス {#optimizer-fix-controls-reference}

### <a href="https://github.com/pingcap/tidb/issues/33031"><code>33031</code></a><span class="version-mark">バージョン8.0.0の新機能</span> {#a-href-https-github-com-pingcap-tidb-issues-33031-code-33031-code-a-span-class-version-mark-new-in-v8-0-0-span}

-   デフォルト値: `OFF`
-   可能`OFF`値: `ON`
-   この変数は、パーティションテーブルに対してプランキャッシュを許可するかどうかを制御します。 `ON`に設定した場合、 [パーティションテーブル](/partitioned-table.md)では[準備されたステートメントプランキャッシュ](/sql-prepared-plan-cache.md)も[非プリペアドステートメントプランキャッシュ](/sql-non-prepared-plan-cache.md)有効になりません。

### <a href="https://github.com/pingcap/tidb/issues/44262"><code>44262</code></a> <span class="version-mark">v6.5.3 および v7.2.0 の新機能</span> {#a-href-https-github-com-pingcap-tidb-issues-44262-code-44262-code-a-span-class-version-mark-new-in-v6-5-3-and-v7-2-0-span}

-   デフォルト値: `OFF`
-   可能`OFF`値: `ON`
-   この変数は、パーティションテーブルの[世界統計](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode)が欠落している場合に、 [動的プルーニングモード](/partitioned-table.md#dynamic-pruning-mode)を使用してそのテーブルにアクセスできるようにするかどうかを制御します。

### <a href="https://github.com/pingcap/tidb/issues/44389"><code>44389</code></a> <span class="version-mark">v6.5.3 および v7.2.0 の新機能</span> {#a-href-https-github-com-pingcap-tidb-issues-44389-code-44389-code-a-span-class-version-mark-new-in-v6-5-3-and-v7-2-0-span}

-   デフォルト値: `OFF`
-   可能`OFF`値: `ON`
-   `c = 10 and (a = 'xx' or (a = 'kk' and b = 1))`などのフィルターの場合、この変数は`IndexRangeScan`より包括的なスキャン範囲を構築するかどうかを制御します。

### <a href="https://github.com/pingcap/tidb/issues/44823"><code>44823</code></a><span class="version-mark">バージョン7.3.0の新機能</span> {#a-href-https-github-com-pingcap-tidb-issues-44823-code-44823-code-a-span-class-version-mark-new-in-v7-3-0-span}

-   デフォルト値: `200`
-   可能な値: `[0, 2147483647]`
-   メモリを節約するために、プラン キャッシュでは、この変数で指定された数を超えるパラメータを持つクエリはキャッシュされません。 `0`制限がないことを意味します。

### <a href="https://github.com/pingcap/tidb/issues/44830"><code>44830</code></a> <span class="version-mark">v6.5.7 および v7.3.0 の新機能</span> {#a-href-https-github-com-pingcap-tidb-issues-44830-code-44830-code-a-span-class-version-mark-new-in-v6-5-7-and-v7-3-0-span}

-   デフォルト値: `OFF`
-   可能`OFF`値: `ON`
-   この変数は、物理的な最適化中に生成された`PointGet`演算子を使用して実行プランをプラン キャッシュがキャッシュできるかどうかを制御します。

### <a href="https://github.com/pingcap/tidb/issues/44855"><code>44855</code></a> <span class="version-mark">v6.5.4 および v7.3.0 の新機能</span> {#a-href-https-github-com-pingcap-tidb-issues-44855-code-44855-code-a-span-class-version-mark-new-in-v6-5-4-and-v7-3-0-span}

-   デフォルト値: `OFF`
-   可能`OFF`値: `ON`
-   一部のシナリオでは、 `IndexJoin`演算子の`Probe`側に`Selection`演算子が含まれている場合、TiDB は行数を`IndexScan`と大幅に過大評価します。その結果、 `IndexJoin`ではなく、最適ではないクエリプランが選択される場合があります。
-   この問題を軽減するために、TiDB では改善が導入されました。ただし、クエリプランのフォールバックによる潜在的なリスクがあるため、この改善はデフォルトで無効になっています。
-   この変数は、前述の改善を有効にするかどうかを制御します。

### <a href="https://github.com/pingcap/tidb/issues/45132"><code>45132</code></a><span class="version-mark">バージョン7.4.0の新機能</span> {#a-href-https-github-com-pingcap-tidb-issues-45132-code-45132-code-a-span-class-version-mark-new-in-v7-4-0-span}

-   デフォルト値: `1000`
-   可能な値: `[0, 2147483647]`
-   この変数は、オプティマイザがアクセスパスを選択する際のヒューリスティック戦略の閾値を設定します。あるアクセスパスの推定行数（例えば`Index_A` ）が他のアクセスパスの推定行数（デフォルトでは`1000`倍）よりも大幅に少ない場合、オプティマイザはコスト比較をスキップし、直接`Index_A`選択します。
-   `0` 、このヒューリスティック戦略を無効にすることを意味します。

### <a href="https://github.com/pingcap/tidb/issues/45798"><code>45798</code></a><span class="version-mark">バージョン7.5.0の新機能</span> {#a-href-https-github-com-pingcap-tidb-issues-45798-code-45798-code-a-span-class-version-mark-new-in-v7-5-0-span}

-   デフォルト値: `ON`
-   可能`OFF`値: `ON`
-   この変数は、プラン キャッシュが[生成された列](/generated-columns.md)アクセスする実行プランをキャッシュできるかどうかを制御します。

### <a href="https://github.com/pingcap/tidb/issues/46177"><code>46177</code></a> <span class="version-mark">v6.5.6、v7.1.3、v7.5.0 の新機能</span> {#a-href-https-github-com-pingcap-tidb-issues-46177-code-46177-code-a-span-class-version-mark-new-in-v6-5-6-v7-1-3-and-v7-5-0-span}

-   デフォルト値: `ON` 。v8.5.0 より前では、デフォルト値は`OFF`です。
-   可能`OFF`値: `ON`
-   この変数は、強制されていないプランを見つけた後、クエリの最適化中にオプティマイザーが強制されているプランを探索するかどうかを制御します。

### <a href="https://github.com/pingcap/tidb/issues/47400"><code>47400</code></a><span class="version-mark">バージョン8.4.0の新機能</span> {#a-href-https-github-com-pingcap-tidb-issues-47400-code-47400-code-a-span-class-version-mark-new-in-v8-4-0-span}

-   デフォルト値: `ON`
-   可能`OFF`値: `ON`
-   クエリプランの各プランステップで適切な行数を正確に推定することは困難であるため、オプティマイザは`estRows`小さく推定する場合があります。この変数は、最小値`estRows`を制限するかどうかを制御します。
-   `ON` : 最小値`estRows`を 1 に制限します。これは、v8.4.0 で導入された新しい動作であり、Oracle や Db2 などの他のデータベースと一致しています。
-   `OFF` : 最小行数推定制限を無効にします。これにより、v8.4.0 より前のバージョンとの動作の一貫性が維持されます。この場合、 `estRows` 0 になる可能性があります。

### <a href="https://github.com/pingcap/tidb/issues/52592"><code>52592</code></a><span class="version-mark">バージョン8.4.0の新機能</span> {#a-href-https-github-com-pingcap-tidb-issues-52592-code-52592-code-a-span-class-version-mark-new-in-v8-4-0-span}

-   デフォルト値: `OFF`
-   可能`OFF`値: `ON`
-   この変数は、クエリ実行時に演算子`Point Get`と`Batch Point Get`無効にするかどうかを制御します。デフォルト値`OFF` 、演算子`Point Get`と`Batch Point Get`クエリ実行に使用できることを意味します。11 `ON`設定すると、オプティマイザは演算子`Point Get`と`Batch Point Get`無効にし、クエリ実行にコプロセッサーを強制的に選択します。
-   `Point Get`と`Batch Point Get`列投影をサポートしていません（つまり、列のサブセットのみを返すことはできません）。そのため、シナリオによっては、実行効率がコプロセッサーよりも低くなる可能性があります。この変数を`ON`に設定すると、クエリのパフォーマンスが向上します。この変数を`ON`に設定する推奨シナリオは次のとおりです。

    -   多数の列を持つ幅の広いテーブルで、少数の列のみがクエリされます。
    -   大きな JSON 値を持つテーブルで、JSON 列がクエリされないか、JSON 列の小さな部分のみがクエリされます。

### <a href="https://github.com/pingcap/tidb/issues/52869"><code>52869</code></a><span class="version-mark">バージョン8.1.0の新機能</span> {#a-href-https-github-com-pingcap-tidb-issues-52869-code-52869-code-a-span-class-version-mark-new-in-v8-1-0-span}

-   デフォルト値: `OFF`
-   可能`OFF`値: `ON`
-   [インデックスマージを使用したステートメントの説明](/explain-index-merge.md#examples)の**注記**で述べたように、オプティマイザがクエリ プランに対して単一インデックス スキャン方式 (フル テーブル スキャン以外) を選択できる場合、オプティマイザはインデックス マージを自動的に使用しません。
-   この制限は、この修正制御を有効にすることで解除できます。この制限を解除すると、オプティマイザはより多くのクエリでインデックスマージを自動的に選択できるようになりますが、最適な実行プランを無視してしまう可能性があります。したがって、この制限を解除する前に、実際のユースケースで十分なテストを実施し、パフォーマンスの低下が発生しないことを確認することをお勧めします。

### <a href="https://github.com/pingcap/tidb/issues/54337"><code>54337</code></a><span class="version-mark">バージョン8.3.0の新機能</span> {#a-href-https-github-com-pingcap-tidb-issues-54337-code-54337-code-a-span-class-version-mark-new-in-v8-3-0-span}

-   デフォルト値: `OFF`
-   可能`OFF`値: `ON`
-   現在、TiDBオプティマイザは、各接続詞が範囲のリストで構成される複雑な接続詞条件のインデックス範囲の導出に制限があります。これは、一般的な範囲交差を適用することで解決できます。
-   この修正コントロールを有効にすると、この制限が解除され、オプティマイザーは複雑な範囲交差を処理できるようになります。ただし、接続詞の数が多い（10個を超える）条件の場合、最適化時間がわずかに長くなる可能性があります。

### <a href="https://github.com/pingcap/tidb/issues/56318"><code>56318</code></a> {#a-href-https-github-com-pingcap-tidb-issues-56318-code-56318-code-a}

> **注記：**
>
> これは[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)のみ利用可能です。

-   デフォルト値: `ON`
-   可能`OFF`値: `ON`
-   この変数は`ORDER BY`ステートメントで使用される重い式を 2 回計算することを回避するかどうかを制御します。
