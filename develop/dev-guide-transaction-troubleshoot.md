---
title: Handle Transaction Errors
summary: Learn about how to handle transaction errors, such as deadlocks and application retry errors.
---

# トランザクションエラーの処理 {#handle-transaction-errors}

このドキュメントでは、デッドロックやアプリケーションの再試行エラーなどのトランザクション エラーを処理する方法を紹介します。

## デッドロック {#deadlocks}

アプリケーションの次のエラーは、デッドロックの問題を示しています。

```sql
ERROR 1213: Deadlock found when trying to get lock; try restarting transaction
```

デッドロックは、2 つ以上のトランザクションが、既に保持しているロックを解放するのを相互に待機している場合に発生します。または、ロックの順序に一貫性がないために、ロック リソースを待機するループが発生します。

以下は、データベース[`bookshop`](/develop/dev-guide-bookshop-schema-design.md)のテーブル`books`を使用したデッドロックの例です。

まず、テーブル`books`に 2 つの行を挿入します。

```sql
INSERT INTO books (id, title, stock, published_at) VALUES (1, 'book-1', 10, now()), (2, 'book-2', 10, now());
```

TiDB悲観的トランザクション モードで、2 つのクライアントがそれぞれ次のステートメントを実行すると、デッドロックが発生します。

| クライアント A                                              | クライアント B                                                  |
| ----------------------------------------------------- | --------------------------------------------------------- |
| 始める;                                                  |                                                           |
|                                                       | 始める;                                                      |
| UPDATE 本 SET stock=stock-1 WHERE id=1;                |                                                           |
|                                                       | UPDATE 本 SET stock=stock-1 WHERE id=2;                    |
| UPDATE 本 SET stock=stock-1 WHERE id=2; -- 実行がブロックされます |                                                           |
|                                                       | UPDATE 本 SET stock=stock-1 WHERE id=1; -- デッドロック エラーが発生する |

クライアント B でデッドロック エラーが発生すると、TiDB はクライアント B のトランザクションを自動的にロールバックします。 client-A の更新`id=2`正常に実行されます。その後、 `COMMIT`実行してトランザクションを終了できます。

### 解決策 1: デッドロックを回避する {#solution-1-avoid-deadlocks}

パフォーマンスを向上させるために、ビジネス ロジックまたはスキーマの設計を調整することで、アプリケーション レベルでのデッドロックを回避できます。上記の例では、client-B も client-A と同じ更新順序を使用している場合、つまり、まず book を`id=1`で更新し、次に book を`id=2`で更新します。その後、デッドロックを回避できます。

| クライアント A                               | クライアント B                                           |
| -------------------------------------- | -------------------------------------------------- |
| 始める;                                   |                                                    |
|                                        | 始める;                                               |
| UPDATE 本 SET stock=stock-1 WHERE id=1; |                                                    |
|                                        | UPDATE 本 SET stock=stock-1 WHERE id=1; -- ブロックされます |
| UPDATE 本 SET stock=stock-1 WHERE id=2; |                                                    |
| 専念;                                    |                                                    |
|                                        | UPDATE 本 SET stock=stock-1 WHERE id=2;             |
|                                        | 専念;                                                |

または、2 つのブックを 1 つの SQL ステートメントで更新することもできます。これにより、デッドロックを回避し、より効率的に実行することもできます。

```sql
UPDATE books SET stock=stock-1 WHERE id IN (1, 2);
```

### 解決策 2: トランザクションの粒度を下げる {#solution-2-reduce-transaction-granularity}

各トランザクションで 1 つのブックのみを更新すると、デッドロックも回避できます。ただし、トランザクションの粒度が小さすぎると、パフォーマンスに影響を与える可能性があるというトレードオフがあります。

### 解決策 3:楽観的トランザクションを使用する {#solution-3-use-optimistic-transactions}

