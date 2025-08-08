---
title: TiDB Pessimistic Transaction Mode
summary: TiDB の悲観的トランザクション モードについて学習します。
---

# TiDB 悲観的トランザクションモード {#tidb-pessimistic-transaction-mode}

TiDB を従来のデータベースに近づけ、移行コストを削減するため、v3.0 以降では、楽観的トランザクションモデルに加えて悲観的トランザクションモードもサポートしています。このドキュメントでは、TiDB の悲観的トランザクションモードの機能について説明します。

> **注記：**
>
> v3.0.8以降、新規に作成されたTiDBクラスターはデフォルトで悲観的・トランザクション・モードを使用します。ただし、既存のクラスターをv3.0.7以前からv3.0.8以降にアップグレードした場合、この変更は影響を受けません。つまり、**新規に作成されたクラスターのみがデフォルトで悲観的・トランザクション・モードを使用するようになります**。

## トランザクションモードの切り替え {#switch-transaction-mode}

トランザクションモードは、システム変数[`tidb_txn_mode`](/system-variables.md#tidb_txn_mode)設定することで設定できます。次のコマンドは、クラスター内で新規作成されたセッションによって実行されるすべての明示的なトランザクション（つまり、自動コミットされないトランザクション）を悲観的トランザクションモードに設定します。

```sql
SET GLOBAL tidb_txn_mode = 'pessimistic';
```

次の SQL ステートメントを実行して、悲観的トランザクション モードを明示的に有効にすることもできます。

```sql
BEGIN PESSIMISTIC;
```

```sql
BEGIN /*T! PESSIMISTIC */;
```

`BEGIN PESSIMISTIC;`と`BEGIN OPTIMISTIC;`ステートメントは、システム変数`tidb_txn_mode`よりも優先されます。これらの 2 つのステートメントで開始されたトランザクションは、システム変数を無視し、悲観的トランザクションモードと楽観的トランザクションモードの両方をサポートします。

## 行動 {#behaviors}

TiDBの悲観的トランザクションはMySQLの悲観的トランザクションと同様に動作します。1の小さな違いをご覧ください[MySQL InnoDBとの違い](#differences-from-mysql-innodb)

-   悲観的トランザクションの場合、TiDB はスナップショット読み取りと現在の読み取りを導入します。

    -   スナップショット読み取り：トランザクション開始前にコミットされたバージョンを読み取る、ロック解除された読み取りです。1 `SELECT`のステートメントの読み取りはスナップショット読み取りです。
    -   現在の読み取り：コミットされた最新のバージョンを読み取るロックされた読み取りです。1、3、5、または`INSERT` `UPDATE`ステートメントの読み取り`SELECT FOR UPDATE`現在の読み取り`DELETE` 。

    次の例では、スナップショット読み取りと現在の読み取りについて詳しく説明します。

    | セッション1                                                                                                          | セッション2                                                                                 | セッション3                                                  |
    | :-------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------- | :------------------------------------------------------ |
    | テーブル t を作成します (INT)。                                                                                            |                                                                                        |                                                         |
    | T値に挿入(1);                                                                                                       |                                                                                        |                                                         |
    | 悲観的に始める。                                                                                                        |                                                                                        |                                                         |
    | tを更新し、a = a + 1に設定します。                                                                                          |                                                                                        |                                                         |
    |                                                                                                                 | 悲観的に始める。                                                                               |                                                         |
    |                                                                                                                 | SELECT * FROM t; -- スナップショット読み取りを使用して、現在のトランザクションの開始前にコミットされたバージョンを読み取ります。結果はa=1を返します。 |                                                         |
    |                                                                                                                 |                                                                                        | 悲観的に始める。                                                |
    |                                                                                                                 |                                                                                        | SELECT * FROM t FOR UPDATE; -- 現在の読み取りを使用します。ロックを待機します。 |
    | COMMIT; -- ロックを解除します。セッション3のSELECT FOR UPDATE操作によってロックが取得され、TiDBは現在の読み取りを使用して最新のコミット済みバージョンを読み取ります。結果はa=2を返します。 |                                                                                        |                                                         |
    |                                                                                                                 | SELECT * FROM t; -- スナップショット読み取りを使用して、現在のトランザクションの開始前にコミットされたバージョンを読み取ります。結果はa=1を返します。 |                                                         |

-   `UPDATE` 、または`INSERT`ステートメントを実行すると、コミットされた**最新の**データが読み取られ、データが変更され、変更された行に悲観的ロック`DELETE`適用されます。

-   `SELECT FOR UPDATE`ステートメントの場合、変更された行ではなく、コミットされたデータの最新バージョンに悲観的ロックが適用されます。

-   トランザクションがコミットまたはロールバックされると、ロックは解除されます。データの変更を試みる他のトランザクションはブロックされ、ロックが解除されるまで待機する必要があります。TiDBはマルチバージョン同時実行制御（MVCC）を使用しているため、データの*読み取り*を試みるトランザクションはブロックされません。

-   システム変数[`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630)設定することで、一意制約チェックを伴う悲観的ロックをスキップするかどうかを制御できます。詳細は[制約](/constraints.md#pessimistic-transactions)参照してください。

-   複数のトランザクションが互いのロックを取得しようとすると、デッドロックが発生します。これは自動的に検出され、いずれかのトランザクションがランダムに終了し、MySQL互換のエラーコード`1213`が返されます。

-   トランザクションは新しいロックを取得するために最大`innodb_lock_wait_timeout`秒（デフォルト：50秒）待機します。このタイムアウトに達すると、MySQL互換のエラーコード`1205`返されます。複数のトランザクションが同じロックを待機している場合、優先順位はトランザクションの`start ts`に基づいてほぼ決定されます。

-   TiDBは、同一クラスタ内で楽観的トランザクションモードと悲観的トランザクションモードの両方をサポートします。トランザクション実行にはどちらのモードも指定できます。

-   TiDBは`FOR UPDATE NOWAIT`構文をサポートしており、ブロックしてロックが解放されるのを待つことはありません。代わりに、MySQL互換のエラーコード`3572`返されます。

-   演算子`Point Get`と`Batch Point Get`データを読み取らない場合でも、指定された主キーまたは一意キーはロックされ、他のトランザクションが同じ主キーまたは一意キーをロックしたり、データを書き込んだりすることがブロックされます。

-   TiDBは`FOR UPDATE OF TABLES`構文をサポートしています。複数のテーブルを結合する文の場合、TiDBは`OF TABLES`のテーブルに関連付けられた行に対してのみ悲観的ロックを適用します。

## MySQL InnoDBとの違い {#differences-from-mysql-innodb}

1.  TiDB が WHERE 句で範囲を使用する DML または`SELECT FOR UPDATE`ステートメントを実行する場合、範囲内の同時実行 DML ステートメントはブロックされません。

    例えば：

    ```sql
    CREATE TABLE t1 (
     id INT NOT NULL PRIMARY KEY,
     pad1 VARCHAR(100)
    );
    INSERT INTO t1 (id) VALUES (1),(5),(10);
    ```

    ```sql
    BEGIN /*T! PESSIMISTIC */;
    SELECT * FROM t1 WHERE id BETWEEN 1 AND 10 FOR UPDATE;
    ```

    ```sql
    BEGIN /*T! PESSIMISTIC */;
    INSERT INTO t1 (id) VALUES (6); -- blocks only in MySQL
    UPDATE t1 SET pad1='new value' WHERE id = 5; -- blocks waiting in both MySQL and TiDB
    ```

    この動作は、TiDB が現在*ギャップ ロック*をサポートしていないために発生します。

2.  TiDB は`SELECT LOCK IN SHARE MODE`サポートしていません。

    TiDBはデフォルトでは`SELECT LOCK IN SHARE MODE`構文をサポートしていません。3 [`tidb_enable_noop_functions`](/system-variables.md#tidb_enable_noop_functions-new-in-v40)有効にすると、TiDBは`SELECT LOCK IN SHARE MODE`構文と互換性を持つようになります。7 `SELECT LOCK IN SHARE MODE`実行すると、ロックなしの場合と同じ効果が得られるため、他のトランザクションの読み取りまたは書き込み操作がブロックされることはありません。

    v8.3.0以降、TiDBは[`tidb_enable_shared_lock_promotion`](/system-variables.md#tidb_enable_shared_lock_promotion-new-in-v830)システム変数を使用して`SELECT LOCK IN SHARE MODE`ステートメントによるロックの追加を有効にできるようになりました。ただし、今回追加されるロックは真の共有ロックではなく、 `SELECT FOR UPDATE`と整合性のある排他ロックであることに注意してください。TiDBと`SELECT LOCK IN SHARE MODE`構文の互換性を維持しながら、読み取り中に並行して実行される書き込みトランザクションによるデータの変更を防ぐために書き込みをブロックしたい場合は、この変数を有効にできます。この変数を有効にすると、 [`tidb_enable_noop_functions`](/system-variables.md#tidb_enable_noop_functions-new-in-v40)が有効かどうかに関係なく、 `SELECT LOCK IN SHARE MODE`ステートメントから有効になります。

3.  DDL により悲観的トランザクション コミットが失敗する可能性があります。

    MySQLでDDLを実行すると、実行中のトランザクションによってブロックされる可能性があります。しかし、このシナリオでは、TiDBではDDL操作がブロックされないため、悲観的トランザクションコミットが失敗します`ERROR 1105 (HY000): Information schema is changed. [try again later]` . TiDBはトランザクション実行中に`TRUNCATE TABLE`文を実行するため、 `table doesn't exist`のエラーが発生する可能性があります。

4.  `START TRANSACTION WITH CONSISTENT SNAPSHOT`実行した後、MySQL は他のトランザクションで後で作成されたテーブルを読み取ることができますが、TiDB は読み取ることができません。

5.  自動コミット トランザクションでは楽観的ロックが優先されます。

    悲観的モデルを使用する場合、自動コミットトランザクションはまず、オーバーヘッドの少ない楽観的モデルを使用してステートメントのコミットを試みます。書き込み競合が発生した場合、トランザクションの再試行には悲観的モデルが使用されます。したがって、 `tidb_retry_limit` `0`に設定した場合、自動コミットトランザクションは書き込み競合が発生したときに`Write Conflict`エラーを報告します。

    自動コミット`SELECT FOR UPDATE`ステートメントはロックを待機しません。

6.  ステートメント内の`EMBEDDED SELECT`によって読み取られたデータはロックされません。

7.  TiDBでは、オープントランザクションはガベージコレクション（GC）をブロックしません。デフォルトでは、悲観的トランザクションの最大実行時間は1時間に制限されています。この制限は、TiDB設定ファイルの`max-txn-ttl`の`[performance]`を編集することで変更できます。

## 分離レベル {#isolation-level}

TiDB は、悲観的トランザクション モードで次の 2 つの分離レベルをサポートします。

-   デフォルトでは[繰り返し読み取り](/transaction-isolation-levels.md#repeatable-read-isolation-level)で、これは MySQL と同じです。

    > **注記：**
    >
    > この分離レベルでは、DML操作は最新のコミットデータに基づいて実行されます。動作はMySQLと同じですが、TiDBの楽観的トランザクションモードとは異なります。1 [TiDBとMySQLの繰り返し読み取りの違い](/transaction-isolation-levels.md#difference-between-tidb-and-mysql-repeatable-read)参照してください。

-   [コミットされた読み取り](/transaction-isolation-levels.md#read-committed-isolation-level) 。この分離レベルは[`SET TRANSACTION`](/sql-statements/sql-statement-set-transaction.md)ステートメントを使用して設定できます。

## 悲観的なトランザクションコミットプロセス {#pessimistic-transaction-commit-process}

トランザクションのコミットプロセスにおいて、悲観的トランザクションと楽観的トランザクションは同じロジックを持ちます。どちらのトランザクションも2相コミット（2PC）モードを採用しています。悲観的トランザクションにおける重要な適応は、DML実行です。

![TiDB pessimistic transaction commit process](/media/pessimistic-transaction-commit.png)

悲観的トランザクションは、2PCの前にフェーズ`Acquire Pessimistic Lock`追加します。このフェーズには以下のステップが含まれます。

1.  (楽観的トランザクション モードと同じ) TiDB はクライアントから`begin`リクエストを受信し、現在のタイムスタンプはこのトランザクションの start_ts になります。
2.  TiDBサーバーはクライアントから書き込み要求を受信すると、TiDBサーバーはTiKVサーバーに悲観的ロック要求を開始し、ロックは TiKVサーバーに永続化されます。
3.  (楽観的トランザクション モードと同じ) クライアントがコミット要求を送信すると、TiDB は楽観的トランザクション モードと同様に 2 フェーズ コミットの実行を開始します。

![Pessimistic transactions in TiDB](/media/pessimistic-transaction-in-tidb.png)

## パイプライン化されたロックプロセス {#pipelined-locking-process}

悲観的ロックを追加するには、TiKVへのデータ書き込みが必要です。ロック追加成功のレスポンスは、 Raftを介したコミットと適用後にのみTiDBに返されます。そのため、楽観的トランザクションと比較して、悲観的トランザクションモードでは必然的にレイテンシーが高くなります。

ロックのオーバーヘッドを削減するため、TiKVはパイプライン化されたロック処理を実装しています。データがロックの要件を満たすと、TiKVは直ちにTiDBに後続のリクエストの実行を通知し、悲観的ロックへの非同期書き込みを実行します。この処理により、レイテンシーが大幅に削減され、悲観的トランザクションのパフォーマンスが大幅に向上します。ただし、TiKVでネットワーク分断が発生した場合、またはTiKVノードがダウンした場合、悲観的ロックへの非同期書き込みが失敗し、以下の影響が生じる可能性があります。

-   同じデータを変更する他のトランザクションをブロックすることはできません。アプリケーションロジックがロックまたはロック待機メカニズムに依存している場合、アプリケーションロジックの正確性に影響が出ます。

-   トランザクションのコミットが失敗する可能性は低いですが、トランザクションの正確性には影響しません。

<CustomContent platform="tidb">

アプリケーション ロジックがロックまたはロック待機メカニズムに依存している場合、または TiKV クラスターの異常が発生した場合でもトランザクション コミットの成功率を可能な限り保証したい場合は、パイプライン ロック機能を無効にする必要があります。

![Pipelined pessimistic lock](/media/pessimistic-transaction-pipelining.png)

この機能はデフォルトで有効になっています。無効にするには、TiKVの設定を変更してください。

```toml
[pessimistic-txn]
pipelined = false
```

TiKV クラスターが v4.0.9 以降の場合は、 [TiKV設定を動的に変更する](/dynamic-config.md#modify-tikv-configuration-dynamically)を実行してこの機能を動的に無効にすることもできます。

```sql
set config tikv pessimistic-txn.pipelined='false';
```

</CustomContent>

<CustomContent platform="tidb-cloud">

アプリケーション ロジックがロックまたはロック待機メカニズムに依存している場合、または TiKV クラスターの異常が発生した場合でもトランザクション コミットの成功率を可能な限り保証したい場合は、パイプライン ロック機能を[TiDB Cloudサポートにお問い合わせください](/tidb-cloud/tidb-cloud-support.md)無効にすることができます。

</CustomContent>

## メモリ内悲観的ロック {#in-memory-pessimistic-lock}

v6.0.0では、TiKVにインメモリ悲観的ロック機能が導入されました。この機能を有効にすると、悲観的ロックは通常、リージョンリーダーのメモリにのみ保存され、ディスクに永続化されず、 Raftを介して他のレプリカに複製されることもありません。この機能により、悲観的ロックの取得にかかるオーバーヘッドが大幅に削減され、悲観的トランザクションのスループットが向上します。

<CustomContent platform="tidb">

インメモリ悲観的ロックのメモリ使用量が[リージョン](/tikv-configuration-file.md#in-memory-peer-size-limit-new-in-v840)または[TiKVノード](/tikv-configuration-file.md#in-memory-instance-size-limit-new-in-v840)のメモリしきい値を超えると、悲観的ロックの取得は[パイプライン化されたロックプロセス](#pipelined-locking-process)に切り替わります。リージョンの統合やリーダーの交代時には、悲観的的ロックの喪失を回避するため、TiKVはインメモリ悲観的ロックをディスクに書き込み、他のレプリカに複製します。

</CustomContent>

<CustomContent platform="tidb-cloud">

インメモリ悲観的ロックのメモリ使用量が[リージョン](https://docs.pingcap.com/tidb/dev/tikv-configuration-file#in-memory-peer-size-limit-new-in-v840)または[TiKVノード](https://docs.pingcap.com/tidb/dev/tikv-configuration-file#in-memory-instance-size-limit-new-in-v840)のメモリしきい値を超えると、悲観的ロックの取得は[パイプライン化されたロックプロセス](#pipelined-locking-process)に切り替わります。リージョンの統合やリーダーの交代時には、悲観的的ロックの喪失を回避するため、TiKVはインメモリ悲観的ロックをディスクに書き込み、他のレプリカに複製します。

</CustomContent>

インメモリ悲観的ロックはパイプライン化されたロック処理と同様に動作し、クラスターが正常な場合はロックの取得に影響を与えません。ただし、TiKVでネットワーク分離が発生した場合、またはTiKVノードがダウンした場合、取得済みの悲観的ロックが失われる可能性があります。

アプリケーション ロジックがロック取得またはロック待機メカニズムに依存している場合、またはクラスターが異常な状態にある場合でもトランザクション コミットの成功率を可能な限り保証する場合は、メモリ内悲観的ロック機能**を無効にする**必要があります。

この機能はデフォルトで有効になっています。無効にするには、TiKVの設定を変更してください。

```toml
[pessimistic-txn]
in-memory = false
```

この機能を動的に無効にするには、TiKV 構成を動的に変更します。

```sql
set config tikv pessimistic-txn.in-memory='false';
```

<CustomContent platform="tidb">

v8.4.0 以降では、 [`pessimistic-txn.in-memory-peer-size-limit`](/tikv-configuration-file.md#in-memory-peer-size-limit-new-in-v840)または[`pessimistic-txn.in-memory-instance-size-limit`](/tikv-configuration-file.md#in-memory-instance-size-limit-new-in-v840)使用して、リージョンまたは TiKV インスタンス内のメモリ内悲観的ロックのメモリ使用量制限を設定できます。

```toml
[pessimistic-txn]
in-memory-peer-size-limit = "512KiB"
in-memory-instance-size-limit = "100MiB"
```

これらの制限を動的に変更するには、 [TiKV設定を動的に変更する](/dynamic-config.md#modify-tikv-configuration-dynamically)のようにします。

```sql
SET CONFIG tikv `pessimistic-txn.in-memory-peer-size-limit`="512KiB";
SET CONFIG tikv `pessimistic-txn.in-memory-instance-size-limit`="100MiB";
```

</CustomContent>
