---
title: Upgrade TiDB Using TiUP
summary: TiUPを使用して TiDB をアップグレードする方法を学びます。
---

# TiUPを使用して TiDB をアップグレードする {#upgrade-tidb-using-tiup}

このドキュメントは、次のアップグレード パスを対象としています。

-   TiDB 4.0 バージョンから TiDB 8.1 にアップグレードします。
-   TiDB 5.0-5.4 バージョンから TiDB 8.1 にアップグレードします。
-   TiDB 6.0-6.6 から TiDB 8.1 にアップグレードします。
-   TiDB 7.0-7.6 から TiDB 8.1 にアップグレードします。
-   TiDB 8.0 から TiDB 8.1 にアップグレードします。

> **警告：**
>
> 1.  TiFlash を5.3 より前のバージョンから 5.3 以降にオンラインでアップグレードすることはできません。代わりに、まず以前のバージョンのすべてのTiFlashインスタンスを停止してから、クラスターをオフラインでアップグレードする必要があります。他のコンポーネント (TiDB や TiKV など) がオンライン アップグレードをサポートしていない場合は、 [オンラインアップグレード](#online-upgrade)の警告の手順に従ってください。
> 2.  アップグレード プロセス中に DDL ステートメントを実行**しないでください**。そうしないと、未定義の動作の問題が発生する可能性があります。
> 3.  クラスター内で DDL ステートメントが実行されているときは、TiDB クラスターをアップグレード**しないでください**(通常は、 `ADD INDEX`や列タイプの変更などの時間のかかる DDL ステートメントの場合)。アップグレードの前に、 [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md)コマンドを使用して、TiDB クラスターに実行中の DDL ジョブがあるかどうかを確認することをお勧めします。クラスターに DDL ジョブがある場合は、クラスターをアップグレードする前に、DDL の実行が完了するまで待つか、 [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)コマンドを使用して DDL ジョブをキャンセルしてください。
>
> アップグレード前の TiDB バージョンが v7.1.0 以降の場合、前述の警告 2 と 3 は無視できます。詳細については、 [TiDB スムーズアップグレード](/smooth-upgrade-tidb.md)参照してください。

> **注記：**
>
> -   アップグレードするクラスターが v3.1 またはそれ以前のバージョン (v3.0 または v2.1) の場合、v8.1.0 への直接アップグレードはサポートされていません。最初にクラスターを v4.0 にアップグレードし、次に v8.1.0 にアップグレードする必要があります。
> -   アップグレードするクラスターが v6.2 より前の場合、一部のシナリオではクラスターを v6.2 以降のバージョンにアップグレードすると、アップグレードが停止する可能性があります。 [問題を解決する方法](#how-to-fix-the-issue-that-the-upgrade-gets-stuck-when-upgrading-to-v620-or-later-versions)を参照してください。
> -   TiDB ノードは、構成項目[`server-version`](/tidb-configuration-file.md#server-version)の値を使用して現在の TiDB バージョンを確認します。したがって、予期しない動作を回避するには、TiDB クラスターをアップグレードする前に、値`server-version`を空に設定するか、現在の TiDB クラスターの実際のバージョンに設定する必要があります。
> -   [`performance.force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v657-and-v710)構成項目を`ON`に設定すると、 TiDB の起動時間が長くなり、起動タイムアウトやアップグレードの失敗が発生する可能性があります。 この問題を回避するには、 TiUPの待機タイムアウトを長く設定することをお勧めします。
>     -   影響を受ける可能性があるシナリオ:
>         -   元のクラスターのバージョンは v6.5.7 および v7.1.0 (まだ`performance.force-init-stats`サポートしていません) より前であり、ターゲット バージョンは v7.2.0 以降です。
>         -   元のクラスターのバージョンは v6.5.7 および v7.1.0 以上であり、 `performance.force-init-stats`構成項目は`ON`に設定されています。
>
>     -   `performance.force-init-stats`構成項目の値を確認します。
>
>             SHOW CONFIG WHERE type = 'tidb' AND name = 'performance.force-init-stats';
>
>     -   コマンドライン オプション[`--wait-timeout`](/tiup/tiup-component-cluster.md#--wait-timeout)を追加することで、 TiUP待機タイムアウトを増やすことができます。たとえば、待機タイムアウトを 1200 秒 (20 分) に設定するには、次のコマンドを実行します。
>
>         ```shell
>         tiup update cluster --wait-timeout 1200 [other options]
>         ```
>
>         一般的に、ほとんどのシナリオでは 20 分の待機タイムアウトで十分です。より正確な見積もりを得るには、TiDB ログで`init stats info time`を検索して、前回の起動時の統計読み込み時間を参照として取得します。例:
>
>             [domain.go:2271] ["init stats info time"] [lite=true] ["take time"=2.151333ms]
>
>         元のクラスタが v7.1.0 以前の場合、v7.2.0 以降にアップグレードすると、 [`performance.lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710)の導入により、統計の読み込み時間が大幅に短縮されます。この場合、アップグレード前の`init stats info time`が、アップグレード後の読み込み時間よりも長くなります。
>
>     -   TiDB のローリング アップグレード期間を短縮し、アップグレード中に初期統計情報が失われることによる潜在的なパフォーマンスへの影響がクラスターにとって許容できる場合は、アップグレード前に`performance.force-init-stats`を[TiUPを使用してターゲットインスタンスの構成を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)に設定して`OFF`設定できます。アップグレードが完了したら、必要に応じてこの設定を再評価して元に戻すことができます。

## アップグレードの注意事項 {#upgrade-caveat}

-   TiDB は現在、アップグレード後のバージョンのダウングレードや以前のバージョンへのロールバックをサポートしていません。
-   TiDB Ansibleを使用して管理されているv4.0クラスターの場合、 [TiUP (v4.0) を使用して TiDB をアップグレードする](https://docs.pingcap.com/tidb/v4.0/upgrade-tidb-using-tiup#import-tidb-ansible-and-the-inventoryini-configuration-to-tiup)に従って新しい管理のためにクラスターをTiUP （ `tiup cluster` ）にインポートする必要があります。その後、このドキュメントに従ってクラスターをv8.1.0にアップグレードできます。
-   v3.0 より前のバージョンを v8.1.0 に更新するには:
    1.  [TiDB アンシブル](https://docs.pingcap.com/tidb/v3.0/upgrade-tidb-using-ansible)を使用してこのバージョンを 3.0 に更新します。
    2.  TiUP （ `tiup cluster` ）を使用してTiDB Ansible設定をインポートします。
    3.  [TiUP (v4.0) を使用して TiDB をアップグレードする](https://docs.pingcap.com/tidb/v4.0/upgrade-tidb-using-tiup#import-tidb-ansible-and-the-inventoryini-configuration-to-tiup)に従って 3.0 バージョンを 4.0 に更新します。
    4.  このドキュメントに従ってクラスターを v8.1.0 にアップグレードします。
-   TiDB Binlog、TiCDC、 TiFlash、およびその他のコンポーネントのバージョンのアップグレードをサポートします。
-   TiFlash をv6.3.0 より前のバージョンから v6.3.0 以降のバージョンにアップグレードする場合、CPU が Linux AMD64アーキテクチャの AVX2 命令セットと Linux ARM64アーキテクチャの ARMv8 命令セットアーキテクチャをサポートしている必要があることに注意してください。詳細については、 [v6.3.0 リリースノート](/releases/release-6.3.0.md#others)の説明を参照してください。
-   異なるバージョンの詳細な互換性の変更については、各バージョンの[リリースノート](/releases/release-notes.md)参照してください。対応するリリース ノートの「互換性の変更」セクションに従って、クラスター構成を変更します。
-   v5.3 より前のバージョンから v5.3 以降のバージョンにアップグレードするクラスターの場合、デフォルトでデプロイされている Prometheus は v2.8.1 から v2.27.1 にアップグレードされます。Prometheus v2.27.1 では、より多くの機能が提供され、セキュリティ問題が修正されています。v2.8.1 と比較して、v2.27.1 ではアラート時間の表現が変更されています。詳細については、 [プロメテウスコミット](https://github.com/prometheus/prometheus/commit/7646cbca328278585be15fa615e22f2a50b47d06)参照してください。

## 準備 {#preparations}

このセクションでは、 TiUPおよびTiUPクラスタコンポーネントのアップグレードなど、TiDB クラスターをアップグレードする前に必要な準備作業について説明します。

### ステップ1: 互換性の変更を確認する {#step-1-review-compatibility-changes}

TiDB v8.1.0 リリース ノートの[互換性の変更](/releases/release-8.1.0.md#compatibility-changes)確認してください。アップグレードに影響する変更がある場合は、それに応じて対処してください。

### ステップ2: TiUPまたはTiUPオフラインミラーをアップグレードする {#step-2-upgrade-tiup-or-tiup-offline-mirror}

TiDB クラスターをアップグレードする前に、まずTiUPまたはTiUPミラーをアップグレードする必要があります。

#### TiUPとTiUPクラスタのアップグレード {#upgrade-tiup-and-tiup-cluster}

> **注記：**
>
> アップグレードするクラスターの制御マシンが`https://tiup-mirrors.pingcap.com`アクセスできない場合は、このセクションをスキップして[TiUPオフラインミラーのアップグレード](#upgrade-tiup-offline-mirror)を参照してください。

1.  TiUPバージョンをアップグレードします。TiUP バージョンは`1.11.3`以降が推奨されます。

    ```shell
    tiup update --self
    tiup --version
    ```

2.  TiUPクラスタのバージョンをアップグレードします。TiUPクラスタのTiUPは`1.11.3`以降にすることをお勧めします。

    ```shell
    tiup update cluster
    tiup cluster --version
    ```

#### TiUPオフラインミラーのアップグレード {#upgrade-tiup-offline-mirror}

> **注記：**
>
> アップグレードするクラスターがオフライン方式を使用せずにデプロイされた場合は、この手順をスキップします。

[TiUPを使用して TiDBクラスタをデプロイ- TiUPをオフラインでデプロイ](/production-deployment-using-tiup.md#deploy-tiup-offline)を参照して、新しいバージョンのTiUPミラーをダウンロードし、制御マシンにアップロードします。 `local_install.sh`を実行すると、 TiUP は上書きアップグレードを完了します。

```shell
tar xzvf tidb-community-server-${version}-linux-amd64.tar.gz
sh tidb-community-server-${version}-linux-amd64/local_install.sh
source /home/tidb/.bash_profile
```

上書きアップグレード後、次のコマンドを実行して、サーバーおよびツールキットのオフライン ミラーをサーバーディレクトリにマージします。

```bash
tar xf tidb-community-toolkit-${version}-linux-amd64.tar.gz
ls -ld tidb-community-server-${version}-linux-amd64 tidb-community-toolkit-${version}-linux-amd64
cd tidb-community-server-${version}-linux-amd64/
cp -rp keys ~/.tiup/
tiup mirror merge ../tidb-community-toolkit-${version}-linux-amd64
```

ミラーをマージした後、次のコマンドを実行してTiUPクラスタコンポーネントをアップグレードします。

```shell
tiup update cluster
```

これで、オフライン ミラーのアップグレードは成功しました。上書き後のTiUP操作中にエラーが発生した場合は、 `manifest`が更新されていない可能性があります。TiUPを再度実行する前に、 `rm -rf ~/.tiup/manifests/*`試してください。

### ステップ3: TiUPトポロジ構成ファイルを編集する {#step-3-edit-tiup-topology-configuration-file}

> **注記：**
>
> 次のいずれかの状況に該当する場合は、この手順をスキップしてください。
>
> -   元のクラスターの構成パラメータを変更していません。または、 `tiup cluster`を使用して構成パラメータを変更しましたが、それ以上の変更は必要ありません。
> -   アップグレード後、変更されていない構成項目に対して v8.1.0 のデフォルトのパラメータ値を使用します。

1.  トポロジファイルを編集するには、 `vi`編集モードに入ります。

    ```shell
    tiup cluster edit-config <cluster-name>
    ```

2.  [トポロジー](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml)の構成テンプレートの形式を参照して、トポロジ ファイルの`server_configs`セクションに変更するパラメータを入力します。

3.  変更後、 <kbd>:</kbd> + <kbd>w</kbd> + <kbd>q</kbd>と入力して変更を保存し、編集モードを終了します。変更を確認するには、 <kbd>Y</kbd>と入力します。

> **注記：**
>
> クラスターを v6.6.0 にアップグレードする前に、v4.0 で変更したパラメータが v8.1.0 と互換性があることを確認してください。詳細については、 [TiKVコンフィグレーションファイル](/tikv-configuration-file.md)参照してください。

### ステップ4: クラスターのDDLとバックアップのステータスを確認する {#step-4-check-the-ddl-and-backup-status-of-the-cluster}

アップグレード中に未定義の動作やその他の予期しない問題を回避するために、アップグレード前に次の項目を確認することをお勧めします。

-   クラスタDDL: 実行中の DDL ジョブがあるかどうかを確認するには、 [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md)のステートメントを実行することをお勧めします。実行中の DDL ジョブがある場合は、その実行を待つか、アップグレードを実行する前に[`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)ステートメントを実行してキャンセルします。
-   クラスタバックアップ: クラスター内で実行中のバックアップまたは復元タスクがあるかどうかを確認するには、 [`SHOW [BACKUPS|RESTORES]`](/sql-statements/sql-statement-show-backups.md)ステートメントを実行することをお勧めします。実行中の場合は、アップグレードを実行する前に完了するまで待機します。

### ステップ5: 現在のクラスターのヘルスステータスを確認する {#step-5-check-the-health-status-of-the-current-cluster}

アップグレード中に未定義の動作やその他の問題を回避するには、アップグレード前に現在のクラスターのリージョンのヘルス ステータスを確認することをお勧めします。これを行うには、 `check`サブコマンドを使用できます。

```shell
tiup cluster check <cluster-name> --cluster
```

コマンドを実行すると、「リージョンステータス」のチェック結果が出力されます。

-   結果が「すべてのリージョンが正常です」の場合、現在のクラスター内のすべてのリージョンが正常であり、アップグレードを続行できます。
-   結果が「リージョンが完全に正常ではありません: m ミスピア、n 保留中のピア」で、「他の操作の前に、異常なリージョンを修正してください。」というプロンプトが表示される場合、現在のクラスター内の一部のリージョンが異常です。チェック結果が「すべてのリージョンが正常です」になるまで、異常をトラブルシューティングする必要があります。その後、アップグレードを続行できます。

## TiDBクラスタをアップグレードする {#upgrade-the-tidb-cluster}

このセクションでは、TiDB クラスターをアップグレードし、アップグレード後のバージョンを確認する方法について説明します。

### TiDBクラスタを指定のバージョンにアップグレードする {#upgrade-the-tidb-cluster-to-a-specified-version}

クラスターは、オンライン アップグレードとオフライン アップグレードの 2 つの方法のいずれかでアップグレードできます。

デフォルトでは、 TiUP クラスタ はオンライン方式を使用して TiDB クラスターをアップグレードします。つまり、TiDB クラスターはアップグレード プロセス中でも引き続きサービスを提供できます。オンライン方式では、アップグレードと再起動の前に、各ノードでリーダーが 1 つずつ移行されます。そのため、大規模なクラスターの場合、アップグレード操作全体が完了するまでに長い時間がかかります。

アプリケーションに、メンテナンスのためにデータベースを停止するメンテナンス ウィンドウがある場合は、オフライン アップグレード メソッドを使用して、アップグレード操作を迅速に実行できます。

#### オンラインアップグレード {#online-upgrade}

```shell
tiup cluster upgrade <cluster-name> <version>
```

たとえば、クラスターを v8.1.0 にアップグレードする場合は、次のようにします。

```shell
tiup cluster upgrade <cluster-name> v8.1.0
```

> **注記：**
>
> -   オンライン アップグレードでは、すべてのコンポーネントが 1 つずつアップグレードされます。TiKV のアップグレード中、インスタンスを停止する前に、TiKV インスタンス内のすべてのリーダーが削除されます。デフォルトのタイムアウト時間は 5 分 (300 秒) です。このタイムアウト時間が経過すると、インスタンスは直接停止されます。
>
> -   `--force`パラメータを使用すると、リーダーを削除せずにクラスターをすぐにアップグレードできます。ただし、アップグレード中に発生したエラーは無視されるため、アップグレードの失敗は通知されません。したがって、 `--force`パラメータは慎重に使用してください。
>
> -   安定したパフォーマンスを維持するには、インスタンスを停止する前に、TiKV インスタンス内のすべてのリーダーが排除されていることを確認してください。1 `--transfer-timeout` `--transfer-timeout 3600` (単位: 秒) などのより大きな値に設定できます。
>
> -   TiFlashを v5.3.0 より前のバージョンから v5.3.0 以降にアップグレードするには、 TiFlashを停止してからアップグレードする必要があり、 TiUP のバージョンは v1.12.0 より前である必要があります。詳細については、 [TiUPを使用してTiFlashをアップグレードする](/tiflash-upgrade-guide.md#upgrade-tiflash-using-tiup)参照してください。
>
> -   TiDB Binlogを使用してクラスターにローリング更新を適用するときは、新しいクラスター化インデックス テーブルを作成しないようにしてください。

#### アップグレード中にコンポーネントのバージョンを指定する {#specify-the-component-version-during-upgrade}

tiup-cluster v1.14.0 以降では、クラスターのアップグレード中に特定のコンポーネントを特定のバージョンに指定できます。これらのコンポーネントは、別のバージョンを指定しない限り、後続のアップグレードでも固定バージョンのままになります。

> **注記：**
>
> TiDB、TiKV、PD、TiCDC など、バージョン番号を共有するコンポーネントについては、混合バージョンの展開シナリオで正しく動作することを確認するための完全なテストはありません。このセクションは、テスト環境でのみ使用するか、 [テクニカルサポート](/support.md)の助けを借りて使用してください。

```shell
tiup cluster upgrade -h | grep "version"
      --alertmanager-version string        Fix the version of alertmanager and no longer follows the cluster version.
      --blackbox-exporter-version string   Fix the version of blackbox-exporter and no longer follows the cluster version.
      --cdc-version string                 Fix the version of cdc and no longer follows the cluster version.
      --ignore-version-check               Ignore checking if target version is bigger than current version.
      --node-exporter-version string       Fix the version of node-exporter and no longer follows the cluster version.
      --pd-version string                  Fix the version of pd and no longer follows the cluster version.
      --tidb-dashboard-version string      Fix the version of tidb-dashboard and no longer follows the cluster version.
      --tiflash-version string             Fix the version of tiflash and no longer follows the cluster version.
      --tikv-cdc-version string            Fix the version of tikv-cdc and no longer follows the cluster version.
      --tikv-version string                Fix the version of tikv and no longer follows the cluster version.
      --tiproxy-version string             Fix the version of tiproxy and no longer follows the cluster version.
```

#### オフラインアップグレード {#offline-upgrade}

1.  オフライン アップグレードを行う前に、まずクラスター全体を停止する必要があります。

    ```shell
    tiup cluster stop <cluster-name>
    ```

2.  オフライン アップグレードを実行するには、 `upgrade`コマンドを`--offline`オプションとともに使用します。 `<cluster-name>`にはクラスターの名前を入力し、 `<version>`にはアップグレードするバージョン ( `v8.1.0`など) を入力します。

    ```shell
    tiup cluster upgrade <cluster-name> <version> --offline
    ```

3.  アップグレード後、クラスターは自動的に再起動されません。再起動するには、 `start`コマンドを使用する必要があります。

    ```shell
    tiup cluster start <cluster-name>
    ```

### クラスターのバージョンを確認する {#verify-the-cluster-version}

最新のクラスターバージョン`TiDB Version`を表示するには、 `display`コマンドを実行します。

```shell
tiup cluster display <cluster-name>
```

    Cluster type:       tidb
    Cluster name:       <cluster-name>
    Cluster version:    v8.1.0

## FAQ {#faq}

このセクションでは、 TiUPを使用して TiDB クラスターを更新するときに発生する一般的な問題について説明します。

### エラーが発生してアップグレードが中断された場合、このエラーを修正した後でアップグレードを再開するにはどうすればよいですか? {#if-an-error-occurs-and-the-upgrade-is-interrupted-how-to-resume-the-upgrade-after-fixing-this-error}

アップグレードを再開するには、 `tiup cluster upgrade`コマンドを再実行します。アップグレード操作により、以前にアップグレードされたノードが再起動されます。アップグレードされたノードを再起動したくない場合は、 `replay`サブコマンドを使用して操作を再試行します。

1.  操作記録を表示するには、 `tiup cluster audit`実行します。

    ```shell
    tiup cluster audit
    ```

    失敗したアップグレード操作レコードを見つけて、この操作レコードの ID を保持します。ID は次の手順の`<audit-id>`値です。

2.  対応する操作を再試行するには、 `tiup cluster replay <audit-id>`実行します。

    ```shell
    tiup cluster replay <audit-id>
    ```

### v6.2.0 以降のバージョンにアップグレードするときにアップグレードが停止する問題を修正するにはどうすればよいですか? {#how-to-fix-the-issue-that-the-upgrade-gets-stuck-when-upgrading-to-v6-2-0-or-later-versions}

v6.2.0 以降、TiDB では、 [同時実行DDLフレームワーク](/ddl-introduction.md#how-the-online-ddl-asynchronous-change-works-in-tidb)がデフォルトで同時 DDL を実行できるようになりました。このフレームワークでは、DDL ジョブstorageがKV キューからテーブル キューに変更されます。この変更により、一部のシナリオでアップグレードが停止する可能性があります。この問題を引き起こす可能性のあるシナリオと、それに対応する解決策を次に示します。

-   プラグインの読み込みによりアップグレードが停止する

    アップグレード中に、DDL ステートメントの実行を必要とする特定のプラグインをロードすると、アップグレードが停止する可能性があります。

    **解決策**: アップグレード中にプラグインをロードしないでください。代わりに、アップグレードが完了した後にのみプラグインをロードします。

-   オフラインアップグレードに`kill -9`コマンドを使用したため、アップグレードが停止しました

    -   注意事項: オフライン アップグレードを実行するために`kill -9`コマンドを使用しないでください。必要な場合は、2 分後に新しいバージョンの TiDB ノードを再起動してください。
    -   アップグレードがすでに停止している場合は、影響を受ける TiDB ノードを再起動します。問題が発生したばかりの場合は、2 分後にノードを再起動することをお勧めします。

-   DDL 所有者の変更によりアップグレードが停止する

    複数インスタンスのシナリオでは、ネットワークまたはハードウェアの障害により DDL 所有者が変更される可能性があります。アップグレード フェーズで未完了の DDL ステートメントがある場合、アップグレードが停止する可能性があります。

    **解決**：

    1.  スタックした TiDB ノードを終了します ( `kill -9`使用は避けてください)。
    2.  新しいバージョンの TiDB ノードを再起動します。

### アップグレード中にエビクト リーダーが長時間待機しました。この手順をスキップして迅速にアップグレードするにはどうすればよいでしょうか。 {#the-evict-leader-has-waited-too-long-during-the-upgrade-how-to-skip-this-step-for-a-quick-upgrade}

`--force`を指定できます。その場合、アップグレード中に PD リーダーの転送と TiKV リーダーの削除のプロセスがスキップされます。クラスターは直接再起動されてバージョンが更新されるため、オンラインで実行されるクラスターに大きな影響を与えます。次のコマンドでは、 `<version>`アップグレードするバージョンです (例: `v8.1.0` 。

```shell
tiup cluster upgrade <cluster-name> <version> --force
```

### TiDB クラスターをアップグレードした後、pd-ctl などのツールのバージョンを更新するにはどうすればよいですか? {#how-to-update-the-version-of-tools-such-as-pd-ctl-after-upgrading-the-tidb-cluster}

TiUPを使用して対応するバージョンの`ctl`コンポーネントをインストールすることで、ツールのバージョンをアップグレードできます。

```shell
tiup install ctl:v8.1.0
```
