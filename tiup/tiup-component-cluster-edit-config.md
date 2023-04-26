---
title: tiup cluster edit-config
---

# tiup cluster edit-config {#tiup-cluster-edit-config}

クラスターのデプロイ後にクラスター構成を変更する必要がある場合は、エディターを開始する`tiup cluster edit-config`コマンドを使用して、クラスターの[トポロジ ファイル](/tiup/tiup-cluster-topology-reference.md)変更できます。このエディタは、デフォルトで環境変数`$EDITOR`に指定されています。 `$EDITOR`環境変数が存在しない場合、 `vi`エディターが使用されます。

> **ノート：**
>
> -   構成を変更すると、マシンを追加または削除できなくなります。マシンを追加する方法については、 [クラスターをスケールアウトする](/tiup/tiup-component-cluster-scale-out.md)を参照してください。マシンの削除方法については、 [クラスターでのスケールイン](/tiup/tiup-component-cluster-scale-in.md)参照してください。
> -   `tiup cluster edit-config`コマンドを実行すると、構成は制御マシンでのみ変更されます。次に、 `tiup cluster reload`コマンドを実行して構成をリロードする必要があります。

## 構文 {#syntax}

```shell
tiup cluster edit-config <cluster-name> [flags]
```

`<cluster-name>`は、操作するクラスターです。

## オプション {#option}

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加して、値`true`渡すか、値を何も渡さないようにします。

## 出力 {#output}

-   コマンドが正常に実行された場合、出力はありません。
-   変更できないフィールドを誤って変更した場合は、ファイルを保存するときにエラーが報告され、ファイルを再度編集するように促されます。変更できないフィールドについては、 [トポロジ ファイル](/tiup/tiup-cluster-topology-reference.md)を参照してください。

[&lt;&lt; 前のページに戻る - TiUP クラスタコマンド一覧](/tiup/tiup-component-cluster.md#command-list)
