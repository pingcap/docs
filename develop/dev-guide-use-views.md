---
title: Views
---

# Views

## Overview

TiDB supports views. A view is a virtual table whose structure is defined by the `SELECT` statement when creating a view.

- The view allows you to expose only secure fields and data to the user, thus securing the sensitive fields and data of the underlying table.
- Defining frequently occurring complex queries as views can make complex queries simpler and more convenient.

## Create a view

In TiDB, a complex query can be defined as a view through the `CREATE VIEW` statement. The syntax is as follows:

```sql
CREATE VIEW view_name AS query;
```

Note: that you cannot create a view with the same name as an existing view or table.

For example, in the [multi-table join query](/develop/dev-guide-join-tables.md) chapter, we query the list of books with average ratings by joining the `books` table and the `ratings` table through a `JOIN` statement. 

For the convenience of subsequent queries, we can define the query statement as a view, and the SQL statement is as follows:

{{< copyable "sql" >}}

```sql
CREATE VIEW book_with_ratings AS
SELECT b.id AS book_id, ANY_VALUE(b.title) AS book_title, AVG(r.score) AS average_score
FROM books b
LEFT JOIN ratings r ON b.id = r.book_id
GROUP BY b.id;
```

## Query view

Once the view is created, we can use the `SELECT` statement to query the view just like a normal data table.

{{< copyable "sql" >}}

```sql
SELECT * FROM book_with_ratings LIMIT 10;
```

When TiDB executes a query view statement, it expands the view into the `SELECT` statement defined when the view was created, and then executes the expanded query statement.

## Update view

For now, views in TiDB do not support the `ALTER VIEW view_name AS query;` syntax. You can "update" a view in the following two ways:

- First delete the old view with the `DROP VIEW view_name;` statement, and then update the view by creating a new view with the `CREATE VIEW view_name AS query;` statement.
- Use the `CREATE OR REPLACE VIEW view_name AS query;` statement to overwrite an existing view with the same name.

{{< copyable "sql" >}}

```sql
CREATE OR REPLACE VIEW book_with_ratings AS
SELECT b.id AS book_id, ANY_VALUE(b.title), ANY_VALUE(b.published_at) AS book_title, AVG(r.score) AS average_score
FROM books b
LEFT JOIN ratings r ON b.id = r.book_id
GROUP BY b.id;
```

## Get view related information

### Using the `SHOW CREATE TABLE|VIEW view_name` statement

{{< copyable "sql" >}}

```sql
SHOW CREATE VIEW book_with_ratings\G
```

```
*************************** 1. row ***************************
                View: book_with_ratings
         Create View: CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `book_with_ratings` (`book_id`, `ANY_VALUE(b.title)`, `book_title`, `average_score`) AS SELECT `b`.`id` AS `book_id`,ANY_VALUE(`b`.`title`) AS `ANY_VALUE(b.title)`,ANY_VALUE(`b`.`published_at`) AS `book_title`,AVG(`r`.`score`) AS `average_score` FROM `bookshop`.`books` AS `b` LEFT JOIN `bookshop`.`ratings` AS `r` ON `b`.`id`=`r`.`book_id` GROUP BY `b`.`id`
character_set_client: utf8mb4
collation_connection: utf8mb4_general_ci
1 row in set (0.00 sec)
```

### Query the `INFORMATION_SCHEMA.VIEWS` table

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.views WHERE TABLE_NAME = 'book_with_ratings'\G
```

```
*************************** 1. row ***************************
       TABLE_CATALOG: def
        TABLE_SCHEMA: bookshop
          TABLE_NAME: book_with_ratings
     VIEW_DEFINITION: SELECT `b`.`id` AS `book_id`,ANY_VALUE(`b`.`title`) AS `ANY_VALUE(b.title)`,ANY_VALUE(`b`.`published_at`) AS `book_title`,AVG(`r`.`score`) AS `average_score` FROM `bookshop`.`books` AS `b` LEFT JOIN `bookshop`.`ratings` AS `r` ON `b`.`id`=`r`.`book_id` GROUP BY `b`.`id`
        CHECK_OPTION: CASCADED
        IS_UPDATABLE: NO
             DEFINER: root@%
       SECURITY_TYPE: DEFINER
CHARACTER_SET_CLIENT: utf8mb4
COLLATION_CONNECTION: utf8mb4_general_ci
1 row in set (0.00 sec)
```

## Drop view

Views that have been created can be dropped with the `DROP VIEW view_name;` statement.

{{< copyable "sql" >}}

```sql
DROP VIEW book_with_ratings;
```

## Limitation

You can learn more about the limitations by reading the [View](/views.md#limitations) section in the reference documentation.

## Read More

- [Views](/views.md)
- [CREATE VIEW](/common/sql-statements/sql-statement-create-view.md)
- [DROP VIEW](/common/sql-statements/sql-statement-drop-view.md)
- [EXPLAIN Statements Using Views](/explain-views.md)
- [TiFlink: Strongly Consistent Materialized Views Using TiKV and Flink](https://github.com/tiflink/tiflink)
