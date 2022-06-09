---
title: Placement Rules in SQL
summary: Learn how to schedule placement of tables and partitions using SQL statements.
---

# SQLの配置ルール {#placement-rules-in-sql}

> **警告：**
>
> SQLの配置ルールは、v5.3.0で導入された実験的機能です。 GAの前に構文が変更される可能性があり、バグもある可能性があります。リスクを理解している場合は、 `SET GLOBAL tidb_enable_alter_placement = 1;`を実行することでこの実験機能を有効にできます。

SQLの配置ルールは、SQLインターフェイスを使用してTiKVクラスタのどこにデータを格納するかを指定できる機能です。この機能を使用して、テーブルとパーティションは特定のリージョン、データセンター、ラック、またはホストにスケジュールされます。これは、低コストで高可用性戦略を最適化する、データのローカルレプリカをローカルの古い読み取りに使用できるようにする、データの局所性要件を順守するなどのシナリオで役立ちます。

詳細なユーザーシナリオは次のとおりです。

-   異なるアプリケーションの複数のデータベースをマージして、データベースの保守コストを削減します
-   重要なデータのレプリカ数を増やして、アプリケーションの可用性とデータの信頼性を向上させます
-   新しいデータをSSDに保存し、古いデータをHHDに保存して、データのアーカイブとストレージのコストを削減します
-   ホットスポットデータのリーダーを高性能TiKVインスタンスにスケジュールする
-   コールドデータを低コストのストレージメディアに分離して、コスト効率を向上させます

## 配置オプションを指定する {#specify-placement-options}

SQLで配置ルールを使用するには、SQLステートメントで1つ以上の配置オプションを指定する必要があります。配置オプションを指定するには、*直接配置*を使用するか、<em>配置ポリシー</em>を使用できます。

次の例では、テーブル`t1`と`t2`の両方に同じルールがあります。 `t1`は直接配置を使用して指定されたルールであり、 `t2`は配置ポリシーを使用して指定されたルールです。

```sql
CREATE TABLE t1 (a INT) PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1";
CREATE PLACEMENT POLICY eastandwest PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1";
CREATE TABLE t2 (a INT) PLACEMENT POLICY=eastandwest;
```

ルール管理を簡単にするために、配置ポリシーを使用することをお勧めします。配置ポリシーを（ [`ALTER PLACEMENT POLICY`](/sql-statements/sql-statement-alter-placement-policy.md)を介して）変更すると、変更はすべてのデータベースオブジェクトに自動的に反映されます。

直接配置オプションを使用する場合は、各オブジェクト（テーブルやパーティションなど）のルールを変更する必要があります。

`PLACEMENT POLICY`はどのデータベーススキーマにも関連付けられておらず、グローバルスコープを持っています。したがって、配置ポリシーを割り当てるために、 `CREATE TABLE`の特権に対する追加の特権は必要ありません。

## オプションリファレンス {#option-reference}

> **ノート：**
>
> 配置オプションは、各TiKVノードの構成で正しく指定されたラベルによって異なります。たとえば、 `PRIMARY_REGION`オプションはTiKVの`region`ラベルに依存します。 TiKVクラスタで使用可能なすべてのラベルの要約を表示するには、ステートメント[`SHOW PLACEMENT LABELS`](/sql-statements/sql-statement-show-placement-labels.md)を使用します。
>
> ```sql
> mysql> show placement labels;
> +--------+----------------+
> | Key    | Values         |
> +--------+----------------+
> | disk   | ["ssd"]        |
> | region | ["us-east-1"]  |
> | zone   | ["us-east-1a"] |
> +--------+----------------+
> 3 rows in set (0.00 sec)
> ```

| オプション名           | 説明                                                                            |
| ---------------- | ----------------------------------------------------------------------------- |
| `PRIMARY_REGION` | いかだリーダーは、このオプションの値と一致する`region`のラベルを持つストアに配置されます。                             |
| `REGIONS`        | いかだフォロワーは、このオプションの値と一致する`region`のラベルを持つストアに配置されます。                            |
| `SCHEDULE`       | フォロワーの配置をスケジュールするために使用される戦略。値のオプションは`EVEN` （デフォルト）または`MAJORITY_IN_PRIMARY`です。 |
| `FOLLOWERS`      | フォロワーの数。たとえば、 `FOLLOWERS=2`は、データのレプリカが3つあることを意味します（フォロワー2つとリーダー1つ）。           |

