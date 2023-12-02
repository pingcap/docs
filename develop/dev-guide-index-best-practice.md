---
title: Best Practices for Indexing
summary: Learn some best practices for creating and using indexes in TiDB.
---

<!-- markdownlint-disable MD029 -->

# インデックス作成のベスト プラクティス {#best-practices-for-indexing}

このドキュメントでは、TiDB でインデックスを作成および使用するためのいくつかのベスト プラクティスを紹介します。

## あなたが始める前に {#before-you-begin}

このセクションでは、例として[書店](/develop/dev-guide-bookshop-schema-design.md)データベースの`books`テーブルを取り上げます。

```sql
CREATE TABLE `books` (
  `id` bigint(20) AUTO_RANDOM NOT NULL,
  `title` varchar(100) NOT NULL,
  `type` enum('Magazine', 'Novel', 'Life', 'Arts', 'Comics', 'Education & Reference', 'Humanities & Social Sciences', 'Science & Technology', 'Kids', 'Sports') NOT NULL,
  `published_at` datetime NOT NULL,
  `stock` int(11) DEFAULT '0',
  `price` decimal(15,2) DEFAULT '0.0',
  PRIMARY KEY (`id`) CLUSTERED
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
```

## インデックス作成のベストプラクティス {#best-practices-for-creating-indexes}

