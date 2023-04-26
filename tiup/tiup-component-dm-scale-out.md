---
title: tiup dm scale-out
---

# tiup dm scale-out {#tiup-dm-scale-out}

`tiup dm scale-out`コマンドは、クラスターをスケールアウトするために使用されます。クラスターをスケールアウトする内部ロジックは、クラスターのデプロイに似ています。 `tiup-dm`コンポーネントは、最初に新しいノードへの SSH 接続を確立し、ターゲット ノードに必要なディレクトリを作成してから、デプロイを実行してサービスを開始します。

## 構文 {#syntax}

```shell
tiup dm scale-out <cluster-name> <topology.yaml> [flags]
```

`<cluster-name>` : 操作するクラスターの名前。クラスター名を忘れた場合は、 [クラスタ リスト](/tiup/tiup-component-dm-list.md)コマンドで確認できます。

`<topology.yaml>` : 準備された[トポロジ ファイル](/tiup/tiup-dm-topology-reference.md) 。このトポロジ ファイルには、現在のクラスタに追加される新しいノードのみが含まれている必要があります。

## オプション {#options}

### -u, --user {#u-user}

-   ターゲット マシンへの接続に使用するユーザー名を指定します。このユーザーには、ターゲット マシンでシークレットのない sudo root 権限が必要です。
-   データ型: `STRING`
-   デフォルト: コマンドを実行する現在のユーザー。

### -i, --identity_file {#i-identity-file}

-   ターゲット マシンへの接続に使用するキー ファイルを指定します。
-   データ型: `STRING`
-   このオプションがコマンドで指定されていない場合、デフォルトで`~/.ssh/id_rsa`ファイルがターゲット マシンへの接続に使用されます。

### -p, --password {#p-password}

-   ターゲット マシンへの接続に使用するパスワードを指定します。このオプションと`-i/--identity_file`を同時に使用しないでください。
-   データ型: `BOOLEAN`
-   デフォルト: false

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   デフォルト: false

## 出力 {#output}

スケールアウトのログ。

[&lt;&lt; 前のページに戻る - TiUP DMコマンド一覧](/tiup/tiup-component-dm.md#command-list)
