---
title: Upgrade TiDB Using TiUP
summary: Learn how to upgrade TiDB using TiUP.
---

# TiUPを使用して TiDB をアップグレードする {#upgrade-tidb-using-tiup}

このドキュメントは、次のアップグレード パスを対象としています。

-   TiDB 4.0 バージョンから TiDB 7.5 にアップグレードします。
-   TiDB 5.0 ～ 5.4 バージョンから TiDB 7.5 にアップグレードします。
-   TiDB 6.0 ～ 6.6 から TiDB 7.5 にアップグレードします。
-   TiDB 7.0 ～ 7.4 から TiDB 7.5 にアップグレードします。

> **警告：**
>
> 1.  TiFlash を5.3 より前のバージョンから 5.3 以降にオンラインでアップグレードすることはできません。代わりに、最初に初期バージョンのすべてのTiFlashインスタンスを停止してから、クラスターをオフラインでアップグレードする必要があります。他のコンポーネント (TiDB や TiKV など) がオンライン アップグレードをサポートしていない場合は、 [オンラインアップグレード](#online-upgrade)の警告の指​​示に従ってください。
> 2.  アップグレード プロセス中に DDL ステートメントを実行し**ないでください**。そうしないと、未定義の動作の問題が発生する可能性があります。
> 3.  DDL ステートメントがクラスター内で実行されているときは、TiDB クラスターをアップグレードし**ないでください**(通常は、 `ADD INDEX`や列タイプの変更など、時間のかかる DDL ステートメントの場合)。アップグレードの前に、 [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md)コマンドを使用して、TiDB クラスターに進行中の DDL ジョブがあるかどうかを確認することをお勧めします。クラスターに DDL ジョブがある場合、クラスターをアップグレードするには、DDL の実行が完了するまで待つか、クラスターをアップグレードする前に[`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)コマンドを使用して DDL ジョブをキャンセルします。
>
> アップグレード前の TiDB バージョンが v7.1.0 以降の場合、前述の警告 2 および 3 は無視できます。詳細については、 [TiDB のスムーズなアップグレード](/smooth-upgrade-tidb.md)を参照してください。

> **注記：**
>
> -   アップグレードするクラスターが v3.1 以前のバージョン (v3.0 または v2.1) である場合、v7.5.0 への直接アップグレードはサポートされません。クラスターを最初に v4.0 にアップグレードし、次に v7.5.0 にアップグレードする必要があります。
> -   アップグレードするクラスターが v6.2 より前の場合、シナリオによってはクラスターを v6.2 以降のバージョンにアップグレードすると、アップグレードが停止する可能性があります。 [問題の解決方法](#how-to-fix-the-issue-that-the-upgrade-gets-stuck-when-upgrading-to-v620-or-later-versions)を参照してください。
> -   TiDB ノードは、 [`server-version`](/tidb-configuration-file.md#server-version)構成項目の値を使用して、現在の TiDB バージョンを確認します。したがって、予期しない動作を回避するには、TiDB クラスターをアップグレードする前に、値`server-version`を空、または現在の TiDB クラスターの実際のバージョンに設定する必要があります。

## アップグレードに関する注意事項 {#upgrade-caveat}

-   TiDB は現在、バージョンのダウングレードや、アップグレード後の以前のバージョンへのロールバックをサポートしていません。
-   TiDB Ansible を使用して管理されている v4.0 クラスターの場合、 [TiUP (v4.0) を使用して TiDB をアップグレードする](https://docs.pingcap.com/tidb/v4.0/upgrade-tidb-using-tiup#import-tidb-ansible-and-the-inventoryini-configuration-to-tiup)に従って新しい管理を行うためにクラスターをTiUP ( `tiup cluster` ) にインポートする必要があります。その後、このドキュメントに従ってクラスターを v7.5.0 にアップグレードできます。
-   v3.0 より前のバージョンを v7.5.0 に更新するには:
    1.  [TiDB Ansible](https://docs.pingcap.com/tidb/v3.0/upgrade-tidb-using-ansible)を使用してこのバージョンを 3.0 に更新します。
    2.  TiUP ( `tiup cluster` ) を使用して、TiDB Ansible 構成をインポートします。
    3.  [TiUP (v4.0) を使用して TiDB をアップグレードする](https://docs.pingcap.com/tidb/v4.0/upgrade-tidb-using-tiup#import-tidb-ansible-and-the-inventoryini-configuration-to-tiup)に従って、3.0 バージョンを 4.0 に更新します。
    4.  このドキュメントに従ってクラスターを v7.5.0 にアップグレードします。
-   TiDB Binlog、 TiCDC、 TiFlash、およびその他のコンポーネントのバージョンのアップグレードをサポートします。
-   TiFlash をv6.3.0 より前のバージョンから v6.3.0 以降のバージョンにアップグレードする場合、CPU は Linux AMD64アーキテクチャでは AVX2 命令セットをサポートし、Linux ARM64アーキテクチャでは ARMv8 命令セットアーキテクチャをサポートする必要があることに注意してください。詳細については、 [v6.3.0 リリースノート](/releases/release-6.3.0.md#others)の説明を参照してください。
-   さまざまなバージョンの互換性の変更の詳細については、各バージョンの[リリースノート](/releases/release-notes.md)を参照してください。対応するリリース ノートの「互換性の変更」セクションに従って、クラスター構成を変更します。
-   v5.3 より前のバージョンから v5.3 以降のバージョンにアップグレードするクラスターの場合、デフォルトでデプロイされた Prometheus は v2.8.1 から v2.27.1 にアップグレードされます。 Prometheus v2.27.1 では、より多くの機能が提供され、セキュリティ問題が修正されています。 v2.8.1 と比較して、v2.27.1 ではアラート時間の表現が変更されています。詳細については、 [プロメテウスのコミット](https://github.com/prometheus/prometheus/commit/7646cbca328278585be15fa615e22f2a50b47d06)を参照してください。

## 準備 {#preparations}

このセクションでは、 TiUPおよびTiUPクラスタコンポーネントのアップグレードなど、TiDB クラスターをアップグレードする前に必要な準備作業について説明します。

### ステップ 1: 互換性の変更を確認する {#step-1-review-compatibility-changes}

TiDB v7.5.0 リリース ノートの[互換性が変わります](/releases/release-7.5.0.md#compatibility-changes)確認してください。変更がアップグレードに影響を与える場合は、それに応じて対処してください。

### ステップ 2: TiUPまたはTiUPオフライン ミラーをアップグレードする {#step-2-upgrade-tiup-or-tiup-offline-mirror}

TiDB クラスターをアップグレードする前に、まずTiUPまたはTiUPミラーをアップグレードする必要があります。

#### TiUPおよびTiUPクラスタのアップグレード {#upgrade-tiup-and-tiup-cluster}

> **注記：**
>
> アップグレードするクラスターの制御マシンが`https://tiup-mirrors.pingcap.com`アクセスできない場合は、このセクションをスキップして[TiUPオフライン ミラーをアップグレードする](#upgrade-tiup-offline-mirror)を参照してください。

1.  TiUP のバージョンをアップグレードします。 TiUPバージョンは`1.11.3`以降を推奨します。

    ```shell
    tiup update --self
    tiup --version
    ```

2.  TiUPクラスタのバージョンをアップグレードします。 TiUP クラスタ のバージョンは`1.11.3`以降を推奨します。

    ```shell
    tiup update cluster
    tiup cluster --version
    ```

#### TiUPオフライン ミラーをアップグレードする {#upgrade-tiup-offline-mirror}

> **注記：**
>
> アップグレードするクラスターがオフライン方式を使用せずにデプロイされた場合は、この手順をスキップしてください。

[TiUPを使用して TiDBクラスタをデプロイ- TiUP をオフラインでデプロイ](/production-deployment-using-tiup.md#deploy-tiup-offline)を参照して、新バージョンのTiUPミラーをダウンロードし、制御マシンにアップロードします。 `local_install.sh`を実行すると、 TiUP は上書きアップグレードを完了します。

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

ミラーを結合した後、次のコマンドを実行してTiUPクラスタコンポーネントをアップグレードします。

```shell
tiup update cluster
```

これで、オフライン ミラーが正常にアップグレードされました。上書き後のTiUP動作中にエラーが発生した場合、 `manifest`が更新されていない可能性があります。 TiUP を再度実行する前に、 `rm -rf ~/.tiup/manifests/*`を試すことができます。

### ステップ 3: TiUPトポロジ構成ファイルを編集する {#step-3-edit-tiup-topology-configuration-file}

> **注記：**
>
> 次のいずれかの状況に該当する場合は、この手順をスキップしてください。
>
> -   元のクラスターの構成パラメーターは変更されていません。または、 `tiup cluster`を使用して構成パラメータを変更しましたが、それ以上の変更は必要ありません。
> -   アップグレード後、未変更の構成項目には v7.5.0 のデフォルトのパラメータ値を使用したいと考えています。

1.  `vi`編集モードに入り、トポロジ ファイルを編集します。

    ```shell
    tiup cluster edit-config <cluster-name>
    ```

2.  [トポロジー](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml)構成テンプレートの形式を参照し、トポロジ ファイルの`server_configs`セクションに変更するパラメータを入力します。

3.  変更後、 <kbd>:</kbd> + <kbd>w</kbd> + <kbd>q</kbd>を入力して変更を保存し、編集モードを終了します。 <kbd>Y</kbd>を入力して変更を確認します。

> **注記：**
>
> クラスターを v6.6.0 にアップグレードする前に、v4.0 で変更したパラメーターが v7.5.0 でも互換性があることを確認してください。詳細は[TiKVコンフィグレーションファイル](/tikv-configuration-file.md)を参照してください。

### ステップ 4: 現在のクラスターの健全性ステータスを確認する {#step-4-check-the-health-status-of-the-current-cluster}

アップグレード中の未定義の動作やその他の問題を回避するには、アップグレード前に現在のクラスターのリージョンの健全性ステータスを確認することをお勧めします。これを行うには、 `check`サブコマンドを使用します。

```shell
tiup cluster check <cluster-name> --cluster
```

コマンド実行後、「リージョンステータス」のチェック結果が出力されます。

-   結果が「すべてのリージョンが正常です」の場合は、現在のクラスター内のすべてのリージョンが正常であるため、アップグレードを続行できます。
-   結果が「リージョンが完全に正常ではありません: m miss-peer, n pending-peer」で、「他の操作の前に異常なリージョンを修正してください。」となった場合。プロンプトが表示されると、現在のクラスター内の一部のリージョンが異常です。チェック結果が「すべてのリージョンが正常」になるまで、異常のトラブルシューティングを行う必要があります。その後、アップグレードを続行できます。

### ステップ 5: クラスターの DDL とバックアップのステータスを確認する {#step-5-check-the-ddl-and-backup-status-of-the-cluster}

アップグレード中の未定義の動作やその他の予期しない問題を回避するために、アップグレード前に次の項目を確認することをお勧めします。

-   クラスタDDL: [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md)ステートメントを実行して、進行中の DDL ジョブがあるかどうかを確認することをお勧めします。 「はい」の場合は、その実行を待つか、アップグレードを実行する前に[`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)ステートメントを実行してキャンセルします。
-   クラスタのバックアップ: [`SHOW [BACKUPS|RESTORES]`](/sql-statements/sql-statement-show-backups.md)ステートメントを実行して、クラスター内に進行中のバックアップまたは復元タスクがあるかどうかを確認することをお勧めします。 「はい」の場合は、アップグレードを実行する前に完了するまで待ちます。

## TiDB クラスターをアップグレードする {#upgrade-the-tidb-cluster}

このセクションでは、TiDB クラスターをアップグレードし、アップグレード後のバージョンを確認する方法について説明します。

### TiDB クラスターを指定されたバージョンにアップグレードする {#upgrade-the-tidb-cluster-to-a-specified-version}

クラスターは、オンライン アップグレードとオフライン アップグレードの 2 つの方法のいずれかでアップグレードできます。

デフォルトでは、 TiUPクラスタはオンライン方式を使用して TiDB クラスターをアップグレードします。これは、TiDB クラスターがアップグレード プロセス中に引き続きサービスを提供できることを意味します。オンライン方式では、アップグレードして再起動する前に、各ノードでリーダーが 1 つずつ移行されます。したがって、大規模なクラスターの場合、アップグレード操作全体が完了するまでに長い時間がかかります。

アプリケーションにメンテナンスのためにデータベースを停止するためのメンテナンス期間がある場合は、オフライン アップグレード方法を使用してアップグレード操作を迅速に実行できます。

#### オンラインアップグレード {#online-upgrade}

```shell
tiup cluster upgrade <cluster-name> <version>
```

たとえば、クラスターを v7.5.0 にアップグレードする場合は、次のようにします。

```shell
tiup cluster upgrade <cluster-name> v7.5.0
```

> **注記：**
>
> -   オンライン アップグレードでは、すべてのコンポーネントが 1 つずつアップグレードされます。 TiKV のアップグレード中、TiKV インスタンス内のすべてのリーダーは、インスタンスを停止する前に削除されます。デフォルトのタイムアウト時間は 5 分 (300 秒) です。このタイムアウト時間が経過すると、インスタンスは直接停止されます。
>
> -   `--force`パラメーターを使用すると、リーダーを削除せずにクラスターをすぐにアップグレードできます。ただし、アップグレード中に発生するエラーは無視されます。つまり、アップグレードの失敗については通知されません。したがって、 `--force`パラメータは注意して使用してください。
>
> -   安定したパフォーマンスを維持するには、インスタンスを停止する前に、TiKV インスタンス内のすべてのリーダーが削除されていることを確認してください。 `--transfer-timeout`より大きな値、たとえば`--transfer-timeout 3600`を設定することもできます (単位: 秒)。
>
> -   TiFlash を5.3 より前のバージョンから 5.3 以降にアップグレードするには、 TiFlashを停止してからアップグレードする必要があります。次の手順は、他のコンポーネントを中断せずにTiFlashをアップグレードするのに役立ちます。
>     1.  TiFlashインスタンスを停止します: `tiup cluster stop <cluster-name> -R tiflash`
>     2.  TiDB クラスターを再起動せずにアップグレードします (ファイルの更新のみ): `tiup cluster upgrade <cluster-name> <version> --offline` (例: `tiup cluster upgrade <cluster-name> v6.3.0 --offline`
>     3.  TiDB クラスターをリロードします。 `tiup cluster reload <cluster-name>` .リロード後、 TiFlashインスタンスが開始されるため、手動で開始する必要はありません。
>
> -   TiDB Binlogを使用してクラスターにローリング アップデートを適用する場合は、新しいクラスター化インデックス テーブルを作成しないようにしてください。

#### アップグレード時にコンポーネントのバージョンを指定する {#specify-the-component-version-during-upgrade}

tiup-cluster v1.14.0 以降、クラスターのアップグレード中に特定のコンポーネントを特定のバージョンに指定できます。これらのコンポーネントは、別のバージョンを指定しない限り、後続のアップグレードでも修正されたバージョンのままになります。

> **注記：**
>
> TiDB、TiKV、PD、TiCDC など、バージョン番号を共有するコンポーネントについては、バージョンが混在した展開シナリオで適切に動作することを確認するための完全なテストはありません。このセクションは、テスト環境でのみ使用するか、 [テクニカルサポート](/support.md)の助けを借りて使用するようにしてください。

```shell
tiup cluster upgrade -h | grep "version string"
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

1.  オフライン アップグレードの前に、まずクラスター全体を停止する必要があります。

    ```shell
    tiup cluster stop <cluster-name>
    ```

2.  オフライン アップグレードを実行するには、 `upgrade`コマンドと`--offline`オプションを使用します。 `<cluster-name>`の場合はクラスターの名前を入力し、 `<version>`の場合はアップグレードするバージョン ( `v7.5.0`など) を入力します。

    ```shell
    tiup cluster upgrade <cluster-name> <version> --offline
    ```

3.  アップグレード後、クラスターは自動的に再起動されません。再起動するには`start`コマンドを使用する必要があります。

    ```shell
    tiup cluster start <cluster-name>
    ```

### クラスターのバージョンを確認する {#verify-the-cluster-version}

`display`コマンドを実行して、最新のクラスター バージョン`TiDB Version`を表示します。

```shell
tiup cluster display <cluster-name>
```

    Cluster type:       tidb
    Cluster name:       <cluster-name>
    Cluster version:    v7.5.0

## FAQ {#faq}

このセクションでは、 TiUPを使用して TiDB クラスターを更新するときに発生する一般的な問題について説明します。

### エラーが発生してアップグレードが中断された場合、このエラーを修正した後にアップグレードを再開するにはどうすればよいですか? {#if-an-error-occurs-and-the-upgrade-is-interrupted-how-to-resume-the-upgrade-after-fixing-this-error}

`tiup cluster upgrade`コマンドを再実行して、アップグレードを再開します。アップグレード操作では、以前にアップグレードされたノードが再起動されます。アップグレードされたノードを再起動したくない場合は、 `replay`サブコマンドを使用して操作を再試行します。

1.  `tiup cluster audit`を実行して操作記録を確認します。

    ```shell
    tiup cluster audit
    ```

    失敗したアップグレード操作レコードを見つけて、この操作レコードの ID を保管します。 ID は次のステップの`<audit-id>`値です。

2.  `tiup cluster replay <audit-id>`を実行して、対応する操作を再試行します。

    ```shell
    tiup cluster replay <audit-id>
    ```

### v6.2.0 以降のバージョンにアップグレードするときにアップグレードが停止する問題を解決するにはどうすればよいですか? {#how-to-fix-the-issue-that-the-upgrade-gets-stuck-when-upgrading-to-v6-2-0-or-later-versions}

v6.2.0 以降、TiDB ではデフォルトで[同時 DDL フレームワーク](/ddl-introduction.md#how-the-online-ddl-asynchronous-change-works-in-tidb)が同時 DDL を実行できるようになります。このフレームワークは、DDL ジョブstorageをKV キューからテーブル キューに変更します。この変更により、一部のシナリオではアップグレードが停止する可能性があります。以下に、この問題を引き起こす可能性のあるいくつかのシナリオと、対応する解決策を示します。

-   プラグインの読み込みによりアップグレードが停止する

    アップグレード中に、DDL ステートメントの実行を必要とする特定のプラグインをロードすると、アップグレードが停止する可能性があります。

    **解決策**: アップグレード中にプラグインをロードしないようにします。代わりに、アップグレードが完了した後にのみプラグインをロードしてください。

-   オフライン アップグレードに`kill -9`コマンドを使用したため、アップグレードが停止する

    -   注意事項: `kill -9`コマンドを使用してオフライン アップグレードを実行することは避けてください。必要に応じて、2 分後に新しいバージョンの TiDB ノードを再起動します。
    -   アップグレードがすでに停止している場合は、影響を受ける TiDB ノードを再起動します。問題が発生したばかりの場合は、2 分後にノードを再起動することをお勧めします。

-   DDL 所有者の変更によりアップグレードが停止する

    マルチインスタンスのシナリオでは、ネットワークまたはハードウェアの障害により、DDL 所有者が変更される可能性があります。アップグレード段階で未完了の DDL ステートメントがある場合、アップグレードが停止する可能性があります。

    **解決**：

    1.  スタックした TiDB ノードを終了します ( `kill -9`使用は避けてください)。
    2.  新しいバージョンの TiDB ノードを再起動します。

### エビクト リーダーがアップグレード中に長時間待機しすぎました。この手順をスキップして簡単にアップグレードするにはどうすればよいですか? {#the-evict-leader-has-waited-too-long-during-the-upgrade-how-to-skip-this-step-for-a-quick-upgrade}

`--force`を指定できます。その後、アップグレード中に PD リーダーの転送プロセスと TiKV リーダーの削除プロセスがスキップされます。バージョンを更新するためにクラスターが直接再起動されます。これは、オンラインで実行されるクラスターに大きな影響を与えます。次のコマンドの`<version>` 、アップグレード後のバージョンです ( `v7.5.0`など)。

```shell
tiup cluster upgrade <cluster-name> <version> --force
```

### TiDB クラスターをアップグレードした後に pd-ctl などのツールのバージョンを更新するにはどうすればよいですか? {#how-to-update-the-version-of-tools-such-as-pd-ctl-after-upgrading-the-tidb-cluster}

TiUPを使用して、対応するバージョンの`ctl`コンポーネントをインストールすることで、ツールのバージョンをアップグレードできます。

```shell
tiup install ctl:v7.5.0
```
