---
title: TiDB Dashboard Instance Profiling - Manual Profiling
summary: Manual Profiling allows users to collect current performance data on demand for TiDB, TiKV, PD, and TiFlash instances. Experts can analyze resource consumption details like CPU and memory to pinpoint ongoing performance problems. Access the page through TiDB Dashboard or a browser. Start profiling by choosing target instances and modify the duration if needed. View real-time progress and download performance data after profiling is completed. View profiling history for detailed operations.
---

# TiDB ダッシュボード インスタンス プロファイリング - 手動プロファイリング {#tidb-dashboard-instance-profiling-manual-profiling}

> **注記：**
>
> この機能はデータベースの専門家向けに設計されています。専門家でないユーザーは、PingCAP テクニカル サポートの指導の下でこの機能を使用することをお勧めします。

手動プロファイリングを使用すると、ユーザーは 1 回のクリックで、TiDB、TiKV、PD、およびTiFlashインスタンスごと**に現在のパフォーマンス データをオンデマンドで**収集できます。収集されたパフォーマンス データは、FlameGraph または DAG として視覚化できます。

これらのパフォーマンス データを使用すると、専門家はインスタンスの CPU やメモリなどの現在のリソース消費の詳細を分析し、CPU オーバーヘッドの高さ、メモリ使用量の高さ、プロセスの停止など、進行中の高度なパフォーマンスの問題を正確に特定できます。

プロファイリングを開始すると、TiDB ダッシュボードは一定期間 (デフォルトでは 30 秒) にわたって現在のパフォーマンス データを収集します。したがって、この機能はクラスターが現在直面している進行中の問題を分析するためにのみ使用でき、過去の問題には大きな影響はありません。**いつでも**パフォーマンス データを収集して分析したい場合は、 [継続的なプロファイリング](/dashboard/continuous-profiling.md)を参照してください。

## サポートされているパフォーマンスデータ {#supported-performance-data}

現在、次のパフォーマンス データがサポートされています。

-   CPU: TiDB、TiKV、PD、 TiFlashインスタンス上の各内部関数のCPUオーバーヘッド

    > TiKV およびTiFlashインスタンスの CPU オーバーヘッドは、現在 ARMアーキテクチャではサポートされていません。

-   ヒープ: TiDB、TiKV、PDインスタンス上の各内部関数のメモリ消費量

    > v7.5 以降、TiDB は TiKV ヒープ プロファイルをサポートします。TiDB ダッシュボードの実行環境では Perl 依存関係が必要です。そうでない場合はエラーが発生します。

-   ミューテックス: TiDBおよびPDインスタンス上のミューテックスの競合状態

-   Goroutine: TiDB および PD インスタンス上のすべての Goroutine の実行状態と呼び出しスタック

## ページにアクセスする {#access-the-page}

次のいずれかの方法でインスタンス プロファイリング ページにアクセスできます。

-   TiDB ダッシュボードにログインした後、左側のナビゲーション メニューで**[高度なデバッグ]** &gt; **[インスタンスのプロファイリング]** &gt; **[手動プロファイリング]**をクリックします。

    ![Access instance profiling page](/media/dashboard/dashboard-profiling-access.png)

-   ブラウザで[http://127.0.0.1:2379/ダッシュボード/#/インスタンスプロファイリング](http://127.0.0.1:2379/dashboard/#/instance_profiling)アクセスします。3 `127.0.0.1:2379`実際の PD インスタンスのアドレスとポートに置き換えます。

## プロファイリングを開始 {#start-profiling}

インスタンス プロファイリング ページで、少なくとも 1 つのターゲット インスタンスを選択し、 **[プロファイリングの開始]**をクリックしてインスタンス プロファイリングを開始します。

![Start instance profiling](/media/dashboard/dashboard-profiling-start.png)

プロファイリングを開始する前に、プロファイリング期間を変更できます。この期間は、プロファイリングに必要な時間によって決まります。デフォルトでは 30 秒です。30 秒の期間は、完了するまでに 30 秒かかります。

[継続的なプロファイリング](/dashboard/continuous-profiling.md)が有効になっているクラスターでは手動プロファイリングを開始できません。現時点でのパフォーマンス データを表示するには、 [継続的プロファイリングページ](/dashboard/continuous-profiling.md#access-the-page)で最新のプロファイリング結果をクリックします。

## プロファイリングステータスのビュー {#view-profiling-status}

プロファイリングが開始されると、プロファイリングのステータスと進行状況をリアルタイムで確認できます。

![Profiling detail](/media/dashboard/dashboard-profiling-view-progress.png)

プロファイリングはバックグラウンドで実行されます。現在のページを更新したり終了したりしても、実行中のプロファイリング タスクは停止されません。

## パフォーマンスデータをダウンロード {#download-performance-data}

すべてのインスタンスのプロファイリングが完了したら、右上隅の**「プロファイリング結果のダウンロード」を**クリックして、すべてのパフォーマンス データをダウンロードできます。

![Download profiling result](/media/dashboard/dashboard-profiling-download.png)

表内の個々のインスタンスをクリックして、そのプロファイリング結果を表示することもできます。または、... にマウスを移動して生データをダウンロードすることもできます。

![Single instance result](/media/dashboard/dashboard-profiling-view-single.png)

## プロファイリング履歴をビュー {#view-profiling-history}

オンデマンド プロファイリング履歴がページにリストされます。行をクリックすると詳細が表示されます。

![View profiling history](/media/dashboard/dashboard-profiling-history.png)

プロファイリングステータスページでの詳細な操作については、 [プロファイリングステータスのビュー](#view-profiling-status)参照してください。
