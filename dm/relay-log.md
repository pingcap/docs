---
title: Data Migration Relay Log
summary: Learn the directory structure, initial migration rules and data purge of DM relay logs.
---

# データ移行中継ログ {#data-migration-relay-log}

データ移行 (DM) リレー ログは、データベースの変更を説明するイベントを含む番号付きファイルのいくつかのセットと、使用されたすべてのリレー ログ ファイルの名前を含むインデックス ファイルで構成されます。

リレー ログを有効にすると、DM-worker はアップストリームのbinlog をローカル構成ディレクトリに自動的に移行します (DM がTiUPを使用してデプロイされている場合、デフォルトの移行ディレクトリは`<deploy_dir>/<relay_log>`です)。 `<relay_log>`のデフォルト値は`relay-dir`で、 [アップストリーム データベースコンフィグレーションファイル](/dm/dm-source-configuration-file.md)で変更できます。 v5.4.0 以降、 [DM-worker 構成ファイル](/dm/dm-worker-configuration-file.md)の`relay-dir`までローカル構成ディレクトリを構成できます。これは、アップストリーム データベースの構成ファイルよりも優先されます。

> **警告：**
>
> アップストリーム データベース構成ファイルの`relay-dir` 、v6.1 で非推奨としてマークされており、将来のリリースで削除される可能性があります。関連するコマンドの出力に、 `` `relay-dir` in source config will be deprecated soon, please use `relay-dir` in worker config instead``のプロンプトが表示されます。

DM-worker が実行されている場合、上流のbinlog をリアルタイムでローカル ファイルに移行します。 DM-worker の同期処理ユニットは、ローカル リレー ログのbinlogイベントをリアルタイムで読み取り、これらのイベントを SQL ステートメントに変換してから、これらのステートメントを下流のデータベースに移行します。

このドキュメントでは、DM リレー ログのディレクトリ構造と初期移行ルール、およびリレー ログの一時停止、再開、パージの方法について説明します。

> **ノート：**
>
> リレー ログ機能では、追加のディスク I/O 操作が必要になるため、データ移行のレイテンシーが長くなります。展開環境のディスク I/O パフォーマンスが低い場合、リレー ログ機能が移行タスクのボトルネックになり、移行が遅くなる可能性があります。

## ディレクトリ構造 {#directory-structure}

リレー ログのローカルstorageのディレクトリ構造の例:

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

-   `subdir` :

    -   DM-worker は、アップストリーム データベースから移行されたbinlog を同じディレクトリに保存します。各ディレクトリは`subdir`です。

    -   `subdir`は`<Upstream database UUID>.<Local subdir serial number>`という名前です。

    -   アップストリームでプライマリ インスタンスとセカンダリ インスタンスを切り替えた後、DM-worker は増分シリアル番号を持つ新しい`subdir`ディレクトリを生成します。

        -   上記の例では、 `7e427cc0-091c-11e9-9e45-72b7c59d52d7.000001`ディレクトリの場合、 `7e427cc0-091c-11e9-9e45-72b7c59d52d7`アップストリーム データベースの UUID であり、 `000001`はローカル`subdir`シリアル番号です。

-   `server-uuid.index` : 現在使用可能な`subdir`ディレクトリの名前のリストを記録します。

-   `relay.meta` : 移行されたbinlogの情報を`subdir`ごとに格納します。例えば、

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

リレー ログの移行の開始位置は、次の規則によって決定されます。

-   ダウンストリーム同期ユニットのチェックポイントから、DM は最初に、移行タスクがデータ ソースからレプリケートする必要がある最も早い位置を取得します。ポジションが次のいずれかのポジションより遅い場合、DM-worker はこのポジションから移行を開始します。

-   有効なローカル リレー ログが存在する場合 (有効なリレー ログとは、有効な`server-uuid.index` `subdir`および`relay.meta`ファイルを含むリレー ログです)、DM-worker は`relay.meta`によって記録された位置から移行を再開します。

-   有効なローカル リレー ログが存在しないが、ソース構成ファイルで`relay-binlog-name`または`relay-binlog-gtid`が指定されている場合:

    -   非 GTID モードで`relay-binlog-name`を指定すると、DM-worker は指定されたbinlogファイルからマイグレーションを開始します。
    -   GTID モードで`relay-binlog-gtid`を指定すると、DM-worker は指定された GTID からマイグレーションを開始します。

-   有効なローカル リレー ログが存在せず、DM 構成ファイルで`relay-binlog-name`または`relay-binlog-gtid`が指定されていない場合:

    -   非 GTID モードでは、DM-worker は最初の上流のbinlogから移行を開始し、すべての上流のbinlogファイルを最新のものに順次移行します。

    -   GTID モードでは、DM-worker は最初のアップストリーム GTID から移行を開始します。

        > **ノート：**
        >
        > アップストリーム リレー ログがパージされると、エラーが発生します。この場合、マイグレーションの開始位置を指定するために`relay-binlog-gtid`を設定します。

## リレーログ機能の開始と停止 {#start-and-stop-the-relay-log-feature}

<SimpleTab>

<div label="v5.4.0 and later versions">

v5.4.0 以降のバージョンでは、 `enable-relay` ～ `true`を設定することでリレー ログを有効にできます。 v5.4.0 以降、アップストリーム データ ソースをバインドするときに、DM-worker はデータ ソースの構成の`enable-relay`項目をチェックします。 `enable-relay`が`true`の場合、このデータ ソースに対してリレー ログ機能が有効になります。

詳細な設定方法については、 [アップストリーム データベースコンフィグレーションファイル](/dm/dm-source-configuration-file.md)を参照してください。

