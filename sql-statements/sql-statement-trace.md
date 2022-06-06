---
title: TRACE | TiDB SQL Statement Reference
summary: An overview of the usage of TRACE for the TiDB database.
---

# 痕跡 {#trace}

`TRACE`ステートメントは、クエリの実行に関する詳細情報を提供します。これは、TiDBサーバーのステータスポートによって公開されるグラフィカルインターフェイスを介して表示することを目的としています。

## あらすじ {#synopsis}

**TraceStmt：**

![TraceStmt](/media/sqlgram/TraceStmt.png)

**TraceableStmt：**

![TraceableStmt](/media/sqlgram/TraceableStmt.png)

## 例 {#examples}

{{< copyable "" >}}

```sql
trace format='row' select * from mysql.user;
```

```
+--------------------------------------------+-----------------+------------+
| operation                                  | startTS         | duration   |
+--------------------------------------------+-----------------+------------+
| trace                                      | 17:03:31.938237 | 886.086µs  |
|   ├─session.Execute                        | 17:03:31.938247 | 507.812µs  |
|   │ ├─session.ParseSQL                     | 17:03:31.938254 | 22.504µs   |
|   │ ├─executor.Compile                     | 17:03:31.938321 | 278.931µs  |
|   │ │ └─session.getTxnFuture               | 17:03:31.938337 | 1.515µs    |
|   │ └─session.runStmt                      | 17:03:31.938613 | 109.578µs  |
|   │   ├─TableReaderExecutor.Open           | 17:03:31.938645 | 50.657µs   |
|   │   │ └─distsql.Select                   | 17:03:31.938666 | 21.066µs   |
|   │   │   └─RPCClient.SendRequest          | 17:03:31.938799 | 158.411µs  |
|   │   └─session.CommitTxn                  | 17:03:31.938705 | 12.06µs    |
|   │     └─session.doCommitWitRetry         | 17:03:31.938709 | 2.437µs    |
|   ├─*executor.TableReaderExecutor.Next     | 17:03:31.938781 | 224.327µs  |
|   └─*executor.TableReaderExecutor.Next     | 17:03:31.939019 | 6.266µs    |
+--------------------------------------------+-----------------+------------+
13 rows in set (0.00 sec)
```

{{< copyable "" >}}

```sql
trace format='json' select * from mysql.user;
```

JSON形式のトレースは、TiDBステータスポートを介してアクセスされるトレースビューアに貼り付けることができます。

![TiDB Trace Viewer-1](/media/trace-paste.png)

![TiDB Trace Viewer-2](/media/trace-view.png)

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文のTiDB拡張です。

## も参照してください {#see-also}

-   [説明分析](/sql-statements/sql-statement-explain-analyze.md)
