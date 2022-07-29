---
title: TiDB Binlog Deployment Topology
summary: Learn the deployment topology of TiDB Binlog based on the minimal TiDB topology.
---

# Binlogデプロイメントトポロジ {#tidb-binlog-deployment-topology}

このドキュメントでは、最小のTiDBトポロジに基づく[TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md)の展開トポロジについて説明します。

TiDB Binlogは、増分データを複製するために広く使用されているコンポーネントです。ほぼリアルタイムのバックアップとレプリケーションを提供します。

## トポロジー情報 {#topology-information}

| 実例      | カウント | 物理マシン構成        | 知財                                   | Configuration / コンフィグレーション                                                                              |
| :------ | :--- | :------------- | :----------------------------------- | :------------------------------------------------------------------------------------------------------ |
| TiDB    | 3    | 16 VCore 32 GB | 10.0.1.1<br/> 10.0.1.2<br/> 10.0.1.3 | デフォルトのポート構成。<br/> `enable_binlog`を有効にします。<br/> `ignore-error`を有効にする                                     |
| PD      | 3    | 4 VCore 8 GB   | 10.0.1.4<br/> 10.0.1.5<br/> 10.0.1.6 | デフォルトのポート構成                                                                                             |
| TiKV    | 3    | 16 VCore 32 GB | 10.0.1.7<br/> 10.0.1.8<br/> 10.0.1.9 | デフォルトのポート構成                                                                                             |
| Pump    | 3    | 8 VCore 16GB   | 10.0.1.1<br/> 10.0.1.7<br/> 10.0.1.8 | デフォルトのポート構成。<br/> GC時間を7日に設定します                                                                         |
| Drainer | 1    | 8 VCore 16GB   | 10.0.1.12                            | デフォルトのポート構成。<br/>デフォルトの初期化commitTS-1を最新のタイムスタンプとして設定します。<br/>ダウンストリームターゲットTiDBを`10.0.1.12:4000`として構成します |

### トポロジテンプレート {#topology-templates}

-   [TiDB Binlogトポロジの単純なテンプレート（ダウンストリームタイプとして`mysql`を使用）](https://github.com/pingcap/docs/blob/master/config-templates/simple-tidb-binlog.yaml)
-   [TiDB Binlogトポロジの単純なテンプレート（ダウンストリームタイプとして`file`を使用）](https://github.com/pingcap/docs/blob/master/config-templates/simple-file-binlog.yaml)
-   [Binlogトポロジの複雑なテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-tidb-binlog.yaml)

上記のTiDBクラスタトポロジファイルの構成項目の詳細については、 [TiUPを使用してTiDBを展開するためのトポロジConfiguration / コンフィグレーションファイル](/tiup/tiup-cluster-topology-reference.md)を参照してください。

### 重要なパラメータ {#key-parameters}

トポロジ構成テンプレートの主要なパラメーターは次のとおりです。

-   `server_configs.tidb.binlog.enable: true`

    -   binlogサービスを有効にします。
    -   デフォルト値： `false` 。

-   `server_configs.tidb.binlog.ignore-error: true`

    -   高可用性シナリオでは、この構成を有効にすることをお勧めします。
    -   `true`に設定すると、エラーが発生すると、TiDBはbinlogへのデータの書き込みを停止し、 `tidb_server_critical_error_total`の監視メトリックの値に`1`を追加します。
    -   `false`に設定すると、TiDBがbinlogへのデータの書き込みに失敗すると、TiDBサービス全体が停止します。

-   `drainer_servers.config.syncer.db-type`

    Binlogのダウンストリームタイプ。現在、 `mysql` 、および`kafka`がサポートさ`file`てい`tidb` 。

-   `drainer_servers.config.syncer.to`

    Binlogのダウンストリーム構成。異なる`db-type`に応じて、この構成項目を使用して、ダウンストリーム・データベースの接続パラメーター、Kafkaの接続パラメーター、およびファイル保存パスを構成できます。詳しくは[BinlogConfiguration / コンフィグレーションファイル](/tidb-binlog/tidb-binlog-configuration-file.md#syncerto)をご覧ください。

> **ノート：**
>
> -   構成ファイルテンプレートを編集するときに、カスタムポートまたはディレクトリが必要ない場合は、IPのみを変更します。
> -   構成ファイルに`tidb`人のユーザーを手動で作成する必要はありません。 TiUPクラスタコンポーネントは、ターゲットマシン上に`tidb`のユーザーを自動的に作成します。ユーザーをカスタマイズすることも、ユーザーと制御マシンの一貫性を保つこともできます。
> -   展開ディレクトリを相対パスとして構成すると、クラスタはユーザーのホームディレクトリに展開されます。
