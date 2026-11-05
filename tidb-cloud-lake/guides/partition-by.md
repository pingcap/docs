---
title: Fuse テーブルのパーティショニング
summary: TiDB Cloud Lake で Fuse テーブルをパーティショニングし、クエリのプルーニングを高速化して予測可能なデータレイアウトを実現する方法を学びます。
---

# より高速なプルーニングと予測可能なデータレイアウトのための Fuse テーブルのパーティショニング

`PARTITION BY` は Fuse テーブルを物理的にパーティションへ分割します。{{{ .lake }}} は異なるパーティション値のブロックとセグメントを分離して保持し、メタデータにパーティション値を記録し、クエリ述語に一致しないパーティションをプルーニングします。

大規模なテーブルが時間範囲、テナントまたはリージョン識別子、あるいは別の安定した次元で頻繁にフィルタリングされる場合は、パーティショニングを使用します。カーディナリティの高いキーには、`BUCKET()` を使用して固定数のハッシュパーティションを作成します。

## どのような問題を解決するのか {#what-problem-does-it-solve}

| 問題 | 影響 | `PARTITION BY` による解決策 |
|---------|--------|-------------------------|
| クエリが大規模テーブルの一部だけを対象とする | 関係のないセグメントやブロックも調べる必要がある | パーティションメタデータにより、スキャン前に無関係なパーティションを除外する |
| 時系列データが何日分、何か月分にもまたがる | 直近期間のクエリでも過去データを読み込む | 日付式によってデータを時間パーティションにグループ化する |
| 自然キーのカーディナリティが非常に高い | 値ごとに 1 パーティションを作ると断片化が過剰になる | `BUCKET()` が値を固定数のハッシュパーティションにマッピングする |
| 分散ライターが多数の小さなブロックを生成する | 同じパーティションが複数ノードで独立して書き込まれる可能性がある | ハッシュ書き込み分散により、各パーティション値を 1 つのライターにルーティングする |

## パーティショニングとクラスタリングの比較 {#partitioning-vs-clustering}

`PARTITION BY` と `CLUSTER BY` は互いに補完し合う機能です。

| 機能 | `PARTITION BY` | `CLUSTER BY` |
|---------|----------------|--------------|
| 物理的な保証 | ブロックとセグメントはパーティション境界をまたがない | 行はソートされ、関連する値は同じ場所に配置される |
| 主な利点 | パーティションレベルのプルーニングと分離 | パーティション内での細粒度なブロックプルーニング |
| 一般的なカーディナリティ | 低い、または上限がある | 中程度から高い |
| 一般的な式 | `DATE_TRUNC(day, event_time)`, `region`, `BUCKET(32, customer_id)` | `event_time`, `customer_id`, `(region, event_time)` |
| 管理 | 書き込み、変更、コンパクション、再クラスタリングによって維持される | クラスタリングと再クラスタリングによって維持される |

1 つのテーブルで両方を使用できます。パーティションキーは、ユーザーに見えるクラスターキーの一部にはなりません。

```sql
CREATE TABLE events (
    event_time TIMESTAMP,
    tenant_id  BIGINT,
    payload    VARIANT
)
PARTITION BY (DATE_TRUNC(day, event_time))
CLUSTER BY (tenant_id, event_time);
```

## クイックセットアップ {#quick-setup}

日単位でパーティショニングされたテーブルを作成します。

```sql
CREATE TABLE events (
    event_id   BIGINT,
    event_time TIMESTAMP,
    event_type STRING
)
PARTITION BY (DATE_TRUNC(day, event_time));
```

以降のすべての書き込みは、このパーティション境界に従います。

```sql
INSERT INTO events VALUES
    (1, '2026-07-08 10:00:00', 'login'),
    (2, '2026-07-08 18:30:00', 'purchase'),
    (3, '2026-07-09 09:15:00', 'logout');
```

その後、時間に対する述語によって、無関係な日次パーティションをプルーニングできます。

```sql
EXPLAIN
SELECT *
FROM events
WHERE event_time >= TIMESTAMP '2026-07-08'
  AND event_time <  TIMESTAMP '2026-07-09';
```

`EXPLAIN` の出力では、`partitions total` と `partitions scanned` を比較し、`range pruning` の統計を確認してください。スキャンされたパーティション数が少ないほど、パーティションプルーニングが適用されていることを示します。

## パーティショニング戦略 {#partitioning-strategies}

このセクションでは、{{{ .lake }}} で Fuse テーブルをパーティショニングするさまざまな戦略について説明します。

### 時間ベースのパーティショニング {#time-based-partitioning}

タイムスタンプまたは日付カラムに決定的な式を適用します。

