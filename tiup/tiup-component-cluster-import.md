---
title: tiup cluster import
---

# tiup cluster import {#tiup-cluster-import}

TiDB v4.0より前は、TiDBクラスターは主にTiDBAnsibleを使用してデプロイされていました。 TiDB v4.0以降のリリースでは、TiUP Clusterは、管理のためにクラスターをtiup-clusterコンポーネントに転送するための`import`のコマンドを提供します。

> **ノート：**
>
> -   管理のためにTiDBAnsible構成をTiUPにインポートした後は、クラスタ操作に**TiDBAnsible**を使用しないでください。そうしないと、一貫性のないメタ情報が原因で競合が発生する可能性があります。
> -   TiDB Ansibleを使用してデプロイされたクラスターが次のいずれかの状況にある場合は、 `import`コマンドを使用しないでください。
>     -   TLS暗号化が有効になっているクラスター
>     -   純粋なKVクラスター（TiDBインスタンスのないクラスター）
>     -   Kafkaが有効になっているクラスター
>     -   Sparkが有効になっているクラスター
>     -   TiDB Lightning/TiKVインポーターが有効になっているクラスター
>     -   監視メトリックを収集するために引き続き古い`push`モードを使用しているクラスター（デフォルトのモード`pull`を変更しない場合は、 `import`コマンドの使用がサポートされます）
>     -   デフォルト以外のポート（ `group_vars`ディレクトリで構成されたポートが互換性がある）が`node_exporter_port`を使用して`inventory.ini`構成ファイルで個別に構成されている`blackbox_exporter_port`
> -   TiDB Ansibleを使用してデプロイされたクラスタの一部のノードがモニタリングコンポーネントなしでデプロイされる場合は、最初にTiDB Ansibleを使用して対応するノード情報を`inventory.ini`ファイルの`monitored_servers`セクションに追加し、次に`deploy.yaml`プレイブックを使用してモニタリングコンポーネントを完全にデプロイする必要があります。そうしないと、クラスタがTiUPにインポートされた後に保守操作を実行するときに、監視コンポーネントが不足しているためにエラーが発生する可能性があります。

## 構文 {#syntax}

```shell
tiup cluster import [flags]
```

## オプション {#options}

### -d、-dir {#d-dir}

-   TiDBAnsibleが配置されているディレクトリを指定します。
-   データ型： `STRING`
-   このオプションは、現在のディレクトリ（デフォルト値）が渡された状態でデフォルトで有効になっています。

### --ansible-config {#ansible-config}

-   Ansible構成ファイルのパスを指定します。
-   データ型： `STRING`
-   このオプションはデフォルトで有効になっており、 `. /ansible.cfg` （デフォルト値）が渡されます。

### - 在庫 {#inventory}

-   Ansibleインベントリファイルの名前を指定します。
-   データ型： `STRING`
-   このオプションはデフォルトで有効になっており、 `inventory.ini` （デフォルト値）が渡されます。

### --バックアップなし {#no-backup}

-   TiDBAnsibleが配置されているディレクトリ内のファイルのバックアップを無効にするかどうかを制御します。
-   データ型： `BOOLEAN`
-   このオプションは、デフォルトで`false`の値で無効になっています。インポートが成功すると、 `-dir`オプションで指定されたディレクトリ内のすべてが`${TIUP_HOME}/.tiup/storage/cluster/clusters/{cluster-name}/ansible-backup`ディレクトリにバックアップされます。このディレクトリに複数のインベントリファイルがある場合（複数のクラスタが展開されている場合）、このオプションを有効にすることをお勧めします。このオプションを有効にするには、このオプションをコマンドに追加し、 `true`の値を渡すか、値を渡さないようにします。

### --名前を変更 {#rename}

-   インポートされたクラスタの名前を変更します。
-   データ型： `STRING`
-   デフォルト：NULL。コマンドでこのオプションが指定されていない場合、inventoryで指定されたcluster_nameがクラスタ名として使用されます。

### -h、-help {#h-help}

-   ヘルプ情報を出力します。
-   データ型： `BOOLEAN`
-   このオプションは、デフォルトで`false`の値で無効になっています。このオプションを有効にするには、このオプションをコマンドに追加し、 `true`の値を渡すか、値を渡さないようにします。

## 出力 {#output}

インポートプロセスのログを表示します。

[&lt;&lt;前のページに戻る-TiUPクラスターコマンドリスト](/tiup/tiup-component-cluster.md#command-list)
