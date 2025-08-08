---
title: PingCAP Clinic Diagnostic Data
summary: PingCAPクリニック診断サービスは、 TiUPを使用してTiDBおよびDMクラスターから診断データを収集します。収集されるデータの種類には、クラスター情報、TiDBの診断データ、TiKV、PD、 TiFlash、TiCDC、Prometheusモニタリング、システム変数、ノードシステム情報が含まれます。データは、海外および中国本土のユーザー向けにClinic Serverに保存されます。収集されたデータは、クラスターの問題のトラブルシューティングにのみ使用されます。
---

# PingCAPクリニック診断データ {#pingcap-clinic-diagnostic-data}

このドキュメントでは、 TiUPを使用して展開された TiDB および DM クラスタからPingCAPクリニック診断サービス (PingCAPクリニック ) によって収集できる診断データの種類について説明します。また、各データの種類に対応するデータ収集パラメータも示します。1 [Diagクライアント（Diag）を使用してデータを収集する](/clinic/clinic-user-guide-for-tiup.md)コマンドを実行する際に、収集するデータの種類に応じて必要なパラメータをコマンドに追加できます。

PingCAPクリニックによって収集された診断データは、クラスターの問題のトラブルシューティングに**のみ**使用されます。

クラウドに展開される診断サービスである Clinic Server は、データのstorage場所に応じて 2 つの独立したサービスを提供します。

