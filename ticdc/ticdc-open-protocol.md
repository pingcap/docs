---
title: TiCDC Open Protocol
summary: TiCDC オープン プロトコルの概念とその使用方法を学びます。
---

# TiCDCオープンプロトコル {#ticdc-open-protocol}

TiCDCオープンプロトコルは、行レベルのデータ変更通知プロトコルであり、監視、キャッシュ、全文インデックス作成、分析エンジン、そして異なるデータベース間のプライマリ-セカンダリレプリケーションのためのデータソースを提供します。TiCDCはTiCDCオープンプロトコルに準拠しており、TiDBのデータ変更をMQ（メッセージキュー）などのサードパーティのデータメディアに複製します。

TiCDCオープンプロトコルは、データ変更イベントを下流に複製するための基本単位としてイベントを使用します。イベントは以下の3つのカテゴリに分類されます。

-   行変更イベント：行のデータ変更を表します。行が変更されると、このイベントが送信され、変更された行に関する情報が含まれます。
-   DDLイベント：DDLの変更を表します。このイベントは、上流でDDL文が正常に実行された後に送信されます。DDLイベントはすべてのMQパーティションにブロードキャストされます。
-   解決されたイベント: 受信したイベントが完了する特別な時点を表します。

## 制限 {#restrictions}

-   ほとんどの場合、バージョンの行変更イベントは 1 回だけ送信されますが、ノード障害やネットワーク パーティションなどの特別な状況では、同じバージョンの行変更イベントが複数回送信されることがあります。
-   同じテーブルで、最初に送信された各バージョンの行変更イベントは、イベント ストリーム内のタイムスタンプ (TS) の順に増加します。
-   解決済みイベントは、各MQパーティションに定期的にブロードキャストされます。解決済みイベントとは、解決済みイベントTSよりも前のTSを持つイベントがダウンストリームに送信されたことを意味します。
-   DDL イベントは各 MQ パーティションにブロードキャストされます。
-   1 つの行の複数の行変更イベントが同じ MQ パーティションに送信されます。

## メッセージ形式 {#message-format}

メッセージには、次の形式で配置された 1 つ以上のイベントが含まれます。

鍵：

| オフセット(バイト) | 0～7        | 8～15 | 16～(15+長さ1) | ... | ...     |
| :--------- | :--------- | :--- | :---------- | :-- | :------ |
| パラメータ      | プロトコルバージョン | 長さ1  | イベントキー1     | 長さN | イベントキーN |

値：

| オフセット(バイト) | 0～7 | 8～(7+長さ1) | ... | ...    |
| :--------- | :-- | :-------- | :-- | :----- |
| パラメータ      | 長さ1 | イベント値1    | 長さN | イベント値N |

-   `LengthN` `N`番目のキー/値の長さを表します。
-   長さとプロトコルバージョンはビッグエンディアン`int64`型です。
-   現在のプロトコルのバージョンは`1`です。

## イベント形式 {#event-format}

このセクションでは、行変更イベント、DDL イベント、解決イベントの形式について説明します。

### 行変更イベント {#row-changed-event}

-   **鍵：**

    ```json
    {
        "ts":<TS>,
        "scm":<Schema Name>,
        "tbl":<Table Name>,
        "t":1
    }
    ```

    | パラメータ | 型 | 説明                           |
    | :--------- | :-- | :--------------------------- |
    | TS         | number  | 行の変更を引き起こしたトランザクションのタイムスタンプ。 |
    | Schema Name | string   | 行が含まれているスキーマの名前。             |
    | Table Name  | string   | 行が含まれているテーブルの名前。             |

