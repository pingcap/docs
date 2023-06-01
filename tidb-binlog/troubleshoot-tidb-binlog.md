---
title: TiDB Binlog Troubleshooting
summary: Learn the troubleshooting process of TiDB Binlog.
---

# TiDBBinlogのトラブルシューティング {#tidb-binlog-troubleshooting}

このドキュメントでは、TiDB Binlog のトラブルシューティングを行って問題を見つける方法について説明します。

TiDB Binlogの実行中にエラーが発生した場合は、次の手順に従ってトラブルシューティングを行ってください。

1.  各監視指標が正常かどうかを確認してください。詳細は[TiDBBinlogのモニタリング](/tidb-binlog/monitor-tidb-binlog-cluster.md)を参照してください。

2.  [binlogctl ツール](/tidb-binlog/binlog-control.md)使用して、各PumpまたはDrainerノードの状態が正常かどうかを確認します。

3.  PumpログまたはDrainerに`ERROR`または`WARN`が存在するか確認してください。

上記の手順で問題が判明したら、 [問題](https://github.com/pingcap/tidb-binlog/issues)を送信してサポートを求めてください。
