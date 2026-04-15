---
title: Placement Rules in SQL
summary: SQL文を使用してテーブルとパーティションの配置をスケジュールする方法を学びましょう。
---

# SQLにおける配置ルール {#placement-rules-in-sql}

SQLの配置ルールは、SQL文を使用してTiKVクラスタ内のデータの保存場所を指定できる機能です。この機能を使用すると、クラスタ、データベース、テーブル、またはパーティションのデータを、特定のリージョン、データセンター、ラック、またはホストにスケジュールできます。

この機能は、以下のユースケースに対応できます。

-   複数のデータセンターにデータをデプロイ、高可用性戦略を最適化するためのルールを設定します。
-   異なるアプリケーションの複数のデータベースを統合し、異なるユーザーのデータを物理的に分離することで、インスタンス内の異なるユーザーの分離要件を満たします。
-   アプリケーションの可用性とデータの信頼性を向上させるため、重要なデータのレプリカ数を増やしてください。

> **注記：**
>
> この機能は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスではご利用いただけません。

## 概要 {#overview}

SQL の配置ルール機能を使用すると、配置ポリシー[配置ポリシーを作成する](#create-and-attach-placement-policies)、次のように粗いものから細かいものまで、さまざまなレベルでデータに必要な配置ポリシーを構成できます。

| レベル     | 説明                                                                                                                                                                        |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| クラスタ    | デフォルトでは、TiDB はクラスターに対して 3 つのレプリカのポリシーを構成します。クラスターのグローバル配置ポリシーを構成できます。詳細については、 [クラスターのレプリカ数をグローバルに指定します。](#specify-the-number-of-replicas-globally-for-a-cluster)参照してください。 |
| データベース  | 特定のデータベースの配置ポリシーを構成できます。詳細については、 [データベースのデフォルトの配置ポリシーを指定します。](#specify-a-default-placement-policy-for-a-database)参照してください。                                                |
| テーブル    | 特定のテーブルの配置ポリシーを構成できます。詳細については、[テーブルの配置ポリシーを指定します。](#specify-a-placement-policy-for-a-table)参照してください。                                                                      |
| パーティション | テーブル内のさまざまな行にパーティションを作成し、パーティションの配置ポリシーを個別に構成できます。詳細については、 [パーティションテーブルの配置ポリシーを指定します。](#specify-a-placement-policy-for-a-partitioned-table)参照してください。                      |

> **ヒント：**
>
> *SQL における配置ルール*の実装は、PD の*配置ルール機能*に依存しています。詳細については、 [配置ルールを設定する](https://docs.pingcap.com/tidb/stable/configure-placement-rules)を参照してください。SQL における配置ルールのコンテキストでは、*配置ルール*とは、他のオブジェクトに添付された*配置ポリシー*、または TiDB から PD に送信されるルールを指す場合があります。

## 制限事項 {#limitations}

-   メンテナンスを簡素化するため、クラスター内の配置ポリシーの数を10以下に制限することをお勧めします。
-   配置ポリシーを適用するテーブルとパーティションの総数は、10,000以下に制限することをお勧めします。ポリシーを適用するテーブルやパーティションが多すぎると、PD（配置データベース）の計算負荷が増加し、サービスパフォーマンスに影響を与える可能性があります。
-   複雑な配置ポリシーを使用するよりも、本書に記載されている例に従ってSQLの配置ルール機能を使用することをお勧めします。

## 前提条件 {#prerequisites}

配置ポリシーは、TiKVノード上のラベルの設定に依存します。たとえば、 `PRIMARY_REGION`配置オプションは、TiKV内の`region`ラベルに依存します。

<CustomContent platform="tidb">

配置ポリシーを作成する際、TiDB はポリシーで指定されたラベルが存在するかどうかをチェックしません。代わりに、TiDB はポリシーをアタッチする際にチェックを実行します。したがって、配置ポリシーをアタッチする前に、各 TiKV ノードに正しいラベルが設定されていることを確認してください。TiDB セルフマネージド クラスタの構成方法は以下のとおりです。

    tikv-server --labels region=<region>,zone=<zone>,host=<host>

詳細な設定方法については、以下の例を参照してください。

| 展開方法                      | 例                                                                                                                                 |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| 手動展開                      | [トポロジーラベルに基づいてレプリカをスケジュールする](/schedule-replicas-by-topology-labels.md)                                                            |
| TiUPを使用した展開               | [地理的に分散した展開トポロジー](/geo-distributed-deployment-topology.md)                                                                        |
| TiDB Operatorを使用したデプロイメント | [KubernetesでTiDBクラスタを構成する](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-a-tidb-cluster#high-availability-of-data) |

> **注記：**
>
> TiDB Cloud Dedicatedクラスターの場合、 TiDB Cloud Dedicatedクラスター内の TiKV ノードのラベルは自動的に構成されるため、これらのラベル構成手順はスキップできます。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB Cloud Dedicatedクラスターの場合、TiKV ノード上のラベルは自動的に構成されます。

</CustomContent>

現在の TiKV クラスターで使用可能なすべてのラベルを表示するには、 [`SHOW PLACEMENT LABELS`](/sql-statements/sql-statement-show-placement-labels.md)ステートメントを使用できます。

```sql
SHOW PLACEMENT LABELS;
+--------+----------------------------+
| Key    | Values                     |
+--------+----------------------------+
| disk   | ["ssd"]                    |
| region | ["us-east-1", "us-west-1"] |
| zone   | ["us-east-1a"]             |
+--------+----------------------------+
3 rows in set (0.00 sec)
```

## 使用法 {#usage}

このセクションでは、SQL文を使用して配置ポリシーを作成、添付、表示、変更、および削除する方法について説明します。

### 配置ポリシーを作成して添付する {#create-and-attach-placement-policies}

1.  配置ポリシーを作成するには、 [`CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-create-placement-policy.md)ステートメントを使用します。

    ```sql
    CREATE PLACEMENT POLICY myplacementpolicy PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1";
    ```

    この声明では、

    -   `PRIMARY_REGION="us-east-1"`オプションは、 `region`ラベルのノードに`us-east-1`としてRaftリーダーを配置することを意味します。
    -   `REGIONS="us-east-1,us-west-1"`オプションは、 `region` - `us-east-1`として、 `region`ラベルのノードに`us-west-1`として Raft Followers を配置することを意味します。

    構成可能な配置オプションとその意味の詳細については、「[配置オプション](#placement-option-reference)参照してください。

2.  テーブルまたはパーティションテーブルに配置ポリシーを適用するには、 `CREATE TABLE`または`ALTER TABLE`ステートメントを使用して、そのテーブルまたはパーティションテーブルの配置ポリシーを指定します。

    ```sql
    CREATE TABLE t1 (a INT) PLACEMENT POLICY=myplacementpolicy;
    CREATE TABLE t2 (a INT);
    ALTER TABLE t2 PLACEMENT POLICY=myplacementpolicy;
    ```

    `PLACEMENT POLICY`どのデータベース スキーマにも関連付けられておらず、グローバル スコープに添付できます。したがって、 `CREATE TABLE`を使用して配置ポリシーを指定する場合、追加の権限は必要ありません。

### 配置ポリシーをビュー {#view-placement-policies}

-   既存の配置ポリシーを表示するには、 [`SHOW CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-show-create-placement-policy.md)ステートメントを使用できます。

    ```sql
    SHOW CREATE PLACEMENT POLICY myplacementpolicy\G
    *************************** 1. row ***************************
           Policy: myplacementpolicy
    Create Policy: CREATE PLACEMENT POLICY myplacementpolicy PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1"
    1 row in set (0.00 sec)
    ```

-   特定のテーブルに紐づけられた配置ポリシーを表示するには、 [`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md)ステートメントを使用できます。

    ```sql
    SHOW CREATE TABLE t1\G
    *************************** 1. row ***************************
           Table: t1
    Create Table: CREATE TABLE `t1` (
      `a` int DEFAULT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin /*T![placement] PLACEMENT POLICY=`myplacementpolicy` */
    1 row in set (0.00 sec)
    ```

-   クラスタ内の配置ポリシーの定義を表示するには、 [`INFORMATION_SCHEMA.PLACEMENT_POLICIES`](/information-schema/information-schema-placement-policies.md)システム テーブルをクエリします。

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

-   クラスタ内の配置ポリシーに関連付けられているすべてのテーブルを表示するには、 `tidb_placement_policy_name`システムテーブルの`information_schema.tables`列をクエリします。

    ```sql
    SELECT * FROM information_schema.tables WHERE tidb_placement_policy_name IS NOT NULL;
    ```

-   クラスタ内の配置ポリシーが関連付けられているすべてのパーティションを表示するには、 `tidb_placement_policy_name`システムテーブルの`information_schema.partitions`列をクエリします。

    ```sql
    SELECT * FROM information_schema.partitions WHERE tidb_placement_policy_name IS NOT NULL;
    ```

-   すべてのオブジェクトに適用される配置ポリシーは*非同期的に*適用されます。配置ポリシーのスケジューリングの進行状況を確認するには、 [`SHOW PLACEMENT`](/sql-statements/sql-statement-show-placement.md)ステートメントを使用できます。

    ```sql
    SHOW PLACEMENT;
    ```

### 配置ポリシーを変更する {#modify-placement-policies}

配置ポリシーを変更するには、 [`ALTER PLACEMENT POLICY`](/sql-statements/sql-statement-alter-placement-policy.md)ステートメントを使用します。変更内容は、該当するポリシーが関連付けられているすべてのオブジェクトに適用されます。

```sql
ALTER PLACEMENT POLICY myplacementpolicy FOLLOWERS=4;
```

このステートメントでは、 `FOLLOWERS=4`オプションは、データに対して 4 つの Followers と 1 Leaderを含む 5 つのレプリカを構成することを意味します。構成可能な配置オプションとその意味の詳細については、[配置オプションの参考](#placement-option-reference)参照してください。

### ドロップ配置ポリシー {#drop-placement-policies}

どのテーブルまたはパーティションにも関連付けられていないポリシーを削除するには、 [`DROP PLACEMENT POLICY`](/sql-statements/sql-statement-drop-placement-policy.md)ステートメントを使用できます。

```sql
DROP PLACEMENT POLICY myplacementpolicy;
```

## 配置オプションの参考 {#placement-option-reference}

配置ポリシーを作成または変更する際には、必要に応じて配置オプションを設定できます。

> **注記：**
>
> `PRIMARY_REGION` 、 `REGIONS` 、および`SCHEDULE`オプションは、 `CONSTRAINTS`オプションと同時に指定することはできません。同時に指定するとエラーが発生します。

### 通常の配置オプション {#regular-placement-options}

通常の配置オプションは、データ配置の基本的な要件を満たすことができます。

| オプション名           | 説明                                                                               |
| ---------------- | -------------------------------------------------------------------------------- |
| `PRIMARY_REGION` | このオプションの値と一致する`region`ラベルを持つノードにRaftリーダーを配置することを指定します。                           |
| `REGIONS`        | このオプションの値と一致する`region`ラベルを持つノードにRaft Followers を配置することを指定します。                    |
| `SCHEDULE`       | フォロワーの配置スケジュール戦略を指定します。値のオプションは`EVEN` (デフォルト) または`MAJORITY_IN_PRIMARY`です。        |
| `FOLLOWERS`      | フォロワーの数を指定します。たとえば、 `FOLLOWERS=2`データのレプリカが 3 つ（フォロワー 2 つとLeader1 つ）存在することを意味します。 |

### 高度な配置オプション {#advanced-placement-options}

高度な構成オプションを使用すると、複雑なシナリオの要件を満たすために、データの配置に関してより柔軟な設定が可能になります。ただし、高度なオプションの設定は通常のオプションよりも複雑であり、クラスタトポロジーとTiDBのデータシャーディングに関する深い理解が必要です。

| オプション名                 | 説明                                                                           |
| ---------------------- | ---------------------------------------------------------------------------- |
| `CONSTRAINTS`          | すべての役割に適用される制約のリスト。例: `CONSTRAINTS="[+disk=ssd]"` 。                          |
| `LEADER_CONSTRAINTS`   | Leaderにのみ適用される制約のリスト。                                                        |
| `FOLLOWER_CONSTRAINTS` | フォロワーにのみ適用される制約事項のリスト。                                                       |
| `LEARNER_CONSTRAINTS`  | 学習者のみに適用される制約事項のリスト。                                                         |
| `LEARNERS`             | 学習者の数。                                                                       |
| `SURVIVAL_PREFERENCE`  | ラベルの災害耐性レベルに応じたレプリカ配置の優先順位。例： `SURVIVAL_PREFERENCE="[region, zone, host]"` 。 |

### 制約形式 {#constraints-formats}

`CONSTRAINTS` 、 `FOLLOWER_CONSTRAINTS` 、および`LEARNER_CONSTRAINTS`配置オプションは、以下のいずれかの形式で設定できます。

| 制約形式  | 説明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| リスト形式 | 指定する制約がすべてのレプリカに適用される場合は、キーと値のリスト形式を使用できます。各キーは`+`または`-`で始まります。例:<br/><ul><li> `[+region=us-east-1]`は、 `region`ラベルを持つノードに`us-east-1`としてデータを配置することを意味します。</li><li> `[+region=us-east-1,-type=fault]`は、 `region`という`us-east-1`ラベルを持つノードにデータを配置することを意味しますが、 `type`という`fault`ラベルは持っていません。</li></ul><br/>                                                                                                                                                                                                                                                                                                                                                                                     |
| 辞書形式  | 異なる制約に対して異なるレプリカ数を指定する必要がある場合は、辞書形式を使用できます。例：<br/><ul><li> `FOLLOWER_CONSTRAINTS="{+region=us-east-1: 1,+region=us-east-2: 1,+region=us-west-1: 1}";`は、 `us-east-1`にFollowerを 1 つ、 `us-east-2`にFollowerを1 つ、 `us-west-1`にフォロワーを 1 つFollower。</li><li> `FOLLOWER_CONSTRAINTS='{"+region=us-east-1,+type=scale-node": 1,"+region=us-west-1": 1}';`は、 `us-east-1` `type` } `scale-node`あるノードに 1 つのフォロワーを配置し、 `us-west-1`に 1 つのFollowerを意味します。</li></ul>辞書形式は`+`または`-`で始まる各キーをサポートし、特別な`#evict-leader`属性を設定できます。たとえば、 `FOLLOWER_CONSTRAINTS='{"+region=us-east-1":1, "+region=us-east-2": 2, "+region=us-west-1,#evict-leader": 1}'`は、 `us-west-1`で選出されたリーダーが、ディザスタリカバリ中に可能な限り排除されることを意味します。 |

> **注記：**
>
> -   `LEADER_CONSTRAINTS`配置オプションはリスト形式のみをサポートしています。
> -   リスト形式と辞書形式はどちらも YAML パーサーに基づいていますが、YAML 構文は場合によっては正しく解析されないことがあります。たとえば、 `"{+region=east:1,+region=west:2}"` ( `:`の後にスペースがない場合) は、 `'{"+region=east:1": null, "+region=west:2": null}'`と誤って解析される可能性があり、これは予期しない結果です。しかし、 `"{+region=east: 1,+region=west: 2}"` `:`の後にスペースがある場合) `'{"+region=east": 1, "+region=west": 2}'`と正しく解析されます。したがって、 `:`の後にスペースを追加することをお勧めします。

## 基本的な例 {#basic-examples}

### クラスターのレプリカ数をグローバルに指定します。 {#specify-the-number-of-replicas-globally-for-a-cluster}

クラスターが初期化されると、デフォルトのレプリカ数は`3`になります。クラスターでより多くのレプリカが必要な場合は、配置ポリシーを構成してこの数を増やし、 [`ALTER RANGE`](/sql-statements/sql-statement-alter-range.md)を使用してクラスターレベルでポリシーを適用できます。例:

```sql
CREATE PLACEMENT POLICY five_replicas FOLLOWERS=4;
ALTER RANGE global PLACEMENT POLICY five_replicas;
```

TiDB ではリーダーの数がデフォルトで`1`に設定されているため、 `five replicas`は`4`フォロワーと`1`のLeader。

### データベースのデフォルトの配置ポリシーを指定します。 {#specify-a-default-placement-policy-for-a-database}

データベースのデフォルトの配置ポリシーを指定できます。これは、データベースのデフォルトの文字セットや照合順序を設定するのと同様に機能します。データベース内のテーブルまたはパーティションに他の配置ポリシーが指定されていない場合、データベースの配置ポリシーがテーブルとパーティションに適用されます。例:

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

テーブルからパーティションへのポリシー継承は、前述の例とは異なる点に注意してください。テーブルのデフォルトポリシーを変更すると、新しいポリシーはそのテーブル内のパーティションにも適用されます。ただし、テーブルがデータベースからポリシーを継承するのは、ポリシーを指定せずに作成された場合のみです。テーブルがデータベースからポリシーを継承すると、データベースのデフォルトポリシーを変更しても、そのテーブルには適用されません。

### テーブルの配置ポリシーを指定します。 {#specify-a-placement-policy-for-a-table}

テーブルのデフォルトの配置ポリシーを指定できます。例：

```sql
CREATE PLACEMENT POLICY five_replicas FOLLOWERS=4;

CREATE TABLE t (a INT) PLACEMENT POLICY=five_replicas;  -- Creates a table t and attaches the 'five_replicas' placement policy to it.

ALTER TABLE t PLACEMENT POLICY=default; -- Removes the placement policy 'five_replicas' from the table t and resets the placement policy to the default one.
```

### パーティションテーブルの配置ポリシーを指定します。 {#specify-a-placement-policy-for-a-partitioned-table}

パーティションテーブルまたはパーティションに対して、配置ポリシーを指定することもできます。例：

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

テーブル内のパーティションに配置ポリシーが指定されていない場合、パーティションはテーブルからポリシー（存在する場合）を継承しようとします。テーブルに[グローバルインデックス](/global-indexes.md)がある場合、インデックスはテーブルと同じ配置ポリシーを適用します。上記の例では、次のようになります。

-   `p0`パーティションには`storageforhistorydata`ポリシーが適用されます。
-   `p4`パーティションには`storagefornewdata`ポリシーが適用されます。
-   `p1` 、 `p2` 、および`p3`パーティションは、テーブル`companystandardpolicy`から継承された`t1`ポリシーを適用します。
-   グローバルインデックス`idx`は、テーブル`companystandardpolicy`と同じ`t1`配置ポリシーを適用します。
-   テーブル`t1`に対して配置ポリシーが指定されていない場合、 `p1` 、 `p2` 、 `p3`パーティションとグローバルインデックス`idx`データベースのデフォルトポリシーまたはグローバルのデフォルトポリシーを継承します。

これらのパーティションに配置ポリシーを適用した後、次の例のように、特定のパーティションの配置ポリシーを変更できます。

```sql
ALTER TABLE t1 PARTITION p1 PLACEMENT POLICY=storageforhistorydata;
```

## 高可用性の例 {#high-availability-examples}

TiKVノードが3つの領域に分散され、各領域に3つの利用可能なゾーンが含まれる、以下のトポロジーを持つクラスターが存在すると仮定します。

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

### 生存に関する希望条件を指定してください {#specify-survival-preferences}

データの正確な分散方法には特にこだわらず、ディザスタリカバリ要件を満たすことを優先する場合は、 `SURVIVAL_PREFERENCES`オプションを使用して、データの生存に関する設定を指定できます。

前述の例と同様に、TiDB クラスタは 3 つのリージョンに分散され、各リージョンには 3 つのゾーンが含まれています。このクラスタの配置ポリシーを作成する場合、 `SURVIVAL_PREFERENCES`を次のように構成することを想定します。

```sql
CREATE PLACEMENT POLICY multiaz SURVIVAL_PREFERENCES="[region, zone, host]";
CREATE PLACEMENT POLICY singleaz CONSTRAINTS="[+region=us-east-1]" SURVIVAL_PREFERENCES="[zone]";
```

配置ポリシーを作成した後、必要に応じて対応するテーブルにそれらを添付できます。

-   `multiaz`配置ポリシーが添付されたテーブルの場合、データは異なるリージョンの3つのレプリカに配置され、データの分離というリージョン間生存目標を満たすことが最優先され、次にゾーン間生存目標、最後にホスト間生存目標が優先されます。
-   `singleaz`配置ポリシーが添付されたテーブルの場合、データはまず`us-east-1`リージョンの3つのレプリカに配置され、その後、データ分離のゾーン間生存目標を満たします。

<CustomContent platform="tidb">

> **注記：**
>
> `SURVIVAL_PREFERENCES` PD の`location-labels`と同等です。詳細については、[トポロジーラベルによるレプリカのスケジュール設定](/schedule-replicas-by-topology-labels.md)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> `SURVIVAL_PREFERENCES` PD の`location-labels`と同等です。詳細については、 [トポロジーラベルによるレプリカのスケジュール設定](https://docs.pingcap.com/tidb/stable/schedule-replicas-by-topology-labels)参照してください。

</CustomContent>

### 複数のデータセンターに2:2:1の比率で分散された5つのレプリカを持つクラスターを指定します。 {#specify-a-cluster-with-5-replicas-distributed-2-2-1-across-multiple-data-centers}

2:2:1の比率で5つのレプリカを配布するなど、特定のデータ分布が必要な場合は、これらの`CONSTRAINTS`[辞書形式](#constraints-formats)で構成することにより、異なる制約に対して異なるレプリカ数を指定できます。

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

クラスターに対してグローバルな`deploy221`配置ポリシーが設定されると、TiDBはこのポリシーに従ってデータを分散します。 `us-east-1`領域に2つのレプリカ、 `us-east-2`領域に2つのレプリカ、 `us-west-1`領域に1つのレプリカを配置します。

### リーダーとフォロワーの分布を指定します {#specify-the-distribution-of-leaders-and-followers}

制約または`PRIMARY_REGION`を使用して、リーダーとフォロワーの特定の分布を指定できます。

#### 制約を使用する {#use-constraints}

ノード間でのRaftリーダーの配置に関して特定の要件がある場合は、次のステートメントを使用して配置ポリシーを指定できます。

```sql
CREATE PLACEMENT POLICY deploy221_primary_east1 LEADER_CONSTRAINTS="[+region=us-east-1]" FOLLOWER_CONSTRAINTS='{"+region=us-east-1": 1, "+region=us-east-2": 2, "+region=us-west-1": 1}';
```

この配置ポリシーが作成され、目的のデータに適用されると、データのRaftLeaderレプリカは`us-east-1`オプションで指定された`LEADER_CONSTRAINTS`リージョンに配置され、その他のデータのレプリカは`FOLLOWER_CONSTRAINTS`オプションで指定されたリージョンに配置されます。クラスターが障害を起こした場合（たとえば、 `us-east-1`リージョンでノードが停止した場合など）、これらのリージョン`FOLLOWER_CONSTRAINTS`で指定されていても、他のリージョンから新しいLeaderが選出されることに注意してください。つまり、サービスの可用性を確保することが最優先事項となります。

`us-east-1`領域で障害が発生した場合、 `us-west-1`に新しいリーダーを配置したくない場合は、特別な`evict-leader`属性を設定して、その領域で新たに選出されたリーダーを排除することができます。

```sql
CREATE PLACEMENT POLICY deploy221_primary_east1 LEADER_CONSTRAINTS="[+region=us-east-1]" FOLLOWER_CONSTRAINTS='{"+region=us-east-1": 1, "+region=us-east-2": 2, "+region=us-west-1,#evict-leader": 1}';
```

#### <code>PRIMARY_REGION</code>を使用する {#use-code-primary-region-code}

クラスタトポロジに`region`ラベルが設定されている場合、 `PRIMARY_REGION`および`REGIONS`オプションを使用して、フォロワーの配置ポリシーを指定することもできます。

```sql
CREATE PLACEMENT POLICY eastandwest PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-east-2,us-west-1" SCHEDULE="MAJORITY_IN_PRIMARY" FOLLOWERS=4;
CREATE TABLE t1 (a INT) PLACEMENT POLICY=eastandwest;
```

-   `PRIMARY_REGION`リーダーの配布地域を指定します。このオプションでは、1 つの地域のみを指定できます。
-   `SCHEDULE`オプションは、TiDB がフォロワーの分布をどのようにバランスさせるかを指定します。
    -   デフォルトの`EVEN`スケジューリングルールは、すべてのリージョンにわたってフォロワーが均等に分散されることを保証します。
    -   `PRIMARY_REGION` (つまり`us-east-1` ) に十分な数のFollowerレプリカを配置したい場合は、 `MAJORITY_IN_PRIMARY`スケジューリングルールを使用できます。このスケジューリングルールは、可用性を多少犠牲にする代わりに、トランザクションのレイテンシーを低減します。プライマリリージョンが障害を起こした場合、 `MAJORITY_IN_PRIMARY`自動フェイルオーバーを提供しません。

## データ分離の例 {#data-isolation-examples}

次の例のように、配置ポ​​リシーを作成する際に、各ポリシーに対して制約を設定できます。この制約では、指定された`app`ラベルを持つ TiKV ノードにデータを配置する必要があります。

```sql
CREATE PLACEMENT POLICY app_order CONSTRAINTS="[+app=order]";
CREATE PLACEMENT POLICY app_list CONSTRAINTS="[+app=list_collection]";
CREATE TABLE order (id INT, name VARCHAR(50), purchased DATE)
PLACEMENT POLICY=app_order
CREATE TABLE list (id INT, name VARCHAR(50), purchased DATE)
PLACEMENT POLICY=app_list
```

この例では、制約は`[+app=order]`のようなリスト形式で指定されています。また、 `{+app=order: 3}`のような辞書形式で指定することもできます。

例のステートメントを実行すると、TiDB は`app_order`データを`app`ラベルの TiKV ノードに`order`として配置し、 `app_list`データを`app`ラベルの TiKV ノードに`list_collection`として配置し、storage内の物理的なデータ分離を実現します。

## 互換性 {#compatibility}

## 他の機能との互換性 {#compatibility-with-other-features}

-   一時テーブルは配置ポリシーをサポートしていません。
-   配置ポリシーは、保存されているデータが正しい TiKV ノードに存在することを保証するだけであり、転送中のデータ (ユーザーからのクエリまたは内部操作によるもの) が特定のリージョンでのみ発生することを保証するものではありません。
-   データのTiFlashレプリカを構成するには、配置ポリシーを使用するのではなく、 [TiFlashのレプリカを作成する](/tiflash/create-tiflash-replicas.md)必要があります。
-   `PRIMARY_REGION`および`REGIONS`の設定には、構文糖衣ルールが許可されています。今後は、 `PRIMARY_RACK` 、 `PRIMARY_ZONE` 、および`PRIMARY_HOST`のバリエーションを追加する予定です。 [問題番号18030](https://github.com/pingcap/tidb/issues/18030)を参照してください。

## ツールとの互換性 {#compatibility-with-tools}

<CustomContent platform="tidb">

| ツール名           | サポートされている最小バージョン | 説明                                                                                                                                                                                                  |
| -------------- | ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| バックアップと復元 (BR) | 6.0              | v6.0 より前のBR は、配置ポリシーのバックアップと復元をサポートしていません。詳細については、 [クラスターに配置ルールを復元するとエラーが発生するのはなぜですか？](/faq/backup-and-restore-faq.md#why-does-an-error-occur-when-i-restore-placement-rules-to-a-cluster)参照してください。 |
| TiDB Lightning | まだ互換性がありません      | TiDB Lightningが配置ポリシーを含むバックアップデータをインポートする際にエラーが報告される                                                                                                                                                |
| TiCDC          | 6.0              | 配置ポリシーを無視し、下流にポリシーを複製しません。                                                                                                                                                                          |

</CustomContent>

<CustomContent platform="tidb-cloud">

| ツール名           | サポートされている最小バージョン | 説明                                                   |
| -------------- | ---------------- | ---------------------------------------------------- |
| TiDB Lightning | まだ互換性がありません      | TiDB Lightningが配置ポリシーを含むバックアップデータをインポートする際にエラーが報告される |
| TiCDC          | 6.0              | 配置ポリシーを無視し、下流にポリシーを複製しません。                           |

</CustomContent>
