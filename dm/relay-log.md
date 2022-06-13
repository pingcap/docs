---
title: Data Migration Relay Log
summary: Learn the directory structure, initial migration rules and data purge of DM relay logs.
---

# データ移行リレーログ {#data-migration-relay-log}

データ移行（DM）リレーログは、データベースの変更を説明するイベントを含む番号付きファイルのいくつかのセットと、使用されているすべてのリレーログファイルの名前を含むインデックスファイルで構成されます。

リレーログを有効にすると、DM-workerはアップストリームbinlogをローカル構成ディレクトリに自動的に移行します（DMがTiUPを使用してデプロイされている場合、デフォルトの移行ディレクトリは`<deploy_dir>/<relay_log>`です）。デフォルト値の`<relay_log>`は`relay-dir`で、 [アップストリームデータベースConfiguration / コンフィグレーションファイル](/dm/dm-source-configuration-file.md)で変更できます。 v5.4.0以降、 [DM-worker構成ファイル](/dm/dm-worker-configuration-file.md)の`relay-dir`からローカル構成ディレクトリを構成できます。これは、アップストリーム・データベースの構成ファイルよりも優先されます。

> **警告：**
>
> アップストリームデータベース構成ファイルの`relay-dir`は、v6.1で非推奨としてマークされており、将来のリリースで削除される可能性があります。関連するコマンドの出力に次のプロンプトが表示されます`` `relay-dir` in source config will be deprecated soon, please use `relay-dir` in worker config instead`` 。

DM-workerが実行されている場合、アップストリームのbinlogをローカルファイルにリアルタイムで移行します。 DM-workerの同期処理ユニットは、ローカルリレーログのbinlogイベントをリアルタイムで読み取り、これらのイベントをSQLステートメントに変換してから、これらのステートメントをダウンストリームデータベースに移行します。

このドキュメントでは、ディレクトリ構造と初期移行ルールのDMリレーログ、およびリレーログを一時停止、再開、およびパージする方法を紹介します。

> **ノート：**
>
> リレーログ機能には追加のディスクI/O操作が必要であるため、データ移行の待ち時間が長くなります。展開環境でのディスクI/Oのパフォーマンスが低い場合、リレーログ機能が移行タスクのボトルネックになり、移行が遅くなる可能性があります。

## ディレクトリ構造 {#directory-structure}

リレーログのローカルストレージのディレクトリ構造の例：

