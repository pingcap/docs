---
title: Quick Start Guide for PingCAP Clinic
summary: Learn how to use PingCAP Clinic to collect, upload, and view cluster diagnosis data quickly.
---

# PingCAPクリニックのクイックスタートガイド {#quick-start-guide-for-pingcap-clinic}

このドキュメントでは、 PingCAPクリニック診断サービス（PingCAPクリニック）を使用して、クラスタ診断データをすばやく収集、アップロード、および表示する方法について説明します。

PingCAPクリニックは、Diagクライアント（Diagと短縮）とClinic Serverクラウドサービス（Clinic Serverと短縮）の2つのコンポーネントで構成されています。これら2つのコンポーネントの詳細については、 [PingCAPクリニックの概要](/clinic/clinic-introduction.md)を参照してください。

## ユーザーシナリオ {#user-scenarios}

-   PingCAPテクニカルサポートからリモートでヘルプを求めるときにクラスタの問題を正確に特定して迅速に解決するために、Diagで診断データを収集し、収集したデータをクリニックサーバーにアップロードし、テクニカルサポートへのデータアクセスリンクを提供できます。
-   クラスタが正常に実行されていて、クラスタのステータスを確認する必要がある場合は、Diagを使用して診断データを収集し、データをClinic Serverにアップロードして、ヘルスレポートの結果を表示できます。

