---
title: Placement Rules in SQL
summary: Learn how to schedule placement of tables and partitions using SQL statements.
---

# SQL の配置規則 {#placement-rules-in-sql}

> **警告：**
>
> SQL の配置規則は、v5.3.0 で導入された実験的機能です。構文は GA の前に変更される可能性があり、バグもある可能性があります。リスクを理解している場合は、 `SET GLOBAL tidb_enable_alter_placement = 1;`を実行してこの実験機能を有効にすることができます。

SQL の配置ルールは、SQL インターフェイスを使用して TiKV クラスター内のデータの保存場所を指定できるようにする機能です。この機能を使用すると、テーブルとパーティションが特定の地域、データ センター、ラック、またはホストにスケジュールされます。これは、低コストで高可用性戦略を最適化したり、データのローカル レプリカをローカルの古い読み取りに使用できるようにしたり、データの局所性要件を順守したりするなどのシナリオに役立ちます。

詳細なユーザー シナリオは次のとおりです。

-   異なるアプリケーションの複数のデータベースをマージして、データベース メンテナンスのコストを削減します。
-   重要なデータのレプリカ数を増やして、アプリケーションの可用性とデータの信頼性を向上させます
-   新しいデータを NVMe ストレージに保存し、古いデータを SSD に保存して、データのアーカイブとストレージのコストを削減します
-   ホットスポット データのリーダーを高性能 TiKV インスタンスにスケジュールする
-   コールド データを低コストのストレージ メディアに分離して、コスト効率を向上させる

## 配置オプションを指定する {#specify-placement-options}

SQL で配置規則を使用するには、SQL ステートメントで 1 つ以上の配置オプションを指定する必要があります。配置オプションを指定するには、*直接配置*または<em>配置ポリシー</em>を使用できます。

次の例では、テーブル`t1`と`t2`の両方に同じルールがあります。 `t1`は直接配置を使用して指定されたルールであり、 `t2`は配置ポリシーを使用して指定されたルールです。

```sql
CREATE TABLE t1 (a INT) PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1";
CREATE PLACEMENT POLICY eastandwest PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1";
CREATE TABLE t2 (a INT) PLACEMENT POLICY=eastandwest;
```

ルール管理を簡素化するために、配置ポリシーを使用することをお勧めします。配置ポリシーを ( [`ALTER PLACEMENT POLICY`](/sql-statements/sql-statement-alter-placement-policy.md)を介して) 変更すると、その変更はすべてのデータベース オブジェクトに自動的に反映されます。

直接配置オプションを使用する場合は、オブジェクト (テーブルやパーティションなど) ごとにルールを変更する必要があります。

`PLACEMENT POLICY`はどのデータベース スキーマにも関連付けられておらず、グローバル スコープを持ちます。したがって、配置ポリシーを割り当てる場合、 `CREATE TABLE`権限以上の追加の特権は必要ありません。

## オプション参照 {#option-reference}

> **ノート：**
>
> -   配置オプションは、各 TiKV ノードの構成で正しく指定されたラベルに依存します。たとえば、 `PRIMARY_REGION`オプションは TiKV の`region`ラベルに依存します。 TiKV クラスターで使用可能なすべてのラベルの概要を表示するには、ステートメント[`SHOW PLACEMENT LABELS`](/sql-statements/sql-statement-show-placement-labels.md)を使用します。
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
> -   `CREATE PLACEMENT POLICY`を使用して配置ポリシーを作成すると、TiDB はラベルが存在するかどうかをチェックしません。代わりに、TiDB は、ポリシーをテーブルにアタッチするときにチェックを実行します。

| オプション名           | 説明                                                                             |
| ---------------- | ------------------------------------------------------------------------------ |
| `PRIMARY_REGION` | Raftのリーダーは、このオプションの値に一致する`region`のラベルを持つストアに配置されます。                            |
| `REGIONS`        | Raftフォロワーは、このオプションの値に一致する`region`のラベルを持つストアに配置されます。                            |
| `SCHEDULE`       | フォロワーの配置をスケジュールするために使用される戦略。値のオプションは`EVEN` (デフォルト) または`MAJORITY_IN_PRIMARY`です。 |
| `FOLLOWERS`      | フォロワー数。たとえば、 `FOLLOWERS=2`は、データのレプリカが 3 つあることを意味します (フォロワー 2 つとリーダー 1 つ)。      |

