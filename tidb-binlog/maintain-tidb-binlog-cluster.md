---
title: TiDB Binlog Cluster Operations
summary: Learn how to operate the cluster version of TiDB Binlog.
---

# Binlogクラスターの操作 {#tidb-binlog-cluster-operations}

このドキュメントでは、次のBinlogクラスタ操作を紹介します。

-   PumpとDrainerノードの状態
-   PumpまたはDrainerプロセスの開始または終了
-   binlogctlツールを使用するか、TiDBでSQL操作を直接実行することによるBinlogクラスタの管理

## PumpまたはDrainerの状態 {#pump-or-drainer-state}

PumpまたはDrainerの状態の説明：

-   `online` ：正常に動作しています
-   `pausing` ：一時停止中
-   `paused` ：停止しました
-   `closing` ：オフラインプロセス中
-   `offline` ：オフラインになっています

> **ノート：**
>
> PumpノードまたはDrainerノードの状態情報は、サービス自体によって維持され、配置Driver（PD）に定期的に更新されます。

## PumpまたはDrainerプロセスの開始と終了 {#starting-and-exiting-a-pump-or-drainer-process}

### Pump {#pump}

-   開始：開始すると、Pumpノードは`online`状態のすべてのDrainerノードに通知します。通知が成功すると、 Pumpノードはその状態を`online`に設定します。それ以外の場合、 Pumpノードはエラーを報告し、その状態を`paused`に設定して、プロセスを終了します。
-   終了：プロセスが正常に終了する前に、Pumpノードは`paused`または`offline`の状態になります。プロセスが異常終了した場合（ `kill -9`コマンド、プロセスpanic、クラッシュが原因）、ノードは`online`状態のままです。
    -   一時停止： `kill`コマンド（ `kill -9`ではなく）を使用するか、 <kbd>Ctrl</kbd> + <kbd>C</kbd>を押すか、binlogctlツールの`pause-pump`コマンドを使用して、 Pumpプロセスを一時停止できます。一時停止命令を受信した後、 Pumpノードはその状態を`pausing`に設定し、binlog書き込み要求の受信を停止し、 Drainerノードへのbinlogデータの提供を停止します。すべてのスレッドが安全に終了した後、 Pumpノードはその状態を`paused`に更新し、プロセスを終了します。
    -   オフライン：binlogctlツールの`offline-pump`コマンドを使用することによってのみ、 Pumpプロセスを閉じることができます。オフライン命令を受信した後、 Pumpノードはその状態を`closing`に設定し、binlog書き込み要求の受信を停止します。 Pumpノードは、すべてのbinlogデータがDrainerノードによって消費されるまで、 Drainerノードにbinlogを提供し続けます。次に、 Pumpノードはその状態を`offline`に設定し、プロセスを終了します。

### Drainer {#drainer}

-   開始：開始すると、 Drainerノードはその状態を`online`に設定し、 `offline`状態ではないすべてのPumpノードからbinlogをプルしようとします。 binlogの取得に失敗した場合は、試行を続けます。
-   終了：プロセスが正常に終了する前に、 Drainerノードは`paused`または`offline`の状態になります。プロセスが異常終了した場合（ `kill -9` 、プロセスpanic、クラッシュが原因）、 Drainerノードは`online`状態のままです。
    -   一時停止： `kill`コマンド（ `kill -9`ではなく）を使用するか、 <kbd>Ctrl</kbd> + <kbd>C</kbd>を押すか、binlogctlツールの`pause-drainer`コマンドを使用して、 Drainerプロセスを一時停止できます。一時停止命令を受け取った後、 Drainerノードはその状態を`pausing`に設定し、 Pumpノードからのbinlogのプルを停止します。すべてのスレッドが安全に終了した後、 Drainerノードはその状態を`paused`に設定し、プロセスを終了します。
    -   オフライン：binlogctlツールの`offline-drainer`コマンドを使用することによってのみ、 Drainerプロセスを閉じることができます。オフライン命令を受け取った後、 Drainerノードはその状態を`closing`に設定し、 Pumpノードからのbinlogのプルを停止します。すべてのスレッドが安全に終了した後、 Drainerノードはその状態を`offline`に更新し、プロセスを終了します。

Drainerの状態を一時停止、閉じる、確認、および変更する方法については、 [binlogctlガイド](/tidb-binlog/binlog-control.md)を参照してください。

## Drainerを使用してPump/ <code>binlogctl</code>を管理します {#use-code-binlogctl-code-to-manage-pump-drainer}

[`binlogctl`](https://github.com/pingcap/tidb-binlog/tree/master/binlogctl)は、次の機能を備えたBinlogの操作ツールです。

-   PumpまたはDrainerの状態を確認する
-   PumpまたはDrainerの一時停止または閉鎖
-   PumpまたはDrainerの異常状態への対応

`binlogctl`の詳細な使用法については、 [binlogctlの概要](/tidb-binlog/binlog-control.md)を参照してください。

## SQLステートメントを使用してPumpまたはDrainerを管理する {#use-sql-statements-to-manage-pump-or-drainer}

binlog関連の状態を表示または変更するには、TiDBで対応するSQLステートメントを実行します。

-   binlogが有効になっているかどうかを確認します。

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

    値が`0`の場合、binlogが有効になります。値が`1`の場合、binlogは無効になります。

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

-   異常な状況でPumpまたはDrainerノードの状態を変更します

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

    上記のSQLステートメントの実行は、binlogctlの`update-pump`または`update-drainer`コマンドと同じように機能します。上記のSQLステートメントは、 PumpノードまたはDrainerノードが異常な状況にある場合に**のみ**使用してください。

> **ノート：**
>
> -   binlogが有効になっているかどうか、およびPumpまたはDrainerの実行ステータスがTiDBv2.1.7以降のバージョンでサポートされているかどうかを確認します。
> -   PumpまたはDrainerのステータスの変更は、TiDBv3.0.0-rc.1以降のバージョンでサポートされています。この機能は、PDに保存されているPumpノードまたはDrainerノードのステータスの変更のみをサポートします。ノードを一時停止または閉じるには、 `binlogctl`ツールを使用します。
