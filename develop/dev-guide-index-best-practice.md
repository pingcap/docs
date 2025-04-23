---
title: Best Practices for Indexing
summary: TiDB でインデックスを作成および使用するためのベスト プラクティスをいくつか学習します。
---

<!-- markdownlint-disable MD029 -->

# インデックス作成のベストプラクティス {#best-practices-for-indexing}

このドキュメントでは、TiDB でインデックスを作成および使用するためのベスト プラクティスをいくつか紹介します。

## 始める前に {#before-you-begin}

このセクションでは、 [書店](/develop/dev-guide-bookshop-schema-design.md)データベースの`books`テーブルを例として取り上げます。

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

-   複数の列を含む結合インデックスを作成します。これは[カバーインデックスの最適化](/explain-indexes.md#indexreader)呼ばれる最適化です。**カバーインデックス最適化**により、TiDB はインデックス上で直接データをクエリできるようになり、パフォーマンスが向上します。

-   頻繁にクエリを実行しない列には、セカンダリインデックスを作成しないでください。セカンダリインデックスはクエリの速度向上に役立ちますが、副作用もあることに注意してください。インデックスを追加するたびに、行を挿入する際にキーと値が1つずつ追加されます。インデックスの数が増えるほど、書き込み速度が低下し、消費する領域も増加します。さらに、インデックスが多すぎるとオプティマイザーの実行時間に影響し、不適切なインデックスはオプティマイザーに誤動作をさせる可能性があります。そのため、インデックスの数が多いほど必ずしもパフォーマンスが向上するとは限りません。

-   アプリケーションに応じて適切なインデックスを作成してください。原則として、パフォーマンスを向上させるために、クエリで使用する列にのみインデックスを作成してください。以下のケースはインデックスの作成に適しています。

    -   識別度の高い列は、フィルタリングされる行数を大幅に削減できます。例えば、個人ID番号にはインデックスを作成し、性別にはインデックスを作成しないことをお勧めします。
    -   複数の条件でクエリを実行する場合は、複合インデックスを使用します。同じ条件を持つ列は、複合インデックスの先頭に配置する必要があることに注意してください。例えば、クエリ`select* from t where c1 = 10 and c2 = 100 and c3 > 10`頻繁に使用される場合は、複合インデックス`Index cidx (c1, c2, c3)`を作成することを検討してください。これにより、クエリ条件でスキャンするためのインデックスプレフィックスを構築できます。

-   セカンダリインデックスには意味のある名前を付けてください。会社または組織のテーブル命名規則に従うことをお勧めします。そのような命名規則がない場合は、 [インデックス命名仕様](/develop/dev-guide-object-naming-guidelines.md)のルールに従ってください。

## インデックスの使用に関するベストプラクティス {#best-practices-for-using-indexes}

-   インデックスはクエリを高速化するためのものなので、既存のインデックスが実際にいくつかのクエリで使用されていることを確認してください。どのクエリでも使用されていないインデックスは意味がないため、削除する必要があります。

-   結合インデックスを使用する場合は、左プレフィックスルールに従ってください。

    `title`と`published_at`列目に新しい結合インデックスを作成するとします。

    ```sql
    CREATE INDEX title_published_at_idx ON books (title, published_at);
    ```

    次のクエリでは、結合されたインデックスを引き続き使用できます。

    ```sql
    SELECT * FROM books WHERE title = 'database';
    ```

    ただし、次のクエリでは、インデックスの左端の最初の列の条件が指定されていないため、結合インデックスを使用できません。

    ```sql
    SELECT * FROM books WHERE published_at = '2018-08-18 21:42:08';
    ```

-   クエリの条件としてインデックス列を使用する場合は、計算、関数、または型変換を使用しないでください。そうしないと、TiDB オプティマイザーがインデックスを使用できなくなります。

    時間型の列`published_at`に新しいインデックスを作成するとします。

    ```sql
    CREATE INDEX published_at_idx ON books (published_at);
    ```

    ただし、次のクエリでは`published_at`のインデックスを使用できません。

    ```sql
    SELECT * FROM books WHERE YEAR(published_at)=2022;
    ```

    `published_at`のインデックスを使用するには、クエリを次のように書き換えます。これにより、インデックス列で関数を使用することがなくなります。

    ```sql
    SELECT * FROM books WHERE published_at >= '2022-01-01' AND published_at < '2023-01-01';
    ```

    式インデックスを使用して、クエリ条件で`YEAR(Published at)`式インデックスを作成することもできます。

    ```sql
    CREATE INDEX published_year_idx ON books ((YEAR(published_at)));
    ```

    ここで、 `SELECT * FROM books WHERE YEAR(published_at)=2022;`クエリを実行すると、クエリは`published_year_idx`インデックスを使用して実行を高速化できます。

    > **警告：**
    >
    > 現在、式インデックスは実験的機能であり、TiDB設定ファイルで有効化する必要があります。詳細については[表現インデックス](/sql-statements/sql-statement-create-index.md#expression-index)ご覧ください。

-   クエリ対象の列がインデックス内の列に含まれるカバーリング インデックスを使用するようにし、 `SELECT *`ステートメントですべての列をクエリすることは避けてください。

    次のクエリでは、データを取得するためにインデックス`title_published_at_idx`スキャンするだけで済みます。

    ```sql
    SELECT title, published_at FROM books WHERE title = 'database';
    ```

    次のクエリ ステートメントでは結合インデックス`(title, published_at)`を使用できますが、インデックスのない列をクエリするための追加コストが発生し、TiDB はインデックス データに格納されている参照 (通常は主キー情報) に従って行データをクエリする必要があります。

    ```sql
    SELECT * FROM books WHERE title = 'database';
    ```

-   クエリ条件に`!=`または`NOT IN`含まれる場合、クエリではインデックスを使用できません。例えば、次のクエリではインデックスを使用できません。

    ```sql
    SELECT * FROM books WHERE title != 'database';
    ```

-   クエリ内の条件`LIKE`がワイルドカード`%`で始まる場合、クエリではインデックスを使用できません。例えば、次のクエリではインデックスを使用できません。

    ```sql
    SELECT * FROM books WHERE title LIKE '%database';
    ```

-   クエリ条件に複数のインデックスがあり、実際にどのインデックスが最適かわかっている場合は、 [オプティマイザーヒント](/optimizer-hints.md)指定してTiDBオプティマイザにそのインデックスを強制的に使用させることをお勧めします。これにより、統計情報の不正確さやその他の問題により、TiDBオプティマイザが誤ったインデックスを選択するのを防ぐことができます。

    次のクエリでは、インデックス`id_idx`と`title_idx`それぞれ列`id`と`title`で使用可能であると仮定し、 `id_idx`方が適していることが分かっている場合は、SQL で`USE INDEX`ヒントを使用して、TiDB オプティマイザーに`id_idx`インデックスを使用するように強制できます。

    ```sql
    SELECT * FROM t USE INDEX(id_idx) WHERE id = 1 and title = 'database';
    ```

-   クエリ条件で`IN`式を使用する場合、その後に一致する値の数が 300 を超えないようにすることをお勧めします。そうしないと、実行効率が低下します。

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](/support.md)についてコミュニティに質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](https://tidb.support.pingcap.com/)についてコミュニティに質問してください。

</CustomContent>
