---
title: Kafka - Credentials（プレビュー）
summary: Kafka 接続情報を再利用できるように保存するための「Kafka - Credentials」データソースを作成します。これは Kafka Consumer 統合タスクで使用されます。
---

# Kafka - Credentials（プレビュー）

このページでは、`Kafka - Credentials` データソースを作成する方法について説明します。このデータソースには、Kafka クラスターへのアクセスに必要な broker アドレス、認証方式、および接続資格情報が保存されます。これらの設定は、複数の Kafka Consumer 統合タスクで再利用できます。

`Kafka - Credentials` は Kafka の接続情報のみを保存します。メッセージ自体を消費することはありません。Kafka トピックのメッセージを読み取り、内部オブジェクトストレージに書き込む実際の処理は、[Kafka Consumer Integration Task (Preview)](/tidb-cloud-lake/guides/integrate-with-kafka.md) によって実行されます。

## ユースケース {#use-cases}

- Kafka broker アドレスと認証設定を一元管理する
- 同じ Kafka 接続設定を複数の Kafka Consumer タスクで再利用する
- 複数のタスクから参照されている Kafka アドレス、認証方式、またはアカウント情報を 1 か所で更新する

## Kafka - Credentials を作成する {#create-kafka-credentials}

1. **Data** > **Data Sources** に移動し、**Create Data Source** をクリックします。
2. サービスタイプとして **Kafka - Credentials** を選択し、接続の詳細を入力します。

    | フィールド | 必須 | 説明 |
    |-------|----------|-------------|
    | **Name** | はい | データソースを識別するための説明的な名前 |
    | **Brokers** | はい | Kafka broker アドレスの一覧。複数のアドレスはカンマで区切ります。例: `broker-1:9092,broker-2:9093,broker-3:9092` |
    | **Authentication** | はい | Kafka の認証方式。サポートされるオプションは **None** と **SASL/PLAIN** です |
    | **TLS encryption** | いいえ | TLS 暗号化を有効にするかどうか |
    | **Username** | 該当する場合は必須 | Kafka のユーザー名。**SASL/PLAIN** を選択した場合に必須です |
    | **Password** | 該当する場合は必須 | Kafka のパスワード。**SASL/PLAIN** を選択した場合に必須です |

3. **Test Connectivity** をクリックして接続を検証します。テストが成功したら、**OK** をクリックしてデータソースを保存します。

## 設定に関する推奨事項 {#configuration-recommendations}

- アプリケーションアカウントを共有するのではなく、プラットフォーム専用の Kafka ユーザーを作成してください。
- Kafka クラスターで暗号化接続が必要な場合は、**TLS encryption** を有効にしてください。
- **SASL/PLAIN** を選択する場合は、Kafka ユーザーに、下流タスクで消費されるトピックを読み取る権限があることを確認してください。
- データソースを保存する前に **Test Connectivity** を実行し、broker アドレス、ネットワークアクセス、および認証設定を確認してください。

## 次のステップ {#next-steps}

データソースを作成した後、それを使用して [Kafka Consumer Integration Task (Preview)](/tidb-cloud-lake/guides/integrate-with-kafka.md) を作成できます。