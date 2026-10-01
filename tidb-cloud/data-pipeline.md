---
title: Data Pipeline
summary: TiDB Cloud から TiDB Cloud Lake に完全データと増分データをレプリケートするデータパイプラインの作成方法と管理方法を学びます。
---

# Data Pipeline

TiDB Cloud Data Pipeline は、サードパーティの ETL ツールを必要とせずに、TiDB Cloud インスタンスから TiDB Cloud Lake に完全データと増分変更をレプリケートします。継続的なレプリケーションでは、まず選択したソースデータの完全スナップショットをエクスポートし、その後、行の変更を継続的にレプリケートすることで、TiDB Cloud Lake 内のデータを最新の状態に保ちます。

Data Pipeline は、次のシナリオで使用できます。

- **一度限りのデータロード**: 初期データロードまたは移行のために、完全スナップショットを TiDB Cloud Lake にエクスポートします。
- **継続的なデータ同期**: 分析およびレポートのワークロード向けに、TiDB Cloud Lake を TiDB Cloud インスタンスと同期した状態に保ちます。

## 仕組み {#how-it-works}

継続的レプリケーションを伴うデータパイプラインは、2 つのフェーズで動作します。

1. **完全スナップショットのエクスポート**: 選択したソーステーブルを外部 stage に一度だけエクスポートし、そこから TiDB Cloud Lake がスナップショットをロードします。
2. **増分レプリケーション**: 行の変更（挿入、更新、削除）を継続的にキャプチャしてレプリケートし、TiDB Cloud Lake をソースの最新状態に保ちます。

継続的なレプリケーションを行わず、完全スナップショットのみをエクスポートするようにパイプラインを設定することもできます。

**外部 stage**（Amazon S3 または Alibaba Cloud OSS）は、TiDB Cloud インスタンスと TiDB Cloud Lake の間の中間ストレージとして使用されます。TiDB Cloud は、エクスポートしたスナップショットとキャプチャした行変更を stage に書き込み、TiDB Cloud Lake は stage からターゲット Warehouse にデータをロードします。これにより、書き込みレートと消費レートが分離され、信頼性が向上するとともに、コストとレイテンシーを制御できます。

詳細については、[Data Pipeline FAQ](/tidb-cloud/data-pipeline-lake-faq.md) を参照してください。

## 利用可能状況 {#availability}

<CustomContent plan="premium">

