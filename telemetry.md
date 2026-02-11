---
title: Telemetry
summary: テレメトリ機能と、その機能を無効化してそのステータスを表示する方法について学習します。
---

# テレメトリー {#telemetry}

テレメトリ機能を有効にすると、 TiUPと TiSpark は使用状況情報を収集し、その情報を PingCAP と共有して、製品の改善方法の理解に役立てます。

> **注記：**
>
> -   TiUP v1.11.3以降、 TiUPのテレメトリ機能はデフォルトで無効化されており、 TiUPの使用状況情報はデフォルトで収集されません。v1.11.3より前のTiUPバージョンからv1.11.3以降のバージョンにアップグレードした場合、テレメトリ機能はアップグレード前と同じ状態を維持します。
> -   TiSpark v3.0.3 以降、TiSpark のテレメトリ機能はデフォルトで無効になっており、TiSpark の使用状況情報はデフォルトでは収集されません。
> -   バージョン v8.1.0 から v8.5.1 では、TiDB および TiDB ダッシュボードのテレメトリ機能が削除されます。
> -   v8.5.3以降、TiDBはテレメトリ機能を再度導入しました。ただし、テレメトリ関連の情報はローカルにのみ記録され、ネットワーク経由でPingCAPにデータが送信されなくなりました。

## テレメトリを有効にすると何が共有されますか? {#what-is-shared-when-telemetry-is-enabled}

以下のセクションでは、 TiUPとTiSparkの共有される使用状況情報について詳しく説明します。共有される使用状況情報は、今後変更される可能性があります。変更があった場合は、 [リリースノート](/releases/_index.md)でお知らせします。

> **注記：**
>
> **いずれの**場合も、TiDBクラスタに保存されたユーザーデータは共有され**ません**[PingCAPプライバシーポリシー](https://pingcap.com/privacy-policy)も参照してください。

### TiUP {#tiup}

TiUPでテレメトリ収集機能が有効になっている場合、次のような (ただしこれらに限定されない) TiUPの使用状況の詳細が共有されます。

-   ランダムに生成されたテレメトリ ID。
-   実行が成功したかどうかや実行時間などのTiUPコマンドの実行ステータス。
-   ハードウェアのサイズ、TiDB コンポーネントのバージョン、変更されたデプロイメント構成名などのデプロイメント特性。

PingCAPに共有される使用状況情報の全内容を表示するには、 TiUPコマンド実行時に環境変数`TIUP_CLUSTER_DEBUG=enable`を設定します。例：

```shell
TIUP_CLUSTER_DEBUG=enable tiup cluster list
```

### ティスパーク {#tispark}

> **注記：**
>
> v3.0.3 以降、TiSpark ではテレメトリ収集がデフォルトで無効になっており、使用状況情報は収集されず、PingCAP と共有されません。

TiSpark のテレメトリ収集機能が有効になっている場合、Spark モジュールは次のようなもの (ただしこれに限定されません) を含む TiSpark の使用状況の詳細を共有します。

-   ランダムに生成されたテレメトリ ID。
-   読み取りエンジンやストリーミング読み取りが有効かどうかなど、TiSpark の一部の構成情報。
-   TiSpark が配置されているノードのマシン ハードウェア情報、OS 情報、コンポーネントバージョン番号などのクラスタ展開情報。

Sparkログに収集されたTiSparkの使用状況情報を確認できます。SparkログレベルをINFO以下に設定できます。例：

```shell
grep "Telemetry report" {spark.log} | tail -n 1
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

## テレメトリのステータスを確認する {#check-telemetry-status}

TiUPテレメトリの場合、次のコマンドを実行してテレメトリのステータスを確認します。

```shell
tiup telemetry status
```

## コンプライアンス {#compliance}

さまざまな国や地域のコンプライアンス要件を満たすために、使用情報は送信元マシンの IP アドレスに応じてさまざまな国にあるサーバーに送信されます。

-   中国本土の IP アドレスの場合、使用情報は中国本土のクラウド サーバーに送信され、保存されます。
-   中国本土以外の IP アドレスの場合、使用情報は米国のクラウド サーバーに送信され、保存されます。

詳細は[PingCAPプライバシーポリシー](https://www.pingcap.com/privacy-policy/)参照。
