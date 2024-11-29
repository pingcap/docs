---
title: Data Migration Relay Log
summary: DM リレー ログのディレクトリ構造、初期移行ルール、データ消去について学習します。
---

# データ移行リレーログ {#data-migration-relay-log}

データ移行 (DM) リレー ログは、データベースの変更を記述するイベントを含む番号付きファイルの複数のセットと、使用されたすべてのリレー ログ ファイルの名前を含むインデックス ファイルで構成されます。

リレー ログを有効にすると、DM-worker はアップストリームbinlog をローカル構成ディレクトリに自動的に移行します (DM がTiUP を使用してデプロイされている場合、デフォルトの移行ディレクトリは`<deploy_dir>/<relay_log>`です)。 `<relay_log>`のデフォルト値は`relay-dir`で、 [アップストリームデータベースコンフィグレーションファイル](/dm/dm-source-configuration-file.md)で変更できます。 v5.4.0 以降では、 [DMワーカー設定ファイル](/dm/dm-worker-configuration-file.md)の`relay-dir`を通じてローカル構成ディレクトリを構成できます。これは、アップストリーム データベースの構成ファイルよりも優先されます。

## ユーザーシナリオ {#user-scenarios}

MySQL では、storageスペースが限られているため、最大保持時間に達すると、 binlog は自動的に消去されます。アップストリーム データベースがbinlog を消去すると、DM は消去されたbinlog をプルできず、移行タスクは失敗します。移行タスクごとに、DM はアップストリームに接続を作成し、 binlog をプルします。接続が多すぎると、アップストリーム データベースのワークロードが重くなる可能性があります。

リレー ログを有効にすると、同じアップストリーム データベースを持つ複数の移行タスクで、ローカル ディスクにプルされたリレー ログを再利用できます。これにより、**アップストリーム データベースへの負荷が軽減されます**。

完全および増分データ移行タスク ( `task-mode=all` ) の場合、DM は最初に完全なデータを移行し、次にbinlogに基づいて増分移行を実行する必要があります。完全移行フェーズに時間がかかる場合、上流のbinlog が消去され、増分移行が失敗する可能性があります。この状況を回避するには、リレーログ機能を有効にして、DM がローカルディスクに十分なログを自動的に保持し、**増分移行タスクが正常に実行されるようにします**。

通常はリレー ログを有効にすることをお勧めしますが、次の潜在的な問題に注意してください。

リレー ログはディスクに書き込む必要があるため、外部 IO および CPU リソースが消費されます。これにより、データ レプリケーション プロセス全体が長くなり、データ レプリケーションのレイテンシーが増加します。**レイテンシの影響を受けやすい**シナリオでは、リレー ログを有効にすることはお勧めしません。

> **注記：**
>
> DM v2.0.7 以降のバージョンでは、リレー ログの書き込みが最適化されています。レイテンシーと CPU リソースの消費は比較的低くなっています。

## リレーログを使用する {#use-relay-log}

このセクションでは、リレー ログを有効化および無効化する方法、リレー ログの状態を照会する方法、リレー ログを消去する方法について説明します。

### リレーログを有効または無効にする {#enable-and-disable-relay-log}

<SimpleTab>

<div label="v5.4.0 and later versions">

v5.4.0 以降のバージョンでは、 `enable-relay` `true`に設定することでリレー ログを有効にできます。v5.4.0 以降では、上流データ ソースをバインドするときに、DM-worker はデータ ソースの構成で`enable-relay`項目をチェックします。 `enable-relay`が`true`の場合、このデータ ソースに対してリレー ログ機能が有効になります。

