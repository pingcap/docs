---
title: Best Practices for Developing Java Applications with TiDB
summary: このドキュメントでは、TiDB を使用したJavaアプリケーション開発のベストプラクティスを紹介します。データベース関連コンポーネント、JDBC の使用、接続プールの設定、データアクセスフレームワーク、Spring トランザクション、トラブルシューティングツールなどについて解説します。TiDB は MySQL と高い互換性があるため、MySQL ベースのJavaアプリケーションのベストプラクティスのほとんどは TiDB にも適用できます。
aliases: ['/ja/tidb/stable/java-app-best-practices/']
---

# TiDB を使用したJavaアプリケーション開発のベスト プラクティス {#best-practices-for-developing-java-applications-with-tidb}

このドキュメントでは、TiDBをより有効に活用するためのJavaアプリケーション開発のベストプラクティスを紹介します。バックエンドのTiDBデータベースとやり取りする一般的なJavaアプリケーションコンポーネントに基づいて、開発中によく発生する問題への解決策も提供します。

## Javaアプリケーションのデータベース関連コンポーネント {#database-related-components-in-java-applications}

Javaアプリケーションで TiDB データベースと対話する一般的なコンポーネントは次のとおりです。

-   ネットワーク プロトコル: クライアントは標準[MySQLプロトコル](https://dev.mysql.com/doc/dev/mysql-server/latest/PAGE_PROTOCOL.html)を介して TiDBサーバーと対話します。
-   JDBC APIとJDBCドライバ： Javaアプリケーションは通常、標準の[JDBC (Javaデータベース接続)](https://docs.oracle.com/javase/8/docs/technotes/guides/jdbc/) APIを使用してデータベースにアクセスします。TiDBに接続するには、JDBC APIを介してMySQLプロトコルを実装したJDBCドライバを使用できます。MySQL用の一般的なJDBCドライバには、 [MySQL コネクタ/J](https://github.com/mysql/mysql-connector-j)と[MariaDB コネクタ/J](https://mariadb.com/docs/connectors/mariadb-connector-j/about-mariadb-connector-j#about-mariadb-connectorj)あります。
-   データベース接続プール：接続が要求されるたびに作成するオーバーヘッドを削減するため、アプリケーションは通常、接続プールを使用して接続をキャッシュし、再利用します。JDBC [データソース](https://docs.oracle.com/javase/8/docs/api/javax/sql/DataSource.html)では接続プールAPIが定義されています。必要に応じて、様々なオープンソースの接続プール実装から選択できます。
-   データ アクセス フレームワーク: アプリケーションは通常、 [マイバティス](https://mybatis.org/mybatis-3/index.html)や[休止状態](https://hibernate.org/)などのデータ アクセス フレームワークを使用して、データベース アクセス操作をさらに簡素化および管理します。
-   アプリケーション実装：アプリケーションロジックは、データベースにどのコマンドをいつ送信するかを制御します。一部のアプリケーションでは、トランザクションの開始とコミットのロジックを管理するために[春のトランザクション](https://docs.spring.io/spring/docs/4.2.x/spring-framework-reference/html/transaction.html)アスペクトを使用します。

![Java application components](/media/best-practices/java-practice-1.png)

上の図から、 Javaアプリケーションが次のことを実行する可能性があることがわかります。

-   TiDB と対話するために、JDBC API を介して MySQL プロトコルを実装します。
-   接続プールから永続的な接続を取得します。
-   MyBatis などのデータ アクセス フレームワークを使用して、SQL ステートメントを生成および実行します。
-   Spring トランザクションを使用して、トランザクションを自動的に開始または停止します。

このドキュメントの残りの部分では、上記のコンポーネントを使用してJavaアプリケーションを開発する際に発生する問題とその解決策について説明します。

## JDBC {#jdbc}

Javaアプリケーションは様々なフレームワークでカプセル化されたできます。ほとんどのフレームワークでは、データベースサーバーとやり取りするために最下層でJDBC APIが呼び出されます。JDBCでは、以下の点に重点を置くことをお勧めします。

-   JDBC APIの使用選択
-   API実装者のパラメータ設定

### JDBC API {#jdbc-api}

JDBC APIの使用方法については、 [JDBC公式チュートリアル](https://docs.oracle.com/javase/tutorial/jdbc/)参照してください。このセクションでは、いくつかの重要なAPIの使用方法について説明します。

#### 準備APIを使用する {#use-prepare-api}

OLTP（オンライントランザクション処理）シナリオでは、プログラムからデータベースに送信されるSQL文は複数の種類に分かれており、パラメータの変更を取り除いた後には使い尽くされてしまう可能性があります。そのため、通常の[テキストファイルからの実行](https://docs.oracle.com/javase/tutorial/jdbc/basics/processingsqlstatements.html#executing_queries)ではなく[準備された声明](https://docs.oracle.com/javase/tutorial/jdbc/basics/prepared.html)使用し、Prepared Statementを再利用して直接実行することをお勧めします。これにより、TiDBでSQL実行プランを繰り返し解析および生成するオーバーヘッドを回避できます。

現在、上位フレームワークのほとんどはSQL実行時にPrepare APIを呼び出します。開発でJDBC APIを直接使用する場合は、Prepare APIを選択する際に注意してください。

また、MySQL Connector/J のデフォルト実装では、クライアント側のステートメントのみが前処理され、クライアント側で`?`が置換された後、テキストファイルでサーバーに送信されます。そのため、TiDBサーバーでステートメントの前処理を行う前に、Prepare API の使用に加えて、JDBC 接続パラメータの`useServerPrepStmts = true`設定する必要があります。詳細なパラメータ設定については、 [MySQL JDBCパラメータ](#mysql-jdbc-parameters)参照してください。

#### バッチAPIを使用する {#use-batch-api}

バッチ挿入の場合は、 [`addBatch` / `executeBatch` API](https://www.tutorialspoint.com/jdbc/jdbc-batch-processing)を使用できます。3 `addBatch()`方法は、複数のSQL文をまずクライアント側でキャッシュし、 `executeBatch`方法を呼び出したときにそれらをまとめてデータベースサーバーに送信するために使用されます。

> **注記：**
>
> MySQL Connector/Jのデフォルトの実装では、 `addBatch()`でバッチに追加されたSQL文の送信は`executeBatch()`が呼び出された時点まで遅延されますが、実際のネットワーク転送では文は1つずつ送信されます。そのため、この方法では通常、通信オーバーヘッドは削減されません。
>
> バッチネットワーク転送を行う場合は、JDBC接続パラメータの`rewriteBatchedStatements = true`設定する必要があります。詳細なパラメータ設定については、 [バッチ関連のパラメータ](#batch-related-parameters)参照してください。

#### <code>StreamingResult</code>を使用して実行結果を取得します {#use-code-streamingresult-code-to-get-the-execution-result}

多くの場合、JDBCは実行効率を向上させるために、クエリ結果を事前に取得し、デフォルトでクライアントメモリに保存します。しかし、クエリが返す結果セットが非常に大きい場合、クライアントはデータベースサーバーに一度に返されるレコード数を減らすよう要求し、クライアントのメモリが準備できて次のバッチを要求するまで待機することがよくあります。

JDBC では通常、次の 2 つの処理方法が使用されます。

-   最初の方法： [`FetchSize`を`Integer.MIN_VALUE`に設定する](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-implementation-notes.html#ResultSet)クライアントがキャッシュしないようにします。クライアントは`StreamingResult`を介してネットワーク接続から実行結果を読み取ります。

    クライアントがストリーミング読み取り方式を使用する場合、クエリを実行するためにステートメントを続行する前に、読み取りを完了するか、 `resultset`閉じる必要があります。そうでない場合は、エラー`No statements may be issued when any streaming result sets are open and in use on a given connection. Ensure that you have called .close() on any active streaming result sets before attempting more queries.`が返されます。

    クライアントが読み取りを完了するか`resultset`閉じる前にクエリでこのようなエラーが発生するのを回避するには、URL に`clobberStreamingResults=true`パラメータを追加します。これにより、 `resultset`自動的に閉じられますが、前のストリーミングクエリで読み取られるべき結果セットは失われます。

-   2 番目の方法: 最初に[`FetchSize`設定](http://makejavafaster.blogspot.com/2015/06/jdbc-fetch-size-performance.html)正の整数として設定し、次に JDBC URL で`useCursorFetch = true`設定してカーソル フェッチを使用します。

TiDB は両方の方法をサポートしていますが、実装が簡単で実行効率が優れているため、 `FetchSize`を`Integer.MIN_VALUE`に設定する最初の方法を使用することをお勧めします。

2番目の方法では、TiDBはまずすべてのデータをTiDBノードにロードし、その後`FetchSize`に従ってクライアントにデータを返します。そのため、通常は1番目の方法よりも多くのメモリを消費します。3 [`tidb_enable_tmp_storage_on_oom`](/system-variables.md#tidb_enable_tmp_storage_on_oom) `ON`設定した場合、TiDBは結果を一時的にハードディスクに書き込む可能性があります。

[`tidb_enable_lazy_cursor_fetch`](/system-variables.md#tidb_enable_lazy_cursor_fetch-new-in-v830)システム変数を`ON`に設定すると、TiDB はクライアントがデータを取得する際にのみデータの一部を読み取ろうとするため、メモリ使用量が少なくなります。詳細と制限事項については、 [`tidb_enable_lazy_cursor_fetch`システム変数の完全な説明](/system-variables.md#tidb_enable_lazy_cursor_fetch-new-in-v830)をご覧ください。

### MySQL JDBCパラメータ {#mysql-jdbc-parameters}

JDBCは通常、実装関連の設定をJDBC URLパラメータの形で提供します。このセクションでは[MySQL Connector/Jのパラメータ設定](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-configuration-properties.html)について説明します（MariaDBをご利用の場合は[MariaDBのパラメータ設定](https://mariadb.com/docs/connectors/mariadb-connector-j/about-mariadb-connector-j#optional-url-parameters)参照してください）。このドキュメントではすべての設定項目を網羅することはできないため、主にパフォーマンスに影響を与える可能性のあるいくつかのパラメータに焦点を当てます。

#### 準備関連のパラメータ {#prepare-related-parameters}

このセクションでは、 `Prepare`に関連するパラメータを紹介します。

##### <code>useServerPrepStmts</code> {#code-useserverprepstmts-code}

デフォルトでは`useServerPrepStmts`は`false`に設定されています。つまり、Prepare API を使用した場合でも、「準備」操作はクライアント側でのみ実行されます。サーバーの解析オーバーヘッドを回避するため、同じ SQL 文で Prepare API を複数回使用する場合は、この設定を`true`に設定することをお勧めします。

この設定がすでに有効になっていることを確認するには、次の操作を実行します。

-   TiDB 監視ダッシュボードに移動し、**クエリ サマリー**&gt;**インスタンス別の CPS**を通じて要求コマンド タイプを表示します。
-   リクエスト内の`COM_QUERY` `COM_STMT_EXECUTE`または`COM_STMT_PREPARE`に置き換えられた場合、この設定は既に有効になっていることを意味します。

##### <code>cachePrepStmts</code> {#code-cacheprepstmts-code}

`useServerPrepStmts=true`ではサーバーがプリペアドステートメントを実行できますが、デフォルトではクライアントはプリペアドステートメントを毎回実行した後に閉じ、再利用しません。つまり、「準備」操作はテキストファイルの実行ほど効率的ではありません。この問題を解決するには、 `useServerPrepStmts=true`設定した後、 `cachePrepStmts=true`設定することをお勧めします。これにより、クライアントはプリペアドステートメントをキャッシュできるようになります。

この設定がすでに有効になっていることを確認するには、次の操作を実行します。

-   TiDB 監視ダッシュボードに移動し、**クエリ サマリー**&gt;**インスタンス別の CPS**を通じて要求コマンド タイプを表示します。
-   リクエスト内の`COM_STMT_EXECUTE`の数が`COM_STMT_PREPARE`の数よりはるかに多い場合、この設定はすでに有効になっていることを意味します。

また、 `useConfigs=maxPerformance`設定すると、 `cachePrepStmts=true`含む複数のパラメータが同時に設定されます。

##### <code>prepStmtCacheSqlLimit</code> {#code-prepstmtcachesqllimit-code}

`cachePrepStmts`設定した後は、 `prepStmtCacheSqlLimit`設定にも注意してください（デフォルト値は`256`です）。この設定は、クライアントにキャッシュされるプリペアドステートメントの最大長を制御します。

この最大長を超えるプリペアドステートメントはキャッシュされないため、再利用できません。この場合、アプリケーションの実際のSQLの長さに応じて、この設定の値を増やすことを検討してください。

次の場合は、この設定が小さすぎないかどうかを確認する必要があります。

-   TiDB 監視ダッシュボードに移動し、**クエリ サマリー**&gt;**インスタンス別の CPS**を通じて要求コマンド タイプを表示します。
-   そして、 `cachePrepStmts=true`設定されていることがわかりますが、 `COM_STMT_PREPARE`はまだ`COM_STMT_EXECUTE`とほぼ同じで、 `COM_STMT_CLOSE`存在します。

##### <code>prepStmtCacheSize</code> {#code-prepstmtcachesize-code}

`prepStmtCacheSize`キャッシュされるプリペアドステートメントの数を制御します（デフォルト値は`25`です）。アプリケーションで多くの種類のSQL文を「準備」する必要があり、プリペアドステートメントを再利用したい場合は、この値を増やすことができます。

この設定がすでに有効になっていることを確認するには、次の操作を実行します。

-   TiDB 監視ダッシュボードに移動し、**クエリ サマリー**&gt;**インスタンス別の CPS**を通じて要求コマンド タイプを表示します。
-   リクエスト内の`COM_STMT_EXECUTE`の数が`COM_STMT_PREPARE`の数よりはるかに多い場合、この設定はすでに有効になっていることを意味します。

#### バッチ関連のパラメータ {#batch-related-parameters}

バッチ書き込み処理中は、 `rewriteBatchedStatements=true`設定することをお勧めします。 `addBatch()`または`executeBatch()`を使用した後でも、JDBCはデフォルトでSQLを1つずつ送信します。例：

```java
pstmt = prepare("insert into t (a) values(?)");
pstmt.setInt(1, 10);
pstmt.addBatch();
pstmt.setInt(1, 11);
pstmt.addBatch();
pstmt.setInt(1, 12);
pstmt.executeBatch();
```

`Batch`方法が使用されていますが、TiDB に送信される SQL ステートメントは個別の`INSERT`ステートメントのままです。

```sql
insert into t(a) values(10);
insert into t(a) values(11);
insert into t(a) values(12);
```

ただし、 `rewriteBatchedStatements=true`設定すると、TiDB に送信される SQL ステートメントは単一の`INSERT`ステートメントになります。

```sql
insert into t(a) values(10),(11),(12);
```

`INSERT`番目の文の書き換えは、複数の「values」キーワードの後の値を連結して、1 つの SQL 文にまとめるというものです。3 `INSERT`文に他の違いがある場合は、書き換えることはできません。例えば、次のようになります。

```sql
insert into t (a) values (10) on duplicate key update a = 10;
insert into t (a) values (11) on duplicate key update a = 11;
insert into t (a) values (12) on duplicate key update a = 12;
```

上記の`INSERT`の文を1つの文に書き直すことはできません。しかし、3つの文を次のように書き換えると、

```sql
insert into t (a) values (10) on duplicate key update a = values(a);
insert into t (a) values (11) on duplicate key update a = values(a);
insert into t (a) values (12) on duplicate key update a = values(a);
```

すると、書き換え要件を満たします。上記の`INSERT`つの文は、次の1つの文に書き換えられます。

```sql
insert into t (a) values (10), (11), (12) on duplicate key update a = values(a);
```

バッチ更新中に3つ以上の更新が発生した場合、SQL文は書き換えられ、複数のクエリとして送信されます。これにより、クライアントからサーバーへのリクエストのオーバーヘッドは効果的に削減されますが、副作用として生成されるSQL文のサイズが大きくなります。例えば、次のようになります。

```sql
update t set a = 10 where id = 1; update t set a = 11 where id = 2; update t set a = 12 where id = 3;
```

また、 [クライアントのバグ](https://bugs.mysql.com/bug.php?id=96623)ため、バッチ更新中に`rewriteBatchedStatements=true`と`useServerPrepStmts=true`を設定する場合は、このバグを回避するために`allowMultiQueries=true`パラメータも設定することをお勧めします。

#### パラメータを統合する {#integrate-parameters}

監視中に、アプリケーションがTiDBクラスタに対して`INSERT`操作しか実行していないにもかかわらず、冗長な`SELECT`ステートメントが多数存在することに気付く場合があります。これは通常、JDBCが設定を照会するためにいくつかのSQLステートメント（例えば`select @@session.transaction_read_only`を送信するために発生します。これらのSQLステートメントはTiDBには役に立たないため、余分なオーバーヘッドを回避するために`useConfigs=maxPerformance`に設定することをお勧めします。

`useConfigs=maxPerformance`には一連の設定が含まれています。MySQL Connector/J 8.0とMySQL Connector/J 5.1の詳細な設定については、それぞれ[mysql-コネクタ-j 8.0](https://github.com/mysql/mysql-connector-j/blob/release/8.0/src/main/resources/com/mysql/cj/configurations/maxPerformance.properties)と[mysql-コネクタ-j 5.1](https://github.com/mysql/mysql-connector-j/blob/release/5.1/src/com/mysql/jdbc/configs/maxPerformance.properties)参照してください。

設定後、監視をチェックして、 `SELECT`ステートメントの数が減っていることを確認できます。

> **注記：**
>
> `useConfigs=maxPerformance`を有効にするには、MySQL Connector/J バージョン 8.0.33 以降が必要です。詳細については[MySQL JDBC バグ](/develop/dev-guide-third-party-tools-compatibility.md#mysql-jdbc-bugs)参照してください。

#### タイムアウト関連のパラメータ {#timeout-related-parameters}

TiDB は、次の MySQL 互換のタイムアウト制御パラメータを提供します。

-   `wait_timeout` : Javaアプリケーションへの接続における非対話型アイドルタイムアウトを制御します。TiDB v5.4以降では、デフォルト値は`wait_timeout`で、これは`28800`秒（8時間）です。TiDB v5.4より前のバージョンでは、デフォルト値は`0`で、これはタイムアウトが無制限であることを意味します。
-   `interactive_timeout` : Javaアプリケーションへの接続における対話型アイドルタイムアウトを制御します。デフォルト値は8時間です。
-   `max_execution_time` : 接続におけるSQL実行のタイムアウトを制御します。2文（ `SELECT` `SELECT ... FOR UPDATE`を含む）の場合のみ有効です。デフォルト値は`0`で、接続が無限にビジー状態になることを許可します。つまり、SQL文が無限に長い時間実行されます。

しかし、実際の本番環境では、アイドル接続や実行時間が長すぎるSQL文は、データベースやアプリケーションに悪影響を及ぼします。アイドル接続や実行時間が長すぎるSQL文を回避するには、アプリケーションの接続文字列でこれらの2つのパラメータを設定できます。例えば、 `sessionVariables=wait_timeout=3600` （1時間）と`sessionVariables=max_execution_time=300000` （5分）を設定します。

#### 一般的なJDBC接続文字列パラメータ {#typical-jdbc-connection-string-parameters}

上記のパラメータ値を組み合わせると、JDBC 接続文字列の構成は次のようになります。

    jdbc:mysql://<IP_ADDRESS>:<PORT_NUMBER>/<DATABASE_NAME>?characterEncoding=UTF-8&useSSL=false&useServerPrepStmts=true&cachePrepStmts=true&prepStmtCacheSqlLimit=10000&prepStmtCacheSize=1000&useConfigs=maxPerformance&rewriteBatchedStatements=true

> **注記：**
>
> パブリックネットワーク経由で接続する場合は、 `useSSL=true`と[TiDBクライアントとサーバー間のTLSを有効にする](/enable-tls-between-clients-and-servers.md)設定する必要があります。

## 接続プール {#connection-pool}

TiDB (MySQL) 接続の構築は、TCP 接続の構築に加えて接続認証も必要となるため、比較的コストがかかります（少なくとも OLTP シナリオでは）。そのため、クライアントは通常、TiDB (MySQL) 接続を接続プールに保存し、再利用できるようにします。

TiDB は次のJava接続プールをサポートしています。

-   [HikariCP](https://github.com/brettwooldridge/HikariCP)
-   [tomcat-jdbc](https://tomcat.apache.org/tomcat-10.1-doc/jdbc-pool)
-   [druid](https://github.com/alibaba/druid)
-   [c3p0](https://www.mchange.com/projects/c3p0/)
-   [dbcp](https://commons.apache.org/proper/commons-dbcp/)

実際には、一部の接続プールは特定のアクティブセッションを永続的に使用する場合があります。接続の総数はTiDBコンピューティングノード間で均等に分散されているように見えますが、アクティブ接続の不均一な分散は、実際の負荷の不均衡につながる可能性があります。分散シナリオでは、接続ライフサイクルを効果的に管理し、アクティブ接続が特定のノードに固定されるのを防ぎ、バランスの取れた負荷分散を実現するHikariCPの使用をお勧めします。

### 一般的な接続プールの構成 {#typical-connection-pool-configuration}

以下は、 HikariCPの設定例です。

```yaml
hikari:
  maximumPoolSize: 20
  poolName: hikariCP
  connectionTimeout: 30000 
  maxLifetime: 1200000
  keepaliveTime: 120000
```

パラメータの説明は以下のとおりです。詳細については[HikariCP公式ドキュメント](https://github.com/brettwooldridge/HikariCP/blob/dev/README.md)を参照してください。

-   `maximumPoolSize` : プール内の最大接続数。デフォルト値は`10`です。コンテナ環境では、 Javaアプリケーションで利用可能なCPUコア数の4～10倍に設定することをお勧めします。この値を高く設定しすぎるとリソースの無駄遣いにつながる可能性があり、低く設定しすぎると接続の取得が遅くなる可能性があります。詳細は[プールのサイズについて](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing)参照してください。
-   `minimumIdle` : HikariCP、このパラメータの設定を推奨しません。デフォルト値は`maximumPoolSize`で、接続プールのスケーリングは無効になります。これにより、トラフィックの急増時でも接続が常に利用可能になり、接続作成による遅延を回避できます。
-   `connectionTimeout` : アプリケーションがプールから接続を取得するまでの最大待機時間（ミリ秒単位）。デフォルト値は`30000`ミリ秒（30秒）です。この時間内に利用可能な接続を取得できない場合は、例外`SQLException`が発生します。
-   `maxLifetime` : プール内の接続の最大存続時間（ミリ秒単位）。デフォルト値は`1800000`ミリ秒（30 分）です。使用中の接続は影響を受けません。接続が閉じられた後、この設定に従って削除されます。この値が低すぎると、再接続が頻繁に発生する可能性があります。4 [`graceful-wait-before-shutdown`](/tidb-configuration-file.md#graceful-wait-before-shutdown-new-in-v50)使用する場合は、この値が待機時間よりも小さいことを確認してください。
-   `keepaliveTime` : プール内の接続に対するキープアライブ操作の間隔（ミリ秒単位）。この設定は、データベースまたはネットワークのアイドルタイムアウトによる切断を防ぐのに役立ちます。デフォルト値は`120000`ミリ秒（2分）です。プールは、アイドル接続を維持するためにJDBC4 `isValid()`方式を優先的に使用します。

### プローブ構成 {#probe-configuration}

接続プールは、次のようにクライアントから TiDB への永続的な接続を維持します。

-   v5.4 より前では、TiDB はデフォルトでクライアント接続を積極的に閉じません (エラーが報告されない限り)。
-   バージョン5.4以降、TiDBはデフォルトで`28800`秒（つまり`8`時間）の非アクティブ状態が続くとクライアント接続を自動的に閉じます。このタイムアウト設定は、TiDBとMySQL互換の`wait_timeout`変数を使用して制御できます。詳細については、 [JDBCクエリタイムアウト](/develop/dev-guide-timeouts-in-tidb.md#jdbc-query-timeout)参照してください。

さらに、クライアントとTiDBの間には、 [LVS](https://en.wikipedia.org/wiki/Linux_Virtual_Server)や[HAプロキシ](https://en.wikipedia.org/wiki/HAProxy)ようなネットワークプロキシが存在する場合があります。これらのプロキシは通常、一定のアイドル時間（プロキシのアイドル設定によって決定されます）が経過すると、接続をプロアクティブにクリーンアップします。プロキシのアイドル設定を監視するだけでなく、接続プールはキープアライブのために接続を維持またはプローブする必要があります。

Javaアプリケーションで次のエラーが頻繁に表示される場合:

    The last packet sent successfully to the server was 3600000 milliseconds ago. The driver has not received any packets from the server. com.mysql.jdbc.exceptions.jdbc4.CommunicationsException: Communications link failure

`n milliseconds ago`分の`n` `0`または非常に小さい値である場合、通常は実行されたSQL操作によってTiDBが異常終了したことが原因です。原因を特定するには、TiDBのstderrログを確認することをお勧めします。

`n`が非常に大きな値（上記の例では`3600000`など）の場合、この接続は長時間アイドル状態のままで、その後中間プロキシによって切断された可能性があります。通常の解決策は、プロキシのアイドル設定の値を増やし、接続プールで以下の処理を実行することです。

-   毎回接続を使用する前に接続が利用可能かどうかを確認してください
-   別のスレッドを使用して、接続が利用可能かどうかを定期的に確認します。
-   接続を維持するために定期的にテストクエリを送信する

接続プールの実装によっては、上記の方法のうち1つ以上をサポートしている場合があります。対応する設定については、接続プールのドキュメントをご確認ください。

## データアクセスフレームワーク {#data-access-framework}

アプリケーションでは、データベース アクセスを簡素化するために、何らかのデータ アクセス フレームワークを使用することが多いです。

### マイバティス {#mybatis}

[マイバティス](http://www.mybatis.org/mybatis-3/)は、広く普及しているJavaデータアクセスフレームワークです。主にSQLクエリの管理と、結果セットとJavaオブジェクトのマッピングに使用されます。MyBatisはTiDBと高い互換性があります。MyBatisはこれまでの歴史から、問題が発生することはほとんどありません。

このドキュメントでは、主に以下の構成に焦点を当てています。

#### マッパーパラメータ {#mapper-parameters}

MyBatis Mapper は次の 2 つのパラメータをサポートしています。

-   `select 1 from t where id = #{param1}`は Prepared Statement として`select 1 from t where id =?`に変換され、「準備済み」となり、実際のパラメータは再利用のために使用されます。このパラメータを前述の Prepare 接続パラメータと併用すると、最高のパフォーマンスが得られます。
-   `select 1 from t where id = ${param2}`はテキストファイルとして`select 1 from t where id = 1`に置き換えられ、実行されます。このステートメントが異なるパラメータに置き換えられて実行されると、MyBatis は TiDB にステートメントを「準備」するための異なるリクエストを送信します。これにより、TiDB は多数の Prepared Statement をキャッシュする可能性があり、この方法で SQL 操作を実行するとインジェクションのセキュリティリスクが生じます。

#### 動的SQLバッチ {#dynamic-sql-batch}

[動的SQL - foreach](http://www.mybatis.org/mybatis-3/dynamic-sql.html#foreach)

複数の`INSERT`文を`insert ... values(...), (...), ...`形式に自動書き換えるために、前述のようにJDBCで`rewriteBatchedStatements=true`設定することに加え、MyBatisでは動的SQLを使用して半自動でバッチ挿入を生成することもできます。以下のマッパーを例に挙げましょう。

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

このマッパーは`insert on duplicate key update`文を生成します。その後に続く`(?,?,?)`の「値」の数は、渡されたリストの数によって決まります。最終的な効果は`rewriteBatchStatements=true`使用した場合と似ており、クライアントとTiDB間の通信オーバーヘッドも効果的に削減されます。

前述のように、準備済みステートメントの最大長が`prepStmtCacheSqlLimit`を超えるとキャッシュされなくなることにも注意する必要があります。

#### ストリーミング結果 {#streaming-result}

[前のセクション](#use-streamingresult-to-get-the-execution-result) 、JDBCで実行結果をストリーム読み取りする方法が導入されました。JDBCの対応する設定に加えて、MyBatisで非常に大きな結果セットを読み取る場合は、以下の点にも注意する必要があります。

-   マッパー設定で単一のSQL文に`fetchSize`設定できます（前のコードブロックを参照）。これはJDBCで`setFetchSize`呼び出すのと同じ効果があります。
-   クエリ インターフェイスを`ResultHandler`で使用すると、一度に結果セット全体を取得することを回避できます。
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

`openSession`間に`ExecutorType`選択できます。MyBatis は 3 種類のエグゼキューターをサポートしています。

-   シンプル: 準備されたステートメントは実行ごとにJDBCに呼び出されます（JDBC構成項目`cachePrepStmts`が有効になっている場合は、繰り返し準備されたステートメントが再利用されます）
-   再利用: 準備済みステートメントは`executor`にキャッシュされるため、JDBC `cachePrepStmts`を使用せずに準備済みステートメントの重複呼び出しを削減できます。
-   バッチ：各更新操作（ `INSERT` / `DELETE` / `UPDATE` ）はまずバッチに追加され、トランザクションがコミットされるか、 `SELECT`クエリが実行されるまで実行されます。JDBCレイヤーで`rewriteBatchStatements`有効になっている場合は、ステートメントの書き換えが試行されます。有効になっていない場合は、ステートメントが1つずつ送信されます。

通常、デフォルト値`ExecutorType`は`Simple`です。7 `openSession`呼び出す場合は`ExecutorType`変更する必要があります。バッチ実行の場合、トランザクション内で`UPDATE`または`INSERT`のステートメントは非常に高速に実行されるものの、データの読み取りやトランザクションのコミット時に速度が低下することがあります。これは実際には正常な動作であるため、遅いSQLクエリのトラブルシューティングを行う際にはこの点に注意する必要があります。

## 春のトランザクション {#spring-transaction}

現実の世界では、アプリケーションは[春のトランザクション](https://docs.spring.io/spring/docs/4.2.x/spring-framework-reference/html/transaction.html)と AOP の側面を使用してトランザクションを開始および停止する場合があります。

メソッド定義に`@Transactional`アノテーションを追加すると、AOPはメソッドが呼び出される前にトランザクションを開始し、メソッドが結果を返す前にトランザクションをコミットします。アプリケーションで同様のニーズがある場合は、コード内の`@Transactional`使用して、トランザクションの開始と終了のタイミングを判断できます。

埋め込みの特殊なケースに注意してください。このケースが発生した場合、Springは[伝搬](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/transaction/annotation/Propagation.html)設定に基づいて異なる動作をします。

## その他 {#misc}

このセクションでは、問題のトラブルシューティングに役立つJavaの便利なツールをいくつか紹介します。

### トラブルシューティングツール {#troubleshooting-tools}

Javaアプリケーションで問題が発生し、アプリケーションロジックが不明な場合は、JVMの強力なトラブルシューティングツールの使用をお勧めします。以下に、一般的なツールをいくつか紹介します。

#### jスタック {#jstack}

[jスタック](https://docs.oracle.com/javase/7/docs/technotes/tools/share/jstack.html)は Go の pprof/goroutine に似ており、プロセスがスタックする問題を簡単にトラブルシューティングできます。

`jstack pid`実行すると、対象プロセス内のすべてのスレッドのIDとスタック情報を出力できます。デフォルトではJavaスタックのみが出力されます。JVM内のC++スタックも同時に出力したい場合は、 `-m`オプションを追加してください。

jstack を複数回使用することで、スタックの問題 (たとえば、Mybatis で Batch ExecutorType を使用しているためにアプリケーションのビューからのクエリが遅いなど) やアプリケーションのデッドロックの問題 (たとえば、アプリケーションが SQL ステートメントを送信する前にロックをプリエンプトしているために SQL ステートメントを送信しないなど) を簡単に見つけることができます。

さらに、 `top -p $ PID -H`またはJava のスイスナイフは、スレッドIDを確認する一般的な方法です。また、「スレッドが大量のCPUリソースを占有し、何を実行しているのかわからない」という問題を特定するには、次の手順を実行してください。

-   スレッド ID を 16 進数に変換するには`printf "%x\n" pid`使用します。
-   対応するスレッドのスタック情報を見つけるには、jstack 出力に移動します。

#### jmapとmat {#jmap-x26-mat}

Go の pprof/heap とは異なり、 [jmap](https://docs.oracle.com/javase/7/docs/technotes/tools/share/jmap.html)​​プロセス全体のメモリスナップショットをダンプし (Go ではディストリビューターのサンプリング)、そのスナップショットを別のツール[マット](https://www.eclipse.org/mat/)で分析できます。

mat を使用すると、プロセス内のすべてのオブジェクトの関連情報と属性を確認できるほか、スレッドの実行状態を観察することもできます。例えば、mat を使用すると、現在のアプリケーションに存在する MySQL 接続オブジェクトの数や、各接続オブジェクトのアドレスとステータス情報を確認できます。

mat はデフォルトでは到達可能なオブジェクトのみを処理することに注意してください。若いGCの問題をトラブルシューティングしたい場合は、mat の設定を調整して到達不可能なオブジェクトを表示できます。また、若いGCの問題（または多数の短命オブジェクト）のメモリ割り当てを調査するには、 Java Flight Recorder を使用する方が便利です。

#### トレース {#trace}

オンラインアプリケーションは通常、コードの変更をサポートしていませんが、 Javaで動的なインストルメンテーションを実行して問題を特定することが求められることがよくあります。そのため、btraceやarthas traceの使用は良い選択肢です。これらのツールは、アプリケーションプロセスを再起動することなく、トレースコードを動的に挿入できます。

#### フレームグラフ {#flame-graph}

Javaアプリケーションでフレームグラフを取得するのは面倒です。詳細については[Java Flame Graphs の紹介: みんなに火を!](http://psy-lob-saw.blogspot.com/2017/02/flamegraphs-intro-fire-for-everyone.html)参照してください。

## 結論 {#conclusion}

このドキュメントでは、データベースとやり取りする一般的なJavaコンポーネントに基づいて、TiDBを使用したJavaアプリケーション開発における一般的な問題と解決策について説明します。TiDBはMySQLプロトコルと高い互換性があるため、MySQLベースのJavaアプリケーションのベストプラクティスのほとんどがTiDBにも適用できます。

## ヘルプが必要ですか? {#need-help}

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](/support.md)についてコミュニティに質問してください。
