---
title: Troubleshoot TiDB Cluster Using PingCAP Clinic
summary: Learn how to use the PingCAP Clinic Diagnostic Service to troubleshoot cluster problems remotely and perform a quick check of the cluster status on a cluster deployed using TiUP.
---

# PingCAPクリニックを使用したTiDBクラスターのトラブルシューティング {#troubleshoot-tidb-cluster-using-pingcap-clinic}

TiUPを使用して展開されたTiDBクラスターおよびDMクラスターの場合、 PingCAPクリニック Diagnostic Service（PingCAPクリニック）を使用して、クラスタの問題をリモートでトラブルシューティングし、Diagクライアント（Diag）および[クリニックサーバー中国](https://clinic.pingcap.com.cn) （Clinic Server）を使用してローカルでクラスタステータスのクイックチェックを実行できます。 Diag and Clinic Serverの詳細については、 [PingCAPクリニックのコンポーネント](/clinic/clinic-introduction.md)を参照してください。

PingCAPクリニックは現在テクニカルプレビュー段階にあります。

> **ノート：**
>
> PingCAPクリニックは、TiDBAnsibleを使用してデプロイされたクラスターからのデータの収集**をサポートしていません**。

## ユーザーシナリオ {#user-scenarios}

-   [クラスタの問題をリモートでトラブルシューティングする](#troubleshoot-cluster-problems-remotely)

    -   クラスタに問題がある場合、PingCAPテクニカルサポートに連絡する必要がある場合は、リモートトラブルシューティングを容易にするために次の操作を実行できます。Diagで診断データを収集し、収集したデータをClinic Serverにアップロードし、データアクセスリンクをテクニカルサポートスタッフ。
    -   クラスタに問題がある場合、問題をすぐに分析できない場合は、Diagを使用してデータを収集および保存し、後で分析することができます。

-   [ローカルでクラスタステータスのクイックチェックを実行します](#perform-a-quick-check-on-the-cluster-status-locally)

    現在クラスタが安定して稼働している場合でも、潜在的な安定性のリスクを回避するために、クラスタを定期的にチェックする必要があります。 PingCAPクリニックが提供するローカルクイックチェック機能を使用して、クラスタの潜在的な健康リスクをチェックできます。 PingCAPクリニック Technical Previewバージョンは、クラスタ構成アイテムの合理性チェックを提供して、不合理な構成を発見し、変更の提案を提供します。

## 前提条件 {#prerequisites}

PingCAPクリニックを使用する前に、Diag（ PingCAPクリニックによって提供されるデータを収集するためのコンポーネント）をインストールし、データをアップロードするための環境を準備する必要があります。

1.  Diagをインストールします。

    -   制御マシンにTiUPをインストールした場合は、次のコマンドを実行してDiagをインストールします。

        {{< copyable "" >}}

        ```bash
        tiup install diag
        ```

    -   Diagをインストールしている場合は、次のコマンドを使用してDiagを最新バージョンにアップグレードできます。

        {{< copyable "" >}}

        ```bash
        tiup update diag
        ```

    > **ノート：**
    >
    > -   インターネットに接続されていないクラスターの場合、Diagをオフラインでデプロイする必要があります。詳しくは[TiUPをオフラインでデプロイ：方法2](/production-deployment-using-tiup.md#deploy-tiup-offline)をご覧ください。
    > -   Diagは、v5.4.0以降のTiDBサーバーオフラインミラーパッケージで**のみ**提供されます。

2.  データをアップロードするためのアクセストークン（トークン）を取得して設定します。

    収集したデータをDiag経由でアップロードする場合、ユーザー認証用のトークンが必要です。トークンDiagをすでに設定している場合は、トークンを再利用してこの手順をスキップできます。

    トークンを取得するには、 [クリニックサーバー](https://clinic.pingcap.com.cn)にログインし、クラスターページの右下隅にあるアイコンをクリックします。次に、[**診断ツールのアクセストークンの取得**]を選択し、ポップアップウィンドウで[ <strong>+</strong> ]をクリックします。表示されたトークン情報をコピーして保存したことを確認してください。

    ![Get the Token](/media/clinic-get-token.png)

    > **ノート：**
    >
    > -   Clinic Serverに初めてアクセスするときは、トークンを取得する前に、AskTUGアカウントを使用して[クリニックサーバー](https://clinic.pingcap.com.cn)にログインし、最初に組織を作成する必要があります。
    > -   データセキュリティのために、TiDBはトークンの作成時にのみトークンを表示します。トークンを紛失した場合は、古いトークンを削除して新しいトークンを作成してください。
    > -   トークンは、データのアップロードにのみ使用されます。

    次に、Diagでトークンを設定します。例えば：

    {{< copyable "" >}}

    ```bash
    tiup diag config clinic.token ${token-value}
    ```

3.  （オプション）ログの編集を有効にします。

    TiDBが詳細なログ情報を提供する場合、機密情報（ユーザーデータなど）をログに出力する場合があります。ローカルログとクリニックサーバーで機密情報が漏洩するのを防ぎたい場合は、TiDB側でログの編集を有効にすることができます。詳細については、 [ログ編集](/log-redaction.md#log-redaction-in-tidb-side)を参照してください。

## クラスタの問題をリモートでトラブルシューティングする {#troubleshoot-cluster-problems-remotely}

Diagを使用すると、監視データや構成情報など、TiDBクラスターおよびDMクラスターから診断データをすばやく収集できます。

### 手順1.収集するデータを確認します {#step-1-check-the-data-to-be-collected}

Diagが収集できるデータの完全なリストについては、 [PingCAPクリニックの診断データ](/clinic/clinic-data-instruction-for-tiup.md)を参照してください。

後の診断の効率を向上させるために、監視データや構成情報を含む完全な診断データを収集することをお勧めします。詳細については、 [TiDBクラスターからデータを収集する](#collect-data-from-tidb-clusters)を参照してください。

### ステップ2.データを収集する {#step-2-collect-data}

Diagを使用すると、TiUPを使用してデプロイされたTiDBクラスターおよびDMクラスターからデータを収集できます。

#### TiDBクラスターからデータを収集する {#collect-data-from-tidb-clusters}

1.  Diagのデータ収集コマンドを実行します。

    たとえば、現在の時刻に基づいて4時間前から2時間前までの診断データを収集するには、次のコマンドを実行します。

    {{< copyable "" >}}

    ```bash
    tiup diag collect ${cluster-name} -f="-4h" -t="-2h"
    ```

    データ収集のパラメーターの説明：

    -   `-f/--from` ：データ収集の開始時刻を指定します。このパラメーターを指定しない場合、デフォルトの開始時刻は現在時刻の2時間前です。タイムゾーンを変更するには、 `-f="12:30 +0800"`の構文を使用します。このパラメータで`+0800`などのタイムゾーン情報を指定しない場合、タイムゾーンはデフォルトでUTCです。
    -   `-t/--to` ：データ収集の終了時刻を指定します。このパラメーターを指定しない場合、デフォルトの終了時刻は現在の瞬間です。タイムゾーンを変更するには、 `-f="12:30 +0800"`の構文を使用します。このパラメータで`+0800`などのタイムゾーン情報を指定しない場合、タイムゾーンはデフォルトでUTCです。

    パラメータ使用のヒント：

    データ収集時間を指定することに加えて、Diagを使用してより多くのパラメーターを指定できます。すべてのパラメーターを取得するには、 `tiup diag collect -h`コマンドを実行します。

    > **ノート：**
    >
    > -   Diagは、デフォルトではシステム変数データ（db_vars）を収集しません。このデータを収集するには、データベースにアクセスできるユーザー名とパスワードを追加で提供する必要があります。このデータベースでは、システム変数への読み取りアクセスを有効にする必要があることに注意してください。
    > -   Diagは、デフォルトではパフォーマンスデータ（ `perf` ）とデバッグデータ（ `debug` ）を収集しません。
    > -   システム変数を含む完全な診断データを収集するには、コマンド`tiup diag collect <cluster-name> --include="system,monitor,log,config,db_vars,perf,debug"`を使用します。

    -   `-l` ：ファイル転送の帯域幅制限。単位はKbit / s、デフォルト値は`100000` （scpの`-l`パラメーター）です。
    -   `-N/--node` ：指定されたノードからのみデータを収集します。形式は`ip:port`です。
    -   `--include` ：特定のタイプのデータのみを収集します。オプションの値`db_vars` 、 `system` 、 `log` `monitor` `config` 。 2つ以上のタイプを含めるには、タイプ間の区切り文字として`,`を使用できます。
    -   `--exclude` ：特定の種類のデータを収集しません。オプションの値`db_vars` 、 `system` 、 `log` `monitor` `config` 。 2つ以上のタイプを除外するには、タイプ間の区切り文字として`,`を使用できます。

    コマンドを実行した後、Diagはすぐにデータの収集を開始しません。代わりに、Diagは、続行するかどうかを確認するために、出力に推定データサイズとターゲットデータストレージパスを提供します。例えば：

    {{< copyable "" >}}

    ```bash
    Estimated size of data to collect:
    Host               Size       Target
    ----               ----       ------
    172.16.7.129:9090  43.57 MB   1775 metrics, compressed
    172.16.7.87        0 B        /tidb-deploy/tidb-4000/log/tidb_stderr.log
    ... ...
    172.16.7.179       325 B      /tidb-deploy/tikv-20160/conf/tikv.toml
    Total              2.01 GB    (inaccurate)
    These data will be stored in /home/qiaodan/diag-fNTnz5MGhr6
    Do you want to continue? [y/N]: (default=N)
    ```

2.  `Y`を入力して、データの収集を開始することを確認します。

    データの収集には一定の時間がかかります。時間は、収集するデータの量によって異なります。たとえば、テスト環境では、1GBのデータを収集するのに約10分かかります。

    収集が完了すると、Diagは収集されたデータが配置されているフォルダーパスを提供します。例えば：

    {{< copyable "" >}}

    ```bash
    Collected data are stored in /home/qiaodan/diag-fNTnz5MGhr6
    ```

#### DMクラスターからデータを収集する {#collect-data-from-dm-clusters}

1.  Diagのデータ収集コマンドを実行します。

    たとえば、現在の時刻に基づいて4時間前から2時間前までの診断データを収集するには、次のコマンドを実行します。

    {{< copyable "" >}}

    ```bash
    tiup diag collectdm ${cluster-name} -f="-4h" -t="-2h"
    ```

    上記のコマンドで使用されるパラメーター、またはDiagで使用される可能性のあるその他のパラメーターの説明については、 [TiDBクラスターからデータを収集する](#collect-data-from-tidb-clusters)を参照してください。

    コマンドを実行した後、Diagはすぐにデータの収集を開始しません。代わりに、Diagは、続行するかどうかを確認するために、出力に推定データサイズとターゲットデータストレージパスを提供します。

2.  `Y`を入力して、データの収集を開始することを確認します。

    データの収集には一定の時間がかかります。時間は、収集するデータの量によって異なります。たとえば、テスト環境では、1GBのデータを収集するのに約10分かかります。

    収集が完了すると、Diagは収集されたデータが配置されているフォルダーパスを提供します。例えば：

    {{< copyable "" >}}

    ```bash
    Collected data are stored in /home/qiaodan/diag-fNTnz5MGhr6
    ```

### 手順3.データをローカルでビューする（オプション） {#step-3-view-data-locally-optional}

収集されたデータは、そのデータソースに基づいて個別のサブディレクトリに保存されます。これらのサブディレクトリは、マシン名とポート番号にちなんで名付けられています。各ノードの構成、ログ、およびその他のファイルの保存場所は、TiDBクラスタの実サーバーでの相対的な保存パスと同じです。

-   システムとハードウェアの基本情報：in `insight.json`
-   システムの内容`/etc/security/limits.conf` ：in `limits.conf`
-   カーネルパラメータのリスト：in `sysctl.conf`
-   カーネルログ：in `dmesg.log`
-   データ収集中のネットワーク接続：in `ss.txt`
-   Configuration / コンフィグレーションデータ：各ノードの`config.json`のディレクトリ
-   クラスタ自体のメタ情報：in `meta.yaml` （このファイルは、収集されたデータを格納するディレクトリの最上位にあります）
-   監視データ： `/monitor`ファイルディレクトリ内。監視データはデフォルトで圧縮されており、直接表示することはできません。監視データを含むJSONファイルを直接表示するには、データを収集するときに`--compress-metrics=false`パラメーターを使用して圧縮を無効にします。

### ステップ4.データをアップロードする {#step-4-upload-data}

クラスタ診断データをPingCAPテクニカルサポートスタッフに提供するには、最初にデータをクリニックサーバーにアップロードしてから、取得したデータアクセスリンクをスタッフに送信する必要があります。 Clinic Serverは、診断データを安全に保存および共有するクラウドサービスです。

クラスタのネットワーク接続に応じて、次のいずれかの方法を選択してデータをアップロードできます。

-   方法1：クラスタが配置されているネットワークがインターネットにアクセスできる場合は、 [uploadコマンドを使用してデータを直接アップロードする](#method-1-upload-directly)を実行できます。
-   方法2：クラスタが配置されているネットワークがインターネットにアクセスできない場合は、 [データをパックしてからアップロードします](#method-2-pack-and-upload-data)を実行する必要があります。

> **ノート：**
>
> データをアップロードする前にDiagでトークンを設定しなかった場合、Diagはアップロードの失敗を報告し、トークンを設定するように通知します。トークンを設定するには、 [前提条件の2番目のステップ](#prerequisites)を参照してください。

#### 方法1.直接アップロードする {#method-1-upload-directly}

クラスタが配置されているネットワークがインターネットにアクセスできる場合は、次のコマンドを使用して、 [ステップ2：データを収集する](#step-2-collect-data)で取得した収集データを含むフォルダを直接アップロードできます。

{{< copyable "" >}}

```bash
tiup diag upload
```

アップロードが完了すると、出力に`Download URL`が表示されます。 `Download URL`のリンクを開いて、アップロードされたデータを表示するか、以前に連絡したPingCAPテクニカルサポートスタッフにリンクを送信できます。

#### 方法2.データをパックしてアップロードする {#method-2-pack-and-upload-data}

クラスタが配置されているネットワークがインターネットにアクセスできない場合は、イントラネットにデータをパックし、インターネットにアクセスできるデバイスを使用してデータパッケージをクリニックサーバーにアップロードする必要があります。詳細な操作は次のとおりです。

1.  次のコマンドを実行して、 [ステップ2.データを収集する](#step-2-collect-data)で取得した収集データをパックします。

    {{< copyable "" >}}

    ```bash
    tiup diag package ${filepath}
    ```

    パッケージ化中に、Diagはデータの暗号化と圧縮を同時に行います。テスト環境では、800MBのデータが57MBに圧縮されました。次に、出力例を示します。

    ```bash
    Starting component `diag`: /root/.tiup/components/diag/v0.7.0/diag package diag-fNTnz5MGhr6
    packaged data set saved to /home/qiaodan/diag-fNTnz5MGhr6.diag
    ```

    パッケージ化が完了すると、データは`.diag`形式にパッケージ化されます。 `.diag`ファイルは、クリニックサーバーにアップロードされた後にのみ復号化および表示できます。収集したデータをクリニックサーバーにアップロードするのではなく、直接転送する場合は、独自の方法でデータを圧縮して転送することができます。

2.  インターネットにアクセスできるマシンから、圧縮データパッケージをアップロードします。

    {{< copyable "" >}}

    ```bash
    tiup diag upload ${filepath}
    ```

    次に、出力例を示します。

    {{< copyable "" >}}

    ```bash
    [root@Copy-of-VM-EE-CentOS76-v1 qiaodan]# tiup diag upload /home/qiaodan/diag-fNTnz5MGhr6
    Starting component `diag`: /root/.tiup/components/diag/v0.7.0/diag upload /home/qiaodan/diag-fNTnz5MGhr6
    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>><>>>>>>>>>
    Completed!
    Download URL: "https://clinic.pingcap.com.cn/portal/#/orgs/4/clusters/XXXX"
    ```

3.  アップロードが完了したら、 `Download URL`のリンクを開いてアップロードされたデータを表示するか、以前に連絡したPingCAPテクニカルサポートスタッフにリンクを送信できます。

## ローカルでクラスタステータスのクイックチェックを実行します {#perform-a-quick-check-on-the-cluster-status-locally}

Diagを使用して、ローカルでクラスタステータスをすばやく確認できます。現在クラスタが安定して稼働している場合でも、潜在的な安定性のリスクを回避するために、クラスタを定期的にチェックする必要があります。 PingCAPクリニック Technical Previewバージョンは、クラスタ構成アイテムの合理性チェックを提供して、不合理な構成を発見し、変更の提案を提供します。

1.  構成データを収集します。

    {{< copyable "" >}}

    ```bash
    tiup diag collect ${cluster-name} --include="config"
    ```

    構成ファイルのデータは比較的小さいです。収集後、収集されたデータはデフォルトで現在のパスに保存されます。テスト環境では、18ノードのクラスタの場合、構成ファイルのデータサイズは10KB未満です。

2.  構成データの診断：

    {{< copyable "" >}}

    ```bash
    tiup diag check ${subdir-in-output-data}
    ```

    上記のコマンドの`${subdir-in-output-data}`は、収集されたデータを格納するパスであり、このパスには`meta.yaml`ファイルがあります。

3.  診断結果をビューします。

    診断結果はコマンドラインに返されます。例えば：

    {{< copyable "" >}}

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

    診断結果の最後のセクション（上記の出力例では`#### Path to save the diagnostic result file`未満）で、検出された構成の潜在的なリスクごとに、Diagは詳細な構成の提案を含む対応するナレッジベースリンクを提供します。上記の例では、関連するリンクは`https://s.tidb.io/msmo6awg`です。

## FAQ {#faq}

1.  データのアップロードに失敗した場合、再アップロードできますか？

    はい。データアップロードはブレークポイントアップロードをサポートします。アップロードに失敗した場合は、直接再度アップロードできます。

2.  データをアップロードした後、返されたデータアクセスリンクを開くことができません。私は何をすべきか？

    最初に[クリニックサーバー](https://clinic.pingcap.com.cn)にログインしてみてください。それでもリンクを開くことができない場合は、データを表示する権限があるかどうかを確認してください。そうでない場合は、許可を得るためにデータ所有者に連絡してください。許可を得た後、クリニックサーバーにログインしてリンクを再度開いてみてください。

3.  アップロードされたデータはクリニックサーバーにどのくらいの期間保持されますか？

    テクニカルサポートケースがクローズされた後、PingCAPは90日以内に対応するデータを完全に削除または匿名化します。
