---
title: Compatibility Catalog of TiDB Data Migration
summary: このドキュメントでは、TiDBデータ移行（DM）と上流および下流データベースとの互換性について説明します。
---

# TiDBデータ移行の互換性カタログ {#compatibility-catalog-of-tidb-data-migration}

DMは、さまざまなソースからTiDBクラスタへのデータ移行をサポートしています。データソースの種類に基づいて、DMには4つの互換性レベルがあります。

-   **一般提供開始（GA）** ：アプリケーションシナリオが検証され、GAテストに合格しました。
-   **Experimental**：一般的なアプリケーションシナリオは検証済みですが、対象範囲は限定的であるか、ごく少数のユーザーのみが対象となっています。まれに問題が発生する可能性があるため、ご使用のシナリオにおける互換性を確認する必要があります。
-   **未テスト**：DMはMySQLプロトコルおよびbinlogとの互換性を目指していますが、DMのテストマトリックスにはすべてのMySQLフォークやバージョンが含まれているわけではありません。フォークやバージョンがMySQL互換のプロトコルとbinlogフォーマットを使用している場合は動作するはずですが、使用前にご自身の環境で互換性を確認する必要があります。
-   **互換性なし**：DMには既知のブロッキング問題があるため、本番での使用は推奨されません。

## データソース {#data-sources}

