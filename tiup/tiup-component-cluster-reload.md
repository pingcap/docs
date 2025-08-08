---
title: tiup cluster reload
summary: tiup cluster reload` コマンドは、変更されたクラスタ構成を適用し、サービスを再起動するために使用されます。`--force` で強制実行、`--transfer-timeout` で転送タイムアウトを設定、` --ignore-config-check で設定チェックを無視、` -N 、 --node でノードを指定、` -R 、 --role でロールを指定、`--skip-restart` で再起動をスキップできます。出力はtiup-clusterの実行ログです。
---

# tiup cluster reload {#tiup-cluster-reload}

[クラスタ構成の変更](/tiup/tiup-component-cluster-edit-config.md)後、設定を有効にするには、 `tiup cluster reload`コマンドを使用してクラスタをリロードする必要があります。このコマンドは、制御マシンの設定をサービスが稼働しているリモートマシンに公開し、アップグレードプロセスに従ってサービスを順番に再起動します。再起動プロセス中もクラスタは引き続き利用可能です。

## 構文 {#syntax}

```shell
tiup cluster reload <cluster-name> [flags]
```

`<cluster-name>` : 操作対象のクラスター名。

## オプション {#options}

### &#x20;--force {#force}

-   再ロード プロセス中のエラーを無視し、強制的に再ロードします。
-   データ型: `BOOLEAN`
-   デフォルト: false

### --transfer-timeout {#transfer-timeout}

-   PDまたはTiKVを再起動する際、再起動されたノードのリーダーノードが最初に他のノードに移行されるため、移行プロセスには時間がかかります。最大待機時間（秒単位）を`-transfer-timeout`に設定できます。タイムアウト後、サービスは待機せずに直接再起動できます。
-   データ型: `UINT`
-   デフォルト: 600

> **注記：**
>
> 待機をスキップして直接再起動する場合、サービスのパフォーマンスが不安定になる可能性があります。

### --ignore-config-check {#ignore-config-check}

-   コンポーネントのバイナリファイルがデプロイされた後、 `<binary> --config-check <config-file>`使用して TiDB、TiKV、PD コンポーネントの設定がチェックされます。3 `<binary>`デプロイされたバイナリファイルのパスです。5 `<config-file>`ユーザー設定に基づいて生成された設定ファイルです。このチェックをスキップしたい場合は、このオプションを使用できます。
-   データ型: `BOOLEAN`
-   デフォルト: false

### -N, --node {#n-node}

-   再起動するノードを指定します。指定しない場合は、すべてのノードが再起動されます。このオプションの値は、ノードIDのカンマ区切りのリストです。ノードIDは、 [`tiup cluster display`](/tiup/tiup-component-cluster-display.md)コマンドで返されるクラスターステータステーブルの最初の列から取得できます。
-   データ型: `STRINGS`
-   このオプションがコマンドで指定されていない場合は、デフォルトですべてのノードが選択されます。

> **注記：**
>
> -   `-R, --role`オプションを同時に指定した場合は、 `-N, --node`と`-R, --role`両方の指定に一致するサービス ノードのみが再起動されます。
> -   オプション`--skip-restart`指定した場合、オプション`-N, --node`は無効になります。

### -R, --role {#r-role}

-   再起動するロールを指定します。指定しない場合は、すべてのロールが再起動されます。このオプションの値は、ノードロールのカンマ区切りのリストです。ロールは、表[クラスターステータス](/tiup/tiup-component-cluster-display.md)の2番目の列です。
-   データ型: `STRINGS`
-   コマンドでこのオプションを指定しない場合は、すべてのロールがデフォルトで選択されます。

> **注記：**
>
> 1.  `-N, --node`オプションを同時に指定した場合は、 `-N, --node`と`-R, --role`両方の指定に一致するサービス ノードのみが再起動されます。
> 2.  オプション`--skip-restart`指定した場合、オプション`-R, --role`は無効になります。

### --skip-restart {#skip-restart}

`tiup cluster reload`コマンドは 2 つの操作を実行します。

-   すべてのノード構成を更新します
-   指定されたノードを再起動します

`--skip-restart`オプションを指定すると、ノードを再起動せずに構成のみが更新されるため、更新された構成は適用されず、対応するサービスの次回の再起動まで有効になりません。

-   データ型: `BOOLEAN`
-   デフォルト: false

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   デフォルト: false

### --pre-restart-script {#pre-restart-script}

> **警告：**
>
> このオプションは実験的であり、本番での展開には推奨されません。

-   リロード前にスクリプトを実行します。
-   データ型: `STRINGS`
-   このオプションは、リロードするノードで実行されるスクリプトのパスを指定します。1 `--skip-restart` `true`に設定した場合は無効になります。

### --post-restart-script {#post-restart-script}

> **警告：**
>
> このオプションは実験的であり、本番での展開には推奨されません。

-   リロード後にスクリプトを実行します。
-   データ型: `STRINGS`
-   このオプションは、ノードのリロード後に実行されるスクリプトのパスを指定します。1 `--skip-restart` `true`に設定されている場合は有効になりません。

## 出力 {#output}

tiup-clusterの実行ログ。

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
