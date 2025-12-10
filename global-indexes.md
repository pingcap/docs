---
title: Global Indexes
summary: TiDB グローバル インデックスの使用例、利点、使用方法、動作原理、制限について学習します。
---

# グローバルインデックス {#global-indexes}

グローバルインデックスを導入する前、TiDBはパーティションごとにローカルインデックスを作成していました。つまり、パーティションごとに[制限](/partitioned-table.md#partitioning-keys-primary-keys-and-unique-keys)のローカルインデックスが作成されていました。このインデックス作成アプローチでは、データのグローバルな一意性を保証するために、主キーと一意キーにすべてのパーティションキーを含める必要がありました。さらに、クエリが複数のパーティションにまたがるデータにアクセスする必要がある場合、TiDBは結果を返すために各パーティションのデータをスキャンする必要がありました。

これらの問題に対処するため、TiDBは[バージョン8.3.0](https://docs.pingcap.com/tidb/stable/release-8.3.0)でグローバルインデックス機能を導入しました。単一のグローバルインデックスでテーブル全体のデータをカバーするため、パーティションキーが含まれていない場合でも、主キーと一意キーはグローバルに一意に保たれます。さらに、グローバルインデックスを使用すると、TiDBは各パーティションのローカルインデックスを参照することなく、複数のパーティションにまたがるインデックスデータに単一の操作でアクセスできます。これにより、パーティションキー以外のキーに対するクエリパフォーマンスが大幅に向上します。v8.5.4以降では、一意でないインデックスもグローバルインデックスとして作成できます。

## 利点 {#advantages}

グローバル インデックスを使用すると、クエリのパフォーマンスが大幅に向上し、インデックスの柔軟性が高まり、データの移行とアプリケーションの変更にかかるコストが削減されます。

### クエリパフォーマンスの向上 {#improved-query-performance}

グローバルインデックスは、非パーティション列へのクエリの効率を効果的に向上させます。クエリに非パーティション列が含まれる場合、グローバルインデックスは関連データを迅速に特定できるため、すべてのパーティションにわたるフルテーブルスキャンを回避できます。これにより、コプロセッサー（COP）タスクの数が大幅に削減され、特にパーティション数が多いシナリオで大きな効果を発揮します。

ベンチマーク テストでは、テーブルに 100 個のパーティションが含まれている場合、sysbench `select_random_points`シナリオでのパフォーマンスが最大 53 倍向上することが示されています。

### 強化されたインデックスの柔軟性 {#enhanced-indexing-flexibility}

グローバルインデックスにより、パーティションテーブルの一意のキーにはすべてのパーティション列が含まれていなければならないという制約がなくなります。これにより、インデックス設計の柔軟性が向上します。パーティションスキームに制約されることなく、実際のクエリパターンとビジネスロジックに基づいてインデックスを作成できるようになります。この柔軟性は、クエリパフォーマンスを向上させるだけでなく、より幅広いアプリケーション要件に対応できるようになります。

### データ移行とアプリケーション変更にかかるコストの削減 {#reduced-cost-for-data-migration-and-application-modifications}

データ移行やアプリケーションの変更時に、グローバルインデックスを使用することで、追加の調整作業を大幅に削減できます。グローバルインデックスがない場合、パーティションスキームを変更したり、インデックスの制限を回避するためにSQLクエリを書き直したりする必要があるかもしれません。グローバルインデックスを使用すれば、こうした変更を回避でき、開発コストと保守コストの両方を削減できます。

例えば、OracleデータベースからTiDBにテーブルを移行する場合、Oracleはグローバルインデックスをサポートしているため、パーティション列を含まない一意のインデックスが使用されることがあります。TiDBがグローバルインデックスを導入する前は、TiDBのパーティションルールに準拠するようにテーブルスキーマを変更する必要がありました。現在、TiDBはグローバルインデックスをサポートしています。データを移行する際には、これらのインデックスをグローバルとして定義するだけで済み、スキーマの動作をOracleと一貫性のあるものにすることができ、移行コストを大幅に削減できます。

## グローバルインデックスの制限 {#limitations-of-global-indexes}

-   インデックス定義で`GLOBAL`キーワードが明示的に指定されていない場合、TiDB はデフォルトでローカル インデックスを作成します。
-   キーワード`GLOBAL`と`LOCAL`はパーティションテーブルにのみ適用され、非パーティションテーブルには影響しません。つまり、非パーティションテーブルでは、グローバルインデックスとローカルインデックスに違いはありません。
-   `DROP PARTITION` `REORGANIZE PARTITION`の DDL 操作も、グローバルインデックスの更新をトリガーします。これらの DDL 操作は`TRUNCATE PARTITION`結果を返す前にグローバルインデックスの更新が完了するのを待つ必要があるため、実行時間が長くなります。これは、 `DROP PARTITION`や`TRUNCATE PARTITION`などのデータアーカイブのシナリオで特に顕著です。グローバルインデックスがない場合、これらの操作は通常すぐに完了します。しかし、グローバルインデックスがある場合、更新が必要なインデックスの数が増えるにつれて実行時間が長くなります。
-   グローバル インデックスを含むテーブルは`EXCHANGE PARTITION`操作をサポートしません。
-   デフォルトでは、パーティションテーブルの主キーはクラスター化インデックスであり、パーティションキーを含める必要があります。主キーからパーティションキーを除外する必要がある場合は、テーブル作成時に主キーを非クラスター化グローバルインデックスとして明示的に指定できます（例： `PRIMARY KEY(col1, col2) NONCLUSTERED GLOBAL` ）。
-   式列にグローバル インデックスが追加された場合、またはグローバル インデックスがプレフィックス インデックスでもある場合 (たとえば`UNIQUE KEY idx_id_prefix (id(10)) GLOBAL` )、このグローバル インデックスの統計を手動で収集する必要があります。

## 機能の進化 {#feature-evolution}

-   **v7.6.0より前**：TiDBはパーティションテーブル上のローカルインデックスのみをサポートします。つまり、パーティションテーブルの一意キーには、パーティション式内のすべての列を含める必要があります。パーティションキーを使用しないクエリはすべてのパーティションをスキャンする必要があり、クエリパフォーマンスが低下します。
-   **<a href="https://docs.pingcap.com/tidb/stable/release-7.6.0">v7.6.0</a>** : グローバルインデックスを有効にするシステム変数[`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-new-in-v760)が導入されました。ただし、この機能は現時点ではまだ開発中であり、本番での使用は推奨されません。
-   **<a href="https://docs.pingcap.com/tidb/stable/release-8.3.0">v8.3.0</a>** : グローバルインデックスが実験的機能としてリリースされました。インデックスを定義する際に`GLOBAL`キーワードを使用することで、明示的にグローバルインデックスを作成できます。
-   **<a href="https://docs.pingcap.com/tidb/stable/release-8.4.0">v8.4.0</a>** : グローバルインデックス機能が一般提供（GA）されました。システム変数`tidb_enable_global_index`を設定せずに、キーワード`GLOBAL`を使って直接グローバルインデックスを作成できます。このバージョン以降、システム変数 4 は非推奨となり、値は`ON`に固定されます。つまり、グローバルインデックスはデフォルトで有効になります。
-   **<a href="https://docs.pingcap.com/tidb/stable/release-8.5.0">v8.5.0</a>** : グローバル インデックスは、パーティション式のすべての列を含めることをサポートします。

## グローバルインデックスとローカルインデックス {#global-indexes-vs-local-indexes}

次の図は、グローバル インデックスとローカル インデックスの違いを示しています。

![Global Index vs. Local Index](/media/global-index-vs-local-index.png)

**グローバルインデックスのシナリオ**:

-   **頻度の低いデータアーカイブ**：例えば、医療業界では、一部のビジネスデータは最大30年間保持する必要があります。このようなデータは月ごとにパーティション分割されることが多く、一度に360個のパーティションが作成され、その後`DROP` ～ `TRUNCATE`操作が発生することは非常にまれです。このようなシナリオでは、パーティション間の一貫性とクエリパフォーマンスの向上を実現するグローバルインデックスの方が適しています。
-   **複数のパーティションにまたがるクエリ**: クエリが複数のパーティションにわたるデータにアクセスする必要がある場合、グローバル インデックスを使用すると、すべてのパーティションにわたるフル スキャンを回避し、クエリの効率を高めることができます。

**ローカルインデックスのシナリオ**:

-   **頻繁なデータ アーカイブ**: データ アーカイブ操作が頻繁に発生し、ほとんどのクエリが単一のパーティションに制限されている場合は、ローカル インデックスの方がパフォーマンスが向上します。
-   **パーティション交換の使用**：銀行などの業界では、処理済みのデータをまず通常のテーブルに書き込み、検証後にパーティションテーブルに交換することで、パーティションテーブルへのパフォーマンスへの影響を最小限に抑える場合があります。この場合、グローバルインデックスを使用するとパーティションテーブルはパーティション交換をサポートしなくなるため、ローカルインデックスが推奨されます。

## グローバルインデックスとクラスター化インデックス {#global-indexes-vs-clustered-indexes}

クラスター化インデックスとグローバルインデックスの根本的な制約により、1つのインデックスをクラスター化インデックスとグローバルインデックスの両方の機能を同時に使用することはできません。ただし、それぞれのインデックスは、クエリシナリオに応じて異なるパフォーマンス上のメリットをもたらします。両方のメリットを活用する必要がある場合は、パーティション列をクラスター化インデックスに含め、パーティション列を含まない別のグローバルインデックスを作成することができます。

次のようなテーブル スキーマがあるとします。

```sql
CREATE TABLE `t` (
  `id` int DEFAULT NULL,
  `ts` timestamp NULL DEFAULT NULL,
  `data` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
PARTITION BY RANGE (UNIX_TIMESTAMP(`ts`))
(PARTITION `p0` VALUES LESS THAN (1735660800)
 PARTITION `p1` VALUES LESS THAN (1738339200)
 ...)
```

前述のテーブル`t`では、列`id`に一意の値が含まれています。ポイントクエリと範囲クエリの両方を最適化するには、テーブル作成ステートメントでクラスター化インデックス`PRIMARY KEY(id, ts)`と、パーティション列を含まないグローバルインデックス`UNIQUE KEY id(id)`を定義します。これにより、 `id`に基づくポイントクエリはグローバルインデックス`id`を使用し、実行プラン`PointGet`を選択します。範囲クエリではクラスター化インデックスが使用されます。これは、クラスター化インデックスはグローバルインデックスと比較して追加のテーブル参照を回避し、クエリ効率を向上させるためです。

変更されたテーブル スキーマは次のとおりです。

```sql
CREATE TABLE `t` (
  `id` int NOT NULL,
  `ts` timestamp NOT NULL,
  `data` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`, `ts`) /*T![clustered_index] CLUSTERED */,
  UNIQUE KEY `id` (`id`) /*T![global_index] GLOBAL */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
PARTITION BY RANGE (UNIX_TIMESTAMP(`ts`))
(PARTITION `p0` VALUES LESS THAN (1735660800),
 PARTITION `p1` VALUES LESS THAN (1738339200)
 ...)
```

このアプローチは、 `id`に基づいてポイント クエリを最適化すると同時に範囲クエリのパフォーマンスを向上させ、タイムスタンプ ベースのクエリでテーブルのパーティション列が効果的に利用されることを保証します。

## 使用法 {#usage}

グローバル インデックスを作成するには、インデックス定義に`GLOBAL`キーワードを追加します。

> **注記：**
>
> グローバルインデックスはパーティション管理に影響します。1、3、または`REORGANIZE PARTITION` `TRUNCATE`を実行すると`DROP`テーブルレベルのグローバルインデックスの更新がトリガーされます。つまり、これらのDDL操作は、対応するグローバルインデックスの更新が完了した後にのみ返されるため、実行時間が長くなる可能性があります。

```sql
CREATE TABLE t1 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY uidx12(col1, col2) GLOBAL,
    UNIQUE KEY uidx3(col3),
    KEY idx1(col1) GLOBAL
)
PARTITION BY HASH(col3)
PARTITIONS 4;
```

前の例では、一意のインデックス`uidx12`と一意でないインデックス`idx1`はグローバル インデックスになりますが、 `uidx3`通常の一意のインデックスのままです。

クラスター化インデックスはグローバルインデックスにはなり得ないことに注意してください。例:

```sql
CREATE TABLE t2 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    PRIMARY KEY (col2) CLUSTERED GLOBAL
) PARTITION BY HASH(col1) PARTITIONS 5;
```

    ERROR 1503 (HY000): A CLUSTERED INDEX must include all columns in the table's partitioning function

クラスター化インデックスはグローバルインデックスとしても機能しません。これは、クラスター化インデックスをグローバルにすると、テーブルがパーティション化されなくなるためです。クラスター化インデックスのキーはパーティションレベルの行データのキーですが、グローバルインデックスはテーブルレベルで定義されるため、競合が発生します。主キーをグローバルインデックスにする必要がある場合は、明示的に非クラスター化インデックスとして定義する必要があります。例:

```sql
PRIMARY KEY(col1, col2) NONCLUSTERED GLOBAL
```

[`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md)の出力で`GLOBAL`インデックス オプションをチェックすることで、グローバル インデックスを識別できます。

```sql
SHOW CREATE TABLE t1\G
```

           Table: t1
    Create Table: CREATE TABLE `t1` (
      `col1` int NOT NULL,
      `col2` date NOT NULL,
      `col3` int NOT NULL,
      `col4` int NOT NULL,
      UNIQUE KEY `uidx12` (`col1`,`col2`) /*T![global_index] GLOBAL */,
      UNIQUE KEY `uidx3` (`col3`),
      KEY `idx1` (`col1`) /*T![global_index] GLOBAL */
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
    PARTITION BY HASH (`col3`) PARTITIONS 4
    1 row in set (0.00 sec)

あるいは、 [`INFORMATION_SCHEMA.TIDB_INDEXES`](/information-schema/information-schema-tidb-indexes.md)テーブルをクエリし、出力の`IS_GLOBAL`列をチェックしてグローバル インデックスを識別することもできます。

```sql
SELECT * FROM information_schema.tidb_indexes WHERE table_name='t1';
```

    +--------------+------------+------------+----------+--------------+-------------+----------+---------------+------------+----------+------------+-----------+-----------+
    | TABLE_SCHEMA | TABLE_NAME | NON_UNIQUE | KEY_NAME | SEQ_IN_INDEX | COLUMN_NAME | SUB_PART | INDEX_COMMENT | Expression | INDEX_ID | IS_VISIBLE | CLUSTERED | IS_GLOBAL |
    +--------------+------------+------------+----------+--------------+-------------+----------+---------------+------------+----------+------------+-----------+-----------+
    | test         | t1         |          0 | uidx12   |            1 | col1        |     NULL |               | NULL       |        1 | YES        | NO        |         1 |
    | test         | t1         |          0 | uidx12   |            2 | col2        |     NULL |               | NULL       |        1 | YES        | NO        |         1 |
    | test         | t1         |          0 | uidx3    |            1 | col3        |     NULL |               | NULL       |        2 | YES        | NO        |         0 |
    | test         | t1         |          1 | idx1     |            1 | col1        |     NULL |               | NULL       |        3 | YES        | NO        |         1 |
    +--------------+------------+------------+----------+--------------+-------------+----------+---------------+------------+----------+------------+-----------+-----------+
    3 rows in set (0.00 sec)

通常のテーブルをパーティション分割する場合、またはパーティションテーブルを再パーティションする場合、必要に応じてインデックスをグローバル インデックスまたはローカル インデックスに更新できます。

例えば、次のSQL文は、列`col1`に基づいて表`t1`再パーティション化し、グローバルインデックス`uidx12`と`idx1`ローカルインデックスに更新し、ローカルインデックス`uidx3`グローバルインデックスに更新します。列`uidx3`は列`col3`の一意のインデックスです。すべてのパーティションにわたって列`col3`の一意性を確保するには、列`uidx3`グローバルインデックスにする必要があります。列`uidx12`と`idx1`は列`col1`のインデックスであり、グローバルインデックスまたはローカルインデックスのどちらでも構いません。

```sql
ALTER TABLE t1 PARTITION BY HASH (col1) PARTITIONS 3 UPDATE INDEXES (uidx12 LOCAL, uidx3 GLOBAL, idx1 LOCAL);
```

## 動作メカニズム {#working-mechanism}

このセクションでは、グローバル インデックスの設計原則と実装を含む、グローバル インデックスの動作メカニズムについて説明します。

### 設計原則 {#design-principles}

TiDBのパーティションテーブルでは、ローカルインデックスのキープレフィックスはパーティションIDですが、グローバルインデックスのキープレフィックスはテーブルIDです。この設計により、グローバルインデックスデータがTiKV上で連続的に分散され、インデックス検索に必要なRPCリクエストの数が削減されます。

```sql
CREATE TABLE `sbtest` (
  `id` int(11) NOT NULL,
  `k` int(11) NOT NULL DEFAULT '0',
  `c` char(120) NOT NULL DEFAULT '',
  KEY idx(k),
  KEY global_idx(k) GLOBAL
) partition by hash(id) partitions 5;
```

前述のテーブルスキーマを例に挙げましょう。1 `idx`ローカルインデックス、 `global_idx`はグローバルインデックスです。5 のデータは`PartitionID1_i_xxx`や`PartitionID2_i_xxx`など`idx`つの異なる範囲に分散されていますが、 `global_idx`のデータは単一の範囲 ( `TableID_i_xxx` ) に集中しています。

`k`に関連するクエリ（例えば`SELECT * FROM sbtest WHERE k > 1`を実行すると、ローカルインデックス`idx`は5つの個別の範囲を生成しますが、グローバルインデックス`global_idx`は1つの範囲のみを生成します。TiDBの各範囲は1つ以上のRPCリクエストに対応するため、グローバルインデックスを使用することでRPCリクエストの数を数倍削減でき、インデックスクエリのパフォーマンスが向上します。

次の図は、 `idx`と`global_idx`という 2 つの異なるインデックスを使用して`SELECT * FROM sbtest WHERE k > 1`ステートメントを実行した場合の RPC 要求とデータ フローの違いを示しています。

![Mechanism of Global Indexes](/media/global-index-mechanism.png)

### エンコード方法 {#encoding-method}

TiDBでは、インデックスエントリはキーと値のペアとしてエンコードされます。パーティションテーブルの場合、各パーティションはTiKVレイヤーで独立した物理テーブルとして扱われ、それぞれに`partitionID`設定されます。したがって、パーティションテーブルにおけるインデックスエントリのエンコードは次のようになります。

    Unique key
    Key:
    - PartitionID_indexID_ColumnValues

    Value:
    - IntHandle
     - TailLen_IntHandle

    - CommonHandle
     - TailLen_IndexVersion_CommonHandle

    Non-unique key
    Key:
    - PartitionID_indexID_ColumnValues_Handle

    Value:
    - IntHandle
     - TailLen_Padding

    - CommonHandle
     - TailLen_IndexVersion

グローバルインデックスの場合、インデックスエントリのエンコーディングは異なります。グローバルインデックスのキーレイアウトが現在のインデックスキーのエンコーディングと互換性を保つため、新しいインデックスエンコーディングレイアウトは次のように定義されます。

    Unique key
    Key:
    - TableID_indexID_ColumnValues

    Value:
    - IntHandle
     - TailLen_PartitionID_IntHandle

    - CommonHandle
     - TailLen_IndexVersion_CommonHandle_PartitionID

    Non-unique key
    Key:
    - TableID_indexID_ColumnValues_Handle

    Value:
    - IntHandle
     - TailLen_PartitionID

    - CommonHandle
     - TailLen_IndexVersion_PartitionID

このエンコーディング方式では、 `TableID`グローバルインデックスキーの先頭に配置され、 `PartitionID`が値に格納されます。この設計の利点は、既存のインデックスキーエンコーディングとの互換性が確保されることです。しかし、いくつかの課題も生じます。例えば、 `DROP PARTITION`や`TRUNCATE PARTITION`などのDDL操作を実行する場合、インデックスエントリが連続して格納されないため、追加の処理が必要になります。

## パフォーマンステスト結果 {#performance-test-results}

次のテストは、sysbench の`select_random_points`シナリオに基づいており、主にさまざまなパーティション戦略とインデックス作成方法でのクエリ パフォーマンスを比較するために使用されます。

テストで使用されるテーブル スキーマは次のとおりです。

```sql
CREATE TABLE `sbtest` (
  `id` int(11) NOT NULL,
  `k` int(11) NOT NULL DEFAULT '0',
  `c` char(120) NOT NULL DEFAULT '',
  `pad` char(60) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */,
  KEY `k_1` (`k`)
  /* Key `k_1` (`k`, `c`) GLOBAL */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
/* Partition by hash(`id`) partitions 100 */
/* Partition by range(`id`) xxxx */
```

ワークロード SQL は次のとおりです。

```sql
SELECT id, k, c, pad
FROM sbtest
WHERE k IN (xx, xx, xx)
```

範囲パーティション（100 パーティション）:

| テーブルタイプ                                         | 同時実行1 | 同時実行数 32 | 同時実行数 64 | 平均RU   |
| ----------------------------------------------- | ----- | -------- | -------- | ------ |
| クラスタ化された非パーティションテーブル                            | 225   | 19,999   | 30,293   | 7.92   |
| PK でパーティション化されたクラスター化テーブル範囲                     | 68    | 480      | 511      | 114.87 |
| PK によって範囲分割されたクラスター化テーブル、 `k` `c`グローバル インデックスあり | 207   | 17,798   | 27,707   | 11.73  |

ハッシュパーティション（100パーティション）:

| テーブルタイプ                                     | 同時実行1 | 同時実行数 32 | 同時実行数 64 | 平均RU   |
| ------------------------------------------- | ----- | -------- | -------- | ------ |
| クラスタ化された非パーティションテーブル                        | 166   | 20,361   | 28,922   | 7.86   |
| PK で分割されたクラスタ化テーブルハッシュ                      | 60    | 244      | 283      | 119.73 |
| PKでハッシュ分割されたクラスタ化テーブル、 `k` `c`グローバルインデックスあり | 156   | 18,233   | 15,581   | 10.77  |

前述のテストでは、高同時実行環境において、グローバルインデックスによってパーティションテーブルのクエリパフォーマンスが大幅に向上し、最大50倍のパフォーマンス向上が実現できることが実証されています。さらに、グローバルインデックスはリクエストユニット（RU）の消費量を大幅に削減します。パーティション数が増えるにつれて、パフォーマンスのメリットはさらに顕著になります。
