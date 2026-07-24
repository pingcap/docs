---
title: TiDB Dashboard Top SQL page
summary: Top SQLを使用して、CPU、ネットワーク、論理I/Oリソースを最も消費するクエリを特定します
---

# TiDB DashboardのTop SQLページ {#tidb-dashboard-top-sql-page}

TiDB DashboardのTop SQLページでは、指定したTiDBまたはTiKVノードで、一定期間にわたって最も多くのリソースを消費するSQLクエリを表示および分析できます。

- Top SQLを有効にすると、この機能は既存のTiDBノードおよびTiKVノードからCPUワークロードデータを継続的に収集し、最大30日間保持します。
- v8.5.7以降では、Top SQL設定で**TiKV Network IO collection (multi-dimensional)**を有効にして、指定したTiKVノードの`Network Bytes`や`Logical IO Bytes`などのメトリクスをさらに表示し、`By Query`、`By Table`、`By DB`、`By Region`の次元で集計分析を実行することもできます。

Top SQLは以下の機能を提供します。

-   現在の時間範囲で最も多くのリソースを消費する上位`5`、`20`、または`100`件のSQLクエリをグラフと表で可視化し、残りのレコードは自動的に`Others`として集約されます。
-   CPU時間またはネットワークバイトでソートされたリソース消費のホットスポットを表示します。TiKVノードを選択した場合は、論理I/Oバイトでソートすることもできます。
-   クエリごとにSQLと実行プランの詳細を表示します。TiKVノードを選択した場合は、`By Table`、`By DB`、`By Region`の次元で集計分析を行うこともできます。
-   グラフで選択した時間範囲を拡大し、データを手動で更新し、自動更新を有効にし、表データをCSVにエクスポートします。
-   実行されたすべてのSQL文（現在実行中のものも含む）を収集します。
-   特定のTiDBまたはTiKVノードのデータを表示します。

## 推奨シナリオ {#recommended-scenarios}

Top SQLは、パフォーマンスの問題を分析するのに適しています。以下に、 Top SQLの典型的なシナリオをいくつか示します。

-   クラスター内の特定のTiDBまたはTiKVノードのCPU使用率が非常に高いことがわかりました。どの種類のSQLが大量のCPUリソースを消費しているかをすばやく特定したいと考えています。
-   クラスター全体のクエリが遅くなっています。現在最も多くのリソースを消費しているSQLを見つけたい、またはワークロードの変化の前後で主なクエリの違いを比較したいと考えています。
-   より高い次元からホットスポットを特定する必要があり、TiKV側で`Table`、`DB`、または`Region`ごとにリソース消費を集計して表示したいと考えています。
-   CPU次元だけでなく、ネットワークトラフィックまたは論理I/Oの観点からTiKVホットスポットをトラブルシューティングする必要があります。

以下のシナリオでは、Top SQLは使用できません。

-   Top SQLは、データの誤りや異常なクラッシュなど、パフォーマンス以外の問題を特定するために使用することはできません。
-   Top SQLは、ロック競合、トランザクションのセマンティクスエラー、またはリソース消費が原因ではないその他の問題を直接分析するには適していません。

## ページにアクセスしてください {#access-the-page}

以下のいずれかの方法で、Top SQLページにアクセスできます。

-   TiDB Dashboardにログイン後、左側のナビゲーションメニューにある**「Top SQL」**をクリックしてください。

    ![Top SQL](/media/dashboard/v8.5-top-sql-access.png)

