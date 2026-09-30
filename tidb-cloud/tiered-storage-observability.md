---
title: 階層型ストレージの可観測性
summary: TiDB Cloud Premium または BYOC で階層型ストレージを監視する方法（変換の進行状況、IA 読み取りメトリクス、キャッシュ性能パネルを含む）を学びます。
---

# 階層型ストレージの可観測性

このドキュメントでは、Infrequent Access (IA) ストレージを監視する方法について説明します。これには、ストレージクラス移行の進行状況、SQL レベルでの IA 読み取りメトリクス、クラスター レベルでの IA キャッシュ性能が含まれます。

> **Note:**
>
> 階層型ストレージは、{{{ .premium }}} および {{{ .byoc }}} 向けに **private preview** として提供されており、デフォルトでは無効です。利用するには、[TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) に連絡して、インスタンスで有効化してもらう必要があります。このページで説明している動作は現在のプレビュー実装に基づいており、一般提供 (GA) 前に変更される可能性があります。

## ストレージクラス移行を監視する {#monitor-storage-class-transitions}

このセクションでは、ストレージクラス変換の進行状況を追跡する方法と、過去の変換を確認する方法について説明します。

変換の進行状況は、ストレージクラスを変更する方法にかかわらず、同じ方法で追跡されます。

- `STORAGE_CLASS` 構文シュガー。例: `ALTER TABLE t1 STORAGE_CLASS='IA'`
- `ENGINE_ATTRIBUTE` 形式。例: `ALTER TABLE t1 ENGINE_ATTRIBUTE='{"storage_class":"IA"}'`
- `ENGINE_ATTRIBUTE` を使用したパーティション レベルの変更

パーティションテーブルは `ENGINE_ATTRIBUTE` のみをサポートするため、パーティション変換はテーブル レベルの変換と同じビューに表示されます。テーブルまたはパーティションが最初から IA ストレージクラスで作成された場合、移行するデータがないため、これらのビューには表示されません。

`ALTER TABLE` 文自体は、数秒以内にスキーマ メタデータを更新します。その後のリージョン レベルのデータ移行は TiKV 内で非同期に実行され、DDL ライフサイクルとは分離されているため、`ADMIN SHOW DDL JOBS` では進行状況は報告されません。進行中の変換を追跡するには `SHOW STORAGE_CLASS TRANSITIONS` を使用し、過去および進行中の変換を確認するには `mysql.tidb_storage_class_transition_history` をクエリします。履歴テーブルには、変換開始時に `state = 'RUNNING'` のレコードが挿入され、変換が最終状態に達するとその場で更新されます。

### 進行中の移行を表示する {#view-in-progress-transitions}

```sql
SHOW STORAGE_CLASS TRANSITIONS;
SHOW STORAGE_CLASS TRANSITIONS LIKE 'table_name';
SHOW STORAGE_CLASS TRANSITIONS WHERE DIRECTION = 'TO_STANDARD';
```

`SHOW STORAGE_CLASS TRANSITIONS` は `SELECT * FROM INFORMATION_SCHEMA.TIKV_STORAGE_CLASS_TRANSITIONS` と等価です。

`INFORMATION_SCHEMA.TIKV_STORAGE_CLASS_TRANSITIONS` テーブルには、現在進行中の変換が一覧表示されます。このテーブルには state カラムはありません。含まれるすべての行が進行中の変換だからです。このテーブルには次のカラムがあります。

