---
title: tiup cluster check
summary: TiUP クラスタは、ハードウェアとソフトウェア環境が本番の要件を満たしていることを確認するための「check」コマンドを提供します。OSバージョン、CPUサポート、時刻同期、システム制限などをチェックします。オプションには、自動修復や、CPUコア数、メモリサイズ、ディスクパフォーマンスのチェックの有効化などがあります。チェックを実行するには、「tiup cluster check <topology.yml | cluster-name> [flags]」コマンドを使用します。自動修復を試行するには、「--apply」を使用します。チェックするノードとロールを指定するには、「-N, --node」および「-R, --role」を使用します。特定のチェックを有効にするには、「--enable-cpu」、「--enable-disk」、「--enable-mem」を使用します。
---

# tiup cluster check {#tiup-cluster-check}

正式な本番環境では、稼働前に一連のチェックを実施し、クラスターが最高のパフォーマンスを発揮していることを確認する必要があります。手動チェックの手順を簡素化するため、 TiUP クラスタは、指定されたクラスターのターゲットマシンのハードウェアおよびソフトウェア環境が正常に動作するための要件を満たしているかどうかを確認するための`check`のコマンドを提供しています。

## チェック項目一覧 {#list-of-check-items}

### オペレーティング システムのバージョン {#operating-system-version}

