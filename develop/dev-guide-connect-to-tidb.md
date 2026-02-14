---
title: Connect to TiDB
summary: TiDB に接続する方法の概要。
aliases: ['/ja/tidb/stable/dev-guide-connect-to-tidb/']
---

# TiDBに接続する {#connect-to-tidb}

TiDB は MySQL プロトコルとの互換性が高いため、ほとんどの MySQL ツール、ドライバー、ORM を使用して接続できます。

-   SQL を手動で実行するには (接続テスト、デバッグ、またはクイック検証のため)、 [MySQL CLIツール](/develop/dev-guide-mysql-tools.md)から開始します。

-   ビジュアル インターフェイスを使用して接続するには、次の一般的な GUI ツールのドキュメントを参照してください。

    -   [ジェットブレインズ データグリップ](/develop/dev-guide-gui-datagrip.md)
    -   [DBeaver](/develop/dev-guide-gui-dbeaver.md)
    -   [VSコード](/develop/dev-guide-gui-vscode-sqltools.md)
    -   [MySQLワークベンチ](/develop/dev-guide-gui-mysql-workbench.md)
    -   [ナビキャット](/develop/dev-guide-gui-navicat.md)

-   TiDB 上にアプリケーションを構築するには、プログラミング言語とフレームワークに基づいて[ドライバーまたはORMを選択する](/develop/dev-guide-choose-driver-or-orm.md)選択します。

-   エッジ環境から HTTP 経由でTiDB Cloud Starter またはTiDB Cloud Essential クラスターに接続するには、 [TiDB CloudサーバーレスDriver](/develop/serverless-driver.md)を使用します。サーバーレス ドライバーはベータ版であり、 TiDB Cloud Starter またはTiDB Cloud Essential クラスターにのみ適用されることに注意してください。

## ヘルプが必要ですか? {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに問い合わせてください。
-   [TiDB Cloudのサポートチケットを送信する](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDBセルフマネージドのサポートチケットを送信する](/support.md)
