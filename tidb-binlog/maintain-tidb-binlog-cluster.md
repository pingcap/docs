---
title: TiDB Binlog Cluster Operations
summary: TiDB Binlogのクラスター バージョンの操作方法を学習します。
---

# TiDBBinlogクラスタ操作 {#tidb-binlog-cluster-operations}

このドキュメントでは、次の TiDB Binlogクラスター操作について説明します。

-   PumpとDrainerノードの状態
-   PumpまたはDrainerプロセスの開始または終了
-   binlogctl ツールを使用するか、TiDB で直接 SQL 操作を実行して、TiDB Binlogクラスターを管理する

## PumpまたはDrainerの状態 {#pump-or-drainer-state}

PumpまたはDrainerの状態の説明:

-   `online` : 正常に動作中
-   `pausing` : 一時停止中
-   `paused` : 停止されました
-   `closing` : オフラインプロセス中
-   `offline` : オフラインです

> **注記：**
>
> PumpまたはDrainerノードの状態情報はサービス自体によって維持され、配置Driver(PD) に定期的に更新されます。

## PumpまたはDrainerプロセスの開始と終了 {#starting-and-exiting-a-pump-or-drainer-process}

### Pump {#pump}

-   開始: 開始されると、PumpノードはすべてのDrainerノードに`online`状態で通知します。通知が成功すると、Pumpノードは状態を`online`に設定します。それ以外の場合、Pumpノードはエラーを報告し、状態を`paused`に設定してプロセスを終了します。
-   終了中: プロセスが正常に終了する前に、 Pumpノードは`paused`または`offline`状態になります。プロセスが異常終了した場合 ( `kill -9`コマンド、プロセスpanic、クラッシュが原因)、ノードは`online`状態のままになります。
    -   一時停止: Pumpプロセスを一時停止するには、 `kill`コマンド ( `kill -9`ではありません) を使用するか、 <kbd>Ctrl</kbd> + <kbd>C</kbd>を押すか、binlogctl ツールで`pause-pump`コマンドを使用します。一時停止命令を受信すると、 Pumpノードは状態を`pausing`に設定し、 binlog書き込み要求の受信を停止し、 Drainerノードへのbinlogデータの提供を停止します。すべてのスレッドが安全に終了すると、 Pumpノードは状態を`paused`に更新し、プロセスを終了します。
    -   オフライン: Pumpプロセスを閉じるには、binlogctl ツールの`offline-pump`コマンドのみを使用します。オフライン命令を受信すると、 Pumpノードは状態を`closing`に設定し、 binlog書き込み要求の受信を停止します。Pump ノードは、すべてのbinlogデータがDrainerノードによって消費されるまで、 Drainerノードにbinlogを提供し続けます。その後、 Pumpノードは状態を`offline`に設定し、プロセスを終了します。

### Drainer {#drainer}

-   開始: 開始されると、 Drainerノードは状態を`online`に設定し、状態`offline`ではないすべてのPumpノードから binlog を取得しようとします。binlog を取得できない場合は、試行を続けます。
-   終了: プロセスが正常に終了する前に、 Drainerノードは`paused`または`offline`状態になります。プロセスが異常終了した場合 ( `kill -9` 、プロセスpanic、クラッシュが原因)、 Drainerノードは`online`状態のままになります。
    -   一時停止: `kill`コマンド ( `kill -9`ではありません) を使用するか、 <kbd>Ctrl</kbd> + <kbd>C</kbd>を押すか、binlogctl ツールで`pause-drainer`コマンドを使用することで、 Drainerプロセスを一時停止できます。一時停止命令を受信すると、 Drainerノードは状態を`pausing`に設定し、 Pumpノードからの binlog のプルを停止します。すべてのスレッドが安全に終了すると、 Drainerノードは状態を`paused`に設定し、プロセスを終了します。
    -   オフライン: Drainerプロセスを閉じるには、binlogctl ツールの`offline-drainer`コマンドを使用する必要があります。オフライン命令を受信すると、 Drainerノードは状態を`closing`に設定し、 Pumpノードからの binlog の取得を停止します。すべてのスレッドが安全に終了すると、 Drainerノードは状態を`offline`に更新し、プロセスを終了します。

Drainerを一時停止、終了、確認、状態の変更を行う方法については、 [binlogctl ガイド](/tidb-binlog/binlog-control.md)参照してください。

## <code>binlogctl</code>を使用してPump/Drainerを管理する {#use-code-binlogctl-code-to-manage-pump-drainer}

[`binlogctl`](https://github.com/pingcap/tidb-binlog/tree/release-8.1/binlogctl) 、以下の機能を備えた TiDB Binlogの操作ツールです。

-   PumpまたはDrainerの状態を確認する
-   PumpまたはDrainerを一時停止または閉じる
-   PumpやDrainerの異常時の対応

`binlogctl`の詳しい使い方については[binlogctl の概要](/tidb-binlog/binlog-control.md)を参照してください。

## SQL文を使用してPumpまたはDrainerを管理する {#use-sql-statements-to-manage-pump-or-drainer}

binlog関連の状態を表示または変更するには、TiDB で対応する SQL ステートメントを実行します。

-   binlogが有効になっているかどうかを確認します。

    ```sql
    show variables like "log_bin";
    ```

        +---------------+-------+
        | Variable_name | Value |
        +---------------+-------+
        | log_bin       |  0   |
        +---------------+-------+

    値が`0`場合、 binlogは有効になります。値が`1`場合、 binlogは無効になります。

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

    上記の SQL 文を実行すると、binlogctl の`update-pump`または`update-drainer`のコマンドと同じように動作します。上記の SQL 文は、 PumpまたはDrainerノードが異常な状態にある場合に**のみ**使用してください。

> **注記：**
>
> -   TiDB v2.1.7 以降のバージョンでは、 binlogが有効になっているかどうか、およびPumpまたはDrainerの実行ステータスを確認することがサポートされています。
> -   PumpまたはDrainerのステータスの変更は、TiDB v3.0.0-rc.1 以降のバージョンでサポートされています。この機能は、PD に保存されているPumpまたはDrainerノードのステータスの変更のみをサポートします。ノードを一時停止または閉じるには、 `binlogctl`ツールを使用します。
