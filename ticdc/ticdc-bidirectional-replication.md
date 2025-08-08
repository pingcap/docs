---
title: Bidirectional Replication
summary: TiCDC の双方向レプリケーションの使用方法を学習します。
---

# 双方向レプリケーション {#bidirectional-replication}

TiCDCは、2つのTiDBクラスタ間の双方向レプリケーション（BDR）をサポートしています。この機能を利用することで、TiCDCを使用したマルチアクティブTiDBソリューションを構築できます。

このセクションでは、2 つの TiDB クラスターを例にして双方向レプリケーションを使用する方法について説明します。

## 双方向レプリケーションをデプロイ {#deploy-bi-directional-replication}

TiCDCは、指定されたタイムスタンプ以降に発生した増分データ変更のみを下流クラスターに複製します。双方向レプリケーションを開始する前に、次の手順を実行する必要があります。

1.  (オプション) 必要に応じて、データ エクスポート ツール[Dumpling](/dumpling-overview.md)とデータ インポート ツール[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)を使用して、2 つの TiDB クラスターのデータを相互にインポートします。

2.  2つのTiDBクラスターの間に2つのTiCDCクラスターをデプロイ。クラスタートポロジは以下のとおりです。図中の矢印はデータフローの方向を示しています。

    ![TiCDC bidirectional replication](/media/ticdc/ticdc-bidirectional-replication.png)

3.  アップストリーム クラスターとダウンストリーム クラスターのデータ複製の開始時点を指定します。

    1.  上流クラスタと下流クラスタの時点を確認します。2つのTiDBクラスタがある場合、特定の時点において2つのクラスタのデータが整合していることを確認します。例えば、TiDB Aの`ts=1`のデータとTiDB Bの`ts=2`のデータは整合しています。

    2.  changefeed を作成する際、上流クラスターの changefeed の`--start-ts`対応する`tso`に設定します。つまり、上流クラスターが TiDB A の場合は`--start-ts=1` 、上流クラスターが TiDB B の場合は`--start-ts=2`設定します。

4.  `--config`パラメータで指定された構成ファイルに、次の構成を追加します。

    ```toml
    # Whether to enable the bi-directional replication mode
    bdr-mode = true
    ```

構成が有効になると、クラスターは双方向のレプリケーションを実行できるようになります。

## DDL型 {#ddl-types}

v7.6.0 以降、双方向レプリケーションで DDL レプリケーションを可能な限りサポートするために、TiDB は、DDL がビジネスに与える影響に応じて、DDL をレプリケート可能な DDL とレプリケート不可能な DDL の[TiCDCが元々サポートしていたDDL](/ticdc/ticdc-ddl.md)種類に分割します。

### 複製可能なDDL {#replicable-ddls}

レプリケート可能な DDL は、直接実行して双方向レプリケーションで他の TiDB クラスターにレプリケートできる DDL です。

レプリケート可能な DDL には次のものが含まれます。

-   `CREATE DATABASE`
-   `CREATE TABLE`
-   `ADD COLUMN` : 列は`null`になるか、同時に`not null`と`default value`になります
-   `ADD NON-UNIQUE INDEX`
-   `DROP INDEX`
-   `MODIFY COLUMN` : 列の`default value`と`comment`のみ変更できます
-   `ALTER COLUMN DEFAULT VALUE`
-   `MODIFY TABLE COMMENT`
-   `RENAME INDEX`
-   `ADD TABLE PARTITION`
-   `DROP PRIMARY KEY`
-   `ALTER TABLE INDEX VISIBILITY`
-   `ALTER TABLE TTL`
-   `ALTER TABLE REMOVE TTL`
-   `CREATE VIEW`
-   `DROP VIEW`

### 複製不可能なDDL {#non-replicable-ddls}

複製不可能なDDLは、ビジネスに大きな影響を与え、クラスタ間のデータ不整合を引き起こす可能性のあるDDLです。複製不可能なDDLは、TiCDCを介した双方向レプリケーションにおいて、他のTiDBクラスタに直接複製することはできません。複製不可能なDDLは、特定の操作を通じて実行する必要があります。

レプリケートできない DDL には次のものが含まれます。

-   `DROP DATABASE`
-   `DROP TABLE`
-   `ADD COLUMN` : 列は`not null`で、 `default value`はありません
-   `DROP COLUMN`
-   `ADD UNIQUE INDEX`
-   `TRUNCATE TABLE`
-   `MODIFY COLUMN` : `default value`と`comment`除く列の属性を変更できます
-   `RENAME TABLE`
-   `DROP PARTITION`
-   `TRUNCATE PARTITION`
-   `ALTER TABLE CHARACTER SET`
-   `ALTER DATABASE CHARACTER SET`
-   `RECOVER TABLE`
-   `ADD PRIMARY KEY`
-   `REBASE AUTO ID`
-   `EXCHANGE PARTITION`
-   `REORGANIZE PARTITION`

## DDLレプリケーション {#ddl-replication}

レプリケート可能な DDL とレプリケート不可能な DDL の問題を解決するために、TiDB は次の BDR ロールを導入します。

-   `PRIMARY` : レプリケート可能なDDLは実行できますが、レプリケート不可能なDDLは実行できません。プライマリクラスターで実行されたレプリケート可能なDDLは、TiCDCによってダウンストリームにレプリケートされます。
-   `SECONDARY` ：レプリケート可能なDDLもレプリケート不可能なDDLも実行できません。ただし、プライマリクラスターで実行されたDDLは、TiCDCによってセカンダリクラスターにレプリケートできます。

BDRロールが設定されていない場合、任意のDDLを実行できます。ただし、BDRモードの変更フィードでは、そのクラスター上のDDLはレプリケートされません。

