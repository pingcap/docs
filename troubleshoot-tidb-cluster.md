---
title: TiDB Cluster Troubleshooting Guide
summary: Learn how to diagnose and resolve issues when you use TiDB.
---

# TiDBクラスタートラブルシューティングガイド {#tidb-cluster-troubleshooting-guide}

このガイドを使用すると、TiDBの使用中に基本的な問題を診断して解決するのに役立ちます。問題が解決しない場合は、次の情報と[問題を作成する](https://github.com/pingcap/tidb/issues/new/choose)を収集してください。

-   正確なエラーメッセージとエラー発生時の操作
-   すべてのコンポーネントの状態
-   `fatal`を報告するコンポーネントのログ内の`error` `panic`
-   構成と展開のトポロジ
-   `dmesg`のTiDBコンポーネント関連の問題

その他の情報については、 [よくある質問（FAQ）](/faq/tidb-faq.md)を参照してください。

## データベースに接続できません {#cannot-connect-to-the-database}

1.  `tidb-server` 、および`pd-server`を含むすべてのサービスが開始されていることを確認し`tikv-server` 。

2.  `ps`コマンドを使用して、すべてのプロセスが実行されているかどうかを確認します。

    -   特定のプロセスが実行されていない場合は、次の対応するセクションを参照して、問題を診断および解決してください。

    <!---->

    -   すべてのプロセスが実行されている場合は、 `tidb-server`のログをチェックして、次のメッセージが表示されているかどうかを確認します。
        -   InformationSchemaが古くなっています：このメッセージは、 `tikv-server`が接続できない場合に表示されます。 `pd-server`と`tikv-server`の状態とログを確認してください。
        -   panic：このメッセージは、プログラムに問題がある場合に表示されます。詳細なpanicログと[問題を作成する](https://github.com/pingcap/tidb/issues/new/choose)を提供してください。

3.  データがクリアされ、サービスが再デプロイされた場合は、次のことを確認してください。

    -   `tikv-server`と`pd-server`のすべてのデータがクリアされます。特定のデータは`tikv-server`に格納され、メタデータは`pd-server`に格納されます。 2つのサーバーのうち1つだけがクリアされると、データに一貫性がなくなります。
    -   `pd-server`と`tikv-server`のデータがクリアされ、 `pd-server`と`tikv-server`が再起動された後、 `tidb-server`も再起動する必要があります。クラスタIDは、 `pd-server`が初期化されるときにランダムに割り当てられます。したがって、クラスタが再デプロイされると、クラスタIDが変更され、新しいクラスタIDを取得するために`tidb-server`を再起動する必要があります。

## <code>tidb-server</code>を起動できません {#cannot-start-code-tidb-server-code}

`tidb-server`を開始できない状況については、以下を参照してください。

-   起動パラメータにエラーがあります。

    [TiDBの構成とオプション](/command-line-flags-for-tidb-configuration.md)を参照してください。

-   ポートは占有されています。

    `lsof -i:port`コマンドを使用して、特定のポートに関連するすべてのネットワークを表示し、 `tidb-server`を開始するポートが占有されていないことを確認します。

<!---->

-   `pd-server`に接続できません。

    -   TiDBとPDの間のネットワークがスムーズに実行されているかどうかを確認します。これには、ネットワークにpingを実行できるかどうか、ファイアウォールの構成に問題があるかどうかなどが含まれます。
    -   ネットワークに問題がない場合は、 `pd-server`のプロセスの状態とログを確認してください。

## <code>tikv-server</code>を起動できません {#cannot-start-code-tikv-server-code}

`tikv-server`を開始できない状況については、以下を参照してください。

-   起動パラメータのエラー： [TiKVの構成とオプション](/command-line-flags-for-tikv-configuration.md)を参照してください。

-   ポートが占有されている： `lsof -i:port`コマンドを使用して、特定のポートに関連するすべてのネットワークを表示し、 `tikv-server`を開始するポートが占有されていないことを確認します。

<!---->

-   `pd-server`に接続できません。

    -   TiDBとPDの間のネットワークがスムーズに実行されているかどうかを確認します。これには、ネットワークにpingを実行できるかどうか、ファイアウォールの構成に問題があるかどうかなどが含まれます。

    -   ネットワークに問題がない場合は、 `pd-server`のプロセスの状態とログを確認してください。

<!---->

-   ファイルが占有されています。

    1つのデータベースファイルディレクトリで2つのTiKVファイルを開かないでください。

## <code>pd-server</code>を起動できません {#cannot-start-code-pd-server-code}

`pd-server`を開始できない状況については、以下を参照してください。

-   起動パラメータにエラーがあります。

    [PDの構成とオプション](/command-line-flags-for-pd-configuration.md)を参照してください。

-   ポートは占有されています。

    `lsof -i:port`コマンドを使用して、特定のポートに関連するすべてのネットワークを表示し、 `pd-server`を開始するポートが占有されていないことを確認します。

## TiDB / TiKV/PDプロセスが予期せず中止される {#the-tidb-tikv-pd-process-aborts-unexpectedly}

-   プロセスはフォアグラウンドで開始されていますか？クライアントが異常終了したため、プロセスが終了する場合があります。

-   コマンドラインで`nohup+&`実行されていますか？これにより、プロセスがhup信号を受信するため、プロセスが中止される可能性があります。スクリプトで起動コマンドを記述して実行することをお勧めします。

## TiDBpanic {#tidb-panic}

panicログと[問題を作成する](https://github.com/pingcap/tidb/issues/new/choose)を提供してください。

## 接続が拒否されました {#the-connection-is-rejected}

オペレーティングシステムのネットワークパラメータが正しいことを確認してください。これには次のものが含まれますが、これらに限定されません。

-   接続文字列のポートは、 `tidb-server`の開始ポートと一致しています。
-   ファイアウォールが正しく構成されている。

## 開くファイルが多すぎます {#open-too-many-files}

プロセスを開始する前に、 `ulimit -n`の結果が十分に大きいことを確認してください。値を`unlimited`または`1000000`より大きい値に設定することをお勧めします。

## データベースアクセスがタイムアウトし、システム負荷が高すぎる {#database-access-times-out-and-the-system-load-is-too-high}

まず、 [遅いクエリログ](/identify-slow-queries.md)をチェックして、不適切なSQLステートメントが原因であるかどうかを確認します。

問題の解決に失敗した場合は、次の情報を提供してください。

-   展開トポロジ

    -   `tidb-server`インスタンスはいくつデプロイされて`tikv-server` `pd-server`か？
    -   これらのインスタンスはマシンでどのように配布されますか？

-   これらのインスタンスがデプロイされているマシンのハードウェア構成：

    -   CPUコアの数
    -   メモリのサイズ
    -   ディスクの種類（SSDまたはハードディスク）
    -   それらは物理マシンですか、それとも仮想マシンですか？

<!---->

-   TiDBクラスタ以外に他のサービスはありますか？
-   `pd-server`と`tikv-server`は別々に展開されていますか？
-   現在の操作は何ですか？
-   `top -H`コマンドでCPUスレッド名を確認してください。
-   最近、ネットワークまたはIO監視データに例外はありますか？
