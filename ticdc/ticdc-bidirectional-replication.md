---
title: Bidirectional Replication
summary: TiCDC の双方向レプリケーションの使用方法を学習します。
---

# 双方向レプリケーション {#bidirectional-replication}

TiCDC は、2 つの TiDB クラスター間の双方向レプリケーション (BDR) をサポートします。この機能に基づいて、TiCDC を使用してマルチアクティブ TiDB ソリューションを作成できます。

このセクションでは、2 つの TiDB クラスターを例に、双方向レプリケーションを使用する方法について説明します。

## 双方向レプリケーションをデプロイ {#deploy-bi-directional-replication}

TiCDC は、指定されたタイムスタンプの後に発生した増分データ変更のみをダウンストリーム クラスターに複製します。双方向レプリケーションを開始する前に、次の手順を実行する必要があります。

1.  (オプション) 必要に応じて、データ エクスポート ツール[Dumpling](/dumpling-overview.md)とデータ インポート ツール[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)を使用して、2 つの TiDB クラスターのデータを相互にインポートします。

2.  2 つの TiDB クラスターの間に 2 つの TiCDC クラスターをデプロイ。クラスター トポロジは次のようになります。図の矢印はデータ フローの方向を示します。

    ![TiCDC bidirectional replication](/media/ticdc/ticdc-bidirectional-replication.png)

3.  アップストリーム クラスターとダウンストリーム クラスターのデータ レプリケーションの開始時点を指定します。

    1.  上流クラスターと下流クラスターの時点を確認します。2 つの TiDB クラスターの場合は、特定の時点で 2 つのクラスターのデータが一致していることを確認します。たとえば、 `ts=1`の TiDB A のデータと`ts=2`の TiDB B のデータは一致しています。

    2.  changefeed を作成するときは、上流クラスターの changefeed の`--start-ts`対応する`tso`に設定します。つまり、上流クラスターが TiDB A の場合は`--start-ts=1`を設定し、上流クラスターが TiDB B の場合は`--start-ts=2`を設定します。

4.  `--config`パラメータで指定された構成ファイルに、次の構成を追加します。

    ```toml
    # Whether to enable the bi-directional replication mode
    bdr-mode = true
    ```

構成が有効になると、クラスターは双方向のレプリケーションを実行できるようになります。

## DDL タイプ {#ddl-types}

v7.6.0 以降、双方向レプリケーションで DDL レプリケーションを可能な限りサポートするために、TiDB は、DDL がビジネスに与える影響に応じて、 [TiCDCが元々サポートしていたDDL](/ticdc/ticdc-ddl.md)レプリケート可能な DDL とレプリケート不可能な DDL の 2 種類に分割します。

### 複製可能な DDL {#replicable-ddls}

レプリケート可能な DDL は、直接実行して双方向レプリケーションで他の TiDB クラスターにレプリケートできる DDL です。

複製可能な DDL には次のものが含まれます。

-   `CREATE DATABASE`
-   `CREATE TABLE`
-   `ADD COLUMN` : 列は`null`になるか、 `not null`と`default value`が同時に存在する
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

### 複製不可能な DDL {#non-replicable-ddls}

複製不可能な DDL は、ビジネスに大きな影響を与え、クラスター間でデータの不整合を引き起こす可能性のある DDL です。複製不可能な DDL は、TiCDC を介した双方向レプリケーションで他の TiDB クラスターに直接複製することはできません。複製不可能な DDL は、特定の操作を通じて実行する必要があります。

複製不可能な DDL には次のものが含まれます。

-   `DROP DATABASE`
-   `DROP TABLE`
-   `ADD COLUMN` : 列は`not null`で`default value`ありません
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

複製可能な DDL と複製不可能な DDL の問題を解決するために、TiDB は次の BDR ロールを導入します。

-   `PRIMARY` : レプリケート可能な DDL は実行できますが、レプリケート不可能な DDL は実行できません。レプリケート可能な DDL は、TiCDC によってダウンストリームにレプリケートされます。
-   `SECONDARY` : レプリケート可能な DDL またはレプリケート不可能な DDL は実行できませんが、TiCDC によってレプリケートされた DDL は実行できます。

BDR ロールが設定されていない場合は、任意の DDL を実行できます。ただし、TiCDC で`bdr_mode=true`設定すると、実行された DDL は TiCDC によってレプリケートされなくなります。

> **警告：**
>
> この機能は実験的ものです。本番環境での使用は推奨されません。この機能は予告なしに変更または削除される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)報告できます。

### 複製可能な DDL のレプリケーション シナリオ {#replication-scenarios-of-replicable-ddls}

1.  TiDB クラスターを選択し、 `ADMIN SET BDR ROLE PRIMARY`実行してそれをプライマリ クラスターとして設定します。
2.  他の TiDB クラスターでは、 `ADMIN SET BDR ROLE SECONDARY`実行してそれらをセカンダリ クラスターとして設定します。
3.  プライマリ クラスターで**複製可能な DDL を**実行します。正常に実行された DDL は、TiCDC によってセカンダリ クラスターに複製されます。

