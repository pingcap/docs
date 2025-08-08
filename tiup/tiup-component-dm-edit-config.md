---
title: tiup dm edit-config
summary: tiup dm edit-config`コマンドを使用すると、デプロイメント後にクラスタサービスの設定を変更できます。エディタを使用して、指定したクラスタのトポロジファイルを変更できます。設定変更時にマシンの追加や削除はできないことに注意してください。コマンド実行後、設定はコントロールマシン上でのみ変更されるため、`tiup dm reloadコマンドを実行して設定を再読み込みする必要があります。
---

# tiup dm 編集設定 {#tiup-dm-edit-config}

クラスターのデプロイ後にクラスターサービス設定を変更する必要がある場合は、 `tiup dm edit-config`コマンドを使用してエディターを起動し、指定したクラスターの[トポロジファイル](/tiup/tiup-dm-topology-reference.md) . を変更できます。このエディターは、デフォルトで`$EDITOR`環境変数に指定されています。7 環境変数が存在しない場合は、 `$EDITOR`エディター`vi`使用されます。

> **注記：**
>
> -   設定を変更すると、マシンの追加や削除はできなくなります。マシンの追加方法については[クラスターをスケールアウトする](/tiup/tiup-component-dm-scale-out.md)参照してください。マシンの削除方法については[クラスターのスケールイン](/tiup/tiup-component-dm-scale-in.md)参照してください。
> -   `tiup dm edit-config`コマンドを実行すると、コントロールマシン上でのみ設定が変更されます。その後、 `tiup dm reload`コマンドを実行して設定を再読み込みする必要があります。

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

-   通常は出力されません。
-   変更できないフィールドを誤って変更した場合、ファイルを保存するとエラーが表示され、ファイルを再度編集するように促されます。変更できないフィールドについては、 [トポロジファイル](/tiup/tiup-dm-topology-reference.md)参照してください。

[&lt;&lt; 前のページに戻る - TiUP DMコマンドリスト](/tiup/tiup-component-dm.md#command-list)
