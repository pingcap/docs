---
title: Merge and Migrate Data from Sharded Tables in Optimistic Mode
summary: Learn how DM merges and migrates data from sharded tables in the optimistic mode.
---

# オプティミスティックモードでシャードテーブルからデータをマージおよび移行する {#merge-and-migrate-data-from-sharded-tables-in-optimistic-mode}

このドキュメントでは、オプティミスティックモードのデータ移行（DM）によって提供されるシャーディングサポート機能を紹介します。この機能を使用すると、アップストリームのMySQLまたはMariaDBインスタンスにある同じまたは異なるテーブルスキーマを持つテーブルのデータを、ダウンストリームのTiDBにある1つの同じテーブルにマージして移行できます。

> **ノート：**
>
> オプティミスティックモードとその制限について詳しく理解していない場合は、このモードを使用することはお勧めし**ません**。そうしないと、移行の中断やデータの不整合が発生する可能性があります。

## バックグラウンド {#background}

DMは、シャーディングDDLと呼ばれるシャーディングテーブルでのオンラインでのDDLステートメントの実行をサポートし、デフォルトで「ペシミスティックモード」を使用します。このモードでは、アップストリームのシャードテーブルでDDLステートメントが実行されると、他のすべてのシャードテーブルで同じDDLステートメントが実行されるまで、このテーブルのデータ移行が一時停止されます。その時までに、このDDLステートメントがダウンストリームで実行され、データ移行が再開されます。

ペシミスティックモードは、ダウンストリームに移行されたデータが常に正しいことを保証しますが、データ移行を一時停止します。これは、アップストリームでA/Bを変更するのに適していません。場合によっては、ユーザーは単一のシャードテーブルでDDLステートメントを実行するのに長い時間を費やし、検証期間の後にのみ他のシャードテーブルのスキーマを変更することがあります。ペシミスティックモードでは、これらのDDLステートメントはデータ移行をブロックし、多くのbinlogイベントを積み上げます。

したがって、「楽観的なモード」が必要です。このモードでは、シャードテーブルで実行されたDDLステートメントは、他のシャードテーブルと互換性のあるステートメントに自動的に変換され、すぐにダウンストリームに移行されます。このように、DDLステートメントはシャードテーブルによるDML移行の実行をブロックしません。

## 楽観的なモードのConfiguration / コンフィグレーション {#configuration-of-the-optimistic-mode}

オプティミスティックモードを使用するには、タスク構成ファイルの`shard-mode`項目を`optimistic`として指定します。詳細なサンプル構成ファイルについては、 [DM高度なタスクConfiguration / コンフィグレーションファイル](/dm/task-configuration-file-full.md)を参照してください。

## 制限 {#restrictions}

楽観的なモードを使用するには、いくつかのリスクが伴います。使用するときは、次のルールに従ってください。

-   DDLステートメントのバッチを実行する前後に、すべてのシャードテーブルのスキーマが互いに整合していることを確認してください。

-   A / Bテストを実行する場合は、1つのシャードテーブルで**のみ**テストを実行してください。

-   A / Bテストが終了したら、最も直接的なDDLステートメントのみを最終スキーマに移行します。テストのすべての正しいステップまたは間違ったステップを再実行しないでください。

    たとえば、シャードテーブルで`ADD COLUMN A INT; DROP COLUMN A; ADD COLUMN A FLOAT;`を実行した場合、他のシャードテーブルで`ADD COLUMN A FLOAT`を実行するだけで済みます。 3つのDDLステートメントすべてを再度実行する必要はありません。

-   DDLステートメントを実行するときは、DM移行のステータスを確認してください。エラーが報告された場合、このDDLステートメントのバッチがデータの不整合を引き起こすかどうかを判断する必要があります。

オプティミスティックモードでは、アップストリームで実行されるほとんどのDDLステートメントは、余分な労力を必要とせずに自動的にダウンストリームに移行されます。これらのDDLステートメントは「タイプ1DDL」と呼ばれます。

列名、列タイプ、または列のデフォルト値を変更するDDLステートメントは、「タイプ2DDL」と呼ばれます。アップストリームでタイプ2DDLステートメントを実行するときは、すべてのシャードテーブルで同じ順序でDDLステートメントを実行するようにしてください。

タイプ2DDLステートメントの例を次に示します。

-   列のタイプを変更します： `ALTER TABLE table_name MODIFY COLUMN column_name VARCHAR(20)` 。
-   列の名前を変更します： `ALTER TABLE table_name RENAME COLUMN column_1 TO column_2;` 。
-   デフォルト値なしで`NOT NULL`列を追加します： `ALTER TABLE table_name ADD COLUMN column_1 NOT NULL;` 。
-   インデックスの名前を変更します： `ALTER TABLE table_name RENAME INDEX index_1 TO index_2;` 。

シャードテーブルが上記のDDLステートメントを実行するときに、実行順序が異なる場合、移行は中断されます。例えば：

-   シャード1は列の名前を変更してから、列の種類を変更します。
    1.  列の名前を変更します： `ALTER TABLE table_name RENAME COLUMN column_1 TO column_2;` 。
    2.  列タイプを変更します： `ALTER TABLE table_name MODIFY COLUMN column_3 VARCHAR(20);` 。
-   シャード2は列タイプを変更してから、列の名前を変更します。
    1.  列タイプを変更します： `ALTER TABLE table_name MODIFY COLUMN column_3 VARCHAR(20)` 。
    2.  列の名前を変更します： `ALTER TABLE table_name RENAME COLUMN column_1 TO column_2;` 。

さらに、次の制限が楽観的モードと悲観的モードの両方に適用されます。