-   [海外ユーザー向けクリニックサーバー](https://clinic.pingcap.com) ：収集したデータを海外ユーザー向けのClinic Serverにアップロードすると、データはPingCAPがAWS米国リージョンに展開するAmazon S3サービスに保存されます。PingCAPは厳格なデータアクセスポリシーを採用しており、承認されたテクニカルサポート担当者のみがデータにアクセスできます。
-   [中国本土のユーザー向けクリニックサーバー](https://clinic.pingcap.com.cn) ：収集したデータを中国本土のユーザー向けクリニックサーバーにアップロードすると、データはPingCAPが中国（北京）リージョンに展開するAmazon S3サービスに保存されます。PingCAPは厳格なデータアクセスポリシーを採用しており、承認されたテクニカルサポート担当者のみがデータにアクセスできます。

## TiDB クラスター {#tidb-clusters}

このセクションでは、 TiUPを使用して展開された TiDB クラスターから[診断](https://github.com/pingcap/diag)によって収集できる診断データの種類を示します。

### TiDB クラスタ情報 {#tidb-cluster-information}

| データ型                 | エクスポートされたファイル  | PingCAPクリニックによるデータ収集パラメータ |
| :------------------- | :------------- | :------------------------ |
| クラスターIDを含むクラスターの基本情報 | `cluster.json` | デフォルトでは、データは実行ごとに収集されます。  |
| クラスターの詳細情報           | `meta.yaml`    | デフォルトでは、データは実行ごとに収集されます。  |

### TiDB診断データ {#tidb-diagnostic-data}

| データ型           | エクスポートされたファイル         | PingCAPクリニックによるデータ収集パラメータ |
| :------------- | :-------------------- | :------------------------ |
| ログ             | `tidb.log`            | `--include=log`           |
| エラーログ          | `tidb_stderr.log`     | `--include=log`           |
| スローログ          | `tidb_slow_query.log` | `--include=log`           |
| 監査ログ           | `tidb-audit.log.json` | `--include=log`           |
| コンフィグレーションファイル | `tidb.toml`           | `--include=config`        |
| リアルタイム構成       | `config.json`         | `--include=config`        |

### TiKV診断データ {#tikv-diagnostic-data}

| データ型           | エクスポートされたファイル     | PingCAPクリニックによるデータ収集パラメータ |
| :------------- | :---------------- | :------------------------ |
| ログ             | `tikv.log`        | `--include=log`           |
| エラーログ          | `tikv_stderr.log` | `--include=log`           |
| コンフィグレーションファイル | `tikv.toml`       | `--include=config`        |
| リアルタイム構成       | `config.json`     | `--include=config`        |

### PD診断データ {#pd-diagnostic-data}

| データ型                                                                                           | エクスポートされたファイル         | PingCAPクリニックによるデータ収集パラメータ |
| :--------------------------------------------------------------------------------------------- | :-------------------- | :------------------------ |
| ログ                                                                                             | `pd.log`              | `--include=log`           |
| エラーログ                                                                                          | `pd_stderr.log`       | `--include=log`           |
| コンフィグレーションファイル                                                                                 | `pd.toml`             | `--include=config`        |
| リアルタイム構成                                                                                       | `config.json`         | `--include=config`        |
| コマンド`tiup ctl:v<CLUSTER_VERSION> pd -u http://${pd IP}:${PORT} store`の出力                       | `store.json`          | `--include=config`        |
| コマンド`tiup ctl:v<CLUSTER_VERSION> pd -u http://${pd IP}:${PORT} config placement-rules show`の出力 | `placement-rule.json` | `--include=config`        |

### TiFlash診断データ {#tiflash-diagnostic-data}

| データ型           | エクスポートされたファイル                                                     | PingCAPクリニックによるデータ収集パラメータ |
| :------------- | :---------------------------------------------------------------- | :------------------------ |
| ログ             | `tiflash.log`                                                     | `--include=log`           |
| エラーログ          | `tiflash_stderr.log`                                              | `--include=log`           |
| コンフィグレーションファイル | `tiflash-learner.toml` `tiflash-preprocessed.toml` `tiflash.toml` | `--include=config`        |
| リアルタイム構成       | `config.json`                                                     | `--include=config`        |

### TiCDC診断データ {#ticdc-diagnostic-data}

| データ型           | エクスポートされたファイル                                                             | PingCAPクリニックによるデータ収集パラメータ                         |
| :------------- | :------------------------------------------------------------------------ | :------------------------------------------------ |
| ログ             | `ticdc.log`                                                               | `--include=log`                                   |
| エラーログ          | `ticdc_stderr.log`                                                        | `--include=log`                                   |
| コンフィグレーションファイル | `ticdc.toml`                                                              | `--include=config`                                |
| デバッグデータ        | `info.txt` `status.txt` `changefeeds.txt` `captures.txt` `processors.txt` | `--include=debug` (Diag はデフォルトではこのデータ タイプを収集しません) |

### プロメテウス監視データ {#prometheus-monitoring-data}

| データ型        | エクスポートされたファイル        | PingCAPクリニックによるデータ収集パラメータ |
| :---------- | :------------------- | :------------------------ |
| すべての指標データ   | `{metric_name}.json` | `--include=monitor`       |
| すべてのアラートデータ | `alerts.json`        | `--include=monitor`       |

### TiDB システム変数 {#tidb-system-variables}

| データ型        | エクスポートされたファイル          | PingCAPクリニックによるデータ収集パラメータ                                                                  |
| :---------- | :--------------------- | :----------------------------------------------------------------------------------------- |
| TiDB システム変数 | `mysql.tidb.csv`       | `--include=db_vars` (Diag はデフォルトではこのデータ タイプを収集しません。このデータ タイプを収集する必要がある場合は、データベース資格情報が必要です) |
|             | `global_variables.csv` | `--include=db_vars` (Diag はデフォルトではこのデータ タイプを収集しません)                                        |

### クラスタノードのシステム情報 {#system-information-of-the-cluster-node}

| データ型                           | エクスポートされたファイル  | PingCAPクリニックによるデータ収集パラメータ |
| :----------------------------- | :------------- | :------------------------ |
| カーネルログ                         | `dmesg.log`    | `--include=system`        |
| システムとハードウェアの基本情報               | `insight.json` | `--include=system`        |
| `/etc/security/limits.conf`の内容 | `limits.conf`  | `--include=system`        |
| カーネルパラメータのリスト                  | `sysctl.conf`  | `--include=system`        |
| ソケットシステム情報（ `ss`コマンドの出力）       | `ss.txt`       | `--include=system`        |

## DMクラスター {#dm-clusters}

このセクションでは、 TiUPを使用して展開された DM クラスターから Diag によって収集できる診断データの種類を示します。

### DMクラスター情報 {#dm-cluster-information}

| データ型                 | エクスポートされたファイル  | PingCAPクリニックによるデータ収集パラメータ |
| :------------------- | :------------- | :------------------------ |
| クラスターIDを含むクラスターの基本情報 | `cluster.json` | デフォルトでは、データは実行ごとに収集されます。  |
| クラスターの詳細情報           | `meta.yaml`    | デフォルトでは、データは実行ごとに収集されます。  |

### dm-master診断データ {#dm-master-diagnostic-data}

| データ型           | エクスポートされたファイル          | PingCAPクリニックによるデータ収集パラメータ |
| :------------- | :--------------------- | :------------------------ |
| ログ             | `dm-master.log`        | `--include=log`           |
| エラーログ          | `dm-master_stderr.log` | `--include=log`           |
| コンフィグレーションファイル | `dm-master.toml`       | `--include=config`        |

### dm-worker診断データ {#dm-worker-diagnostic-data}

| データ型           | エクスポートされたファイル          | PingCAPクリニックによるデータ収集パラメータ |
| :------------- | :--------------------- | :------------------------ |
| ログ             | `dm-worker.log`        | `--include=log`           |
| エラーログ          | `dm-worker_stderr.log` | `--include=log`           |
| コンフィグレーションファイル | `dm-work.toml`         | `--include=config`        |

### プロメテウス監視データ {#prometheus-monitoring-data}

| データ型        | エクスポートされたファイル        | PingCAPクリニックによるデータ収集パラメータ |
| :---------- | :------------------- | :------------------------ |
| すべての指標データ   | `{metric_name}.json` | `--include=monitor`       |
| すべてのアラートデータ | `alerts.json`        | `--include=monitor`       |

### クラスタノードのシステム情報 {#system-information-of-the-cluster-node}

| データ型                               | エクスポートされたファイル  | PingCAPクリニックによるデータ収集パラメータ |
| :--------------------------------- | :------------- | :------------------------ |
| カーネルログ                             | `dmesg.log`    | `--include=system`        |
| システムとハードウェアの基本情報                   | `insight.json` | `--include=system`        |
| `/etc/security/limits.conf`システムの内容 | `limits.conf`  | `--include=system`        |
| カーネルパラメータのリスト                      | `sysctl.conf`  | `--include=system`        |
| ソケットシステム情報（ `ss`コマンドの出力）           | `ss.txt`       | `--include=system`        |

### ログファイルの分類 {#log-file-classification}

`--include=log.<type>`パラメータを使用して、収集するログの種類を指定できます。

ログの種類:

-   `std` : ファイル名に`stderr`含まれるログファイル。
-   `rocksdb` : プレフィックスが`rocksdb` 、サフィックスが`.info`ログ ファイル。
-   `slow` : クエリ ログ ファイルが遅い。
-   `unknown` : 上記のいずれの種類にも一致しないログ ファイル。
