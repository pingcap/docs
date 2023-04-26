---
title: Perform a Proof of Concept (PoC) with TiDB Cloud
summary: Learn about how to perform a Proof of Concept (PoC) with TiDB Cloud.
---

# TiDB Cloudで概念実証 (PoC) を実行する {#perform-a-proof-of-concept-poc-with-tidb-cloud}

TiDB Cloud は、サービスとしてのデータベース (DBaaS) 製品であり、完全に管理されたクラウド データベースで TiDB の優れた機能をすべて提供します。データベースの複雑さではなく、アプリケーションに集中するのに役立ちます。 TiDB Cloudは現在、Amazon Web Services (AWS) と Google Cloud Platform (GCP) の両方で利用できます。

概念実証 (PoC) を開始することは、 TiDB Cloud がビジネス ニーズに最適かどうかを判断するための最良の方法です。また、短時間でTiDB Cloudの主要な機能に慣れることができます。パフォーマンス テストを実行することで、ワークロードがTiDB Cloudで効率的に実行できるかどうかを確認できます。また、データの移行と構成の適応に必要な作業を評価することもできます。

このドキュメントでは、一般的な PoC 手順について説明し、 TiDB Cloud PoC を迅速に完了するのに役立つことを目的としています。これは、TiDB の専門家と大規模な顧客ベースによって検証されたベスト プラクティスです。

PoC に興味がある場合は、始める前に<a href="mailto:tidbcloud-support@pingcap.com">PingCAP に</a>お気軽にお問い合わせください。サポート チームは、テスト計画の作成を支援し、PoC 手順をスムーズに進めることができます。

