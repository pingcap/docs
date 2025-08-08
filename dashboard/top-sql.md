---
title: TiDB Dashboard Top SQL page
summary: TiDBダッシュボードのTop SQLは、データベース内のSQL文のCPUオーバーヘッドをリアルタイムで監視・可視化します。CPU負荷の高いSQL文を特定し、詳細な実行情報を提供することで、パフォーマンスの最適化を支援します。パフォーマンスの問題分析に適しており、TiDBダッシュボードまたはブラウザからアクセスできます。この機能はクラスタのパフォーマンスに若干の影響を及ぼしますが、本番での一般提供を開始しました。
---

# TiDBダッシュボードのTop SQLページ {#tidb-dashboard-top-sql-page}

Top SQLを使用すると、データベース内の各 SQL 文の CPU オーバーヘッドをリアルタイムで監視し、視覚的に把握できます。これにより、データベースのパフォーマンス問題の最適化と解決に役立ちます。Top Top SQL は、すべての TiDB および TiKV インスタンスから、任意の秒数における SQL 文ごとにまとめられた CPU 負荷データを継続的に収集し、保存します。収集されたデータは最大 30 日間保存できます。Top Top SQL は、視覚的なグラフと表を表示し、一定期間にわたって TiDB または TiKV インスタンスの CPU 負荷を高めている SQL 文を迅速に特定できるようにします。

Top SQL は次の機能を提供します。

-   グラフと表を使用して、CPU オーバーヘッドが最も高い上位 5 種類の SQL ステートメントを視覚化します。
-   1 秒あたりのクエリ数、平均レイテンシー、クエリ プランなどの詳細な実行情報を表示します。
-   まだ実行中のものも含め、実行されたすべての SQL ステートメントを収集します。
-   特定の TiDB および TiKV インスタンスのデータを表示できるようにします。

## 推奨シナリオ {#recommended-scenarios}

Top SQLはパフォーマンスの問題を分析するのに適しています。以下は、 Top SQLの典型的なシナリオです。

-   Grafanaのチャートから、クラスター内の個々のTiKVインスタンスのCPU使用率が非常に高いことがわかりました。どのSQL文がCPUホットスポットを引き起こしているかを把握することで、それらを最適化し、分散リソース全体をより有効に活用したいと考えています。
-   クラスター全体のCPU使用率が非常に高く、クエリの実行速度が遅いことがわかりました。どのSQL文が最もCPUリソースを消費しているかを迅速に把握し、最適化したいと考えています。
-   クラスターの CPU 使用率が大幅に変化したため、その主な原因を知りたいと考えています。
-   クラスター内で最もリソースを消費する SQL ステートメントを分析し、最適化してハードウェア コストを削減します。

Top SQL は次のシナリオでは使用できません。

-   Top SQL は、不正なデータや異常なクラッシュなど、パフォーマンス以外の問題を正確に特定するために使用することはできません。
-   Top SQL は、トランザクション ロックの競合など、CPU の高負荷が原因ではないデータベース パフォーマンスの問題の分析をサポートしていません。

## ページにアクセスする {#access-the-page}

次のいずれかの方法で「Top SQL」ページにアクセスできます。

-   TiDB ダッシュボードにログインしたら、左側のナビゲーション メニューで**[Top SQL]**をクリックします。

    ![Top SQL](/media/dashboard/top-sql-access.png)