-   **値：**

    `Insert`イベント。新しく追加された行データが出力されます。

    ```json
    {
        "u":{
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "f":<Flag>,
                "v":<Column Value>
            },
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "f":<Flag>,
                "v":<Column Value>
            }
        }
    }
    ```

    `Update`イベント。新しく追加された行データ（&quot;u&quot;）と更新前の行データ（&quot;p&quot;）が出力されます。

    ```json
    {
        "u":{
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "f":<Flag>,
                "v":<Column Value>
            },
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "f":<Flag>,
                "v":<Column Value>
            }
        },
        "p":{
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "f":<Flag>,
                "v":<Column Value>
            },
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "f":<Flag>,
                "v":<Column Value>
            }
        }
    }
    ```

    `Delete`イベント。削除された行データが出力されます。

    ```json
    {
        "d":{
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "f":<Flag>,
                "v":<Column Value>
            },
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "f":<Flag>,
                "v":<Column Value>
            }
        }
    }
    ```

    | Parameter | 型  | 説明                                                                                |
    | :-------- | :--- | :-------------------------------------------------------------------------------- |
    | カラム名      | string    | 列名。                                                                               |
    | カラムタイプ    | number   | 列の種類。詳細は[カラムタイプコード](#column-type-code)を参照してください。                                   |
    | ハンドル      | boolean | この列が`Where`節のフィルター条件に使用できるかどうかを判断します。この列がテーブル上で一意の場合、 `Where Handle`は`true`になります。 |
    | フラグ       | number   | 列のビットフラグ。詳細は[列のビットフラグ](#bit-flags-of-columns)参照。                                  |
    | カラムの値     | どれでも | カラムの値。                                                                            |

### DDLイベント {#ddl-event}

-   **鍵：**

    ```json
    {
        "ts":<TS>,
        "scm":<Schema Name>,
        "tbl":<Table Name>,
        "t":2
    }
    ```

    | パラメータ | 型 | 説明                            |
    | :--- | :--- | :--------------------------- |
    | TS    | number  | DDL 変更を実行するトランザクションのタイムスタンプ。  |
    | スキーマ名 | string   | DDL 変更のスキーマ名。空の文字列になる場合があります。 |
    | テーブル名 | string   | DDL 変更のテーブル名。空の文字列になる場合があります。 |

-   **値：**

    ```json
    {
        "q":<DDL Query>,
        "t":<DDL Type>
    }
    ```

    | パラメータ  | Type | 説明                                             |
    | :----- | :--- | :--------------------------------------------- |
    | DDLクエリ | string    | DDLクエリSQL                                      |
    | DDLタイプ | string    | DDLタイプ。詳細は[DDLタイプコード](#ddl-type-code)を参照してください。 |

### 解決されたイベント {#resolved-event}

-   **鍵：**

    ```json
    {
        "ts":<TS>,
        "t":3
    }
    ```

    | パラメータ | 型 | 説明                                |
    | :---- | :-- | :-------------------------------- |
    | TS    | number  | 解決されたタイムスタンプ。このイベントより前のTSは送信済みです。 |

-   **Value:** None

## イベントストリーム出力の例 {#examples-of-the-event-stream-output}

このセクションでは、イベント ストリームの出力ログを表示します。

アップストリームで次の SQL ステートメントを実行し、MQ パーティション番号が 2 であるとします。

```sql
CREATE TABLE test.t1(id int primary key, val varchar(16));
```

次のログ 1 とログ 3 から、DDL イベントがすべての MQ パーティションにブロードキャストされ、解決されたイベントが各 MQ パーティションに定期的にブロードキャストされていることがわかります。

    1. [partition=0] [key="{\"ts\":415508856908021766,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":2}"] [value="{\"q\":\"CREATE TABLE test.t1(id int primary key, val varchar(16))\",\"t\":3}"]
    2. [partition=0] [key="{\"ts\":415508856908021766,\"t\":3}"] [value=]
    3. [partition=1] [key="{\"ts\":415508856908021766,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":2}"] [value="{\"q\":\"CREATE TABLE test.t1(id int primary key, val varchar(16))\",\"t\":3}"]
    4. [partition=1] [key="{\"ts\":415508856908021766,\"t\":3}"] [value=]

アップストリームで次の SQL ステートメントを実行します。

```sql
BEGIN;
INSERT INTO test.t1(id, val) VALUES (1, 'aa');
INSERT INTO test.t1(id, val) VALUES (2, 'aa');
UPDATE test.t1 SET val = 'bb' WHERE id = 2;
INSERT INTO test.t1(id, val) VALUES (3, 'cc');
COMMIT;
```

-   次のログ 5 とログ 6 から、同じテーブル上の行変更イベントは主キーに基づいて異なるパーティションに送信される可能性がありますが、同じ行への変更は同じパーティションに送信されるため、ダウンストリームでイベントを簡単に同時に処理できることがわかります。
-   ログ 6 以降、トランザクション内の同じ行に対する複数の変更は、1 つの行変更イベントでのみ送信されます。
-   ログ 8 は、ログ 7 の繰り返しイベントです。行変更イベントは繰り返される可能性がありますが、各バージョンの最初のイベントは順番に送信されます。

<!---->

    5. [partition=0] [key="{\"ts\":415508878783938562,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":1},\"val\":{\"t\":15,\"v\":\"aa\"}}}"]
    6. [partition=1] [key="{\"ts\":415508878783938562,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":2},\"val\":{\"t\":15,\"v\":\"bb\"}}}"]
    7. [partition=0] [key="{\"ts\":415508878783938562,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":3},\"val\":{\"t\":15,\"v\":\"cc\"}}}"]
    8. [partition=0] [key="{\"ts\":415508878783938562,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":3},\"val\":{\"t\":15,\"v\":\"cc\"}}}"]

