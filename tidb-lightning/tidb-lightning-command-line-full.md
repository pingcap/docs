---
title: TiDB Lightning Command Line Flags
summary: Learn how to configure TiDB Lightning using command line flags.
---

# TiDB Lightningコマンドライン フラグ {#tidb-lightning-command-line-flags}

構成ファイルまたはコマンドラインを使用して、 TiDB Lightningを構成できます。このドキュメントでは、 TiDB Lightningのコマンドライン フラグについて説明します。

## コマンド ライン フラグ {#command-line-flags}

### <code>tidb-lightning</code> {#code-tidb-lightning-code}

`tidb-lightning`を使用して次のパラメーターを構成できます。

| パラメータ                         | 説明                                                                                                                                                                                     | 対応する構成アイテム                     |
| :---------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------- |
| `--config <file>`             | ファイルからグローバル構成を読み取ります。このパラメータが指定されていない場合、 TiDB Lightning はデフォルト設定を使用します。                                                                                                                |                                |
| `-V`                          | プログラムのバージョンを印刷します。                                                                                                                                                                     |                                |
| `-d <directory>`              | ローカル ディレクトリまたはデータ ファイルの[外部storageURL](/br/backup-and-restore-storages.md#url-format) 。                                                                                                 | `mydumper.data-source-dir`     |
| `-L <level>`                  | ログ レベル: `debug` 、 `info` 、 `warn` 、 `error` 、または`fatal` 。デフォルトでは`info` 。                                                                                                               | `lightning.level`              |
| `-f <rule>`                   | [テーブル フィルター ルール](/table-filter.md) .複数回指定できます。                                                                                                                                         | `mydumper.filter`              |
| `--backend <backend>`         | インポート モードを選択します。 `local` [物理インポート モード](/tidb-lightning/tidb-lightning-physical-import-mode.md)を指します。 `tidb` [論理インポート モード](/tidb-lightning/tidb-lightning-logical-import-mode.md)を指します。 | `tikv-importer.backend`        |
| `--log-file <file>`           | ログ ファイルのパス。デフォルトでは`/tmp/lightning.log.{timestamp}`です。 「-」に設定すると、ログ ファイルが stdout に出力されることを意味します。                                                                                        | `lightning.log-file`           |
| `--status-addr <ip:port>`     | TiDB Lightningサーバーのリッスン アドレス                                                                                                                                                           | `lightning.status-port`        |
| `--importer <host:port>`      | TiKV インポーターの住所                                                                                                                                                                         | `tikv-importer.addr`           |
| `--pd-urls <host:port>`       | PD エンドポイント アドレス                                                                                                                                                                        | `tidb.pd-addr`                 |
| `--tidb-host <host>`          | TiDBサーバーホスト                                                                                                                                                                            | `tidb.host`                    |
| `--tidb-port <port>`          | TiDBサーバーポート (デフォルト = 4000)                                                                                                                                                             | `tidb.port`                    |
| `--tidb-status <port>`        | TiDB ステータス ポート (デフォルト = 10080)                                                                                                                                                         | `tidb.status-port`             |
| `--tidb-user <user>`          | TiDB に接続するためのユーザー名                                                                                                                                                                     | `tidb.user`                    |
| `--tidb-password <password>`  | TiDB に接続するためのパスワード。パスワードは、プレーンテキストまたは Base64 エンコードのいずれかです。                                                                                                                             | `tidb.password`                |
| `--enable-checkpoint <bool>`  | チェックポイントを有効にするかどうか (デフォルト = true)                                                                                                                                                      | `checkpoint.enable`            |
| `--analyze <level>`           | インポート後にテーブルを分析します。使用可能な値は、「required」、「optional」(デフォルト値)、および「off」です。                                                                                                                    | `post-restore.analyze`         |
| `--checksum <level>`          | インポート後にチェックサムを比較します。使用可能な値は、「required」(デフォルト値)、「optional」、および「off」です。                                                                                                                  | `post-restore.checksum`        |
| `--check-requirements <bool>` | 開始前にクラスターのバージョンの互換性を確認する (デフォルト = true)                                                                                                                                                | `lightning.check-requirements` |
| `--ca <file>`                 | TLS 接続の CA 証明書パス                                                                                                                                                                       | `security.ca-path`             |
| `--cert <file>`               | TLS 接続の証明書パス                                                                                                                                                                           | `security.cert-path`           |
| `--key <file>`                | TLS 接続の秘密鍵パス                                                                                                                                                                           | `security.key-path`            |
| `--server-mode`               | サーバーモードでTiDB Lightningを起動する                                                                                                                                                            | `lightning.server-mode`        |

コマンド ライン パラメータと構成ファイルの対応する設定の両方を指定すると、コマンド ライン パラメータが優先されます。たとえば、 `./tidb-lightning -L debug --config cfg.toml`を実行すると、 `cfg.toml`の内容に関係なく、常にログ レベルが「debug」に設定されます。

## <code>tidb-lightning-ctl</code> {#code-tidb-lightning-ctl-code}

`tidb-lightning`のすべてのパラメーターが`tidb-lightning-ctl`に適用されます。さらに、 `tidb-lightning-ctl`を使用して次のパラメーターを構成することもできます。

| パラメータ                                     | 説明                                                  |
| :---------------------------------------- | :-------------------------------------------------- |
| `--compact`                               | 完全圧縮を実行します。                                         |
| `--switch-mode <mode>`                    | すべての TiKV ストアを特定のモード (通常またはインポート) に切り替えます。          |
| `--fetch-mode`                            | すべての TiKV ストアの現在のモードを出力します。                         |
| `--import-engine <uuid>`                  | 閉じたエンジン ファイルを TiKV Importer から TiKV クラスターにインポートします。 |
| `--cleanup-engine <uuid>`                 | エンジン ファイルを TiKV Importer から削除します。                   |
| `--checkpoint-dump <folder>`              | 現在のチェックポイントを CSV としてフォルダーにダンプします。                   |
| `--checkpoint-error-destroy <table_name>` | チェックポイントを削除します。エラーが発生する場合は、テーブルを削除します。              |
| `--checkpoint-error-ignore <table_name>`  | 指定されたテーブルに関連するチェックポイントに記録されたエラーを無視します。              |
| `--checkpoint-remove <table_name>`        | テーブルのチェックポイントを無条件に削除します。                            |

`<table_name>`フォーム`` `db`.`tbl` `` (逆引用符を含む) の修飾テーブル名か、キーワード`all`いずれかでなければなりません。
