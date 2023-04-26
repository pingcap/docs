---
title: tiup dm edit-config
---

# tiup dm edit-config {#tiup-dm-edit-config}

クラスターのデプロイ後にクラスター サービス構成を変更する必要がある場合は、エディターを起動する`tiup dm edit-config`コマンドを使用して[トポロジ ファイル](/tiup/tiup-dm-topology-reference.md)を変更できます。指定されたクラスターの。このエディタは、デフォルトで環境変数`$EDITOR`に指定されています。 `$EDITOR`環境変数が存在しない場合、 `vi`エディターが使用されます。

> **ノート：**
>
> -   構成を変更すると、マシンを追加または削除できなくなります。マシンを追加する方法については、 [クラスターをスケールアウトする](/tiup/tiup-component-dm-scale-out.md)を参照してください。マシンの削除方法については、 [クラスターでのスケールイン](/tiup/tiup-component-dm-scale-in.md)参照してください。
> -   `tiup dm edit-config`コマンドを実行すると、構成は制御マシンでのみ変更されます。次に、 `tiup dm reload`コマンドを実行して構成をリロードする必要があります。

## 構文 {#syntax}

```shell
tiup dm edit-config <cluster-name> [flags]
```

`<cluster-name>` : 操作するクラスター。

## オプション {#option}

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   デフォルト: false

## 出力 {#output}

-   通常、出力はありません。
-   変更できないフィールドを誤って変更した場合、ファイルを保存するときにエラーが報告され、ファイルを再度編集するように促されます。変更できないフィールドについては、 [トポロジーファイル](/tiup/tiup-dm-topology-reference.md)を参照してください。

[&lt;&lt; 前のページに戻る - TiUP DMコマンド一覧](/tiup/tiup-component-dm.md#command-list)
