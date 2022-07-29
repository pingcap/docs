---
title: Handle Transaction Errors
summary: Learn about how to handle transaction errors, such as deadlocks and application retry errors.
---

# トランザクションエラーの処理 {#handle-transaction-errors}

このドキュメントでは、デッドロックやアプリケーションの再試行エラーなどのトランザクションエラーを処理する方法を紹介します。

## デッドロック {#deadlocks}

アプリケーションの次のエラーは、デッドロックの問題を示しています。

```sql
ERROR 1213: Deadlock found when trying to get lock; try restarting transaction
```

デッドロックは、2つ以上のトランザクションが、すでに保持しているロックを解放するために相互に待機している場合、または一貫性のないロック順序により、ロックリソースを待機するループが発生した場合に発生します。

以下は、 [`bookshop`](/develop/dev-guide-bookshop-schema-design.md)データベースのテーブル`books`を使用したデッドロックの例です。

まず、テーブル`books`に2行を挿入します。

```sql
INSERT INTO books (id, title, stock, published_at) VALUES (1, 'book-1', 10, now()), (2, 'book-2', 10, now());
```

TiDBペシミスティックトランザクションモードでは、2つのクライアントがそれぞれ次のステートメントを実行すると、デッドロックが発生します。

| クライアント-A                                          | クライアントB                                               |
| ------------------------------------------------- | ----------------------------------------------------- |
| 始める;                                              |                                                       |
|                                                   | 始める;                                                  |
| 書籍の更新SETstock= stock-1 WHERE id = 1;              |                                                       |
|                                                   | 書籍の更新SETstock= stock-1 WHERE id = 2;                  |
| 書籍の更新SETstock= stock-1 WHERE id = 2; -実行はブロックされます |                                                       |
|                                                   | 書籍の更新SETstock= stock-1 WHERE id = 1; -デッドロックエラーが発生します |

クライアントBでデッドロックエラーが発生すると、TiDBはクライアントBのトランザクションを自動的にロールバックします。クライアントAで`id=2`を更新すると正常に実行されます。その後、 `COMMIT`を実行してトランザクションを終了できます。

### 解決策1：デッドロックを回避する {#solution-1-avoid-deadlocks}

パフォーマンスを向上させるために、ビジネスロジックまたはスキーマ設計を調整することにより、アプリケーションレベルでのデッドロックを回避できます。上記の例では、client-Bもclient-Aと同じ更新順序を使用している場合、つまり、最初に`id=1`で本を更新し、次に`id=2`で本を更新します。これにより、デッドロックを回避できます。

| クライアント-A                             | クライアントB                                        |
| ------------------------------------ | ---------------------------------------------- |
| 始める;                                 |                                                |
|                                      | 始める;                                           |
| 書籍の更新SETstock= stock-1 WHERE id = 1; |                                                |
|                                      | 書籍の更新SETstock= stock-1 WHERE id = 1; -ブロックされます |
| 書籍の更新SETstock= stock-1 WHERE id = 2; |                                                |
| 専念;                                  |                                                |
|                                      | 書籍の更新SETstock= stock-1 WHERE id = 2;           |
|                                      | 専念;                                            |

または、1つのSQLステートメントで2冊の本を更新することもできます。これにより、デッドロックを回避し、より効率的に実行することもできます。

```sql
UPDATE books SET stock=stock-1 WHERE id IN (1, 2);
```

### 解決策2：トランザクションの粒度を下げる {#solution-2-reduce-transaction-granularity}

各トランザクションで1冊の本のみを更新する場合は、デッドロックを回避することもできます。ただし、トレードオフは、トランザクションの粒度が小さすぎるとパフォーマンスに影響を与える可能性があることです。

### 解決策3：楽観的なトランザクションを使用する {#solution-3-use-optimistic-transactions}

楽観的なトランザクションモデルにはデッドロックはありません。ただし、アプリケーションでは、失敗した場合に備えて、楽観的なトランザクション再試行ロジックを追加する必要があります。詳細については、 [アプリケーションの再試行とエラー処理](#application-retry-and-error-handling)を参照してください。

### 解決策4：再試行 {#solution-4-retry}

エラーメッセージに示されているように、アプリケーションに再試行ロジックを追加します。詳細については、 [アプリケーションの再試行とエラー処理](#application-retry-and-error-handling)を参照してください。

## アプリケーションの再試行とエラー処理 {#application-retry-and-error-handling}

TiDBはMySQLと可能な限り互換性がありますが、その分散システムの性質により、特定の違いが生じます。それらの1つはトランザクションモデルです。

開発者がデータベースに接続するために使用するアダプタとORMは、MySQLやOracleなどの従来のデータベース用に調整されています。これらのデータベースでは、トランザクションがデフォルトの分離レベルでコミットに失敗することはめったにないため、再試行メカニズムは必要ありません。トランザクションのコミットに失敗すると、これらのデータベースでは例外として扱われるため、これらのクライアントはエラーのために中止されます。

MySQLなどの従来のデータベースとは異なり、TiDBでは、楽観的なトランザクションモデルを使用し、コミットの失敗を回避したい場合は、アプリケーションで関連する例外を処理するメカニズムを追加する必要があります。

次のPython擬似コードは、アプリケーションレベルの再試行を実装する方法を示しています。高度な再試行ロジックを実装するためにドライバーやORMは必要ありません。あらゆるプログラミング言語または環境で使用できます。

再試行ロジックは、次のルールに従う必要があります。

-   再試行の失敗回数が`max_retries`の制限に達すると、エラーがスローされます。
-   `try ... catch ...`を使用して、SQL実行例外をキャッチします。次のエラーが発生した場合は、再試行してください。他のエラーが発生した場合はロールバックします。エラーコードの詳細については、 [エラーコードとトラブルシューティング](/error-codes.md)を参照してください。
    -   `Error 8002: can not retry select for update statement` ：SELECTFORUPDATE書き込み競合エラー
    -   `Error 8022: Error: KV error safe to retry` ：トランザクションコミット失敗エラー。
    -   `Error 8028: Information schema is changed during the execution of the statement` ：テーブルスキーマがDDL操作によって変更されたため、トランザクションのコミットでエラーが発生しました。
    -   `Error 9007: Write conflict` ：書き込み競合エラー。通常、楽観的なトランザクションモードが使用されているときに、複数のトランザクションが同じデータ行を変更することによって発生します。
-   `COMMIT`ブロックの最後のトランザクション。

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
            connnection.exec('ROLLBACK');

            # Capture the error types that require application-side retry,
            # wait for a short period of time,
            # and exponentially increase the wait time for each transaction failure
            sleep_ms = int(((1.5 ** n) + rand) * 100)
            sleep(sleep_ms) # make sure your sleep() takes milliseconds
```

> ノート：
>
> `Error 9007: Write conflict`が頻繁に発生する場合は、スキーマの設計とワークロードのデータアクセスパターンを確認して、競合の根本原因を特定し、より適切な設計で競合を回避する必要があります。トランザクションの競合をトラブルシューティングして解決する方法については、 [ロックの競合のトラブルシューティング](/troubleshoot-lock-conflicts.md)を参照してください。

## も参照してください {#see-also}

-   [ロックの競合のトラブルシューティング](/troubleshoot-lock-conflicts.md)
-   [楽観的なトランザクションでの書き込みの競合のトラブルシューティング](/troubleshoot-write-conflicts.md)
