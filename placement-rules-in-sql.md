---
title: Placement Rules in SQL
summary: Learn how to schedule placement of tables and partitions using SQL statements.
---

# SQLでの配置ルール {#placement-rules-in-sql}

SQLの配置ルールは、SQLインターフェイスを使用してTiKVクラスタのどこにデータを格納するかを指定できる機能です。この機能を使用して、テーブルとパーティションが特定のリージョン、データセンター、ラック、またはホストにスケジュールされます。これは、低コストで高可用性戦略を最適化する、データのローカルレプリカをローカルの古い読み取りに使用できるようにする、データの局所性要件を順守するなどのシナリオで役立ちます。

> **ノート：**
>
> *SQLでの配置ルール*の実装は、PDの<em>配置ルール機能</em>に依存しています。詳しくは[配置ルールを構成する](/configure-placement-rules.md)をご覧ください。 SQLの配置ルールのコンテキストでは、<em>配置ルール</em>は、他のオブジェクトにアタッチされた<em>配置ポリシー</em>、またはTiDBからPDに送信されるルールを参照する場合があります。

詳細なユーザーシナリオは次のとおりです。

-   異なるアプリケーションの複数のデータベースをマージして、データベースの保守コストを削減します
-   重要なデータのレプリカ数を増やして、アプリケーションの可用性とデータの信頼性を向上させます
-   新しいデータをNVMeストレージに保存し、古いデータをSSDに保存して、データのアーカイブとストレージのコストを削減します
-   ホットスポットデータのリーダーを高性能TiKVインスタンスにスケジュールする
-   コールドデータを低コストのストレージメディアに分離して、コスト効率を向上させます

## 配置ルールを指定する {#specify-placement-rules}

