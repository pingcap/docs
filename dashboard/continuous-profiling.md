---
title: TiDB Dashboard Instance Profiling - Continuous Profiling
summary: Learn how to collect performance data from TiDB, TiKV and PD continuously to reduce MTTR.
---

# TiDB ダッシュボード インスタンス プロファイリング - 継続的プロファイリング {#tidb-dashboard-instance-profiling-continuous-profiling}

> **注記：**
>
> この機能はデータベースの専門家向けに設計されています。専門家以外のユーザーの場合は、PingCAP テクニカル サポートの指導の下でこの機能を使用することをお勧めします。

継続的プロファイリングにより、各 TiDB、TiKV、PD インスタンスからパフォーマンス データを**継続的に**収集できます。収集されたパフォーマンス データは、FlameGraph または DAG として視覚化できます。

これらのパフォーマンス データを使用して、専門家はインスタンスの CPU やメモリなどのリソース消費の詳細を分析し、高い CPU オーバーヘッド、高いメモリ使用量、プロセスの停止などの高度なパフォーマンスの問題をいつでも特定できるようになります。再現できない問題であっても、専門家はその時点で収集された履歴パフォーマンス データを表示することで、問題を深く掘り下げることができます。このようにして、MTTR を効果的に削減できます。

## 手動プロファイリングとの比較 {#compare-with-manual-profiling}

継続的プロファイリングは[手動プロファイリング](/dashboard/dashboard-profiling.md)の拡張機能です。どちらも、インスタンスごとにさまざまな種類のパフォーマンス データを収集および分析するために使用できます。それらの違いは次のとおりです。

-   手動プロファイリングは、プロファイリングを開始した瞬間の短期間 (たとえば、30 秒) のパフォーマンス データのみを収集しますが、継続的プロファイリングは、有効にすると継続的にデータを収集します。
-   手動プロファイリングは現在発生している問題の分析にのみ使用できますが、継続プロファイリングは現在の問題と過去の問題の両方を分析するために使用できます。
-   手動プロファイリングでは特定のインスタンスの特定のパフォーマンス データを収集できますが、継続的プロファイリングではすべてのインスタンスのすべてのパフォーマンス データが収集されます。
-   継続的プロファイリングはより多くのパフォーマンス データを保存するため、より多くのディスク領域を消費します。

## サポートされているパフォーマンスデータ {#supported-performance-data}

[手動プロファイリング](/dashboard/dashboard-profiling.md#supported-performance-data)のすべてのパフォーマンスデータが収集されます。

-   CPU: TiDB、TiKV、 TiFlash、PD インスタンスの各内部関数の CPU オーバーヘッド

-   ヒープ: TiDB および PD インスタンスの各内部関数のメモリ消費量

-   Mutex: TiDB および PD インスタンスのミューテックス競合状態

-   Goroutine: TiDB および PD インスタンス上のすべての Goroutine の実行状態とコール スタック

## ページにアクセスする {#access-the-page}

次のいずれかの方法を使用して、「継続的プロファイリング」ページにアクセスできます。

-   TiDB ダッシュボードにログインした後、左側のナビゲーション メニューで**[高度なデバッグ**] &gt; **[プロファイリング インスタンス]** &gt; **[継続的プロファイリング]**をクリックします。

    ![Access page](/media/dashboard/dashboard-conprof-access.png)

-   ブラウザで[http://127.0.0.1:2379/dashboard/#/continuous_profiling](http://127.0.0.1:2379/dashboard/#/continuous_profiling)にアクセスしてください。 `127.0.0.1:2379`を実際の PD インスタンスのアドレスとポートに置き換えます。

## 継続的プロファイリングを有効にする {#enable-continuous-profiling}

> **注記：**
>
> 継続的プロファイリングを使用するには、クラスターを最新バージョンのTiUP (v1.9.0 以降) またはTiDB Operator (v1.3.0 以降) でデプロイまたはアップグレードする必要があります。クラスターが以前のバージョンのTiUPまたはTiDB Operatorを使用してアップグレードされた場合、手順については[FAQ](/dashboard/dashboard-faq.md#a-required-component-ngmonitoring-is-not-started-error-is-shown)を参照してください。

継続的プロファイリングを有効にすると、Web ページを常にアクティブにしておくことなく、バックグラウンドでパフォーマンス データを継続的に収集できます。収集されたデータは一定期間保存でき、期限切れのデータは自動的に消去されます。

この機能を有効にするには:

1.  [継続的プロファイリングページ](#access-the-page)にアクセスしてください。
2.  **[設定を開く]**をクリックします。右側の**設定**領域で、**機能の有効化**をオンにし、必要に応じて**保存期間**のデフォルト値を変更します。
3.  **「保存」**をクリックします。

![Enable feature](/media/dashboard/dashboard-conprof-start.png)

## 現在のパフォーマンス データをビュー {#view-current-performance-data}

継続的プロファイリングが有効になっているクラスターでは手動プロファイリングを開始できません。現時点でのパフォーマンス データを表示するには、最新のプロファイリング結果をクリックするだけです。

## 過去のパフォーマンス データをビュー {#view-historical-performance-data}

リスト ページでは、この機能を有効にしてから収集されたすべてのパフォーマンス データを確認できます。

![History results](/media/dashboard/dashboard-conprof-history.png)

## パフォーマンスデータのダウンロード {#download-performance-data}

プロファイリング結果ページで、右上隅にある**[プロファイリング結果のダウンロード]**をクリックして、すべてのプロファイリング結果をダウンロードできます。

![Download profiling result](/media/dashboard/dashboard-conprof-download.png)

テーブル内の個々のインスタンスをクリックして、そのプロファイリング結果を表示することもできます。または、... にカーソルを合わせると、生データをダウンロードできます。

![View profiling result](/media/dashboard/dashboard-conprof-single.png)

## 継続的プロファイリングを無効にする {#disable-continuous-profiling}

1.  [継続的プロファイリングページ](#access-the-page)にアクセスしてください。
2.  右上隅にある歯車アイコンをクリックして設定ページを開きます。 **「機能の有効化」**をオフに切り替えます。
3.  **「保存」**をクリックします。
4.  ポップアップダイアログボックスで、 **「無効にする」**をクリックします。

![Disable feature](/media/dashboard/dashboard-conprof-stop.png)

## よくある質問 {#frequently-asked-questions}

**1. 継続的プロファイリングを有効にできず、UI に「必須コンポーネントNgMonitoring が開始されていません」と表示されます**。

[TiDB ダッシュボードFAQ](/dashboard/dashboard-faq.md#a-required-component-ngmonitoring-is-not-started-error-is-shown)を参照してください。

**2. 継続的プロファイリングを有効にした後、パフォーマンスは影響を受けますか?**

弊社のベンチマークによると、この機能が有効になっている場合の平均パフォーマンスへの影響は 1% 未満です。

**3. この機能のステータスはどうなっていますか?**

現在、一般提供 (GA) 機能となっており、本番環境で使用できます。
