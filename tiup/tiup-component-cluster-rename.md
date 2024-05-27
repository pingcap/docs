---
title: tiup cluster rename
summary: tiup cluster rename コマンドは、デプロイ後にクラスター名を変更するために使用されます。`grafana_servers` の `dashboard_dir` フィールドがTiUPクラスター用に構成されている場合は、追加の手順が必要です。コマンドの構文は `tiup cluster rename <old-cluster-name> <new-cluster-name>` です。`-h, --help` オプションはヘルプ情報を出力。出力はtiup-clusterの実行ログです。
---

# tiup cluster rename {#tiup-cluster-rename}

[クラスターが展開される](/tiup/tiup-component-cluster-deploy.md)ときにクラスター名を指定します。クラスターをデプロイした後にクラスター名を変更する場合は、コマンド`tiup cluster rename`を使用します。

> **注記：**
>
> TiUPクラスターの`dashboard_dir`フィールドが`grafana_servers`に設定されている場合、コマンド`tiup cluster rename`を実行してクラスターの名前を変更した後、次の追加手順が必要になります。
>
> -   ローカル ダッシュボード ディレクトリ内の`*.json`ファイルについては、各ファイルの`datasource`フィールドを新しいクラスター名に更新します。これは、 `datasource`の値がクラスターの名前である必要があるためです。
> -   コマンド`tiup cluster reload -R grafana`を実行します。

## 構文 {#syntax}

```shell
tiup cluster rename <old-cluster-name> <new-cluster-name> [flags]
```

-   `<old-cluster-name>` : 古いクラスター名。
-   `<new-cluster-name>` : 新しいクラスター名。

## オプション {#options}

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションは、デフォルトで値`false`で無効になっています。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`を渡すか、値を渡さないようにする必要があります。

## 出力 {#outputs}

tiup-clusterの実行ログ。

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
