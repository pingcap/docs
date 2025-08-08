---
title: Merge and Migrate Data from Sharded Tables in Optimistic Mode
summary: DM が楽観的モードでシャード テーブルからデータをマージおよび移行する方法を学習します。
---

# オプティミスティックモードでシャードテーブルからデータをマージおよび移行する {#merge-and-migrate-data-from-sharded-tables-in-optimistic-mode}

このドキュメントでは、データ移行（DM）の楽観的モードにおけるシャーディングサポート機能について説明します。この機能を使用すると、上流のMySQLまたはMariaDBインスタンスにある、同一または異なるテーブルスキーマを持つテーブルのデータを、下流のTiDBにある同じテーブルにマージして移行できます。

> **注記：**
>
> 楽観的モードとその制限事項を十分に理解していない場合は、このモードの使用は推奨さ**れません**。そうでない場合、移行が中断されたり、データの不整合が発生する可能性があります。

## 背景 {#background}

DMは、シャーディングDDLと呼ばれるシャーディングテーブルへのDDL文のオンライン実行をサポートしており、デフォルトで「悲観的モード」を使用します。このモードでは、上流のシャーディングテーブルでDDL文が実行されると、そのテーブルのデータ移行は、他のすべてのシャーディングテーブルで同じDDL文が実行されるまで一時停止されます。その後、下流のシャーディングテーブルで同じDDL文が実行され、データ移行が再開されます。

悲観的モードでは、下流に移行されるデータが常に正しいことが保証されますが、データ移行が一時停止されるため、上流でのA/B変更には適していません。場合によっては、ユーザーは単一のシャードテーブルでDDL文の実行に長い時間を費やし、検証期間が経過した後に他のシャードテーブルのスキーマを変更することがあります。悲観的モードでは、これらのDDL文がデータ移行をブロックし、多くのbinlogイベントが蓄積される原因となります。

そのため、「楽観的モード」が必要になります。このモードでは、シャードテーブルに対して実行されたDDL文は、他のシャードテーブルと互換性のある文に自動的に変換され、すぐに下流に移行されます。これにより、DDL文がシャードテーブルによるDML移行の実行をブロックすることはありません。

## 楽観的モードのコンフィグレーション {#configuration-of-the-optimistic-mode}

楽観的モードを使用するには、タスク設定ファイルの`shard-mode`項目を`optimistic`に指定します。5 `strict-optimistic-shard-mode`の設定を有効にすると、楽観的モードの動作を制限できます。詳細なサンプル設定ファイルについては、 [DM 高度なタスクコンフィグレーションファイル](/dm/task-configuration-file-full.md)参照してください。

## 制限 {#restrictions}

楽観的モードの使用には多少のリスクが伴います。使用する際は、以下のルールに従ってください。

-   DDL ステートメントのバッチを実行する前と実行後に、各シャード テーブルのスキーマが相互に一貫していることを確認します。

-   A/B テストを実行する場合は、1 つのシャード テーブルで**のみ**テストを実行します。

-   A/Bテストが完了したら、最も直接的なDDL文のみを最終スキーマに移行します。テストのすべてのステップを、正解か不正解かを問わず再実行しないでください。

    たとえば、あるシャードテーブルで`ADD COLUMN A INT; DROP COLUMN A; ADD COLUMN A FLOAT;` DDL文を実行した場合、他のシャードテーブルでは`ADD COLUMN A FLOAT` DDL文を実行するだけで済みます。3つのDDL文すべてを再度実行する必要はありません。

-   DDL文を実行する際は、DM移行のステータスを確認してください。エラーが報告された場合は、この一連のDDL文がデータの不整合を引き起こすかどうかを判断する必要があります。

楽観的モードでは、上流で実行されたDDL文の大部分が、追加の作業なしに自動的に下流に移行されます。これらのDDL文は「タイプ1 DDL」と呼ばれます。

列名、列の型、または列のデフォルト値を変更するDDL文は「Type 2 DDL」と呼ばれます。アップストリームでType 2 DDL文を実行する場合は、すべてのシャードテーブルで同じ順序でDDL文を実行するようにしてください。

タイプ 2 DDL ステートメントの例を次に示します。

-   列のタイプを変更します: `ALTER TABLE table_name MODIFY COLUMN column_name VARCHAR(20)` .
-   列の名前を変更します: `ALTER TABLE table_name RENAME COLUMN column_1 TO column_2;` .
-   デフォルト値のない`NOT NULL`列を追加します: `ALTER TABLE table_name ADD COLUMN column_1 NOT NULL;` 。
-   インデックスの名前を変更します: `ALTER TABLE table_name RENAME INDEX index_1 TO index_2;` 。

シャードテーブルが上記のDDL文を実行する際、 `strict-optimistic-shard-mode: true`設定されている場合はタスクが直接中断され、エラーが報告されます。3 `strict-optimistic-shard-mode: false`設定されている場合、または指定されていない場合は、シャードテーブル内のDDL文の実行順序が異なるため、移行が中断されます。例：

-   シャード 1 は列の名前を変更し、列の種類を変更します。
    1.  列の名前を変更します: `ALTER TABLE table_name RENAME COLUMN column_1 TO column_2;` .
    2.  列のタイプを変更します: `ALTER TABLE table_name MODIFY COLUMN column_3 VARCHAR(20);` 。
-   シャード 2 は列の種類を変更し、列の名前を変更します。
    1.  列の種類を変更します: `ALTER TABLE table_name MODIFY COLUMN column_3 VARCHAR(20)` 。
    2.  列の名前を変更します: `ALTER TABLE table_name RENAME COLUMN column_1 TO column_2;` .