```
<deploy_dir>/<relay_log>/
|-- 7e427cc0-091c-11e9-9e45-72b7c59d52d7.000001
|   |-- mysql-bin.000001
|   |-- mysql-bin.000002
|   |-- mysql-bin.000003
|   |-- mysql-bin.000004
|   `-- relay.meta
|-- 842965eb-091c-11e9-9e45-9a3bff03fa39.000002
|   |-- mysql-bin.000001
|   `-- relay.meta
`-- server-uuid.index
```

-   `subdir` ：

    -   DM-workerは、アップストリームデータベースから移行されたbinlogを同じディレクトリに保存します。各ディレクトリは`subdir`です。

    -   `subdir`は`<Upstream database UUID>.<Local subdir serial number>`という名前です。

    -   アップストリームでプライマリインスタンスとセカンダリインスタンスを切り替えた後、DM-workerは増分シリアル番号を使用して新しい`subdir`ディレクトリを生成します。

        -   上記の例では、 `7e427cc0-091c-11e9-9e45-72b7c59d52d7.000001`ディレクトリの場合、 `7e427cc0-091c-11e9-9e45-72b7c59d52d7`はアップストリームデータベースのUUIDであり、 `000001`はローカル`subdir`のシリアル番号です。

-   `server-uuid.index` ：現在利用可能な`subdir`ディレクトリの名前のリストを記録します。

-   `relay.meta` ：移行されたbinlogの情報を各`subdir`に格納します。例えば、

    ```bash
    $ cat c0149e17-dff1-11e8-b6a8-0242ac110004.000001/relay.meta
    binlog-name = "mysql-bin.000010"                            # The name of the currently migrated binlog.
    binlog-pos = 63083620                                       # The position of the currently migrated binlog.
    binlog-gtid = "c0149e17-dff1-11e8-b6a8-0242ac110004:1-3328" # GTID of the currently migrated binlog.
                                                                # There might be multiple GTIDs.
    $ cat 92acbd8a-c844-11e7-94a1-1866daf8accc.000001/relay.meta
    binlog-name = "mysql-bin.018393"
    binlog-pos = 277987307
    binlog-gtid = "3ccc475b-2343-11e7-be21-6c0b84d59f30:1-14,406a3f61-690d-11e7-87c5-6c92bf46f384:1-94321383,53bfca22-690d-11e7-8a62-18ded7a37b78:1-495,686e1ab6-c47e-11e7-a42c-6c92bf46f384:1-34981190,03fc0263-28c7-11e7-a653-6c0b84d59f30:1-7041423,05474d3c-28c7-11e7-8352-203db246dd3d:1-170,10b039fc-c843-11e7-8f6a-1866daf8d810:1-308290454"
    ```

## 初期移行ルール {#initial-migration-rules}

リレーログ移行の開始位置は、次のルールによって決定されます。

-   ダウンストリーム同期ユニットのチェックポイントから、DMは最初に、移行タスクがデータソースから複製する必要がある最も早い位置を取得します。ポジションが以下のポジションのいずれよりも遅い場合、DM-workerはこのポジションから移行を開始します。

-   有効なローカルリレーログが存在する場合（有効なリレーログは、有効な`server-uuid.index` 、および`subdir`ファイルの`relay.meta`です）、DM-workerは`relay.meta`によって記録された位置から移行を再開します。

-   有効なローカルリレーログが存在しないが、ソース設定ファイルで`relay-binlog-name`または`relay-binlog-gtid`が指定されている場合：

    -   非GTIDモードでは、 `relay-binlog-name`が指定されている場合、DM-workerは指定されたbinlogファイルから移行を開始します。
    -   GTIDモードでは、 `relay-binlog-gtid`が指定されている場合、DM-workerは指定されたGTIDからの移行を開始します。

-   有効なローカルリレーログが存在せず、DM構成ファイルで`relay-binlog-name`または`relay-binlog-gtid`が指定されていない場合：

    -   非GTIDモードでは、DM-workerは最初のアップストリームbinlogからの移行を開始し、すべてのアップストリームbinlogファイルを最新のものに連続して移行します。

    -   GTIDモードでは、DM-workerは最初のアップストリームGTIDから移行を開始します。

        > **ノート：**
        >
        > アップストリームリレーログがパージされると、エラーが発生します。この場合、移行の開始位置を指定するには`relay-binlog-gtid`を設定します。

## リレーログ機能を開始および停止します {#start-and-stop-the-relay-log-feature}

<SimpleTab>

<div label="v5.4.0 and later versions">

v5.4.0以降のバージョンでは、 `enable-relay`を`true`に設定することでリレーログを有効にできます。 v5.4.0以降、アップストリームデータソースをバインドするときに、DM-workerはデータソースの構成の`enable-relay`の項目をチェックします。 `enable-relay`が`true`の場合、このデータソースに対してリレーログ機能が有効になります。

詳細な設定方法については、 [アップストリームデータベースConfiguration / コンフィグレーションファイル](/dm/dm-source-configuration-file.md)を参照してください。

さらに、 `start-relay`または`stop-relay`コマンドを使用してデータソースの`enable-relay`構成を動的に調整し、リレーログイン時間を有効または無効にすることもできます。

{{< copyable "" >}}

```bash
» start-relay -s mysql-replica-01
```

```
{
    "result": true,
    "msg": ""
}
```

</div>

<div label="versions between v2.0.2 (included) and v5.3.0 (included)">

> **ノート：**
>
> DMv2.0.2より後のDMv2.0.xおよびv5.3.0では、ソース構成ファイルの構成項目`enable-relay`は無効になり、リレーログの有効化と無効化に使用できるのは`start-relay`と`stop-relay`のみです。 DMは、 [データソース構成のロード](/dm/dm-manage-source.md#operate-data-source)のときに`enable-relay`が`true`に設定されていることを検出すると、次のメッセージを出力します。
>
> ```
> Please use `start-relay` to specify which workers should pull relay log of relay-enabled sources.
> ```

> **警告：**
>
> この起動方法はv6.1で非推奨としてマークされており、将来のリリースで削除される可能性があります。関連するコマンドの出力に次のプロンプトが表示されます`start-relay/stop-relay with worker name will be deprecated soon. You can try stopping relay first and use start-relay without worker name instead` 。

コマンド`start-relay`では、指定されたデータソースのリレーログを移行するように1つ以上のDM-workerを構成できますが、パラメーターで指定されたDM-workerは解放されているか、アップストリームデータソースにバインドされている必要があります。例は次のとおりです。

{{< copyable "" >}}

```bash
» start-relay -s mysql-replica-01 worker1 worker2
```

```
{
    "result": true,
    "msg": ""
}
```

{{< copyable "" >}}

```bash
» stop-relay -s mysql-replica-01 worker1 worker2
```

```
{
    "result": true,
    "msg": ""
}
```

</div>

<div label="earlier than v2.0.2">

v2.0.2より前のバージョン（v2.0.2を含まない）では、DMワーカーをアップストリームデータソースにバインドするときに、DMはソース構成ファイルの構成項目`enable-relay`をチェックします。 `enable-relay`が`true`に設定されている場合、DMはデータソースのリレーログ機能を有効にします。

構成項目`enable-relay`の設定方法については、 [アップストリームデータベースConfiguration / コンフィグレーションファイル](/dm/dm-source-configuration-file.md)を参照してください。

</div>
</SimpleTab>

## リレーログのクエリ {#query-relay-logs}

コマンド`query-status -s`を使用して、アップストリームデータソースのリレーログプルプロセスのステータスを照会できます。次の例を参照してください。

{{< copyable "" >}}

```bash
» query-status -s mysql-replica-01
```

```
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "no sub task started",
            "sourceStatus": {
                "source": "mysql-replica-01",
                "worker": "worker2",
                "result": null,
                "relayStatus": {
                    "masterBinlog": "(mysql-bin.000005, 916)",
                    "masterBinlogGtid": "09bec856-ba95-11ea-850a-58f2b4af5188:1-28",
                    "relaySubDir": "09bec856-ba95-11ea-850a-58f2b4af5188.000001",
                    "relayBinlog": "(mysql-bin.000005, 4)",
                    "relayBinlogGtid": "09bec856-ba95-11ea-850a-58f2b4af5188:1-28",
                    "relayCatchUpMaster": false,
                    "stage": "Running",
                    "result": null
                }
            },
            "subTaskStatus": [
            ]
        },
        {
            "result": true,
            "msg": "no sub task started",
            "sourceStatus": {
                "source": "mysql-replica-01",
                "worker": "worker1",
                "result": null,
                "relayStatus": {
                    "masterBinlog": "(mysql-bin.000005, 916)",
                    "masterBinlogGtid": "09bec856-ba95-11ea-850a-58f2b4af5188:1-28",
                    "relaySubDir": "09bec856-ba95-11ea-850a-58f2b4af5188.000001",
                    "relayBinlog": "(mysql-bin.000005, 916)",
                    "relayBinlogGtid": "",
                    "relayCatchUpMaster": true,
                    "stage": "Running",
                    "result": null
                }
            },
            "subTaskStatus": [
            ]
        }
    ]
}
```

## リレーログ機能を一時停止して再開します {#pause-and-resume-the-relay-log-feature}

コマンド`pause-relay`を使用してリレーログのプルプロセスを一時停止し、コマンド`resume-relay`を使用してプロセスを再開できます。これらの2つのコマンドを実行するときは、アップストリームデータソースの`source-id`を指定する必要があります。次の例を参照してください。

{{< copyable "" >}}

```bash
» pause-relay -s mysql-replica-01 -s mysql-replica-02
```

```
{
    "op": "PauseRelay",
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "source": "mysql-replica-01",
            "worker": "worker1"
        },
        {
            "result": true,
            "msg": "",
            "source": "mysql-replica-02",
            "worker": "worker2"
        }
    ]
}
```

{{< copyable "" >}}

```bash
» resume-relay -s mysql-replica-01
```

```
{
    "op": "ResumeRelay",
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "source": "mysql-replica-01",
            "worker": "worker1"
        }
    ]
}
```

## リレーログを削除する {#purge-relay-logs}

DM-workerは、ファイルの読み取りと書き込みの検出メカニズムを通じて、現在実行中のデータ移行タスクによって使用されている、または後で使用されるリレーログを削除しません。

リレーログのデータパージ方法には、自動パージと手動パージが含まれます。

### 自動データパージ {#automatic-data-purge}

自動データパージを有効にして、ソース構成ファイルでその戦略を構成できます。次の例を参照してください。

```yaml
# relay log purge strategy
purge:
    interval: 3600
    expires: 24
    remain-space: 15
