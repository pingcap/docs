---
title: TiDB Data Migration Block and Allow Lists
summary: Learn how to use the DM block and allow lists feature.
---

# TiDB データ移行のブロック リストと許可リスト {#tidb-data-migration-block-and-allow-lists}

TiDB データ移行 (DM) を使用してデータを移行する場合、ブロック リストと許可リストを構成して、一部のデータベースまたは一部のテーブルのすべての操作をフィルター処理または移行することができます。

## ブロック リストと許可リストを構成する {#configure-the-block-and-allow-lists}

タスク構成ファイルで、次の構成を追加します。

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
      tbl-name: "t"
    ignore-tables:
    - db-name: "test"
      tbl-name: "log"
```

単純なシナリオでは、スキーマとテーブルの一致にワイルドカードを使用することをお勧めします。ただし、次のバージョンの違いに注意してください。

-   DM v1.0.5 以降のバージョンの場合、ブロック リストと許可リストは[ワイルドカードマッチ](https://en.wikipedia.org/wiki/Glob_(programming)#Syntax)サポートしますが、ワイルドカード式で指定できるのは`*`**だけ**であり、<strong>最後に</strong>`*`を配置する必要があります。

-   v1.0.5 より前の DM バージョンでは、ブロック リストと許可リストは正規表現の一致のみをサポートします。

## パラメータの説明 {#parameter-descriptions}

-   `do-dbs` : MySQL の[`replicate-do-db`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-do-db)と同様に、スキーマのリストの移行を許可します。
-   `ignore-dbs` : 移行するスキーマのブロック リスト。MySQL の[`replicate-ignore-db`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-ignore-db)に似ています。
-   `do-tables` : MySQL の[`replicate-do-table`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-do-table)と同様に、テーブルのリストの移行を許可します。 `db-name`と`tbl-name`の両方を指定する必要があります。
-   `ignore-tables` : 移行するテーブルのブロック リスト。MySQL の[`replicate-ignore-table`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-ignore-table)に似ています。 `db-name`と`tbl-name`の両方を指定する必要があります。

上記のパラメーターの値が`~`文字で始まる場合、この値の後続の文字は[正規表現](https://golang.org/pkg/regexp/syntax/#hdr-syntax)として扱われます。このパラメーターを使用して、スキーマまたはテーブル名を一致させることができます。

## フィルタリングプロセス {#filtering-process}

-   `do-dbs`と`ignore-dbs`に対応するフィルタリング ルールは、MySQL の[データベース レベルのレプリケーションおよびバイナリ ログ オプションの評価](https://dev.mysql.com/doc/refman/5.7/en/replication-rules-db-options.html)に似ています。
-   `do-tables`と`ignore-tables`に対応するフィルタリング ルールは、MySQL の[テーブル レベルのレプリケーション オプションの評価](https://dev.mysql.com/doc/refman/5.7/en/replication-rules-table-options.html)に似ています。

> **ノート：**
>
> DM と MySQL では、ブロック リストと許可リストのフィルタリング ルールは次の点で異なります。
>
> -   MySQL では、 [`replicate-wild-do-table`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-wild-do-table)と[`replicate-wild-ignore-table`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-wild-ignore-table)ワイルドカード文字をサポートしています。 DM では、一部のパラメーター値は、 `~`文字で始まる正規表現を直接サポートしています。
> -   DM は現在、 `ROW`形式のバイナリログのみをサポートしており、 `STATEMENT`または`MIXED`形式のバイナリログはサポートしていません。したがって、DM のフィルタリング ルールは、MySQL の`ROW`形式のフィルタリング ルールに対応します。
> -   MySQL は、ステートメントの`USE`セクションで明示的に指定されたデータベース名によってのみ DDL ステートメントを決定します。 DM は、最初に DDL ステートメントのデータベース名セクションに基づいてステートメントを決定します。 DDL ステートメントにそのようなセクションが含まれていない場合、DM は`USE`セクションによってステートメントを判別します。判別する SQL ステートメントが`USE test_db_2; CREATE TABLE test_db_1.test_table (c1 INT PRIMARY KEY)`であるとします。 `replicate-do-db=test_db_1`は MySQL で構成され、 `do-dbs: ["test_db_1"]`は DM で構成されます。次に、このルールは DM にのみ適用され、MySQL には適用されません。

`test`のフィルタリング プロセス。 `t`テーブルは次のとおりです。

1.  **スキーマ**レベルでフィルター処理します。

    -   `do-dbs`が空でない場合は、一致するスキーマが`do-dbs`に存在するかどうかを確認します。

        -   はいの場合は、引き続き**テーブル**レベルでフィルタリングします。
        -   そうでない場合は、フィルタ`test`を使用します。 `t` .

    -   `do-dbs`が空で`ignore-dbs`空でない場合、一致するスキーマが`ignore-dbs`に存在するかどうかを確認します。

        -   はいの場合、フィルター`test` 。 `t` .
        -   そうでない場合は、引き続き**テーブル**レベルでフィルタリングします。

    -   `do-dbs`と`ignore-dbs`両方が空の場合は、引き続き**テーブル**レベルでフィルタリングします。

2.  **テーブル**レベルでフィルター処理します。

    1.  `do-tables`が空でない場合、一致するテーブルが`do-tables`に存在するかどうかを確認します。

        -   はいの場合は、移行`test`します。 `t` .
        -   そうでない場合は、フィルタ`test`を使用します。 `t` .

    2.  `ignore-tables`が空でない場合、一致するテーブルが`ignore-tables`に存在するかどうかを確認します。

        -   はいの場合、フィルター`test` 。 `t` .
        -   そうでない場合は、移行`test`します。 `t` .

    3.  `do-tables`と`ignore-tables`両方が空の場合は、 `test`を移行します。 `t` .

> **ノート：**
>
> スキーマ`test`をフィルタリングする必要があるかどうかを確認するには、スキーマ レベルでフィルタリングするだけです。

## 使用例 {#usage-examples}

アップストリームの MySQL インスタンスに次のテーブルが含まれているとします。

```
`logs`.`messages_2016`
`logs`.`messages_2017`
`logs`.`messages_2018`
`forum`.`users`
`forum`.`messages`
`forum_backup_2016`.`messages`
`forum_backup_2017`.`messages`
`forum_backup_2018`.`messages`
```

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

| テーブル                             | フィルタリングするかどうか | フィルタリングする理由                                                                                                                                                |
| :------------------------------- | :------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `logs` . `messages_2016`         | はい            | スキーマ`logs`どの`do-dbs`とも一致しません。                                                                                                                              |
| `logs` . `messages_2017`         | はい            | スキーマ`logs`どの`do-dbs`とも一致しません。                                                                                                                              |
| `logs` . `messages_2018`         | はい            | スキーマ`logs`どの`do-dbs`とも一致しません。                                                                                                                              |
| `forum_backup_2016` . `messages` | はい            | スキーマ`forum_backup_2016`どの`do-dbs`とも一致しません。                                                                                                                 |
| `forum_backup_2017` . `messages` | はい            | スキーマ`forum_backup_2017`どの`do-dbs`とも一致しません。                                                                                                                 |
| `forum` . `users`                | はい            | <li>スキーマ`forum` `do-dbs`に一致し、引き続きテーブル レベルでフィルタリングします。<br/> 2. スキーマとテーブルは`do-tables`と`ignore-tables`のいずれとも一致せず、 `do-tables`は空ではありません。</li>                  |
| `forum` . `messages`             | いいえ           | <li>スキーマ`forum` `do-dbs`に一致し、引き続きテーブル レベルでフィルタリングします。<br/> 2. 表`messages` `do-tables`の`db-name: "~^forum.*",tbl-name: "messages"`の中にあります。</li>             |
| `forum_backup_2018` . `messages` | いいえ           | <li>スキーマ`forum_backup_2018` `do-dbs`に一致し、引き続きテーブル レベルでフィルタリングします。<br/> 2. スキーマとテーブルは`db-name: "~^forum.*",tbl-name: "messages"` of `do-tables`と一致します。</li> |
