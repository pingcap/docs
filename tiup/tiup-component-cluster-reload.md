---
title: tiup cluster reload
---

# tiup cluster reload {#tiup-cluster-reload}

[クラスター構成の変更](/tiup/tiup-component-cluster-edit-config.md)の後、構成を有効にするには、 `tiup cluster reload`コマンドを使用してクラスターをリロードする必要があります。このコマンドは、サービスが実行されているリモート マシンにコントロール マシンの構成を発行し、アップグレード プロセスに従って、アップグレード プロセスに従ってサービスを順番に再起動します。クラスターは、再起動プロセス中も引き続き使用できます。

## 構文 {#syntax}

```shell
tiup cluster reload <cluster-name> [flags]
```

`<cluster-name>` : 操作するクラスター名。

## オプション {#options}

### &#x20;--force {#force}

-   リロード プロセスのエラーを無視し、リロードを強制します。
-   データ型: `BOOLEAN`
-   デフォルト: false

### --transfer-timeout {#transfer-timeout}

-   PD または TiKV を再起動すると、再起動したノードのリーダーが最初に他のノードに移行され、移行プロセスに時間がかかります。 `-transfer-timeout`を設定すると、最大待機時間 (秒単位) を設定できます。タイムアウト後、サービスは待機せずに直接再起動できます。
-   データ型: `UINT`
-   デフォルト: 300

> **ノート：**
>
> 待機をスキップして直接再起動した場合、サービスのパフォーマンスが低下する可能性があります。

### --ignore-config-check {#ignore-config-check}

-   コンポーネントのバイナリ ファイルがデプロイされた後、TiDB、TiKV、および PD コンポーネントの構成が`<binary> --config-check <config-file>`を使用してチェックされます。 `<binary>`は、デプロイされたバイナリ ファイルのパスです。 `<config-file>`は、ユーザー構成に基づいて生成された構成ファイルです。このチェックをスキップしたい場合は、このオプションを使用できます。
-   データ型: `BOOLEAN`
-   デフォルト: false

### -N, --ノード {#n-node}

-   再起動するノードを指定します。指定しない場合、すべてのノードが再起動されます。このオプションの値は、ノード ID のコンマ区切りリストです。ノード ID は、 [`tiup cluster display`](/tiup/tiup-component-cluster-display.md)コマンドによって返されるクラスター ステータス テーブルの最初の列から取得できます。
-   データ型: `STRINGS`
-   このオプションがコマンドで指定されていない場合、デフォルトですべてのノードが選択されます。

> **ノート：**
>
> -   `-R, --role`オプションを同時に指定した場合、 `-N, --node`と`-R, --role`の両方の指定に一致するサービスノードのみが再起動されます。
> -   オプション`--skip-restart`を指定した場合、オプション`-N, --node`は無効です。

### -R, --role {#r-role}

-   再開するロールを指定します。指定しない場合、すべてのロールが再起動されます。このオプションの値は、ノード ロールのコンマ区切りリストです。ロールは[クラスターの状態](/tiup/tiup-component-cluster-display.md)テーブルの 2 番目の列です。
-   データ型: `STRINGS`
-   このオプションがコマンドで指定されていない場合、デフォルトですべてのロールが選択されます。

> **ノート：**
>
> 1.  `-N, --node`オプションを同時に指定した場合、 `-N, --node`と`-R, --role`の両方の指定に一致するサービスノードのみが再起動されます。
> 2.  オプション`--skip-restart`を指定した場合、オプション`-R, --role`は無効です。

### --skip-restart {#skip-restart}

`tiup cluster reload`コマンドは、次の 2 つの操作を実行します。

-   すべてのノード構成を更新します
-   指定したノードを再起動します

`--skip-restart`オプションを指定すると、ノードを再起動せずに構成のみが更新されるため、更新された構成は適用されず、対応するサービスが次に再起動されるまで有効になりません。

-   データ型: `BOOLEAN`
-   デフォルト: false

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   デフォルト: false

## 出力 {#output}

tiup-clusterの実行ログ。

[&lt;&lt; 前のページに戻る - TiUP クラスタコマンド一覧](/tiup/tiup-component-cluster.md#command-list)
