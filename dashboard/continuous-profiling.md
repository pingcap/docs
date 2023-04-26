---
title: TiDB Dashboard Instance Profiling - Continuous Profiling
summary: Learn how to collect performance data from TiDB, TiKV and PD continuously to reduce MTTR.
---

# TiDB ダッシュボード インスタンスのプロファイリング - 継続的なプロファイリング {#tidb-dashboard-instance-profiling-continuous-profiling}

> **ノート：**
>
> この機能は、データベースの専門家向けに設計されています。専門家以外のユーザーには、PingCAP テクニカル サポートの指導の下でこの機能を使用することをお勧めします。

継続的なプロファイリングにより、各 TiDB、TiKV、および PD インスタンスから**継続的に**パフォーマンス データを収集できます。収集されたパフォーマンス データは、FlameGraph または DAG として視覚化できます。

これらのパフォーマンス データを使用して、専門家はインスタンスの CPU やメモリなどのリソース消費の詳細を分析し、高い CPU オーバーヘッド、高いメモリ使用量、プロセス ストールなどの高度なパフォーマンスの問題をいつでも特定できます。再現できない問題でも、専門家はその時点で収集された過去のパフォーマンス データを参照することで、問題を深く掘り下げることができます。このようにして、MTTRを効果的に削減できます。

## 手動プロファイリングとの比較 {#compare-with-manual-profiling}

連続プロファイリングは[手動プロファイリング](/dashboard/dashboard-profiling.md)の拡張機能です。どちらも、インスタンスごとにさまざまな種類のパフォーマンス データを収集および分析するために使用できます。それらの違いは次のとおりです。

-   手動プロファイリングは、プロファイリングを開始した時点で短時間 (たとえば 30 秒) のパフォーマンス データのみを収集しますが、継続的プロファイリングは、有効にすると継続的にデータを収集します。
-   手動プロファイリングは、現在発生している問題の分析にのみ使用できますが、継続的プロファイリングは、現在および過去の問題の両方の分析に使用できます。
-   手動プロファイリングでは、特定のインスタンスの特定のパフォーマンス データを収集できますが、継続的プロファイリングでは、すべてのインスタンスのすべてのパフォーマンス データを収集できます。
-   継続的プロファイリングはより多くのパフォーマンス データを保存するため、より多くのディスク領域を占有します。

## 対応実績データ {#supported-performance-data}

[手動プロファイリング](/dashboard/dashboard-profiling.md#supported-performance-data)のすべてのパフォーマンス データが収集されます。

-   CPU: TiDB、TiKV、 TiFlash、および PD インスタンスの各内部関数の CPU オーバーヘッド

-   ヒープ: TiDB および PD インスタンスの各内部関数のメモリ消費量

-   Mutex: TiDB および PD インスタンスでのミューテックスの競合状態

-   Goroutine: TiDB および PD インスタンス上のすべての goroutine の実行状態とコール スタック

## ページにアクセスする {#access-the-page}

次のいずれかの方法を使用して、Continuous Profiling ページにアクセスできます。

-   TiDB ダッシュボードにログインした後、左側のナビゲーション バーで**[Advanced Debugging** ] &gt; <strong>[Profiling Instances]</strong> &gt; <strong>[Continuous Profiling]</strong>をクリックします。

    ![Access page](/media/dashboard/dashboard-conprof-access.png)

-   ブラウザで[http://127.0.0.1:2379/dashboard/#/continuous_profiling](http://127.0.0.1:2379/dashboard/#/continuous_profiling)にアクセスします。 `127.0.0.1:2379`を実際の PD インスタンスのアドレスとポートに置き換えます。

## 継続的なプロファイリングを有効にする {#enable-continuous-profiling}

> **ノート：**
>
> 継続的プロファイリングを使用するには、 TiUP (v1.9.0 以降) またはTiDB Operator (v1.3.0 以降) の最新バージョンを使用してクラスターをデプロイまたはアップグレードする必要があります。以前のバージョンのTiUPまたはTiDB Operatorを使用してクラスターをアップグレードした場合は、手順について[FAQ](/dashboard/dashboard-faq.md#a-required-component-ngmonitoring-is-not-started-error-is-shown)を参照してください。

継続的なプロファイリングを有効にすると、Web ページを常にアクティブにしなくても、パフォーマンス データをバックグラウンドで継続的に収集できます。収集したデータは一定期間保持でき、期限切れのデータは自動的に消去されます。

この機能を有効にするには:

1.  [継続的なプロファイリング ページ](#access-the-page)ご覧ください。
2.  **[設定を開く]**をクリックします。右側の<strong>[設定]</strong>領域で、 <strong>[機能を有効にする</strong>] をオンにし、必要に応じて<strong>[保持期間]</strong>のデフォルト値を変更します。
3.  **[保存]**をクリックします。

![Enable feature](/media/dashboard/dashboard-conprof-start.png)

## 現在のパフォーマンス データをビュー {#view-current-performance-data}

手動プロファイリングは、継続的プロファイリングが有効になっているクラスターでは開始できません。現時点でのパフォーマンス データを表示するには、最新のプロファイリング結果をクリックします。

## 過去のパフォーマンス データをビュー {#view-historical-performance-data}

リスト ページでは、この機能を有効にしてから収集されたすべてのパフォーマンス データを確認できます。

![History results](/media/dashboard/dashboard-conprof-history.png)

## 性能データのダウンロード {#download-performance-data}

プロファイリング結果ページで、右上隅にある**[プロファイリング結果のダウンロード]**をクリックして、すべてのプロファイリング結果をダウンロードできます。

![Download profiling result](/media/dashboard/dashboard-conprof-download.png)

テーブル内の個々のインスタンスをクリックして、そのプロファイリング結果を表示することもできます。または、... にカーソルを合わせて生データをダウンロードすることもできます。

![View profiling result](/media/dashboard/dashboard-conprof-single.png)

## 継続的なプロファイリングを無効にする {#disable-continuous-profiling}

1.  [継続的なプロファイリング ページ](#access-the-page)ご覧ください。
2.  右上隅の歯車アイコンをクリックして、設定ページを開きます。**機能の有効化**をオフに切り替えます。
3.  **[保存]**をクリックします。
4.  表示されたダイアログ ボックスで、 **[無効にする]**をクリックします。

![Disable feature](/media/dashboard/dashboard-conprof-stop.png)

## よくある質問 {#frequently-asked-questions}

**1. 継続的なプロファイリングを有効にできず、UI に「必要なコンポーネントNgMonitoring が開始されていません」と表示されます**。

[TiDB ダッシュボードFAQ](/dashboard/dashboard-faq.md#a-required-component-ngmonitoring-is-not-started-error-is-shown)を参照してください。

**2. 継続的プロファイリングを有効にした後、パフォーマンスは影響を受けますか?**

ベンチマークによると、この機能が有効になっている場合の平均パフォーマンスへの影響は 1% 未満です。

**3. この機能のステータスは?**

これは現在、一般提供 (GA) 機能であり、本番環境で使用できます。