-   `DROP TABLE`または`DROP DATABASE`はサポートされていません。
-   `TRUNCATE TABLE`はサポートされていません。
-   各DDLステートメントには、1つのテーブルのみに対する操作が含まれている必要があります。
-   TiDBでサポートされていないDDLステートメントは、DMでもサポートされていません。
-   新しく追加された列のデフォルト`rand()`には、 `current_timestamp`を含めることはできませ`uuid()` 。そうしないと、アップストリームとダウンストリームの間でデータの不整合が発生する可能性があります。

## リスク {#risks}

移行タスクにオプティミスティックモードを使用すると、DDLステートメントはすぐにダウンストリームに移行されます。このモードを誤用すると、アップストリームとダウンストリームの間でデータの不整合が発生する可能性があります。

### データの不整合を引き起こす操作 {#operations-that-cause-data-inconsistency}

-   各シャーディングテーブルのスキーマは互いに互換性がありません。例えば：
    -   同じ名前の2つの列がそれぞれ2つのシャードテーブルに追加されますが、列のタイプは異なります。
    -   同じ名前の2つの列がそれぞれ2つのシャードテーブルに追加されますが、列のデフォルト値は異なります。
    -   同じ名前の2つの生成された列は、それぞれ2つのシャードテーブルに追加されますが、列は異なる式を使用して生成されます。
    -   同じ名前の2つのインデックスが2つのシャードテーブルにそれぞれ追加されますが、キーは異なります。
    -   同じ名前の他の異なるテーブルスキーマ。
-   シャーディングされたテーブルのデータを破損する可能性のあるDDLステートメントを実行してから、ロールバックを試みてください。

    たとえば、列`X`を削除してから、この列を追加し直します。

### 例 {#example}

次の3つのシャードテーブルをマージしてTiDBに移行します。

![optimistic-ddl-fail-example-1](/media/dm/optimistic-ddl-fail-example-1.png)

`tbl01`に`Age`の新しい列を追加し、列のデフォルト値を`0`に設定します。

```sql
ALTER TABLE `tbl01` ADD COLUMN `Age` INT DEFAULT 0;
```

![optimistic-ddl-fail-example-2](/media/dm/optimistic-ddl-fail-example-2.png)

`tbl00`に`Age`の新しい列を追加し、列のデフォルト値を`-1`に設定します。

```sql
ALTER TABLE `tbl00` ADD COLUMN `Age` INT DEFAULT -1;
```

![optimistic-ddl-fail-example-3](/media/dm/optimistic-ddl-fail-example-3.png)

それまでに、 `DEFAULT 0`と`DEFAULT -1`は互いに互換性がないため、 `tbl00`の`Age`列は矛盾しています。この状況では、DMはエラーを報告しますが、データの不整合を手動で修正する必要があります。

## 実装の原則 {#implementation-principle}

オプティミスティックモードでは、DM-workerがアップストリームからDDLステートメントを受信した後、更新されたテーブルスキーマをDM-masterに転送します。 DM-workerは、各シャーディングテーブルの現在のスキーマを追跡し、DM-masterは、これらのスキーマを、すべてのシャードテーブルのDMLステートメントと互換性のある複合スキーマにマージします。次に、DMマスターは対応するDDLステートメントをダウンストリームに移行します。 DMLステートメントは、ダウンストリームに直接移行されます。

![optimistic-ddl-flow](/media/dm/optimistic-ddl-flow.png)

### 例 {#examples}

アップストリームのMySQLに`tbl01` `tbl00`および`tbl02` ）があると想定します。これらのシャーディングされたテーブルをマージして、ダウンストリームTiDBの`tbl`テーブルに移行します。次の画像を参照してください。

![optimistic-ddl-example-1](/media/dm/optimistic-ddl-example-1.png)

アップストリームに`Level`列を追加します。

```sql
ALTER TABLE `tbl00` ADD COLUMN `Level` INT;
```

![optimistic-ddl-example-2](/media/dm/optimistic-ddl-example-2.png)

次に、TiDBは`tbl00` （ `Level`列あり）からDMLステートメントを受け取り、 `tbl01`および`tbl02`テーブル（ `Level`列なし）からDMLステートメントを受け取ります。

![optimistic-ddl-example-3](/media/dm/optimistic-ddl-example-3.png)

次のDMLステートメントは、変更せずにダウンストリームに移行できます。

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

この時点で、ダウンストリームにはすでに同じ`Level`列があるため、DM-masterはテーブルスキーマを比較した後に操作を実行しません。

`tbl01`に`Name`列をドロップします：

```sql
ALTER TABLE `tbl01` DROP COLUMN `Name`;
```

![optimistic-ddl-example-6](/media/dm/optimistic-ddl-example-6.png)

次に、ダウンストリームは`Name`列の`tbl00`および`tbl02`からDMLステートメントを受信するため、この列はすぐには削除されません。

同様に、すべてのDMLステートメントは引き続きダウンストリームに移行できます。

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

それまでに、すべてのシャーディングされたテーブルには`Level`列があります。

`Name`列をそれぞれ`tbl00`列と`tbl02`列にドロップします。

```sql
ALTER TABLE `tbl00` DROP COLUMN `Name`;
ALTER TABLE `tbl02` DROP COLUMN `Name`;
```

![optimistic-ddl-example-9](/media/dm/optimistic-ddl-example-9.png)

それまでに、 `Name`列はすべてのシャーディングされたテーブルから削除され、ダウンストリームで安全に削除できます。

```sql
ALTER TABLE `tbl` DROP COLUMN `Name`;
```

![optimistic-ddl-example-10](/media/dm/optimistic-ddl-example-10.png)
