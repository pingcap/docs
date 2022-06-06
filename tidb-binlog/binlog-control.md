---
title: binlogctl
summary: Learns how to use `binlogctl`.
---

# binlogctl {#binlogctl}

[ビンログ制御](https://github.com/pingcap/tidb-binlog/tree/master/binlogctl) （略して`binlogctl` ）は、TiDBBinlogのコマンドラインツールです。 `binlogctl`を使用して、TiDBBinlogクラスターを管理できます。

`binlogctl`を使用して次のことができます。

-   ポンプまたはドレイナーの状態を確認してください
-   ポンプまたはドレイナーを一時停止または閉じます
-   ポンプまたはドレイナーの異常状態に対処する

その使用シナリオは次のとおりです。

-   データ複製中にエラーが発生したか、ポンプまたはドレイナーの実行状態を確認する必要があります。
-   クラスタを保守するときは、ポンプまたはドレイナーを一時停止または閉じる必要があります。
-   ノードの状態が更新されていないか、予期しないときに、ポンプまたはドレイナープロセスが異常終了します。これは、データ複製タスクに影響します。

## <code>binlogctl</code>ダウンロードする {#download-code-binlogctl-code}

> **ノート：**
>
> 使用する制御ツールのバージョンは、クラスタのバージョンと一致していることをお勧めします。

{{< copyable "" >}}

```bash
wget https://download.pingcap.org/tidb-{version}-linux-amd64.tar.gz &&
wget https://download.pingcap.org/tidb-{version}-linux-amd64.sha256
```

ファイルの整合性を確認するには、次のコマンドを実行します。結果に問題がなければ、ファイルは正しいです。

{{< copyable "" >}}

```bash
sha256sum -c tidb-{version}-linux-amd64.sha256
```

ファイルの整合性を確認するには、次のコマンドを実行します。結果に問題がなければ、ファイルは正しいです。

{{< copyable "" >}}

```bash
sha256sum -c tidb-enterprise-tools-latest-linux-amd64.sha256
```

## 説明 {#descriptions}

コマンドラインパラメータ：

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

コマンドの例：

-   すべてのポンプノードまたはドレイナーノードの状態を確認します。

    `cmd`を`pumps`または`drainers`に設定します。例えば：

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

-   ポンプまたはドレイナーを一時停止または閉じます。

    次のコマンドを使用して、サービスを一時停止または閉じることができます。

    | 指示         | 説明          | 例                                                                                              |
    | :--------- | :---------- | :--------------------------------------------------------------------------------------------- |
    | 一時停止-ポンプ   | ポンプを一時停止します | `bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd pause-pump -node-id ip-127-0-0-1:8250`      |
    | 一時停止-水切り   | ドレイナーを一時停止  | `bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd pause-drainer -node-id ip-127-0-0-1:8249`   |
    | オフラインポンプ   | ポンプを閉じる     | `bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd offline-pump -node-id ip-127-0-0-1:8250`    |
    | オフラインドレイナー | ドレイナーを閉じる   | `bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd offline-drainer -node-id ip-127-0-0-1:8249` |

    `binlogctl`は、HTTPリクエストをPumpまたはDrainerノードに送信します。要求を受信した後、ノードはそれに応じて終了手順を実行します。

-   異常な状態のポンプまたはドレイナーノードの状態を変更します。

    ポンプノードまたはドレイナーノードが正常に動作している場合、または通常のプロセスで一時停止または閉じている場合、通常の状態になります。異常な状態では、PumpまたはDrainerノードはその状態を正しく維持できません。これは、データ複製タスクに影響します。この場合、 `binlogctl`を使用して状態情報を修復します。

    PumpまたはDrainerノードの状態を更新するには、 `cmd`を`update-pump`または`update-drainer`に設定します。状態は`paused`または`offline`にすることができます。例えば：

    {{< copyable "" >}}

    ```bash
    bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd update-pump -node-id ip-127-0-0-1:8250 -state paused
    ```

    > **ノート：**
    >
    > PumpまたはDrainerノードが正常に実行されると、その状態は定期的にPDに更新されます。上記のコマンドは、PDに保存されているポンプまたはドレイナーの状態を直接変更します。したがって、PumpまたはDrainerノードが正常に動作しているときは、このコマンドを使用しないでください。詳細については、 [TiDB Binlog FAQ](/tidb-binlog/tidb-binlog-faq.md)を参照してください。
