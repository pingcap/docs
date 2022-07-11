---
title: Best Practices for Indexing
summary: Learn some best practices for creating and using indexes in TiDB.
---

<!-- markdownlint-disable MD029 -->

# インデックス作成のベストプラクティス {#best-practices-for-indexing}

このドキュメントでは、TiDBでインデックスを作成および使用するためのいくつかのベストプラクティスを紹介します。

## あなたが始める前に {#before-you-begin}

このセクションでは、例として[書店](/develop/dev-guide-bookshop-schema-design.md)データベースの`books`テーブルを取り上げます。

{{< copyable "" >}}

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

## インデックスを作成するためのベストプラクティス {#best-practices-for-creating-indexes}

-   [インデックスの最適化をカバー](/explain-indexes.md#indexreader)と呼ばれる最適化である、複数の列を持つ結合インデックスの作成。**インデックスの最適化をカバー**することで、TiDBはインデックスで直接データをクエリできるようになり、パフォーマンスの向上に役立ちます。

-   頻繁にクエリを実行しない列にセカンダリインデックスを作成することは避けてください。便利なセカンダリインデックスはクエリを高速化できますが、副作用もあることに注意してください。インデックスを追加するたびに、行を挿入するときに追加のKey-Valueが追加されます。インデックスが多いほど、書き込みが遅くなり、より多くのスペースが消費されます。さらに、インデックスが多すぎるとオプティマイザの実行時間に影響し、不適切なインデックスはオプティマイザを誤解させる可能性があります。したがって、インデックスが多いからといって、必ずしもパフォーマンスが向上するとは限りません。

-   アプリケーションに基づいて適切なインデックスを作成します。原則として、パフォーマンスを向上させるために、クエリで使用される列にのみインデックスを作成します。次の場合は、インデックスの作成に適しています。

    -   区別度の高い列は、フィルター処理された行の数を大幅に減らすことができます。たとえば、性別ではなく、個人ID番号にインデックスを作成することをお勧めします。
    -   複数の条件でクエリを実行する場合は、複合インデックスを使用します。同等の条件の列は、結合されたインデックスの前に配置する必要があることに注意してください。次に例を示します`select* from t where c1 = 10 and c2 = 100 and c3 > 10`クエリが頻繁に使用される場合は、結合インデックス`Index cidx (c1, c2, c3)`を作成することを検討してください。これにより、クエリ条件でスキャンするインデックスプレフィックスを作成できます。

-   セカンダリインデックスに意味のある名前を付けます。会社または組織のテーブルの命名規則に従うことをお勧めします。このような命名規則が存在しない場合は、 [インデックス命名仕様](/develop/dev-guide-object-naming-guidelines.md)の規則に従ってください。

## インデックスを使用するためのベストプラクティス {#best-practices-for-using-indexes}

-   インデックスはクエリを高速化するためのものであるため、既存のインデックスが実際に一部のクエリで使用されていることを確認してください。インデックスがどのクエリでも使用されていない場合、インデックスは無意味であるため、削除する必要があります。

-   複合インデックスを使用する場合は、左プレフィックス規則に従ってください。

    `title`列と`published_at`列に新しい複合インデックスを作成するとします。

    {{< copyable "" >}}

    ```sql
    CREATE INDEX title_published_at_idx ON books (title, published_at);
    ```

    次のクエリでも、結合されたインデックスを使用できます。

    {{< copyable "" >}}

    ```sql
    SELECT * FROM books WHERE title = 'database';
    ```

    ただし、インデックスの左端の最初の列の条件が指定されていないため、次のクエリでは結合インデックスを使用できません。

    {{< copyable "" >}}

    ```sql
    SELECT * FROM books WHERE published_at = '2018-08-18 21:42:08';
    ```

-   クエリの条件としてインデックス列を使用する場合は、計算、関数、または型変換を使用しないでください。TiDBオプティマイザがインデックスを使用できなくなります。

    時間タイプ列`published_at`に新しいインデックスを作成するとします。

    {{< copyable "" >}}

    ```sql
    CREATE INDEX published_at_idx ON books (published_at);
    ```

    ただし、次のクエリでは`published_at`のインデックスを使用できません。

    {{< copyable "" >}}

    ```sql
    SELECT * FROM books WHERE YEAR(published_at)=2022;
    ```

    `published_at`でインデックスを使用するには、次のようにクエリを書き直すことができます。これにより、インデックス列で関数を使用する必要がなくなります。

    {{< copyable "" >}}

    ```sql
    SELECT * FROM books WHERE published_at >= '2022-01-01' AND published_at < '2023-01-01';
    ```

    式インデックスを使用して、クエリ条件で`YEAR(Published at)`の式インデックスを作成することもできます。

    {{< copyable "" >}}

    ```sql
    CREATE INDEX published_year_idx ON books ((YEAR(published_at)));
    ```

    これで、 `SELECT * FROM books WHERE YEAR(published_at)=2022;`のクエリを実行すると、クエリは`published_year_idx`のインデックスを使用して実行を高速化できます。

    > **警告：**
    >
    > 現在、式インデックスは実験的機能であり、TiDB構成ファイルで有効にする必要があります。詳細については、 [式インデックス](/sql-statements/sql-statement-create-index.md#expression-index)を参照してください。

-   インデックス内の列にクエリ対象の列が含まれているカバーリングインデックスを使用し、 `SELECT *`のステートメントですべての列をクエリしないようにしてください。

    次のクエリは、データを取得するためにインデックス`title_published_at_idx`をスキャンするだけで済みます。

    {{< copyable "" >}}

    ```sql
    SELECT title, published_at FROM books WHERE title = 'database';
    ```

    次のクエリステートメントは結合インデックス`(title, published_at)`を使用できますが、インデックスなしの列をクエリするための追加コストが発生します。これにより、TiDBは、インデックスデータ（通常は主キー情報）に格納されている参照に従って行データをクエリする必要があります。

    {{< copyable "" >}}

    ```sql
    SELECT * FROM books WHERE title = 'database';
    ```

-   クエリ条件に`!=`または`NOT IN`が含まれている場合、クエリはインデックスを使用できません。たとえば、次のクエリはインデックスを使用できません。

    {{< copyable "" >}}

    ```sql
    SELECT * FROM books WHERE title != 'database';
    ```

-   `LIKE`条件がクエリのワイルドカード`%`で始まる場合、クエリはインデックスを使用できません。たとえば、次のクエリはインデックスを使用できません。

    {{< copyable "" >}}

    ```sql
    SELECT * FROM books WHERE title LIKE '%database';
    ```

-   クエリ条件に複数のインデックスが使用可能であり、どのインデックスが実際に最適であるかがわかっている場合は、 [オプティマイザーのヒント](/optimizer-hints.md)を使用してTiDBオプティマイザにこのインデックスを使用させることをお勧めします。これにより、不正確な統計やその他の問題が原因でTiDBオプティマイザが間違ったインデックスを選択するのを防ぐことができます。

    次のクエリでは、インデックス`id_idx`と`title_idx`がそれぞれ列`id`と`title`で使用可能であると仮定して、 `id_idx`の方が優れていることがわかっている場合は、SQLで`USE INDEX`ヒントを使用して、TiDBオプティマイザーに`id_idx`インデックスを使用させることができます。

    {{< copyable "" >}}

    ```sql
    SELECT * FROM t USE INDEX(id_idx) WHERE id = 1 and title = 'database';
    ```

-   クエリ条件で`IN`式を使用する場合は、一致する値の数が300を超えないようにすることをお勧めします。そうしないと、実行効率が低下します。
