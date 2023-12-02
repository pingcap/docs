---
title: Changefeed DDL Replication
summary: Learn about the DDL statements supported by TiCDC and some special cases.
---

# チェンジフィード DDL レプリケーション {#changefeed-ddl-replication}

このドキュメントでは、TiCDC での DDL レプリケーションのルールと特殊なケースについて説明します。

## DDL許可リスト {#ddl-allow-list}

現在、TiCDC は許可リストを使用して、DDL ステートメントを複製するかどうかを決定します。許可リスト内の DDL ステートメントのみがダウンストリームにレプリケートされます。許可リストにない DDL ステートメントはレプリケートされません。

TiCDC でサポートされる DDL ステートメントの許可リストは次のとおりです。

-   データベースを作成する
-   データベースを削除する
-   テーブルを作成する
-   ドロップテーブル
-   列を追加
-   ドロップカラム
-   インデックスの作成 / インデックスの追加
-   インデックスを削除
-   テーブルを切り捨てる
-   列を変更する
-   テーブルの名前を変更する
-   列のデフォルト値を変更する
-   テーブルのコメントを変更する
-   インデックスの名前を変更する
-   パーティションを追加する
-   パーティションを削除する
-   パーティションを切り詰める
-   ビューの作成
-   ドロップビュー
-   テーブルの文字セットを変更する
-   データベースの文字セットを変更する
-   テーブルをリカバリする
-   主キーを追加する
-   主キーを削除する
-   自動 ID をリベースする
-   テーブルインデックスの可視性を変更する
-   パーティションを交換する
-   パーティションを再編成する
-   テーブルttlを変更する
-   テーブルを変更して TTL を削除

## DDL レプリケーションに関する考慮事項 {#ddl-replication-considerations}

### <code>ADD INDEX</code>および<code>CREATE INDEX</code> DDL の非同期実行 {#asynchronous-execution-of-code-add-index-code-and-code-create-index-code-ddls}

ダウンストリームが TiDB の場合、TiCDC は`ADD INDEX`および`CREATE INDEX` DDL 操作を非同期に実行して、チェンジフィード レプリケーションのレイテンシーへの影響を最小限に抑えます。これは、実行のために`ADD INDEX`および`CREATE INDEX` DDL をダウンストリーム TiDB に複製した後、TiCDC は DDL 実行の完了を待たずにすぐに戻ることを意味します。これにより、後続の DML 実行のブロックが回避されます。

> **注記：**
>
> -   特定のダウンストリーム DML の実行が、レプリケーションが完了していないインデックスに依存している場合、これらの DML の実行が遅くなる可能性があり、その結果 TiCDC レプリケーションのレイテンシーに影響を与える可能性があります。
> -   DDL をダウンストリームにレプリケートする前に、TiCDC ノードがクラッシュした場合、またはダウンストリームが他の書き込み操作を実行している場合、DDL レプリケーションが失敗する可能性は非常に低くなります。ダウンストリームをチェックして、それが発生するかどうかを確認できます。

### テーブルの名前変更に関する DDL レプリケーションの考慮事項 {#ddl-replication-considerations-for-renaming-tables}

レプリケーション プロセス中に一部のコンテキストが欠如しているため、TiCDC には`RENAME TABLE` DDL のレプリケーションにいくつかの制約があります。

#### DDL ステートメント内の単一テーブルの名前を変更する {#rename-a-single-table-in-a-ddl-statement}

DDL ステートメントが単一テーブルの名前を変更する場合、TiCDC は、古いテーブル名がフィルター ルールに一致する場合にのみ DDL ステートメントを複製します。以下は一例です。

変更フィードの構成ファイルが次のとおりであると仮定します。

```toml
[filter]
rules = ['test.t*']
```

TiCDC は、このタイプの DDL を次のように処理します。

