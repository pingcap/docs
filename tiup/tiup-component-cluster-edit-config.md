---
title: tiup cluster edit-config
---

# tiup cluster edit-config {#tiup-cluster-edit-config}

クラスターのデプロイ後にクラスター構成を変更する必要がある場合は、エディターを起動する`tiup cluster edit-config`コマンドを使用して、クラスターの[<a href="/tiup/tiup-cluster-topology-reference.md">トポロジファイル</a>](/tiup/tiup-cluster-topology-reference.md)変更できます。このエディタはデフォルトで`$EDITOR`環境変数に指定されています。 `$EDITOR`環境変数が存在しない場合は、 `vi`エディタが使用されます。

> **ノート：**
>
> -   構成を変更する場合、マシンを追加または削除することはできません。マシンの追加方法については、 [<a href="/tiup/tiup-component-cluster-scale-out.md">クラスターをスケールアウトする</a>](/tiup/tiup-component-cluster-scale-out.md)を参照してください。マシンの削除方法については、 [<a href="/tiup/tiup-component-cluster-scale-in.md">クラスタースケールイン</a>](/tiup/tiup-component-cluster-scale-in.md)を参照してください。
> -   `tiup cluster edit-config`コマンドを実行すると、制御マシンのみの設定が変更されます。次に、 `tiup cluster reload`コマンドを実行して構成を再ロードする必要があります。

## 構文 {#syntax}

```shell
tiup cluster edit-config <cluster-name> [flags]
```

`<cluster-name>`は操作対象のクラスターです。

## オプション {#option}

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトでは無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加して、値`true`渡すか、値を渡さないことができます。

## 出力 {#output}

-   コマンドが正常に実行された場合、出力はありません。
-   変更できないフィールドを誤って変更した場合、ファイルを保存するときにエラーが報告され、ファイルを再度編集するよう通知されます。変更できないフィールドについては、 [<a href="/tiup/tiup-cluster-topology-reference.md">トポロジファイル</a>](/tiup/tiup-cluster-topology-reference.md)を参照してください。

[<a href="/tiup/tiup-component-cluster.md#command-list">&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト</a>](/tiup/tiup-component-cluster.md#command-list)