> **注記：**
>
> 不正使用を防ぐために：
>
> -   プライマリ クラスターで**複製不可能な DDL**を実行しようとすると、 [エラー 8263](/error-codes.md)が返されます。
> -   セカンダリ クラスターで**レプリケート可能な DDL**または**レプリケート不可能な DDL を**実行しようとすると、 [エラー 8263](/error-codes.md)が返されます。

### 複製不可能な DDL の複製シナリオ {#replication-scenarios-of-non-replicable-ddls}

1.  すべての TiDB クラスターで`ADMIN UNSET BDR ROLE`実行して、BDR ロールを設定解除します。
2.  すべてのクラスターで DDL を実行する必要があるテーブルへのデータの書き込みを停止します。
3.  すべてのクラスター内の対応するテーブルへのすべての書き込みが他のクラスターに複製されるまで待機し、各 TiDB クラスターですべての DDL を手動で実行します。
4.  DDL が完了するまで待ってから、データの書き込みを再開します。
5.  [複製可能な DDL のレプリケーション シナリオ](#replication-scenarios-of-replicable-ddls)の手順に従って、レプリケート可能な DDL のレプリケーション シナリオに戻ります。

> **警告：**
>
> すべての TiDB クラスターで`ADMIN UNSET BDR ROLE`実行すると、TiCDC によって DDL はレプリケートされません。各クラスターで個別に DDL を手動で実行する必要があります。

## 双方向レプリケーションを停止する {#stop-bi-directional-replication}

アプリケーションがデータの書き込みを停止した後、各クラスターに特別なレコードを挿入できます。 2 つの特別なレコードをチェックすることで、2 つのクラスターのデータが一貫していることを確認できます。

チェックが完了したら、changefeed を停止して双方向レプリケーションを停止し、すべての TiDB クラスターで`ADMIN UNSET BDR ROLE`実行できます。

## 制限事項 {#limitations}

-   BDR ロールは次のシナリオでのみ使用してください。

    -   1 `PRIMARY`クラスターと n `SECONDARY`クラスター (複製可能な DDL のレプリケーション シナリオ)

    -   BDR ロールを持たない n 個のクラスタ (各クラスタで複製不可能な DDL を手動で実行できるレプリケーション シナリオ)

    > **注記：**
    >
    > 他のシナリオでは BDR ロールを設定しないでください。たとえば、同時に`PRIMARY` 、 `SECONDARY` 、および BDR ロールなしを設定します。BDR ロールを誤って設定すると、TiDB はデータ レプリケーション中にデータの正確性と一貫性を保証できません。

-   通常、レプリケートされたテーブルでデータの競合を避けるため、 `AUTO_INCREMENT`または`AUTO_RANDOM`使用しないでください。 `AUTO_INCREMENT`または`AUTO_RANDOM`使用する必要がある場合は、異なるクラスターに異なる主キーを割り当てることができるように、異なるクラスターに異なる`auto_increment_increment`と`auto_increment_offset`設定できます。 たとえば、双方向レプリケーションに 3 つの TiDB クラスター (A、B、C) がある場合、次のように設定できます。

    -   クラスタAでは、 `auto_increment_increment=3`と`auto_increment_offset=2000`設定します
    -   クラスタBでは、 `auto_increment_increment=3`と`auto_increment_offset=2001`設定します
    -   クラスタCでは、 `auto_increment_increment=3`と`auto_increment_offset=2002`設定します

    この方法では、暗黙的に割り当てられた`AUTO_INCREMENT` ID と`AUTO_RANDOM` ID で A、B、C が競合することはありません。BDR モードでクラスターを追加する必要がある場合は、関連アプリケーションのデータの書き込みを一時的に停止し、すべてのクラスターで`auto_increment_increment`と`auto_increment_offset`に適切な値を設定してから、関連アプリケーションのデータの書き込みを再開する必要があります。

-   双方向レプリケーション クラスターは書き込み競合を検出できないため、未定義の動作が発生する可能性があります。したがって、アプリケーション側から書き込み競合がないことを確認する必要があります。

-   双方向レプリケーションは 2 つ以上のクラスターをサポートしますが、カスケード モードの複数のクラスター、つまり TiDB A -&gt; TiDB B -&gt; TiDB C -&gt; TiDB A のような循環レプリケーションはサポートしません。このようなトポロジでは、1 つのクラスターに障害が発生すると、データ レプリケーション全体が影響を受けます。したがって、複数のクラスター間で双方向レプリケーションを有効にするには、各クラスターを他のすべてのクラスター`TiDB C <-> TiDB A`例: `TiDB A <-> TiDB B` `TiDB B <-> TiDB C`に接続する必要があります。
