---
title: TiDB Binlog Cluster Operations
summary: Learn how to operate the cluster version of TiDB Binlog.
---

# TiDBBinlogクラスタの操作 {#tidb-binlog-cluster-operations}

このドキュメントでは、次の TiDB Binlogクラスター操作を紹介します。

-   PumpとDrainerノードの状態
-   PumpまたはDrainerプロセスの開始または終了
-   binlogctl ツールを使用するか、TiDB で SQL 操作を直接実行することによる、TiDB Binlogクラスターの管理

## PumpまたはDrainerの状態 {#pump-or-drainer-state}

PumpまたはDrainerの状態の説明:

-   `online` : 正常に動作しています
-   `pausing` : 一時停止中
-   `paused` : 停止中
-   `closing` : オフラインプロセス中
-   `offline` : オフラインになっています

> **注記：**
>
> PumpノードまたはDrainerノードの状態情報はサービス自体によって維持され、定期的に配置Driver(PD) に更新されます。

## PumpまたはDrainerプロセスの開始と終了 {#starting-and-exiting-a-pump-or-drainer-process}

### Pump {#pump}

-   開始中: 開始すると、 PumpノードはすべてのDrainerノードに`online`状態を通知します。通知が成功すると、 Pumpノードはその状態を`online`に設定します。それ以外の場合、 Pumpノードはエラーを報告し、状態を`paused`に設定してプロセスを終了します。
-   終了中: プロセスが正常に終了する前に、Pumpノードは`paused`または`offline`状態に入ります。プロセスが異常終了した場合 (コマンド`kill -9` 、プロセスpanic、クラッシュが原因)、ノードは依然として`online`状態にあります。
    -   一時停止: `kill`コマンド ( `kill -9`ではない) を使用するか、 <kbd>Ctrl</kbd> + <kbd>C</kbd>を押すか、binlogctl ツールで`pause-pump`コマンドを使用することで、Pumpプロセスを一時停止できます。一時停止命令を受信した後、Pumpノードはその状態を`pausing`に設定し、binlog書き込み要求の受信を停止し、Drainerノードへのbinlogデータの提供を停止します。すべてのスレッドが安全に終了すると、 Pumpノードは状態を`paused`に更新し、プロセスを終了します。
    -   オフライン: Pumpプロセスを閉じるには、binlogctl ツールの`offline-pump`コマンドを使用する必要があります。オフライン命令を受信した後、Pumpノードは状態を`closing`に設定し、binlog書き込み要求の受信を停止します。 Pumpノードは、すべてのbinlogデータがDrainerノードによって消費されるまで、 Drainerノードにbinlogを提供し続けます。次に、 Pumpノードは状態を`offline`に設定し、プロセスを終了します。

### Drainer {#drainer}

-   開始: 開始されると、 Drainerノードはその状態を`online`に設定し、状態`offline`にないすべてのPumpノードからバイナリログを取得しようとします。バイナリログの取得に失敗した場合は、試行を続けます。
-   終了: プロセスが正常に終了する前に、 Drainerノードは`paused`または`offline`状態に入ります。プロセスが異常終了した場合 ( `kill -9` 、プロセスpanic、クラッシュが原因)、 Drainerノードは依然として`online`状態のままです。
    -   一時停止: Drainerプロセスを一時停止するには、 `kill`コマンド ( `kill -9`ではありません) を使用するか、 <kbd>Ctrl</kbd> + <kbd>C</kbd>を押すか、binlogctl ツールで`pause-drainer`コマンドを使用します。一時停止命令を受信した後、 Drainerノードはその状態を`pausing`に設定し、 Pumpノードからのバイナリログの取得を停止します。すべてのスレッドが安全に終了すると、 Drainerノードは状態を`paused`に設定し、プロセスを終了します。
    -   オフライン: Drainerプロセスを閉じるには、binlogctl ツールの`offline-drainer`コマンドを使用する必要があります。オフライン命令を受信した後、 Drainerノードは状態を`closing`に設定し、 Pumpノードからのバイナリログの取得を停止します。すべてのスレッドが安全に終了すると、 Drainerノードは状態を`offline`に更新し、プロセスを終了します。

