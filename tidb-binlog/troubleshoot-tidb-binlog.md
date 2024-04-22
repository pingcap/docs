---
title: TiDB Binlog Troubleshooting
summary: TiDB Binlogのトラブルシューティングについて説明します。エラーが発生した場合は、監視指標を確認し、binlogctlツールを使用してノードの状態を確認します。さらに、PumpログやDrainerのエラーを確認し、問題が判明したらFAQやエラー処理を参照して解決してください。解決策が見つからない場合は、問題を送信してサポートを求めてください。
---

# TiDBBinlogのトラブルシューティング {#tidb-binlog-troubleshooting}

このドキュメントでは、TiDB Binlog のトラブルシューティングを行って問題を見つける方法について説明します。

TiDB Binlogの実行中にエラーが発生した場合は、次の手順に従ってトラブルシューティングを行ってください。

1.  各監視指標が正常かどうかを確認してください。詳細は[TiDBBinlogのモニタリング](/tidb-binlog/monitor-tidb-binlog-cluster.md)を参照してください。

2.  [binlogctl ツール](/tidb-binlog/binlog-control.md)使用して、各PumpまたはDrainerノードの状態が正常かどうかを確認します。

3.  PumpログまたはDrainerに`ERROR`または`WARN`が存在するかどうかを確認します。

上記の手順で問題が判明したら、 [FAQ](/tidb-binlog/tidb-binlog-faq.md)と[TiDBBinlogのエラー処理](/tidb-binlog/handle-tidb-binlog-errors.md)を参照して解決してください。解決策が見つからない場合、または提供された解決策が役に立たない場合は、「 [問題](https://github.com/pingcap/tidb-binlog/issues)を送信してサポートを求めてください。