さらに、楽観的モードと悲観的モードの両方に次の制限が適用されます。

-   `DROP TABLE`または`DROP DATABASE`サポートされていません。
-   `TRUNCATE TABLE`はサポートされていません。
-   各 DDL ステートメントには、1 つのテーブルに対する操作のみを含める必要があります。
-   TiDB でサポートされていない DDL ステートメントは、DM でもサポートされません。
-   新しく追加された列のデフォルト値には、 `current_timestamp` 、 `rand()` 、 `uuid()`を含めることはできません。そうしないと、上流と下流の間でデータの不整合が発生する可能性があります。

## リスク {#risks}

移行タスクに楽観的モードを使用すると、DDL文は直ちに下流に移行されます。このモードを誤って使用すると、上流と下流の間でデータの不整合が発生する可能性があります。

### データの不整合を引き起こす操作 {#operations-that-cause-data-inconsistency}

-   各シャードテーブルのスキーマは互いに互換性がありません。例:
    -   同じ名前の 2 つの列が 2 つのシャード テーブルにそれぞれ追加されていますが、列のタイプは異なります。
    -   同じ名前の 2 つの列が 2 つのシャード テーブルにそれぞれ追加されていますが、列のデフォルト値は異なります。
    -   同じ名前の 2 つの生成された列がそれぞれ 2 つのシャード テーブルに追加されますが、列は異なる式を使用して生成されます。
    -   同じ名前の 2 つのインデックスが 2 つのシャード テーブルにそれぞれ追加されていますが、キーは異なります。
    -   同じ名前を持つ他の異なるテーブル スキーマ。
-   シャード テーブル内のデータを破損する可能性のある DDL ステートメントを実行し、ロールバックを試みます。

    たとえば、列`X`を削除し、この列を再度追加します。

### 例 {#example}

次の 3 つのシャード テーブルをマージして TiDB に移行します。

![optimistic-ddl-fail-example-1](/media/dm/optimistic-ddl-fail-example-1.png)

`tbl01`に新しい列`Age`を追加し、列のデフォルト値を`0`に設定します。

```sql
ALTER TABLE `tbl01` ADD COLUMN `Age` INT DEFAULT 0;
```

![optimistic-ddl-fail-example-2](/media/dm/optimistic-ddl-fail-example-2.png)

`tbl00`に新しい列`Age`を追加し、列のデフォルト値を`-1`に設定します。

```sql
ALTER TABLE `tbl00` ADD COLUMN `Age` INT DEFAULT -1;
```

![optimistic-ddl-fail-example-3](/media/dm/optimistic-ddl-fail-example-3.png)

この時点で、 `DEFAULT 0`と`DEFAULT -1`互いに互換性がないため、 `tbl00`の`Age`列目は不整合になります。このような状況では、DMはエラーを報告しますが、データの不整合を手動で修正する必要があります。

## 実施原則 {#implementation-principle}

楽観的モードでは、DMワーカーは上流からDDL文を受信すると、更新されたテーブルスキーマをDMマスターに転送します。DMワーカーは各シャードテーブルの現在のスキーマを追跡し、DMマスターはこれらのスキーマを、各シャードテーブルのDML文と互換性のある複合スキーマにマージします。その後、DMマスターは対応するDDL文を下流に移行します。DML文は下流に直接移行されます。

![optimistic-ddl-flow](/media/dm/optimistic-ddl-flow.png)

### 例 {#examples}

アップストリームMySQLに3つ`tbl02`シャードテーブル（ `tbl00` ）があると仮定します。これらのシャードテーブル`tbl01`ダウンストリームTiDBの`tbl`テーブルにマージして移行します。次の図をご覧ください。

![optimistic-ddl-example-1](/media/dm/optimistic-ddl-example-1.png)

アップストリームに`Level`列を追加します。

```sql
ALTER TABLE `tbl00` ADD COLUMN `Level` INT;
```

![optimistic-ddl-example-2](/media/dm/optimistic-ddl-example-2.png)

次に、TiDB は`tbl00` (列`Level`を含む) からの DML ステートメントと、 `tbl01`および`tbl02`テーブル (列`Level`を含まない) からの DML ステートメントを受け取ります。

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

この時点で、ダウンストリームにはすでに同じ`Level`列があるため、DM マスターはテーブル スキーマを比較した後、何も操作を実行しません。

`tbl01`に`Name`列をドロップします。

```sql
ALTER TABLE `tbl01` DROP COLUMN `Name`;
```

![optimistic-ddl-example-6](/media/dm/optimistic-ddl-example-6.png)

その後、ダウンストリームは`Name`列を含む`tbl00`と`tbl02`からの DML ステートメントを受信するため、この列はすぐには削除されません。

同様に、すべての DML ステートメントをダウンストリームに移行することもできます。

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

その時までに、すべてのシャードテーブルに`Level`列が存在します。

それぞれ`tbl00`と`tbl02`の`Name`列目を削除します。

```sql
ALTER TABLE `tbl00` DROP COLUMN `Name`;
ALTER TABLE `tbl02` DROP COLUMN `Name`;
```

![optimistic-ddl-example-9](/media/dm/optimistic-ddl-example-9.png)

その時までに、 `Name`列はすべてのシャード テーブルから削除され、ダウンストリームで安全に削除できるようになります。

```sql
ALTER TABLE `tbl` DROP COLUMN `Name`;
```

![optimistic-ddl-example-10](/media/dm/optimistic-ddl-example-10.png)
