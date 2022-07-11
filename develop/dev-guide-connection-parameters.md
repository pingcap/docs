---
title: Connection Pools and Connection Parameters
---

# 接続プールと接続パラメータ {#connection-pools-and-connection-parameters}

このドキュメントでは、ドライバまたはORMフレームワークを使用してTiDBに接続するときに、接続プールと接続パラメータを構成する方法について説明します。

Javaアプリケーション開発に関するその他のヒントに興味がある場合は、 [TiDBを使用してJavaアプリケーションを開発するためのベストプラクティス](/best-practices/java-app-best-practices.md#connection-pool)を参照してください。

## 接続プール {#connection-pool}

TiDB（MySQL）接続の構築は、比較的コストがかかります（少なくとも、OLTPシナリオの場合）。 TCP接続の構築に加えて、接続認証も必要になるためです。したがって、クライアントは通常、再利用のためにTiDB（MySQL）接続を接続プールに保存します。

[ドルイド](https://github.com/alibaba/druid)には、 [HikariCP](https://github.com/brettwooldridge/HikariCP)などの多くの接続プールの[c3p0](https://www.mchange.com/projects/c3p0/)が[dbcp](https://commons.apache.org/proper/commons-dbcp/) [tomcat-jdbc](https://tomcat.apache.org/tomcat-7.0-doc/jdbc-pool.html) 。 TiDBは、使用する接続プールを制限しないため、アプリケーションに適した接続プールを選択できます。

### 接続数を設定する {#configure-the-number-of-connections}

接続プールのサイズは、アプリケーション自体のニーズに応じて適切に調整するのが一般的な方法です。例としてHikariCPを取り上げます。

-   **maximumPoolSize** ：接続プール内の接続の最大数。この値が大きすぎると、TiDBはリソースを消費して無駄な接続を維持します。この値が小さすぎると、アプリケーションの接続が遅くなります。したがって、アプリケーションの特性に応じてこの値を構成する必要があります。詳細については、 [プールのサイズについて](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing)を参照してください。
-   **minimumIdle** ：接続プール内のアイドル状態の接続の最小数。これは主に、アプリケーションがアイドル状態のときに突然の要求に応答するために一部の接続を予約するために使用されます。また、アプリケーションの特性に応じて構成する必要があります。

アプリケーションは、使用を終了した後、接続を返す必要があります。アプリケーションは、対応する接続プールの監視（ **metricRegistry**など）を使用して、接続プールの問題を時間内に特定することをお勧めします。

### プローブ構成 {#probe-configuration}

接続プールは、TiDBへの永続的な接続を維持します。 TiDBは、デフォルトでは（エラーが報告されない限り）クライアント接続をプロアクティブに閉じませんが、通常、クライアントとTiDBの間に[LVS](https://en.wikipedia.org/wiki/Linux_Virtual_Server)または[HAProxy](https://en.wikipedia.org/wiki/HAProxy)などのネットワークプロキシもあります。通常、これらのプロキシは、特定の期間アイドル状態になっている接続をプロアクティブにクリーンアップします。プロキシのアイドル構成に注意を払うことに加えて、接続プールは、接続を維持またはプローブする必要もあります。

Javaアプリケーションで次のエラーが頻繁に発生する場合：

```
The last packet sent successfully to the server was 3600000 milliseconds ago. The driver has not received any packets from the server. com.mysql.jdbc.exceptions.jdbc4.CommunicationsException: Communications link failure
```

`n milliseconds ago`の`n`が`0`または非常に小さい値である場合、通常、実行されたSQL操作によってTiDBが異常終了することが原因です。原因を特定するには、TiDBstderrログを確認することをお勧めします。

`n`が非常に大きい値（上記の例の`3600000`など）である場合、この接続は長時間アイドル状態であり、その後プロキシによって閉じられた可能性があります。通常の解決策は、プロキシのアイドル構成の値を増やし、接続プールが次のことを行えるようにすることです。

-   毎回接続を使用する前に、接続が使用可能かどうかを確認してください。
-   別のスレッドを使用して接続が使用可能かどうかを定期的に確認してください。
-   定期的にテストクエリを送信して、接続を維持します。

異なる接続プールの実装は、上記の方法の1つ以上をサポートする場合があります。接続プールのドキュメントを確認して、対応する構成を見つけることができます。

### 経験に基づく公式 {#formulas-based-on-experience}

HikariCPの[プールのサイズについて](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing)の記事によると、データベース接続プールに適切なサイズを設定する方法がわからない場合は、 [経験に基づく公式](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing#connections--core_count--2--effective_spindle_count)から始めることができます。次に、式から計算されたプールサイズのパフォーマンス結果に基づいて、サイズをさらに調整して、最高のパフォーマンスを実現できます。

経験に基づく計算式は次のとおりです。

```
connections = ((core_count * 2) + effective_spindle_count)
```

式の各パラメーターの説明は次のとおりです。

-   **接続**：取得された接続のサイズ。
-   **core_count** ：CPUコアの数。
-   **Effective_spindle_count** ：ハードドライブの数（ [SSD](https://en.wikipedia.org/wiki/Solid-state_drive)ではありません）。回転する各ハードディスクはスピンドルと呼ぶことができるからです。たとえば、16個のディスクのRAIDを備えたサーバーを使用している場合、 <strong>effective_spindle_count</strong>は16になります<strong>。HDD</strong>は通常一度に1つの要求しか処理できないため、ここでの式は、サーバーが実行できる同時I/O要求の数を実際に測定しています。管理。

特に、 [方式](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing#the-formula)の下にある次の注意事項に注意してください。

> ```
> A formula which has held up pretty well across a lot of benchmarks for years is
> that for optimal throughput the number of active connections should be somewhere
> near ((core_count * 2) + effective_spindle_count). Core count should not include
> HT threads, even if hyperthreading is enabled. Effective spindle count is zero if
> the active data set is fully cached, and approaches the actual number of spindles
> as the cache hit rate falls. ... There hasn't been any analysis so far regarding
> how well the formula works with SSDs.
> ```

このメモは次のことを示しています。

-   **core_count**は、 [ハイパースレッディング](https://en.wikipedia.org/wiki/Hyper-threading)を有効にするかどうかに関係なく、物理コアの数です。
-   データが完全にキャッシュされたら、 **effective_spindle_count**を`0`に設定する必要があります。キャッシュのヒット率が低下すると、カウントは実際の`HDD`に近づきます。
-   **公式が*SSD*で機能するかどうかはテストされておらず、不明です。**

SSDを使用する場合は、代わりに経験に基づいて次の式を使用することをお勧めします。

```
connections = (number of cores * 4)
```

したがって、SSDの場合は初期接続プールの最大接続サイズを`cores * 4`に設定し、さらにサイズを調整してパフォーマンスを調整できます。

### チューニングの方向 {#tuning-direction}

ご覧のとおり、 [経験に基づく公式](#formulas-based-on-experience)から計算されたサイズは単なる推奨ベース値です。特定のマシンで最適なサイズを取得するには、基本値の前後で他の値を試して、パフォーマンスをテストする必要があります。

最適なサイズを取得するための基本的なルールは次のとおりです。

-   ネットワークまたはストレージの遅延が大きい場合は、接続の最大数を増やして、遅延の待機時間を短縮します。スレッドがレイテンシーによってブロックされると、他のスレッドが引き継いで処理を続行できます。
-   サーバーに複数のサービスがデプロイされていて、各サービスに個別の接続プールがある場合は、すべての接続プールへの接続の最大数の合計を考慮してください。

## 接続パラメータ {#connection-parameters}

Javaアプリケーションは、さまざまなフレームワークでカプセル化できます。ほとんどのフレームワークでは、JDBC APIは、データベースサーバーと対話するために最下位レベルで呼び出されます。 JDBCの場合、次のことに焦点を当てることをお勧めします。

-   JDBCAPIの使用法の選択
-   API実装者のパラメーター構成

### JDBC API {#jdbc-api}

JDBC APIの使用法については、 [JDBC公式チュートリアル](https://docs.oracle.com/javase/tutorial/jdbc/)を参照してください。このセクションでは、いくつかの重要なAPIの使用法について説明します。

#### 準備APIを使用する {#use-prepare-api}

OLTP（Online Transactional Processing）シナリオの場合、プログラムによってデータベースに送信されるSQLステートメントは、パラメーターの変更を削除した後に使い果たされる可能性のあるいくつかのタイプです。したがって、通常の[テキストファイルからの実行](https://docs.oracle.com/javase/tutorial/jdbc/basics/processingsqlstatements.html#executing_queries)ではなく[プリペアドステートメント](https://docs.oracle.com/javase/tutorial/jdbc/basics/prepared.html)を使用し、PreparedStatementsを再利用して直接実行することをお勧めします。これにより、TiDBでSQL実行プランを繰り返し解析および生成するオーバーヘッドが回避されます。

現在、ほとんどの上位レベルのフレームワークは、SQL実行のために準備APIを呼び出します。開発にJDBCAPIを直接使用する場合は、PrepareAPIの選択に注意してください。

さらに、MySQL Connector / Jのデフォルトの実装では、クライアント側のステートメントのみが前処理され、クライアントで`?`が置き換えられた後、ステートメントはテキストファイルでサーバーに送信されます。したがって、Prepare APIを使用することに加えて、TiDBサーバーでステートメントの前処理を実行する前に、JDBC接続パラメーターで`useServerPrepStmts = true`を構成する必要もあります。パラメータ設定の詳細については、 [MySQLJDBCパラメータ](#mysql-jdbc-parameters)を参照してください。

#### バッチAPIを使用する {#use-batch-api}

バッチ挿入の場合は、 [`addBatch` / <code>executeBatch</code> API](https://www.tutorialspoint.com/jdbc/jdbc-batch-processing)を使用できます。 `addBatch()`メソッドは、最初にクライアントで複数のSQLステートメントをキャッシュし、次に`executeBatch`メソッドを呼び出すときにそれらをデータベースサーバーに一緒に送信するために使用されます。

> **ノート：**
>
> デフォルトのMySQLConnector/ J実装では、 `addBatch()`でバッチに追加されたSQLステートメントの送信時間は、 `executeBatch()`が呼び出された時間まで遅延しますが、実際のネットワーク転送中にステートメントは1つずつ送信されます。したがって、この方法では通常、通信のオーバーヘッドを減らすことはできません。
>
> ネットワーク転送をバッチ処理する場合は、JDBC接続パラメーターで`rewriteBatchedStatements = true`を構成する必要があります。詳細なパラメータ設定については、 [バッチ関連のパラメーター](#batch-related-parameters)を参照してください。

#### <code>StreamingResult</code>を使用して実行結果を取得します {#use-code-streamingresult-code-to-get-the-execution-result}

ほとんどのシナリオでは、実行効率を向上させるために、JDBCはクエリ結果を事前に取得し、デフォルトでクライアントメモリに保存します。しかし、クエリが非常に大きな結果セットを返す場合、クライアントはデータベースサーバーが一度に返されるレコードの数を減らして、クライアントのメモリの準備ができて次のバッチを要求するまで待機することを望んでいることがよくあります。

通常、JDBCには2種類の処理方法があります。

-   [**FetchSize**を`Integer.MIN_VALUE`に設定します](https://dev.mysql.com/doc/connector-j/5.1/en/connector-j-reference-implementation-notes.html#ResultSet)は、クライアントがキャッシュしないようにします。クライアントは、 `StreamingResult`を介してネットワーク接続から実行結果を読み取ります。

    クライアントがストリーミング読み取りメソッドを使用する場合、ステートメントを使用してクエリを実行し続ける前に、読み取りを終了するか、 `resultset`を閉じる必要があります。それ以外の場合は、エラー`No statements may be issued when any streaming result sets are open and in use on a given connection. Ensure that you have called .close() on any active streaming result sets before attempting more queries.`が返されます。

    クライアントが読み取りを終了するか`resultset`を閉じる前にクエリでこのようなエラーを回避するために、URLに`clobberStreamingResults=true`パラメータを追加できます。次に、 `resultset`は自動的に閉じられますが、前のストリーミングクエリで読み取られる結果セットは失われます。

-   カーソルフェッチを使用するには、最初に[`FetchSize`を設定します](http://makejavafaster.blogspot.com/2015/06/jdbc-fetch-size-performance.html)を正の整数として使用し、JDBCURLで`useCursorFetch=true`を構成します。

TiDBは両方の方法をサポートしていますが、実装が単純で実行効率が高いため、最初の方法を使用することをお勧めします。

### MySQLJDBCパラメータ {#mysql-jdbc-parameters}

JDBCは通常、実装関連の構成をJDBCURLパラメーターの形式で提供します。このセクションでは[MySQL Connector/Jのパラメータ構成](https://dev.mysql.com/doc/connector-j/5.1/en/connector-j-reference-configuration-properties.html)を紹介します（MariaDBを使用する場合は、 [MariaDBのパラメーター構成](https://mariadb.com/kb/en/library/about-mariadb-connector-j/#optional-url-parameters)を参照してください）。このドキュメントはすべての構成項目を網羅しているわけではないため、パフォーマンスに影響を与える可能性のあるいくつかのパラメーターに主に焦点を当てています。

#### 関連するパラメータを準備する {#prepare-related-parameters}

このセクションでは、 `Prepare`に関連するパラメーターを紹介します。

-   **useServerPrepStmts**

    **useServerPrepStmts**はデフォルトで`false`に設定されています。つまり、Prepare APIを使用している場合でも、「prepare」操作はクライアントでのみ実行されます。サーバーの解析オーバーヘッドを回避するために、同じSQLステートメントがPrepare APIを複数回使用する場合は、この構成を`true`に設定することをお勧めします。

    この設定がすでに有効になっていることを確認するには、次のようにします。

    -   TiDBモニタリングダッシュボードに移動し、[ **Query Summary** ]&gt; [ <strong>QPSByInstance</strong> ]からリクエストコマンドタイプを表示します。
    -   リクエストで`COM_QUERY`が`COM_STMT_EXECUTE`または`COM_STMT_PREPARE`に置き換えられた場合、この設定はすでに有効になっていることを意味します。

-   **cachePrepStmts**

    `useServerPrepStmts=true`を使用すると、サーバーはプリペアドステートメントを実行できますが、デフォルトでは、クライアントは実行のたびにプリペアドステートメントを閉じ、それらを再利用しません。これは、「準備」操作がテキストファイルの実行ほど効率的ではないことを意味します。これを解決するには、 `useServerPrepStmts=true`を設定した後、 `cachePrepStmts=true`も構成することをお勧めします。これにより、クライアントはプリペアドステートメントをキャッシュできます。

    この設定がすでに有効になっていることを確認するには、次のようにします。

    -   TiDBモニタリングダッシュボードに移動し、[ **Query Summary** ]&gt; [ <strong>QPSByInstance</strong> ]からリクエストコマンドタイプを表示します。
    -   リクエストの`COM_STMT_EXECUTE`の数が`COM_STMT_PREPARE`の数よりはるかに多い場合は、この設定がすでに有効になっていることを意味します。

    ![QPS By Instance](/media/java-practice-2.png)

    さらに、 `useConfigs=maxPerformance`を構成すると、 `cachePrepStmts=true`を含む複数のパラメーターが同時に構成されます。

-   **prepStmtCacheSqlLimit**

    `cachePrepStmts`を構成した後、 `prepStmtCacheSqlLimit`の構成にも注意してください（デフォルト値は`256`です）。この構成は、クライアントにキャッシュされる準備済みステートメントの最大長を制御します。

    この最大長を超えるプリペアドステートメントはキャッシュされないため、再利用できません。この場合、アプリケーションの実際のSQLの長さに応じて、この構成の値を増やすことを検討できます。

    次の場合は、この設定が小さすぎるかどうかを確認する必要があります。

    -   TiDBモニタリングダッシュボードに移動し、[ **Query Summary** ]&gt; [ <strong>QPSByInstance</strong> ]からリクエストコマンドタイプを表示します。
    -   そして、 `cachePrepStmts=true`が構成されているが、 `COM_STMT_PREPARE`はまだほとんど`COM_STMT_EXECUTE`に等しく、 `COM_STMT_CLOSE`が存在することを確認します。

-   **prepStmtCacheSize**

    **prepStmtCacheSize**は、キャッシュされるプリペアドステートメントの数を制御します（デフォルト値は`25`です）。アプリケーションで多くの種類のSQLステートメントを「準備」する必要があり、準備済みステートメントを再利用したい場合は、この値を増やすことができます。

    この設定がすでに有効になっていることを確認するには、次のようにします。

    -   TiDBモニタリングダッシュボードに移動し、[ **Query Summary** ]&gt; [ <strong>QPSByInstance</strong> ]からリクエストコマンドタイプを表示します。
    -   リクエストの`COM_STMT_EXECUTE`の数が`COM_STMT_PREPARE`の数よりはるかに多い場合は、この設定がすでに有効になっていることを意味します。

#### バッチ関連のパラメーター {#batch-related-parameters}

バッチ書き込みの処理中に、 `rewriteBatchedStatements=true`を構成することをお勧めします。 `addBatch()`または`executeBatch()`を使用した後でも、JDBCはデフォルトでSQLを1つずつ送信します。次に例を示します。

{{< copyable "" >}}

```java
pstmt = prepare("INSERT INTO `t` (a) values(?)");
pstmt.setInt(1, 10);
pstmt.addBatch();
pstmt.setInt(1, 11);
pstmt.addBatch();
pstmt.setInt(1, 12);
pstmt.executeBatch();
```

`Batch`のメソッドが使用されますが、TiDBに送信されるSQLステートメントは依然として個別の`INSERT`のステートメントです。

{{< copyable "" >}}

```sql
INSERT INTO `t` (`a`) VALUES(10);
INSERT INTO `t` (`a`) VALUES(11);
INSERT INTO `t` (`a`) VALUES(12);
```

ただし、 `rewriteBatchedStatements=true`を設定すると、TiDBに送信されるSQLステートメントは単一の`INSERT`ステートメントになります。

{{< copyable "" >}}

```sql
INSERT INTO `t` (`a`) values(10),(11),(12);
```

`INSERT`ステートメントの書き直しは、複数の「values」キーワードの後の値をSQLステートメント全体に連結することであることに注意してください。 `INSERT`のステートメントに他の違いがある場合、次のように書き換えることはできません。

{{< copyable "" >}}

```sql
INSERT INTO `t` (`a`) VALUES (10) ON DUPLICATE KEY UPDATE `a` = 10;
INSERT INTO `t` (`a`) VALUES (11) ON DUPLICATE KEY UPDATE `a` = 11;
INSERT INTO `t` (`a`) VALUES (12) ON DUPLICATE KEY UPDATE `a` = 12;
```

上記の`INSERT`つのステートメントを1つのステートメントに書き換えることはできません。ただし、3つのステートメントを次のステートメントに変更した場合：

{{< copyable "" >}}

```sql
INSERT INTO `t` (`a`) VALUES (10) ON DUPLICATE KEY UPDATE `a` = VALUES(`a`);
INSERT INTO `t` (`a`) VALUES (11) ON DUPLICATE KEY UPDATE `a` = VALUES(`a`);
INSERT INTO `t` (`a`) VALUES (12) ON DUPLICATE KEY UPDATE `a` = VALUES(`a`);
```

次に、それらは書き換え要件を満たします。上記の`INSERT`つのステートメントは、次の1つのステートメントに書き換えられます。

{{< copyable "" >}}

```sql
INSERT INTO `t` (`a`) VALUES (10), (11), (12) ON DUPLICATE KEY UPDATE a = VALUES(`a`);
```

バッチ更新中に3つ以上の更新がある場合、SQLステートメントは書き直され、複数のクエリとして送信されます。これにより、クライアントからサーバーへの要求のオーバーヘッドが効果的に削減されますが、副作用として、より大きなSQLステートメントが生成されます。例えば：

{{< copyable "" >}}

```sql
UPDATE `t` SET `a` = 10 WHERE `id` = 1; UPDATE `t` SET `a` = 11 WHERE `id` = 2; UPDATE `t` SET `a` = 12 WHERE `id` = 3;
```

さらに、 [クライアントのバグ](https://bugs.mysql.com/bug.php?id=96623)のため、バッチ更新中に`rewriteBatchedStatements=true`と`useServerPrepStmts=true`を構成する場合は、このバグを回避するために`allowMultiQueries=true`パラメーターも構成することをお勧めします。

#### パラメータを統合する {#integrate-parameters}

監視を通じて、アプリケーションがTiDBクラスタに対して`INSERT`の操作しか実行しないにもかかわらず、冗長な`SELECT`のステートメントが多数あることに気付く場合があります。通常、これは、JDBCが設定をクエリするためにいくつかのSQLステートメントを送信するために発生します（例： `select @@session.transaction_read_only` ）。これらのSQLステートメントはTiDBには役に立たないため、余分なオーバーヘッドを回避するために`useConfigs=maxPerformance`を構成することをお勧めします。

`useConfigs=maxPerformance`構成には、構成のグループが含まれます。

```ini
cacheServerConfiguration=true
useLocalSessionState=true
elideSetAutoCommits=true
alwaysSendSetIsolation=false
enableQueryTimeouts=false
```

設定後、モニタリングをチェックして、 `SELECT`ステートメントの数が減少していることを確認できます。

#### タイムアウト関連のパラメーター {#timeout-related-parameters}

TiDBは、タイムアウトを制御するための2つのMySQL互換パラメーター**wait_timeout**と<strong>max_execution_time</strong>を提供します。これらの2つのパラメーターはそれぞれ、Javaアプリケーションとの接続アイドルタイムアウトと接続でのSQL実行のタイムアウトを制御します。つまり、これらのパラメータは、TiDBとJavaアプリケーション間の接続の最長アイドル時間と最長ビジー時間を制御します。両方のパラメーターのデフォルト値は`0`です。これにより、デフォルトで接続が無限にアイドル状態になり、無限にビジーになります（1つのSQLステートメントが実行されるまでの期間は無限になります）。

ただし、実際の実稼働環境では、実行時間が長すぎるアイドル状態の接続とSQLステートメントは、データベースとアプリケーションに悪影響を及ぼします。アイドル状態の接続と長時間実行されるSQLステートメントを回避するために、アプリケーションの接続文字列でこれら2つのパラメーターを構成できます。たとえば、 `sessionVariables=wait_timeout=3600` （1時間）と`sessionVariables=max_execution_time=300000` （5分）を設定します。
