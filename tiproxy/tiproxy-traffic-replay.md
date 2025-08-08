---
title: TiProxy Traffic Replay
summary: TiProxy トラフィック再生機能の使用例と手順を紹介します。
---

# TiProxy トラフィックリプレイ {#tiproxy-traffic-replay}

> **警告：**
>
> 現在、TiProxy トラフィックリプレイ機能は実験的です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、GitHub で[問題](https://github.com/pingcap/tiproxy/issues)報告を行ってください。

TiProxy v1.3.0以降では、TiProxyを使用してTiDB本番クラスタのアクセストラフィックをキャプチャし、指定したレートでテストクラスタに再生することができます。この機能により、本番クラスタの実際のワークロードをテスト環境で再現し、SQL文の実行結果とパフォーマンスを検証できます。

<img src="https://docs-download.pingcap.com/media/images/docs/tiproxy/tiproxy-traffic-replay.png" alt="TiProxyトラフィックリプレイ" width="800" />

## ユースケース {#use-cases}

トラフィック リプレイは、次のシナリオに適しています。

-   **TiDB バージョンのアップグレードを確認する**: 新しい TiDB バージョンを使用してテスト クラスターで本番トラフィックを再生し、新しい TiDB バージョンがすべての SQL ステートメントを正常に実行できることを確認します。
-   **変更の影響を評価する**：テストクラスター上で本番のトラフィックをシミュレートし、クラスターへの変更の影響を検証します。例えば、構成項目やシステム変数の変更、テーブルスキーマの変更、TiDBの新機能の有効化などを行う前に、その影響を検証します。
-   **TiDBのスケーリング前にパフォーマンスを検証**：新しいスケールのテストクラスターで対応する速度でトラフィックを再生し、パフォーマンスが要件を満たしているかどうかを検証します。例えば、コスト削減のためにクラスターを50%縮小する計画を立てる場合、トラフィックを半分の速度で再生し、スケーリング後のSQLレイテンシーが要件を満たしているかどうかを検証します。
-   **パフォーマンス制限のテスト**: 同じ規模のテスト クラスターでトラフィックを複数回再生し、再生レートを毎回上げてその規模のスループット制限をテストし、パフォーマンスが将来のビジネス成長のニーズを満たすかどうかを評価します。

トラフィック再生は、次のシナリオには適していません。

-   TiDB と MySQL 間の SQL 互換性を確認します。TiProxy は生成したトラフィック ファイルの読み取りのみをサポートしており、MySQL からのトラフィックをキャプチャして TiDB で再生することはできません。
-   TiDB バージョン間で SQL 実行結果を比較します。TiProxy は、SQL ステートメントが正常に実行されたかどうかのみを確認し、結果を比較しません。

## 使用法 {#usage}

1.  テスト環境を準備します。

    1.  テストクラスタを作成します。詳細については、 [TiUPを使用して TiDBクラスタをデプロイ](/production-deployment-using-tiup.md)参照してください。
    2.  `tiproxyctl`インストールし、 `tiproxyctl`インストールされているホストが本番とテスト環境の両方の TiProxy インスタンスに接続できることを確認します。詳細については、 [TiProxyコントロールをインストールする](/tiproxy/tiproxy-command-line-flags.md#install-tiproxy-control)参照してください。
    3.  本番クラスタからテスト環境クラスタにデータを複製します。詳細については、 [データ移行の概要](/migration-overview.md)参照してください。
    4.  テスト クラスターで[`ANALYZE`](/sql-statements/sql-statement-analyze-table.md)ステートメントを実行して統計を更新します。

2.  [`tiproxyctl traffic capture`](/tiproxy/tiproxy-command-line-flags.md#traffic-capture)コマンドを使用して、本番クラスターの TiProxy インスタンスに接続し、トラフィックのキャプチャを開始します。

    > **注記：**
    >
    > -   TiProxy は、既存の接続と新しく作成された接続を含むすべての接続のトラフィックをキャプチャします。
    > -   TiProxy プライマリ/セカンダリ モードで、プライマリ TiProxy インスタンスに接続します。
    > -   TiProxy が仮想 IP で構成されている場合は、仮想 IP アドレスに接続することをお勧めします。
    > -   TiProxyのCPU使用率が高いほど、トラフィックキャプチャによるQPSへの影響が大きくなります。本番クラスタへの影響を軽減するには、CPU容量の少なくとも30%を予約することをお勧めします。これにより、平均QPSが約3%低下します。詳細なパフォーマンスデータについては、 [トラフィックキャプチャテスト](/tiproxy/tiproxy-performance-test.md#traffic-capture-test)ご覧ください。
    > -   TiProxyはトラフィックを再度キャプチャする際に、以前のキャプチャファイルを自動的に削除しません。手動で削除する必要があります。

    たとえば、次のコマンドは、 `10.0.1.10:3080`の TiProxy インスタンスに接続し、1 時間のトラフィックをキャプチャし、それを TiProxy インスタンスの`/tmp/traffic`ディレクトリに保存します。

    ```shell
    tiproxyctl traffic capture --host 10.0.1.10 --port 3080 --output="/tmp/traffic" --duration=1h
    ```

    トラフィックファイルは自動的にローテーションされ、圧縮されます。1 `/tmp/traffic`内のファイルの例:

    ```shell
    ls /tmp/traffic
    # meta    traffic-2024-08-29T17-37-12.477.log.gz  traffic-2024-08-29T17-43-11.166.log.gz traffic.log
    ```

    詳細については[`tiproxyctl traffic capture`](/tiproxy/tiproxy-command-line-flags.md#traffic-capture)参照してください。

3.  トラフィック ファイル ディレクトリをテスト クラスターの TiProxy インスタンスにコピーします。

4.  [`tiproxyctl traffic replay`](/tiproxy/tiproxy-command-line-flags.md#traffic-replay)使用してテスト クラスターの TiProxy インスタンスに接続し、トラフィックの再生を開始します。

    デフォルトでは、SQL ステートメントは本番クラスターと同じ速度で実行され、各データベース接続は本番クラスター内の接続に対応して、本番負荷をシミュレートし、一貫したトランザクション実行順序を確保します。

    たとえば、次のコマンドは、ユーザー名`u1`とパスワード`123456`を使用して`10.0.1.10:3080`の TiProxy インスタンスに接続し、TiProxy インスタンスの`/tmp/traffic`ディレクトリからトラフィック ファイルを読み取り、トラフィックを再生します。

    ```shell
    tiproxyctl traffic replay --host 10.0.1.10 --port 3080 --username="u1" --password="123456" --input="/tmp/traffic"
    ```

    すべてのトラフィックはユーザー`u1`で実行されるため、 `u1`すべてのデータベースとテーブルにアクセスできることを確認してください。該当するユーザーが存在しない場合は、作成してください。

    詳細については[`tiproxyctl traffic replay`](/tiproxy/tiproxy-command-line-flags.md#traffic-replay)参照してください。

5.  リプレイレポートをビュー。

    再生が完了すると、レポートはテストクラスターのデータベース`tiproxy_traffic_replay`に保存されます。このデータベースには、テーブル`fail`と`other_errors` 2つのテーブルが含まれています。

    `fail`テーブルには、次のフィールドを持つ失敗した SQL ステートメントが格納されます。

    -   `cmd_type` : 失敗したコマンドのタイプ。例: `Query` (通常のステートメントを実行)、 `Prepare` (ステートメントを準備)、 `Execute` (プリペアドステートメントを実行)。
    -   `digest` : 失敗した SQL ステートメントのダイジェスト。
    -   `sample_stmt` : ステートメントが最初に失敗したときの SQL テキスト。
    -   `sample_err_msg` : SQL ステートメントが失敗した場合のエラー メッセージ。
    -   `sample_conn_id` : SQL文のトラフィックファイルに記録された接続ID。これを使用して、トラフィックファイル内の実行コンテキストを表示できます。
    -   `sample_capture_time` : トラフィックファイルに記録されたSQL文の実行時間。これを使用して、トラフィックファイル内の実行コンテキストを確認できます。
    -   `sample_replay_time` : 再生中にSQL文が失敗した時刻。これを使用して、TiDBログファイルでエラー情報を確認できます。
    -   `count` : SQL ステートメントが失敗した回数。

    以下はテーブル`fail`の出力例です。

    ```sql
    SELECT * FROM tiproxy_traffic_replay.fail LIMIT 1\G
    ```

        *************************** 1. row ***************************
                   cmd_type: StmtExecute
                     digest: 89c5c505772b8b7e8d5d1eb49f4d47ed914daa2663ed24a85f762daa3cdff43c
                sample_stmt: INSERT INTO new_order (no_o_id, no_d_id, no_w_id) VALUES (?, ?, ?) params=[3077 6 1]
             sample_err_msg: ERROR 1062 (23000): Duplicate entry '1-6-3077' for key 'new_order.PRIMARY'
             sample_conn_id: 1356
        sample_capture_time: 2024-10-17 12:59:15
         sample_replay_time: 2024-10-17 13:05:05
                      count: 4

    `other_errors`テーブルには、ネットワーク エラーやデータベース接続エラーなどの予期しないエラーが次のフィールドに格納されます。

    -   `err_type` : エラーの種類。簡潔なエラーメッセージとして表示されます。例: `i/o timeout` 。
    -   `sample_err_msg` : エラーが最初に発生したときの完全なエラー メッセージ。
    -   `sample_replay_time` : 再生中にエラーが発生した時刻。これを使用して、TiDBログファイルでエラー情報を確認できます。
    -   `count` : このエラーの発生回数。

    以下はテーブル`other_errors`の出力例です。

    ```sql
    SELECT * FROM tiproxy_traffic_replay.other_errors LIMIT 1\G
    ```

        *************************** 1. row ***************************
                  err_type: failed to read the connection: EOF
            sample_err_msg: this is an error from the backend connection: failed to read the connection: EOF
        sample_replay_time: 2024-10-17 12:57:39
                     count: 1

    > **注記：**
    >
    > -   `tiproxy_traffic_replay`のテーブルスキーマは将来のバージョンで変更される可能性があります。アプリケーションやツールの開発において、 `tiproxy_traffic_replay`のデータを直接読み取ることは推奨されません。
    > -   リプレイでは、接続間のトランザクション実行順序がキャプチャシーケンスと完全に一致することが保証されません。そのため、誤ったエラーレポートが生成される可能性があります。
    > -   TiProxyはトラフィックを再生する際に、以前の再生レポートを自動的に削除しません。手動で削除する必要があります。

## テストスループット {#test-throughput}

クラスターのスループットをテストするには、 `--speed`オプションを使用して再生レートを調整します。

たとえば、 `--speed=2` SQL ステートメントを 2 倍の速度で実行し、合計再生時間を半分に短縮します。

```shell
tiproxyctl traffic replay --host 10.0.1.10 --port 3080 --username="u1" --password="123456" --input="/tmp/traffic" --speed=2
```

再生速度を上げると、SQL文間のアイドル時間が短縮されるだけで、接続数は増加しません。セッションのアイドル時間が既に短い場合、速度を上げてもスループットが効果的に向上しない可能性があります。このような場合は、複数のTiProxyインスタンスを導入して同じトラフィックファイルを同時に再生することで、同時実行性を高め、スループットを向上させることができます。

## タスクのビューと管理 {#view-and-manage-tasks}

キャプチャと再生中に不明なエラーが発生した場合、タスクは自動的に停止します。現在のタスクの進行状況や前回のタスクのエラー情報を表示するには、 [`tiproxyctl traffic show`](/tiproxy/tiproxy-command-line-flags.md#traffic-show)コマンドを使用します。

```shell
tiproxyctl traffic show --host 10.0.1.10 --port 3080
```

たとえば、次の出力は実行中のキャプチャ タスクを示します。

```json
[
   {
      "type": "capture",
      "start_time": "2024-09-03T09:10:58.220644+08:00",
      "duration": "2h",
      "output": "/tmp/traffic",
      "progress": "45%",
      "status": "running"
   }
]
```

詳細については[`tiproxyctl traffic show`](/tiproxy/tiproxy-command-line-flags.md#traffic-show)参照してください。

現在のキャプチャまたは再生タスクをキャンセルするには、 [`tiproxyctl traffic cancel`](/tiproxy/tiproxy-command-line-flags.md#traffic-cancel)コマンドを使用します。

```shell
tiproxyctl traffic cancel --host 10.0.1.10 --port 3080
```

詳細については[`tiproxyctl traffic cancel`](/tiproxy/tiproxy-command-line-flags.md#traffic-cancel)参照してください。

## 制限事項 {#limitations}

-   TiProxyは、TiProxyによってキャプチャされたトラフィックファイルの再生のみをサポートしており、他のファイル形式はサポートしていません。そのため、まずはTiProxyを使用して本番クラスタからトラフィックをキャプチャしてください。
-   TiProxyトラフィックの再生はSQLタイプのフィルタリングをサポートしておらず、DMLおよびDDL文が再生されます。そのため、再度再生する前に、クラスターデータを再生前の状態に復元する必要があります。
-   TiProxy トラフィック再生では、トラフィックの再生に同じユーザー名が使用されるため、テスト[リソース管理](/tidb-resource-control-ru-groups.md)と[権限管理](/privilege-management.md)サポートされません。
-   TiProxy は[`LOAD DATA`](/sql-statements/sql-statement-load-data.md)ステートメントの再生をサポートしていません。

## その他のリソース {#more-resources}

TiProxy のトラフィック再生の詳細については、 [設計書](https://github.com/pingcap/tiproxy/blob/main/docs/design/2024-08-27-traffic-replay.md)参照してください。
