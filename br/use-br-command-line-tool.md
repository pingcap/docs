---
title: Use BR Command-line for Backup and Restoration
summary: Learn how to use the BR command line to backup and restore cluster data.
---

# バックアップと復元にBRコマンドラインを使用する {#use-br-command-line-for-backup-and-restoration}

このドキュメントでは、BRコマンドラインを使用してTiDBクラスタデータをバックアップおよび復元する方法について説明します。

[BRツールの概要](/br/backup-and-restore-tool.md) 、特に[使用制限](/br/backup-and-restore-tool.md#usage-restrictions)と[ベストプラクティス](/br/backup-and-restore-tool.md#best-practices)を読んだことを確認してください。

## BRコマンドラインの説明 {#br-command-line-description}

`br`コマンドは、サブコマンド、オプション、およびパラメーターで構成されます。

-   サブコマンド： `-`または`--`のない文字。
-   オプション： `-`または`--`で始まる文字。
-   パラメーター：直後に続き、サブコマンドまたはオプションに渡される文字。

これは完全な`br`のコマンドです。

{{< copyable "" >}}

```shell
br backup full --pd "${PDIP}:2379" -s "local:///tmp/backup"
```

上記のコマンドの説明は次のとおりです。

-   `backup` ： `br`のサブコマンド。
-   `full` ： `backup`のサブコマンド。
-   `-s` （または`--storage` ）：バックアップファイルが保存されるパスを指定するオプション。
-   `"local:///tmp/backup"` ： `-s`のパラメータ。 `/tmp/backup`は、各TiKVノードのバックアップファイルが保存されているローカルディスク内のパスです。
-   `--pd` ：配置ドライバー（PD）サービスアドレスを指定するオプション。
-   `"${PDIP}:2379"` ： `--pd`のパラメータ。

> **ノート：**
>
> -   `local`のストレージを使用すると、バックアップデータは各ノードのローカルファイルシステムに分散されます。
>
> -   データの復元を完了するには、これらのデータを手動で集約する必要**が**あるため、実稼働環境でローカルディスクにバックアップすることは<strong>お勧め</strong>しません。詳細については、 [クラスターデータの復元](#use-br-command-line-to-restore-cluster-data)を参照してください。
>
> -   これらのバックアップデータを集約すると、冗長性が生じ、運用や保守に支障をきたす可能性があります。さらに悪いことに、これらのデータを集約せずにデータを復元すると、かなり紛らわしいエラーメッセージ`SST file not found`を受け取る可能性があります。
>
> -   各ノードにNFSディスクをマウントするか、 `S3`のオブジェクトストレージにバックアップすることをお勧めします。

### サブコマンド {#sub-commands}

`br`のコマンドは、サブコマンドの複数のレイヤーで構成されます。現在、BRには次の3つのサブコマンドがあります。

-   `br backup` ：TiDBクラスタのデータをバックアップするために使用されます。
-   `br restore` ：TiDBクラスタのデータを復元するために使用されます。

上記の3つのサブコマンドのそれぞれに、操作の範囲を指定するための次の3つのサブコマンドが含まれている場合があります。

-   `full` ：すべてのクラスタデータをバックアップまたは復元するために使用されます。
-   `db` ：クラスタの指定されたデータベースをバックアップまたは復元するために使用されます。
-   `table` ：クラスタの指定されたデータベース内の単一のテーブルをバックアップまたは復元するために使用されます。

### 一般的なオプション {#common-options}

-   `--pd` ：接続に使用され、PDサーバーアドレスを指定します。たとえば、 `"${PDIP}:2379"` 。
-   `-h` （または`--help` ）：すべてのサブコマンドのヘルプを取得するために使用されます。たとえば、 `br backup --help` 。
-   `-V` （または`--version` ）：BRのバージョンを確認するために使用されます。
-   `--ca` ：信頼できるCA証明書へのパスをPEM形式で指定します。
-   `--cert` ：SSL証明書へのパスをPEM形式で指定します。
-   `--key` ：SSL証明書キーへのパスをPEM形式で指定します。
-   `--status-addr` ：BRがPrometheusに統計を提供するためのリスニングアドレスを指定します。

## BRコマンドラインを使用してクラスタデータをバックアップする {#use-br-command-line-to-back-up-cluster-data}

クラスタデータをバックアップするには、 `br backup`コマンドを使用します。 `full`または`table`サブコマンドを追加して、バックアップ操作の範囲（クラスタ全体または単一のテーブル）を指定できます。

### すべてのクラスタデータをバックアップします {#back-up-all-the-cluster-data}

すべてのクラスタデータをバックアップするには、 `br backup full`コマンドを実行します。このコマンドのヘルプを表示するには、 `br backup full -h`または`br backup full --help`を実行します。

**使用例：**

すべてのクラスタデータを各TiKVノードの`/tmp/backup`のパスにバックアップし、このパスに`backupmeta`のファイルを書き込みます。

> **ノート：**
>
> -   バックアップディスクとサービスディスクが異なる場合、フルスピードバックアップの場合、オンラインバックアップによって読み取り専用オンラインサービスのQPSが約15％〜25％低下することがテストされています。 QPSへの影響を減らしたい場合は、 `--ratelimit`を使用してレートを制限します。
>
> -   バックアップディスクとサービスディスクが同じである場合、バックアップはI/Oリソースを求めてサービスと競合します。これにより、読み取り専用オンラインサービスのQPSが半分以上低下する可能性があります。したがって、オンラインサービスデータをTiKVデータディスクにバックアップすることは**強くお勧め**しません。

{{< copyable "" >}}

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --storage "local:///tmp/backup" \
    --ratelimit 128 \
    --log-file backupfull.log
```

上記のコマンドのいくつかのオプションの説明は次のとおりです。

-   `--ratelimit` ：各TiKVノードでバックアップ操作が実行される最大速度（MiB / s）を指定します。
-   `--log-file` ：BRログを`backupfull.log`ファイルに書き込むことを指定します。

バックアップ中は、端末にプログレスバーが表示されます。プログレスバーが100％に進むと、バックアップが完了します。次に、BRはバックアップデータもチェックして、データの安全性を確保します。プログレスバーは次のように表示されます。

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --storage "local:///tmp/backup" \
    --ratelimit 128 \
    --log-file backupfull.log
Full Backup <---------/................................................> 17.12%.
```

### データベースをバックアップする {#back-up-a-database}

クラスタのデータベースをバックアップするには、 `br backup db`コマンドを実行します。このコマンドのヘルプを表示するには、 `br backup db -h`または`br backup db --help`を実行します。

**使用例：**

`test`のデータベースのデータを各TiKVノードの`/tmp/backup`のパスにバックアップし、 `backupmeta`のファイルをこのパスに書き込みます。

{{< copyable "" >}}

```shell
br backup db \
    --pd "${PDIP}:2379" \
    --db test \
    --storage "local:///tmp/backup" \
    --ratelimit 128 \
    --log-file backupdb.log
```

上記のコマンドで、 `--db`はバックアップするデータベースの名前を指定します。その他のオプションの説明については、 [すべてのクラスタデータをバックアップします](#use-br-command-line-to-back-up-cluster-data)を参照してください。

バックアップ中は、端末にプログレスバーが表示されます。プログレスバーが100％に進むと、バックアップが完了します。次に、BRはバックアップデータもチェックして、データの安全性を確保します。

### テーブルをバックアップする {#back-up-a-table}

クラスタの単一のテーブルのデータをバックアップするには、 `br backup table`コマンドを実行します。このコマンドのヘルプを表示するには、 `br backup table -h`または`br backup table --help`を実行します。

**使用例：**

`test.usertable`のテーブルのデータを各TiKVノードの`/tmp/backup`のパスにバックアップし、 `backupmeta`のファイルをこのパスに書き込みます。

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

`table`サブコマンドには2つのオプションがあります。

-   `--db` ：データベース名を指定します
-   `--table` ：テーブル名を指定します。

その他のオプションの説明については、 [すべてのクラスタデータをバックアップします](#use-br-command-line-to-back-up-cluster-data)を参照してください。

バックアップ操作中は、端末にプログレスバーが表示されます。プログレスバーが100％に進むと、バックアップが完了します。次に、BRはバックアップデータもチェックして、データの安全性を確保します。

### テーブルフィルターでバックアップする {#back-up-with-table-filter}

より複雑な基準で複数のテーブルをバックアップするには、 `br backup full`コマンドを実行し、 `--filter`または`-f`で[テーブルフィルター](/table-filter.md)を指定します。

**使用例：**

次のコマンドは、フォーム`db*.tbl*`のすべてのテーブルのデータを各TiKVノードの`/tmp/backup`パスにバックアップし、 `backupmeta`ファイルをこのパスに書き込みます。

{{< copyable "" >}}

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --filter 'db*.tbl*' \
    --storage "local:///tmp/backup" \
    --ratelimit 128 \
    --log-file backupfull.log
```

### データをAmazonS3バックエンドにバックアップします {#back-up-data-to-amazon-s3-backend}

データを`local`のストレージではなくAmazonS3バックエンドにバックアップする場合は、 `storage`サブコマンドでS3ストレージパスを指定し、BRノードとTiKVノードがAmazonS3にアクセスできるようにする必要があります。

[AWS公式ドキュメント](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-bucket.html)を参照して、指定した`Bucket`にS33を作成でき`Region` 。別の[AWS公式ドキュメント](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-folder.html)を参照して、 `Bucket`に`Folder`を作成することもできます。

> **ノート：**
>
> 1つのバックアップを完了するには、TiKVとBRは通常、 `s3:ListBucket` 、および`s3:PutObject`の最小特権を必要とし`s3:AbortMultipartUpload` 。

S3バックエンドにアクセスする権限を持つアカウントの`SecretKey`と`AccessKey`をBRノードに渡します。ここでは、 `SecretKey`と`AccessKey`が環境変数として渡されます。次に、BRを介して特権をTiKVノードに渡します。

{{< copyable "" >}}

```shell
export AWS_ACCESS_KEY_ID=${AccessKey}
export AWS_SECRET_ACCESS_KEY=${SecretKey}
```

BRを使用してバックアップする場合は、パラメーター`--s3.region`と`--send-credentials-to-tikv`を明示的に指定してください。 `--s3.region`はS3が配置されているリージョンを示し、 `--send-credentials-to-tikv`はS3にアクセスする特権をTiKVノードに渡すことを意味します。

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

### インクリメンタルデータをバックアップする {#back-up-incremental-data}

増分バックアップする場合は、**最後のバックアップタイムスタンプ**`--lastbackupts`を指定するだけで済みます。

増分バックアップには2つの制限があります。

-   増分バックアップは、前の完全バックアップとは異なるパスの下にある必要があります。
-   GC（ガベージコレクション）セーフポイントは、 `lastbackupts`の前にある必要があります。

`(LAST_BACKUP_TS, current PD timestamp]`の間の増分データをバックアップするには、次のコマンドを実行します。

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

上記の例では、増分バックアップデータの場合、BRは`(LAST_BACKUP_TS, current PD timestamp]`の間のデータ変更とDDL操作を記録します。データを復元する場合、BRは最初にDDL操作を復元し、次にデータを復元します。

### バックアップ中にデータを暗号化する（実験的機能） {#encrypt-data-during-backup-experimental-feature}

TiDB v5.3.0以降、TiDBはバックアップ暗号化をサポートしています。バックアップ中にデータを暗号化するには、次のパラメーターを構成できます。

-   `--crypter.method` ：暗号化アルゴリズム。 3つのアルゴリズムをサポートします`aes128-ctr/aes192-ctr/aes256-ctr` 。デフォルト値は`plaintext`で、暗号化されていないことを示します。
-   `--crypter.key`進文字列形式の暗号化キー。 `aes128-ctr`は128ビット（16バイト）のキー長を意味し、 `aes192-ctr`は24バイトを意味し、 `aes256-ctr`は32バイトを意味します。
-   `--crypter.key-file` ：キーファイル。 「crypter.key」を渡さなくても、キーがパラメータとして保存されているファイルパスを直接渡すことができます。

> **警告：**
>
> -   これはまだ実験的機能です。実稼働環境で使用することはお勧めし**ません**。
> -   キーを紛失した場合、バックアップデータをクラスタに復元できません。
> -   暗号化機能は、BRツールおよびTiDBクラスターv5.3.0以降のバージョンで使用する必要があり、暗号化されたバックアップデータはv5.3.0より前のクラスターでは復元できません。

バックアップ暗号化の設定例は次のとおりです。

{{< copyable "" >}}

```shell
br backup full\
    --pd ${PDIP}:2379 \
    -s local:///home/tidb/backupdata/incr \
    --crypter.method aes128-ctr \
    --crypter.key 0123456789abcdef0123456789abcdef
```

### Raw KVのバックアップ（実験的機能） {#back-up-raw-kv-experimental-feature}

> **警告：**
>
> この機能は実験的であり、完全にはテストされていません。この機能を実稼働環境で使用することは強く**お勧め**しません。

一部のシナリオでは、TiKVはTiDBとは独立して実行される場合があります。そのため、BRはTiDBレイヤーのバイパスとTiKVでのデータのバックアップもサポートしています。

たとえば、次のコマンドを実行して、デフォルトCFの`[0x31, 0x3130303030303030)`から`$BACKUP_DIR`までのすべてのキーをバックアップできます。

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

ここで、 `--start`と`--end`のパラメータは、TiKVに送信される前に、 `--format`で指定された方法を使用してデコードされます。現在、次の方法を使用できます。

-   &quot;raw&quot;：入力文字列はバイナリ形式のキーとして直接エンコードされます。
-   「hex」：デフォルトのエンコード方法。入力文字列は16進数として扱われます。
-   「エスケープ」：最初に入力文字列をエスケープしてから、バイナリ形式にエンコードします。

## BRコマンドラインを使用してクラスタデータを復元する {#use-br-command-line-to-restore-cluster-data}

クラスタデータを復元するには、 `br restore`コマンドを使用します。 `full` 、または`db`サブコマンドを追加して、復元の範囲（クラスタ全体、データベース、または単一のテーブル）を指定でき`table` 。

> **ノート：**
>
> ローカルストレージを使用する場合は、すべてのバックアップSSTファイルを`--storage`で指定されたパスのすべてのTiKVノードにコピーする**必要**があります。
>
> 各TiKVノードが最終的にすべてのSSTファイルの一部を読み取るだけでよい場合でも、次の理由により、すべてのTiKVノードが完全なアーカイブへのフルアクセスを必要とします。
>
> -   データは複数のピアに複製されます。 SSTを取り込む場合、これらのファイルは*すべての*ピアに存在する必要があります。これは、単一ノードからの読み取りで十分なバックアップとは異なります。
> -   復元中に各ピアが分散する場所はランダムです。どのノードがどのファイルを読み取るかは事前にわかりません。
>
> これらは、共有ストレージを使用して回避できます。たとえば、ローカルパスにNFSをマウントしたり、S3を使用したりできます。ネットワークストレージを使用すると、すべてのノードがすべてのSSTファイルを自動的に読み取ることができるため、これらの警告は適用されなくなります。
>
> また、1つのクラスタに対して同時に実行できる復元操作は1つだけであることに注意してください。そうしないと、予期しない動作が発生する可能性があります。詳細については、 [FAQ](/br/backup-and-restore-faq.md#can-i-use-multiple-br-processes-at-the-same-time-to-restore-the-data-of-a-single-cluster)を参照してください。

### すべてのバックアップデータを復元する {#restore-all-the-backup-data}

すべてのバックアップデータをクラスタに復元するには、 `br restore full`コマンドを実行します。このコマンドのヘルプを表示するには、 `br restore full -h`または`br restore full --help`を実行します。

**使用例：**

クラスタへの`/tmp/backup`のパスにあるすべてのバックアップデータを復元します。

{{< copyable "" >}}

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --storage "local:///tmp/backup" \
    --ratelimit 128 \
    --log-file restorefull.log
```

上記のコマンドのいくつかのオプションの説明は次のとおりです。

-   `--ratelimit` ：各TiKVノードで復元操作が実行される最大速度（MiB / s）を指定します。
-   `--log-file` ：BRログを`restorefull.log`ファイルに書き込むことを指定します。

復元中は、ターミナルにプログレスバーが表示されます。プログレスバーが100％に進むと、復元が完了します。次に、BRはバックアップデータもチェックして、データの安全性を確保します。

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --storage "local:///tmp/backup" \
    --ratelimit 128 \
    --log-file restorefull.log
Full Restore <---------/...............................................> 17.12%.
```

### データベースを復元する {#restore-a-database}

データベースをクラスタに復元するには、 `br restore db`コマンドを実行します。このコマンドのヘルプを表示するには、 `br restore db -h`または`br restore db --help`を実行します。

**使用例：**

クラスタへの`/tmp/backup`のパスでバックアップされたデータベースを復元します。

{{< copyable "" >}}

```shell
br restore db \
    --pd "${PDIP}:2379" \
    --db "test" \
    --ratelimit 128 \
    --storage "local:///tmp/backup" \
    --log-file restoredb.log
```

上記のコマンドで、 `--db`は復元するデータベースの名前を指定します。その他のオプションの説明については、 [すべてのバックアップデータを復元する](#restore-all-the-backup-data) ）を参照してください。

> **ノート：**
>
> バックアップデータを復元する場合、 `--db`で指定されたデータベースの名前は、backupコマンドで`-- db`で指定された名前と同じである必要があります。それ以外の場合、復元は失敗します。これは、バックアップデータのメタファイル（ `backupmeta`ファイル）にデータベース名が記録されているため、同じ名前のデータベースにしかデータを復元できないためです。推奨される方法は、バックアップデータを別のクラスタの同じ名前のデータベースに復元することです。

### テーブルを復元する {#restore-a-table}

単一のテーブルをクラスタに復元するには、 `br restore table`コマンドを実行します。このコマンドのヘルプを表示するには、 `br restore table -h`または`br restore table --help`を実行します。

**使用例：**

クラスタへの`/tmp/backup`のパスでバックアップされたテーブルを復元します。

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

上記のコマンドで、 `--table`は復元するテーブルの名前を指定します。その他のオプションの説明については、 [すべてのバックアップデータを復元する](#restore-all-the-backup-data)および[データベースを復元する](#restore-a-database)を参照してください。

### テーブルフィルターで復元 {#restore-with-table-filter}

より複雑な基準で複数のテーブルを復元するには、 `br restore full`コマンドを実行し、 `--filter`または`-f`で[テーブルフィルター](/table-filter.md)を指定します。

**使用例：**

次のコマンドは、クラスタへの`/tmp/backup`のパスでバックアップされたテーブルのサブセットを復元します。

{{< copyable "" >}}

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --filter 'db*.tbl*' \
    --storage "local:///tmp/backup" \
    --log-file restorefull.log
```

### AmazonS3バックエンドからデータを復元する {#restore-data-from-amazon-s3-backend}

`local`のストレージではなくAmazonS3バックエンドからデータを復元する場合は、 `storage`サブコマンドでS3ストレージパスを指定し、BRノードとTiKVノードがAmazonS3にアクセスできるようにする必要があります。

> **ノート：**
>
> 1つの復元を完了するには、通常、TiKVとBRに`s3:ListBucket`と`s3:GetObject`の最小特権が必要です。

S3バックエンドにアクセスする権限を持つアカウントの`SecretKey`と`AccessKey`をBRノードに渡します。ここでは、 `SecretKey`と`AccessKey`が環境変数として渡されます。次に、BRを介して特権をTiKVノードに渡します。

{{< copyable "" >}}

```shell
export AWS_ACCESS_KEY_ID=${AccessKey}
export AWS_SECRET_ACCESS_KEY=${SecretKey}
```

BRを使用してデータを復元する場合は、パラメータ`--s3.region`と`--send-credentials-to-tikv`を明示的に指定してください。 `--s3.region`はS3が配置されているリージョンを示し、 `--send-credentials-to-tikv`はS3にアクセスする特権をTiKVノードに渡すことを意味します。

`--storage`パラメーターの`Bucket`と`Folder`は、S3バケットと、復元するデータが配置されているフォルダーを表します。

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

### 増分データを復元する {#restore-incremental-data}

インクリメンタルデータの復元は[BRを使用して完全なデータを復元する](#restore-all-the-backup-data)に似ています。インクリメンタルデータを復元するときは、 `last backup ts`より前にバックアップされたすべてのデータがターゲットクラスタに復元されていることを確認してください。

### <code>mysql</code>スキーマで作成されたテーブルを復元する（実験的機能） {#restore-tables-created-in-the-code-mysql-code-schema-experimental-feature}

BRは、デフォルトで`mysql`スキーマで作成されたテーブルをバックアップします。

BRを使用してデータを復元する場合、 `mysql`スキーマで作成されたテーブルはデフォルトでは復元されません。これらのテーブルを復元する必要がある場合は、 [テーブルフィルター](/table-filter.md#syntax)を使用して明示的に含めることができます。次の例では、 `mysql`スキーマで作成された`mysql.usertable`を復元します。このコマンドは、他のデータとともに`mysql.usertable`を復元します。

{{< copyable "" >}}

```shell
br restore full -f '*.*' -f '!mysql.*' -f 'mysql.usertable' -s $external_storage_url --ratelimit 128
```

上記のコマンドでは、 `-f '*.*'`はデフォルトのルールをオーバーライドするために使用され、 `-f '!mysql.*'`は特に明記されていない限り`mysql`のテーブルを復元しないようにBRに指示します。 `-f 'mysql.usertable'`は、復元に`mysql.usertable`が必要であることを示します。詳細な実装については、 [テーブルフィルタードキュメント](/table-filter.md#syntax)を参照してください。

`mysql.usertable`のみを復元する必要がある場合は、次のコマンドを使用します。

{{< copyable "" >}}

```shell
br restore full -f 'mysql.usertable' -s $external_storage_url --ratelimit 128
```

> **警告：**
>
> BRツールを使用してシステムテーブル（ `mysql.tidb`など）をバックアップできますが、復元を実行するために`--filter`設定を使用した場合でも、BRは次のシステムテーブルを無視します。
>
> -   統計情報表（ `mysql.stat_*` ）
> -   システム変数`mysql.global_variables` `mysql.tidb`
> -   ユーザー情報テーブル（ `mysql.user`や`mysql.columns_priv`など）
> -   [その他のシステムテーブル](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/restore/systable_restore.go#L31)

### 復元中にデータを復号化する（実験的機能） {#decrypt-data-during-restore-experimental-feature}

> **警告：**
>
> これはまだ実験的機能です。実稼働環境で使用することはお勧めし**ません**。

バックアップデータを暗号化した後、対応する復号化パラメータを渡してデータを復元する必要があります。復号化パラメーターと暗号化パラメーターが一貫していることを確認する必要があります。復号化アルゴリズムまたはキーが正しくない場合、データを復元できません。

以下は、バックアップデータを復号化する例です。

{{< copyable "" >}}

```shell
br restore full\
    --pd ${PDIP}:2379 \
    -s local:///home/tidb/backupdata/incr \
    --crypter.method aes128-ctr \
    --crypter.key 0123456789abcdef0123456789abcdef
```

### Raw KVの復元（実験的機能） {#restore-raw-kv-experimental-feature}

> **警告：**
>
> この機能は、徹底的にテストされていないが、実験中です。この機能を実稼働環境で使用することは強く**お勧め**しません。

[RawKVのバックアップ](#back-up-raw-kv-experimental-feature)と同様に、次のコマンドを実行してRawKVを復元できます。

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

上記の例では、範囲`[0x31, 0x3130303030303030)`のすべてのバックアップされたキーがTiKVクラスタに復元されます。これらのキーのコーディング方法は、 [バックアッププロセス中のキー](#back-up-raw-kv-experimental-feature)のコーディング方法と同じです。

### オンライン復元（実験的機能） {#online-restore-experimental-feature}

> **警告：**
>
> この機能は、徹底的にテストされていないが、実験中です。また、PDの不安定な`Placement Rules`機能に依存しています。この機能を実稼働環境で使用することは強く**お勧め**しません。

データの復元中に、書き込みが多すぎると、オンラインクラスタのパフォーマンスに影響します。この影響を可能な限り回避するために、BRはリソースを分離するために[配置ルール](/configure-placement-rules.md)をサポートします。この場合、SSTのダウンロードとインポートは、指定されたいくつかのノード（または略して「ノードの復元」）でのみ実行されます。オンライン復元を完了するには、次の手順を実行します。

1.  PDを構成し、配置ルールを開始します。

    {{< copyable "" >}}

    ```shell
    echo "config set enable-placement-rules true" | pd-ctl
    ```

2.  TiKVの「復元ノード」の設定ファイルを編集し、 `server`の設定項目に「復元」を指定します。

    {{< copyable "" >}}

    ```
    [server]
    labels = { exclusive = "restore" }
    ```

3.  「復元ノード」のTiKVを起動し、BRを使用してバックアップファイルを復元します。オフライン復元と比較すると、 `--online`のフラグを追加するだけで済みます。

    {{< copyable "" >}}

    ```
    br restore full \
        -s "local://$BACKUP_DIR" \
        --ratelimit 128 \
        --pd $PD_ADDR \
        --online
    ```
