---
title: TiDB Binlog Deployment Topology
summary: 最小限の TiDB トポロジに基づいた TiDB Binlogのデプロイメント トポロジを学習します。
---

# TiDBBinlog展開トポロジ {#tidb-binlog-deployment-topology}

このドキュメントでは、最小限の TiDB トポロジに基づく[TiDBBinlog](/tidb-binlog/tidb-binlog-overview.md)のデプロイメント トポロジについて説明します。

TiDB Binlog は、増分データのレプリケーションに広く使用されているコンポーネントです。ほぼリアルタイムのバックアップとレプリケーションを提供します。

## トポロジ情報 {#topology-information}

| 実例      | カウント | 物理マシン構成        | IP                                   | コンフィグレーション                                                                                        |
| :------ | :--- | :------------- | :----------------------------------- | :------------------------------------------------------------------------------------------------ |
| ティビ     | 3    | 16 VCore 32 GB | 10.0.1.1<br/> 10.0.1.2<br/> 10.0.1.3 | デフォルトのポート構成。<br/> `enable_binlog`有効にする;<br/>有効`ignore-error`                                      |
| PD      | 3    | 4 VCore 8 GB   | 10.0.1.4<br/> 10.0.1.5<br/> 10.0.1.6 | デフォルトのポート構成                                                                                       |
| ティクヴ    | 3    | 16 VCore 32 GB | 10.0.1.7<br/> 10.0.1.8<br/> 10.0.1.9 | デフォルトのポート構成                                                                                       |
| Pump    | 3    | 8 VCore 16GB   | 10.0.1.1<br/> 10.0.1.7<br/> 10.0.1.8 | デフォルトのポート構成。<br/> GC時間を7日間に設定する                                                                   |
| Drainer | 1    | 8 VCore 16GB   | 10.0.1.12                            | デフォルトのポート構成。<br/>デフォルトの初期化 commitTS -1 を最新のタイムスタンプとして設定します。<br/>下流ターゲットTiDBを`10.0.1.12:4000`に設定する |

### トポロジーテンプレート {#topology-templates}

-   [TiDB Binlogトポロジのシンプルなテンプレート (ダウンストリーム タイプとして`mysql`を使用)](https://github.com/pingcap/docs/blob/master/config-templates/simple-tidb-binlog.yaml)
-   [TiDB Binlogトポロジのシンプルなテンプレート (ダウンストリーム タイプとして`file`を使用)](https://github.com/pingcap/docs/blob/master/config-templates/simple-file-binlog.yaml)
-   [TiDB Binlogトポロジの複雑なテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-tidb-binlog.yaml)

上記の TiDB クラスタ トポロジ ファイルの構成項目の詳細については、 [TiUPを使用して TiDB をデプロイするためのトポロジコンフィグレーションファイル](/tiup/tiup-cluster-topology-reference.md)を参照してください。

### 主なパラメータ {#key-parameters}

トポロジ構成テンプレートの主なパラメータは次のとおりです。

-   `server_configs.tidb.binlog.enable: true`

    -   binlogサービスを有効にします。
    -   デフォルト値: `false` 。

-   `server_configs.tidb.binlog.ignore-error: true`

    -   高可用性のシナリオでは、この構成を有効にすることをお勧めします。
    -   `true`に設定すると、エラーが発生すると、TiDB はbinlogへのデータの書き込みを停止し、監視メトリック`tidb_server_critical_error_total`の値に`1`を追加します。
    -   `false`に設定すると、TiDB がbinlogへのデータの書き込みに失敗すると、TiDB サービス全体が停止します。

-   `drainer_servers.config.syncer.db-type`

    TiDB Binlogのダウンストリーム タイプ。現在、 `mysql` 、 `tidb` 、 `kafka` 、 `file`がサポートされています。

-   `drainer_servers.config.syncer.to`

    TiDB Binlogのダウンストリーム構成。 `db-type`に応じて、この構成項目を使用して、ダウンストリーム データベースの接続パラメータ、Kafka の接続パラメータ、およびファイル保存パスを構成できます。 詳細については、 [TiDBBinlogコンフィグレーションファイル](/tidb-binlog/tidb-binlog-configuration-file.md#syncerto)を参照してください。

> **注記：**
>
> -   構成ファイル テンプレートを編集するときに、カスタム ポートまたはディレクトリが必要ない場合は、IP のみを変更します。
> -   構成ファイルで`tidb`ユーザーを手動で作成する必要はありません。TiUP クラスターコンポーネントは、ターゲット マシンに`tidb`ユーザーを自動的に作成します。ユーザーをカスタマイズすることも、ユーザーをコントロール マシンと一致させることもできます。
> -   デプロイメント ディレクトリを相対パスとして構成すると、クラスターはユーザーのホーム ディレクトリにデプロイされます。
