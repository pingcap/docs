---
title: TiDB Lightning Command Line Flags
summary: Learn how to configure TiDB Lightning using command line flags.
---

# TiDB Lightningコマンドラインフラグ {#tidb-lightning-command-line-flags}

TiDB Lightning は、構成ファイルまたはコマンドラインを使用して構成できます。このドキュメントでは、 TiDB Lightningのコマンド ライン フラグについて説明します。

## コマンドラインフラグ {#command-line-flags}

### <code>tidb-lightning</code> {#code-tidb-lightning-code}

`tidb-lightning`を使用して次のパラメータを設定できます。

| パラメータ                         | 説明                                                                                                                                                                                  | 対応する設定項目                       |
| :---------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------- |
| `--config <file>`             | ファイルからグローバル構成を読み取ります。このパラメータが指定されていない場合、 TiDB Lightning はデフォルト設定を使用します。                                                                                                             |                                |
| `-V`                          | プログラムのバージョンを印刷します。                                                                                                                                                                  |                                |
| `-d <directory>`              | ローカル ディレクトリまたはデータ ファイルの[外部storageURI](/external-storage-uri.md) 。                                                                                                                   | `mydumper.data-source-dir`     |
| `-L <level>`                  | ログレベル: `debug` 、 `info` 、 `warn` 、 `error` 、または`fatal` 。デフォルトでは`info` 。                                                                                                             | `lightning.level`              |
| `-f <rule>`                   | [テーブルフィルタールール](/table-filter.md) 。複数指定可能です。                                                                                                                                         | `mydumper.filter`              |
| `--backend <backend>`         | インポートモードを選択します。 `local` [物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md)を指します。 `tidb` [論理インポートモード](/tidb-lightning/tidb-lightning-logical-import-mode.md)を指します。 | `tikv-importer.backend`        |
| `--log-file <file>`           | ログファイルのパス。デフォルトでは`/tmp/lightning.log.{timestamp}`です。 「-」に設定すると、ログ ファイルが stdout に出力されることを意味します。                                                                                      | `lightning.log-file`           |
| `--status-addr <ip:port>`     | TiDB Lightningサーバーのリスニング アドレス                                                                                                                                                       | `lightning.status-port`        |
| `--pd-urls <host:port>`       | PDエンドポイントアドレス                                                                                                                                                                       | `tidb.pd-addr`                 |
| `--tidb-host <host>`          | TiDBサーバーホスト                                                                                                                                                                         | `tidb.host`                    |
| `--tidb-port <port>`          | TiDBサーバーポート (デフォルト = 4000)                                                                                                                                                          | `tidb.port`                    |
| `--tidb-status <port>`        | TiDB ステータス ポート (デフォルト = 10080)                                                                                                                                                      | `tidb.status-port`             |
| `--tidb-user <user>`          | TiDB に接続するためのユーザー名                                                                                                                                                                  | `tidb.user`                    |
| `--tidb-password <password>`  | TiDB に接続するためのパスワード。パスワードはプレーンテキストまたは Base64 エンコードのいずれかにすることができます。                                                                                                                   | `tidb.password`                |
| `--enable-checkpoint <bool>`  | チェックポイントを有効にするかどうか (デフォルト = true)                                                                                                                                                   | `checkpoint.enable`            |
| `--analyze <level>`           | インポート後にテーブルを分析します。使用可能な値は、「必須」、「オプション」(デフォルト値)、および「オフ」です。                                                                                                                           | `post-restore.analyze`         |
| `--checksum <level>`          | インポート後にチェックサムを比較します。使用可能な値は、「必須」(デフォルト値)、「オプション」、および「オフ」です。                                                                                                                         | `post-restore.checksum`        |
| `--check-requirements <bool>` | タスクを開始する前にクラスターのバージョンの互換性を確認し、実行中に TiKV に 10% 以上の空き領域が残っているかどうかを確認してください。 (デフォルト = true)                                                                                            | `lightning.check-requirements` |
| `--ca <file>`                 | TLS接続用のCA証明書パス                                                                                                                                                                      | `security.ca-path`             |
| `--cert <file>`               | TLS接続の証明書パス                                                                                                                                                                         | `security.cert-path`           |
| `--key <file>`                | TLS接続用の秘密キーのパス                                                                                                                                                                      | `security.key-path`            |
| `--server-mode`               | TiDB Lightning をサーバーモードで開始する                                                                                                                                                        | `lightning.server-mode`        |

コマンド ライン パラメータと構成ファイル内の対応する設定の両方を指定した場合は、コマンド ライン パラメータが優先されます。たとえば、 `./tidb-lightning -L debug --config cfg.toml`を実行すると、 `cfg.toml`の内容に関係なく、ログ レベルが常に「デバッグ」に設定されます。

## <code>tidb-lightning-ctl</code> {#code-tidb-lightning-ctl-code}

`tidb-lightning`のすべてのパラメータは`tidb-lightning-ctl`に適用されます。さらに、 `tidb-lightning-ctl`を使用して次のパラメータを設定することもできます。

| パラメータ                                     | 説明                                               |
| :---------------------------------------- | :----------------------------------------------- |
| `--compact`                               | 完全な圧縮を実行します。                                     |
| `--switch-mode <mode>`                    | すべての TiKV ストアを指定されたモード (通常またはインポート) に切り替えます。     |
| `--fetch-mode`                            | すべての TiKV ストアの現在のモードを出力します。                      |
| `--import-engine <uuid>`                  | 閉じたエンジン ファイルを TiKV インポーターから TiKV クラスターにインポートします。 |
| `--cleanup-engine <uuid>`                 | TiKV Importer からエンジン ファイルを削除します。                 |
| `--checkpoint-dump <folder>`              | 現在のチェックポイントを CSV としてフォルダーにダンプします。                |
| `--checkpoint-error-destroy <table_name>` | チェックポイントを削除します。エラーが発生する場合は、テーブルを削除します。           |
| `--checkpoint-error-ignore <table_name>`  | 指定されたテーブルに関連するチェックポイントに記録されたエラーを無視します。           |
| `--checkpoint-remove <table_name>`        | テーブルのチェックポイントを無条件に削除します。                         |

`<table_name>`形式`` `db`.`tbl` `` (逆引用符を含む) の修飾テーブル名、またはキーワード`all`いずれかである必要があります。
