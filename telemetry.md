---
title: Telemetry
summary: Learn the telemetry feature, how to disable the feature and view its status.
---

# テレメトリー {#telemetry}

テレメトリが有効になると、TiDB、 TiUP 、および TiDB ダッシュボードは使用状況情報を収集し、その情報を PingCAP と共有して、製品の改善方法を理解するのに役立ちます。たとえば、この使用状況情報は、新機能の優先順位付けに役立ちます。

> **注記：**
>
> -   2023 年 2 月 20 日以降、v6.6.0 を含む TiDB および TiDB ダッシュボードの新しいバージョンではテレメトリ機能がデフォルトで無効になり、使用状況情報は収集されず、PingCAP と共有されません。これらのバージョンにアップグレードする前に、クラスターでデフォルトのテレメトリ構成が使用されている場合、アップグレード後にテレメトリ機能は無効になります。特定のバージョンについては[TiDB リリース タイムライン](/releases/release-timeline.md)を参照してください。
> -   v1.11.3 以降、新しく展開されたTiUPではテレメトリ機能がデフォルトで無効になっており、使用状況情報は収集されません。 TiUP のv1.11.3 より前のバージョンから v1.11.3 以降のバージョンにアップグレードすると、テレメトリ機能はアップグレード前と同じステータスを維持します。

## 何が共有されますか? {#what-is-shared}

次のセクションでは、各コンポーネントの共有使用法情報について詳しく説明します。共有される使用状況の詳細は、時間の経過とともに変更される可能性があります。これらの変更は (ある場合) [リリースノート](/releases/release-notes.md)で発表されます。

