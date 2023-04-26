---
title: Connection Pools and Connection Parameters
---

# 接続プールと接続パラメータ {#connection-pools-and-connection-parameters}

このドキュメントでは、ドライバーまたは ORM フレームワークを使用して TiDB に接続するときに、接続プールと接続パラメーターを構成する方法について説明します。

<CustomContent platform="tidb">

Javaアプリケーション開発に関するその他のヒントに興味がある場合は、 [TiDB でJavaアプリケーションを開発するためのベスト プラクティス](/best-practices/java-app-best-practices.md#connection-pool)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

Javaアプリケーション開発に関するその他のヒントに興味がある場合は、 [TiDB でJavaアプリケーションを開発するためのベスト プラクティス](https://docs.pingcap.com/tidb/stable/java-app-best-practices)を参照してください。

</CustomContent>

## 接続プール {#connection-pool}

TiDB (MySQL) 接続の構築は比較的高価です (少なくとも OLTP シナリオの場合)。 TCP 接続の構築に加えて、接続認証も必要になるためです。したがって、クライアントは通常、再利用のために TiDB (MySQL) 接続を接続プールに保存します。

Java には、 [HikariCP](https://github.com/brettwooldridge/HikariCP) 、 [tomcat-jdbc](https://tomcat.apache.org/tomcat-10.1-doc/jdbc-pool.html) 、 [druid](https://github.com/alibaba/druid) 、 [c3p0](https://www.mchange.com/projects/c3p0/) 、および[dbcp](https://commons.apache.org/proper/commons-dbcp/)などの多くの接続プールの実装があります。 TiDB は、使用する接続プールを制限しないため、アプリケーションに合わせて好きなものを選択できます。

### 接続数を構成する {#configure-the-number-of-connections}

接続プールのサイズは、アプリケーション自体のニーズに合わせて適切に調整するのが一般的です。例としてHikariCP を取り上げます。

-   **maximumPoolSize** : 接続プール内の接続の最大数。この値が大きすぎると、TiDB は無駄な接続を維持するためにリソースを消費します。この値が小さすぎると、アプリケーションの接続が遅くなります。したがって、アプリケーションの特性に応じてこの値を構成する必要があります。詳細については、 [プールのサイジングについて](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing)を参照してください。
-   **minimumIdle** : 接続プール内のアイドル接続の最小数。主に、アプリケーションがアイドル状態のときに突然の要求に応答するために、いくつかの接続を予約するために使用されます。また、アプリケーションの特性に応じて構成する必要があります。

アプリケーションは、使用終了後に接続を返す必要があります。アプリケーションで対応する接続プール監視 ( **metricRegistry**など) を使用して、接続プールの問題を時間内に特定することをお勧めします。

### プローブ構成 {#probe-configuration}

接続プールは、TiDB への永続的な接続を維持します。デフォルトでは、TiDB は積極的にクライアント接続を閉じませんが (エラーが報告されない限り)、通常、クライアントと TiDB の間に[LVS](https://en.wikipedia.org/wiki/Linux_Virtual_Server)や[HAProxy](https://en.wikipedia.org/wiki/HAProxy)などのネットワーク プロキシもあります。通常、これらのプロキシは、一定期間アイドル状態になっている接続をプロアクティブにクリーンアップします。プロキシのアイドル構成に注意を払うことに加えて、接続プールは、接続を維持するかプローブする必要もあります。

Javaアプリケーションで次のエラーが頻繁に表示される場合:

```
The last packet sent successfully to the server was 3600000 milliseconds ago. The driver has not received any packets from the server. com.mysql.jdbc.exceptions.jdbc4.CommunicationsException: Communications link failure
```

`n` `n milliseconds ago` `0`または非常に小さい値である場合、通常は、実行された SQL 操作によって TiDB が異常終了するためです。原因を特定するには、TiDB の stderr ログを確認することをお勧めします。

`n`が非常に大きな値 (上記の例の`3600000`など) である場合、この接続は長時間アイドル状態であり、その後プロキシによって閉じられた可能性があります。通常の解決策は、プロキシのアイドル構成の値を増やし、接続プールで次のことができるようにすることです。

-   毎回接続を使用する前に、接続が利用可能かどうかを確認してください。
-   別のスレッドを使用して、接続が利用可能かどうかを定期的に確認してください。
-   テスト クエリを定期的に送信して、接続を維持します。

異なる接続プールの実装では、上記のメソッドの 1 つ以上がサポートされている場合があります。接続プールのドキュメントを確認して、対応する構成を見つけることができます。

### 経験に基づく公式 {#formulas-based-on-experience}

HikariCPの[プールのサイジングについて](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing)記事によると、データベース接続プールの適切なサイズを設定する方法がわからない場合は、 [経験に基づく公式](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing#connections--core_count--2--effective_spindle_count)から始めることができます。次に、式から計算されたプール サイズのパフォーマンス結果に基づいて、最適なパフォーマンスを実現するためにサイズをさらに調整できます。

経験に基づいた式は次のとおりです。

```
connections = ((core_count * 2) + effective_spindle_count)
```

式の各パラメータの説明は次のとおりです。

-   **connections** : 取得した接続のサイズ。
-   **core_count** : CPU コアの数。
-   **effective_spindle_count** : ハード ドライブの数 ( [SSD](https://en.wikipedia.org/wiki/Solid-state_drive)ではありません)。回転する各ハードディスクをスピンドルと呼ぶことができるからです。たとえば、16 ディスクの RAID を備えたサーバーを使用している場合、 <strong>effective_spindle_count</strong>は 16 にする必要があります。HDD<strong>は</strong>通常、一度に 1 つの要求しか処理できないため、ここでの式は、サーバーが同時に処理できる I/O 要求の数を実際に測定しています。管理。

特に、 [方式](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing#the-formula)の下の次の注意事項に注意してください。

> ```
> A formula which has held up pretty well across a lot of benchmarks for years is
> that for optimal throughput the number of active connections should be somewhere
> near ((core_count * 2) + effective_spindle_count). Core count should not include
> HT threads, even if hyperthreading is enabled. Effective spindle count is zero if
> the active data set is fully cached, and approaches the actual number of spindles
> as the cache hit rate falls. ... There hasn't been any analysis so far regarding
> how well the formula works with SSDs.
> ```

この注記は、次のことを示しています。

-   **core_count は**、 [ハイパースレッディング](https://en.wikipedia.org/wiki/Hyper-threading)有効にするかどうかに関係なく、物理コアの数です。
-   データが完全にキャッシュされたら、 **effective_spindle_count**を`0`に設定する必要があります。キャッシュのヒット率が低下するにつれて、カウントは実際の`HDD`の数に近づきます。
-   **数式が*SSD*で機能するかどうかはテストされておらず、不明です。**

SSD を使用する場合は、代わりに経験に基づいて次の式を使用することをお勧めします。

```
connections = (number of cores * 4)
```

したがって、SSD の場合は初期接続プールの最大接続サイズを`cores * 4`に設定し、さらにサイズを調整してパフォーマンスを調整できます。

### チューニング方向 {#tuning-direction}

ご覧のとおり、 [経験に基づく公式](#formulas-based-on-experience)から計算されたサイズは、推奨される基本値にすぎません。特定のマシンで最適なサイズを取得するには、基本値に近い他の値を試して、パフォーマンスをテストする必要があります。

最適なサイズを得るのに役立ついくつかの基本的なルールを次に示します。

-   ネットワークまたはstorageのレイテンシーが長い場合は、接続の最大数を増やしてレイテンシーを短縮します。スレッドがレイテンシーによってブロックされると、他のスレッドが引き継ぎ、処理を続行できます。
-   サーバーに複数のサービスがデプロイされていて、各サービスに個別の接続プールがある場合は、すべての接続プールへの最大接続数の合計を考慮してください。

## 接続パラメータ {#connection-parameters}

Javaアプリケーションは、さまざまなフレームワークでカプセル化されたできます。ほとんどのフレームワークでは、JDBC API が最下位レベルで呼び出され、データベースサーバーと対話します。 JDBC の場合、次の点に注目することをお勧めします。

-   JDBC API の使用方法の選択
-   API 実装者のパラメーター構成

### JDBC API {#jdbc-api}

JDBC API の使用法については、 [JDBC 公式チュートリアル](https://docs.oracle.com/javase/tutorial/jdbc/)を参照してください。このセクションでは、いくつかの重要な API の使用法について説明します。

#### 準備 API を使用する {#use-prepare-api}

OLTP (オンライン トランザクション処理) シナリオの場合、プログラムによってデータベースに送信される SQL ステートメントは、パラメーターの変更を削除した後に使い果たされる可能性があるいくつかのタイプです。したがって、通常の[テキストファイルからの実行](https://docs.oracle.com/javase/tutorial/jdbc/basics/processingsqlstatements.html#executing_queries)の代わりに[準備されたステートメント](https://docs.oracle.com/javase/tutorial/jdbc/basics/prepared.html)使用し、Prepared Statements を再利用して直接実行することをお勧めします。これにより、TiDB で SQL 実行計画を繰り返し解析して生成するオーバーヘッドが回避されます。

現在、ほとんどの上位レベルのフレームワークは、SQL 実行のために Prepare API を呼び出します。開発に JDBC API を直接使用する場合は、Prepare API の選択に注意してください。

さらに、MySQL Connector/J のデフォルトの実装では、クライアント側のステートメントのみが前処理され、ステートメントはクライアントで`?`置き換えられた後、テキスト ファイルでサーバーに送信されます。したがって、Prepare API の使用に加えて、TiDBサーバーでステートメントの前処理を実行する前に、JDBC 接続パラメーターで`useServerPrepStmts = true`も構成する必要があります。詳細なパラメータ設定については、 [MySQL JDBC パラメータ](#mysql-jdbc-parameters)を参照してください。

#### バッチ API を使用する {#use-batch-api}

バッチ挿入の場合は、 [`addBatch` / <code>executeBatch</code> API](https://www.tutorialspoint.com/jdbc/jdbc-batch-processing)を使用できます。メソッド`addBatch()`は、最初に複数の SQL ステートメントをクライアントにキャッシュし、次にメソッド`executeBatch`を呼び出すときにそれらを一緒にデータベースサーバーに送信するために使用されます。

> **ノート：**
>
> デフォルトの MySQL Connector/J 実装では、 `addBatch()`でバッチに追加された SQL ステートメントの送信時刻は`executeBatch()`呼び出される時刻まで遅延しますが、実際のネットワーク転送中にステートメントは 1 つずつ送信されます。したがって、この方法では通常、通信オーバーヘッドの量は減少しません。
>
> ネットワーク転送をバッチ処理する場合は、JDBC 接続パラメーターで`rewriteBatchedStatements = true`を構成する必要があります。詳細なパラメータ設定については、 [バッチ関連のパラメーター](#batch-related-parameters)を参照してください。

#### <code>StreamingResult</code>使用して実行結果を取得する {#use-code-streamingresult-code-to-get-the-execution-result}

ほとんどのシナリオでは、実行効率を向上させるために、JDBC は事前にクエリ結果を取得し、デフォルトでクライアントメモリに保存します。しかし、クエリが非常に大きな結果セットを返す場合、クライアントはデータベースサーバーに一度に返されるレコードの数を減らすことを要求し、クライアントのメモリの準備が整い、次のバッチを要求するまで待機します。

通常、JDBC には 2 種類の処理方法があります。

-   [**FetchSize を**`Integer.MIN_VALUE`に設定します](https://dev.mysql.com/doc/connector-j/8.0/en/connector-j-reference-implementation-notes.html#ResultSet)を指定すると、クライアントはキャッシュされません。クライアントは`StreamingResult`を介してネットワーク接続から実行結果を読み取ります。

    クライアントがストリーミング読み取りメソッドを使用する場合、ステートメントを使用してクエリを作成し続ける前に、読み取りを終了するか、 `resultset`を閉じる必要があります。それ以外の場合は、エラー`No statements may be issued when any streaming result sets are open and in use on a given connection. Ensure that you have called .close() on any active streaming result sets before attempting more queries.`が返されます。

    クライアントが`resultset`読み取りを終了するか閉じる前にクエリでこのようなエラーを回避するには、URL に`clobberStreamingResults=true`パラメーターを追加します。次に、 `resultset`は自動的に閉じられますが、前のストリーミング クエリで読み取られる結果セットは失われます。

-   Cursor Fetch を使用するには、最初に正の整数として[`FetchSize`を設定](http://makejavafaster.blogspot.com/2015/06/jdbc-fetch-size-performance.html)し、JDBC URL で`useCursorFetch=true`構成します。

TiDB は両方の方法をサポートしていますが、最初の方法を使用することをお勧めします。これは、実装がより単純で実行効率が高いためです。

### MySQL JDBC パラメータ {#mysql-jdbc-parameters}

JDBC は通常、JDBC URL パラメータの形式で実装関連の構成を提供します。このセクションでは[MySQL Connector/J のパラメータ設定](https://dev.mysql.com/doc/connector-j/8.0/en/connector-j-reference-configuration-properties.html)を紹介します (MariaDB を使用する場合は[MariaDB のパラメーター構成](https://mariadb.com/kb/en/library/about-mariadb-connector-j/#optional-url-parameters)を参照してください)。このドキュメントではすべての構成項目を取り上げることはできないため、主にパフォーマンスに影響を与える可能性があるいくつかのパラメーターに焦点を当てています。

#### 準備関連パラメータ {#prepare-related-parameters}

このセクションでは、 `Prepare`に関連するパラメーターを紹介します。

-   **useServerPrepStmts**

    **useServerPrepStmts は**デフォルトで`false`に設定されています。つまり、Prepare API を使用した場合でも、「準備」操作はクライアントでのみ行われます。サーバーの解析オーバーヘッドを回避するために、同じ SQL ステートメントで Prepare API を複数回使用する場合は、この構成を`true`に設定することをお勧めします。

    この設定が既に有効になっていることを確認するには、次のようにします。

    -   TiDB モニタリング ダッシュボードに移動し、 **[Query Summary]** &gt; <strong>[CPS By Instance]</strong>からリクエスト コマンド タイプを表示します。
    -   リクエストで`COM_QUERY` `COM_STMT_EXECUTE`または`COM_STMT_PREPARE`に置き換えられている場合は、この設定がすでに有効になっていることを意味します。

-   **cachePrepStmts**

    `useServerPrepStmts=true`を指定すると、サーバーはプリペアド ステートメントを実行できますが、デフォルトでは、クライアントは各実行後にプリペアド ステートメントを閉じ、それらを再利用しません。これは、「準備」操作がテキスト ファイルの実行ほど効率的ではないことを意味します。これを解決するには、 `useServerPrepStmts=true`設定した後、 `cachePrepStmts=true`も設定することをお勧めします。これにより、クライアントはプリペアド ステートメントをキャッシュできます。

    この設定が既に有効になっていることを確認するには、次のようにします。

    -   TiDB モニタリング ダッシュボードに移動し、 **[Query Summary]** &gt; <strong>[CPS By Instance]</strong>からリクエスト コマンド タイプを表示します。
    -   リクエスト内の`COM_STMT_EXECUTE`の数が`COM_STMT_PREPARE`の数よりはるかに多い場合、この設定はすでに有効になっていることを意味します。

    さらに、 `useConfigs=maxPerformance`を構成すると、 `cachePrepStmts=true`を含む複数のパラメーターが同時に構成されます。

-   **prepStmtCacheSqlLimit**

    `cachePrepStmts`を設定したら、 `prepStmtCacheSqlLimit`設定にも注意してください (デフォルト値は`256`です)。この構成は、クライアントにキャッシュされるプリペアド ステートメントの最大長を制御します。

    この最大長を超えるプリペアド ステートメントはキャッシュされないため、再利用できません。この場合、アプリケーションの実際の SQL 長に応じて、この構成の値を増やすことを検討してください。

    次の場合は、この設定が小さすぎるかどうかを確認する必要があります。

    -   TiDB モニタリング ダッシュボードに移動し、 **[Query Summary]** &gt; <strong>[CPS By Instance]</strong>からリクエスト コマンド タイプを表示します。
    -   `cachePrepStmts=true`が構成されていることを確認しますが、 `COM_STMT_PREPARE`はまだ`COM_STMT_EXECUTE`とほぼ等しく、 `COM_STMT_CLOSE`存在します。

-   **prepStmtCacheSize**

    **prepStmtCacheSize は、**キャッシュされるプリペアド ステートメントの数を制御します (デフォルト値は`25`です)。アプリケーションで多くの種類の SQL ステートメントを「準備」する必要があり、準備済みステートメントを再利用したい場合は、この値を増やすことができます。

    この設定が既に有効になっていることを確認するには、次のようにします。

    -   TiDB モニタリング ダッシュボードに移動し、 **[Query Summary]** &gt; <strong>[CPS By Instance]</strong>からリクエスト コマンド タイプを表示します。
    -   リクエスト内の`COM_STMT_EXECUTE`の数が`COM_STMT_PREPARE`の数よりはるかに多い場合、この設定はすでに有効になっていることを意味します。

#### バッチ関連のパラメーター {#batch-related-parameters}

バッチ書き込みの処理中は、 `rewriteBatchedStatements=true`を構成することをお勧めします。 `addBatch()`または`executeBatch()`使用した後でも、JDBC はデフォルトで SQL を 1 つずつ送信します。次に例を示します。

```java
pstmt = prepare("INSERT INTO `t` (a) values(?)");
pstmt.setInt(1, 10);
pstmt.addBatch();
pstmt.setInt(1, 11);
pstmt.addBatch();
pstmt.setInt(1, 12);
pstmt.executeBatch();
```

`Batch`メソッドが使用されますが、TiDB に送信される SQL ステートメントは依然として個別の`INSERT`のステートメントです。

```sql
INSERT INTO `t` (`a`) VALUES(10);
INSERT INTO `t` (`a`) VALUES(11);
INSERT INTO `t` (`a`) VALUES(12);
```

ただし、 `rewriteBatchedStatements=true`を設定すると、TiDB に送信される SQL ステートメントは単一の`INSERT`ステートメントになります。

```sql
INSERT INTO `t` (`a`) values(10),(11),(12);
```

`INSERT`ステートメントの書き直しは、複数の「値」キーワードの後の値を SQL ステートメント全体に連結することであることに注意してください。 `INSERT`のステートメントに他の違いがある場合は、次のように書き直すことはできません。

```sql
INSERT INTO `t` (`a`) VALUES (10) ON DUPLICATE KEY UPDATE `a` = 10;
INSERT INTO `t` (`a`) VALUES (11) ON DUPLICATE KEY UPDATE `a` = 11;
INSERT INTO `t` (`a`) VALUES (12) ON DUPLICATE KEY UPDATE `a` = 12;
```

上記の`INSERT`ステートメントを 1 つのステートメントに書き換えることはできません。ただし、3 つのステートメントを次のステートメントに変更すると、次のようになります。

```sql
INSERT INTO `t` (`a`) VALUES (10) ON DUPLICATE KEY UPDATE `a` = VALUES(`a`);
INSERT INTO `t` (`a`) VALUES (11) ON DUPLICATE KEY UPDATE `a` = VALUES(`a`);
INSERT INTO `t` (`a`) VALUES (12) ON DUPLICATE KEY UPDATE `a` = VALUES(`a`);
```

次に、書き換え要件を満たします。上記の`INSERT`ステートメントは、次の 1 つのステートメントに書き換えられます。

```sql
INSERT INTO `t` (`a`) VALUES (10), (11), (12) ON DUPLICATE KEY UPDATE a = VALUES(`a`);
```

バッチ更新中に 3 つ以上の更新がある場合、SQL ステートメントは書き換えられ、複数のクエリとして送信されます。これにより、クライアントからサーバーへの要求のオーバーヘッドが効果的に削減されますが、より大きな SQL ステートメントが生成されるという副作用があります。例えば：

```sql
UPDATE `t` SET `a` = 10 WHERE `id` = 1; UPDATE `t` SET `a` = 11 WHERE `id` = 2; UPDATE `t` SET `a` = 12 WHERE `id` = 3;
```

さらに、 [クライアントのバグ](https://bugs.mysql.com/bug.php?id=96623)であるため、バッチ更新中に`rewriteBatchedStatements=true`と`useServerPrepStmts=true`を構成する場合は、このバグを回避するために`allowMultiQueries=true`パラメーターも構成することをお勧めします。

#### パラメータを統合する {#integrate-parameters}

監視を通じて、アプリケーションが TiDB クラスターに対して`INSERT`操作しか実行しないにもかかわらず、冗長な`SELECT`のステートメントが多数あることに気付く場合があります。通常、これは、JDBC が`select @@session.transaction_read_only`の設定をクエリするためにいくつかの SQL ステートメントを送信するために発生します。これらの SQL ステートメントは TiDB には役に立たないため、余分なオーバーヘッドを避けるために`useConfigs=maxPerformance`を構成することをお勧めします。

`useConfigs=maxPerformance`は、構成のグループが含まれます。 MySQL Connector/J 8.0 および MySQL Connector/J 5.1 の詳細な構成を取得するには、それぞれ[mysql-connector-j 8.0](https://github.com/mysql/mysql-connector-j/blob/release/8.0/src/main/resources/com/mysql/cj/configurations/maxPerformance.properties)および[mysql-connector-j 5.1](https://github.com/mysql/mysql-connector-j/blob/release/5.1/src/com/mysql/jdbc/configs/maxPerformance.properties)を参照してください。

構成後、モニタリングを確認して、 `SELECT`ステートメントの数が減少していることを確認できます。

#### タイムアウト関連のパラメーター {#timeout-related-parameters}

TiDB は、タイムアウトを制御する 2 つの MySQL 互換パラメーターを提供します: [`wait_timeout`](/system-variables.md#wait_timeout)と[`max_execution_time`](/system-variables.md#max_execution_time) 。これら 2 つのパラメータは、 Javaアプリケーションとの接続アイドル タイムアウトと、接続での SQL 実行のタイムアウトをそれぞれ制御します。つまり、これらのパラメータは、TiDB とJavaアプリケーション間の接続の最長アイドル時間と最長ビジー時間を制御します。 TiDB v5.4 以降、デフォルト値の`wait_timeout`は`28800`秒、つまり 8 時間です。 v5.4 より前のバージョンの TiDB の場合、デフォルト値は`0`です。これは、タイムアウトが無制限であることを意味します。デフォルト値`max_execution_time`は`0`です。これは、SQL ステートメントの最大実行時間が無制限であることを意味します。

ただし、実際の本番環境では、アイドル接続や実行時間が過度に長い SQL ステートメントは、データベースやアプリケーションに悪影響を及ぼします。アイドル状態の接続と長時間実行される SQL ステートメントを回避するために、アプリケーションの接続文字列でこれら 2 つのパラメーターを構成できます。たとえば、 `sessionVariables=wait_timeout=3600` (1 時間) と`sessionVariables=max_execution_time=300000` (5 分) を設定します。
