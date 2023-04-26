---
title: TiDB Cluster Troubleshooting Guide
summary: Learn how to diagnose and resolve issues when you use TiDB.
---

# TiDBクラスタトラブルシューティング ガイド {#tidb-cluster-troubleshooting-guide}

このガイドを使用して、TiDB を使用する際の基本的な問題を診断して解決することができます。問題が解決しない場合は、次の情報と[問題を作成する](https://github.com/pingcap/tidb/issues/new/choose)を収集してください。

-   正確なエラー メッセージとエラーが発生したときの操作
-   すべてのコンポーネントの状態
-   エラーを報告するコンポーネントのログ内の`error` / `fatal` / `panic`情報
-   構成と展開のトポロジ
-   `dmesg`のTiDBコンポーネント関連の問題

その他の情報については、 [よくある質問 (FAQ)](/faq/tidb-faq.md)を参照してください。

## データベースに接続できません {#cannot-connect-to-the-database}

1.  `tidb-server` 、 `pd-server` 、および`tikv-server`を含むすべてのサービスが開始されていることを確認します。

2.  `ps`コマンドを使用して、すべてのプロセスが実行されているかどうかを確認します。

    -   特定のプロセスが実行されていない場合は、次の対応するセクションを参照して、問題を診断して解決してください。

    <!---->

    -   すべてのプロセスが実行されている場合は、 `tidb-server`ログをチェックして、次のメッセージが表示されているかどうかを確認します。
        -   InformationSchema が古くなっています: このメッセージは、 `tikv-server`に接続できない場合に表示されます。 `pd-server`と`tikv-server`の状態とログを確認します。
        -   panic: このメッセージは、プログラムに問題がある場合に表示されます。詳細なpanicログと[問題を作成する](https://github.com/pingcap/tidb/issues/new/choose)を提供してください。

3.  データが消去され、サービスが再デプロイされた場合は、次のことを確認してください。

    -   `tikv-server`と`pd-server`のすべてのデータがクリアされます。特定のデータは`tikv-server`に格納され、メタデータは`pd-server`に格納されます。 2 つのサーバーのうち 1 つだけが消去されると、データの一貫性が失われます。
    -   `pd-server`と`tikv-server`のデータがクリアされ、 `pd-server`と`tikv-server`が再起動された後、 `tidb-server`も再起動する必要があります。クラスター ID は、 `pd-server`の初期化時にランダムに割り当てられます。そのため、クラスターが再デプロイされると、クラスター ID が変更され、新しいクラスター ID を取得するには`tidb-server`を再起動する必要があります。

## <code>tidb-server</code>を起動できません {#cannot-start-code-tidb-server-code}

`tidb-server`を起動できない状況については、以下を参照してください。

-   起動パラメータにエラーがあります。

    [TiDB の構成とオプション](/command-line-flags-for-tidb-configuration.md)を参照してください。

-   ポートが占有されています。

    `lsof -i:port`コマンドを使用して、特定のポートに関連するすべてのネットワークを表示し、 `tidb-server`開始するポートが占有されていないことを確認します。

<!---->

-   `pd-server`に接続できません。

    -   TiDB と PD の間のネットワークがスムーズに動作しているかどうかを確認します。これには、ネットワークに ping を実行できるかどうか、またはファイアウォールの構成に問題があるかどうかが含まれます。
    -   ネットワークに問題がない場合は、 `pd-server`プロセスの状態とログを確認します。

## <code>tikv-server</code>を起動できません {#cannot-start-code-tikv-server-code}

`tikv-server`を起動できない状況については、以下を参照してください。

-   起動パラメータのエラー: [TiKV の構成とオプション](/command-line-flags-for-tikv-configuration.md)を参照してください。

-   ポートが占有されている: `lsof -i:port`コマンドを使用して、特定のポートに関連するすべてのネットワークを表示し、 `tikv-server`開始するポートが占有されていないことを確認します。

<!---->

-   `pd-server`に接続できません。

    -   TiDB と PD の間のネットワークがスムーズに動作しているかどうかを確認します。これには、ネットワークに ping を実行できるかどうか、またはファイアウォールの構成に問題があるかどうかが含まれます。

    -   ネットワークに問題がない場合は、 `pd-server`プロセスの状態とログを確認します。

<!---->

-   ファイルが占有されています。

    1 つのデータベース ファイル ディレクトリで 2 つの TiKV ファイルを開かないでください。

## <code>pd-server</code>を起動できません {#cannot-start-code-pd-server-code}

`pd-server`を起動できない状況については、以下を参照してください。

-   起動パラメータにエラーがあります。

    [PD の構成とオプション](/command-line-flags-for-pd-configuration.md)を参照してください。

-   ポートが占有されています。

    `lsof -i:port`コマンドを使用して、特定のポートに関連するすべてのネットワークを表示し、 `pd-server`開始するポートが占有されていないことを確認します。

## TiDB/TiKV/PD プロセスが予期せず中断する {#the-tidb-tikv-pd-process-aborts-unexpectedly}

-   プロセスはフォアグラウンドで開始されていますか?クライアントが異常終了するため、プロセスが終了する可能性があります。

-   `nohup+&`コマンド ラインで実行されますか?これにより、hup シグナルを受信するため、プロセスが異常終了する可能性があります。スクリプトに起動コマンドを記述して実行することをお勧めします。

## TiDBpanic {#tidb-panic}

panicログと[問題を作成する](https://github.com/pingcap/tidb/issues/new/choose)を提供してください。

## 接続が拒否されました {#the-connection-is-rejected}

オペレーティング システムのネットワーク パラメータが正しいことを確認してください。

-   接続文字列のポートは、 `tidb-server`の開始ポートと一致しています。
-   ファイアウォールが正しく構成されている。

## 開いているファイルが多すぎる {#open-too-many-files}

プロセスを開始する前に、 `ulimit -n`の結果が十分に大きいことを確認してください。値を`unlimited`以上に設定することをお`1000000`します。

## データベース アクセスがタイムアウトし、システム負荷が高すぎる {#database-access-times-out-and-the-system-load-is-too-high}

まず、 [遅いクエリ ログ](/identify-slow-queries.md)確認して、不適切な SQL ステートメントによるものかどうかを確認します。

問題を解決できなかった場合は、次の情報を提供してください。

-   展開トポロジ

    -   デプロイされている`tidb-server` / `pd-server` / `tikv-server`インスタンスの数は?
    -   これらのインスタンスはどのようにマシンに分散されていますか?

-   これらのインスタンスがデプロイされるマシンのハードウェア構成:

    -   CPUコア数
    -   メモリのサイズ
    -   ディスクのタイプ (SSD またはハード ドライブ ディスク)
    -   それらは物理マシンですか、それとも仮想マシンですか?

<!---->

-   TiDB クラスター以外のサービスはありますか?
-   `pd-server`と`tikv-server`は別々に展開されますか?
-   現在の運用は？
-   `top -H`コマンドで CPU スレッド名を確認します。
-   最近のネットワークまたは IO 監視データに例外はありますか?
