---
title: Handle Transaction Errors
summary: デッドロックやアプリケーション再試行エラーなどのトランザクション エラーを処理する方法について学習します。
---

# トランザクションエラーの処理 {#handle-transaction-errors}

このドキュメントでは、デッドロックやアプリケーション再試行エラーなどのトランザクション エラーを処理する方法について説明します。

## デッドロック {#deadlocks}

アプリケーション内の次のエラーは、デッドロックの問題を示しています。

```sql
ERROR 1213: Deadlock found when trying to get lock; try restarting transaction
```

デッドロックは、2 つ以上のトランザクションが、既に保持しているロックを互いに解放するのを待機している場合、またはロックの順序に一貫性がないためにロック リソースを待機するループが発生した場合に発生します。

以下は、データベース[`bookshop`](/develop/dev-guide-bookshop-schema-design.md)のテーブル`books`を使用したデッドロックの例です。

まず、表`books`に 2 行挿入します。

```sql
INSERT INTO books (id, title, stock, published_at) VALUES (1, 'book-1', 10, now()), (2, 'book-2', 10, now());
```

TiDB悲観的トランザクション モードでは、2 つのクライアントがそれぞれ次のステートメントを実行すると、デッドロックが発生します。

| クライアントA                                                   | クライアントB                                                       |
| --------------------------------------------------------- | ------------------------------------------------------------- |
| 始める;                                                      |                                                               |
|                                                           | 始める;                                                          |
| 本を更新します。set stock=stock-1 WHERE id=1;                     |                                                               |
|                                                           | 本を更新します。set stock=stock-1 WHERE id=2;                         |
| UPDATE books SET stock=stock-1 WHERE id=2; -- 実行はブロックされます |                                                               |
|                                                           | UPDATE books SET stock=stock-1 WHERE id=1; -- デッドロックエラーが発生します |

クライアント B でデッドロック エラーが発生すると、TiDB は自動的にクライアント B のトランザクションをロールバックします。クライアント A の`id=2`更新は正常に実行されます。その後、 `COMMIT`実行してトランザクションを終了できます。

### 解決策1: デッドロックを回避する {#solution-1-avoid-deadlocks}

パフォーマンスを向上させるには、ビジネス ロジックまたはスキーマ設計を調整して、アプリケーション レベルでデッドロックを回避できます。上記の例では、クライアント B もクライアント A と同じ更新順序を使用する場合、つまり、最初に`id=1`で本を更新し、次に`id=2`で本を更新します。これにより、デッドロックを回避できます。

| クライアントA                               | クライアントB                                                |
| ------------------------------------- | ------------------------------------------------------ |
| 始める;                                  |                                                        |
|                                       | 始める;                                                   |
| 本を更新します。set stock=stock-1 WHERE id=1; |                                                        |
|                                       | UPDATE books SET stock=stock-1 WHERE id=1; -- ブロックされます |
| 本を更新します。set stock=stock-1 WHERE id=2; |                                                        |
| 専念;                                   |                                                        |
|                                       | 本を更新します。set stock=stock-1 WHERE id=2;                  |
|                                       | 専念;                                                    |

あるいは、1 つの SQL ステートメントで 2 冊の本を更新することもできます。これにより、デッドロックを回避し、より効率的に実行できます。

```sql
UPDATE books SET stock=stock-1 WHERE id IN (1, 2);
```

### 解決策2: トランザクションの粒度を下げる {#solution-2-reduce-transaction-granularity}

各トランザクションで 1 冊のみを更新する場合も、デッドロックを回避できます。ただし、トレードオフとして、トランザクションの粒度が小さすぎるとパフォーマンスに影響する可能性があります。

### 解決策3:楽観的トランザクションを使用する {#solution-3-use-optimistic-transactions}

