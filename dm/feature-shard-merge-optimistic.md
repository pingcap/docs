---
title: Merge and Migrate Data from Sharded Tables in Optimistic Mode
summary: Learn how DM merges and migrates data from sharded tables in the optimistic mode.
---

# オプティミスティックモードでのシャードテーブルからのデータのマージと移行 {#merge-and-migrate-data-from-sharded-tables-in-optimistic-mode}

このドキュメントでは、楽観的モードのデータ移行 (DM) によって提供されるシャーディング サポート機能を紹介します。この機能を使用すると、アップストリームの MySQL または MariaDB インスタンスにある同じまたは異なるテーブル スキーマを持つテーブルのデータを、ダウンストリーム TiDB の 1 つの同じテーブルにマージおよび移行できます。

> **注記：**
>
> 楽観的モードとその制限事項を深く理解していない場合は、このモードの使用は**お勧めできません**。そうしないと、移行が中断されたり、データの不整合が発生したりする可能性があります。

## 背景 {#background}

DM は、シャーディング DDL と呼ばれるオンラインのシャード テーブルに対する DDL ステートメントの実行をサポートしており、デフォルトで「悲観的モード」を使用します。このモードでは、DDL ステートメントが上流のシャード テーブルで実行されると、同じ DDL ステートメントが他のすべてのシャード テーブルで実行されるまで、このテーブルのデータ移行は一時停止されます。それまでにこの DDL ステートメントがダウンストリームで実行され、データ移行が再開されます。

悲観的モードでは、ダウンストリームに移行されるデータが常に正しいことが保証されますが、データの移行が一時停止されるため、アップストリームで A/B 変更を行うには悪影響を及ぼします。場合によっては、ユーザーが単一のシャード テーブルで DDL ステートメントの実行に長時間を費やし、検証期間が経過した後にのみ他のシャード テーブルのスキーマを変更することがあります。悲観的モードでは、これらの DDL ステートメントによってデータ移行がブロックされ、多くのbinlogイベントが蓄積されます。

したがって、「楽観的モード」が必要です。このモードでは、シャード テーブルで実行される DDL ステートメントは、他のシャード テーブルと互換性のあるステートメントに自動的に変換され、すぐにダウンストリームに移行されます。このように、DDL ステートメントは、シャード テーブルによる DML 移行の実行をブロックしません。

## 楽観的モードのコンフィグレーション {#configuration-of-the-optimistic-mode}

楽観的モードを使用するには、タスク構成ファイルの`shard-mode`項目を`optimistic`として指定します。 `strict-optimistic-shard-mode`設定を有効にすることで、楽観的モードの動作を制限できます。詳細なサンプル構成ファイルについては、 [DM 拡張タスクコンフィグレーションファイル](/dm/task-configuration-file-full.md)を参照してください。

## 制限 {#restrictions}

楽観的モードを使用するには、ある程度のリスクが伴います。使用するときは次の規則に従ってください。

-   DDL ステートメントのバッチを実行する前後で、すべてのシャード テーブルのスキーマが相互に一貫していることを確認してください。

-   A/B テストを実行する場合は、1 つのシャード テーブルに対して**のみ**テストを実行してください。

-   A/B テストが終了したら、最も直接的な DDL ステートメントのみを最終スキーマに移行します。テストの正しいステップや間違ったステップをすべて再実行しないでください。

    たとえば、シャードテーブルで`ADD COLUMN A INT; DROP COLUMN A; ADD COLUMN A FLOAT;`を実行した場合、他のシャードテーブルでは`ADD COLUMN A FLOAT`を実行するだけで済みます。 3 つの DDL ステートメントをすべて再度実行する必要はありません。

-   DDL ステートメントを実行するときに、DM 移行のステータスを観察します。エラーが報告された場合は、この DDL ステートメントのバッチがデータの不整合を引き起こすかどうかを判断する必要があります。

楽観的モードでは、アップストリームで実行された DDL ステートメントのほとんどが、追加の労力を必要とせずに自動的にダウンストリームに移行されます。これらの DDL ステートメントは「タイプ 1 DDL」と呼ばれます。

列名、列の型、または列のデフォルト値を変更する DDL ステートメントは、「タイプ 2 DDL」と呼ばれます。アップストリームでタイプ 2 DDL ステートメントを実行する場合は、すべてのシャード テーブルで DDL ステートメントを同じ順序で実行するようにしてください。

