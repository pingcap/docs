---
title: Use TiFlash
---

データのインポートからTPC-Hデータセットでのクエリまでのプロセス全体を体験するには、 [TiDB HTAPのクイックスタートガイド](/quick-start-with-htap.md)を参照してください。

# TiFlashを使用する {#use-tiflash}

TiFlashがデプロイされた後、データレプリケーションは自動的に開始されません。複製するテーブルを手動で指定する必要があります。

TiDBを使用して中規模の分析処理用のTiFlashレプリカを読み取るか、TiSparkを使用して大規模な分析処理用のTiFlashレプリカを読み取ることができます。これは独自のニーズに基づいています。詳細については、次のセクションを参照してください。

-   [TiDBを使用してTiFlashレプリカを読み取る](#use-tidb-to-read-tiflash-replicas)
-   [TiSparkを使用してTiFlashレプリカを読み取ります](#use-tispark-to-read-tiflash-replicas)

## テーブルのTiFlashレプリカを作成する {#create-tiflash-replicas-for-tables}

TiFlashがTiKVクラスタに接続された後、デフォルトではデータレプリケーションは開始されません。 MySQLクライアントを介してDDLステートメントをTiDBに送信して、特定のテーブルのTiFlashレプリカを作成できます。

{{< copyable "" >}}

```sql
ALTER TABLE table_name SET TIFLASH REPLICA count;
```

上記のコマンドのパラメータは次のとおりです。

-   `count`はレプリカの数を示します。値が`0`の場合、レプリカは削除されます。

同じテーブルで複数のDDLステートメントを実行すると、最後のステートメントのみが有効になります。次の例では、2つのDDLステートメントがテーブル`tpch50`で実行されますが、2番目のステートメント（レプリカを削除するため）のみが有効になります。

テーブルのレプリカを2つ作成します。

{{< copyable "" >}}

```sql
ALTER TABLE `tpch50`.`lineitem` SET TIFLASH REPLICA 2;
```

レプリカを削除します。

{{< copyable "" >}}

```sql
ALTER TABLE `tpch50`.`lineitem` SET TIFLASH REPLICA 0;
```

**ノート：**

-   テーブル`t`が上記のDDLステートメントを介してTiFlashに複製される場合、次のステートメントを使用して作成されたテーブルも自動的にTiFlashに複製されます。

    {{< copyable "" >}}

    ```sql
    CREATE TABLE table_name like t;
    ```

-   v4.0.6より前のバージョンでは、TiDB Lightningを使用してデータをインポートする前にTiFlashレプリカを作成すると、データのインポートが失敗します。テーブルのTiFlashレプリカを作成する前に、データをテーブルにインポートする必要があります。

-   TiDBとTiDBLightningの両方がv4.0.6以降の場合、テーブルにTiFlashレプリカがあるかどうかに関係なく、TiDBLightningを使用してそのテーブルにデータをインポートできます。これにより、TiDB Lightningの手順が遅くなる可能性があることに注意してください。これは、LightningホストのNIC帯域幅、TiFlashノードのCPUとディスクの負荷、およびTiFlashレプリカの数によって異なります。

-   PDスケジューリングのパフォーマンスが低下するため、1,000を超えるテーブルを複製しないことをお勧めします。この制限は、今後のバージョンで削除される予定です。

-   v5.1以降のバージョンでは、システムテーブルのレプリカの設定はサポートされなくなりました。クラスタをアップグレードする前に、関連するシステムテーブルのレプリカをクリアする必要があります。そうしないと、クラスタを新しいバージョンにアップグレードした後、システムテーブルのレプリカ設定を変更できません。

### レプリケーションの進行状況を確認する {#check-replication-progress}

次のステートメントを使用して、特定のテーブルのTiFlashレプリカのステータスを確認できます。テーブルは`WHERE`句を使用して指定されます。 `WHERE`句を削除すると、すべてのテーブルのレプリカステータスが確認されます。

{{< copyable "" >}}

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>' and TABLE_NAME = '<table_name>';
```

上記のステートメントの結果：

-   `AVAILABLE`は、このテーブルのTiFlashレプリカが使用可能かどうかを示します。 `1`は利用可能、 `0`は利用不可を意味します。レプリカが使用可能になると、このステータスは変更されません。 DDLステートメントを使用してレプリカの数を変更すると、レプリケーションステータスが再計算されます。
-   `PROGRESS`は、レプリケーションの進行状況を意味します。値は`0.0` `1.0` 。 `1`は、少なくとも1つのレプリカが複製されることを意味します。

### 利用可能なゾーンを設定する {#set-available-zones}

レプリカを構成するときに、ディザスタリカバリのためにTiFlashレプリカを複数のデータセンターに配布する必要がある場合は、以下の手順に従って使用可能なゾーンを構成できます。

1.  クラスタ構成ファイルでTiFlashノードのラベルを指定します。

    ```
    tiflash_servers:
      - host: 172.16.5.81
        config:
          flash.proxy.labels: zone=z1
      - host: 172.16.5.82
        config:
          flash.proxy.labels: zone=z1
      - host: 172.16.5.85
        config:
          flash.proxy.labels: zone=z2
    ```

2.  クラスタを起動した後、レプリカを作成するときにラベルを指定します。

    {{< copyable "" >}}

    ```sql
    ALTER TABLE table_name SET TIFLASH REPLICA count LOCATION LABELS location_labels;
    ```

    例えば：

    {{< copyable "" >}}

    ```sql
    ALTER TABLE t SET TIFLASH REPLICA 2 LOCATION LABELS "zone";
    ```

3.  PDは、ラベルに基づいてレプリカをスケジュールします。この例では、PDはそれぞれテーブル`t`の2つのレプリカを2つの使用可能なゾーンにスケジュールします。 pd-ctlを使用してスケジュールを表示できます。

    ```shell
    > tiup ctl:<version> pd -u<pd-host>:<pd-port> store

        ...
        "address": "172.16.5.82:23913",
        "labels": [
          { "key": "engine", "value": "tiflash"},
          { "key": "zone", "value": "z1" }
        ],
        "region_count": 4,

        ...
        "address": "172.16.5.81:23913",
        "labels": [
          { "key": "engine", "value": "tiflash"},
          { "key": "zone", "value": "z1" }
        ],
        "region_count": 5,
        ...

        "address": "172.16.5.85:23913",
        "labels": [
          { "key": "engine", "value": "tiflash"},
          { "key": "zone", "value": "z2" }
        ],
        "region_count": 9,
        ...
    ```

ラベルを使用したレプリカのスケジューリングの詳細については、 [トポロジラベルによるレプリカのスケジュール](/schedule-replicas-by-topology-labels.md) 、および[1 つの地域展開における複数のデータセンター](/multi-data-centers-in-one-city-deployment.md)を参照して[2つの都市に配置された3つのデータセンター](/three-data-centers-in-two-cities-deployment.md) 。

## TiDBを使用してTiFlashレプリカを読み取る {#use-tidb-to-read-tiflash-replicas}

TiDBは、TiFlashレプリカを読み取る3つの方法を提供します。エンジン構成なしでTiFlashレプリカを追加した場合、デフォルトでCBO（コストベースの最適化）モードが使用されます。

### スマートセレクション {#smart-selection}

TiFlashレプリカを含むテーブルの場合、TiDBオプティマイザは、コスト見積もりに基づいてTiFlashレプリカを使用するかどうかを自動的に決定します。 `desc`または`explain analyze`ステートメントを使用して、TiFlashレプリカが選択されているかどうかを確認できます。例えば：

{{< copyable "" >}}

```sql
desc select count(*) from test.t;
```

```
+--------------------------+---------+--------------+---------------+--------------------------------+
| id                       | estRows | task         | access object | operator info                  |
+--------------------------+---------+--------------+---------------+--------------------------------+
| StreamAgg_9              | 1.00    | root         |               | funcs:count(1)->Column#4       |
| └─TableReader_17         | 1.00    | root         |               | data:TableFullScan_16          |
|   └─TableFullScan_16     | 1.00    | cop[tiflash] | table:t       | keep order:false, stats:pseudo |
+--------------------------+---------+--------------+---------------+--------------------------------+
3 rows in set (0.00 sec)
```

{{< copyable "" >}}

```sql
explain analyze select count(*) from test.t;
```

```
+--------------------------+---------+---------+--------------+---------------+----------------------------------------------------------------------+--------------------------------+-----------+------+
| id                       | estRows | actRows | task         | access object | execution info                                                       | operator info                  | memory    | disk |
+--------------------------+---------+---------+--------------+---------------+----------------------------------------------------------------------+--------------------------------+-----------+------+
| StreamAgg_9              | 1.00    | 1       | root         |               | time:83.8372ms, loops:2                                              | funcs:count(1)->Column#4       | 372 Bytes | N/A  |
| └─TableReader_17         | 1.00    | 1       | root         |               | time:83.7776ms, loops:2, rpc num: 1, rpc time:83.5701ms, proc keys:0 | data:TableFullScan_16          | 152 Bytes | N/A  |
|   └─TableFullScan_16     | 1.00    | 1       | cop[tiflash] | table:t       | time:43ms, loops:1                                                   | keep order:false, stats:pseudo | N/A       | N/A  |
+--------------------------+---------+---------+--------------+---------------+----------------------------------------------------------------------+--------------------------------+-----------+------+
```

`cop[tiflash]`は、タスクが処理のためにTiFlashに送信されることを意味します。 TiFlashレプリカを選択していない場合は、 `analyze table`ステートメントを使用して統計を更新し、 `explain analyze`ステートメントを使用して結果を確認できます。

テーブルにTiFlashレプリカが1つしかなく、関連ノードがサービスを提供できない場合、CBOモードのクエリは繰り返し再試行することに注意してください。この状況では、エンジンを指定するか、手動ヒントを使用してTiKVレプリカからデータを読み取る必要があります。

### エンジンの分離 {#engine-isolation}

エンジンの分離とは、対応する変数を構成することにより、すべてのクエリが指定されたエンジンのレプリカを使用するように指定することです。オプションのエンジンは、「tikv」、「tidb」（一部のTiDBシステムテーブルを格納し、ユーザーがアクティブに使用できないTiDBの内部メモリテーブル領域を示します）、および「tiflash」で、次の2つの構成レベルがあります。

-   TiDBインスタンスレベル、つまりINSTANCEレベル。 TiDB構成ファイルに次の構成項目を追加します。

    ```
    [isolation-read]
    engines = ["tikv", "tidb", "tiflash"]
    ```

    **INSTANCEレベルのデフォルト構成は`[&quot;tikv&quot;, &quot;tidb&quot;, &quot;tiflash&quot;]`です。**

-   SESSIONレベル。次のステートメントを使用して構成します。

    {{< copyable "" >}}

    ```sql
    set @@session.tidb_isolation_read_engines = "engine list separated by commas";
    ```

    また

    {{< copyable "" >}}

    ```sql
    set SESSION tidb_isolation_read_engines = "engine list separated by commas";
    ```

    SESSIONレベルのデフォルト構成は、TiDBINSTANCEレベルの構成を継承します。

最終的なエンジン構成はセッションレベルの構成です。つまり、セッションレベルの構成はインスタンスレベルの構成をオーバーライドします。たとえば、INSTANCEレベルで「tikv」を構成し、SESSIONレベルで「tiflash」を構成した場合、TiFlashレプリカが読み取られます。最終的なエンジン構成が「tikv」と「tiflash」の場合、TiKVとTiFlashのレプリカが両方とも読み取られ、オプティマイザーは実行するのに適したエンジンを自動的に選択します。

> **ノート：**
>
> [TiDBダッシュボード](/dashboard/dashboard-intro.md)およびその他のコンポーネントは、TiDBメモリテーブル領域に格納されている一部のシステムテーブルを読み取る必要があるため、常に「tidb」エンジンをインスタンスレベルのエンジン構成に追加することをお勧めします。

照会されたテーブルに指定されたエンジンのレプリカがない場合（たとえば、エンジンが「tiflash」として構成されているが、テーブルにTiFlashレプリカがない場合）、クエリはエラーを返します。

### 手動ヒント {#manual-hint}

手動のヒントにより、TiDBは、エンジンの分離を満たすことを前提として、特定のテーブルに指定されたレプリカを使用するように強制できます。手動ヒントの使用例を次に示します。

{{< copyable "" >}}

```sql
select /*+ read_from_storage(tiflash[table_name]) */ ... from table_name;
```

クエリステートメントでテーブルにエイリアスを設定する場合は、ヒントを有効にするためのヒントを含むエイリアスをステートメントで使用する必要があります。例えば：

{{< copyable "" >}}

```sql
select /*+ read_from_storage(tiflash[alias_a,alias_b]) */ ... from table_name_1 as alias_a, table_name_2 as alias_b where alias_a.column_1 = alias_b.column_2;
```

上記のステートメントで、 `tiflash[]`はオプティマイザにTiFlashレプリカを読み取るように促します。 `tikv[]`を使用して、必要に応じてオプティマイザにTiKVレプリカを読み取るように求めることもできます。ヒント構文の詳細については、 [READ_FROM_STORAGE](/optimizer-hints.md#read_from_storagetiflasht1_name--tl_name--tikvt2_name--tl_name-)を参照してください。

ヒントで指定されたテーブルに指定されたエンジンのレプリカがない場合、ヒントは無視され、警告が報告されます。さらに、ヒントはエンジン分離の前提でのみ有効になります。ヒントで指定されたエンジンがエンジン分離リストにない場合、ヒントも無視され、警告が報告されます。

> **ノート：**
>
> 5.7.7以前のバージョンのMySQLクライアントは、デフォルトでオプティマイザヒントをクリアします。これらの初期バージョンでヒント構文を使用するには、 `--comments`オプション（たとえば、 `mysql -h 127.0.0.1 -P 4000 -uroot --comments` ）でクライアントを起動します。

### スマートセレクション、エンジン分離、および手動ヒントの関係 {#the-relationship-of-smart-selection-engine-isolation-and-manual-hint}

上記の3つのTiFlashレプリカの読み取り方法では、エンジン分離により、エンジンの使用可能なレプリカの全体的な範囲が指定されます。この範囲内で、手動ヒントは、よりきめ細かいステートメントレベルおよびテーブルレベルのエンジン選択を提供します。最後に、CBOが決定を下し、指定されたエンジンリスト内のコスト見積もりに基づいてエンジンのレプリカを選択します。

> **ノート：**
>
> `UPDATE ...`より前では、非読み取り専用SQLステートメント（たとえば、 `INSERT INTO ... SELECT` ）での`SELECT ... FOR UPDATE`レプリカからの読み取りの`DELETE ...`は定義されていません。 v4.0.3以降のバージョンでは、内部的にTiDBは非読み取り専用SQLステートメントのTiFlashレプリカを無視して、データの正確性を保証します。つまり、 [スマートセレクション](#smart-selection)の場合、TiDBは非TiFlashレプリカを自動的に選択します。 TiFlashレプリカ**のみ**を指定する[エンジンの分離](#engine-isolation)の場合、TiDBはエラーを報告します。 [手動ヒント](#manual-hint)の場合、TiDBはヒントを無視します。

## TiSparkを使用してTiFlashレプリカを読み取ります {#use-tispark-to-read-tiflash-replicas}

現在、TiSparkを使用して、TiDBのエンジン分離と同様の方法でTiFlashレプリカを読み取ることができます。この方法は、 `spark.tispark.isolation_read_engines`つのパラメーターを構成するためのものです。パラメータ値のデフォルトは`tikv,tiflash`です。これは、TiDBがCBOの選択に従ってTiFlashまたはTiKVからデータを読み取ることを意味します。パラメータ値を`tiflash`に設定すると、TiDBがTiFlashからデータを強制的に読み取ることを意味します。

> **ノート**
>
> このパラメーターが`tiflash`に設定されている場合、クエリに関係するすべてのテーブルのTiFlashレプリカのみが読み取られ、これらのテーブルにはTiFlashレプリカが必要です。 TiFlashレプリカがないテーブルの場合、エラーが報告されます。このパラメーターが`tikv`に設定されている場合、TiKVレプリカのみが読み取られます。

このパラメーターは、次のいずれかの方法で構成できます。

-   `spark-defaults.conf`のファイルに次の項目を追加します。

    ```
    spark.tispark.isolation_read_engines tiflash
    ```

-   SparkシェルまたはThriftサーバーを初期化するときに、初期化コマンドに`--conf spark.tispark.isolation_read_engines=tiflash`を追加します。

-   リアルタイムでSparkシェルに`spark.conf.set("spark.tispark.isolation_read_engines", "tiflash")`を設定します。

-   サーバーがbeeline経由で接続された後、Thriftサーバーに`set spark.tispark.isolation_read_engines=tiflash`を設定します。

## サポートされているプッシュダウン計算 {#supported-push-down-calculations}

TiFlashは、次の演算子のプッシュダウンをサポートしています。

-   TableScan：テーブルからデータを読み取ります。
-   選択：データをフィルタリングします。
-   HashAgg： [ハッシュ集計](/explain-aggregation.md#hash-aggregation)アルゴリズムに基づいてデータ集約を実行します。
-   StreamAgg： [ストリーム集計](/explain-aggregation.md#stream-aggregation)のアルゴリズムに基づいてデータ集約を実行します。 SteamAggは、 `GROUP BY`の条件なしで集約のみをサポートします。
-   TopN：TopN計算を実行します。
-   制限：制限計算を実行します。
-   プロジェクト：投影計算を実行します。
-   HashJoin（Equi Join）： [ハッシュ参加](/explain-joins.md#hash-join)アルゴリズムに基づいて結合計算を実行しますが、次の条件があります。
    -   オペレーターは[MPPモード](#use-the-mpp-mode)でのみ押し下げることができます。
    -   `Full Outer Join`のプッシュダウンはサポートされていません。
-   HashJoin（非等結合）：デカルト結合アルゴリズムを実行しますが、次の条件があります。
    -   オペレーターは[MPPモード](#use-the-mpp-mode)でのみ押し下げることができます。
    -   デカルト結合は、ブロードキャスト結合でのみサポートされます。

TiDBでは、演算子はツリー構造で編成されています。オペレーターをTiFlashにプッシュダウンするには、次のすべての前提条件が満たされている必要があります。

-   その子演算子はすべてTiFlashにプッシュダウンできます。
-   演算子に式が含まれている場合（ほとんどの演算子に式が含まれている場合）、演算子のすべての式をTiFlashにプッシュダウンできます。

現在、TiFlashは次のプッシュダウン式をサポートしています。

-   数学関数： `+, -, /, *, %, >=, <=, =, !=, <, >, round, abs, floor(int), ceil(int), ceiling(int), sqrt, log, log2, log10, ln, exp, pow, sign, radians, degrees, conv, crc32`
-   論理関数： `and, or, not, case when, if, ifnull, isnull, in, like, coalesce`
-   ビット演算： `bitand, bitor, bigneg, bitxor`
-   文字列関数： `substr, char_length, replace, concat, concat_ws, left, right, ascii, length, trim, ltrim, rtrim, position, format, lower, ucase, upper, substring_index, lpad, rpad, strcmp`
-   日付関数： `date_format, timestampdiff, from_unixtime, unix_timestamp(int), unix_timestamp(decimal), str_to_date(date), str_to_date(datetime), datediff, year, month, day, extract(datetime), date, hour, microsecond, minute, second, sysdate, date_add, date_sub, adddate, subdate, quarter`
-   JSON関数： `json_length`
-   変換機能： `cast(int as double), cast(int as decimal), cast(int as string), cast(int as time), cast(double as int), cast(double as decimal), cast(double as string), cast(double as time), cast(string as int), cast(string as double), cast(string as decimal), cast(string as time), cast(decimal as int), cast(decimal as string), cast(decimal as time), cast(time as int), cast(time as decimal), cast(time as string), cast(time as real)`
-   集計関数： `min, max, sum, count, avg, approx_count_distinct, group_concat`
-   その他の機能： `inetntoa, inetaton, inet6ntoa, inet6aton`

### その他の制限 {#other-restrictions}

-   Bit、Set、およびGeometryタイプを含む式は、TiFlashにプッシュダウンできません。

-   `date_add` 、 `subdate` `date_sub`は、次の間隔タイプのみをサポートし`adddate` 。他の間隔タイプが使用されている場合、TiFlashはエラーを報告します。

    -   日
    -   週
    -   月
    -   年
    -   時間
    -   分
    -   2番目

クエリでサポートされていないプッシュダウン計算が発生した場合、TiDBは残りの計算を完了する必要があります。これは、TiFlashアクセラレーション効果に大きな影響を与える可能性があります。現在サポートされていない演算子と式は、将来のバージョンでサポートされる可能性があります。

## MPPモードを使用する {#use-the-mpp-mode}

TiFlashは、MPPモードを使用したクエリの実行をサポートします。これにより、ノード間のデータ交換（データシャッフルプロセス）が計算に導入されます。 TiDBは、オプティマイザのコスト見積もりを使用して、MPPモードを選択するかどうかを自動的に決定します。 [`tidb_allow_mpp`](/system-variables.md#tidb_allow_mpp-new-in-v50)と[`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-new-in-v51)の値を変更することにより、選択戦略を変更できます。

### MPPモードを選択するかどうかを制御します {#control-whether-to-select-the-mpp-mode}

`tidb_allow_mpp`変数は、TiDBがクエリを実行するためにMPPモードを選択できるかどうかを制御します。 `tidb_enforce_mpp`変数は、オプティマイザーのコスト見積もりを無視するかどうかを制御し、TiFlashのMPPモードを使用してクエリを強制的に実行します。

これら2つの変数のすべての値に対応する結果は次のとおりです。

|                               | tidb_allow_mpp = off | tidb_allow_mpp = on（デフォルト）                 |
| ----------------------------- | -------------------- | ------------------------------------------ |
| tidb_enforce_mpp = off（デフォルト） | MPPモードは使用されません。      | オプティマイザは、コスト見積もりに基づいてMPPモードを選択します。 （デフォルト） |
| tidb_enforce_mpp = on         | MPPモードは使用されません。      | TiDBはコスト見積もりを無視し、MPPモードを選択します。             |

たとえば、MPPモードを使用したくない場合は、次のステートメントを実行できます。

{{< copyable "" >}}

```sql
set @@session.tidb_allow_mpp=1;
set @@session.tidb_enforce_mpp=0;
```

TiDBのコストベースのオプティマイザでMPPモード（デフォルト）を使用するかどうかを自動的に決定する場合は、次のステートメントを実行できます。

{{< copyable "" >}}

```sql
set @@session.tidb_allow_mpp=1;
set @@session.tidb_enforce_mpp=0;
```

TiDBでオプティマイザのコスト見積もりを無視し、MPPモードを強制的に選択する場合は、次のステートメントを実行できます。

{{< copyable "" >}}

```sql
set @@session.tidb_allow_mpp=1;
set @@session.tidb_enforce_mpp=1;
```

`tidb_enforce_mpp`セッション変数の初期値は、このtidb-serverインスタンスの[`enforce-mpp`](/tidb-configuration-file.md#enforce-mpp)構成値（デフォルトでは`false` ）と同じです。 TiDBクラスタの複数のtidb-serverインスタンスが分析クエリのみを実行し、これらのインスタンスでMPPモードが使用されていることを確認する場合は、 [`enforce-mpp`](/tidb-configuration-file.md#enforce-mpp)の構成値を`true`に変更できます。

> **ノート：**
>
> `tidb_enforce_mpp=1`が有効になると、TiDBオプティマイザはコスト見積もりを無視してMPPモードを選択します。ただし、他の要因がMPPモードをブロックしている場合、TiDBはMPPモードを選択しません。これらの要因には、TiFlashレプリカの欠如、TiFlashレプリカの未完成の複製、およびMPPモードでサポートされていない演算子または関数を含むステートメントが含まれます。
>
> コスト見積もり以外の理由でTiDBオプティマイザがMPPモードを選択できない場合、 `EXPLAIN`ステートメントを使用して実行プランをチェックアウトすると、理由を説明する警告が返されます。例えば：
>
> {{< copyable "" >}}
>
> ```sql
> set @@session.tidb_enforce_mpp=1;
> create table t(a int);
> explain select count(*) from t;
> show warnings;
> ```
>
> ```
> +---------+------+-----------------------------------------------------------------------------+
> | Level   | Code | Message                                                                     |
> +---------+------+-----------------------------------------------------------------------------+
> | Warning | 1105 | MPP mode may be blocked because there aren't tiflash replicas of table `t`. |
> +---------+------+-----------------------------------------------------------------------------+
> ```

### MPPモードのアルゴリズムサポート {#algorithm-support-for-the-mpp-mode}

MPPモードは、ブロードキャストハッシュ結合、シャッフルハッシュ結合、シャッフルハッシュ集計、Union All、TopN、およびLimitの物理アルゴリズムをサポートします。オプティマイザは、クエリで使用するアルゴリズムを自動的に決定します。特定のクエリ実行プランを確認するには、 `EXPLAIN`ステートメントを実行します。 `EXPLAIN`ステートメントの結果にExchangeSenderおよびExchangeReceiver演算子が表示されている場合は、MPPモードが有効になっていることを示しています。

次のステートメントは、TPC-Hテストセットのテーブル構造を例として取り上げています。

```sql
explain select count(*) from customer c join nation n on c.c_nationkey=n.n_nationkey;
+------------------------------------------+------------+-------------------+---------------+----------------------------------------------------------------------------+
| id                                       | estRows    | task              | access object | operator info                                                              |
+------------------------------------------+------------+-------------------+---------------+----------------------------------------------------------------------------+
| HashAgg_23                               | 1.00       | root              |               | funcs:count(Column#16)->Column#15                                          |
| └─TableReader_25                         | 1.00       | root              |               | data:ExchangeSender_24                                                     |
|   └─ExchangeSender_24                    | 1.00       | batchCop[tiflash] |               | ExchangeType: PassThrough                                                  |
|     └─HashAgg_12                         | 1.00       | batchCop[tiflash] |               | funcs:count(1)->Column#16                                                  |
|       └─HashJoin_17                      | 3000000.00 | batchCop[tiflash] |               | inner join, equal:[eq(tpch.nation.n_nationkey, tpch.customer.c_nationkey)] |
|         ├─ExchangeReceiver_21(Build)     | 25.00      | batchCop[tiflash] |               |                                                                            |
|         │ └─ExchangeSender_20            | 25.00      | batchCop[tiflash] |               | ExchangeType: Broadcast                                                    |
|         │   └─TableFullScan_18           | 25.00      | batchCop[tiflash] | table:n       | keep order:false                                                           |
|         └─TableFullScan_22(Probe)        | 3000000.00 | batchCop[tiflash] | table:c       | keep order:false                                                           |
+------------------------------------------+------------+-------------------+---------------+----------------------------------------------------------------------------+
9 rows in set (0.00 sec)
```

実行プランの例には、 `ExchangeReceiver`と`ExchangeSender`の演算子が含まれています。実行プランは、 `nation`テーブルが読み取られた後、 `ExchangeSender`オペレーターがテーブルを各ノードにブロードキャストし、 `HashJoin`および`HashAgg`操作が`nation`テーブルと`customer`テーブルで実行され、結果がTiDBに返されることを示しています。

TiFlashは、ブロードキャストハッシュ結合を使用するかどうかを制御するために、次の2つのグローバル/セッション変数を提供します。

-   [`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50) ：値の単位はバイトです。テーブルサイズ（バイト単位）が変数の値よりも小さい場合は、ブロードキャストハッシュ結合アルゴリズムが使用されます。それ以外の場合は、シャッフルハッシュ結合アルゴリズムが使用されます。
-   [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50) ：値の単位は行です。結合操作のオブジェクトがサブクエリに属している場合、オプティマイザはサブクエリ結果セットのサイズを推定できないため、サイズは結果セットの行数によって決定されます。サブクエリの推定行数がこの変数の値よりも少ない場合は、ブロードキャストハッシュ結合アルゴリズムが使用されます。それ以外の場合は、シャッフルハッシュ結合アルゴリズムが使用されます。

## データ検証 {#data-validation}

### ユーザーシナリオ {#user-scenarios}

データの破損は通常、深刻なハードウェア障害によって引き起こされます。このような場合、手動でデータを回復しようとしても、データの信頼性が低下します。

データの整合性を確保するために、デフォルトでは、TiFlashは`City128`アルゴリズムを使用してデータファイルに対して基本的なデータ検証を実行します。データ検証に失敗した場合、TiFlashはすぐにエラーを報告して終了し、一貫性のないデータによって引き起こされる二次的な災害を回避します。このとき、TiFlashノードを復元する前に、手動で介入してデータを再度複製する必要があります。

v5.4.0以降、TiFlashはより高度なデータ検証機能を導入しています。 TiFlashはデフォルトで`XXH3`アルゴリズムを使用し、検証フレームとアルゴリズムをカスタマイズできます。

### 検証メカニズム {#validation-mechanism}

検証メカニズムは、DeltaTreeファイル（DTFile）に基づいて構築されています。 DTFileは、TiFlashデータを保持するストレージファイルです。 DTFileには次の3つの形式があります。

| バージョン | 州        | 検証メカニズム                                                   | ノート                       |
| :---- | :------- | :-------------------------------------------------------- | :------------------------ |
| V1    | 非推奨      | ハッシュはデータファイルに埋め込まれています。                                   |                           |
| V2    | デフォルト    | ハッシュはデータファイルに埋め込まれています。                                   | V1と比較して、V2は列データの統計を追加します。 |
| V3    | 手動で有効にする | V3には、メタデータとトークンデータのチェックサムが含まれており、複数のハッシュアルゴリズムをサポートしています。 | v5.4.0の新機能。               |

DTFileは、データファイルディレクトリの`stable`フォルダに保存されます。現在有効になっているすべての形式はフォルダ形式です。つまり、データは`dmf_<file id>`のような名前のフォルダの下にある複数のファイルに保存されます。

#### データ検証を使用する {#use-data-validation}

TiFlashは、自動データ検証と手動データ検証の両方をサポートしています。

-   自動データ検証：
    -   TiFlashは、デフォルトでV2検証メカニズムを有効にします。
    -   V3検証メカニズムを有効にするには、 [TiFlash構成ファイル](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)を参照してください。
-   手動データ検証。 [`DTTool inspect`](/tiflash/tiflash-command-line-flags.md#dttool-inspect)を参照してください。

> **警告：**
>
> V3検証メカニズムを有効にすると、新しく生成されたDTFileをv5.4.0より前のTiFlashで直接読み取ることはできません。 v5.4.0以降、TiFlashはV2とV3の両方をサポートし、バージョンをアクティブにアップグレードまたはダウングレードしません。既存のファイルのバージョンをアップグレードまたはダウングレードする必要がある場合は、手動で[バージョンの切り替え](/tiflash/tiflash-command-line-flags.md#dttool-migrate)を実行する必要があります。

#### 検証ツール {#validation-tool}

TiFlashがデータを読み取るときに実行される自動データ検証に加えて、データの整合性を手動でチェックするためのツールがv5.4.0で導入されています。詳しくは[DTTool](/tiflash/tiflash-command-line-flags.md#dttool-inspect)をご覧ください。

## ノート {#notes}

次の状況では、TiFlashはTiDBと互換性がありません。

-   TiFlash計算レイヤー：
    -   オーバーフローした数値のチェックはサポートされていません。たとえば、 `BIGINT`タイプ`9223372036854775807 + 9223372036854775807`の2つの最大値を追加します。 TiDBでのこの計算の予想される動作は、 `ERROR 1690 (22003): BIGINT value is out of range`エラーを返すことです。ただし、この計算をTiFlashで実行すると、オーバーフロー値`-2`がエラーなしで返されます。
    -   ウィンドウ関数はサポートされていません。
    -   TiKVからのデータの読み取りはサポートされていません。
    -   現在、TiFlashの`sum`関数は文字列型引数をサポートしていません。ただし、TiDBは、コンパイル中に文字列型の引数が`sum`関数に渡されたかどうかを識別できません。したがって、 `select sum(string_col) from t`と同様のステートメントを実行すると、TiFlashは`[FLASH:Coprocessor:Unimplemented] CastStringAsReal is not supported.`エラーを返します。この場合のこのようなエラーを回避するには、このSQLステートメントを`select sum(cast(string_col as double)) from t`に変更する必要があります。
    -   現在、TiFlashの小数除算の計算はTiDBの計算と互換性がありません。たとえば、小数を除算する場合、TiFlashは常にコンパイルから推測されたタイプを使用して計算を実行します。ただし、TiDBは、コンパイルから推測されるタイプよりも正確なタイプを使用してこの計算を実行します。したがって、10進数の除算を含む一部のSQLステートメントは、TiDB+TiKVとTiDB+TiFlashで実行されたときに異なる実行結果を返します。例えば：

        ```sql
        mysql> create table t (a decimal(3,0), b decimal(10, 0));
        Query OK, 0 rows affected (0.07 sec)
        mysql> insert into t values (43, 1044774912);
        Query OK, 1 row affected (0.03 sec)
        mysql> alter table t set tiflash replica 1;
        Query OK, 0 rows affected (0.07 sec)
        mysql> set session tidb_isolation_read_engines='tikv';
        Query OK, 0 rows affected (0.00 sec)
        mysql> select a/b, a/b + 0.0000000000001 from t where a/b;
        +--------+-----------------------+
        | a/b    | a/b + 0.0000000000001 |
        +--------+-----------------------+
        | 0.0000 |       0.0000000410001 |
        +--------+-----------------------+
        1 row in set (0.00 sec)
        mysql> set session tidb_isolation_read_engines='tiflash';
        Query OK, 0 rows affected (0.00 sec)
        mysql> select a/b, a/b + 0.0000000000001 from t where a/b;
        Empty set (0.01 sec)
        ```

        上記の例では、コンパイルから推測される`a/b`の型は、TiDBとTiFlashの両方で`Decimal(7,4)`です。 `Decimal(7,4)`によって制約され、 `a/b`の返されるタイプは`0.0000`である必要があります。 TiDBでは、 `a/b`の実行時精度は`Decimal(7,4)`よりも高いため、元のテーブルデータは`where a/b`条件によってフィルタリングされません。ただし、TiFlashでは、 `a/b`の計算では結果タイプとして`Decimal(7,4)`が使用されるため、元のテーブルデータは`where a/b`条件でフィルタリングされます。
