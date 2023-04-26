---
title: Quick Start Guide for PingCAP Clinic
summary: Learn how to use PingCAP Clinic to collect, upload, and view cluster diagnosis data quickly.
---

# PingCAPクリニックのクイック スタート ガイド {#quick-start-guide-for-pingcap-clinic}

このドキュメントでは、 PingCAPクリニック診断サービス (PingCAPクリニック) を使用してクラスター診断データを迅速に収集、アップロード、および表示する方法について説明します。

PingCAPクリニック は、 [診断クライアント](https://github.com/pingcap/diag) (略して Diag) と Clinic Server クラウド サービス (略して Clinic Server) の 2 つのコンポーネントで構成されています。これら 2 つのコンポーネントの詳細については、 [PingCAPクリニックの概要](/clinic/clinic-introduction.md)を参照してください。

## ユーザー シナリオ {#user-scenarios}

-   PingCAP テクニカル サポートからリモートでヘルプを求めるときにクラスターの問題を正確に特定して迅速に解決するには、Diag を使用して診断データを収集し、収集したデータを Clinic Server にアップロードして、テクニカル サポートへのデータ アクセス リンクを提供します。
-   クラスタが正常に動作していて、クラスタのステータスを確認する必要がある場合は、Diag を使用して診断データを収集し、データを Clinic Server にアップロードして、Health Report の結果を表示できます。

> **ノート：**
>
> -   データを収集してアップロードする次の方法は、 [TiUPを使用してデプロイされたクラスター](/production-deployment-using-tiup.md)に**のみ**適用されます。 TiDB Operatorを使用して Kubernetes にデプロイされたクラスターについては、 [TiDB Operator環境向けのPingCAPクリニック](https://docs.pingcap.com/tidb-in-kubernetes/stable/clinic-user-guide)を参照してください。
> -   PingCAPクリニックによって収集された診断データは、クラスターの問題のトラブルシューティングに**のみ**使用されます。

## 前提条件 {#prerequisites}

PingCAPクリニックを利用する前に、Diag をインストールし、データをアップロードするための環境を準備する必要があります。

1.  TiUPがインストールされているコントロール マシンで、次のコマンドを実行して Diag をインストールします。

    ```bash
    tiup install diag
    ```

2.  クリニック サーバーにログインします。

    <SimpleTab groupId="clinicServer">
     <div label="Clinic Server for international users" value="clinic-us">

    [海外ユーザー向けクリニックサーバー](https://clinic.pingcap.com)に移動し、 **[TiDB アカウントでサインイン]**を選択して、 TiDB Cloudのログイン ページに入ります。 TiDB Cloudアカウントをお持ちでない場合は、そのページで作成してください。

    > **ノート：**
    >
    > TiDB Cloudアカウントは、SSO モードで Clinic Server にログインするためにのみ使用され、 TiDB Cloudサービスへのアクセスには必須ではありません。

    </div>

    <div label="Clinic Server for users in the Chinese mainland" value="clinic-cn">

    [中国本土のユーザー向けクリニックサーバー](https://clinic.pingcap.com.cn)に移動し、 **[AskTUG でサインイン]**を選択して、AskTUG コミュニティのログイン ページに入ります。 AskTUG アカウントをお持ちでない場合は、そのページでアカウントを作成してください

    </div>
     </SimpleTab>

3.  Clinic Server に組織を作成します。組織は TiDB クラスターの集まりです。作成した組織に診断データをアップロードできます。

4.  データをアップロードするためのアクセス トークンを取得します。収集したデータを Diag を介してアップロードする場合、データが安全に分離されるように、ユーザー認証用のトークンが必要です。 Clinic Server から既にトークンを取得している場合は、そのトークンを再利用できます。

    トークンを取得するには、 [クラスタ]ページの右下隅にあるアイコンをクリックし、 **[診断ツールのアクセス トークンを取得]**を選択し、ポップアップ ウィンドウで<strong>[+]</strong>をクリックします。表示されたトークンをコピーして保存したことを確認してください。

    ![An example of a token](/media/clinic-get-token.png)

    > **ノート：**
    >
    > -   データのセキュリティのために、TiDB は作成時にトークン情報のみを表示します。情報を紛失した場合は、古いトークンを削除して新しいトークンを作成できます。
    > -   トークンは、データのアップロードにのみ使用されます。

5.  Diag に token と`region`を設定します。

    -   次のコマンドを実行して`clinic.token`を設定します。

        ```bash
        tiup diag config clinic.token ${token-value}
        ```

    -   次のコマンドを実行して`clinic.region`を設定します。

    `region`データのパッキングに使用される暗号化証明書と、データのアップロード時のターゲット サービスを決定します。例えば：

    > **ノート：**
    >
    > -   Diag v0.9.0 以降のバージョンは設定`region`をサポートします。
    > -   Diag v0.9.0 より前のバージョンでは、データはデフォルトで中国地域の Clinic Server にアップロードされます。これらのバージョンで`region`を設定するには、 `tiup update diag`コマンドを実行して Diag を最新バージョンにアップグレードしてから、Diag で`region`を設定します。

    <SimpleTab groupId="clinicServer">
     <div label="Clinic Server for international users" value="clinic-us">

    海外ユーザー向けに Clinic Server を使用する場合は、次のコマンドを使用して`region` ～ `US`を設定します。

    ```bash
    tiup diag config clinic.region US
    ```

    </div>
     <div label="Clinic Server for users in the Chinese mainland" value="clinic-cn">

    中国本土のユーザーに Clinic Server を使用する場合は、次のコマンドを使用して`region` ～ `CN`を設定します。

    ```bash
    tiup diag config clinic.region CN
    ```

    </div>

    </SimpleTab>

6.  (オプション) ログのリダクションを有効にします。

    TiDB が詳細なログ情報を提供する場合、機密情報 (ユーザー データなど) をログに出力することがあります。ローカル ログと Clinic Server で機密情報が漏洩するのを避けたい場合は、TiDB 側でログの編集を有効にすることができます。詳細については、 [ログ編集](/log-redaction.md#log-redaction-in-tidb-side)を参照してください。

## 手順 {#steps}

1.  Diag を実行して、診断データを収集します。

    たとえば、現在の時刻に基づいて 4 時間前から 2 時間前までの診断データを収集するには、次のコマンドを実行します。

    ```bash
    tiup diag collect ${cluster-name} -f="-4h" -t="-2h"
    ```

    コマンドを実行した後、Diag はデータの収集をすぐには開始しません。代わりに、Diag は推定データ サイズとターゲット データstorageパスを出力で提供し、続行するかどうかを確認します。データの収集を開始することを確認するには、 `Y`を入力します。

    収集が完了すると、Diag は、収集されたデータが配置されているフォルダー パスを提供します。

2.  収集したデータを Clinic Server にアップロードします。

    > **ノート：**
    >
    > アップロードするデータ（収集したデータを圧縮したファイル）のサイズは、3 GB**を超えない**ようにしてください。そうしないと、データのアップロードは失敗します。

    -   クラスターが配置されているネットワークがインターネットにアクセスできる場合は、次のコマンドを使用して、収集されたデータを含むフォルダーを直接アップロードできます。

        {{< copyable "" >}}

        ```bash
        tiup diag upload ${filepath}
        ```

        アップロードが完了すると、出力に`Download URL`が表示されます。

        > **ノート：**
        >
        > この方法でデータをアップロードする場合は、Diag v0.9.0 以降のバージョンを使用する必要があります。実行すると、Diag バージョンを取得できます。 Diag のバージョンが 0.9.0 より前の場合は、 `tiup update diag`コマンドを使用して Diag を最新バージョンにアップグレードできます。

    -   クラスターが配置されているネットワークがインターネットにアクセスできない場合は、収集したデータをパックしてパッケージをアップロードする必要があります。詳細については、 [方法 2. データをパックしてアップロードする](/clinic/clinic-user-guide-for-tiup.md#method-2-pack-and-upload-data)を参照してください。

3.  アップロードが完了したら、コマンド出力の`Download URL`からデータ アクセス リンクを取得します。

    デフォルトでは、診断データには、収集された診断データ内のクラスター名、クラスター トポロジー情報、ログ コンテンツ、および収集されたデータ内のメトリックに基づいて再編成された Grafana ダッシュボード情報が含まれます。

    データを使用してクラスターの問題を自分でトラブルシューティングするか、PingCAP テクニカル サポート スタッフにデータ アクセス リンクを提供して、リモート トラブルシューティングを容易にすることができます。

4.  ヘルスレポートの結果をビュー

    データがアップロードされた後、Clinic Server はデータをバックグラウンドで自動的に処理します。正常性レポートは、約 5 ～ 15 分で生成されます。レポートを表示するには、診断データ リンクを開き、[ヘルス レポート] をクリックします。

## 次は何ですか {#what-s-next}

-   [PingCAPクリニックの概要](/clinic/clinic-introduction.md)
-   [PingCAPクリニックを使用したクラスターのトラブルシューティング](/clinic/clinic-user-guide-for-tiup.md)
-   [PingCAPクリニックの診断データ](/clinic/clinic-data-instruction-for-tiup.md)
