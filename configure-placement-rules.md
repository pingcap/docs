---
title: Placement Rules
summary: 配置ルールを構成する方法を学習します。
---

# 配置ルール {#placement-rules}

> **注記：**
>
> このドキュメントでは、Placement Driver (PD) で配置ルールを手動で指定する方法を紹介します。現在は[SQLの配置ルール](/placement-rules-in-sql.md)使用が推奨されています。これにより、テーブルとパーティションの配置をより簡単に設定できます。

バージョン5.0で導入された配置ルールは、PDが様々なデータタイプに対応するスケジュールを生成するためのレプリカルールシステムです。様々なスケジューリングルールを組み合わせることで、レプリカ数、storage場所、ホストタイプ、 Raft選出への参加、 Raftリーダーとしての役割など、任意の連続データ範囲の属性を細かく制御できます。

TiDBバージョン5.0以降では、配置ルール機能はデフォルトで有効になっています。無効にするには、 [配置ルールを無効にする](#disable-placement-rules)を参照してください。

## ルールシステム {#rule-system}

ルールシステム全体の構成は複数のルールで構成されます。各ルールは、レプリカ数、 Raftの役割、配置場所、ルールが適用されるキー範囲などの属性を指定できます。PDがスケジュールを実行する際、まずルールシステム内でリージョンのキー範囲に基づいてリージョンに対応するルールを検索し、次に対応するスケジュールを生成することで、リージョンのレプリカの配置がルールに準拠するようにします。

複数のルールのキー範囲は重複する部分を持つ場合があり、これはリージョンが複数のルールに一致する可能性があることを意味します。この場合、PDはルールの属性に基づいて、ルールが互いに上書きされるか、同時に有効になるかを決定します。複数のルールが同時に有効になる場合、PDはルールマッチングのために、ルールのスタック順序に従って順番にスケジュールを生成します。

さらに、異なるソースからのルールを互いに分離するという要件を満たすため、これらのルールをより柔軟に整理できます。そのため、「グループ」という概念が導入されました。一般的に、ユーザーは異なるソースに基づいてルールを異なるグループに配置できます。

![Placement rules overview](/media/placement-rules-1.png)

### ルールフィールド {#rule-fields}

次の表は、ルール内の各フィールドの意味を示しています。

| フィールド名            | 種類と制限             | 説明                                 |
| :---------------- | :---------------- | :--------------------------------- |
| `GroupID`         | `string`          | ルールのソースを示すグループ ID。                 |
| `ID`              | `string`          | グループ内のルールの一意の ID。                  |
| `Index`           | `int`             | グループ内のルールの積み重ね順序。                  |
| `Override`        | `true` / `false`  | グループ内のより小さいインデックスを持つルールを上書きするかどうか。 |
| `StartKey`        | `string` （16進数形式） | 範囲の開始キーに適用されます。                    |
| `EndKey`          | `string` （16進数形式） | 範囲の終了キーに適用されます。                    |
| `Role`            | `string`          | 投票者/リーダー/フォロワー/学習者などのレプリカロール。      |
| `Count`           | `int` 、正の整数       | レプリカの数。                            |
| `LabelConstraint` | `[]Constraint`    | ラベルに基づいてノードをフィルタリングします。            |
| `LocationLabels`  | `[]string`        | 物理的な分離に使用されます。                     |
| `IsolationLevel`  | `string`          | 最小の物理的分離レベルを設定するために使用              |

`LabelConstraint`は`notIn` `notExists` `in` `exists`のプリミティブに基づいてラベルをフィルタリングします。これらの4つのプリミティブの意味は次のとおりです。

-   `in` : 指定されたキーのラベル値が指定されたリストに含まれます。
-   `notIn` : 指定されたキーのラベル値は、指定されたリストに含まれていません。
-   `exists` : 指定されたラベル キーが含まれます。
-   `notExists` : 指定されたラベル キーは含まれません。

`LocationLabels`の意味と機能は、v4.0 以前のバージョンと同じです。例えば、 `[zone,rack,host]`デプロイし、3 層トポロジを定義しているとします。クラスターには複数のゾーン（アベイラビリティゾーン）があり、各ゾーンには複数のラックがあり、各ラックには複数のホストがあります。スケジュールを実行する際、PD はまずリージョンのピアを異なるゾーンに配置しようとします。この試行が失敗した場合（レプリカは 3 つあるがゾーンは合計 2 つしかない場合など）、PD はこれらのレプリカを異なるラックに配置することを保証します。ラック数が分離を保証するのに十分でない場合、PD はホストレベルの分離を試みます。

`IsolationLevel`の意味と機能については[クラスタトポロジ構成](/schedule-replicas-by-topology-labels.md)で詳しく説明します。例えば、 `LocationLabels`を含む3層トポロジを定義する`[zone,rack,host]`デプロイし、 `IsolationLevel`を`zone`に設定した場合、PDはスケジューリング中に各リージョンのすべてのピアが異なるゾーンに配置されるように保証します。 `IsolationLevel`の最小分離レベル制限を満たすことができない場合（例えば、レプリカが3つ設定されているが、データゾーンが合計で2つしかない場合）、PDはこの制限を満たすために調整を試みません。デフォルト値`IsolationLevel`は空の文字列であり、無効であることを意味します。

### ルールグループのフィールド {#fields-of-the-rule-group}

次の表は、ルール グループ内の各フィールドの説明を示しています。

| フィールド名     | 種類と制限            | 説明                                |
| :--------- | :--------------- | :-------------------------------- |
| `ID`       | `string`         | ルールのソースを示すグループ ID。                |
| `Index`    | `int`            | 異なるグループの積み重ね順序。                   |
| `Override` | `true` / `false` | より小さいインデックスを持つグループをオーバーライドするかどうか。 |

## ルールを設定する {#configure-rules}

このセクションの操作は[pd-ctl](/pd-control.md)に基づいており、操作に関連するコマンドは HTTP API 経由の呼び出しもサポートしています。

### 配置ルールを有効にする {#enable-placement-rules}

TiDB v5.0以降では、配置ルール機能はデフォルトで有効になっています。無効にするには、 [配置ルールを無効にする](#disable-placement-rules)を参照してください。無効にした後でこの機能を有効にするには、クラスターを初期化する前に、PD構成ファイルを以下のように変更します。

```toml
[replication]
enable-placement-rules = true
```

このように、PD はクラスターが正常にブートストラップされた後にこの機能を有効にし、 [`max-replicas`](/pd-configuration-file.md#max-replicas) 、 [`location-labels`](/pd-configuration-file.md#location-labels) 、および[`isolation-level`](/pd-configuration-file.md#isolation-level)構成に応じて対応するルールを生成します。

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

ブートストラップされたクラスターの場合、pd-ctl を使用して配置ルールを動的に有効にすることもできます。

```bash
pd-ctl config placement-rules enable
```

PD は、 `max-replicas` 、 `location-labels` 、および`isolation-level`構成に基づいてデフォルトのルールも生成します。

> **注記：**
>
> -   配置ルールが有効で複数のルールが存在する場合、以前に設定されたルール`max-replicas` 、 `location-labels` 、および`isolation-level`適用されなくなります。レプリカポリシーを調整するには、配置ルールに関連するインターフェースを使用してください。
> -   配置ルールが有効になっていて、デフォルト ルールが 1 つだけ存在する場合、 `max-replicas` 、または`isolation-level` `location-labels`が変更されると、TiDB はこのデフォルト ルールを自動的に更新します。

### 配置ルールを無効にする {#disable-placement-rules}

pd-ctl を使用すると、配置ルール機能を無効にし、以前のスケジュール戦略に切り替えることができます。

```bash
pd-ctl config placement-rules disable
```

> **注記：**
>
> 配置ルールを無効にすると、PDは元`isolation-level` `max-replicas` `location-labels`設定を使用します。配置ルールが有効になっている場合、ルールを変更しても、これらの3つの設定はリアルタイムで更新されません。また、設定されたすべてのルールはPDに保持され、次回配置ルールを有効にしたときに使用されます。

### pd-ctlを使用してルールを設定する {#set-rules-using-pd-ctl}

> **注記：**
>
> ルールの変更はPDのスケジューリングにリアルタイムで影響します。ルール設定が不適切だと、レプリカ数が減少し、システムの高可用性に影響を与える可能性があります。

pd-ctl は、システム内のルールを表示するために次のメソッドの使用をサポートしており、出力は JSON 形式のルールまたはルール リストです。

-   すべてのルールのリストを表示するには:

    ```bash
    pd-ctl config placement-rules show
    ```

-   PD グループ内のすべてのルールのリストを表示するには:

    ```bash
    pd-ctl config placement-rules show --group=pd
    ```

-   グループ内の特定の ID のルールを表示するには:

    ```bash
    pd-ctl config placement-rules show --group=pd --id=default
    ```

-   リージョンに一致するルール リストを表示するには:

    ```bash
    pd-ctl config placement-rules show --region=2
    ```

    上記の例では、 `2`リージョンID です。

ルールの追加と編集は似ています。対応するルールをファイルに記述し、 `save`コマンドを使用してPDに保存する必要があります。

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

» ./pd-ctl -u 127.0.0.1:2379 config placement-rules save --in=rules.json
Success!
```

上記の操作により、 `rule1`と`rule2` PDに書き込まれます。同じ`GroupID` + `ID`を持つルールがシステム内に既に存在する場合、このルールは上書きされます。

ルールを削除するには、ルールの`count` `0`に設定するだけで、同じ`GroupID` + `ID`を持つルールが削除されます。次のコマンドは、 `pd / rule2`ルールを削除します。

```bash
cat > rules.json <<EOF
[
    {
        "group_id": "pd",
        "id": "rule2"
    }
]
EOF

» ./pd-ctl -u 127.0.0.1:2379 config placement-rules save --in=rules.json
Success!
```

### pd-ctlを使用してルールグループを構成する {#use-pd-ctl-to-configure-rule-groups}

-   すべてのルール グループのリストを表示するには:

    ```bash
    pd-ctl config placement-rules rule-group show
    ```

-   特定の ID のルール グループを表示するには:

    ```bash
    pd-ctl config placement-rules rule-group show pd
    ```

-   ルール グループの`index`と`override`属性を設定するには:

    ```bash
    pd-ctl config placement-rules rule-group set pd 100 true
    ```

-   ルール グループの構成を削除するには (グループ内にルールがある場合はデフォルトのグループ構成を使用します)。

    ```bash
    pd-ctl config placement-rules rule-group delete pd
    ```

### pd-ctl を使用してグループとグループ内のルールを一括更新する {#use-pd-ctl-to-batch-update-groups-and-rules-in-groups}

ルール グループとグループ内のすべてのルールを同時に表示および変更するには、サブコマンド`rule-bundle`を実行します。

このサブコマンドでは、 `get {group_id}`使用してグループを照会し、出力結果にはルール グループとグループのルールがネストされた形式で表示されます。

```bash
pd-ctl config placement-rules rule-bundle get pd
```

上記のコマンドの出力:

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

出力をファイルに書き込むには、 `rule-bundle get`サブコマンドに`--out`引数を追加します。これは、後続の変更や保存に便利です。

```bash
pd-ctl config placement-rules rule-bundle get pd --out="group.json"
```

変更が完了したら、サブコマンド`rule-bundle set`を使用して、ファイル内の設定を PDサーバーに保存できます。 [pd-ctlを使用してルールを設定する](#set-rules-using-pd-ctl)で説明したコマンド`save`とは異なり、このコマンドはサーバー側でこのグループのすべてのルールを置き換えます。

```bash
pd-ctl config placement-rules rule-bundle set pd --in="group.json"
```

### pd-ctlを使用してすべての設定を表示および変更します {#use-pd-ctl-to-view-and-modify-all-configurations}

pd-ctl を使用してすべての設定を表示および変更することもできます。これを行うには、すべての設定をファイルに保存し、その設定ファイルを編集して PDサーバーに保存し、以前の設定を上書きします。この操作でも`rule-bundle`サブコマンドを使用します。

たとえば、すべての構成を`rules.json`ファイルに保存するには、次のコマンドを実行します。

```bash
pd-ctl config placement-rules rule-bundle load --out="rules.json"
```

ファイルを編集した後、次のコマンドを実行して、設定を PDサーバーに保存します。

```bash
pd-ctl config placement-rules rule-bundle save --in="rules.json"
```

### tidb-ctlを使用してテーブル関連のキー範囲を照会する {#use-tidb-ctl-to-query-the-table-related-key-range}

メタデータまたは特定のテーブルに特別な設定が必要な場合は、「 [`keyrange`コマンド](https://github.com/pingcap/tidb-ctl/blob/master/doc/tidb-ctl_keyrange.md) in [tidb-ctl](https://github.com/pingcap/tidb-ctl)を実行して関連キーをクエリできます。コマンドの末尾に`--encode`を追加することを忘れないでください。

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

> **注記：**
>
> DDL やその他の操作によってテーブル ID が変更される可能性があるため、対応するルールも同時に更新する必要があります。

## 一般的な使用シナリオ {#typical-usage-scenarios}

このセクションでは、配置ルールの一般的な使用シナリオを紹介します。

### シナリオ 1: 通常のテーブルに 3 つのレプリカを使用し、メタデータに 5 つのレプリカを使用してクラスタの耐障害性を向上させる {#scenario-1-use-three-replicas-for-normal-tables-and-five-replicas-for-the-metadata-to-improve-cluster-disaster-tolerance}

キーの範囲をメタデータの範囲に制限するルールを追加し、値を`count`から`5`に設定するだけです。このルールの例を以下に示します。

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

### シナリオ2: 3つのデータセンターに5つのレプリカを2:2:1の割合で配置し、Leaderは3番目のデータセンターに配置しない {#scenario-2-place-five-replicas-in-three-data-centers-in-the-proportion-of-2-2-1-and-the-leader-should-not-be-in-the-third-data-center}

3つのルールを作成します。レプリカ数をそれぞれ`2` 、 `2` 、 `1`に設定します。各ルールで、レプリカを対応するデータセンター`label_constraints`から 8 に制限します。さらに、Leaderを必要としないデータセンターについては、 `role`を`follower`に変更します。

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

### シナリオ3: テーブルに2つのTiFlashレプリカを追加する {#scenario-3-add-two-tiflash-replicas-for-a-table}

テーブルの行キーに別のルールを追加し、 `count`から`2`の範囲で制限します。 `label_constraints`使用することで、レプリカが`engine = tiflash`のノードに生成されるようにします。ここで別途`group_id`使用するのは、このルールがシステム内の他のソースのルールと重複したり衝突したりしないようにするためです。

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

### シナリオ4: 高性能ディスクを備えた北京ノードのテーブルに2つのフォロワーレプリカを追加する {#scenario-4-add-two-follower-replicas-for-a-table-in-the-beijing-node-with-high-performance-disks}

次の例は、より複雑な`label_constraints`構成を示しています。このルールでは、レプリカは`bj1`または`bj2`マシンルームに配置する必要があり、ディスクタイプは`nvme`ある必要があります。

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
    {"key": "disk", "op": "in", "values": ["nvme"]}
  ],
  "location_labels": ["host"]
}
```

### シナリオ5: SSDディスクを搭載したノードにテーブルを移行する {#scenario-5-migrate-a-table-to-the-nodes-with-ssd-disks}

シナリオ3とは異なり、このシナリオは既存の設定に基づいて新しいレプリカを追加するのではなく、データ範囲の他の設定を強制的に上書きします。そのため、ルールグループ設定で、十分な大きさの`index`値を指定し、既存のルールを上書きするには`override` ～ `true`を設定する必要があります。

ルール:

```json
{
  "group_id": "ssd-override",
  "id": "ssd-table-45",
  "start_key": "7480000000000000ff2d5f720000000000fa",
  "end_key": "7480000000000000ff2e00000000000000f8",
  "role": "voter",
  "count": 3,
  "label_constraints": [
    {"key": "disk", "op": "in", "values": ["ssd"]}
  ],
  "location_labels": ["rack", "host"]
}
```

ルール グループ:

```json
{
  "id": "ssd-override",
  "index": 1024,
  "override": true,
}
```