タイプ 2 DDL ステートメントの例をいくつか次に示します。

-   列のタイプを変更します。 `ALTER TABLE table_name MODIFY COLUMN column_name VARCHAR(20)` 。
-   列の名前を変更します: `ALTER TABLE table_name RENAME COLUMN column_1 TO column_2;` 。
-   デフォルト値なしで`NOT NULL`列を追加します: `ALTER TABLE table_name ADD COLUMN column_1 NOT NULL;` 。
-   インデックスの名前を変更します: `ALTER TABLE table_name RENAME INDEX index_1 TO index_2;` 。

シャードテーブルが上記の DDL ステートメントを実行するときに、 `strict-optimistic-shard-mode: true`が設定されている場合、タスクは直接中断され、エラーが報告されます。 `strict-optimistic-shard-mode: false`が設定されているか指定されていない場合、シャード テーブル内の DDL ステートメントの実行順序が異なるため、移行が中断されます。例えば：

-   シャード 1 は列の名前を変更し、列のタイプを変更します。
    1.  列の名前を変更します: `ALTER TABLE table_name RENAME COLUMN column_1 TO column_2;` 。
    2.  列のタイプを変更します: `ALTER TABLE table_name MODIFY COLUMN column_3 VARCHAR(20);` 。
-   シャード 2 は列のタイプを変更し、列の名前を変更します。
    1.  列の型を変更します: `ALTER TABLE table_name MODIFY COLUMN column_3 VARCHAR(20)` 。
    2.  列の名前を変更します: `ALTER TABLE table_name RENAME COLUMN column_1 TO column_2;` 。

さらに、次の制限が楽観的モードと悲観的モードの両方に適用されます。

-   `DROP TABLE`または`DROP DATABASE`はサポートされていません。
-   `TRUNCATE TABLE`はサポートされていません。
-   各 DDL ステートメントには、1 つのテーブルのみに対する操作が含まれる必要があります。
-   TiDB でサポートされていない DDL ステートメントは、DM でもサポートされません。
-   新しく追加された列のデフォルト値には`current_timestamp` 、 `rand()` 、 `uuid()`を含めることはできません。そうしないと、上流と下流の間でデータの不整合が発生する可能性があります。

## リスク {#risks}

移行タスクに楽観的モードを使用すると、DDL ステートメントはすぐにダウンストリームに移行されます。このモードを誤って使用すると、上流と下流の間でデータの不整合が発生する可能性があります。

### データの不整合を引き起こす操作 {#operations-that-cause-data-inconsistency}

-   各シャードテーブルのスキーマは相互に互換性がありません。例えば：
    -   同じ名前の 2 つの列が 2 つのシャード テーブルにそれぞれ追加されますが、列のタイプは異なります。
    -   同じ名前の 2 つの列が 2 つのシャードテーブルにそれぞれ追加されますが、それらの列のデフォルト値は異なります。
    -   生成された同じ名前の 2 つの列がそれぞれ 2 つのシャード テーブルに追加されますが、これらの列は異なる式を使用して生成されます。
    -   同じ名前の 2 つのインデックスが 2 つのシャード テーブルにそれぞれ追加されますが、キーは異なります。
    -   同じ名前を持つ他の異なるテーブル スキーマ。
-   シャードテーブル内のデータを破損する可能性がある DDL ステートメントを実行してから、ロールバックを試行します。

    たとえば、列`X`を削除し、この列を追加し直します。

### 例 {#example}

次の 3 つのシャード テーブルを結合して TiDB に移行します。

![optimistic-ddl-fail-example-1](/media/dm/optimistic-ddl-fail-example-1.png)

新しい列`Age` in `tbl01`を追加し、列のデフォルト値を`0`に設定します。

```sql
ALTER TABLE `tbl01` ADD COLUMN `Age` INT DEFAULT 0;
```

![optimistic-ddl-fail-example-2](/media/dm/optimistic-ddl-fail-example-2.png)

新しい列`Age` in `tbl00`を追加し、列のデフォルト値を`-1`に設定します。

```sql
ALTER TABLE `tbl00` ADD COLUMN `Age` INT DEFAULT -1;
```

