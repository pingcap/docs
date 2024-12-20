---
title: Placement Rules in SQL
summary: SQL ステートメントを使用してテーブルとパーティションの配置をスケジュールする方法を学習します。
---

# SQL の配置ルール {#placement-rules-in-sql}

SQL の配置ルールは、SQL ステートメントを使用して TiKV クラスター内のデータの保存場所を指定できる機能です。この機能を使用すると、クラスター、データベース、テーブル、またはパーティションのデータを特定のリージョン、データセンター、ラック、またはホストにスケジュールできます。

この機能は、次のユースケースを満たすことができます。

-   複数のデータセンターにデータをデプロイ、高可用性戦略を最適化するためのルールを構成します。
-   異なるアプリケーションからの複数のデータベースをマージし、異なるユーザーのデータを物理的に分離することで、インスタンス内の異なるユーザーの分離要件を満たします。
-   重要なデータのレプリカ数を増やして、アプリケーションの可用性とデータの信頼性を向上させます。

> **注記：**
>
> この機能は[TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)クラスターでは使用できません。

## 概要 {#overview}

SQL の配置ルール機能を使用すると、次のように、粗い粒度から細かい粒度までのさまざまなレベルのデータに対して、 [配置ポリシーを作成する](#create-and-attach-placement-policies)な配置ポリシーを構成できます。

| レベル     | 説明                                                                                                                                                                      |
| ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| クラスタ    | デフォルトでは、TiDB はクラスターに対して 3 つのレプリカのポリシーを構成します。クラスターのグローバル配置ポリシーを構成することができます。詳細については、 [クラスタ全体のレプリカ数を指定する](#specify-the-number-of-replicas-globally-for-a-cluster)参照してください。 |
| データベース  | 特定のデータベースの配置ポリシーを構成できます。詳細については、 [データベースのデフォルトの配置ポリシーを指定する](#specify-a-default-placement-policy-for-a-database)参照してください。                                                |
| テーブル    | 特定のテーブルに対して配置ポリシーを設定できます。詳細については、 [テーブルの配置ポリシーを指定する](#specify-a-placement-policy-for-a-table)参照してください。                                                                  |
| パーティション | テーブル内の異なる行にパーティションを作成し、パーティションの配置ポリシーを個別に構成できます。詳細については、 [パーティションテーブルの配置ポリシーを指定する](#specify-a-placement-policy-for-a-partitioned-table)参照してください。                        |

> **ヒント：**
>
> *SQL での配置ルール*の実装は、PD の*配置ルール機能*に依存します。詳細については、 [配置ルールを構成する](https://docs.pingcap.com/tidb/stable/configure-placement-rules)を参照してください。SQL での配置ルールのコンテキストでは、*配置ルールは、*他のオブジェクトに添付された*配置ポリシー*、または TiDB から PD に送信されるルールを指す場合があります。

## 制限事項 {#limitations}

-   メンテナンスを簡素化するために、クラスター内の配置ポリシーの数を 10 以下に制限することをお勧めします。
-   配置ポリシーがアタッチされるテーブルとパーティションの合計数は 10,000 以下に制限することをお勧めします。ポリシーをアタッチするテーブルとパーティションが多すぎると、PD の計算ワークロードが増加し、サービス パフォーマンスに影響する可能性があります。
-   他の複雑な配置ポリシーを使用するのではなく、このドキュメントに示されている例に従って SQL 機能の配置ルールを使用することをお勧めします。

## 前提条件 {#prerequisites}

配置ポリシーは、TiKV ノードのラベルの構成に依存します。たとえば、配置オプション`PRIMARY_REGION`は、TiKV のラベル`region`に依存します。

<CustomContent platform="tidb">

配置ポリシーを作成すると、TiDB はポリシーで指定されたラベルが存在するかどうかをチェックしません。代わりに、ポリシーをアタッチするときに TiDB がチェックを実行します。したがって、配置ポリシーをアタッチする前に、各 TiKV ノードが正しいラベルで構成されていることを確認してください。TiDB セルフマネージド クラスターの構成方法は次のとおりです。

    tikv-server --labels region=<region>,zone=<zone>,host=<host>

詳細な設定方法については、次の例を参照してください。

| 展開方法                    | 例                                                                                                                                  |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| 手動展開                    | [トポロジラベルによるレプリカのスケジュール](/schedule-replicas-by-topology-labels.md)                                                                  |
| TiUPによる展開               | [地理的に分散した展開トポロジ](/geo-distributed-deployment-topology.md)                                                                          |
| TiDB Operatorによるデプロイメント | [KubernetesでTiDBクラスターを構成する](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-a-tidb-cluster#high-availability-of-data) |

> **注記：**
>
> TiDB Cloud Dedicated クラスターの場合、 TiDB Cloud Dedicated クラスター内の TiKV ノードのラベルは自動的に構成されるため、これらのラベル構成手順をスキップできます。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB Cloud Dedicated クラスターの場合、TiKV ノードのラベルは自動的に構成されます。

</CustomContent>

現在の TiKV クラスターで使用可能なすべてのラベルを表示するには、次の[`SHOW PLACEMENT LABELS`](/sql-statements/sql-statement-show-placement-labels.md)ステートメントを使用します。

```sql
SHOW PLACEMENT LABELS;
+--------+----------------+
| Key    | Values         |
+--------+----------------+
| disk   | ["ssd"]        |
| region | ["us-east-1"]  |
| zone   | ["us-east-1a"] |
+--------+----------------+
3 rows in set (0.00 sec)
```

## 使用法 {#usage}

このセクションでは、SQL ステートメントを使用して配置ポリシーを作成、アタッチ、表示、変更、および削除する方法について説明します。

### 配置ポリシーを作成して添付する {#create-and-attach-placement-policies}

1.  配置ポリシーを作成するには、 [`CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-create-placement-policy.md)ステートメントを使用します。

    ```sql
    CREATE PLACEMENT POLICY myplacementpolicy PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1";
    ```

    この声明では、

    -   `PRIMARY_REGION="us-east-1"`オプションは、 `region`ラベルのノードにRaft Leaders を`us-east-1`として配置することを意味します。
    -   `REGIONS="us-east-1,us-west-1"`オプションは、 `region`ラベルのノードに`us-east-1`として、 `region`ラベルのノードに`us-west-1`としてRaft Followers を配置することを意味します。

    構成可能な配置オプションとその意味の詳細については、 [配置オプション](#placement-option-reference)を参照してください。

2.  テーブルまたはパーティションテーブルに配置ポリシーをアタッチするには、 `CREATE TABLE`または`ALTER TABLE`ステートメントを使用して、そのテーブルまたはパーティションテーブルの配置ポリシーを指定します。

    ```sql
    CREATE TABLE t1 (a INT) PLACEMENT POLICY=myplacementpolicy;
    CREATE TABLE t2 (a INT);
    ALTER TABLE t2 PLACEMENT POLICY=myplacementpolicy;
    ```

    `PLACEMENT POLICY`どのデータベース スキーマにも関連付けられておらず、グローバル スコープでアタッチできます。したがって、 `CREATE TABLE`使用して配置ポリシーを指定する場合、追加の権限は必要ありません。

### 配置ポリシーをビュー {#view-placement-policies}

-   既存の配置ポリシーを表示するには、次の[`SHOW CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-show-create-placement-policy.md)ステートメントを使用します。

    ```sql
    SHOW CREATE PLACEMENT POLICY myplacementpolicy\G
    *************************** 1. row ***************************
           Policy: myplacementpolicy
    Create Policy: CREATE PLACEMENT POLICY myplacementpolicy PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1"
    1 row in set (0.00 sec)
    ```

-   特定のテーブルにアタッチされている配置ポリシーを表示するには、次の[`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md)ステートメントを使用します。

    ```sql
    SHOW CREATE TABLE t1\G
    *************************** 1. row ***************************
           Table: t1
    Create Table: CREATE TABLE `t1` (
      `a` int DEFAULT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin /*T![placement] PLACEMENT POLICY=`myplacementpolicy` */
    1 row in set (0.00 sec)
    ```

-   クラスター内の配置ポリシーの定義を表示するには、 [`INFORMATION_SCHEMA.PLACEMENT_POLICIES`](/information-schema/information-schema-placement-policies.md)システム テーブルをクエリします。

    ```sql
    SELECT * FROM information_schema.placement_policies\G
    ***************************[ 1. row ]***************************
    POLICY_ID            | 1
    CATALOG_NAME         | def
    POLICY_NAME          | p1
    PRIMARY_REGION       | us-east-1
    REGIONS              | us-east-1,us-west-1
    CONSTRAINTS          |
    LEADER_CONSTRAINTS   |
    FOLLOWER_CONSTRAINTS |
    LEARNER_CONSTRAINTS  |
    SCHEDULE             |
    FOLLOWERS            | 4
    LEARNERS             | 0
    1 row in set
    ```

-   クラスター内の配置ポリシーに関連付けられているすべてのテーブルを表示するには、 `information_schema.tables`のシステム テーブルの`tidb_placement_policy_name`列目をクエリします。

    ```sql
    SELECT * FROM information_schema.tables WHERE tidb_placement_policy_name IS NOT NULL;
    ```

-   クラスター内の配置ポリシーに関連付けられているすべてのパーティションを表示するには、 `information_schema.partitions`システム テーブルの`tidb_placement_policy_name`列目をクエリします。

    ```sql
    SELECT * FROM information_schema.partitions WHERE tidb_placement_policy_name IS NOT NULL;
    ```

-   すべてのオブジェクトに添付された配置ポリシーは*非同期的に*適用されます。配置ポリシーのスケジュールの進行状況を確認するには、 [`SHOW PLACEMENT`](/sql-statements/sql-statement-show-placement.md)ステートメントを使用できます。

    ```sql
    SHOW PLACEMENT;
    ```

### 配置ポリシーを変更する {#modify-placement-policies}

配置ポリシーを変更するには、 [`ALTER PLACEMENT POLICY`](/sql-statements/sql-statement-alter-placement-policy.md)ステートメントを使用できます。変更は、対応するポリシーに関連付けられているすべてのオブジェクトに適用されます。

```sql
ALTER PLACEMENT POLICY myplacementpolicy FOLLOWERS=4;
```

このステートメントでは、 `FOLLOWERS=4`オプションは、 4 つのフォロワーと 1 つのLeaderを含む、データの 5 つのレプリカを構成することを意味します。 構成可能な配置オプションとその意味の詳細については、 [配置オプションリファレンス](#placement-option-reference)参照してください。

### ドロップ配置ポリシー {#drop-placement-policies}

どのテーブルまたはパーティションにもアタッチされていないポリシーを削除するには、次の[`DROP PLACEMENT POLICY`](/sql-statements/sql-statement-drop-placement-policy.md)ステートメントを使用します。

```sql
DROP PLACEMENT POLICY myplacementpolicy;
```

## 配置オプションリファレンス {#placement-option-reference}

配置ポリシーを作成または変更するときに、必要に応じて配置オプションを構成できます。

> **注記：**
>
> `PRIMARY_REGION` 、 `REGIONS` 、 `SCHEDULE`オプションは`CONSTRAINTS`オプションと同時に指定できません。指定するとエラーが発生します。

### 通常の配置オプション {#regular-placement-options}

通常の配置オプションは、データ配置の基本要件を満たすことができます。

| オプション名           | 説明                                                                                 |
| ---------------- | ---------------------------------------------------------------------------------- |
| `PRIMARY_REGION` | このオプションの値と一致する`region`ラベルを持つノードにRaftリーダーを配置することを指定します。                             |
| `REGIONS`        | このオプションの値に一致する`region`ラベルを持つノードにRaft Follower を配置することを指定します。                       |
| `SCHEDULE`       | フォロワーの配置をスケジュールするための戦略を指定します。値のオプションは`EVEN` (デフォルト) または`MAJORITY_IN_PRIMARY`です。    |
| `FOLLOWERS`      | フォロワーの数を指定します。たとえば、 `FOLLOWERS=2`データのレプリカが 3 つあることを意味します (フォロワーが 2 つ、Leaderが 1 つ)。 |

### 高度な配置オプション {#advanced-placement-options}

高度な構成オプションを使用すると、複雑なシナリオの要件を満たすために、データ配置の柔軟性が高まります。ただし、高度なオプションの構成は通常のオプションよりも複雑であり、クラスター トポロジと TiDB データ シャーディングについて深く理解している必要があります。

| オプション名                 | 説明                                                                              |
| ---------------------- | ------------------------------------------------------------------------------- |
| `CONSTRAINTS`          | すべてのロールに適用される制約のリスト。たとえば、 `CONSTRAINTS="[+disk=ssd]"` 。                         |
| `LEADER_CONSTRAINTS`   | Leaderにのみ適用される制約のリスト。                                                           |
| `FOLLOWER_CONSTRAINTS` | フォロワーにのみ適用される制約のリスト。                                                            |
| `LEARNER_CONSTRAINTS`  | 学習者にのみ適用される制約のリスト。                                                              |
| `LEARNERS`             | 学習者の数。                                                                          |
| `SURVIVAL_PREFERENCE`  | ラベルの災害許容レベルに応じたレプリカ配置の優先順位。たとえば、 `SURVIVAL_PREFERENCE="[region, zone, host]"` 。 |

### 制約フォーマット {#constraints-formats}

次のいずれかの形式を使用して、 `CONSTRAINTS` 、 `FOLLOWER_CONSTRAINTS` 、および`LEARNER_CONSTRAINTS`配置オプションを設定できます。

| CONSTRAINTS 形式 | 説明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| リスト形式          | 指定する制約がすべてのレプリカに適用される場合、キー値リスト形式を使用できます。各キーは`+`または`-`で始まります。例:<br/><ul><li> `[+region=us-east-1]` `region`ラベルを持つノードにデータを`us-east-1`として配置することを意味します。</li><li> `[+region=us-east-1,-type=fault]` `region`ラベルが`us-east-1`であるが、 `type`ラベルが`fault`ではないノードにデータを配置することを意味します。</li></ul><br/>                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 辞書形式           | 異なる制約に対して異なるレプリカ数を指定する必要がある場合は、辞書形式を使用できます。例:<br/><ul><li> `FOLLOWER_CONSTRAINTS="{+region=us-east-1: 1,+region=us-east-2: 1,+region=us-west-1: 1}";` 、 `us-east-1`にFollowerを 1 人、 `us-east-2`にFollowerを 1 人、 `us-west-1`にFollowerを 1 人配置することを意味します。</li><li> `FOLLOWER_CONSTRAINTS='{"+region=us-east-1,+type=scale-node": 1,"+region=us-west-1": 1}';` 、 `us-east-1`領域にあり、 `type`ラベルが`scale-node`であるノードに 1 つのFollowerを配置し、 `us-west-1`に 1 つのFollowerを配置することを意味します。</li></ul>辞書形式は、 `+`または`-`で始まる各キーをサポートし、特別な`#evict-leader`属性を構成できます。たとえば、 `FOLLOWER_CONSTRAINTS='{"+region=us-east-1":1, "+region=us-east-2": 2, "+region=us-west-1,#evict-leader": 1}'` 、 `us-west-1`で選出されたリーダーが災害復旧中に可能な限り排除されることを意味します。 |

> **注記：**
>
> -   `LEADER_CONSTRAINTS`配置オプションはリスト形式のみをサポートします。
> -   リスト形式と辞書形式はどちらも YAML パーサーに基づいていますが、場合によっては YAML 構文が誤って解析されることがあります。たとえば、 `"{+region=east:1,+region=west:2}"` ( `:`後にスペースがない) は`'{"+region=east:1": null, "+region=west:2": null}'`と誤って解析される可能性がありますが、これは予期しません。ただし、 `"{+region=east: 1,+region=west: 2}"` ( `:`の後にスペースがある) は`'{"+region=east": 1, "+region=west": 2}'`と正しく解析されます。したがって、 `:`の後にスペースを追加することをお勧めします。

## 基本的な例 {#basic-examples}

### クラスタ全体のレプリカ数を指定する {#specify-the-number-of-replicas-globally-for-a-cluster}

クラスターが初期化された後、デフォルトのレプリカ数は`3`です。クラスターにさらに多くのレプリカが必要な場合は、配置ポリシーを構成してこの数を増やし、 [`ALTER RANGE`](/sql-statements/sql-statement-alter-range.md)使用してクラスター レベルでポリシーを適用できます。例:

```sql
CREATE PLACEMENT POLICY five_replicas FOLLOWERS=4;
ALTER RANGE global PLACEMENT POLICY five_replicas;
```

TiDB ではリーダーの数がデフォルトで`1`に設定されているので、 `five replicas`フォロワーが`4` 、Leaderが`1`であることを意味することに注意してください。

### データベースのデフォルトの配置ポリシーを指定する {#specify-a-default-placement-policy-for-a-database}

データベースのデフォルトの配置ポリシーを指定できます。これは、データベースのデフォルトの文字セットまたは照合順序を設定するのと同様に機能します。データベース内のテーブルまたはパーティションに他の配置ポリシーが指定されていない場合は、データベースの配置ポリシーがテーブルとパーティションに適用されます。例:

```sql
CREATE PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-east-2";  -- Creates a placement policy

CREATE PLACEMENT POLICY p2 FOLLOWERS=4;

CREATE PLACEMENT POLICY p3 FOLLOWERS=2;

CREATE TABLE t1 (a INT);  -- Creates a table t1 without specifying any placement policy.

ALTER DATABASE test PLACEMENT POLICY=p2;  -- Changes the default placement policy of the database to p2, which does not apply to the existing table t1.

CREATE TABLE t2 (a INT);  -- Creates a table t2. The default placement policy p2 applies to t2.

CREATE TABLE t3 (a INT) PLACEMENT POLICY=p1;  -- Creates a table t3. Because this statement has specified another placement rule, the default placement policy p2 does not apply to table t3.

ALTER DATABASE test PLACEMENT POLICY=p3;  -- Changes the default policy of the database again, which does not apply to existing tables.

CREATE TABLE t4 (a INT);  -- Creates a table t4. The default placement policy p3 applies to t4.

ALTER PLACEMENT POLICY p3 FOLLOWERS=3; -- `FOLLOWERS=3` applies to the table attached with policy p3 (that is, table t4).
```

テーブルからそのパーティションへのポリシー継承は、前述の例のポリシー継承とは異なることに注意してください。テーブルのデフォルト ポリシーを変更すると、新しいポリシーはそのテーブル内のパーティションにも適用されます。ただし、テーブルがデータベースからポリシーを継承するのは、ポリシーを指定せずに作成された場合のみです。テーブルがデータベースからポリシーを継承すると、データベースのデフォルト ポリシーを変更してもそのテーブルには適用されません。

### テーブルの配置ポリシーを指定する {#specify-a-placement-policy-for-a-table}

テーブルのデフォルトの配置ポリシーを指定できます。例:

```sql
CREATE PLACEMENT POLICY five_replicas FOLLOWERS=4;

CREATE TABLE t (a INT) PLACEMENT POLICY=five_replicas;  -- Creates a table t and attaches the 'five_replicas' placement policy to it.

ALTER TABLE t PLACEMENT POLICY=default; -- Removes the placement policy 'five_replicas' from the table t and resets the placement policy to the default one.
```

### パーティションテーブルの配置ポリシーを指定する {#specify-a-placement-policy-for-a-partitioned-table}

パーティションテーブルまたはパーティションの配置ポリシーを指定することもできます。例:

```sql
CREATE PLACEMENT POLICY storageforhistorydata CONSTRAINTS="[+node=history]";
CREATE PLACEMENT POLICY storagefornewdata CONSTRAINTS="[+node=new]";
CREATE PLACEMENT POLICY companystandardpolicy CONSTRAINTS="";

CREATE TABLE t1 (id INT, name VARCHAR(50), purchased DATE, UNIQUE INDEX idx(id) GLOBAL)
PLACEMENT POLICY=companystandardpolicy
PARTITION BY RANGE( YEAR(purchased) ) (
  PARTITION p0 VALUES LESS THAN (2000) PLACEMENT POLICY=storageforhistorydata,
  PARTITION p1 VALUES LESS THAN (2005),
  PARTITION p2 VALUES LESS THAN (2010),
  PARTITION p3 VALUES LESS THAN (2015),
  PARTITION p4 VALUES LESS THAN MAXVALUE PLACEMENT POLICY=storagefornewdata
);
```

テーブル内のパーティションに配置ポリシーが指定されていない場合、パーティションはテーブルからポリシー (存在する場合) を継承しようとします。テーブルに[グローバルインデックス](/partitioned-table.md#global-indexes)がある場合、インデックスはテーブルと同じ配置ポリシーを適用します。上記の例では、次のようになります。

-   `p0`パーティションには`storageforhistorydata`ポリシーが適用されます。
-   `p4`パーティションには`storagefornewdata`ポリシーが適用されます。
-   `p1` 、および`p3`パーティションには`p2`表`t1`から継承された`companystandardpolicy`配置ポリシーが適用されます。
-   グローバルインデックス`idx`テーブル`t1`と同じ`companystandardpolicy`配置ポリシーが適用されます。
-   テーブル`t1`に配置ポリシーが指定されていない場合、パーティション`p1` 、 `p2` 、 `p3`およびグローバル インデックス`idx`は、データベースのデフォルト ポリシーまたはグローバルのデフォルト ポリシーを継承します。

これらのパーティションに配置ポリシーをアタッチした後、次の例のように特定のパーティションの配置ポリシーを変更できます。

```sql
ALTER TABLE t1 PARTITION p1 PLACEMENT POLICY=storageforhistorydata;
```

## 高可用性の例 {#high-availability-examples}

次のトポロジを持つクラスターがあり、TiKV ノードが 3 つのリージョンに分散され、各リージョンに 3 つの利用可能なゾーンが含まれているとします。

```sql
SELECT store_id,address,label from INFORMATION_SCHEMA.TIKV_STORE_STATUS;
+----------+-----------------+--------------------------------------------------------------------------------------------------------------------------+
| store_id | address         | label                                                                                                                    |
+----------+-----------------+--------------------------------------------------------------------------------------------------------------------------+
|        1 | 127.0.0.1:20163 | [{"key": "region", "value": "us-east-1"}, {"key": "zone", "value": "us-east-1a"}, {"key": "host", "value": "host1"}]     |
|        2 | 127.0.0.1:20162 | [{"key": "region", "value": "us-east-1"}, {"key": "zone", "value": "us-east-1b"}, {"key": "host", "value": "host2"}]     |
|        3 | 127.0.0.1:20164 | [{"key": "region", "value": "us-east-1"}, {"key": "zone", "value": "us-east-1c"}, {"key": "host", "value": "host3"}]     |
|        4 | 127.0.0.1:20160 | [{"key": "region", "value": "us-east-2"}, {"key": "zone", "value": "us-east-2a"}, {"key": "host", "value": "host4"}]     |
|        5 | 127.0.0.1:20161 | [{"key": "region", "value": "us-east-2"}, {"key": "zone", "value": "us-east-2b"}, {"key": "host", "value": "host5"}]     |
|        6 | 127.0.0.1:20165 | [{"key": "region", "value": "us-east-2"}, {"key": "zone", "value": "us-east-2c"}, {"key": "host", "value": "host6"}]     |
|        7 | 127.0.0.1:20166 | [{"key": "region", "value": "us-west-1"}, {"key": "zone", "value": "us-west-1a"}, {"key": "host", "value": "host7"}]     |
|        8 | 127.0.0.1:20167 | [{"key": "region", "value": "us-west-1"}, {"key": "zone", "value": "us-west-1b"}, {"key": "host", "value": "host8"}]     |
|        9 | 127.0.0.1:20168 | [{"key": "region", "value": "us-west-1"}, {"key": "zone", "value": "us-west-1c"}, {"key": "host", "value": "host9"}]     |
+----------+-----------------+--------------------------------------------------------------------------------------------------------------------------+

```

### 生存の好みを指定する {#specify-survival-preferences}

正確なデータ分散については特に気にせず、災害復旧要件を満たすことを優先する場合は、 `SURVIVAL_PREFERENCES`オプションを使用してデータ存続の設定を指定できます。

前の例と同様に、TiDB クラスターは 3 つのリージョンに分散されており、各リージョンには 3 つのゾーンが含まれています。このクラスターの配置ポリシーを作成するときは、 `SURVIVAL_PREFERENCES`を次のように構成すると仮定します。

```sql
CREATE PLACEMENT POLICY multiaz SURVIVAL_PREFERENCES="[region, zone, host]";
CREATE PLACEMENT POLICY singleaz CONSTRAINTS="[+region=us-east-1]" SURVIVAL_PREFERENCES="[zone]";
```

配置ポリシーを作成したら、必要に応じて対応するテーブルに添付できます。

-   `multiaz`の配置ポリシーが関連付けられているテーブルの場合、データは異なるリージョンの 3 つのレプリカに配置され、データ分離のクロスリージョン存続目標、次にクロスゾーン存続目標、最後にクロスホスト存続目標を満たすことが優先されます。
-   `singleaz`の配置ポリシーがアタッチされたテーブルの場合、データは最初に`us-east-1`リージョンの 3 つのレプリカに配置され、その後、データ分離のゾーン間存続目標が満たされます。

<CustomContent platform="tidb">

> **注記：**
>
> `SURVIVAL_PREFERENCES`はPDでは`location-labels`に相当します。詳細については[トポロジラベルによるレプリカのスケジュール](/schedule-replicas-by-topology-labels.md)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> `SURVIVAL_PREFERENCES`はPDでは`location-labels`に相当します。詳細については[トポロジラベルによるレプリカのスケジュール](https://docs.pingcap.com/tidb/stable/schedule-replicas-by-topology-labels)参照してください。

</CustomContent>

### 複数のデータセンターに2:2:1で分散された5つのレプリカを持つクラスターを指定します。 {#specify-a-cluster-with-5-replicas-distributed-2-2-1-across-multiple-data-centers}

2:2:1 の比率で 5 つのレプリカを分散するなど、特定のデータ分散が必要な場合は、次の[辞書の形式](#constraints-formats)の`CONSTRAINTS`構成することで、さまざまな制約に対して異なる数のレプリカを指定できます。

```sql
CREATE PLACEMENT POLICY `deploy221` CONSTRAINTS='{"+region=us-east-1":2, "+region=us-east-2": 2, "+region=us-west-1": 1}';

ALTER RANGE global PLACEMENT POLICY = "deploy221";

SHOW PLACEMENT;
+-------------------+---------------------------------------------------------------------------------------------+------------------+
| Target            | Placement                                                                                   | Scheduling_State |
+-------------------+---------------------------------------------------------------------------------------------+------------------+
| POLICY deploy221  | CONSTRAINTS="{\"+region=us-east-1\":2, \"+region=us-east-2\": 2, \"+region=us-west-1\": 1}" | NULL             |
| RANGE TiDB_GLOBAL | CONSTRAINTS="{\"+region=us-east-1\":2, \"+region=us-east-2\": 2, \"+region=us-west-1\": 1}" | SCHEDULED        |
+-------------------+---------------------------------------------------------------------------------------------+------------------+
```

クラスターにグローバル`deploy221`配置ポリシーが設定されると、TiDB はこのポリシーに従ってデータを分散します。つまり、 `us-east-1`リージョンに 2 つのレプリカ、 `us-east-2`リージョンに 2 つのレプリカ、 `us-west-1`リージョンに 1 つのレプリカを配置します。

### リーダーとフォロワーの分布を指定する {#specify-the-distribution-of-leaders-and-followers}

制約または`PRIMARY_REGION`使用して、リーダーとフォロワーの特定の分布を指定できます。

#### 制約を使用する {#use-constraints}

ノード間でのRaftリーダーの分散に関して特定の要件がある場合は、次のステートメントを使用して配置ポリシーを指定できます。

```sql
CREATE PLACEMENT POLICY deploy221_primary_east1 LEADER_CONSTRAINTS="[+region=us-east-1]" FOLLOWER_CONSTRAINTS='{"+region=us-east-1": 1, "+region=us-east-2": 2, "+region=us-west-1": 1}';
```

この配置ポリシーが作成され、目的のデータにアタッチされると、データのRaftLeaderレプリカは`LEADER_CONSTRAINTS`オプションで指定された`us-east-1`リージョンに配置され、データの他のレプリカは`FOLLOWER_CONSTRAINTS`オプションで指定されたリージョンに配置されます。 `us-east-1`リージョンのノード停止など、クラスターに障害が発生した場合、これらのリージョンが`FOLLOWER_CONSTRAINTS`で指定されている場合でも、新しいLeaderは他のリージョンから選出されることに注意してください。つまり、サービスの可用性を確保することが最優先されます。

`us-east-1`リージョンで障害が発生した場合、 `us-west-1`に新しいリーダーを配置したくない場合は、そのリージョンで新しく選出されたリーダーを排除するための特別な`evict-leader`属性を構成できます。

```sql
CREATE PLACEMENT POLICY deploy221_primary_east1 LEADER_CONSTRAINTS="[+region=us-east-1]" FOLLOWER_CONSTRAINTS='{"+region=us-east-1": 1, "+region=us-east-2": 2, "+region=us-west-1,#evict-leader": 1}';
```

#### <code>PRIMARY_REGION</code>使用する {#use-code-primary-region-code}

クラスター トポロジで`region`ラベルが設定されている場合は、 `PRIMARY_REGION`および`REGIONS`オプションを使用してフォロワーの配置ポリシーを指定することもできます。

```sql
CREATE PLACEMENT POLICY eastandwest PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-east-2,us-west-1" SCHEDULE="MAJORITY_IN_PRIMARY" FOLLOWERS=4;
CREATE TABLE t1 (a INT) PLACEMENT POLICY=eastandwest;
```

-   `PRIMARY_REGION`リーダーの配布地域を指定します。このオプションでは 1 つの地域のみ指定できます。
-   `SCHEDULE`オプションは、TiDB がフォロワーの分散をどのようにバランスさせるかを指定します。
    -   デフォルトの`EVEN`スケジュール ルールにより、すべてのリージョンにわたってフォロワーが均等に分散されます。
    -   十分な数のFollowerレプリカが`PRIMARY_REGION` (つまり`us-east-1` ) に配置されるようにするには、 `MAJORITY_IN_PRIMARY`スケジュール ルールを使用できます。このスケジュール ルールでは、可用性を犠牲にして、トランザクションのレイテンシーが低くなります。プライマリ リージョンに障害が発生した場合、 `MAJORITY_IN_PRIMARY`自動フェイルオーバーは提供されません。

## データ分離の例 {#data-isolation-examples}

次の例のように、配置ポリシーを作成するときに、各ポリシーに制約を構成して、指定された`app`ラベルを持つ TiKV ノードにデータを配置するように要求できます。

```sql
CREATE PLACEMENT POLICY app_order CONSTRAINTS="[+app=order]";
CREATE PLACEMENT POLICY app_list CONSTRAINTS="[+app=list_collection]";
CREATE TABLE order (id INT, name VARCHAR(50), purchased DATE)
PLACEMENT POLICY=app_order
CREATE TABLE list (id INT, name VARCHAR(50), purchased DATE)
PLACEMENT POLICY=app_list
```

この例では、制約は`[+app=order]`などのリスト形式を使用して指定されています。 `{+app=order: 3}`などの辞書形式を使用して指定することもできます。

例のステートメントを実行すると、TiDB は`app_order`データを`app`ラベルを持つ TiKV ノードに`order`として配置し、 `app_list`データを`app`ラベルを持つ TiKV ノードに`list_collection`として配置して、storage内での物理的なデータ分離を実現します。

## 互換性 {#compatibility}

## 他の機能との互換性 {#compatibility-with-other-features}

-   一時テーブルは配置ポリシーをサポートしていません。
-   配置ポリシーは、保存中のデータが正しい TiKV ノードに存在することを保証するだけで、転送中のデータ (ユーザー クエリまたは内部操作経由) が特定のリージョンでのみ発生することを保証するものではありません。
-   データのTiFlashレプリカを構成するには、配置ポリシーを使用するのではなく、 [TiFlashレプリカを作成する](/tiflash/create-tiflash-replicas.md)実行する必要があります。
-   構文糖衣規則は設定`PRIMARY_REGION`と`REGIONS`に許可されています。将来的には`PRIMARY_RACK` 、 `PRIMARY_ZONE` 、 `PRIMARY_HOST`にも多様性を追加する予定です。 [問題 #18030](https://github.com/pingcap/tidb/issues/18030)参照してください。

## ツールとの互換性 {#compatibility-with-tools}

<CustomContent platform="tidb">

| ツール名           | サポートされる最小バージョン | 説明                                                                                                                                                                                                  |
| -------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| バックアップと復元 (BR) | 6.0            | v6.0 より前のBRでは、配置ポリシーのバックアップと復元はサポートされていません。詳細については、 [配置ルールをクラスターに復元するとエラーが発生するのはなぜですか](/faq/backup-and-restore-faq.md#why-does-an-error-occur-when-i-restore-placement-rules-to-a-cluster)参照してください。 |
| TiDB Lightning | まだ互換性がありません    | TiDB Lightningが配置ポリシーを含むバックアップデータをインポートするとエラーが報告される                                                                                                                                                 |
| ティCDC          | 6.0            | 配置ポリシーを無視し、下流にポリシーを複製しません。                                                                                                                                                                          |

</CustomContent>

<CustomContent platform="tidb-cloud">

| ツール名           | サポートされる最小バージョン | 説明                                                  |
| -------------- | -------------- | --------------------------------------------------- |
| TiDB Lightning | まだ互換性がありません    | TiDB Lightningが配置ポリシーを含むバックアップデータをインポートするとエラーが報告される |
| ティCDC          | 6.0            | 配置ポリシーを無視し、下流にポリシーを複製しません。                          |

</CustomContent>
