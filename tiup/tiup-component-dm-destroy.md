---
title: tiup dm destroy
---

# tiup dm destroy {#tiup-dm-destroy}

アプリケーションがオフラインになった後、他のアプリケーションで使用するためにクラスタによって占有されているマシンを解放する場合は、クラスタ上のデータとデプロイされたバイナリファイルをクリーンアップする必要があります。クラスタを破棄するために、 `tiup dm destroy`コマンドは次の操作を実行します。

-   クラスタを停止します。
-   サービスごとに、ログディレクトリ、デプロイメントディレクトリ、およびデータディレクトリを削除します。
-   各サービスのデータディレクトリまたはデプロイメントディレクトリの親ディレクトリが`tiup-dm`で作成されている場合は、親ディレクトリも削除します。

## 構文 {#syntax}

```shell
tiup dm destroy <cluster-name> [flags]
```

`<cluster-name>` ：クラスタの名前。

## オプション {#option}

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型： `Boolean`
-   デフォルト：false

## 出力 {#output}

tiup-dmの実行ログ。

[&lt;&lt;前のページに戻るTiUP DMコマンドリスト](/tiup/tiup-component-dm.md#command-list)
