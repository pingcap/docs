---
title: Handle Transaction Errors
summary: Learn about how to handle transaction errors, such as deadlocks and application retry errors.
---

# トランザクションエラーの処理 {#handle-transaction-errors}

このドキュメントでは、デッドロックやアプリケーションの再試行エラーなどのトランザクション エラーを処理する方法を紹介します。

## デッドロック {#deadlocks}

アプリケーション内の次のエラーは、デッドロックの問題を示しています。

```sql
ERROR 1213: Deadlock found when trying to get lock; try restarting transaction
```

デッドロックは、2 つ以上のトランザクションが、すでに保持しているロックを解放するのをお互いに待っている場合、またはロック順序が矛盾しているため、ロック リソースを待機するループが発生する場合に発生します。

以下は、データベース[`bookshop`](/develop/dev-guide-bookshop-schema-design.md)のテーブル`books`を使用したデッドロックの例です。

まず、テーブル`books`に 2 行を挿入します。

```sql
INSERT INTO books (id, title, stock, published_at) VALUES (1, 'book-1', 10, now()), (2, 'book-2', 10, now());
```

TiDB悲観的トランザクション モードでは、2 つのクライアントがそれぞれ次のステートメントを実行すると、デッドロックが発生します。

| クライアントA                                            | クライアントB                                               |
| -------------------------------------------------- | ----------------------------------------------------- |
| 始める;                                               |                                                       |
|                                                    | 始める;                                                  |
| 書籍を更新 SET Stock=stock-1 WHERE id=1;                |                                                       |
|                                                    | 書籍を更新 SET Stock=stock-1 WHERE id=2;                   |
| 書籍を更新 SET Stock=stock-1 WHERE id=2; -- 実行はブロックされます |                                                       |
|                                                    | 書籍を更新 SET Stock=stock-1 WHERE id=1; -- デッドロックエラーが発生する |

クライアント B でデッドロック エラーが発生すると、TiDB はクライアント B のトランザクションを自動的にロールバックします。 client-A での更新`id=2`正常に実行されます。次に`COMMIT`実行してトランザクションを終了します。

### 解決策 1: デッドロックを回避する {#solution-1-avoid-deadlocks}

パフォーマンスを向上させるには、ビジネス ロジックまたはスキーマ設計を調整することで、アプリケーション レベルでのデッドロックを回避できます。上の例では、クライアント B もクライアント A と同じ更新順序を使用する場合、つまり、最初に`id=1`で書籍を更新し、次に`id=2`で書籍を更新します。これにより、デッドロックを回避できます。

| クライアントA                             | クライアントB                                         |
| ----------------------------------- | ----------------------------------------------- |
| 始める;                                |                                                 |
|                                     | 始める;                                            |
| 書籍を更新 SET Stock=stock-1 WHERE id=1; |                                                 |
|                                     | 書籍を更新 SET Stock=stock-1 WHERE id=1; -- ブロックされます |
| 書籍を更新 SET Stock=stock-1 WHERE id=2; |                                                 |
| 専念;                                 |                                                 |
|                                     | 書籍を更新 SET Stock=stock-1 WHERE id=2;             |
|                                     | 専念;                                             |

あるいは、1 つの SQL ステートメントで 2 つのブックを更新することもできます。これにより、デッドロックを回避し、より効率的に実行できます。

```sql
UPDATE books SET stock=stock-1 WHERE id IN (1, 2);
```

### 解決策 2: トランザクションの粒度を下げる {#solution-2-reduce-transaction-granularity}

各トランザクションで 1 冊のブックのみを更新する場合も、デッドロックを回避できます。ただし、トランザクションの粒度が小さすぎるとパフォーマンスに影響を与える可能性があるというトレードオフがあります。

### 解決策 3:楽観的トランザクションを使用する {#solution-3-use-optimistic-transactions}

楽観的トランザクション モデルにはデッドロックがありません。ただし、アプリケーションでは、失敗した場合に備えて楽観的トランザクション再試行ロジックを追加する必要があります。詳細は[アプリケーションの再試行とエラー処理](#application-retry-and-error-handling)を参照してください。

### 解決策 4: 再試行する {#solution-4-retry}

エラー メッセージに示されているように、アプリケーションに再試行ロジックを追加します。詳細は[アプリケーションの再試行とエラー処理](#application-retry-and-error-handling)を参照してください。

## アプリケーションの再試行とエラー処理 {#application-retry-and-error-handling}

TiDB は MySQL と可能な限り互換性がありますが、その分散システムの性質により、特定の違いが生じます。その 1 つはトランザクション モデルです。

開発者がデータベースに接続するために使用するアダプターと ORM は、MySQL や Oracle などの従来のデータベースに合わせて調整されています。これらのデータベースでは、トランザクションがデフォルトの分離レベルでコミットに失敗することはほとんどないため、再試行メカニズムは必要ありません。トランザクションがコミットに失敗すると、これらのデータベースでは例外として扱われるため、これらのクライアントはエラーにより中止されます。

MySQL などの従来のデータベースとは異なり、TiDB では楽観的トランザクション モデルを使用し、コミットの失敗を回避したい場合は、関連する例外を処理するメカニズムをアプリケーションに追加する必要があります。

次の Python 疑似コードは、アプリケーション レベルの再試行を実装する方法を示しています。ドライバーや ORM が高度な再試行ロジックを実装する必要はありません。あらゆるプログラミング言語や環境で使用できます。

再試行ロジックは次のルールに従う必要があります。

-   失敗した再試行の数が`max_retries`制限に達すると、エラーがスローされます。
-   SQL 実行例外をキャッチするには`try ... catch ...`を使用します。次のエラーが発生した場合は、再試行してください。他のエラーが発生した場合はロールバックします。
    -   `Error 8002: can not retry select for update statement` : SELECT FOR UPDATE書き込み競合エラー
    -   `Error 8022: Error: KV error safe to retry` : トランザクションのコミット失敗エラー。
    -   `Error 8028: Information schema is changed during the execution of the statement` : テーブル スキーマが DDL 操作によって変更されたため、トランザクション コミットでエラーが発生しました。
    -   `Error 9007: Write conflict` : 書き込み競合エラー。通常、楽観的トランザクション モードの使用時に複数のトランザクションが同じデータ行を変更することによって発生します。
-   `COMMIT` try ブロックの最後のトランザクション。

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

> **注記：**
>
> `Error 9007: Write conflict`頻繁に発生する場合は、スキーマ設計とワークロードのデータ アクセス パターンをチェックして競合の根本原因を特定し、より適切な設計によって競合を回避する必要がある場合があります。

<CustomContent platform="tidb">

トランザクション競合のトラブルシューティングと解決方法については、 [ロックの競合のトラブルシューティング](/troubleshoot-lock-conflicts.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

トランザクション競合のトラブルシューティングと解決方法については、 [ロックの競合のトラブルシューティング](https://docs.pingcap.com/tidb/stable/troubleshoot-lock-conflicts)を参照してください。

</CustomContent>

## こちらも参照 {#see-also}

<CustomContent platform="tidb">

-   [オプティミスティック トランザクションでの書き込み競合のトラブルシューティング](/troubleshoot-write-conflicts.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [オプティミスティック トランザクションでの書き込み競合のトラブルシューティング](https://docs.pingcap.com/tidb/stable/troubleshoot-write-conflicts)

</CustomContent>
