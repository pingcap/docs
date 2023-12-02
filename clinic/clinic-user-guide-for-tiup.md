---
title: Troubleshoot Clusters Using PingCAP Clinic
summary: Learn how to use the PingCAP Clinic Diagnostic Service to troubleshoot cluster problems remotely and perform a quick check of the cluster status on a TiDB cluster or DM cluster deployed using TiUP.
---

# PingCAPクリニックを使用したクラスターのトラブルシューティング {#troubleshoot-clusters-using-pingcap-clinic}

TiUPを使用してデプロイされた TiDB クラスターおよび DM クラスターの場合、 PingCAPクリニック診断サービス (PingCAPクリニック) を使用してクラスターの問題をリモートでトラブルシューティングし、 [診断クライアント (Diag)](https://github.com/pingcap/diag)と Clinic Server を使用してローカルでクラスターのステータスを簡単にチェックできます。

> **注記：**
>
> -   このドキュメントは、セルフホスト環境でTiUP を使用してデプロイされたクラスターに**のみ**適用されます。 TiDB Operator on Kubernetes を使用してデプロイされたクラスターについては、 [TiDB Operator環境向けPingCAPクリニック](https://docs.pingcap.com/tidb-in-kubernetes/stable/clinic-user-guide)参照してください。
>
> -   PingCAPクリニック は、 TiDB Ansible を使用してデプロイされたクラスターからのデータ収集を**サポートしていません**。

## ユーザーシナリオ {#user-scenarios}

-   [クラスターの問題をリモートでトラブルシューティングする](#troubleshoot-cluster-problems-remotely)

    -   クラスターに[支持を得ます](/support.md)問題がある場合、PingCAP から必要な場合は、リモート トラブルシューティングを容易にするために次の操作を実行できます。Diag を使用して診断データを収集し、収集したデータをクリニック サーバーにアップロードし、サーバーへのデータ アクセス リンクを提供します。テクニカルサポートスタッフ。
    -   クラスターに問題が発生し、問題をすぐに分析できない場合は、Diag を使用してデータを収集し、後で分析するために保存できます。

-   [クラスターのステータスをローカルで簡単にチェックする](#perform-a-quick-check-on-the-cluster-status-locally)

    現時点ではクラスターが安定して実行されている場合でも、潜在的な安定性リスクを検出するためにクラスターを定期的にチェックする必要があります。 PingCAPクリニックが提供するローカル クイック チェック機能を使用して、クラスターの潜在的な健康リスクを特定できます。ローカル チェックは構成のみをチェックします。メトリクスやログなど、より多くの項目を確認するには、診断データをクリニック サーバーにアップロードし、ヘルス レポート機能を使用することをお勧めします。

## 前提条件 {#prerequisites}

PingCAPクリニックを使用する前に、Diag ( PingCAPクリニックが提供するデータ収集コンポーネント) をインストールし、データをアップロードする環境を準備する必要があります。

1.  インストール診断。

    -   制御マシンにTiUPをインストールしている場合は、次のコマンドを実行して Diag をインストールします。

        ```bash
        tiup install diag
        ```

    -   Diag をインストールしている場合は、次のコマンドを使用して Diag を最新バージョンにアップグレードできます。

        ```bash
        tiup update diag
        ```

    > **注記：**
    >
    > -   インターネット接続のないクラスターの場合は、Diag をオフラインでデプロイする必要があります。詳細は[TiUP をオフラインでデプロイ: 方法 2](/production-deployment-using-tiup.md#deploy-tiup-offline)を参照してください。
    > -   Diag は、v5.4.0 以降の TiDB Server オフライン ミラー パッケージで**のみ**提供されます。

2.  データをアップロードするためのアクセストークン（トークン）を取得、設定します。

    収集したデータをDiag経由でアップロードする場合、ユーザー認証用のトークンが必要です。すでにトークン診断を設定している場合は、トークンを再利用してこの手順をスキップできます。

    トークンを取得するには、次の手順を実行します。

    -   クリニックサーバーにログインします。

        <SimpleTab groupId="clinicServer">
          <div label="Clinic Server for international users" value="clinic-us">

        [海外ユーザー向けクリニックサーバー](https://clinic.pingcap.com) : データは米国の AWS に保存されます。

        </div>
          <div label="Clinic Server for users in the Chinese mainland" value="clinic-cn">

        [中国本土のユーザー向けクリニックサーバー](https://clinic.pingcap.com.cn) : データは中国 (北京) リージョンの AWS に保存されます。

        </div>

        </SimpleTab>

    -   [クラスタ]ページの右下隅にあるアイコンをクリックし、 **[診断ツールのアクセス トークンの取得]**を選択し、ポップアップ ウィンドウで**[+]**をクリックします。表示されたトークンをコピーして保存したことを確認してください。

        ![Get the Token](/media/clinic-get-token.png)

    > **注記：**
    >
    > -   Clinic Server に初めてアクセスする場合は、トークンを取得する前に[PingCAPクリニックのクイック スタート](/clinic/quick-start-with-clinic.md#prerequisites)を参照して環境を準備する必要があります。
    > -   データのセキュリティのため、TiDB はトークンの作成時にのみトークンを表示します。トークンを紛失した場合は、古いトークンを削除して、新しいトークンを作成してください。
    > -   トークンはデータのアップロードにのみ使用されます。

    -   次に、Diag でトークンを設定します。例えば：

        ```bash
        tiup diag config clinic.token ${token-value}
        ```

3.  Diagに`region`を設定します。

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

4.  (オプション) ログの編集を有効にします。

    TiDB が詳細なログ情報を提供する場合、機密情報 (ユーザー データなど) がログに出力される場合があります。ローカル ログおよびクリニック サーバー内の機密情報の漏洩を回避したい場合は、TiDB 側でログの編集を有効にすることができます。詳細については、 [ログ編集](/log-redaction.md#log-redaction-in-tidb-side)を参照してください。

## クラスターの問題をリモートでトラブルシューティングする {#troubleshoot-cluster-problems-remotely}

Diag を使用すると、モニタリング データや構成情報を含む診断データを TiDB クラスターおよび DM クラスターから迅速に収集できます。

### ステップ1. 収集するデータを確認する {#step-1-check-the-data-to-be-collected}

Diag によって収集できるデータの完全なリストについては、 [PingCAPクリニックの診断データ](/clinic/clinic-data-instruction-for-tiup.md)を参照してください。

後の診断の効率を向上させるために、監視データや構成情報を含む完全な診断データを収集することをお勧めします。詳細は[クラスターからデータを収集する](#step-2-collect-data)を参照してください。

### ステップ 2. データを収集する {#step-2-collect-data}

Diag を使用すると、 TiUPを使用してデプロイされた TiDB クラスターおよび DM クラスターからデータを収集できます。

1.  Diagの資料採取コマンドを実行します。

    たとえば、現在時刻に基づいて 4 時間前から 2 時間前までの診断データを収集するには、次のコマンドを実行します。

    <SimpleTab>
     <div label="TiDB Cluster">

    ```bash
    tiup diag collect ${cluster-name} -f="-4h" -t="-2h"
    ```

    </div>
     <div label="DM Cluster">

    ```bash
    tiup diag collectdm ${dm-cluster-name} -f="-4h" -t="-2h"
    ```

    </div>
     </SimpleTab>

    データ収集のパラメータの説明:

    -   `-f/--from` : データ収集の開始時間を指定します。このパラメータを指定しない場合、デフォルトの開始時刻は現在時刻の 2 時間前になります。タイムゾーンを変更するには、 `-f="12:30 +0800"`構文を使用します。このパラメータにタイム ゾーン情報 ( `+0800`など) を指定しない場合、タイム ゾーンはデフォルトで UTC になります。
    -   `-t/--to` : データ収集の終了時刻を指定します。このパラメータを指定しない場合、デフォルトの終了時刻は現在の時刻になります。タイムゾーンを変更するには、 `-f="12:30 +0800"`構文を使用します。このパラメータにタイム ゾーン情報 ( `+0800`など) を指定しない場合、タイム ゾーンはデフォルトで UTC になります。

    パラメータの使用に関するヒント:

    データ収集時間の指定に加えて、Diag を使用してさらに多くのパラメーターを指定できます。すべてのパラメータを取得するには、 `tiup diag collect -h`または`tiup diag collectdm -h`コマンドを実行します。

    > **注記：**
    >
    > -   Diag は、デフォルトではシステム変数データ (db_vars) を収集しません。このデータを収集するには、データベースにアクセスできるユーザー名とパスワードを追加で提供する必要があります。このデータベースではシステム変数への読み取りアクセスを有効にする必要があることに注意してください。
    > -   Diag は、デフォルトではパフォーマンス データ ( `perf` ) とデバッグ データ ( `debug` ) を収集しません。
    > -   システム変数を含む完全な診断データを収集するには、コマンド`tiup diag collect <cluster-name> --include="system,monitor,log,config,db_vars,perf,debug"`を使用します。

    -   `-l` : ファイル転送の帯域幅制限、単位は Kbit/s、デフォルト値は`100000` (scp の`-l`のパラメータ) です。
    -   `-N/--node` : 指定されたノードからのみデータを収集します。形式は`ip:port`です。
    -   `--include` : 特定の種類のデータのみを収集します。オプションの値は`system` 、 `monitor` 、 `log` 、 `config` 、および`db_vars`です。 2 つ以上のタイプを含めるには、タイプ間の区切り文字として`,`を使用できます。
    -   `--exclude` : 特定の種類のデータを収集しません。オプションの値は`system` 、 `monitor` 、 `log` 、 `config` 、および`db_vars`です。 2 つ以上のタイプを除外するには、タイプ間の区切り文字として`,`を使用できます。

    コマンドを実行した後、Diag はデータの収集をすぐには開始しません。代わりに、Diag は、続行するかどうかを確認するために、出力で推定データ サイズとターゲット データstorageパスを提供します。例えば：

    ```bash
    Estimated size of data to collect:
    Host               Size       Target
    ----               ----       ------
    172.16.7.129:9090  43.57 MB   1775 metrics, compressed
    172.16.7.87        0 B        /tidb-deploy/tidb-4000/log/tidb_stderr.log
    ... ...
    172.16.7.179       325 B      /tidb-deploy/tikv-20160/conf/tikv.toml
    Total              2.01 GB    (inaccurate)
    These data will be stored in /home/user/diag-fNTnz5MGhr6
    Do you want to continue? [y/N]: (default=N)
    ```

2.  データの収集を開始することを確認するには、 `Y`を入力します。

    データの収集にはある程度の時間がかかります。収集するデータの量によって時間は異なります。たとえば、テスト環境では、1 GB のデータを収集するのに約 10 分かかります。

    収集が完了すると、Diag は収集されたデータが配置されるフォルダー パスを提供します。例えば：

    ```bash
    Collected data are stored in /home/user/diag-fNTnz5MGhr6
    ```

### ステップ 3. データをローカルでビュー(オプション) {#step-3-view-data-locally-optional}

収集されたデータは、データ ソースに基づいて個別のサブディレクトリに保存されます。これらのサブディレクトリには、マシン名とポート番号に基づいて名前が付けられます。各ノードの構成、ログ、およびその他のファイルのstorage場所は、TiDB クラスターの実サーバー内の相対storageパスと同じです。

-   システムとハードウェアの基本情報: in `insight.json`
-   システム`/etc/security/limits.conf` : `limits.conf`の内容
-   カーネルパラメータのリスト: in `sysctl.conf`
-   カーネルログ: `dmesg.log`
-   データ収集中のネットワーク接続: `ss.txt`
-   コンフィグレーションデータ: 各ノードの`config.json`ディレクトリ内
-   クラスタ自身のメタ情報: in `meta.yaml` (このファイルは収集されたデータを格納するディレクトリの最上位にあります)
-   モニタリングデータ: `/monitor`ファイルディレクトリ内。監視データはデフォルトで圧縮されているため、直接表示することはできません。監視データを含む JSON ファイルを直接表示するには、データ収集時に`--compress-metrics=false`パラメータで圧縮を無効にします。

### ステップ 4. データをアップロードする {#step-4-upload-data}

クラスター診断データを PingCAP テクニカル サポート スタッフに提供するには、まずデータをクリニック サーバーにアップロードし、次に取得したデータ アクセス リンクをスタッフに送信する必要があります。 Clinic Server は、診断データを安全に保存および共有するクラウド サービスです。

クラスターのネットワーク接続に応じて、次のいずれかの方法を選択してデータをアップロードできます。

-   方法 1: クラスターが配置されているネットワークがインターネットにアクセスできる場合は、 [アップロード コマンドを使用してデータを直接アップロードする](#method-1-upload-directly)ことができます。
-   方法 2: クラスターが配置されているネットワークがインターネットにアクセスできない場合は、 [データをパックしてアップロードする](#method-2-pack-and-upload-data)を実行する必要があります。

> **注記：**
>
> データをアップロードする前に Diag でトークンまたは`region`設定しなかった場合、Diag はアップロードの失敗を報告し、トークンまたは`region`を設定するように通知します。トークンを設定するには、 [前提条件の 2 番目のステップ](#prerequisites)を参照してください。

#### 方法 1. 直接アップロードする {#method-1-upload-directly}

クラスターが配置されているネットワークがインターネットにアクセスできる場合は、次のコマンドを使用して、 [ステップ 2: データを収集する](#step-2-collect-data)で取得した収集データが含まれるフォルダーを直接アップロードできます。

```bash
tiup diag upload
```

アップロードが完了すると、出力に`Download URL`が表示されます。 `Download URL`のリンクを開いてアップロードされたデータを確認するか、以前に連絡した PingCAP テクニカル サポート スタッフにリンクを送信できます。

#### 方法 2. データをパックしてアップロードする {#method-2-pack-and-upload-data}

クラスターが配置されているネットワークがインターネットにアクセスできない場合は、イントラネット上にデータをパックし、インターネットにアクセスできるデバイスを使用してデータ パッケージをクリニック サーバーにアップロードする必要があります。詳細な操作は次のとおりです。

1.  次のコマンドを実行して、 [ステップ 2. データを収集する](#step-2-collect-data)で取得した収集データをパックします。

    ```bash
    tiup diag package ${filepath}
    ```

    パッケージ化中に、Diag はデータの暗号化と圧縮を同時に行います。テスト環境では、800 MB のデータが 57 MB に圧縮されました。以下は出力例です。

    ```bash
    Starting component `diag`: /root/.tiup/components/diag/v0.7.0/diag package diag-fNTnz5MGhr6
    packaged data set saved to /home/user/diag-fNTnz5MGhr6.diag
    ```

    パッケージ化が完了すると、データは`.diag`形式にパッケージ化されます。 `.diag`ファイルは、クリニック サーバーにアップロードされた後でのみ復号化して表示できます。収集したデータをクリニックサーバーにアップロードせずに直接転送したい場合は、独自の方法でデータを圧縮して転送することができます。

2.  インターネットにアクセスできるマシンから、圧縮データ パッケージをアップロードします。

    ```bash
    tiup diag upload ${filepath}
    ```

    以下は出力例です。

    ```bash
    [root@Copy-of-VM-EE-CentOS76-v1 user]# tiup diag upload /home/user/diag-fNTnz5MGhr6
    Starting component `diag`: /root/.tiup/components/diag/v0.7.0/diag upload /home/user/diag-fNTnz5MGhr6
    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>><>>>>>>>>>
    Completed!
    Download URL: "https://clinic.pingcap.com.cn/portal/#/orgs/4/clusters/XXXX"
    ```

3.  アップロードが完了したら、 `Download URL`のリンクを開いてアップロードされたデータを確認するか、以前に連絡した PingCAP テクニカル サポート スタッフにリンクを送信できます。

## クラスターのステータスをローカルで簡単にチェックする {#perform-a-quick-check-on-the-cluster-status-locally}

Diag を使用すると、クラスターのステータスをローカルで簡単に確認できます。現時点ではクラスターが安定して実行されている場合でも、潜在的な安定性リスクを検出するためにクラスターを定期的にチェックする必要があります。 PingCAPクリニックが提供するローカル クイック チェック機能を使用して、クラスターの潜在的な健康リスクを特定できます。ローカル チェックは構成のみをチェックします。メトリクスやログなど、より多くの項目を確認するには、診断データをクリニック サーバーにアップロードし、ヘルス レポート機能を使用することをお勧めします。

1.  構成データを収集します。

    ```bash
    tiup diag collect ${cluster-name} --include="config"
    ```

    設定ファイルのデータは比較的小さいです。収集後、収集されたデータはデフォルトで現在のパスに保存されます。テスト環境では、18 ノードのクラスターの場合、構成ファイルのデータ サイズは 10 KB 未満です。

2.  構成データを診断します。

    ```bash
    tiup diag check ${subdir-in-output-data}
    ```

    上記コマンドの`${subdir-in-output-data}`は採取したデータを格納するパスで、このパスに`meta.yaml`ファイルがあります。

3.  診断結果をビュー。

    診断結果はコマンド ラインで返されます。例えば：

    ```bash
    Starting component `diag`: /root/.tiup/components/diag/v0.7.0/diag check diag-fNTnz5MGhr6

    # Diagnostic result
    lili 2022-01-24T09:33:57+08:00

    ## 1. Cluster basic information
    - Cluster ID: 7047403704292855808
    - Cluster Name: lili
    - Cluster Version: v5.3.0

    ## 2. Sampling information
    - Sample ID: fNTnz5MGhr6
    - Sampling Date: 2022-01-24T09:33:57+08:00
    - Sample Content:: [system monitor log config]

    ## 3. Diagnostic result, including potential configuration problems
    In this inspection, 22 rules were executed.

    The results of **1** rules were abnormal and needed to be further discussed with support team.

    The following is the details of the abnormalities.

    ### Diagnostic result summary
    The configuration rules are all derived from PingCAP’s OnCall Service.

    If the results of the configuration rules are found to be abnormal, they may cause the cluster to fail.

    There were **1** abnormal results.

    #### Path to save the diagnostic result file

    Rule Name: tidb-max-days
    - RuleID: 100
    - Variation: TidbConfig.log.file.max-days
    - For more information, please visit: https://s.tidb.io/msmo6awg
    - Check Result:
      TidbConfig_172.16.7.87:4000   TidbConfig.log.file.max-days:0   warning
      TidbConfig_172.16.7.86:4000   TidbConfig.log.file.max-days:0   warning
      TidbConfig_172.16.7.179:4000   TidbConfig.log.file.max-days:0   warning

    Result report and record are saved at diag-fNTnz5MGhr6/report-220125153215
    ```

    診断結果の最後のセクション (上記の出力例の`#### Path to save the diagnostic result file`の下) では、検出された構成の潜在的なリスクごとに、Diag は詳細な構成提案を含む対応するナレッジ ベースのリンクを提供します。上の例では、関連するリンクは`https://s.tidb.io/msmo6awg`です。

## FAQ {#faq}

1.  データのアップロードに失敗した場合、再アップロードできますか?

    はい。データのアップロードはブレークポイントのアップロードをサポートしています。アップロードが失敗した場合は、直接再度アップロードできます。

2.  データをアップロードした後、返されたデータ アクセス リンクを開くことができません。どうすればいいですか？

    まずクリニックサーバーにログインします。ログインに成功した後もリンクを開けない場合は、データにアクセスできるかどうかを確認してください。そうでない場合は、データ所有者に連絡して許可を求めてください。許可を取得したら、Clinic Server にログインし、再度リンクを開きます。

3.  アップロードされたデータはクリニックサーバーにどのくらいの期間保存されますか?

    最長は 180 日です。 Clinic Server ページにアップロードしたデータはいつでも削除できます。
