---
title: tiup cluster scale-out
---

# tiup cluster scale-out {#tiup-cluster-scale-out}

`tiup cluster scale-out`コマンドはクラスターをスケールアウトするために使用されます。クラスターをスケールアウトする内部ロジックは、クラスターの展開と似ています。 tiup-clusterコンポーネントは、まず新しいノードへの SSH 接続を確立し、ターゲット ノードに必要なディレクトリを作成してから、デプロイメントを実行してサービスを開始します。

PD がスケールアウトされると、結合操作によって新しい PD ノードがクラスターに追加され、PD に関連付けられたサービスの構成が更新されます。他のサービスは直接開始され、クラスターに追加されます。

## 構文 {#syntax}

```shell
tiup cluster scale-out <cluster-name> <topology.yaml> [flags]
```

`<cluster-name>` : 操作するクラスターの名前。クラスター名を忘れた場合は、 [`cluster list`](/tiup/tiup-component-dm-list.md)コマンドで確認できます。

`<topology.yaml>` : 準備された[トポロジファイル](/tiup/tiup-dm-topology-reference.md) 。このトポロジ ファイルには、現在のクラスターに追加される新しいノードのみが含まれている必要があります。

## オプション {#options}

### -u、--user {#u-user}

-   ターゲット マシンへの接続に使用するユーザー名を指定します。このユーザーは、ターゲット マシン上でシークレットなしの sudo root 権限を持っている必要があります。
-   データ型: `STRING`
-   デフォルト: コマンドを実行する現在のユーザー。

### -i、--identity_file {#i-identity-file}

-   ターゲット マシンへの接続に使用するキー ファイルを指定します。
-   データ型: `STRING`
-   このオプションがコマンドで指定されていない場合、デフォルトで`~/.ssh/id_rsa`ファイルがターゲット マシンへの接続に使用されます。

### -p、--パスワード {#p-password}

-   ターゲット マシンへの接続に使用するパスワードを指定します。このオプションと`-i/--identity_file`を同時に使用しないでください。
-   データ型: `BOOLEAN`
-   デフォルト: false

### --no-labels {#no-labels}

-   このオプションは、ラベル チェックをスキップするために使用されます。
-   2 つ以上の TiKV ノードが同じ物理マシン上にデプロイされている場合、リスクが存在します。PD はクラスター トポロジを認識していないため、リージョンの複数のレプリカを 1 つの物理マシン上の異なる TiKV ノードにスケジュールする可能性があり、この物理マシンは単一障害点。このリスクを回避するには、ラベルを使用して、同じリージョンを同じマシンにスケジュールしないよう PD に指示できます。ラベルの構成については[トポロジーラベルごとにレプリカをスケジュールする](/schedule-replicas-by-topology-labels.md)を参照してください。
-   テスト環境では、このリスクは問題にならない可能性があるため、 `--no-labels`を使用してチェックをスキップできます。
-   データ型: `BOOLEAN`
-   デフォルト: false

### --skip-create-user {#skip-create-user}

-   クラスターの展開中に、 tiup-cluster はトポロジー ファイルに指定されたユーザー名が存在するかどうかを確認します。そうでない場合は、作成されます。このチェックをスキップするには、 `--skip-create-user`オプションを使用できます。
-   データ型: `BOOLEAN`
-   デフォルト: false

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   デフォルト: false

## 出力 {#output}

スケールアウトのログ。

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
