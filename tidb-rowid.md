---
title: _tidb_rowid
summary: _tidb_rowid`とは何か、いつ利用できるのか、そして安全に使用する方法について学びましょう。
---

# <code>_tidb_rowid</code> {#code-tidb-rowid-code}

`_tidb_rowid`はTiDBによって自動的に生成される非表示のシステム列です。クラスタ化インデックスを使用しないテーブルの場合、この列はテーブルの内部行IDとして機能します。テーブルスキーマでこの列を宣言または変更することはできませんが、テーブルが内部行IDとして`_tidb_rowid`使用している場合は、SQLで参照できます。

現在の実装では、 `_tidb_rowid`はTiDBによって自動的に管理される追加の`BIGINT NOT NULL`列です。

> **警告：**
>
> -   `_tidb_rowid`常にグローバルに一意であるとは限らないことに注意してください。クラスタ化インデックスを使用しないパーティションテーブルの場合、 `ALTER TABLE ... EXCHANGE PARTITION`実行すると、異なるパーティション間で`_tidb_rowid`値が重複する可能性があります。
> -   安定した一意の識別子が必要な場合は、 `_tidb_rowid`に依存するのではなく、明示的な主キーを定義して使用してください。

## <code>_tidb_rowid</code>が利用可能な場合 {#when-code-tidb-rowid-code-is-available}

TiDBでは、テーブルが一意の行識別子としてクラスタ化された主キーを使用しない場合、各行を識別するために`_tidb_rowid`使用します。実際には、これは次のタイプのテーブルが`_tidb_rowid`使用することを意味します。

-   主キーのないテーブル
-   主キーが明示的に`NONCLUSTERED`と定義されているテーブル

`_tidb_rowid`は、クラスター化インデックスを使用するテーブル (つまり、主キーが`CLUSTERED`として定義されているテーブル。主キーが単一列か複合主キーかは関係ありません) では使用できません。

以下の例は、その違いを示しています。

```sql
CREATE TABLE t1 (a INT, b VARCHAR(20));
CREATE TABLE t2 (id BIGINT PRIMARY KEY NONCLUSTERED, a INT);
CREATE TABLE t3 (id BIGINT PRIMARY KEY CLUSTERED, a INT);
```

`t1`と`t2`については、これらのテーブルは行識別子としてクラスタ化インデックスを使用していないため、 `_tidb_rowid`に対してクエリを実行できます。

```sql
SELECT _tidb_rowid, a, b FROM t1;
SELECT _tidb_rowid, id, a FROM t2;
```

`t3`の場合、クラスタ化された主キーが既に行識別子になっているため、 `_tidb_rowid`利用できません。

```sql
SELECT _tidb_rowid, id, a FROM t3;
```

```sql
ERROR 1054 (42S22): Unknown column '_tidb_rowid' in 'field list'
```

## <code>_tidb_rowid</code>を読み込む {#read-code-tidb-rowid-code}

`_tidb_rowid`使用するテーブルの場合、 `SELECT`ステートメントで`_tidb_rowid`クエリできます。これは、ページネーション、トラブルシューティング、バッチ処理などのタスクに役立ちます。

例：

```sql
CREATE TABLE t (a INT, b VARCHAR(20));
INSERT INTO t VALUES (1, 'x'), (2, 'y');