配置ルールを指定するには、最初に[`CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-create-placement-policy.md)を使用して配置ポリシーを作成します。

```sql
CREATE PLACEMENT POLICY myplacementpolicy PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1";
```

次に、 `CREATE TABLE`または`ALTER TABLE`を使用して、ポリシーをテーブルまたはパーティションにアタッチします。次に、配置ルールがテーブルまたはパーティションで指定されます。

```sql
CREATE TABLE t1 (a INT) PLACEMENT POLICY=myplacementpolicy;
CREATE TABLE t2 (a INT);
ALTER TABLE t2 PLACEMENT POLICY=myplacementpolicy;
```

配置ポリシーはどのデータベーススキーマにも関連付けられておらず、グローバルスコープを持っています。したがって、配置ポリシーを割り当てるために、 `CREATE TABLE`の特権に対する追加の特権は必要ありません。

配置ポリシーを変更するには、 [`ALTER PLACEMENT POLICY`](/sql-statements/sql-statement-alter-placement-policy.md)を使用できます。変更は、対応するポリシーが割り当てられているすべてのオブジェクトに反映されます。

```sql
ALTER PLACEMENT POLICY myplacementpolicy FOLLOWERS=5;
```

テーブルまたはパーティションに接続されていないポリシーを削除するには、 [`DROP PLACEMENT POLICY`](/sql-statements/sql-statement-drop-placement-policy.md)を使用できます。

```sql
DROP PLACEMENT POLICY myplacementpolicy;
```

## 現在の配置ルールをビューする {#view-current-placement-rules}

テーブルに配置ルールが添付されている場合は、 [`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md)の出力で配置ルールを表示できます。使用可能なポリシーの定義を表示するには、 [`SHOW CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-show-create-placement-policy.md)を実行します。

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

[`INFORMATION_SCHEMA.PLACEMENT_POLICIES`](/information-schema/information-schema-placement-policies.md)の表を使用して、配置ポリシーの定義を表示することもできます。

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

`information_schema.tables`と`information_schema.partitions`のテーブルには、配置ルールが添付されたすべてのオブジェクトを示す`tidb_placement_policy_name`の列も含まれています。

```sql
SELECT * FROM information_schema.tables WHERE tidb_placement_policy_name IS NOT NULL;
SELECT * FROM information_schema.partitions WHERE tidb_placement_policy_name IS NOT NULL;
```

オブジェクトに添付されているルールは*非同期*で適用されます。配置の現在のスケジュールの進行状況を表示するには、 [`SHOW PLACEMENT`](/sql-statements/sql-statement-show-placement.md)を使用します。

## オプションリファレンス {#option-reference}

> **ノート：**
>
> -   配置オプションは、各TiKVノードの構成で正しく指定されたラベルによって異なります。たとえば、 `PRIMARY_REGION`オプションはTiKVの`region`ラベルに依存します。 TiKVクラスタで使用可能なすべてのラベルの要約を表示するには、ステートメント[`SHOW PLACEMENT LABELS`](/sql-statements/sql-statement-show-placement-labels.md)を使用します。
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
> -   `CREATE PLACEMENT POLICY`を使用して配置ポリシーを作成すると、TiDBはラベルが存在するかどうかをチェックしません。代わりに、ポリシーをテーブルにアタッチすると、TiDBがチェックを実行します。

| オプション名           | 説明                                                                            |
| ---------------- | ----------------------------------------------------------------------------- |
| `PRIMARY_REGION` | Raftリーダーは、このオプションの値と一致する`region`のラベルを持つストアに配置されます。                            |
| `REGIONS`        | Raftフォロワーは、このオプションの値と一致する`region`のラベルを持つストアに配置されます。                           |
| `SCHEDULE`       | フォロワーの配置をスケジュールするために使用される戦略。値のオプションは`EVEN` （デフォルト）または`MAJORITY_IN_PRIMARY`です。 |
| `FOLLOWERS`      | フォロワーの数。たとえば、 `FOLLOWERS=2`は、データのレプリカが3つあることを意味します（2人のフォロワーと1人のリーダー）。         |

上記の配置オプションに加えて、事前構成を使用することもできます。詳細については、 [アドバンストプレイスメントオプション](#advanced-placement-options)を参照してください。

| オプション名                 | 説明                                                     |
| ---------------------- | ------------------------------------------------------ |
| `CONSTRAINTS`          | すべての役割に適用される制約のリスト。たとえば、 `CONSTRAINTS="[+disk=ssd]"` 。 |
| `LEADER_CONSTRAINTS`   | リーダーにのみ適用される制約のリスト。                                    |
| `FOLLOWER_CONSTRAINTS` | フォロワーにのみ適用される制約のリスト。                                   |
| `LEARNER_CONSTRAINTS`  | 学習者にのみ適用される制約のリスト。                                     |
| `LEARNERS`             | 学習者の数。                                                 |

## 例 {#examples}

### レプリカの数を増やす {#increase-the-number-of-replicas}

[`max-replicas`](/pd-configuration-file.md#max-replicas)のデフォルト構成は`3`です。特定のテーブルセットに対してこれを増やすには、次のように配置ポリシーを使用できます。

```sql
CREATE PLACEMENT POLICY fivereplicas FOLLOWERS=4;
CREATE TABLE t1 (a INT) PLACEMENT POLICY=fivereplicas;
```

PD構成にはリーダーとフォロワーの数が含まれているため、4つのフォロワー+1つのリーダーは合計5つのレプリカに相当することに注意してください。

この例を拡張するために、 `PRIMARY_REGION`と`REGIONS`の配置オプションを使用して、フォロワーの配置を説明することもできます。

```sql
CREATE PLACEMENT POLICY eastandwest PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-east-2,us-west-1" SCHEDULE="MAJORITY_IN_PRIMARY" FOLLOWERS=4;
CREATE TABLE t1 (a INT) PLACEMENT POLICY=eastandwest;
```

`SCHEDULE`オプションは、フォロワーのバランスをとる方法についてTiDBに指示します。デフォルトのスケジュールである`EVEN`は、すべての地域でフォロワーのバランスを確保します。

クォーラムを達成できるように十分なフォロワーがプライマリリージョン（ `us-east-1` ）に配置されるようにするには、 `MAJORITY_IN_PRIMARY`のスケジュールを使用できます。このスケジュールは、可用性をいくらか犠牲にして、待ち時間の短いトランザクションを提供するのに役立ちます。プライマリリージョンに障害が発生した場合、 `MAJORITY_IN_PRIMARY`は自動フェイルオーバーを提供できません。

### パーティションテーブルに配置を割り当てる {#assign-placement-to-a-partitioned-table}

テーブルに配置オプションを割り当てるだけでなく、テーブルパーティションにオプションを割り当てることもできます。例えば：

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

パーティションにポリシーが添付されていない場合、パーティションはテーブルに既存のポリシーを適用しようとします。たとえば、 `pEurope`パーティションは`europe`ポリシーを適用しますが、 `pAsia`パーティションは表`t1`の`p1`ポリシーを適用します。 `t1`にポリシーが割り当てられていない場合、 `pAsia`もポリシーを適用しません。

特定のパーティションに割り当てられた配置ポリシーを変更することもできます。例えば：

```sql
ALTER TABLE t1 PARTITION pEurope PLACEMENT POLICY=p1;
```

### スキーマのデフォルトの配置を設定する {#set-the-default-placement-for-a-schema}

デフォルトの配置ルールをデータベーススキーマに直接アタッチできます。これは、スキーマのデフォルトの文字セットまたは照合順序を設定するのと同様に機能します。指定した配置オプションは、他のオプションが指定されていない場合に適用されます。例えば：

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

これは、パーティションとテーブル間の継承とは異なり、テーブルのポリシーを変更するとパーティションに影響することに注意してください。テーブルは、ポリシーが添付されていない状態で作成された場合にのみスキーマのポリシーを継承し、スキーマのポリシーを変更しても、作成されたテーブルには影響しません。

### 高度な配置オプション {#advanced-placement-options}

配置オプション`PRIMARY_REGION` 、および`REGIONS`は、ある程度の柔軟性を失いながら、データ配置の基本的なニーズを満たし`SCHEDULE` 。より高い柔軟性が必要なより複雑なシナリオでは、 `CONSTRAINTS`および`FOLLOWER_CONSTRAINTS`の高度な配置オプションを使用することもできます。 `PRIMARY_REGION` 、または`REGIONS`オプションと`SCHEDULE`オプションを`CONSTRAINTS`指定することはできません。両方を同時に指定すると、エラーが返されます。

たとえば、データがラベル`disk`が値と一致する必要があるTiKVストアに存在する必要があるという制約を設定するには、次のようにします。

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

制約は、リスト形式（ `[+disk=ssd]` ）またはディクショナリ形式（ `{+disk=ssd: 1,+disk=nvme: 2}` ）のいずれかで指定できます。

リスト形式では、制約はキーと値のペアのリストとして指定されます。キーは`+`または`-`で始まります。 `+disk=ssd`は、ラベル`disk`を`ssd`に設定する必要があることを示し、 `-disk=nvme`は、ラベル`disk`を`nvme`に設定してはならないことを示します。

辞書形式では、制約はそのルールに適用されるインスタンスの数も示します。たとえば、 `FOLLOWER_CONSTRAINTS="{+region=us-east-1: 1,+region=us-east-2: 1,+region=us-west-1: 1}";`は、1人のフォロワーがus-east-1にあり、1人のフォロワーがus-east-2にあり、1人のフォロワーがus-west-1にいることを示します。別の例として、 `FOLLOWER_CONSTRAINTS='{"+region=us-east-1,+disk=nvme":1,"+region=us-west-1":1}';`は、1人のフォロワーがnvmeディスクを使用してus-east-1にあり、1人のフォロワーがus-west-1にいることを示します。

> **ノート：**
>
> 辞書とリストの形式はYAMLパーサーに基づいていますが、YAML構文が正しく解析されない可能性があります。たとえば、 `"{+disk=ssd:1,+disk=nvme:2}"`は誤って`'{"+disk=ssd:1": null, "+disk=nvme:1": null}'`として解析されます。ただし、 `"{+disk=ssd: 1,+disk=nvme: 1}"`は`'{"+disk=ssd": 1, "+disk=nvme": 1}'`として正しく解析されます。

## ツールとの互換性 {#compatibility-with-tools}

| ツール名           | サポートされている最小バージョン | 説明                                                                                                 |
| -------------- | ---------------- | -------------------------------------------------------------------------------------------------- |
| バックアップと復元（BR）  | 6.0              | 配置ルールのインポートとエクスポートをサポートします。詳細は[BRの互換性](/br/backup-and-restore-overview.md#compatibility)を参照してください。 |
| TiDB Lightning | まだ互換性がありません      | TiDB Lightningが配置ポリシーを含むバックアップデータをインポートすると、エラーが報告されます                                              |
| TiCDC          | 6.0              | 配置ルールを無視し、ルールをダウンストリームに複製しません                                                                      |
| TiDB Binlog    | 6.0              | 配置ルールを無視し、ルールをダウンストリームに複製しません                                                                      |

## 既知の制限 {#known-limitations}

SQLの配置ルールの実験的リリースには、次の既知の制限があります。

-   一時テーブルは配置オプションをサポートしていません。
-   設定`PRIMARY_REGION`および`REGIONS`には、構文糖衣規則が許可されています。将来的には、 `PRIMARY_RACK`の`PRIMARY_ZONE`を追加する予定`PRIMARY_HOST` 。 [号18030](https://github.com/pingcap/tidb/issues/18030)を参照してください。
-   TiFlashラーナーは、配置ルール構文を使用して構成することはできません。
-   配置ルールは、保存されているデータが正しいTiKVストアに存在することのみを保証します。このルールは、転送中のデータ（ユーザークエリまたは内部操作のいずれかを介して）が特定の地域でのみ発生することを保証するものではありません。
