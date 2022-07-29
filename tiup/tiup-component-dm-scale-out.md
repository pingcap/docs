---
title: tiup dm scale-out
---

# tiup dm scale-out {#tiup-dm-scale-out}

`tiup dm scale-out`コマンドは、クラスタをスケールアウトするために使用されます。クラスタをスケールアウトする内部ロジックは、クラスタのデプロイメントに似ています。 `tiup-dm`のコンポーネントは、最初に新しいノードへのSSH接続を確立し、ターゲットノードに必要なディレクトリを作成してから、展開を実行してサービスを開始します。

## 構文 {#syntax}

```shell
tiup dm scale-out <cluster-name> <topology.yaml> [flags]
```

`<cluster-name>` ：操作するクラスタの名前。クラスタ名を忘れた場合は、 [クラスタリスト](/tiup/tiup-component-dm-list.md)コマンドで確認できます。

`<topology.yaml>` ：準備された[トポロジーファイル](/tiup/tiup-dm-topology-reference.md) 。このトポロジファイルには、現在のクラスタに追加される新しいノードのみが含まれている必要があります。

## オプション {#options}

### -u、-user {#u-user}

-   ターゲットマシンへの接続に使用されるユーザー名を指定します。このユーザーは、ターゲットマシンでシークレットフリーのsudoroot権限を持っている必要があります。
-   データ型： `STRING`
-   デフォルト：コマンドを実行する現在のユーザー。

### -i、-identity_file {#i-identity-file}

-   ターゲットマシンへの接続に使用されるキーファイルを指定します。
-   データ型： `STRING`
-   このオプションがコマンドで指定されていない場合、デフォルトでは`~/.ssh/id_rsa`ファイルがターゲットマシンへの接続に使用されます。

### -p、-password {#p-password}

-   ターゲットマシンへの接続に使用するパスワードを指定します。このオプションと`-i/--identity_file`を同時に使用しないでください。
-   データ型： `BOOLEAN`
-   デフォルト：false

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型： `BOOLEAN`
-   デフォルト：false

## 出力 {#output}

スケールアウトのログ。

[&lt;&lt;前のページに戻るTiUP DMコマンドリスト](/tiup/tiup-component-dm.md#command-list)
