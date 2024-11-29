---
title: tiup cluster edit-config
summary: tiup cluster edit-config` コマンドを使用すると、デプロイメント後にクラスター構成を変更できます。エディターを使用して、`$EDITOR` 環境変数で指定されたトポロジ ファイルを変更できます。構成を変更するときにマシンを追加または削除することはできないことに注意してください。コマンドの実行後、構成は制御マシンでのみ変更されるため、構成を再読み込みするには `tiup cluster reload` を実行する必要があります。
---

# tiup cluster edit-config {#tiup-cluster-edit-config}

クラスターのデプロイ後にクラスター構成を変更する必要がある場合は、クラスターの[トポロジファイル](/tiup/tiup-cluster-topology-reference.md)変更するためのエディターを起動する`tiup cluster edit-config`コマンドを使用できます。このエディターは、デフォルトで`$EDITOR`環境変数に指定されています`$EDITOR`環境変数が存在しない場合は、 `vi`エディターが使用されます。

> **注記：**
>
> -   設定を変更すると、マシンの追加や削除はできなくなります。マシンの追加方法については[クラスターをスケールアウトする](/tiup/tiup-component-cluster-scale-out.md)参照してください。マシンの削除方法については[クラスターのスケールイン](/tiup/tiup-component-cluster-scale-in.md)参照してください。
> -   `tiup cluster edit-config`コマンドを実行すると、コントロール マシンでのみ構成が変更されます。その後、 `tiup cluster reload`コマンドを実行して構成を再読み込みする必要があります。

## 構文 {#syntax}

```shell
tiup cluster edit-config <cluster-name> [flags]
```

`<cluster-name>`操作対象のクラスターです。

## オプション {#option}

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトでは無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`を渡すか、値を渡さないようにします。

## 出力 {#output}

-   コマンドが正常に実行された場合、出力はありません。
-   変更できないフィールドを誤って変更した場合、ファイルを保存するときにエラーが報告され、ファイルを再度編集するように通知されます。変更できないフィールドについては、 [トポロジファイル](/tiup/tiup-cluster-topology-reference.md)を参照してください。

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
