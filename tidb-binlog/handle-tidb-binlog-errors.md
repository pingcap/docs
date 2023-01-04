---
title: TiDB Binlog Error Handling
summary: Learn how to handle TiDB Binlog errors.
---

# TiDB Binlogエラー処理 {#tidb-binlog-error-handling}

このドキュメントでは、TiDB Binlogを使用する際に発生する可能性のある一般的なエラーと、これらのエラーの解決策を紹介します。

## <code>kafka server: Message was too large, server rejected it to avoid allocation error</code> Drainerがデータを Kafka にレプリケートするときに割り当てエラーが返されるのを避けるために、サーバーはそれを拒否しました {#code-kafka-server-message-was-too-large-server-rejected-it-to-avoid-allocation-error-code-is-returned-when-drainer-replicates-data-to-kafka}

原因: TiDB で大きなトランザクションを実行すると、大きなサイズの binlog データが生成され、メッセージ サイズに対する Kafka の制限を超える可能性があります。

解決策: 以下に示すように、Kafka の構成パラメーターを調整します。

{{< copyable "" >}}

```
message.max.bytes=1073741824
replica.fetch.max.bytes=1073741824
fetch.message.max.bytes=1073741824
```

## Pumpは<code>no space left on device</code>返します {#pump-returns-code-no-space-left-on-device-code-error}

原因:Pumpが binlog データを正常に書き込むには、ローカル ディスク領域が不十分です。

解決策: ディスク領域をクリーンアップしてから、 Pumpを再起動します。

## Pumpの起動時に<code>fail to notify all living drainer</code>た {#code-fail-to-notify-all-living-drainer-code-is-returned-when-pump-is-started}

原因: Pumpが開始されると、状態が`online`のすべてのDrainerノードに通知されます。 Drainerへの通知に失敗した場合、このエラー ログが出力されます。

解決策: [binlogctl ツール](/tidb-binlog/binlog-control.md)を使用して、各Drainerノードが正常かどうかを確認します。これは、 `online`状態にあるすべてのDrainerノードが正常に動作していることを確認するためです。 Drainerノードの状態が実際の動作状態と一致しない場合は、binlogctl ツールを使用して状態を変更し、 Pumpを再起動します。

## TiDB Binlogレプリケーション中にデータ損失が発生する {#data-loss-occurs-during-the-tidb-binlog-replication}

TiDB Binlogがすべての TiDB インスタンスで有効になっており、正常に動作していることを確認する必要があります。クラスターのバージョンが v3.0 以降の場合は、 `curl {TiDB_IP}:{STATUS_PORT}/info/all`コマンドを使用して、すべての TiDB インスタンスの TiDB Binlogステータスを確認します。

## アップストリーム トランザクションが大きい場合、 Pumpはエラー<code>rpc error: code = ResourceExhausted desc = trying to send message larger than max (2191430008 vs. 2147483647)</code>を報告します。 {#when-the-upstream-transaction-is-large-pump-reports-an-error-code-rpc-error-code-resourceexhausted-desc-trying-to-send-message-larger-than-max-2191430008-vs-2147483647-code}

このエラーは、TiDB からPumpに送信された gRPC メッセージがサイズ制限を超えているために発生します。 Pumpの起動時に`max-message-size`を指定することで、 Pumpが許可する gRPC メッセージの最大サイズを調整できます。

## Drainerによって出力されたファイル形式の増分データのクリーニング メカニズムはありますか?データは削除されますか？ {#is-there-any-cleaning-mechanism-for-the-incremental-data-of-the-file-format-output-by-drainer-will-the-data-be-deleted}

-   Drainer v3.0.x では、ファイル形式の増分データのクリーニング メカニズムはありません。
-   v4.0.x バージョンには、時間ベースのデータ クリーニング メカニズムがあります。詳細については、 [Drainer の`retention-time`設定項目](https://github.com/pingcap/tidb-binlog/blob/v4.0.9/cmd/drainer/drainer.toml#L153)を参照してください。
