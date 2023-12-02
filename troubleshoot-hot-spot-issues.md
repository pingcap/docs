---
title: Troubleshoot Hotspot Issues
summary: Learn how to locate and resolve read or write hotspot issues in TiDB.
---

# ホットスポットの問題のトラブルシューティング {#troubleshoot-hotspot-issues}

このドキュメントでは、読み取りおよび書き込みホットスポットを特定して問題を解決する方法について説明します。

分散データベースとして、TiDB には、アプリケーションの負荷をさまざまなコンピューティング ノードまたはstorageノードにできるだけ均等に分散して、サーバーリソースを有効に活用する負荷分散メカニズムが備わっています。ただし、特定のシナリオでは、一部のアプリケーション負荷を適切に分散できず、パフォーマンスに影響を及ぼし、ホットスポットとも呼ばれる高負荷の単一点が形成される可能性があります。

TiDB は、ホットスポットのトラブルシューティング、解決、回避のための完全なソリューションを提供します。負荷ホットスポットのバランスをとることで、QPS の向上やレイテンシーの削減など、全体的なパフォーマンスを向上させることができます。

## 一般的なホットスポット {#common-hotspots}

このセクションでは、TiDB エンコード ルール、テーブル ホットスポット、およびインデックス ホットスポットについて説明します。

### TiDB エンコード規則 {#tidb-encoding-rules}

TiDB は、TableID を各テーブルに、IndexID を各インデックスに、RowID を各行に割り当てます。デフォルトでは、テーブルで整数の主キーが使用されている場合、主キーの値は RowID として扱われます。これらの ID のうち、TableID はクラスタ全体で一意であり、IndexID と RowID はテーブル内で一意です。これらすべての ID の型は int64 です。

データの各行は、次のルールに従ってキーと値のペアとしてエンコードされます。

    Key: tablePrefix{tableID}_recordPrefixSep{rowID}
    Value: [col1, col2, col3, col4]

キーの`tablePrefix`と`recordPrefixSep`は特定の文字列定数で、KV 空間内の他のデータと区別するために使用されます。

インデックス データの場合、キーと値のペアは次のルールに従ってエンコードされます。

    Key: tablePrefix{tableID}_indexPrefixSep{indexID}_indexedColumnsValue
    Value: rowID

インデックスデータには一意インデックスと非一意インデックスの 2 種類があります。

-   一意のインデックスの場合は、上記のコーディング ルールに従うことができます。
-   一意でないインデックスの場合、同じインデックスの`tablePrefix{tableID}_indexPrefixSep{indexID}`同じであり、複数の行の`ColumnsValue`が同じである可能性があるため、このエンコーディングでは一意のキーを構築できません。一意でないインデックスのエンコード規則は次のとおりです。

        Key: tablePrefix{tableID}_indexPrefixSep{indexID}_indexedColumnsValue_rowID
        Value: null

### テーブルのホットスポット {#table-hotspots}

TiDBのコーディング規約では、同一テーブルのデータはTableIDの先頭から始まる範囲にあり、RowIDの値順にデータが配置されます。テーブルの挿入中に RowID 値が増加する場合、挿入された行は末尾にのみ追加できます。リージョンは特定のサイズに達すると分割されますが、その後も範囲の末尾にのみ追加できます。 `INSERT`操作は 1 つのリージョンでのみ実行でき、ホットスポットを形成します。

共通の自動インクリメント主キーは順次増加します。主キーが整数型の場合、デフォルトでは主キーの値が RowID として使用されます。このとき、RowID は順次増加しており、 `INSERT`オペレーションが多数存在するとテーブルの書き込みホットスポットが形成されます。

一方、TiDB の RowID もデフォルトで順次自動増分されます。主キーが整数型ではない場合、書き込みホットスポットの問題が発生する可能性もあります。

