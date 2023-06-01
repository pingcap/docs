---
title: Changefeed Overview
summary: Learn basic concepts, state definitions, and state transfer of changefeeds.
---

# チェンジフィードの概要 {#changefeed-overview}

チェンジフィードは TiCDC のレプリケーション タスクであり、TiDB クラスター内の指定されたテーブルのデータ変更ログを指定されたダウンストリームにレプリケートします。 TiCDC クラスターで複数の変更フィードを実行および管理できます。

## チェンジフィード状態転送 {#changefeed-state-transfer}

レプリケーション タスクの状態は、レプリケーション タスクの実行ステータスを表します。 TiCDC の実行中に、レプリケーション タスクがエラーで失敗したり、手動で一時停止または再開されたり、指定された`TargetTs`に達したりする可能性があります。これらの動作により、レプリケーション タスクの状態が変化する可能性があります。このセクションでは、TiCDC レプリケーション タスクの状態と状態間の転送関係について説明します。

![TiCDC state transfer](/media/ticdc/ticdc-state-transfer.png)

前述の状態遷移図の状態は次のように説明されています。

-   `Normal` : レプリケーション タスクは正常に実行され、チェックポイント ts も正常に進行します。
-   `Stopped` : ユーザーが変更フィードを手動で一時停止したため、レプリケーション タスクは停止します。この状態のチェンジフィードは GC 操作をブロックします。
-   `Error` : レプリケーション タスクはエラーを返します。回復可能なエラーがいくつかあるため、レプリケーションを続行できません。この状態のチェンジフィードは、状態が`Normal`に移行するまで再開を試み続けます。この状態のチェンジフィードは GC 操作をブロックします。
-   `Finished` : レプリケーションタスクが終了し、プリセット`TargetTs`に達しました。この状態の変更フィードは GC 操作をブロックしません。
-   `Failed` : レプリケーションタスクは失敗します。いくつかの回復不可能なエラーが原因で、レプリケーション タスクを再開できず、回復できません。この状態の変更フィードは GC 操作をブロックしません。

前述の状態遷移図の番号は次のように説明されます。

-   `changefeed pause`コマンドを実行します。
-   ② `changefeed resume`コマンドを実行してレプリケーションタスクを再開します。
-   ③ `changefeed`動作中に回復可能なエラーが発生し、自動的に動作を再開します。
-   ④ `changefeed resume`コマンドを実行してレプリケーションタスクを再開します。
-   ⑤ `changefeed`操作中に回復不能なエラーが発生します。
-   ⑥ `changefeed`プリセット`TargetTs`に達すると、レプリケーションは自動的に停止されます。
-   ⑦ `changefeed` `gc-ttl`で指定された期間を超えて中断され、再開できません。
-   ⑧ `changefeed`自動回復を実行しようとしたときに回復不能なエラーが発生しました。

## チェンジフィードの操作 {#operate-changefeeds}

コマンドライン ツール`cdc cli`を使用して、TiCDC クラスターとそのレプリケーション タスクを管理できます。詳細は[TiCDC 変更フィードを管理する](/ticdc/ticdc-manage-changefeed.md)を参照してください。

HTTP インターフェイス (TiCDC OpenAPI 機能) を使用して、TiCDC クラスターとそのレプリケーション タスクを管理することもできます。詳細は[TiCDC OpenAPI](/ticdc/ticdc-open-api.md)を参照してください。

TiCDC がTiUPを使用してデプロイされている場合は、 `tiup ctl:v<CLUSTER_VERSION> cdc`コマンドを実行して`cdc cli`を開始できます。 `v<CLUSTER_VERSION>` TiCDC クラスターのバージョン ( `v6.5.0`など) に置き換えます。 `cdc cli`直接実行することもできます。
