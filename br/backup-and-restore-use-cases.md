---
title: BR Use Cases
summary: Learn the use cases of backing up and restoring data using BR.
---

# BRのユースケース {#br-use-cases}

[バックアップと復元（BR）](/br/backup-and-restore-overview.md)は、TiDBクラスタデータの分散バックアップと復元のためのツールです。

このドキュメントでは、一般的なバックアップと復元のシナリオについて説明します。

-   [単一のテーブルをネットワークディスクにバックアップします（実稼働環境に推奨）](#back-up-a-single-table-to-a-network-disk-recommended-for-production-environments)
-   [ネットワークディスクからデータを復元する（実稼働環境に推奨）](#restore-data-from-a-network-disk-recommended-for-production-environments)
-   [1つのテーブルをローカルディスクにバックアップします](#back-up-a-single-table-to-a-local-disk-recommended-for-testing-environments)
-   [ローカルディスクからデータを復元する](#restore-data-from-a-local-disk-recommended-for-testing-environments)

このドキュメントは、次の目標の達成を支援することを目的としています。

-   ネットワークディスクまたはローカルディスクを使用してデータを正しくバックアップおよび復元します。
-   メトリックの監視を通じて、バックアップまたは復元操作のステータスを取得します。
-   バックアップまたは復元操作中にパフォーマンスを調整する方法を学びます。
-   バックアップ操作中に発生する可能性のある異常のトラブルシューティングを行います。

## 観客 {#audience}

TiDBと[TiKV](https://tikv.org/)の基本的な知識が必要です。

読み進める前に、 [BRの概要](/br/backup-and-restore-overview.md) 、特に[使用制限](/br/backup-and-restore-overview.md#usage-restrictions)と[いくつかのヒント](/br/backup-and-restore-overview.md#some-tips)を読んだことを確認してください。

## 前提条件 {#prerequisites}

このセクションでは、TiDBをデプロイするための推奨される方法、クラスタのバージョン、TiKVクラスタのハードウェア情報、およびユースケースのデモンストレーション用のクラスタ構成を紹介します。

独自のハードウェアと構成に基づいて、バックアップまたは復元操作のパフォーマンスを見積もることができます。ネットワークディスクを使用してデータをバックアップおよび復元することをお勧めします。これにより、バックアップファイルの収集が不要になり、特にTiKVクラスタが大規模な場合にバックアップ効率が大幅に向上します。

### 展開方法 {#deployment-method}

[TiUP](/tiup/tiup-cluster.md)を使用してTiDBクラスタをデプロイし、TiUPを使用してBRをインストールすることをお勧めします。

### クラスターバージョン {#cluster-versions}

-   TiDB：v6.1.0
-   TiKV：v6.1.0
-   PD：v6.1.0
-   BR：v6.1.0

> **ノート：**
>
> 最新バージョンの[TiDB / TiKV / PD / BR](/releases/release-notes.md)を使用し、BRバージョンがTiDBバージョンと**一致して**いることを確認することをお勧めします。

### TiKVハードウェア情報 {#tikv-hardware-information}

-   オペレーティングシステム：CentOS Linuxリリース7.6.1810（コア）
-   CPU：16コアの共通KVMプロセッサ
-   RAM：32 GB
-   ディスク：500 GB SSD * 2
-   NIC：10ギガビットネットワークカード

### クラスター構成 {#cluster-configuration}

BRはコマンドをTiKVクラスタに直接送信し、TiDBサーバーに依存しないため、BRを使用するときにTiDBサーバーを構成する必要はありません。

-   TiKV：デフォルト構成
-   PD：デフォルト構成

### その他 {#others}

上記の前提条件に加えて、バックアップと復元を実行する前に、次のチェックも実行する必要があります。

#### バックアップ前に確認してください {#check-before-backup}

[`br backup`コマンド](/br/use-br-command-line-tool.md#br-command-line-description)を実行する前に、次の条件が満たされていることを確認してください。

-   TiDBクラスタで実行されているDDLステートメントはありません。
-   ターゲットストレージデバイスに必要なスペースがあります（バックアップクラスタのディスクスペースの1/3以上）。

#### 復元前に確認してください {#check-before-restoration}

[`br restore`コマンド](/br/use-br-command-line-tool.md#br-command-line-description)を実行する前に、ターゲットクラスタをチェックして、このクラスタのテーブルに重複した名前がないことを確認してください。

## 単一のテーブルをネットワークディスクにバックアップします（実稼働環境に推奨） {#back-up-a-single-table-to-a-network-disk-recommended-for-production-environments}

`br backup`コマンドを実行して、単一のテーブルデータ`--db batchmark --table order_line`をネットワークディスクの指定されたパス`local:///br_data`にバックアップします。

### バックアップの前提条件 {#backup-prerequisites}

-   [バックアップ前に確認してください](#check-before-backup)
-   高性能SSDハードディスクホストをデータを格納するNFSサーバーとして構成し、すべてのBRノード、TiKVノード、およびTiFlashノードをNFSクライアントとして構成します。 NFSクライアントがサーバーにアクセスできるように、同じパス（たとえば、 `/br_data` ）をNFSサーバーにマウントします。
-   NFSサーバーとすべてのNFSクライアント間の合計転送速度は、少なくとも`the number of TiKV instances * 150MB/s`に達する必要があります。そうしないと、ネットワークI/Oがパフォーマンスのボトルネックになる可能性があります。

> **ノート：**
>
> -   データのバックアップ中は、リーダーレプリカのデータのみがバックアップされるため、クラスタにTiFlashレプリカが存在する場合でも、BRはTiFlashノードをマウントせずにバックアップを完了できます。
> -   データを復元する場合、BRはすべてのレプリカのデータを復元します。また、TiFlashノードは、復元を完了するためにBRのバックアップデータにアクセスする必要があります。したがって、復元する前に、TiFlashノードをNFSサーバーにマウントする必要があります。

### トポロジー {#topology}

次の図は、BRの類型を示しています。

![img](/media/br/backup-nfs-deploy.png)

### バックアップ操作 {#backup-operation}

`br backup`コマンドを実行します。

{{< copyable "" >}}

```shell
bin/br backup table \
    --db batchmark \
    --table order_line \
    -s local:///br_data \
    --pd ${PD_ADDR}:2379 \
    --log-file backup-nfs.log
```

### バックアップの監視メトリック {#monitoring-metrics-for-the-backup}

バックアッププロセス中は、監視パネルの次のメトリックに注意して、バックアッププロセスのステータスを取得してください。

**バックアップCPU使用率**：バックアップ操作で動作している各TiKVノードのCPU使用率（たとえば、backup-workerとbackup-endpoint）。

![img](/media/br/backup-cpu.png)

**IO使用率**：バックアップ操作で動作している各TiKVノードのI/O使用率。

![img](/media/br/backup-io.png)

**BackupSST生成スループット**：バックアップ操作で動作している各TiKVノードのbackupSST生成スループット。通常は約150MB/秒です。

![img](/media/br/backup-throughput.png)

**1つのバックアップ範囲期間**：範囲をバックアップする期間。これは、KVをスキャンし、その範囲をbackupSSTファイルとして保存するための合計時間コストです。

![img](/media/br/backup-range-duration.png)

**1つのバックアップサブタスク期間**：バックアップタスクが分割される各サブタスクの期間。

> **ノート：**
>
> -   このタスクでは、バックアップされる単一のテーブルに3つのインデックスがあり、タスクは通常4つのサブタスクに分割されます。
> -   次の画像のパネルには、10個の青と10個の黄色の20個のポイントがあり、10個のサブタスクがあることを示しています。リージョンのスケジューリングはバックアッププロセス中に発生する可能性があるため、数回の再試行が正常です。

![img](/media/br/backup-subtask-duration.png)

**バックアップエラー**：バックアッププロセス中に発生したエラー。通常の状況ではエラーは発生しません。いくつかのエラーが発生した場合でも、バックアップ操作には再試行メカニズムがあり、バックアップ時間が長くなる可能性がありますが、操作の正確性には影響しません。

![img](/media/br/backup-errors.png)

**チェックサム要求期間**：バックアップクラスタでの管理チェックサム要求の期間。

![img](/media/br/checksum-duration.png)

### バックアップ結果の説明 {#backup-results-explanation}

バックアップが完了すると、BRはバックアップの概要をコンソールに出力します。

バックアップコマンドを実行する前に指定されたログで、このログからバックアップ操作の統計情報を取得できます。このログで「概要」を検索すると、次の情報が表示されます。

```
["Full backup Success summary:
    total backup ranges: 2,
    total success: 2,
    total failed: 0,
    total take(Full backup time): 31.802912166s,
    total take(real time): 49.799662427s,
    total size(MB): 5997.49,
    avg speed(MB/s): 188.58,
    total kv: 120000000"]
    ["backup checksum"=17.907153678s]
    ["backup fast checksum"=349.333µs]
    ["backup total regions"=43]
    [BackupTS=422618409346269185]
    [Size=826765915]
```

上記のログには、次の情報が含まれています。

-   `total take(Full backup time)` ：バックアップ期間
-   `total take(real time)` ：アプリケーションの合計実行時間
-   `total size(MB)` ：バックアップデータのサイズ
-   `avg speed(MB/s)` ：バックアップスループット
-   `total kv` ：バックアップされたKVペアの数
-   `backup checksum` ：バックアップチェックサム期間
-   `backup fast checksum` ：各テーブルのチェックサム、KVペア、およびバイトを計算する合計時間
-   `backup total regions` ：バックアップリージョンの総数
-   `BackupTS` ：バックアップデータのスナップショットタイムスタンプ
-   `Size` ：圧縮後のディスク内のバックアップデータの実際のサイズ

上記の情報から、単一のTiKVインスタンスのスループットを計算できます： `avg speed(MB/s)` / `tikv_count` = `62.86` 。

### 性能調整 {#performance-tuning}

バックアッププロセス中にTiKVのリソース使用量が明らかなボトルネックにならない場合（たとえば、 [バックアップの監視メトリック](#monitoring-metrics-for-the-backup)では、バックアップワーカーの最大CPU使用率は約`1500%`であり、全体的なI / O使用率は`30%`未満です）、パフォーマンスを調整するために、 `--concurrency` （デフォルトでは`4` ）の値を増やすことを試みることができます。ただし、このパフォーマンス調整方法は、多くの小さなテーブルのユースケースには適していません。次の例を参照してください。

{{< copyable "" >}}

```shell
bin/br backup table \
    --db batchmark \
    --table order_line \
    -s local:///br_data/ \
    --pd ${PD_ADDR}:2379 \
    --log-file backup-nfs.log \
    --concurrency 16
```

![img](/media/br/backup-diff.png)

![img](/media/br/backup-diff2.png)

調整されたパフォーマンス結果は次のとおりです（同じデータサイズで）。

-   バックアップ期間（ `total take(s)` ）： `986.43`から`535.53`に短縮
-   バックアップスループット（ `avg speed(MB/s)` ）： `358.09`から`659.59`に増加
-   単一のTiKVインスタンスのスループット（ `avg speed(MB/s)/tikv_count` ）： `89`から`164.89`に増加

## ネットワークディスクからデータを復元する（実稼働環境に推奨） {#restore-data-from-a-network-disk-recommended-for-production-environments}

`br restore`コマンドを使用して、完全なバックアップデータをオフラインクラスタに復元します。現在、BRはオンラインクラスタへのデータの復元をサポートしていません。

### 復元の前提条件 {#restoration-prerequisites}

-   [復元する前に確認してください](#check-before-restoration)

### トポロジー {#topology}

次の図は、BRの類型を示しています。

![img](/media/br/restore-nfs-deploy.png)

### 復元操作 {#restoration-operation}

`br restore`コマンドを実行します。

{{< copyable "" >}}

```shell
bin/br restore table --db batchmark --table order_line -s local:///br_data --pd 172.16.5.198:2379 --log-file restore-nfs.log
```

### 復元の監視メトリック {#monitoring-metrics-for-the-restoration}

復元プロセス中は、監視パネルの次のメトリックに注意して、復元プロセスのステータスを取得してください。

**CPU** ：復元操作で動作している各TiKVノードのCPU使用率。

![img](/media/br/restore-cpu.png)

**IO使用率**：復元操作で動作している各TiKVノードのI/O使用率。

![img](/media/br/restore-io.png)

**地域**：地域の分布。リージョンが均等に分散されるほど、復元リソースがより適切に使用されます。

![img](/media/br/restore-region.png)

SSTの処理**時間**：SSTファイルの処理の遅延。テーブルを復元するときに、 `tableID`が変更された場合は、 `tableID`を書き直す必要があります。それ以外の場合、 `tableID`は名前が変更されます。一般的に、書き換えの遅延は名前変更の遅延よりも長くなります。

![img](/media/br/restore-process-sst.png)

**SSTスループット**のダウンロード：外部ストレージからSSTファイルをダウンロードするスループット。

![img](/media/br/restore-download-sst.png)

**復元エラー**：復元プロセス中に発生したエラー。

![img](/media/br/restore-errors.png)

**チェックサム要求期間**：管理チェックサム要求の期間。この復元の期間は、バックアップの期間よりも長くなります。

![img](/media/br/restore-checksum.png)

### 復元結果の説明 {#restoration-results-explanation}

復元コマンドを実行する前に指定されたログで、このログから復元操作の統計情報を取得できます。このログで「概要」を検索すると、次の情報が表示されます。

```
["Table Restore summary:
    total restore tables: 1,
    total success: 1,
    total failed: 0,
    total take(Full restore time): 17m1.001611365s,
    total take(real time): 16m1.371611365s,
    total kv: 5659888624,
    total size(MB): 353227.18,
    avg speed(MB/s): 367.42"]
    ["restore files"=9263]
    ["restore ranges"=6888]
    ["split region"=49.049182743s]
    ["restore checksum"=6m34.879439498s]
    [Size=48693068713]
```

上記のログには、次の情報が含まれています。

-   `total take(Full restore time)` ：復元期間
-   `total take(real time)` ：アプリケーションの合計実行時間
-   `total size(MB)` ：復元するデータのサイズ
-   `total kv` ：復元されたKVペアの数
-   `avg speed(MB/s)` ：復元スループット
-   `split region` ：リージョン分割期間
-   `restore checksum` ：復元チェックサム期間
-   `Size` ：ディスクに復元されたデータの実際のサイズ

上記の情報から、以下の項目を計算することができます。

-   単一のTiKVインスタンスのスループット`91.8` `avg speed(MB/s)` = `tikv_count`
-   単一のTiKVインスタンスの平均復元速度： `total size(MB)` /（ `split time` + `restore time` ）/ `tikv_count` = `87.4`

#### 性能調整 {#performance-tuning}

復元プロセス中にTiKVのリソース使用量が明らかなボトルネックにならない場合は、値を`--concurrency`に増やすことができます（デフォルトは`128` ）。次の例を参照してください。

{{< copyable "" >}}

```shell
bin/br restore table --db batchmark --table order_line -s local:///br_data/ --pd 172.16.5.198:2379 --log-file restore-concurrency.log --concurrency 1024
```

調整されたパフォーマンス結果は次のとおりです（同じデータサイズで）。

-   復元期間（ `total take(s)` ）： `961.37`から`443.49`に短縮
-   復元スループット（ `avg speed(MB/s)` ）： `367.42`から`796.47`に増加
-   単一の`199.1`インスタンスのスループット（ `avg speed(MB/s)` ）： `tikv_count`から`91.8`に増加
-   単一のTiKVインスタンスの平均復元速度（ `total size(MB)` /（ `split time` + `restore time` ）/ `tikv_count` ）： `87.4`から`162.3`に増加

## 単一のテーブルをローカルディスクにバックアップします（テスト環境に推奨） {#back-up-a-single-table-to-a-local-disk-recommended-for-testing-environments}

`br backup`コマンドを実行して、単一のテーブル`--db batchmark --table order_line`をローカルディスクの指定されたパス`local:///home/tidb/backup_local`にバックアップします。

### バックアップの前提条件 {#backup-prerequisites}

-   [バックアップ前に確認してください](#check-before-backup)
-   各TiKVノードには、backupSSTファイルを保存するための個別のディスクがあります。
-   `backup_endpoint`のノードには、 `backupmeta`のファイルを格納するための個別のディスクがあります。
-   TiKVと`backup_endpoint`ノードは、バックアップ用に同じディレクトリ（たとえば、 `/home/tidb/backup_local` ）を共有します。

### トポロジー {#topology}

次の図は、BRの類型を示しています。

![img](/media/br/backup-local-deploy.png)

### バックアップ操作 {#backup-operation}

`br backup`コマンドを実行します。

{{< copyable "" >}}

```shell
bin/br backup table \
    --db batchmark \
    --table order_line \
    -s local:///home/tidb/backup_local/ \
    --pd ${PD_ADDR}:2379 \
    --log-file backup_local.log
```

バックアッププロセス中は、監視パネルのメトリックに注意して、バックアッププロセスのステータスを取得してください。詳細については、 [バックアップの監視メトリック](#monitoring-metrics-for-the-backup)を参照してください。

#### バックアップ結果の説明 {#backup-results-explanation}

バックアップコマンドを実行する前に指定されたログで、このログから復元操作の統計情報を取得できます。このログで「概要」を検索すると、次の情報が表示されます。

```
["Table backup summary:
    total backup ranges: 4,
    total success: 4,
    total failed: 0,
    total take(s): 551.31,
    total kv: 5659888624,
    total size(MB): 353227.18,
    avg speed(MB/s): 640.71"]
    ["backup total regions"=6795]
    ["backup checksum"=6m33.962719217s]
    ["backup fast checksum"=22.995552ms]
```

上記のログには、次の情報が含まれています。

-   `total take(s)` ：バックアップ期間
-   `total size(MB)` ：データサイズ
-   `avg speed(MB/s)` ：バックアップスループット
-   `backup checksum` ：バックアップチェックサム期間

上記の情報から、単一のTiKVインスタンスのスループットを計算できます： `avg speed(MB/s)` / `tikv_count` = `160` 。

## ローカルディスクからデータを復元する（テスト環境に推奨） {#restore-data-from-a-local-disk-recommended-for-testing-environments}

`br restore`コマンドを実行して、完全なバックアップデータをオフラインクラスタに復元します。現在、BRはオンラインクラスタへのデータの復元をサポートしていません。

### 復元の前提条件 {#restoration-prerequisites}

-   [復元する前に確認してください](#check-before-restoration)
-   TiKVクラスタとバックアップデータに重複するデータベースまたはテーブルがありません。現在、BRはテーブルルートをサポートしていません。
-   各TiKVノードには、backupSSTファイルを保存するための個別のディスクがあります。
-   `restore_endpoint`のノードには、 `backupmeta`のファイルを格納するための個別のディスクがあります。
-   TiKVと`restore_endpoint`ノードは、復元のために同じディレクトリ（たとえば、 `/home/tidb/backup_local/` ）を共有します。

復元する前に、次の手順に従ってください。

1.  すべてのbackupSSTファイルを同じディレクトリに収集します。
2.  収集したbackupSSTファイルをクラスタのすべてのTiKVノードにコピーします。
3.  `backupmeta`のファイルを`restore endpoint`のノードにコピーします。

### トポロジー {#topology}

次の図は、BRの類型を示しています。

![img](/media/br/restore-local-deploy.png)

### 復元操作 {#restoration-operation}

`br restore`コマンドを実行します。

{{< copyable "" >}}

```shell
bin/br restore table --db batchmark --table order_line -s local:///home/tidb/backup_local/ --pd 172.16.5.198:2379 --log-file restore_local.log
```

復元プロセス中は、監視パネルのメトリックに注意して、復元プロセスのステータスを取得します。詳細については、 [復元の監視メトリック](#monitoring-metrics-for-the-restoration)を参照してください。

### 復元結果の説明 {#restoration-results-explanation}

復元コマンドを実行する前に指定されたログで、このログから復元操作の統計情報を取得できます。このログで「概要」を検索すると、次の情報が表示されます。

```
["Table Restore summary:
    total restore tables: 1,
    total success: 1,
    total failed: 0,
    total take(s): 908.42,
    total kv: 5659888624,
    total size(MB): 353227.18,
    avg speed(MB/s): 388.84"]
    ["restore files"=9263]
    ["restore ranges"=6888]
    ["split region"=58.7885518s]
    ["restore checksum"=6m19.349067937s]
```

上記のログには、次の情報が含まれています。

-   `total take(s)` ：復元期間
-   `total size(MB)` ：データサイズ
-   `avg speed(MB/s)` ：復元スループット
-   `split region` ：リージョン分割期間
-   `restore checksum` ：復元チェックサム期間

上記の情報から、以下の項目を計算することができます。

-   単一のTiKVインスタンスのスループット`97.2` `avg speed(MB/s)` = `tikv_count`
-   単一のTiKVインスタンスの平均復元速度： `total size(MB)` /（ `split time` + `restore time` ）/ `tikv_count` = `92.4`

## バックアップ中のエラー処理 {#error-handling-during-backup}

このセクションでは、バックアッププロセス中に発生する可能性のある一般的なエラーを紹介します。

### <code>key locked Error</code> {#code-key-locked-error-code-in-the-backup-log}

ログのエラーメッセージ： `log - ["backup occur kv error"][error="{\"KvError\":{\"locked\":`

バックアッププロセス中にキーがロックされている場合、BRはロックを解決しようとします。このエラーの数が少ない場合でも、バックアップの正確性には影響しません。

### バックアップの失敗 {#backup-failure}

ログのエラーメッセージ： `log - Error: msg:"Io(Custom { kind: AlreadyExists, error: \"[5_5359_42_123_default.sst] is already exists in /dir/backup_local/\" })"`

バックアップ操作が失敗し、上記のメッセージが表示された場合は、次のいずれかの操作を実行してから、バックアップ操作を再開してください。

-   バックアップ用のディレクトリを変更します。たとえば、 `/dir/backup-2020-01-01/`を`/dir/backup_local/`に変更します。
-   すべてのTiKVノードとBRノードのバックアップディレクトリを削除します。
