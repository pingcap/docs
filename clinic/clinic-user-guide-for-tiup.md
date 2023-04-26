---
title: Troubleshoot Clusters Using PingCAP Clinic
summary: Learn how to use the PingCAP Clinic Diagnostic Service to troubleshoot cluster problems remotely and perform a quick check of the cluster status on a TiDB cluster or DM cluster deployed using TiUP.
---

# PingCAPクリニックを使用したクラスターのトラブルシューティング {#troubleshoot-clusters-using-pingcap-clinic}

TiUPを使用してデプロイされた TiDB クラスターおよび DM クラスターの場合、 PingCAPクリニック Diagnostic Service (PingCAPクリニック) を使用してクラスターの問題をリモートでトラブルシューティングし、 [Diag クライアント (Diag)](https://github.com/pingcap/diag)および Clinic Server を使用してローカルでクラスターの状態をすばやく確認できます。

> **ノート：**
>
> -   このドキュメントは、オンプレミス環境でTiUP を使用してデプロイされたクラスターに**のみ**適用されます。 TiDB Operatorを使用して Kubernetes にデプロイされたクラスターについては、 [TiDB Operator環境向けのPingCAPクリニック](https://docs.pingcap.com/tidb-in-kubernetes/stable/clinic-user-guide)を参照してください。
>
> -   PingCAPクリニック は、 TiDB Ansible を使用してデプロイされたクラスターからのデータ収集を**サポートしていません**。

## ユーザー シナリオ {#user-scenarios}

-   [クラスターの問題をリモートでトラブルシューティングする](#troubleshoot-cluster-problems-remotely)

    -   クラスターに問題が発生した場合、PingCAP から[支持を得ます](/support.md)する必要がある場合は、次の操作を実行してリモート トラブルシューティングを容易にすることができます: Diag を使用して診断データを収集し、収集したデータを Clinic Server にアップロードし、データ アクセス リンクをテクニカルサポートスタッフ。
    -   クラスターに何らかの問題があり、すぐに問題を分析できない場合は、Diag を使用してデータを収集し、後で分析できるように保存できます。

-   [クラスターのステータスをローカルで簡単に確認する](#perform-a-quick-check-on-the-cluster-status-locally)

    クラスターが今のところ安定して動作している場合でも、クラスターを定期的にチェックして潜在的な安定性リスクを検出する必要があります。 PingCAPクリニックが提供するローカルのクイック チェック機能を使用して、クラスターの潜在的なヘルス リスクを特定できます。ローカル チェックは構成のみをチェックします。メトリクスやログなど、より多くの項目を確認するには、診断データを Clinic Server にアップロードし、Health Report 機能を使用することをお勧めします。

## 前提条件 {#prerequisites}

PingCAPクリニックを利用する前に、Diag（ PingCAPクリニックが提供するデータ収集用コンポーネント）をインストールし、データをアップロードするための環境を整える必要があります。

1.  インストール診断

    -   コントロール マシンにTiUPをインストールした場合は、次のコマンドを実行して Diag をインストールします。

        ```bash
        tiup install diag
        ```

    -   Diag がインストールされている場合は、次のコマンドを使用して Diag を最新バージョンにアップグレードできます。

        ```bash
        tiup update diag
        ```

    > **ノート：**
    >
    > -   インターネット接続のないクラスターの場合、Diag をオフラインでデプロイする必要があります。詳細については、 [TiUP をオフラインでデプロイ: 方法 2](/production-deployment-using-tiup.md#deploy-tiup-offline)を参照してください。
    > -   Diag は、v5.4.0 以降の TiDB サーバー オフライン ミラー パッケージで**のみ**提供されます。

2.  データをアップロードするためのアクセス トークン (トークン) を取得および設定します。

    収集したデータを Diag 経由でアップロードする場合、ユーザー認証のためのトークンが必要です。トークン Diag を既に設定している場合は、トークンを再利用して、この手順をスキップできます。

    トークンを取得するには、次の手順を実行します。

    -   クリニック サーバーにログインします。

        <SimpleTab groupId="clinicServer">
          <div label="Clinic Server for international users" value="clinic-us">

        [海外ユーザー向けクリニックサーバー](https://clinic.pingcap.com) : データは米国の AWS に保存されます。

        </div>
          <div label="Clinic Server for users in the Chinese mainland" value="clinic-cn">

        [中国本土のユーザー向けクリニックサーバー](https://clinic.pingcap.com.cn) : データは中国 (北京) リージョンの AWS に保存されます。

        </div>

        </SimpleTab>

    -   クラスタページの右下隅にあるアイコンをクリックし、 **[Get Access Token For Diag Tool]**を選択して、ポップアップ ウィンドウで<strong>[+]</strong>をクリックします。表示されたトークンをコピーして保存したことを確認してください。

        ![Get the Token](/media/clinic-get-token.png)

    > **ノート：**
    >
    > -   初めてクリニックサーバーにアクセスする場合、トークンを取得する前に、 [PingCAPクリニックのクイック スタート](/clinic/quick-start-with-clinic.md#prerequisites)を参照して環境を準備する必要があります。
    > -   データ セキュリティのため、TiDB はトークンの作成時にのみトークンを表示します。トークンを紛失した場合は、古いトークンを削除して新しいトークンを作成してください。
    > -   トークンは、データのアップロードにのみ使用されます。

    -   次に、トークンを Diag に設定します。例えば：

        ```bash
        tiup diag config clinic.token ${token-value}
        ```

3.  Diag に`region`を設定します。

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

4.  (オプション) ログのリダクションを有効にします。

    TiDB が詳細なログ情報を提供する場合、機密情報 (ユーザー データなど) をログに出力することがあります。ローカル ログと Clinic Server で機密情報が漏洩するのを避けたい場合は、TiDB 側でログの編集を有効にすることができます。詳細については、 [ログ編集](/log-redaction.md#log-redaction-in-tidb-side)を参照してください。

## クラスターの問題をリモートでトラブルシューティングする {#troubleshoot-cluster-problems-remotely}

Diag を使用すると、監視データや構成情報など、TiDB クラスターおよび DM クラスターから診断データをすばやく収集できます。

### Step 1. 収集するデータを確認する {#step-1-check-the-data-to-be-collected}

Diag で収集できるデータの完全なリストについては、 [PingCAPクリニックの診断データ](/clinic/clinic-data-instruction-for-tiup.md)を参照してください。

その後の診断の効率を向上させるために、監視データや構成情報を含む完全な診断データを収集することをお勧めします。詳細については、 [クラスターからデータを収集する](#step-2-collect-data)を参照してください。

### ステップ 2. データを収集する {#step-2-collect-data}

Diag を使用すると、 TiUPを使用してデプロイされた TiDB クラスターおよび DM クラスターからデータを収集できます。

1.  Diagのデータ収集コマンドを実行します。

    たとえば、現在の時刻に基づいて 4 時間前から 2 時間前までの診断データを収集するには、次のコマンドを実行します。

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

    データ収集のパラメーターの説明:

    -   `-f/--from` : データ収集の開始時刻を指定します。このパラメーターを指定しない場合、デフォルトの開始時刻は現在時刻の 2 時間前になります。タイム ゾーンを変更するには、 `-f="12:30 +0800"`構文を使用します。 `+0800`など、このパラメーターでタイム ゾーン情報を指定しない場合、タイム ゾーンは既定で UTC になります。
    -   `-t/--to` : データ収集の終了時刻を指定します。このパラメーターを指定しない場合、デフォルトの終了時間は現時点です。タイム ゾーンを変更するには、 `-f="12:30 +0800"`構文を使用します。 `+0800`など、このパラメーターでタイム ゾーン情報を指定しない場合、タイム ゾーンは既定で UTC になります。

    パラメータの使用に関するヒント:

    データ収集時間の指定に加えて、Diag を使用してさらにパラメーターを指定できます。すべてのパラメーターを取得するには、 `tiup diag collect -h`または`tiup diag collectdm -h`コマンドを実行します。

    > **ノート：**
    >
    > -   デフォルトでは、diag はシステム変数データ (db_vars) を収集しません。このデータを収集するには、データベースにアクセスできるユーザー名とパスワードを追加で提供する必要があります。このデータベースでは、システム変数への読み取りアクセスを有効にする必要があることに注意してください。
    > -   デフォルトでは、diag はパフォーマンス データ ( `perf` ) とデバッグ データ ( `debug` ) を収集しません。
    > -   システム変数を含む完全な診断データを収集するには、コマンド`tiup diag collect <cluster-name> --include="system,monitor,log,config,db_vars,perf,debug"`を使用します。

    -   `-l` : ファイル転送の帯域幅制限。単位は Kbit/s で、デフォルト値は`100000` (scp の`-l`パラメータ) です。
    -   `-N/--node` : 指定したノードからのみデータを収集します。形式は`ip:port`です。
    -   `--include` : 特定のタイプのデータのみを収集します。オプションの値は`system` 、 `monitor` 、 `log` 、 `config` 、および`db_vars`です。 2 つ以上のタイプを含めるには、タイプ間のセパレータとして`,`を使用できます。
    -   `--exclude` : 特定の種類のデータを収集しません。オプションの値は`system` 、 `monitor` 、 `log` 、 `config` 、および`db_vars`です。 2 つ以上のタイプを除外するには、タイプ間のセパレーターとして`,`を使用できます。

    コマンドを実行した後、Diag はデータの収集をすぐには開始しません。代わりに、Diag は推定データ サイズとターゲット データstorageパスを出力で提供し、続行するかどうかを確認します。例えば：

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

2.  `Y`を入力して、データの収集を開始することを確認します。

    データの収集には一定の時間がかかります。時間は、収集するデータ量によって異なります。たとえば、テスト環境では、1 GB のデータを収集するのに約 10 分かかります。

    収集が完了すると、Diag は、収集されたデータが配置されているフォルダー パスを提供します。例えば：

    ```bash
    Collected data are stored in /home/user/diag-fNTnz5MGhr6
    ```

### ステップ 3. ローカルでデータをビュー(オプション) {#step-3-view-data-locally-optional}

収集されたデータは、データ ソースに基づいて個別のサブディレクトリに保存されます。これらのサブディレクトリの名前は、マシン名とポート番号に基づいています。各ノードの構成、ログ、およびその他のファイルのstorage場所は、TiDB クラスターの実サーバー内の相対的なstorageパスと同じです。

-   システムとハードウェアの基本情報: `insight.json`
-   システム内コンテンツ`/etc/security/limits.conf` : in `limits.conf`
-   カーネルパラメータのリスト: `sysctl.conf`
-   カーネルログ: `dmesg.log`
-   データ収集中のネットワーク接続: `ss.txt`
-   コンフィグレーションデータ: 各ノードの`config.json`のディレクトリー内
-   クラスタ自体のメタ情報: `meta.yaml` (このファイルは、収集されたデータを格納するディレクトリの最上位にあります)
-   監視データ: `/monitor`ファイル ディレクトリ内。監視データはデフォルトで圧縮されており、直接表示することはできません。モニタリング データを含む JSON ファイルを直接表示するには、データ収集時に`--compress-metrics=false`パラメータで圧縮を無効にします。

### ステップ 4. データをアップロードする {#step-4-upload-data}

クラスタ診断データを PingCAP テクニカル サポート スタッフに提供するには、まずデータを Clinic Server にアップロードしてから、取得したデータ アクセス リンクをスタッフに送信する必要があります。 Clinic Server は、診断データを安全に保存および共有するクラウド サービスです。

クラスターのネットワーク接続に応じて、次のいずれかの方法を選択してデータをアップロードできます。

-   方法 1: クラスターが配置されているネットワークがインターネットにアクセスできる場合は、 [アップロード コマンドを使用してデータを直接アップロードする](#method-1-upload-directly)ことができます。
-   方法 2: クラスターが配置されているネットワークがインターネットにアクセスできない場合は、 [データをパックしてアップロードする](#method-2-pack-and-upload-data)を行う必要があります。

> **ノート：**
>
> データをアップロードする前に Diag でトークンまたは`region`設定しなかった場合、Diag はアップロードの失敗を報告し、トークンまたは`region`を設定するよう通知します。トークンを設定するには、 [前提条件の 2 番目のステップ](#prerequisites)を参照してください。

#### 方法 1. 直接アップロードする {#method-1-upload-directly}

クラスターが配置されているネットワークがインターネットにアクセスできる場合は、次のコマンドを使用して、 [ステップ 2: データを収集する](#step-2-collect-data)で取得した収集データを含むフォルダーを直接アップロードできます。

{{< copyable "" >}}

```bash
tiup diag upload
```

アップロードが完了すると、出力に`Download URL`が表示されます。 `Download URL`のリンクを開いてアップロードされたデータを表示するか、以前に連絡した PingCAP テクニカル サポート スタッフにリンクを送信できます。

#### 方法 2. データをパックしてアップロードする {#method-2-pack-and-upload-data}

クラスターが配置されているネットワークがインターネットにアクセスできない場合は、イントラネットにデータをパックし、インターネットにアクセスできるデバイスを使用してデータ パッケージを Clinic Server にアップロードする必要があります。詳細な操作は次のとおりです。

1.  次のコマンドを実行して、 [ステップ 2. データを収集する](#step-2-collect-data)で取得した収集データをパックします。

    ```bash
    tiup diag package ${filepath}
    ```

    パッケージ化中に、Diag はデータの暗号化と圧縮を同時に行います。テスト環境では、800 MB のデータが 57 MB に圧縮されました。次に出力例を示します。

    ```bash
    Starting component `diag`: /root/.tiup/components/diag/v0.7.0/diag package diag-fNTnz5MGhr6
    packaged data set saved to /home/user/diag-fNTnz5MGhr6.diag
    ```

    パッケージ化が完了すると、データは`.diag`形式にパッケージ化されます。 `.diag`ファイルは、クリニック サーバーにアップロードされた後にのみ復号化して表示できます。収集したデータをクリニックサーバーにアップロードせずに直接転送したい場合は、独自の方法でデータを圧縮して転送することができます。

2.  インターネットにアクセスできるマシンから、圧縮データ パッケージをアップロードします。

    ```bash
    tiup diag upload ${filepath}
    ```

    次に出力例を示します。

    ```bash
    [root@Copy-of-VM-EE-CentOS76-v1 user]# tiup diag upload /home/user/diag-fNTnz5MGhr6
    Starting component `diag`: /root/.tiup/components/diag/v0.7.0/diag upload /home/user/diag-fNTnz5MGhr6
    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>><>>>>>>>>>
    Completed!
    Download URL: "https://clinic.pingcap.com.cn/portal/#/orgs/4/clusters/XXXX"
    ```

3.  アップロードが完了したら、 `Download URL`のリンクを開いてアップロードされたデータを表示したり、以前連絡した PingCAP テクニカル サポート スタッフにリンクを送信したりできます。

## クラスターのステータスをローカルで簡単に確認する {#perform-a-quick-check-on-the-cluster-status-locally}

Diag を使用して、クラスターの状態をローカルで簡単に確認できます。クラスターが今のところ安定して動作している場合でも、クラスターを定期的にチェックして潜在的な安定性リスクを検出する必要があります。 PingCAPクリニックが提供するローカルのクイック チェック機能を使用して、クラスターの潜在的なヘルス リスクを特定できます。ローカル チェックは構成のみをチェックします。メトリクスやログなど、より多くの項目を確認するには、診断データを Clinic Server にアップロードし、Health Report 機能を使用することをお勧めします。

1.  構成データを収集します。

    ```bash
    tiup diag collect ${cluster-name} --include="config"
    ```

    構成ファイルのデータは比較的小さいです。収集後、収集されたデータはデフォルトで現在のパスに保存されます。テスト環境では、18 ノードのクラスターの場合、構成ファイルのデータ サイズは 10 KB 未満です。

2.  構成データを診断します。

    ```bash
    tiup diag check ${subdir-in-output-data}
    ```

    上記のコマンドの`${subdir-in-output-data}`は、収集されたデータを格納するパスであり、このパスには`meta.yaml`ファイルがあります。

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

    診断結果の最後のセクション (上記の出力例の`#### Path to save the diagnostic result file`の下) で、見つかった構成の潜在的なリスクごとに、Diag は対応するナレッジ ベース リンクと詳細な構成の提案を提供します。上記の例では、関連するリンクは`https://s.tidb.io/msmo6awg`です。

## FAQ {#faq}

1.  データのアップロードに失敗した場合、再アップロードできますか?

    はい。データのアップロードは、ブレークポイントのアップロードをサポートしています。アップロードに失敗した場合は、直接アップロードし直すことができます。

2.  データをアップロードした後、返されたデータ アクセス リンクを開くことができません。私は何をすべきか？

    最初に Clinic Server にログインします。ログインに成功してもリンクを開けない場合は、データにアクセスできるかどうかを確認してください。そうでない場合は、データ所有者に連絡して許可を求めてください。権限を取得したら、Clinic Server にログインし、リンクを再度開きます。

3.  アップロードされたデータはどのくらいの間 Clinic Server に保持されますか?

    最長は180日です。 Clinic Server ページにアップロードしたデータはいつでも削除できます。
