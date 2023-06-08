---
title: Perform a Proof of Concept (PoC) with TiDB Cloud
summary: Learn about how to perform a Proof of Concept (PoC) with TiDB Cloud.
---

# TiDB Cloudを使用して概念実証 (PoC) を実行する {#perform-a-proof-of-concept-poc-with-tidb-cloud}

TiDB Cloud は、フルマネージドのクラウド データベースで TiDB の優れた機能をすべて提供する Database-as-a-Service (DBaaS) 製品です。これにより、データベースの複雑さではなく、アプリケーションに集中することができます。 TiDB Cloudは現在、アマゾン ウェブ サービス (AWS) と Google Cloud Platform (GCP) の両方で利用できます。

TiDB Cloud がビジネス ニーズに最適であるかどうかを判断するには、概念実証 (PoC) を開始することが最善の方法です。また、 TiDB Cloudの主要な機能を短時間で理解できるようになります。パフォーマンス テストを実行すると、ワークロードがTiDB Cloud上で効率的に実行できるかどうかを確認できます。データの移行と構成の適応に必要な作業を評価することもできます。

このドキュメントでは、一般的な PoC 手順について説明し、 TiDB CloudPoC を迅速に完了できるようにすることを目的としています。これは、TiDB の専門家と大規模な顧客ベースによって検証されたベスト プラクティスです。

PoC の実施に興味がある場合は、開始する前にお気軽に<a href="mailto:tidbcloud-support@pingcap.com">PingCAP</a>にお問い合わせください。サポート チームは、テスト計画の作成を支援し、PoC 手順をスムーズに進めることができます。

