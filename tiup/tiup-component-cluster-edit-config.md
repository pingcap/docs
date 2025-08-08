---
title: tiup cluster edit-config
summary: tiup cluster edit-config` コマンドを使用すると、デプロイメント後にクラスタ構成を変更できます。エディタを使用して、`$EDITOR` 環境変数で指定されたトポロジファイルを変更できます。構成の変更時にマシンを追加または削除することはできないことに注意してください。コマンド実行後、構成はコントロールマシン上でのみ変更されるため、`tiup cluster reload` を実行して構成を再読み込みする必要があります。
---

# tiup cluster edit-config {#tiup-cluster-edit-config}

クラスタのデプロイ後にクラスタ設定を変更する必要がある場合は、 `tiup cluster edit-config`コマンドを使用してエディタを起動し、クラスタの[トポロジファイル](/tiup/tiup-cluster-topology-reference.md)編集できます。このエディタは、デフォルトで`$EDITOR`環境変数に指定されています。7 環境変数が存在しない場合は、 `$EDITOR`エディタ`vi`使用されます。

> **注記：**
>
> -   設定を変更すると、マシンの追加や削除はできなくなります。マシンの追加方法については[クラスターをスケールアウトする](/tiup/tiup-component-cluster-scale-out.md)参照してください。マシンの削除方法については[クラスターのスケールイン](/tiup/tiup-component-cluster-scale-in.md)参照してください。
> -   `tiup cluster edit-config`コマンドを実行すると、コントロールマシン上でのみ設定が変更されます。その後、 `tiup cluster reload`コマンドを実行して設定を再読み込みする必要があります。

## 構文 {#syntax}

```shell
tiup cluster edit-config <cluster-name> [flags]
```

`<cluster-name>`は操作対象のクラスターです。

## オプション {#option}

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで無効になっており、デフォルト値は`false`です。このオプションを有効にするには、コマンドにこのオプションを追加し、値`true`を渡すか、値を渡さないかのいずれかを選択します。

## 出力 {#output}

-   コマンドが正常に実行された場合、出力はありません。
-   変更できないフィールドを誤って変更した場合、ファイルを保存するとエラーが表示され、再度編集する必要があることが通知されます。変更できないフィールドについては、 [トポロジファイル](/tiup/tiup-cluster-topology-reference.md)参照してください。

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
