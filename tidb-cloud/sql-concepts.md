---
title: SQL
summary: TiDBにおけるSQLの概念について学びましょう。
---

# SQL {#sql}

TiDBはMySQLプロトコルと高い互換性を持ち、 MySQL 5.7およびMySQL 8.0の共通機能と構文に対応しています。MySQLのエコシステムツール（PHPMyAdmin、Navicat、MySQL Workbench、DBeaver [もっと](/develop/dev-guide-third-party-support.md#gui)）およびMySQLクライアントはTiDBで使用できます。

ただし、TiDBではMySQLの一部の機能はサポートされていません。これは、問題を解決するより良い方法（XML関数の代わりにJSONを使用するなど）が存在するため、または必要な労力に対して現在の需要が不足しているため（ストアドプロシージャや関数など）です。さらに、一部の機能は分散システムでの実装が難しい場合があります。詳細については、 [MySQLとの互換性](/mysql-compatibility.md)を参照してください。

## SQL文 {#sql-statements}

SQL文とは、SQL（構造化照会言語）におけるコマンドまたは命令であり、識別子、パラメータ、変数、データ型、および予約済みのSQLキーワードで構成されます。これは、データベースに対して、データの取得、変更、管理、データベース構造の管理といった特定のアクションを実行するように指示します。

TiDBは、ISO/IEC SQL標準に準拠することを目的としたSQL文を使用しており、必要に応じてMySQL用の拡張機能やTiDB固有の文が追加されています。

SQLは、その関数に応じて以下の4種類に分類されます。

-   DDL (データ定義言語): データベース、テーブル、ビュー、インデックスなどのデータベース オブジェクトを定義するために使用されます。 TiDB の DDL ステートメントについては、 [スキーマ管理／データ定義文（DDL）](/sql-statements/sql-statement-overview.md#schema-management--data-definition-statements-ddl)を参照してください。

-   DML（データ操作言語）：アプリケーション関連のレコードを操作するために使用されます。TiDB の DML ステートメントについては、 [データ操作文（DML）](/sql-statements/sql-statement-overview.md#data-manipulation-statements-dml)を参照してください。

-   DQL（データクエリ言語）：条件付きフィルタリング後のレコードをクエリするために使用されます。

-   DCL（データ制御言語）：アクセス権限とセキュリティレベルを定義するために使用されます。

TiDB の SQL ステートメントの概要については、 [SQLステートメントの概要](/sql-statements/sql-statement-overview.md)参照してください。

## SQLモード {#sql-mode}

TiDBサーバーは複数のSQLモードで動作し、クライアントごとに異なる方法でこれらのモードを適用します。SQLモードでは、TiDBがサポートするSQL構文と、実行するデータ検証チェックの種類が定義されます。

詳細については、 [SQLモード](/sql-mode.md)を参照してください。

## 行ID生成属性 {#row-id-generation-attributes}

TiDBは、行IDの生成とデータ配信を最適化するための3つのSQL属性を提供します。

-   AUTO_INCREMENT

-   AUTO_RANDOM

-   SHARD_ROW_ID_BITS

### AUTO_INCREMENT {#auto-increment}

`AUTO_INCREMENT`は、列のデフォルト値を自動的に入力するために使用される列属性です。 `INSERT`ステートメントで`AUTO_INCREMENT`列の値が指定されていない場合、システムはこの列に値を自動的に割り当てます。

パフォーマンス上の理由から、 `AUTO_INCREMENT`番号は、各 TiDBサーバーに値のバッチ (デフォルトでは 30 千) で割り当てられます。つまり、 `AUTO_INCREMENT`番号は一意であることが保証されますが、 `INSERT`ステートメントに割り当てられる値は、TiDBサーバーごとに単調増加になります。

すべての TiDB サーバーで`AUTO_INCREMENT`の数値を単調増加にしたい場合、また TiDB のバージョンが v6.5.0 以降の場合は、[MySQL互換モード](/auto-increment.md#mysql-compatibility-mode)を有効にすることをお勧めします。

詳細については、[AUTO_INCREMENT](/auto-increment.md)を参照してください。

### AUTO_RANDOM {#auto-random}

`AUTO_RANDOM`は`BIGINT`列に値を自動的に割り当てるために使用される列属性です。自動的に割り当てられる値はランダムで一意です。 `AUTO_RANDOM`の値はランダムで一意であるため、TiDB が連続する ID を割り当てることによって単一のストレージノードで発生する書き込みホットスポットを回避するために、 [`AUTO_INCREMENT`](/auto-increment.md)の代わりに`AUTO_RANDOM`よく使用されます。

`AUTO_RANDOM`の値はランダムかつ一意であるため、TiDB が連続する ID を割り当てることによって単一のストレージノードで発生する書き込みホットスポットを回避するために、 [`AUTO_INCREMENT`](/auto-increment.md)の代わりに`AUTO_RANDOM`がよく使用されます。現在の`AUTO_INCREMENT`列が主キーであり、型が`BIGINT`の場合、 `ALTER TABLE t MODIFY COLUMN id BIGINT AUTO_RANDOM(5);`ステートメントを実行して、 `AUTO_INCREMENT`から`AUTO_RANDOM`に切り替えることができます。

詳細については、[AUTO_RANDOM](/auto-random.md)を参照してください。

### SHARD_ROW_ID_BITS {#shard-row-id-bits}

クラスタ化されていないプライマリキーまたはプライマリキーのないテーブルの場合、TiDB は暗黙的なAUTO_INCREMENT行 ID を使用します。 `INSERT`操作が多数実行されると、データが単一のリージョンに書き込まれるため、書き込みホットスポットが発生します。

ホットスポットの問題を軽減するには、 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)を設定できます。行 ID は分散しており、データは複数の異なるリージョンに書き込まれます。

## キーワード {#keywords}

キーワードとは、 `SELECT` 、 `UPDATE` 、 `DELETE`のように、SQL ステートメントで特別な意味を持つ単語です。

-   それらのいくつかは、識別子として直接使用することができ、それらは非予約キーワードと呼ばれます。

-   それらのいくつかは、識別子として使用する前に特別な処理が必要であり、予約キーワードと呼ばれます。

ただし、予約語ではないキーワードでも、特別な対応が必要になる場合があります。そのようなキーワードは、予約語として扱うことをお勧めします。

詳細については、[キーワード](/keywords.md)を参照してください。

## ユーザー定義変数 {#user-defined-variables}

TiDB では、ユーザー定義変数を設定および読み取ることができます。ユーザー定義変数の形式は`@var_name`です。 `var_name`を構成する文字は、数字`0-9` 、文字`a-zA-Z` 、ドル記号`_` 、および UTF-8 文字など、識別子を構成できる任意の文字です。さらに、英語のピリオド`.` `$`含まれます。ユーザー定義変数は大文字と小文字を区別しません。

ユーザー定義変数はセッション固有のものであり、あるクライアント接続で定義されたユーザー変数は、他のクライアント接続からは参照または使用できません。

詳細については、[ユーザー定義変数](/user-defined-variables.md)を参照してください。

## メタデータロック {#metadata-lock}

TiDBでは、メタデータロックは、オンラインスキーマ変更中にテーブルメタデータの変更を管理するために導入されたメカニズムです。トランザクションが開始されると、現在のメタデータのスナップショットにロックされます。トランザクション中にメタデータが変更されると、TiDBは「情報スキーマが変更されました」というエラーをスローし、トランザクションのコミットを阻止します。メタデータロックは、データ操作言語（DML）とデータ定義言語（DDL）の操作を調整し、DMLの優先順位付けを行うことで、古いメタデータを持つ進行中のDMLトランザクションが新しいDDL変更を適用する前にコミットされるようにし、エラーを最小限に抑え、データの一貫性を維持します。

詳細については、[メタデータロック](/metadata-lock.md)参照してください。
