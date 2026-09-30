---
title: Data Pipeline FAQ
summary: 外部 stage、イベント駆動の取り込み、課金など、TiDB Cloud Data Pipeline から TiDB Cloud Lake への連携に関するよくある質問です。
---

# Data Pipeline FAQ

このドキュメントでは、TiDB Cloud Data Pipeline から TiDB Cloud Lake への連携に関する一般的な質問に回答します。

## データパイプラインで外部 stage が必要なのはなぜですか？ {#why-does-a-data-pipeline-require-an-external-stage}

信頼性を確保するために、外部 stage が必要です。データを直接転送するのではなく、両側が stage を介して動作することで、TiDB Cloud 側の書き込みレートは TiDB Cloud Lake の消費レートから切り離されます。

- 高い書き込みスループット時でも、変更データは stage に永続的に保存され、TiDB Cloud Lake へのロードが遅延または中断した場合でも、TiDB Cloud Lake がロードできる状態を維持します。
- stage は書き込み負荷をバッファリングし、データ生成レートと取り込みレートの一時的な差異が TiDB Cloud Lake の取り込みに直接影響するのを防ぎます。
- TiDB Cloud Lake 側の取り込み頻度は書き込みレートから切り離されるため、TiDB Cloud Lake 側のコストを制御する手段が得られます。

## SQS キューを使用したイベント駆動の取り込みを有効にする必要がありますか？ {#do-i-need-to-enable-event-driven-ingestion-with-an-sqs-queue}

デフォルトのポーリングモードよりも**低いデータレイテンシー**が必要な場合は、イベント駆動の取り込みを有効にしてください。

デフォルトモードでは、Data Pipeline は、changefeed が増分データを外部 stage にフラッシュする間隔と、TiDB Cloud Lake が新しいデータを検出するために stage をスキャンする間隔に依存します。{{{ .premium }}}<CustomContent plan="byoc"> および {{{ .byoc }}}</CustomContent> では、設定された **Sync Interval** が、これらの段階全体におけるエンドツーエンドのレイテンシー目標になります。

イベント駆動モードでは、changefeed は設定された間隔で引き続きデータを外部 stage にフラッシュしますが、各フラッシュは同時に SQS キューへの **S3 event notification** もトリガーします。SQS 通知により、TiDB Cloud Lake は次回の定期スキャンを待つことなく、新しいデータをより早く検出できます。

**トレードオフ:** イベント駆動モードでは、TiDB Cloud Lake は新しいデータをより高頻度で取り込めるため、warehouse が **active** 状態のままより長く維持される可能性があります。これにより、warehouse のホスティングコストが増加します。

## データパイプラインでは TiDB Cloud Lake に追加料金が発生しますか？ {#does-a-data-pipeline-incur-additional-tidb-cloud-lake-charges}

データパイプラインによって、別個の課金カテゴリが追加されることはありません。コストは、パイプラインに関与する既存のコンポーネントから発生します。

- **Export**（1 回限り）: 完全なスナップショットのエクスポートに対して課金されます。
- **Changefeed**（継続）: 増分レプリケーションが有効な場合、継続的なレプリケーションに使用される changefeed リソースに対して課金されます。
- **TiDB Cloud Lake**（継続）: データストレージと Warehouse コンピュートに対して課金されます。詳細は、[TiDB Cloud Lake Pricing & Billing](https://docs.pingcap.com/tidbcloudlake/pricing-billing/) を参照してください。