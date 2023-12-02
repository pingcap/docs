---
title: Data Migration Relay Log
summary: Learn the directory structure, initial migration rules and data purge of DM relay logs.
---

# データ移行リレーログ {#data-migration-relay-log}

データ移行 (DM) リレー ログは、データベースの変更を説明するイベントを含む番号付きファイルのいくつかのセットと、使用されるすべてのリレー ログ ファイルの名前を含むインデックス ファイルで構成されます。

リレー ログが有効になると、DM ワーカーはアップストリームのbinlogをローカル構成ディレクトリに自動的に移行します ( TiUPを使用して DM が展開されている場合、デフォルトの移行ディレクトリは`<deploy_dir>/<relay_log>`です)。デフォルト値`<relay_log>`は`relay-dir`ですが、 [アップストリーム データベースコンフィグレーションファイル](/dm/dm-source-configuration-file.md)で変更できます。 v5.4.0 以降、ローカル構成ディレクトリを`relay-dir`から[DM ワーカー設定ファイル](/dm/dm-worker-configuration-file.md)まで構成できます。これは、アップストリーム データベースの構成ファイルよりも優先されます。

## ユーザーシナリオ {#user-scenarios}

MySQL では、storage容量が限られているため、最大保持時間に達すると、binlogは自動的に消去されます。アップストリーム データベースがbinlogをパージした後、DM はパージされたbinlog のプルに失敗し、移行タスクは失敗します。移行タスクごとに、DM はbinlogをプルするための接続をアップストリームに作成します。接続が多すぎると、アップストリーム データベースに大きな負荷がかかる可能性があります。

リレー ログが有効になっている場合、同じアップストリーム データベースを持つ複数の移行タスクで、ローカル ディスクにプルされたリレー ログを再利用できます。これにより、**上流データベースへの負担が軽減されます**。

完全データ移行タスクと増分データ移行タスク ( `task-mode=all` ) の場合、DM は最初に完全データを移行し、次にbinlogに基づいて増分移行を実行する必要があります。完全な移行フェーズに時間がかかると、上流のbinlogがパージされ、増分移行が失敗する可能性があります。この状況を回避するには、リレー ログ機能を有効にして、DM がローカル ディスクに十分なログを自動的に保持し、**増分移行タスクが正常に実行できるようにします**。

通常はリレー ログを有効にすることが推奨されますが、次の潜在的な問題に注意してください。

リレー ログはディスクに書き込む必要があるため、外部 IO および CPU リソースを消費します。これにより、データ複製プロセス全体が延長され、データ複製のレイテンシーが増加します。**遅延の影響を受ける**シナリオでは、リレー ログを有効にすることはお勧めできません。

> **注記：**
>
> DM v2.0.7 以降のバージョンでは、リレー ログの書き込みが最適化されています。レイテンシーと CPU リソースの消費量は比較的低いです。

## リレーログを使用する {#use-relay-log}

このセクションでは、リレー ログの有効化と無効化、リレー ログのステータスのクエリ、およびリレー ログのパージの方法について説明します。

### リレーログの有効化と無効化 {#enable-and-disable-relay-log}

<SimpleTab>

<div label="v5.4.0 and later versions">

v5.4.0 以降のバージョンでは、 `enable-relay` ～ `true`を設定することでリレー ログを有効にできます。 v5.4.0 以降、DM-worker は上流データ ソースをバインドするときに、データ ソースの設定の`enable-relay`項目をチェックします。 `enable-relay`が`true`の場合、このデータ ソースに対してリレー ログ機能が有効になります。

詳しい設定方法については[アップストリーム データベースコンフィグレーションファイル](/dm/dm-source-configuration-file.md)を参照してください。

さらに、 `start-relay`または`stop-relay`コマンドを使用してデータ ソースの構成を`enable-relay`に調整し、リレー ログイン時間を有効または無効にすることもできます。

```bash
start-relay -s mysql-replica-01
```

    {
        "result": true,
        "msg": ""
    }

</div>

<div label="versions between v2.0.2 (included) and v5.3.0 (included)">

