---
title: Best Practices for Developing Java Applications with TiDB
summary: このドキュメントでは、TiDB を使用したJavaアプリケーション開発におけるベストプラクティスを紹介します。データベース関連コンポーネント、JDBC の使用方法、接続プール構成、データアクセスフレームワーク、Spring トランザクション、およびトラブルシューティングツールについて解説します。TiDB は MySQL と高い互換性があるため、MySQL ベースのJavaアプリケーション開発におけるベストプラクティスのほとんどは TiDB にも適用できます。
aliases: ['/ja/docs/dev/best-practices/java-app-best-practices/','/ja/docs/dev/reference/best-practices/java-app/','/ja/tidb/stable/java-app-best-practices/','/ja/tidb/dev/java-app-best-practices/']
---

# TiDBを使用したJavaアプリケーション開発のベストプラクティス {#best-practices-for-developing-java-applications-with-tidb}

このドキュメントでは、TiDBをより効果的に活用するためのJavaアプリケーション開発におけるベストプラクティスを紹介します。また、バックエンドのTiDBデータベースと連携する一般的なJavaアプリケーションコンポーネントに基づき、開発中に発生する一般的な問題への解決策も提供します。

## Javaアプリケーションにおけるデータベース関連コンポーネント {#database-related-components-in-java-applications}

JavaアプリケーションでTiDBデータベースと連携する一般的なコンポーネントには、以下のようなものがあります。

