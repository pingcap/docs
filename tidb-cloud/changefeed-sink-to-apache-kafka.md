---
title: Sink to Apache Kafka
Summary: Learn how to create a changefeed to stream data from TiDB Cloud to Apache Kafka.
---

# Apache Kafka にシンクする {#sink-to-apache-kafka}

このドキュメントでは、 TiDB Cloudから Apache Kafka にデータをストリーミングするために変更フィードを作成する方法について説明します。

> **ノート：**
>
> 現在、Kafka シンクは**ベータ版**です。 changefeed 機能を使用するには、TiDB クラスターのバージョンが v6.4.0 以降であり、TiKV ノードのサイズが少なくとも 8 vCPU および 16 GiB であることを確認してください。
>
> [Serverless Tierクラスター](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)の場合、changefeed 機能は使用できません。

## 制限 {#restrictions}

-   TiDB Cloudクラスターごとに、最大 5 つの変更フィードを作成できます。
-   現在、 TiDB Cloud は、Kafka ブローカーに接続するための自己署名 TLS 証明書のアップロードをサポートしていません。
-   TiDB Cloud はTiCDC を使用して変更フィードを確立するため、同じ[TiCDCとしての制限](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios)を持ちます。
-   レプリケートするテーブルに主キーまたは null 以外の一意のインデックスがない場合、レプリケーション中に一意の制約がないため、一部の再試行シナリオで重複データがダウンストリームに挿入される可能性があります。

## 前提条件 {#prerequisites}

データを Apache Kafka にストリーミングするための変更フィードを作成する前に、次の前提条件を満たす必要があります。

-   ネットワーク接続をセットアップする
-   Kafka ACL 承認のアクセス許可を追加する

### 通信網 {#network}

TiDB クラスターが Apache Kafka サービスに接続できることを確認してください。

インターネットにアクセスできない AWS VPC に Apache Kafka サービスがある場合は、次の手順を実行します。

1.  Apache Kafka サービスの VPC と TiDB クラスターの間の[VPC ピアリング接続を設定する](/tidb-cloud/set-up-vpc-peering-connections.md) 。

2.  Apache Kafka サービスが関連付けられているセキュリティ グループの受信規則を変更します。

    TiDB Cloudクラスターが配置されているリージョンの CIDR をインバウンド規則に追加する必要があります。 CIDR は**VPC Peering**ページにあります。そうすることで、トラフィックが TiDB クラスターから Kafka ブローカーに流れるようになります。

