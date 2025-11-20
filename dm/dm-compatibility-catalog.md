---
title: Compatibility Catalog of TiDB Data Migration
summary: このドキュメントでは、TiDB データ移行 (DM) とアップストリーム データベースおよびダウンストリーム データベースとの互換性について説明します。
---

# TiDBデータ移行の互換性カタログ {#compatibility-catalog-of-tidb-data-migration}

DMは、異なるソースからTiDBクラスタへのデータ移行をサポートします。データソースの種類に基づいて、DMには4つの互換性レベルがあります。

-   **一般公開 (GA)** : アプリケーション シナリオが検証され、GA テストに合格しました。
-   **Experimental**：一般的なアプリケーションシナリオは検証済みですが、対象範囲が限定されているか、対象ユーザーが少数に限られています。時折問題が発生する可能性があるため、特定のシナリオにおける互換性を検証する必要があります。
-   **未テスト**：DMはMySQLプロトコルおよびbinlogとの互換性を目指しています。ただし、すべてのMySQLフォークまたはバージョンがDMテストマトリックスに含まれているわけではありません。フォークまたはバージョンがMySQL互換プロトコルおよびbinlog形式を使用している場合、動作することが期待されますが、使用前にご自身の環境で互換性を確認する必要があります。
-   **互換性なし**: DM には既知のブロッキング問題があるため、本番での使用は推奨されません。

## データソース {#data-sources}

| データソース                   | 互換性レベル       | 注記                                                                                                                               |
| ------------------------ | ------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| MySQL ≤ 5.5              | テストされていません   |                                                                                                                                  |
| MySQL 5.6                | GA           |                                                                                                                                  |
| MySQL 5.7                | GA           |                                                                                                                                  |
| MySQL 8.0                | GA           | binlogトランザクション圧縮[トランザクションペイロードイベント](https://dev.mysql.com/doc/refman/8.0/en/binary-log-transaction-compression.html)をサポートしていません。 |
| MySQL 8.1 ～ 8.3          | テストされていません   |                                                                                                                                  |
| MySQL 8.4                | 互換性がない       | 詳細については[DM 発行 #11020](https://github.com/pingcap/tiflow/issues/11020)参照してください。                                                   |
| MySQL 9.x                | テストされていません   |                                                                                                                                  |
| MariaDB &lt; 10.1.2      | 互換性がない       | 時間タイプのbinlogとは互換性がありません。                                                                                                         |
| MariaDB 10.1.2 ～ 10.5.10 | Experimental |                                                                                                                                  |
| MariaDB &gt; 10.5.10     | テストされていません   | [事前チェック](/dm/dm-precheck.md)をバイパスした後、ほとんどの場合に機能すると予想されます[MariaDB ノート](#mariadb-notes)参照してください。                                   |

### 外部キーCASCADE操作との非互換性 {#incompatibility-with-foreign-key-cascade-operations}

-   DM はターゲットに外部キー**制約**を作成しますが、DM はセッション変数[`foreign_key_checks=OFF`](/system-variables.md#foreign_key_checks)を設定するため、トランザクションの適用中に外部キー制約は適用されません。
-   DM はデフォルトでは`ON DELETE CASCADE`または`ON UPDATE CASCADE`動作をサポートして**いません**。また、DM タスクセッション変数を使用して`foreign_key_checks`有効にすることは推奨されません。ワークロードがカスケードに依存している場合、カスケード効果が複製されると**想定しないでください**。

### MariaDB ノート {#mariadb-notes}

-   MariaDB **10.5.11以降**では、権限名の変更（例： `BINLOG MONITOR` `REPLICATION MASTER ADMIN`によりDM**事前チェックが失敗します**。レプリケーション権限、ダンプ権限、ダンプ接続番号チェッカーでは`REPLICATION SLAVE ADMIN`エラーは`[code=26005] fail to check synchronization configuration`として表示されます。
-   DMタスクに`ignore-checking-items: ["all"]`追加することで、**事前チェックをバイパス**できます。詳細は[DM事前チェック](/dm/dm-precheck.md)参照してください。

## 対象データベース {#target-databases}

> **警告：**
>
> DM v5.3.0 は推奨されません。DM v5.3.0 でリレーログなしで GTID レプリケーションを有効にすると、低い確率ではありますが、データレプリケーションが失敗する可能性があります。

| ターゲットデータベース | 互換性レベル       | DMバージョン           |
| ----------- | ------------ | ----------------- |
| TiDB 8.x    | GA           | ≥ 5.3.1           |
| TiDB 7.x    | GA           | ≥ 5.3.1           |
| TiDB 6.x    | GA           | ≥ 5.3.1           |
| TiDB 5.4    | GA           | ≥ 5.3.1           |
| TiDB 5.3    | GA           | ≥ 5.3.1           |
| TiDB 5.2    | GA           | ≥ 2.0.7、推奨: 5.4   |
| TiDB 5.1    | GA           | ≥ 2.0.4、推奨: 5.4   |
| TiDB 5.0    | GA           | ≥ 2.0.4、推奨: 5.4   |
| TiDB 4.x    | GA           | ≥ 2.0.1、推奨: 2.0.7 |
| TiDB 3.x    | GA           | ≥ 2.0.1、推奨: 2.0.7 |
| MySQL       | Experimental |                   |
| マリアDB       | Experimental |                   |
