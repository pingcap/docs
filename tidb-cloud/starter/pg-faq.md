---
title: PostgreSQL互換 TiDB Cloud Starter FAQ
summary: パブリックプレビュー期間中の PostgreSQL互換 TiDB Cloud Starter に関するよくある質問への回答を掲載しています。
---

# PostgreSQL互換 TiDB Cloud Starter FAQ

このドキュメントでは、パブリックプレビュー期間中の PostgreSQL互換 {{{ .starter }}} に関するよくある質問に回答します。

PostgreSQL互換 {{{ .starter }}} を使用すると、開発者は TiDB Cloud コンソールから PostgreSQL互換データベースインスタンスを直接作成および管理できます。接続、モニタリング、バックアップ、リストアを含むインスタンスの主要なライフサイクルに加え、pgvector互換のベクトル検索や一部の PostgreSQL 拡張機能など、PostgreSQL エコシステムの機能もサポートします。

パブリックプレビュー期間中、PostgreSQL互換 {{{ .starter }}} は使用量クォータの範囲内で無料で利用できます。プレビュー期間中は課金は有効になっていません。

## 一般 FAQ {#general-faqs}

### PostgreSQL互換 Starter インスタンスを作成するにはどうすればよいですか？ {#how-can-i-create-a-postgresql-compatible-starter-instance}

PostgreSQL互換 {{{ .starter }}} はパブリックプレビューで利用可能です。

インスタンスを作成するには、TiDB Cloud コンソールで **Starter** を選択し、**PostgreSQL Compatible** オプションを選んで、設定を確認したうえでインスタンスを作成します。

パブリックプレビュー期間中、PostgreSQL互換は {{{ .starter }}} でのみ利用できます。{{{ .essential }}} と {{{ .premium }}} は現在このオプションをサポートしていません。

### 現在 PostgreSQL互換 Starter をサポートしているリージョンはどこですか？ {#which-regions-currently-support-postgresql-compatible-starter}

パブリックプレビュー期間中、PostgreSQL互換 {{{ .starter }}} は次のリージョンで利用できます。

- AWS US East (N. Virginia): `us-east-1`

プレビューの拡大に伴い、追加のリージョンが利用可能になる場合があります。新しいリージョンの提供開始時には案内されます。

### 同じ TiDB Cloud organization 内で MySQL互換 Starter インスタンスと PostgreSQL互換 Starter インスタンスの両方を使用できますか？ {#can-i-use-both-mysql-compatible-and-postgresql-compatible-starter-instances-in-the-same-tidb-cloud-organization}

はい。同じ organization、project、リージョン内で、MySQL互換と PostgreSQL互換の {{{ .starter }}} インスタンスを両方使用できます。

TiDB Cloud では、リソース一覧とインスタンス概要にデータベースタイプが表示されるため、2種類のインスタンスを区別できます。

### Starter インスタンスはいくつ作成できますか？ {#how-many-starter-instances-can-i-create}

有料 organization では、デフォルトで合計 **100 個の {{{ .starter }}} インスタンス** を作成できます。これには MySQL互換インスタンスと PostgreSQL互換インスタンスの両方が含まれます。MySQL互換インスタンスでは、各ブランチも 1 つのインスタンスとしてカウントされます。

無料インスタンス枠の対象は次のとおりです。

- 最初の **5 個の MySQL互換** {{{ .starter }}} インスタンス
- 最初の **10 個の PostgreSQL互換** {{{ .starter }}} インスタンス

### PostgreSQL互換 Starter を本番で使用できますか？ {#can-i-use-postgresql-compatible-starter-in-production}

パブリックプレビュー期間中は、開発、テスト、および本番相当のワークロードで PostgreSQL互換 {{{ .starter }}} を評価できます。**パブリックプレビュー期間中は、サービスレベル契約 (SLA) の保証は提供されません。**

このサービスはまだプレビュー段階であり、一部の機能は今後も進化する可能性があるため、本番ワークロードで PostgreSQL互換 {{{ .starter }}} を使用する場合は、General Availability (GA) まで待つことを推奨します。

## 機能と運用に関する FAQ {#features-and-operations-faqs}

### 現在 PostgreSQL互換 Starter で利用できる機能は何ですか？ {#what-features-are-currently-available-in-postgresql-compatible-starter}

PostgreSQL互換 {{{ .starter }}} には、次の機能があります。

