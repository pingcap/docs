---
title: tiup dm scale-out
summary: tiup dm scale-out` コマンドは、新しいノードへの SSH 接続を確立し、必要なディレクトリを作成し、デプロイしてサービスを開始することで、クラスターをスケールアウトするために使用されます。
---

# tiup dm scale-out {#tiup-dm-scale-out}

`tiup dm scale-out`コマンドはクラスタのスケールアウトに使用されます。クラスタのスケールアウトの内部ロジックは、クラスタのデプロイメントと同様です。3 `tiup-dm`コンポーネントは、まず新しいノードへのSSH接続を確立し、ターゲットノードに必要なディレクトリを作成し、次にデプロイメントを実行してサービスを起動します。

## 構文 {#syntax}

```shell
tiup dm scale-out <cluster-name> <topology.yaml> [flags]
```

`<cluster-name>` : 操作対象のクラスターの名前。クラスター名を忘れた場合は、 [クラスターリスト](/tiup/tiup-component-dm-list.md)コマンドで確認できます。

`<topology.yaml>` : 準備された[トポロジファイル](/tiup/tiup-dm-topology-reference.md)このトポロジファイルには、現在のクラスターに追加される新しいノードのみを含める必要があります。

## オプション {#options}

### -u, --user {#u-user}

-   ターゲットマシンへの接続に使用するユーザー名を指定します。このユーザーは、ターゲットマシン上でシークレットフリーのsudo root権限を持っている必要があります。
-   データ型: `STRING`
-   デフォルト: コマンドを実行する現在のユーザー。

### -i, --identity_file {#i-identity-file}

-   ターゲット マシンに接続するために使用するキー ファイルを指定します。
-   データ型: `STRING`
-   コマンドでこのオプションを指定しない場合は、デフォルトで`~/.ssh/id_rsa`ファイルを使用してターゲット マシンに接続します。

### -p, --パスワード {#p-password}

-   ターゲットマシンへの接続に使用するパスワードを指定します。このオプションと`-i/--identity_file`同時に使用しないでください。
-   データ型: `BOOLEAN`
-   デフォルト: false

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   デフォルト: false

## 出力 {#output}

スケールアウトのログ。

[&lt;&lt; 前のページに戻る - TiUP DMコマンドリスト](/tiup/tiup-component-dm.md#command-list)
