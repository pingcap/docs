---
title: Best Practices for Monitoring TiDB Using Grafana
summary: Learn seven tips for efficiently using Grafana to monitor TiDB.
---

# Grafanaを使用してTiDBを監視するためのベストプラクティス {#best-practices-for-monitoring-tidb-using-grafana}

[TiUPを使用してTiDBクラスタをデプロイする](/production-deployment-using-tiup.md)を実行し、トポロジ構成にGrafanaとPrometheusを追加すると、 [Grafana+Prometheusモニタリングプラットフォーム](/tidb-monitoring-framework.md)のセットが同時にデプロイされ、TiDBクラスタのさまざまなコンポーネントとマシンのメトリックを収集して表示します。このドキュメントでは、Grafanaを使用してTiDBを監視するためのベストプラクティスについて説明します。これは、メトリックを使用してTiDBクラスタのステータスを分析し、問題を診断するのに役立つことを目的としています。

## 監視アーキテクチャ {#monitoring-architecture}

[プロメテウス](https://prometheus.io/)は、多次元データモデルと柔軟なクエリ言語を備えた時系列データベースです。 [Grafana](https://grafana.com/)は、メトリックを分析および視覚化するためのオープンソースの監視システムです。

![The monitoring architecture in the TiDB cluster](/media/prometheus-in-tidb.png)

TiDB 2.1.3以降のバージョンでは、TiDBモニタリングはプル方式をサポートしています。これは、次の利点を備えた適切な調整です。

-   Prometheusを移行する必要がある場合は、TiDBクラスタ全体を再起動する必要はありません。調整する前に、ターゲットアドレスを更新する必要があるため、Prometheusを移行するにはクラスタ全体を再起動する必要があります。
-   Grafana + Prometheusモニタリングプラットフォームの2つの別々のセット（高可用性ではありません）をデプロイして、単一のモニタリングポイントを防ぐことができます。
-   単一障害点になる可能性のあるプッシュゲートウェイが削除されます。

## モニタリングデータのソースと表示 {#source-and-display-of-monitoring-data}

TiDBの3つのコアコンポーネント（TiDBサーバー、TiKVサーバー、PDサーバー）は、HTTPインターフェイスを介してメトリックを取得します。これらのメトリックはプログラムコードから収集され、ポートは次のとおりです。

| 成分       | ポート   |
| :------- | :---- |
| TiDBサーバー | 10080 |
| TiKVサーバー | 20181 |
| PDサーバー   | 2379  |

次のコマンドを実行して、HTTPインターフェイスを介してSQLステートメントのQPSを確認します。例としてTiDBサーバーを取り上げます。

{{< copyable "" >}}

```bash
curl http://__tidb_ip__:10080/metrics |grep tidb_executor_statement_total
```

```
# Check the real-time QPS of different types of SQL statements. The numbers below are the cumulative values of counter type (scientific notation).
tidb_executor_statement_total{type="Delete"} 520197
tidb_executor_statement_total{type="Explain"} 1
tidb_executor_statement_total{type="Insert"} 7.20799402e+08
tidb_executor_statement_total{type="Select"} 2.64983586e+08
tidb_executor_statement_total{type="Set"} 2.399075e+06
tidb_executor_statement_total{type="Show"} 500531
tidb_executor_statement_total{type="Use"} 466016
```

上記のデータはPrometheusに保存され、Grafanaに表示されます。パネルを右クリックしてから、次の図に示す[**編集**]ボタンをクリックします（または<kbd>E</kbd>キーを直接押します）。

![The Edit entry for the Metrics tab](/media/best-practices/metric-board-edit-entry.png)

[**編集**]ボタンをクリックすると、[メトリック]タブに`tidb_executor_statement_total`のメトリック名のクエリ式が表示されます。パネル上のいくつかの項目の意味は次のとおりです。

-   `rate[1m]` ：1分間の成長率。カウンタタイプのデータにのみ使用できます。
-   `sum` ：値の合計。
-   `by type` ：合計されたデータは、元のメトリック値のタイプごとにグループ化されます。
-   `Legend format` ：メトリック名の形式。
-   `Resolution` ：ステップ幅のデフォルトは15秒です。解像度とは、複数のピクセルに対して1つのデータポイントを生成するかどうかを意味します。

[**メトリック**]タブのクエリ式は次のとおりです。

![The query expression on the Metrics tab](/media/best-practices/metric-board-expression.jpeg)

Prometheusは、多くのクエリ式と関数をサポートしています。詳細については、 [プロメテウス公式サイト](https://prometheus.io/docs/prometheus/latest/querying)を参照してください。

## Grafanaのヒント {#grafana-tips}

このセクションでは、Grafanaを効率的に使用してTiDBのメトリックを監視および分析するための7つのヒントを紹介します。

### ヒント1：すべてのディメンションを確認し、クエリ式を編集します {#tip-1-check-all-dimensions-and-edit-the-query-expression}

[モニタリングデータのソースと表示](#source-and-display-of-monitoring-data)セクションに示されている例では、データはタイプごとにグループ化されています。他のディメンションでグループ化できるかどうかを知り、使用可能なディメンションをすばやく確認する場合は、次の方法を使用でき**ます。クエリ式にメトリック名のみを保持し、計算は行わず、[ `Legend format` ]フィールドは空白のままにします**。このようにして、元のメトリックが表示されます。たとえば、次の図は、 `type`つの次元（ `instance` 、および`job` ）があることを示しています。

![Edit query expression and check all dimensions](/media/best-practices/edit-expression-check-dimensions.jpg)

次に、 `type`の後に`instance`ディメンションを追加し、 `Legend format`フィールドに`{{instance}}`を追加することで、クエリ式を変更できます。このようにして、各TiDBサーバーで実行されるさまざまなタイプのSQLステートメントのQPSを確認できます。

![Add an instance dimension to the query expression](/media/best-practices/add-instance-dimension.jpeg)

### ヒント2：Y軸のスケールを切り替える {#tip-2-switch-the-scale-of-the-y-axis}

クエリ期間を例にとると、Y軸はデフォルトで2進対数スケール（log <sub>2</sub> n）になり、表示のギャップが狭くなります。変化を増幅するために、線形スケールに切り替えることができます。次の2つの図を比較すると、表示の違いに簡単に気づき、SQLステートメントの実行が遅い時間を見つけることができます。

もちろん、線形スケールはすべての状況に適しているわけではありません。たとえば、1か月間のパフォーマンスの傾向を観察すると、線形スケールのノイズが発生し、観察が困難になる可能性があります。

Y軸は、デフォルトで2進の対数目盛を使用します。

![The Y-axis uses a binary logarithmic scale](/media/best-practices/default-axes-scale.jpg)

Y軸を線形スケールに切り替えます。

![Switch to a linear scale](/media/best-practices/axes-scale-linear.jpg)

> **ヒント：**
>
> ヒント2とヒント1を組み合わせると、 `SELECT`ステートメントまたは`UPDATE`ステートメントのどちらが遅いかをすぐに分析するのに役立つ`sql_type`の次元を見つけることができます。遅いSQLステートメントでインスタンスを見つけることもできます。

### ヒント3：Y軸のベースラインを変更して、変更を増幅します {#tip-3-modify-the-baseline-of-the-y-axis-to-amplify-changes}

線形スケールに切り替えた後でも、トレンドが表示されない場合があります。たとえば、次の図では、クラスタをスケーリングした後に`Store size`のリアルタイムの変化を観察する必要がありますが、ベースラインが大きいため、小さな変化は表示されません。この状況では、Y軸のベースラインを`0`から`auto`に変更して、上部を拡大できます。以下の2つの図を確認すると、データ移行が開始されていることがわかります。

ベースラインのデフォルトは`0`です。

![Baseline defaults to 0](/media/best-practices/default-y-min.jpeg)

ベースラインを`auto`に変更します。

![Change the baseline to auto](/media/best-practices/y-min-auto.jpg)

### ヒント4：共有十字線またはツールチップを使用する {#tip-4-use-shared-crosshair-or-tooltip}

**[設定]**パネルには、デフォルトで[<strong>デフォルト</strong>]に設定されている<strong>グラフツールチップ</strong>パネルオプションがあります。

![Graphic presentation tools](/media/best-practices/graph-tooltip.jpeg)

次の図に示すように、**共有十字線**と<strong>共有ツールチップ</strong>をそれぞれ使用して、効果をテストできます。次に、スケールがリンクして表示されます。これは、問題を診断するときに2つのメトリックの相関関係を確認するのに便利です。

グラフィックプレゼンテーションツールを**共有十字線**に設定します。

![Set the graphical presentation tool to Shared crosshair](/media/best-practices/graph-tooltip-shared-crosshair.jpeg)

グラフィックプレゼンテーションツールを**共有ツールチップ**に設定します。

![Set the graphic presentation tool to Shared Tooltip](/media/best-practices/graph-tooltip-shared-tooltip.jpg)

### ヒント5： <code>IP address:port number</code>を入力して、履歴のメトリックを確認します {#tip-5-enter-code-ip-address-port-number-code-to-check-the-metrics-in-history}

PDのダッシュボードには、現在のリーダーの指標のみが表示されます。履歴内のPDリーダーのステータスを確認したいが、 `instance`フィールドのドロップダウンリストに存在しなくなった場合は、手動で`IP address:2379`を入力して、リーダーのデータを確認できます。

![Check the metrics in history](/media/best-practices/manually-input-check-metric.jpeg)

### ヒント6： <code>Avg</code>関数を使用する {#tip-6-use-the-code-avg-code-function}

通常、凡例ではデフォルトで`Max`つと`Current`の関数のみが使用可能です。メトリックが大きく変動する場合は、 `Avg`関数などの他の要約関数を凡例に追加して、一定期間の全体的な傾向を確認できます。

`Avg`関数を追加します。

![Add summary functions such as Avg](/media/best-practices/add-avg-function.jpeg)

次に、全体的な傾向を確認します。

![Add Avg function to check the overall trend](/media/best-practices/add-avg-function-check-trend.jpg)

### ヒント7：PrometheusのAPIを使用して、クエリ式の結果を取得します {#tip-7-use-the-api-of-prometheus-to-obtain-the-result-of-query-expressions}

GrafanaはPrometheusのAPIを介してデータを取得し、このAPIを使用して情報を取得することもできます。さらに、次の使用法もあります。

-   クラスタのサイズやステータスなどの情報を自動的に取得します。
-   1日あたりのQPSの合計量、1日あたりのQPSのピーク値、1日あたりの応答時間など、レポートの情報を提供するために式に小さな変更を加えます。
-   重要なメトリクスに対して定期的なヘルスインスペクションを実行します。

PrometheusのAPIは次のように表示されます。

![The API of Prometheus](/media/best-practices/prometheus-api-interface.jpg)

{{< copyable "" >}}

```bash
curl -u user:pass 'http://__grafana_ip__:3000/api/datasources/proxy/1/api/v1/query_range?query=sum(tikv_engine_size_bytes%7Binstancexxxxxxxxx20181%22%7D)%20by%20(instance)&start=1565879269&end=1565882869&step=30' |python -m json.tool
```

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
```

## 概要 {#summary}

Grafana+Prometheusモニタリングプラットフォームは非常に強力なツールです。これをうまく利用すると、効率が向上し、TiDBクラスタのステータスを分析する時間を大幅に節約できます。さらに重要なことに、問題の診断に役立ちます。このツールは、特に大量のデータがある場合に、TiDBクラスターの操作と保守に非常に役立ちます。
