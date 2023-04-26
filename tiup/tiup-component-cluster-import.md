---
title: tiup cluster import
---

# tiup cluster import {#tiup-cluster-import}

TiDB v4.0 より前は、TiDB クラスターは主に TiDB Ansible を使用してデプロイされていました。 TiDB v4.0 以降のリリースの場合、 TiUPクラスタは、管理のためにクラスターをtiup-clusterコンポーネントに転送するための`import`コマンドを提供します。

> **ノート：**
>
> -   管理のために TiDB Ansible 構成をTiUPにインポートした後は、TiDB Ansible をクラスター操作に使用し**ないでください**。そうしないと、メタ情報が一致しないために競合が発生する可能性があります。
> -   TiDB Ansible を使用してデプロイされたクラスターが次のいずれかの状況にある場合は、 `import`コマンドを使用しないでください。
>     -   TLS 暗号化が有効になっているクラスター
>     -   Pure KV クラスター (TiDB インスタンスのないクラスター)
>     -   Kafka が有効になっているクラスター
>     -   Spark が有効なクラスター
>     -   TiDB Lightning/TiKV Importer が有効になっているクラスター
>     -   監視メトリクスを収集するためにまだ古い`push`モードを使用しているクラスター (デフォルト モード`pull`を変更しない場合、 `import`コマンドの使用がサポートされます)
>     -   `node_exporter_port` / `blackbox_exporter_port`を使用して、デフォルト以外のポート ( `group_vars`ディレクトリで構成されたポートに互換性がある) が`inventory.ini`の構成ファイルで個別に構成されているクラスター
> -   TiDB Ansible を使用してデプロイされたクラスター内の一部のノードが監視コンポーネントなしでデプロイされている場合、まず TiDB Ansible を使用して対応するノード情報を`inventory.ini`ファイルの`monitored_servers`セクションに追加し、次に`deploy.yaml`プレイブックを使用して監視コンポーネントを完全にデプロイする必要があります。そうしないと、クラスターがTiUPにインポートされた後に保守操作を実行するときに、監視コンポーネントの不足が原因でエラーが発生する可能性があります。

## 構文 {#syntax}

```shell
tiup cluster import [flags]
```

## オプション {#options}

### -d, --dir {#d-dir}

-   TiDB Ansible が配置されているディレクトリを指定します。
-   データ型: `STRING`
-   このオプションは、現在のディレクトリ (デフォルト値) が渡された状態でデフォルトで有効になっています。

### --ansible-config {#ansible-config}

-   Ansible 構成ファイルのパスを指定します。
-   データ型: `STRING`
-   このオプションはデフォルトで有効になっており、 `. /ansible.cfg` (デフォルト値) が渡されます。

### &#x20;--inventory {#inventory}

-   Ansible インベントリー ファイルの名前を指定します。
-   データ型: `STRING`
-   このオプションはデフォルトで有効になっており、 `inventory.ini` (デフォルト値) が渡されます。

### --no-backup {#no-backup}

-   TiDB Ansible が配置されているディレクトリ内のファイルのバックアップを無効にするかどうかを制御します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで無効になっており、値は`false`です。インポートが正常に完了すると、 `-dir`オプションで指定されたディレクトリ内のすべてが`${TIUP_HOME}/.tiup/storage/cluster/clusters/{cluster-name}/ansible-backup`ディレクトリにバックアップされます。このディレクトリに複数のインベントリ ファイルがある場合 (複数のクラスターが展開されている場合)、このオプションを有効にすることをお勧めします。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`を渡すか、値を何も渡さないでください。

### --rename {#rename}

-   インポートされたクラスターの名前を変更します。
-   データ型: `STRING`
-   デフォルト: NULL。このオプションがコマンドで指定されていない場合、インベントリーで指定された cluster_name がクラスター名として使用されます。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで無効になっており、値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`渡すか、値を何も渡さないでください。

## 出力 {#output}

インポート プロセスのログを表示します。

[&lt;&lt; 前のページに戻る - TiUP クラスタコマンド一覧](/tiup/tiup-component-cluster.md#command-list)
