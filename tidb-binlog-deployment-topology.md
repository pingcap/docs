---
title: TiDB Binlog Deployment Topology
summary: Learn the deployment topology of TiDB Binlog based on the minimal TiDB topology.
---

# TiDB Binlog展開トポロジ {#tidb-binlog-deployment-topology}

このドキュメントでは、最小限の TiDB トポロジに基づく[TiDBBinlog](/tidb-binlog/tidb-binlog-overview.md)の展開トポロジについて説明します。

TiDB Binlog は、増分データを複製するために広く使用されているコンポーネントです。ほぼリアルタイムのバックアップとレプリケーションを提供します。

## トポロジ情報 {#topology-information}

| 実例      | カウント | 物理マシン構成       | 知財                                   | コンフィグレーション                                                                                                     |
| :------ | :--- | :------------ | :----------------------------------- | :------------------------------------------------------------------------------------------------------------- |
| TiDB    | 3    | 16 仮想コア 32 GB | 10.0.1.1<br/> 10.0.1.2<br/> 10.0.1.3 | デフォルトのポート構成。<br/> `enable_binlog`を有効にします。<br/> `ignore-error`を有効にする                                            |
| PD      | 3    | 4 仮想コア 8 GB   | 10.0.1.4<br/> 10.0.1.5<br/> 10.0.1.6 | デフォルトのポート構成                                                                                                    |
| TiKV    | 3    | 16 仮想コア 32 GB | 10.0.1.7<br/> 10.0.1.8<br/> 10.0.1.9 | デフォルトのポート構成                                                                                                    |
| Pump    | 3    | 8 Vコア 16GB    | 10.0.1.1<br/> 10.0.1.7<br/> 10.0.1.8 | デフォルトのポート構成。<br/> GC 時間を 7 日に設定する                                                                              |
| Drainer | 1    | 8 Vコア 16GB    | 10.0.1.12                            | デフォルトのポート構成。<br/>デフォルトの初期化 commitTS -1 を最新のタイムスタンプとして設定します。<br/>ダウンストリーム ターゲット TiDB を`10.0.1.12:4000`として構成します。 |

### トポロジ テンプレート {#topology-templates}

-   [TiDB Binlogトポロジの単純なテンプレート (ダウンストリーム タイプとして`mysql`を使用)](https://github.com/pingcap/docs/blob/master/config-templates/simple-tidb-binlog.yaml)
-   [TiDB Binlogトポロジの単純なテンプレート (ダウンストリーム タイプとして`file`を使用)](https://github.com/pingcap/docs/blob/master/config-templates/simple-file-binlog.yaml)
-   [TiDB Binlogトポロジの複雑なテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-tidb-binlog.yaml)

上記の TiDB クラスター トポロジ ファイルの構成項目の詳細な説明については、 [TiUPを使用して TiDB をデプロイするためのトポロジコンフィグレーションファイル](/tiup/tiup-cluster-topology-reference.md)を参照してください。

### 主なパラメータ {#key-parameters}

トポロジ構成テンプレートの主要なパラメーターは次のとおりです。

-   `server_configs.tidb.binlog.enable: true`

    -   binlogサービスを有効にします。
    -   デフォルト値: `false` 。

-   `server_configs.tidb.binlog.ignore-error: true`

    -   高可用性シナリオでは、この構成を有効にすることをお勧めします。
    -   `true`に設定すると、エラーが発生すると、TiDB はbinlogへのデータの書き込みを停止し、 `tidb_server_critical_error_total`モニタリング メトリックの値に`1`を追加します。
    -   `false`に設定すると、TiDB がbinlogへのデータの書き込みに失敗すると、TiDB サービス全体が停止します。

-   `drainer_servers.config.syncer.db-type`

    TiDB Binlogのダウンストリーム タイプ。現在、 `mysql` 、 `tidb` 、 `kafka` 、および`file`がサポートされています。

-   `drainer_servers.config.syncer.to`

    TiDB Binlogのダウンストリーム構成。異なる`db-type`に応じて、この構成アイテムを使用して、ダウンストリーム データベースの接続パラメーター、Kafka の接続パラメーター、およびファイル保存パスを構成できます。詳細は[TiDB Binlogコンフィグレーションファイル](/tidb-binlog/tidb-binlog-configuration-file.md#syncerto)を参照してください。

> **ノート：**
>
> -   構成ファイル テンプレートを編集するときに、カスタム ポートまたはディレクトリが必要ない場合は、IP のみを変更します。
> -   構成ファイルで`tidb`ユーザーを手動で作成する必要はありません。 TiUPクラスターコンポーネントは、ターゲット マシンに`tidb`ユーザーを自動的に作成します。ユーザーをカスタマイズしたり、ユーザーと制御マシンとの一貫性を保つことができます。
> -   展開ディレクトリを相対パスとして構成すると、クラスターはユーザーのホーム ディレクトリに展開されます。
