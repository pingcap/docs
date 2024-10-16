---
title: TiCDC Behavior in Splitting UPDATE Events
summary: TiCDC が UPDATE` イベントを分割するかどうかに関する動作の変更について、その理由と影響を含めて紹介します。
---

# UPDATE イベントを分割する際の TiCDC の動作 {#ticdc-behavior-in-splitting-update-events}

## MySQLシンクの<code>UPDATE</code>イベントを分割する {#split-code-update-code-events-for-mysql-sinks}

v7.5.2 以降、MySQL シンクを使用する場合、テーブルのレプリケーション要求を受信したすべての TiCDC ノードは、ダウンストリームへのレプリケーションを開始する前に、PD から現在のタイムスタンプ`thresholdTS`取得します。このタイムスタンプの値に基づいて、TiCDC は`UPDATE`イベントを分割するかどうかを決定します。

-   1 つまたは複数の`UPDATE`変更を含むトランザクションの場合、トランザクション`commitTS`が`thresholdTS`未満であれば、TiCDC は`UPDATE`イベントを`DELETE`イベントと`INSERT`イベントに分割してから、それらを Sorter モジュールに書き込みます。
-   トランザクション`commitTS`が`thresholdTS`以上である`UPDATE`のイベントの場合、TiCDC はそれらを分割しません。詳細については、GitHub の問題[＃10918](https://github.com/pingcap/tiflow/issues/10918)を参照してください。

この動作の変更により、TiCDC が受信した`UPDATE`イベントの順序が誤っている可能性があり、その結果、分割された`DELETE`および`INSERT`のイベントの順序が誤っている可能性がある、ダウンストリーム データの不整合の問題が解決されます。

次の SQL ステートメントを例に挙げます。

```sql
CREATE TABLE t (a INT PRIMARY KEY, b INT);
INSERT INTO t VALUES (1, 1);
INSERT INTO t VALUES (2, 2);

