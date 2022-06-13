---
title: Troubleshoot Write Conflicts in Optimistic Transactions
summary: Learn about the reason of and solutions to write conflicts in optimistic transactions.
---

# 楽観的なトランザクションでの書き込みの競合のトラブルシューティング {#troubleshoot-write-conflicts-in-optimistic-transactions}

このドキュメントでは、楽観的なトランザクションで競合を書き込む理由と解決策を紹介します。

TiDB v3.0.8より前では、TiDBはデフォルトで楽観的なトランザクションモデルを使用していました。このモデルでは、TiDBはトランザクションの実行中に競合をチェックしません。代わりに、トランザクションが最終的にコミットされている間に、2フェーズコミット（2PC）がトリガーされ、TiDBチェックで書き込みの競合が発生します。書き込みの競合が存在し、自動再試行メカニズムが有効になっている場合、TiDBは限られた時間内にトランザクションを再試行します。再試行が成功するか、再試行時間の上限に達した場合、TiDBはトランザクション実行の結果をクライアントに返します。したがって、TiDBクラスタに多くの書き込みの競合が存在する場合、期間が長くなる可能性があります。

## 書き込みの競合の理由 {#the-reason-of-write-conflicts}

TiDBは、 [パーコレーター](https://www.usenix.org/legacy/event/osdi10/tech/full_papers/Peng.pdf)トランザクションモデルを使用してトランザクションを実装します。 `percolator`は一般的に2PCの実装です。詳細な2PCプロセスについては、 [TiDBオプティミスティックトランザクションモデル](/optimistic-transaction.md)を参照してください。

クライアントがTiDBに`COMMIT`の要求を送信した後、TiDBは2PCプロセスを開始します。

1.  TiDBは、トランザクションのすべてのキーから1つのキーをトランザクションの主キーとして選択します。
2.  TiDBは、このコミットに関係するすべてのTiKVリージョンに`prewrite`のリクエストを送信します。 TiKVは、すべてのキーが正常にプレビューできるかどうかを判断します。
3.  TiDBは、 `prewrite`の要求すべてが成功したという結果を受け取ります。
4.  TiDBはPDから`commit_ts`を取得します。
5.  TiDBは、トランザクションの主キーを含むTiKVリージョンに`commit`の要求を送信します。 TiKVは`commit`リクエストを受信した後、データの有効性をチェックし、 `prewrite`ステージに残っているロックをクリアします。
6.  `commit`の要求が正常に返された後、TiDBは成功をクライアントに返します。

書き込みの競合は`prewrite`段階で発生します。別のトランザクションが現在のキーを書き込んでいることをトランザクションが検出すると（ `data.commit_ts` &gt; `txn.start_ts` ）、書き込みの競合が発生します。

## 書き込みの競合を検出する {#detect-write-conflicts}

TiDB Grafanaパネルで、 **KVエラー**の下にある次の監視メトリックを確認します。

-   **KVバックオフOPS**は、TiKVによって返される1秒あたりのエラーメッセージの数を示します。

    ![kv-backoff-ops](/media/troubleshooting-write-conflict-kv-backoff-ops.png)

    `txnlock`メトリックは、書き込みと書き込みの競合を示します。 `txnLockFast`メトリックは、読み取りと書き込みの競合を示します。

-   **Lock Resolve OPS**は、1秒あたりのトランザクション競合に関連するアイテムの数を示します。

    ![lock-resolve-ops](/media/troubleshooting-write-conflict-lock-resolve-ops.png)

    -   `not_expired`は、ロックのTTLが期限切れになっていないことを示します。競合トランザクションは、TTLが期限切れになるまでロックを解決できません。
    -   `wait_expired`は、トランザクションがロックの有効期限が切れるのを待つ必要があることを示します。
    -   `expired`は、ロックのTTLが期限切れになったことを示します。次に、競合トランザクションはこのロックを解決できます。

-   **KV再試行期間**は、KV要求を再送信する期間を示します。

    ![kv-retry-duration](/media/troubleshooting-write-conflict-kv-retry-duration.png)

TiDBログで検索するキーワードとして`[kv:9007]Write conflict`を使用することもできます。キーワードは、書き込みの競合がクラスタに存在することも示します。

## 書き込みの競合を解決する {#resolve-write-conflicts}

クラスタに多くの書き込み競合が存在する場合は、書き込み競合キーとその理由を確認してから、書き込み競合を回避するためにアプリケーションロジックを変更することをお勧めします。クラスタに書き込みの競合が存在する場合、TiDBログファイルに次のようなログが表示されます。

```log
[2020/05/12 15:17:01.568 +08:00] [WARN] [session.go:446] ["commit failed"] [conn=3] ["finished txn"="Txn{state=invalid}"] [error="[kv:9007]Write conflict, txnStartTS=416617006551793665, conflictStartTS=416617018650001409, conflictCommitTS=416617023093080065, key={tableID=47, indexID=1, indexValues={string, }} primary={tableID=47, indexID=1, indexValues={string, }} [try again later]"]
```

上記のログの説明は次のとおりです。

-   `[kv:9007]Write conflict` ：書き込みと書き込みの競合を示します。
-   `txnStartTS=416617006551793665` ：現在のトランザクションの`start_ts`を示します。 `pd-ctl`ツールを使用して、 `start_ts`を物理時間に変換できます。
-   `conflictStartTS=416617018650001409` ：書き込み競合トランザクションの`start_ts`を示します。
-   `conflictCommitTS=416617023093080065` ：書き込み競合トランザクションの`commit_ts`を示します。
-   `key={tableID=47, indexID=1, indexValues={string, }}` ：書き込み競合キーを示します。 `tableID`は、書き込み競合テーブルのIDを示します。 `indexID`は書き込み競合インデックスのIDを示します。書き込み競合キーがレコードキーの場合、ログは`handle=x`を出力し、どのレコード（行）に競合があるかを示します。 `indexValues`は、競合するインデックスの値を示します。
-   `primary={tableID=47, indexID=1, indexValues={string, }}` ：現在のトランザクションの主キー情報を示します。

`pd-ctl`ツールを使用して、タイムスタンプを読み取り可能な時間に変換できます。

{{< copyable "" >}}

```shell
tiup ctl pd -u https://127.0.0.1:2379 tso {TIMESTAMP}
```

`tableID`を使用して、関連するテーブルの名前を見つけることができます。

{{< copyable "" >}}

```shell
curl http://{TiDBIP}:10080/db-table/{tableID}
```

`indexID`とテーブル名を使用して、関連するインデックスの名前を見つけることができます。

{{< copyable "" >}}

```sql
SELECT * FROM INFORMATION_SCHEMA.TIDB_INDEXES WHERE TABLE_SCHEMA='{db_name}' AND TABLE_NAME='{table_name}' AND INDEX_ID={indexID};
```

さらに、TiDB v3.0.8以降のバージョンでは、ペシミスティックトランザクションがデフォルトモードになります。ペシミスティックトランザクションモードでは、トランザクションの事前書き込み段階での書き込みの競合を回避できるため、アプリケーションを変更する必要はありません。ペシミスティックトランザクションモードでは、各DMLステートメントは、実行中に関連するキーにペシミスティックロックを書き込みます。この悲観的なロックは、他のトランザクションが同じキーを変更するのを防ぐことができるため、トランザクション2PCの`prewrite`のステージで書き込みの競合が発生しないようにします。
