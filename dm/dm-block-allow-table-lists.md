---
title: TiDB Data Migration Block and Allow Lists
summary: Learn how to use the DM block and allow lists feature.
---

# TiDB データ移行のブロック リストと許可リスト {#tidb-data-migration-block-and-allow-lists}

TiDB Data Migration (DM) を使用してデータを移行する場合、ブロックおよび許可リストを構成して、一部のデータベースまたは一部のテーブルのすべての操作をフィルタリングしたり、すべての操作のみを移行したりできます。

## ブロックリストと許可リストを構成する {#configure-the-block-and-allow-lists}

タスク構成ファイルに次の構成を追加します。

```yaml
block-allow-list:             # Use black-white-list if the DM version is earlier than or equal to v2.0.0-beta.2.
  rule-1:
    do-dbs: ["test*"]         # Starting with characters other than "~" indicates that it is a wildcard;
                              # v1.0.5 or later versions support the regular expression rules.
    do-tables:
    - db-name: "test[123]"    # Matches test1, test2, and test3.
      tbl-name: "t[1-5]"      # Matches t1, t2, t3, t4, and t5.
    - db-name: "test"
      tbl-name: "t"
  rule-2:
    do-dbs: ["~^test.*"]      # Starting with "~" indicates that it is a regular expression.
    ignore-dbs: ["mysql"]
    do-tables:
    - db-name: "~^test.*"
      tbl-name: "~^t.*"
    - db-name: "test"
      tbl-name: "t*"
    ignore-tables:
    - db-name: "test"
      tbl-name: "log"
```

単純なシナリオでは、スキーマとテーブルを一致させるためにワイルドカードを使用することをお勧めします。ただし、次のバージョンの違いに注意してください。

