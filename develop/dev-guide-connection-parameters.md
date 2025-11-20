---
title: Connection Pools and Connection Parameters
summary: このドキュメントでは、TiDB の接続プールとパラメータの設定方法について説明します。接続プールのサイズ、プローブの設定、最適なスループットを得るための計算式などについて説明します。また、パフォーマンスを最適化するための JDBC API の使用方法と MySQL Connector/J パラメータ設定についても説明します。
---

# 接続プールと接続パラメータ {#connection-pools-and-connection-parameters}

このドキュメントでは、ドライバーまたは ORM フレームワークを使用して TiDB に接続するときに、接続プールと接続パラメータを構成する方法について説明します。

<CustomContent platform="tidb">

Javaアプリケーション開発に関するさらなるヒントに興味がある場合は、 [TiDB を使用したJavaアプリケーション開発のベスト プラクティス](/best-practices/java-app-best-practices.md#connection-pool)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

Javaアプリケーション開発に関するさらなるヒントに興味がある場合は、 [TiDB を使用したJavaアプリケーション開発のベスト プラクティス](https://docs.pingcap.com/tidb/stable/java-app-best-practices)参照してください。

</CustomContent>

## 接続プール {#connection-pool}

TiDB (MySQL) 接続の構築は、比較的コストがかかります（少なくともOLTPシナリオでは）。TCP 接続の構築に加えて、接続認証も必要となるためです。そのため、クライアントは通常、TiDB (MySQL) 接続を接続プールに保存し、再利用できるようにします。

Java には、 [HikariCP](https://github.com/brettwooldridge/HikariCP) 、 [tomcat-jdbc](https://tomcat.apache.org/tomcat-10.1-doc/jdbc-pool.html) 、 [druid](https://github.com/alibaba/druid) 、 [c3p0](https://www.mchange.com/projects/c3p0/) 、 [dbcp](https://commons.apache.org/proper/commons-dbcp/)など、多くの接続プール実装があります。TiDB では使用する接続プールに制限がないため、アプリケーションに合わせて好きな接続プールを選択できます。

### 接続数を設定する {#configure-the-number-of-connections}

アプリケーションのニーズに応じて接続プールのサイズを適切に調整するのが一般的です。HikariCPを例に挙げましょう。

-   **maximumPoolSize** : 接続プールの最大接続数。この値が大きすぎると、TiDBは無駄な接続を維持するためにリソースを消費します。この値が小さすぎると、アプリケーションの接続速度が遅くなります。したがって、アプリケーションの特性に応じてこの値を設定する必要があります。詳細は[プールのサイズについて](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing)参照してください。
-   **minimumIdle** : 接続プール内のアイドル接続の最小数。これは主に、アプリケーションがアイドル状態のときに突発的なリクエストに対応するために、いくつかの接続を予約するために使用されます。アプリケーションの特性に応じて設定する必要があります。

アプリケーションは、使用を終えた後、接続を返却する必要があります。接続プールの問題を適時に特定するために、アプリケーションでは対応する接続プール監視（ **metricRegistry**など）を使用することをお勧めします。

### 接続の有効期間を設定する {#configure-the-lifetime-of-connections}

TiDBサーバーがシャットダウン、メンテナンスのために再起動、あるいはハードウェアやネットワーク障害などの予期せぬ問題が発生した場合、既存のクライアント接続がリセットされ、アプリケーションの中断につながる可能性があります。このような問題を回避するために、長時間実行されるデータベース接続を少なくとも1日に1回閉じて再作成することをお勧めします。

ほとんどの接続プール ライブラリは、接続の最大有効期間を制御するためのパラメータを提供します。

<SimpleTab>
<div label="HikariCP">

-   **`maxLifetime`** : プール内の接続の最大有効期間。

</div>

<div label="tomcat-jdbc">

-   **`maxAge`** : プール内の接続の最大有効期間。

</div>

<div label="c3p0">

-   **`maxConnectionAge`** : プール内の接続の最大有効期間。

</div>

<div label="dbcp">

-   **`maxConnLifetimeMillis`** : プール内の接続の最大有効期間。

</div>
</SimpleTab>

### プローブ構成 {#probe-configuration}

接続プールは、次のようにクライアントから TiDB への永続的な接続を維持します。

-   v5.4 より前では、TiDB はデフォルトでクライアント接続を積極的に閉じません (エラーが報告されない限り)。
-   バージョン5.4以降、TiDBはデフォルトで`28800`秒（つまり`8`時間）の非アクティブ状態が続くとクライアント接続を自動的に閉じます。このタイムアウト設定は、TiDBとMySQL互換の`wait_timeout`変数を使用して制御できます。詳細については、 [JDBCクエリタイムアウト](/develop/dev-guide-timeouts-in-tidb.md#jdbc-query-timeout)参照してください。

さらに、クライアントとTiDBの間には、 [LVS](https://en.wikipedia.org/wiki/Linux_Virtual_Server)や[HAプロキシ](https://en.wikipedia.org/wiki/HAProxy)ようなネットワークプロキシが存在する場合があります。これらのプロキシは通常、一定のアイドル時間（プロキシのアイドル設定によって決定されます）が経過すると、接続をプロアクティブにクリーンアップします。プロキシのアイドル設定を監視するだけでなく、接続プールはキープアライブのために接続を維持またはプローブする必要があります。

Javaアプリケーションで次のエラーが頻繁に表示される場合:

    The last packet sent successfully to the server was 3600000 milliseconds ago. The driver has not received any packets from the server. com.mysql.jdbc.exceptions.jdbc4.CommunicationsException: Communications link failure

`n milliseconds ago`分の`n` `0`または非常に小さい値である場合、通常は実行されたSQL操作によってTiDBが異常終了したことが原因です。原因を特定するには、TiDBのstderrログを確認することをお勧めします。

`n`が非常に大きな値（上記の例の`3600000`など）の場合、この接続は長時間アイドル状態のままで、その後プロキシによって閉じられた可能性があります。通常の解決策は、プロキシのアイドル設定の値を増やし、接続プールで以下の処理を実行することです。

-   毎回接続を使用する前に、接続が利用可能かどうかを確認してください。
-   別のスレッドを使用して、接続が利用可能かどうかを定期的に確認します。
-   接続を維持するために定期的にテスト クエリを送信します。

接続プールの実装によっては、上記の方法のうち1つ以上をサポートしている場合があります。対応する設定については、接続プールのドキュメントをご確認ください。

### 経験に基づいた公式 {#formulas-based-on-experience}

HikariCPの[プールのサイズについて](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing)記事によると、データベース接続プールの適切なサイズ設定方法がわからない場合は、まず[経験に基づいた式](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing#connections--core_count--2--effective_spindle_count)から始めることができます。その後、計算式から算出されたプールサイズのパフォーマンス結果に基づいて、最適なパフォーマンスが得られるようにサイズをさらに調整することができます。

経験に基づいた計算式は次のとおりです。

    connections = ((core_count * 2) + effective_spindle_count)

数式内の各パラメータの説明は次のとおりです。

-   **接続**: 取得された接続のサイズ。
-   **core_count** : CPU コアの数。
-   **effective_spindle_count** : ハードドライブの数（ [SSD](https://en.wikipedia.org/wiki/Solid-state_drive)ではありません）。回転するハードディスクはそれぞれスピンドルと呼ばれるため、スピンドルと呼ばれます。例えば、16台のディスクでRAIDを構成しているサーバーを使用している場合、 **effective_spindle_count**は16になります。HDD**は**通常、一度に1つのリクエストしか処理できないため、この式は実際にはサーバーが処理できる同時I/Oリクエストの数を測定しています。

特に、 [式](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing#the-formula)下にある以下の注意事項に注意してください。

>     A formula which has held up pretty well across a lot of benchmarks for years is
>     that for optimal throughput the number of active connections should be somewhere
>     near ((core_count * 2) + effective_spindle_count). Core count should not include
>     HT threads, even if hyperthreading is enabled. Effective spindle count is zero if
>     the active data set is fully cached, and approaches the actual number of spindles
>     as the cache hit rate falls. ... There hasn't been any analysis so far regarding
>     how well the formula works with SSDs.

このメモは次のことを示しています:

-   **core_count は**、 [ハイパースレッディング](https://en.wikipedia.org/wiki/Hyper-threading)有効にするかどうかに関係なく、物理コアの数です。
-   データが完全にキャッシュされている場合は、 **effective_spindle_count を**`0`に設定する必要があります。キャッシュのヒット率が低下すると、カウントは実際の値である`HDD`に近づきます。
-   **この式が*SSD*で機能するかどうかはテストされておらず不明です。**

SSD を使用する場合は、代わりに経験に基づいた次の式を使用することをお勧めします。

    connections = (number of cores * 4)

したがって、SSD の場合は初期接続プールの最大接続サイズを`cores * 4`に設定し、さらにサイズを調整してパフォーマンスをチューニングすることができます。

### チューニング方向 {#tuning-direction}

ご覧のとおり、 [経験に基づいた公式](#formulas-based-on-experience)から計算されたサイズはあくまで推奨される基本値です。特定のマシンで最適なサイズを得るには、基本値付近の値を試してパフォーマンスをテストする必要があります。

最適なサイズを見つけるのに役立つ基本的なルールをいくつか示します。

-   ネットワークまたはstorageのレイテンシーが高い場合は、最大接続数を増やしてレイテンシーによる待機時間を短縮してください。レイテンシーによってスレッドがブロックされた場合でも、他のスレッドが引き継いで処理を続行できます。
-   サーバーに複数のサービスがデプロイされていて、各サービスに個別の接続プールがある場合は、すべての接続プールへの接続の最大数の合計を考慮してください。

## 接続パラメータ {#connection-parameters}

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

多くの場合、JDBCは実行効率を向上させるために、クエリ結果を事前に取得し、デフォルトでクライアントのメモリに保存します。しかし、クエリが返す結果セットが非常に大きい場合、クライアントはデータベースサーバーに一度に返されるレコード数を減らすよう要求し、クライアントのメモリが準備できて次のバッチを要求するまで待機することがあります。

JDBC では通常、次の 2 つの処理方法が使用されます。

-   最初の方法： [**FetchSize**を`Integer.MIN_VALUE`に設定する](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-implementation-notes.html#ResultSet)クライアントがキャッシュしないようにします。クライアントは`StreamingResult`を介してネットワーク接続から実行結果を読み取ります。

    クライアントがストリーミング読み取り方式を使用する場合、クエリを実行するためにステートメントを続行する前に、読み取りを完了するか、 `resultset`閉じる必要があります。そうでない場合は、エラー`No statements may be issued when any streaming result sets are open and in use on a given connection. Ensure that you have called .close() on any active streaming result sets before attempting more queries.`が返されます。

    クライアントが読み取りを完了するか`resultset`閉じる前にクエリでこのようなエラーが発生するのを回避するには、URL に`clobberStreamingResults=true`パラメータを追加します。これにより、 `resultset`自動的に閉じられますが、前のストリーミングクエリで読み取られるべき結果セットは失われます。

-   2 番目の方法: 最初に[`FetchSize`設定](http://makejavafaster.blogspot.com/2015/06/jdbc-fetch-size-performance.html)正の整数として設定し、次に JDBC URL で`useCursorFetch = true`設定してカーソル フェッチを使用します。

TiDB は両方の方法をサポートしていますが、実装がより単純で実行効率が優れているため、 `FetchSize`を`Integer.MIN_VALUE`に設定する最初の方法を使用することをお勧めします。

2番目の方法では、TiDBはまずすべてのデータをTiDBノードにロードし、その後`FetchSize`に従ってクライアントにデータを返します。そのため、通常は1番目の方法よりも多くのメモリを消費します。3 [`tidb_enable_tmp_storage_on_oom`](/system-variables.md#tidb_enable_tmp_storage_on_oom) `ON`設定した場合、TiDBは結果を一時的にハードディスクに書き込む可能性があります。

[`tidb_enable_lazy_cursor_fetch`](/system-variables.md#tidb_enable_lazy_cursor_fetch-new-in-v830)システム変数を`ON`に設定すると、TiDB はクライアントがデータを取得する際にのみデータの一部を読み取ろうとするため、メモリ使用量が少なくなります。詳細と制限事項については、 [`tidb_enable_lazy_cursor_fetch`システム変数の完全な説明](/system-variables.md#tidb_enable_lazy_cursor_fetch-new-in-v830)をご覧ください。

### MySQL JDBCパラメータ {#mysql-jdbc-parameters}

JDBCは通常、実装関連の設定をJDBC URLパラメータの形で提供します。このセクションでは[MySQL Connector/Jのパラメータ設定](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-configuration-properties.html)について説明します（MariaDBをご利用の場合は[MariaDBのパラメータ設定](https://mariadb.com/docs/connectors/mariadb-connector-j/about-mariadb-connector-j#optional-url-parameters)参照してください）。このドキュメントではすべての設定項目を網羅することはできないため、主にパフォーマンスに影響を与える可能性のあるいくつかのパラメータに焦点を当てます。

#### 準備関連のパラメータ {#prepare-related-parameters}

このセクションでは、 `Prepare`に関連するパラメータを紹介します。

-   **useServerPrepStmts**

    **useServerPrepStmts は**デフォルトで`false`に設定されています。つまり、Prepare API を使用した場合でも、「準備」操作はクライアント側でのみ実行されます。サーバーの解析オーバーヘッドを回避するため、同じ SQL 文で Prepare API を複数回使用する場合は、この設定を`true`に設定することをお勧めします。

    この設定がすでに有効になっていることを確認するには、次の操作を実行します。

    -   TiDB 監視ダッシュボードに移動し、**クエリ サマリー**&gt;**インスタンス別の CPS**を通じて要求コマンド タイプを表示します。
    -   リクエスト内の`COM_QUERY` `COM_STMT_EXECUTE`または`COM_STMT_PREPARE`に置き換えられた場合、この設定は既に有効になっていることを意味します。

-   **キャッシュ準備ステートメント**

    `useServerPrepStmts=true`ではサーバーがプリペアドステートメントを実行できますが、デフォルトではクライアントはプリペアドステートメントを毎回実行した後に閉じ、再利用しません。つまり、「準備」操作はテキストファイルの実行ほど効率的ではありません。この問題を解決するには、 `useServerPrepStmts=true`設定した後、 `cachePrepStmts=true`設定することをお勧めします。これにより、クライアントはプリペアドステートメントをキャッシュできるようになります。

    この設定がすでに有効になっていることを確認するには、次の操作を実行します。

    -   TiDB 監視ダッシュボードに移動し、**クエリ サマリー**&gt;**インスタンス別の CPS**を通じて要求コマンド タイプを表示します。
    -   リクエスト内の`COM_STMT_EXECUTE`の数が`COM_STMT_PREPARE`の数よりはるかに多い場合、この設定はすでに有効になっていることを意味します。

    また、 `useConfigs=maxPerformance`設定すると、 `cachePrepStmts=true`含む複数のパラメータが同時に設定されます。

-   **準備StmtCacheSqlLimit**

    `cachePrepStmts`設定した後は、 `prepStmtCacheSqlLimit`設定にも注意してください（デフォルト値は`256`です）。この設定は、クライアントにキャッシュされるプリペアドステートメントの最大長を制御します。

    この最大長を超えるプリペアドステートメントはキャッシュされないため、再利用できません。この場合、アプリケーションの実際のSQLの長さに応じて、この設定の値を増やすことを検討してください。

    次の場合は、この設定が小さすぎないかどうかを確認する必要があります。

    -   TiDB 監視ダッシュボードに移動し、**クエリ サマリー**&gt;**インスタンス別の CPS**を通じて要求コマンド タイプを表示します。
    -   そして、 `cachePrepStmts=true`設定されていることがわかりますが、 `COM_STMT_PREPARE`はまだ`COM_STMT_EXECUTE`とほぼ同じで、 `COM_STMT_CLOSE`存在します。

-   **準備StmtCacheSize**

    **prepStmtCacheSize は**、キャッシュされる Prepared Statement の数を制御します（デフォルト値は`25` ）。アプリケーションで多くの種類の SQL 文を「準備」する必要があり、Prepared Statement を再利用したい場合は、この値を増やすことができます。

    この設定がすでに有効になっていることを確認するには、次の操作を実行します。

    -   TiDB 監視ダッシュボードに移動し、**クエリ サマリー**&gt;**インスタンス別の CPS**を通じて要求コマンド タイプを表示します。
    -   リクエスト内の`COM_STMT_EXECUTE`の数が`COM_STMT_PREPARE`の数よりはるかに多い場合、この設定はすでに有効になっていることを意味します。

#### バッチ関連のパラメータ {#batch-related-parameters}

バッチ書き込み処理中は、 `rewriteBatchedStatements=true`設定することをお勧めします。 `addBatch()`または`executeBatch()`を使用した後でも、JDBCはデフォルトでSQLを1つずつ送信します。例：

```java
pstmt = prepare("INSERT INTO `t` (a) values(?)");
pstmt.setInt(1, 10);
pstmt.addBatch();
pstmt.setInt(1, 11);
pstmt.addBatch();
pstmt.setInt(1, 12);
pstmt.executeBatch();
```

`Batch`方法が使用されていますが、TiDB に送信される SQL ステートメントは個別の`INSERT`ステートメントのままです。

```sql
INSERT INTO `t` (`a`) VALUES(10);
INSERT INTO `t` (`a`) VALUES(11);
INSERT INTO `t` (`a`) VALUES(12);
```

ただし、 `rewriteBatchedStatements=true`設定すると、TiDB に送信される SQL ステートメントは単一の`INSERT`ステートメントになります。

```sql
INSERT INTO `t` (`a`) values(10),(11),(12);
```

`INSERT`番目の文の書き換えは、複数の「values」キーワードの後の値を連結して、1 つの SQL 文にまとめるというものです。3 `INSERT`文に他の違いがある場合は、書き換えることはできません。例えば、次のようになります。

```sql
INSERT INTO `t` (`a`) VALUES (10) ON DUPLICATE KEY UPDATE `a` = 10;
INSERT INTO `t` (`a`) VALUES (11) ON DUPLICATE KEY UPDATE `a` = 11;
INSERT INTO `t` (`a`) VALUES (12) ON DUPLICATE KEY UPDATE `a` = 12;
```

上記の`INSERT`の文を1つの文に書き直すことはできません。しかし、3つの文を次のように書き換えると、

```sql
INSERT INTO `t` (`a`) VALUES (10) ON DUPLICATE KEY UPDATE `a` = VALUES(`a`);
INSERT INTO `t` (`a`) VALUES (11) ON DUPLICATE KEY UPDATE `a` = VALUES(`a`);
INSERT INTO `t` (`a`) VALUES (12) ON DUPLICATE KEY UPDATE `a` = VALUES(`a`);
```

すると、書き換え要件を満たします。上記の`INSERT`つの文は、次の1つの文に書き換えられます。

```sql
INSERT INTO `t` (`a`) VALUES (10), (11), (12) ON DUPLICATE KEY UPDATE a = VALUES(`a`);
```

バッチ更新中に3つ以上の更新が発生した場合、SQL文は書き換えられ、複数のクエリとして送信されます。これにより、クライアントからサーバーへのリクエストのオーバーヘッドは効果的に削減されますが、副作用として生成されるSQL文のサイズが大きくなります。例えば、次のようになります。

```sql
UPDATE `t` SET `a` = 10 WHERE `id` = 1; UPDATE `t` SET `a` = 11 WHERE `id` = 2; UPDATE `t` SET `a` = 12 WHERE `id` = 3;
```

また、 [クライアントのバグ](https://bugs.mysql.com/bug.php?id=96623)ため、バッチ更新中に`rewriteBatchedStatements=true`と`useServerPrepStmts=true`を設定する場合は、このバグを回避するために`allowMultiQueries=true`パラメータも設定することをお勧めします。

#### パラメータを統合する {#integrate-parameters}

監視中に、アプリケーションがTiDBクラスタに対して`INSERT`操作しか実行していないにもかかわらず、冗長な`SELECT`ステートメントが多数存在することに気付く場合があります。これは通常、JDBCが設定を照会するためにいくつかのSQLステートメント（例えば`select @@session.transaction_read_only`を送信するために発生します。これらのSQLステートメントはTiDBには役に立たないため、余分なオーバーヘッドを回避するために`useConfigs=maxPerformance`に設定することをお勧めします。

`useConfigs=maxPerformance`には一連の設定が含まれています。MySQL Connector/J 8.0およびMySQL Connector/J 5.1の詳細な設定については、それぞれ[mysql-コネクタ-j 8.0](https://github.com/mysql/mysql-connector-j/blob/release/8.0/src/main/resources/com/mysql/cj/configurations/maxPerformance.properties)と[mysql-コネクタ-j 5.1](https://github.com/mysql/mysql-connector-j/blob/release/5.1/src/com/mysql/jdbc/configs/maxPerformance.properties)参照してください。

設定後、監視をチェックして、 `SELECT`ステートメントの数が減っていることを確認できます。

#### タイムアウト関連のパラメータ {#timeout-related-parameters}

TiDB には、タイムアウトを制御するための MySQL 互換パラメータが[`wait_timeout`](/system-variables.md#wait_timeout)と[`max_execution_time`](/system-variables.md#max_execution_time) 2 つが用意されています。これらの 2 つのパラメータは、それぞれJavaアプリケーションとの接続アイドル タイムアウトと、接続中の SQL 実行のタイムアウトを制御します。つまり、これらのパラメータは、TiDB とJavaアプリケーション間の接続の最長アイドル時間と最長ビジー時間を制御します。TiDB v5.4 以降では、デフォルト値`wait_timeout`は`28800`秒 (8 時間) です。v5.4 より前のバージョンの TiDB では、デフォルト値は`0`で、タイムアウトは無制限であることを意味します。デフォルト値`max_execution_time`は`0`で、SQL 文の最大実行時間は無制限であることを意味し、 `SELECT`文すべて ( `SELECT ... FOR UPDATE`を含む) に適用されます。

デフォルト値の[`wait_timeout`](/system-variables.md#wait_timeout)は比較的大きい値です。トランザクションが開始されたものの、コミットもロールバックも行われないシナリオでは、ロックの長時間保持を防ぐために、よりきめ細かな制御と短いタイムアウトが必要になる場合があります。このような場合は、TiDB v7.6.0で導入された[`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760)を使用して、ユーザーセッションにおけるトランザクションのアイドルタイムアウトを制御できます。

しかし、実際の本番環境では、アイドル接続や実行時間が長すぎるSQL文は、データベースやアプリケーションに悪影響を及ぼします。アイドル接続や実行時間が長すぎるSQL文を回避するには、アプリケーションの接続文字列でこれらの2つのパラメータを設定できます。例えば、 `sessionVariables=wait_timeout=3600` （1時間）と`sessionVariables=max_execution_time=300000` （5分）を設定します。

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](/support.md)についてコミュニティに質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](https://tidb.support.pingcap.com/)についてコミュニティに質問してください。

</CustomContent>
