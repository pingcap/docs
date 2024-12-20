---
title: TiDB Lightning Command Line Flags
summary: コマンドラインフラグを使用してTiDB Lightning を構成する方法を学習します。
---

# TiDB Lightningコマンドラインフラグ {#tidb-lightning-command-line-flags}

TiDB Lightning は、構成ファイルまたはコマンド ラインを使用して構成できます。このドキュメントでは、 TiDB Lightningのコマンド ライン フラグについて説明します。

## コマンドラインフラグ {#command-line-flags}

### <code>tidb-lightning</code> {#code-tidb-lightning-code}

`tidb-lightning`使用して次のパラメータを設定できます。

| パラメータ                                                 | 説明                                                                                                                                                                                | 対応する構成項目                       |
| :---------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------- |
| `--config <file>`                                     | ファイルからグローバル構成を読み取ります。このパラメータが指定されていない場合、 TiDB Lightning はデフォルトの構成を使用します。                                                                                                          |                                |
| `-V`                                                  | プログラムのバージョンを印刷します。                                                                                                                                                                |                                |
| `-d <directory>`                                      | ローカル ディレクトリまたはデータ ファイルの[外部storageURI](/external-storage-uri.md) 。                                                                                                                 | `mydumper.data-source-dir`     |
| `-L <level>`                                          | `fatal` `info` `debug` `warn` `info` `error`                                                                                                                                      | `lightning.level`              |
| `-f <rule>`                                           | [テーブルフィルタルール](/table-filter.md) 。複数回指定できます。                                                                                                                                       | `mydumper.filter`              |
| `--backend <backend>`                                 | インポート モードを選択します。1 `local` [物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md) 、 `tidb` [論理インポートモード](/tidb-lightning/tidb-lightning-logical-import-mode.md)を表します。 | `tikv-importer.backend`        |
| `--log-file <file>`                                   | ログ ファイルのパス。デフォルトでは`/tmp/lightning.log.{timestamp}`です。 &#39;-&#39; に設定すると、ログ ファイルは stdout に出力されます。                                                                                 | `lightning.log-file`           |
| `--status-addr <ip:port>`                             | TiDB Lightningサーバーのリスニング アドレス                                                                                                                                                     | `lightning.status-port`        |
| `--pd-urls <host1:port1,host2:port2,...,hostn:portn>` | PD エンドポイント アドレス。v7.6.0 以降、TiDB は複数の PD アドレスの設定をサポートします。                                                                                                                           | `tidb.pd-addr`                 |
| `--tidb-host <host>`                                  | TiDBサーバーホスト                                                                                                                                                                       | `tidb.host`                    |
| `--tidb-port <port>`                                  | TiDBサーバーポート (デフォルト = 4000)                                                                                                                                                        | `tidb.port`                    |
| `--tidb-status <port>`                                | TiDB ステータス ポート (デフォルト = 10080)                                                                                                                                                    | `tidb.status-port`             |
| `--tidb-user <user>`                                  | TiDBに接続するためのユーザー名                                                                                                                                                                 | `tidb.user`                    |
| `--tidb-password <password>`                          | TiDB に接続するためのパスワード。パスワードはプレーンテキストまたは Base64 でエンコードされた形式にすることができます。                                                                                                                | `tidb.password`                |
| `--enable-checkpoint <bool>`                          | チェックポイントを有効にするかどうか（デフォルト = true）                                                                                                                                                  | `checkpoint.enable`            |
| `--analyze <level>`                                   | インポート後にテーブルを分析します。使用可能な値は、「必須」、「オプション」(デフォルト値)、および「オフ」です。                                                                                                                         | `post-restore.analyze`         |
| `--checksum <level>`                                  | インポート後にチェックサムを比較します。使用可能な値は、「必須」(デフォルト値)、「オプション」、および「オフ」です。                                                                                                                       | `post-restore.checksum`        |
| `--check-requirements <bool>`                         | タスクを開始する前にクラスターのバージョンの互換性を確認し、実行中に TiKV に 10% 以上の空き領域が残っているかどうかを確認します。(デフォルト = true)                                                                                              | `lightning.check-requirements` |
| `--ca <file>`                                         | TLS接続のCA証明書パス                                                                                                                                                                     | `security.ca-path`             |
| `--cert <file>`                                       | TLS接続の証明書パス                                                                                                                                                                       | `security.cert-path`           |
| `--key <file>`                                        | TLS接続の秘密鍵パス                                                                                                                                                                       | `security.key-path`            |
| `--server-mode`                                       | TiDB Lightningをサーバーモードで起動する                                                                                                                                                       | `lightning.server-mode`        |

コマンドラインパラメータと構成ファイル内の対応する設定の両方を指定した場合、コマンドラインパラメータが優先されます。たとえば、 `tiup tidb-lightning -L debug --config cfg.toml`実行すると、 `cfg.toml`の内容に関係なく、ログレベルは常に「debug」に設定されます。

## <code>tidb-lightning-ctl</code> {#code-tidb-lightning-ctl-code}

`tidb-lightning`のすべてのパラメータは`tidb-lightning-ctl`に適用されます。さらに、 `tidb-lightning-ctl`使用して次のパラメータを設定することもできます。

| パラメータ                                     | 説明                                                  |
| :---------------------------------------- | :-------------------------------------------------- |
| `--compact`                               | 完全な圧縮を実行します。                                        |
| `--switch-mode <mode>`                    | すべての TiKV ストアを指定されたモード (通常モードまたはインポート モード) に切り替えます。 |
| `--fetch-mode`                            | すべての TiKV ストアの現在のモードを出力します。                         |
| `--import-engine <uuid>`                  | 閉じたエンジン ファイルを TiKV インポーターから TiKV クラスターにインポートします。    |
| `--cleanup-engine <uuid>`                 | TiKV インポーターからエンジン ファイルを削除します。                       |
| `--checkpoint-dump <folder>`              | 現在のチェックポイントを CSV としてフォルダーにダンプします。                   |
| `--checkpoint-error-destroy <table_name>` | チェックポイントを削除します。エラーが発生した場合は、テーブルを削除します。              |
| `--checkpoint-error-ignore <table_name>`  | 指定されたテーブルに関連するチェックポイントに記録されたエラーを無視します。              |
| `--checkpoint-remove <table_name>`        | テーブルのチェックポイントを無条件に削除します。                            |

`<table_name>`は、形式`` `db`.`tbl` `` (バッククォートを含む) の修飾テーブル名、またはキーワード`all`のいずれかである必要があります。
