---
title: TiDB Data Migration Block and Allow Lists
summary: DM ブロックおよび許可リスト機能の使用方法を学びます。
---

# TiDB データ移行ブロックリストと許可リスト {#tidb-data-migration-block-and-allow-lists}

TiDB データ移行 (DM) を使用してデータを移行する場合、ブロック リストと許可リストを構成して、一部のデータベースまたは一部のテーブルのすべての操作をフィルター処理したり、移行のみを行ったりすることができます。

## ブロックリストと許可リストを設定する {#configure-the-block-and-allow-lists}

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

-   `*` 、 `?` 、 `[]`などのワイルドカードがサポートされています。ワイルドカードの一致には`*`記号が 1 つだけ存在でき、末尾に配置する必要があります。たとえば、 `tbl-name: "t*"`では、 `"t*"` `t`で始まるすべてのテーブルを示します。詳細については[ワイルドカードマッチング](https://en.wikipedia.org/wiki/Glob_(programming)#Syntax)を参照してください。

-   正規表現は`~`文字で始まる必要があります。

## パラメータの説明 {#parameter-descriptions}

-   `do-dbs` : MySQL の[`replicate-do-db`](https://dev.mysql.com/doc/refman/8.0/en/replication-options-replica.html#option_mysqld_replicate-do-db)と同様に、移行するスキーマのリストを許可します。
-   `ignore-dbs` : 移行するスキーマのブロック リスト。MySQL の[`replicate-ignore-db`](https://dev.mysql.com/doc/refman/8.0/en/replication-options-replica.html#option_mysqld_replicate-ignore-db)に似ています。
-   `do-tables` : MySQL の[`replicate-do-table`](https://dev.mysql.com/doc/refman/8.0/en/replication-options-replica.html#option_mysqld_replicate-do-table)と同様に、移行するテーブルのリストを許可します。4 と`tbl-name` `db-name`を指定する必要があります。
-   `ignore-tables` : 移行するテーブルのブロック リスト。MySQL の[`replicate-ignore-table`](https://dev.mysql.com/doc/refman/8.0/en/replication-options-replica.html#option_mysqld_replicate-ignore-table)に似ています。4 と`tbl-name` `db-name`を指定する必要があります。

上記のパラメータの値が`~`文字で始まる場合、この値のその後の文字は[正規表現](https://golang.org/pkg/regexp/syntax/#hdr-syntax)として扱われます。このパラメータを使用して、スキーマ名またはテーブル名を一致させることができます。

## フィルタリングプロセス {#filtering-process}

-   `do-dbs`と`ignore-dbs`に対応するフィルタリング ルールは、MySQL の[データベースレベルのレプリケーションとバイナリログオプションの評価](https://dev.mysql.com/doc/refman/8.0/en/replication-rules-db-options.html)と同様です。
-   `do-tables`と`ignore-tables`に対応するフィルタリング ルールは、MySQL の[テーブルレベルのレプリケーション オプションの評価](https://dev.mysql.com/doc/refman/8.0/en/replication-rules-table-options.html)と同様です。

> **注記：**
>
> DM と MySQL では、ブロック リストと許可リストのフィルタリング ルールが次の点で異なります。
>
> -   MySQL では、 [`replicate-wild-do-table`](https://dev.mysql.com/doc/refman/8.0/en/replication-options-replica.html#option_mysqld_replicate-wild-do-table)と[`replicate-wild-ignore-table`](https://dev.mysql.com/doc/refman/8.0/en/replication-options-replica.html#option_mysqld_replicate-wild-ignore-table)ワイルドカード文字をサポートします。DM では、一部のパラメータ値は`~`文字で始まる正規表現を直接サポートします。
> -   DM は現在、 `ROW`形式のバイナリログのみをサポートしており、 `STATEMENT`形式や`MIXED`形式のバイナリログはサポートしていません。したがって、DM のフィルタリング ルールは、MySQL の`ROW`形式のフィルタリング ルールに対応しています。
> -   MySQL は、ステートメントの`USE`セクションで明示的に指定されたデータベース名のみで DDL ステートメントを決定します。DM は、まず DDL ステートメントのデータベース名セクションに基づいてステートメントを決定します。DDL ステートメントにそのようなセクションが含まれていない場合、DM は`USE`セクションでステートメントを決定します。決定する SQL ステートメントが`USE test_db_2; CREATE TABLE test_db_1.test_table (c1 INT PRIMARY KEY)`であり、 `replicate-do-db=test_db_1`が MySQL で構成され、 `do-dbs: ["test_db_1"]` DM で構成されているとします。この場合、このルールは DM にのみ適用され、MySQL には適用されません。

`test`テーブルのフィルタリング プロセス`t`次のとおりです。

1.  **スキーマ**レベルでフィルターします。

    -   `do-dbs`空でない場合は、 `do-dbs`に一致するスキーマが存在するかどうかを確認します。

        -   はいの場合は、**テーブル**レベルでフィルタリングを続行します。
        -   そうでない場合は、 `test` . `t`をフィルタリングします。

    -   `do-dbs`が空で`ignore-dbs`空でない場合は、 `ignore-dbs`に一致するスキーマが存在するかどうかを確認します。

        -   はいの場合は、フィルター`test` 。 `t` 。
        -   そうでない場合は、**テーブル**レベルでフィルタリングを続行します。

    -   `do-dbs`と`ignore-dbs`両方が空の場合は、**テーブル**レベルでフィルタリングを続行します。

2.  **テーブル**レベルでフィルターします。

    1.  `do-tables`空でない場合は、 `do-tables`に一致するテーブルが存在するかどうかを確認します。

        -   はいの場合は、 `test` . `t` . を移行します。
        -   そうでない場合は、 `test` . `t`をフィルタリングします。

    2.  `ignore-tables`空でない場合は、 `ignore-tables`に一致するテーブルが存在するかどうかを確認します。

        -   はいの場合は、フィルター`test` 。 `t` 。
        -   そうでない場合は、 `test` . `t`を移行します。

    3.  `do-tables`と`ignore-tables`の両方が空の場合は、 `test` 。 `t` 。

> **注記：**
>
> スキーマ`test`をフィルタリングする必要があるかどうかを確認するには、スキーマ レベルでフィルタリングするだけで済みます。

## 使用例 {#usage-examples}

アップストリーム MySQL インスタンスに次のテーブルが含まれていると仮定します。

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

| テーブル                             | フィルタリングするかどうか | なぜフィルタリングするのか                                                                                                                                          |
| :------------------------------- | :------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `logs` 。 `messages_2016`         | はい            | スキーマ`logs`いずれの`do-dbs`とも一致しません。                                                                                                                        |
| `logs` 。 `messages_2017`         | はい            | スキーマ`logs`いずれの`do-dbs`とも一致しません。                                                                                                                        |
| `logs` 。 `messages_2018`         | はい            | スキーマ`logs`いずれの`do-dbs`とも一致しません。                                                                                                                        |
| `forum_backup_2016` 。 `messages` | はい            | スキーマ`forum_backup_2016`いずれの`do-dbs`とも一致しません。                                                                                                           |
| `forum_backup_2017` 。 `messages` | はい            | スキーマ`forum_backup_2017`いずれの`do-dbs`とも一致しません。                                                                                                           |
| `forum` 。 `users`                | はい            | <li>スキーマ`forum` `do-dbs`と一致し、テーブル レベルでフィルタリングを続行します。<br/> 2. スキーマとテーブルが`do-tables`と`ignore-tables`のいずれにも一致せず、 `do-tables`空ではありません。</li>                |
| `forum` 。 `messages`             | いいえ           | <li>スキーマ`forum` `do-dbs`と一致し、テーブル レベルでフィルタリングを続行します。<br/> 2. 表`messages` `do-tables`の`db-name: "~^forum.*",tbl-name: "messages"`にあります。</li>            |
| `forum_backup_2018` 。 `messages` | いいえ           | <li>スキーマ`forum_backup_2018` `do-dbs`と一致し、テーブル レベルでフィルタリングを続行します。<br/> 2. スキーマとテーブルは`do-tables`中`db-name: "~^forum.*",tbl-name: "messages"`と一致します。</li> |
