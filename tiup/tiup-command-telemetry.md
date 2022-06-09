---
title: tiup telemetry
---

# tiup telemetry {#tiup-telemetry}

TiDB、TiUP、およびTiDBダッシュボードは、デフォルトで使用情報を収集し、その情報をPingCAPと共有して、製品を改善します。たとえば、この使用法情報を通じて、PingCAPは一般的なTiDBクラスタ操作について学習し、それによって新機能の優先順位を決定します。

TiUPテレメトリが有効になっている場合、TiUPコマンドが実行されると、使用情報がPingCAPと共有されます。

-   ランダムに生成されたテレメトリ識別子。
-   コマンドの実行が成功したかどうかやコマンドの実行時間など、TiUPコマンドの実行ステータス。
-   ターゲットマシンのハードウェア情報、コンポーネントのバージョン番号、変更された展開構成名など、展開にTiUPを使用している状況。

以下の情報は共有されていません。

-   クラスタの正確な名前
-   クラスタトポロジー
-   クラスタ構成ファイル

TiUPは、 `tiup telemetry`コマンドを使用してテレメトリを制御します。

> **ノート：**
>
> この機能はデフォルトで有効になっています。

## 構文 {#syntax}

```shell
tiup telemetry <command>
```

`<command>`はサブコマンドを表します。サポートされているサブコマンドのリストについては、以下のコマンドセクションを参照してください。

## コマンド {#commands}

### 状態 {#status}

`tiup telemetry status`コマンドは、現在のテレメトリ設定を表示し、次の情報を出力するために使用されます。

-   `status` ：テレメトリ`(enable|disable)`の有効化または無効化を指定します。
-   `uuid` ：ランダムに生成されたテレメトリ識別子を指定します。

### リセット {#reset}

`tiup telemetry reset`コマンドは、現在のテレメトリIDをリセットし、新しいランダムIDに置き換えるために使用されます。

### 有効 {#enable}

`tiup telemetry enable`コマンドは、テレメトリを有効にするために使用されます。

### 無効にする {#disable}

`tiup telemetry disable`コマンドは、テレメトリを無効にするために使用されます。

[&lt;&lt;前のページに戻る-TiUPリファレンスコマンドリスト](/tiup/tiup-reference.md#command-list)
