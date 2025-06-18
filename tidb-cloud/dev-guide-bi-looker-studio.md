---
title: Connect to TiDB Cloud Serverless with Looker Studio
summary: Looker Studio を使用してTiDB Cloud Serverless に接続する方法を学習します。
---

# Looker Studio でTiDB Cloud Serverless に接続する {#connect-to-tidb-cloud-serverless-with-looker-studio}

TiDB は MySQL 互換のデータベース、 TiDB Cloud Serverless は完全に管理された TiDB サービス、 [ルッカースタジオ](https://lookerstudio.google.com/)さまざまなソースからのデータを視覚化できる無料の Web ベースの BI ツールです。

このチュートリアルでは、Looker Studio を使用してTiDB Cloud Serverless クラスターに接続する方法を学習します。

> **注記：**
>
> このチュートリアルのほとんどの手順はTiDB Cloud Dedicatedでも同様に機能します。ただし、 TiDB Cloud Dedicatedの場合は、以下の点にご注意ください。
>
> -   [ファイルからTiDB Cloudにデータをインポートする](/tidb-cloud/tidb-cloud-migration-overview.md#import-data-from-files-to-tidb-cloud)に従ってデータセットをインポートします。
> -   [TiDB Cloud専用に接続](/tidb-cloud/connect-via-standard-connection.md)に従ってクラスタの接続情報を取得します。TiDB TiDB Cloud Dedicatedに接続する場合は、 `142.251.74.0/23`からのアクセスを許可する必要があります。Looker Studioからの接続の詳細については、 [Looker Studio ドキュメント](https://support.google.com/looker-studio/answer/7088031#zippy=%2Cin-this-article)参照してください。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   Googleアカウント
-   TiDB Cloudサーバーレスクラスター

**TiDB Cloud Serverless クラスターがない場合は、次のように作成できます。**

-   [TiDB Cloud Serverless クラスターを作成する](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-tidb-cloud-serverless-cluster)

## ステップ1.データセットをインポートする {#step-1-import-a-dataset}

TiDB Cloud Serverless のインタラクティブ チュートリアルで提供されている S&amp;P 500 データセットをインポートできます。

1.  [**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、右下隅の**「？」**をクリックします。**ヘルプ**ダイアログが表示されます。

2.  ダイアログで、 **[インタラクティブ チュートリアル]**をクリックし、 **[S&amp;P 500 分析]**をクリックします。

3.  TiDB Cloud Serverless クラスターを選択し、 **「Import Dataset」**をクリックして S&amp;P 500 データセットをクラスターにインポートします。

4.  インポート ステータスが**IMPORTED**に変わったら、 **[チュートリアルを終了]**をクリックしてこのダイアログを閉じます。

インポート中に問題が発生した場合は、次の手順に従ってこのインポート タスクをキャンセルできます。

1.  [**クラスター**](https://tidbcloud.com/project/clusters)ページで、 TiDB Cloud Serverless クラスターの名前をクリックして、概要ページに移動します。
2.  左側のナビゲーション ペインで、 **[データ]** &gt; **[インポート] を**クリックします。
3.  **sp500-insight**という名前のインポート タスクを見つけて、 **[アクション**] 列の**[...]**をクリックし、 **[キャンセル]**をクリックします。

## ステップ2. クラスターの接続情報を取得する {#step-2-get-the-connection-information-for-your-cluster}

1.  [**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログで、 **「接続先」を**`General`に設定し、 **「パスワードの生成」**をクリックしてランダム パスワードを作成します。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」**をクリックして新しいパスワードを生成します。

4.  [CA証明書](https://letsencrypt.org/certs/isrgrootx1.pem)ダウンロードしてください。

    > **ヒント：**
    >
    > TiDB Cloud Serverless では、クライアントとクラスター間の安全な TLS 接続が必要なので、Looker Studio の接続設定にはこの CA 証明書が必要です。

## ステップ3. Looker Studioを使用してTiDBクラスタに接続する {#step-3-connect-to-your-tidb-cluster-with-looker-studio}

1.  [ルッカースタジオ](https://lookerstudio.google.com/)にログインし、左側のナビゲーション ペインで**[作成]** &gt; **[レポート]**をクリックします。

2.  表示されたページで、 **MySQL**コネクタを検索して選択し、 **AUTHORIZE を**クリックします。

3.  **基本**設定ペインで、接続パラメータを構成します。

    -   **ホスト名または IP** : TiDB Cloud Serverless 接続ダイアログから`HOST`パラメータを入力します。
    -   **ポート (オプション)** : TiDB Cloud Serverless 接続ダイアログから`PORT`パラメータを入力します。
    -   **データベース**: 接続先のデータベースを入力します。このチュートリアルでは`sp500insight`と入力します。
    -   **ユーザー名**: TiDB Cloud Serverless 接続ダイアログから`USERNAME`パラメータを入力します。
    -   **パスワード**: TiDB Cloud Serverless 接続ダイアログから`PASSWORD`パラメータを入力します。
    -   **SSL を有効にする**: このオプションを選択し、 **MySQL SSL クライアントコンフィグレーションファイル**の右側にあるアップロード アイコンをクリックして、 [ステップ2](#step-2-get-the-connection-information-for-your-cluster)からダウンロードした CA ファイルをアップロードします。

    ![Looker Studio: configure connection settings for TiDB Cloud Serverless](/media/tidb-cloud/looker-studio-configure-connection.png)

4.  **[認証]**をクリックします。

認証が成功すると、データベース内のテーブルが表示されます。

## ステップ4. シンプルなチャートを作成する {#step-4-create-a-simple-chart}

これで、TiDB クラスターをデータ ソースとして使用し、データを含む簡単なグラフを作成できるようになりました。

1.  右側のペインで、 **[カスタム クエリ]**をクリックします。

    ![Looker Studio: custom query](/media/tidb-cloud/looker-studio-custom-query.png)

2.  次のコードを**[カスタム クエリの入力]**領域にコピーし、右下隅の**[追加]**をクリックします。

    ```sql
    SELECT sector,
        COUNT(*)                                                                      AS companies,
        ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC )                                   AS companies_ranking,
        SUM(market_cap)                                                               AS total_market_cap,
        ROW_NUMBER() OVER (ORDER BY SUM(market_cap) DESC )                            AS total_market_cap_ranking,
        SUM(revenue_growth * weight) / SUM(weight)                                    AS avg_revenue_growth,
        ROW_NUMBER() OVER (ORDER BY SUM(revenue_growth * weight) / SUM(weight) DESC ) AS avg_revenue_growth_ranking
    FROM companies
        LEFT JOIN index_compositions ic ON companies.stock_symbol = ic.stock_symbol
    GROUP BY sector
    ORDER BY 5 ASC;
    ```

    **「このレポートにデータを追加しようとしています」という**ダイアログが表示された場合は、 **「レポートに追加」**をクリックします。すると、レポートに表が表示されます。

3.  レポートのツールバーで、 **「グラフの追加」**をクリックし、 `Line`カテゴリで`Combo chart`選択します。

4.  右側の**チャート**設定ペインで、次のパラメータを設定します。

    -   **セットアップ**タブで：
        -   **寸法**: `sector` .
        -   **メトリック**: `companies`と`total_market_cap` 。
    -   **[スタイル]**タブ:
        -   シリーズ＃1：オプション`Line`と軸`Right`選択します。
        -   シリーズ＃2：オプション`Bars`と軸`Left`選択します。
    -   他のフィールドはデフォルトのままにします。

すると、次のようなコンボ チャートが表示されます。

![Looker Studio: A simple Combo chart](/media/tidb-cloud/looker-studio-simple-chart.png)

## 次のステップ {#next-steps}

-   [Looker Studio ヘルプ](https://support.google.com/looker-studio)から Looker Studio の使い方を詳しく学びます。
-   [開発者ガイド](/develop/dev-guide-overview.md)の[データを挿入する](/develop/dev-guide-insert-data.md) 、 [データを更新する](/develop/dev-guide-update-data.md) 、 [データを削除する](/develop/dev-guide-delete-data.md) 、 [単一テーブルの読み取り](/develop/dev-guide-get-data-from-single-table.md) 、 [取引](/develop/dev-guide-transaction-overview.md) 、 [SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)などの章で、 TiDB アプリケーション開発のベスト プラクティスを学習します。
-   プロフェッショナル[TiDB開発者コース](https://www.pingcap.com/education/)を通じて学び、試験に合格すると[TiDB認定](https://www.pingcap.com/education/certification/)獲得します。

## ヘルプが必要ですか? {#need-help}

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](https://tidb.support.pingcap.com/)についてコミュニティに質問してください。
