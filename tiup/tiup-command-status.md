---
title: tiup status
---

# tiup status {#tiup-status}

`tiup status`コマンドは、 `tiup [flags] <component> [args...]`コマンドを使用してコンポーネントを実行した後に、コンポーネントの操作情報を表示するために使用されます。

> **ノート：**
>
> 次のコンポーネントの情報のみを確認できます。
>
> -   稼働中のコンポーネント
> -   `tiup -T/--tag`で指定されたタグを通過するコンポーネント

## 構文 {#syntax}

```shell
tiup status [flags]
```

## オプション {#option}

なし

## 出力 {#output}

次のフィールドで構成されるテーブル:

-   `Name` : `-T/--tag`で指定されたタグ名。指定しない場合は、ランダムな文字列です。
-   `Component` : 操作コンポーネント。
-   `PID` : 対応する運用コンポーネントのプロセス ID。
-   `Status` : 稼働中のコンポーネントのステータス。
-   `Created Time` : コンポーネントの開始時間。
-   `Directory` : コンポーネントのデータ ディレクトリ。
-   `Binary` : コンポーネントのバイナリ ファイル パス。
-   `Args` : 操作部品の開始引数。

[&lt;&lt; 前のページに戻る - TiUPリファレンス コマンド一覧](/tiup/tiup-reference.md#command-list)
