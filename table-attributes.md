---
title: Table Attributes
summary: TiDB のテーブル属性機能の使用方法を学習します。
---

# テーブル属性 {#table-attributes}

テーブル属性機能は、TiDB v5.3.0 で導入されました。この機能を使用すると、テーブルまたはパーティションに特定の属性を追加して、その属性に対応する操作を実行できます。たとえば、テーブル属性を使用してリージョンのマージ動作を制御できます。

<CustomContent platform="tidb">

現在、TiDB は、リージョンのマージ動作を制御するために、テーブルまたはパーティションに`merge_option`属性を追加することのみをサポートしています。 `merge_option`属性は、ホットスポットを処理する方法の一部にすぎません。詳細については、 [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

現在、TiDB は、リージョンのマージ動作を制御するために`merge_option`テーブルまたはパーティションに`merge_option`属性を追加することのみをサポートしています。3 属性は、ホットスポットを処理する方法の一部にすぎません。

</CustomContent>

> **注記：**
>
> TiCDC を使用してレプリケーションを実行する場合、またはBR を使用して増分バックアップを実行する場合、レプリケーションまたはバックアップ操作では、テーブル属性を設定する DDL ステートメントがスキップされます。ダウンストリームまたはバックアップ クラスターでテーブル属性を使用するには、ダウンストリームまたはバックアップ クラスターで DDL ステートメントを手動で実行する必要があります。

## 使用法 {#usage}

テーブル属性は`key=value`の形式です。複数の属性はカンマで区切られます。次の例では、 `t`変更するテーブルの名前、 `p`変更するパーティションの名前です。 `[]`の項目はオプションです。

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

テーブルに設定された属性は、テーブルのすべてのパーティションに反映されます。ただし、例外が 1 つあります。テーブルとパーティションが同じ属性で、属性値が異なるように設定されている場合は、パーティション属性がテーブル属性よりも優先されます。たとえば、テーブル`t`が`key=value`属性で構成され、パーティション`p`が`key=value1`属性で構成されているとします。

```sql
ALTER TABLE t ATTRIBUTES[=]'key=value';
ALTER TABLE t PARTITION p ATTRIBUTES[=]'key=value1';
```

この場合、 `key=value1` `p1`パーティションに実際に適用される属性です。

## テーブル属性を使用してリージョンの結合動作を制御する {#control-the-region-merge-behavior-using-table-attributes}

### ユーザーシナリオ {#user-scenarios}

書き込みホットスポットまたは読み取りホットスポットがある場合は、テーブル属性を使用してリージョンのマージ動作を制御できます。最初にテーブルまたはパーティションに`merge_option`属性を追加し、その値を`deny`に設定します。次の 2 つのシナリオがあります。

#### 新しく作成されたテーブルまたはパーティションにホットスポットを書き込む {#write-hotspot-on-a-newly-created-table-or-partition}

新しく作成されたテーブルまたはパーティションにデータが書き込まれるときにホットスポットの問題が発生する場合は、通常、リージョンを分割して分散する必要があります。ただし、分割/分散操作と書き込みの間に一定の時間間隔がある場合、これらの操作では書き込みホットスポットが実際に回避されるわけではありません。これは、テーブルまたはパーティションの作成時に実行される分割操作によって空のリージョンが生成されるため、時間間隔が存在すると、分割されたリージョンが結合される可能性があるためです。このケースを処理するには、テーブルまたはパーティションに`merge_option`属性を追加し、属性値を`deny`に設定します。

#### 読み取り専用シナリオでの定期的な読み取りホットスポット {#periodic-read-hotspot-in-read-only-scenarios}

読み取り専用シナリオで、手動で領域を分割してテーブルまたはパーティションで発生する定期的な読み取りホットスポットを削減しようとし、ホットスポットの問題が解決された後に手動で分割した領域をマージしたくないとします。この場合、テーブルまたはパーティションに`merge_option`属性を追加し、その値を`deny`に設定できます。

### 使用法 {#usage}

-   テーブルの領域が結合されないようにする:

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

-   パーティションの領域が結合されるのを防ぎます:

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

上記 2 つの属性を同時に設定すると、パーティション`p`に属するリージョンを実際にマージできます。パーティションの属性がリセットされると、パーティション`p`はテーブル`t`から属性を継承し、リージョンをマージできなくなります。

<CustomContent platform="tidb">

> **注記：**
>
> -   パーティションを持つテーブルの場合、 `merge_option`属性がテーブル レベルのみで構成されている場合は、 `merge_option=allow`であっても、実際のパーティション数に応じてテーブルはデフォルトで複数のリージョンに分割されます。すべてのリージョンをマージするには、 [テーブルの属性をリセットする](#usage)が必要です。
> -   `merge_option`属性を使用する場合は、PD 構成パラメータ[`split-merge-interval`](/pd-configuration-file.md#split-merge-interval)に注意する必要があります。 `merge_option`属性が設定されていないと仮定します。この場合、リージョンが条件を満たしている場合、 `split-merge-interval`で指定された間隔後にリージョンをマージできます。 `merge_option`属性が設定されている場合、PD は`merge_option`構成に従って、指定された間隔後にリージョンをマージするかどうかを決定します。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> -   パーティションを持つテーブルの場合、 `merge_option`属性がテーブル レベルのみで構成されている場合は、 `merge_option=allow`であっても、実際のパーティション数に応じてテーブルはデフォルトで複数のリージョンに分割されます。すべてのリージョンをマージするには、 [テーブルの属性をリセットする](#usage)が必要です。
> -   `merge_option`属性が設定されていないとします。この場合、リージョンが条件を満たしていれば、1 時間後にリージョンをマージできます。3 属性が設定`merge_option` `merge_option`に従って 1 時間後にリージョンをマージするかどうかを決定します。

</CustomContent>
