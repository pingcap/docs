---
title: Sink to TiDB Cloud
Summary: Learn how to create a changefeed to stream data from a TiDB Cloud Dedicated Tier cluster to a TiDB Cloud Serverless Tier cluster.
---

# TiDB Cloudにシンク {#sink-to-tidb-cloud}

このドキュメントでは、 TiDB Cloud Dedicated TierクラスターからTiDB Cloud Serverless Tierクラスターにデータをストリーミングする方法について説明します。

> **ノート：**
>
> Changefeed 機能を使用するには、TiDB クラスターのバージョンが v6.4.0 以降であることを確認してください。

## 制限 {#restrictions}

-   TiDB Cloudクラスターごとに、最大 5 つの変更フィードを作成できます。

-   TiDB Cloud はTiCDC を使用して変更フィードを確立するため、同じ[TiCDCとしての制限](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios)を持ちます。

-   レプリケートするテーブルに主キーまたは null 以外の一意のインデックスがない場合、レプリケーション中に一意の制約がないため、一部の再試行シナリオで重複データがダウンストリームに挿入される可能性があります。

-   **Sink to TiDB Cloud**機能は、次の AWS リージョンにあり、2022 年 11 月 9 日以降に作成されたTiDB Cloud Dedicated Tierクラスターでのみ使用できます。

    -   AWS オレゴン (us-west-2)
    -   AWS フランクフルト (eu-central-1)
    -   AWS シンガポール (ap-southeast-1)
    -   AWS 東京 (ap-northeast-1)

-   ソースDedicated Tierクラスターと宛先Serverless Tierクラスターは、同じプロジェクトおよび同じリージョンにある必要があります。

-   **Sink to TiDB Cloud**機能は、プライベート エンドポイント経由のネットワーク接続のみをサポートします。 TiDB Cloud Dedicated TierクラスターからTiDB Cloud Serverless Tierクラスターにデータをストリーミングするための変更フィードを作成すると、 TiDB Cloud は2 つのクラスター間のプライベート エンドポイント接続を自動的にセットアップします。

## 前提条件 {#prerequisites}

**Sink to TiDB Cloud**コネクタは、TiDB Cloud Dedicated TierクラスターからServerless Tierクラスターに特定の[TSO](https://docs.pingcap.com/tidb/stable/glossary#tso)後にのみ増分データをシンクできます。

変更フィードを作成する前に、ソースのDedicated Tierクラスターから既存のデータをエクスポートし、そのデータを宛先のServerless Tierクラスターにロードする必要があります。

1.  次の 2 つの操作の合計時間よりも長くなるように[tidb_gc_life_time](https://docs.pingcap.com/tidb/stable/system-variables#tidb_gc_life_time-new-in-v50)拡張して、その間の履歴データが TiDB によってガベージ コレクションされないようにします。

    -   既存のデータをエクスポートおよびインポートする時間
    -   **Sink to TiDB Cloud**を作成する時が来ました

    例えば：

    ```sql
    SET GLOBAL tidb_gc_life_time = '720h';
    ```

2.  TiDB Cloud Dedicated Tierクラスターから[データのエクスポート](/tidb-cloud/export-data-from-tidb-cloud.md)をロードし、 [マイダンパー/マイローダー](https://centminmod.com/mydumper.html)などのコミュニティ ツールを使用して、宛先のServerless Tierクラスターにデータをロードします。

3.  [Dumplingのエクスポートファイル](/dumpling-overview.md#format-of-exported-files)から、メタデータ ファイルからTiDB Cloudシンクの開始位置を取得します。

    以下は、メタデータ ファイルの例の一部です。 `Pos` of `SHOW MASTER STATUS`は既存データの TSO であり、 TiDB Cloudシンクの開始位置でもあります。

    ```
    Started dump at: 2023-03-28 10:40:19
    SHOW MASTER STATUS:
            Log: tidb-binlog
            Pos: 420747102018863124
    Finished dump at: 2023-03-28 10:40:20
    ```

## TiDB Cloudシンクを作成する {#create-a-tidb-cloud-sink}

前提条件を完了したら、データを宛先のServerless Tierクラスターにシンクできます。

1.  ターゲット TiDB クラスターのクラスター概要ページに移動し、左側のナビゲーション ペインで**[Changefeed]**をクリックします。

2.  **Create Changefeed を**クリックし、送信先として<strong>TiDB Cloud</strong>を選択します。

3.  **[TiDB Cloud接続]**領域で、宛先のServerless Tierクラスターを選択し、宛先クラスターのユーザー名とパスワードを入力します。

4.  **[次へ]**をクリックして、2 つの TiDB クラスター間の接続を確立し、changefeed がそれらを正常に接続できるかどうかをテストします。

    -   はいの場合、構成の次のステップに進みます。
    -   そうでない場合は、接続エラーが表示され、エラーを処理する必要があります。エラーが解決したら、もう一度**[次へ]**をクリックします。

5.  **テーブル フィルタを**カスタマイズして、複製するテーブルをフィルタリングします。ルールの構文については、 [テーブル フィルター規則](/table-filter.md)を参照してください。

    -   **フィルター ルール**: この列でフィルター ルールを設定できます。デフォルトでは、すべてのテーブルをレプリケートすることを表すルール`*. *`があります。新しいルールを追加すると、 TiDB Cloud はTiDB 内のすべてのテーブルに対してクエリを実行し、右側のボックスのルールに一致するテーブルのみを表示します。
    -   **レプリケートされるテーブル**: この列は、レプリケートされるテーブルを示します。ただし、将来レプリケートされる新しいテーブルや、完全にレプリケートされるスキーマは表示されません。
    -   **有効なキーのないテーブル**: この列には、一意キーと主キーのないテーブルが表示されます。これらのテーブルでは、重複イベントを処理するためにダウンストリーム システムで一意の識別子を使用できないため、レプリケーション中にデータの一貫性が失われる可能性があります。このような問題を回避するには、レプリケーションの前にこれらのテーブルに一意のキーまたは主キーを追加するか、これらのテーブルを除外するフィルター ルールを設定することをお勧めします。たとえば、「!test.tbl1」を使用してテーブル`test.tbl1`を除外できます。

6.  **[レプリケーションの開始位置]**領域で、エクスポートされたDumplingメタデータ ファイルから取得した TSO を入力します。

7.  **[次へ]**をクリックして、changefeed 仕様を構成します。

    -   **[Changefeed 仕様]**領域で、changefeed が使用するレプリケーション キャパシティ ユニット (RCU) の数を指定します。
    -   **[変更フィード名]**領域で、変更フィードの名前を指定します。

8.  **[次へ]**をクリックして、Changefeed 構成を確認します。

    すべての構成が正しいことを確認したら、クロスリージョン レプリケーションのコンプライアンスを確認し、 **[作成]**をクリックします。

    一部の構成を変更する場合は、 **[前へ]**をクリックして前の構成ページに戻ります。

9.  シンクがすぐに開始され、シンクのステータスが**[作成中]**から<strong>[実行中]</strong>に変化したことがわかります。

    変更フィード名をクリックすると、チェックポイント、レプリケーションレイテンシー、その他のメトリックなど、変更フィードに関する詳細が表示されます。

10. シンクの作成後に[tidb_gc_life_time](https://docs.pingcap.com/tidb/stable/system-variables#tidb_gc_life_time-new-in-v50)元の値 (デフォルト値は`10m` ) に戻します。

    ```sql
    SET GLOBAL tidb_gc_life_time = '10m';
    ```
