---
title: tiup dm scale-out
summary: tiup dm scale-out コマンドは、新しいノードへの SSH 接続を確立し、必要なディレクトリを作成し、デプロイしてサービスを開始することで、クラスターをスケールアウトするために使用されます。
---

# tiup dm scale-out {#tiup-dm-scale-out}

`tiup dm scale-out`コマンドは、クラスターのスケールアウトに使用されます。クラスターのスケールアウトの内部ロジックは、クラスターのデプロイメントに似ています。3 `tiup-dm`コンポーネントは、最初に新しいノードへの SSH 接続を確立し、ターゲット ノードに必要なディレクトリを作成してから、デプロイメントを実行してサービスを開始します。

## 構文 {#syntax}

```shell
tiup dm scale-out <cluster-name> <topology.yaml> [flags]
```

`<cluster-name>` : 操作するクラスターの名前。クラスター名を忘れた場合は、 [クラスターリスト](/tiup/tiup-component-dm-list.md)コマンドで確認できます。

`<topology.yaml>` : 準備された[トポロジファイル](/tiup/tiup-dm-topology-reference.md) 。このトポロジ ファイルには、現在のクラスターに追加される新しいノードのみを含める必要があります。

## オプション {#options}

### -u、--ユーザー {#u-user}

-   ターゲット マシンへの接続に使用するユーザー名を指定します。このユーザーには、ターゲット マシンに対するシークレットフリーの sudo ルート権限が必要です。
-   データ型: `STRING`
-   デフォルト: コマンドを実行する現在のユーザー。

### -i, --identity_file {#i-identity-file}

-   ターゲット マシンに接続するために使用されるキー ファイルを指定します。
-   データ型: `STRING`
-   コマンドでこのオプションが指定されていない場合、デフォルトで`~/.ssh/id_rsa`ファイルがターゲット マシンへの接続に使用されます。

### -p, --パスワード {#p-password}

-   ターゲット マシンに接続するために使用するパスワードを指定します。このオプションと`-i/--identity_file`同時に使用しないでください。
-   データ型: `BOOLEAN`
-   デフォルト: false

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   デフォルト: false

## 出力 {#output}

スケールアウトのログ。

[&lt;&lt; 前のページに戻る - TiUP DMコマンドリスト](/tiup/tiup-component-dm.md#command-list)