| カラム | 型 | 説明 |
|-|-|-|
| `TABLE_SCHEMA` | VARCHAR(64) | データベース名 |
| `TABLE_NAME` | VARCHAR(64) | テーブル名 |
| `TABLE_ID` | BIGINT(21) | テーブルの内部 ID |
| `PARTITION_NAME` | VARCHAR(64) | パーティション名。テーブル レベルの変換では値は `NULL` |
| `PARTITION_ID` | BIGINT(21) | パーティションの内部 ID。テーブル レベルの変換では値は `NULL` |
| `DIRECTION` | VARCHAR(16) | 変換方向: `TO_IA` または `TO_STANDARD` |
| `TOTAL_REPLICAS` | BIGINT(21) UNSIGNED | 変換に関与するレプリカの総数。最初の観測が成功する前は値は `NULL` |
| `COMPLETED_REPLICAS` | BIGINT(21) UNSIGNED | 準備完了となったレプリカ数。最初の観測が成功する前は値は `NULL` |
| `PROGRESS` | DOUBLE | `COMPLETED_REPLICAS` を `TOTAL_REPLICAS` で割った比率。`0` から `1` の範囲です。百分率にするには 100 を掛けます。有効な進捗率が観測されるまでは値は `NULL` です。これは `TOTAL_REPLICAS` と `COMPLETED_REPLICAS` が最初に埋まる観測より後になる場合があります |
| `START_TIME` | DATETIME(6) | 変換開始時刻（セッション タイムゾーン） |
| `DURATION` | BIGINT(21) UNSIGNED | 変換開始から現在までの経過時間（秒） |
| `LAST_UPDATE_TIME` | DATETIME(6) | 直近で成功した進捗観測の時刻 |

> **Note:**
>
> - 行が表示されるのは、そのテーブルに対して `ALL` 権限を持っている場合のみです。アクセスできないテーブルの行は、エラーや警告なしでスキップされます。
> - 進捗は 10 秒ごとに収集されるため、値はリアルタイムではありません。

特定の変換の進行状況と経過時間を確認するには、次を実行します。

```sql
SELECT TABLE_NAME, DIRECTION, COMPLETED_REPLICAS, TOTAL_REPLICAS,
       ROUND(PROGRESS * 100, 1) AS PROGRESS_PCT,
       DURATION, LAST_UPDATE_TIME
FROM INFORMATION_SCHEMA.TIKV_STORAGE_CLASS_TRANSITIONS
WHERE TABLE_SCHEMA = 'db_name' AND TABLE_NAME = 'table_name';
```

変換は 1 つの進行中状態を経て、2 つの最終状態のいずれかで終了します。各状態は `mysql.tidb_storage_class_transition_history` にも記録されます。

| State | 記録場所 | 説明 |
|-|-|-|
| `RUNNING` | `INFORMATION_SCHEMA.TIKV_STORAGE_CLASS_TRANSITIONS` および `mysql.tidb_storage_class_transition_history` の `state` カラム | リージョン レベルの変換が進行中です。`INFORMATION_SCHEMA` テーブルにはこの変換のみが一覧表示され、state カラムはありません。変換が `RUNNING` の間、履歴レコードの `finish_time`、`duration`、`total_replicas`、`completed_replicas` は `NULL` です。進捗は `PROGRESS`、`COMPLETED_REPLICAS`、`TOTAL_REPLICAS` で、経過時間は `DURATION` で追跡します |
| `COMPLETED` | `mysql.tidb_storage_class_transition_history` の `state` カラム | すべてのレプリカの準備が完了しています。変換は `INFORMATION_SCHEMA.TIKV_STORAGE_CLASS_TRANSITIONS` から削除され、履歴レコードは `COMPLETED` に更新されます |
| `SUPERSEDED` | `mysql.tidb_storage_class_transition_history` の `state` カラム | 完了前に逆方向の変換が発行されたため、この変換は無効化されました。履歴レコードは `SUPERSEDED` に更新されます |

### 変換が停止しているかどうかを判断する {#determine-whether-a-conversion-is-stuck}

`LAST_UPDATE_TIME`、`COMPLETED_REPLICAS`、`DURATION` をあわせて確認してください。

- `COMPLETED_REPLICAS` が増加し、`LAST_UPDATE_TIME` も更新され続けている場合: 変換は正常に進行しており、単にデータ量が大きいだけです。
- `DURATION` は増え続けているのに、`COMPLETED_REPLICAS` が長時間増加しない場合: TiKV のローリング再起動、一時的なリソース不足、短時間のオブジェクトストレージ利用不可などのシステム例外により、変換が停止している可能性があります。
- `TOTAL_REPLICAS`、`COMPLETED_REPLICAS`、`PROGRESS`、`LAST_UPDATE_TIME` がすべて `NULL` のままの場合: まだ成功した観測が行われていません。これらのカラムはまとめて設定・クリアされるため、`LAST_UPDATE_TIME` だけでは観測の試行が継続しているかどうかは判断できません。代わりに `DURATION` を確認してください。これは変換が追跡されている間は常に増加します。これらのカラムが `NULL` のままで `DURATION` だけが増え続けている場合、ポーリングは継続中ですが、有効な観測結果がまだ返ってきていません。

