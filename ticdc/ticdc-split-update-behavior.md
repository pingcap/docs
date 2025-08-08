---
title: TiCDC Behavior in Splitting UPDATE Events
summary: TiCDC が UPDATE` イベントを分割するかどうかに関する動作の変更について、その理由と影響を含めて紹介します。
---

# TiCDC の UPDATE イベントの分割動作 {#ticdc-behavior-in-splitting-update-events}

## MySQLシンクの<code>UPDATE</code>イベントを分割する {#split-code-update-code-events-for-mysql-sinks}

v6.5.10、v7.1.6、v7.5.2、v8.1.1、v8.2.0以降では、MySQLシンクを使用する場合、テーブルのレプリケーション要求を受信したTiCDCノードは、下流へのレプリケーションを開始する前に、PDから現在のタイムスタンプ`thresholdTS`取得します。このタイムスタンプの値に基づいて、TiCDCは`UPDATE`イベントを分割するかどうかを決定します。

-   1 つまたは複数の`UPDATE`変更を含むトランザクションの場合、トランザクション`commitTS` `thresholdTS`未満であれば、TiCDC は`UPDATE`イベントを`DELETE`イベントと`INSERT`イベントに分割してから、それらを Sorter モジュールに書き込みます。
-   トランザクション`commitTS`が`thresholdTS`以上であるイベントが`UPDATE`ある場合、TiCDC はそれらを分割しません。詳細については、GitHub の問題[＃10918](https://github.com/pingcap/tiflow/issues/10918)参照してください。

> **注記：**
>
> v8.1.0では、MySQL Sinkを使用する場合、TiCDCは`thresholdTS`値に基づいて`UPDATE`イベントを分割するかどうかを決定しますが、 `thresholdTS`取得方法は異なります。具体的には、v8.1.0では、 `thresholdTS` TiCDC起動時にPDから取得される現在のタイムスタンプですが、この方法はマルチノードシナリオでデータの不整合の問題を引き起こす可能性があります。詳細については、GitHubのissue [＃11219](https://github.com/pingcap/tiflow/issues/11219)ご覧ください。

この動作の変更 (つまり、 `thresholdTS`に基づいて`UPDATE`イベントを分割するかどうかを決定する) により、TiCDC が受信した`UPDATE`イベントの順序が正しくない可能性があり、その結果、分割された`DELETE`と`INSERT`イベントの順序が間違ってしまう可能性がある、下流のデータの不整合の問題が解決されます。

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

この例では、トランザクション内の2つの`UPDATE`文は実行時に順次依存関係を持ちます。主キー`a` `2`から`3`に変更され、次に主キー`a` `1`から`2`に変更されます。このトランザクションの実行後、上流データベースのレコードは`(2, 1)`と`(3, 2)`なります。

ただし、TiCDC が受信する`UPDATE`イベントの順序は、上流トランザクションの実際の実行順序と異なる場合があります。例:

```sql
UPDATE t SET a = 2 WHERE a = 1;
UPDATE t SET a = 3 WHERE a = 2;
```

-   この動作変更前、TiCDCはこれらの`UPDATE`イベントをSorterモジュールに書き込み、その後`DELETE`つと`INSERT`イベントに分割していました。分割後、下流におけるこれらのイベントの実際の実行順序は以下のようになります。

    ```sql
    BEGIN;
    DELETE FROM t WHERE a = 1;
    REPLACE INTO t VALUES (2, 1);
    DELETE FROM t WHERE a = 2;
    REPLACE INTO t VALUES (3, 2);
    COMMIT;
    ```

    ダウンストリームがトランザクションを実行した後、データベース内のレコードは`(3, 2)`なりますが、これはアップストリーム データベースのレコード ( `(2, 1)`と`(3, 2)` ) と異なり、データの不整合の問題があることを示しています。

-   この動作変更後、TiCDCが対応するテーブルを下流にレプリケーションし始める際に、トランザクション`commitTS` PDからフェッチされた`thresholdTS`より小さい場合、TiCDCはこれらの`UPDATE`イベントを`DELETE`つと`INSERT`イベントに分割してからSorterモジュールに書き込みます。Sorterモジュールによるソート後、下流におけるこれらのイベントの実際の実行順序は以下のようになります。

    ```sql
    BEGIN;
    DELETE FROM t WHERE a = 1;
    DELETE FROM t WHERE a = 2;
    REPLACE INTO t VALUES (2, 1);
    REPLACE INTO t VALUES (3, 2);
    COMMIT;
    ```

    ダウンストリームがトランザクションを実行すると、ダウンストリーム データベースのレコードはアップストリーム データベースのレコード ( `(2, 1)`と`(3, 2)`と同じになり、データの一貫性が確保されます。

前の例からわかるように、 `UPDATE`イベントを`DELETE`つと`INSERT`イベントに分割してから Sorter モジュールに書き込むと、分割後の`INSERT`イベントの前に`DELETE`イベントすべてが実行されるようになり、TiCDC が受信した`UPDATE`イベントの順序に関係なく、データの一貫性が維持されます。

> **注記：**
>
> この動作変更後、MySQLシンクを使用する場合、TiCDCはほとんどの場合、 `UPDATE`イベントを分割しません。その結果、変更フィード実行時に主キーまたは一意キーの競合が発生し、変更フィードが自動的に再起動される可能性があります。再起動後、TiCDCは競合する`UPDATE`イベントを`DELETE`つと`INSERT`イベントに分割してから、Sorterモジュールに書き込みます。これにより、同一トランザクション内のすべてのイベントが正しく順序付けされ、 `DELETE`イベントすべてが`INSERT`イベントの前に配置されるため、データレプリケーションが正しく完了します。

## MySQL以外のシンクの主キーまたは一意キーの<code>UPDATE</code>イベントを分割する {#split-primary-or-unique-key-code-update-code-events-for-non-mysql-sinks}

### 単一の<code>UPDATE</code>変更を含むトランザクション {#transactions-containing-a-single-code-update-code-change}

v6.5.3、v7.1.1、v7.2.0以降、MySQL以外のシンクを使用する場合、単一の更新変更のみを含むトランザクションにおいて、主キーまたはnull以外の一意のインデックス値が`UPDATE`イベントで変更されると、TiCDCはこのイベントを`DELETE`つと`INSERT`イベントに分割します。詳細については、GitHubのissue [＃9086](https://github.com/pingcap/tiflow/issues/9086)ご覧ください。

この変更は主に、CSVおよびAVROプロトコル使用時にTiCDCがデフォルトで新しい値のみを出力し、古い値は出力しないという問題に対処します。この問題により、主キーまたは非NULLの一意のインデックス値が変更された場合、コンシューマーは新しい値しか受信できず、変更前の値を処理する（例えば、古い値を削除する）ことができなくなります。次のSQLを例に挙げましょう。

```sql
CREATE TABLE t (a INT PRIMARY KEY, b INT);
INSERT INTO t VALUES (1, 1);
UPDATE t SET a = 2 WHERE a = 1;
```

この例では、主キー`a`が`1`から`2`に更新されます。イベント`UPDATE`が分割されていない場合、CSV プロトコルおよび AVRO プロトコルを使用する場合、コンシューマーは新しい値`a = 2`のみを取得でき、古い値`a = 1`取得できません。そのため、下流のコンシューマーは古い値`1`を削除せずに、新しい値`2`のみを挿入する可能性があります。

### 複数の<code>UPDATE</code>変更を含むトランザクション {#transactions-containing-multiple-code-update-code-changes}

v6.5.4、v7.1.2、v7.4.0以降、複数の変更を含むトランザクションにおいて、 `UPDATE`イベントで主キーまたはNULL以外の一意のインデックス値が変更された場合、TiCDCはイベントを`DELETE`と`INSERT`イベントに分割し、すべてのイベントが`INSERT`のイベントの前の`DELETE`のイベントのシーケンスに従うようにします。詳細については、GitHubのissue [＃9430](https://github.com/pingcap/tiflow/issues/9430)ご覧ください。

この変更は主に、Kafkaシンクまたはその他のシンクからリレーショナルデータベースへのデータ変更の書き込み時、あるいは同様の操作を実行する際にコンシューマーが遭遇する可能性のある、主キーまたは一意キーの競合に関する潜在的な問題に対処します。この問題は、TiCDCが受信した`UPDATE`イベントの順序が誤っている可能性があることに起因します。

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

この例では、2つの行の主キーを交換する3つのSQL文を実行することで、TiCDCは主キー`a` `1`から`2`に変更し、主キー`a` `2`から`1`に変更するという2つの更新変更イベントのみを受け取ります。コンシューマーがこれらの2つの`UPDATE`イベントをダウンストリームに直接書き込むと、主キーの競合が発生し、変更フィードエラーが発生します。

したがって、TiCDC はこれら 2 つのイベントを 4 つのイベントに分割します。つまり、レコード`(1, 1)`と`(2, 2)`削除し、レコード`(2, 1)`と`(1, 2)`書き込みます。

### 主キーまたは一意キーの<code>UPDATE</code>イベントを分割するかどうかを制御する {#control-whether-to-split-primary-or-unique-key-code-update-code-events}

v6.5.10、v7.1.6、v7.5.3、v8.1.1以降、MySQL以外のシンクを使用する場合、TiCDCはGitHub Issue [＃11211](https://github.com/pingcap/tiflow/issues/11211)に記載されているように、 `output-raw-change-event`パラメータを介して主キーまたは一意キーの`UPDATE`イベントを分割するかどうかを制御できるようになりました。このパラメータの具体的な動作は次のとおりです。

-   `output-raw-change-event = false`設定すると、主キーまたは null 以外の一意のインデックス値が`UPDATE`イベントで変更された場合、TiCDC はイベントを`DELETE`と`INSERT`イベントに分割し、すべてのイベントが`INSERT`イベントの前の`DELETE`イベントのシーケンスに従うようにします。
-   `output-raw-change-event = true`設定すると、TiCDCは`UPDATE`イベントを分割せず、 [MySQL以外のシンクの主キーまたは一意キーの`UPDATE`イベントを分割する](/ticdc/ticdc-split-update-behavior.md#split-primary-or-unique-key-update-events-for-non-mysql-sinks)で説明した問題への対処はコンシューマー側で行います。そうしないと、データの不整合が発生するリスクがあります。テーブルの主キーがクラスター化インデックスである場合、主キーへの更新はTiDB内で依然として`DELETE`つと`INSERT`イベントに分割されますが、この動作は`output-raw-change-event`パラメータの影響を受けません。

> **注記**
>
> 次の表では、UK/PK は主キーまたは一意キーを表します。

#### リリース6.5の互換性 {#release-6-5-compatibility}

| バージョン           | プロトコル   | UK/PK `UPDATE`イベントの分割                          | UK/ `UPDATE`イベントを分割しない                       | コメント                                                                               |
| --------------- | ------- | ---------------------------------------------- | -------------------------------------------- | ---------------------------------------------------------------------------------- |
| バージョン6.5.2以下    | 全て      | ✗                                              | ✓                                            |                                                                                    |
| v6.5.3 / v6.5.4 | 運河/オープン | ✗                                              | ✓                                            |                                                                                    |
| バージョン6.5.3      | CSV/アブロ | ✗                                              | ✗                                            | 分割しますが、並べ替えは行いません。1を参照してください[＃9086](https://github.com/pingcap/tiflow/issues/9658) |
| バージョン6.5.4      | 運河/オープン | ✗                                              | ✗                                            | 複数の変更を含むトランザクションのみを分割して並べ替える                                                       |
| v6.5.5 ～ v6.5.9 | 全て      | ✓                                              | ✗                                            |                                                                                    |
| = v6.5.10       | 全て      | ✓ (デフォルト値: `output-raw-change-event = false` ) | ✓ （オプション： `output-raw-change-event = true` ） |                                                                                    |

#### リリース7.1の互換性 {#release-7-1-compatibility}

| バージョン           | プロトコル   | UK/PK `UPDATE`イベントの分割                          | UK/ `UPDATE`イベントを分割しない                       | コメント                                                                               |
| --------------- | ------- | ---------------------------------------------- | -------------------------------------------- | ---------------------------------------------------------------------------------- |
| バージョン7.1.0      | 全て      | ✗                                              | ✓                                            |                                                                                    |
| バージョン7.1.1      | 運河/オープン | ✗                                              | ✓                                            |                                                                                    |
| バージョン7.1.1      | CSV/アブロ | ✗                                              | ✗                                            | 分割しますが、並べ替えは行いません。1を参照してください[＃9086](https://github.com/pingcap/tiflow/issues/9658) |
| v7.1.2 ~ v7.1.5 | 全て      | ✓                                              | ✗                                            |                                                                                    |
| = v7.1.6        | 全て      | ✓ (デフォルト値: `output-raw-change-event = false` ) | ✓ （オプション： `output-raw-change-event = true` ） |                                                                                    |

#### リリース7.5の互換性 {#release-7-5-compatibility}

| バージョン        | プロトコル | UK/PK `UPDATE`イベントの分割                          | UK/ `UPDATE`イベントを分割しない                       | コメント |
| ------------ | ----- | ---------------------------------------------- | -------------------------------------------- | ---- |
| バージョン7.5.2以下 | 全て    | ✓                                              | ✗                                            |      |
| = v7.5.3     | 全て    | ✓ (デフォルト値: `output-raw-change-event = false` ) | ✓ （オプション： `output-raw-change-event = true` ） |      |

#### リリース8.1の互換性 {#release-8-1-compatibility}

| バージョン      | プロトコル | UK/PK `UPDATE`イベントの分割                          | UK/ `UPDATE`イベントを分割しない                       | コメント |
| ---------- | ----- | ---------------------------------------------- | -------------------------------------------- | ---- |
| バージョン8.1.0 | 全て    | ✓                                              | ✗                                            |      |
| = v8.1.1   | 全て    | ✓ (デフォルト値: `output-raw-change-event = false` ) | ✓ （オプション： `output-raw-change-event = true` ） |      |
