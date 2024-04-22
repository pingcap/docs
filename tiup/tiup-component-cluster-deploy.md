---
title: tiup cluster deploy
summary: tiup cluster deployコマンドは、新しいクラスターをデプロイするために使用されます。構文は、tiup cluster deploy <cluster-name> <version> <topology.yaml> [flags]であり、オプションには-u、--user、-i、--identity_file、-p、--パスワード、--ignore-config-check、--no-labels、--skip-create-user、-h、--helpがあります。出力はデプロイメントログです。
---

# tiup cluster deploy {#tiup-cluster-deploy}

`tiup cluster deploy`コマンドは、新しいクラスターをデプロイするために使用されます。

## 構文 {#syntax}

```shell
tiup cluster deploy <cluster-name> <version> <topology.yaml> [flags]
```

-   `<cluster-name>` : 新しいクラスターの名前。既存のクラスター名と同じにすることはできません。
-   `<version>` : デプロイする TiDB クラスターのバージョン番号`v7.5.1`など)。
-   `<topology.yaml>` : 準備された[トポロジーファイル](/tiup/tiup-cluster-topology-reference.md) 。

## オプション {#options}

### -u、--user {#u-user}

-   ターゲット マシンへの接続に使用するユーザー名を指定します。このユーザーは、ターゲット マシン上でシークレットなしの sudo root 権限を持っている必要があります。
-   データ型: `STRING`
-   デフォルト: コマンドを実行する現在のユーザー。

### -i、--identity_file {#i-identity-file}

-   ターゲット マシンへの接続に使用するキー ファイルを指定します。
-   データ型: `STRING`
-   このオプションがコマンドで指定されていない場合、デフォルトでは`~/.ssh/id_rsa`ファイルがターゲット マシンへの接続に使用されます。

### -p、--パスワード {#p-password}

-   ターゲット マシンへの接続に使用するパスワードを指定します。このオプションを`-i/--identity_file`と同時に使用しないでください。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトでは無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加して、値`true`渡すか、値を渡さないことができます。

### --ignore-config-check {#ignore-config-check}

-   このオプションは、構成チェックをスキップするために使用されます。コンポーネントのバイナリ ファイルがデプロイされた後、TiDB、TiKV、および PD コンポーネントの構成が`<binary> --config-check <config-file>`を使用してチェックされます。 `<binary>`は、デプロイされたバイナリ ファイルのパスです。 `<config-file>`はユーザー設定に基づいて生成された設定ファイルです。
-   このオプションはデフォルトでは無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加して、値`true`渡すか、値を渡さないことができます。
-   デフォルト: false

### --no-labels {#no-labels}

-   このオプションは、ラベル チェックをスキップするために使用されます。
-   2 つ以上の TiKV ノードが同じ物理マシンにデプロイされている場合、リスクが存在します。PD はリージョントポロジを学習できないため、PD は 1 つの物理マシン上の異なる TiKV ノードにリージョンの複数のレプリカをスケジュールする可能性があり、これにより、この物理マシンは単一になります。ポイント。このリスクを回避するには、ラベルを使用して、同じリージョンを同じマシンにスケジュールしないよう PD に指示できます。ラベルの構成については[トポロジーラベルごとにレプリカをスケジュールする](/schedule-replicas-by-topology-labels.md)を参照してください。
-   テスト環境では、このリスクが重要になる可能性があるため、 `--no-labels`使用してチェックをスキップできます。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトでは無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加して、値`true`渡すか、値を渡さないことができます。

### --skip-create-user {#skip-create-user}

-   クラスターの展開中に、 tiup-cluster はトポロジー ファイルに指定されたユーザー名が存在するかどうかを確認します。そうでない場合は、作成されます。このチェックをスキップするには、 `--skip-create-user`オプションを使用できます。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトでは無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加して、値`true`渡すか、値を渡さないことができます。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトでは無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加して、値`true`渡すか、値を渡さないことができます。

## 出力 {#output}

デプロイメントログ。

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
