---
title: TiDB Dashboard Instance Profiling - Manual Profiling
summary: Learn how to collect performance data to analyze sophisticated problems.
---

# TiDB ダッシュボード インスタンスのプロファイリング - 手動プロファイリング {#tidb-dashboard-instance-profiling-manual-profiling}

> **ノート：**
>
> この機能は、データベースの専門家向けに設計されています。専門家以外のユーザーには、PingCAP テクニカル サポートの指導の下でこの機能を使用することをお勧めします。

手動プロファイリングにより、ユーザーはワンクリックで各 TiDB、TiKV、PD、およびTiFlashインスタンスの現在のパフォーマンス データを**オンデマンド**で収集できます。収集されたパフォーマンス データは、FlameGraph または DAG として視覚化できます。

これらのパフォーマンス データを使用して、専門家はインスタンスの CPU やメモリなどの現在のリソース消費の詳細を分析し、高い CPU オーバーヘッド、高いメモリ使用量、プロセス ストールなどの進行中の高度なパフォーマンスの問題を特定するのに役立ちます。

プロファイリングを開始した後、TiDB ダッシュボードは現在のパフォーマンス データを一定期間 (デフォルトでは 30 秒) 収集します。したがって、この機能は、クラスターが現在直面している進行中の問題を分析するためにのみ使用でき、過去の問題には大きな影響を与えません。**いつでも**パフォーマンス データを収集して分析したい場合は、 [継続的なプロファイリング](/dashboard/continuous-profiling.md)を参照してください。

## 対応実績データ {#supported-performance-data}

現在、次のパフォーマンス データがサポートされています。

-   CPU: TiDB、TiKV、PD、およびTiFlashインスタンスの各内部関数の CPU オーバーヘッド

    > TiKV およびTiFlashインスタンスの CPU オーバーヘッドは、現在 ARMアーキテクチャではサポートされていません。

-   ヒープ: TiDB および PD インスタンスの各内部関数のメモリ消費量

-   Mutex: TiDB および PD インスタンスでのミューテックスの競合状態

-   Goroutine: TiDB および PD インスタンス上のすべての goroutine の実行状態とコール スタック

## ページにアクセスする {#access-the-page}

次のいずれかの方法を使用して、インスタンス プロファイリング ページにアクセスできます。

-   TiDB ダッシュボードにログインした後、左側のナビゲーション バーで**[Advanced Debugging]** &gt; <strong>[Profiling Instances]</strong> &gt; <strong>[Manual Profiling]</strong>をクリックします。

    ![Access instance profiling page](/media/dashboard/dashboard-profiling-access.png)

-   ブラウザで[http://127.0.0.1:2379/dashboard/#/instance_profiling](http://127.0.0.1:2379/dashboard/#/instance_profiling)にアクセスします。 `127.0.0.1:2379`を実際の PD インスタンスのアドレスとポートに置き換えます。

## プロファイリングを開始 {#start-profiling}

インスタンスのプロファイリング ページで、少なくとも 1 つのターゲット インスタンスを選択し、 **[プロファイリングの開始]**をクリックしてインスタンスのプロファイリングを開始します。

![Start instance profiling](/media/dashboard/dashboard-profiling-start.png)

プロファイリングを開始する前に、プロファイリング期間を変更できます。この期間は、プロファイリングに必要な時間によって決まります。デフォルトでは 30 秒です。 30 秒間の継続時間は、完了するまでに 30 秒かかります。

[継続的なプロファイリング](/dashboard/continuous-profiling.md)が有効になっているクラスターでは、手動プロファイリングを開始できません。現時点でのパフォーマンス データを表示するには、 [継続的なプロファイリング ページ](/dashboard/continuous-profiling.md#access-the-page)で最新のプロファイリング結果をクリックします。

## プロファイリング ステータスのビュー {#view-profiling-status}

プロファイリングが開始されると、プロファイリングのステータスと進行状況をリアルタイムで表示できます。

![Profiling detail](/media/dashboard/dashboard-profiling-view-progress.png)

プロファイリングはバックグラウンドで実行されます。現在のページを更新または終了しても、実行中のプロファイリング タスクは停止しません。

## 性能データのダウンロード {#download-performance-data}

すべてのインスタンスのプロファイリングが完了したら、右上隅にある**[プロファイル結果のダウンロード]**をクリックして、すべてのパフォーマンス データをダウンロードできます。

![Download profiling result](/media/dashboard/dashboard-profiling-download.png)

テーブル内の個々のインスタンスをクリックして、そのプロファイリング結果を表示することもできます。または、... にカーソルを合わせて生データをダウンロードすることもできます。

![Single instance result](/media/dashboard/dashboard-profiling-view-single.png)

## プロファイリング履歴をビュー {#view-profiling-history}

オンデマンド プロファイリングの履歴がページに一覧表示されます。行をクリックして詳細を表示します。

![View profiling history](/media/dashboard/dashboard-profiling-history.png)

プロファイリング ステータス ページの詳細な操作については、 [プロファイリング ステータスのビュー](#view-profiling-status)を参照してください。
