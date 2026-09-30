---
title: tiup cluster rename
summary: "`tiup cluster rename`コマンドは、デプロイ後にクラスター名を変更するために使用します。TiUP クラスター用に `grafana_servers` の `dashboard_dir` フィールドが設定されている場合は、追加の手順が必要です。このコマンドの構文は `tiup cluster rename <old-cluster-name> <new-cluster-name>` です。`-h, --help`オプションはヘルプ情報を出力します。出力はtiup-clusterの実行ログです。"
---

# tiup cluster rename {#tiup-cluster-rename}

クラスター名は[クラスターのデプロイ時](/tiup/tiup-component-cluster-deploy.md)に指定します。クラスターをデプロイした後にクラスター名を変更する場合は、コマンド`tiup cluster rename`を使用します。

> **Note:**
>
> TiUPクラスターで`grafana_servers`の`dashboard_dir`フィールドが設定されている場合、コマンド`tiup cluster rename`を実行してクラスターの名前を変更した後、次の追加手順が必要になります。
>
> - ローカル ダッシュボード ディレクトリ内の`*.json`ファイルについては、各ファイルの`datasource`フィールドを新しいクラスター名に更新します。`datasource`の値はクラスターの名前である必要があるためです。
> - コマンド`tiup cluster reload -R grafana`を実行します。

## 構文 {#syntax}

```shell
tiup cluster rename <old-cluster-name> <new-cluster-name> [flags]
```

- `<old-cluster-name>` : 古いクラスター名。
- `<new-cluster-name>` : 新しいクラスター名。

## オプション {#options}

### -h, --help {#h-help}

- ヘルプ情報を出力します。
- データ型: `BOOLEAN`
- このオプションはデフォルトで値`false`で無効になっています。このオプションを有効にするには、コマンドにこのオプションを追加し、値`true`を渡すか、値を渡さないかのいずれかを選択します。

## 出力 {#outputs}

tiup-clusterの実行ログ。

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