-   ブラウザで[http://127.0.0.1:2379/dashboard/#/topsql](http://127.0.0.1:2379/dashboard/#/topsql)にアクセスしてください。 `127.0.0.1:2379`を実際の PD ノードのアドレスとポートに置き換えてください。

## Top SQLを有効にする {#enable-top-sql}

> **Note:**
>
> Top SQLを使用するには、クラスターが最新バージョンのTiUP （v1.9.0以降）またはTiDB Operator （v1.3.0以降）を使用してデプロイまたはアップグレードされている必要があります。以前のバージョンのTiUPまたはTiDB Operatorを使用してクラスターをアップグレードした場合は、 [FAQ](/dashboard/dashboard-faq.md#a-required-component-ngmonitoring-is-not-started-error-is-shown)参照して手順を確認してください。

Top SQLは、有効にするとクラスタのパフォーマンスにわずかな影響（平均で3%以内）を与えるため、デフォルトでは有効になっていません。Top Top SQLを有効にするには、以下の手順に従ってください。

1.  [Top SQLページ](#access-the-page)にアクセスしてください。
2.  **「設定を開く」**をクリックします。ページ右側の**設定**領域で、**「機能を有効にする」**スイッチを有効にします。
3.  **「保存」**をクリックしてください。

Top SQLを有効にすると、この時点以降に収集されたデータのみを表示でき、有効化前の履歴データは補完されません。データ表示には通常約1分の遅延があるため、新しいデータを確認するには少し待つ必要があります。Top SQLを無効にした後も、履歴データの有効期限が切れていなければ、Top SQLページにはこの履歴データが引き続き表示されますが、新しいデータは収集も表示もされなくなります。

UIに加えて、TiDBシステム変数[`tidb_enable_top_sql`](/system-variables.md#tidb_enable_top_sql-new-in-v540)設定することで、 Top SQL機能を有効にすることもできます。

```sql
SET GLOBAL tidb_enable_top_sql = 1;
```

### （オプション）TiKV Network IO collectionを有効にする <span class="version-mark">v8.5.7の新機能</span> {#optional-enable-tikv-network-io-collection-new-in-v857}

TiKVノードで`Order By Network`または`Order By Logical IO`によるTop SQLを表示したり、`By Region`集計を使用したりするには、Top SQL設定で**Enable TiKV Network IO collection (multi-dimensional)**スイッチを有効にして変更を保存します。

- **Order By Network**: TiKVリクエスト処理中に生成されたネットワークバイト数でソートします。
- **Order By Logical IO**: 読み取り時にスキャンまたは処理されたデータや、書き込みリクエストによって書き込まれたデータなど、TiKVリクエストについてストレージレイヤーでTiKVが処理した論理データ量（バイト単位）でソートします。

次のスクリーンショットに示すように、右側の**Settings**パネルには**Enable Feature**と**Enable TiKV Network IO collection (multi-dimensional)**の両方のスイッチが表示されます。

![Enable TiKV Network IO collection](/media/dashboard/v8.5-top-sql-settings-enable-tikv-network-io.png)

**Enable TiKV Network IO collection (multi-dimensional)**を有効にすると、ストレージとクエリのオーバーヘッドが増加します。有効化後、この設定は現在のすべてのTiKVノードに配信されます。データ表示にも約1分の遅延が生じる場合があります。一部のTiKVノードでこの機能の有効化に失敗した場合、ページに警告が表示され、新しいデータが不完全になる可能性があります。

新しく追加されたTiKVノードには、このスイッチは自動的には有効になりません。Top SQL設定パネルで**Enable TiKV Network IO collection (multi-dimensional)**スイッチをすべて有効な状態に設定して保存し、設定をすべてのTiKVノードに再度配信する必要があります。新しく追加されたTiKVノードでもこの機能を自動的に有効にしたい場合は、TiUPクラスターのトポロジーファイルの`server_configs.tikv`の下に次の設定を追加し、TiUPを使用してTiKV設定を再配信してください。

```yaml
server_configs:
  tikv:
    resource-metering.enable-network-io-collection: true
```

TiUPトポロジー設定の詳細については、 [TiUPクラスターのトポロジーファイル設定](/tiup/tiup-cluster-topology-reference.md)を参照してください。

## Top SQLを使用する {#use-top-sql}

以下は、 Top SQL を使用するための一般的な手順です。

1.  [Top SQLページ](#access-the-page)にアクセスしてください。

2.  ワークロードを監視したい特定のTiDBまたはTiKVノードを選択してください。

    ![Select a TiDB or TiKV node](/media/dashboard/v8.5-top-sql-usage-select-instance.png)

    どのノードを監視すればよいかわからない場合は、まずGrafanaまたは[TiDB DashboardのOverviewページ](/dashboard/dashboard-overview.md)でワークロードが異常なノードを特定し、その後Top SQLページに戻ってさらに分析できます。

3.  必要に応じて時間範囲を設定し、データを更新します。

    タイムピッカーで時間範囲を調整するか、グラフで時間範囲を選択して観測ウィンドウを拡大できます。時間範囲を小さく設定すると、最大1秒の精度でよりきめ細かいデータが表示されます。

    ![Change time range](/media/dashboard/v8.5-top-sql-usage-change-timerange.png)

    グラフが最新でない場合は、**Refresh**をクリックして1回更新するか、**Refresh**ドロップダウンリストからデータの自動更新頻度を選択します。

    ![Refresh](/media/dashboard/v8.5-top-sql-usage-refresh.png)

4.  観測モードを選択します。

    - `Limit`を使用して、Top `5`、`20`、または`100`件のSQLクエリを表示します。
    - デフォルトの集計次元は`By Query`です。TiKVノードを選択した場合は、`By Table`、`By DB`、または`By Region`の次元で集計することもできます。

        ![Select aggregation dimension](/media/dashboard/v8.5-top-sql-usage-select-agg-by.png)

    - デフォルトのソート順は`Order By CPU`（CPU時間でソート）です。TiKVノードを選択し、[TiKV Network IO collection (multi-dimensional)を有効にしている](#optional-enable-tikv-network-io-collection-new-in-v857)場合は、`Order By Network`（ネットワークバイトでソート）または`Order By Logical IO`（論理IOバイトでソート）を選択することもできます。

        ![Select order by](/media/dashboard/v8.5-top-sql-usage-select-order-by.png)

    > **Note:**
    >
    > `By Region`、`Order By Network`、および`Order By Logical IO`は、[TiKV Network IO collection (multi-dimensional)](#optional-enable-tikv-network-io-collection-new-in-v857)が有効な場合にのみ使用できます。この機能が有効でなくても履歴データがまだ存在する場合、ページには引き続き履歴データが表示され、新しいデータを完全には収集できないことが示されます。

5.  グラフと表でリソース消費のホットスポットレコードを確認します。

    ![Chart and Table](/media/dashboard/v8.5-top-sql-usage-chart.png)

    棒グラフは現在のソート次元でのリソース消費を示し、異なる色は異なるレコードを表します。表には現在のソート次元に従った累積値が表示され、末尾にはTop N以外のすべてのレコードを集約する`Others`行が表示されます。

6.  `By Query`ビューで、表の行をクリックすると、その種類のSQLの実行プラン詳細を表示できます。

    ![Details](/media/dashboard/v8.5-top-sql-details.png)

    SQL文の詳細では、対応するSQLテンプレート、Query template ID、Plan template ID、および実行プランテキストを確認できます。SQL文詳細テーブルには、ノードタイプに応じて異なるメトリクスが表示されます。

    - TiDBノードには通常、`Call/sec`と`Latency/call`が表示されます。
    - TiKVノードには通常、`Call/sec`、`Scan Rows/sec`、および`Scan Indexes/sec`が表示されます。

    > **Note**
    >
    > `By Table`、`By DB`、または`By Region`の集計ビューを選択した場合、ページには集計結果が表示され、SQL実行プランごとのSQL文詳細は表示されません。

    `By Query`ビューでは、Top SQLテーブル内の**Search in SQL Statements**をクリックして、対応するSQL Statement Analysisページに移動することもできます。現在の表の結果をオフラインで分析する必要がある場合は、表の上にある**Download to CSV**をクリックして現在の表データをエクスポートできます。

7.  TiKVノードで、より高い次元からホットスポットを特定する必要がある場合は、`By Table`、`By DB`、または`By Region`に切り替えて集計結果を表示できます。

    ![Aggregated results at DB level](/media/dashboard/v8.5-top-sql-usage-agg-by-db-detail.png)

8.  これらの最初の手がかりに基づいて、 [SQLステートメント](/dashboard/dashboard-statement-list.md)または[スロークエリ](/dashboard/dashboard-slow-query.md)ページを使用して根本原因をさらに分析できます。

## Top SQLを無効にする {#disable-top-sql}

以下の手順に従うことで、この機能を無効にすることができます。

1.  [Top SQLページ](#access-the-page)にアクセスしてください。
2.  右上隅の歯車アイコンをクリックして設定ペインを開き、**「機能を有効にする」**スイッチを無効にします。
3.  **「保存」**をクリックしてください。
4.  ポップアップ表示されたダイアログボックスで、 **「無効にする」**をクリックします。

Top SQLを無効にすると、Top SQLは新しいデータの収集を停止しますが、有効期限が切れる前の履歴データは引き続き表示できます。

UIに加えて、TiDBシステム変数[`tidb_enable_top_sql`](/system-variables.md#tidb_enable_top_sql-new-in-v540)設定することで、 Top SQL機能を無効にすることもできます。

```sql
SET GLOBAL tidb_enable_top_sql = 0;
```

### TiKV Network IO collectionを無効にする {#disable-tikv-network-io-collection}

Top SQLのCPU次元の分析機能は維持したまま、TiKVの`Network Bytes`や`Logical IO Bytes`などの多次元データの収集のみを停止したい場合は、Top SQL設定パネルで**Enable TiKV Network IO collection (multi-dimensional)**スイッチを無効にします。

無効化後:

- Top SQLページでは、以前に収集された有効期限切れでない履歴のnetwork IOおよびlogical IOデータを引き続き表示できます。
- 新しいnetwork IOおよびlogical IOデータ、ならびに`By Region`データは収集されなくなります。

## よくある質問 {#frequently-asked-questions}

**1.Top SQLを有効にできず、UI に「必要なコンポーネントNgMonitoring が開始されていません」と表示されます**。

[TiDB Dashboardに関するFAQ](/dashboard/dashboard-faq.md#a-required-component-ngmonitoring-is-not-started-error-is-shown)参照してください。

**2.Top SQLを有効にすると、パフォーマンスに影響が出ますか？**

Top SQLを有効にすると、クラスターのパフォーマンスにわずかな影響があります。測定によると、平均的なパフォーマンスへの影響は3%未満です。TiKV Network IO collection (multi-dimensional)も有効にすると、追加のストレージおよびクエリのオーバーヘッドが発生します。

**3. この機能の現状はどうなっていますか？**

これは現在、一般提供（GA）機能となっており、本番環境で使用できます。

**4. UIの`Others`は何を意味しますか？**

`Others`は、現在のソート次元におけるTop N以外のすべてのレコードの集計結果を表します。これを使用して、全体のワークロードのうちTop Nレコードがどの程度を占めるかを把握できます。

**5. Top SQLで表示されるCPUオーバーヘッドと、プロセスの実際のCPU使用率との関係は何ですか？**

両者の相関関係は強いものの、全く同じものではありません。例えば、複数のレプリカを作成するコストは、Top SQLで表示されるTiKVのCPUオーバーヘッドには含まれません。一般的に、CPU使用率の高いSQL文ほど、 Top SQLに表示されるCPUオーバーヘッドも高くなります。

**6.Top SQLチャートのY軸は何を意味しますか？**

Top SQLチャートのY軸は、現在のソート次元でのリソース消費を表します。

- `Order By CPU`を選択した場合、Y軸はCPU時間を表します。
- `Order By Network`を選択した場合、Y軸はネットワークバイトを表します。
- `Order By Logical IO`を選択した場合、Y軸は論理IOバイトを表します。

**7. Top SQLは実行中の（未完了の）SQL文を収集しますか？**

はい。Top SQLを有効にすると、TiDB Dashboardは未完了のものを含む、実行中のすべてのSQL文のリソース消費を収集します。

**8. `Order By Network`、`Order By Logical IO`、または`By Region`に新しいデータがないのはなぜですか？**

これらのビューはTiKV Network IO collection (multi-dimensional)に依存します。次の項目を確認できます。

- TiKVノードを選択していること。
- Top SQL設定パネルの**Enable TiKV Network IO collection (multi-dimensional)**スイッチが有効になっていること。
- クラスター内の関連するTiKVノードがすべてこの設定の有効化に成功していること。一部のノードのみがこの設定を有効にしている場合、Top SQLページには新しいデータが不完全である可能性が示されます。
- 新しく追加されたTiKVノードについては、Top SQL設定パネルで**Enable TiKV Network IO collection (multi-dimensional)**スイッチを手動で有効にし、変更を再度保存する必要があります。この設定を新しく追加されたノードで自動的に有効にするには、TiUPのTiKVデフォルト設定でも`resource-metering.enable-network-io-collection`を有効にします.
