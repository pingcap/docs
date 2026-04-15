---
title: Import Data from Amazon S3 into TiDB Cloud Premium
summary: コンソールウィザードを使用して、Amazon S3からTiDB Cloud PremiumインスタンスにCSVファイルをインポートする方法を学びましょう。
---

# Amazon S3からTiDB Cloud Premiumにデータをインポートする {#import-data-from-amazon-s3-into-tidb-cloud-premium}

このドキュメントでは、Amazon Simple Storage Service (Amazon S3) からTiDB Cloud Premium インスタンスに CSV ファイルをインポートする方法について説明します。この手順は、現在のプライベートプレビュー版のユーザーインターフェースを反映したものであり、今後のパブリックプレビュー版のリリースに向けた初期フレームワークとして機能します。

> **警告：**
>
> TiDB Cloud Premiumは現在、一部のAWSリージョンで**プライベートプレビュー版**として提供されています。
>
> 組織で Premium がまだ有効になっていない場合、または別のクラウド プロバイダーまたは地域でアクセスする必要がある場合は、 [TiDB Cloudコンソール](https://tidbcloud.com/)の左下隅にある**[サポート]**をクリックするか、Web サイトの[お問い合わせ](https://www.pingcap.com/contact-us)フォームからリクエストを送信してください。

> **ヒント：**
>
> -   TiDB Cloud StarterまたはEssentialについては、 [TiDB Cloud StarterまたはEssentialにクラウドストレージからCSVファイルをインポートする](/tidb-cloud/import-csv-files-serverless.md)。
> -   TiDB Cloud Dedicatedについては、[クラウドストレージからTiDB Cloud DedicatedにCSVファイルをインポートする](/tidb-cloud/import-csv-files.md)参照してください。

## 制限事項 {#limitations}

-   データの一貫性を確保するため、 TiDB Cloud Premium では、CSV ファイルを空のテーブルにのみインポートできます。対象テーブルに既にデータが含まれている場合は、ステージングテーブルにインポートしてから、 `INSERT ... SELECT`ステートメントを使用して行をコピーしてください。
-   プライベートプレビュー期間中は、ユーザーインターフェースはstorageプロバイダーとしてAmazon S3のみをサポートしています。その他のプロバイダーへの対応は、今後のリリースで追加される予定です。
-   各インポートジョブは、単一のソースパターンを1つの宛先テーブルにマッピングします。

## ステップ1. CSVファイルを準備する {#step-1-prepare-the-csv-files}

1.  CSVファイルが256MiBを超える場合は、 TiDB Cloud Premiumが並列処理できるように、256MiB程度の小さなファイルに分割することを検討してください。
2.  CSVファイルの名前は、 Dumplingの命名規則に従ってください。
    -   完全な表ファイルの場合： `${db_name}.${table_name}.csv`形式を使用してください。
    -   シャーディングされたファイル: `${db_name}.${table_name}.000001.csv`のような数値サフィックスを追加します。
    -   圧縮ファイル: `${db_name}.${table_name}.${suffix}.csv.${compress}`形式を使用してください。
3.  オプションのスキーマファイル（ `${db_name}-schema-create.sql` 、 `${db_name}.${table_name}-schema.sql` ）を使用すると、 TiDB Cloud Premium はデータベースとテーブルを自動的に作成できます。

<!--Todo
These naming conventions are identical to the TiDB Cloud Serverless workflow. Update this section after we validate the Premium defaults.
-->

## ステップ2．ターゲットスキーマを作成する（オプション） {#step-2-create-target-schemas-optional}

TiDB Cloud Premiumでデータベースとテーブルを自動的に作成する場合は、 Dumplingで生成されたスキーマファイルを同じS3ディレクトリに配置してください。そうでない場合は、インポートを実行する前に、 TiDB Cloud Premiumでデータベースとテーブルを手動で作成してください。

## ステップ3. Amazon S3へのアクセスを設定する {#step-3-configure-access-to-amazon-s3}

TiDB Cloud Premiumがバケットを読み取れるようにするには、以下のいずれかの方法を使用してください。

-   TiDB Cloudを信頼し、関連するパスに対して`s3:GetObject`および`s3:ListBucket`権限を付与するAWSロールARNを指定します。
-   同等の権限を持つAWSアクセスキー（アクセスキーIDとシークレットアクセスキー）を提供してください。

ウィザードには**、「AWS CloudFormation を使用して新しいロールを作成するには、ここをクリックしてください」**というラベルの付いたヘルプリンクが含まれています。TiDB TiDB Cloud Premium で CloudFormation スタックを事前に設定してロールを作成する必要がある場合は、このリンクをクリックしてください。

## ステップ4. Amazon S3からCSVファイルをインポートする {#step-4-import-csv-files-from-amazon-s3}

1.  [TiDB Cloudコンソール](https://tidbcloud.com/tidbs)で、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、 TiDB Cloud Premiumインスタンスの名前をクリックします。

2.  左側のナビゲーションペインで、 **[データ]** &gt; **[インポート]**をクリックし、 **[クラウドストレージからデータをインポート]**を選択します。

3.  **ソース接続**ダイアログで：
    -   **ストレージプロバイダー**を**Amazon S3**に設定します。
    -   単一ファイル（ `s3://bucket/path/file.csv` ）またはフォルダ（ `s3://bucket/path/` ）の**ソースファイルURI**を入力します。
    -   **AWSロールARN**または**AWSアクセスキー**を選択し、認証情報を入力してください。
    -   接続を確認するには、 **「テストバケットアクセス」**をクリックしてください。&lt;!--Todo-- 既知のプレビューの問題: ボタンをクリックすると、成功のトーストが表示されずにアイドル状態に戻ります。--&gt;

4.  **「次へ」**をクリックし、インポートジョブに使用するTiDB SQLのユーザー名とパスワードを入力してください。必要に応じて、接続テストを実行してください。

5.  自動生成されたソースとターゲットのマッピングを確認してください。カスタムパターンと宛先テーブルを定義する必要がある場合は、自動マッピングを無効にしてください。

6.  **「次へ」**をクリックして事前チェックを実行してください。ファイルが見つからない、またはスキーマが互換性がないといった警告が表示された場合は、解決してください。

7.  **「インポート開始」**をクリックしてジョブグループを起動します。

8.  ジョブのステータスが**「完了」と**表示されるまで監視し、その後、 TiDB Cloudにインポートされたデータを確認します。

## トラブルシューティング {#troubleshooting}

-   事前チェックでファイルがゼロと報告された場合は、S3パスとIAM権限を確認してください。
-   ジョブが**「準備中」**のままになっている場合は、宛先テーブルが空であること、および必要なスキーマファイルが存在することを確認してください。
-   マッピングや認証情報を調整する必要がある場合は、**キャンセル**操作を使用してジョブグループを停止してください。

## 次のステップ {#next-steps}

-   スクリプトによるインポートについては[MySQLコマンドラインクライアントを使用してTiDB Cloud Premiumにデータをインポートする](/tidb-cloud/premium/import-with-mysql-cli-premium.md)参照してください。
-   IAM関連の問題については[Amazon S3からのデータインポート中に発生するアクセス拒否エラーのトラブルシューティング](/tidb-cloud/troubleshoot-import-access-denied-error.md)参照してください。
