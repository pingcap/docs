---
title: Quick Start Guide for PingCAP Clinic
summary: Learn how to use PingCAP Clinic to collect, upload, and view cluster diagnosis data quickly.
---

# PingCAPクリニックのクイック スタート ガイド {#quick-start-guide-for-pingcap-clinic}

このドキュメントでは、 PingCAPクリニック診断サービス (PingCAPクリニック) を使用してクラスター診断データを迅速に収集、アップロード、および表示する方法について説明します。

PingCAPクリニック は、 2 つのコンポーネントで構成されています[クライアントを診断する](https://github.com/pingcap/diag) (Diag と短縮) と Clinic Server クラウド サービス (Clinic Server と短縮)。これら 2 つのコンポーネントの詳細については、 [PingCAPクリニックの概要](/clinic/clinic-introduction.md)を参照してください。

## ユーザーシナリオ {#user-scenarios}

-   PingCAP テクニカル サポートにリモートでサポートを求めるときにクラスターの問題を正確に特定して迅速に解決するには、Diag を使用して診断データを収集し、収集したデータをクリニック サーバーにアップロードし、テクニカル サポートへのデータ アクセス リンクを提供します。
-   クラスターが適切に実行されており、クラスターのステータスを確認する必要がある場合は、Diag を使用して診断データを収集し、そのデータを Clinic Server にアップロードし、ヘルス レポートの結果を表示できます。

> **注記：**
>
> -   データを収集してアップロードする次の方法は[TiUPを使用してデプロイされたクラスター](/production-deployment-using-tiup.md)に**のみ**適用されます。 TiDB Operator on Kubernetes を使用してデプロイされたクラスターについては、 [TiDB Operator環境向けPingCAPクリニック](https://docs.pingcap.com/tidb-in-kubernetes/stable/clinic-user-guide)を参照してください。
> -   PingCAPクリニックによって収集された診断データは、クラスターの問題のトラブルシューティングに**のみ**使用されます。

## 前提条件 {#prerequisites}

PingCAPクリニックを使用する前に、Diag をインストールし、データをアップロードする環境を準備する必要があります。

1.  TiUPがインストールされている制御マシンで、次のコマンドを実行して Diag をインストールします。

    ```bash
    tiup install diag
    ```

2.  クリニックサーバーにログインします。

    <SimpleTab groupId="clinicServer">
     <div label="Clinic Server for international users" value="clinic-us">

    [海外ユーザー向けクリニックサーバー](https://clinic.pingcap.com)に進み、 **「TiDB アカウントでサインイン」**を選択して、 TiDB Cloudのログイン ページに入ります。 TiDB Cloudアカウントをお持ちでない場合は、そのページで作成してください。

    > **注記：**
    >
    > TiDB Cloudアカウントは、SSO モードで Clinic Server にログインする場合にのみ使用され、 TiDB Cloudサービスへのアクセスには必須ではありません。

    </div>

    <div label="Clinic Server for users in the Chinese mainland" value="clinic-cn">

    [中国本土のユーザー向けクリニックサーバー](https://clinic.pingcap.com.cn)に進み、 **「AskTUG でサインイン」**を選択して、AskTUG コミュニティのログイン ページに入ります。 AskTUG アカウントをお持ちでない場合は、そのページでアカウントを作成してください

    </div>
     </SimpleTab>

3.  Clinic Server 上に組織を作成します。組織は TiDB クラスターの集合です。作成した組織の診断データをアップロードできます。

4.  データをアップロードするためのアクセス トークンを取得します。 Diag を通じて収集したデータをアップロードする場合、データが安全に分離されていることを確認するためにユーザー認証用のトークンが必要です。すでにクリニック サーバーからトークンを取得している場合は、そのトークンを再利用できます。

    トークンを取得するには、 [クラスタ]ページの右下隅にあるアイコンをクリックし、 **[診断ツールのアクセス トークンの取得]**を選択し、ポップアップ ウィンドウで**[+]**をクリックします。表示されたトークンをコピーして保存したことを確認してください。

    ![An example of a token](/media/clinic-get-token.png)

    > **注記：**
    >
    > -   データのセキュリティのため、TiDB はトークンの作成時にのみトークン情報を表示します。情報を紛失した場合は、古いトークンを削除して、新しいトークンを作成できます。
    > -   トークンはデータのアップロードにのみ使用されます。

5.  Diagにトークンと`region`を設定します。

    -   次のコマンドを実行して`clinic.token`を設定します。

        ```bash
        tiup diag config clinic.token ${token-value}
        ```

    -   次のコマンドを実行して`clinic.region`を設定します。

    `region`データのアップロード時にデータとターゲット サービスをパッキングするために使用される暗号化証明書を決定します。例えば：

    > **注記：**
    >
    > -   Diag v0.9.0 以降のバージョンでは、設定`region`サポートされています。
    > -   Diag v0.9.0 より前のバージョンの場合、データはデフォルトで中国地域の Clinic Server にアップロードされます。これらのバージョンで`region`を設定するには、 `tiup update diag`コマンドを実行して Diag を最新バージョンにアップグレードし、Diag で`region`を設定します。

    <SimpleTab groupId="clinicServer">
     <div label="Clinic Server for international users" value="clinic-us">

    海外ユーザー向けに Clinic Server を使用する場合は、次のコマンドを使用して`region` ～ `US`を設定します。

    ```bash
    tiup diag config clinic.region US
    ```

    </div>
     <div label="Clinic Server for users in the Chinese mainland" value="clinic-cn">

    中国本土のユーザーに対して Clinic Server を使用する場合は、次のコマンドを使用して`region` ～ `CN`を設定します。

    ```bash
    tiup diag config clinic.region CN
    ```

    </div>

    </SimpleTab>

6.  (オプション) ログの編集を有効にします。

    TiDB が詳細なログ情報を提供する場合、機密情報 (ユーザー データなど) がログに出力される場合があります。ローカル ログおよびクリニック サーバー内の機密情報の漏洩を回避したい場合は、TiDB 側でログの編集を有効にすることができます。詳細については、 [ログ編集](/log-redaction.md#log-redaction-in-tidb-side)を参照してください。

## ステップ {#steps}

1.  Diag を実行して診断データを収集します。

    たとえば、現在時刻に基づいて 4 時間前から 2 時間前までの診断データを収集するには、次のコマンドを実行します。

    ```bash
    tiup diag collect ${cluster-name} -f="-4h" -t="-2h"
    ```

    コマンドを実行した後、Diag はデータの収集をすぐには開始しません。代わりに、Diag は、続行するかどうかを確認するために、出力で推定データ サイズとターゲット データstorageパスを提供します。データ収集の開始を確認するには、 `Y`と入力します。

    収集が完了すると、Diag は収集されたデータが配置されるフォルダー パスを提供します。

2.  収集したデータをクリニックサーバーにアップロードします。

    > **注記：**
    >
    > アップロードするデータ（収集したデータを圧縮したファイル）のサイズは3GB**以下に**してください。それ以外の場合、データのアップロードは失敗します。

    -   クラスターが配置されているネットワークがインターネットにアクセスできる場合は、次のコマンドを使用して、収集したデータを含むフォルダーを直接アップロードできます。

        ```bash
        tiup diag upload ${filepath}
        ```

        アップロードが完了すると、出力に`Download URL`が表示されます。

        > **注記：**
        >
        > この方法でデータをアップロードする場合は、Diag v0.9.0 以降のバージョンを使用する必要があります。 Diag を実行すると、Diag のバージョンを取得できます。 Diag のバージョンが 0.9.0 より前の場合は、 `tiup update diag`コマンドを使用して Diag を最新バージョンにアップグレードできます。

    -   クラスターが配置されているネットワークがインターネットにアクセスできない場合は、収集したデータを圧縮してパッケージをアップロードする必要があります。詳細は[方法 2. データをパックしてアップロードする](/clinic/clinic-user-guide-for-tiup.md#method-2-pack-and-upload-data)を参照してください。

3.  アップロードが完了したら、コマンド出力の`Download URL`からデータ アクセス リンクを取得します。

    デフォルトでは、診断データには、クラスター名、クラスター トポロジ情報、収集された診断データのログ内容、および収集されたデータのメトリックに基づいて再編成された Grafana ダッシュボード情報が含まれます。

    データを使用してクラスターの問題を自分でトラブルシューティングすることも、PingCAP テクニカル サポート スタッフにデータ アクセス リンクを提供して、リモート トラブルシューティングを容易にすることもできます。

4.  ヘルスレポートの結果をビュー

    データがアップロードされると、Clinic Server はバックグラウンドでデータを自動的に処理します。ヘルスレポートは約 5 ～ 15 分で生成されます。診断データのリンクを開いて「ヘルスレポート」をクリックすると、レポートを表示できます。

## 次は何ですか {#what-s-next}

-   [PingCAPクリニックの概要](/clinic/clinic-introduction.md)
-   [PingCAPクリニックを使用したクラスターのトラブルシューティング](/clinic/clinic-user-guide-for-tiup.md)
-   [PingCAPクリニックの診断データ](/clinic/clinic-data-instruction-for-tiup.md)