3.  Apache Kafka URL にホスト名が含まれている場合、 TiDB Cloud がApache Kafka ブローカーの DNS ホスト名を解決できるようにする必要があります。

    1.  [VPC ピアリング接続の DNS 解決を有効にする](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html#vpc-peering-dns)の手順に従います。
    2.  **Accepter DNS 解決**オプションを有効にします。

インターネットにアクセスできない GCP VPC に Apache Kafka サービスがある場合は、次の手順を実行します。

1.  Apache Kafka サービスの VPC と TiDB クラスターの間の[VPC ピアリング接続を設定する](/tidb-cloud/set-up-vpc-peering-connections.md) 。
2.  Apache Kafka が配置されている VPC のイングレス ファイアウォール ルールを変更します。

    TiDB Cloudクラスターが配置されているリージョンの CIDR をイングレス ファイアウォール ルールに追加する必要があります。 CIDR は**VPC Peering**ページにあります。そうすることで、トラフィックが TiDB クラスターから Kafka ブローカーに流れるようになります。

### Kafka ACL 承認 {#kafka-acl-authorization}

TiDB Cloud changefeeds がデータを Apache Kafka にストリーミングし、Kafka トピックを自動的に作成できるようにするには、次の権限が Kafka に追加されていることを確認してください。

-   Kafka のトピック リソース タイプに`Create`と`Write`アクセス許可が追加されました。
-   Kafka のクラスター リソース タイプに`DescribeConfigs`パーミッションが追加されました。

たとえば、Kafka クラスターが Confluent Cloud にある場合、詳細については Confluent ドキュメントの[資力](https://docs.confluent.io/platform/current/kafka/authorization.html#resources)と[ACL の追加](https://docs.confluent.io/platform/current/kafka/authorization.html#adding-acls)を参照してください。

## ステップ 1. Apache Kafka の changefeed ページを開く {#step-1-open-the-changefeed-page-for-apache-kafka}

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、ターゲット TiDB クラスターのクラスター概要ページに移動し、左側のナビゲーション ペインで**[Changefeed]**をクリックします。
2.  **Create Changefeed を**クリックし、 <strong>Kafka を</strong><strong>Target Type</strong>として選択します。

## ステップ 2. changefeed ターゲットを構成する {#step-2-configure-the-changefeed-target}

1.  **Brokers コンフィグレーション**の下で、Kafka ブローカーのエンドポイントを入力します。コンマ`,`使用して、複数のエンドポイントを区切ることができます。

2.  Kafka のバージョンを選択します。それがわからない場合は、Kafka V2 を使用してください。

3.  この変更フィードのデータに必要な圧縮タイプを選択します。

4.  Kafka で**TLS 暗号化が**有効になっており、Kafka 接続に TLS 暗号化を使用する場合は、TLS 暗号化オプションを有効にします。

5.  Kafka 認証構成に従って、**認証**オプションを選択します。

    -   Kafka が認証を必要としない場合は、デフォルトのオプション**DISABLE の**ままにしてください。
    -   Kafka で認証が必要な場合は、対応する認証タイプを選択し、認証のために Kafka アカウントのユーザー名とパスワードを入力します。

6.  **[次へ]**をクリックして、設定した構成を確認し、次のページに進みます。

## ステップ 3. changefeed を設定する {#step-3-set-the-changefeed}

1.  **テーブル フィルタを**カスタマイズして、複製するテーブルをフィルタリングします。ルールの構文については、 [テーブル フィルター規則](/table-filter.md)を参照してください。

    -   **フィルター ルールの追加**: この列でフィルター ルールを設定できます。デフォルトでは、すべてのテーブルをレプリケートすることを表すルール`*.*`があります。新しいルールを追加すると、 TiDB Cloud はTiDB 内のすべてのテーブルに対してクエリを実行し、<strong>複製されるテーブル列</strong>のルールに一致するテーブルのみを表示します。
    -   **レプリケートされるテーブル**: この列は、レプリケートされるテーブルを示します。ただし、将来レプリケートされる新しいテーブルや、完全にレプリケートされるスキーマは表示されません。
    -   **有効なキーのないテーブル**: この列には、一意キーと主キーのないテーブルが表示されます。これらのテーブルでは、重複イベントを処理するためにダウンストリーム システムで一意の識別子を使用できないため、レプリケーション中にデータの一貫性が失われる可能性があります。このような問題を回避するには、レプリケーションの前にこれらのテーブルに一意のキーまたは主キーを追加するか、これらのテーブルを除外するフィルター ルールを設定することをお勧めします。たとえば、「!test.tbl1」を使用してテーブル`test.tbl1`を除外できます。

2.  **[データ形式]**領域で、目的の Kafka メッセージの形式を選択します。

    -   Avro は、豊富なデータ構造を備えたコンパクトで高速なバイナリ データ形式であり、さまざまなフロー システムで広く使用されています。詳細については、 [Avro データ形式](https://docs.pingcap.com/tidb/stable/ticdc-avro-protocol)を参照してください。
    -   Canal-JSON はプレーンな JSON テキスト形式で、解析が簡単です。詳細については、 [Canal-JSON データ形式](https://docs.pingcap.com/tidb/stable/ticdc-canal-json)を参照してください。

3.  Kafka メッセージ本文に**TiDB 拡張フィールドを追加する場合は、TiDB 拡張**オプションを有効にします。

    TiDB 拡張フィールドの詳細については、 [Avro データ形式の TiDB 拡張フィールド](https://docs.pingcap.com/tidb/stable/ticdc-avro-protocol#tidb-extension-fields)および[Canal-JSON データ形式の TiDB 拡張フィールド](https://docs.pingcap.com/tidb/stable/ticdc-canal-json#tidb-extension-field)を参照してください。

4.  **Avro を**データ形式として選択すると、Avro 固有の設定がページに表示されます。これらの構成は次のように入力できます。

    -   **Decimal**および<strong>Unsigned BigInt</strong>構成で、 TiDB Cloud がKafka メッセージの decimal および unsigned bigint データ型を処理する方法を指定します。
    -   **[スキーマ レジストリ]**領域で、スキーマ レジストリ エンドポイントを入力します。 <strong>HTTP 認証を</strong>有効にすると、ユーザー名とパスワードのフィールドが表示され、TiDB クラスターのエンドポイントとパスワードが自動的に入力されます。

5.  **[トピックの配布]**領域で、配布モードを選択し、モードに従ってトピック名の構成を入力します。

    データ形式として**Avro**を選択した場合は、[<strong>配布モード]</strong>ドロップダウン リストで<strong>[テーブルごとに変更ログを Kafka トピックに配布する]</strong>モードのみを選択できます。

    配布モードは、changefeed が Kafka トピックをテーブルごと、データベースごとに作成する方法、またはすべての変更ログに対して 1 つのトピックを作成する方法を制御します。

    -   **テーブルごとに変更ログを Kafka トピックに配布する**

        変更フィードでテーブルごとに専用の Kafka トピックを作成する場合は、このモードを選択します。次に、テーブルのすべての Kafka メッセージが専用の Kafka トピックに送信されます。トピックのプレフィックス、データベース名とテーブル名の間の区切り文字、およびサフィックスを設定することで、テーブルのトピック名をカスタマイズできます。たとえば、セパレータを`_`に設定すると、トピック名は`<Prefix><DatabaseName>_<TableName><Suffix>`の形式になります。

        スキーマ イベントの作成など、行以外のイベントの変更ログの場合、 **[デフォルトのトピック名]**フィールドにトピック名を指定できます。 changefeed は、そのような変更ログを収集するために、それに応じてトピックを作成します。

    -   **データベースごとに変更ログを Kafka トピックに配布する**

        変更フィードでデータベースごとに専用の Kafka トピックを作成する場合は、このモードを選択します。次に、データベースのすべての Kafka メッセージが専用の Kafka トピックに送信されます。トピックのプレフィックスとサフィックスを設定して、データベースのトピック名をカスタマイズできます。

        Resolved Ts Event などの行以外のイベントの変更ログの場合、 **[デフォルトのトピック名]**フィールドにトピック名を指定できます。 changefeed は、そのような変更ログを収集するために、それに応じてトピックを作成します。

    -   **指定された 1 つの Kafka トピックにすべての変更ログを送信します**

        変更フィードですべての変更ログに対して 1 つの Kafka トピックを作成する場合は、このモードを選択します。次に、変更フィード内のすべての Kafka メッセージが 1 つの Kafka トピックに送信されます。 **[トピック名]**フィールドでトピック名を定義できます。

6.  **[パーティション配布]**領域で、Kafka メッセージが送信されるパーティションを決定できます。

    -   **インデックス値ごとに変更ログを Kafka パーティションに配布する**

        変更フィードでテーブルの Kafka メッセージを別のパーティションに送信する場合は、この分散方法を選択します。行変更ログのインデックス値によって、変更ログが送信されるパーティションが決まります。この分散方法により、パーティションのバランスが改善され、行レベルの順序が確保されます。

    -   **テーブルごとに変更ログを Kafka パーティションに配布する**

        変更フィードでテーブルの Kafka メッセージを 1 つの Kafka パーティションに送信する場合は、この分散方法を選択します。行変更ログのテーブル名によって、変更ログが送信されるパーティションが決まります。この分散方法では、テーブルの順序が確保されますが、不均衡なパーティションが発生する可能性があります。

7.  **[トピックのコンフィグレーション]**領域で、次の番号を構成します。 changefeed は、番号に従って Kafka トピックを自動的に作成します。

    -   **Replication Factor** : 各 Kafka メッセージが複製される Kafka サーバーの数を制御します。
    -   **パーティション番号**: トピックに存在するパーティションの数を制御します。

8.  **[次へ]**をクリックします。

## ステップ 4. changefeed 仕様を構成する {#step-4-configure-your-changefeed-specification}

1.  **[Changefeed 仕様]**領域で、changefeed が使用するレプリケーション キャパシティ ユニット (RCU) の数を指定します。
2.  **[変更フィード名]**領域で、変更フィードの名前を指定します。
3.  **[次へ]**をクリックして、設定した構成を確認し、次のページに進みます。

## ステップ 5.構成を確認する {#step-5-review-the-configurations}

このページでは、設定したすべての変更フィード構成を確認できます。

エラーが見つかった場合は、戻ってエラーを修正できます。エラーがない場合は、下部にあるチェック ボックスをクリックし、 **[作成]**をクリックして変更フィードを作成できます。