> **注記：**
>
> DM v2.0.2 より後の DM v2.0.x および v5.3.0 では、ソース設定ファイルの設定項目`enable-relay`は無効になり、リレー ログを有効または無効にするために使用できるのは`start-relay`と`stop-relay`のみです。 DM は、 [データソース構成のロード](/dm/dm-manage-source.md#operate-data-source)のときに`enable-relay` `true`に設定されていることを検出すると、次のメッセージを出力します。
>
>     Please use `start-relay` to specify which workers should pull relay log of relay-enabled sources.

> **警告：**
>
> この起動方法は v6.1 では非推奨としてマークされており、将来のリリースでは削除される可能性があります。関連するコマンドの出力に`start-relay/stop-relay with worker name will be deprecated soon. You can try stopping relay first and use start-relay without worker name instead`のプロンプトが表示されます。

コマンド`start-relay`では、指定されたデータ ソースのリレー ログを移行するように 1 つ以上の DM ワーカーを構成できますが、パラメータで指定された DM ワーカーはフリーであるか、アップストリーム データ ソースにバインドされている必要があります。例は次のとおりです。

```bash
start-relay -s mysql-replica-01 worker1 worker2
```

    {
        "result": true,
        "msg": ""
    }

```bash
stop-relay -s mysql-replica-01 worker1 worker2
```

    {
        "result": true,
        "msg": ""
    }

</div>

<div label="earlier than v2.0.2">

v2.0.2 より前の DM バージョン (v2.0.2 を除く) では、DM は、DM ワーカーをアップストリーム データ ソースにバインドするときに、ソース構成ファイル内の構成項目`enable-relay`をチェックします。 `enable-relay`が`true`に設定されている場合、DM はデータ ソースのリレー ログ機能を有効にします。

設定項目`enable-relay`の設定方法は[アップストリーム データベースコンフィグレーションファイル](/dm/dm-source-configuration-file.md)を参照してください。

</div>
</SimpleTab>

### リレーログステータスのクエリ {#query-relay-log-status}

コマンド`query-status -s`を使用して、リレー ログのステータスをクエリできます。

```bash
query-status -s mysql-replica-01
```

<details><summary>期待される出力</summary>

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

</details>

### リレーログの一時停止と再開 {#pause-and-resume-relay-log}

コマンド`pause-relay`を使用してリレー ログの取得プロセスを一時停止し、コマンド`resume-relay`を使用してプロセスを再開できます。これら 2 つのコマンドを実行するときは、上流データ ソースの`source-id`を指定する必要があります。次の例を参照してください。

```bash
pause-relay -s mysql-replica-01 -s mysql-replica-02
```

<details><summary>期待される出力</summary>

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

</details>

```bash
resume-relay -s mysql-replica-01
```

<details><summary>期待される出力</summary>

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

</details>

### リレーログをパージする {#purge-relay-logs}

DM では、手動パージと自動パージという 2 つの方法でリレー ログをパージできます。これら 2 つの方法はいずれも、アクティブなリレー ログをパージしません。

> **注記：**
>
> -   アクティブなリレー ログ: リレー ログはデータ移行タスクによって使用されています。現在、アクティブなリレー ログは Syncer Unit にのみ更新および書き込まれます。すべてモードのデータ移行タスクが完全なエクスポート/インポートに、データ ソースのパージで構成された有効期限よりも長い時間を費やした場合でも、リレー ログはパージされます。
>
> -   期限切れのリレー ログ: リレー ログ ファイルの最終変更時刻と現在時刻の差が、設定ファイルの`expires`フィールドの値を超えています。

#### 自動パージ {#automatic-purge}

自動パージを有効にし、ソース構成ファイルでその戦略を構成できます。次の例を参照してください。

```yaml
# relay log purge strategy
purge:
    interval: 3600
    expires: 24
    remain-space: 15
```

-   `purge.interval`
    -   バックグラウンドでの自動パージの間隔 (秒単位)。
    -   デフォルトは「3600」で、バックグラウンド消去タスクが 3600 秒ごとに実行されることを示します。

-   `purge.expires`
    -   リレー ログ (以前にリレー処理ユニットに書き込まれ、使用されていない、または現在実行中のデータ移行タスクによって後で読み取られない) が自動ログ ファイルでパージされるまで保持できる時間数。バックグラウンドパージ。
    -   デフォルトは「0」で、リレーログの更新時間に応じたデータパージは行われません。

-   `purge.remain-space`
    -   指定された DM ワーカー マシンがリレー ログのパージを試行する残りのディスク容量 (GB 単位)。自動バックグラウンド パージで安全にパージできます。 `0`に設定すると、残りのディスク容量に応じてデータのパージは実行されません。
    -   デフォルトは「15」で、使用可能なディスク容量が 15 GB 未満の場合、DM マスターはリレー ログを安全にパージしようとします。

#### 手動パージ {#manual-purge}

手動パージとは、dmctl によって提供される`purge-relay`コマンドを使用して`subdir`とbinlog名を指定し、指定されたbinlog**より前の**すべてのリレー ログをパージすることを意味します。コマンドで`-subdir`オプションが指定されていない場合、現在のリレー ログ サブディレクトリ**より前の**すべてのリレー ログが消去されます。

現在のリレーログのディレクトリ構造が次のとおりであると仮定します。

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

-   dmctl で次の`purge-relay`コマンドを実行すると、 `e4e0e8ab-09cc-11e9-9220-82cc35207219.000002/mysql-bin.000001`**より前**のすべてのリレー ログ ファイル ( `deb76a2b-09cc-11e9-9129-5242cf3bb246.000001`のすべてのリレー ログ ファイル) がパージされます。 `e4e0e8ab-09cc-11e9-9220-82cc35207219.000002`と`deb76a2b-09cc-11e9-9129-5242cf3bb246.000003`のファイルは保持されます。

    ```bash
    purge-relay -s mysql-replica-01 --filename mysql-bin.000001 --sub-dir e4e0e8ab-09cc-11e9-9220-82cc35207219.000002
    ```

-   dmctl で次の`purge-relay`コマンドを実行すると、**現在の**( `deb76a2b-09cc-11e9-9129-5242cf3bb246.000003` ) ディレクトリの`mysql-bin.000001`より前のすべてのリレー ログ ファイル ( `deb76a2b-09cc-11e9-9129-5242cf3bb246.000001`および`e4e0e8ab-09cc-11e9-9220-82cc35207219.000002`のすべてのリレー ログ ファイル) がパージされます。 `deb76a2b-09cc-11e9-9129-5242cf3bb246.000003`のファイルは保持されます。

    ```bash
    purge-relay -s mysql-replica-01 --filename mysql-bin.000001
    ```

## リレーログの内部仕組み {#internal-mechanism-of-relay-log}

ここではリレーログの内部仕組みを紹介します。

### ディレクトリ構造 {#directory-structure}

リレー ログのローカルstorageのディレクトリ構造の例:

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

-   `subdir` :

    -   DM-worker は、上流データベースから移行されたbinlogを同じディレクトリに保存します。各ディレクトリは`subdir`です。

    -   `subdir`は`<Upstream database UUID>.<Local subdir serial number>`の形式で名前が付けられます。

    -   アップストリームでプライマリ インスタンスとセカンダリ インスタンスが切り替わった後、DM ワーカーは増分シリアル番号を持つ新しい`subdir`ディレクトリを生成します。

    -   上記の例では、ディレクトリ`7e427cc0-091c-11e9-9e45-72b7c59d52d7.000001`の場合、 `7e427cc0-091c-11e9-9e45-72b7c59d52d7`はアップストリーム データベース UUID、 `000001`はローカル`subdir`シリアル番号です。

-   `server-uuid.index` : 現在利用可能な`subdir`ディレクトリのリストを記録します。

-   `relay.meta` : 移行されたbinlogの情報を各`subdir`に保存します。例えば、

    ```bash
    cat c0149e17-dff1-11e8-b6a8-0242ac110004.000001/relay.meta
    ```

        binlog-name = "mysql-bin.000010"                            # The name of the currently migrated binlog.
        binlog-pos = 63083620                                       # The position of the currently migrated binlog.
        binlog-gtid = "c0149e17-dff1-11e8-b6a8-0242ac110004:1-3328" # GTID of the currently migrated binlog.

    複数の GTID が存在する場合もあります。

    ```bash
    cat 92acbd8a-c844-11e7-94a1-1866daf8accc.000001/relay.meta
    ```

        binlog-name = "mysql-bin.018393"
        binlog-pos = 277987307
        binlog-gtid = "3ccc475b-2343-11e7-be21-6c0b84d59f30:1-14,406a3f61-690d-11e7-87c5-6c92bf46f384:1-94321383,53bfca22-690d-11e7-8a62-18ded7a37b78:1-495,686e1ab6-c47e-11e7-a42c-6c92bf46f384:1-34981190,03fc0263-28c7-11e7-a653-6c0b84d59f30:1-7041423,05474d3c-28c7-11e7-8352-203db246dd3d:1-170,10b039fc-c843-11e7-8f6a-1866daf8d810:1-308290454"

### DMがbinlogを受信する位置 {#the-position-where-dm-receives-the-binlog}

-   DM は、保存されたチェックポイント (デフォルトではダウンストリーム`dm_meta`スキーマ内) から各移行タスクが必要とする最も早い位置を取得します。この位置が次のいずれかの位置より後の場合、DM はこの位置から移動を開始します。

-   ローカルリレーログが有効な場合、つまりリレーログに有効な`server-uuid.index` 、 `subdir` 、および`relay.meta`ファイルが含まれている場合、DM ワーカーは`relay.meta`に記録された位置から移行を回復します。

-   有効なローカル リレー ログがないが、アップストリーム データ ソース構成ファイルで`relay-binlog-name`または`relay-binlog-gtid`が指定されている場合:

    -   非 GTID モードで`relay-binlog-name`を指定すると、DM-worker は指定されたbinlogファイルから移行を開始します。
    -   GTID モードで`relay-binlog-gtid`を指定すると、DM-worker は指定された GTID から移行を開始します。

-   有効なローカル リレー ログがなく、DM 構成ファイルで`relay-binlog-name`または`relay-binlog-gtid`が指定されていない場合:

    -   非 GTID モードでは、DM ワーカーは、各サブタスクが移行している最も古いbinlogから、最新のbinlogが移行されるまで移行を開始します。

    -   GTID モードでは、DM ワーカーは、最新の GTID が移行されるまで、各サブタスクが移行する最も古い GTID から移行を開始します。

    > **注記：**
    >
    > 上流のリレー ログがパージされると、エラーが発生します。この場合、移行の開始位置を指定するには[`relay-binlog-gtid`](/dm/dm-source-configuration-file.md#global-configuration)を設定する必要があります。
