---
title: tiup dm destroy
summary: tiup dm destroy` コマンドは、クラスターを停止し、各サービスのログ、デプロイメント、およびデータ ディレクトリを削除し、`tiup-dm` によって作成された親ディレクトリも削除します。構文は `tiup dm destroy <cluster-name> [flags]` です。オプション `-h, --help` はヘルプ情報を出力。出力は tiup-dm の実行ログです。
---

# tiup dm 破壊する {#tiup-dm-destroy}

アプリケーションがオフラインになった後、クラスターが占有しているマシンを解放して他のアプリケーションで使用できるようにするには、クラスター上のデータとデプロイされたバイナリ ファイルをクリーンアップする必要があります。クラスターを破棄するには、 `tiup dm destroy`コマンドで次の操作を実行します。

-   クラスターを停止します。
-   各サービスについて、ログ ディレクトリ、デプロイメント ディレクトリ、およびデータ ディレクトリを削除します。
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

tiup-dm の実行ログ。

[&lt;&lt; 前のページに戻る - TiUP DMコマンドリスト](/tiup/tiup-component-dm.md#command-list)
