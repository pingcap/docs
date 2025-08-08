---
title: Upgrade TiDB Using TiUP
summary: TiUPを使用して TiDB をアップグレードする方法を学びます。
---

# TiUPを使用して TiDB をアップグレードする {#upgrade-tidb-using-tiup}

このドキュメントは、次のバージョンから TiDB v8.5.x へのアップグレードに適用されます: v6.1.x、v6.5.x、v7.1.x、v7.5.x、v8.1.x、v8.2.0、v8.3.0、および v8.4.0

> **警告：**
>
> 1.  TiDBをアップグレードする前に、ご使用のオペレーティングシステムのバージョンが[OS and platform requirements](/hardware-and-software-requirements.md#os-and-platform-requirements)満たしていることを確認してください。CentOS Linux 7で稼働しているクラスタをv8.5にアップグレードする場合は、クラスタが利用できなくなるリスクを回避するため、TiDB v8.5.1以降のバージョンを使用してください。詳細については、 [TiDB v8.5.1 リリースノート](/releases/release-8.5.1.md)参照してください。
> 2.  TiFlash を5.3 より前のバージョンから 5.3 以降にオンラインでアップグレードすることはできません。まず、以前のバージョンのTiFlashインスタンスをすべて停止し、その後、クラスターをオフラインでアップグレードする必要があります。他のコンポーネント（TiDB や TiKV など）がオンラインアップグレードをサポートしていない場合は、 [オンラインアップグレード](#online-upgrade)の警告の手順に従ってください。
> 3.  アップグレードプロセス中はDDL文を実行**しないでください**。そうしないと、未定義の動作が発生する可能性があります。
> 4.  **DO NOT** upgrade a TiDB cluster when a DDL statement is being executed in the cluster (usually for the time-consuming DDL statements such as `ADD INDEX` and the column type changes). Before the upgrade, it is recommended to use the [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md) command to check whether the TiDB cluster has an ongoing DDL job. If the cluster has a DDL job, to upgrade the cluster, wait until the DDL execution is finished or use the [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md) command to cancel the DDL job before you upgrade the cluster.
> 5.  アップグレード前の TiDB バージョンが 7.1.0 以降の場合は、前述の警告 3 と 4 は無視できます。詳細については、 [TiDBスムーズアップグレードの使用に関する制限](/smooth-upgrade-tidb.md#limitations)参照してください。
> 6.  TiUPを使用して TiDB クラスターをアップグレードする前に、必ず[ユーザー操作の制限](/smooth-upgrade-tidb.md#limitations-on-user-operations)お読みください。

> **注記：**
>
> -   アップグレード対象のクラスターがバージョン6.2より前のバージョンの場合、一部のシナリオでは、クラスターをバージョン6.2以降にアップグレードすると、アップグレードが停止する可能性があります[How to fix the issue](#how-to-fix-the-issue-that-the-upgrade-gets-stuck-when-upgrading-to-v620-or-later-versions)を参照してください。
> -   TiDBノードは、構成項目[`server-version`](/tidb-configuration-file.md#server-version)の値を使用して現在のTiDBバージョンを確認します。そのため、予期しない動作を回避するには、TiDBクラスタをアップグレードする前に、値`server-version`を空または現在のTiDBクラスタの実際のバージョンに設定する必要があります。
> -   設定項目[`performance.force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v657-and-v710) `ON`に設定すると、TiDB の起動時間が長くなり、起動タイムアウトやアップグレード失敗が発生する可能性があります。この問題を回避するには、 TiUPの待機タイムアウトを長めに設定することをお勧めします。
>     -   Scenarios that might be affected:
>         -   元のクラスターバージョンは v6.5.7 および v7.1.0 ( `performance.force-init-stats`はまだサポートされていません) より前であり、ターゲットバージョンは v7.2.0 以降です。
>         -   元のクラスターのバージョンは v6.5.7 および v7.1.0 以上であり、 `performance.force-init-stats`構成項目は`ON`に設定されています。
>
>     -   `performance.force-init-stats`構成項目の値を確認します。
>
>             SHOW CONFIG WHERE type = 'tidb' AND name = 'performance.force-init-stats';
>
>     -   You can increase the TiUP waiting timeout by adding the command-line option [`--wait-timeout`](/tiup/tiup-component-cluster.md#--wait-timeout). For example, execute the following command to set the waiting timeout to 1200 seconds (20 minutes).
>
>         ```shell
>         tiup update cluster --wait-timeout 1200 [other options]
>         ```
>
>         一般的に、ほとんどのシナリオでは20分の待機タイムアウトで十分です。より正確な推定値を得るには、TiDBログで`init stats info time`検索し、前回の起動時の統計読み込み時間を参考にしてください。例えば、
>
>             [domain.go:2271] ["init stats info time"] [lite=true] ["take time"=2.151333ms]
>
>         元のクラスターがv7.1.0以前の場合、v7.2.0以降にアップグレードすると、 [`performance.lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710)の導入により統計情報の読み込み時間が大幅に短縮されます。この場合、アップグレード前の`init stats info time`アップグレード後の読み込み時間よりも長くなります。
>
>     -   If you want to shorten the rolling upgrade duration of TiDB and the potential performance impact of missing initial statistical information during the upgrade is acceptable for your cluster, you can set `performance.force-init-stats` to `OFF` before the upgrade by [TiUPを使用してターゲットインスタンスの構成を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration). After the upgrade is completed, you can reassess and revert this setting if necessary.

## アップグレードの注意事項 {#upgrade-caveat}

-   現在、TiDB は、アップグレード後のバージョンのダウングレードまたは以前のバージョンへのロールバックをサポートしていません。
-   Support upgrading the versions of TiCDC, TiFlash, and other components.
-   TiFlashをv6.3.0より前のバージョンからv6.3.0以降のバージョンにアップグレードする場合、CPUがLinux AMD64アーキテクチャではAVX2命令セット、Linux ARM64アーキテクチャではARMv8命令セットアーキテクチャをサポートしている必要があることに注意してください。詳細については、 [v6.3.0 リリースノート](/releases/release-6.3.0.md#others)の説明を参照してください。
-   各バージョン間の互換性に関する変更の詳細については、各バージョンの[リリースノート](/releases/release-notes.md)ご覧ください。対応するリリースノートの「互換性の変更」セクションに従って、クラスター構成を変更してください。
-   クラスターをv5.3より前のバージョンからv5.3以降のバージョンにアップデートする場合、デフォルトでデプロイされているPrometheusによって生成されるアラートの時刻形式が変更されていることにご注意ください。この形式の変更は、Prometheus v2.27.1から導入されています。詳細については、 [プロメテウスコミット](https://github.com/prometheus/prometheus/commit/7646cbca328278585be15fa615e22f2a50b47d06)ご覧ください。

## 準備 {#preparations}

This section introduces the preparation works needed before upgrading your TiDB cluster, including upgrading TiUP and the TiUP Cluster component.

### ステップ1: 互換性の変更を確認する {#step-1-review-compatibility-changes}

TiDB リリースノートで互換性の変更点をご確認ください。アップグレードに影響する変更点がある場合は、それに応じた対応を行ってください。

以下は、v8.4.0から最新バージョン（v8.5.2）にアップグレードする際に知っておくべきリリースノートです。v8.3.0以前のバージョンから最新バージョンにアップグレードする場合は、中間バージョン[リリースノート](/releases/release-notes.md)確認する必要があるかもしれません。

-   TiDB v8.5.0 [compatibility changes](/releases/release-8.5.0.md#compatibility-changes)
-   TiDB v8.5.1 [リリースノート](/releases/release-8.5.1.md)
-   TiDB v8.5.2 [リリースノート](/releases/release-8.5.2.md)

### ステップ2: TiUPまたはTiUPオフラインミラーをアップグレードする {#step-2-upgrade-tiup-or-tiup-offline-mirror}

TiDB クラスターをアップグレードする前に、まずTiUPまたはTiUPミラーをアップグレードする必要があります。

#### TiUPとTiUPクラスタのアップグレード {#upgrade-tiup-and-tiup-cluster}

> **注記：**
>
> アップグレードするクラスターの制御マシンが`https://tiup-mirrors.pingcap.com`アクセスできない場合は、このセクションをスキップして[TiUPオフラインミラーのアップグレード](#upgrade-tiup-offline-mirror)参照してください。

1.  TiUPのバージョンをアップグレードしてください。TiUPのバージョンは`1.11.3`以降が推奨されます。

    ```shell
    tiup update --self
    tiup --version
    ```

2.  TiUPクラスタのバージョンをアップグレードしてください。TiUPTiUPのバージョンは`1.11.3`以降が推奨されます。

    ```shell
    tiup update cluster
    tiup cluster --version
    ```

#### TiUPオフラインミラーのアップグレード {#upgrade-tiup-offline-mirror}

> **注記：**
>
> アップグレードするクラスターがオフライン方式を使用せずにデプロイされた場合は、この手順をスキップします。

[TiUPを使用して TiDBクラスタをデプロイ- TiUPをオフラインでデプロイ](/production-deployment-using-tiup.md#deploy-tiup-offline)を参照して、新しいバージョンのTiUPミラーをダウンロードし、制御マシンにアップロードしてください。3 `local_install.sh`実行すると、 TiUP は上書きアップグレードを完了します。

```shell
tar xzvf tidb-community-server-${version}-linux-amd64.tar.gz
sh tidb-community-server-${version}-linux-amd64/local_install.sh
source /home/tidb/.bash_profile
```

上書きアップグレード後、次のコマンドを実行して、サーバーとツールキットのオフライン ミラーをサーバーディレクトリにマージします。

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

Now, the offline mirror has been upgraded successfully. If an error occurs during TiUP operation after the overwriting, it might be that the `manifest` is not updated. You can try `rm -rf ~/.tiup/manifests/*` before running TiUP again.

### ステップ3: TiUPトポロジ構成ファイルを編集する {#step-3-edit-tiup-topology-configuration-file}

> **注記：**
>
> 次のいずれかの状況に該当する場合は、この手順をスキップしてください。
>
> -   元のクラスタの構成パラメータを変更していません。または、 `tiup cluster`使用して構成パラメータを変更しましたが、それ以上の変更は必要ありません。
> -   アップグレード後、変更されていない構成項目に対して、v8.5.2 のデフォルトのパラメータ値を使用します。

1.  トポロジファイルを編集するには、 `vi`編集モードに入ります。

    ```shell
    tiup cluster edit-config <cluster-name>
    ```

2.  [トポロジー](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml)構成テンプレートの形式を参照し、トポロジ ファイルの`server_configs`セクションに変更するパラメータを入力します。

3.  変更後、 <kbd>:</kbd> + <kbd>w</kbd> + <kbd>q</kbd>と入力して変更を保存し、編集モードを終了します。Y<kbd>と</kbd>入力して変更を確定します。

### ステップ4: クラスターのDDLとバックアップのステータスを確認する {#step-4-check-the-ddl-and-backup-status-of-the-cluster}

アップグレード中に未定義の動作やその他の予期しない問題を回避するために、アップグレード前に次の項目を確認することをお勧めします。

-   クラスタDDL:

    -   [スムーズなアップグレード](/smooth-upgrade-tidb.md)使用して TiDB を v8.1.0 以降にアップグレードし、 [Distributed eXecution Framework (DXF)](/tidb-distributed-execution-framework.md)有効になっている場合は、アップグレード前に DXF を無効にすることをお勧めします。そうしないと、アップグレードプロセス中に追加されたインデックスがデータと不整合になり、アップグレードが失敗する可能性があります。
    -   [スムーズなアップグレード](/smooth-upgrade-tidb.md)使用しない場合は、 [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md)ステートメントを使用して、実行中の DDL ジョブが存在するかどうかを確認することをお勧めします。実行中の DDL ジョブが存在する場合は、アップグレードを実行する前に、その実行が完了するまで待つか、 [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)ステートメントを使用してキャンセルしてください。

-   クラスタのバックアップ：クラスター内で実行中のバックアップまたは復元タスクがあるかどうかを確認するために、 [`SHOW [BACKUPS|RESTORES]`](/sql-statements/sql-statement-show-backups.md)ステートメントを実行することをお勧めします。実行中の場合は、アップグレードを実行する前に完了をお待ちください。

### ステップ5: 現在のクラスターのヘルスステータスを確認する {#step-5-check-the-health-status-of-the-current-cluster}

アップグレード中に未定義の動作やその他の問題が発生するのを避けるため、アップグレード前に現在のクラスタのリージョンのヘルスステータスを確認することをお勧めします。そのためには、サブコマンド`check`を使用します。

```shell
tiup cluster check <cluster-name> --cluster
```

コマンドを実行すると、「リージョンステータス」のチェック結果が出力されます。

-   結果が「すべてのリージョンが正常です」の場合、現在のクラスター内のすべてのリージョンが正常であるため、アップグレードを続行できます。
-   結果が「リージョンが完全に正常ではありません: m 個のミスピア、n 個の保留中のピア」で、「他の操作を行う前に、異常なリージョンを修正してください。」というプロンプトが表示される場合、現在のクラスター内の一部のリージョンに異常があります。チェック結果が「すべてのリージョンが正常です」になるまで、異常をトラブルシューティングする必要があります。その後、アップグレードを続行できます。

## TiDBクラスタをアップグレードする {#upgrade-the-tidb-cluster}

このセクションでは、TiDB クラスターをアップグレードし、アップグレード後のバージョンを確認する方法について説明します。

### Upgrade the TiDB cluster to a specified version {#upgrade-the-tidb-cluster-to-a-specified-version}

クラスターは、オンライン アップグレードとオフライン アップグレードのいずれかの方法でアップグレードできます。

TiUP クラスタはデフォルトでオンライン方式を使用してTiDBクラスタをアップグレードします。つまり、アップグレードプロセス中もTiDBクラスタはサービスを提供し続けることができます。オンライン方式では、アップグレードと再起動の前に、各ノードのリーダーが1つずつ移行されます。そのため、大規模なクラスタでは、アップグレード操作全体を完了するのに長い時間がかかります。

アプリケーションに、メンテナンスのためにデータベースを停止するメンテナンス ウィンドウがある場合は、オフライン アップグレード方式を使用して、アップグレード操作を迅速に実行できます。

#### オンラインアップグレード {#online-upgrade}

```shell
tiup cluster upgrade <cluster-name> <version>
```

たとえば、クラスターを v8.5.2 にアップグレードする場合は、次のようにします。

```shell
tiup cluster upgrade <cluster-name> v8.5.2
```

> **注記：**
>
> -   オンラインアップグレードでは、すべてのコンポーネントが1つずつアップグレードされます。TiKVのアップグレード中は、インスタンスを停止する前に、TiKVインスタンス内のすべてのリーダーが強制的にエビクションされます。デフォルトのタイムアウト時間は5分（300秒）です。このタイムアウト時間が経過すると、インスタンスは直ちに停止されます。
>
> -   `--force`のパラメータを使用すると、リーダーノードを退去させることなく、クラスターを直ちにアップグレードできます。ただし、アップグレード中に発生したエラーは無視されるため、アップグレードの失敗は通知されません。そのため、 `--force`パラメータは慎重に使用してください。
>
> -   安定したパフォーマンスを維持するには、TiKVインスタンスを停止する前に、すべてのリーダーが排除されていることを確認してください。1 `--transfer-timeout` `--transfer-timeout 3600` （単位：秒）などの大きな値に設定することもできます。
>
> -   TiFlashをv5.3.0より前のバージョンからv5.3.0以降にアップグレードするには、 TiFlashを停止してからアップグレードする必要があります。また、 TiUPのバージョンはv1.12.0より前である必要があります。詳細については、 [TiUPを使用してTiFlashをアップグレードする](/tiflash-upgrade-guide.md#upgrade-tiflash-using-tiup)参照してください。

#### アップグレード中にコンポーネントのバージョンを指定する {#specify-the-component-version-during-upgrade}

tiup-cluster v1.14.0以降では、クラスタのアップグレード時に特定のコンポーネントを特定のバージョンに指定できます。これらのコンポーネントは、別のバージョンを指定しない限り、以降のアップグレードでも固定バージョンのままになります。

> **注記：**
>
> TiDB、TiKV、PD、TiCDC など、バージョン番号を共有するコンポーネントについては、混在バージョンのデプロイメントシナリオで正常に動作することを保証するための完全なテストは用意されていません。このセクションはテスト環境でのみ使用するか、 [テクニカルサポート](/support.md)の支援を受けて使用してください。

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

2.  オフラインアップグレードを実行するには、 `upgrade`コマンドに`--offline`オプションを付けて実行します。 `<cluster-name>`にはクラスター名を、 `<version>`にはアップグレードするバージョン（例： `v8.5.2` ）を入力してください。

    ```shell
    tiup cluster upgrade <cluster-name> <version> --offline
    ```

3.  アップグレード後、クラスターは自動的に再起動されません。再起動するには、 `start`コマンドを使用する必要があります。

    ```shell
    tiup cluster start <cluster-name>
    ```

### クラスタのバージョンを確認する {#verify-the-cluster-version}

最新のクラスター バージョン`TiDB Version`表示するには、コマンド`display`を実行します。

```shell
tiup cluster display <cluster-name>
```

    Cluster type:       tidb
    Cluster name:       <cluster-name>
    Cluster version:    v8.5.2

## FAQ {#faq}

このセクションでは、 TiUPを使用して TiDB クラスターを更新するときに発生する一般的な問題について説明します。

### エラーが発生してアップグレードが中断された場合、このエラーを修正した後でアップグレードを再開するにはどうすればよいですか? {#if-an-error-occurs-and-the-upgrade-is-interrupted-how-to-resume-the-upgrade-after-fixing-this-error}

アップグレードを再開するには、 `tiup cluster upgrade`コマンドを再実行してください。アップグレード操作により、以前にアップグレードされたノードが再起動されます。アップグレードされたノードを再起動したくない場合は、 `replay`番目のサブコマンドを使用して操作を再試行してください。

1.  操作記録を表示するには、 `tiup cluster audit`実行します。

    ```shell
    tiup cluster audit
    ```

    失敗したアップグレード操作レコードを見つけ、その操作レコードのIDを控えておきます。このIDは次のステップで`<audit-id>`値として使用されます。

2.  対応する操作を再試行するには、 `tiup cluster replay <audit-id>`実行します。

    ```shell
    tiup cluster replay <audit-id>
    ```

### v6.2.0 以降のバージョンにアップグレードするときにアップグレードが停止する問題を修正するにはどうすればよいですか? {#how-to-fix-the-issue-that-the-upgrade-gets-stuck-when-upgrading-to-v6-2-0-or-later-versions}

Starting from v6.2.0, TiDB enables the [並行DDLフレームワーク](/ddl-introduction.md#how-the-online-ddl-asynchronous-change-works-in-tidb) by default to execute concurrent DDLs. This framework changes the DDL job storage from a KV queue to a table queue. This change might cause the upgrade to get stuck in some scenarios. The following are some scenarios that might trigger this issue and the corresponding solutions:

-   Upgrade gets stuck due to plugin loading

    アップグレード中に、DDL ステートメントの実行を必要とする特定のプラグインをロードすると、アップグレードが停止する可能性があります。

    **解決策**：アップグレード中はプラグインの読み込みを避け、アップグレードが完了した後にのみプラグインを読み込みましょう。

-   オフラインアップグレードに`kill -9`コマンドを使用したためにアップグレードが停止する

    -   注意：オフラインアップグレードを実行する際にコマンド`kill -9`使用は避けてください。必要な場合は、2分後に新しいバージョンのTiDBノードを再起動してください。
    -   アップグレードが既に停止している場合は、影響を受けるTiDBノードを再起動してください。問題が発生した直後の場合は、2分後にノードを再起動することをお勧めします。

-   DDL 所有者の変更によりアップグレードが停止する

    複数インスタンスのシナリオでは、ネットワークまたはハードウェア障害によりDDL所有者が変更される可能性があります。アップグレードフェーズで未完了のDDLステートメントがある場合、アップグレードが停止する可能性があります。

    **Solution**:

    1.  スタックした TiDB ノードを終了します ( `kill -9`使用は避けてください)。
    2.  Restart the new version TiDB node.

### アップグレード中にエビクトリーダーの待機時間が長すぎます。この手順をスキップして迅速にアップグレードするにはどうすればよいですか？ {#the-evict-leader-has-waited-too-long-during-the-upgrade-how-to-skip-this-step-for-a-quick-upgrade}

`--force`指定することもできます。その場合、アップグレード中にPDリーダーの移行とTiKVリーダーの削除のプロセスがスキップされます。バージョンを更新するためにクラスターが直接再起動されるため、オンラインで稼働しているクラスターに大きな影響を与えます。以下のコマンドでは、 `<version>`アップグレードするバージョン（例： `v8.5.2` ）です。

```shell
tiup cluster upgrade <cluster-name> <version> --force
```

### TiDB クラスターをアップグレードした後、pd-ctl などのツールのバージョンを更新するにはどうすればよいですか? {#how-to-update-the-version-of-tools-such-as-pd-ctl-after-upgrading-the-tidb-cluster}

TiUPを使用して対応するバージョンの`ctl`コンポーネントをインストールすることで、ツールのバージョンをアップグレードできます。

```shell
tiup install ctl:v8.5.2
```