| データソース                   | 互換性レベル                           | 注記                                                                                                                                           |
| ------------------------ | -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| MySQL ≤ 5.5              | テストされていません                       |                                                                                                                                              |
| MySQL 5.6                | GA                               |                                                                                                                                              |
| MySQL 5.7                | GA                               |                                                                                                                                              |
| MySQL 8.0                | GA                               | [binlogトランザクション圧縮（ `Transaction_payload_event` ）](https://dev.mysql.com/doc/refman/8.0/en/binary-log-transaction-compression.html)はサポートしません。 |
| MySQL 8.1～8.3            | テストされていません                       | [binlogトランザクション圧縮（ `Transaction_payload_event` ）](https://dev.mysql.com/doc/refman/8.0/en/binary-log-transaction-compression.html)はサポートしません。 |
| MySQL 8.4                | Experimental（TiDB v8.5.6以降でサポート） | [binlogトランザクション圧縮（ `Transaction_payload_event` ）](https://dev.mysql.com/doc/refman/8.4/en/binary-log-transaction-compression.html)はサポートしません。 |
| MySQL 9.x                | テストされていません                       |                                                                                                                                              |
| MariaDB &lt; 10.1.2      | 互換性がない                           | 時間型のbinlogとは互換性がありません。                                                                                                                       |
| MariaDB 10.1.2 ～ 10.5.10 | Experimental                     |                                                                                                                                              |
| MariaDB &gt; 10.5.10     | テストされていません                       | [事前チェック](/dm/dm-precheck.md)をバイパスした後は、ほとんどの場合に機能すると予想されます。 [MariaDBに関する注記](#mariadb-notes)参照してください。                                          |

### 外部キーの<code>CASCADE</code>操作 {#foreign-key-code-cascade-code-operations}

> **警告：**
>
> この機能は実験的です。本番環境での使用は推奨されません。予告なく変更または削除される場合があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tiflow/issues)を報告してください。

バージョン8.5.6以降、DMは外部キー制約を使用するテーブルのレプリケーションに関する**実験的**サポートを提供します。このサポートには、以下の改善点が含まれます。

-   **セーフモード**: セーフモード実行中、DM は各バッチに対して`foreign_key_checks=0`を設定し、主キーまたは一意キーの値を変更しない`DELETE`ステートメントの冗長な`UPDATE` } ステップをスキップします。これにより、 `REPLACE INTO` (内部で`DELETE` + `INSERT`を実行) が子行に意図しない`ON DELETE CASCADE`効果を引き起こすのを防ぎます。詳細については、 [DMセーフモード](/dm/dm-safe-mode.md#foreign-key-handling-new-in-v856)を参照してください。
-   **マルチワーカー因果関係**: `worker-count > 1`の場合、DM はタスク開始時にダウンストリーム スキーマから外部キー関係を読み取り、因果関係キーを挿入します。これにより、親行に対する DML 操作が依存する子行に対する操作よりも先に完了し、ワーカー間でbinlogの順序が維持されます。

外部キーのレプリケーションには、以下の制限事項が適用されます。

-   セーフモードでは、DM は主キーまたは一意キーの値を変更する`UPDATE`ステートメントをサポートしていません。タスクはエラー`safe-mode update with foreign_key_checks=1 and PK/UK changes is not supported`で一時停止します。このようなステートメントを再現するには、 `safe-mode: false`を設定してください。
-   `foreign_key_checks=1`の場合、DM はレプリケーション中に外部キー制約を作成、変更、または削除する DDL ステートメントをサポートしません。
-   `worker-count > 1`の場合、テーブルルーティングはサポートされません。外部キーを含むテーブルでテーブルルーティングを使用する場合は、 `worker-count`を`1`に設定してください。
-   ブロック許可リストには、外部キー依存関係チェーン内のすべての祖先テーブルを含める必要があります。祖先テーブルが除外されている場合、増分レプリケーション中にエラーが発生し、タスクが一時停止します。
-   外部キーのメタデータは、ソースとダウンストリーム間で一貫している必要があります。不整合が検出された場合は、 `binlog-schema update --from-target`を実行してメタデータを再同期してください。
-   `ON UPDATE CASCADE`が主キーまたは一意キーの値を変更する場合、 `UPDATE`はセーフ モードで正しく複製されません。DM は、このようなステートメントを`DELETE` + `REPLACE`に書き換え、 `ON DELETE`アクションではなく`ON UPDATE`アクションをトリガーします。この場合、DM はステートメントを拒否し、タスクを一時停止します。キー値を変更しない`UPDATE`ステートメントは正しく複製されます。

バージョン8.5.6より前のバージョンでは、DMはダウンストリームに外部キー制約を作成しますが、セッション変数[`foreign_key_checks=OFF`](/system-variables.md#foreign_key_checks)設定するため、制約を適用しません。その結果、カスケード操作はダウンストリームに複製されません。

### MariaDBに関する注記 {#mariadb-notes}

-   MariaDB **10.5.11 以降**では、権限名の**変更**(例: `BINLOG MONITOR` 、 `REPLICATION SLAVE ADMIN` 、 `REPLICATION MASTER ADMIN` ) により、DM の事前チェックが失敗します。このエラーは、レプリケーション権限、ダンプ権限、およびダンプ接続番号のチェッカーで`[code=26005] fail to check synchronization configuration`として表示されます。
-   DM タスクに`ignore-checking-items: ["all"]`を追加すると、**事前チェックをバイパス**できます。詳細は[DM事前チェック](/dm/dm-precheck.md)をご覧ください。

## 対象データベース {#target-databases}

> **警告：**
>
> DM v5.3.0 は推奨されません。DM v5.3.0 でリレーログなしで GTID レプリケーションを有効にすると、データレプリケーションが失敗する可能性がありますが、その確率は低いです。

| 対象データベース | 互換性レベル       | DM版                    |
| -------- | ------------ | ---------------------- |
| TiDB 8.x | GA           | ≥ 5.3.1                |
| TiDB 7.x | GA           | ≥ 5.3.1                |
| TiDB 6.x | GA           | ≥ 5.3.1                |
| TiDB 5.4 | GA           | ≥ 5.3.1                |
| TiDB 5.3 | GA           | ≥ 5.3.1                |
| TiDB 5.2 | GA           | ≥ 2.0.7、推奨バージョン: 5.4   |
| TiDB 5.1 | GA           | ≥ 2.0.4、推奨バージョン: 5.4   |
| TiDB 5.0 | GA           | ≥ 2.0.4、推奨バージョン: 5.4   |
| TiDB 4.x | GA           | ≥ 2.0.1、推奨バージョン: 2.0.7 |
| TiDB 3.x | GA           | ≥ 2.0.1、推奨バージョン: 2.0.7 |
| MySQL    | Experimental |                        |
| MariaDB  | Experimental |                        |
