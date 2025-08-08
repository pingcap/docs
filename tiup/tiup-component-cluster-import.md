---
title: tiup cluster import
summary: TiUP クラスタは、TiDB AnsibleからTiUPにTiDBクラスターを転送して管理するための「import」コマンドを提供しています。特定の構成のクラスターでは「import」を使用しないでください。インポートプロセスをカスタマイズするには、「--dir」や「--rename」などのオプションを使用してください。
---

# tiup cluster import {#tiup-cluster-import}

TiDB v4.0より前のバージョンでは、TiDBクラスターは主にTiDB Ansibleを使用してデプロイされていました。TiDB v4.0以降のリリースでは、 TiUP クラスタは、クラスターを管理用のtiup-clusterコンポーネントに転送するためのコマンド`import`を提供します。

> **注記：**
>
> -   TiDB Ansible設定を管理用にTiUPにインポートした後は、クラスタ操作にTiDB Ansibleを使用し**ないでください**。メタ情報の不一致により競合が発生する可能性があります。
> -   TiDB Ansible を使用してデプロイされたクラスターが次のいずれかの状況にある場合は、 `import`コマンドを使用しないでください。
>     -   TLS暗号化が有効になっているクラスター
>     -   純粋な KV クラスター (TiDB インスタンスのないクラスター)
>     -   Kafka が有効になっているクラスター
>     -   Sparkが有効になっているクラスター
>     -   TiDB Lightning/TiKVインポーターが有効になっているクラスター
>     -   監視メトリックを収集するために古いモード`push`をまだ使用しているクラスター (デフォルト モード`pull`を変更しない場合は、 `import`コマンドの使用がサポートされます)
>     -   デフォルト以外のポート（ `group_vars`ディレクトリに設定されているポートは互換性がある）が`node_exporter_port` / `blackbox_exporter_port`を使用して`inventory.ini`構成ファイルで個別に設定されているクラスタ
> -   TiDB Ansibleを使用してデプロイしたクラスター内の一部のノードに監視コンポーネントがデプロイされていない場合は、まずTiDB Ansibleを使用して`inventory.ini`ファイルの`monitored_servers`セクションに対応するノード情報を追加し、その後`deploy.yaml`プレイブックを使用して監視コンポーネントを完全にデプロイする必要があります。そうしないと、クラスターをTiUPにインポートした後にメンテナンス操作を実行すると、監視コンポーネントの不足によりエラーが発生する可能性があります。

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
-   このオプションはデフォルトで有効になっており、 `. /ansible.cfg` (デフォルト値) が渡されます。

### &#x20;--inventory {#inventory}

-   Ansible インベントリ ファイルの名前を指定します。
-   データ型: `STRING`
-   このオプションはデフォルトで有効になっており、 `inventory.ini` (デフォルト値) が渡されます。

### --no-backup {#no-backup}

-   TiDB Ansible が配置されているディレクトリ内のファイルのバックアップを無効にするかどうかを制御します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで値`false`に設定されており、無効になっています。インポートが成功すると、オプション`-dir`で指定されたディレクトリ内のすべてのデータがディレクトリ`${TIUP_HOME}/.tiup/storage/cluster/clusters/{cluster-name}/ansible-backup`にバックアップされます。このディレクトリに複数のインベントリファイルがある場合（複数のクラスタがデプロイされている場合）、このオプションを有効にすることをお勧めします。このオプションを有効にするには、コマンドにこのオプションを追加し、値`true`を渡すか、値を渡さないでください。

### --rename {#rename}

-   インポートされたクラスターの名前を変更します。
-   データ型: `STRING`
-   デフォルト: NULL。このオプションがコマンドで指定されていない場合、インベントリで指定されたcluster_nameがクラスター名として使用されます。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで値`false`で無効になっています。このオプションを有効にするには、コマンドにこのオプションを追加し、値`true`を渡すか、値を渡さないでください。

## 出力 {#output}

インポート プロセスのログを表示します。

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
