---
title: TiProxy Traffic Replay
summary: TiProxy トラフィック再生機能の使用例と手順を紹介します。
---

# TiProxy トラフィック再生 {#tiproxy-traffic-replay}

> **警告：**
>
> 現在、TiProxy トラフィック再生機能は実験的です。実本番環境での使用は推奨されません。この機能は予告なしに変更または削除される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tiproxy/issues)を報告できます。

TiProxy v1.3.0 以降では、TiProxy を使用して TiDB本番クラスターのアクセス トラフィックをキャプチャし、指定されたレートでテスト クラスターで再生することができます。この機能により、実本番クラスターの実際のワークロードをテスト環境で再現し、SQL ステートメントの実行結果とパフォーマンスを検証できます。

<img src="https://download.pingcap.com/images/docs/tiproxy/tiproxy-traffic-replay.png" alt="TiProxy トラフィック再生" width="800" />

## ユースケース {#use-cases}

トラフィック再生は、次のシナリオに適しています。

-   **TiDB バージョンのアップグレードを確認する**: 新しい TiDB バージョンを使用してテスト クラスターで本番トラフィックを再生し、新しい TiDB バージョンがすべての SQL ステートメントを正常に実行できることを確認します。
-   **変更の影響を評価する**: テスト クラスターで本番トラフィックをシミュレートして、クラスターへの変更の影響を確認します。たとえば、構成項目やシステム変数を変更する前、テーブル スキーマを変更する前、または新しい TiDB 機能を有効にする前に、影響を確認します。
-   **TiDB スケーリングの前にパフォーマンスを検証する**: 新しいスケールのテスト クラスターで対応する速度でトラフィックを再生し、パフォーマンスが要件を満たしているかどうかを検証します。たとえば、コスト削減のためにクラスターを 50% 縮小する計画を立てるには、トラフィックを半分の速度で再生し、スケーリング後に SQLレイテンシーが要件を満たしているかどうかを検証します。
-   **パフォーマンスの制限をテストする**: 同じ規模のテスト クラスターでトラフィックを複数回再生し、再生レートを毎回上げてその規模のスループット制限をテストし、パフォーマンスが将来のビジネス成長のニーズを満たすかどうかを評価します。

トラフィック再生は、次のシナリオには適していません。

-   TiDB と MySQL 間の SQL 互換性を確認します。TiProxy は、生成したトラフィック ファイルの読み取りのみをサポートしており、MySQL からのトラフィックをキャプチャして TiDB で再生することはできません。
-   TiDB バージョン間で SQL 実行結果を比較します。TiProxy は、SQL ステートメントが正常に実行されたかどうかのみを検証し、結果を比較しません。

## 使用法 {#usage}

