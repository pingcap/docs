---
title: Troubleshoot Clusters Using PingCAP Clinic
summary: PingCAPクリニック診断サービス (PingCAPクリニック) は、 TiUPを使用して導入された TiDB および DM クラスターのトラブルシューティングに役立ちます。Diag クライアントと Clinic Server を使用して、リモート トラブルシューティングとローカル クラスターの状態確認が可能です。前提条件として、Diag のインストール、アクセス トークンの設定、リージョンの構成が必要です。リモートでのトラブルシューティングには、診断データの収集、表示、アップロードが含まれます。ローカルでのクラスター状態のクイック チェックには、構成データの収集と診断が含まれます。データのアップロードはブレークポイント アップロードをサポートしており、アップロードされたデータは Clinic Server に最大 180 日間保存されます。
---

# PingCAPクリニックを使用したクラスターのトラブルシューティング {#troubleshoot-clusters-using-pingcap-clinic}

TiUPを使用して導入された TiDB クラスターおよび DM クラスターの場合、 PingCAPクリニック診断サービス (PingCAPクリニック) を使用してクラスターの問題をリモートでトラブルシューティングし、 [診断クライアント（Diag）](https://github.com/pingcap/diag)および Clinic Server を使用してクラスターの状態をローカルで簡単にチェックすることができます。

> **注記：**
>
> -   このドキュメントは、セルフホスト環境でTiUPを使用してデプロイされたクラスターに**のみ**適用されます。Kubernetes上でTiDB Operatorを使用してデプロイされたクラスターについては、 [TiDB Operator環境向けPingCAPクリニック](https://docs.pingcap.com/tidb-in-kubernetes/stable/clinic-user-guide)参照してください。
>
> -   PingCAPクリニック は、 TiDB Ansible を使用してデプロイされたクラスターからのデータ収集を**サポートしていません**。

## ユーザーシナリオ {#user-scenarios}

-   [クラスタの問題をリモートでトラブルシューティングする](#troubleshoot-cluster-problems-remotely)

    -   クラスターに問題がある場合、PingCAP から[サポートを受ける](/support.md)取得する必要があります。リモート トラブルシューティングを容易にするために、Diag を使用して診断データを収集し、収集したデータを Clinic Server にアップロードし、データ アクセス リンクをテクニカル サポート スタッフに提供するための次の操作を実行できます。
    -   クラスターに何らかの問題があり、すぐに問題を分析できない場合は、Diag を使用してデータを収集し、後で分析できるように保存することができます。

-   [ローカルでクラスタのステータスをクイックチェックする](#perform-a-quick-check-on-the-cluster-status-locally)

    クラスタが現在安定して動作している場合でも、潜在的な安定性リスクを検出するために、定期的にクラスタを検査する必要があります。PingCAP PingCAPクリニックが提供するローカルクイックチェック機能を使用すると、クラスタの潜在的なヘルスリスクを特定できます。ローカルチェックでは構成のみがチェックされます。メトリックやログなど、より多くの項目をチェックするには、診断データをClinic Serverにアップロードし、ヘルスレポート機能を使用することをお勧めします。

## 前提条件 {#prerequisites}

PingCAPクリニックを使用する前に、Diag（ PingCAPクリニックが提供するデータ収集コンポーネント）をインストールし、データをアップロードする環境を準備する必要があります。

1.  Diag をインストールします。

    -   コントロール マシンにTiUPがインストールされている場合は、次のコマンドを実行して Diag をインストールします。

        ```bash
        tiup install diag
        ```

    -   Diag をインストールしている場合は、次のコマンドを使用して Diag を最新バージョンにアップグレードできます。

        ```bash
        tiup update diag
        ```

    > **注記：**
    >
    > -   インターネット接続のないクラスタでは、Diagをオフラインで展開する必要があります。詳細については、 [TiUPをオフラインでデプロイ: 方法2](/production-deployment-using-tiup.md#deploy-tiup-offline)を参照してください。
    > -   Diag は、TiDB Server オフライン ミラー パッケージ v5.4.0 以降で**のみ**提供されます。

2.  データをアップロードするためのアクセス トークン (トークン) を取得して設定します。

    Diag を通じて収集したデータをアップロードする際、ユーザー認証用のトークンが必要です。既にトークン Diag を設定している場合は、そのトークンを再利用してこの手順を省略できます。

    トークンを取得するには、次の手順を実行します。

    -   クリニックサーバーにログインします。

        <SimpleTab groupId="clinicServer">
          <div label="Clinic Server for international users" value="clinic-us">

        [海外ユーザー向けクリニックサーバー](https://clinic.pingcap.com) : データは米国リージョンの AWS に保存されます。

        </div>
          <div label="Clinic Server for users in the Chinese mainland" value="clinic-cn">

        [中国本土のユーザー向けクリニックサーバー](https://clinic.pingcap.com.cn) : データは中国 (北京) リージョンの AWS に保存されます。

        </div>

        </SimpleTab>

    -   クラスタページの右下隅にあるアイコンをクリックし、 **「診断ツールのアクセストークンを取得」**を選択して、ポップアップウィンドウの**「+」**をクリックします。表示されるトークンをコピーして保存してください。

        ![Get the Token](/media/clinic-get-token.png)

    > **注記：**
    >
    > -   Clinic Serverに初めてアクセスする場合は、トークンを取得する前に、 [PingCAPクリニックでクイックスタート](/clinic/quick-start-with-clinic.md#prerequisites)を参考に環境を準備する必要があります。
    > -   データセキュリティのため、TiDBはトークン作成時にのみトークンを表示します。トークンを紛失した場合は、古いトークンを削除して新しいトークンを作成してください。
    > -   トークンはデータのアップロードにのみ使用されます。

    -   次に、Diag でトークンを設定します。例:

        ```bash
        tiup diag config clinic.token ${token-value}
        ```

3.  Diag に`region`設定します。

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

4.  (オプション) ログ編集を有効にします。

    TiDBが詳細なログ情報を提供する場合、ログに機密情報（ユーザーデータなど）が出力される可能性があります。ローカルログおよびClinic Serverへの機密情報の漏洩を防ぎたい場合は、TiDB側でログ編集を有効にすることができます。詳細については、 [ログ編集](/log-redaction.md#log-redaction-in-tidb-side)ご覧ください。

## クラスタの問題をリモートでトラブルシューティングする {#troubleshoot-cluster-problems-remotely}

Diag を使用すると、監視データや構成情報などの診断データを TiDB クラスターおよび DM クラスターから迅速に収集できます。

### ステップ1. 収集するデータを確認する {#step-1-check-the-data-to-be-collected}

Diag によって収集できるデータの完全なリストについては、 [PingCAPクリニック診断データ](/clinic/clinic-data-instruction-for-tiup.md)参照してください。

後続の診断の効率を高めるため、監視データや設定情報を含む完全な診断データを収集することをお勧めします。詳細については、 [クラスターからデータを収集する](#step-2-collect-data)参照してください。

### ステップ2. データを収集する {#step-2-collect-data}

Diag を使用すると、 TiUPを使用して展開された TiDB クラスターと DM クラスターからデータを収集できます。

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

    -   `-f/--from` : データ収集の開始時刻を指定します。このパラメータを指定しない場合、デフォルトの開始時刻は現在時刻の2時間前になります。タイムゾーンを変更するには、 `-f="12:30 +0800"`構文を使用します。このパラメータでタイムゾーン情報を指定しない場合（例： `+0800` ）、デフォルトのタイムゾーンはUTCです。
    -   `-t/--to` : データ収集の終了時刻を指定します。このパラメータを指定しない場合、デフォルトの終了時刻は現在時刻となります。タイムゾーンを変更するには、 `-f="12:30 +0800"`構文を使用します。このパラメータでタイムゾーン情報を指定しない場合（例： `+0800` ）、デフォルトのタイムゾーンはUTCです。

    パラメータの使用に関するヒント:

    Diag では、データ収集時間の指定に加えて、より多くのパラメータを指定できます。すべてのパラメータを取得するには、コマンド`tiup diag collect -h`または`tiup diag collectdm -h`実行します。

    > **注記：**
    >
    > -   Diag はデフォルトではシステム変数データ (db_vars) を収集しません。このデータを収集するには、データベースにアクセスできるユーザー名とパスワードを追加で入力する必要があります。なお、このデータベースではシステム変数への読み取りアクセスが有効になっている必要があります。
    > -   Diagはデフォルトではパフォーマンスデータ（ `perf` ）とデバッグデータ（ `debug` ）を収集しません。
    > -   システム変数を含む完全な診断データを収集するには、コマンド`tiup diag collect <cluster-name> --include="system,monitor,log,config,db_vars,perf,debug"`を使用します。

    -   `-l` : ファイル転送の帯域幅制限。単位は Kbit/s、デフォルト値は`100000` (scp の`-l`のパラメータ) です。
    -   `-N/--node` : 指定されたノードからのみデータを収集します。形式は`ip:port`です。
    -   `--include` : 特定の種類のデータのみを収集します。オプションの値は`system` 、 `monitor` 、 `log` 、 `config` 、 `db_vars`です。2つ以上の種類を含める場合は、種類間の区切りとして`,`使用できます。
    -   `--exclude` : 特定の種類のデータを収集しません。オプションの値は`system` 、 `monitor` 、 `log` 、 `config` 、 `db_vars`です。2つ以上の種類を除外する場合は、種類間の区切りとして`,`使用できます。
    -   `--metricsfilter` : 指定されたPrometheusメトリックのみを収集します。メトリックのプレフィックスをカンマ区切りで指定できます。例えば、 `--metricsfilter=tidb,pd` `tidb`で始まるメトリックと`pd`で始まるメトリックを収集します。

        > **ヒント：**
        >
        > 利用可能なメトリック プレフィックスを取得するには、次のコマンドを使用して TiDB モニタリング API をクエリできます。
        >
        > ```bash
        > curl -s 'http://${prometheus-host}:${prometheus-port}/api/v1/label/__name__/values' | jq -r '.data[]' | cut -d\_ -f1 | uniq -c | sort -rn
        > ```

    コマンドを実行した後、Diag はすぐにデータの収集を開始するわけではありません。代わりに、Diag は推定データサイズとターゲットデータstorageパスを出力に表示し、続行するかどうかを確認します。例:

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

    データの収集には一定の時間がかかります。収集するデータの量によって時間は異なります。例えば、テスト環境では1GBのデータの収集に約10分かかります。

    収集が完了すると、Diag は収集されたデータが保存されているフォルダのパスを表示します。例:

    ```bash
    Collected data are stored in /home/user/diag-fNTnz5MGhr6
    ```

### ステップ3. ローカルでデータをビュー（オプション） {#step-3-view-data-locally-optional}

収集されたデータは、データソースに基づいて個別のサブディレクトリに保存されます。これらのサブディレクトリは、マシン名とポート番号に基づいて名前が付けられます。各ノードの設定、ログ、その他のファイルのstorage場所は、TiDBクラスターの実サーバーにおける相対的なstorageパスと同じです。

-   システムとハードウェアの基本情報： `insight.json`
-   システム`/etc/security/limits.conf`の内容： `limits.conf`
-   カーネルパラメータのリスト: `sysctl.conf`
-   カーネルログ: `dmesg.log`
-   データ収集中のネットワーク接続: `ss.txt`
-   コンフィグレーションデータ：各ノードの`config.json`ディレクトリ
-   クラスター自体のメタ情報: in `meta.yaml` (このファイルは収集されたデータを保存するディレクトリの最上位にあります)
-   監視データ： `/monitor`ファイルディレクトリ内。監視データはデフォルトで圧縮されており、直接表示できません。監視データを含むJSONファイルを直接表示するには、データ収集時に`--compress-metrics=false`パラメータで圧縮を無効にしてください。

### ステップ4. データのアップロード {#step-4-upload-data}

PingCAPテクニカルサポートスタッフにクラスター診断データを提供するには、まずデータをクリニックサーバーにアップロードし、取得したデータアクセスリンクをスタッフに送信する必要があります。クリニックサーバーは、診断データを安全に保存・共有するクラウドサービスです。

クラスターのネットワーク接続に応じて、次のいずれかの方法を選択してデータをアップロードできます。

-   方法 1: クラスターが配置されているネットワークがインターネットにアクセスできる場合は、 [アップロードコマンドを使用してデータを直接アップロードする](#method-1-upload-directly)実行できます。
-   方法 2: クラスターが配置されているネットワークがインターネットにアクセスできない場合は、 [データをパックしてアップロードする](#method-2-pack-and-upload-data)実行する必要があります。

> **注記：**
>
> データをアップロードする前にDiagでトークンまたは`region`設定していない場合、Diagはアップロードの失敗を報告し、トークンまたは`region`設定するように促します。トークンを設定するには、 [前提条件の2番目のステップ](#prerequisites)参照してください。

#### 方法1. 直接アップロードする {#method-1-upload-directly}

クラスターが配置されているネットワークがインターネットにアクセスできる場合は、次のコマンドを使用して、 [ステップ2: データを収集する](#step-2-collect-data)で取得した収集データを含むフォルダーを直接アップロードできます。

```bash
tiup diag upload
```

アップロードが完了すると、出力に`Download URL`が表示されます。3 `Download URL`リンクを開いてアップロードされたデータを確認するか、以前に連絡したPingCAPテクニカルサポートスタッフにリンクを送信してください。

#### 方法2. データをパックしてアップロードする {#method-2-pack-and-upload-data}

クラスターが設置されているネットワークがインターネットにアクセスできない場合は、イントラネット上でデータをパックし、インターネットにアクセスできるデバイスを使用してデータパッケージをクリニックサーバーにアップロードする必要があります。詳細な手順は以下のとおりです。

1.  以下のコマンドを実行して、 [ステップ2. データを収集する](#step-2-collect-data)で取得した収集データをパックします。

    ```bash
    tiup diag package ${filepath}
    ```

    Diagはパッケージ化の際に、データの暗号化と圧縮を同時に行います。テスト環境では、800MBのデータが57MBに圧縮されました。以下は出力例です。

    ```bash
    Starting component `diag`: /root/.tiup/components/diag/v0.7.0/diag package diag-fNTnz5MGhr6
    packaged data set saved to /home/user/diag-fNTnz5MGhr6.diag
    ```

    パッケージングが完了すると、データは`.diag`形式にパッケージ化されます。3 `.diag`ファイルは、クリニックサーバーにアップロードされた後にのみ復号化して閲覧できます。収集したデータをクリニックサーバーにアップロードせずに直接転送する場合は、独自の方法でデータを圧縮して転送することもできます。

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

## ローカルでクラスタのステータスをクイックチェックする {#perform-a-quick-check-on-the-cluster-status-locally}

Diag を使用すると、クラスタの状態をローカルで簡単に確認できます。クラスタが現在安定して動作している場合でも、潜在的な安定性リスクを検出するために、定期的にクラスタの状態を確認する必要があります。PingCAP PingCAPクリニックが提供するローカルクイックチェック機能を使用すると、クラスタの潜在的なヘルスリスクを特定できます。ローカルチェックでは構成のみがチェックされます。メトリックやログなど、より多くの項目を確認するには、診断データを Clinic サーバーにアップロードし、ヘルスレポート機能を使用することをお勧めします。

1.  構成データを収集します。

    ```bash
    tiup diag collect ${cluster-name} --include="config"
    ```

    設定ファイルのデータは比較的小さく、収集後、デフォルトで現在のパスに保存されます。テスト環境では、18ノードのクラスタの場合、設定ファイルのデータサイズは10KB未満でした。

2.  構成データを診断します。

    ```bash
    tiup diag check ${subdir-in-output-data}
    ```

    上記コマンドの`${subdir-in-output-data}`は収集したデータを保存するパスであり、このパスには`meta.yaml`ファイルがあります。

3.  診断結果をビュー:

    診断結果はコマンドラインに返されます。例:

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
    The configuration rules are all derived from PingCAP's OnCall Service.

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

    診断結果の最後のセクション（上記の出力例の`#### Path to save the diagnostic result file` ）では、検出された設定上の潜在的なリスクごとに、詳細な設定提案を含むナレッジベースへのリンクが提供されます。上記の例では、関連するリンクは`https://s.tidb.io/msmo6awg`です。

## FAQ {#faq}

1.  データのアップロードに失敗した場合、再度アップロードできますか？

    はい。データのアップロードはブレークポイントアップロードをサポートしています。アップロードに失敗した場合は、直接再度アップロードできます。

2.  データをアップロードした後、返されたデータアクセスリンクを開くことができません。どうすればよいでしょうか？

    まずクリニックサーバーにログインしてください。ログインに成功してもリンクを開けない場合は、データへのアクセス権があるかどうかを確認してください。アクセス権がない場合は、データ所有者に連絡して許可を得てください。許可を得た後、クリニックサーバーにログインしてリンクを再度開いてください。

3.  アップロードされたデータはクリニックサーバーにどのくらいの期間保存されますか?

    最長期間は180日間です。クリニックサーバーページでアップロードしたデータはいつでも削除できます。
