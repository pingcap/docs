---
title: Merge and Migrate Data from Sharded Tables in Optimistic Mode
summary: Learn how DM merges and migrates data from sharded tables in the optimistic mode.
---

# オプティミスティック モードでのシャード テーブルからのデータのマージと移行 {#merge-and-migrate-data-from-sharded-tables-in-optimistic-mode}

このドキュメントでは、楽観的モードのデータ マイグレーション (DM) によって提供されるシャーディング サポート機能について説明します。この機能を使用すると、上流の MySQL または MariaDB インスタンス内の同じまたは異なるテーブル スキーマを持つテーブルのデータをマージして、下流の TiDB 内の 1 つの同じテーブルに移行できます。

> **ノート：**
>
> 楽観的モードとその制限について十分に理解していない場合は、このモードを使用し**ないこと**をお勧めします。そうしないと、移行が中断されたり、データの不整合が発生したりする可能性があります。

## バックグラウンド {#background}

DM は、シャーディング DDL と呼ばれるオンラインでのシャード テーブルでの DDL ステートメントの実行をサポートし、デフォルトで「悲観的モード」を使用します。このモードでは、アップストリームのシャード テーブルで DDL ステートメントが実行されると、同じ DDL ステートメントが他のすべてのシャード テーブルで実行されるまで、このテーブルのデータ移行が一時停止されます。それまでに、この DDL ステートメントがダウンストリームで実行され、データ移行が再開されます。

悲観的モードでは、ダウンストリームに移行されるデータが常に正しいことが保証されますが、データの移行が一時停止されるため、アップストリームで A/B 変更を行うには適していません。場合によっては、ユーザーが 1 つのシャード テーブルで DDL ステートメントの実行に長時間を費やし、一定期間の検証後にのみ他のシャード テーブルのスキーマを変更することがあります。悲観的モードでは、これらの DDL ステートメントがデータの移行をブロックし、多くのbinlogイベントが蓄積されます。

したがって、「楽観的モード」が必要です。このモードでは、シャード テーブルで実行された DDL ステートメントは、他のシャード テーブルと互換性のあるステートメントに自動的に変換され、すぐにダウンストリームに移行されます。このように、DDL ステートメントはシャード テーブルが DML 移行を実行するのをブロックしません。

## 楽観的モードのコンフィグレーション {#configuration-of-the-optimistic-mode}

楽観的モードを使用するには、タスク構成ファイルで`shard-mode`項目を`optimistic`として指定します。詳細なサンプル構成ファイルについては、 [DM 拡張タスクコンフィグレーションファイル](/dm/task-configuration-file-full.md)を参照してください。

## 制限 {#restrictions}

楽観的モードを使用するには、いくつかのリスクが伴います。使用するときは、次の規則に従ってください。

-   DDL ステートメントのバッチを実行する前後に、すべてのシャード テーブルのスキーマが互いに一貫していることを確認します。

-   A/B テストを実行する場合は、1 つのシャード テーブルで**のみ**テストを実行します。

-   A/B テストが終了したら、最も直接的な DDL ステートメントのみを最終的なスキーマに移行します。テストのすべての正しいステップまたは間違ったステップを再実行しないでください。

    たとえば、シャード テーブルで`ADD COLUMN A INT; DROP COLUMN A; ADD COLUMN A FLOAT;`を実行した場合、他のシャード テーブルでは`ADD COLUMN A FLOAT`を実行するだけで済みます。 3 つの DDL ステートメントすべてを再度実行する必要はありません。

-   DDL ステートメントを実行するときに、DM 移行のステータスを監視します。エラーが報告されたら、この DDL ステートメントのバッチがデータの不整合を引き起こすかどうかを判断する必要があります。

楽観的モードでは、アップストリームで実行された DDL ステートメントのほとんどが自動的にダウンストリームに移行され、追加の作業は必要ありません。これらの DDL ステートメントは「タイプ 1 DDL」と呼ばれます。

列名、列タイプ、または列のデフォルト値を変更する DDL ステートメントは、「タイプ 2 DDL」と呼ばれます。アップストリームでタイプ 2 の DDL ステートメントを実行する場合は、すべてのシャード テーブルで DDL ステートメントを同じ順序で実行するようにしてください。

タイプ 2 DDL ステートメントの例を次に示します。

-   列のタイプを変更します: `ALTER TABLE table_name MODIFY COLUMN column_name VARCHAR(20)` .
-   列の名前を変更します: `ALTER TABLE table_name RENAME COLUMN column_1 TO column_2;` .
-   デフォルト値`ALTER TABLE table_name ADD COLUMN column_1 NOT NULL;`なしで`NOT NULL`列を追加します。
-   インデックスの名前を変更します: `ALTER TABLE table_name RENAME INDEX index_1 TO index_2;` .

分割されたテーブルが上記の DDL ステートメントを実行するときに、実行順序が異なると、移行が中断されます。例えば：

-   シャード 1 は、列の名前を変更してから、列の型を変更します。
    1.  列の名前を変更します: `ALTER TABLE table_name RENAME COLUMN column_1 TO column_2;` .
    2.  列タイプを変更します: `ALTER TABLE table_name MODIFY COLUMN column_3 VARCHAR(20);` 。