| プラン | ステータス |
| ---- | ------ |
| {{{ .premium }}} | Data Pipeline は [TiDB Cloud コンソール](https://tidbcloud.com) でプライベートプレビューとして提供されており、リクエストに応じて利用できます。 |
| {{{ .dedicated }}} | Data Pipeline はまだ TiDB Cloud コンソールでは利用できません。データパイプラインを使用するには、手動でセットアップする必要があります。 |
| {{{ .essential }}} | Data Pipeline はまだ TiDB Cloud コンソールでは利用できません。データパイプラインを使用するには、手動でセットアップする必要があります。 |
</CustomContent>

<CustomContent plan="byoc">

| プラン | ステータス |
| ---- | ------ |
| {{{ .premium }}} | Data Pipeline は [TiDB Cloud コンソール](https://tidbcloud.com) でプライベートプレビューとして提供されており、リクエストに応じて利用できます。 |
| {{{ .byoc }}} | Data Pipeline は [TiDB Cloud コンソール](https://tidbcloud.com) でプライベートプレビューとして提供されており、リクエストに応じて利用できます。 |
| {{{ .dedicated }}} | Data Pipeline はまだ TiDB Cloud コンソールでは利用できません。データパイプラインを使用するには、手動でセットアップする必要があります。 |
| {{{ .essential }}} | Data Pipeline はまだ TiDB Cloud コンソールでは利用できません。データパイプラインを使用するには、手動でセットアップする必要があります。 |
</CustomContent>

> **Note:**
>
> 現在、Data Pipeline は送信先として TiDB Cloud Lake をサポートしています。

## データパイプラインを作成する {#create-a-data-pipeline}

ご利用のプランに応じたガイドを参照してください。

- TiDB Cloud Premium<CustomContent plan="byoc"> および {{{ .byoc }}}</CustomContent>: [TiDB Cloud Lake への Data Pipeline をセットアップする](/tidb-cloud/data-pipeline-sink-to-lake.md)
- TiDB Cloud Dedicated: [TiDB Cloud Lake にデータをレプリケートするデータパイプラインを手動でセットアップする](/tidb-cloud/data-pipeline-dedicated-sink-to-lake.md)
- TiDB Cloud Essential: [TiDB Cloud Lake にデータをレプリケートするデータパイプラインを手動でセットアップする](/tidb-cloud/data-pipeline-essential-sink-to-lake.md)

## Data Pipeline ページを表示する {#view-the-data-pipeline-page}

> **Note:**
>
> **Data Pipeline** ページおよびこのセクションの管理操作は、{{{ .premium }}}<CustomContent plan="byoc"> および {{{ .byoc }}}</CustomContent> でのみ利用できます。{{{ .dedicated }}} と {{{ .essential }}} では、データパイプラインを手動で設定および管理します。

データパイプラインを表示および管理するには、次の手順を実行します。

1. [TiDB Cloud コンソール](https://tidbcloud.com) で、[**My TiDB**](https://tidbcloud.com/tidbs) ページに移動します。

    > **Tip:**
    >
    > 複数の組織に所属している場合は、まず左上のコンボボックスを使用して対象の組織に切り替えてください。

2. 対象の {{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンス名をクリックして概要ページに移動し、左側のナビゲーションペインで **Data** > **Data Pipeline** をクリックします。**Data Pipeline** ページが表示されます。

**Data Pipeline** ページでは、データパイプラインの作成、既存のデータパイプライン一覧の表示、および既存のデータパイプラインの管理（パイプラインの一時停止、再開、編集、削除など）ができます。

## データパイプラインを管理する {#manage-a-data-pipeline}

### データパイプラインを一時停止および再開する {#pause-and-resume-a-data-pipeline}

- **Pause**: データレプリケーションを停止し、パイプラインを `Paused` としてマークします。データが失われることはなく、レプリケーションの進行状況は保持されます。パイプラインの作成中、または完全スナップショットのエクスポート中は、一時停止できません。
- **Resume**: 一時停止した位置からレプリケーションを再開します。これには TiDB Cloud Lake への取り込みも含まれます。

データパイプラインを一時停止または再開するには、対象の {{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンスの **Data Pipeline** ページに移動し、パイプラインの行にある **...** をクリックしてから、**Pause** または **Resume** をクリックします。

### データパイプラインを編集する {#edit-a-data-pipeline}

データパイプラインを編集するには、対象の {{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンスの **Data Pipeline** ページに移動し、パイプラインの行にある **...** をクリックしてから、**Edit** をクリックします。

データパイプラインが `Running` の間は編集できません。まずパイプラインを一時停止し、その後編集して、変更を適用するために再開してください。

送信先タイプと同期モードは、パイプライン作成後に変更できません。

> **Note:**
>
> テーブルフィルタールールの変更は、以降の増分データにのみ影響します。
>
> - 新しいルールで除外されたテーブルには、以後増分データは取り込まれません。すでに書き込まれたデータは保持されます。
> - 新しいルールで追加されたテーブルには、増分データのみが取り込まれます。過去データのバックフィルは行われません。

### データパイプラインを削除する {#delete-a-data-pipeline}

データパイプラインを削除するには、次の手順を実行します。

1. 対象の {{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンスの **Data Pipeline** ページに移動し、パイプラインの行にある **...** をクリックしてから、**Delete** をクリックします。
2. 警告を確認し、操作を確定します。データパイプラインを削除すると、次のようになります。

    - すべてのデータレプリケーションが直ちに停止します。
    - パイプラインに関連付けられた TiDB Cloud Lake のデータソースと統合タスクの削除を試みます。削除に失敗した場合、これらのリソースが残り、手動でのクリーンアップが必要になることがあります。
    - TiDB Cloud Lake にすでに書き込まれたデータは**削除されません**。
    - Warehouse 内のターゲットデータベースまたはテーブルは**削除されません**。

この操作は元に戻せません。

## 関連情報 {#see-also}

- Data Pipeline に関するよくある質問については、[Data Pipeline FAQ](/tidb-cloud/data-pipeline-lake-faq.md) を参照してください。
- DDL、DML、およびカラム型のサポートの詳細については、[TiDB Cloud Lake 向け Data Pipeline SQL 互換性](/tidb-cloud/data-pipeline-lake-sql-compatibility.md) を参照してください。