アップストリームで次の SQL ステートメントを実行します。

```sql
BEGIN;
DELETE FROM test.t1 WHERE id = 1;
UPDATE test.t1 SET val = 'dd' WHERE id = 3;
UPDATE test.t1 SET id = 4, val = 'ee' WHERE id = 2;
COMMIT;
```

-   ログ9は、 `Delete`タイプの行変更イベントです。このタイプのイベントには、主キー列または一意インデックス列のみが含まれます。
-   ログ13とログ14は解決済みイベントです。解決済みイベントとは、このパーティションにおいて、解決済みTSよりも小さいイベント（行変更イベントとDDLイベントを含む）が送信されたことを意味します。

<!---->

    9. [partition=0] [key="{\"ts\":415508881418485761,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"d\":{\"id\":{\"t\":3,\"h\":true,\"v\":1}}}"]
    10. [partition=1] [key="{\"ts\":415508881418485761,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"d\":{\"id\":{\"t\":3,\"h\":true,\"v\":2}}}"]
    11. [partition=0] [key="{\"ts\":415508881418485761,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":3},\"val\":{\"t\":15,\"v\":\"ZGQ=\"}}}"]
    12. [partition=0] [key="{\"ts\":415508881418485761,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":4},\"val\":{\"t\":15,\"v\":\"ZWU=\"}}}"]
    13. [partition=0] [key="{\"ts\":415508881038376963,\"t\":3}"] [value=]
    14. [partition=1] [key="{\"ts\":415508881038376963,\"t\":3}"] [value=]

## 消費者向けプロトコル解析 {#protocol-parsing-for-consumers}

現在、TiCDCはTiCDCオープンプロトコル用の標準解析ライブラリを提供していませんが、 Golang版とJava版の解析例が提供されています。このドキュメントで提供されているデータ形式と以下の例を参考に、コンシューマー向けのプロトコル解析を実装できます。

