---
title: Table Attributes
summary: TiDB のテーブル属性機能の使用方法を学習します。
---

# テーブル属性 {#table-attributes}

テーブル属性機能はTiDB v5.3.0で導入されました。この機能を使用すると、テーブルまたはパーティションに特定の属性を追加し、その属性に対応する操作を実行できます。例えば、テーブル属性を使用してリージョンのマージ動作を制御できます。

<CustomContent platform="tidb">

現在、TiDBは、リージョンマージの動作を制御するために、テーブルまたはパーティションに属性`merge_option`を追加することのみをサポートしています。属性`merge_option`は、ホットスポットの処理方法の一部にすぎません。詳細については、 [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

現在、TiDBは、リージョンマージの動作を制御するために、テーブルまたはパーティションに属性`merge_option`追加することのみをサポートしています。属性`merge_option`は、ホットスポットに対処する方法の一部にすぎません。

</CustomContent>

> **注記：**
>
> TiCDC を使用してレプリケーションを実行したり、 BRを使用して増分バックアップを実行したりする場合、レプリケーションまたはバックアップ操作ではテーブル属性を設定する DDL 文がスキップされます。ダウンストリームまたはバックアップクラスターでテーブル属性を使用するには、ダウンストリームまたはバックアップクラスターで DDL 文を手動で実行する必要があります。

## 使用法 {#usage}

テーブル属性は`key=value`の形式です。複数の属性はカンマで区切られます。以下の例では、 `t`変更するテーブル名、 `p`変更するパーティション名です。 `[]`の項目はオプションです。

-   テーブルまたはパーティションの属性を設定します。

    ```sql
    ALTER TABLE t [PARTITION p] ATTRIBUTES [=] 'key=value[, key1=value1...]';
    ```

-   テーブルまたはパーティションの属性をリセットします。

    ```sql
    ALTER TABLE t [PARTITION p] ATTRIBUTES [=] DEFAULT;
    ```

-   すべてのテーブルとパーティションの属性を表示します。

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

テーブルに設定された属性は、そのテーブルのすべてのパーティションに適用されます。ただし、例外が1つあります。テーブルとパーティションに同じ属性が設定されていて、属性値が異なる場合、パーティション属性がテーブル属性をオーバーライドします。例えば、テーブル`t`に属性`key=value`が設定され、パーティション`p`に属性`key=value1`が設定されているとします。

```sql
ALTER TABLE t ATTRIBUTES[=]'key=value';
ALTER TABLE t PARTITION p ATTRIBUTES[=]'key=value1';
```

この場合、 `key=value1` `p1`パーティションに実際に影響する属性です。

## テーブル属性を使用してリージョン結合の動作を制御する {#control-the-region-merge-behavior-using-table-attributes}

### ユーザーシナリオ {#user-scenarios}

書き込みホットスポットまたは読み取りホットスポットがある場合、テーブル属性を使用してリージョンのマージ動作を制御できます。まずテーブルまたはパーティションに`merge_option`属性を追加し、次にその値を`deny`に設定します。次の2つのシナリオがあります。

#### 新しく作成されたテーブルまたはパーティションへの書き込みホットスポット {#write-hotspot-on-a-newly-created-table-or-partition}

新しく作成されたテーブルまたはパーティションへのデータ書き込み時にホットスポットの問題が発生した場合、通常はリージョンを分割して分散させる必要があります。しかし、分割/分散操作と書き込みの間に一定の時間間隔がある場合、これらの操作では書き込みホットスポットを完全に回避することはできません。これは、テーブルまたはパーティションの作成時に実行される分割操作によって空のリージョンが生成されるため、時間間隔が存在すると分割されたリージョンが結合される可能性があるためです。このようなケースに対処するには、テーブルまたはパーティションに`merge_option`属性を追加し、その属性値を`deny`に設定します。

#### 読み取り専用シナリオでの定期的な読み取りホットスポット {#periodic-read-hotspot-in-read-only-scenarios}

読み取り専用シナリオにおいて、テーブルまたはパーティションで発生する定期的な読み取りホットスポットを軽減するために、手動で分割したリージョンを、ホットスポットの問題が解決された後にマージしたくないとします。この場合、テーブルまたはパーティションに`merge_option`属性を追加し、その値を`deny`に設定します。

### 使用法 {#usage}

-   テーブルの領域が結合されないようにします。

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

-   パーティションの領域が結合されるのを防ぎます。

    ```sql
    ALTER TABLE t PARTITION p ATTRIBUTES 'merge_option=deny';
    ```

-   パーティションに属する領域の結合を許可します。

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

上記の2つの属性を同時に設定すると、パーティション`p`に属するリージョンを実際にマージできます。パーティションの属性がリセットされると、パーティション`p`テーブル`t`の属性を継承し、リージョンをマージできなくなります。

<CustomContent platform="tidb">

> **注記：**
>
> -   パーティションを持つテーブルの場合、 `merge_option`属性がテーブルレベルでのみ設定されている場合、 `merge_option=allow`であっても、テーブルはデフォルトで実際のパーティション数に応じて複数のリージョンに分割されます。すべてのリージョンをマージするには、 [テーブルの属性をリセットする](#usage)実行する必要があります。
> -   `merge_option`属性を使用する場合は、PD設定パラメータ[`split-merge-interval`](/pd-configuration-file.md#split-merge-interval)に注意する必要があります。5 属性`merge_option`設定されていない場合、リージョンが条件を満たしている場合、 `split-merge-interval`で指定された間隔後にリージョンをマージできます`merge_option`属性が設定されている場合、PDは`merge_option`設定に基づいて、指定された間隔後にリージョンをマージするかどうかを決定します。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> -   パーティションを持つテーブルの場合、 `merge_option`属性がテーブルレベルでのみ設定されている場合、 `merge_option=allow`であっても、テーブルはデフォルトで実際のパーティション数に応じて複数のリージョンに分割されます。すべてのリージョンをマージするには、 [テーブルの属性をリセットする](#usage)実行する必要があります。
> -   `merge_option`の属性が設定されていない場合、リージョンが条件を満たしていれば、1時間後にリージョンを統合できます。3 `merge_option`属性が設定されている場合、PDは`merge_option`設定に基づいて、1時間後にリージョンを統合するかどうかを決定します。

</CustomContent>
