---
title: Telemetry
summary: Learn the telemetry feature, how to disable the feature and view its status.
---

# テレメトリー {#telemetry}

デフォルトでは、TiDB、TiUP、およびTiDBダッシュボードは使用情報を収集し、その情報をPingCAPと共有して、製品を改善する方法を理解するのに役立ちます。たとえば、この使用法情報は、新機能の優先順位付けに役立ちます。

## 何が共有されますか？ {#what-is-shared}

次のセクションでは、各コンポーネントの共有使用情報について詳しく説明します。共有される使用法の詳細は、時間の経過とともに変更される可能性があります。これらの変更（ある場合）は[リリースノート](/releases/release-notes.md)で発表されます。

> **ノート：**
>
> **すべて**の場合において、TiDBクラスタに保存されているユーザーデータは共有され<strong>ません</strong>。 [PingCAPプライバシーポリシー](https://pingcap.com/privacy-policy)も参照できます。

### TiDB {#tidb}

TiDBでテレメトリ収集機能が有効になっている場合、TiDBクラスタは6時間ごとに使用状況の詳細を収集します。これらの使用法の詳細には、以下が含まれますが、これらに限定されません。

-   ランダムに生成されたテレメトリID。
-   ハードウェアのサイズ（CPU、メモリ、ディスク）、TiDBコンポーネントのバージョン、OS名などの展開特性。
-   クエリ要求の数や期間など、システム内のクエリ要求のステータス。
-   コンポーネントの使用法、たとえば、非同期コミット機能が使用されているかどうか。
-   TiDBテレメトリデータ送信者の仮名化されたIPアドレス。

PingCAPに共有される使用情報の全内容を表示するには、次のSQLステートメントを実行します。

{{< copyable "" >}}

```sql
ADMIN SHOW TELEMETRY;
```

### TiDBダッシュボード {#tidb-dashboard}

テレメトリ収集機能がTiDBダッシュボードで有効になっている場合、TiDBダッシュボードWeb UIの使用情報が共有されます（ただし、これらに限定されません）。

-   ランダムに生成されたテレメトリID。
-   ユーザーがアクセスしたTiDBダッシュボードWebページの名前などのユーザー操作情報。
-   ブラウザ名、OS名、画面解像度などのブラウザとOSの情報。

PingCAPに共有される使用情報の全内容を表示するには、 [ChromeDevToolsのネットワークアクティビティインスペクター](https://developers.google.com/web/tools/chrome-devtools/network)または[Firefox開発ツールのネットワークモニター](https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor)を使用します。

### TiUP {#tiup}

TiUPでテレメトリ収集機能が有効になっている場合、TiUPを使用したユーザー操作は、以下を含む（ただしこれらに限定されない）共有されます。

-   ランダムに生成されたテレメトリID。
-   実行が成功したかどうかや実行時間など、TiUPコマンドの実行ステータス。
-   ハードウェアのサイズ、TiDBコンポーネントのバージョン、変更された展開構成名などの展開特性。

PingCAPに共有される使用情報の全内容を表示するには、TiUPコマンドの実行時に`TIUP_CLUSTER_DEBUG=enable`環境変数を設定します。例えば：

{{< copyable "" >}}

```shell
TIUP_CLUSTER_DEBUG=enable tiup cluster list
```

## テレメトリを無効にする {#disable-telemetry}

### 展開時にTiDBテレメトリを無効にする {#disable-tidb-telemetry-at-deployment}

TiDBクラスターを展開するときは、すべてのTiDBインスタンスでTiDBテレメトリコレクションを無効にするように[`enable-telemetry = false`](/tidb-configuration-file.md#enable-telemetry-new-in-v402)を構成します。この設定を使用して、既存のTiDBクラスタでテレメトリを無効にすることもできます。テレメトリは、クラスタを再起動するまで有効になりません。

さまざまな展開ツールでテレメトリを無効にする詳細な手順を以下に示します。

<details><summary>バイナリ展開</summary>

次の内容で構成ファイル`tidb_config.toml`を作成します。

{{< copyable "" >}}

```toml
enable-telemetry = false
```

上記の構成ファイルを有効にするには、TiDBを起動するときに`--config=tidb_config.toml`のコマンドラインパラメーターを指定します。

詳細については、 [TiDBConfiguration / コンフィグレーションオプション](/command-line-flags-for-tidb-configuration.md#--config)と[TiDBConfiguration / コンフィグレーションファイル](/tidb-configuration-file.md#enable-telemetry-new-in-v402)を参照してください。

</details>

<details><summary>TiUPPlaygroundを使用した展開</summary>

次の内容で構成ファイル`tidb_config.toml`を作成します。

{{< copyable "" >}}

```toml
enable-telemetry = false
```

TiUP Playgroundを起動するときは、上記の構成ファイルの`--db.config tidb_config.toml`コマンドラインパラメーターを指定して有効にします。例えば：

{{< copyable "" >}}

```shell
tiup playground --db.config tidb_config.toml
```

詳細については、 [ローカルTiDBクラスターを迅速にデプロイする](/tiup/tiup-playground.md)を参照してください。

</details>

<details><summary>TiUPクラスターを使用した展開</summary>

デプロイメントトポロジファイル`topology.yaml`を変更して、次のコンテンツを追加します。

{{< copyable "" >}}

```yaml
server_configs:
  tidb:
    enable-telemetry: false
```

</details>

<details><summary>TiDB Operatorを介したKubernetesでのデプロイ</summary>

`tidb-cluster.yaml`分の`spec.tidb.config.enable-telemetry: false`またはTidbClusterカスタムリソースを構成します。

詳細については、 [KubernetesにTiDB Operatorをデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-tidb-operator)を参照してください。

> **ノート：**
>
> この構成アイテムを有効にするには、 TiDB Operatorv1.1.3以降が必要です。

</details>

### デプロイされたTiDBクラスターのTiDBテレメトリを無効にする {#disable-tidb-telemetry-for-deployed-tidb-clusters}

既存のTiDBクラスターでは、システム変数[`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-new-in-v402)を変更して、TiDBテレメトリコレクションを動的に無効にすることもできます。

{{< copyable "" >}}

```sql
SET GLOBAL tidb_enable_telemetry = 0;
```

> **ノート：**
>
> テレメトリを無効にすると、構成ファイルの優先度がシステム変数よりも高くなります。つまり、テレメトリ収集が構成ファイルによって無効にされた後、システム変数の値は無視されます。

### TiDBダッシュボードテレメトリを無効にする {#disable-tidb-dashboard-telemetry}

[`dashboard.enable-telemetry = false`](/pd-configuration-file.md#enable-telemetry)を構成して、すべてのPDインスタンスでTiDBダッシュボードテレメトリコレクションを無効にします。構成を有効にするには、実行中のクラスターを再起動する必要があります。

さまざまな展開ツールのテレメトリを無効にする詳細な手順を以下に示します。

<details><summary>バイナリ展開</summary>

次の内容で構成ファイル`pd_config.toml`を作成します。

{{< copyable "" >}}

```toml
[dashboard]
enable-telemetry = false
```

PDを開始するときに、 `--config=pd_config.toml`のコマンドラインパラメータを指定して有効にします。

詳細については、 [PDConfiguration / コンフィグレーションフラグ](/command-line-flags-for-pd-configuration.md#--config)と[PDConfiguration / コンフィグレーションファイル](/pd-configuration-file.md#enable-telemetry)を参照してください。

</details>

<details><summary>TiUPPlaygroundを使用した展開</summary>

次の内容で構成ファイル`pd_config.toml`を作成します。

{{< copyable "" >}}

```toml
[dashboard]
enable-telemetry = false
```

TiUP Playgroundを起動するときに、有効にする`--pd.config pd_config.toml`のコマンドラインパラメーターを指定します。次に例を示します。

{{< copyable "" >}}

```shell
tiup playground --pd.config pd_config.toml
```

詳細については、 [ローカルTiDBクラスターを迅速にデプロイする](/tiup/tiup-playground.md)を参照してください。

</details>

<details><summary>TiUPクラスターを使用した展開</summary>

デプロイメントトポロジファイル`topology.yaml`を変更して、次のコンテンツを追加します。

{{< copyable "" >}}

```yaml
server_configs:
  pd:
    dashboard.enable-telemetry: false
```

</details>

<details><summary>TiDB Operatorを介したKubernetesでのデプロイ</summary>

`tidb-cluster.yaml`分の`spec.pd.config.dashboard.enable-telemetry: false`またはTidbClusterカスタムリソースを構成します。

詳細については、 [KubernetesにTiDB Operatorをデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-tidb-operator)を参照してください。

> **ノート：**
>
> この構成アイテムを有効にするには、 TiDB Operatorv1.1.3以降が必要です。

</details>

### TiUPテレメトリを無効にする {#disable-tiup-telemetry}

TiUPテレメトリ収集を無効にするには、次のコマンドを実行します。

{{< copyable "" >}}

```shell
tiup telemetry disable
```

## テレメトリステータスを確認する {#check-telemetry-status}

TiDBテレメトリの場合、次のSQLステートメントを実行してテレメトリステータスを確認します。

{{< copyable "" >}}

```sql
ADMIN SHOW TELEMETRY;
```

実行結果の`DATA_PREVIEW`列が空の場合、TiDBテレメトリは無効になります。そうでない場合、TiDBテレメトリが有効になります。また、 `LAST_STATUS`列目で、以前に利用情報が共有された時期や、共有が成功したかどうかを確認することもできます。

TiUPテレメトリの場合、次のコマンドを実行してテレメトリステータスを確認します。

{{< copyable "" >}}

```shell
tiup telemetry status
```

## コンプライアンス {#compliance}

さまざまな国または地域のコンプライアンス要件を満たすために、使用情報は、送信側マシンのIPアドレスに従ってさまざまな国にあるサーバーに送信されます。

-   中国本土からのIPアドレスの場合、使用情報は中国本土のクラウドサーバーに送信されて保存されます。
-   中国本土以外のIPアドレスの場合、使用情報は米国のクラウドサーバーに送信されて保存されます。

詳細については、 [PingCAPプライバシーポリシー](https://en.pingcap.com/privacy-policy/)を参照してください。
