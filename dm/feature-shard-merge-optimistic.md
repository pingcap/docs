---
title: Merge and Migrate Data from Sharded Tables in Optimistic Mode
summary: DM が楽観的モードでシャード テーブルからデータをマージおよび移行する方法について説明します。
---

# オプティミスティック モードでシャード テーブルからデータをマージおよび移行する {#merge-and-migrate-data-from-sharded-tables-in-optimistic-mode}

このドキュメントでは、楽観的モードのデータ移行 (DM) によって提供されるシャーディング サポート機能を紹介します。この機能を使用すると、アップストリームの MySQL または MariaDB インスタンス内の同じまたは異なるテーブル スキーマを持つテーブルのデータを、ダウンストリームの TiDB 内の 1 つの同じテーブルにマージして移行できます。

> **注記：**
>
> 楽観的モードとその制限事項を詳しく理解していない場合は、このモードの使用はお勧めし**ません**。そうしないと、移行が中断したり、データの不整合が発生する可能性があります。

## 背景 {#background}

DM は、シャーディング DDL と呼ばれるシャーディング テーブルでの DDL ステートメントのオンライン実行をサポートし、デフォルトで「悲観的モード」を使用します。このモードでは、上流のシャーディング テーブルで DDL ステートメントが実行されると、他のすべてのシャーディング テーブルで同じ DDL ステートメントが実行されるまで、このテーブルのデータ移行は一時停止されます。その時点でのみ、この DDL ステートメントが下流で実行され、データ移行が再開されます。

悲観的モードでは、ダウンストリームに移行されたデータが常に正しいことが保証されますが、データ移行が一時停止されるため、アップストリームで A/B 変更を行うのに適していません。場合によっては、ユーザーは単一のシャード テーブルで DDL ステートメントを実行するのに長い時間を費やし、検証期間が経過した後にのみ他のシャード テーブルのスキーマを変更することがあります。悲観的モードでは、これらの DDL ステートメントによってデータ移行がブロックされ、多くのbinlogイベントが蓄積されます。

したがって、「楽観的モード」が必要です。このモードでは、シャード テーブルで実行された DDL ステートメントは、他のシャード テーブルと互換性のあるステートメントに自動的に変換され、すぐにダウンストリームに移行されます。このように、DDL ステートメントは、シャード テーブルによる DML 移行の実行をブロックしません。

## 楽観的モードのコンフィグレーション {#configuration-of-the-optimistic-mode}

楽観的モードを使用するには、タスク設定ファイルの`shard-mode`項目を`optimistic`に指定します。 `strict-optimistic-shard-mode`設定を有効にすることで、楽観的モードの動作を制限できます。詳細なサンプル設定ファイルについては、 [DM 高度なタスクコンフィグレーションファイル](/dm/task-configuration-file-full.md)を参照してください。

## 制限 {#restrictions}

楽観的モードを使用するには、ある程度のリスクが伴います。使用時には、次のルールに従ってください。

-   DDL ステートメントのバッチを実行する前と実行後に、各シャード テーブルのスキーマが相互に一貫していることを確認します。

-   A/B テストを実行する場合は、1 つのシャード テーブルで**のみ**テストを実行します。

-   A/B テストが終了したら、最も直接的な DDL ステートメントのみを最終スキーマに移行します。テストのすべての正しいステップまたは間違ったステップを再実行しないでください。

    たとえば、シャード テーブルで`ADD COLUMN A INT; DROP COLUMN A; ADD COLUMN A FLOAT;`実行した場合、他のシャード テーブルでは`ADD COLUMN A FLOAT`実行するだけで済みます。3 つの DDL ステートメントすべてを再度実行する必要はありません。

-   DDL ステートメントを実行するときに、DM 移行のステータスを確認します。エラーが報告された場合は、この一連の DDL ステートメントによってデータの不整合が発生するかどうかを判断する必要があります。

楽観的モードでは、アップストリームで実行された DDL ステートメントのほとんどが、追加の作業を必要とせずにダウンストリームに自動的に移行されます。これらの DDL ステートメントは、「タイプ 1 DDL」と呼ばれます。

列名、列タイプ、または列のデフォルト値を変更する DDL ステートメントは、「タイプ 2 DDL」と呼ばれます。アップストリームでタイプ 2 DDL ステートメントを実行する場合は、すべてのシャード テーブルで DDL ステートメントを同じ順序で実行するようにしてください。

タイプ 2 DDL ステートメントの例をいくつか示します。

-   列のタイプを変更します: `ALTER TABLE table_name MODIFY COLUMN column_name VARCHAR(20)` 。
-   列の名前を変更します: `ALTER TABLE table_name RENAME COLUMN column_1 TO column_2;` .
-   デフォルト値のない`NOT NULL`列を追加します: `ALTER TABLE table_name ADD COLUMN column_1 NOT NULL;` 。
-   インデックスの名前を変更します: `ALTER TABLE table_name RENAME INDEX index_1 TO index_2;` 。

