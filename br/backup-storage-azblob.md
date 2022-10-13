---
title: Back up and Restore Data on Azure Blob Storage Using BR
summary: Learn how to use BR to back up and restore data on Azure Blob Storage.
---

# BR を使用して Azure Blob Storage のデータをバックアップおよび復元する {#back-up-and-restore-data-on-azure-blob-storage-using-br}

バックアップと復元 (BR) ツールは、データのバックアップと復元のための外部ストレージとして Azure Blob Storage の使用をサポートしています。

## ユーザーシナリオ {#user-scenario}

Azure 仮想マシンは、大規模なデータを Azure Blob Storage にすばやく格納できます。 Azure 仮想マシンを使用してクラスターをデプロイしている場合は、Azure Blob Storage にデータをバックアップできます。

## 使用法 {#usage}

BR を使用すると、次の 2 つの方法で Azure Blob Storage のデータをバックアップおよび復元できます。

-   Azure AD (Azure Active Directory) を使用してデータをバックアップおよび復元する
-   アクセス キーを使用してデータをバックアップおよび復元する

一般的なケースでは、コマンド ラインでキー情報 ( `account-key`など) を公開しないようにするために、Azure AD を使用することをお勧めします。

上記の 2 つの方法を使用した Azure Blob Storage でのバックアップおよび復元操作の例を次に示します。操作の目的は次のとおりです。

-   バックアップ: Azure Blob Storage のパス プレフィックスとして`t1`を使用して、 `test`データベースを`container=test`コンテナー内のスペースにバックアップします。
-   復元: Azure Blob Storage のパス プレフィックスとして`t1`を使用して、 `container=test`コンテナー内のスペースから`test`データベースにデータを復元します。

> **ノート：**
>
> Azure AD またはアクセス キーを使用して Azure Blob Storage にデータをバックアップする場合は、 `send-credentials-to-tikv = true` (既定では`true` ) を設定する必要があります。そうしないと、バックアップ タスクが失敗します。

### 方法 1: Azure AD を使用してデータをバックアップおよび復元する (推奨) {#method-1-back-up-and-restore-data-using-azure-ad-recommended}

このセクションでは、Azure AD を使用してデータをバックアップおよび復元する方法について説明します。バックアップまたは復元を実行する前に、環境変数を構成する必要があります。

#### 環境変数の構成 {#configure-environment-variables}

BR と TiKV の動作環境で、環境変数`$AZURE_CLIENT_ID` 、 `$AZURE_TENANT_ID` 、および`$AZURE_CLIENT_SECRET`を設定します。

-   TiUP を使用してクラスターを起動すると、TiKV は「systemd」サービスを使用します。次の例では、前述の 3 つの環境変数を TiKV のパラメーターとして構成する方法を紹介します。

    > **ノート：**
    >
    > 手順 3 で TiKV を再起動する必要があります。TiKV を再起動できない場合は、 [方法 2](#method-2-back-up-and-restore-using-an-access-key-easy)を使用してデータをバックアップおよび復元します。

    1.  このノードの TiKV ポートが 24000、つまり「systemd」サービスの名前が「tikv-24000」であるとします。

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

    3.  構成をリロードし、TiKV を再起動します。

        ```
        systemctl daemon-reload
        systemctl restart tikv-24000
        ```

-   コマンド ラインで開始された TiKV および BR の Azure AD 情報を構成するには、次のコマンドを実行して、環境変数`$AZURE_CLIENT_ID` 、 `$AZURE_TENANT_ID` 、および`$AZURE_CLIENT_SECRET`が動作環境で構成されているかどうかを確認するだけで済みます。

    ```
    echo $AZURE_CLIENT_ID
    echo $AZURE_TENANT_ID
    echo $AZURE_CLIENT_SECRET
    ```

環境変数の詳細については、 [Azblob URL パラメーター](/br/backup-and-restore-storages.md#azblob-url-parameters)を参照してください。

#### バックアップする {#back-up}

このセクションは、データを`cool tier`にバックアップすることを示しています。つまり、アップロードされたオブジェクトのアクセス層は`Cool`です。 `account-name`と`access-tier`は 2 つの方法で指定できます。バックアップ操作は、選択した方法によって異なります。

-   URL のパラメーターとして`account-name`と`access-tier`を指定します。

    ```
    tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1&access-tier=Cool'
    ```

    `access-tier`が設定されていない (値が空である) 場合、値はデフォルトで`Hot`になります。

-   コマンドライン パラメータとして`account-name`と`access-tier`を指定します。

    ```
    tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1 --azblob.access-tier=Cool
    ```

#### 戻す {#restore}

[バックアップする](#back-up)で`account-name`を指定する方法と同様に、URL またはコマンドライン パラメーターを使用してデータを復元できます。

-   URL のパラメーターとして`account-name`を指定します。

    ```
    tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1'
    ```

-   コマンドライン パラメータとして`account-name`を指定します。

    ```
    tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1
    ```

### 方法 2: アクセス キーを使用してバックアップおよび復元する (簡単) {#method-2-back-up-and-restore-using-an-access-key-easy}

Azure AD を使用したデータのバックアップと復元に比べて、アクセス キーを使用したバックアップと復元は、環境変数を構成する必要がないため簡単です。その他の手順は、Azure AD を使用する場合と同様です。

#### バックアップする {#back-up}

-   URL のパラメーターとして`account-name` 、 `account-key` 、および`access-tier`を指定します。

    ```
    tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1&account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==&access-tier=Cool'
    ```

-   コマンドライン パラメータとして`account-name` 、 `account-key` 、および`access-tier`を指定します。

    ```
    tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1 --azblob.account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw== --azblob.access-tier=Cool
    ```

#### 戻す {#restore}

-   URL のパラメーターとして`account-name`と`account-key`を指定します。

    ```
    tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1&account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw=='
    ```

-   コマンドライン パラメータとして`account-name`と`account-key`を指定します。

    ```
    tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1 --azblob.account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==
    ```

## 互換性 {#compatibility}

この機能は、v5.4.0 以降のバージョンとの**み互換性**があります。

## こちらもご覧ください {#see-also}

-   BR でサポートされているその他の外部ストレージについては、 [外部ストレージ](/br/backup-and-restore-storages.md)を参照してください。
-   パラメータの詳細については、次のドキュメントを参照してください。

    -   [Azblob URL パラメーター](/br/backup-and-restore-storages.md#azblob-url-parameters)
    -   [Azblob コマンド ライン パラメーター](/br/backup-and-restore-storages.md#azblob-command-line-parameters)
