---
title: Tableau で TiDB Cloud Lake に接続する
summary: Tableau は、データを使って問題を解決する方法を変革するビジュアル分析プラットフォームです。lake-jdbc ドライバーを使用することで、Tableau の Other Databases (JDBC) インターフェースを介して TiDB Cloud Lake に接続できます。
---

# Tableau で TiDB Cloud Lake に接続する

[Tableau](https://www.tableau.com/) は、データを使って問題を解決する方法を変革するビジュアル分析プラットフォームです。[lake-jdbc driver](https://github.com/tidbcloud/lake-jdbc) を使用することで、Tableau の **Other Databases (JDBC)** インターフェースを介して {{{ .lake }}} に接続できます。

最適な互換性のために、Tableau バージョン 2022.3 以降を使用してください。

## チュートリアル: {{{ .lake }}} との統合 {#tutorial-integrating-with-lake}

このチュートリアルでは、`lake-jdbc` を使用して Tableau Desktop を {{{ .lake }}} に接続する方法を説明します。

### Step 1. 接続情報を取得する {#step-1-obtain-connection-information}

{{{ .lake }}} Warehouse の接続情報を取得します。詳細については、[Warehouse への接続](/tidb-cloud-lake/guides/warehouse.md#connecting-to-a-warehouse) を参照してください。

### Step 2. lake-jdbc をインストールする {#step-2-install-lake-jdbc}

1. 次のいずれかの場所から `lake-jdbc` バージョン `0.4.6` 以降をダウンロードします。

    - [lake-jdbc GitHub repository](https://github.com/tidbcloud/lake-jdbc)
    - [lake-jdbc on Maven Central](https://repo1.maven.org/maven2/com/tidbcloud/lake-jdbc/)

2. ドライバーの JAR ファイル（たとえば `lake-jdbc-0.4.6.jar`）を Tableau のドライバーフォルダーに移動します。

    | オペレーティングシステム | Tableau のドライバーフォルダー      |
    | ---------------- | -------------------------------- |
    | MacOS            | ~/Library/Tableau/Drivers        |
    | Windows          | C:\Program Files\Tableau\Drivers |
    | Linux            | /opt/tableau/tableau_driver/jdbc |

### Step 3. {{{ .lake }}} に接続する {#step-3-connect-to-lake}

1. Tableau Desktop を起動し、サイドバーで **Other Databases (JDBC)** を選択します。

    ![Other Databases (JDBC)](/media/tidb-cloud-lake/bi-tableau-1.png)

2. ウィンドウで {{{ .lake }}} の接続情報を入力し、**Sign In** をクリックします。

    | パラメーター | 説明                               | このチュートリアルでの値                                           |
    | --------- | ----------------------------------------- | ------------------------------------------------------------------- |
    | URL       | 形式: `jdbc:lake://{user}:{password}@{host}:{port}/{database}` | `jdbc:lake://cloudapp:<your-password>@<your-host>:443/default` |
    | Dialect   | SQL dialect には "MySQL" を選択します。           | MySQL                                                               |
    | Username  | {{{ .lake }}} に接続するための SQL user  | cloudapp                                                            |
    | Password  | SQL user のパスワード                         | あなたのパスワード                                                       |

3. Tableau ワークブックが開いたら、クエリ対象のデータベース、スキーマ、およびテーブルを選択します。このチュートリアルでは、**Database** と **Schema** の両方に _default_ を選択します。

これで準備完了です。テーブルを作業エリアにドラッグして、クエリとその後の分析を開始できます。