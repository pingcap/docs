---
title: tiup dm edit-config
---

# tiup dm edit-config {#tiup-dm-edit-config}

クラスターのデプロイ後にクラスター サービス構成を変更する必要がある場合は、エディターを起動する`tiup dm edit-config`コマンドを使用して[トポロジファイル](/tiup/tiup-dm-topology-reference.md)を変更できます。指定されたクラスターの。このエディタはデフォルトで`$EDITOR`環境変数に指定されています。 `$EDITOR`環境変数が存在しない場合は、 `vi`エディタが使用されます。

> **注記：**
>
> -   構成を変更する場合、マシンを追加または削除することはできません。マシンの追加方法については、 [クラスターをスケールアウトする](/tiup/tiup-component-dm-scale-out.md)を参照してください。マシンの削除方法については、 [クラスタースケールイン](/tiup/tiup-component-dm-scale-in.md)を参照してください。
> -   `tiup dm edit-config`コマンドを実行すると、制御マシンのみの設定が変更されます。次に、 `tiup dm reload`コマンドを実行して構成を再ロードする必要があります。

## 構文 {#syntax}

```shell
tiup dm edit-config <cluster-name> [flags]
```

`<cluster-name>` : 操作対象のクラスター。

## オプション {#option}

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   デフォルト: false

## 出力 {#output}

-   通常は出力しません。
-   変更できないフィールドを誤って変更した場合、ファイルを保存するときにエラーが報告され、ファイルを再度編集するように通知されます。変更できないフィールドについては、 [トポロジーファイル](/tiup/tiup-dm-topology-reference.md)を参照してください。

[&lt;&lt; 前のページに戻る - TiUP DMコマンド一覧](/tiup/tiup-component-dm.md#command-list)
