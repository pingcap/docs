---
title: Table Attributes
summary: Learn how to use the table attribute feature of TiDB.
---

# テーブル属性 {#table-attributes}

テーブル属性機能は、TiDB v5.3.0 で導入されました。この機能を使用すると、テーブルまたはパーティションに特定の属性を追加して、属性に対応する操作を実行できます。たとえば、テーブル属性を使用して、リージョンのマージ動作を制御できます。

<CustomContent platform="tidb">

現在、TiDB は、リージョンのマージ動作を制御するためにテーブルまたはパーティションに`merge_option`属性を追加することのみをサポートしています。 `merge_option`属性は、ホットスポットを処理する方法の一部にすぎません。詳細については、 [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

現在、TiDB は、リージョンのマージ動作を制御するためにテーブルまたはパーティションに`merge_option`属性を追加することのみをサポートしています。 `merge_option`属性は、ホットスポットを処理する方法の一部にすぎません。

</CustomContent>

> **ノート：**
>
> -   TiDB Binlogまたは TiCDC を使用してレプリケーションを実行するか、 BRを使用して増分バックアップを実行する場合、レプリケーションまたはバックアップ操作は、テーブル属性を設定する DDL ステートメントをスキップします。ダウンストリームまたはバックアップ クラスターでテーブル属性を使用するには、ダウンストリームまたはバックアップ クラスターで DDL ステートメントを手動で実行する必要があります。

## 使用法 {#usage}

テーブル属性は`key=value`の形式です。複数の属性はコンマで区切ります。次の例では、 `t`は変更するテーブルの名前、 `p`は変更するパーティションの名前です。 `[]`の項目はオプションです。

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

-   テーブルまたはパーティションに構成された属性を表示します。

    ```sql
    SELECT * FROM information_schema.attributes WHERE id='schema/t[/p]';
    ```

-   特定の属性を持つすべてのテーブルとパーティションを表示します。

    ```sql
    SELECT * FROM information_schema.attributes WHERE attributes LIKE '%key%';
    ```

## 属性オーバーライド規則 {#attribute-override-rules}

テーブルに設定された属性は、テーブルのすべてのパーティションで有効になります。ただし、例外が 1 つあります。テーブルとパーティションが同じ属性で異なる属性値で構成されている場合、パーティション属性がテーブル属性をオーバーライドします。たとえば、テーブル`t`が`key=value`属性で構成され、パーティション`p`が`key=value1`で構成されているとします。

```sql
ALTER TABLE t ATTRIBUTES[=]'key=value';
ALTER TABLE t PARTITION p ATTRIBUTES[=]'key=value1';
```

この場合、 `key=value1`は`p1`パーティションで実際に有効になる属性です。

## テーブル属性を使用してリージョン結合動作を制御する {#control-the-region-merge-behavior-using-table-attributes}

### ユーザー シナリオ {#user-scenarios}

書き込みホットスポットまたは読み取りホットスポットがある場合は、テーブル属性を使用してリージョンのマージ動作を制御できます。最初に`merge_option`属性をテーブルまたはパーティションに追加してから、その値を`deny`に設定できます。 2 つのシナリオは次のとおりです。

#### 新しく作成されたテーブルまたはパーティションにホットスポットを書き込む {#write-hotspot-on-a-newly-created-table-or-partition}

データが新しく作成されたテーブルまたはパーティションに書き込まれるときにホットスポットの問題が発生した場合は、通常、リージョンを分割して分散させる必要があります。ただし、分割/分散操作と書き込みの間に一定の時間間隔がある場合、これらの操作は書き込みホットスポットを真に回避するわけではありません。これは、テーブルまたはパーティションの作成時に実行される分割操作によって空のリージョンが生成されるためです。そのため、時間間隔が存在する場合、分割されたリージョンがマージされる可能性があります。このケースを処理するには、テーブルまたはパーティションに`merge_option`属性を追加し、属性値を`deny`に設定します。

#### 読み取り専用シナリオでの定期的な読み取りホットスポット {#periodic-read-hotspot-in-read-only-scenarios}

読み取り専用のシナリオで、リージョンを手動で分割することによってテーブルまたはパーティションで発生する定期的な読み取りホットスポットを削減しようとしており、ホットスポットの問題が解決された後に手動で分割されたリージョンをマージしたくないとします。この場合、テーブルまたはパーティションに`merge_option`属性を追加し、その値を`deny`に設定できます。

### 使用法 {#usage}

-   テーブルのリージョンがマージされないようにします。

    ```sql
    ALTER TABLE t ATTRIBUTES 'merge_option=deny';
    ```

-   テーブルに属するリージョンのマージを許可:

    ```sql
    ALTER TABLE t ATTRIBUTES 'merge_option=allow';
    ```

-   テーブルの属性をリセットします。

    ```sql
    ALTER TABLE t ATTRIBUTES DEFAULT;
    ```

-   パーティションのリージョンがマージされないようにします。

    ```sql
    ALTER TABLE t PARTITION p ATTRIBUTES 'merge_option=deny';
    ```

-   パーティションに属するリージョンのマージを許可:

    ```sql
    ALTER TABLE t PARTITION p ATTRIBUTES 'merge_option=allow';
    ```

-   `merge_option`属性が設定されたすべてのテーブルまたはパーティションを表示:

    ```sql
    SELECT * FROM information_schema.attributes WHERE attributes LIKE '%merge_option%';
    ```

### 属性オーバーライド規則 {#attribute-override-rules}

```sql
ALTER TABLE t ATTRIBUTES 'merge_option=deny';
ALTER TABLE t PARTITION p ATTRIBUTES 'merge_option=allow';
```

上記の 2 つの属性を同時に設定すると、パーティション`p`に属するリージョンを実際にマージできます。パーティションの属性がリセットされると、パーティション`p`はテーブル`t`から属性を継承し、リージョンはマージできなくなります。

<CustomContent platform="tidb">

> **ノート：**
>
> -   パーティションを持つテーブルの場合、 `merge_option`属性がテーブル レベルでのみ構成されている場合、 `merge_option=allow`であっても、テーブルはデフォルトで実際のパーティション数に従って複数のリージョンに分割されます。すべてのリージョンをマージするには、 [テーブルの属性をリセットします](#usage)必要があります。
> -   `merge_option`属性を使用する場合は、PD 構成パラメーター[`split-merge-interval`](/pd-configuration-file.md#split-merge-interval)に注意する必要があります。 `merge_option`属性が構成されていないとします。この場合、リージョンが条件を満たしていれば、 `split-merge-interval`で指定された間隔の後にリージョンをマージできます。 `merge_option`属性が構成されている場合、PD は、 `merge_option`構成に従って、指定された間隔の後にリージョンをマージするかどうかを決定します。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> -   パーティションを持つテーブルの場合、 `merge_option`属性がテーブル レベルでのみ構成されている場合、 `merge_option=allow`であっても、テーブルはデフォルトで実際のパーティション数に従って複数のリージョンに分割されます。すべてのリージョンをマージするには、 [テーブルの属性をリセットします](#usage)必要があります。
> -   `merge_option`属性が構成されていないとします。この場合、リージョンが条件を満たしていれば、1 時間後にリージョンをマージできます。 `merge_option`属性が設定されている場合、PD は`merge_option`設定に従って 1 時間後にリージョンをマージするかどうかを決定します。

</CustomContent>
