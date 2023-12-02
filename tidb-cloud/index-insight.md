---
title: Index Insight (Beta)
summary: Learn how to use the Index Insight feature in TiDB Cloud and obtain index recommendations for slow queries.
---

# インデックスインサイト（ベータ版） {#index-insight-beta}

TiDB Cloudの Index Insight (ベータ) 機能は、インデックスを効果的に使用していない遅いクエリに対してインデックスの推奨を提供することで、クエリのパフォーマンスを最適化する強力な機能を提供します。このドキュメントでは、Index Insight 機能を有効にして効果的に利用する手順について説明します。

> **注記：**
>
> Index Insight は現在ベータ版であり、 [TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターでのみ使用できます。

## 導入 {#introduction}

Index Insight 機能には次の利点があります。

-   クエリのパフォーマンスの強化: Index Insight は遅いクエリを特定し、それらに適切なインデックスを提案します。これにより、クエリの実行が高速化され、応答時間が短縮され、ユーザー エクスペリエンスが向上します。
-   コスト効率: Index Insight を使用してクエリ パフォーマンスを最適化すると、追加のコンピューティング リソースの必要性が減り、既存のインフラストラクチャをより効果的に使用できるようになります。これにより、運用コストの削減につながる可能性があります。
-   簡素化された最適化プロセス: Index Insight は、インデックスの改善点の特定と実装を簡素化し、手動による分析や推測の必要性を排除します。その結果、正確なインデックス推奨により時間と労力を節約できます。
-   アプリケーション効率の向上: Index Insight を使用してデータベースのパフォーマンスを最適化することで、 TiDB Cloud上で実行されるアプリケーションはより大きなワークロードを処理し、より多くのユーザーに同時にサービスを提供できるため、アプリケーションのスケーリング操作がより効率的になります。

## 使用法 {#usage}

このセクションでは、インデックス インサイト機能を有効にして、遅いクエリに対して推奨されるインデックスを取得する方法を紹介します。

### あなたが始める前に {#before-you-begin}

Index Insight 機能を有効にする前に、TiDB 専用クラスターを作成していることを確認してください。お持ちでない場合は、 [TiDB 専用クラスターの作成](/tidb-cloud/create-tidb-cluster.md)の手順に従って作成してください。

### ステップ 1: Index Insight を有効にする {#step-1-enable-index-insight}

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、TiDB 専用クラスターのクラスター概要ページに移動し、左側のナビゲーション ペインで**[診断]**をクリックします。

2.  **「Index Insight BETA」**タブをクリックします。 **Index Insight の概要**ページが表示されます。

3.  Index Insight 機能を使用するには、専用の SQL ユーザーを作成する必要があります。このユーザーは、機能をトリガーし、インデックスの推奨事項を受け取るために使用されます。次の SQL ステートメントは、必要な権限( `information_schema`と`mysql`に対する読み取り権限、すべてのデータベースに対する`PROCESS`と`REFERENCES`権限)を持つ新しい SQL ユーザーを作成します。 `'index_insight_user'`と`'random_password'`実際の値に置き換えます。

    ```sql
    CREATE user 'index_insight_user'@'%' IDENTIFIED by 'random_password';
    GRANT SELECT ON information_schema.* TO 'index_insight_user'@'%';
    GRANT SELECT ON mysql.* TO 'index_insight_user'@'%';
    GRANT PROCESS, REFERENCES ON *.* TO 'index_insight_user'@'%';
    FLUSH PRIVILEGES;
    ```

    > **注記：**
    >
    > TiDB 専用クラスターに接続するには、 [TiDB 専用クラスターに接続する](/tidb-cloud/connect-to-tidb-cluster.md)を参照してください。

4.  前の手順で作成した SQL ユーザーのユーザー名とパスワードを入力します。次に、 **「アクティブ化」**をクリックしてアクティブ化プロセスを開始します。

### ステップ 2: Index Insight を手動でトリガーする {#step-2-manually-trigger-index-insight}

遅いクエリに対するインデックスの推奨事項を取得するには、[インデックス インサイト]**概要**ページの右上隅にある**[チェックアップ]**をクリックして、インデックス インサイト機能を手動でトリガーできます。

次に、この機能は過去 3 時間の遅いクエリのスキャンを開始します。スキャンが完了すると、分析に基づいてインデックスの推奨事項のリストが提供されます。

### ステップ 3: インデックスの推奨事項をビュー {#step-3-view-index-recommendations}

特定のインデックス推奨の詳細を表示するには、リストからインサイトをクリックします。 **[インデックス インサイトの詳細]**ページが表示されます。

このページでは、インデックスの推奨事項、関連する遅いクエリ、実行プラン、および関連するメトリクスを見つけることができます。この情報は、パフォーマンスの問題をより深く理解し、インデックス推奨事項の実装による潜在的な影響を評価するのに役立ちます。

### ステップ 4: インデックスの推奨事項を実装する {#step-4-implement-index-recommendations}

インデックスの推奨事項を実装する前に、まず**[インデックス インサイトの詳細]**ページで推奨事項を確認して評価する必要があります。

インデックスの推奨事項を実装するには、次の手順に従います。

1.  提案されたインデックスが既存のクエリとワークロードに及ぼす影響を評価します。
2.  storage要件と、インデックスの実装に関連する潜在的なトレードオフを考慮してください。
3.  適切なデータベース管理ツールを使用して、関連するテーブルに推奨されるインデックスを作成します。
4.  インデックスを実装した後のパフォーマンスを監視して、改善を評価します。

## ベストプラクティス {#best-practices}

このセクションでは、Index Insight 機能を使用するためのベスト プラクティスをいくつか紹介します。

### Index Insight を定期的にトリガーする {#regularly-trigger-index-insight}

最適化されたインデックスを維持するには、毎日、またはクエリやデータベース スキーマに大幅な変更が発生したときなど、定期的に Index Insight 機能をトリガーすることをお勧めします。

### インデックスを導入する前に影響を分析する {#analyze-impact-before-implementing-indexes}

インデックスの推奨事項を実装する前に、クエリ実行プラン、ディスク容量、および関連するトレードオフに対する潜在的な影響を分析してください。最も大幅なパフォーマンス向上をもたらすインデックスの実装を優先します。

### パフォーマンスを監視する {#monitor-performance}

インデックスの推奨事項を実装した後は、クエリのパフォーマンスを定期的に監視します。これは、改善点を確認し、必要に応じてさらに調整するのに役立ちます。

## FAQ {#faq}

このセクションでは、Index Insight 機能に関してよくある質問をいくつか示します。

### Index Insight を非アクティブ化するにはどうすればよいですか? {#how-to-deactivate-index-insight}

Index Insight 機能を無効にするには、次の手順を実行します。

1.  **Index Insight の概要**ページの右上隅にある**[設定]**をクリックします。 **Index Insight 設定**ページが表示されます。
2.  **「非アクティブ化」**をクリックします。確認のダイアログボックスが表示されます。
3.  **「OK」**をクリックして非アクティブ化を確認します。

    Index Insight 機能を非アクティブ化すると、すべてのインデックスの推奨事項が**Index Insight の概要**ページから削除されます。ただし、この機能用に作成された SQL ユーザーは削除されません。 SQL ユーザーは手動で削除できます。

### Index Insight を非アクティブ化した後に SQL ユーザーを削除するにはどうすればよいですか? {#how-to-delete-the-sql-user-after-deactivating-index-insight}

Index Insight 機能を非アクティブ化した後、 `DROP USER`ステートメントを実行して、この機能用に作成された SQL ユーザーを削除できます。以下は一例です。 `'username'`実際の値に置き換えます。

```sql
DROP USER 'username';
```

### アクティベーションまたはチェックアップ中に<code>invalid user or password</code>メッセージが表示されるのはなぜですか? {#why-does-the-code-invalid-user-or-password-code-message-show-up-during-activation-or-check-up}

`invalid user or password`メッセージは通常、指定した資格情報をシステムが認証できない場合にプロンプ​​トを表示します。この問題は、ユーザー名やパスワードが間違っている、ユーザー アカウントの有効期限が切れているかロックされているなど、さまざまな理由で発生する可能性があります。

この問題を解決するには、次の手順を実行します。

1.  資格情報を確認する: 指定したユーザー名とパスワードが正しいことを確認してください。大文字と小文字の区別に注意してください。
2.  アカウントのステータスを確認する: ユーザー アカウントがアクティブなステータスにあり、期限切れまたはロックされていないことを確認します。これを確認するには、システム管理者または関連するサポート チャネルに問い合わせてください。
3.  新しい SQL ユーザーを作成する: 前の手順でこの問題が解決されない場合は、次のステートメントを使用して新しい SQL ユーザーを作成できます。 `'index_insight_user'`と`'random_password'`を実際の値に置き換えます。

    ```sql
    CREATE user 'index_insight_user'@'%' IDENTIFIED by 'random_password';
    GRANT SELECT ON information_schema.* TO 'index_insight_user'@'%';
    GRANT SELECT ON mysql.* TO 'index_insight_user'@'%';
    GRANT PROCESS, REFERENCES ON *.* TO 'index_insight_user'@'%';
    FLUSH PRIVILEGES;
    ```

前述の手順を実行しても問題が解決しない場合は、 [PingCAP サポート チーム](/tidb-cloud/tidb-cloud-support.md)に連絡することをお勧めします。

### アクティベーションまたはチェックアップ中に<code>no sufficient privileges</code>メッセージが表示されるのはなぜですか? {#why-does-the-code-no-sufficient-privileges-code-message-show-up-during-activation-or-check-up}

`no sufficient privileges`メッセージは通常、指定した SQL ユーザーに Index Insight からのインデックス推奨を要求するために必要な権限がない場合にプロンプ​​トを表示します。

この問題を解決するには、次の手順を実行します。

1.  ユーザー権限を確認する: ユーザー アカウントに、すべてのデータベースに対する`information_schema`と`mysql`の読み取り権限、 `PROCESS`と`REFERENCES`権限など、必要な権限が付与されているかどうかを確認します。

2.  新しい SQL ユーザーを作成する: 前の手順でこの問題が解決されない場合は、次のステートメントを使用して新しい SQL ユーザーを作成できます。 `'index_insight_user'`と`'random_password'`を実際の値に置き換えます。

    ```sql
    CREATE user 'index_insight_user'@'%' IDENTIFIED by 'random_password';
    GRANT SELECT ON information_schema.* TO 'index_insight_user'@'%';
    GRANT SELECT ON mysql.* TO 'index_insight_user'@'%';
    GRANT PROCESS, REFERENCES ON *.* TO 'index_insight_user'@'%';
    FLUSH PRIVILEGES;
    ```

前述の手順を実行しても問題が解決しない場合は、 [PingCAP サポート チーム](/tidb-cloud/tidb-cloud-support.md)に連絡することをお勧めします。

### Index Insight の使用中に<code>operations may be too frequent</code>というメッセージが表示されるのはなぜですか? {#why-does-the-code-operations-may-be-too-frequent-code-message-show-up-during-using-index-insight}

`operations may be too frequent`メッセージは通常、Index Insight によって設定されたレートまたは使用制限を超過した場合にプロンプ​​トを表示します。

この問題を解決するには、次の手順を実行します。

1.  操作を遅くしてください: このメッセージが表示された場合は、Index Insight での操作頻度を減らす必要があります。
2.  サポートに連絡する: 問題が解決しない場合は、 [PingCAP サポート チーム](/tidb-cloud/tidb-cloud-support.md)に連絡し、エラー メッセージの詳細、アクション、その他の関連情報を提供してください。

### Index Insight の使用中に<code>internal error</code>メッセージが表示されるのはなぜですか? {#why-does-the-code-internal-error-code-message-show-up-during-using-index-insight}

`internal error`メッセージは通常、システムで予期しないエラーまたは問題が発生したときに表示されます。このエラー メッセージは一般的なものであり、根本的な原因に関する詳細は示されていません。

この問題を解決するには、次の手順を実行します。

1.  操作を再試行します: ページを更新するか、操作を再試行してください。エラーは一時的なものである可能性があり、簡単な再試行で解決できます。
2.  サポートに連絡する: 問題が解決しない場合は、 [PingCAP サポート チーム](/tidb-cloud/tidb-cloud-support.md)に連絡し、エラー メッセージの詳細、アクション、その他の関連情報を提供してください。
