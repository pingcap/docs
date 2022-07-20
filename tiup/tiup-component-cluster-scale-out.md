---
title: tiup cluster scale-out
---

# tiup cluster scale-out {#tiup-cluster-scale-out}

`tiup cluster scale-out`コマンドは、クラスタをスケールアウトするために使用されます。クラスタをスケールアウトする内部ロジックは、クラスタのデプロイメントに似ています。 tiup-clusterコンポーネントは、最初に新しいノードへのSSH接続を確立し、ターゲットノードに必要なディレクトリを作成してから、展開を実行してサービスを開始します。

PDがスケールアウトされると、結合操作によって新しいPDノードがクラスタに追加され、PDに関連付けられたサービスの構成が更新されます。他のサービスは直接開始され、クラスタに追加されます。

## 構文 {#syntax}

```shell
tiup cluster scale-out <cluster-name> <topology.yaml> [flags]
```

`<cluster-name>` ：操作するクラスタの名前。クラスタ名を忘れた場合は、 [`cluster list`](/tiup/tiup-component-dm-list.md)コマンドで確認できます。

`<topology.yaml>` ：準備された[トポロジーファイル](/tiup/tiup-dm-topology-reference.md) 。このトポロジファイルには、現在のクラスタに追加される新しいノードのみが含まれている必要があります。

## オプション {#options}

### -u、-user {#u-user}

-   ターゲットマシンへの接続に使用されるユーザー名を指定します。このユーザーは、ターゲットマシンに対するシークレットフリーのsudoroot権限を持っている必要があります。
-   データ型： `STRING`
-   デフォルト：コマンドを実行する現在のユーザー。

### -i、-identity_file {#i-identity-file}

-   ターゲットマシンへの接続に使用されるキーファイルを指定します。
-   データ型： `STRING`
-   コマンドでこのオプションが指定されていない場合、デフォルトでは`~/.ssh/id_rsa`ファイルがターゲットマシンへの接続に使用されます。

### -p、-password {#p-password}

-   ターゲットマシンへの接続に使用するパスワードを指定します。このオプションと`-i/--identity_file`を同時に使用しないでください。
-   データ型： `BOOLEAN`
-   デフォルト：false

### --no-labels {#no-labels}

-   このオプションは、ラベルチェックをスキップするために使用されます。
-   2つ以上のTiKVノードが同じ物理マシンにデプロイされている場合、リスクが存在します。PDはクラスタトポロジを認識しないため、リージョンの複数のレプリカを1つの物理マシン上の異なるTiKVノードにスケジュールする可能性があります。これにより、この物理マシンは単一障害点。このリスクを回避するために、ラベルを使用して、同じリージョンを同じマシンにスケジュールしないようにPDに指示できます。ラベルの設定については、 [トポロジラベルによるレプリカのスケジュール](/schedule-replicas-by-topology-labels.md)を参照してください。
-   テスト環境では、このリスクは問題にならない可能性があり、 `--no-labels`を使用してチェックをスキップできます。
-   データ型： `BOOLEAN`
-   デフォルト：false

### --skip-create-user {#skip-create-user}

-   クラスタの展開中に、tiup-clusterはトポロジファイルに指定されたユーザー名が存在するかどうかを確認します。そうでない場合は、作成します。このチェックをスキップするには、 `--skip-create-user`オプションを使用できます。
-   データ型： `BOOLEAN`
-   デフォルト：false

### -h、-help {#h-help}

-   ヘルプ情報を出力します。
-   データ型： `BOOLEAN`
-   デフォルト：false

## 出力 {#output}

スケールアウトのログ。

[&lt;&lt;前のページに戻る-TiUPクラスターコマンドリスト](/tiup/tiup-component-cluster.md#command-list)
