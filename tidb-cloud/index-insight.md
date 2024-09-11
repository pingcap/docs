---
title: Index Insight (Beta)
summary: TiDB Cloudの Index Insight 機能を使用して、低速クエリのインデックス推奨事項を取得する方法を学習します。
---

# インデックスインサイト（ベータ版） {#index-insight-beta}

TiDB Cloudの Index Insight (ベータ版) 機能は、インデックスを効果的に使用していない低速クエリに対してインデックスの推奨事項を提供することで、クエリ パフォーマンスを最適化する強力な機能を提供します。このドキュメントでは、Index Insight 機能を効果的に有効化して活用する手順について説明します。

> **注記：**
>
> Index Insight は現在ベータ版であり、 [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターでのみ使用できます。

## 導入 {#introduction}

Index Insight 機能には、次のような利点があります。

-   強化されたクエリ パフォーマンス: Index Insight は、遅いクエリを識別し、適切なインデックスを提案します。これにより、クエリの実行が高速化され、応答時間が短縮され、ユーザー エクスペリエンスが向上します。
-   コスト効率: Index Insight を使用してクエリ パフォーマンスを最適化すると、追加のコンピューティング リソースの必要性が減り、既存のインフラストラクチャをより効率的に使用できるようになります。これにより、運用コストの削減につながる可能性があります。
-   簡素化された最適化プロセス: Index Insight は、インデックスの改善の特定と実装を簡素化し、手動分析や推測の必要性を排除します。その結果、正確なインデックスの推奨事項により、時間と労力を節約できます。
-   アプリケーション効率の向上: Index Insight を使用してデータベース パフォーマンスを最適化することで、 TiDB Cloudで実行されるアプリケーションはより大きなワークロードを処理し、より多くのユーザーに同時にサービスを提供できるようになり、アプリケーションのスケーリング操作がより効率的になります。

## 使用法 {#usage}

このセクションでは、Index Insight 機能を有効にして、低速クエリに推奨されるインデックスを取得する方法について説明します。

### 始める前に {#before-you-begin}

Index Insight 機能を有効にする前に、 TiDB Cloud Dedicated クラスターを作成していることを確認してください。クラスターがない場合は、 [TiDB Cloud専用クラスターを作成する](/tidb-cloud/create-tidb-cluster.md)の手順に従って作成してください。

### ステップ1: Index Insightを有効にする {#step-1-enable-index-insight}

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、 TiDB Cloud Dedicated クラスターのクラスター概要ページに移動し、左側のナビゲーション ペインで**[診断] を**クリックします。

2.  **Index Insight BETA**タブをクリックします。Index **Insight の概要**ページが表示されます。

3.  Index Insight 機能を使用するには、機能をトリガーしてインデックスの推奨事項を受信するために使用される専用の SQL ユーザーを作成する必要があります。次の SQL ステートメントは、 `information_schema`と`mysql`の読み取り権限、およびすべてのデータベースに対する`PROCESS`と`REFERENCES`権限を含む、必要な権限を持つ新しい SQL ユーザーを作成します。 `'index_insight_user'`と`'random_password'`実際の値に置き換えます。

    ```sql
    CREATE user 'index_insight_user'@'%' IDENTIFIED by 'random_password';
    GRANT SELECT ON information_schema.* TO 'index_insight_user'@'%';
    GRANT SELECT ON mysql.* TO 'index_insight_user'@'%';
    GRANT PROCESS, REFERENCES ON *.* TO 'index_insight_user'@'%';
    FLUSH PRIVILEGES;
    ```

    > **注記：**
    >
    > TiDB Cloud Dedicated クラスターに接続するには、 [TiDB Cloud Dedicatedクラスタに接続する](/tidb-cloud/connect-to-tidb-cluster.md)参照してください。

4.  前の手順で作成した SQL ユーザーのユーザー名とパスワードを入力します。次に、 **[アクティブ化] を**クリックしてアクティブ化プロセスを開始します。

### ステップ2: Index Insightを手動で起動する {#step-2-manually-trigger-index-insight}

遅いクエリのインデックス推奨事項を取得するには、 **Index Insight 概要**ページの右上隅にある**[チェック アップ]**をクリックして、Index Insight 機能を手動でトリガーできます。

次に、この機能は過去 3 時間の遅いクエリのスキャンを開始します。スキャンが完了すると、分析に基づいてインデックスの推奨事項のリストが提供されます。

### ステップ3: インデックスの推奨事項をビュー {#step-3-view-index-recommendations}

特定のインデックス推奨事項の詳細を表示するには、リストからインサイトをクリックします。**インデックス インサイトの詳細**ページが表示されます。

このページでは、インデックスの推奨事項、関連する低速クエリ、実行プラン、および関連メトリックを確認できます。この情報は、パフォーマンスの問題をより深く理解し、インデックスの推奨事項を実装した場合の潜在的な影響を評価するのに役立ちます。

### ステップ4: インデックスの推奨事項を実装する {#step-4-implement-index-recommendations}

インデックスの推奨事項を実装する前に、まず**Index Insight の詳細**ページから推奨事項を確認して評価する必要があります。

インデックスの推奨事項を実装するには、次の手順に従います。

1.  提案されたインデックスが既存のクエリとワークロードに与える影響を評価します。
2.  インデックス実装に関連するstorage要件と潜在的なトレードオフを考慮してください。
3.  適切なデータベース管理ツールを使用して、関連するテーブルにインデックスの推奨事項を作成します。
4.  インデックスを実装した後のパフォーマンスを監視して、改善を評価します。

## ベストプラクティス {#best-practices}

このセクションでは、Index Insight 機能の使用に関するベスト プラクティスをいくつか紹介します。

### インデックスインサイトを定期的に起動する {#regularly-trigger-index-insight}

最適化されたインデックスを維持するには、毎日など定期的に、またはクエリやデータベース スキーマに大幅な変更が発生したときに Index Insight 機能をトリガーすることをお勧めします。

### インデックスを実装する前に影響を分析する {#analyze-impact-before-implementing-indexes}

インデックスの推奨事項を実装する前に、クエリ実行プラン、ディスク領域、および関連するトレードオフへの潜在的な影響を分析します。パフォーマンスの大幅な向上をもたらすインデックスの実装を優先します。

### パフォーマンスを監視する {#monitor-performance}

インデックスの推奨事項を実装した後は、クエリのパフォーマンスを定期的に監視します。これにより、改善点を確認し、必要に応じてさらに調整を行うことができます。

## FAQ {#faq}

このセクションでは、Index Insight 機能に関するよくある質問をいくつか示します。

### Index Insight を非アクティブ化するにはどうすればよいですか? {#how-to-deactivate-index-insight}

Index Insight 機能を無効にするには、次の手順を実行します。

1.  **Index Insight の概要**ページの右上隅にある**[設定]**をクリックします。Index **Insight の設定**ページが表示されます。
2.  **「非アクティブ化」**をクリックします。確認ダイアログボックスが表示されます。
3.  非アクティブ化を確認するには、 **[OK]**をクリックします。

    Index Insight 機能を非アクティブ化すると、すべてのインデックス推奨事項が**Index Insight 概要**ページから削除されます。ただし、この機能用に作成された SQL ユーザーは削除されません。SQL ユーザーは手動で削除できます。

### Index Insight を非アクティブ化した後、SQL ユーザーを削除するにはどうすればよいでしょうか? {#how-to-delete-the-sql-user-after-deactivating-index-insight}

Index Insight 機能を無効にした後、 `DROP USER`ステートメントを実行して、その機能用に作成された SQL ユーザーを削除できます。次に例を示します。3 `'username'`実際の値に置き換えます。

```sql
DROP USER 'username';
```

### アクティベーションまたはチェックアップ中に<code>invalid user or password</code>メッセージが表示されるのはなぜですか? {#why-does-the-code-invalid-user-or-password-code-message-show-up-during-activation-or-check-up}

`invalid user or password`メッセージは通常、システムが提供した資格情報を認証できない場合に表示されます。この問題は、ユーザー名またはパスワードが正しくない、ユーザー アカウントの有効期限が切れている、またはロックされているなど、さまざまな理由で発生する可能性があります。

この問題を解決するには、次の手順を実行します。

1.  資格情報を確認してください: 入力したユーザー名とパスワードが正しいことを確認してください。大文字と小文字の区別に注意してください。
2.  アカウントのステータスを確認する: ユーザー アカウントがアクティブなステータスであり、期限切れまたはロックされていないことを確認します。これを確認するには、システム管理者または関連するサポート チャネルに問い合わせてください。
3.  新しい SQL ユーザーを作成します。前の手順でこの問題が解決しない場合は、次のステートメントを使用して新しい SQL ユーザーを作成できます。1 と`'random_password'` `'index_insight_user'`の値に置き換えます。

    ```sql
    CREATE user 'index_insight_user'@'%' IDENTIFIED by 'random_password';
    GRANT SELECT ON information_schema.* TO 'index_insight_user'@'%';
    GRANT SELECT ON mysql.* TO 'index_insight_user'@'%';
    GRANT PROCESS, REFERENCES ON *.* TO 'index_insight_user'@'%';
    FLUSH PRIVILEGES;
    ```

上記の手順を実行しても問題が解決しない場合は、 [PingCAP サポートチーム](/tidb-cloud/tidb-cloud-support.md)連絡することをお勧めします。

### アクティベーションまたはチェックアップ中に<code>no sufficient privileges</code>メッセージが表示されるのはなぜですか? {#why-does-the-code-no-sufficient-privileges-code-message-show-up-during-activation-or-check-up}

`no sufficient privileges`メッセージは通常、指定した SQL ユーザーに Index Insight からインデックスの推奨を要求するために必要な権限がない場合に表示されます。

この問題を解決するには、次の手順を実行します。

1.  ユーザー権限を確認する: ユーザー アカウントに、 `information_schema`と`mysql`の読み取り権限、およびすべてのデータベースに対する`PROCESS`と`REFERENCES`権限など、必要な権限が付与されているかどうかを確認します。

2.  新しい SQL ユーザーを作成します。前の手順でこの問題が解決しない場合は、次のステートメントを使用して新しい SQL ユーザーを作成できます。1 と`'random_password'` `'index_insight_user'`の値に置き換えます。

    ```sql
    CREATE user 'index_insight_user'@'%' IDENTIFIED by 'random_password';
    GRANT SELECT ON information_schema.* TO 'index_insight_user'@'%';
    GRANT SELECT ON mysql.* TO 'index_insight_user'@'%';
    GRANT PROCESS, REFERENCES ON *.* TO 'index_insight_user'@'%';
    FLUSH PRIVILEGES;
    ```

上記の手順を実行しても問題が解決しない場合は、 [PingCAP サポートチーム](/tidb-cloud/tidb-cloud-support.md)連絡することをお勧めします。

### Index Insight の使用中に、 <code>operations may be too frequent</code>メッセージが表示されるのはなぜですか? {#why-does-the-code-operations-may-be-too-frequent-code-message-show-up-during-using-index-insight}

`operations may be too frequent`メッセージは通常、Index Insight によって設定されたレートまたは使用制限を超えた場合に表示されます。

この問題を解決するには、次の手順を実行します。

1.  操作を遅くする: このメッセージが表示された場合は、Index Insight での操作頻度を下げる必要があります。
2.  サポートにお問い合わせください: 問題が解決しない場合は、 [PingCAP サポートチーム](/tidb-cloud/tidb-cloud-support.md)連絡して、エラー メッセージの詳細、操作内容、その他の関連情報を提供してください。

### Index Insight の使用中に<code>internal error</code>メッセージが表示されるのはなぜですか? {#why-does-the-code-internal-error-code-message-show-up-during-using-index-insight}

`internal error`メッセージは通常、システムで予期しないエラーや問題が発生した場合に表示されます。このエラー メッセージは一般的な内容であり、根本的な原因の詳細は示されません。

この問題を解決するには、次の手順を実行します。

1.  操作を再試行してください: ページを更新するか、操作を再試行してください。エラーは一時的なものである可能性があり、単純に再試行することで解決できます。
2.  サポートにお問い合わせください: 問題が解決しない場合は、 [PingCAP サポートチーム](/tidb-cloud/tidb-cloud-support.md)連絡して、エラー メッセージの詳細、操作内容、その他の関連情報を提供してください。