詳しい設定方法については[アップストリームデータベースコンフィグレーションファイル](/dm/dm-source-configuration-file.md)参照してください。

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
> DM v2.0.2 以降の DM v2.0.x および v5.3.0 では、ソース構成ファイルの構成項目`enable-relay`無効になり、リレー ログを有効または無効にするには`start-relay`と`stop-relay`を使用できます。DM は、 [データソース構成の読み込み](/dm/dm-manage-source.md#operate-data-source)ときに`enable-relay`が`true`に設定されていることを検出した場合、次のメッセージを出力します。
>
>     Please use `start-relay` to specify which workers should pull relay log of relay-enabled sources.

> **警告：**
>
> この起動方法は、バージョン 6.1 では非推奨とされており、将来のリリースでは削除される可能性があります。関連するコマンドの出力には、次のプロンプトが表示されます: `start-relay/stop-relay with worker name will be deprecated soon. You can try stopping relay first and use start-relay without worker name instead` 。

コマンド`start-relay`では、指定されたデータ ソースのリレー ログを移行するために 1 つ以上の DM ワーカーを構成できますが、パラメータで指定された DM ワーカーは空いているか、アップストリーム データ ソースにバインドされている必要があります。次に例を示します。

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

v2.0.2 より前の DM バージョン (v2.0.2 は含まない) では、DM ワーカーをアップストリーム データ ソースにバインドするときに、DM はソース構成ファイルの構成項目`enable-relay`チェックします。3 が`enable-relay`に設定されている場合、DM `true`データ ソースのリレー ログ機能を有効にします。

設定項目`enable-relay`設定方法については[アップストリームデータベースコンフィグレーションファイル](/dm/dm-source-configuration-file.md)参照してください。

</div>
</SimpleTab>

### リレーログのステータスを照会する {#query-relay-log-status}

コマンド`query-status -s`使用して、リレー ログのステータスを照会できます。

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

コマンド`pause-relay`を使用してリレー ログのプル プロセスを一時停止し、コマンド`resume-relay`を使用してプロセスを再開できます。これらの 2 つのコマンドを実行するときは、アップストリーム データ ソースの`source-id`指定する必要があります。次の例を参照してください。

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

DM では、リレー ログを消去する方法として、手動消去と自動消去の 2 つの方法を提供しています。どちらの方法でも、アクティブなリレー ログは消去されません。

> **注記：**
>
> -   アクティブ リレー ログ: リレー ログはデータ移行タスクによって使用されています。アクティブ リレー ログは現在、Syncer ユニットでのみ更新および書き込みが行われます。All モードのデータ移行タスクが、データ ソースの消去で設定された有効期限よりも長い時間をフル エクスポート/インポートに費やした場合、リレー ログは消去されます。
>
> -   期限切れのリレー ログ: リレー ログ ファイルの最終変更時刻と現在の時刻の差が、構成ファイルの`expires`フィールドの値よりも大きくなっています。

#### 自動パージ {#automatic-purge}

自動パージを有効にし、その戦略をソース構成ファイルで構成できます。次の例を参照してください。

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
    -   リレー ログ (リレー処理ユニットに以前に書き込まれ、現在実行中のデータ移行タスクによって使用されていないか、後で読み取られないログ) を自動バックグラウンド パージで消去されるまで保持できる時間数。
    -   デフォルトでは「0」で、リレーログの更新時間に応じてデータの消去が実行されないことを示します。

-   `purge.remain-space`
    -   指定された DM ワーカー マシンが、自動バックグラウンド パージで安全にパージできるリレー ログをパージしようとする、残りのディスク領域の量 (GB 単位)。 `0`に設定すると、残りのディスク領域に応じてデータ パージは実行されません。
    -   デフォルトでは「15」であり、使用可能なディスク容量が 15 GB 未満になると、DM マスターはリレー ログを安全に消去しようとします。

#### 手動パージ {#manual-purge}

手動パージとは、dmctl が提供する`purge-relay`コマンドを使用して`subdir`とbinlog名を指定し、指定されたbinlog**より前の**すべてのリレー ログをパージすることを意味します。コマンドで`-subdir`オプションが指定されていない場合は、現在のリレー ログ サブディレクトリ**より前の**すべてのリレー ログがパージされます。

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

-   dmctl で次の`purge-relay`コマンドを実行すると、 `e4e0e8ab-09cc-11e9-9220-82cc35207219.000002/mysql-bin.000001`**より前の**すべてのリレー ログ ファイル ( `deb76a2b-09cc-11e9-9129-5242cf3bb246.000001`のすべてのリレー ログ ファイル) が削除されます。 `e4e0e8ab-09cc-11e9-9220-82cc35207219.000002`と`deb76a2b-09cc-11e9-9129-5242cf3bb246.000003`のファイルは保持されます。

    ```bash
    purge-relay -s mysql-replica-01 --filename mysql-bin.000001 --sub-dir e4e0e8ab-09cc-11e9-9220-82cc35207219.000002
    ```

-   dmctl で次の`purge-relay`コマンドを実行すると、**現在**の ( `deb76a2b-09cc-11e9-9129-5242cf3bb246.000003` ) ディレクトリの`mysql-bin.000001`より前のすべての`deb76a2b-09cc-11e9-9129-5242cf3bb246.000003`ログ ファイル ( `deb76a2b-09cc-11e9-9129-5242cf3bb246.000001`と`e4e0e8ab-09cc-11e9-9220-82cc35207219.000002`のすべてのリレー ログ ファイル) が削除されます。13 のファイルは保持されます。

    ```bash
    purge-relay -s mysql-replica-01 --filename mysql-bin.000001
    ```

## リレーログの内部機構 {#internal-mechanism-of-relay-log}

このセクションでは、リレーログの内部の仕組みを紹介します。

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

    -   DM-worker は、アップストリーム データベースから移行されたbinlog を同じディレクトリに保存します。各ディレクトリは`subdir`です。

    -   `subdir` `<Upstream database UUID>.<Local subdir serial number>`の形式で名前が付けられます。

    -   アップストリームでプライマリ インスタンスとセカンダリ インスタンスが切り替わると、DM-worker は増分シリアル番号を持つ新しい`subdir`ディレクトリを生成します。

    -   上記の例では、ディレクトリ`7e427cc0-091c-11e9-9e45-72b7c59d52d7.000001`の場合、 `7e427cc0-091c-11e9-9e45-72b7c59d52d7`アップストリーム データベース UUID であり、 `000001`ローカル`subdir`シリアル番号です。

-   `server-uuid.index` : 現在利用可能な`subdir`ディレクトリのリストを記録します。

-   `relay.meta` : 移行されたbinlogの情報を各`subdir`に格納します。たとえば、

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

-   DM は、保存されたチェックポイント (デフォルトではダウンストリーム`dm_meta`スキーマ) から各移行タスクに必要な最も早い位置を取得します。この位置が後続の位置よりも後の場合、DM はこの位置から移行を開始します。

-   ローカルリレーログが有効である場合、つまりリレーログに有効な`server-uuid.index` 、 `subdir` 、および`relay.meta`ファイルが含まれている場合、DM-worker は`relay.meta`に記録された位置から移行を回復します。

-   有効なローカルリレーログが存在しないが、アップストリームデータソース構成ファイルで`relay-binlog-name`または`relay-binlog-gtid`指定されている場合:

    -   非 GTID モードでは、 `relay-binlog-name`を指定すると、DM ワーカーは指定されたbinlogファイルから移行を開始します。
    -   GTID モードでは、 `relay-binlog-gtid`が指定されると、DM ワーカーは指定された GTID から移行を開始します。

-   有効なローカル リレー ログがなく、DM 構成ファイルに`relay-binlog-name`または`relay-binlog-gtid`指定されていない場合:

    -   非 GTID モードでは、DM ワーカーは、各サブタスクが移行している最も古いbinlogから移行を開始し、最新のbinlogが移行されるまで移行を続けます。

    -   GTID モードでは、DM ワーカーは、各サブタスクが移行している最も古い GTID から移行を開始し、最新の GTID が移行されるまで移行を続けます。

    > **注記：**
    >
    > アップストリームリレーログがパージされるとエラーが発生します。この場合、移行の開始位置を指定するために[`relay-binlog-gtid`](/dm/dm-source-configuration-file.md#global-configuration)を設定する必要があります。