SELECT _tidb_rowid, a, b FROM t ORDER BY _tidb_rowid;
```

```sql
+-------------+---+---+
| _tidb_rowid | a | b |
+-------------+---+---+
|           1 | 1 | x |
|           2 | 2 | y |
+-------------+---+---+
```

TiDB が行 ID に割り当てる次の値を表示するには、 `SHOW TABLE ... NEXT_ROW_ID`使用します。

```sql
SHOW TABLE t NEXT_ROW_ID;
```

```sql
+-----------------------+------------+-------------+--------------------+-------------+
| DB_NAME               | TABLE_NAME | COLUMN_NAME | NEXT_GLOBAL_ROW_ID | ID_TYPE     |
+-----------------------+------------+-------------+--------------------+-------------+
| update_doc_rowid_test | t          | _tidb_rowid |              30001 | _TIDB_ROWID |
+-----------------------+------------+-------------+--------------------+-------------+
```

## <code>_tidb_rowid</code>を書き込む {#write-code-tidb-rowid-code}

デフォルトでは、TiDB は`INSERT` 、または`REPLACE`ステートメント`UPDATE` `_tidb_rowid`直接書き込むことを許可しません。

```sql
INSERT INTO t(_tidb_rowid, a, b) VALUES (101, 4, 'w');
```

```sql
ERROR 1105 (HY000): insert, update and replace statements for _tidb_rowid are not supported
```

データインポートまたは移行中に元の行IDを保持する必要がある場合は、まずシステム変数[`tidb_opt_write_row_id`](/system-variables.md#tidb_opt_write_row_id)有効にしてください。

```sql
SET @@tidb_opt_write_row_id = ON;
INSERT INTO t(_tidb_rowid, a, b) VALUES (100, 3, 'z');
SET @@tidb_opt_write_row_id = OFF;

SELECT _tidb_rowid, a, b FROM t WHERE _tidb_rowid = 100;
```

```sql
+-------------+---+---+
| _tidb_rowid | a | b |
+-------------+---+---+
|         100 | 3 | z |
+-------------+---+---+
```

> **警告：**
>
> `tidb_opt_write_row_id`はインポートおよび移行シナリオを想定しています。通常のアプリケーション書き込みには推奨されません。

## 制限 {#restrictions}

-   `_tidb_rowid`という名前のユーザー列を作成することはできません。
-   既存のユーザー列の名前を`_tidb_rowid`に変更することはできません。
-   `_tidb_rowid`はTiDBの内部列です。ビジネス上の主キーや長期的な識別子として扱わないでください。
-   パーティション化された非クラスタ化テーブルでは、 `_tidb_rowid`値はパーティション間で一意であることが保証されません。3 `EXCHANGE PARTITION`実行した後、異なるパーティションに同じ`_tidb_rowid`値を持つ行が含まれる可能性があります。
-   `_tidb_rowid`存在するかどうかは、テーブルのスキーマによって異なります。クラスタ化インデックスを持つテーブルの場合は、行識別子として主キーを使用してください。

## ホットスポットの問題に対処する {#address-hotspot-issues}

`_tidb_rowid`使用するテーブルの場合、TiDB はデフォルトで行 ID を昇順で割り当てます。書き込み負荷の高いワークロードでは、これにより書き込みホットスポットが発生する可能性があります。

この問題を軽減するために（行IDとして`_tidb_rowid`を使用するテーブルの場合）、行IDをより均等に分配するために[`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)使用し、必要に応じてリージョンを事前に分割するために[`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions)使用することを検討してください。

例：

```sql
CREATE TABLE t (
    id BIGINT PRIMARY KEY NONCLUSTERED,
    c INT
) SHARD_ROW_ID_BITS = 4;
```

`SHARD_ROW_ID_BITS` `_tidb_rowid`使用するテーブルにのみ適用され、クラスター化インデックスを持つテーブルには適用されません。

## 関連する記述と変数 {#related-statements-and-variables}

-   [`SHOW TABLE NEXT_ROW_ID`](/sql-statements/sql-statement-show-table-next-rowid.md) ：TiDBが次に割り当てる行IDを示します
-   [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md) ：ホットスポットを減らすために暗黙の行IDをシャーディングする
-   [`Clustered Indexes`](/clustered-indexes.md) : テーブルが主キーを使用する理由を説明します`_tidb_rowid`
-   [`tidb_opt_write_row_id`](/system-variables.md#tidb_opt_write_row_id) ： `_tidb_rowid`への書き込みを許可するかどうかを制御します

## 関連項目 {#see-also}

-   [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)
-   [`AUTO_INCREMENT`](/auto-increment.md)
-   [非トランザクションDML](/non-transactional-dml.md)
