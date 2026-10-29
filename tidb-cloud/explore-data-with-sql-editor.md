---
title: SQL Editor（プレビュー）でデータを探索する
summary: TiDB Cloud コンソールで SQL Editor を使用して SQL クエリの作成と実行、SQL ファイルの管理、クエリ結果の表示を行う方法を学びます。
aliases: ['/ja/tidbcloud/explore-data-with-chat2query','/ja/tidbcloud/use-chat2query-api','/ja/tidbcloud/use-chat2query-knowledge','/ja/tidbcloud/use-chat2query-sessions']
---

# SQL Editor（プレビュー）でデータを探索する {#explore-your-data-with-sql-editor-preview}

[TiDB Cloudコンソール](https://tidbcloud.com/) に組み込まれている SQL Editor を使用して、データの価値を最大限に引き出すことができます。

SQL Editor では、ローカルの SQL クライアントがなくても、データベースに対して SQL クエリを作成して実行できます。クエリ結果をテーブルやチャートで直感的に確認でき、クエリログも簡単に確認できます。

## ユースケース {#use-cases}

SQL Editor の推奨ユースケースは次のとおりです。

- TiDB の MySQL 互換性をすばやくテストする。
- 自分のデータセットを使って、TiDB の SQL 機能を簡単に探索する。

## 制限事項 {#limitations}

- SQL Editor は、AWS でホストされる [{{{ .starter }}}](/tidb-cloud/select-cluster-tier.md#starter) インスタンス向けにパブリックプレビューとして提供されています。[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) クラスターで SQL Editor を使用するには、[TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。

## SQL Editor にアクセスする {#access-sql-editor}

1. [**My TiDB**](https://tidbcloud.com/tidbs) ページに移動します。

    > **Tip:**
    >
    > 複数の組織に所属している場合は、まず左上のコンボボックスを使用して対象の組織に切り替えてください。

2. {{{ .starter }}} インスタンスまたは TiDB Cloud Dedicated クラスターの名前をクリックし、左側のナビゲーションペインで **SQL Editor** をクリックします。

    > **Note:**
    >
    > 次の場合、**SQL Editor** エントリはグレー表示され、クリックできません。
    >
    > - TiDB Cloud Dedicated クラスターのバージョンが v6.5.0 より前である場合。SQL Editor を使用するには、[TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) に連絡してクラスターをアップグレードする必要があります。
    > - TiDB Cloud Dedicated クラスターを作成したばかりで、SQL Editor の実行環境がまだ準備中である場合。この場合は数分待つと、SQL Editor を利用できるようになります。
    > - TiDB Cloud Dedicated クラスターが[一時停止](/tidb-cloud/pause-or-resume-tidb-cluster.md)されている場合。

## SQL クエリを作成して実行する {#write-and-run-sql-queries}

SQL Editor では、自分のデータセットを使用して SQL クエリを作成し、実行できます。

1. SQL クエリを作成します。

2. SQL クエリを実行します。

    <SimpleTab>
    <div label="macOS">

    macOS の場合:

    - エディター内にクエリが 1 つだけある場合は、**⌘ + Enter** を押すか、<svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg>**Run** をクリックして実行します。

    - エディター内に複数のクエリがある場合は、対象のクエリの行をカーソルで選択し、**⌘ + Enter** を押すか **Run** をクリックすると、1 つまたは複数のクエリを順番に実行できます。

    - エディター内のすべてのクエリを順番に実行するには、**⇧ + ⌘ + Enter** を押すか、すべてのクエリの行をカーソルで選択して **Run** をクリックします。

    </div>

    <div label="Windows/Linux">

    Windows または Linux の場合:

    - エディター内にクエリが 1 つだけある場合は、**Ctrl + Enter** を押すか、<svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg>**Run** をクリックして実行します。

    - エディター内に複数のクエリがある場合は、対象のクエリの行をカーソルで選択し、**Ctrl + Enter** を押すか **Run** をクリックすると、1 つまたは複数のクエリを順番に実行できます。

    - エディター内のすべてのクエリを順番に実行するには、**Shift + Ctrl + Enter** を押すか、すべてのクエリの行をカーソルで選択して **Run** をクリックします。

    </div>
    </SimpleTab>

クエリを実行すると、ページ下部ですぐにクエリログと結果を確認できます。

> **Note:**
>
> 返される結果のサイズ上限は 8 MiB です。

## SQL ファイルを管理する {#manage-sql-files}

SQL Editor では、SQL クエリを異なる SQL ファイルに保存し、次のように SQL ファイルを管理できます。

- SQL ファイルを追加するには、**SQL Files** タブで **+** をクリックします。
- SQL ファイル名を変更するには、ファイル名にカーソルを合わせ、ファイル名の横にある **...** をクリックしてから **Rename** を選択します。
- SQL ファイルを削除するには、ファイル名にカーソルを合わせ、ファイル名の横にある **...** をクリックしてから **Delete** を選択します。**SQL Files** タブに SQL ファイルが 1 つしかない場合は削除できないことに注意してください。

## SQL Editor の設定を管理する {#manage-sql-editor-settings}

SQL Editor では、次の設定を変更できます。

- クエリ結果に表示する最大行数
- **Schemas** タブにシステムデータベーススキーマを表示するかどうか

設定を変更するには、次の手順を実行します。

1. **SQL Editor** の右上隅で **...** をクリックし、**Settings** を選択します。
2. 必要に応じて設定を変更します。
3. **Save** をクリックします。