シャード テーブルが上記の DDL ステートメントを実行する場合、 `strict-optimistic-shard-mode: true`設定されている場合はタスクが直接中断され、エラーが報告されます。3 `strict-optimistic-shard-mode: false`設定されているか指定されていない場合は、シャード テーブル内の DDL ステートメントの実行順序が異なるため、移行が中断されます。例:

-   シャード 1 は列の名前を変更し、列の種類を変更します。
    1.  列の名前を変更します: `ALTER TABLE table_name RENAME COLUMN column_1 TO column_2;` .
    2.  列のタイプを変更します: `ALTER TABLE table_name MODIFY COLUMN column_3 VARCHAR(20);` 。
-   シャード 2 は列の種類を変更し、列の名前を変更します。
    1.  列の種類を変更します: `ALTER TABLE table_name MODIFY COLUMN column_3 VARCHAR(20)` 。
    2.  列の名前を変更します: `ALTER TABLE table_name RENAME COLUMN column_1 TO column_2;` .

さらに、楽観的モードと悲観的モードの両方に次の制限が適用されます。

-   `DROP TABLE`または`DROP DATABASE`サポートされていません。
-   `TRUNCATE TABLE`はサポートされていません。
-   各 DDL ステートメントには、1 つのテーブルに対する操作のみが含まれる必要があります。
-   TiDB でサポートされていない DDL ステートメントは、DM でもサポートされていません。
-   新しく追加された列のデフォルト値には、 `current_timestamp` 、 `rand()` 、 `uuid()`を含めることはできません。そうしないと、上流と下流の間でデータの不整合が発生する可能性があります。

## リスク {#risks}

移行タスクに楽観的モードを使用すると、DDL ステートメントはすぐにダウンストリームに移行されます。このモードを誤って使用すると、アップストリームとダウンストリームの間でデータの不整合が発生する可能性があります。

### データの不整合を引き起こす操作 {#operations-that-cause-data-inconsistency}

-   各シャード テーブルのスキーマは相互に互換性がありません。例:
    -   同じ名前の 2 つの列がそれぞれ 2 つのシャード テーブルに追加されていますが、列のタイプは異なります。
    -   同じ名前の 2 つの列がそれぞれ 2 つのシャード テーブルに追加されていますが、列のデフォルト値は異なります。
    -   同じ名前の 2 つの生成された列がそれぞれ 2 つのシャード テーブルに追加されますが、列は異なる式を使用して生成されます。
    -   同じ名前の 2 つのインデックスが 2 つのシャード テーブルにそれぞれ追加されていますが、キーは異なります。
    -   同じ名前を持つ他の異なるテーブル スキーマ。
-   シャード テーブル内のデータを破損する可能性のある DDL ステートメントを実行し、ロールバックを試みます。

    たとえば、列`X`を削除してから、この列を再度追加します。

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

この時点で、 `DEFAULT 0`と`DEFAULT -1`互いに互換性がないため、 `tbl00`の`Age`列目は不整合になります。この状況では、DM はエラーを報告しますが、データの不整合を手動で修正する必要があります。

## 実施原則 {#implementation-principle}

楽観的モードでは、DM ワーカーはアップストリームから DDL ステートメントを受け取った後、更新されたテーブル スキーマを DM マスターに転送します。DM ワーカーは各シャード テーブルの現在のスキーマを追跡し、DM マスターはこれらのスキーマを、すべてのシャード テーブルの DML ステートメントと互換性のある複合スキーマにマージします。次に、DM マスターは対応する DDL ステートメントをダウンストリームに移行します。DML ステートメントはダウンストリームに直接移行されます。

![optimistic-ddl-flow](/media/dm/optimistic-ddl-flow.png)

### 例 {#examples}

アップストリーム MySQL に 3 つのシャード テーブル ( `tbl00` 、 `tbl01` 、 `tbl02` ) があるとします。これらのシャード テーブルをダウンストリーム TiDB の`tbl`テーブルにマージして移行します。次の図を参照してください。

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

`tbl01`に`Level`列を追加します。

```sql
ALTER TABLE `tbl01` ADD COLUMN `Level` INT;
```

![optimistic-ddl-example-5](/media/dm/optimistic-ddl-example-5.png)

この時点で、ダウンストリームにはすでに同じ`Level`の列があるため、DM マスターはテーブル スキーマを比較した後、何も操作を実行しません。

`tbl01`に`Name`列をドロップします。

```sql
ALTER TABLE `tbl01` DROP COLUMN `Name`;
```

![optimistic-ddl-example-6](/media/dm/optimistic-ddl-example-6.png)

その後、ダウンストリームは`Name`列を含む`tbl00`と`tbl02`からの DML ステートメントを受信するため、この列はすぐには削除されません。

同様に、すべての DML ステートメントをダウンストリームに移行できます。

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

その時までに、 `Name`列はすべてのシャード テーブルから削除され、ダウンストリームで安全に削除できます。

```sql
ALTER TABLE `tbl` DROP COLUMN `Name`;
```

![optimistic-ddl-example-10](/media/dm/optimistic-ddl-example-10.png)
