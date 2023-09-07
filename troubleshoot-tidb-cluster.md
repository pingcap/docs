---
title: TiDB Cluster Troubleshooting Guide
summary: Learn how to diagnose and resolve issues when you use TiDB.
---

# TiDBクラスタのトラブルシューティング ガイド {#tidb-cluster-troubleshooting-guide}

このガイドは、TiDB の使用中に発生する基本的な問題の診断と解決に役立ちます。問題が解決しない場合は、次の情報を収集してください[バグを報告](/support.md) :

-   正確なエラーメッセージとエラー発生時の操作
-   すべてのコンポーネントの状態
-   エラーを報告するコンポーネントのログ内の`error` / `fatal` / `panic`の情報
-   構成と展開トポロジ
-   `dmesg`の TiDBコンポーネント関連の問題

その他の情報については、 [よくある質問 (FAQ)](/faq/tidb-faq.md)を参照してください。

## データベースに接続できません {#cannot-connect-to-the-database}

1.  `tidb-server` 、 `pd-server` 、および`tikv-server`を含むすべてのサービスが開始されていることを確認します。

2.  `ps`コマンドを使用して、すべてのプロセスが実行されているかどうかを確認します。

    -   特定のプロセスが実行されていない場合は、次の対応するセクションを参照して問題を診断し、解決してください。

    <!---->

    -   すべてのプロセスが実行されている場合は、 `tidb-server`ログをチェックして、次のメッセージが表示されるかどうかを確認します。
        -   InformationSchema is out of date: このメッセージは、 `tikv-server`に接続できない場合に表示されます。 `pd-server`と`tikv-server`の状態とログを確認します。
        -   panic: このメッセージは、プログラムに問題がある場合に表示されます。詳細なpanicログを提供してください[バグを報告](/support.md) 。

3.  データがクリアされ、サービスが再デプロイされた場合は、次のことを確認してください。

    -   `tikv-server`と`pd-server`のデータは全てクリアされます。 `tikv-server`には特定データが、 `pd-server`にはメタデータが格納される。 2 つのサーバーのうち 1 つだけをクリアすると、データに不整合が生じます。
    -   `pd-server`と`tikv-server`のデータがクリアされ、 `pd-server`と`tikv-server`が再起動された後、 `tidb-server`も再起動する必要があります。クラスタ ID は、 `pd-server`の初期化時にランダムに割り当てられます。したがって、クラスターが再デプロイされるとクラスター ID が変更されるため、新しいクラスター ID を取得するには`tidb-server`を再起動する必要があります。

## <code>tidb-server</code>を起動できません {#cannot-start-code-tidb-server-code}

`tidb-server`起動できない場合は、以下を参照してください。

-   起動パラメータにエラーがあります。

    [TiDB の構成とオプション](/command-line-flags-for-tidb-configuration.md)を参照してください。

-   港が占領されています。

    `lsof -i:port`コマンドを使用して、特定のポートに関連するすべてのネットワークを表示し、 `tidb-server`開始するポートが占有されていないことを確認します。

<!---->

-   `pd-server`に接続できません。

    -   TiDB と PD の間のネットワークがスムーズに実行されているかどうか (ネットワークに ping が送信できるかどうか、ファイアウォール構成に問題があるかどうかなど) を確認します。
    -   ネットワークに問題がない場合は、 `pd-server`プロセスの状態とログを確認してください。

## <code>tikv-server</code>を起動できません {#cannot-start-code-tikv-server-code}

`tikv-server`起動できない場合は、以下を参照してください。

-   起動パラメータのエラー: [TiKV の構成とオプション](/command-line-flags-for-tikv-configuration.md)を参照してください。

-   ポートが占有されている: `lsof -i:port`コマンドを使用して、特定のポートに関連するすべてのネットワークを表示し、 `tikv-server`開始するポートが占有されていないことを確認します。

<!---->

-   `pd-server`に接続できません。

    -   TiDB と PD の間のネットワークがスムーズに実行されているかどうか (ネットワークに ping が送信できるかどうか、ファイアウォール構成に問題があるかどうかなど) を確認します。

    -   ネットワークに問題がない場合は、 `pd-server`プロセスの状態とログを確認してください。

<!---->

-   ファイルが占有されています。

    1 つのデータベース ファイル ディレクトリ上で 2 つの TiKV ファイルを開かないでください。

## <code>pd-server</code>起動できません {#cannot-start-code-pd-server-code}

`pd-server`起動できない場合は、以下を参照してください。

-   起動パラメータにエラーがあります。

    [PDの構成とオプション](/command-line-flags-for-pd-configuration.md)を参照してください。

-   港が占領されています。

    `lsof -i:port`コマンドを使用して、特定のポートに関連するすべてのネットワークを表示し、 `pd-server`開始するポートが占有されていないことを確認します。

## TiDB/TiKV/PD プロセスが予期せず中止される {#the-tidb-tikv-pd-process-aborts-unexpectedly}

-   プロセスはフォアグラウンドで開始されますか?クライアントが中止されるため、プロセスが終了する可能性があります。

-   `nohup+&`コマンドラインで実行されますか?これにより、プロセスが hup シグナルを受信するために中止される可能性があります。起動コマンドをスクリプトに記述して実行することをお勧めします。

## TiDBpanic {#tidb-panic}

panicログを提供してください[バグを報告](/support.md) 。

## 接続が拒否されました {#the-connection-is-rejected}

オペレーティング システムのネットワーク パラメータが正しいことを確認してください。次のものが含まれますが、これらに限定されません。

-   接続文字列内のポートは、開始ポート`tidb-server`と一致します。
-   ファイアウォールは正しく構成されています。

## 開いたファイルが多すぎます {#open-too-many-files}

プロセスを開始する前に、 `ulimit -n`の結果が十分に大きいことを確認してください。値を`unlimited`以上に設定することをお`1000000`します。

## データベースアクセスがタイムアウトし、システム負荷が高すぎる {#database-access-times-out-and-the-system-load-is-too-high}

まず、 [遅いクエリログ](/identify-slow-queries.md)チェックして、不適切な SQL ステートメントが原因であるかどうかを確認します。

問題を解決できなかった場合は、次の情報を提供してください。

-   導入トポロジ

    -   `tidb-server` / `pd-server` / `tikv-server`インスタンスはいくつデプロイされていますか?
    -   これらのインスタンスはマシン内にどのように分散されますか?

-   これらのインスタンスがデプロイされているマシンのハードウェア構成は次のとおりです。

    -   CPUコア数
    -   メモリのサイズ
    -   ディスクのタイプ (SSD またはハードドライブディスク)
    -   物理マシンですか、それとも仮想マシンですか?

<!---->

-   TiDB クラスター以外のサービスはありますか?
-   `pd-server`と`tikv-server`は別々に展開されますか?
-   現在の操作は何ですか?
-   `top -H`コマンドを使用してCPUスレッド名を確認します。
-   最近、ネットワークまたは IO 監視データに例外はありますか?