楽観的トランザクション モデルではデッドロックは発生しません。ただし、アプリケーションでは、障害が発生した場合に備えて楽観的トランザクションの再試行ロジックを追加する必要があります。詳細については、 [アプリケーションの再試行とエラー処理](#application-retry-and-error-handling)参照してください。

### 解決策4: 再試行 {#solution-4-retry}

エラー メッセージで提案されているように、アプリケーションに再試行ロジックを追加します。詳細については、 [アプリケーションの再試行とエラー処理](#application-retry-and-error-handling)参照してください。

## アプリケーションの再試行とエラー処理 {#application-retry-and-error-handling}

TiDB は MySQL と可能な限り互換性がありますが、分散システムの性質上、いくつかの違いがあります。その 1 つがトランザクション モデルです。

開発者がデータベースに接続するために使用するアダプタと ORM は、MySQL や Oracle などの従来のデータベースに合わせて調整されています。これらのデータベースでは、デフォルトの分離レベルでトランザクションがコミットに失敗することはほとんどないため、再試行メカニズムは必要ありません。トランザクションがコミットに失敗すると、これらのデータベースでは例外として扱われるため、クライアントはエラーのために中止します。

MySQL などの従来のデータベースとは異なり、TiDB では、楽観的トランザクション モデルを使用してコミットの失敗を回避する場合、アプリケーションで関連する例外を処理するメカニズムを追加する必要があります。

次の Python 疑似コードは、アプリケーション レベルの再試行を実装する方法を示しています。高度な再試行ロジックを実装するためにドライバーや ORM は必要ありません。任意のプログラミング言語や環境で使用できます。

再試行ロジックは次のルールに従う必要があります。

-   失敗した再試行回数が`max_retries`制限に達するとエラーがスローされます。
-   SQL 実行例外をキャッチするには`try ... catch ...`使用します。次のエラーが発生した場合は再試行します。その他のエラーが発生した場合はロールバックします。
    -   `Error 8002: can not retry select for update statement` : SELECT FOR UPDATE 書き込み競合エラー
    -   `Error 8022: Error: KV error safe to retry` : トランザクションのコミットに失敗したエラー。
    -   `Error 8028: Information schema is changed during the execution of the statement` : DDL 操作によってテーブル スキーマが変更され、トランザクションのコミットでエラーが発生しました。
    -   `Error 9007: Write conflict` : 書き込み競合エラー。通常、楽観的トランザクション モードが使用されているときに、複数のトランザクションが同じデータ行を変更することによって発生します。
-   `COMMIT` try ブロックの最後にあるトランザクション。

<CustomContent platform="tidb">

エラーコードの詳細については、 [エラーコードとトラブルシューティング](/error-codes.md)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

エラーコードの詳細については、 [エラーコードとトラブルシューティング](https://docs.pingcap.com/tidb/stable/error-codes)参照してください。

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
> `Error 9007: Write conflict`頻繁に発生する場合は、スキーマ設計とワークロードのデータ アクセス パターンを確認して競合の根本原因を特定し、より適切な設計で競合を回避する必要があります。

<CustomContent platform="tidb">

トランザクションの競合のトラブルシューティングと解決方法については、 [ロック競合のトラブルシューティング](/troubleshoot-lock-conflicts.md)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

トランザクションの競合のトラブルシューティングと解決方法については、 [ロック競合のトラブルシューティング](https://docs.pingcap.com/tidb/stable/troubleshoot-lock-conflicts)参照してください。

</CustomContent>

## 参照 {#see-also}

<CustomContent platform="tidb">

-   [楽観的トランザクションにおける書き込み競合のトラブルシューティング](/troubleshoot-write-conflicts.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [楽観的トランザクションにおける書き込み競合のトラブルシューティング](https://docs.pingcap.com/tidb/stable/troubleshoot-write-conflicts)

</CustomContent>

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、または[サポートチケットを送信する](/support.md)についてコミュニティに質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、または[サポートチケットを送信する](https://tidb.support.pingcap.com/)についてコミュニティに質問してください。

</CustomContent>
