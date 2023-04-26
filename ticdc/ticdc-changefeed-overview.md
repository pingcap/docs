---
title: Changefeed Overview
summary: Learn basic concepts, state definitions, and state transfer of changefeeds.
---

# チェンジフィードの概要 {#changefeed-overview}

変更フィードは、TiCDC のレプリケーション タスクであり、TiDB クラスター内の指定されたテーブルのデータ変更ログを指定されたダウンストリームにレプリケートします。 TiCDC クラスターで複数の変更フィードを実行および管理できます。

## Changefeed 状態転送 {#changefeed-state-transfer}

レプリケーション タスクの状態は、レプリケーション タスクの実行ステータスを表します。 TiCDC の実行中に、レプリケーション タスクがエラーで失敗したり、手動で一時停止、再開したり、指定された`TargetTs`に達したりする場合があります。これらの動作により、レプリケーション タスクの状態が変化する可能性があります。このセクションでは、TiCDC レプリケーション タスクの状態と、状態間の転送関係について説明します。

![TiCDC state transfer](/media/ticdc/ticdc-state-transfer.png)

前の状態遷移図の状態は、次のように説明されています。

-   `Normal` : レプリケーション タスクは正常に実行され、checkpoint-ts は正常に進行します。
-   `Stopped` : ユーザーが変更フィードを手動で一時停止したため、レプリケーション タスクは停止されています。この状態の変更フィードは、GC 操作をブロックします。
-   `Error` : レプリケーション タスクはエラーを返します。いくつかの回復可能なエラーが原因で、レプリケーションを続行できません。この状態の changefeed は、状態が`Normal`に移行するまで再開を試み続けます。この状態の変更フィードは、GC 操作をブロックします。
-   `Finished` : レプリケーション タスクが完了し、プリセット`TargetTs`に達しました。この状態の変更フィードは、GC 操作をブロックしません。
-   `Failed` : レプリケーション タスクは失敗します。一部の回復不能なエラーが原因で、レプリケーション タスクを再開できず、回復できません。この状態の変更フィードは、GC 操作をブロックしません。

前の状態遷移図の番号は、次のように記述されます。

-   ① `changefeed pause`コマンドを実行します。
-   ② `changefeed resume`コマンドを実行してレプリケーションタスクを再開します。
-   ③ `changefeed`動作中に回復可能なエラーが発生し、自動的に動作が再開されます。
-   ④ `changefeed resume`コマンドを実行してレプリケーションタスクを再開します。
-   ⑤ `changefeed`回目の操作で回復不可能なエラーが発生した。
-   ⑥ `changefeed`プリセット`TargetTs`に到達し、レプリケーションが自動的に停止されます。
-   ⑦ `changefeed` `gc-ttl`で指定された期間を超えて停止し、再開することはできません。
-   ⑧ `changefeed`自動回復を実行しようとしたときに、回復不能なエラーが発生しました。

## チェンジフィードを操作する {#operate-changefeeds}

コマンドライン ツール`cdc cli`を使用して、TiCDC クラスターとそのレプリケーション タスクを管理できます。詳細については、 [TiCDC チェンジフィードの管理](/ticdc/ticdc-manage-changefeed.md)を参照してください。

HTTP インターフェイス (TiCDC OpenAPI 機能) を使用して、TiCDC クラスターとそのレプリケーション タスクを管理することもできます。詳細については、 [TiCDC OpenAPI](/ticdc/ticdc-open-api.md)を参照してください。

TiCDC がTiUPを使用してデプロイされている場合は、 `tiup ctl:v<CLUSTER_VERSION> cdc`コマンドを実行して`cdc cli`を開始できます。 `v<CLUSTER_VERSION>` TiCDC クラスターのバージョン ( `v6.5.2`など) に置き換えます。 `cdc cli`直接実行することもできます。
