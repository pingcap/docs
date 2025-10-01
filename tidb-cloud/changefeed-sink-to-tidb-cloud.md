---
title: Sink to TiDB Cloud
summary: このドキュメントでは、TiDB Cloud Dedicated クラスターからTiDB Cloud Starter またはTiDB Cloud Essential クラスターにデータをストリーミングする方法について説明します。この機能には、利用可能な変更フィード数とリージョン数に制限があります。前提条件として、tidb_gc_life_time の拡張、データのバックアップ、 TiDB Cloudシンクの開始位置の取得が必要です。TiDB TiDB Cloudシンクを作成するには、クラスターの概要ページに移動し、接続を確立し、テーブルとイベントフィルターをカスタマイズし、レプリケーション開始位置を入力し、変更フィード仕様を指定し、構成を確認してシンクを作成します。最後に、tidb_gc_life_time を元の値に戻します。
---

# TiDB Cloudにシンク {#sink-to-tidb-cloud}

このドキュメントでは、 TiDB Cloud Dedicated クラスターからTiDB Cloud Starter またはTiDB Cloud Essential クラスターにデータをストリーミングする方法について説明します。

> **注記：**
>
> Changefeed 機能を使用するには、 TiDB Cloud Dedicated クラスターのバージョンが v6.1.3 以降であることを確認してください。

## 制限 {#restrictions}

-   TiDB Cloudクラスターごとに、最大 100 個の変更フィードを作成できます。

-   TiDB Cloud は、変更フィードを確立するために TiCDC を使用するため、同じ[TiCDCとしての制限](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios)持ちます。

-   レプリケートするテーブルに主キーまたは NULL 以外の一意のインデックスがない場合、レプリケーション中に一意の制約がないと、再試行シナリオによっては下流に重複したデータが挿入される可能性があります。

-   **Sink to TiDB Cloud**機能は、次の AWS リージョンにあり、2022 年 11 月 9 日以降に作成されたTiDB Cloud Dedicated クラスターでのみ使用できます。

    -   AWS オレゴン (us-west-2)
    -   AWS フランクフルト (eu-central-1)
    -   AWS シンガポール (ap-southeast-1)
    -   AWS 東京 (ap-northeast-1)

-   ソースTiDB Cloud Dedicated クラスターと宛先TiDB Cloud Starter またはTiDB Cloud Essential クラスターは、同じプロジェクトと同じリージョンに存在する必要があります。

-   **TiDB Cloudへのシンク**機能は、プライベートエンドポイント経由のネットワーク接続のみをサポートします。TiDB TiDB Cloud DedicatedクラスターからTiDB Cloud StarterまたはTiDB Cloud Essentialクラスターにデータをストリーミングするための変更フィードを作成すると、 TiDB Cloudは2つのクラスター間のプライベートエンドポイント接続を自動的に確立します。

## 前提条件 {#prerequisites}

