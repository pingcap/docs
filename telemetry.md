---
title: Telemetry
summary: テレメトリ機能と、その機能を無効にしてそのステータスを表示する方法について学習します。
---

# テレメトリー {#telemetry}

テレメトリを有効にすると、TiDB、 TiUP 、および TiDB ダッシュボードは使用状況情報を収集し、その情報を PingCAP と共有して、製品の改善方法の理解に役立てます。たとえば、この使用状況情報は、新機能の優先順位付けに役立ちます。

> **注記：**
>
> -   2023 年 2 月 20 日以降、v6.6.0 を含む TiDB および TiDB Dashboard の新しいバージョンでは、テレメトリ機能がデフォルトで無効になっており、使用状況情報は収集されず、PingCAP と共有されません。これらのバージョンにアップグレードする前に、クラスターがデフォルトのテレメトリ構成を使用している場合、アップグレード後にテレメトリ機能が無効になります。特定のバージョンについては、 [TiDB リリース タイムライン](/releases/release-timeline.md)参照してください。
> -   v1.11.3 以降、新しく導入されたTiUPではテレメトリ機能がデフォルトで無効になっており、使用状況情報は収集されません。v1.11.3 より前のバージョンのTiUPから v1.11.3 以降のバージョンにアップグレードした場合、テレメトリ機能はアップグレード前と同じ状態を維持します。

## 共有されるものは何ですか? {#what-is-shared}

以下のセクションでは、各コンポーネントの共有される使用情報について詳しく説明します。共有される使用詳細は、時間の経過とともに変更される可能性があります。これらの変更 (ある場合) は[リリースノート](/releases/release-notes.md)で発表されます。