```

-   `purge.interval`
    -   バックグラウンドでの自動パージの間隔（秒単位）。
    -   デフォルトでは「3600」で、バックグラウンドパージタスクが3600秒ごとに実行されることを示します。

-   `purge.expires`
    -   自動でパージされる前に、リレーログ（以前にリレー処理装置に書き込まれ、使用されていないか、現在実行中のデータ移行タスクによって後で読み取られない）を保持できる時間数。バックグラウンドパージ。
    -   デフォルトでは「0」。リレーログの更新時間に従ってデータパージが実行されないことを示します。

-   `purge.remain-space`
    -   指定されたDMワーカーマシンが自動バックグラウンドパージで安全にパージできるリレーログをパージしようとするGB単位の残りのディスク容量。 `0`に設定されている場合、残りのディスク容量に応じてデータのパージは実行されません。
    -   デフォルトでは「15」で、使用可能なディスク容量が15GB未満の場合、DMマスターはリレーログを安全にパージしようとします。

### 手動データパージ {#manual-data-purge}

手動データパージとは、dmctlが提供する`purge-relay`コマンドを使用して`subdir`とbinlog名を指定し、指定されたbinlogの**前に**すべてのリレーログをパージすることを意味します。コマンドの`-subdir`オプションが指定されていない場合、現在のリレーログサブディレクトリ<strong>より前</strong>のすべてのリレーログが削除されます。

現在のリレーログのディレクトリ構造が次のようになっていると仮定します。

```
$ tree .
.
|-- deb76a2b-09cc-11e9-9129-5242cf3bb246.000001
|   |-- mysql-bin.000001
|   |-- mysql-bin.000002
|   |-- mysql-bin.000003
|   `-- relay.meta
|-- deb76a2b-09cc-11e9-9129-5242cf3bb246.000003
|   |-- mysql-bin.000001
|   `-- relay.meta
|-- e4e0e8ab-09cc-11e9-9220-82cc35207219.000002
|   |-- mysql-bin.000001
|   `-- relay.meta
`-- server-uuid.index