-   `*` 、 `?` 、および`[]`を含むワイルドカードがサポートされています。ワイルドカード一致では`*`シンボルは 1 つだけ使用でき、最後になければなりません。たとえば、 `tbl-name: "t*"`では、 `"t*"` `t`で始まるすべてのテーブルを示します。詳細は[ワイルドカードマッチング](https://en.wikipedia.org/wiki/Glob_(programming)#Syntax)参照してください。

-   正規表現は`~`文字で始まる必要があります。

## パラメータの説明 {#parameter-descriptions}

-   `do-dbs` : MySQL の[`replicate-do-db`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-do-db)と同様に、スキーマのリストの移行を許可します。
-   `ignore-dbs` : MySQL の[`replicate-ignore-db`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-ignore-db)に似た、移行するスキーマのブロック リスト。
-   `do-tables` : MySQL の[`replicate-do-table`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-do-table)と同様に、テーブルのリストの移行を許可します。 `db-name`と`tbl-name`の両方を指定する必要があります。
-   `ignore-tables` : MySQL の[`replicate-ignore-table`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-ignore-table)に似た、移行するテーブルのブロック リスト。 `db-name`と`tbl-name`の両方を指定する必要があります。

上記のパラメータの値が`~`文字で始まる場合、この値の後続の文字は[正規表現](https://golang.org/pkg/regexp/syntax/#hdr-syntax)として扱われます。このパラメータを使用して、スキーマ名またはテーブル名を一致させることができます。

## フィルタリングプロセス {#filtering-process}

-   `do-dbs`と`ignore-dbs`に対応するフィルタリング ルールは、MySQL の[データベースレベルのレプリケーションとバイナリログオプションの評価](https://dev.mysql.com/doc/refman/5.7/en/replication-rules-db-options.html)に似ています。
-   `do-tables`と`ignore-tables`に対応するフィルタリング ルールは、MySQL の[テーブルレベルのレプリケーション オプションの評価](https://dev.mysql.com/doc/refman/5.7/en/replication-rules-table-options.html)に似ています。

> **注記：**
>
> DM と MySQL では、ブロック リストと許可リストのフィルタリング ルールが次の点で異なります。
>
> -   MySQL では、 [`replicate-wild-do-table`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-wild-do-table)と[`replicate-wild-ignore-table`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-wild-ignore-table)ワイルドカード文字をサポートします。 DM では、一部のパラメーター値は、 `~`文字で始まる正規表現を直接サポートします。
> -   DM は現在、 `ROW`形式のバイナリログのみをサポートしており、 `STATEMENT`または`MIXED`形式のバイナリログはサポートしていません。したがって、DM のフィルタリング ルールは、MySQL の`ROW`形式のルールに対応します。
> -   MySQL は、ステートメントの`USE`セクションで明示的に指定されたデータベース名のみによって DDL ステートメントを決定します。 DM は、まず DDL ステートメントのデータベース名セクションに基づいてステートメントを決定します。 DDL ステートメントにそのようなセクションが含まれていない場合、DM は`USE`番目のセクションによってステートメントを決定します。判定対象の SQL ステートメントが`USE test_db_2; CREATE TABLE test_db_1.test_table (c1 INT PRIMARY KEY)`であるとします。 `replicate-do-db=test_db_1`は MySQL で構成され、 `do-dbs: ["test_db_1"]`は DM で構成されます。このルールは DM にのみ適用され、MySQL には適用されません。

a `test`のフィルタリング プロセス。 `t`表は以下の通りです。

1.  **スキーマ**レベルでフィルタリングします。

    -   `do-dbs`が空でない場合は、一致するスキーマが`do-dbs`に存在するかどうかを確認します。

        -   「はい」の場合は、**テーブル**レベルでのフィルタリングを続けます。
        -   そうでない場合は、フィルタ`test`を実行します。 `t` ．

    -   `do-dbs`が空で`ignore-dbs`空でない場合は、一致するスキーマが`ignore-dbs`に存在するかどうかを確認します。

        -   「はい」の場合は、フィルター`test`を適用します。 `t` ．
        -   そうでない場合は、**テーブル**レベルでのフィルタリングを続けます。

    -   `do-dbs`と`ignore-dbs`の両方が空の場合は、**テーブル**レベルでのフィルタ処理を続けます。

2.  **テーブル**レベルでフィルタリングします。

    1.  `do-tables`が空でない場合は、 `do-tables`に一致するテーブルが存在するかどうかを確認します。

        -   「はい」の場合、移行`test` 。 `t` ．
        -   そうでない場合は、フィルタ`test`を実行します。 `t` ．

    2.  `ignore-tables`が空でない場合は、 `ignore-tables`に一致するテーブルが存在するかどうかを確認します。

        -   「はい」の場合は、フィルター`test`を適用します。 `t` ．
        -   そうでない場合は、移行します`test` 。 `t` ．

    3.  `do-tables`と`ignore-tables`両方が空の場合は、 `test`を移行します。 `t` ．

> **注記：**
>
> スキーマ`test`フィルタリングする必要があるかどうかを確認するには、スキーマ レベルでフィルタリングするだけで済みます。

## 使用例 {#usage-examples}

アップストリームの MySQL インスタンスに次のテーブルが含まれていると仮定します。

    `logs`.`messages_2016`
    `logs`.`messages_2017`
    `logs`.`messages_2018`
    `forum`.`users`
    `forum`.`messages`
    `forum_backup_2016`.`messages`
    `forum_backup_2017`.`messages`
    `forum_backup_2018`.`messages`

構成は次のとおりです。

```yaml
block-allow-list:  # Use black-white-list if the DM version is earlier than or equal to v2.0.0-beta.2.
  bw-rule:
    do-dbs: ["forum_backup_2018", "forum"]
    ignore-dbs: ["~^forum_backup_"]
    do-tables:
    - db-name: "logs"
      tbl-name: "~_2018$"
    - db-name: "~^forum.*"
​      tbl-name: "messages"
    ignore-tables:
    - db-name: "~.*"
​      tbl-name: "^messages.*"
```

`bw-rule`ルールを適用した後:

| テーブル                             | フィルタをかけるかどうか | フィルターをかける理由                                                                                                                                              |
| :------------------------------- | :----------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `logs` 。 `messages_2016`         | はい           | スキーマ`logs`どの`do-dbs`とも一致しません。                                                                                                                            |
| `logs` 。 `messages_2017`         | はい           | スキーマ`logs`どの`do-dbs`とも一致しません。                                                                                                                            |
| `logs` 。 `messages_2018`         | はい           | スキーマ`logs`どの`do-dbs`とも一致しません。                                                                                                                            |
| `forum_backup_2016` 。 `messages` | はい           | スキーマ`forum_backup_2016`どの`do-dbs`とも一致しません。                                                                                                               |
| `forum_backup_2017` 。 `messages` | はい           | スキーマ`forum_backup_2017`どの`do-dbs`とも一致しません。                                                                                                               |
| `forum` 。 `users`                | はい           | <li>スキーマ`forum` `do-dbs`と一致し、テーブル レベルでのフィルタ処理を続けます。<br/> 2. スキーマとテーブルが`do-tables`と`ignore-tables`のいずれにも一致せず、 `do-tables`空ではありません。</li>                   |
| `forum` 。 `messages`             | いいえ          | <li>スキーマ`forum` `do-dbs`と一致し、テーブル レベルでのフィルタ処理を続けます。<br/> 2. 表`messages` `do-tables` `db-name: "~^forum.*",tbl-name: "messages"`含まれます。</li>               |
| `forum_backup_2018` 。 `messages` | いいえ          | <li>スキーマ`forum_backup_2018` `do-dbs`と一致し、テーブル レベルでのフィルタ処理を続けます。<br/> 2. スキーマとテーブルは`db-name: "~^forum.*",tbl-name: "messages"` of `do-tables`と一致します。</li> |
