---
title: tiup cluster import
summary: TiUP クラスタ は、TiDB クラスターを TiDB Ansible からTiUPに転送して管理するための `import` コマンドを提供します。特定の構成のクラスターには `import` を使用しないでください。インポート プロセスをカスタマイズするには、`--dir` や `--renameなどのオプションを使用します。
---

# tiup cluster import {#tiup-cluster-import}

TiDB v4.0 より前では、TiDB クラスターは主に TiDB Ansible を使用してデプロイされていました。TiDB v4.0 以降のリリースでは、 TiUP クラスタ は、クラスターを管理用のtiup-clusterコンポーネントに転送する`import`コマンドを提供します。

> **注記：**
>
> -   管理のために TiDB Ansible 構成をTiUPにインポートした後は、クラスター操作に TiDB Ansible を使用**しないでください**。そうしないと、メタ情報の不一致により競合が発生する可能性があります。
> -   TiDB Ansible を使用してデプロイされたクラスターが次のいずれかの状況にある場合は、 `import`コマンドを使用しないでください。
>     -   TLS暗号化が有効になっているクラスター
>     -   純粋な KV クラスター (TiDB インスタンスのないクラスター)
>     -   Kafka が有効になっているクラスター
>     -   Spark が有効になっているクラスター
>     -   TiDB Lightning/TiKV インポーターが有効になっているクラスター
>     -   監視メトリックを収集するために古い`push`モードをまだ使用しているクラスター (デフォルト モード`pull`を変更しない場合は、 `import`コマンドの使用がサポートされます)
>     -   デフォルト以外のポート（ `group_vars`ディレクトリで設定されたポートは互換性がある）が`node_exporter_port` / `blackbox_exporter_port`を使用して`inventory.ini`構成ファイルで個別に設定されているクラスタ
> -   TiDB Ansible を使用してデプロイされたクラスター内の一部のノードが監視コンポーネントなしでデプロイされている場合は、まず TiDB Ansible を使用して`inventory.ini`ファイルの`monitored_servers`セクションに対応するノード情報を追加し、次に`deploy.yaml`プレイブックを使用して監視コンポーネントを完全にデプロイする必要があります。そうしないと、クラスターをTiUPにインポートした後にメンテナンス操作を実行すると、監視コンポーネントが不足しているためにエラーが発生する可能性があります。

## 構文 {#syntax}

```shell
tiup cluster import [flags]
```

## オプション {#options}

### -d, --dir {#d-dir}

-   TiDB Ansible が配置されているディレクトリを指定します。
-   データ型: `STRING`
-   このオプションは、現在のディレクトリ (デフォルト値) が渡され、デフォルトで有効になります。

### --ansible-config {#ansible-config}

-   Ansible 構成ファイルのパスを指定します。
-   データ型: `STRING`
-   このオプションは、 `. /ansible.cfg` (デフォルト値) が渡されるとデフォルトで有効になります。

### &#x20;--inventory {#inventory}

-   Ansible インベントリ ファイルの名前を指定します。
-   データ型: `STRING`
-   このオプションはデフォルトで有効になっており、 `inventory.ini` (デフォルト値) が渡されます。

### --no-backup {#no-backup}

-   TiDB Ansible が配置されているディレクトリ内のファイルのバックアップを無効にするかどうかを制御します。
-   データ型: `BOOLEAN`
-   このオプションは、デフォルトで値`false`で無効になっています。インポートが成功すると、オプション`-dir`で指定されたディレクトリ内のすべてのものがディレクトリ`${TIUP_HOME}/.tiup/storage/cluster/clusters/{cluster-name}/ansible-backup`にバックアップされます。このディレクトリに複数のインベントリ ファイルがある場合 (複数のクラスターがデプロイされている場合)、このオプションを有効にすることをお勧めします。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`を渡すか、値を渡さないようにする必要があります。

### --rename {#rename}

-   インポートされたクラスターの名前を変更します。
-   データ型: `STRING`
-   デフォルト: NULL。このオプションがコマンドで指定されていない場合は、インベントリで指定された cluster_name がクラスター名として使用されます。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションは、値`false`でデフォルトで無効になっています。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`を渡すか、値を渡さないようにする必要があります。

## 出力 {#output}

インポート プロセスのログを表示します。

[&lt;&lt; 前のページに戻る - TiUP クラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
