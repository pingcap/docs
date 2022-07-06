---
title: Placement Rules
summary: Learn how to configure Placement Rules.
---

# 配置ルール {#placement-rules}

> **ノート：**
>
> このドキュメントでは、配置ドライバ（PD）で配置ルールを手動で指定する方法を紹介します。現在、 [SQLの配置ルール](/placement-rules-in-sql.md)を使用することをお勧めします。これにより、テーブルとパーティションの配置を構成するためのより便利な方法が提供されます。

v5.0で導入された配置ルールは、PDがさまざまなタイプのデータに対応するスケジュールを生成するようにガイドするレプリカルールシステムです。さまざまなスケジューリングルールを組み合わせることで、レプリカの数、保存場所、ホストタイプ、Raft選挙に参加するかどうか、Raftリーダーとして機能するかどうかなど、任意の連続データ範囲の属性を細かく制御できます。

配置ルール機能は、v5.0以降のバージョンのTiDBではデフォルトで有効になっています。無効にするには、 [配置ルールを無効にする](#disable-placement-rules)を参照してください。

## ルールシステム {#rule-system}

ルールシステム全体の構成は、複数のルールで構成されています。各ルールは、レプリカの数、ラフトの役割、配置場所、このルールが有効になるキー範囲などの属性を指定できます。 PDがスケジュールを実行しているとき、PDはまず、リージョンのキー範囲に従ってルールシステム内のリージョンに対応するルールを見つけ、次に対応するスケジュールを生成して、リージョンレプリカの配布をルールに準拠させます。

複数のルールのキー範囲は重複する部分を持つ可能性があります。つまり、リージョンは複数のルールに一致する可能性があります。この場合、PDは、ルールの属性に応じて、ルールが相互に上書きするか、同時に有効になるかを決定します。複数のルールが同時に有効になる場合、PDはルールマッチングのルールのスタック順序に従って順番にスケジュールを生成します。

さらに、さまざまなソースからのルールを相互に分離するという要件を満たすために、これらのルールをより柔軟な方法で編成できます。そこで、「グループ」の概念を紹介します。一般に、ユーザーはさまざまなソースに応じてさまざまなグループにルールを配置できます。

![Placement rules overview](/media/placement-rules-1.png)

### ルールフィールド {#rule-fields}

次の表は、ルールの各フィールドの意味を示しています。

| フィールド名            | タイプと制限         | 説明                                 |
| :---------------- | :------------- | :--------------------------------- |
| `GroupID`         | `string`       | ルールのソースをマークするグループID。               |
| `ID`              | `string`       | グループ内のルールの一意のID。                   |
| `Index`           | `int`          | グループ内のルールのスタックシーケンス。               |
| `Override`        | `true` `false` | ルールを（グループ内の）より小さなインデックスで上書きするかどうか。 |
| `StartKey`        | `string`進形式    | 範囲の開始キーに適用されます。                    |
| `EndKey`          | `string`進形式    | 範囲の終了キーに適用されます。                    |
| `Role`            | `string`       | リーダー/フォロワー/学習者を含むレプリカの役割。          |
| `Count`           | `int` 、正の整数    | レプリカの数。                            |
| `LabelConstraint` | `[]Constraint` | ラベルに基づくファイラーノード。                   |
| `LocationLabels`  | `[]string`     | 物理的な分離に使用されます。                     |
| `IsolationLevel`  | `string`       | 最小の物理的分離レベルを設定するために使用されます          |

`LabelConstraint`は、 `in` 、および`notExists`の`notIn` `exists`のプリミティブに基づいてラベルをフィルタリングするKubernetesの関数に似ています。これらの4つのプリミティブの意味は次のとおりです。

-   `in` ：指定されたキーのラベル値が指定されたリストに含まれます。
-   `notIn` ：指定されたキーのラベル値は指定されたリストに含まれていません。
-   `exists` ：指定されたラベルキーを含みます。
-   `notExists` ：指定されたラベルキーは含まれません。

`LocationLabels`の意味と機能は、v4.0より前のものと同じです。たとえば、3層トポロジを定義する`[zone,rack,host]`をデプロイした場合、クラスタには複数のゾーン（可用性ゾーン）があり、各ゾーンには複数のラックがあり、各ラックには複数のホストがあります。スケジュールを実行するとき、PDは最初にリージョンのピアを異なるゾーンに配置しようとします。この試行が失敗した場合（レプリカが3つあるが、合計でゾーンが2つしかない場合など）、PDはこれらのレプリカを異なるラックに配置することを保証します。ラックの数が分離を保証するのに十分でない場合、PDはホストレベルの分離を試みます。

`IsolationLevel`の意味と機能は[クラスタートポロジ構成](/schedule-replicas-by-topology-labels.md)で詳しく説明されています。たとえば、 `LocationLabels`で3層トポロジを定義し、 `IsolationLevel`を`zone`に設定する`[zone,rack,host]`を展開した場合、PDは、スケジューリング中に各リージョンのすべてのピアが異なるゾーンに配置されるようにします。 `IsolationLevel`の最小分離レベル制限を満たすことができない場合（たとえば、3つのレプリカが構成されているが、合計で2つのデータゾーンしかない場合）、PDはこの制限を満たすことを試みません。デフォルト値の`IsolationLevel`は空の文字列です。これは、無効になっていることを意味します。

### ルールグループのフィールド {#fields-of-the-rule-group}

次の表に、ルールグループの各フィールドの説明を示します。

| フィールド名     | タイプと制限         | 説明                            |
| :--------- | :------------- | :---------------------------- |
| `ID`       | `string`       | ルールのソースをマークするグループID。          |
| `Index`    | `int`          | 異なるグループのスタックシーケンス。            |
| `Override` | `true` `false` | インデックスが小さいグループをオーバーライドするかどうか。 |

## ルールを構成する {#configure-rules}

このセクションの操作は[pd-ctl](/pd-control.md)に基づいており、操作に関連するコマンドはHTTPAPIを介した呼び出しもサポートしています。

### 配置ルールを有効にする {#enable-placement-rules}

配置ルール機能は、v5.0以降のバージョンのTiDBではデフォルトで有効になっています。無効にするには、 [配置ルールを無効にする](#disable-placement-rules)を参照してください。無効にした後でこの機能を有効にするには、クラスタを初期化する前に、PD構成ファイルを次のように変更できます。

{{< copyable "" >}}

```toml
[replication]
enable-placement-rules = true
```

このように、PDは、クラスタが正常にブートストラップされた後にこの機能を有効にし、 `max-replicas`および`location-labels`の構成に従って対応するルールを生成します。

{{< copyable "" >}}

```json
{
  "group_id": "pd",
  "id": "default",
  "start_key": "",
  "end_key": "",
  "role": "voter",
  "count": 3,
  "location_labels": ["zone", "rack", "host"],
  "isolation_level": ""
}
```

ブートストラップクラスタの場合、pd-ctlを使用してオンラインで配置ルールを有効にすることもできます。

{{< copyable "" >}}

```bash
pd-ctl config placement-rules enable
```

PDは、 `max-replicas`および`location-labels`の構成に基づいてデフォルトのルールも生成します。

> **ノート：**
>
> 配置ルールを有効にすると、以前に構成した`max-replicas`と`location-labels`は有効になりません。レプリカポリシーを調整するには、配置ルールに関連するインターフェイスを使用します。

### 配置ルールを無効にする {#disable-placement-rules}

pd-ctlを使用して、配置ルール機能を無効にし、以前のスケジューリング戦略に切り替えることができます。

{{< copyable "" >}}

```bash
pd-ctl config placement-rules disable
```

> **ノート：**
>
> 配置ルールを無効にした後、PDは元の`max-replicas`および`location-labels`構成を使用します。ルールを変更すると（配置ルールが有効になっている場合）、これら2つの構成はリアルタイムで更新されません。さらに、構成されたすべてのルールはPDに残り、次に配置ルールを有効にしたときに使用されます。

### pd-ctlを使用してルールを設定する {#set-rules-using-pd-ctl}

> **ノート：**
>
> ルールの変更は、リアルタイムのPDスケジューリングに影響します。ルール設定が不適切な場合、レプリカが少なくなり、システムの高可用性に影響を与える可能性があります。

pd-ctlは、次のメソッドを使用してシステム内のルールを表示することをサポートしており、出力はJSON形式のルールまたはルールリストです。

-   すべてのルールのリストを表示するには：

    {{< copyable "" >}}

    ```bash
    pd-ctl config placement-rules show
    ```

-   PDグループ内のすべてのルールのリストを表示するには：

    {{< copyable "" >}}

    ```bash
    pd-ctl config placement-rules show --group=pd
    ```

-   グループ内の特定のIDのルールを表示するには：

    {{< copyable "" >}}

    ```bash
    pd-ctl config placement-rules show --group=pd --id=default
    ```

-   リージョンに一致するルールリストを表示するには：

    {{< copyable "" >}}

    ```bash
    pd-ctl config placement-rules show --region=2
    ```

    上記の例では、 `2`はリージョンIDです。

ルールの追加とルールの編集は似ています。対応するルールをファイルに書き込んでから、 `save`コマンドを使用してルールをPDに保存する必要があります。

{{< copyable "" >}}

```bash
cat > rules.json <<EOF
[
    {
        "group_id": "pd",
        "id": "rule1",
        "role": "voter",
        "count": 3,
        "location_labels": ["zone", "rack", "host"]
    },
    {
        "group_id": "pd",
        "id": "rule2",
        "role": "voter",
        "count": 2,
        "location_labels": ["zone", "rack", "host"]
    }
]
EOF
pd-ctl config placement save --in=rules.json
```

上記の操作は、 `rule1`と`rule2`をPDに書き込みます。同じ`GroupID` + `ID`のルールがシステムにすでに存在する場合、このルールは上書きされます。

ルールを削除するには、ルールの`count`を`0`に設定するだけで、同じ`GroupID` + `ID`のルールが削除されます。次のコマンドは、 `pd / rule2`のルールを削除します。

{{< copyable "" >}}

```bash
cat > rules.json <<EOF
[
    {
        "group_id": "pd",
        "id": "rule2"
    }
]
EOF
pd-ctl config placement save --in=rules.json
```

### pd-ctlを使用してルールグループを構成します {#use-pd-ctl-to-configure-rule-groups}

-   すべてのルールグループのリストを表示するには：

    {{< copyable "" >}}

    ```bash
    pd-ctl config placement-rules rule-group show
    ```

-   特定のIDのルールグループを表示するには：

    {{< copyable "" >}}

    ```bash
    pd-ctl config placement-rules rule-group show pd
    ```

-   ルールグループの`index`と`override`の属性を設定するには：

    {{< copyable "" >}}

    ```bash
    pd-ctl config placement-rules rule-group set pd 100 true
    ```

-   ルールグループの構成を削除するには（グループにルールがある場合は、デフォルトのグループ構成を使用します）：

    {{< copyable "" >}}

    ```bash
    pd-ctl config placement-rules rule-group delete pd
    ```

### pd-ctlを使用して、グループとグループ内のルールをバッチ更新します {#use-pd-ctl-to-batch-update-groups-and-rules-in-groups}

ルールグループとグループ内のすべてのルールを同時に表示および変更するには、 `rule-bundle`サブコマンドを実行します。

このサブコマンドでは、 `get {group_id}`を使用してグループを照会し、出力結果にルールグループとグループのルールがネストされた形式で表示されます。

{{< copyable "" >}}

```bash
pd-ctl config placement-rules rule-bundle get pd
```

上記のコマンドの出力：

```json
{
  "group_id": "pd",
  "group_index": 0,
  "group_override": false,
  "rules": [
    {
      "group_id": "pd",
      "id": "default",
      "start_key": "",
      "end_key": "",
      "role": "voter",
      "count": 3
    }
  ]
}
```

出力をファイルに書き込むには、 `rule-bundle get`サブコマンドに`--out`引数を追加します。これは、その後の変更と保存に便利です。

{{< copyable "" >}}

```bash
pd-ctl config placement-rules rule-bundle get pd --out="group.json"
```

変更が完了したら、 `rule-bundle set`サブコマンドを使用して、ファイル内の構成をPDサーバーに保存できます。 [pd-ctlを使用してルールを設定する](#set-rules-using-pd-ctl)で説明した`save`コマンドとは異なり、このコマンドはサーバー側でこのグループのすべてのルールを置き換えます。

{{< copyable "" >}}

```bash
pd-ctl config placement-rules rule-bundle set pd --in="group.json"
```

### pd-ctlを使用して、すべての構成を表示および変更します {#use-pd-ctl-to-view-and-modify-all-configurations}

pd-ctlを使用して、すべての構成を表示および変更することもできます。これを行うには、すべての構成をファイルに保存し、構成ファイルを編集してから、ファイルをPDサーバーに保存して、前の構成を上書きします。この操作でも`rule-bundle`サブコマンドを使用します。

たとえば、すべての構成を`rules.json`のファイルに保存するには、次のコマンドを実行します。

{{< copyable "" >}}

```bash
pd-ctl config placement-rules rule-bundle load --out="rules.json"
```

ファイルを編集した後、次のコマンドを実行して構成をPDサーバーに保存します。

{{< copyable "" >}}

```bash
pd-ctl config placement-rules rule-bundle save --in="rules.json"
```

### tidb-ctlを使用して、テーブル関連のキー範囲を照会します {#use-tidb-ctl-to-query-the-table-related-key-range}

メタデータまたは特定のテーブルの特別な構成が必要な場合は、 [tidb-ctl](https://github.com/pingcap/tidb-ctl)の[`keyrange`コマンド](https://github.com/pingcap/tidb-ctl/blob/master/doc/tidb-ctl_keyrange.md)を実行して関連するキーを照会できます。コマンドの最後に`--encode`を追加することを忘れないでください。

{{< copyable "" >}}

```bash
tidb-ctl keyrange --database test --table ttt --encode
```

```text
global ranges:
  meta: (6d00000000000000f8, 6e00000000000000f8)
  table: (7400000000000000f8, 7500000000000000f8)
table ttt ranges: (NOTE: key range might be changed after DDL)
  table: (7480000000000000ff2d00000000000000f8, 7480000000000000ff2e00000000000000f8)
  table indexes: (7480000000000000ff2d5f690000000000fa, 7480000000000000ff2d5f720000000000fa)
    index c2: (7480000000000000ff2d5f698000000000ff0000010000000000fa, 7480000000000000ff2d5f698000000000ff0000020000000000fa)
    index c3: (7480000000000000ff2d5f698000000000ff0000020000000000fa, 7480000000000000ff2d5f698000000000ff0000030000000000fa)
    index c4: (7480000000000000ff2d5f698000000000ff0000030000000000fa, 7480000000000000ff2d5f698000000000ff0000040000000000fa)
  table rows: (7480000000000000ff2d5f720000000000fa, 7480000000000000ff2e00000000000000f8)
```

> **ノート：**
>
> DDLおよびその他の操作により、テーブルIDが変更される可能性があるため、対応するルールを同時に更新する必要があります。

## 典型的な使用シナリオ {#typical-usage-scenarios}

このセクションでは、配置ルールの一般的な使用シナリオを紹介します。

### シナリオ1：クラスタの災害耐性を向上させるために、通常のテーブルに3つのレプリカを使用し、メタデータに5つのレプリカを使用します {#scenario-1-use-three-replicas-for-normal-tables-and-five-replicas-for-the-metadata-to-improve-cluster-disaster-tolerance}

キーの範囲をメタデータの範囲に制限するルールを追加し、値を`count`に設定するだけ`5` 。このルールの例を次に示します。

{{< copyable "" >}}

```json
{
  "group_id": "pd",
  "id": "meta",
  "index": 1,
  "override": true,
  "start_key": "6d00000000000000f8",
  "end_key": "6e00000000000000f8",
  "role": "voter",
  "count": 5,
  "location_labels": ["zone", "rack", "host"]
}
```

### シナリオ2：5つのレプリカを2：2：1の比率で3つのデータセンターに配置します。リーダーは3番目のデータセンターに配置しないでください。 {#scenario-2-place-five-replicas-in-three-data-centers-in-the-proportion-of-2-2-1-and-the-leader-should-not-be-in-the-third-data-center}

3つのルールを作成します。レプリカの数をそれぞれ`2` 、および`2`に設定し`1` 。レプリカを、各ルールの`label_constraints`までの対応するデータセンターに制限します。さらに、リーダーを必要としないデータセンターの場合は`role`を`follower`に変更します。

{{< copyable "" >}}

```json
[
    {
        "group_id": "pd",
        "id": "zone1",
        "start_key": "",
        "end_key": "",
        "role": "voter",
        "count": 2,
        "label_constraints": [
            {"key": "zone", "op": "in", "values": ["zone1"]}
        ],
        "location_labels": ["rack", "host"]
    },
    {
        "group_id": "pd",
        "id": "zone2",
        "start_key": "",
        "end_key": "",
        "role": "voter",
        "count": 2,
        "label_constraints": [
            {"key": "zone", "op": "in", "values": ["zone2"]}
        ],
        "location_labels": ["rack", "host"]
    },
    {
        "group_id": "pd",
        "id": "zone3",
        "start_key": "",
        "end_key": "",
        "role": "follower",
        "count": 1,
        "label_constraints": [
            {"key": "zone", "op": "in", "values": ["zone3"]}
        ],
        "location_labels": ["rack", "host"]
    }
]
```

### シナリオ3：テーブルに2つのTiFlashレプリカを追加する {#scenario-3-add-two-tiflash-replicas-for-a-table}

テーブルの行キーに別のルールを追加し、 `count`から`2`に制限します。 `label_constraints`を使用して、レプリカが`engine = tiflash`のノードで生成されるようにします。このルールがシステム内の他のソースからのルールと重複または競合しないようにするために、ここでは別の`group_id`が使用されていることに注意してください。

{{< copyable "" >}}

```json
{
  "group_id": "tiflash",
  "id": "learner-replica-table-ttt",
  "start_key": "7480000000000000ff2d5f720000000000fa",
  "end_key": "7480000000000000ff2e00000000000000f8",
  "role": "learner",
  "count": 2,
  "label_constraints": [
    {"key": "engine", "op": "in", "values": ["tiflash"]}
  ],
  "location_labels": ["host"]
}
```

### シナリオ4：高性能ディスクを備えた北京ノードのテーブルに2つのフォロワーレプリカを追加する {#scenario-4-add-two-follower-replicas-for-a-table-in-the-beijing-node-with-high-performance-disks}

次の例は、より複雑な`label_constraints`構成を示しています。このルールでは、レプリカは`bj1`または`bj2`のマシンルームに配置する必要があり、ディスクタイプは`ssd`であってはなりません。

{{< copyable "" >}}

```json
{
  "group_id": "follower-read",
  "id": "follower-read-table-ttt",
  "start_key": "7480000000000000ff2d00000000000000f8",
  "end_key": "7480000000000000ff2e00000000000000f8",
  "role": "follower",
  "count": 2,
  "label_constraints": [
    {"key": "zone", "op": "in", "values": ["bj1", "bj2"]},
    {"key": "disk", "op": "notIn", "values": ["ssd"]}
  ],
  "location_labels": ["host"]
}
```

### シナリオ5：テーブルをTiFlashクラスタに移行する {#scenario-5-migrate-a-table-to-the-tiflash-cluster}

シナリオ3とは異なり、このシナリオでは、既存の構成に基づいて新しいレプリカを追加するのではなく、データ範囲の他の構成を強制的にオーバーライドします。したがって、既存のルールを上書きするには、十分な大きさの`index`の値を指定し、ルールグループ構成で`override`から`true`を設定する必要があります。

ルール：

{{< copyable "" >}}

```json
{
  "group_id": "tiflash-override",
  "id": "learner-replica-table-ttt",
  "start_key": "7480000000000000ff2d5f720000000000fa",
  "end_key": "7480000000000000ff2e00000000000000f8",
  "role": "voter",
  "count": 3,
  "label_constraints": [
    {"key": "engine", "op": "in", "values": ["tiflash"]}
  ],
  "location_labels": ["host"]
}
```

ルールグループ：

{{< copyable "" >}}

```json
{
  "id": "tiflash-override",
  "index": 1024,
  "override": true,
}
```
