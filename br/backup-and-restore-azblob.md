---
title: Back up and Restore Data on Azure Blob Storage
summary: Learn how to use BR to back up and restore data on Azure Blob Storage.
---

# AzureBlobStorageでのデータのバックアップと復元 {#back-up-and-restore-data-on-azure-blob-storage}

Backup＆Restore（BR）ツールは、データのバックアップと復元のための外部ストレージとしてAzureBlobStorageを使用することをサポートしています。

BRでサポートされているその他の外部ストレージの詳細については、 [外部ストレージ](/br/backup-and-restore-storages.md)を参照してください。

## ユーザーシナリオ {#user-scenario}

Azure仮想マシンは、大規模なデータをAzureBlobStorageにすばやく保存できます。 Azure仮想マシンを使用してクラスタをデプロイしている場合は、AzureBlobStorageにデータをバックアップできます。

## 使用法 {#usage}

BRを使用すると、次の2つの方法で、AzureBlobStorage上のデータをバックアップおよび復元できます。

-   Azure AD（Azure Active Directory）を使用してデータをバックアップおよび復元する
-   アクセスキーを使用してデータをバックアップおよび復元する

一般的に、コマンドラインで重要な情報（ `account-key`など）が公開されないようにするには、AzureADを使用することをお勧めします。

以下は、上記の2つの方法を使用したAzureBlobStorageでのバックアップと復元の操作の例です。操作の目的は次のとおりです。

-   バックアップ： `test`のデータベースを`container=test`のコンテナー内のスペースにバックアップし、AzureBlobStorageのパスプレフィックスとして`t1`を使用します。
-   復元：AzureBlobStorageのパスプレフィックスとして`t1`を使用する`container=test`コンテナー内のスペースから`test`データベースへのデータを復元します。

### 方法1：Azure ADを使用してバックアップと復元（推奨） {#method-1-back-up-and-restore-using-azure-ad-recommended}

BRおよびTiKVの動作環境では、環境変数`$AZURE_CLIENT_ID` 、および`$AZURE_TENANT_ID`を構成する必要があり`$AZURE_CLIENT_SECRET` 。これらの変数を構成すると、BRはAzureADを使用して`account-key`を構成せずにAzureBlobStorageにアクセスできます。この方法の方が安全であるため、お勧めします。 `$AZURE_CLIENT_ID` 、および`$AZURE_TENANT_ID`は、AzureアプリケーションのアプリケーションID `client_id` 、テナントID `tenant_id` 、およびクライアントパスワード`$AZURE_CLIENT_SECRET`を`client_secret`します。