-   複数の列を含む結合インデックスを作成します。これは[インデックスの最適化をカバーする](/explain-indexes.md#indexreader)と呼ばれる最適化です。**インデックスの最適化をカバーすると、** TiDB はインデックス上でデータを直接クエリできるようになり、パフォーマンスの向上に役立ちます。

-   頻繁にクエリを実行しない列にはセカンダリ インデックスを作成しないでください。便利なセカンダリ インデックスを使用するとクエリを高速化できますが、副作用もあることに注意してください。インデックスを追加するたびに、行を挿入するときに追加の Key-Value が追加されます。インデックスの数が増えると、書き込みが遅くなり、消費するスペースも増えます。さらに、インデックスが多すぎるとオプティマイザーの実行時間に影響し、不適切なインデックスはオプティマイザーに誤解を与える可能性があります。したがって、インデックスが多いほどパフォーマンスが向上するとは限りません。

-   アプリケーションに基づいて適切なインデックスを作成します。原則として、パフォーマンスを向上させるために、クエリで使用される列にのみインデックスを作成します。インデックスの作成には次のような場合が適しています。

    -   区別度の高い列を使用すると、フィルター処理される行の数を大幅に減らすことができます。たとえば、個人 ID 番号についてはインデックスを作成するが、性別については作成しないことをお勧めします。
    -   複数の条件でクエリを実行する場合は、結合インデックスを使用します。同等の条件を持つ列は、結合インデックスの前に配置する必要があることに注意してください。以下に例を示します。 `select* from t where c1 = 10 and c2 = 100 and c3 > 10`クエリが頻繁に使用される場合は、クエリ条件によってスキャンするためのインデックス プレフィックスを構築できるように、結合インデックス`Index cidx (c1, c2, c3)`の作成を検討してください。

-   セカンダリ インデックスにはわかりやすい名前を付け、会社または組織のテーブル命名規則に従うことをお勧めします。このような命名規則が存在しない場合は、 [インデックス命名仕様](/develop/dev-guide-object-naming-guidelines.md)の規則に従ってください。

## インデックスを使用するためのベスト プラクティス {#best-practices-for-using-indexes}

-   インデックスはクエリを高速化するためのものであるため、既存のインデックスが一部のクエリで実際に使用されていることを確認してください。インデックスがどのクエリでも使用されない場合、そのインデックスは無意味であるため、削除する必要があります。

-   結合インデックスを使用する場合は、左プレフィックスの規則に従ってください。

    `title`と`published_at`列に新しい結合インデックスを作成するとします。

    ```sql
    CREATE INDEX title_published_at_idx ON books (title, published_at);
    ```

    次のクエリでは、結合インデックスを引き続き使用できます。

    ```sql
    SELECT * FROM books WHERE title = 'database';
    ```

    ただし、次のクエリでは、インデックスの左端の最初の列の条件が指定されていないため、結合インデックスを使用できません。

    ```sql
    SELECT * FROM books WHERE published_at = '2018-08-18 21:42:08';
    ```

-   インデックス列をクエリの条件として使用する場合は、計算、関数、または型変換を使用しないでください。これにより、TiDB オプティマイザーがインデックスを使用できなくなります。

    時刻タイプの列`published_at`に新しいインデックスを作成するとします。

    ```sql
    CREATE INDEX published_at_idx ON books (published_at);
    ```

    ただし、次のクエリでは`published_at`のインデックスを使用できません。

    ```sql
    SELECT * FROM books WHERE YEAR(published_at)=2022;
    ```

    `published_at`でインデックスを使用するには、クエリを次のように書き換えることができます。これにより、インデックス列で関数を使用することがなくなります。

    ```sql
    SELECT * FROM books WHERE published_at >= '2022-01-01' AND published_at < '2023-01-01';
    ```

    式インデックスを使用して、クエリ条件内の`YEAR(Published at)`式インデックスを作成することもできます。

    ```sql
    CREATE INDEX published_year_idx ON books ((YEAR(published_at)));
    ```

    ここで、 `SELECT * FROM books WHERE YEAR(published_at)=2022;`クエリを実行すると、クエリは`published_year_idx`インデックスを使用して実行を高速化できます。

    > **警告：**
    >
    > 現在、式インデックスは実験的機能であり、TiDB 構成ファイルで有効にする必要があります。詳細については、 [式インデックス](/sql-statements/sql-statement-create-index.md#expression-index)を参照してください。

-   インデックス内の列にクエリ対象の列が含まれるカバリング インデックスを使用するようにし、すべての列を`SELECT *`ステートメントでクエリすることは避けてください。

    次のクエリでは、データを取得するためにインデックス`title_published_at_idx`をスキャンするだけで済みます。

    ```sql
    SELECT title, published_at FROM books WHERE title = 'database';
    ```

    次のクエリ ステートメントでは結合インデックス`(title, published_at)`を使用できますが、インデックスのない列をクエリするための追加コストが発生します。そのため、TiDB はインデックス データに格納されている参照 (通常は主キー情報) に従って行データをクエリする必要があります。

    ```sql
    SELECT * FROM books WHERE title = 'database';
    ```

-   クエリ条件に`!=`または`NOT IN`が含まれる場合、クエリではインデックスを使用できません。たとえば、次のクエリではインデックスを使用できません。

    ```sql
    SELECT * FROM books WHERE title != 'database';
    ```

-   クエリ内の`LIKE`条件がワイルドカード`%`で始まる場合、クエリではインデックスを使用できません。たとえば、次のクエリではインデックスを使用できません。

    ```sql
    SELECT * FROM books WHERE title LIKE '%database';
    ```

-   クエリ条件に複数のインデックスが使用可能で、実際にどのインデックスが最適であるかがわかっている場合は、 [オプティマイザーのヒント](/optimizer-hints.md)を使用して TiDB オプティマイザにこのインデックスの使用を強制することをお勧めします。これにより、不正確な統計やその他の問題により、TiDB オプティマイザーが間違ったインデックスを選択するのを防ぐことができます。

    次のクエリでは、インデックス`id_idx`と`title_idx`それぞれ列`id`と列`title`で使用できると仮定し、 `id_idx`の方が優れていることがわかっている場合は、SQL で`USE INDEX`ヒントを使用して、TiDB オプティマイザーに強制的に`id_idx`インデックスを使用させることができます。

    ```sql
    SELECT * FROM t USE INDEX(id_idx) WHERE id = 1 and title = 'database';
    ```

-   クエリ条件で`IN`式を使用する場合、その後に一致する値の数が 300 を超えないようにすることをお勧めします。そうしないと、実行効率が悪くなります。
