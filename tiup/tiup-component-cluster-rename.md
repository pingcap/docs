---
title: tiup cluster rename
---

# tiup cluster rename {#tiup-cluster-rename}

[クラスターがデプロイされています](/tiup/tiup-component-cluster-deploy.md)の場合はクラスタ名を指定します。クラスターのデプロイ後にクラスター名を変更する場合は、コマンド`tiup cluster rename`使用できます。

> **注記：**
>
> TiUPクラスターに対して`grafana_servers` `dashboard_dir`フィールドが構成されている場合は、コマンド`tiup cluster rename`を実行してクラスターの名前を変更した後、次の追加手順が必要です。
>
> -   ローカル ダッシュボード ディレクトリ内の`*.json`ファイルについては、値`datasource`がクラスターの名前である必要があるため、各ファイルの`datasource`フィールドを新しいクラスター名に更新します。
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
-   このオプションは、値`false`を指定するとデフォルトで無効になります。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`渡すか、値を渡しません。

## 出力 {#outputs}

tiup-clusterの実行ログ。

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
