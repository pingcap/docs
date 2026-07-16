---
title: TiCDC Table Routing
summary: TiCDC の新しいアーキテクチャにおけるテーブルルーティング設定について説明します。これには、target-schema と target-table を使用して下流のデータベース名とテーブル名を書き換える方法、DDL の書き換えとルーティング競合の処理方法、一般的な問題のトラブルシューティングが含まれます。
---

# TiCDC Table Routing <span class="version-mark">New in v8.5.7</span>

TiCDC のテーブルルーティングを使用すると、changefeed の設定を通じて、上流テーブルを特定の下流データベース名またはテーブル名にマッピングできます。この機能は [TiCDC new architecture](/ticdc/ticdc-architecture.md) にのみ適用され、[TiCDC classic architecture](/ticdc/ticdc-classic-architecture.md) ではサポートされません。

テーブルルーティングは、TiCDC が下流に出力するデータベース名とテーブル名のみを変更します。行データ、カラム名、テーブルスキーマ、テーブルフィルタルール、トピックディスパッチルール、パーティションディスパッチルール、またはカラムセレクタルールは変更しません。

## 使用シナリオ {#usage-scenarios}

次のシナリオでテーブルルーティングを設定できます。

- `sales.orders` を `archive.sales_orders` にレプリケートする場合、または他の下流命名規則に従うテーブルにレプリケートする場合。
- 複数のソースデータベースを同じターゲットデータベースにレプリケートしつつ、ソースデータベースを区別できるようにターゲットテーブル名を一意に保つ場合。たとえば、`tenant_001.orders` を `tenant_mirror.tenant_001_orders` にレプリケートする場合。
- マイグレーション、ディザスタリカバリ、アーカイブ、またはシャドウトラフィック用の changefeed を構築し、上流と同じ名前の下流オブジェクトへの書き込みを避ける場合。
- MQ コンシューマーアプリケーションまたはストレージサービスに対して、安定したデータベース名とテーブル名を公開する場合。

> **Note:**
>
> テーブルルーティングは、上流テーブルから下流ターゲットテーブルへの一対一のマッピングのみをサポートします。複数の上流テーブルを同じ下流テーブルにマージすることはサポートしていません。
> テーブルルーティングは、1 つの上流テーブルを複数の下流テーブルに分割したり、行データの内容を変換したりすることはサポートしていません。

## テーブルルーティングを設定する {#configure-table-routing}

