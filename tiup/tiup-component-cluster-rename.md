---
title: tiup cluster rename
---

# tiup cluster rename {#tiup-cluster-rename}

[クラスタがデプロイされました](/tiup/tiup-component-cluster-deploy.md)の場合はクラスタ名を指定します。クラスタのデプロイ後にクラスタ名を変更する場合は、コマンド`tiup cluster rename`を使用できます。

> **ノート：**
>
> `grafana_servers`のフィールドのうち`dashboard_dir`のフィールドが TiUPクラスタに構成されている場合、コマンド`tiup cluster rename`を実行してクラスタの名前を変更した後、次の追加の手順が必要です。
>
> -   ローカル ダッシュボード ディレクトリの`*.json`ファイルについて、各ファイルの`datasource`フィールドを新しいクラスタ名に更新します。これは、 `datasource`の値がクラスタの名前でなければならないためです。
> -   コマンド`tiup cluster reload -R grafana`を実行します。

## 構文 {#syntax}

```shell
tiup cluster rename <old-cluster-name> <new-cluster-name> [flags]
```

-   `<old-cluster-name>` : 古いクラスタ名。
-   `<new-cluster-name>` : 新しいクラスタ名。

## オプション {#options}

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで無効になっており、値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`を渡すか、値を何も渡さないでください。

## 出力 {#outputs}

tiup-cluster の実行ログ。

[&lt;&lt; 前のページに戻る - TiUP Clusterコマンド一覧](/tiup/tiup-component-cluster.md#command-list)