さらに、 `start-relay`または`stop-relay`コマンドを使用してデータ ソースの`enable-relay`構成を動的に調整し、リレー ログ イン タイムを有効または無効にすることもできます。

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
> DM v2.0.2 より後の DM v2.0.x および v5.3.0 では、ソース構成ファイルの構成項目`enable-relay`は無効になり、 `start-relay`と`stop-relay`のみを使用してリレー ログを有効または無効にできます。 [データ ソース構成の読み込み](/dm/dm-manage-source.md#operate-data-source)のときに`enable-relay`が`true`に設定されていることを DM が検出すると、次のメッセージが出力されます。
>
> ```
> Please use `start-relay` to specify which workers should pull relay log of relay-enabled sources.
> ```

> **警告：**
>
> この起動方法は、v6.1 で非推奨としてマークされており、将来のリリースで削除される可能性があります。関連するコマンドの出力に、 `start-relay/stop-relay with worker name will be deprecated soon. You can try stopping relay first and use start-relay without worker name instead`のプロンプトが表示されます。

コマンド`start-relay`では、指定されたデータ ソースのリレー ログを移行するように 1 つ以上の DM-worker を構成できますが、パラメーターで指定された DM-worker は解放されているか、上流のデータ ソースにバインドされている必要があります。例は次のとおりです。

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

v2.0.2 より前の DM バージョン (v2.0.2 を除く) では、DM ワーカーをアップストリーム データ ソースにバインドするときに、DM はソース構成ファイルの構成項目`enable-relay`をチェックします。 `enable-relay`が`true`に設定されている場合、DM はデータ ソースのリレー ログ機能を有効にします。

設定項目`enable-relay`の設定方法は[アップストリーム データベースコンフィグレーションファイル](/dm/dm-source-configuration-file.md)を参照してください。

</div>
</SimpleTab>

## リレー ログのクエリ {#query-relay-logs}

コマンド`query-status -s`を使用して、アップストリーム データ ソースのリレー ログ プル プロセスのステータスを照会できます。次の例を参照してください。

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

## リレー ログ機能の一時停止と再開 {#pause-and-resume-the-relay-log-feature}

コマンド`pause-relay`を使用してリレー ログのプル プロセスを一時停止し、コマンド`resume-relay`を使用してプロセスを再開できます。これら 2 つのコマンドを実行するときは、アップストリーム データ ソースの`source-id`指定する必要があります。次の例を参照してください。

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

## リレー ログのパージ {#purge-relay-logs}

ファイルの読み取りと書き込みの検出メカニズムを通じて、DM-worker は、現在実行中のデータ移行タスクによって使用されている、または後で使用されるリレー ログをパージしません。

中継ログのデータ消去方法には、自動消去と手動消去があります。

### 自動データ消去 {#automatic-data-purge}

自動データ消去を有効にして、ソース構成ファイルでその戦略を構成できます。次の例を参照してください。

```yaml
# relay log purge strategy
purge:
    interval: 3600
    expires: 24
    remain-space: 15
```

-   `purge.interval`
    -   バックグラウンドでの自動パージの間隔 (秒単位)。
    -   デフォルトでは「3600」で、バックグラウンド パージ タスクが 3600 秒ごとに実行されることを示します。

-   `purge.expires`
    -   リレー ログ (以前にリレー処理ユニットに書き込まれ、使用されていないか、現在実行中のデータ移行タスクによって後で読み取られることはない) を保持できる時間数。バックグラウンド パージ。
    -   デフォルトは「0」で、リレーログの更新時刻によるデータパージは行われません。

-   `purge.remain-space`
    -   自動バックグラウンド パージで安全にパージできるリレー ログを、指定された DM ワーカー マシンがパージしようとする、GB 単位の残りのディスク容量。 `0`に設定すると、残りのディスク容量に応じてデータのパージは実行されません。
    -   デフォルトの「15」は、使用可能なディスク容量が 15GB 未満になると、DM マスターがリレー ログを安全にパージしようとすることを示します。

### 手動データ消去 {#manual-data-purge}

手動データ消去とは、dmctl が提供する`purge-relay`コマンドを使用して`subdir`とbinlog名を指定し、指定されたbinlog**より前の**すべてのリレー ログを消去することを意味します。コマンドの`-subdir`オプションが指定されていない場合、現在のリレー ログ サブディレクトリ<strong>より前の</strong>すべてのリレー ログが消去されます。

現在のリレーログのディレクトリ構造が次のとおりであると仮定します。

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

-   dmctl で次の`purge-relay`コマンドを実行すると、 `e4e0e8ab-09cc-11e9-9220-82cc35207219.000002/mysql-bin.000001`**より前の**すべてのリレー ログ ファイルがパージされます。これは、 `deb76a2b-09cc-11e9-9129-5242cf3bb246.000001`のすべてのリレー ログ ファイルです。

    {{< copyable "" >}}

    ```bash
    » purge-relay -s mysql-replica-01 --filename mysql-bin.000001 --sub-dir e4e0e8ab-09cc-11e9-9220-82cc35207219.000002
    ```

-   dmctl で次の`purge-relay`コマンドを実行すると、**現在の**( `deb76a2b-09cc-11e9-9129-5242cf3bb246.000003` ) ディレクトリの`mysql-bin.000001`より前のすべてのリレー ログ ファイルが削除されます。これは、 `deb76a2b-09cc-11e9-9129-5242cf3bb246.000001`と`e4e0e8ab-09cc-11e9-9220-82cc35207219.000002`のすべてのリレー ログ ファイルです。

    {{< copyable "" >}}

    ```bash
    » purge-relay -s mysql-replica-01 --filename mysql-bin.000001
    ```
