---
title: Troubleshoot Hotspot Issues
summary: Learn how to locate and resolve read or write hotspot issues in TiDB.
---

# ホットスポットの問題のトラブルシューティング {#troubleshoot-hotspot-issues}

このドキュメントでは、ホットスポットの読み取りと書き込みの問題を特定して解決する方法について説明します。

分散データベースとして、TiDBには、サーバーリソースをより有効に活用するために、アプリケーションの負荷をさまざまなコンピューティングノードまたはストレージノードに可能な限り均等に分散する負荷分散メカニズムがあります。ただし、特定のシナリオでは、一部のアプリケーションの負荷を適切に分散できないため、パフォーマンスに影響を与え、ホットスポットとも呼ばれる単一の高負荷ポイントを形成する可能性があります。

TiDBは、ホットスポットのトラブルシューティング、解決、または回避に対する完全なソリューションを提供します。負荷のホットスポットのバランスをとることにより、QPSの改善や遅延の削減など、全体的なパフォーマンスを向上させることができます。

## 一般的なホットスポット {#common-hotspots}

このセクションでは、TiDBエンコーディングルール、テーブルホットスポット、およびインデックスホットスポットについて説明します。

### TiDBエンコーディングルール {#tidb-encoding-rules}

TiDBは、TableIDを各テーブルに、IndexIDを各インデックスに、RowIDを各行に割り当てます。デフォルトでは、テーブルが整数の主キーを使用している場合、主キーの値はRowIDとして扱われます。これらのIDの中で、TableIDはクラスタ全体で一意ですが、IndexIDとRowIDはテーブルで一意です。これらすべてのIDのタイプはint64です。

データの各行は、次のルールに従ってキーと値のペアとしてエンコードされます。

```
Key: tablePrefix{tableID}_recordPrefixSep{rowID}
Value: [col1, col2, col3, col4]
```

キーの`tablePrefix`と`recordPrefixSep`は特定の文字列定数であり、KV空間内の他のデータと区別するために使用されます。

インデックスデータの場合、キーと値のペアは次のルールに従ってエンコードされます。

```
Key: tablePrefix{tableID}_indexPrefixSep{indexID}_indexedColumnsValue
Value: rowID
```

インデックスデータには、一意のインデックスと非一意のインデックスの2つのタイプがあります。

-   一意のインデックスについては、上記のコーディング規則に従うことができます。
-   一意でないインデックスの場合、同じインデックスの`tablePrefix{tableID}_indexPrefixSep{indexID}`つが同じであり、複数の行の`ColumnsValue`が同じである可能性があるため、このエンコーディングを使用して一意のキーを作成することはできません。非一意インデックスのエンコード規則は次のとおりです。

    ```
    Key: tablePrefix{tableID}_indexPrefixSep{indexID}_indexedColumnsValue_rowID
    Value: null
    ```

### テーブルのホットスポット {#table-hotspots}

TiDBコーディング規則によれば、同じテーブルのデータは、TableIDの先頭が前に付いた範囲にあり、データはRowID値の順序で配置されます。テーブルの挿入中にRowID値がインクリメントされる場合、挿入された行は末尾にのみ追加できます。リージョンは特定のサイズに達した後に分割されますが、それでも範囲の最後にのみ追加できます。 `INSERT`の操作は、1つのリージョンでのみ実行でき、ホットスポットを形成します。

一般的な自動インクリメントの主キーは順次増加しています。主キーが整数型の場合、デフォルトでは主キーの値がRowIDとして使用されます。このとき、RowIDは順次増加しており、 `INSERT`操作が多数存在するとテーブルの書き込みホットスポットが形成されます。

一方、TiDBのRowIDも、デフォルトで順次自動インクリメントされます。主キーが整数型でない場合は、書き込みホットスポットの問題も発生する可能性があります。

### ホットスポットのインデックス {#index-hotspots}

インデックスのホットスポットは、テーブルのホットスポットに似ています。一般的なインデックスのホットスポットは、時間順に単調に増加するフィールド、または繰り返し値が多数ある`INSERT`のシナリオに表示されます。

