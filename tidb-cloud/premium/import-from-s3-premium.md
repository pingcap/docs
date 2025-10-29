---
title: Import Data from Amazon S3 into TiDB Cloud Premium
summary: コンソール ウィザードを使用して、Amazon S3 からTiDB Cloud Premium インスタンスに CSV ファイルをインポートする方法を学習します。
---

# Amazon S3 からTiDB Cloud Premium にデータをインポートする {#import-data-from-amazon-s3-into-tidb-cloud-premium}

このドキュメントでは、Amazon Simple Storage Service (Amazon S3) からTiDB Cloud Premium インスタンスに CSV ファイルをインポートする方法について説明します。手順は現在のプライベートプレビューのユーザーインターフェースを反映しており、今後のパブリックプレビュー開始に向けた初期フレームワークとして役立ちます。

> **警告：**
>
> TiDB Cloud Premium は現在、一部の AWS リージョンで**プライベートプレビュー**としてご利用いただけます。
>
> 組織で Premium がまだ有効になっていない場合、または別のクラウド プロバイダーやリージョンでアクセスする必要がある場合は、 [TiDB Cloudコンソール](https://tidbcloud.com/)の左下隅にある**[サポート]**をクリックするか、Web サイトの[お問い合わせ](https://www.pingcap.com/contact-us)フォームからリクエストを送信してください。

> **ヒント：**
>
> -   TiDB Cloud Starter または Essential については、 [クラウドストレージからTiDB Cloud StarterまたはEssentialにCSVファイルをインポートする](/tidb-cloud/import-csv-files-serverless.md)参照してください。
> -   TiDB Cloud Dedicated については、 [クラウドストレージからTiDB Cloud DedicatedにCSVファイルをインポートする](/tidb-cloud/import-csv-files.md)参照してください。

## 制限事項 {#limitations}

-   データの一貫性を確保するため、 TiDB Cloud PremiumではCSVファイルのインポートは空のテーブルのみに制限されています。インポート先のテーブルに既にデータが含まれている場合は、ステージングテーブルにインポートし、 `INSERT ... SELECT`ステートメントを使用して行をコピーしてください。
-   プライベートプレビュー期間中、ユーザーインターフェースは現在Amazon S3のみをstorageプロバイダーとしてサポートしています。今後のリリースでは、他のプロバイダーのサポートも追加される予定です。
-   各インポート ジョブは、1 つのソース パターンを 1 つの宛先テーブルにマッピングします。

## ステップ1.CSVファイルを準備する {#step-1-prepare-the-csv-files}

1.  CSV ファイルが 256 MiB より大きい場合は、 TiDB Cloud Premium が並列処理できるように、256 MiB 程度の小さなファイルに分割することを検討してください。
2.  Dumpling の命名規則に従って CSV ファイルに名前を付けます。
    -   完全なテーブルファイル: `${db_name}.${table_name}.csv`形式を使用します。
    -   分割されたファイル: `${db_name}.${table_name}.000001.csv`などの数値サフィックスを追加します。
    -   圧縮ファイル: `${db_name}.${table_name}.${suffix}.csv.${compress}`形式を使用します。
3.  オプションのスキーマ ファイル ( `${db_name}-schema-create.sql` ) は`${db_name}.${table_name}-schema.sql` TiDB Cloud Premium がデータベースとテーブルを自動的に作成するのに役立ちます。

<!--Todo
These naming conventions are identical to the TiDB Cloud Serverless workflow. Update this section after we validate the Premium defaults.
-->

## ステップ 2. ターゲット スキーマを作成する (オプション) {#step-2-create-target-schemas-optional}

TiDB Cloud Premium でデータベースとテーブルを自動作成したい場合は、 Dumplingによって生成されたスキーマファイルを同じ S3 ディレクトリに配置してください。そうでない場合は、インポートを実行する前にTiDB Cloud Premium でデータベースとテーブルを手動で作成してください。

## ステップ3. Amazon S3へのアクセスを構成する {#step-3-configure-access-to-amazon-s3}

TiDB Cloud Premium がバケットを読み取れるようにするには、次のいずれかの方法を使用します。

-   TiDB Cloud を信頼し、関連するパスに対する`s3:GetObject`および`s3:ListBucket`権限を付与する AWS ロール ARN を提供します。
-   同等の権限を持つ AWS アクセスキー (アクセスキー ID とシークレットアクセスキー) を提供します。

ウィザードには、 **「AWS CloudFormation で新規作成するには、こちらをクリックしてください」**というヘルパーリンクが含まれています。ロールを作成する CloudFormation スタックをTiDB Cloud Premium で事前に設定する必要がある場合は、このリンクをクリックしてください。

## ステップ4. Amazon S3からCSVファイルをインポートする {#step-4-import-csv-files-from-amazon-s3}

1.  [TiDB Cloudコンソール](https://tidbcloud.com/tidbs)で[**TiDBインスタンス**](https://tidbcloud.com/tidbs)ページに移動し、TiDB インスタンスの名前をクリックします。
2.  左側のナビゲーション ペインで、 **[データ]** &gt; **[インポート]**をクリックし、 **[Cloud Storage からデータをインポート]**を選択します。
3.  **ソース接続**ダイアログで次の操作を行います。
    -   **ストレージプロバイダーを****Amazon S3**に設定します。
    -   単一ファイル（ `s3://bucket/path/file.csv` ）またはフォルダ（ `s3://bucket/path/` ）の**ソースファイルURI**を入力します。
    -   **AWS ロール ARN**または**AWS アクセスキー**を選択し、認証情報を入力します。
    -   接続を検証するには、 **「バケット アクセスのテスト」**をクリックします。
        <!--Todo-- Known preview issue: the button returns to the idle state without a success toast.-->
4.  **「次へ」**をクリックし、インポートジョブで使用するTiDB SQLのユーザー名とパスワードを入力します。必要に応じて接続をテストしてください。
5.  自動生成されたソースからターゲットへのマッピングを確認します。カスタムパターンとターゲットテーブルを定義する必要がある場合は、自動マッピングを無効にしてください。
6.  **「次へ」**をクリックして事前チェックを実行します。不足しているファイルや互換性のないスキーマに関する警告があれば解決してください。
7.  **[インポートの開始]**をクリックしてジョブ グループを起動します。
8.  ジョブのステータスが**「完了」**と表示されるまで監視し、 TiDB Cloudにインポートされたデータを確認します。

## トラブルシューティング {#troubleshooting}

-   事前チェックでファイルがゼロであると報告された場合は、S3 パスとIAM権限を確認してください。
-   ジョブが**「準備中」**のままの場合は、宛先テーブルが空であり、必要なスキーマ ファイルが存在することを確認してください。
-   マッピングまたは資格情報を調整する必要がある場合は、 **[キャンセル]**アクションを使用してジョブ グループを停止します。

## 次のステップ {#next-steps}

-   スクリプトによるインポートについては[MySQL コマンドラインクライアントを使用してTiDB Cloud Premium にデータをインポートする](/tidb-cloud/premium/import-with-mysql-cli-premium.md)参照してください。
-   IAM関連の問題については[Amazon S3 からのデータインポート中に発生するアクセス拒否エラーのトラブルシューティング](/tidb-cloud/troubleshoot-import-access-denied-error.md)参照してください。
