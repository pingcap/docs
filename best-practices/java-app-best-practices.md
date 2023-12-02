---
title: Best Practices for Developing Java Applications with TiDB
summary: Learn the best practices for developing Java applications with TiDB.
---

# TiDB を使用したJavaアプリケーション開発のベスト プラクティス {#best-practices-for-developing-java-applications-with-tidb}

このドキュメントでは、TiDB をより効果的に使用するためのJavaアプリケーション開発のベスト プラクティスを紹介します。このドキュメントは、バックエンド TiDB データベースと対話するいくつかの一般的なJavaアプリケーション コンポーネントに基づいて、開発中によく発生する問題の解決策も提供します。

## Javaアプリケーションのデータベース関連コンポーネント {#database-related-components-in-java-applications}

Javaアプリケーションで TiDB データベースと対話する一般的なコンポーネントには次のものがあります。

-   ネットワーク プロトコル: クライアントは、標準[MySQLプロトコル](https://dev.mysql.com/doc/dev/mysql-server/latest/PAGE_PROTOCOL.html)を介して TiDBサーバーと対話します。
-   JDBC API と JDBC ドライバー: Javaアプリケーションは通常、標準の[JDBC (Javaデータベース接続)](https://docs.oracle.com/javase/8/docs/technotes/guides/jdbc/) API を使用してデータベースにアクセスします。 TiDB に接続するには、JDBC API 経由で MySQL プロトコルを実装する JDBC ドライバーを使用できます。このような MySQL 用の一般的な JDBC ドライバーには、 [MySQLコネクタ/J](https://github.com/mysql/mysql-connector-j)および[MariaDB コネクタ/J](https://mariadb.com/kb/en/library/about-mariadb-connector-j/#about-mariadb-connectorj)が含まれます。
-   データベース接続プール: 接続が要求されるたびに作成するオーバーヘッドを軽減するために、アプリケーションは通常、接続プールを使用して接続をキャッシュし、再利用します。 JDBC [情報元](https://docs.oracle.com/javase/8/docs/api/javax/sql/DataSource.html)は接続プール API を定義します。必要に応じて、さまざまなオープンソース接続プール実装から選択できます。
-   データ アクセス フレームワーク: アプリケーションは通常、 [マイバティス](https://mybatis.org/mybatis-3/index.html)や[休止状態](https://hibernate.org/)などのデータ アクセス フレームワークを使用して、データベース アクセス操作をさらに簡素化し、管理します。
-   アプリケーションの実装: アプリケーション ロジックは、いつどのコマンドをデータベースに送信するかを制御します。一部のアプリケーションは、トランザクションの開始ロジックとコミットロジックを管理するために[春のトランザクション](https://docs.spring.io/spring/docs/4.2.x/spring-framework-reference/html/transaction.html)アスペクトを使用します。

![Java application components](/media/best-practices/java-practice-1.png)

上の図から、 Javaアプリケーションが次のことを実行する可能性があることがわかります。

-   JDBC API を介して MySQL プロトコルを実装し、TiDB と対話します。
-   接続プールから永続的な接続を取得します。
-   MyBatis などのデータ アクセス フレームワークを使用して、SQL ステートメントを生成および実行します。
-   Spring トランザクション を使用して、トランザクションを自動的に開始または停止します。

このドキュメントの残りの部分では、上記のコンポーネントを使用してJavaアプリケーションを開発する場合の問題とその解決策について説明します。

## JDBC {#jdbc}

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

-   [`FetchSize` `Integer.MIN_VALUE`に設定します](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-implementation-notes.html#ResultSet)を指定すると、クライアントはキャッシュを行わなくなります。クライアントは`StreamingResult`を介してネットワーク接続から実行結果を読み取ります。

    クライアントがストリーミング読み取りメソッドを使用する場合、ステートメントを使用してクエリを作成し続ける前に、読み取りを完了するかクローズ`resultset`する必要があります。それ以外の場合は、エラー`No statements may be issued when any streaming result sets are open and in use on a given connection. Ensure that you have called .close() on any active streaming result sets before attempting more queries.`が返されます。

    クライアントが読み取りを完了するか、 `resultset`閉じる前にクエリでこのようなエラーが発生するのを回避するには、URL に`clobberStreamingResults=true`パラメータを追加します。その後、 `resultset`は自動的に閉じられますが、前のストリーミング クエリで読み取られる結果セットは失われます。

-   カーソルフェッチを使用するには、まず正の整数として[`FetchSize`を設定する](http://makejavafaster.blogspot.com/2015/06/jdbc-fetch-size-performance.html)を設定し、JDBC URL で`useCursorFetch=true`を設定します。

TiDB は両方の方法をサポートしていますが、最初の方法を使用することをお勧めします。これは、実装が単純で実行効率が高いためです。

### MySQL JDBC パラメータ {#mysql-jdbc-parameters}

JDBC は通常、実装関連の設定を JDBC URL パラメーターの形式で提供します。このセクションでは[MySQL Connector/J のパラメータ設定](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-configuration-properties.html)を紹介します (MariaDB を使用する場合は[MariaDBのパラメータ設定](https://mariadb.com/kb/en/library/about-mariadb-connector-j/#optional-url-parameters)を参照してください)。このドキュメントではすべての構成項目をカバーすることはできないため、パフォーマンスに影響を与える可能性のあるいくつかのパラメーターに主に焦点を当てています。

#### 関連パラメータの準備 {#prepare-related-parameters}

このセクションでは、 `Prepare`に関連するパラメータを紹介します。

##### <code>useServerPrepStmts</code> {#code-useserverprepstmts-code}

デフォルトでは`useServerPrepStmts`が`false`に設定されています。つまり、Prepare API を使用する場合でも、「準備」操作はクライアント上でのみ実行されます。同じ SQL ステートメントで Prepare API を複数回使用する場合、サーバーの解析オーバーヘッドを回避するには、この構成を`true`に設定することをお勧めします。

この設定がすでに有効になっていることを確認するには、次の操作を実行できます。

-   TiDB モニタリング ダッシュボードに移動し、 **[Query Summary]** &gt; **[CPS By Instance]**からリクエスト コマンド タイプを表示します。
-   リクエスト内で`COM_QUERY` `COM_STMT_EXECUTE`または`COM_STMT_PREPARE`に置き換えられている場合は、この設定がすでに有効になっていることを意味します。

##### <code>cachePrepStmts</code> {#code-cacheprepstmts-code}

`useServerPrepStmts=true`を指定すると、サーバーはプリペアド ステートメントを実行できますが、デフォルトでは、クライアントは各実行後にプリペアド ステートメントを閉じ、再利用しません。これは、「準備」操作がテキスト ファイルの実行ほど効率的ではないことを意味します。これを解決するには、 `useServerPrepStmts=true`設定した後、 `cachePrepStmts=true`も設定することをお勧めします。これにより、クライアントは Prepared Statement をキャッシュできるようになります。

この設定がすでに有効になっていることを確認するには、次の操作を実行できます。

-   TiDB モニタリング ダッシュボードに移動し、 **[Query Summary]** &gt; **[CPS By Instance]**からリクエスト コマンド タイプを表示します。
-   リクエスト内の`COM_STMT_EXECUTE`の数が`COM_STMT_PREPARE`の数よりはるかに多い場合、この設定はすでに有効になっていることを意味します。

さらに、 `useConfigs=maxPerformance`を設定すると、 `cachePrepStmts=true`を含む複数のパラメータが同時に設定されます。

##### <code>prepStmtCacheSqlLimit</code> {#code-prepstmtcachesqllimit-code}

`cachePrepStmts`を設定した後、 `prepStmtCacheSqlLimit`設定にも注意してください (デフォルト値は`256` )。この構成は、クライアントにキャッシュされるプリペアド ステートメントの最大長を制御します。

この最大長を超えるプリペアド ステートメントはキャッシュされないため、再利用できません。この場合、アプリケーションの実際の SQL 長に応じて、この構成の値を増やすことを検討できます。

次の場合は、この設定が小さすぎるかどうかを確認する必要があります。

-   TiDB モニタリング ダッシュボードに移動し、 **[Query Summary]** &gt; **[CPS By Instance]**からリクエスト コマンド タイプを表示します。
-   そして`cachePrepStmts=true`は設定されていますが、 `COM_STMT_PREPARE`は依然として`COM_STMT_EXECUTE`とほぼ同じであり、 `COM_STMT_CLOSE`存在することがわかります。

##### <code>prepStmtCacheSize</code> {#code-prepstmtcachesize-code}

`prepStmtCacheSize`キャッシュされる Prepared Statement の数を制御します (デフォルト値は`25` )。アプリケーションで多くの種類の SQL ステートメントを「準備」する必要があり、準備されたステートメントを再利用したい場合は、この値を増やすことができます。

この設定がすでに有効になっていることを確認するには、次の操作を実行できます。

-   TiDB モニタリング ダッシュボードに移動し、 **[Query Summary]** &gt; **[CPS By Instance]**からリクエスト コマンド タイプを表示します。
-   リクエスト内の`COM_STMT_EXECUTE`の数が`COM_STMT_PREPARE`の数よりはるかに多い場合、この設定はすでに有効になっていることを意味します。

#### バッチ関連パラメータ {#batch-related-parameters}

バッチ書き込みの処理中は、 `rewriteBatchedStatements=true`を構成することをお勧めします。 `addBatch()`または`executeBatch()`使用した後も、JDBC はデフォルトで SQL を 1 つずつ送信します。次に例を示します。

```java
pstmt = prepare("insert into t (a) values(?)");
pstmt.setInt(1, 10);
pstmt.addBatch();
pstmt.setInt(1, 11);
pstmt.addBatch();
pstmt.setInt(1, 12);
pstmt.executeBatch();
```

`Batch`メソッドが使用されていますが、TiDB に送信される SQL ステートメントは依然として個別の`INSERT`のステートメントです。

```sql
insert into t(a) values(10);
insert into t(a) values(11);
insert into t(a) values(12);
```

ただし、 `rewriteBatchedStatements=true`を設定すると、TiDB に送信される SQL ステートメントは単一の`INSERT`ステートメントになります。

```sql
insert into t(a) values(10),(11),(12);
```

`INSERT`ステートメントの書き換えでは、複数の「values」キーワードの後の値が SQL ステートメント全体に連結されることに注意してください。 `INSERT`のステートメントに他の相違点がある場合、次のように書き直すことはできません。

```sql
insert into t (a) values (10) on duplicate key update a = 10;
insert into t (a) values (11) on duplicate key update a = 11;
insert into t (a) values (12) on duplicate key update a = 12;
```

上記`INSERT`ステートメントを 1 つのステートメントに書き換えることはできません。しかし、3 つのステートメントを次のステートメントに変更すると、次のようになります。

```sql
insert into t (a) values (10) on duplicate key update a = values(a);
insert into t (a) values (11) on duplicate key update a = values(a);
insert into t (a) values (12) on duplicate key update a = values(a);
```

その後、書き換え要件を満たします。上記の`INSERT`ステートメントは、次の 1 つのステートメントに書き換えられます。

```sql
insert into t (a) values (10), (11), (12) on duplicate key update a = values(a);
```

バッチ更新中に 3 つ以上の更新があった場合、SQL ステートメントが書き換えられ、複数のクエリとして送信されます。これにより、クライアントからサーバーへのリクエストのオーバーヘッドが効果的に削減されますが、副作用として、生成される SQL ステートメントが大きくなります。例えば：

```sql
update t set a = 10 where id = 1; update t set a = 11 where id = 2; update t set a = 12 where id = 3;
```

さらに、 [クライアントのバグ](https://bugs.mysql.com/bug.php?id=96623)があるため、バッチ更新中に`rewriteBatchedStatements=true`と`useServerPrepStmts=true`を設定する場合は、このバグを回避するために`allowMultiQueries=true`パラメータも設定することをお勧めします。

#### パラメータを統合する {#integrate-parameters}

モニタリングを通じて、アプリケーションは TiDB クラスターに対して`INSERT`操作のみを実行しますが、冗長な`SELECT`のステートメントが多数あることに気づくかもしれません。通常、これは、JDBC が設定をクエリするためにいくつかの SQL ステートメント (例: `select @@session.transaction_read_only`を送信するために発生します。これらの SQL ステートメントは TiDB では役に立たないため、余分なオーバーヘッドを避けるために`useConfigs=maxPerformance`を構成することをお勧めします。

`useConfigs=maxPerformance`には構成のグループが含まれます。 MySQL Connector/J 8.0 および MySQL Connector/J 5.1 の詳細な設定を取得するには、それぞれ[mysql-コネクタ-j 8.0](https://github.com/mysql/mysql-connector-j/blob/release/8.0/src/main/resources/com/mysql/cj/configurations/maxPerformance.properties)と[mysql-コネクタ-j 5.1](https://github.com/mysql/mysql-connector-j/blob/release/5.1/src/com/mysql/jdbc/configs/maxPerformance.properties)を参照してください。

構成後、モニタリングをチェックして、 `SELECT`ステートメントの数が減少していることを確認できます。

#### タイムアウト関連のパラメータ {#timeout-related-parameters}

TiDB には、タイムアウトを制御する 2 つの MySQL 互換パラメータ`wait_timeout`と`max_execution_time`が用意されています。これら 2 つのパラメータは、それぞれJavaアプリケーションとの接続アイドル タイムアウトと接続での SQL 実行のタイムアウトを制御します。つまり、これらのパラメータは、TiDB とJavaアプリケーション間の接続の最長アイドル時間と最長ビジー時間を制御します。両方のパラメータのデフォルト値は`0`で、デフォルトでは接続が無限にアイドル状態および無限にビジー状態 (1 つの SQL ステートメントの実行時間が無限) になります。

ただし、実際の本番環境では、アイドル状態の接続や実行時間が長すぎる SQL ステートメントはデータベースやアプリケーションに悪影響を及ぼします。アイドル状態の接続や長時間実行される SQL ステートメントを回避するために、アプリケーションの接続文字列でこれら 2 つのパラメーターを構成できます。たとえば、 `sessionVariables=wait_timeout=3600` （1時間）と`sessionVariables=max_execution_time=300000` （5分）を設定します。

## 接続プール {#connection-pool}

TiDB (MySQL) 接続の構築は、TCP 接続の構築に加えて接続認証も必要となるため、(少なくとも OLTP シナリオでは) 比較的高価です。したがって、クライアントは通常、TiDB (MySQL) 接続を接続プールに保存して再利用します。

Java には、 [HikariCP](https://github.com/brettwooldridge/HikariCP) 、 [tomcat-jdbc](https://tomcat.apache.org/tomcat-10.1-doc/jdbc-pool.html) 、 [druid](https://github.com/alibaba/druid) 、 [c3p0](https://www.mchange.com/projects/c3p0/) 、 [dbcp](https://commons.apache.org/proper/commons-dbcp/)などの多くの接続プール実装があります。 TiDB は使用する接続プールを制限しないため、アプリケーションに合わせて好きなものを選択できます。

### 接続数を構成する {#configure-the-number-of-connections}

接続プールのサイズは、アプリケーション独自のニーズに応じて適切に調整されるのが一般的です。例として、 HikariCP を取り上げます。

-   `maximumPoolSize` : 接続プール内の最大接続数。この値が大きすぎる場合、TiDB は無駄な接続を維持するためにリソースを消費します。この値が小さすぎると、アプリケーションの接続が遅くなります。したがって、この値は自分のために設定してください。詳細は[プールのサイジングについて](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing)を参照してください。
-   `minimumIdle` : 接続プール内のアイドル接続の最小数。これは主に、アプリケーションがアイドル状態のときに突然のリクエストに応答するためにいくつかの接続を予約するために使用されます。アプリケーションのニーズに応じて構成することもできます。

アプリケーションは、使用を終了した後に接続を返す必要があります。また、アプリケーションが対応する接続​​プール監視 ( `metricRegistry`など) を使用して、接続プールの問題を適時に特定することもお勧めします。

### プローブの構成 {#probe-configuration}

接続プールは、TiDB への永続的な接続を維持します。 TiDB は、デフォルトでは (エラーが報告されない限り) クライアント接続を積極的に閉じませんが、通常はクライアントと TiDB の間に LVS や HAProxy などのネットワーク プロキシが存在します。通常、これらのプロキシは、(プロキシのアイドル構成によって制御されます) 一定期間アイドル状態の接続を積極的にクリーンアップします。プロキシのアイドル構成に注意を払うことに加えて、接続プールは接続を維持するか、接続をプローブする必要もあります。

Javaアプリケーションで次のエラーが頻繁に表示される場合:

    The last packet sent successfully to the server was 3600000 milliseconds ago. The driver has not received any packets from the server. com.mysql.jdbc.exceptions.jdbc4.CommunicationsException: Communications link failure

`n milliseconds ago`の`n`が`0`または非常に小さい値の場合、通常は、実行された SQL 操作によって TiDB が異常終了することが原因です。原因を見つけるには、TiDB stderr ログを確認することをお勧めします。

`n`が非常に大きな値 (上記の例の`3600000`など) である場合、この接続は長時間アイドル状態であり、その後中間プロキシによって閉じられた可能性があります。通常の解決策は、プロキシのアイドル構成の値を増やし、接続プールが次のことを行えるようにすることです。

-   接続を使用する前に毎回接続が利用可能かどうかを確認する
-   別のスレッドを使用して接続が利用可能かどうかを定期的に確認してください。
-   テストクエリを定期的に送信して接続を維持します

接続プールの実装が異なれば、上記の方法の 1 つ以上がサポートされる場合があります。接続プールのドキュメントを確認して、対応する構成を見つけることができます。

## データアクセスフレームワーク {#data-access-framework}

アプリケーションは多くの場合、データベース アクセスを簡素化するために、ある種のデータ アクセス フレームワークを使用します。

### マイバティス {#mybatis}

[マイバティス](http://www.mybatis.org/mybatis-3/)は、人気のあるJavaデータ アクセス フレームワークです。これは主に、SQL クエリを管理し、結果セットとJavaオブジェクト間のマッピングを完了するために使用されます。 MyBatis は TiDB と高い互換性があります。 MyBatis では、歴史的な問題に基づく問題が発生することはほとんどありません。

ここでは、このドキュメントでは主に次の構成に焦点を当てます。

#### マッパーパラメータ {#mapper-parameters}

MyBatis Mapper は 2 つのパラメータをサポートしています。

-   `select 1 from t where id = #{param1}`は Prepared Statement として`select 1 from t where id =?`に変換されて「準備」され、実パラメータが再利用されます。このパラメーターを前述の Prepare 接続パラメーターとともに使用すると、最高のパフォーマンスが得られます。
-   `select 1 from t where id = ${param2}`テキストファイルとして`select 1 from t where id = 1`に置き換えて実行します。このステートメントが別のパラメータに置き換えられて実行されると、MyBatis はステートメントを「準備」するためのさまざまなリクエストを TiDB に送信します。これにより、TiDB が大量のプリペアド ステートメントをキャッシュする可能性があり、この方法で SQL 操作を実行すると、インジェクションのセキュリティ リスクが発生します。

#### 動的SQLバッチ {#dynamic-sql-batch}

[動的SQL - foreach](http://www.mybatis.org/mybatis-3/dynamic-sql.html#foreach)

複数の`INSERT`ステートメントの`insert ... values(...), (...), ...`形式への自動書き換えをサポートするために、前述したように JDBC で`rewriteBatchedStatements=true`を構成することに加えて、MyBatis は動的 SQL を使用してバッチ挿入を半自動的に生成することもできます。次のマッパーを例として取り上げます。

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

このマッパーは`insert on duplicate key update`ステートメントを生成します。 「値」に続く`(?,?,?)`の数は、渡されたリストの数によって決まります。その最終的な効果は`rewriteBatchStatements=true`使用した場合と同様で、クライアントと TiDB 間の通信オーバーヘッドも効果的に削減されます。

前に述べたように、Prepared Statements の最大長が値`prepStmtCacheSqlLimit`を超えると、Prepared Statements はキャッシュされなくなることにも注意する必要があります。

#### ストリーミング結果 {#streaming-result}

[前のセクション](#use-streamingresult-to-get-the-execution-result)読み取り実行結果を JDBC でストリーミングする方法が紹介されています。 MyBatis で超大規模な結果セットを読み込む場合は、JDBC の対応する設定に加えて、次の点にも注意する必要があります。

-   マッパー構成内の単一の SQL ステートメントに`fetchSize`を設定できます (前のコード ブロックを参照)。その効果は、JDBC で`setFetchSize`呼び出すのと同じです。
-   クエリ インターフェイスを`ResultHandler`で使用すると、結果セット全体を一度に取得することを避けることができます。
-   `Cursor`クラスはストリーム読み取りに使用できます。

XML を使用してマッピングを構成する場合、マッピングの`<select>`セクションで`fetchSize="-2147483648"` ( `Integer.MIN_VALUE` ) を構成することで、読み取り結果をストリーミングできます。

```xml
<select id="getAll" resultMap="postResultMap" fetchSize="-2147483648">
  select * from post;
</select>
```

コードを使用してマッピングを構成する場合、 `@Options(fetchSize = Integer.MIN_VALUE)`アノテーションを追加し、結果のタイプを`Cursor`のままにして、SQL 結果をストリーミングで読み取れるようにすることができます。

```java
@Select("select * from post")
@Options(fetchSize = Integer.MIN_VALUE)
Cursor<Post> queryAllPost();
```

### <code>ExecutorType</code> {#code-executortype-code}

`openSession`の中で`ExecutorType`を選択できます。 MyBatis は 3 種類のエグゼキュータをサポートしています。

-   シンプル: 実行のたびにプリペアド ステートメントが JDBC に呼び出されます (JDBC 構成項目`cachePrepStmts`が有効な場合、繰り返されるプリペアド ステートメントが再利用されます)
-   再利用: プリペアド ステートメントは`executor`にキャッシュされるため、JDBC `cachePrepStmts`を使用せずにプリペアド ステートメントの重複呼び出しを減らすことができます。
-   バッチ: 各更新操作 ( `INSERT` / `DELETE` / `UPDATE` ) は最初にバッチに追加され、トランザクションがコミットされるか`SELECT`が実行されるまで実行されます。 JDBCレイヤーで`rewriteBatchStatements`が有効になっている場合、ステートメントの書き換えが試行されます。そうでない場合は、明細書が 1 つずつ送信されます。

通常、デフォルト値の`ExecutorType`は`Simple`です。 `openSession`を呼び出すときは`ExecutorType`を変更する必要があります。バッチ実行の場合、トランザクションでは`UPDATE`または`INSERT`のステートメントがかなり高速に実行されますが、データの読み取りやトランザクションのコミット時には遅くなることがわかります。これは実際には正常な現象であるため、遅い SQL クエリのトラブルシューティングを行う場合は、これに注意する必要があります。

## 春のトランザクション {#spring-transaction}

現実の世界では、アプリケーションは[春のトランザクション](https://docs.spring.io/spring/docs/4.2.x/spring-framework-reference/html/transaction.html)および AOP アスペクトを使用してトランザクションを開始および停止する場合があります。

`@Transactional`アノテーションをメソッド定義に追加すると、AOP はメソッドが呼び出される前にトランザクションを開始し、メソッドが結果を返す前にトランザクションをコミットします。アプリケーションでも同様のニーズがある場合は、コード内で`@Transactional`見つけて、トランザクションの開始時と終了時を決定できます。

埋め込みの特殊なケースに注意してください。これが発生すると、Spring は[伝搬](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/transaction/annotation/Propagation.html)設定に基づいて異なる動作をします。

## その他 {#misc}

このセクションでは、問題のトラブルシューティングに役立つJava用の便利なツールをいくつか紹介します。

### トラブルシューティングツール {#troubleshooting-tools}

Javaアプリケーションで問題が発生し、アプリケーション ロジックがわからない場合は、JVM の強力なトラブルシューティング ツールを使用することをお勧めします。以下に一般的なツールをいくつか示します。

#### jスタック {#jstack}

[jスタック](https://docs.oracle.com/javase/7/docs/technotes/tools/share/jstack.html)は Go の pprof/goroutine に似ており、プロセスのスタック問題を簡単にトラブルシューティングできます。

`jstack pid`を実行すると、対象プロセス内の全スレッドのIDとスタック情報を出力できます。デフォルトでは、 Javaスタックのみが出力されます。 JVM 内の C++ スタックも同時に出力したい場合は、 `-m`オプションを追加します。

jstack を複数回使用すると、スタックした問題 (たとえば、Mybatis で Batch ExecutorType を使用するためにアプリケーションのビューからのクエリが遅い) やアプリケーションのデッドロックの問題 (たとえば、アプリケーションが SQL ステートメントを送信しないなど) を簡単に特定できます。送信する前にロックをプリエンプトします)。

さらに、スレッド ID を表示するには、 `top -p $ PID -H`またはJavaスイスナイフが一般的な方法です。また、「スレッドが多くの CPU リソースを占有しており、何を実行しているのかわからない」という問題を特定するには、次の手順を実行します。

-   スレッド ID を 16 進数に変換するには、 `printf "%x\n" pid`を使用します。
-   jstack 出力に移動して、対応するスレッドのスタック情報を見つけます。

#### jmapとマット {#jmap-x26-mat}

Go の pprof/heap とは異なり、プロセス全体のメモリスナップショット (Go ではディストリビュータのサンプリング) を[jmap](https://docs.oracle.com/javase/7/docs/technotes/tools/share/jmap.html)し、そのスナップショットを別のツールで分析できます[マット](https://www.eclipse.org/mat/) 。

mat を通じて、プロセス内のすべてのオブジェクトの関連情報と属性を確認でき、スレッドの実行ステータスを観察することもできます。たとえば、mat を使用すると、現在のアプリケーションに存在する MySQL 接続オブジェクトの数と、各接続オブジェクトのアドレスとステータス情報を確認できます。

デフォルトでは、マットは到達可能なオブジェクトのみを処理することに注意してください。若い GC の問題をトラブルシューティングしたい場合は、マット構成を調整して、到達不能なオブジェクトを表示できます。さらに、若い GC の問題 (または多数の存続期間の短いオブジェクト) のメモリ割り当てを調査するには、 Java Flight Recorder を使用する方が便利です。

#### 痕跡 {#trace}

オンライン アプリケーションは通常、コードの変更をサポートしていませんが、問題を特定するためにJavaで動的インストルメンテーションを実行することが望まれることがよくあります。したがって、btrace または arthas トレースを使用することは良い選択肢です。アプリケーション プロセスを再起動せずに、トレース コードを動的に挿入できます。

#### フレームグラフ {#flame-graph}

Javaアプリケーションでフレーム グラフを取得するのは面倒です。詳細は[Java Flame Graphs の概要: Fire ForEveryone!](http://psy-lob-saw.blogspot.com/2017/02/flamegraphs-intro-fire-for-everyone.html)を参照してください。

## 結論 {#conclusion}

このドキュメントでは、データベースと対話する一般的に使用されるJavaコンポーネントに基づいて、TiDB を使用したJavaアプリケーションの開発に関する一般的な問題と解決策について説明します。 TiDB は MySQL プロトコルと高い互換性があるため、MySQL ベースのJavaアプリケーションのベスト プラクティスのほとんどが TiDB にも適用されます。

[TiDB コミュニティのスラック チャンネル](https://tidbcommunity.slack.com/archives/CH7TTLL7P)に参加して、TiDB でJavaアプリケーションを開発する際の経験や問題について幅広い TiDB ユーザー グループと共有してください。
