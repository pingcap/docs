---
title: Placement Rules in SQL
summary: Learn how to schedule placement of tables and partitions using SQL statements.
---

# SQL の配置ルール {#placement-rules-in-sql}

SQL の配置ルールは、SQL インターフェイスを使用して TiKV クラスター内のデータの保存場所を指定できる機能です。この機能を使用すると、テーブルとパーティションが特定の領域、データセンター、ラック、またはホストにスケジュールされます。これは、低コストで高可用性戦略を最適化すること、データのローカル レプリカをローカルの古い読み取りに確実に利用できるようにすること、データの局所性要件を順守することなどのシナリオに役立ちます。

> **注記：**
>
> -   この機能は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターでは使用できません。
> -   *SQL での配置ルール*の実装は、PD の*配置ルール機能*に依存します。詳細は[配置ルールの構成](https://docs.pingcap.com/zh/tidb/stable/configure-placement-rules)を参照してください。 SQL の配置ルールのコンテキストでは、*配置ルールは*、他のオブジェクトに付加された*配置ポリシー*、または TiDB から PD に送信されるルールを指す場合があります。

詳細なユーザー シナリオは次のとおりです。

-   異なるアプリケーションの複数のデータベースをマージして、データベースの保守コストを削減します。
-   重要なデータのレプリカ数を増やして、アプリケーションの可用性とデータの信頼性を向上させます。
-   新しいデータをNVMestorageに保存し、古いデータをSSDに保存して、データのアーカイブとstorageのコストを削減します。
-   ホットスポット データのリーダーを高性能 TiKV インスタンスにスケジュールする
-   コールド データを低コストのstorageメディアに分離して、コスト効率を向上させます。
-   異なるユーザー間でのコンピューティング リソースの物理的な分離をサポートします。これにより、クラスター内の異なるユーザーの分離要件と、CPU、I/O、メモリ、および異なる混合負荷を持つその他のリソースの分離要件が満たされます。

## 配置ルールを指定する {#specify-placement-rules}

配置ルールを指定するには、まず[`CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-create-placement-policy.md)を使用して配置ポリシーを作成します。

```sql
CREATE PLACEMENT POLICY myplacementpolicy PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1";
```

次に、 `CREATE TABLE`または`ALTER TABLE`を使用して、ポリシーをテーブルまたはパーティションにアタッチします。次に、テーブルまたはパーティションに配置ルールを指定します。

```sql
CREATE TABLE t1 (a INT) PLACEMENT POLICY=myplacementpolicy;
CREATE TABLE t2 (a INT);
ALTER TABLE t2 PLACEMENT POLICY=myplacementpolicy;
```

配置ポリシーはデータベース スキーマに関連付けられておらず、グローバル スコープを持ちます。したがって、配置ポリシーを割り当てるには、 `CREATE TABLE`権限を超える追加の権限は必要ありません。

配置ポリシーを変更するには、 [`ALTER PLACEMENT POLICY`](/sql-statements/sql-statement-alter-placement-policy.md)を使用できます。変更は、対応するポリシーが割り当てられているすべてのオブジェクトに反映されます。

```sql
ALTER PLACEMENT POLICY myplacementpolicy FOLLOWERS=5;
```

どのテーブルまたはパーティションにもアタッチされていないポリシーを削除するには、 [`DROP PLACEMENT POLICY`](/sql-statements/sql-statement-drop-placement-policy.md)使用できます。

```sql
DROP PLACEMENT POLICY myplacementpolicy;
```

## 現在の配置ルールをビュー {#view-current-placement-rules}

テーブルに配置ルールがアタッチされている場合は、 [`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md)の出力で配置ルールを確認できます。利用可能なポリシーの定義を表示するには、 [`SHOW CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-show-create-placement-policy.md)を実行します。

```sql
tidb> SHOW CREATE TABLE t1\G
*************************** 1. row ***************************
       Table: t1
Create Table: CREATE TABLE `t1` (
  `a` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin /*T![placement] PLACEMENT POLICY=`myplacementpolicy` */
1 row in set (0.00 sec)

tidb> SHOW CREATE PLACEMENT POLICY myplacementpolicy\G
*************************** 1. row ***************************
       Policy: myplacementpolicy
Create Policy: CREATE PLACEMENT POLICY myplacementpolicy PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1"
1 row in set (0.00 sec)
```

[`INFORMATION_SCHEMA.PLACEMENT_POLICIES`](/information-schema/information-schema-placement-policies.md)テーブルを使用して、配置ポリシーの定義を表示することもできます。

```sql
tidb> select * from information_schema.placement_policies\G
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

`information_schema.tables`と`information_schema.partitions`テーブルには`tidb_placement_policy_name`の列も含まれており、配置ルールが適用されたすべてのオブジェクトが表示されます。

```sql
SELECT * FROM information_schema.tables WHERE tidb_placement_policy_name IS NOT NULL;
SELECT * FROM information_schema.partitions WHERE tidb_placement_policy_name IS NOT NULL;
```

オブジェクトに付加されたルールは*非同期的に*適用されます。現在の配置のスケジュールの進行状況を表示するには、 [`SHOW PLACEMENT`](/sql-statements/sql-statement-show-placement.md)を使用します。

## オプションリファレンス {#option-reference}

> **注記：**
>
> -   配置オプションは、各 TiKV ノードの構成で正しく指定されたラベルによって異なります。たとえば、 `PRIMARY_REGION`オプションは TiKV の`region`ラベルに依存します。 TiKV クラスターで使用可能なすべてのラベルの概要を表示するには、ステートメント[`SHOW PLACEMENT LABELS`](/sql-statements/sql-statement-show-placement-labels.md)を使用します。
>
>     ```sql
>     mysql> show placement labels;
>     +--------+----------------+
>     | Key    | Values         |
>     +--------+----------------+
>     | disk   | ["ssd"]        |
>     | region | ["us-east-1"]  |
>     | zone   | ["us-east-1a"] |
>     +--------+----------------+
>     3 rows in set (0.00 sec)
>     ```
>
> -   `CREATE PLACEMENT POLICY`を使用して配置ポリシーを作成する場合、TiDB はラベルが存在するかどうかをチェックしません。代わりに、TiDB は、ポリシーをテーブルにアタッチするときにチェックを実行します。

| オプション名           | 説明                                                                             |
| ---------------- | ------------------------------------------------------------------------------ |
| `PRIMARY_REGION` | Raftリーダーは、このオプションの値と一致する`region`ラベルが付いた店舗に配置されます。                              |
| `REGIONS`        | Raftフォロワーは、このオプションの値と一致する`region`ラベルを持つストアに配置されます。                             |
| `SCHEDULE`       | フォロワーの配置をスケジュールするために使用される戦略。値のオプションは`EVEN` (デフォルト) または`MAJORITY_IN_PRIMARY`です。 |
| `FOLLOWERS`      | フォロワー数。たとえば、 `FOLLOWERS=2` 、データのレプリカが 3 つ (2 つのフォロワーと 1 つのリーダー) 存在することを意味します。  |

上記の配置オプションに加えて、高度な構成を使用することもできます。詳細は[高度な配置オプション](#advanced-placement-options)を参照してください。

| オプション名                 | 説明                                                                              |
| ---------------------- | ------------------------------------------------------------------------------- |
| `CONSTRAINTS`          | すべてのロールに適用される制約のリスト。たとえば、 `CONSTRAINTS="[+disk=ssd]"` 。                         |
| `LEADER_CONSTRAINTS`   | 引出線にのみ適用される制約のリスト。                                                              |
| `FOLLOWER_CONSTRAINTS` | フォロワーにのみ適用される制約のリスト。                                                            |
| `LEARNER_CONSTRAINTS`  | 学習者にのみ適用される制約のリスト。                                                              |
| `LEARNERS`             | 学習者の数。                                                                          |
| `SURVIVAL_PREFERENCE`  | ラベルの災害耐性レベルに応じたレプリカ配置の優先順位。たとえば、 `SURVIVAL_PREFERENCE="[region, zone, host]"` 。 |

## 例 {#examples}

### レプリカの数を増やす {#increase-the-number-of-replicas}

<CustomContent platform="tidb">

デフォルト設定の[`max-replicas`](/pd-configuration-file.md#max-replicas)は`3`です。特定のテーブル セットに対してこれを増やすには、次のように配置ポリシーを使用できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

デフォルト設定の[`max-replicas`](https://docs.pingcap.com/tidb/stable/pd-configuration-file#max-replicas)は`3`です。特定のテーブル セットに対してこれを増やすには、次のように配置ポリシーを使用できます。

</CustomContent>

```sql
CREATE PLACEMENT POLICY fivereplicas FOLLOWERS=4;
CREATE TABLE t1 (a INT) PLACEMENT POLICY=fivereplicas;
```

PD 構成にはリーダーとフォロワーの数が含まれるため、フォロワー 4 個 + リーダー 1 個で合計 5 つのレプリカに相当することに注意してください。

この例をさらに拡張するには、 `PRIMARY_REGION`および`REGIONS`配置オプションを使用してフォロワーの配置を記述することもできます。

```sql
CREATE PLACEMENT POLICY eastandwest PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-east-2,us-west-1" SCHEDULE="MAJORITY_IN_PRIMARY" FOLLOWERS=4;
CREATE TABLE t1 (a INT) PLACEMENT POLICY=eastandwest;
```

`SCHEDULE`オプションは、フォロワーのバランスをとる方法を TiDB に指示します。デフォルトのスケジュール`EVEN`すべての地域でフォロワーのバランスが確保されます。

クォーラムを達成できるように十分なフォロワーがプライマリ リージョン ( `us-east-1` ) に配置されるようにするには、 `MAJORITY_IN_PRIMARY`スケジュールを使用できます。このスケジュールは、可用性をある程度犠牲にして、トランザクションのレイテンシーを短縮するのに役立ちます。プライマリ リージョンに障害が発生した場合、 `MAJORITY_IN_PRIMARY`自動フェールオーバーを提供できません。

### パーティションテーブルに配置を割り当てる {#assign-placement-to-a-partitioned-table}

配置オプションをテーブルに割り当てるだけでなく、テーブル パーティションにもオプションを割り当てることができます。例えば：

```sql
CREATE PLACEMENT POLICY p1 FOLLOWERS=5;
CREATE PLACEMENT POLICY europe PRIMARY_REGION="eu-central-1" REGIONS="eu-central-1,eu-west-1";
CREATE PLACEMENT POLICY northamerica PRIMARY_REGION="us-east-1" REGIONS="us-east-1";

SET tidb_enable_list_partition = 1;
CREATE TABLE t1 (
  country VARCHAR(10) NOT NULL,
  userdata VARCHAR(100) NOT NULL
) PLACEMENT POLICY=p1 PARTITION BY LIST COLUMNS (country) (
  PARTITION pEurope VALUES IN ('DE', 'FR', 'GB') PLACEMENT POLICY=europe,
  PARTITION pNorthAmerica VALUES IN ('US', 'CA', 'MX') PLACEMENT POLICY=northamerica,
  PARTITION pAsia VALUES IN ('CN', 'KR', 'JP')
);
```

パーティションにポリシーがアタッチされていない場合、テーブルに既存のポリシーを適用しようとします。たとえば、 `pEurope`パーティションには`europe`ポリシーが適用されますが、 `pAsia`パーティションには表`t1`の`p1`ポリシーが適用されます。 `t1`にポリシーが割り当てられていない場合、 `pAsia`ポリシーを適用しません。

特定のパーティションに割り当てられた配置ポリシーを変更することもできます。例えば：

```sql
ALTER TABLE t1 PARTITION pEurope PLACEMENT POLICY=p1;
```

### スキーマのデフォルトの配置を設定する {#set-the-default-placement-for-a-schema}

デフォルトの配置ルールをデータベース スキーマに直接添付できます。これは、スキーマのデフォルトの文字セットまたは照合順序を設定するのと同様に機能します。指定した配置オプションは、他のオプションが指定されていない場合に適用されます。例えば：

```sql
CREATE PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-east-2";  -- Create placement policies

CREATE PLACEMENT POLICY p2 FOLLOWERS=4;

CREATE PLACEMENT POLICY p3 FOLLOWERS=2;

CREATE TABLE t1 (a INT);  -- Creates a table t1 with no placement options.

ALTER DATABASE test PLACEMENT POLICY=p2;  -- Changes the default placement option, and does not apply to the existing table t1.

CREATE TABLE t2 (a INT);  -- Creates a table t2 with the default placement policy p2.

CREATE TABLE t3 (a INT) PLACEMENT POLICY=p1;  -- Creates a table t3 without the default policy p2, because this statement has specified another placement rule.

ALTER DATABASE test PLACEMENT POLICY=p3;  -- Changes the default policy, and does not apply to existing tables.

CREATE TABLE t4 (a INT);  -- Creates a table t4 with the default policy p3.

ALTER PLACEMENT POLICY p3 FOLLOWERS=3; -- The table with policy p3 (t4) will have FOLLOWERS=3.
```

これは、テーブルのポリシーを変更するとパーティションに影響する、パーティションとテーブル間の継承とは異なることに注意してください。テーブルは、ポリシーをアタッチせずに作成された場合にのみスキーマのポリシーを継承し、スキーマのポリシーを変更しても、作成されたテーブルには影響しません。

### 高度な配置オプション {#advanced-placement-options}

配置オプション`PRIMARY_REGION` 、および`SCHEDULE` `REGIONS`ある程度の柔軟性は失われますが、データ配置の基本的なニーズは満たします。より高い柔軟性が必要な、より複雑なシナリオの場合は、 `CONSTRAINTS`および`FOLLOWER_CONSTRAINTS`の高度な配置オプションを使用することもできます。 `PRIMARY_REGION` 、 `REGIONS` 、または`SCHEDULE`オプションと`CONSTRAINTS`オプションを同時に指定することはできません。同時に指定した場合はエラーとなります。

たとえば、ラベル`disk`が値と一致する必要がある TiKV ストアにデータが存在する必要があるという制約を設定するには、次のようにします。

```sql
CREATE PLACEMENT POLICY storageonnvme CONSTRAINTS="[+disk=nvme]";
CREATE PLACEMENT POLICY storageonssd CONSTRAINTS="[+disk=ssd]";
CREATE PLACEMENT POLICY companystandardpolicy CONSTRAINTS="";

CREATE TABLE t1 (id INT, name VARCHAR(50), purchased DATE)
PLACEMENT POLICY=companystandardpolicy
PARTITION BY RANGE( YEAR(purchased) ) (
  PARTITION p0 VALUES LESS THAN (2000) PLACEMENT POLICY=storageonssd,
  PARTITION p1 VALUES LESS THAN (2005),
  PARTITION p2 VALUES LESS THAN (2010),
  PARTITION p3 VALUES LESS THAN (2015),
  PARTITION p4 VALUES LESS THAN MAXVALUE PLACEMENT POLICY=storageonnvme
);
```

制約はリスト形式 ( `[+disk=ssd]` ) または辞書形式 ( `{+disk=ssd: 1,+disk=nvme: 2}` ) で指定できます。

リスト形式では、制約はキーと値のペアのリストとして指定されます。キーは`+`または`-`で始まります。 `+disk=ssd`ラベル`disk` `ssd`に設定する必要があることを示し、 `-disk=nvme`ラベル`disk` `nvme`に設定してはならないことを示します。

辞書形式では、制約はそのルールに適用されるインスタンスの数も示します。たとえば、 `FOLLOWER_CONSTRAINTS="{+region=us-east-1: 1,+region=us-east-2: 1,+region=us-west-1: 1}";` 1 人のフォロワーが us-east-1 に、1 人のフォロワーが us-east-2 に、1 人のフォロワーが us-west-1 にいることを示します。別の例として、 `FOLLOWER_CONSTRAINTS='{"+region=us-east-1,+disk=nvme":1,"+region=us-west-1":1}';` 、1 人のフォロワーが nvme ディスクを持つ us-east-1 にあり、1 人のフォロワーが us-west-1 にあることを示します。

> **注記：**
>
> 辞書とリストの形式は YAML パーサーに基づいていますが、YAML 構文が誤って解析される可能性があります。たとえば、 `"{+disk=ssd:1,+disk=nvme:2}"`は​​誤って`'{"+disk=ssd:1": null, "+disk=nvme:1": null}'`として解析されます。ただし、 `"{+disk=ssd: 1,+disk=nvme: 1}"`は`'{"+disk=ssd": 1, "+disk=nvme": 1}'`として正しく解析されます。

### 生存の好み {#survival-preferences}

配置ポリシーを作成または変更する場合、 `SURVIVAL_PREFERENCES`オプションを使用して、データの優先存続可能性を設定できます。

たとえば、3 つのアベイラビリティ ゾーンにまたがる TiDB クラスターがあり、各ゾーンの各ホストに複数の TiKV インスタンスがデプロイされていると仮定します。このクラスターの配置ポリシーを作成するときに、次のように`SURVIVAL_PREFERENCES`を設定しました。

```sql
CREATE PLACEMENT POLICY multiaz SURVIVAL_PREFERENCES="[zone, host]";
CREATE PLACEMENT POLICY singleaz CONSTRAINTS="[+zone=zone1]" SURVIVAL_PREFERENCES="[host]";
```

配置ポリシーを作成した後、必要に応じて、それらを対応するテーブルにアタッチできます。

-   `multiaz`配置ポリシーがアタッチされたテーブルの場合、データは異なるアベイラビリティ ゾーンの 3 つのレプリカに配置され、ゾーン間のデータ分離の存続目標が優先され、ホスト間のデータ分離の存続目標が続きます。
-   `singleaz`配置ポリシーがアタッチされたテーブルの場合、データは最初に`zone1`アベイラビリティ ゾーン内の 3 つのレプリカに配置され、その後ホスト間でのデータ分離の存続目標が満たされます。

<CustomContent platform="tidb">

> **注記：**
>
> `SURVIVAL_PREFERENCES`は PD の`location-labels`に相当します。詳細については、 [トポロジーラベルごとにレプリカをスケジュールする](/schedule-replicas-by-topology-labels.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> `SURVIVAL_PREFERENCES`は PD の`location-labels`に相当します。詳細については、 [トポロジーラベルごとにレプリカをスケジュールする](https://docs.pingcap.com/tidb/stable/schedule-replicas-by-topology-labels)を参照してください。

</CustomContent>

## ツールとの互換性 {#compatibility-with-tools}

<CustomContent platform="tidb">

| ツール名           | サポートされる最小バージョン | 説明                                                                                                 |
| -------------- | -------------- | -------------------------------------------------------------------------------------------------- |
| バックアップと復元 (BR) | 6.0            | 配置ルールのインポートとエクスポートをサポートします。詳細は[BRの互換性](/br/backup-and-restore-overview.md#compatibility)を参照してください。 |
| TiDB Lightning | まだ互換性がありません    | TiDB Lightning が配置ポリシーを含むバックアップ データをインポートするとエラーが報告される                                              |
| TiCDC          | 6.0            | 配置ルールを無視し、ルールをダウンストリームに複製しません。                                                                     |
| TiDBBinlog     | 6.0            | 配置ルールを無視し、ルールをダウンストリームに複製しません。                                                                     |

</CustomContent>

<CustomContent platform="tidb-cloud">

| TiDB Lightning|まだ互換性がありません | TiDB Lightning が配置ポリシーを含むバックアップ データをインポートすると、エラーが報告されます。 |ティCDC | 6.0 |配置ルールを無視し、ルールをダウンストリームに複製しません。

</CustomContent>

## 既知の制限事項 {#known-limitations}

既知の制限事項は次のとおりです。

-   一時テーブルは配置オプションをサポートしていません。
-   設定`PRIMARY_REGION`および`REGIONS`では、糖衣構文ルールが許可されます。将来的には、 `PRIMARY_RACK` 、 `PRIMARY_ZONE` 、 `PRIMARY_HOST`の品種も追加する予定です。 [問題 #18030](https://github.com/pingcap/tidb/issues/18030)を参照してください。
-   配置ルールは、保存データが正しい TiKV ストアに存在することを保証するだけです。このルールでは、転送中のデータ (ユーザー クエリまたは内部操作による) が特定のリージョンでのみ発生することは保証されません。