または、簡単な評価のためにTiDB Cloudに慣れる[Serverless Tierを作成する](/tidb-cloud/tidb-cloud-quickstart.md#step-1-create-a-tidb-cluster)こともできます。Serverless Tierには[特別利用規約](/tidb-cloud/select-cluster-tier.md#serverless-tier-special-terms-and-conditions)があることに注意してください。

## PoC手順の概要 {#overview-of-the-poc-procedures}

PoC の目的は、 TiDB Cloud がビジネス要件を満たしているかどうかをテストすることです。一般的な PoC は通常 14 日間続きます。その間、PoC の完了に集中することが期待されます。

典型的なTiDB Cloud PoC は、次の手順で構成されます。

1.  成功基準を定義し、テスト計画を作成する
2.  ワークロードの特性を特定する
3.  サインアップして PoC 専用クラスターを作成する
4.  スキーマと SQL を適応させる
5.  データのインポート
6.  ワークロードを実行して結果を評価する
7.  その他の機能を調べる
8.  環境をクリーンアップして PoC を終了する

## ステップ 1. 成功基準を定義し、テスト計画を作成する {#step-1-define-success-criteria-and-create-a-test-plan}

PoC を通じてTiDB Cloudを評価する場合は、ビジネス ニーズに基づいて関心のあるポイントと対応する技術評価基準を決定し、PoC に対する期待と目標を明確にすることをお勧めします。詳細なテスト計画を備えた明確で測定可能な技術基準は、主要な側面に焦点を当て、ビジネス レベルの要件をカバーし、最終的に PoC 手順を通じて回答を得るのに役立ちます。

次の質問を使用して、PoC の目標を特定します。

-   ワークロードのシナリオは何ですか?
-   ビジネスのデータセットのサイズまたはワークロードはどのくらいですか?成長率は？
-   ビジネスに不可欠なスループットやレイテンシーの要件など、パフォーマンスの要件は何ですか?
-   最小限の許容可能な計画的または計画外のダウンタイムを含め、可用性と安定性の要件は何ですか?
-   運用効率に必要な指標は何ですか?それらをどのように測定しますか？
-   ワークロードのセキュリティとコンプライアンスの要件は何ですか?

成功基準とテスト計画の作成方法の詳細については、お気軽に<a href="mailto:tidbcloud-support@pingcap.com">PingCAP</a>にお問い合わせください。

## ステップ 2. ワークロードの特性を特定する {#step-2-identify-characteristics-of-your-workload}

TiDB Cloud は、大量のデータとの高可用性と強整合性を必要とするさまざまなユース ケースに適しています。 [TiDB の紹介](https://docs.pingcap.com/tidb/stable/overview)主な機能とシナリオを示します。それらがビジネス シナリオに当てはまるかどうかを確認できます。

-   水平方向のスケールアウトまたはスケールイン
-   金融グレードの高可用性
-   リアルタイム HTAP
-   MySQL 5.7プロトコルおよび MySQL エコシステムとの互換性

また、分析処理の高速化に役立つ列指向storageエンジンである[TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview)の使用にも関心があるかもしれません。 PoC 期間中はいつでもTiFlash機能を使用できます。

## ステップ 3.サインアップして、PoC 用の専用クラスターを作成する {#step-3-sign-up-and-create-a-dedicated-cluster-for-the-poc}

PoC 用の専用クラスターを作成するには、次の手順を実行します。

1.  次のいずれかを実行して、PoC アプリケーション フォームに入力します。

    -   PingCAP の Web サイトで、 [PoCに申し込む](https://pingcap.com/apply-for-poc/)ページに移動して、アプリケーション フォームに入力します。
    -   [TiDB Cloudコンソール](https://tidbcloud.com/)で、<mdsvgicon name="icon-top-contact-us">右上隅にある**[お問い合わせ] を**選択し、 <strong>[PoC に申し込む] を</strong>選択してアプリケーション フォームに入力します。</mdsvgicon>

    フォームを送信すると、 TiDB Cloudサポート チームがアプリケーションを確認し、連絡を取り、アプリケーションが承認されたらクレジットをアカウントに転送します。 PingCAP サポート エンジニアに連絡して、PoC 手順をサポートし、PoC が可能な限りスムーズに実行されるようにすることもできます。

2.  [クイックスタート](/tidb-cloud/tidb-cloud-quickstart.md)を参照して、PoC 用の[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスターを作成します。

クラスターを作成する前に、クラスターのサイジングのために容量計画を立てることをお勧めします。 TiDB、TiKV、またはTiFlashノードの推定数から開始し、後でクラスターをスケールアウトして、パフォーマンス要件を満たすことができます。詳細については、次のドキュメントを参照するか、サポート チームにお問い合わせください。

-   見積もり方法の詳細については、 [TiDB のサイジング](/tidb-cloud/size-your-cluster.md)を参照してください。
-   専用クラスターの構成については、 [TiDBクラスタを作成する](/tidb-cloud/create-tidb-cluster.md)を参照してください。 TiDB、TiKV、およびTiFlash (オプション) のクラスター サイズをそれぞれ構成します。
-   PoC クレジットの消費を効果的に計画および最適化する方法については、このドキュメントの[FAQ](#faq)を参照してください。
-   スケーリングの詳細については、 [TiDBクラスタをスケーリングする](/tidb-cloud/scale-tidb-cluster.md)を参照してください。

専用の PoC クラスターが作成されると、データを読み込んで一連のテストを実行する準備が整います。 TiDB クラスターに接続する方法については、 [TiDBクラスタに接続する](/tidb-cloud/connect-to-tidb-cluster.md)を参照してください。

新しく作成されたクラスターの場合、次の構成に注意してください。

-   デフォルトのタイム ゾーン (ダッシュボードの [**作成時間]**列) は UTC です。 [ローカル タイム ゾーンの設定](/tidb-cloud/manage-user-access.md#set-the-time-zone-for-your-organization)に従って、ローカル タイム ゾーンに変更できます。
-   新しいクラスターのデフォルトのバックアップ設定は、毎日の完全なデータベース バックアップです。希望するバックアップ時間を指定するか、データを手動でバックアップできます。デフォルトのバックアップ時間と詳細については、 [TiDBクラスタデータのバックアップと復元](/tidb-cloud/backup-and-restore.md#backup)を参照してください。

## ステップ 4. スキーマと SQL を適応させる {#step-4-adapt-your-schemas-and-sql}

次に、テーブルとインデックスを含むデータベース スキーマを TiDB クラスターにロードできます。

PoC クレジットの量は限られているため、クレジットの価値を最大化するために、 TiDB Cloudでの互換性テストおよび予備分析用に[Serverless Tierクラスター](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)を作成することをお勧めします。

TiDB Cloud はMySQL 5.7と高い互換性があります。 MySQL と互換性がある場合、または MySQL と互換性があるように調整できる場合は、TiDB にデータを直接インポートできます。

互換性の詳細については、次のドキュメントを参照してください。

-   [TiDB と MySQL の互換性](https://docs.pingcap.com/tidb/stable/mysql-compatibility) .
-   [MySQL とは異なる TiDB の機能](https://docs.pingcap.com/tidb/stable/mysql-compatibility#features-that-are-different-from-mysql) .
-   [TiDB のキーワードと予約語](https://docs.pingcap.com/tidb/stable/keywords) .
-   [TiDB の制限事項](https://docs.pingcap.com/tidb/stable/tidb-limitations) .

いくつかのベスト プラクティスを次に示します。

-   スキーマのセットアップに非効率性がないかどうかを確認します。
-   不要なインデックスを削除します。
-   効果的なパーティショニングのためのパーティショニング ポリシーを計画します。
-   タイムスタンプのインデックスなど、右側のインデックスの増加による[ホットスポットの問題](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#identify-hotspot-issues)避けてください。
-   [SHARD_ROW_ID_BITS](https://docs.pingcap.com/tidb/stable/shard-row-id-bits)と[自動ランダム](https://docs.pingcap.com/tidb/stable/auto-random)を使用して[ホットスポットの問題](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#identify-hotspot-issues)を回避します。

SQL ステートメントの場合、データ ソースと TiDB との互換性のレベルに応じて、それらを調整する必要がある場合があります。

ご不明な点がございましたら、 [PingCAP](/tidb-cloud/tidb-cloud-support.md)までご相談ください。

## ステップ 5. データのインポート {#step-5-import-data}

小さなデータセットをインポートして実現可能性をすばやくテストしたり、大きなデータセットをインポートして TiDB データ移行ツールのスループットをテストしたりできます。 TiDB はサンプル データを提供しますが、ビジネスの実際のワークロードでテストを実行することを強くお勧めします。

さまざまな形式のデータをTiDB Cloudにインポートできます。

-   [サンプル データを SQL ファイル形式でインポートする](/tidb-cloud/import-sample-data.md)
-   [Amazon Aurora MySQL からの移行](/tidb-cloud/migrate-from-aurora-bulk-import.md)
-   [Amazon S3 または GCS から CSV ファイルをインポートする](/tidb-cloud/import-csv-files.md)
-   [Apache Parquet ファイルのインポート](/tidb-cloud/import-parquet-files.md)

> **ノート：**
>
> -   TiDB Cloudでサポートされている文字照合については、 [MySQL 互換データベースからの移行](/tidb-cloud/migrate-data-into-tidb.md)を参照してください。データが元々どのように保存されているかを理解することは非常に役立ちます。
> -   **データ インポート**ページでのデータ インポートでは、追加の請求料金は発生しません。

## ステップ 6. ワークロードを実行して結果を評価する {#step-6-run-your-workload-and-evaluate-results}

これで、環境を作成し、スキーマを調整し、データをインポートしました。ワークロードをテストする時が来ました。

ワークロードをテストする前に、必要に応じてデータベースを元の状態に復元できるように、手動バックアップを実行することを検討してください。詳細については、 [TiDBクラスタデータのバックアップと復元](/tidb-cloud/backup-and-restore.md#backup)を参照してください。

ワークロードを開始した後、次の方法を使用してシステムを観察できます。

-   クラスタの一般的に使用されるメトリクスは、クラスタの概要ページで確認できます。これには、合計 QPS、レイテンシ、接続、 TiFlashリクエスト QPS、 TiFlashリクエスト期間、 TiFlashストレージ サイズ、TiKV ストレージ サイズ、TiDB CPU、TiKV CPU、TiKV IO 読み取り、および TiKV IO 書き込み。 [TiDBクラスタを監視する](/tidb-cloud/monitor-tidb-cluster.md)を参照してください。
-   **[診断] &gt; [ステートメント]**に移動します。ここでは、SQL の実行を観察し、システム テーブルにクエリを実行しなくてもパフォーマンスの問題を簡単に見つけることができます。 [ステートメント分析](/tidb-cloud/tune-performance.md)を参照してください。
-   **[診断] &gt; [キー ビジュアライザー]**に移動します。TiDB データ アクセス パターンとデータ ホットスポットを表示できます。 [キー ビジュアライザー](/tidb-cloud/tune-performance.md#key-visualizer)を参照してください。
-   これらのメトリックを独自の Datadog および Prometheus に統合することもできます。 [サードパーティの監視統合](/tidb-cloud/third-party-monitoring-integrations.md)を参照してください。

ここで、テスト結果を評価します。

より正確な評価を得るには、テストの前にメトリックのベースラインを決定し、実行ごとにテスト結果を適切に記録します。結果を分析することで、 TiDB Cloud がアプリケーションに適しているかどうかを判断できます。一方、これらの結果はシステムの実行ステータスを示しており、メトリックに従ってシステムを調整できます。例えば：

-   システムのパフォーマンスが要件を満たしているかどうかを評価します。合計 QPS とレイテンシーを確認します。システムのパフォーマンスが不十分な場合は、次のようにパフォーマンスを調整できます。

    -   ネットワークレイテンシーを監視して最適化します。
    -   SQL パフォーマンスを調査して調整します。
    -   モニターと[ホットスポットの問題を解決する](https://docs.pingcap.com/tidb/dev/troubleshoot-hot-spot-issues#troubleshoot-hotspot-issues) ．

-   storageサイズと CPU 使用率を評価し、それに応じて TiDB クラスターをスケールアウトまたはスケールインします。スケーリングの詳細については、セクション[FAQ](#faq)を参照してください。

次に、パフォーマンス チューニングのヒントを示します。

-   書き込みパフォーマンスの向上

    -   TiDB クラスターをスケールアウトして、書き込みスループットを向上させます ( [TiDBクラスタのスケーリング](/tidb-cloud/scale-tidb-cluster.md)を参照)。
    -   [楽観的取引モデル](https://docs.pingcap.com/tidb/stable/optimistic-transaction#tidb-optimistic-transaction-model)を使用してロックの競合を減らします。

-   クエリのパフォーマンスを向上させる

    -   **[診断] &gt; [ステートメント]**ページで SQL 実行計画を確認します。
    -   **[ダッシュボード] &gt; [キー ビジュアライザー]**ページでホットスポットの問題を確認します。
    -   **[概要] &gt; [容量メトリクス]**ページで、TiDB クラスターの容量が不足しているかどうかを監視します。
    -   TiFlash機能を使用して、分析処理を最適化します。 [HTAPクラスタを使用する](/tiflash/tiflash-overview.md)を参照してください。

## ステップ 7. その他の機能を調べる {#step-7-explore-more-features}

ワークロードのテストが完了したので、アップグレードやバックアップなど、さらに多くの機能を調べることができます。

-   アップグレード

    TiDB Cloud はTiDB クラスターを定期的にアップグレードしますが、サポート チケットを送信してクラスターのアップグレードをリクエストすることもできます。 [TiDBクラスタをアップグレードする](/tidb-cloud/upgrade-tidb-cluster.md)を参照してください。

-   バックアップ

    ベンダー ロックインを回避するには、毎日の完全バックアップを使用してデータを新しいクラスターに移行し、 [Dumpling](/dumpling-overview.md)を使用してデータをエクスポートします。詳細については、 [TiDB からのデータのエクスポート](/tidb-cloud/export-data-from-tidb-cloud.md)を参照してください。

## ステップ 8. 環境をクリーンアップして PoC を終了する {#step-8-clean-up-the-environment-and-finish-the-poc}

実際のワークロードを使用してTiDB Cloudをテストし、テスト結果を取得したら、PoC の完全なサイクルを完了しました。これらの結果は、 TiDB Cloud が期待を満たしているかどうかを判断するのに役立ちます。その間、 TiDB Cloudを使用するためのベスト プラクティスを蓄積してきました。

TiDB Cloud を大規模に試してみたい場合は、 TiDB Cloudが提供する他のノードstorageサイズでのデプロイなど、新しいラウンドのデプロイとテストのために、 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)を作成してTiDB Cloudへのフル アクセスを取得します。

クレジットがなくなり、PoC を続行したい場合は、 [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)に連絡して相談してください。

いつでも PoC を終了してテスト環境を削除できます。詳細については、 [TiDBクラスタを削除する](/tidb-cloud/delete-tidb-cluster.md)を参照してください。

サポート チームへのフィードバックは、PoC プロセス、機能のリクエスト、製品の改善方法など、 [TiDB Cloudフィードバック フォーム](https://www.surveymonkey.com/r/L3VVW8R)に記入していただければ幸いです。

## FAQ {#faq}

### 1. データのバックアップと復元にはどのくらいの時間がかかりますか? {#1-how-long-does-it-take-to-back-up-and-restore-my-data}

TiDB Cloud は、自動バックアップと手動バックアップの 2 種類のデータベース バックアップを提供します。どちらの方法でも、データベース全体がバックアップされます。

データのバックアップと復元にかかる時間は、テーブルの数、ミラー コピーの数、および CPU を集中的に使用するレベルによって異なります。 1 つの TiKV ノードでのバックアップと復元の速度は、約 50 MB/秒です。

通常、データベースのバックアップおよび復元操作は CPU を集中的に使用し、常に追加の CPU リソースを必要とします。この環境の CPU 使用率によっては、QPS とトランザクションレイテンシーに影響 (10% から 50%) が生じる可能性があります。

### 2. いつスケールアウトおよびスケールインする必要がありますか? {#2-when-do-i-need-to-scale-out-and-scale-in}

スケーリングに関するいくつかの考慮事項を次に示します。

-   ピーク時またはデータ インポート時に、ダッシュボードの容量メトリックが上限に達したことを確認した場合 ( [TiDBクラスタを監視する](/tidb-cloud/monitor-tidb-cluster.md)を参照)、クラスターをスケールアウトする必要がある場合があります。
-   リソースの使用率が持続的に低い場合 (たとえば、CPU 使用率が 10% ～ 20% のみ)、クラスターをスケールインしてリソースを節約できます。

コンソールでクラスターを自分でスケールアウトできます。クラスターをスケールインする必要がある場合は、 [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)に連絡してサポートを受ける必要があります。スケーリングの詳細については、 [TiDBクラスタをスケーリングする](/tidb-cloud/scale-tidb-cluster.md)参照してください。サポートチームと連絡を取り合い、正確な進捗状況を追跡できます。データの再調整によりパフォーマンスに影響を与える可能性があるため、テストを開始する前にスケーリング操作が完了するまで待つ必要があります。

### 3. PoC クレジットを最大限に活用するにはどうすればよいですか? {#3-how-to-make-the-best-use-of-my-poc-credits}

PoC の申請が承認されると、アカウントにクレジットが付与されます。通常、クレジットは 14 日間の PoC に十分です。クレジットは、ノードのタイプとノードの数によって、時間単位で課金されます。詳細については、 [TiDB Cloud請求](/tidb-cloud/tidb-cloud-billing.md#credits)を参照してください。

PoC に残っているクレジットを確認するには、次のスクリーンショットに示すように、ターゲット プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

![TiDB Cloud PoC Credits](/media/tidb-cloud/poc-points.png)

をクリックすることもできます。<mdsvgicon name="icon-top-account-settings"> TiDB Cloudコンソールの右上隅にある**[アカウント] を**クリックし、 <strong>[請求] を</strong>クリックし、 <strong>[クレジット]</strong>をクリックして、クレジットの詳細ページを表示します。</mdsvgicon>

クレジットを節約するには、使用していないクラスターを削除します。現在、クラスターを停止することはできません。クラスターを削除する前に、バックアップが最新であることを確認する必要があります。これにより、後で PoC を再開するときにクラスターを復元できます。

PoC プロセスが完了した後も未使用のクレジットがある場合は、クレジットの有効期限が切れていない限り、引き続きクレジットを使用して TiDB クラスター料金を支払うことができます。

### 4. PoC を完了するのに 2 週間以上かかることはありますか? {#4-can-i-take-more-than-2-weeks-to-complete-a-poc}

PoC の試用期間を延長したい場合、またはクレジットが不足している場合は、 [お問い合わせ](https://www.pingcap.com/contact-us/)までお問い合わせください。

### 5. 技術的な問題で立ち往生しています。 PoC のサポートを受けるにはどうすればよいですか? {#5-i-m-stuck-with-a-technical-problem-how-do-i-get-help-for-my-poc}

いつでも助けを求める[TiDB Cloudサポートに連絡する](/tidb-cloud/tidb-cloud-support.md)ができます。
