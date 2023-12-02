---
title: tiup dm destroy
---

# ティアップDM破壊 {#tiup-dm-destroy}

アプリケーションがオフラインになった後、クラスターによって占有されていたマシンを他のアプリケーションで使用できるように解放したい場合は、クラスター上のデータとデプロイされたバイナリ ファイルをクリーンアップする必要があります。クラスターを破棄するには、 `tiup dm destroy`コマンドは次の操作を実行します。

-   クラスターを停止します。
-   サービスごとに、ログ ディレクトリ、デプロイメント ディレクトリ、およびデータ ディレクトリを削除します。
-   `tiup-dm`で各サービスのデータディレクトリやデプロイメントディレクトリの親ディレクトリを作成した場合は、親ディレクトリも削除します。

## 構文 {#syntax}

```shell
tiup dm destroy <cluster-name> [flags]
```

`<cluster-name>` : 破棄するクラスターの名前。

## オプション {#option}

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `Boolean`
-   デフォルト: false

## 出力 {#output}

tiup-dmの実行ログ。

[&lt;&lt; 前のページに戻る - TiUP DMコマンド一覧](/tiup/tiup-component-dm.md#command-list)