> **注記：**
>
> **すべての**場合において、TiDB クラスターに保存されているユーザー データは共有されませ**ん**。 [PingCAP プライバシー ポリシー](https://pingcap.com/privacy-policy)も参照してください。

### TiDB {#tidb}

TiDB でテレメトリ収集機能が有効になっている場合、TiDB クラスターは 6 時間単位で使用状況の詳細を収集します。これらの使用法の詳細には次のものが含まれますが、これらに限定されません。

-   ランダムに生成されたテレメトリ ID。
-   ハードウェアのサイズ (CPU、メモリ、ディスク)、TiDB コンポーネントのバージョン、OS 名などの展開特性。
-   クエリリクエストの数や期間など、システム内のクエリリクエストのステータス。
-   コンポーネントの使用状況 (非同期コミット機能が使用されているかどうかなど)。
-   TiDB テレメトリ データ送信者の仮名化された IP アドレス。

PingCAP に共有されている使用状況情報の完全な内容を表示するには、次の SQL ステートメントを実行します。

```sql
ADMIN SHOW TELEMETRY;
```

### TiDB ダッシュボード {#tidb-dashboard}

TiDB ダッシュボードでテレメトリ収集機能が有効になっている場合、TiDB ダッシュボード Web UI の使用状況の詳細が共有されます。これには次のものが含まれます (ただし、これらに限定されません)。

-   ランダムに生成されたテレメトリ ID。
-   ユーザーがアクセスした TiDB ダッシュボード Web ページの名前などのユーザー操作情報。
-   ブラウザ名、OS名、画面解像度などのブラウザとOSの情報。

PingCAP に共有されている使用状況情報の完全な内容を表示するには、 [Chrome DevTools のネットワーク アクティビティ インスペクター](https://developers.google.com/web/tools/chrome-devtools/network)または[Firefox 開発者ツールのネットワーク モニター](https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor)を使用します。

### TiUP {#tiup}

TiUPでテレメトリ収集機能が有効になっている場合、以下を含む (ただしこれらに限定されない) TiUPの使用状況の詳細が共有されます。

-   ランダムに生成されたテレメトリ ID。
-   TiUPコマンドの実行ステータス (実行が成功したかどうか、実行時間など)。
-   ハードウェアのサイズ、TiDB コンポーネントのバージョン、変更された展開構成名などの展開特性。

PingCAP に共有される使用状況情報の完全な内容を表示するには、 TiUPコマンドの実行時に`TIUP_CLUSTER_DEBUG=enable`環境変数を設定します。例えば：

```shell
TIUP_CLUSTER_DEBUG=enable tiup cluster list
```

### ティスパーク {#tispark}

> **注記：**
>
> v3.0.3 以降、TiSpark ではテレメトリ収集がデフォルトで無効になっており、使用状況情報は収集されず、PingCAP と共有されません。

TiSpark のテレメトリ収集機能が有効になっている場合、Spark モジュールは、以下を含む (ただしこれらに限定されない) TiSpark の使用状況の詳細を共有します。

-   ランダムに生成されたテレメトリ ID。
-   読み取りエンジンやストリーミング読み取りが有効かどうかなど、TiSpark の一部の構成情報。
-   TiSpark が配置されているノードのマシンのハードウェア情報、OS 情報、コンポーネントのバージョン番号などのクラスタ展開情報。

Spark ログに収集された TiSpark の使用状況情報を表示できます。 Spark ログ レベルを INFO 以下に設定できます。次に例を示します。

```shell
cat {spark.log} | grep Telemetry report | tail -n 1
```

## テレメトリを無効にする {#disable-telemetry}

### 導入時に TiDB テレメトリを無効にする {#disable-tidb-telemetry-at-deployment}

既存の TiDB クラスターでテレメトリが有効になっている場合、各 TiDB インスタンスで[`enable-telemetry = false`](/tidb-configuration-file.md#enable-telemetry-new-in-v402)を構成して、そのインスタンスでの TiDB テレメトリ収集を無効にすることができます。これはクラスターを再起動するまで有効になりません。

さまざまな展開ツールでテレメトリを無効にする詳細な手順を以下に示します。

<details><summary>バイナリ展開</summary>

次の内容を含む構成ファイル`tidb_config.toml`を作成します。

```toml
enable-telemetry = false
```

上記の構成ファイルを有効にするには、TiDB を起動するときに`--config=tidb_config.toml`コマンドライン パラメーターを指定します。

詳細については、 [TiDBコンフィグレーションオプション](/command-line-flags-for-tidb-configuration.md#--config)と[TiDBコンフィグレーションファイル](/tidb-configuration-file.md#enable-telemetry-new-in-v402)を参照してください。

</details>

<details><summary>TiUP Playground を使用した展開</summary>

次の内容を含む構成ファイル`tidb_config.toml`を作成します。

```toml
enable-telemetry = false
```

TiUP Playground を起動するときに、上記の設定ファイルを有効にするために`--db.config tidb_config.toml`コマンド ライン パラメータを指定します。例えば：

```shell
tiup playground --db.config tidb_config.toml
```

詳細については[ローカル TiDBクラスタを迅速にデプロイ](/tiup/tiup-playground.md)を参照してください。

</details>

<details><summary>TiUPクラスタを使用した導入</summary>

デプロイメント トポロジ ファイル`topology.yaml`を変更して、次の内容を追加します。

```yaml
server_configs:
  tidb:
    enable-telemetry: false
```

</details>

<details><summary>TiDB Operatorを介した Kubernetes へのデプロイメント</summary>

`spec.tidb.config.enable-telemetry: false`または TidbCluster カスタム リソースを`tidb-cluster.yaml`します。

詳細については[TiDB Operator をKubernetes にデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-tidb-operator)を参照してください。

> **注記：**
>
> この構成項目を有効にするには、 TiDB Operator v1.1.3 以降が必要です。

</details>

### デプロイされた TiDB クラスターの TiDB テレメトリを無効にする {#disable-tidb-telemetry-for-deployed-tidb-clusters}

既存の TiDB クラスターでは、システム変数[`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-new-in-v402)を変更して TiDB テレメトリ収集を動的に無効にすることもできます。

```sql
SET GLOBAL tidb_enable_telemetry = 0;
```

> **注記：**
>
> テレメトリを無効にすると、構成ファイルがシステム変数よりも優先されます。つまり、構成ファイルによってテレメトリ収集が無効になった後は、システム変数の値は無視されます。

### TiDB ダッシュボード テレメトリを無効にする {#disable-tidb-dashboard-telemetry}

[`dashboard.enable-telemetry = false`](/pd-configuration-file.md#enable-telemetry)を構成して、すべての PD インスタンスで TiDB ダッシュボード テレメトリ収集を無効にします。構成を有効にするには、実行中のクラスターを再起動する必要があります。

さまざまな展開ツールのテレメトリを無効にする詳細な手順を以下に示します。

<details><summary>バイナリ展開</summary>

次の内容を含む構成ファイル`pd_config.toml`を作成します。

```toml
[dashboard]
enable-telemetry = false
```

PD を開始するときに`--config=pd_config.toml`コマンドライン パラメータを指定して有効にします。

詳細については、 [PDコンフィグレーションフラグ](/command-line-flags-for-pd-configuration.md#--config)と[PDコンフィグレーションファイル](/pd-configuration-file.md#enable-telemetry)を参照してください。

</details>

<details><summary>TiUP Playground を使用した展開</summary>

次の内容を含む構成ファイル`pd_config.toml`を作成します。

```toml
[dashboard]
enable-telemetry = false
```

TiUP Playground を開始するときに、有効にする`--pd.config pd_config.toml`コマンド ライン パラメーターを指定します。例:

```shell
tiup playground --pd.config pd_config.toml
```

詳細については[ローカル TiDBクラスタを迅速にデプロイ](/tiup/tiup-playground.md)を参照してください。

</details>

<details><summary>TiUPクラスタを使用した導入</summary>

デプロイメント トポロジ ファイル`topology.yaml`を変更して、次の内容を追加します。

```yaml
server_configs:
  pd:
    dashboard.enable-telemetry: false
```

</details>

<details><summary>TiDB Operatorを介した Kubernetes へのデプロイメント</summary>

`spec.pd.config.dashboard.enable-telemetry: false`または TidbCluster カスタム リソースを`tidb-cluster.yaml`します。

詳細については[TiDB Operator をKubernetes にデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-tidb-operator)を参照してください。

> **注記：**
>
> この構成項目を有効にするには、 TiDB Operator v1.1.3 以降が必要です。

</details>

### TiUPテレメトリを無効にする {#disable-tiup-telemetry}

TiUPテレメトリ収集を無効にするには、次のコマンドを実行します。

```shell
tiup telemetry disable
```

## テレメトリーステータスを確認する {#check-telemetry-status}

TiDB テレメトリの場合は、次の SQL ステートメントを実行してテレメトリのステータスを確認します。

```sql
ADMIN SHOW TELEMETRY;
```

実行結果の`DATA_PREVIEW`列が空の場合、TiDB テレメトリは無効になります。そうでない場合は、TiDB テレメトリが有効になっています。また、 `LAST_STATUS`の列に従って、使用状況情報が以前にいつ共有されたか、共有が成功したかどうかを確認することもできます。

TiUPテレメトリの場合は、次のコマンドを実行してテレメトリのステータスを確認します。

```shell
tiup telemetry status
```

## コンプライアンス {#compliance}

さまざまな国や地域のコンプライアンス要件を満たすために、使用状況情報は、送信側マシンの IP アドレスに従ってさまざまな国にあるサーバーに送信されます。

-   中国本土の IP アドレスの場合、使用状況情報は中国本土のクラウド サーバーに送信され、そこに保存されます。
-   中国本土以外の IP アドレスの場合、使用状況情報は米国のクラウド サーバーに送信され、そこに保存されます。

詳細については[PingCAP プライバシー ポリシー](https://en.pingcap.com/privacy-policy/)を参照してください。