**Sink to TiDB Cloud**コネクタは、一定の[TSO](https://docs.pingcap.com/tidb/stable/glossary#tso)経過した後にのみ、 TiDB Cloud Dedicated クラスターからTiDB Cloud Starter またはTiDB Cloud Essential クラスターに増分データをシンクできます。

変更フィードを作成する前に、ソースのTiDB Cloud Dedicated クラスターから既存のデータをエクスポートし、そのデータを宛先のTiDB Cloud Starter またはTiDB Cloud Essential クラスターにロードする必要があります。

1.  その間、履歴データが TiDB によってガベージ コレクションされないように、 [tidb_gc_life_time](https://docs.pingcap.com/tidb/stable/system-variables#tidb_gc_life_time-new-in-v50)次の 2 つの操作の合計時間よりも長く延長します。

    -   既存のデータをエクスポートおよびインポートする時間
    -   **Sink to TiDB Cloud**を作成する時間

    例えば：

    ```sql
    SET GLOBAL tidb_gc_life_time = '720h';
    ```

2.  [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)使用してTiDB Cloud Dedicated クラスターからデータをエクスポートし、 [インポート機能](/tidb-cloud/import-csv-files-serverless.md)使用して宛先のTiDB Cloud Starter またはTiDB Cloud Essential クラスターにデータをロードします。

3.  [Dumplingのエクスポートファイル](https://docs.pingcap.com/tidb/stable/dumpling-overview#format-of-exported-files)から、メタデータ ファイルからTiDB Cloudシンクの開始位置を取得します。

    以下はメタデータファイルの例の一部です。3 `SHOW MASTER STATUS`のうち`Pos`は既存データのTSOであり、 TiDB Cloudシンクの開始位置でもあります。

        Started dump at: 2023-03-28 10:40:19
        SHOW MASTER STATUS:
                Log: tidb-binlog
                Pos: 420747102018863124
        Finished dump at: 2023-03-28 10:40:20

## TiDB Cloudシンクを作成する {#create-a-tidb-cloud-sink}

前提条件を完了したら、データを宛先のTiDB Cloud Starter またはTiDB Cloud Essential クラスターにシンクできます。

1.  ターゲット TiDB クラスターのクラスター概要ページに移動し、左側のナビゲーション ペインで**[データ]** &gt; **[Changefeed] を**クリックします。

2.  **「Changefeed の作成」**をクリックし、宛先として**TiDB Cloud**を選択します。

3.  **TiDB Cloud接続**領域で、宛先のTiDB Cloud Starter またはTiDB Cloud Essential クラスターを選択し、宛先クラスターのユーザー名とパスワードを入力します。

4.  **[次へ]**をクリックして、2 つの TiDB クラスター間の接続を確立し、変更フィードが正常に接続できるかどうかをテストします。

    -   はいの場合は、構成の次の手順に進みます。
    -   そうでない場合は接続エラーが表示されるので、エラーに対処する必要があります。エラーが解決したら、もう一度**「次へ」**をクリックしてください。

5.  **テーブルフィルター**をカスタマイズして、複製するテーブルをフィルタリングします。ルールの構文については、 [テーブルフィルタルール](/table-filter.md)を参照してください。

    -   **大文字と小文字を区別**: フィルタールール内のデータベース名とテーブル名のマッチングで大文字と小文字を区別するかどうかを設定できます。デフォルトでは、大文字と小文字は区別されません。
    -   **フィルタールール**: この列でフィルタールールを設定できます。デフォルトでは、すべてのテーブルを複製するルール`*.*`が設定されています。新しいルールを追加すると、 TiDB CloudはTiDB内のすべてのテーブルをクエリし、ルールに一致するテーブルのみを右側のボックスに表示されます。フィルタールールは最大100件まで追加できます。
    -   **有効なキーを持つテーブル**: この列には、主キーや一意のインデックスなどの有効なキーを持つテーブルが表示されます。
    -   **有効なキーのないテーブル**: この列には、主キーまたは一意キーを持たないテーブルが表示されます。これらのテーブルは、一意の識別子がないと、下流で重複イベントを処理する際にデータの不整合が発生する可能性があるため、レプリケーション中に問題が発生します。データの整合性を確保するには、レプリケーションを開始する前に、これらのテーブルに一意のキーまたは主キーを追加することをお勧めします。または、これらのテーブルを除外するフィルタールールを追加することもできます。例えば、ルール`"!test.tbl1"`を使用してテーブル`test.tbl1`を除外できます。

6.  **イベント フィルター**をカスタマイズして、複製するイベントをフィルターします。

    -   **一致するテーブル**: この列では、イベントフィルターを適用するテーブルを設定できます。ルールの構文は、前述の**「テーブルフィルター」**領域で使用した構文と同じです。変更フィードごとに最大10個のイベントフィルタールールを追加できます。
    -   **イベント フィルター**: 次のイベント フィルターを使用して、変更フィードから特定のイベントを除外できます。
        -   **イベントを無視**: 指定されたイベント タイプを除外します。
        -   **SQLを無視**: 指定した式に一致するDDLイベントを除外します。例えば、 `^drop`指定すると`DROP`で始まる文が除外され、 `add column`指定すると`ADD COLUMN`含む文が除外されます。
        -   **挿入値式を無視**: 特定の条件を満たす`INSERT`文を除外します。例えば、 `id >= 100`指定すると、 `id`が100以上の`INSERT`文が除外されます。
        -   **新しい値の更新式を無視**: 新しい値が指定条件に一致する`UPDATE`文を除外します。例えば、 `gender = 'male'`指定すると、 `gender`が`male`になる更新は除外されます。
        -   **更新前の値を無視**: 指定した条件に一致する古い値を持つステートメントを`UPDATE`除外します。例えば、 `age < 18`指定すると、古い値`age`が18未満となる更新は除外されます。
        -   **削除値式を無視**: 指定された条件を満たす`DELETE`文を除外します。例えば、 `name = 'john'`指定すると、 `name`が`'john'`なる`DELETE`文が除外されます。

7.  **「レプリケーション開始位置」**領域に、 Dumplingからエクスポートされたメタデータ ファイルから取得した TSO を入力します。

8.  **次へ**をクリックして、変更フィード仕様を構成します。

    -   **「Changefeed 仕様」**領域で、Changefeed で使用されるレプリケーション容量単位 (RCU) の数を指定します。
    -   **「Changefeed 名」**領域で、Changefeed の名前を指定します。

9.  **「次へ」**をクリックして、変更フィード構成を確認します。

    すべての構成が正しいことを確認したら、リージョン間レプリケーションのコンプライアンスをチェックし、 **「作成」**をクリックします。

    設定を変更する場合は、 **「前へ」**をクリックして前の設定ページに戻ります。

10. シンクはすぐに起動し、シンクのステータスが**「作成中」**から**「実行中」**に変わることがわかります。

    変更フィード名をクリックすると、チェックポイント、レプリケーションのレイテンシー、その他のメトリックなど、変更フィードに関する詳細が表示されます。

11. シンクが作成された後、 [tidb_gc_life_time](https://docs.pingcap.com/tidb/stable/system-variables#tidb_gc_life_time-new-in-v50)元の値（デフォルト値は`10m` ）に戻します。

    ```sql
    SET GLOBAL tidb_gc_life_time = '10m';
    ```
