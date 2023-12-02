---
title: Connection Pools and Connection Parameters
---

# 接続プールと接続パラメータ {#connection-pools-and-connection-parameters}

このドキュメントでは、ドライバーまたは ORM フレームワークを使用して TiDB に接続するときに、接続プールと接続パラメーターを構成する方法について説明します。

<CustomContent platform="tidb">

Javaアプリケーション開発に関するその他のヒントに興味がある場合は、 [TiDB を使用したJavaアプリケーション開発のベスト プラクティス](/best-practices/java-app-best-practices.md#connection-pool)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

Javaアプリケーション開発に関するその他のヒントに興味がある場合は、 [TiDB を使用したJavaアプリケーション開発のベスト プラクティス](https://docs.pingcap.com/tidb/stable/java-app-best-practices)を参照してください。

</CustomContent>

## 接続プール {#connection-pool}

TiDB (MySQL) 接続の構築は (少なくとも OLTP シナリオでは) 比較的高価です。 TCP 接続の構築に加えて、接続認証も必要となるためです。したがって、クライアントは通常、TiDB (MySQL) 接続を接続プールに保存して再利用します。

Java には、 [HikariCP](https://github.com/brettwooldridge/HikariCP) 、 [tomcat-jdbc](https://tomcat.apache.org/tomcat-10.1-doc/jdbc-pool.html) 、 [druid](https://github.com/alibaba/druid) 、 [c3p0](https://www.mchange.com/projects/c3p0/) 、 [dbcp](https://commons.apache.org/proper/commons-dbcp/)などの多くの接続プール実装があります。 TiDB は使用する接続プールを制限しないため、アプリケーションに合わせて好きなものを選択できます。

### 接続数を構成する {#configure-the-number-of-connections}

接続プールのサイズは、アプリケーション独自のニーズに応じて適切に調整されるのが一般的です。例として、 HikariCP を取り上げます。

-   **minimumPoolSize** : 接続プール内の接続の最大数。この値が大きすぎる場合、TiDB は無駄な接続を維持するためにリソースを消費します。この値が小さすぎると、アプリケーションの接続が遅くなります。したがって、アプリケーションの特性に応じてこの値を設定する必要があります。詳細は[プールのサイジングについて](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing)を参照してください。
-   **minimumIdle** : 接続プール内のアイドル状態の接続の最小数。これは主に、アプリケーションがアイドル状態のときに突然のリクエストに応答するためにいくつかの接続を予約するために使用されます。アプリケーションの特性に応じて構成する必要もあります。

アプリケーションは、使用を終了した後に接続を返す必要があります。アプリケーションでは、対応する接続​​プール監視 ( **metricRegistry**など) を使用して、接続プールの問題を適時に特定することをお勧めします。

### プローブの構成 {#probe-configuration}

接続プールは、TiDB への永続的な接続を維持します。 TiDB は、デフォルトでは (エラーが報告されない限り) クライアント接続を積極的に閉じませんが、通常、クライアントと TiDB の間には[LVS](https://en.wikipedia.org/wiki/Linux_Virtual_Server)や[HAプロキシ](https://en.wikipedia.org/wiki/HAProxy)などのネットワーク プロキシもあります。通常、これらのプロキシは、一定期間アイドル状態の接続を積極的にクリーンアップします。プロキシのアイドル構成に注意を払うことに加えて、接続プールは接続を維持するか、接続をプローブする必要もあります。

Javaアプリケーションで次のエラーが頻繁に表示される場合:

    The last packet sent successfully to the server was 3600000 milliseconds ago. The driver has not received any packets from the server. com.mysql.jdbc.exceptions.jdbc4.CommunicationsException: Communications link failure

`n milliseconds ago`の`n`が`0`または非常に小さい値の場合、通常は、実行された SQL 操作によって TiDB が異常終了することが原因です。原因を見つけるには、TiDB stderr ログを確認することをお勧めします。

`n`が非常に大きな値 (上記の例の`3600000`など) の場合、この接続は長時間アイドル状態であり、その後プロキシによって閉じられた可能性があります。通常の解決策は、プロキシのアイドル構成の値を増やし、接続プールが次のことを行えるようにすることです。

-   接続を使用する前に、毎回接続が利用可能かどうかを確認してください。
-   別のスレッドを使用して接続が利用可能かどうかを定期的に確認してください。
-   テスト クエリを定期的に送信して、接続を維持します。

接続プールの実装が異なれば、上記の方法の 1 つ以上がサポートされる場合があります。接続プールのドキュメントを確認して、対応する構成を見つけることができます。

### 経験に基づいた公式 {#formulas-based-on-experience}

HikariCPの[プールのサイジングについて](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing)記事によると、データベース接続プールの適切なサイズを設定する方法がわからない場合は、 [経験に基づいた公式](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing#connections--core_count--2--effective_spindle_count)から始めることができます。次に、式から計算されたプール サイズのパフォーマンス結果に基づいて、最適なパフォーマンスが得られるようにサイズをさらに調整できます。

経験に基づいた式は次のとおりです。

    connections = ((core_count * 2) + effective_spindle_count)

式の各パラメータの説明は次のとおりです。

-   **connection** : 取得された接続のサイズ。
-   **core_count** : CPU コアの数。
-   **有効なスピンドルカウント**: ハードドライブの数 ( [SSD](https://en.wikipedia.org/wiki/Solid-state_drive)ではありません)。回転する各ハードディスクをスピンドルと呼ぶことができるためです。たとえば、16 ディスクの RAID を持つサーバーを使用している場合、 **effective_spindle_count**は 16 である必要があります。通常、 **HDD は**一度に 1 つのリクエストしか処理できないため、ここでの式は実際にサーバーが同時に処理できる I/O リクエストの数を測定します。管理。

特に、 [式](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing#the-formula)の下の注記に注意してください。

>     A formula which has held up pretty well across a lot of benchmarks for years is
>     that for optimal throughput the number of active connections should be somewhere
>     near ((core_count * 2) + effective_spindle_count). Core count should not include
>     HT threads, even if hyperthreading is enabled. Effective spindle count is zero if
>     the active data set is fully cached, and approaches the actual number of spindles
>     as the cache hit rate falls. ... There hasn't been any analysis so far regarding
>     how well the formula works with SSDs.

このメモは次のことを示しています。

-   **core_count は**、 [ハイパースレッディング](https://en.wikipedia.org/wiki/Hyper-threading)有効にするかどうかに関係なく、物理コアの数です。
-   データが完全にキャッシュされたら、 **effective_spindle_count**を`0`に設定する必要があります。キャッシュのヒット率が低下するにつれて、カウントは実際の数`HDD`に近づきます。
-   **この公式が*SSD*で機能するかどうかはテストされておらず、不明です。**

SSD を使用する場合は、経験に基づいて代わりに次の公式を使用することをお勧めします。

    connections = (number of cores * 4)

したがって、SSD の場合は初期接続プールの最大接続サイズを`cores * 4`に設定し、さらにサイズを調整してパフォーマンスを調整できます。

### チューニング方向 {#tuning-direction}

ご覧のとおり、 [経験に基づいた公式](#formulas-based-on-experience)から計算されたサイズは推奨される基本値にすぎません。特定のマシンで最適なサイズを取得するには、基本値に近い他の値を試してパフォーマンスをテストする必要があります。

最適なサイズを取得するための基本的なルールをいくつか示します。

-   ネットワークまたはstorageのレイテンシーが長い場合は、最大接続数を増やしてレイテンシーを短縮します。スレッドがレイテンシーによってブロックされると、他のスレッドが引き継いで処理を続行できます。
-   サーバー上に複数のサービスがデプロイされており、各サービスに個別の接続プールがある場合は、すべての接続プールへの最大接続数の合計を考慮してください。

## 接続パラメータ {#connection-parameters}

Javaアプリケーションは、さまざまなフレームワークを使用してカプセル化されたできます。ほとんどのフレームワークでは、JDBC API はデータベースサーバーと対話するために最下位レベルで呼び出されます。 JDBC の場合は、次のことに重点を置くことをお勧めします。

-   JDBC API の使用法の選択
-   API実装者のパラメータ設定

### JDBC API {#jdbc-api}

JDBC API の使用法については、 [JDBC公式チュートリアル](https://docs.oracle.com/javase/tutorial/jdbc/)を参照してください。このセクションでは、いくつかの重要な API の使用法について説明します。

#### 準備APIを使用する {#use-prepare-api}

OLTP (オンライン トランザクション処理) シナリオの場合、プログラムによってデータベースに送信される SQL ステートメントは、パラメーターの変更を削除した後に枯渇する可能性があるいくつかのタイプです。したがって、通常の[テキストファイルからの実行](https://docs.oracle.com/javase/tutorial/jdbc/basics/processingsqlstatements.html#executing_queries)の代わりに[準備されたステートメント](https://docs.oracle.com/javase/tutorial/jdbc/basics/prepared.html)使用し、Prepared Statement を再利用して直接実行することをお勧めします。これにより、TiDB で SQL 実行プランを繰り返し解析して生成するオーバーヘッドが回避されます。

現在、ほとんどの上位レベルのフレームワークは、SQL 実行のために Prepare API を呼び出します。 JDBC API を開発に直接使用する場合は、Prepare API の選択に注意してください。

さらに、MySQL Connector/J のデフォルト実装では、クライアント側のステートメントのみが前処理され、クライアント上で`?`置き換えられた後、ステートメントはテキスト ファイルでサーバーに送信されます。したがって、Prepare API の使用に加えて、TiDBサーバーでステートメントの前処理を実行する前に、JDBC 接続パラメータで`useServerPrepStmts = true`を設定する必要もあります。詳細なパラメータ設定については、 [MySQL JDBC パラメータ](#mysql-jdbc-parameters)を参照してください。

#### バッチAPIを使用する {#use-batch-api}

バッチ挿入の場合は、 [`addBatch` / `executeBatch` API](https://www.tutorialspoint.com/jdbc/jdbc-batch-processing)を使用できます。 `addBatch()`メソッドは、最初にクライアント上で複数の SQL ステートメントをキャッシュし、 `executeBatch`メソッドを呼び出すときにそれらをまとめてデータベースサーバーに送信するために使用されます。

> **注記：**
>
> デフォルトの MySQL Connector/J 実装では、 `addBatch()`でバッチに追加された SQL ステートメントの送信時刻が`executeBatch()`呼び出される時刻まで遅延しますが、実際のネットワーク転送中にステートメントは 1 つずつ送信されます。したがって、この方法では通常、通信オーバーヘッドの量は削減されません。
>
> ネットワーク転送を一括して行う場合は、JDBC 接続パラメータに`rewriteBatchedStatements = true`を設定する必要があります。詳細なパラメータ設定については、 [バッチ関連パラメータ](#batch-related-parameters)を参照してください。

#### <code>StreamingResult</code>使用して実行結果を取得します {#use-code-streamingresult-code-to-get-the-execution-result}

ほとんどのシナリオでは、実行効率を向上させるために、JDBC はクエリ結果を事前に取得し、デフォルトでクライアントメモリに保存します。しかし、クエリが非常に大きな結果セットを返す場合、クライアントは多くの場合、データベースサーバー一度に返されるレコードの数を減らし、クライアントのメモリの準備ができて次のバッチを要求するまで待機します。

通常、JDBC には次の 2 種類の処理方法があります。

-   [**FetchSize を**`Integer.MIN_VALUE`に設定します](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-implementation-notes.html#ResultSet)を指定すると、クライアントはキャッシュを行わなくなります。クライアントは`StreamingResult`を介してネットワーク接続から実行結果を読み取ります。

    クライアントがストリーミング読み取りメソッドを使用する場合、ステートメントを使用してクエリを作成し続ける前に、読み取りを完了するかクローズ`resultset`する必要があります。それ以外の場合は、エラー`No statements may be issued when any streaming result sets are open and in use on a given connection. Ensure that you have called .close() on any active streaming result sets before attempting more queries.`が返されます。

    クライアントが読み取りを完了するか、 `resultset`閉じる前にクエリでこのようなエラーが発生するのを回避するには、URL に`clobberStreamingResults=true`パラメータを追加します。その後、 `resultset`は自動的に閉じられますが、前のストリーミング クエリで読み取られる結果セットは失われます。

-   カーソルフェッチを使用するには、まず正の整数として[`FetchSize`を設定する](http://makejavafaster.blogspot.com/2015/06/jdbc-fetch-size-performance.html)を設定し、JDBC URL で`useCursorFetch=true`を設定します。

TiDB は両方の方法をサポートしていますが、最初の方法を使用することをお勧めします。これは、実装が単純で実行効率が高いためです。

### MySQL JDBC パラメータ {#mysql-jdbc-parameters}

JDBC は通常、実装関連の設定を JDBC URL パラメータの形式で提供します。このセクションでは[MySQL Connector/J のパラメータ設定](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-configuration-properties.html)を紹介します (MariaDB を使用する場合は[MariaDBのパラメータ設定](https://mariadb.com/kb/en/library/about-mariadb-connector-j/#optional-url-parameters)を参照してください)。このドキュメントではすべての構成項目をカバーすることはできないため、パフォーマンスに影響を与える可能性のあるいくつかのパラメーターに主に焦点を当てています。

#### 関連パラメータの準備 {#prepare-related-parameters}

このセクションでは、 `Prepare`に関連するパラメータを紹介します。

-   **useServerPrepStmts**

    **useServerPrepStmts は**デフォルトで`false`に設定されています。つまり、Prepare API を使用する場合でも、「準備」操作はクライアント上でのみ実行されます。同じ SQL ステートメントで Prepare API を複数回使用する場合、サーバーの解析オーバーヘッドを回避するには、この構成を`true`に設定することをお勧めします。

    この設定がすでに有効になっていることを確認するには、次の操作を実行できます。

    -   TiDB モニタリング ダッシュボードに移動し、 **[Query Summary]** &gt; **[CPS By Instance]**からリクエスト コマンド タイプを表示します。
    -   リクエスト内で`COM_QUERY` `COM_STMT_EXECUTE`または`COM_STMT_PREPARE`に置き換えられている場合は、この設定がすでに有効になっていることを意味します。

-   **キャッシュPrepStmts**

    `useServerPrepStmts=true`を指定すると、サーバーはプリペアド ステートメントを実行できますが、デフォルトでは、クライアントは各実行後にプリペアド ステートメントを閉じ、再利用しません。これは、「準備」操作がテキスト ファイルの実行ほど効率的ではないことを意味します。これを解決するには、 `useServerPrepStmts=true`設定した後、 `cachePrepStmts=true`も設定することをお勧めします。これにより、クライアントは Prepared Statement をキャッシュできるようになります。

    この設定がすでに有効になっていることを確認するには、次の操作を実行できます。

    -   TiDB モニタリング ダッシュボードに移動し、 **[Query Summary]** &gt; **[CPS By Instance]**からリクエスト コマンド タイプを表示します。
    -   リクエスト内の`COM_STMT_EXECUTE`の数が`COM_STMT_PREPARE`の数よりはるかに多い場合、この設定はすでに有効になっていることを意味します。

    さらに、 `useConfigs=maxPerformance`を設定すると、 `cachePrepStmts=true`を含む複数のパラメータが同時に設定されます。

-   **prepStmtCacheSqlLimit**

    `cachePrepStmts`を設定した後、 `prepStmtCacheSqlLimit`設定にも注意してください (デフォルト値は`256` )。この構成は、クライアントにキャッシュされるプリペアド ステートメントの最大長を制御します。

    この最大長を超えるプリペアド ステートメントはキャッシュされないため、再利用できません。この場合、アプリケーションの実際の SQL 長に応じて、この構成の値を増やすことを検討できます。

    次の場合は、この設定が小さすぎるかどうかを確認する必要があります。

    -   TiDB モニタリング ダッシュボードに移動し、 **[Query Summary]** &gt; **[CPS By Instance]**からリクエスト コマンド タイプを表示します。
    -   そして`cachePrepStmts=true`設定されていますが、 `COM_STMT_PREPARE`は依然として`COM_STMT_EXECUTE`とほぼ同じであり、 `COM_STMT_CLOSE`存在することがわかります。

-   **prepStmtCacheSize**

    **prepStmtCacheSize は、**キャッシュされる Prepared Statement の数を制御します (デフォルト値は`25` )。アプリケーションで多くの種類の SQL ステートメントを「準備」する必要があり、準備されたステートメントを再利用したい場合は、この値を増やすことができます。

    この設定がすでに有効になっていることを確認するには、次の操作を実行できます。

    -   TiDB モニタリング ダッシュボードに移動し、 **[Query Summary]** &gt; **[CPS By Instance]**からリクエスト コマンド タイプを表示します。
    -   リクエスト内の`COM_STMT_EXECUTE`の数が`COM_STMT_PREPARE`の数よりはるかに多い場合、この設定はすでに有効になっていることを意味します。

#### バッチ関連パラメータ {#batch-related-parameters}

バッチ書き込みの処理中は、 `rewriteBatchedStatements=true`を構成することをお勧めします。 `addBatch()`または`executeBatch()`使用した後も、JDBC はデフォルトで SQL を 1 つずつ送信します。次に例を示します。

```java
pstmt = prepare("INSERT INTO `t` (a) values(?)");
pstmt.setInt(1, 10);
pstmt.addBatch();
pstmt.setInt(1, 11);
pstmt.addBatch();
pstmt.setInt(1, 12);
pstmt.executeBatch();
```

`Batch`メソッドが使用されていますが、TiDB に送信される SQL ステートメントは依然として個別の`INSERT`のステートメントです。

```sql
INSERT INTO `t` (`a`) VALUES(10);
INSERT INTO `t` (`a`) VALUES(11);
INSERT INTO `t` (`a`) VALUES(12);
```

ただし、 `rewriteBatchedStatements=true`を設定すると、TiDB に送信される SQL ステートメントは単一の`INSERT`ステートメントになります。

```sql
INSERT INTO `t` (`a`) values(10),(11),(12);
```

`INSERT`ステートメントの書き換えでは、複数の「values」キーワードの後の値が SQL ステートメント全体に連結されることに注意してください。 `INSERT`のステートメントに他の相違点がある場合、次のように書き直すことはできません。

```sql
INSERT INTO `t` (`a`) VALUES (10) ON DUPLICATE KEY UPDATE `a` = 10;
INSERT INTO `t` (`a`) VALUES (11) ON DUPLICATE KEY UPDATE `a` = 11;
INSERT INTO `t` (`a`) VALUES (12) ON DUPLICATE KEY UPDATE `a` = 12;
```

上記`INSERT`ステートメントを 1 つのステートメントに書き換えることはできません。しかし、3 つのステートメントを次のステートメントに変更すると、次のようになります。

```sql
INSERT INTO `t` (`a`) VALUES (10) ON DUPLICATE KEY UPDATE `a` = VALUES(`a`);
INSERT INTO `t` (`a`) VALUES (11) ON DUPLICATE KEY UPDATE `a` = VALUES(`a`);
INSERT INTO `t` (`a`) VALUES (12) ON DUPLICATE KEY UPDATE `a` = VALUES(`a`);
```

その後、書き換え要件を満たします。上記の`INSERT`ステートメントは、次の 1 つのステートメントに書き換えられます。

```sql
INSERT INTO `t` (`a`) VALUES (10), (11), (12) ON DUPLICATE KEY UPDATE a = VALUES(`a`);
```

バッチ更新中に 3 つ以上の更新があった場合、SQL ステートメントが書き換えられ、複数のクエリとして送信されます。これにより、クライアントからサーバーへのリクエストのオーバーヘッドが効果的に削減されますが、副作用として、生成される SQL ステートメントが大きくなります。例えば：

```sql
UPDATE `t` SET `a` = 10 WHERE `id` = 1; UPDATE `t` SET `a` = 11 WHERE `id` = 2; UPDATE `t` SET `a` = 12 WHERE `id` = 3;
```

さらに、 [クライアントのバグ](https://bugs.mysql.com/bug.php?id=96623)があるため、バッチ更新中に`rewriteBatchedStatements=true`と`useServerPrepStmts=true`を設定する場合は、このバグを回避するために`allowMultiQueries=true`パラメータも設定することをお勧めします。

#### パラメータを統合する {#integrate-parameters}

モニタリングを通じて、アプリケーションは TiDB クラスターに対して`INSERT`操作のみを実行しますが、冗長な`SELECT`のステートメントが多数あることに気づくかもしれません。通常、これは、JDBC が設定をクエリするためにいくつかの SQL ステートメント (例: `select @@session.transaction_read_only`を送信するために発生します。これらの SQL ステートメントは TiDB では役に立たないため、余分なオーバーヘッドを避けるために`useConfigs=maxPerformance`を構成することをお勧めします。

`useConfigs=maxPerformance`には構成のグループが含まれます。 MySQL Connector/J 8.0 の詳細な設定と MySQL Connector/J 5.1 の詳細な設定を取得するには、それぞれ[mysql-コネクタ-j 8.0](https://github.com/mysql/mysql-connector-j/blob/release/8.0/src/main/resources/com/mysql/cj/configurations/maxPerformance.properties)と[mysql-コネクタ-j 5.1](https://github.com/mysql/mysql-connector-j/blob/release/5.1/src/com/mysql/jdbc/configs/maxPerformance.properties)を参照してください。

構成後、モニタリングをチェックして、 `SELECT`ステートメントの数が減少していることを確認できます。

#### タイムアウト関連のパラメータ {#timeout-related-parameters}

TiDB には、タイムアウトを制御するための 2 つの MySQL 互換パラメータ[`wait_timeout`](/system-variables.md#wait_timeout)と[`max_execution_time`](/system-variables.md#max_execution_time)が用意されています。これら 2 つのパラメータは、それぞれJavaアプリケーションとの接続アイドル タイムアウトと接続での SQL 実行のタイムアウトを制御します。つまり、これらのパラメータは、TiDB とJavaアプリケーション間の接続の最長アイドル時間と最長ビジー時間を制御します。 TiDB v5.4 以降、デフォルト値の`wait_timeout`は`28800`秒、つまり 8 時間です。 v5.4 より前の TiDB バージョンの場合、デフォルト値は`0`で、タイムアウトが無制限であることを意味します。デフォルト値`max_execution_time`は`0`で、これは SQL ステートメントの最大実行時間が無制限であることを意味します。

ただし、実際の本番環境では、アイドル状態の接続や実行時間が長すぎる SQL ステートメントはデータベースやアプリケーションに悪影響を及ぼします。アイドル状態の接続や長時間実行される SQL ステートメントを回避するために、アプリケーションの接続文字列でこれら 2 つのパラメーターを構成できます。たとえば、 `sessionVariables=wait_timeout=3600` （1時間）と`sessionVariables=max_execution_time=300000` （5分）を設定します。
