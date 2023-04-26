---
title: Explore Your Data with AI-Powered Chat2Query (beta)
summary: Learn how to use Chat2Query, an AI-powered SQL editor in the TiDB Cloud console, to maximize your data value.
---

# AI を活用した Chat2Query (ベータ版) を使用してデータを探索する {#explore-your-data-with-ai-powered-chat2query-beta}

TiDB Cloud はAI によって強化されています。 [TiDB Cloudコンソール](https://tidbcloud.com/)の AI 搭載 SQL エディターである Chat2Query (ベータ版) を使用して、データの価値を最大化できます。

Chat2Query では、単に`--`を入力してから命令を入力し、AI に SQL クエリを自動的に生成させるか、SQL クエリを手動で記述してから、ターミナルを使用せずにデータベースに対して SQL クエリを実行することができます。クエリ結果をテーブルで直感的に検索し、クエリ ログを簡単に確認できます。

TiDB Cloud は、 RESTful インターフェイスである Chat2Query API も提供します。詳細については、 [Chat2Query API の使用を開始する](/tidb-cloud/use-chat2query-api.md)を参照してください。

> **ノート：**
>
> Chat2Query は[Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターでのみ使用できます。

## ユースケース {#use-cases}

Chat2Query の推奨される使用例は次のとおりです。

-   Chat2Query の AI 機能を使用して、複雑な SQL クエリを即座に生成できます。
-   TiDB の MySQL 互換性をすばやくテストします。
-   TiDB SQL機能を簡単に調べます。

## 制限 {#limitation}

AI によって生成された SQL クエリは 100% 正確ではなく、さらに調整が必要になる場合があります。

## Chat2Query へのアクセス {#access-chat2query}

1.  プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

    > **ヒント：**
    >
    > 複数のプロジェクトがある場合は、プロジェクト リストを表示し、左上隅の ☰ ホバー メニューから別のプロジェクトに切り替えることができます。

2.  クラスター名をクリックし、左側のナビゲーション ペインで**[Chat2Query]**をクリックします。

## AI による SQL クエリの生成を有効または無効にする {#enable-or-disable-ai-to-generate-sql-queries}

PingCAP は、ユーザーのデータのプライバシーとセキュリティを最優先事項としています。 Chat2Query の AI 機能は、データ自体ではなく、データベース スキーマにアクセスして SQL クエリを生成するだけで済みます。詳細については、 [Chat2Query プライバシーFAQ](https://www.pingcap.com/privacy-policy/privacy-chat2query)を参照してください。

初めて Chat2Query にアクセスすると、PingCAP と OpenAI がコード スニペットを使用してサービスを調査および改善することを許可するかどうかについてのダイアログが表示されます。

-   AI が SQL クエリを生成できるようにするには、チェックボックスを選択して**[保存して開始] を**クリックします。
-   AI による SQL クエリの生成を無効にするには、このダイアログを直接閉じます。

初めてアクセスした後でも、次のように AI 設定を変更できます。

-   AI を有効にするには、Chat2Query の右上隅にある**[データ探索のために AI パワーを有効にする]**をクリックします。
-   AI を無効にするには、<mdsvgicon name="icon-top-account-settings"> [TiDB Cloudコンソール](https://tidbcloud.com/)の右上隅にある**[アカウント] を**クリックし、 <strong>[アカウント設定]</strong>をクリックし、 <strong>[プライバシー]</strong>タブをクリックして、 <strong>[AI によるデータ探索]</strong>オプションを無効にします。</mdsvgicon>

## SQL クエリを作成して実行する {#write-and-run-sql-queries}

Chat2Query では、事前に構築されたサンプル データセットまたは独自のデータセットを使用して、SQL クエリを作成および実行できます。

1.  SQL クエリを記述します。

    -   AI が有効になっている場合は、 `--`入力してから指示を入力し、AI が SQL クエリを自動的に生成するか、SQL クエリを手動で記述できるようにします。

        AI によって生成された SQL クエリの場合、 <kbd>Tab を</kbd>押して受け入れ、必要に応じてさらに編集するか、 <kbd>Esc</kbd>を押して拒否できます。

    -   AI が無効になっている場合は、SQL クエリを手動で記述します。

2.  SQL クエリを実行します。

    <SimpleTab>
     <div label="macOS">

    macOS の場合:

    -   エディターにクエリが 1 つしかない場合、それを実行するには、 **⌘ + Enter**を押すか、 <svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg><strong>実行します</strong>。

    -   エディターに複数のクエリがある場合、そのうちの 1 つまたは複数を順番に実行するには、カーソルでターゲット クエリの行を選択し、 **⌘ + Enter**を押すか、 <strong>[実行]</strong>をクリックします。

    -   エディターですべてのクエリを順番に実行するには、 **⇧ + ⌘ + Enter を**押すか、カーソルですべてのクエリの行を選択して<strong>[実行]</strong>をクリックします。

    </div>

    <div label="Windows/Linux">

    Windows または Linux の場合:

    -   エディターにクエリが 1 つしかない場合、それを実行するには、 **Ctrl + Enter を**押すか、 <svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg><strong>実行します</strong>。

    -   エディターに複数のクエリがある場合、それらの 1 つまたは複数を順番に実行するには、カーソルでターゲット クエリの行を選択し、 **Ctrl + Enter**を押すか、 [<strong>実行]</strong>をクリックします。

    -   エディターですべてのクエリを順番に実行するには、 **Shift + Ctrl + Enter を**押すか、カーソルですべてのクエリの行を選択して<strong>[実行]</strong>をクリックします。

    </div>
     </SimpleTab>

クエリを実行すると、ページの下部にクエリ ログと結果がすぐに表示されます。

## SQL ファイルの管理 {#manage-sql-files}

Chat2Query では、SQL クエリを別の SQL ファイルに保存し、次のように SQL ファイルを管理できます。

-   SQL ファイルを追加するには、 **[SQL ファイル]**タブで<strong>[+]</strong>をクリックします。
-   SQL ファイルの名前を変更するには、ファイル名にカーソルを移動し、ファイル名の横にある**[...]**をクリックして、 <strong>[名前の変更]</strong>を選択します。
-   SQL ファイルを削除するには、カーソルをファイル名に移動し、ファイル名の横にある**[...]**をクリックして、 <strong>[削除]</strong>を選択します。 <strong>[SQL ファイル]</strong>タブに SQL ファイルが 1 つしかない場合、そのファイルは削除できないことに注意してください。

## SQL ファイルからエンドポイントを生成する {#generate-an-endpoint-from-a-sql-file}

TiDB Cloud は、カスタム API エンドポイントを使用して HTTPS 要求を介してTiDB Cloudデータにアクセスできるようにする[データ サービス (ベータ)](/tidb-cloud/data-service-overview.md)機能を提供します。 Chat2Query では、次の手順を実行して、SQL ファイルから Data Service (ベータ) でエンドポイントを生成できます。

1.  カーソルをファイル名に移動し、ファイル名の横にある**[...]**をクリックして、 <strong>[エンドポイントの生成]</strong>を選択します。
2.  **[エンドポイントの生成]**ダイアログ ボックスで、エンドポイントを生成するデータ アプリを選択し、エンドポイント名を入力します。
3.  **[生成]**をクリックします。エンドポイントが生成され、その詳細ページが表示されます。

詳細については、 [エンドポイントを管理する](/tidb-cloud/data-service-manage-endpoint.md)を参照してください。

## Chat2Query 設定の管理 {#manage-chat2query-settings}

デフォルトでは、Chat2Query はクエリ結果の最大行数を 500 に制限し、システム データベース スキーマを表示せず、 **[スキーマ]**タブで[Chat2Query API](/tidb-cloud/use-chat2query-api.md)を無効にします。

設定を変更するには、次の手順を実行します。

1.  Chat2Query の右上隅にある**[...]**をクリックし、 <strong>[設定]</strong>を選択します。
2.  必要に応じて設定を変更してください。
3.  **[保存]**をクリックします。
