---
title: Connect to TiDB with Hibernate
summary: Hibernateを使用してTiDBに接続する方法を学びましょう。このチュートリアルでは、Hibernateを使用してTiDBと連携するJavaのサンプルコードを紹介します。
aliases: ['/ja/tidb/stable/dev-guide-sample-application-java-hibernate/','/ja/tidb/dev/dev-guide-sample-application-java-hibernate/','/ja/tidbcloud/dev-guide-sample-application-java-hibernate/']
---

# Hibernateを使用してTiDBに接続する {#connect-to-tidb-with-hibernate}

TiDBはMySQL互換データベースであり、[ハイバネイト](https://hibernate.org/orm/)人気のオープンソースJava ORMです。TiDBはMySQLとの互換性が非常に高いため、長期的な互換性を確保するには、Hibernateの方言として`org.hibernate.dialect.MySQLDialect`使用することをお勧めします。あるいは、 [Hibernateコミュニティ方言](https://github.com/hibernate/hibernate-orm/tree/main/hibernate-community-dialects)にはTiDB専用の方言（ `org.hibernate.community.dialect.TiDBDialect` ）も用意されていますが、PingCAPではメンテナンスされていません。 `MySQLDialect`を使用して互換性の問題が発生した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告してください。

このチュートリアルでは、TiDBとHibernateを使用して以下のタスクを実行する方法を学ぶことができます。

-   環境をセットアップしてください。
-   Hibernateを使用してTiDBに接続します。
-   アプリケーションをビルドして実行します。オプションで、基本的な CRUD 操作用の[サンプルコードスニペット](#sample-code-snippets)を見つけることができます。

> **注記：**
>
> このチュートリアルは、 TiDB Cloud Starter、 TiDB Cloud Essential、 TiDB Cloud Premium、 TiDB Cloud Dedicated、およびTiDB Self-Managedに対応しています。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、以下が必要です。

-   **Java Development Kit (JDK) 17**以降が必要です。業務要件や個人のニーズに応じて、 [OpenJDK](https://openjdk.org/)または[Oracle JDK](https://www.oracle.com/hk/java/technologies/downloads/)を選択できます。
-   [メイブン](https://maven.apache.org/install.html)**3.8**以上。
-   [Git](https://git-scm.com/downloads) 。
-   TiDBクラスタ。

**TiDBクラスタをお持ちでない場合は、以下の手順で作成できます。**

-   (推奨) [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)。
-   [ローカルテスト用のTiDBセルフマネージドクラスタをデプロイ。](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番本番のTiDBセルフマネージドクラスタをデプロイ。](/production-deployment-using-tiup.md)

## TiDBに接続するには、サンプルアプリを実行してください。 {#run-the-sample-app-to-connect-to-tidb}

このセクションでは、サンプルアプリケーションコードを実行してTiDBに接続する方法を説明します。

### ステップ1：サンプルアプリのリポジトリをクローンする {#step-1-clone-the-sample-app-repository}

サンプルコードリポジトリをクローンするには、ターミナルウィンドウで以下のコマンドを実行してください。

```shell
git clone https://github.com/tidb-samples/tidb-java-hibernate-quickstart.git
cd tidb-java-hibernate-quickstart
```

### ステップ2：接続情報を設定する {#step-2-configure-connection-information}

選択したTiDBのデプロイオプションに応じて、TiDBに接続してください。

<SimpleTab>
<div label="TiDB Cloud Starter or Essential">

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックして、概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  接続ダイアログの設定がご使用のオペレーティング環境と一致していることを確認してください。

    -   **接続タイプ**は`Public`に設定されています。

    -   **ブランチ**は`main`に設定されています。

    -   **Connect With は**`General`に設定されています。

    -   お使いの環境に合った**オペレーティングシステム**を選択してください。

    > **ヒント：**
    >
    > プログラムがWindows Subsystem for Linux（WSL）上で実行されている場合は、対応するLinuxディストリビューションに切り替えてください。

4.  **「パスワードを生成」を**クリックすると、ランダムなパスワードが生成されます。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードをリセット」**をクリックして新しいパスワードを生成できます。

5.  `env.sh.example`をコピーして`env.sh`に名前を変更するには、次のコマンドを実行します。

    ```shell
    cp env.sh.example env.sh
    ```

6.  対応する接続​​文字列`env.sh`ファイルにコピー＆ペーストしてください。例は以下のとおりです。

    ```shell
    export TIDB_HOST='{host}'  # e.g. gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    export TIDB_PORT='4000'
    export TIDB_USER='{user}'  # e.g. xxxxxx.root
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='true'
    ```

    必ずプレースホルダー`{}`を、接続ダイアログから取得した接続パラメータに置き換えてください。

    TiDB Cloud Starter は安全な接続を必要とします。そのため、 `USE_SSL`の値を`true`に設定する必要があります。

7.  `env.sh`ファイルを保存します。

</div>
<div label="TiDB Cloud Premium">

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud Premiumインスタンスの名前をクリックして概要ページに移動します。

2.  左側のナビゲーションペインで、 **[設定]** &gt; **[ネットワーク]**をクリックします。

3.  **ネットワークの**ページで、 **[パブリックエンドポイント****を有効にする]**をクリックし、次に**[IP アドレスの追加]**をクリックします。

    クライアントのIPアドレスがアクセスリストに追加されていることを確認してください。

4.  左側のナビゲーションペインで**「概要」**をクリックすると、インスタンスの概要ページに戻ります。

5.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

6.  接続ダイアログで、 **「接続タイプ」**ドロップダウンリストから**「パブリック」**を選択します。

    -   公開エンドポイントがまだ有効化中であることを示すメッセージが表示された場合は、処理が完了するまでお待ちください。
    -   まだパスワードを設定していない場合は、ダイアログの**「ルートパスワードを設定」**をクリックしてください。
    -   サーバー証明書を確認する必要がある場合、または接続に失敗して認証局（CA）証明書が必要な場合は、 **「CA証明書」**をクリックしてダウンロードしてください。
    -   **パブリック**接続タイプに加えて、 TiDB Cloud Premium は**プライベート エンドポイント**接続をサポートします。詳細については、 [AWS PrivateLink経由でTiDB Cloud Premiumに接続します。](/tidb-cloud/premium/connect-to-premium-via-aws-private-endpoint.md)を参照してください。

7.  `env.sh.example`をコピーして`env.sh`に名前を変更するには、次のコマンドを実行します。

    ```shell
    cp env.sh.example env.sh
    ```

8.  対応する接続​​文字列`env.sh`ファイルにコピー＆ペーストしてください。例は以下のとおりです。

    ```shell
    export TIDB_HOST='{host}'  # e.g. tidb.xxxx.clusters.tidb-cloud.com
    export TIDB_PORT='4000'
    export TIDB_USER='{user}'  # e.g. root
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='false'
    ```

    必ずプレースホルダー`{}`を、接続ダイアログから取得した接続パラメータに置き換えてください。

9.  `env.sh`ファイルを保存します。

</div>
<div label="TiDB Cloud Dedicated">

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud Dedicatedクラスタの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  接続ダイアログで、「**接続タイプ」**ドロップダウンリストから**「パブリック」**を選択し、 **「CA証明書」**をクリックしてCA証明書をダウンロードします。

    IP アクセス リストを設定していない場合は、最初の接続の前に、 **[IP アクセス リストの設定] をクリックするか、「IP アクセス リストを設定する」**の手順に従って[IPアクセスリストを設定する](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)。

    TiDB Cloud Dedicated は、**パブリック**接続タイプに加えて、**プライベート エンドポイント**および**VPC ピアリング**接続タイプもサポートしています。詳細については、 [TiDB Cloud Dedicatedクラスタに接続します](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)参照してください。

4.  `env.sh.example`をコピーして`env.sh`に名前を変更するには、次のコマンドを実行します。

    ```shell
    cp env.sh.example env.sh
    ```

5.  対応する接続​​文字列`env.sh`ファイルにコピー＆ペーストしてください。例は以下のとおりです。

    ```shell
    export TIDB_HOST='{host}'  # e.g. tidb.xxxx.clusters.tidb-cloud.com
    export TIDB_PORT='4000'
    export TIDB_USER='{user}'  # e.g. root
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='false'
    ```

    必ずプレースホルダー`{}`を、接続ダイアログから取得した接続パラメータに置き換えてください。

6.  `env.sh`ファイルを保存します。

</div>
<div label="TiDB Self-Managed" value="tidb">

1.  `env.sh.example`をコピーして`env.sh`に名前を変更するには、次のコマンドを実行します。

    ```shell
    cp env.sh.example env.sh
    ```

2.  対応する接続​​文字列`env.sh`ファイルにコピー＆ペーストしてください。例は以下のとおりです。

    ```shell
    export TIDB_HOST='{host}'
    export TIDB_PORT='4000'
    export TIDB_USER='root'
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='false'
    ```

    プレースホルダー`{}`を接続パラメータに置き換え、 `USE_SSL` `false`に設定してください。TiDB をローカルで実行している場合、デフォルトのホスト アドレスは`127.0.0.1`で、パスワードは空です。

3.  `env.sh`ファイルを保存します。

</div>
</SimpleTab>

### ステップ3：コードを実行して結果を確認する {#step-3-run-the-code-and-check-the-result}

1.  サンプルコードを実行するには、以下のコマンドを実行してください。

    ```shell
    make
    ```

2.  [期待される出力.txt](https://github.com/tidb-samples/tidb-java-hibernate-quickstart/blob/main/Expected-Output.txt)をチェックして、出力が一致するかどうかを確認してください。

## サンプルコードスニペット {#sample-code-snippets}

以下のサンプルコードスニペットを参考に、独自のアプリケーション開発を完成させてください。

完全なサンプルコードと実行方法については、 [tidb-samples/tidb-java-hibernate-quickstart](https://github.com/tidb-samples/tidb-java-hibernate-quickstart)リポジトリを参照してください。

### TiDBに接続する {#connect-to-tidb}

Hibernateの設定ファイル`hibernate.cfg.xml`を編集します。

```xml
<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE hibernate-configuration PUBLIC
        "-//Hibernate/Hibernate Configuration DTD 3.0//EN"
        "http://www.hibernate.org/dtd/hibernate-configuration-3.0.dtd">
<hibernate-configuration>
    <session-factory>

        <!-- Database connection settings -->
        <property name="hibernate.connection.driver_class">com.mysql.cj.jdbc.Driver</property>
        <property name="hibernate.dialect">org.hibernate.dialect.MySQLDialect</property>
        <property name="hibernate.connection.url">${tidb_jdbc_url}</property>
        <property name="hibernate.connection.username">${tidb_user}</property>
        <property name="hibernate.connection.password">${tidb_password}</property>
        <property name="hibernate.connection.autocommit">false</property>

        <!-- Required so a table can be created from the 'PlayerDAO' class -->
        <property name="hibernate.hbm2ddl.auto">create-drop</property>

        <!-- Optional: Show SQL output for debugging -->
        <property name="hibernate.show_sql">true</property>
        <property name="hibernate.format_sql">true</property>
    </session-factory>
</hibernate-configuration>
```

`${tidb_jdbc_url}` 、 `${tidb_user}` 、および`${tidb_password}`を、ご使用のTiDBの実際の値に置き換えてください。次に、以下の関数を定義します。

```java
public SessionFactory getSessionFactory() {
    return new Configuration()
            .configure("hibernate.cfg.xml")
            .addAnnotatedClass(${your_entity_class})
            .buildSessionFactory();
}
```

この関数を使用する際は、 `${your_entity_class}`独自のデータエンティティクラスに置き換える必要があります。複数のエンティティクラスを使用する場合は、それぞれに`.addAnnotatedClass(${your_entity_class})`ステートメントを追加する必要があります。上記の関数は、Hibernate を設定する方法の 1 つにすぎません。設定で問題が発生した場合、または Hibernate についてさらに詳しく知りたい場合は、 [Hibernateの公式ドキュメント](https://hibernate.org/orm/documentation)を参照してください。

### データを挿入または更新する {#insert-or-update-data}

```java
try (Session session = sessionFactory.openSession()) {
    session.persist(new PlayerBean("id", 1, 1));
}
```

詳細については、[データを挿入する](/develop/dev-guide-insert-data.md)[データの更新](/develop/dev-guide-update-data.md)を参照してください。

### クエリデータ {#query-data}

```java
try (Session session = sessionFactory.openSession()) {
    PlayerBean player = session.get(PlayerBean.class, "id");
    System.out.println(player);
}
```

詳細については、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データを削除する {#delete-data}

```java
try (Session session = sessionFactory.openSession()) {
    session.remove(new PlayerBean("id", 1, 1));
}
```

詳細については、[データを削除する](/develop/dev-guide-delete-data.md)を参照してください。

## <code>MySQLDialect</code>との互換性 {#compatibility-with-code-mysqldialect-code}

TiDB で`MySQLDialect`を使用する場合は、以下の動作に注意してください。

### <code>SERIALIZABLE</code>分離レベル {#code-serializable-code-isolation-level}

TiDB で`SERIALIZABLE`トランザクション分離レベルを設定しようとするアプリケーションは、次のエラーに遭遇します。

    The isolation level 'SERIALIZABLE' is not supported. Set tidb_skip_isolation_level_check=1 to skip this error

このエラーを回避するには、サーバー側で以下のTiDBシステム変数を設定してください。

```sql
SET GLOBAL tidb_skip_isolation_level_check=1;
```

この変数を有効にすると、TiDB は`SERIALIZABLE`を指定したリクエストをエラーを返さずに受け入れます。内部的には、TiDB は引き続き最も強力な分離レベルである`REPEATABLE-READ`を使用します。詳細については、 [`tidb_skip_isolation_level_check`](/system-variables.md#tidb_skip_isolation_level_check)参照してください。

> **注記：**
>
> コミュニティが管理する`TiDBDialect` `SERIALIZABLE`分離レベルを必要とする機能をスキップすることで、この動作を自動的に処理します。

### <code>CHECK</code>制約 {#code-check-code-constraints}

Hibernate の[`@Check`](https://docs.hibernate.org/orm/6.5/javadocs/org/hibernate/annotations/Check.html)アノテーションは、DDL `CHECK`制約を生成します。 [MySQL 8.0.16以降のバージョン](https://dev.mysql.com/doc/refman/8.0/en/create-table-check-constraints.html)では、これらの制約がデフォルトで強制されますが、TiDB は明示的に有効にされない限り、これらの制約を強制しません。

TiDBで`CHECK`制約の適用を有効にするには、次のシステム変数を設定します。

```sql
SET GLOBAL tidb_enable_check_constraint=ON;
```

この設定がない場合、TiDB は`CHECK`制約構文を受け入れますが、それを強制しないため、予期しないデータ整合性の問題が発生する可能性があります。詳細については、 [`CHECK`制約](/constraints.md#check)参照してください。 。

## 次のステップ {#next-steps}

-   Hibernate の使用法の詳細については[Hibernateのドキュメント](https://hibernate.org/orm/documentation)参照してください。
-   [開発者ガイド](https://docs.pingcap.com/developer/)[データを挿入する](/develop/dev-guide-insert-data.md)[データの更新](/develop/dev-guide-update-data.md)、[データを削除する](/develop/dev-guide-delete-data.md)、「SQL パフォーマンス最適化」などの章[単一表の読み取り](/develop/dev-guide-get-data-from-single-table.md)読んで、TiDB アプリケーション [取引](/develop/dev-guide-transaction-overview.md)[SQLパフォーマンス最適化](/develop/dev-guide-optimize-sql-overview.md)。
-   プロフェッショナルな[TiDB開発者向けコース](https://www.pingcap.com/education/)コースを通じて学習し、試験に合格すると[TiDB認定資格](https://www.pingcap.com/education/certification/)を取得します。
-   Java開発者向けのコース「 [JavaからTiDBを操作する](https://eng.edu.pingcap.com/catalog/info/id:212)を通じて学習します。

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)