-   ブラウザで[http://127.0.0.1:2379/ダッシュボード/#/topsql](http://127.0.0.1:2379/dashboard/#/topsql)アクセスしてください。3 `127.0.0.1:2379`実際のPDインスタンスのアドレスとポートに置き換えてください。

## Top SQLを有効にする {#enable-top-sql}

> **注記：**
>
> Top SQLを使用するには、クラスターを最新バージョンのTiUP （v1.9.0 以上）またはTiDB Operator （v1.3.0 以上）でデプロイまたはアップグレードする必要があります。以前のバージョンのTiUPまたはTiDB Operatorを使用してクラスターをアップグレードした場合は、手順[FAQ](/dashboard/dashboard-faq.md#a-required-component-ngmonitoring-is-not-started-error-is-shown)参照してください。

Top SQLは、有効化するとクラスターのパフォーマンスにわずかな影響（平均3%以内）を与えるため、デフォルトでは有効化されていません。Top Top SQLは、以下の手順で有効化できます。

1.  [Top SQLページ](#access-the-page)ご覧ください。
2.  **「設定を開く」を**クリックします。**設定**領域の右側にある**「機能を有効にする」**をオンにします。
3.  **[保存]を**クリックします。

この機能を有効にした後、 Top SQLがデータをロードするまで最大1分ほどお待ちください。その後、CPU負荷の詳細を確認できます。

UI に加えて、TiDB システム変数[`tidb_enable_top_sql`](/system-variables.md#tidb_enable_top_sql-new-in-v540)設定することでTop SQL機能を有効にすることもできます。

```sql
SET GLOBAL tidb_enable_top_sql = 1;
```

## Top SQLを使用する {#use-top-sql}

Top SQLを使用する一般的な手順は次のとおりです。

1.  [Top SQLページ](#access-the-page)ご覧ください。

2.  負荷を監視する特定の TiDB または TiKV インスタンスを選択します。

    ![Select Instance](/media/dashboard/top-sql-usage-select-instance.png)

    どのTiDBまたはTiKVインスタンスを監視すべきかわからない場合は、任意のインスタンスを選択できます。また、クラスターのCPU負荷が極端に不均衡な場合は、まずGrafanaチャートを使用して、監視するインスタンスを特定することもできます。

3.  Top SQLが提示するグラフと表を観察します。

    ![Chart and Table](/media/dashboard/top-sql-usage-chart.png)

    棒グラフの棒の大きさは、その時点でSQL文が消費しているCPUリソースの量を表しています。色の違いはSQL文の種類によって区別されます。ほとんどの場合、グラフ内の対応する時間範囲においてCPUリソースのオーバーヘッドが大きいSQL文にのみ注目すれば十分です。

4.  表内のSQL文をクリックすると、詳細情報が表示されます。その文の様々なプランにおける詳細な実行指標（Call/sec（1秒あたりの平均クエリ数）やScan Indexes/sec（1秒あたりの平均インデックス行スキャン数）など）を確認できます。

    ![Details](/media/dashboard/top-sql-details.png)

5.  これらの最初の手がかりに基づいて、 [SQL文](/dashboard/dashboard-statement-list.md)目または[遅いクエリ](/dashboard/dashboard-slow-query.md)ページ目をさらに調査し、CPU 消費量の増加や SQL ステートメントの大量データ スキャンの根本原因を見つけることができます。

    タイムピッカーで時間範囲を調整するか、チャートで時間範囲を選択すると、問題をより正確かつ詳細に把握できます。時間範囲を狭くすると、最大1秒単位の精度でより詳細なデータを取得できます。

    ![Change time range](/media/dashboard/top-sql-usage-change-timerange.png)

    グラフが古い場合は、 **[更新]**ボタンをクリックするか、 **[更新]**ドロップダウン リストから [自動更新] オプションを選択できます。

    ![Refresh](/media/dashboard/top-sql-usage-refresh.png)

6.  テーブルまたはデータベースレベルごとにCPUリソースの使用状況をビュー、より高レベルのリソース使用状況を迅速に把握できます。現在、TiKVインスタンスのみがサポートされています。

    TiKV インスタンスを選択し、**テーブル**別または**DB 別**を選択します。

    ![Select aggregation dimension](/media/dashboard/top-sql-usage-select-agg-by.png)

    集計結果を上位レベルでビュー。

    ![Aggregated results at DB level](/media/dashboard/top-sql-usage-agg-by-db-detail.png)

## Top SQLを無効にする {#disable-top-sql}

次の手順に従って、この機能を無効にできます。

1.  [Top SQLページ](#access-the-page)訪問します。
2.  右上隅の歯車アイコンをクリックして設定画面を開き、 **「機能の有効化」**をオフにします。
3.  **［保存］を**クリックします。
4.  ポップアップされたダイアログボックスで、 **[無効にする]**をクリックします。

UI に加えて、TiDB システム変数[`tidb_enable_top_sql`](/system-variables.md#tidb_enable_top_sql-new-in-v540)設定することでTop SQL機能を無効にすることもできます。

```sql
SET GLOBAL tidb_enable_top_sql = 0;
```

## よくある質問 {#frequently-asked-questions}

**1. Top SQLを有効にできず、UI に「必要なコンポーネントNgMonitoring が開始されていません」と表示されます**。

[TiDBダッシュボードFAQ](/dashboard/dashboard-faq.md#a-required-component-ngmonitoring-is-not-started-error-is-shown)参照。

**2. Top SQLを有効にするとパフォーマンスに影響はありますか?**

この機能はクラスタのパフォーマンスにわずかな影響を与えます。当社のベンチマークによると、この機能を有効にした場合のパフォーマンスへの影響は平均で通常3%未満です。

**3. この機能のステータスはどうなっていますか?**

これは現在、一般公開 (GA) された機能であり、本番環境で使用できます。

**4. 「その他の記述」とはどういう意味ですか?**

「その他のステートメント」は、上位5つ以外のすべてのステートメントのCPUオーバーヘッドの合計をカウントします。この情報により、上位5つのステートメントが全体と比較してどの程度のCPUオーバーヘッドをもたらしているかを把握できます。

**5. Top SQLによって表示される CPU オーバーヘッドとプロセスの実際の CPU 使用率との関係は何ですか?**

これらは強い相関関係にありますが、全く同じものではありません。例えば、複数のレプリカを書き込むコストは、 Top SQLに表示される TiKV CPU オーバーヘッドには含まれません。一般的に、CPU 使用率の高い SQL 文は、 Top SQLに表示される CPU オーバーヘッドも高くなります。

**6.Top SQLグラフの Y 軸の意味は何ですか?**

これは消費されたCPUリソースの量を表します。SQL文によって消費されるリソースが多いほど、値は大きくなります。ほとんどの場合、特定の値の意味や単位を気にする必要はありません。

**7. Top SQL は実行中の (未完了の) SQL ステートメントを収集しますか?**

はい。各瞬間の「Top SQL」チャートに表示されるバーは、その瞬間に実行中のすべての SQL ステートメントの CPU オーバーヘッドを示します。
