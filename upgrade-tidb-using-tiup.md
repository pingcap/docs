---
title: Upgrade TiDB Using TiUP
summary: Learn how to upgrade TiDB using TiUP.
---

# TiUPを使用して TiDB をアップグレードする {#upgrade-tidb-using-tiup}

このドキュメントは、次のアップグレード パスを対象としています。

-   TiDB 4.0 バージョンから TiDB 6.5 にアップグレードします。
-   TiDB 5.0 ～ 5.4 バージョンから TiDB 6.5 にアップグレードします。
-   TiDB 6.0 から TiDB 6.5 にアップグレードします。
-   TiDB 6.1 から TiDB 6.5 にアップグレードします。
-   TiDB 6.2 から TiDB 6.5 にアップグレードします。
-   TiDB 6.3 から TiDB 6.5 にアップグレードします。
-   TiDB 6.4 から TiDB 6.5 にアップグレードします。

> **警告：**
>
> -   TiFlash を5.3 より前のバージョンから 5.3 以降にオンラインでアップグレードすることはできません。代わりに、最初に初期バージョンのすべてのTiFlashインスタンスを停止してから、クラスターをオフラインでアップグレードする必要があります。他のコンポーネント (TiDB や TiKV など) がオンライン アップグレードをサポートしていない場合は、 [オンラインアップグレード](#online-upgrade)の警告の指示に従ってください。
> -   DDL ステートメントがクラスターで実行されているときは、TiDB クラスターをアップグレード**しないでください**(通常、 `ADD INDEX`のような時間のかかる DDL ステートメントや列の型の変更のため)。
> -   アップグレードの前に、 [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md)コマンドを使用して、TiDB クラスターに進行中の DDL ジョブがあるかどうかを確認することをお勧めします。クラスターに DDL ジョブがある場合、クラスターをアップグレードするには、DDL の実行が完了するまで待つか、 [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)コマンドを使用して DDL ジョブをキャンセルしてからクラスターをアップグレードします。
> -   また、クラスターのアップグレード中は、DDL ステートメントを実行し**ないでください**。そうしないと、未定義の動作の問題が発生する可能性があります。

> **ノート：**
>
> アップグレードするクラスターが v3.1 以前のバージョン (v3.0 または v2.1) である場合、v6.5.0 以降の v6.5.x バージョンへの直接アップグレードはサポートされていません。最初にクラスターを v4.0 にアップグレードしてから、ターゲットの TiDB バージョンにアップグレードする必要があります。

## アップグレードの注意事項 {#upgrade-caveat}

-   TiDB は現在、バージョンのダウングレードまたはアップグレード後の以前のバージョンへのロールバックをサポートしていません。
-   TiDB Ansible を使用して管理されている v4.0 クラスターの場合、 [TiUP (v4.0) を使用して TiDB をアップグレードする](https://docs.pingcap.com/tidb/v4.0/upgrade-tidb-using-tiup#import-tidb-ansible-and-the-inventoryini-configuration-to-tiup)に従って新しい管理のためにクラスターをTiUP ( `tiup cluster` ) にインポートする必要があります。その後、このドキュメントに従ってクラスターを v6.5.2 にアップグレードできます。
-   v3.0 より前のバージョンを v6.5.2 に更新するには:
    1.  [TiDB アンシブル](https://docs.pingcap.com/tidb/v3.0/upgrade-tidb-using-ansible)を使用して、このバージョンを 3.0 に更新します。
    2.  TiUP ( `tiup cluster` ) を使用して、TiDB Ansible 構成をインポートします。
    3.  [TiUP (v4.0) を使用して TiDB をアップグレードする](https://docs.pingcap.com/tidb/v4.0/upgrade-tidb-using-tiup#import-tidb-ansible-and-the-inventoryini-configuration-to-tiup)に従って、バージョン 3.0 を 4.0 に更新します。
    4.  このドキュメントに従って、クラスターを v6.5.2 にアップグレードします。
-   TiDB Binlog、TiCDC、 TiFlash、およびその他のコンポーネントのバージョンのアップグレードをサポートします。
-   TiFlash をv6.3.0 より前のバージョンから v6.3.0 以降のバージョンにアップグレードする場合、CPU は Linux AMD64アーキテクチャで AVX2 命令セットをサポートし、Linux ARM64アーキテクチャで ARMv8 命令セットアーキテクチャをサポートする必要があることに注意してください。詳細については、 [v6.3.0 リリースノート](/releases/release-6.3.0.md#others)の説明を参照してください。
-   異なるバージョンの詳細な互換性の変更については、各バージョンの[リリースノート](/releases/release-notes.md)を参照してください。対応するリリース ノートの「互換性の変更」セクションに従って、クラスター構成を変更します。
-   v5.3 より前のバージョンから v5.3 以降のバージョンにアップグレードするクラスターの場合、デフォルトでデプロイされた Prometheus は v2.8.1 から v2.27.1 にアップグレードされます。 Prometheus v2.27.1 は、より多くの機能を提供し、セキュリティの問題を修正します。 v2.8.1 と比較して、v2.27.1 のアラート時間の表現が変更されました。詳細については、 [プロメテウスコミット](https://github.com/prometheus/prometheus/commit/7646cbca328278585be15fa615e22f2a50b47d06)を参照してください。

## 準備 {#preparations}

このセクションでは、 TiUPおよびTiUPクラスタコンポーネントのアップグレードを含む、TiDB クラスターをアップグレードする前に必要な準備作業を紹介します。

### ステップ 1: 互換性の変更を確認する {#step-1-review-compatibility-changes}

TiDB リリース ノートで互換性の変更を確認してください。変更がアップグレードに影響する場合は、それに応じて対処してください。

以下では、v6.4.0 から現在のバージョン (v6.5.2) にアップグレードするときに知っておく必要がある互換性の変更について説明します。 v6.3.0 以前のバージョンから現在のバージョンにアップグレードする場合は、対応する[リリースノート](/releases/release-notes.md)の中間バージョンで導入された互換性の変更も確認する必要がある場合があります。

-   TiDB v6.5.0 [互換性の変更](/releases/release-6.5.0.md#compatibility-changes)および[非推奨の機能](/releases/release-6.5.0.md#deprecated-feature)
-   TiDB v6.5.1 [互換性の変更](/releases/release-6.5.1.md#compatibility-changes)
-   TiDB v6.5.2 [互換性の変更](/releases/release-6.5.2.md#compatibility-changes)

### ステップ 2: TiUPまたはTiUPオフライン ミラーをアップグレードする {#step-2-upgrade-tiup-or-tiup-offline-mirror}

TiDB クラスターをアップグレードする前に、まずTiUPまたはTiUPミラーをアップグレードする必要があります。

#### TiUPおよびTiUPクラスタのアップグレード {#upgrade-tiup-and-tiup-cluster}

> **ノート：**
>
> アップグレードするクラスタの制御マシンが`https://tiup-mirrors.pingcap.com`にアクセスできない場合は、このセクションをスキップして[TiUPオフライン ミラーのアップグレード](#upgrade-tiup-offline-mirror)を参照してください。

1.  TiUPのバージョンアップ。 TiUPのバージョンは`1.11.0`以降を推奨します。

    {{< copyable "" >}}

    ```shell
    tiup update --self
    tiup --version
    ```

2.  TiUPクラスタのバージョンをアップグレードします。 TiUP クラスタ のバージョンは`1.11.0`以降を推奨します。

    {{< copyable "" >}}

    ```shell
    tiup update cluster
    tiup cluster --version
    ```

#### TiUPオフライン ミラーのアップグレード {#upgrade-tiup-offline-mirror}

> **ノート：**
>
> アップグレードするクラスターがオフラインの方法を使用せずにデプロイされた場合は、この手順をスキップしてください。

[TiUPを使用して TiDBクラスタをデプロイ- TiUP をオフラインでデプロイ](/production-deployment-using-tiup.md#deploy-tiup-offline)を参照して、新しいバージョンのTiUPミラーをダウンロードし、制御マシンにアップロードします。 `local_install.sh`を実行すると、 TiUP は上書きアップグレードを完了します。

{{< copyable "" >}}

```shell
tar xzvf tidb-community-server-${version}-linux-amd64.tar.gz
sh tidb-community-server-${version}-linux-amd64/local_install.sh
source /home/tidb/.bash_profile
```

上書きアップグレードの後、次のコマンドを実行して、サーバーとツールキットのオフライン ミラーをサーバーディレクトリにマージします。

{{< copyable "" >}}

```bash
tar xf tidb-community-toolkit-${version}-linux-amd64.tar.gz
ls -ld tidb-community-server-${version}-linux-amd64 tidb-community-toolkit-${version}-linux-amd64
cd tidb-community-server-${version}-linux-amd64/
cp -rp keys ~/.tiup/
tiup mirror merge ../tidb-community-toolkit-${version}-linux-amd64
```

ミラーをマージした後、次のコマンドを実行してTiUP クラスタコンポーネントをアップグレードします。

{{< copyable "" >}}

```shell
tiup update cluster
```

これで、オフライン ミラーが正常にアップグレードされました。上書き後のTiUP操作でエラーが発生した場合、 `manifest`が更新されていない可能性があります。 TiUP を再度実行する前に`rm -rf ~/.tiup/manifests/*`を試すことができます。

### 手順 3: TiUPトポロジ構成ファイルを編集する {#step-3-edit-tiup-topology-configuration-file}

> **ノート：**
>
> 次のいずれかの状況に該当する場合は、この手順をスキップしてください。
>
> -   元のクラスターの構成パラメーターを変更していません。または、 `tiup cluster`を使用して構成パラメーターを変更しましたが、それ以上の変更は必要ありません。
> -   アップグレード後、変更されていない構成アイテムに対して v6.5.2 のデフォルトのパラメーター値を使用したいと考えています。

1.  `vi`編集モードに入り、トポロジ ファイルを編集します。

    {{< copyable "" >}}

    ```shell
    tiup cluster edit-config <cluster-name>
    ```

2.  [トポロジー](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml)構成テンプレートのフォーマットを参照し、変更するパラメーターをトポロジー ファイルの`server_configs`セクションに入力します。

3.  変更後、 <kbd>:</kbd> + <kbd>w</kbd> + <kbd>q</kbd>を入力して変更を保存し、編集モードを終了します。 <kbd>Y</kbd>を入力して変更を確認します。

> **ノート：**
>
> クラスターを v6.5.2 にアップグレードする前に、v4.0 で変更したパラメーターが v6.5.2 で互換性があることを確認してください。詳細については、 [TiKVコンフィグレーションファイル](/tikv-configuration-file.md)を参照してください。

### ステップ 4: 現在のクラスターのヘルス ステータスを確認する {#step-4-check-the-health-status-of-the-current-cluster}

アップグレード中の未定義の動作やその他の問題を回避するには、アップグレード前に現在のクラスターのリージョンのヘルス ステータスを確認することをお勧めします。これを行うには、 `check`サブコマンドを使用できます。

{{< copyable "" >}}

```shell
tiup cluster check <cluster-name> --cluster
```

コマンド実行後、「リージョンの状態」チェック結果が出力されます。

-   結果が「すべてのリージョンが正常」である場合、現在のクラスター内のすべてのリージョンは正常であり、アップグレードを続行できます。
-   結果が「リージョンが完全に正常ではありません: m miss-peer、n pending-peer」の場合、「他の操作の前に異常なリージョンを修正してください」。現在のクラスターの一部のリージョンが異常です。チェック結果が「すべてのリージョンが正常」になるまで、異常をトラブルシューティングする必要があります。その後、アップグレードを続行できます。

### 手順 5: クラスターの DDL とバックアップの状態を確認する {#step-5-check-the-ddl-and-backup-status-of-the-cluster}

アップグレード中の未定義の動作やその他の予期しない問題を回避するために、アップグレードの前に次の項目を確認することをお勧めします。

-   クラスタDDL: [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md)ステートメントを実行して、進行中の DDL ジョブがあるかどうかを確認することをお勧めします。はいの場合は、その実行を待つか、アップグレードを実行する前に[`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)ステートメントを実行してキャンセルします。
-   クラスタバックアップ: [`SHOW [BACKUPS|RESTORES]`](/sql-statements/sql-statement-show-backups.md)ステートメントを実行して、クラスタ内で進行中のバックアップまたは復元タスクがあるかどうかを確認することをお勧めします。 「はい」の場合は、アップグレードが完了するまで待ってからアップグレードを実行してください。

## TiDB クラスターをアップグレードする {#upgrade-the-tidb-cluster}

このセクションでは、TiDB クラスターをアップグレードし、アップグレード後にバージョンを確認する方法について説明します。

### TiDB クラスターを指定されたバージョンにアップグレードする {#upgrade-the-tidb-cluster-to-a-specified-version}

クラスタは、オンライン アップグレードとオフライン アップグレードの 2 つの方法のいずれかでアップグレードできます。

デフォルトでは、 TiUPクラスタはオンライン方式を使用して TiDB クラスターをアップグレードします。これは、TiDB クラスターがアップグレード プロセス中にサービスを提供できることを意味します。オンライン方式では、リーダーはアップグレードと再起動の前に各ノードで 1 つずつ移行されます。したがって、大規模なクラスターの場合、アップグレード操作全体を完了するには長い時間がかかります。

メンテナンスのためにデータベースを停止するメンテナンス ウィンドウがアプリケーションにある場合は、オフライン アップグレード方法を使用して、アップグレード操作をすばやく実行できます。

#### オンラインアップグレード {#online-upgrade}

{{< copyable "" >}}

```shell
tiup cluster upgrade <cluster-name> <version>
```

たとえば、クラスターを v6.5.2 にアップグレードする場合:

{{< copyable "" >}}

```shell
tiup cluster upgrade <cluster-name> v6.5.2
```

> **ノート：**
>
> -   オンライン アップグレードでは、すべてのコンポーネントが 1 つずつアップグレードされます。 TiKV のアップグレード中、TiKV インスタンス内のすべてのリーダーは、インスタンスを停止する前に削除されます。デフォルトのタイムアウト時間は 5 分 (300 秒) です。このタイムアウト時間が経過すると、インスタンスは直接停止されます。
>
> -   `--force`パラメーターを使用して、リーダーを削除せずにすぐにクラスターをアップグレードできます。ただし、アップグレード中に発生するエラーは無視されます。つまり、アップグレードの失敗は通知されません。したがって、 `--force`パラメータは注意して使用してください。
>
> -   安定したパフォーマンスを維持するには、インスタンスを停止する前に、TiKV インスタンス内のすべてのリーダーが削除されていることを確認してください。 `--transfer-timeout` `--transfer-timeout 3600` (単位: 秒) など、より大きな値に設定できます。
>
> -   TiFlash を5.3 より前のバージョンから 5.3 以降にアップグレードするには、 TiFlashを停止してからアップグレードする必要があります。次の手順は、他のコンポーネントを中断することなくTiFlashをアップグレードするのに役立ちます。
>     1.  TiFlashインスタンスを停止します: `tiup cluster stop <cluster-name> -R tiflash`
>     2.  再起動せずに TiDB クラスターをアップグレードします (ファイルの更新のみ): `tiup cluster upgrade <cluster-name> <version> --offline` 、 `tiup cluster upgrade <cluster-name> v6.3.0 --offline`など
>     3.  TiDB クラスターをリロードします。 `tiup cluster reload <cluster-name>` .リロード後、 TiFlashインスタンスが開始されるため、手動で開始する必要はありません。
>
> -   TiDB Binlogを使用してクラスターにローリング更新を適用するときは、新しいクラスター化インデックス テーブルを作成しないようにしてください。

#### オフライン アップグレード {#offline-upgrade}

1.  オフライン アップグレードの前に、まずクラスター全体を停止する必要があります。

    {{< copyable "" >}}

    ```shell
    tiup cluster stop <cluster-name>
    ```

2.  `upgrade`コマンドと`--offline`オプションを使用して、オフライン アップグレードを実行します。 `<cluster-name>`にはクラスターの名前を入力し、 `<version>`にはアップグレードするバージョン`v6.5.2`など) を入力します。

    {{< copyable "" >}}

    ```shell
    tiup cluster upgrade <cluster-name> <version> --offline
    ```

3.  アップグレード後、クラスターは自動的に再起動されません。 `start`コマンドを使用して再起動する必要があります。

    {{< copyable "" >}}

    ```shell
    tiup cluster start <cluster-name>
    ```

### クラスターのバージョンを確認する {#verify-the-cluster-version}

`display`コマンドを実行して、最新のクラスター バージョン`TiDB Version`を表示します。

{{< copyable "" >}}

```shell
tiup cluster display <cluster-name>
```

```
Cluster type:       tidb
Cluster name:       <cluster-name>
Cluster version:    v6.5.2
```

## FAQ {#faq}

このセクションでは、 TiUPを使用して TiDB クラスターを更新するときに発生する一般的な問題について説明します。

### エラーが発生してアップグレードが中断された場合、このエラーを修正した後にアップグレードを再開するにはどうすればよいですか? {#if-an-error-occurs-and-the-upgrade-is-interrupted-how-to-resume-the-upgrade-after-fixing-this-error}

`tiup cluster upgrade`コマンドを再実行して、アップグレードを再開します。アップグレード操作により、以前にアップグレードされたノードが再起動されます。アップグレードしたノードを再起動したくない場合は、 `replay`サブコマンドを使用して操作を再試行します。

1.  `tiup cluster audit`を実行して操作記録を表示します。

    {{< copyable "" >}}

    ```shell
    tiup cluster audit
    ```

    失敗したアップグレード操作レコードを見つけて、この操作レコードの ID を保持します。 ID は、次のステップの`<audit-id>`値です。

2.  `tiup cluster replay <audit-id>`を実行して、対応する操作を再試行します。

    {{< copyable "" >}}

    ```shell
    tiup cluster replay <audit-id>
    ```

### エビクト リーダーは、アップグレード中に長時間待機しました。迅速なアップグレードのためにこの手順をスキップするにはどうすればよいですか? {#the-evict-leader-has-waited-too-long-during-the-upgrade-how-to-skip-this-step-for-a-quick-upgrade}

`--force`を指定できます。その後、PD リーダーの転送と TiKV リーダーの削除のプロセスは、アップグレード中にスキップされます。クラスターを直接再起動してバージョンを更新するため、オンラインで実行されるクラスターに大きな影響を与えます。次のコマンドで、 `<version>` `v6.5.2`などのアップグレード先のバージョンです。

{{< copyable "" >}}

```shell
tiup cluster upgrade <cluster-name> <version> --force
```

### TiDB クラスターをアップグレードした後、pd-ctl などのツールのバージョンを更新する方法を教えてください。 {#how-to-update-the-version-of-tools-such-as-pd-ctl-after-upgrading-the-tidb-cluster}

TiUPを使用して、対応するバージョンの`ctl`コンポーネントをインストールすることで、ツールのバージョンをアップグレードできます。

{{< copyable "" >}}

```shell
tiup install ctl:v6.5.2
```
