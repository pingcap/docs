---
title: TiDB Dashboard Top SQL page
summary: Top SQLを使用して、CPU、ネットワーク、および論理I/Oリソースを最も多く消費するクエリを特定します。
---

# TiDBダッシュボードのTop SQLページ {#tidb-dashboard-top-sql-page}

TiDBダッシュボードの「Top SQL」ページでは、指定したTiDBまたはTiKVノード上で、一定期間にわたって最もリソースを消費したSQLクエリを表示および分析できます。

-   Top SQLを有効にすると、この機能は既存のTiDBおよびTiKVノードからCPUワークロードデータを継続的に収集し、最大30日間データを保持します。
-   バージョン 8.5.6 以降では、Top SQL設定で**TiKV ネットワーク IO 収集 (多次元) を**有効にして、指定した TiKV ノードの`Network Bytes`や`Logical IO Bytes`などのメトリックをさらに表示し、 `By Query` 、 `By Table` 、 `By DB` -E}} 、および`By Region` 。

Top SQLは以下の機能を提供します。

-   現在の時間範囲で最もリソースを消費している上位`5` 、 `20` 、または`100` SQL クエリをグラフと表で視覚化し、残りのレコードは`Others`として自動的に集計されます。
-   リソース消費のホットスポットをCPU時間またはネットワークバイト数でソートして表示します。TiKVノードを選択する際には、論理I/Oバイト数でソートすることもできます。
-   クエリごとにSQLと実行プランの詳細を表示します。TiKVノードを選択すると、 `By Table` 、 `By DB` 、および`By Region`のディメンションで分析を集計することもできます。
-   グラフで選択した期間を拡大表示したり、データを手動で更新したり、自動更新を有効にしたり、テーブルデータをCSVファイルにエクスポートしたりできます。
-   実行されたすべてのSQL文（現在実行中のものも含む）を収集します。
-   特定のTiDBまたはTiKVノードのデータを表示します。

## 推奨シナリオ {#recommended-scenarios}

Top SQLは、パフォーマンスの問題を分析するのに適しています。以下に、 Top SQLの典型的なシナリオをいくつか示します。

-   クラスタ内の特定のTiDBまたはTiKVノードのCPU使用率が非常に高いことが判明しました。どのタイプのSQLが大量のCPUリソースを消費しているかを迅速に特定したいと考えています。
-   クラスタ全体のクエリ処理が遅くなる。現在どのSQLクエリが最も多くのリソースを消費しているかを把握したい場合、またはワークロード変更前後の主要クエリの違いを比較したい場合。
-   より高次元からホットスポットを特定し、 `Table` 、 `DB` `Region` 。
-   TiKVのホットスポットをトラブルシューティングするには、CPUの側面だけでなく、ネットワークトラフィックや論理I/Oの観点からも検討する必要があります。

以下のシナリオでは、Top SQLは使用できません。

-   Top SQLは、データの誤りや異常なクラッシュなど、パフォーマンス以外の問題を特定するために使用することはできません。
-   Top SQLは、ロックの競合、トランザクションのセマンティックエラー、またはリソース消費以外の原因によるその他の問題を直接分析するのには適していません。

## ページにアクセスしてください {#access-the-page}

以下のいずれかの方法で、Top SQLページにアクセスできます。

-   TiDBダッシュボードにログイン後、左側のナビゲーションメニューにある**「Top SQL」**をクリックしてください。

    ![Top SQL](/media/dashboard/v8.5-top-sql-access.png)

