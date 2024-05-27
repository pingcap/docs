---
title: tiup cluster reload
summary: tiup cluster reload コマンドは、変更されたクラスター構成を適用し、サービスを再起動するために使用されます。`--force` で強制実行、`--transfer-timeout` で転送タイムアウトを設定、`--ignore-config-check` で構成チェックを無視、`-N、--node` でノードを指定、`-R、--role` でロールを指定、`--skip-restart` で再起動をスキップすることができます。出力はtiup-clusterの実行ログです。
---

# tiup cluster reload {#tiup-cluster-reload}

[クラスタ構成の変更](/tiup/tiup-component-cluster-edit-config.md)の後、設定を有効にするには、 `tiup cluster reload`コマンドを使用してクラスターをリロードする必要があります。このコマンドは、サービスが実行されているリモート マシンに制御マシンの設定を公開し、アップグレード プロセスに従ってサービスを順番に再起動します。クラスターは、再起動プロセス中も引き続き使用できます。

## 構文 {#syntax}

```shell
tiup cluster reload <cluster-name> [flags]
```

`<cluster-name>` : 操作するクラスター名。

## オプション {#options}

### &#x20;--force {#force}

-   再ロード プロセス中のエラーを無視し、強制的に再ロードします。
-   データ型: `BOOLEAN`
-   デフォルト: false

### --transfer-timeout {#transfer-timeout}

-   PD または TiKV を再起動する場合、再起動されたノードのリーダーが最初に他のノードに移行されるため、移行プロセスには時間がかかります。 `-transfer-timeout`設定すると、最大待機時間 (秒単位) を設定できます。タイムアウト後、サービスは待機せずに直接再起動できます。
-   データ型: `UINT`
-   デフォルト: 600

> **注記：**
>
> 待機をスキップして直接再起動する場合、サービスのパフォーマンスが不安定になる可能性があります。

### --設定チェックを無視 {#ignore-config-check}

-   コンポーネントのバイナリ ファイルがデプロイされた後、 `<binary> --config-check <config-file>`使用して TiDB、TiKV、および PD コンポーネントの構成がチェックされます。3 `<binary>`デプロイされたバイナリ ファイルのパスです。5 `<config-file>` 、ユーザー構成に基づいて生成された構成ファイルです。このチェックをスキップする場合は、このオプションを使用できます。
-   データ型: `BOOLEAN`
-   デフォルト: false

### -N、--ノード {#n-node}

-   再起動するノードを指定します。指定しない場合は、すべてのノードが再起動されます。 [`tiup cluster display`](/tiup/tiup-component-cluster-display.md)オプションの値は、ノード ID のコンマ区切りリストです。1 コマンドによって返されるクラスター ステータス テーブルの最初の列からノード ID を取得できます。
-   データ型: `STRINGS`
-   このオプションがコマンドで指定されていない場合は、デフォルトですべてのノードが選択されます。

> **注記：**
>
> -   `-R, --role`オプションを同時に指定した場合は、 `-N, --node`と`-R, --role`の両方の指定に一致するサービス ノードのみが再起動されます。
> -   `--skip-restart`オプションが指定されている場合、 `-N, --node`オプションは無効です。

### -R, --役割 {#r-role}

-   再起動するロールを指定します。指定しない場合は、すべてのロールが再起動されます。このオプションの値は、ノード ロールのコンマ区切りリストです。ロールは、 [クラスターステータス](/tiup/tiup-component-cluster-display.md)テーブルの 2 番目の列です。
-   データ型: `STRINGS`
-   コマンドでこのオプションが指定されていない場合は、すべてのロールがデフォルトで選択されます。

> **注記：**
>
> 1.  `-N, --node`オプションを同時に指定した場合は、 `-N, --node`と`-R, --role`の両方の指定に一致するサービス ノードのみが再起動されます。
> 2.  `--skip-restart`オプションが指定されている場合、 `-R, --role`オプションは無効です。

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

## 出力 {#output}

tiup-clusterの実行ログ。

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
