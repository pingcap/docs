---
title: Connection Pools and Connection Parameters
summary: このドキュメントでは、TiDB の接続プールとパラメータを構成する方法について説明します。接続プールのサイズ、プローブ構成、最適なスループットを得るための計算式について説明します。また、パフォーマンスを最適化するための JDBC API の使用法と MySQL Connector/J パラメータ構成についても説明します。
---

# 接続プールと接続パラメータ {#connection-pools-and-connection-parameters}

このドキュメントでは、ドライバーまたは ORM フレームワークを使用して TiDB に接続するときに、接続プールと接続パラメータを構成する方法について説明します。

<CustomContent platform="tidb">

Javaアプリケーション開発に関するさらなるヒントにご興味がおありの場合は、 [TiDB を使用したJavaアプリケーション開発のベスト プラクティス](/best-practices/java-app-best-practices.md#connection-pool)ご覧ください。

</CustomContent>

<CustomContent platform="tidb-cloud">

Javaアプリケーション開発に関するさらなるヒントにご興味がおありの場合は、 [TiDB を使用したJavaアプリケーション開発のベスト プラクティス](https://docs.pingcap.com/tidb/stable/java-app-best-practices)ご覧ください。

</CustomContent>

## 接続プール {#connection-pool}

TiDB (MySQL) 接続の構築は比較的コストがかかります (少なくとも OLTP シナリオの場合)。TCP 接続の構築に加えて、接続認証も必要となるためです。そのため、クライアントは通常、再利用のために TiDB (MySQL) 接続を接続プールに保存します。

Java には、 [HikariCP](https://github.com/brettwooldridge/HikariCP) 、 [tomcat-jdbc](https://tomcat.apache.org/tomcat-10.1-doc/jdbc-pool.html) 、 [druid](https://github.com/alibaba/druid) 、 [翻訳:](https://www.mchange.com/projects/c3p0/) 、 [dbcp](https://commons.apache.org/proper/commons-dbcp/)など、多くの接続プール実装があります。TiDB では、使用する接続プールに制限がないため、アプリケーションに応じて好きな接続プールを選択できます。

### 接続数を設定する {#configure-the-number-of-connections}

接続プールのサイズは、アプリケーション自体のニーズに応じて適切に調整されるのが一般的です。HikariCPを例に挙げます。

-   **maximumPoolSize** : 接続プール内の最大接続数。この値が大きすぎると、TiDB は無駄な接続を維持するためにリソースを消費します。この値が小さすぎると、アプリケーションの接続速度が遅くなります。したがって、アプリケーションの特性に応じてこの値を構成する必要があります。詳細については、 [プールのサイズについて](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing)参照してください。
-   **minimumIdle** : 接続プール内のアイドル接続の最小数。主に、アプリケーションがアイドル状態のときに突然の要求に応答するためにいくつかの接続を予約するために使用されます。また、アプリケーションの特性に応じて構成する必要があります。

アプリケーションは、使用を終了した後、接続を返す必要があります。アプリケーションでは、対応する接続プール監視 ( **metricRegistry**など) を使用して、接続プールの問題を適時に特定することをお勧めします。

### プローブ構成 {#probe-configuration}

接続プールは、次のようにクライアントから TiDB への永続的な接続を維持します。

-   v5.4 より前では、TiDB はデフォルトでクライアント接続を積極的に閉じません (エラーが報告されない限り)。
-   v5.4 以降、TiDB はデフォルトで`28800`秒 (つまり`8`時間) 非アクティブになるとクライアント接続を自動的に閉じます。このタイムアウト設定は、TiDB および MySQL 互換の`wait_timeout`変数を使用して制御できます。詳細については、 [JDBC クエリ タイムアウト](/develop/dev-guide-timeouts-in-tidb.md#jdbc-query-timeout)参照してください。

さらに、クライアントと TiDB の間には、 [LVS の](https://en.wikipedia.org/wiki/Linux_Virtual_Server)や[HAプロキシ](https://en.wikipedia.org/wiki/HAProxy)などのネットワーク プロキシが存在する場合があります。これらのプロキシは通常、特定のアイドル期間 (プロキシのアイドル構成によって決定) の経過後に、積極的に接続をクリーンアップします。プロキシのアイドル構成を監視することに加えて、接続プールはキープアライブのために接続を維持またはプローブする必要もあります。

Javaアプリケーションで次のエラーが頻繁に表示される場合:

    The last packet sent successfully to the server was 3600000 milliseconds ago. The driver has not received any packets from the server. com.mysql.jdbc.exceptions.jdbc4.CommunicationsException: Communications link failure

`n milliseconds ago`分の`n`が`0`または非常に小さい値である場合、通常は実行された SQL 操作によって TiDB が異常終了したためです。原因を見つけるには、TiDB の stderr ログを確認することをお勧めします。

`n`非常に大きな値の場合 (上記の例では`3600000`など)、この接続は長時間アイドル状態だった後、プロキシによって閉じられた可能性があります。通常の解決策は、プロキシのアイドル構成の値を増やし、接続プールで次の操作を行うことです。

-   毎回接続を使用する前に、接続が利用可能かどうかを確認してください。
-   別のスレッドを使用して、接続が利用可能かどうかを定期的に確認します。
-   接続を維持するために定期的にテスト クエリを送信します。

異なる接続プールの実装では、上記の方法の 1 つ以上がサポートされる場合があります。対応する構成を見つけるには、接続プールのドキュメントを確認してください。

### 経験に基づいた公式 {#formulas-based-on-experience}

HikariCPの[プールのサイズについて](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing)記事によると、データベース接続プールの適切なサイズを設定する方法がわからない場合は、 [経験に基づく公式](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing#connections--core_count--2--effective_spindle_count)から始めることができます。その後、数式から計算されたプール サイズのパフォーマンス結果に基づいて、サイズをさらに調整して、最高のパフォーマンスを実現できます。

経験に基づいた計算式は次のとおりです。

    connections = ((core_count * 2) + effective_spindle_count)

式内の各パラメータの説明は次のとおりです。

-   **接続**: 取得された接続のサイズ。
-   **core_count** : CPU コアの数。
-   **effective_spindle_count** : ハード ドライブの数 ( [ソリッドステートドライブ](https://en.wikipedia.org/wiki/Solid-state_drive)ではありません)。回転するハード ディスクはそれぞれスピンドルと呼ばれることがあります。たとえば、16 個のディスクの RAID を備えたサーバーを使用している場合、 **effective_spindle_count**は 16 になります。HDD**は**通常、一度に 1 つの要求しか処理できないため、ここでの式は実際にはサーバーが処理できる同時 I/O 要求の数を測定しています。

特に、 [式](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing#the-formula)の下にある以下の注意事項に注意してください。

>     A formula which has held up pretty well across a lot of benchmarks for years is
>     that for optimal throughput the number of active connections should be somewhere
>     near ((core_count * 2) + effective_spindle_count). Core count should not include
>     HT threads, even if hyperthreading is enabled. Effective spindle count is zero if
>     the active data set is fully cached, and approaches the actual number of spindles
>     as the cache hit rate falls. ... There hasn't been any analysis so far regarding
>     how well the formula works with SSDs.

このメモは次のことを示しています:

-   **core_count は**、 [ハイパースレッディング](https://en.wikipedia.org/wiki/Hyper-threading)有効にするかどうかに関係なく、物理コアの数です。
-   データが完全にキャッシュされている場合は、 **effective_spindle_count を**`0`に設定する必要があります。キャッシュのヒット率が低下すると、カウントは実際の数値である`HDD`に近づきます。
-   **この式が*SSD*で機能するかどうかはテストされておらず不明です。**

SSD を使用する場合は、代わりに経験に基づいた次の式を使用することをお勧めします。

    connections = (number of cores * 4)

したがって、SSD の場合は初期接続プールの最大接続サイズを`cores * 4`に設定し、さらにサイズを調整してパフォーマンスを調整することができます。

### チューニング方向 {#tuning-direction}

ご覧のとおり、 [経験に基づいた公式](#formulas-based-on-experience)から計算されたサイズは、推奨される基本値にすぎません。特定のマシンで最適なサイズを取得するには、基本値の近くの他の値を試してパフォーマンスをテストする必要があります。

最適なサイズを見つけるのに役立つ基本的なルールをいくつか紹介します。

-   ネットワークまたはstorageのレイテンシーが高い場合は、最大接続数を増やしてレイテンシーの待機時間を短縮します。レイテンシーによってスレッドがブロックされると、他のスレッドが引き継いで処理を続行できます。
-   サーバーに複数のサービスがデプロイされており、各サービスに個別の接続プールがある場合は、すべての接続プールへの最大接続数の合計を考慮してください。

## 接続パラメータ {#connection-parameters}

Javaアプリケーションは、さまざまなフレームワークでカプセル化されたできます。ほとんどのフレームワークでは、データベースサーバーと対話するために最下層で JDBC API が呼び出されます。JDBC の場合、次の点に重点を置くことをお勧めします。

-   JDBC API の使用選択
-   API実装者のパラメータ設定

### JDBC API {#jdbc-api}

JDBC API の使用方法については、 [JDBC 公式チュートリアル](https://docs.oracle.com/javase/tutorial/jdbc/)参照してください。このセクションでは、いくつかの重要な API の使用方法について説明します。

#### 準備APIを使用する {#use-prepare-api}

OLTP (オンライン トランザクション処理) シナリオの場合、プログラムによってデータベースに送信される SQL ステートメントは、パラメータの変更を削除すると使い果たされる可能性のある複数のタイプです。したがって、通常の[テキストファイルからの実行](https://docs.oracle.com/javase/tutorial/jdbc/basics/processingsqlstatements.html#executing_queries)ではなく[準備された声明](https://docs.oracle.com/javase/tutorial/jdbc/basics/prepared.html)使用し、準備済みステートメントを再利用して直接実行することをお勧めします。これにより、TiDB で SQL 実行プランを繰り返し解析して生成するオーバーヘッドを回避できます。

現在、ほとんどの上位フレームワークはSQL実行にPrepare APIを呼び出します。開発にJDBC APIを直接使用する場合は、Prepare APIを選択するように注意してください。

また、MySQL Connector/J のデフォルト実装では、クライアント側のステートメントのみが前処理され、クライアント側で`?`が置換された後に、ステートメントがテキストファイルでサーバーに送信されます。そのため、Prepare API を使用するだけでなく、TiDBサーバーでステートメントの前処理を行う前に、JDBC 接続パラメータで`useServerPrepStmts = true`も設定する必要があります。詳細なパラメータ設定については、 [MySQL JDBCパラメータ](#mysql-jdbc-parameters)参照してください。

#### バッチAPIを使用する {#use-batch-api}

バッチ挿入の場合は、 [`addBatch` / `executeBatch` API](https://www.tutorialspoint.com/jdbc/jdbc-batch-processing)を使用できます。 `addBatch()`メソッドは、複数の SQL ステートメントを最初にクライアント上でキャッシュし、次に`executeBatch`メソッドを呼び出すときにそれらをまとめてデータベースサーバーに送信するために使用されます。

> **注記：**
>
> デフォルトの MySQL Connector/J 実装では、 `addBatch()`でバッチに追加された SQL ステートメントの送信時刻は`executeBatch()`が呼び出された時刻まで遅延されますが、実際のネットワーク転送中にステートメントは 1 つずつ送信されます。そのため、この方法では通常、通信オーバーヘッドの量は削減されません。
>
> バッチネットワーク転送を行う場合は、JDBC 接続パラメータの`rewriteBatchedStatements = true`設定する必要があります。詳細なパラメータ設定については、 [バッチ関連パラメータ](#batch-related-parameters)参照してください。

#### <code>StreamingResult</code>使用して実行結果を取得します {#use-code-streamingresult-code-to-get-the-execution-result}

ほとんどのシナリオでは、実行効率を向上させるために、JDBC はクエリ結果を事前に取得し、デフォルトでクライアントメモリに保存します。ただし、クエリが非常に大きな結果セットを返す場合、クライアントはデータベースサーバーが一度に返すレコードの数を減らすことを希望し、クライアントのメモリが準備されて次のバッチを要求するまで待機します。

通常、JDBC には 2 種類の処理方法があります。

-   [**FetchSize を**`Integer.MIN_VALUE`に設定する](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-implementation-notes.html#ResultSet) 、クライアントがキャッシュしないようにします。クライアントは、 `StreamingResult`を介してネットワーク接続から実行結果を読み取ります。

    クライアントがストリーミング読み取りメソッドを使用する場合、クエリを実行するためにステートメントを引き続き使用する前に、読み取りを終了するか`resultset`閉じる必要があります。そうしないと、エラー`No statements may be issued when any streaming result sets are open and in use on a given connection. Ensure that you have called .close() on any active streaming result sets before attempting more queries.`が返されます。

    クライアントが読み取りを完了するか`resultset`閉じる前にクエリでこのようなエラーを回避するには、URL に`clobberStreamingResults=true`パラメータを追加します。すると、 `resultset`自動的に閉じられますが、前のストリーミング クエリで読み取られる結果セットは失われます。

-   カーソル フェッチを使用するには、まず正の整数として[`FetchSize`を設定する](http://makejavafaster.blogspot.com/2015/06/jdbc-fetch-size-performance.html)設定し、JDBC URL で`useCursorFetch=true`設定します。

TiDB は両方の方法をサポートしていますが、実装が簡単で実行効率が優れているため、最初の方法を使用することをお勧めします。

### MySQL JDBCパラメータ {#mysql-jdbc-parameters}

JDBC は通常、実装関連の設定を JDBC URL パラメータの形で提供します。このセクションでは[MySQL Connector/J のパラメータ設定](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-configuration-properties.html)紹介します (MariaDB を使用する場合は[MariaDBのパラメータ設定](https://mariadb.com/kb/en/library/about-mariadb-connector-j/#optional-url-parameters)参照してください)。このドキュメントではすべての設定項目を網羅することはできないため、主にパフォーマンスに影響を与える可能性のあるいくつかのパラメータに焦点を当てています。

#### 準備関連のパラメータ {#prepare-related-parameters}

このセクションでは、 `Prepare`に関連するパラメータを紹介します。

-   **サーバー準備ステートメントの使用**

    **useServerPrepStmts は**デフォルトで`false`に設定されています。つまり、Prepare API を使用する場合でも、「準備」操作はクライアントでのみ実行されます。サーバーの解析オーバーヘッドを回避するために、同じ SQL ステートメントで Prepare API を複数回使用する場合は、この構成を`true`に設定することをお勧めします。

    この設定がすでに有効になっていることを確認するには、次の操作を実行します。

    -   TiDB 監視ダッシュボードに移動し、**クエリ サマリー**&gt;**インスタンス別の CPS を通じて**要求コマンド タイプを表示します。
    -   リクエスト内の`COM_QUERY` `COM_STMT_EXECUTE`または`COM_STMT_PREPARE`に置き換えられた場合、この設定はすでに有効になっていることを意味します。

-   **キャッシュ準備ステートメント**

    `useServerPrepStmts=true`ではサーバーがPrepared Statements を実行できますが、デフォルトでは、クライアントは実行ごとに Prepared Statements を閉じて再利用しません。つまり、「準備」操作はテキスト ファイルの実行ほど効率的ではありません。これを解決するには、 `useServerPrepStmts=true`設定した後、 `cachePrepStmts=true`も構成することをお勧めします。これにより、クライアントは Prepared Statements をキャッシュできます。

    この設定がすでに有効になっていることを確認するには、次の操作を実行します。

    -   TiDB 監視ダッシュボードに移動し、**クエリ サマリー**&gt;**インスタンス別の CPS を通じて**要求コマンド タイプを表示します。
    -   リクエスト内の`COM_STMT_EXECUTE`の数が`COM_STMT_PREPARE`の数よりはるかに多い場合、この設定はすでに有効になっていることを意味します。

    また、 `useConfigs=maxPerformance`設定すると、 `cachePrepStmts=true`含む複数のパラメータが同時に設定されます。

-   **準備StmtCacheSqlLimit**

    `cachePrepStmts`設定した後は、 `prepStmtCacheSqlLimit`設定にも注意してください (デフォルト値は`256`です)。この設定は、クライアントにキャッシュされる Prepared Statements の最大長を制御します。

    この最大長を超える準備済みステートメントはキャッシュされないため、再利用できません。この場合、アプリケーションの実際の SQL の長さに応じて、この構成の値を増やすことを検討してください。

    次の場合には、この設定が小さすぎないかどうかを確認する必要があります。

    -   TiDB 監視ダッシュボードに移動し、**クエリ サマリー**&gt;**インスタンス別の CPS を通じて**要求コマンド タイプを表示します。
    -   そして、 `cachePrepStmts=true`設定されていることがわかりますが、 `COM_STMT_PREPARE`まだ`COM_STMT_EXECUTE`とほぼ同じであり、 `COM_STMT_CLOSE`存在します。

-   **準備StmtCacheSize**

    **prepStmtCacheSize は、**キャッシュされた Prepared Statements の数を制御します (デフォルト値は`25`です)。アプリケーションで多くの種類の SQL ステートメントを「準備」する必要があり、Prepared Statements を再利用したい場合は、この値を増やすことができます。

    この設定がすでに有効になっていることを確認するには、次の操作を実行します。

    -   TiDB 監視ダッシュボードに移動し、**クエリ サマリー**&gt;**インスタンス別の CPS を通じて**要求コマンド タイプを表示します。
    -   リクエスト内の`COM_STMT_EXECUTE`の数が`COM_STMT_PREPARE`の数よりはるかに多い場合、この設定はすでに有効になっていることを意味します。

#### バッチ関連パラメータ {#batch-related-parameters}

バッチ書き込みを処理する場合は、 `rewriteBatchedStatements=true`設定することをお勧めします。 `addBatch()`または`executeBatch()`使用した後でも、JDBC はデフォルトで SQL を 1 つずつ送信します。次に例を示します。

```java
pstmt = prepare("INSERT INTO `t` (a) values(?)");
pstmt.setInt(1, 10);
pstmt.addBatch();
pstmt.setInt(1, 11);
pstmt.addBatch();
pstmt.setInt(1, 12);
pstmt.executeBatch();
```

`Batch`方法が使用されていますが、TiDB に送信される SQL ステートメントは、個別の`INSERT`のステートメントのままです。

```sql
INSERT INTO `t` (`a`) VALUES(10);
INSERT INTO `t` (`a`) VALUES(11);
INSERT INTO `t` (`a`) VALUES(12);
```

ただし、 `rewriteBatchedStatements=true`設定すると、TiDB に送信される SQL ステートメントは単一の`INSERT`ステートメントになります。

```sql
INSERT INTO `t` (`a`) values(10),(11),(12);
```

`INSERT`ステートメントの書き換えは、複数の「values」キーワードの後の値を 1 つの SQL ステートメント全体に連結することであることに注意してください。3 `INSERT`ステートメントに他の違いがある場合は、次のように書き換えることはできません。

```sql
INSERT INTO `t` (`a`) VALUES (10) ON DUPLICATE KEY UPDATE `a` = 10;
INSERT INTO `t` (`a`) VALUES (11) ON DUPLICATE KEY UPDATE `a` = 11;
INSERT INTO `t` (`a`) VALUES (12) ON DUPLICATE KEY UPDATE `a` = 12;
```

上記の`INSERT`文を 1 つの文に書き直すことはできません。ただし、3 つの文を次のように変更すると、

```sql
INSERT INTO `t` (`a`) VALUES (10) ON DUPLICATE KEY UPDATE `a` = VALUES(`a`);
INSERT INTO `t` (`a`) VALUES (11) ON DUPLICATE KEY UPDATE `a` = VALUES(`a`);
INSERT INTO `t` (`a`) VALUES (12) ON DUPLICATE KEY UPDATE `a` = VALUES(`a`);
```

すると、書き換え要件が満たされます。上記の`INSERT`ステートメントは、次の 1 つのステートメントに書き換えられます。

```sql
INSERT INTO `t` (`a`) VALUES (10), (11), (12) ON DUPLICATE KEY UPDATE a = VALUES(`a`);
```

バッチ更新中に 3 つ以上の更新が行われる場合、SQL ステートメントは書き換えられ、複数のクエリとして送信されます。これにより、クライアントからサーバーへの要求のオーバーヘッドが効果的に削減されますが、副作用として、より大きな SQL ステートメントが生成されます。例:

```sql
UPDATE `t` SET `a` = 10 WHERE `id` = 1; UPDATE `t` SET `a` = 11 WHERE `id` = 2; UPDATE `t` SET `a` = 12 WHERE `id` = 3;
```

また、 [クライアントのバグ](https://bugs.mysql.com/bug.php?id=96623)のため、バッチ更新中に`rewriteBatchedStatements=true`と`useServerPrepStmts=true`を設定する場合は、このバグを回避するために`allowMultiQueries=true`パラメータも設定することをお勧めします。

#### パラメータを統合する {#integrate-parameters}

監視を通じて、アプリケーションが TiDB クラスターに対して`INSERT`操作のみを実行しているにもかかわらず、冗長な`SELECT`ステートメントが多数あることに気付く場合があります。通常、これは、JDBC が設定を照会するためにいくつかの SQL ステートメント (例: `select @@session.transaction_read_only`を送信するために発生します。これらの SQL ステートメントは TiDB には役に立たないため、余分なオーバーヘッドを回避するために`useConfigs=maxPerformance`を構成することをお勧めします。

`useConfigs=maxPerformance` 、一連の構成が含まれています。MySQL Connector/J 8.0 および MySQL Connector/J 5.1 の詳細な構成については、それぞれ[mysql-コネクタ-j 8.0](https://github.com/mysql/mysql-connector-j/blob/release/8.0/src/main/resources/com/mysql/cj/configurations/maxPerformance.properties)と[mysql-コネクタ-j 5.1](https://github.com/mysql/mysql-connector-j/blob/release/5.1/src/com/mysql/jdbc/configs/maxPerformance.properties)参照してください。

設定後、監視をチェックして、 `SELECT`ステートメントの数が減っていることを確認できます。

#### タイムアウト関連のパラメータ {#timeout-related-parameters}

TiDB は、タイムアウトを制御するために、MySQL 互換のパラメータ[`wait_timeout`](/system-variables.md#wait_timeout)と[`max_execution_time`](/system-variables.md#max_execution_time) 2 つ提供しています。これら 2 つのパラメータは、それぞれJavaアプリケーションとの接続アイドル タイムアウトと、接続中の SQL 実行のタイムアウトを制御します。つまり、これらのパラメータは、TiDB とJavaアプリケーション間の接続の最長アイドル時間と最長ビジー時間を制御します。TiDB v5.4 以降、デフォルト値`wait_timeout`は`28800`秒、つまり 8 時間です。v5.4 より前のバージョンの TiDB の場合、デフォルト値は`0`で、タイムアウトは無制限であることを意味します。デフォルト値`max_execution_time`は`0`で、SQL ステートメントの最大実行時間は無制限であることを意味します。

デフォルト値の[`wait_timeout`](/system-variables.md#wait_timeout)は比較的大きい値です。トランザクションが開始されてもコミットもロールバックもされないシナリオでは、ロックの保持が長引かないように、よりきめ細かい制御と短いタイムアウトが必要になる場合があります。この場合、 [`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760) (TiDB v7.6.0 で導入) を使用して、ユーザー セッションのトランザクションのアイドル タイムアウトを制御できます。

ただし、実際の本番環境では、アイドル接続や実行時間が長すぎる SQL ステートメントは、データベースやアプリケーションに悪影響を及ぼします。アイドル接続や実行時間が長すぎる SQL ステートメントを回避するには、アプリケーションの接続文字列でこれらの 2 つのパラメータを設定します。たとえば、 `sessionVariables=wait_timeout=3600` (1 時間) と`sessionVariables=max_execution_time=300000` (5 分) を設定します。

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[TiDB コミュニティ](https://ask.pingcap.com/) 、または[サポートチケットを作成する](/support.md)について質問します。

</CustomContent>

<CustomContent platform="tidb-cloud">

[TiDB コミュニティ](https://ask.pingcap.com/) 、または[サポートチケットを作成する](https://support.pingcap.com/)について質問します。

</CustomContent>