BEGIN;
UPDATE t SET a = 3 WHERE a = 2;
UPDATE t SET a = 2 WHERE a = 1;
COMMIT;
```

この例では、トランザクション内の 2 つの`UPDATE`ステートメントは実行時に順次依存関係を持ちます。主キー`a` `2`から`3`に変更され、次に主キー`a` `1`から`2`に変更されます。このトランザクションが実行されると、上流データベースのレコードは`(2, 1)`と`(3, 2)`なります。

ただし、TiCDC が受信する`UPDATE`イベントの順序は、上流トランザクションの実際の実行順序と異なる場合があります。例:

```sql
UPDATE t SET a = 2 WHERE a = 1;
UPDATE t SET a = 3 WHERE a = 2;
```

-   この動作変更の前は、TiCDC はこれらの`UPDATE`イベントを Sorter モジュールに書き込み、それらを`DELETE` `INSERT`イベントに分割していました。分割後、ダウンストリームでのこれらのイベントの実際の実行順序は次のようになります。

    ```sql
    BEGIN;
    DELETE FROM t WHERE a = 1;
    REPLACE INTO t VALUES (2, 1);
    DELETE FROM t WHERE a = 2;
    REPLACE INTO t VALUES (3, 2);
    COMMIT;
    ```

    ダウンストリームがトランザクションを実行した後、データベース内のレコードは`(3, 2)`になりますが、これはアップストリーム データベース内のレコード ( `(2, 1)`と`(3, 2)` ) と異なり、データの不整合の問題があることを示しています。

-   この動作変更後、TiCDC が対応するテーブルをダウンストリームに複製し始めたときに、トランザクション`commitTS` PD から取得された`thresholdTS`より少ない場合、TiCDC はこれらの`UPDATE`イベントを`DELETE`と`INSERT`イベントに分割してから、Sorter モジュールに書き込みます。Sorter モジュールによるソート後、ダウンストリームでのこれらのイベントの実際の実行順序は次のようになります。

    ```sql
    BEGIN;
    DELETE FROM t WHERE a = 1;
    DELETE FROM t WHERE a = 2;
    REPLACE INTO t VALUES (2, 1);
    REPLACE INTO t VALUES (3, 2);
    COMMIT;
    ```

    ダウンストリームがトランザクションを実行すると、ダウンストリーム データベースのレコードはアップストリーム データベースのレコード ( `(2, 1)`と`(3, 2)`と同じになり、データの一貫性が確保されます。

前の例からわかるように、 `UPDATE`イベントを`DELETE` `INSERT`イベントに分割してから Sorter モジュールに書き込むと、分割後の`INSERT`イベントの前に`DELETE`イベントがすべて実行されるため、TiCDC が受信した`UPDATE`イベントの順序に関係なく、データの一貫性が維持されます。

> **注記：**
>
> この動作変更後、MySQL シンクを使用すると、ほとんどの場合、TiCDC は`UPDATE`イベントを分割しません。その結果、changefeed 実行時に主キーまたは一意キーの競合が発生し、changefeed が自動的に再起動される可能性があります。再起動後、TiCDC は競合する`UPDATE`イベントを`DELETE` `INSERT`イベントに分割してから、Sorter モジュールに書き込みます。これにより、同じトランザクション内のすべてのイベントが正しく順序付けられ、 `DELETE`イベントすべてが`INSERT`イベントより前に来るため、データ レプリケーションが正しく完了します。

## 非MySQLシンクの主キーまたは一意キーの<code>UPDATE</code>イベントを分割する {#split-primary-or-unique-key-code-update-code-events-for-non-mysql-sinks}

### 単一の<code>UPDATE</code>変更を含むトランザクション {#transactions-containing-a-single-code-update-code-change}

v6.5.3、v7.1.1、v7.2.0 以降では、MySQL 以外のシンクを使用する場合、単一の更新変更のみを含むトランザクションで、主キーまたは null 以外の一意のインデックス値が`UPDATE`イベントで変更されると、TiCDC はこのイベントを`DELETE`つと`INSERT`イベントに分割します。詳細については、GitHub の問題[＃9086](https://github.com/pingcap/tiflow/issues/9086)を参照してください。

この変更は主に、CSV および AVRO プロトコルを使用する場合、TiCDC がデフォルトで古い値なしで新しい値のみを出力するという問題に対処します。この問題により、主キーまたは null 以外の一意のインデックス値が変更されると、コンシューマーは新しい値しか受信できず、変更前の値を処理することができなくなります (たとえば、古い値を削除する)。次の SQL を例に挙げます。

```sql
CREATE TABLE t (a INT PRIMARY KEY, b INT);
INSERT INTO t VALUES (1, 1);
UPDATE t SET a = 2 WHERE a = 1;
```

この例では、主キー`a`が`1`から`2`に更新されます。 `UPDATE`イベントが分割されていない場合、CSV および AVRO プロトコルを使用すると、コンシューマーは新しい値`a = 2`のみを取得でき、古い値`a = 1`取得できません。これにより、下流のコンシューマーは古い値`1`削除せずに、新しい値`2`のみを挿入する可能性があります。

### 複数の<code>UPDATE</code>変更を含むトランザクション {#transactions-containing-multiple-code-update-code-changes}

v6.5.4、v7.1.2、v7.4.0 以降では、複数の変更を含むトランザクションの場合、主キーまたは null 以外の一意のインデックス値が`UPDATE`番目のイベントで変更されると、TiCDC はイベントを`DELETE`つと`INSERT`のイベントに分割し、すべてのイベントが`INSERT`イベントの前の`DELETE`のイベントのシーケンスに従うようにします。詳細については、GitHub の問題[＃9430](https://github.com/pingcap/tiflow/issues/9430)を参照してください。

この変更は主に、Kafka シンクまたは他のシンクからリレーショナル データベースにデータ変更を書き込むとき、または同様の操作を実行するときにコンシューマーが遭遇する可能性のある主キーまたは一意キーの競合の潜在的な問題に対処します。この問題は、TiCDC が受信した`UPDATE`のイベントの順序が間違っている可能性があることによって発生します。

次の SQL を例に挙げます。

```sql
CREATE TABLE t (a INT PRIMARY KEY, b INT);
INSERT INTO t VALUES (1, 1);
INSERT INTO t VALUES (2, 2);

