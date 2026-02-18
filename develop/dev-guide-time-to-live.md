---
title: Periodically Delete Data Using TTL (Time to Live)
summary: TiDB の TTL 機能を使用して、期限切れのデータを自動的かつ定期的に削除する方法を学習します。
---

# TTL（Time to Live）を使用して定期的にデータを削除する {#periodically-delete-data-using-ttl-time-to-live}

アプリケーション開発において、一部のデータは限られた期間のみ価値を持ちます。例えば、認証コードは通常数分間しか保持する必要がなく、短縮リンクは特定のキャンペーン期間中のみ有効となる場合があり、アクセスログや中間計算結果も数か月しか保持されないことがよくあります。

TiDBは、TiDBデータの有効期間を行レベルで管理できる[TTL (存続時間)](/time-to-live.md)機能を提供します。TTLを使用すると、複雑なスケジュールされたクリーンアップスクリプトを作成することなく、期限切れのデータを**自動的かつ定期的に**削除できます。

## ユースケース {#use-cases}

TTLは、一定期間が経過するとデータがビジネス価値を失うシナリオ向けに設計されています。典型的なユースケースとしては、以下のようなものがあります。

-   認証コードと短縮URLの記録を定期的に削除する
-   古くなった過去の注文を定期的にクリーンアップする
-   中間計算結果を自動的に削除する

> **注記：**
>
> TTLジョブはバックグラウンドで定期的に実行されます。そのため、有効期限が切れたデータは、有効期限が切れた直後に削除されるとは限りません。

## クイックスタート {#quick-start}

TTL属性は、テーブルの作成時に設定することも、既存のテーブルに追加することもできます。以下のセクションでは、TTLを使用して期限切れのデータを定期的に削除する基本的な例を示します。詳細な例、使用上の制限、および他のツールや機能との互換性の詳細については、 [TTL (存続時間)](/time-to-live.md)参照してください。

### TTLでテーブルを作成する {#create-a-table-with-ttl}

インスタント メッセージを保存するための`app_messages`という名前のテーブルを作成し、作成後 3 か月後にメッセージを自動的に削除するには、次のステートメントを実行します。

```sql
CREATE TABLE app_messages (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    sender_id INT,
    msg_content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) TTL = `created_at` + INTERVAL 3 MONTH;
```

この例では、 `TTL = ...`有効期限ポリシーを定義します。3 `created_at`には各行の作成時刻が記録され、 `INTERVAL 3 MONTH`各行が最大 3 か月間保持されることを指定します。

### 既存のテーブルのTTL属性を構成する {#configure-the-ttl-attribute-for-an-existing-table}

すでに`app_logs`という名前のテーブルがあり、自動クリーンアップを有効にする場合 (たとえば、1 か月分のデータのみを保持する)、次のステートメントを実行します。

```sql
ALTER TABLE app_logs TTL = `created_at` + INTERVAL 1 MONTH;
```

### TTL期間を変更する {#modify-the-ttl-period}

`app_logs`テーブルの保持期間を変更するには、次のステートメントを実行します。

```sql
ALTER TABLE app_logs TTL = `created_at` + INTERVAL 6 MONTH;
```

### TTLを無効にする {#disable-ttl}

`app_logs`テーブルの TTL を無効にするには、次のステートメントを実行します。

```sql
ALTER TABLE app_logs TTL_ENABLE = 'OFF';
```

## 参照 {#see-also}

-   [TTL (存続時間)](/time-to-live.md)
