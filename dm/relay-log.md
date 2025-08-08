---
title: Data Migration Relay Log
summary: DM リレー ログのディレクトリ構造、初期移行ルール、およびデータ パージについて学習します。
---

# データ移行リレーログ {#data-migration-relay-log}

データ移行 (DM) リレー ログは、データベースの変更を記述するイベントを含む番号付きファイルの複数のセットと、使用されたすべてのリレー ログ ファイルの名前を含むインデックス ファイルで構成されます。

リレーログを有効にすると、DM-workerはアップストリームのbinlogをローカル設定ディレクトリに自動的に移行します（DMがTiUPを使用してデプロイされている場合、デフォルトの移行ディレクトリは`<deploy_dir>/<relay_log>`です）。デフォルト値は`<relay_log>`で、 `relay-dir`に設定されていますが、 [上流データベースコンフィグレーションファイル](/dm/dm-source-configuration-file.md)で変更できます。v5.4.0以降では、 [DMワーカー構成ファイル](/dm/dm-worker-configuration-file.md)の`relay-dir`でローカル設定ディレクトリを設定できます。これは、アップストリームデータベースの設定ファイルよりも優先されます。

## ユーザーシナリオ {#user-scenarios}

MySQLではstorage容量が限られているため、最大保存期間に達するとbinlogは自動的に消去されます。上流データベースがbinlogを消去すると、DMは消去されたbinlogを取得できず、移行タスクは失敗します。移行タスクごとに、DMは上流データベースに接続を作成し、binlogを取得します。接続数が多すぎると、上流データベースの負荷が増大する可能性があります。

リレーログを有効にすると、同じ上流データベースを持つ複数の移行タスクで、ローカルディスクにプルされたリレーログを再利用できます。これにより**、上流データベースへの負荷が軽減されます**。

完全データ移行タスクと増分データ移行タスク（ `task-mode=all` ）では、DMはまず完全データを移行し、その後、binlogに基づいて増分移行を実行する必要があります。完全移行フェーズに時間がかかると、上流のbinlogが消去され、増分移行が失敗する可能性があります。このような状況を回避するには、リレーログ機能を有効にすることで、DMがローカルディスクに十分なログを自動的に保持し、**増分移行タスクが正常に実行されるようにします**。

通常はリレー ログを有効にすることをお勧めしますが、次の潜在的な問題に注意してください。

リレーログはディスクに書き込む必要があるため、外部IOおよびCPUリソースを消費します。これにより、データレプリケーションプロセス全体が長くなり、データレプリケーションのレイテンシーが増加します。**レイテンシが重要な**シナリオでは、リレーログを有効にすることは推奨されません。

> **注記：**
>
> DM v2.0.7以降のバージョンでは、リレーログの書き込みが最適化されており、レイテンシーとCPUリソースの消費量は比較的低くなっています。

## リレーログを使用する {#use-relay-log}

このセクションでは、リレー ログを有効化および無効化する方法、リレー ログの状態を照会する方法、リレー ログを消去する方法について説明します。

### リレーログの有効化と無効化 {#enable-and-disable-relay-log}

<SimpleTab>

<div label="v5.4.0 and later versions">

v5.4.0以降のバージョンでは、 `enable-relay`を`true`に設定することでリレーログを有効にできます。v5.4.0以降では、上流データソースをバインドする際に、DM-workerはデータソースの設定で`enable-relay`をチェックします。 `enable-relay`が`true`場合、このデータソースに対してリレーログ機能が有効になります。

詳しい設定方法については[上流データベースコンフィグレーションファイル](/dm/dm-source-configuration-file.md)参照してください。