さらに、データ書き込み (新しく作成されたテーブルまたはパーティション上) またはデータ読み取り (読み取り専用シナリオでの定期読み取りホットスポット) のプロセス中にホットスポットが発生した場合、テーブル属性を使用してリージョンのマージ動作を制御できます。詳細は[テーブル属性を使用してリージョンのマージ動作を制御する](/table-attributes.md#control-the-region-merge-behavior-using-table-attributes)を参照してください。

### インデックスホットスポット {#index-hotspots}

インデックス ホットスポットはテーブル ホットスポットに似ています。一般的なインデックス ホットスポットは、時間順に単調増加するフィールド、または`INSERT`の値が繰り返されるシナリオに発生します。

## ホットスポットの問題を特定する {#identify-hotspot-issues}

パフォーマンスの問題は必ずしもホットスポットによって引き起こされるわけではなく、複数の要因によって引き起こされる可能性があります。問題のトラブルシューティングを行う前に、問題がホットスポットに関連しているかどうかを確認してください。

-   書き込みホットスポットを判断するには、 **TiKV トラブルシューティング**モニタリング パネルで**ホット ライト**を開き、いずれかの TiKV ノードのRaftstore CPU メトリック値が他のノードの値より大幅に高いかどうかを確認します。

-   読み取りホットスポットを判断するには、 **TiKV 詳細**監視パネルで**Thread_CPU**を開いて、TiKV ノードのコプロセッサ CPU メトリック値が特に高いかどうかを確認します。

### TiDB ダッシュボードを使用してホットスポット テーブルを見つける {#use-tidb-dashboard-to-locate-hotspot-tables}

[TiDB ダッシュボード](/dashboard/dashboard-intro.md)の**Key Visualizer**機能は、ユーザーがホットスポットのトラブルシューティング範囲をテーブル レベルに絞り込むのに役立ちます。以下は**Key Visualizer**で表示される熱線図の例です。グラフの横軸は時間、縦軸は各種表と指標です。色が明るいほど負荷が大きくなります。ツールバーで読み取りまたは書き込みフローを切り替えることができます。

![Dashboard Example 1](/media/troubleshoot-hot-spot-issues-1.png)

書き込みフロー グラフに、次のような明るい斜線 (斜め上または下) が表示されることがあります。 writeは最後にしか現れないため、テーブルRegionの数が多くなると梯子状に現れます。これは、書き込みホットスポットがこの表に示されていることを示します。

![Dashboard Example 2](/media/troubleshoot-hot-spot-issues-2.png)

読み取りホットスポットの場合、通常、熱ダイアグラムに明るい水平線が表示されます。通常、これらは、次に示すように、多数のアクセスがある小さなテーブルによって発生します。

![Dashboard Example 3](/media/troubleshoot-hot-spot-issues-3.png)

明るいブロックの上にマウスを置くと、どのテーブルまたはインデックスに負荷がかかっているかがわかります。例えば：

![Dashboard Example 4](/media/troubleshoot-hot-spot-issues-4.png)

## <code>SHARD_ROW_ID_BITS</code>を使用してホットスポットを処理する {#use-code-shard-row-id-bits-code-to-process-hotspots}

非クラスター化主キーまたは主キーのないテーブルの場合、TiDB は暗黙的な自動インクリメント RowID を使用します。多数の`INSERT`オペレーションが存在する場合、データは 1 つのリージョンに書き込まれ、書き込みホットスポットが発生します。

[`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)を設定すると、行 ID が分散されて複数のリージョンに書き込まれるため、書き込みホットスポットの問題が軽減されます。

    SHARD_ROW_ID_BITS = 4 # Represents 16 shards.
    SHARD_ROW_ID_BITS = 6 # Represents 64 shards.
    SHARD_ROW_ID_BITS = 0 # Represents the default 1 shard.

ステートメントの例:

```sql
CREATE TABLE: CREATE TABLE t (c int) SHARD_ROW_ID_BITS = 4;
ALTER TABLE: ALTER TABLE t SHARD_ROW_ID_BITS = 4;
```

`SHARD_ROW_ID_BITS`の値は動的に変更できます。変更された値は、新しく書き込まれたデータに対してのみ有効です。

タイプ`CLUSTERED`の主キーを持つテーブルの場合、TiDB はテーブルの主キーを RowID として使用します。現時点では、 `SHARD_ROW_ID_BITS`オプションは RowID の生成ルールが変更されるため使用できません。 `NONCLUSTERED`タイプの主キーを持つテーブルの場合、TiDB は自動的に割り当てられた 64 ビット整数を RowID として使用します。この場合、 `SHARD_ROW_ID_BITS`機能を使用できます。 `CLUSTERED`タイプの主キーの詳細については、 [クラスター化インデックス](/clustered-indexes.md)を参照してください。

次の 2 つの負荷図は、主キーのない 2 つのテーブルが`SHARD_ROW_ID_BITS`を使用してホットスポットを分散するケースを示しています。最初の図はホットスポットを分散させる前の状況を示し、2 番目の図はホットスポットを分散させた後の状況を示します。

![Dashboard Example 5](/media/troubleshoot-hot-spot-issues-5.png)

![Dashboard Example 6](/media/troubleshoot-hot-spot-issues-6.png)

上の負荷図に示されているように、 `SHARD_ROW_ID_BITS`を設定する前は、負荷ホットスポットが 1 つのリージョンに集中しています。 `SHARD_ROW_ID_BITS`を設定すると、負荷ホットスポットが分散されます。

## <code>AUTO_RANDOM</code>を使用して自動インクリメント主キー ホットスポット テーブルを処理する {#handle-auto-increment-primary-key-hotspot-tables-using-code-auto-random-code}

自動インクリメント主キーによってもたらされる書き込みホットスポットを解決するには、 `AUTO_RANDOM`を使用して自動インクリメント主キーを持つホットスポット テーブルを処理します。

この機能が有効な場合、TiDB は書き込みホットスポットを分散するという目的を達成するために、ランダムに分散された非反復の (スペースが使い果たされる前に) 主キーを生成します。

TiDB によって生成された主キーは自動インクリメント主キーではなくなり、 `LAST_INSERT_ID()`を使用して最後に割り当てられた主キー値を取得できることに注意してください。

この機能を使用するには、 `CREATE TABLE`ステートメントの`AUTO_INCREMENT`を`AUTO_RANDOM`に変更します。この機能は、主キーが一意性を保証することだけが必要な、アプリケーション以外のシナリオに適しています。

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

次の 2 つの負荷図は、ホットスポットを分散するために`AUTO_INCREMENT`から`AUTO_RANDOM`を変更する前と後の両方の状況を示しています。最初のものは`AUTO_INCREMENT`を使用し、2 つ目は`AUTO_RANDOM`を使用します。

![Dashboard Example 7](/media/troubleshoot-hot-spot-issues-7.png)

![Dashboard Example 8](/media/troubleshoot-hot-spot-issues-8.png)

上の負荷図に示されているように、 `AUTO_INCREMENT` `AUTO_RANDOM`に置き換えると、ホットスポットが分散される可能性があります。

詳細については、 [自動ランダム](/auto-random.md)を参照してください。

## 小さなテーブルのホットスポットの最適化 {#optimization-of-small-table-hotspots}

TiDB のコプロセッサーキャッシュ機能は、コンピューティング結果キャッシュのプッシュ ダウンをサポートしています。この機能を有効にすると、TiDB は TiKV にプッシュダウンされる計算結果をキャッシュします。この機能は、小さなテーブルの読み取りホットスポットに適しています。

詳細については、 [コプロセッサーキャッシュ](/coprocessor-cache.md)を参照してください。

**以下も参照してください。**

-   [高度な同時書き込みのベスト プラクティス](/best-practices/high-concurrency-best-practices.md)
-   [分割リージョン](/sql-statements/sql-statement-split-region.md)

## 分散読み取りホットスポット {#scatter-read-hotspots}

読み取りホットスポットのシナリオでは、ホットスポット TiKV ノードが読み取りリクエストを時間内に処理できず、読み取りリクエストがキューイングされます。ただし、現時点ではすべての TiKV リソースが使い果たされているわけではありません。レイテンシーを短縮するために、TiDB v7.1.0 には負荷ベースのレプリカ読み取り機能が導入されています。これにより、TiDB は、ホットスポット TiKV ノードでキューに入れることなく、他の TiKV ノードからデータを読み取ることができます。 [`tidb_load_based_replica_read_threshold`](/system-variables.md#tidb_load_based_replica_read_threshold-new-in-v700)システム変数を使用して、読み取りリクエストのキューの長さを制御できます。リーダー ノードの推定キュー時間がこのしきい値を超えると、TiDB はフォロワー ノードからのデータの読み取りを優先します。この機能により、読み取りホットスポットのシナリオでは、読み取りホットスポットを分散しない場合と比較して、読み取りスループットが 70% ～ 200% 向上します。