## ホットスポットの問題を特定する {#identify-hotspot-issues}

パフォーマンスの問題は必ずしもホットスポットが原因であるとは限らず、複数の要因が原因である可能性があります。問題のトラブルシューティングを行う前に、それがホットスポットに関連しているかどうかを確認してください。

-   書き込みホットスポットを判断するには、 **TiKV-Trouble-Shooting**監視パネルで<strong>Hot Write</strong>を開き、TiKVノードのRaftstoreCPUメトリック値が他のノードのメトリック値よりも大幅に高いかどうかを確認します。

-   読み取りホットスポットを判断するには、 **TiKV-Details**監視パネルで<strong>Thread_CPU</strong>を開いて、任意のTiKVノードのコプロセッサーCPUメトリック値が特に高いかどうかを確認します。

### TiDBダッシュボードを使用してホットスポットテーブルを見つける {#use-tidb-dashboard-to-locate-hotspot-tables}

[TiDBダッシュボード](/dashboard/dashboard-intro.md)の**キービジュアライザー**機能は、ユーザーがホットスポットのトラブルシューティングの範囲をテーブルレベルに絞り込むのに役立ちます。以下は、 <strong>KeyVisualizer</strong>によって示される熱図の例です。グラフの横軸は時間、縦軸はさまざまな表や索引です。色が明るいほど、負荷が大きくなります。ツールバーで読み取りまたは書き込みフローを切り替えることができます。

![Dashboard Example 1](/media/troubleshoot-hot-spot-issues-1.png)

次の明るい対角線（上向きまたは下向きに斜め）が書き込みフローグラフに表示されます。書き込みは最後にしか表示されないため、テーブルリージョンの数が増えると、ラダーとして表示されます。これは、書き込みホットスポットが次の表に表示されていることを示しています。

![Dashboard Example 2](/media/troubleshoot-hot-spot-issues-2.png)

読み取りホットスポットの場合、通常、熱図に明るい水平線が表示されます。通常、これらは、次のように、アクセス数が多い小さなテーブルが原因で発生します。

![Dashboard Example 3](/media/troubleshoot-hot-spot-issues-3.png)

明るいブロックにカーソルを合わせると、どのテーブルまたはインデックスに大きな負荷がかかっているかがわかります。例えば：

![Dashboard Example 4](/media/troubleshoot-hot-spot-issues-4.png)

## <code>SHARD_ROW_ID_BITS</code>を使用してホットスポットを処理します {#use-code-shard-row-id-bits-code-to-process-hotspots}

非整数の主キー、または主キーまたは共同主キーのないテーブルの場合、TiDBは暗黙の自動インクリメントRowIDを使用します。 `INSERT`の操作が多数存在する場合、データは単一のリージョンに書き込まれ、書き込みホットスポットになります。

`SHARD_ROW_ID_BITS`を設定すると、RowIDが分散して複数のリージョンに書き込まれ、書き込みホットスポットの問題を軽減できます。ただし、 `SHARD_ROW_ID_BITS`を大きすぎる値に設定すると、RPC要求の数が増え、CPUとネットワークのオーバーヘッドが増加します。

```
SHARD_ROW_ID_BITS = 4 # Represents 16 shards.
SHARD_ROW_ID_BITS = 6 # Represents 64 shards.
SHARD_ROW_ID_BITS = 0 # Represents the default 1 shard.
```

ステートメントの例：

{{< copyable "" >}}

```sql
CREATE TABLE：CREATE TABLE t (c int) SHARD_ROW_ID_BITS = 4;
ALTER TABLE：ALTER TABLE t SHARD_ROW_ID_BITS = 4;
```

`SHARD_ROW_ID_BITS`の値は動的に変更できます。変更された値は、新しく書き込まれたデータに対してのみ有効になります。

