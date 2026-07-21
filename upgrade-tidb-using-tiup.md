---
title: Upgrade TiDB Using TiUP
summary: TiUPを使用してTiDBをアップグレードする方法を学びましょう。
---

# TiUPを使用してTiDBをアップグレードする {#upgrade-tidb-using-tiup}

このドキュメントは、TiDB v8.5.x へのアップグレードに適用されます。アップグレード対象バージョンは、v6.1.x、v6.5.x、v7.1.x、v7.5.x、v8.1.x、v8.2.0、v8.3.0、v8.4.0 です。

> **Warning:**
>
> 1.  TiDB をアップグレードする前に、オペレーティング システムのバージョンが[OSおよびプラットフォームの要件](/hardware-and-software-requirements.md#os-and-platform-requirements)を満たしていることを確認してください。 CentOS Linux 7 で実行されているクラスターを v8.5 にアップグレードする場合は、クラスターが使用できなくなるリスクを避けるために、必ず TiDB v8.5.1 以降のバージョンを使用してください。詳細については、 [TiDB v8.5.1 リリースノート](/releases/release-8.5.1.md)を参照してください。
> 2.  TiFlash を5.3 より前のバージョンから 5.3 以降にオンラインでアップグレードすることはできません。代わりに、まず以前のバージョンのTiFlashインスタンスをすべて停止し、その後オフラインでクラスタをアップグレードする必要があります。TiDB や TiKV などの他のコンポーネントがオンラインアップグレードをサポートしていない場合は、[オンラインアップグレード](#online-upgrade)の警告の手順に従ってください。 。
> 3.  アップグレード処理中はDDLステートメントを実行**しないでください**。実行すると、未定義の動作が発生する可能性があります。
> 4.  TiDB クラスターで DDL ステートメントが実行されている間は、クラスターをアップグレード**しないでください**(通常、 `ADD INDEX`や列型の変更など、時間のかかる DDL ステートメントの場合)。アップグレードの前に、 [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md)コマンドを使用して、TiDB クラスターで DDL ジョブが実行中かどうかを確認することをお勧めします。クラスターで DDL ジョブが実行されている場合は、クラスターをアップグレードする前に、DDL の実行が完了するまで待つか、 [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)コマンドを使用して DDL ジョブをキャンセルしてください。
> 5.  アップグレード前の TiDB バージョンが 7.1.0 以降の場合は、前述の警告 3 と 4 を無視してかまいません。詳細については、 [TiDB スムーズアップグレードの使用に関する制限](/smooth-upgrade-tidb.md#limitations)を参照してください。
> 6.  TiUPを使用して TiDB クラスターをアップグレードする前に、 [ユーザー操作に関する制限](/smooth-upgrade-tidb.md#limitations-on-user-operations)を必ずお読みください。

> **Note:**
>
> -   アップグレードするクラスターが v6.2 より前の場合、シナリオによってはクラスターを v6.2 以降のバージョンにアップグレードすると、アップグレードが停止する可能性があります。 [問題を解決する方法](#how-to-fix-the-issue-that-the-upgrade-gets-stuck-when-upgrading-to-v620-or-later-versions)を参照してください。
> -   TiDBノードは[`server-version`](/tidb-configuration-file.md#server-version)構成項目の値を使用して現在のTiDBバージョンを確認します。そのため、予期しない動作を避けるため、TiDBクラスタをアップグレードする前に、 `server-version`の値を空にするか、現在のTiDBクラスタの実際のバージョンに設定する必要があります。
> -   [`performance.force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v657-and-v710)設定項目を`ON`に設定すると、TiDB の起動時間が長くなり、起動タイムアウトやアップグレードの失敗が発生する可能性があります。この問題を回避するには、 TiUPの待機タイムアウトを長く設定することをお勧めします。
>     -   影響を受ける可能性のあるシナリオ：
>         -   元のクラスタバージョンはv6.5.7およびv7.1.0（ `performance.force-init-stats`をまだサポートしていない）より前のバージョンであり、ターゲットバージョンはv7.2.0以降です。
>         -   元のクラスタバージョンはv6.5.7およびv7.1.0以降であり、 `performance.force-init-stats`構成項目は`ON`に設定されています。
>
>     -   `performance.force-init-stats`設定項目の値を確認してください。
>
>             SHOW CONFIG WHERE type = 'tidb' AND name = 'performance.force-init-stats';
>
>     -   TiUPの待機タイムアウトは、コマンドラインオプション[`--wait-timeout`](/tiup/tiup-component-cluster.md#--wait-timeout)を追加することで延長できます。例えば、以下のコマンドを実行すると、待機タイムアウトを1200秒（20分）に設定できます。
>
>         ```shell
>         tiup update cluster --wait-timeout 1200 [other options]
>         ```
>
>         一般的に、ほとんどのシナリオでは20分の待機タイムアウトで十分です。より正確な見積もりについては、TiDBログで`init stats info time`を検索して、前回の起動時の統計読み込み時間を参考にしてください。例：
>
>             [domain.go:2271] ["init stats info time"] [lite=true] ["take time"=2.151333ms]
>
>         元のクラスターが v7.1.0 以前の場合、v7.2.0 以降にアップグレードすると、 [`performance.lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710)の導入により、統計情報の読み込み時間が大幅に短縮されます。この場合、アップグレード前の`init stats info time`は、アップグレード後の読み込み時間よりも長くなります。
>
>     -   TiDB のローリング アップグレード期間を短縮したい場合、およびアップグレード中の初期統計情報の欠落による潜在的なパフォーマンスへの影響がクラスターで許容できる場合は、TiUP を使用して対象インスタンスの設定を変更することで、アップグレード前に`performance.force-init-stats` `OFF`に[TiUPを使用して対象インスタンスの設定を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)。アップグレードの完了後、必要に応じてこの設定を再評価して元に戻すことができます。

## アップグレードに関する注意事項 {#upgrade-caveat}

-   TiDBは現在、アップグレード後にバージョンをダウングレードしたり、以前のバージョンに戻したりすることをサポートしていません。
-   TiCDC、 TiFlash、およびその他のコンポーネントのバージョンアップグレードをサポートします。
-   クラスターが TiCDC クラシックアーキテクチャ(v8.1.2 など) を使用している場合は、メジャー バージョン間のアップグレード中に変更フィードを実行し続けないでください。この場合、次の手順を順番に実行します。すべての変更フィードを一時停止し、TiCDC をアップグレードし、TiDB クラスターをアップグレードし、すべての変更フィードを再開します。詳細については、 [以前のバージョンからのアップグレードに関する互換性に関する注意事項](/ticdc/ticdc-compatibility.md#compatibility-notes-for-upgrading-from-earlier-versions)参照してください。
-   TiFlashをv6.3.0より前のバージョンからv6.3.0以降のバージョンにアップグレードする場合、Linux AMD64アーキテクチャではCPUがAVX2命令セットを、Linux ARM64アーキテクチャではARMv8命令セットアーキテクチャをサポートしている必要があることに注意してください。詳細は[v6.3.0 リリースノート](/releases/release-6.3.0.md#others)の説明を参照してください。
-   各バージョンの互換性に関する詳細な変更点については、各バージョンの[リリースノート](/releases/_index.md)を参照してください。該当するリリースノートの「互換性の変更点」セクションに従って、クラスタ構成を変更してください。
-   クラスターをv5.3より前のバージョンからv5.3以降のバージョンに更新する場合、デフォルトでデプロイされているPrometheusによって生成されるアラートの時刻フォーマットが変更されることに注意してください。このフォーマット変更はPrometheus v2.27.1から導入されています。詳細については、 [Prometheus](https://github.com/prometheus/prometheus/commit/7646cbca328278585be15fa615e22f2a50b47d06)を参照してください。

## 準備 {#preparations}

このセクションでは、 TiUPおよびTiUP クラスタコンポーネントのアップグレードを含め、TiDB クラスターをアップグレードする前に必要な準備作業について説明します。

### ステップ1：互換性の変更点を確認する {#step-1-review-compatibility-changes}

TiDBのリリースノートに記載されている互換性の変更点を確認してください。変更点がアップグレードに影響する場合は、適切な対応を取ってください。

以下は、v8.4.0 から最新バージョン (v8.5.4) にアップグレードする際に必要なリリースノートです。v8.3.0 以前のバージョンから最新バージョンにアップグレードする場合は、中間バージョンの[リリースノート](/releases/_index.md)も確認する必要があるかもしれません。

-   TiDB v8.5.0 [互換性の変更](/releases/release-8.5.0.md#compatibility-changes)
-   TiDB v8.5.1[リリースノート](/releases/release-8.5.1.md)
-   TiDB v8.5.2[リリースノート](/releases/release-8.5.2.md)
-   TiDB v8.5.3 [互換性の変更](/releases/release-8.5.3.md#compatibility-changes)
-   TiDB v8.5.4 [互換性の変更](/releases/release-8.5.4.md#compatibility-changes)
-   TiDB v8.5.5 [互換性の変更](https://docs.pingcap.com/tidb/stable/release-8.5.5/#compatibility-changes)
-   TiDB v8.5.6 [互換性の変更](https://docs.pingcap.com/tidb/stable/release-8.5.6/#compatibility-changes)
-   TiDB v8.5.7 [互換性の変更](https://docs.pingcap.com/tidb/stable/release-8.5.7/#compatibility-changes)

### ステップ2： TiUPまたはTiUPオフラインミラーをアップグレードする {#step-2-upgrade-tiup-or-tiup-offline-mirror}

TiDBクラスタをアップグレードする前に、まずTiUPまたはTiUPミラーをアップグレードする必要があります。

#### TiUPとTiUP クラスタをアップグレードする {#upgrade-tiup-and-tiup-cluster}

> **Note:**
>
> アップグレードするクラスターの制御マシンが`https://tiup-mirrors.pingcap.com`にアクセスできない場合は、このセクションをスキップして、 [TiUPオフラインミラーをアップグレード](#upgrade-tiup-offline-mirror)参照してください。

1.  TiUPのバージョンをアップグレードしてください。TiUPのバージョンは`1.11.3`以降を推奨します。

    ```shell
    tiup update --self
    tiup --version
    ```

2.  TiUP クラスタのバージョンをアップグレードしてください。TiUP クラスタのTiUPは`1.11.3`以降を推奨します。

    ```shell
    tiup update cluster
    tiup cluster --version
    ```

#### TiUPオフラインミラーをアップグレード {#upgrade-tiup-offline-mirror}

> **Note:**
>
> アップグレード対象のクラスターがオフライン方式を使用せずにデプロイされている場合は、この手順をスキップしてください。

新しいバージョンのTiUPミラー[TiUPを使用してTiDBクラスタをデプロイ- TiUPをオフラインでデプロイ](/production-deployment-using-tiup.md#deploy-tiup-offline)を参照してください。 `local_install.sh`を実行すると、 TiUP は上書きアップグレードを完了します。

```shell
tar xzvf tidb-community-server-${version}-linux-amd64.tar.gz
sh tidb-community-server-${version}-linux-amd64/local_install.sh
source /home/tidb/.bash_profile
```

上書きアップグレード後、次のコマンドを実行して、サーバーとツールキットのオフラインミラーをサーバーディレクトリにマージします。

```bash
tar xf tidb-community-toolkit-${version}-linux-amd64.tar.gz
ls -ld tidb-community-server-${version}-linux-amd64 tidb-community-toolkit-${version}-linux-amd64
cd tidb-community-server-${version}-linux-amd64/
cp -rp keys ~/.tiup/
tiup mirror merge ../tidb-community-toolkit-${version}-linux-amd64
```

ミラーをマージした後、次のコマンドを実行してTiUP クラスタコンポーネントをアップグレードします。

```shell
tiup update cluster
```

これでオフラインミラーのアップグレードは正常に完了しました。上書き後にTiUP操作中にエラーが発生した場合は、 `manifest`が更新されていない可能性があります。TiUPを再度実行する前に、 `rm -rf ~/.tiup/manifests/*`を試してみてください。

### ステップ3： TiUPトポロジー構成ファイルを編集する {#step-3-edit-tiup-topology-configuration-file}

> **Note:**
>
> 以下のいずれかの状況に該当する場合は、この手順をスキップしてください。
>
> -   元のクラスターの構成パラメータを変更していません。または、 `tiup cluster`を使用して構成パラメータを変更しましたが、それ以上の変更は必要ありません。
> -   アップグレード後、変更されていない設定項目については、v8.5.4のデフォルトのパラメータ値を使用します。

1.  トポロジーファイルを編集するには、 `vi`編集モードに入ります。

    ```shell
    tiup cluster edit-config <cluster-name>
    ```

2.  フォーマットを参照[トポロジー](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml)設定テンプレートを参照し、トポロジファイルの`server_configs`セクションに変更したいパラメータを入力します。

3.  変更後、 <kbd>「:</kbd> + <kbd>w</kbd> + <kbd>q」</kbd>と入力して変更を保存し、編集モードを終了します。変更を確定するには<kbd>「Y」</kbd>と入力してください。

### ステップ4：クラスターのDDLとバックアップの状態を確認します {#step-4-check-the-ddl-and-backup-status-of-the-cluster}

アップグレード中に予期せぬ動作やその他の問題が発生するのを避けるため、アップグレード前に以下の項目を確認することをお勧めします。

-   クラスタDDL:

    -   [スムーズなアップグレード](/smooth-upgrade-tidb.md)アップグレードを使用して TiDB を v8.1.0 以降にアップグレードし、[分散実行フレームワーク（DXF）](/tidb-distributed-execution-framework.md)が有効になっている場合は、アップグレードする前に DXF を無効にすることをお勧めします。そうしないと、アップグレード プロセス中に追加されたインデックスがデータと矛盾し、アップグレードが失敗する可能性があります。
    -   な を使用しない場合は、 [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md)[スムーズなアップグレード](/smooth-upgrade-tidb.md)を使用して、実行中の DDL ジョブが存在するかどうかを確認することをお勧めします。実行中の DDL ジョブが存在する場合は、アップグレードを実行する前に、ジョブの実行が完了するまで待つか、 [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)ステートメントを使用してキャンセルしてください。

-   クラスタのバックアップ：クラスタ内でバックアップまたはリストアタスクが実行中かどうかを確認するには[`SHOW [BACKUPS|RESTORES]`](/sql-statements/sql-statement-show-backups.md)コマンドを実行することをお勧めします。実行中の場合は、アップグレードを実行する前にタスクが完了するまでお待ちください。

### ステップ5：現在のクラスターの健全性状態を確認する {#step-5-check-the-health-status-of-the-current-cluster}

アップグレード中に予期しない動作やその他の問題が発生しないように、アップグレード前に現在のクラスターのリージョンの健全性状態を確認することをお勧めします。そのためには、 `check`サブコマンドを使用できます。

```shell
tiup cluster check <cluster-name> --cluster
```

コマンドが実行されると、「リージョンステータス」のチェック結果が出力されます。

-   結果が「すべてのリージョンは正常です」であれば、現在のクラスター内のすべてのリージョンは正常であり、アップグレードを続行できます。
-   結果が「リージョンが完全に正常ではありません：m個のミスピア、n個の保留ピア」で、「他の操作を行う前に、異常なリージョンを修正してください。」というメッセージが表示される場合、現在のクラスタ内の一部のリージョンに異常があります。チェック結果が「すべてのリージョンが正常です」になるまで、異常のトラブルシューティングを行う必要があります。その後、アップグレードを続行できます。

## TiDBクラスタをアップグレードする {#upgrade-the-tidb-cluster}

このセクションでは、TiDBクラスタをアップグレードする方法と、アップグレード後のバージョンを確認する方法について説明します。

### TiDBクラスタを指定されたバージョンにアップグレードする {#upgrade-the-tidb-cluster-to-a-specified-version}

クラスターのアップグレードは、オンラインアップグレードとオフラインアップグレードの2つの方法のいずれかで行うことができます。

TiUP クラスタはデフォルトではオンライン方式でTiDBクラスタをアップグレードします。つまり、アップグレード処理中もTiDBクラスタはサービスを提供し続けることができます。オンライン方式では、アップグレードと再起動の前に各ノードでリーダーが1つずつ移行されます。そのため、大規模なクラスタでは、アップグレード操作全体が完了するまでに時間がかかります。

アプリケーションに、データベースのメンテナンスのために停止するメンテナンス期間が設定されている場合、オフラインアップグレード方式を使用することで、アップグレード操作を迅速に実行できます。

#### オンラインアップグレード {#online-upgrade}

```shell
tiup cluster upgrade <cluster-name> <version>
```

例えば、クラスターをv8.5.4にアップグレードする場合：

```shell
tiup cluster upgrade <cluster-name> v8.5.4
```

> **Note:**
>
> -   オンラインアップグレードは、TiUPの固定コンポーネントアップグレード順序に従って行われます。各コンポーネントタイプ内では、インスタンスが順次アップグレードされます。
>
>     -   **TiFlash** ： TiFlashは常に最初にアップグレードされます。クラスタにTiFlashが含まれている場合、 TiUPは他のコンポーネント（PD、TiKV、TiDBなど）に進む前に、すべてのTiFlashインスタンスのローリングアップグレードを実行します。クラスタにデプロイされていないコンポーネントタイプはスキップされます。
>     -   **TiKV** ：TiKVのアップグレード中、 TiUPはインスタンスを停止する前に、PDを介してTiKVストアからすべてのリージョンリーダーを削除します。リーダー転送のデフォルトのタイムアウトは5分（300秒）です。タイムアウトに達すると、 TiUPはリーダー削除の完了を待たずにインスタンスを直接停止します。
>
> -   `--force`パラメータを使用すると、リーダーを削除せずにクラスターを即座にアップグレードできます。ただし、アップグレード中に発生したエラーは無視されるため、アップグレードの失敗に関する通知は届きません。したがって、 `--force`パラメータは慎重に使用してください。
>
> -   安定したパフォーマンスを維持するには、TiKV インスタンスを停止する前に、インスタンス内のすべてのリーダーが強制終了されていることを確認してください。 `--transfer-timeout`を、例えば`--transfer-timeout 3600` (単位: 秒) のように、より大きな値に設定できます。
>
> -   TiFlash をv5.3.0 より前のバージョンから v5.3.0 以降にアップグレードするには、 TiFlash を停止してからアップグレードする必要があります。また、 TiUP のバージョンは v1.12.0 より前である必要があります。詳細については、 [TiUPを使用してTiFlashをアップグレードする](/tiflash-upgrade-guide.md#upgrade-tiflash-using-tiup)参照してください。

#### アップグレード時にコンポーネントのバージョンを指定してください。 {#specify-the-component-version-during-upgrade}

tiup-cluster v1.14.0以降では、クラスタのアップグレード時に特定のコンポーネントを特定のバージョンに指定できるようになりました。別のバージョンを指定しない限り、これらのコンポーネントは以降のアップグレードでも固定バージョンのままになります。

> **Note:**
>
> TiDB、TiKV、PD、TiCDCなど、バージョン番号を共有するコンポーネントについては、バージョンが混在する展開環境で正しく動作することを保証する完全なテストは実施されていません。このセクションはテスト環境でのみ使用するか、または[テクニカルサポート](/support.md)の支援を受けて使用してください。

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

1.  オフラインアップグレードを行う前に、まずクラスター全体を停止する必要があります。

    ```shell
    tiup cluster stop <cluster-name>
    ```

2.  `upgrade`コマンドに`--offline`オプションを指定して、オフラインアップグレードを実行します。 `<cluster-name>`にはクラスタ名を、 `<version>`にはアップグレード先のバージョン（例: `v8.5.4`入力します。

    ```shell
    tiup cluster upgrade <cluster-name> <version> --offline
    ```

3.  アップグレード後、クラスターは自動的に再起動されません。 `start`コマンドを使用して再起動する必要があります。

    ```shell
    tiup cluster start <cluster-name>
    ```

### クラスターのバージョンを確認します {#verify-the-cluster-version}

`display`コマンドを実行して、最新のクラスタバージョン`TiDB Version`を表示します。

```shell
tiup cluster display <cluster-name>
```

    Cluster type:       tidb
    Cluster name:       <cluster-name>
    Cluster version:    v8.5.4

## FAQ {#faq}

このセクションでは、 TiUPを使用して TiDB クラスタを更新する際に発生する一般的な問題について説明します。

### エラーが発生してアップグレードが中断された場合、エラーを修正した後、どのようにアップグレードを再開すればよいですか？ {#if-an-error-occurs-and-the-upgrade-is-interrupted-how-to-resume-the-upgrade-after-fixing-this-error}

アップグレードを再開するには、 `tiup cluster upgrade`コマンドを再度実行してください。アップグレード操作では、既にアップグレード済みのノードが再起動されます。アップグレード済みのノードを再起動したくない場合は、 `replay`サブコマンドを使用して操作を再試行してください。

1.  操作記録を表示するには、 `tiup cluster audit`を実行してください。

    ```shell
    tiup cluster audit
    ```

    失敗したアップグレード操作レコードを見つけて、その操作レコードのIDを控えてください。このIDは、次のステップで`<audit-id>`値として使用されます。

2.  対応する操作を再試行するには、 `tiup cluster replay <audit-id>`を実行してください。

    ```shell
    tiup cluster replay <audit-id>
    ```

### バージョン6.2.0以降へのアップグレード時にアップグレード処理が停止してしまう問題を解決するにはどうすればよいですか？ {#how-to-fix-the-issue-that-the-upgrade-gets-stuck-when-upgrading-to-v620-or-later-versions}

バージョン6.2.0以降、TiDBはデフォルトで[並行DDLフレームワーク](/best-practices/ddl-introduction.md#how-the-online-ddl-asynchronous-change-works-in-tidb)を有効にし、同時DDLの実行を可能にしました。このフレームワークは、DDLジョブのストレージをKVキューからテーブルキューに変更します。この変更により、一部のシナリオではアップグレードが停止する可能性があります。この問題が発生する可能性のあるシナリオと、それに対応する解決策を以下に示します。

-   プラグインの読み込みが原因でアップグレードが停止します

    アップグレード中に、DDLステートメントの実行を必要とする特定のプラグインを読み込むと、アップグレードが停止する可能性があります。

    **解決策**：アップグレード中はプラグインをロードしないようにしてください。代わりに、アップグレードが完了した後にのみプラグインをロードしてください。

-   オフラインアップグレードに`kill -9`コマンドを使用しているため、アップグレードが停止します。

    -   注意事項： `kill -9`コマンドを使用してオフラインアップグレードを実行することは避けてください。どうしても必要な場合は、2 分後に新しいバージョンの TiDB ノードを再起動してください。
    -   アップグレードが既に停止している場合は、影響を受けているTiDBノードを再起動してください。問題が発生したばかりの場合は、2分後にノードを再起動することをお勧めします。

-   DDL所有者の変更によりアップグレードが停止する

    マルチインスタンス環境では、ネットワーク障害やハードウェア障害によってDDL所有者が変更される可能性があります。アップグレードフェーズで未完了のDDLステートメントが存在する場合、アップグレードが停止する可能性があります。

    **解決**：

    1.  停止した TiDB ノードを終了します ( `kill -9`の使用は避けてください)。
    2.  新しいバージョンのTiDBノードを再起動してください。

### 退去リーダーはアップグレード中に待ち時間が長すぎました。この手順をスキップしてアップグレードを迅速に行うにはどうすればよいでしょうか？ {#the-evict-leader-has-waited-too-long-during-the-upgrade-how-to-skip-this-step-for-a-quick-upgrade}

`--force`を指定できます。そうすると、アップグレード中に PD リーダーの転送と TiKV リーダーの強制終了のプロセスがスキップされます。クラスターは直接再起動され、バージョンが更新されます。これは、オンラインで実行されているクラスターに大きな影響を与えます。次のコマンドでは、 `<version>`はアップグレード先のバージョンです。たとえば`v8.5.4`などです。

```shell
tiup cluster upgrade <cluster-name> <version> --force
```

### TiDBクラスタをアップグレードした後、pd-ctlなどのツールのバージョンを更新するにはどうすればよいですか？ {#how-to-update-the-version-of-tools-such-as-pd-ctl-after-upgrading-the-tidb-cluster}

TiUPを使用して対応するコンポーネントの`ctl`コンポーネントをインストールすることで、ツールのバージョンをアップグレードできます。

```shell
tiup install ctl:v8.5.4
```
