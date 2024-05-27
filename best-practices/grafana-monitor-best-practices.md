---
title: Best Practices for Monitoring TiDB Using Grafana
summary: Grafana を使用して TiDB を監視するためのベスト プラクティス。TiUPを使用して TiDB クラスターをデプロイ、監視用に Grafana と Prometheus を追加します。メトリックを使用してクラスターの状態を分析し、問題を診断します。Prometheus は TiDB コンポーネントからメトリックを収集し、Grafana はそれを表示します。Grafana を効率的に使用するためのヒントには、クエリ式の変更、Y 軸スケールの切り替え、クエリ結果の API の使用などがあります。このプラットフォームは、TiDB クラスターの状態を分析および診断する強力なツールです。
---

# Grafana を使用した TiDB 監視のベスト プラクティス {#best-practices-for-monitoring-tidb-using-grafana}

[TiUPを使用してTiDBクラスタを展開する](/production-deployment-using-tiup.md)トポロジ構成に Grafana と Prometheus を追加すると、 [Grafana + Prometheus 監視プラットフォーム](/tidb-monitoring-framework.md)のセットが同時にデプロイされ、TiDB クラスター内のさまざまなコンポーネントとマシンのメトリックを収集して表示します。このドキュメントでは、Grafana を使用して TiDB を監視するためのベスト プラクティスについて説明します。メトリックを使用して TiDB クラスターの状態を分析し、問題を診断するのに役立つことを目的としています。

## 監視アーキテクチャ {#monitoring-architecture}

