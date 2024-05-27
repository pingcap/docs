---
title: TiDB Binlog Troubleshooting
summary: TiDB Binlogのトラブルシューティング プロセスを学習します。
---

# TiDBBinlogシューティング {#tidb-binlog-troubleshooting}

このドキュメントでは、TiDB Binlog をトラブルシューティングして問題を見つける方法について説明します。

TiDB Binlog の実行中にエラーが発生した場合は、次の手順に従ってトラブルシューティングしてください。

1.  各監視メトリックが正常かどうかを確認します。詳細は[TiDBBinlog監視](/tidb-binlog/monitor-tidb-binlog-cluster.md)を参照してください。

2.  [binlogctl ツール](/tidb-binlog/binlog-control.md)使用して、各PumpまたはDrainerノードの状態が正常かどうかを確認します。

3.  PumpログまたはDrainerログに`ERROR`または`WARN`存在するかどうかを確認します。

上記の手順で問題を見つけたら、 [FAQ](/tidb-binlog/tidb-binlog-faq.md)と[TiDBBinlogエラー処理](/tidb-binlog/handle-tidb-binlog-errors.md)を参照して解決策を探してください。解決策が見つからない場合、または提供された解決策が役に立たない場合は、 [問題](https://github.com/pingcap/tidb-binlog/issues)を送信してヘルプを求めてください。