上記の配置オプションに加えて、高度な構成も使用できます。詳細については、 [先行配置](#advanced-placement)を参照してください。

| オプション名                 | 説明                                                      |
| ---------------------- | ------------------------------------------------------- |
| `CONSTRAINTS`          | すべてのロールに適用される制約のリスト。たとえば、 `CONSTRAINTS="[+disk=ssd]`です。 |
| `FOLLOWER_CONSTRAINTS` | フォロワーのみに適用される制約のリスト。                                    |

## 例 {#examples}

### レプリカの数を増やす {#increase-the-number-of-replicas}

[`max-replicas`](/pd-configuration-file.md#max-replicas)のデフォルト設定は`3`です。特定のテーブル セットでこれを増やすには、次のように配置ポリシーを使用できます。

```sql
CREATE PLACEMENT POLICY fivereplicas FOLLOWERS=4;
CREATE TABLE t1 (a INT) PLACEMENT POLICY=fivereplicas;
```

PD 構成にはリーダーとフォロワーの数が含まれていることに注意してください。したがって、4 つのフォロワー + 1 つのリーダーは、合計で 5 つのレプリカに相当します。

この例を拡張するために、 `PRIMARY_REGION`と`REGIONS`の配置オプションを使用して、フォロワーの配置を説明することもできます。

```sql
CREATE PLACEMENT POLICY eastandwest PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-east-2,us-west-1" SCHEDULE="MAJORITY_IN_PRIMARY" FOLLOWERS=4;
CREATE TABLE t1 (a INT) PLACEMENT POLICY=eastandwest;
```

`SCHEDULE`オプションは、フォロワーのバランスを取る方法を TiDB に指示します。デフォルトのスケジュール`EVEN`では、すべての地域でフォロワーのバランスが確保されます。

クォーラムを達成できるように十分な数のフォロワーがプライマリ リージョン ( `us-east-1` ) に配置されるようにするには、 `MAJORITY_IN_PRIMARY`スケジュールを使用できます。このスケジュールは、ある程度の可用性を犠牲にして、より低いレイテンシーのトランザクションを提供するのに役立ちます。プライマリ リージョンに障害が発生した場合、 `MAJORITY_IN_PRIMARY`は自動フェールオーバーを提供できません。

### パーティションテーブルに配置を割り当てる {#assign-placement-to-a-partitioned-table}

> **ノート：**
>
> 次の例では、現在 TiDB の実験的機能であるリスト パーティショニングを使用しています。分割されたテーブルでは、テーブルの分割関数のすべての列に`PRIMARY KEY`を含める必要もあります。

配置オプションをテーブルに割り当てるだけでなく、オプションをテーブル パーティションに割り当てることもできます。例えば：

```sql
CREATE PLACEMENT POLICY europe PRIMARY_REGION="eu-central-1" REGIONS="eu-central-1,eu-west-1";
CREATE PLACEMENT POLICY northamerica PRIMARY_REGION="us-east-1" REGIONS="us-east-1";

SET tidb_enable_list_partition = 1;
CREATE TABLE t1 (
  country VARCHAR(10) NOT NULL,
  userdata VARCHAR(100) NOT NULL
) PARTITION BY LIST COLUMNS (country) (
  PARTITION pEurope VALUES IN ('DE', 'FR', 'GB') PLACEMENT POLICY=europe,
  PARTITION pNorthAmerica VALUES IN ('US', 'CA', 'MX') PLACEMENT POLICY=northamerica
);
```

### スキーマのデフォルトの配置を設定する {#set-the-default-placement-for-a-schema}

デフォルトの配置オプションをデータベース スキーマに直接アタッチできます。これは、スキーマのデフォルトの文字セットまたは照合順序を設定するのと同様に機能します。指定した配置オプションは、他のオプションが指定されていない場合に適用されます。例えば：

```sql
CREATE TABLE t1 (a INT);  -- Creates a table t1 with no placement options.

ALTER DATABASE test FOLLOWERS=4;  -- Changes the default placement option, and does not apply to the existing table t1.

CREATE TABLE t2 (a INT);  -- Creates a table t2 with the default placement of FOLLOWERS=4.

CREATE TABLE t3 (a INT) PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-east-2";  -- Creates a table t3 without the default FOLLOWERS=4 placement, because this statement has specified another placement.

ALTER DATABASE test FOLLOWERS=2;  -- Changes the default placement, and does not apply to existing tables.

CREATE TABLE t4 (a INT);  -- Creates a table t4 with the default FOLLOWERS=2 option.
```

配置オプションは、テーブルの作成時にデータベース スキーマからのみ継承されるため、 `PLACEMENT POLICY`を使用してデフォルトの配置オプションを設定することをお勧めします。これにより、ポリシーに対する将来の変更が既存のテーブルに確実に反映されます。

### 高度な配置 {#advanced-placement}

配置オプション`PRIMARY_REGION` 、 `REGIONS` 、および`SCHEDULE`は、データ配置の基本的なニーズを満たしますが、ある程度の柔軟性が失われます。より高い柔軟性が必要なより複雑なシナリオでは、 `CONSTRAINTS`および`FOLLOWER_CONSTRAINTS`の高度な配置オプションを使用することもできます。 `PRIMARY_REGION` 、 `REGIONS` 、または`SCHEDULE`オプションを`CONSTRAINTS`オプションと同時に指定することはできません。両方を同時に指定すると、エラーが返されます。

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

リスト形式 ( `[+disk=ssd]` ) または辞書形式 ( `{+disk=ssd: 1,+disk=nvme: 2}` ) で制約を指定できます。

リスト形式では、制約はキーと値のペアのリストとして指定されます。キーは`+`または`-`で始まります。 `+disk=ssd`はラベル`disk`を`ssd`に設定する必要があることを示し、 `-disk=nvme`はラベル`disk`を`nvme`に設定してはならないことを示します。

ディクショナリ形式では、制約はそのルールに適用されるインスタンスの数も示します。たとえば、 `FOLLOWER_CONSTRAINTS="{+region=us-east-1: 1,+region=us-east-2: 1,+region=us-west-1: 1,+any: 1}";`は、1 人のフォロワーが us-east-1 に、1 人のフォロワーが us-east-2 に、1 人のフォロワーが us-west-1 に、1 人のフォロワーが任意のリージョンにいることを示します。別の例として、 `FOLLOWER_CONSTRAINTS='{"+region=us-east-1,+disk=nvme":1,"+region=us-west-1":1}';`は、1 人のフォロワーが nvme ディスクを持つ us-east-1 にあり、1 人のフォロワーが us-west-1 にあることを示します。

> **ノート：**
>
> ディクショナリとリストの形式は YAML パーサーに基づいていますが、YAML 構文は正しく解析されない可能性があります。たとえば、 `"{+disk=ssd:1,+disk=nvme:2}"`は`'{"+disk=ssd:1": null, "+disk=nvme:1": null}'`として誤って解析されます。しかし、 `"{+disk=ssd: 1,+disk=nvme: 1}"`は`'{"+disk=ssd": 1, "+disk=nvme": 1}'`として正しく解析されます。

## 既知の制限 {#known-limitations}

次の既知の制限事項は次のとおりです。

-   Dumplingは、ダンプ配置ポリシーをサポートしていません。 [問題 #29371](https://github.com/pingcap/tidb/issues/29371)を参照してください。
-   Backup &amp; Restore (BR)、TiCDC、 TiDB Lightning、TiDB Data Migration (DM) などの TiDB ツールは、配置ルールをまだサポートしていません。
-   一時テーブルは、(直接配置または配置ポリシーによる) 配置オプションをサポートしていません。
-   設定`PRIMARY_REGION`および`REGIONS` 、構文糖衣規則が許可されます。今後、 `PRIMARY_RACK`・`PRIMARY_ZONE`・`PRIMARY_HOST`の品種追加を予定しております。 [問題 #18030](https://github.com/pingcap/tidb/issues/18030)を参照してください。
-   TiFlash学習者は、配置規則の構文では構成できません。
-   配置ルールは、保管中のデータが正しい TiKV ストアに存在することのみを保証します。ルールは、(ユーザー クエリまたは内部操作のいずれかを介して) 転送中のデータが特定のリージョンでのみ発生することを保証するものではありません。