> **ノート：**
>
> -   データを収集およびアップロードする次の方法は、 [TiUPを使用して展開されたクラスター](/production-deployment-using-tiup.md)に**のみ**適用されます。 KubernetesでTiDB Operatorを使用してデプロイされたクラスターについては、 [TiDBTiDB Operator環境向けのPingCAPクリニック](https://docs.pingcap.com/tidb-in-kubernetes/stable/clinic-user-guide)を参照してください。
> -   PingCAPクリニックによって収集された診断データは、クラスタの問題のトラブルシューティングに**のみ**使用されます。

## 前提条件 {#prerequisites}

PingCAPクリニックを使用する前に、Diagをインストールし、データをアップロードするための環境を準備する必要があります。

1.  TiUPがインストールされているコントロールマシンで、次のコマンドを実行してDiagをインストールします。

    ```bash
    tiup install diag
    ```

2.  クリニックサーバーにログインします。

    <SimpleTab>
     <div label="Clinic Server in the US">

    [米国のクリニックサーバー](https://clinic.pingcap.com)に移動し、[ **TiDBアカウントでサインイン]**を選択して、 TiDB Cloudログインページに入ります。 TiDB Cloudアカウントをお持ちでない場合は、そのページで作成してください。

    > **ノート：**
    >
    > TiDB Cloudアカウントは、SSOモードでClinic Serverにログインするためにのみ使用され、 TiDB Cloudサービスにアクセスするために必須ではありません。

    </div>

    <div label="Clinic Server in the Chinese mainland">

    [中国本土のクリニックサーバー](https://clinic.pingcap.com.cn)に移動し、[ **AskTUGでサインイン]を**選択して、AskTUGコミュニティのログインページに入ります。 AskTUGアカウントをお持ちでない場合は、そのページでアカウントを作成してください

    </div>
     </SimpleTab>

3.  クリニックサーバー上に組織を作成します。編成は、TiDBクラスターのコレクションです。作成した組織の診断データをアップロードできます。

4.  データをアップロードするためのアクセストークンを取得します。収集したデータをDiagを介してアップロードする場合、データを安全に分離するために、ユーザー認証用のトークンが必要です。クリニックサーバーからすでにトークンを取得している場合は、トークンを再利用できます。

    トークンを取得するには、[クラスター]ページの右下隅にあるアイコンをクリックし、[**診断ツールのアクセストークンの取得**]を選択して、ポップアップウィンドウで[ <strong>+</strong> ]をクリックします。表示されたトークンをコピーして保存したことを確認してください。

    ![An example of a token](/media/clinic-get-token.png)

    > **ノート：**
    >
    > -   データセキュリティのために、TiDBはトークン情報が作成されたときにのみ表示します。情報を紛失した場合は、古いトークンを削除して新しいトークンを作成できます。
    > -   トークンは、データのアップロードにのみ使用されます。

5.  Diagにトークンと`region`を設定します。

    -   次のコマンドを実行して、 `clinic.token`を設定します。

        ```bash
        tiup diag config clinic.token ${token-value}
        ```

    -   次のコマンドを実行して、 `clinic.region`を設定します。

    `region`は、データのアップロード時にデータとターゲットサービスをパックするために使用される暗号化証明書を決定します。例えば：

    > **ノート：**
    >
    > -   Diag v0.9.0以降のバージョンは、設定`region`をサポートします。
    > -   Diag v0.9.0より前のバージョンの場合、データはデフォルトで中国地域のClinicServerにアップロードされます。これらのバージョンで`region`を設定するには、 `tiup update diag`コマンドを実行してDiagを最新バージョンにアップグレードしてから、Diagで`region`を設定します。

    <SimpleTab>
     <div label="Clinic Server in the US">

    米国のClinicServerの場合、次のコマンドを使用して`region`から`US`に設定します。

    ```bash
    tiup diag config clinic.region US
    ```

    </div>
     <div label="Clinic Server in the Chinese mainland">

    中国本土のクリニックサーバーの場合、次のコマンドを使用して`region`から`CN`に設定します。

    ```bash
    tiup diag config clinic.region CN
    ```

    </div>

    </SimpleTab>

6.  （オプション）ログ編集を有効にします。

    TiDBが詳細なログ情報を提供すると、機密情報（ユーザーデータなど）がログに出力される場合があります。ローカルログとクリニックサーバーで機密情報が漏洩するのを防ぎたい場合は、TiDB側でログの編集を有効にすることができます。詳細については、 [ログ編集](/log-redaction.md#log-redaction-in-tidb-side)を参照してください。

## 手順 {#steps}

1.  Diagを実行して診断データを収集します。

    たとえば、現在の時刻に基づいて4時間前から2時間前までの診断データを収集するには、次のコマンドを実行します。

    ```bash
    tiup diag collect ${cluster-name} -f="-4h" -t="-2h"
    ```

    コマンドを実行した後、Diagはすぐにデータの収集を開始しません。代わりに、Diagは、続行するかどうかを確認するために、出力に推定データサイズとターゲットデータストレージパスを提供します。データの収集を開始することを確認するには、 `Y`を入力します。

    収集が完了すると、Diagは収集されたデータが配置されているフォルダーパスを提供します。

2.  収集したデータをクリニックサーバーにアップロードします。

    > **ノート：**
    >
    > アップロードするデータ（収集されたデータを含む圧縮ファイル）のサイズは、3GB**以下で**ある必要があります。それ以外の場合、データのアップロードは失敗します。

    -   クラスタが配置されているネットワークがインターネットにアクセスできる場合は、次のコマンドを使用して、収集されたデータを含むフォルダを直接アップロードできます。

        {{< copyable "" >}}

        ```bash
        tiup diag upload ${filepath}
        ```

        アップロードが完了すると、出力に`Download URL`が表示されます。

        > **ノート：**
        >
        > この方法でデータをアップロードする場合は、Diagv0.9.0以降を使用する必要があります。実行すると、Diagバージョンを取得できます。 Diagのバージョンが0.9.0より前の場合は、 `tiup update diag`コマンドを使用してDiagを最新バージョンにアップグレードできます。

    -   クラスタが配置されているネットワークがインターネットにアクセスできない場合は、収集したデータをパックして、パッケージをアップロードする必要があります。詳細については、 [方法2.データをパックしてアップロードする](/clinic/clinic-user-guide-for-tiup.md#method-2-pack-and-upload-data)を参照してください。

3.  アップロードが完了したら、コマンド出力の`Download URL`からデータアクセスリンクを取得します。

    デフォルトでは、診断データには、クラスタ名、クラスタトポロジ情報、収集された診断データのログコンテンツ、および収集されたデータのメトリックに基づいて再編成されたGrafanaダッシュボード情報が含まれます。

    データを使用してクラスタの問題を自分でトラブルシューティングすることも、データアクセスリンクをPingCAPテクニカルサポートスタッフに提供してリモートトラブルシューティングを容易にすることもできます。

4.  ヘルスレポートの結果をビューする

    データがアップロードされた後、ClinicServerはバックグラウンドでデータを自動的に処理します。ヘルスレポートは約5〜15分で生成されます。診断データのリンクを開いて「ヘルスレポート」をクリックすると、レポートを表示できます。

## 次は何ですか {#what-s-next}

-   [PingCAPクリニックの概要](/clinic/clinic-introduction.md)
-   [PingCAPクリニックを使用したTiDBクラスターのトラブルシューティング](/clinic/clinic-user-guide-for-tiup.md)
-   [PingCAPクリニックの診断データ](/clinic/clinic-data-instruction-for-tiup.md)