上記の配置オプションに加えて、事前構成を使用することもできます。詳細については、 [アドバンストプレイスメント](#advanced-placement)を参照してください。

| オプション名                 | 説明                                                    |
| ---------------------- | ----------------------------------------------------- |
| `CONSTRAINTS`          | すべての役割に適用される制約のリスト。たとえば、 `CONSTRAINTS="[+disk=ssd]` 。 |
| `FOLLOWER_CONSTRAINTS` | フォロワーにのみ適用される制約のリスト。                                  |

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

### パーティションテーブルに配置を割り当てます {#assign-placement-to-a-partitioned-table}

> **ノート：**
>
> 次の例では、現在TiDBの実験的機能であるリストパーティショニングを使用しています。パーティション化されたテーブルでは、テーブルのパーティション化関数のすべての列に`PRIMARY KEY`が含まれている必要もあります。

テーブルに配置オプションを割り当てるだけでなく、テーブルパーティションにオプションを割り当てることもできます。例えば：

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

デフォルトの配置オプションをデータベーススキーマに直接アタッチできます。これは、スキーマのデフォルトの文字セットまたは照合順序を設定するのと同様に機能します。指定した配置オプションは、他のオプションが指定されていない場合に適用されます。例えば：

```sql
CREATE TABLE t1 (a INT);  -- Creates a table t1 with no placement options.

ALTER DATABASE test FOLLOWERS=4;  -- Changes the default placement option, and does not apply to the existing table t1.

CREATE TABLE t2 (a INT);  -- Creates a table t2 with the default placement of FOLLOWERS=4.

CREATE TABLE t3 (a INT) PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-east-2";  -- Creates a table t3 without the default FOLLOWERS=4 placement, because this statement has specified another placement.

ALTER DATABASE test FOLLOWERS=2;  -- Changes the default placement, and does not apply to existing tables.

CREATE TABLE t4 (a INT);  -- Creates a table t4 with the default FOLLOWERS=2 option.
```

配置オプションは、テーブルの作成時にデータベーススキーマからのみ継承されるため、 `PLACEMENT POLICY`を使用してデフォルトの配置オプションを設定することをお勧めします。これにより、ポリシーへの将来の変更が既存のテーブルに確実に反映されます。

### アドバンストプレイスメント {#advanced-placement}

配置オプション`PRIMARY_REGION` 、および`REGIONS`は、ある程度の柔軟性を失いながら、データ配置の基本的なニーズを満たし`SCHEDULE` 。より高い柔軟性が必要なより複雑なシナリオでは、 `CONSTRAINTS`および`FOLLOWER_CONSTRAINTS`の高度な配置オプションを使用することもできます。 `PRIMARY_REGION` 、または`REGIONS`オプションと`SCHEDULE`オプションを`CONSTRAINTS`指定することはできません。両方を同時に指定すると、エラーが返されます。

たとえば、データがラベル`disk`が値と一致する必要があるTiKVストアに存在する必要があるという制約を設定するには、次のようにします。

```sql
CREATE PLACEMENT POLICY storeonfastssd CONSTRAINTS="[+disk=ssd]";
CREATE PLACEMENT POLICY storeonhdd CONSTRAINTS="[+disk=hdd]";
CREATE PLACEMENT POLICY companystandardpolicy CONSTRAINTS="";

CREATE TABLE t1 (id INT, name VARCHAR(50), purchased DATE)
PLACEMENT POLICY=companystandardpolicy
PARTITION BY RANGE( YEAR(purchased) ) (
  PARTITION p0 VALUES LESS THAN (2000) PLACEMENT POLICY=storeonhdd,
  PARTITION p1 VALUES LESS THAN (2005),
  PARTITION p2 VALUES LESS THAN (2010),
  PARTITION p3 VALUES LESS THAN (2015),
  PARTITION p4 VALUES LESS THAN MAXVALUE PLACEMENT POLICY=storeonfastssd
);
```

制約は、リスト形式（ `[+disk=ssd]` ）またはディクショナリ形式（ `{+disk=ssd: 1,+disk=hdd: 2}` ）のいずれかで指定できます。

リスト形式では、制約はキーと値のペアのリストとして指定されます。キーは`+`または`-`で始まります。 `+disk=ssd`は、ラベル`disk`を`ssd`に設定する必要があることを示し、 `-disk=hdd`は、ラベル`disk`を`hdd`に設定してはならないことを示します。

ディクショナリ形式では、制約はそのルールに適用されるインスタンスの数も示します。たとえば、 `FOLLOWER_CONSTRAINTS="{+region=us-east-1: 1,+region=us-east-2: 1,+region=us-west-1: 1,+any: 1}";`は、1人のフォロワーがus-east-1にいること、1人のフォロワーがus-east-2にいること、1人のフォロワーがus-west-1にいること、1人のフォロワーが任意の地域にいることを示します。別の例では、 `FOLLOWER_CONSTRAINTS='{"+region=us-east-1,+disk=hdd":1,"+region=us-west-1":1}';`は、1人のフォロワーがhddディスクを使用してus-east-1にあり、1人のフォロワーがus-west-1にいることを示します。

> **ノート：**
>
> 辞書とリストの形式はYAMLパーサーに基づいていますが、YAML構文が正しく解析されていない可能性があります。たとえば、 `"{+disk=ssd:1,+disk=hdd:2}"`は誤って`'{"+disk=ssd:1": null, "+disk=hdd:1": null}'`として解析されます。ただし、 `"{+disk=ssd: 1,+disk=hdd: 1}"`は`'{"+disk=ssd": 1, "+disk=hdd": 1}'`として正しく解析されます。

## 既知の制限 {#known-limitations}

SQLの配置ルールの実験的リリースには、次の既知の制限があります。

-   Dumplingは、餃子配置ポリシーをサポートしていません。 [号＃29371](https://github.com/pingcap/tidb/issues/29371)を参照してください。
-   Backup＆Restore（BR）、TiCDC、TiDB Lightning、TiDB Data Migration（DM）などのTiDBツールは、配置ルールをまだサポートしていません。
-   一時テーブルは、配置オプションをサポートしていません（直接配置または配置ポリシーのいずれかを介して）。
-   設定`PRIMARY_REGION`および`REGIONS`には、構文糖衣規則が許可されています。将来的には、 `PRIMARY_RACK`の`PRIMARY_ZONE`を追加する予定`PRIMARY_HOST` 。 [号18030](https://github.com/pingcap/tidb/issues/18030)を参照してください。
-   TiFlashラーナーは、配置ルール構文では構成できません。
-   配置ルールは、保存されているデータが正しいTiKVストアに存在することのみを保証します。このルールは、転送中のデータ（ユーザークエリまたは内部操作のいずれかを介して）が特定のリージョンでのみ発生することを保証するものではありません。