$ cat server-uuid.index
deb76a2b-09cc-11e9-9129-5242cf3bb246.000001
e4e0e8ab-09cc-11e9-9220-82cc35207219.000002
deb76a2b-09cc-11e9-9129-5242cf3bb246.000003
```

-   dmctlで次の`purge-relay`コマンドを実行すると、 `e4e0e8ab-09cc-11e9-9220-82cc35207219.000002/mysql-bin.000001`**より前**のすべてのリレーログファイルが削除されます。これは、 `deb76a2b-09cc-11e9-9129-5242cf3bb246.000001`のすべてのリレーログファイルです。

    {{< copyable "" >}}

    ```bash
    » purge-relay -s mysql-replica-01 --filename mysql-bin.000001 --sub-dir e4e0e8ab-09cc-11e9-9220-82cc35207219.000002
    ```

-   dmctlで次の`purge-relay`コマンドを実行する**と、現在の**（ `deb76a2b-09cc-11e9-9129-5242cf3bb246.000003` ）ディレクトリの`mysql-bin.000001`の前にあるすべてのリレーログファイルが削除されます。これは、 `deb76a2b-09cc-11e9-9129-5242cf3bb246.000001`と`e4e0e8ab-09cc-11e9-9220-82cc35207219.000002`のすべてのリレーログファイルです。

    {{< copyable "" >}}

    ```bash
    » purge-relay -s mysql-replica-01 --filename mysql-bin.000001
    ```
