---
title: binlogctl
summary: Learns how to use `binlogctl`.
---

# binlogctl {#binlogctl}

[Binlog制御](https://github.com/pingcap/tidb-binlog/tree/master/binlogctl) (略して`binlogctl` ) は TiDB Binlogのコマンド ライン ツールです。 `binlogctl`使用して、TiDB Binlogクラスターを管理できます。

`binlogctl`の目的で使用できます。

-   PumpやDrainerの状態を確認
-   PumpまたはDrainerを一時停止または閉じる
-   PumpやDrainerの異常状態への対応

以下は、その使用シナリオです。

-   データ複製中にエラーが発生したか、 PumpまたはDrainerの実行状態を確認する必要があります。
-   クラスターを維持するときは、 PumpまたはDrainerを一時停止または閉じる必要があります。
-   PumpまたはDrainerプロセスが異常終了し、ノードの状態が更新されていないか、予期しない状態です。これは、データ複製タスクに影響します。

## <code>binlogctl</code>のダウンロード {#download-code-binlogctl-code}

`binlogctl`はTiDB Toolkitに含まれています。 TiDB Toolkitをダウンロードするには、 [TiDB ツールをダウンロード](/download-ecosystem-tools.md)を参照してください。

## 説明 {#descriptions}

コマンド ライン パラメータ:

```
Usage of binlogctl:
  -V    prints version and exit
  -cmd string
        operator: "generate_meta", "pumps", "drainers", "update-pump", "update-drainer", "pause-pump", "pause-drainer", "offline-pump", "offline-drainer", "encrypt" (default "pumps")
  -data-dir string
        meta directory path (default "binlog_position")
  -node-id string
        id of node, used to update some nodes with operations update-pump, update-drainer, pause-pump, pause-drainer, offline-pump and offline-drainer
  -pd-urls string
        a comma separated list of PD endpoints (default "http://127.0.0.1:2379")
  -show-offline-nodes
        include offline nodes when querying pumps/drainers
  -ssl-ca string
        Path of file that contains list of trusted SSL CAs for connection with cluster components.
  -ssl-cert string
        Path of file that contains X509 certificate in PEM format for connection with cluster components.
  -ssl-key string
        Path of file that contains X509 key in PEM format for connection with cluster components.
  -state string
        set node's state, can be set to online, pausing, paused, closing or offline.
  -text string
        text to be encrypted when using encrypt command
  -time-zone Asia/Shanghai
        set time zone if you want to save time info in savepoint file; for example, Asia/Shanghai for CST time, `Local` for local time
```

コマンド例:

-   すべてのPumpノードまたはDrainerノードの状態を確認します。

    `cmd` ～ `pumps`または`drainers`を設定します。例えば：

    {{< copyable "" >}}

    ```bash
    bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd pumps
    ```

    ```
    [2019/04/28 09:29:59.016 +00:00] [INFO] [nodes.go:48] ["query node"] [type=pump] [node="{NodeID: 1.1.1.1:8250, Addr: pump:8250, State: online, MaxCommitTS: 408012403141509121, UpdateTime: 2019-04-28 09:29:57 +0000 UTC}"]
    ```

    {{< copyable "" >}}

    ```bash
    bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd drainers
    ```

    ```
    [2019/04/28 09:29:59.016 +00:00] [INFO] [nodes.go:48] ["query node"] [type=drainer] [node="{NodeID: 1.1.1.1:8249, Addr: 1.1.1.1:8249, State: online, MaxCommitTS: 408012403141509121, UpdateTime: 2019-04-28 09:29:57 +0000 UTC}"]
    ```

-   PumpまたはDrainer を一時停止または閉じます。

    次のコマンドを使用して、サービスを一時停止または終了できます。

    | 指図         | 説明           | 例                                                                                              |
    | :--------- | :----------- | :--------------------------------------------------------------------------------------------- |
    | 一時停止ポンプ    | Pumpの一時停止    | `bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd pause-pump -node-id ip-127-0-0-1:8250`      |
    | 一時停止ドレーナー  | Drainerを一時停止 | `bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd pause-drainer -node-id ip-127-0-0-1:8249`   |
    | オフラインポンプ   | Pumpを閉じる     | `bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd offline-pump -node-id ip-127-0-0-1:8250`    |
    | オフライン ドレイン | Drainerを閉じる  | `bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd offline-drainer -node-id ip-127-0-0-1:8249` |

    `binlogctl` HTTP 要求をPumpまたはDrainerノードに送信します。リクエストを受信した後、ノードはそれに応じて既存の手順を実行します。

-   異常な状態のPumpまたはDrainerノードの状態を変更します。

    PumpまたはDrainerノードが正常に実行されている場合、または通常のプロセスで一時停止または閉じられている場合は、正常な状態です。異常な状態では、 PumpまたはDrainerノードはその状態を正しく維持できません。これは、データ複製タスクに影響します。この場合、 `binlogctl`を使用して状態情報を修復します。

    PumpノードまたはDrainerノードの状態を更新するには、 `cmd`を`update-pump`または`update-drainer`に設定します。状態は`paused`または`offline`です。例えば：

    {{< copyable "" >}}

    ```bash
    bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd update-pump -node-id ip-127-0-0-1:8250 -state paused
    ```

    > **ノート：**
    >
    > PumpまたはDrainerノードが正常に実行されると、その状態が定期的に PD に更新されます。上記のコマンドは、PD に保存されているPumpまたはDrainerの状態を直接変更します。そのため、 PumpまたはDrainerノードが正常に動作している場合は、このコマンドを使用しないでください。詳細については、 [TiDB Binlog FAQ](/tidb-binlog/tidb-binlog-faq.md)を参照してください。