[プロメテウス](https://prometheus.io/)は、多次元データ モデルと柔軟なクエリ言語を備えた時系列データベースです。2 [グラファナ](https://grafana.com/) 、メトリックを分析および視覚化するためのオープン ソース監視システムです。

![The monitoring architecture in the TiDB cluster](/media/prometheus-in-tidb.png)

TiDB 2.1.3 以降のバージョンでは、TiDB モニタリングはプル方式をサポートしています。これは、次のような利点がある優れた調整です。

-   Prometheus を移行する必要がある場合、TiDB クラスター全体を再起動する必要はありません。調整の前に、Prometheus を移行するには、ターゲット アドレスを更新する必要があるため、クラスター全体を再起動する必要があります。
-   監視ポイントが 1 つになることを防ぐために、Grafana + Prometheus 監視プラットフォーム (高可用性ではない) の 2 つの別々のセットを展開できます。
-   単一障害点となる可能性のある Pushgateway が削除されます。

## 監視データのソースと表示 {#source-and-display-of-monitoring-data}

TiDB の 3 つのコア コンポーネント (TiDBサーバー、TiKVサーバー、PDサーバー) は、HTTP インターフェイスを介してメトリックを取得します。これらのメトリックはプログラム コードから収集され、ポートは次のとおりです。

| 成分       | ポート   |
| :------- | :---- |
| TiDBサーバー | 10080 |
| TiKVサーバー | 20181 |
| PDサーバー   | 2379  |

HTTP インターフェイスを介して SQL ステートメントの QPS を確認するには、次のコマンドを実行します。TiDBサーバーを例に挙げます。

```bash
curl http://__tidb_ip__:10080/metrics |grep tidb_executor_statement_total
```

    # Check the real-time QPS of different types of SQL statements. The numbers below are the cumulative values of counter type (scientific notation).
    tidb_executor_statement_total{type="Delete"} 520197
    tidb_executor_statement_total{type="Explain"} 1
    tidb_executor_statement_total{type="Insert"} 7.20799402e+08
    tidb_executor_statement_total{type="Select"} 2.64983586e+08
    tidb_executor_statement_total{type="Set"} 2.399075e+06
    tidb_executor_statement_total{type="Show"} 500531
    tidb_executor_statement_total{type="Use"} 466016

上記のデータは Prometheus に保存され、Grafana に表示されます。パネルを右クリックし、次の図に示すように**編集**ボタンをクリックするか (または直接<kbd>E</kbd>キーを押します)。

![The Edit entry for the Metrics tab](/media/best-practices/metric-board-edit-entry.png)

**[編集]**ボタンをクリックすると、[メトリック] タブに`tidb_executor_statement_total`メトリック名を含むクエリ式が表示されます。パネル上のいくつかの項目の意味は次のとおりです。

-   `rate[1m]` : 1分間の成長率。カウンター型のデータにのみ使用できます。
-   `sum` : 値の合計。
-   `by type` : 合計データは元のメトリック値のタイプ別にグループ化されます。
-   `Legend format` : メトリック名の形式。
-   `Resolution` : ステップ幅のデフォルトは 15 秒です。解像度は、複数のピクセルに対して 1 つのデータ ポイントを生成するかどうかを意味します。

**[メトリック]**タブのクエリ式は次のとおりです。

![The query expression on the Metrics tab](/media/best-practices/metric-board-expression.jpeg)

Prometheusは多くのクエリ式と関数をサポートしています。詳細については、 [プロメテウス公式サイト](https://prometheus.io/docs/prometheus/latest/querying)を参照してください。

## Grafanaのヒント {#grafana-tips}

このセクションでは、Grafana を使用して TiDB のメトリックを効率的に監視および分析するための 7 つのヒントを紹介します。

### ヒント1: すべてのディメンションをチェックし、クエリ式を編集する {#tip-1-check-all-dimensions-and-edit-the-query-expression}

セクション[監視データのソースと表示](#source-and-display-of-monitoring-data)に示した例では、データはタイプ別にグループ化されています。他のディメンションでグループ化できるかどうか、またどのディメンションが使用可能かをすばやく確認したい場合は、次の方法を使用できます。**クエリ式にメトリック名のみを残し、計算は行わず、 `Legend format`フィールドを空白のままにします**。このようにすると、元のメトリックが表示されます。たとえば、次の図は、3 つのディメンション ( `instance` 、 `job` 、 `type` ) があることを示しています。

![Edit query expression and check all dimensions](/media/best-practices/edit-expression-check-dimensions.jpg)

次に、 `type`の後に`instance`ディメンションを追加し、 `Legend format`フィールドに`{{instance}}`追加して、クエリ式を変更できます。このようにして、各 TiDBサーバーで実行されるさまざまな種類の SQL ステートメントの QPS を確認できます。

![Add an instance dimension to the query expression](/media/best-practices/add-instance-dimension.jpeg)

### ヒント2: Y軸のスケールを切り替える {#tip-2-switch-the-scale-of-the-y-axis}

クエリ期間を例にとると、Y 軸はデフォルトで 2 進対数スケール (log <sub>2</sub> n) に設定されており、表示のギャップが狭くなります。変化を強調するには、線形スケールに切り替えることができます。次の 2 つの図を比較すると、表示の違いが簡単にわかり、SQL ステートメントの実行が遅い時間を特定できます。

もちろん、線形スケールはすべての状況に適しているわけではありません。たとえば、1 か月間のパフォーマンスの傾向を観察する場合、線形スケールではノイズが発生し、観察が困難になる可能性があります。

Y 軸はデフォルトで 2 進対数スケールを使用します。

![The Y-axis uses a binary logarithmic scale](/media/best-practices/default-axes-scale.jpg)

Y 軸を線形スケールに切り替えます。

![Switch to a linear scale](/media/best-practices/axes-scale-linear.jpg)

> **ヒント：**
>
> ヒント 2 とヒント 1 を組み合わせると、 `SELECT`ステートメントと`UPDATE`のステートメントのどちらが遅いかをすぐに分析するのに役立つ`sql_type`ディメンションを見つけることができます。また、遅い SQL ステートメントのインスタンスを見つけることもできます。

### ヒント3: Y軸のベースラインを変更して変化を強調する {#tip-3-modify-the-baseline-of-the-y-axis-to-amplify-changes}

線形スケールに切り替えても、傾向がまだ見えない場合があります。たとえば、次の図では、クラスターをスケーリングした後、 `Store size`のリアルタイムの変化を観察したいのですが、ベースラインが大きいため、小さな変化は見えません。このような状況では、Y 軸のベースラインを`0`から`auto`に変更して、上部を拡大することができます。下の 2 つの図を確認すると、データ移行が始まっていることがわかります。

ベースラインのデフォルトは`0`です。

![Baseline defaults to 0](/media/best-practices/default-y-min.jpeg)

ベースラインを`auto`に変更します。

![Change the baseline to auto](/media/best-practices/y-min-auto.jpg)

### ヒント4: 共有のクロスヘアまたはツールチップを使用する {#tip-4-use-shared-crosshair-or-tooltip}

**設定**パネルには、デフォルトで**Default**に設定されている**グラフ ツールチップ**パネル オプションがあります。

![Graphic presentation tools](/media/best-practices/graph-tooltip.jpeg)

次の図に示すように、**共有クロスヘア**と**共有ツールチップ**をそれぞれ使用して効果をテストできます。その後、スケールがリンクして表示されるため、問題を診断するときに 2 つのメトリックの相関関係を確認するのに便利です。

グラフィックプレゼンテーションツールを**共有クロスヘア**に設定します。

![Set the graphical presentation tool to Shared crosshair](/media/best-practices/graph-tooltip-shared-crosshair.jpeg)

グラフィカルプレゼンテーションツールを**共有ツールチップ**に設定します。

![Set the graphic presentation tool to Shared Tooltip](/media/best-practices/graph-tooltip-shared-tooltip.jpg)

### ヒント5: 履歴のメトリックを確認するには、 <code>IP address:port number</code>を入力します。 {#tip-5-enter-code-ip-address-port-number-code-to-check-the-metrics-in-history}

PD のダッシュボードには、現在のリーダーの指標のみが表示されます。履歴内の PD リーダーのステータスを確認する場合、その PD リーダーが`instance`フィールドのドロップダウン リストに存在しない場合は、手動で`IP address:2379`を入力してリーダーのデータを確認できます。

![Check the metrics in history](/media/best-practices/manually-input-check-metric.jpeg)

### ヒント6: <code>Avg</code>関数を使用する {#tip-6-use-the-code-avg-code-function}

通常、凡例ではデフォルトで`Max`と`Current`関数のみが使用可能です。指標が大きく変動する場合は、凡例に`Avg`機能などの他のサマリー関数を追加して、一定期間の全体的な傾向を確認できます。

`Avg`関数などの集計関数を追加します。

![Add summary functions such as Avg](/media/best-practices/add-avg-function.jpeg)

次に、全体的な傾向を確認します。

![Add Avg function to check the overall trend](/media/best-practices/add-avg-function-check-trend.jpg)

### ヒント7: PrometheusのAPIを使用してクエリ式の結果を取得する {#tip-7-use-the-api-of-prometheus-to-obtain-the-result-of-query-expressions}

Grafana は Prometheus の API を通じてデータを取得しており、この API を使用して情報を取得することもできます。また、次のような用途もあります。

-   クラスターのサイズやステータスなどの情報を自動的に取得します。
-   1 日あたりの QPS の合計量、1 日あたりの QPS のピーク値、1 日あたりの応答時間のカウントなど、レポートの情報を提供するために式に小さな変更を加えます。
-   重要な指標について定期的な健全性検査を実行します。

Prometheus の API は次のようになります。

![The API of Prometheus](/media/best-practices/prometheus-api-interface.jpg)

```bash
curl -u user:pass 'http://__grafana_ip__:3000/api/datasources/proxy/1/api/v1/query_range?query=sum(tikv_engine_size_bytes%7Binstancexxxxxxxxx20181%22%7D)%20by%20(instance)&start=1565879269&end=1565882869&step=30' |python -m json.tool
```

    {
        "data": {
            "result": [
                {
                    "metric": {
                        "instance": "xxxxxxxxxx:20181"
                    },
                    "values": [
                        [
                            1565879269,
                            "1006046235280"
                        ],
                        [
                            1565879299,
                            "1006057877794"
                        ],
                        [
                            1565879329,
                            "1006021550039"
                        ],
                        [
                            1565879359,
                            "1006021550039"
                        ],
                        [
                            1565882869,
                            "1006132630123"
                        ]
                    ]
                }
            ],
            "resultType": "matrix"
        },
        "status": "success"
    }

## まとめ {#summary}

Grafana + Prometheus 監視プラットフォームは非常に強力なツールです。これをうまく活用することで効率が向上し、TiDB クラスターの状態を分析する時間を大幅に節約できます。さらに重要なのは、問題の診断に役立つことです。このツールは、特に大量のデータがある場合、TiDB クラスターの運用と保守に非常に役立ちます。
