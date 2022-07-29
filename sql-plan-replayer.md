---
title: Use PLAN REPLAYER to Save and Restore the On-Site Information of a Cluster
summary: Learn how to use PLAN REPLAYER to save and restore the on-site information of a cluster.
---

# PLAN REPLAYERを使用して、クラスターのオンサイト情報を保存および復元します {#use-plan-replayer-to-save-and-restore-the-on-site-information-of-a-cluster}

TiDBクラスタの問題を見つけてトラブルシューティングするときは、多くの場合、システムと実行プランに関する情報を提供する必要があります。より便利で効率的な方法で情報を取得し、クラスタの問題をトラブルシューティングするのに役立つように、 `PLAN REPLAYER`コマンドがTiDBv5.3.0に導入されました。このコマンドを使用すると、クラスタのオンサイト情報を簡単に保存および復元でき、トラブルシューティングの効率が向上し、管理のために問題をより簡単にアーカイブできます。

`PLAN REPLAYER`の特徴は次のとおりです。

-   オンサイトトラブルシューティングでのTiDBクラスタの情報をZIP形式のファイルにエクスポートして保存します。
-   別のTiDBクラスタからエクスポートされたZIP形式のファイルをクラスタにインポートします。このファイルには、オンサイトトラブルシューティングでの後者のTiDBクラスタの情報が含まれています。

## <code>PLAN REPLAER</code>を使用してクラスタ情報をエクスポートします {#use-code-plan-replaer-code-to-export-cluster-information}

`PLAN REPLAYER`を使用して、TiDBクラスタのオンサイト情報を保存できます。エクスポートインターフェイスは次のとおりです。

{{< copyable "" >}}

```sql
PLAN REPLAYER DUMP EXPLAIN [ANALYZE] sql-statement;
```

`sql-statement`に基づいて、TiDBは次のオンサイト情報を分類してエクスポートします。

-   TiDBバージョン
-   TiDB構成
-   TiDBセッション変数
-   TiDB SQLバインディング
-   `sql-statement`のテーブルスキーマ
-   `sql-statement`のテーブルの統計
-   `EXPLAIN [ANALYZE] sql-statement`の結果

> **ノート：**
>
> `PLAN REPLAYER`テーブルデータをエクスポートし**ません**。

### クラスタ情報のエクスポートの例 {#examples-of-exporting-cluster-information}

{{< copyable "" >}}

```sql
use test;
create table t(a int, b int);
insert into t values(1,1), (2, 2), (3, 3);
analyze table t;

plan replayer dump explain select * from t;
```

`PLAN REPLAYER DUMP`は、上記のテーブル情報を`ZIP`ファイルにパッケージ化し、実行結果としてファイル識別子を返します。このファイルは1回限りのファイルです。ファイルがダウンロードされた後、TiDBはそれを削除します。

> **ノート：**
>
> `ZIP`のファイルは最大1時間TiDBクラスタに保存されます。 1時間後、TiDBはそれを削除します。

```sql
MySQL [test]> plan replayer dump explain select * from t;
+------------------------------------------------------------------+
| Dump_link                                                        |
+------------------------------------------------------------------+
| replayer_single_JOGvpu4t7dssySqJfTtS4A==_1635750890568691080.zip |
+------------------------------------------------------------------+
1 row in set (0.015 sec)
```

ファイルはMySQLクライアントにダウンロードできないため、ファイルをダウンロードするには、TiDBHTTPインターフェイスとファイル識別子を使用する必要があります。

{{< copyable "" >}}

```shell
http://${tidb-server-ip}:${tidb-server-status-port}/plan_replayer/dump/${file_token}
```

`${tidb-server-ip}:${tidb-server-status-port}`は、クラスタの任意のTiDBサーバーのアドレスです。例えば：

{{< copyable "" >}}

```shell
curl http://127.0.0.1:10080/plan_replayer/dump/replayer_single_JOGvpu4t7dssySqJfTtS4A==_1635750890568691080.zip > plan_replayer.zip
```

## <code>PLAN REPLAYER</code>を使用してクラスタ情報をインポートします {#use-code-plan-replayer-code-to-import-cluster-information}

> **警告：**
>
> TiDBクラスタのオンサイト情報を別のクラスタにインポートすると、TiDBセッション変数、SQLバインディング、テーブルスキーマ、および後者のクラスタの統計が変更されます。

`PLAN REPLAYER`を使用してエクスポートされた既存の`ZIP`ファイルを使用して、 `PLAN REPLAYER`インポートインターフェイスを使用して、クラスタのオンサイト情報を他のTiDBクラスタに復元できます。構文は次のとおりです。

{{< copyable "" >}}

```sql
PLAN REPLAYER LOAD 'file_name';
```

上記のステートメントで、 `file_name`はエクスポートされる`ZIP`のファイルの名前です。

例えば：

{{< copyable "" >}}

```sql
PLAN REPLAYER LOAD 'plan_replayer.zip';
```