テーブルルーティングを設定する前に、TiCDC new architecture を有効にしてください。詳細は [`newarch`](/ticdc/ticdc-server-config.md#newarch-new-in-v854-release1) を参照してください。

次の例では、`sales.orders` を `archive.sales_orders` にルーティングします。

```toml
[sink]
[[sink.dispatchers]]
matcher = ["sales.orders"]
target-schema = "archive"
target-table = "{schema}_{table}"
```

changefeed の開始後、TiCDC は `sales.orders` の DML および DDL イベントを下流の `archive.sales_orders` に書き込みます。

> **Note:**
>
> 同じ上流データベース内の異なるテーブルを異なるターゲットデータベースにルーティングできますが、このルーティング設定が適用されるのは DML とテーブルレベル DDL のみです。

> - `CREATE DATABASE`、`DROP DATABASE`、`ALTER DATABASE` などのデータベースレベル DDL については、TiCDC がルーティングルールに基づいて一意のターゲットデータベースを判定できる必要があります。そうでない場合、その DDL のレプリケーションは失敗します。
> - 同じ上流データベース内の異なるテーブルを異なるターゲットデータベースにルーティングしたい場合は、下流のターゲットデータベースを事前に作成し、自動レプリケーションが必要な上流のデータベースレベル DDL の実行を避ける必要があります。

## 設定フィールド {#configuration-fields}

テーブルルーティング機能を使用するには、[`sink.dispatchers`](/ticdc/ticdc-changefeed-config.md#dispatchers) で次のフィールドを設定できます。

| フィールド | 説明 |
| :--- | :--- |
| `matcher` | 上流のデータベースとテーブルに一致させます。構文は [table filter syntax](/table-filter.md#syntax) と同じで、`sales.*` のようなワイルドカード一致や `!sales.tmp_*` のような除外一致を含みます。 |
| `target-schema` | 下流データベース名を指定します。このフィールドが設定されていない場合、TiCDC は上流データベース名を変更しません。 |
| `target-table` | 下流テーブル名を指定します。このフィールドが設定されていない場合、TiCDC は上流テーブル名を変更しません。 |

一致動作は次のとおりです。

- テーブルルーティングには、`target-schema` または `target-table` を指定した `sink.dispatchers` ルールのみが使用されます。
- 1 つのテーブルが複数のテーブルルーティングルールに一致する場合、`sink.dispatchers` 内で最初に一致したルールのみが有効になります。
- `matcher` は常に上流のデータベース名とテーブル名に一致し、ルーティング後のターゲットデータベース名やテーブル名には一致しません。
- changefeed 設定項目 `case-sensitive` は、テーブルルーティング内の `matcher` が大文字小文字を区別するかどうかにのみ影響します。`{schema}` および `{table}` から展開される値の大文字小文字は変更しません。詳細は [`case-sensitive`](/ticdc/ticdc-changefeed-config.md#case-sensitive) を参照してください。

### プレースホルダー {#placeholders}

`target-schema` と `target-table` では、次のプレースホルダーを使用できます。

| プレースホルダー | 説明 |
| :--- | :--- |
| `{schema}` | 上流データベース名。実際に一致したデータベース名の大文字小文字を保持します。 |
| `{table}` | 上流テーブル名。実際に一致したテーブル名の大文字小文字を保持します。 |

`target-schema` と `target-table` の値には、リテラルテキスト、`{schema}`、`{table}` のみを含めることができます。`{db}` のような未知のプレースホルダーを使用すると、TiCDC は changefeed 設定を拒否し、`CDC:ErrInvalidTableRoutingRule` エラーを返します。

ソーステーブル `sales.orders` を例にすると、次のようになります。

| 設定 | ターゲットテーブル |
| :--- | :--- |
| `target-schema = "archive"` | `archive.orders` |
| `target-table = "{table}_bak"` | `sales.orders_bak` |
| `target-schema = "{schema}_mirror"` | `sales_mirror.orders` |
| `target-schema = "archive"` and `target-table = "{schema}_{table}"` | `archive.sales_orders` |

## 例 {#examples}

### 1 つのデータベース内のすべてのテーブルをルーティングする {#route-all-tables-in-one-database}

次の設定では、`sales` データベース内のすべてのテーブルを `archive` データベースにルーティングし、ターゲットテーブル名に `_bak` を追加します。

```toml
[filter]
rules = ["sales.*"]

[sink]
[[sink.dispatchers]]
matcher = ["sales.*"]
target-schema = "archive"
target-table = "{table}_bak"
```

ルーティング結果の例:

- `sales.orders` は `archive.orders_bak` にルーティングされます。
- `sales.order_items` は `archive.order_items_bak` にルーティングされます。

### 複数のデータベースを同じターゲットデータベースにルーティングする {#route-multiple-databases-to-the-same-target-database}

複数のデータベースを同じターゲットデータベースにルーティングする場合は、ターゲットテーブル名の一意性を確保するために、`target-table` に `{schema}` を含めることを推奨します。

```toml
[filter]
rules = ["sales.*", "crm.*", "finance.*"]

[sink]
[[sink.dispatchers]]
matcher = ["sales.*", "crm.*", "finance.*"]
target-schema = "archive"
target-table = "{schema}_{table}"
```

ルーティング結果の例:

- `sales.orders` は `archive.sales_orders` にルーティングされます。
- `crm.orders` は `archive.crm_orders` にルーティングされます。
- `finance.orders` は `archive.finance_orders` にルーティングされます。

> **Note:**
>
> この設定はデータベースのマージにのみ適用され、テーブルのマージには適用されません。テーブルルーティングは、複数の上流データベースにある同名テーブルを同じ下流テーブルにマージすることをサポートしていません。

### Kafka sink の topic および partition dispatchers と一緒にテーブルルーティングを使用する {#use-table-routing-together-with-kafka-sink-topic-and-partition-dispatchers}

同じ dispatcher ルール内で、テーブルルーティングフィールドと既存の dispatch フィールドの両方を設定できます。

```toml
[filter]
rules = ["sales.orders"]

[sink]
[[sink.dispatchers]]
matcher = ["sales.orders"]
topic = "order-events"
partition = "index-value"
target-schema = "public"
target-table = "orders"
```

前述の例では、テーブルルーティングにより、下流データで公開されるデータベース名とテーブル名が `public.orders` に変更されます。

テーブルルーティングは、topic または partition のディスパッチ結果を変更しません。`topic` および `partition` dispatchers は、引き続き上流テーブル `sales.orders` に基づいて一致判定とディスパッチ計算を行います。

## 出力動作 {#output-behavior}

| Sink | 動作 |
| :--- | :--- |
| MySQL sink | TiCDC は、ルーティング後のターゲットデータベースとテーブルに DDL および DML ステートメントを書き込みます。Redo 機能が有効な場合、`redo apply` を実行すると、ルーティング後のターゲットテーブルにイベントが再生されます。 |
| Kafka sink and Pulsar sink | プロトコル内の `payload` フィールドの値と、DDL イベント内の `query` フィールドの値には、ルーティング後のターゲットデータベース名とテーブル名が使用されます。エンコーディングプロトコル内の `schema` フィールドと `table` フィールドの値にも、ルーティング後のターゲットデータベース名とテーブル名が使用されます。 |
| Cloud storage sink | TiCDC は、ルーティング後のターゲットデータベース名とテーブル名に基づいて、対応するストレージパス、スキーマファイル、テーブル定義ファイル、およびデータファイルを生成します。 |

## DDL の動作 {#ddl-behavior}

テーブルルーティングを有効にすると、TiCDC は DDL ステートメントを書き換え、構造化 DDL メタデータ内のデータベース名とテーブル名が SQL テキスト内のものと一貫するようにします。

たとえば、次のルールが設定されている場合:

```toml
[[sink.dispatchers]]
matcher = ["sales.*"]
target-schema = "archive"
target-table = "{table}_routed"
```

次の上流 DDL ステートメントに対して:

```sql
RENAME TABLE `sales`.`temp_table` TO `sales`.`renamed_table`;
```

TiCDC はこれを次の下流 DDL ステートメントに書き換えます。

```sql
RENAME TABLE `archive`.`temp_table_routed` TO `archive`.`renamed_table_routed`;
```

DDL ステートメントにテーブル参照が含まれており、その参照先テーブルがテーブルルーティングルールに一致する場合、TiCDC は参照先テーブル名も書き換えます。たとえば、TiCDC は `CREATE VIEW` ステートメント内のテーブル参照や、`ALTER TABLE` ステートメント内の外部キー参照を書き換えることができます。

`CREATE DATABASE`、`DROP DATABASE`、`ALTER DATABASE ... CHARACTER SET/COLLATE` などのデータベースレベル DDL については、データベース名がテーブルルーティングルールに一致する場合、TiCDC はそのデータベース名を書き換えます。**同じ上流データベースが複数のテーブルルーティングルールに一致し、それらのルールが異なるターゲットデータベース名にマッピングされる場合、TiCDC はそのデータベースレベル DDL に対して一意のターゲットデータベースを判定できず、changefeed はテーブルルーティングエラーを返します。**

changefeed の作成時または更新時に、TiCDC は現在レプリケーション対象範囲にあるテーブルに基づいてターゲットテーブルの競合をチェックします。実行時には、TiCDC は `CREATE TABLE`、`RENAME TABLE`、`DROP TABLE`、`DROP DATABASE` などの DDL をレプリケートする際に、競合検出状態を更新します。データベースレベル DDL ステートメントについては、TiCDC はそれをレプリケートする際に一意のターゲットデータベースを判定できるかどうかを評価します。

## ルート競合の検出 {#route-conflict-detection}

ルート競合は、1 つの changefeed 内で 2 つの異なる上流テーブルが同じ下流の `(schema, table)` にルーティングされる場合に発生します。TiCDC は、複数の上流テーブルを同じ下流テーブルにマージすることをサポートしていません。

たとえば、次の設定では競合が発生する可能性があります。

```toml
[filter]
rules = ["sales.*", "crm.*"]

[sink]
[[sink.dispatchers]]
matcher = ["sales.*"]
target-schema = "archive"
target-table = "{table}"

[[sink.dispatchers]]
matcher = ["crm.*"]
target-schema = "archive"
target-table = "{table}"
```

`sales.orders` と `crm.orders` の両方がレプリケーション範囲に含まれている場合、両方のテーブルは `archive.orders` にルーティングされます。TiCDC は changefeed の作成または更新を拒否し、`CDC:ErrTableRouteConflict` エラーを返します。

changefeed の実行中に、`CREATE TABLE` や `RENAME TABLE` などの DDL 文によって、現在レプリケーション範囲に含まれている 2 つの上流テーブルが同じターゲットテーブルにルーティングされるようになると、changefeed は失敗し、`CDC:ErrTableRouteConflict` エラーを返します。

上流テーブルが削除またはリネームされると、TiCDC はその上流テーブルとターゲットテーブルの間のルーティング関係を削除します。その後、新しい上流テーブルはそのターゲットテーブルを引き続き使用できます。ただし、任意の時点において、同じターゲットテーブルに対応できるのは、現在の changefeed によってレプリケートされている 1 つの上流テーブルのみです。

> **Warning:**
>
> ルート競合検出は、単一の changefeed 内で有効になります。複数の changefeed が同じ下流システムに書き込む場合は、それらの changefeed のテーブルルーティングルールによって同じターゲットオブジェクトにテーブルがルーティングされないようにしてください。

## トラブルシューティング {#troubleshooting}

| 症状 | 考えられる原因 | 解決策 |
| :--- | :--- | :--- |
| changefeed の作成または更新時に、TiCDC が `CDC:ErrInvalidTableRoutingRule` エラーを報告する。 | `matcher` の構文が無効であるか、`target-schema` または `target-table` に不明なプレースホルダーまたは対応しない中括弧が含まれている。 | `matcher` が [table filter syntax](/table-filter.md#syntax) に準拠しているか確認し、`target-schema` と `target-table` ではリテラルテキスト、`{schema}`、`{table}` のみを使用していることを確認してください。 |
| MQ topic 名が引き続き上流のデータベース名とテーブル名を使用している。 | テーブルルーティングでは topic やパーティションのディスパッチルールは変更されない。 | topic 名を変更する必要がある場合は、`sink.dispatchers` で `topic` を個別に設定してください。 |
| DDL レプリケーション中に、TiCDC が `CDC:ErrTableRoutingFailed` エラーを報告する。 | TiCDC がテーブルルーティング用に DDL を安全に書き換えられないか、データベースレベル DDL のターゲットデータベースが曖昧である。 | DDL の種類とルーティングルールを確認してください。データベースレベル DDL の場合は、同じ上流データベースが 1 つのターゲットデータベースにのみマッピングされるようにしてください。 |
| 実行中に changefeed が失敗し、TiCDC が `CDC:ErrTableRouteConflict` エラーを報告する。 | テーブルの作成またはリネーム後に、2 つの異なる上流テーブルが同じ下流テーブルにルーティングされる。 | 単一の changefeed 内で、任意の時点において各ターゲットテーブルが現在の changefeed によってレプリケートされている 1 つの上流テーブルにのみ対応するよう、テーブルルーティングルールまたは上流 DDL を調整してください。 |

## 関連ドキュメント {#related-documentation}

- [TiCDC Changefeed の CLI と設定パラメータ](/ticdc/ticdc-changefeed-config.md)
- [Changefeed Log Filters](/ticdc/ticdc-filter.md)
- [MySQL-compatible Databases へのデータレプリケーション](/ticdc/ticdc-sink-to-mysql.md)
- [Kafka へのデータレプリケーション](/ticdc/ticdc-sink-to-kafka.md)
- [Pulsar へのデータレプリケーション](/ticdc/ticdc-sink-to-pulsar.md)
- [Storage Services へのデータレプリケーション](/ticdc/ticdc-sink-to-cloud-storage.md)