-   ネットワークプロトコル: クライアントは標準の[MySQLプロトコル](https://dev.mysql.com/doc/dev/mysql-server/latest/PAGE_PROTOCOL.html)を介して TiDBサーバーとやり取りします。
-   JDBC APIとJDBCドライバ： Javaアプリケーションは通常、標準の[JDBC（Javaデータベース接続）](https://docs.oracle.com/javase/8/docs/technotes/guides/jdbc/) APIを使用してデータベースにアクセスします。TiDBに接続するには、JDBC APIを介してMySQLプロトコルを実装するJDBCドライバを使用できます。MySQL用の一般的なJDBCドライバには、 [MySQL Connector/J](https://github.com/mysql/mysql-connector-j)と[MariaDB Connector/J](https://mariadb.com/docs/connectors/mariadb-connector-j/about-mariadb-connector-j#about-mariadb-connectorj)あります。
-   データベース接続プール：アプリケーションは通常、接続要求のたびに接続を作成するオーバーヘッドを削減するために、接続プールを使用して接続をキャッシュし、再利用します。JDBC [データソース](https://docs.oracle.com/javase/8/docs/api/javax/sql/DataSource.html)では、接続プールAPIが定義されています。必要に応じて、さまざまなオープンソースの接続プール実装から選択できます。
-   データアクセスフレームワーク: アプリケーションは通常、データベースアクセス操作をさらに簡素化および管理するために、 [MyBatis](https://mybatis.org/mybatis-3/index.html)や[ハイバネイト](https://hibernate.org/)のようなデータアクセスフレームワークを使用します。
-   アプリケーションの実装：アプリケーションロジックは、データベースにどのコマンドをいつ送信するかを制御します。一部のアプリケーションでは、トランザクションの開始とコミットのロジックを管理するために[春のトランザクション](https://docs.spring.io/spring/docs/4.2.x/spring-framework-reference/html/transaction.html)アスペクトを使用します。

![Java application components](/media/best-practices/java-practice-1.png)

上記の図から、 Javaアプリケーションは次のようなことを行う可能性があることがわかります。

-   TiDBと連携するために、JDBC APIを介してMySQLプロトコルを実装します。
-   接続プールから永続的な接続を取得します。
-   SQL文を生成および実行するには、MyBatisなどのデータアクセスフレームワークを使用します。
-   Spring トランザクションを使用すると、トランザクションを自動的に開始または停止できます。

この文書の残りの部分では、上記のコンポーネントを使用してJavaアプリケーションを開発する際に発生する問題とその解決策について説明します。

## JDBC {#jdbc}

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

-   最初の方法: [`FetchSize` `Integer.MIN_VALUE`に設定します。](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-implementation-notes.html#ResultSet)クライアントがキャッシュしないようにします。クライアントは`StreamingResult`を介してネットワーク接続から実行結果を読み取ります。

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

##### <code>useServerPrepStmts</code> {#code-useserverprepstmts-code}

`useServerPrepStmts`はデフォルトで`false`に設定されています。つまり、Prepare API を使用する場合でも、「prepare」操作はクライアント側でのみ実行されます。サーバーの解析オーバーヘッドを回避するため、同じ SQL ステートメントで Prepare API を複数回使用する場合は、この設定を`true`に設定することをお勧めします。

この設定が既に有効になっていることを確認するには、次の操作を実行してください。

-   TiDB モニタリング ダッシュボードに移動し、 **[クエリ概要]** &gt; **[インスタンス別 CPS]**からリクエスト コマンド タイプを確認します。
-   リクエストで`COM_QUERY` `COM_STMT_EXECUTE`または`COM_STMT_PREPARE`に置き換えられている場合、この設定は既に有効になっていることを意味します。

##### <code>cachePrepStmts</code> {#code-cacheprepstmts-code}

`useServerPrepStmts=true`ではサーバーがプリペアドステートメントを実行できますが、デフォルトではクライアントは実行後にプリペアドステートメントを閉じ、再利用しません。つまり、「準備」操作はテキストファイルの実行ほど効率的ではありません。この問題を解決するには、 `useServerPrepStmts=true`設定した後、 `cachePrepStmts=true`設定することをお勧めします。これにより、クライアントはプリペアドステートメントをキャッシュできるようになります。

この設定が既に有効になっていることを確認するには、次の操作を実行してください。

-   TiDB モニタリング ダッシュボードに移動し、 **[クエリ概要]** &gt; **[インスタンス別 CPS]**からリクエスト コマンド タイプを確認します。
-   リクエスト内の`COM_STMT_EXECUTE`の数が`COM_STMT_PREPARE`の数よりはるかに多い場合、この設定は既に有効になっていることを意味します。

さらに、 `useConfigs=maxPerformance`設定すると、 `cachePrepStmts=true`含む複数のパラメータが同時に設定されます。

##### <code>prepStmtCacheSqlLimit</code> {#code-prepstmtcachesqllimit-code}

`cachePrepStmts`設定が完了したら、 `prepStmtCacheSqlLimit`設定（デフォルト値は`256` ）にも注意してください。この設定は、クライアントにキャッシュされるプリペアドステートメントの最大長を制御します。

この最大長を超えるプリペアドステートメントはキャッシュされないため、再利用できません。この場合、アプリケーションの実際のSQLの長さに応じて、この設定値を増やすことを検討してください。

次のような場合は、この設定が小さすぎるかどうかを確認する必要があります。

-   TiDB モニタリング ダッシュボードに移動し、 **[クエリ概要]** &gt; **[インスタンス別 CPS]**からリクエスト コマンド タイプを確認します。
-   そして、 `cachePrepStmts=true`設定されているが、 `COM_STMT_PREPARE`は依然として`COM_STMT_EXECUTE`とほぼ等しく、 `COM_STMT_CLOSE`存在することがわかった。

##### <code>prepStmtCacheSize</code> {#code-prepstmtcachesize-code}

`prepStmtCacheSize`キャッシュされるプリペアドステートメントの数を制御します（デフォルト値は`25`です）。アプリケーションで多くの種類のSQLステートメントを「準備」する必要があり、プリペアドステートメントを再利用したい場合は、この値を増やすことができます。

この設定が既に有効になっていることを確認するには、次の操作を実行してください。

-   TiDB モニタリング ダッシュボードに移動し、 **[クエリ概要]** &gt; **[インスタンス別 CPS]**からリクエスト コマンド タイプを確認します。
-   リクエスト内の`COM_STMT_EXECUTE`の数が`COM_STMT_PREPARE`の数よりはるかに多い場合、この設定は既に有効になっていることを意味します。

#### <code>readOnlyPropagatesToServer</code> {#code-readonlypropagatestoserver-code}

プロパティ`readOnlyPropagatesToServer`を無効にしてください。このプロパティが有効になっている場合、JDBCドライバはサーバーにステートメント`SET SESSION TRANSACTION READ ONLY`を送信します。TiDBはこのステートメントをサポートしておらず、すべてのTiDBノードが読み取り接続と書き込み接続の両方を受け入れるため、このステートメントを送信する必要はありません。

#### バッチ関連パラメータ {#batch-related-parameters}

バッチ書き込みを処理する際は、 `rewriteBatchedStatements=true`設定することをお勧めします。3 または`executeBatch()` `addBatch()`使用した後でも、JDBC はデフォルトでは SQL を 1 つずつ送信します。例:

```java
pstmt = prepare("insert into t (a) values(?)");
pstmt.setInt(1, 10);
pstmt.addBatch();
pstmt.setInt(1, 11);
pstmt.addBatch();
pstmt.setInt(1, 12);
pstmt.executeBatch();
```

`Batch`メソッドが使用されているにもかかわらず、TiDBに送信されるSQLステートメントは依然として個別の`INSERT`ステートメントです。

```sql
insert into t(a) values(10);
insert into t(a) values(11);
insert into t(a) values(12);
```

しかし、 `rewriteBatchedStatements=true`設定すると、TiDB に送信される SQL ステートメントは単一の`INSERT`ステートメントになります。

```sql
insert into t(a) values(10),(11),(12);
```

`INSERT`のステートメントの書き換えは、複数の「values」キーワードの後の値を連結して、1つのSQLステートメントにすることです。3 `INSERT`のステートメントに他の違いがある場合は、書き換えることはできません。たとえば、次のようになります。

```sql
insert into t (a) values (10) on duplicate key update a = 10;
insert into t (a) values (11) on duplicate key update a = 11;
insert into t (a) values (12) on duplicate key update a = 12;
```

上記の`INSERT`つの文は1つの文に書き換えることはできません。しかし、3つの文を次のように変更すると次のようになります。

```sql
insert into t (a) values (10) on duplicate key update a = values(a);
insert into t (a) values (11) on duplicate key update a = values(a);
insert into t (a) values (12) on duplicate key update a = values(a);
```

すると、書き換え要件を満たします。上記の`INSERT`つの文は、次の1つの文に書き換えられます。

```sql
insert into t (a) values (10), (11), (12) on duplicate key update a = values(a);
```

バッチ更新中に3つ以上の更新がある場合、SQLステートメントは書き換えられ、複数のクエリとして送信されます。これにより、クライアントからサーバーへのリクエストのオーバーヘッドは効果的に削減されますが、副作用として、より大きなSQLステートメントが生成されます。例：

```sql
update t set a = 10 where id = 1; update t set a = 11 where id = 2; update t set a = 12 where id = 3;
```

さらに、 [クライアントのバグ](https://bugs.mysql.com/bug.php?id=96623)問題があるため、バッチ更新中に`rewriteBatchedStatements=true`と`useServerPrepStmts=true`を設定する場合は、このバグを回避するために`allowMultiQueries=true`パラメータも設定することをお勧めします。

#### パラメータを統合する {#integrate-parameters}

監視を通じて、アプリケーションが TiDB クラスタに対して実行する操作は`INSERT`だけであるにもかかわらず、冗長な`SELECT`ステートメントが多数あることに気づくかもしれません。通常、これは JDBC が設定を照会するためにいくつかの SQL ステートメントを送信することによって発生します (例: `select @@session.transaction_read_only` )。これらの SQL ステートメントは TiDB にとって不要なので、余分なオーバーヘッドを避けるために`useConfigs=maxPerformance`を設定することをお勧めします。

`useConfigs=maxPerformance`には設定のグループが含まれています。MySQL Connector/J 8.0およびMySQL Connector/J 5.1の詳細な設定については、それぞれ[mysql-connector-j 8.0](https://github.com/mysql/mysql-connector-j/blob/release/8.0/src/main/resources/com/mysql/cj/configurations/maxPerformance.properties)および[mysql-connector-j 5.1](https://github.com/mysql/mysql-connector-j/blob/release/5.1/src/com/mysql/jdbc/configs/maxPerformance.properties)を参照してください。

設定が完了したら、監視画面で`SELECT`ステートメントの数が減少していることを確認できます。

> **注記：**
>
> `useConfigs=maxPerformance`を有効にするには、MySQL Connector/Jバージョン8.0.33以降が必要です。詳細については、 [MySQL JDBC バグ](/develop/dev-guide-third-party-tools-compatibility.md#mysql-jdbc-bugs)参照してください。

#### タイムアウト関連のパラメータ {#timeout-related-parameters}

TiDBは、以下のMySQL互換のタイムアウト制御パラメータを提供します。

-   `wait_timeout` ： Javaアプリケーションへの接続における非対話型アイドルタイムアウトを制御します。TiDB v5.4以降では、デフォルト値の`wait_timeout`は`28800`秒（8時間）です。v5.4より前のTiDBバージョンでは、デフォルト値は`0`で、タイムアウトは無制限です。
-   `interactive_timeout` ： Javaアプリケーションへの接続における対話型アイドルタイムアウトを制御します。デフォルト値は8時間です。
-   `max_execution_time` ：接続におけるSQL実行のタイムアウトを制御します。2 `SELECT`ステートメント（ `SELECT ... FOR UPDATE`を含む）に対してのみ有効です。デフォルト値は`0`で、接続が無限にビジー状態になることを許可します。つまり、SQLステートメントが無限に長い時間実行されます。

しかし、実際の本番環境では、アイドル状態の接続や実行時間が長すぎるSQL文は、データベースやアプリケーションに悪影響を及ぼします。アイドル状態の接続や実行時間が長すぎるSQL文を回避するには、アプリケーションの接続文字列でこれらの2つのパラメータを設定できます。例えば、 `sessionVariables=wait_timeout=3600` （1時間）と`sessionVariables=max_execution_time=300000` （5分）を設定します。

#### 一般的なJDBC接続文字列パラメータ {#typical-jdbc-connection-string-parameters}

上記のパラメータ値を組み合わせると、JDBC接続文字列の設定は次のようになります。

    jdbc:mysql://<IP_ADDRESS>:<PORT_NUMBER>/<DATABASE_NAME>?characterEncoding=UTF-8&useSSL=false&useServerPrepStmts=true&cachePrepStmts=true&prepStmtCacheSqlLimit=10000&prepStmtCacheSize=1000&useConfigs=maxPerformance&rewriteBatchedStatements=true

> **注記：**
>
> 公共ネットワーク経由で接続する場合は、 `useSSL=true`と[TiDBクライアントとサーバー間でTLSを有効にする](/enable-tls-between-clients-and-servers.md)設定する必要があります。

## 接続プール {#connection-pool}

TiDB（MySQL）接続の構築は、（少なくともOLTPシナリオにおいては）比較的コストがかかります。なぜなら、TCP接続の確立に加えて、接続認証も必要となるからです。そのため、クライアントは通常、TiDB（MySQL）接続を接続プールに保存して再利用します。

TiDBは以下のJava接続プールをサポートしています。

-   [HikariCP](https://github.com/brettwooldridge/HikariCP)
-   [トムキャットJDBC](https://tomcat.apache.org/tomcat-10.1-doc/jdbc-pool)
-   [druid](https://github.com/alibaba/druid)
-   [c3p0](https://www.mchange.com/projects/c3p0/)
-   [dbcp](https://commons.apache.org/proper/commons-dbcp/)

実際には、一部の接続プールは特定のセッションを継続的に使用する場合があります。TiDB の計算ノード全体で接続の総数は均等に分散されているように見えますが、アクティブな接続の分散が不均一な場合、実際の負荷の不均衡が生じる可能性があります。分散環境では、接続ライフサイクルを効果的に管理し、アクティブな接続が特定のノードに固定されるのを防ぎ、負荷分散のバランスを保つHikariCPの使用をお勧めします。

### 典型的な接続プール構成 {#typical-connection-pool-configuration}

以下はHikariCPの設定例です。

```yaml
hikari:
  maximumPoolSize: 20
  poolName: hikariCP
  connectionTimeout: 30000 
  maxLifetime: 1200000
  keepaliveTime: 120000
```

パラメータの説明は以下のとおりです。詳細については、 [HikariCPの公式ドキュメント](https://github.com/brettwooldridge/HikariCP/blob/dev/README.md)を参照してください。

-   `maximumPoolSize` ：プール内の最大接続数。デフォルト値は`10`です。コンテナ化された環境では、 Javaアプリケーションで使用可能なCPUコア数の4～10倍に設定することをお勧めします。この値を高く設定しすぎるとリソースの無駄遣いにつながり、低く設定しすぎると接続の取得が遅くなる可能性があります。詳細は[プールのサイズについて](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing)参照してください。
-   `minimumIdle` ： HikariCP、このパラメータを設定しないことを推奨します。デフォルト値は`maximumPoolSize`で、接続プールのスケーリングを無効にします。これにより、トラフィックの急増時にも接続がすぐに利用可能になり、接続作成による遅延を回避できます。
-   `connectionTimeout` ：アプリケーションが接続プールから接続を取得するために待機する最大時間（ミリ秒）。デフォルト値は`30000`ミリ秒（30秒）です。この時間内に利用可能な接続が得られない場合、例外`SQLException`が発生します。
-   `maxLifetime` ：接続プール内の接続の最大有効期間（ミリ秒）。デフォルト値は`1800000`ミリ秒（30分）です。使用中の接続には影響しません。接続が閉じられた後、この設定に従って削除されます。この値を低く設定しすぎると、再接続が頻繁に発生する可能性があります。4 [`graceful-wait-before-shutdown`](/tidb-configuration-file.md#graceful-wait-before-shutdown-new-in-v50)使用する場合は、この値が待機時間よりも小さいことを確認してください。
-   `keepaliveTime` : プール内の接続に対するキープアライブ操作の間隔（ミリ秒）。この設定は、データベースまたはネットワークのアイドルタイムアウトによる切断を防ぐのに役立ちます。デフォルト値は`120000`ミリ秒 (2 分) です。プールは、アイドル状態の接続を維持するために JDBC4 `isValid()`メソッドを使用することを優先します。

### プローブ構成 {#probe-configuration}

接続プールは、以下のようにクライアントからTiDBへの永続的な接続を維持します。

-   バージョン5.4より前のTiDBでは、デフォルトでは（エラーが報告されない限り）クライアント接続を積極的に閉じることはありません。
-   バージョン5.4以降、TiDBはデフォルトで`28800`秒間（つまり`8`時間）の非アクティブ状態が続くとクライアント接続を自動的に閉じます。このタイムアウト設定は、TiDBとMySQL互換の`wait_timeout`変数を使用して制御できます。詳細については、 [JDBCクエリタイムアウト](/develop/dev-guide-timeouts-in-tidb.md#jdbc-query-timeout)参照してください。

さらに、クライアントとTiDBの間には、 [LVS](https://en.wikipedia.org/wiki/Linux_Virtual_Server)や[HAProxy](https://en.wikipedia.org/wiki/HAProxy)ようなネットワークプロキシが存在する場合があります。これらのプロキシは通常、特定のアイドル期間（プロキシのアイドル設定によって決定されます）が経過すると、接続を自動的にクリーンアップします。接続プールは、プロキシのアイドル設定を監視するだけでなく、キープアライブのために接続を維持またはプローブする必要もあります。

Javaアプリケーションで以下のエラーが頻繁に発生する場合：

    The last packet sent successfully to the server was 3600000 milliseconds ago. The driver has not received any packets from the server. com.mysql.jdbc.exceptions.jdbc4.CommunicationsException: Communications link failure

`n`が`n milliseconds ago`または非常に`0`値の場合、通常は実行されたSQL操作によってTiDBが異常終了したことが原因です。原因を特定するには、TiDBの標準エラーログを確認することをお勧めします。

`n`が非常に大きな値 (上記の例の`3600000`など) の場合、この接続は長時間アイドル状態になり、中間プロキシによって閉じられた可能性が高いです。通常の解決策は、プロキシのアイドル設定の値を増やし、接続プールが次のことを実行できるようにすることです。

-   接続を使用する前に毎回接続が利用可能かどうかを確認してください。
-   別のスレッドを使用して、接続が利用可能かどうかを定期的に確認してください。
-   接続を維持するために、定期的にテストクエリを送信してください。

接続プールの実装によっては、上記の方法のうち1つ以上がサポートされている場合があります。対応する設定については、接続プールのドキュメントを参照してください。

## データアクセスフレームワーク {#data-access-framework}

アプリケーションは、データベースへのアクセスを簡素化するために、何らかのデータアクセスフレームワークを使用することが多い。

### MyBatis {#mybatis}

[MyBatis](http://www.mybatis.org/mybatis-3/)は、人気の高いJavaデータアクセスフレームワークです。主にSQLクエリの管理や、結果セットとJavaオブジェクト間のマッピングに使用されます。MyBatisはTiDBと高い互換性があり、過去の事例に基づくと、MyBatisで問題が発生することはほとんどありません。

この文書では、主に以下の構成に焦点を当てています。

#### マッパーパラメータ {#mapper-parameters}

MyBatis Mapperは2つのパラメータをサポートしています。

-   `select 1 from t where id = #{param1}`プリペアドステートメントとして`select 1 from t where id =?`に変換され、「準備済み」の状態となり、実際のパラメータは再利用されます。このパラメータを前述の接続準備パラメータと併用すると、最高のパフォーマンスが得られます。
-   テキストファイルでは、 `select 1 from t where id = ${param2}` `select 1 from t where id = 1`に置き換えられ、実行されます。このステートメントが異なるパラメータに置き換えられて実行されると、MyBatis はステートメントの「準備」のために TiDB に異なるリクエストを送信します。これにより、TiDB が多数のプリペアドステートメントをキャッシュする可能性があり、この方法で SQL 操作を実行すると、インジェクションによるセキュリティリスクが発生します。

#### 動的SQLバッチ {#dynamic-sql-batch}

[動的SQL - foreach](http://www.mybatis.org/mybatis-3/dynamic-sql.html#foreach)

複数の`INSERT`ステートメントを`insert ... values(...), (...), ...`の形式に自動的に書き換えることをサポートするために、前述のように JDBC で`rewriteBatchedStatements=true`設定することに加えて、MyBatis は動的 SQL を使用してバッチ挿入を半自動的に生成することもできます。次のマッパーを例にとります。

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

このマッパーは`insert on duplicate key update`ステートメントを生成します。それに続く`(?,?,?)`の「値」の数は、渡されたリストの数によって決まります。最終的な効果は`rewriteBatchStatements=true`使用した場合と同様で、クライアントとTiDB間の通信オーバーヘッドを効果的に削減します。

前述のとおり、プリペアドステートメントは最大長が`prepStmtCacheSqlLimit`を超えるとキャッシュされないことにも注意が必要です。

#### ストリーミング結果 {#streaming-result}

[前のセクション](#use-streamingresult-to-get-the-execution-result) 、JDBCで読み取り実行結果をストリーミングする方法を紹介します。JDBCの対応する設定に加えて、MyBatisで非常に大きな結果セットを読み取りたい場合は、次の点にも注意する必要があります。

-   マッパー設定で、単一のSQLステートメントに対して`fetchSize`設定できます（前のコードブロックを参照）。これはJDBCで`setFetchSize`呼び出すのと同等の効果があります。
-   クエリインターフェースで`ResultHandler`を指定すると、結果セット全体を一度に取得することを避けることができます。
-   ストリーム読み取りには、 `Cursor`クラスを使用できます。

XML を使用してマッピングを設定する場合、マッピングの`<select>`セクションで`fetchSize="-2147483648"` ( `Integer.MIN_VALUE` ) を設定することで、読み取り結果をストリーミングできます。

```xml
<select id="getAll" resultMap="postResultMap" fetchSize="-2147483648">
  select * from post;
</select>
```

コードを使用してマッピングを設定する場合は、 `@Options(fetchSize = Integer.MIN_VALUE)`アノテーションを追加し、結果のタイプを`Cursor`のままにしておくことで、SQL の結果をストリーミングで読み取ることができます。

```java
@Select("select * from post")
@Options(fetchSize = Integer.MIN_VALUE)
Cursor<Post> queryAllPost();
```

### <code>ExecutorType</code> {#code-executortype-code}

`openSession`選択肢の中から`ExecutorType`選ぶことができます。MyBatisは3種類の実行エンジンをサポートしています。

-   シンプル：プリペアドステートメントは、実行ごとにJDBCに呼び出されます（JDBC構成項目`cachePrepStmts`有効になっている場合、繰り返し実行されるプリペアドステートメントは再利用されます）。
-   再利用: 準備済みステートメントは`executor`にキャッシュされるため、JDBC `cachePrepStmts`を使用せずに準備済みステートメントの重複呼び出しを減らすことができます。
-   バッチ処理：各更新操作（ `INSERT` ） `UPDATE`まずバッチに追加され、トランザクションがコミットされるか、 `SELECT`クエリが実行されるまで実行されます。JDBCレイヤーで`rewriteBatchStatements` `DELETE`有効になっている場合は、ステートメントの書き換えが試みられます。そうでない場合は、ステートメントは1つずつ送信されます。

通常、デフォルト値`ExecutorType`は`Simple`です。7 `openSession`呼び出す場合は`ExecutorType`変更する必要があります。バッチ実行の場合、トランザクション内で`UPDATE`または`INSERT`ステートメントは非常に高速に実行されますが、データの読み取りやトランザクションのコミットは遅くなる場合があります。これは実際には正常な動作なので、SQLクエリの遅延をトラブルシューティングする際にはこの点に注意してください。

## 春のトランザクション {#spring-transaction}

現実世界では、アプリケーションはトランザクションを開始および停止するために、 [春のトランザクション](https://docs.spring.io/spring/docs/4.2.x/spring-framework-reference/html/transaction.html)とAOPの側面を使用する可能性があります。

メソッド定義にアノテーション`@Transactional`を追加することで、AOPはメソッドが呼び出される前にトランザクションを開始し、メソッドが結果を返す前にトランザクションをコミットします。アプリケーションで同様の要件がある場合は、コード内でトランザクションの開始と終了のタイミングを判断するためのアノテーション`@Transactional`見つけることができます。

埋め込みの特殊なケースに注意してください。それが発生した場合、Spring は[伝搬](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/transaction/annotation/Propagation.html)設定に基づいて異なる動作をします。

## その他 {#misc}

このセクションでは、 Javaで問題解決に役立つ便利なツールをいくつか紹介します。

### トラブルシューティングツール {#troubleshooting-tools}

Javaアプリケーションで問題が発生し、そのアプリケーションロジックが不明な場合は、JVMの強力なトラブルシューティングツールを使用することをお勧めします。以下に、よく使用されるツールをいくつか紹介します。

#### jstack {#jstack}

[jstack](https://docs.oracle.com/javase/7/docs/technotes/tools/share/jstack.html)は Go の pprof/goroutine に似ており、プロセスが停止する問題を簡単にトラブルシューティングできます。

`jstack pid`実行すると、対象プロセス内のすべてのスレッドの ID とスタック情報を出力できます。デフォルトでは、 Javaスタックのみが出力されます。JVM 内の C++ スタックも同時に出力したい場合は、 `-m`オプションを追加してください。

jstackを複数回使用することで、スタックしている問題（例えば、MybatisのBatch ExecutorTypeを使用しているためにアプリケーションビューからのクエリが遅い場合）やアプリケーションのデッドロック問題（例えば、アプリケーションがSQLステートメントを送信する前にロックをプリエンプトしているため、SQLステートメントを送信しない場合）を簡単に特定できます。

さらに、スレッドIDを確認するには、 `top -p $ PID -H`またはJavaスイスナイフが一般的な方法です。また、「スレッドが大量のCPUリソースを占有しているが、何を実行しているのか分からない」という問題を特定するには、次の手順を実行してください。

-   スレッドIDを16進数に変換するには、 `printf "%x\n" pid`使用してください。
-   jstackの出力結果を確認すると、対応するスレッドのスタック情報が表示されます。

#### jmap &amp; mat {#jmap-x26-mat}

Go の pprof/heap とは異なり、 [jmap](https://docs.oracle.com/javase/7/docs/technotes/tools/share/jmap.html)プロセス全体のメモリスナップショットをダンプし (Go ではディストリビュータのサンプリング)、その後スナップショットを別のツール[マット](https://www.eclipse.org/mat/)で分析できます。

mat を使用すると、プロセス内のすべてのオブジェクトに関連付けられた情報と属性を確認できるほか、スレッドの実行状態も監視できます。たとえば、mat を使用して、現在のアプリケーションに存在する MySQL 接続オブジェクトの数、および各接続オブジェクトのアドレスと状態情報を調べることができます。

matはデフォルトでは到達可能なオブジェクトのみを処理することに注意してください。ヤングGCの問題をトラブルシューティングしたい場合は、matの設定を調整して到達不可能なオブジェクトを表示できます。また、ヤングGCの問題（または多数の短命オブジェクト）のメモリ割り当てを調査するには、 Java Flight Recorderを使用する方が便利です。

#### トレース {#trace}

オンラインアプリケーションは通常、コードの変更をサポートしていませんが、 Javaで動的な計測を実行して問題箇所を特定することが求められる場合がよくあります。そのため、btraceやarthas traceを使用するのが良い選択肢となります。これらのツールは、アプリケーションプロセスを再起動することなく、トレースコードを動的に挿入できます。

#### 炎のグラフ {#flame-graph}

Javaアプリケーションでフレームグラフを取得するのは面倒です。詳細は[Java Flame Graphs入門：みんなのための炎！](http://psy-lob-saw.blogspot.com/2017/02/flamegraphs-intro-fire-for-everyone.html)参照してください。

## 結論 {#conclusion}

このドキュメントでは、データベースと連携する一般的なJavaコンポーネントに基づいて、TiDBを使用したJavaアプリケーション開発における一般的な問題点とその解決策について説明します。TiDBはMySQLプロトコルとの互換性が非常に高いため、MySQLベースのJavaアプリケーション開発におけるベストプラクティスのほとんどがTiDBにも適用できます。

## お困りですか？ {#need-help}

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 、または[サポートチケットを送信してください](/support.md)でコミュニティ[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)質問してください。