1.  テスト環境を準備します。

    1.  テスト クラスターを作成します。詳細については、 [TiUP を使用して TiDBクラスタをデプロイ](/production-deployment-using-tiup.md)参照してください。
    2.  `tiproxyctl`インストールし、 `tiproxyctl`のホストが本番とテスト クラスターの両方で TiProxy インスタンスに接続できることを確認します。詳細については、 [TiProxy コントロールをインストールする](/tiproxy/tiproxy-command-line-flags.md#install-tiproxy-control)参照してください。
    3.  本番クラスターからテスト クラスターにデータを複製します。詳細については、 [データ移行の概要](/migration-overview.md)参照してください。
    4.  統計を更新するには、テスト クラスターで[`ANALYZE`](/sql-statements/sql-statement-analyze-table.md)ステートメントを実行します。

2.  [`tiproxyctl traffic capture`](/tiproxy/tiproxy-command-line-flags.md#traffic-capture)コマンドを使用して、本番クラスターの TiProxy インスタンスに接続し、トラフィックのキャプチャを開始します。

    > **注記：**
    >
    > -   TiProxy は、既存の接続と新しく作成された接続を含むすべての接続のトラフィックをキャプチャします。
    > -   TiProxy プライマリ/セカンダリ モードで、プライマリ TiProxy インスタンスに接続します。
    > -   TiProxy が仮想 IP で構成されている場合は、仮想 IP アドレスに接続することをお勧めします。
    > -   TiProxy の CPU 使用率が高くなるほど、トラフィック キャプチャが QPS に与える影響が大きくなります。本番クラスターへの影響を軽減するには、CPU 容量の少なくとも 30% を予約することをお勧めします。これにより、平均 QPS が約 3% 減少します。詳細なパフォーマンス データについては、 [トラフィックキャプチャテスト](/tiproxy/tiproxy-performance-test.md#traffic-capture-test)参照してください。
    > -   TiProxy はトラフィックを再度キャプチャするときに以前のキャプチャ ファイルを自動的に削除しません。手動で削除する必要があります。

    たとえば、次のコマンドは、 `10.0.1.10:3080`の TiProxy インスタンスに接続し、1 時間のトラフィックをキャプチャし、それを TiProxy インスタンスの`/tmp/traffic`ディレクトリに保存します。

    ```shell
    tiproxyctl traffic capture --host 10.0.1.10 --port 3080 --output="/tmp/traffic" --duration=1h
    ```

    トラフィック ファイルは自動的にローテーションされ、圧縮されます。1 `/tmp/traffic`内のファイルの例:

    ```shell
    ls /tmp/traffic
    # meta    traffic-2024-08-29T17-37-12.477.log.gz  traffic-2024-08-29T17-43-11.166.log.gz traffic.log
    ```

    詳細については[`tiproxyctl traffic capture`](/tiproxy/tiproxy-command-line-flags.md#traffic-capture)参照してください。

3.  トラフィック ファイル ディレクトリをテスト クラスターの TiProxy インスタンスにコピーします。

4.  [`tiproxyctl traffic replay`](/tiproxy/tiproxy-command-line-flags.md#traffic-replay)使用してテスト クラスターの TiProxy インスタンスに接続し、トラフィックの再生を開始します。

    デフォルトでは、SQL ステートメントは実本番クラスターと同じ速度で実行され、各データベース接続は本番クラスターの接続に対応して、本番負荷をシミュレートし、一貫したトランザクション実行順序を確保します。

    たとえば、次のコマンドは、ユーザー名`u1`とパスワード`123456`使用して`10.0.1.10:3080`の TiProxy インスタンスに接続し、TiProxy インスタンスの`/tmp/traffic`ディレクトリからトラフィック ファイルを読み取り、トラフィックを再生します。

    ```shell
    tiproxyctl traffic replay --host 10.0.1.10 --port 3080 --username="u1" --password="123456" --input="/tmp/traffic"
    ```

    すべてのトラフィックはユーザー`u1`の下で実行されるため、 `u1`すべてのデータベースとテーブルにアクセスできることを確認してください。そのようなユーザーが存在しない場合は、作成してください。

    詳細については[`tiproxyctl traffic replay`](/tiproxy/tiproxy-command-line-flags.md#traffic-replay)参照してください。

5.  リプレイレポートをビュー。

    再生が完了すると、レポートはテスト クラスターの`tiproxy_traffic_replay`データベースに保存されます。このデータベースには、 `fail`と`other_errors` 2 つのテーブルが含まれています。

    `fail`テーブルには、次のフィールドを持つ失敗した SQL ステートメントが格納されます。

    -   `cmd_type` : 失敗したコマンドのタイプ。たとえば、 `Query` (通常のステートメントを実行)、 `Prepare` (ステートメントを準備)、 `Execute` (プリペアドステートメントを実行) など。
    -   `digest` : 失敗した SQL ステートメントのダイジェスト。
    -   `sample_stmt` : ステートメントが最初に失敗したときの SQL テキスト。
    -   `sample_err_msg` : SQL ステートメントが失敗した場合のエラー メッセージ。
    -   `sample_conn_id` : SQL ステートメントのトラフィック ファイルに記録された接続 ID。これを使用して、トラフィック ファイル内の実行コンテキストを表示できます。
    -   `sample_capture_time` : SQL ステートメントのトラフィック ファイルに記録された実行時間。これを使用して、トラフィック ファイル内の実行コンテキストを表示できます。
    -   `sample_replay_time` : 再生中に SQL ステートメントが失敗した時刻。これを使用して、TiDB ログ ファイルでエラー情報を表示できます。
    -   `count` : SQL ステートメントが失敗した回数。

    以下は`fail`のテーブルの出力例です。

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

    -   `err_type` : エラーの種類。簡単なエラー メッセージとして表示されます。たとえば、 `i/o timeout` 。
    -   `sample_err_msg` : エラーが最初に発生したときの完全なエラー メッセージ。
    -   `sample_replay_time` : 再生中にエラーが発生した時刻。これを使用して、TiDB ログ ファイル内のエラー情報を表示できます。
    -   `count` : このエラーの発生回数。

    以下は`other_errors`のテーブルの出力例です。

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
    > -   `tiproxy_traffic_replay`のテーブル スキーマは将来のバージョンで変更される可能性があります。アプリケーションやツールの開発で`tiproxy_traffic_replay`からデータを直接読み取ることは推奨されません。
    > -   再生では、接続間のトランザクション実行順序がキャプチャ シーケンスと正確に一致することが保証されません。これにより、誤ったエラー レポートが発生する可能性があります。
    > -   TiProxy はトラフィックを再生するときに以前の再生レポートを自動的に削除しません。手動で削除する必要があります。

## テストスループット {#test-throughput}

クラスターのスループットをテストするには、 `--speed`オプションを使用して再生レートを調整します。

たとえば、 `--speed=2` SQL ステートメントを 2 倍の速度で実行し、合計再生時間を半分に短縮します。

```shell
tiproxyctl traffic replay --host 10.0.1.10 --port 3080 --username="u1" --password="123456" --input="/tmp/traffic" --speed=2
```

再生速度を上げると、SQL ステートメント間のアイドル時間が短縮されるだけで、接続数は増加しません。セッションのアイドル時間がすでに短い場合、速度を上げてもスループットが効果的に向上しない可能性があります。このような場合は、複数の TiProxy インスタンスを展開して同じトラフィック ファイルを同時に再生し、同時実行性を高めてスループットを向上させることができます。

## タスクのビューと管理 {#view-and-manage-tasks}

キャプチャおよび再生中に不明なエラーが発生すると、タスクは自動的に停止します。現在のタスクの進行状況または最後のタスクのエラー情報を表示するには、 [`tiproxyctl traffic show`](/tiproxy/tiproxy-command-line-flags.md#traffic-show)コマンドを使用します。

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

-   TiProxy は、TiProxy によってキャプチャされたトラフィック ファイルの再生のみをサポートしており、他のファイル形式はサポートしていません。したがって、最初に TiProxy を使用して実本番クラスターからトラフィックをキャプチャするようにしてください。
-   TiProxy トラフィック再生では、SQL タイプのフィルタリングはサポートされておらず、DML および DDL ステートメントが再生されます。したがって、再度再生する前に、クラスター データを再生前の状態に復元する必要があります。
-   TiProxy はトラフィックの再生に同じユーザー名を使用するため、TiProxy トラフィックの再生ではテスト[リソース管理](/tidb-resource-control.md)と[権限管理](/privilege-management.md)サポートされません。
-   TiProxy は[`LOAD DATA`](/sql-statements/sql-statement-load-data.md)ステートメントの再生をサポートしていません。

## その他のリソース {#more-resources}

TiProxy のトラフィック再生の詳細については、 [設計文書](https://github.com/pingcap/tiproxy/blob/main/docs/design/2024-08-27-traffic-replay.md)を参照してください。
