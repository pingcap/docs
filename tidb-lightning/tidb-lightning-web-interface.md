---
title: TiDB Lightning Web Interface
summary: TiDB LightningはWebインターフェースを通じて制御できます。
---

# TiDB Lightning Webインターフェース {#tidb-lightning-web-interface}

> **警告：**
>
> バージョン8.5.6以降、 TiDB Lightning Webインターフェースは非推奨となり、バージョン8.5.7で削除されます。Web UIビルドはバージョン8.4.0以降、不具合が発生しています。代わりに[`tidb-lightning` CLI](/tidb-lightning/tidb-lightning-overview.md)または[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)ステートメントを使用してください。この変更がワークフローに影響する場合は、 [#67697](https://github.com/pingcap/tidb/issues/67697)にコメントしてください。

TiDB Lightningは、インポートの進行状況を確認したり、簡単なタスク管理を実行したりするためのウェブページを提供します。これは*サーバーモード*と呼ばれます。

サーバーモードを有効にするには、 `tidb-lightning` `--server-mode`フラグ付きで起動します。

```sh
tiup tidb-lightning --server-mode --status-addr :8289
```

または、設定ファイルで`lightning.server-mode`を設定します。

```toml
[lightning]
server-mode = true
status-addr = ':8289'
```

TiDB Lightningを起動したら、 `http://127.0.0.1:8289`にアクセスしてプログラムを制御してください (実際の URL は`status-addr`の設定によって異なります)。

サーバーモードでは、 TiDB Lightningはすぐに起動しません。ユーザーはWebインターフェースを介して（複数の）*タスク*を送信し、データをインポートします。

## トップページ {#front-page}

![Front page of the web interface](/media/lightning-web-frontpage.png)

タイトルバーの機能（左から右へ）：

| アイコン           | 関数                                                                |
| :------------- | :---------------------------------------------------------------- |
| TiDB Lightning | クリックしてトップページに戻る                                                   |
| ⚠              | *前の*タスクからのエラーメッセージを表示する                                           |
| ⓘ              | 現在実行中のタスクとキューに入っているタスクを一覧表示します。キューに入っているタスクの数を示すバッジが表示される場合があります。 |
| +              | タスクを送信する                                                          |
| ⏸/▶            | 現在の実行を一時停止/再開する                                                   |
| ⟳              | ウェブページの自動更新を設定する                                                  |

タイトルバーの下にある3つのパネルには、すべてのテーブルが異なる状態に表示されます。

-   アクティブ: これらのテーブルは現在インポート中です
-   完了: これらのテーブルは正常にインポートされましたか、または失敗しました
-   保留中：これらのテーブルはまだ処理されていません

各パネルには、テーブルの状態を説明するカードが入っています。

## タスクを送信する {#submit-task}

タイトルバーの**「+」**ボタンをクリックしてタスクを送信してください。

![Submit task dialog](/media/lightning-web-submit.png)

タスクは[タスク構成](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)として記述される TOML ファイルです。 **[アップロード]**をクリックしてローカル TOML ファイルを開くこともできます。

タスクを実行するには、 **「送信」**をクリックしてください。既にタスクが実行中の場合は、新しいタスクはキューに追加され、現在のタスクが正常に完了した後に実行されます。

## テーブル進行状況 {#table-progress}

トップページのテーブルカードにある**「&gt;」**ボタンをクリックすると、テーブルの詳細な進捗状況が表示されます。

![Table progress](/media/lightning-web-table.png)

このページには、テーブルに関連付けられているすべてのエンジンファイルとデータファイルのインポート状況が表示されます。

トップページに戻るには、タイトルバーの**「TiDB Lightning」**をクリックしてください。

## タスク管理 {#task-management}

タイトルバーの**ⓘ**ボタンをクリックすると、現在実行中のタスクとキューに登録されているタスクを管理できます。

![Task management page](/media/lightning-web-queue.png)

各タスクには提出日時がラベル付けされています。タスクをクリックすると、JSON形式でフォーマットされた設定が表示されます。

タスクの横にある**⋮**ボタンをクリックして、タスクを管理してください。タスクをすぐに停止したり、キューに入っているタスクの順番を変更したりできます。
