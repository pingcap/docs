---
title: tiup status
---

# tiup status {#tiup-status}

`tiup status`コマンドは、 `tiup [flags] <component> [args...]`コマンドを使用してコンポーネントを実行した後、コンポーネントの動作情報を表示するために使用されます。

> **ノート：**
>
> 次のコンポーネントの情報のみを確認できます。
>
> -   まだ稼働中のコンポーネント
> -   `tiup -T/--tag`で指定されたタグを実行するコンポーネント

## 構文 {#syntax}

```shell
tiup status [flags]
```

## オプション {#option}

なし

## 出力 {#output}

次のフィールドで構成されるテーブル：

-   `Name` ： `-T/--tag`で指定されたタグ名。指定しない場合は、ランダムな文字列です。
-   `Component` ：操作コンポーネント。
-   `PID` ：オペレーティングコンポーネントの対応するプロセスID。
-   `Status` ：動作中のコンポーネントのステータス。
-   `Created Time` ：コンポーネントの開始時刻。
-   `Directory` ：コンポーネントのデータディレクトリ。
-   `Binary` ：コンポーネントのバイナリファイルパス。
-   `Args` ：オペレーティングコンポーネントの開始引数。

[&lt;&lt;前のページに戻る-TiUPリファレンスコマンドリスト](/tiup/tiup-reference.md#command-list)
