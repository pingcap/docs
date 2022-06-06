---
title: Troubleshoot TiCDC
summary: Learn how to troubleshoot issues you might encounter when you use TiCDC.
---

# TiCDCのトラブルシューティング {#troubleshoot-ticdc}

このドキュメントでは、TiCDCを使用するときに発生する可能性のある一般的な問題とエラー、および対応するメンテナンスとトラブルシューティングの方法を紹介します。

> **ノート：**
>
> このドキュメントでは、 `cdc cli`コマンドで指定されたPDアドレスは`--pd=http://10.0.10.25:2379`です。コマンドを使用するときは、アドレスを実際のPDアドレスに置き換えてください。

## TiCDCでタスクを作成するときに<code>start-ts</code>を選択するにはどうすればよいですか？ {#how-do-i-choose-code-start-ts-code-when-creating-a-task-in-ticdc}

レプリケーションタスクの`start-ts`は、アップストリームTiDBクラスタのタイムスタンプOracle（TSO）に対応します。 TiCDCは、レプリケーションタスクでこのTSOにデータを要求します。したがって、レプリケーションタスクの`start-ts`は、次の要件を満たす必要があります。

-   `start-ts`の値は、現在のTiDBクラスタの`tikv_gc_safe_point`の値よりも大きくなります。そうしないと、タスクの作成時にエラーが発生します。
-   タスクを開始する前に、ダウンストリームに`start-ts`より前のすべてのデータがあることを確認してください。メッセージキューへのデータの複製などのシナリオで、アップストリームとダウンストリーム間のデータの整合性が必要ない場合は、アプリケーションのニーズに応じてこの要件を緩和できます。

`start-ts`を指定しない場合、または`start-ts`を`0`として指定する場合、レプリケーションタスクの開始時に、TiCDCは現在のTSOを取得し、このTSOからタスクを開始します。

## TiCDCでタスクを作成すると、一部のテーブルを複製できないのはなぜですか？ {#why-can-t-some-tables-be-replicated-when-i-create-a-task-in-ticdc}