-   [Golangの例](https://github.com/pingcap/tiflow/tree/release-8.5/cmd/kafka-consumer)
-   [Javaの例](https://github.com/pingcap/tiflow/tree/release-8.5/examples/java)

## カラムタイプコード {#column-type-code}

`Column Type Code` 、行変更イベントの列データ型を表します。

| 型                     | コード    | 出力例                                                                                                                      | 説明                                                          |
| :-------------------- | :----- | :----------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------- |
| TINYINT/BOOLEAN       | 1      | {"t":1,"v":1}                                                                                                            |                                                             |
| SMALLINT              | 2      | {&quot;t&quot;:2,&quot;v&quot;:1}                                                                                        |                                                             |
| INT                   | 3      | {&quot;t&quot;:3,&quot;v&quot;:123}                                                                                      |                                                             |
| FLOAT                 | 4      | {&quot;t&quot;:4,&quot;v&quot;:153.123}                                                                                  |                                                             |
| DOUBLE                | 5      | {&quot;t&quot;:5,&quot;v&quot;:153.123}                                                                                  |                                                             |
| NULL                  | 6      | {&quot;t&quot;:6,&quot;v&quot;:null}                                                                                     |                                                             |
| TIMESTAMP             | 7      | {&quot;t&quot;:7,&quot;v&quot;:&quot;1973-12-30 15:30:00&quot;}                                                          |                                                             |
| BIGINT                | 8      | {&quot;t&quot;:8,&quot;v&quot;:123}                                                                                      |                                                             |
| MEDIUMINT             | 9      | {&quot;t&quot;:9,&quot;v&quot;:123}                                                                                      |                                                             |
| DATE                  | 10/14 | {&quot;t&quot;:10,&quot;v&quot;:&quot;2000-01-01&quot;}                                                                  |                                                             |
| TIME                  | 11     | {&quot;t&quot;:11,&quot;v&quot;:&quot;23:59:59&quot;}                                                                    |                                                             |
| DATETIME              | 12     | {&quot;t&quot;:12,&quot;v&quot;:&quot;2015-12-20 23:58:58&quot;}                                                         |                                                             |
| YEAR                  | 13     | {&quot;t&quot;:13,&quot;v&quot;:1970}                                                                                    |                                                             |
| VARCHAR/VARBINARY     | 15/253 | {&quot;t&quot;:15,&quot;v&quot;:&quot;テスト&quot;} / {&quot;t&quot;:15,&quot;v&quot;:&quot;\\x89PNG\\r\\n\\x1a\\n&quot;}   | 値はUTF-8でエンコードされます。アップストリームの型がVARBINARYの場合、非表示の文字はエスケープされます。 |
| BIT                   | 16     | {&quot;t&quot;:16,&quot;v&quot;:81}                                                                                      |                                                             |
| JSON                  | 245    | {&quot;t&quot;:245,&quot;v&quot;:&quot;{\&quot;キー1\&quot;: \&quot;値1\&quot;}&quot;}                                      |                                                             |
| DECIMAL               | 246    | {&quot;t&quot;:246,&quot;v&quot;:&quot;129012.1230000&quot;}                                                             |                                                             |
| ENUM                  | 247    | {&quot;t&quot;:247,&quot;v&quot;:1}                                                                                      |                                                             |
| SET                   | 248    | {&quot;t&quot;:248,&quot;v&quot;:3}                                                                                      |                                                             |
| TINYTEXT/TINYBLOB     | 249    | {&quot;t&quot;:249,&quot;v&quot;:&quot;5rWL6K+VdGV4dA==&quot;}                                                           | 値は Base64 でエンコードされます。                                       |
| MEDIUMTEXT/MEDIUMBLOB | 250    | {&quot;t&quot;:250,&quot;v&quot;:&quot;5rWL6K+VdGV4dA==&quot;}                                                           | 値は Base64 でエンコードされます。                                       |
| LONGTEXT/LONGBLOB     | 251    | {&quot;t&quot;:251,&quot;v&quot;:&quot;5rWL6K+VdGV4dA==&quot;}                                                           | 値は Base64 でエンコードされます。                                       |
| TEXT/BLOB             | 252    | {&quot;t&quot;:252,&quot;v&quot;:&quot;5rWL6K+VdGV4dA==&quot;}                                                           | 値は Base64 でエンコードされます。                                       |
| CHAR/BINARY           | 254    | {&quot;t&quot;:254,&quot;v&quot;:&quot;テスト&quot;} / {&quot;t&quot;:254,&quot;v&quot;:&quot;\\x89PNG\\r\\n\\x1a\\n&quot;} | 値はUTF-8でエンコードされます。アップストリームの型がBINARYの場合、非表示の文字はエスケープされます。    |
| TiDBVectorFloat32     | 225    | {&quot;t&quot;:225,&quot;v&quot;:&quot;[1.23, -0.4]&quot;}                                                               |                                                             |
| GEOMETRY              | 255    |                                                                                                                          | Unsupported                                                 |

## DDLタイプコード {#ddl-type-code}

`DDL Type Code` 、DDL イベントの DDL ステートメント タイプを表します。

| Type                              | Code |
| :-------------------------------- | :-- |
| Create Schema                     | 1   |
| Drop Schema                       | 2   |
| Create Table                      | 3   |
| Drop Table                        | 4   |
| Add Column                        | 5   |
| Drop Column                       | 6   |
| Add Index                         | 7   |
| Drop Index                        | 8   |
| Add Foreign Key                   | 9   |
| Drop Foreign Key                  | 10  |
| Truncate Table                    | 11  |
| Modify Column                     | 12  |
| Rebase Auto ID                    | 13  |
| Rename Table                      | 14  |
| Set Default Value                 | 15  |
| Shard RowID                       | 16  |
| Modify Table Comment              | 17  |
| Rename Index                      | 18  |
| Add Table Partition               | 19  |
| Drop Table Partition              | 20  |
| Create View                       | 21  |
| Modify Table Charset And Collate  | 22  |
| Truncate Table Partition          | 23  |
| Drop View                         | 24  |
| Recover Table                     | 25  |
| Modify Schema Charset And Collate | 26  |
| Lock Table                        | 27  |
| Unlock Table                      | 28  |
| Repair Table                      | 29  |
| Set TiFlash Replica               | 30  |
| Update TiFlash Replica Status     | 31  |
| Add Primary Key                   | 32  |
| Drop Primary Key                  | 33  |
| Create Sequence                   | 34  |
| Alter Sequence                    | 35  |
| Drop Sequence                     | 36  |

## 列のビットフラグ {#bit-flags-of-columns}

ビット フラグは列の特定の属性を表します。

| Bit | Value | Name                | 説明                      |
| :- | :--- | :------------------ | :---------------------- |
| 1  | 0x01 | BinaryFlag          | 列がバイナリエンコードされた列であるかどうか。 |
| 2  | 0x02 | HandleKeyFlag       | 列がハンドル インデックス列であるかどうか。  |
| 3  | 0x04 | GeneratedColumnFlag | 列が生成された列であるかどうか。        |
| 4  | 0x08 | PrimaryKeyFlag      | 列が主キー列であるかどうか。          |
| 5  | 0x10 | UniqueKeyFlag       | 列が一意インデックス列であるかどうか。    |
| 6  | 0x20 | MultipleKeyFlag     | 列が複合インデックス列であるかどうか。     |
| 7  | 0x40 | NullableFlag        | 列が NULL 可能列であるかどうか。     |
| 8  | 0x80 | UnsignedFlag        | 列が符号なし列であるかどうか。         |

例：

列フラグの値が`85`の場合、その列は NULL 可能列、一意インデックス列、生成された列、およびバイナリ エンコード列になります。

    85 == 0b_101_0101
       == NullableFlag | UniqueKeyFlag | GeneratedColumnFlag | BinaryFlag

列の値が`46`の場合、その列は複合インデックス列、主キー列、生成列、およびハンドル キー列になります。

    46 == 0b_010_1110
       == MultipleKeyFlag | PrimaryKeyFlag | GeneratedColumnFlag | HandleKeyFlag

> **Note:**
>
> -   `BinaryFlag` 、列の型が BLOB/ TEXT （TINYBLOB/TINYTEXT、BINARY/CHAR を含む）の場合にのみ意味を持ちます。上流の列が BLOB 型の場合、 `BinaryFlag`値は`1`に設定されます。上流の列がTEXT型の場合、 `BinaryFlag`値は`0`に設定されます。
> -   TiCDCは、上流からテーブルを複製するために、ハンドルインデックスとして[有効なインデックス](/ticdc/ticdc-overview.md#best-practices)選択します。ハンドルインデックス列の`HandleKeyFlag`の値は`1`に設定されます。
