---
title: tiup cluster import
---

# tiup cluster import {#tiup-cluster-import}

TiDB v4.0 より前は、TiDB クラスターは主に TiDB Ansible を使用してデプロイされていました。 TiDB v4.0 以降のリリースの場合、 TiUPクラスタは、管理のためにクラスターをtiup-clusterコンポーネントに転送する`import`コマンドを提供します。

> **注記：**
>
> -   管理のために TiDB Ansible 構成をTiUPにインポートした後は、クラスター操作に TiDB Ansible を使用し**ないでください**。そうしないと、メタ情報の不一致により競合が発生する可能性があります。
> -   TiDB Ansible を使用してデプロイされたクラスターが次のいずれかの状況にある場合は、 `import`コマンドを使用しないでください。
>     -   TLS 暗号化が有効になっているクラスター
>     -   純粋な KV クラスター (TiDB インスタンスのないクラスター)
>     -   Kafka が有効になっているクラスター
>     -   Spark が有効になっているクラスター
>     -   TiDB Lightning/TiKV インポーターが有効になっているクラスター
>     -   クラスターは監視メトリックを収集するために古い`push`モードを引き続き使用します (デフォルトのモード`pull`を変更しない場合、 `import`コマンドの使用がサポートされます)。
>     -   デフォルト以外のポート ( `group_vars`ディレクトリで設定されたポートは互換性がある) が`node_exporter_port` / `blackbox_exporter_port`を使用して`inventory.ini`設定ファイルで個別に設定されているクラスタ
> -   TiDB Ansible を使用してデプロイされたクラスター内の一部のノードがモニタリング コンポーネントなしでデプロイされている場合は、まず TiDB Ansible を使用して、対応するノード情報を`inventory.ini`ファイルの`monitored_servers`セクションに追加し、次に`deploy.yaml`プレイブックを使用してモニタリング コンポーネントを完全にデプロイする必要があります。そうしないと、クラスターがTiUPにインポートされた後にメンテナンス操作を実行するときに、監視コンポーネントの不足によりエラーが発生する可能性があります。

## 構文 {#syntax}

```shell
tiup cluster import [flags]
```

## オプション {#options}

### -d、--dir {#d-dir}

-   TiDB Ansible が配置されているディレクトリを指定します。
-   データ型: `STRING`
-   このオプションは、現在のディレクトリ (デフォルト値) が渡されることでデフォルトで有効になります。

### --ansible-config {#ansible-config}

-   Ansible 構成ファイルのパスを指定します。
-   データ型: `STRING`
-   このオプションは、 `. /ansible.cfg` (デフォルト値) が渡されるとデフォルトで有効になります。

### &#x20;--inventory {#inventory}

-   Ansible インベントリー ファイルの名前を指定します。
-   データ型: `STRING`
-   このオプションは、 `inventory.ini` (デフォルト値) が渡されるとデフォルトで有効になります。

### --no-backup {#no-backup}

-   TiDB Ansible が配置されているディレクトリ内のファイルのバックアップを無効にするかどうかを制御します。
-   データ型: `BOOLEAN`
-   このオプションは、値`false`を指定するとデフォルトで無効になります。インポートが成功すると、 `-dir`オプションで指定したディレクトリ内のすべてが`${TIUP_HOME}/.tiup/storage/cluster/clusters/{cluster-name}/ansible-backup`ディレクトリにバックアップされます。このディレクトリに複数のインベントリ ファイルがある場合 (複数のクラスターがデプロイされている場合)、このオプションを有効にすることをお勧めします。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`渡すか、値を渡しません。

### --rename {#rename}

-   インポートされたクラスターの名前を変更します。
-   データ型: `STRING`
-   デフォルト: NULL。コマンドでこのオプションを指定しない場合は、inventory で指定したクラスター名がクラスター名として使用されます。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションは、値`false`を指定するとデフォルトで無効になります。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`渡すか、値を渡しません。

## 出力 {#output}

インポートプロセスのログを表示します。

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
