---
title: tiup status
summary: tiup statusコマンドは、tiup [flags] <component> [args...]コマンドでコンポーネントを実行した後、コンポーネントの動作情報を表示します。コンポーネントの情報のみ確認できます。現在も稼働しているコンポーネントとtiup -T/--tagで指定されたタグを介して実行されるコンポーネント。構文はtiup status [flags]で、オプションはなし。出力はName、Component、PID、Status、Created Time、Directory、Binary、Argsのフィールドで構成されるテーブルです。コンポーネントのステータスはUp、ダウンまたは到達不能、廃棄、オフライン保留中、不明のいずれかです。TiUPのPending Offline、PD APIによって返されるOffline、およびTiDBダッシュボードのLeavingは同じステータスを示します。
---

# tiup status {#tiup-status}

`tiup status`コマンドは、 `tiup [flags] <component> [args...]`コマンドでコンポーネントを実行した後、コンポーネントの動作情報を表示するために使用します。

> **注記：**
>
> 以下のコンポーネントの情報のみ確認できます。
>
> -   現在も稼働しているコンポーネント
> -   `tiup -T/--tag`で指定されたタグを介して実行されるコンポーネント

## 構文 {#syntax}

```shell
tiup status [flags]
```

## オプション {#option}

なし

## 出力 {#output}

次のフィールドで構成されるテーブル:

-   `Name` ： `-T/--tag`で指定したタグ名。指定しない場合は、ランダムな文字列になります。
-   `Component` : 動作コンポーネント。
-   `PID` : 運用部品の対応するプロセスID。
-   `Status` : 動作部品の状態。
-   `Created Time` : コンポーネントの開始時刻。
-   `Directory` : コンポーネントのデータ ディレクトリ。
-   `Binary` : コンポーネントのバイナリ ファイル パス。
-   `Args` : 操作コンポーネントの開始引数。

### コンポーネントのステータス {#component-status}

コンポーネントは、次のいずれかのステータスで実行できます。

-   Up:コンポーネントは正常に実行されています。
-   ダウンまたは到達不能:コンポーネントが実行されていないか、対応するホストにネットワークの問題が存在します。
-   廃棄:コンポーネント上のデータは完全に移行され、スケールインは完了しました。このステータスは TiKV またはTiFlashにのみ存在します。
-   オフライン保留中:コンポーネント上のデータは移行中であり、スケールインが進行中です。このステータスは TiKV またはTiFlashにのみ存在します。
-   不明:コンポーネントの実行ステータスが不明です。

> **注記：**
>
> TiUPの`Pending Offline` 、PD API によって返される`Offline` 、および TiDB ダッシュボードの`Leaving`同じステータスを示します。

コンポーネントのステータスは、PD スケジュール情報から取得されます。詳細については、 [情報収集](/tidb-scheduling.md#information-collection)を参照してください。

[&lt;&lt; 前のページに戻る - TiUPリファレンスコマンドリスト](/tiup/tiup-reference.md#command-list)