`cdc cli changefeed create`を実行してレプリケーションタスクを作成すると、TiCDCはアップストリームテーブルが[複製の制限](/ticdc/ticdc-overview.md#restrictions)を満たしているかどうかを確認します。一部のテーブルが制限を満たしていない場合は、不適格なテーブルのリストとともに`some tables are not eligible to replicate`が返されます。 `Y`または`y`を選択してタスクの作成を続行でき、これらのテーブルのすべての更新はレプリケーション中に自動的に無視されます。 `Y`または`y`以外の入力を選択した場合、レプリケーションタスクは作成されません。

## TiCDCレプリケーションタスクの状態を表示するにはどうすればよいですか？ {#how-do-i-view-the-state-of-ticdc-replication-tasks}

TiCDCレプリケーションタスクのステータスを表示するには、 `cdc cli`を使用します。例えば：

{{< copyable "" >}}

```shell
cdc cli changefeed list --pd=http://10.0.10.25:2379
```

期待される出力は次のとおりです。

```json
[{
    "id": "4e24dde6-53c1-40b6-badf-63620e4940dc",
    "summary": {
      "state": "normal",
      "tso": 417886179132964865,
      "checkpoint": "2020-07-07 16:07:44.881",
      "error": null
    }
}]
```

-   `checkpoint` ：TiCDCは、このタイムスタンプより前のすべてのデータをダウンストリームに複製しました。
-   `state` ：このレプリケーションタスクの状態：
    -   `normal` ：タスクは正常に実行されます。
    -   `stopped` ：タスクが手動で停止されたか、エラーが発生しました。
    -   `removed` ：タスクが削除されます。

> **ノート：**
>
> この機能はTiCDC4.0.3で導入されました。

## TiCDCレプリケーションの中断 {#ticdc-replication-interruptions}

### TiCDCレプリケーションタスクが中断されているかどうかを確認するにはどうすればよいですか？ {#how-do-i-know-whether-a-ticdc-replication-task-is-interrupted}

-   Grafanaダッシュボードでレプリケーションタスクの`changefeed checkpoint`のモニタリングメトリックを確認します（右の`changefeed id`を選択します）。メトリック値が変更されない場合、または`checkpoint lag`メトリックが増加し続ける場合は、レプリケーションタスクが中断される可能性があります。
-   `exit error count`の監視メトリックを確認します。メトリック値が`0`より大きい場合、レプリケーションタスクでエラーが発生しています。
-   `cdc cli changefeed list`と`cdc cli changefeed query`を実行して、レプリケーションタスクのステータスを確認します。 `stopped`はタスクが停止したことを意味し、 `error`項目は詳細なエラーメッセージを提供します。エラーが発生した後、TiCDCサーバーログで`error on running processor`を検索して、トラブルシューティングのためのエラースタックを確認できます。
-   極端な場合には、TiCDCサービスが再起動されます。トラブルシューティングのために、TiCDCサーバーログで`FATAL`レベルのログを検索できます。

### レプリケーションタスクが手動で停止されているかどうかを確認するにはどうすればよいですか？ {#how-do-i-know-whether-the-replication-task-is-stopped-manually}

`cdc cli`を実行すると、レプリケーションタスクが手動で停止されているかどうかを確認できます。例えば：

{{< copyable "" >}}

```shell
cdc cli changefeed query --pd=http://10.0.10.25:2379 --changefeed-id 28c43ffc-2316-4f4f-a70b-d1a7c59ba79f
```

上記のコマンドの出力で、 `admin-job-type`はこのレプリケーションタスクの状態を示しています。

-   `0` ：進行中です。これは、タスクが手動で停止されていないことを意味します。
-   `1` ：一時停止。タスクが一時停止されると、複製されたすべての`processor`が終了します。タスクの構成と複製ステータスは保持されるため、 `checkpiont-ts`からタスクを再開できます。
-   `2` ：再開しました。レプリケーションタスクは`checkpoint-ts`から再開します。
-   `3` ：削除されました。タスクが削除されると、複製された`processor`がすべて終了し、複製タスクの構成情報がクリアされます。レプリケーションステータスは、後のクエリのためにのみ保持されます。

### レプリケーションの中断を処理するにはどうすればよいですか？ {#how-do-i-handle-replication-interruptions}

次の既知のシナリオでは、レプリケーションタスクが中断される可能性があります。

-   ダウンストリームは引き続き異常であり、TiCDCは何度も再試行した後も失敗します。

    -   このシナリオでは、TiCDCはタスク情報を保存します。 TiCDCはPDにサービスGCセーフポイントを設定しているため、タスクチェックポイント後のデータは有効期間`gc-ttl`以内にTiKVGCによってクリーンアップされません。

    -   処理方法：ダウンストリームが通常に戻った後、HTTPインターフェースを介してレプリケーションタスクを再開できます。

-   ダウンストリームに互換性のないSQLステートメントがあるため、レプリケーションを続行できません。

    -   このシナリオでは、TiCDCはタスク情報を保存します。 TiCDCはPDにサービスGCセーフポイントを設定しているため、タスクチェックポイント後のデータは有効期間`gc-ttl`以内にTiKVGCによってクリーンアップされません。
    -   取り扱い手順：
        1.  `cdc cli changefeed query`コマンドを使用してレプリケーションタスクのステータス情報を照会し、値`checkpoint-ts`を記録します。
        2.  新しいタスク構成ファイルを使用し、 `ignore-txn-start-ts`パラメーターを追加して、指定された`start-ts`に対応するトランザクションをスキップします。
        3.  HTTPAPIを介して古いレプリケーションタスクを停止します。 `cdc cli changefeed create`を実行して新しいタスクを作成し、新しいタスク構成ファイルを指定します。手順1で記録した`checkpoint-ts`を`start-ts`として指定し、新しいタスクを開始してレプリケーションを再開します。

-   TiCDC v4.0.13以前のバージョンでは、TiCDCがパーティションテーブルを複製するときに、複製の中断につながるエラーが発生する場合があります。

    -   このシナリオでは、TiCDCはタスク情報を保存します。 TiCDCはPDにサービスGCセーフポイントを設定しているため、タスクチェックポイント後のデータは有効期間`gc-ttl`以内にTiKVGCによってクリーンアップされません。
    -   取り扱い手順：
        1.  `cdc cli changefeed pause -c <changefeed-id>`を実行して、レプリケーションタスクを一時停止します。
        2.  約1つのムナイトを待ってから、 `cdc cli changefeed resume -c <changefeed-id>`を実行してレプリケーションタスクを再開します。

### タスクの中断後にTiCDCが再起動された後に発生するOOMを処理するにはどうすればよいですか？ {#what-should-i-do-to-handle-the-oom-that-occurs-after-ticdc-is-restarted-after-a-task-interruption}

-   TiDBクラスタとTiCDCクラスタを最新バージョンに更新します。 OOMの問題は、 **v4.0.14以降のv4.0バージョン、v5.0.2以降のv5.0バージョン、および最新バージョンで**はすでに解決されています。

-   上記の更新バージョンでは、ユニファイドソーターを有効にして、システムメモリが不足しているときにディスク内のデータを並べ替えることができます。この機能を有効にするには、レプリケーションタスクを作成するときに`--sort-engine=unified`から`cdc cli`のコマンドを渡すことができます。例えば：

{{< copyable "" >}}

```shell
cdc cli changefeed update -c <changefeed-id> --sort-engine="unified" --pd=http://10.0.10.25:2379
```

クラスタを上記の新しいバージョンに更新できない場合でも、**以前のバージョン**でユニファイドソーターを有効にすることができます。レプリケーションタスクを作成するときに、 `--sort-engine=unified`と`--sort-dir=/path/to/sort_dir`を`cdc cli`コマンドに渡すことができます。例えば：

{{< copyable "" >}}

```shell
cdc cli changefeed update -c <changefeed-id> --sort-engine="unified" --sort-dir="/data/cdc/sort" --pd=http://10.0.10.25:2379
```

> **ノート：**
>
> -   v4.0.9以降、TiCDCは統合ソーターエンジンをサポートしています。
> -   TiCDC（4.0バージョン）は、ソートエンジンの動的な変更をまだサポートしていません。ソーター設定を変更する前に、チェンジフィードが停止していることを確認してください。
> -   `sort-dir`は、バージョンごとに動作が異なります。 [`sort-dir`と<code>data-dir</code>の互換性に関する注意事項](/ticdc/ticdc-overview.md#compatibility-notes-for-sort-dir-and-data-dir)を参照し、注意して設定してください。
> -   現在、統合ソーターは実験的機能です。テーブルの数が多すぎる場合（&gt; = 100）、統合ソーターはパフォーマンスの問題を引き起こし、レプリケーションのスループットに影響を与える可能性があります。したがって、実稼働環境での使用はお勧めしません。統合ソーターを有効にする前に、各TiCDCノードのマシンに十分なディスク容量があることを確認してください。未処理のデータ変更の合計サイズが1TBを超える可能性がある場合は、レプリケーションにTiCDCを使用することはお勧めしません。

## TiCDC <code>gc-ttl</code>とは何ですか？ {#what-is-code-gc-ttl-code-in-ticdc}

v4.0.0-rc.1以降、PDはサービスレベルのGCセーフポイントの設定で外部サービスをサポートします。どのサービスでも、GCセーフポイントを登録および更新できます。 PDは、このGCセーフポイントより後のキー値データがGCによってクリーンアップされないようにします。

レプリケーションタスクが使用できないか中断されている場合、この機能により、TiCDCによって消費されるデータがGCによってクリーンアップされることなくTiKVに保持されます。

TiCDCサーバーを起動するときに、 `gc-ttl`を構成することにより、GCセーフポイントの存続時間（TTL）期間を指定できます。 `gc-ttl`もでき[TiUPを使用して変更する](/ticdc/manage-ticdc.md#modify-ticdc-configuration-using-tiup) 。デフォルト値は24時間です。 TiCDCでは、この値は次のことを意味します。

-   TiCDCサービスが停止した後、GCセーフポイントがPDに保持される最大時間。
-   タスクが中断または手動で停止された後、レプリケーションタスクを一時停止できる最大時間。中断されたレプリケーションタスクの時間が`gc-ttl`で設定された値よりも長い場合、レプリケーションタスクは`failed`ステータスになり、再開できず、GCセーフポイントの進行に影響を与え続けることができません。

上記の2番目の動作は、TiCDCv4.0.13以降のバージョンで導入されています。目的は、TiCDCのレプリケーションタスクが長時間中断され、アップストリームTiKVクラスタのGCセーフポイントが長時間継続せず、古いデータバージョンが多すぎて、アップストリームクラスタのパフォーマンスに影響を与えるのを防ぐことです。

> **ノート：**
>
> 一部のシナリオでは、たとえば、 Dumpling/ BRを使用した完全レプリケーションの後に増分レプリケーションにTiCDCを使用する場合、デフォルトの24時間の`gc-ttl`では不十分な場合があります。 TiCDCサーバーを起動するときは、 `gc-ttl`に適切な値を指定する必要があります。

## TiCDCガベージコレクション（GC）セーフポイントの完全な動作は何ですか？ {#what-is-the-complete-behavior-of-ticdc-garbage-collection-gc-safepoint}

TiCDCサービスの開始後にレプリケーションタスクが開始された場合、TiCDC所有者は、すべてのレプリケーションタスクの中で最小値の`checkpoint-ts`でPDサービスGCセーフポイントを更新します。サービスGCセーフポイントは、TiCDCがその時点およびそれ以降に生成されたデータを削除しないことを保証します。レプリケーションタスクが中断された場合、または手動で停止された場合、このタスクの`checkpoint-ts`は変更されません。一方、PDの対応するサービスGCセーフポイントも更新されません。

レプリケーションタスクが`gc-ttl`で指定された時間より長く中断された場合、レプリケーションタスクは`failed`ステータスになり、再開できません。 PDに対応するサービスGCセーフポイントは続行されます。

TiCDCがサービスGCセーフポイントに設定するTime-To-Live（TTL）は24時間です。つまり、TiCDCサービスが中断されてから24時間以内に回復できる場合、GCメカニズムはデータを削除しません。

## レプリケーションタスクを作成するとき、またはデータをMySQLにレプリケートするときに、 <code>Error 1298: Unknown or incorrect time zone: &#39;UTC&#39;</code>エラーを処理するにはどうすればよいですか？ {#how-do-i-handle-the-code-error-1298-unknown-or-incorrect-time-zone-utc-code-error-when-creating-the-replication-task-or-replicating-data-to-mysql}

このエラーは、ダウンストリームのMySQLがタイムゾーンをロードしない場合に返されます。 [`mysql_tzinfo_to_sql`](https://dev.mysql.com/doc/refman/8.0/en/mysql-tzinfo-to-sql.html)を実行すると、タイムゾーンを読み込むことができます。タイムゾーンを読み込んだ後、タスクを作成してデータを通常どおりに複製できます。

{{< copyable "" >}}

```shell
mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root mysql -p
```

上記のコマンドの出力が次のようなものである場合、インポートは成功しています。

```
Enter password:
Warning: Unable to load '/usr/share/zoneinfo/iso3166.tab' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/leap-seconds.list' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/zone.tab' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/zone1970.tab' as time zone. Skipping it.
```

ダウンストリームが特別なMySQL環境（パブリッククラウドRDSまたは一部のMySQL派生バージョン）であり、上記の方法を使用したタイムゾーンのインポートが失敗した場合、 `sink-uri`の`time-zone`パラメーターを使用してダウンストリームのMySQLタイムゾーンを指定する必要があります。最初に、MySQLで使用されるタイムゾーンをクエリできます。

1.  MySQLで使用されるタイムゾーンをクエリします。

    {{< copyable "" >}}

    ```sql
    show variables like '%time_zone%';
    ```

    ```
    +------------------+--------+
    | Variable_name    | Value  |
    +------------------+--------+
    | system_time_zone | CST    |
    | time_zone        | SYSTEM |
    +------------------+--------+
    ```

2.  レプリケーションタスクを作成してTiCDCサービスを作成するときに、タイムゾーンを指定します。

    {{< copyable "" >}}

    ```shell
    cdc cli changefeed create --sink-uri="mysql://root@127.0.0.1:3306/?time-zone=CST" --pd=http://10.0.10.25:2379
    ```

    > **ノート：**
    >
    > CSTは、次の4つの異なるタイムゾーンの略語である可能性があります。
    >
    > -   中部標準時（米国）UT-6:00
    > -   中央標準時間（オーストラリア）UT + 9：30
    > -   中国標準時UT+8：00
    > -   キューバ標準時UT-4:00
    >
    > 中国では、CSTは通常中国標準時の略です。

## TiCDCタイムゾーンとアップストリーム/ダウンストリームデータベースのタイムゾーンの関係を理解するにはどうすればよいですか？ {#how-to-understand-the-relationship-between-the-ticdc-time-zone-and-the-time-zones-of-the-upstream-downstream-databases}

|                              |                              上流のタイムゾーン                             |                                  TiCDCタイムゾーン                                 |                            下流のタイムゾーン                           |
| :--------------------------: | :----------------------------------------------------------------: | :--------------------------------------------------------------------------: | :------------------------------------------------------------: |
| Configuration / コンフィグレーション方法 |              [タイムゾーンのサポート](/configure-time-zone.md)を参照             |                       TiCDCサーバーの起動時に`--tz`パラメーターを使用して構成                      |               `sink-uri`の`time-zone`パラメータを使用して構成               |
|              説明              | アップストリームTiDBのタイムゾーン。タイムスタンプタイプのDML操作とタイムスタンプタイプの列に関連するDDL操作に影響します。 | TiCDCは、アップストリームTiDBのタイムゾーンがTiCDCタイムゾーン構成と同じであると想定し、タイムスタンプ列に対して関連する操作を実行します。 | ダウンストリームMySQLは、ダウンストリームタイムゾーン設定に従って、DMLおよびDDL操作のタイムスタンプを処理します。 |

> **ノート：**
>
> TiCDCサーバーのタイムゾーンを設定するときは注意してください。このタイムゾーンはタイムタイプの変換に使用されるためです。アップストリームタイムゾーン、TiCDCタイムゾーン、およびダウンストリームタイムゾーンの一貫性を保ちます。 TiCDCサーバーは、次の優先順位でタイムゾーンを選択します。
>
> -   TiCDCは、最初に`--tz`を使用して指定されたタイムゾーンを使用します。
> -   `--tz`が使用できない場合、TiCDCは`TZ`環境変数を使用して設定されたタイムゾーンを読み取ろうとします。
> -   `TZ`の環境変数が使用できない場合、TiCDCはマシンのデフォルトのタイムゾーンを使用します。

## <code>--config</code>で構成ファイルを指定せずにレプリケーションタスクを作成した場合のTiCDCのデフォルトの動作は何ですか？ {#what-is-the-default-behavior-of-ticdc-if-i-create-a-replication-task-without-specifying-the-configuration-file-in-code-config-code}

`-config`パラメータを指定せずに`cdc cli changefeed create`コマンドを使用すると、TiCDCは次のデフォルトの動作でレプリケーションタスクを作成します。

-   システムテーブルを除くすべてのテーブルを複製します
-   古い値機能を有効にします
-   [有効なインデックス](/ticdc/ticdc-overview.md#restrictions)を含まないテーブルの複製をスキップします

## TiCDCのアップグレードによって引き起こされる構成ファイルの非互換性の問題をどのように処理しますか？ {#how-do-i-handle-the-incompatibility-issue-of-configuration-files-caused-by-ticdc-upgrade}

[互換性に関する注意](/ticdc/manage-ticdc.md#notes-for-compatibility)を参照してください。

## TiCDCは、Canal形式でのデータ変更の出力をサポートしていますか？ {#does-ticdc-support-outputting-data-changes-in-the-canal-format}

はい。 Canal出力を有効にするには、 `--sink-uri`パラメーターでプロトコルを`canal`として指定します。例えば：

{{< copyable "" >}}

```shell
cdc cli changefeed create --pd=http://10.0.10.25:2379 --sink-uri="kafka://127.0.0.1:9092/cdc-test?kafka-version=2.4.0&protocol=canal" --config changefeed.toml
```

> **ノート：**
>
> -   この機能はTiCDC4.0.2で導入されました。
> -   TiCDCは現在、KafkaやPulsarなどのMQシンクにのみCanal形式でデータ変更を出力することをサポートしています。

詳細については、 [レプリケーションタスクを作成する](/ticdc/manage-ticdc.md#create-a-replication-task)を参照してください。

## TiCDCからKafkaまでのレイテンシーがますます高くなるのはなぜですか？ {#why-does-the-latency-from-ticdc-to-kafka-become-higher-and-higher}

-   [TiCDCレプリケーションタスクの状態を表示するにはどうすればよいですか](#how-do-i-view-the-state-of-ticdc-replication-tasks)を確認してください。
-   Kafkaの次のパラメータを調整します。

    -   `message.max.bytes`の値を`server.properties`から`1073741824` （1 GB）に増やします。
    -   `replica.fetch.max.bytes`の値を`server.properties`から`1073741824` （1 GB）に増やします。
    -   `consumer.properties`の`fetch.message.max.bytes`の値を増やして、 `message.max.bytes`の値より大きくします。

## TiCDCがデータをKafkaに複製するとき、トランザクション内のすべての変更を1つのメッセージに書き込みますか？そうでない場合、それはどのような基準で変更を分割しますか？ {#when-ticdc-replicates-data-to-kafka-does-it-write-all-the-changes-in-a-transaction-into-one-message-if-not-on-what-basis-does-it-divide-the-changes}

いいえ。構成されたさまざまな配布戦略に従って、 `row id`は`default` 、および`table`を含むさまざまなベースで変更を分割し`ts` 。

詳細については、 [レプリケーションタスク構成ファイル](/ticdc/manage-ticdc.md#task-configuration-file)を参照してください。

## TiCDCがKafkaにデータを複製するとき、TiDBの単一メッセージの最大サイズを制御できますか？ {#when-ticdc-replicates-data-to-kafka-can-i-control-the-maximum-size-of-a-single-message-in-tidb}

はい。 `max-message-bytes`パラメーターを設定して、毎回Kafkaブローカーに送信されるデータの最大サイズを制御できます（オプション、デフォルトでは`10MB` ）。 `max-batch-size`を設定して、各Kafkaメッセージの変更レコードの最大数を指定することもできます。現在、この設定は、Kafkaの`protocol`が`open-protocol` （オプション、デフォルトでは`16` ）の場合にのみ有効になります。

## TiCDCがデータをKafkaに複製するとき、メッセージには複数のタイプのデータ変更が含まれていますか？ {#when-ticdc-replicates-data-to-kafka-does-a-message-contain-multiple-types-of-data-changes}

はい。 1つのメッセージに複数の`update`または`delete`が含まれる場合があり、 `update`と`delete`が共存する場合があります。

## TiCDCがデータをKafkaに複製する場合、TiCDC Open Protocolの出力でタイムスタンプ、テーブル名、およびスキーマ名を表示するにはどうすればよいですか？ {#when-ticdc-replicates-data-to-kafka-how-do-i-view-the-timestamp-table-name-and-schema-name-in-the-output-of-ticdc-open-protocol}

この情報は、Kafkaメッセージのキーに含まれています。例えば：

```json
{
    "ts":<TS>,
    "scm":<Schema Name>,
    "tbl":<Table Name>,
    "t":1
}
```

詳細については、 [TiCDCOpenProtocolイベント形式](/ticdc/ticdc-open-protocol.md#event-format)を参照してください。

## TiCDCがデータをKafkaに複製するとき、メッセージ内のデータ変更のタイムスタンプをどのように知ることができますか？ {#when-ticdc-replicates-data-to-kafka-how-do-i-know-the-timestamp-of-the-data-changes-in-a-message}

Unixタイムスタンプを取得するには、Kafkaメッセージのキーの`ts`を18ビット右に移動します。

## TiCDC Open Protocolはどのように<code>null</code>を表しますか？ {#how-does-ticdc-open-protocol-represent-code-null-code}

TiCDC Open Protocolでは、タイプコード`6`は`null`を表します。

| タイプ | コード | 出力例                | ノート |
| :-- | :-- | :----------------- | :-- |
| ヌル  | 6   | `{"t":6,"v":null}` |     |

詳細については、 [TiCDCOpenProtocol列タイプコード](/ticdc/ticdc-open-protocol.md#column-type-code)を参照してください。

## TiCDCタスクの<code>start-ts</code>タイムスタンプは、現在の時刻とはかなり異なります。このタスクの実行中に、レプリケーションが中断され、エラー<code>[CDC:ErrBufferReachLimit]</code>が発生します {#the-code-start-ts-code-timestamp-of-the-ticdc-task-is-quite-different-from-the-current-time-during-the-execution-of-this-task-replication-is-interrupted-and-an-error-code-cdc-errbufferreachlimit-code-occurs}

v4.0.9以降では、レプリケーションタスクで統合ソーター機能を有効にするか、BRツールを使用して増分バックアップと復元を行い、新しい時間からTiCDCレプリケーションタスクを開始できます。

## TiCDC Open Protocolの行変更イベントが<code>INSERT</code>イベントなのか<code>UPDATE</code>イベントなのかはどうすればわかりますか？ {#how-can-i-tell-if-a-row-changed-event-of-ticdc-open-protocol-is-an-code-insert-code-event-or-an-code-update-code-event}

Old Value機能が有効になっていない場合、TiCDCOpenProtocolの行変更イベントが`INSERT`イベントであるか`UPDATE`イベントであるかを判断できません。この機能が有効になっている場合は、含まれているフィールドによってイベントタイプを判別できます。

-   `UPDATE`イベントには`"p"`フィールドと`"u"`フィールドの両方が含まれます
-   `INSERT`イベントには`"u"`フィールドのみが含まれます
-   `DELETE`イベントには`"d"`フィールドのみが含まれます

詳細については、 [オープンプロトコル行変更イベント形式](/ticdc/ticdc-open-protocol.md#row-changed-event)を参照してください。

## TiCDCはどのくらいのPDストレージを使用しますか？ {#how-much-pd-storage-does-ticdc-use}

TiCDCはPDでetcdを使用して、メタデータを保存し、定期的に更新します。 etcdのMVCCとPDのデフォルトの圧縮の間の時間間隔は1時間であるため、TiCDCが使用するPDストレージの量は、この1時間以内に生成されるメタデータバージョンの量に比例します。ただし、v4.0.5、v4.0.6、およびv4.0.7では、TiCDCに頻繁な書き込みの問題があるため、1時間に1000個のテーブルが作成またはスケジュールされている場合、etcdストレージをすべて使用し、 `etcdserver: mvcc: database space exceeded`のエラーを返します。 。このエラーが発生した後、etcdストレージをクリーンアップする必要があります。詳細については、 [etcdmaintainceスペースクォータ](https://etcd.io/docs/v3.4.0/op-guide/maintenance/#space-quota)を参照してください。クラスタをv4.0.9以降のバージョンにアップグレードすることをお勧めします。

## TiCDCは大規模なトランザクションの複製をサポートしていますか？リスクはありますか？ {#does-ticdc-support-replicating-large-transactions-is-there-any-risk}

TiCDCは、大規模なトランザクション（5 GBを超えるサイズ）を部分的にサポートします。さまざまなシナリオに応じて、次のリスクが存在する可能性があります。

-   TiCDCの内部処理能力が不十分な場合、レプリケーションタスクエラー`ErrBufferReachLimit`が発生する可能性があります。
-   TiCDCの内部処理能力が不十分な場合、またはTiCDCのダウンストリームのスループット能力が不十分な場合、メモリ不足（OOM）が発生する可能性があります。

上記のエラーが発生した場合は、BRを使用して大規模なトランザクションの増分データを復元することをお勧めします。詳細な操作は次のとおりです。

1.  大規模なトランザクションのために終了したチェンジフィードの`checkpoint-ts`を記録し、このTSOをBR増分バックアップの`--lastbackupts`として使用して、 [増分データバックアップ](/br/use-br-command-line-tool.md#back-up-incremental-data)を実行します。
2.  インクリメンタルデータをバックアップした後、BRログ出力に`["Full backup Failed summary : total backup ranges: 0, total success: 0, total failed: 0"] [BackupTS=421758868510212097]`に類似したログレコードを見つけることができます。このログに`BackupTS`を記録します。
3.  [インクリメンタルデータを復元する](/br/use-br-command-line-tool.md#restore-incremental-data) 。
4.  新しいチェンジフィードを作成し、 `BackupTS`からレプリケーションタスクを開始します。
5.  古いチェンジフィードを削除します。

## チェンジフィードのダウンストリームがMySQLと同様のデータベースであり、TiCDCが時間のかかるDDLステートメントを実行する場合、他のすべてのチェンジフィードはブロックされます。問題をどのように処理する必要がありますか？ {#when-the-downstream-of-a-changefeed-is-a-database-similar-to-mysql-and-ticdc-executes-a-time-consuming-ddl-statement-all-other-changefeeds-are-blocked-how-should-i-handle-the-issue}

1.  時間のかかるDDLステートメントを含むチェンジフィードの実行を一時停止します。次に、他のチェンジフィードがブロックされなくなったことがわかります。
2.  TiCDCログで`apply job`のフィールドを検索し、時間のかかるDDLステートメントの`start-ts`を確認します。
3.  ダウンストリームでDDLステートメントを手動で実行します。実行終了後、以下の操作を行ってください。
4.  チェンジフィード構成を変更し、上記の`start-ts`を`ignore-txn-start-ts`構成項目に追加します。
5.  一時停止したチェンジフィードを再開します。

## TiCDCクラスタをv4.0.8にアップグレードした後、チェンジフィードを実行すると、 <code>[CDC:ErrKafkaInvalidConfig]Canal requires old value to be enabled</code>ますエラーが報告されます {#after-i-upgrade-the-ticdc-cluster-to-v4-0-8-the-code-cdc-errkafkainvalidconfig-canal-requires-old-value-to-be-enabled-code-error-is-reported-when-i-execute-a-changefeed}

v4.0.8以降、チェンジフィードの出力に`canal-json` 、または`canal`プロトコルが使用されている場合、 `maxwell`は古い値の機能を自動的に有効にします。ただし、TiCDCを以前のバージョンから`maxwell` `canal-json` `canal`使用し、古い値の機能が無効になっていると、このエラーが報告されます。

エラーを修正するには、次の手順を実行します。

1.  チェンジフィード構成ファイルの値`enable-old-value`を`true`に設定します。

2.  `cdc cli changefeed pause`を実行して、レプリケーションタスクを一時停止します。

    {{< copyable "" >}}

    ```shell
    cdc cli changefeed pause -c test-cf --pd=http://10.0.10.25:2379
    ```

3.  `cdc cli changefeed update`を実行して、元のチェンジフィード構成を更新します。

    {{< copyable "" >}}

    ```shell
    cdc cli changefeed update -c test-cf --pd=http://10.0.10.25:2379 --sink-uri="mysql://127.0.0.1:3306/?max-txn-row=20&worker-number=8" --config=changefeed.toml
    ```

4.  `cdc cli changfeed resume`を実行して、レプリケーションタスクを再開します。

    {{< copyable "" >}}

    ```shell
    cdc cli changefeed resume -c test-cf --pd=http://10.0.10.25:2379
    ```

## <code>[tikv:9006]GC life time is shorter than transaction duration, transaction starts at xx, GC safe point is yy</code>です。TiCDCを使用してチェンジフィードを作成すると、エラーが報告されます。 {#the-code-tikv-9006-gc-life-time-is-shorter-than-transaction-duration-transaction-starts-at-xx-gc-safe-point-is-yy-code-error-is-reported-when-i-use-ticdc-to-create-a-changefeed}

解決策： `pd-ctl service-gc-safepoint --pd <pd-addrs>`コマンドを実行して、現在のGCセーフポイントとサービスGCセーフポイントを照会する必要があります。 GCセーフポイントがTiCDCレプリケーションタスクの`start-ts` （チェンジフィード）よりも小さい場合は、 `cdc cli create changefeed`コマンドに`--disable-gc-check`オプションを直接追加して、チェンジフィードを作成できます。

`pd-ctl service-gc-safepoint --pd <pd-addrs>`の結果に`gc_worker service_id`がない場合：

-   PDのバージョンがv4.0.8以前の場合、詳細については[PDの問題＃3128](https://github.com/tikv/pd/issues/3128)を参照してください。
-   PDがv4.0.8以前のバージョンから新しいバージョンにアップグレードされた場合、詳細については[PDの問題＃3366](https://github.com/tikv/pd/issues/3366)を参照してください。

## TiCDCレプリケーションタスクを作成すると、 <code>enable-old-value</code>が<code>true</code>に設定されますが、アップストリームからの<code>INSERT</code> / <code>UPDATE</code>ステートメントは、ダウンストリームにレプリケートされた後、 <code>REPLACE INTO</code>になります。 {#code-enable-old-value-code-is-set-to-code-true-code-when-i-create-a-ticdc-replication-task-but-code-insert-code-code-update-code-statements-from-the-upstream-become-code-replace-into-code-after-being-replicated-to-the-downstream}

TiCDCでチェンジフィードが作成されると、 `safe-mode`の設定はデフォルトで`true`になり、アップストリームの`INSERT`ステートメントに対して実行する`REPLACE INTO`ステートメントが生成され`UPDATE` 。

現在、ユーザーは`safe-mode`の設定を変更できないため、この問題は現在解決策がありません。

## TiCDCを使用してメッセージをKafkaに複製すると、Kafkaは<code>Message was too large</code>というエラーを返します {#when-i-use-ticdc-to-replicate-messages-to-kafka-kafka-returns-the-code-message-was-too-large-code-error}

TiCDC v4.0.8以前のバージョンでは、シンクURIでKafkaの`max-message-bytes`設定を構成するだけでは、Kafkaに出力されるメッセージのサイズを効果的に制御することはできません。メッセージサイズを制御するには、Kafkaが受信するメッセージのバイト数の制限も増やす必要があります。このような制限を追加するには、Kafkaサーバー構成に次の構成を追加します。

```
# The maximum byte number of a message that the broker receives
message.max.bytes=2147483648
# The maximum byte number of a message that the broker copies
replica.fetch.max.bytes=2147483648
# The maximum message byte number that the consumer side reads
fetch.message.max.bytes=2147483648
```

## TiCDCレプリケーション中にDDLステートメントがダウンストリームで実行されないかどうかを確認するにはどうすればよいですか？レプリケーションを再開するにはどうすればよいですか？ {#how-can-i-find-out-whether-a-ddl-statement-fails-to-execute-in-downstream-during-ticdc-replication-how-to-resume-the-replication}

DDLステートメントの実行に失敗すると、レプリケーションタスク（changefeed）は自動的に停止します。 checkpoint-tsは、DDLステートメントのfinish-tsから1を引いたものです。 TiCDCがダウンストリームでこのステートメントの実行を再試行する場合は、 `cdc cli changefeed resume`を使用してレプリケーションタスクを再開します。例えば：

{{< copyable "" >}}

```shell
cdc cli changefeed resume -c test-cf --pd=http://10.0.10.25:2379
```

失敗するこのDDLステートメントをスキップする場合は、changefeedのstart-tsをcheckpoint-ts（DDLステートメントが失敗するタイムスタンプ）に1を加えた値に設定します。たとえば、DDLステートメントが失敗するチェックポイント-tsが`415241823337054209`の場合、次のコマンドを実行して、このDDLステートメントをスキップします。

{{< copyable "" >}}

```shell
cdc cli changefeed update -c test-cf --pd=http://10.0.10.25:2379 --start-ts 415241823337054210
cdc cli changefeed resume -c test-cf --pd=http://10.0.10.25:2379
```

## DDLステートメントをダウンストリームのMySQL5.7に複製する場合、時間タイプフィールドのデフォルト値に一貫性がありません。私に何ができる？ {#the-default-value-of-the-time-type-field-is-inconsistent-when-replicating-a-ddl-statement-to-the-downstream-mysql-5-7-what-can-i-do}

`create table test (id int primary key, ts timestamp)`ステートメントがアップストリームTiDBで実行されると仮定します。 TiCDCがこのステートメントをダウンストリームのMySQL5.7に複製する場合、MySQLはデフォルト構成を使用します。レプリケーション後のテーブルスキーマは次のとおりです。 `timestamp`フィールドのデフォルト値は`CURRENT_TIMESTAMP`になります：

{{< copyable "" >}}

```sql
mysql root@127.0.0.1:test> show create table test;
+-------+----------------------------------------------------------------------------------+
| Table | Create Table                                                                     |
+-------+----------------------------------------------------------------------------------+
| test  | CREATE TABLE `test` (                                                            |
|       |   `id` int(11) NOT NULL,                                                         |
|       |   `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, |
|       |   PRIMARY KEY (`id`)                                                             |
|       | ) ENGINE=InnoDB DEFAULT CHARSET=latin1                                           |
+-------+----------------------------------------------------------------------------------+
1 row in set
```

結果から、レプリケーションの前後のテーブルスキーマに一貫性がないことがわかります。これは、TiDBのデフォルト値`explicit_defaults_for_timestamp`がMySQLのデフォルト値と異なるためです。詳細については、 [MySQLの互換性](/mysql-compatibility.md#default-differences)を参照してください。

v5.0.1またはv4.0.13以降、MySQLへのレプリケーションごとに、TiCDCは自動的に`explicit_defaults_for_timestamp = ON`を設定して、時間タイプがアップストリームとダウンストリームの間で一貫していることを確認します。 v5.0.1またはv4.0.13より前のバージョンでは、TiCDCを使用して時間タイプデータを複製するときに、一貫性のない`explicit_defaults_for_timestamp`値によって引き起こされる互換性の問題に注意してください。

## ダウンストリームのレプリケーションのシンクがTiDBまたはMySQLの場合、ダウンストリームデータベースのユーザーにはどのような権限が必要ですか？ {#when-the-sink-of-the-replication-downstream-is-tidb-or-mysql-what-permissions-do-users-of-the-downstream-database-need}

シンクがTiDBまたはMySQLの場合、ダウンストリームデータベースのユーザーには次の権限が必要です。

-   `Select`
-   `Index`
-   `Insert`
-   `Update`
-   `Delete`
-   `Create`
-   `Drop`
-   `Alter`
-   `Create View`

`recover table`をダウンストリームTiDBに複製する必要がある場合は、 `Super`の権限が必要です。