デプロイされたマシンのオペレーティングシステムのディストリビューションとバージョンを確認してください。サポートされているバージョンのリストについては、 [OSおよびプラットフォームの要件](/hardware-and-software-requirements.md#os-and-platform-requirements)参照してください。

### CPU EPOLLEX限定 {#cpu-epollexclusive}

対象マシンのCPUがEPOLLEXCLUSIVEをサポートしているかどうかを確認します。

### ヌマクトル {#numactl}

ターゲットマシンに`numactl`インストールされているかどうかを確認してください。ターゲットマシンに複数のコアが紐付けられている場合は、 `numactl`インストールする必要があります。

### システム時間 {#system-time}

対象マシンのシステム時刻が同期されているかどうかを確認します。対象マシンのシステム時刻と中央制御マシンのシステム時刻を比較し、偏差が一定の閾値（500ミリ秒）を超えた場合はエラーを報告します。

### システムのタイムゾーン {#system-time-zone}

対象マシンのシステムタイムゾーンが同期されているかどうかを確認します。これらのマシンのタイムゾーン設定を比較し、タイムゾーンが一致していない場合はエラーを報告します。

### 時刻同期サービス {#time-synchronization-service}

ターゲットマシンで時刻同期サービスが設定されているかどうかを確認します。つまり、ntpd が実行中かどうかを確認します。

### スワップパーティション {#swap-partitioning}

ターゲットマシンでスワップパーティションが有効になっているかどうかを確認してください。スワップパーティションを無効にすることをお勧めします。

### カーネルパラメータ {#kernel-parameters}

次のカーネル パラメータの値を確認します。

-   `net.ipv4.tcp_tw_recycle` : 0
-   `net.ipv4.tcp_syncookies` : 0
-   `net.core.somaxconn` : 32768
-   `vm.swappiness` : 0
-   `vm.overcommit_memory` ：0または1
-   `fs.file-max` : 1000000

### 透過的な巨大ページ (THP) {#transparent-huge-pages-thp}

対象マシンでTHPが有効になっているかどうかを確認してください。THPを無効にすることをお勧めします。

THP が有効になっているかどうかを確認するには、次のコマンドを実行します。

    cat /sys/kernel/mm/transparent_hugepage/enabled

`never`に設定されていない場合は`grubby --update-kernel=ALL --args="transparent_hugepage=never"`に変更できます。

実行中の設定を変更するには、再起動するか、 `echo never > /sys/kernel/mm/transparent_hugepage/enabled`実行します。

### システム制限 {#system-limits}

`/etc/security/limits.conf`ファイル内の制限値を確認します。

    <deploy-user> soft nofile 1000000
    <deploy-user> hard nofile 1000000
    <deploy-user> soft stack 10240

`<deploy-user>`は TiDB クラスターを展開して実行するユーザーであり、最後の列はシステムに必要な最小値です。

### SELinux {#selinux}

SELinuxを無効にするか、permissiveモードに設定する必要があります。現在のステータスを確認するには、 [ゲットエンフォース(8)](https://linux.die.net/man/8/getenforce)ユーティリティを使用してください。

SELinuxが無効になっていない場合は、 `/etc/selinux/config`ファイルを開き、 `SELINUX=`で始まる行を`SELINUX=disabled`に変更します。この変更を行った後、システムを再起動する必要があります。7または`enforcing` `permissive` `disabled`への変更は、再起動しないと有効になりません。

一部のシステム（Ubuntuなど）では、 `/etc/selinux/config`ファイルが存在せず、getenforceユーティリティがインストールされていない場合があります。その場合は、この手順をスキップしてください。

### ファイアウォール {#firewall}

FirewallD サービスが有効になっているかどうかを確認してください。FirewallD サービスを無効にするか、TiDB クラスター内の各サービスに権限ルールを追加することをお勧めします。

### irqバランス {#irqbalance}

irqbalanceサービスが有効になっているかどうかを確認してください。irqbalanceサービスを有効にすることをお勧めします。

### ディスクマウントオプション {#disk-mount-options}

ext4パーティションのマウントオプションを確認してください。マウントオプションにnodelallocオプションとnoatimeオプションが含まれていることを確認してください。

### ポートの使用 {#port-usage}

トポロジで定義されているポート (自動補完のデフォルト ポートを含む) が、ターゲット マシン上のプロセスによってすでに使用されているかどうかを確認します。

> **注記：**
>
> ポート使用状況チェックは、クラスターがまだ起動していないことを前提としています。クラスターが既にデプロイされ起動されている場合、ポートは使用中であるはずなので、クラスターのポート使用状況チェックは失敗します。

### CPUコア数 {#cpu-core-number}

対象マシンのCPU情報を確認してください。本番のクラスタでは、CPU論理コアの数が16以上であることが推奨されます。

> **注記：**
>
> CPUコア数はデフォルトではチェックされません。チェックを有効にするには、コマンドに`-enable-cpu`オプションを追加する必要があります。

### メモリサイズ {#memory-size}

対象マシンのメモリサイズを確認してください。本番のクラスターでは、合計メモリ容量が32GB以上であることが推奨されます。

> **注記：**
>
> メモリサイズはデフォルトではチェックされません。チェックを有効にするには、コマンドに`-enable-mem`オプションを追加する必要があります。

### Fioディスクパフォーマンステスト {#fio-disk-performance-test}

フレキシブル I/O テスター (fio) を使用して、次の 3 つのテスト項目を含む、 `data_dir`が配置されているディスクのパフォーマンスをテストします。

-   fio_randread_write_latency
-   fio_randread_write
-   fio_randread

> **注記：**
>
> fioディスクパフォーマンステストはデフォルトでは実行されません。テストを実行するには、コマンドに`-enable-disk`オプションを追加する必要があります。

## 構文 {#syntax}

```shell
tiup cluster check <topology.yml | cluster-name> [flags]
```

-   クラスターがまだデプロイされていない場合は、クラスターのデプロイに使用する[トポロジー.yml](/tiup/tiup-cluster-topology-reference.md)ファイルを渡す必要があります。このファイルの内容に従って、 tiup-clusterは対応するマシンに接続し、チェックを実行します。
-   クラスターがすでにデプロイされている場合は、チェック オブジェクトとして`<cluster-name>`使用できます。
-   既存のクラスターのスケールアウト YAML ファイルをチェックする場合は、チェック オブジェクトとして`<scale-out.yml>`と`<cluster-name>`両方を使用できます。

> **注記：**
>
> チェックに`<cluster-name>`使用する場合は、コマンドに`--cluster`オプションを追加する必要があります。

## オプション {#options}

### - 適用する {#apply}

-   失敗したチェック項目の自動修復を試みます。現在、 tiup-cluster は以下のチェック項目のみを修復しようとします。
    -   SELinux
    -   ファイアウォール
    -   irqバランス
    -   カーネルパラメータ
    -   システム制限
    -   THP (透過的巨大ページ)
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで値`false`で無効になっています。このオプションを有効にするには、コマンドにこのオプションを追加し、値`true`を渡すか、値を渡さないでください。

> **注記：**
>
> `tiup cluster check` 、次のコマンド形式を使用して、既存のクラスターの`scale-out.yml`ファイルの修復もサポートされています。
>
> ```shell
> tiup cluster check <cluster-name> scale-out.yml --cluster --apply --user root [-p] [-i /home/root/.ssh/gcp_rsa]
> ```

### - クラスタ {#cluster}

-   チェックがデプロイ済みのクラスターを対象としていることを示します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで値`false`で無効になっています。このオプションを有効にするには、コマンドにこのオプションを追加し、値`true`を渡すか、値を渡さないでください。
-   コマンド形式:

    ```shell
    tiup cluster check <topology.yml | cluster-name> --cluster [flags]
    ```

> **注記：**
>
> -   `tiup cluster check <cluster-name>`コマンドを使用する場合は、 `--cluster`オプション`tiup cluster check <cluster-name> --cluster`追加する必要があります。
> -   `tiup cluster check`では、次のコマンド形式を使用して、既存のクラスターの`scale-out.yml`ファイルを確認することもサポートされています。
>
>     ```shell
>     tiup cluster check <cluster-name> scale-out.yml --cluster --user root [-p] [-i /home/root/.ssh/gcp_rsa]
>     ```

### -N, --node {#n-node}

-   チェックするノードを指定します。このオプションの値は、ノードIDのカンマ区切りのリストです。ノードIDは、 [`tiup cluster display`](/tiup/tiup-component-cluster-display.md)コマンドで返されるクラスターステータステーブルの最初の列から取得できます。
-   データ型: `STRINGS`
-   コマンドでこのオプションを指定しない場合は、デフォルトですべてのノードがチェックされます。

> **注記：**
>
> `-R, --role`オプションを同時に指定した場合は、 `-N, --node`と`-R, --role`両方の指定に一致するサービス ノードのみがチェックされます。

### -R, --role {#r-role}

-   チェックするロールを指定します。このオプションの値は、ノードロールのコンマ区切りのリストです。ノードのロールは、 [`tiup cluster display`](/tiup/tiup-component-cluster-display.md)コマンドで返されるクラスターステータステーブルの2列目から取得できます。
-   データ型: `STRINGS`
-   コマンドでこのオプションを指定しない場合は、すべてのロールがデフォルトでチェックされます。

> **注記：**
>
> `-N, --node`オプションを同時に指定した場合は、 `-N, --node`と`-R, --role`両方の指定に一致するサービス ノードのみがチェックされます。

### --enable-CPU {#enable-cpu}

-   CPUコア数のチェックを有効にします。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで値`false`で無効になっています。このオプションを有効にするには、コマンドにこのオプションを追加し、値`true`を渡すか、値を渡さないでください。

### --enable-disk {#enable-disk}

-   fio ディスク パフォーマンス テストを有効にします。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで値`false`で無効になっています。このオプションを有効にするには、コマンドにこのオプションを追加し、値`true`を渡すか、値を渡さないでください。

### --enable-mem {#enable-mem}

-   メモリサイズのチェックを有効にします。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで値`false`で無効になっています。このオプションを有効にするには、コマンドにこのオプションを追加し、値`true`を渡すか、値を渡さないでください。

### --u, --user {#u-user}

-   ターゲットマシンに接続するためのユーザー名を指定します。指定されたユーザーは、ターゲットマシン上でパスワード不要のsudo root権限を持っている必要があります。
-   データ型: `STRING`
-   コマンドでこのオプションを指定しない場合は、コマンドを実行したユーザーがデフォルト値として使用されます。

> **注記：**
>
> このオプションは、 `-cluster`オプションが false の場合にのみ有効です。それ以外の場合、このオプションの値は、クラスタデプロイメントのトポロジファイルで指定されたユーザー名に固定されます。

### -i, --identity_file {#i-identity-file}

-   ターゲット マシンに接続するためのキー ファイルを指定します。
-   データ型: `STRING`
-   このオプションはデフォルトで有効になっており、 `~/.ssh/id_rsa` (デフォルト値) が渡されます。

> **注記：**
>
> このオプションは、 `--cluster`オプションが false の場合にのみ有効です。それ以外の場合、このオプションの値は`${TIUP_HOME}/storage/cluster/clusters/<cluster-name>/ssh/id_rsa`に固定されます。

### -p, --パスワード {#p-password}

-   ターゲットマシンに接続するときにパスワードを使用してログインします。
    -   クラスターに`--cluster`オプションが追加された場合、パスワードはクラスターのデプロイ時にトポロジ ファイルに指定されたユーザーのパスワードになります。
    -   クラスターにオプション`--cluster`追加されていない場合、パスワードはオプション`-u/--user`で指定されたユーザーのパスワードになります。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで値`false`で無効になっています。このオプションを有効にするには、コマンドにこのオプションを追加し、値`true`を渡すか、値を渡さないでください。

### -h, --help {#h-help}

-   関連するコマンドのヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで値`false`で無効になっています。このオプションを有効にするには、コマンドにこのオプションを追加し、値`true`を渡すか、値を渡さないでください。

## 出力 {#output}

次のフィールドを含むテーブル:

-   `Node` : ターゲットノード
-   `Check` : チェック項目
-   `Result` : チェック結果（合格、警告、不合格）
-   `Message` : 結果の説明

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