![optimistic-ddl-fail-example-3](/media/dm/optimistic-ddl-fail-example-3.png)

その時点では、 `DEFAULT 0`と`DEFAULT -1`は互いに互換性がないため、 `tbl00`の`Age`列は矛盾しています。この状況では、DM はエラーを報告しますが、データの不整合を手動で修正する必要があります。

## 実施原則 {#implementation-principle}

楽観的モードでは、DM ワーカーは上流から DDL ステートメントを受信した後、更新されたテーブル スキーマを DM マスターに転送します。 DM ワーカーは各シャード テーブルの現在のスキーマを追跡し、DM マスターはこれらのスキーマを、すべてのシャード テーブルの DML ステートメントと互換性のある複合スキーマにマージします。次に、DM マスターは、対応する DDL ステートメントをダウンストリームに移行します。 DML ステートメントはダウンストリームに直接移行されます。

![optimistic-ddl-flow](/media/dm/optimistic-ddl-flow.png)

### 例 {#examples}

アップストリーム MySQL に 3 つのシャード テーブル ( `tbl00` 、 `tbl01` 、および`tbl02` ) があると仮定します。これらのシャードテーブルをダウンストリーム TiDB の`tbl`テーブルにマージして移行します。次の画像を参照してください。

![optimistic-ddl-example-1](/media/dm/optimistic-ddl-example-1.png)

上流に`Level`列を追加します。

```sql
ALTER TABLE `tbl00` ADD COLUMN `Level` INT;
```

![optimistic-ddl-example-2](/media/dm/optimistic-ddl-example-2.png)

次に、TiDB は`tbl00` (列`Level`を含む) からの DML ステートメントと、テーブル`tbl01`と`tbl02` (列`Level`を除く) からの DML ステートメントを受け取ります。

![optimistic-ddl-example-3](/media/dm/optimistic-ddl-example-3.png)

次の DML ステートメントは、変更せずにダウンストリームに移行できます。

```sql
UPDATE `tbl00` SET `Level` = 9 WHERE `ID` = 1;
INSERT INTO `tbl02` (`ID`, `Name`) VALUES (27, 'Tony');
```

![optimistic-ddl-example-4](/media/dm/optimistic-ddl-example-4.png)

また、 `tbl01`に`Level`列を追加します。

```sql
ALTER TABLE `tbl01` ADD COLUMN `Level` INT;
```

![optimistic-ddl-example-5](/media/dm/optimistic-ddl-example-5.png)

この時点では、下流にはすでに同じ`Level`列が存在するため、DM-master はテーブル スキーマの比較後に何も操作を行いません。

`Name`列を`tbl01`にドロップします。

```sql
ALTER TABLE `tbl01` DROP COLUMN `Name`;
```

![optimistic-ddl-example-6](/media/dm/optimistic-ddl-example-6.png)

その後、ダウンストリームは`Name`列を持つ`tbl00`と`tbl02`からの DML ステートメントを受信するため、この列はすぐには削除されません。

同様に、すべての DML ステートメントを引き続きダウンストリームに移行できます。

```sql
INSERT INTO `tbl01` (`ID`, `Level`) VALUES (15, 7);
UPDATE `tbl00` SET `Level` = 5 WHERE `ID` = 5;
```

![optimistic-ddl-example-7](/media/dm/optimistic-ddl-example-7.png)

`tbl02`に`Level`列を追加します。

```sql
ALTER TABLE `tbl02` ADD COLUMN `Level` INT;
```

![optimistic-ddl-example-8](/media/dm/optimistic-ddl-example-8.png)

それまでに、すべてのシャードテーブルには`Level`列が含まれます。

`Name`列をそれぞれ`tbl00`と`tbl02`にドロップします。

```sql
ALTER TABLE `tbl00` DROP COLUMN `Name`;
ALTER TABLE `tbl02` DROP COLUMN `Name`;
```

![optimistic-ddl-example-9](/media/dm/optimistic-ddl-example-9.png)

それまでに、 `Name`列はすべてのシャード テーブルから削除され、ダウンストリームで安全に削除できるようになります。

```sql
ALTER TABLE `tbl` DROP COLUMN `Name`;
```

![optimistic-ddl-example-10](/media/dm/optimistic-ddl-example-10.png)
