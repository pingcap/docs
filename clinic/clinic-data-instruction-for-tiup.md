---
title: PingCAP Clinic Diagnostic Data
summary: Learn what diagnostic data can be collected by PingCAP Clinic Diagnostic Service from the TiDB and DM clusters deployed using TiUP.
---

# PingCAPクリニックの診断データ {#pingcap-clinic-diagnostic-data}

このドキュメントでは、 TiUPを使用して展開された TiDB および DM クラスターからPingCAPクリニック診断サービス (PingCAPクリニック) によって収集できる診断データの種類について説明します。また、このドキュメントには、各データ タイプに対応するデータ収集用のパラメーターがリストされています。 [Diag クライアント (Diag) を使用してデータを収集する](/clinic/clinic-user-guide-for-tiup.md)にコマンドを実行する場合、収集するデータの種類に応じて必要なパラメータをコマンドに追加できます。

PingCAPクリニックによって収集された診断データは、クラスターの問題のトラブルシューティングに**のみ**使用されます。

クラウドに展開された診断サービスである Clinic Server は、データのstorage場所に応じて 2 つの独立したサービスを提供します。

-   [海外ユーザー向けクリニックサーバー](https://clinic.pingcap.com) : 収集したデータを海外ユーザー向けの Clinic Server にアップロードすると、データは AWS 米国リージョンの PingCAP によってデプロイされた Amazon S3 サービスに保存されます。 PingCAP は厳格なデータ アクセス ポリシーを使用しており、承認されたテクニカル サポートのみがデータにアクセスできます。
-   [中国本土のユーザー向けクリニックサーバー](https://clinic.pingcap.com.cn) : 収集したデータを中国本土のユーザー向けに Clinic Server にアップロードすると、データは中国 (北京) リージョンの PingCAP によって展開された Amazon S3 サービスに保存されます。 PingCAP は厳格なデータ アクセス ポリシーを使用しており、承認されたテクニカル サポートのみがデータにアクセスできます。

## TiDB クラスター {#tidb-clusters}

このセクションでは、 TiUPを使用してデプロイされた TiDB クラスターから[診断](https://github.com/pingcap/diag)で収集できる診断データのタイプをリストします。

### TiDB クラスター情報 {#tidb-cluster-information}

| データ・タイプ              | エクスポートされたファイル  | PingCAPクリニックによるデータ収集のパラメータ |
| :------------------- | :------------- | :------------------------- |
| クラスターIDなどのクラスターの基本情報 | `cluster.json` | デフォルトでは、データは実行ごとに収集されます。   |
| クラスターの詳細情報           | `meta.yaml`    | デフォルトでは、データは実行ごとに収集されます。   |

### TiDB 診断データ {#tidb-diagnostic-data}

| データ・タイプ        | エクスポートされたファイル         | PingCAPクリニックによるデータ収集のパラメータ |
| :------------- | :-------------------- | :------------------------- |
| ログ             | `tidb.log`            | `--include=log`            |
| エラーログ          | `tidb_stderr.log`     | `--include=log`            |
| 遅いログ           | `tidb_slow_query.log` | `--include=log`            |
| コンフィグレーションファイル | `tidb.toml`           | `--include=config`         |
| リアルタイム設定       | `config.json`         | `--include=config`         |

### TiKV 診断データ {#tikv-diagnostic-data}

| データ・タイプ        | エクスポートされたファイル     | PingCAPクリニックによるデータ収集のパラメータ |
| :------------- | :---------------- | :------------------------- |
| ログ             | `tikv.log`        | `--include=log`            |
| エラーログ          | `tikv_stderr.log` | `--include=log`            |
| コンフィグレーションファイル | `tikv.toml`       | `--include=config`         |
| リアルタイム設定       | `config.json`     | `--include=config`         |

### PD診断データ {#pd-diagnostic-data}

| データ・タイプ                                                                                        | エクスポートされたファイル         | PingCAPクリニックによるデータ収集のパラメータ |
| :--------------------------------------------------------------------------------------------- | :-------------------- | :------------------------- |
| ログ                                                                                             | `pd.log`              | `--include=log`            |
| エラーログ                                                                                          | `pd_stderr.log`       | `--include=log`            |
| コンフィグレーションファイル                                                                                 | `pd.toml`             | `--include=config`         |
| リアルタイム設定                                                                                       | `config.json`         | `--include=config`         |
| コマンド`tiup ctl:v<CLUSTER_VERSION> pd -u http://${pd IP}:${PORT} store`の出力                       | `store.json`          | `--include=config`         |
| コマンド`tiup ctl:v<CLUSTER_VERSION> pd -u http://${pd IP}:${PORT} config placement-rules show`の出力 | `placement-rule.json` | `--include=config`         |

### TiFlash診断データ {#tiflash-diagnostic-data}

| データ・タイプ        | エクスポートされたファイル                                                     | PingCAPクリニックによるデータ収集のパラメータ |
| :------------- | :---------------------------------------------------------------- | :------------------------- |
| ログ             | `tiflash.log`                                                     | `--include=log`            |
| エラーログ          | `tiflash_stderr.log`                                              | `--include=log`            |
| コンフィグレーションファイル | `tiflash-learner.toml` `tiflash-preprocessed.toml` `tiflash.toml` | `--include=config`         |
| リアルタイム設定       | `config.json`                                                     | `--include=config`         |

### TiCDC 診断データ {#ticdc-diagnostic-data}

| データ・タイプ        | エクスポートされたファイル                                                             | PingCAPクリニックによるデータ収集のパラメータ                        |
| :------------- | :------------------------------------------------------------------------ | :------------------------------------------------ |
| ログ             | `ticdc.log`                                                               | `--include=log`                                   |
| エラーログ          | `ticdc_stderr.log`                                                        | `--include=log`                                   |
| コンフィグレーションファイル | `ticdc.toml`                                                              | `--include=config`                                |
| デバッグデータ        | `info.txt` `status.txt` `changefeeds.txt` `captures.txt` `processors.txt` | `--include=debug` (Diag はデフォルトではこのデータ タイプを収集しません) |

### プロメテウス監視データ {#prometheus-monitoring-data}

| データ・タイプ       | エクスポートされたファイル        | PingCAPクリニックによるデータ収集のパラメータ |
| :------------ | :------------------- | :------------------------- |
| すべてのメトリクス データ | `{metric_name}.json` | `--include=monitor`        |
| すべてのアラート データ  | `alerts.json`        | `--include=monitor`        |

### TiDB システム変数 {#tidb-system-variables}

| データ・タイプ     | エクスポートされたファイル          | PingCAPクリニックによるデータ収集のパラメータ                                                                  |
| :---------- | :--------------------- | :------------------------------------------------------------------------------------------ |
| TiDB システム変数 | `mysql.tidb.csv`       | `--include=db_vars` (Diag はデフォルトではこのデータ タイプを収集しません。このデータ タイプを収集する必要がある場合は、データベースの資格情報が必要です) |
|             | `global_variables.csv` | `--include=db_vars` (Diag はデフォルトではこのデータ タイプを収集しません)                                         |

### クラスタノードのシステム情報 {#system-information-of-the-cluster-node}

| データ・タイプ                        | エクスポートされたファイル  | PingCAPクリニックによるデータ収集のパラメータ |
| :----------------------------- | :------------- | :------------------------- |
| カーネルログ                         | `dmesg.log`    | `--include=system`         |
| システムやハードウェアの基本情報               | `insight.json` | `--include=system`         |
| `/etc/security/limits.conf`の内容 | `limits.conf`  | `--include=system`         |
| カーネルパラメータのリスト                  | `sysctl.conf`  | `--include=system`         |
| `ss`コマンドの出力であるソケット システム情報      | `ss.txt`       | `--include=system`         |

## DMクラスター {#dm-clusters}

このセクションでは、 TiUPを使用してデプロイされた DM クラスターから Diag によって収集できる診断データのタイプをリストします。

### DMクラスター情報 {#dm-cluster-information}

| データ・タイプ              | エクスポートされたファイル  | PingCAPクリニックによるデータ収集のパラメータ |
| :------------------- | :------------- | :------------------------- |
| クラスターIDなどのクラスターの基本情報 | `cluster.json` | デフォルトでは、データは実行ごとに収集されます。   |
| クラスターの詳細情報           | `meta.yaml`    | デフォルトでは、データは実行ごとに収集されます。   |

### dm-master 診断データ {#dm-master-diagnostic-data}

| データ・タイプ        | エクスポートされたファイル          | PingCAPクリニックによるデータ収集のパラメータ |
| :------------- | :--------------------- | :------------------------- |
| ログ             | `m-master.log`         | `--include=log`            |
| エラーログ          | `dm-master_stderr.log` | `--include=log`            |
| コンフィグレーションファイル | `dm-master.toml`       | `--include=config`         |

### dm-worker 診断データ {#dm-worker-diagnostic-data}

| データ・タイプ        | エクスポートされたファイル          | PingCAPクリニックによるデータ収集のパラメータ |
| :------------- | :--------------------- | :------------------------- |
| ログ             | `dm-worker.log`        | `--include=log`            |
| エラーログ          | `dm-worker_stderr.log` | `--include=log`            |
| コンフィグレーションファイル | `dm-work.toml`         | `--include=config`         |

### プロメテウス監視データ {#prometheus-monitoring-data}

| データ・タイプ       | エクスポートされたファイル        | PingCAPクリニックによるデータ収集のパラメータ |
| :------------ | :------------------- | :------------------------- |
| すべてのメトリクス データ | `{metric_name}.json` | `--include=monitor`        |
| すべてのアラート データ  | `alerts.json`        | `--include=monitor`        |

### クラスタノードのシステム情報 {#system-information-of-the-cluster-node}

| データ・タイプ                            | エクスポートされたファイル  | PingCAPクリニックによるデータ収集のパラメータ |
| :--------------------------------- | :------------- | :------------------------- |
| カーネルログ                             | `dmesg.log`    | `--include=system`         |
| システムやハードウェアの基本情報                   | `insight.json` | `--include=system`         |
| `/etc/security/limits.conf`システムの内容 | `limits.conf`  | `--include=system`         |
| カーネルパラメータのリスト                      | `sysctl.conf`  | `--include=system`         |
| `ss`コマンドの出力であるソケット システム情報          | `ss.txt`       | `--include=system`         |
