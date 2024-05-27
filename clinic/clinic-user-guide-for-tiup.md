---
title: Troubleshoot Clusters Using PingCAP Clinic
summary: PingCAPクリニック診断サービス (PingCAPクリニック) は、 TiUPを使用して展開された TiDB および DM クラスターのトラブルシューティングに役立ちます。Diag クライアントと Clinic Server を使用して、リモート トラブルシューティングとローカル クラスターの状態チェックを実行できます。前提条件には、Diag のインストール、アクセス トークンの設定、およびリージョンの構成が含まれます。リモートでのトラブルシューティングには、診断データの収集、表示、およびアップロードが含まれます。ローカルでのクラスターの状態のクイック チェックには、構成データの収集と診断が含まれます。データ アップロードではブレークポイント アップロードがサポートされ、アップロードされたデータは Clinic Server に最大 180 日間保持されます。
---

# PingCAPクリニックを使用してクラスターをトラブルシューティングする {#troubleshoot-clusters-using-pingcap-clinic}

TiUPを使用してデプロイされた TiDB クラスターおよび DM クラスターの場合、 PingCAPクリニック診断サービス (PingCAPクリニック) を使用してクラスターの問題をリモートでトラブルシューティングし、 [診断クライアント (Diag)](https://github.com/pingcap/diag)および Clinic Server を使用してローカルでクラスターの状態をすばやくチェックできます。

> **注記：**
>
> -   このドキュメントは、セルフホスト環境でTiUPを使用してデプロイされたクラスターに**のみ**適用されます。Kubernetes 上のTiDB Operatorを使用してデプロイされたクラスターについては、 [TiDB Operator環境向けPingCAPクリニック](https://docs.pingcap.com/tidb-in-kubernetes/stable/clinic-user-guide)を参照してください。
>
> -   PingCAPクリニック は、 TiDB Ansible を使用してデプロイされたクラスターからのデータ収集を**サポートしていません**。

## ユーザーシナリオ {#user-scenarios}

-   [クラスターの問題をリモートでトラブルシューティングする](#troubleshoot-cluster-problems-remotely)

    -   クラスターに問題があり、PingCAP から[支持を得ます](/support.md)を取得する必要がある場合は、Diag を使用して診断データを収集し、収集したデータを Clinic Server にアップロードし、データ アクセス リンクをテクニカル サポート スタッフに提供するという操作を実行して、リモート トラブルシューティングを容易にすることができます。
    -   クラスターに何らかの問題があり、すぐに問題を分析できない場合は、Diag を使用してデータを収集し、後で分析できるように保存できます。

-   [ローカルでクラスターのステータスを素早くチェックする](#perform-a-quick-check-on-the-cluster-status-locally)

    現時点ではクラスターが安定して動作している場合でも、潜在的な安定性リスクを検出するために、クラスターを定期的にチェックする必要があります。PingCAP PingCAPクリニックが提供するローカル クイック チェック機能を使用して、クラスターの潜在的なヘルス リスクを特定できます。ローカル チェックでは構成のみがチェックされます。メトリックやログなどのより多くの項目をチェックするには、診断データを Clinic Server にアップロードし、ヘルス レポート機能を使用することをお勧めします。

## 前提条件 {#prerequisites}

PingCAPクリニックを使用する前に、 Diag ( PingCAPクリニックが提供するデータ収集コンポーネント) をインストールし、データをアップロードする環境を準備する必要があります。

1.  Diagをインストールします。

    -   制御マシンにTiUP がインストールされている場合は、次のコマンドを実行して Diag をインストールします。

        ```bash
        tiup install diag
        ```

    -   Diag をインストールしている場合は、次のコマンドを使用して Diag を最新バージョンにアップグレードできます。

        ```bash
        tiup update diag
        ```

    > **注記：**
    >
    > -   インターネットに接続されていないクラスターの場合は、Diag をオフラインで展開する必要があります。詳細については、 [TiUP をオフラインでデプロイ: 方法 2](/production-deployment-using-tiup.md#deploy-tiup-offline)を参照してください。
    > -   Diag は、TiDB Server オフライン ミラー パッケージ v5.4.0 以降で**のみ**提供されます。

2.  データをアップロードするためのアクセストークン（トークン）を取得して設定します。

    Diag を通じて収集したデータをアップロードする場合、ユーザー認証用のトークンが必要です。すでにトークン Diag を設定している場合は、そのトークンを再利用してこの手順をスキップできます。

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

    -   クラスタページの右下隅にあるアイコンをクリックし、**診断ツールのアクセス トークンの取得を**選択して、ポップアップ ウィンドウで**+**をクリックします。表示されるトークンをコピーして保存したことを確認します。

        ![Get the Token](/media/clinic-get-token.png)

    > **注記：**
    >
    > -   Clinic Serverに初めてアクセスする場合は、トークンを取得する前に、 [PingCAPクリニックのクイックスタート](/clinic/quick-start-with-clinic.md#prerequisites)を参考に環境を準備する必要があります。
    > -   データ セキュリティのため、TiDB はトークンの作成時にのみトークンを表示します。トークンを紛失した場合は、古いトークンを削除して新しいトークンを作成してください。
    > -   トークンはデータのアップロードにのみ使用されます。

    -   次に、Diag でトークンを設定します。例:

        ```bash
        tiup diag config clinic.token ${token-value}
        ```

3.  Diag に`region`設定します。

    `region` 、データをアップロードするときにデータのパック化に使用される暗号化証明書とターゲット サービスを決定します。例:

    > **注記：**
    >
    > -   Diag v0.9.0 以降のバージョンでは設定`region`サポートされます。
    > -   Diag v0.9.0 より前のバージョンの場合、データはデフォルトで中国地域の Clinic Server にアップロードされます。これらのバージョンで`region`を設定するには、 `tiup update diag`コマンドを実行して Diag を最新バージョンにアップグレードしてから、Diag で`region`を設定します。

    <SimpleTab groupId="clinicServer">
     <div label="Clinic Server for international users" value="clinic-us">

    海外ユーザー向けに Clinic Server を使用する場合は、次のコマンドを使用して`region`から`US`に設定します。

    ```bash
    tiup diag config clinic.region US
    ```

    </div>
     <div label="Clinic Server for users in the Chinese mainland" value="clinic-cn">

    中国本土のユーザー向けに Clinic Server を使用する場合は、次のコマンドを使用して`region`から`CN`に設定します。

    ```bash
    tiup diag config clinic.region CN
    ```

    </div>

    </SimpleTab>

4.  (オプション) ログ編集を有効にします。

    TiDB が詳細なログ情報を提供する場合、ログに機密情報 (ユーザーデータなど) が出力されることがあります。ローカル ログと Clinic Server に機密情報が漏洩するのを防ぐには、TiDB 側でログ編集を有効にします。詳細については、 [ログ編集](/log-redaction.md#log-redaction-in-tidb-side)参照してください。

## クラスターの問題をリモートでトラブルシューティングする {#troubleshoot-cluster-problems-remotely}

Diag を使用すると、監視データや構成情報などの診断データを TiDB クラスターおよび DM クラスターから迅速に収集できます。

### ステップ1. 収集するデータを確認する {#step-1-check-the-data-to-be-collected}

Diag で収集できるデータの完全なリストについては、 [PingCAPクリニック診断データ](/clinic/clinic-data-instruction-for-tiup.md)参照してください。

後の診断の効率を高めるために、監視データや構成情報を含む完全な診断データを収集することをお勧めします。詳細については、 [クラスターからデータを収集する](#step-2-collect-data)を参照してください。

### ステップ2. データを収集する {#step-2-collect-data}

Diag を使用すると、 TiUPを使用してデプロイされた TiDB クラスターと DM クラスターからデータを収集できます。

1.  Diag のデータ収集コマンドを実行します。

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

    データ収集のパラメータの説明:

    -   `-f/--from` : データ収集の開始時刻を指定します。このパラメータを指定しない場合、デフォルトの開始時刻は現在の時刻の 2 時間前になります。タイム ゾーンを変更するには、 `-f="12:30 +0800"`構文を使用します。このパラメータでタイム ゾーン情報を指定しない場合 ( `+0800`など)、タイム ゾーンはデフォルトで UTC になります。
    -   `-t/--to` : データ収集の終了時刻を指定します。このパラメータを指定しない場合、デフォルトの終了時刻は現在時刻になります。タイムゾーンを変更するには、 `-f="12:30 +0800"`構文を使用します。このパラメータでタイムゾーン情報を指定しない場合 ( `+0800`など)、タイムゾーンはデフォルトで UTC になります。

    パラメータの使用に関するヒント:

    データ収集時間を指定することに加えて、Diag を使用してさらに多くのパラメータを指定できます。すべてのパラメータを取得するには、 `tiup diag collect -h`または`tiup diag collectdm -h`コマンドを実行します。

    > **注記：**
    >
    > -   Diag は、デフォルトではシステム変数データ (db_vars) を収集しません。このデータを収集するには、データベースにアクセスできるユーザー名とパスワードを追加で提供する必要があります。このデータベースでは、システム変数への読み取りアクセスが有効になっている必要があることに注意してください。
    > -   Diagはデフォルトではパフォーマンスデータ（ `perf` ）とデバッグデータ（ `debug` ）を収集しません。
    > -   システム変数を含む完全な診断データを収集するには、コマンド`tiup diag collect <cluster-name> --include="system,monitor,log,config,db_vars,perf,debug"`を使用します。

    -   `-l` : ファイル転送の帯域幅制限。単位は Kbit/s、デフォルト値は`100000` (scp の`-l`のパラメータ) です。
    -   `-N/--node` : 指定されたノードからのみデータを収集します。形式は`ip:port`です。
    -   `--include` : 特定の種類のデータのみを収集します。オプションの値は`system` 、 `monitor` 、 `log` 、 `config` 、および`db_vars`です。2 つ以上の種類を含めるには、種類間の区切りとして`,`を使用できます。
    -   `--exclude` : 特定の種類のデータは収集しません。オプションの値は`system` 、 `monitor` 、 `log` 、 `config` 、および`db_vars`です。2 つ以上の種類を除外するには、種類間の区切りとして`,`を使用できます。

    コマンドを実行しても、Diag はすぐにデータの収集を開始しません。代わりに、Diag は推定データ サイズとターゲット データstorageパスを出力に表示し、続行するかどうかを確認します。例:

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

2.  データの収集を開始することを確認するには、 `Y`入力します。

    データの収集には一定の時間がかかります。収集するデータの量に応じて時間は異なります。たとえば、テスト環境では 1 GB のデータの収集に約 10 分かかります。

    収集が完了すると、Diag は収集されたデータが保存されているフォルダー パスを提供します。例:

    ```bash
    Collected data are stored in /home/user/diag-fNTnz5MGhr6
    ```

### ステップ 3. データをローカルでビュー(オプション) {#step-3-view-data-locally-optional}

収集されたデータは、データ ソースに基づいて個別のサブディレクトリに保存されます。これらのサブディレクトリの名前は、マシン名とポート番号に基づいて付けられます。各ノードの構成、ログ、およびその他のファイルのstorage場所は、TiDB クラスターの実サーバー内の相対的なstorageパスと同じです。

-   システムとハードウェアの基本情報： `insight.json`
-   システム内のコンテンツ`/etc/security/limits.conf` : `limits.conf`
-   カーネルパラメータのリスト: `sysctl.conf`
-   カーネルログ: `dmesg.log`
-   データ収集中のネットワーク接続: `ss.txt`
-   コンフィグレーションデータ: 各ノードの`config.json`ディレクトリ内
-   クラスター自体のメタ情報: in `meta.yaml` (このファイルは収集されたデータを保存するディレクトリの最上位にあります)
-   監視データ: `/monitor`ファイル ディレクトリ内。監視データはデフォルトで圧縮されており、直接表示できません。監視データを含む JSON ファイルを直接表示するには、データ収集時に`--compress-metrics=false`パラメータを使用して圧縮を無効にします。

### ステップ4. データをアップロードする {#step-4-upload-data}

PingCAP テクニカル サポート スタッフにクラスター診断データを提供するには、まずデータを Clinic Server にアップロードし、取得したデータ アクセス リンクをスタッフに送信する必要があります。Clinic Server は、診断データを安全に保存して共有するクラウド サービスです。

クラスターのネットワーク接続に応じて、次のいずれかの方法を選択してデータをアップロードできます。

-   方法 1: クラスターが配置されているネットワークがインターネットにアクセスできる場合は、 [アップロードコマンドを使用してデータを直接アップロードする](#method-1-upload-directly)実行できます。
-   方法 2: クラスターが配置されているネットワークがインターネットにアクセスできない場合は、 [データをパックしてアップロードする](#method-2-pack-and-upload-data)実行する必要があります。

> **注記：**
>
> データをアップロードする前に Diag でトークンまたは`region`設定していない場合、 Diag はアップロードの失敗を報告し、トークンまたは`region`設定するように通知します。トークンを設定するには、 [前提条件の2番目のステップ](#prerequisites)参照してください。

#### 方法1. 直接アップロードする {#method-1-upload-directly}

クラスターが配置されているネットワークがインターネットにアクセスできる場合は、次のコマンドを使用して、 [ステップ2: データを収集する](#step-2-collect-data)で取得した収集データを含むフォルダーを直接アップロードできます。

```bash
tiup diag upload
```

アップロードが完了すると、出力に`Download URL`表示されます。3 `Download URL`リンクを開いてアップロードされたデータを確認するか、以前に連絡した PingCAP テクニカル サポート スタッフにリンクを送信することができます。

#### 方法2. データをパックしてアップロードする {#method-2-pack-and-upload-data}

クラスターが配置されているネットワークがインターネットにアクセスできない場合は、イントラネット上でデータをパックし、インターネットにアクセスできるデバイスを使用してデータ パッケージを Clinic Server にアップロードする必要があります。詳細な操作は次のとおりです。

1.  以下のコマンドを実行して、 [ステップ2. データを収集する](#step-2-collect-data)で取得した収集データをパックします。

    ```bash
    tiup diag package ${filepath}
    ```

    パッケージ化中に、Diag はデータの暗号化と圧縮を同時に行います。テスト環境では、800 MB のデータが 57 MB に圧縮されました。出力例を次に示します。

    ```bash
    Starting component `diag`: /root/.tiup/components/diag/v0.7.0/diag package diag-fNTnz5MGhr6
    packaged data set saved to /home/user/diag-fNTnz5MGhr6.diag
    ```

    パッケージングが完了すると、データは`.diag`形式にパッケージ化されます。 `.diag`ファイルは、クリニックサーバーにアップロードされた後にのみ復号化して表示できます。 収集したデータをクリニックサーバーにアップロードせずに直接転送する場合は、独自の方法でデータを圧縮して転送できます。

2.  インターネットにアクセスできるマシンから、圧縮されたデータ パッケージをアップロードします。

    ```bash
    tiup diag upload ${filepath}
    ```

    出力例は次のとおりです。

    ```bash
    [root@Copy-of-VM-EE-CentOS76-v1 user]# tiup diag upload /home/user/diag-fNTnz5MGhr6
    Starting component `diag`: /root/.tiup/components/diag/v0.7.0/diag upload /home/user/diag-fNTnz5MGhr6
    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>><>>>>>>>>>
    Completed!
    Download URL: "https://clinic.pingcap.com.cn/portal/#/orgs/4/clusters/XXXX"
    ```

3.  アップロードが完了したら、 `Download URL`のリンクを開いてアップロードされたデータを確認するか、以前に連絡した PingCAP テクニカル サポート スタッフにリンクを送信することができます。

## ローカルでクラスターのステータスを素早くチェックする {#perform-a-quick-check-on-the-cluster-status-locally}

Diag を使用すると、ローカルでクラスターの状態をすばやく確認できます。クラスターが今のところ安定して動作している場合でも、潜在的な安定性リスクを検出するために、クラスターを定期的にチェックする必要があります。PingCAP PingCAPクリニックが提供するローカル クイック チェック機能を使用すると、クラスターの潜在的なヘルス リスクを特定できます。ローカル チェックでは構成のみがチェックされます。メトリックやログなどのより多くの項目をチェックするには、診断データを Clinic Server にアップロードし、ヘルス レポート機能を使用することをお勧めします。

1.  構成データを収集します。

    ```bash
    tiup diag collect ${cluster-name} --include="config"
    ```

    設定ファイルのデータは比較的小さいです。収集後、収集されたデータはデフォルトで現在のパスに保存されます。テスト環境では、18 ノードのクラスターの場合、設定ファイルのデータ サイズは 10 KB 未満です。

2.  構成データを診断します:

    ```bash
    tiup diag check ${subdir-in-output-data}
    ```

    上記コマンドの`${subdir-in-output-data}`収集したデータを保存するパスであり、このパスには`meta.yaml`ファイルがあります。

3.  診断結果をビュー:

    診断結果はコマンド ラインで返されます。例:

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

    診断結果の最後のセクション (上記の出力例の`#### Path to save the diagnostic result file`の下) では、検出された構成の潜在的なリスクごとに、詳細な構成の提案を含む対応するナレッジ ベース リンクが Diag によって提供されます。上記の例では、関連するリンクは`https://s.tidb.io/msmo6awg`です。

## FAQ {#faq}

1.  データのアップロードに失敗した場合、再アップロードできますか?

    はい。データのアップロードはブレークポイントアップロードをサポートしています。アップロードが失敗した場合は、直接再度アップロードできます。

2.  データをアップロードした後、返されたデータ アクセス リンクを開くことができません。どうすればよいでしょうか?

    まずクリニック サーバーにログインしてください。ログインに成功してもリンクを開けない場合は、データにアクセスできるかどうかを確認してください。アクセスできない場合は、データ所有者に連絡して許可を得てください。許可を得たら、クリニック サーバーにログインしてリンクを再度開いてください。

3.  アップロードされたデータはクリニックサーバーにどのくらいの期間保存されますか?

    最長180日間です。クリニックサーバーページでアップロードしたデータはいつでも削除できます。
