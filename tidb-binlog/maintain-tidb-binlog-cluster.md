---
title: TiDB Binlog Cluster Operations
summary: Learn how to operate the cluster version of TiDB Binlog.
---

# TiDB Binlogクラスタの操作 {#tidb-binlog-cluster-operations}

このドキュメントでは、次の TiDB Binlogクラスター操作について説明します。

-   PumpとDrainerノードの状態
-   PumpまたはDrainerプロセスの開始または終了
-   binlogctl ツールを使用するか、TiDB で SQL 操作を直接実行して、TiDB Binlogクラスターを管理する

## PumpまたはDrainerの状態 {#pump-or-drainer-state}

PumpまたはDrainerの状態の説明:

-   `online` : 通常稼働
-   `pausing` : 一時停止中
-   `paused` : 停止中
-   `closing` : オフライン プロセス中
-   `offline` : オフラインです

> **ノート：**
>
> PumpまたはDrainerノードの状態情報は、サービス自体によって維持され、配置Driver(PD) に定期的に更新されます。

## PumpまたはDrainerプロセスの開始と終了 {#starting-and-exiting-a-pump-or-drainer-process}

### Pump {#pump}

-   開始中: 開始すると、 PumpノードはすべてのDrainerノードに`online`状態で通知します。通知が成功した場合、 Pumpノードはその状態を`online`に設定します。それ以外の場合、 Pumpノードはエラーを報告し、状態を`paused`に設定してプロセスを終了します。
-   終了: Pumpノードは、プロセスが正常に終了する前に`paused`または`offline`状態に入ります。プロセスが異常終了した場合 ( `kill -9`コマンド、プロセスpanic、クラッシュが原因)、ノードはまだ`online`状態です。
    -   一時停止: `kill`コマンド ( `kill -9`ではなく) を使用するか、 <kbd>Ctrl</kbd> + <kbd>C</kbd>を押すか、binlogctl ツールで`pause-pump`コマンドを使用して、 Pumpプロセスを一時停止できます。一時停止命令を受け取った後、 Pumpノードはその状態を`pausing`に設定し、 binlog書き込み要求の受信を停止し、 binlogデータのDrainerノードへの提供を停止します。すべてのスレッドが安全に終了した後、 Pumpノードはその状態を`paused`に更新し、プロセスを終了します。
    -   オフライン:Pumpプロセスを閉じるには、binlogctl ツールで`offline-pump`コマンドを使用する必要があります。オフライン命令を受信した後、 Pumpノードはその状態を`closing`に設定し、 binlog書き込み要求の受信を停止します。 Pumpノードは、すべてのbinlogデータがDrainerノードによって消費されるまで、 binlog をDrainerノードに提供し続けます。次に、 Pumpノードは状態を`offline`に設定し、プロセスを終了します。

### Drainer {#drainer}

-   開始: 開始すると、 Drainerノードはその状態を`online`に設定し、 `offline`状態にないすべてのPumpノードから binlog をプルしようとします。 binlog の取得に失敗した場合は、試行を続けます。
-   終了: Drainerノードは、プロセスが正常に終了する前に`paused`または`offline`状態に入ります。プロセスが異常終了した場合 ( `kill -9` 、プロセスpanic、クラッシュが原因)、 Drainerノードはまだ`online`状態です。
    -   一時停止: `kill`コマンド ( `kill -9`ではありません) を使用するか、 <kbd>Ctrl</kbd> + <kbd>C</kbd>を押すか、binlogctl ツールで`pause-drainer`コマンドを使用して、 Drainerプロセスを一時停止できます。一時停止命令を受け取った後、 Drainerノードはその状態を`pausing`に設定し、 Pumpノードからのバイナリログのプルを停止します。すべてのスレッドが安全に終了した後、 Drainerノードはその状態を`paused`に設定し、プロセスを終了します。
    -   オフライン: Drainerプロセスを閉じるには、binlogctl ツールで`offline-drainer`コマンドを使用する必要があります。オフライン命令を受け取った後、 Drainerノードはその状態を`closing`に設定し、 Pumpノードからのバイナリログのプルを停止します。すべてのスレッドが安全に終了した後、 Drainerノードはその状態を`offline`に更新し、プロセスを終了します。

