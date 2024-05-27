---
title: TiDB Lightning Web Interface
summary: Web インターフェースを通じてTiDB Lightningを制御します。
---

# TiDB Lightning Web インターフェース {#tidb-lightning-web-interface}

TiDB Lightning は、インポートの進行状況を表示したり、簡単なタスク管理を実行したりするための Web ページを提供します。これは*サーバーモード*と呼ばれます。

サーバーモードを有効にするには、 `tidb-lightning` `--server-mode`フラグで開始するか

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

サーバーモードでは、 TiDB Lightning はすぐに実行を開始しません。代わりに、ユーザーは Web インターフェイスを介して (複数の)*タスク*を送信してデータをインポートします。

## 表紙 {#front-page}

![Front page of the web interface](/media/lightning-web-frontpage.png)

タイトル バーの機能 (左から右へ):

| アイコン             | 関数                                                                |
| :--------------- | :---------------------------------------------------------------- |
| 「TiDB Lightning」 | クリックするとトップページに戻ります                                                |
| ⚠                | *前の*タスクからのエラーメッセージを表示する                                           |
| ⓘ                | 現在のタスクとキューに入れられたタスクを一覧表示します。キューに入れられたタスクの数を示すバッジがここに表示されることがあります。 |
| <li></li>        | タスクを送信する                                                          |
| ⏸/▶              | 現在の実行を一時停止/再開する                                                   |
| ⟳                | ウェブページの自動更新を設定する                                                  |

タイトル バーの下の 3 つのパネルには、さまざまな状態のすべてのテーブルが表示されます。

-   アクティブ: これらのテーブルは現在インポート中です
-   完了: これらのテーブルは正常にインポートされたか、失敗しました
-   保留中: これらのテーブルはまだ処理されていません

各パネルには、テーブルの状態を説明するカードが含まれています。

## タスクを送信 {#submit-task}

タスクを送信するには、タイトル バーの**+**ボタンをクリックします。

![Submit task dialog](/media/lightning-web-submit.png)

タスクは[タスク構成](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)として記述される TOML ファイルです。UPLOAD**を**クリックしてローカルの TOML ファイルを開くこともできます。

タスクを実行するには、 **[送信]**をクリックします。タスクがすでに実行中の場合は、新しいタスクがキューに追加され、現在のタスクが成功した後に実行されます。

## テーブルの進捗状況 {#table-progress}

テーブルの詳細な進行状況を表示するには、フロント ページのテーブル カードの**[&gt;]**ボタンをクリックしてください。

![Table progress](/media/lightning-web-table.png)

このページには、テーブルに関連付けられているすべてのエンジンとデータ ファイルのインポートの進行状況が表示されます。

タイトル バーの**TiDB Lightning を**クリックすると、フロント ページに戻ります。

## タスク管理 {#task-management}

現在のタスクとキューに入れられたタスクを管理するには、タイトル バーの**ⓘ**ボタンをクリックします。

![Task management page](/media/lightning-web-queue.png)

各タスクには、送信された時間によってラベルが付けられます。タスクをクリックすると、JSON 形式の構成が表示されます。

タスクの横にある**⋮**ボタンをクリックしてタスクを管理します。タスクをすぐに停止したり、キューに入れられたタスクの順序を変更したりできます。