```sql
-- Daily partitions
PARTITION BY (DATE_TRUNC(day, event_time))

-- Monthly partitions
PARTITION BY (DATE_TRUNC(month, event_time))
```

一般的なフィルタ条件に合った粒度を選びつつ、各パーティションが断片化を避けられるだけの十分な大きさになるようにしてください。日次パーティションは通常、データ量の多いイベントデータに適しています。月次パーティションは、データ量の少ない履歴データに適していることが多いです。

### Identity パーティショニング {#identity-partitioning}

カラムが取りうる値の種類がすでに少なく、増減もほとんどない場合は、そのカラムを直接使用します。

```sql
CREATE TABLE regional_sales (
    region     STRING,
    order_id   BIGINT,
    order_date DATE,
    amount     DECIMAL(18, 2)
)
PARTITION BY (region);
```

適した Identity キーには、リージョン、国、テナント階層、またはその他の上限がある業務上の次元が含まれます。一意 ID で直接パーティショニングするのは避けてください。

### `BUCKET()` を使ったハッシュパーティショニング {#hash-partitioning-with-bucket}

`BUCKET(<count>, <column>)` は、サポートされる値を `0` から `<count> - 1` の範囲の符号なしパーティション番号へ決定的にマッピングします。バケット数は、`1` から `4294967295` までの定数整数である必要があります。

```sql
CREATE TABLE customer_events (
    customer_id BIGINT,
    event_time  TIMESTAMP,
    payload     VARIANT
)
PARTITION BY (BUCKET(32, customer_id));
```

バケットパーティショニングは、等価フィルタがカーディナリティの高いカラムを対象とする一方で、値ごとに 1 つの物理パーティションを作成するのが現実的でない場合に有効です。

`BUCKET()` でサポートされる値のデータ型は、整数、文字列、日付、タイムスタンプです。詳細は [`BUCKET()`](/tidb-cloud-lake/sql/bucket.md) を参照してください。

### 複合パーティショニング {#composite-partitioning}

複数の式を並べて、複合パーティションキーを構成します。

```sql
CREATE TABLE tenant_events (
    tenant_id  BIGINT,
    event_time TIMESTAMP,
    payload    VARIANT
)
PARTITION BY (
    DATE_TRUNC(month, event_time),
    BUCKET(16, tenant_id)
);
```

各パーティション式は、必ず 1 つのソースカラムだけを参照する必要があります。2 つのカラムでパーティショニングするには、上記のように個別の式を使用してください。`tenant_id + another_id` のような式は無効です。

## ハッシュ分散書き込み {#hash-distributed-writes}

パーティションテーブルへの分散または高並列な取り込みでは、`WRITE_DISTRIBUTION_MODE = 'hash'` を設定します。

```sql
CREATE TABLE customer_events (
    customer_id BIGINT,
    event_time  TIMESTAMP,
    payload     VARIANT
)
PARTITION BY (BUCKET(32, customer_id))
WRITE_DISTRIBUTION_MODE = 'hash';
```

このモードでは、評価済みのパーティションキーをハッシュ化し、同じパーティション値を持つ行をローカルソートの前に同じライターへルーティングします。複数のノードまたはパイプラインが同じパーティションへ同時に書き込む場合に、小さなブロックの断片化を減らせます。

`WRITE_DISTRIBUTION_MODE` には次の値を指定できます。

- `'none'` (デフォルト): 書き込み前に行を再分散しません。
- `'hash'`: 書き込み前にパーティションキーで行を再分散します。この値には `PARTITION BY` が必要です。

ハッシュ再分散ではネットワークシャッフルが追加されます。ブロックレイアウトの改善効果がシャッフルコストを上回る、分散または並列のロード で有効にしてください。小規模な単一ライターの挿入では効果がない場合があります。

> **Note:**
>
> ハッシュ分散がない場合、未ソート入力は低速です。デフォルトの `WRITE_DISTRIBUTION_MODE = 'none'` では、行は到着順に書き込まれます。入力にパーティション値が行ごとに混在していると、{{{ .lake }}} は非常に小さなブロックを多数書き込み、ロード が遅くなります。テーブルで `WRITE_DISTRIBUTION_MODE = 'hash'` を設定するか、入力をパーティションキーでソートしてください。
>
> ```sql
> INSERT INTO events SELECT ... FROM source ORDER BY DATE_TRUNC(day, event_time);
> ```

## 既存のテーブルへのパーティションキーの追加 {#adding-a-partition-key-to-an-existing-table}

`ALTER TABLE ... PARTITION BY` はテーブル定義のみを変更します。既存データは再分散されず、その後に `OPTIMIZE TABLE` や `RECLUSTER` を実行しても再分散されません。変更後に書き込まれたデータのみがパーティション化されます。

