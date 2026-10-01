---
title: 階層型ストレージの設定と管理
summary: TiDB Cloud Premium または BYOC で、DDL、パーティションセレクター、ベストプラクティスを含む階層型ストレージを設定および管理する方法を学びます。
---

# 階層型ストレージの設定と管理

このドキュメントでは、ストレージクラス設定、パーティションセレクター、および推奨される運用プラクティスを含む、Infrequent Access (IA) ストレージの設定と管理方法について説明します。

> **Note:**
>
> 階層型ストレージは、{{{ .premium }}} および {{{ .byoc }}} 向けに **プライベートプレビュー** として提供されており、デフォルトでは無効になっています。使用するには、[TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) に連絡して、インスタンスで有効化してもらってください。このページで説明している動作は、現在のプレビュー実装に基づくものであり、一般提供 (GA) 前に変更される可能性があります。

## 使用方法 {#how-to-use}

このセクションでは、ストレージクラス設定、パーティションセレクター、および推奨される運用プラクティスを含む、IA ストレージの設定と管理方法について説明します。

### ストレージクラスのサポートマトリクス {#storage-class-support-matrix}

このセクションでは、サポートされるストレージクラス値、テーブルタイプ、およびインデックスや関連オブジェクトの継承ルールについて説明します。

#### ストレージクラス値 {#storage-class-values}

| 値 | 意味 | デフォルト |
|-|-|-|
| `Standard` | ローカルのホットストレージ。すべてのデータがローカルディスク上に存在 | はい |
| `IA` | リモートのコールドストレージ。すべてのデータはオブジェクトストレージにあり、ローカルではオンデマンドキャッシュされる | いいえ |

値では大文字と小文字は区別されません。

#### サポートされるテーブルタイプ {#supported-table-types}

| テーブルタイプ | IA サポート | 注記 |
|-|-|-|
| 通常の非パーティションテーブル | サポート対象 | `STORAGE_CLASS` の糖衣構文または `ENGINE_ATTRIBUTE` を使用 |
| Range パーティション | サポート対象 | `ENGINE_ATTRIBUTE` を使用する必要があります |
| Range Columns パーティション | サポート対象 | `ENGINE_ATTRIBUTE` を使用する必要があります |
| List パーティション | サポート対象 | `ENGINE_ATTRIBUTE` を使用する必要があります |
| List Columns パーティション | サポート対象 | `ENGINE_ATTRIBUTE` を使用する必要があります |
| Hash パーティション | **サポート対象外** | — |
| Key パーティション | **サポート対象外** | — |

#### インデックスおよび関連オブジェクトのストレージタイプ継承ルール {#storage-type-inheritance-rules-for-indexes-and-related-objects}

| オブジェクト | 継承ルール |
|-|-|
| 通常テーブルのインデックス | テーブルと同じ |
| パーティションテーブルの Local Index | 所有するパーティションと同じ |
| パーティションテーブルの Global Index | テーブルレベル設定と同じ |
| TiFlash | **テーブルのストレージ設定には従いません** |

### 通常テーブルの DDL {#regular-table-ddl}

このセクションでは、通常の（非パーティション）テーブルに対して IA ストレージを設定する方法を説明します。

#### 作成時に指定する {#specify-at-create-time}

糖衣構文（推奨）:

```sql
CREATE TABLE t_ia (
    id BIGINT PRIMARY KEY,
    created_at DATETIME NOT NULL,
    payload VARCHAR(256) NOT NULL
) ENGINE=InnoDB STORAGE_CLASS='IA';
```

`ENGINE_ATTRIBUTE` を使用する方法:

```sql
CREATE TABLE t_ia (
    id BIGINT PRIMARY KEY
) ENGINE_ATTRIBUTE='{"storage_class":"IA"}';
```

**競合制約**: `STORAGE_CLASS` の糖衣構文と `ENGINE_ATTRIBUTE` の `storage_class` は、**同時に指定できません**。指定すると、システムはエラーを返して拒否します。

#### 既存テーブルを変更する {#modify-an-existing-table}

