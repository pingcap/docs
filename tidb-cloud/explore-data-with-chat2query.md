---
title: Explore Your Data with AI-Powered Chat2Query (beta)
summary: Learn how to use Chat2Query, an AI-powered SQL editor in the TiDB Cloud console, to maximize your data value.
---

# AI を活用した Chat2Query (ベータ版) でデータを探索する {#explore-your-data-with-ai-powered-chat2query-beta}

TiDB CloudはAI を活用しています。 [TiDB Cloudコンソール](https://tidbcloud.com/)の AI を活用した SQL エディターである Chat2Query (ベータ版) を使用すると、データの価値を最大化できます。

Chat2Query では、 `--`入力してから AI に SQL クエリを自動的に生成させる指示を入力するか、SQL クエリを手動で作成して、ターミナルを使用せずにデータベースに対して SQL クエリを実行することができます。クエリ結果をテーブルで直感的に見つけたり、クエリログを簡単に確認したりできます。

> **注記：**
>
> Chat2Query は、AWS でホストされている v6.5.0 以降の TiDB クラスターでサポートされています。
>
> -   [TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターの場合、Chat2Query はデフォルトで使用可能です。
> -   [TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターの場合、Chat2Query はリクエストに応じてのみ利用可能です。 TiDB 専用クラスターで Chat2Query を使用するには、 [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

## ユースケース {#use-cases}

Chat2Query の推奨される使用例は次のとおりです。

-   Chat2Query の AI 機能を使用すると、複雑な SQL クエリを即座に生成できます。
-   TiDB の MySQL 互換性をすぐにテストします。
-   TiDB SQL の機能を簡単に探索できます。

## 制限 {#limitation}

-   AI によって生成された SQL クエリは 100% 正確ではないため、さらに調整が必要な場合があります。
-   [Chat2Query API](/tidb-cloud/use-chat2query-api.md) [TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターで使用できます。 [TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターで Chat2Query API を使用するには、 [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

## Chat2Query にアクセスする {#access-chat2query}

1.  プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

    > **ヒント：**
    >
    > 複数のプロジェクトがある場合は、<mdsvgicon name="icon-left-projects">左下隅の をクリックして、別のプロジェクトに切り替えます。</mdsvgicon>

2.  クラスター名をクリックし、左側のナビゲーション ウィンドウで**[Chat2Query]**をクリックします。

    > **注記：**
    >
    > 次の場合、 **Chat2Query**エントリは灰色で表示され、クリックできません。
    >
    > -   TiDB 専用クラスターは v6.5.0 より前です。 Chat2Query を使用するには、クラスターをアップグレードするために[TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)を契約する必要があります。
    > -   TiDB 専用クラスターが作成されたばかりで、Chat2Query の実行環境はまだ準備中です。この場合、数分待つと Chat2Query が使用可能になります。
    > -   TiDB 専用クラスターは[一時停止した](/tidb-cloud/pause-or-resume-tidb-cluster.md)です。

## AI による SQL クエリの生成を有効または無効にする {#enable-or-disable-ai-to-generate-sql-queries}

PingCAP は、ユーザーのデータのプライバシーとセキュリティを最優先事項としています。 Chat2Query の AI 機能は、データ自体ではなく、データベース スキーマにアクセスして SQL クエリを生成することのみが必要です。詳細については、 [Chat2Query のプライバシーに関するFAQ](https://www.pingcap.com/privacy-policy/privacy-chat2query)を参照してください。

初めて Chat2Query にアクセスすると、PingCAP と OpenAI がコード スニペットを使用してサービスを調査および改善することを許可するかどうかを尋ねるダイアログが表示されます。

-   AI が SQL クエリを生成できるようにするには、チェックボックスを選択し、 **[保存して開始]**をクリックします。
-   AI による SQL クエリの生成を無効にするには、このダイアログを直接閉じます。

初回アクセス後も、次のように AI 設定を変更できます。

-   AI を有効にするには、Chat2Query の右上隅にある**[データ探索のための AI パワーを有効にする]**をクリックします。
-   AI を無効にするには、<mdsvgicon name="icon-top-account-settings"> [TiDB Cloudコンソール](https://tidbcloud.com/)の左下隅にある**[アカウント設定]**をクリックし、 **[プライバシー]**タブをクリックして、 **AI を利用したデータ探索**オプションを無効にします。</mdsvgicon>

## SQL クエリを作成して実行する {#write-and-run-sql-queries}

Chat2Query では、独自のデータセットを使用して SQL クエリを作成および実行できます。

1.  SQL クエリを作成します。

    -   AI が有効な場合は、 `--`を入力してから AI に SQL クエリを自動的に生成させるか、SQL クエリを手動で作成するかの指示を入力するだけです。

        AI によって生成された SQL クエリの場合は、 <kbd>Tab キー</kbd>を押して受け入れ、必要に応じてさらに編集するか、 <kbd>Esc キー</kbd>を押して拒否することができます。

    -   AI が無効になっている場合は、SQL クエリを手動で作成します。

2.  SQL クエリを実行します。

    <SimpleTab>
     <div label="macOS">

    macOS の場合:

    -   エディターにクエリが 1 つしかない場合、それを実行するには、 **⌘ + Enter キー**を押すか、 <svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg>**走る**。

    -   エディターに複数のクエリがある場合、1 つまたは複数のクエリを順番に実行するには、カーソルでターゲット クエリの行を選択し、 **⌘ + Enter**を押すか、 **[実行]**をクリックします。

    -   エディターですべてのクエリを順番に実行するには、 **⇧ + ⌘ + Enter を**押すか、カーソルですべてのクエリの行を選択し、 **Run**をクリックします。

    </div>

    <div label="Windows/Linux">

    Windows または Linux の場合:

    -   エディターにクエリが 1 つしかない場合、それを実行するには、 **Ctrl + Enter を**押すか、 <svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg>**走る**。

    -   エディターに複数のクエリがある場合、1 つまたは複数のクエリを順番に実行するには、カーソルでターゲット クエリの行を選択し、 **Ctrl + Enter**を押すか、 [**実行]**をクリックします。

    -   エディターですべてのクエリを順番に実行するには、 **Shift + Ctrl + Enter を**押すか、カーソルですべてのクエリの行を選択し、 **[実行]**をクリックします。

    </div>
     </SimpleTab>

クエリを実行すると、ページの下部にクエリのログと結果がすぐに表示されます。

## SQLファイルを管理する {#manage-sql-files}

Chat2Query では、SQL クエリをさまざまな SQL ファイルに保存し、次のように SQL ファイルを管理できます。

-   SQL ファイルを追加するには、 **[SQL ファイル]**タブで**[+]**をクリックします。
-   SQL ファイルの名前を変更するには、ファイル名の上にカーソルを移動し、ファイル名の横にある**[...]**をクリックして、 **[名前の変更]**を選択します。
-   SQL ファイルを削除するには、ファイル名の上にカーソルを移動し、ファイル名の横にある**[...]**をクリックして、 **[削除]**を選択します。 **[SQL ファイル]**タブに SQL ファイルが 1 つしかない場合は、削除できないことに注意してください。

## API経由でChat2Queryにアクセス {#access-chat2query-via-api}

Chat2Query には UI 経由でアクセスするだけでなく、API 経由でアクセスすることもできます。これを行うには、まず Chat2Query データ アプリを作成する必要があります。

Chat2Query では、次のように Chat2Query データ アプリにアクセスしたり、Chat2Query データ アプリを作成したりできます。

1.  右上隅の**[...]**をクリックし、 **[API 経由で Chat2Query にアクセス] を**クリックします。
2.  表示されたダイアログで、次のいずれかを実行します。

    -   新しい Chat2Query データ アプリを作成するには、 **[新しい Chat2Query データ アプリ]**をクリックします。
    -   既存の Chat2Query データ アプリにアクセスするには、ターゲット データ アプリの名前をクリックします。

詳細については、 [Chat2Query API を使ってみる](/tidb-cloud/use-chat2query-api.md)を参照してください。

## SQL ファイルからエンドポイントを生成する {#generate-an-endpoint-from-a-sql-file}

TiDB クラスターの場合、 TiDB Cloud は、カスタム API エンドポイントを使用して HTTPS リクエスト経由でTiDB Cloudデータにアクセスできるようにする[データサービス（ベータ版）](/tidb-cloud/data-service-overview.md)機能を提供します。 Chat2Query では、次の手順を実行して SQL ファイルから Data Service (ベータ) のエンドポイントを生成できます。

1.  ファイル名の上にカーソルを移動し、ファイル名の横にある**[...]**をクリックして、 **[エンドポイントの生成]**を選択します。
2.  **[エンドポイントの生成]**ダイアログ ボックスで、エンドポイントを生成するデータ アプリを選択し、エンドポイント名を入力します。
3.  **「生成」**をクリックします。エンドポイントが生成され、その詳細ページが表示されます。

詳細については、 [エンドポイントを管理する](/tidb-cloud/data-service-manage-endpoint.md)を参照してください。

## Chat2Query 設定を管理する {#manage-chat2query-settings}

Chat2Query では、次の設定を変更できます。

-   クエリ結果の最大行数
-   **[スキーマ]**タブにシステム データベース スキーマを表示するかどうか

設定を変更するには、次の手順を実行します。

1.  Chat2Query の右上隅で**[...]**をクリックし、 **[設定]**を選択します。
2.  必要に応じて設定を変更してください。
3.  **「保存」**をクリックします。
