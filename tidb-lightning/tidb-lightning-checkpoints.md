---
title: TiDB Lightning Checkpoints
summary: Use checkpoints to avoid redoing the previously completed tasks before the crash.
---

# TiDB Lightningチェックポイント {#tidb-lightning-checkpoints}

大規模なデータベースのインポートには通常、数時間から数日かかります。そのような長時間実行プロセスが誤ってクラッシュした場合、以前に完了したタスクをやり直すのは非常に時間の無駄になる可能性があります。これを解決するために、 TiDB Lightning は*チェックポイント*を使用してインポートの進行状況を保存し、再起動後に中断`tidb-lightning`たところからインポートを続行します。

このドキュメントでは、*チェックポイントを*有効化、構成、保存、制御する方法について説明します。

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

## チェックポイントのstorage {#checkpoints-storage}

TiDB Lightning は、ローカル ファイルまたはリモートの MySQL 互換データベースの 2 種類のチェックポイントstorageをサポートします。

-   `driver = "file"`を指定すると、チェックポイントは`dsn`設定で指定されたパスのローカル ファイルに保存されます。チェックポイントは急速に更新されるため、RAM ディスクなど、書き込み耐久性が非常に高いドライブにチェックポイント ファイルを配置することを強くお勧めします。

-   `driver = "mysql"`を使用すると、 MySQL 5.7以降と互換性のあるデータベース (MariaDB や TiDB など) にチェックポイントを保存できます。デフォルトでは、チェックポイントはターゲット データベースに保存されます。

Lightning は、ターゲットデータベースをチェックポイントstorageとして使用しながら、同時に大量のデータをインポートします。これにより、ターゲット データベースに余分な負荷がかかり、場合によっては通信タイムアウトが発生することがあります。したがって、**これらのチェックポイントを保存するために一時的な MySQLサーバーをインストールすることを強くお勧めします**。このサーバーは`tidb-lightning`と同じホストにインストールでき、インポーターの進行が完了した後にアンインストールできます。

## チェックポイント制御 {#checkpoints-control}

`tidb-lightning`が回復不可能なエラー (データ破損など) により異常終了した場合、エラーが解決されるまでチェックポイントの再利用を拒否します。これは状況の悪化を防ぐためです。チェックポイント エラーは、 `tidb-lightning-ctl`プログラムを使用して解決できます。

### <code>--checkpoint-error-destroy</code> {#code-checkpoint-error-destroy-code}

```sh
tidb-lightning-ctl --checkpoint-error-destroy='`schema`.`table`'
```

このオプションを使用すると、テーブルのインポートを最初から再開できます。スキーマ名とテーブル名は逆引用符で囲む必要があり、大文字と小文字が区別されます。

-   テーブル`` `schema`.`table` ``のインポートが以前に失敗した場合、このオプションは次の操作を実行します。

    1.  ターゲット データベースからテーブル`` `schema`.`table` ``を DROP します。これは、インポートされたデータをすべて削除することを意味します。
    2.  このテーブルのチェックポイント レコードを「まだ開始されていない」状態にリセットします。

-   テーブル`` `schema`.`table` ``に関連するエラーがない場合、この操作は何も行いません。

上記をすべてのテーブルに適用するのと同じです。これは、チェックポイント エラーの問題を解決するための最も便利で安全かつ保守的な解決策です。

```sh
tidb-lightning-ctl --checkpoint-error-destroy=all
```

### <code>--checkpoint-error-ignore</code> {#code-checkpoint-error-ignore-code}

```sh
tidb-lightning-ctl --checkpoint-error-ignore='`schema`.`table`'
tidb-lightning-ctl --checkpoint-error-ignore=all
```

テーブル`` `schema`.`table` ``のインポートが以前に失敗した場合、これにより、何も起こらなかったかのようにエラー ステータスがクリアされます。 `all`バリアントでは、この操作がすべてのテーブルに適用されます。

> **注記：**
>
> このオプションは、エラーが実際に無視できることが確実な場合にのみ使用してください。そうしないと、インポートされたデータの一部が失われる可能性があります。唯一のセーフティネットは最後の「チェックサム」チェックであるため、 `--checkpoint-error-ignore`を使用する場合は「チェックサム」オプションを常に有効にしておく必要があります。

### <code>--checkpoint-remove</code> {#code-checkpoint-remove-code}

```sh
tidb-lightning-ctl --checkpoint-remove='`schema`.`table`'
tidb-lightning-ctl --checkpoint-remove=all
```

このオプションは、ステータスに関係なく、1 つのテーブルまたはすべてのテーブルに関するすべてのチェックポイント情報を単純に削除します。

### <code>--checkpoint-dump</code> {#code-checkpoint-dump-code}

```sh
tidb-lightning-ctl --checkpoint-dump=output/directory
```

このオプションは、チェックポイントの内容を指定されたディレクトリにダンプします。これは主に技術スタッフによるデバッグに使用されます。このオプションは`driver = "mysql"`の場合にのみ有効になります。
