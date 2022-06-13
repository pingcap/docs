---
title: tiup cluster edit-config
---

# tiup cluster edit-config {#tiup-cluster-edit-config}

クラスタのデプロイ後にクラスタ構成を変更する必要がある場合は、エディターを起動する`tiup cluster edit-config`コマンドを使用して、クラスタの[トポロジーファイル](/tiup/tiup-cluster-topology-reference.md)を変更できます。このエディターは、デフォルトで`$EDITOR`環境変数で指定されています。 `$EDITOR`環境変数が存在しない場合は、 `vi`エディターが使用されます。

> **ノート：**
>
> -   構成を変更する場合、マシンを追加または削除することはできません。マシンの追加方法については、 [クラスタをスケールアウトする](/tiup/tiup-component-cluster-scale-out.md)を参照してください。マシンを削除する方法については、 [クラスタでのスケーリング](/tiup/tiup-component-cluster-scale-in.md)を参照してください。
> -   `tiup cluster edit-config`コマンドを実行すると、制御マシンでのみ構成が変更されます。次に、 `tiup cluster reload`コマンドを実行して構成を再ロードする必要があります。

## 構文 {#syntax}

```shell
tiup cluster edit-config <cluster-name> [flags]
```

`<cluster-name>`は操作するクラスタです。

## オプション {#option}

### -h、-help {#h-help}

-   ヘルプ情報を印刷します。
-   データ型： `BOOLEAN`
-   このオプションはデフォルトで無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加して、 `true`の値を渡すか、値を渡さないようにします。

## 出力 {#output}

-   コマンドが正常に実行された場合、出力はありません。
-   変更できないフィールドを誤って変更した場合、ファイルを保存するとエラーが報告され、ファイルを再度編集するように通知されます。変更できないフィールドについては、 [トポロジーファイル](/tiup/tiup-cluster-topology-reference.md)を参照してください。

[&lt;&lt;前のページに戻る-TiUPClusterコマンドリスト](/tiup/tiup-component-cluster.md#command-list)
