---
title: Quick Start Guide for PingCAP Clinic
summary: PingCAPクリニックは、クラスター診断データを迅速に収集・閲覧できるサービスです。DiagクライアントとClinic Serverで構成されています。ユーザーはDiagで診断データを収集し、Clinic Serverにアップロードして、Health Reportの結果を閲覧できます。ご利用前に、Diagをインストールし、Clinic Serverにログインし、組織を作成し、アクセストークンを取得して、Diagでトークンとリージョンを設定する必要があります。データを収集・アップロードした後、データアクセスリンクを取得し、Health Reportを閲覧できるようになります。
---

# PingCAPクリニッククイックスタートガイド {#quick-start-guide-for-pingcap-clinic}

このドキュメントでは、 PingCAPクリニック診断サービス (PingCAPクリニック) を使用して、クラスター診断データを迅速に収集、アップロード、表示する方法について説明します。

PingCAPクリニックは、 [診断クライアント](https://github.com/pingcap/diag) （Diagと略記）とClinic Serverクラウドサービス（Clinic Serverと略記）の2つのコンポーネントで構成されています。これらの2つのコンポーネントの詳細については、 [PingCAPクリニックの概要](/clinic/clinic-introduction.md)を参照してください。

## ユーザーシナリオ {#user-scenarios}

-   PingCAP テクニカル サポートからリモートで支援を受ける際にクラスターの問題を正確に特定し、迅速に解決するには、Diag を使用して診断データを収集し、収集したデータを Clinic Server にアップロードして、データ アクセス リンクをテクニカル サポートに提供することができます。
-   クラスターが正常に実行されており、クラスターのステータスを確認する必要がある場合は、Diag を使用して診断データを収集し、そのデータを Clinic Server にアップロードして、Health Report の結果を表示できます。

> **注記：**
>
> -   以下のデータ収集およびアップロード方法は[TiUPを使用して展開されたクラスター](/production-deployment-using-tiup.md)に**のみ**適用されます。Kubernetes 上のTiDB Operatorを使用してデプロイされたクラスターの場合は、 [TiDB Operator環境向けPingCAPクリニック](https://docs.pingcap.com/tidb-in-kubernetes/stable/clinic-user-guide)参照してください。
> -   PingCAPクリニックによって収集された診断データは、クラスターの問題のトラブルシューティングに**のみ**使用されます。

## 前提条件 {#prerequisites}

PingCAPクリニックを使用する前に、Diag をインストールし、データをアップロードするための環境を準備する必要があります。

1.  TiUPがインストールされているコントロール マシンで、次のコマンドを実行して Diag をインストールします。

    ```bash
    tiup install diag
    ```

2.  クリニックサーバーにログインします。

    <SimpleTab groupId="clinicServer">
     <div label="Clinic Server for international users" value="clinic-us">



    > **注記：**
    >
    > TiDB Cloudアカウントは、SSO モードで Clinic Server にログインする場合にのみ使用され、 TiDB Cloudサービスへのアクセスには必須ではありません。

    </div>

    <div label="Clinic Server for users in the Chinese mainland" value="clinic-cn">

    [中国本土のユーザー向けクリニックサーバー](https://clinic.pingcap.com.cn)に進み、 **「AskTUGを続ける」**を選択してAskTUGコミュニティのログインページに進みます。AskTUGアカウントをお持ちでない場合は、このページでアカウントを作成してください。

    </div>
     </SimpleTab>

3.  Clinic Server 上に組織を作成します。組織は TiDB クラスターの集合です。作成した組織に診断データをアップロードできます。

4.  データをアップロードするには、アクセストークンを取得してください。Diag を通じて収集したデータをアップロードする際は、データが安全に分離されていることを確認するために、ユーザー認証用のトークンが必要です。クリニックサーバーから既にトークンを取得している場合は、そのトークンを再利用できます。



    ![An example of a token](/media/clinic-get-token.png)

    > **注記：**
    >
    > -   データセキュリティのため、TiDBはトークン作成時にのみトークン情報を表示します。トークン情報を紛失した場合は、古いトークンを削除して新しいトークンを作成できます。
    > -   トークンはデータのアップロードにのみ使用されます。

5.  Diag にトークンと`region`設定します。

    -   `clinic.token`設定するには、次のコマンドを実行します。

        ```bash
        tiup diag config clinic.token ${token-value}
        ```

    -   `clinic.region`設定するには、次のコマンドを実行します。

    `region` 、データの圧縮に使用する暗号化証明書と、データのアップロード時に使用する対象サービスを決定します。例:

    > **注記：**
    >
    > -   Diag v0.9.0 以降のバージョンでは設定`region`サポートされます。
    > -   Diag v0.9.0より前のバージョンでは、データはデフォルトで中国リージョンのClinic Serverにアップロードされます。これらのバージョンで`region`設定するには、 `tiup update diag`コマンドを実行してDiagを最新バージョンにアップグレードし、その後Diagで`region`設定してください。

    <SimpleTab groupId="clinicServer">
     <div label="Clinic Server for international users" value="clinic-us">

    国際ユーザー向けに Clinic Server を使用する場合は、次のコマンドを使用して`region`を`US`設定します。

    ```bash
    tiup diag config clinic.region US
    ```

    </div>
     <div label="Clinic Server for users in the Chinese mainland" value="clinic-cn">

    中国本土のユーザー向けに Clinic Server を使用する場合は、次のコマンドを使用して`region`を`CN`設定します。

    ```bash
    tiup diag config clinic.region CN
    ```

    </div>

    </SimpleTab>

6.  (オプション) ログ編集を有効にします。

    TiDBが詳細なログ情報を提供する場合、ログに機密情報（ユーザーデータなど）が出力される可能性があります。ローカルログおよびClinic Serverへの機密情報の漏洩を防ぎたい場合は、TiDB側でログ編集を有効にすることができます。詳細については、 [ログ編集](/log-redaction.md#log-redaction-in-tidb-side)ご覧ください。

## 手順 {#steps}

1.  Diag を実行して診断データを収集します。

    たとえば、現在の時刻に基づいて 4 時間前から 2 時間前までの診断データを収集するには、次のコマンドを実行します。

    ```bash
    tiup diag collect ${cluster-name} -f="-4h" -t="-2h"
    ```

    コマンドを実行しても、Diag はすぐにデータ収集を開始するわけではありません。代わりに、Diag は推定データサイズとターゲットデータstorageパスを出力に表示し、続行するかどうかを確認します。データ収集を開始するには、 `Y`と入力してください。

    収集が完了すると、Diag は収集されたデータが保存されているフォルダー パスを提供します。

2.  収集したデータをクリニックサーバーにアップロードします。

    > **注記：**
    >
    > アップロードするデータ（収集されたデータを含む圧縮ファイル）のサイズは3GB**以下に**してください。3GBを超える場合、データのアップロードは失敗します。

    -   クラスターが配置されているネットワークがインターネットにアクセスできる場合は、次のコマンドを使用して、収集されたデータを含むフォルダーを直接アップロードできます。

        ```bash
        tiup diag upload ${filepath}
        ```

        アップロードが完了すると、出力に`Download URL`表示されます。

        > **注記：**
        >
        > この方法でデータをアップロードする場合は、Diag v0.9.0以降のバージョンを使用する必要があります。Diagのバージョンは実行時に取得できます。Diagのバージョンが0.9.0より前のバージョンの場合は、 `tiup update diag`コマンドを使用してDiagを最新バージョンにアップグレードできます。

    -   クラスターが設置されているネットワークがインターネットにアクセスできない場合は、収集したデータをパックしてアップロードする必要があります。詳細は[方法2. データをパックしてアップロードする](/clinic/clinic-user-guide-for-tiup.md#method-2-pack-and-upload-data)ご覧ください。

3.  アップロードが完了したら、コマンド出力の`Download URL`からデータ アクセス リンクを取得します。

    デフォルトでは、診断データには、クラスター名、クラスター トポロジ情報、収集された診断データ内のログ コンテンツ、収集されたデータ内のメトリックに基づいて再構成された Grafana ダッシュボード情報が含まれます。

    データを使用してクラスターの問題を自分でトラブルシューティングすることも、PingCAP テクニカル サポート スタッフにデータ アクセス リンクを提供してリモート トラブルシューティングを容易にすることもできます。

4.  健康レポートの結果をビュー

    データがアップロードされると、Clinic Server はバックグラウンドで自動的にデータを処理します。ヘルスレポートは約5～15分で生成されます。診断データリンクを開き、「ヘルスレポート」をクリックすると、レポートをご覧いただけます。

## 次は何？ {#what-s-next}

-   [PingCAPクリニックの概要](/clinic/clinic-introduction.md)
-   [PingCAPクリニックを使用したクラスターのトラブルシューティング](/clinic/clinic-user-guide-for-tiup.md)
-   [PingCAPクリニック診断データ](/clinic/clinic-data-instruction-for-tiup.md)
