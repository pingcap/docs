---
title: Views
summary: Learn how to use views in TiDB.
---

# ビュー {#views}

このドキュメントでは、TiDB でビューを使用する方法について説明します。

## 概要 {#overview}

TiDB はビューをサポートしています。ビューは仮想テーブルとして機能し、そのスキーマはビューを作成する`SELECT`ステートメントによって定義されます。

-   安全なフィールドとデータのみをユーザーに公開するビューを作成して、基になるテーブルの機密フィールドとデータのセキュリティを確保できます。
-   複雑なクエリをより簡単かつ便利にするために、頻繁に使用される複雑なクエリのビューを作成できます。

## ビューを作成する {#create-a-view}

TiDB では、複雑なクエリを`CREATE VIEW`ステートメントのビューとして定義できます。構文は次のとおりです。

```sql
CREATE VIEW view_name AS query;
```

既存のビューまたはテーブルと同じ名前のビューを作成できないことに注意してください。

たとえば、 [複数テーブル結合クエリ](/develop/dev-guide-join-tables.md) 、 `JOIN`ステートメントを使用して`books`テーブルと`ratings`テーブルを結合することにより、平均評価の書籍のリストを取得します。

後続のクエリの便宜上、次のステートメントを使用してクエリをビューとして定義できます。

```sql
CREATE VIEW book_with_ratings AS
SELECT b.id AS book_id, ANY_VALUE(b.title) AS book_title, AVG(r.score) AS average_score
FROM books b
LEFT JOIN ratings r ON b.id = r.book_id
GROUP BY b.id;
```

## クエリ ビュー {#query-views}

ビューが作成されると、 `SELECT`ステートメントを使用して、通常のテーブルと同じようにビューをクエリできます。

```sql
SELECT * FROM book_with_ratings LIMIT 10;
```

TiDB がビューにクエリを実行すると、ビューに関連付けられた`SELECT`ステートメントがクエリされます。

## ビューの更新 {#update-views}

現在、TiDB のビューは`ALTER VIEW view_name AS query;`サポートしていません。次の 2 つの方法でビューを「更新」できます。

-   `DROP VIEW view_name;`ステートメントで古いビューを削除してから、 `CREATE VIEW view_name AS query;`ステートメントで新しいビューを作成してビューを更新します。
-   `CREATE OR REPLACE VIEW view_name AS query;`ステートメントを使用して、既存のビューを同じ名前で上書きします。

```sql
CREATE OR REPLACE VIEW book_with_ratings AS
SELECT b.id AS book_id, ANY_VALUE(b.title), ANY_VALUE(b.published_at) AS book_title, AVG(r.score) AS average_score
FROM books b
LEFT JOIN ratings r ON b.id = r.book_id
GROUP BY b.id;
```

## ビュー関連の情報を取得する {#get-view-related-information}

### <code>SHOW CREATE TABLE|VIEW view_name</code>ステートメントの使用 {#using-the-code-show-create-table-view-view-name-code-statement}

```sql
SHOW CREATE VIEW book_with_ratings\G
```

結果は次のとおりです。

```
*************************** 1. row ***************************
                View: book_with_ratings
         Create View: CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `book_with_ratings` (`book_id`, `ANY_VALUE(b.title)`, `book_title`, `average_score`) AS SELECT `b`.`id` AS `book_id`,ANY_VALUE(`b`.`title`) AS `ANY_VALUE(b.title)`,ANY_VALUE(`b`.`published_at`) AS `book_title`,AVG(`r`.`score`) AS `average_score` FROM `bookshop`.`books` AS `b` LEFT JOIN `bookshop`.`ratings` AS `r` ON `b`.`id`=`r`.`book_id` GROUP BY `b`.`id`
character_set_client: utf8mb4
collation_connection: utf8mb4_general_ci
1 row in set (0.00 sec)
```

### <code>INFORMATION_SCHEMA.VIEWS</code>テーブルをクエリします。 {#query-the-code-information-schema-views-code-table}

```sql
SELECT * FROM information_schema.views WHERE TABLE_NAME = 'book_with_ratings'\G
```

結果は次のとおりです。

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

## ビューを削除 {#drop-views}

ビューをドロップするには、 `DROP VIEW view_name;`ステートメントを使用します。

```sql
DROP VIEW book_with_ratings;
```

## 制限 {#limitation}

TiDB でのビューの制限については、 [ビューの制限](/views.md#limitations)を参照してください。

## 続きを読む {#read-more}

-   [ビュー](/views.md)
-   [CREATE VIEW ステートメント](/sql-statements/sql-statement-create-view.md)
-   [DROP VIEW ステートメント](/sql-statements/sql-statement-drop-view.md)
-   [ビューを使用したEXPLAINステートメント](/explain-views.md)
-   [TiFlink: TiKV と Flink を使用した強整合性のマテリアライズド ビュー](https://github.com/tiflink/tiflink)