あるいは、 TiDB Cloudに慣れて簡単に評価すること[<a href="/tidb-cloud/tidb-cloud-quickstart.md#step-1-create-a-tidb-cluster">TiDB Serverlessを作成する</a>](/tidb-cloud/tidb-cloud-quickstart.md#step-1-create-a-tidb-cluster)できます。 TiDB Serverless にはいくつかの[<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-special-terms-and-conditions">特別な利用規約</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-special-terms-and-conditions)あることに注意してください。

## PoC手順の概要 {#overview-of-the-poc-procedures}

PoC の目的は、 TiDB Cloud がビジネス要件を満たしているかどうかをテストすることです。通常、PoC は 14 日間続き、その間は PoC を完了することに集中することが期待されます。

一般的なTiDB CloudPoC は、次の手順で構成されます。

1.  成功基準を定義し、テスト計画を作成する
2.  ワークロードの特性を特定する
3.  サインアップして、PoC 用の TiDB Dedicatedクラスターを作成します
4.  スキーマと SQL を適応させる
5.  データのインポート
6.  ワークロードを実行して結果を評価する
7.  さらに機能を探索する
8.  環境をクリーンアップして PoC を終了する

## ステップ 1. 成功基準を定義し、テスト計画を作成する {#step-1-define-success-criteria-and-create-a-test-plan}

PoC を通じてTiDB Cloudを評価する場合は、ビジネス ニーズに基づいて関心のある点とそれに対応する技術的な評価基準を決定し、PoC に対する期待と目標を明確にすることをお勧めします。詳細なテスト計画を備えた明確で測定可能な技術基準は、主要な側面に焦点を当て、ビジネス レベルの要件をカバーし、最終的に PoC 手順を通じて回答を得るのに役立ちます。

PoC の目標を特定するには、次の質問を使用してください。

-   ワークロードのシナリオは何ですか?
-   あなたのビジネスのデータセットのサイズまたはワークロードはどれくらいですか?成長率とは何ですか?
-   ビジネスクリティカルなスループットやレイテンシーの要件を含むパフォーマンス要件は何ですか?
-   許容可能な計画的または計画外のダウンタイムの最小値を含む、可用性と安定性の要件は何ですか?
-   業務効率化に必要な指標は何ですか?どのように測定しますか?
-   ワークロードのセキュリティとコンプライアンスの要件は何ですか?

成功基準とテスト計画の作成方法の詳細については、お気軽に<a href="mailto:tidbcloud-support@pingcap.com">PingCAP</a>にお問い合わせください。

## ステップ 2. ワークロードの特性を特定する {#step-2-identify-characteristics-of-your-workload}

TiDB Cloudは、高可用性と大量のデータの強力な一貫性を必要とするさまざまなユースケースに適しています。 [<a href="https://docs.pingcap.com/tidb/stable/overview">TiDB の紹介</a>](https://docs.pingcap.com/tidb/stable/overview)主要な機能とシナリオを示します。それらがビジネス シナリオに適用されるかどうかを確認できます。

-   水平方向のスケールアウトまたはスケールイン
-   金融グレードの高可用性
-   リアルタイムHTAP
-   MySQL 5.7プロトコルおよび MySQL エコシステムとの互換性

分析処理の高速化に役立つカラムナ型storageエンジン[<a href="https://docs.pingcap.com/tidb/stable/tiflash-overview">TiFlash</a>](https://docs.pingcap.com/tidb/stable/tiflash-overview)の使用にも興味があるかもしれません。 PoC 中はいつでもTiFlash機能を使用できます。

## ステップ 3. サインアップして PoC 用の TiDB Dedicatedクラスターを作成する {#step-3-sign-up-and-create-a-tidb-dedicated-cluster-for-the-poc}

PoC 用の TiDB Dedicatedクラスターを作成するには、次の手順を実行します。

1.  次のいずれかの方法で PoC 申請フォームに記入します。

    -   PingCAP Web サイトの[<a href="https://pingcap.com/apply-for-poc/">PoC に応募する</a>](https://pingcap.com/apply-for-poc/)ページに移動して、申請フォームに記入します。
    -   [<a href="https://tidbcloud.com/">TiDB Cloudコンソール</a>](https://tidbcloud.com/)で、 をクリックします。<mdsvgicon name="icon-top-contact-us">右上隅にある**[お問い合わせ] を**クリックし、 **[PoC に申請] を**選択して申請フォームに記入します。</mdsvgicon>

    フォームを送信すると、 TiDB Cloudサポート チームが申請を審査し、連絡し、申請が承認されたらアカウントにクレジットを転送します。 PingCAP サポート エンジニアに連絡して、PoC 手順を支援して、PoC ができるだけスムーズに実行されるようにすることもできます。

2.  PoC 用に[<a href="/tidb-cloud/select-cluster-tier.md#tidb-dedicated">TiDB Dedicated</a>](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターを作成するには、 [<a href="/tidb-cloud/tidb-cloud-quickstart.md">クイックスタート</a>](/tidb-cloud/tidb-cloud-quickstart.md)を参照してください。

クラスターを作成する前に、クラスターのサイジングについてキャパシティ プランニングを行うことをお勧めします。 TiDB、TiKV、またはTiFlashノードの推定数から開始し、パフォーマンス要件を満たすために後でクラスターをスケールアウトできます。詳細については、次のドキュメントを参照するか、サポート チームにお問い合わせください。

-   推定方法の詳細については、 [<a href="/tidb-cloud/size-your-cluster.md">TiDB のサイズを設定する</a>](/tidb-cloud/size-your-cluster.md)を参照してください。
-   TiDB Dedicatedクラスターの構成については、 [<a href="/tidb-cloud/create-tidb-cluster.md">TiDBクラスタを作成する</a>](/tidb-cloud/create-tidb-cluster.md)を参照してください。 TiDB、TiKV、 TiFlash (オプション) のクラスター サイズをそれぞれ構成します。
-   PoC クレジットの消費を効果的に計画および最適化する方法については、このドキュメントの[<a href="#faq">FAQ</a>](#faq)を参照してください。
-   スケーリングの詳細については、 [<a href="/tidb-cloud/scale-tidb-cluster.md">TiDBクラスタを拡張する</a>](/tidb-cloud/scale-tidb-cluster.md)を参照してください。

専用の PoC クラスターが作成されたら、データをロードして一連のテストを実行する準備が整います。 TiDB クラスターに接続する方法については、 [<a href="/tidb-cloud/connect-to-tidb-cluster.md">TiDBクラスタに接続する</a>](/tidb-cloud/connect-to-tidb-cluster.md)を参照してください。

新しく作成されたクラスターの場合は、次の構成に注意してください。

-   デフォルトのタイムゾーン (ダッシュボードの**「作成時刻」**列) は UTC です。次の手順[<a href="/tidb-cloud/manage-user-access.md#set-the-time-zone-for-your-organization">ローカルタイムゾーンを設定する</a>](/tidb-cloud/manage-user-access.md#set-the-time-zone-for-your-organization)でローカルタイムゾーンに変更できます。
-   新しいクラスターのデフォルトのバックアップ設定は、毎日のデータベースの完全バックアップです。希望のバックアップ時間を指定したり、データを手動でバックアップしたりできます。デフォルトのバックアップ時間と詳細については、 [<a href="/tidb-cloud/backup-and-restore.md#backup">TiDBクラスタデータのバックアップと復元</a>](/tidb-cloud/backup-and-restore.md#backup)を参照してください。

## ステップ 4. スキーマと SQL を調整する {#step-4-adapt-your-schemas-and-sql}

次に、テーブルやインデックスを含むデータベース スキーマを TiDB クラスターにロードできます。

PoC クレジットの量には限りがあるため、クレジットの価値を最大化するには、 TiDB Cloudでの互換性テストと予備分析用に[<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta">TiDB Serverlessクラスタ</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta)を作成することをお勧めします。

TiDB Cloud はMySQL 5.7と高い互換性があります。データが MySQL と互換性がある場合、または MySQL と互換性があるように調整できる場合は、データを TiDB に直接インポートできます。

互換性の詳細については、次のドキュメントを参照してください。

-   [<a href="https://docs.pingcap.com/tidb/stable/mysql-compatibility">TiDB と MySQL の互換性</a>](https://docs.pingcap.com/tidb/stable/mysql-compatibility) 。
-   [<a href="https://docs.pingcap.com/tidb/stable/mysql-compatibility#features-that-are-different-from-mysql">MySQL とは異なる TiDB の機能</a>](https://docs.pingcap.com/tidb/stable/mysql-compatibility#features-that-are-different-from-mysql) 。
-   [<a href="https://docs.pingcap.com/tidb/stable/keywords">TiDBのキーワードと予約語</a>](https://docs.pingcap.com/tidb/stable/keywords) 。
-   [<a href="https://docs.pingcap.com/tidb/stable/tidb-limitations">TiDB の制限事項</a>](https://docs.pingcap.com/tidb/stable/tidb-limitations) 。

いくつかのベスト プラクティスを次に示します。

-   スキーマの設定に非効率な点がないか確認してください。
-   不要なインデックスを削除します。
-   効果的なパーティショニングのためのパーティショニング ポリシーを計画します。
-   タイムスタンプのインデックスなど、右側のインデックスの増加によって引き起こされる[<a href="https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#identify-hotspot-issues">ホットスポットの問題</a>](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#identify-hotspot-issues)避けてください。
-   [<a href="https://docs.pingcap.com/tidb/stable/shard-row-id-bits">SHARD_ROW_ID_BITS</a>](https://docs.pingcap.com/tidb/stable/shard-row-id-bits)と[<a href="https://docs.pingcap.com/tidb/stable/auto-random">自動ランダム</a>](https://docs.pingcap.com/tidb/stable/auto-random)を使用して[<a href="https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#identify-hotspot-issues">ホットスポットの問題</a>](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#identify-hotspot-issues)を回避します。

SQL ステートメントの場合は、データ ソースの TiDB との互換性のレベルに応じて SQL ステートメントを調整する必要がある場合があります。

ご不明な点がございましたら、 [<a href="/tidb-cloud/tidb-cloud-support.md">PingCAP</a>](/tidb-cloud/tidb-cloud-support.md)までご連絡ください。

## ステップ 5. データをインポートする {#step-5-import-data}

小規模なデータセットをインポートして実現可能性を迅速にテストすることも、大規模なデータセットをインポートして TiDB データ移行ツールのスループットをテストすることもできます。 TiDB はサンプル データを提供しますが、ビジネスの実際のワークロードを使用してテストを実行することを強くお勧めします。

さまざまな形式のデータをTiDB Cloudにインポートできます。

-   [<a href="/tidb-cloud/import-sample-data.md">SQLファイル形式でサンプルデータをインポートする</a>](/tidb-cloud/import-sample-data.md)
-   [<a href="/tidb-cloud/migrate-from-aurora-bulk-import.md">Amazon Aurora MySQL からの移行</a>](/tidb-cloud/migrate-from-aurora-bulk-import.md)
-   [<a href="/tidb-cloud/import-csv-files.md">Amazon S3 または GCS から CSV ファイルをインポートする</a>](/tidb-cloud/import-csv-files.md)
-   [<a href="/tidb-cloud/import-parquet-files.md">Apache Parquet ファイルをインポートする</a>](/tidb-cloud/import-parquet-files.md)

> **ノート：**
>
> -   TiDB Cloudでサポートされる文字照合順序については、 [<a href="/tidb-cloud/migrate-data-into-tidb.md">MySQL 互換データベースからの移行</a>](/tidb-cloud/migrate-data-into-tidb.md)を参照してください。データが元々どのように保存されているかを理解することは非常に役立ちます。
> -   **データ インポート**ページでのデータ インポートでは、追加の請求料金は発生しません。

## ステップ 6. ワークロードを実行して結果を評価する {#step-6-run-your-workload-and-evaluate-results}

これで、環境を作成し、スキーマを調整し、データをインポートしました。ワークロードをテストする時期が来ました。

ワークロードをテストする前に、必要に応じてデータベースを元の状態に復元できるように、手動バックアップの実行を検討してください。詳細については、 [<a href="/tidb-cloud/backup-and-restore.md#backup">TiDBクラスタデータのバックアップと復元</a>](/tidb-cloud/backup-and-restore.md#backup)を参照してください。

ワークロードを開始した後、次の方法を使用してシステムを観察できます。

-   クラスターの一般的に使用されるメトリクスは、クラスターの概要ページで確認できます。これには、合計 QPS、レイテンシー、接続、 TiFlashリクエスト QPS、 TiFlashリクエスト期間、 TiFlashストレージ サイズ、TiKV ストレージ サイズ、TiDB CPU、TiKV CPU、TiKV IO 読み取り、 TiKV IO 書き込み。 [<a href="/tidb-cloud/monitor-tidb-cluster.md">TiDBクラスタを監視する</a>](/tidb-cloud/monitor-tidb-cluster.md)を参照してください。
-   **[診断] &gt; [ステートメント]**に移動すると、SQL の実行を観察し、システム テーブルにクエリを実行せずにパフォーマンスの問題を簡単に特定できます。 [<a href="/tidb-cloud/tune-performance.md">ステートメント分析</a>](/tidb-cloud/tune-performance.md)を参照してください。
-   **[診断] &gt; [キー ビジュアライザー]**に移動すると、TiDB データ アクセス パターンとデータ ホットスポットを表示できます。 [<a href="/tidb-cloud/tune-performance.md#key-visualizer">キービジュアライザー</a>](/tidb-cloud/tune-performance.md#key-visualizer)を参照してください。
-   これらのメトリクスを独自の Datadog や Prometheus に統合することもできます。 [<a href="/tidb-cloud/third-party-monitoring-integrations.md">サードパーティの監視統合</a>](/tidb-cloud/third-party-monitoring-integrations.md)を参照してください。

次に、テスト結果を評価します。

より正確な評価を得るには、テスト前にメトリクスのベースラインを決定し、実行ごとにテスト結果を適切に記録します。結果を分析することで、 TiDB Cloud がアプリケーションに適しているかどうかを判断できます。一方、これらの結果はシステムの実行ステータスを示しており、メトリックに従ってシステムを調整できます。例えば：

-   システムのパフォーマンスが要件を満たしているかどうかを評価します。合計 QPS とレイテンシーを確認します。システムのパフォーマンスが満足できない場合は、次のようにパフォーマンスを調整できます。

    -   ネットワークレイテンシーを監視し、最適化します。
    -   SQL パフォーマンスを調査して調整します。
    -   モニターと[<a href="https://docs.pingcap.com/tidb/dev/troubleshoot-hot-spot-issues#troubleshoot-hotspot-issues">ホットスポットの問題を解決する</a>](https://docs.pingcap.com/tidb/dev/troubleshoot-hot-spot-issues#troubleshoot-hotspot-issues) ．

-   storageサイズと CPU 使用率を評価し、それに応じて TiDB クラスターをスケールアウトまたはスケールインします。スケーリングの詳細については、 [<a href="#faq">FAQ</a>](#faq)セクションを参照してください。

パフォーマンス チューニングのヒントは次のとおりです。

-   書き込みパフォーマンスの向上

    -   TiDB クラスターをスケールアウトして、書き込みスループットを向上させます ( [<a href="/tidb-cloud/scale-tidb-cluster.md">TiDBクラスタをスケールする</a>](/tidb-cloud/scale-tidb-cluster.md)を参照)。
    -   [<a href="https://docs.pingcap.com/tidb/stable/optimistic-transaction#tidb-optimistic-transaction-model">楽観的トランザクション モデル</a>](https://docs.pingcap.com/tidb/stable/optimistic-transaction#tidb-optimistic-transaction-model)を使用してロックの競合を減らします。

-   クエリのパフォーマンスを向上させる

    -   **[診断] &gt; [ステートメント]**ページで SQL 実行プランを確認します。
    -   **[ダッシュボード] &gt; [キー ビジュアライザー]**ページでホットスポットの問題を確認します。
    -   [**概要] &gt; [容量メトリック]**ページで、TiDB クラスターの容量が不足しているかどうかを監視します。
    -   TiFlash機能を使用して分析処理を最適化します。 [<a href="/tiflash/tiflash-overview.md">HTAPクラスタを使用する</a>](/tiflash/tiflash-overview.md)を参照してください。

## ステップ 7. さらに機能を探索する {#step-7-explore-more-features}

これでワークロードのテストが完了したので、アップグレードやバックアップなど、さらに多くの機能を試すことができます。

-   アップグレード

    TiDB Cloud はTiDB クラスターを定期的にアップグレードしますが、サポート チケットを送信してクラスターのアップグレードをリクエストすることもできます。 [<a href="/tidb-cloud/upgrade-tidb-cluster.md">TiDBクラスタのアップグレード</a>](/tidb-cloud/upgrade-tidb-cluster.md)を参照してください。

-   バックアップ

    ベンダー ロックインを回避するには、毎日の完全バックアップを使用してデータを新しいクラスターに移行し、 [<a href="/dumpling-overview.md">Dumpling</a>](/dumpling-overview.md)を使用してデータをエクスポートします。詳細については、 [<a href="/tidb-cloud/export-data-from-tidb-cloud.md">TiDB からデータをエクスポート</a>](/tidb-cloud/export-data-from-tidb-cloud.md)を参照してください。

## ステップ 8. 環境をクリーンアップして PoC を終了する {#step-8-clean-up-the-environment-and-finish-the-poc}

実際のワークロードを使用してTiDB Cloudをテストし、テスト結果を取得すると、PoC の全サイクルが完了しました。これらの結果は、 TiDB Cloud が期待を満たしているかどうかを判断するのに役立ちます。その一方で、 TiDB Cloudを使用するためのベスト プラクティスを蓄積してきました。

TiDB Cloudが提供する他のノードstorageサイズでの展開など、新しい展開やテストのために TiDB TiDB Cloudを大規模に試したい場合は、 [<a href="/tidb-cloud/select-cluster-tier.md#tidb-dedicated">TiDB Dedicated</a>](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターを作成してTiDB Cloudへのフル アクセスを取得します。

クレジットが残り少なくなり、PoC を続行したい場合は、 [<a href="/tidb-cloud/tidb-cloud-support.md">TiDB Cloudのサポート</a>](/tidb-cloud/tidb-cloud-support.md)に連絡して相談してください。

PoC はいつでも終了してテスト環境を削除できます。詳細については、 [<a href="/tidb-cloud/delete-tidb-cluster.md">TiDBクラスタの削除</a>](/tidb-cloud/delete-tidb-cluster.md)を参照してください。

PoC プロセス、機能リクエスト、製品の改善方法など、サポート チームへのフィードバックは[<a href="https://www.surveymonkey.com/r/L3VVW8R">TiDB Cloudフィードバック フォーム</a>](https://www.surveymonkey.com/r/L3VVW8R)に記入していただければ幸いです。

## FAQ {#faq}

### 1. データのバックアップと復元にはどのくらい時間がかかりますか? {#1-how-long-does-it-take-to-back-up-and-restore-my-data}

TiDB Cloud は、自動バックアップと手動バックアップの 2 種類のデータベース バックアップを提供します。どちらの方法でもデータベース全体をバックアップします。

データのバックアップと復元にかか​​る時間は、テーブルの数、ミラー コピーの数、CPU 負荷のレベルによって異なる場合があります。 1 つの単一 TiKV ノードでのバックアップおよび復元速度は約 50 MB/秒です。

データベースのバックアップおよび復元操作は通常、CPU を集中的に使用し、常に追加の CPU リソースを必要とします。この環境の CPU 使用率に応じて、QPS とトランザクションレイテンシーに影響 (10% ～ 50%) が生じる可能性があります。

### 2. いつスケールアウトおよびスケールインする必要がありますか? {#2-when-do-i-need-to-scale-out-and-scale-in}

スケーリングに関するいくつかの考慮事項を次に示します。

-   ピーク時間またはデータのインポート中に、ダッシュボード上の容量メトリックが上限に達していることが観察された場合 ( [<a href="/tidb-cloud/monitor-tidb-cluster.md">TiDBクラスタを監視する</a>](/tidb-cloud/monitor-tidb-cluster.md)を参照)、クラスターのスケールアウトが必要になる可能性があります。
-   リソース使用率が持続的に低い (たとえば、CPU 使用率が 10% ～ 20% のみである) ことが観察される場合は、クラスターをスケールインしてリソースを節約できます。

コンソール上でクラスターを自分でスケールアウトできます。クラスターでスケールインする必要がある場合は、 [<a href="/tidb-cloud/tidb-cloud-support.md">TiDB Cloudのサポート</a>](/tidb-cloud/tidb-cloud-support.md)に連絡して支援を求める必要があります。スケーリングの詳細については、 [<a href="/tidb-cloud/scale-tidb-cluster.md">TiDBクラスタを拡張する</a>](/tidb-cloud/scale-tidb-cluster.md)を参照してください。サポート チームと連絡を取り合い、正確な進捗状況を追跡できます。データの再バランスによりパフォーマンスに影響を与える可能性があるため、テストを開始する前にスケーリング操作が完了するまで待つ必要があります。

### 3. PoC クレジットを最大限に活用するにはどうすればよいですか? {#3-how-to-make-the-best-use-of-my-poc-credits}

PoC への申請が承認されると、アカウントにクレジットが付与されます。通常、クレジットは 14 日間の PoC に十分です。クレジットは、ノードのタイプとノード数に応じて時間単位で課金されます。詳細については、 [<a href="/tidb-cloud/tidb-cloud-billing.md#credits">TiDB Cloudの請求</a>](/tidb-cloud/tidb-cloud-billing.md#credits)を参照してください。

PoC に残っているクレジットを確認するには、次のスクリーンショットに示すように、ターゲット プロジェクトの[<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページに移動します。

![TiDB Cloud PoC Credits](/media/tidb-cloud/poc-points.png)

または、 をクリックすることもできます。<mdsvgicon name="icon-top-account-settings"> TiDB Cloudコンソールの右上隅にある**[アカウント] を**クリックし、 **[請求] を**クリックし、 **[クレジット]**をクリックしてクレジットの詳細ページを表示します。</mdsvgicon>

クレジットを節約するには、使用していないクラスターを削除します。現在、クラスターを停止することはできません。後で PoC を再開するときにクラスターを復元できるように、クラスターを削除する前にバックアップが最新であることを確認する必要があります。

PoC プロセスが完了した後も未使用のクレジットが残っている場合は、これらのクレジットの有効期限が切れない限り、引き続きそのクレジットを使用して TiDB クラスター料金を支払うことができます。

### 4. PoC を完了するまでに 2 週間以上かかることがありますか? {#4-can-i-take-more-than-2-weeks-to-complete-a-poc}

PoC 試用期間を延長したい場合、またはクレジットが不足している場合は、 [<a href="https://www.pingcap.com/contact-us/">PingCAP に連絡する</a>](https://www.pingcap.com/contact-us/)をサポートしてください。

### 5. 技術的な問題で行き詰まっています。 PoC に関するサポートを受けるにはどうすればよいですか? {#5-i-m-stuck-with-a-technical-problem-how-do-i-get-help-for-my-poc}

いつでも[<a href="/tidb-cloud/tidb-cloud-support.md">TiDB Cloudサポートにお問い合わせください</a>](/tidb-cloud/tidb-cloud-support.md)で助けを求めることができます。
