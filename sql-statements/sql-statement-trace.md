---
title: TRACE | TiDB SQL Statement Reference
summary: An overview of the usage of TRACE for the TiDB database.
---

# 痕跡 {#trace}

`TRACE`ステートメントは、クエリ実行に関する詳細情報を提供します。これは、TiDB サーバーのステータス ポートによって公開されるグラフィカル インターフェイスを通じて表示されることを目的としています。

## 概要 {#synopsis}

```ebnf+diagram
TraceStmt ::=
    "TRACE" ( "FORMAT" "=" stringLit )? TracableStmt

TracableStmt ::=
    ( SelectStmt | DeleteFromStmt | UpdateStmt | InsertIntoStmt | ReplaceIntoStmt | UnionStmt | LoadDataStmt | BeginTransactionStmt | CommitStmt | RollbackStmt | SetStmt )
```

| フォーマット | 説明              |
| ------ | --------------- |
| 行      | ツリー形式で出力        |
| json   | JSON形式の構造化された出力 |
| ログ     | ログベースの出力        |

## 例 {#examples}

### 行 {#row}

```sql
TRACE FORMAT='row' SELECT * FROM mysql.user;
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

### 翻訳 {#json}

```sql
TRACE FORMAT='json' SELECT * FROM mysql.user;
```

JSON 形式のトレースは、TiDB ステータス ポート経由でアクセスできるトレース ビューアーに貼り付けることができます。

![TiDB Trace Viewer-1](/media/trace-paste.png)

![TiDB Trace Viewer-2](/media/trace-view.png)

### ログ {#log}

```sql
TRACE FORMAT='log' SELECT * FROM mysql.user;
```

    +----------------------------+--------------------------------------------------------+------+------------------------------------+
    | time                       | event                                                  | tags | spanName                           |
    +----------------------------+--------------------------------------------------------+------+------------------------------------+
    | 2024-04-08 08:41:47.358734 | --- start span trace ----                              |      | trace                              |
    | 2024-04-08 08:41:47.358737 | --- start span session.ExecuteStmt ----                |      | session.ExecuteStmt                |
    | 2024-04-08 08:41:47.358746 | --- start span executor.Compile ----                   |      | executor.Compile                   |
    | 2024-04-08 08:41:47.358984 | --- start span session.runStmt ----                    |      | session.runStmt                    |
    | 2024-04-08 08:41:47.359035 | --- start span TableReaderExecutor.Open ----           |      | TableReaderExecutor.Open           |
    | 2024-04-08 08:41:47.359047 | --- start span distsql.Select ----                     |      | distsql.Select                     |
    | 2024-04-08 08:41:47.359073 | --- start span *executor.TableReaderExecutor.Next ---- |      | *executor.TableReaderExecutor.Next |
    | 2024-04-08 08:41:47.359077 | table scan table: user, range: [[-inf,+inf]]           |      | *executor.TableReaderExecutor.Next |
    | 2024-04-08 08:41:47.359094 | --- start span regionRequest.SendReqCtx ----           |      | regionRequest.SendReqCtx           |
    | 2024-04-08 08:41:47.359098 | send Cop request to region 16 at store1                |      | regionRequest.SendReqCtx           |
    | 2024-04-08 08:41:47.359237 | --- start span *executor.TableReaderExecutor.Next ---- |      | *executor.TableReaderExecutor.Next |
    | 2024-04-08 08:41:47.359240 | table scan table: user, range: [[-inf,+inf]]           |      | *executor.TableReaderExecutor.Next |
    | 2024-04-08 08:41:47.359242 | execute done, ReturnRow: 1, ModifyRow: 0               |      | trace                              |
    | 2024-04-08 08:41:47.359252 | execute done, modify row: 0                            |      | trace                              |
    +----------------------------+--------------------------------------------------------+------+------------------------------------+
    14 rows in set (0.0008 sec)

## MySQL 互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [EXPLAIN分析](/sql-statements/sql-statement-explain-analyze.md)
