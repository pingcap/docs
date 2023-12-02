---
title: Troubleshoot Write Conflicts in Optimistic Transactions
summary: Learn about the reason of and solutions to write conflicts in optimistic transactions.
---

# オプティミスティック トランザクションでの書き込み競合のトラブルシューティング {#troubleshoot-write-conflicts-in-optimistic-transactions}

このドキュメントでは、楽観的トランザクションでの書き込み競合の原因と解決策を紹介します。

TiDB v3.0.8 より前では、TiDB はデフォルトで楽観的トランザクション モデルを使用します。このモデルでは、TiDB はトランザクションの実行中に競合をチェックしません。代わりに、トランザクションが最終的にコミットされる間に、2 フェーズ コミット (2PC) がトリガーされ、TiDB が書き込み競合をチェックします。書き込み競合が存在し、自動再試行メカニズムが有効になっている場合、TiDB は制限時間内にトランザクションを再試行します。リトライが成功した場合、またはリトライ回数の上限に達した場合、TiDB はトランザクションの実行結果をクライアントに返します。したがって、TiDB クラスター内に多くの書き込み競合が存在する場合、時間が長くなる可能性があります。

## 書き込み競合の理由 {#the-reason-of-write-conflicts}

TiDB は、 [パーコレーター](https://www.usenix.org/legacy/event/osdi10/tech/full_papers/Peng.pdf)トランザクション モデルを使用してトランザクションを実装します。 `percolator`は一般に 2PC の実装です。 2PC プロセスの詳細については、 [TiDB 楽観的トランザクションモデル](/optimistic-transaction.md)を参照してください。

クライアントが`COMMIT`リクエストを TiDB に送信した後、TiDB は 2PC プロセスを開始します。

1.  TiDB は、トランザクション内のすべてのキーから 1 つのキーをトランザクションの主キーとして選択します。
2.  TiDB は、このコミットに関係するすべての TiKV リージョンに`prewrite`リクエストを送信します。 TiKV は、すべてのキーが正常にプレビューできるかどうかを判断します。
3.  TiDB は、すべての`prewrite`リクエストが成功したという結果を受け取ります。
4.  TiDB は PD から`commit_ts`を取得します。
5.  TiDB は、トランザクションの主キーを含む`commit`リクエストを TiKVリージョンに送信します。 TiKV は`commit`リクエストを受信すると、データの有効性をチェックし、 `prewrite`段階で残ったロックをクリアします。
6.  `commit`リクエストが正常に返された後、TiDB はクライアントに成功を返します。

書き込み競合は`prewrite`ステージで発生します。別のトランザクションが現在のキー ( `data.commit_ts` &gt; `txn.start_ts` ) を書き込んでいることをトランザクションが検出すると、書き込み競合が発生します。

## 書き込み競合の検出 {#detect-write-conflicts}

TiDB Grafana パネルの**KV エラー**で次の監視メトリクスを確認します。

-   **KV バックオフ OPS は、** TiKV によって返される 1 秒あたりのエラー メッセージの数を示します。

    ![kv-backoff-ops](/media/troubleshooting-write-conflict-kv-backoff-ops.png)

    `txnlock`メトリックは、書き込みと書き込みの競合を示します。 `txnLockFast`メトリックは、読み取り/書き込みの競合を示します。

-   **Lock Resolve OPS は、** 1 秒あたりのトランザクション競合に関連するアイテムの数を示します。

    ![lock-resolve-ops](/media/troubleshooting-write-conflict-lock-resolve-ops.png)

    -   `not_expired`ロックの TTL が期限切れになっていないことを示します。競合トランザクションは、TTL が期限切れになるまでロックを解決できません。
    -   `wait_expired` 、トランザクションがロックの有効期限が切れるまで待つ必要があることを示します。
    -   `expired`ロックの TTL が期限切れであることを示します。その後、競合トランザクションはこのロックを解決できます。

-   **KV 再試行期間は、** KV リクエストを再送信する期間を示します。

    ![kv-retry-duration](/media/troubleshooting-write-conflict-kv-retry-duration.png)

TiDB ログ内を検索するキーワードとして`[kv:9007]Write conflict`を使用することもできます。キーワードは、クラスター内に書き込み競合が存在することも示します。

## 書き込み競合を解決する {#resolve-write-conflicts}

クラスター内に多数の書き込み競合が存在する場合は、書き込み競合キーとその理由を特定し、書き込み競合を回避するためにアプリケーション ロジックを変更してみることをお勧めします。クラスター内に書き込み競合が存在する場合、TiDB ログ ファイルに次のようなログが表示されます。

```log
[2020/05/12 15:17:01.568 +08:00] [WARN] [session.go:446] ["commit failed"] [conn=3] ["finished txn"="Txn{state=invalid}"] [error="[kv:9007]Write conflict, txnStartTS=416617006551793665, conflictStartTS=416617018650001409, conflictCommitTS=416617023093080065, key={tableID=47, indexID=1, indexValues={string, }} primary={tableID=47, indexID=1, indexValues={string, }} [try again later]"]
```

上記のログの説明は次のとおりです。

-   `[kv:9007]Write conflict` : 書き込みと書き込みの競合を示します。
-   `txnStartTS=416617006551793665` : 現在のトランザクションの`start_ts`を示します。 `pd-ctl`ツールを使用すると、 `start_ts`物理時間に変換できます。
-   `conflictStartTS=416617018650001409` : 書き込み競合トランザクションの`start_ts`を示します。
-   `conflictCommitTS=416617023093080065` : 書き込み競合トランザクションの`commit_ts`を示します。
-   `key={tableID=47, indexID=1, indexValues={string, }}` : 書き込み競合キーを示します。 `tableID`書き込み競合テーブルの ID を示します。 `indexID`書き込み競合インデックスの ID を示します。書き込み競合キーがレコード キーの場合、ログには`handle=x`出力、どのレコード (行) に競合があるかを示します。 `indexValues`競合があるインデックスの値を示します。
-   `primary={tableID=47, indexID=1, indexValues={string, }}` : 現在のトランザクションの主キー情報を示します。

`pd-ctl`ツールを使用して、タイムスタンプを読み取り可能な時刻に変換できます。

```shell
tiup ctl:v<CLUSTER_VERSION> pd -u https://127.0.0.1:2379 tso {TIMESTAMP}
```

`tableID`を使用すると、関連テーブルの名前を見つけることができます。

```shell
curl http://{TiDBIP}:10080/db-table/{tableID}
```

`indexID`とテーブル名を使用して、関連インデックスの名前を見つけることができます。

```sql
SELECT * FROM INFORMATION_SCHEMA.TIDB_INDEXES WHERE TABLE_SCHEMA='{db_name}' AND TABLE_NAME='{table_name}' AND INDEX_ID={indexID};
```

さらに、TiDB v3.0.8 以降のバージョンでは、悲観的トランザクションがデフォルト モードになります。悲観的トランザクション モードでは、トランザクションの事前書き込み段階での書き込み競合を回避できるため、アプリケーションを変更する必要がなくなりました。悲観的トランザクション モードでは、各 DML ステートメントは実行中に関連するキーに悲観的ロックを書き込みます。この悲観的ロックにより、他のトランザクションが同じキーを変更するのを防ぐことができるため、トランザクション 2PC の`prewrite`ステージで書き込み競合が存在しないことが保証されます。
