---
title: TiDB Lightning Command Line Flags
summary: コマンドラインフラグを使用してTiDB Lightningを構成する方法を学習します。
---

# TiDB Lightningコマンドラインフラグ {#tidb-lightning-command-line-flags}

TiDB Lightning は、設定ファイルまたはコマンドラインから設定できます。このドキュメントでは、 TiDB Lightningのコマンドラインフラグについて説明します。

## コマンドラインフラグ {#command-line-flags}

### <code>tidb-lightning</code> {#code-tidb-lightning-code}

`tidb-lightning`使用して次のパラメータを設定できます。

| パラメータ                                                 | 説明                                                                                                                                                                                | 対応する構成項目                       |
| :---------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------- |
| `--config <file>`                                     | ファイルからグローバル設定を読み取ります。このパラメータが指定されていない場合、 TiDB Lightningはデフォルト設定を使用します。                                                                                                            |                                |
| `-V`                                                  | プログラムのバージョンを印刷します。                                                                                                                                                                |                                |
| `-d <directory>`                                      | ローカル ディレクトリまたはデータ ファイルの[外部storageURI](/external-storage-uri.md) 。                                                                                                                 | `mydumper.data-source-dir`     |
| `-L <level>`                                          | ログ`info` : `debug` 、または`error` `warn`は`info` `fatal` 。                                                                                                                            | `lightning.level`              |
| `-f <rule>`                                           | [テーブルフィルタルール](/table-filter.md) 。複数回指定できます。                                                                                                                                       | `mydumper.filter`              |
| `--backend <backend>`                                 | インポート モードを選択します。1 は`local` 、 `tidb` [物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md) [論理インポートモード](/tidb-lightning/tidb-lightning-logical-import-mode.md)指します。 | `tikv-importer.backend`        |
| `--log-file <file>`                                   | ログファイルのパス。デフォルトでは`/tmp/lightning.log.{timestamp}`です。「-」に設定すると、ログファイルは標準出力に出力されます。                                                                                                 | `lightning.log-file`           |
| `--status-addr <ip:port>`                             | TiDB Lightningサーバーのリスニング アドレス                                                                                                                                                     | `lightning.status-port`        |
| `--pd-urls <host1:port1,host2:port2,...,hostn:portn>` | PDエンドポイントアドレス。v7.6.0以降、TiDBは複数のPDアドレスの設定をサポートします。                                                                                                                                 | `tidb.pd-addr`                 |
| `--tidb-host <host>`                                  | TiDBサーバーホスト                                                                                                                                                                       | `tidb.host`                    |
| `--tidb-port <port>`                                  | TiDBサーバーポート (デフォルト = 4000)                                                                                                                                                        | `tidb.port`                    |
| `--tidb-status <port>`                                | TiDB ステータス ポート (デフォルト = 10080)                                                                                                                                                    | `tidb.status-port`             |
| `--tidb-user <user>`                                  | TiDBに接続するためのユーザー名                                                                                                                                                                 | `tidb.user`                    |
| `--tidb-password <password>`                          | TiDBに接続するためのパスワード。パスワードはプレーンテキストまたはBase64エンコードのいずれかで指定できます。                                                                                                                       | `tidb.password`                |
| `--enable-checkpoint <bool>`                          | チェックポイントを有効にするかどうか（デフォルト = true）                                                                                                                                                  | `checkpoint.enable`            |
| `--analyze <level>`                                   | インポート後にテーブルを分析します。使用可能な値は「必須」、「オプション」（デフォルト値）、および「オフ」です。                                                                                                                          | `post-restore.analyze`         |
| `--checksum <level>`                                  | インポート後にチェックサムを比較します。使用可能な値は「必須」（デフォルト値）、「オプション」、「オフ」です。                                                                                                                           | `post-restore.checksum`        |
| `--check-requirements <bool>`                         | タスクを開始する前にクラスターのバージョンの互換性を確認し、実行中に TiKV に 10% 以上の空き領域が残っているかどうかを確認します。(デフォルト = true)                                                                                              | `lightning.check-requirements` |
| `--ca <file>`                                         | TLS接続のCA証明書パス                                                                                                                                                                     | `security.ca-path`             |
| `--cert <file>`                                       | TLS接続の証明書パス                                                                                                                                                                       | `security.cert-path`           |
| `--key <file>`                                        | TLS接続の秘密鍵パス                                                                                                                                                                       | `security.key-path`            |
| `--server-mode`                                       | TiDB Lightningをサーバーモードで起動する                                                                                                                                                       | `lightning.server-mode`        |

コマンドラインパラメータと設定ファイル内の対応する設定の両方を指定した場合、コマンドラインパラメータが優先されます。例えば、 `tiup tidb-lightning -L debug --config cfg.toml`実行すると、 `cfg.toml`の内容に関係なく、ログレベルは常に「debug」に設定されます。

## <code>tidb-lightning-ctl</code> {#code-tidb-lightning-ctl-code}

`tidb-lightning`のすべてのパラメータは`tidb-lightning-ctl`にも適用されます。さらに、 `tidb-lightning-ctl`を使用して以下のパラメータを設定することもできます。

| パラメータ                                     | 説明                                               |
| :---------------------------------------- | :----------------------------------------------- |
| `--compact`                               | 完全な圧縮を実行します。                                     |
| `--switch-mode <mode>`                    | すべての TiKV ストアを指定されたモード (通常またはインポート) に切り替えます。     |
| `--fetch-mode`                            | 各 TiKV ストアの現在のモードを出力します。                         |
| `--import-engine <uuid>`                  | 閉じたエンジン ファイルを TiKV インポーターから TiKV クラスターにインポートします。 |
| `--cleanup-engine <uuid>`                 | TiKV インポーターからエンジン ファイルを削除します。                    |
| `--checkpoint-dump <folder>`              | 現在のチェックポイントを CSV としてフォルダーにダンプします。                |
| `--checkpoint-error-destroy <table_name>` | チェックポイントを削除します。エラーが発生した場合は、テーブルを削除します。           |
| `--checkpoint-error-ignore <table_name>`  | 指定されたテーブルに関連するチェックポイントに記録されたエラーを無視します。           |
| `--checkpoint-remove <table_name>`        | テーブルのチェックポイントを無条件に削除します。                         |

`<table_name>` 、形式`` `db`.`tbl` `` (バッククォートを含む) の修飾されたテーブル名、またはキーワード`all`いずれかである必要があります。
