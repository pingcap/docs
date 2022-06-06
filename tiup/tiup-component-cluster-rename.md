---
title: tiup cluster rename
---

# クラスタの名前変更 {#tiup-cluster-rename}

クラスタ名は[クラスタがデプロイされます](/tiup/tiup-component-cluster-deploy.md)の場合に指定されます。クラスタのデプロイ後にクラスタ名を変更する場合は、コマンド`tiup cluster rename`を使用できます。

> **ノート：**
>
> `grafana_servers`の`dashboard_dir`フィールドがTiUPクラスタ用に構成されている場合、コマンド`tiup cluster rename`を実行してクラスタの名前を変更した後、次の追加手順が必要です。
>
> -   ローカルダッシュボードディレクトリ内の`*.json`のファイルについては、各ファイルの`datasource`のフィールドを新しいクラスタ名に更新します。これは、 `datasource`の値がクラスタの名前である必要があるためです。
> -   コマンド`tiup cluster reload -R grafana`を実行します。

## 構文 {#syntax}

```shell
tiup cluster rename <old-cluster-name> <new-cluster-name> [flags]
```

-   `<old-cluster-name>` ：古いクラスタ名。
-   `<new-cluster-name>` ：新しいクラスタ名。

## オプション {#options}

### -h、-help {#h-help}

-   ヘルプ情報を出力します。
-   データ型： `BOOLEAN`
-   このオプションは、デフォルトで`false`の値で無効になっています。このオプションを有効にするには、このオプションをコマンドに追加し、 `true`の値を渡すか、値を渡さないようにします。

## 出力 {#outputs}

tiup-clusterの実行ログ。

[&lt;&lt;前のページに戻る-TiUPClusterコマンドリスト](/tiup/tiup-component-cluster.md#command-list)