Drainerの状態を一時停止、終了、確認、および変更する方法については、 [binlogctl ガイド](/tidb-binlog/binlog-control.md)を参照してください。

## <code>binlogctl</code>使用してPump/ Drainerを管理します {#use-code-binlogctl-code-to-manage-pump-drainer}

[`binlogctl`](https://github.com/pingcap/tidb-binlog/tree/master/binlogctl)は、次の機能を備えた TiDB Binlogの操作ツールです。

-   PumpやDrainerの状態を確認する
-   PumpまたはDrainerの一時停止または終了
-   PumpやDrainerの異常時の対応

`binlogctl`の詳しい使い方は[binlogctl の概要](/tidb-binlog/binlog-control.md)を参照。

## SQL ステートメントを使用してPumpまたはDrainerを管理する {#use-sql-statements-to-manage-pump-or-drainer}

binlog関連の状態を表示または変更するには、TiDB で対応する SQL ステートメントを実行します。

-   binlog が有効になっているかどうかを確認します。

    {{< copyable "" >}}

    ```sql
    show variables like "log_bin";
    ```

    ```
    +---------------+-------+
    | Variable_name | Value |
    +---------------+-------+
    | log_bin       |  0   |
    +---------------+-------+
    ```

    値が`0`の場合、 binlogが有効になります。値が`1`の場合、 binlog は無効になります。

-   すべてのPumpノードまたはDrainerノードのステータスを確認します。

    {{< copyable "" >}}

    ```sql
    show pump status;
    ```

    ```
    +--------|----------------|--------|--------------------|---------------------|
    | NodeID |     Address    | State  |   Max_Commit_Ts    |    Update_Time      |
    +--------|----------------|--------|--------------------|---------------------|
    | pump1  | 127.0.0.1:8250 | Online | 408553768673342237 | 2019-05-01 00:00:01 |
    +--------|----------------|--------|--------------------|---------------------|
    | pump2  | 127.0.0.2:8250 | Online | 408553768673342335 | 2019-05-01 00:00:02 |
    +--------|----------------|--------|--------------------|---------------------|
    ```

    {{< copyable "" >}}

    ```sql
    show drainer status;
    ```

    ```
    +----------|----------------|--------|--------------------|---------------------|
    |  NodeID  |     Address    | State  |   Max_Commit_Ts    |    Update_Time      |
    +----------|----------------|--------|--------------------|---------------------|
    | drainer1 | 127.0.0.3:8249 | Online | 408553768673342532 | 2019-05-01 00:00:03 |
    +----------|----------------|--------|--------------------|---------------------|
    | drainer2 | 127.0.0.4:8249 | Online | 408553768673345531 | 2019-05-01 00:00:04 |
    +----------|----------------|--------|--------------------|---------------------|
    ```

-   異常な状況でPumpまたはDrainerノードの状態を変更する

    {{< copyable "" >}}

    ```sql
    change pump to node_state ='paused' for node_id 'pump1';
    ```

    ```
    Query OK, 0 rows affected (0.01 sec)
    ```

    {{< copyable "" >}}

    ```sql
    change drainer to node_state ='paused' for node_id 'drainer1';
    ```

    ```
    Query OK, 0 rows affected (0.01 sec)
    ```

    上記の SQL ステートメントを実行すると、binlogctl の`update-pump`または`update-drainer`コマンドと同じように機能します。上記の SQL ステートメントは、 PumpまたはDrainerノードが異常な状態にある場合に**のみ**使用してください。

> **ノート：**
>
> -   TiDB v2.1.7 以降のバージョンでbinlog が有効になっていて、 PumpまたはDrainerの実行ステータスがサポートされているかどうかを確認します。
> -   PumpまたはDrainerのステータスの変更は、TiDB v3.0.0-rc.1 以降のバージョンでサポートされています。この機能は、PD に保存されているPumpまたはDrainerノードのステータスの変更のみをサポートします。ノードを一時停止または閉じるには、 `binlogctl`ツールを使用します。