楽観的トランザクション モデルにはデッドロックはありません。ただし、アプリケーションでは、失敗した場合に楽観的トランザクション再試行ロジックを追加する必要があります。詳細については、 [アプリケーションの再試行とエラー処理](#application-retry-and-error-handling)を参照してください。

### 解決策 4: 再試行する {#solution-4-retry}

エラー メッセージで提案されているように、アプリケーションに再試行ロジックを追加します。詳細については、 [アプリケーションの再試行とエラー処理](#application-retry-and-error-handling)を参照してください。

## アプリケーションの再試行とエラー処理 {#application-retry-and-error-handling}

TiDB は MySQL と可能な限り互換性がありますが、その分散システムの性質により、特定の違いが生じます。そのうちの 1 つがトランザクション モデルです。

開発者がデータベースに接続するために使用するアダプタと ORM は、MySQL や Oracle などの従来のデータベース用に調整されています。これらのデータベースでは、トランザクションがデフォルトの分離レベルでコミットに失敗することはめったにないため、再試行メカニズムは必要ありません。トランザクションがコミットに失敗すると、これらのデータベースでは例外として扱われるため、これらのクライアントはエラーのために中止されます。

MySQL などの従来のデータベースとは異なり、TiDB では楽観的トランザクション モデルを使用し、コミットの失敗を回避したい場合は、アプリケーションで関連する例外を処理するメカニズムを追加する必要があります。

次の Python 疑似コードは、アプリケーション レベルの再試行を実装する方法を示しています。ドライバーや ORM で高度な再試行ロジックを実装する必要はありません。あらゆるプログラミング言語や環境で使用できます。

再試行ロジックは、次の規則に従う必要があります。

-   再試行の失敗回数が`max_retries`回の制限に達すると、エラーがスローされます。
-   SQL 実行例外をキャッチするには、 `try ... catch ...`を使用します。次のエラーが発生した場合は、再試行してください。他のエラーが発生した場合はロールバックします。
    -   `Error 8002: can not retry select for update statement` : SELECT FOR UPDATE 書き込み競合エラー
    -   `Error 8022: Error: KV error safe to retry` : トランザクション コミット失敗エラー。
    -   `Error 8028: Information schema is changed during the execution of the statement` : テーブル スキーマが DDL 操作によって変更されたため、トランザクション コミットでエラーが発生しました。
    -   `Error 9007: Write conflict` : 書き込み競合エラー。通常、楽観的トランザクション モードが使用されている場合に、複数のトランザクションが同じデータ行を変更することによって発生します。
-   try ブロックの最後のトランザクションを`COMMIT` 。

<CustomContent platform="tidb">

エラー コードの詳細については、 [エラーコードとトラブルシューティング](/error-codes.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

エラー コードの詳細については、 [エラーコードとトラブルシューティング](https://docs.pingcap.com/tidb/stable/error-codes)を参照してください。

</CustomContent>

```python
while True:
    n++
    if n == max_retries:
        raise("did not succeed within #{n} retries")
    try:
        connection.execute("your sql statement here")
        connection.exec('COMMIT')
        break
    catch error:
        if (error.code != "9007" && error.code != "8028" && error.code != "8002" && error.code != "8022"):
            raise error
        else:
            connection.exec('ROLLBACK')

            # Capture the error types that require application-side retry,
            # wait for a short period of time,
            # and exponentially increase the wait time for each transaction failure
            sleep_ms = int(((1.5 ** n) + rand) * 100)
            sleep(sleep_ms) # make sure your sleep() takes milliseconds
```

> **ノート：**
>
> `Error 9007: Write conflict`頻繁に発生する場合は、スキーマ設計とワークロードのデータ アクセス パターンを確認して、競合の根本原因を見つけ、より適切な設計で競合を回避する必要があります。

<CustomContent platform="tidb">

トランザクションの競合をトラブルシューティングして解決する方法については、 [ロック競合のトラブルシューティング](/troubleshoot-lock-conflicts.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

トランザクションの競合をトラブルシューティングして解決する方法については、 [ロック競合のトラブルシューティング](https://docs.pingcap.com/tidb/stable/troubleshoot-lock-conflicts)を参照してください。

</CustomContent>

## こちらもご覧ください {#see-also}

<CustomContent platform="tidb">

-   [オプティミスティック トランザクションでの書き込み競合のトラブルシューティング](/troubleshoot-write-conflicts.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [オプティミスティック トランザクションでの書き込み競合のトラブルシューティング](https://docs.pingcap.com/tidb/stable/troubleshoot-write-conflicts)

</CustomContent>
