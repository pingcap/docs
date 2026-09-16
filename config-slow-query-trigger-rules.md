---
title: スロークエリのトリガールールを設定する
summary: スロークエリログのトリガールールを定義します。
---

# スロークエリのトリガールールを設定する

<CustomContent platform="tidb">

このドキュメントでは、[`tidb_slow_log_rules`](/system-variables.md#tidb_slow_log_rules) システム変数を使用して、[スロークエリログ](/identify-slow-queries.md) のトリガールールを定義する方法について説明します。

[`tidb_slow_log_rules`](/system-variables.md#tidb_slow_log_rules) は、多次元メトリクスの組み合わせをサポートします。これは、スロークエリログの「対象を絞ったサンプリング」や「問題の再現」に適しており、特定のメトリクスの組み合わせに基づいて対象のステートメントをフィルタリングできます。

TiDB Self-Managed では、スロークエリログのトリガー動作は `tidb_slow_log_rules` の設定に依存します。

- 現在のセッションに適用可能な `tidb_slow_log_rules` ルールがない場合（この変数が設定されていない、または設定済みのルールのいずれもセッションに適用されない場合）、スロークエリのログ出力は引き続き [`tidb_slow_log_threshold`](/system-variables.md#tidb_slow_log_threshold)（ミリ秒）に依存します。
- 現在のセッションに適用可能な `tidb_slow_log_rules` ルールが1つでもある場合、スロークエリのログ出力はルールのマッチ結果によって決まり、[`tidb_slow_log_threshold`](/system-variables.md#tidb_slow_log_threshold) は無視されます。

</CustomContent>
<CustomContent platform="tidb-cloud">

[TiDB Cloud コンソール](https://tidbcloud.com/) では、[**Diagnosis**](/tidb-cloud/tune-performance.md#view-the-diagnosis-page) ページの [**Slow Query**](/tidb-cloud/tune-performance.md#slow-query) タブでスロークエリを確認できます。

デフォルトでは、300 ミリ秒を超える SQL クエリはスロークエリと見なされます。スロークエリのトリガールールを設定するには、[`tidb_slow_log_rules`](/system-variables.md#tidb_slow_log_rules) システム変数を変更します。

[`tidb_slow_log_rules`](/system-variables.md#tidb_slow_log_rules) は、多次元メトリクスの組み合わせをサポートします。これは、スロークエリの「対象を絞ったサンプリング」や「問題の再現」に適しており、特定のメトリクスの組み合わせに基づいて対象のステートメントをフィルタリングできます。

</CustomContent>

## 例 {#examples}

- 標準形式（`SESSION` スコープ）:

    ```sql
    SET SESSION tidb_slow_log_rules = 'Query_time: 0.5, Is_internal: false';
    ```

- 無効な `SESSION` ルール（`SESSION` スコープは `Conn_ID` をサポートしません）:

    ```sql
    SET SESSION tidb_slow_log_rules = 'Conn_ID: 12, Query_time: 0.5, Is_internal: false';
    ```

<CustomContent platform="tidb">

- グローバルルール（すべての接続に適用）:

    ```sql
    SET GLOBAL tidb_slow_log_rules = 'Query_time: 0.5, Is_internal: false';
    ```

- 特定の接続向けのグローバルルール（2 つの接続 `Conn_ID:11` と `Conn_ID:12` にそれぞれ別々に適用）:

    ```sql
    SET GLOBAL tidb_slow_log_rules = 'Conn_ID: 11, Query_time: 0.5, Is_internal: false; Conn_ID: 12, Query_time: 0.6, Process_time: 0.3, DB: db1';
    ```

</CustomContent>

<CustomContent platform="tidb-cloud" plan="dedicated">

- グローバルルール（すべての接続に適用）:

    ```sql
    SET GLOBAL tidb_slow_log_rules = 'Query_time: 0.5, Is_internal: false';
    ```

- 特定の接続向けのグローバルルール（2 つの接続 `Conn_ID:11` と `Conn_ID:12` にそれぞれ別々に適用）:

    ```sql
    SET GLOBAL tidb_slow_log_rules = 'Conn_ID: 11, Query_time: 0.5, Is_internal: false; Conn_ID: 12, Query_time: 0.6, Process_time: 0.3, DB: db1';
    ```

</CustomContent>

## 統一されたルール構文と型制約 {#unified-rule-syntax-and-type-constraints}

- ルール数の上限と区切り: サポートされる各スコープには最大 10 個のルールを含めることができます。ルールは `;` で区切ります。
- 条件形式: 各条件は `field_name:value` 形式を使用します。1 つのルール内の複数条件は `,` で区切ります。
- フィールド名は大文字と小文字を区別しません。フィールド名内のアンダースコアやその他の文字はそのまま保持されます。

<CustomContent platform="tidb">

TiDB Self-Managed は、`tidb_slow_log_rules` に対して `SESSION` ルールと `GLOBAL` ルールの両方をサポートします。1 つのセッションでは、2 つのスコープをまたいで最大 20 個の有効なルールを持つことができます。`SESSION` ルールは `Conn_ID` をサポートせず、このフィールドをサポートするのは `GLOBAL` ルールのみです。

</CustomContent>

<CustomContent platform="tidb-cloud" plan="dedicated">

TiDB Cloud Dedicated は、`tidb_slow_log_rules` に対して `SESSION` ルールと `GLOBAL` ルールの両方をサポートします。1 つのセッションでは、2 つのスコープをまたいで最大 20 個の有効なルールを持つことができます。`SESSION` ルールは `Conn_ID` をサポートせず、このフィールドをサポートするのは `GLOBAL` ルールのみです。

</CustomContent>

<CustomContent platform="tidb-cloud" plan="essential,premium">

TiDB Cloud Essential と TiDB Cloud Premium は、`tidb_slow_log_rules` に対して `SESSION` ルールのみをサポートします。したがって、`GLOBAL` ルールでのみ使用可能な `Conn_ID` はサポートされません。

</CustomContent>

- マッチングの意味:
    - `Conn_ID` を除く数値フィールドは `>=` でマッチします。`Conn_ID`、文字列フィールド、ブールフィールドは等価比較（`=`）でマッチします。
    - `DB` と `Resource_group` のマッチングでは大文字と小文字を区別しません。
    - `>`、`<`、`!=` などの明示的な演算子はサポートされません。

型制約は次のとおりです。

- 数値型（`int64`、`uint64`、`float64`）では、値は `0` 以上である必要があります。負の値はパースエラーになります。
    - `int64`: 最大値は `2^63-1` です。
    - `uint64`: 最大値は `2^64-1` です。
    - `float64`: 値は有限かつ非負である必要があります。最大値はおよそ `1.79e308` です。`NaN` や `Inf`、`-Inf` などの無限値は無効であり、エラーになります。
- `bool`: `true`/`false`、`1`/`0`、`t`/`f` をサポートします（大文字と小文字は区別しません）。
- `string`: 現時点では、引用符（シングルまたはダブル）で囲んだ場合でも、区切り文字 `,`（条件区切り）または `;`（ルール区切り）を含む文字列はサポートされません。エスケープはサポートされません。
- 重複フィールド: 同じフィールドが 1 つのルール内で複数回指定された場合、最後に出現したものが有効になります。

## サポートされるフィールド {#supported-fields}

以下の表のフィールドは、特に明記がない限り、[統一されたルール構文と型制約](#unified-rule-syntax-and-type-constraints) で説明した一般的なマッチングルールと型ルールに従います。

| フィールド名 | 型 | 単位 | 説明 |
| --- | --- | --- | --- |
| `Conn_ID` | `uint` | count | 接続 ID（セッション ID）です。このフィールドは完全一致でマッチします。たとえば、`Conn_ID:3` はセッション ID が `3` のログにのみマッチします。このフィールドは `GLOBAL` ルールでのみサポートされます。 |
| `Session_alias` | `string` | none | 現在のセッションのエイリアスです。 |
| `DB` | `string` | none | 現在のデータベースです。マッチングでは大文字と小文字を区別しません。 |
| `Exec_retry_count` | `uint` | count | このステートメントのリトライ回数です。このフィールドは通常、ロック取得に失敗したときにステートメントが再試行される悲観的トランザクション向けです。 |
| `Query_time` | `float` | second | ステートメントの実行時間です。 |
| `Parse_time` | `float` | second | ステートメントのパース時間です。 |
| `Compile_time` | `float` | second | クエリ最適化にかかった時間です。 |
| `Rewrite_time` | `float` | second | このステートメントのクエリ書き換えに消費された時間です。 |
| `Optimize_time` | `float` | second | 実行計画の最適化に消費された時間です。 |
| `Wait_TS` | `float` | second | トランザクションのタイムスタンプ取得を待機した時間です。 |
| `Is_internal` | `bool` | none | SQL ステートメントが TiDB 内部のものかどうかを示します。`true` はステートメントが TiDB 内部で実行されたことを示し、`false` はユーザーによって実行されたことを示します。 |
| `Digest` | `string` | none | SQL ステートメントのフィンガープリントです。 |
| `Plan_digest` | `string` | none | 実行計画の digest です。 |
| `Num_cop_tasks` | `int` | count | このステートメントによって送信されたコプロセッサータスクの数です。 |
| `Mem_max` | `int` | bytes | SQL ステートメントの実行期間中に使用された最大メモリ空間です。 |
| `Disk_max` | `int` | bytes | SQL ステートメントの実行期間中に使用された最大ディスク空間です。 |
| `Write_sql_response_total` | `float` | second | このステートメントが結果をクライアントへ返送するのに消費した時間です。 |
| `Succ` | `bool` | none | ステートメントが正常に実行されたかどうかを示します。 |
| `Resource_group` | `string` | none | ステートメントがバインドされているリソースグループです。マッチングでは大文字と小文字を区別しません。 |
| `KV_total` | `float` | second | このステートメントによる TiKV または TiFlash へのすべての RPC リクエストに費やされた時間です。 |
| `PD_total` | `float` | second | このステートメントによる PD へのすべての RPC リクエストに費やされた時間です。 |
| `Process_time` | `float` | second | TiKV における SQL ステートメントの合計処理時間です。データは TiKV に並行して送信されるため、この値は `Query_time` を超える場合があります。 |
| `Backoff_time` | `float` | second | ステートメントがリトライを必要とするエラーに遭遇した際、再試行前に待機した時間です。一般的なエラーには、ロック競合、リージョン分割、TiKV サーバーのビジー状態などがあります。 |
| `Total_keys` | `uint` | count | コプロセッサーがスキャンしたキー数です。 |
| `Process_keys` | `uint` | count | コプロセッサーが処理したキー数です。`Total_keys` と比べて、`Process_keys` には MVCC の古いバージョンは含まれません。`Process_keys` と `Total_keys` の差が大きい場合、多数の古いバージョンが存在することを示します。 |
| `cop_mvcc_read_amplification` | `float` | ratio | MVCC 読み取り増幅率で、`Total_keys / Process_keys` として計算されます。 |
| `Prewrite_time` | `float` | second | 2 フェーズトランザクションコミットの第 1 フェーズ（prewrite）の継続時間です。 |
| `Commit_time` | `float` | second | 2 フェーズトランザクションコミットの第 2 フェーズ（commit）の継続時間です。 |
| `Write_keys` | `uint` | count | トランザクションが TiKV の Write CF に書き込むキー数です。 |
| `Write_size` | `uint` | bytes | トランザクションのコミット時に書き込まれるキーまたは値の合計サイズです。 |
| `Prewrite_region` | `uint` | count | 2 フェーズトランザクションコミットの第 1 フェーズ（prewrite）に関与する TiKV リージョン数です。各リージョンは 1 回のリモートプロシージャコールを発生させます。 |

## 有効時の動作とマッチ順序 {#effective-behavior-and-matching-order}

- `tidb_slow_log_rules` を設定すると、新しいルールが追加されるのではなく、指定したスコープ内の既存ルールが上書きされます。
- `tidb_slow_log_rules` に空文字列を設定すると、指定したスコープ内のルールがクリアされます。
- 複数ルールは `OR` で結合され、1 つのルール内の複数フィールド条件は `AND` で結合されます。
- SQL 実行時間を引き続きスロークエリログ出力の条件として使用したい場合は、ルール内で `Query_time` を使用し、単位が秒であることに注意してください。

<CustomContent platform="tidb">

TiDB Self-Managed は、`tidb_slow_log_rules` に対して `SESSION` ルールと `GLOBAL` ルールの両方をサポートします。

- 現在のセッションに、`SESSION` ルール、現在の `Conn_ID` に対する `GLOBAL` ルール、または `Conn_ID` を持たない汎用 `GLOBAL` ルールなど、適用可能なルールが 1 つでもある場合、スロークエリログの出力はルールのマッチ結果によって決まり、`tidb_slow_log_threshold` は無視されます。
- 現在のセッションに適用可能なルールがない場合、たとえば `SESSION` ルールと `GLOBAL` ルールの両方が空である場合や、現在の `Conn_ID` に一致しない `GLOBAL` ルールのみが設定されている場合、スロークエリのログ出力は引き続き `tidb_slow_log_threshold` に依存します。`tidb_slow_log_threshold` の単位はミリ秒です。
- TiDB はまず `SESSION` ルールをマッチします。どれも一致しない場合、TiDB は次に現在の `Conn_ID` に対する `GLOBAL` ルールをマッチし、その後 `Conn_ID` を持たない汎用 `GLOBAL` ルールをマッチします。
- `SHOW VARIABLES LIKE 'tidb_slow_log_rules'` と `SELECT @@SESSION.tidb_slow_log_rules` は `SESSION` ルールのテキストを返します。未設定の場合は空文字列を返します。`SELECT @@GLOBAL.tidb_slow_log_rules` は `GLOBAL` ルールのテキストを返します。

</CustomContent>

<CustomContent platform="tidb-cloud" plan="dedicated">

TiDB Cloud Dedicated は、`tidb_slow_log_rules` に対して `SESSION` ルールと `GLOBAL` ルールの両方をサポートします。

- 現在のセッションに、`SESSION` ルール、現在の `Conn_ID` に対する `GLOBAL` ルール、または `Conn_ID` を持たない汎用 `GLOBAL` ルールなど、適用可能なルールが 1 つでもある場合、スロークエリログの出力はルールのマッチ結果によって決まります。
- 現在のセッションに適用可能なルールがない場合、たとえば `SESSION` ルールと `GLOBAL` ルールの両方が空である場合や、現在の `Conn_ID` に一致しない `GLOBAL` ルールのみが設定されている場合、スロークエリログのルールはデフォルトのものにフォールバックします。つまり、300 ミリ秒を超える SQL クエリはスロークエリと見なされます。
- TiDB はまず `SESSION` ルールをマッチします。どれも一致しない場合、TiDB は次に現在の `Conn_ID` に対する `GLOBAL` ルールをマッチし、その後 `Conn_ID` を持たない汎用 `GLOBAL` ルールをマッチします。
- `SHOW VARIABLES LIKE 'tidb_slow_log_rules'` と `SELECT @@SESSION.tidb_slow_log_rules` は `SESSION` ルールのテキストを返します。未設定の場合は空文字列を返します。`SELECT @@GLOBAL.tidb_slow_log_rules` は `GLOBAL` ルールのテキストを返します。

</CustomContent>

<CustomContent platform="tidb-cloud" plan="essential,premium">

TiDB Cloud Essential と TiDB Cloud Premium は、`tidb_slow_log_rules` に対して `SESSION` ルールのみをサポートします。

- 現在のセッションに `SESSION` ルールが 1 つでもある場合、スロークエリログの出力はルールのマッチ結果によって決まります。
- `SHOW VARIABLES LIKE 'tidb_slow_log_rules'` と `SELECT @@SESSION.tidb_slow_log_rules` は `SESSION` ルールのテキストを返します。未設定の場合は空文字列を返します。

</CustomContent>

## 推奨事項 {#recommendations}

- `tidb_slow_log_rules` は、単一しきい値方式を置き換えるために設計されています。多次元メトリクス条件の組み合わせをサポートし、スロークエリログ出力をより柔軟かつきめ細かく制御できます。

- 1 台の TiDB ノード（16 CPU コア、48 GiB メモリ）と 3 台の TiKV ノード（各 16 CPU コア、48 GiB メモリ）を備えた十分なリソースのあるテスト環境において、sysbench テストを繰り返した結果、多次元のスロークエリログルールによって 30 分以内に数百万件のスローログエントリが生成される場合でも、パフォーマンスへの影響は小さいことが示されています。ただし、ログ量が数千万件に達すると、TPS は大幅に低下し、レイテンシーも顕著に増加します。したがって、業務ワークロードが高い場合や CPU とメモリリソースが限界に近い場合は、過度に広いルールによるログの氾濫を避けるため、`tidb_slow_log_rules` を慎重に設定してください。 <CustomContent platform="tidb">ログ出力レートを制限する必要がある場合は、[`tidb_slow_log_max_per_sec`](/system-variables.md#tidb_slow_log_max_per_sec) を使用してスロットリングし、業務パフォーマンスへの影響を軽減してください。</CustomContent>