-   シャード 2 は、列の型を変更してから、列の名前を変更します。
    1.  列タイプを変更します: `ALTER TABLE table_name MODIFY COLUMN column_3 VARCHAR(20)` .
    2.  列の名前を変更します: `ALTER TABLE table_name RENAME COLUMN column_1 TO column_2;` .

さらに、楽観的モードと悲観的モードの両方に次の制限が適用されます。

-   `DROP TABLE`または`DROP DATABASE`はサポートされていません。
-   `TRUNCATE TABLE`はサポートされていません。
-   各 DDL ステートメントには、1 つのテーブルのみに対する操作が含まれている必要があります。
-   TiDB でサポートされていない DDL ステートメントは、DM でもサポートされていません。
-   新しく追加された列のデフォルト値には、 `current_timestamp` `uuid()`含めること`rand()`できません。そうしないと、上流と下流の間でデータの不整合が発生する可能性があります。

## リスク {#risks}

移行タスクに楽観的モードを使用すると、DDL ステートメントはすぐにダウンストリームに移行されます。このモードを誤用すると、上流と下流の間でデータの不整合が発生する可能性があります。

### データの不整合を引き起こす操作 {#operations-that-cause-data-inconsistency}

-   各シャード テーブルのスキーマは互いに互換性がありません。例えば：
    -   同じ名前の 2 つの列が 2 つのシャード テーブルにそれぞれ追加されますが、列の型は異なります。
    -   同じ名前の 2 つの列がそれぞれ 2 つのシャード テーブルに追加されますが、列の既定値は異なります。
    -   同じ名前の 2 つの生成された列がそれぞれ 2 つのシャード テーブルに追加されますが、列は異なる式を使用して生成されます。
    -   同じ名前の 2 つのインデックスが 2 つのシャード テーブルにそれぞれ追加されますが、キーは異なります。
    -   同じ名前の他の異なるテーブル スキーマ。
-   シャード テーブルのデータを破損する可能性のある DDL ステートメントを実行してから、ロールバックを試みます。

    たとえば、列`X`を削除してから、この列を追加し直します。

### 例 {#example}

次の 3 つのシャード テーブルをマージして TiDB に移行します。

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

それまでに、 `DEFAULT 0`と`DEFAULT -1`は互いに互換性がないため、 `tbl00`の`Age`列は矛盾しています。この場合、DM はエラーを報告しますが、データの不整合を手動で修正する必要があります。

## 実施原則 {#implementation-principle}

楽観的モードでは、DM-worker がアップストリームから DDL ステートメントを受け取った後、更新されたテーブル スキーマを DM-master に転送します。 DM-worker は各シャード テーブルの現在のスキーマを追跡し、DM-master はこれらのスキーマをすべてのシャード テーブルの DML ステートメントと互換性のある複合スキーマにマージします。次に、DM マスターは、対応する DDL ステートメントをダウンストリームに移行します。 DML ステートメントはダウンストリームに直接移行されます。

![optimistic-ddl-flow](/media/dm/optimistic-ddl-flow.png)

### 例 {#examples}

アップストリームの MySQL に 3 つのシャード テーブル ( `tbl00` 、 `tbl01` 、および`tbl02` ) があるとします。これらの分割されたテーブルをマージして、下流の TiDB の`tbl`テーブルに移行します。次の画像を参照してください。

![optimistic-ddl-example-1](/media/dm/optimistic-ddl-example-1.png)

アップストリームに`Level`列を追加します。

```sql
ALTER TABLE `tbl00` ADD COLUMN `Level` INT;
```

![optimistic-ddl-example-2](/media/dm/optimistic-ddl-example-2.png)

次に、TiDB は`tbl00`から DML ステートメント ( `Level`列あり) を受け取り、 `tbl01`および`tbl02`テーブル ( `Level`列なし) から DML ステートメントを受け取ります。

![optimistic-ddl-example-3](/media/dm/optimistic-ddl-example-3.png)

次の DML ステートメントは、変更なしでダウンストリームに移行できます。

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

この時点で、ダウンストリームには既に同じ列が`Level`あるため、DM-master はテーブル スキーマを比較した後、何も実行しません。

`Name`列を`tbl01`にドロップします。

```sql
ALTER TABLE `tbl01` DROP COLUMN `Name`;
```

![optimistic-ddl-example-6](/media/dm/optimistic-ddl-example-6.png)

次に、ダウンストリームは`tbl00`と`tbl02`から`Name`列の DML ステートメントを受け取るため、この列はすぐには削除されません。

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

それまでに、シャードされたすべてのテーブルの列は`Level`になります。

`Name`列をそれぞれ`tbl00`と`tbl02`にドロップします。

```sql
ALTER TABLE `tbl00` DROP COLUMN `Name`;
ALTER TABLE `tbl02` DROP COLUMN `Name`;
```

![optimistic-ddl-example-9](/media/dm/optimistic-ddl-example-9.png)

それまでに、シャードされたすべてのテーブルから`Name`列が削除され、ダウンストリームで安全に削除できます。

```sql
ALTER TABLE `tbl` DROP COLUMN `Name`;
```

![optimistic-ddl-example-10](/media/dm/optimistic-ddl-example-10.png)
