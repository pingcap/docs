---
title: Best Practices for Developing Java Applications with TiDB
summary: このドキュメントでは、データベース関連のコンポーネント、JDBC の使用、接続プールの構成、データ アクセス フレームワーク、Spring トランザクション 、トラブルシューティング ツールなど、TiDB を使用してJavaアプリケーションを開発するためのベスト プラクティスを紹介します。TiDB は MySQL と高い互換性があるため、MySQL ベースのJavaアプリケーションのベスト プラクティスのほとんどは TiDB にも適用されます。
---

# TiDB を使用したJavaアプリケーション開発のベスト プラクティス {#best-practices-for-developing-java-applications-with-tidb}

このドキュメントでは、TiDB をより有効に活用するためのJavaアプリケーション開発のベスト プラクティスを紹介します。バックエンドの TiDB データベースと対話する一般的なJavaアプリケーション コンポーネントに基づいて、開発中によく発生する問題の解決策も提供します。

## Javaアプリケーションのデータベース関連コンポーネント {#database-related-components-in-java-applications}

Javaアプリケーションで TiDB データベースと対話する一般的なコンポーネントは次のとおりです。

-   ネットワーク プロトコル: クライアントは標準[MySQL プロトコル](https://dev.mysql.com/doc/dev/mysql-server/latest/PAGE_PROTOCOL.html)を介して TiDBサーバーと対話します。
-   JDBC API と JDBC ドライバー: Javaアプリケーションは通常、標準の[JDBC (Javaデータベース接続)](https://docs.oracle.com/javase/8/docs/technotes/guides/jdbc/) API を使用してデータベースにアクセスします。TiDB に接続するには、JDBC API を介して MySQL プロトコルを実装する JDBC ドライバーを使用できます。MySQL 用の一般的な JDBC ドライバーには、 [MySQL コネクタ/J](https://github.com/mysql/mysql-connector-j)と[MariaDB コネクタ/J](https://mariadb.com/kb/en/library/about-mariadb-connector-j/#about-mariadb-connectorj)あります。
-   データベース接続プール: 要求されるたびに接続を作成するオーバーヘッドを削減するために、アプリケーションは通常、接続プールを使用して接続をキャッシュし、再利用します。JDBC [情報元](https://docs.oracle.com/javase/8/docs/api/javax/sql/DataSource.html)では、接続プール API が定義されています。必要に応じて、さまざまなオープン ソース接続プール実装から選択できます。
-   データ アクセス フレームワーク: アプリケーションは通常、 [マイバティス](https://mybatis.org/mybatis-3/index.html)や[休止状態](https://hibernate.org/)などのデータ アクセス フレームワークを使用して、データベース アクセス操作をさらに簡素化および管理します。
-   アプリケーション実装: アプリケーション ロジックは、データベースにどのコマンドをいつ送信するかを制御します。一部のアプリケーションでは、 [春のトランザクション](https://docs.spring.io/spring/docs/4.2.x/spring-framework-reference/html/transaction.html)側面を使用してトランザクションの開始およびコミット ロジックを管理します。

![Java application components](/media/best-practices/java-practice-1.png)

上の図から、 Javaアプリケーションが次のことを実行する可能性があることがわかります。

-   TiDB と対話するには、JDBC API 経由で MySQL プロトコルを実装します。
-   接続プールから永続的な接続を取得します。
-   MyBatis などのデータ アクセス フレームワークを使用して、SQL ステートメントを生成および実行します。
-   Spring トランザクション を使用して、トランザクションを自動的に開始または停止します。

このドキュメントの残りの部分では、上記のコンポーネントを使用してJavaアプリケーションを開発するときに発生する問題とその解決策について説明します。

## ODBC ドライバ {#jdbc}

Javaアプリケーションは、さまざまなフレームワークでカプセル化されたできます。ほとんどのフレームワークでは、データベースサーバーと対話するために最下層で JDBC API が呼び出されます。JDBC の場合、次の点に重点を置くことをお勧めします。

-   JDBC API の使用選択
-   API実装者のパラメータ設定

### JDBC API {#jdbc-api}

JDBC API の使用方法については、 [JDBC 公式チュートリアル](https://docs.oracle.com/javase/tutorial/jdbc/)参照してください。このセクションでは、いくつかの重要な API の使用方法について説明します。

#### 準備APIを使用する {#use-prepare-api}

OLTP (オンライン トランザクション処理) シナリオの場合、プログラムからデータベースに送信される SQL ステートメントは、パラメータの変更を削除すると使い果たされる可能性のある複数のタイプです。したがって、通常の[テキストファイルからの実行](https://docs.oracle.com/javase/tutorial/jdbc/basics/processingsqlstatements.html#executing_queries)ではなく[準備された声明](https://docs.oracle.com/javase/tutorial/jdbc/basics/prepared.html)使用し、準備済みステートメントを再利用して直接実行することをお勧めします。これにより、TiDB で SQL 実行プランを繰り返し解析して生成するオーバーヘッドを回避できます。

現在、上位フレームワークの多くはSQL実行にPrepare APIを呼び出します。開発にJDBC APIを直接使用する場合は、Prepare APIを選択するように注意してください。

また、MySQL Connector/J のデフォルト実装では、クライアント側のステートメントのみが前処理され、クライアント側で`?`が置換された後、ステートメントがテキストファイルでサーバーに送信されます。そのため、Prepare API を使用するだけでなく、TiDBサーバーでステートメントの前処理を行う前に、JDBC 接続パラメータで`useServerPrepStmts = true`設定する必要があります。詳細なパラメータ設定については、 [MySQL JDBCパラメータ](#mysql-jdbc-parameters)を参照してください。

#### バッチAPIを使用する {#use-batch-api}

バッチ挿入の場合は、 [`addBatch` / `executeBatch` API](https://www.tutorialspoint.com/jdbc/jdbc-batch-processing)を使用できます。 `addBatch()`メソッドは、複数の SQL ステートメントを最初にクライアント上でキャッシュし、次に`executeBatch`メソッドを呼び出すときにそれらをまとめてデータベースサーバーに送信するために使用されます。

> **注記：**
>
> デフォルトの MySQL Connector/J 実装では、 `addBatch()`でバッチに追加された SQL ステートメントの送信時刻は`executeBatch()`が呼び出された時刻まで遅延されますが、実際のネットワーク転送中にステートメントは 1 つずつ送信されます。そのため、この方法では通常、通信オーバーヘッドの量は削減されません。
>
> バッチネットワーク転送を行う場合は、JDBC 接続パラメータの`rewriteBatchedStatements = true`設定する必要があります。詳細なパラメータ設定については、 [バッチ関連パラメータ](#batch-related-parameters)を参照してください。

#### <code>StreamingResult</code>を使用して実行結果を取得します {#use-code-streamingresult-code-to-get-the-execution-result}

ほとんどのシナリオでは、実行効率を向上させるために、JDBC はクエリ結果を事前に取得し、デフォルトでクライアントメモリに保存します。ただし、クエリが非常に大きな結果セットを返す場合、クライアントはデータベースサーバーに一度に返されるレコードの数を減らすように要求することが多く、クライアントのメモリが準備されて次のバッチを要求するまで待機します。

通常、JDBC には 2 種類の処理方法があります。

-   [`FetchSize`を`Integer.MIN_VALUE`に設定する](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-implementation-notes.html#ResultSet) 、クライアントがキャッシュしないようにします。クライアントは、 `StreamingResult`を介してネットワーク接続から実行結果を読み取ります。

    クライアントがストリーミング読み取りメソッドを使用する場合、クエリを実行するためにステートメントを引き続き使用する前に、読み取りを終了するか`resultset`を閉じる必要があります。そうしないと、エラー`No statements may be issued when any streaming result sets are open and in use on a given connection. Ensure that you have called .close() on any active streaming result sets before attempting more queries.`が返されます。

    クライアントが読み取りを完了するか`resultset`を閉じる前にクエリでこのようなエラーを回避するには、URL に`clobberStreamingResults=true`パラメータを追加します。すると、 `resultset`自動的に閉じられますが、前のストリーミング クエリで読み取られる結果セットは失われます。

-   カーソル フェッチを使用するには、まず正の整数として[`FetchSize`を設定する](http://makejavafaster.blogspot.com/2015/06/jdbc-fetch-size-performance.html)設定し、JDBC URL で`useCursorFetch=true`設定します。

TiDB は両方の方法をサポートしていますが、実装が簡単で実行効率が優れているため、最初の方法を使用することをお勧めします。

### MySQL JDBCパラメータ {#mysql-jdbc-parameters}

JDBC は通常、実装関連の設定を JDBC URL パラメータの形で提供します。このセクションでは[MySQL Connector/J のパラメータ設定](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-configuration-properties.html)紹介します (MariaDB を使用する場合は[MariaDBのパラメータ設定](https://mariadb.com/kb/en/library/about-mariadb-connector-j/#optional-url-parameters)を参照してください)。このドキュメントではすべての設定項目を網羅することはできないため、主にパフォーマンスに影響を与える可能性のあるいくつかのパラメータに焦点を当てています。

#### 準備関連のパラメータ {#prepare-related-parameters}

このセクションでは、 `Prepare`に関連するパラメータを紹介します。

##### <code>useServerPrepStmts</code> {#code-useserverprepstmts-code}

デフォルトでは`useServerPrepStmts`は`false`に設定されています。つまり、Prepare API を使用する場合でも、「準備」操作はクライアントでのみ実行されます。サーバーの解析オーバーヘッドを回避するために、同じ SQL ステートメントで Prepare API を複数回使用する場合は、この構成を`true`に設定することをお勧めします。

この設定がすでに有効になっていることを確認するには、次の操作を実行します。

-   TiDB 監視ダッシュボードに移動し、**クエリ サマリー**&gt;**インスタンス別の CPS**を通じて要求コマンド タイプを表示します。
-   リクエスト内の`COM_QUERY` `COM_STMT_EXECUTE`または`COM_STMT_PREPARE`に置き換えられた場合、この設定はすでに有効になっていることを意味します。

##### <code>cachePrepStmts</code> {#code-cacheprepstmts-code}

`useServerPrepStmts=true`ではサーバーがPrepared Statements を実行できますが、デフォルトでは、クライアントは実行ごとに Prepared Statements を閉じて再利用しません。つまり、「準備」操作はテキスト ファイルの実行ほど効率的ではありません。これを解決するには、 `useServerPrepStmts=true`設定した後、 `cachePrepStmts=true`も構成することをお勧めします。これにより、クライアントは Prepared Statements をキャッシュできます。

この設定がすでに有効になっていることを確認するには、次の操作を実行します。

-   TiDB 監視ダッシュボードに移動し、**クエリ サマリー**&gt;**インスタンス別の CPS**を通じて要求コマンド タイプを表示します。
-   リクエスト内の`COM_STMT_EXECUTE`の数が`COM_STMT_PREPARE`の数よりはるかに多い場合、この設定はすでに有効になっていることを意味します。

また、 `useConfigs=maxPerformance`を設定すると、 `cachePrepStmts=true`を含む複数のパラメータが同時に設定されます。

##### <code>prepStmtCacheSqlLimit</code> {#code-prepstmtcachesqllimit-code}

`cachePrepStmts`を設定した後は、 `prepStmtCacheSqlLimit`設定にも注意してください (デフォルト値は`256`です)。この設定は、クライアントにキャッシュされる Prepared Statements の最大長を制御します。

この最大長を超える準備済みステートメントはキャッシュされないため、再利用できません。この場合、アプリケーションの実際の SQL の長さに応じて、この構成の値を増やすことを検討してください。

次の場合には、この設定が小さすぎないかどうかを確認する必要があります。

-   TiDB 監視ダッシュボードに移動し、**クエリ サマリー**&gt;**インスタンス別の CPS**を通じて要求コマンド タイプを表示します。
-   そして、 `cachePrepStmts=true`設定されていることがわかりますが、 `COM_STMT_PREPARE`まだ`COM_STMT_EXECUTE`とほぼ同じであり、 `COM_STMT_CLOSE`存在します。

##### <code>prepStmtCacheSize</code> {#code-prepstmtcachesize-code}

`prepStmtCacheSize`キャッシュされた Prepared Statements の数を制御します (デフォルト値は`25`です)。アプリケーションで多くの種類の SQL ステートメントを「準備」する必要があり、Prepared Statements を再利用したい場合は、この値を増やすことができます。

この設定がすでに有効になっていることを確認するには、次の操作を実行します。

-   TiDB 監視ダッシュボードに移動し、**クエリ サマリー**&gt;**インスタンス別の CPS**を通じて要求コマンド タイプを表示します。
-   リクエスト内の`COM_STMT_EXECUTE`の数が`COM_STMT_PREPARE`の数よりはるかに多い場合、この設定はすでに有効になっていることを意味します。

#### バッチ関連パラメータ {#batch-related-parameters}

バッチ書き込みを処理する場合は、 `rewriteBatchedStatements=true`設定することをお勧めします。 `addBatch()`または`executeBatch()`を使用した後でも、JDBC はデフォルトで SQL を 1 つずつ送信します。次に例を示します。

```java
pstmt = prepare("insert into t (a) values(?)");
pstmt.setInt(1, 10);
pstmt.addBatch();
pstmt.setInt(1, 11);
pstmt.addBatch();
pstmt.setInt(1, 12);
pstmt.executeBatch();
```

`Batch`方法が使用されていますが、TiDB に送信される SQL ステートメントは、個別の`INSERT`のステートメントのままです。

```sql
insert into t(a) values(10);
insert into t(a) values(11);
insert into t(a) values(12);
```

ただし、 `rewriteBatchedStatements=true`設定すると、TiDB に送信される SQL ステートメントは単一の`INSERT`ステートメントになります。

```sql
insert into t(a) values(10),(11),(12);
```

`INSERT`のステートメントの書き換えは、複数の「values」キーワードの後の値を 1 つの SQL ステートメント全体に連結することであることに注意してください。3 `INSERT`ステートメントに他の違いがある場合は、次のように書き換えることはできません。

```sql
insert into t (a) values (10) on duplicate key update a = 10;
insert into t (a) values (11) on duplicate key update a = 11;
insert into t (a) values (12) on duplicate key update a = 12;
```

上記の`INSERT`文を 1 つの文に書き直すことはできません。ただし、3 つの文を次のように変更すると、

```sql
insert into t (a) values (10) on duplicate key update a = values(a);
insert into t (a) values (11) on duplicate key update a = values(a);
insert into t (a) values (12) on duplicate key update a = values(a);
```

すると、書き換え要件が満たされます。上記の`INSERT`ステートメントは、次の 1 つのステートメントに書き換えられます。

```sql
insert into t (a) values (10), (11), (12) on duplicate key update a = values(a);
```

バッチ更新中に 3 つ以上の更新が行われる場合、SQL ステートメントは書き換えられ、複数のクエリとして送信されます。これにより、クライアントからサーバーへの要求のオーバーヘッドが効果的に削減されますが、副作用として、より大きな SQL ステートメントが生成されます。例:

```sql
update t set a = 10 where id = 1; update t set a = 11 where id = 2; update t set a = 12 where id = 3;
```

また、 [クライアントのバグ](https://bugs.mysql.com/bug.php?id=96623)のため、バッチ更新中に`rewriteBatchedStatements=true`と`useServerPrepStmts=true`を設定する場合は、このバグを回避するために`allowMultiQueries=true`パラメータも設定することをお勧めします。

#### パラメータを統合する {#integrate-parameters}

監視を通じて、アプリケーションが TiDB クラスターに対して`INSERT`操作のみを実行しているにもかかわらず、冗長な`SELECT`ステートメントが多数あることに気付く場合があります。通常、これは、JDBC が設定を照会するためにいくつかの SQL ステートメント (例: `select @@session.transaction_read_only`を送信するために発生します。これらの SQL ステートメントは TiDB には役に立たないため、余分なオーバーヘッドを回避するために`useConfigs=maxPerformance`を構成することをお勧めします。

`useConfigs=maxPerformance`には、一連の構成が含まれています。MySQL Connector/J 8.0 および MySQL Connector/J 5.1 の詳細な構成については、それぞれ[mysql-コネクタ-j 8.0](https://github.com/mysql/mysql-connector-j/blob/release/8.0/src/main/resources/com/mysql/cj/configurations/maxPerformance.properties)と[mysql-コネクタ-j 5.1](https://github.com/mysql/mysql-connector-j/blob/release/5.1/src/com/mysql/jdbc/configs/maxPerformance.properties)を参照してください。

設定後、監視をチェックして、 `SELECT`ステートメントの数が減っていることを確認できます。

#### タイムアウト関連のパラメータ {#timeout-related-parameters}

TiDB は、タイムアウトを制御する`wait_timeout`と`max_execution_time`という 2 つの MySQL 互換パラメータを提供します。これら 2 つのパラメータは、それぞれJavaアプリケーションとの接続アイドル タイムアウトと接続中の SQL 実行のタイムアウトを制御します。つまり、これらのパラメータは、TiDB とJavaアプリケーション間の接続の最長アイドル時間と最長ビジー時間を制御します。両方のパラメータのデフォルト値は`0`で、デフォルトでは接続が無限にアイドル状態および無限にビジー状態 (1 つの SQL 文の実行に無限の期間) になることができます。

ただし、実際の本番環境では、アイドル接続や実行時間が長すぎる SQL ステートメントは、データベースやアプリケーションに悪影響を及ぼします。アイドル接続や実行時間が長すぎる SQL ステートメントを回避するには、アプリケーションの接続文字列でこれらの 2 つのパラメータを設定します。たとえば、 `sessionVariables=wait_timeout=3600` (1 時間) と`sessionVariables=max_execution_time=300000` (5 分) を設定します。

## 接続プール {#connection-pool}

TiDB (MySQL) 接続の構築は、TCP 接続の構築に加えて接続認証も必要となるため、比較的コストがかかります (少なくとも OLTP シナリオの場合)。そのため、クライアントは通常、再利用のために TiDB (MySQL) 接続を接続プールに保存します。

Javaには、 [HikariCP](https://github.com/brettwooldridge/HikariCP) 、 [tomcat-jdbc](https://tomcat.apache.org/tomcat-10.1-doc/jdbc-pool.html) 、 [druid](https://github.com/alibaba/druid) 、 [翻訳:](https://www.mchange.com/projects/c3p0/) 、 [dbcp](https://commons.apache.org/proper/commons-dbcp/)など、多くの接続プール実装があります。TiDB では、使用する接続プールに制限がないため、アプリケーションに応じて好きな接続プールを選択できます。

### 接続数を設定する {#configure-the-number-of-connections}

接続プールのサイズは、アプリケーション自体のニーズに応じて適切に調整するのが一般的です。HikariCPを例に挙げます。

-   `maximumPoolSize` : 接続プール内の最大接続数。この値が大きすぎると、TiDB は無駄な接続を維持するためにリソースを消費します。この値が小さすぎると、アプリケーションの接続速度が遅くなります。したがって、この値は適切に設定してください。詳細については、 [プールのサイズについて](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing)を参照してください。
-   `minimumIdle` : 接続プール内のアイドル接続の最小数。主に、アプリケーションがアイドル状態のときに突然の要求に応答するためにいくつかの接続を予約するために使用されます。アプリケーションのニーズに応じて構成することもできます。

アプリケーションは、使用を終了した後、接続を返す必要があります。また、アプリケーションが対応する接続​​プール監視 ( `metricRegistry`など) を使用して、接続プールの問題を適時に特定することも推奨されます。

### プローブ構成 {#probe-configuration}

接続プールは、次のようにクライアントから TiDB への永続的な接続を維持します。

-   v5.4 より前では、TiDB はデフォルトでクライアント接続を積極的に閉じません (エラーが報告されない限り)。
-   v5.4 以降、TiDB はデフォルトで`28800`秒 (つまり`8`時間) 非アクティブになるとクライアント接続を自動的に閉じます。このタイムアウト設定は、TiDB および MySQL 互換の`wait_timeout`変数を使用して制御できます。詳細については、 [JDBC クエリ タイムアウト](/develop/dev-guide-timeouts-in-tidb.md#jdbc-query-timeout)を参照してください。

さらに、クライアントと TiDB の間には、 [LVS の](https://en.wikipedia.org/wiki/Linux_Virtual_Server)や[HAプロキシ](https://en.wikipedia.org/wiki/HAProxy)などのネットワーク プロキシが存在する場合があります。これらのプロキシは通常、特定のアイドル期間 (プロキシのアイドル構成によって決定) の経過後に、積極的に接続をクリーンアップします。プロキシのアイドル構成を監視することに加えて、接続プールはキープアライブのために接続を維持またはプローブする必要もあります。

Javaアプリケーションで次のエラーが頻繁に表示される場合:

    The last packet sent successfully to the server was 3600000 milliseconds ago. The driver has not received any packets from the server. com.mysql.jdbc.exceptions.jdbc4.CommunicationsException: Communications link failure

`n milliseconds ago`分の`n`が`0`または非常に小さい値である場合、通常は実行された SQL 操作によって TiDB が異常終了したためです。原因を見つけるには、TiDB の stderr ログを確認することをお勧めします。

`n`が非常に大きな値の場合 (上記の例では`3600000`など)、この接続は長時間アイドル状態だった後、中間プロキシによって閉じられた可能性があります。通常の解決策は、プロキシのアイドル構成の値を増やし、接続プールで次の操作を行うことです。

-   毎回接続を使用する前に接続が利用可能かどうかを確認してください
-   別のスレッドを使用して、接続が利用可能かどうかを定期的に確認します。
-   接続を維持するために定期的にテストクエリを送信する

異なる接続プールの実装では、上記の方法の 1 つ以上がサポートされる場合があります。対応する構成を見つけるには、接続プールのドキュメントを確認してください。

## データアクセスフレームワーク {#data-access-framework}

アプリケーションでは、データベース アクセスを簡素化するために、何らかのデータ アクセス フレームワークを使用することが多いです。

### マイバティス {#mybatis}

[マイバティス](http://www.mybatis.org/mybatis-3/) 、人気のあるJavaデータ アクセス フレームワークです。主に SQL クエリを管理し、結果セットとJavaオブジェクト間のマッピングを完了するために使用されます。MyBatis は TiDB と高い互換性があります。MyBatis は、これまでの問題により、ほとんど問題がありません。

このドキュメントでは、主に以下の構成に焦点を当てています。

#### マッパーパラメータ {#mapper-parameters}

MyBatis Mapper は次の 2 つのパラメータをサポートしています。

-   `select 1 from t where id = #{param1}`は Prepared Statement として`select 1 from t where id =?`に変換され、「準備」され、実際のパラメータは再利用に使用されます。このパラメータを前述の Prepare 接続パラメータと併用すると、最高のパフォーマンスが得られます。
-   `select 1 from t where id = ${param2}`テキスト ファイルとして`select 1 from t where id = 1`に置き換えられ、実行されます。このステートメントが異なるパラメーターに置き換えられて実行されると、MyBatis はステートメントを「準備」するための異なるリクエストを TiDB に送信します。これにより、TiDB が多数の Prepared Statements をキャッシュする可能性があり、この方法で SQL 操作を実行すると、インジェクション セキュリティ リスクが発生します。

#### 動的SQLバッチ {#dynamic-sql-batch}

[動的 SQL - foreach](http://www.mybatis.org/mybatis-3/dynamic-sql.html#foreach)

複数の`INSERT`ステートメントを`insert ... values(...), (...), ...`の形式に自動的に書き換えることをサポートするために、前述のように JDBC で`rewriteBatchedStatements=true`を構成することに加えて、MyBatis は動的 SQL を使用して半自動的にバッチ挿入を生成することもできます。次のマッパーを例に挙げます。

```xml
<insert id="insertTestBatch" parameterType="java.util.List" fetchSize="1">
  insert into test
   (id, v1, v2)
  values
  <foreach item="item" index="index" collection="list" separator=",">
  (
   #{item.id}, #{item.v1}, #{item.v2}
  )
  </foreach>
  on duplicate key update v2 = v1 + values(v1)
</insert>
```

このマッパーは`insert on duplicate key update`ステートメントを生成します。 `(?,?,?)`に続く「値」の数は、渡されたリストの数によって決まります。 最終的な効果は`rewriteBatchStatements=true`使用する場合と同様であり、クライアントと TiDB 間の通信オーバーヘッドも効果的に削減されます。

前述したように、準備済みステートメントの最大長が`prepStmtCacheSqlLimit`を超えるとキャッシュされなくなることにも注意する必要があります。

#### ストリーミング結果 {#streaming-result}

[前のセクション](#use-streamingresult-to-get-the-execution-result)では、JDBC で読み取り実行結果をストリームする方法が導入されています。JDBC の対応する構成に加えて、MyBatis で非常に大きな結果セットを読み取る場合は、次の点にも注意する必要があります。

-   マッパー構成で単一の SQL ステートメントに`fetchSize`設定できます (前のコード ブロックを参照)。その効果は、JDBC で`setFetchSize`を呼び出すのと同じです。
-   結果セット全体を一度に取得しないようにするには、クエリ インターフェイスを`ResultHandler`で使用します。
-   ストリーム読み取りには`Cursor`クラスを使用できます。

XML を使用してマッピングを構成する場合は、マッピングの`<select>`セクションで`fetchSize="-2147483648"` ( `Integer.MIN_VALUE` ) を構成することで読み取り結果をストリーミングできます。

```xml
<select id="getAll" resultMap="postResultMap" fetchSize="-2147483648">
  select * from post;
</select>
```

コードを使用してマッピングを構成する場合は、 `@Options(fetchSize = Integer.MIN_VALUE)`アノテーションを追加し、結果のタイプを`Cursor`のままにして、SQL 結果をストリーミングで読み取ることができるようにすることができます。

```java
@Select("select * from post")
@Options(fetchSize = Integer.MIN_VALUE)
Cursor<Post> queryAllPost();
```

### <code>ExecutorType</code> {#code-executortype-code}

`openSession`の中から`ExecutorType`選択できます。MyBatis は 3 種類のエグゼキュータをサポートしています。

-   シンプル: 準備済みステートメントは実行ごとにJDBCに呼び出されます（JDBC構成項目`cachePrepStmts`が有効になっている場合は、繰り返しの準備済みステートメントが再利用されます）
-   再利用: 準備済みステートメントは`executor`にキャッシュされるため、JDBC `cachePrepStmts`を使用せずに準備済みステートメントの重複呼び出しを減らすことができます。
-   バッチ: 各更新操作 ( `INSERT` / `DELETE` / `UPDATE` ) は最初にバッチに追加され、トランザクションがコミットされるか、クエリが`SELECT`実行されるまで実行されます。JDBCレイヤーで`rewriteBatchStatements`有効になっている場合は、ステートメントの書き換えが試行されます。そうでない場合は、ステートメントが 1 つずつ送信されます。

通常、 `ExecutorType`のデフォルト値は`Simple`です。 `openSession`を呼び出す場合は`ExecutorType`を変更する必要があります。 バッチ実行の場合、トランザクションで`UPDATE`または`INSERT`ステートメントはかなり速く実行されますが、データの読み取りやトランザクションのコミットの際には遅くなることが分かります。 これは実際には正常なので、遅い SQL クエリのトラブルシューティングを行うときは、この点に注意する必要があります。

## 春のトランザクション {#spring-transaction}

現実の世界では、アプリケーションは[春のトランザクション](https://docs.spring.io/spring/docs/4.2.x/spring-framework-reference/html/transaction.html)と AOP の側面を使用してトランザクションを開始および停止する場合があります。

メソッド定義に`@Transactional`アノテーションを追加することで、AOP はメソッドが呼び出される前にトランザクションを開始し、メソッドが結果を返す前にトランザクションをコミットします。アプリケーションに同様のニーズがある場合は、コード内に`@Transactional`見つけて、トランザクションがいつ開始され、いつ終了するかを判断できます。

埋め込みの特殊なケースに注意してください。その場合、Spring は[伝搬](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/transaction/annotation/Propagation.html)構成に基づいて異なる動作をします。

## その他 {#misc}

このセクションでは、問題のトラブルシューティングに役立つJavaの便利なツールをいくつか紹介します。

### トラブルシューティングツール {#troubleshooting-tools}

Javaアプリケーションで問題が発生し、アプリケーション ロジックがわからない場合は、JVM の強力なトラブルシューティング ツールを使用することをお勧めします。一般的なツールをいくつか紹介します。

#### jstack {#jstack}

[jstack](https://docs.oracle.com/javase/7/docs/technotes/tools/share/jstack.html)は Go の pprof/goroutine に似ており、プロセスがスタックした問題を簡単にトラブルシューティングできます。

`jstack pid`を実行すると、対象プロセス内のすべてのスレッドの ID とスタック情報を出力できます。デフォルトではJavaスタックのみが出力されます。JVM 内の C++ スタックも同時に出力したい場合は、 `-m`オプションを追加します。

jstack を複数回使用することで、スタックした問題 (たとえば、Mybatis で Batch ExecutorType を使用しているためにアプリケーションのビューからクエリが遅いなど) やアプリケーションのデッドロックの問題 (たとえば、アプリケーションが送信前にロックをプリエンプトしているために SQL ステートメントを送信しないなど) を簡単に見つけることができます。

さらに、 `top -p $ PID -H`またはJavaスイスナイフは、スレッド ID を表示する一般的な方法です。また、「スレッドが CPU リソースを大量に占有し、何を実行しているのかわからない」という問題を特定するには、次の手順を実行します。

-   スレッド ID を 16 進数に変換するには`printf "%x\n" pid`使用します。
-   対応するスレッドのスタック情報を見つけるには、jstack 出力に移動します。

#### jmapとmat {#jmap-x26-mat}

Go の pprof/heap とは異なり、 [jmap](https://docs.oracle.com/javase/7/docs/technotes/tools/share/jmap.html)​​プロセス全体のメモリスナップショットをダンプし (Go ではディストリビューターのサンプリング)、そのスナップショットを別のツール[マット](https://www.eclipse.org/mat/)で分析できます。

mat を使用すると、プロセス内のすべてのオブジェクトの関連情報と属性を確認できるほか、スレッドの実行ステータスを観察することもできます。たとえば、mat を使用して、現在のアプリケーションに存在する MySQL 接続オブジェクトの数や、各接続オブジェクトのアドレスとステータス情報を確認できます。

デフォルトでは、mat は到達可能なオブジェクトのみを処理することに注意してください。若い GC の問題をトラブルシューティングする場合は、到達不可能なオブジェクトを表示するように mat 構成を調整できます。また、若い GC の問題 (または多数の短命オブジェクト) のメモリ割り当てを調査するには、 Java Flight Recorder を使用する方が便利です。

#### 痕跡 {#trace}

通常、オンライン アプリケーションではコードの変更はサポートされていませんが、問題を特定するためにJavaで動的なインストルメンテーションを実行することが望まれることがよくあります。そのため、btrace または arthas trace を使用するのがよい選択肢です。これらを使用すると、アプリケーション プロセスを再起動せずにトレース コードを動的に挿入できます。

#### フレームグラフ {#flame-graph}

Javaアプリケーションでフレーム グラフを取得するのは面倒です。詳細については、 [Java Flame Graphs の紹介: みんなに火を!](http://psy-lob-saw.blogspot.com/2017/02/flamegraphs-intro-fire-for-everyone.html)参照してください。

## 結論 {#conclusion}

このドキュメントでは、データベースと対話する一般的なJavaコンポーネントに基づいて、TiDB を使用したJavaアプリケーションの開発に関する一般的な問題と解決策について説明します。TiDB は MySQL プロトコルと高い互換性があるため、MySQL ベースのJavaアプリケーションのベスト プラクティスのほとんどは TiDB にも適用されます。

[TiDB コミュニティ Slack チャンネル](https://tidbcommunity.slack.com/archives/CH7TTLL7P)にご参加いただき、TiDB を使用してJavaアプリケーションを開発する際の経験や問題について、幅広い TiDB ユーザー グループと共有してください。
