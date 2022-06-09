---
title: TiDB Dashboard Continuous Profiling
summary: Learn how to enable Continuous Profiling and observe system conditions by using this feature.
---

# TiDBダッシュボードインスタンスプロファイリング-継続的なプロファイリング {#tidb-dashboard-instance-profiling-continuous-profiling}

> **警告：**
>
> 継続的プロファイリングは現在実験的機能であり、実稼働環境での使用はお勧めしません。

TiDB 5.3.0で導入された継続的プロファイリングは、システムコールレベルでリソースのオーバーヘッドを監視する方法です。継続的プロファイリングのサポートにより、TiDBは、データベースのソースコードを直接調べるのと同じくらい明確なパフォーマンスの洞察を提供し、研究開発および運用および保守担当者がフレームグラフを使用してパフォーマンスの問題の根本原因を特定するのに役立ちます。

0.5％未満のパフォーマンス低下で、この機能はデータベース内部操作の継続的なスナップショット（CTスキャンと同様）を取得し、データベースを「ブラックボックス」からより観察しやすい「ホワイトボックス」に変えます。この機能は、ワンクリックで有効にすると自動的に実行され、保存期間内に生成されたストレージ結果を保持します。保存期間を超えた保管結果は、保管スペースを解放するためにリサイクルされます。

## 制限 {#restrictions}

連続プロファイリング機能を有効にする前に、次の制限に注意してください。

-   x86アーキテクチャでは、この機能はTiDB、PD、TiKV、およびTiFlashをサポートします。この機能はARMアーキテクチャと完全には互換性がなく、このアーキテクチャでは有効にできません。

-   この機能は、v1.9.0以降のTiUPまたはv1.3.0以降のTiDB Operatorを使用してデプロイまたはアップグレードされたクラスターで使用できます。この機能は、バイナリパッケージを使用して展開またはアップグレードされたクラスターでは使用できません。

## コンテンツのプロファイリング {#profiling-content}

継続的プロファイリングを使用すると、TiDB、PD、TiKV、およびTiFlashインスタンスの継続的なパフォーマンスデータを収集し、ノードを再起動せずに昼夜を問わず監視できます。収集されたデータは、フレームグラフや有向非巡回グラフなどの形式で表示できます。表示されるデータは、パフォーマンスプロファイリング期間中にインスタンスで実行される内部操作と対応する比率を視覚的に示します。このようなデータを使用すると、これらのインスタンスのCPUリソース消費量をすばやく知ることができます。

現在、ContinuousProfilingは次のパフォーマンスデータを表示できます。

-   TiDB / PD：CPUプロファイル、ヒープ、ミューテックス、ゴルーチン（debug = 2）
-   TiKV / TiFlash：CPUプロファイル

## 継続的なプロファイリングを有効にする {#enable-continuous-profiling}

このセクションでは、TiUPおよびTiDB Operatorをそれぞれ使用してデプロイされたTiDBクラスターで継続的プロファイリングを有効にする方法について説明します。

### TiUPを使用してデプロイされたクラスター {#clusters-deployed-using-tiup}

TiUPを使用してデプロイされたクラスターで継続的プロファイリングを有効にするには、次の手順を実行します。

1.  TiDBダッシュボードで、[**高度なデバッグ**]&gt;[<strong>インスタンスのプロファイリング</strong>]&gt;[<strong>継続的なプロファイリング</strong>]をクリックします。

2.  表示されたウィンドウで、[設定を**開く]**をクリックします。右側の<strong>[設定]</strong>領域で、[<strong>機能</strong>を有効にする]をオンに切り替え、必要に応じて<strong>保持期間</strong>のデフォルト値を変更します。

3.  この機能を有効にするには、[**保存]**をクリックします。

![Enable the feature](/media/dashboard/dashboard-conprof-start.png)

### TiDB Operatorを使用してデプロイされたクラスター {#clusters-deployed-using-tidb-operator}

[継続的なプロファイリングを有効にする](https://docs.pingcap.com/tidb-in-kubernetes/dev/access-dashboard#enable-continuous-profiling)を参照してください。

## ページにアクセスする {#access-the-page}

次のいずれかの方法を使用して、継続的なプロファイリングページにアクセスできます。

-   TiDBダッシュボードにログインした後、左側のナビゲーションバーで[**高度なデバッグ**]&gt;[<strong>インスタンスのプロファイリング</strong>]&gt;[<strong>継続的なプロファイリング</strong>]をクリックします。

    ![Access](/media/dashboard/dashboard-conprof-access.png)

-   ブラウザから[http://127.0.0.1:2379/dashboard/#/continuous_profiling](http://127.0.0.1:2379/dashboard/#/continuous_profiling)にアクセスします。 `127.0.0.1:2379`を実際のPDインスタンスのアドレスとポートに置き換えます。

## プロファイリング履歴を表示する {#view-profiling-history}

継続的なプロファイリングを開始した後、インスタンスプロファイリングページでプロファイリング結果を表示できます。

![Profiling history](/media/dashboard/dashboard-conprof-history.png)

パフォーマンスプロファイリングはバックグラウンドで実行されます。現在のページを更新または終了しても、実行中のパフォーマンスプロファイリングタスクは終了しません。

## プロファイリング結果をダウンロード {#download-profiling-result}

プロファイリング結果ページで、右上隅にある[**プロファイリング結果のダウンロード**]をクリックして、すべてのプロファイリング結果をダウンロードできます。

![Download profiling result](/media/dashboard/dashboard-conprof-download.png)

テーブル内の個々のインスタンスをクリックして、そのプロファイリング結果（フレームチャート、有向非巡回グラフ、テキストなど）を表示することもできます。または、...にカーソルを合わせて生データをダウンロードすることもできます。

![View the profiling result of an instance](/media/dashboard/dashboard-conprof-single.png)

## 継続的なプロファイリングを無効にする {#disable-continuous-profiling}

1.  TiDBダッシュボードで、左側のナビゲーションバーの[ **Advanced Debugging** ]&gt; [ <strong>Profiling Instances</strong> ]&gt;[ <strong>ContinuousProfiling</strong> ]をクリックします。 [<strong>設定]</strong>をクリックします。

2.  ポップアップウィンドウで、[**機能を有効**にする]の下のボタンをオフにします。

3.  [**連続プロファイリング機能を無効**にする]ダイアログボックスで、[<strong>無効</strong>にする]をクリックします。

4.  [**保存]**をクリックします。

5.  ポップアップウィンドウで、[**無効**にする]をクリックします。

![Disable the feature](/media/dashboard/dashboard-conprof-stop.png)