- **インスタンス管理:** TiDB Cloud コンソールで PostgreSQL互換 {{{ .starter }}} インスタンスを作成、一覧表示、監視、削除できます。
- **接続性:** PostgreSQL互換クライアントおよびドライバーを使用して、パブリックエンドポイント経由で接続できます。
- **データインポート:** `psql` や `COPY` など、一般的な PostgreSQL ワークフローを使用してデータをインポートできます。
- **バックアップとリストア:** 毎日の自動バックアップを使用し、スナップショットを新しい PostgreSQL互換 {{{ .starter }}} インスタンスにリストアできます。
- **オブザーバビリティ:** ストレージ使用量、1 秒あたりのクエリ数 (QPS)、接続数、クエリ実行時間に関する組み込みメトリクスを確認できます。
- **AI とベクトル検索:** pgvector互換のベクトル検索、全文検索、サーバー側の埋め込み機能、および一部の PostgreSQL 拡張機能を使用できます。

PostgreSQL互換 {{{ .starter }}} はパブリックプレビュー期間中も進化を続けており、追加機能も計画されています。

### PostgreSQL互換 Starter インスタンスに接続するにはどうすればよいですか？ {#how-do-i-connect-to-a-postgresql-compatible-starter-instance}

TiDB Cloud コンソールで PostgreSQL互換 {{{ .starter }}} インスタンスの接続情報を開くと、パブリックエンドポイント、ポート、ユーザー名、および接続例を確認できます。

現在、PostgreSQL互換 {{{ .starter }}} ではプライベートエンドポイントはサポートされていません。

### PostgreSQL互換バックアップを MySQL互換インスタンスにリストアできますか？ {#can-a-postgresql-compatible-backup-be-restored-into-a-mysql-compatible-instance}

いいえ。プロトコルをまたぐリストアはサポートされていません。PostgreSQL互換バックアップは、PostgreSQL互換 {{{ .starter }}} インスタンスにのみリストアできます。

### `tidbcloud_com_cell_*` テーブルとは何ですか？ {#what-are-the-tidbcloud-com-cell-tables}

PostgreSQL互換 {{{ .starter }}} は、データベースユーザーを管理し、変更を安全に処理するために、`public` スキーマ内のシステム管理テーブルを使用します。これらのテーブルにはアプリケーションデータではなく、サービスメタデータが保存されます。

- **`tidbcloud_com_cell_principals`:** TiDB Cloud によって管理されるデータベースユーザーを追跡します。
- **`tidbcloud_com_cell_sql_versions`:** 管理対象データベースリソースへの変更を追跡し、競合する更新の防止に役立ちます。
- **`tidbcloud_com_cell_sql_receipts`:** リトライを安全に処理できるように、操作結果を記録します。このテーブルにはパスワードは保存されません。

TiDB Cloud はこれらのテーブルを自動的に管理します。**これらを変更または削除したり、アプリケーションデータの保存に使用したりしないでください。** そうすると、管理対象データベースユーザーの操作に支障をきたす可能性があります。

## 課金と計測に関する FAQ {#billing-and-metering-faqs}

### 使用量はどのように計測されますか？ {#how-is-my-usage-measured}

PostgreSQL互換 {{{ .starter }}} は TiDB Cloud Starter の使用量モデルに従い、次の項目を計測します。

- **Request Units (RUs)**
- **行ベースのストレージ**

パブリックプレビュー期間中は、RU 使用量はまだ表示されず、課金も発生しません。

### PostgreSQL互換 Starter はパブリックプレビュー期間中は無料ですか？ {#is-postgresql-compatible-starter-free-during-public-preview}

はい。PostgreSQL互換 {{{ .starter }}} は、使用量クォータの範囲内で、パブリックプレビュー期間中は無料で利用できます。この期間中は課金は有効になっていません。

各 organization における最初の **10 個の PostgreSQL互換 {{{ .starter }}} インスタンス** について、各インスタンスの無料クォータは次のとおりです。

- **行ベースのストレージ:** 50 GiB
- **Request Units (RUs):** 月あたり 5 億

リソース使用量が無料クォータを超えた場合、TiDB Cloud はそれ以上の使用を制限するか、サービスを停止する場合があります。

これらの上限を超える見込みがある場合、または追加リソースが必要な場合は、要件について相談するため <a href="mailto:support@pingcap.com">support@pingcap.com</a> までご連絡ください。