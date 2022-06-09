---
title: Manual Profiling
summary: Learn the manual instance profiling of TiDB Dashboard.
---

# 手動インスタンスプロファイリングページ {#manual-instance-profiling-page}

手動インスタンスプロファイリングページでは、TiDB、TiKV、PD、およびTiFlashインスタンスのパフォーマンスデータを収集できます。収集されたデータは、フレームグラフまたは有向非巡回グラフに表示できます。グラフは、パフォーマンスの要約期間中にインスタンスで実行された内部操作と、対応する比率を視覚的に示します。このグラフを使用すると、これらのインスタンスのCPUリソース消費量をすばやく知ることができます。

## コンテンツのプロファイリング {#profiling-content}

手動プロファイリングを使用すると、TiDB、PD、TiKV、およびTiFlashインスタンスのパフォーマンスデータを収集できます。収集されたデータは、フレームグラフや有向非巡回グラフなどの形式で表示できます。表示されるデータは、パフォーマンスプロファイリング期間中にインスタンスで実行される内部操作と対応する比率を視覚的に示します。このようなデータを使用すると、これらのインスタンスのCPUリソース消費量をすばやく知ることができます。

## ページにアクセスする {#access-the-page}

次のいずれかの方法を使用して、インスタンスプロファイリングページにアクセスできます。

-   TiDBダッシュボードにログインした後、左側のナビゲーションバーで[**高度なデバッグ**]&gt;[<strong>インスタンスのプロファイリング</strong>]&gt;[<strong>手動プロファイリング</strong>]をクリックします。

    ![Access instance profiling page](/media/dashboard/dashboard-profiling-access.png)

-   ブラウザで[http://127.0.0.1:2379/dashboard/#/instance_profiling](http://127.0.0.1:2379/dashboard/#/instance_profiling)にアクセスします。 `127.0.0.1:2379`を実際のPDインスタンスのアドレスとポートに置き換えます。

## プロファイリングを開始します {#start-profiling}

インスタンスプロファイリングページで、少なくとも1つのターゲットインスタンスを選択し、[**プロファイリング**の開始]をクリックしてインスタンスプロファイリングを開始します。

![Start instance profiling](/media/dashboard/dashboard-profiling-start.png)

プロファイリングを開始する前に、プロファイリング期間を変更できます。この期間は、プロファイリングに必要な時間によって決定されます。デフォルトでは30秒です。 30秒の期間は、完了するまでに約30秒かかります。

## プロファイリングステータスの表示 {#view-profiling-status}

プロファイリングが開始されると、プロファイリングのステータスと進行状況をリアルタイムで表示できます。

![Profiling detail](/media/dashboard/dashboard-profiling-view-progress.png)

プロファイリングはバックグラウンドで実行されます。現在のページを更新または終了しても、実行中のプロファイリングタスクは停止しません。

## プロファイリング結果をダウンロード {#download-profiling-result}

すべてのインスタンスのプロファイリングが完了したら、右上隅にある[**プロファイリング結果のダウンロード**]をクリックして、すべてのプロファイリング結果をダウンロードできます。

![Download profiling result](/media/dashboard/dashboard-profiling-download.png)

テーブル内の個々のインスタンスをクリックして、そのプロファイリング結果（フレームチャート、有向非巡回グラフ、テキストなど）を表示することもできます。または、...にカーソルを合わせて生データをダウンロードすることもできます。

![Single instance result](/media/dashboard/dashboard-profiling-view-single.png)

## プロファイリング履歴を表示する {#view-profiling-history}

プロファイリング履歴は、インスタンスプロファイリングページに一覧表示されます。リストの1行をクリックすると、ステータスの詳細を表示できます。

![View profiling history](/media/dashboard/dashboard-profiling-history.png)

プロファイリングステータスページの詳細な操作については、 [プロファイリングステータスの表示](#view-profiling-status)を参照してください。
