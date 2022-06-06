---
title: TiDB Binlog Troubleshooting
summary: Learn the troubleshooting process of TiDB Binlog.
---

# TiDBBinlogのトラブルシューティング {#tidb-binlog-troubleshooting}

このドキュメントでは、問題を見つけるためにTiDBBinlogのトラブルシューティングを行う方法について説明します。

TiDB Binlogの実行中にエラーが発生した場合は、次の手順を実行してトラブルシューティングを行ってください。

1.  各監視メトリックが正常かどうかを確認します。詳細は[TiDBBinlogモニタリング](/tidb-binlog/monitor-tidb-binlog-cluster.md)を参照してください。

2.  [binlogctlツール](/tidb-binlog/binlog-control.md)を使用して、各ポンプまたはドレイナーノードの状態が正常であるかどうかを確認します。

3.  ポンプログまたはドレイナーログに`ERROR`または`WARN`が存在するかどうかを確認します。

上記の手順で問題を見つけたら、 [FAQ](/tidb-binlog/tidb-binlog-faq.md)と[TiDBBinlogエラー処理](/tidb-binlog/handle-tidb-binlog-errors.md)を参照して解決策を確認してください。解決策が見つからない場合、または提供されている解決策が役に立たない場合は、 [問題](https://github.com/pingcap/tidb-binlog/issues)を送信してください。
