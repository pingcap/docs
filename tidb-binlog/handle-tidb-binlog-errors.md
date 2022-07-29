---
title: TiDB Binlog Error Handling
summary: Learn how to handle TiDB Binlog errors.
---

# Binlogエラー処理 {#tidb-binlog-error-handling}

このドキュメントでは、TiDB Binlogを使用するときに発生する可能性のある一般的なエラーと、これらのエラーの解決策を紹介します。

## <code>kafka server: Message was too large, server rejected it to avoid allocation error</code>たDrainerがKafkaにデータを複製するときに割り当てエラーが返されるのを避けるために、サーバーはメッセージを拒否しました。 {#code-kafka-server-message-was-too-large-server-rejected-it-to-avoid-allocation-error-code-is-returned-when-drainer-replicates-data-to-kafka}

原因：TiDBで大規模なトランザクションを実行すると、大規模なbinlogデータが生成されます。これは、Kafkaのメッセージサイズの制限を超える可能性があります。

解決策：以下に示すように、Kafkaの構成パラメーターを調整します。

{{< copyable "" >}}

```
message.max.bytes=1073741824
replica.fetch.max.bytes=1073741824
fetch.message.max.bytes=1073741824
```

## Pumpは<code>no space left on device</code> {#pump-returns-code-no-space-left-on-device-code-error}

原因： Pumpがbinlogデータを正常に書き込むには、ローカルディスク領域が不十分です。

解決策：ディスク領域をクリーンアップしてから、 Pumpを再起動します。

## Pumpの始動時に、 <code>fail to notify all living drainer</code> {#code-fail-to-notify-all-living-drainer-code-is-returned-when-pump-is-started}

原因： Pumpが起動すると、 `online`状態にあるすべてのDrainerノードに通知します。 Drainerへの通知に失敗した場合、このエラーログが出力されます。

解決策： [binlogctlツール](/tidb-binlog/binlog-control.md)を使用して、各Drainerノードが正常かどうかを確認します。これは、 `online`の状態にあるすべてのDrainerノードが正常に機能していることを確認するためです。 Drainerノードの状態が実際の動作ステータスと一致しない場合は、binlogctlツールを使用してその状態を変更してから、 Pumpを再起動します。

## Binlogレプリケーション中にデータ損失が発生する {#data-loss-occurs-during-the-tidb-binlog-replication}

TiDB BinlogがすべてのTiDBインスタンスで有効になっていて、正常に実行されていることを確認する必要があります。クラスタのバージョンがv3.0より後の場合は、 `curl {TiDB_IP}:{STATUS_PORT}/info/all`コマンドを使用して、すべてのTiDBインスタンスのBinlogステータスを確認します。

## アップストリームトランザクションが大きい場合、 Pumpはエラー<code>rpc error: code = ResourceExhausted desc = trying to send message larger than max (2191430008 vs. 2147483647)</code> {#when-the-upstream-transaction-is-large-pump-reports-an-error-code-rpc-error-code-resourceexhausted-desc-trying-to-send-message-larger-than-max-2191430008-vs-2147483647-code}

このエラーは、TiDBからPumpに送信されるgRPCメッセージがサイズ制限を超えているために発生します。 Pumpの起動時に`max-message-size`を指定することで、 Pumpが許可するgRPCメッセージの最大サイズを調整できます。

## Drainerによって出力されたファイル形式のインクリメンタルデータのクリーニングメカニズムはありますか？データは削除されますか？ {#is-there-any-cleaning-mechanism-for-the-incremental-data-of-the-file-format-output-by-drainer-will-the-data-be-deleted}

-   Drainer v3.0.xには、ファイル形式の増分データのクリーニングメカニズムはありません。
-   v4.0.xバージョンには、時間ベースのデータクリーニングメカニズムがあります。詳しくは[ドレイナーの`retention-time`構成項目](https://github.com/pingcap/tidb-binlog/blob/v4.0.9/cmd/drainer/drainer.toml#L153)をご覧ください。
