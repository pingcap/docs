---
title: Connect to TiDB with DBeaver
summary: DBeaver Communityを使用してTiDBに接続する方法を学びましょう。
aliases: ['/ja/tidb/stable/dev-guide-gui-dbeaver/','/ja/tidb/dev/dev-guide-gui-dbeaver/','/ja/tidbcloud/dev-guide-gui-dbeaver/']
---

# DBeaverを使用してTiDBに接続する {#connect-to-tidb-with-dbeaver}

TiDBはMySQL互換データベースであり、 [DBeaverコミュニティ](https://dbeaver.io/download/)開発者、データベース管理者、アナリスト、およびデータを扱うすべての人向けの無料のクロスプラットフォームデータベースツールです。

このチュートリアルでは、DBeaver Communityを使用してTiDBに接続する方法を学ぶことができます。

> **注記：**
>
> このチュートリアルは、 TiDB Cloud Starter、 TiDB Cloud Essential、 TiDB Cloud Premium、 TiDB Cloud Dedicated、およびTiDB Self-Managedに対応しています。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、以下が必要です。

-   [DBeaver Community **23.0.3**以降](https://dbeaver.io/download/)。
-   TiDBクラスタ。

**TiDBクラスタをお持ちでない場合は、以下の手順で作成できます。**

-   (推奨) [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)。
-   [ローカルテスト用のTiDBセルフマネージドクラスタをデプロイ。](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番本番のTiDBセルフマネージドクラスタをデプロイ。](/production-deployment-using-tiup.md)

さらに、 **Windows**上の DBeaver からTiDB Cloud StarterまたはTiDB Cloud Essential のパブリックエンドポイントに接続するには、以下の手順で追加の SSL 証明書 (ISRG Root X1) を設定する必要があります。設定しない場合、接続は失敗します。その他のオペレーティングシステムの場合は、これらの手順はスキップできます。

1.  [ISRGルートX1証明書](https://letsencrypt.org/certs/isrgrootx1.pem)をダウンロードし、 `C:\certs\isrgrootx1.pem`などのローカル パスに保存します。

2.  DBeaverで接続設定を編集し、 **SSL**タブに移動します。

    1.  **「SSLを使用する」**を選択してください。
    2.  **CA証明書の**フィールドで、ダウンロードした`isrgrootx1.pem`ファイルを選択します。
    3.  その他の証明書欄は空欄のままにしてください。

3.  SSL 構成の競合を避けるため、**Driverのプロパティ**タブで、既存の`sslMode` 、 `useSSL` 、または`requireSSL`エントリをすべて削除してください。

4.  **接続テスト**をクリックして、接続が成功したことを確認してください。

## TiDBに接続する {#connect-to-tidb}

選択したTiDBのデプロイオプションに応じて、TiDBに接続してください。

<SimpleTab>
<div label="TiDB Cloud Starter or Essential">

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックして、概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  接続ダイアログの設定がご使用のオペレーティング環境と一致していることを確認してください。

    -   **接続タイプ**は`Public`に設定されています。
    -   **ブランチ**は`main`に設定されています。
    -   **Connect With は**`DBeaver`に設定されています。
    -   お使いの環境に合った**オペレーティングシステム**を選択してください。

4.  **「パスワードを生成」を**クリックすると、ランダムなパスワードが生成されます。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードをリセット」**をクリックして新しいパスワードを生成できます。

5.  DBeaverを起動し、左上隅の**「新しいデータベース接続」**をクリックします。 **「データベースへの接続**」ダイアログで、リストから**TiDBを**選択し、 **「次へ」**をクリックします。

    ![Select TiDB as the database in DBeaver](/media/develop/dbeaver-select-database.jpg)

6.  TiDB Cloud接続ダイアログから接続文字列をコピーします。DBeaverで、 **「接続方法**」に**「URL」**を選択し、 **URL**フィールドに接続文字列を貼り付けます。

7.  **「認証（データベースネイティブ）」**セクションで、**ユーザー名**と**パスワード**を入力してください。例は以下のとおりです。

    ![Configure connection settings for TiDB Cloud Starter](/media/develop/dbeaver-connection-settings-serverless.jpg)

8.  **「接続テスト」**をクリックして、対象のTiDB Cloud StarterまたはEssentialインスタンスへの接続を検証してください。

    **「ドライバファイルのダウンロード」**ダイアログが表示されたら、 **「ダウンロード」**をクリックしてドライバファイルを入手してください。

    ![Download driver files](/media/develop/dbeaver-download-driver.jpg)

    接続テストが成功すると、以下のように**接続テスト**ダイアログが表示されます。 **「OK」**をクリックして閉じます。

    ![Connection test result](/media/develop/dbeaver-connection-test.jpg)

9.  接続設定を保存するには、 **「完了」**をクリックしてください。

</div>
<div label="TiDB Cloud Premium">

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud Premiumインスタンスの名前をクリックして概要ページに移動します。

2.  左側のナビゲーションペインで、 **[設定]** &gt; **[ネットワーク]**をクリックします。

3.  **ネットワークの**ページで、 **[パブリックエンドポイント****を有効にする]**をクリックし、次に**[IP アドレスの追加]**をクリックします。

    クライアントのIPアドレスがアクセスリストに追加されていることを確認してください。

4.  左側のナビゲーションペインで**「概要」**をクリックすると、インスタンスの概要ページに戻ります。

5.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

6.  接続ダイアログで、 **「接続タイプ」**ドロップダウンリストから**「パブリック」**を選択します。

    -   公開エンドポイントがまだ有効化中であることを示すメッセージが表示された場合は、処理が完了するまでお待ちください。
    -   まだパスワードを設定していない場合は、ダイアログの**「ルートパスワードを設定」**をクリックしてください。
    -   サーバー証明書を確認する必要がある場合、または接続に失敗して認証局（CA）証明書が必要な場合は、 **「CA証明書」**をクリックしてダウンロードしてください。
    -   **パブリック**接続タイプに加えて、 TiDB Cloud Premium は**プライベート エンドポイント**接続をサポートします。詳細については、 [AWS PrivateLink経由でTiDB Cloud Premiumに接続します。](/tidb-cloud/premium/connect-to-premium-via-aws-private-endpoint.md)を参照してください。

7.  DBeaverを起動し、左上隅の**「新しいデータベース接続」**をクリックします。 **「データベースへの接続**」ダイアログで、リストから**TiDBを**選択し、 **「次へ」**をクリックします。

8.  適切な接続文字列をコピーして、DBeaverの接続パネルに貼り付けてください。DBeaverのフィールドとTiDB Cloud Premiumの接続文字列のマッピングは以下のとおりです。

    | DBeaverフィールド | TiDB Cloud Premium接続文字列 |
    | ------------ | ----------------------- |
    | サーバーホスト      | `{host}`                |
    | ポート          | `{port}`                |
    | ユーザー名        | `{user}`                |
    | パスワード        | `{password}`            |

    SSL設定は無効のままにしてください。

9.  **「接続テスト」**をクリックして、 TiDB Cloud Premiumインスタンスへの接続を検証してください。

10. 接続設定を保存するには、 **「完了」**をクリックしてください。

</div>
<div label="TiDB Cloud Dedicated">

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud Dedicatedクラスタの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  接続ダイアログで、「**接続タイプ」**ドロップダウンリストから**「パブリック」**を選択し、 **「CA証明書」**をクリックしてCA証明書をダウンロードします。

    IP アクセス リストを設定していない場合は、最初の接続の前に、 **[IP アクセス リストの設定] をクリックするか、「IP アクセス リストを設定する」**の手順に従って[IPアクセスリストを設定する](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)。

    TiDB Cloud Dedicated は、**パブリック**接続タイプに加えて、**プライベート エンドポイント**および**VPC ピアリング**接続タイプもサポートしています。詳細については、 [TiDB Cloud Dedicatedクラスタに接続します](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)参照してください。

4.  DBeaverを起動し、左上隅の**「新しいデータベース接続」**をクリックします。 **「データベースへの接続**」ダイアログで、リストから**TiDBを**選択し、 **「次へ」**をクリックします。

    ![Select TiDB as the database in DBeaver](/media/develop/dbeaver-select-database.jpg)

5.  適切な接続文字列をコピーして、DBeaverの接続パネルに貼り付けてください。DBeaverのフィールドとTiDB Cloud Dedicatedの接続文字列のマッピングは以下のとおりです。

    | DBeaverフィールド | TiDB Cloud Dedicated接続文字列 |
    | ------------ | ------------------------- |
    | サーバーホスト      | `{host}`                  |
    | ポート          | `{port}`                  |
    | ユーザー名        | `{user}`                  |
    | パスワード        | `{password}`              |

    例えば、以下のような例があります。

    ![Configure connection settings for TiDB Cloud Dedicated](/media/develop/dbeaver-connection-settings-dedicated.jpg)

6.  **「接続テスト」**をクリックして、 TiDB Cloud Dedicatedクラスターへの接続を検証してください。

    **「ドライバファイルのダウンロード」**ダイアログが表示されたら、 **「ダウンロード」**をクリックしてドライバファイルを入手してください。

    ![Download driver files](/media/develop/dbeaver-download-driver.jpg)

    接続テストが成功すると、以下のように**接続テスト**ダイアログが表示されます。 **「OK」**をクリックして閉じます。

    ![Connection test result](/media/develop/dbeaver-connection-test.jpg)

7.  接続設定を保存するには、 **「完了」**をクリックしてください。

</div>
<div label="TiDB Self-Managed" value="tidb">

1.  DBeaverを起動し、左上隅の**「新しいデータベース接続」**をクリックします。 **「データベースへの接続**」ダイアログで、リストから**TiDBを**選択し、 **「次へ」**をクリックします。

    ![Select TiDB as the database in DBeaver](/media/develop/dbeaver-select-database.jpg)

2.  以下の接続パラメータを設定してください。

    -   **サーバーホスト**：TiDBセルフマネージドクラスタのIPアドレスまたはドメイン名。
    -   **ポート**：TiDBセルフマネージドクラスタのポート番号。
    -   **ユーザー名**：TiDBセルフマネージドクラスタに接続するために使用するユーザー名。
    -   **パスワード**：ユーザー名のパスワード。

    例えば、以下のような例があります。

    ![Configure connection settings for TiDB Self-Managed](/media/develop/dbeaver-connection-settings-self-hosted.jpg)

3.  **「接続テスト」**をクリックして、TiDBセルフマネージドクラスタへの接続を検証してください。

    **「ドライバファイルのダウンロード」**ダイアログが表示されたら、 **「ダウンロード」**をクリックしてドライバファイルを入手してください。

    ![Download driver files](/media/develop/dbeaver-download-driver.jpg)

    接続テストが成功すると、以下のように**接続テスト**ダイアログが表示されます。 **「OK」**をクリックして閉じます。

    ![Connection test result](/media/develop/dbeaver-connection-test.jpg)

4.  接続設定を保存するには、 **「完了」**をクリックしてください。

</div>
</SimpleTab>

## 次のステップ {#next-steps}

-   DBeaver の使用法の詳細については[DBeaverのドキュメント](https://github.com/dbeaver/dbeaver/wiki)参照してください。
-   [開発者ガイド](https://docs.pingcap.com/developer/)[データを挿入する](/develop/dev-guide-insert-data.md)[データの更新](/develop/dev-guide-update-data.md)、[データを削除する](/develop/dev-guide-delete-data.md)、「SQL パフォーマンス最適化」などの章[単一表の読み取り](/develop/dev-guide-get-data-from-single-table.md)読んで、TiDB アプリケーション [取引](/develop/dev-guide-transaction-overview.md)[SQLパフォーマンス最適化](/develop/dev-guide-optimize-sql-overview.md)。
-   プロフェッショナルな[TiDB開発者向けコース](https://www.pingcap.com/education/)コースを通じて学習し、試験に合格すると[TiDB認定資格](https://www.pingcap.com/education/certification/)を取得します。

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)