BEGIN;
UPDATE t SET a = 3 WHERE a = 1;
UPDATE t SET a = 1 WHERE a = 2;
UPDATE t SET a = 2 WHERE a = 3;
COMMIT;
```

この例では、2 つの行の主キーを交換する 3 つの SQL 文を実行することで、TiCDC は 2 つの更新変更イベント、つまり主キー`a`を`1`から`2`に変更し、主キー`a` `2`から`1`に変更するイベントのみを受信します。コンシューマーがこれら 2 つの`UPDATE`イベントをダウンストリームに直接書き込むと、主キーの競合が発生し、変更フィード エラーが発生します。

したがって、TiCDC はこれら 2 つのイベントを 4 つのイベントに分割し、レコード`(1, 1)`と`(2, 2)`削除し、レコード`(2, 1)`と`(1, 2)`書き込みます。

### 主キーまたは一意キーの<code>UPDATE</code>イベントを分割するかどうかを制御する {#control-whether-to-split-primary-or-unique-key-code-update-code-events}

v6.5.10、v7.1.6、v7.5.3 以降では、MySQL 以外のシンクを使用する場合、TiCDC は、GitHub の問題[＃11211](https://github.com/pingcap/tiflow/issues/11211)で説明されているように、 `output-raw-change-event`パラメータを介してプライマリ キーまたは一意のキー`UPDATE`イベントを分割するかどうかを制御できます。このパラメータの具体的な動作は次のとおりです。

-   `output-raw-change-event = false`設定すると、主キーまたは null 以外の一意のインデックス値が`UPDATE`イベントで変更された場合、TiCDC はイベントを`DELETE`と`INSERT`イベントに分割し、すべてのイベントが`INSERT`イベントの前の`DELETE`イベントのシーケンスに従うようにします。
-   `output-raw-change-event = true`設定すると、TiCDC は`UPDATE`イベントを分割せず、コンシューマー側が[非MySQLシンクの主キーまたは一意キーの`UPDATE`イベントを分割する](/ticdc/ticdc-split-update-behavior.md#split-primary-or-unique-key-update-events-for-non-mysql-sinks)で説明した問題に対処する必要があります。そうしないと、データの不整合が発生するリスクがあります。テーブルの主キーがクラスター化インデックスである場合、主キーの更新は TiDB で`DELETE`と`INSERT`イベントに分割され、このような動作は`output-raw-change-event`パラメータの影響を受けません。

> **注記**
>
> 次の表では、UK/PK は主キーまたは一意キーを表します。

#### リリース 6.5 の互換性 {#release-6-5-compatibility}

| バージョン           | プロトコル   | スプリットUK/PK `UPDATE`イベント                        | UK/PK `UPDATE`イベントを分割しない                     | コメント                                                                             |
| --------------- | ------- | ---------------------------------------------- | -------------------------------------------- | -------------------------------------------------------------------------------- |
| &lt;= v6.5.2    | 全て      | ✗                                              | ✓                                            |                                                                                  |
| v6.5.3 / v6.5.4 | 運河/オープン | ✗                                              | ✓                                            |                                                                                  |
| バージョン6.5.3      | CSV/アブロ | ✗                                              | ✗                                            | 分割しますが、並べ替えは行いません[＃9086](https://github.com/pingcap/tiflow/issues/9658)参照してください。 |
| バージョン6.5.4      | 運河/オープン | ✗                                              | ✗                                            | 複数の変更を含むトランザクションのみを分割して並べ替える                                                     |
| v6.5.5 ～ v6.5.9 | 全て      | ✓                                              | ✗                                            |                                                                                  |
| = v6.5.10       | 全て      | ✓ (デフォルト値: `output-raw-change-event = false` ) | ✓ (オプション: `output-raw-change-event = true` ) |                                                                                  |

#### リリース 7.1 の互換性 {#release-7-1-compatibility}

| バージョン                    | プロトコル   | スプリットUK/PK `UPDATE`イベント                        | UK/PK `UPDATE`イベントを分割しない                     | コメント                                                                             |
| ------------------------ | ------- | ---------------------------------------------- | -------------------------------------------- | -------------------------------------------------------------------------------- |
| バージョン7.1.0               | 全て      | ✗                                              | ✓                                            |                                                                                  |
| バージョン7.1.1               | 運河/オープン | ✗                                              | ✓                                            |                                                                                  |
| バージョン7.1.1               | CSV/アブロ | ✗                                              | ✗                                            | 分割しますが、並べ替えは行いません[＃9086](https://github.com/pingcap/tiflow/issues/9658)参照してください。 |
| v7.1.2 ~ v7.1.5          | 全て      | ✓                                              | ✗                                            |                                                                                  |
| = v7.1.6 (まだリリースされていません) | 全て      | ✓ (デフォルト値: `output-raw-change-event = false` ) | ✓ (オプション: `output-raw-change-event = true` ) |                                                                                  |

#### リリース 7.5 の互換性 {#release-7-5-compatibility}

| バージョン        | プロトコル | スプリットUK/PK `UPDATE`イベント                        | UK/PK `UPDATE`イベントを分割しない                     | コメント |
| ------------ | ----- | ---------------------------------------------- | -------------------------------------------- | ---- |
| &lt;= v7.5.2 | 全て    | ✓                                              | ✗                                            |      |
| = v7.5.3     | 全て    | ✓ (デフォルト値: `output-raw-change-event = false` ) | ✓ (オプション: `output-raw-change-event = true` ) |      |