つまり、BDR モードでは、TiCDC はプライマリ クラスター内の複製可能な DDL のみをダウンストリームに複製します。

### 複製可能なDDLのレプリケーションシナリオ {#replication-scenarios-of-replicable-ddls}

1.  TiDB クラスターを選択し、 `ADMIN SET BDR ROLE PRIMARY`実行してそれをプライマリ クラスターとして設定します。

    ```sql
    ADMIN SET BDR ROLE PRIMARY;
    Query OK, 0 rows affected
    Time: 0.003s

    ADMIN SHOW BDR ROLE;
    +----------+
    | BDR_ROLE |
    +----------+
    | primary  |
    +----------+
    ```

2.  他の TiDB クラスターで`ADMIN SET BDR ROLE SECONDARY`実行して、それらをセカンダリ クラスターとして設定します。

3.  プライマリクラスターで**レプリケート可能なDDL**を実行します。正常に実行されたDDLは、TiCDCによってセカンダリクラスターにレプリケートされます。

> **注記：**
>
> 不正使用を防ぐために:
>
> -   プライマリ クラスターで**レプリケートできない DDL**を実行しようとすると、 [エラー8263](/error-codes.md)返されます。
> -   セカンダリ クラスターで**レプリケート可能な DDL**または**レプリケート不可能な DDL**を実行しようとすると、 [エラー8263](/error-codes.md)返されます。

### 複製不可能なDDLのレプリケーションシナリオ {#replication-scenarios-of-non-replicable-ddls}

1.  すべての TiDB クラスターで`ADMIN UNSET BDR ROLE`実行して、BDR ロールを設定解除します。
2.  すべてのクラスターで DDL を実行する必要があるテーブルへのデータの書き込みを停止します。
3.  すべてのクラスター内の対応するテーブルへのすべての書き込みが他のクラスターに複製されるまで待機し、各 TiDB クラスターですべての DDL を手動で実行します。
4.  DDL が完了するまで待ってから、データの書き込みを再開します。
5.  レプリケート可能な DDL のレプリケーション シナリオに戻すには、手順[複製可能なDDLのレプリケーションシナリオ](#replication-scenarios-of-replicable-ddls)に従います。

> **警告：**
>
> すべてのTiDBクラスターで`ADMIN UNSET BDR ROLE`実行すると、TiCDCによってDDLは複製されません。各クラスターで個別にDDLを手動で実行する必要があります。

## 双方向レプリケーションを停止する {#stop-bi-directional-replication}

アプリケーションがデータの書き込みを停止した後、各クラスタに特別なレコードを挿入できます。2つの特別なレコードをチェックすることで、2つのクラスタ内のデータの整合性を確認できます。

チェックが完了したら、変更フィードを停止して双方向レプリケーションを停止し、すべての TiDB クラスターで`ADMIN UNSET BDR ROLE`実行できます。

## 制限事項 {#limitations}

-   BDR ロールは次のシナリオでのみ使用してください。

    -   1 `PRIMARY`クラスタと n `SECONDARY`クラスタ（複製可能な DDL のレプリケーション シナリオ）

    -   BDR ロールを持たない n 個のクラスタ（各クラスタで複製不可能な DDL を手動で実行できるレプリケーション シナリオ）

    > **注記：**
    >
    > 他のシナリオではBDRロールを設定しないでください。例えば、BDRロールを`PRIMARY` 、 `SECONDARY` 、そして0つを同時に設定しないでください。BDRロールを誤って設定すると、TiDBはデータレプリケーション中にデータの正確性と一貫性を保証できません。

-   通常、レプリケートされたテーブルでのデータ競合を避けるため、 `AUTO_INCREMENT`または`AUTO_RANDOM`使用しないでください。5 または`AUTO_INCREMENT` `AUTO_RANDOM`使用する必要がある場合は、異なるクラスタに異なる主キーを割り当てることができるように、異なるクラスタに異なる`auto_increment_increment`と`auto_increment_offset`設定できます。例えば、双方向レプリケーションに3つのTiDBクラスタ（A、B、C）がある場合、次のように設定します。

    -   クラスタAでは、 `auto_increment_increment=3`と`auto_increment_offset=2000`を設定します
    -   クラスタBでは`auto_increment_increment=3`と`auto_increment_offset=2001`設定します
    -   クラスタCでは、 `auto_increment_increment=3`と`auto_increment_offset=2002`設定します

    これにより、A、B、Cは暗黙的に割り当てられた`AUTO_INCREMENT`と`AUTO_RANDOM`で互いに競合することがなくなります。BDRモードでクラスターを追加する必要がある場合は、関連アプリケーションのデータ書き込みを一時的に停止し、すべてのクラスターの`auto_increment_increment`と`auto_increment_offset`に適切な値を設定してから、関連アプリケーションのデータ書き込みを再開する必要があります。

-   双方向レプリケーションクラスタは書き込み競合を検出できないため、未定義の動作が発生する可能性があります。そのため、アプリケーション側で書き込み競合がないことを確認する必要があります。

-   双方向レプリケーションは2つ以上のクラスタをサポートしますが、カスケードモード、つまりTiDB A -&gt; TiDB B -&gt; TiDB C -&gt; TiDB Aのような循環的なレプリケーションはサポートしません。このようなトポロジでは、1つのクラスタに障害が発生すると、データレプリケーション全体に影響が出ます。したがって、複数のクラスタ間で双方向レプリケーションを実現するには、各クラスタを他のすべてのクラスタ（例： `TiDB A <-> TiDB B` `TiDB C <-> TiDB A`に接続する必要があります`TiDB B <-> TiDB C`
