---
title: Events
summary: Events ページを使用して TiDB Cloud リソースのイベントを表示する方法を学びます。
---

# Events

<CustomContent plan="starter,essential">

{{{ .starter }}} および Essential インスタンスでは、TiDB Cloud はインスタンスレベルで履歴イベントを記録します。*event* は、{{{ .starter }}} または Essential インスタンスに発生した変更を示します。記録されたイベントは **Events** ページで確認でき、イベントタイプ、ステータス、メッセージ、トリガー時刻、トリガーしたユーザーが表示されます。

</CustomContent>

<CustomContent plan="dedicated">

TiDB Cloud Dedicated クラスターでは、TiDB Cloud はクラスターレベルで履歴イベントを記録します。*event* は、TiDB Cloud Dedicated クラスターに発生した変更を示します。記録されたイベントは **Events** ページで確認でき、イベントタイプ、ステータス、メッセージ、トリガー時刻、トリガーしたユーザーが表示されます。

</CustomContent>

このドキュメントでは、**Events** ページを使用して履歴イベントを表示する方法を説明し、サポートされているイベントタイプを一覧で示します。

## Events ページを表示する {#view-the-events-page}

**Events** ページでイベントを表示するには、次の手順を実行します。

1. [**My TiDB**](https://tidbcloud.com/tidbs) ページで、対象の <CustomContent plan="starter,essential">{{{ .starter }}} または Essential インスタンス</CustomContent><CustomContent plan="dedicated">TiDB Cloud Dedicated クラスター</CustomContent> の名前をクリックして、その概要ページに移動します。

    > **Tip:**
    >
    > 複数の組織に所属している場合は、まず左上隅のコンボボックスを使用して対象の組織に切り替えてください。

2. 左側のナビゲーションペインで、**Monitoring** > **Events** をクリックします。

## 記録されるイベント {#logged-events}

TiDB Cloud は、次の種類のクラスターイベントを記録します。

| Event Type| Description |
|:--- |:--- |
| CreateCluster |  クラスターを作成する |  
| PauseCluster |   クラスターを一時停止する |  
| ResumeCluster |   クラスターを再開する | 
| ModifyClusterSize |   クラスターサイズを変更する | 
| BackupCluster |   クラスターをバックアップする |  
| ExportBackup |   バックアップをエクスポートする |
| RestoreFromCluster |   クラスターを復元する |  
| CreateChangefeed |   changefeed を作成する |  
| PauseChangefeed |   changefeed を一時停止する | 
| ResumeChangefeed |   changefeed を再開する | 
| DeleteChangefeed |   changefeed を削除する |  
| EditChangefeed |  changefeed を編集する |  
| ScaleChangefeed |   changefeed の仕様をスケールする |  
| FailedChangefeed |   changefeed の障害 |  
| ImportData |   クラスターにデータをインポートする |  
| UpdateSpendingLimit |   {{{ .starter }}} インスタンスの支出上限を更新する |  
| ResourceLimitation |   {{{ .starter }}} または {{{ .essential }}} インスタンスのリソース制限を更新する |  

各イベントについて、次の情報が記録されます。

- Event Type
- Status
- Message
- Time
- Triggered By

## イベント保持ポリシー {#event-retention-policy}

イベントデータは 7 日間保持されます。