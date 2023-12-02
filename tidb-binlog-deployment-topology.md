---
title: TiDB Binlog Deployment Topology
summary: Learn the deployment topology of TiDB Binlog based on the minimal TiDB topology.
---

# TiDBBinlog展開トポロジ {#tidb-binlog-deployment-topology}

このドキュメントでは、最小の TiDB トポロジに基づいた[TiDBBinlog](/tidb-binlog/tidb-binlog-overview.md)の展開トポロジについて説明します。

TiDB Binlog は、増分データをレプリケートするために広く使用されているコンポーネントです。ほぼリアルタイムのバックアップとレプリケーションを提供します。

## トポロジ情報 {#topology-information}

| 実例      | カウント | 物理マシンの構成      | IP                                   | コンフィグレーション                                                                                                     |
| :------ | :--- | :------------ | :----------------------------------- | :------------------------------------------------------------------------------------------------------------- |
| TiDB    | 3    | 16 仮想コア 32 GB | 10.0.1.1<br/> 10.0.1.2<br/> 10.0.1.3 | デフォルトのポート構成。<br/> `enable_binlog`を有効にする。<br/>有効化`ignore-error`                                                 |
| PD      | 3    | 4仮想コア8GB      | 10.0.1.4<br/> 10.0.1.5<br/> 10.0.1.6 | デフォルトのポート構成                                                                                                    |
| TiKV    | 3    | 16 仮想コア 32 GB | 10.0.1.7<br/> 10.0.1.8<br/> 10.0.1.9 | デフォルトのポート構成                                                                                                    |
| Pump    | 3    | 8仮想コア16GB     | 10.0.1.1<br/> 10.0.1.7<br/> 10.0.1.8 | デフォルトのポート構成。<br/> GC 時間を 7 日に設定する                                                                              |
| Drainer | 1    | 8仮想コア16GB     | 10.0.1.12                            | デフォルトのポート構成。<br/>デフォルトの初期化 commitTS -1 を最新のタイムスタンプとして設定します。<br/>ダウンストリーム ターゲット TiDB を`10.0.1.12:4000`として構成します。 |

### トポロジテンプレート {#topology-templates}

-   [TiDB Binlogトポロジの単純なテンプレート (ダウンストリーム タイプとして`mysql`を使用)](https://github.com/pingcap/docs/blob/master/config-templates/simple-tidb-binlog.yaml)
-   [TiDB Binlogトポロジの単純なテンプレート (ダウンストリーム タイプとして`file`を使用)](https://github.com/pingcap/docs/blob/master/config-templates/simple-file-binlog.yaml)
-   [TiDB Binlogトポロジの複雑なテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-tidb-binlog.yaml)

上記の TiDB クラスター トポロジー ファイルの構成項目の詳細な説明については、 [TiUPを使用して TiDB を展開するためのトポロジコンフィグレーションファイル](/tiup/tiup-cluster-topology-reference.md)を参照してください。

### 主要パラメータ {#key-parameters}

トポロジ構成テンプレートの主要なパラメータは次のとおりです。

-   `server_configs.tidb.binlog.enable: true`

    -   binlogサービスを有効にします。
    -   デフォルト値: `false` 。

-   `server_configs.tidb.binlog.ignore-error: true`

    -   高可用性シナリオでは、この構成を有効にすることをお勧めします。
    -   `true`に設定すると、エラーが発生すると、TiDB はbinlogへのデータの書き込みを停止し、 `tidb_server_critical_error_total`監視メトリックの値に`1`を追加します。
    -   `false`に設定すると、TiDB がbinlogへのデータの書き込みに失敗すると、TiDB サービス全体が停止します。

-   `drainer_servers.config.syncer.db-type`

    TiDB Binlogのダウンストリーム タイプ。現在、 `mysql` 、 `tidb` 、 `kafka` 、および`file`がサポートされています。

-   `drainer_servers.config.syncer.to`

    TiDB Binlogのダウンストリーム構成。さまざまな`db-type`に応じて、この構成アイテムを使用して、ダウンストリーム データベースの接続パラメーター、Kafka の接続パラメーター、およびファイルの保存パスを構成できます。詳細は[TiDBBinlogコンフィグレーションファイル](/tidb-binlog/tidb-binlog-configuration-file.md#syncerto)を参照してください。

> **注記：**
>
> -   構成ファイル テンプレートを編集するときに、カスタム ポートまたはディレクトリが必要ない場合は、IP のみを変更します。
> -   構成ファイルに`tidb`ユーザーを手動で作成する必要はありません。 TiUPクラスターコンポーネントは、ターゲット マシン上に`tidb`のユーザーを自動的に作成します。ユーザーをカスタマイズしたり、ユーザーと制御マシンの一貫性を保つことができます。
> -   デプロイメント ディレクトリを相対パスとして構成すると、クラスターはユーザーのホーム ディレクトリにデプロイされます。
