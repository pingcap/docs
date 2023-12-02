---
title: binlogctl
summary: Learns how to use `binlogctl`.
---

# binlogctl {#binlogctl}

[Binlog制御](https://github.com/pingcap/tidb-binlog/tree/release-7.5/binlogctl) (略して`binlogctl` ) は、TiDB Binlogのコマンド ライン ツールです。 `binlogctl`を使用して TiDB Binlogクラスターを管理できます。

`binlogctl`を使用すると、次のことができます。

-   PumpやDrainerの状態を確認してください
-   PumpまたはDrainerを一時停止または閉じる
-   PumpやDrainerの異常時の対処

その使用シナリオは次のとおりです。

-   データのレプリケーション中にエラーが発生したか、 PumpまたはDrainerの実行状態を確認する必要があります。
-   クラスターを保守するときは、 PumpまたはDrainerを一時停止または閉じる必要があります。
-   ノードの状態が更新されていないか、予期しない状態であるにもかかわらず、PumpまたはDrainerのプロセスが異常終了します。これはデータ複製タスクに影響します。

## <code>binlogctl</code>をダウンロードする {#download-code-binlogctl-code}

`binlogctl`はTiDB Toolkitに含まれています。 TiDB Toolkitをダウンロードするには、 [TiDB ツールをダウンロード](/download-ecosystem-tools.md)を参照してください。

## 説明 {#descriptions}

コマンドラインパラメータ:

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

コマンドの例:

-   すべてのPumpまたはDrainerノードの状態を確認します。

    `cmd` ～ `pumps`または`drainers`を設定します。例えば：

    ```bash
    bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd pumps
    ```

        [2019/04/28 09:29:59.016 +00:00] [INFO] [nodes.go:48] ["query node"] [type=pump] [node="{NodeID: 1.1.1.1:8250, Addr: pump:8250, State: online, MaxCommitTS: 408012403141509121, UpdateTime: 2019-04-28 09:29:57 +0000 UTC}"]

    ```bash
    bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd drainers
    ```

        [2019/04/28 09:29:59.016 +00:00] [INFO] [nodes.go:48] ["query node"] [type=drainer] [node="{NodeID: 1.1.1.1:8249, Addr: 1.1.1.1:8249, State: online, MaxCommitTS: 408012403141509121, UpdateTime: 2019-04-28 09:29:57 +0000 UTC}"]

-   PumpまたはDrainerを一時停止または閉じます。

    次のコマンドを使用して、サービスを一時停止または終了できます。

    | 指示         | 説明          | 例                                                                                              |
    | :--------- | :---------- | :--------------------------------------------------------------------------------------------- |
    | 一時停止ポンプ    | Pumpを一時停止する | `bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd pause-pump -node-id ip-127-0-0-1:8250`      |
    | ポーズドレイナー   | 一時停止Drainer | `bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd pause-drainer -node-id ip-127-0-0-1:8249`   |
    | オフラインポンプ   | Pumpを閉じる    | `bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd offline-pump -node-id ip-127-0-0-1:8250`    |
    | オフラインドレイナー | Drainerを閉じる | `bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd offline-drainer -node-id ip-127-0-0-1:8249` |

    `binlogctl` HTTP リクエストをPumpまたはDrainerノードに送信します。リクエストを受信した後、ノードはそれに応じて終了手順を実行します。

-   異常な状態のPumpまたはDrainerノードの状態を変更します。

    PumpまたはDrainerノードが正常に実行されている場合、または通常のプロセスで一時停止または閉じられている場合、ノードは通常の状態になります。異常な状態では、PumpまたはDrainerノードはその状態を正しく維持できません。これはデータ複製タスクに影響します。この場合、 `binlogctl`を使用して状態情報を修復します。

    PumpノードまたはDrainerノードの状態を更新するには、 `cmd`を`update-pump`または`update-drainer`に設定します。状態は`paused`または`offline`です。例えば：

    ```bash
    bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd update-pump -node-id ip-127-0-0-1:8250 -state paused
    ```

    > **注記：**
    >
    > PumpまたはDrainerノードが正常に実行されている場合、その状態は定期的に PD に更新されます。上記のコマンドは、PD に保存されているPumpまたはDrainerの状態を直接変更します。したがって、 PumpまたはDrainerノードが正常に動作しているときは、このコマンドを使用しないでください。詳細については、 [TiDBBinlogFAQ](/tidb-binlog/tidb-binlog-faq.md)を参照してください。