さらに、 `start-relay`または`stop-relay`コマンドを使用してデータ ソースの`enable-relay`構成を動的に調整し、リレー ログイン時間を有効または無効にすることもできます。

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
> DM v2.0.2 以降の DM v2.0.x および v5.3.0 では、ソース設定ファイル内の設定項目`enable-relay`無効になっており、リレーログの有効化と無効化には`start-relay`と`stop-relay`のみを使用できます。DM は、 [データソース構成の読み込み](/dm/dm-manage-source.md#operate-data-source)ときに`enable-relay` `true`に設定されていることを検出した場合、以下のメッセージを出力します。
>
>     Please use `start-relay` to specify which workers should pull relay log of relay-enabled sources.

> **警告：**
>
> この起動方法はバージョン6.1で非推奨とされており、将来のリリースで削除される可能性があります。関連コマンドの出力には、次のプロンプトが表示されます: `start-relay/stop-relay with worker name will be deprecated soon. You can try stopping relay first and use start-relay without worker name instead` 。

コマンド`start-relay`では、指定されたデータソースのリレーログを移行する 1 つ以上の DM ワーカーを設定できます。ただし、パラメータで指定する DM ワーカーは、空いているか、上流のデータソースにバインドされている必要があります。例を以下に示します。

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

DM バージョン 2.0.2 より前のバージョン（v2.0.2 は含まない）では、DM ワーカーを上流データソースにバインドする際に、ソース設定ファイルの設定項目`enable-relay`チェックされます。3 `enable-relay` `true`に設定されている場合、DM はデータソースのリレーログ機能を有効にします。

設定項目`enable-relay`設定方法については[上流データベースコンフィグレーションファイル](/dm/dm-source-configuration-file.md)参照してください。

</div>
</SimpleTab>

### リレーログのステータスを照会する {#query-relay-log-status}

コマンド`query-status -s`を使用してリレー ログのステータスを照会できます。

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

コマンド`pause-relay`リレーログのプル処理を一時停止し、コマンド`resume-relay`で再開できます。これらの2つのコマンドを実行する際は、上流データソースの`source-id`指定する必要があります。以下の例をご覧ください。

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

### リレーログを消去する {#purge-relay-logs}

DM では、リレーログをパージする方法として、手動パージと自動パージの 2 つの方法を提供しています。どちらの方法でも、アクティブなリレーログはパージされません。

> **注記：**
>
> -   アクティブリレーログ：リレーログはデータ移行タスクによって使用されています。アクティブリレーログは現在、Syncerユニット内でのみ更新および書き込みされます。「すべて」モードのデータ移行タスクが、データソースのパージで設定された有効期限よりも長い時間、フルエクスポート/インポートを実行した場合でも、リレーログはパージされます。
>
> -   期限切れのリレー ログ: リレー ログ ファイルの最終変更時刻と現在の時刻の差が、構成ファイルの`expires`フィールドの値よりも大きくなっています。

#### 自動パージ {#automatic-purge}

自動パージを有効にし、その戦略をソース設定ファイルで設定できます。次の例をご覧ください。

```yaml
# relay log purge strategy
purge:
    interval: 3600
    expires: 24
    remain-space: 15
```

-   `purge.interval`
    -   バックグラウンドでの自動パージの間隔（秒単位）。
    -   デフォルトでは「3600」であり、バックグラウンド パージ タスクが 3600 秒ごとに実行されることを示します。

-   `purge.expires`
    -   リレー ログ (以前にリレー処理ユニットに書き込まれ、現在実行中のデータ移行タスクによって使用されていないか、後で読み取られないログ) を自動バックグラウンド パージで消去されるまで保持できる時間数。
    -   デフォルトは「0」で、リレーログの更新時間に応じてデータのパージが実行されないことを示します。

-   `purge.remain-space`
    -   指定されたDMワーカーマシンが、自動バックグラウンドパージで安全にパージできるリレーログをパージしようとするディスク残量（GB単位）です`0`に設定すると、ディスク残量に応じたデータパージは実行されません。
    -   デフォルトでは「15」で、使用可能なディスク容量が 15 GB 未満になると、DM マスターはリレー ログを安全に消去しようとします。

#### 手動パージ {#manual-purge}

手動パージとは、dmctl が提供する`purge-relay`コマンドを使用して`subdir`とbinlog名を指定し、指定したbinlog**より前の**すべてのリレーログをパージすることを意味します。コマンドに`-subdir`オプションが指定されていない場合は、現在のリレーログサブディレクトリ**より前の**すべてのリレーログがパージされます。

現在のリレーログのディレクトリ構造が次のようになっていると仮定します。

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

-   dmctl で次の`purge-relay`コマンドを実行すると、 `e4e0e8ab-09cc-11e9-9220-82cc35207219.000002/mysql-bin.000001`**より前の**すべてのリレーログファイル（つまり`deb76a2b-09cc-11e9-9129-5242cf3bb246.000001`のすべてのリレーログファイル）が削除されます。 `e4e0e8ab-09cc-11e9-9220-82cc35207219.000002`と`deb76a2b-09cc-11e9-9129-5242cf3bb246.000003`のファイルは保持されます。

    ```bash
    purge-relay -s mysql-replica-01 --filename mysql-bin.000001 --sub-dir e4e0e8ab-09cc-11e9-9220-82cc35207219.000002
    ```

-   dmctlで次の`purge-relay`コマンドを実行すると、**現在の**（ `deb76a2b-09cc-11e9-9129-5242cf3bb246.000003` ）ディレクトリの`mysql-bin.000001`より前のすべてのリレーログファイル（ `deb76a2b-09cc-11e9-9129-5242cf3bb246.000001`と`e4e0e8ab-09cc-11e9-9220-82cc35207219.000002`にあるすべてのリレーログファイル）が削除されます。13 `deb76a2b-09cc-11e9-9129-5242cf3bb246.000003`ファイルは保持されます。

    ```bash
    purge-relay -s mysql-replica-01 --filename mysql-bin.000001
    ```

## リレーログの内部機構 {#internal-mechanism-of-relay-log}

このセクションでは、リレーログの内部の仕組みを紹介します。

### ディレクトリ構造 {#directory-structure}

リレーログのローカルstorageのディレクトリ構造の例:

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

    -   DM-workerは、上流データベースから移行されたbinlogを同じディレクトリに保存します。各ディレクトリは`subdir`です。

    -   `subdir`は`<Upstream database UUID>.<Local subdir serial number>`形式で名前が付けられます。

    -   アップストリームでプライマリ インスタンスとセカンダリ インスタンスが切り替わると、DM-worker は増分シリアル番号を持つ新しい`subdir`ディレクトリを生成します。

    -   上記の例では、ディレクトリ`7e427cc0-091c-11e9-9e45-72b7c59d52d7.000001`場合、 `7e427cc0-091c-11e9-9e45-72b7c59d52d7`アップストリーム データベース UUID であり、 `000001`ローカル`subdir`シリアル番号です。

-   `server-uuid.index` : 現在利用可能な`subdir`ディレクトリのリストを記録します。

-   `relay.meta` : 移行されたbinlogの情報を`subdir`に格納します。例えば、

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

-   DMは、保存されたチェックポイント（デフォルトでは下流`dm_meta`スキーマ）から、各移行タスクに必要な最も古い位置を取得します。この位置が後続の位置よりも後の場合、DMはこの位置から移行を開始します。

-   ローカルリレーログが有効な場合、つまりリレーログに有効な`server-uuid.index` 、 `subdir` 、 `relay.meta`ファイルが含まれている場合、DM-worker は`relay.meta`に記録された位置から移行を回復します。

-   有効なローカルリレーログが存在しないが、アップストリームデータソース構成ファイルで`relay-binlog-name`または`relay-binlog-gtid`指定されている場合:

    -   非 GTID モードでは、 `relay-binlog-name`指定すると、DM ワーカーは指定されたbinlogファイルから移行を開始します。
    -   GTID モードでは、 `relay-binlog-gtid`指定すると、DM ワーカーは指定された GTID から移行を開始します。

-   有効なローカルリレーログがなく、DM 構成ファイルに`relay-binlog-name`または`relay-binlog-gtid`指定されていない場合:

    -   非 GTID モードでは、DM ワーカーは、各サブタスクが移行している最も古いbinlogから移行を開始し、最新のbinlogが移行されるまで続けます。

    -   GTID モードでは、DM ワーカーは、各サブタスクが移行している最も古い GTID から移行を開始し、最新の GTID が移行されるまで続けます。

    > **注記：**
    >
    > 上流のリレーログがパージされている場合はエラーが発生します。この場合、移行の開始位置を指定するために[`relay-binlog-gtid`](/dm/dm-source-configuration-file.md#global-configuration)設定する必要があります。
