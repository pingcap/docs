---
title: DDL (Data Definition Language) コマンド
summary: これらのトピックでは、{{{ .lake }}} における DDL (Data Definition Language) コマンドのリファレンス情報を提供します。
---

# DDL (Data Definition Language) コマンド

これらのトピックでは、{{{ .lake }}} における DDL (Data Definition Language) コマンドのリファレンス情報を提供します。

## データベースとテーブルの管理 {#database-table-management}

| コンポーネント | 説明 |
|-----------|-------------|
| **[Catalog](/tidb-cloud-lake/sql/catalog.md)** | Catalog の作成、削除、および一覧表示 |
| **[データベース](/tidb-cloud-lake/sql/ddl-database-overview.md)** | データベースの作成、変更、および削除 |
| **[Table](/tidb-cloud-lake/sql/ddl-table-overview.md)** | テーブルの作成、変更、および管理 |
| **[テーブルバージョニング](/tidb-cloud-lake/sql/table-versioning.md)** | タイムトラベル用の名前付きスナップショットタグを作成 |
| **[ビュー](/tidb-cloud-lake/sql/ddl-view-overview.md)** | クエリに基づく仮想テーブルの作成と管理 |

## パフォーマンスとインデックス {#performance-indexing}

| コンポーネント | 説明 |
|-----------|-------------|
| **[クラスターキー](/tidb-cloud-lake/sql/cluster-key.md)** | クエリ最適化のためのデータクラスタリングを定義 |
| **[集約インデックス](/tidb-cloud-lake/sql/aggregating-index-sql.md)** | より高速なクエリのために集計を事前計算 |
| **[転置インデックス](/tidb-cloud-lake/sql/inverted-index.md)** | テキストカラム向けの全文検索インデックス |
| **[Ngram Index](/tidb-cloud-lake/sql/ngram-index-sql.md)** | LIKE パターン向けの部分文字列検索インデックス |
| **[Spatial Index](/tidb-cloud-lake/sql/spatial-index-overview.md)** | GEOMETRY カラム向けの空間プルーニングインデックス |
| **[Vector Index](/tidb-cloud-lake/sql/vector-index.md)** | ベクトル埋め込み向けの類似検索インデックス |
| **[仮想カラム](/tidb-cloud-lake/sql/virtual-column-overview.md)** | JSON フィールドを仮想カラムとして抽出してインデックス化 |

## セキュリティとアクセス制御 {#security-access-control}

| コンポーネント | 説明 |
|-----------|-------------|
| **[User](/tidb-cloud-lake/sql/user-role.md)** | データベースユーザーの作成と管理 |
| **[Tag](/tidb-cloud-lake/sql/tag-overview.md)** | ガバナンスと分類のためにオブジェクトへキーと値のメタデータを付加 |
| **[ネットワークポリシー](/tidb-cloud-lake/sql/network-policy-sql.md)** | データベースへのネットワークアクセスを制御 |
| **[マスクポリシー](/tidb-cloud-lake/sql/masking-policy-sql.md)** | 機密情報に対してデータマスキングを適用 |
| **[パスワードポリシー](/tidb-cloud-lake/sql/password-policy-sql.md)** | パスワード要件とローテーションを強制 |
| **[行アクセスポリシー](/tidb-cloud-lake/sql/row-access-policy-overview.md)** | 集中管理された行レベル述語でテーブル行をフィルタリング |

## データ統合と処理 {#data-integration-processing}

| コンポーネント | 説明 |
|-----------|-------------|
| **[Stage](/tidb-cloud-lake/sql/stage.md)** | データロード用のストレージ場所を定義 |
| **[Pipe](/tidb-cloud-lake/sql/pipe.md)** | 取り込みパイプを管理 |
| **[Stream](/tidb-cloud-lake/sql/stream.md)** | データ変更をキャプチャして処理 |
| **[タスク](/tidb-cloud-lake/sql/task.md)** | SQL 操作をスケジュールして自動化 |
| **[シーケンス](/tidb-cloud-lake/sql/sequence.md)** | 一意な連番を生成 |
| **[Connection](/tidb-cloud-lake/sql/connection.md)** | 外部データソース接続を設定 |
| **[ファイル形式](/tidb-cloud-lake/sql/file-format.md)** | データのインポート/エクスポート用フォーマットを定義 |
| **[Dictionary](/tidb-cloud-lake/sql/dictionary.md)** | 外部ソースをバックエンドとする辞書を定義 |

## 関数とプロシージャ {#functions-procedures}

| コンポーネント | 説明 |
|-----------|-------------|
| **[UDF](/tidb-cloud-lake/sql/user-defined-function.md)** | Python または JavaScript でカスタム関数を作成 |
| **[External Function](/tidb-cloud-lake/sql/external-function.md)** | 外部 API を SQL 関数として統合 |
| **[Procedure](/tidb-cloud-lake/sql/stored-procedure.md)** | 複雑なロジックのためのストアドプロシージャを作成 |
| **[Notification](/tidb-cloud-lake/sql/notification.md)** | イベント通知と webhook を設定 |

## リソース管理 {#resource-management}

| コンポーネント | 説明 |
|-----------|-------------|
| **[Warehouse](/tidb-cloud-lake/sql/warehouse-overview.md)** | クエリ実行用のコンピュートリソースを管理 |
| **[Worker](/tidb-cloud-lake/sql/worker-overview.md)** | クラウド制御を通じて sandbox UDF 実行環境を管理 |
| **[Workload Group](/tidb-cloud-lake/sql/workload-group.md)** | リソース割り当てと優先度を制御 |
| **[トランザクション](/tidb-cloud-lake/sql/transaction.md)** | データベーストランザクションを管理 |
| **[Variable](/tidb-cloud-lake/sql/sql-variables.md)** | セッション変数とグローバル変数を設定して使用 |