---
title: tiup dm edit-config
---

# tiup dm edit-config {#tiup-dm-edit-config}

クラスタのデプロイ後にクラスタサービス構成を変更する必要がある場合は、エディターを起動する`tiup dm edit-config`コマンドを使用して、 [トポロジーファイル](/tiup/tiup-dm-topology-reference.md)を変更できます。指定されたクラスタの。このエディターは、デフォルトで`$EDITOR`環境変数で指定されています。 `$EDITOR`環境変数が存在しない場合は、 `vi`エディターが使用されます。

> **ノート：**
>
> -   構成を変更する場合、マシンを追加または削除することはできません。マシンの追加方法については、 [クラスタをスケールアウトする](/tiup/tiup-component-dm-scale-out.md)を参照してください。マシンを削除する方法については、 [クラスタでのスケーリング](/tiup/tiup-component-dm-scale-in.md)を参照してください。
> -   `tiup dm edit-config`コマンドを実行すると、制御マシンでのみ構成が変更されます。次に、 `tiup dm reload`コマンドを実行して構成を再ロードする必要があります。

## 構文 {#syntax}

```shell
tiup dm edit-config <cluster-name> [flags]
```

`<cluster-name>` ：操作するクラスタ。

## オプション {#option}

### -h、-help {#h-help}

-   ヘルプ情報を出力します。
-   データ型： `BOOLEAN`
-   デフォルト：false

## 出力 {#output}

-   通常、出力はありません。
-   変更できないフィールドを誤って変更した場合、ファイルを保存するとエラーが報告され、ファイルを再度編集するように通知されます。変更できないフィールドについては、 [トポロジファイル](/tiup/tiup-dm-topology-reference.md)を参照してください。

[&lt;&lt;前のページに戻るTiUP DMコマンドリスト](/tiup/tiup-component-dm.md#command-list)
