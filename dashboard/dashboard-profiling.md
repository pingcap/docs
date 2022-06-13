---
title: TiDB Dashboard Instance Profiling - Manual Profiling
summary: Learn how to collect performance data to analyze sophisticated problems.
---

# TiDBダッシュボードインスタンスプロファイリング-手動プロファイリング {#tidb-dashboard-instance-profiling-manual-profiling}

> **ノート：**
>
> この機能は、データベースの専門家向けに設計されています。専門家でないユーザーの場合は、PingCAPテクニカルサポートの指導の下でこの機能を使用することをお勧めします。

手動プロファイリングにより、ユーザーはシングルクリックで各TiDB、TiKV、PD、およびTiFlashインスタンスの現在のパフォーマンスデータ**をオンデマンド**で収集できます。収集されたパフォーマンスデータは、FlameGraphまたはDAGとして視覚化できます。

これらのパフォーマンスデータを使用して、専門家はインスタンスのCPUやメモリなどの現在のリソース消費の詳細を分析し、CPUオーバーヘッドの高さ、メモリ使用量の高さ、プロセスのストールなど、進行中の高度なパフォーマンスの問題を特定できます。

プロファイリングを開始した後、TiDBダッシュボードは一定期間（デフォルトでは30秒）の現在のパフォーマンスデータを収集します。したがって、この機能は、クラスタが現在直面している進行中の問題を分析するためにのみ使用でき、履歴の問題には大きな影響を与えません。**いつでも**パフォーマンスデータを収集して分析する場合は、 [継続的なプロファイリング](/dashboard/continuous-profiling.md)を参照してください。

## サポートされているパフォーマンスデータ {#supported-performance-data}

現在、次のパフォーマンスデータがサポートされています。

-   CPU：TiDB、TiKV、PD、およびTiFlashインスタンスの各内部機能のCPUオーバーヘッド

    > TiKVおよびTiFlashインスタンスのCPUオーバーヘッドは、現在ARMアーキテクチャではサポートされていません。

-   ヒープ：TiDBおよびPDインスタンスの各内部関数のメモリ消費量

-   ミューテックス：TiDBおよびPDインスタンスでのミューテックス競合状態

-   Goroutine：TiDBおよびPDインスタンス上のすべてのgoroutineの実行状態と呼び出しスタック

## ページにアクセスする {#access-the-page}

次のいずれかの方法を使用して、インスタンスプロファイリングページにアクセスできます。

-   TiDBダッシュボードにログインした後、左側のナビゲーションバーで[**高度なデバッグ**]&gt;[<strong>インスタンスのプロファイリング</strong>]&gt;[<strong>手動プロファイリング</strong>]をクリックします。

    ![Access instance profiling page](/media/dashboard/dashboard-profiling-access.png)

-   ブラウザで[http://127.0.0.1:2379/dashboard/#/instance_profiling](http://127.0.0.1:2379/dashboard/#/instance_profiling)にアクセスします。 `127.0.0.1:2379`を実際のPDインスタンスのアドレスとポートに置き換えます。

## プロファイリングを開始します {#start-profiling}

インスタンスプロファイリングページで、少なくとも1つのターゲットインスタンスを選択し、[**プロファイリング**の開始]をクリックしてインスタンスプロファイリングを開始します。

![Start instance profiling](/media/dashboard/dashboard-profiling-start.png)

プロファイリングを開始する前に、プロファイリング期間を変更できます。この期間は、プロファイリングに必要な時間によって決定されます。デフォルトでは30秒です。 30秒の期間は、完了するのに30秒かかります。

[継続的なプロファイリング](/dashboard/continuous-profiling.md)が有効になっているクラスターでは、手動プロファイリングを開始できません。現時点でのパフォーマンスデータを表示するには、 [継続的なプロファイリングページ](/dashboard/continuous-profiling.md#access-the-page)の最新のプロファイリング結果をクリックします。

## プロファイリングステータスの表示 {#view-profiling-status}

プロファイリングが開始されると、プロファイリングのステータスと進行状況をリアルタイムで表示できます。

![Profiling detail](/media/dashboard/dashboard-profiling-view-progress.png)

プロファイリングはバックグラウンドで実行されます。現在のページを更新または終了しても、実行中のプロファイリングタスクは停止しません。

## パフォーマンスデータをダウンロードする {#download-performance-data}

すべてのインスタンスのプロファイリングが完了したら、右上隅にある[**プロファイリング結果のダウンロード**]をクリックして、すべてのパフォーマンスデータをダウンロードできます。

![Download profiling result](/media/dashboard/dashboard-profiling-download.png)

テーブル内の個々のインスタンスをクリックして、そのプロファイリング結果を表示することもできます。または、...にカーソルを合わせて生データをダウンロードすることもできます。

![Single instance result](/media/dashboard/dashboard-profiling-view-single.png)

## プロファイリング履歴を表示する {#view-profiling-history}

オンデマンドのプロファイリング履歴がページに一覧表示されます。行をクリックして詳細を表示します。

![View profiling history](/media/dashboard/dashboard-profiling-history.png)

プロファイリングステータスページの詳細な操作については、 [プロファイリングステータスの表示](#view-profiling-status)を参照してください。