> **注記：**
>
> **いずれの**場合も、TiDB クラスターに保存されているユーザー データは共有されませ**ん**。5 [PingCAP プライバシーポリシー](https://pingcap.com/privacy-policy)参照してください。

### ティビ {#tidb}

TiDB でテレメトリ収集機能が有効になっている場合、TiDB クラスターは 6 時間ごとに使用状況の詳細を収集します。これらの使用状況の詳細には、次のものが含まれますが、これらに限定されません。

-   ランダムに生成されたテレメトリ ID。
-   ハードウェア (CPU、メモリ、ディスク) のサイズ、TiDB コンポーネントのバージョン、OS 名などのデプロイメント特性。
-   クエリ要求の数や期間など、システム内のクエリ要求のステータス。
-   コンポーネントの使用状況。たとえば、非同期コミット機能が使用されているかどうかなど。
-   TiDB テレメトリ データ送信者の仮名 IP アドレス。

PingCAP に共有された使用状況情報の全内容を表示するには、次の SQL ステートメントを実行します。

```sql
ADMIN SHOW TELEMETRY;
```

### TiDBダッシュボード {#tidb-dashboard}

TiDB ダッシュボードのテレメトリ収集機能が有効になっている場合、次のような (ただしこれらに限定されない) TiDB ダッシュボード Web UI の使用状況の詳細が共有されます。

-   ランダムに生成されたテレメトリ ID。
-   ユーザーがアクセスした TiDB ダッシュボード Web ページの名前などのユーザー操作情報。
-   ブラウザ名、OS 名、画面解像度などのブラウザと OS の情報。

PingCAP に共有された使用情報の全内容を表示するには、 [Chrome DevTools のネットワーク アクティビティ インスペクター](https://developers.google.com/web/tools/chrome-devtools/network)または[Firefox 開発ツールのネットワーク モニター](https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor)使用します。

### TiUP {#tiup}

TiUPでテレメトリ収集機能が有効になっている場合、次のようなTiUPの使用状況の詳細が共有されます (ただし、これらに限定されません)。

-   ランダムに生成されたテレメトリ ID。
-   実行が成功したかどうかや実行時間などのTiUPコマンドの実行ステータス。
-   ハードウェアのサイズ、TiDB コンポーネントのバージョン、変更されたデプロイメント構成名などのデプロイメント特性。

PingCAP に共有された使用情報の全内容を表示するには、 TiUPコマンドを実行するときに`TIUP_CLUSTER_DEBUG=enable`環境変数を設定します。例:

```shell
TIUP_CLUSTER_DEBUG=enable tiup cluster list
```

### ティスパーク {#tispark}

> **注記：**
>
> v3.0.3 以降、TiSpark ではテレメトリ収集がデフォルトで無効になっており、使用状況情報は収集されず、PingCAP と共有されません。

TiSpark のテレメトリ収集機能が有効になっている場合、Spark モジュールは TiSpark の使用状況の詳細 (以下を含むがこれらに限定されない) を共有します。

-   ランダムに生成されたテレメトリ ID。
-   読み取りエンジンやストリーミング読み取りが有効かどうかなど、TiSpark の一部の構成情報。
-   TiSpark が配置されているノードのマシン ハードウェア情報、OS 情報、コンポーネントバージョン番号などのクラスタ展開情報。

Spark ログに収集された TiSpark の使用状況情報を表示できます。Spark ログ レベルを INFO 以下に設定できます。例:

```shell
cat {spark.log} | grep Telemetry report | tail -n 1
```

## テレメトリを無効にする {#disable-telemetry}

### デプロイメント時に TiDB テレメトリを無効にする {#disable-tidb-telemetry-at-deployment}

既存の TiDB クラスターでテレメトリが有効になっている場合は、各 TiDB インスタンスで[`enable-telemetry = false`](/tidb-configuration-file.md#enable-telemetry-new-in-v402)構成して、そのインスタンスでの TiDB テレメトリ収集を無効にすることができます。これは、クラスターを再起動するまで有効になりません。

さまざまな展開ツールでテレメトリを無効にする詳細な手順を以下に示します。

<details><summary>バイナリ展開</summary>

次の内容の構成ファイル`tidb_config.toml`を作成します。

```toml
enable-telemetry = false
```

上記の構成ファイルを有効にするには、TiDB を起動するときに`--config=tidb_config.toml`コマンドライン パラメータを指定します。

詳細は[TiDBコンフィグレーションオプション](/command-line-flags-for-tidb-configuration.md#--config)と[TiDBコンフィグレーションファイル](/tidb-configuration-file.md#enable-telemetry-new-in-v402)ご覧ください。

</details>

<details><summary>TiUP Playgroundを使用したデプロイメント</summary>

次の内容の構成ファイル`tidb_config.toml`を作成します。

```toml
enable-telemetry = false
```

TiUP Playground を起動するときに、上記の構成ファイルを有効にするには、 `--db.config tidb_config.toml`コマンドライン パラメータを指定します。例:

```shell
tiup playground --db.config tidb_config.toml
```

詳細は[ローカル TiDBクラスタを迅速にデプロイ](/tiup/tiup-playground.md)参照。

</details>

<details><summary>TiUP クラスタを使用したデプロイメント</summary>

デプロイメント トポロジ ファイル`topology.yaml`を変更して、次のコンテンツを追加します。

```yaml
server_configs:
  tidb:
    enable-telemetry: false
```

</details>

<details><summary>TiDB Operatorによる Kubernetes へのデプロイ</summary>

`spec.tidb.config.enable-telemetry: false` in `tidb-cluster.yaml`または TidbCluster カスタム リソースを構成します。

詳細は[Kubernetes にTiDB Operatorをデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-tidb-operator)参照。

> **注記：**
>
> この構成項目を有効にするには、 TiDB Operator v1.1.3 以降が必要です。

</details>

### デプロイされた TiDB クラスターの TiDB テレメトリを無効にする {#disable-tidb-telemetry-for-deployed-tidb-clusters}

既存の TiDB クラスターでは、システム変数[`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-new-in-v402)を変更して、TiDB テレメトリ収集を動的に無効にすることもできます。

```sql
SET GLOBAL tidb_enable_telemetry = 0;
```

> **注記：**
>
> テレメトリを無効にすると、構成ファイルはシステム変数よりも優先されます。つまり、構成ファイルによってテレメトリの収集が無効にされると、システム変数の値は無視されます。

### TiDBダッシュボードテレメトリを無効にする {#disable-tidb-dashboard-telemetry}

すべての PD インスタンスで TiDB ダッシュボード テレメトリ収集を無効にするには、 [`dashboard.enable-telemetry = false`](/pd-configuration-file.md#enable-telemetry)設定します。設定を有効にするには、実行中のクラスターを再起動する必要があります。

さまざまな展開ツールのテレメトリを無効にする詳細な手順を以下に示します。

<details><summary>バイナリ展開</summary>

次の内容の構成ファイル`pd_config.toml`を作成します。

```toml
[dashboard]
enable-telemetry = false
```

PD を有効にするには、起動時に`--config=pd_config.toml`コマンドライン パラメータを指定します。

詳細は[PDコンフィグレーションフラグ](/command-line-flags-for-pd-configuration.md#--config)と[PDコンフィグレーションファイル](/pd-configuration-file.md#enable-telemetry)ご覧ください。

</details>

<details><summary>TiUP Playgroundを使用したデプロイメント</summary>

次の内容の構成ファイル`pd_config.toml`を作成します。

```toml
[dashboard]
enable-telemetry = false
```

TiUP Playground を起動するときに、有効にする`--pd.config pd_config.toml`コマンドライン パラメータを指定します。例:

```shell
tiup playground --pd.config pd_config.toml
```

詳細は[ローカル TiDBクラスタを迅速にデプロイ](/tiup/tiup-playground.md)参照。

</details>

<details><summary>TiUP クラスタを使用したデプロイメント</summary>

デプロイメント トポロジ ファイル`topology.yaml`を変更して、次のコンテンツを追加します。

```yaml
server_configs:
  pd:
    dashboard.enable-telemetry: false
```

</details>

<details><summary>TiDB Operatorによる Kubernetes へのデプロイ</summary>

`spec.pd.config.dashboard.enable-telemetry: false` in `tidb-cluster.yaml`または TidbCluster カスタム リソースを構成します。

詳細は[Kubernetes にTiDB Operatorをデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-tidb-operator)参照。

> **注記：**
>
> この構成項目を有効にするには、 TiDB Operator v1.1.3 以降が必要です。

</details>

### TiUPテレメトリを無効にする {#disable-tiup-telemetry}

TiUPテレメトリ収集を無効にするには、次のコマンドを実行します。

```shell
tiup telemetry disable
```

## テレメトリステータスを確認する {#check-telemetry-status}

TiDB テレメトリの場合、次の SQL ステートメントを実行してテレメトリのステータスを確認します。

```sql
ADMIN SHOW TELEMETRY;
```

実行結果の`DATA_PREVIEW`列目が空の場合、TiDB テレメトリは無効です。空でない場合は、TiDB テレメトリが有効です。また、 `LAST_STATUS`列目から、以前に使用状況情報が共有された時期や、共有が成功したかどうかも確認できます。

TiUPテレメトリの場合、次のコマンドを実行してテレメトリのステータスを確認します。

```shell
tiup telemetry status
```

## コンプライアンス {#compliance}

さまざまな国や地域のコンプライアンス要件を満たすために、使用情報は送信側マシンの IP アドレスに応じてさまざまな国にあるサーバーに送信されます。

-   中国本土の IP アドレスの場合、使用情報は中国本土のクラウド サーバーに送信され、保存されます。
-   中国本土以外の IP アドレスの場合、使用情報は米国のクラウド サーバーに送信され、保存されます。

詳細は[PingCAP プライバシーポリシー](https://en.pingcap.com/privacy-policy/)参照。
