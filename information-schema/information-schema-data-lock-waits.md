---
title: DATA_LOCK_WAITS
summary: Learn the `DATA_LOCK_WAITS` information_schema table.
---

# DATA_LOCK_WAITS {#data-lock-waits}

表`DATA_LOCK_WAITS`は、クラスター内のすべての TiKV ノードで進行中のロック待機情報を示します。これには、悲観的トランザクションのロック待機情報と、ブロックされている楽観的トランザクションの情報が含まれます。

```sql
USE information_schema;
DESC data_lock_waits;
```

```sql
+------------------------+---------------------+------+------+---------+-------+
| Field                  | Type                | Null | Key  | Default | Extra |
+------------------------+---------------------+------+------+---------+-------+
| KEY                    | text                | NO   |      | NULL    |       |
| KEY_INFO               | text                | YES  |      | NULL    |       |
| TRX_ID                 | bigint(21) unsigned | NO   |      | NULL    |       |
| CURRENT_HOLDING_TRX_ID | bigint(21) unsigned | NO   |      | NULL    |       |
| SQL_DIGEST             | varchar(64)         | YES  |      | NULL    |       |
| SQL_DIGEST_TEXT        | text                | YES  |      | NULL    |       |
+------------------------+---------------------+------+------+---------+-------+
```

`DATA_LOCK_WAITS`テーブルの各列フィールドの意味は次のとおりです。

-   `KEY` : ロックを待機している 16 進数形式のキー。
-   `KEY_INFO` ： `KEY`の詳細情報です。 [KEY_INFO](#key_info)セクションを参照してください。
-   `TRX_ID` : ロックを待機しているトランザクションの ID。この ID はトランザクションの`start_ts`でもあります。
-   `CURRENT_HOLDING_TRX_ID` : 現在ロックを保持しているトランザクションの ID。この ID はトランザクションの`start_ts`でもあります。
-   `SQL_DIGEST` : ロック待ちトランザクションで現在ブロックされている SQL 文のダイジェスト。
-   `SQL_DIGEST_TEXT` : ロック待機トランザクションで現在ブロックされている正規化された SQL ステートメント (引数と形式のない SQL ステートメント)。 `SQL_DIGEST`に相当します。

> **警告：**
>
> -   [プロセス](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process)権限を持つユーザーのみがこのテーブルをクエリできます。
> -   現在、楽観的トランザクションの場合、 `SQL_DIGEST`フィールドと`SQL_DIGEST_TEXT`フィールドは`null` (使用できないことを意味します) です。回避策として、ブロッキングの原因となっている SQL ステートメントを特定するには、このテーブルを[`CLUSTER_TIDB_TRX`](/information-schema/information-schema-tidb-trx.md)と結合して、楽観的トランザクションのすべての SQL ステートメントを取得します。
> -   `DATA_LOCK_WAITS`テーブルの情報は、クエリ中にすべての TiKV ノードからリアルタイムで取得されます。現在、クエリに`WHERE`条件がある場合でも、情報収集はすべての TiKV ノードで実行されます。クラスターが大きく負荷が高い場合、このテーブルにクエリを実行すると、パフォーマンス ジッターの潜在的なリスクが発生する可能性があります。したがって、実際の状況に応じて使用してください。
> -   異なる TiKV ノードからの情報は、同じ時刻のスナップショットであることは保証されません。
> -   `SQL_DIGEST`列目の情報（SQLダイジェスト）は、正規化されたSQL文から計算されたハッシュ値です。 `SQL_DIGEST_TEXT`列の情報はステートメント概要テーブルから内部的にクエリされるため、対応するステートメントが内部で見つからない可能性があります。 SQL ダイジェストとステートメント概要テーブルの詳細については、 [ステートメント概要テーブル](/statement-summary-tables.md)を参照してください。

## <code>KEY_INFO</code> {#code-key-info-code}

`KEY_INFO`列目は`KEY`列目の詳細情報を表示します。情報はJSON形式で表示されます。各フィールドの説明は次のとおりです。

-   `"db_id"` : キーが属するスキーマの ID。
-   `"db_name"` : キーが属するスキーマの名前。
-   `"table_id"` : キーが属するテーブルの ID。
-   `"table_name"` : キーが属するテーブルの名前。
-   `"partition_id"` : キーが配置されているパーティションの ID。
-   `"partition_name"` : キーが存在するパーティションの名前。
-   `"handle_type"` : 行キー (つまり、データ行を格納するキー) のハンドル タイプ。可能な値は次のとおりです。
    -   `"int"` : ハンドルのタイプは int です。これは、ハンドルが行 ID であることを意味します。
    -   `"common"` : ハンドルの型は int64 ではありません。この型は、クラスター化インデックスが有効になっている場合、非 int 主キーに表示されます。
    -   `"unknown"` : ハンドル タイプは現在サポートされていません。
-   `"handle_value"` : ハンドル値。
-   `"index_id"` : インデックスキー(インデックスを格納するキー)が属するインデックスID。
-   `"index_name"` : インデックスキーが属するインデックスの名前。
-   `"index_values"` : インデックス キーのインデックス値。

上記のフィールドでは、フィールドの情報が適用できない場合、または現在利用できない場合、そのフィールドはクエリ結果で省略されます。たとえば、行キー情報には`index_id` 、 `index_name` 、および`index_values`は含まれません。インデックス キーには`handle_type`と`handle_value`が含まれません。パーティション化されていないテーブルには`partition_id`と`partition_name`は表示されません。削除されたテーブルのキー情報は、 `table_name`などのスキーマ情報`db_name`取得できず、テーブル`index_name`パーティションテーブルである`db_id`どうかを区別できません。

> **注記：**
>
> パーティショニングが有効になっているテーブルからキーが取得され、クエリ中に何らかの理由 (キーが属するテーブルが削除されたなど) によりキーが属するスキーマの情報をクエリできない場合、IDキーが属するパーティションの名前が`table_id`フィールドに表示される場合があります。これは、TiDB が複数の独立したテーブルのキーをエンコードするのと同じ方法で、異なるパーティションのキーをエンコードするためです。したがって、スキーマ情報が欠落している場合、TiDB はキーがパーティション化されていないテーブルに属しているのか、テーブルの 1 つのパーティションに属しているのかを確認できません。

## 例 {#example}

```sql
select * from information_schema.data_lock_waits\G
```

```sql
*************************** 1. row ***************************
                   KEY: 7480000000000000355F728000000000000001
              KEY_INFO: {"db_id":1,"db_name":"test","table_id":53,"table_name":"t","handle_type":"int","handle_value":"1"}
                TRX_ID: 426790594290122753
CURRENT_HOLDING_TRX_ID: 426790590082449409
            SQL_DIGEST: 38b03afa5debbdf0326a014dbe5012a62c51957f1982b3093e748460f8b00821
       SQL_DIGEST_TEXT: update `t` set `v` = `v` + ? where `id` = ?
1 row in set (0.01 sec)
```

上記のクエリ結果は、ID `426790594290122753`のトランザクションが、ダイジェスト`"38b03afa5debbdf0326a014dbe5012a62c51957f1982b3093e748460f8b00821"`を持ち、 ``update `t` set `v` = `v` + ? where `id` = ?``の形式であるステートメントを実行するときに、キー`"7480000000000000355F728000000000000001"`の悲観的ロックを取得しようとしていますが、このキーのロックはトランザクションによって保持されていることを示しています。 ID `426790590082449409`の。
