---
title: Troubleshoot Hotspot Issues
summary: TiDB の読み取りまたは書き込みホットスポットの問題を特定して解決する方法を学びます。
---

# ホットスポットの問題のトラブルシューティング {#troubleshoot-hotspot-issues}

このドキュメントでは、読み取りおよび書き込みホットスポットの問題を特定して解決する方法について説明します。

分散データベースである TiDB には、アプリケーションの負荷をさまざまなコンピューティング ノードまたはstorageノードにできるだけ均等に分散して、サーバーリソースをより有効に活用するための負荷分散メカニズムがあります。ただし、特定のシナリオでは、一部のアプリケーションの負荷が適切に分散されない場合があり、パフォーマンスに影響を及ぼし、ホットスポットとも呼ばれる単一の高負荷ポイントが形成される可能性があります。

TiDB は、ホットスポットのトラブルシューティング、解決、回避のための完全なソリューションを提供します。負荷ホットスポットを分散することで、QPS の向上やレイテンシーの削減など、全体的なパフォーマンスを向上させることができます。

## 一般的なホットスポット {#common-hotspots}

このセクションでは、TiDB エンコーディング ルール、テーブル ホットスポット、およびインデックス ホットスポットについて説明します。

### TiDB エンコーディングルール {#tidb-encoding-rules}

TiDB は各テーブルに TableID、各インデックスに IndexID、各行に RowID を割り当てます。デフォルトでは、テーブルが整数の主キーを使用する場合、主キーの値が RowID として扱われます。これらの ID のうち、TableID はクラスター全体で一意であり、IndexID と RowID はテーブル内で一意です。これらの ID の型はすべて int64 です。

各データ行は、次の規則に従ってキーと値のペアとしてエンコードされます。

    Key: tablePrefix{tableID}_recordPrefixSep{rowID}
    Value: [col1, col2, col3, col4]

キーの`tablePrefix`と`recordPrefixSep`特定の文字列定数であり、KV 空間内の他のデータと区別するために使用されます。

インデックス データの場合、キーと値のペアは次の規則に従ってエンコードされます。

    Key: tablePrefix{tableID}_indexPrefixSep{indexID}_indexedColumnsValue
    Value: rowID

インデックス データには、一意のインデックスと非一意のインデックスの 2 種類があります。

-   一意のインデックスの場合は、上記のコーディング規則に従うことができます。
-   非一意インデックスの場合、同じインデックスの`tablePrefix{tableID}_indexPrefixSep{indexID}`同じであり、複数の行の`ColumnsValue`同じである可能性があるため、このエンコーディングでは一意キーを構築できません。非一意インデックスのエンコーディング ルールは次のとおりです。

        Key: tablePrefix{tableID}_indexPrefixSep{indexID}_indexedColumnsValue_rowID
        Value: null

### テーブルホットスポット {#table-hotspots}

TiDB のコーディング規則によれば、同じテーブルのデータは TableID の先頭で始まる範囲にあり、データは RowID 値の順序で配置されます。テーブルの挿入中に RowID 値が増加すると、挿入された行は末尾にのみ追加できます。Regionは一定のサイズに`INSERT`と分割され、その後も範囲の末尾にのみ追加できます。1 操作は 1 つのリージョンでのみ実行でき、ホットスポットを形成します。

一般的な自動増分主キーは順次増加します。主キーが整数型の場合、デフォルトで主キーの値が RowID として使用されます。このとき、RowID は順次増加し、 `INSERT`操作が多数存在するとテーブルの書き込みホットスポットが形成されます。

一方、TiDB の RowID も、デフォルトで順次自動増分されます。主キーが整数型でない場合は、書き込みホットスポットの問題が発生する可能性もあります。

