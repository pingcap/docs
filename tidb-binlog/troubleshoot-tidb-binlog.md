---
title: TiDB Binlog Troubleshooting
summary: Learn the troubleshooting process of TiDB Binlog.
---

# TiDBBinlogのトラブルシューティング {#tidb-binlog-troubleshooting}

このドキュメントでは、TiDB Binlog のトラブルシューティングを行って問題を見つける方法について説明します。

TiDB Binlogの実行中にエラーが発生した場合は、次の手順に従ってトラブルシューティングを行ってください。

1.  各監視指標が正常かどうかを確認してください。詳細は[<a href="/tidb-binlog/monitor-tidb-binlog-cluster.md">TiDBBinlogのモニタリング</a>](/tidb-binlog/monitor-tidb-binlog-cluster.md)を参照してください。

2.  [<a href="/tidb-binlog/binlog-control.md">binlogctl ツール</a>](/tidb-binlog/binlog-control.md)使用して、各PumpまたはDrainerノードの状態が正常かどうかを確認します。

3.  PumpログまたはDrainerに`ERROR`または`WARN`が存在するか確認してください。

上記の手順で問題が判明したら、 [<a href="/tidb-binlog/tidb-binlog-faq.md">FAQ</a>](/tidb-binlog/tidb-binlog-faq.md)と[<a href="/tidb-binlog/handle-tidb-binlog-errors.md">TiDBBinlogのエラー処理</a>](/tidb-binlog/handle-tidb-binlog-errors.md)を参照して解決してください。解決策が見つからない場合、または提供された解決策が役に立たない場合は、「 [<a href="https://github.com/pingcap/tidb-binlog/issues">問題</a>](https://github.com/pingcap/tidb-binlog/issues)を送信してサポートを求めてください。