```sql
-- Standard → IA
ALTER TABLE t1 STORAGE_CLASS='IA';
ALTER TABLE t1 ENGINE_ATTRIBUTE='{"storage_class":"IA"}';

-- IA → Standard
ALTER TABLE t1 STORAGE_CLASS='STANDARD';
ALTER TABLE t1 ENGINE_ATTRIBUTE='{"storage_class":"STANDARD"}';
```

`ALTER` 操作ではすべてのデータへのアクセスが維持され、変換中も SQL による読み取りと書き込みを実行できます。

### パーティションテーブルの DDL {#partitioned-table-ddl}

パーティションテーブルは `STORAGE_CLASS` の糖衣構文を**サポートしておらず**、`ENGINE_ATTRIBUTE` を使用する必要があります。

パーティション属性では、3 種類のセレクター（混在不可）に加えて、テーブルレベルのデフォルトをサポートします。

| 設定方法 | 構文 | 適用可能なパーティションタイプ | 目的 |
|-|-|-|-|
| テーブルレベルのデフォルト | `{"storage_class":"IA"}` | すべて | すべてのパーティションを一律に IA に設定 |
| パーティション名による指定 | `"names_in":["p1","p2"]` | すべて | パーティション名の正確なリストを指定 |
| 範囲による指定 | `"less_than":"2024-01-01"` | RANGE / RANGE COLUMNS | 境界値でパーティションをマッチ |
| リスト値による指定 | `"values_in":["1","2"]` | LIST / LIST COLUMNS | リスト値でパーティションをマッチ |

#### 例 A: テーブルレベルで IA を設定し、特定のパーティションを Standard に上書きする {#example-a-table-level-ia-with-specific-partitions-overridden-to-standard}

```sql
CREATE TABLE orders (
    order_id BIGINT NOT NULL,
    created_at DATETIME NOT NULL,
    PRIMARY KEY (order_id, created_at)
) ENGINE_ATTRIBUTE='{
    "storage_class":[
        {"tier":"ia"},
        {"tier":"standard","names_in":["p2025","p_future"]}
    ]
}'
PARTITION BY RANGE (YEAR(created_at)) (
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

結果: p2023 / p2024 → IA、p2025 / p_future → Standard。

#### 例 B: range セレクター {#example-b-range-selector}

```sql
CREATE TABLE users (
    user_id BIGINT NOT NULL,
    PRIMARY KEY (user_id)
) ENGINE_ATTRIBUTE='{
    "storage_class":[
        {"tier":"ia","less_than":"2000000"}
    ]
}'
PARTITION BY RANGE (user_id) (
    PARTITION p0 VALUES LESS THAN (1000000),
    PARTITION p1 VALUES LESS THAN (2000000),
    PARTITION p2 VALUES LESS THAN (3000000),
    PARTITION p3 VALUES LESS THAN MAXVALUE
);
```

結果: p0 / p1 → IA、p2 / p3 → Standard。

#### 例 C: list 値セレクター {#example-c-list-value-selector}

```sql
CREATE TABLE order_status_log (
    log_id BIGINT NOT NULL,
    status INT NOT NULL,
    PRIMARY KEY (log_id, status)
) ENGINE_ATTRIBUTE='{
    "storage_class":[
        {"tier":"ia","values_in":["1","2"]}
    ]
}'
PARTITION BY LIST (status) (
    PARTITION p_pending VALUES IN (1),
    PARTITION p_paid VALUES IN (2),
    PARTITION p_shipped VALUES IN (3),
    PARTITION p_completed VALUES IN (4)
);
```

結果: p_pending / p_paid → IA、p_shipped / p_completed → Standard。

#### パーティションセレクタールール {#partition-selector-rules}

- **優先順位**: パーティションレベルの設定は、テーブルレベルの設定を**上書き**します
- **相互排他**: 同じセレクター内で複数のマッチ方法（例: `"names_in"` と `"less_than"`）を同時に使用することはできません。使用するとエラーになります
- **前方互換性**: 後から追加された新しいパーティション（`ADD PARTITION` / `REORGANIZE PARTITION`）は、永続化されたストレージクラスルールに対して自動的に評価されます。一致するパーティションはその設定を継承します

### 表示と監視 {#view-and-monitor}

```sql
-- View DDL definition
SHOW CREATE TABLE t1\G