| DDL                                   | 複製するかどうか               | 取り扱い理由                                                                                       |
| ------------------------------------- | ---------------------- | -------------------------------------------------------------------------------------------- |
| `RENAME TABLE test.t1 TO test.t2`     | 複製する                   | `test.t1`フィルタルールに一致します                                                                       |
| `RENAME TABLE test.t1 TO ignore.t1`   | 複製する                   | `test.t1`フィルタルールに一致します                                                                       |
| `RENAME TABLE ignore.t1 TO ignore.t2` | 無視する                   | `ignore.t1`はフィルタルールに一致しません                                                                   |
| `RENAME TABLE test.n1 TO test.t1`     | エラーを報告してレプリケーションを終了します | `test.n1`はフィルター ルールに一致しませんが、 `test.t1`フィルター ルールに一致します。この操作は違法です。この場合は、エラーメッセージを参照して対処してください。 |
| `RENAME TABLE ignore.t1 TO test.t1`   | エラーを報告してレプリケーションを終了します | 上記と同じ理由です。                                                                                   |

#### DDL ステートメント内の複数のテーブルの名前を変更する {#rename-multiple-tables-in-a-ddl-statement}

DDL ステートメントで複数のテーブルの名前を変更する場合、TiCDC は、古いデータベース名、古いテーブル名、および新しいデータベース名のすべてがフィルター ルールに一致する場合にのみ DDL ステートメントを複製します。

さらに、TiCDC はテーブル名を交換する`RENAME TABLE` DDL をサポートしていません。以下は一例です。

変更フィードの構成ファイルが次のとおりであると仮定します。

```toml
[filter]
rules = ['test.t*']
```

TiCDC は、このタイプの DDL を次のように処理します。

| DDL                                                                        | 複製するかどうか | 取り扱い理由                                                                                                                 |
| -------------------------------------------------------------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------- |
| `RENAME TABLE test.t1 TO test.t2, test.t3 TO test.t4`                      | 複製する     | すべてのデータベース名とテーブル名がフィルター ルールに一致します。                                                                                     |
| `RENAME TABLE test.t1 TO test.ignore1, test.t3 TO test.ignore2`            | 複製する     | 古いデータベース名、古いテーブル名、および新しいデータベース名がフィルター ルールに一致します。                                                                       |
| `RENAME TABLE test.t1 TO ignore.t1, test.t2 TO test.t22;`                  | エラーを報告する | 新しいデータベース名`ignore`はフィルター ルールに一致しません。                                                                                   |
| `RENAME TABLE test.t1 TO test.t4, test.t3 TO test.t1, test.t4 TO test.t3;` | エラーを報告する | `RENAME TABLE` DDL は 1 つの DDL ステートメント内で`test.t1`と`test.t3`の名前を交換しますが、TiCDC はこれを正しく処理できません。この場合は、エラーメッセージを参照して対処してください。 |

### SQLモード {#sql-mode}

デフォルトでは、TiCDC は TiDB のデフォルト SQL モードを使用して DDL ステートメントを解析します。アップストリーム TiDB クラスターがデフォルト以外の SQL モードを使用する場合は、TiCDC 構成ファイルで SQL モードを指定する必要があります。そうしないと、TiCDC が DDL ステートメントを正しく解析できない可能性があります。 TiDB SQLモードの詳細については、 [SQLモード](/sql-mode.md)を参照してください。

たとえば、アップストリーム TiDB クラスターが`ANSI_QUOTES`モードを使用する場合、changefeed 構成ファイルで次のように SQL モードを指定する必要があります。

```toml
# In the value, "ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION" is the default SQL mode of TiDB.
# "ANSI_QUOTES" is the SQL mode added to your upstream TiDB cluster.

sql-mode = "ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION,ANSI_QUOTES"
```

SQL モードが構成されていない場合、TiCDC は一部の DDL ステートメントを正しく解析できない可能性があります。例えば：

```sql
CREATE TABLE "t1" ("a" int PRIMARY KEY);
```

TiDB のデフォルト SQL モードでは、二重引用符が識別子ではなく文字列として扱われるため、TiCDC は DDL ステートメントを正しく解析できません。

したがって、レプリケーション タスクを作成するときは、構成ファイルで上流の TiDB クラスターによって使用される SQL モードを指定することをお勧めします。
