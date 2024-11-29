---
title: Telemetry
summary: テレメトリ機能と、その機能を無効にしてそのステータスを表示する方法について学習します。
aliases: ['/tidb/stable/sql-statement-admin-show-telemetry','/tidb/v8.1/sql-statement-admin-show-telemetry']
---

# テレメトリー {#telemetry}

テレメトリ機能を有効にすると、 TiUPと TiSpark は使用状況情報を収集し、その情報を PingCAP と共有して、製品の改善方法の理解に役立てます。

> **注記：**
>
> -   TiUP v1.11.3 以降では、 TiUPのテレメトリ機能はデフォルトで無効になっています。つまり、 TiUP の使用状況情報はデフォルトでは収集されません。TiUP バージョンTiUPより前のバージョンから v1.11.3 以降のバージョンにアップグレードすると、テレメトリ機能はアップグレード前と同じ状態を維持します。
> -   TiSpark v3.0.3 以降では、TiSpark のテレメトリ機能はデフォルトで無効になっており、TiSpark の使用状況情報はデフォルトでは収集されません。
> -   v8.1.0 以降では、TiDB および TiDB ダッシュボードのテレメトリ機能が削除されます。

## テレメトリを有効にすると何が共有されますか? {#what-is-shared-when-telemetry-is-enabled}

以下のセクションでは、 TiUPと TiSpark の共有使用情報について詳しく説明します。共有される使用詳細は、時間の経過とともに変更される可能性があります。これらの変更 (ある場合) は[リリースノート](/releases/release-notes.md)で発表されます。

> **注記：**
>
> **いずれ**の場合も、TiDB クラスターに保存されているユーザー データは共有され**ません**[PingCAP プライバシーポリシー](https://pingcap.com/privacy-policy)も参照してください。

### TiUP {#tiup}

TiUPでテレメトリ収集機能が有効になっている場合、次のようなTiUPの使用状況の詳細が共有されます (ただし、これらに限定されません)。

-   ランダムに生成されたテレメトリ ID。
-   実行が成功したかどうかや実行時間などのTiUPコマンドの実行ステータス。
-   ハードウェアのサイズ、TiDB コンポーネントのバージョン、変更されたデプロイメント構成名などのデプロイメント特性。

PingCAP に共有される使用情報の全内容を表示するには、 TiUPコマンドを実行するときに`TIUP_CLUSTER_DEBUG=enable`環境変数を設定します。例:

```shell
TIUP_CLUSTER_DEBUG=enable tiup cluster list
```

### ティスパーク {#tispark}

> **注記：**
>
> v3.0.3 以降、TiSpark ではテレメトリ収集がデフォルトで無効になっており、使用状況情報は収集されず、PingCAP と共有されません。

TiSpark のテレメトリ収集機能が有効になっている場合、Spark モジュールは TiSpark の使用状況の詳細 (以下を含みますが、これに限定されません) を共有します。

-   ランダムに生成されたテレメトリ ID。
-   読み取りエンジンやストリーミング読み取りが有効かどうかなど、TiSpark の一部の構成情報。
-   TiSpark が配置されているノードのマシン ハードウェア情報、OS 情報、コンポーネントバージョン番号などのクラスタ展開情報。

Spark ログに収集された TiSpark の使用状況情報を表示できます。Spark ログ レベルを INFO 以下に設定できます。例:

```shell
cat {spark.log} | grep Telemetry report | tail -n 1
```

## テレメトリを有効にする {#enable-telemetry}

### TiUPテレメトリを有効にする {#enable-tiup-telemetry}

TiUPテレメトリ収集を有効にするには、次のコマンドを実行します。

```shell
tiup telemetry enable
```

### TiSparkテレメトリを有効にする {#enable-tispark-telemetry}

TiSpark テレメトリ収集を有効にするには、TiSpark 構成ファイルで`spark.tispark.telemetry.enable = true`構成します。

## テレメトリを無効にする {#disable-telemetry}

### TiUPテレメトリを無効にする {#disable-tiup-telemetry}

TiUPテレメトリ収集を無効にするには、次のコマンドを実行します。

```shell
tiup telemetry disable
```

### TiSparkテレメトリを無効にする {#disable-tispark-telemetry}

TiSpark テレメトリ収集を無効にするには、TiSpark 構成ファイルで`spark.tispark.telemetry.enable = false`構成します。

## テレメトリステータスを確認する {#check-telemetry-status}

TiUPテレメトリの場合、次のコマンドを実行してテレメトリのステータスを確認します。

```shell
tiup telemetry status
```

## コンプライアンス {#compliance}

さまざまな国や地域のコンプライアンス要件を満たすために、使用情報は送信側マシンの IP アドレスに応じてさまざまな国にあるサーバーに送信されます。

-   中国本土の IP アドレスの場合、使用情報は中国本土のクラウド サーバーに送信され、保存されます。
-   中国本土以外の IP アドレスの場合、使用情報は米国のクラウド サーバーに送信され、保存されます。

詳細は[PingCAP プライバシーポリシー](https://www.pingcap.com/privacy-policy/)参照。