Drainerの一時停止、終了、状態の確認、および変更の方法については、 [binlogctl ガイド](/tidb-binlog/binlog-control.md)を参照してください。

## <code>binlogctl</code>使用してPump/Drainerを管理する {#use-code-binlogctl-code-to-manage-pump-drainer}

[`binlogctl`](https://github.com/pingcap/tidb-binlog/tree/release-7.5/binlogctl)は、次の機能を備えた TiDB Binlogの操作ツールです。

-   PumpやDrainerの状態を確認する
-   PumpまたはDrainerを一時停止または閉じる
-   PumpやDrainerの異常時の対処

`binlogctl`の詳しい使い方は[binlogctl の概要](/tidb-binlog/binlog-control.md)を参照してください。

## SQL ステートメントを使用してPumpまたはDrainerを管理する {#use-sql-statements-to-manage-pump-or-drainer}

binlog関連の状態を表示または変更するには、TiDB で対応する SQL ステートメントを実行します。

-   binlog が有効になっているかどうかを確認します。

    ```sql
    show variables like "log_bin";
    ```

        +---------------+-------+
        | Variable_name | Value |
        +---------------+-------+
        | log_bin       |  0   |
        +---------------+-------+

    値が`0`の場合、 binlogが有効になります。値が`1`の場合、 binlog は無効になります。

-   すべてのPumpまたはDrainerノードのステータスを確認します。

    ```sql
    show pump status;
    ```

        +--------|----------------|--------|--------------------|---------------------|
        | NodeID |     Address    | State  |   Max_Commit_Ts    |    Update_Time      |
        +--------|----------------|--------|--------------------|---------------------|
        | pump1  | 127.0.0.1:8250 | Online | 408553768673342237 | 2019-05-01 00:00:01 |
        +--------|----------------|--------|--------------------|---------------------|
        | pump2  | 127.0.0.2:8250 | Online | 408553768673342335 | 2019-05-01 00:00:02 |
        +--------|----------------|--------|--------------------|---------------------|

    ```sql
    show drainer status;
    ```

        +----------|----------------|--------|--------------------|---------------------|
        |  NodeID  |     Address    | State  |   Max_Commit_Ts    |    Update_Time      |
        +----------|----------------|--------|--------------------|---------------------|
        | drainer1 | 127.0.0.3:8249 | Online | 408553768673342532 | 2019-05-01 00:00:03 |
        +----------|----------------|--------|--------------------|---------------------|
        | drainer2 | 127.0.0.4:8249 | Online | 408553768673345531 | 2019-05-01 00:00:04 |
        +----------|----------------|--------|--------------------|---------------------|

-   異常な状況でPumpまたはDrainerノードの状態を変更する

    ```sql
    change pump to node_state ='paused' for node_id 'pump1';
    ```

        Query OK, 0 rows affected (0.01 sec)

    ```sql
    change drainer to node_state ='paused' for node_id 'drainer1';
    ```

        Query OK, 0 rows affected (0.01 sec)

    上記の SQL ステートメントの実行は、binlogctl の`update-pump`または`update-drainer`コマンドと同じように機能します。上記の SQL ステートメントは、PumpまたはDrainerノードが異常な状況にある場合**にのみ**使用してください。

> **注記：**
>
> -   binlog が有効になっているかどうか、およびPumpまたはDrainerの実行ステータスを確認することは、TiDB v2.1.7 以降のバージョンでサポートされています。
> -   PumpまたはDrainerのステータスの変更は、TiDB v3.0.0-rc.1 以降のバージョンでサポートされています。この機能は、PD に保存されているPumpまたはDrainerノードのステータスの変更のみをサポートしています。ノードを一時停止または閉じるには、 `binlogctl`ツールを使用します。