-   ブラウザで[http://127.0.0.1:2379/dashboard/#/topsql](http://127.0.0.1:2379/dashboard/#/topsql)にアクセスしてください。 `127.0.0.1:2379`実際の PD ノードのアドレスとポートに置き換えてください。

## Top SQLを有効にする {#enable-top-sql}

> **注記：**
>
> Top SQLを使用するには、クラスターが最新バージョンのTiUP （v1.9.0以降）またはTiDB Operator （v1.3.0以降）を使用してデプロイまたはアップグレードされている必要があります。以前のバージョンのTiUPまたはTiDB Operatorを使用してクラスターをアップグレードした場合は、 [FAQ](/dashboard/dashboard-faq.md#a-required-component-ngmonitoring-is-not-started-error-is-shown)参照して手順を確認してください。

Top SQLは、有効にするとクラスタのパフォーマンスにわずかな影響（平均で3%以内）を与えるため、デフォルトでは有効になっていません。Top Top SQLを有効にするには、以下の手順に従ってください。

1.  [Top SQLページ](#access-the-page)にアクセスしてください。
2.  **「設定を開く」**をクリックします。ページの右側にある**設定**エリアで、「**機能を有効にする」**スイッチをオンにします。
3.  **「保存」**をクリックしてください。

Top SQLを有効にすると、その時点から収集されたデータのみが表示され、有効化前の履歴データは更新されません。データの表示には通常約1分の遅延があるため、新しいデータが表示されるまでしばらくお待ちください。Top Top SQLを無効にした後、履歴データが期限切れになっていない場合は、 Top SQLページに履歴データが表示されますが、新しいデータは収集も表示もされなくなります。

UIに加えて、TiDBシステム変数[`tidb_enable_top_sql`](/system-variables.md#tidb_enable_top_sql-new-in-v540)設定することで、 Top SQL機能を有効にすることもできます。

```sql
SET GLOBAL tidb_enable_top_sql = 1;
```

### （オプション）TiKVネットワークIO収集を有効にする<span class="version-mark">（v8.5.6の新機能）</span> {#optional-enable-tikv-network-io-collection-span-class-version-mark-new-in-v8-5-6-span}

TiKVノードの`Order By Network`または`Order By Logical IO`によるTop SQLを表示する場合、または`By Region`集計を使用する場合は、 Top SQL設定で**「TiKVネットワークIOコレクション（多次元）」スイッチを有効にし**て変更を保存します。

-   **ネットワークによる並べ替え**：TiKVリクエスト処理中に生成されたネットワークバイト数で並べ替えます。
-   **論理I/Oによる並べ替え**：TiKVリクエストに対してstorageレイヤーでTiKVによって処理された論理データの量（バイト単位）で並べ替えます。これには、読み取り中にスキャンまたは処理されたデータや、書き込みリクエストによって書き込まれたデータなどが含まれます。

次のスクリーンショットに示すように、右側の**設定**パネルには、「**機能を有効にする」**と**「TiKVネットワークIO収集（多次元）を有効にする」の**両方のスイッチが表示されます。

![Enable TiKV Network IO collection](/media/dashboard/v8.5-top-sql-settings-enable-tikv-network-io.png)

**TiKVネットワークI/O収集（多次元）を有効にすると、**storageとクエリのオーバーヘッドが増加します。有効化後、設定はすべてのTiKVノードに配信されます。データ表示には約1分の遅延が発生する場合があります。一部のTiKVノードでこの機能が有効にならない場合、ページに警告が表示され、新しいデータが不完全になる可能性があります。

新しく追加された TiKV ノードでは、このスイッチは自動的に有効になりません。Top Top SQL設定パネルで**、[TiKV ネットワーク IO コレクション (多次元)]**スイッチを [すべて有効] に設定して保存し、構成をすべての TiKV ノードに再度配信する必要があります。新しく追加された TiKV ノードでこの機能を自動的に有効にするには、 TiUPクラスタ トポロジ ファイルの`server_configs.tikv`の下に次の構成を追加し、 TiUPを使用して TiKV 構成を再配信します。

```yaml
server_configs:
  tikv:
    resource-metering.enable-network-io-collection: true
```

TiUPトポロジ構成の詳細については、 [TiUPクラスタトポロジーファイル構成](/tiup/tiup-cluster-topology-reference.md)を参照してください。

## Top SQLを使用する {#use-top-sql}

以下は、 Top SQL を使用するための一般的な手順です。

1.  [Top SQLページ](#access-the-page)にアクセスしてください。

2.  ワークロードを監視したい特定のTiDBまたはTiKVノードを選択してください。

    ![Select a TiDB or TiKV node](/media/dashboard/v8.5-top-sql-usage-select-instance.png)

    どのノードを観察すればよいかわからない場合は、まず Grafana または[TiDBダッシュボードの概要ページ](/dashboard/dashboard-overview.md)から異常なワークロードのあるノードを見つけてから、Top SQLページに戻ってさらに分析することができます。

3.  時間範囲を設定し、必要に応じてデータを更新してください。

    タイムピッカーで時間範囲を調整したり、グラフで時間範囲を選択して観測ウィンドウを拡大したりできます。時間範囲を小さく設定すると、最大1秒単位の精度でより詳細なデータが表示されます。

    ![Change time range](/media/dashboard/v8.5-top-sql-usage-change-timerange.png)

    グラフが最新でない場合は、 **「更新」**をクリックして一度更新するか、 **「更新」**ドロップダウンリストからデータの自動更新頻度を選択してください。

    ![Refresh](/media/dashboard/v8.5-top-sql-usage-refresh.png)

4.  観測モードを選択してください。

    -   `Limit`を使用すると、上位の`5` 、 `20` 、または`100` SQL クエリが表示されます。

    -   デフォルトの集計ディメンションは`By Query`です。TiKV ノードを選択した場合は、 `By Table` 、 `By DB` 、または`By Region`のディメンションで集計することもできます。

        ![Select aggregation dimension](/media/dashboard/v8.5-top-sql-usage-select-agg-by.png)

    -   デフォルトの並べ替え順序は`Order By CPU` (CPU 時間で並べ替え) です。 TiKV ノードを選択し、 [TiKVネットワークIO収集（多次元）を有効にする](#optional-enable-tikv-network-io-collection-new-in-v856)場合は、 `Order By Network` (ネットワークバイトでソート) または`Order By Logical IO` (論理 IO バイトでソート) を選択することもできます。

        ![Select order by](/media/dashboard/v8.5-top-sql-usage-select-order-by.png)

    > **注記**
    >
    > `By Region` 、 `Order By Network` 、および`Order By Logical IO`は、 [TiKVネットワークIO収集（多次元）](#optional-enable-tikv-network-io-collection-new-in-v856)が有効になっている場合にのみ利用可能です。この機能が有効になっていない場合でも履歴データが存在すると、ページには履歴データが表示され続け、新しいデータを完全に収集できない旨のメッセージが表示されます。

5.  グラフと表に示されている資源消費のホットスポットの記録を確認してください。

    ![Chart and Table](/media/dashboard/v8.5-top-sql-usage-chart.png)

    棒グラフは、現在のソートディメンションにおけるリソース消費量を示しており、異なる色は異なるレコードを表しています。表には、現在のソートディメンションに応じた累積値が表示され、末尾に`Others`行が追加され、上位N件以外のすべてのレコードが要約されます。

6.  `By Query`ビューで、テーブルの行をクリックすると、そのタイプの SQL の実行プランの詳細が表示されます。

    ![Details](/media/dashboard/v8.5-top-sql-details.png)

    SQLステートメントの詳細では、対応するSQLテンプレート、クエリテンプレートID、プランテンプレートID、および実行プランテキストを表示できます。SQLステートメントの詳細テーブルには、ノードタイプに応じて異なるメトリックが表示されます。

    -   TiDBノードは通常`Call/sec`と`Latency/call`を表示します。

    -   TiKVノードは通常、 `Call/sec` 、 `Scan Rows/sec` 、および`Scan Indexes/sec`を表示します。

    > **注記**
    >
    > `By Table` 、 `By DB` 、または`By Region`集計ビューを選択した場合、ページには集計結果が表示され、SQL実行プランごとのSQLステートメントの詳細は表示されません。

    `By Query`ビューでは、Top SQLテーブルの**[SQL ステートメントの検索]**をクリックすると、対応する SQL ステートメント分析ページに移動できます。現在のテーブルの結果をオフラインで分析する必要がある場合は、テーブルの上にある**[CSV にダウンロード] を**クリックして、現在のテーブルデータをエクスポートできます。

7.  TiKVノードでは、より高次元のホットスポットを特定する必要がある場合は、 `By Table` 、 `By DB` 、または`By Region`に切り替えて、集計結果を表示できます。

    ![Aggregated results at DB level](/media/dashboard/v8.5-top-sql-usage-agg-by-db-detail.png)

8.  これらの最初の手がかりに基づいて、 [SQLステートメント](/dashboard/dashboard-statement-list.md)または[遅いクエリ](/dashboard/dashboard-slow-query.md)ページを使用して根本原因をさらに分析できます。

## Top SQLを無効にする {#disable-top-sql}

以下の手順に従うことで、この機能を無効にすることができます。

1.  [Top SQLページ](#access-the-page)にアクセスしてください。
2.  右上隅の歯車アイコンをクリックして設定画面を開き、 **「機能を有効にする」**スイッチを無効にします。
3.  **「保存」**をクリックしてください。
4.  表示されたダイアログボックスで、 **[無効にする]**をクリックします。

Top SQLを無効にすると、新しいTop SQLデータの収集は停止しますが、過去のデータは有効期限が切れる前に引き続き閲覧できます。

UIに加えて、TiDBシステム変数[`tidb_enable_top_sql`](/system-variables.md#tidb_enable_top_sql-new-in-v540)設定することで、 Top SQL機能を無効にすることもできます。

```sql
SET GLOBAL tidb_enable_top_sql = 0;
```

### TiKVネットワークIO収集を無効にする {#disable-tikv-network-io-collection}

TiKV 用の`Network Bytes`や`Logical IO Bytes`などの多次元データの収集のみを停止し、 Top SQLの CPU 次元分析機能を維持したい場合は、 Top SQL設定パネルの**[TiKV ネットワーク IO 収集 (多次元) を有効にする]**スイッチを無効にしてください。

無効化後：

-   Top SQLページでは、以前に収集された有効期限内のネットワークI/Oおよび論理I/Oの履歴データを引き続き表示できます。
-   新しいネットワーク IO および論理 IO データ、ならびに`By Region`データは、今後収集されなくなります。

## よくある質問 {#frequently-asked-questions}

**1.Top SQLを有効にできず、UI に「必要なコンポーネントNgMonitoring が開始されていません」と表示されます**。

[TiDBダッシュボードに関するFAQ](/dashboard/dashboard-faq.md#a-required-component-ngmonitoring-is-not-started-error-is-shown)参照してください。

**2.Top SQLを有効にすると、パフォーマンスに影響が出ますか？**

Top SQLを有効にすると、クラスタのパフォーマンスにわずかな影響があります。測定結果によると、平均的なパフォーマンスへの影響は3%未満です。TiKVネットワークIO収集（多次元）も有効にすると、storageとクエリのオーバーヘッドが増加します。

**3. この機能の現状はどうなっていますか？**

これは現在、一般提供（GA）機能となっており、本番環境で使用できます。

**4. UI上の`Others`とはどういう意味ですか？**

`Others`現在のソートディメンションにおける上位 N レコード以外のすべてのレコードの集計結果を表します。これを使用すると、全体のワークロードのうち上位 N レコードが占める割合を把握できます。

**5. Top SQLで表示されるCPUオーバーヘッドと、プロセスの実際のCPU使用率との関係は何ですか？**

両者の相関関係は強いものの、全く同じものではありません。例えば、複数のレプリカを作成するコストは、Top SQLで表示されるTiKVのCPUオーバーヘッドには含まれません。一般的に、CPU使用率の高いSQL文ほど、 Top SQLに表示されるCPUオーバーヘッドも高くなります。

**6.Top SQLチャートのY軸は何を意味しますか？**

Top SQLチャートのY軸は、現在のソートディメンションにおけるリソース消費量を表します。

-   `Order By CPU`が選択されている場合、Y軸はCPU時間を表します。
-   `Order By Network`が選択されている場合、Y軸はネットワークバイトを表します。
-   `Order By Logical IO`が選択されている場合、Y軸は論理IOバイトを表します。

**7. Top SQLは実行中の（未完了の）SQL文を収集しますか？**

はい。Top Top SQLを有効にすると、TiDB Dashboardは、未完了のものも含め、実行中のすべてのSQLステートメントのリソース消費量を収集します。

**8. `Order By Network` 、 `Order By Logical IO` 、 `By Region`に新しいデータがないのはなぜですか？**

これらのビューは、TiKVネットワークIO収集（多次元）に依存します。以下の項目を確認できます。

-   TiKVノードを選択しました。
-   Top SQL設定パネルの**「TiKVネットワークIO収集（多次元）」**スイッチが有効になっています。
-   クラスター内の関連するTiKVノードはすべて、この構成を正常に有効化しています。一部のノードのみがこの構成を有効化している場合、Top SQLページに新しいデータが不完全である可能性があるという警告が表示されます。
-   新しく追加された TiKV ノードについては、Top SQL設定パネルで**「TiKV ネットワーク IO コレクション (多次元) を有効にする」**スイッチを手動で有効にし、変更を再度保存する必要があります。新しく追加されたノードでこの設定を自動的に有効にするには、 TiUPの TiKV デフォルト設定で`resource-metering.enable-network-io-collection`も有効にしてください。
