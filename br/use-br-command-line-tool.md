---
title: Use BR Command-line for Backup and Restoration
summary: Learn how to use the BR command line to backup and restore cluster data.
---

# バックアップと復元にBRコマンドラインを使用する {#use-br-command-line-for-backup-and-restoration}

このドキュメントでは、 BRコマンド ラインを使用して TiDB クラスター データをバックアップおよび復元する方法について説明します。

[BRツールの概要](/br/backup-and-restore-tool.md) 、特に[使用制限](/br/backup-and-restore-tool.md#usage-restrictions)と[ベストプラクティス](/br/backup-and-restore-tool.md#best-practices)を読んだことを確認してください。

## BRコマンドラインの説明 {#br-command-line-description}

`br`コマンドは、サブコマンド、オプション、およびパラメーターで構成されます。

-   サブコマンド: `-`または`--`のない文字。
-   オプション: `-`または`--`で始まる文字。
-   パラメータ: 直後に続き、サブコマンドまたはオプションに渡される文字。

これは完全な`br`のコマンドです。

{{< copyable "" >}}

```shell
br backup full --pd "${PDIP}:2379" -s "local:///tmp/backup"
```

上記のコマンドの説明は次のとおりです。

-   `backup` : `br`のサブコマンド。
-   `full` : `backup`のサブコマンド。
-   `-s` (または`--storage` ): バックアップ ファイルが格納されるパスを指定するオプション。
-   `"local:///tmp/backup"` : `-s`のパラメーター。 `/tmp/backup`は、各 TiKV ノードのバックアップ ファイルが保存されるローカル ディスク内のパスです。
-   `--pd` : Placement Driver (PD) サービス アドレスを指定するオプション。
-   `"${PDIP}:2379"` : `--pd`のパラメーター。

> **ノート：**
>
> -   `local`のストレージを使用する場合、バックアップ データは各ノードのローカル ファイル システムに分散されます。
>
> -   データの復元を完了するには、これらのデータを手動で集約する必要**が**あるため、本番環境でローカル ディスクにバックアップすることは<strong>お勧め</strong>しません。詳細については、 [クラスタデータの復元](#use-br-command-line-to-restore-cluster-data)を参照してください。
>
> -   これらのバックアップデータを集約すると、冗長性が生じ、運用や保守に支障をきたす可能性があります。さらに悪いことに、これらのデータを集約せずにデータを復元すると、かなり紛らわしいエラー メッセージが表示される可能性があります`SST file not found` 。
>
> -   各ノードに NFS ディスクをマウントするか、 `S3`のオブジェクト ストレージにバックアップすることをお勧めします。

### サブコマンド {#sub-commands}

`br`のコマンドは、サブコマンドの複数のレイヤーで構成されます。現在、 BRには次の 3 つのサブコマンドがあります。

-   `br backup` : TiDB クラスターのデータをバックアップするために使用されます。
-   `br restore` : TiDB クラスターのデータを復元するために使用されます。

上記の 3 つのサブコマンドのそれぞれには、操作の範囲を指定する次の 3 つのサブコマンドが含まれる場合があります。

-   `full` : すべてのクラスター データのバックアップまたは復元に使用されます。
-   `db` : クラスターの指定されたデータベースのバックアップまたは復元に使用されます。
-   `table` : クラスターの指定されたデータベース内の単一のテーブルをバックアップまたは復元するために使用されます。

### 共通オプション {#common-options}

-   `--pd` : 接続に使用され、PDサーバーのアドレスを指定します。たとえば、 `"${PDIP}:2379"`です。
-   `-h` (または`--help` ): すべてのサブコマンドのヘルプを取得するために使用されます。たとえば、 `br backup --help`です。
-   `-V` (または`--version` ): BRのバージョンを確認するために使用されます。
-   `--ca` : 信頼できる CA 証明書へのパスを PEM 形式で指定します。
-   `--cert` : SSL 証明書へのパスを PEM 形式で指定します。
-   `--key` : SSL 証明書キーへのパスを PEM 形式で指定します。
-   `--status-addr` : BRが Prometheus に統計情報を提供するためのリスニング アドレスを指定します。

## BRコマンドラインを使用してクラスター データをバックアップする {#use-br-command-line-to-back-up-cluster-data}

クラスター データをバックアップするには、 `br backup`コマンドを使用します。 `full`または`table`サブコマンドを追加して、バックアップ操作の範囲 (クラスター全体または単一のテーブル) を指定できます。

### すべてのクラスター データをバックアップする {#back-up-all-the-cluster-data}

すべてのクラスタ データをバックアップするには、 `br backup full`コマンドを実行します。このコマンドのヘルプを表示するには、 `br backup full -h`または`br backup full --help`を実行します。

**使用例:**

すべてのクラスター データを各 TiKV ノードの`/tmp/backup`パスにバックアップし、 `backupmeta`ファイルをこのパスに書き込みます。

> **ノート：**
>
> -   バックアップ ディスクとサービス ディスクが異なる場合、オンライン バックアップでは、全速バックアップの場合、読み取り専用オンライン サービスの QPS が約 15% ～ 25% 低下することがテストされています。 QPS への影響を減らしたい場合は、 `--ratelimit`を使用してレートを制限します。
>
> -   バックアップ ディスクとサービス ディスクが同じ場合、バックアップはサービスと I/O リソースを競合します。これにより、読み取り専用オンライン サービスの QPS が半分以上低下する可能性があります。したがって、オンライン サービス データを TiKV データ ディスクにバックアップすることは**強くお勧め**しません。

{{< copyable "" >}}

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --storage "local:///tmp/backup" \
    --ratelimit 128 \
    --log-file backupfull.log
```

上記のコマンドのいくつかのオプションの説明は次のとおりです。

-   `--ratelimit` : 各 TiKV ノードでバックアップ操作が実行される最大速度 (MiB/秒) を指定します。
-   `--log-file` : BRログを`backupfull.log`ファイルに書き込むことを指定します。

バックアップ中はターミナルに進行状況バーが表示されます。プログレス バーが 100% まで進むと、バックアップは完了です。次に、 BRはバックアップ データもチェックして、データの安全性を確保します。プログレスバーは次のように表示されます。

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --storage "local:///tmp/backup" \
    --ratelimit 128 \
    --log-file backupfull.log
Full Backup <---------/................................................> 17.12%.
```

### データベースのバックアップ {#back-up-a-database}

クラスタ内のデータベースをバックアップするには、 `br backup db`コマンドを実行します。このコマンドのヘルプを表示するには、 `br backup db -h`または`br backup db --help`を実行します。

**使用例:**

`test`データベースのデータを各 TiKV ノードの`/tmp/backup`パスにバックアップし、 `backupmeta`ファイルをこのパスに書き込みます。

{{< copyable "" >}}

```shell
br backup db \
    --pd "${PDIP}:2379" \
    --db test \
    --storage "local:///tmp/backup" \
    --ratelimit 128 \
    --log-file backupdb.log
```

上記のコマンドで、 `--db`はバックアップするデータベースの名前を指定します。その他のオプションの説明については、 [すべてのクラスター データをバックアップする](#use-br-command-line-to-back-up-cluster-data)を参照してください。

バックアップ中はターミナルに進行状況バーが表示されます。プログレス バーが 100% まで進むと、バックアップは完了です。次に、 BRはバックアップ データもチェックして、データの安全性を確保します。

### テーブルをバックアップする {#back-up-a-table}

クラスタ内の単一のテーブルのデータをバックアップするには、 `br backup table`コマンドを実行します。このコマンドのヘルプを表示するには、 `br backup table -h`または`br backup table --help`を実行します。

**使用例:**

`test.usertable`テーブルのデータを各 TiKV ノードの`/tmp/backup`パスにバックアップし、 `backupmeta`ファイルをこのパスに書き込みます。

{{< copyable "" >}}

```shell
br backup table \
    --pd "${PDIP}:2379" \
    --db test \
    --table usertable \
    --storage "local:///tmp/backup" \
    --ratelimit 128 \
    --log-file backuptable.log
```

`table`サブコマンドには 2 つのオプションがあります。

-   `--db` : データベース名を指定します
-   `--table` : テーブル名を指定します。

その他のオプションの説明については、 [すべてのクラスター データをバックアップする](#use-br-command-line-to-back-up-cluster-data)を参照してください。

バックアップ操作中は、進行状況バーがターミナルに表示されます。プログレス バーが 100% まで進むと、バックアップは完了です。次に、 BRはバックアップ データもチェックして、データの安全性を確保します。

### テーブルフィルターでバックアップ {#back-up-with-table-filter}

より複雑な条件で複数のテーブルをバックアップするには、 `br backup full`コマンドを実行し、 `--filter`または`-f`で[テーブル フィルター](/table-filter.md)を指定します。

**使用例:**

次のコマンドは、フォーム`db*.tbl*`のすべてのテーブルのデータを各 TiKV ノードの`/tmp/backup`パスにバックアップし、 `backupmeta`ファイルをこのパスに書き込みます。

{{< copyable "" >}}

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --filter 'db*.tbl*' \
    --storage "local:///tmp/backup" \
    --ratelimit 128 \
    --log-file backupfull.log
```

### データを Amazon S3 バックエンドにバックアップする {#back-up-data-to-amazon-s3-backend}

データを`local`ストレージではなく Amazon S3 バックエンドにバックアップする場合は、 `storage`サブコマンドで S3 ストレージ パスを指定し、 BRノードと TiKV ノードが Amazon S3 にアクセスできるようにする必要があります。

[AWS 公式ドキュメント](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-bucket.html)を参照して、指定された`Region`で S3 `Bucket`を作成できます。また、別の[AWS 公式ドキュメント](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-folder.html)を参照して`Bucket`に`Folder`を作成することもできます。

> **ノート：**
>
> 1 つのバックアップを完了するには、通常、TiKV とBRは`s3:ListBucket` 、 `s3:PutObject` 、および`s3:AbortMultipartUpload`の最小権限を必要とします。

S3 バックエンドへのアクセス権限を持つアカウントの`SecretKey`と`AccessKey`をBRノードに渡します。ここでは、 `SecretKey`と`AccessKey`が環境変数として渡されます。次に、 BRを介して TiKV ノードに権限を渡します。

{{< copyable "" >}}

```shell
export AWS_ACCESS_KEY_ID=${AccessKey}
export AWS_SECRET_ACCESS_KEY=${SecretKey}
```

BRを使用してバックアップする場合は、パラメータ`--s3.region`と`--send-credentials-to-tikv`を明示的に指定します。 `--s3.region`は S3 が配置されている領域を示し、 `--send-credentials-to-tikv`は S3 へのアクセス権を TiKV ノードに渡すことを意味します。

{{< copyable "" >}}

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --storage "s3://${Bucket}/${Folder}" \
    --s3.region "${region}" \
    --send-credentials-to-tikv=true \
    --ratelimit 128 \
    --log-file backupfull.log
```

### 増分データのバックアップ {#back-up-incremental-data}

<Warning>この機能は現在実験的であり、本番環境での使用は推奨されていません。</Warning>

増分バックアップする場合は、**最後のバックアップのタイムスタンプ**を指定するだけで済みます`--lastbackupts` 。

増分バックアップには 2 つの制限があります。

-   増分バックアップは、以前の完全バックアップとは別のパスにある必要があります。
-   GC (ガベージ コレクション) セーフポイントは`lastbackupts`の前にある必要があります。

`(LAST_BACKUP_TS, current PD timestamp]`間の増分データをバックアップするには、次のコマンドを実行します。

{{< copyable "" >}}

```shell
br backup full\
    --pd ${PDIP}:2379 \
    --ratelimit 128 \
    -s local:///home/tidb/backupdata/incr \
    --lastbackupts ${LAST_BACKUP_TS}
```

最後のバックアップのタイムスタンプを取得するには、 `validate`コマンドを実行します。例えば：

{{< copyable "" >}}

```shell
LAST_BACKUP_TS=`br validate decode --field="end-version" -s local:///home/tidb/backupdata | tail -n1`
```

上記の例では、増分バックアップ データの場合、 BRは`(LAST_BACKUP_TS, current PD timestamp]`の間のデータ変更と DDL 操作を記録します。データを復元するとき、 BRは最初に DDL 操作を復元し、次にデータを復元します。

### バックアップ中にデータを暗号化する (実験的機能) {#encrypt-data-during-backup-experimental-feature}

TiDB v5.3.0 以降、TiDB はバックアップの暗号化をサポートしています。次のパラメータを構成して、バックアップ中にデータを暗号化できます。

-   `--crypter.method` : 暗号化アルゴリズム。 3 つのアルゴリズムをサポート`aes128-ctr/aes192-ctr/aes256-ctr` 。デフォルト値は`plaintext`で、暗号化なしを示します。
-   `--crypter.key` : 16 進文字列形式の暗号化キー。 `aes128-ctr`は 128 ビット (16 バイト) のキー長を意味し、 `aes192-ctr`は 24 バイトを意味し、 `aes256-ctr`は 32 バイトを意味します。
-   `--crypter.key-file` : 鍵ファイル。 「crypter.key」を渡さずに、キーが保存されているファイルパスをパラメーターとして直接渡すことができます

> **警告：**
>
> -   これはまだ実験的機能です。本番環境で使用することはお勧めし**ません**。
> -   キーを紛失すると、バックアップ データをクラスタに復元できなくなります。
> -   暗号化機能は、 BRツールおよび TiDB クラスター v5.3.0 以降のバージョンで使用する必要があり、暗号化されたバックアップ データは、v5.3.0 より前のクラスターでは復元できません。

バックアップ暗号化の構成例は次のとおりです。

{{< copyable "" >}}

```shell
br backup full\
    --pd ${PDIP}:2379 \
    -s local:///home/tidb/backupdata/incr \
    --crypter.method aes128-ctr \
    --crypter.key 0123456789abcdef0123456789abcdef
```

### Raw KV のバックアップ (実験的機能) {#back-up-raw-kv-experimental-feature}

> **警告：**
>
> この機能は実験的であり、十分にテストされていません。この機能を本番環境で使用することは強く**お勧め**しません。

一部のシナリオでは、TiKV は TiDB とは独立して実行される場合があります。そのため、 BRは TiDBレイヤーのバイパスと TiKV でのデータのバックアップもサポートしています。

たとえば、次のコマンドを実行して、デフォルト CF の`[0x31, 0x3130303030303030)`から`$BACKUP_DIR`までのすべてのキーをバックアップできます。

{{< copyable "" >}}

```shell
br backup raw --pd $PD_ADDR \
    -s "local://$BACKUP_DIR" \
    --start 31 \
    --ratelimit 128 \
    --end 3130303030303030 \
    --format hex \
    --cf default
```

ここで、 `--start`と`--end`のパラメータは、TiKV に送信される前に`--format`で指定された方法を使用してデコードされます。現在、次の方法が利用可能です。

-   &quot;raw&quot;: 入力文字列はバイナリ形式のキーとして直接エンコードされます。
-   &quot;hex&quot;: デフォルトのエンコード方法。入力文字列は 16 進数として扱われます。
-   &quot;escape&quot;: 最初に入力文字列をエスケープしてから、バイナリ形式にエンコードします。

## BRコマンドラインを使用してクラスター データを復元する {#use-br-command-line-to-restore-cluster-data}

クラスター データを復元するには、 `br restore`コマンドを使用します。 `full` 、 `db`または`table`サブコマンドを追加して、復元の範囲 (クラスター全体、データベース、または単一のテーブル) を指定できます。

> **ノート：**
>
> ローカル ストレージを使用する場合は、すべてのバックアップ SST ファイルを`--storage`で指定されたパス内のすべての TiKV ノードにコピーする**必要**があります。
>
> 各 TiKV ノードが最終的にすべての SST ファイルの一部のみを読み取る必要がある場合でも、次の理由により、すべてのノードが完全なアーカイブへのフル アクセスを必要とします。
>
> -   データは複数のピアに複製されます。 SST を取り込む場合、これらのファイルは*すべての*ピアに存在する必要があります。これは、単一ノードからの読み取りで十分なバックアップとは異なります。
> -   復元中に各ピアが分散する場所はランダムです。どのノードがどのファイルを読み取るかは事前にわかりません。
>
> これらは、ローカル パスに NFS をマウントする、または S3 を使用するなど、共有ストレージを使用することで回避できます。ネットワーク ストレージを使用すると、すべてのノードがすべての SST ファイルを自動的に読み取ることができるため、これらの警告は適用されなくなります。
>
> また、1 つのクラスターに対して同時に実行できる復元操作は 1 つだけであることに注意してください。そうしないと、予期しない動作が発生する可能性があります。詳細については、 [FAQ](/br/backup-and-restore-faq.md#can-i-use-multiple-br-processes-at-the-same-time-to-restore-the-data-of-a-single-cluster)を参照してください。

### すべてのバックアップ データを復元する {#restore-all-the-backup-data}

すべてのバックアップ データをクラスターに復元するには、 `br restore full`コマンドを実行します。このコマンドのヘルプを表示するには、 `br restore full -h`または`br restore full --help`を実行します。

**使用例:**

`/tmp/backup`パスのすべてのバックアップ データをクラスターに復元します。

{{< copyable "" >}}

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --storage "local:///tmp/backup" \
    --ratelimit 128 \
    --log-file restorefull.log
```

上記のコマンドのいくつかのオプションの説明は次のとおりです。

-   `--ratelimit` : 各 TiKV ノードで復元操作が実行される最大速度 (MiB/秒) を指定します。
-   `--log-file` : BRログを`restorefull.log`ファイルに書き込むことを指定します。

復元中はターミナルに進行状況バーが表示されます。プログレス バーが 100% まで進むと、復元は完了です。次に、 BRはバックアップ データもチェックして、データの安全性を確保します。

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --storage "local:///tmp/backup" \
    --ratelimit 128 \
    --log-file restorefull.log
Full Restore <---------/...............................................> 17.12%.
```

### データベースを復元する {#restore-a-database}

データベースをクラスターに復元するには、 `br restore db`コマンドを実行します。このコマンドのヘルプを表示するには、 `br restore db -h`または`br restore db --help`を実行します。

**使用例:**

`/tmp/backup`パスにバックアップされたデータベースをクラスターに復元します。

{{< copyable "" >}}

```shell
br restore db \
    --pd "${PDIP}:2379" \
    --db "test" \
    --ratelimit 128 \
    --storage "local:///tmp/backup" \
    --log-file restoredb.log
```

上記のコマンドで、 `--db`は復元するデータベースの名前を指定します。その他のオプションの説明については、 [すべてのバックアップ データを復元する](#restore-all-the-backup-data) ) を参照してください。

> **ノート：**
>
> バックアップデータを復元する場合、 `--db`で指定するデータベースの名前は、バックアップコマンドの`-- db`で指定するデータベースの名前と同じでなければなりません。そうしないと、復元は失敗します。これは、バックアップ データのメタファイル ( `backupmeta`ファイル) にデータベース名が記録されているためです。同じ名前のデータベースにしかデータを復元できません。推奨される方法は、バックアップ データを別のクラスター内の同じ名前のデータベースに復元することです。

### テーブルを復元する {#restore-a-table}

1 つのテーブルをクラスターに復元するには、 `br restore table`コマンドを実行します。このコマンドのヘルプを表示するには、 `br restore table -h`または`br restore table --help`を実行します。

**使用例:**

`/tmp/backup`パスにバックアップされたテーブルをクラスターに復元します。

{{< copyable "" >}}

```shell
br restore table \
    --pd "${PDIP}:2379" \
    --db "test" \
    --table "usertable" \
    --ratelimit 128 \
    --storage "local:///tmp/backup" \
    --log-file restoretable.log
```

上記のコマンドで、 `--table`は復元するテーブルの名前を指定します。その他のオプションの説明については、 [すべてのバックアップ データを復元する](#restore-all-the-backup-data)および[データベースを復元する](#restore-a-database)を参照してください。

### テーブルフィルターで復元 {#restore-with-table-filter}

より複雑な条件で複数のテーブルを復元するには、 `br restore full`コマンドを実行し、 `--filter`または`-f`で[テーブル フィルター](/table-filter.md)を指定します。

**使用例:**

次のコマンドは、 `/tmp/backup`パスでバックアップされたテーブルのサブセットをクラスターに復元します。

{{< copyable "" >}}

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --filter 'db*.tbl*' \
    --storage "local:///tmp/backup" \
    --log-file restorefull.log
```

### Amazon S3 バックエンドからデータを復元する {#restore-data-from-amazon-s3-backend}

`local`のストレージではなく Amazon S3 バックエンドからデータを復元する場合は、 `storage`サブコマンドで S3 ストレージ パスを指定し、 BRノードと TiKV ノードが Amazon S3 にアクセスできるようにする必要があります。

> **ノート：**
>
> 1 回の復元を完了するには、通常、TiKV とBRは`s3:ListBucket`と`s3:GetObject`の最小権限が必要です。

S3 バックエンドへのアクセス権限を持つアカウントの`SecretKey`と`AccessKey`をBRノードに渡します。ここでは、 `SecretKey`と`AccessKey`が環境変数として渡されます。次に、 BRを介して TiKV ノードに権限を渡します。

{{< copyable "" >}}

```shell
export AWS_ACCESS_KEY_ID=${AccessKey}
export AWS_SECRET_ACCESS_KEY=${SecretKey}
```

BRを使用してデータを復元する場合は、パラメータ`--s3.region`と`--send-credentials-to-tikv`を明示的に指定します。 `--s3.region`は S3 が配置されている領域を示し、 `--send-credentials-to-tikv`は S3 へのアクセス権を TiKV ノードに渡すことを意味します。

パラメータ`--storage`の`Bucket`と`Folder`は、S3 バケットと、復元するデータが配置されているフォルダを表します。

{{< copyable "" >}}

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --storage "s3://${Bucket}/${Folder}" \
    --s3.region "${region}" \
    --ratelimit 128 \
    --send-credentials-to-tikv=true \
    --log-file restorefull.log
```

上記のコマンドで、 `--table`は復元するテーブルの名前を指定します。その他のオプションの説明については、 [データベースを復元する](#restore-a-database)を参照してください。

### 増分データの復元 {#restore-incremental-data}

<Warning>この機能は現在実験的であり、本番環境での使用は推奨されていません。</Warning>

増分データの復元は[BRを使用して完全なデータを復元する](#restore-all-the-backup-data)に似ています。増分データを復元する場合は、 `last backup ts`より前にバックアップされたすべてのデータがターゲット クラスターに復元されていることを確認してください。

### <code>mysql</code>スキーマで作成されたテーブルを復元する (実験的機能) {#restore-tables-created-in-the-code-mysql-code-schema-experimental-feature}

BRは、デフォルトで`mysql`スキーマで作成されたテーブルをバックアップします。

BRを使用してデータを復元する場合、 `mysql`スキーマで作成されたテーブルはデフォルトでは復元されません。これらのテーブルを復元する必要がある場合は、 [テーブル フィルター](/table-filter.md#syntax)を使用して明示的に含めることができます。次の例では、 `mysql`スキーマで作成された`mysql.usertable`を復元します。このコマンドは、他のデータとともに`mysql.usertable`を復元します。

{{< copyable "" >}}

```shell
br restore full -f '*.*' -f '!mysql.*' -f 'mysql.usertable' -s $external_storage_url --ratelimit 128
```

上記のコマンドでは、 `-f '*.*'`はデフォルト ルールをオーバーライドするために使用され、 `-f '!mysql.*'`は特に明記されていない限り`mysql`でテーブルを復元しないようにBRに指示します。 `-f 'mysql.usertable'`は、復元に`mysql.usertable`が必要であることを示します。詳細な実装については、 [テーブル フィルター ドキュメント](/table-filter.md#syntax)を参照してください。

`mysql.usertable`のみを復元する必要がある場合は、次のコマンドを使用します。

{{< copyable "" >}}

```shell
br restore full -f 'mysql.usertable' -s $external_storage_url --ratelimit 128
```

> **警告：**
>
> BRツールを使用してシステム テーブル ( `mysql.tidb`など) をバックアップできますが、 `--filter`設定を使用して復元を実行しても、 BRは次のシステム テーブルを無視します。
>
> -   統計情報表 ( `mysql.stat_*` )
> -   システム変数テーブル ( `mysql.tidb` ， `mysql.global_variables` )
> -   ユーザー情報テーブル ( `mysql.user`や`mysql.columns_priv`など)
> -   [その他のシステム テーブル](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/restore/systable_restore.go#L31)

### 復元中にデータを復号化する (実験的機能) {#decrypt-data-during-restore-experimental-feature}

> **警告：**
>
> これはまだ実験的機能です。本番環境で使用することはお勧めし**ません**。

バックアップ データを暗号化したら、対応する復号化パラメータを渡してデータを復元する必要があります。復号化パラメーターと暗号化パラメーターが一貫していることを確認する必要があります。復号化アルゴリズムまたはキーが正しくない場合、データは復元できません。

以下は、バックアップ データの復号化の例です。

{{< copyable "" >}}

```shell
br restore full\
    --pd ${PDIP}:2379 \
    -s local:///home/tidb/backupdata/incr \
    --crypter.method aes128-ctr \
    --crypter.key 0123456789abcdef0123456789abcdef
```

### Raw KV の復元 (実験的機能) {#restore-raw-kv-experimental-feature}

> **警告：**
>
> この機能は実験段階であり、完全にはテストされていません。この機能を本番環境で使用することは強く**お勧め**しません。

[Raw KV のバックアップ](#back-up-raw-kv-experimental-feature)と同様に、次のコマンドを実行して Raw KV を復元できます。

{{< copyable "" >}}

```shell
br restore raw --pd $PD_ADDR \
    -s "local://$BACKUP_DIR" \
    --start 31 \
    --end 3130303030303030 \
    --ratelimit 128 \
    --format hex \
    --cf default
```

上記の例では、範囲`[0x31, 0x3130303030303030)`のバックアップされたすべてのキーが TiKV クラスターに復元されます。これらのキーのコーディング方法は、 [バックアップ プロセス中のキー](#back-up-raw-kv-experimental-feature)の方法と同じです。

### オンライン復元 (実験的機能) {#online-restore-experimental-feature}

> **警告：**
>
> この機能は実験段階であり、完全にはテストされていません。また、PD の不安定な`Placement Rules`機能にも依存しています。この機能を本番環境で使用することは強く**お勧め**しません。

データの復元中に書き込みすぎるデータは、オンライン クラスターのパフォーマンスに影響します。この影響をできるだけ回避するために、 BRは[配置ルール](/configure-placement-rules.md)をサポートしてリソースを分離します。この場合、SST のダウンロードとインポートは、指定されたいくつかのノード (または略して「ノードの復元」) でのみ実行されます。オンライン復元を完了するには、次の手順を実行します。

1.  PD を構成し、配置ルールを開始します。

    {{< copyable "" >}}

    ```shell
    echo "config set enable-placement-rules true" | pd-ctl
    ```

2.  TiKV で「復元ノード」の構成ファイルを編集し、 `server`の構成項目に「復元」を指定します。

    {{< copyable "" >}}

    ```
    [server]
    labels = { exclusive = "restore" }
    ```

3.  「リストア ノード」の TiKV を起動し、バックアップしたファイルをBRを使用してリストアします。オフライン リストアと比較して、 `--online`のフラグを追加するだけで済みます。

    {{< copyable "" >}}

    ```
    br restore full \
        -s "local://$BACKUP_DIR" \
        --ratelimit 128 \
        --pd $PD_ADDR \
        --online
    ```
