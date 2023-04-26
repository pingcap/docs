---
title: tiup cluster rename
---

# tiup cluster rename {#tiup-cluster-rename}

[クラスタがデプロイされました](/tiup/tiup-component-cluster-deploy.md)の場合はクラスター名を指定します。クラスターのデプロイ後にクラスター名を変更する場合は、コマンド`tiup cluster rename`使用できます。

> **ノート：**
>
> TiUPクラスターに`grafana_servers` `dashboard_dir`フィールドが構成されている場合、コマンド`tiup cluster rename`を実行してクラスターの名前を変更した後、次の追加の手順が必要です。
>
> -   ローカル ダッシュボード ディレクトリ内の`*.json`ファイルについて、各ファイルの`datasource`フィールドを新しいクラスター名に更新します。これは、 `datasource`の値がクラスターの名前でなければならないためです。
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
-   このオプションはデフォルトで無効になっており、値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`渡すか、値を何も渡さないでください。

## 出力 {#outputs}

tiup-clusterの実行ログ。

[&lt;&lt; 前のページに戻る - TiUP クラスタコマンド一覧](/tiup/tiup-component-cluster.md#command-list)
