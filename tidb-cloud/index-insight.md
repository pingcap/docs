---
title: Index Insight (Beta)
summary: TiDB Cloudの Index Insight 機能を使用して、低速クエリのインデックス推奨事項を取得する方法を学習します。
---

# インデックスインサイト（ベータ版） {#index-insight-beta}

TiDB CloudのIndex Insight（ベータ版）機能は、インデックスを効果的に使用していない低速クエリに対してインデックスの推奨事項を提示することで、クエリパフォーマンスを最適化する強力な機能を提供します。このドキュメントでは、Index Insight機能を有効化し、効果的に活用するための手順を詳しく説明します。

> **注記：**
>
> Index Insight は現在ベータ版であり、 [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターでのみ使用できます。

## 導入 {#introduction}

Index Insight 機能には、次のような利点があります。

-   強化されたクエリ パフォーマンス: Index Insight は、遅いクエリを識別し、適切なインデックスを提案します。これにより、クエリの実行が高速化され、応答時間が短縮され、ユーザー エクスペリエンスが向上します。
-   コスト効率：Index Insight を使用してクエリパフォーマンスを最適化することで、追加のコンピューティングリソースの必要性が軽減され、既存のインフラストラクチャをより効率的に活用できるようになります。これにより、運用コストの削減につながる可能性があります。
-   簡素化された最適化プロセス：Index Insightは、インデックスの改善点の特定と実装を簡素化し、手作業による分析や推測作業の必要性を排除します。その結果、正確なインデックス推奨によって時間と労力を節約できます。
-   アプリケーション効率の向上: Index Insight を使用してデータベース パフォーマンスを最適化することで、 TiDB Cloudで実行されるアプリケーションはより大きなワークロードを処理し、より多くのユーザーに同時にサービスを提供できるようになり、アプリケーションのスケーリング操作がより効率的になります。

## 使用法 {#usage}

このセクションでは、Index Insight 機能を有効にして、低速クエリに推奨されるインデックスを取得する方法を紹介します。

### 始める前に {#before-you-begin}

Index Insight機能を有効にする前に、 TiDB Cloud Dedicatedクラスターを作成済みであることを確認してください。まだ作成していない場合は、 [TiDB Cloud専用クラスタを作成する](/tidb-cloud/create-tidb-cluster.md)の手順に従って作成してください。

### ステップ1: Index Insightを有効にする {#step-1-enable-index-insight}

1.  TiDB Cloud Dedicated クラスターの[**診断**](/tidb-cloud/tune-performance.md#view-the-diagnosis-page)ページに移動します。

2.  **「Index Insight BETA」**タブをクリックします。Index **Insightの概要**ページが表示されます。

3.  Index Insight機能を使用するには、専用のSQLユーザーを作成する必要があります。このユーザーは、機能のトリガーとインデックスの推奨事項の受信に使用されます。以下のSQL文は、必要な権限`information_schema`と`mysql`の読み取り権限、およびすべてのデータベースに対する`PROCESS`と`REFERENCES`権限）を持つ新しいSQLユーザーを作成します。9と`'random_password'` `'index_insight_user'`お客様の値に置き換えてください。

    ```sql
    CREATE user 'index_insight_user'@'%' IDENTIFIED by 'random_password';
    GRANT SELECT ON information_schema.* TO 'index_insight_user'@'%';
    GRANT SELECT ON mysql.* TO 'index_insight_user'@'%';
    GRANT PROCESS, REFERENCES ON *.* TO 'index_insight_user'@'%';
    FLUSH PRIVILEGES;
    ```

    > **注記：**
    >
    > TiDB Cloud Dedicated クラスターに接続するには、 [TiDB Cloud Dedicated クラスターに接続する](/tidb-cloud/connect-to-tidb-cluster.md)参照してください。

4.  前の手順で作成したSQLユーザーのユーザー名とパスワードを入力します。次に、 **「アクティブ化」**をクリックしてアクティベーションプロセスを開始します。

### ステップ2: Index Insightを手動で起動する {#step-2-manually-trigger-index-insight}

遅いクエリのインデックス推奨事項を取得するには、 **Index Insight 概要**ページの右上隅にある**[チェック アップ] を**クリックして、Index Insight 機能を手動でトリガーできます。

その後、この機能は過去3時間のスロークエリのスキャンを開始します。スキャンが完了すると、分析結果に基づいてインデックスの推奨事項のリストが表示されます。

### ステップ3: インデックスの推奨事項をビュー {#step-3-view-index-recommendations}

特定のインデックス推奨事項の詳細を表示するには、リストから該当するインサイトをクリックします。「**インデックスインサイトの詳細」**ページが表示されます。

このページでは、インデックスに関する推奨事項、関連するスロークエリ、実行プラン、関連指標を確認できます。これらの情報は、パフォーマンスの問題をより深く理解し、インデックスに関する推奨事項の実装による潜在的な影響を評価するのに役立ちます。

### ステップ4: インデックスの推奨事項を実装する {#step-4-implement-index-recommendations}

インデックスの推奨事項を実装する前に、まず**Index Insight の詳細**ページから推奨事項を確認して評価する必要があります。

インデックスの推奨事項を実装するには、次の手順に従います。

1.  提案されたインデックスが既存のクエリとワークロードに与える影響を評価します。
2.  インデックス実装に関連するstorage要件と潜在的なトレードオフを考慮してください。
3.  適切なデータベース管理ツールを使用して、関連するテーブルにインデックス推奨事項を作成します。
4.  インデックスを実装した後のパフォーマンスを監視して、改善を評価します。

## ベストプラクティス {#best-practices}

このセクションでは、Index Insight 機能の使用に関するベスト プラクティスをいくつか紹介します。

### インデックスインサイトを定期的に起動する {#regularly-trigger-index-insight}

最適化されたインデックスを維持するには、毎日など定期的に、またはクエリやデータベース スキーマに大幅な変更が発生したときに Index Insight 機能をトリガーすることをお勧めします。

### インデックスを実装する前に影響を分析する {#analyze-impact-before-implementing-indexes}

インデックスの推奨事項を実装する前に、クエリ実行プラン、ディスク容量、および関連するトレードオフへの潜在的な影響を分析してください。パフォーマンスの大幅な向上が見込めるインデックスを優先的に実装してください。

### パフォーマンスを監視する {#monitor-performance}

インデックスの推奨事項を実装した後は、クエリのパフォーマンスを定期的に監視してください。これにより、改善効果を確認し、必要に応じてさらに調整を行うことができます。

## FAQ {#faq}

このセクションでは、Index Insight 機能に関するよくある質問をいくつか紹介します。

### Index Insight を非アクティブ化するにはどうすればよいですか? {#how-to-deactivate-index-insight}

Index Insight 機能を無効にするには、次の手順を実行します。

1.  **Index Insightの概要**ページの右上隅にある**「設定」**をクリックします。Index **Insightの設定**ページが表示されます。
2.  **「非アクティブ化」**をクリックします。確認ダイアログボックスが表示されます。
3.  **「OK」**をクリックして非アクティブ化を確認します。

    Index Insight機能を無効化すると、 **Index Insightの概要**ページからすべてのインデックス推奨事項が削除されます。ただし、この機能用に作成されたSQLユーザーは削除されません。SQLユーザーは手動で削除できます。

### Index Insight を非アクティブ化した後、SQL ユーザーを削除するにはどうすればよいでしょうか? {#how-to-delete-the-sql-user-after-deactivating-index-insight}

Index Insight機能を無効化した後、 `DROP USER`ステートメントを実行して、この機能用に作成されたSQLユーザーを削除できます。以下は例です。3 `'username'`実際の値に置き換えてください。

```sql
DROP USER 'username';
```

### アクティベーションまたはチェックアップ中に<code>invalid user or password</code>メッセージが表示されるのはなぜですか? {#why-does-the-code-invalid-user-or-password-code-message-show-up-during-activation-or-check-up}

`invalid user or password`メッセージは通常、システムが入力した資格情報を認証できない場合に表示されます。この問題は、ユーザー名またはパスワードが正しくない、ユーザーアカウントの有効期限が切れている、またはロックされているなど、さまざまな理由で発生する可能性があります。

この問題を解決するには、次の手順を実行します。

1.  認証情報を確認してください：入力したユーザー名とパスワードが正しいことを確認してください。大文字と小文字の区別にご注意ください。
2.  アカウントのステータスを確認：ユーザーアカウントがアクティブであり、期限切れやロックされていないことを確認してください。システム管理者または関連サポートチャネルに問い合わせることで確認できます。
3.  新しいSQLユーザーを作成します。上記の手順で問題が解決しない場合は、以下のステートメントを使用して新しいSQLユーザーを作成できます。1と`'index_insight_user'` `'random_password'`実際の値に置き換えてください。

    ```sql
    CREATE user 'index_insight_user'@'%' IDENTIFIED by 'random_password';
    GRANT SELECT ON information_schema.* TO 'index_insight_user'@'%';
    GRANT SELECT ON mysql.* TO 'index_insight_user'@'%';
    GRANT PROCESS, REFERENCES ON *.* TO 'index_insight_user'@'%';
    FLUSH PRIVILEGES;
    ```

上記の手順を実行しても問題が解決しない場合は、 [PingCAPサポートチーム](/tidb-cloud/tidb-cloud-support.md)連絡することをお勧めします。

### アクティベーションまたはチェックアップ中に<code>no sufficient privileges</code>メッセージが表示されるのはなぜですか? {#why-does-the-code-no-sufficient-privileges-code-message-show-up-during-activation-or-check-up}

`no sufficient privileges`メッセージは通常、指定した SQL ユーザーに Index Insight からインデックスの推奨を要求するために必要な権限がない場合に表示されます。

この問題を解決するには、次の手順を実行します。

1.  ユーザー権限を確認します。ユーザー アカウントに、すべてのデータベースに対する`information_schema`と`mysql`の読み取り権限、および`PROCESS`と`REFERENCES`権限など、必要な権限が付与されているかどうかを確認します。

2.  新しいSQLユーザーを作成します。上記の手順で問題が解決しない場合は、以下のステートメントを使用して新しいSQLユーザーを作成できます。1と`'index_insight_user'` `'random_password'`実際の値に置き換えてください。

    ```sql
    CREATE user 'index_insight_user'@'%' IDENTIFIED by 'random_password';
    GRANT SELECT ON information_schema.* TO 'index_insight_user'@'%';
    GRANT SELECT ON mysql.* TO 'index_insight_user'@'%';
    GRANT PROCESS, REFERENCES ON *.* TO 'index_insight_user'@'%';
    FLUSH PRIVILEGES;
    ```

上記の手順を実行しても問題が解決しない場合は、 [PingCAPサポートチーム](/tidb-cloud/tidb-cloud-support.md)連絡することをお勧めします。

### Index Insight の使用中に、 <code>operations may be too frequent</code>メッセージが表示されるのはなぜですか? {#why-does-the-code-operations-may-be-too-frequent-code-message-show-up-during-using-index-insight}

`operations may be too frequent`メッセージは通常、Index Insight によって設定されたレートまたは使用制限を超えた場合に表示されます。

この問題を解決するには、次の手順を実行します。

1.  操作を遅くする: このメッセージが表示された場合は、Index Insight での操作頻度を下げる必要があります。
2.  サポートにお問い合わせください: 問題が解決しない場合は、 [PingCAPサポートチーム](/tidb-cloud/tidb-cloud-support.md)連絡して、エラー メッセージの詳細、操作内容、その他の関連情報を提供してください。

### Index Insight の使用中に<code>internal error</code>メッセージが表示されるのはなぜですか? {#why-does-the-code-internal-error-code-message-show-up-during-using-index-insight}

`internal error`メッセージは通常、システムで予期しないエラーや問題が発生したときに表示されます。このエラーメッセージは一般的な内容であり、根本的な原因の詳細は示されません。

この問題を解決するには、次の手順を実行します。

1.  操作を再試行してください：ページを更新するか、操作をもう一度お試しください。エラーは一時的なものである可能性があり、再試行するだけで解決できる場合があります。
2.  サポートにお問い合わせください: 問題が解決しない場合は、 [PingCAPサポートチーム](/tidb-cloud/tidb-cloud-support.md)連絡して、エラー メッセージの詳細、操作内容、その他の関連情報を提供してください。
