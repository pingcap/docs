---
title: Table Attributes
summary: Learn how to use the table attribute feature of TiDB.
---

# テーブルの属性 {#table-attributes}

テーブル属性機能は TiDB v5.3.0 で導入されました。この機能を使用すると、特定の属性をテーブルまたはパーティションに追加して、その属性に対応する操作を実行できます。たとえば、テーブル属性を使用してリージョンの結合動作を制御できます。

<CustomContent platform="tidb">

現在、TiDB は、リージョンのマージ動作を制御するためにテーブルまたはパーティションに`merge_option`属性を追加することのみをサポートしています。 `merge_option`属性は、ホットスポットへの対処方法の一部にすぎません。詳細については、 [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

現在、TiDB は、リージョンのマージ動作を制御するためにテーブルまたはパーティションに`merge_option`属性を追加することのみをサポートしています。 `merge_option`属性は、ホットスポットへの対処方法の一部にすぎません。

</CustomContent>

> **注記：**
>
> -   TiDB Binlogまたは TiCDC を使用してレプリケーションを実行するか、 BRを使用して増分バックアップを実行する場合、レプリケーションまたはバックアップ操作ではテーブル属性を設定する DDL ステートメントがスキップされます。ダウンストリームまたはバックアップ クラスターでテーブル属性を使用するには、ダウンストリームまたはバックアップ クラスターで DDL ステートメントを手動で実行する必要があります。

## 使用法 {#usage}

table 属性は`key=value`の形式です。複数の属性はカンマで区切られます。次の例では、 `t`は変更するテーブルの名前、 `p`は変更するパーティションの名前です。 `[]`の項目はオプションです。

-   テーブルまたはパーティションの属性を設定します。

    ```sql
    ALTER TABLE t [PARTITION p] ATTRIBUTES [=] 'key=value[, key1=value1...]';
    ```

-   テーブルまたはパーティションの属性をリセットします。

    ```sql
    ALTER TABLE t [PARTITION p] ATTRIBUTES [=] DEFAULT;
    ```

-   すべてのテーブルとパーティションの属性を確認します。

    ```sql
    SELECT * FROM information_schema.attributes;
    ```

-   テーブルまたはパーティションに設定された属性を確認します。

    ```sql
    SELECT * FROM information_schema.attributes WHERE id='schema/t[/p]';
    ```

-   特定の属性を持つすべてのテーブルとパーティションを表示します。

    ```sql
    SELECT * FROM information_schema.attributes WHERE attributes LIKE '%key%';
    ```

## 属性オーバーライドルール {#attribute-override-rules}

テーブルに設定された属性は、テーブルのすべてのパーティションに有効になります。ただし、例外が 1 つあります。テーブルとパーティションが同じ属性で異なる属性値で構成されている場合、パーティション属性がテーブル属性をオーバーライドします。たとえば、テーブル`t`が`key=value`属性で構成され、パーティション`p`が`key=value1`で構成されているとします。

```sql
ALTER TABLE t ATTRIBUTES[=]'key=value';
ALTER TABLE t PARTITION p ATTRIBUTES[=]'key=value1';
```

この場合、 `key=value1` `p1`パーティションで実際に有効となる属性です。

## テーブル属性を使用してリージョンのマージ動作を制御する {#control-the-region-merge-behavior-using-table-attributes}

### ユーザーシナリオ {#user-scenarios}

書き込みホットスポットまたは読み取りホットスポットがある場合は、テーブル属性を使用してリージョンのマージ動作を制御できます。まずテーブルまたはパーティションに`merge_option`属性を追加してから、その値を`deny`に設定します。 2 つのシナリオは次のとおりです。

#### 新しく作成されたテーブルまたはパーティション上の書き込みホットスポット {#write-hotspot-on-a-newly-created-table-or-partition}

新しく作成したテーブルまたはパーティションにデータを書き込むときにホットスポットの問題が発生した場合は、通常、リージョンを分割して分散する必要があります。ただし、分割/分散操作と書き込みの間に一定の時間間隔がある場合、これらの操作は書き込みホットスポットを完全に回避することはできません。これは、テーブルまたはパーティションの作成時に実行される分割操作によって空のリージョンが生成されるため、時間間隔が存在する場合、分割されたリージョンがマージされる可能性があるためです。このケースに対処するには、テーブルまたはパーティションに`merge_option`属性を追加し、属性値を`deny`に設定します。

#### 読み取り専用シナリオでの定期読み取りホットスポット {#periodic-read-hotspot-in-read-only-scenarios}

読み取り専用のシナリオで、リージョンを手動で分割することでテーブルまたはパーティションで発生する定期的な読み取りホットスポットを削減しようとし、ホットスポットの問題が解決された後に手動で分割したリージョンをマージしたくないとします。この場合、テーブルまたはパーティションに`merge_option`属性を追加し、その値を`deny`に設定できます。

### 使用法 {#usage}

-   テーブルのリージョンが結合しないようにします。

    ```sql
    ALTER TABLE t ATTRIBUTES 'merge_option=deny';
    ```

-   テーブルに属するリージョンの結合を許可します。

    ```sql
    ALTER TABLE t ATTRIBUTES 'merge_option=allow';
    ```

-   テーブルの属性をリセットします。

    ```sql
    ALTER TABLE t ATTRIBUTES DEFAULT;
    ```

-   パーティションのリージョンが結合しないようにします。

    ```sql
    ALTER TABLE t PARTITION p ATTRIBUTES 'merge_option=deny';
    ```

-   パーティションに属するリージョンの結合を許可します。

    ```sql
    ALTER TABLE t PARTITION p ATTRIBUTES 'merge_option=allow';
    ```

-   `merge_option`属性が構成されているすべてのテーブルまたはパーティションを表示します。

    ```sql
    SELECT * FROM information_schema.attributes WHERE attributes LIKE '%merge_option%';
    ```

### 属性オーバーライドルール {#attribute-override-rules}

```sql
ALTER TABLE t ATTRIBUTES 'merge_option=deny';
ALTER TABLE t PARTITION p ATTRIBUTES 'merge_option=allow';
```

上記 2 つの属性を同時に設定すると、実際にパーティション`p`に属するリージョンをマージできます。パーティションの属性がリセットされると、パーティション`p`はテーブル`t`の属性を継承し、リージョンをマージすることができなくなる。

<CustomContent platform="tidb">

> **注記：**
>
> -   パーティションのあるテーブルの場合、 `merge_option`属性がテーブル レベルでのみ構成されている場合、 `merge_option=allow`であっても、テーブルは実際のパーティション数に応じてデフォルトで複数のリージョンに分割されます。すべてのリージョンをマージするには、 [テーブルの属性をリセットする](#usage)を行う必要があります。
> -   `merge_option`属性を使用する場合は、PD 構成パラメータ[`split-merge-interval`](/pd-configuration-file.md#split-merge-interval)に注意する必要があります。 `merge_option`属性が設定されていないとします。この場合、リージョンが条件を満たしていれば、 `split-merge-interval`で指定された間隔の後にリージョンをマージできます。 `merge_option`属性が設定されている場合、PD は、 `merge_option`設定に従って、指定された間隔の後にリージョンをマージするかどうかを決定します。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> -   パーティションのあるテーブルの場合、 `merge_option`属性がテーブル レベルでのみ構成されている場合、 `merge_option=allow`であっても、テーブルは実際のパーティション数に応じてデフォルトで複数のリージョンに分割されます。すべてのリージョンをマージするには、 [テーブルの属性をリセットする](#usage)を行う必要があります。
> -   `merge_option`属性が設定されていないとします。この場合、リージョンが条件を満たしていれば、1 時間後にリージョンをマージできます。 `merge_option`属性が設定されている場合、PD は`merge_option`設定に従って 1 時間後にリージョンをマージするかどうかを決定します。

</CustomContent>
