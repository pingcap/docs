---
title: TiDB Lightning Web Interface
summary: Control TiDB Lightning through the web interface.
---

# TiDB Lightningインターフェイス {#tidb-lightning-web-interface}

TiDB Lightningは、インポートの進行状況を表示し、いくつかの簡単なタスク管理を実行するためのWebページを提供します。これは*サーバーモード*と呼ばれます。

サーバーモードを有効にするには、 `--server-mode`フラグで`tidb-lightning`を開始します。

```sh
./tidb-lightning --server-mode --status-addr :8289
```

または、構成ファイルで`lightning.server-mode`の設定を設定します。

```toml
[lightning]
server-mode = true
status-addr = ':8289'
```

TiDB Lightningを起動したら、 `http://127.0.0.1:8289`にアクセスしてプログラムを制御します（実際のURLは`status-addr`の設定によって異なります）。

サーバーモードでは、 TiDB Lightningはすぐには実行を開始しません。むしろ、ユーザーはWebインターフェースを介して（複数の）*タスク*を送信してデータをインポートします。

## 表紙 {#front-page}

![Front page of the web interface](/media/lightning-web-frontpage.png)

左から右へのタイトルバーの機能：

| アイコン             | 関数                                                               |
| :--------------- | :--------------------------------------------------------------- |
| 「TiDB Lightning」 | クリックしてフロントページに戻ります                                               |
| ⚠                | *前の*タスクからのエラーメッセージを表示します                                         |
| ⓘ                | 現在のタスクとキューに入れられたタスクを一覧表示します。キューに入れられたタスクの数を示すバッジがここに表示される場合があります |
| <li></li>        | タスクを送信する                                                         |
| ⏸/▶              | 現在の実行を一時停止/再開します                                                 |
| ⟳                | Webページの自動更新を構成する                                                 |

タイトルバーの下の3つのパネルには、さまざまな状態のすべてのテーブルが表示されます。

-   アクティブ：これらのテーブルは現在インポートされています
-   完了：これらのテーブルは正常にインポートされたか、失敗しました
-   保留中：これらのテーブルはまだ処理されていません

各パネルには、テーブルのステータスを説明するカードが含まれています。

## タスクを送信する {#submit-task}

タスクを送信するには、タイトルバーの[ **+** ]ボタンをクリックします。

![Submit task dialog](/media/lightning-web-submit.png)

タスクは、 [タスク構成](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)として記述されたTOMLファイルです。 [アップロード]をクリックして、ローカルの**TOML**ファイルを開くこともできます。

[**送信]**をクリックしてタスクを実行します。タスクがすでに実行されている場合、現在のタスクが成功した後、新しいタスクがキューに入れられて実行されます。

## テーブルの進捗状況 {#table-progress}

表の詳細な進行状況を表示するには、フロントページのテーブルカードの**&gt;**ボタンをクリックします。

![Table progress](/media/lightning-web-table.png)

このページには、テーブルに関連付けられているすべてのエンジンとデータファイルのインポートの進行状況が表示されます。

タイトルバーの[ **TiDB Lightning]**をクリックして、フロントページに戻ります。

## タスク管理 {#task-management}

タイトルバーの**ⓘ**ボタンをクリックして、現在のタスクとキューに入れられているタスクを管理します。

![Task management page](/media/lightning-web-queue.png)

各タスクには、送信された時刻のラベルが付けられています。タスクをクリックすると、JSONとしてフォーマットされた構成が表示されます。

タスクの横にある**⋮**ボタンをクリックして、タスクを管理します。タスクをすぐに停止することも、キューに入れられたタスクを並べ替えることもできます。
