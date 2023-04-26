---
title: PingCAP Clinic Diagnostic Data
summary: Learn what diagnostic data can be collected by PingCAP Clinic Diagnostic Service from the TiDB and DM clusters deployed using TiUP.
---

# PingCAPクリニックの診断データ {#pingcap-clinic-diagnostic-data}

このドキュメントでは、 TiUPを使用して展開された TiDB および DM クラスターからPingCAPクリニック Diagnostic Service (PingCAPクリニック ) によって収集できる診断データの種類について説明します。また、ドキュメントには、各データ型に対応するデータ収集用のパラメーターがリストされています。コマンドを[Diag クライアント (Diag) を使用してデータを収集する](/clinic/clinic-user-guide-for-tiup.md)に実行する場合、収集するデータの種類に応じて、コマンドに必要なパラメーターを追加できます。

PingCAPクリニックによって収集された診断データは、クラスターの問題のトラブルシューティングに**のみ**使用されます。

クラウドに展開された診断サービスである Clinic Server は、データstorageの場所に応じて 2 つの独立したサービスを提供します。

-   [海外ユーザー向けクリニックサーバー](https://clinic.pingcap.com) : 収集したデータを国際ユーザー向けの Clinic Server にアップロードすると、データは PingCAP によって AWS 米国リージョンにデプロイされた Amazon S3 サービスに保存されます。 PingCAP は厳格なデータ アクセス ポリシーを使用しており、承認されたテクニカル サポートのみがデータにアクセスできます。
-   [中国本土のユーザー向けクリニックサーバー](https://clinic.pingcap.com.cn) : 収集したデータを中国本土のユーザー向けの Clinic Server にアップロードすると、データは中国 (北京) リージョンの PingCAP によってデプロイされた Amazon S3 サービスに保存されます。 PingCAP は厳格なデータ アクセス ポリシーを使用しており、承認されたテクニカル サポートのみがデータにアクセスできます。

## TiDB クラスター {#tidb-clusters}

このセクションでは、 TiUPを使用してデプロイされた TiDB クラスターから[診断](https://github.com/pingcap/diag)で収集できる診断データの種類を示します。

### TiDB クラスター情報 {#tidb-cluster-information}

| データ・タイプ                | エクスポートされたファイル  | PingCAPクリニックによるデータ収集のパラメータ |
| :--------------------- | :------------- | :------------------------- |
| クラスター ID を含むクラスターの基本情報 | `cluster.json` | デフォルトでは、データは実行ごとに収集されます。   |
| クラスタの詳細情報              | `meta.yaml`    | デフォルトでは、データは実行ごとに収集されます。   |

### TiDB 診断データ {#tidb-diagnostic-data}

| データ・タイプ        | エクスポートされたファイル         | PingCAPクリニックによるデータ収集のパラメータ |
| :------------- | :-------------------- | :------------------------- |
| ログ             | `tidb.log`            | `--include=log`            |
| エラーログ          | `tidb_stderr.log`     | `--include=log`            |
| スローログ          | `tidb_slow_query.log` | `--include=log`            |
| コンフィグレーションファイル | `tidb.toml`           | `--include=config`         |
| リアルタイム構成       | `config.json`         | `--include=config`         |

### TiKV診断データ {#tikv-diagnostic-data}

| データ・タイプ        | エクスポートされたファイル     | PingCAPクリニックによるデータ収集のパラメータ |
| :------------- | :---------------- | :------------------------- |
| ログ             | `tikv.log`        | `--include=log`            |
| エラーログ          | `tikv_stderr.log` | `--include=log`            |
| コンフィグレーションファイル | `tikv.toml`       | `--include=config`         |
| リアルタイム構成       | `config.json`     | `--include=config`         |

### PD診断データ {#pd-diagnostic-data}

| データ・タイプ                                                                                        | エクスポートされたファイル         | PingCAPクリニックによるデータ収集のパラメータ |
| :--------------------------------------------------------------------------------------------- | :-------------------- | :------------------------- |
| ログ                                                                                             | `pd.log`              | `--include=log`            |
| エラーログ                                                                                          | `pd_stderr.log`       | `--include=log`            |
| コンフィグレーションファイル                                                                                 | `pd.toml`             | `--include=config`         |
| リアルタイム構成                                                                                       | `config.json`         | `--include=config`         |
| コマンド`tiup ctl:v<CLUSTER_VERSION> pd -u http://${pd IP}:${PORT} store`の出力                       | `store.json`          | `--include=config`         |
| コマンド`tiup ctl:v<CLUSTER_VERSION> pd -u http://${pd IP}:${PORT} config placement-rules show`の出力 | `placement-rule.json` | `--include=config`         |

### TiFlash診断データ {#tiflash-diagnostic-data}

| データ・タイプ        | エクスポートされたファイル                                                         | PingCAPクリニックによるデータ収集のパラメータ |
| :------------- | :-------------------------------------------------------------------- | :------------------------- |
| ログ             | `tiflash.log`                                                         | `--include=log`            |
| エラーログ          | `tiflash_stderr.log`                                                  | `--include=log`            |
| コンフィグレーションファイル | `tiflash-learner.toml` 、 `tiflash-preprocessed.toml` 、 `tiflash.toml` | `--include=config`         |
| リアルタイム構成       | `config.json`                                                         | `--include=config`         |

### TiCDC 診断データ {#ticdc-diagnostic-data}

| データ・タイプ        | エクスポートされたファイル                                                                     | PingCAPクリニックによるデータ収集のパラメータ                      |
| :------------- | :-------------------------------------------------------------------------------- | :---------------------------------------------- |
| ログ             | `ticdc.log`                                                                       | `--include=log`                                 |
| エラーログ          | `ticdc_stderr.log`                                                                | `--include=log`                                 |
| コンフィグレーションファイル | `ticdc.toml`                                                                      | `--include=config`                              |
| デバッグデータ        | `info.txt` 、 `status.txt` 、 `changefeeds.txt` 、 `captures.txt` 、 `processors.txt` | `--include=debug` (デフォルトでは、Diag はこのデータ型を収集しません) |

### プロメテウス監視データ {#prometheus-monitoring-data}

| データ・タイプ      | エクスポートされたファイル        | PingCAPクリニックによるデータ収集のパラメータ |
| :----------- | :------------------- | :------------------------- |
| すべての指標データ    | `{metric_name}.json` | `--include=monitor`        |
| すべてのアラート データ | `alerts.json`        | `--include=monitor`        |

### TiDB システム変数 {#tidb-system-variables}

| データ・タイプ     | エクスポートされたファイル          | PingCAPクリニックによるデータ収集のパラメータ                                                                  |
| :---------- | :--------------------- | :------------------------------------------------------------------------------------------ |
| TiDB システム変数 | `mysql.tidb.csv`       | `--include=db_vars` (デフォルトでは、Diag はこのデータ タイプを収集しません。このデータ タイプを収集する必要がある場合は、データベース資格情報が必要です) |
|             | `global_variables.csv` | `--include=db_vars` (デフォルトでは、Diag はこのデータ型を収集しません)                                           |

### クラスタノードのシステム情報 {#system-information-of-the-cluster-node}

| データ・タイプ                        | エクスポートされたファイル  | PingCAPクリニックによるデータ収集のパラメータ |
| :----------------------------- | :------------- | :------------------------- |
| カーネルログ                         | `dmesg.log`    | `--include=system`         |
| システムとハードウェアの基本情報               | `insight.json` | `--include=system`         |
| `/etc/security/limits.conf`の内容 | `limits.conf`  | `--include=system`         |
| カーネルパラメータ一覧                    | `sysctl.conf`  | `--include=system`         |
| `ss`コマンドの出力であるソケット システム情報      | `ss.txt`       | `--include=system`         |

## DM クラスター {#dm-clusters}

このセクションでは、 TiUPを使用してデプロイされた DM クラスターから Diag によって収集できる診断データの種類を示します。

### DM クラスター情報 {#dm-cluster-information}

| データ・タイプ                | エクスポートされたファイル  | PingCAPクリニックによるデータ収集のパラメータ |
| :--------------------- | :------------- | :------------------------- |
| クラスター ID を含むクラスターの基本情報 | `cluster.json` | デフォルトでは、データは実行ごとに収集されます。   |
| クラスタの詳細情報              | `meta.yaml`    | デフォルトでは、データは実行ごとに収集されます。   |

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

| データ・タイプ      | エクスポートされたファイル        | PingCAPクリニックによるデータ収集のパラメータ |
| :----------- | :------------------- | :------------------------- |
| すべての指標データ    | `{metric_name}.json` | `--include=monitor`        |
| すべてのアラート データ | `alerts.json`        | `--include=monitor`        |

### クラスタノードのシステム情報 {#system-information-of-the-cluster-node}

| データ・タイプ                          | エクスポートされたファイル  | PingCAPクリニックによるデータ収集のパラメータ |
| :------------------------------- | :------------- | :------------------------- |
| カーネルログ                           | `dmesg.log`    | `--include=system`         |
| システムとハードウェアの基本情報                 | `insight.json` | `--include=system`         |
| `/etc/security/limits.conf`系統の内容 | `limits.conf`  | `--include=system`         |
| カーネルパラメータ一覧                      | `sysctl.conf`  | `--include=system`         |
| `ss`コマンドの出力であるソケット システム情報        | `ss.txt`       | `--include=system`         |