停止した変換を自分で解消することはできません。[TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) に連絡してください。問題が解消されると、`COMPLETED_REPLICAS` は `COMPLETED` に達するまで再び増加し続け、追加の操作は不要です。

### まだ進行中の変換を逆方向に戻す {#reverse-a-conversion-that-is-still-in-progress}

テーブルまたはパーティションに対して、前回の変換がまだ進行中の間に逆方向の変換を発行すると、前回の変換は無効化されます。

- `INFORMATION_SCHEMA.TIKV_STORAGE_CLASS_TRANSITIONS` では、そのテーブルまたはパーティションの行が新しい変換に置き換えられます。`DIRECTION` には新しい方向が表示され、`START_TIME` は新しい変換の開始時刻になり、進捗は再び最初からカウントされます。そのテーブルまたはパーティションには 1 行だけが残ります。
- 無効化された変換の `mysql.tidb_storage_class_transition_history` 内の履歴レコードは、`state = 'SUPERSEDED'` に更新されます。その `finish_time` は新しい変換の開始時刻になり、`total_replicas` と `completed_replicas` は無効化される直前に最後に観測された値になります。まだ何も観測されていなかった場合、両方のカラムは `NULL` です。

無効化された変換がどこまで進んでいたかを確認するには、履歴テーブルで `state = 'SUPERSEDED'` のレコードをクエリしてください。

### 移行履歴をクエリする {#query-transition-history}

すべての変換は、開始時に `mysql.tidb_storage_class_transition_history` テーブルに記録され、進行に応じてそのレコードが更新されます。このテーブルには次のカラムがあります。

| カラム | 型 | 説明 |
|-|-|-|
| `table_schema` | VARCHAR(64) | データベース名 |
| `table_name` | VARCHAR(64) | テーブル名 |
| `table_id` | BIGINT | テーブルの内部 ID。`start_ts` および `direction` とあわせて、このテーブルの主キーを構成します |
| `partition_name` | VARCHAR(64) | パーティション名。テーブル レベルの変換では値は `NULL` |
| `partition_id` | BIGINT | パーティションの内部 ID。テーブル レベルの変換では値は `NULL` |
| `direction` | VARCHAR(16) | 変換方向: `TO_IA` または `TO_STANDARD` |
| `state` | VARCHAR(16) | 変換状態: `RUNNING`、`COMPLETED`、または `SUPERSEDED` |
| `total_replicas` | BIGINT UNSIGNED | 変換に関与するレプリカの総数。`SUPERSEDED` レコードでは、変換が無効化される前に最後に観測された値、または何も観測されていなければ `NULL` です。変換が `RUNNING` の間は値は `NULL` です |
| `completed_replicas` | BIGINT UNSIGNED | 準備完了だったレプリカ数。`COMPLETED` レコードでは、これは `total_replicas` と等しくなります。`SUPERSEDED` レコードでは、変換が無効化される前に最後に観測された値、または何も観測されていなければ `NULL` です。変換が `RUNNING` の間は値は `NULL` です |
| `schema_version` | BIGINT | この変換が属する TiDB スキーマ バージョン |
| `start_ts` | BIGINT UNSIGNED | 変換の開始 TSO。`table_id` および `direction` とあわせて変換を識別します |
| `start_time` | DATETIME(6) | 変換開始時刻 |
| `finish_time` | DATETIME(6) | 変換が最終状態に達した時刻。`COMPLETED` レコードでは、すべてのレプリカの準備が完了した時刻です。`SUPERSEDED` レコードでは、新しい変換の開始時刻です。変換が最終状態に達するまでは値は `NULL` です |
| `duration` | BIGINT UNSIGNED | 総所要時間（秒）。`SUPERSEDED` レコードでは、これは開始から無効化されるまでの時間のみを表し、完全な変換時間ではありません。変換がまだ `RUNNING` の間は値は `NULL` です |

このテーブルを使用すると、テスト環境の参考値よりも信頼性高く、自分のクラスターで類似の変換にどれくらい時間がかかるかを見積もれます。

