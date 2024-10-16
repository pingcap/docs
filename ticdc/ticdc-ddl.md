---
title: Changefeed DDL Replication
summary: TiCDC でサポートされている DDL ステートメントといくつかの特殊なケースについて学習します。
---

# チェンジフィード DDL レプリケーション {#changefeed-ddl-replication}

このドキュメントでは、TiCDC での DDL レプリケーションのルールと特殊なケースについて説明します。

## DDL 許可リスト {#ddl-allow-list}

現在、TiCDC は許可リストを使用して、DDL ステートメントをレプリケートするかどうかを決定します。許可リスト内の DDL ステートメントのみがダウンストリームにレプリケートされます。許可リストにない DDL ステートメントはレプリケートされません。

TiCDC でサポートされている DDL ステートメントの許可リストは次のとおりです。

-   データベースを作成する
-   データベースを削除
-   テーブルを作成する
-   ドロップテーブル
-   列を追加
-   ドロップ列
-   インデックスの作成 / インデックスの追加
-   インデックスを削除
-   テーブルを切り捨てる
-   列を変更する
-   テーブル名の変更
-   列のデフォルト値を変更する
-   テーブルコメントの変更
-   インデックス名の変更
-   パーティションを追加
-   パーティションを削除する
-   パーティションを切り捨てる
-   ビューを作成
-   ドロップビュー
-   テーブル文字セットを変更する
-   データベースの文字セットを変更する
-   テーブルを回復する
-   主キーを追加する
-   主キーを削除する
-   自動 ID をリベースする
-   テーブルインデックスの可視性を変更する
-   交換パーティション
-   パーティションを再編成する
-   テーブルTTLを変更する
-   テーブルを変更してTTLを削除

## DDLレプリケーションの考慮事項 {#ddl-replication-considerations}

### <code>ADD INDEX</code>および<code>CREATE INDEX</code> DDL の非同期実行 {#asynchronous-execution-of-code-add-index-code-and-code-create-index-code-ddls}

ダウンストリームが TiDB の場合、TiCDC は`ADD INDEX`および`CREATE INDEX` DDL 操作を非同期で実行し、変更フィード レプリケーションの待機レイテンシーへの影響を最小限に抑えます。つまり、 `ADD INDEX`および`CREATE INDEX` DDL をダウンストリーム TiDB に複製して実行した後、TiCDC は DDL 実行の完了を待たずにすぐに戻ります。これにより、後続の DML 実行がブロックされることが回避されます。

ダウンストリームで`ADD INDEX`または`CREATE INDEX` DDL 操作を実行中に、TiCDC が同じテーブルの次の DDL 操作を実行すると、この DDL 操作が`queueing`状態で長時間ブロックされる可能性があります。これにより、TiCDC がこの DDL 操作を繰り返し実行することになり、再試行に時間がかかりすぎると、レプリケーション タスクが失敗する可能性があります。v7.5.4 以降では、TiCDC がダウンストリーム データベースの`SUPER`権限を持っている場合、定期的に`ADMIN SHOW DDL JOBS`実行して、非同期で実行された DDL タスクのステータスを確認します。TiCDC は、レプリケーションを続行する前に、インデックス作成が完了するまで待機します。これにより、レプリケーションのレイテンシーが長くなる可能性がありますが、レプリケーション タスクの失敗を回避できます。

> **注記：**
>
> -   特定のダウンストリーム DML の実行がレプリケーションが完了していないインデックスに依存している場合、これらの DML の実行が遅くなり、TiCDC レプリケーションのレイテンシーに影響する可能性があります。
> -   DDL をダウンストリームにレプリケートする前に、TiCDC ノードがクラッシュした場合、またはダウンストリームが他の書き込み操作を実行している場合、DDL レプリケーションが失敗する可能性は非常に低くなります。ダウンストリームをチェックして、それが発生するかどうかを確認できます。

### テーブル名の変更に関する DDL レプリケーションの考慮事項 {#ddl-replication-considerations-for-renaming-tables}

レプリケーション プロセス中に一部のコンテキストが不足しているため、TiCDC では`RENAME TABLE` DDL のレプリケーションにいくつかの制約があります。

#### DDL ステートメントで単一のテーブルの名前を変更する {#rename-a-single-table-in-a-ddl-statement}

DDL ステートメントが単一のテーブルの名前を変更する場合、TiCDC は古いテーブル名がフィルター ルールと一致する場合にのみ DDL ステートメントを複製します。次に例を示します。

changefeed の構成ファイルが次のようになっていると仮定します。

```toml
[filter]
rules = ['test.t*']
```

TiCDC はこのタイプの DDL を次のように処理します。

