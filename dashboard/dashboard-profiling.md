---
title: TiDB Dashboard Instance Profiling - Manual Profiling
summary: 手動プロファイリングを使用すると、TiDB、TiKV、PD、 TiFlashインスタンスの現在のパフォーマンスデータをオンデマンドで収集できます。エキスパートはCPUやメモリなどのリソース消費量の詳細を分析し、進行中のパフォーマンス問題を特定できます。このページには、TiDB Dashboardまたはブラウザからアクセスできます。対象インスタンスを選択してプロファイリングを開始し、必要に応じて期間を変更します。リアルタイムの進行状況を確認し、プロファイリング完了後にパフォーマンスデータをダウンロードできます。詳細な操作については、プロファイリング履歴を確認する。
---

# TiDB Dashboardインスタンスプロファイリング - 手動プロファイリング {#tidb-dashboard-instance-profiling-manual-profiling}

> **Note:**
>
> この機能はデータベースのエキスパート向けに設計されています。エキスパートでない方は、PingCAPテクニカルサポートの指示に従ってこの機能を使用することをお勧めします。

手動プロファイリングを使用すると、TiDB、TiKV、PD、 TiFlashの各インスタンスの現在のパフォーマンスデータをワンクリックでオン**デマンドで**収集できます。収集されたパフォーマンスデータは、FlameGraphまたはDAG形式で視覚化できます。

これらのパフォーマンス データを使用すると、専門家はインスタンスの CPU やメモリなどの現在のリソース消費の詳細を分析し、CPU オーバーヘッドの増加、メモリ使用量の増加、プロセスの停止など、進行中の高度なパフォーマンスの問題を正確に特定できます。

プロファイリングを開始すると、TiDB Dashboardは一定期間（デフォルトでは30秒）現在のパフォーマンスデータを収集します。そのため、この機能はクラスターが現在直面している進行中の問題の分析にのみ使用でき、過去の問題には大きな影響を与えません。**いつでも**パフォーマンスデータを収集して分析したい場合は、 [継続的なプロファイリング](/dashboard/continuous-profiling.md)参照してください。

## サポートされているパフォーマンスデータ {#supported-performance-data}

現在、次のパフォーマンス データがサポートされています。

-   CPU: TiDB、TiKV、PD、 TiFlashインスタンスの各内部関数のCPUオーバーヘッド

    > TiKV およびTiFlashインスタンスの CPU オーバーヘッドは、現在 ARMアーキテクチャではサポートされていません。

-   ヒープ: TiDB、TiKV、PDインスタンス上の各内部関数のメモリ消費量

    > TiDBはv7.5以降、TiKVヒーププロファイルをサポートしています。TiDB Dashboardの実行環境にはPerl実行環境が必要です。Perl実行環境がない場合、エラーが発生します。

-   ミューテックス: TiDBおよびPDインスタンス上のミューテックスの競合状態

-   Goroutine: TiDB および PD インスタンス上のすべての Goroutine の実行状態と呼び出しスタック

## ページにアクセスする {#access-the-page}

次のいずれかの方法でインスタンス プロファイリング ページにアクセスできます。

-   TiDB Dashboardにログインしたら、左側のナビゲーション メニューで**[高度なデバッグ]** &gt; **[インスタンスのプロファイリング]** &gt; **[手動プロファイリング]**をクリックします。

    ![Access instance profiling page](/media/dashboard/dashboard-profiling-access.png)

-   ブラウザで[http://127.0.0.1:2379/dashboard/#/instance_profiling](http://127.0.0.1:2379/dashboard/#/instance_profiling)にアクセスしてください。`127.0.0.1:2379`を実際のPDインスタンスのアドレスとポートに置き換えてください。

## プロファイリングを開始 {#start-profiling}

インスタンス プロファイリング ページで、少なくとも 1 つのターゲット インスタンスを選択し、 **[プロファイリングの開始]**をクリックしてインスタンス プロファイリングを開始します。

![Start instance profiling](/media/dashboard/dashboard-profiling-start.png)

プロファイリングを開始する前に、プロファイリング期間を変更できます。この期間はプロファイリングに必要な時間によって決まり、デフォルトでは30秒です。30秒の期間は完了まで30秒かかります。

[継続的なプロファイリング](/dashboard/continuous-profiling.md)有効になっているクラスターでは、手動プロファイリングを開始できません。現時点でのパフォーマンスデータを表示するには、 [継続的なプロファイリングページ](/dashboard/continuous-profiling.md#access-the-page)で最新のプロファイリング結果をクリックしてください。

## プロファイリングステータスを表示する {#view-profiling-status}

プロファイリングが開始されると、プロファイリングのステータスと進行状況をリアルタイムで確認できます。

![Profiling detail](/media/dashboard/dashboard-profiling-view-progress.png)

プロファイリングはバックグラウンドで実行されます。現在のページを更新したり終了したりしても、実行中のプロファイリングタスクは停止されません。

## パフォーマンスデータをダウンロード {#download-performance-data}

すべてのインスタンスのプロファイリングが完了したら、右上隅の**「プロファイリング結果のダウンロード」**をクリックして、すべてのパフォーマンス データをダウンロードできます。

![Download profiling result](/media/dashboard/dashboard-profiling-download.png)

表内の個々のインスタンスをクリックすると、そのプロファイリング結果を表示できます。また、... にマウスを合わせると、生データをダウンロードできます。

![Single instance result](/media/dashboard/dashboard-profiling-view-single.png)

## プロファイリング履歴を表示する {#view-profiling-history}

オンデマンドプロファイリングの履歴がページに表示されます。行をクリックすると詳細が表示されます。

![View profiling history](/media/dashboard/dashboard-profiling-history.png)

プロファイリング ステータス ページでの詳細な操作については、 [プロファイリングステータスを表示する](#view-profiling-status)を参照してください。
