---
title: Upgrade TiDB Using TiUP
summary: TiUPを使用して TiDB をアップグレードする方法を学びます。
---

# TiUPを使用して TiDB をアップグレードする {#upgrade-tidb-using-tiup}

このドキュメントは、v6.1.x、v6.5.x、v7.1.x、v7.5.x、v8.1.x、v8.2.0、v8.3.0、および v8.4.0 から TiDB v8.5.x へのアップグレードに適用されます。

> **警告：**
>
> 1.  TiDBをアップグレードする前に、オペレーティングシステムのバージョンが[OSおよびプラットフォームの要件](/hardware-and-software-requirements.md#os-and-platform-requirements)を満たしていることを確認してください。CentOS Linux 7で稼働しているクラスタをv8.5にアップグレードする場合は、クラスタが利用できなくなるリスクを回避するため、TiDB v8.5.1以降のバージョンを使用してください。詳細については、 [TiDB v8.5.1 リリースノート](/releases/release-8.5.1.md)参照してください。
> 2.  TiFlash を5.3 より前のバージョンから 5.3 以降にオンラインでアップグレードすることはできません。まず、以前のバージョンのTiFlashインスタンスをすべて停止し、その後、クラスターをオフラインでアップグレードする必要があります。他のコンポーネント（TiDB や TiKV など）がオンラインアップグレードをサポートしていない場合は、 [オンラインアップグレード](#online-upgrade)の警告の手順に従ってください。
> 3.  アップグレードプロセス中はDDLステートメントを実行**しないでください**。そうしないと、未定義の動作が発生する可能性があります。
> 4.  クラスター内でDDL文が実行されている間（通常は、 `ADD INDEX`や列型の変更などの時間のかかるDDL文の実行中）は、TiDBクラスターをアップグレード**しないでください**。アップグレード前に、 [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md)コマンドを使用して、TiDBクラスターで実行中のDDLジョブがあるかどうかを確認することをお勧めします。クラスターにDDLジョブがある場合は、クラスターをアップグレードする前に、DDLの実行が完了するまで待つか、 [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)コマンドを使用してDDLジョブをキャンセルしてください。
> 5.  アップグレード前の TiDB バージョンが 7.1.0 以降の場合は、前述の警告 3 と 4 を無視できます。詳細については、 [TiDBスムーズアップグレードの使用に関する制限](/smooth-upgrade-tidb.md#limitations)参照してください。
> 6.  TiUPを使用して TiDB クラスターをアップグレードする前に、必ず[ユーザー操作の制限](/smooth-upgrade-tidb.md#limitations-on-user-operations)お読みください。

> **注記：**
>
> -   アップグレード対象のクラスターがv6.2より前のバージョンの場合、一部のシナリオではクラスターをv6.2以降のバージョンにアップグレードすると、アップグレードが停止する可能性があります[問題を解決する方法](#how-to-fix-the-issue-that-the-upgrade-gets-stuck-when-upgrading-to-v620-or-later-versions)を参照してください。
> -   TiDBノードは、設定項目[`server-version`](/tidb-configuration-file.md#server-version)の値を使用して現在のTiDBバージョンを確認します。そのため、予期しない動作を回避するには、TiDBクラスタをアップグレードする前に、設定項目`server-version`の値を空の値、または現在のTiDBクラスタの実際のバージョンに設定する必要があります。
> -   設定項目[`performance.force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v657-and-v710) `ON`に設定すると、TiDB の起動時間が長くなり、起動タイムアウトやアップグレード失敗が発生する可能性があります。この問題を回避するには、 TiUPの待機タイムアウトを長めに設定することをお勧めします。
>     -   影響を受ける可能性のあるシナリオ:
>         -   元のクラスターバージョンは v6.5.7 および v7.1.0 (まだ`performance.force-init-stats`サポートしていません) より前であり、ターゲットバージョンは v7.2.0 以降です。
>         -   元のクラスターのバージョンは v6.5.7 および v7.1.0 以上であり、 `performance.force-init-stats`構成項目は`ON`に設定されています。
>
>     -   `performance.force-init-stats`構成項目の値を確認します。
>
>             SHOW CONFIG WHERE type = 'tidb' AND name = 'performance.force-init-stats';
>
>     -   コマンドラインオプション[`--wait-timeout`](/tiup/tiup-component-cluster.md#--wait-timeout)を追加することで、 TiUP の待機タイムアウトを長くすることができます。例えば、以下のコマンドを実行すると、待機タイムアウトが 1200 秒（20 分）に設定されます。
>
>         ```shell
>         tiup update cluster --wait-timeout 1200 [other options]
>         ```
>
>         一般的に、ほとんどのシナリオでは20分の待機タイムアウトで十分です。より正確な推定値を得るには、TiDBログで`init stats info time`を検索し、前回の起動時の統計情報の読み込み時間を参考にしてください。例えば、
>
>             [domain.go:2271] ["init stats info time"] [lite=true] ["take time"=2.151333ms]
>
>         元のクラスターがv7.1.0以前の場合、v7.2.0以降にアップグレードすると、 [`performance.lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710)の導入により統計情報の読み込み時間が大幅に短縮されます。この場合、アップグレード前の`init stats info time`アップグレード後の読み込み時間よりも長くなります。
>
>     -   TiDBのローリングアップグレード期間を短縮したい場合、かつアップグレード中に初期統計情報が失われることによるパフォーマンスへの影響がクラスターにとって許容範囲内であれば、アップグレード前に`performance.force-init-stats`を`OFF`に設定し、 [TiUPを使用してターゲットインスタンスの構成を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)を加算することができます。アップグレードが完了したら、必要に応じてこの設定を再評価し、元に戻すことができます。

## アップグレードの注意事項 {#upgrade-caveat}

-   現在、TiDB はバージョンのダウングレードやアップグレード後の以前のバージョンへのロールバックをサポートしていません。
-   TiCDC、 TiFlash、およびその他のコンポーネントのバージョンのアップグレードをサポートします。
-   TiFlashをv6.3.0より前のバージョンからv6.3.0以降のバージョンにアップグレードする場合、CPUがLinux AMD64アーキテクチャではAVX2命令セット、Linux ARM64アーキテクチャではARMv8命令セットアーキテクチャをサポートしている必要があることに注意してください。詳細については、 [v6.3.0 リリースノート](/releases/release-6.3.0.md#others)の説明を参照してください。
-   各バージョン間の互換性に関する変更の詳細については、各バージョンの[リリースノート](/releases/release-notes.md)ご覧ください。対応するリリースノートの「互換性に関する変更」セクションに従って、クラスター構成を変更してください。
-   クラスターをv5.3より前のバージョンからv5.3以降のバージョンにアップデートする場合、デフォルトでデプロイされているPrometheusによって生成されるアラートの時刻形式が変更されていることにご注意ください。この形式の変更は、Prometheus v2.27.1以降で導入されています。詳細については、 [プロメテウスコミット](https://github.com/prometheus/prometheus/commit/7646cbca328278585be15fa615e22f2a50b47d06)ご覧ください。

## 準備 {#preparations}

このセクションでは、 TiUPおよびTiUPクラスタコンポーネントのアップグレードなど、TiDB クラスターをアップグレードする前に必要な準備作業について説明します。

### ステップ1: 互換性の変更を確認する {#step-1-review-compatibility-changes}

TiDB リリースノートで互換性の変更点をご確認ください。アップグレードに影響する変更点がある場合は、それに応じた対応を行ってください。

以下は、v8.4.0から最新バージョン（v8.5.5）にアップグレードする際に知っておくべきリリースノートです。v8.3.0以前のバージョンから最新バージョンにアップグレードする場合は、中間バージョン[リリースノート](/releases/release-notes.md)も確認する必要があるかもしれません。

-   TiDB v8.5.0 [互換性の変更](/releases/release-8.5.0.md#compatibility-changes)
-   TiDB v8.5.1 [リリースノート](/releases/release-8.5.1.md)
-   TiDB v8.5.2 [リリースノート](/releases/release-8.5.2.md)
-   TiDB v8.5.3 [互換性の変更](/releases/release-8.5.3.md#compatibility-changes)
-   TiDB v8.5.4 [互換性の変更](/releases/release-8.5.4.md#compatibility-changes)
-   TiDB v8.5.5 [互換性の変更](https://docs.pingcap.com/tidb/v8.5/release-8.5.5/#compatibility-changes)

### ステップ2: TiUPまたはTiUPオフラインミラーをアップグレードする {#step-2-upgrade-tiup-or-tiup-offline-mirror}

TiDB クラスターをアップグレードする前に、まずTiUPまたはTiUPミラーをアップグレードする必要があります。

#### TiUPとTiUP クラスタのアップグレード {#upgrade-tiup-and-tiup-cluster}

> **注記：**
>
> アップグレードするクラスターの制御マシンが`https://tiup-mirrors.pingcap.com`アクセスできない場合は、このセクションをスキップして[TiUPオフラインミラーのアップグレード](#upgrade-tiup-offline-mirror)参照してください。

1.  TiUPのバージョンをアップグレードしてください。TiUPのバージョンは`1.11.3`以降が推奨されます。

    ```shell
    tiup update --self
    tiup --version
    ```

2.  TiUPクラスタのバージョンをアップグレードしてください。TiUPクラスタのTiUPは`1.11.3`以降が推奨されます。

    ```shell
    tiup update cluster
    tiup cluster --version
    ```

#### TiUPオフラインミラーのアップグレード {#upgrade-tiup-offline-mirror}

> **注記：**
>
> アップグレードするクラスターがオフライン方式を使用せずにデプロイされた場合は、この手順をスキップします。

[TiUPを使用して TiDBクラスタをデプロイ- TiUP をオフラインでデプロイ](/production-deployment-using-tiup.md#deploy-tiup-offline)を参照して、新しいバージョンのTiUPミラーをダウンロードし、制御マシンにアップロードしてください。3 `local_install.sh`実行すると、 TiUP は上書きアップグレードを完了します。

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

これで、オフラインミラーのアップグレードは正常に完了しました。上書き後のTiUP操作中にエラーが発生した場合は、 `manifest`が更新されていない可能性があります。TiUPを再度実行する前に、 `rm -rf ~/.tiup/manifests/*`試してください。

### ステップ3: TiUPトポロジ構成ファイルを編集する {#step-3-edit-tiup-topology-configuration-file}

> **注記：**
>
> 次のいずれかの状況に該当する場合は、この手順をスキップしてください。
>
> -   元のクラスタの構成パラメータを変更していません。または、 `tiup cluster`使用して構成パラメータを変更しましたが、それ以上の変更は必要ありません。
> -   アップグレード後、変更されていない構成項目に対して、v8.5.5 のデフォルトのパラメータ値を使用します。

1.  トポロジファイルを編集するには、 `vi`編集モードに入ります。

    ```shell
    tiup cluster edit-config <cluster-name>
    ```

2.  [トポロジー](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml)構成テンプレートの形式を参照し、トポロジ ファイルの`server_configs`セクションに変更するパラメータを入力します。

3.  変更後、 <kbd>:</kbd> + <kbd>w</kbd> + <kbd>q</kbd>と入力して変更を保存し、編集モードを終了します。Y<kbd>と</kbd>入力して変更を確定します。

### ステップ4: クラスターのDDLとバックアップのステータスを確認する {#step-4-check-the-ddl-and-backup-status-of-the-cluster}

アップグレード中に未定義の動作やその他の予期しない問題を回避するために、アップグレード前に次の項目を確認することをお勧めします。

-   クラスタDDL:

    -   [スムーズなアップグレード](/smooth-upgrade-tidb.md)使用して TiDB を v8.1.0 以降にアップグレードし、 [分散実行フレームワーク (DXF)](/tidb-distributed-execution-framework.md)が有効になっている場合は、アップグレード前に DXF を無効にすることをお勧めします。そうしないと、アップグレードプロセス中に追加されたインデックスがデータと不整合になり、アップグレードが失敗する可能性があります。
    -   [スムーズなアップグレード](/smooth-upgrade-tidb.md)使用しない場合は、 [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md)ステートメントを使用して実行中の DDL ジョブが存在するかどうかを確認することをお勧めします。実行中の DDL ジョブが存在する場合は、アップグレードを実行する前に、その実行が完了するまで待つか、 [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)ステートメントを使用してキャンセルしてください。

-   クラスタのバックアップ：クラスター内で実行中のバックアップまたは復元タスクがあるかどうかを確認するために、 [`SHOW [BACKUPS|RESTORES]`](/sql-statements/sql-statement-show-backups.md)のステートメントを実行することをお勧めします。実行中のタスクがある場合は、アップグレードを実行する前に完了を待ってください。

### ステップ5: 現在のクラスターのヘルスステータスを確認する {#step-5-check-the-health-status-of-the-current-cluster}

アップグレード中に未定義の動作やその他の問題が発生するのを避けるため、アップグレード前に現在のクラスターのリージョンのヘルスステータスを確認することをお勧めします。そのためには、 `check`サブコマンドを使用します。

```shell
tiup cluster check <cluster-name> --cluster
```

コマンドを実行すると、「リージョンステータス」のチェック結果が出力されます。

-   結果が「すべてのリージョンが正常です」の場合、現在のクラスター内のすべてのリージョンが正常であるため、アップグレードを続行できます。
-   結果が「リージョンが完全に正常ではありません: m 個のミスピア、n 個の保留中のピア」で、「他の操作を行う前に、異常なリージョンを修正してください。」というプロンプトが表示される場合、現在のクラスター内の一部のリージョンに異常があります。チェック結果が「すべてのリージョンが正常です」になるまで、異常をトラブルシューティングする必要があります。その後、アップグレードを続行できます。

## TiDBクラスタをアップグレードする {#upgrade-the-tidb-cluster}

このセクションでは、TiDB クラスターをアップグレードし、アップグレード後のバージョンを確認する方法について説明します。

### TiDBクラスタを指定のバージョンにアップグレードする {#upgrade-the-tidb-cluster-to-a-specified-version}

クラスターは、オンライン アップグレードとオフライン アップグレードのいずれかの方法でアップグレードできます。

TiUP クラスタはデフォルトでオンライン方式を使用してTiDBクラスタをアップグレードします。つまり、アップグレードプロセス中もTiDBクラスタはサービスを提供し続けることができます。オンライン方式では、アップグレードと再起動の前に、各ノードでリーダーノードが1つずつ移行されます。そのため、大規模なクラスタでは、アップグレード操作全体を完了するのに長い時間がかかります。

アプリケーションに、メンテナンスのためにデータベースを停止するメンテナンス ウィンドウがある場合は、オフライン アップグレード方式を使用して、アップグレード操作を迅速に実行できます。

#### オンラインアップグレード {#online-upgrade}

```shell
tiup cluster upgrade <cluster-name> <version>
```

たとえば、クラスターを v8.5.5 にアップグレードする場合は、次のようにします。

```shell
tiup cluster upgrade <cluster-name> v8.5.5
```

> **注記：**
>
> -   オンラインアップグレードでは、すべてのコンポーネントが1つずつアップグレードされます。TiKVのアップグレード中は、インスタンスを停止する前に、TiKVインスタンス内のすべてのリーダーが強制的にエビクションされます。デフォルトのタイムアウト時間は5分（300秒）です。このタイムアウト時間が経過すると、インスタンスは直ちに停止されます。
>
> -   `--force`のパラメータを使用すると、リーダーノードを退去させることなくクラスターを即時にアップグレードできます。ただし、アップグレード中に発生したエラーは無視されるため、アップグレードの失敗は通知されません。そのため、 `--force`パラメータは慎重に使用してください。
>
> -   安定したパフォーマンスを維持するには、TiKVインスタンスを停止する前に、インスタンス内のすべてのリーダーが排除されていることを確認してください。1 `--transfer-timeout`より大きな値、例えば`--transfer-timeout 3600` （単位：秒）に設定することもできます。
>
> -   TiFlashをv5.3.0より前のバージョンからv5.3.0以降にアップグレードするには、 TiFlashを停止してからアップグレードする必要があります。また、 TiUPのバージョンはv1.12.0より前である必要があります。詳細については、 [TiUPを使用してTiFlashをアップグレードする](/tiflash-upgrade-guide.md#upgrade-tiflash-using-tiup)参照してください。

#### アップグレード中にコンポーネントのバージョンを指定する {#specify-the-component-version-during-upgrade}

tiup-cluster v1.14.0以降では、クラスタのアップグレード時に特定のコンポーネントを特定のバージョンに指定できます。これらのコンポーネントは、別のバージョンを指定しない限り、以降のアップグレードでも固定バージョンのままになります。

> **注記：**
>
> TiDB、TiKV、PD、TiCDC など、バージョン番号を共有するコンポーネントについては、混在バージョンのデプロイメントシナリオで正常に動作することを保証するための完全なテストは存在しません。このセクションは、テスト環境でのみ使用するか、 [テクニカルサポート](/support.md)の支援を受けて使用してください。

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

1.  オフライン アップグレードを実行する前に、まずクラスター全体を停止する必要があります。

    ```shell
    tiup cluster stop <cluster-name>
    ```

2.  オフラインアップグレードを実行するには、 `upgrade`コマンドに`--offline`オプションを付けて実行します。 `<cluster-name>`にはクラスター名を、 `<version>`にはアップグレードするバージョン（例： `v8.5.5`を入力します。

    ```shell
    tiup cluster upgrade <cluster-name> <version> --offline
    ```

3.  アップグレード後、クラスターは自動的に再起動されません。再起動するには、 `start`コマンドを使用する必要があります。

    ```shell
    tiup cluster start <cluster-name>
    ```

### クラスタのバージョンを確認する {#verify-the-cluster-version}

最新のクラスターバージョン`TiDB Version`を表示するには、 `display`コマンドを実行します。

```shell
tiup cluster display <cluster-name>
```

    Cluster type:       tidb
    Cluster name:       <cluster-name>
    Cluster version:    v8.5.5

## FAQ {#faq}

このセクションでは、 TiUPを使用して TiDB クラスターを更新するときに発生する一般的な問題について説明します。

### エラーが発生してアップグレードが中断された場合、このエラーを修正した後でアップグレードを再開するにはどうすればよいですか? {#if-an-error-occurs-and-the-upgrade-is-interrupted-how-to-resume-the-upgrade-after-fixing-this-error}

アップグレードを再開するには、 `tiup cluster upgrade`コマンドを再実行してください。アップグレード操作により、以前にアップグレードされたノードが再起動されます。アップグレードされたノードを再起動したくない場合は、 `replay`サブコマンドを使用して操作を再試行してください。

1.  操作記録を表示するには、 `tiup cluster audit`実行します。

    ```shell
    tiup cluster audit
    ```

    失敗したアップグレード操作レコードを見つけ、その操作レコードのIDを控えておきます。このIDは次のステップで`<audit-id>`値として使用されます。

2.  対応する操作を再試行するには`tiup cluster replay <audit-id>`実行します。

    ```shell
    tiup cluster replay <audit-id>
    ```

### v6.2.0 以降のバージョンにアップグレードするときにアップグレードが停止する問題を修正するにはどうすればよいですか? {#how-to-fix-the-issue-that-the-upgrade-gets-stuck-when-upgrading-to-v6-2-0-or-later-versions}

v6.2.0以降、TiDBはデフォルトで[並行DDLフレームワーク](/ddl-introduction.md#how-the-online-ddl-asynchronous-change-works-in-tidb)による同時DDL実行を有効にします。このフレームワークにより、DDLジョブのstorageがKVキューからテーブルキューに変更されます。この変更により、一部のシナリオでアップグレードが停止する可能性があります。この問題を引き起こす可能性のあるシナリオと、それに対応する解決策を以下に示します。

-   プラグインの読み込みによりアップグレードが停止する

    アップグレード中に、DDL ステートメントの実行を必要とする特定のプラグインをロードすると、アップグレードが停止する可能性があります。

    **解決策**：アップグレード中はプラグインの読み込みを避け、アップグレードが完了した後にのみプラグインを読み込みましょう。

-   オフラインアップグレードに`kill -9`コマンドを使用したため、アップグレードが停止しました

    -   注意：オフラインアップグレードを実行する際にコマンド`kill -9`使用は避けてください。必要な場合は、2分後に新しいバージョンのTiDBノードを再起動してください。
    -   アップグレードが既に停止している場合は、影響を受けるTiDBノードを再起動してください。問題が発生した直後の場合は、2分後にノードを再起動することをお勧めします。

-   DDL 所有者の変更によりアップグレードが停止する

    複数インスタンスのシナリオでは、ネットワークまたはハードウェア障害によりDDL所有者が変更される可能性があります。アップグレードフェーズで未完了のDDLステートメントがある場合、アップグレードが停止する可能性があります。

    **解決**：

    1.  スタックした TiDB ノードを終了します ( `kill -9`使用は避けてください)。
    2.  新しいバージョンの TiDB ノードを再起動します。

### アップグレード中にエビクトリーダーの待機時間が長すぎます。このステップをスキップして迅速にアップグレードするにはどうすればよいですか？ {#the-evict-leader-has-waited-too-long-during-the-upgrade-how-to-skip-this-step-for-a-quick-upgrade}

`--force`指定することもできます。その場合、アップグレード中に PD リーダーの移行と TiKV リーダーの削除のプロセスがスキップされます。バージョンを更新するためにクラスターが直接再起動されるため、オンラインで稼働しているクラスターに大きな影響を与えます。以下のコマンドでは、 `<version>`アップグレードするバージョン（例： `v8.5.5` ）です。

```shell
tiup cluster upgrade <cluster-name> <version> --force
```

### TiDB クラスターをアップグレードした後、pd-ctl などのツールのバージョンを更新するにはどうすればよいですか? {#how-to-update-the-version-of-tools-such-as-pd-ctl-after-upgrading-the-tidb-cluster}

TiUPを使用して対応するバージョンの`ctl`コンポーネントをインストールすることで、ツールのバージョンをアップグレードできます。

```shell
tiup install ctl:v8.5.5
```
