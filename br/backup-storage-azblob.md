---
title: Back up and Restore Data on Azure Blob Storage Using BR
summary: Learn how to use BR to back up and restore data on Azure Blob Storage.
aliases: ['/tidb/v6.1/backup-and-restore-azblob/']
---

# BRを使用してAzureBlobStorageのデータをバックアップおよび復元する {#back-up-and-restore-data-on-azure-blob-storage-using-br}

Backup＆Restore（BR）ツールは、データのバックアップと復元のための外部ストレージとしてAzureBlobStorageを使用することをサポートしています。

## ユーザーシナリオ {#user-scenario}

Azure仮想マシンは、大規模なデータをAzureBlobStorageにすばやく保存できます。 Azure仮想マシンを使用してクラスタをデプロイしている場合は、AzureBlobStorageにデータをバックアップできます。

## 使用法 {#usage}

BRを使用すると、次の2つの方法で、AzureBlobStorage上のデータをバックアップおよび復元できます。

-   Azure AD（Azure Active Directory）を使用してデータをバックアップおよび復元する
-   アクセスキーを使用してデータをバックアップおよび復元する

一般的に、コマンドラインで重要な情報（ `account-key`など）が公開されないようにするには、AzureADを使用することをお勧めします。

以下は、前述の2つの方法を使用したAzureBlobStorageでのバックアップと復元の操作の例です。操作の目的は次のとおりです。

-   バックアップ： `test`のデータベースを`container=test`のコンテナー内のスペースにバックアップし、AzureBlobStorageのパスプレフィックスとして`t1`を使用します。
-   復元：AzureBlobStorageのパスプレフィックスとして`t1`を使用する`container=test`コンテナー内のスペースから`test`データベースへのデータを復元します。

> **ノート：**
>
> AzureADまたはアクセスキーを使用してAzureBlobStorageにデータをバックアップする場合は、 `send-credentials-to-tikv = true` （デフォルトでは`true` ）を設定する必要があります。そうしないと、バックアップタスクが失敗します。

### 方法1：Azure ADを使用してデータをバックアップおよび復元する（推奨） {#method-1-back-up-and-restore-data-using-azure-ad-recommended}

このセクションでは、AzureADを使用してデータをバックアップおよび復元する方法について説明します。バックアップまたは復元を実行する前に、環境変数を構成する必要があります。

#### 環境変数を構成する {#configure-environment-variables}

BRおよびTiKVの動作環境で、環境変数`$AZURE_CLIENT_ID` 、および`$AZURE_TENANT_ID`を構成し`$AZURE_CLIENT_SECRET` 。

-   TiUPを使用してクラスタを開始すると、TiKVは「systemd」サービスを使用します。次の例では、前述の3つの環境変数をTiKVのパラメーターとして構成する方法を紹介します。

    > **ノート：**
    >
    > 手順3でTiKVを再起動する必要があります。TiKVを再起動できない場合は、 [方法2](#method-2-back-up-and-restore-using-an-access-key-easy)を使用してデータをバックアップおよび復元します。

    1.  このノードのTiKVポートが24000であると仮定します。つまり、「systemd」サービスの名前は「tikv-24000」です。

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

-   コマンドラインで開始するTiKVおよびBRの`$AZURE_CLIENT_SECRET` `$AZURE_CLIENT_ID` `$AZURE_TENANT_ID`環境で構成されているかどうかを確認するだけです。

    ```
    echo $AZURE_CLIENT_ID
    echo $AZURE_TENANT_ID
    echo $AZURE_CLIENT_SECRET
    ```

環境変数の詳細については、 [AzblobURLパラメーター](/br/backup-and-restore-storages.md#azblob-url-parameters)を参照してください。

#### バックアップ {#back-up}

このセクションでは、データを`cool tier`にバックアップする方法を示します。つまり、アップロードされたオブジェクトのアクセス層は`Cool`です。 `account-name`と`access-tier`は2つの方法で指定できます。バックアップ操作は、選択した方法によって異なります。

-   URLのパラメーターとして`account-name`と`access-tier`を指定します。

    ```
    tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1&access-tier=Cool'
    ```

    `access-tier`が設定されていない場合（値が空の場合）、デフォルトで値は`Hot`です。

-   コマンドラインパラメータとして`account-name`と`access-tier`を指定します。

    ```
    tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1 --azblob.access-tier=Cool
    ```

#### 戻す {#restore}

[バックアップ](#back-up)で`account-name`を指定する方法と同様に、URLまたはコマンドラインパラメータを使用してデータを復元できます。

-   URLのパラメータとして`account-name`を指定します。

    ```
    tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1'
    ```

-   コマンドラインパラメータとして`account-name`を指定します。

    ```
    tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1
    ```

### 方法2：アクセスキーを使用してバックアップおよび復元する（簡単） {#method-2-back-up-and-restore-using-an-access-key-easy}

Azure ADを使用したデータのバックアップと復元と比較すると、環境変数を構成する必要がないため、アクセスキーを使用したバックアップと復元が簡単です。その他の手順は、AzureADを使用する手順と同様です。

#### バックアップ {#back-up}

-   URLのパラメーターとして`account-name` 、および`account-key`を指定し`access-tier` 。

    ```
    tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1&account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==&access-tier=Cool'
    ```

-   コマンドラインパラメータとして`account-name` 、および`account-key`を指定し`access-tier` 。

    ```
    tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1 --azblob.account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw== --azblob.access-tier=Cool
    ```

#### 戻す {#restore}

-   URLのパラメーターとして`account-name`と`account-key`を指定します。

    ```
    tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1&account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw=='
    ```

-   コマンドラインパラメータとして`account-name`と`account-key`を指定します。

    ```
    tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1 --azblob.account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==
    ```

## 互換性 {#compatibility}

この機能は、v5.4.0以降のバージョンとの**み互換性**があります。

## も参照してください {#see-also}

-   BRでサポートされている他の外部ストレージについては、 [外部ストレージ](/br/backup-and-restore-storages.md)を参照してください。
-   パラメータの詳細については、次のドキュメントを参照してください。

    -   [AzblobURLパラメーター](/br/backup-and-restore-storages.md#azblob-url-parameters)
    -   [Azblobコマンドラインパラメーター](/br/backup-and-restore-storages.md#azblob-command-line-parameters)
