---
title: Statement Insight (PREVIEW)
summary: Statement Insight を使用して、DB user、DB、table、SQL type、または SQL digest ごとの過去の RU 消費量、レイテンシー、実行回数を分析し、TiDB Cloud インスタンスの RU およびパフォーマンスのベースラインを構築する方法を説明します。
---

# Statement Insight (PREVIEW)

**Statement Insight** は、<CustomContent plan="premium">{{{ .premium }}}</CustomContent><CustomContent plan="byoc">{{{ .premium }}} and {{{ .byoc }}}</CustomContent> インスタンス向けに、SQL リソース消費の多次元分析を提供します。Request Unit (RU) の消費量、レイテンシー、実行回数を **DB User**、**DB**、**Table**、**SQL Type**、または **SQL Digest** ごとに分類し、リーダーボードとトレンドチャートによって、主要な要因をひと目で把握できます。Statement Insight を使用すると、過去データから RU とパフォーマンスのベースラインを確立し、RU 消費や処理遅延の原因を特定できます。

Statement Insight は、履歴データに基づいてベースラインを把握するためのビューです。 

> **Note:**
>
> Statement Insight はパブリックプレビュー中であり、8 月 19 日以降に作成された一部の <CustomContent plan="premium">{{{ .premium }}}</CustomContent><CustomContent plan="byoc">{{{ .premium }}} and {{{ .byoc }}}</CustomContent> インスタンスでのみ利用できます。今後のリリースで、より広範囲に展開される予定です。早期アクセスを希望する場合は、[TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。
> Statement Insight がまだ利用できないインスタンスでは、当面の間、ステートメント分析に [SQL Statement](/tidb-cloud/tune-performance.md#statement-analysis) タブを引き続き使用できます。

## 始める前に {#before-you-begin}

Statement Insight は、インスタンスで有効化された後にのみデータ収集を開始するため、初めてページを開く際は次の点に注意してください。

- 過去データは補完されません。表示されるのは、この機能がインスタンスで有効化された時点以降のデータのみです。
- 利用可能な時間範囲は日ごとに増えていきます。たとえば、機能の稼働開始から 1 日後には、約 1 日分のデータが表示されます。

## Statement Insight を開く {#open-statement-insight}

1. [TiDB Cloud console](https://tidbcloud.com/) にログインし、<CustomContent plan="premium">{{{ .premium }}}</CustomContent><CustomContent plan="byoc">{{{ .premium }}} or {{{ .byoc }}}</CustomContent> インスタンスに移動します。
2. 左側のナビゲーションペインで、**Monitoring** > **Diagnosis** をクリックします。
3. **Diagnosis** ページで、**Statement Insight** タブをクリックします。

## フィルターを設定する {#set-filters}

ページ上部のフィルターを使用して、データを絞り込みます。

- **Time range**: プリセットの期間またはカスタム範囲を選択します。
- **DB User**: SQL ステートメントを実行したデータベースユーザーで絞り込みます。 
- **SQL Type**: `SELECT`、`INSERT`、`UPDATE` などの SQL ステートメント種別で絞り込みます。
- **Database**: SQL ステートメントの実行対象となったデータベースで絞り込みます。
- **Table**: SQL ステートメントの実行対象となったテーブルで絞り込みます。
- **Keyword**: SQL digest テキストに一致するキーワードで絞り込みます。

すべてのフィルターは組み合わせて使用でき、分析対象を必要な SQL ステートメントに絞り込めます。

## RU 消費量、レイテンシー、実行回数を分析する {#analyze-ru-consumption-latency-and-execution-counts}

**Top Contributors** パネルには、フィルター条件に一致する SQL ステートメントの概要が、複数の次元ごとに表示されます。各次元では、**Measured by** コントロールを切り替えることで、リーダーボードとトレンドチャートの両方で使用する指標を変更できます。

- **Total RU**: 消費された RU の合計。
- **Mean RU**: 総 RU を実行回数で割った値。
- **Total latency**: 実行レイテンシーの合計。
- **Mean latency**: 総レイテンシーを実行回数で割った値。
- **Execution count**: SQL ステートメントが実行された回数。

### DB user、SQL type、SQL digest、DB、table ごとの主要な要因 {#top-contributors-by-db-user-sql-type-sql-digest-db-and-table}

各次元（DB User、SQL Type、SQL Digest、DB、または Table）について、パネルには次の情報が表示されます。

- **Total count**: 選択した SQL ステートメントの中で、その次元における異なる値の総数。たとえば、選択した SQL ステートメントを実行した異なる DB user の総数です。
- **Top values**: **Measured by** で選択した指標に基づく上位の値。たとえば、**Measured by** が **Total RU** に設定されている場合、最も多くの RU を消費した DB user、SQL type、SQL digest、DB、または Table が表示されます。

### トレンドチャート {#trend-charts}

**Resource Usage Over Time** トレンドチャートには、表示中の次元について、選択した指標が時間の経過とともにどのように変化するかが示されます。

## 制限事項 {#limitations}

- Statement Insight は、履歴分析および RU またはパフォーマンスのベースライン作成を目的としています。データ収集方法と集計方法の違いにより、表示される RU は TiDB Cloud 請求書に記載される RU 使用量とは異なります（Statement Insight では累積 RU 消費量を表示します）。請求額の照合に Statement Insight のデータを使用しないでください。
- データの更新間隔は最大 **10 minutes** で、基盤となる収集サイクルに一致します。

## FAQ {#faq}

### Statement Insight にデータが表示されない、または短い期間のデータしか表示されないのはなぜですか？ {#why-is-there-no-data-or-only-a-short-time-range-of-data-in-statement-insight}

Statement Insight は過去データを補完しません。データは、この機能がインスタンスで有効化された時点から蓄積され始め、利用可能な時間範囲は時間の経過とともに広がります。インスタンスでこの機能が最近有効化された場合、これは想定どおりの動作であり、データの欠落や障害を意味するものではありません。

### Statement Insight と Top RU の違いは何ですか？ {#what-is-the-difference-between-statement-insight-and-top-ru}

[Top RU](/tidb-cloud/top-ru.md) は、進行中の RU スパイクを診断するためのほぼリアルタイムのツールです。短い直近の時間枠において、累積 RU 消費量で SQL ステートメントを順位付けし、現在も実行中のステートメントを含め、RU を最も多く消費している SQL ステートメントと主要フィールドに焦点を当てます。

Statement Insight は履歴分析ツールです。より多くの SQL ステートメント（収集間隔ごとに最大 3,000 SQL digests）を、より詳細なフィールドとともに収集・表示し、DB User、SQL Type、SQL Digest、DB、または Table ごとに分類された、より長い期間にわたる RU 消費量、レイテンシー、実行回数の傾向を把握するのに役立ちます。これにより、RU とパフォーマンスのベースラインを確立し、継続的な最適化の機会を特定できます。

### Statement Insight に表示される RU は、請求対象の RU と同じですか？ {#is-the-ru-shown-in-statement-insight-the-same-as-the-billed-ru}

いいえ。Statement Insight は、請求ではなく、可観測性と最適化を目的としています。請求およびコスト管理については、TiDB Cloud の請求コンソールを参照してください。