-- View table-level storage type
SELECT TABLE_NAME, TIDB_STORAGE_CLASS
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'your_database'
  AND TABLE_NAME = 'your_table';

-- View partition-level storage type
SELECT PARTITION_NAME, TIDB_STORAGE_CLASS
FROM INFORMATION_SCHEMA.PARTITIONS
WHERE TABLE_SCHEMA = 'your_database'
  AND TABLE_NAME = 'your_table';
```

#### IA ストレージ容量を監視する {#monitor-ia-storage-space}

TiDB Cloud コンソールで確認します。

- パス: **Overview** > **Monitoring** > **Metrics** > **Instance Overview** (または **Overview** > **Core Metrics**)
- 新しいメトリクス:
    - `Row-based IA Storage` — IA ストレージクラス内のデータのストレージ容量
    - `Row-based Standard Storage` — Standard テーブル容量の合計
- 関係: `Row-based Storage` = `Row-based IA Storage` + `Row-based Standard Storage`

> **Note:**
>
> IA ストレージ容量には、テーブルの L1 以降のより深いレイヤーのみが含まれます。memtable と L0 ファイルはローカルディスク上に残るため、IA ストレージとしてはカウントされません。理由については、[LSM-Tree の書き込みパス](/tidb-cloud/tiered-storage-overview.md#lsm-tree-write-path) を参照してください。

単一テーブルの容量を問い合わせる方法は変更ありません。

> **Note:**
>
> この方法はテーブル統計情報に依存するため、推定誤差が大きくなる可能性があります。また、テーブル全体を対象とするため、結果を `Row-based IA Storage` と直接比較することはできません。

```sql
SELECT TABLE_NAME,
    ROUND(DATA_LENGTH / 1024 / 1024, 2) AS Data_MB,
    ROUND(INDEX_LENGTH / 1024 / 1024, 2) AS Index_MB,
    TABLE_ROWS
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'your_database'
  AND TABLE_NAME = 'your_table'
