---
title: Troubleshoot Write Conflicts in Optimistic Transactions
summary: 楽観的トランザクションにおける書き込み競合の原因と解決策について学習します。
---

# 楽観的トランザクションにおける書き込み競合のトラブルシューティング {#troubleshoot-write-conflicts-in-optimistic-transactions}

このドキュメントでは、楽観的トランザクションにおける書き込み競合の原因と解決策を紹介します。

TiDB v3.0.8より前のバージョンでは、TiDBはデフォルトで楽観的トランザクションモデルを使用しています。このモデルでは、TiDBはトランザクション実行中に競合をチェックしません。代わりに、トランザクションが最終的にコミットされる際に2相コミット（2PC）がトリガーされ、TiDBは書き込み競合をチェックします。書き込み競合が存在し、自動再試行メカニズムが有効になっている場合、TiDBは制限時間内にトランザクションを再試行します。再試行が成功するか、再試行回数の上限に達した場合、TiDBはトランザクション実行結果をクライアントに返します。そのため、TiDBクラスタ内に書き込み競合が多数存在する場合、この期間は長くなる可能性があります。

## 書き込み競合の原因 {#the-reason-of-write-conflicts}

TiDBは[パーコレーター](https://www.usenix.org/legacy/event/osdi10/tech/full_papers/Peng.pdf)トランザクションモデルを用いてトランザクションを実装します。3 `percolator`一般的に2PCの実装です。2PCの詳細なプロセスについては[TiDB 楽観的トランザクションモデル](/optimistic-transaction.md)参照してください。

クライアントが TiDB に`COMMIT`リクエストを送信すると、TiDB は 2PC プロセスを開始します。

1.  TiDB は、トランザクション内のすべてのキーから 1 つのキーをトランザクションの主キーとして選択します。
2.  TiDBは、このコミットに関係するすべてのTiKVリージョンに`prewrite`リクエストを送信します。TiKVは、すべてのキーが正常にプレビューできるかどうかを判断します。
3.  TiDB は、 `prewrite`リクエストがすべて成功したという結果を受け取ります。
4.  TiDB は PD から`commit_ts`を取得します。
5.  TiDBは、トランザクションの主キーを含むTiKVリージョンに`commit`リクエストを送信します。TiKVは`commit`リクエストを受信すると、データの有効性を確認し、 `prewrite`番目のステージに残っているロックを解除します。
6.  `commit`回目のリクエストが正常に返されると、TiDB はクライアントに成功を返します。

書き込み競合はステージ`prewrite`で発生します。トランザクションが、別のトランザクションが現在のキー（ `data.commit_ts` &gt; `txn.start_ts` ）に書き込みを行っていることを検出すると、書き込み競合が発生します。

## 書き込み競合を検出する {#detect-write-conflicts}

TiDB Grafana パネルで、 **KV エラー**の下にある次の監視メトリックを確認します。

-   **KV バックオフ OPS は**、TiKV によって返される 1 秒あたりのエラー メッセージの数を示します。

    ![kv-backoff-ops](/media/troubleshooting-write-conflict-kv-backoff-ops.png)

    メトリック`txnlock`は書き込み競合を示します。メトリック`txnLockFast`は読み取り競合を示します。

-   **ロック解決 OPS は、** 1 秒あたりのトランザクション競合に関連する項目の数を示します。

    ![lock-resolve-ops](/media/troubleshooting-write-conflict-lock-resolve-ops.png)

    -   `not_expired` 、ロックのTTLが期限切れになっていないことを示します。競合トランザクションは、TTLが期限切れになるまでロックを解決できません。
    -   `wait_expired` 、トランザクションがロックの有効期限が切れるまで待機する必要があることを示します。
    -   `expired`ロックのTTLが期限切れであることを示します。その後、競合トランザクションはこのロックを解決できます。

-   **KV 再試行期間は、** KV 要求を再送信する期間を示します。

    ![kv-retry-duration](/media/troubleshooting-write-conflict-kv-retry-duration.png)

TiDBログを検索するキーワードとして`[kv:9007]Write conflict`を使用することもできます。このキーワードは、クラスター内で書き込み競合が発生していることを示します。

## 書き込み競合を解決する {#resolve-write-conflicts}

クラスター内で書き込み競合が多数発生している場合は、書き込み競合のキーとその理由を特定し、書き込み競合を回避するためにアプリケーションロジックを変更することを推奨します。クラスター内で書き込み競合が発生している場合、TiDBログファイルに次のようなログが記録されます。

```log
[2020/05/12 15:17:01.568 +08:00] [WARN] [session.go:446] ["commit failed"] [conn=3] ["finished txn"="Txn{state=invalid}"] [error="[kv:9007]Write conflict, txnStartTS=416617006551793665, conflictStartTS=416617018650001409, conflictCommitTS=416617023093080065, key={tableID=47, indexID=1, indexValues={string, }} primary={tableID=47, indexID=1, indexValues={string, }} [try again later]"]
```

上記のログの説明は次のとおりです。

-   `[kv:9007]Write conflict` : 書き込み間の競合を示します。
-   `txnStartTS=416617006551793665` : 現在のトランザクションの`start_ts`示します。4ツール`pd-ctl`使用して、 `start_ts`物理時間に変換できます。
-   `conflictStartTS=416617018650001409` : 書き込み競合トランザクションの`start_ts`示します。
-   `conflictCommitTS=416617023093080065` : 書き込み競合トランザクションの`commit_ts`示します。
-   `key={tableID=47, indexID=1, indexValues={string, }}` : 書き込み競合キーを示します。2 `tableID`書き込み競合テーブルのIDを示します。4 `indexID`書き込み競合インデックスのIDを示します。書き込み競合キーがレコードキーの場合、ログには競合が発生しているレコード（行）を示す`handle=x`が出力。8 `indexValues`競合が発生しているインデックスの値を示します。
-   `primary={tableID=47, indexID=1, indexValues={string, }}` : 現在のトランザクションの主キー情報を示します。

`pd-ctl`ツールを使用して、タイムスタンプを読み取り可能な時間に変換できます。

```shell
tiup ctl:v<CLUSTER_VERSION> pd -u https://127.0.0.1:2379 tso {TIMESTAMP}
```

`tableID`使用して、関連するテーブルの名前を見つけることができます。

```shell
curl http://{TiDBIP}:10080/db-table/{TableID}
```

`indexID`とテーブル名を使用して、関連するインデックスの名前を見つけることができます。

```sql
SELECT * FROM INFORMATION_SCHEMA.TIDB_INDEXES WHERE TABLE_SCHEMA='{db_name}' AND TABLE_NAME='{table_name}' AND INDEX_ID={indexID};
```

さらに、TiDB v3.0.8以降のバージョンでは、悲観的トランザクションがデフォルトモードになります。悲観的トランザクションモードでは、トランザクションの事前書き込みステージにおける書き込み競合を回避できるため、アプリケーションを変更する必要がなくなります。悲観的トランザクションモードでは、各DML文は実行中に関連するキーに悲観的ロックを書き込みます。この悲観的ロックにより、他のトランザクションによる同じキーの変更を防止できるため、トランザクションの2PCステージ`prewrite`における書き込み競合の発生を確実に防ぐことができます。
