---
title: BR Use Cases
summary: Learn the use cases of backing up and restoring data using BR.
---

# BR ユースケース {#br-use-cases}

[バックアップと復元 (BR)](/br/backup-and-restore-overview.md)は、TiDB クラスター データの分散バックアップおよび復元用のツールです。

このドキュメントでは、一般的なバックアップと復元のシナリオについて説明します。

-   [1 つのテーブルをネットワーク ディスクにバックアップする (運用環境に推奨)](#back-up-a-single-table-to-a-network-disk-recommended-for-production-environments)
-   [ネットワーク ディスクからのデータの復元 (本番環境に推奨)](#restore-data-from-a-network-disk-recommended-for-production-environments)
-   [1 つのテーブルをローカル ディスクにバックアップする](#back-up-a-single-table-to-a-local-disk-recommended-for-testing-environments)
-   [ローカル ディスクからデータを復元する](#restore-data-from-a-local-disk-recommended-for-testing-environments)

このドキュメントは、次の目標の達成を支援することを目的としています。

-   ネットワーク ディスクまたはローカル ディスクを正しく使用して、データのバックアップと復元を行ってください。
-   メトリックを監視して、バックアップまたは復元操作のステータスを取得します。
-   バックアップまたは復元操作中にパフォーマンスを調整する方法を学びます。
-   バックアップ操作中に発生する可能性のある異常をトラブルシューティングします。

## 観客 {#audience}

TiDB と[TiKV](https://tikv.org/)の基本的な知識が必要です。

読み進める前に、 [BRの概要](/br/backup-and-restore-overview.md) 、特に[使用制限](/br/backup-and-restore-overview.md#usage-restrictions)と[いくつかのヒント](/br/backup-and-restore-overview.md#some-tips)を読んだことを確認してください。

## 前提条件 {#prerequisites}

このセクションでは、TiDB の推奨デプロイ方法、クラスター バージョン、TiKV クラスターのハードウェア情報、およびユース ケース デモンストレーション用のクラスター構成を紹介します。

独自のハードウェアと構成に基づいて、バックアップまたは復元操作のパフォーマンスを見積もることができます。データのバックアップと復元には、ネットワーク ディスクを使用することをお勧めします。これにより、バックアップ ファイルを収集する手間が省け、特に TiKV クラスターが大規模な場合にバックアップ効率が大幅に向上します。

### 導入方法 {#deployment-method}

[TiUP](/tiup/tiup-cluster.md)を使用して TiDB クラスターをデプロイし、TiUP を使用して BR をインストールすることをお勧めします。

### クラスタのバージョン {#cluster-versions}

-   TiDB: v6.1.2
-   TiKV: v6.1.2
-   PD: v6.1.2
-   BR: v6.1.2

> **ノート：**
>
> [TiDB/TiKV/PD/BR](/releases/release-notes.md)の最新バージョンを使用し、BR バージョンが TiDB バージョンと**一致して**いることを確認することをお勧めします。

### TiKV ハードウェア情報 {#tikv-hardware-information}

-   オペレーティング システム: CentOS Linux リリース 7.6.1810 (コア)
-   CPU: 16 コア共通 KVM プロセッサ
-   RAM: 32GB
-   ディスク: 500 GB SSD * 2
-   NIC: 10 ギガビット ネットワーク カード

### クラスタ構成 {#cluster-configuration}

BR は直接 TiKV クラスターにコマンドを送信し、TiDBサーバーに依存しないため、BR を使用する場合に TiDBサーバーを構成する必要はありません。

-   TiKV: デフォルト設定
-   PD: デフォルト設定

### その他 {#others}

上記の前提条件に加えて、バックアップと復元を実行する前に、次のチェックも実行する必要があります。

#### バックアップ前の確認 {#check-before-backup}

[`br backup`コマンド](/br/use-br-command-line-tool.md#br-command-line-description)を実行する前に、次の条件が満たされていることを確認してください。

-   TiDB クラスターで実行されている DDL ステートメントはありません。
-   ターゲット ストレージ デバイスには、必要な容量 (バックアップ クラスターのディスク容量の 1/3 以上) が必要です。

#### 復旧前の確認 {#check-before-restoration}

[`br restore`コマンド](/br/use-br-command-line-tool.md#br-command-line-description)を実行する前に、ターゲット クラスターをチェックして、このクラスター内のテーブルに重複した名前がないことを確認します。

## 1 つのテーブルをネットワーク ディスクにバックアップする (運用環境に推奨) {#back-up-a-single-table-to-a-network-disk-recommended-for-production-environments}

`br backup`コマンドを実行して、単一テーブル データ`--db batchmark --table order_line`をネットワーク ディスクの指定されたパス`local:///br_data`にバックアップします。

### バックアップの前提条件 {#backup-prerequisites}

-   [バックアップ前の確認](#check-before-backup)
-   高性能 SSD ハードディスク ホストを NFSサーバーとして構成してデータを保存し、すべての BR ノード、TiKV ノード、および TiFlash ノードを NFS クライアントとして構成します。 NFS クライアントがサーバーにアクセスできるように、NFSサーバーに同じパス (たとえば、 `/br_data` ) をマウントします。
-   NFSサーバーとすべての NFS クライアント間の合計転送速度は、少なくとも`the number of TiKV instances * 150MB/s`に達する必要があります。そうしないと、ネットワーク I/O がパフォーマンスのボトルネックになる可能性があります。

> **ノート：**
>
> -   データバックアップ時は、リーダーレプリカのデータのみをバックアップするため、クラスター内にTiFlashレプリカが存在する場合でも、BRはTiFlashノードをマウントせずにバックアップを完了できます。
> -   データを復元する場合、BR はすべてのレプリカのデータを復元します。また、TiFlash ノードは、リストアを完了するために BR のバックアップ データにアクセスする必要があります。したがって、復元の前に、TiFlash ノードを NFSサーバーにマウントする必要があります。

### トポロジー {#topology}

次の図は、BR の類型を示しています。

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

### バックアップのモニタリング メトリック {#monitoring-metrics-for-the-backup}

バックアップ プロセス中は、監視パネルの次のメトリックに注意して、バックアップ プロセスのステータスを取得します。

**バックアップ CPU 使用率**: バックアップ操作で動作している各 TiKV ノードの CPU 使用率 (たとえば、バックアップ ワーカーとバックアップ エンドポイント)。

![img](/media/br/backup-cpu.png)

**IO 使用率**: バックアップ操作で動作している各 TiKV ノードの I/O 使用率。

![img](/media/br/backup-io.png)

**BackupSST Generation Throughput** : バックアップ操作で動作している各 TiKV ノードの backupSST 生成スループット。通常は約 150 MB/秒です。

![img](/media/br/backup-throughput.png)

**One Backup Range Duration** : 範囲をバックアップする期間。これは、KV をスキャンし、範囲を backupSST ファイルとして保存するための合計時間コストです。

![img](/media/br/backup-range-duration.png)

**1 つのバックアップ サブタスク期間**: バックアップ タスクが分割された各サブタスクの期間。

> **ノート：**
>
> -   このタスクでは、バックアップする 1 つのテーブルに 3 つのインデックスがあり、タスクは通常 4 つのサブタスクに分割されます。
> -   次の画像のパネルには 20 個のポイントがあり、10 個が青、10 個が黄色であり、10 個のサブタスクがあることを示しています。リージョンのスケジューリングはバックアップ プロセス中に発生する可能性があるため、数回の再試行は正常です。

![img](/media/br/backup-subtask-duration.png)

**バックアップ エラー**: バックアップ プロセス中に発生したエラー。通常の状況ではエラーは発生しません。多少のエラーが発生した場合でも、バックアップ操作には再試行メカニズムがあり、バックアップ時間が長くなる可能性がありますが、操作の正確性には影響しません。

![img](/media/br/backup-errors.png)

**Checksum Request Duration** : バックアップ クラスタでの管理チェックサム リクエストの期間。

![img](/media/br/checksum-duration.png)

### バックアップ結果の説明 {#backup-results-explanation}

バックアップが完了すると、BR はバックアップの概要をコンソールに出力します。

バックアップコマンドを実行する前に指定したログでは、このログからバックアップ操作の統計情報を取得できます。このログで「概要」を検索すると、次の情報が表示されます。

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

-   `total take(Full backup time)` : バックアップ期間
-   `total take(real time)` : アプリケーションの総実行時間
-   `total size(MB)` : バックアップ データのサイズ
-   `avg speed(MB/s)` : バックアップ スループット
-   `total kv` : バックアップされた KV ペアの数
-   `backup checksum` : バックアップ チェックサム期間
-   `backup fast checksum` : 各テーブルのチェックサム、KV ペア、およびバイトを計算する合計時間
-   `backup total regions` : バックアップ リージョンの総数
-   `BackupTS` : バックアップ データのスナップショット タイムスタンプ
-   `Size` : 圧縮後のディスク内のバックアップ データの実際のサイズ

上記の情報から、単一の TiKV インスタンスのスループットを計算できます: `avg speed(MB/s)` / `tikv_count` = `62.86` 。

### 性能調整 {#performance-tuning}

バックアップ プロセス中に TiKV のリソース使用率が明らかなボトルネックにならない場合 (たとえば、 [バックアップのモニタリング メトリック](#monitoring-metrics-for-the-backup)で、backup-worker の最大 CPU 使用率が`1500%`前後で、全体の I/O 使用率が`30%`未満である場合)、 `--concurrency` (デフォルトでは`4` ) の値を増やして、パフォーマンスを調整できます。ただし、このパフォーマンス チューニング方法は、多くの小さなテーブルのユース ケースには適していません。次の例を参照してください。

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

チューニングされたパフォーマンスの結果は次のとおりです (データ サイズは同じです)。

-   バックアップ期間 ( `total take(s)` ): `986.43`から`535.53`に短縮
-   バックアップ スループット ( `avg speed(MB/s)` ): `358.09`から`659.59`に増加
-   単一の TiKV インスタンスのスループット ( `avg speed(MB/s)/tikv_count` ): `89`から`164.89`に増加

## ネットワーク ディスクからのデータの復元 (本番環境に推奨) {#restore-data-from-a-network-disk-recommended-for-production-environments}

`br restore`コマンドを使用して、完全なバックアップ データをオフライン クラスターに復元します。現在、BR はオンライン クラスターへのデータの復元をサポートしていません。

### 復元の前提条件 {#restoration-prerequisites}

-   [復元前の確認](#check-before-restoration)

### トポロジー {#topology}

次の図は、BR の類型を示しています。

![img](/media/br/restore-nfs-deploy.png)

### 復旧作業 {#restoration-operation}

`br restore`コマンドを実行します。

{{< copyable "" >}}

```shell
bin/br restore table --db batchmark --table order_line -s local:///br_data --pd 172.16.5.198:2379 --log-file restore-nfs.log
```

### 復元のモニタリング メトリック {#monitoring-metrics-for-the-restoration}

復元プロセス中は、監視パネルの次のメトリックに注意して、復元プロセスのステータスを取得してください。

**CPU** : 復元操作における各稼働中の TiKV ノードの CPU 使用率。

![img](/media/br/restore-cpu.png)

**IO 使用率**: 復元操作で動作している各 TiKV ノードの I/O 使用率。

![img](/media/br/restore-io.png)

**リージョン**:リージョン分布。リージョンが均等に分散されているほど、復元リソースがより適切に使用されます。

![img](/media/br/restore-region.png)

**Process SST Duration** : SST ファイルの処理の遅延。テーブルを復元する場合、 `tableID`を変更した場合は`tableID`を書き換える必要があります。それ以外の場合、 `tableID`は名前が変更されます。一般に、書き換えの遅延は、名前の変更の遅延よりも長くなります。

![img](/media/br/restore-process-sst.png)

**ダウンロード SST スループット**: 外部ストレージから SST ファイルをダウンロードするスループット。

![img](/media/br/restore-download-sst.png)

**復元エラー**: 復元プロセス中に発生したエラー。

![img](/media/br/restore-errors.png)

**Checksum Request Duration** : 管理チェックサム要求の期間。このリストアの所要時間は、バックアップの所要時間よりも長くなります。

![img](/media/br/restore-checksum.png)

### 復元結果の説明 {#restoration-results-explanation}

リストアコマンドを実行する前に指定したログでは、このログからリストア操作の統計情報を取得できます。このログで「概要」を検索すると、次の情報が表示されます。

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

-   `total take(Full restore time)` : 復元期間
-   `total take(real time)` : アプリケーションの総実行時間
-   `total size(MB)` : 復元するデータのサイズ
-   `total kv` : 復元された KV ペアの数
-   `avg speed(MB/s)` : 復元スループット
-   `split region` :リージョン分割デュレーション
-   `restore checksum` : 復元チェックサム期間
-   `Size` : ディスク内の復元されたデータの実際のサイズ

上記の情報から、次の項目を計算できます。

-   単一の TiKV インスタンスのスループット: `avg speed(MB/s)` / `tikv_count` = `91.8`
-   単一の TiKV インスタンスの平均復元速度: `total size(MB)` /( `split time` + `restore time` )/ `tikv_count` = `87.4`

#### 性能調整 {#performance-tuning}

復元プロセス中に TiKV のリソース使用量が明らかなボトルネックにならない場合は、値`--concurrency`を増やすことができます (デフォルトは`128` )。次の例を参照してください。

{{< copyable "" >}}

```shell
bin/br restore table --db batchmark --table order_line -s local:///br_data/ --pd 172.16.5.198:2379 --log-file restore-concurrency.log --concurrency 1024
```

チューニングされたパフォーマンスの結果は次のとおりです (データ サイズは同じです)。

-   回復時間 ( `total take(s)` ): `961.37`から`443.49`に減少
-   復元スループット ( `avg speed(MB/s)` ): `367.42`から`796.47`に増加
-   単一の TiKV インスタンスのスループット ( `avg speed(MB/s)` / `tikv_count` ): `91.8`から`199.1`に増加
-   単一の TiKV インスタンスの平均復元速度 ( `total size(MB)` /( `split time` + `restore time` )/ `tikv_count` ): `87.4`から`162.3`に増加

## 1 つのテーブルをローカル ディスクにバックアップする (テスト環境に推奨) {#back-up-a-single-table-to-a-local-disk-recommended-for-testing-environments}

`br backup`コマンドを実行して、単一のテーブル`--db batchmark --table order_line`をローカル ディスクの指定されたパス`local:///home/tidb/backup_local`にバックアップします。

### バックアップの前提条件 {#backup-prerequisites}

-   [バックアップ前の確認](#check-before-backup)
-   各 TiKV ノードには、backupSST ファイルを格納するための個別のディスクがあります。
-   `backup_endpoint`のノードには、 `backupmeta`のファイルを格納するための個別のディスクがあります。
-   TiKV と`backup_endpoint`ノードは、バックアップ用に同じディレクトリ (たとえば、 `/home/tidb/backup_local` ) を共有します。

### トポロジー {#topology}

次の図は、BR の類型を示しています。

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

バックアップ プロセス中は、監視パネルのメトリックに注意して、バックアップ プロセスのステータスを取得します。詳細は[バックアップのモニタリング メトリック](#monitoring-metrics-for-the-backup)を参照してください。

#### バックアップ結果の説明 {#backup-results-explanation}

バックアップコマンドを実行する前に指定したログでは、このログからリストア操作の統計情報を取得できます。このログで「概要」を検索すると、次の情報が表示されます。

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

-   `total take(s)` : バックアップ期間
-   `total size(MB)` : データサイズ
-   `avg speed(MB/s)` : バックアップのスループット
-   `backup checksum` : バックアップ チェックサム期間

上記の情報から、単一の TiKV インスタンスのスループットを計算できます: `avg speed(MB/s)` / `tikv_count` = `160` 。

## ローカル ディスクからデータを復元する (テスト環境に推奨) {#restore-data-from-a-local-disk-recommended-for-testing-environments}

`br restore`コマンドを実行して、完全なバックアップ データをオフライン クラスターに復元します。現在、BR はオンライン クラスターへのデータの復元をサポートしていません。

### 復元の前提条件 {#restoration-prerequisites}

-   [復元前の確認](#check-before-restoration)
-   TiKV クラスターとバックアップ データには、重複するデータベースまたはテーブルがありません。現在、BR はテーブル ルートをサポートしていません。
-   各 TiKV ノードには、backupSST ファイルを格納するための個別のディスクがあります。
-   `restore_endpoint`のノードには、 `backupmeta`のファイルを格納するための個別のディスクがあります。
-   TiKV と`restore_endpoint`ノードは、復元のために同じディレクトリ (たとえば、 `/home/tidb/backup_local/` ) を共有します。

復元する前に、次の手順に従います。

1.  すべての backupSST ファイルを同じディレクトリーに集めます。
2.  収集した backupSST ファイルをクラスターのすべての TiKV ノードにコピーします。
3.  `backupmeta`ファイルを`restore endpoint`ノードにコピーします。

### トポロジー {#topology}

次の図は、BR の類型を示しています。

![img](/media/br/restore-local-deploy.png)

### 復旧作業 {#restoration-operation}

`br restore`コマンドを実行します。

{{< copyable "" >}}

```shell
bin/br restore table --db batchmark --table order_line -s local:///home/tidb/backup_local/ --pd 172.16.5.198:2379 --log-file restore_local.log
```

復元プロセス中は、監視パネルのメトリックに注意して、復元プロセスのステータスを取得してください。詳細は[復元のモニタリング メトリック](#monitoring-metrics-for-the-restoration)を参照してください。

### 復元結果の説明 {#restoration-results-explanation}

リストアコマンドを実行する前に指定したログでは、このログからリストア操作の統計情報を取得できます。このログで「概要」を検索すると、次の情報が表示されます。

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

-   `total take(s)` : 復元期間
-   `total size(MB)` : データサイズ
-   `avg speed(MB/s)` : 復元スループット
-   `split region` : リージョン分割のデュレーション
-   `restore checksum` : 復元チェックサム期間

上記の情報から、次の項目を計算できます。

-   単一の TiKV インスタンスのスループット: `avg speed(MB/s)` / `tikv_count` = `97.2`
-   単一の TiKV インスタンスの平均復元速度: `total size(MB)` /( `split time` + `restore time` )/ `tikv_count` = `92.4`

## バックアップ中のエラー処理 {#error-handling-during-backup}

このセクションでは、バックアップ プロセス中に発生する可能性のある一般的なエラーについて説明します。

### <code>key locked Error</code> {#code-key-locked-error-code-in-the-backup-log}

ログのエラー メッセージ: `log - ["backup occur kv error"][error="{\"KvError\":{\"locked\":`

バックアップ プロセス中にキーがロックされている場合、BR はロックの解決を試みます。少数のこのエラーは、バックアップの正確性には影響しません。

### バックアップの失敗 {#backup-failure}

ログのエラー メッセージ: `log - Error: msg:"Io(Custom { kind: AlreadyExists, error: \"[5_5359_42_123_default.sst] is already exists in /dir/backup_local/\" })"`

バックアップ操作が失敗し、前述のメッセージが表示された場合は、次の操作のいずれかを実行してから、バックアップ操作を再度開始します。

-   バックアップのディレクトリを変更します。たとえば、 `/dir/backup-2020-01-01/`を`/dir/backup_local/`に変更します。
-   すべての TiKV ノードと BR ノードのバックアップ ディレクトリを削除します。
