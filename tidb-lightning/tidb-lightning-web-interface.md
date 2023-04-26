---
title: TiDB Lightning Web Interface
summary: Control TiDB Lightning through the web interface.
---

# TiDB LightningWeb インターフェイス {#tidb-lightning-web-interface}

TiDB Lightning は、インポートの進行状況を表示し、いくつかの簡単なタスク管理を実行するための Web ページを提供します。これを*サーバーモード*と呼びます。

サーバーモードを有効にするには、 `tidb-lightning` `--server-mode`フラグで開始します。

```sh
tiup tidb-lightning --server-mode --status-addr :8289
```

または、構成ファイルで`lightning.server-mode`設定を設定します。

```toml
[lightning]
server-mode = true
status-addr = ':8289'
```

TiDB Lightningが起動したら、 `http://127.0.0.1:8289`にアクセスしてプログラムを制御します (実際の URL は`status-addr`設定によって異なります)。

サーバーモードでは、 TiDB Lightning はすぐに実行を開始しません。むしろ、ユーザーは Web インターフェイスを介して (複数の)*タスク*を送信し、データをインポートします。

## 表紙 {#front-page}

![Front page of the web interface](/media/lightning-web-frontpage.png)

タイトルバーの機能、左から右へ:

| アイコン             | 関数                                                               |
| :--------------- | :--------------------------------------------------------------- |
| 「TiDB Lightning」 | クリックするとトップページに戻ります                                               |
| ⚠                | *前の*タスクのエラー メッセージを表示する                                           |
| ⓘ                | 現在のタスクとキューに入れられたタスクを一覧表示します。キューに入れられたタスクの数を示すバッジがここに表示される場合があります |
| <li></li>        | タスクを送信する                                                         |
| ⏸/▶              | 現在の実行を一時停止/再開                                                    |
| ⟳                | Web ページの自動更新を構成する                                                |

タイトル バーの下の 3 つのパネルには、すべてのテーブルがさまざまな状態で表示されます。

-   アクティブ: これらのテーブルは現在インポート中です
-   完了: これらのテーブルは正常にインポートされたか失敗しました
-   保留中: これらのテーブルはまだ処理されていません

各パネルには、テーブルのステータスを説明するカードが含まれています。

## タスクを送信 {#submit-task}

タイトル バーの**+**ボタンをクリックして、タスクを送信します。

![Submit task dialog](/media/lightning-web-submit.png)

タスクは[タスク構成](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)として記述された TOML ファイルです。 **UPLOAD**をクリックして、ローカルの TOML ファイルを開くこともできます。

**[SUBMIT]**をクリックしてタスクを実行します。タスクが既に実行されている場合、新しいタスクはキューに入れられ、現在のタスクが成功した後に実行されます。

## テーブルの進行状況 {#table-progress}

フロント ページのテーブル カードの**[&gt;]**ボタンをクリックして、テーブルの詳細な進行状況を表示します。

![Table progress](/media/lightning-web-table.png)

このページには、テーブルに関連付けられているすべてのエンジンとデータ ファイルのインポートの進行状況が表示されます。

タイトル バーの**TiDB Lightning を**クリックして、フロント ページに戻ります。

## タスク管理 {#task-management}

タイトル バーの**ⓘ**ボタンをクリックして、現在のタスクとキューに入れられたタスクを管理します。

![Task management page](/media/lightning-web-queue.png)

各タスクは、送信された時間によってラベル付けされます。タスクをクリックすると、JSON 形式の構成が表示されます。

タスクの横にある**⋮**ボタンをクリックして、タスクを管理します。タスクをすぐに停止したり、キューに入れられたタスクを並べ替えたりできます。
