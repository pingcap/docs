---
title: SET_VAR
summary: SET_VAR は、単一の SQL 文内でオプティマイザヒントを指定するために使用され、その特定の文の実行計画をより細かく制御できます。これには以下が含まれます。
---

# SET_VAR

SET_VAR は、単一の SQL 文内でオプティマイザヒントを指定するために使用され、その特定の文の実行計画をより細かく制御できます。これには以下が含まれます。

> **Note:**
>
> SET_VAR は今後のリリースで非推奨になる予定です。代わりに [SETTINGS 句](/tidb-cloud-lake/sql/settings-clause.md) の使用を検討してください。

- 設定を一時的に構成し、その SQL 文の実行中にのみ有効にします。SET_VAR で指定した設定は、現在実行中の文の結果にのみ影響し、データベース全体の設定には永続的な影響を与えない点に注意してください。SET_VAR を使用して構成できる利用可能な設定の一覧については、[SHOW SETTINGS](/tidb-cloud-lake/sql/show-settings.md) を参照してください。動作の理解については、次の例を参照してください。

    - [例 1. タイムゾーンを一時的に設定する](#example-1-temporarily-set-timezone)
    - [例 2: COPY INTO の並列処理を制御する](#example-2-control-parallel-processing-for-copy-into)

- *deduplicate_label* ラベルを使用して、[INSERT](/tidb-cloud-lake/sql/insert.md)、[UPDATE](/tidb-cloud-lake/sql/update.md)、または [REPLACE](/tidb-cloud-lake/sql/replace.md) 操作の重複排除動作を制御します。SQL 文に deduplicate_label が含まれるこれらの操作では、{{{ .lake }}} は最初の文のみを実行し、同じ deduplicate_label 値を持つ後続の文は、意図したデータ変更内容に関係なく無視されます。なお、deduplicate_label を設定すると、その効果は 24 時間継続します。deduplicate_label が重複排除にどのように役立つかについては、[例 3: deduplicate_label を設定する](#example-3-set-deduplicate-label) を参照してください。

関連情報:

- [SETTINGS 句](/tidb-cloud-lake/sql/settings-clause.md)
- [SET](/tidb-cloud-lake/sql/set.md)

## 構文 {#syntax}

```sql
/*+ SET_VAR(key=value) SET_VAR(key=value) ... */
```

- ヒントは、SQL 文の先頭となる [SELECT](/tidb-cloud-lake/sql/select.md)、[INSERT](/tidb-cloud-lake/sql/insert.md)、[UPDATE](/tidb-cloud-lake/sql/update.md)、[REPLACE](/tidb-cloud-lake/sql/replace.md)、[MERGE](/tidb-cloud-lake/sql/merge.md)、[DELETE](/tidb-cloud-lake/sql/dml.md)、または [COPY](/tidb-cloud-lake/sql/copy-into-table.md) (INTO) キーワードの直後に記述する必要があります。
- 1 つの SET_VAR には 1 つの Key=Value ペアしか含められません。つまり、1 つの SET_VAR で構成できる設定は 1 つだけです。ただし、複数の SET_VAR ヒントを使用して複数の設定を構成できます。
    - 同じ key を含む複数の SET_VAR ヒントがある場合、最初の Key=Value ペアが適用されます。
    - key の解析またはバインドに失敗した場合、すべてのヒントが無視されます。

## 例 {#examples}

### 例 1: タイムゾーンを一時的に設定する {#example-1-temporarily-set-timezone}

```sql
root@localhost> SELECT TIMEZONE();

SELECT
  TIMEZONE();

┌────────────┐
│ timezone() │
│   String   │
├────────────┤
│ UTC        │
└────────────┘

1 row in 0.011 sec. Processed 1 rows, 1B (91.23 rows/s, 91B/s)

root@localhost> SELECT /*+SET_VAR(timezone='America/Toronto') */ TIMEZONE();

SELECT
  /*+SET_VAR(timezone='America/Toronto') */
  TIMEZONE();

┌─────────────────┐
│    timezone()   │
│      String     │
├─────────────────┤
│ America/Toronto │
└─────────────────┘

1 row in 0.023 sec. Processed 1 rows, 1B (43.99 rows/s, 43B/s)

root@localhost> SELECT TIMEZONE();

SELECT
  TIMEZONE();

┌────────────┐
│ timezone() │
│   String   │
├────────────┤
│ UTC        │
└────────────┘

1 row in 0.010 sec. Processed 1 rows, 1B (104.34 rows/s, 104B/s)
```

### 例 2: COPY INTO の並列処理を制御する {#example-2-control-parallel-processing-for-copy-into}

{{{ .lake }}} では、*max_threads* 設定は、リクエストの実行に使用できるスレッドの最大数を指定します。デフォルトでは、この値は通常、マシンで使用可能な CPU コア数に一致するように設定されます。

COPY INTO を使用して {{{ .lake }}} にデータをロード (load) する際は、COPY INTO コマンドにヒントを埋め込み、*max_threads* パラメータを設定することで、並列処理能力を制御できます。例:

```sql
COPY /*+ set_var(max_threads=6) */ INTO mytable FROM @mystage/ pattern='.*[.]parq' FILE_FORMAT=(TYPE=parquet);
```

### 例 3: deduplicate_label を設定する {#example-3-set-deduplicate-label}

```sql
CREATE TABLE t1(a Int, b bool);
INSERT /*+ SET_VAR(deduplicate_label='datalake') */ INTO t1 (a, b) VALUES(1, false);
SELECT * FROM t1;

a|b|
-+-+
1|0|

UPDATE /*+ SET_VAR(deduplicate_label='datalake') */ t1 SET a = 20 WHERE b = false;
SELECT * FROM t1;

a|b|
-+-+
1|0|

REPLACE /*+ SET_VAR(deduplicate_label='datalake') */ INTO t1 on(a,b) VALUES(40, false);
SELECT * FROM t1;

a|b|
-+-+
1|0|

MERGE /*+ SET_VAR(deduplicate_label='datalake') */ INTO t1 using t2 on t1.a = t2.a when matched then update *;
SELECT * FROM t1;

a|b|
-+-+
1|0|
```