```sql
-- Average duration of completed conversions, grouped by direction.
-- Filter on state = 'COMPLETED': the duration of a SUPERSEDED record
-- does not represent a full conversion.
SELECT direction,
       COUNT(*) AS total_conversions,
       ROUND(AVG(duration), 0) AS avg_duration_sec,
       MIN(duration) AS min_duration_sec,
       MAX(duration) AS max_duration_sec
FROM mysql.tidb_storage_class_transition_history
WHERE state = 'COMPLETED'
GROUP BY direction;

-- The most recent finished conversion of a specific table
SELECT table_name, direction, state, duration AS total_duration_sec,
       total_replicas, completed_replicas, start_time, finish_time
FROM mysql.tidb_storage_class_transition_history
WHERE table_schema = 'db_name' AND table_name = 'table_name'
    AND state <> 'RUNNING'
ORDER BY finish_time DESC
LIMIT 1;

-- Conversions that were voided by a reverse conversion
SELECT table_schema, table_name, partition_name, direction,
       completed_replicas, total_replicas, start_time, finish_time, duration
FROM mysql.tidb_storage_class_transition_history
WHERE state = 'SUPERSEDED'
ORDER BY finish_time DESC;
```

#### 履歴レコードの保持 {#retention-of-history-records}

`mysql.tidb_storage_class_transition_history` に保持されるレコードの最大数は、システム変数 [`tidb_storage_class_transition_history_size`](#tidb_storage_class_transition_history_size) によって制御されます。レコード数がこの上限を超えると、`finish_time` の古い順に最も古いレコードから削除されます。保持制御は最大でも 1 分に 1 回しか実行されないため、行数が一時的に上限を超えることがあります。

```sql
-- View the current retention limit
SELECT @@tidb_storage_class_transition_history_size;

-- Retain up to 500 records
SET GLOBAL tidb_storage_class_transition_history_size = 500;
```

#### tidb_storage_class_transition_history_size {#tidb-storage-class-transition-history-size}

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `1000`
- Range: `[100, 100000]`
- この変数は、`mysql.tidb_storage_class_transition_history` テーブルに保持するストレージクラス移行レコードの最大数を設定するために使用されます。値を大きくすると、より長期間履歴を保持できますが、`mysql` データベースで使用する領域も増えます。

## SQL レベルで IA 読み取りを監視する {#monitor-ia-reads-at-the-sql-level}

このセクションでは、`EXPLAIN ANALYZE`、statement summary テーブル、slow query ログ、および TiDB Cloud コンソールで利用できる IA メトリクスについて説明します。

### EXPLAIN ANALYZE {#explain-analyze}

クエリにリモート データ ロードが含まれる場合、`scan_detail` には次のフィールドが含まれます。

```sql
EXPLAIN ANALYZE SELECT * FROM t_ia WHERE id BETWEEN 1 AND 50000;
-- The output includes:
-- ia_remote_read_segment_size: 2320453     -- Total bytes loaded remotely
-- ia_remote_read_segment_count: 3           -- Number of remote loading events
-- ia_remote_read_segment_wait_time: 0.008   -- Remote wait time (seconds)
```

> **Note:**
>
> IA シグナルは、テーブル レベルで安定したフラグではなく、リクエスト単位の読み取りパスの証拠です。同じクエリでも、初回実行では IA 情報が表示されても、キャッシュヒット後には表示されないことがあります。
>
> また、`ia_remote_read_segment_wait_time` はすべてのリモート リクエスト時間の合計です。TiKV の基盤となる並列読み取りメカニズムにより、この値は SQL の実際の実行時間を上回る場合があります。

### Statement summary {#statement-summary}

`STATEMENTS_SUMMARY`, `STATEMENTS_SUMMARY_HISTORY` およびそれらの `CLUSTER_` 対応ビューには、次の IA カラムが含まれます。

| Column | 説明 |
|-|-|
| `IA_EXEC_COUNT` | 少なくとも 1 回の IA リモート読み取りを発生させた実行回数。`EXEC_COUNT` と比較することで、IA データにアクセスした実行の割合を把握できます。たとえば、`IA_EXEC_COUNT = 2` かつ `EXEC_COUNT = 1000` は、実行のうち IA データにアクセスしたのが 0.2% のみであることを意味します |
| `AVG_IA_REMOTE_READ_SEGMENT_COUNT` | 実行ごとのリモート読み取りセグメント数の平均 |
| `MAX_IA_REMOTE_READ_SEGMENT_COUNT` | 1 回の実行で読み取られたリモートセグメント数の最大値 |
| `AVG_IA_REMOTE_READ_SEGMENT_SIZE` | 実行ごとのリモート読み取りデータ量の平均 |
| `MAX_IA_REMOTE_READ_SEGMENT_SIZE` | 1 回の実行でのリモート読み取りデータ量の最大値 |
| `AVG_IA_REMOTE_READ_SEGMENT_WAIT_TIME` | 実行ごとのリモート待機時間の平均 |
| `MAX_IA_REMOTE_READ_SEGMENT_WAIT_TIME` | 1 回の実行でのリモート待機時間の最大値 |

`AVG_` および `MAX_` の各カラムは、各実行でどれだけのデータをリモートから読み取ったかを示し、`IA_EXEC_COUNT` は、そもそも何回の実行がリモート読み取りを行ったかを示します。これら 2 つの観点を組み合わせて使用してください。たとえば、`AVG_IA_REMOTE_READ_SEGMENT_SIZE` は小さい一方で `IA_EXEC_COUNT / EXEC_COUNT` の比率が高いステートメントは、少量のコールドデータに頻繁にアクセスしていることを意味します。

IA テーブルを含まないクエリでは、これらのカラムは `0` または `NULL` になります。

コールドリード実行の割合が最も高いステートメントを見つけるには、次の SQL を使用します。

```sql
SELECT DIGEST_TEXT, EXEC_COUNT, IA_EXEC_COUNT,
       ROUND(IA_EXEC_COUNT / EXEC_COUNT * 100, 2) AS ia_exec_pct,
       AVG_IA_REMOTE_READ_SEGMENT_SIZE
FROM INFORMATION_SCHEMA.CLUSTER_STATEMENTS_SUMMARY_HISTORY
WHERE IA_EXEC_COUNT > 0
ORDER BY ia_exec_pct DESC
LIMIT 10;
```

### Slow queries {#slow-queries}

`INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY` には、次の IA カラムが含まれます。

- `IA_remote_read_segment_count`
- `IA_remote_read_segment_size`
- `IA_remote_read_segment_wait_time`

同じフィールドは `ADMIN SHOW SLOW` の出力でも利用できます。

```sql
ADMIN SHOW SLOW RECENT 10;
ADMIN SHOW SLOW TOP INTERNAL 10;
ADMIN SHOW SLOW TOP ALL 10;
```

フィールドの意味と単位は、`SLOW_QUERY` テーブルと同じです。IA テーブルを含まないクエリでは、値は `NULL` または `0` になります。対応するフィールドは、TiDB Cloud コンソールのスロークエリ詳細にも表示されます。

### SQL statement list in the console {#sql-statement-list-in-the-console}

`IA_EXEC_COUNT` カラムは、SQL ステートメント診断リストにも表示されます。

- **Cloud Console**: **Monitoring** > **Diagnosis** > **SQL Statement**
- **Clinic**: **Diagnosis** > **SQL Statements**

このカラム名は **Exec Count of IA** で、**Executions Count** の直後に配置されるため、2 つの値を直接比較できます。他のカラムと同様に、昇順および降順のソートをサポートします。IA テーブルを含まないステートメントでは、値は `0` です。

## クラスター レベルで IA キャッシュ性能を監視する {#monitor-ia-cache-performance-at-the-cluster-level}

このセクションでは、TiDB Cloud コンソールで IA キャッシュの挙動を確認するためのクラスター レベルのパネルについて説明します。

### IA Cache Performance panels {#ia-cache-performance-panels}

パス: **Monitoring** > **Metrics** > **Instance Overview** > **IA Cache Performance**。

| Panel | 説明 |
|-|-|
| **IA Cache Hit Rate (%)** | クラスター全体の IA キャッシュヒット率。値が 85% を下回ると黄色のインジケーターが表示されます |
| **IA Cache Miss Rate (ops/s)** | IA キャッシュミスの発生頻度。通常、この値は低く保たれます。急増した場合は、大量のコールドリードまたはキャッシュへの負荷を示します |
| **IA Remote Read Segment** | オブジェクトストレージから読み取られたセグメントの頻度 (Count) とデータ量 (Size)。オブジェクトストレージへのリクエスト量と帯域幅消費の評価に使用します |
| **IA Remote Read Segment Wait Time** | 1 回のリモート読み取りの待機時間。P99 と Avg で表示されます。継続的な増加は、オブジェクトストレージのレイテンシー悪化または帯域幅制限を示します |

時間選択ツールで時間範囲を変更すると、より長期的な傾向を観察できます。クラスターに IA テーブルがない場合、パネルには `0%` やエラーの代わりに **No IA data** が表示されます。

単一ステートメントのコールドデータ量を監視するには、**Monitoring** > **Diagnosis** > **Slow Query** > **Coprocessor** にある `IA Remote Read Segment Size` パネルを使用します。

### パネルの見方 {#interpret-the-panels}

キャッシュヒット率は、実際のアクセスパターンに依存します。アクセスが集中していれば 95% を超えることもありますが、アクセスが分散している場合は 95% を下回ることがあります。

- **ヒット率の急低下**: 同時に **IA Cache Miss Rate** が上昇しているか確認してください。同時に上昇していれば、収集上の問題ではなく、コールドリードが実際に増加していることを示します。その後、ステートメントサマリーテーブルの `IA_EXEC_COUNT` を使って、どのステートメントがコールドリードを引き起こしたかを特定します。
- **ヒット率が継続的に低い**: キャッシュがコールドデータによって圧迫されています。IA キャッシュレベルを引き上げるか、IA に設定するデータ量を減らすことを検討してください。[ティアードストレージの設定と管理](/tidb-cloud/tiered-storage-guide.md) を参照してください。
- **テーブルが IA に適しているかの評価**: パーティションを IA に設定した後、少なくとも 1 営業日分は **IA Cache Hit Rate** を観察してください。ヒット率が安定していれば、そのアクセスパターンは IA に適しています。大きな変動や低い平均値は、そのデータへのアクセスが IA に対して分散しすぎていることを意味します。

## 診断ワークフロー {#diagnostic-workflows}

### 変更前に変換ウィンドウを見積もる {#estimate-the-conversion-window-before-a-change}

1. `SHOW STORAGE_CLASS TRANSITIONS` を実行して、他の変換がすでに進行中かどうかを確認します。このテーブルには、進行中の変換のみが表示されます。
2. `mysql.tidb_storage_class_transition_history` をクエリし、`state = 'COMPLETED'` で絞り込んだうえで、クラスター内の類似する過去の変換の `duration` を確認します。
3. 変換中は、`DURATION` と `PROGRESS` を組み合わせて残り時間を見積もります。

### キャッシュヒット率の急低下を調査する {#investigate-a-sudden-drop-in-cache-hit-rate}

1. **IA Cache Hit Rate** の低下を確認し、同時に **IA Cache Miss Rate** が上昇しているかを確認します。
2. ステートメントサマリーテーブルで、`IA_EXEC_COUNT / EXEC_COUNT` の比率が高いステートメントを特定します。
3. 多くのステートメントで同時にこの比率が上昇している場合、分析クエリのバッチが IA テーブルをスキャンし、キャッシュからホットデータを追い出している可能性があります。
4. IA キャッシュレベルを引き上げるか、影響を受けたデータを Standard ストレージに戻すかを判断します。

### テーブルを IA に保持するかどうかを判断する {#decide-whether-to-keep-a-table-in-ia}

1. そのテーブルにアクセスするステートメントについて、`IA_EXEC_COUNT / EXEC_COUNT` を集計します。
2. ほとんどのステートメントでコールドリード比率が高いままであれば、IA に対してキャッシュヒット率が低すぎます。テーブルを Standard に戻すことを検討してください。
3. コールドリード比率が低くても、一部のステートメントが毎回大量のデータを読み取る場合は、テーブル全体を戻すのではなく、それらのステートメントを最適化してください。

## See also {#see-also}

- [階層型ストレージの概要](/tidb-cloud/tiered-storage-overview.md)
- [ティアードストレージの設定と管理](/tidb-cloud/tiered-storage-guide.md)
- [Tiered Storage の制限事項](/tidb-cloud/tiered-storage-limitations.md)
- [Tiered Storage FAQ](/tidb-cloud/tiered-storage-faq.md)