| テーブル | 結果 |
|---|---|
| 空 | 推奨されます。後からロードされるすべてのデータがパーティション化されます。 |
| データあり | 成功しますが、既存データはプルーニングされず、既存行に対する `UPDATE`、`DELETE`、または `MERGE INTO` は `serialized block contains more than one partition` で失敗します。以下のようにデータを書き直してください。 |
| 同じキーあり | 変更はありません。 |
| 異なるキーあり | `PARTITION BY is already defined ...; changing it is not supported` で失敗します。先にキーを削除してください。 |
| Fuse テーブルではない | `ALTER TABLE PARTITION BY is not supported for engine ...` で失敗します。 |

**空のテーブル:** キーを追加してからロードします。

```sql
ALTER TABLE events PARTITION BY (DATE_TRUNC(month, event_time));
INSERT INTO events SELECT * FROM source;
```

**データがあるテーブル:** キーを追加してからテーブルを書き直します。`ORDER BY` は維持してください。これがないと、書き直し時に非常に小さいブロックが書き込まれ、処理が遅くなります。

```sql
ALTER TABLE events PARTITION BY (DATE_TRUNC(month, event_time));
INSERT OVERWRITE events SELECT * FROM events ORDER BY DATE_TRUNC(month, event_time);
```

**キーを変更する場合:** いったん削除し、新しいキーを追加してからテーブルを書き直します。

```sql
ALTER TABLE events DROP PARTITION KEY;
ALTER TABLE events PARTITION BY (DATE_TRUNC(day, event_time));
INSERT OVERWRITE events SELECT * FROM events ORDER BY DATE_TRUNC(day, event_time);
```

`DROP PARTITION KEY` はデータを書き直しません。パーティションプルーニングを停止し、`WRITE_DISTRIBUTION_MODE` を `'none'` にリセットします。

## 行のパーティションキー値の更新 {#updating-the-partition-key-value-of-a-row}

`UPDATE` と `MERGE INTO` は、行のパーティションキー値を変更できます。行は新しい値に対応するパーティションへ移動します。追加の操作は不要です。

```sql
-- Moves the row from the September partition to the October partition.
UPDATE events SET event_time = '2026-10-05 12:00:00' WHERE event_id = 42;
```

行の移動ではその行が書き直されるため、インプレース更新よりコストが高くなります。

## 式のルールとテーブル変更 {#expression-rules-and-table-changes}

Fuse テーブルのパーティション式については、次のルールがあります。

- 各式は決定的で、ちょうど 1 つのソースカラムを参照する必要があります。
- 複合パーティション化では、複数カラムの 1 つの式ではなく、複数の式を使用します。
- `BUCKET()` では、`1` から `4294967295` までの定数のバケット数が必要です。
- パーティションキーが参照するカラムは、削除したりデータ型を変更したりできません。
- 参照されているカラムの名前を変更すると、保存されているパーティション式も更新されます。
- 内部の `partition_by` メタデータは `SET OPTIONS` では変更できません。
- `PARTITION BY` は Fuse テーブルでサポートされています。その他のエンジンでは、異なるパーティション構文やセマンティクスが実装されている場合があります。

## ベストプラクティス {#best-practices}

| プラクティス | 役立つ理由 |
|----------|--------------|
| パーティション式を頻繁に使うフィルターに合わせる | オプティマイザが早い段階でパーティションを除外できるようになります |
| 低い、または上限のあるカーディナリティを優先する | 過剰に多い小さなパーティションやメタデータを避けられます |
| 高カーディナリティの等価キーには `BUCKET()` を使う | パーティション数を予測しやすく保てます |
| パーティション化をクラスターキーと組み合わせる | 各パーティション内でより細かいプルーニングを追加できます |
| 実際の取り込み並行性を代表する条件でテストする | ハッシュ分散書き込みが断片化の低減に有効かどうかを判断できます |
| `EXPLAIN` で確認する | 述語によって `partitions scanned` が減っていることを確認できます |

> **Tip:**
>
> 適した候補:
>
> - 日または月でフィルタリングされるイベントテーブルやログテーブル
> - テナントでフィルタリングされるマルチテナントテーブル
> - 値の範囲が限定されているリージョン別またはカテゴリ別のデータセット
> - 固定バケット数を使う高カーディナリティの等価検索

> **Note:**
>
> **パーティション化しないほうがよい場合:** 小さいテーブル、安定したフィルターパターンがないテーブル、多数の非常に小さいパーティションを作るキーは、一般に物理パーティション化の恩恵を受けません。そのような場合は、[クラスターキー](/tidb-cloud-lake/guides/cluster-key-performance.md) だけのほうが適していることがあります。