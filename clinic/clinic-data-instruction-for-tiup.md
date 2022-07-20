---
title: PingCAP Clinic Diagnostic Data
summary: Learn what diagnostic data can be collected by PingCAP Clinic Diagnostic Service from the TiDB and DM clusters deployed using TiUP.
---

# PingCAPクリニックの診断データ {#pingcap-clinic-diagnostic-data}

このドキュメントでは、TiUPを使用して展開されたTiDBおよびDMクラスターからPingCAP PingCAPクリニック Diagnostic Service（PingCAPクリニック）によって収集できる診断データの種類について説明します。また、このドキュメントには、各データタイプに対応するデータ収集のパラメータがリストされています。コマンドを[Diagクライアント（Diag）を使用してデータを収集する](/clinic/clinic-user-guide-for-tiup.md)に実行すると、収集するデータの種類に応じて、必要なパラメーターをコマンドに追加できます。

PingCAPクリニックによって収集された診断データは、クラスタの問題のトラブルシューティングに**のみ**使用されます。

クラウドにデプロイされた診断サービスであるClinicServerは、データの保存場所に応じて2つの独立したサービスを提供します。

-   [米国のクリニックサーバー](https://clinic.pingcap.com) ：収集したデータを米国のクリニックサーバーにアップロードすると、データはAWSUSリージョンのPingCAPによってデプロイされたAmazonS3サービスに保存されます。 PingCAPは厳格なデータアクセスポリシーを使用しており、許可されたテクニカルサポートのみがデータにアクセスできます。
-   [中国本土のクリニックサーバー](https://clinic.pingcap.com.cn) ：収集したデータを中国本土のクリニックサーバーにアップロードすると、データは中国（北京）地域のPingCAPによってデプロイされたAmazonS3サービスに保存されます。 PingCAPは厳格なデータアクセスポリシーを使用しており、許可されたテクニカルサポートのみがデータにアクセスできます。

## TiDBクラスター {#tidb-clusters}

このセクションでは、TiUPを使用してデプロイされたTiDBクラスターからDiagが収集できる診断データのタイプをリストします。

### TiDBクラスタ情報 {#tidb-cluster-information}

| データ・タイプ            | エクスポートされたファイル  | PingCAPクリニックによるデータ収集のパラメータ |
| :----------------- | :------------- | :------------------------- |
| クラスタIDを含むクラスタの基本情報 | `cluster.json` | データは、デフォルトで実行ごとに収集されます。    |
| クラスタの詳細情報          | `meta.yaml`    | データは、デフォルトで実行ごとに収集されます。    |

### TiDB診断データ {#tidb-diagnostic-data}

| データ・タイプ                        | エクスポートされたファイル         | PingCAPクリニックによるデータ収集のパラメータ |
| :----------------------------- | :-------------------- | :------------------------- |
| ログ                             | `tidb.log`            | `--include=log`            |
| エラーログ                          | `tidb_stderr.log`     | `--include=log`            |
| 遅いログ                           | `tidb_slow_query.log` | `--include=log`            |
| Configuration / コンフィグレーションファイル | `tidb.toml`           | `--include=config`         |
| リアルタイム構成                       | `config.json`         | `--include=config`         |

### TiKV診断データ {#tikv-diagnostic-data}

| データ・タイプ                        | エクスポートされたファイル     | PingCAPクリニックによるデータ収集のパラメータ |
| :----------------------------- | :---------------- | :------------------------- |
| ログ                             | `tikv.log`        | `--include=log`            |
| エラーログ                          | `tikv_stderr.log` | `--include=log`            |
| Configuration / コンフィグレーションファイル | `tikv.toml`       | `--include=config`         |
| リアルタイム構成                       | `config.json`     | `--include=config`         |

### PD診断データ {#pd-diagnostic-data}

| データ・タイプ                                                                     | エクスポートされたファイル         | PingCAPクリニックによるデータ収集のパラメータ |
| :-------------------------------------------------------------------------- | :-------------------- | :------------------------- |
| ログ                                                                          | `pd.log`              | `--include=log`            |
| エラーログ                                                                       | `pd_stderr.log`       | `--include=log`            |
| Configuration / コンフィグレーションファイル                                              | `pd.toml`             | `--include=config`         |
| リアルタイム構成                                                                    | `config.json`         | `--include=config`         |
| コマンドの出力`tiup ctl pd -u http://${pd IP}:${PORT} store`                       | `store.json`          | `--include=config`         |
| コマンドの出力`tiup ctl pd -u http://${pd IP}:${PORT} config placement-rules show` | `placement-rule.json` | `--include=config`         |

### TiFlash診断データ {#tiflash-diagnostic-data}

| データ・タイプ                        | エクスポートされたファイル                                                     | PingCAPクリニックによるデータ収集のパラメータ |
| :----------------------------- | :---------------------------------------------------------------- | :------------------------- |
| ログ                             | `tiflash.log`                                                     | `--include=log`            |
| エラーログ                          | `tiflash_stderr.log`                                              | `--include=log`            |
| Configuration / コンフィグレーションファイル | `tiflash-learner.toml` `tiflash-preprocessed.toml` `tiflash.toml` | `--include=config`         |
| リアルタイム構成                       | `config.json`                                                     | `--include=config`         |

### TiCDC診断データ {#ticdc-diagnostic-data}

| データ・タイプ                        | エクスポートされたファイル                                                             | PingCAPクリニックによるデータ収集のパラメータ                    |
| :----------------------------- | :------------------------------------------------------------------------ | :-------------------------------------------- |
| ログ                             | `ticdc.log`                                                               | `--include=log`                               |
| エラーログ                          | `ticdc_stderr.log`                                                        | `--include=log`                               |
| Configuration / コンフィグレーションファイル | `ticdc.toml`                                                              | `--include=config`                            |
| デバッグデータ                        | `info.txt` `status.txt` `changefeeds.txt` `captures.txt` `processors.txt` | `--include=debug` （Diagはデフォルトではこのデータ型を収集しません） |

### プロメテウスモニタリングデータ {#prometheus-monitoring-data}

| データ・タイプ     | エクスポートされたファイル        | PingCAPクリニックによるデータ収集のパラメータ |
| :---------- | :------------------- | :------------------------- |
| すべての指標データ   | `{metric_name}.json` | `--include=monitor`        |
| すべてのアラートデータ | `alerts.json`        | `--include=monitor`        |

### TiDBシステム変数 {#tidb-system-variables}

| データ・タイプ    | エクスポートされたファイル          | PingCAPクリニックによるデータ収集のパラメータ                                                           |
| :--------- | :--------------------- | :----------------------------------------------------------------------------------- |
| TiDBシステム変数 | `mysql.tidb.csv`       | `--include=db_vars` （Diagはデフォルトではこのデータ型を収集しません。このデータ型を収集する必要がある場合は、データベースの資格情報が必要です） |
|            | `global_variables.csv` | `--include=db_vars` （Diagはデフォルトではこのデータ型を収集しません）                                      |

### クラスタノードのシステム情報 {#system-information-of-the-cluster-node}

| データ・タイプ                        | エクスポートされたファイル  | PingCAPクリニックによるデータ収集のパラメータ |
| :----------------------------- | :------------- | :------------------------- |
| カーネルログ                         | `dmesg.log`    | `--include=system`         |
| システムとハードウェアの基本情報               | `insight.json` | `--include=system`         |
| `/etc/security/limits.conf`の内容 | `limits.conf`  | `--include=system`         |
| カーネルパラメータのリスト                  | `sysctl.conf`  | `--include=system`         |
| `ss`コマンドの出力であるソケットシステム情報       | `ss.txt`       | `--include=system`         |

## DMクラスター {#dm-clusters}

このセクションでは、TiUPを使用してデプロイされたDMクラスターからDiagが収集できる診断データのタイプをリストします。

### DMクラスタ情報 {#dm-cluster-information}

| データ・タイプ            | エクスポートされたファイル  | PingCAPクリニックによるデータ収集のパラメータ |
| :----------------- | :------------- | :------------------------- |
| クラスタIDを含むクラスタの基本情報 | `cluster.json` | データは、デフォルトで実行ごとに収集されます。    |
| クラスタの詳細情報          | `meta.yaml`    | データは、デフォルトで実行ごとに収集されます。    |

### dm-master診断データ {#dm-master-diagnostic-data}

| データ・タイプ                        | エクスポートされたファイル          | PingCAPクリニックによるデータ収集のパラメータ |
| :----------------------------- | :--------------------- | :------------------------- |
| ログ                             | `m-master.log`         | `--include=log`            |
| エラーログ                          | `dm-master_stderr.log` | `--include=log`            |
| Configuration / コンフィグレーションファイル | `dm-master.toml`       | `--include=config`         |

### dm-worker診断データ {#dm-worker-diagnostic-data}

| データ・タイプ                        | エクスポートされたファイル          | PingCAPクリニックによるデータ収集のパラメータ |
| :----------------------------- | :--------------------- | :------------------------- |
| ログ                             | `dm-worker.log`        | `--include=log`            |
| エラーログ                          | `dm-worker_stderr.log` | `--include=log`            |
| Configuration / コンフィグレーションファイル | `dm-work.toml`         | `--include=config`         |

### プロメテウスモニタリングデータ {#prometheus-monitoring-data}

| データ・タイプ     | エクスポートされたファイル        | PingCAPクリニックによるデータ収集のパラメータ |
| :---------- | :------------------- | :------------------------- |
| すべての指標データ   | `{metric_name}.json` | `--include=monitor`        |
| すべてのアラートデータ | `alerts.json`        | `--include=monitor`        |

### クラスタノードのシステム情報 {#system-information-of-the-cluster-node}

| データ・タイプ                            | エクスポートされたファイル  | PingCAPクリニックによるデータ収集のパラメータ |
| :--------------------------------- | :------------- | :------------------------- |
| カーネルログ                             | `dmesg.log`    | `--include=system`         |
| システムとハードウェアの基本情報                   | `insight.json` | `--include=system`         |
| `/etc/security/limits.conf`システムの内容 | `limits.conf`  | `--include=system`         |
| カーネルパラメータのリスト                      | `sysctl.conf`  | `--include=system`         |
| `ss`コマンドの出力であるソケットシステム情報           | `ss.txt`       | `--include=system`         |