`CLUSTERED`タイプの主キーを持つテーブルの場合、TiDBはテーブルの主キーをRowIDとして使用します。現時点では、RowID生成ルールが変更されるため、 `SHARD_ROW_ID_BITS`オプションは使用できません。 `NONCLUSTERED`タイプの主キーを持つテーブルの場合、TiDBは自動的に割り当てられた64ビット整数をRowIDとして使用します。この場合、 `SHARD_ROW_ID_BITS`機能を使用できます。 `CLUSTERED`タイプの主キーの詳細については、 [クラスター化されたインデックス](/clustered-indexes.md)を参照してください。

次の2つの負荷図は、主キーのない2つのテーブルが`SHARD_ROW_ID_BITS`を使用してホットスポットを分散させる場合を示しています。最初の図はホットスポットを散乱させる前の状況を示し、2番目の図はホットスポットを散乱させた後の状況を示しています。

![Dashboard Example 5](/media/troubleshoot-hot-spot-issues-5.png)

![Dashboard Example 6](/media/troubleshoot-hot-spot-issues-6.png)

上記の負荷図に示されているように、 `SHARD_ROW_ID_BITS`を設定する前は、負荷のホットスポットは単一の領域に集中しています。 `SHARD_ROW_ID_BITS`を設定すると、ロードホットスポットが分散します。

## <code>AUTO_RANDOM</code>を使用して自動インクリメントの主キーホットスポットテーブルを処理する {#handle-auto-increment-primary-key-hotspot-tables-using-code-auto-random-code}

自動インクリメントの主キーによってもたらされる書き込みホットスポットを解決するには、 `AUTO_RANDOM`を使用して、自動インクリメントの主キーを持つホットスポットテーブルを処理します。

この機能が有効になっている場合、TiDBは、書き込みホットスポットを分散させる目的を達成するために、ランダムに分散され、繰り返されない（スペースが使い果たされる前に）主キーを生成します。

TiDBによって生成された主キーは、主キーの自動インクリメントではなくなり、 `LAST_INSERT_ID()`を使用して、前回割り当てられた主キーの値を取得できることに注意してください。

この機能を使用するには、 `CREATE TABLE`ステートメントの`AUTO_INCREMENT`から`AUTO_RANDOM`を変更します。この機能は、主キーが一意性を保証するだけでよい非アプリケーションシナリオに適しています。

例えば：

{{< copyable "" >}}

```sql
CREATE TABLE t (a BIGINT PRIMARY KEY AUTO_RANDOM, b varchar(255));
INSERT INTO t (b) VALUES ("foo");
SELECT * FROM t;
```

```sql
+------------+---+
| a          | b |
+------------+---+
| 1073741825 | b |
+------------+---+
```

{{< copyable "" >}}

```sql
SELECT LAST_INSERT_ID();
```

```sql
+------------------+
| LAST_INSERT_ID() |
+------------------+
| 1073741825       |
+------------------+
```

次の2つの負荷図は、ホットスポットを分散させるために`AUTO_INCREMENT`から`AUTO_RANDOM`を変更する前と後の両方の状況を示しています。最初のものは`AUTO_INCREMENT`を使用し、2番目のものは`AUTO_RANDOM`を使用します。

![Dashboard Example 7](/media/troubleshoot-hot-spot-issues-7.png)

![Dashboard Example 8](/media/troubleshoot-hot-spot-issues-8.png)

上記の負荷図に示されているように、 `AUTO_RANDOM`を使用して`AUTO_INCREMENT`を置き換えると、ホットスポットが分散する可能性があります。

詳細については、 [AUTO_RANDOM](/auto-random.md)を参照してください。

## 小さなテーブルのホットスポットの最適化 {#optimization-of-small-table-hotspots}

TiDBのコプロセッサーキャッシュ機能は、計算結果キャッシュのプッシュダウンをサポートします。この機能を有効にすると、TiDBはTiKVにプッシュダウンされる計算結果をキャッシュします。この機能は、小さなテーブルの読み取りホットスポットに適しています。

詳細については、 [コプロセッサーキャッシュ](/coprocessor-cache.md)を参照してください。

**参照：**

-   [非常に同時の書き込みのベストプラクティス](/best-practices/high-concurrency-best-practices.md)
-   [スプリットリージョン](/sql-statements/sql-statement-split-region.md)