| DDL                                   | 複製するかどうか              | 取り扱い理由                                                                                  |
| ------------------------------------- | --------------------- | --------------------------------------------------------------------------------------- |
| `RENAME TABLE test.t1 TO test.t2`     | 複製する                  | `test.t1`フィルタルールに一致します                                                                  |
| `RENAME TABLE test.t1 TO ignore.t1`   | 複製する                  | `test.t1`フィルタルールに一致します                                                                  |
| `RENAME TABLE ignore.t1 TO ignore.t2` | 無視する                  | `ignore.t1`フィルタルールに一致しません                                                               |
| `RENAME TABLE test.n1 TO test.t1`     | エラーを報告してレプリケーションを終了する | `test.n1`フィルタルールに一致しませんが、 `test.t1`フィルタルールに一致します。この操作は不正です。この場合、エラー メッセージを参照して対処してください。 |
| `RENAME TABLE ignore.t1 TO test.t1`   | エラーを報告してレプリケーションを終了する | 上記と同じ理由です。                                                                              |

#### DDL ステートメントで複数のテーブルの名前を変更する {#rename-multiple-tables-in-a-ddl-statement}

DDL ステートメントで複数のテーブルの名前を変更する場合、TiCDC は、古いデータベース名、古いテーブル名、および新しいデータベース名がすべてフィルター ルールに一致する場合にのみ、DDL ステートメントを複製します。

また、TiCDC はテーブル名を入れ替える`RENAME TABLE` DDL をサポートしていません。以下は例です。

changefeed の構成ファイルが次のようになっていると仮定します。

```toml
[filter]
rules = ['test.t*']
```

TiCDC はこのタイプの DDL を次のように処理します。

| DDL                                                                        | 複製するかどうか | 取り扱い理由                                                                                                                  |
| -------------------------------------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------- |
| `RENAME TABLE test.t1 TO test.t2, test.t3 TO test.t4`                      | 複製する     | すべてのデータベース名とテーブル名はフィルター ルールと一致します。                                                                                      |
| `RENAME TABLE test.t1 TO test.ignore1, test.t3 TO test.ignore2`            | 複製する     | 古いデータベース名、古いテーブル名、および新しいデータベース名は、フィルター ルールと一致します。                                                                       |
| `RENAME TABLE test.t1 TO ignore.t1, test.t2 TO test.t22;`                  | エラーを報告する | 新しいデータベース名`ignore`フィルター ルールと一致しません。                                                                                     |
| `RENAME TABLE test.t1 TO test.t4, test.t3 TO test.t1, test.t4 TO test.t3;` | エラーを報告する | `RENAME TABLE` DDL は 1 つの DDL ステートメント内で`test.t1`と`test.t3`の名前を入れ替えますが、TiCDC はこれを正しく処理できません。この場合、エラー メッセージを参照して処理してください。 |

### DDL ステートメントの考慮事項 {#ddl-statement-considerations}

アップストリームでクロスデータベース DDL ステートメント ( `CREATE TABLE db1.t1 LIKE t2`など) を実行する場合は、関連するすべてのデータベース名を DDL ステートメント ( `CREATE TABLE db1.t1 LIKE db2.t2`など) で明示的に指定することをお勧めします。そうしないと、データベース名情報が不足しているため、ダウンストリームでクロスデータベース DDL ステートメントが正しく実行されない可能性があります。

### SQL モード {#sql-mode}

デフォルトでは、TiCDC は TiDB のデフォルト SQL モードを使用して DDL ステートメントを解析します。アップストリーム TiDB クラスターがデフォルト以外の SQL モードを使用している場合は、TiCDC 構成ファイルで SQL モードを指定する必要があります。そうしないと、TiCDC は DDL ステートメントを正しく解析できない可能性があります。TiDB TiDB SQLモードの詳細については、 [SQL モード](/sql-mode.md)参照してください。

たとえば、アップストリーム TiDB クラスターが`ANSI_QUOTES`モードを使用する場合、次のように changefeed 構成ファイルで SQL モードを指定する必要があります。

```toml
# In the value, "ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION" is the default SQL mode of TiDB.
# "ANSI_QUOTES" is the SQL mode added to your upstream TiDB cluster.

sql-mode = "ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION,ANSI_QUOTES"
```

SQL モードが構成されていない場合、TiCDC は一部の DDL ステートメントを正しく解析できない可能性があります。例:

```sql
CREATE TABLE "t1" ("a" int PRIMARY KEY);
```

TiDB のデフォルトの SQL モードでは、二重引用符は識別子ではなく文字列として扱われるため、TiCDC は DDL ステートメントを正しく解析できません。

したがって、レプリケーション タスクを作成するときは、アップストリーム TiDB クラスターで使用される SQL モードを構成ファイルで指定することをお勧めします。