`$AZURE_CLIENT_ID` 、および`$AZURE_TENANT_ID`が操作環境にあることを確認する方法、またはこれらの環境変数をパラメーターとして構成する場合は、 `$AZURE_CLIENT_SECRET`を参照して[環境変数をパラメーターとして構成する](#configure-environment-variables-as-parameters) 。

#### バックアップ {#back-up}

Azure ADを使用してデータをバックアップする場合は、 `account-name`と`access-tier`を指定する必要があります。 `access-tier`が設定されていない（値が空の）場合、値はデフォルトで`Hot`です。

> **ノート：**
>
> Azure Blob Storageを外部ストレージとして使用する場合は、 `send-credentials-to-tikv = true` （デフォルトで設定）を設定する必要があります。そうしないと、バックアップタスクが失敗します。

このセクションでは、データを`cool tier`にバックアップする方法を示します。つまり、アップロードされたオブジェクトのアクセス層は`Cool`です。 `account-name`と`access-tier`は、次の2つの方法で指定できます。

-   パラメータ情報をURLパラメータに書き込みます。

    ```
    tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1&access-tier=Cool'
    ```

-   コマンドラインパラメータにパラメータ情報を書き込みます。

    ```
    tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1 --azblob.access-tier=Cool
    ```

#### 戻す {#restore}

Azure ADを使用してデータを復元する場合は、 `account-name`を指定する必要があります。次の2つの方法で指定できます。

-   パラメータ情報をURLパラメータに書き込みます。

    ```
    tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1'
    ```

-   コマンドラインパラメータにパラメータ情報を書き込みます。

    ```
    tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1
    ```

### 方法2：アクセスキーを使用してバックアップおよび復元する（簡単） {#method-2-back-up-and-restore-using-an-access-key-easy}

#### バックアップ {#back-up}

アクセスキーを使用してデータをバックアップする場合は、 `account-name` 、および`account-key`を指定する必要があり`access-tier` 。 `access-tier`が設定されていない（値が空の）場合、値はデフォルトで`Hot`です。

> **ノート：**
>
> Azure Blob Storageを外部ストレージとして使用する場合は、 `send-credentials-to-tikv = true` （デフォルトで設定）を設定する必要があります。そうしないと、バックアップタスクが失敗します。

このセクションでは、データを`cool tier`にバックアップする方法を示します。つまり、アップロードされたオブジェクトのアクセス層は`Cool`です。 `account-name` 、および`account-key`は、次の2 `access-tier`の方法で指定できます。

-   パラメータ情報をURLパラメータに書き込みます。

    ```
    tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1&account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==&access-tier=Cool'
    ```

-   コマンドラインパラメータにパラメータ情報を書き込みます。

    ```
    tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1 --azblob.account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw== --azblob.access-tier=Cool
    ```

#### 戻す {#restore}

アクセスキーを使用してデータを復元する場合は、 `account-name`と`account-key`を指定する必要があります。パラメータは次の2つの方法で指定できます。

-   パラメータ情報をURLパラメータに書き込みます。

    ```
    tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1&account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw=='
    ```

-   コマンドラインパラメータにパラメータ情報を書き込みます。

    ```
    tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1 --azblob.account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==
    ```

## パラメータの説明 {#parameter-description}

バックアップと復元のプロセスでは、 `account-name` 、および`account-key`を使用する必要があり`access-tier` 。以下は、パラメーターの詳細な説明です。

-   [URLパラメータ](/br/backup-and-restore-storages.md#azblob-url-parameters)
-   [コマンドラインパラメータ](/br/backup-and-restore-storages.md#azblob-command-line-parameters)

### 環境変数をパラメーターとして構成する {#configure-environment-variables-as-parameters}

Azure ADを使用してデータをバックアップおよび復元する場合、環境変数`$AZURE_CLIENT_ID` 、および`$AZURE_TENANT_ID`は、BRおよびTiKVのオペレーティング環境で構成する必要があり`$AZURE_CLIENT_SECRET` 。

-   TiUPを使用してクラスタを開始すると、TiKVは「systemd」サービスを使用します。次の例は、上記の3つの環境変数をTiKVのパラメーターとして構成する方法を示しています。

    > **ノート：**
    >
    > 手順3でTiKVを再起動する必要があります。TiKVを再起動できない場合は、 [方法2](#method-2-back-up-and-restore-using-an-access-key-easy)を使用してデータをバックアップおよび復元できます。

    1.  このノードのTiKVポートが`24000`であると仮定します。つまり、「systemd」サービスの名前は「tikv-24000」です。

        ```
        systemctl edit tikv-24000
        ```

    2.  環境変数情報を入力します。

        ```
        [Service]
        Environment="AZURE_CLIENT_ID=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
        Environment="AZURE_TENANT_ID=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
        Environment="AZURE_CLIENT_SECRET=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        ```

    3.  構成を再ロードし、TiKVを再起動します。

        ```
        systemctl daemon-reload
        systemctl restart tikv-24000
        ```

-   コマンドラインで開始したTiKVおよびBRの場合、それらのAzure AD情報を構成するには、環境変数`$AZURE_CLIENT_ID` 、および`$AZURE_TENANT_ID`が操作環境で構成されているかどうかを確認するだけで済み`$AZURE_CLIENT_SECRET` 。次のコマンドを実行して、変数がBRおよびTiKVの動作環境にあるかどうかを確認できます。

    ```shell
    echo $AZURE_CLIENT_ID
    echo $AZURE_TENANT_ID
    echo $AZURE_CLIENT_SECRET
    ```

## 互換性 {#compatibility}

この機能は、v5.4.0以降のバージョンとの**み互換性**があります。
