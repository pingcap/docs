---
title: Connect to TiDB
summary: TiDBへの接続方法の概要。
aliases: ['/ja/tidb/stable/dev-guide-connect-to-tidb/','/ja/tidb/dev/dev-guide-connect-to-tidb/']
---

# TiDBに接続する {#connect-to-tidb}

TiDBはMySQLプロトコルとの互換性が非常に高いため、ほとんどのMySQLツール、ドライバ、およびORMを使用して接続できます。

-   SQLを手動で実行する（接続テスト、デバッグ、または簡単な検証のため）には、 [MySQL CLIツール](/develop/dev-guide-mysql-tools.md)から始めます。

-   視覚的なインターフェースを使用して接続するには、以下の一般的なGUIツールのドキュメントを参照してください。

    -   [JetBrains DataGrip](/develop/dev-guide-gui-datagrip.md)
    -   [DBeaver](/develop/dev-guide-gui-dbeaver.md)
    -   [VS Code](/develop/dev-guide-gui-vscode-sqltools.md)
    -   [MySQL Workchen](/develop/dev-guide-gui-mysql-workbench.md)
    -   [ナビキャット](/develop/dev-guide-gui-navicat.md)

-   TiDB 上でアプリケーションを構築するには、プログラミング言語とフレームワークに基づいて [ドライバーまたはORMを選択してください](/develop/dev-guide-choose-driver-or-orm.md)。

-   エッジ環境から HTTP 経由でTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスに接続するには、 [TiDB CloudサーバーレスDriver](/develop/serverless-driver.md)を使用します。サーバーレスドライバーはベータ版であり、 TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスにのみ適用可能であることに注意してください。

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)
