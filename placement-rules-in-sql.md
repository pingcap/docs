---
title: Placement Rules in SQL
summary: Learn how to schedule placement of tables and partitions using SQL statements.
---

# SQL の配置ルール {#placement-rules-in-sql}

SQL の配置ルールは、SQL ステートメントを使用して TiKV クラスター内のデータの保存場所を指定できる機能です。この機能を使用すると、クラスター、データベース、テーブル、またはパーティションのデータを特定のリージョン、データセンター、ラック、またはホストにスケジュールできます。

この機能は、次のユースケースを実現できます。

-   複数のデータセンターにデータをデプロイ、ルールを構成して高可用性戦略を最適化します。
-   異なるアプリケーションからの複数のデータベースを結合し、異なるユーザーのデータを物理的に分離します。これにより、インスタンス内の異なるユーザーの分離要件が満たされます。
-   重要なデータのレプリカの数を増やして、アプリケーションの可用性とデータの信頼性を向上させます。

> **注記：**
>
> この機能は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターでは使用できません。

## 概要 {#overview}

SQL の配置ルール機能を使用すると、次のように、粗いものから細かいものまでの粒度で、さまざまなレベルのデータに必要な配置ポリシーを[配置ポリシーを作成する](#create-and-attach-placement-policies)できます。

| レベル     | 説明                                                                                                                                                                        |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| クラスタ    | デフォルトでは、TiDB はクラスターに対して 3 つのレプリカのポリシーを構成します。クラスターのグローバル配置ポリシーを構成できます。詳細については、 [クラスターのグローバルなレプリカの数を指定する](#specify-the-number-of-replicas-globally-for-a-cluster)を参照してください。 |
| データベース  | 特定のデータベースの配置ポリシーを構成できます。詳細については、 [データベースのデフォルトの配置ポリシーを指定する](#specify-a-default-placement-policy-for-a-database)を参照してください。                                                 |
| テーブル    | 特定のテーブルの配置ポリシーを構成できます。詳細については、 [テーブルの配置ポリシーを指定する](#specify-a-placement-policy-for-a-table)を参照してください。                                                                      |
| パーティション | テーブル内のさまざまな行にパーティションを作成し、パーティションの配置ポリシーを個別に構成できます。詳細については、 [パーティションテーブルの配置ポリシーを指定する](#specify-a-placement-policy-for-a-partitioned-table)を参照してください。                       |

> **ヒント：**
>
> *SQL での配置ルール*の実装は、PD の*配置ルール機能*に依存します。詳細は[配置ルールの構成](https://docs.pingcap.com/zh/tidb/stable/configure-placement-rules)を参照してください。 SQL の配置ルールのコンテキストでは、*配置ルールは*、他のオブジェクトに付加された*配置ポリシー*、または TiDB から PD に送信されるルールを指す場合があります。

## 制限事項 {#limitations}

-   メンテナンスを簡素化するために、クラスター内の配置ポリシーの数を 10 以下に制限することをお勧めします。
-   配置ポリシーが適用されるテーブルとパーティションの合計数を 10,000 以下に制限することをお勧めします。あまりにも多くのテーブルやパーティションにポリシーをアタッチすると、PD の計算ワークロードが増加し、サービスのパフォーマンスに影響を与える可能性があります。
-   他の複雑な配置ポリシーを使用するのではなく、このドキュメントで提供される例に従って SQL の配置ルール機能を使用することをお勧めします。

## 前提条件 {#prerequisites}

配置ポリシーは、TiKV ノード上のラベルの構成に依存します。たとえば、 `PRIMARY_REGION`配置オプションは TiKV の`region`ラベルに依存します。

<CustomContent platform="tidb">

配置ポリシーを作成する場合、TiDB はポリシーで指定されたラベルが存在するかどうかをチェックしません。代わりに、TiDB はポリシーをアタッチするときにチェックを実行します。したがって、配置ポリシーをアタッチする前に、各 TiKV ノードが正しいラベルで構成されていることを確認してください。 TiDB セルフホスト クラスターの構成方法は次のとおりです。

    tikv-server --labels region=<region>,zone=<zone>,host=<host>

詳細な構成方法については、次の例を参照してください。

| 導入方法                 | 例                                                                                                                                       |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| 手動展開                 | [トポロジーラベルごとにレプリカをスケジュールする](/schedule-replicas-by-topology-labels.md)                                                                    |
| TiUPによる導入            | [地理的に分散された導入トポロジ](/geo-distributed-deployment-topology.md)                                                                              |
| TiDB Operatorを使用した展開 | [Kubernetes で TiDB クラスターを構成する](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-a-tidb-cluster#high-data-high-availability) |

> **注記：**
>
> TiDB 専用クラスターの場合、TiDB 専用クラスターの TiKV ノード上のラベルは自動的に構成されるため、これらのラベル構成ステップをスキップできます。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB 専用クラスターの場合、TiKV ノード上のラベルは自動的に構成されます。

</CustomContent>

現在の TiKV クラスターで使用可能なすべてのラベルを表示するには、 [`SHOW PLACEMENT LABELS`](/sql-statements/sql-statement-show-placement-labels.md)ステートメントを使用できます。

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

### 配置ポリシーを作成してアタッチする {#create-and-attach-placement-policies}

1.  配置ポリシーを作成するには、 [`CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-create-placement-policy.md)ステートメントを使用します。

    ```sql
    CREATE PLACEMENT POLICY myplacementpolicy PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1";
    ```

    この声明では次のようになります。

    -   `PRIMARY_REGION="us-east-1"`オプションは、 `region`ラベルが`us-east-1`であるノードにRaft Leader を配置することを意味します。
    -   `REGIONS="us-east-1,us-west-1"`オプションは、 `region`ラベルを持つノードに`us-east-1`として、 `region`ラベルを持つノードに`us-west-1`としてRaft Followers を配置することを意味します。

    構成可能な配置オプションとその意味の詳細については、 [配置オプション](#placement-option-reference)を参照してください。

2.  配置ポリシーをテーブルまたはパーティションテーブルにアタッチするには、 `CREATE TABLE`または`ALTER TABLE`ステートメントを使用して、そのテーブルまたはパーティションテーブルの配置ポリシーを指定します。

    ```sql
    CREATE TABLE t1 (a INT) PLACEMENT POLICY=myplacementpolicy;
    CREATE TABLE t2 (a INT);
    ALTER TABLE t2 PLACEMENT POLICY=myplacementpolicy;
    ```

    `PLACEMENT POLICY`はデータベース スキーマに関連付けられていないため、グローバル スコープでアタッチできます。したがって、 `CREATE TABLE`を使用して配置ポリシーを指定する場合、追加の権限は必要ありません。

### 配置ポリシーをビュー {#view-placement-policies}

-   既存の配置ポリシーを表示するには、 [`SHOW CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-show-create-placement-policy.md)ステートメントを使用できます。

    ```sql
    SHOW CREATE PLACEMENT POLICY myplacementpolicy\G
    *************************** 1. row ***************************
           Policy: myplacementpolicy
    Create Policy: CREATE PLACEMENT POLICY myplacementpolicy PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1"
    1 row in set (0.00 sec)
    ```

-   特定のテーブルにアタッチされた配置ポリシーを表示するには、 [`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md)ステートメントを使用できます。

    ```sql
    SHOW CREATE TABLE t1\G
    *************************** 1. row ***************************
           Table: t1
    Create Table: CREATE TABLE `t1` (
      `a` int(11) DEFAULT NULL
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

-   クラスター内の配置ポリシーがアタッチされているすべてのテーブルを表示するには、 `information_schema.tables`システム テーブルの`tidb_placement_policy_name`列をクエリします。

    ```sql
    SELECT * FROM information_schema.tables WHERE tidb_placement_policy_name IS NOT NULL;
    ```

-   クラスター内の配置ポリシーがアタッチされているすべてのパーティションを表示するには、 `information_schema.partitions`システム テーブルの`tidb_placement_policy_name`列をクエリします。

    ```sql
    SELECT * FROM information_schema.partitions WHERE tidb_placement_policy_name IS NOT NULL;
    ```

-   すべてのオブジェクトに適用される配置ポリシーは*非同期的に*適用されます。配置ポリシーのスケジュールの進行状況を確認するには、 [`SHOW PLACEMENT`](/sql-statements/sql-statement-show-placement.md)ステートメントを使用できます。

    ```sql
    SHOW PLACEMENT;
    ```

### 配置ポリシーを変更する {#modify-placement-policies}

配置ポリシーを変更するには、 [`ALTER PLACEMENT POLICY`](/sql-statements/sql-statement-alter-placement-policy.md)ステートメントを使用できます。変更は、対応するポリシーがアタッチされているすべてのオブジェクトに適用されます。

```sql
ALTER PLACEMENT POLICY myplacementpolicy FOLLOWERS=4;
```

このステートメントの`FOLLOWERS=4`オプションは、4 つの Followers と 1 つのLeaderを含む、データの 5 つのレプリカを構成することを意味します。構成可能な配置オプションとその意味の詳細については、 [配置オプションのリファレンス](#placement-option-reference)を参照してください。

### ドロップ配置ポリシー {#drop-placement-policies}

どのテーブルまたはパーティションにもアタッチされていないポリシーを削除するには、 [`DROP PLACEMENT POLICY`](/sql-statements/sql-statement-drop-placement-policy.md)ステートメントを使用できます。

```sql
DROP PLACEMENT POLICY myplacementpolicy;
```

## 配置オプションのリファレンス {#placement-option-reference}

配置ポリシーを作成または変更するときに、必要に応じて配置オプションを構成できます。

> **注記：**
>
> `PRIMARY_REGION` 、 `REGIONS` 、 `SCHEDULE`オプションは`CONSTRAINTS`オプションと同時に指定できず、エラーとなります。

### 通常の配置オプション {#regular-placement-options}

通常の配置オプションは、データ配置の基本要件を満たすことができます。

| オプション名           | 説明                                                                                     |
| ---------------- | -------------------------------------------------------------------------------------- |
| `PRIMARY_REGION` | このオプションの値と一致する`region`ラベルを持つノードにRaftリーダーを配置することを指定します。                                 |
| `REGIONS`        | このオプションの値と一致する`region`ラベルを持つノードにRaft Followers を配置することを指定します。                          |
| `SCHEDULE`       | フォロワーの配置をスケジュールするための戦略を指定します。値のオプションは`EVEN` (デフォルト) または`MAJORITY_IN_PRIMARY`です。        |
| `FOLLOWERS`      | フォロワーの数を指定します。たとえば、 `FOLLOWERS=2` 、データのレプリカが 3 つ (2 つのフォロワーと 1 つのLeader) 存在することを意味します。 |

### 高度な配置オプション {#advanced-placement-options}

高度な構成オプションにより、複雑なシナリオの要件を満たすデータ配置の柔軟性が向上します。ただし、詳細オプションの構成は通常のオプションよりも複雑で、クラスター トポロジと TiDB データ シャーディングについて深く理解している必要があります。

| オプション名                 | 説明                                                                              |
| ---------------------- | ------------------------------------------------------------------------------- |
| `CONSTRAINTS`          | すべてのロールに適用される制約のリスト。たとえば、 `CONSTRAINTS="[+disk=ssd]"` 。                         |
| `LEADER_CONSTRAINTS`   | Leaderにのみ適用される制約のリスト。                                                           |
| `FOLLOWER_CONSTRAINTS` | フォロワーにのみ適用される制約のリスト。                                                            |
| `LEARNER_CONSTRAINTS`  | 学習者にのみ適用される制約のリスト。                                                              |
| `LEARNERS`             | 学習者の数。                                                                          |
| `SURVIVAL_PREFERENCE`  | ラベルの災害耐性レベルに応じたレプリカ配置の優先順位。たとえば、 `SURVIVAL_PREFERENCE="[region, zone, host]"` 。 |

### CONSTRAINTS 形式 {#constraints-formats}

次のいずれかの形式を使用して、 `CONSTRAINTS` 、 `FOLLOWER_CONSTRAINTS` 、および`LEARNER_CONSTRAINTS`配置オプションを構成できます。

| 制約形式  | 説明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ----- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| リスト形式 | 指定する制約がすべてのレプリカに適用される場合は、キーと値のリスト形式を使用できます。各キーは`+`または`-`で始まります。例えば：<br/><ul><li> `[+region=us-east-1]` `region`ラベルを持つノードにデータを`us-east-1`として配置することを意味します。</li><li> `[+region=us-east-1,-type=fault]` `region`ラベルを`us-east-1`として持つが、 `type`ラベルを`fault`として持たないノードにデータを配置することを意味します。</li></ul><br/>                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| 辞書形式  | さまざまな制約に対してさまざまな数のレプリカを指定する必要がある場合は、ディクショナリ形式を使用できます。例えば：<br/><ul><li> `FOLLOWER_CONSTRAINTS="{+region=us-east-1: 1,+region=us-east-2: 1,+region=us-west-1: 1}";` `us-east-1`に 1 人のFollower、 `us-east-2`に 1 人のFollower、 `us-west-1`に 1 人のFollowerを配置することを意味します。</li><li> `FOLLOWER_CONSTRAINTS='{"+region=us-east-1,+type=scale-node": 1,"+region=us-west-1": 1}';` `us-east-1`領域に位置し、 `type`ラベルが`scale-node`であるノードに 1 つのFollowerを配置し、 `us-west-1`に 1 つのFollowerを配置することを意味します。</li></ul>辞書形式では、 `+`または`-`で始まる各キーがサポートされており、特別な`#reject-leader`属性を構成できます。たとえば、 `FOLLOWER_CONSTRAINTS='{"+region=us-east-1":1, "+region=us-east-2": 2, "+region=us-west-1,#reject-leader": 1}'` 、 `us-west-1`で選出されたリーダーが災害復旧中に可能な限り立ち退かせることを意味します。 |

> **注記：**
>
> -   `LEADER_CONSTRAINTS`配置オプションはリスト形式のみをサポートします。
> -   リスト形式と辞書形式は両方とも YAML パーサーに基づいていますが、場合によっては YAML 構文が誤って解析される可能性があります。たとえば、 `"{+region=east:1,+region=west:2}"` ( `:`後にスペースなし) は、予期せぬ`'{"+region=east:1": null, "+region=west:2": null}'`として誤って解析される可能性があります。ただし、 `"{+region=east: 1,+region=west: 2}"` ( `:`の後のスペース) は`'{"+region=east": 1, "+region=west": 2}'`として正しく解析できます。したがって、 `:`の後にスペースを追加することをお勧めします。

## 基本的な例 {#basic-examples}

### クラスターのグローバルなレプリカの数を指定する {#specify-the-number-of-replicas-globally-for-a-cluster}

クラスターが初期化された後のデフォルトのレプリカ数は`3`です。クラスターにさらに多くのレプリカが必要な場合は、配置ポリシーを構成してこの数を増やし、 [`ALTER RANGE`](/sql-statements/sql-statement-alter-range.md)使用してクラスター レベルでポリシーを適用できます。例えば：

```sql
CREATE PLACEMENT POLICY five_replicas FOLLOWERS=4;
ALTER RANGE global PLACEMENT POLICY five_replicas;
```

TiDB のデフォルトのリーダー数は`1`であるため、 `five replicas` `4`人のフォロワーと`1`人のLeaderを意味することに注意してください。

### データベースのデフォルトの配置ポリシーを指定する {#specify-a-default-placement-policy-for-a-database}

データベースのデフォルトの配置ポリシーを指定できます。これは、データベースのデフォルトの文字セットまたは照合順序を設定するのと同様に機能します。データベース内のテーブルまたはパーティションに他の配置ポリシーが指定されていない場合は、データベースの配置ポリシーがテーブルとパーティションに適用されます。例えば：

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

テーブルからそのパーティションへのポリシー継承は、前の例のポリシー継承とは異なることに注意してください。テーブルのデフォルト ポリシーを変更すると、新しいポリシーはそのテーブル内のパーティションにも適用されます。ただし、テーブルがデータベースからポリシーを継承するのは、テーブルがポリシーを指定せずに作成された場合のみです。テーブルがデータベースからポリシーを継承すると、データベースのデフォルト ポリシーを変更しても、そのテーブルには適用されません。

### テーブルの配置ポリシーを指定する {#specify-a-placement-policy-for-a-table}

テーブルのデフォルトの配置ポリシーを指定できます。例えば：

```sql
CREATE PLACEMENT POLICY five_replicas FOLLOWERS=4;

CREATE TABLE t (a INT) PLACEMENT POLICY=five_replicas;  -- Creates a table t and attaches the 'five_replicas' placement policy to it.

ALTER TABLE t PLACEMENT POLICY=default; -- Removes the placement policy 'five_replicas' from the table t and resets the placement policy to the default one.
```

### パーティションテーブルの配置ポリシーを指定する {#specify-a-placement-policy-for-a-partitioned-table}

パーティションテーブルまたはパーティションの配置ポリシーを指定することもできます。例えば：

```sql
CREATE PLACEMENT POLICY storageforhisotrydata CONSTRAINTS="[+node=history]";
CREATE PLACEMENT POLICY storagefornewdata CONSTRAINTS="[+node=new]";
CREATE PLACEMENT POLICY companystandardpolicy CONSTRAINTS="";

CREATE TABLE t1 (id INT, name VARCHAR(50), purchased DATE)
PLACEMENT POLICY=companystandardpolicy
PARTITION BY RANGE( YEAR(purchased) ) (
  PARTITION p0 VALUES LESS THAN (2000) PLACEMENT POLICY=storageforhisotrydata,
  PARTITION p1 VALUES LESS THAN (2005),
  PARTITION p2 VALUES LESS THAN (2010),
  PARTITION p3 VALUES LESS THAN (2015),
  PARTITION p4 VALUES LESS THAN MAXVALUE PLACEMENT POLICY=storagefornewdata
);
```

テーブル内のパーティションに配置ポリシーが指定されていない場合、パーティションはテーブルからポリシー (存在する場合) を継承しようとします。前の例では次のようになります。

-   `p0`パーティションには`storageforhisotrydata`ポリシーが適用されます。
-   `p4`パーティションには`storagefornewdata`ポリシーが適用されます。
-   `p1` `p2`および`p3`パーティションには、テーブル`t1`から継承された`companystandardpolicy`配置ポリシーが適用されます。
-   テーブル`t1`に配置ポリシーが指定されていない場合、パーティション`p1` 、 `p2` 、および`p3`データベースのデフォルト ポリシーまたはグローバル デフォルト ポリシーを継承します。

これらのパーティションに配置ポリシーをアタッチした後、次の例のように、特定のパーティションの配置ポリシーを変更できます。

```sql
ALTER TABLE t1 PARTITION p1 PLACEMENT POLICY=storageforhisotrydata;
```

## 高可用性の例 {#high-availability-examples}

次のトポロジを持つクラスターがあり、TiKV ノードが 3 つのリージョンに分散されており、各リージョンに 3 つの使用可能なゾーンが含まれているとします。

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

### 生存環境の設定を指定する {#specify-survival-preferences}

正確なデータ分散には特に関心がなく、災害復旧要件を満たすことを優先する場合は、 `SURVIVAL_PREFERENCES`オプションを使用してデータ存続設定を指定できます。

前の例と同様に、TiDB クラスターは 3 つのリージョンに分散されており、各リージョンには 3 つのゾーンが含まれています。このクラスターの配置ポリシーを作成するときは、 `SURVIVAL_PREFERENCES`を次のように構成すると仮定します。

```sql
CREATE PLACEMENT POLICY multiaz SURVIVAL_PREFERENCES="[region, zone, host]";
CREATE PLACEMENT POLICY singleaz CONSTRAINTS="[+region=us-east-1]" SURVIVAL_PREFERENCES="[zone]";
```

配置ポリシーを作成した後、必要に応じて、それらを対応するテーブルにアタッチできます。

-   `multiaz`配置ポリシーがアタッチされたテーブルの場合、データは異なるリージョンの 3 つのレプリカに配置され、データ分離というリージョン間の生存目標を達成することが優先され、次にゾーン間の生存目標、最後にホスト間の生存目標が続きます。 。
-   `singleaz`配置ポリシーがアタッチされたテーブルの場合、データはまず`us-east-1`のリージョン内の 3 つのレプリカに配置され、その後、データ分離のクロスゾーン存続目標を達成します。

<CustomContent platform="tidb">

> **注記：**
>
> `SURVIVAL_PREFERENCES`は PD の`location-labels`に相当します。詳細については、 [トポロジ ラベルごとにレプリカをスケジュールする](/schedule-replicas-by-topology-labels.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> `SURVIVAL_PREFERENCES`は PD の`location-labels`に相当します。詳細については、 [トポロジ ラベルごとにレプリカをスケジュールする](https://docs.pingcap.com/tidb/stable/schedule-replicas-by-topology-labels)を参照してください。

</CustomContent>

### 複数のデータセンターに 2:2:1 で分散された 5 つのレプリカを持つクラスターを指定します {#specify-a-cluster-with-5-replicas-distributed-2-2-1-across-multiple-data-centers}

2:2:1 の比率で 5 レプリカの分散など、特定のデータ分散が必要な場合は、次の[辞書形式](#constraints-formats)の`CONSTRAINTS`を構成することで、さまざまな制約に応じて異なる数のレプリカを指定できます。

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

クラスターにグローバル`deploy221`配置ポリシーが設定されると、TiDB はこのポリシーに従ってデータを分散します。つまり、2 つのレプリカを`us-east-1`リージョンに、2 つのレプリカを`us-east-2`リージョンに、1 つのレプリカを`us-west-1`リージョンに配置します。

### リーダーとフォロワーの分布を指定する {#specify-the-distribution-of-leaders-and-followers}

制約または`PRIMARY_REGION`を使用して、リーダーとフォロワーの特定の分布を指定できます。

#### 制約を使用する {#use-constraints}

ノード間でRaft Leader を分散するための特定の要件がある場合は、次のステートメントを使用して配置ポリシーを指定できます。

```sql
CREATE PLACEMENT POLICY deploy221_primary_east1 LEADER_CONSTRAINTS="[+region=us-east-1]" FOLLOWER_CONSTRAINTS='{"+region=us-east-1": 1, "+region=us-east-2": 2, "+region=us-west-1: 1}';
```

この配置ポリシーが作成され、目的のデータにアタッチされた後、データのRaft Leaderレプリカは`LEADER_CONSTRAINTS`オプションで指定された`us-east-1`リージョンに配置され、データの他のレプリカは`FOLLOWER_CONSTRAINTS`オプションで指定されたリージョンに配置されます。 `us-east-1`リージョンでのノード停止など、クラスターに障害が発生した場合、他のリージョンが`FOLLOWER_CONSTRAINTS`で指定されている場合でも、新しいLeaderが他のリージョンから選出されることに注意してください。言い換えれば、サービスの可用性を確保することが最優先されます。

`us-east-1`リージョンで障害が発生した場合に、新しいリーダーを`us-west-1`に配置したくない場合は、特別な`reject-leader`属性を設定して、そのリージョンで新しく選出されたリーダーを排除できます。

```sql
CREATE PLACEMENT POLICY deploy221_primary_east1 LEADER_CONSTRAINTS="[+region=us-east-1]" FOLLOWER_CONSTRAINTS='{"+region=us-east-1": 1, "+region=us-east-2": 2, "+region=us-west-1,#reject-leader": 1}';
```

#### <code>PRIMARY_REGION</code>を使用する {#use-code-primary-region-code}

クラスター トポロジで`region`ラベルが構成されている場合は、 `PRIMARY_REGION`および`REGIONS`オプションを使用してフォロワーの配置ポリシーを指定することもできます。

```sql
CREATE PLACEMENT POLICY eastandwest PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-east-2,us-west-1" SCHEDULE="MAJORITY_IN_PRIMARY" FOLLOWERS=4;
CREATE TABLE t1 (a INT) PLACEMENT POLICY=eastandwest;
```

-   `PRIMARY_REGION`リーダーの配布地域を指定します。このオプションでは 1 つのリージョンのみを指定できます。
-   `SCHEDULE`オプションは、TiDB がフォロワーの分散のバランスをとる方法を指定します。
    -   デフォルトの`EVEN`スケジュール ルールにより、すべてのリージョンにわたってフォロワーがバランスよく分散されます。
    -   十分な数のFollowerレプリカが`PRIMARY_REGION` (つまり`us-east-1` ) に確実に配置されるようにする場合は、 `MAJORITY_IN_PRIMARY`スケジューリング ルールを使用できます。このスケジューリング ルールは、可用性をある程度犠牲にして、トランザクションのレイテンシーを短縮します。プライマリ リージョンに障害が発生した場合、 `MAJORITY_IN_PRIMARY`は自動フェールオーバーを提供しません。

## データ分離の例 {#data-isolation-examples}

次の例のように、配置ポ​​リシーを作成するときに、ポリシーごとに制約を構成できます。これにより、指定された`app`ラベルを持つ TiKV ノードにデータが配置される必要があります。

```sql
CREATE PLACEMENT POLICY app_order CONSTRAINTS="[+app=order]";
CREATE PLACEMENT POLICY app_list CONSTRAINTS="[+app=list_collection]";
CREATE TABLE order (id INT, name VARCHAR(50), purchased DATE)
PLACEMENT POLICY=app_order
CREATE TABLE list (id INT, name VARCHAR(50), purchased DATE)
PLACEMENT POLICY=app_list
```

この例では、制約は`[+app=order]`などのリスト形式を使用して指定されます。 `{+app=order: 3}`などの辞書形式を使用して指定することもできます。

例のステートメントを実行した後、TiDB は`app_order`データを`app`ラベルを持つ TiKV ノードに`order`として配置し、 `app_list`データを`app`ラベルを持つ TiKV ノードに`list_collection`として配置します。これにより、storage内の物理データの分離が実現されます。

## 互換性 {#compatibility}

## 他の機能との互換性 {#compatibility-with-other-features}

-   一時テーブルは配置ポリシーをサポートしません。
-   配置ポリシーは、保存データが正しい TiKV ノード上に存在することを保証するだけであり、転送中のデータ (ユーザー クエリまたは内部操作のいずれかを介して) が特定のリージョンでのみ発生することを保証するものではありません。
-   データのTiFlashレプリカを構成するには、配置ポリシーを使用するのではなく、 [TiFlashレプリカを作成する](/tiflash/create-tiflash-replicas.md)を行う必要があります。
-   設定`PRIMARY_REGION`および`REGIONS`では、糖衣構文ルールが許可されます。将来的には、 `PRIMARY_RACK` 、 `PRIMARY_ZONE` 、 `PRIMARY_HOST`の品種も追加する予定です。 [問題 #18030](https://github.com/pingcap/tidb/issues/18030)を参照してください。

## ツールとの互換性 {#compatibility-with-tools}

<CustomContent platform="tidb">

| ツール名           | サポートされる最小バージョン | 説明                                                                                                                                                                                                  |
| -------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| バックアップと復元 (BR) | 6.0            | v6.0 より前のBR は、配置ポリシーのバックアップと復元をサポートしていません。詳細については、 [配置ルールをクラスターに復元するとエラーが発生するのはなぜですか](/faq/backup-and-restore-faq.md#why-does-an-error-occur-when-i-restore-placement-rules-to-a-cluster)を参照してください。 |
| TiDB Lightning | まだ互換性がありません    | TiDB Lightning が配置ポリシーを含むバックアップ データをインポートするとエラーが報告される                                                                                                                                               |
| TiCDC          | 6.0            | 配置ポリシーを無視し、ポリシーをダウンストリームに複製しません。                                                                                                                                                                    |
| TiDBBinlog     | 6.0            | 配置ポリシーを無視し、ポリシーをダウンストリームに複製しません。                                                                                                                                                                    |

</CustomContent>

<CustomContent platform="tidb-cloud">

| ツール名           | サポートされる最小バージョン | 説明                                                    |
| -------------- | -------------- | ----------------------------------------------------- |
| TiDB Lightning | まだ互換性がありません    | TiDB Lightning が配置ポリシーを含むバックアップ データをインポートするとエラーが報告される |
| TiCDC          | 6.0            | 配置ポリシーを無視し、ポリシーをダウンストリームに複製しません。                      |

</CustomContent>