ORDER BY (DATA_LENGTH + INDEX_LENGTH) DESC;
```

### IA キャッシュレベルを設定する {#configure-the-ia-cache-level}

IA キャッシュレベルは、どれだけの IA データをローカルディスクにキャッシュするかを制御します。レベルが高いほど、より多くのデータがキャッシュされ、コールドリード性能は向上しますが、コストも増加します。

> **Note:**
>
> - IA キャッシュレベルの調整には、階層型ストレージのプライベートプレビュー有効化に加えて、別途許可リストへの登録が必要です。インスタンスで有効にするには、[TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。
> - キャッシュレベルは、個々の論理インスタンスではなく、基盤となる TiKV 物理クラスターのレベルで有効になります。複数の論理インスタンスが同じ物理クラスターを共有している場合、1 つのインスタンスでキャッシュレベルを変更すると、すべてのインスタンスに反映されます。{{{ .premium }}} と {{{ .byoc }}} では、基盤となる TiKV 物理クラスターはお客様専用であるため、他の顧客には影響しません。論理インスタンスレベルでの制御は、今後のリリースで提供予定です。

| キャッシュレベル | ユースケース |
|-|-|
| **Economy** | コールドリードがまれで、ローカルディスクのコストを最小化したい場合 |
| **Default** | システムのデフォルトで、一般的なワークロードに適しています |
| **Balanced** | コストとコールドリードレイテンシーのバランスを取りたい場合 |
| **Deep** | ワークロードにおいてコールドリードレイテンシーが重要な場合 |

キャッシュレベルを変更するには、次の手順を実行します。

1. Cloud Console で **Overview** > **Capacity** に移動し、**Update Capacity** をクリックします。
2. **Storage Acceleration** ブロックで、キャッシュレベルを選択します。
3. **Summary** ペインでコストへの影響を確認し、**Update Capacity** をクリックします。

変更は再起動なしで有効になり、通常は 1 分以内に反映されます。TiDB Cloud が基盤リソースを自動的にプロビジョニングするため、利用可能な空き容量を確認したり、スケーリング方法を選択したりする必要はありません。プロビジョニングには多少時間がかかる場合があります。

{{{ .premium }}} では、各キャッシュレベルに IA ストレージ相当係数があり、請求額の計算時に報告された IA ストレージ使用量へ適用されるため、レベルが高いほどコストも高くなります。{{{ .byoc }}} では係数は適用されません。追加のローカルキャッシュリソースはお客様自身のクラウドアカウント内にプロビジョニングされ、クラウドプロバイダーから課金されます。各レベルの係数については、[TiDB Cloud課金](/tidb-cloud/tidb-cloud-billing.md) を参照してください。

### IA セグメントサイズを調整する（BYOC のみ） {#adjust-the-ia-segment-size-byoc-only}

セグメントは、TiKV がオブジェクトストレージから読み取り、ローカルキャッシュへ書き込む最小単位です。デフォルトサイズは 1 MiB です。

{{{ .byoc }}} では、TiKV 設定パラメーター `kvengine.ia.segment-size` を `128 KiB`、`256 KiB`、`512 KiB`、`1 MiB`、または `2 MiB` に設定できます。このパラメーターは {{{ .premium }}} では使用できません。

`kvengine.ia.segment-size` は起動時にのみ有効になります。変更後は、できればオフピーク時間帯に TiKV ノードのローリング再起動を実行してください。

セグメントサイズを変更しても、オブジェクトストレージ内のファイルが書き換えられることはありません。SST ファイルはオブジェクト全体として保存され、セグメント単位で構成されているわけではないため、変わるのはローカルディスク上での読み取り粒度とキャッシュ粒度だけです。再起動後、ローカルキャッシュはクエリの到着に応じて新しい粒度で徐々に再構築されます。

## 可観測性 {#observability}

ストレージクラス移行の進行状況、`EXPLAIN ANALYZE` フィールド、ステートメントサマリーとスロークエリのメトリクス、クラスターレベルの IA キャッシュ性能パネルを含む IA の可観測性については、[階層型ストレージの可観測性](/tidb-cloud/tiered-storage-observability.md) を参照してください。

## ベストプラクティス {#best-practices}

このセクションでは、階層化戦略、ロールアウト戦略、書き込み最適化、クエリ最適化、キャッシュレベルのチューニング、セグメントサイズの選択、切り戻し時の考慮事項、設定の安定性など、IA ストレージに関する推奨運用プラクティスを説明します。

### 階層化戦略: パーティションレベル IA を優先する {#tiering-strategy-prefer-partition-level-ia}

パーティションテーブルでは、テーブルレベル IA よりも **常にパーティションレベル IA を優先** してください。これにより、コールド/ホット境界を正確に制御できます。

- 過去のコールドパーティション（例: `p2023`）→ IA
- 最近のホットパーティション（例: `p2025`）→ Standard
- 将来のパーティション（例: `p_future`）→ Standard

### ロールアウト戦略: 最も古く最も小さいパーティションから開始する {#rollout-strategy-start-with-the-smallest-oldest-partition}

```
Step 1: Select the oldest and smallest partition → ALTER PARTITION → IA
Step 2: Observe for one full business day (at least 24h)
Step 3: Verify QPS / TPS / P99 Latency / CPU metrics show no degradation
Step 4: Set the next cold partition → IA one by one
Step 5: Repeat Steps 2-4 until all target partitions are covered
```

**すべてのパーティションを一度にまとめて IA に設定しないでください。**

### 書き込み最適化 {#write-optimization}

- このチューニングを適用する前に、同じスレッド数、ワークロード、パーティション分布で並行書き込みをベンチマークしてください。あるテスト環境では、IA パーティションへのランダム書き込みは平均 50k rows/sec、1 つの IA パーティションへの固定単一スレッド書き込みは平均 70k rows/sec でした。ただし、これらの結果を直接比較することはできません。
- 新しくインポートされたデータは、フラッシュまたはコンパクションの後にのみ IA モードへ移行します。インポート直後の大きな範囲クエリでは、コールドキャッシュに遭遇する可能性があります。

これらの数値はテスト環境から得られたものであり、実際の本番シナリオを表すものではありません。正確なデータは、お客様自身の業務テストに基づいて取得してください。

### クエリ最適化 {#query-optimization}

- IA パーティションにまたがるクエリは、**3 パーティション以下** に抑えることを推奨します。これを超えると、応答時間が大幅に悪化する可能性があります
- IA テーブルに対する並行 `SELECT *` フルテーブルスキャンを同時に実行することは避けてください
- `EXPLAIN ANALYZE` とスロークエリを通じて IA リモート読み取り量を監視し、必要に応じて調整してください

### IA キャッシュレベルをチューニングする {#tune-the-ia-cache-level}

キャッシュレベルを変更するかどうかは、**IA Cache Hit Rate** パネルを使って判断します。

- ヒット率が 85% を下回った状態が続く場合は、キャッシュレベルを上げてください。**Balanced** は妥当な開始点です。
- 変更のたびに、再度変更する前に少なくとも 1 営業日分の期間、ヒット率を観察してください。
- ヒット率が一貫して高く、コストを下げたい場合は、キャッシュレベルを **Economy** に下げてください。

このチューニングループで使用するパネルと ステートメントレベルのメトリクスについては、[階層型ストレージの可観測性](/tidb-cloud/tiered-storage-observability.md) を参照してください。

### セグメントサイズを選択する（BYOC のみ） {#choose-the-segment-size-byoc-only}

セグメントサイズは、読み取り増幅とオブジェクトストレージリクエスト数のトレードオフになります。

| セグメントサイズ | キャッシュミスごとの読み取り増幅 | オブジェクトストレージリクエスト | 適した用途 |
|-|-|-|-|
| 1 MiB 未満 | 低い | 多い | リクエストコストが問題にならない場合の、低レイテンシーなオブジェクトストレージに対するポイントクエリ |
| 1 MiB (デフォルト) | 中程度 | 中程度 | 一般的なワークロード |
| 1 MiB より大きい | 高い | 少ない | 十分なネットワーク帯域幅がある大規模範囲スキャン |

このパラメーターを変更する前に、お客様自身のワークロードでベンチマークを行い、ローリング再起動はオフピーク時間帯に実施してください。

### 切り戻し時の考慮事項 {#switch-back-considerations}

- IA → Standard への変換では、すべてのデータをオブジェクトストレージからダウンロードするため、大量のコールドストレージ帯域幅を消費します
- 帯域幅使用量を監視してスムーズな運用を確保してください。必要に応じて、**事前に TiDB Cloud チームへ連絡し**、共同で監視を行ってください
- 変換中も業務 SQL の読み書きには影響しませんが、性能（例: QPS/TPS）にはわずかな影響が出る可能性があります (テスト環境では 5% 未満)
- 開始前に、変更作業に必要な時間枠を見積もるため、`mysql.tidb_storage_class_transition_history` を `state = 'COMPLETED'` で絞り込んで、クラスター上で過去に行われた類似変換の所要時間を確認してください
- 変換中は、`SHOW STORAGE_CLASS TRANSITIONS` を実行して進行状況を追跡し、変換の停止を検出してください

### 設定の安定性 {#configuration-stability}

ストレージクラス設定は安定した状態に保ち、IA と Standard の間で頻繁に切り替えないでください。切り替えのたびに、次の処理が発生します。

- リージョンのリロード
- オブジェクトストレージデータのダウンロード、またはメタデータの再構築
- IA キャッシュデータのフラッシュ

これらの処理の累積コストは無視できません。

前回の変換がまだ実行中の間に逆方向の変換を発行すると、前回の変換は無効になり、それまでの進捗は破棄されます。進行中の変換を反転すると、追加のリージョンのリロードやデータダウンロードが発生する可能性があります。既存のローカルファイルの一部は再利用できるため、追加作業の量は、変換がどこまで進んでいたか、およびどのデータがローカルで引き続き利用可能かによって異なります。不要な I/O とリソース使用量を減らすため、IA と Standard の間で頻繁に切り替えることは避けてください。無効化された変換を識別する方法については、[階層型ストレージの可観測性](/tidb-cloud/tiered-storage-observability.md) を参照してください。

これは、テーブルまたはパーティションのストレージクラスに適用されます。IA キャッシュレベルの調整は別の操作です。これはホットアップデートであり、ストレージクラス間でデータを移動せず、コストと性能の目標に応じて必要な頻度で変更できます。