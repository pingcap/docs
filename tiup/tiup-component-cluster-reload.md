---
title: tiup cluster reload
---

# tiup cluster reload {#tiup-cluster-reload}

[クラスタ構成の変更](/tiup/tiup-component-cluster-edit-config.md)の後、構成を有効にするには、 `tiup cluster reload`コマンドを使用してクラスターをリロードする必要があります。このコマンドは、サービスが実行されているリモート マシンに制御マシンの構成を公開し、アップグレード プロセスに従ってサービスを順番に再起動します。クラスターは再起動プロセス中も引き続き使用できます。

## 構文 {#syntax}

```shell
tiup cluster reload <cluster-name> [flags]
```

`<cluster-name>` : 操作対象のクラスター名。

## オプション {#options}

### &#x20;--force {#force}

-   リロードプロセスのエラーを無視し、強制的にリロードします。
-   データ型: `BOOLEAN`
-   デフォルト: false

### --transfer-timeout {#transfer-timeout}

-   PD または TiKV を再起動すると、再起動されたノードのリーダーが最初に他のノードに移行されるため、移行プロセスに時間がかかります。 `-transfer-timeout`を設定すると、最大待機時間 (秒単位) を設定できます。タイムアウト後、サービスは待たずに直接再起動できます。
-   データ型: `UINT`
-   デフォルト: 600

> **注記：**
>
> 待機をスキップして直接再起動すると、サービスのパフォーマンスが不安定になる可能性があります。

### --ignore-config-check {#ignore-config-check}

-   コンポーネントのバイナリ ファイルがデプロイされた後、TiDB、TiKV、および PD コンポーネントの構成が`<binary> --config-check <config-file>`を使用してチェックされます。 `<binary>`は、デプロイされたバイナリ ファイルのパスです。 `<config-file>`はユーザー設定に基づいて生成された設定ファイルです。このチェックをスキップしたい場合は、このオプションを使用できます。
-   データ型: `BOOLEAN`
-   デフォルト: false

### -N、--node {#n-node}

-   再起動するノードを指定します。指定しない場合、すべてのノードが再起動されます。このオプションの値は、ノード ID のカンマ区切りリストです。ノード ID は、 [`tiup cluster display`](/tiup/tiup-component-cluster-display.md)コマンドによって返されるクラスター ステータス テーブルの最初の列から取得できます。
-   データ型: `STRINGS`
-   このオプションがコマンドで指定されていない場合、デフォルトですべてのノードが選択されます。

> **注記：**
>
> -   `-R, --role`オプションを同時に指定した場合、 `-N, --node`と`-R, --role`の両方の指定に一致するサービスノードだけが再起動されます。
> -   `--skip-restart`オプションを指定した場合、 `-N, --node`オプションは無効になります。

### -R、--役割 {#r-role}

-   再起動するロールを指定します。指定しない場合、すべてのロールが再起動されます。このオプションの値は、ノードの役割のカンマ区切りのリストです。ロールは[クラスタのステータス](/tiup/tiup-component-cluster-display.md)テーブルの 2 列目です。
-   データ型: `STRINGS`
-   このオプションがコマンドで指定されていない場合、デフォルトですべてのロールが選択されます。

> **注記：**
>
> 1.  `-N, --node`オプションを同時に指定した場合、 `-N, --node`と`-R, --role`の両方の指定に一致するサービスノードだけが再起動されます。
> 2.  `--skip-restart`オプションを指定した場合、 `-R, --role`オプションは無効になります。

### --skip-restart {#skip-restart}

`tiup cluster reload`コマンドは 2 つの操作を実行します。

-   すべてのノード構成を更新します
-   指定されたノードを再起動します

`--skip-restart`オプションを指定すると、ノードを再起動せずに構成のみが更新されるため、更新された構成は適用されず、対応するサービスが次に再起動されるまで有効になりません。

-   データ型: `BOOLEAN`
-   デフォルト: false

### -h, --help {#h-help}

-   ヘルプ情報を印刷します。
-   データ型: `BOOLEAN`
-   デフォルト: false

## 出力 {#output}

tiup-clusterの実行ログ。

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
