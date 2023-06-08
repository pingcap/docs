---
title: Sink to Apache Kafka (Beta)
Summary: Learn how to create a changefeed to stream data from TiDB Cloud to Apache Kafka.
---

# Apache Kafka にシンク (ベータ) {#sink-to-apache-kafka-beta}

このドキュメントでは、 TiDB Cloudから Apache Kafka にデータをストリーミングするためのチェンジフィードを作成する方法について説明します。

> **ノート：**
>
> 現在、Kafka シンクは**ベータ版**です。チェンジフィード機能を使用するには、TiDB クラスターのバージョンが v6.4.0 以降であり、TiKV ノードのサイズが少なくとも 8 vCPU および 16 GiB であることを確認してください。
>
> [<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta">TiDB Serverlessクラスタ</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta)の場合、チェンジフィード機能は使用できません。

## 制限 {#restrictions}

-   TiDB Cloudクラスターごとに、最大 5 つの変更フィードを作成できます。
-   現在、 TiDB Cloud は、Kafka ブローカーに接続するための自己署名 TLS 証明書のアップロードをサポートしていません。
-   TiDB Cloud はTiCDC を使用して変更フィードを確立するため、同じ[<a href="https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios">TiCDC としての制限</a>](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios)を持ちます。
-   レプリケートされるテーブルに主キーまたは NULL 以外の一意のインデックスがない場合、レプリケーション中に一意制約がないため、一部の再試行シナリオでは重複したデータがダウンストリームに挿入される可能性があります。

## 前提条件 {#prerequisites}

データを Apache Kafka にストリーミングするための変更フィードを作成する前に、次の前提条件を満たしている必要があります。

-   ネットワーク接続をセットアップする
-   Kafka ACL 認可のためのアクセス許可を追加する

### 通信網 {#network}

TiDB クラスターが Apache Kafka サービスに接続できることを確認してください。

Apache Kafka サービスがインターネットにアクセスできない AWS VPC にある場合は、次の手順を実行します。

1.  Apache Kafka サービスの VPC と TiDB クラスターの間の[<a href="/tidb-cloud/set-up-vpc-peering-connections.md">VPC ピアリング接続をセットアップする</a>](/tidb-cloud/set-up-vpc-peering-connections.md) 。

2.  Apache Kafka サービスが関連付けられているセキュリティ グループの受信ルールを変更します。

    TiDB Cloudクラスターが配置されているリージョンの CIDR を受信ルールに追加する必要があります。 CIDR は、 **「VPC ピアリング」**ページにあります。これにより、TiDB クラスターから Kafka ブローカーにトラフィックが流れるようになります。

3.  Apache Kafka URL にホスト名が含まれている場合は、 TiDB Cloud がApache Kafka ブローカーの DNS ホスト名を解決できるようにする必要があります。

    1.  [<a href="https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html#vpc-peering-dns">VPC ピアリング接続の DNS 解決を有効にする</a>](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html#vpc-peering-dns)の手順に従います。
    2.  **アクセプター DNS 解決**オプションを有効にします。

Apache Kafka サービスがインターネットにアクセスできない GCP VPC にある場合は、次の手順を実行します。

1.  Apache Kafka サービスの VPC と TiDB クラスターの間の[<a href="/tidb-cloud/set-up-vpc-peering-connections.md">VPC ピアリング接続をセットアップする</a>](/tidb-cloud/set-up-vpc-peering-connections.md) 。
2.  Apache Kafka が配置されている VPC のイングレス ファイアウォール ルールを変更します。

    TiDB Cloudクラスターが配置されているリージョンの CIDR をイングレス ファイアウォール ルールに追加する必要があります。 CIDR は、 **「VPC ピアリング」**ページにあります。これにより、TiDB クラスターから Kafka ブローカーにトラフィックが流れるようになります。

### Kafka ACL 認可 {#kafka-acl-authorization}

TiDB Cloud変更フィードがデータを Apache Kafka にストリーミングし、Kafka トピックを自動的に作成できるようにするには、次の権限が Kafka に追加されていることを確認します。

-   Kafka のトピック リソース タイプに`Create`および`Write`権限が追加されます。
-   Kafka のクラスター リソース タイプに`DescribeConfigs`権限が追加されます。

たとえば、Kafka クラスターが Confluent Cloud にある場合、詳細については Confluent ドキュメントの[<a href="https://docs.confluent.io/platform/current/kafka/authorization.html#resources">資力</a>](https://docs.confluent.io/platform/current/kafka/authorization.html#resources)と[<a href="https://docs.confluent.io/platform/current/kafka/authorization.html#adding-acls">ACLの追加</a>](https://docs.confluent.io/platform/current/kafka/authorization.html#adding-acls)を参照してください。

## ステップ 1. Apache Kafka のチェンジフィード ページを開く {#step-1-open-the-changefeed-page-for-apache-kafka}

1.  [<a href="https://tidbcloud.com">TiDB Cloudコンソール</a>](https://tidbcloud.com)では、ターゲット TiDB クラスターのクラスター概要ページに移動し、左側のナビゲーション ペインで**[Changefeed]**をクリックします。
2.  **[変更フィードの作成]**をクリックし、**ターゲット タイプ**として**Kafka**を選択します。

## ステップ 2. チェンジフィードターゲットを構成する {#step-2-configure-the-changefeed-target}

1.  **[ブローカーのコンフィグレーション]**で、Kafka ブローカー エンドポイントを入力します。カンマ`,`使用して複数のエンドポイントを区切ることができます。

2.  Kafka のバージョンを選択します。それがわからない場合は、Kafka V2 を使用してください。

3.  この変更フィード内のデータに必要な圧縮タイプを選択します。

4.  Kafka で**TLS 暗号化が**有効になっており、Kafka 接続に TLS 暗号化を使用する場合は、TLS 暗号化オプションを有効にします。

5.  Kafka 認証構成に従って**認証**オプションを選択します。

    -   Kafka が認証を必要としない場合は、デフォルトのオプション**DISABLE の**ままにしてください。
    -   Kafka で認証が必要な場合は、対応する認証タイプを選択し、認証用の Kafka アカウントのユーザー名とパスワードを入力します。

6.  **「次へ」**をクリックして設定した構成を確認し、次のページに進みます。

## ステップ 3. チェンジフィードを設定する {#step-3-set-the-changefeed}

1.  **テーブル フィルターを**カスタマイズして、複製するテーブルをフィルターします。ルールの構文については、 [<a href="/table-filter.md">テーブルフィルタールール</a>](/table-filter.md)を参照してください。

    -   **フィルター ルールの追加**: この列でフィルター ルールを設定できます。デフォルトでは、すべてのテーブルを複製することを表すルール`*.*`があります。新しいルールを追加すると、 TiDB CloudはTiDB 内のすべてのテーブルをクエリし、ルールに一致するテーブルのみを**[複製する**テーブル] 列に表示します。
    -   **複製されるテーブル**: この列には、複製されるテーブルが表示されます。ただし、今後複製される新しいテーブルや完全に複製されるスキーマは表示されません。
    -   **有効なキーのないテーブル**: この列には、一意キーと主キーのないテーブルが表示されます。これらのテーブルでは、ダウンストリーム システムが重複イベントを処理するために一意の識別子を使用できないため、レプリケーション中にデータが不整合になる可能性があります。このような問題を回避するには、レプリケーションの前にこれらのテーブルに一意キーまたは主キーを追加するか、これらのテーブルをフィルターで除外するフィルター ルールを設定することをお勧めします。たとえば、「!test.tbl1」を使用してテーブル`test.tbl1`を除外できます。

2.  **「データ形式」**領域で、Kafka メッセージの希望の形式を選択します。

    -   Avro は、豊富なデータ構造を備えたコンパクトで高速なバイナリ データ形式で、さまざまなフロー システムで広く使用されています。詳細については、 [<a href="https://docs.pingcap.com/tidb/stable/ticdc-avro-protocol">Avro データ形式</a>](https://docs.pingcap.com/tidb/stable/ticdc-avro-protocol)を参照してください。
    -   Canal-JSON はプレーンな JSON テキスト形式であり、解析が簡単です。詳細については、 [<a href="https://docs.pingcap.com/tidb/stable/ticdc-canal-json">Canal-JSON データ形式</a>](https://docs.pingcap.com/tidb/stable/ticdc-canal-json)を参照してください。

3.  **TiDB 拡張フィールドを Kafka メッセージ本文に追加する場合は、TiDB 拡張**オプションを有効にします。

    TiDB 拡張フィールドの詳細については、 [<a href="https://docs.pingcap.com/tidb/stable/ticdc-avro-protocol#tidb-extension-fields">Avro データ形式の TiDB 拡張フィールド</a>](https://docs.pingcap.com/tidb/stable/ticdc-avro-protocol#tidb-extension-fields)および[<a href="https://docs.pingcap.com/tidb/stable/ticdc-canal-json#tidb-extension-field">Canal-JSON データ形式の TiDB 拡張フィールド</a>](https://docs.pingcap.com/tidb/stable/ticdc-canal-json#tidb-extension-field)を参照してください。

4.  データ形式として**Avro**を選択すると、ページに Avro 固有の構成がいくつか表示されます。これらの構成は次のように入力できます。

    -   **Decimal**および**Unsigned BigInt**構成では、 TiDB Cloud がKafka メッセージ内の 10 進数および符号なし bigint データ型を処理する方法を指定します。
    -   **[スキーマ レジストリ]**領域で、スキーマ レジストリ エンドポイントを入力します。 **HTTP 認証 を**有効にすると、ユーザー名とパスワードのフィールドが表示され、TiDB クラスターのエンドポイントとパスワードが自動的に入力されます。

5.  **[トピックの配布]**領域で、配布モードを選択し、モードに従ってトピック名の設定を入力します。

    データ形式として**Avro**を選択した場合は、[**配布モード]**ドロップダウン リストで**[変更ログをテーブルごとに Kafka トピックに**配布] モードのみを選択できます。

    分散モードは、テーブルごと、データベースごと、またはすべての変更ログに対して 1 つのトピックを作成するなど、変更フィードが Kafka トピックを作成する方法を制御します。

    -   **変更ログをテーブルごとに Kafka トピックに配布する**

        チェンジフィードでテーブルごとに専用の Kafka トピックを作成する場合は、このモードを選択します。次に、テーブルのすべての Kafka メッセージが専用の Kafka トピックに送信されます。テーブルのトピック名をカスタマイズするには、トピックのプレフィックス、データベース名とテーブル名の間の区切り文字、およびサフィックスを設定します。たとえば、区切り文字を`_`に設定すると、トピック名の形式は`<Prefix><DatabaseName>_<TableName><Suffix>`になります。

        「スキーマ作成イベント」などの行以外のイベントの変更ログの場合、 **「デフォルトのトピック名」**フィールドにトピック名を指定できます。変更フィードは、そのような変更ログを収集するために、それに応じてトピックを作成します。

    -   **データベースごとに変更ログを Kafka に配布する**

        チェンジフィードでデータベースごとに専用の Kafka トピックを作成する場合は、このモードを選択します。次に、データベースのすべての Kafka メッセージが専用の Kafka トピックに送信されます。トピックのプレフィックスとサフィックスを設定することで、データベースのトピック名をカスタマイズできます。

        解決された Ts イベントなどの非行イベントの変更ログの場合、 **「デフォルトのトピック名」**フィールドにトピック名を指定できます。変更フィードは、そのような変更ログを収集するために、それに応じてトピックを作成します。

    -   **すべての変更ログを指定された 1 つの Kafka トピックに送信します**

        変更フィードですべての変更ログに対して 1 つの Kafka トピックを作成する場合は、このモードを選択します。その後、変更フィード内のすべての Kafka メッセージが 1 つの Kafka トピックに送信されます。 **「トピック名」**フィールドでトピック名を定義できます。

6.  **[パーティション配布]**領域では、Kafka メッセージがどのパーティションに送信されるかを決定できます。

    -   **インデックス値ごとに変更ログを Kafka パーティションに配布する**

        変更フィードでテーブルの Kafka メッセージを別のパーティションに送信する場合は、この分散方法を選択します。行変更ログのインデックス値によって、変更ログがどのパーティションに送信されるかが決まります。この分散方法により、パーティションのバランスが改善され、行レベルの順序性が保証されます。

    -   **変更ログをテーブルごとに Kafka パーティションに分散する**

        チェンジフィードでテーブルの Kafka メッセージを 1 つの Kafka パーティションに送信する場合は、この分散方法を選択します。行変更ログのテーブル名によって、変更ログがどのパーティションに送信されるかが決まります。この分散方法ではテーブルの順序性が保証されますが、パーティションの不均衡が発生する可能性があります。

7.  **[トピックコンフィグレーション]**エリアで、次の数値を設定します。チェンジフィードは、数値に従って Kafka トピックを自動的に作成します。

    -   **レプリケーション係数**: 各 Kafka メッセージがレプリケートされる Kafka サーバーの数を制御します。
    -   **パーティション番号**: トピック内に存在するパーティションの数を制御します。

8.  **「次へ」**をクリックします。

## ステップ 4. 変更フィード仕様を構成する {#step-4-configure-your-changefeed-specification}

1.  **「変更フィードの仕様」**領域で、変更フィードで使用するレプリケーション キャパシティ ユニット (RCU) の数を指定します。
2.  **「変更フィード名」**領域で、変更フィードの名前を指定します。
3.  **「次へ」**をクリックして設定した構成を確認し、次のページに進みます。

## ステップ 5. 構成を確認する {#step-5-review-the-configurations}

このページでは、設定したすべての変更フィード構成を確認できます。

エラーが見つかった場合は、戻ってエラーを修正できます。エラーがない場合は、下部のチェックボックスをクリックし、 **[作成]**をクリックして変更フィードを作成します。
