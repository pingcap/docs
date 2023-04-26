---
title: Migrate from On-Premises TiDB to TiDB Cloud
summary: Learn how to migrate data from on-premises TiDB to TiDB Cloud.
---

# オンプレミス TiDB からTiDB Cloudへの移行 {#migrate-from-on-premises-tidb-to-tidb-cloud}

このドキュメントでは、Dumplingと TiCDC を使用してオンプレミス (OP) TiDB クラスターからTiDB Cloud(AWS) にデータを移行する方法について説明します。

全体的な手順は次のとおりです。

1.  環境を構築し、ツールを準備します。
2.  完全なデータを移行します。プロセスは次のとおりです。
    1.  Dumplingを使用して OP TiDB から Amazon S3 にデータをエクスポートします。
    2.  Amazon S3 からTiDB Cloudにデータをインポートします。
3.  TiCDC を使用して増分データをレプリケートします。
4.  移行されたデータを確認します。

## 前提条件 {#prerequisites}

S3 バケットとTiDB Cloudクラスターを同じリージョンに配置することをお勧めします。リージョン間の移行では、データ変換のために追加のコストが発生する場合があります。

移行の前に、次のものを準備する必要があります。

-   管理者アクセス権を持つ[AWS アカウント](https://docs.aws.amazon.com/AmazonS3/latest/userguide/setting-up-s3.html#sign-up-for-aws-gsg)
-   [AWS S3 バケット](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html)
-   [管理者アクセス権を持つTiDB CloudアカウントとTiDB Cloud (AWS) クラスター](/tidb-cloud/tidb-cloud-quickstart.md)

## ツールを準備する {#prepare-tools}

次のツールを準備する必要があります。

-   Dumpling: データ エクスポート ツール
-   TiCDC: データ複製ツール

### Dumpling {#dumpling}

[Dumpling](https://docs.pingcap.com/tidb/dev/dumpling-overview)は、TiDB または MySQL から SQL または CSV ファイルにデータをエクスポートするツールです。 Dumpling を使用して、OP TiDB から完全なデータをエクスポートできます。

Dumplingをデプロイする前に、次の点に注意してください。

-   TiDB Cloudの TiDB クラスターと同じ VPC 内の新しい EC2 インスタンスにDumplingをデプロイすることをお勧めします。
-   推奨される EC2 インスタンス タイプは**c6g.4xlarge** (16 vCPU および 32 GiBメモリ) です。必要に応じて、他の EC2 インスタンス タイプを選択できます。 Amazon マシン イメージ (AMI) には、Amazon Linux、Ubuntu、または Red Hat を使用できます。

Dumpling は、 TiUPまたはインストール パッケージを使用して展開できます。

#### TiUPを使用してDumplingをデプロイ {#deploy-dumpling-using-tiup}

[TiUP](https://docs.pingcap.com/tidb/stable/tiup-overview)を使用してDumplingをデプロイします。

```bash
## Deploy TiUP
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
source /root/.bash_profile
## Deploy Dumpling and update to the latest version
tiup install dumpling
tiup update --self && tiup update dumpling
```

#### インストール パッケージを使用してDumplingをデプロイ {#deploy-dumpling-using-the-installation-package}

インストール パッケージを使用してDumplingをデプロイするには:

1.  [ツールキット パッケージ](https://docs.pingcap.com/tidb/stable/download-ecosystem-tools)をダウンロードします。

2.  ターゲット マシンに抽出します。 `tiup install dumpling`を実行すると、 TiUPを使用してDumpling を取得できます。その後、 `tiup dumpling ...`使用してDumplingを実行できます。詳細については、 [Dumpling紹介](https://docs.pingcap.com/tidb/stable/dumpling-overview#dumpling-introduction)を参照してください。

#### Dumplingの権限を構成する {#configure-privileges-for-dumpling}

アップストリーム データベースからデータをエクスポートするには、次の権限が必要です。

-   選択する
-   リロード
-   ロックテーブル
-   複製クライアント
-   プロセス

### TiCDCをデプロイ {#deploy-ticdc}

アップストリームの TiDB クラスターからTiDB Cloudに増分データをレプリケートするには、 [TiCDC をデプロイする](https://docs.pingcap.com/tidb/dev/deploy-ticdc)が必要です。

1.  現在の TiDB バージョンが TiCDC をサポートしているかどうかを確認します。 TiDB v4.0.8.rc.1 以降のバージョンは TiCDC をサポートしています。 TiDB クラスターで`select tidb_version();`を実行すると、TiDB のバージョンを確認できます。アップグレードする必要がある場合は、 [TiUPを使用して TiDB をアップグレードする](https://docs.pingcap.com/tidb/dev/deploy-ticdc#upgrade-ticdc-using-tiup)を参照してください。

2.  TiCDCコンポーネントをTiDB クラスターに追加します。 [TiUPを使用して TiCDC を既存の TiDB クラスターに追加またはスケールアウトする](https://docs.pingcap.com/tidb/dev/deploy-ticdc#add-or-scale-out-ticdc-to-an-existing-tidb-cluster-using-tiup)を参照してください。 `scale-out.yml`ファイルを編集して TiCDC を追加します。

    ```yaml
    cdc_servers:
    - host: 10.0.1.3
      gc-ttl: 86400
      data_dir: /tidb-data/cdc-8300
    - host: 10.0.1.4
      gc-ttl: 86400
      data_dir: /tidb-data/cdc-8300
    ```

3.  TiCDCコンポーネントを追加し、ステータスを確認します。

    ```shell
    tiup cluster scale-out <cluster-name> scale-out.yml
    tiup cluster display <cluster-name>
    ```

## 完全なデータを移行する {#migrate-full-data}

OP TiDB クラスターからTiDB Cloudにデータを移行するには、次のように完全なデータ移行を実行します。

1.  OP TiDB クラスターから Amazon S3 にデータを移行します。
2.  Amazon S3 からTiDB Cloudにデータを移行します。

### OP TiDB クラスターから Amazon S3 にデータを移行する {#migrate-data-from-the-op-tidb-cluster-to-amazon-s3}

Dumplingを使用して、OP TiDB クラスターから Amazon S3 にデータを移行する必要があります。

TiDB クラスターがローカル IDC にある場合、またはDumplingサーバーと Amazon S3 の間のネットワークが接続されていない場合は、最初にファイルをローカルstorageにエクスポートしてから、後で Amazon S3 にアップロードできます。

#### ステップ 1. アップストリーム OP TiDB クラスターの GC メカニズムを一時的に無効にする {#step-1-disable-the-gc-mechanism-of-the-upstream-op-tidb-cluster-temporarily}

増分移行中に新しく書き込まれたデータが失われないようにするには、移行を開始する前にアップストリーム クラスターのガベージコレクション(GC) メカニズムを無効にして、システムが履歴データをクリーンアップしないようにする必要があります。

次のコマンドを実行して、設定が成功したかどうかを確認します。

```sql
SET GLOBAL tidb_gc_enable = FALSE;
```

以下は出力例で、 `0`無効であることを示します。

```sql
SELECT @@global.tidb_gc_enable;
+-------------------------+
| @@global.tidb_gc_enable |
+-------------------------+
|                       0 |
+-------------------------+
1 row in set (0.01 sec)
```

#### ステップ 2. Dumplingの Amazon S3 バケットへのアクセス許可を設定する {#step-2-configure-access-permissions-to-the-amazon-s3-bucket-for-dumpling}

AWS コンソールでアクセス キーを作成します。詳細は[アクセスキーを作成する](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)を参照してください。

1.  AWS アカウント ID またはアカウント エイリアス、 IAMユーザー名、およびパスワードを使用して[IAMコンソール](https://console.aws.amazon.com/iam/home#/security_credentials)にサインインします。

2.  右上のナビゲーション バーでユーザー名を選択し、 **[Security資格情報]**をクリックします。

3.  アクセス キーを作成するには、 **[アクセス キーの作成]**をクリックします。次に、 <strong>[.csv ファイルのダウンロード]</strong>を選択して、アクセス キー ID とシークレット アクセス キーをコンピューター上の CSV ファイルに保存します。ファイルを安全な場所に保管します。このダイアログ ボックスを閉じると、シークレット アクセス キーにアクセスできなくなります。 CSV ファイルをダウンロードしたら、 <strong>[Close]</strong>を選択します。アクセス キーを作成すると、キー ペアはデフォルトでアクティブになり、すぐに使用できます。

    ![Create access key](/media/tidb-cloud/op-to-cloud-create-access-key01.png)

    ![Download CSV file](/media/tidb-cloud/op-to-cloud-create-access-key02.png)

#### ステップ 3. Dumplingを使用してアップストリームの TiDB クラスターから Amazon S3 にデータをエクスポートする {#step-3-export-data-from-the-upstream-tidb-cluster-to-amazon-s3-using-dumpling}

Dumplingを使用して上流の TiDB クラスターから Amazon S3 にデータをエクスポートするには、次の手順を実行します。

1.  Dumplingの環境変数を構成します。

    ```shell
    export AWS_ACCESS_KEY_ID=${AccessKey}
    export AWS_SECRET_ACCESS_KEY=${SecretKey}
    ```

2.  AWS コンソールから S3 バケット URI とリージョン情報を取得します。詳細は[バケットを作成する](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html)を参照してください。

    次のスクリーンショットは、S3 バケットの URI 情報を取得する方法を示しています。

    ![Get the S3 URI](/media/tidb-cloud/op-to-cloud-copy-s3-uri.png)

    次のスクリーンショットは、地域情報を取得する方法を示しています。

    ![Get the region information](/media/tidb-cloud/op-to-cloud-copy-region-info.png)

3.  Dumplingを実行して、データを Amazon S3 バケットにエクスポートします。

    ```ymal
    dumpling \
    -u root \
    -P 4000 \
    -h 127.0.0.1 \
    -r 20000 \
    --filetype {sql|csv}  \
    -F 256MiB  \
    -t 8 \
    -o "${S3 URI}" \
    --s3.region "${s3.region}"
    ```

    `-t`オプションは、エクスポートのスレッド数を指定します。スレッドの数を増やすと、Dumplingの同時実行性とエクスポート速度が向上しますが、データベースのメモリ消費も増加します。したがって、このパラメーターにはあまり大きな数値を設定しないでください。

    詳細については、 [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview#export-to-sql-files)を参照してください。

4.  エクスポートデータを確認してください。通常、エクスポートされたデータには次のものが含まれます。

    -   `metadata` : このファイルには、エクスポートの開始時刻とマスター バイナリ ログの場所が含まれます。
    -   `{schema}-schema-create.sql` : スキーマを作成するための SQL ファイル
    -   `{schema}.{table}-schema.sql` : テーブルを作成するための SQL ファイル
    -   `{schema}.{table}.{0001}.{sql|csv}` : データファイル
    -   `*-schema-view.sql` 、 `*-schema-trigger.sql` 、 `*-schema-post.sql` : その他のエクスポートされた SQL ファイル

### Amazon S3 からTiDB Cloudにデータを移行する {#migrate-data-from-amazon-s3-to-tidb-cloud}

OP TiDB クラスターから Amazon S3 にデータをエクスポートした後、データをTiDB Cloudに移行する必要があります。

1.  TiDB Cloudコンソールでクラスターのアカウント ID と外部 ID を取得します。詳細については、 [ステップ 2.Amazon S3 アクセスを構成する](/tidb-cloud/tidb-cloud-auditing.md#step-2-configure-amazon-s3-access)を参照してください。

    次のスクリーンショットは、アカウント ID と外部 ID を取得する方法を示しています。

    ![Get the Account ID and External ID](/media/tidb-cloud/op-to-cloud-get-role-arn.png)

2.  Amazon S3 のアクセス許可を構成します。通常、次の読み取り専用権限が必要です。

    -   s3:GetObject
    -   s3:GetObjectVersion
    -   s3:リストバケット
    -   s3:GetBucketLocation

    S3 バケットがサーバー側の暗号化 SSE-KMS を使用している場合は、KMS アクセス許可も追加する必要があります。

    -   kms:復号化

3.  アクセス ポリシーを構成します。 [AWS コンソール &gt; IAM &gt; アクセス管理 &gt; ポリシー](https://console.aws.amazon.com/iamv2/home#/policies)に移動し、リージョンに切り替えて、 TiDB Cloudのアクセス ポリシーが既に存在するかどうかを確認します。存在しない場合は、このドキュメントに従ってポリシーを作成します[JSON タブでのポリシーの作成](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create-console.html) 。

    以下は、json ポリシーのテンプレートの例です。

    ```json
    ## Create a json policy template
    ##<Your customized directory>: fill in the path to the folder in the S3 bucket where the data files to be imported are located.
    ##<Your S3 bucket ARN>: fill in the ARN of the S3 bucket. You can click the Copy ARN button on the S3 Bucket Overview page to get it.
    ##<Your AWS KMS ARN>: fill in the ARN for the S3 bucket KMS key. You can get it from S3 bucket > Properties > Default encryption > AWS KMS Key ARN. For more information, see https://docs.aws.amazon.com/AmazonS3/latest/userguide/viewing-bucket-key-settings.html

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:GetObjectVersion"
                ],
                "Resource": "arn:aws:s3:::<Your customized directory>"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:ListBucket",
                    "s3:GetBucketLocation"
                ],
                "Resource": "<Your S3 bucket ARN>"
            }
            // If you have enabled SSE-KMS for the S3 bucket, you need to add the following permissions.
            {
                "Effect": "Allow",
                "Action": [
                    "kms:Decrypt"
                ],
                "Resource": "<Your AWS KMS ARN>"
            }
            ,
            {
                "Effect": "Allow",
                "Action": "kms:Decrypt",
                "Resource": "<Your AWS KMS ARN>"
            }
        ]
    }
    ```

4.  役割を構成します。 [IAMロールの作成 (コンソール)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user.html)を参照してください。 [アカウント ID] フィールドに、ステップ 1 でメモしたTiDB Cloudアカウント ID とTiDB Cloud外部 ID を入力します。

5.  Role-ARN を取得します。 [AWS コンソール &gt; IAM &gt; アクセス管理 &gt; ロール](https://console.aws.amazon.com/iamv2/home#/roles)に進みます。お住まいの地域に切り替えます。作成したロールをクリックし、ARN を書き留めます。データをTiDB Cloudにインポートするときに使用します。

6.  データをTiDB Cloudにインポートします。 [ステップ 3. データをTiDB Cloudにインポートする](/tidb-cloud/migrate-from-amazon-s3-or-gcs.md#step-3-import-data-into-tidb-cloud)を参照してください。

## 増分データをレプリケートする {#replicate-incremental-data}

増分データをレプリケートするには、次の手順を実行します。

1.  増分データ移行の開始時刻を取得します。たとえば、完全なデータ移行のメタデータ ファイルから取得できます。

    ![Start Time in Metadata](/media/tidb-cloud/start_ts_in_metadata.png)

2.  TiCDC にTiDB Cloudへの接続を許可します。 [TiDB Cloudコンソール](https://tidbcloud.com/console/clusters)でクラスターを見つけ、 **[概要**] &gt; <strong>[接続]</strong> &gt; <strong>[標準接続]</strong> &gt; <strong>[トラフィック フィルターの作成]</strong>に移動します。 <strong>[編集]</strong> &gt; <strong>[項目の追加]</strong>をクリックします。 <strong>[IP アドレス]</strong>フィールドに TiCDCコンポーネントのパブリック IP アドレスを入力し、 <strong>[フィルターの更新]</strong>をクリックして保存します。これで、TiCDC はTiDB Cloudにアクセスできるようになりました。

    ![Update Filter](/media/tidb-cloud/edit_traffic_filter_rules.png)

3.  下流のTiDB Cloudクラスターの接続情報を取得します。 [TiDB Cloudコンソール](https://tidbcloud.com/console/clusters)で、 **[Overview]** &gt; <strong>[Connect]</strong> &gt; <strong>[Standard Connection]</strong> &gt; <strong>[Connect with a SQL Client]</strong>に移動します。接続情報から、クラスターのホスト IP アドレスとポートを取得できます。詳細については、 [標準接続で接続](/tidb-cloud/connect-via-standard-connection.md)を参照してください。

4.  増分レプリケーション タスクを作成して実行します。アップストリーム クラスターで、次を実行します。

    ```shell
    tiup cdc cli changefeed create \
    --pd=http://172.16.6.122:2379  \
    --sink-uri="tidb://root:123456@172.16.6.125:4000"  \
    --changefeed-id="upstream-to-downstream"  \
    --start-ts="431434047157698561"
    ```

    -   `--pd` : アップストリーム クラスタの PD アドレス。形式は`[upstream_pd_ip]:[pd_port]`のとおりです。2

    -   `--sink-uri` : レプリケーション タスクのダウンストリーム アドレス。 `--sink-uri`次の形式に従って構成します。現在、スキームは`mysql` 、 `tidb` 、 `kafka` 、 `s3` 、および`local`をサポートしています。

        ```shell
        [scheme]://[userinfo@][host]:[port][/path]?[query_parameters]
        ```

    -   `--changefeed-id` : レプリケーション タスクの ID。形式は ^[a-zA-Z0-9]+(-[a-zA-Z0-9]+)*$ 正規表現と一致する必要があります。この ID が指定されていない場合、TiCDC は ID として UUID (バージョン 4 形式) を自動的に生成します。

    -   `--start-ts` : 変更フィードの開始 TSO を指定します。この TSO から、TiCDC クラスターはデータのプルを開始します。デフォルト値は現在の時刻です。

    詳細については、 [TiCDC Changefeeds の CLI およびコンフィグレーションパラメーター](https://docs.pingcap.com/tidb/dev/ticdc-changefeed-config)を参照してください。

5.  アップストリーム クラスタで GC メカニズムを再度有効にします。増分レプリケーションでエラーや遅延が見つからない場合は、GC メカニズムを有効にしてクラスターのガベージコレクションを再開します。

    次のコマンドを実行して、設定が機能するかどうかを確認します。

    ```sql
    SET GLOBAL tidb_gc_enable = TRUE;
    ```

    以下は出力例で、 `1`は GC が無効であることを示します。

    ```sql
    SELECT @@global.tidb_gc_enable;
    +-------------------------+
    | @@global.tidb_gc_enable |
    +-------------------------+
    |                       1 |
    +-------------------------+
    1 row in set (0.01 sec)
    ```

6.  増分レプリケーション タスクを確認します。

    -   「変更フィードの作成に成功しました!」というメッセージが表示された場合が出力に表示されたら、レプリケーション タスクは正常に作成されています。

    -   状態が`normal`の場合、レプリケーション タスクは正常です。

        ```shell
         tiup cdc cli changefeed list --pd=http://172.16.6.122:2379
        ```

        ![Update Filter](/media/tidb-cloud/normal_status_in_replication_task.png)

    -   複製を確認します。上流のクラスターに新しいレコードを書き込み、そのレコードが下流のTiDB Cloudクラスターに複製されているかどうかを確認します。
