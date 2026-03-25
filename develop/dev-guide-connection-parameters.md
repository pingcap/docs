---
title: Configure Connection Pools and Connection Parameters
summary: このドキュメントでは、TiDB の接続プールとパラメータの設定方法について説明します。接続プールのサイズ、プローブの設定、最適なスループットを実現するための計算式について解説します。また、パフォーマンス最適化のための JDBC API の使用方法と MySQL Connector/J パラメータの設定についても説明します。
aliases: ['/ja/tidb/stable/dev-guide-connection-parameters/','/ja/tidb/dev/dev-guide-connection-parameters/','/ja/tidbcloud/dev-guide-connection-parameters/']
---

# 接続プールと接続パラメータの設定 {#configure-connection-pools-and-connection-parameters}

このドキュメントでは、ドライバまたはORMフレームワークを使用してTiDBに接続する場合に、接続プールと接続パラメータを設定する方法について説明します。

> **ヒント：**
>
> この文書では、以下のセクションは[TiDBを使用したJavaアプリケーション開発のベストプラクティス](/develop/java-app-best-practices.md)から抜粋したものです。
>
> -   [接続数を設定する](#configure-the-number-of-connections)
> -   [プローブ構成](#probe-configuration)
> -   [接続パラメータ](#connection-parameters)

## 接続プール {#connection-pool}

TiDB（MySQL）接続の構築は、（少なくともOLTPシナリオにおいては）比較的コストがかかります。これは、TCP接続の確立に加えて、接続認証も必要となるためです。そのため、クライアントは通常、TiDB（MySQL）接続を接続プールに保存して再利用します。

Javaには[Tomcat JDBC](https://tomcat.apache.org/tomcat-10.1-doc/jdbc-pool.html) [HikariCP](https://github.com/brettwooldridge/HikariCP) [dbcp](https://commons.apache.org/proper/commons-dbcp/)多くの接続プール実装があります。TiDBは使用できる接続プール[druid](https://github.com/alibaba/druid)制限しないため、アプリケーションに合わせて好きなもの[c3p0](https://www.mchange.com/projects/c3p0/)選択できます。

### 接続数を設定する {#configure-the-number-of-connections}

接続プールのサイズは、アプリケーションのニーズに合わせて適切に調整するのが一般的です。HikariCPを例にとってみましょう。

-   **maximumPoolSize** : コネクションプール内の最大接続数。この値が大きすぎると、TiDB は不要な接続を維持するためにリソースを消費します。この値が小さすぎると、アプリケーションの接続が遅くなります。したがって、アプリケーションの特性に応じてこの値を構成する必要があります。詳細については、 [プールのサイズについて](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing)参照してください。
-   **minimumIdle** ：接続プール内のアイドル接続の最小数。主に、アプリケーションがアイドル状態のときに突発的なリクエストに対応するために、一部の接続を確保するために使用されます。アプリケーションの特性に合わせて設定する必要があります。

アプリケーションは、接続の使用が終了したら、その接続を返却する必要があります。接続プールの問題を早期に発見するために、アプリケーションは適切な接続プール監視ツール（ **metricRegistry**など）を使用することをお勧めします。

### 接続の有効期間を設定する {#configure-the-lifetime-of-connections}

TiDBサーバーがシャットダウン、メンテナンスのために再起動、またはハードウェア障害やネットワーク障害などの予期せぬ問題が発生した場合、既存のクライアント接続がリセットされ、アプリケーションの動作が中断される可能性があります。このような問題を回避するため、長時間稼働しているデータベース接続は少なくとも1日に1回は切断して再作成することをお勧めします。

ほとんどの接続プールライブラリには、接続の最大有効期間を制御するためのパラメータが用意されています。

<SimpleTab>
<div label="HikariCP">

-   **`maxLifetime`** ：プール内の接続の最大有効期間。

</div>

<div label="tomcat-jdbc">

-   **`maxAge`** ：プール内の接続の最大有効期間。

</div>

<div label="c3p0">

-   **`maxConnectionAge`** ：接続プールにおける接続の最大有効期間。

</div>

<div label="dbcp">

-   **`maxConnLifetimeMillis`** ：接続プールにおける接続の最大有効期間。

</div>
</SimpleTab>

### プローブ構成 {#probe-configuration}

接続プールは、以下のようにクライアントからTiDBへの永続的な接続を維持します。

-   バージョン5.4より前のTiDBでは、デフォルトでは（エラーが報告されない限り）クライアント接続を積極的に閉じることはありません。
-   バージョン5.4以降、TiDBはデフォルトで`28800`秒間（つまり`8`時間）の非アクティブ状態が続くとクライアント接続を自動的に閉じます。このタイムアウト設定は、TiDBとMySQL互換の`wait_timeout`変数を使用して制御できます。詳細については、 [JDBCクエリタイムアウト](/develop/dev-guide-timeouts-in-tidb.md#jdbc-query-timeout)参照してください。

さらに、クライアントとTiDBの間には、 [LVS](https://en.wikipedia.org/wiki/Linux_Virtual_Server)や[HAProxy](https://en.wikipedia.org/wiki/HAProxy)ようなネットワークプロキシが存在する場合があります。これらのプロキシは通常、特定のアイドル期間（プロキシのアイドル設定によって決定されます）が経過すると、接続を自動的にクリーンアップします。接続プールは、プロキシのアイドル設定を監視するだけでなく、キープアライブのために接続を維持またはプローブする必要もあります。

Javaアプリケーションで以下のエラーが頻繁に発生する場合：

    The last packet sent successfully to the server was 3600000 milliseconds ago. The driver has not received any packets from the server. com.mysql.jdbc.exceptions.jdbc4.CommunicationsException: Communications link failure

`n`が`n milliseconds ago`または非常に`0`値の場合、通常は実行されたSQL操作によってTiDBが異常終了したことが原因です。原因を特定するには、TiDBの標準エラーログを確認することをお勧めします。

`n`が非常に大きな値 (上記の例の`3600000`など) の場合、この接続は長時間アイドル状態になり、その後プロキシによって閉じられた可能性が高いです。通常の解決策は、プロキシのアイドル設定の値を増やし、接続プールが次のことを実行できるようにすることです。

-   接続を使用する前に、毎回接続が利用可能かどうかを確認してください。
-   別のスレッドを使用して、接続が利用可能かどうかを定期的に確認してください。
-   接続を維持するために、定期的にテストクエリを送信してください。

接続プールの実装によっては、上記の方法のうち1つ以上がサポートされている場合があります。対応する設定については、接続プールのドキュメントを参照してください。

### 経験に基づいた公式 {#formulas-based-on-experience}

HikariCPの[プールのサイズについて](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing)記事によると、データベース接続プールの適切なサイズを設定する方法がわからない場合は、 [経験に基づいた公式](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing#connections--core_count--2--effective_spindle_count)から始めることができます。次に、式から計算されたプールサイズのパフォーマンス結果に基づいて、最適なパフォーマンスを実現するためにサイズをさらに調整できます。

経験に基づいた公式は以下のとおりです。

    connections = ((core_count * 2) + effective_spindle_count)

式中の各パラメータの説明は以下のとおりです。

-   **接続数**：取得された接続のサイズ。
-   **core_count** ：CPUコアの数。
-   **effective_spindle_count** ：ハードドライブの数（ [SSD](https://en.wikipedia.org/wiki/Solid-state_drive)ではありません）。回転するハードディスクはそれぞれスピンドルと呼ばれるためです。たとえば、16台のディスクで構成されたRAIDサーバーを使用している場合、 **effective_spindle_count**は16になります。HDD**は**通常、一度に1つのリクエストしか処理できないため、この式は実際にはサーバーが同時に処理できるI/Oリクエストの数を測定しています。

特に、 [式](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing#the-formula)下の次の注記に注意してください。

>     A formula which has held up pretty well across a lot of benchmarks for years is
>     that for optimal throughput the number of active connections should be somewhere
>     near ((core_count * 2) + effective_spindle_count). Core count should not include
>     HT threads, even if hyperthreading is enabled. Effective spindle count is zero if
>     the active data set is fully cached, and approaches the actual number of spindles
>     as the cache hit rate falls. ... There hasn't been any analysis so far regarding
>     how well the formula works with SSDs.

このメモは以下を示しています。

-   **core_countは**、 [ハイパースレッディング](https://en.wikipedia.org/wiki/Hyper-threading)有効にするかどうかに関わらず、物理コアの数です。
-   データが完全にキャッシュされると、 **effective_spindle_count を**`0`に設定する必要があります。キャッシュのヒット率が低下すると、カウントは実際の数値である`HDD`に近づきます。
-   **この計算式が*SSD*にも有効かどうかは検証されておらず、不明である。**

SSDを使用する場合は、経験に基づき、以下の式を使用することをお勧めします。

    connections = (number of cores * 4)

したがって、SSDの場合は初期接続プールの最大接続サイズを`cores * 4`に設定し、さらにサイズを調整してパフォーマンスを最適化できます。

### チューニング方向 {#tuning-direction}

ご覧のとおり、 [経験に基づいた公式](#formulas-based-on-experience)から計算されたサイズはあくまで推奨される基本値です。特定のマシンで最適なサイズを見つけるには、基本値周辺のさまざまな値を試してパフォーマンスをテストする必要があります。

最適なサイズを選ぶための基本的なルールをいくつかご紹介します。

-   ネットワークまたはstorageのレイテンシーが高い場合は、最大接続数を増やしてレイテンシーによる待ち時間を短縮してください。スレッドがレイテンシーによってブロックされた場合でも、他のスレッドが処理を引き継いで処理を続行できます。
-   サーバー上に複数のサービスがデプロイされており、各サービスがそれぞれ独立した接続プールを持っている場合は、すべての接続プールへの最大接続数の合計を考慮してください。

## 接続パラメータ {#connection-parameters}

Javaアプリケーションは、さまざまなフレームワークでカプセル化されたできます。ほとんどのフレームワークでは、データベースサーバーとのやり取りを行うために、最下層でJDBC APIが呼び出されます。JDBCに関しては、以下の点に重点を置くことをお勧めします。

-   JDBC APIの使用方法の選択
-   API実装者のパラメータ設定

### JDBC API {#jdbc-api}

JDBC API の使用方法については、 [JDBC公式チュートリアル](https://docs.oracle.com/javase/tutorial/jdbc/)参照してください。このセクションでは、いくつかの重要な API の使用方法について説明します。

#### Prepare APIを使用する {#use-prepare-api}

OLTP（オンライン・トランザクション処理）シナリオでは、プログラムからデータベースに送信されるSQL文は、パラメータ変更を除けば、複数のタイプが存在します。そのため、通常の[テキストファイルからの実行](https://docs.oracle.com/javase/tutorial/jdbc/basics/processingsqlstatements.html#executing_queries)ではなく[準備された声明](https://docs.oracle.com/javase/tutorial/jdbc/basics/prepared.html)使用し、プリペアドステートメントを再利用して直接実行することをお勧めします。これにより、TiDBでSQL実行プランを繰り返し解析および生成するオーバーヘッドを回避できます。

現在、ほとんどの上位フレームワークはSQL実行のためにPrepare APIを呼び出しています。開発でJDBC APIを直接使用する場合は、Prepare APIを選択するように注意してください。

さらに、MySQL Connector/J のデフォルト実装では、クライアント側のステートメントのみが前処理され、クライアント側で`?`が置換された後、ステートメントはテキスト ファイルとしてサーバーに送信されます。したがって、Prepare API を使用するだけでなく、TiDBサーバーでステートメントの前処理を実行する前に、JDBC 接続パラメータで`useServerPrepStmts = true`設定する必要があります。パラメータ設定の詳細については、 [MySQL JDBC パラメータ](#mysql-jdbc-parameters)参照してください。

#### バッチAPIを使用する {#use-batch-api}

バッチ挿入の場合は、 [`addBatch` / `executeBatch` API](https://docs.oracle.com/en/java/javase/25/docs/api/java.sql/java/sql/Statement.html#executeBatch())を使用できます。3 `addBatch()`は、複数の SQL ステートメントを最初にクライアントにキャッシュし、 `executeBatch`メソッドを呼び出すときにそれらをまとめてデータベースサーバーに送信するために使用されます。

> **注記：**
>
> デフォルトのMySQL Connector/Jの実装では、 `addBatch()`でバッチに追加されたSQL文の送信時間は`executeBatch()`呼び出されるまで遅延されますが、実際のネットワーク転送中は文は1つずつ送信されます。そのため、この方法は通常、通信オーバーヘッドを削減しません。
>
> バッチネットワーク転送を行う場合は、JDBC接続パラメータで`rewriteBatchedStatements = true`設定する必要があります。詳細なパラメータ設定については、 [バッチ関連パラメータ](#batch-related-parameters)参照してください。

#### <code>StreamingResult</code>を使用して実行結果を取得します。 {#use-code-streamingresult-code-to-get-the-execution-result}

ほとんどのシナリオでは、実行効率を向上させるために、JDBCはデフォルトでクエリ結果を事前に取得し、クライアントのメモリに保存します。しかし、クエリが非常に大きな結果セットを返す場合、クライアントはデータベースサーバーに一度に返されるレコード数を減らし、クライアントのメモリが準備できるまで待機し、次のバッチを要求することがよくあります。

JDBCでは通常、以下の2つの処理方法が使用されます。

-   最初の方法: [**FetchSizeを**`Integer.MIN_VALUE`に設定します。](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-implementation-notes.html#ResultSet)クライアントがキャッシュしないようにします。クライアントは`StreamingResult`を介してネットワーク接続から実行結果を読み取ります。

    クライアントがストリーミング読み取り方式を使用する場合、クエリを実行するためにステートメントを引き続き使用する前に、読み取りを完了するか、 `resultset`閉じる必要があります。そうしないと、エラー`No statements may be issued when any streaming result sets are open and in use on a given connection. Ensure that you have called .close() on any active streaming result sets before attempting more queries.`が返されます。

    クライアントが読み取りを完了するか、 `resultset`閉じる前にクエリでこのようなエラーが発生するのを回避するには、URLに`clobberStreamingResults=true`パラメータを追加できます。そうすると、 `resultset`自動的に閉じられますが、前のストリーミングクエリで読み取られる結果セットは失われます。

-   2つ目の方法：まず正の整数として[`FetchSize`設定](http://makejavafaster.blogspot.com/2015/06/jdbc-fetch-size-performance.html)設定し、次にJDBC URLで`useCursorFetch = true`設定することで、カーソルフェッチを使用します。

TiDBは両方の方法をサポートしていますが、実装がよりシンプルで実行効率も優れているため、 `FetchSize`から`Integer.MIN_VALUE`に設定する最初の方法を使用することをお勧めします。

2番目の方法では、TiDBはまずすべてのデータをTiDBノードにロードし、次に`FetchSize`に従ってクライアントにデータを返します。そのため、通常は最初の方法よりも多くのメモリを消費します。3 [`tidb_enable_tmp_storage_on_oom`](/system-variables.md#tidb_enable_tmp_storage_on_oom) `ON`設定されている場合、TiDBは結果を一時的にハードディスクに書き込む可能性があります。

システム変数[`tidb_enable_lazy_cursor_fetch`](/system-variables.md#tidb_enable_lazy_cursor_fetch-new-in-v830) `ON`に設定されている場合、TiDB はクライアントがデータを取得するときにのみデータの一部を読み取ろうとします。これによりメモリ使用量が削減されます。詳細および制限事項については、 [`tidb_enable_lazy_cursor_fetch`システム変数の完全な説明](/system-variables.md#tidb_enable_lazy_cursor_fetch-new-in-v830)を参照してください。

### MySQL JDBC パラメータ {#mysql-jdbc-parameters}

JDBCは通常、JDBC URLパラメータの形式で実装関連の設定を提供します。このセクションでは、 [MySQL Connector/Jのパラメータ設定](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-configuration-properties.html) （MariaDBを使用する場合は[MariaDBのパラメータ設定](https://mariadb.com/docs/connectors/mariadb-connector-j/about-mariadb-connector-j#optional-url-parameters)参照）について説明します。このドキュメントではすべての設定項目を網羅することはできないため、主にパフォーマンスに影響を与える可能性のあるいくつかのパラメータに焦点を当てます。

#### 準備関連パラメータ {#prepare-related-parameters}

このセクションでは、 `Prepare`に関連するパラメータを紹介します。

-   **useServerPrepStmts**

    **useServerPrepStmts は**デフォルトで`false`に設定されています。つまり、Prepare API を使用する場合でも、「prepare」操作はクライアント側でのみ実行されます。サーバーの解析オーバーヘッドを回避するため、同じ SQL ステートメントで Prepare API を複数回使用する場合は、この設定を`true`に設定することをお勧めします。

    この設定が既に有効になっていることを確認するには、次の操作を実行してください。

    -   TiDB モニタリング ダッシュボードに移動し、 **[クエリ概要]** &gt; **[インスタンス別 CPS]**からリクエスト コマンド タイプを確認します。
    -   リクエストで`COM_QUERY` `COM_STMT_EXECUTE`または`COM_STMT_PREPARE`に置き換えられている場合、この設定は既に有効になっていることを意味します。

-   **キャッシュ準備ステートメント**

    `useServerPrepStmts=true`ではサーバーがプリペアドステートメントを実行できますが、デフォルトではクライアントは実行後にプリペアドステートメントを閉じ、再利用しません。つまり、「準備」操作はテキストファイルの実行ほど効率的ではありません。この問題を解決するには、 `useServerPrepStmts=true`設定した後、 `cachePrepStmts=true`設定することをお勧めします。これにより、クライアントはプリペアドステートメントをキャッシュできるようになります。

    この設定が既に有効になっていることを確認するには、次の操作を実行してください。

    -   TiDB モニタリング ダッシュボードに移動し、 **[クエリ概要]** &gt; **[インスタンス別 CPS]**からリクエスト コマンド タイプを確認します。
    -   リクエスト内の`COM_STMT_EXECUTE`の数が`COM_STMT_PREPARE`の数よりはるかに多い場合、この設定は既に有効になっていることを意味します。

    さらに、 `useConfigs=maxPerformance`設定すると、 `cachePrepStmts=true`含む複数のパラメータが同時に設定されます。

-   **prepStmtCacheSqlLimit**

    `cachePrepStmts`設定が完了したら、 `prepStmtCacheSqlLimit`設定（デフォルト値は`256` ）にも注意してください。この設定は、クライアントにキャッシュされるプリペアドステートメントの最大長を制御します。

    この最大長を超えるプリペアドステートメントはキャッシュされないため、再利用できません。この場合、アプリケーションの実際のSQLの長さに応じて、この設定値を増やすことを検討してください。

    次のような場合は、この設定が小さすぎるかどうかを確認する必要があります。

    -   TiDB モニタリング ダッシュボードに移動し、 **[クエリ概要]** &gt; **[インスタンス別 CPS]**からリクエスト コマンド タイプを確認します。
    -   そして、 `cachePrepStmts=true`設定されているが、 `COM_STMT_PREPARE`は依然として`COM_STMT_EXECUTE`とほぼ等しく、 `COM_STMT_CLOSE`存在することがわかった。

-   **prepStmtCacheSize**

    **prepStmtCacheSize は**、キャッシュされるプリペアドステートメントの数を制御します（デフォルト値は`25`です）。アプリケーションで多くの種類の SQL ステートメントを「準備」する必要があり、プリペアドステートメントを再利用したい場合は、この値を増やすことができます。

    この設定が既に有効になっていることを確認するには、次の操作を実行してください。

    -   TiDB モニタリング ダッシュボードに移動し、 **[クエリ概要]** &gt; **[インスタンス別 CPS]**からリクエスト コマンド タイプを確認します。
    -   リクエスト内の`COM_STMT_EXECUTE`の数が`COM_STMT_PREPARE`の数よりはるかに多い場合、この設定は既に有効になっていることを意味します。

#### バッチ関連パラメータ {#batch-related-parameters}

バッチ書き込みを処理する際は、 `rewriteBatchedStatements=true`設定することをお勧めします。3 または`executeBatch()` `addBatch()`使用した後でも、JDBC はデフォルトでは SQL を 1 つずつ送信します。例:

```java
pstmt = prepare("INSERT INTO `t` (a) values(?)");
pstmt.setInt(1, 10);
pstmt.addBatch();
pstmt.setInt(1, 11);
pstmt.addBatch();
pstmt.setInt(1, 12);
pstmt.executeBatch();
```

`Batch`メソッドが使用されているにもかかわらず、TiDBに送信されるSQLステートメントは依然として個別の`INSERT`ステートメントです。

```sql
INSERT INTO `t` (`a`) VALUES(10);
INSERT INTO `t` (`a`) VALUES(11);
INSERT INTO `t` (`a`) VALUES(12);
```

しかし、 `rewriteBatchedStatements=true`設定すると、TiDB に送信される SQL ステートメントは単一の`INSERT`ステートメントになります。

```sql
INSERT INTO `t` (`a`) values(10),(11),(12);
```

`INSERT`のステートメントの書き換えは、複数の「values」キーワードの後の値を連結して、1つのSQLステートメントにすることです。3 `INSERT`のステートメントに他の違いがある場合は、書き換えることはできません。たとえば、次のようになります。

```sql
INSERT INTO `t` (`a`) VALUES (10) ON DUPLICATE KEY UPDATE `a` = 10;
INSERT INTO `t` (`a`) VALUES (11) ON DUPLICATE KEY UPDATE `a` = 11;
INSERT INTO `t` (`a`) VALUES (12) ON DUPLICATE KEY UPDATE `a` = 12;
```

上記の`INSERT`つの文は1つの文に書き換えることはできません。しかし、3つの文を次のように変更すると次のようになります。

```sql
INSERT INTO `t` (`a`) VALUES (10) ON DUPLICATE KEY UPDATE `a` = VALUES(`a`);
INSERT INTO `t` (`a`) VALUES (11) ON DUPLICATE KEY UPDATE `a` = VALUES(`a`);
INSERT INTO `t` (`a`) VALUES (12) ON DUPLICATE KEY UPDATE `a` = VALUES(`a`);
```

すると、書き換え要件を満たします。上記の`INSERT`つの文は、次の1つの文に書き換えられます。

```sql
INSERT INTO `t` (`a`) VALUES (10), (11), (12) ON DUPLICATE KEY UPDATE a = VALUES(`a`);
```

バッチ更新中に3つ以上の更新がある場合、SQLステートメントは書き換えられ、複数のクエリとして送信されます。これにより、クライアントからサーバーへのリクエストのオーバーヘッドは効果的に削減されますが、副作用として、より大きなSQLステートメントが生成されます。例：

```sql
UPDATE `t` SET `a` = 10 WHERE `id` = 1; UPDATE `t` SET `a` = 11 WHERE `id` = 2; UPDATE `t` SET `a` = 12 WHERE `id` = 3;
```

さらに、 [クライアントのバグ](https://bugs.mysql.com/bug.php?id=96623)問題があるため、バッチ更新中に`rewriteBatchedStatements=true`と`useServerPrepStmts=true`を設定する場合は、このバグを回避するために`allowMultiQueries=true`パラメータも設定することをお勧めします。

#### パラメータを統合する {#integrate-parameters}

監視を通じて、アプリケーションが TiDB クラスタに対して実行する操作は`INSERT`だけであるにもかかわらず、冗長な`SELECT`ステートメントが多数あることに気づくかもしれません。通常、これは JDBC が設定を照会するためにいくつかの SQL ステートメントを送信することによって発生します (例: `select @@session.transaction_read_only` )。これらの SQL ステートメントは TiDB にとって不要なので、余分なオーバーヘッドを避けるために`useConfigs=maxPerformance`を設定することをお勧めします。

`useConfigs=maxPerformance`には設定のグループが含まれています。MySQL Connector/J 8.0およびMySQL Connector/J 5.1の詳細な設定については、それぞれ[mysql-connector-j 8.0](https://github.com/mysql/mysql-connector-j/blob/release/8.0/src/main/resources/com/mysql/cj/configurations/maxPerformance.properties)および[mysql-connector-j 5.1](https://github.com/mysql/mysql-connector-j/blob/release/5.1/src/com/mysql/jdbc/configs/maxPerformance.properties)を参照してください。

設定が完了したら、監視画面で`SELECT`ステートメントの数が減少していることを確認できます。

#### タイムアウト関連のパラメータ {#timeout-related-parameters}

TiDB はタイムアウトを制御するために 2 つの MySQL 互換パラメータ ( [`wait_timeout`](/system-variables.md#wait_timeout)と[`max_execution_time`](/system-variables.md#max_execution_time) ) を提供します。これらの 2 つのパラメータはそれぞれ、 Javaアプリケーションとの接続アイドルタイムアウトと接続内の SQL 実行のタイムアウトを制御します。つまり、これらのパラメータは、TiDB とJavaアプリケーション間の接続の最長アイドル時間と最長ビジー時間を制御します。TiDB v5.4 以降、 `wait_timeout`のデフォルト値は`28800`秒で、8 時間です。v5.4 より前の TiDB バージョンでは、デフォルト値は`0`で、タイムアウトは無制限です。11 のデフォルト値は`max_execution_time` `0` 、SQL ステートメントの最大実行時間は無制限であり、 `SELECT`ステートメントすべて ( `SELECT ... FOR UPDATE`を含む) に適用されます。

デフォルト値の[`wait_timeout`](/system-variables.md#wait_timeout)は比較的大きな値です。トランザクションが開始されてもコミットもロールバックもされないような状況では、ロックの保持時間が長引くのを防ぐために、よりきめ細かな制御と短いタイムアウトが必要になる場合があります。このような場合は、 [`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760) （TiDB v7.6.0で導入）を使用して、ユーザーセッション内のトランザクションのアイドルタイムアウトを制御できます。

しかし、実際の本番環境では、アイドル状態の接続や実行時間が長すぎるSQL文は、データベースやアプリケーションに悪影響を及ぼします。アイドル状態の接続や実行時間が長すぎるSQL文を回避するには、アプリケーションの接続文字列でこれらの2つのパラメータを設定できます。例えば、 `sessionVariables=wait_timeout=3600` （1時間）と`sessionVariables=max_execution_time=300000` （5分）を設定します。

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)か[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)についてコミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)
