---
title: TiDB Lightning Web Interface
summary: Web インターフェースを通じてTiDB Lightning を制御します。
---

# TiDB Lightning Webインターフェース {#tidb-lightning-web-interface}

TiDB Lightningは、インポートの進行状況を確認したり、簡単なタスク管理を実行したりするためのウェブページを提供します。これは*サーバーモード*と呼ばれます。

サーバーモードを有効にするには、 `tidb-lightning` `--server-mode`フラグで開始するか、

```sh
tiup tidb-lightning --server-mode --status-addr :8289
```

または、構成ファイルで`lightning.server-mode`設定を設定します。

```toml
[lightning]
server-mode = true
status-addr = ':8289'
```

TiDB Lightningが起動したら、 `http://127.0.0.1:8289`アクセスしてプログラムを制御します (実際の URL は`status-addr`設定によって異なります)。

サーバーモードでは、 TiDB Lightning はすぐには実行されません。ユーザーはWebインターフェースを介して（複数の）*タスク*を送信し、データをインポートします。

## 表紙 {#front-page}

![Front page of the web interface](/media/lightning-web-frontpage.png)

タイトル バーの機能 (左から右へ):

| アイコン             | 関数                                                        |
| :--------------- | :-------------------------------------------------------- |
| 「TiDB Lightning」 | クリックするとトップページに戻ります                                        |
| ⚠                | *前の*タスクからのエラーメッセージを表示する                                   |
| ⓘ                | 現在のタスクとキュー内のタスクを一覧表示します。キュー内のタスクの数を示すバッジがここに表示される場合があります。 |
| <li></li>        | タスクを送信する                                                  |
| ⏸/▶              | 現在の実行を一時停止/再開する                                           |
| ⟳                | ウェブページの自動更新を設定する                                          |

タイトル バーの下の 3 つのパネルには、さまざまな状態にあるすべてのテーブルが表示されます。

-   アクティブ: これらのテーブルは現在インポート中です
-   完了: これらのテーブルは正常にインポートされたか、失敗しました
-   保留中: これらのテーブルはまだ処理されていません

各パネルには、テーブルの状態を説明するカードが含まれています。

## タスクを送信 {#submit-task}

タスクを送信するには、タイトルバーの**+**ボタンをクリックします。

![Submit task dialog](/media/lightning-web-submit.png)

タスクは[タスク構成](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)ように記述されたTOMLファイルです。UPLOAD**を**クリックしてローカルのTOMLファイルを開くこともできます。

タスクを実行するには、 **「送信」**をクリックします。すでにタスクが実行中の場合は、新しいタスクがキューに追加され、現在のタスクが成功した後に実行されます。

## 表の進捗状況 {#table-progress}

テーブルの詳細な進行状況を表示するには、フロントページのテーブル カードの**&gt;**ボタンをクリックしてください。

![Table progress](/media/lightning-web-table.png)

このページには、テーブルに関連付けられているすべてのエンジンとデータ ファイルのインポートの進行状況が表示されます。

タイトルバーの**TiDB Lightning**をクリックすると、フロント ページに戻ります。

## タスク管理 {#task-management}

現在のタスクとキューに入れられたタスクを管理するには、タイトル バーの**ⓘ**ボタンをクリックします。

![Task management page](/media/lightning-web-queue.png)

各タスクには送信時刻のラベルが付けられています。タスクをクリックすると、JSON形式で構成された設定が表示されます。

タスクの横にある**「⋮」**ボタンをクリックしてタスクを管理します。タスクをすぐに停止したり、キュー内のタスクの順序を変更したりできます。