さらに、データ書き込み（新しく作成されたテーブルまたはパーティション上）またはデータ読み取り（読み取り専用シナリオでの定期的な読み取りホットスポット）のプロセス中にホットスポットが発生した場合は、テーブル属性を使用してリージョンのマージ動作を制御できます。詳細については、 [テーブル属性を使用してリージョンの結合動作を制御する](/table-attributes.md#control-the-region-merge-behavior-using-table-attributes)参照してください。

### インデックスホットスポット {#index-hotspots}

インデックス ホットスポットはテーブル ホットスポットに似ています。一般的なインデックス ホットスポットは、時間順に単調に増加するフィールド、または多数の繰り返し値がある`INSERT`シナリオに現れます。

## ホットスポットの問題を特定する {#identify-hotspot-issues}

パフォーマンスの問題は必ずしもホットスポットによって発生するわけではなく、複数の要因によって発生する可能性があります。問題をトラブルシューティングする前に、ホットスポットに関連しているかどうかを確認してください。

-   書き込みホットスポットを判断するには、 **TiKV トラブルシューティング**監視パネルで**Hot Write**を開き、いずれかの TiKV ノードのRaftstore CPU メトリック値が他のノードの値よりも大幅に高いかどうかを確認します。

-   読み取りホットスポットを判断するには、 **TiKV 詳細**監視パネルで**Thread_CPU**を開き、いずれかの TiKV ノードのコプロセッサ CPU メトリック値が特に高いかどうかを確認します。

### TiDBダッシュボードを使用してホットスポットテーブルを見つける {#use-tidb-dashboard-to-locate-hotspot-tables}

[TiDBダッシュボード](/dashboard/dashboard-intro.md)の**Key Visualizer**機能は、ホットスポットのトラブルシューティング範囲をテーブル レベルに絞り込むのに役立ちます。以下は、 **Key Visualizer**で表示されるサーマル ダイアグラムの例です。グラフの横軸は時間、縦軸は各種テーブルとインデックスです。色が明るいほど、負荷が大きいことを示します。ツールバーで読み取りフローと書き込みフローを切り替えることができます。

![Dashboard Example 1](/media/troubleshoot-hot-spot-issues-1.png)

書き込みフロー グラフに、次の明るい斜めの線 (斜め上または斜め下) が表示されることがあります。書き込みは最後にのみ表示されるため、テーブル領域の数が増えると、はしごのように見えます。これは、このテーブルに書き込みホットスポットが表示されていることを示しています。

![Dashboard Example 2](/media/troubleshoot-hot-spot-issues-2.png)

読み取りホットスポットの場合、通常、熱図に明るい水平線が表示されます。通常、これは、次に示すように、アクセス数が多い小さなテーブルによって発生します。

![Dashboard Example 3](/media/troubleshoot-hot-spot-issues-3.png)

明るいブロックの上にマウスを置くと、どのテーブルまたはインデックスに負荷がかかっているかがわかります。例:

![Dashboard Example 4](/media/troubleshoot-hot-spot-issues-4.png)

## <code>SHARD_ROW_ID_BITS</code>を使用してホットスポットを処理する {#use-code-shard-row-id-bits-code-to-process-hotspots}

クラスター化されていない主キーまたは主キーの`INSERT`テーブルの場合、TiDB は暗黙的な自動増分 RowID を使用します。1 操作が多数存在する場合、データは単一のリージョンに書き込まれ、書き込みホットスポットが発生します。

[`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)を設定すると、行 ID が分散されて複数のリージョンに書き込まれるため、書き込みホットスポットの問題を軽減できます。

    SHARD_ROW_ID_BITS = 4 # Represents 16 shards.
    SHARD_ROW_ID_BITS = 6 # Represents 64 shards.
    SHARD_ROW_ID_BITS = 0 # Represents the default 1 shard.

ステートメントの例:

```sql
CREATE TABLE: CREATE TABLE t (c int) SHARD_ROW_ID_BITS = 4;
ALTER TABLE: ALTER TABLE t SHARD_ROW_ID_BITS = 4;
```

値`SHARD_ROW_ID_BITS`は動的に変更できます。変更された値は、新しく書き込まれたデータに対してのみ有効になります。

`CLUSTERED`型の主キーを持つテーブルの場合、TiDB はテーブルの主キーを RowID として使用します。この時点では、 `SHARD_ROW_ID_BITS`オプションは RowID 生成ルールを変更するため使用できません。5 型`NONCLUSTERED`主キーを持つテーブルの場合、TiDB は自動的に割り当てられた 64 ビット整数を RowID として使用します。この場合、 `SHARD_ROW_ID_BITS`機能を使用することができます`CLUSTERED`型の主キーの詳細については、 [クラスター化インデックス](/clustered-indexes.md)を参照してください。

次の 2 つの負荷図は、主キーのない 2 つのテーブルが`SHARD_ROW_ID_BITS`使用してホットスポットを分散する場合を示しています。最初の図はホットスポットを分散する前の状況を示し、2 番目の図はホットスポットを分散した後の状況を示しています。

![Dashboard Example 5](/media/troubleshoot-hot-spot-issues-5.png)

![Dashboard Example 6](/media/troubleshoot-hot-spot-issues-6.png)

上記の負荷図に示すように、設定`SHARD_ROW_ID_BITS`前は、負荷ホットスポットが単一のリージョンに集中していました。設定`SHARD_ROW_ID_BITS`の後は、負荷ホットスポットが分散するようになります。

## <code>AUTO_RANDOM</code>を使用して自動増分主キー ホットスポット テーブルを処理する {#handle-auto-increment-primary-key-hotspot-tables-using-code-auto-random-code}

自動インクリメント主キーによってもたらされる書き込みホットスポットを解決するには、 `AUTO_RANDOM`使用して、自動インクリメント主キーを持つホットスポット テーブルを処理します。

この機能を有効にすると、TiDB は書き込みホットスポットを分散させる目的を達成するために、ランダムに分散され、重複のない (スペースが使い果たされる前に) 主キーを生成します。

TiDB によって生成された主キーは自動増分主キーではなくなり、 `LAST_INSERT_ID()`使用して前回割り当てられた主キー値を取得できることに注意してください。

この機能を使用するには、 `CREATE TABLE`ステートメントの`AUTO_INCREMENT`を`AUTO_RANDOM`に変更します。この機能は、主キーの一意性のみを保証する必要がある非アプリケーション シナリオに適しています。

例えば：

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

次の 2 つの負荷図は、ホットスポットを分散させるために`AUTO_INCREMENT`から`AUTO_RANDOM`を変更する前と変更した後の状況を示しています。最初の図では`AUTO_INCREMENT`が使用され、2 番目の図では`AUTO_RANDOM`が使用されます。

![Dashboard Example 7](/media/troubleshoot-hot-spot-issues-7.png)

![Dashboard Example 8](/media/troubleshoot-hot-spot-issues-8.png)

上記の負荷図に示されているように、 `AUTO_INCREMENT`代わりに`AUTO_RANDOM`使用すると、ホットスポットをうまく分散できます。

詳細については[自動ランダム](/auto-random.md)参照してください。

## 小さなテーブルホットスポットの最適化 {#optimization-of-small-table-hotspots}

TiDB のコプロセッサーキャッシュ機能は、コンピューティング結果のキャッシュのプッシュダウンをサポートします。この機能を有効にすると、TiDB は TiKV にプッシュダウンされるコンピューティング結果をキャッシュします。この機能は、小さなテーブルの読み取りホットスポットに適しています。

詳細については[コプロセッサーキャッシュ](/coprocessor-cache.md)参照してください。

**参照:**

-   [高度な同時書き込みのベストプラクティス](/best-practices/high-concurrency-best-practices.md)
-   [分割リージョン](/sql-statements/sql-statement-split-region.md)

## 読み取りホットスポットを分散 {#scatter-read-hotspots}

読み取りホットスポットのシナリオでは、ホットスポット TiKV ノードは読み取り要求を時間内に処理できず、読み取り要求がキューイングされます。ただし、この時点ですべての TiKV リソースが使い果たされるわけではありません。レイテンシーを削減するために、TiDB v7.1.0 では負荷ベースのレプリカ読み取り機能が導入され、これにより、TiDB はホットスポット TiKV ノードでキューイングすることなく、他の TiKV ノードからデータを読み取ることができます。読み取り要求のキューの長さは、 [`tidb_load_based_replica_read_threshold`](/system-variables.md#tidb_load_based_replica_read_threshold-new-in-v700)システム変数を使用して制御できます。リーダー ノードの推定キュー時間がこのしきい値を超えると、TiDB はフォロワー ノードからのデータの読み取りを優先します。この機能により、読み取りホットスポットを分散させない場合と比較して、読み取りホットスポットのシナリオで読み取りスループットが 70% ～ 200% 向上します。
