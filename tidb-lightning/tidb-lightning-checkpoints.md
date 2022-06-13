---
title: TiDB Lightning Checkpoints
summary: Use checkpoints to avoid redoing the previously completed tasks before the crash.
---

# TiDBLightningチェックポイント {#tidb-lightning-checkpoints}

大規模なデータベースのインポートには通常、数時間または数日かかります。このような長時間実行されているプロセスが誤ってクラッシュした場合、以前に完了したタスクをやり直すのに非常に時間がかかる可能性があります。これを解決するために、TiDB Lightningは*チェックポイント*を使用してインポートの進行状況を保存し、 `tidb-lightning`が再起動後に中断したところからインポートを続行するようにします。

このドキュメントでは、*チェックポイント*を有効化、構成、保存、および制御する方法について説明します。

## チェックポイントを有効にして構成する {#enable-and-configure-checkpoints}

```toml
[checkpoint]
# Whether to enable checkpoints.
# While importing data, TiDB Lightning records which tables have been imported, so
# even if TiDB Lightning or some other component crashes, you can start from a known
# good state instead of restarting from scratch.
enable = true

# Where to store the checkpoints.
#  - file:  store as a local file (requires v2.1.1 or later)
#  - mysql: store into a remote MySQL-compatible database
driver = "file"

# The schema name (database name) to store the checkpoints
# Enabled only when `driver = "mysql"`.
# schema = "tidb_lightning_checkpoint"

# The data source name (DSN) indicating the location of the checkpoint storage.
#
# For the "file" driver, the DSN is a path. If the path is not specified, Lightning would
# default to "/tmp/CHECKPOINT_SCHEMA.pb".
#
# For the "mysql" driver, the DSN is a URL in the form of "USER:PASS@tcp(HOST:PORT)/".
# If the URL is not specified, the TiDB server from the [tidb] section is used to
# store the checkpoints. You should specify a different MySQL-compatible
# database server to reduce the load of the target TiDB cluster.
#dsn = "/tmp/tidb_lightning_checkpoint.pb"

# Whether to keep the checkpoints after all data are imported. If false, the
# checkpoints are deleted. Keeping the checkpoints can aid debugging but
# might leak metadata about the data source.
# keep-after-success = false
```

## チェックポイントストレージ {#checkpoints-storage}

TiDB Lightningは、ローカルファイルまたはリモートのMySQL互換データベースの2種類のチェックポイントストレージをサポートします。

-   `driver = "file"`の場合、チェックポイントは`dsn`設定で指定されたパスのローカルファイルに保存されます。チェックポイントは迅速に更新されるため、RAMディスクなどの書き込み耐久性が非常に高いドライブにチェックポイントファイルを配置することを強くお勧めします。

-   `driver = "mysql"`を使用すると、MariaDBやTiDBなど、MySQL5.7以降と互換性のある任意のデータベースにチェックポイントを保存できます。デフォルトでは、チェックポイントはターゲットデータベースに保存されます。

ターゲットデータベースをチェックポイントストレージとして使用している間、Lightningは同時に大量のデータをインポートしています。これにより、ターゲットデータベースに余分なストレスがかかり、通信タイムアウトが発生する場合があります。したがって、**これらのチェックポイントを保存するために一時的なMySQLサーバーをインストールすることを強くお勧めします**。このサーバーは`tidb-lightning`と同じホストにインストールでき、インポーターの進行が完了した後にアンインストールできます。

## チェックポイント管理 {#checkpoints-control}

回復不能なエラー（データ破損など）が原因で`tidb-lightning`が異常終了した場合、エラーが解決されるまでチェックポイントの再利用を拒否します。これは状況の悪化を防ぐためです。チェックポイントエラーは、 `tidb-lightning-ctl`プログラムを使用して解決できます。

### <code>--checkpoint-error-destroy</code> {#code-checkpoint-error-destroy-code}

```sh
tidb-lightning-ctl --checkpoint-error-destroy='`schema`.`table`'
```

このオプションを使用すると、テーブルのインポートを最初から再開できます。スキーマ名とテーブル名はバッククォートで引用する必要があり、大文字と小文字が区別されます。

-   テーブル`` `schema`.`table` ``のインポートが以前に失敗した場合、このオプションは次の操作を実行します。

    1.  ターゲットデータベースからテーブル`` `schema`.`table` ``を削除します。これは、インポートされたすべてのデータを削除することを意味します。
    2.  このテーブルのチェックポイントレコードを「まだ開始されていない」ようにリセットします。

-   表`` `schema`.`table` ``に関連するエラーがない場合、この操作は何もしません。

上記をすべてのテーブルに適用するのと同じです。これは、チェックポイントエラーの問題を修正するための最も便利で安全かつ保守的なソリューションです。

```sh
tidb-lightning-ctl --checkpoint-error-destroy=all
```

### <code>--checkpoint-error-ignore</code> {#code-checkpoint-error-ignore-code}

```sh
tidb-lightning-ctl --checkpoint-error-ignore='`schema`.`table`'
tidb-lightning-ctl --checkpoint-error-ignore=all
```

テーブル`` `schema`.`table` ``のインポートが以前に失敗した場合、これにより、何も起こらなかったかのようにエラーステータスがクリアされます。 `all`バリアントは、この操作をすべてのテーブルに適用します。

> **ノート：**
>
> このオプションは、エラーが実際に無視できることが確実な場合にのみ使用してください。そうしないと、インポートされたデータの一部が失われる可能性があります。唯一のセーフティネットは最後の「チェックサム」チェックであるため、 `--checkpoint-error-ignore`を使用する場合は「チェックサム」オプションを常に有効にしておく必要があります。

### <code>--checkpoint-remove</code> {#code-checkpoint-remove-code}

```sh
tidb-lightning-ctl --checkpoint-remove='`schema`.`table`'
tidb-lightning-ctl --checkpoint-remove=all
```

このオプションは、ステータスに関係なく、1つのテーブルまたはすべてのテーブルに関するすべてのチェックポイント情報を削除するだけです。

### <code>--checkpoint-dump</code> {#code-checkpoint-dump-code}

```sh
tidb-lightning-ctl --checkpoint-dump=output/directory
```

このオプションは、チェックポイントの内容を指定されたディレクトリにダンプします。このディレクトリは、主に技術スタッフによるデバッグに使用されます。このオプションは、 `driver = "mysql"`の場合にのみ有効になります。
